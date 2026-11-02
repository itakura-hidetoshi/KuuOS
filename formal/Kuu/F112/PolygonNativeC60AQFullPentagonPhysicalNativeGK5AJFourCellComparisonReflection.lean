import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5AIStructuralF55WholeCellBridge
import Kuu.F112.PolygonNativeF55RawVerticalFourCellP77
import Kuu.F112.PolygonNativeF55P93AssocFourCellCoherence
import Mathlib.Tactic

/-!
F112-P94D3GK5AJ — genuine original F55 vertical 4-cell structural
preservation, typed P93 four-cell descent, exact reflection gate,
and the independent C60 pentagon/square higher-history interface.

GK5AI supplied the total structural map from ALL NINE original
F55 Type-valued 3-cell constructors to the chosen P92B 3-source.
Here we verify this map against every one of the EIGHT ACTUAL
original P77 vertical 4-cell constructors, translating witnesses
into the corresponding P93C Type-valued four-cells:
refl, symm, trans, left/right whiskering, left/right units, assoc.

The map also commutes DEFINITIONALLY with the actual horizontal
F55 pasting derived from typed left/right contexts and pre/post
composition; it preserves the full signed pentagon/square charge
and nontrivial odd ZMod2 exchange phase.

On actual P77/P93 4-cell quotient objects we construct a genuine
quotient-factor map and the necessary and SUFFICIENT condition for
its injectivity: exactly the reflection of each ACTUAL P93C 4-cell
between two structurally translated original cells back to an
ACTUAL P77 source 4-cell. We DO NOT assume that reflection,
unrestricted higher coherence, or a global physical/whole filler.

The genuine original north-C60 F55 pentagon proof and its unit-
postcomposed proof remain distinct as Type-valued 3-cell terms,
while true P77 and selected P93 4-cell witnesses identify their
4-cell classes. The C60 pentagon charge and odd north hexagon
square phase are preserved without using a merely numerical
equality to create any higher cell.

Independent Kuu only, append-only/tighten-only, same-root107,
strict 空 authority preserved. Qi can import this file; Kuu never
imports Qi. No old KUOS F54 equivalence, Gray, new axioms, sorry,
native_decide, or unrestricted descent.
Pinned Lean v4.30.0-rc2 / mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
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
variable {n n' m m' : Nat}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}
variable (first : KuuNativeF45Tree p n m ma pa mb pb)
variable (last : KuuNativeF45Tree p n' m' ma pa mb pb)

/-- ACTUAL P77 source 4-cell witnesses are preserved by the
GK5AI structural nine-constructor source-to-P92B map, with a
constructed P93C 4-cell rather than a shadow equality. -/
def nativeGK5AJOriginalFourToP93
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
    (w : NativeF55RawVerticalFourCell first last f g) :
    NativeF55P93AssocFourCell
      (nativeGK5AIOriginalToP92Structural f)
      (nativeGK5AIOriginalToP92Structural g) := by
  induction w with
  | refl raw => exact .refl _
  | symm w ih => exact .symm ih
  | trans fg gh ihfg ihgh => exact .trans ihfg ihgh
  | leftWhisker prior w ih =>
      exact .leftWhisker (nativeGK5AIOriginalToP92Structural prior) ih
  | rightWhisker w suffix ih =>
      exact .rightWhisker ih (nativeGK5AIOriginalToP92Structural suffix)
  | leftUnit raw =>
      exact .verticalLeftUnit (nativeGK5AIOriginalToP92Structural raw)
  | rightUnit raw =>
      exact .verticalRightUnit (nativeGK5AIOriginalToP92Structural raw)
  | assoc f g h =>
      exact .verticalAssoc
        (nativeGK5AIOriginalToP92Structural f)
        (nativeGK5AIOriginalToP92Structural g)
        (nativeGK5AIOriginalToP92Structural h)

/-- The original F55 signed pentagon, disjoint-square and odd
ZMod2 phase are preserved for ALL nine source 3-cell constructors,
not only the two selected primitive generator examples. -/
theorem nativeGK5AJStructuralShadow
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    (nativeGK5AIOriginalToP92Structural f).nativeShadow =
      f.nativeShadow := by
  induction f with
  | ident route => rfl
  | pentagon t₁ t₂ t₃ t₄ => rfl
  | disjointSquare left right => rfl
  | symm f ih =>
      change -(nativeGK5AIOriginalToP92Structural f).nativeShadow =
        -f.nativeShadow
      exact congrArg (fun z : KuuNativeF55Shadow => -z) ih
  | trans f g ihf ihg =>
      change (nativeGK5AIOriginalToP92Structural f).nativeShadow +
        (nativeGK5AIOriginalToP92Structural g).nativeShadow =
        f.nativeShadow + g.nativeShadow
      exact congrArg₂ (fun u v : KuuNativeF55Shadow => u + v) ihf ihg
  | leftContext f later ih => exact ih
  | rightContext earlier f ih => exact ih
  | precompose prior f ih => exact ih
  | postcompose f suffix ih => exact ih

/-- The GK5AI structural map preserves the true original
horizontal THREE-cell pasting, defined from typed F54 left/right
contexts, not from a freely postulated interchange. -/
theorem nativeGK5AJStructuralHorizontal
    {k k' l l' : Nat}
    {mc : KuuNativeBlocks a b}
    {pc : KuuNativeBlocks x y}
    {leftBefore : KuuNativeF45Tree p n m ma pa mb pb}
    {leftAfter : KuuNativeF45Tree p n' m' ma pa mb pb}
    {rightBefore : KuuNativeF45Tree p k l mb pb mc pc}
    {rightAfter : KuuNativeF45Tree p k' l' mb pb mc pc}
    {u u' : KuuNativeF45Tree.DepthRotationRoute p leftBefore leftAfter}
    {v v' : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter}
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u u')
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p v v') :
    nativeGK5AIOriginalToP92Structural (f.horizontal g) =
      (nativeGK5AIOriginalToP92Structural f).horizontal
        (nativeGK5AIOriginalToP92Structural g) := rfl

/-- From the ACTUAL original P77 4-cell quotient to the
chosen P93C 4-cell quotient, via the structural F55→P92B
3-cell map. Well-definedness comes from the 4-cell induction,
not from an arbitrary shadow or free Eq assumption. -/
def nativeGK5AJFourClassMap
    (r s : KuuNativeF45Tree.DepthRotationRoute p first last) :
    NativeF55RawVerticalFourClasses first last r s →
      NativeF55P93AssocFourClasses first last r s :=
  _root_.Quotient.lift
    (fun f => nativeF55P93AssocFourClass first last
      (nativeGK5AIOriginalToP92Structural f))
    (by
      intro f g h
      rcases h with ⟨w⟩
      exact _root_.Quotient.sound
        ⟨nativeGK5AJOriginalFourToP93 first last w⟩)

/-- Exact representative computation of the genuine 4-cell
quotient map, without introducing an arbitrary 4-cell relation. -/
theorem nativeGK5AJFourClassMap_spec
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    nativeGK5AJFourClassMap first last r s
      (nativeF55RawVerticalFourClass first last f) =
    nativeF55P93AssocFourClass first last
      (nativeGK5AIOriginalToP92Structural f) := rfl

/-- The precise necessary-and-sufficient compatibility/reflection
gate for faithfulness at the chosen P77/P93 4-cell quotient.
No reflection is assumed: a false implication would inappropriately
promote the separately ADJOINED P93 relations to original P77. -/
theorem nativeGK5AJFourClassInjective_iff_reflect
    (r s : KuuNativeF45Tree.DepthRotationRoute p first last) :
    Function.Injective (nativeGK5AJFourClassMap first last r s) ↔
      (∀ f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s,
        Nonempty (NativeF55P93AssocFourCell
          (nativeGK5AIOriginalToP92Structural f)
          (nativeGK5AIOriginalToP92Structural g)) →
        Nonempty (NativeF55RawVerticalFourCell first last f g)) := by
  constructor
  · intro hinj f g hw
    have htarget :
        nativeF55P93AssocFourClass first last
            (nativeGK5AIOriginalToP92Structural f) =
          nativeF55P93AssocFourClass first last
            (nativeGK5AIOriginalToP92Structural g) :=
      (nativeF55P93AssocFourClass_eq_iff first last
        (nativeGK5AIOriginalToP92Structural f)
        (nativeGK5AIOriginalToP92Structural g)).2 hw
    have hsource :
        nativeF55RawVerticalFourClass first last f =
          nativeF55RawVerticalFourClass first last g := by
      apply hinj
      exact htarget
    exact (nativeF55RawVerticalFourClass_eq_iff first last f g).1 hsource
  · intro href x y
    refine _root_.Quotient.inductionOn₂ x y ?_
    intro f g heq
    apply (nativeF55RawVerticalFourClass_eq_iff first last f g).2
    apply href f g
    exact (nativeF55P93AssocFourClass_eq_iff first last
      (nativeGK5AIOriginalToP92Structural f)
      (nativeGK5AIOriginalToP92Structural g)).1 heq

/-- The full chosen F55 signed/odd-phase shadow on the P77
source 4-cell quotient COMMUTES with passage to the selected
P93C target 4-cell quotient, an actual proved descent square. -/
theorem nativeGK5AJFourClassShadow_commutes
    (r s : KuuNativeF45Tree.DepthRotationRoute p first last)
    (q : NativeF55RawVerticalFourClasses first last r s) :
    nativeF55P93AssocFourToShadow first last r s
        (nativeGK5AJFourClassMap first last r s q) =
      nativeF55RawVerticalFourToShadow first last r s q := by
  refine _root_.Quotient.inductionOn q ?_
  intro f
  exact nativeGK5AJStructuralShadow first last f

/-- The REAL north-C60 four-stage F45 original depth endpoints. -/
private def nativeGK5AJNorthFirst :=
  KuuNativeF45Tree.pentagon0 northNativeF45FirstStage
    northNativeF45SecondStage northNativeF45ThirdStage
    northNativeF45FourthStage

private def nativeGK5AJNorthLast :=
  KuuNativeF45Tree.pentagon3 northNativeF45FirstStage
    northNativeF45SecondStage northNativeF45ThirdStage
    northNativeF45FourthStage

/-- Real original F55 right-unit 4-cell, between the two DIFFERENT
original F55 3-proofs of the SAME north-C60 pentagon boundary. -/
def nativeGK5AJNorthOriginalRightUnitFour :
    NativeF55RawVerticalFourCell
      nativeGK5AJNorthFirst nativeGK5AJNorthLast
      nativeGK5AINorthPentagonWithIdentity
      nativeGK5AGNorthOriginalCell :=
  .rightUnit nativeGK5AGNorthOriginalCell

/-- The original source right-unit FOUR cell is transported into
a genuine P93C four-cell with the structurally translated endpoints.
This does NOT identify the source THREE-cell proof terms. -/
def nativeGK5AJNorthMappedRightUnitFour :
    NativeF55P93AssocFourCell
      (nativeGK5AIOriginalToP92Structural
        nativeGK5AINorthPentagonWithIdentity)
      (nativeGK5AIOriginalToP92Structural
        nativeGK5AGNorthOriginalCell) :=
  nativeGK5AJOriginalFourToP93
    nativeGK5AJNorthFirst nativeGK5AJNorthLast
      nativeGK5AJNorthOriginalRightUnitFour

/-- The two distinct original F55 Type-valued proofs are
four-cell-related in BOTH their original and chosen presentations.
The existence of these Type-valued four-cells, not a claimed
raw-proof equality, justifies the quotient-class equalities. -/
theorem nativeGK5AJNorthOriginalAndSelectedFourClasses_equal :
    (nativeF55RawVerticalFourClass nativeGK5AJNorthFirst
        nativeGK5AJNorthLast nativeGK5AINorthPentagonWithIdentity =
      nativeF55RawVerticalFourClass nativeGK5AJNorthFirst
        nativeGK5AJNorthLast nativeGK5AGNorthOriginalCell) ∧
    (nativeF55P93AssocFourClass nativeGK5AJNorthFirst
        nativeGK5AJNorthLast
        (nativeGK5AIOriginalToP92Structural
          nativeGK5AINorthPentagonWithIdentity) =
      nativeF55P93AssocFourClass nativeGK5AJNorthFirst
        nativeGK5AJNorthLast
        (nativeGK5AIOriginalToP92Structural
          nativeGK5AGNorthOriginalCell)) := by
  constructor
  · exact _root_.Quotient.sound
      ⟨nativeGK5AJNorthOriginalRightUnitFour⟩
  · exact _root_.Quotient.sound
      ⟨nativeGK5AJNorthMappedRightUnitFour⟩

/-- Signed native C60 pentagon charge survives structural translation. -/
theorem nativeGK5AJNorthPentagonCharge_preserved :
    (nativeGK5AIOriginalToP92Structural
      nativeGK5AGNorthOriginalCell).nativeShadow =
        (((1 : Int), (0 : Int)), (0 : ZMod 2)) := by
  rw [nativeGK5AJStructuralShadow]
  exact northNativeF55PentagonCell_shadow

/-- The actual north C60 top HEXAGON original F55 disjoint square
retains its NONZERO odd ZMod2 exchange phase in the new P92B
presentation: no P92B shadow substitution collapses this charge. -/
theorem nativeGK5AJNorthHexagonOddPhase_preserved :
    (nativeGK5AIOriginalToP92Structural
      northHexagonNativeF55SquareCell).nativeShadow.2 =
        (1 : ZMod 2) := by
  rw [nativeGK5AJStructuralShadow, northHexagonNativeF55SquareCell_shadow]

#print axioms nativeGK5AJOriginalFourToP93
#print axioms nativeGK5AJStructuralShadow
#print axioms nativeGK5AJStructuralHorizontal
#print axioms nativeGK5AJFourClassMap
#print axioms nativeGK5AJFourClassMap_spec
#print axioms nativeGK5AJFourClassInjective_iff_reflect
#print axioms nativeGK5AJFourClassShadow_commutes
#print axioms nativeGK5AJNorthOriginalRightUnitFour
#print axioms nativeGK5AJNorthMappedRightUnitFour
#print axioms nativeGK5AJNorthOriginalAndSelectedFourClasses_equal
#print axioms nativeGK5AJNorthPentagonCharge_preserved
#print axioms nativeGK5AJNorthHexagonOddPhase_preserved

end
end Kuu.F112.Physical
