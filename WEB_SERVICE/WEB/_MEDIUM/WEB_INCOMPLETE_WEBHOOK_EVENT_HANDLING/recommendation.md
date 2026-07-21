Treat the webhook as the authoritative reconciliation channel between the provider's lifecycle state and the
application's entitlement state, and handle every event type that should mutate entitlement — not just the
"payment succeeded" / "checkout completed" events.

## Handle the lifecycle events explicitly

At minimum, branch on `customer.subscription.deleted`, `customer.subscription.updated`,
`invoice.payment_failed`, and `charge.refunded` in the webhook dispatch:

```python
EVENT_SUBSCRIPTION_DELETED = "customer.subscription.deleted"
EVENT_SUBSCRIPTION_UPDATED = "customer.subscription.updated"
EVENT_PAYMENT_FAILED = "invoice.payment_failed"
EVENT_CHARGE_REFUNDED = "charge.refunded"

elif event.type == EVENT_SUBSCRIPTION_DELETED:
    sub = Subscription.objects.filter(
        payment_subscription_id=event.data.object.get("id")
    ).first()
    if sub:
        sub.archived = True
        sub.last_payment_cached = None  # force immediate revocation
        sub.save()

elif event.type == EVENT_PAYMENT_FAILED:
    sub = Subscription.objects.filter(
        payment_subscription_id=event.data.object.get("subscription")
    ).first()
    if sub:
        sub.archived = True
        sub.save()

elif event.type == EVENT_CHARGE_REFUNDED:
    # reverse any credits / quota granted for the refunded charge
    ...
```

## Make entitlement revocation actually revoke access

The entitlement decision must consult the archival / status flag, not only a time-based "last payment" clock,
so that archival or a status change revokes access immediately and independently of natural expiry:

```python
def is_active(self) -> bool:
    if self.archived is True:
        return False
    if (
        self.last_payment is None
        or self.has_last_payment_expired() is True
        or self.has_started() is False
    ):
        return False
    return True
```

## Add a compensating periodic reconciliation job

Webhooks can be missed, and customers can cancel directly in the provider dashboard. Run a periodic job (for
example an Airflow DAG) that calls the provider's API (e.g. `stripe.Subscription.retrieve`) for each active
subscription and archives or expires-flag rows whose provider-side status is `canceled`, `unpaid`, or
`incomplete_expired`, so direct cancellations and dunning failures are caught even when a webhook is not delivered.

## Handle one-off / lifetime plans explicitly

For one-off plans the time-based expiry check returns `False` forever, so a refund never revokes entitlement
through the clock. Add an explicit refund / status check so refunds revoke one-off entitlements immediately
instead of relying on natural expiry.

## Test the revocation paths

Extend the webhook test suite to POST a signature-valid `customer.subscription.deleted`,
`charge.refunded`, and `invoice.payment_failed` event against an active subscription and assert that, after the
request, the subscription is archived, the cached payment clock is cleared where applicable, and the entitlement
gates (`is_active`, `can_scan`, `is_feature_allowed`) return `False`. Replace any test that codifies "ignore
unhandled events and return 200" as the intended behavior with state-change assertions for these event types.
