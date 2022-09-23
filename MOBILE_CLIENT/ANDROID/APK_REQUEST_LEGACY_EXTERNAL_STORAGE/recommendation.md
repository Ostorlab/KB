Avoid setting the attribute `android:requestLegacyExternalStorage` and use only scoped storage to guarantee a better protection to app and user data on external storage.

```xml
<application android:icon="@drawable/icon" android:requestLegacyExternalStorage="true">
```
