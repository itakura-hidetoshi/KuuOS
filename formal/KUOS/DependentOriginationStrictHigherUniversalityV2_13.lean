import KUOS.DependentOriginationStrictHigherFactorizationV2_12

namespace KUOS.DependentOriginationStrictHigherUniversalityV2_13

open CategoryTheory
open KUOS.DependentOriginationPresentationUniversalityV2_0
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationStrictHigherLocalizationV2_11
open KUOS.DependentOriginationStrictHigherFactorizationV2_12

universe u v uH vH

/-!
# Strict Cat-valued higher presentation universality v2.13

The v2.11-v2.12 layers established existence of the exact v2.10 higher
localization factorization interface whenever the raw higher system comes from
an ordinary functor

```text
G : C ⥤ Cat
```

which sends every arrow of `W` to an isomorphism in the 1-category `Cat`.

This file records the corresponding universal classification and essential
uniqueness in that strict sector.  It is the specialization of Mathlib's genuine
localization universal property to the target category `Cat`:

```text
(C[W⁻¹] ⥤ Cat) ≌ W.FunctorsInverting Cat.
```

Thus the ordinary Cat-valued carrier underlying the strict higher construction
is not merely an ad hoc lift: it is canonical up to natural isomorphism and is
classified by the localization universal property.

The authority boundary remains important.  `W.FunctorsInverting Cat` asks for
actual isomorphisms in the 1-category `Cat`.  It is strictly stronger than the
v2.10 weak condition requiring only equivalences of categories, and therefore
this file does not assert a bicategorical localization theorem for arbitrary
Cat-valued pseudofunctors.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- Ordinary Cat-valued systems on the presentation-localized context. -/
abbrev StrictLocalizedCatSystem :=
  LocalizedContext W ⥤ Cat.{vH, uH}

/-- Ordinary Cat-valued contextual systems which strictly invert every arrow in
`W` in the 1-category `Cat`. -/
abbrev StrictRawCatWSystem :=
  W.FunctorsInverting Cat.{vH, uH}

/-- Exact universal classification of the strict Cat-valued sector.

Precomposition with the localization unit `W.Q` is an equivalence between
Cat-valued systems on the localization and raw Cat-valued systems which send
`W` to actual isomorphisms in `Cat`. -/
noncomputable def strictCatLocalizationEquivalence :
    StrictLocalizedCatSystem (W := W) ≌
      StrictRawCatWSystem (W := W) :=
  Localization.functorEquivalence W.Q W Cat.{vH, uH}

/-- Essential uniqueness of the canonical strict localized lift.

Any other ordinary Cat-valued functor on `C[W⁻¹]` equipped with a natural
isomorphism recovering `G` after precomposition with `W.Q` is naturally
isomorphic to the canonical `Localization.lift`. -/
noncomputable def strictLocalizedFunctorUniqueIso
    (G : Context ⥤ Cat.{vH, uH})
    (hG : W.IsInvertedBy G)
    (E : LocalizedContext W ⥤ Cat.{vH, uH})
    (hE : W.Q ⋙ E ≅ G) :
    E ≅ strictLocalizedFunctor W G hG := by
  letI : Localization.Lifting W.Q W G E := ⟨hE⟩
  change E ≅ Localization.lift G hG W.Q
  exact
    Localization.liftNatIso W.Q W
      G G E (Localization.lift G hG W.Q)
      (Iso.refl G)

/-- Pairwise essential uniqueness: any two strict localized factors of the same
raw Cat-valued system are naturally isomorphic. -/
noncomputable def strictLocalizedFactorsUniqueIso
    (G : Context ⥤ Cat.{vH, uH})
    (hG : W.IsInvertedBy G)
    (E₁ E₂ : LocalizedContext W ⥤ Cat.{vH, uH})
    (hE₁ : W.Q ⋙ E₁ ≅ G)
    (hE₂ : W.Q ⋙ E₂ ≅ G) :
    E₁ ≅ E₂ :=
  (strictLocalizedFunctorUniqueIso W G hG E₁ hE₁).trans
    (strictLocalizedFunctorUniqueIso W G hG E₂ hE₂).symm

/-- The higher factorization constructed in v2.12 uses exactly the canonical
localized pseudofunctor obtained by promoting the ordinary universal lift. -/
@[simp] theorem strictHigherLocalizationFactorization_lift
    (G : Context ⥤ Cat.{vH, uH})
    (hG : W.IsInvertedBy G) :
    (strictHigherLocalizationFactorization W G hG).lift =
      strictLocalizedHigherSystem W G hG := by
  rfl

/-- Consequently, strict inversion gives both existence of the higher
factorization interface and ordinary essential uniqueness of its localized
Cat-valued carrier. -/
theorem strictSector_has_factorization_and_unique_ordinary_carrier
    (G : Context ⥤ Cat.{vH, uH})
    (hG : W.IsInvertedBy G) :
    HasHigherLocalizationFactorization (W := W)
        (strictRawHigherSystem G) ∧
      ∀ (E : LocalizedContext W ⥤ Cat.{vH, uH})
        (hE : W.Q ⋙ E ≅ G),
        Nonempty (E ≅ strictLocalizedFunctor W G hG) := by
  constructor
  · exact strictSector_hasHigherLocalizationFactorization W G hG
  · intro E hE
    exact ⟨strictLocalizedFunctorUniqueIso W G hG E hE⟩

/-!
The strict higher localization picture is therefore complete at the ordinary
Cat-valued universal-property level:

```text
(C[W⁻¹] ⥤ Cat)
      ≌
{G : C ⥤ Cat | G strictly inverts W}
```

and the canonical lift used by the higher KuuOS factorization is essentially
unique in that category.

What remains is exactly the weak higher problem:

```text
G(w) is an equivalence of categories
```

rather than an isomorphism in `Cat`, together with the required pseudofunctorial
coherence.  Solving that requires a bicategorical localization or a proved
strictification/comparison theorem; it is not supplied by the ordinary
localization equivalence formalized here.
-/

end KUOS.DependentOriginationStrictHigherUniversalityV2_13
