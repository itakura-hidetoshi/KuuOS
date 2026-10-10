import KUOS.DependentOriginationCoherentBiadjunctionHorizontalChainFunctorsV5_127

namespace KUOS.DependentOriginationCoherentBiadjunctionHorizontalQuotientFunctorsV5_127

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionFiniteMateComparisonChainsV5_122.Generic
open KUOS.DependentOriginationCoherentBiadjunctionFiniteComparisonChainConcatenationV5_123.Generic
open KUOS.DependentOriginationCoherentBiadjunctionComparisonCompressionFunctorV5_124.Generic
open KUOS.DependentOriginationCoherentBiadjunctionComparisonKernelHomQuotientV5_125.Generic
open KUOS.DependentOriginationCoherentBiadjunctionCompressionKernelQuotientCategoryV5_125.Generic
open KUOS.DependentOriginationCoherentBiadjunctionNonstrictKernelWhiskeringV5_126.Generic
open KUOS.DependentOriginationCoherentBiadjunctionHorizontalCompositeFunctorsV5_127.Generic
open KUOS.DependentOriginationCoherentBiadjunctionHorizontalChainFunctorsV5_127.Generic

set_option autoImplicit false
noncomputable section

/-!
# F30 / v5.127: genuine kernel quotient category horizontal FUNCTORS

The stagewise horizontal operations from F30-B preserve the exact F28
compression-kernel congruence. Both therefore descend through mathlib's
actual Quotient.lift to FUNCTORS between original kernel quotient
categories. These functors preserve identities and vertical compositions,
and their morphism-level compression is the genuine F29 whiskering of
the original F-ISO and potentially noninvertible G-2-cell.

No faithfulness of the raw F26 compression or ambient biequivalence.
-/

namespace Generic

universe uC vC wC
variable {C : Type uC} [Bicategory.{wC, vC} C]

/-- Exact F28 kernel congruence is preserved by the left horizontal
action on ALL the original comparison stages. -/
theorem leftWhiskerChain_kernel (aF bF aG bG : C)
    {eF eG : C} (uF : eF ⟶ aF) (uG : eG ⟶ aG)
    {x y : ComparisonPair aF bF aG bG} {c d : x ⟶ y}
    (h : (compressionKernelHomRel aF bF aG bG) c d) :
    (compressionKernelHomRel eF bF eG bG)
      (leftWhiskerChain uF uG c) (leftWhiskerChain uF uG d) := by
  obtain ⟨hf, hg⟩ :=
    (comparisonCompressionFunctor_map_eq_iff aF bF aG bG c d).mp h
  change (leftWhiskerChain uF uG c).fComposite =
      (leftWhiskerChain uF uG d).fComposite ∧
    (leftWhiskerChain uF uG c).gComposite =
      (leftWhiskerChain uF uG d).gComposite
  constructor
  · rw [leftWhiskerChain_fComposite, leftWhiskerChain_fComposite, hf]
  · rw [leftWhiskerChain_gComposite, leftWhiskerChain_gComposite, hg]

/-- Exact F28 kernel congruence is likewise preserved by right
whiskering; G remains arbitrary, with no inverse used. -/
theorem rightWhiskerChain_kernel (aF bF aG bG : C)
    {eF eG : C} (vF : bF ⟶ eF) (vG : bG ⟶ eG)
    {x y : ComparisonPair aF bF aG bG} {c d : x ⟶ y}
    (h : (compressionKernelHomRel aF bF aG bG) c d) :
    (compressionKernelHomRel aF eF aG eG)
      (rightWhiskerChain vF vG c) (rightWhiskerChain vF vG d) := by
  obtain ⟨hf, hg⟩ :=
    (comparisonCompressionFunctor_map_eq_iff aF bF aG bG c d).mp h
  change (rightWhiskerChain vF vG c).fComposite =
      (rightWhiskerChain vF vG d).fComposite ∧
    (rightWhiskerChain vF vG c).gComposite =
      (rightWhiskerChain vF vG d).gComposite
  constructor
  · rw [rightWhiskerChain_fComposite, rightWhiskerChain_fComposite, hf]
  · rw [rightWhiskerChain_gComposite, rightWhiskerChain_gComposite, hg]

/-- Real LEFT whiskering functor between mathlib F28 compression-kernel
QUOTIENT categories; native finite chain operations, not reselected
comparison pair presentations. -/
def leftKernelQuotientWhiskerFunctor (aF bF aG bG : C)
    {eF eG : C} (uF : eF ⟶ aF) (uG : eG ⟶ aG) :
    compressionKernelCategory aF bF aG bG ⥤
      compressionKernelCategory eF bF eG bG :=
  CategoryTheory.Quotient.lift (compressionKernelHomRel aF bF aG bG)
    (leftPathWhiskerFunctor aF bF aG bG uF uG ⋙
      comparisonKernelQuotientFunctor eF bF eG bG)
    (by
      intro x y c d h
      change (comparisonKernelQuotientFunctor eF bF eG bG).map
          (leftWhiskerChain uF uG c) =
        (comparisonKernelQuotientFunctor eF bF eG bG).map
          (leftWhiskerChain uF uG d)
      apply (kernelQuotient_map_eq_iff eF bF eG bG _ _).2
      exact leftWhiskerChain_kernel aF bF aG bG uF uG h)

/-- Real RIGHT whiskering functor between the original kernel quotient
categories, induced by genuine finite comparison chains. -/
def rightKernelQuotientWhiskerFunctor (aF bF aG bG : C)
    {eF eG : C} (vF : bF ⟶ eF) (vG : bG ⟶ eG) :
    compressionKernelCategory aF bF aG bG ⥤
      compressionKernelCategory aF eF aG eG :=
  CategoryTheory.Quotient.lift (compressionKernelHomRel aF bF aG bG)
    (rightPathWhiskerFunctor aF bF aG bG vF vG ⋙
      comparisonKernelQuotientFunctor aF eF aG eG)
    (by
      intro x y c d h
      change (comparisonKernelQuotientFunctor aF eF aG eG).map
          (rightWhiskerChain vF vG c) =
        (comparisonKernelQuotientFunctor aF eF aG eG).map
          (rightWhiskerChain vF vG d)
      apply (kernelQuotient_map_eq_iff aF eF aG eG _ _).2
      exact rightWhiskerChain_kernel aF bF aG bG vF vG h)

/-- The quotient left functor retains the actual F26 path lift, not
just an abstract equivalence chosen on the target category. -/
theorem leftKernelQuotientWhisker_onPath (aF bF aG bG : C)
    {eF eG : C} (uF : eF ⟶ aF) (uG : eG ⟶ aG)
    {x y : ComparisonPair aF bF aG bG} (c : x ⟶ y) :
    (leftKernelQuotientWhiskerFunctor aF bF aG bG uF uG).map
      ((comparisonKernelQuotientFunctor aF bF aG bG).map c) =
    (comparisonKernelQuotientFunctor eF bF eG bG).map
      (leftWhiskerChain uF uG c) := by
  rfl

/-- The quotient right functor retains the original path lift. -/
theorem rightKernelQuotientWhisker_onPath (aF bF aG bG : C)
    {eF eG : C} (vF : bF ⟶ eF) (vG : bG ⟶ eG)
    {x y : ComparisonPair aF bF aG bG} (c : x ⟶ y) :
    (rightKernelQuotientWhiskerFunctor aF bF aG bG vF vG).map
      ((comparisonKernelQuotientFunctor aF bF aG bG).map c) =
    (comparisonKernelQuotientFunctor aF eF aG eG).map
      (rightWhiskerChain vF vG c) := by
  rfl

/-- Genuine compression of EVERY quotient-class morphism after left
whiskering is exactly its original F29 componentwise horizontal action. -/
theorem leftKernelQuotientWhisker_compression (aF bF aG bG : C)
    {eF eG : C} (uF : eF ⟶ aF) (uG : eG ⟶ aG)
    {x y : compressionKernelCategory aF bF aG bG} (q : x ⟶ y) :
    (quotientCompositeFunctor eF bF eG bG).map
      ((leftKernelQuotientWhiskerFunctor aF bF aG bG uF uG).map q) =
    (leftCompositeWhiskerFunctor aF bF aG bG uF uG).map
      ((quotientCompositeFunctor aF bF aG bG).map q) := by
  induction q using Quot.inductionOn with
  | _ c =>
      change ((leftWhiskerChain uF uG c).fComposite,
        (leftWhiskerChain uF uG c).gComposite) =
        (Bicategory.whiskerLeftIso uF c.fComposite, uG ◁ c.gComposite)
      exact Prod.ext (leftWhiskerChain_fComposite uF uG c)
        (leftWhiskerChain_gComposite uF uG c)

/-- Same exact quotient-morphism compression comparison for RIGHT
whiskering of the original F ISO and arbitrary G 2-cell. -/
theorem rightKernelQuotientWhisker_compression (aF bF aG bG : C)
    {eF eG : C} (vF : bF ⟶ eF) (vG : bG ⟶ eG)
    {x y : compressionKernelCategory aF bF aG bG} (q : x ⟶ y) :
    (quotientCompositeFunctor aF eF aG eG).map
      ((rightKernelQuotientWhiskerFunctor aF bF aG bG vF vG).map q) =
    (rightCompositeWhiskerFunctor aF bF aG bG vF vG).map
      ((quotientCompositeFunctor aF bF aG bG).map q) := by
  induction q using Quot.inductionOn with
  | _ c =>
      change ((rightWhiskerChain vF vG c).fComposite,
        (rightWhiskerChain vF vG c).gComposite) =
        (Bicategory.whiskerRightIso c.fComposite vF, c.gComposite ▷ vG)
      exact Prod.ext (rightWhiskerChain_fComposite vF vG c)
        (rightWhiskerChain_gComposite vF vG c)

/-- Identity law holds ON the genuine kernel quotient CATEGORY. -/
theorem leftKernelQuotientWhisker_map_id (aF bF aG bG : C)
    {eF eG : C} (uF : eF ⟶ aF) (uG : eG ⟶ aG)
    (x : compressionKernelCategory aF bF aG bG) :
    (leftKernelQuotientWhiskerFunctor aF bF aG bG uF uG).map (𝟙 x) =
      𝟙 ((leftKernelQuotientWhiskerFunctor aF bF aG bG uF uG).obj x) :=
  (leftKernelQuotientWhiskerFunctor aF bF aG bG uF uG).map_id x

/-- Composition law holds for arbitrary quotient morphisms, not only
representatives, including noninvertible G comparisons. -/
theorem leftKernelQuotientWhisker_map_comp (aF bF aG bG : C)
    {eF eG : C} (uF : eF ⟶ aF) (uG : eG ⟶ aG)
    {x y z : compressionKernelCategory aF bF aG bG}
    (p : x ⟶ y) (q : y ⟶ z) :
    (leftKernelQuotientWhiskerFunctor aF bF aG bG uF uG).map (p ≫ q) =
      (leftKernelQuotientWhiskerFunctor aF bF aG bG uF uG).map p ≫
      (leftKernelQuotientWhiskerFunctor aF bF aG bG uF uG).map q :=
  (leftKernelQuotientWhiskerFunctor aF bF aG bG uF uG).map_comp p q

/-- Right quotient horizontal operation preserves all identities. -/
theorem rightKernelQuotientWhisker_map_id (aF bF aG bG : C)
    {eF eG : C} (vF : bF ⟶ eF) (vG : bG ⟶ eG)
    (x : compressionKernelCategory aF bF aG bG) :
    (rightKernelQuotientWhiskerFunctor aF bF aG bG vF vG).map (𝟙 x) =
      𝟙 ((rightKernelQuotientWhiskerFunctor aF bF aG bG vF vG).obj x) :=
  (rightKernelQuotientWhiskerFunctor aF bF aG bG vF vG).map_id x

/-- Right quotient horizontal operation preserves all compositions. -/
theorem rightKernelQuotientWhisker_map_comp (aF bF aG bG : C)
    {eF eG : C} (vF : bF ⟶ eF) (vG : bG ⟶ eG)
    {x y z : compressionKernelCategory aF bF aG bG}
    (p : x ⟶ y) (q : y ⟶ z) :
    (rightKernelQuotientWhiskerFunctor aF bF aG bG vF vG).map (p ≫ q) =
      (rightKernelQuotientWhiskerFunctor aF bF aG bG vF vG).map p ≫
      (rightKernelQuotientWhiskerFunctor aF bF aG bG vF vG).map q :=
  (rightKernelQuotientWhiskerFunctor aF bF aG bG vF vG).map_comp p q

#print axioms leftWhiskerChain_kernel
#print axioms rightWhiskerChain_kernel
#print axioms leftKernelQuotientWhiskerFunctor
#print axioms rightKernelQuotientWhiskerFunctor
#print axioms leftKernelQuotientWhisker_onPath
#print axioms rightKernelQuotientWhisker_onPath
#print axioms leftKernelQuotientWhisker_compression
#print axioms rightKernelQuotientWhisker_compression
#print axioms leftKernelQuotientWhisker_map_id
#print axioms leftKernelQuotientWhisker_map_comp
#print axioms rightKernelQuotientWhisker_map_id
#print axioms rightKernelQuotientWhisker_map_comp

end Generic

end

end KUOS.DependentOriginationCoherentBiadjunctionHorizontalQuotientFunctorsV5_127
