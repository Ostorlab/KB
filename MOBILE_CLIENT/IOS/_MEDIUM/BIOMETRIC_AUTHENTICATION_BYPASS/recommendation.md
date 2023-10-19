### Swift

Use the Keychain to store the secretKey, and enforce the usage of the Biometric authentication to access the item from the Keychain.

1- Create a biometry-protected keychain item:

Use SecAccessControlCreateWithFlags to create a SecAccessControl with the following parameters:

- kSecAttrAccessibleWhenUnlockedThisDeviceOnly: keychain entry can only be read when the iOS device is unlocked. Also it won’t be copied to other devices via iCloud and won’t be added to backups.
- .biometryCurrentSet: sets the requirement of Touch ID or Face ID authentication. It strictly ties your entry to the currently enrolled biometric data.

```Swift
static func getBioSecAccessControl() -> SecAccessControl {
       var access: SecAccessControl?
       var error: Unmanaged<CFError>?
           access = SecAccessControlCreateWithFlags(nil,
               kSecAttrAccessibleWhenUnlockedThisDeviceOnly,
               .biometryCurrentSet,
               &error)
       precondition(access != nil, "SecAccessControlCreateWithFlags failed")
       return access!
   }


static func createBioProtectedEntry(key: String, data: Data) -> OSStatus {
       let query = [
           kSecClass as String: kSecClassGenericPassword as String,
           kSecAttrAccount as String: key,
           kSecAttrAccessControl as String: getBioSecAccessControl(),
           kSecValueData as String: data ] as CFDictionary
       return SecItemAdd(query as CFDictionary, nil)
   }
```

2- Read a biometry-protected entry:

```Swift
static func loadBioProtected(key: String, context: LAContext? = nil,
                                prompt: String? = nil) -> Data? {

    var query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrAccount as String: key,
            kSecReturnData as String: kCFBooleanTrue,
            kSecAttrAccessControl as String: getBioSecAccessControl(),
            kSecMatchLimit as String: kSecMatchLimitOne ]

    if let context = context {
        query[kSecUseAuthenticationContext as String] = context
        query[kSecUseAuthenticationUI as String] = kSecUseAuthenticationUISkip
    }

    if let prompt = prompt {
        query[kSecUseOperationPrompt as String] = prompt
    }

    var dataTypeRef: AnyObject? = nil
    let status = SecItemCopyMatching(query as CFDictionary, &dataTypeRef)

    if status == noErr {
        return (dataTypeRef! as! Data)
    } else {
        return nil
    }
}

static func redBioProtectedEntry(entryName: String) {
    let authContext = LAContext()
    let accessControl = SecAccessControlCreateWithFlags(nil,
                kSecAttrAccessibleWhenUnlockedThisDeviceOnly,
                .biometryCurrentSet,
                &error)
    authContext.evaluateAccessControl(accessControl, operation: .useItem, localizedReason: "Access sample keychain entry") {
        (success, error) in
        var result = ""
        if success, let data = loadBioProtected(key: entryName, context: authContext) {
            let result = String(decoding: data, as: UTF8.self)
        } else {
            result = "Can't read entry, error: \(error?.localizedDescription ?? "-")"
        }
    }
}
```

### Flutter

`biometric_storage` is a plugin that allows using biometric authentication to write and read encrypted data to the device.

The underhood implementation applies the best practices and uses a SecAccessControl with the right SecAccessControlCreateFlags to constraint access with Touch ID fo Face ID.

- The first step is to create the access object where we will write and read the data after the biometric authentication:

=== "Dart"
	```dart
	/// Retrieves the given biometric storage file. Each store is completely separated and has its own encryption and biometric lock.
  Future<BiometricStorageFile> _getStorageFile() async {
      final authStorage = await BiometricStorage().getStorage('authenticated_storage',options:StorageFileInitOptions(
        ///Always call it with `authenticationRequired=true`and`authenticationValidityDurationSeconds = -1` to ensure the secure implementation of bioùetric authentication. 
        authenticationValidityDurationSeconds: -1,
        authenticationRequired: true,
        androidBiometricOnly: true,
      ));
      return authStorage;
    }
	```

- Write data to the secure storage:

=== "Dart"
	```dart
	/// Retrieves the given biometric storage file. Each store is completely separated and has its own encryption and biometric lock.
  Future<void> createBioProtectedEntry(context) async {
    if (await _checkAuthenticate() == false) {
      showAlertDialog(context,const Text("Can't use biometric auth on this device."));
      return ;
    }
    _storageFile = await _getStorageFile();
    await _storageFile?.write(_my_secret_data);
  }
	```

- To read the data:

=== "Dart"
	```dart
	Future<void> redBioProtectedEntry(context) async {
    if (await _checkAuthenticate() == false) {
      showAlertDialog(context,const Text("Can't use biometric auth on this device."));
      return ;
    }
    if (_storageFile == null){
      showAlertDialog(context,const Text("Enable authentication first."));
      return ;
    }
    final data = await _storageFile?.read();
    showAlertDialog(context,Text(data!));
  }
	```