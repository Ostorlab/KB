Do not include Sensitive Informaiton  in Operation Log Information.
Use Log.d() or Log.v() Method When Outputting Throwable Object, the return value should not be used for substitution or comparison.
Construct the Build System to Auto-delete inappropriate logging methods in Release version application.
Use the most appropriate method when outputting log messages: 
	ERROR: Log.e() , WARN: Log.w(), INFO: Log.i()
	DEBUG: Log.d(), VERBOSE: Log.v()  // Not Always Deleted Automatically
