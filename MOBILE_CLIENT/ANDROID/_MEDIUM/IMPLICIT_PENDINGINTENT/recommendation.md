Google recommends that developers fix the vulnerability by applying any (or even better, all) of the following:

- Ensuring that the action, package, and component fields of the base Intent are set; 
- Ensuring that the PendingIntent is only delivered to trusted components; 
- Using FLAG_IMMUTABLE (added in SDK 23) to create PendingIntents. This prevents apps that receive the PendingIntent from filling in unpopulated properties. In case the app also runs on devices running SDK 22 or older, we recommend developers to apply the previous options while strengthening the PendingIntent creation with the pattern:

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
	
	        if (android.os.Build.VERSION.SDK_INT >= 23) {
			  	// Create a PendingIntent using FLAG_IMMUTABLE
				Intent base = new Intent("ACTION_FOO");
				base.setPackage("some_package");
				PendingIntent pi = PendingIntent.getService(this, 0, base, PendingIntent.FLAG_IMMUTABLE);
			} else {
				Intent base = new Intent("ACTION_FOO");
				base.setPackage("some_package");
				PendingIntent pi = PendingIntent.getService(this, 0, base, 0);
			}
	    }
	}
	```

