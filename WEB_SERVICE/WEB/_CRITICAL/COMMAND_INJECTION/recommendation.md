To mitigate the command injection vulnerability, here are some recommendations:

- __Input Validation and Sanitization__: Always validate and sanitize user inputs. Ensure that any user-supplied data passed to the system shell or command execution functions is sanitized and restricted to expected characters or patterns.


- __Least Privilege Principle__: Run your application or services with the least possible privileges required to perform necessary actions. Avoid running services with superuser or administrator privileges.


- __Avoid Executing User-Supplied Input__: Refrain from executing user-supplied data directly within commands or system shells. Validate and use whitelists or predefined options wherever possible.


- __Use Security Libraries__: Employ security-focused libraries or frameworks that handle user inputs and command execution securely. These libraries often provide functions or methods that mitigate common vulnerabilities.

### Examples

#### Java

```java
Scanner scanner = new Scanner(System.in);

System.out.print("Enter the file name: ");
String userInput = scanner.nextLine(); // Takes user input

// Sanitize user input to prevent command injection
String sanitizedInput = userInput.replaceAll("[^A-Za-z0-9]", ""); // Example sanitization

// Command execution
ProcessBuilder processBuilder = new ProcessBuilder("ls", "-l", sanitizedInput);

// Redirect error stream to output
processBuilder.redirectErrorStream(true);

Process process = processBuilder.start();
```

#### Php

```php
<?php
// User-supplied filename
$userInput = $_POST['filename']; // Example: 'file.txt'

// Validate and sanitize user input
if (preg_match('/^[a-zA-Z0-9_\.]+$/', $userInput)) { // Validate against alphanumeric and dot
    // Safely escape the user input to prevent command injection
    $escapedInput = escapeshellarg($userInput);

    // Command execution using the sanitized input
    $command = "ls -l " . $escapedInput;
    $output = shell_exec($command);

    echo "<pre>$output</pre>";
} else {
    echo "Invalid filename input!";
}
?>
```