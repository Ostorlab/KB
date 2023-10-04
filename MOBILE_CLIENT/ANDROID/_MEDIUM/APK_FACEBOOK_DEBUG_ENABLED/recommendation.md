Disable debug logs before deploying your app to the public.

=== "Java"
	```java
	FacebookSdk.setIsDebugEnabled(false);
	```


Method signature:

=== "Java"
	```java
	public static void setIsDebugEnabled(boolean enabled)
	```


If the API defaults to `BuildConfig.DEBUG`.
