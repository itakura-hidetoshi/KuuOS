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

universe uB vB uC vC uF vF uG vG
section AbstractEqualityTransport
variable {B : Type uB} [Category.{vB} B]
variable {C : Type uC} [Category.{vC} C]
variable {F : Type uF} [Category.{vF} F]
variable {G : Type uG} [Category.{vG} G]

/-- Pinned Mathlib's actual functor associator is the
canonical natural isomorphism of its definitional associativity. -/
private theorem nativeGK4BVAssociator_eqToIso
    (A : B ⥤ C) (W : C ⥤ F) (Z : F ⥤ G) :
    Functor.associator A W Z = eqToIso (Functor.assoc A W Z) := by
  apply Iso.ext
  ext X
  rfl

/-- Equality transports commute with honest left whiskering. -/
private theorem nativeGK4BVWhiskerLeft_eqToIso
    (A : B ⥤ C) {W Z : C ⥤ F} (h : W = Z) :
    Functor.isoWhiskerLeft A (eqToIso h) =
      eqToIso (congrArg (fun K : C ⥤ F => A ⋙ K) h) := by
  cases h
  simp only [eqToIso_refl, Functor.isoWhiskerLeft_refl]

/-- Equality transports commute with honest right whiskering. -/
private theorem nativeGK4BVWhiskerRight_eqToIso
    {A W : B ⥤ C} (h : A = W) (Z : C ⥤ F) :
    Functor.isoWhiskerRight (eqToIso h) Z =
      eqToIso (congrArg (fun K : B ⥤ C => K ⋙ Z) h) := by
  cases h
  simp only [eqToIso_refl, Functor.isoWhiskerRight_refl]

/-- Reversing an equality reverses its genuine Mathlib iso. -/
private theorem nativeGK4BVSymm_eqToIso
    {A W : B} (h : A = W) :
    (eqToIso h).symm = eqToIso h.symm := by
  cases h
  rfl

end AbstractEqualityTransport

universe uA0 vA0 uA1 vA1 uA2 vA2 uB0 vB0 uB1 vB1 uB2 vB2
section AbstractGaugeComposition
variable {A0 : Type uA0} [Category.{vA0} A0]
variable {A1 : Type uA1} [Category.{vA1} A1]
variable {A2 : Type uA2} [Category.{vA2} A2]
variable {B0 : Type uB0} [Category.{vB0} B0]
variable {B1 : Type uB1} [Category.{vB1} B1]
variable {B2 : Type uB2} [Category.{vB2} B2]

/-- General two-stage gauge cancellation in genuine Mathlib
functor categories. The middle k1.symm and k1 are pasted
through associators and whiskering; this is exactly the
2-categorical coherence required to transport strict P to
arbitrary-choice Q without inventing extra source cells. -/
private theorem nativeGK4BVGaugeComposition
    (wholeC : A0 ⥤ A2) (wholeA : B0 ⥤ B2)
    (cR : A0 ⥤ A1) (cS : A1 ⥤ A2)
    (aR : B0 ⥤ B1) (aS : B1 ⥤ B2)
    (p0 q0 : A0 ⥤ B0) (p1 q1 : A1 ⥤ B1) (p2 q2 : A2 ⥤ B2)
    (k0 : q0 ≅ p0) (k1 : q1 ≅ p1) (k2 : q2 ≅ p2)
    (hc : wholeC ≅ cR ⋙ cS) (ha : aR ⋙ aS ≅ wholeA)
    (hR : cR ⋙ p1 ≅ p0 ⋙ aR)
    (hS : cS ⋙ p2 ≅ p1 ⋙ aS) :
    Functor.isoWhiskerRight hc q2 ≪≫
      Functor.associator cR cS q2 ≪≫
      Functor.isoWhiskerLeft cR
        (Functor.isoWhiskerLeft cS k2 ≪≫ hS ≪≫
          Functor.isoWhiskerRight k1.symm aS) ≪≫
      (Functor.associator cR q1 aS).symm ≪≫
      Functor.isoWhiskerRight
        (Functor.isoWhiskerLeft cR k1 ≪≫ hR ≪≫
          Functor.isoWhiskerRight k0.symm aR) aS ≪≫
      Functor.associator q0 aR aS ≪≫
      Functor.isoWhiskerLeft q0 ha =
    Functor.isoWhiskerLeft wholeC k2 ≪≫
      (Functor.isoWhiskerRight hc p2 ≪≫
        Functor.associator cR cS p2 ≪≫
        Functor.isoWhiskerLeft cR hS ≪≫
        (Functor.associator cR p1 aS).symm ≪≫
        Functor.isoWhiskerRight hR aS ≪≫
        Functor.associator p0 aR aS ≪≫
        Functor.isoWhiskerLeft p0 ha) ≪≫
      Functor.isoWhiskerRight k0.symm wholeA := by
  apply Iso.ext
  ext X
  simp only [Iso.trans_hom, Functor.isoWhiskerLeft_hom,
    Functor.isoWhiskerRight_hom, Functor.associator_hom_app,
    NatTrans.comp_app, Functor.whiskerLeft_app, Functor.whiskerRight_app,
    Iso.symm_hom, Functor.associator_inv_app,
    Category.id_comp, Category.comp_id, Functor.map_comp, Category.assoc]
  have hCancel :
      aS.map (k1.inv.app (cR.obj X)) ≫
        aS.map (k1.hom.app (cR.obj X)) = 𝟙 _ := by
    rw [← aS.map_comp, Iso.inv_hom_id_app, aS.map_id]
  have hCancel_assoc {Z : B2}
      (f : aS.obj (p1.obj (cR.obj X)) ⟶ Z) :
      aS.map (k1.inv.app (cR.obj X)) ≫
        (aS.map (k1.hom.app (cR.obj X)) ≫ f) = f := by
    rw [← Category.assoc, hCancel, Category.id_comp]
  simp only [Category.id_comp, Category.comp_id]
  simp only [← Category.assoc]
  rw [k2.hom.naturality (hc.hom.app X)]
  simp only [Category.assoc, hCancel_assoc, Category.id_comp, Category.comp_id]
  rw [ha.hom.naturality (k0.inv.app X)]
  simp only [Category.assoc]

end AbstractGaugeComposition

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

/-- For the EXPLICIT GK4BP inverse P only: the
two-stage comparison is built solely from the strict target
equality squares, canonical associators, and their transports.
There is no arbitrary-choice Q in this isomorphism. -/
noncomputable def nativeGK4BVExplicitInverse_twoTargetCompositeIso
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (R : T ⥤ U) (S : U ⥤ V) :
    (nativeGK4BNPostcompCompatible p ma mb pa pb (R ⋙ S) ⋙
      nativeGK4BPExplicitInverseFunctor (T := V) p ma mb pa pb) ≅
    (nativeGK4BPExplicitInverseFunctor (T := T) p ma mb pa pb ⋙
      nativeGK4BNPostcompAttained p ma mb pa pb (R ⋙ S)) :=
  eqToIso (congrArg
    (fun W => W ⋙ nativeGK4BPExplicitInverseFunctor (T := V) p ma mb pa pb)
    (nativeGK4BNPostcompCompatible_comp p ma mb pa pb R S)) ≪≫
  Functor.associator
    (nativeGK4BNPostcompCompatible p ma mb pa pb R)
    (nativeGK4BNPostcompCompatible p ma mb pa pb S)
    (nativeGK4BPExplicitInverseFunctor (T := V) p ma mb pa pb) ≪≫
  Functor.isoWhiskerLeft
    (nativeGK4BNPostcompCompatible p ma mb pa pb R)
    (eqToIso (nativeGK4BPExplicitInverse_target_square p ma mb pa pb S)) ≪≫
  (Functor.associator
    (nativeGK4BNPostcompCompatible p ma mb pa pb R)
    (nativeGK4BPExplicitInverseFunctor (T := U) p ma mb pa pb)
    (nativeGK4BNPostcompAttained p ma mb pa pb S)).symm ≪≫
  Functor.isoWhiskerRight
    (eqToIso (nativeGK4BPExplicitInverse_target_square p ma mb pa pb R))
    (nativeGK4BNPostcompAttained p ma mb pa pb S) ≪≫
  Functor.associator
    (nativeGK4BPExplicitInverseFunctor (T := T) p ma mb pa pb)
    (nativeGK4BNPostcompAttained p ma mb pa pb R)
    (nativeGK4BNPostcompAttained p ma mb pa pb S) ≪≫
  eqToIso (congrArg
    (fun W => nativeGK4BPExplicitInverseFunctor (T := T) p ma mb pa pb ⋙ W)
    (nativeGK4BVAttainedTarget_comp p ma mb pa pb R S).symm)

/-- The two-stage STRICT explicit inverse transport equals
the DIRECT GK4BP target-square equality transport. Unlike
the chosen inverse Q, all isomorphisms here originate in
real equalities; proof irrelevance makes the final witness
canonical, without equating choice inverses. -/
theorem nativeGK4BVExplicitInverse_twoTarget_eq_direct
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (R : T ⥤ U) (S : U ⥤ V) :
    nativeGK4BVExplicitInverse_twoTargetCompositeIso p ma mb pa pb R S =
      eqToIso (nativeGK4BPExplicitInverse_target_square
        p ma mb pa pb (R ⋙ S)) := by
  simp only [nativeGK4BVExplicitInverse_twoTargetCompositeIso,
    nativeGK4BVAssociator_eqToIso,
    nativeGK4BVWhiskerLeft_eqToIso,
    nativeGK4BVWhiskerRight_eqToIso,
    nativeGK4BVSymm_eqToIso, eqToIso_trans]

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
  have h := nativeGK4BVGaugeComposition
    (nativeGK4BNPostcompCompatible p ma mb pa pb (R ⋙ S))
    (nativeGK4BNPostcompAttained p ma mb pa pb (R ⋙ S))
    (nativeGK4BNPostcompCompatible p ma mb pa pb R)
    (nativeGK4BNPostcompCompatible p ma mb pa pb S)
    (nativeGK4BNPostcompAttained p ma mb pa pb R)
    (nativeGK4BNPostcompAttained p ma mb pa pb S)
    (nativeGK4BPExplicitInverseFunctor (T := T) p ma mb pa pb)
    (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
    (nativeGK4BPExplicitInverseFunctor (T := U) p ma mb pa pb)
    (nativeGK4BMCompatibleReverseFunctor (T := U) p ma mb pa pb)
    (nativeGK4BPExplicitInverseFunctor (T := V) p ma mb pa pb)
    (nativeGK4BMCompatibleReverseFunctor (T := V) p ma mb pa pb)
    (nativeGK4BQChosenInverseComparisonIso (T := T) p ma mb pa pb)
    (nativeGK4BQChosenInverseComparisonIso (T := U) p ma mb pa pb)
    (nativeGK4BQChosenInverseComparisonIso (T := V) p ma mb pa pb)
    (eqToIso (nativeGK4BNPostcompCompatible_comp p ma mb pa pb R S))
    (eqToIso (nativeGK4BVAttainedTarget_comp p ma mb pa pb R S).symm)
    (eqToIso (nativeGK4BPExplicitInverse_target_square p ma mb pa pb R))
    (eqToIso (nativeGK4BPExplicitInverse_target_square p ma mb pa pb S))
  simpa only [nativeGK4BVChosenInverse_twoTargetCompositeIso,
    nativeGK4BVExplicitInverse_twoTargetCompositeIso,
    nativeGK4BTChosenInverse_targetNatIso,
    nativeGK4BVWhiskerRight_eqToIso,
    nativeGK4BVWhiskerLeft_eqToIso,
    nativeGK4BVExplicitInverse_twoTarget_eq_direct] using h

end TwoTargetChosenInverse

#print axioms nativeGK4BVAttainedTarget_comp
#print axioms nativeGK4BVChosenInverse_twoTargetCompositeIso
#print axioms nativeGK4BVExplicitInverse_twoTargetCompositeIso
#print axioms nativeGK4BVExplicitInverse_twoTarget_eq_direct
#print axioms nativeGK4BVChosenInverse_composition_coherence

end
end Kuu.F112.Physical
