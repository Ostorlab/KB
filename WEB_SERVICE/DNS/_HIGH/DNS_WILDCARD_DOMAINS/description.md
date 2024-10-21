DNS wildcard domains allow a domain owner to specify that all subdomains (or non-existent subdomains) resolve to the same IP address. While this can simplify domain management, it also introduces significant security risks. Attackers can exploit wildcard domains to:

- **Create Phishing Subdomains:** Attackers can easily set up phishing websites using subdomains of a wildcard domain, making them look legitimate.
- **Subdomain Takeover:** If the hosting service for a wildcard domain is misconfigured or abandoned, attackers may take control of subdomains and use them for malicious purposes.
- **Abuse of Trust:** Users may mistakenly trust all subdomains under a wildcard domain, making them vulnerable to malicious content served from those subdomains.

### Example Scenario:
An organization configures a wildcard domain (`*.example.com`) for its site. An attacker identifies an unclaimed or misconfigured subdomain and uses it to host a phishing page (`login.example.com`). Since it falls under the same domain, users and even some security tools may trust the site, leading to credential theft.