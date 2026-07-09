* Avoid transmitting PII/PHI in URL query parameters; use the request body instead, since URLs are commonly logged by proxies, load balancers, and browser history.
* Always transmit PII/PHI over an encrypted channel (TLS), never in plain text.
* Minimize the amount of PII sent to the backend to what is strictly necessary for the request.
* Mask or redact PII before sending it to third-party analytics, crash-reporting, or logging SDKs.
* Do not echo PII back in error messages or debug responses.
* Some jurisdictions may require you to provide a privacy policy for transmitting personal information, and to obtain explicit user consent before sending it off-device.
* If a backend integration requires PII, ensure it is only sent to first-party, trusted endpoints, and validate third-party SDKs are not silently forwarding it elsewhere.

=== "Kotlin"
  ```kotlin
  import okhttp3.OkHttpClient
  import okhttp3.Request
  import okhttp3.RequestBody
  import okhttp3.MediaType.Companion.toMediaType

  val client = OkHttpClient()

  fun submitProfile(email: String, phoneNumber: String, ssn: String) {
      // PII sent only in the encrypted request body, not in the URL.
      val json = """{"email":"$email","phone":"$phoneNumber","ssn":"$ssn"}"""
      val body = RequestBody.create("application/json".toMediaType(), json)
      val request = Request.Builder()
          .url("https://api.example.com/profile")
          .post(body)
          .build()

      client.newCall(request).execute()
  }
  ```

=== "Swift"
  ```swift
  import Foundation

  func submitProfile(email: String, phoneNumber: String, ssn: String) {
      // PII sent only in the encrypted request body, not in the URL.
      var request = URLRequest(url: URL(string: "https://api.example.com/profile")!)
      request.httpMethod = "POST"
      request.httpBody = try? JSONSerialization.data(withJSONObject: [
          "email": email,
          "phone": phoneNumber,
          "ssn": ssn
      ])

      URLSession.shared.dataTask(with: request).resume()
  }
  ```

=== "Flutter"
  ```dart
  import 'package:http/http.dart' as http;
  import 'dart:convert';

  Future<void> submitProfile(String email, String phoneNumber, String ssn) async {
    // PII sent only in the encrypted request body, not in the URL.
    final uri = Uri.parse('https://api.example.com/profile');

    await http.post(
      uri,
      body: jsonEncode({'email': email, 'phone': phoneNumber, 'ssn': ssn}),
    );
  }
  ```
