Array-based batch queries in GraphQL occur when an attacker sends multiple queries in a single request using an array structure, which can overwhelm the server's processing capabilities.

In GraphQL, clients are typically allowed to send a single query per request. However, if not properly restricted, attackers can bundle multiple queries into a single request using an array. This can result in a Denial of Service (DoS) attack by consuming excessive server resources, degrading performance, or causing a service outage.

Example:

```
[
  { query: "{ user(id: 1) { name } }" },
  { query: "{ user(id: 2) { name } }" },
  { query: "{ user(id: 3) { name } }" }
]

```


Security Impact of Array-Based Batch Queries:

**Denial of Service:** Attackers can send large batches of queries in a single request, forcing the server to handle numerous operations simultaneously. This can lead to resource exhaustion and potential service crashes.
**Resource Exhaustion:** Like Field Duplication, array-based batch queries can spike CPU and memory usage by overloading the server with a large number of queries in a single call.
**Service Disruption:** If left unchecked, array-based batch queries can make the GraphQL API unavailable to legitimate users, causing system downtime or degraded performance.