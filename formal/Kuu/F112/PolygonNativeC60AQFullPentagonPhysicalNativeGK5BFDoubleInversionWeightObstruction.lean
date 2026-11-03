import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5BESignedOriginalGradeObstruction
import Mathlib.Tactic

/-!
F112-P94D3GK5BF — genuine north C60 DOUBLE-INVERSION obstruction:
even the JOINT GK5BB unsigned-count-one AND GK5BE signed-grade-one
necessary conditions are NOT sufficient for a selected P94A
local original F55 → recursive structural phi higher seam.

A genuinely new P92B Nat observer counts the original wrappers
with weight 2^k at inversion depth k: original=1, symm doubles,
refl/assocNaturality=0, trans/horizontal add, contexts preserve.
It is NOT obtained from the unsigned N or signed S alone.
We prove preservation through all 16 P93C and all 19 P94A
Type-valued four-cell constructors, with no missing cases.

At the exact SAME north C60 F54 source/target pentagon pair,
the source primitive p admits a reflexive local seam while the
different genuine original F55 source symm(symm p) does not:
N(phi)=1 and S(phi)=1 for BOTH, but depth-weight of phi is
1 versus 4; raw original(symm(symm p)) weighs 1. This is an
unconditional concrete counterexample to sufficiency of N=S=1,
even without reversing the dependent F54 route endpoints.

The joint N=S=1 test DOES descend as a genuine Prop-valued
predicate to the P77 source quotient, using GK5AJ and
GK5BB/GK5BE four-cell soundness. A stricter depth-weight gate
also descends. The primitive-positive and double-inversion-
negative P77 classes are rigorously different in one Hom fiber.
All P77 finite words from the double inverse stay negative.

We do not prove that N=1,S=1,W=1 is sufficient, that arbitrary
P94A witnesses normalize, or any global GK5AY seam, GK5BA kit,
original P89 faithfulness/nonfaithfulness or Gray reconstruction.

Strict 空 authority; independent Kuu→Qi; original F54
two-Nat, two-category, Blocks, original Type-valued F55
history retained. Append-only, root107, protected #1558
Draft/OPEN. Lean v4.30.0-rc2 / pinned mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
No new axioms, sorry, admit, native_decide or weakening.
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
variable {first : KuuNativeF45Tree p n m ma pa mb pb}
variable {last : KuuNativeF45Tree p n' m' ma pa mb pb}

/-- An independent inversion-DEPTH-weighted Nat invariant on
P92B Type-valued proof syntax. A raw original has weight 1;
each selected P92B.symm DOUBLES the weight (unlike GK5BB
unsigned and GK5BE sign). Vertical/horizontal pasting adds;
contexts preserve the weight. -/
def NativeF55P92AssocComparison.gk5bfInverseDepthWeight
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55P92AssocComparison p r s) : Nat := by
  induction f with
  | original old => exact 1
  | assocNaturality u v w => exact 0
  | refl r => exact 0
  | symm f ih => exact 2 * ih
  | trans f g ihf ihg => exact ihf + ihg
  | leftContext f later ih => exact ih
  | rightContext earlier f ih => exact ih
  | precompose prior f ih => exact ih
  | postcompose f suffix ih => exact ih

/-- Exact vertical 3-proof computation; using the named lemma
avoids unfolding the dependent recursor inside interchange. -/
theorem NativeF55P92AssocComparison.gk5bfTrans_weight
    {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55P92AssocComparison p r s)
    (g : NativeF55P92AssocComparison p s t) :
    (NativeF55P92AssocComparison.trans f g).gk5bfInverseDepthWeight =
      f.gk5bfInverseDepthWeight + g.gk5bfInverseDepthWeight := rfl

/-- Exact genuine P92B horizontal pasting: inverse-depth weight is additive
under the real dependent post/pre-context horizontal definition. -/
theorem NativeF55P92AssocComparison.gk5bfHorizontal_weight
    {n₁ n₁' m₁ m₁' n₂ n₂' m₂ m₂' : Nat}
    {p₀ p₁ p₂ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ : KuuNativeBlocks x y}
    {leftBefore : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁}
    {leftAfter : KuuNativeF45Tree p n₁' m₁' p₀ q₀ p₁ q₁}
    {rightBefore : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂}
    {rightAfter : KuuNativeF45Tree p n₂' m₂' p₁ q₁ p₂ q₂}
    {u u' : KuuNativeF45Tree.DepthRotationRoute p leftBefore leftAfter}
    {v v' : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter}
    (f : NativeF55P92AssocComparison p u u')
    (g : NativeF55P92AssocComparison p v v') :
    (f.horizontal g).gk5bfInverseDepthWeight =
      f.gk5bfInverseDepthWeight + g.gk5bfInverseDepthWeight := rfl

/-- ALL SIXTEEN genuine P93C four-cell constructors preserve
the inversion-depth Nat weight. The old P89 case is two
raw original wrappers of weight one regardless of source history.
Pasting and interchange preserve the additive grade. -/
theorem NativeF55P93AssocFourCell.gk5bfInverseDepthWeight_sound
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55P92AssocComparison p r s}
    (w : NativeF55P93AssocFourCell f g) :
    f.gk5bfInverseDepthWeight = g.gk5bfInverseDepthWeight := by
  induction w with
  | old w => rfl
  | refl f => rfl
  | symm w ih => exact ih.symm
  | trans fg gh ihfg ihgh => exact ihfg.trans ihgh
  | verticalLeftUnit f =>
      change (0 : Nat) + f.gk5bfInverseDepthWeight = f.gk5bfInverseDepthWeight
      exact zero_add _
  | verticalRightUnit f =>
      change f.gk5bfInverseDepthWeight + (0 : Nat) = f.gk5bfInverseDepthWeight
      exact add_zero _
  | verticalAssoc f g h =>
      change (f.gk5bfInverseDepthWeight + g.gk5bfInverseDepthWeight) +
        h.gk5bfInverseDepthWeight =
        f.gk5bfInverseDepthWeight + (g.gk5bfInverseDepthWeight + h.gk5bfInverseDepthWeight)
      exact add_assoc _ _ _
  | leftWhisker prior w ih =>
      exact congrArg (fun z : Nat => prior.gk5bfInverseDepthWeight + z) ih
  | rightWhisker w suffix ih =>
      exact congrArg (fun z : Nat => z + suffix.gk5bfInverseDepthWeight) ih
  | leftContext w later ih => exact ih
  | rightContext earlier w ih => exact ih
  | precompose prior w ih => exact ih
  | postcompose w suffix ih => exact ih
  | horizontalLeft w other ih =>
      simpa only [NativeF55P92AssocComparison.gk5bfHorizontal_weight] using
        congrArg (fun z : Nat => z + other.gk5bfInverseDepthWeight) ih
  | horizontalRight other w ih =>
      simpa only [NativeF55P92AssocComparison.gk5bfHorizontal_weight] using
        congrArg (fun z : Nat => other.gk5bfInverseDepthWeight + z) ih
  | interchange f₁ f₂ g₁ g₂ =>
      simp only [NativeF55P92AssocComparison.gk5bfHorizontal_weight,
        NativeF55P92AssocComparison.gk5bfTrans_weight]
      omega

/-- ALL NINETEEN chosen P94A constructors preserve the inverse-depth
weight, including horizontalUnit and both contextUnit additions. -/
theorem NativeF55P94UnitFourCell.gk5bfInverseDepthWeight_sound
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55P92AssocComparison p r s}
    (w : NativeF55P94UnitFourCell f g) :
    f.gk5bfInverseDepthWeight = g.gk5bfInverseDepthWeight := by
  induction w with
  | old w => exact w.gk5bfInverseDepthWeight_sound
  | refl f => rfl
  | symm w ih => exact ih.symm
  | trans fg gh ihfg ihgh => exact ihfg.trans ihgh
  | verticalLeftUnit f =>
      change (0 : Nat) + f.gk5bfInverseDepthWeight = f.gk5bfInverseDepthWeight
      exact zero_add _
  | verticalRightUnit f =>
      change f.gk5bfInverseDepthWeight + (0 : Nat) = f.gk5bfInverseDepthWeight
      exact add_zero _
  | verticalAssoc f g h =>
      change (f.gk5bfInverseDepthWeight + g.gk5bfInverseDepthWeight) +
        h.gk5bfInverseDepthWeight =
        f.gk5bfInverseDepthWeight + (g.gk5bfInverseDepthWeight + h.gk5bfInverseDepthWeight)
      exact add_assoc _ _ _
  | leftWhisker prior w ih =>
      exact congrArg (fun z : Nat => prior.gk5bfInverseDepthWeight + z) ih
  | rightWhisker w suffix ih =>
      exact congrArg (fun z : Nat => z + suffix.gk5bfInverseDepthWeight) ih
  | leftContext w later ih => exact ih
  | rightContext earlier w ih => exact ih
  | precompose prior w ih => exact ih
  | postcompose w suffix ih => exact ih
  | horizontalLeft w other ih =>
      simpa only [NativeF55P92AssocComparison.gk5bfHorizontal_weight] using
        congrArg (fun z : Nat => z + other.gk5bfInverseDepthWeight) ih
  | horizontalRight other w ih =>
      simpa only [NativeF55P92AssocComparison.gk5bfHorizontal_weight] using
        congrArg (fun z : Nat => other.gk5bfInverseDepthWeight + z) ih
  | interchange f₁ f₂ g₁ g₂ =>
      simp only [NativeF55P92AssocComparison.gk5bfHorizontal_weight,
        NativeF55P92AssocComparison.gk5bfTrans_weight]
      omega
  | horizontalUnit u v =>
      change (0 : Nat) + 0 = 0
      omega
  | leftContextUnit route later => rfl
  | rightContextUnit earlier route => rfl


/-- An original whole F55 raw wrapper has weight ONE even when
its internal source term itself contains several inversions. -/
theorem nativeGK5BFRawOriginal_weight_one
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    (NativeF55P92AssocComparison.original f).gk5bfInverseDepthWeight = 1 := rfl

/-- Chosen P92B proof inversion multiplies inverse-depth weight
by two; this is definitionally distinct from GK5BE signed negation. -/
theorem NativeF55P92AssocComparison.gk5bfSymm_weight
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55P92AssocComparison p r s) :
    (NativeF55P92AssocComparison.symm f).gk5bfInverseDepthWeight =
      2 * f.gk5bfInverseDepthWeight := rfl

/-- Original F55 inversion is structural under GK5AI recursive
phi, with all original dependent source/target indices retained. -/
theorem nativeGK5BFPhiSymm_weight
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    (nativeGK5AIOriginalToP92Structural (.symm f)).gk5bfInverseDepthWeight =
      2 * (nativeGK5AIOriginalToP92Structural f).gk5bfInverseDepthWeight := rfl

/-- Every actual local direct four-cell seam imposes three
independent necessary scalar gates at its structural phi end:
unsigned original count one, signed grade one, and inversion
depth-weight one. None is asserted sufficient. -/
theorem nativeGK5BFLocalSeam_three_necessary
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s)
    (bridge : nativeGK5AZSeamAt f) :
    (nativeGK5AIOriginalToP92Structural f).gk5bbOriginalCount = 1 ∧
    (nativeGK5AIOriginalToP92Structural f).gk5beSignedCount = 1 ∧
    (nativeGK5AIOriginalToP92Structural f).gk5bfInverseDepthWeight = 1 := by
  obtain ⟨hN, hS⟩ := nativeGK5BENecessary_unsigned_and_signed f bridge
  have hW := bridge.gk5bfInverseDepthWeight_sound
  change (1 : Nat) = _ at hW
  exact ⟨hN, hS, hW.symm⟩

/-- A chosen phi weight other than one is an explicit,
unconditional obstruction to the genuine P94A direct local seam. -/
theorem nativeGK5BFNoSeam_if_weight_ne_one
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s)
    (hole : (nativeGK5AIOriginalToP92Structural f).gk5bfInverseDepthWeight ≠ 1) :
    ¬ Nonempty (nativeGK5AZSeamAt f) := by
  rintro ⟨w⟩
  exact hole (nativeGK5BFLocalSeam_three_necessary f w).2.2

/-- Original F55 twofold inversion is a real, non-primitive
source proof term in the very SAME source/target north F54
pentagon slot as the single primitive source p. -/
def nativeGK5BFNorthDoubleInverse :
    KuuNativeF45Tree.DepthRotationRoute.PresentedCell
      (.pentagon .north)
      northNativeF45PentagonLong northNativeF45PentagonShort :=
  .symm (.symm nativeGK5AGNorthOriginalCell)

/-- The selected phi of the double inverse still passes BOTH
previous numerical gates N=1 AND S=1, but has weight FOUR. -/
theorem nativeGK5BFNorthDoubleInverse_phi_grades :
    (nativeGK5AIOriginalToP92Structural
      nativeGK5BFNorthDoubleInverse).gk5bbOriginalCount = 1 ∧
    (nativeGK5AIOriginalToP92Structural
      nativeGK5BFNorthDoubleInverse).gk5beSignedCount = 1 ∧
    (nativeGK5AIOriginalToP92Structural
      nativeGK5BFNorthDoubleInverse).gk5bfInverseDepthWeight = 4 :=
  ⟨rfl, rfl, rfl⟩

/-- Original whole wrapper remains weight ONE, whereas recursive
phi is 4, despite the simultaneous N=S=1 conditions. -/
theorem nativeGK5BFNorthDoubleInverse_raw_vs_phi_weight :
    (NativeF55P92AssocComparison.original
      nativeGK5BFNorthDoubleInverse).gk5bfInverseDepthWeight = 1 ∧
    (nativeGK5AIOriginalToP92Structural
      nativeGK5BFNorthDoubleInverse).gk5bfInverseDepthWeight = 4 :=
  ⟨rfl, rfl⟩

/-- The full P94A four-cell proof is impossible at the double
inverse even though the old two numerical conditions both pass. -/
theorem nativeGK5BFNorthDoubleInverse_no_seam :
    ¬ Nonempty (nativeGK5AZSeamAt nativeGK5BFNorthDoubleInverse) := by
  apply nativeGK5BFNoSeam_if_weight_ne_one
  change (4 : Nat) ≠ 1
  omega

/-- Genuine SAME-FIBER strict counterexample:
the original north primitive has a true reflexive seam,
while its original double inversion passes N=S=1 and has NO
selected direct seam. Reverse route typing is not used here. -/
theorem nativeGK5BFNorthSameFiber_joint_gate_not_sufficient :
    (nativeGK5AIOriginalToP92Structural
      nativeGK5AGNorthOriginalCell).gk5bbOriginalCount = 1 ∧
    (nativeGK5AIOriginalToP92Structural
      nativeGK5AGNorthOriginalCell).gk5beSignedCount = 1 ∧
    Nonempty (nativeGK5AZSeamAt nativeGK5AGNorthOriginalCell) ∧
    (nativeGK5AIOriginalToP92Structural
      nativeGK5BFNorthDoubleInverse).gk5bbOriginalCount = 1 ∧
    (nativeGK5AIOriginalToP92Structural
      nativeGK5BFNorthDoubleInverse).gk5beSignedCount = 1 ∧
    ¬ Nonempty (nativeGK5AZSeamAt nativeGK5BFNorthDoubleInverse) :=
  ⟨rfl, rfl, ⟨.refl _⟩, rfl, rfl,
    nativeGK5BFNorthDoubleInverse_no_seam⟩

/-- A two-component NECESSARY gate on genuine original F55
source syntax, not a sufficient decision procedure for seams. -/
def nativeGK5BFCountSignedGate
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) : Prop :=
  (nativeGK5AIOriginalToP92Structural f).gk5bbOriginalCount = 1 ∧
  (nativeGK5AIOriginalToP92Structural f).gk5beSignedCount = 1

/-- Any genuine P77 source four-cell transports BOTH N and S
at structural phi endpoints via GK5AJ's REAL P93C witness. -/
theorem nativeGK5BFCountSignedGate_iff_P77
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
    (w : NativeF55RawVerticalFourCell first last f g) :
    nativeGK5BFCountSignedGate f ↔
      nativeGK5BFCountSignedGate g := by
  have hN := (nativeGK5AJOriginalFourToP93 first last w).gk5bbOriginalCount_sound
  have hS := (nativeGK5AJOriginalFourToP93 first last w).gk5beSignedCount_sound
  constructor
  · rintro ⟨hn, hs⟩
    exact ⟨hN.symm.trans hn, hS.symm.trans hs⟩
  · rintro ⟨hn, hs⟩
    exact ⟨hN.trans hn, hS.trans hs⟩

/-- TRUE source-quotient descent of the weaker numerical N=S=1
gate using P77 evidence rather than equality of raw F55 terms. -/
def nativeGK5BFCountSignedOnP77Class
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (r s : KuuNativeF45Tree.DepthRotationRoute p first last) :
    NativeF55RawVerticalFourClasses first last r s → Prop :=
  _root_.Quotient.lift
    (fun f => nativeGK5BFCountSignedGate f)
    (by
      intro f g related
      rcases related with ⟨w⟩
      exact propext (nativeGK5BFCountSignedGate_iff_P77 w))

/-- One additional inversion-depth weight gate; the stronger
triple numerical test will also descend, but is not sufficient. -/
def nativeGK5BFWeightGate
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) : Prop :=
  (nativeGK5AIOriginalToP92Structural f).gk5bfInverseDepthWeight = 1

/-- Weight equality on the selected structural phi endpoints
follows from an ACTUAL original P77 four-cell. -/
theorem nativeGK5BFWeightGate_iff_P77
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
    (w : NativeF55RawVerticalFourCell first last f g) :
    nativeGK5BFWeightGate f ↔ nativeGK5BFWeightGate g := by
  have hW := (nativeGK5AJOriginalFourToP93 first last w).gk5bfInverseDepthWeight_sound
  constructor
  · intro hw
    exact hW.symm.trans hw
  · intro hw
    exact hW.trans hw

/-- TRUE quotient descent of ALL THREE local numerical necessary
conditions. This statement intentionally has NO sufficiency arrow. -/
def nativeGK5BFThreeGatesOnP77Class
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (r s : KuuNativeF45Tree.DepthRotationRoute p first last) :
    NativeF55RawVerticalFourClasses first last r s → Prop :=
  _root_.Quotient.lift
    (fun f => nativeGK5BFCountSignedGate f ∧ nativeGK5BFWeightGate f)
    (by
      intro f g related
      rcases related with ⟨w⟩
      exact propext
        (and_congr (nativeGK5BFCountSignedGate_iff_P77 w)
          (nativeGK5BFWeightGate_iff_P77 w)))

/-- The weaker numerical quotient gate is in fact TRUE at
both original north proof classes, whereas local seam exists
at only the original primitive class in this same Hom fiber. -/
private def nativeGK5BFNorthFirst :=
  KuuNativeF45Tree.pentagon0 northNativeF45FirstStage
    northNativeF45SecondStage northNativeF45ThirdStage
    northNativeF45FourthStage

private def nativeGK5BFNorthLast :=
  KuuNativeF45Tree.pentagon3 northNativeF45FirstStage
    northNativeF45SecondStage northNativeF45ThirdStage
    northNativeF45FourthStage

theorem nativeGK5BFNorthSameFiber_quotient_gate_not_sufficient :
    nativeGK5BFCountSignedOnP77Class
      nativeGK5BFNorthFirst nativeGK5BFNorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort
      (nativeF55RawVerticalFourClass
        nativeGK5BFNorthFirst nativeGK5BFNorthLast
        nativeGK5AGNorthOriginalCell) ∧
    nativeGK5BFCountSignedOnP77Class
      nativeGK5BFNorthFirst nativeGK5BFNorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort
      (nativeF55RawVerticalFourClass
        nativeGK5BFNorthFirst nativeGK5BFNorthLast
        nativeGK5BFNorthDoubleInverse) ∧
    nativeGK5BDSeamExistsOnP77Class
      nativeGK5BFNorthFirst nativeGK5BFNorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort
      (nativeF55RawVerticalFourClass
        nativeGK5BFNorthFirst nativeGK5BFNorthLast
        nativeGK5AGNorthOriginalCell) ∧
    ¬ nativeGK5BDSeamExistsOnP77Class
      nativeGK5BFNorthFirst nativeGK5BFNorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort
      (nativeF55RawVerticalFourClass
        nativeGK5BFNorthFirst nativeGK5BFNorthLast
        nativeGK5BFNorthDoubleInverse) :=
  ⟨⟨rfl, rfl⟩, ⟨rfl, rfl⟩,
    ⟨.refl _⟩, nativeGK5BFNorthDoubleInverse_no_seam⟩

/-- These two full SOURCE-P77 classes are PROVABLY distinct,
even though their GK5BB/GK5BE numerical observations agree.
The stronger weight is one versus four after phi translation. -/
theorem nativeGK5BFNorthPrimitive_ne_double_inverse_P77_class :
    nativeF55RawVerticalFourClass
      nativeGK5BFNorthFirst nativeGK5BFNorthLast
      nativeGK5AGNorthOriginalCell ≠
    nativeF55RawVerticalFourClass
      nativeGK5BFNorthFirst nativeGK5BFNorthLast
      nativeGK5BFNorthDoubleInverse := by
  intro heq
  have hp77 : Nonempty (NativeF55RawVerticalFourCell
      nativeGK5BFNorthFirst nativeGK5BFNorthLast
      nativeGK5AGNorthOriginalCell nativeGK5BFNorthDoubleInverse) :=
    (nativeF55RawVerticalFourClass_eq_iff
      nativeGK5BFNorthFirst nativeGK5BFNorthLast
      nativeGK5AGNorthOriginalCell nativeGK5BFNorthDoubleInverse).mp heq
  rcases hp77 with ⟨w⟩
  have hW := (nativeGK5AJOriginalFourToP93
    nativeGK5BFNorthFirst nativeGK5BFNorthLast w).gk5bfInverseDepthWeight_sound
  change (1 : Nat) = 4 at hW
  omega

/-- Every genuine finite P77 source word starting at the
double inverse remains seam-NEGATIVE by proven four-cell
transport, not by a numerical shadow quotient. -/
theorem nativeGK5BFNorthDoubleInverseP77Word_no_seam
    {target : KuuNativeF45Tree.DepthRotationRoute.PresentedCell
      (.pentagon .north)
      northNativeF45PentagonLong northNativeF45PentagonShort}
    (w : NativeGK5BDP77Word
      nativeGK5BFNorthFirst nativeGK5BFNorthLast
      nativeGK5BFNorthDoubleInverse target) :
    ¬ Nonempty (nativeGK5AZSeamAt target) := by
  rintro ⟨bridge⟩
  exact nativeGK5BFNorthDoubleInverse_no_seam
    ⟨nativeGK5BCSeam_transport_P77 w.toP77 bridge⟩

#print axioms NativeF55P92AssocComparison.gk5bfInverseDepthWeight
#print axioms NativeF55P92AssocComparison.gk5bfTrans_weight
#print axioms NativeF55P92AssocComparison.gk5bfHorizontal_weight
#print axioms NativeF55P93AssocFourCell.gk5bfInverseDepthWeight_sound
#print axioms NativeF55P94UnitFourCell.gk5bfInverseDepthWeight_sound
#print axioms nativeGK5BFRawOriginal_weight_one
#print axioms NativeF55P92AssocComparison.gk5bfSymm_weight
#print axioms nativeGK5BFPhiSymm_weight
#print axioms nativeGK5BFLocalSeam_three_necessary
#print axioms nativeGK5BFNoSeam_if_weight_ne_one
#print axioms nativeGK5BFNorthDoubleInverse
#print axioms nativeGK5BFNorthDoubleInverse_phi_grades
#print axioms nativeGK5BFNorthDoubleInverse_raw_vs_phi_weight
#print axioms nativeGK5BFNorthDoubleInverse_no_seam
#print axioms nativeGK5BFNorthSameFiber_joint_gate_not_sufficient
#print axioms nativeGK5BFCountSignedGate
#print axioms nativeGK5BFCountSignedGate_iff_P77
#print axioms nativeGK5BFCountSignedOnP77Class
#print axioms nativeGK5BFWeightGate
#print axioms nativeGK5BFWeightGate_iff_P77
#print axioms nativeGK5BFThreeGatesOnP77Class
#print axioms nativeGK5BFNorthSameFiber_quotient_gate_not_sufficient
#print axioms nativeGK5BFNorthPrimitive_ne_double_inverse_P77_class
#print axioms nativeGK5BFNorthDoubleInverseP77Word_no_seam

end
end Kuu.F112.Physical
