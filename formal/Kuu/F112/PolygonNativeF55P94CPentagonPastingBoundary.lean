import Kuu.F112.PolygonNativeF55P94UnitFourQuotientHorizontalCategory
import Mathlib.Tactic

/-!
# F112-P94C1 — genuine F54 pentagon boundary and typed F55/P92B 4-pasting audit

For FOUR consecutively typed original F45 stages (arbitrary double Nat
depth and genuinely stored F19/F28 blocks), retain the unequal actual
F54 pentagonLong / pentagonShort routes and construct the ORIGINAL
nine-constructor F55 pentagon 3-cell INSIDE the P92B presentation.

Two explicitly written vertical 3-cell pastings around this pentagon
differ by parenthesization. Their equality in the P94A quotient is
proved by an ACTUAL P94A Type-valued 4-cell, not by matching shadows.
The complete pentagon/square/odd-phase shadow and the original 3-vs-2
route obstruction are separately checked, including the north C60
four-sector instance.

This is the typed P94C pentagon boundary/pasting BASE CASE, NOT the
full four-dimensional pentagonator coherence between arbitrary
associator-naturality pastings. No additional pentagonator is inferred
from unit/associativity or numerical equality. No Gray, sorry or axioms.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

variable {p : Polygon} {a b : D} {x y : E}
variable {n₁ n₂ n₃ n₄ m₁ m₂ m₃ m₄ : Nat}
variable {p₀ p₁ p₂ p₃ p₄ : KuuNativeBlocks a b}
variable {q₀ q₁ q₂ q₃ q₄ : KuuNativeBlocks x y}
variable
  (t₁ : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁)
  (t₂ : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂)
  (t₃ : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃)
  (t₄ : KuuNativeF45Tree p n₄ m₄ p₃ q₃ p₄ q₄)

/-- The unmodified original F55 pentagon generator, included in the
actual NEW P92B proof source; this is not a shadow-derived filler. -/
def nativeF55P94CPentagonThreeCell :
    NativeF55P92AssocComparison p
      (KuuNativeF45Tree.DepthRotationRoute.pentagonLong t₁ t₂ t₃ t₄)
      (KuuNativeF45Tree.DepthRotationRoute.pentagonShort t₁ t₂ t₃ t₄) :=
  .original (.pentagon t₁ t₂ t₃ t₄)

/-- The genuine long route still has three rotations and the short
route has two; the two original F54 proof terms are not equal. -/
theorem nativeF55P94CPentagon_boundary_obstruction :
    (KuuNativeF45Tree.DepthRotationRoute.pentagonLong t₁ t₂ t₃ t₄).rotationCount = 3 ∧
    (KuuNativeF45Tree.DepthRotationRoute.pentagonShort t₁ t₂ t₃ t₄).rotationCount = 2 ∧
    KuuNativeF45Tree.DepthRotationRoute.pentagonLong t₁ t₂ t₃ t₄ ≠
      KuuNativeF45Tree.DepthRotationRoute.pentagonShort t₁ t₂ t₃ t₄ :=
  ⟨KuuNativeF45Tree.DepthRotationRoute.pentagonLong_count t₁ t₂ t₃ t₄,
   KuuNativeF45Tree.DepthRotationRoute.pentagonShort_count t₁ t₂ t₃ t₄,
   KuuNativeF45Tree.DepthRotationRoute.pentagonLong_ne_short t₁ t₂ t₃ t₄⟩

/-- The full original signed F55 shadow, not just its first charge. -/
theorem nativeF55P94CPentagonThreeCell_shadow :
    (nativeF55P94CPentagonThreeCell t₁ t₂ t₃ t₄).nativeShadow =
      (((1 : Int), (0 : Int)), (0 : ZMod 2)) := rfl

/-- A geometric rigidity statement for EVERY genuine P92B 3-proof on
this fixed long-to-short F54 boundary, not just the chosen generator:
the signed pentagon charge is necessarily 3 - 2 = 1. -/
theorem nativeF55P94CPentagon_any_charge_one
    (f : NativeF55P92AssocComparison p
      (KuuNativeF45Tree.DepthRotationRoute.pentagonLong t₁ t₂ t₃ t₄)
      (KuuNativeF45Tree.DepthRotationRoute.pentagonShort t₁ t₂ t₃ t₄)) :
    f.nativeShadow.1.1 = (1 : Int) := by
  have h := f.pentagonCharge_eq_countDefect
  rw [KuuNativeF45Tree.DepthRotationRoute.pentagonLong_count,
    KuuNativeF45Tree.DepthRotationRoute.pentagonShort_count] at h
  norm_num at h
  exact h.symm

/-- A first genuinely typed 3-proof PASTING for the four-stage
pentagon: (identity ; pentagon) ; identity. -/
def nativeF55P94CPentagonPastingLong :
    NativeF55P92AssocComparison p
      (KuuNativeF45Tree.DepthRotationRoute.pentagonLong t₁ t₂ t₃ t₄)
      (KuuNativeF45Tree.DepthRotationRoute.pentagonShort t₁ t₂ t₃ t₄) :=
  .trans
    (.trans
      (.refl (KuuNativeF45Tree.DepthRotationRoute.pentagonLong t₁ t₂ t₃ t₄))
      (nativeF55P94CPentagonThreeCell t₁ t₂ t₃ t₄))
    (.refl (KuuNativeF45Tree.DepthRotationRoute.pentagonShort t₁ t₂ t₃ t₄))

/-- The other explicitly different source 3-proof bracketing:
identity ; (pentagon ; identity). -/
def nativeF55P94CPentagonPastingShort :
    NativeF55P92AssocComparison p
      (KuuNativeF45Tree.DepthRotationRoute.pentagonLong t₁ t₂ t₃ t₄)
      (KuuNativeF45Tree.DepthRotationRoute.pentagonShort t₁ t₂ t₃ t₄) :=
  .trans
    (.refl (KuuNativeF45Tree.DepthRotationRoute.pentagonLong t₁ t₂ t₃ t₄))
    (.trans
      (nativeF55P94CPentagonThreeCell t₁ t₂ t₃ t₄)
      (.refl (KuuNativeF45Tree.DepthRotationRoute.pentagonShort t₁ t₂ t₃ t₄)))

/-- Actual TYPE-valued 4-cell comparison in the already declared P94A
presentation. It is a concrete pentagon-boundary instance of the
structural 3-proof associator, NOT an invented full pentagonator. -/
theorem nativeF55P94CPentagonPasting_fourCell :
    NativeF55P94UnitFourCell
      (nativeF55P94CPentagonPastingLong t₁ t₂ t₃ t₄)
      (nativeF55P94CPentagonPastingShort t₁ t₂ t₃ t₄) :=
  NativeF55P94UnitFourCell.verticalAssoc
    (.refl (KuuNativeF45Tree.DepthRotationRoute.pentagonLong t₁ t₂ t₃ t₄))
    (nativeF55P94CPentagonThreeCell t₁ t₂ t₃ t₄)
    (.refl (KuuNativeF45Tree.DepthRotationRoute.pentagonShort t₁ t₂ t₃ t₄))

/-- Both genuine P92B pastings descend to the SAME P94A 4-proof
class by exact Type evidence. -/
theorem nativeF55P94CPentagonPasting_class_eq :
    nativeF55P94UnitFourClass
      (KuuNativeF45Tree.pentagon0 t₁ t₂ t₃ t₄)
      (KuuNativeF45Tree.pentagon3 t₁ t₂ t₃ t₄)
      (nativeF55P94CPentagonPastingLong t₁ t₂ t₃ t₄) =
    nativeF55P94UnitFourClass
      (KuuNativeF45Tree.pentagon0 t₁ t₂ t₃ t₄)
      (KuuNativeF45Tree.pentagon3 t₁ t₂ t₃ t₄)
      (nativeF55P94CPentagonPastingShort t₁ t₂ t₃ t₄) :=
  Quot.sound ⟨nativeF55P94CPentagonPasting_fourCell t₁ t₂ t₃ t₄⟩

/-- The full signed shadow of the two 3-pastings agrees because the
actual 4-cell exists; shadow equality is CONSEQUENCE, not witness. -/
theorem nativeF55P94CPentagonPasting_shadow_sound :
    (nativeF55P94CPentagonPastingLong t₁ t₂ t₃ t₄).nativeShadow =
    (nativeF55P94CPentagonPastingShort t₁ t₂ t₃ t₄).nativeShadow :=
  (nativeF55P94CPentagonPasting_fourCell t₁ t₂ t₃ t₄).shadow_sound

/-- The P94A quotient continues to retain the original nonzero
pentagon integer, zero square charge and even original phase. -/
theorem nativeF55P94CPentagon_class_shadow :
    nativeF55P94UnitFourToShadow
      (KuuNativeF45Tree.pentagon0 t₁ t₂ t₃ t₄)
      (KuuNativeF45Tree.pentagon3 t₁ t₂ t₃ t₄)
      (KuuNativeF45Tree.DepthRotationRoute.pentagonLong t₁ t₂ t₃ t₄)
      (KuuNativeF45Tree.DepthRotationRoute.pentagonShort t₁ t₂ t₃ t₄)
      (nativeF55P94UnitFourClass _ _
        (nativeF55P94CPentagonThreeCell t₁ t₂ t₃ t₄)) =
      (((1 : Int), (0 : Int)), (0 : ZMod 2)) :=
  nativeF55P94CPentagonThreeCell_shadow t₁ t₂ t₃ t₄

/-- The same TYPE-witness pasting is present at the original, genuinely
sector-labelled north C60 four-stage F45 pentagon. -/
theorem northNativeF55P94C_pentagon_pasting_fourCell :
    NativeF55P94UnitFourCell
      (nativeF55P94CPentagonPastingLong
        northNativeF45FirstStage northNativeF45SecondStage
        northNativeF45ThirdStage northNativeF45FourthStage)
      (nativeF55P94CPentagonPastingShort
        northNativeF45FirstStage northNativeF45SecondStage
        northNativeF45ThirdStage northNativeF45FourthStage) :=
  nativeF55P94CPentagonPasting_fourCell _ _ _ _

/-- This C60 instance does not collapse the original distinct raw
F54 long/short routes when its 3-cells are later quotiented by 4-cells. -/
theorem northNativeF55P94C_original_route_obstruction :
    northNativeF45PentagonLong ≠ northNativeF45PentagonShort :=
  northNativeF45PentagonLong_ne_short

#print axioms nativeF55P94CPentagonThreeCell
#print axioms nativeF55P94CPentagon_boundary_obstruction
#print axioms nativeF55P94CPentagonThreeCell_shadow
#print axioms nativeF55P94CPentagon_any_charge_one
#print axioms nativeF55P94CPentagonPastingLong
#print axioms nativeF55P94CPentagonPastingShort
#print axioms nativeF55P94CPentagonPasting_fourCell
#print axioms nativeF55P94CPentagonPasting_class_eq
#print axioms nativeF55P94CPentagonPasting_shadow_sound
#print axioms nativeF55P94CPentagon_class_shadow
#print axioms northNativeF55P94C_pentagon_pasting_fourCell
#print axioms northNativeF55P94C_original_route_obstruction

end Kuu.F112.Physical
