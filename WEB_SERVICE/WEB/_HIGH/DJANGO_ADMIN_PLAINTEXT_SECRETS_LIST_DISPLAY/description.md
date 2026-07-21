Sensitive credential and secret model fields are registered in Django admin `list_display` and/or `search_fields` while the corresponding `ModelAdmin` defines no `readonly_fields`, `exclude`, `formfield_overrides`, or `get_readonly_fields` for those secret fields. Because the admin changelist template unconditionally renders every `list_display` column as a table cell in the HTTP response (and includes them in any CSV/export action), any staff user holding the model `view` permission can bulk-read the secrets directly from the changelist. When `search_fields` includes a secret column, the `?q=` search bar additionally lets the user target-search those secrets across the whole table.

The exposure is compounded when no `ModelAdmin.get_queryset(self, request)` override scopes the changelist to the requesting user's tenant. Django admin then falls back to `Model._default_manager.all()`, returning every row across all organisations/tenants. The `organisation` (or equivalent) `ForeignKey` on the model is the tenant boundary, but unless the admin filters on it, it is display-only and never enforces isolation. The result is cross-tenant data exposure: a single staff account (typically gated only by `is_staff` plus a verified OTP/2FA session) can enumerate and export every tenant's secrets through the changelist and the search bar.

At rest, the secret fields are commonly stored as plaintext `CharField`, `IntegerField`, `TextField`, or `HStoreField` (e.g. card PAN + CVV, passwords, TOTP seeds, TLS private-key material, scan-bus passwords, arbitrary key/value headers). Storing full PAN and CVV in plaintext is a PCI-DSS Requirement 3.3/3.4 violation independent of the admin exposure. Encrypted-at-rest fields (e.g. AES-CCM `BinaryField` ciphertext + tag + nonce) are not directly readable as plaintext, but rendering their ciphertext material in the changelist is an unnecessary metadata disclosure whose severity rises when the decryption key is co-located on the same host as the ciphertext (a co-located environment variable, or a hardcoded known value in non-production environments).

=== "Python"
  ```python
  from django.contrib import admin

  from credentials import models


  # Vulnerable: secret fields rendered in the changelist and searchable across all tenants.
  @admin.register(models.LoginPasswordTestCredentials)
  class LoginPasswordTestCredentials(admin.ModelAdmin):
      # No readonly_fields, no exclude, no formfield_overrides, no get_queryset override.
      list_display = ["credential_name", "role", "login", "password", "url", "organisation"]


  @admin.register(models.CreditCardTestCredentials)
  class CreditCardTestCredentials(admin.ModelAdmin):
      # Full PAN and CVV rendered in the changelist and stored as plaintext CharField/IntegerField.
      list_display = [
          "credential_name",
          "credit_card_number",
          "expiration_date",
          "cvv",
          "name",
          "organisation",
      ]


  @admin.register(models.Totp2FATestCredentials)
  class Totp2FATestCredentials(admin.ModelAdmin):
      # TOTP seed rendered in the changelist enables account takeover of the scanned targets.
      list_display = ["credential_name", "totp_secret", "organisation"]


  @admin.register(models.AgentScanInstanceCredential)
  class AgentScanInstanceCredentialAdmin(admin.ModelAdmin):
      # Plaintext bus password is BOTH bulk-rendered in the changelist AND searchable via ?q=.
      search_fields = ("username", "password")
      list_display = ("username", "password")
  ```

=== "Python"
  ```python
  from django.contrib import admin

  from credentials import models
  from user_portal import models as up_models


  # Secure: secret fields removed from list_display/search_fields, masked read-only preview,
  # and the changelist scoped to the requesting user's organisations.
  @admin.register(models.LoginPasswordTestCredentials)
  class LoginPasswordTestCredentials(admin.ModelAdmin):
      list_display = ["credential_name", "role", "login", "masked_password", "url", "organisation"]
      search_fields = ["credential_name", "login", "role"]
      readonly_fields = ["password"]

      @admin.display(description="Password")
      def masked_password(self, obj):
          return f"****{(obj.password or "")[-4:]}" if obj.password else ""

      def get_queryset(self, request):
          qs = super().get_queryset(request)
          org_ids = up_models.OrganisationUserAccess.objects.filter(
              organisation_user__user=request.user
          ).values_list("organisation_id", flat=True)
          return qs.filter(organisation_id__in=org_ids)
  ```
