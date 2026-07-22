Move staging and development hostnames out of the release-included `main` source set into debug-only source sets (for example `src/debug`, `src/staging`) so they are not compiled into the production application package. Replace any hardcoded staging/development URLs shipped as Remote Config or feature-flag defaults in the `main` source set with production endpoints so a failed remote fetch cannot route production users to a non-production endpoint.

Gate any non-production server-selection branch behind `BuildConfig.DEBUG` so production builds cannot reach staging hosts even if an unrecognized server name were injected, and enforce a CI lint rule that scans the release-merged resources and strings for staging/development markers (`staging`, `dev`, `preprod`, `qa`, `uat`, `sandbox`, `localhost`, private IP ranges) to prevent regressions.

=== "Kotlin"

	```kotlin
	fun setApiServer(context: Context, serverName: String) {
	    apiUrl = when (serverName) {
	        PROD_SERVER_NAME -> RemoteConfigManager.apiProdServer
	        STAGING_SERVER_NAME, DEV_SERVER_NAME -> {
	            check(BuildConfig.DEBUG) { "Non-production server name $serverName in release build" }
	            RemoteConfigManager.apiStagingServer
	        }
	        else -> RemoteConfigManager.apiProdServer
	    }
	}
	```
