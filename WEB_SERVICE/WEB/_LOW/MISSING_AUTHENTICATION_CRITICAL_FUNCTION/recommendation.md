Require and verify an authenticator proving the caller's identity on every inbound request to a critical function before any state-mutating operation, and reject requests that are missing or fail verification with `403 Forbidden`. A CSRF exemption (`@csrf.csrf_exempt`) only neutralizes Django's CSRF token check; it does not preclude — and must not replace — an independent signature or authentication check.

For a third-party provider webhook (e.g. an SMS provider such as Vonage), verify the provider's documented HMAC signature header in constant time before persisting anything:

```python
import base64
import hashlib
import hmac

from django.conf import settings
from django import http
from django.views.decorators import csrf

from webhooks import models


@csrf.csrf_exempt
def sms_webhook_view(request):
    secret = getattr(settings, "VONAGE_SIGNATURE_SECRET", "")
    signature = request.headers.get("vonage-signature") or request.headers.get(
        "x-vonage-signature"
    )
    if not secret or not signature:
        return http.HttpResponseForbidden()
    body = request.body
    expected = base64.b64encode(
        hmac.new(secret.encode(), body, hashlib.sha256).digest()
    ).decode()
    if not hmac.compare_digest(expected, signature):
        return http.HttpResponseForbidden()

    if request.method != "POST":
        return http.HttpResponseNotAllowed(["POST"])

    sender = request.POST.get("msisdn") or request.POST.get("From")
    receiver = request.POST.get("to") or request.POST.get("To")
    message = request.POST.get("text") or request.POST.get("Body")
    if sender and message:
        models.SMS.objects.create(sender=sender, receiver=receiver, message=message)
    return http.HttpResponse("OK")
```

Defense in depth:

  * **Verify before write.** Reject (and do **not** persist) on signature failure; never persist first and verify later.
  * **Constant-time compare.** Use `hmac.compare_digest` for the signature comparison; never use `==`.
  * **Require a configured secret.** Fail closed (`403`) when `VONAGE_SIGNATURE_SECRET` is empty or unset.
  * **Restrict the method.** Enforce the method the provider actually uses (typically `POST`); do not accept arbitrary `GET` into the write sink.
  * **IP allowlist.** If signature verification cannot be deployed immediately, add a temporary IP allowlist for the provider's documented egress ranges at the reverse proxy / WAF in front of the route.
  * **Rate limiting.** Add per-source-IP and per-`sender` throttling to prevent unlimited row amplification.
  * **Tenant scope.** If the persisted model is shared across tenants, add an organisation / tenant FK and scope all reads to the caller's tenant to close the related cross-tenant read (CWE-639 / CWE-200).
