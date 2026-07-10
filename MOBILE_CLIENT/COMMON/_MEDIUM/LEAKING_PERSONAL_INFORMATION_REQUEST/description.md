Personally Identifiable Information (PII) is, according to NIST Special Publication 800-122, a collective term for any information that can be used to distinguish or trace an individual's identity, such as name, social security number, date and place of birth, mother's maiden name, or biometric records; and any other information that is linked or linkable to an individual, such as medical, educational, financial, and employment information.

In the context of mobile security, PII leakage in network traffic occurs when plain text PII is transmitted in an HTTP(S) request or response body, headers, or URL/query parameters, making it accessible to anyone able to observe the traffic: intermediate proxies, logging infrastructure, analytics/crash-reporting SDKs, or an attacker positioned on the network.

=== "Kotlin"
  ```kotlin
  import okhttp3.OkHttpClient
  import okhttp3.Request
  import okhttp3.RequestBody
  import okhttp3.MediaType.Companion.toMediaType

  val client = OkHttpClient()

  fun submitProfile(email: String, phoneNumber: String, ssn: String) {
      // PII sent in plain text as URL query parameters and JSON body.
      val json = """{"email":"$email","phone":"$phoneNumber","ssn":"$ssn"}"""
      val body = RequestBody.create("application/json".toMediaType(), json)
      val request = Request.Builder()
          .url("https://api.example.com/profile?email=$email&ssn=$ssn")
          .post(body)
          .build()

      client.newCall(request).execute()
  }
  ```

=== "Swift"
  ```swift
  import Foundation

  func submitProfile(email: String, phoneNumber: String, ssn: String) {
      // PII sent in plain text as URL query parameters and JSON body.
      var components = URLComponents(string: "https://api.example.com/profile")!
      components.queryItems = [
          URLQueryItem(name: "email", value: email),
          URLQueryItem(name: "ssn", value: ssn)
      ]

      var request = URLRequest(url: components.url!)
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
    // PII sent in plain text as URL query parameters and JSON body.
    final uri = Uri.parse('https://api.example.com/profile?email=$email&ssn=$ssn');

    await http.post(
      uri,
      body: jsonEncode({'email': email, 'phone': phoneNumber, 'ssn': ssn}),
    );
  }
  ```
