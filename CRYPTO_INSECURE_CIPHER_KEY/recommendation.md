The application must avoid, whenever possible, storing sensitive data on the device. Otherwise, the application must implement secure encryption, preferably using vetted third-party libraries that support both scanning the bytecode for possible hardcoded credentials and checking all keys to prevent any match of transformation of these values. Keys must be unique to the device and may use input from the user to compute the key. 
*    When generating a key from password, use salt. 
*    When generating a key from password, specify an appropriate hash iteration count. 
*    Use a key of length sufficient to guarantee this strength of encryption.
