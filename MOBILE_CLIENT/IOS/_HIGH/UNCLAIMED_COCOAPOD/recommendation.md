Developers who have released IOS applications should take the following steps to secure their code:
 * Pin the version of all Cocoapods packages, This prevents automatic updates to potentially harmful versions.
 * For internally developed Pods hosted on CocoaPods for distribution, developers should perform CRC (checksum) validation against the version downloaded from the CocoaPods trunk server to ensure it matches the internally developed version.
 * Review CocoaPods dependencies and verify you are not using an orphaned Pod.
 * Ensure you use third party dependencies that are actively maintained and whose ownership is clear.
 * Perform periodic security code scans to detect secrets and malicious code in all external libraries, especially CocoaPods.