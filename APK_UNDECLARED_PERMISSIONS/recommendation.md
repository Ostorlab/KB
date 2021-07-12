Before applying a permission on any component, make sure it is declared using `<permission>` element.

For example, an app that wants to control who can start one of its activities could declare a permission for this operation as follows:

- Step 1 : I declare a permission with the name `com.example.myapp.permission.DEADLY_ACTIVITY` and fill the necessary attributes
- Step 2: I apply the permission `com.example.myapp.permission.DEADLY_ACTIVITY` on my activity

```xml

<manifest
  xmlns:android="http://schemas.android.com/apk/res/android"
  package="com.example.myapp" >
    
    <permission
      android:name="com.example.myapp.permission.DEADLY_ACTIVITY"
      android:label="@string/permlab_deadlyActivity"
      android:description="@string/permdesc_deadlyActivity"
      android:permissionGroup="android.permission-group.COST_MONEY"
      android:protectionLevel="dangerous" />
    ...
    <activity android:exported="true" android:name="com.important.PushActivity" android:permission="com.example.myapp.permission.DEADLY_ACTIVITY"/>

</manifest>
```

