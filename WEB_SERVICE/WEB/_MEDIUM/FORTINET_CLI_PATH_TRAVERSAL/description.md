The command line interpreter of several Fortinet products contains a path-traversal vulnerability (CVE-2025-61624, CWE-22). An **authenticated attacker holding an admin profile with at least read-write permissions** can supply specifically crafted arguments to **existing CLI commands** and thereby **write or delete arbitrary files** on the appliance, which Fortinet classifies as an escalation of privilege on the device. Fortinet publishes the issue as FG-IR-26-122 (severity Medium, CVSSv3 6.0, `AV:L/AC:L/PR:H/UI:N/S:U/C:N/I:H/A:H`; NVD's primary score is 6.5 with a network attack vector), discovered internally, and marks it **Known Exploited: Yes** — CISA added it to the Known Exploited Vulnerabilities catalog on October 16, 2026.

Because the vulnerability is reachable only from a privileged CLI session, active exploitation typically indicates either a compromised administrator account or a foothold already on the device's management: when reviewing an affected device, the finding should trigger an account-and-session review, not only a patch check.

Siemens additionally lists **RUGGEDCOM APE1808** industrial application-hosting platforms running Fortinet NGFW below V7.4.10 as affected through this FortiOS flaw (SSA-975644, V1.1), so OT deployments need the same version review.

### Affected versions and fixes

| Product / branch | Affected | Fix |
| --- | --- | --- |
| FortiOS 7.6 | 7.6.0 – 7.6.4 | upgrade to 7.6.5 or above |
| FortiOS 7.4 | 7.4.0 – 7.4.9 | upgrade to 7.4.10 or above |
| FortiOS 7.2 | all versions | migrate to a fixed release |
| FortiOS 7.0 | all versions | migrate to a fixed release |
| FortiOS 6.4 | all versions | migrate to a fixed release |
| FortiPAM 1.8 | not affected | — |
| FortiPAM 1.7 | 1.7.0 | upgrade to 1.7.1 or above |
| FortiPAM 1.6 – 1.0 | all versions | migrate to a fixed release |
| FortiProxy 7.6 | 7.6.0 – 7.6.4 | upgrade to 7.6.5 or above |
| FortiProxy 7.4 | 7.4.0 – 7.4.11 | upgrade to 7.4.12 or above |
| FortiProxy 7.2 / 7.0 | all versions | migrate to a fixed release |
| FortiSwitchManager 7.2 | 7.2.0 – 7.2.7 | upgrade to 7.2.8 or above |
| FortiSwitchManager 7.0 | 7.0.0 – 7.0.6 | upgrade to 7.0.7 or above |
| Siemens RUGGEDCOM APE1808 (Fortinet NGFW) | below V7.4.10 | update Fortinet NGFW to V7.4.10 or later |

A FortiGuard **virtual patch** ("FG-VD-59270.0day.") is available in FMWP database update **25.120**, which can flag the attack pattern but does not fix the CLI weakness itself.

### Distinguishing a real finding from a benign lookalike

The reportable condition is a FortiOS / FortiPAM / FortiProxy / FortiSwitchManager (or RUGGEDCOM APE1808) device whose version falls inside the affected ranges above. The safe, sufficient verification is a version fingerprint of the device compared against the table; do **not** verify by sending crafted CLI arguments, which write or delete files on the target.

Two traps to check while triaging:

* **"Migrate" branches have no in-branch fix.** FortiOS 7.2, 7.0, 6.4 (and FortiPAM 1.0 – 1.6, FortiProxy 7.2/7.0) are vulnerable in *all* versions: moving to the newest release of those branches does not fix the finding — only migration to a fixed release does.
* **Version fingerprint provenance.** A version banner taken from a different device in the same HA cluster or management domain is not evidence about this device; fingerprint each appliance individually.

The following signals are **not** evidence of the vulnerability on their own: a Fortinet login page or product banner (fingerprint only), an admin CLI session being open (privileged CLI use is normal operation), or an up-to-date version on the device.

  ```bash
    # Benign verification (version fingerprint only — never send crafted CLI arguments):
    # 1) Fingerprint each device's version (management interface, API, or an
    #    authenticated 'get system status'-style read-only query).
    # 2) Compare against the fixed builds:
    #    FortiOS 7.6 >= 7.6.5 | FortiOS 7.4 >= 7.4.10 | FortiOS 7.2/7.0/6.4: no fixed build, migrate
    #    FortiPAM 1.7 >= 1.7.1 | FortiPAM 1.6-1.0: no fixed build, migrate | FortiPAM 1.8 unaffected
    #    FortiProxy 7.6 >= 7.6.5 | FortiProxy 7.4 >= 7.4.12 | FortiProxy 7.2/7.0: migrate
    #    FortiSwitchManager 7.2 >= 7.2.8 | FortiSwitchManager 7.0 >= 7.0.7
    # 3) For Siemens RUGGEDCOM APE1808: Fortinet NGFW >= V7.4.10 fixed.
  ```

### Detection of exploitation attempts

* Review administrator and CLI session logs on affected devices for unexpected file operations, unfamiliar argument strings on otherwise ordinary commands, or sessions from unusual sources — the flaw is exercised from privileged CLI sessions, so exploitation implies administrator-level access on the device.
* Fortinet's advisory marks the issue Known Exploited: Yes, and CISA's KEV entry requires mitigation per vendor instructions plus BOD 26-04 prioritization and forensics-triage guidance; treat confirmed unexplained privileged CLI activity on an affected build as a privilege-escalation incident, rotate administrator credentials, and rebuild the device from a known-good image if compromise is confirmed.
* The FortiGuard virtual patch FG-VD-59270.0day (FMWP database update 25.120) can flag the attack pattern, but does not fix the CLI weakness itself.
