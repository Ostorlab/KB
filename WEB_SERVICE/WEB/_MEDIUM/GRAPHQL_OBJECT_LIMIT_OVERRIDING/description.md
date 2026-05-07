Object Limit Overriding in GraphQL refers to a vulnerability where an attacker can manipulate query arguments to exceed the intended limits of an API. This often involves passing extremely large values to pagination or limit parameters, potentially leading to denial-of-service (DoS) attacks or excessive resource consumption.

Potential Risks:

**Denial of Service (DoS):** By requesting an excessive number of objects, attackers can overwhelm the server, causing performance degradation or outages.

**Resource Exhaustion:** Queries requesting a vast number of objects can overload the server's memory and processing capabilities.

**Data Exposure:** In some cases, bypassing limits could lead to unauthorized access to large amounts of data.

**Increased Costs:** For cloud-based services, processing queries with extremely large limits may result in unexpected costs due to high resource usage.

Vulnerable Query Example:

```graphql
query {
  users(first: 1000000) {
    id
    name
    email
  }
}
```