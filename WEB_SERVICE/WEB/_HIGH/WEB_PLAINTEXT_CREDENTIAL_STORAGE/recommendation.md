Introduce an encryption-at-rest layer for every secret-bearing field and migrate existing plaintext data, while
removing any value that must never be persisted (such as the card CVV/CVC).

* Replace plain `CharField`/`TextField`/`IntegerField`/`HStoreField` secret columns with encrypted equivalents
  (for example `EncryptedCharField`, `EncryptedTextField`, `EncryptedIntegerField` from
  `django-fernet-fields` / `django-cryptography`).
* Never store the card CVV/CVC after authorization (PCI DSS Requirement 3.2.2 forbids CVV storage regardless of
  encryption). Remove the column entirely; do not merely encrypt it.
* Store key/value secret stores as a single encrypted JSON blob instead of a plaintext HStore.
* Manage the encryption (Fernet/AES) key in a secrets manager (HashiCorp Vault, AWS Secrets Manager, GCP Secret
  Manager). Never commit the key to the repository.
* Write a data migration that reads each existing plaintext row, encrypts the value, writes it back and drops the old
  plain columns.
* Decrypt before consumption: update every read path that ships secrets to downstream consumers (scan agents,
  auth routines, TLS contexts) so the decrypted value is only materialized in memory at the point of use.
* Mask every secret field in API/GraphQL responses so a read role alone never surfaces usable material.
* Restrict, audit and rotate database, backup and admin access, and rotate any hardcoded development/test database
  credentials.

=== "Python"

    ```python
    from cryptography_fields.fields import (
        EncryptedCharField,
        EncryptedTextField,
    )


    class LoginPasswordTestCredentials(models.Model):
        login = EncryptedCharField(max_length=250, null=True, blank=True)
        password = EncryptedCharField(max_length=250, null=True, blank=True)


    class Totp2FATestCredentials(models.Model):
        totp_secret = EncryptedCharField(max_length=128)


    class TlsCertificateTestCredentials(models.Model):
        tls_certificate = EncryptedTextField()


    class CreditCardTestCredentials(models.Model):
        credit_card_number = EncryptedCharField(max_length=64)
        expiration_date = EncryptedCharField(max_length=16)
        name = EncryptedCharField(max_length=128)
        # cvv field REMOVED entirely for PCI DSS compliance.
    ```
