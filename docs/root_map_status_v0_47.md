# KuuOS Root Map Status v0.47

This stage follows root map ledger v0.46.

It adds a compact status table for the current root map layers.

## Focused check

```bash
python3 -m unittest tests.test_kuuos_root_map_status_v0_47
```

## Current layer

The table names the current check, sequence, map, ledger, and this status layer.

This layer is read-only and metadata-only.
