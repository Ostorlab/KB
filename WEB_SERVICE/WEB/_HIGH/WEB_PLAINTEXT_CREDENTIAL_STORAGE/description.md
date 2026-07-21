Credential secrets such as passwords, TOTP seeds, TLS private keys, credit-card PAN/CVV, embedded API keys and bearer
tokens are persisted to a database, file, key/value store or cache using a plain field/column type with no
encryption-at-rest layer. Because the value is written and read verbatim, anyone with database, backup, dump or admin
access recovers the usable secret with zero cryptographic work, and any authenticated read path that returns the field
unmasked amplifies the exposure over the API.

This vulnerability covers any of the following secret classes stored as cleartext:

* User passwords and reusable login credentials (Basic/Email2FA).
* TOTP shared secrets (the long-term seed used to generate every 2FA code).
* TLS certificates and private-key material (PEM).
* Payment-card data: PAN, expiration date and CVV/CVC.
* Executable scripts that embed inline secrets.
* Key/value secret stores (HStore/JSON) holding third-party API keys and tokens.
* Request header stores holding `Authorization` / `Bearer` / `Cookie` values.

The following example shows plaintext credential storage in a Django model where every secret-bearing field is a plain
`CharField`/`TextField`/`IntegerField`/`HStoreField` and the `save()` method performs no encryption:

=== "Python"

    ```python
    from django.contrib.postgres import fields
    from django.db import models


    class LoginPasswordTestCredentials(models.Model):
        login = models.CharField(max_length=250, null=True, blank=True)
        password = models.CharField(max_length=250, null=True, blank=True)


    class Totp2FATestCredentials(models.Model):
        totp_secret = models.CharField(max_length=128)


    class TlsCertificateTestCredentials(models.Model):
        tls_certificate = models.TextField()


    class CreditCardTestCredentials(models.Model):
        credit_card_number = models.CharField(max_length=64)
        expiration_date = models.CharField(max_length=16)
        cvv = models.IntegerField()  # CVV must never be stored post-authorization.


    class CustomTestCredentials(models.Model):
        credentials = fields.HStoreField(null=True, blank=True)
    ```

## Impact

* Account takeover and lateral movement through recovered reusable passwords.
* Full 2FA bypass by deriving valid time-based codes from the recovered TOTP seed.
* Server/service impersonation, TLS MITM and certificate minting from recovered private keys.
* Card-not-present fraud from recovered PAN + expiry + CVV; storing CVV post-authorization is a direct
  PCI DSS Requirement 3 violation regardless of exploitation.
* Abuse of embedded third-party API keys and bearer tokens against their respective providers.

The exposure spans every credential of the affected class across every organisation in the database, and the cleartext
store amplifies any separate response-layer disclosure because the values returned are the verbatim stored secrets.
