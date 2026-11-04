import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5CFOriginalPhiTypedPentagonComparison
import Mathlib.Tactic

/-!
F112-P94D3GK5CG — actual original F55 P77 four-proof associator charge
and obstruction to a conservative source-TYPE pentagonator five-cell.

GK5CF constructs the five ACTUAL original F55 3-proof parenthesizations
with five ACTUAL P77 four-cells, and the upper/three-edge and lower/two-edge
parallel P77 four-proof terms. This file does NOT conflate equality of
the numerical GK5CE/GK5CF RingHoms or original P77 four-cell existence
with an equality or higher five-cell between these parallel four-proofs.

We define an independent signed INTEGER observer on the original
TYPE-valued P77 four-proof constructors:
  assoc=+1, refl/unit=0, symm=negation, trans=addition,
  left/right whiskering preserve the count.
For every genuine composable original F55 four-tuple the upper P77 path
has charge THREE, the lower P77 path charge TWO. Thus the ORIGINAL
free four-proof terms are unequal, with an exact +1 discrepancy.
No shadow or numeric polynomial proxy is used for this proof.

Specify a separate CONSERVATIVE Type-valued source five-cell grammar:
identity, inverse, vertical five-cell pasting, four-cell vertical
congruence/association/units/inverse cancellation, whisker congruence,
and inverse respect. Every constructor preserves the integer charge.
The true original source pentagon paths are consequently NOT connected
by any conservative five-cell, for every dependent F54 source slot.

A second, EXPLICITLY DIFFERENT free presentation can *adjoin*
a new typed pentagonator five-cell generator with exactly those endpoints.
It cannot retract into the conservative grammar, and the old integer
observer cannot be preserved by every generator of that extension.
This added constructor is a NEW presentation, not a retroactive proof
of an original P77/P94A higher five-cell, not a numerical descent,
and not the separate physical K5 pentagonator.

The numerical RingHom pentagon still holds in the presence of the
structural conservative-five-cell obstruction. No unconditional source
original→phi seam, proof equality in P94A, or Gray is asserted.

Strict 空 / independent Kuu→Qi. Original F54 2 Nat, two categories,
Blocks, and original F55 Type history untouched. Append-only, root107,
pinned Lean v4.30.0-rc2 / mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Protected PR #1558 Draft/open/unmerged; no sorry, admit, axiom,
native_decide, original P77/P94A grammar rewrite or proof weakening.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {p : Polygon} {a b : D} {x y : E}
variable {n n' m m' : Nat}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}
variable {first : KuuNativeF45Tree p n m ma pa mb pb}
variable {last : KuuNativeF45Tree p n' m' ma pa mb pb}

/-- Signed integer count of original P77 associator FOUR-PROOF
occurrences, retaining the full dependent Type-valued evidence.
Unlike GK5BB's original-P92B-wrapper count, this observer is on
the *original P77 four-cell proof grammar itself*. -/
def NativeF55RawVerticalFourCell.gk5cgAssocCharge
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
    (w : NativeF55RawVerticalFourCell first last f g) : ℤ := by
  induction w with
  | refl raw => exact 0
  | symm w ih => exact -ih
  | trans ab bc ihab ihbc => exact ihab + ihbc
  | leftWhisker prior w ih => exact ih
  | rightWhisker w suffix ih => exact ih
  | leftUnit raw => exact 0
  | rightUnit raw => exact 0
  | assoc f g h => exact 1

/-- Original P77 inverse reverses the associator charge. -/
theorem nativeGK5CGAssocCharge_symm
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
    (w : NativeF55RawVerticalFourCell first last f g) :
    (NativeF55RawVerticalFourCell.symm w).gk5cgAssocCharge =
      -w.gk5cgAssocCharge := rfl

/-- Original P77 four-proof vertical pasting adds actual charge. -/
theorem nativeGK5CGAssocCharge_trans
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
    (ab : NativeF55RawVerticalFourCell first last f g)
    (bc : NativeF55RawVerticalFourCell first last g h) :
    (NativeF55RawVerticalFourCell.trans ab bc).gk5cgAssocCharge =
      ab.gk5cgAssocCharge + bc.gk5cgAssocCharge := rfl

/-- Original F55 left-whiskering keeps the signed P77 four-charge. -/
theorem nativeGK5CGAssocCharge_leftWhisker
    {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
    (prior : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s)
    {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p s t}
    (w : NativeF55RawVerticalFourCell first last f g) :
    (NativeF55RawVerticalFourCell.leftWhisker prior w).gk5cgAssocCharge =
      w.gk5cgAssocCharge := rfl

/-- Original F55 right-whiskering keeps the signed P77 four-charge. -/
theorem nativeGK5CGAssocCharge_rightWhisker
    {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
    (w : NativeF55RawVerticalFourCell first last f g)
    (suffix : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p s t) :
    (NativeF55RawVerticalFourCell.rightWhisker w suffix).gk5cgAssocCharge =
      w.gk5cgAssocCharge := rfl

variable {r₀ r₁ r₂ r₃ r₄ :
  KuuNativeF45Tree.DepthRotationRoute p first last}

/-- The genuine original UPPER three-edge F55 source pentagon
contains EXACTLY three oriented P77 associator generators. -/
theorem nativeGK5CGUpperPath_assocCharge_three
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₀ r₁)
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₁ r₂)
    (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₂ r₃)
    (k : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₃ r₄) :
    (nativeGK5CFP77UpperPath f g h k).gk5cgAssocCharge = 3 := by
  norm_num [nativeGK5CFP77UpperPath, nativeGK5CFP77Edge01,
    nativeGK5CFP77Edge12, nativeGK5CFP77Edge23,
    NativeF55RawVerticalFourCell.gk5cgAssocCharge]

/-- The genuine original LOWER two-edge F55 source pentagon
contains EXACTLY two oriented P77 associator generators. -/
theorem nativeGK5CGLowerPath_assocCharge_two
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₀ r₁)
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₁ r₂)
    (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₂ r₃)
    (k : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₃ r₄) :
    (nativeGK5CFP77LowerPath f g h k).gk5cgAssocCharge = 2 := by
  norm_num [nativeGK5CFP77LowerPath, nativeGK5CFP77Edge40,
    nativeGK5CFP77Edge34,
    NativeF55RawVerticalFourCell.gk5cgAssocCharge]

/-- Exact charge discrepancy +1 for the two ACTUAL
parallel Type-valued P77 four-proof paths. -/
theorem nativeGK5CGOriginalPentagon_charge_defect_one
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₀ r₁)
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₁ r₂)
    (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₂ r₃)
    (k : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₃ r₄) :
    (nativeGK5CFP77UpperPath f g h k).gk5cgAssocCharge -
      (nativeGK5CFP77LowerPath f g h k).gk5cgAssocCharge = 1 := by
  rw [nativeGK5CGUpperPath_assocCharge_three,
    nativeGK5CGLowerPath_assocCharge_two]
  norm_num

/-- Source proof equality is impossible; its obstruction is
a *four-proof-constructor* charge, NOT a P92B original wrapper,
integer-polynomial substitution value, or actual higher five-cell. -/
theorem nativeGK5CGOriginalUpper_ne_lower
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₀ r₁)
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₁ r₂)
    (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₂ r₃)
    (k : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₃ r₄) :
    nativeGK5CFP77UpperPath f g h k ≠
      nativeGK5CFP77LowerPath f g h k := by
  intro heq
  have hc := congrArg
    (fun w => NativeF55RawVerticalFourCell.gk5cgAssocCharge w) heq
  change (nativeGK5CFP77UpperPath f g h k).gk5cgAssocCharge =
    (nativeGK5CFP77LowerPath f g h k).gk5cgAssocCharge at hc
  rw [nativeGK5CGUpperPath_assocCharge_three,
    nativeGK5CGLowerPath_assocCharge_two] at hc
  norm_num at hc

/-- A CONSERVATIVE, separately presented Type-valued 5-cell
language on the ACTUAL original P77 four-proof syntax. All
generators are ordinary groupoid/whiskering coherences for
four-cell pasting; NO pentagonator generator is smuggled in. -/
inductive NativeGK5CGConservativeFiveCell
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :
    ∀ {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s},
      NativeF55RawVerticalFourCell first last f g →
      NativeF55RawVerticalFourCell first last f g →
      Type (max (max uD uE) (max vD vE)) where
  | refl
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
      (w : NativeF55RawVerticalFourCell first last f g) :
      NativeGK5CGConservativeFiveCell first last w w
  | symm
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
      {w z : NativeF55RawVerticalFourCell first last f g}
      (a : NativeGK5CGConservativeFiveCell first last w z) :
      NativeGK5CGConservativeFiveCell first last z w
  | trans
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
      {w z q : NativeF55RawVerticalFourCell first last f g}
      (a : NativeGK5CGConservativeFiveCell first last w z)
      (b : NativeGK5CGConservativeFiveCell first last z q) :
      NativeGK5CGConservativeFiveCell first last w q
  | verticalLeft
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
      {w z : NativeF55RawVerticalFourCell first last f g}
      (a : NativeGK5CGConservativeFiveCell first last w z)
      (q : NativeF55RawVerticalFourCell first last g h) :
      NativeGK5CGConservativeFiveCell first last (.trans w q) (.trans z q)
  | verticalRight
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
      (q : NativeF55RawVerticalFourCell first last f g)
      {w z : NativeF55RawVerticalFourCell first last g h}
      (a : NativeGK5CGConservativeFiveCell first last w z) :
      NativeGK5CGConservativeFiveCell first last (.trans q w) (.trans q z)
  | verticalAssoc
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g h k : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
      (w : NativeF55RawVerticalFourCell first last f g)
      (z : NativeF55RawVerticalFourCell first last g h)
      (q : NativeF55RawVerticalFourCell first last h k) :
      NativeGK5CGConservativeFiveCell first last
        (.trans (.trans w z) q) (.trans w (.trans z q))
  | verticalLeftUnit
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
      (w : NativeF55RawVerticalFourCell first last f g) :
      NativeGK5CGConservativeFiveCell first last (.trans (.refl f) w) w
  | verticalRightUnit
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
      (w : NativeF55RawVerticalFourCell first last f g) :
      NativeGK5CGConservativeFiveCell first last (.trans w (.refl g)) w
  | inverseLeft
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
      (w : NativeF55RawVerticalFourCell first last f g) :
      NativeGK5CGConservativeFiveCell first last
        (.trans w (.symm w)) (.refl f)
  | inverseRight
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
      (w : NativeF55RawVerticalFourCell first last f g) :
      NativeGK5CGConservativeFiveCell first last
        (.trans (.symm w) w) (.refl g)
  | inverseRespect
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
      {w z : NativeF55RawVerticalFourCell first last f g}
      (a : NativeGK5CGConservativeFiveCell first last w z) :
      NativeGK5CGConservativeFiveCell first last (.symm w) (.symm z)
  | leftWhisker
      {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
      (prior : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s)
      {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p s t}
      {w z : NativeF55RawVerticalFourCell first last f g}
      (a : NativeGK5CGConservativeFiveCell first last w z) :
      NativeGK5CGConservativeFiveCell first last
        (.leftWhisker prior w) (.leftWhisker prior z)
  | rightWhisker
      {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
      {w z : NativeF55RawVerticalFourCell first last f g}
      (a : NativeGK5CGConservativeFiveCell first last w z)
      (suffix : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p s t) :
      NativeGK5CGConservativeFiveCell first last
        (.rightWhisker w suffix) (.rightWhisker z suffix)

/-- EVERY genuine conservative 5-cell constructor preserves
the signed source P77 4-associator charge, with exact dependent
source and target four-proof types. -/
theorem NativeGK5CGConservativeFiveCell.assocCharge_sound
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
    {w z : NativeF55RawVerticalFourCell first last f g}
    (v : NativeGK5CGConservativeFiveCell first last w z) :
    w.gk5cgAssocCharge = z.gk5cgAssocCharge := by
  induction v with
  | refl w => rfl
  | symm a ih => exact ih.symm
  | trans a b iha ihb => exact iha.trans ihb
  | verticalLeft a q ih =>
      change _ + q.gk5cgAssocCharge = _ + q.gk5cgAssocCharge
      exact congrArg (fun t : ℤ => t + q.gk5cgAssocCharge) ih
  | verticalRight q a ih =>
      change q.gk5cgAssocCharge + _ = q.gk5cgAssocCharge + _
      exact congrArg (fun t : ℤ => q.gk5cgAssocCharge + t) ih
  | verticalAssoc w z q =>
      change (w.gk5cgAssocCharge + z.gk5cgAssocCharge) +
        q.gk5cgAssocCharge =
        w.gk5cgAssocCharge + (z.gk5cgAssocCharge + q.gk5cgAssocCharge)
      exact add_assoc _ _ _
  | verticalLeftUnit w =>
      change (0 : ℤ) + w.gk5cgAssocCharge = w.gk5cgAssocCharge
      exact zero_add _
  | verticalRightUnit w =>
      change w.gk5cgAssocCharge + (0 : ℤ) = w.gk5cgAssocCharge
      exact add_zero _
  | inverseLeft w =>
      change w.gk5cgAssocCharge + -w.gk5cgAssocCharge = (0 : ℤ)
      exact add_neg_cancel _
  | inverseRight w =>
      change -w.gk5cgAssocCharge + w.gk5cgAssocCharge = (0 : ℤ)
      exact neg_add_cancel _
  | inverseRespect a ih =>
      exact congrArg Neg.neg ih
  | leftWhisker prior a ih => exact ih
  | rightWhisker a suffix ih => exact ih

/-- The TRUE source P77 upper/lower four-proof pentagon paths
CANNOT be linked by any conservative Type-valued 5-cell.
This no-go is quantified over ALL original F54/F55 source data,
not restricted to one physical numeric north gauge instance. -/
theorem nativeGK5CGOriginalPentagon_noConservativeFiveCell
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₀ r₁)
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₁ r₂)
    (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₂ r₃)
    (k : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₃ r₄) :
    ¬ Nonempty (NativeGK5CGConservativeFiveCell first last
      (nativeGK5CFP77UpperPath f g h k)
      (nativeGK5CFP77LowerPath f g h k)) := by
  rintro ⟨v⟩
  have hc := v.assocCharge_sound
  rw [nativeGK5CGUpperPath_assocCharge_three,
    nativeGK5CGLowerPath_assocCharge_two] at hc
  norm_num at hc

/-- Genuine P94A raw-four-cell comparisons on BOTH pentagon paths
exist, while a conservative ORIGINAL-P77 five-cell between their
source certificates does not. A P94A proof equality is NOT claimed. -/
theorem nativeGK5CGP94TwoPaths_but_noOriginalFiveCell
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₀ r₁)
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₁ r₂)
    (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₂ r₃)
    (k : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₃ r₄) :
    Nonempty (NativeF55P94UnitFourCell
      (NativeF55P92AssocComparison.original
        (nativeGK5CFOriginalLeftLeftLeft f g h k))
      (NativeF55P92AssocComparison.original
        (nativeGK5CFOriginalRightRight f g h k))) ∧
    ¬ Nonempty (NativeGK5CGConservativeFiveCell first last
      (nativeGK5CFP77UpperPath f g h k)
      (nativeGK5CFP77LowerPath f g h k)) :=
  ⟨⟨nativeGK5CFUpperRawP94 f g h k⟩,
   nativeGK5CGOriginalPentagon_noConservativeFiveCell f g h k⟩

/-- The precise independent numerical-structural boundary:
GK5CF/GK5CE RingHom pentagon always holds, but it does not
produce a conservative source 5-cell between ACTUAL P77 paths. -/
theorem nativeGK5CGNumericPentagon_and_fiveCellObstruction
    {α : Nat → Type u}
    (steps : (i : Nat) → α i → MvPolynomial (α (i+1)) Int)
    (start a b c d : Nat)
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₀ r₁)
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₁ r₂)
    (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₂ r₃)
    (k : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₃ r₄) :
    nativeGK5CFNumericalPentagonBoundary steps start a b c d ∧
    ¬ Nonempty (NativeGK5CGConservativeFiveCell first last
      (nativeGK5CFP77UpperPath f g h k)
      (nativeGK5CFP77LowerPath f g h k)) :=
  ⟨nativeGK5CFNumericalPentagonBoundary_valid steps start a b c d,
   nativeGK5CGOriginalPentagon_noConservativeFiveCell f g h k⟩

/-- A DIFFERENT newly-adjoined free Type-valued presentation.
Its 'pentagon' is an EXPLICIT NEW GENERATOR on the original P77
upper/lower proofs; it is NOT derived from P77 or P94A, does not
rewrite them, and does not imply the old conservative five-cell. -/
inductive NativeGK5CGAdjoinedPentagonFiveCell
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :
    ∀ {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s},
      NativeF55RawVerticalFourCell first last f g →
      NativeF55RawVerticalFourCell first last f g →
      Type (max (max uD uE) (max vD vE)) where
  | old
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
      {w z : NativeF55RawVerticalFourCell first last f g}
      (v : NativeGK5CGConservativeFiveCell first last w z) :
      NativeGK5CGAdjoinedPentagonFiveCell first last w z
  | pentagon
      {r₀ r₁ r₂ r₃ r₄ :
        KuuNativeF45Tree.DepthRotationRoute p first last}
      (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₀ r₁)
      (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₁ r₂)
      (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₂ r₃)
      (k : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₃ r₄) :
      NativeGK5CGAdjoinedPentagonFiveCell first last
        (nativeGK5CFP77UpperPath f g h k)
        (nativeGK5CFP77LowerPath f g h k)
  | refl
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
      (w : NativeF55RawVerticalFourCell first last f g) :
      NativeGK5CGAdjoinedPentagonFiveCell first last w w
  | symm
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
      {w z : NativeF55RawVerticalFourCell first last f g}
      (v : NativeGK5CGAdjoinedPentagonFiveCell first last w z) :
      NativeGK5CGAdjoinedPentagonFiveCell first last z w
  | trans
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
      {w z q : NativeF55RawVerticalFourCell first last f g}
      (v : NativeGK5CGAdjoinedPentagonFiveCell first last w z)
      (zq : NativeGK5CGAdjoinedPentagonFiveCell first last z q) :
      NativeGK5CGAdjoinedPentagonFiveCell first last w q

/-- A genuine new PRESENTATION generator now fills the parallel
source P77 upper/lower endpoints as an independently adjoined
Type-valued 5-cell, NOT as an old-P77 derivation. -/
def nativeGK5CGAdjoinedPentagonator
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₀ r₁)
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₁ r₂)
    (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₂ r₃)
    (k : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₃ r₄) :
    NativeGK5CGAdjoinedPentagonFiveCell first last
      (nativeGK5CFP77UpperPath f g h k)
      (nativeGK5CFP77LowerPath f g h k) :=
  .pentagon f g h k

/-- Sharp minimal boundary: the NEW pentagonator constructor
exists only in the enlarged presentation, while the true original
conservative source 5-cell remains impossible. -/
theorem nativeGK5CGAdjoined_vs_conservative_split
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₀ r₁)
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₁ r₂)
    (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₂ r₃)
    (k : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₃ r₄) :
    Nonempty (NativeGK5CGAdjoinedPentagonFiveCell first last
      (nativeGK5CFP77UpperPath f g h k)
      (nativeGK5CFP77LowerPath f g h k)) ∧
    ¬ Nonempty (NativeGK5CGConservativeFiveCell first last
      (nativeGK5CFP77UpperPath f g h k)
      (nativeGK5CFP77LowerPath f g h k)) :=
  ⟨⟨nativeGK5CGAdjoinedPentagonator f g h k⟩,
   nativeGK5CGOriginalPentagon_noConservativeFiveCell f g h k⟩

/-- There is NO endpoint-preserving retraction of the
adjoined presentation into the conservative source-five-cell
grammar. Even one true original F55 four-tuple yields the
contradictory signed charge 3=2. -/
theorem nativeGK5CGNoConservativeRetraction
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₀ r₁)
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₁ r₂)
    (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₂ r₃)
    (k : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₃ r₄) :
    ¬ (∀ {s t : KuuNativeF45Tree.DepthRotationRoute p first last}
         {a b : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p s t}
         {w z : NativeF55RawVerticalFourCell first last a b},
         NativeGK5CGAdjoinedPentagonFiveCell first last w z →
           Nonempty (NativeGK5CGConservativeFiveCell first last w z)) := by
  intro retract
  exact nativeGK5CGOriginalPentagon_noConservativeFiveCell f g h k
    (retract (nativeGK5CGAdjoinedPentagonator f g h k))

#print axioms NativeF55RawVerticalFourCell.gk5cgAssocCharge
#print axioms nativeGK5CGAssocCharge_symm
#print axioms nativeGK5CGAssocCharge_trans
#print axioms nativeGK5CGAssocCharge_leftWhisker
#print axioms nativeGK5CGAssocCharge_rightWhisker
#print axioms nativeGK5CGUpperPath_assocCharge_three
#print axioms nativeGK5CGLowerPath_assocCharge_two
#print axioms nativeGK5CGOriginalPentagon_charge_defect_one
#print axioms nativeGK5CGOriginalUpper_ne_lower
#print axioms NativeGK5CGConservativeFiveCell
#print axioms NativeGK5CGConservativeFiveCell.assocCharge_sound
#print axioms nativeGK5CGOriginalPentagon_noConservativeFiveCell
#print axioms nativeGK5CGP94TwoPaths_but_noOriginalFiveCell
#print axioms nativeGK5CGNumericPentagon_and_fiveCellObstruction
#print axioms NativeGK5CGAdjoinedPentagonFiveCell
#print axioms nativeGK5CGAdjoinedPentagonator
#print axioms nativeGK5CGAdjoined_vs_conservative_split
#print axioms nativeGK5CGNoConservativeRetraction

end
end Kuu.F112.Physical
