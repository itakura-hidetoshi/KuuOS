import Kuu.F112.PolygonNativeF55P94DK5FiveStageTypedShell
import Mathlib.Tactic

/-!
# F112-P94D2 — all NINE five-stage K₅ faces as true F55/P92B 3-cells

Each of the six K₅ pentagonal boundaries is the EXISTING genuine
four-stage original F55 pentagon generator, placed in one actual
native F45 binary-tree context, or applied to an actual consecutive
pair node of the original five stages.

Each of the THREE K₅ quadrilaterals is the explicitly NEW P92B
associator-naturality generator, applied to an actual F54 associator
in one of the three arguments, with genuinely typed identity routes
in the two other arguments. These are NOT the unrelated six-leaf
F55 original disjointSquare with odd ZMod2 charge.

All nine have the full original native F45 Blocks and independent
Nat histories; their signed full shadows are computed from ACTUAL
source proof terms, not assigned from matching numerical metadata.
This is the face-by-face typed boundary stage, not yet the global
2-sphere boundary pasting or Type-valued 4D pentagonator filler.
No Gray, sorry, admit or added logical axioms.
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

section FiveNativeStages

variable {p : Polygon} {a b : D} {x y : E}
variable {n₁ n₂ n₃ n₄ n₅ m₁ m₂ m₃ m₄ m₅ : Nat}
variable {p₀ p₁ p₂ p₃ p₄ p₅ : KuuNativeBlocks a b}
variable {q₀ q₁ q₂ q₃ q₄ q₅ : KuuNativeBlocks x y}
variable
  (t1 : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁)
  (t2 : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂)
  (t3 : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃)
  (t4 : KuuNativeF45Tree p n₄ m₄ p₃ q₃ p₄ q₄)
  (t5 : KuuNativeF45Tree p n₅ m₅ p₄ q₄ p₅ q₅)

/-- K₅ face #3: the original 4-stage pentagon inside the RIGHT
context of the true first F45 stage (five leaf positions). -/
def nativeK5PentagonFace3 :=
  NativeF55P92AssocComparison.rightContext t1
    (nativeF55P94CPentagonThreeCell t2 t3 t4 t5)

/-- K₅ face #4: genuinely consecutive t4;t5 as the FOURTH
original F55 pentagon argument. -/
def nativeK5PentagonFace4 :=
  nativeF55P94CPentagonThreeCell t1 t2 t3 (.node t4 t5)

/-- K₅ face #5: t3;t4 as the THIRD original F55 argument. -/
def nativeK5PentagonFace5 :=
  nativeF55P94CPentagonThreeCell t1 t2 (.node t3 t4) t5

/-- K₅ face #6: t2;t3 as the SECOND original F55 argument. -/
def nativeK5PentagonFace6 :=
  nativeF55P94CPentagonThreeCell t1 (.node t2 t3) t4 t5

/-- K₅ face #7: t1;t2 as the FIRST original F55 argument. -/
def nativeK5PentagonFace7 :=
  nativeF55P94CPentagonThreeCell (.node t1 t2) t3 t4 t5

/-- K₅ face #8: original first-four-stage F55 pentagon inside
the LEFT native F45 context of the fifth stage. -/
def nativeK5PentagonFace8 :=
  NativeF55P92AssocComparison.leftContext
    (nativeF55P94CPentagonThreeCell t1 t2 t3 t4) t5

/-- Real F54 identity route on a stored F45 stage. No equality
between unrelated trees or depths is assumed. -/
def nativeK5RouteUnit
    {n m : Nat} {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (t : KuuNativeF45Tree p n m ma pa mb pb) :
    KuuNativeF45Tree.DepthRotationRoute p t t :=
  .chain (.refl t)

/-- Square #0: associator naturality in the THIRD argument, with
the actual t3-t4-t5 source reassociation and two route units. -/
def nativeK5NaturalitySquare0 :=
  NativeF55P92AssocComparison.assocNaturality
    (nativeK5RouteUnit t1) (nativeK5RouteUnit t2)
    (KuuNativeF45Tree.DepthRotationRoute.assoc t3 t4 t5)

/-- Square #1: associator naturality in the SECOND argument. -/
def nativeK5NaturalitySquare1 :=
  NativeF55P92AssocComparison.assocNaturality
    (nativeK5RouteUnit t1)
    (KuuNativeF45Tree.DepthRotationRoute.assoc t2 t3 t4)
    (nativeK5RouteUnit t5)

/-- Square #2: associator naturality in the FIRST argument. -/
def nativeK5NaturalitySquare2 :=
  NativeF55P92AssocComparison.assocNaturality
    (KuuNativeF45Tree.DepthRotationRoute.assoc t1 t2 t3)
    (nativeK5RouteUnit t4) (nativeK5RouteUnit t5)

/-- Every genuine pentagon face uses the ORIGINAL F55 3-cell and
retains its actual (+1,0,even) full shadow. The shell orientation
from P94D1 reverses #5,#7,#8; that global orientation adjustment
is not a raw constructor equality. -/
theorem nativeK5PentagonFace3_shadow :
    (nativeK5PentagonFace3 t1 t2 t3 t4 t5).nativeShadow =
      (((1 : Int), (0 : Int)), (0 : ZMod 2)) := rfl
theorem nativeK5PentagonFace4_shadow :
    (nativeK5PentagonFace4 t1 t2 t3 t4 t5).nativeShadow =
      (((1 : Int), (0 : Int)), (0 : ZMod 2)) := rfl
theorem nativeK5PentagonFace5_shadow :
    (nativeK5PentagonFace5 t1 t2 t3 t4 t5).nativeShadow =
      (((1 : Int), (0 : Int)), (0 : ZMod 2)) := rfl
theorem nativeK5PentagonFace6_shadow :
    (nativeK5PentagonFace6 t1 t2 t3 t4 t5).nativeShadow =
      (((1 : Int), (0 : Int)), (0 : ZMod 2)) := rfl
theorem nativeK5PentagonFace7_shadow :
    (nativeK5PentagonFace7 t1 t2 t3 t4 t5).nativeShadow =
      (((1 : Int), (0 : Int)), (0 : ZMod 2)) := rfl
theorem nativeK5PentagonFace8_shadow :
    (nativeK5PentagonFace8 t1 t2 t3 t4 t5).nativeShadow =
      (((1 : Int), (0 : Int)), (0 : ZMod 2)) := rfl

/-- In the selected P92B extension all three genuine K₅
naturality generators have precisely the chosen ZERO full shadow.
The original F55 odd disjoint-square phase is not destroyed. -/
theorem nativeK5NaturalitySquare0_shadow :
    (nativeK5NaturalitySquare0 t1 t2 t3 t4 t5).nativeShadow =
      (0 : KuuNativeF55Shadow) := rfl
theorem nativeK5NaturalitySquare1_shadow :
    (nativeK5NaturalitySquare1 t1 t2 t3 t4 t5).nativeShadow =
      (0 : KuuNativeF55Shadow) := rfl
theorem nativeK5NaturalitySquare2_shadow :
    (nativeK5NaturalitySquare2 t1 t2 t3 t4 t5).nativeShadow =
      (0 : KuuNativeF55Shadow) := rfl

/-- Inversion of the full proof source is an ORIGINAL typed P92B
constructor; the three negatively oriented K₅ faces are real
witnesses, not arithmetic negatives invented for a numeric shadow. -/
def nativeK5PentagonFace5_oriented :=
  NativeF55P92AssocComparison.symm (nativeK5PentagonFace5 t1 t2 t3 t4 t5)
def nativeK5PentagonFace7_oriented :=
  NativeF55P92AssocComparison.symm (nativeK5PentagonFace7 t1 t2 t3 t4 t5)
def nativeK5PentagonFace8_oriented :=
  NativeF55P92AssocComparison.symm (nativeK5PentagonFace8 t1 t2 t3 t4 t5)

/-- Actual nine genuine proof-term shadows cancel under the outward
K₅ orientation. This still does NOT assert all nine differently
typed 3-cells form a pastable spherical composite or admit a 4D
filler; both remain the next independent coherence problem. -/
theorem nativeK5NineGenuineFaceShadows_balance :
    (nativeK5PentagonFace3 t1 t2 t3 t4 t5).nativeShadow +
    (nativeK5PentagonFace4 t1 t2 t3 t4 t5).nativeShadow +
    (nativeK5PentagonFace5_oriented t1 t2 t3 t4 t5).nativeShadow +
    (nativeK5PentagonFace6 t1 t2 t3 t4 t5).nativeShadow +
    (nativeK5PentagonFace7_oriented t1 t2 t3 t4 t5).nativeShadow +
    (nativeK5PentagonFace8_oriented t1 t2 t3 t4 t5).nativeShadow +
    (nativeK5NaturalitySquare0 t1 t2 t3 t4 t5).nativeShadow +
    (nativeK5NaturalitySquare1 t1 t2 t3 t4 t5).nativeShadow +
    (nativeK5NaturalitySquare2 t1 t2 t3 t4 t5).nativeShadow =
      (0 : KuuNativeF55Shadow) := by
  simp [nativeK5PentagonFace3_shadow, nativeK5PentagonFace4_shadow,
    nativeK5PentagonFace5_shadow, nativeK5PentagonFace6_shadow,
    nativeK5PentagonFace7_shadow, nativeK5PentagonFace8_shadow,
    nativeK5NaturalitySquare0_shadow, nativeK5NaturalitySquare1_shadow,
    nativeK5NaturalitySquare2_shadow,
    nativeK5PentagonFace5_oriented, nativeK5PentagonFace7_oriented,
    nativeK5PentagonFace8_oriented, NativeF55P92AssocComparison.nativeShadow]
  abel

#print axioms nativeK5PentagonFace3
#print axioms nativeK5PentagonFace4
#print axioms nativeK5PentagonFace5
#print axioms nativeK5PentagonFace6
#print axioms nativeK5PentagonFace7
#print axioms nativeK5PentagonFace8
#print axioms nativeK5NaturalitySquare0
#print axioms nativeK5NaturalitySquare1
#print axioms nativeK5NaturalitySquare2
#print axioms nativeK5PentagonFace3_shadow
#print axioms nativeK5PentagonFace4_shadow
#print axioms nativeK5PentagonFace5_shadow
#print axioms nativeK5PentagonFace6_shadow
#print axioms nativeK5PentagonFace7_shadow
#print axioms nativeK5PentagonFace8_shadow
#print axioms nativeK5NaturalitySquare0_shadow
#print axioms nativeK5NaturalitySquare1_shadow
#print axioms nativeK5NaturalitySquare2_shadow
#print axioms nativeK5NineGenuineFaceShadows_balance

end FiveNativeStages
end
end Kuu.F112.Physical
