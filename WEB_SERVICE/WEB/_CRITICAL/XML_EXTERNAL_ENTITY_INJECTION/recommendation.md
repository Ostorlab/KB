Virtually all XXE vulnerabilities arise because the application's XML parsing library supports potentially dangerous XML features that the application does not need or intend to use. The easiest and most effective way to prevent XXE attacks is to disable those features.

Generally, it is sufficient to disable resolution of external entities and disable support for XInclude. This can usually be done via configuration options or by programmatically overriding default behavior. Consult the documentation for your XML parsing library or API for details about how to disable unnecessary capabilities.

### Examples

#### Java

```java
//Input example : 
String xmlInput = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n" +
    "<!DOCTYPE foo [<!ENTITY xxe SYSTEM \"file:///etc/passwd\">]>\n" +
    "<foo>&xxe;</foo>";

DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();

// Enable secure processing mode to mitigate common XML security vulnerabilities
factory.setFeature(XMLConstants.FEATURE_SECURE_PROCESSING, true);

// Disable external DTDs and stylesheets to prevent potential XXE attacks
factory.setAttribute(XMLConstants.ACCESS_EXTERNAL_DTD, "");
factory.setAttribute(XMLConstants.ACCESS_EXTERNAL_STYLESHEET, "");

DocumentBuilder builder = factory.newDocumentBuilder();
Document doc = builder.parse(new ByteArrayInputStream(xmlInput.getBytes()));
```
#### Javascript

```javascript
const app = require("express")();
const libxml = require("libxmljs");
app.post("/path", (req, res) => {
  Element = libxml.parseXml(req.body);
 // Processing the XML element
});
```

#### Php

```php
<?php
$loadEntities = libxml_disable_entity_loader(true);

$xmlInput = '<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
<foo>&xxe;</foo>';

$doc = new DOMDocument();
$doc->loadXML($xmlInput);

libxml_disable_entity_loader($loadEntities);

echo $doc->saveXML();
?>
```