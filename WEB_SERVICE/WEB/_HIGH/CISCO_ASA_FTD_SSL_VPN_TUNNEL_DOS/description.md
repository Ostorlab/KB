The Remote Access SSL VPN service of Cisco Secure Firewall Adaptive Security Appliance (ASA) Software and Cisco Secure Firewall Threat Defense (FTD) Software contains an unchecked return value to NULL pointer dereference vulnerability (CVE-2026-76418, CWE-690, CVSS 8.6 `CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:N/I:N/A:H`) that could allow an **unauthenticated, remote attacker to cause the device to reload unexpectedly, resulting in a denial of service (DoS) condition**.

The vulnerability is due to logic errors when secondary authentication is configured on a tunnel group. An attacker exploits it by sending a crafted request when connecting to the SSL remote access VPN; a successful exploit reloads the affected device. No credentials and no successful VPN login are required to reach the affected processing path. Cisco's PSIRT became aware of active exploitation of this vulnerability in October 2026.

### Conditions required

A device is vulnerable when **all** of the following hold:

1. It runs a vulnerable release of Cisco Secure Firewall ASA Software or Cisco Secure FTD Software (see the fixed-release tables below).
2. The SSL remote access VPN login service is reachable — the running configuration contains the `webvpn` keyword with SSL VPN enabled on at least one interface (`webvpn` / `enable <interface_name>`).
3. Secondary authentication is configured on a tunnel group in that scope — `secondary-authentication-server-group` on any tunnel group, **including the default tunnel group `DefaultWEBVPNGroup`**. This check is not limited to profiles shown in the login page's group list, and it applies even when `tunnel-group-list enable` is absent or removed: if the default group uses secondary authentication, the exposure remains.

Cloud-delivered Firewall (CDFW), Cloud-delivered Firewall Management Center (cdFMC), Secure Access (CSA) and Secure FMC Software are confirmed not vulnerable.

### Fixed releases

First fixed release per track (upgrade to the fixed release for your train):

| Cisco Secure Firewall ASA Software | First fixed release |
| --- | --- |
| 9.16 and earlier | 9.16.4.104 |
| 9.18 | 9.18.4.96 |
| 9.20 | 9.20.4.50 |
| 9.22 | 9.22.3.200 |
| 9.23 | 9.23.1.48 |
| 9.24 | 9.24.1.27 or 9.24.10.1 |

| Cisco Secure FTD Software | First fixed release |
| --- | --- |
| 7.0 and earlier | 7.0.11 |
| 7.2 | 7.2.13 |
| 7.4 | 7.4.9 |
| 7.6 | 7.6.7 |
| 7.7 | 7.7.14 |
| 10.0 | 10.0.3 |
| 10.1 | 10.1.1 |

There are no workarounds; the only mitigation is removing secondary authentication (see the recommendation file).

=== "Cisco ASA/FTD CLI"
  ```text
    ! Identify the vulnerable configuration (device CLI):
    ! 1) SSL remote access VPN enabled:
    show running-config webvpn
    !   webvpn
    !    enable outside        <-- SSL VPN service reachable

    ! 2) Secondary authentication on any tunnel group, including the default:
    show running-config tunnel-group DefaultWEBVPNGroup
    !   tunnel-group DefaultWEBVPNGroup webvpn-attributes
    !    secondary-authentication-server-group LDAP-SERVER   <-- exposed

    ! 3) Software version:
    show version
  ```

### Validating a finding

* **Do not send the crafted request.** The "proof" of this vulnerability is that the device reloads — an active check against a production firewall is a denial-of-service test, not a scan. A finding must therefore be based on the observable conditions: a reachable SSL remote access VPN login service (for example the `/+CSCOE+/logon.html` login page), a software release in a vulnerable train, and — from the device side — the `webvpn` and `secondary-authentication-server-group` configuration described above.
* The secondary authentication precondition is a device configuration and is **not observable from outside**, so an external finding can at most establish "vulnerable release + SSL VPN service reachable"; confirm the tunnel group configuration on the device before remediating. Report the finding as confirmed only when all three conditions are established; otherwise report it as potentially exposed.
* Benign lookalikes: a Cisco ASA/FTD login page served by a **management interface** without remote access VPN enabled, or an instance already running a first-fixed release (or later), is not vulnerable. Cisco Secure FMC, CDFW and cdFMC are not affected.
