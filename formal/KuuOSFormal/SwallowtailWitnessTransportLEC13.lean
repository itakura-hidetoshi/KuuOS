import KuuOSFormal.HistoricalNativeF55CommonShadowLEC12
import KUOS.DependentOriginationCoherentBiadjunctionSwallowtailModificationExchangeV5_112

/-!
# LEC-13 — original swallowtail-certified transport of typed witnesses

The new ingredient is NOT a postulated old-F54/native-F54 equivalence.
The retained v5.101 actual-lift datum already proves both original
swallowtail laws, on the SAME F/G/unit/counit and independently constructed
interchangers. We use those precise boundary isomorphisms to transport
endomorphism witnesses by conjugation, without replacing raw F55 terms.

1. On any category, conjugation is a reversible witness equivalence. It
   preserves ordered composition, finite histories and exact function-sheaf
   gluing; it also REFLECTS compatibility and global existence.
2. On the actual original StrongTrans modification boundaries, v5.112
   swallowtail exchange proves that this transport sends a unit/counit
   modification whiskered with one triangle to the SAME modification
   whiskered with the other triangle. This is where swallowtail is used;
   invertibility alone would not supply that identification.
3. LEC-12's actual historical F55 raw collision remains a collision after
   every shadow-only readout followed by such reversible transport. A
   coherent change of boundary does not recover information erased before
   transport. No old/native source map is manufactured from numeric equality.

This mixed module belongs only to KuuOSFormal, not independent KuuOSStrict.
No raw F54/F55/P77/GK5CG equivalence, geometric endpoint identification,
higher-stack effectivity, nonzero H1 or external execution is asserted.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace KUOS.LivingEngiSwallowtail

open CategoryTheory
open Kuu.LivingEngi

set_option autoImplicit false
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uCat vCat uBase uIndex uRaw

section ExactWitnessTransport
variable {C : Type uCat} [Category.{vCat} C] {a b c : C}

/-- Transport an actual endomorphism witness, with both inverse boundary
maps retained. This is NOT a quotient or a choice of raw representative. -/
def witnessConjugation (e : a ≅ b) : (a ⟶ a) ≃ (b ⟶ b) where
  toFun f := e.inv ≫ f ≫ e.hom
  invFun g := e.hom ≫ g ≫ e.inv
  left_inv f := by simp [Category.assoc]
  right_inv g := by simp [Category.assoc]

/-- Genuine equality of witnesses is reflected, not just preserved. -/
theorem witnessConjugation_eq_iff (e : a ≅ b) (f g : a ⟶ a) :
    witnessConjugation e f = witnessConjugation e g ↔ f = g :=
  (witnessConjugation e).injective.eq_iff

/-- Ordered categorical composition is preserved; no commutation or
interchange of the raw sequence is imposed. -/
theorem witnessConjugation_comp (e : a ≅ b) (f g : a ⟶ a) :
    witnessConjugation e (f ≫ g) =
      witnessConjugation e f ≫ witnessConjugation e g := by
  simp [witnessConjugation, Category.assoc]

theorem witnessConjugation_id (e : a ≅ b) :
    witnessConjugation e (𝟙 a) = 𝟙 b := by
  simp [witnessConjugation]

/-- Two successive boundary transports agree with the genuine composite
isomorphism, with its inverse in the correct opposite order. -/
theorem witnessConjugation_trans (e : a ≅ b) (d : b ≅ c) (f : a ⟶ a) :
    witnessConjugation (e ≪≫ d) f =
      witnessConjugation d (witnessConjugation e f) := by
  simp [witnessConjugation, Category.assoc]

/-- The entire finite list is recovered, not merely its composite or a
numeric digest. No original history is discarded by this transport. -/
theorem witnessHistory_roundtrip (e : a ≅ b) (history : List (a ⟶ a)) :
    (history.map (witnessConjugation e)).map
        (witnessConjugation e).symm = history := by
  simp

/-- Two histories become equal after transport exactly when they were
already equal as ordered lists of the original morphism witnesses. -/
theorem witnessHistory_eq_iff
    (e : a ≅ b) (h₁ h₂ : List (a ⟶ a)) :
    h₁.map (witnessConjugation e) = h₂.map (witnessConjugation e) ↔
      h₁ = h₂ := by
  constructor
  · intro h
    have hr := congrArg (List.map (witnessConjugation e).symm) h
    simpa only [witnessHistory_roundtrip] using hr
  · intro h
    exact congrArg (List.map (witnessConjugation e)) h

/-- Reversible boundary transport preserves AND reflects ordinary
pointwise overlap compatibility for actual endomorphism-valued sections. -/
theorem witnessConjugation_compatible_iff
    {X : Type uBase} {I : Type uIndex}
    (e : a ≅ b) (U : I → Set X) (s : LocalSections U (a ⟶ a)) :
    Compatible U (shadowSections U (witnessConjugation e) s) ↔
      Compatible U s := by
  constructor
  · intro h i j x hi hj
    exact (witnessConjugation e).injective (h i j x hi hj)
  · exact sourceCompatible_implies_shadowCompatible
      U (witnessConjugation e) s

/-- No cover or injectivity assumption is omitted: transport has a
constructed inverse on the whole witness type, so global sections can be
transported in both directions even for a non-covering family. This is an
ordinary function-sheaf result, not arbitrary higher-stack effectivity. -/
theorem witnessConjugation_hasGlobal_iff
    {X : Type uBase} {I : Type uIndex}
    (e : a ≅ b) (U : I → Set X) (s : LocalSections U (a ⟶ a)) :
    HasGlobal U (shadowSections U (witnessConjugation e) s) ↔
      HasGlobal U s := by
  constructor
  · rintro ⟨g, hg⟩
    refine ⟨fun x => (witnessConjugation e).symm (g x), ?_⟩
    intro i x
    have h := congrArg (witnessConjugation e).symm (hg i x)
    simpa only [shadowSections, Equiv.symm_apply_apply] using h
  · exact sourceGlobal_implies_shadowGlobal U (witnessConjugation e) s

/-- Exact reconstruction from a readout is unchanged by a reversible
change of receiver coordinates. This does not grant reconstruction from
an already information-losing source observation. -/
theorem witnessConjugation_factors_iff
    {Raw : Type uRaw} (e : a ≅ b) (readout : Raw → (a ⟶ a)) :
    Factors (fun r => witnessConjugation e (readout r))
        (fun r : Raw => r) ↔
      Factors readout (fun r : Raw => r) := by
  constructor
  · rintro ⟨recover, h⟩
    exact ⟨fun z => recover (witnessConjugation e z), h⟩
  · rintro ⟨recover, h⟩
    refine ⟨fun z => recover ((witnessConjugation e).symm z), ?_⟩
    intro r
    simpa only [Equiv.symm_apply_apply] using h r

/-- Normalize an exact comparison of two isomorphisms to the identity
of the TARGET. This is the orientation used for the swallowtail defect. -/
theorem comparison_defect_eq_id_iff (sigma paste : a ≅ b) :
    sigma.inv ≫ paste.hom = 𝟙 b ↔ sigma = paste := by
  constructor
  · intro h
    apply Iso.ext
    have h' := congrArg (fun f => sigma.hom ≫ f) h
    simpa [Category.assoc] using h'.symm
  · intro h
    subst paste
    exact sigma.inv_hom_id

end ExactWitnessTransport

section SwallowtailBoundaries
open scoped CategoryTheory.Bicategory CategoryTheory.Pseudofunctor.StrongTrans
open KUOS.DependentOriginationBiadjunctionTriangulatorHorizontalPastesV5_64.Generic.IncoherentBiadjunctionDatum
open KUOS.DependentOriginationForwardSwallowtailPredicateV5_65.Generic.IncoherentBiadjunctionDatum
open KUOS.DependentOriginationReverseSwallowtailPredicateV5_66.Generic.IncoherentBiadjunctionDatum

universe uB vB wB uC vC wC
variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]
variable (D :
  KUOS.DependentOriginationCoherentBiadjunctionActualLiftV5_101.Generic.CoherentBiadjunctionDatum B C)

/- Pin precisely the four existing modification hom categories. -/
local instance sourceRoundtripHom :
    Category (Pseudofunctor.StrongTrans
      (sourceRoundtrip D.datum) (sourceRoundtrip D.datum)) :=
  Pseudofunctor.StrongTrans.homCategory (B := B) (C := B)
    (F := sourceRoundtrip D.datum) (G := sourceRoundtrip D.datum)

local instance targetRoundtripHom :
    Category (Pseudofunctor.StrongTrans
      (targetRoundtrip D.datum) (targetRoundtrip D.datum)) :=
  Pseudofunctor.StrongTrans.homCategory (B := C) (C := C)
    (F := targetRoundtrip D.datum) (G := targetRoundtrip D.datum)

local instance forwardBoundaryHom :
    Category (Pseudofunctor.StrongTrans
      (Pseudofunctor.id B) (sourceRoundtrip D.datum)) :=
  Pseudofunctor.StrongTrans.homCategory (B := B) (C := B)
    (F := Pseudofunctor.id B) (G := sourceRoundtrip D.datum)

local instance reverseBoundaryHom :
    Category (Pseudofunctor.StrongTrans
      (targetRoundtrip D.datum) (Pseudofunctor.id C)) :=
  Pseudofunctor.StrongTrans.homCategory (B := C) (C := C)
    (F := targetRoundtrip D.datum) (G := Pseudofunctor.id C)

/-- Reversible witness transport on the ORIGINAL unit-centered boundary. -/
def forwardWitnessTransport := witnessConjugation D.forwardInterchanger

/-- Reversible witness transport on the ORIGINAL counit-centered boundary. -/
def reverseWitnessTransport := witnessConjugation D.reverseInterchanger

/-- The original forward swallowtail has zero normalized defect. The
interchanger has NOT been redefined to be the triangulator paste. -/
theorem forward_swallowtail_defect_identity :
    D.forwardInterchanger.inv ≫ (forwardTriangulatorPaste D.datum).hom =
      𝟙 (forwardSwallowtailRight D.datum) :=
  (comparison_defect_eq_id_iff D.forwardInterchanger
    (forwardTriangulatorPaste D.datum)).2 D.forward_swallowtail

/-- The OTHER, independently certified original swallowtail orientation. -/
theorem reverse_swallowtail_defect_identity :
    D.reverseInterchanger.inv ≫ (reverseTriangulatorPaste D.datum).hom =
      𝟙 (reverseSwallowtailRight D.datum) :=
  (comparison_defect_eq_id_iff D.reverseInterchanger
    (reverseTriangulatorPaste D.datum)).2 D.reverse_swallowtail

/-- Swallowtail is used essentially here: transport agrees with the
specified unit modification on the OTHER triangle boundary, by the old
whisker-exchange theorem, not merely because an isomorphism exists. -/
theorem forwardWitnessTransport_unit_modification
    (Gamma : Pseudofunctor.StrongTrans.Modification
      D.datum.base.unit D.datum.base.unit) :
    forwardWitnessTransport D
        ((Pseudofunctor.StrongTrans.Hom.of Gamma) ▷
          (sourceForwardTriangulator D.datum).triangle) =
      (Pseudofunctor.StrongTrans.Hom.of Gamma) ▷
        (sourceReverseTriangulator D.datum).triangle := by
  change D.forwardInterchanger.inv ≫
    ((Pseudofunctor.StrongTrans.Hom.of Gamma) ▷
      (sourceForwardTriangulator D.datum).triangle ≫
        D.forwardInterchanger.hom) = _
  rw [← KUOS.DependentOriginationCoherentBiadjunctionSwallowtailModificationExchangeV5_112.Generic.forwardInterchanger_exchange D Gamma]
  simp

/-- Counit-centered transport uses the reverse swallowtail, retaining
its original opposite whiskering orientation and all structural cells. -/
theorem reverseWitnessTransport_counit_modification
    (Gamma : Pseudofunctor.StrongTrans.Modification
      D.datum.base.counit D.datum.base.counit) :
    reverseWitnessTransport D
        ((targetForwardTriangulator D.datum).triangle ◁
          (Pseudofunctor.StrongTrans.Hom.of Gamma)) =
      (targetReverseTriangulator D.datum).triangle ◁
        (Pseudofunctor.StrongTrans.Hom.of Gamma) := by
  change D.reverseInterchanger.inv ≫
    ((targetForwardTriangulator D.datum).triangle ◁
      (Pseudofunctor.StrongTrans.Hom.of Gamma) ≫
        D.reverseInterchanger.hom) = _
  rw [KUOS.DependentOriginationCoherentBiadjunctionSwallowtailModificationExchangeV5_112.Generic.reverseInterchanger_exchange D Gamma]
  simp

/-- Exact LEC-11 gluing comparison on the ACTUAL old forward
modification boundary, not a newly invented Bool proxy. -/
theorem forwardWitnessTransport_hasGlobal_iff
    {X : Type uBase} {I : Type uIndex} (U : I → Set X)
    (s : LocalSections U
      (forwardSwallowtailLeft D.datum ⟶ forwardSwallowtailLeft D.datum)) :
    HasGlobal U (shadowSections U (forwardWitnessTransport D) s) ↔
      HasGlobal U s :=
  witnessConjugation_hasGlobal_iff D.forwardInterchanger U s

theorem reverseWitnessTransport_hasGlobal_iff
    {X : Type uBase} {I : Type uIndex} (U : I → Set X)
    (s : LocalSections U
      (reverseSwallowtailLeft D.datum ⟶ reverseSwallowtailLeft D.datum)) :
    HasGlobal U (shadowSections U (reverseWitnessTransport D) s) ↔
      HasGlobal U s :=
  witnessConjugation_hasGlobal_iff D.reverseInterchanger U s

end SwallowtailBoundaries

section ActualLift
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationCoherentBiadjunctionActualLiftV5_101

universe u v uH vH uW uP
variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

/-- Concrete instance: use the existing proved actual-lift forward
swallowtail, preserving its chosen F/G/eta/epsilon, not new adjoints. -/
def actualLiftForwardWitnessTransport :=
  forwardWitnessTransport
    (actualLiftCoherentBiadjunctionDatum (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))

/-- The same unmodified actual-lift datum supplies the reverse transport. -/
def actualLiftReverseWitnessTransport :=
  reverseWitnessTransport
    (actualLiftCoherentBiadjunctionDatum (W := W) A
      (WorldLabel := WorldLabel) (PresentationLabel := PresentationLabel))

end ActualLift

section OriginalF55Boundary
open KUOS.LivingEngiHistoricalBridge
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {n₁ n₂ n₃ n₄ m₁ m₂ m₃ m₄ : Nat}
variable {p₀ p₁ p₂ p₃ p₄ : Blocks a b}
variable {q₀ q₁ q₂ q₃ q₄ : Blocks x y}
variable
  (t₁ : OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁)
  (t₂ : OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂)
  (t₃ : OriginalF45BracketTree n₃ m₃ p₂ q₂ p₃ q₃)
  (t₄ : OriginalF45BracketTree n₄ m₄ p₃ q₃ p₄ q₄)

/-- Real historical F55 limitation. Any separately supplied shadow-only
receiver followed by reversible boundary transport still cannot recover
ALL original raw witnesses. This includes swallowtail transport when
instantiated on its genuine modification category. No such receiver is
silently asserted to be a faithful old-to-native source functor. -/
theorem historicalF55_no_raw_reconstruction_after_transport
    {C : Type uCat} [Category.{vCat} C] {A B : C}
    (e : A ≅ B) (read : HistoricalNativeF55CommonShadow → (A ⟶ A)) :
    ¬ Factors
      (fun raw : HistoricalPentagonF55Raw t₁ t₂ t₃ t₄ =>
        witnessConjugation e (read (historicalF55CommonReadout raw)))
      (fun raw : HistoricalPentagonF55Raw t₁ t₂ t₃ t₄ => raw) := by
  apply no_factor_of_collision _ _
    (historicalPentagonF55Cell t₁ t₂ t₃ t₄)
    (historicalPentagonF55WithUnit t₁ t₂ t₃ t₄)
  · exact congrArg (fun z => witnessConjugation e (read z))
      (historicalPentagonF55_unit_shadow_equal t₁ t₂ t₃ t₄)
  · exact historicalPentagonF55_raw_distinct t₁ t₂ t₃ t₄

end OriginalF55Boundary

#print axioms witnessConjugation
#print axioms witnessConjugation_eq_iff
#print axioms witnessConjugation_comp
#print axioms witnessConjugation_id
#print axioms witnessConjugation_trans
#print axioms witnessHistory_roundtrip
#print axioms witnessHistory_eq_iff
#print axioms witnessConjugation_compatible_iff
#print axioms witnessConjugation_hasGlobal_iff
#print axioms witnessConjugation_factors_iff
#print axioms comparison_defect_eq_id_iff
#print axioms forward_swallowtail_defect_identity
#print axioms reverse_swallowtail_defect_identity
#print axioms forwardWitnessTransport_unit_modification
#print axioms reverseWitnessTransport_counit_modification
#print axioms forwardWitnessTransport_hasGlobal_iff
#print axioms reverseWitnessTransport_hasGlobal_iff
#print axioms actualLiftForwardWitnessTransport
#print axioms actualLiftReverseWitnessTransport
#print axioms historicalF55_no_raw_reconstruction_after_transport

end
end KUOS.LivingEngiSwallowtail
