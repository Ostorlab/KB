To ensure a safe validation of the hostname, consider the implementations below.

1. Implement Regular Expression (Regex) Validation: Instead of using simple methods like `startsWith` or `endsWith`, opt for regular expressions to perform thorough hostname validation. Regex patterns can allow for precise matching criteria.

2. Consider Standardized Validation Libraries: Utilize established libraries or frameworks that offer robust hostname validation functionalities. These libraries are often well-maintained and regularly updated to address potential security flaws.

3. Implement Whitelisting: If the you have a limited number of whitelisted hosts, consider implementing a whitelist approach where only known and trusted hostnames are accepted by the application. 