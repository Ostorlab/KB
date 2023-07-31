Clear text HTTP traffic vulnerability refers to the risk associated with transmitting data over HTTP (Hypertext Transfer Protocol) without any encryption. This means that the information being sent and received is in clear text, making it easily readable and accessible to anyone who intercepts the data. This vulnerability can lead to serious security breaches as it exposes sensitive information like usernames, passwords, credit card numbers, and other personal data to potential hackers. It is particularly dangerous when using public Wi-Fi networks where data interception is more likely.

### Examples

#### Dart

```dart
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(
          title: Text('Vulnerable Flutter App'),
        ),
        body: MyHomePage(),
      ),
    );
  }
}

class MyHomePage extends StatefulWidget {
  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  final myController = TextEditingController();

  @override
  void dispose() {
    myController.dispose();
    super.dispose();
  }

  void sendHttpRequest(String url) async {
    var response = await http.get(url);
    print('Response status: ${response.statusCode}');
    print('Response body: ${response.body}');
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: EdgeInsets.all(10.0),
      child: Column(
        children: <Widget>[
          TextField(
            controller: myController,
            decoration: InputDecoration(
              border: OutlineInputBorder(),
              labelText: 'Enter URL',
            ),
          ),
          RaisedButton(
            onPressed: () {
              sendHttpRequest(myController.text);
            },
            child: Text('Send HTTP Request'),
          ),
        ],
      ),
    );
  }
}
```

#### Swift

```swift
import UIKit
import Foundation

class ViewController: UIViewController {
    
    @IBOutlet weak var urlField: UITextField!
    
    override func viewDidLoad() {
        super.viewDidLoad()
    }
    
    @IBAction func sendRequest(_ sender: Any) {
        guard let urlString = urlField.text, let url = URL(string: urlString) else {
            return
        }
        
        let task = URLSession.shared.dataTask(with: url) {(data, response, error) in
            guard let data = data else { return }
            print(String(data: data, encoding: .utf8)!)
        }
        
        task.resume()
    }
}
```

#### Kotlin

```kotlin
import java.net.URL
import java.util.Scanner

fun main(args: Array<String>) {
    println("Please enter the URL:")
    val userInput = Scanner(System.`in`).nextLine()
    val url = URL(userInput)
    val connection = url.openConnection()
    val content = connection.getInputStream().bufferedReader().use { it.readText() }
    println(content)
}
```
