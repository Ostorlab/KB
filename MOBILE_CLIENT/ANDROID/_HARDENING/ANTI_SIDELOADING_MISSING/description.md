The application ran normally after being installed from an unofficial source instead of the store it was published through, without detecting or responding to the sideloaded installation.

A sideloaded build is the typical delivery vector for a repackaged app: an attacker decompiles the original APK, injects malicious code or strips out security controls, re-signs it with their own key, and distributes it through third-party stores, file-sharing sites, or social engineering. Because the app never checks where it was installed from, the tampered copy runs with full functionality.

**Common attack scenarios:**

- **Repackaged malware distribution:** A trojanized clone of the app is published on a third-party store; users who sideload it expose their credentials and data to the attacker.
- **Ad/SDK swapping:** The original APK is rebuilt with the attacker's analytics or ad SDK to hijack revenue and exfiltrate user data.
- **Control stripping:** Root detection, certificate pinning, or license checks are removed from the repackaged build before redistribution.
- **Bypassing store-side protections:** Sideloading skips the publishing channel's malware scanning and integrity guarantees entirely.
