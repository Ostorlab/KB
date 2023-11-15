Implicit PendingIntent is a vulnerability which may cause security threats in the form of denial-of-service, private data theft, and privilege escalation. Please review the detailed steps below to fix the issue with your apps. 
 
=== "Java"
	```java
	import android.content.Intent;
	import android.os.Bundle;
	import android.support.v7.app.AppCompatActivity;
	
	public class YourActivity extends AppCompatActivity {
	
	    @Override
	    protected void onCreate(Bundle savedInstanceState) {
	        super.onCreate(savedInstanceState);
	        setContentView(R.layout.activity_main);
	
	        // Create an implicit base Intent and wrap it in a PendingIntent
			Intent base = new Intent("ACTION_FOO");
			base.setPackage("some_package");
			PendingIntent pi = PendingIntent.getService(this, 0, base, 0);
	    }
	}
	```

