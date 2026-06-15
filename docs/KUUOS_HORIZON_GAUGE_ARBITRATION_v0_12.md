# KuuOS Horizon Gauge Arbitration v0.12

v0.12 compares short-, medium-, and long-horizon policy sections through pairwise connection residuals and bounded curvature.

The controller performs active parallel transport of horizon weights, preserves a positive plurality floor, and starts one v0.11 child cycle.

This layer uses gauge-theoretic local sections, connection, curvature, and holonomy. It does not use graph semantics.

The validated sequence is `experiment -> reobserve -> exploit -> exploit`, with one trial and total trial cost `0.2`.

See `formal/KUOS/OpenHorizon/HorizonGaugeArbitrationV0_12.lean` for the bounded finite formal surface.
