The hasFragileUserData flag can be added to the application node of AndroidManifest.xml. 
####
If its value is true, then when the user uninstalls the app, a prompt will be shown to the user asking him whether to keep the app's data.

```xml
<application android:icon="@drawable/icon" android:hasFragileUserData="true">
```
