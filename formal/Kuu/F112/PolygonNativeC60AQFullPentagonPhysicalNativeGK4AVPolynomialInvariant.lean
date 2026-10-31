import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4AUParameterCongruence
import Mathlib.Algebra.Polynomial.Eval.Defs
import Mathlib.Algebra.Polynomial.Degree.Lemmas
import Mathlib.Tactic

/-!
F112-P94D3GK4AV — ACTUAL original F54 Type-valued histories admit an
integer POLYNOMIAL two-by-two matrix invariant in Z[X], not merely
an untyped word, or a function with hypothesized polynomiality.
Generators are C=[[1,1],[0,1]], F=[[1,-1],[0,1]],
R(X)=[[1,0],[X,1]]. The exact noncommutative product is used.

Preservation is proven on all true original F55 9, P92B 9,
independent 14 structural seams and 3 extended constructors,
then separately descended to original Q and independent S.
Comparison equations do NOT create source Type-valued cells, do not
assume Q category laws, nor descend automatically through old K_AI.

This is an append-only strict extension: no old Lean is edited;
107 public roots, Lean v4.30.0-rc2, mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6 are fixed.
Strict Kuu central, independent Kuu one presentation;
Gray excluded; protect #1558 Draft/OPEN/unmerged.
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

/-- Polynomial matrix with four genuine integer-polynomial entries. -/
abbrev NativeGK4AVValue := (Polynomial Int × Polynomial Int) ×
  (Polynomial Int × Polynomial Int)

/-- Ordered multiplication in SL₂(Z[X])'s ambient matrix ring. -/
def nativeGK4AVMul (u v : NativeGK4AVValue) : NativeGK4AVValue :=
  ((u.1.1 * v.1.1 + u.1.2 * v.2.1,
    u.1.1 * v.1.2 + u.1.2 * v.2.2),
   (u.2.1 * v.1.1 + u.2.2 * v.2.1,
    u.2.1 * v.1.2 + u.2.2 * v.2.2))

def nativeGK4AVOne : NativeGK4AVValue := ((1, 0), (0, 1))
def nativeGK4AVCast : NativeGK4AVValue := ((1, 1), (0, 1))
def nativeGK4AVForward : NativeGK4AVValue := ((1, -1), (0, 1))
def nativeGK4AVBackward : NativeGK4AVValue :=
  ((1, 0), (Polynomial.X, 1))

theorem nativeGK4AVMul_assoc (u v w : NativeGK4AVValue) :
    nativeGK4AVMul (nativeGK4AVMul u v) w =
      nativeGK4AVMul u (nativeGK4AVMul v w) := by
  rcases u with ⟨⟨a,b⟩,⟨c,d⟩⟩
  rcases v with ⟨⟨e,f⟩,⟨g,h⟩⟩
  rcases w with ⟨⟨i,j⟩,⟨k,l⟩⟩
  apply Prod.ext
  · apply Prod.ext
    · change (a*e+b*g)*i + (a*f+b*h)*k =
        a*(e*i+f*k) + b*(g*i+h*k)
      ring
    · change (a*e+b*g)*j + (a*f+b*h)*l =
        a*(e*j+f*l) + b*(g*j+h*l)
      ring
  · apply Prod.ext
    · change (c*e+d*g)*i + (c*f+d*h)*k =
        c*(e*i+f*k) + d*(g*i+h*k)
      ring
    · change (c*e+d*g)*j + (c*f+d*h)*l =
        c*(e*j+f*l) + d*(g*j+h*l)
      ring

theorem nativeGK4AVMul_leftUnit (u : NativeGK4AVValue) :
    nativeGK4AVMul nativeGK4AVOne u = u := by
  rcases u with ⟨⟨a,b⟩,⟨c,d⟩⟩
  simp [nativeGK4AVMul, nativeGK4AVOne]

theorem nativeGK4AVMul_rightUnit (u : NativeGK4AVValue) :
    nativeGK4AVMul u nativeGK4AVOne = u := by
  rcases u with ⟨⟨a,b⟩,⟨c,d⟩⟩
  simp [nativeGK4AVMul, nativeGK4AVOne]

/-- The actual F54 associator is neutral as a full polynomial matrix. -/
theorem nativeGK4AVCastForward :
    nativeGK4AVMul nativeGK4AVCast nativeGK4AVForward =
      nativeGK4AVOne := by
  simp [nativeGK4AVMul, nativeGK4AVCast,
    nativeGK4AVForward, nativeGK4AVOne]

section GenuineOriginalSource
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}

def KuuNativeF45Tree.RotationEdge.gk4avPolynomial
    {n m : Nat}
    {before after : KuuNativeF45Tree p n m ma pa mb pb}
    (edge : KuuNativeF45Tree.RotationEdge p before after) : NativeGK4AVValue :=
  match edge with
  | .forward _ => nativeGK4AVForward
  | .backward _ => nativeGK4AVBackward

def KuuNativeF45Tree.RotationChain.gk4avPolynomial
    {n m : Nat}
    {before after : KuuNativeF45Tree p n m ma pa mb pb} :
    KuuNativeF45Tree.RotationChain p before after → NativeGK4AVValue
  | .refl _ => nativeGK4AVOne
  | .snoc chain edge => nativeGK4AVMul chain.gk4avPolynomial edge.gk4avPolynomial

/-- Original dependent route, retaining both Nat axes and all contexts. -/
def KuuNativeF45Tree.DepthRotationRoute.gk4avPolynomial
    {n n' m m' : Nat}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (route : KuuNativeF45Tree.DepthRotationRoute p first last) : NativeGK4AVValue := by
  induction route with
  | chain path => exact path.gk4avPolynomial
  | castDepths _ _ _ => exact nativeGK4AVCast
  | trans _ _ ihLeft ihRight => exact nativeGK4AVMul ihLeft ihRight
  | leftContext _ _ ih => exact ih
  | rightContext _ _ ih => exact ih

theorem nativeGK4AV_trans
    {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
    {first : KuuNativeF45Tree p n₁ m₁ ma pa mb pb}
    {middle : KuuNativeF45Tree p n₂ m₂ ma pa mb pb}
    {last : KuuNativeF45Tree p n₃ m₃ ma pa mb pb}
    (u : KuuNativeF45Tree.DepthRotationRoute p first middle)
    (v : KuuNativeF45Tree.DepthRotationRoute p middle last) :
    (KuuNativeF45Tree.DepthRotationRoute.trans u v).gk4avPolynomial =
      nativeGK4AVMul u.gk4avPolynomial v.gk4avPolynomial := rfl

@[simp] theorem nativeGK4AV_leftContext
    {n n' m m' k l : Nat}
    {mc : KuuNativeBlocks a b} {pc : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (route : KuuNativeF45Tree.DepthRotationRoute p first last)
    (later : KuuNativeF45Tree p k l mb pb mc pc) :
    (KuuNativeF45Tree.DepthRotationRoute.leftContext route later).gk4avPolynomial =
      route.gk4avPolynomial := rfl

@[simp] theorem nativeGK4AV_rightContext
    {k l n n' m m' : Nat}
    {mc : KuuNativeBlocks a b} {pc : KuuNativeBlocks x y}
    (earlier : KuuNativeF45Tree p k l ma pa mb pb)
    {first : KuuNativeF45Tree p n m mb pb mc pc}
    {last : KuuNativeF45Tree p n' m' mb pb mc pc}
    (route : KuuNativeF45Tree.DepthRotationRoute p first last) :
    (KuuNativeF45Tree.DepthRotationRoute.rightContext earlier route).gk4avPolynomial =
      route.gk4avPolynomial := rfl

@[simp] theorem nativeGK4AV_assoc
    {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
    {p₀ p₁ p₂ p₃ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ q₃ : KuuNativeBlocks x y}
    (t₁ : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁)
    (t₂ : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂)
    (t₃ : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃) :
    (KuuNativeF45Tree.DepthRotationRoute.assoc t₁ t₂ t₃).gk4avPolynomial =
      nativeGK4AVOne := by
  change nativeGK4AVMul nativeGK4AVCast
    (nativeGK4AVMul nativeGK4AVOne nativeGK4AVForward) = nativeGK4AVOne
  rw [nativeGK4AVMul_leftUnit]
  exact nativeGK4AVCastForward

theorem nativeGK4AV_horizontal
    {n n' m m' k k' l l' : Nat}
    {p₀ p₁ p₂ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ : KuuNativeBlocks x y}
    {leftBefore : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
    {leftAfter : KuuNativeF45Tree p n' m' p₀ q₀ p₁ q₁}
    {rightBefore : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂}
    {rightAfter : KuuNativeF45Tree p k' l' p₁ q₁ p₂ q₂}
    (u : KuuNativeF45Tree.DepthRotationRoute p leftBefore leftAfter)
    (v : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter) :
    (nativeF54P90HorizontalRoute u v).gk4avPolynomial =
      nativeGK4AVMul u.gk4avPolynomial v.gk4avPolynomial := rfl

/-- Actual associator naturality uses only reassociation, never exchange. -/
theorem nativeGK4AV_assocNaturality
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
    (nativeF54P90AssocNaturalityLeftRoute u v w).gk4avPolynomial =
      (nativeF54P90AssocNaturalityRightRoute u v w).gk4avPolynomial := by
  simp only [nativeF54P90AssocNaturalityLeftRoute,
    nativeF54P90AssocNaturalityRightRoute, nativeGK4AV_trans,
    nativeGK4AV_horizontal, nativeGK4AV_assoc,
    nativeGK4AVMul_leftUnit, nativeGK4AVMul_rightUnit]
  exact nativeGK4AVMul_assoc u.gk4avPolynomial v.gk4avPolynomial w.gk4avPolynomial

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
theorem nativeGK4AV_original_sound
    (cell : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    r.gk4avPolynomial = s.gk4avPolynomial := by
  induction cell with
  | ident route => rfl
  | pentagon a b c d =>
      -- The raw F54 pentagon contains 3 vs 2 genuine associators.
      -- Its polynomial image sees the same ordered neutral factor.
      let v : NativeGK4AVValue :=
        nativeGK4AVMul nativeGK4AVCast
          (nativeGK4AVMul nativeGK4AVOne nativeGK4AVForward)
      change nativeGK4AVMul (nativeGK4AVMul v v) v =
        nativeGK4AVMul v v
      have hv : v = nativeGK4AVOne := by
        dsimp [v]
        rw [nativeGK4AVMul_leftUnit]
        exact nativeGK4AVCastForward
      simp only [hv, nativeGK4AVMul_leftUnit]
  | disjointSquare left right =>
      -- Each genuinely typed forward edge contributes ONE*F, irrespective
      -- of which physical context is rotated first.
      let v : NativeGK4AVValue :=
        nativeGK4AVMul nativeGK4AVOne nativeGK4AVForward
      change nativeGK4AVMul v v = nativeGK4AVMul v v
      rfl
  | symm cell ih => exact ih.symm
  | trans left right ihLeft ihRight => exact ihLeft.trans ihRight
  | leftContext cell later ih => exact ih
  | rightContext earlier cell ih => exact ih
  | precompose prior cell ih =>
      simp only [nativeGK4AV_trans]
      exact congrArg (nativeGK4AVMul prior.gk4avPolynomial) ih
  | postcompose cell suffix ih =>
      simp only [nativeGK4AV_trans]
      exact congrArg (fun x => nativeGK4AVMul x suffix.gk4avPolynomial) ih

/-- All nine actual original P92B constructors. -/
theorem nativeGK4AV_p92_sound
    (cell : NativeF55P92AssocComparison p r s) :
    r.gk4avPolynomial = s.gk4avPolynomial := by
  induction cell with
  | original old => exact nativeGK4AV_original_sound old
  | assocNaturality u v w => exact nativeGK4AV_assocNaturality u v w
  | refl route => rfl
  | symm cell ih => exact ih.symm
  | trans left right ihLeft ihRight => exact ihLeft.trans ihRight
  | leftContext cell later ih => exact ih
  | rightContext earlier cell ih => exact ih
  | precompose prior cell ih =>
      simp only [nativeGK4AV_trans]
      exact congrArg (nativeGK4AVMul prior.gk4avPolynomial) ih
  | postcompose cell suffix ih =>
      simp only [nativeGK4AV_trans]
      exact congrArg (fun x => nativeGK4AVMul x suffix.gk4avPolynomial) ih

/-- All fourteen independent structural seam constructors. -/
theorem nativeGK4AV_seam_sound
    (seam : NativeF54StructuralSeam p r s) :
    r.gk4avPolynomial = s.gk4avPolynomial := by
  induction seam with
  | refl route => rfl
  | symm seam ih => exact ih.symm
  | trans left right ihLeft ihRight => exact ihLeft.trans ihRight
  | reassoc u v w =>
      simp only [nativeGK4AV_trans]
      exact nativeGK4AVMul_assoc _ _ _
  | leftUnit route =>
      simp only [nativeGK4AV_trans]
      change nativeGK4AVMul nativeGK4AVOne route.gk4avPolynomial = route.gk4avPolynomial
      exact nativeGK4AVMul_leftUnit _
  | rightUnit route =>
      simp only [nativeGK4AV_trans]
      change nativeGK4AVMul route.gk4avPolynomial nativeGK4AVOne = route.gk4avPolynomial
      exact nativeGK4AVMul_rightUnit _
  | precompose prior seam ih =>
      simp only [nativeGK4AV_trans]
      exact congrArg (nativeGK4AVMul prior.gk4avPolynomial) ih
  | postcompose seam suffix ih =>
      simp only [nativeGK4AV_trans]
      exact congrArg (fun x => nativeGK4AVMul x suffix.gk4avPolynomial) ih
  | leftContextTrans u v later =>
      simp only [nativeGK4AV_leftContext, nativeGK4AV_trans]
  | rightContextTrans earlier u v =>
      simp only [nativeGK4AV_rightContext, nativeGK4AV_trans]
  | leftContextUnit earlier later => rfl
  | rightContextUnit earlier later => rfl
  | leftContextCongruence seam later ih => exact ih
  | rightContextCongruence earlier seam ih => exact ih

/-- All three extended structural comparison constructors. -/
theorem nativeGK4AV_structural_sound
    (cell : NativeF55StructuralComparison p r s) :
    r.gk4avPolynomial = s.gk4avPolynomial := by
  induction cell with
  | original old => exact nativeGK4AV_p92_sound old
  | structural seam => exact nativeGK4AV_seam_sound seam
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

def nativeGK4AVP92Value :
    NativeF55P92AssocRouteClasses first middle → NativeGK4AVValue :=
  _root_.Quotient.lift
    (fun raw : KuuNativeF45Tree.DepthRotationRoute p first middle => raw.gk4avPolynomial)
    (by
      intro r s h
      rcases h with ⟨cell⟩
      exact nativeGK4AV_p92_sound cell)

def nativeGK4AVStructuralValue :
    NativeGK4EStructuralRouteClasses first middle → NativeGK4AVValue :=
  _root_.Quotient.lift
    (fun raw : KuuNativeF45Tree.DepthRotationRoute p first middle => raw.gk4avPolynomial)
    (by
      intro r s h
      rcases h with ⟨cell⟩
      exact nativeGK4AV_structural_sound cell)

@[simp] theorem nativeGK4AVP92Value_class
    (raw : KuuNativeF45Tree.DepthRotationRoute p first middle) :
    nativeGK4AVP92Value first middle (nativeF55P92AssocRouteClass first middle raw) =
      raw.gk4avPolynomial := rfl

@[simp] theorem nativeGK4AVStructuralValue_class
    (raw : KuuNativeF45Tree.DepthRotationRoute p first middle) :
    nativeGK4AVStructuralValue first middle
      (nativeGK4EStructuralRouteClass first middle raw) = raw.gk4avPolynomial := rfl

theorem nativeGK4AV_commutes
    (q : NativeF55P92AssocRouteClasses first middle) :
    nativeGK4AVStructuralValue first middle
      (nativeGK4EP92ToStructural first middle q) = nativeGK4AVP92Value first middle q := by
  refine _root_.Quotient.inductionOn q ?_
  intro raw
  rfl

theorem nativeGK4AVStructural_compose
    (u : NativeGK4EStructuralRouteClasses first middle)
    (v : NativeGK4EStructuralRouteClasses middle last) :
    nativeGK4AVStructuralValue first last
      (nativeGK4H_structuralCompose first middle last u v) =
    nativeGK4AVMul (nativeGK4AVStructuralValue first middle u)
      (nativeGK4AVStructuralValue middle last v) := by
  refine _root_.Quotient.inductionOn₂ u v ?_
  intro rawU rawV
  exact nativeGK4AV_trans rawU rawV

@[simp] theorem nativeGK4AVStructural_unit :
    nativeGK4AVStructuralValue first first (nativeGK4H_structuralUnit first) =
      nativeGK4AVOne := rfl

end GenuineQuotientDescent

#print axioms NativeGK4AVValue
#print axioms nativeGK4AVMul
#print axioms nativeGK4AVOne
#print axioms nativeGK4AVCast
#print axioms nativeGK4AVForward
#print axioms nativeGK4AVBackward
#print axioms nativeGK4AVMul_assoc
#print axioms nativeGK4AVMul_leftUnit
#print axioms nativeGK4AVMul_rightUnit
#print axioms nativeGK4AVCastForward
#print axioms KuuNativeF45Tree.RotationEdge.gk4avPolynomial
#print axioms KuuNativeF45Tree.RotationChain.gk4avPolynomial
#print axioms KuuNativeF45Tree.DepthRotationRoute.gk4avPolynomial
#print axioms nativeGK4AV_trans
#print axioms nativeGK4AV_leftContext
#print axioms nativeGK4AV_rightContext
#print axioms nativeGK4AV_assoc
#print axioms nativeGK4AV_horizontal
#print axioms nativeGK4AV_assocNaturality
#print axioms nativeGK4AV_original_sound
#print axioms nativeGK4AV_p92_sound
#print axioms nativeGK4AV_seam_sound
#print axioms nativeGK4AV_structural_sound
#print axioms nativeGK4AVP92Value
#print axioms nativeGK4AVStructuralValue
#print axioms nativeGK4AVP92Value_class
#print axioms nativeGK4AVStructuralValue_class
#print axioms nativeGK4AV_commutes
#print axioms nativeGK4AVStructural_compose
#print axioms nativeGK4AVStructural_unit

end
end Kuu.F112.Physical
