import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4BHFirstJetADRecovery
import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4ACForwardRank
import Mathlib.Tactic

/-!
F112-P94D3GK4BH (part 2) — exact original F54 physical rank
determines the remaining Boolean grade from backwardCount and
the original typed endpoints. Combined with GK4BH's first-jet
recovery of ALL ordered GK4AD data from the original AH matrix,
this proves actual old AH observation FAITHFUL on EVERY typed Hom
of the EXISTING second-kernel K_AI.

A real F54 zero-rotation route preserves the exact original
left-branch rank (including both contexts and double-Nat casts).
The preexisting GK4AC no-backward forward-rank inequality forces
the converse when backwardCount=0 and endpoint ranks agree. Thus

  grade(r)=true iff back(r)=0 and rank(first)=rank(last).

All are genuine original, fully dependent F54 routes and actually
attained K_AI kernel classes. No untyped word loops, no new source
3-cells, no Q category laws, no faithfulness of S->K_AI, no Gray,
no hyperdescent and no arbitrary AH matrices assumed attainable.

Tighten-only / append-only / same public root107.
Lean v4.30.0-rc2, pinned mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Protected validation-only #1558 stays Draft/open/unmerged.
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

section ExactOriginalPhysicalGrade
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}

/-- Every genuinely oriented backward edge is one among the real
primitive rotations, for ANY original intermediate-tree chain. -/
theorem nativeGK4BHChain_backward_le_length
    {n m : Nat}
    {first last : KuuNativeF45Tree p n m ma pa mb pb}
    (chain : KuuNativeF45Tree.RotationChain p first last) :
    chain.gk4zBackwardCount ≤ chain.length := by
  induction chain with
  | refl => exact Nat.le_refl 0
  | snoc path edge ih =>
      cases edge with
      | forward _ =>
          change path.gk4zBackwardCount + 0 ≤ path.length + 1
          omega
      | backward _ =>
          change path.gk4zBackwardCount + 1 ≤ path.length + 1
          omega

/-- Actual dependent F54 source: backwardCount ≤ primitive
rotationCount, including casts, trans and BOTH original contexts. -/
theorem nativeGK4BHRoute_backward_le_count
    {n n' m m' : Nat}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (route : KuuNativeF45Tree.DepthRotationRoute p first last) :
    route.gk4zBackwardCount ≤ route.rotationCount := by
  induction route with
  | chain path => exact nativeGK4BHChain_backward_le_length path
  | castDepths _ _ _ => exact Nat.le_refl 0
  | trans u v ihU ihV =>
      change u.gk4zBackwardCount + v.gk4zBackwardCount ≤
        u.rotationCount + v.rotationCount
      omega
  | leftContext _ _ ih => exact ih
  | rightContext _ _ ih => exact ih

/-- ZERO real rotations means ZERO rank change for ANY typed F54
route; this is stronger than a merely numerical count argument:
intermediate original F45 trees and two contextual constructors
are preserved by induction on the full source. -/
theorem nativeGK4BHZeroRotation_rank_eq
    {n n' m m' : Nat}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (route : KuuNativeF45Tree.DepthRotationRoute p first last)
    (hzero : route.rotationCount = 0) :
    first.gk4acLeftRank = last.gk4acLeftRank := by
  induction route with
  | chain path =>
      cases path with
      | refl => rfl
      | snoc prior edge =>
          change prior.length + 1 = 0 at hzero
          omega
  | castDepths hn hm tree =>
      exact (KuuNativeF45Tree.gk4acLeftRank_cast hn hm tree).symm
  | trans u v ihU ihV =>
      have hsum : u.rotationCount + v.rotationCount = 0 := hzero
      have hu : u.rotationCount = 0 := by omega
      have hv : v.rotationCount = 0 := by omega
      exact (ihU hu).trans (ihV hv)
  | leftContext path later ih =>
      have hr : path.rotationCount = 0 := hzero
      have hl := path.gk4acLeafCount_eq
      have he := ih hr
      simp only [KuuNativeF45Tree.gk4acLeftRank_node]
      omega
  | rightContext earlier path ih =>
      have hr : path.rotationCount = 0 := hzero
      have he := ih hr
      simp only [KuuNativeF45Tree.gk4acLeftRank_node]
      omega

/-- Exact necessary and sufficient condition for genuine physical
grade TRUE at any original typed Hom endpoints, with NO assumptions
about old source Q categorical laws or route-word cancellations. -/
theorem nativeGK4BHRaw_grade_true_iff
    {n n' m m' : Nat}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (route : KuuNativeF45Tree.DepthRotationRoute p first last) :
    nativeGK4GRawGrade first last route = true ↔
      route.gk4zBackwardCount = 0 ∧
        first.gk4acLeftRank = last.gk4acLeftRank := by
  constructor
  · intro h
    have hzero : route.rotationCount = 0 := by
      simpa [nativeGK4GRawGrade] using h
    have hbound := nativeGK4BHRoute_backward_le_count route
    exact ⟨by omega, nativeGK4BHZeroRotation_rank_eq route hzero⟩
  · rintro ⟨hback, hrank⟩
    have hb := route.gk4acNoBackward_bound hback
    have hzero : route.rotationCount = 0 := by omega
    simp [nativeGK4GRawGrade, hzero]

end ExactOriginalPhysicalGrade

section ActualKAIGradeAndFaithfulness
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable {n n' m m' : Nat}
variable (first : KuuNativeF45Tree p n m ma pa mb pb)
variable (last : KuuNativeF45Tree p n' m' ma pa mb pb)

/-- Every actually attained K_AI Boolean grade is fully determined
by OLD AD backwardCount plus the two original F45 endpoint ranks.
No new degree of freedom remains in the previous GK4BG AE residual. -/
theorem nativeGK4BHKernel_grade_true_iff
    (z : NativeGK4SKernelClasses
      (nativeGK4AIP92Family p D E) first last) :
    (nativeGK4AIKernelValue first last z).1.1.1 = true ↔
      (nativeGK4AIKernelValue first last z).1.1.2.1.2 = 0 ∧
        first.gk4acLeftRank = last.gk4acLeftRank := by
  refine _root_.Quotient.inductionOn z ?_
  intro q
  refine _root_.Quotient.inductionOn q ?_
  intro raw
  change nativeGK4GRawGrade first last raw = true ↔
    raw.gk4adValue.1.2 = 0 ∧
      first.gk4acLeftRank = last.gk4acLeftRank
  have hb := congrArg Prod.snd raw.gk4aeADFirstPair
  rw [hb]
  exact nativeGK4BHRaw_grade_true_iff raw

/-- AH agreement already fixes AD by the first jet, and consequently
fixes the remaining original Boolean grade on the SAME typed Hom. -/
theorem nativeGK4BHKernel_AH_determines_grade
    (u v : NativeGK4SKernelClasses
      (nativeGK4AIP92Family p D E) first last)
    (hAH : (nativeGK4AIKernelValue first last u).2 =
      (nativeGK4AIKernelValue first last v).2) :
    (nativeGK4AIKernelValue first last u).1.1.1 =
      (nativeGK4AIKernelValue first last v).1.1.1 := by
  have hAD := nativeGK4BHKernel_AH_determines_AD first last u v hAH
  have hb :
      (nativeGK4AIKernelValue first last u).1.1.2.1.2 =
      (nativeGK4AIKernelValue first last v).1.1.2.1.2 :=
    congrArg (fun x : NativeGK4ADValue => x.1.2) hAD
  have hiff :
      ((nativeGK4AIKernelValue first last u).1.1.1 = true) ↔
        ((nativeGK4AIKernelValue first last v).1.1.1 = true) := by
    constructor
    · intro h
      obtain ⟨hzero, hrank⟩ :=
        (nativeGK4BHKernel_grade_true_iff first last u).1 h
      apply (nativeGK4BHKernel_grade_true_iff first last v).2
      constructor
      · calc
          (nativeGK4AIKernelValue first last v).1.1.2.1.2 =
            (nativeGK4AIKernelValue first last u).1.1.2.1.2 := hb.symm
          _ = 0 := hzero
      · exact hrank
    · intro h
      obtain ⟨hzero, hrank⟩ :=
        (nativeGK4BHKernel_grade_true_iff first last v).1 h
      apply (nativeGK4BHKernel_grade_true_iff first last u).2
      constructor
      · calc
          (nativeGK4AIKernelValue first last u).1.1.2.1.2 =
            (nativeGK4AIKernelValue first last v).1.1.2.1.2 := hb
          _ = 0 := hzero
      · exact hrank
  cases hu : (nativeGK4AIKernelValue first last u).1.1.1 <;>
    cases hv : (nativeGK4AIKernelValue first last v).1.1.1 <;>
    simp_all

/-- MAIN RESULT: actual original AH matrix is INJECTIVE on EVERY
genuine dependent K_AI second-kernel Hom. This is NOT source S->K_AI
faithfulness and NOT equality of original Type-valued F54 routes. -/
theorem nativeGK4BHKernel_AH_injective
    (u v : NativeGK4SKernelClasses
      (nativeGK4AIP92Family p D E) first last)
    (hAH : (nativeGK4AIKernelValue first last u).2 =
      (nativeGK4AIKernelValue first last v).2) :
    u = v := by
  have hAD := nativeGK4BHKernel_AH_determines_AD first last u v hAH
  have hGrade := nativeGK4BHKernel_AH_determines_grade first last u v hAH
  have hAF := nativeGK4BGKernelAH_eq_implies_AF_eq first last u v hAH
  apply nativeGK4AIKernelValue_injective first last
  apply Prod.ext
  · apply Prod.ext
    · apply Prod.ext
      · exact hGrade
      · exact hAD
    · exact hAF
  · exact hAH

/-- Faithfulness of the old AH Mathlib functor on all existing
original typed K_AI Homs, with no additional observer or quotient. -/
theorem nativeGK4BHOldAHFunctor_injective_hom
    {D' : Type uD} [Category.{vD} D']
    {E' : Type uE} [Category.{vE} E']
    {a' b' : D'} {x' y' : E'}
    (p' : Polygon)
    (ma' mb' : KuuNativeBlocks a' b')
    (pa' pb' : KuuNativeBlocks x' y')
    (X Y : NativeGK4AIKernelStage p' ma' mb' pa' pb') :
    Function.Injective
      (fun f : X ⟶ Y =>
        (nativeGK4BDOldAHFunctor p' ma' mb' pa' pb').map f) := by
  intro u v h
  change (nativeGK4AIKernelValue X.original.2.2 Y.original.2.2 u).2 =
    (nativeGK4AIKernelValue X.original.2.2 Y.original.2.2 v).2 at h
  exact nativeGK4BHKernel_AH_injective X.original.2.2 Y.original.2.2 u v h

/-- The old K_AI -> genuinely reached AH-image category map is now
also Hom-INJECTIVE. The previous GK4BF criterion is satisfied by
the actual source, rather than merely postulated. -/
theorem nativeGK4BHImageFunctor_injective_hom
    {D' : Type uD} [Category.{vD} D']
    {E' : Type uE} [Category.{vE} E']
    {a' b' : D'} {x' y' : E'}
    (p' : Polygon)
    (ma' mb' : KuuNativeBlocks a' b')
    (pa' pb' : KuuNativeBlocks x' y')
    (X Y : NativeGK4AIKernelStage p' ma' mb' pa' pb') :
    Function.Injective
      (fun f : X ⟶ Y =>
        (nativeGK4BFImageFunctor p' ma' mb' pa' pb').map f) := by
  apply (nativeGK4BFImageFunctor_injective_hom_iff
    p' ma' mb' pa' pb' X Y).2
  intro u v h
  exact nativeGK4BHOldAHFunctor_injective_hom
    p' ma' mb' pa' pb' X Y h

/-- The old K_AI -> reached AH-image functor is BIJECTIVE on EVERY
typed Hom, combining the existing GK4BF true surjectivity with
GK4BH's independent injectivity proof. -/
theorem nativeGK4BHImageFunctor_bijective_hom
    {D' : Type uD} [Category.{vD} D']
    {E' : Type uE} [Category.{vE} E']
    {a' b' : D'} {x' y' : E'}
    (p' : Polygon)
    (ma' mb' : KuuNativeBlocks a' b')
    (pa' pb' : KuuNativeBlocks x' y')
    (X Y : NativeGK4AIKernelStage p' ma' mb' pa' pb') :
    Function.Bijective
      (fun f : X ⟶ Y =>
        (nativeGK4BFImageFunctor p' ma' mb' pa' pb').map f) :=
  ⟨nativeGK4BHImageFunctor_injective_hom p' ma' mb' pa' pb' X Y,
    nativeGK4BFImageFunctor_surjective_hom p' ma' mb' pa' pb' X Y⟩

/-- Every old AH fixed fiber on the TRUE K_AI stage is at most one
class. No claim that arbitrary ambient integer matrices are reached. -/
theorem nativeGK4BHFixedAHFiber_subsingleton
    (A : NativeGK4AHMatrix) :
    Subsingleton (NativeGK4BGFixedAHFiber first last A) := by
  refine ⟨?_⟩
  intro u v
  apply Subtype.ext
  apply nativeGK4BHKernel_AH_injective first last u.val v.val
  exact u.property.trans v.property.symm

/-- The GK4BG residual obstruction is now PROVED ABSENT on all old
K_AI typed AH fibers: no two genuinely distinct K_AI classes have
the same AH matrix. The original S -> K_AI kernel is NOT trivialized. -/
theorem nativeGK4BHNoResidualAHCollision
    (A : NativeGK4AHMatrix) :
    ¬ ∃ e f : NativeGK4BGAttainedResidualAE first last A, e ≠ f := by
  intro h
  obtain ⟨u, v, huv⟩ :=
    (nativeGK4BGFixedAH_nontrivial_iff_residual first last A).2 h
  letI : Subsingleton (NativeGK4BGFixedAHFiber first last A) :=
    nativeGK4BHFixedAHFiber_subsingleton first last A
  exact huv (Subsingleton.elim u v)

end ActualKAIGradeAndFaithfulness

#print axioms nativeGK4BHChain_backward_le_length
#print axioms nativeGK4BHRoute_backward_le_count
#print axioms nativeGK4BHZeroRotation_rank_eq
#print axioms nativeGK4BHRaw_grade_true_iff
#print axioms nativeGK4BHKernel_grade_true_iff
#print axioms nativeGK4BHKernel_AH_determines_grade
#print axioms nativeGK4BHKernel_AH_injective
#print axioms nativeGK4BHOldAHFunctor_injective_hom
#print axioms nativeGK4BHImageFunctor_injective_hom
#print axioms nativeGK4BHImageFunctor_bijective_hom
#print axioms nativeGK4BHFixedAHFiber_subsingleton
#print axioms nativeGK4BHNoResidualAHCollision

end
end Kuu.F112.Physical
