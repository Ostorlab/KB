Treat every verified webhook event as a request that may be delivered more than once, and make the handler idempotent by construction.

1. **Add event-ID deduplication before any side effect.** Persist the provider event identifier (for example `event["id"]`) in a dedicated table with a unique constraint, and short-circuit the branch if the identifier already exists. Apply this guard *before* any outbound provider API call or local mutation:

```python
from django.db import IntegrityError

elif event.type == EVENT_PAYMENT_SUCCEEDED:
    try:
        StripeWebhookEvent.objects.create(event_id=event["id"])  # unique-constraint dedup
    except IntegrityError:
        return HttpResponse(status=200)  # already processed — idempotent
    ...
```

2. **Wrap the mutation in a transaction with row-level locking**, mirroring the idempotency pattern used by sibling branches, and gate clock resets so the value only moves *forward* (never backward, and never beyond what the verified provider record actually authorizes):

```python
with transaction.atomic():
    subscription = SubscriptionNg.objects.select_for_update().get(
        payment_subscription_id=subscription["id"]
    )
    now = timezone.now()
    if subscription.last_payment_cached is None or now > subscription.last_payment_cached:
        subscription.last_payment_cached = now
        subscription.save()
```

3. **Bound outbound API usage.** Wrap per-delivery outbound provider calls (for example `stripe.Subscription.list(customer=customer)`) in a short-lived cache keyed by the selector (TTL ~60s) so a replay or redelivery does not amplify provider API usage.

4. **Do not hardcode webhook secrets.** Source the signing secret from an environment variable in every profile (including dev, CI, and test). A hardcoded secret (for example `whsec_test_secret`) makes signature forgery trivial in non-production, which raises this defect from a bounded replay to unbounded forgery.

5. **Verify the fix end to end.** Submit the same validly-signed event twice (via the provider's redelivery or a captured-replay harness) and assert that the protected state is mutated at most once, that the second delivery returns 200 with no state change, that the dedup row is created on first delivery and that a duplicate insert raises a uniqueness violation, and that the outbound provider call is invoked at most once per unique event.
