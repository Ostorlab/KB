In mobile applications, A secure implementation of mobile biometric authentication guarantees the need to use Face ID or Touch ID authentication to access the application’s sensitive data.

a secure implementation of biometric authentication goes beyond just verifying the fingerprint or the face to log in. It also includes encrypting the application's sensitive data using the biometric data.

This encryption adds an extra layer of protection, making it highly challenging for unauthorized individuals to access or use sensitive information. Encryption with biometric data becomes crucial in case an unauthorized party gains access to the device, via Malware or physical access.

Without encryption, an attacker can manipulate the memory to bypass the biometric check and log in successfully to the application. However, they would be unable to interpret or utilize the application data if the encryption is used with the biometric data. This helps to maintain the confidentiality of the application's sensitive information, thereby safeguarding the privacy and security of users' data.

In the example below from DVIA, it is possible to bypass biometric authentication by hooking evaluatePolicy using frida

=== "Swift"
	```Swift
	+(void)authenticateWithTouchID {
     
    LAContext *myContext = [[LAContext alloc] init];
    NSError *authError = nil;
    NSString *myLocalizedReasonString = @"Please authenticate yourself";
     
    if ([myContext canEvaluatePolicy:LAPolicyDeviceOwnerAuthenticationWithBiometrics error:&authError]) {
        [myContext evaluatePolicy:LAPolicyDeviceOwnerAuthenticationWithBiometrics
                  localizedReason:myLocalizedReasonString
                            reply:^(BOOL success, NSError *error) {
                                if (success) {
                                    dispatch_async(dispatch_get_main_queue(), ^{
                                    [TouchIDAuthentication showAlert:@"Authentication Successful" withTitle:@"Success"];
                                    });
                                } else {
                                    dispatch_async(dispatch_get_main_queue(), ^{
                                       [TouchIDAuthentication showAlert:@"Authentication Failed !" withTitle:@"Error"];
                                    });
                                }
                            }];
		} else {
			dispatch_async(dispatch_get_main_queue(), ^{
				[TouchIDAuthentication showAlert:@"Your device doesn't support Touch ID or you haven't configured Touch ID authentication on your device" withTitle:@"Error"];
			});
		}
	}
	```


