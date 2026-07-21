A webhook handler authenticates inbound requests by computing `HMAC(SECRET, str(org_id), sha256)` and comparing it to a value embedded in the request URL path. Because the HMAC message covers **only** the static organization id — not the request body, not the object-resolution key (`issue_key` / `sys_id` / `integrationId`), not path parameters, not a timestamp, and not a nonce — the value is a **deterministic, reusable per-org bearer secret** carried in the URL. Once a single per-org webhook URL is leaked or observed (e.g. visible to admins of the configured third-party system), the holder can submit arbitrary forged bodies until the secret rotates.

This is an access-control design flaw, not an unauthenticated free bypass: without the leaked per-org URL segment, `hmac.compare_digest` returns `False` and no state change occurs. The risk is therefore precondition-gated (low).

### Attack pattern

```http
POST /integrations/webhook/<vendor>/<leaked_per_org_hmac> HTTP/1.1
Content-Type: application/json

{ "<object-resolution key>": "<any mapped object of that org>",
  "<vendor fields>": "<attacker-controlled payload>" }
```

The server resolves the protected object from an attacker-controlled body/path key, recomputes `HMAC(SECRET, str(org.id))` derived from that object, matches the URL segment, and then mutates state from the attacker-controlled body — which is never HMAC'd.

### Vulnerable shape (Python / Django)

```python
@csrf_exempt
def webhook_view(request, webhook_hmac):
    event = json.loads(request.body)                 # body NOT HMAC'd
    obj = MappedObject.objects.get(key=event["key"])  # attacker-chosen key, NOT HMAC'd
    expected = hmac.new(SECRET, str(obj.organisation.id).encode(), hashlib.sha256).hexdigest()
    if hmac.compare_digest(webhook_hmac, expected):  # URL path vs static per-org HMAC
        # ... mutate state from attacker-controlled body fields ...
        obj.save()
```

### Impact

* **Integrity** — arbitrary mapped-object mutation (e.g. ticket `title`/`description`) for the leaked-URL org, scoped to objects whose resolution key exists in the integration map.
* **Integrity + Confidentiality (elevated variant)** — when the handler additionally performs an outbound fetch authenticated with the org's stored credential (e.g. an `api_key`) for an attacker-chosen resource, or creates privileged records (e.g. scans) under the org. One leaked per-org URL may expose **all** of the org's integrations when the HMAC depends only on `org.id`.

### Preconditions (why risk is low)

* Requires a leaked/observed per-org webhook URL whose path value equals `HMAC(SECRET, str(org.id))`.
* Without it, `hmac.compare_digest` is `False`: the handler performs no state change (typically a `200` no-op or explicit `403`).
* The static value is reusable until the shared `SECRET` is rotated; there is no per-request timestamp, nonce, or source-IP allowlist gating the route.
