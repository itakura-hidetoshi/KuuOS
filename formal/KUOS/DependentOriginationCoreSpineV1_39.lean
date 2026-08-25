import KUOS.DependentOriginationCoreSpineV1_38
import KUOS.DependentOriginationScaledHornCylinderExtensionV1_39

namespace KUOS.DependentOriginationCoreSpineV1_39

open KUOS.DependentOriginationScaledHornCylinderExtensionV1_39

/-!
# Dependent-origination core spine v1.39

This aggregate replaces the bare homotopy-class strictification boundary of
v1.38 by a geometric sufficient condition: two-sided relative cylinder
extension across one-step horn homotopies.

```text
homotopy-class equality
  -> Quot.eqvGen_exact
  -> rel / refl / symm / trans zigzag
  + two-sided scaled horn cylinder extension
  -> literal strict horn filler
  -> presentation-independent strict scaled fibrancy.
```

The underlying ordinary horn inclusions are Mathlib anodyne extensions.  The
pinned Mathlib revision does not yet supply inner/scaled-anodyne variants, so
the scaled cylinder-extension theorem remains an explicit independent target.
The parent dependent-origination object is unchanged.
-/

end KUOS.DependentOriginationCoreSpineV1_39
