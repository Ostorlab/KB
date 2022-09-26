Make sure you are only exporting broadcast receivers that really need the ability to be started by any third-party
applications; or create a permission with android:protectionLevel="signature" in the AndroidManifest.xml file and use it
for all broadcast receivers that are to be started only by your applications, setting exported="false" for all broadcast
receivers that should not be started by third-party applications at all.