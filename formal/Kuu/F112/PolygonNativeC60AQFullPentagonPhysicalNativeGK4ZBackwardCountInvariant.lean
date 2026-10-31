import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4YEnhancedKernelForgetful
import Mathlib.Tactic

/-!
F112-P94D3GK4Z — genuine original F54 backward physical-rotation count.

The GK4W signed cast-minus-total-rotation charge is INSUFFICIENT
to classify the independent F54 structural quotient. The actual
F54 RotationEdge stores a Type-valued forward OR backward local
rotation witness. Count only backward edges of each genuine
RotationChain. Check ALL NINE original F55 presented 3-cell shapes
(pentagon/square have only forward edges), ALL NINE P92B constructors
(including the actual source associator naturality), ALL FOURTEEN
independent F54 structural seam constructors, and all THREE extended
structural comparison constructors.

The result is a new additive Nat invariant of the actual original
P92B quotient Q and independent GK4E structural quotient S.
Equality of numeric observations does not imply a Type-valued
original P92B 3-cell; neither original P92B associativity nor
unitality is assumed.

Keep strict 空 central; independent Kuu one presentation, no Gray,
append-only, same-root, public root 107. Pinned Lean v4.30.0-rc2;
mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Protected validation-only PR #1558 Draft/open/unmerged.
Copyright 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section
universe uD vD uE vE

section OriginalBackwardCount
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}

/-- Exactly one on an ACTUAL backward Type-valued F54 rotation edge,
zero on an original forward edge. No arbitrary inverse edges. -/
def KuuNativeF45Tree.RotationEdge.gk4zBackwardCount
    {n m : Nat}
    {before after : KuuNativeF45Tree p n m ma pa mb pb}
    (edge : KuuNativeF45Tree.RotationEdge p before after) : Nat :=
  match edge with
  | .forward _ => 0
  | .backward _ => 1

/-- Count every ACTUAL backward edge of the whole original
intermediate-tree-preserving RotationChain. -/
def KuuNativeF45Tree.RotationChain.gk4zBackwardCount
    {n m : Nat}
    {before after : KuuNativeF45Tree p n m ma pa mb pb} :
    KuuNativeF45Tree.RotationChain p before after → Nat
  | .refl _ => 0
  | .snoc chain edge =>
      chain.gk4zBackwardCount + edge.gk4zBackwardCount

/-- Original F54 DependentRotationRoute signature retains the
exact chain backward count. Casts contribute ZERO; real trans
adds; original F45 contexts preserve this source witness count. -/
def KuuNativeF45Tree.DepthRotationRoute.gk4zBackwardCount
    {n n' m m' : Nat}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (route : KuuNativeF45Tree.DepthRotationRoute p first last) : Nat := by
  induction route with
  | chain path => exact path.gk4zBackwardCount
  | castDepths _ _ _ => exact 0
  | trans _ _ ihLeft ihRight => exact ihLeft + ihRight
  | leftContext _ _ ih => exact ih
  | rightContext _ _ ih => exact ih

theorem nativeGK4ZBackward_trans
    {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
    {t₁ : KuuNativeF45Tree p n₁ m₁ ma pa mb pb}
    {t₂ : KuuNativeF45Tree p n₂ m₂ ma pa mb pb}
    {t₃ : KuuNativeF45Tree p n₃ m₃ ma pa mb pb}
    (u : KuuNativeF45Tree.DepthRotationRoute p t₁ t₂)
    (v : KuuNativeF45Tree.DepthRotationRoute p t₂ t₃) :
    (KuuNativeF45Tree.DepthRotationRoute.trans u v).gk4zBackwardCount =
      u.gk4zBackwardCount + v.gk4zBackwardCount := rfl

@[simp] theorem nativeGK4ZBackward_leftContext
    {n n' m m' k l : Nat}
    {mc : KuuNativeBlocks a b} {pc : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (route : KuuNativeF45Tree.DepthRotationRoute p first last)
    (later : KuuNativeF45Tree p k l mb pb mc pc) :
    (KuuNativeF45Tree.DepthRotationRoute.leftContext route later).gk4zBackwardCount =
      route.gk4zBackwardCount := rfl

@[simp] theorem nativeGK4ZBackward_rightContext
    {k l n n' m m' : Nat}
    {mc : KuuNativeBlocks a b} {pc : KuuNativeBlocks x y}
    (earlier : KuuNativeF45Tree p k l ma pa mb pb)
    {first : KuuNativeF45Tree p n m mb pb mc pc}
    {last : KuuNativeF45Tree p n' m' mb pb mc pc}
    (route : KuuNativeF45Tree.DepthRotationRoute p first last) :
    (KuuNativeF45Tree.DepthRotationRoute.rightContext earlier route).gk4zBackwardCount =
      route.gk4zBackwardCount := rfl

/-- Every genuine original F54 associator uses one FORWARD
physical rotation and one double-depth cast, hence backward=0. -/
@[simp] theorem nativeGK4ZBackward_assoc
    {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
    {p₀ p₁ p₂ p₃ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ q₃ : KuuNativeBlocks x y}
    (t₁ : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁)
    (t₂ : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂)
    (t₃ : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃) :
    (KuuNativeF45Tree.DepthRotationRoute.assoc t₁ t₂ t₃).gk4zBackwardCount =
      0 := by
  rfl

/-- Real two-context F54 horizontal source adds backwards exactly. -/
theorem nativeGK4ZBackward_horizontal
    {n n' m m' k k' l l' : Nat}
    {p₀ p₁ p₂ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ : KuuNativeBlocks x y}
    {leftBefore : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
    {leftAfter : KuuNativeF45Tree p n' m' p₀ q₀ p₁ q₁}
    {rightBefore : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂}
    {rightAfter : KuuNativeF45Tree p k' l' p₁ q₁ p₂ q₂}
    (u : KuuNativeF45Tree.DepthRotationRoute p leftBefore leftAfter)
    (v : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter) :
    (nativeF54P90HorizontalRoute u v).gk4zBackwardCount =
      u.gk4zBackwardCount + v.gk4zBackwardCount := by
  simp only [nativeF54P90HorizontalRoute, nativeGK4ZBackward_trans,
    nativeGK4ZBackward_leftContext, nativeGK4ZBackward_rightContext]

/-- Both genuinely typed P90 associator-naturality paths have
the same backwards count, since each uses exactly one forward
associator and both include the same 3 raw source histories. -/
theorem nativeGK4ZBackward_assocNaturality
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
    (nativeF54P90AssocNaturalityLeftRoute u v w).gk4zBackwardCount =
      (nativeF54P90AssocNaturalityRightRoute u v w).gk4zBackwardCount := by
  simp only [nativeF54P90AssocNaturalityLeftRoute,
    nativeF54P90AssocNaturalityRightRoute, nativeGK4ZBackward_trans,
    nativeGK4ZBackward_horizontal, nativeGK4ZBackward_assoc,
    add_zero, zero_add]
  omega

end OriginalBackwardCount

section AllFullOriginalComparisons
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}
variable {n n' m m' : Nat}
variable {first : KuuNativeF45Tree p n m ma pa mb pb}
variable {last : KuuNativeF45Tree p n' m' ma pa mb pb}
variable {r s : KuuNativeF45Tree.DepthRotationRoute p first last}

/-- All nine ORIGINAL F55 source proof constructors preserve
backwards count. Actual pentagon and square use only FORWARD edges. -/
theorem nativeGK4ZBackward_original_sound
    (cell : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    r.gk4zBackwardCount = s.gk4zBackwardCount := by
  induction cell with
  | ident route => rfl
  | pentagon a b c d =>
      change (0 : Nat) = 0
      rfl
  | disjointSquare left right =>
      change (0 : Nat) = 0
      rfl
  | symm cell ih => exact ih.symm
  | trans left right ihLeft ihRight => exact ihLeft.trans ihRight
  | leftContext cell later ih => exact ih
  | rightContext earlier cell ih => exact ih
  | precompose prior cell ih =>
      simp only [nativeGK4ZBackward_trans]
      omega
  | postcompose cell suffix ih =>
      simp only [nativeGK4ZBackward_trans]
      omega

/-- All nine original P92B Type-valued comparison constructors,
including the independently added P90 assocNaturality source. -/
theorem nativeGK4ZBackward_p92_sound
    (cell : NativeF55P92AssocComparison p r s) :
    r.gk4zBackwardCount = s.gk4zBackwardCount := by
  induction cell with
  | original old => exact nativeGK4ZBackward_original_sound old
  | assocNaturality u v w => exact nativeGK4ZBackward_assocNaturality u v w
  | refl route => rfl
  | symm cell ih => exact ih.symm
  | trans left right ihLeft ihRight => exact ihLeft.trans ihRight
  | leftContext cell later ih => exact ih
  | rightContext earlier cell ih => exact ih
  | precompose prior cell ih =>
      simp only [nativeGK4ZBackward_trans]
      omega
  | postcompose cell suffix ih =>
      simp only [nativeGK4ZBackward_trans]
      omega

/-- All FOURTEEN separate genuine F54 structural seam constructors,
without replacing their original proof histories by shadows. -/
theorem nativeGK4ZBackward_seam_sound
    (seam : NativeF54StructuralSeam p r s) :
    r.gk4zBackwardCount = s.gk4zBackwardCount := by
  induction seam with
  | refl route => rfl
  | symm seam ih => exact ih.symm
  | trans left right ihLeft ihRight => exact ihLeft.trans ihRight
  | reassoc u v w =>
      simp only [nativeGK4ZBackward_trans]
      omega
  | leftUnit route =>
      simp only [nativeGK4ZBackward_trans]
      change (0 : Nat) + route.gk4zBackwardCount = route.gk4zBackwardCount
      omega
  | rightUnit route =>
      simp only [nativeGK4ZBackward_trans]
      change route.gk4zBackwardCount + (0 : Nat) = route.gk4zBackwardCount
      omega
  | precompose prior seam ih =>
      simp only [nativeGK4ZBackward_trans]
      omega
  | postcompose seam suffix ih =>
      simp only [nativeGK4ZBackward_trans]
      omega
  | leftContextTrans u v later =>
      simp only [nativeGK4ZBackward_leftContext, nativeGK4ZBackward_trans]
  | rightContextTrans earlier u v =>
      simp only [nativeGK4ZBackward_rightContext, nativeGK4ZBackward_trans]
  | leftContextUnit earlier later => rfl
  | rightContextUnit earlier later => rfl
  | leftContextCongruence seam later ih => exact ih
  | rightContextCongruence earlier seam ih => exact ih

/-- All THREE extended genuine structural comparison constructors. -/
theorem nativeGK4ZBackward_structural_sound
    (cell : NativeF55StructuralComparison p r s) :
    r.gk4zBackwardCount = s.gk4zBackwardCount := by
  induction cell with
  | original old => exact nativeGK4ZBackward_p92_sound old
  | structural seam => exact nativeGK4ZBackward_seam_sound seam
  | trans left right ihLeft ihRight => exact ihLeft.trans ihRight

end AllFullOriginalComparisons

section TrueQuotientDescent

variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}
variable {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
variable (t₁ : KuuNativeF45Tree p n₁ m₁ ma pa mb pb)
variable (t₂ : KuuNativeF45Tree p n₂ m₂ ma pa mb pb)
variable (t₃ : KuuNativeF45Tree p n₃ m₃ ma pa mb pb)

/-- The new backward count on the genuine ORIGINAL P92B existence
quotient Q. This is NOT a new raw Type-valued P92B comparison. -/
def nativeGK4ZBackwardP92 :
    NativeF55P92AssocRouteClasses t₁ t₂ → Nat :=
  _root_.Quotient.lift
    (fun r : KuuNativeF45Tree.DepthRotationRoute p t₁ t₂ =>
      r.gk4zBackwardCount)
    (by
      intro r s h
      rcases h with ⟨cell⟩
      exact nativeGK4ZBackward_p92_sound cell)

/-- The SAME raw invariant independently on the genuinely larger
F54 structural-comparison existence quotient S. -/
def nativeGK4ZBackwardStructural :
    NativeGK4EStructuralRouteClasses t₁ t₂ → Nat :=
  _root_.Quotient.lift
    (fun r : KuuNativeF45Tree.DepthRotationRoute p t₁ t₂ =>
      r.gk4zBackwardCount)
    (by
      intro r s h
      rcases h with ⟨cell⟩
      exact nativeGK4ZBackward_structural_sound cell)

@[simp] theorem nativeGK4ZBackwardP92_class
    (r : KuuNativeF45Tree.DepthRotationRoute p t₁ t₂) :
    nativeGK4ZBackwardP92 t₁ t₂
      (nativeF55P92AssocRouteClass t₁ t₂ r) = r.gk4zBackwardCount := rfl

@[simp] theorem nativeGK4ZBackwardStructural_class
    (r : KuuNativeF45Tree.DepthRotationRoute p t₁ t₂) :
    nativeGK4ZBackwardStructural t₁ t₂
      (nativeGK4EStructuralRouteClass t₁ t₂ r) = r.gk4zBackwardCount := rfl

theorem nativeGK4ZBackward_commutes
    (q : NativeF55P92AssocRouteClasses t₁ t₂) :
    nativeGK4ZBackwardStructural t₁ t₂
      (nativeGK4EP92ToStructural t₁ t₂ q) =
      nativeGK4ZBackwardP92 t₁ t₂ q := by
  refine _root_.Quotient.inductionOn q ?_
  intro raw
  rfl

/-- Genuine original and independent structural composition both
preserve backward count additively without source Q category laws. -/
theorem nativeGK4ZBackwardStructural_compose
    (u : NativeGK4EStructuralRouteClasses t₁ t₂)
    (v : NativeGK4EStructuralRouteClasses t₂ t₃) :
    nativeGK4ZBackwardStructural t₁ t₃
      (nativeGK4H_structuralCompose t₁ t₂ t₃ u v) =
    nativeGK4ZBackwardStructural t₁ t₂ u +
      nativeGK4ZBackwardStructural t₂ t₃ v := by
  refine _root_.Quotient.inductionOn u ?_
  intro rawU
  refine _root_.Quotient.inductionOn v ?_
  intro rawV
  exact nativeGK4ZBackward_trans rawU rawV

@[simp] theorem nativeGK4ZBackwardStructural_unit :
    nativeGK4ZBackwardStructural t₁ t₁
      (nativeGK4H_structuralUnit t₁) = 0 := rfl

#print axioms KuuNativeF45Tree.RotationEdge.gk4zBackwardCount
#print axioms KuuNativeF45Tree.RotationChain.gk4zBackwardCount
#print axioms KuuNativeF45Tree.DepthRotationRoute.gk4zBackwardCount
#print axioms nativeGK4ZBackward_trans
#print axioms nativeGK4ZBackward_leftContext
#print axioms nativeGK4ZBackward_rightContext
#print axioms nativeGK4ZBackward_assoc
#print axioms nativeGK4ZBackward_horizontal
#print axioms nativeGK4ZBackward_assocNaturality
#print axioms nativeGK4ZBackward_original_sound
#print axioms nativeGK4ZBackward_p92_sound
#print axioms nativeGK4ZBackward_seam_sound
#print axioms nativeGK4ZBackward_structural_sound
#print axioms nativeGK4ZBackwardP92
#print axioms nativeGK4ZBackwardStructural
#print axioms nativeGK4ZBackwardP92_class
#print axioms nativeGK4ZBackwardStructural_class
#print axioms nativeGK4ZBackward_commutes
#print axioms nativeGK4ZBackwardStructural_compose
#print axioms nativeGK4ZBackwardStructural_unit

end TrueQuotientDescent
end
end Kuu.F112.Physical
