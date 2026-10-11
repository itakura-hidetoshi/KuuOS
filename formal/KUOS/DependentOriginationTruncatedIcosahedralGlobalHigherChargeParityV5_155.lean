import KUOS.DependentOriginationTruncatedIcosahedralCyclicHigherChargeCollarV5_155

namespace KUOS.DependentOriginationTruncatedIcosahedralGlobalHigherChargeV5_155

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans
open KUOS.DependentOriginationTruncatedIcosahedralStarRefinementV3_83
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationTruncatedIcosahedralFlagSquaresV5_154
open KUOS.DependentOriginationTruncatedIcosahedralPentagonRotationBridgeV5_154
open KUOS.DependentOriginationTruncatedIcosahedralHigherChargeV5_155
open KUOS.DependentOriginationTruncatedIcosahedralCyclicChargeV5_155
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false
noncomputable section

/-!
# F58-F / v5.155 — global C60 pentagon-collar higher generator-charge and parity

The REAL truncated-icosahedral seed has exactly 12 original
icosahedral vertices, each creating one genuine five-edge
pentagonal C60 face, hence exactly 60 around-vertex edges.
F58-E proved each of those pentagons plus its FIVE actual
cyclic corner-glued four-flag square labels has independent
additive generator-charge pair (1,5) in Int × Int.

With the SAME explicitly supplied original F55 F45 t1/t2 local
square rotations repeated as labels over all geometric C60
pentagon-hexagon shared edges, the global finite sum is (12,60).

The independent group homomorphism coordinatewise Int -> ZMod 2
detects the nonzero LOCAL signature (1,1), but its GLOBAL
uniform twelve-pentagon sum vanishes (0,0). This is a concrete
and fully typed parity-collapse test on the NEW F58 additive
generator charges, reminiscent of but NEVER IDENTIFIED WITH
the older v4.14 Stage-II obstruction-class uniform-parity
computation: any such comparison is a separate unproved map.

Nothing here proves a tricategorical/Gray 3-cell coherence law,
equates all F55 free path syntax, or asserts nontriviality of a
global Stage-II class.
-/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

/-- Coordinatewise reduction of the independent signed pentagon and
square generator-charge pair. This is NOT the old Stage-II map ω;
no old obstruction class is identified with a charge coordinate. -/
def originalC60HigherChargeMod2
    (z : Int × Int) : ZMod 2 × ZMod 2 :=
  ((z.1 : ZMod 2), (z.2 : ZMod 2))

/-- Reverify the original C60 seed's twelve icosahedral vertices
using kernel reduction rather than importing the old v3.84
`native_decide`-specific compiler axiom. -/
theorem originalC60IcosahedralVertex_card_kernel :
    Fintype.card IcosahedralVertex = 12 := by
  decide

section GlobalActualPentagonCollars
variable {a b : D} {x y : E}
variable {n₁ n₂ m₁ m₂ : Nat}
variable {p₀ p₁ p₂ : Blocks a b}
variable {q₀ q₁ q₂ : Blocks x y}
variable
  (t₁ : OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁)
  (t₂ : OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂)
variable
  {leftAfter : OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁}
  {rightAfter : OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂}
  (left : OriginalF45BracketTree.LocalRotation t₁ leftAfter)
  (right : OriginalF45BracketTree.LocalRotation t₂ rightAfter)

/-- Every ACTUAL vertex-origin pentagon collar has LOCAL mod-two
generator-charge (1,1); both original pentagon and square
coordinates survive on each individual five-edge face. -/
theorem originalC60LocalCollarCharge_mod2
    (v : IcosahedralVertex) :
    originalC60HigherChargeMod2
      (originalC60PentagonSquareCollarCharge t₁ t₂ left right v) =
      ((1 : ZMod 2), (1 : ZMod 2)) := by
  rw [originalC60PentagonSquareCollarCharge_eq t₁ t₂ left right v]
  norm_num [originalC60HigherChargeMod2] ; decide

/-- The genuine C60 has EXACTLY twelve distinct original
vertex-origin pentagonal faces, each with exact signed integer
generator-charge (1,5), and their total is therefore (12,60).
This is a finite sum of ACTUAL original 60 around-edge labels,
not a formal assertion of external composability of 3-cells. -/
theorem originalC60GlobalPentagonCollarCharge :
    (∑ v : IcosahedralVertex,
      originalC60PentagonSquareCollarCharge t₁ t₂ left right v) =
      ((12 : Int), (60 : Int)) := by
  calc
    (∑ v : IcosahedralVertex,
      originalC60PentagonSquareCollarCharge t₁ t₂ left right v) =
        ∑ _v : IcosahedralVertex, ((1 : Int), (5 : Int)) := by
          apply Finset.sum_congr rfl
          intro v _
          exact originalC60PentagonSquareCollarCharge_eq t₁ t₂ left right v
    _ = ((12 : Int), (60 : Int)) := by
          simp only [Finset.sum_const, Finset.card_univ]
          rw [originalC60IcosahedralVertex_card_kernel]
          decide

/-- Although the independently defined higher-charge pair is
nonzero on a single actual C60 pentagon, the uniform global
charge vanishes after mapping its two integer coordinates into
ZMod 2, because 12 and 60 are both even. -/
theorem originalC60GlobalPentagonCollarCharge_mod2_zero :
    originalC60HigherChargeMod2
      (∑ v : IcosahedralVertex,
        originalC60PentagonSquareCollarCharge t₁ t₂ left right v) =
      ((0 : ZMod 2), (0 : ZMod 2)) := by
  rw [originalC60GlobalPentagonCollarCharge t₁ t₂ left right]
  change ((12 : ZMod 2), (60 : ZMod 2)) =
    ((0 : ZMod 2), (0 : ZMod 2))
  apply Prod.ext
  · calc
      (12 : ZMod 2) = 6 * (2 : ZMod 2) := by ring
      _ = 0 := by rw [ZMod.natCast_self]; simp
  · calc
      (60 : ZMod 2) = 30 * (2 : ZMod 2) := by ring
      _ = 0 := by rw [ZMod.natCast_self]; simp

/-- The local-to-global distinction is REAL and proved: the
individual C60 pentagon charge survives mod 2 whereas its
uniform twelve-pentagon / sixty-square global image vanishes.
There is no assertion that this NEW additive charge is the
older original Stage-II ZMod2 obstruction class. -/
theorem originalC60LocalNonzeroGlobalZero
    (v : IcosahedralVertex) :
    originalC60HigherChargeMod2
      (originalC60PentagonSquareCollarCharge t₁ t₂ left right v) ≠
        ((0 : ZMod 2), (0 : ZMod 2)) ∧
    originalC60HigherChargeMod2
      (∑ w : IcosahedralVertex,
        originalC60PentagonSquareCollarCharge t₁ t₂ left right w) =
      ((0 : ZMod 2), (0 : ZMod 2)) := by
  constructor
  · rw [originalC60LocalCollarCharge_mod2 t₁ t₂ left right v]
    decide
  · exact originalC60GlobalPentagonCollarCharge_mod2_zero t₁ t₂ left right

end GlobalActualPentagonCollars

#print axioms originalC60HigherChargeMod2
#print axioms originalC60IcosahedralVertex_card_kernel
#print axioms originalC60LocalCollarCharge_mod2
#print axioms originalC60GlobalPentagonCollarCharge
#print axioms originalC60GlobalPentagonCollarCharge_mod2_zero
#print axioms originalC60LocalNonzeroGlobalZero

end
end KUOS.DependentOriginationTruncatedIcosahedralGlobalHigherChargeV5_155
