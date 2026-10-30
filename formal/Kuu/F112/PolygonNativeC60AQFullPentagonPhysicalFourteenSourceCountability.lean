import Mathlib.Tactic.DeriveCountable
import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalFifteenSyntaxCountability

/-!
# F112-P94D3GE — source-aware 14D Countable derivation probe

Work with the genuine original 14D source Type-valued inductive,
preserving all its constructor-specific 8D–13D arguments and source
category Hom, rather than replacing it by a finite C60 graph.

The existing 14D core and structural inductives contain exact
higher endpoints and lower original proof evidence. Test whether
mathlib's pinned standalone Countable derivation can construct a
faithful Nat code and an injectivity proof for both original families
without editing their definitions. No category Hom is postulated
Countable simply from C60's finite geometry.

Pinned Lean v4.30.0-rc2, mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Append-only; 107 roots, protected #1558 untouched, no new axioms.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

deriving instance Countable for NativeK5CoreFourteenCell
deriving instance Countable for NativeK5StructuralFourteenCell

end
end Kuu.F112.Physical
