Cisco Secure Email Gateway (ESA), physical and virtual, contains an unauthenticated arbitrary-file-write vulnerability in its Advanced Malware Protection (AMP) feature (CVE-2026-76519, CWE-23 relative path traversal; CVSS 3.1 9.8, AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H, CNA Cisco PSIRT). A remote, unauthenticated attacker exploits it by **sending an email that contains a crafted attachment** through an affected device; the AMP file reputation component handles the attachment improperly and writes attacker-controlled files to the underlying operating system, which can lead to command execution with **root** privileges. CISA added the CVE to the Known Exploited Vulnerabilities catalog on October 14, 2026 — the same day the advisory was published — and Cisco states it became aware of active exploitation in October 2026. The vulnerability was found through internal security scanning.

Both of the following conditions must hold for a device to be exploitable:

* the **File Reputation service** (part of AMP) is enabled and assigned to a mail policy, and
* the **Content Scanner Tools** version is earlier than 25.3.0.5525.

Cisco confirmed that Secure Email and Web Manager and Secure Web Appliance are **not** affected, and that only the ESA is in scope — a mail-flow appliance is the exposure, not the management plane.

### Affected versions

Any Cisco Secure Email Gateway release is affected while the two conditions above hold, because the vulnerable code ships inside the AMP Content Scanner Tools package rather than a single AsyncOS train. The AsyncOS-level first fixed releases are 15.5.5-014 (15.5 line) and 16.5.0-780 (16.5 line); releases on the 16.0 train have no fixed AsyncOS build and must migrate to a fixed release. Cisco's CSAF lists these known-affected AsyncOS builds: 13.0.0-392, 13.0.5-007, 13.5.1-277, 13.5.4-038, 14.0.0-698, 14.2.0-620, 14.2.1-020, 14.3.0-032, 15.0.0-104, 15.0.1-030, 15.0.3-002, 15.0.5-016, 15.5.0-048, 15.5.1-055, 15.5.2-018, 15.5.3-022, 15.5.4-012, 16.0.0-050, 16.0.0-054, 16.0.1-017, 16.0.2-112, 16.0.3-044, 16.0.4-016.

### Distinguishing a real finding from a benign lookalike

Concrete evidence is the conjunction of the two required conditions on a device, not either one alone:

* **File Reputation enabled** — in the web UI under Mail Policies > Incoming/Outgoing Mail Policies > Advanced Malware Protection, the "Enable File Reputation" box is checked for a policy. File reputation enabled but not assigned to any policy does not expose the device.
* **Content Scanner Tools below 25.3.0.5525** — from the CLI, `contentscannerstatus` prints the running version; any version earlier than 25.3.0.5525 is vulnerable when File Reputation is also enabled.

The following signals are **not** evidence on their own:

* An ESA product fingerprint (management login page, SMTP banner) — that is product identification only.
* A device running an older AsyncOS release with File Reputation **disabled** or unassigned — the exploit path requires the service to be enabled on a mail policy; such a device is not exploitable through this CVE, though it still should be upgraded.
* Malware detections in quarantine or outbreak logs — normal AMP functioning, not evidence of this vulnerability.
* High email volume — the exploit is a single crafted message, not a volumetric event.

=== "Text"
  ```
    # Benign device-side checks (no crafted email is ever sent):
    cisco-esa> contentscannerstatus
    Component              Version                Last Updated
    Content Scanner Tools  25.2.0.5427.15.5.001   Never updated
    # A version below 25.3.0.5525 is the second required condition.

    # Check for compromise indicators recorded by the device:
    esa-appliance> grep "System Security" system_logs
    # 'Suspected compromise indicator was found.' -> treat as compromised.
    # 'No compromise indicator was found.' -> no compromise detected.
    # 'Security scan did not complete.' -> contact TAC.
    # For clusters, run this on every member.
  ```

An exploitation attempt must never be verified by sending a crafted attachment: a successful write can produce root command execution on the appliance. A network-side check that a targeted device actually received a suspicious message may use the mail logs, but confirmation of vulnerability is the two benign conditions above.

### Detection of exploitation attempts

* Run `grep "System Security" system_logs` on every cluster member; the three possible messages and their meanings are in the benign-check block above. On Cisco Secure Email Cloud, Cisco has contacted affected customers directly and admins without CLI access cannot check independently.
* Assume evidence removal: successful exploitation grants root, which lets the attacker remove or hide indicators. Cross-check network and firewall logs **outside** the device for unexpected uploads initiated from the appliance to external IPs, or downloads from known-malicious IPs.
* In a cluster, a compromised member exposes the SSH keys used for inter-member authentication, which can be used to move to the other members — treat one compromised member as putting the whole cluster at risk.
