# Incomplete Webhook Event Handling

The application exposes a webhook endpoint that receives signed lifecycle events from a third-party payment or
billing provider (for example Stripe) and uses it as the trusted reconciliation channel between the provider's
payment state and the application's internal entitlement state. The handler dispatches only on a small subset of
event types (typically the "payment succeeded" / "checkout completed" events) and silently ignores the lifecycle
events that signal that a customer's paid entitlement should be revoked or reduced — `customer.subscription.deleted`,
`customer.subscription.updated`, `invoice.payment_failed` and `charge.refunded`.

Because those events fall through to a catch-all branch that only logs and returns `200 OK` with no state mutation,
a customer who legitimately cancels, is refunded, or whose recurring payment fails is never reconciled server-side:
their subscription/entitlement record is not archived, the cached "last payment" clock that gates access is not
cleared or advanced, and any credits granted for the refunded charge are not reversed. Entitlement therefore
persists until natural expiry of the billing window (the cached payment timestamp plus the billing frequency), which
can be up to a full year for yearly plans and is indefinite for one-off / lifetime plans.

## Impact

* Continued paid access (scans, premium features, API quota) after a legitimate cancellation or refund — direct
  revenue leakage and unauthorized access retention.
* Refunded charges are not reversed: tokens, credits or quota granted from the refunded payment remain available.
* The exposure window is bounded by natural expiry for recurring plans but unbounded for one-off / lifetime plans.
* The issue is a business-logic / entitlement-persistence gap, not an unauthenticated forgery vector: the webhook is
  protected by the provider's HMAC signature verification, so the attacker model is a legitimately authenticated
  paying customer who cancels or refunds and retains access, rather than an anonymous principal.

## Example vulnerable pattern

```python
# A webhook handler that only reconciles "happy path" events.
EVENT_CHECKOUT_COMPLETED = "checkout.session.completed"
EVENT_PAYMENT_SUCCEEDED = "payment_intent.succeeded"

def webhook(request):
    event = stripe.Webhook.construct_event(
        request.body, request.headers["Stripe-Signature"], WEBHOOK_SECRET
    )
    if event.type == EVENT_CHECKOUT_COMPLETED:
        # create / extend the subscription entitlement ...
        ...
    elif event.type == EVENT_PAYMENT_SUCCEEDED:
        # advance the cached "last payment" clock ...
        ...
    else:
        # cancellation / refund / failure events land here and are silently ignored.
        logger.error("Unhandled event type %s", event.type)
    return HttpResponse(status=200)
```

The cancellation (`customer.subscription.deleted`), refund (`charge.refunded`), payment-failure
(`invoice.payment_failed`) and update (`customer.subscription.updated`) events match neither branch, reach the
`else` log-and-return, and produce no revocation, archiving, or credit reversal.

## Common causes

* The dispatch was written for the initial purchase flow only and was never extended to cover the full lifecycle.
* Entitlement checks (`is_active`, `can_scan`, `is_feature_allowed`) consult only a time-based "last payment" clock
  and ignore an `archived` / `status` flag, so even an explicit cancel path that sets `archived = True` does not
  revoke access — only natural expiry does.
* No compensating periodic reconciliation job exists that retrieves the provider-side subscription status and
  archives locally-stale entitlement rows, so cancellations performed directly in the provider dashboard, dunning
  failures, or missed webhooks are never caught.
