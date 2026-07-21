Treat this as a defense-in-depth improvement, applicable mainly to deployments
that intend the affected resources to be per-principal owned secrets. If the
resources are by design org-wide shared assets, the shared RBAC behaviour is
acceptable and no change is required; the cross-tenant boundary is already
enforced and must be preserved on every `objects.get`/`objects.filter`.

### Permanent fix (per-user ownership)

If the deployment model intends per-user ownership, add a `created_by`
foreign key to the model and add an ownership predicate to every update and
delete lookup, while preserving the `organisation=organisation` invariant on
every query.

```python
# models.py
class TestCredential(models.Model):
    credential_name = models.CharField(max_length=250, null=True, blank=True)
    organisation = models.ForeignKey(
        Organisation, related_name="test_credentials",
        on_delete=models.CASCADE)
    created_by = models.ForeignKey(
        OrganisationUser, null=True, on_delete=models.SET_NULL,
        related_name="created_test_credentials")
```

```python
# Update — keep organisation, add ownership predicate.
credential = TestCredential.objects.get(
    organisation=organisation, id=test_credential_id,
    created_by=org_user)

# Delete — keep organisation, add ownership predicate.
TestCredential.objects.filter(
    organisation=organisation, id__in=test_credential_ids,
    created_by=org_user)
```

Apply the same predicate consistently to every entrypoint that mutates the
resource (GraphQL mutations, copilot/agent tools, and any REST view). Ensure
administrators / org-owners can still manage all organisation records when
business logic requires it, for example by exempting the `admin` role from
the ownership predicate.

### Verification

After implementation, verify:

1. A write-role user `U2` issuing `update`/`delete` with another same-org
   user `U1`'s identifier is rejected (ownership mismatch).
2. A foreign-organisation identifier still returns `DoesNotExist` / deletes
   zero rows, confirming the cross-tenant boundary is preserved.
3. The existing negative-control tests (foreign-org identifier is not
   mutated; unauthorised callers are rejected) still pass.
4. A positive test asserting `U2` cannot delete `U1`'s record is added.
