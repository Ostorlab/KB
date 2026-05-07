Directive Overloading in GraphQL occurs when an attacker leverages a large number of directives in a query to overwhelm the server's processing capabilities. 

Directives in GraphQL are used to modify the behavior of queries, but excessive use can lead to Denial of Service (DoS) attacks by exhausting server resources. This kind of attack can cause performance degradation or complete service outages.

Example:

```
query oxo {
  __typename @aa @aa @aa @aa @aa @aa @aa @aa @aa @aa
}
```

The security impact of Directive Overloading can lead to the following issues:

- **Denial of Service**: By sending an excessive number of directives in a single query, attackers can overwhelm the server, causing legitimate users to experience slow responses or service outages.
- **Resource Exhaustion**: Servers may use significant computational resources to parse and validate the directives, which can result in memory exhaustion or CPU spikes.
- **System Unavailability**: If left unchecked, a Directive Overloading attack could make the GraphQL service unavailable for all users.