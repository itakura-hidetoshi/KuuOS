import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4ACExactPositiveFiber
import Mathlib.Tactic

/-!
F112-P94D3GK4AD — a NONCOMMUTATIVE ordered F54 history invariant.

The three existing GK4AA numeric components forget the ordering of
genuine original castDepths and actual backward RotationEdge evidence.
We preserve that information in the integral Heisenberg-type triple
((charge, backwardCount), orderedMoment) with the NONCOMMUTATIVE law
 (c,b,m) * (d,e,n) = (c+d, b+e, m+n+c*e).
Cast = (1,0,0), forward physical rotation = (-1,0,0),
backward physical rotation = (-1,1,0).

The genuine F54 associator is ONE cast followed by ONE forward
rotation and therefore acts as the UNIT in this new target. Original
F55 pentagon and square, ALL NINE original P92B constructors
(including true typed associator naturality), ALL FOURTEEN independent
structural seams, and all THREE extended comparison constructors are
checked on their ACTUAL Type-valued source proof histories.

This is not a synthetic P92B 3-cell, an imported Gray interchange,
or a claim that existing three numeric components are faithful.
Keep independent Kuu one presentation, strict 空 central,
append-only, tighten-only, same-root 107. No new axioms or sorry.
Protected validation-only #1558 Draft/open/unmerged.
Lean v4.30.0-rc2, mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section
universe uD vD uE vE

/-- Genuine ordered value: the first two components are physical
cast-minus-rotation charge and backwardCount; the third component
is the signed number of charge-before-backward encounters. -/
abbrev NativeGK4ADValue := (Int × Nat) × Int

def nativeGK4ADZero : NativeGK4ADValue := ((0, 0), 0)
def nativeGK4ADCast : NativeGK4ADValue := ((1, 0), 0)
def nativeGK4ADForward : NativeGK4ADValue := ((-1, 0), 0)
def nativeGK4ADBackward : NativeGK4ADValue := ((-1, 1), 0)

/-- Integer Heisenberg product. NONCOMMUTATIVE because the order
of a genuine backward rotation relative to an original cast matters. -/
def nativeGK4ADCombine (u v : NativeGK4ADValue) : NativeGK4ADValue :=
  ((u.1.1 + v.1.1, u.1.2 + v.1.2),
    u.2 + v.2 + u.1.1 * (v.1.2 : Int))

theorem nativeGK4ADCombine_assoc (a b c : NativeGK4ADValue) :
    nativeGK4ADCombine (nativeGK4ADCombine a b) c =
      nativeGK4ADCombine a (nativeGK4ADCombine b c) := by
  rcases a with ⟨⟨ca, ba⟩, ma⟩
  rcases b with ⟨⟨cb, bb⟩, mb⟩
  rcases c with ⟨⟨cc, bc⟩, mc⟩
  apply Prod.ext
  · apply Prod.ext
    · change (ca + cb) + cc = ca + (cb + cc)
      omega
    · change (ba + bb) + bc = ba + (bb + bc)
      omega
  · change
      (ma + mb + ca * (bb : Int)) + mc + (ca + cb) * (bc : Int) =
        ma + (mb + mc + cb * (bc : Int)) + ca * ((bb + bc : Nat) : Int)
    push_cast
    ring

theorem nativeGK4ADCombine_leftUnit (a : NativeGK4ADValue) :
    nativeGK4ADCombine nativeGK4ADZero a = a := by
  rcases a with ⟨⟨c, b⟩, m⟩
  simp [nativeGK4ADCombine, nativeGK4ADZero]

theorem nativeGK4ADCombine_rightUnit (a : NativeGK4ADValue) :
    nativeGK4ADCombine a nativeGK4ADZero = a := by
  rcases a with ⟨⟨c, b⟩, m⟩
  simp [nativeGK4ADCombine, nativeGK4ADZero]

/-- This is the crucial original typed associator cancellation,
NOT cancellation of an arbitrary forward/backward physical backtrack. -/
theorem nativeGK4ADCastForward :
    nativeGK4ADCombine nativeGK4ADCast nativeGK4ADForward =
      nativeGK4ADZero := by decide

section GenuineOriginalSource
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}

/-- The ACTUAL oriented F54 rotation-edge constructor is inspected,
including the original LocalRotation Type-valued witness. -/
def KuuNativeF45Tree.RotationEdge.gk4adValue
    {n m : Nat}
    {before after : KuuNativeF45Tree p n m ma pa mb pb}
    (edge : KuuNativeF45Tree.RotationEdge p before after) :
    NativeGK4ADValue :=
  match edge with
  | .forward _ => nativeGK4ADForward
  | .backward _ => nativeGK4ADBackward

/-- Intermediate-tree preserving genuine F54 original RotationChain. -/
def KuuNativeF45Tree.RotationChain.gk4adValue
    {n m : Nat}
    {before after : KuuNativeF45Tree p n m ma pa mb pb} :
    KuuNativeF45Tree.RotationChain p before after → NativeGK4ADValue
  | .refl _ => nativeGK4ADZero
  | .snoc chain edge =>
      nativeGK4ADCombine chain.gk4adValue edge.gk4adValue

/-- Every original F54 source constructor is counted directly.
Both dependent Nat casts are ONE original cast history symbol;
typed source contexts preserve the ordered history. -/
def KuuNativeF45Tree.DepthRotationRoute.gk4adValue
    {n n' m m' : Nat}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (route : KuuNativeF45Tree.DepthRotationRoute p first last) :
    NativeGK4ADValue := by
  induction route with
  | chain path => exact path.gk4adValue
  | castDepths _ _ _ => exact nativeGK4ADCast
  | trans _ _ ihLeft ihRight =>
      exact nativeGK4ADCombine ihLeft ihRight
  | leftContext _ _ ih => exact ih
  | rightContext _ _ ih => exact ih

theorem nativeGK4AD_trans
    {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
    {first : KuuNativeF45Tree p n₁ m₁ ma pa mb pb}
    {middle : KuuNativeF45Tree p n₂ m₂ ma pa mb pb}
    {last : KuuNativeF45Tree p n₃ m₃ ma pa mb pb}
    (u : KuuNativeF45Tree.DepthRotationRoute p first middle)
    (v : KuuNativeF45Tree.DepthRotationRoute p middle last) :
    (KuuNativeF45Tree.DepthRotationRoute.trans u v).gk4adValue =
      nativeGK4ADCombine u.gk4adValue v.gk4adValue := rfl

@[simp] theorem nativeGK4AD_leftContext
    {n n' m m' k l : Nat}
    {mc : KuuNativeBlocks a b} {pc : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (route : KuuNativeF45Tree.DepthRotationRoute p first last)
    (later : KuuNativeF45Tree p k l mb pb mc pc) :
    (KuuNativeF45Tree.DepthRotationRoute.leftContext route later).gk4adValue =
      route.gk4adValue := rfl

@[simp] theorem nativeGK4AD_rightContext
    {k l n n' m m' : Nat}
    {mc : KuuNativeBlocks a b} {pc : KuuNativeBlocks x y}
    (earlier : KuuNativeF45Tree p k l ma pa mb pb)
    {first : KuuNativeF45Tree p n m mb pb mc pc}
    {last : KuuNativeF45Tree p n' m' mb pb mc pc}
    (route : KuuNativeF45Tree.DepthRotationRoute p first last) :
    (KuuNativeF45Tree.DepthRotationRoute.rightContext earlier route).gk4adValue =
      route.gk4adValue := rfl

@[simp] theorem nativeGK4AD_assoc
    {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
    {p₀ p₁ p₂ p₃ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ q₃ : KuuNativeBlocks x y}
    (t₁ : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁)
    (t₂ : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂)
    (t₃ : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃) :
    (KuuNativeF45Tree.DepthRotationRoute.assoc t₁ t₂ t₃).gk4adValue =
      nativeGK4ADZero := by
  exact nativeGK4ADCastForward

/-- All two-context horizontal paths read the original histories in
the TRUE left-to-right order and NOT in the opposite order. -/
theorem nativeGK4AD_horizontal
    {n n' m m' k k' l l' : Nat}
    {p₀ p₁ p₂ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ : KuuNativeBlocks x y}
    {leftBefore : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
    {leftAfter : KuuNativeF45Tree p n' m' p₀ q₀ p₁ q₁}
    {rightBefore : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂}
    {rightAfter : KuuNativeF45Tree p k' l' p₁ q₁ p₂ q₂}
    (u : KuuNativeF45Tree.DepthRotationRoute p leftBefore leftAfter)
    (v : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter) :
    (nativeF54P90HorizontalRoute u v).gk4adValue =
      nativeGK4ADCombine u.gk4adValue v.gk4adValue := by
  rfl

/-- Associator-naturality soundness is NONCOMMUTATIVE: no arbitrary
reordering of u/v/w; only reassociation of the exact same order,
with a genuine value-neutral source/target associator. -/
theorem nativeGK4AD_assocNaturality
    {n₁ n₁' n₂ n₂' n₃ n₃' m₁ m₁' m₂ m₂' m₃ m₃' : Nat}
    {p₀ p₁ p₂ p₃ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ q₃ : KuuNativeBlocks x y}
    {firstBefore : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁}
    {firstAfter : KuuNativeF45Tree p n₁' m₁' p₀ q₀ p₁ q₁}
    {secondBefore : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂}
    {secondAfter : KuuNativeF45Tree p n₂' m₂' p₁ q₁ p₂ q₂}
    {thirdBefore : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃}
    {thirdAfter : KuuNativeF45Tree p n₃' m₃' p₂ q₂ p₃ q₃}
    (u : KuuNativeF45Tree.DepthRotationRoute p firstBefore firstAfter)
    (v : KuuNativeF45Tree.DepthRotationRoute p secondBefore secondAfter)
    (w : KuuNativeF45Tree.DepthRotationRoute p thirdBefore thirdAfter) :
    (nativeF54P90AssocNaturalityLeftRoute u v w).gk4adValue =
      (nativeF54P90AssocNaturalityRightRoute u v w).gk4adValue := by
  simp only [nativeF54P90AssocNaturalityLeftRoute,
    nativeF54P90AssocNaturalityRightRoute, nativeGK4AD_trans,
    nativeGK4AD_horizontal, nativeGK4AD_assoc,
    nativeGK4ADCombine_leftUnit, nativeGK4ADCombine_rightUnit]
  exact nativeGK4ADCombine_assoc u.gk4adValue v.gk4adValue w.gk4adValue

end GenuineOriginalSource

section AllActualComparisons
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable {n n' m m' : Nat}
variable {first : KuuNativeF45Tree p n m ma pa mb pb}
variable {last : KuuNativeF45Tree p n' m' ma pa mb pb}
variable {r s : KuuNativeF45Tree.DepthRotationRoute p first last}

/-- ALL NINE actual original F55 proof comparison constructors. -/
theorem nativeGK4AD_original_sound
    (cell : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    r.gk4adValue = s.gk4adValue := by
  induction cell with
  | ident route => rfl
  | pentagon a b c d =>
      change nativeGK4ADZero = nativeGK4ADZero
      rfl
  | disjointSquare left right =>
      change
        nativeGK4ADCombine nativeGK4ADForward nativeGK4ADForward =
          nativeGK4ADCombine nativeGK4ADForward nativeGK4ADForward
      rfl
  | symm cell ih => exact ih.symm
  | trans left right ihLeft ihRight => exact ihLeft.trans ihRight
  | leftContext cell later ih => exact ih
  | rightContext earlier cell ih => exact ih
  | precompose prior cell ih =>
      simp only [nativeGK4AD_trans]
      exact congrArg (nativeGK4ADCombine prior.gk4adValue) ih
  | postcompose cell suffix ih =>
      simp only [nativeGK4AD_trans]
      exact congrArg (fun x => nativeGK4ADCombine x suffix.gk4adValue) ih

/-- ALL NINE original typed P92B comparison constructors. -/
theorem nativeGK4AD_p92_sound
    (cell : NativeF55P92AssocComparison p r s) :
    r.gk4adValue = s.gk4adValue := by
  induction cell with
  | original old => exact nativeGK4AD_original_sound old
  | assocNaturality u v w => exact nativeGK4AD_assocNaturality u v w
  | refl route => rfl
  | symm cell ih => exact ih.symm
  | trans left right ihLeft ihRight => exact ihLeft.trans ihRight
  | leftContext cell later ih => exact ih
  | rightContext earlier cell ih => exact ih
  | precompose prior cell ih =>
      simp only [nativeGK4AD_trans]
      exact congrArg (nativeGK4ADCombine prior.gk4adValue) ih
  | postcompose cell suffix ih =>
      simp only [nativeGK4AD_trans]
      exact congrArg (fun x => nativeGK4ADCombine x suffix.gk4adValue) ih

/-- ALL FOURTEEN original independent structural seam constructors. -/
theorem nativeGK4AD_seam_sound
    (seam : NativeF54StructuralSeam p r s) :
    r.gk4adValue = s.gk4adValue := by
  induction seam with
  | refl route => rfl
  | symm seam ih => exact ih.symm
  | trans left right ihLeft ihRight => exact ihLeft.trans ihRight
  | reassoc u v w =>
      simp only [nativeGK4AD_trans]
      exact nativeGK4ADCombine_assoc _ _ _
  | leftUnit route =>
      simp only [nativeGK4AD_trans]
      change nativeGK4ADCombine nativeGK4ADZero route.gk4adValue =
        route.gk4adValue
      exact nativeGK4ADCombine_leftUnit _
  | rightUnit route =>
      simp only [nativeGK4AD_trans]
      change nativeGK4ADCombine route.gk4adValue nativeGK4ADZero =
        route.gk4adValue
      exact nativeGK4ADCombine_rightUnit _
  | precompose prior seam ih =>
      simp only [nativeGK4AD_trans]
      exact congrArg (nativeGK4ADCombine prior.gk4adValue) ih
  | postcompose seam suffix ih =>
      simp only [nativeGK4AD_trans]
      exact congrArg (fun x => nativeGK4ADCombine x suffix.gk4adValue) ih
  | leftContextTrans u v later =>
      simp only [nativeGK4AD_leftContext, nativeGK4AD_trans]
  | rightContextTrans earlier u v =>
      simp only [nativeGK4AD_rightContext, nativeGK4AD_trans]
  | leftContextUnit earlier later => rfl
  | rightContextUnit earlier later => rfl
  | leftContextCongruence seam later ih => exact ih
  | rightContextCongruence earlier seam ih => exact ih

/-- ALL THREE extended structural comparison constructors. -/
theorem nativeGK4AD_structural_sound
    (cell : NativeF55StructuralComparison p r s) :
    r.gk4adValue = s.gk4adValue := by
  induction cell with
  | original old => exact nativeGK4AD_p92_sound old
  | structural seam => exact nativeGK4AD_seam_sound seam
  | trans left right ihLeft ihRight => exact ihLeft.trans ihRight

end AllActualComparisons

section GenuineQuotientDescent
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
variable (first : KuuNativeF45Tree p n₁ m₁ ma pa mb pb)
variable (middle : KuuNativeF45Tree p n₂ m₂ ma pa mb pb)
variable (last : KuuNativeF45Tree p n₃ m₃ ma pa mb pb)

/-- Descend the full noncommutative ordered invariant to the
ORIGINAL P92B witness-existence quotient Q by actual Type cells. -/
def nativeGK4ADP92Value :
    NativeF55P92AssocRouteClasses first middle → NativeGK4ADValue :=
  _root_.Quotient.lift
    (fun raw : KuuNativeF45Tree.DepthRotationRoute p first middle =>
      raw.gk4adValue)
    (by
      intro r s h
      rcases h with ⟨cell⟩
      exact nativeGK4AD_p92_sound cell)

/-- INDEPENDENT descent to the structural quotient S: F54 seams are
real added comparisons, not implicit P92B 3-cell constructors. -/
def nativeGK4ADStructuralValue :
    NativeGK4EStructuralRouteClasses first middle → NativeGK4ADValue :=
  _root_.Quotient.lift
    (fun raw : KuuNativeF45Tree.DepthRotationRoute p first middle =>
      raw.gk4adValue)
    (by
      intro r s h
      rcases h with ⟨cell⟩
      exact nativeGK4AD_structural_sound cell)

@[simp] theorem nativeGK4ADP92Value_class
    (raw : KuuNativeF45Tree.DepthRotationRoute p first middle) :
    nativeGK4ADP92Value first middle
        (nativeF55P92AssocRouteClass first middle raw) =
      raw.gk4adValue := rfl

@[simp] theorem nativeGK4ADStructuralValue_class
    (raw : KuuNativeF45Tree.DepthRotationRoute p first middle) :
    nativeGK4ADStructuralValue first middle
        (nativeGK4EStructuralRouteClass first middle raw) =
      raw.gk4adValue := rfl

theorem nativeGK4AD_commutes
    (q : NativeF55P92AssocRouteClasses first middle) :
    nativeGK4ADStructuralValue first middle
        (nativeGK4EP92ToStructural first middle q) =
      nativeGK4ADP92Value first middle q := by
  refine _root_.Quotient.inductionOn q ?_
  intro raw
  rfl

theorem nativeGK4ADStructural_compose
    (u : NativeGK4EStructuralRouteClasses first middle)
    (v : NativeGK4EStructuralRouteClasses middle last) :
    nativeGK4ADStructuralValue first last
        (nativeGK4H_structuralCompose first middle last u v) =
      nativeGK4ADCombine
        (nativeGK4ADStructuralValue first middle u)
        (nativeGK4ADStructuralValue middle last v) := by
  refine _root_.Quotient.inductionOn u ?_
  intro rawU
  refine _root_.Quotient.inductionOn v ?_
  intro rawV
  exact nativeGK4AD_trans rawU rawV

@[simp] theorem nativeGK4ADStructural_unit :
    nativeGK4ADStructuralValue first first
      (nativeGK4H_structuralUnit first) = nativeGK4ADZero := rfl

end GenuineQuotientDescent

#print axioms NativeGK4ADValue
#print axioms nativeGK4ADCombine
#print axioms nativeGK4ADCombine_assoc
#print axioms nativeGK4ADCombine_leftUnit
#print axioms nativeGK4ADCombine_rightUnit
#print axioms nativeGK4ADCastForward
#print axioms KuuNativeF45Tree.RotationEdge.gk4adValue
#print axioms KuuNativeF45Tree.RotationChain.gk4adValue
#print axioms KuuNativeF45Tree.DepthRotationRoute.gk4adValue
#print axioms nativeGK4AD_trans
#print axioms nativeGK4AD_leftContext
#print axioms nativeGK4AD_rightContext
#print axioms nativeGK4AD_assoc
#print axioms nativeGK4AD_horizontal
#print axioms nativeGK4AD_assocNaturality
#print axioms nativeGK4AD_original_sound
#print axioms nativeGK4AD_p92_sound
#print axioms nativeGK4AD_seam_sound
#print axioms nativeGK4AD_structural_sound
#print axioms nativeGK4ADP92Value
#print axioms nativeGK4ADStructuralValue
#print axioms nativeGK4ADP92Value_class
#print axioms nativeGK4ADStructuralValue_class
#print axioms nativeGK4AD_commutes
#print axioms nativeGK4ADStructural_compose
#print axioms nativeGK4ADStructural_unit

end
end Kuu.F112.Physical
