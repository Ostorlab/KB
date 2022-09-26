One or more of the application's broadcast receivers is dynamically registered in the code and not protected by
signature permission in the AndroidManifest.xml file. All of the dynamically registered receivers are exported. Using a
malware application, an attacker can broadcast arbitrary data to the exported receiver, which can lead to invocation of
different components of the application or to code execution. For example, a lot of broadcast receivers are programmed
to receive SMS messages or GCM messages. To work properly, these receivers should always be exported to receive data
from other applications, such as the SMS app or the GCM framework. To secure receivers like this, you should always
declare appropriate permissions during the call to the registerReceiver method. Broadcast receivers represent a likely
exploitable component which is often used to start services, so it's highly recommended to check all of the external
data is passed to them. To enable the most restrictive and therefore secure policy, you should minimize the number of
exported intents by using the signature permissions.