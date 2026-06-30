# KuuOS Repository Checkpoint Restore Authorization v1.06

This layer separates automatic restore eligibility from final execution authorization.

Evidence collection, certificate recomputation, current-state comparison, exact compare-and-swap scope generation, rejection, and audit reporting are automatic.

Any final authorization that permits a live checkpoint-reference change requires exact human approval, whether the reference is missing or substituted.

Authorization remains distinct from execution and does not invoke Git, consume a nonce, or mutate the repository.
