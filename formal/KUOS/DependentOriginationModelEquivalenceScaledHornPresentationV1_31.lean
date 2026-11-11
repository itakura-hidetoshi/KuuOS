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

universe u₁ u₂ v₁ v₂ w₁ w₂ u₃

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

/-!
The two bridges from original horn families to the lifted families are explicit
certificates. They may NOT be inferred from the bicategorical model maps.
The following composition lemmas preserve all filler-reflection conditions.
-/

private theorem presentationForwardFillerIff
    {X : SSet.{u₁}} {Y : SSet.{u₂}}
    {sX : ScaledSimplicialSet X} {sY : ScaledSimplicialSet Y}
    {HX : ScaledHornFamily X sX} {HY : ScaledHornFamily Y sY}
    (A : ScaledHornPresentationEquivalence HX HY)
    {n : Nat} {i : Fin (n + 1)}
    (P : ScaledHornExtensionProblem X sX n i) :
    Nonempty (ScaledHornFiller (A.forward P)) ↔
      Nonempty (ScaledHornFiller P) := by
  constructor
  · intro h
    exact (A.backward_forward_filler_equiv P).mp
      (A.backward_filler (A.forward P) h)
  · intro h
    exact A.forward_filler P h

private theorem presentationBackwardFillerIff
    {X : SSet.{u₁}} {Y : SSet.{u₂}}
    {sX : ScaledSimplicialSet X} {sY : ScaledSimplicialSet Y}
    {HX : ScaledHornFamily X sX} {HY : ScaledHornFamily Y sY}
    (A : ScaledHornPresentationEquivalence HX HY)
    {n : Nat} {i : Fin (n + 1)}
    (Q : ScaledHornExtensionProblem Y sY n i) :
    Nonempty (ScaledHornFiller (A.backward Q)) ↔
      Nonempty (ScaledHornFiller Q) := by
  constructor
  · intro h
    exact (A.forward_backward_filler_equiv Q).mp
      (A.forward_filler (A.backward Q) h)
  · intro h
    exact A.backward_filler Q h

private def presentationEquivalenceSymm
    {X : SSet.{u₁}} {Y : SSet.{u₂}}
    {sX : ScaledSimplicialSet X} {sY : ScaledSimplicialSet Y}
    {HX : ScaledHornFamily X sX} {HY : ScaledHornFamily Y sY}
    (A : ScaledHornPresentationEquivalence HX HY) :
    ScaledHornPresentationEquivalence HY HX where
  forward := A.backward
  backward := A.forward
  forward_admissible := A.backward_admissible
  backward_admissible := A.forward_admissible
  forward_filler := A.backward_filler
  backward_filler := A.forward_filler
  forward_backward_filler_equiv := A.backward_forward_filler_equiv
  backward_forward_filler_equiv := A.forward_backward_filler_equiv

private def presentationEquivalenceComp
    {X : SSet.{u₁}} {Y : SSet.{u₂}} {Z : SSet.{u₃}}
    {sX : ScaledSimplicialSet X} {sY : ScaledSimplicialSet Y}
    {sZ : ScaledSimplicialSet Z}
    {HX : ScaledHornFamily X sX} {HY : ScaledHornFamily Y sY}
    {HZ : ScaledHornFamily Z sZ}
    (A : ScaledHornPresentationEquivalence HX HY)
    (D : ScaledHornPresentationEquivalence HY HZ) :
    ScaledHornPresentationEquivalence HX HZ where
  forward := fun P => D.forward (A.forward P)
  backward := fun R => A.backward (D.backward R)
  forward_admissible := by
    intro n i P hP
    exact D.forward_admissible (A.forward P) (A.forward_admissible P hP)
  backward_admissible := by
    intro n i R hR
    exact A.backward_admissible (D.backward R) (D.backward_admissible R hR)
  forward_filler := by
    intro n i P h
    exact D.forward_filler (A.forward P) (A.forward_filler P h)
  backward_filler := by
    intro n i R h
    exact A.backward_filler (D.backward R) (D.backward_filler R h)
  forward_backward_filler_equiv := by
    intro n i R
    exact (presentationForwardFillerIff D
      (A.forward (A.backward (D.backward R)))).trans
        ((A.forward_backward_filler_equiv (D.backward R)).trans
          (presentationBackwardFillerIff D R))
  backward_forward_filler_equiv := by
    intro n i P
    exact (presentationBackwardFillerIff A
      (D.backward (D.forward (A.forward P)))).trans
        ((D.backward_forward_filler_equiv (A.forward P)).trans
          (presentationForwardFillerIff A P))

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
  liftedSourceFamily : ScaledHornFamily
    (normalizedDuskinSource B C) (normalizedDuskinSourceScaling B C)
  liftedTargetFamily : ScaledHornFamily
    (normalizedDuskinTarget B C) (normalizedDuskinTargetScaling B C)
  sourceBridge : ScaledHornPresentationEquivalence HB liftedSourceFamily
  targetBridge : ScaledHornPresentationEquivalence HC liftedTargetFamily
  forwardFamily :
    ScaledHornFamilyMap forwardScaled.map_scaled
      liftedSourceFamily liftedTargetFamily
  backwardFamily :
    ScaledHornFamilyMap backwardScaled.map_scaled
      liftedTargetFamily liftedSourceFamily
  forward_backward_filler_equiv :
    ∀ {n : Nat} {i : Fin (n + 1)}
      (Q : ScaledHornExtensionProblem
        (normalizedDuskinTarget B C) (normalizedDuskinTargetScaling B C) n i),
      Nonempty (ScaledHornFiller
        (transportGlobalDuskinHornProblem forwardScaled
          (transportGlobalDuskinHornProblem backwardScaled Q))) ↔
        Nonempty (ScaledHornFiller Q)
  backward_forward_filler_equiv :
    ∀ {n : Nat} {i : Fin (n + 1)}
      (P : ScaledHornExtensionProblem
        (normalizedDuskinSource B C) (normalizedDuskinSourceScaling B C) n i),
      Nonempty (ScaledHornFiller
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
    ScaledHornPresentationEquivalence HB HC := by
  let L : ScaledHornPresentationEquivalence
      E.liftedSourceFamily E.liftedTargetFamily := {
    forward := fun P => transportGlobalDuskinHornProblem E.forwardScaled P
    backward := fun Q => transportGlobalDuskinHornProblem E.backwardScaled Q
    forward_admissible := by
      intro n i P hP
      exact E.forwardFamily.admissible_preserved P hP
    backward_admissible := by
      intro n i Q hQ
      exact E.backwardFamily.admissible_preserved Q hQ
    forward_filler := by
      intro n i P hP
      exact mapScaledHornFiller_nonempty E.forwardScaled.map_scaled hP
    backward_filler := by
      intro n i Q hQ
      exact mapScaledHornFiller_nonempty E.backwardScaled.map_scaled hQ
    forward_backward_filler_equiv := E.forward_backward_filler_equiv
    backward_forward_filler_equiv := E.backward_forward_filler_equiv
  }
  exact presentationEquivalenceComp
    (presentationEquivalenceComp E.sourceBridge L)
    (presentationEquivalenceSymm E.targetBridge)

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
