import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4ATStrictJointArithmeticSlice
import Mathlib.Tactic

/-!
F112-P94D3GK4AU -- one integer-parametric family on the ACTUAL
original F54 Type-valued source. The value is a function Int ->
integer 2x2 matrices, with pointwise NONCOMMUTATIVE multiplication:
  C(t)=[[1,1],[0,1]], F(t)=[[1,-1],[0,1]], R(t)=[[1,0],[t,1]].
C(t)*F(t)=I for every t. Reuse the existing verified AH matrix
multiplication rather than replace any old matrix definitions.

Prove preservation of all actual F55 9, P92B 9, independent
structural seam 14 and extended comparison 3 constructors as
EQUALITY OF WHOLE FAMILIES. Descend separately to the original
P92B Q and independent S, with true S composition and units.
No source cell is manufactured from observation equality. No
unproved Q category laws, global faithfulness, arithmetic
surjectivity, fixed infinite fiber, Gray or hyperdescent.
In particular descent of this WHOLE FAMILY through the old K_AI
is NOT asserted merely because evaluations at 1 and 4 descend.
Append-only/tighten-only/same-root107. Strict Kuu central;
independent Kuu one presentation; protect #1558 Draft/open/unmerged.
Lean v4.30.0-rc2; mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
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

/-- A whole family, not a pair of sampled matrices. -/
abbrev NativeGK4AUValue := Int → NativeGK4AHMatrix

def nativeGK4AUMul (u v : NativeGK4AUValue) : NativeGK4AUValue :=
  fun t => nativeGK4AHMul (u t) (v t)

def nativeGK4AUOne : NativeGK4AUValue := fun _ => nativeGK4AHOne
def nativeGK4AUCast : NativeGK4AUValue := fun _ => nativeGK4AHCast
def nativeGK4AUForward : NativeGK4AUValue := fun _ => nativeGK4AHForward
def nativeGK4AUBackward : NativeGK4AUValue := fun t => ((1, 0), (t, 1))

theorem nativeGK4AUMul_assoc (u v w : NativeGK4AUValue) :
    nativeGK4AUMul (nativeGK4AUMul u v) w =
      nativeGK4AUMul u (nativeGK4AUMul v w) := by
  funext t
  exact nativeGK4AHMul_assoc (u t) (v t) (w t)

theorem nativeGK4AUMul_leftUnit (u : NativeGK4AUValue) :
    nativeGK4AUMul nativeGK4AUOne u = u := by
  funext t
  exact nativeGK4AHMul_leftUnit (u t)

theorem nativeGK4AUMul_rightUnit (u : NativeGK4AUValue) :
    nativeGK4AUMul u nativeGK4AUOne = u := by
  funext t
  exact nativeGK4AHMul_rightUnit (u t)

/-- The TRUE associator's cast-forward product is neutral at all t. -/
theorem nativeGK4AUCastForward :
    nativeGK4AUMul nativeGK4AUCast nativeGK4AUForward = nativeGK4AUOne := by
  funext t
  exact nativeGK4AHCastForward

section GenuineOriginalSource
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}

def KuuNativeF45Tree.RotationEdge.gk4auFamily
    {n m : Nat}
    {before after : KuuNativeF45Tree p n m ma pa mb pb}
    (edge : KuuNativeF45Tree.RotationEdge p before after) : NativeGK4AUValue :=
  match edge with
  | .forward _ => nativeGK4AUForward
  | .backward _ => nativeGK4AUBackward

def KuuNativeF45Tree.RotationChain.gk4auFamily
    {n m : Nat}
    {before after : KuuNativeF45Tree p n m ma pa mb pb} :
    KuuNativeF45Tree.RotationChain p before after → NativeGK4AUValue
  | .refl _ => nativeGK4AUOne
  | .snoc chain edge => nativeGK4AUMul chain.gk4auFamily edge.gk4auFamily

/-- Original dependent route, retaining both Nat axes and all contexts. -/
def KuuNativeF45Tree.DepthRotationRoute.gk4auFamily
    {n n' m m' : Nat}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (route : KuuNativeF45Tree.DepthRotationRoute p first last) : NativeGK4AUValue := by
  induction route with
  | chain path => exact path.gk4auFamily
  | castDepths _ _ _ => exact nativeGK4AUCast
  | trans _ _ ihLeft ihRight => exact nativeGK4AUMul ihLeft ihRight
  | leftContext _ _ ih => exact ih
  | rightContext _ _ ih => exact ih

theorem nativeGK4AU_trans
    {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
    {first : KuuNativeF45Tree p n₁ m₁ ma pa mb pb}
    {middle : KuuNativeF45Tree p n₂ m₂ ma pa mb pb}
    {last : KuuNativeF45Tree p n₃ m₃ ma pa mb pb}
    (u : KuuNativeF45Tree.DepthRotationRoute p first middle)
    (v : KuuNativeF45Tree.DepthRotationRoute p middle last) :
    (KuuNativeF45Tree.DepthRotationRoute.trans u v).gk4auFamily =
      nativeGK4AUMul u.gk4auFamily v.gk4auFamily := rfl

@[simp] theorem nativeGK4AU_leftContext
    {n n' m m' k l : Nat}
    {mc : KuuNativeBlocks a b} {pc : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (route : KuuNativeF45Tree.DepthRotationRoute p first last)
    (later : KuuNativeF45Tree p k l mb pb mc pc) :
    (KuuNativeF45Tree.DepthRotationRoute.leftContext route later).gk4auFamily =
      route.gk4auFamily := rfl

@[simp] theorem nativeGK4AU_rightContext
    {k l n n' m m' : Nat}
    {mc : KuuNativeBlocks a b} {pc : KuuNativeBlocks x y}
    (earlier : KuuNativeF45Tree p k l ma pa mb pb)
    {first : KuuNativeF45Tree p n m mb pb mc pc}
    {last : KuuNativeF45Tree p n' m' mb pb mc pc}
    (route : KuuNativeF45Tree.DepthRotationRoute p first last) :
    (KuuNativeF45Tree.DepthRotationRoute.rightContext earlier route).gk4auFamily =
      route.gk4auFamily := rfl

@[simp] theorem nativeGK4AU_assoc
    {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
    {p₀ p₁ p₂ p₃ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ q₃ : KuuNativeBlocks x y}
    (t₁ : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁)
    (t₂ : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂)
    (t₃ : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃) :
    (KuuNativeF45Tree.DepthRotationRoute.assoc t₁ t₂ t₃).gk4auFamily =
      nativeGK4AUOne := nativeGK4AUCastForward

theorem nativeGK4AU_horizontal
    {n n' m m' k k' l l' : Nat}
    {p₀ p₁ p₂ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ : KuuNativeBlocks x y}
    {leftBefore : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
    {leftAfter : KuuNativeF45Tree p n' m' p₀ q₀ p₁ q₁}
    {rightBefore : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂}
    {rightAfter : KuuNativeF45Tree p k' l' p₁ q₁ p₂ q₂}
    (u : KuuNativeF45Tree.DepthRotationRoute p leftBefore leftAfter)
    (v : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter) :
    (nativeF54P90HorizontalRoute u v).gk4auFamily =
      nativeGK4AUMul u.gk4auFamily v.gk4auFamily := rfl

/-- Actual associator naturality uses only reassociation, never exchange. -/
theorem nativeGK4AU_assocNaturality
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
    (nativeF54P90AssocNaturalityLeftRoute u v w).gk4auFamily =
      (nativeF54P90AssocNaturalityRightRoute u v w).gk4auFamily := by
  simp only [nativeF54P90AssocNaturalityLeftRoute,
    nativeF54P90AssocNaturalityRightRoute, nativeGK4AU_trans,
    nativeGK4AU_horizontal, nativeGK4AU_assoc,
    nativeGK4AUMul_leftUnit, nativeGK4AUMul_rightUnit]
  exact nativeGK4AUMul_assoc u.gk4auFamily v.gk4auFamily w.gk4auFamily

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

/-- All nine actual original F55 comparison constructors. -/
theorem nativeGK4AU_original_sound
    (cell : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    r.gk4auFamily = s.gk4auFamily := by
  induction cell with
  | ident route => rfl
  | pentagon a b c d =>
      change nativeGK4AUOne = nativeGK4AUOne
      rfl
  | disjointSquare left right =>
      change nativeGK4AUMul nativeGK4AUForward nativeGK4AUForward =
        nativeGK4AUMul nativeGK4AUForward nativeGK4AUForward
      rfl
  | symm cell ih => exact ih.symm
  | trans left right ihLeft ihRight => exact ihLeft.trans ihRight
  | leftContext cell later ih => exact ih
  | rightContext earlier cell ih => exact ih
  | precompose prior cell ih =>
      simp only [nativeGK4AU_trans]
      exact congrArg (nativeGK4AUMul prior.gk4auFamily) ih
  | postcompose cell suffix ih =>
      simp only [nativeGK4AU_trans]
      exact congrArg (fun x => nativeGK4AUMul x suffix.gk4auFamily) ih

/-- All nine actual original P92B constructors. -/
theorem nativeGK4AU_p92_sound
    (cell : NativeF55P92AssocComparison p r s) :
    r.gk4auFamily = s.gk4auFamily := by
  induction cell with
  | original old => exact nativeGK4AU_original_sound old
  | assocNaturality u v w => exact nativeGK4AU_assocNaturality u v w
  | refl route => rfl
  | symm cell ih => exact ih.symm
  | trans left right ihLeft ihRight => exact ihLeft.trans ihRight
  | leftContext cell later ih => exact ih
  | rightContext earlier cell ih => exact ih
  | precompose prior cell ih =>
      simp only [nativeGK4AU_trans]
      exact congrArg (nativeGK4AUMul prior.gk4auFamily) ih
  | postcompose cell suffix ih =>
      simp only [nativeGK4AU_trans]
      exact congrArg (fun x => nativeGK4AUMul x suffix.gk4auFamily) ih

/-- All fourteen independent structural seam constructors. -/
theorem nativeGK4AU_seam_sound
    (seam : NativeF54StructuralSeam p r s) :
    r.gk4auFamily = s.gk4auFamily := by
  induction seam with
  | refl route => rfl
  | symm seam ih => exact ih.symm
  | trans left right ihLeft ihRight => exact ihLeft.trans ihRight
  | reassoc u v w =>
      simp only [nativeGK4AU_trans]
      exact nativeGK4AUMul_assoc _ _ _
  | leftUnit route =>
      simp only [nativeGK4AU_trans]
      change nativeGK4AUMul nativeGK4AUOne route.gk4auFamily = route.gk4auFamily
      exact nativeGK4AUMul_leftUnit _
  | rightUnit route =>
      simp only [nativeGK4AU_trans]
      change nativeGK4AUMul route.gk4auFamily nativeGK4AUOne = route.gk4auFamily
      exact nativeGK4AUMul_rightUnit _
  | precompose prior seam ih =>
      simp only [nativeGK4AU_trans]
      exact congrArg (nativeGK4AUMul prior.gk4auFamily) ih
  | postcompose seam suffix ih =>
      simp only [nativeGK4AU_trans]
      exact congrArg (fun x => nativeGK4AUMul x suffix.gk4auFamily) ih
  | leftContextTrans u v later =>
      simp only [nativeGK4AU_leftContext, nativeGK4AU_trans]
  | rightContextTrans earlier u v =>
      simp only [nativeGK4AU_rightContext, nativeGK4AU_trans]
  | leftContextUnit earlier later => rfl
  | rightContextUnit earlier later => rfl
  | leftContextCongruence seam later ih => exact ih
  | rightContextCongruence earlier seam ih => exact ih

/-- All three extended structural comparison constructors. -/
theorem nativeGK4AU_structural_sound
    (cell : NativeF55StructuralComparison p r s) :
    r.gk4auFamily = s.gk4auFamily := by
  induction cell with
  | original old => exact nativeGK4AU_p92_sound old
  | structural seam => exact nativeGK4AU_seam_sound seam
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

def nativeGK4AUP92Value :
    NativeF55P92AssocRouteClasses first middle → NativeGK4AUValue :=
  _root_.Quotient.lift
    (fun raw : KuuNativeF45Tree.DepthRotationRoute p first middle => raw.gk4auFamily)
    (by
      intro r s h
      rcases h with ⟨cell⟩
      exact nativeGK4AU_p92_sound cell)

def nativeGK4AUStructuralValue :
    NativeGK4EStructuralRouteClasses first middle → NativeGK4AUValue :=
  _root_.Quotient.lift
    (fun raw : KuuNativeF45Tree.DepthRotationRoute p first middle => raw.gk4auFamily)
    (by
      intro r s h
      rcases h with ⟨cell⟩
      exact nativeGK4AU_structural_sound cell)

@[simp] theorem nativeGK4AUP92Value_class
    (raw : KuuNativeF45Tree.DepthRotationRoute p first middle) :
    nativeGK4AUP92Value first middle (nativeF55P92AssocRouteClass first middle raw) =
      raw.gk4auFamily := rfl

@[simp] theorem nativeGK4AUStructuralValue_class
    (raw : KuuNativeF45Tree.DepthRotationRoute p first middle) :
    nativeGK4AUStructuralValue first middle
      (nativeGK4EStructuralRouteClass first middle raw) = raw.gk4auFamily := rfl

theorem nativeGK4AU_commutes
    (q : NativeF55P92AssocRouteClasses first middle) :
    nativeGK4AUStructuralValue first middle
      (nativeGK4EP92ToStructural first middle q) = nativeGK4AUP92Value first middle q := by
  refine _root_.Quotient.inductionOn q ?_
  intro raw
  rfl

theorem nativeGK4AUStructural_compose
    (u : NativeGK4EStructuralRouteClasses first middle)
    (v : NativeGK4EStructuralRouteClasses middle last) :
    nativeGK4AUStructuralValue first last
      (nativeGK4H_structuralCompose first middle last u v) =
    nativeGK4AUMul (nativeGK4AUStructuralValue first middle u)
      (nativeGK4AUStructuralValue middle last v) := by
  refine _root_.Quotient.inductionOn₂ u v ?_
  intro rawU rawV
  exact nativeGK4AU_trans rawU rawV

@[simp] theorem nativeGK4AUStructural_unit :
    nativeGK4AUStructuralValue first first (nativeGK4H_structuralUnit first) =
      nativeGK4AUOne := rfl

end GenuineQuotientDescent

#print axioms NativeGK4AUValue
#print axioms nativeGK4AUMul
#print axioms nativeGK4AUOne
#print axioms nativeGK4AUCast
#print axioms nativeGK4AUForward
#print axioms nativeGK4AUBackward
#print axioms nativeGK4AUMul_assoc
#print axioms nativeGK4AUMul_leftUnit
#print axioms nativeGK4AUMul_rightUnit
#print axioms nativeGK4AUCastForward
#print axioms KuuNativeF45Tree.RotationEdge.gk4auFamily
#print axioms KuuNativeF45Tree.RotationChain.gk4auFamily
#print axioms KuuNativeF45Tree.DepthRotationRoute.gk4auFamily
#print axioms nativeGK4AU_trans
#print axioms nativeGK4AU_leftContext
#print axioms nativeGK4AU_rightContext
#print axioms nativeGK4AU_assoc
#print axioms nativeGK4AU_horizontal
#print axioms nativeGK4AU_assocNaturality
#print axioms nativeGK4AU_original_sound
#print axioms nativeGK4AU_p92_sound
#print axioms nativeGK4AU_seam_sound
#print axioms nativeGK4AU_structural_sound
#print axioms nativeGK4AUP92Value
#print axioms nativeGK4AUStructuralValue
#print axioms nativeGK4AUP92Value_class
#print axioms nativeGK4AUStructuralValue_class
#print axioms nativeGK4AU_commutes
#print axioms nativeGK4AUStructural_compose
#print axioms nativeGK4AUStructural_unit

end
end Kuu.F112.Physical
