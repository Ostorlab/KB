**1. Restrict Keychain Item Accessibility:**

   Set appropriate conditions for accessing keychain items based on the device state and user preferences.

   - For sensitive data that should only be accessed when the device is unlocked, use `kSecAttrAccessibleWhenUnlocked`.
   - If access to the keychain item is required after the user unlocks the device for the first time, use `kSecAttrAccessibleAfterFirstUnlock`.
   - Avoid using `kSecAttrAccessibleAlways`, as it provides unrestricted access to the keychain item regardless of the device's locked state, which can compromise security.

=== "Swift"
   ```swift
   var query: [String: Any] = [kSecClass as String: kSecClassInternetPassword,
                               kSecAttrAccount as String: account,
                               kSecAttrServer as String: server,
                               kSecAttrAccessible as String: kSecAttrAccessibleWhenUnlocked,
                               kSecValueData as String: password]
   ```

**2. Demand User Presence:**

   Enhance security by requiring user presence, such as biometric authentication, before accessing sensitive data from the keychain.

   - Use `SecAccessControlCreateWithFlags` to create a `SecAccessControl` instance with appropriate authentication requirements.
   - Incorporate options such as `kSecAccessControlUserPresence` to ensure user interaction is required for accessing keychain items.

=== "Swift"
   ```swift
   let access = SecAccessControlCreateWithFlags(nil,
                                                kSecAttrAccessibleWhenUnlocked,
                                                kSecAccessControlUserPresence,
                                                &error);
   ```

**3. Require Application-Specific Passwords:**

   Implement application-specific passwords to further enhance security for individual keychain items.

   - Utilize `kSecAccessControlApplicationPassword` option when defining access control flags to prompt users for a specific password.
   - Ensure that the application-specific password is distinct from the device passcode, providing an additional layer of protection for sensitive data.

=== "Swift"
   ```swift
   let access = SecAccessControlCreateWithFlags(nil,
                                                kSecAttrAccessibleWhenPasscodeSet,
                                                kSecAccessControlBiometryAny | kSecAccessControlApplicationPassword,
                                                &error);
   ```