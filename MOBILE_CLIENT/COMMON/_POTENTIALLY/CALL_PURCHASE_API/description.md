
# Call Payment Api

Maybe the way that you code a call for a purchase API is vulnerable to potential attacks due to insufficient output checking mechanisms. Attackers can exploit this vulnerability to gain unauthorized access to paid features, manipulate payment transactions, and cause financial losses to the organization.

### Examples

#### Dart

```dart

import 'package:flutter/material.dart';
import 'package:flutter_paystack/flutter_paystack.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await PaystackPlugin.initialize(
    publicKey: 'YOUR_PUBLIC_KEY', // Replace with your Paystack public key
  );
  runApp(MyApp());
}

class PaymentScreen extends StatefulWidget {
  @override
  _PaymentScreenState createState() => _PaymentScreenState();
}

class _PaymentScreenState extends State<PaymentScreen> {
  bool isLoading = false;

  void startPayment() async {
    setState(() {
      isLoading = true;
    });

    Charge charge = Charge()
      ..amount = 10000 // Amount in kobo (e.g., 10000 kobo = ₦100)
      ..email = 'user@example.com' // Customer's email address
      ..reference = 'REFERENCE_CODE'; // A unique reference code for the payment

      CheckoutResponse response = await PaystackPlugin.checkout(
        context,
        charge: charge,
      );

    setState(() {
      isLoading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Payment Screen'),
      ),
      body: Center(
        child: isLoading
            ? CircularProgressIndicator()
            : RaisedButton(
                child: Text('Make Payment'),
                onPressed: startPayment,
              ),
      ),
    );
  }
}

```

#### Swift

```swift

import Alamofire

func makePayment() {
    let apiUrl = "https://api.example.com/payment"
    
    // Prepare the request data
    let requestData: [String: Any] = [
        "amount": 100.00,
        "currency": "USD",
        "cardNumber": "4111111111111111",
        "expiryMonth": "12",
        "expiryYear": "2025",
        "cvv": "123"
        // additional parameters as required
    ]
    
    AF.request(apiUrl,
               method: .post,
               parameters: requestData,
               encoding: JSONEncoding.default)
        .validate()
        .responseJSON {}
}

```

#### Kotlin

```kotlin
import com.github.kittinunf.fuel.Fuel
import com.github.kittinunf.fuel.core.Method
import com.github.kittinunf.fuel.core.Parameters

fun makePayment() {
    val apiUrl = "https://api.example.com/payment"
    
    // Prepare the request data
    val requestData: Parameters = listOf(
        "amount" to 100.00,
        "currency" to "USD",
        "cardNumber" to "4111111111111111",
        "expiryMonth" to "12",
        "expiryYear" to "2025",
        "cvv" to "123"
        // additional parameters as required
    )
    
    Fuel.request(Method.POST, apiUrl)
        .header("Content-Type" to "application/json")
        .body(requestData.toJson())
        .responseString { _, response, result ->
            when (response.statusCode) {}
        }
}

```
