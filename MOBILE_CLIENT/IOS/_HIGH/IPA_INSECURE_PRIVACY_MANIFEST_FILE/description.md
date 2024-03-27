The application or third-party SDK does not declare the Privacy manifest file `PrivacyInfo.xcprivacy`.


Privacy manifest files describe the data your app or third-party SDK collects and the reasons required APIs it uses.
 
Your app and its third-party SDKs must declare the Privacy manifest file `PrivacyInfo.xcprivacy`. 
The file should record the types of data collected by your app or third-party SDK, and the required reason APIs your app or third-party SDK uses.

If your application or its third-party SDKs is using one of the APIs listed below (required reason APIs):

File timestamp APIs
System boot time APIs
Disk space APIs
Active keyboard APIs
User defaults APIs

Then you need to declare in the privacy manifest file the approved reasons that accurately reflect your use of each of these APIs and the data derived from their use. 
These declared reasons must be consistent with your app’s functionality as presented to users, and you may not use the APIs or derived data for tracking.