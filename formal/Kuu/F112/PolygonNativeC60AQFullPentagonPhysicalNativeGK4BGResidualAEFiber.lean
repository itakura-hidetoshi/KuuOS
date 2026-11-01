import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4BFAttainedAHCategory
import Mathlib.Tactic

/-!
F112-P94D3GK4BG — exact residual obstruction on genuinely attained
AH fibers of the EXISTING second-kernel K_AI category.

Old AH equality already determines the complete original polynomial
and old AF matrices. The remaining potential nonfaithfulness resides
only in the genuine original AE component (Boolean grade and ordered
AD triple). For each fixed attained AH matrix, construct an explicit
equivalence of the genuine K_AI fiber with the actually reached AE
image, and characterize precisely when that fiber is nontrivial.

On a genuine F54 self-Hom with zero original backward rotations,
the physical rank argument forces Boolean grade true. Conditional
AH collisions in that slice can therefore occur only in AD.

No actual nontrivial AH collision is assumed or asserted. No original
Q category laws, fabricated source Type-valued 3-cells, untyped matrix
words, unattained values, Gray or hyperdescent. This is a
tighten-only refinement of GK4BA-BF, not a weaker theorem.
Append-only / same public root107; strict 空 central;
independent Kuu one presentation; protect PR #1558 Draft OPEN.
Lean v4.30.0-rc2; pinned mathlib
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

section GenuinelyAttainedAHResidual
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable {n n' m m' : Nat}
variable (first : KuuNativeF45Tree p n m ma pa mb pb)
variable (last : KuuNativeF45Tree p n' m' ma pa mb pb)

/-- Original first matrix is exactly t=1 polynomial specialization
of EVERY genuine K_AI quotient arrow. -/
theorem nativeGK4BGKernelAF_eval_one
    (z : NativeGK4SKernelClasses
      (nativeGK4AIP92Family p D E) first last) :
    nativeGK4AVPolyEval 1 (nativeGK4BBPolynomialOnAI first last z) =
      (nativeGK4AIKernelValue first last z).1.2 := by
  refine _root_.Quotient.inductionOn z ?_
  intro q
  change nativeGK4AVPolyEval 1 (nativeGK4AVP92Value first last q) =
    nativeGK4AFP92Value first last q
  exact (nativeGK4AVP92_recover first last q).1

/-- Fixed genuinely attained old AH forces the old AF matrix.
This uses GK4BA one-point determinacy, not original route equality. -/
theorem nativeGK4BGKernelAH_eq_implies_AF_eq
    (u v : NativeGK4SKernelClasses
      (nativeGK4AIP92Family p D E) first last)
    (hAH : (nativeGK4AIKernelValue first last u).2 =
      (nativeGK4AIKernelValue first last v).2) :
    (nativeGK4AIKernelValue first last u).1.2 =
      (nativeGK4AIKernelValue first last v).1.2 := by
  have h4 :
      nativeGK4AVPolyEval 4 (nativeGK4BBPolynomialOnAI first last u) =
      nativeGK4AVPolyEval 4 (nativeGK4BBPolynomialOnAI first last v) := by
    simpa only [nativeGK4BBPolynomialOnAI_eval_four] using hAH
  have h1 := nativeGK4BEFour_determines_all first last u v 1 h4
  calc
    (nativeGK4AIKernelValue first last u).1.2 =
      nativeGK4AVPolyEval 1 (nativeGK4BBPolynomialOnAI first last u) :=
        (nativeGK4BGKernelAF_eval_one first last u).symm
    _ = nativeGK4AVPolyEval 1 (nativeGK4BBPolynomialOnAI first last v) := h1
    _ = (nativeGK4AIKernelValue first last v).1.2 :=
      nativeGK4BGKernelAF_eval_one first last v

/-- Residual comparison: WITH AH fixed, two genuine K_AI
classes coincide iff their old AE observation is identical. -/
theorem nativeGK4BGKernelAH_eq_class_iff_AE_eq
    (u v : NativeGK4SKernelClasses
      (nativeGK4AIP92Family p D E) first last)
    (hAH : (nativeGK4AIKernelValue first last u).2 =
      (nativeGK4AIKernelValue first last v).2) :
    u = v ↔
      (nativeGK4AIKernelValue first last u).1.1 =
        (nativeGK4AIKernelValue first last v).1.1 := by
  constructor
  · intro h
    exact congrArg
      (fun z : NativeGK4SKernelClasses
        (nativeGK4AIP92Family p D E) first last =>
        (nativeGK4AIKernelValue first last z).1.1) h
  · intro hAE
    apply nativeGK4AIKernelValue_injective first last
    apply Prod.ext
    · apply Prod.ext
      · exact hAE
      · exact nativeGK4BGKernelAH_eq_implies_AF_eq first last u v hAH
    · exact hAH

/-- Every typed K_AI arrow with exactly old AH matrix A.
Unattained A yields an EMPTY fiber, not a fictional witness. -/
def NativeGK4BGFixedAHFiber (A : NativeGK4AHMatrix) :
    Type (max (max uD uE) (max vD vE)) :=
  {z : NativeGK4SKernelClasses
       (nativeGK4AIP92Family p D E) first last //
     (nativeGK4AIKernelValue first last z).2 = A}

/-- Only the genuinely attained AE values OVER this fixed AH
matrix are retained. No all-values surjectivity claim. -/
def NativeGK4BGAttainedResidualAE (A : NativeGK4AHMatrix) : Type :=
  {e : NativeGK4AEValue //
    ∃ z : NativeGK4BGFixedAHFiber first last A,
      (nativeGK4AIKernelValue first last z.val).1.1 = e}

/-- The true fixed-AH fiber sends each class to its reached AE value. -/
def nativeGK4BGFixedAHToResidualAE
    (A : NativeGK4AHMatrix)
    (z : NativeGK4BGFixedAHFiber first last A) :
    NativeGK4BGAttainedResidualAE first last A :=
  ⟨(nativeGK4AIKernelValue first last z.val).1.1, ⟨z, rfl⟩⟩

/-- Old AE still separates K_AI classes WITHIN the same old AH fiber. -/
theorem nativeGK4BGFixedAHToResidualAE_injective
    (A : NativeGK4AHMatrix) :
    Function.Injective (nativeGK4BGFixedAHToResidualAE first last A) := by
  intro u v huv
  apply Subtype.ext
  apply (nativeGK4BGKernelAH_eq_class_iff_AE_eq
    first last u.val v.val (u.property.trans v.property.symm)).2
  exact congrArg Subtype.val huv

/-- Every reached residual AE value has an actual same-AH K_AI
witness; this is not a source-route section into Q. -/
theorem nativeGK4BGFixedAHToResidualAE_surjective
    (A : NativeGK4AHMatrix) :
    Function.Surjective (nativeGK4BGFixedAHToResidualAE first last A) := by
  intro e
  obtain ⟨z, hz⟩ := e.property
  refine ⟨z, ?_⟩
  apply Subtype.ext
  exact hz

/-- First-isomorphism statement on EACH fixed, genuinely attained
old AH fiber; no nontriviality of the target is assumed. -/
noncomputable def nativeGK4BGFixedAHFiberEquivResidualAE
    (A : NativeGK4AHMatrix) :
    NativeGK4BGFixedAHFiber first last A ≃
      NativeGK4BGAttainedResidualAE first last A :=
  Equiv.ofBijective (nativeGK4BGFixedAHToResidualAE first last A)
    ⟨nativeGK4BGFixedAHToResidualAE_injective first last A,
      nativeGK4BGFixedAHToResidualAE_surjective first last A⟩

/-- An ACTUAL AH collision exists iff two DIFFERENT actual reached
residual AE values exist, with fully typed underlying witnesses. -/
theorem nativeGK4BGFixedAH_nontrivial_iff_residual
    (A : NativeGK4AHMatrix) :
    (∃ u v : NativeGK4BGFixedAHFiber first last A, u ≠ v) ↔
      (∃ e f : NativeGK4BGAttainedResidualAE first last A, e ≠ f) := by
  constructor
  · rintro ⟨u, v, hne⟩
    refine ⟨nativeGK4BGFixedAHToResidualAE first last A u,
      nativeGK4BGFixedAHToResidualAE first last A v, ?_⟩
    intro h
    exact hne (nativeGK4BGFixedAHToResidualAE_injective first last A h)
  · rintro ⟨e, f, hne⟩
    obtain ⟨u, rfl⟩ := nativeGK4BGFixedAHToResidualAE_surjective first last A e
    obtain ⟨v, rfl⟩ := nativeGK4BGFixedAHToResidualAE_surjective first last A f
    refine ⟨u, v, ?_⟩
    intro h
    exact hne (congrArg (nativeGK4BGFixedAHToResidualAE first last A) h)

end GenuinelyAttainedAHResidual

section PhysicalZeroBackwardGate
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E} {n m : Nat}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable (tree : KuuNativeF45Tree p n m ma pa mb pb)

/-- Original F54 self-Hom with zero backward witnesses cannot have
forward rotations either, by the actual GK4AC physical rank bound.
Its Boolean grade is therefore true after the genuine K_AI descent. -/
theorem nativeGK4BGSelf_zeroBackward_grade_true
    (z : NativeGK4SKernelClasses
      (nativeGK4AIP92Family p D E) tree tree)
    (hback : (nativeGK4AIKernelValue tree tree z).1.1.2.1.2 = 0) :
    (nativeGK4AIKernelValue tree tree z).1.1.1 = true := by
  revert hback
  refine _root_.Quotient.inductionOn z ?_
  intro q hback
  revert hback
  refine _root_.Quotient.inductionOn q ?_
  intro raw hback
  have hbridge := raw.gk4aeADFirstPair
  have hraw : raw.gk4zBackwardCount = 0 := by
    change raw.gk4adValue.1.2 = 0 at hback
    exact (congrArg (fun z : Int × Nat => z.2) hbridge).symm.trans hback
  change nativeGK4GRawGrade tree tree raw = true
  exact nativeGK4ACRawSelf_noBackward_grade_true tree raw hraw

/-- Conditional collision criterion on the zero-backward self-Hom
slice: the residual distinction can ONLY lie in old AD history. -/
theorem nativeGK4BGSelf_zeroBackward_collision_iff_AD
    (u v : NativeGK4SKernelClasses
      (nativeGK4AIP92Family p D E) tree tree)
    (hbu : (nativeGK4AIKernelValue tree tree u).1.1.2.1.2 = 0)
    (hbv : (nativeGK4AIKernelValue tree tree v).1.1.2.1.2 = 0)
    (hAH : (nativeGK4AIKernelValue tree tree u).2 =
      (nativeGK4AIKernelValue tree tree v).2) :
    u ≠ v ↔
      (nativeGK4AIKernelValue tree tree u).1.1.2 ≠
        (nativeGK4AIKernelValue tree tree v).1.1.2 := by
  have gu := nativeGK4BGSelf_zeroBackward_grade_true tree u hbu
  have gv := nativeGK4BGSelf_zeroBackward_grade_true tree v hbv
  constructor
  · intro hne hAD
    have hAE : (nativeGK4AIKernelValue tree tree u).1.1 =
        (nativeGK4AIKernelValue tree tree v).1.1 :=
      Prod.ext (gu.trans gv.symm) hAD
    exact hne ((nativeGK4BGKernelAH_eq_class_iff_AE_eq
      tree tree u v hAH).2 hAE)
  · intro hAD huv
    exact hAD (congrArg
      (fun z : NativeGK4SKernelClasses
        (nativeGK4AIP92Family p D E) tree tree =>
        (nativeGK4AIKernelValue tree tree z).1.1.2) huv)

end PhysicalZeroBackwardGate

#print axioms nativeGK4BGKernelAF_eval_one
#print axioms nativeGK4BGKernelAH_eq_implies_AF_eq
#print axioms nativeGK4BGKernelAH_eq_class_iff_AE_eq
#print axioms NativeGK4BGFixedAHFiber
#print axioms NativeGK4BGAttainedResidualAE
#print axioms nativeGK4BGFixedAHToResidualAE
#print axioms nativeGK4BGFixedAHToResidualAE_injective
#print axioms nativeGK4BGFixedAHToResidualAE_surjective
#print axioms nativeGK4BGFixedAHFiberEquivResidualAE
#print axioms nativeGK4BGFixedAH_nontrivial_iff_residual
#print axioms nativeGK4BGSelf_zeroBackward_grade_true
#print axioms nativeGK4BGSelf_zeroBackward_collision_iff_AD

end
end Kuu.F112.Physical
