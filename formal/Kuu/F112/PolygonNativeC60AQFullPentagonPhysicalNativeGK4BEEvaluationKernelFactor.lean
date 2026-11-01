import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4BDIntegerEvaluationFunctor
import Mathlib.Tactic

/-!
F112-P94D3GK4BE — original one-point determinacy as an exact
kernel criterion and a unique observed-image factorization.

For every actual fully dependent Hom of the EXISTING second kernel
K_AI, equality at the one genuinely old AH value t=4 determines
the entire GK4BB polynomial and all integer evaluations. The three
kernel relations (polynomial / eval at 4 / all integer evaluations)
therefore coincide ON ATTAINED K_AI Homs, not on arbitrary polynomial
matrices or all ambient 2x2 integer matrices.

For each original typed boundary, the evaluation at ANY integer t
factors uniquely through the ATTAINED IMAGE of the original AH
observation, by genuine witness-existence and GK4BA determinacy.
This is a local Hom-wise image factorization, not a category on Q,
a splitting of source Type-valued 3-cells or a globally faithful
polynomial functor. Actual Q and independent S receive separate
comparison lemmas without identifying their source proof objects.

Append-only/tighten-only/overwrite-forbidden/same-root107.
Strict 空 central; independent Kuu one presentation, no Gray.
Lean v4.30.0-rc2; mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Protected validation-only PR #1558 Draft/OPEN/unmerged.
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

section GenuineKAIKernelAndAttainedImage

variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}
variable {n n' m m' : Nat}
variable (first : KuuNativeF45Tree p n m ma pa mb pb)
variable (last : KuuNativeF45Tree p n' m' ma pa mb pb)

/-- One old t=4 polynomial evaluation determines EVERY integer
specialization of the genuine original GK4BB lift on K_AI. -/
theorem nativeGK4BEFour_determines_all
    (u v : NativeGK4SKernelClasses
      (nativeGK4AIP92Family p D E) first last)
    (t : Int)
    (h4 : nativeGK4AVPolyEval 4 (nativeGK4BBPolynomialOnAI first last u) =
          nativeGK4AVPolyEval 4 (nativeGK4BBPolynomialOnAI first last v)) :
    nativeGK4AVPolyEval t (nativeGK4BBPolynomialOnAI first last u) =
      nativeGK4AVPolyEval t (nativeGK4BBPolynomialOnAI first last v) := by
  have hAH :
      (nativeGK4AIKernelValue first last u).2 =
        (nativeGK4AIKernelValue first last v).2 := by
    simpa only [nativeGK4BBPolynomialOnAI_eval_four] using h4
  exact congrArg (nativeGK4AVPolyEval t)
    ((nativeGK4BBPolynomialOnAI_eq_iff_AH first last u v).2 hAH)

/-- On the ACTUAL typed K_AI quotient, equality of the entire
polynomial family is equivalent to equality at the SINGLE point 4. -/
theorem nativeGK4BEPolynomial_eq_iff_four
    (u v : NativeGK4SKernelClasses
      (nativeGK4AIP92Family p D E) first last) :
    nativeGK4BBPolynomialOnAI first last u =
        nativeGK4BBPolynomialOnAI first last v ↔
      nativeGK4AVPolyEval 4
        (nativeGK4BBPolynomialOnAI first last u) =
      nativeGK4AVPolyEval 4
        (nativeGK4BBPolynomialOnAI first last v) := by
  constructor
  · intro h
    exact congrArg (nativeGK4AVPolyEval 4) h
  · intro h
    apply (nativeGK4BBPolynomialOnAI_eq_iff_AH first last u v).2
    simpa only [nativeGK4BBPolynomialOnAI_eval_four] using h

/-- Pointwise family intersection kernel is exactly the old t=4
kernel, not a claim that either is equality of original K_AI classes. -/
theorem nativeGK4BEAll_eq_iff_four
    (u v : NativeGK4SKernelClasses
      (nativeGK4AIP92Family p D E) first last) :
    (∀ t : Int,
      nativeGK4AVPolyEval t (nativeGK4BBPolynomialOnAI first last u) =
        nativeGK4AVPolyEval t (nativeGK4BBPolynomialOnAI first last v)) ↔
      nativeGK4AVPolyEval 4
        (nativeGK4BBPolynomialOnAI first last u) =
      nativeGK4AVPolyEval 4
        (nativeGK4BBPolynomialOnAI first last v) := by
  constructor
  · intro h
    exact h 4
  · intro h t
    exact nativeGK4BEFour_determines_all first last u v t h

/-- The intersection of ALL integer evaluation kernels is also the
kernel of the TRUE full polynomial family on the old K_AI Hom. -/
theorem nativeGK4BEAll_eq_iff_polynomial
    (u v : NativeGK4SKernelClasses
      (nativeGK4AIP92Family p D E) first last) :
    (∀ t : Int,
      nativeGK4AVPolyEval t (nativeGK4BBPolynomialOnAI first last u) =
        nativeGK4AVPolyEval t (nativeGK4BBPolynomialOnAI first last v)) ↔
      nativeGK4BBPolynomialOnAI first last u =
        nativeGK4BBPolynomialOnAI first last v := by
  constructor
  · intro h
    exact (nativeGK4BEPolynomial_eq_iff_four first last u v).2 (h 4)
  · intro h t
    exact congrArg (nativeGK4AVPolyEval t) h

/-- Exactly those old AH matrices attained by the original typed
K_AI Hom, with an explicit witness that the matrix is attained.
We do NOT replace this with the entire ambient matrix set. -/
def NativeGK4BEAttainedAH : Type :=
  {A : NativeGK4AHMatrix //
    ∃ z : NativeGK4SKernelClasses
      (nativeGK4AIP92Family p D E) first last,
      (nativeGK4AIKernelValue first last z).2 = A}

/-- Original true K_AI representative as an attained old AH value. -/
def nativeGK4BEAttainedAHClass
    (z : NativeGK4SKernelClasses
      (nativeGK4AIP92Family p D E) first last) :
    NativeGK4BEAttainedAH first last :=
  ⟨(nativeGK4AIKernelValue first last z).2, ⟨z, rfl⟩⟩

/-- Every attained AH value has a genuine typed K_AI witness. -/
theorem nativeGK4BEAttainedAHClass_surjective :
    Function.Surjective (nativeGK4BEAttainedAHClass first last) := by
  intro A
  obtain ⟨z, hz⟩ := A.property
  refine ⟨z, ?_⟩
  apply Subtype.ext
  exact hz

/-- The unique evaluation at ANY integer t on the attained old AH
image, using one genuine K_AI witness. Choice of witness is harmless:
GK4BA proves all polynomial values are determined by old AH. -/
noncomputable def nativeGK4BEAttainedEval
    (t : Int) (A : NativeGK4BEAttainedAH first last) :
    NativeGK4AHMatrix :=
  nativeGK4AVPolyEval t
    (nativeGK4BBPolynomialOnAI first last (Classical.choose A.property))

/-- The image-factorized evaluation reproduces the original K_AI
polynomial evaluation, for EVERY genuine typed class and integer t. -/
theorem nativeGK4BEAttainedEval_class
    (t : Int)
    (z : NativeGK4SKernelClasses
      (nativeGK4AIP92Family p D E) first last) :
    nativeGK4BEAttainedEval first last t
        (nativeGK4BEAttainedAHClass first last z) =
      nativeGK4AVPolyEval t (nativeGK4BBPolynomialOnAI first last z) := by
  let A := nativeGK4BEAttainedAHClass first last z
  let w := Classical.choose A.property
  have hw :
      (nativeGK4AIKernelValue first last w).2 =
        (nativeGK4AIKernelValue first last z).2 := by
    have hh := Classical.choose_spec A.property
    simpa only [A, nativeGK4BEAttainedAHClass] using hh
  have hp := (nativeGK4BBPolynomialOnAI_eq_iff_AH first last w z).2 hw
  change nativeGK4AVPolyEval t (nativeGK4BBPolynomialOnAI first last w) =
    nativeGK4AVPolyEval t (nativeGK4BBPolynomialOnAI first last z)
  exact congrArg (nativeGK4AVPolyEval t) hp

/-- At exactly t=4, the universal image factorization is the
identity on the attained old AH matrix value, no extra matrix data. -/
theorem nativeGK4BEAttainedEval_four
    (A : NativeGK4BEAttainedAH first last) :
    nativeGK4BEAttainedEval first last 4 A = A.val := by
  obtain ⟨z, rfl⟩ := nativeGK4BEAttainedAHClass_surjective first last A
  exact
    (nativeGK4BEAttainedEval_class first last 4 z).trans
      (nativeGK4BBPolynomialOnAI_eval_four first last z)

/-- Universal property on the actually attained old AH image:
ANY map reproducing every genuine K_AI evaluation must be THIS map.
It asserts no extension to unattained integer matrices. -/
theorem nativeGK4BEAttainedEval_unique
    (t : Int)
    (F : NativeGK4BEAttainedAH first last → NativeGK4AHMatrix)
    (hF : ∀ z : NativeGK4SKernelClasses
      (nativeGK4AIP92Family p D E) first last,
      F (nativeGK4BEAttainedAHClass first last z) =
        nativeGK4AVPolyEval t (nativeGK4BBPolynomialOnAI first last z)) :
    F = nativeGK4BEAttainedEval first last t := by
  funext A
  obtain ⟨z, rfl⟩ := nativeGK4BEAttainedAHClass_surjective first last A
  exact (hF z).trans (nativeGK4BEAttainedEval_class first last t z).symm

end GenuineKAIKernelAndAttainedImage

section GenuineEvaluationFunctorKernels
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}

/-- Kernel of the old AH Functor on each genuine dependent K_AI
Hom is contained in the kernel of EVERY integer evaluation Functor. -/
theorem nativeGK4BEFunctor_four_kernel_subset
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (X Y : NativeGK4AIKernelStage p ma mb pa pb)
    (u v : X ⟶ Y)
    (t : Int)
    (h4 :
      (nativeGK4BDKAIIntegerEvaluationFunctor p ma mb pa pb 4).map u =
      (nativeGK4BDKAIIntegerEvaluationFunctor p ma mb pa pb 4).map v) :
    (nativeGK4BDKAIIntegerEvaluationFunctor p ma mb pa pb t).map u =
      (nativeGK4BDKAIIntegerEvaluationFunctor p ma mb pa pb t).map v := by
  change nativeGK4AVPolyEval t
      (nativeGK4BBPolynomialOnAI X.original.2.2 Y.original.2.2 u) =
    nativeGK4AVPolyEval t
      (nativeGK4BBPolynomialOnAI X.original.2.2 Y.original.2.2 v)
  change nativeGK4AVPolyEval 4
      (nativeGK4BBPolynomialOnAI X.original.2.2 Y.original.2.2 u) =
    nativeGK4AVPolyEval 4
      (nativeGK4BBPolynomialOnAI X.original.2.2 Y.original.2.2 v) at h4
  exact nativeGK4BEFour_determines_all
    X.original.2.2 Y.original.2.2 u v t h4

/-- The family of ALL integer evaluation functors has the SAME
per-Hom kernel as the genuine old AH functor at t=4. -/
theorem nativeGK4BEFunctor_family_kernel_iff_four
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (X Y : NativeGK4AIKernelStage p ma mb pa pb)
    (u v : X ⟶ Y) :
    (∀ t : Int,
      (nativeGK4BDKAIIntegerEvaluationFunctor p ma mb pa pb t).map u =
        (nativeGK4BDKAIIntegerEvaluationFunctor p ma mb pa pb t).map v) ↔
      (nativeGK4BDOldAHFunctor p ma mb pa pb).map u =
        (nativeGK4BDOldAHFunctor p ma mb pa pb).map v := by
  constructor
  · intro h
    calc
      (nativeGK4BDOldAHFunctor p ma mb pa pb).map u =
          (nativeGK4BDKAIIntegerEvaluationFunctor p ma mb pa pb 4).map u :=
        (nativeGK4BDKAIIntegerEvaluation_four_map p ma mb pa pb X Y u).symm
      _ = (nativeGK4BDKAIIntegerEvaluationFunctor p ma mb pa pb 4).map v :=
        h 4
      _ = (nativeGK4BDOldAHFunctor p ma mb pa pb).map v :=
        nativeGK4BDKAIIntegerEvaluation_four_map p ma mb pa pb X Y v
  · intro h t
    apply nativeGK4BEFunctor_four_kernel_subset p ma mb pa pb X Y u v t
    calc
      (nativeGK4BDKAIIntegerEvaluationFunctor p ma mb pa pb 4).map u =
          (nativeGK4BDOldAHFunctor p ma mb pa pb).map u :=
        nativeGK4BDKAIIntegerEvaluation_four_map p ma mb pa pb X Y u
      _ = (nativeGK4BDOldAHFunctor p ma mb pa pb).map v := h
      _ = (nativeGK4BDKAIIntegerEvaluationFunctor p ma mb pa pb 4).map v :=
        (nativeGK4BDKAIIntegerEvaluation_four_map p ma mb pa pb X Y v).symm

/-- Even the full polynomial functor on K_AI and the genuine old
AH functor have precisely the SAME per-Hom kernel; this says
NEITHER of them is faithful on K_AI. -/
theorem nativeGK4BEFunctor_polynomial_kernel_iff_AH
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (X Y : NativeGK4AIKernelStage p ma mb pa pb)
    (u v : X ⟶ Y) :
    (nativeGK4BCPolynomialValueFunctor p ma mb pa pb).map u =
        (nativeGK4BCPolynomialValueFunctor p ma mb pa pb).map v ↔
      (nativeGK4BDOldAHFunctor p ma mb pa pb).map u =
        (nativeGK4BDOldAHFunctor p ma mb pa pb).map v := by
  change nativeGK4BBPolynomialOnAI X.original.2.2 Y.original.2.2 u =
      nativeGK4BBPolynomialOnAI X.original.2.2 Y.original.2.2 v ↔
    (nativeGK4AIKernelValue X.original.2.2 Y.original.2.2 u).2 =
      (nativeGK4AIKernelValue X.original.2.2 Y.original.2.2 v).2
  exact nativeGK4BBPolynomialOnAI_eq_iff_AH
    X.original.2.2 Y.original.2.2 u v

end GenuineEvaluationFunctorKernels

section GenuineOriginalQAndS
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}
variable {n n' m m' : Nat}
variable (first : KuuNativeF45Tree p n m ma pa mb pb)
variable (last : KuuNativeF45Tree p n' m' ma pa mb pb)

/-- The original Type-valued P92B existence quotient Q has the
same old AH⇒all-integer evaluation implication, without asserting
that Q itself has a category structure. -/
theorem nativeGK4BEP92_four_determines_all
    (q r : NativeF55P92AssocRouteClasses first last)
    (t : Int)
    (h4 : nativeGK4AHP92Value first last q =
      nativeGK4AHP92Value first last r) :
    nativeGK4AUP92Value first last q t =
      nativeGK4AUP92Value first last r t := by
  have hp := nativeGK4BAP92_AH_determines first last q r h4
  calc
    _ = nativeGK4AVPolyEval t (nativeGK4AVP92Value first last q) :=
      (nativeGK4AVP92_eval first last q t).symm
    _ = nativeGK4AVPolyEval t (nativeGK4AVP92Value first last r) :=
      congrArg (nativeGK4AVPolyEval t) hp
    _ = _ := nativeGK4AVP92_eval first last r t

/-- Independent original structural S obtains a SEPARATE typed
statement. This does not identify S and Q or generate old 3-cells. -/
theorem nativeGK4BEStructural_four_determines_all
    (q r : NativeGK4EStructuralRouteClasses first last)
    (t : Int)
    (h4 : nativeGK4AHStructuralValue first last q =
      nativeGK4AHStructuralValue first last r) :
    nativeGK4AUStructuralValue first last q t =
      nativeGK4AUStructuralValue first last r t := by
  have hp := nativeGK4BAStructural_AH_determines first last q r h4
  calc
    _ = nativeGK4AVPolyEval t (nativeGK4AVStructuralValue first last q) :=
      (nativeGK4AVStructural_eval first last q t).symm
    _ = nativeGK4AVPolyEval t (nativeGK4AVStructuralValue first last r) :=
      congrArg (nativeGK4AVPolyEval t) hp
    _ = _ := nativeGK4AVStructural_eval first last r t

end GenuineOriginalQAndS

#print axioms nativeGK4BEFour_determines_all
#print axioms nativeGK4BEPolynomial_eq_iff_four
#print axioms nativeGK4BEAll_eq_iff_four
#print axioms nativeGK4BEAll_eq_iff_polynomial
#print axioms NativeGK4BEAttainedAH
#print axioms nativeGK4BEAttainedAHClass
#print axioms nativeGK4BEAttainedAHClass_surjective
#print axioms nativeGK4BEAttainedEval
#print axioms nativeGK4BEAttainedEval_class
#print axioms nativeGK4BEAttainedEval_four
#print axioms nativeGK4BEAttainedEval_unique
#print axioms nativeGK4BEFunctor_four_kernel_subset
#print axioms nativeGK4BEFunctor_family_kernel_iff_four
#print axioms nativeGK4BEFunctor_polynomial_kernel_iff_AH
#print axioms nativeGK4BEP92_four_determines_all
#print axioms nativeGK4BEStructural_four_determines_all

end
end Kuu.F112.Physical
