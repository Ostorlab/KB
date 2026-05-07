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




#### Kotlin

```kotlin
// Recommended Kotlin code for Recommendation (Secure Data Access with CryptoObject)
import android.hardware.biometrics.BiometricPrompt
import android.os.Build
import androidx.annotation.RequiresApi
import java.nio.charset.StandardCharsets
import java.security.KeyStore
import javax.crypto.Cipher
import javax.crypto.KeyGenerator
import javax.crypto.NoSuchPaddingException
import javax.crypto.SecretKey
import javax.crypto.spec.IvParameterSpec
import java.security.InvalidAlgorithmParameterException
import java.security.InvalidKeyException
import java.security.NoSuchAlgorithmException
import java.util.Base64

@RequiresApi(Build.VERSION_CODES.P)
class SecureBiometricDataAccess {

    private val KEY_NAME = "biometric_data_key"
    private val TRANSFORMATION = "AES/CBC/PKCS7Padding"
    private val keyStore: KeyStore

    init {
        try {
            keyStore = KeyStore.getInstance("AndroidKeyStore")
            keyStore.load(null)
            if (!keyStore.containsAlias(KEY_NAME)) {
                generateKey()
            }
        } catch (e: Exception) {
            throw RuntimeException("Failed to initialize Keystore", e)
        }
    }

    private fun generateKey() {
        try {
            val keyGenerator = KeyGenerator.getInstance("AES", "AndroidKeyStore")
            keyGenerator.init(null)
            keyGenerator.generateKey()
        } catch (e: Exception) {
            throw RuntimeException("Failed to generate key", e)
        }
    }

    private fun getCryptoObject(): BiometricPrompt.CryptoObject? {
        return try {
            val key = keyStore.getKey(KEY_NAME, null) as SecretKey
            val cipher = Cipher.getInstance(TRANSFORMATION)
            cipher.init(Cipher.DECRYPT_MODE, key, IvParameterSpec(ByteArray(cipher.blockSize)))
            BiometricPrompt.CryptoObject(cipher)
        } catch (e: NoSuchAlgorithmException | NoSuchPaddingException | InvalidKeyException | InvalidAlgorithmParameterException) {
            RuntimeException("Failed to get CryptoObject for decryption", e)
            null
        }
    }

    // Simulate encrypted data storage
    private val encryptedData = "some_encrypted_data" // In a real app, this would be fetched

    fun authenticateAndDecrypt(biometricPrompt: BiometricPrompt, callback: BiometricPrompt.AuthenticationCallback) {
        val promptInfo = BiometricPrompt.PromptInfo.Builder()
            .setTitle("Biometric Authentication for Data Access")
            .setSubtitle("Authenticate to decrypt sensitive data")
            .setNegativeButtonText("Cancel")
            .build()

        val cryptoObject = getCryptoObject()
        if (cryptoObject != null) {
            biometricPrompt.authenticate(promptInfo, cryptoObject, callback)
            println("Authentication initiated for data decryption.")
        } else {
            System.err.println("Failed to obtain CryptoObject for decryption.")
        }
    }

    class AuthenticationCallback : BiometricPrompt.AuthenticationCallback() {
        override fun onAuthenticationSucceeded(result: BiometricPrompt.AuthenticationResult) {
            super.onAuthenticationSucceeded(result)
            val cryptoObject = result.cryptoObject
            if (cryptoObject != null) {
                val cipher = cryptoObject.cipher
                try {
                    // Simulate fetching encrypted data
                    val encryptedBytes = Base64.getDecoder().decode("YWFhYWFhYWFhYWFhYWFhYQ==") // Replace with actual encrypted data
                    val decryptedBytes = cipher?.doFinal(encryptedBytes)
                    val decryptedData = decryptedBytes?.toString(StandardCharsets.UTF_8)
                    println("Biometric authentication successful. Decrypted data: $decryptedData")
                    // Now you can securely use the decrypted data.
                } catch (e: Exception) {
                    System.err.println("Error during decryption: ${e.message}")
                }
            } else {
                System.err.println("Authentication succeeded, but CryptoObject is null.")
            }
        }

        override fun onAuthenticationFailed() {
            super.onAuthenticationFailed()
            println("Biometric authentication failed.")
        }

        override fun onAuthenticationError(errorCode: Int, errString: CharSequence) {
            super.onAuthenticationError(errorCode, errString)
            System.err.println("Authentication error: $errString")
        }
    }
}

fun main() {
    // Requires an Android environment for BiometricPrompt
    println("This demonstrates secure data access after biometric authentication.")
}
```

#### Java

```java
// Recommended Java code for Recommendation (Secure Data Access with CryptoObject)
import android.hardware.biometrics.BiometricPrompt;
import android.os.Build;
import androidx.annotation.RequiresApi;

import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.NoSuchPaddingException;
import javax.crypto.SecretKey;
import javax.crypto.spec.IvParameterSpec;
import java.nio.charset.StandardCharsets;
import java.security.InvalidAlgorithmParameterException;
import java.security.InvalidKeyException;
import java.security.KeyStore;
import java.security.NoSuchAlgorithmException;
import java.util.Base64;

@RequiresApi(api = Build.VERSION_CODES.P)
public class SecureBiometricDataAccess {

    private static final String KEY_NAME = "biometric_data_key";
    private static final String TRANSFORMATION = "AES/CBC/PKCS7Padding";
    private KeyStore keyStore;

    public SecureBiometricDataAccess() {
        try {
            keyStore = KeyStore.getInstance("AndroidKeyStore");
            keyStore.load(null);
            if (!keyStore.containsAlias(KEY_NAME)) {
                generateKey();
            }
        } catch (Exception e) {
            throw new RuntimeException("Failed to initialize Keystore", e);
        }
    }

    private void generateKey() {
        try {
            KeyGenerator keyGenerator = KeyGenerator.getInstance("AES", "AndroidKeyStore");
            keyGenerator.init(null);
            keyGenerator.generateKey();
        } catch (Exception e) {
            throw new RuntimeException("Failed to generate key", e);
        }
    }

    private BiometricPrompt.CryptoObject getCryptoObject() {
        try {
            SecretKey key = (SecretKey) keyStore.getKey(KEY_NAME, null);
            Cipher cipher = Cipher.getInstance(TRANSFORMATION);
            cipher.init(Cipher.DECRYPT_MODE, key, new IvParameterSpec(new byte[cipher.getBlockSize()]));
            return new BiometricPrompt.CryptoObject(cipher);
        } catch (NoSuchAlgorithmException | NoSuchPaddingException | InvalidKeyException | InvalidAlgorithmParameterException e) {
            throw new RuntimeException("Failed to get CryptoObject for decryption", e);
        }
    }

    // Simulate encrypted data storage
    private String encryptedData = "some_encrypted_data"; // In a real app, this would be fetched

    public void authenticateAndDecrypt(BiometricPrompt biometricPrompt, BiometricPrompt.AuthenticationCallback callback) {
        BiometricPrompt.PromptInfo promptInfo = new BiometricPrompt.PromptInfo.Builder()
                .setTitle("Biometric Authentication for Data Access")
                .setSubtitle("Authenticate to decrypt sensitive data")
                .setNegativeButtonText("Cancel")
                .build();

        BiometricPrompt.CryptoObject cryptoObject = getCryptoObject();
        if (cryptoObject != null) {
            biometricPrompt.authenticate(promptInfo, cryptoObject, callback);
            System.out.println("Authentication initiated for data decryption.");
        } else {
            System.err.println("Failed to obtain CryptoObject for decryption.");
        }
    }

    public static class AuthenticationCallback extends BiometricPrompt.AuthenticationCallback {
        @Override
        public void onAuthenticationSucceeded(BiometricPrompt.AuthenticationResult result) {
            super.onAuthenticationSucceeded(result);
            if (result.getCryptoObject() != null) {
                Cipher cipher = result.getCryptoObject().getCipher();
                try {
                    // Simulate fetching encrypted data
                    byte[] encryptedBytes = Base64.getDecoder().decode("YWFhYWFhYWFhYWFhYWFhYQ=="); // Replace with actual encrypted data
                    byte[] decryptedBytes = cipher.doFinal(encryptedBytes);
                    String decryptedData = new String(decryptedBytes, StandardCharsets.UTF_8);
                    System.out.println("Biometric authentication successful. Decrypted data: " + decryptedData);
                    // Now you can securely use the decrypted data.
                } catch (Exception e) {
                    System.err.println("Error during decryption: " + e.getMessage());
                }
            } else {
                System.err.println("Authentication succeeded, but CryptoObject is null.");
            }
        }

        @Override
        public void onAuthenticationFailed() {
            super.onAuthenticationFailed();
            System.out.println("Biometric authentication failed.");
        }

        @Override
        public void onAuthenticationError(int errorCode, CharSequence errString) {
            super.onAuthenticationError(errorCode, errString);
            System.err.println("Authentication error: " + errString);
        }
    }

    public static void main(String[] args) {
        // Requires an Android environment for BiometricPrompt
        System.out.println("This demonstrates secure data access after biometric authentication.");
    }
}
```