The `addJavascriptInterface()` method on API level JELLY\_BEAN or below can be abused via reflection to execute commands remotely in the context of the running application

The addJavascriptInterface method exposes a supplied Java object from within a WebView to JavaScript. For applications compiled or linked against and API level less than 17; all public methods (including the inherited ones) can be accessed. Through the use of reflection it is also possible to invoke any other unregistered Java class.