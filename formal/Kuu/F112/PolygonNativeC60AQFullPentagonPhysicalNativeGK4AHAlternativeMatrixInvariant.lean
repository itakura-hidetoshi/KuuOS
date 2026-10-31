import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4AGForgetful
import Mathlib.Tactic

/-!
F112-P94D3GK4AH — an independent noncommutative integer 2x2 history
representation of ACTUAL original F54 typed source, distinct from
GK4AF's previous representation and from GK4AG's joint observer.
  C  = [[1, 1],[0, 1]]   (true double Nat cast)
  F  = [[1,-1],[0, 1]]   (true forward rotation)
  R4 = [[1, 0],[4, 1]]   (true backward rotation evaluated differently)
  C*F = I              (true original associator)

Unlike the GK4AF matrix, B=F*R4 has infinite order, allowing detection
of residual SAME-(four-coordinate, old-matrix) collisions. The new map
preserves all REAL original F55 9, P92B 9, structural seams 14 and
extended comparison 3 Type-valued constructors, separately descends
to actual Q and S, and preserves S composition and units. No inference
of a Type-valued source 3-cell from observed equality, no Q category
axioms, no Gray and no hyperdescent.

Append-only/tighten-only/same-root 107, strict 空 central, independent
Kuu a presentation; protected #1558 Draft/OPEN/unmerged.
Lean v4.30.0-rc2, pinned mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
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

/-- Fully explicit 2×2 integer matrix, avoiding any hidden quotient
or invented original proof comparison. -/
abbrev NativeGK4AHMatrix := (Int × Int) × (Int × Int)

/-- Genuine matrix multiplication, not commutative word-count addition. -/
def nativeGK4AHMul (u v : NativeGK4AHMatrix) : NativeGK4AHMatrix :=
  ((u.1.1 * v.1.1 + u.1.2 * v.2.1,
    u.1.1 * v.1.2 + u.1.2 * v.2.2),
   (u.2.1 * v.1.1 + u.2.2 * v.2.1,
    u.2.1 * v.1.2 + u.2.2 * v.2.2))

def nativeGK4AHOne : NativeGK4AHMatrix := ((1, 0), (0, 1))
def nativeGK4AHCast : NativeGK4AHMatrix := ((1, 1), (0, 1))
def nativeGK4AHForward : NativeGK4AHMatrix := ((1, -1), (0, 1))
def nativeGK4AHBackward : NativeGK4AHMatrix := ((1, 0), (4, 1))

/-- Associativity is proved by FOUR exact ring identities on entries. -/
theorem nativeGK4AHMul_assoc (u v w : NativeGK4AHMatrix) :
    nativeGK4AHMul (nativeGK4AHMul u v) w =
      nativeGK4AHMul u (nativeGK4AHMul v w) := by
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

theorem nativeGK4AHMul_leftUnit (u : NativeGK4AHMatrix) :
    nativeGK4AHMul nativeGK4AHOne u = u := by
  rcases u with ⟨⟨a,b⟩,⟨c,d⟩⟩
  simp [nativeGK4AHMul, nativeGK4AHOne]

theorem nativeGK4AHMul_rightUnit (u : NativeGK4AHMatrix) :
    nativeGK4AHMul u nativeGK4AHOne = u := by
  rcases u with ⟨⟨a,b⟩,⟨c,d⟩⟩
  simp [nativeGK4AHMul, nativeGK4AHOne]

/-- REAL F54 assoc has the honest original double-axis cast followed
by a real forward LocalRotation; their matrix product is identity. -/
theorem nativeGK4AHCastForward :
    nativeGK4AHMul nativeGK4AHCast nativeGK4AHForward =
      nativeGK4AHOne := by decide

section GenuineOriginalSource
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}

/-- The ACTUAL oriented F54 rotation-edge constructor is inspected,
including the original LocalRotation Type-valued witness. -/
def KuuNativeF45Tree.RotationEdge.gk4ahMatrix
    {n m : Nat}
    {before after : KuuNativeF45Tree p n m ma pa mb pb}
    (edge : KuuNativeF45Tree.RotationEdge p before after) :
    NativeGK4AHMatrix :=
  match edge with
  | .forward _ => nativeGK4AHForward
  | .backward _ => nativeGK4AHBackward

/-- Intermediate-tree preserving genuine F54 original RotationChain. -/
def KuuNativeF45Tree.RotationChain.gk4ahMatrix
    {n m : Nat}
    {before after : KuuNativeF45Tree p n m ma pa mb pb} :
    KuuNativeF45Tree.RotationChain p before after → NativeGK4AHMatrix
  | .refl _ => nativeGK4AHOne
  | .snoc chain edge =>
      nativeGK4AHMul chain.gk4ahMatrix edge.gk4ahMatrix

/-- Every original F54 source constructor is counted directly.
Both dependent Nat casts are ONE original cast history symbol;
typed source contexts preserve the ordered history. -/
def KuuNativeF45Tree.DepthRotationRoute.gk4ahMatrix
    {n n' m m' : Nat}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (route : KuuNativeF45Tree.DepthRotationRoute p first last) :
    NativeGK4AHMatrix := by
  induction route with
  | chain path => exact path.gk4ahMatrix
  | castDepths _ _ _ => exact nativeGK4AHCast
  | trans _ _ ihLeft ihRight =>
      exact nativeGK4AHMul ihLeft ihRight
  | leftContext _ _ ih => exact ih
  | rightContext _ _ ih => exact ih

theorem nativeGK4AH_trans
    {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
    {first : KuuNativeF45Tree p n₁ m₁ ma pa mb pb}
    {middle : KuuNativeF45Tree p n₂ m₂ ma pa mb pb}
    {last : KuuNativeF45Tree p n₃ m₃ ma pa mb pb}
    (u : KuuNativeF45Tree.DepthRotationRoute p first middle)
    (v : KuuNativeF45Tree.DepthRotationRoute p middle last) :
    (KuuNativeF45Tree.DepthRotationRoute.trans u v).gk4ahMatrix =
      nativeGK4AHMul u.gk4ahMatrix v.gk4ahMatrix := rfl

@[simp] theorem nativeGK4AH_leftContext
    {n n' m m' k l : Nat}
    {mc : KuuNativeBlocks a b} {pc : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (route : KuuNativeF45Tree.DepthRotationRoute p first last)
    (later : KuuNativeF45Tree p k l mb pb mc pc) :
    (KuuNativeF45Tree.DepthRotationRoute.leftContext route later).gk4ahMatrix =
      route.gk4ahMatrix := rfl

@[simp] theorem nativeGK4AH_rightContext
    {k l n n' m m' : Nat}
    {mc : KuuNativeBlocks a b} {pc : KuuNativeBlocks x y}
    (earlier : KuuNativeF45Tree p k l ma pa mb pb)
    {first : KuuNativeF45Tree p n m mb pb mc pc}
    {last : KuuNativeF45Tree p n' m' mb pb mc pc}
    (route : KuuNativeF45Tree.DepthRotationRoute p first last) :
    (KuuNativeF45Tree.DepthRotationRoute.rightContext earlier route).gk4ahMatrix =
      route.gk4ahMatrix := rfl

@[simp] theorem nativeGK4AH_assoc
    {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
    {p₀ p₁ p₂ p₃ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ q₃ : KuuNativeBlocks x y}
    (t₁ : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁)
    (t₂ : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂)
    (t₃ : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃) :
    (KuuNativeF45Tree.DepthRotationRoute.assoc t₁ t₂ t₃).gk4ahMatrix =
      nativeGK4AHOne := by
  exact nativeGK4AHCastForward

/-- All two-context horizontal paths read the original histories in
the TRUE left-to-right order and NOT in the opposite order. -/
theorem nativeGK4AH_horizontal
    {n n' m m' k k' l l' : Nat}
    {p₀ p₁ p₂ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ : KuuNativeBlocks x y}
    {leftBefore : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
    {leftAfter : KuuNativeF45Tree p n' m' p₀ q₀ p₁ q₁}
    {rightBefore : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂}
    {rightAfter : KuuNativeF45Tree p k' l' p₁ q₁ p₂ q₂}
    (u : KuuNativeF45Tree.DepthRotationRoute p leftBefore leftAfter)
    (v : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter) :
    (nativeF54P90HorizontalRoute u v).gk4ahMatrix =
      nativeGK4AHMul u.gk4ahMatrix v.gk4ahMatrix := by
  rfl

/-- Associator-naturality soundness is NONCOMMUTATIVE: no arbitrary
reordering of u/v/w; only reassociation of the exact same order,
with a genuine value-neutral source/target associator. -/
theorem nativeGK4AH_assocNaturality
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
    (nativeF54P90AssocNaturalityLeftRoute u v w).gk4ahMatrix =
      (nativeF54P90AssocNaturalityRightRoute u v w).gk4ahMatrix := by
  simp only [nativeF54P90AssocNaturalityLeftRoute,
    nativeF54P90AssocNaturalityRightRoute, nativeGK4AH_trans,
    nativeGK4AH_horizontal, nativeGK4AH_assoc,
    nativeGK4AHMul_leftUnit, nativeGK4AHMul_rightUnit]
  exact nativeGK4AHMul_assoc u.gk4ahMatrix v.gk4ahMatrix w.gk4ahMatrix

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
theorem nativeGK4AH_original_sound
    (cell : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    r.gk4ahMatrix = s.gk4ahMatrix := by
  induction cell with
  | ident route => rfl
  | pentagon a b c d =>
      change nativeGK4AHOne = nativeGK4AHOne
      rfl
  | disjointSquare left right =>
      change
        nativeGK4AHMul nativeGK4AHForward nativeGK4AHForward =
          nativeGK4AHMul nativeGK4AHForward nativeGK4AHForward
      rfl
  | symm cell ih => exact ih.symm
  | trans left right ihLeft ihRight => exact ihLeft.trans ihRight
  | leftContext cell later ih => exact ih
  | rightContext earlier cell ih => exact ih
  | precompose prior cell ih =>
      simp only [nativeGK4AH_trans]
      exact congrArg (nativeGK4AHMul prior.gk4ahMatrix) ih
  | postcompose cell suffix ih =>
      simp only [nativeGK4AH_trans]
      exact congrArg (fun x => nativeGK4AHMul x suffix.gk4ahMatrix) ih

/-- ALL NINE original typed P92B comparison constructors. -/
theorem nativeGK4AH_p92_sound
    (cell : NativeF55P92AssocComparison p r s) :
    r.gk4ahMatrix = s.gk4ahMatrix := by
  induction cell with
  | original old => exact nativeGK4AH_original_sound old
  | assocNaturality u v w => exact nativeGK4AH_assocNaturality u v w
  | refl route => rfl
  | symm cell ih => exact ih.symm
  | trans left right ihLeft ihRight => exact ihLeft.trans ihRight
  | leftContext cell later ih => exact ih
  | rightContext earlier cell ih => exact ih
  | precompose prior cell ih =>
      simp only [nativeGK4AH_trans]
      exact congrArg (nativeGK4AHMul prior.gk4ahMatrix) ih
  | postcompose cell suffix ih =>
      simp only [nativeGK4AH_trans]
      exact congrArg (fun x => nativeGK4AHMul x suffix.gk4ahMatrix) ih

/-- ALL FOURTEEN original independent structural seam constructors. -/
theorem nativeGK4AH_seam_sound
    (seam : NativeF54StructuralSeam p r s) :
    r.gk4ahMatrix = s.gk4ahMatrix := by
  induction seam with
  | refl route => rfl
  | symm seam ih => exact ih.symm
  | trans left right ihLeft ihRight => exact ihLeft.trans ihRight
  | reassoc u v w =>
      simp only [nativeGK4AH_trans]
      exact nativeGK4AHMul_assoc _ _ _
  | leftUnit route =>
      simp only [nativeGK4AH_trans]
      change nativeGK4AHMul nativeGK4AHOne route.gk4ahMatrix =
        route.gk4ahMatrix
      exact nativeGK4AHMul_leftUnit _
  | rightUnit route =>
      simp only [nativeGK4AH_trans]
      change nativeGK4AHMul route.gk4ahMatrix nativeGK4AHOne =
        route.gk4ahMatrix
      exact nativeGK4AHMul_rightUnit _
  | precompose prior seam ih =>
      simp only [nativeGK4AH_trans]
      exact congrArg (nativeGK4AHMul prior.gk4ahMatrix) ih
  | postcompose seam suffix ih =>
      simp only [nativeGK4AH_trans]
      exact congrArg (fun x => nativeGK4AHMul x suffix.gk4ahMatrix) ih
  | leftContextTrans u v later =>
      simp only [nativeGK4AH_leftContext, nativeGK4AH_trans]
  | rightContextTrans earlier u v =>
      simp only [nativeGK4AH_rightContext, nativeGK4AH_trans]
  | leftContextUnit earlier later => rfl
  | rightContextUnit earlier later => rfl
  | leftContextCongruence seam later ih => exact ih
  | rightContextCongruence earlier seam ih => exact ih

/-- ALL THREE extended structural comparison constructors. -/
theorem nativeGK4AH_structural_sound
    (cell : NativeF55StructuralComparison p r s) :
    r.gk4ahMatrix = s.gk4ahMatrix := by
  induction cell with
  | original old => exact nativeGK4AH_p92_sound old
  | structural seam => exact nativeGK4AH_seam_sound seam
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
def nativeGK4AHP92Value :
    NativeF55P92AssocRouteClasses first middle → NativeGK4AHMatrix :=
  _root_.Quotient.lift
    (fun raw : KuuNativeF45Tree.DepthRotationRoute p first middle =>
      raw.gk4ahMatrix)
    (by
      intro r s h
      rcases h with ⟨cell⟩
      exact nativeGK4AH_p92_sound cell)

/-- INDEPENDENT descent to the structural quotient S: F54 seams are
real added comparisons, not implicit P92B 3-cell constructors. -/
def nativeGK4AHStructuralValue :
    NativeGK4EStructuralRouteClasses first middle → NativeGK4AHMatrix :=
  _root_.Quotient.lift
    (fun raw : KuuNativeF45Tree.DepthRotationRoute p first middle =>
      raw.gk4ahMatrix)
    (by
      intro r s h
      rcases h with ⟨cell⟩
      exact nativeGK4AH_structural_sound cell)

@[simp] theorem nativeGK4AHP92Value_class
    (raw : KuuNativeF45Tree.DepthRotationRoute p first middle) :
    nativeGK4AHP92Value first middle
        (nativeF55P92AssocRouteClass first middle raw) =
      raw.gk4ahMatrix := rfl

@[simp] theorem nativeGK4AHStructuralValue_class
    (raw : KuuNativeF45Tree.DepthRotationRoute p first middle) :
    nativeGK4AHStructuralValue first middle
        (nativeGK4EStructuralRouteClass first middle raw) =
      raw.gk4ahMatrix := rfl

theorem nativeGK4AH_commutes
    (q : NativeF55P92AssocRouteClasses first middle) :
    nativeGK4AHStructuralValue first middle
        (nativeGK4EP92ToStructural first middle q) =
      nativeGK4AHP92Value first middle q := by
  refine _root_.Quotient.inductionOn q ?_
  intro raw
  rfl

theorem nativeGK4AHStructural_compose
    (u : NativeGK4EStructuralRouteClasses first middle)
    (v : NativeGK4EStructuralRouteClasses middle last) :
    nativeGK4AHStructuralValue first last
        (nativeGK4H_structuralCompose first middle last u v) =
      nativeGK4AHMul
        (nativeGK4AHStructuralValue first middle u)
        (nativeGK4AHStructuralValue middle last v) := by
  refine _root_.Quotient.inductionOn u ?_
  intro rawU
  refine _root_.Quotient.inductionOn v ?_
  intro rawV
  exact nativeGK4AH_trans rawU rawV

@[simp] theorem nativeGK4AHStructural_unit :
    nativeGK4AHStructuralValue first first
      (nativeGK4H_structuralUnit first) = nativeGK4AHOne := rfl

end GenuineQuotientDescent

#print axioms NativeGK4AHMatrix
#print axioms nativeGK4AHMul
#print axioms nativeGK4AHOne
#print axioms nativeGK4AHCast
#print axioms nativeGK4AHForward
#print axioms nativeGK4AHBackward
#print axioms nativeGK4AHMul_assoc
#print axioms nativeGK4AHMul_leftUnit
#print axioms nativeGK4AHMul_rightUnit
#print axioms nativeGK4AHCastForward
#print axioms KuuNativeF45Tree.RotationEdge.gk4ahMatrix
#print axioms KuuNativeF45Tree.RotationChain.gk4ahMatrix
#print axioms KuuNativeF45Tree.DepthRotationRoute.gk4ahMatrix
#print axioms nativeGK4AH_trans
#print axioms nativeGK4AH_leftContext
#print axioms nativeGK4AH_rightContext
#print axioms nativeGK4AH_assoc
#print axioms nativeGK4AH_horizontal
#print axioms nativeGK4AH_assocNaturality
#print axioms nativeGK4AH_original_sound
#print axioms nativeGK4AH_p92_sound
#print axioms nativeGK4AH_seam_sound
#print axioms nativeGK4AH_structural_sound
#print axioms nativeGK4AHP92Value
#print axioms nativeGK4AHStructuralValue
#print axioms nativeGK4AHP92Value_class
#print axioms nativeGK4AHStructuralValue_class
#print axioms nativeGK4AH_commutes
#print axioms nativeGK4AHStructural_compose
#print axioms nativeGK4AHStructural_unit

end
end Kuu.F112.Physical
