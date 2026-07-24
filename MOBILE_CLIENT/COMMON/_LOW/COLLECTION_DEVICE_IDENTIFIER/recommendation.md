## Recommendation

For secure and privacy-respecting handling of persistent device identifiers, it is crucial to follow best practices that minimize tracking risks and comply with privacy regulations. Two general strategies are recommended:

* **Limit Collection and Prefer Safer Identifiers**: Only collect persistent device identifiers when strictly necessary for core application functionality. Avoid hardware-based identifiers like IMEI or serial numbers unless there is a compelling operational need. When collection is required, prefer safer alternatives such as platform-approved app-scoped identifiers (e.g., Android’s App Set ID, iOS’s IDFV) or ephemeral/custom-generated UUIDs stored securely for the duration of the app lifecycle.


* **Transparency and Consent**: Clearly document the purpose of collecting any persistent identifier. Disclose collection practices in the privacy policy and obtain user consent where legally required.

* **Secure Storage**: Store any persistent identifiers securely using platform-provided secure storage mechanisms (e.g., Android Keystore, iOS Keychain). Avoid storing identifiers in plain text or in locations accessible to other apps.

* **Avoid Cross-App Tracking**: Do not use persistent identifiers for advertising, analytics, or tracking across multiple apps unless explicitly allowed by platform policies and user consent.

By following these best practices, applications can reduce privacy risks, comply with regulatory requirements, and maintain user trust.
