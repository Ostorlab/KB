# Missing Right to Erasure and Account Deletion Mechanism

The application collects and stores user accounts or personal data (including, in many cases, protected health information) but does not implement any user-reachable account deletion or data erasure mechanism. There is no client- or server-side operation (GraphQL mutation, REST endpoint, or other API call) that deletes the user's account or erases their personal data, and the user interface exposes no "Delete my account" or "Erase my data" affordance. The only user-initiated account action is typically a local "Logout", which clears some local session state but performs no server-side account or data deletion and often leaves local stores (encrypted preferences, on-device media, image caches) populated.

As a result, a data subject has no in-app mechanism to exercise their right to erasure. The server-side account and personal data are retained indefinitely, and significant personal data may remain on the device after the user believes they have "left" the application.

## Impact

This is a compliance and design gap rather than a directly exploitable security vulnerability. An attacker cannot use the absence to gain unauthorized access, but data subjects in GDPR and CCPA jurisdictions cannot delete their account or personal data, which is retained server-side indefinitely and may persist on the device.

## Regulatory and Standards Context

* **GDPR Article 17 (Right to erasure / "right to be forgotten")** is not satisfied: there is no deletion path for the account or the personal data.
* **CCPA / CPRA Civil Code 1798.105 (Right to delete)** is not satisfied.
* **CWE-459 (Incomplete Cleanup)** applies: there is no end-to-end purge path. Logout only partially clears local stores and nothing deletes server-side data.
* **OWASP Top 10 A04:2021 (Insecure Design)** applies: the absence of a documented, user-reachable data-erasure control is a design-level privacy control gap.

## Verification

A finding of this rule is supported when an exhaustive search of the application for account-deletion and data-erasure terms (for example `deleteAccount`, `eraseData`, `rightToErasure`, `forgetMe`, `purgeAccount`, `closeAccount`, `removeAccount`, `accountDeletion`, `deleteMyData`, `dataErasure`) across the source (e.g. Kotlin, Swift, Dart, GraphQL and REST definitions) returns no matches that target a user account or personal-data record, the backend API surface exposes no erasure operation, and the settings/account screen exposes only a Logout affordance. Occurrences of `delete` limited to local temporary-file cleanup (for example `File.delete()`) or routine boolean model fields are not account or personal-data deletion sinks and do not satisfy the right to erasure.
