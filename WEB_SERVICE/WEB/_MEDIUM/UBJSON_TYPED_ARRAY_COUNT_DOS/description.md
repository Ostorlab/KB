# UBJSON Typed-Array Count Marker Amplification Denial of Service

A web endpoint that decodes attacker-supplied [Universal Binary JSON](https://ubjson.org/type-specification/) (UBJSON) request bodies without an application-level size, count, or nesting guard is vulnerable to a CPU/memory amplification denial of service. The amplification primitive is the UBJSON typed-array count marker `[$<type>#<count>]`, which lets the client *declare* an element count that the decoder trusts before validating that the matching element bytes are present. The decoder therefore loops (and in some implementations pre-allocates) `count` times before raising an `Insufficient input` error, so the cost is driven by the attacker-declared integer count, not by the payload byte length.

A single request of a few bytes can declare a count in the billions and consume seconds of single-core CPU; a slightly larger count marker (for example an `int64` count near `10^18`) forces the decoder to attempt a multi-exabyte allocation and raises `MemoryError` immediately. Because the per-request cost is incurred *inside* the decode loop — before the exception is caught and a `400`/`500` is returned — the worker process typically survives a single request, so denial is realised through sustained concurrent tiny requests that starve the worker pool, saturate CPU, or trip the OOM killer. The impact is greatest on unauthenticated, CSRF-exempt endpoints (such as a public GraphQL route that accepts `Content-Type: application/ubjson`), where an attacker can fire many concurrent amplification requests without credentials.

The framework request-body size cap (for example Django's `DATA_UPLOAD_MAX_MEMORY_SIZE`) bounds the *byte* length of the payload but does **not** bound the declared-integer-count amplifier, whose cost is independent of payload size.

## Examples

### Amplifier payload

The typed-array count marker declares a huge element count with no matching element bytes. A 9-byte payload can declare a count of `2_000_000_000`:

```
Hex:   5b 24 69 23 6c 77 35 94 00
UBJSON: [  $  i  #  <int64 2_000_000_000>   (no element bytes)
```

Decoding this tiny payload burns seconds of single-core CPU before the decoder raises an "Insufficient input" error, because it iterates the declared count before validating that element bytes exist.

A 13-byte payload declares a count near `10^18` and triggers an immediate `MemoryError` as the decoder attempts to allocate for the declared count:

```
Hex:   5b 24 69 23 4c 0d e0 b6 b3 a7 64 00 00
UBJSON: [  $  i  #  <int64 ~10^18>            (no element bytes)
```

### Unauthenticated request

```http
POST /public_graphql HTTP/1.1
Host: <target>
Content-Type: application/ubjson
Content-Length: 9

<9 amplifier bytes>
```

## Security Impact

- **Denial of Service**: Sustained concurrent amplifier requests exhaust the worker pool and saturate CPU, degrading or completely disabling the service for legitimate users.
- **Resource Exhaustion**: A memory-amplifier count marker forces a huge allocation, tripping `MemoryError` and, under OS overcommit, the OOM killer.
- **Unauthenticated Reachability**: On endpoints that require no authentication (and are CSRF-exempt), the amplifier is reachable without any credentials, maximising the concurrency an attacker can sustain.
- **Amplification Independent of Payload Size**: The cost scales with the attacker-declared integer count, not the request byte length, so framework body-size caps alone do not bound the amplifier.
