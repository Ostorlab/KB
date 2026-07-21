Remove secret/sensitive fields from `list_display` and `search_fields`, scope every `ModelAdmin.get_queryset(self, request)` to the requesting user's tenant, and apply field-level protection so secrets are never edited or rendered in plaintext. Layer the controls as follows:

1. **Remove secrets from `list_display` and `search_fields`.** Never place raw secrets (e.g. `password`, `credit_card_number`, `cvv`, `totp_secret`, `tls_certificate`, `script`, `private_ssh_key_*`, HStoreField `credentials`/`test_headers`, or any scan-bus `password`) in either attribute. The changelist renders every `list_display` column as a table cell in the HTTP response and includes them in CSV/export actions, and `search_fields` runs an unscoped `__icontains` over the default manager. Replace them with a non-sensitive placeholder column or a masked read-only method.

2. **Scope the changelist and search to the requesting user's tenant.** Override `get_queryset(self, request)` on every credential/agent `ModelAdmin` to filter rows by the requesting user's organisation linkage (e.g. via `OrganisationUser`/`OrganisationUserAccess`), enforcing tenant isolation. Without this override, Django admin uses `Model._default_manager.all()`, returning every row across all organisations to any staff viewer with the model `view` permission.

   ```python
   @admin.register(models.CreditCardTestCredentials)
   class CreditCardTestCredentials(admin.ModelAdmin):
       list_display = ["credential_name", "organisation"]  # no PAN/CVV

       def get_queryset(self, request):
           qs = super().get_queryset(request)
           org_ids = OrganisationUserAccess.objects.filter(
               organisation_user__user=request.user
           ).values_list("organisation_id", flat=True)
           return qs.filter(organisation_id__in=org_ids)
   ```

3. **Apply field-level protection for the change form.** Add `readonly_fields` for secret fields that must not be edited, `exclude` for fields that must not appear at all, or `get_readonly_fields(self, request, obj=None)` for conditional protection. Render a masked preview (e.g. `****1234`) instead of the raw value.

4. **Stop storing full PAN and CVV in plaintext.** Tokenize PANs and never persist CVV (PCI-DSS Requirement 3.3/3.4). Use encrypted field types (e.g. `django-cryptography`/`django-fernet`) for `password`, `totp_secret`, `tls_certificate`, `script`, and scan-bus passwords.

5. **Containment while remediating.** As a temporary measure, set `show_full_result_count = False` and disable any CSV/export action that includes secret columns until the fields are removed and the queryset is scoped.

6. **Protect encrypted-at-rest material too.** Do not expose `BinaryField` ciphertext, tag, and nonce columns in `list_display`; move the decryption key (e.g. `SSH_ENCRYPTION_KEY`) to a secrets manager or KMS-backed store rather than a co-located environment variable, and rotate it; remove any hardcoded dev/ci/test value.
