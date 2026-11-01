import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4BUChosenInverseTargetNatTransCoherence
import Mathlib.CategoryTheory.EqToHom
import Mathlib.CategoryTheory.Whiskering
import Mathlib.Tactic

/-!
F112-P94D3GK4BV — fully typed two-target composition coherence
of the choice-based inverse comparison Theta, using the original
F45 structural source, attained AH category, and GK4BM genuine
AH-kernel-compatible full subcategory unchanged.

GK4BU proves target-NatTrans modification squares. The next
question is whether Theta_(R ⋙ S) equals a genuine composite
of Theta_R and Theta_S. We insert the pinned Mathlib functor
associators and the exact GK4BN strict target-composition
transport explicitly. We never identify GK4BM's selected
quasi-inverse Q with GK4BP's explicit inverse P by definition.

Append-only / tighten-only / same-root107. Strict 空 center;
independent Kuu is one presentation; no Gray.
Lean v4.30.0-rc2; pinned mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Protected PR #1558 stays Draft/OPEN/unmerged.
No raw F54/F55/P92B higher fillers, source-Q category laws,
unconditional original S faithfulness, ambient unattained integer
matrices, global Gray coherence or higher hyperdescent.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section
universe uD vD uE vE uT vT uU vU uV vV

section TwoTargetChosenInverse
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {T : Type uT} [Category.{vT} T]
variable {U : Type uU} [Category.{vU} U]
variable {V : Type uV} [Category.{vV} V]

/-- Mathlib's actual attained-AH right-whiskering functors
compose strictly as whole Functors under two target changes.
This is NOT a claim about the choice-based inverse Q. -/
theorem nativeGK4BVAttainedTarget_comp
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (R : T ⥤ U) (S : U ⥤ V) :
    nativeGK4BNPostcompAttained p ma mb pa pb (R ⋙ S) =
      nativeGK4BNPostcompAttained p ma mb pa pb R ⋙
        nativeGK4BNPostcompAttained p ma mb pa pb S := by
  rfl

/-- The actual two-step candidate comparison for the arbitrary
GK4BM choice inverse. Every middle object is typed in genuine
functor categories. Left and right boundary transports use
the proved exact GK4BN target composition equalities; the
three associators are Mathlib's actual natural isomorphisms. -/
noncomputable def nativeGK4BVChosenInverse_twoTargetCompositeIso
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (R : T ⥤ U) (S : U ⥤ V) :
    (nativeGK4BNPostcompCompatible p ma mb pa pb (R ⋙ S) ⋙
      nativeGK4BMCompatibleReverseFunctor (T := V) p ma mb pa pb) ≅
    (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb ⋙
      nativeGK4BNPostcompAttained p ma mb pa pb (R ⋙ S)) :=
  eqToIso (congrArg
    (fun W => W ⋙ nativeGK4BMCompatibleReverseFunctor (T := V) p ma mb pa pb)
    (nativeGK4BNPostcompCompatible_comp p ma mb pa pb R S)) ≪≫
  Functor.associator
    (nativeGK4BNPostcompCompatible p ma mb pa pb R)
    (nativeGK4BNPostcompCompatible p ma mb pa pb S)
    (nativeGK4BMCompatibleReverseFunctor (T := V) p ma mb pa pb) ≪≫
  Functor.isoWhiskerLeft
    (nativeGK4BNPostcompCompatible p ma mb pa pb R)
    (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb S) ≪≫
  (Functor.associator
    (nativeGK4BNPostcompCompatible p ma mb pa pb R)
    (nativeGK4BMCompatibleReverseFunctor (T := U) p ma mb pa pb)
    (nativeGK4BNPostcompAttained p ma mb pa pb S)).symm ≪≫
  Functor.isoWhiskerRight
    (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb R)
    (nativeGK4BNPostcompAttained p ma mb pa pb S) ≪≫
  Functor.associator
    (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
    (nativeGK4BNPostcompAttained p ma mb pa pb R)
    (nativeGK4BNPostcompAttained p ma mb pa pb S) ≪≫
  eqToIso (congrArg
    (fun W => nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb ⋙ W)
    (nativeGK4BVAttainedTarget_comp p ma mb pa pb R S).symm)

/-- Pseudonatural composition: the directly constructed GK4BT
comparison Theta_(R⋙S) is exactly the honestly whiskered
two-step comparison, including both strict target-action
transport isomorphisms and all three associators. -/
theorem nativeGK4BVChosenInverse_composition_coherence
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (R : T ⥤ U) (S : U ⥤ V) :
    nativeGK4BVChosenInverse_twoTargetCompositeIso p ma mb pa pb R S =
      nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S) := by
  apply Iso.ext
  ext H X
  simp [nativeGK4BVChosenInverse_twoTargetCompositeIso,
    nativeGK4BTChosenInverse_targetNatIso,
    Functor.associator, Functor.isoWhiskerLeft,
    Functor.isoWhiskerRight]
  simp only [eqToHom_app, eqToHom_map, eqToHom_refl,
    Category.comp_id, Category.id_comp]

end TwoTargetChosenInverse

#print axioms nativeGK4BVAttainedTarget_comp
#print axioms nativeGK4BVChosenInverse_twoTargetCompositeIso
#print axioms nativeGK4BVChosenInverse_composition_coherence

end
end Kuu.F112.Physical
