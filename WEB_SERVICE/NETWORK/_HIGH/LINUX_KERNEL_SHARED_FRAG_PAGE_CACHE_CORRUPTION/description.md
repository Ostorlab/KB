The Linux kernel's socket-buffer coalescing path can lose the `SKBFL_SHARED_FRAG` marker when `skb_try_coalesce()` attaches paged fragments from one skb to another (CVE-2026-46300, CVSS 7.8 local, CWE-787/456). That marker is the invariant relied on by later in-place writers. ESP (IPsec) input processing checks `skb_has_shared_frag()` before deciding whether an uncloned non-linear skb can skip `skb_cow_data()` and decrypt in place. If TCP receive coalescing has moved shared, page-cache-backed fragments into an skb that no longer carries the marker, ESP sees `skb_has_shared_frag()` as false and **decrypts in place over page-cache-backed fragments** — an unintended, silent modification of page-cache data, i.e. of the contents of files as read from the page cache, without touching the underlying storage. The fix propagates `SKBFL_SHARED_FRAG` whenever coalescing transfers paged fragments. It repairs the invariants introduced by the earlier "avoid in-place decrypt on shared skb frags" (`f4c50a4034e6`) and checksum-generation (`cef401de7be8`) fixes, and was reported by William Bowling (Zellic), reviewed by Eric Dumazet.

CISA added CVE-2026-46300 to the Known Exploited Vulnerabilities catalog on October 28, 2026, recording that it is exploited in the wild. Observed chains combine it with the PHP RCEs CVE-2026-109618/CVE-2026-109619 (see the PHP2Shell entry): the PHP flaw first gains unauthenticated code execution as the web user, and this kernel bug then corrupts page-cache-backed file data to implant PHP webshells and run commands as **root**. The page-cache aspect matters for triage: content read through the page cache can differ from what the same file contains on disk, so file-integrity baselines that re-read through the cache may not see the implant, and a reboot can make the modification disappear.

### Affected and fixed versions

The stable fix has been backported to every maintained branch. Affected ranges and their fixes:

| Stable line | First fixed version |
| --- | --- |
| 5.15.y | 5.15.208 |
| 6.1.y | 6.1.174 |
| 6.6.y | 6.6.141 |
| 6.12.y | 6.12.91 |
| 6.18.y | 6.18.33 |
| 7.0.y | 7.0.10 |

A 5.10.y backport also exists (setting `SKBTX_SHARED_FRAG` in `tx_flags` for that tree). 7.1 release candidates before the fix are affected. Distribution kernels carry their own backport decisions and errata: Red Hat's record lists **RHEL 8 (4.18), RHEL 9 (5.14) and RHEL 10 (6.12)** — including the EUS/AUS/TUS streams — plus **OpenShift 4.12–4.21** and vendor-embedded products such as the **Siemens SIMATIC S7-1500 MFP** (per the NVD configurations), while **RHEL 6 and 7 are listed as not affected**. Check the distributor's advisory for the fixed kernel build.

### What conditions are required for exploitation?

Exploitation is not a generic remote compromise of any host with an affected kernel: it requires (a) a position that lets the attacker drive **ESP input processing** — i.e. the host terminates or processes attacker-influenced IPsec/ESP traffic (an IPsec endpoint, or a device exposing xfrm processing of untrusted tunnels), and (b) on the full PHP2Shell path, an unauthenticated foothold such as CVE-2026-109618/109619 to aim the corruption at page-cache-backed file content. In the observed chain the corrupted content is PHP file data on web servers, which is why the finding clusters with PHP workloads.

### Distinguishing a real finding from a benign lookalike

* Concrete evidence is a **kernel version/build below the fixed versions** on a host, combined with the exposure condition above (host terminates IPsec/ESP for traffic an attacker can influence). For host-level or image assessments, the version is the finding.
* An affected kernel version alone, on a host with **no ESP/IPsec processing of untrusted input**, is a lower-urgency patch-compliance finding — the corruption primitive needs the ESP path — but still patch, since the kernel configuration can change independently of the version.
* Page-cache implants from this bug are **not visible as on-disk file changes**: compare content read through the page cache against a read that bypasses it (or against the block device) when triaging a suspected implant, and expect artifacts to vanish after reboot or cache eviction.

  ```bash
    # Benign version fingerprint checks (no exploitation):
    uname -r
    cat /proc/version
    # 6.6.140 places the host below the fix on the 6.6 line; 6.6.141 or newer
    # is patched. Compare the reported version against the fixed-version table
    # above for the host's stable line.
  ```
