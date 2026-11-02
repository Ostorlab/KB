Apply the **second-round hotfix** for your track and reboot the server — this is the only complete fix. Because the first patch round (v9.15.2.59 and v10.3.4.0) did not fully address either flaw, upgrading *again* is required even if you already patched once this year.

* **v7, v8 and v9 tracks**: apply the AhsayCBS **9.15.2.70** hotfix (available to partners through Ahsay's partner portal), then reboot the server.
* **v10 track**: apply the AhsayCBS **10.3.4.45** hotfix (available to partners through Ahsay's partner portal), then reboot the server.
* **Verify the running build after reboot** by fingerprinting the console/API again. A server that reports a fixed build but was not rebooted after applying the hotfix may still be running vulnerable code in memory.

If the server was reachable from the internet while running an affected build, treat the appliance as potentially compromised rather than merely unpatched:

1. Follow CISA's KEV required action for these CVEs, which references the BOD 26-04 prioritization and forensics-triage guidance.
2. Review Replication Receiver configuration and server logs around `/rps/api/json/UpdateReceivers.do` for unexpected receiver entries or command execution.
3. Rotate every credential the backup server holds or stores: administrator accounts, system passwords, API credentials, and any customer encryption-key material.
4. Verify recent backup sets before trusting them, and restore the server from a known-good state if tampering or code execution is confirmed.

To reduce future exposure, keep the AhsayCBS console and API off the public internet — restrict them to a management network or VPN — since a backup server concentrates an organisation's customer data and encryption keys in a single internet-facing target that has now been exploited in the wild.
