VMware ESX contains an insufficient logging vulnerability (CVE-2026-41709, CVSS 3.1 **2.7 Low** — AV:N/AC:L/PR:H/UI:N/S:U/C:N/I:L/A:N, CWE-778, reported to Broadcom by Ian Barton of CrowdStrike). A **malicious administrator** can exploit it to perform certain operations **without them being logged**. This is not a remotely exploitable pre-authentication flaw: it requires administrator-level access to the hypervisor. Its risk is **post-compromise anti-forensics** — an intruder who has already reached admin level (for example after a credential-theft or another hypervisor chain) gains operations that leave no audit trail, which is precisely the scenario that motivates its inclusion in CISA's Known Exploited Vulnerabilities catalog (added October 28, 2026, alongside the forensic-triage requirements that KEV entries in this wave carry).

### Affected builds and fixed versions

Per the VMSA-2026-0006.2 response matrix (no workarounds exist; patches are cumulative):

| Product / component | Version | Fixed version |
| --- | --- | --- |
| VMware Cloud Foundation / vSphere Foundation, ESX | 9.1.x.x | ESXi-9.1.0.0-25370933 |
| VMware Cloud Foundation / vSphere Foundation, ESX | 9.0.x.x | ESXi-9.0.2.0100-25595025 |
| VMware ESX | 8.0 | ESXi80U3j-25429389 |
| VMware Cloud Foundation, ESX | 5.x | 5.2.4 (async patching, KB88287) |
| VMware Telco Cloud Platform, ESX | 5.0.x / 5.1.x | KB449886 |

### Distinguishing a real finding from a benign lookalike

* The weakness itself is **not externally observable** — there is no response, banner or behavioral probe that distinguishes a vulnerable build from a fixed one. The only concrete finding is a **build fingerprint** of the ESX host (management interface welcome/host client, SOAP `about` information, or inventory data from an authenticated source) that places the build below the fixed versions above.
* An ESX build at or above the fixed version is not affected.
* **An ESXi management interface exposed to the internet is a separate finding** (attack surface / access control) — do not fold it into this one, and do not report this CVE merely because a hypervisor is exposed; exposure changes the priority of patching, not the presence of the logging flaw.
* Because the impact is "operations without logging", the practical consequence appears during incident response as **missing audit records**: an admin action corroborated by other evidence (VM state, task history from other sources, storage timestamps) with no corresponding log entry is the post-hoc indicator, not a remotely testable condition.

### Detection and forensic use

* For detection, fingerprint the ESX build and compare against the matrix; treat unpatched builds as an audit-trail integrity gap in hypervisor incident response plans.
* During triage of a compromised vSphere estate, prefer corroborating sources beyond the host's own logs (vCenter task/event records, storage and network telemetry), since the weakness's effect is precisely that some admin operations are absent from the host log.
