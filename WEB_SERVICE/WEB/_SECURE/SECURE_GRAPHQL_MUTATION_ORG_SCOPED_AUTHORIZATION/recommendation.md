The implementation is secure, no recommendation apply.

### Verification (Ongoing)

To maintain the current authorization posture as new mutations are added, regression-test that:

- Every new GraphQL mutation resolves the organization via the trusted principal helper (e.g. `get_organisation_from_context(info)`) and scopes its first database query by `organisation=organisation` before acting on any attacker-supplied identifier.
- Bulk operations use `.filter(id__in=..., organisation=organisation)` and never a raw `.filter(id__in=...).delete()/update()` that re-resolves by attacker-supplied ids alone.
- Import/upload paths force `organisation` from the trusted principal and never trust manifest-supplied tenant identifiers (`organisation_id`, `project_id`, foreign `scan_id`) embedded in the uploaded archive.
