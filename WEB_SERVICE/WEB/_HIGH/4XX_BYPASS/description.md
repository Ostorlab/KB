
# 4Xx-Bypass

The 4xx-bypass vulnerability allows an attacker to bypass client-side restrictions and access unauthorized resources or perform actions on a web application. This can lead to unauthorized data access, privilege escalation, and other security risks.

### Examples

#### Dart

```dart
dart
import 'package:flutter/material.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  final TextEditingController _controller = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(
          title: Text('Vulnerable App'),
        ),
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget>[
              TextField(
                controller: _controller,
                decoration: InputDecoration(
                  hintText: 'Enter a number',
                ),
              ),
              RaisedButton(
                onPressed: () {
                  int number = int.tryParse(_controller.text);
                  if (number != null && number > 0) {
                    // Vulnerable code that depends on user input
                    fetchResource('https://example.com/api/resource/$number');
                  } else {
                    // Handle invalid input
                  }
                },
                child: Text('Fetch Resource'),
              ),
            ],
          ),
        ),
      ),
    );
  }

  void fetchResource(String url) {
    // Code to make HTTP request to the provided URL
  }
}
```

#### Swift

```swift
swift
import Foundation

func main() {
    print("Enter a number:")
    if let input = readLine(), let number = Int(input) {
        if number == 123 {
            print("Access granted!")
        } else {
            print("Access denied!")
        }
    } else {
        print("Invalid input!")
    }
}

main()
```

#### Kotlin

```kotlinraise ValueErro
kotlin
import java.util.*

fun main() {
    val scanner = Scanner(System.`in`)
    print("Enter a number: ")
    val number = scanner.nextInt()

    if (number == 200) {
        println("Success")
    } else {
        println("Error")
    }
}
```
