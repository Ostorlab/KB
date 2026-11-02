Palo Alto Networks PAN-OS software contains a remote code execution vulnerability (CVE-2026-0322, CWE-94 — improper control of generation of code) in the **management interface**. An attacker who already has valid administrator credentials and network access to the management interface can execute arbitrary code **with root privileges** on the device. Palo Alto Networks scores it 8.6 HIGH on the CVSS 4.0 base scale (network attack vector, low attack complexity, high privileges required, high impact on confidentiality, integrity and availability) and marks it urgency **HIGHEST** "when you allow access to the management interface from external IP addresses on the internet"; NVD's CVSS 3.1 score is 7.2. CISA added it to the Known Exploited Vulnerabilities catalog on October 14, 2026, and Palo Alto Networks states that **very limited exploitation has been observed targeting the management interface**.

Scope, from the vendor advisory:

* Applicable to PAN-OS on **PA-Series and VM-Series firewalls and on Panorama (virtual and M-Series)**.
* **Cloud NGFW and Prisma Access are not impacted.**
* **No special configuration is required** to be affected — the required configuration for exposure is simply the management interface being reachable by the attacker, with valid credentials.
* There are **no known workarounds**; restricting management access reduces the risk but does not fix the flaw.

### Affected versions and fixes

| Branch | Affected (examples) | Fixed by |
| --- | --- | --- |
| PAN-OS 12.2 | 12.2.0 – 12.2.3 | 12.2.4 or later |
| PAN-OS 12.1 | 12.1.0 – 12.1.4-h11, 12.1.5 – 12.1.7-h7, 12.1.8 – 12.1.10-h1 | 12.1.4-h12, 12.1.7-h8 or 12.1.10-h2 or later |
| PAN-OS 11.2 | 11.2.0 – 11.2.4-h21, 11.2.5 – 11.2.7-h20, 11.2.8 – 11.2.10-h14, 11.2.11 – 11.2.13-h2, 11.2.14 – 11.2.15 | 11.2.4-h22, 11.2.7-h21, 11.2.10-h15, 11.2.13-h3 or 11.2.16 or later |
| PAN-OS 11.1 | 11.1.0 – 11.1.4-h36, 11.1.5 – 11.1.6-h38, 11.1.7 – 11.1.7-h10, 11.1.8 – 11.1.10-h34, 11.1.11 – 11.1.13-h14, 11.1.14 – 11.1.16-h2 | 11.1.4-h37, 11.1.6-h39, 11.1.7-h11, 11.1.10-h35, 11.1.13-h15 or 11.1.16-h3 or later |
| PAN-OS 10.2 | 10.2.0 – 10.2.7-h37, 10.2.8 – 10.2.10-h40, 10.2.11 – 10.2.13-h25, 10.2.14 – 10.2.16-h10, 10.2.17 – 10.2.18-h11 | 10.2.7-h38, 10.2.10-h41, 10.2.13-h26, 10.2.16-h11 or 10.2.18-h12 or later |
| Older unsupported PAN-OS | all | upgrade to a supported fixed version |

The full per-branch solution table is in the vendor advisory; within each affected maintenance line, only the hotfix listed (or a later one) closes the flaw, and a build from any other line is outside that line's protection boundary.

### Distinguishing a real finding from a benign lookalike

This is an **authenticated** weakness: exploitation requires valid administrator credentials *and* reachability of the management interface. The reportable conditions, therefore, are:

* a PAN-OS (or Panorama) build below the fixed builds for its branch **combined with** an externally reachable management interface — this is the highest-urgency instance, and the one the vendor marks HIGHEST; or
* the same unpatched build in any environment where administrative credentials may be compromised, with the finding's severity reflecting the reduced reachability of the interface.

The following signals are **not** evidence of the vulnerability on their own:

* A PAN-OS or Panorama login page visible from the internet — that is a management-exposure finding on its own (worth reporting separately as hardening), but without the version boundary or credential compromise it is not this CVE.
* A version fingerprint at or above the fixed builds — not vulnerable to this CVE regardless of exposure; report at most as a hygiene/patch-currency note.
* Scan traffic or exploit attempts against the **data-plane** (GlobalProtect, SSL VPN, or user-traffic ports) — this vulnerability is in the management interface, not the data plane; those attempts do not establish exposure to CVE-2026-0322.

The safe verification is a version fingerprint of the management interface compared against the fixed-build table above. Do not attempt to exercise the code-injection path: that requires administrator credentials and executes code as root on a production security device.

  ```bash
    # Benign verification (version fingerprint only — no payloads, no credential use):
    # 1) Fingerprint the PAN-OS build of the management interface (the build is
    #    reported by the interface itself on its login surface and resources).
    # 2) Compare against the fixed builds for the branch, e.g.:
    #    12.2 -> >= 12.2.4 | 12.1 -> >= 12.1.4-h12 / 12.1.7-h8 / 12.1.10-h2
    #    11.2 -> >= 11.2.4-h22 / 11.2.7-h21 / 11.2.10-h15 / 11.2.13-h3 / 11.2.16
    #    11.1 -> >= 11.1.4-h37 / 11.1.6-h39 / 11.1.7-h11 / 11.1.10-h35 /
    #            11.1.13-h15 / 11.1.16-h3
    #    10.2 -> >= 10.2.7-h38 / 10.2.10-h41 / 10.2.13-h26 / 10.2.16-h11 / 10.2.18-h12
    # 3) Record whether the management interface is reachable from outside the
    #    management network — exposure multiplies the urgency of an unpatched build.
  ```

### Detection of exploitation attempts

* The vendor advisory associates three IP addresses with threat activity and limited exploit attempts against this vulnerability: `66[.]42[.]72[.]14`, `208[.]83[.]239[.]114`, `149[.]248[.]47[.]234`. Alert on management-interface traffic from these addresses.
* Threat Prevention subscriptions provide **limited** (not complete) coverage through Threat IDs **510046 and 510047** (Applications and Threats content 9159-10287 and later). For the signatures to protect management traffic, the MGT port's traffic must be routed through a DP port, the inbound-traffic management certificate must be replaced, traffic to the management interface must be decrypted so the firewall can inspect it, and Threat Prevention must be enabled on that inbound traffic.
* Investigate unexplained administrative sessions and configuration changes on appliances below the fixed builds, since exploitation runs with root privileges on the device.
