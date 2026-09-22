import KUOS.DependentOriginationQuotientDirectionalPropertyTransportV3_31
import Mathlib.CategoryTheory.MorphismProperty.Composition

namespace KUOS.DependentOriginationCertifiedQuotientSectorClosureV3_32

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationAssociatorUnitorTriangleResidualV3_26
open KUOS.DependentOriginationQuotientRepresentativeDirectionalClosureV3_30
open KUOS.DependentOriginationQuotientDirectionalPropertyTransportV3_31

universe u v uH vH uQ vQ

set_option autoImplicit false

/-!
# Certified quotient sector closure v3.32

v3.31 replaces a certificate on the particular `Quot.out` word by existence of
one certified representative. This layer proves the algebra of that existence
condition: it contains identities, is closed under composition, and is the
least multiplicative morphism property containing the certified generator
images.

The generic construction uses an arbitrary relation on a path category. It
needs no invariance of the letterwise predicate under that relation. Witness
paths concatenate, and the quotient functor preserves their composition.

Specialization gives multiplicative sectors for the two v3.31 existence
conditions. These sectors remain sufficient for semantic EssSurj/Faithful;
minimality among multiplicative properties containing the specified generators
is not a necessary-and-sufficient characterization of those semantic properties.
-/

section PathCertificates

variable {V : Type uQ} [Q : Quiver.{vQ} V]
variable {P : ∀ {X Y : V}, (X ⟶ Y) → Prop}

/-- Concatenating two certified paths preserves their letterwise certificate.
Induction is on the right-hand evidence, with the same uniform predicate. -/
theorem pathEdgesSatisfy_comp
    {X Y Z : V} {p : Quiver.Path X Y} {q : Quiver.Path Y Z}
    (hp : PathEdgesSatisfy (@P) p)
    (hq : PathEdgesSatisfy (@P) q) :
    PathEdgesSatisfy (@P) (p.comp q) := by
  induction hq with
  | nil => exact hp
  | @cons Y Z q e _hq he ih =>
      exact PathEdgesSatisfy.cons ih he

end PathCertificates

section QuotientSectors

variable {V : Type uQ} [Q : Quiver.{vQ} V]
variable (r : HomRel (Paths V))
variable (P : ∀ {X Y : V}, (X ⟶ Y) → Prop)

/-- Quotient morphisms admitting at least one path all of whose edges satisfy
`P`. The quotient relation is arbitrary; `P` itself need not descend. -/
def certifiedQuotientSector : MorphismProperty (Quotient r) :=
  fun X Y f =>
    ∃ p : X.as ⟶ Y.as,
      (Quotient.functor r).map p = f ∧ PathEdgesSatisfy (@P) p

/-- Existence of certified representatives contains identities and is stable
under composition, even when individual representative certificates differ. -/
instance certifiedQuotientSector_isMultiplicative :
    (certifiedQuotientSector r (@P)).IsMultiplicative where
  id_mem X := by
    refine ⟨(𝟙 X.as : X.as ⟶ X.as), ?_, ?_⟩
    · rfl
    · -- X.as is a Paths V object: keep the original edge quiver Q explicit.
      exact @PathEdgesSatisfy.nil V Q (@P) X.as
  comp_mem f g hf hg := by
    rcases hf with ⟨p, hp, hEdgesP⟩
    rcases hg with ⟨q, hq, hEdgesQ⟩
    refine ⟨p ≫ q, ?_, ?_⟩
    · exact ((Quotient.functor r).map_comp p q).trans
        (congrArg₂ (fun a b => a ≫ b) hp hq)
    · exact pathEdgesSatisfy_comp hEdgesP hEdgesQ

/-- Every certified generator image belongs to the quotient sector. -/
theorem certifiedQuotientSector_generator
    {X Y : V} (e : X ⟶ Y) (he : P e) :
    certifiedQuotientSector r (@P)
      ((Quotient.functor r).map e.toPath) := by
  refine ⟨e.toPath, rfl, ?_⟩
  exact PathEdgesSatisfy.cons (PathEdgesSatisfy.nil X) he

/-- Any multiplicative property containing the certified generator images
contains the image of every certified path. -/
theorem certifiedPath_map_mem
    (S : MorphismProperty (Quotient r)) [S.IsMultiplicative]
    (hS : ∀ {X Y : V} (e : X ⟶ Y),
      P e → S ((Quotient.functor r).map e.toPath))
    {X Y : V} (p : Quiver.Path X Y)
    (hp : PathEdgesSatisfy (@P) p) :
    S ((Quotient.functor r).map p) := by
  induction hp with
  | nil =>
      exact S.id_mem _
  | @cons Y Z p e _hp he ih =>
      -- Quotient composition and right singleton concatenation reduce
      -- definitionally; no relation-level certificate invariance is used.
      change S ((Quotient.functor r).map p ≫
        (Quotient.functor r).map e.toPath)
      exact S.comp_mem _ _ ih (hS e he)

/-- The certified quotient sector is the least multiplicative property
containing the certified generator images. -/
theorem certifiedQuotientSector_le
    (S : MorphismProperty (Quotient r)) [S.IsMultiplicative]
    (hS : ∀ {X Y : V} (e : X ⟶ Y),
      P e → S ((Quotient.functor r).map e.toPath)) :
    certifiedQuotientSector r (@P) ≤ S := by
  intro X Y f hf
  rcases hf with ⟨p, hp, hEdges⟩
  have hMem := certifiedPath_map_mem r (@P) S hS p hEdges
  exact hp ▸ hMem

/-- A generator test characterizes containment in any multiplicative property.
This is a minimality statement for the certificate sector, not for arbitrary
semantic evaluation properties. -/
theorem certifiedQuotientSector_le_iff
    (S : MorphismProperty (Quotient r)) [S.IsMultiplicative] :
    certifiedQuotientSector r (@P) ≤ S ↔
      ∀ {X Y : V} (e : X ⟶ Y),
        P e → S ((Quotient.functor r).map e.toPath) := by
  constructor
  · intro h X Y e he
    exact h _ (certifiedQuotientSector_generator r (@P) e he)
  · exact certifiedQuotientSector_le r (@P) S

end QuotientSectors

section DirectionalSectors

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (R : RawHigherContextualSystem.{u, v, uH, vH}
  (Context := Context))

/-!
The v3.31 predicates use ordinary implicit endpoints `{X Y}`. A bare partial
application to `W R` inserts endpoint metavariables, producing a predicate on
one hom-set. `MorphismProperty` instead retains strict implicit endpoints
`⦃X Y⦄`. Neither a postfix type ascription nor a fully qualified API name
prevents the earlier insertion. At each higher-order boundary, explicitly
bind both endpoints and the arrow; only then apply the v3.31 predicate fully.
This preserves the original definitions and all mathematical hypotheses.
-/

/-- The v3.31 EssSurj existence certificate is a multiplicative property on
the actual localization. No pointwise equivalence choice is needed here. -/
instance hasOrdinaryEssSurjRepresentative_isMultiplicative :
    MorphismProperty.IsMultiplicative
      ((fun ⦃X Y : W.Localization⦄ (f : X ⟶ Y) =>
        HasOrdinaryEssSurjRepresentative W R f) : MorphismProperty W.Localization) :=
  certifiedQuotientSector_isMultiplicative
    (Localization.Construction.relations W)
    (OrdinaryLocalizationGeneratorEssSurj W R)

/-- The v3.31 Faithful existence certificate is also multiplicative. -/
instance hasOrdinaryFaithfulRepresentative_isMultiplicative :
    MorphismProperty.IsMultiplicative
      ((fun ⦃X Y : W.Localization⦄ (f : X ⟶ Y) =>
        HasOrdinaryFaithfulRepresentative W R f) : MorphismProperty W.Localization) :=
  certifiedQuotientSector_isMultiplicative
    (Localization.Construction.relations W)
    (OrdinaryLocalizationGeneratorFaithful W R)

/-- Identity arrows have an EssSurj certificate, witnessed by the empty path. -/
theorem hasOrdinaryEssSurjRepresentative_id (X : W.Localization) :
    HasOrdinaryEssSurjRepresentative W R (𝟙 X) :=
  MorphismProperty.id_mem
    ((fun ⦃X Y : W.Localization⦄ (f : X ⟶ Y) =>
      HasOrdinaryEssSurjRepresentative W R f) : MorphismProperty W.Localization) X

/-- Identity arrows have a Faithful certificate, witnessed by the empty path. -/
theorem hasOrdinaryFaithfulRepresentative_id (X : W.Localization) :
    HasOrdinaryFaithfulRepresentative W R (𝟙 X) :=
  MorphismProperty.id_mem
    ((fun ⦃X Y : W.Localization⦄ (f : X ⟶ Y) =>
      HasOrdinaryFaithfulRepresentative W R f) : MorphismProperty W.Localization) X

/-- Concatenate witnesses to compose EssSurj-certified quotient morphisms. -/
theorem hasOrdinaryEssSurjRepresentative_comp
    {X Y Z : W.Localization} (f : X ⟶ Y) (g : Y ⟶ Z)
    (hf : HasOrdinaryEssSurjRepresentative W R f)
    (hg : HasOrdinaryEssSurjRepresentative W R g) :
    HasOrdinaryEssSurjRepresentative W R (f ≫ g) :=
  MorphismProperty.comp_mem
    ((fun ⦃X Y : W.Localization⦄ (f : X ⟶ Y) =>
      HasOrdinaryEssSurjRepresentative W R f) : MorphismProperty W.Localization) f g hf hg

/-- Concatenate witnesses to compose Faithful-certified quotient morphisms. -/
theorem hasOrdinaryFaithfulRepresentative_comp
    {X Y Z : W.Localization} (f : X ⟶ Y) (g : Y ⟶ Z)
    (hf : HasOrdinaryFaithfulRepresentative W R f)
    (hg : HasOrdinaryFaithfulRepresentative W R g) :
    HasOrdinaryFaithfulRepresentative W R (f ≫ g) :=
  MorphismProperty.comp_mem
    ((fun ⦃X Y : W.Localization⦄ (f : X ⟶ Y) =>
      HasOrdinaryFaithfulRepresentative W R f) : MorphismProperty W.Localization) f g hf hg

/-- Generator-level characterization of containment for the EssSurj sector.
Formal W-inverse letters are included without an extra hypothesis because the
ordinary-letter condition on them is `True`. -/
theorem hasOrdinaryEssSurjRepresentative_le_iff
    (S : MorphismProperty W.Localization) [S.IsMultiplicative] :
    ((fun ⦃X Y : W.Localization⦄ (f : X ⟶ Y) =>
      HasOrdinaryEssSurjRepresentative W R f) : MorphismProperty W.Localization) ≤ S ↔
      ∀ {X Y : Localization.Construction.LocQuiver W} (e : X ⟶ Y),
        OrdinaryLocalizationGeneratorEssSurj W R e →
          S ((Quotient.functor
            (Localization.Construction.relations W)).map e.toPath) :=
  certifiedQuotientSector_le_iff
    (Localization.Construction.relations W)
    (OrdinaryLocalizationGeneratorEssSurj W R) S

/-- The corresponding generator characterization for the Faithful sector. -/
theorem hasOrdinaryFaithfulRepresentative_le_iff
    (S : MorphismProperty W.Localization) [S.IsMultiplicative] :
    ((fun ⦃X Y : W.Localization⦄ (f : X ⟶ Y) =>
      HasOrdinaryFaithfulRepresentative W R f) : MorphismProperty W.Localization) ≤ S ↔
      ∀ {X Y : Localization.Construction.LocQuiver W} (e : X ⟶ Y),
        OrdinaryLocalizationGeneratorFaithful W R e →
          S ((Quotient.functor
            (Localization.Construction.relations W)).map e.toPath) :=
  certifiedQuotientSector_le_iff
    (Localization.Construction.relations W)
    (OrdinaryLocalizationGeneratorFaithful W R) S

/-- Composable certified pieces give separation for the composed outer arrows.
The v3.31 mixed-triangle theorem can therefore be applied to these composites
with its unchanged corrected-route and anchor-agreement hypotheses. -/
theorem middleIdentityWhiskerSeparating_of_composite_certificates
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X A Y B Z : W.Localization}
    (f₁ : X ⟶ A) (f₂ : A ⟶ Y) (g₁ : Y ⟶ B) (g₂ : B ⟶ Z)
    (hf₁ : HasOrdinaryEssSurjRepresentative W R f₁)
    (hf₂ : HasOrdinaryEssSurjRepresentative W R f₂)
    (hg₁ : HasOrdinaryFaithfulRepresentative W R g₁)
    (hg₂ : HasOrdinaryFaithfulRepresentative W R g₂) :
    MiddleIdentityWhiskerSeparating W R D (f₁ ≫ f₂) (g₁ ≫ g₂) := by
  exact middleIdentityWhiskerSeparating_of_exists_representatives
    W R D (f₁ ≫ f₂) (g₁ ≫ g₂)
    (hasOrdinaryEssSurjRepresentative_comp W R f₁ f₂ hf₁ hf₂)
    (hasOrdinaryFaithfulRepresentative_comp W R g₁ g₂ hg₁ hg₂)

end DirectionalSectors

/-!
## Boundary after v3.32

The two existence-certificate sectors now have a checked algebraic target:
identities, composition, and minimality among multiplicative properties
containing their certified generator images. Their definitions contain no
choice of `D` or `Quot.out`.

No assertion is made that every representative is certified, that every
semantically EssSurj/Faithful arrow admits such a certificate, that the sectors
are closed under taking arbitrary factors or inverses, or that arrows outside
them fail separation. No global correction family, simultaneous coherent
isomorphism choice, or general Stage-I/Stage-II conclusion is added.
-/

end KUOS.DependentOriginationCertifiedQuotientSectorClosureV3_32
