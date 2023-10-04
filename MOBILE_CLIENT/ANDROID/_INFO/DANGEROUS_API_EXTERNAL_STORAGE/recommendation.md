We can distinguish four types of files based on the access permission and storage location:

* Private files:
    * A very safe way to use files
    * Must be created in the application's directory
    * Can store sensitive information and must use encryption when storing PII
    * Can be used for files that can be read/written only in the same application
    * The access privilege must be set to private mode in order to restrict access from other applications
    * Content Provider, Service or other inter-application linkage system are recommended to exchange information between applications

    === "Java"
        ```java
        public void onCreateFileClick(View view) {
            FileOutputStream fos = null;
            try {
                fos = openFileOutput(FILE_NAME, MODE_PRIVATE);

                fos.write(new String("Not sensitive information (File Activity)").getBytes());
            } catch (FileNotFoundException e) {
                mFileView.setText(R.string.file_view);
            } catch (IOException e) {
                android.util.Log.e("PrivateFileActivity","failed to read file");
            } finally {
                if (fos != null) {
                    try {
                        fos.close();
                    } catch (IOException e) {
                        android.util.Log.e("PrivateFileActivity","failed to close file");
                    }
                }
            }
            finish();
        }        
        ```


* Public Read Only files:
    * Used to disclose content to unspecified number of applications
    * The access privilege must be set to read only
    * Must not contain sensitive information
    * Using the `MODE_WORLD_READABLE` variable to create a public file is deprecated in API Level 17 and later versions, and will trigger a security exception in API Level 24 and later versions
    * File-sharing methods using Content Provider are preferable

    === "Java"
        ```java
        public void onCreateFileClick(View view) {
            FileOutputStream fos = null;
            try {
                fos = openFileOutput(FILE_NAME, MODE_WORLD_READABLE);

                fos.write(new String("Not sensitive information (Public File Activity)").getBytes());

            } catch (FileNotFoundException e) {
                mFileView.setText(R.string.file_view);
            } catch (IOException e) {
                android.util.Log.e("PublicFileActivity","failed to read file");
            } finally {
                if (fos != null) {
                    try {
                        fos.close();
                    } catch (IOException e) {
                        android.util.Log.e("PublicFileActivity","failed to close file");
                    }
                }
            }
            finish();
        }
        ```



* Public Read/Write files:
    * Used to permit Read/Write access to unspecified number of applications
    * Confidentiality and Integrity can’t be guaranteed
    * This type of file is not practical and should be avoided


* External memory (Read Write Public) files:
    * It's supposed to be used when storing huge files, or when there is a need to bring out data to outside (e.g. backup, ...)
    * In addition to having the equal characteristics of "Read Write Public file" to unspecified large number of applications, it has also the same characteristics of "Read Write Public file" to applications which declare `android.permission.WRITE.EXTERNAL.STORAGE` permission
    * In applications that output backup, some contrivances to minimize risks in terms of application spec or designing like displaying a caution “Copy Backup files to the safety location like PC etc., a.s.a.p.”, are necessary
    * Using external memory devices should be avoided, unless necessary, and encryption must be used
    * When reading in files in external memory device, validate the input data read from external memory device
    * Applications should be designed supposing that files in external memory device can be deleted

    === "Java"
        ```java
        public void onCreateFileClick(View view) {
            FileOutputStream fos = null;
            try {
                File file = new File(getExternalFilesDir(TARGET_TYPE), FILE_NAME);
                fos = new FileOutputStream(file, false);
                fos.write(new String("Non-Sensitive Information(ExternalFileActivity)").getBytes());
            } catch (FileNotFoundException e) {
                mFileView.setText(R.string.file_view);
            } catch (IOException e) {
                android.util.Log.e("ExternalFileActivity","failed to read file");
            } finally {
                if (fos != null) {
                    try {
                        fos.close();
                    } catch (IOException e) {
                        android.util.Log.e("ExternalFileActivity","failed to close file");
                    }
                }
            }
            finish();
        }
        ```
