To mitigate the command injection vulnerability, here are some recommendations:
- Use input validation to ensure user-supplied data is sanitized and contains only expected values.
- Use parameterized queries to pass parameters to a query or command string in a secure manner.
- Design your app to run with the least privilege necessary to perform its intended functions.

Here's an example of a secure code that uses ProcessBuilder to execute commands safely:
The ProcessBuilder class is used to create a secure command with the ls command, the -al flag, and the /path/to/directory parameter.

=== "Java"
	```java
	String[] cmd = {"ls", "-al", "/path/to/directory"};
	ProcessBuilder pb = new ProcessBuilder(cmd);
	Process p = pb.start();
	```


=== "Kotlin"
	```kotlin
	val cmd = listOf("ls", "-al", "/path/to/directory")
	val pb = ProcessBuilder(cmd)
	val process = pb.start()
	```

In the following example, the path argument is coming from a user-input,
First, we remove any special characters and prevent command injection. Then we split it into words and check each word again to prevent any malicious commands or arguments.
Finally, we construct the 'ls' command using the sanitized input words.


=== "Dart"
	```dart
	path = ProcessManager.instance.sanitizeInput(path);
	
	// Split the input into words and sanitize each word
	List<String> words = path.split(" ");
	for (int i = 0; i < words.length; i++) {
	      words[i] = ProcessManager.instance.sanitizeInput(words[i]);
	}
	
	// Construct the command to list the files in the specified directory
	List<String> cmd = ["ls"];
	cmd.addAll(words);
	
	// Execute the command using Process.run
	ProcessResult result = await Process.run(
	      cmd[0],
	      cmd.sublist(1),
	      includeParentEnvironment: false,
	      environment: {});
	```


In the final example we are using `shell-quote` to parse and quote the shell command.

=== "Javascript"
	```javascript
	const { exec } = require('child_process');
	const command = quote(["ls",arg1, arg1]);
	 // Execute the external program and send the response back
	execFile(command, args, (err, output) => {
	      //...
	});
	```



By implementing these recommendations, you can help protect your app from command injection attacks, ensuring the security and integrity of your application and its users.
