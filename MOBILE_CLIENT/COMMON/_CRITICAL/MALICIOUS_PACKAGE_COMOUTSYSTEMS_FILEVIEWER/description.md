The package `com.outsystems.plugins.fileviewer` version `1.0.6` has been identified as malicious. This specific version, tracked under the identifier `MAL-2022-2047`, poses a severe security risk.

The presence of this package in an application, particularly in environments like Cordova where it might be included via `cordova_plugins.js`, implies that the build environment, developer workstation, or the resulting application itself could be compromised.

According to the advisory associated with `MAL-2022-2047` (source: `ghsa-malware`), any computer that has this package installed or running should be considered fully compromised. This suggests the package likely contains malware designed for remote access, data exfiltration, or other malicious activities.

The attack vector is the inclusion of a compromised third-party dependency into the software supply chain.