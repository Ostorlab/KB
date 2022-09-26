Do not seed `Random` with the current time because that value is more predictable to an attacker than the default seed.

The java.util.Random class must not be used either for security-critical applications or for protecting sensitive data.
Use a more secure random number generator, such as the java.security.SecureRandom class.