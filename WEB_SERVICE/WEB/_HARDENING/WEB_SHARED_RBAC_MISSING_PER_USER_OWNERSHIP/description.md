A resource protected by organisation-level (tenant-level) RBAC carries no
per-user ownership dimension: every update and delete resolver scopes records
only by `organisation=<caller org>` and a user-supplied identifier, with no
`created_by`/owner predicate. As a result any authenticated principal that
holds a write role inside an organisation can supply the identifier of a
record authored by another same-organisation principal and overwrite or
delete it.

This is a defense-in-depth observation rather than a confirmed exploitable
cross-tenant access-control flaw. The intended authorisation boundary — the
organisation/tenant boundary — is enforced consistently: every
object-resolution site pairs the user-supplied identifier with a
server-derived `organisation` predicate, so a foreign-organisation
identifier resolves to `DoesNotExist` or an empty queryset (cross-tenant
IDOR is protected). What is missing is a *per-user ownership* boundary on
resources that some deployments may expect to treat as per-principal secrets
(for example scan-time credentials, API keys, or tokens). When the
deployment model intends such resources to be org-wide shared assets, the
shared RBAC behaviour is by design and the residual is purely a
least-privilege / hardening gap.

### Implications

1. Intra-tenant horizontal write:
   - A write-role principal `U2` can `update`/`delete` a record authored by
     another same-organisation principal `U1` by supplying `U1`'s identifier.
   - The effect is confined to the caller's own organisation; no tenant or
     principal boundary is crossed.

2. Integrity and availability impact on same-org records:
   - A credential, token, or configuration record can be overwritten or
     removed by a peer who did not author it, affecting availability of the
     underlying scan/automation flow that depends on it.

3. Least-privilege / accountability gap:
   - Audit trails record the organisation-scoped mutation but cannot
     distinguish the legitimate author from a peer, weakening non-repudiation
     within the organisation.

### Code Example

=== "Python (Django / Strawberry-GraphQL)"
  ```python
  # Model: only an organisation FK, no created_by/owner field.
  class TestCredential(models.Model):
      credential_name = models.CharField(max_length=250, null=True, blank=True)
      organisation = models.ForeignKey(
          Organisation, related_name="test_credentials",
          on_delete=models.CASCADE)

  # Update / Delete resolvers scope by organisation + id only.
  @authorize(action=PermissionAction.WRITE)
  def update_test_credential(root, info, test_credential_id, **kwargs):
      organisation = get_organisation_from_context(info.context)
      # organisation is server-derived (good) but no ownership predicate.
      credential = TestCredential.objects.get(
          organisation=organisation, id=test_credential_id)
      ...  # mutation succeeds for any same-org id, including U1's record.

  @authorize(action=PermissionAction.WRITE)
  def delete_test_credential(root, info, test_credential_ids):
      organisation = get_organisation_from_context(info.context)
      TestCredential.objects.filter(
          organisation=organisation, id__in=test_credential_ids).delete()
  ```
  In this example the organisation predicate holds (a foreign-org id cannot
  resolve), so cross-tenant IDOR is protected. The residual is strictly
  intra-org: any WRITE principal can mutate a record authored by another
  same-org principal because no `created_by`/owner predicate is applied.
