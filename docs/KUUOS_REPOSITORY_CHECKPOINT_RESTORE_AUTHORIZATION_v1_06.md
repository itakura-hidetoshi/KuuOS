# KuuOS Repository Checkpoint Restore Authorization v1.06

This layer separates automatic restore eligibility from final execution authorization.

A missing local checkpoint reference may use an exact pre-authorized compare-and-swap path without new human review.

Replacing an existing substituted reference requires exact human approval.

Authorization remains distinct from execution and does not invoke Git or mutate the repository.
