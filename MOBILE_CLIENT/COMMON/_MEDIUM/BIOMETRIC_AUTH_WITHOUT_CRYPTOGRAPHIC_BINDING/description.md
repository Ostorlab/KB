Biometric Authentication Without Cryptographic Binding occurs when an application implements biometric authentication (fingerprint, face recognition, etc.) without properly binding it to cryptographic keys or secure credentials. This vulnerability allows attackers to bypass biometric authentication by directly accessing the protected resources or by intercepting and replaying authentication tokens. The biometric check becomes merely a UI-layer verification that can be circumvented at the API or storage level, as the biometric data is not cryptographically linked to the secured data or session.

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