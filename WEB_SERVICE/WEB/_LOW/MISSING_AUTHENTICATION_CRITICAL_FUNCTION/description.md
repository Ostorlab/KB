A critical function that mutates security-relevant state (such as a webhook that persists inbound messages into a database, or any endpoint that writes, deletes, or returns sensitive data) is reachable without authentication and without verifying an authenticator proving the caller's identity.

When the only protection on such a function is a CSRF exemption (e.g. `@csrf.csrf_exempt`) or none at all, any anonymous internet user can invoke it. Request parameters are then taken verbatim from attacker-controlled input and persisted or acted upon unconditionally, so a single unauthenticated request can forge a row, pollute a shared data store, amplify storage with no rate limit, or trigger a privileged side effect — all while the endpoint derives no trusted identity from the caller.

This is CWE-306 (Missing Authentication for a Critical Function). It is distinct from a broken *authorization* check (CWE-862): here there is no authentication of the principal in the first place, so authorization decisions cannot be made at all. It is also distinct from CSRF (CWE-352): CSRF abuses a *session* principal; this flaw has no principal and is therefore forgeable by any anonymous party.

A common instance is a third-party provider webhook (e.g. an SMS provider such as Vonage, or a payment / event provider) that documents an HMAC signature header. The receiving view is `@csrf_exempt`, performs no `vonage-signature` / `X-Provider-Signature` HMAC verification, no authentication, no `Origin`/`Referer` check, and no IP allowlist, then writes fields straight from `request.GET` / `request.POST` into a model with no tenant scope:

```python
@csrf.csrf_exempt
def sms_webhook_view(request):
    if request.GET:
        sender = request.GET.get("msisdn") or request.GET.get("From")
        message = request.GET.get("text") or request.GET.get("Body")
        if sender is not None and message is not None:
            models.SMS.objects.create(sender=sender, message=message)
    return http.HttpResponse("OK")
```

A trivial unauthenticated request injects a forged row with no token or signature required:

```http
GET /webhooks/sms?msisdn=%2B15551234567&to=%2B15557654321&text=forged-row HTTP/1.1
```

**Impact bounding:** when no downstream consumer treats the persisted payload as an OTP / 2FA / account-recovery code for the platform's own authentication, the impact is bounded to data-integrity pollution (poisoned admin inbox and authenticated query results, where an injected row can become "latest" for a chosen key) plus unlimited row amplification / storage pressure (no rate limit). It is **not** an authentication or 2FA bypass on its own; the rating reflects that bounded integrity impact.
