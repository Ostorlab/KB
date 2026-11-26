The application sets permissive POSIX permissions on a file or directory, for example by calling `chmod` or by
passing `NSFilePosixPermissions` to `FileManager`. The permission bits allow users other than the owner to read the
file (`0o644`, `0o755`), or to write to it as well (`0o666`, `0o777`).

### Permission bits on iOS

On iOS, all third-party apps run as the same nonprivileged user, `mobile`. Permission bits therefore do not separate
one app from another. What keeps other apps out of a file is the App Sandbox: each app can only reach its own
container, whatever permission bits its files carry. Permissive bits on a file inside the app container do not, on
their own, give another app access to it.

The exposure of a file on iOS depends on where it is stored and on its Data Protection class, not on its permission
bits. Files stored in the following locations can be reached outside the app, whatever their permission bits:

* **App Group shared containers:** every app and extension in the App Group can read and write the container.
* **Documents directory shared with the user:** when `UIFileSharingEnabled` is set, the files can be read and changed
  from a connected computer, and from the Files app when `LSSupportsOpeningDocumentsInPlace` is also set.
* **Jailbroken devices:** the sandbox can be bypassed. Only files with the Complete Data Protection class stay
  encrypted while the device is locked.
