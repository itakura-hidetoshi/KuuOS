import KUOS.DependentOriginationLiftedDuskinStrictInverseDescentV1_29
import KUOS.DependentOriginationScaledDuskinUniverseLiftBridgeV1_29

/-!
# Typed unlifted/lifted scaled-horn descent: canonical same-universe case

This append-only file constructs, rather than assumes, the presentation
equivalence for a genuine *scaled isomorphism* of simplicial carriers.
It then applies the construction to the objectwise ULift equivalence at
the same ambient SSet universe. Both the horn problems and their fillers
are transported with the same horn indices, horn scaling and simplex scaling.

For independent different universe levels, a further natural isomorphism
between the ULift of each representable horn/simplex and its larger-universe
representable remains an independent obligation. This module does not
identify arbitrary admissibility predicates or claim that extra bridge.
-/

namespace KUOS.DependentOriginationCanonicalULiftHornPresentationBridgeV1_29

open CategoryTheory
open Simplicial
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationGlobalDuskinScaledHornCoherenceV1_22
open KUOS.DependentOriginationScaledDuskinHornTransportV1_29
open KUOS.DependentOriginationScaledDuskinUniverseLiftBridgeV1_29
open KUOS.DependentOriginationLiftedDuskinRoundTripBridgeV1_29
open KUOS.DependentOriginationLiftedDuskinStrictInverseDescentV1_29
open KUOS.DependentOriginationScaledHornPresentationInvariantTypedRepairV1_30

universe u

/-- Transport an admissibility predicate *backwards* along a scaled map.
No assertion that an arbitrary target family has the same predicate is made. -/
def pulledBackHornFamily
    {X Y : SSet.{u}}
    {sX : ScaledSimplicialSet X}
    {sY : ScaledSimplicialSet Y}
    {g : Y ⟶ X}
    (hg : IsScaledMap sY sX g)
    (FX : ScaledHornFamily X sX) :
    ScaledHornFamily Y sY where
  admissible := fun {_ _} Q => FX.admissible (mapScaledHornProblem hg Q)

/-- A genuinely scaled isomorphism reflects horn problems exactly. -/
theorem scaledIso_problem_roundTrip
    {X Y : SSet.{u}}
    {sX : ScaledSimplicialSet X}
    {sY : ScaledSimplicialSet Y}
    (e : X ≅ Y)
    (hf : IsScaledMap sX sY e.hom)
    (hg : IsScaledMap sY sX e.inv)
    {n : Nat} {i : Fin (n + 1)}
    (P : ScaledHornExtensionProblem X sX n i) :
    mapScaledHornProblem hg (mapScaledHornProblem hf P) = P := by
  calc
    mapScaledHornProblem hg (mapScaledHornProblem hf P) =
        mapScaledHornProblem (hf.comp hg) P :=
      mapScaledHornProblem_comp hf hg P
    _ = mapScaledHornProblem (isScaledMap_id sX) P :=
      mapScaledHornProblem_congr (hf.comp hg) (isScaledMap_id sX)
        e.hom_inv_id P
    _ = P := mapScaledHornProblem_id P

/-- A scaled isomorphism canonically supplies the full typed horn-presentation
equivalence, including both filler-reflection laws; admissibility on the
target is the actual pullback of the source predicate, not an arbitrary choice. -/
def scaledIso_presentationEquivalence
    {X Y : SSet.{u}}
    {sX : ScaledSimplicialSet X}
    {sY : ScaledSimplicialSet Y}
    (e : X ≅ Y)
    (hf : IsScaledMap sX sY e.hom)
    (hg : IsScaledMap sY sX e.inv)
    (FX : ScaledHornFamily X sX) :
    ScaledHornPresentationEquivalence FX (pulledBackHornFamily hg FX) where
  forward := fun P => mapScaledHornProblem hf P
  backward := fun Q => mapScaledHornProblem hg Q
  forward_admissible := by
    intro n i P hP
    change FX.admissible
      (mapScaledHornProblem hg (mapScaledHornProblem hf P))
    rw [scaledIso_problem_roundTrip e hf hg P]
    exact hP
  backward_admissible := by
    intro n i Q hQ
    exact hQ
  forward_filler := by
    intro n i P hP
    exact mapScaledHornFiller_nonempty hf hP
  backward_filler := by
    intro n i Q hQ
    exact mapScaledHornFiller_nonempty hg hQ
  forward_backward_filler_equiv := by
    intro n i Q
    exact roundTrip_filler_iff_of_leftInverse hg hf e.inv_hom_id Q
  backward_forward_filler_equiv := by
    intro n i P
    exact roundTrip_filler_iff_of_leftInverse hf hg e.hom_inv_id P

/-- Pointwise ULift is a true simplicial-set isomorphism at a *fixed*
ambient universe. Naturality follows from ULift.up commuting with every
simplicial operator. -/
def sameUniverseULiftIso (X : SSet.{u}) :
    X ≅ (SSet.uliftFunctor.{u, u}).obj X :=
  NatIso.ofComponents
    (fun d => (Equiv.ulift.symm : X.obj d ≃ ULift.{u} (X.obj d)).toIso)
    (fun {_ _} _ => by
      ext x
      rfl)

/-- The forward pointwise ULift is a scaled map for the canonical scaling. -/
theorem sameUniverseULiftIso_hom_scaled
    {X : SSet.{u}}
    (sX : ScaledSimplicialSet X) :
    IsScaledMap sX (uliftScaling.{u, u} sX) (sameUniverseULiftIso X).hom := by
  intro t ht
  change sX.thin t
  exact ht

/-- The inverse pointwise ULift is scaled, with no additional thinness axiom. -/
theorem sameUniverseULiftIso_inv_scaled
    {X : SSet.{u}}
    (sX : ScaledSimplicialSet X) :
    IsScaledMap (uliftScaling.{u, u} sX) sX (sameUniverseULiftIso X).inv := by
  intro t ht
  change sX.thin t.down
  exact ht

/-- Canonical admissibility family on the same-universe ULift carrier. -/
def canonicalSameUniverseULiftFamily
    {X : SSet.{u}}
    (sX : ScaledSimplicialSet X)
    (FX : ScaledHornFamily X sX) :
    ScaledHornFamily ((SSet.uliftFunctor.{u, u}).obj X)
      (uliftScaling.{u, u} sX) :=
  pulledBackHornFamily (sameUniverseULiftIso_inv_scaled sX) FX

/-- The desired E bridge is constructed, rather than supplied, for the
same-universe ULift. It is an equivalence of actual horn presentations. -/
def canonicalSameUniverseULiftPresentationEquivalence
    {X : SSet.{u}}
    (sX : ScaledSimplicialSet X)
    (FX : ScaledHornFamily X sX) :
    ScaledHornPresentationEquivalence FX
      (canonicalSameUniverseULiftFamily sX FX) :=
  scaledIso_presentationEquivalence
    (sameUniverseULiftIso X)
    (sameUniverseULiftIso_hom_scaled sX)
    (sameUniverseULiftIso_inv_scaled sX) FX

/-- Fibrancy descends in both directions between the unlifted carrier and
its canonical same-universe lift, without either E_B or E_C as an axiom. -/
theorem canonicalSameUniverseULift_fibrancy_iff
    {X : SSet.{u}}
    (sX : ScaledSimplicialSet X)
    (FX : ScaledHornFamily X sX) :
    HasScaledHornFillers X sX FX ↔
      HasScaledHornFillers ((SSet.uliftFunctor.{u, u}).obj X)
        (uliftScaling.{u, u} sX)
        (canonicalSameUniverseULiftFamily sX FX) :=
  hasScaledHornFillers_iff
    (canonicalSameUniverseULiftPresentationEquivalence sX FX)

#print axioms scaledIso_problem_roundTrip
#print axioms scaledIso_presentationEquivalence
#print axioms sameUniverseULiftIso
#print axioms canonicalSameUniverseULiftPresentationEquivalence
#print axioms canonicalSameUniverseULift_fibrancy_iff

end KUOS.DependentOriginationCanonicalULiftHornPresentationBridgeV1_29
