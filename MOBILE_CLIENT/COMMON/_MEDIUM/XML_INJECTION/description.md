# XML Injection

XML Injection is a type of attack where an attacker injects malicious XML code into an application, which can then be executed by the application. This can lead to a variety of attacks, including denial of service, data theft, and remote code execution.

## External Entity Injection

External Entity Injection is a type of XML Injection where an attacker injects an external entity into an XML document. This can be used to read sensitive data, perform denial of service attacks, or execute remote code.

### Examples


#### Swift

```{language}
import Foundation

func main() {
    print("Enter XML data:")
    if let xmlData = readLine() {
        let data = xmlData.data(using: .utf8)
        let document = try! XMLDocument(data: data!, options: [])

        let root = document.rootElement()
        let content = root?.stringValue

        print("Data: \(content ?? "")")
    }
}
```

#### Kotlin

```{language}
import javax.xml.parsers.DocumentBuilderFactory

fun main() {
    println("Enter XML data:")
    val xmlData = readLine() // User input

    val factory = DocumentBuilderFactory.newInstance()
    val builder = factory.newDocumentBuilder()

    val document = builder.parse(xmlData)
    val root = document.documentElement
    val data = root.textContent

    println("Data: $data")
}
```

## XPath Injection

XPath Injection is a type of XML Injection where an attacker injects malicious XPath code into an application. This can be used to read sensitive data, modify data, or execute remote code.

### Examples

#### Dart

```{language}
import 'package:flutter/material.dart';
import 'package:xml/xml.dart' as xml;

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  final String xmlData = '''
    <library>
      <book>
        <title>{title}</title>
        <author>John Doe</author>
        <price>19.99</price>
      </book>
    </library>
  ''';

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'XPath Injection',
      home: Scaffold(
        appBar: AppBar(
          title: Text('XPath Injection'),
        ),
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget>[
              TextField(
                onChanged: (value) {
                  searchBooks(value);
                },
                decoration: InputDecoration(
                  hintText: 'Enter a search term',
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  void searchBooks(String title) {
    final document = xml.parse(xmlData.replaceAll('{title}', title));

    final expressionString = "//book[contains(title, '$title')]";
    final nodes = document.findAll(expressionString);

    for (final node in nodes) {
      final titleNode = node.findElements('title').single;
      final authorNode = node.findElements('author').single;
      final priceNode = node.findElements('price').single;

      print('Book Title: ${titleNode.text}');
      print('Author: ${authorNode.text}');
      print('Price: ${priceNode.text}');
      print('------------------');
    }
  }
}
```

#### Swift

```{language}
import Foundation

func searchBooks(title: String) {
    let xmlData = """
        <library>
            <book>
                <title>\(title)</title>
                <author>John Doe</author>
                <price>19.99</price>
            </book>
        </library>
        """.data(using: .utf8)!

    let document = try! XMLDocument(data: xmlData, options: [])

    let expressionString = "//book[contains(title, '\(title)')]"
    let nodes = try! document.nodes(forXPath: expressionString)

    for node in nodes {
        if let titleNode = node["title"] as? XMLNode,
           let authorNode = node["author"] as? XMLNode,
           let priceNode = node["price"] as? XMLNode {
            print("Book Title: \(titleNode.stringValue)")
            print("Author: \(authorNode.stringValue)")
            print("Price: \(priceNode.stringValue)")
            print("------------------")
        }
    }
}

print("Enter a search term:")
if let searchTerm = readLine() {
    searchBooks(title: searchTerm)
}
```

#### Kotlin

```{language}
import javax.xml.parsers.DocumentBuilderFactory
import javax.xml.xpath.XPathConstants
import javax.xml.xpath.XPathFactory

fun main() {
    println("Enter a search term:")
    val searchTerm = readLine() // User input

    val factory = DocumentBuilderFactory.newInstance()
    val builder = factory.newDocumentBuilder()
    val document = builder.parse("data.xml")

    val xpathFactory = XPathFactory.newInstance()
    val xpath = xpathFactory.newXPath()

    val expression = "//book[contains(title, '$searchTerm')]"
    val nodeList = xpath.evaluate(expression, document, XPathConstants.NODESET)

    for (i in 0 until nodeList.length) {
        val node = nodeList.item(i)
        println("Book Title: ${xpath.evaluate("title", node)}")
        println("Author: ${xpath.evaluate("author", node)}")
        println("Price: ${xpath.evaluate("price", node)}")
        println("------------------")
    }
}
```

