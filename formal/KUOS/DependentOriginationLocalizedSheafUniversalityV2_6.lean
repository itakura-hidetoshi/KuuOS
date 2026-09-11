import Mathlib
import KUOS.DependentOriginationPresentationUniversalityV2_0
import KUOS.DependentOriginationSheafDescentUniversalityV2_2
import KUOS.DependentOriginationBaseChangeDescentV2_5

namespace KUOS.DependentOriginationLocalizedSheafUniversalityV2_6

open CategoryTheory
open KUOS.DependentOriginationFunctorialTransportV0_1
open KUOS.DependentOriginationContextualDescentV1_1
open KUOS.DependentOriginationEffectiveDescentComparisonV2_1
open KUOS.DependentOriginationPresentationUniversalityV2_0
open KUOS.DependentOriginationSheafDescentUniversalityV2_2
open KUOS.DependentOriginationOppositeSiteVarianceBridgeV2_3
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationBaseChangeDescentV2_5

universe u v w

/-!
# Localized sheaf universality for dependent origination v2.6

The preceding universal layers are now strong enough to combine the two
1-categorical axes without transporting a topology through localization by
fiat.

* v2.0 constructs the presentation-independent category `C[W⁻¹]` and proves its
  localization universal property;
* v2.3 identifies covariant KuuOS transport on any category with presheaves on
  its opposite refinement site;
* v2.5 identifies effective contextual descent everywhere with sheafness for a
  generated Grothendieck topology, provided the localized refinement atlas is
  stable under base change and has universal pushout overlaps.

The mathematically clean order is therefore

```text
raw contexts C
    | localize W
    v
C[W⁻¹]
    | opposite refinement site + generated topology J_A
    v
Sh_{J_A}((C[W⁻¹])ᵒᵖ, Type).
```

This file packages that composite construction and its objectwise universal
mapping property.  No assertion is made that an arbitrary topology on the raw
category descends through `W`: the atlas lives directly on the localization.
Likewise this is the `W + J` 1-categorical layer only; higher coherence `H`
remains a separate later theorem.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- The presentation-independent context category on which the descent site is
built. -/
abbrev LocalizedContext := PresentationCompletion W

/-- The 1-categorical dependent-origination carrier associated to a localized
refinement atlas.

The site is `(C[W⁻¹])ᵒᵖ`; consequently an object is a Type-valued sheaf whose
underlying presheaf has variance `((C[W⁻¹])ᵒᵖ)ᵒᵖ ⥤ Type`. -/
abbrev DependentOriginationCompletion1
    (A : RefinementAtlas (LocalizedContext W)) : Type _ :=
  Sheaf A.generatedTopology (Type w)

/-- The canonical localized contextual transport of a raw system which inverts
all declared presentation changes in `W`. -/
noncomputable abbrev localizedTransportSystem
    (D : FunctorialTransportSystem.{u, v, w} Context)
    (hD : W.IsInvertedBy D.state) :
    FunctorialTransportSystem (LocalizedContext W) :=
  factorTransportSystem W D hD

/-- The variance-correct presheaf associated to the localized contextual
transport. -/
noncomputable abbrev localizedOppositePresheaf
    (D : FunctorialTransportSystem.{u, v, w} Context)
    (hD : W.IsInvertedBy D.state) :
    ((LocalizedContext W)ᵒᵖ)ᵒᵖ ⥤ Type w :=
  asOppositeSitePresheaf (localizedTransportSystem W D hD)

/-- The composite `W + J` completion of a raw contextual system: first factor
through presentation localization, then sheafify on the localized opposite
site. -/
noncomputable def dependentOriginationCompletionObj
    (A : RefinementAtlas (LocalizedContext W))
    (D : FunctorialTransportSystem.{u, v, w} Context)
    (hD : W.IsInvertedBy D.state) :
    DependentOriginationCompletion1 (W := W) A :=
  (descentCompletionFunctor (A := Type w) A.generatedTopology).obj
    (localizedOppositePresheaf W D hD)

/-- The underlying presheaf-level unit of the `J` reflection after the `W`
localization. -/
noncomputable abbrev dependentOriginationCompletionUnit
    (A : RefinementAtlas (LocalizedContext W))
    (D : FunctorialTransportSystem.{u, v, w} Context)
    (hD : W.IsInvertedBy D.state) :
    localizedOppositePresheaf W D hD ⟶
      descentCompletionObj A.generatedTopology
        (localizedOppositePresheaf W D hD) :=
  descentUnit A.generatedTopology (localizedOppositePresheaf W D hD)

/-- Universal mapping property of the composite completion at the sheaf stage.
For every descent-complete target `Q`, maps from the completed localized system
to `Q` are equivalent to maps from the localized presheaf to the underlying
presheaf of `Q`. -/
noncomputable def dependentOriginationCompletionHomEquiv
    (A : RefinementAtlas (LocalizedContext W))
    (D : FunctorialTransportSystem.{u, v, w} Context)
    (hD : W.IsInvertedBy D.state)
    (Q : DependentOriginationCompletion1 (W := W) A) :
    (dependentOriginationCompletionObj W A D hD ⟶ Q) ≃
      (localizedOppositePresheaf W D hD ⟶
        (descentForgetFunctor (A := Type w) A.generatedTopology).obj Q) :=
  descentHomEquiv A.generatedTopology (localizedOppositePresheaf W D hD) Q

/-- Presentation localization still recovers the original raw contextual
system, up to the canonical natural isomorphism supplied by v2.0. -/
noncomputable def presentationRecoveryIso
    (D : FunctorialTransportSystem.{u, v, w} Context)
    (hD : W.IsInvertedBy D.state) :
    W.Q ⋙ (localizedTransportSystem W D hD).state ≅ D.state :=
  factorTransportSystemIso W D hD

/-- `J`-admissibility of a `W`-invariant raw system means precisely that its
canonical localization factor is already a sheaf on the localized refinement
site. -/
noncomputable def IsWJAdmissible
    (A : RefinementAtlas (LocalizedContext W))
    (D : FunctorialTransportSystem.{u, v, w} Context)
    (hD : W.IsInvertedBy D.state) : Prop :=
  IsGrothendieckDescentComplete A.generatedTopology
    (localizedTransportSystem W D hD)

/-- Under the geometric hypotheses from v2.5, `W + J` admissibility is exactly
effective contextual descent at every object of the presentation localization. -/
theorem isWJAdmissible_iff_allEffectiveStateDescent
    (A : RefinementAtlas (LocalizedContext W))
    (hbc : A.IsBaseChangeClosed)
    (O : A.PushoutOverlapAtlas)
    (D : FunctorialTransportSystem.{u, v, w} Context)
    (hD : W.IsInvertedBy D.state) :
    IsWJAdmissible W A D hD ↔
      ∀ X : LocalizedContext W,
        HasEffectiveStateDescent
          (localizedTransportSystem W D hD)
          (A.coverAt X)
          (O.overlap X) := by
  unfold IsWJAdmissible
  exact
    isGrothendieckDescentComplete_iff_allEffectiveStateDescent
      A hbc O (localizedTransportSystem W D hD)

/-- A raw system which is already `W + J` admissible is unchanged by the
sheafification stage up to the canonical v2.2 natural isomorphism.  Presentation
localization may still change the carrier category, but v2.0 records its
canonical recovery via `presentationRecoveryIso`. -/
noncomputable def alreadyWJAdmissibleIso
    (A : RefinementAtlas (LocalizedContext W))
    (D : FunctorialTransportSystem.{u, v, w} Context)
    (hD : W.IsInvertedBy D.state)
    (hJ : IsWJAdmissible W A D hD) :
    localizedOppositePresheaf W D hD ≅
      descentCompletionObj A.generatedTopology
        (localizedOppositePresheaf W D hD) := by
  apply alreadyDescentCompleteIso A.generatedTopology
  exact hJ

/-- Package the two admissibility conditions as one reusable structure.  This
is an object-level interface rather than a claim that a category of such raw
systems has already been proved equivalent to the sheaf category. -/
structure WJAdmissibleSystem
    (A : RefinementAtlas (LocalizedContext W)) where
  raw : FunctorialTransportSystem.{u, v, w} Context
  inverts : W.IsInvertedBy raw.state
  descent : IsWJAdmissible W A raw inverts

namespace WJAdmissibleSystem

variable {W}

/-- Every bundled `W + J` admissible system determines a canonical object of the
localized sheaf carrier. -/
noncomputable def toCompletion
    {A : RefinementAtlas (LocalizedContext W)}
    (S : WJAdmissibleSystem W A) :
    DependentOriginationCompletion1 (W := W) A :=
  dependentOriginationCompletionObj W A S.raw S.inverts

/-- The sheafification step for an already admissible bundled system is
canonically invisible at the presheaf level. -/
noncomputable def toCompletionAlreadyCompleteIso
    {A : RefinementAtlas (LocalizedContext W)}
    (S : WJAdmissibleSystem W A) :
    localizedOppositePresheaf W S.raw S.inverts ≅
      descentCompletionObj A.generatedTopology
        (localizedOppositePresheaf W S.raw S.inverts) :=
  alreadyWJAdmissibleIso W A S.raw S.inverts S.descent

end WJAdmissibleSystem

/-!
The 1-categorical `W + J` spine now has a canonical carrier and a canonical
objectwise completion:

```text
D : C ⥤ Type,  D(W) iso
        | localization factor
        v
D_W : C[W⁻¹] ⥤ Type
        | opposite-site reinterpretation
        v
P_W : ((C[W⁻¹])ᵒᵖ)ᵒᵖ ⥤ Type
        | sheafification for J_A
        v
DO₁(C,W,A) := Sh_{J_A}((C[W⁻¹])ᵒᵖ, Type).
```

The localization factor is canonical up to coherent natural isomorphism (v2.0),
and the sheafification factor is universal by adjunction (v2.2).  Under the v2.5
base-change and pushout-overlap hypotheses, being already in the image of the
`J` reflection is equivalent to effective KuuOS descent at every localized
context.

A later theorem may organize morphisms between admissible raw systems and prove
a category-level equivalence with an appropriate sheaf category.  That stronger
statement, and the higher-coherence axis `H`, are intentionally not claimed in
this file.
-/

end KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
