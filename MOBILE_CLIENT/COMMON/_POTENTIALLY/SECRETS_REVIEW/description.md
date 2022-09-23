The application is detected to contain secret credentials, like SSH keys, private certificate or private API keys.

Secrets can be split into 3 categories with different risk profiles:

* Over-billing: affects API keys that grant access to services like Google Maps and are billed by number of requests.
Attackers will harvest the keys to access the service without paying while the target is paying for the service.
  
* Unauthorized Access: affects keys, secrets and token that grant access to services like S3 buckets. If
the service improperly configured, attackers can get access to unauthorized data or elevate his privileges through 
  other services.
  

