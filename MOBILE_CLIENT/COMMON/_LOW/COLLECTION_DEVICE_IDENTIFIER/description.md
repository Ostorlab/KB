# Collection of Device Identifiers

A **device identifier** is any value—hardware-based, platform-provided, or application-generated—that remains stable over time and can be used to uniquely identify a device or user across sessions. These identifiers enable device recognition and long-term correlation of activity, but also introduce significant privacy considerations.

There are typically three families:

## Hardware-Based Identifiers

Hardware identifiers come from the device’s physical components or firmware and usually remain constant for the lifetime of the device.

* **IMEI / MEID**: Unique modem identifiers historically used to identify mobile devices. Access is highly restricted on modern operating systems.
* **Serial Number**: A unique hardware identifier assigned by the manufacturer. Generally not accessible to normal applications.

## Platform-Provided Identifiers

Operating systems expose identifiers with limited scope or permissions.

* **Android ID**: A stable, app-scoped identifier that persists across reinstalls for the same app and signing key on modern Android versions.
* **IDFV (Identifier for Vendor)**: An iOS identifier shared across apps belonging to the same vendor, reset only if all of the vendor’s apps are uninstalled.
* **IDFA (Advertising Identifier)**: A user-resettable identifier used for advertising and analytics, available only with user consent under modern privacy frameworks.

## Application-Generated Identifiers

Applications may generate their own identifiers and store them persistently.

* **Custom UUIDs**: Random identifiers stored in local storage or secure system keychains, potentially surviving app reinstalls.
* **Derived or hashed identifiers**: Values created by combining device attributes.

These identifiers function as device identifiers if they can be used to correlate user activity over time.

## Privacy & Regulatory Considerations

Under major privacy regulations such as **GDPR**, **CCPA**, and similar frameworks, persistent device identifiers are classified as **personal data** because they allow the identification or tracking of a user or device. Improper handling may violate:

* **Data minimization**
* **Purpose limitation**
* **Transparency requirements**
* **Consent obligations**

Platform policies (e.g., Apple App Store, Google Play) further restrict the use of persistent identifiers for analytics, advertising, or cross-app tracking without explicit user authorization.

## Security & Compliance Implications

Persistent identifiers can be misused for:

* Device fingerprinting  
* Cross-app or cross-service tracking  
* Behavioral profiling  

Because of this, they require careful handling and justification for collection.
