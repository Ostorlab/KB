To address The issue make sure to do the following:

1. **Implement DNSSEC**: Enable DNSSEC on all authoritative DNS servers for the domain, make sure to test your implementation thoroughly.

2. **Configure DNSSEC records properly**: 
   - Generate and publish DNSKEY records
   - Create and sign RRSIG records for all DNS record sets
   - Publish DS records in the parent zone

3. **Key management**:
   - Implement a secure key management process
   - Regularly rotate DNSSEC keys (ZSK and KSK)
   - Update DS records with the parent zone after key rollovers

4. **Validation and monitoring**:
   - Use online DNSSEC validation tools to verify correct implementation
   - Set up monitoring for DNSSEC-related issues and expiration dates

5. **DNS infrastructure**:
   - Ensure all DNS servers support DNSSEC
   - Configure recursive resolvers to perform DNSSEC validation

6. **Review and update**:
   - Regularly review DNSSEC configuration for best practices
   - Keep DNS software and DNSSEC tools up to date
