import Mathlib
import KUOS.DependentOriginationHigherLocalizationInterfaceV2_10

namespace KUOS.DependentOriginationStrictHigherLocalizationV2_11

open CategoryTheory
open Opposite
open KUOS.DependentOriginationPresentationUniversalityV2_0
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherStackDescentV2_8
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10

universe u v uH vH

/-!
# Strict Cat-valued presentation localization sector v2.11

The v2.10 interface isolates the genuinely missing higher theorem:
weak `W`-admissible pseudofunctors `LocallyDiscrete C ⥤ᵖ Cat` should factor,
up to coherent equivalence, through `C[W⁻¹]`.  Ordinary Mathlib localization
does not prove that full bicategorical statement.

There is, however, a rigorous sector where existence is already available.
Suppose the raw higher system comes from an ordinary functor

```text
G : C ⥤ Cat
```

and every arrow in `W` is sent to an *isomorphism in the category `Cat`*.
This is stronger than merely being an equivalence of categories.  Then the
ordinary localization universal property applies directly, producing

```text
Localization.lift G hG W.Q : C[W⁻¹] ⥤ Cat.
```

Since `Cat` is a strict bicategory, both `G` and its localized lift can be
promoted to pseudofunctors from locally discrete bicategories.  This file
records that strict sector exactly.  It is a genuine existence theorem for a
subclass of raw higher systems, not a proof of the still-missing weak
bicategorical localization theorem.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- An ordinary Cat-valued contextual functor, promoted to a pseudofunctor. -/
abbrev strictRawHigherSystem
    (G : Context ⥤ Cat.{vH, uH}) :
    RawHigherContextualSystem (Context := Context) :=
  G.toPseudofunctor'

/-- The ordinary localized Cat-valued functor supplied by Mathlib when `G`
strictly inverts `W` in the category `Cat`. -/
noncomputable def strictLocalizedFunctor
    (G : Context ⥤ Cat.{vH, uH})
    (hG : W.IsInvertedBy G) :
    LocalizedContext W ⥤ Cat.{vH, uH} :=
  Localization.lift G hG W.Q

/-- Re-express the ordinary localized functor in the exact double-opposite
variance expected by the Cat-valued stack layer, then promote it to a
pseudofunctor. -/
noncomputable def strictLocalizedHigherSystem
    (G : Context ⥤ Cat.{vH, uH})
    (hG : W.IsInvertedBy G) :
    HigherLocalizedDescentSystem (W := W) :=
  (unopUnop (LocalizedContext W) ⋙ strictLocalizedFunctor W G hG).toPseudofunctor'

/-- Ordinary localization recovers the original Cat-valued contextual functor
after precomposition with the presentation unit. -/
noncomputable def strictLocalizationFactorizationIso
    (G : Context ⥤ Cat.{vH, uH})
    (hG : W.IsInvertedBy G) :
    W.Q ⋙ strictLocalizedFunctor W G hG ≅ G :=
  Localization.fac G hG W.Q

/-- Strict inversion in `Cat` is sufficient for the promoted raw pseudofunctor
to satisfy the weaker v2.10 higher `W`-admissibility condition. -/
theorem strictRawHigherSystem_isHigherWAdmissible
    (G : Context ⥤ Cat.{vH, uH})
    (hG : W.IsInvertedBy G) :
    IsHigherWAdmissible W (strictRawHigherSystem G) := by
  intro X Y f hf
  haveI : IsIso (G.map f) := hG f hf
  let eCat := asIso (G.map f)
  let e : (G.obj X) ≌ (G.obj Y) :=
    { functor := eCat.hom.toFunctor
      inverse := eCat.inv.toFunctor
      unitIso := eqToIso (congrArg Cat.Hom.toFunctor eCat.hom_inv_id).symm
      counitIso := eqToIso (congrArg Cat.Hom.toFunctor eCat.inv_hom_id) }
  change (G.map f).toFunctor.IsEquivalence
  simpa [e, eCat] using e.isEquivalence_functor

/-- Therefore every strictly `W`-inverting ordinary Cat-valued contextual
functor has a canonical localized Cat-valued higher lift. -/
theorem strictSector_hasLocalizedHigherLift
    (G : Context ⥤ Cat.{vH, uH})
    (hG : W.IsInvertedBy G) :
    Nonempty (HigherLocalizedDescentSystem (W := W)) :=
  ⟨strictLocalizedHigherSystem W G hG⟩

/-!
The proven implication is thus

```text
ordinary G : C ⥤ Cat
+ W.IsInvertedBy G
        ↓
raw pseudofunctor G.toPseudofunctor'
+ weak higher W-admissibility
        ↓
Localization.lift G hG W.Q
        ↓
localized Cat-valued pseudofunctor.
```

The gap to the full v2.10 objective is now exact.  The hypothesis
`W.IsInvertedBy G` asks for isomorphisms in `Cat`, whereas the desired raw
higher condition only asks for equivalences of categories.  Bridging precisely
that gap requires bicategorical localization / strictification coherence; it
cannot be obtained merely by reusing the ordinary localization theorem.
-/

end KUOS.DependentOriginationStrictHigherLocalizationV2_11
