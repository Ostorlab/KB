To ensure proper email authentication and mitigate the risk of phishing and email spoofing, it’s essential to configure and validate your SPF, DKIM, DMARC, and BIMI DNS records. Below are the steps to set up and verify each of these mechanisms for three different email server configurations.

=== "SPF"
  ### Validate SPF Record Syntax:
  ```bash
  dig TXT example.com | grep "v=spf1"
  ```
  ### Check for Missing SPF Records:
  ```bash
  if [ -z "$(dig +short TXT example.com | grep spf1)" ]; then
    echo "No SPF record found"
  fi
  ```

  ### Check SPF Record Length:
  ```bash
  spf_record=$(dig TXT example.com | grep "v=spf1")
  if [ ${#spf_record} -gt 255 ]; then
    echo "SPF record exceeds length limit"
  fi
  ```

  ### Verify DNS Lookup Limits:
  ```bash
  spf_check=$(dig TXT example.com | grep "v=spf1")
  lookup_count=$(echo "$spf_check" | grep -o 'include' | wc -l)
  if [ "$lookup_count" -gt 10 ]; then
    echo "SPF record exceeds the 10 DNS lookup limit"
  fi
  ```

=== "DKIM"
  ### Query DKIM Record:
  ```bash
  dig TXT default._domainkey.example.com | grep "v=DKIM1"
  ```

  ### Validate DKIM Record Syntax:
  ```bash
  dkim_record=$(dig TXT default._domainkey.example.com)
  if [[ "$dkim_record" =~ "v=DKIM1" ]]; then
    echo "Valid DKIM record"
  else
    echo "Invalid DKIM record syntax"
  fi
  ```

  ### Check DKIM Key Length:
  ```bash
  dkim_key=$(dig TXT default._domainkey.example.com | grep -o "p=.*" | cut -d' ' -f2)
  if [ ${#dkim_key} -lt 1024 ]; then
    echo "DKIM key is too short"
  fi
  ```

=== "DMARC"
  ### Query DMARC Record:
  ```bash
  dig TXT _dmarc.example.com | grep "v=DMARC1"
  ```

  ### Validate DMARC Record Syntax:
  ```bash
  dmarc_record=$(dig TXT _dmarc.example.com)
  if [[ "$dmarc_record" =~ "v=DMARC1" ]]; then
    echo "Valid DMARC record"
  else
    echo "Invalid DMARC record syntax"
  fi
  ```

  ### Check for Missing DMARC Records:
  ```bash
  if [ -z "$(dig +short TXT _dmarc.example.com)" ]; then
    echo "No DMARC record found"
  fi
  ```

  ### Analyze DMARC Policy:
  ```bash
  policy=$(dig TXT _dmarc.example.com | grep "p=")
  if [[ "$policy" =~ "p=none" ]]; then
    echo "DMARC policy is set to 'none' – no action taken on unauthenticated emails"
  elif [[ "$policy" =~ "p=reject" ]]; then
    echo "DMARC policy is set to 'reject' – unauthenticated emails are rejected"
  elif [[ "$policy" =~ "p=quarantine" ]]; then
    echo "DMARC policy is set to 'quarantine' – unauthenticated emails are flagged"
  fi
  ```

=== "BIMI"
  ### Query BIMI Record:
  ```bash
  dig TXT default._bimi.example.com | grep "v=BIMI1"
  ```

  ### Validate BIMI Record Syntax:
  ```bash
  bimi_record=$(dig TXT default._bimi.example.com)
  if [[ "$bimi_record" =~ "v=BIMI1" ]]; then
    echo "Valid BIMI record"
  else
    echo "Invalid BIMI record syntax"
  fi
  ```

  ### Verify BIMI Logo URL:
  ```bash
  logo_url=$(dig TXT default._bimi.example.com | grep "l=" | cut -d'=' -f2)
  if curl --output /dev/null --silent --head --fail "$logo_url"; then
    echo "Valid logo URL"
  else
    echo "Invalid logo URL"
  fi
  ```
