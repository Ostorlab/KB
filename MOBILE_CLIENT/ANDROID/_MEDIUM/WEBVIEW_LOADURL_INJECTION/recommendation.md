All untrusted URLs must have proper input validation to ensure only
trusted content is accessible. For instance, if the application is
loading local assets, the list of loaded URLs must be whitelisted.

The `Webview` settings must also be hardened, removing all non required
settings, like javascript or file access.

=== "Java"
  ```java
 public class WhitelistBrowserActivity extends Activity {
    private static WHITELISTED_URLS = ImmutableList.of(
      "url1",
      "url2");

    @override
    public void onCreate(Bundle savedInstanceState) {
      super.onCreate(savedInstanceState);
      setContentView(R.layout.main);

      WebView webView = (WebView) findViewById(R.id.webview);

      String url = getIntent().getStringExtra("url");
      if (!WHITELISTED_URLS.contains(url)) {  /* Note: "https".startsWith("http") == true */
          url = "about:blank";
      }

      webView.loadUrl(url);
    }
 }
	```

=== "Dart (Flutter - flutter_inappwebview)"
	```dart
 import 'package:flutter_inappwebview/flutter_inappwebview.dart';
 import 'package:flutter/material.dart';

 class SafeWebViewWidget extends StatelessWidget {
   final String untrustedUrl;
   static const List<String> WHITELISTED_URLS = [
      "url1",
      "url2"
    ];

   SafeWebViewWidget({required this.untrustedUrl});

   @override
   Widget build(BuildContext context) {
     // Validate the incoming URL against the whitelist
     String safeUrl = "about:blank";
     if (WHITELISTED_URLS.contains(untrustedUrl)) {
       safeUrl = untrustedUrl;
     }

     return InAppWebView(
        initialUrlRequest: URLRequest(url: WebUri(safeUrl)),
        initialSettings: InAppWebViewSettings(
          // Harden settings by disabling features if not strictly required
          javaScriptEnabled: false, 
          allowFileAccess: false,
          allowFileAccessFromFileURLs: false,
          allowUniversalAccessFromFileURLs: false,
       ),
     );
   }
 }
	```
