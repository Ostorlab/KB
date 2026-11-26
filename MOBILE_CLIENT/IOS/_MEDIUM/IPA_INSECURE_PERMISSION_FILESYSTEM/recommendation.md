* When setting permissions explicitly, use owner-only modes: `0o600` for files and `0o700` for directories.
* Keep sensitive files inside the app container, for example in `Library/Application Support`. Do not store them in
  an App Group shared container, or in the Documents directory when `UIFileSharingEnabled` is set.
* Protect sensitive files with Data Protection, using `NSFileProtectionComplete` where the app does not need the file
  while the device is locked.
* Store secrets such as tokens and keys in the Keychain, not in files.

```swift
import Foundation

func save(_ data: Data, named name: String) throws {
    let directory = try FileManager.default.url(
        for: .applicationSupportDirectory,
        in: .userDomainMask,
        appropriateFor: nil,
        create: true
    )
    let fileURL = directory.appendingPathComponent(name)
    try data.write(to: fileURL, options: [.completeFileProtection])
    try FileManager.default.setAttributes(
        [.posixPermissions: 0o600],
        ofItemAtPath: fileURL.path
    )
}
```
