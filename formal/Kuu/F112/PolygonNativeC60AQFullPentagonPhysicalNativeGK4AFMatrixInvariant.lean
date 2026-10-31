import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4AEKernelForgetful
import Mathlib.Tactic

/-!
F112-P94D3GK4AF — a genuine higher-order NONCOMMUTATIVE original F54
history invariant in the integer 2-by-2 matrix monoid.

This is a PROOF-RELEVANT SOURCE OBSERVATION of original F54
bidirectional typed RotationEdges, independent double-Nat casts,
every intermediate-tree RotationChain, route trans and both contexts.
The genuine original F54 associator is ONE CAST followed by ONE
FORWARD rotation, represented exactly by C*F=identity.
The F55 pentagon and the disjoint square, ALL original F55 9
constructors, original P92B 9 constructors including TRUE
associator-naturality, all structural 14 seams, and all three
extended comparison constructors are checked individually.

The original P92B proof-existence quotient Q and independently
generated structural quotient S receive SEPARATE well-defined
matrix observations and a commuting Q->S comparison.
This does NOT manufacture a Type-valued original P92B 3-cell from
an observed equality, nor assume original Q category laws, Gray,
historical full typed equivalence or hyperdescent.
Append-only / tighten-only / same-root 107; protected #1558
Draft/open/unmerged. Strict 空 central, independent Kuu one
presentation. Lean v4.30.0-rc2, mathlib pinned
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
abbrev NativeGK4AFMatrix := (Int × Int) × (Int × Int)

/-- Genuine matrix multiplication, not commutative word-count addition. -/
def nativeGK4AFMul (u v : NativeGK4AFMatrix) : NativeGK4AFMatrix :=
  ((u.1.1 * v.1.1 + u.1.2 * v.2.1,
    u.1.1 * v.1.2 + u.1.2 * v.2.2),
   (u.2.1 * v.1.1 + u.2.2 * v.2.1,
    u.2.1 * v.1.2 + u.2.2 * v.2.2))

def nativeGK4AFOne : NativeGK4AFMatrix := ((1, 0), (0, 1))
def nativeGK4AFCast : NativeGK4AFMatrix := ((1, 1), (0, 1))
def nativeGK4AFForward : NativeGK4AFMatrix := ((1, -1), (0, 1))
def nativeGK4AFBackward : NativeGK4AFMatrix := ((1, 0), (1, 1))

/-- Associativity is proved by FOUR exact ring identities on entries. -/
theorem nativeGK4AFMul_assoc (u v w : NativeGK4AFMatrix) :
    nativeGK4AFMul (nativeGK4AFMul u v) w =
      nativeGK4AFMul u (nativeGK4AFMul v w) := by
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

theorem nativeGK4AFMul_leftUnit (u : NativeGK4AFMatrix) :
    nativeGK4AFMul nativeGK4AFOne u = u := by
  rcases u with ⟨⟨a,b⟩,⟨c,d⟩⟩
  simp [nativeGK4AFMul, nativeGK4AFOne]

theorem nativeGK4AFMul_rightUnit (u : NativeGK4AFMatrix) :
    nativeGK4AFMul u nativeGK4AFOne = u := by
  rcases u with ⟨⟨a,b⟩,⟨c,d⟩⟩
  simp [nativeGK4AFMul, nativeGK4AFOne]

/-- REAL F54 assoc has the honest original double-axis cast followed
by a real forward LocalRotation; their matrix product is identity. -/
theorem nativeGK4AFCastForward :
    nativeGK4AFMul nativeGK4AFCast nativeGK4AFForward =
      nativeGK4AFOne := by decide

section GenuineOriginalSource
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}

/-- The ACTUAL oriented F54 rotation-edge constructor is inspected,
including the original LocalRotation Type-valued witness. -/
def KuuNativeF45Tree.RotationEdge.gk4afMatrix
    {n m : Nat}
    {before after : KuuNativeF45Tree p n m ma pa mb pb}
    (edge : KuuNativeF45Tree.RotationEdge p before after) :
    NativeGK4AFMatrix :=
  match edge with
  | .forward _ => nativeGK4AFForward
  | .backward _ => nativeGK4AFBackward

/-- Intermediate-tree preserving genuine F54 original RotationChain. -/
def KuuNativeF45Tree.RotationChain.gk4afMatrix
    {n m : Nat}
    {before after : KuuNativeF45Tree p n m ma pa mb pb} :
    KuuNativeF45Tree.RotationChain p before after → NativeGK4AFMatrix
  | .refl _ => nativeGK4AFOne
  | .snoc chain edge =>
      nativeGK4AFMul chain.gk4afMatrix edge.gk4afMatrix

/-- Every original F54 source constructor is counted directly.
Both dependent Nat casts are ONE original cast history symbol;
typed source contexts preserve the ordered history. -/
def KuuNativeF45Tree.DepthRotationRoute.gk4afMatrix
    {n n' m m' : Nat}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (route : KuuNativeF45Tree.DepthRotationRoute p first last) :
    NativeGK4AFMatrix := by
  induction route with
  | chain path => exact path.gk4afMatrix
  | castDepths _ _ _ => exact nativeGK4AFCast
  | trans _ _ ihLeft ihRight =>
      exact nativeGK4AFMul ihLeft ihRight
  | leftContext _ _ ih => exact ih
  | rightContext _ _ ih => exact ih

theorem nativeGK4AF_trans
    {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
    {first : KuuNativeF45Tree p n₁ m₁ ma pa mb pb}
    {middle : KuuNativeF45Tree p n₂ m₂ ma pa mb pb}
    {last : KuuNativeF45Tree p n₃ m₃ ma pa mb pb}
    (u : KuuNativeF45Tree.DepthRotationRoute p first middle)
    (v : KuuNativeF45Tree.DepthRotationRoute p middle last) :
    (KuuNativeF45Tree.DepthRotationRoute.trans u v).gk4afMatrix =
      nativeGK4AFMul u.gk4afMatrix v.gk4afMatrix := rfl

@[simp] theorem nativeGK4AF_leftContext
    {n n' m m' k l : Nat}
    {mc : KuuNativeBlocks a b} {pc : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (route : KuuNativeF45Tree.DepthRotationRoute p first last)
    (later : KuuNativeF45Tree p k l mb pb mc pc) :
    (KuuNativeF45Tree.DepthRotationRoute.leftContext route later).gk4afMatrix =
      route.gk4afMatrix := rfl

@[simp] theorem nativeGK4AF_rightContext
    {k l n n' m m' : Nat}
    {mc : KuuNativeBlocks a b} {pc : KuuNativeBlocks x y}
    (earlier : KuuNativeF45Tree p k l ma pa mb pb)
    {first : KuuNativeF45Tree p n m mb pb mc pc}
    {last : KuuNativeF45Tree p n' m' mb pb mc pc}
    (route : KuuNativeF45Tree.DepthRotationRoute p first last) :
    (KuuNativeF45Tree.DepthRotationRoute.rightContext earlier route).gk4afMatrix =
      route.gk4afMatrix := rfl

@[simp] theorem nativeGK4AF_assoc
    {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
    {p₀ p₁ p₂ p₃ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ q₃ : KuuNativeBlocks x y}
    (t₁ : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁)
    (t₂ : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂)
    (t₃ : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃) :
    (KuuNativeF45Tree.DepthRotationRoute.assoc t₁ t₂ t₃).gk4afMatrix =
      nativeGK4AFOne := by
  exact nativeGK4AFCastForward

/-- All two-context horizontal paths read the original histories in
the TRUE left-to-right order and NOT in the opposite order. -/
theorem nativeGK4AF_horizontal
    {n n' m m' k k' l l' : Nat}
    {p₀ p₁ p₂ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ : KuuNativeBlocks x y}
    {leftBefore : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
    {leftAfter : KuuNativeF45Tree p n' m' p₀ q₀ p₁ q₁}
    {rightBefore : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂}
    {rightAfter : KuuNativeF45Tree p k' l' p₁ q₁ p₂ q₂}
    (u : KuuNativeF45Tree.DepthRotationRoute p leftBefore leftAfter)
    (v : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter) :
    (nativeF54P90HorizontalRoute u v).gk4afMatrix =
      nativeGK4AFMul u.gk4afMatrix v.gk4afMatrix := by
  rfl

/-- Associator-naturality soundness is NONCOMMUTATIVE: no arbitrary
reordering of u/v/w; only reassociation of the exact same order,
with a genuine value-neutral source/target associator. -/
theorem nativeGK4AF_assocNaturality
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
    (nativeF54P90AssocNaturalityLeftRoute u v w).gk4afMatrix =
      (nativeF54P90AssocNaturalityRightRoute u v w).gk4afMatrix := by
  simp only [nativeF54P90AssocNaturalityLeftRoute,
    nativeF54P90AssocNaturalityRightRoute, nativeGK4AF_trans,
    nativeGK4AF_horizontal, nativeGK4AF_assoc,
    nativeGK4AFMul_leftUnit, nativeGK4AFMul_rightUnit]
  exact nativeGK4AFMul_assoc u.gk4afMatrix v.gk4afMatrix w.gk4afMatrix

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
theorem nativeGK4AF_original_sound
    (cell : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    r.gk4afMatrix = s.gk4afMatrix := by
  induction cell with
  | ident route => rfl
  | pentagon a b c d =>
      change nativeGK4AFOne = nativeGK4AFOne
      rfl
  | disjointSquare left right =>
      change
        nativeGK4AFMul nativeGK4AFForward nativeGK4AFForward =
          nativeGK4AFMul nativeGK4AFForward nativeGK4AFForward
      rfl
  | symm cell ih => exact ih.symm
  | trans left right ihLeft ihRight => exact ihLeft.trans ihRight
  | leftContext cell later ih => exact ih
  | rightContext earlier cell ih => exact ih
  | precompose prior cell ih =>
      simp only [nativeGK4AF_trans]
      exact congrArg (nativeGK4AFMul prior.gk4afMatrix) ih
  | postcompose cell suffix ih =>
      simp only [nativeGK4AF_trans]
      exact congrArg (fun x => nativeGK4AFMul x suffix.gk4afMatrix) ih

/-- ALL NINE original typed P92B comparison constructors. -/
theorem nativeGK4AF_p92_sound
    (cell : NativeF55P92AssocComparison p r s) :
    r.gk4afMatrix = s.gk4afMatrix := by
  induction cell with
  | original old => exact nativeGK4AF_original_sound old
  | assocNaturality u v w => exact nativeGK4AF_assocNaturality u v w
  | refl route => rfl
  | symm cell ih => exact ih.symm
  | trans left right ihLeft ihRight => exact ihLeft.trans ihRight
  | leftContext cell later ih => exact ih
  | rightContext earlier cell ih => exact ih
  | precompose prior cell ih =>
      simp only [nativeGK4AF_trans]
      exact congrArg (nativeGK4AFMul prior.gk4afMatrix) ih
  | postcompose cell suffix ih =>
      simp only [nativeGK4AF_trans]
      exact congrArg (fun x => nativeGK4AFMul x suffix.gk4afMatrix) ih

/-- ALL FOURTEEN original independent structural seam constructors. -/
theorem nativeGK4AF_seam_sound
    (seam : NativeF54StructuralSeam p r s) :
    r.gk4afMatrix = s.gk4afMatrix := by
  induction seam with
  | refl route => rfl
  | symm seam ih => exact ih.symm
  | trans left right ihLeft ihRight => exact ihLeft.trans ihRight
  | reassoc u v w =>
      simp only [nativeGK4AF_trans]
      exact nativeGK4AFMul_assoc _ _ _
  | leftUnit route =>
      simp only [nativeGK4AF_trans]
      change nativeGK4AFMul nativeGK4AFOne route.gk4afMatrix =
        route.gk4afMatrix
      exact nativeGK4AFMul_leftUnit _
  | rightUnit route =>
      simp only [nativeGK4AF_trans]
      change nativeGK4AFMul route.gk4afMatrix nativeGK4AFOne =
        route.gk4afMatrix
      exact nativeGK4AFMul_rightUnit _
  | precompose prior seam ih =>
      simp only [nativeGK4AF_trans]
      exact congrArg (nativeGK4AFMul prior.gk4afMatrix) ih
  | postcompose seam suffix ih =>
      simp only [nativeGK4AF_trans]
      exact congrArg (fun x => nativeGK4AFMul x suffix.gk4afMatrix) ih
  | leftContextTrans u v later =>
      simp only [nativeGK4AF_leftContext, nativeGK4AF_trans]
  | rightContextTrans earlier u v =>
      simp only [nativeGK4AF_rightContext, nativeGK4AF_trans]
  | leftContextUnit earlier later => rfl
  | rightContextUnit earlier later => rfl
  | leftContextCongruence seam later ih => exact ih
  | rightContextCongruence earlier seam ih => exact ih

/-- ALL THREE extended structural comparison constructors. -/
theorem nativeGK4AF_structural_sound
    (cell : NativeF55StructuralComparison p r s) :
    r.gk4afMatrix = s.gk4afMatrix := by
  induction cell with
  | original old => exact nativeGK4AF_p92_sound old
  | structural seam => exact nativeGK4AF_seam_sound seam
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
def nativeGK4AFP92Value :
    NativeF55P92AssocRouteClasses first middle → NativeGK4AFMatrix :=
  _root_.Quotient.lift
    (fun raw : KuuNativeF45Tree.DepthRotationRoute p first middle =>
      raw.gk4afMatrix)
    (by
      intro r s h
      rcases h with ⟨cell⟩
      exact nativeGK4AF_p92_sound cell)

/-- INDEPENDENT descent to the structural quotient S: F54 seams are
real added comparisons, not implicit P92B 3-cell constructors. -/
def nativeGK4AFStructuralValue :
    NativeGK4EStructuralRouteClasses first middle → NativeGK4AFMatrix :=
  _root_.Quotient.lift
    (fun raw : KuuNativeF45Tree.DepthRotationRoute p first middle =>
      raw.gk4afMatrix)
    (by
      intro r s h
      rcases h with ⟨cell⟩
      exact nativeGK4AF_structural_sound cell)

@[simp] theorem nativeGK4AFP92Value_class
    (raw : KuuNativeF45Tree.DepthRotationRoute p first middle) :
    nativeGK4AFP92Value first middle
        (nativeF55P92AssocRouteClass first middle raw) =
      raw.gk4afMatrix := rfl

@[simp] theorem nativeGK4AFStructuralValue_class
    (raw : KuuNativeF45Tree.DepthRotationRoute p first middle) :
    nativeGK4AFStructuralValue first middle
        (nativeGK4EStructuralRouteClass first middle raw) =
      raw.gk4afMatrix := rfl

theorem nativeGK4AF_commutes
    (q : NativeF55P92AssocRouteClasses first middle) :
    nativeGK4AFStructuralValue first middle
        (nativeGK4EP92ToStructural first middle q) =
      nativeGK4AFP92Value first middle q := by
  refine _root_.Quotient.inductionOn q ?_
  intro raw
  rfl

theorem nativeGK4AFStructural_compose
    (u : NativeGK4EStructuralRouteClasses first middle)
    (v : NativeGK4EStructuralRouteClasses middle last) :
    nativeGK4AFStructuralValue first last
        (nativeGK4H_structuralCompose first middle last u v) =
      nativeGK4AFMul
        (nativeGK4AFStructuralValue first middle u)
        (nativeGK4AFStructuralValue middle last v) := by
  refine _root_.Quotient.inductionOn u ?_
  intro rawU
  refine _root_.Quotient.inductionOn v ?_
  intro rawV
  exact nativeGK4AF_trans rawU rawV

@[simp] theorem nativeGK4AFStructural_unit :
    nativeGK4AFStructuralValue first first
      (nativeGK4H_structuralUnit first) = nativeGK4AFOne := rfl

end GenuineQuotientDescent

#print axioms NativeGK4AFMatrix
#print axioms nativeGK4AFMul
#print axioms nativeGK4AFOne
#print axioms nativeGK4AFCast
#print axioms nativeGK4AFForward
#print axioms nativeGK4AFBackward
#print axioms nativeGK4AFMul_assoc
#print axioms nativeGK4AFMul_leftUnit
#print axioms nativeGK4AFMul_rightUnit
#print axioms nativeGK4AFCastForward
#print axioms KuuNativeF45Tree.RotationEdge.gk4afMatrix
#print axioms KuuNativeF45Tree.RotationChain.gk4afMatrix
#print axioms KuuNativeF45Tree.DepthRotationRoute.gk4afMatrix
#print axioms nativeGK4AF_trans
#print axioms nativeGK4AF_leftContext
#print axioms nativeGK4AF_rightContext
#print axioms nativeGK4AF_assoc
#print axioms nativeGK4AF_horizontal
#print axioms nativeGK4AF_assocNaturality
#print axioms nativeGK4AF_original_sound
#print axioms nativeGK4AF_p92_sound
#print axioms nativeGK4AF_seam_sound
#print axioms nativeGK4AF_structural_sound
#print axioms nativeGK4AFP92Value
#print axioms nativeGK4AFStructuralValue
#print axioms nativeGK4AFP92Value_class
#print axioms nativeGK4AFStructuralValue_class
#print axioms nativeGK4AF_commutes
#print axioms nativeGK4AFStructural_compose
#print axioms nativeGK4AFStructural_unit

end
end Kuu.F112.Physical
