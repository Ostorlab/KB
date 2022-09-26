Files saved to the external storage prior to Android 4.1 are world-readable. Prior to Android 1, files saved to external
storage are world-writable. From Android 1 to Android 4.3, only the `WRITE_EXTERNAL_STORAGE` permission is required for
an app to write to any external storage file stored by any app. Starting with Android 4.4, groups and modes of files are
created based on a directory structure, which allows an app permission to manage/read/write files within a directory
structure based on its package name. Starting with Android 4.4, users (including apps as users) are isolated from
primary external storage spaces of other apps controlled by the Android device.

Consequent to the lack of restrictions described above, files written to external storage can be modified or read by
other apps installed on the device (for the Android versions which allow read/write) and by anyone with access to the
files if stored on an off-device external storage device such as a PC (or if the in-device external storage media is
removed and mounted elsewhere).
