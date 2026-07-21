Missing SAML `InResponseTo` binding and replay protection is a notable authentication vulnerability that can expose web applications to account takeover. Here is a contextual exploration of its risks, impacts, and real-world compromises:

### Real-world cases:

* **CVE-2017-11427 / CVE-2017-11428**: python3-saml (and the broader OneLogin SAML lineage) shipped replay/unsolicited-response handling flaws where, depending on configuration, a captured or unsolicited SAML response could be accepted because the `InResponseTo` binding guard was effectively bypassed. These CVEs were the catalyst for the `wantResponseInResponseTo` / `rejectUnsolicitedResponsesWithInResponseTo` controls referenced in this entry.
* **OneLogin customer data breach (2017)**: an attacker obtained AWS keys and was able to access OneLogin's SAML IdP infrastructure, underscoring the sensitivity of SAML response capture and the value of binding assertions to outstanding requests and rejecting replays.

### Business impact:

The exploitation can lead to full account takeover within the assertion validity window for any user whose SAML response is captured via a MITM/browser-proxy/IdP-log position. Beyond the direct unauthorised access, exploitation can cause reputational damage, regulatory exposure (failure to enforce authentication controls), and loss of customer trust. Federated SSO is widely deployed in enterprise environments, so a replay gap can translate to broad tenant-level risk.

### Notes:

The replay vector requires a capture position and a legitimately signed response (signature, issuer and audience checks remain enforced); it is not a standalone authentication bypass. Forging an unsolicited response additionally requires control of the trusted per-org IdP signing key, which is a misconfiguration/compromised-key threat rather than a code bypass.
