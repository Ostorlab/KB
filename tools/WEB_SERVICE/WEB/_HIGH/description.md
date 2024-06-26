
# Access Control Bypass

An access control bypass vulnerability allows an attacker to circumvent the intended restrictions and gain unauthorized access to resources or functionality within a system or application.

### Examples

#### Dart

```dart
dart
import 'package:flutter/material.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  String currentUserRole = "user";

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(
          title: Text('Access Control Bypass Demo'),
        ),
        body: Center(
          child: ElevatedButton(
            onPressed: () {
              if (currentUserRole == "admin") {
                // Perform admin actions
                showDialog(
                  context: context,
                  builder: (context) {
                    return AlertDialog(
                      title: Text('Admin Panel'),
                      content: Text('You have admin access!'),
                    );
                  },
                );
              } else {
                // Perform user actions
                showDialog(
                  context: context,
                  builder: (context) {
                    return AlertDialog(
                      title: Text('User Panel'),
                      content: Text('You have user access!'),
                    );
                  },
                );
              }
            },
            child: Text('Click Me'),
          ),
        ),
      ),
    );
  }
}
```

#### Swift

```swift
swift
import Foundation

public struct User {
    private var username: String
    private var password: String
    
    public init(username: String, password: String) {
        self.username = username
        self.password = password
    }
    
    public func getUsername() -> String {
        return self.username
    }
    
    public func getPassword() -> String {
        return self.password
    }
}

func main() {
    print("Enter username:")
    let username = readLine() ?? ""
    
    print("Enter password:")
    let password = readLine() ?? ""
    
    let user = User(username: username, password: password)
    
    print("User: \(user.getUsername())")
    print("Password: \(user.getPassword())")
}

main()
```

#### Kotlin

```kotlin
kotlin
import java.util.Scanner

fun main() {
    val scanner = Scanner(System.`in`)
    println("Enter your role (admin/user):")
    val role = scanner.nextLine()

    if (role == "admin") {
        println("Welcome admin!")
    } else {
        println("Welcome user!")
    }
}
```
