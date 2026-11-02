The Brotli decompression library contains an out-of-bounds write in the streaming decoder (CVE-2026-111497, CVSS 9.8, CWE-787, tracked by researchers as **Node2Shell**). Google Brotli versions **1.0.3 through 1.2.0** on all platforms are affected, and the upstream advisories describe the mechanism precisely: an **invalid block switch was reported as a temporary need for more input instead of a permanent format error**, so the streaming decoder kept appending input bytes to an **eight-byte internal buffer**, writing past the end of it. A remote unauthenticated attacker who can supply Brotli data that an application decompresses can corrupt adjacent decoder state memory — causing a crash, disclosure of memory contents, a denial of service, or potentially arbitrary code execution. Fixed releases: **1.0.10** (1.0.x line), **1.1.1** (1.1.x line) and **1.2.1** (1.2.x line).

CISA added CVE-2026-111497 to the Known Exploited Vulnerabilities catalog on October 27, 2026; exploitation tooling for stock runtime builds circulates widely, and the entry records observed malicious use.

### Where the library is embedded — the affected surface

Because Brotli ships inside runtimes and bindings, the vulnerable surface is much broader than servers running the C library directly:

* **Node.js** — the decoder is bundled with `node:zlib`; Node.js 22.x, 24.x and 26.x are affected, fixed in **22.23.4 / 24.22.1 / 26.12.1** (October 21, 2026 security releases). Any Node application that calls `zlib.brotliDecompress`-family APIs on untrusted input is exposed.
* **Microsoft .NET** — `System.IO.Compression.Brotli`; fixed in **8.0.33, 9.0.22, 10.0.14** and the .NET 11 final previews/RC. Any .NET service that decompresses request bodies with `Content-Encoding: br` is exposed.
* **Go** — `github.com/andybalholm/brotli` embeds the C decoder; fixed in **v1.2.7**.
* **Python** — PyPI `brotli` fixed in **1.2.1**, `brotlicffi` fixed in **1.2.1.0**.
* Broader embedding per the advisory ecosystem records: Envoy, Istio, Bun, WOFF2 tooling (web fonts embed Brotli streams), DuckDB, ClickHouse, Apache Arrow, 7-Zip variants, and vendor firmware — each shipping their own fixed-version guidance. Anything that decodes **WOFF2 fonts or Brotli-compressed archives from untrusted sources** should be treated as exposed until its fixed version is confirmed.

The security property that fails is generic: **a server or client that decompresses attacker-controlled Brotli streams with an affected decoder version**. The common remotely exposed pattern is an HTTP service that accepts request bodies with `Content-Encoding: br` (APIs and proxies doing request-body decompression); the encoder side (a server that merely *sends* brotli-compressed responses when the client advertises `Accept-Encoding: br`) is **not** this vulnerability.

### Distinguishing a real finding from a benign lookalike

* Concrete evidence is a **library or runtime version in the affected range**: google/brotli in [1.0.3, 1.0.10) ∪ [1.1.0, 1.1.1) ∪ [1.2.0, 1.2.1), Node.js below 22.23.4 / 24.22.1 / 26.12.1, .NET below 8.0.33 / 9.0.22 / 10.0.14, `andybalholm/brotli` below 1.2.7, PyPI `brotli` below 1.2.1 — observed in dependency manifests/lockfiles, package metadata, or version strings of embedded native libraries (for example `libbrotlidec` symbols or `.so` version strings in server builds and mobile applications).
* **Servers that only emit brotli-compressed responses are not affected** — a response `Content-Encoding: br` header alone is not evidence of this vulnerability; the decoder must run on untrusted input.
* A runtime at or above the fixed version **is not** affected, even if it decompresses untrusted streams.
* For mobile applications: an embedded brotli library in the affected range is a finding when the app decompresses streams from outside the trust boundary (untrusted servers, message attachments, downloaded content); the version evidence comes from the packaged native library, not from network traffic.

  ```bash
    # Benign checks (no crafted payloads):
    # 1) Dependency side (source scans): look for the pinned versions.
    grep -rE "brotli|Brotli" package-lock.json go.mod requirements.txt pyproject.toml
    # 2) Runtime side (web server): confirm the Node.js runtime version.
    node --version   # 22.23.4 / 24.22.1 / 26.12.1 or later contain the fix.
    # 3) Embedded library: check version strings in packaged native binaries.
    strings libbrotlidec.so* | grep -iE "brotli|1\.[012]\."
  ```
