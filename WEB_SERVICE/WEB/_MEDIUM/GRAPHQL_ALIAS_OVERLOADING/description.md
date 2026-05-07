Alias Overloading in GraphQL occurs when an attacker uses a large number of aliases in a query to overwhelm the server's processing capabilities.

Aliases in GraphQL allow a client to request the same field multiple times with different names. However, excessive use of aliases in a single query can lead to Denial of Service (DoS) attacks by exhausting the server’s resources. This attack can degrade performance or cause complete service outages.
Example:

```
query oxo {
  alias1: __typename
  alias2: __typename
  alias3: __typename
  alias4: __typename
  alias5: __typename
  ...
}
```

Security Impact of Alias Overloading:

- **Denial of Service**: By sending a query with a large number of aliases, attackers can cause the server to use excessive resources to process and respond, which could slow down or crash the service.
- **Resource Exhaustion**: Servers may struggle to handle the computational load of processing numerous aliases, potentially leading to memory exhaustion, CPU spikes, or degraded performance.
- **System Unavailability**: If an Alias Overloading attack goes unchecked, it can render the GraphQL API unavailable, disrupting service for all users.