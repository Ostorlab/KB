User input should be strictly validated before being incorporated into XPath queries. In most cases, it will be appropriate to accept input containing only short alphanumeric strings. At the very least, input containing any XPath metacharacters such as " ' / @ = * [ ] ( and ) should be rejected.

Subsequently, encoding user input using HTML entities can provide an additional layer of defense against potential attacks by rendering special characters inert. However, a superior approach, if available, is to utilize parameterized XPath queries. This method, akin to SQL's parameterized queries, involves inserting user input as a variable into the query. In doing so, any special characters are either handled to avoid query syntax modification or cause the query to fail, thereby enhancing security."


### Examples

#### Java

```java
String xmlInput = "<users>" +
        "<user><username>admin</username><password>admin@123</password></user>" +
        "<user><username>guest</username><password>guest@123</password></user>" +
        "</users>";

DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
DocumentBuilder builder = factory.newDocumentBuilder();
Document doc = builder.parse(new InputSource(new StringReader(xmlInput)));

//Input example :
String inputUsername = "admi'n";
String inputPassword = "admin@//'123";

// Sanitize inputs 
inputUsername = inputUsername.replaceAll("[^a-zA-Z0-9]", "");

XPathFactory xPathfactory = XPathFactory.newInstance();
XPath xpath = xPathfactory.newXPath();

// Using parameterized queries
String query = "//user[username/text()=? and password/text()=?]";
XPathExpression expr = xpath.compile(query);

expr.setXPathVariableResolver((varName) -> {
    if (varName.equals("username")) {
        return inputUsername;
    } else if (varName.equals("password")) {
        return inputPassword;
    }
    return null;
});

Object result = expr.evaluate(doc, XPathConstants.NODESET);
NodeList nodes = (NodeList) result;

System.out.println(nodes.getLength() > 0 ? "Authenticated" : "Authentication Failed");
```
#### Javascript

```javascript
const express = require('express');
const libxml = require('libxmljs');

const app = express();
const xmlInput = `<users>
  <user><username>admin</username><password>admin@123</password></user>
  <user><username>guest</username><password>guest@123</password></user>
</users>`;

app.post('/authenticate', (req, res) => {
  let { username, password } = req.body;

  const xmlDoc = libxml.parseXml(xmlInput);
  const query = `//user[username/text()=$username and password/text()=$password]`;
  const nodes = xmlDoc.find(query, { $username: username, $password: password });

  res.send(nodes.length > 0 ? 'Authenticated' : 'Authentication Failed');
});

app.listen(3000, () => {
  console.log('Server running on port 3000');
});
```

#### Php

```php
<?php
$xmlInput = "<users>" .
    "<user><username>admin</username><password>admin@123</password></user>" .
    "<user><username>guest</username><password>guest@123</password></user>" .
    "</users>";

$inputUsername = "admin";
$inputPassword = "admin@123";

// Sanitize inputs to avoid ' and " 
$inputUsername = htmlspecialchars($inputUsername, ENT_QUOTES, 'UTF-8');
$inputPassword = htmlspecialchars($inputPassword, ENT_QUOTES, 'UTF-8');

$doc = new DOMDocument();
$doc->loadXML($xmlInput);

$xpath = new DOMXPath($doc);

// Using parameterized queries
$query = "//user[username/text()='" . $inputUsername . "' and password/text()='" . $inputPassword . "']";
$nodes = $xpath->query($query);

echo ($nodes->length > 0) ? "Authenticated" : "Authentication Failed";
?>
```