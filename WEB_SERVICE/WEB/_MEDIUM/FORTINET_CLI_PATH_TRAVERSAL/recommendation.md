Upgrade each affected device to a fixed release for its branch, using Fortinet's upgrade-path tool to pick the route; for branches with no fixed build, migrate to a fixed release.

* **FortiOS**: 7.6.0–7.6.4 → 7.6.5+; 7.4.0–7.4.9 → 7.4.10+; **7.2, 7.0 and 6.4 have no fixed build — migrate to a fixed release** (staying current within those branches does not remediate this finding).
* **FortiPAM**: 1.7.0 → 1.7.1+; 1.8 is not affected; **1.0 through 1.6 have no fixed build — migrate**.
* **FortiProxy**: 7.6.0–7.6.4 → 7.6.5+; 7.4.0–7.4.11 → 7.4.12+; **7.2 and 7.0 — migrate**.
* **FortiSwitchManager**: 7.2.0–7.2.7 → 7.2.8+; 7.0.0–7.0.6 → 7.0.7+.
* **Siemens RUGGEDCOM APE1808** platforms running Fortinet NGFW below V7.4.10: update the Fortinet NGFW to V7.4.10 or later (Siemens ProductCERT can supply patch and update information).
* Follow the recommended upgrade path with Fortinet's upgrade tool rather than jumping directly across major versions.

Because the flaw is confirmed exploited in the wild and is exercised from privileged CLI sessions:

* Review administrator accounts and CLI session logs on affected devices for unexpected file writes or deletes, unfamiliar arguments on ordinary commands, and sessions from unusual sources.
* Treat confirmed unexplained privileged CLI activity as a privilege-escalation incident: rotate administrator credentials, and rebuild the device from a known-good image if tampering is confirmed.
* Apply CISA's KEV required action for this CVE (mitigate per vendor instructions, with BOD 26-04 prioritization and forensics-triage guidance), and restrict CLI and administrative access to dedicated management networks to shrink the window in which a compromised admin account can be turned into device-level file manipulation.
