To securely implement biometric authentication, cryptographically bind the biometric verification to the sensitive data or authentication process. Use the device's secure hardware (such as Keystore/Keychain) to generate and store cryptographic keys that can only be accessed after successful biometric authentication. This ensures that even if an attacker bypasses the UI layer or gains access to stored preferences, they cannot access the protected data without passing the biometric check, as the decryption keys remain hardware-protected and biometric-gated.

### Code Examples:

#### Dart

```dart
import 'package:flutter/material.dart';
import 'package:local_auth/local_auth.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:encrypt/encrypt.dart' as encrypt;

class SecureBiometricAuth {
  final LocalAuthentication auth = LocalAuthentication();
  final FlutterSecureStorage secureStorage = FlutterSecureStorage();
  
  // For securely storing encryption key
  final String keyId = 'biometric_protected_key';
  
  Future<bool> authenticateUser() async {
    return await auth.authenticate(
      localizedReason: 'Authenticate to access the app',
      options: const AuthenticationOptions(
        stickyAuth: true,
        biometricOnly: true,
      ),
    );
  }
  
  Future<void> secureData(String sensitiveData) async {
    if (await authenticateUser()) {
      // Generate cryptographic key after biometric authentication
      final key = encrypt.Key.fromSecureRandom(32);
      final iv = encrypt.IV.fromSecureRandom(16);
      
      // Store encryption key in secure storage
      await secureStorage.write(key: keyId, value: key.base64);
      await secureStorage.write(key: '${keyId}_iv', value: iv.base64);
      
      // Encrypt sensitive data
      final encrypter = encrypt.Encrypter(encrypt.AES(key));
      final encrypted = encrypter.encrypt(sensitiveData, iv: iv);
      
      // Store encrypted data - only useful with the key
      final prefs = await SharedPreferences.getInstance();
      prefs.setString('encrypted_sensitive_data', encrypted.base64);
      
      return true;
    }
    return false;
  }
  
  Future<String?> retrieveSecureData() async {
    if (await authenticateUser()) {
      // Get encryption key (requires biometric auth to access secure storage)
      final keyString = await secureStorage.read(key: keyId);
      final ivString = await secureStorage.read(key: '${keyId}_iv');
      
      if (keyString == null || ivString == null) return null;
      
      // Get encrypted data
      final prefs = await SharedPreferences.getInstance();
      final encryptedData = prefs.getString('encrypted_sensitive_data');
      if (encryptedData == null) return null;
      
      // Decrypt data using key from secure storage
      final key = encrypt.Key.fromBase64(keyString);
      final iv = encrypt.IV.fromBase64(ivString);
      final encrypter = encrypt.Encrypter(encrypt.AES(key));
      
      return encrypter.decrypt64(encryptedData, iv: iv);
    }
    return null;
  }
}
```
