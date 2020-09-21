Disable debug logs before deploying your app to the public.

```java
FacebookSdk.setIsDebugEnabled(false);
```

Method signature:
```java
public static void setIsDebugEnabled(boolean enabled)
```
Documentation:

Used to enable or disable logging, and other debug features. Defaults to BuildConfig.DEBUG.

Parameters:
enabled - Debug features (like logging) are enabled if true, disabled if false.