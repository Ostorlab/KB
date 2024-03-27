It is mandatory to add the privacy manifest files to your application and your third-party SDK if it’s listed in `SDKs that require a privacy manifest and signature`.

To add the privacy manifest to your app or third-party SDK in Xcode, follow these steps:
- Choose File > New File.
- Scroll down to the Resource section, and select App Privacy File type.
- Click Next.
- Check your app or third-party SDK's target in the Targets list.
- Click Create.

Also, make sure to include the reason why the application or the third-party SDK uses the required reason API. 
To do so, for each category of required reason API that your app or third-party SDK uses, add a dictionary to the `NSPrivacyAccessedAPITypes` array in your app or third-party SDK’s privacy manifest file that reports the reasons your app uses the API category.
Each dictionary in the `NSPrivacyAccessedAPITypes` array needs to contain these keys and values:

- `NSPrivacyAccessedAPIType`: A string that identifies the category of required reason APIs your app uses. The value you provide must be one of the values listed in the sections below.
- `NSPrivacyAccessedAPITypeReasons`: An array of strings that identifies the reasons your app uses the APIs. The values you provide must be the values associated with the accessed API type in the sections below.

**Starting May 1, 2024, apps that don’t describe their use of required reason API in their privacy manifest file aren’t accepted by App Store Connect.