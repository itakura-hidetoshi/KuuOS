import Mathlib
import KUOS.DependentOriginationFunctorialTransportV0_1

namespace KUOS.DependentOriginationPresentationUniversalityV2_0

open CategoryTheory
open KUOS.DependentOriginationFunctorialTransportV0_1

universe u v uD vD uE vE w uD₁ vD₁ uD₂ vD₂

/-!
# Dependent-origination presentation universality v2.0

This file begins the universal-property program at the weakest layer where a
complete theorem is already available from Mathlib: presentation invariance.

Let `Context` be a category of contexts and let `W` be the class of context
changes that are declared to preserve intrinsic semantics.  Mathlib constructs
the localization `W.Localization` and its canonical functor

```text
W.Q : Context ⥤ W.Localization.
```

The universal property says that, for every target category `Target`,
precomposition with `W.Q` induces an equivalence

```text
(W.Localization ⥤ Target) ≌ W.FunctorsInverting Target.
```

Thus a contextual system descends to the presentation-independent completion
exactly when it sends every morphism in `W` to an isomorphism.  The factor is
canonical up to unique coherent equivalence.  Any two categories carrying the
same localization universal property are equivalent, compatibly with their
canonical maps from `Context`.

This is a genuine universal theorem, but only for the presentation-invariance
axis `W`.  It does not yet include descent data `J`, higher coherence `H`, or a
proof that the final `DO(Context, W, J, H)` completion has been constructed.
-/

section CanonicalCompletion

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- The canonical presentation-independent context supplied by Mathlib's
localization construction. -/
abbrev PresentationCompletion := W.Localization

/-- The canonical map from contexts to the presentation-independent
completion. -/
abbrev presentationUnit : Context ⥤ PresentationCompletion W := W.Q

/--
The exact universal mapping property of the presentation completion.

A functor out of the completion is equivalently a contextual functor that
inverts every declared presentation equivalence in `W`.
-/
noncomputable def presentationFunctorEquivalence
    (Target : Type uE) [Category.{vE} Target] :
    (PresentationCompletion W ⥤ Target) ≌ W.FunctorsInverting Target :=
  Localization.functorEquivalence W.Q W Target

/--
A contextual dependent-origination transport system that inverts all maps in
`W` factors through the canonical presentation completion.
-/
noncomputable def factorTransportSystem
    (D : FunctorialTransportSystem Context)
    (hD : W.IsInvertedBy D.state) :
    FunctorialTransportSystem (PresentationCompletion W) where
  state := Localization.lift D.state hD W.Q

/--
The canonical factor really recovers the original contextual state functor
after precomposition with the localization map.
-/
noncomputable def factorTransportSystemIso
    (D : FunctorialTransportSystem Context)
    (hD : W.IsInvertedBy D.state) :
    W.Q ⋙ (factorTransportSystem W D hD).state ≅ D.state :=
  Localization.fac D.state hD W.Q

/--
Essential uniqueness of the factorization: every other factor carrying the
same comparison with the original contextual system is naturally isomorphic
to the canonical factor.
-/
noncomputable def factorTransportSystemUniqueIso
    (D : FunctorialTransportSystem Context)
    (hD : W.IsInvertedBy D.state)
    (E : FunctorialTransportSystem (PresentationCompletion W))
    (hE : W.Q ⋙ E.state ≅ D.state) :
    E.state ≅ (factorTransportSystem W D hD).state := by
  letI : Localization.Lifting W.Q W D.state E.state := ⟨hE⟩
  change E.state ≅ Localization.lift D.state hD W.Q
  exact
    Localization.liftNatIso W.Q W
      D.state D.state E.state (Localization.lift D.state hD W.Q)
      (Iso.refl D.state)

end CanonicalCompletion

section ArbitraryModel

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable {Completion : Type uD} [Category.{vD} Completion]
variable (η : Context ⥤ Completion) [η.IsLocalization W]

/--
Every concrete model of the same localization universal property represents
exactly the same category of `W`-inverting semantics.
-/
noncomputable def modelFunctorEquivalence
    (Target : Type uE) [Category.{vE} Target] :
    (Completion ⥤ Target) ≌ W.FunctorsInverting Target :=
  Localization.functorEquivalence η W Target

/--
Factor a `W`-invariant contextual transport system through any chosen model of
the presentation completion.
-/
noncomputable def factorTransportSystemThrough
    (D : FunctorialTransportSystem Context)
    (hD : W.IsInvertedBy D.state) :
    FunctorialTransportSystem Completion where
  state := Localization.lift D.state hD η

/-- The chosen factor is a genuine factorization up to natural isomorphism. -/
noncomputable def factorTransportSystemThroughIso
    (D : FunctorialTransportSystem Context)
    (hD : W.IsInvertedBy D.state) :
    η ⋙ (factorTransportSystemThrough W η D hD).state ≅ D.state :=
  Localization.fac D.state hD η

/-- Essential uniqueness of factorization through an arbitrary localization
model. -/
noncomputable def factorTransportSystemThroughUniqueIso
    (D : FunctorialTransportSystem Context)
    (hD : W.IsInvertedBy D.state)
    (E : FunctorialTransportSystem Completion)
    (hE : η ⋙ E.state ≅ D.state) :
    E.state ≅ (factorTransportSystemThrough W η D hD).state := by
  letI : Localization.Lifting η W D.state E.state := ⟨hE⟩
  change E.state ≅ Localization.lift D.state hD η
  exact
    Localization.liftNatIso η W
      D.state D.state E.state (Localization.lift D.state hD η)
      (Iso.refl D.state)

end ArbitraryModel

section UniversalCarrierUniqueness

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable {Completion₁ : Type uD₁} [Category.{vD₁} Completion₁]
variable {Completion₂ : Type uD₂} [Category.{vD₂} Completion₂]
variable (η₁ : Context ⥤ Completion₁) [η₁.IsLocalization W]
variable (η₂ : Context ⥤ Completion₂) [η₂.IsLocalization W]

/--
Any two carriers satisfying the same presentation-localization universal
property are equivalent categories.
-/
noncomputable def universalCarrierEquivalence : Completion₁ ≌ Completion₂ :=
  Localization.uniq η₁ η₂ W

/--
The carrier equivalence is compatible with the two canonical maps out of the
original context category.
-/
noncomputable def universalCarrierTriangleIso :
    η₁ ⋙ (universalCarrierEquivalence W η₁ η₂).functor ≅ η₂ :=
  Localization.compUniqFunctor η₁ η₂ W

/-- The inverse equivalence is likewise compatible with the localization
maps. -/
noncomputable def universalCarrierInverseTriangleIso :
    η₂ ⋙ (universalCarrierEquivalence W η₁ η₂).inverse ≅ η₁ :=
  Localization.compUniqInverse η₁ η₂ W

end UniversalCarrierUniqueness

/-!
The theorem proved here is the `W`-axis of the intended KuuOS universality
program:

```text
presentation changes W
        ↓
localization W.Localization
        ↓
(Target-valued systems on the completion)
    ≌
(contextual systems that invert W)
```

The next universal layer must add descent/gluing and higher coherence without
silently identifying those extra conditions with ordinary localization.
-/

end KUOS.DependentOriginationPresentationUniversalityV2_0
