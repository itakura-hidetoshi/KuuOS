import KUOS.DependentOriginationScaledHornPresentationInvariantV1_30

namespace KUOS.DependentOriginationModelEquivalenceScaledHornPresentationV1_31

open CategoryTheory
open CategoryTheory.Category
open CategoryTheory.Bicategory
open scoped Bicategory
open KUOS.DependentOriginationGlobalDuskinScaledNerveV1_21
open KUOS.DependentOriginationGlobalDuskinScaledHornCoherenceV1_22
open KUOS.DependentOriginationStrictlyUnitaryDuskinModelTransportV1_27
open KUOS.DependentOriginationScaledDuskinHornTransportV1_29
open KUOS.DependentOriginationScaledHornPresentationInvariantV1_30

universe u₁ u₂ v₁ v₂ w₁ w₂

/-!
# Model-equivalence lift to scaled horn presentations v1.31

Version 1.30 proved that scaled fibrancy is invariant once an equivalence of
admissible horn presentations has been supplied.  This layer connects that
presentation-level theorem to bicategorical model replacement.

A general bicategorical model equivalence still does not automatically provide
all data needed for a global scaled Duskin comparison.  The present interface
therefore records exactly the missing geometric data:

* strictly-unitary model equivalences in both directions;
* full scaling preservation of the two normalized Duskin maps;
* preservation of the chosen admissible horn families;
* filler-existence equivalences for the two round trips.

From these ingredients the horn-presentation equivalence is constructed, rather
than assumed as a separate primitive.  Consequently global scaled fibrancy is
an invariant of any bicategorical model replacement carrying this explicit
scaled-Duskin equivalence structure.
-/

/--
Bidirectional bicategorical model-equivalence data sufficient to induce an
actual equivalence of chosen global Duskin scaled-horn presentations.
-/
structure BidirectionalScaledDuskinModelEquivalence
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (HB : GlobalDuskinScaledHornFamily B)
    (HC : GlobalDuskinScaledHornFamily C) where
  forwardModel : StrictlyUnitaryBicategoricalModelEquivalence B C
  backwardModel : StrictlyUnitaryBicategoricalModelEquivalence C B
  forwardScaled : FullScaledDuskinMapCertificate forwardModel
  backwardScaled : FullScaledDuskinMapCertificate backwardModel
  forwardFamily :
    ScaledHornFamilyMap forwardScaled.map_scaled HB HC
  backwardFamily :
    ScaledHornFamilyMap backwardScaled.map_scaled HC HB
  forward_backward_filler_equiv :
    ∀ {n : Nat} {i : Fin (n + 1)}
      (Q : ScaledHornExtensionProblem
        (duskinNerve C) (duskinScaling C) n i),
      Nonempty
        (ScaledHornFiller
          (transportGlobalDuskinHornProblem forwardScaled
            (transportGlobalDuskinHornProblem backwardScaled Q))) ↔
        Nonempty (ScaledHornFiller Q)
  backward_forward_filler_equiv :
    ∀ {n : Nat} {i : Fin (n + 1)}
      (P : ScaledHornExtensionProblem
        (duskinNerve B) (duskinScaling B) n i),
      Nonempty
        (ScaledHornFiller
          (transportGlobalDuskinHornProblem backwardScaled
            (transportGlobalDuskinHornProblem forwardScaled P))) ↔
        Nonempty (ScaledHornFiller P)

namespace BidirectionalScaledDuskinModelEquivalence

variable
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    {HB : GlobalDuskinScaledHornFamily B}
    {HC : GlobalDuskinScaledHornFamily C}
    (E : BidirectionalScaledDuskinModelEquivalence HB HC)

/-- The model-equivalence package canonically produces a horn-presentation equivalence. -/
def toScaledHornPresentationEquivalence :
    ScaledHornPresentationEquivalence HB HC where
  forward := fun P =>
    transportGlobalDuskinHornProblem E.forwardScaled P
  backward := fun Q =>
    transportGlobalDuskinHornProblem E.backwardScaled Q
  forward_admissible := by
    intro P hP
    exact E.forwardFamily.admissible_preserved P hP
  backward_admissible := by
    intro Q hQ
    exact E.backwardFamily.admissible_preserved Q hQ
  forward_filler := by
    intro P hP
    exact mapScaledHornFiller_nonempty E.forwardScaled.map_scaled hP
  backward_filler := by
    intro Q hQ
    exact mapScaledHornFiller_nonempty E.backwardScaled.map_scaled hQ
  forward_backward_filler_equiv := E.forward_backward_filler_equiv
  backward_forward_filler_equiv := E.backward_forward_filler_equiv

/-- Global scaled-Duskin fibrancy is invariant under the bidirectional model equivalence. -/
theorem globalDuskinScaledFibrancy_iff :
    HasScaledHornFillers (duskinNerve B) (duskinScaling B) HB ↔
      HasScaledHornFillers (duskinNerve C) (duskinScaling C) HC :=
  hasScaledHornFillers_iff E.toScaledHornPresentationEquivalence

/-- Bundled presentation-independent fibrancy follows from the model-equivalence package. -/
def presentationIndependentScaledFibrancyOfModelEquivalence :
    PresentationIndependentScaledFibrancy HB HC :=
  presentationIndependentScaledFibrancy E.toScaledHornPresentationEquivalence

end BidirectionalScaledDuskinModelEquivalence

/-!
The v1.31 implication is therefore

```text
strictly-unitary bicategorical model equivalence B -> C
+ strictly-unitary comparison C -> B
+ full scaled Duskin maps in both directions
+ admissible-family preservation
+ round-trip filler equivalence
  -> ScaledHornPresentationEquivalence
  -> global scaled fibrancy is presentation-independent.
```

Still intentionally separate is the existence theorem saying that every
Whitehead-style `BicategoricalModelEquivalence` of v1.26 admits this stronger
bidirectional scaled-Duskin structure.  That requires normalization, a coherent
quasi-inverse, and full scaled control; none is silently postulated here.
-/

end KUOS.DependentOriginationModelEquivalenceScaledHornPresentationV1_31
