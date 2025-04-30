Biometric Authentication without Cryptographic Binding occurs when an application implements biometric authentication (fingerprint, face recognition, etc.) without properly binding it to cryptographic keys or secure credentials. This vulnerability allows attackers to bypass biometric authentication by directly accessing the protected resources or by intercepting and replaying authentication tokens. The biometric check becomes merely a UI-layer verification that can be circumvented at the API or storage level, as the biometric data is not cryptographically linked to the secured data or session.

### Examples

#### Dart

```dart
import 'package:flutter/material.dart';
import 'package:local_auth/local_auth.dart';
import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Biometric Auth Demo',
      theme: ThemeData(primarySwatch: Colors.blue),
      home: LoginScreen(),
    );
  }
}

class LoginScreen extends StatefulWidget {
  @override
  _LoginScreenState createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final LocalAuthentication auth = LocalAuthentication();
  bool _isAuthenticated = false;
  final String apiKey = "secret_api_key_12345";
  
  Future<void> _authenticate() async {
    bool authenticated = false;
    try {
      authenticated = await auth.authenticate(
        localizedReason: 'Authenticate to access the app',
        options: const AuthenticationOptions(
          stickyAuth: true,
          biometricOnly: true,
        ),
      );
    } catch (e) {
      print(e);
    }
    
    if (authenticated) {
      setState(() {
        _isAuthenticated = true;
      });
      
      // VULNERABLE: Storing sensitive data without cryptographic binding
      final prefs = await SharedPreferences.getInstance();
      prefs.setString('auth_status', 'authenticated');
      prefs.setString('api_key', apiKey);
    }
  }

  void _accessSecureData() async {
    final prefs = await SharedPreferences.getInstance();
    // VULNERABLE: Only checking local flag without cryptographic verification
    if (prefs.getString('auth_status') == 'authenticated') {
      final retrievedApiKey = prefs.getString('api_key');
      print('Accessed secure data: $retrievedApiKey');
    } else {
      print('Authentication required');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Biometric Auth Demo')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            if (!_isAuthenticated)
              ElevatedButton(
                onPressed: _authenticate,
                child: Text('Authenticate with Biometrics'),
              )
            else
              Column(
                children: [
                  Text('Authentication Successful!'),
                  SizedBox(height: 20),
                  ElevatedButton(
                    onPressed: _accessSecureData,
                    child: Text('Access Secure Data'),
                  ),
                ],
              ),
          ],
        ),
      ),
    );
  }
}
```


#### Kotlin

```kotlin
import android.hardware.biometrics.BiometricPrompt
import android.os.Build
import androidx.annotation.RequiresApi

@RequiresApi(Build.VERSION_CODES.P)
class BiometricAuthVulnerable {

    private var cryptoObject: BiometricPrompt.CryptoObject? = null

    init {
        // In a vulnerable implementation, the CryptoObject might be null or not properly bound
        cryptoObject = null
    }

    fun authenticate(biometricPrompt: BiometricPrompt, callback: BiometricPrompt.AuthenticationCallback) {
        val promptInfo = BiometricPrompt.PromptInfo.Builder()
            .setTitle("Biometric Authentication")
            .setSubtitle("Authenticate using your fingerprint")
            .setNegativeButtonText("Cancel")
            .build()

        // The cryptoObject is passed but is null or not properly initialized,
        // meaning the biometric data isn't cryptographically bound.
        biometricPrompt.authenticate(promptInfo, cryptoObject, callback)
        println("Authentication initiated without proper cryptographic binding.")
    }

    // In a real scenario, you would have a callback to handle success/failure
    class AuthenticationCallback : BiometricPrompt.AuthenticationCallback() {
        override fun onAuthenticationSucceeded(result: BiometricPrompt.AuthenticationResult) {
            super.onAuthenticationSucceeded(result)
            println("Authentication succeeded, but without cryptographic binding, the result is vulnerable.")
            // Access granted without proper security measures.
        }

        override fun onAuthenticationFailed() {
            super.onAuthenticationFailed()
            println("Authentication failed.")
        }

        override fun onAuthenticationError(errorCode: Int, errString: CharSequence) {
            super.onAuthenticationError(errorCode, errString)
            System.err.println("Authentication error: $errString")
        }
    }
}

fun main() {
    // This is a simplified example and would require an Activity context
    // and proper BiometricPrompt initialization in a real Android application.
    println("This is a demonstration of vulnerable biometric authentication.")
    println("In a real app, the CryptoObject would be missing or improperly used.")
}

```

#### Java

```java
import android.hardware.biometrics.BiometricPrompt;
import android.os.Build;
import androidx.annotation.RequiresApi;

import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;
import java.security.KeyStore;

@RequiresApi(api = Build.VERSION_CODES.P)
public class SecureBiometricAuthCrypto {

    private static final String KEY_NAME = "biometric_key";
    private KeyStore keyStore;

    public SecureBiometricAuthCrypto() {
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
            keyGenerator.init(null); // No specific parameters needed for AndroidKeyStore
            keyGenerator.generateKey();
        } catch (Exception e) {
            throw new RuntimeException("Failed to generate key", e);
        }
    }

    private BiometricPrompt.CryptoObject getCryptoObject() {
        try {
            SecretKey key = (SecretKey) keyStore.getKey(KEY_NAME, null);
            Cipher cipher = Cipher.getInstance("AES/CBC/PKCS7Padding");
            cipher.init(Cipher.ENCRYPT_MODE, key);
            return new BiometricPrompt.CryptoObject(cipher);
        } catch (Exception e) {
            throw new RuntimeException("Failed to get CryptoObject", e);
        }
    }

    public void authenticate(BiometricPrompt biometricPrompt, BiometricPrompt.AuthenticationCallback callback) {
        BiometricPrompt.PromptInfo promptInfo = new BiometricPrompt.PromptInfo.Builder()
                .setTitle("Biometric Authentication")
                .setSubtitle("Authenticate using your fingerprint")
                .setNegativeButtonText("Cancel")
                .build();

        // Properly obtain and pass the CryptoObject to bind the biometric data
        BiometricPrompt.CryptoObject cryptoObject = getCryptoObject();
        if (cryptoObject != null) {
            biometricPrompt.authenticate(promptInfo, cryptoObject, callback);
            System.out.println("Authentication initiated with cryptographic binding.");
        } else {
            System.err.println("Failed to obtain CryptoObject. Authentication cannot be securely performed.");
        }
    }

    public static class AuthenticationCallback extends BiometricPrompt.AuthenticationCallback {
        @Override
        public void onAuthenticationSucceeded(BiometricPrompt.AuthenticationResult result) {
            super.onAuthenticationSucceeded(result);
            if (result.getCryptoObject() != null) {
                // The getCryptoObject() will return the CryptoObject used during authentication.
                // You can now use the Cipher object within it to perform cryptographic operations
                // on the data that the user intended to protect with their biometric.
                System.out.println("Authentication succeeded with cryptographic binding. Cipher: " + result.getCryptoObject().getCipher().getAlgorithm());
                // Proceed with secure operations using the cipher.
            } else {
                System.err.println("Authentication succeeded, but CryptoObject is null. This should not happen in a secure implementation.");
                // Handle this error appropriately.
            }
        }

        @Override
        public void onAuthenticationFailed() {
            super.onAuthenticationFailed();
            System.out.println("Authentication failed.");
        }

        @Override
        public void onAuthenticationError(int errorCode, CharSequence errString) {
            super.onAuthenticationError(errorCode, errString);
            System.err.println("Authentication error: " + errString);
        }
    }

    public static void main(String[] args) {
        // This is a simplified example and would require an Activity context
        // and proper BiometricPrompt initialization in a real Android application.
        System.out.println("This demonstrates secure biometric authentication using CryptoObject.");
    }
}
```