import KUOS.DependentOriginationQuotientRelationIsoExistenceV2_58

namespace KUOS.DependentOriginationCoherentQuotientTransportV2_59

open CategoryTheory
open CategoryTheory.Bicategory
open Opposite
open KUOS.DependentOriginationPresentationUniversalityV2_0
open KUOS.DependentOriginationHigherStackDescentV2_8
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationFreePathEvaluatorV2_57
open KUOS.DependentOriginationQuotientRelationIsoExistenceV2_58

universe u v uH vH

/-!
# Coherent quotient transport v2.59

The v2.58 layer proves that whenever two free localization paths represent the
same morphism in `W.Localization`, their evaluations under the v2.57 free-path
evaluator are naturally isomorphic.  That theorem deliberately returns
`Nonempty (F.map p ≅ F.map q)`: it proves existence without choosing a
proof-dependent transport.

This file isolates the exact additional coherence needed to pass from that
existence statement to an actual pseudofunctor on the quotient category.

For every morphism of `W.Localization` we use `Quot.out` to choose one concrete
free-path representative and evaluate that representative.  Thus the object and
1-morphism assignments are fixed; they are not extra assumptions.  What remains
to be supplied is precisely:

* an invertible identity comparison `mapId`;
* an invertible composition comparison `mapComp`;
* the associativity coherence equation;
* the left-unit coherence equation;
* the right-unit coherence equation.

These are exactly the inputs required by Mathlib's
`LocallyDiscrete.mkPseudofunctor`.  Consequently this file proves that such
coherent quotient-transport data constructs a genuine pseudofunctor

```text
LocallyDiscrete (W.Localization) ⥤ᵖ Cat
```

and then transports it through the standard double-opposite variance correction
to the exact KuuOS localized higher-system carrier.

No existence of the coherence data is asserted here.  In particular v2.58 gives
pointwise isomorphism existence, but does not by itself prove that a simultaneous
choice satisfies the three equations below.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- Evaluate a morphism of the quotient localization by choosing its concrete
free-path representative with `Quot.out` and applying the v2.57 evaluator.

The choice of representative is computational scaffolding only: v2.58 proves
that changing to any quotient-equal representative changes the result only up
to natural isomorphism. -/
noncomputable def quotientRepresentativeMap
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y : W.Localization} (f : X ⟶ Y) :
    R.obj (.mk X.as.obj) ⟶ R.obj (.mk Y.as.obj) :=
  (freePathEvaluator W R D).map (Quot.out f)

/-- The exact coherence package still missing after v2.58.

The object assignment and morphism assignment are fixed by `R`, `D`, and
`Quot.out`; only the pseudofunctorial comparison 2-isomorphisms and their three
coherence equations are fields.

This is intentionally weaker than storing a localized pseudofunctor as a field:
the latter would merely restate the desired construction. -/
structure CoherentQuotientTransportData
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R) where
  /-- Chosen coherent comparison for the identity morphism of the quotient. -/
  mapId :
    ∀ X : W.Localization,
      quotientRepresentativeMap W R D (𝟙 X) ≅
        𝟙 (R.obj (.mk X.as.obj))
  /-- Chosen coherent comparison for composition in the quotient. -/
  mapComp :
    ∀ {X Y Z : W.Localization} (f : X ⟶ Y) (g : Y ⟶ Z),
      quotientRepresentativeMap W R D (f ≫ g) ≅
        quotientRepresentativeMap W R D f ≫
          quotientRepresentativeMap W R D g
  /-- Pentagon/associativity coherence for the chosen composition transports. -/
  map₂_associator :
    ∀ {X Y Z T : W.Localization}
      (f : X ⟶ Y) (g : Y ⟶ Z) (h : Z ⟶ T),
      (mapComp (f ≫ g) h).hom ≫
          (mapComp f g).hom ▷ quotientRepresentativeMap W R D h ≫
          (α_
            (quotientRepresentativeMap W R D f)
            (quotientRepresentativeMap W R D g)
            (quotientRepresentativeMap W R D h)).hom ≫
          quotientRepresentativeMap W R D f ◁ (mapComp g h).inv ≫
          (mapComp f (g ≫ h)).inv =
        eqToHom (by simp)
  /-- Left-unit coherence for the chosen identity/composition transports. -/
  map₂_left_unitor :
    ∀ {X Y : W.Localization} (f : X ⟶ Y),
      (mapComp (𝟙 X) f).hom ≫
          (mapId X).hom ▷ quotientRepresentativeMap W R D f ≫
          (λ_ (quotientRepresentativeMap W R D f)).hom =
        eqToHom (by simp)
  /-- Right-unit coherence for the chosen identity/composition transports. -/
  map₂_right_unitor :
    ∀ {X Y : W.Localization} (f : X ⟶ Y),
      (mapComp f (𝟙 Y)).hom ≫
          quotientRepresentativeMap W R D f ◁ (mapId Y).hom ≫
          (ρ_ (quotientRepresentativeMap W R D f)).hom =
        eqToHom (by simp)

/-- Existence of coherent quotient transport is kept as an explicit proposition.
It is the sharpened general-`W` obstruction after v2.58. -/
def HasCoherentQuotientTransportData
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R) : Prop :=
  Nonempty (CoherentQuotientTransportData (W := W) R D)

/-- Coherent quotient transport constructs an actual pseudofunctor on the
canonical localization category.

Mathlib's locally-discrete constructor shows that the three equations packaged
above are exactly sufficient: no extra hidden coherence field is introduced. -/
noncomputable def quotientLocalizationPseudofunctor
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (T : CoherentQuotientTransportData (W := W) R D) :
    Pseudofunctor (LocallyDiscrete W.Localization) Cat.{vH, uH} :=
  LocallyDiscrete.mkPseudofunctor
    (fun X : W.Localization => R.obj (.mk X.as.obj))
    (fun f => quotientRepresentativeMap W R D f)
    T.mapId T.mapComp T.map₂_associator
    T.map₂_left_unitor T.map₂_right_unitor

/-- The quotient pseudofunctor has exactly the original raw fiber category on
each localized object representative. -/
@[simp] theorem quotientLocalizationPseudofunctor_obj
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (T : CoherentQuotientTransportData (W := W) R D)
    (X : W.Localization) :
    (quotientLocalizationPseudofunctor W R D T).obj (.mk X) =
      R.obj (.mk X.as.obj) := by
  rfl

/-- Its map on a localized 1-morphism is exactly evaluation of the chosen
`Quot.out` free-path representative. -/
@[simp] theorem quotientLocalizationPseudofunctor_map
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (T : CoherentQuotientTransportData (W := W) R D)
    {X Y : W.Localization} (f : X ⟶ Y) :
    (quotientLocalizationPseudofunctor W R D T).map f.toLoc =
      quotientRepresentativeMap W R D f := by
  rfl

/-- Apply the standard double-opposite variance correction to obtain precisely
the localized higher-system type used by the v2.10 KuuOS factorization
interface. -/
noncomputable def coherentQuotientLocalizedHigherSystem
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (T : CoherentQuotientTransportData (W := W) R D) :
    HigherLocalizedDescentSystem (W := W) (uH := uH) (vH := vH) :=
  Pseudofunctor.comp
    (unopUnop (LocalizedContext W)).toPseudofunctor
    (quotientLocalizationPseudofunctor W R D T)

/-- Coherent quotient transport therefore suffices for existence of an actual
localized pseudofunctor candidate in the exact KuuOS carrier. -/
theorem hasLocalizedHigherSystem_of_coherentQuotientTransport
    (R : RawHigherContextualSystem
      (Context := Context) (uH := uH) (vH := vH))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (hT : HasCoherentQuotientTransportData W R D) :
    Nonempty (HigherLocalizedDescentSystem (W := W) (uH := uH) (vH := vH)) := by
  rcases hT with ⟨T⟩
  exact ⟨coherentQuotientLocalizedHigherSystem W R D T⟩

/-!
## Boundary fixed by v2.59

The general-`W` route is now factored as

```text
IsHigherWAdmissible W R
  → pointwise adjoint equivalences                         [v2.56]
  → free-path evaluator                                  [v2.57]
  → quotient-equal paths have Nonempty evaluation Iso    [v2.58]
  → CoherentQuotientTransportData
  → LocallyDiscrete (W.Localization) ⥤ᵖ Cat              [v2.59]
  → exact KuuOS double-op localized higher-system.
```

Thus the remaining obstruction is no longer construction of the localized
pseudofunctor *from* coherent quotient transport; that implication is proved
here.  What remains for the v2.10 factorization is a coherent strong comparison
between restriction of this localized system and the original `R`, and then the
existence problem for the coherent transport/comparison data themselves.

This file does not claim that v2.58's pointwise `Nonempty Iso` witnesses admit a
simultaneously coherent choice, and it does not yet prove

```text
IsHigherWAdmissible W R
  ⇒ HasHigherLocalizationFactorization W R.
```
-/

end KUOS.DependentOriginationCoherentQuotientTransportV2_59
