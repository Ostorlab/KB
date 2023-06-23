
# Server Side Template Injection

Server Side Template Injection (SSTI) is a vulnerability that allows an attacker to inject malicious code into a server-side template, which can then be executed by the server. This can lead to a range of attacks, including data theft, privilege escalation, and remote code execution. SSTI attacks are particularly dangerous because they can be difficult to detect and can affect multiple pages or applications on a server.

### Examples

#### Dart

```dart
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'SSTI Demo',
      home: HomePage(),
    );
  }
}

class HomePage extends StatefulWidget {
  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  String _name = '';

  Future<void> _fetchData() async {
    final response = await http.get('https://example.com/api?name=$_name');
    setState(() {
      _name = response.body;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('SSTI Demo'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            TextField(
              onChanged: (value) {
                setState(() {
                  _name = value;
                });
              },
              decoration: InputDecoration(
                hintText: 'Enter your name',
              ),
            ),
            SizedBox(height: 20),
            RaisedButton(
              onPressed: _fetchData,
              child: Text('Submit'),
            ),
            SizedBox(height: 20),
            Text(
              'Hello, $_name!',
              style: TextStyle(fontSize: 24),
            ),
          ],
        ),
      ),
    );
  }
}
```

#### Swift

```swift
import Foundation
import Kitura
import KituraStencil

let router = Router()

router.setDefault(templateEngine: StencilTemplateEngine())

router.get("/") { request, response, next in
    let context: [String: Any] = [:]
    try response.render("index", context: context).end()
}

router.post("/search") { request, response, next in
    let query = request.body?.asURLEncoded
    let context: [String: Any] = ["query": query?["q"] ?? ""]
    try response.render("search", context: context).end()
}

Kitura.addHTTPServer(onPort: 8080, with: router)
Kitura.run()
```

#### Kotlin

```kotlin
import java.util.*
import kotlin.collections.HashMap

fun main() {
    val scanner = Scanner(System.`in`)
    print("Enter your name: ")
    val name = scanner.nextLine()
    val template = "Hello, {{name}}!"
    val context = HashMap<String, String>()
    context["name"] = name
    val result = render(template, context)
    println(result)
}

fun render(template: String, context: Map<String, String>): String {
    var result = template
    for ((key, value) in context) {
        result = result.replace("{{${key}}}", value)
    }
    return result
}
```
