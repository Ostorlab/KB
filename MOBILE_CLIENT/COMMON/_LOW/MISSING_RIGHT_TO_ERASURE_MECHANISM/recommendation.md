## Recommendation

Implement an end-to-end erasure pathway so that data subjects can exercise their right to erasure (GDPR Article 17 / CCPA Civil Code 1798.105) directly within the application.

### Immediate Mitigation

* Add a user-facing "Delete my account / Erase my data" affordance on the account or settings screen and surface it prominently for users in GDPR/CCPA jurisdictions while the permanent server-side implementation is being built.
* Publish a documented manual erasure process (for example a support email or web form) so data subjects can currently request erasure, and track those requests to completion.

### Permanent Fix

Implement an end-to-end erasure pathway covering the server, the client repository, the UI entry point, and a full local purge:

* **Server:** expose a `deleteAccount` / `eraseData` mutation (or REST endpoint) that, for an authenticated user, purges the account and all associated personal data server-side and returns a confirmation (for example a `deletedAt` timestamp).
* **Client:** add a repository method that invokes the server erasure operation and verifies the confirmation.
* **UI:** add a `DeleteAccount` entry to the account/settings menu and wire a confirmation handler that calls the server mutation, then runs a complete local purge.
* **Local purge:** after server confirmation, clear every local store, not only the partial set cleared by logout. This includes the default and encrypted SharedPreferences (remove all keys, including the OAuth token), the local GraphQL/SQLite cache (clearAll and delete the database file), on-device downloaded media, image caches (memory and disk), and any analytics SDK user data.

### Verification

* Re-run a case-insensitive search for account-deletion and data-erasure terms across the source and confirm the new erasure symbols now appear.
* Confirm the new server erasure operation appears in the API introspection schema and returns a confirmation when invoked by an authenticated user.
* End-to-end test: create a test account, populate personal data, call the erasure operation, then verify that server records are purged and that all local stores on the device are empty on next launch.
* Confirm a data subject can fully exercise GDPR Article 17 / CCPA Civil Code 1798.105 through the new flow with no residual account or personal data server-side.
