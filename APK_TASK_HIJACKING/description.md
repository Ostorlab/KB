In Android, a task is a collection of activities that users interact with when performing a certain job. 

Activities from different apps can reside in the same task which might be used to relocate a malicious activity to your application's task by
manipulating the following parameters:
 - Task affinity
 - allowTaskReparenting
 
 Task Affinity is an activity attribute defined in each <activity> tag in AndroidManifest.xml. It specifies which task that the activity desires
to join. By default, all activities in an app have the same affinity (the app package name)

```javas
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
package="co.secureApp.app“ >
<application>
<activity android:name=".ActivityA “/>
<activity android:name=".ActivityB“ android:taskAffinity="co.ostorlab.Myapp:taskB “/>
</application>
</manifest>
``` 

allowTaskReparenting when set to `true` for an activity A, and when a new task with the same affinity is brought to the front, the
system would move the “relocatable” activity A from its original hosting task to this new foreground task.

Task Hijacking attack:

- Case1:

My application has a  packagename `com.mySecureApp.app` and an activity A1.
A malicious application has two activities M1 and M2 where M2.taskAffinity =  `com.mySecureApp.app` and M2.allowTaskReparenting = `true`

If the malicious app is open on M2, once you start your application, M2 is relocated to the front and the user will interact with the malicious application.  
