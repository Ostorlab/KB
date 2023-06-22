
# Xpath Injection

XPath Injection is a type of injection attack targeting applications that use XPath to query XML data. It occurs when an attacker injects malicious input into an XPath query, which can lead to unauthorized access to sensitive data, modification of data, or even complete system compromise. This vulnerability can be exploited by attackers to bypass authentication mechanisms, execute arbitrary code, and gain access to sensitive information.

### Examples

#### Dart

```dart
void _fetch_data(String _searchQuery) {

  final content = XmlDocument.parse(xmlFileContent);
  final xml_node = XmlXPath.node(content);
  final xpath = xml_node.query('//book[author=$_searchQuery');

  showDialog(
    context: context,
    builder: (context) => AlertDialog(
      title: Text('Search Result'),
      content: Text(result),
    ),
  );
  }
```

#### Swift

```swift
import Foundation
import SWXMLHash

func main() {
    print("Enter search term:")
    let searchTerm = readLine()!
    let xml = SWXMLHash.parse(xmlString)
    let results = xml["books"]["book"].all(withAttribute: "title", matchingXPath: "//title[contains(text(), '\(searchTerm)')]")
    
    for result in results {
        print(result["title"].element!.text)
        print(result["author"].element!.text)
    }
}
```

#### Kotlin

```kotlin
import javax.xml.parsers.DocumentBuilderFactory
import org.xml.sax.InputSource
import java.io.StringReader

fun main() {
    val userInput = readLine() ?: ""
    val factory = DocumentBuilderFactory.newInstance()
    val builder = factory.newDocumentBuilder()
    val inputSource = InputSource(StringReader(xml))
    val document = builder.parse(inputSource)
    val name = document.getElementsByTagName("name").item(0).textContent
    println("Hello, $name!")
}
```
