## Case Study: $450,000 Google Cloud API Key Compromise

A translation app with a Google Cloud backend experienced a catastrophic API key compromise that resulted in $450,000 in charges over 1.5 months. The app had been running consistently at $1,500/month for years before the incident.

### What Happened:
- 19 billion characters of translations were processed without the owner's knowledge
- No warning emails from Google Cloud about the anomalous usage
- Google Cloud refused to provide a full refund, offering only $50k in credits
- The actual cost to Google for the resources used was estimated at 1-20% of the charged amount
- No easy way to set billing caps in Google Cloud's controls
- The company is now migrating off Google Cloud

### Key Lessons:
1. API keys must be secured and rotated regularly
2. Cloud providers may not provide adequate warnings about anomalous usage
3. Billing caps are critical but often not easily configurable
4. Compromised API keys can lead to catastrophic financial consequences
5. Cloud providers may refuse refunds even when usage is clearly fraudulent

Source: [Reddit Post](https://www.reddit.com/r/googlecloud/comments/1i21otu/450000_charge_from_google_cloud_no_refund/)
