# Historical compatibility namespace — not the current foundation

These versioned KUOS modules preserve pre-v5.292 results and old tooling paths. They are not roots of the current Lake package and cannot be imported by the independent Kuu foundation. In particular F94–F97 and v5.291 remain indirectly dependent on historical F51/F77/Gray definitions.

The exact independently buildable legacy snapshot is `legacy/v5.291/`. The current standard entry is `formal/KuuOSFormal.lean`, importing only `KuuOSStrict` and `Kuu.*`.

Do not describe these historical theorems as already ported to the new independent theory. Do not re-enable the old KUOS root to make a new proof compile.
