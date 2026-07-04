# KuuOS Lifecycle Bounded Transition Start Authorization v0.21

Lifecycle Bounded Transition Start Authorization v0.21 follows Lifecycle Bounded Transition Approval v0.20.

The stage accepts only an approval record with this status.

```text
LIFECYCLE_BOUNDED_TRANSITION_APPROVAL_APPROVED_FOR_SEPARATE_TRANSITION_START_AUTHORIZATION
```

The stage authorizes or denies the later start of the prepared lifecycle transition.

It does not start the transition.

It does not complete the transition.

It does not mutate lifecycle state, authority state, external state, or repository state.

The three statuses are:

```text
LIFECYCLE_BOUNDED_TRANSITION_START_AUTHORIZATION_AUTHORIZED_FOR_SEPARATE_TRANSITION_START
LIFECYCLE_BOUNDED_TRANSITION_START_AUTHORIZATION_DENIED
LIFECYCLE_BOUNDED_TRANSITION_START_AUTHORIZATION_REJECTED
```

AUTHORIZED issues a start-authorization record and routes only to a later separate transition-start stage.

DENIED issues a valid record but does not route to transition start.

REJECTED issues no valid record.

The implementation recomputes the v0.20 source artifact and binds the source start-authorization route, transition package digest, future operator, current lifecycle state digest, target lifecycle state digest, and transition start route.
