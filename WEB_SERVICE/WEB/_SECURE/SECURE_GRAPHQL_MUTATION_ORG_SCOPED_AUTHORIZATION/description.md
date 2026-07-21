The GraphQL mutation surface is protected against cross-tenant Insecure Direct Object Reference (IDOR, CWE-639) by binding every attacker-supplied object identifier to the authenticated principal's organization before any state-changing sink is reached.

Each mutation resolver derives the organization/tenant exclusively from the trusted request context (e.g. `get_organisation_from_context(info)`) rather than from an attacker-controllable argument, and scopes its first data-access query by `organisation=organisation` before acting on a user-supplied `id`, `id__in` list, uploaded manifest, or referenced foreign key. A foreign-organization identifier is therefore excluded by the org-scoped queryset: an all-foreign selector yields an empty queryset and raises, a mixed selector only touches same-tenant rows, and a referenced `asset_id`/`agent_group_id`/`scan_id` belonging to another tenant raises `ObjectDoesNotExist`. The action-level authorization decorator is treated as a coarse permission gate only; object-level ownership is enforced by the inline `organisation=` predicate that precedes every destructive, export, import, or run sink, and no unscoped re-resolution path (raw `.filter(id__in=...).delete()/update()` or a signed-URL/report-download re-resolved by raw id) exists downstream.

### Secure Pattern

=== "Python"
  ```python
  class DeleteScansMutation(graphene.Mutation):
      scan_ids = graphene.List(graphene.Int, required=True)

      @authorization.authorize(action=PermissionAction.WRITE)
      def mutate(root, info, scan_ids: list[int]):
          # Organization derived from the trusted principal, never from user input.
          organisation, org_user, _ = authentication.get_organisation_from_context(info)

          # Object-level authorization: the attacker-supplied ids are scoped by
          # the server-derived organization BEFORE any sink is reached.
          scans = Scan.objects.filter(id__in=scan_ids, organisation=organisation)
          if len(scans) == 0:
              raise graphql.GraphQLError("No scan is found.")

          for scan in scans:  # iterates only the org-scoped queryset
              scan.archived = True
              scan.save()
  ```

### Vulnerable Pattern (refuted by this control)

=== "Python"
  ```python
  # Vulnerable: raw attacker ids reach the sink with no organization predicate.
  scans = Scan.objects.filter(id__in=scan_ids)  # missing organisation=organisation
  scans.delete()
  ```
