# Frozen legacy formal package — v5.291

This package preserves the exact complete formal tree, Lake configuration and dependency manifest at canonical commit `f4b4e7859d380019bc6dcab0ee97c3be84bbc285`. Formal tree SHA: `d72e83b11ea316730ded81cd6d73612b2ce09919`.

The old source includes Gray-dependent F51/F77 and the v5.291 module previously called Kuu-only. Those are historical results of that theory; they are not the independent current Kuu foundation. Keeping the record does not import it into the current build.

For historical reproduction only:

```bash
cd legacy/v5.291
lake exe cache get
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build \
  KUOS.DependentOriginationC60KuuOnlyOriginalIncidenceDescentV5_291
```

The old top-level README and ROADMAP are preserved byte-for-byte under `docs/legacy/`; their relative links describe the old repository root. Use the pinned commit above to navigate those historical references.

The current root package intentionally does NOT expose this package's KUOS modules. New mathematical work belongs to `formal/Kuu/` and must not depend on this archive. The existing root `formal/KUOS/` files are compatibility mirrors for historical tooling, not a supported current build surface.

Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Original license and attribution remain in effect.
