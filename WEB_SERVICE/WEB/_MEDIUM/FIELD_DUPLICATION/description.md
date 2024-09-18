Field Duplication in GraphQL occurs when an attacker sends a query that requests the same field repeatedly, overloading the server's processing capabilities.

In GraphQL, clients can request multiple fields in a query, including the same field multiple times. However, excessive duplication of fields can result in a Denial of Service (DoS) attack by consuming server resources. This can degrade performance or cause a service outage.
Example:

```
query overload {
  user {
    id
    id
    id
    id
    id
    ...
  }
}
```


Security Impact of Field Duplication:

- **Denial of Service:** By duplicating the same field in a query, attackers can force the server to repeatedly process the same request, leading to excessive resource use and potential service crashes.
- **Resource Exhaustion:** Similar to Alias Overloading, this attack can cause spikes in CPU and memory usage, slowing down the system and affecting overall performance.
- **Service Disruption:** If not mitigated, Field Duplication attacks can make the GraphQL API unavailable to legitimate users, leading to system downtime or degraded service.
