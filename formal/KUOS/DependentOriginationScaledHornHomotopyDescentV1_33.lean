import KUOS.DependentOriginationCoherentNormalizedScaledModelEquivalenceV1_32
import Mathlib.AlgebraicTopology.SimplicialSet.Homotopy

namespace KUOS.DependentOriginationScaledHornHomotopyDescentV1_33

open CategoryTheory
open CategoryTheory.Category
open Simplicial
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationGlobalDuskinScaledNerveV1_21
open KUOS.DependentOriginationGlobalDuskinScaledHornCoherenceV1_22
open KUOS.DependentOriginationBiequivalencePresentationInvariantV1_26
open KUOS.DependentOriginationStrictlyUnitaryDuskinModelTransportV1_27
open KUOS.DependentOriginationNormalizationChoiceInvariantV1_28
open KUOS.DependentOriginationScaledDuskinHornTransportV1_29
open KUOS.DependentOriginationCoherentNormalizedScaledModelEquivalenceV1_32

universe u u₁ u₂ v₁ v₂ w₁ w₂

/-!
# Scaled horn homotopy descent v1.33

Version 1.32 isolated `ScaledHornRoundTripDescent` as the last bridge between
coherent normalized bicategorical round trips and strict scaled-horn filler
existence.  This file resolves the logical structure of that bridge.

A strict filler of a round-trip horn does not, from a simplicial homotopy alone,
automatically become a strict filler of the original horn.  What the homotopy
canonically gives is a simplex whose boundary is *homotopic* to the prescribed
horn map.  Therefore the correct factorization is

```text
strict round-trip filler
  + hornwise round-trip homotopy
  -> homotopy filler of the original horn
  + homotopy-to-strict rectification
  -> strict filler of the original horn.
```

This avoids silently assuming a lifting theorem.  The forward direction from an
original strict filler to a round-trip strict filler is already automatic from
v1.29 by postcomposition with the two scaled Duskin maps.

The pinned Mathlib revision supplies the native `SSet.Homotopy` used below.
-/

/--
A homotopy filler has a scaled simplex map whose boundary is simplicially
homotopic to the prescribed horn map.

The homotopy is oriented from the actual boundary of the simplex map to the
prescribed horn map.  This matches the `roundTrip ==> id` orientation of the
native strong quasi-inverse data from v1.32.
-/
structure HomotopyScaledHornFiller
    {X : SSet.{u}}
    {sX : ScaledSimplicialSet X}
    {n : Nat} {i : Fin (n + 1)}
    (P : ScaledHornExtensionProblem X sX n i) where
  simplexMap : Δ[n] ⟶ X
  boundaryHomotopy :
    SSet.Homotopy (Λ[n, i].ι ≫ simplexMap) P.hornMap
  simplexMap_scaled : IsScaledMap P.simplexScaling sX simplexMap

/--
A scaled horn presentation admits homotopy rectification when every homotopy
filler can be replaced by an honest strict filler.

This is deliberately separated from the existence of the boundary homotopy.
It is the exact extra lifting property needed to turn homotopy invariance into
the strict horn-filling invariant used by v1.22--v1.32.
-/
structure ScaledHornHomotopyRectification
    (X : SSet.{u})
    (sX : ScaledSimplicialSet X) : Prop where
  rectify :
    ∀ {n : Nat} {i : Fin (n + 1)}
      (P : ScaledHornExtensionProblem X sX n i),
      Nonempty (HomotopyScaledHornFiller P) →
      Nonempty (ScaledHornFiller P)

/--
Hornwise simplicial homotopies from each normalized round trip back to the
original horn map.

This is the precise simplicial realization expected from the strong
quasi-inverse `G F ==> id_B` and `F G ==> id_C`.  It is weaker than demanding
literal equality of the round-trip simplicial maps and stronger than merely
knowing that object and 1-cell data are bicategorically equivalent.

The full scaled-Duskin transport certificates of v1.27-v1.29 are bundled in a
single universe triple.  We keep exactly that boundary here; the more general
coherent quasi-inverse itself remains universe-polymorphic in v1.32.
-/
structure ScaledHornRoundTripBoundaryHomotopy
    {B C : Type u₁}
    [Bicategory.{w₁, v₁} B] [Bicategory.{w₁, v₁} C]
    (F : StrictlyUnitaryBicategoricalModelEquivalence B C)
    (G : StrictlyUnitaryBicategoricalModelEquivalence C B)
    (HF : FullScaledDuskinMapCertificate F)
    (HG : FullScaledDuskinMapCertificate G) : Prop where
  source :
    ∀ {n : Nat} {i : Fin (n + 1)}
      (P : ScaledHornExtensionProblem
        (duskinNerve B) (duskinScaling B) n i),
      SSet.Homotopy
        ((transportGlobalDuskinHornProblem HG
          (transportGlobalDuskinHornProblem HF P)).hornMap)
        P.hornMap
  target :
    ∀ {n : Nat} {i : Fin (n + 1)}
      (Q : ScaledHornExtensionProblem
        (duskinNerve C) (duskinScaling C) n i),
      SSet.Homotopy
        ((transportGlobalDuskinHornProblem HF
          (transportGlobalDuskinHornProblem HG Q)).hornMap)
        Q.hornMap

/--
A realization certificate saying that the native coherent quasi-inverse of
v1.32 has been promoted to hornwise homotopies on the global Duskin nerves.

The construction of this certificate from `Oplax.StrongTrans` is now a sharply
isolated nerve/prism problem rather than part of the filler-descent argument.
-/
structure NormalizedQuasiInverseDuskinHomotopyRealization
    {B C : Type u₁}
    [Bicategory.{w₁, v₁} B] [Bicategory.{w₁, v₁} C]
    {F : StrictlyUnitaryBicategoricalModelEquivalence B C}
    {G : StrictlyUnitaryBicategoricalModelEquivalence C B}
    (K : NormalizedCoherentQuasiInverse F G)
    (HF : FullScaledDuskinMapCertificate F)
    (HG : FullScaledDuskinMapCertificate G) : Prop where
  hornwise : ScaledHornRoundTripBoundaryHomotopy F G HF HG

/--
A strict round-trip source filler canonically becomes a homotopy filler of the
original source horn once the hornwise round-trip homotopy is supplied.
-/
def sourceHomotopyFillerOfRoundTrip
    {B C : Type u₁}
    [Bicategory.{w₁, v₁} B] [Bicategory.{w₁, v₁} C]
    {F : StrictlyUnitaryBicategoricalModelEquivalence B C}
    {G : StrictlyUnitaryBicategoricalModelEquivalence C B}
    {HF : FullScaledDuskinMapCertificate F}
    {HG : FullScaledDuskinMapCertificate G}
    (H : ScaledHornRoundTripBoundaryHomotopy F G HF HG)
    {n : Nat} {i : Fin (n + 1)}
    {P : ScaledHornExtensionProblem
      (duskinNerve B) (duskinScaling B) n i}
    (Q : ScaledHornFiller
      (transportGlobalDuskinHornProblem HG
        (transportGlobalDuskinHornProblem HF P))) :
    HomotopyScaledHornFiller P where
  simplexMap := Q.simplexMap
  boundaryHomotopy := by
    simpa [Q.extends_horn] using H.source P
  simplexMap_scaled := Q.simplexMap_scaled

/-- Target-side analogue of `sourceHomotopyFillerOfRoundTrip`. -/
def targetHomotopyFillerOfRoundTrip
    {B C : Type u₁}
    [Bicategory.{w₁, v₁} B] [Bicategory.{w₁, v₁} C]
    {F : StrictlyUnitaryBicategoricalModelEquivalence B C}
    {G : StrictlyUnitaryBicategoricalModelEquivalence C B}
    {HF : FullScaledDuskinMapCertificate F}
    {HG : FullScaledDuskinMapCertificate G}
    (H : ScaledHornRoundTripBoundaryHomotopy F G HF HG)
    {n : Nat} {i : Fin (n + 1)}
    {Q : ScaledHornExtensionProblem
      (duskinNerve C) (duskinScaling C) n i}
    (R : ScaledHornFiller
      (transportGlobalDuskinHornProblem HF
        (transportGlobalDuskinHornProblem HG Q))) :
    HomotopyScaledHornFiller Q where
  simplexMap := R.simplexMap
  boundaryHomotopy := by
    simpa [R.extends_horn] using H.target Q
  simplexMap_scaled := R.simplexMap_scaled

/-- Nonempty source round-trip fillers yield nonempty source homotopy fillers. -/
theorem sourceRoundTripFiller_to_homotopyFiller
    {B C : Type u₁}
    [Bicategory.{w₁, v₁} B] [Bicategory.{w₁, v₁} C]
    {F : StrictlyUnitaryBicategoricalModelEquivalence B C}
    {G : StrictlyUnitaryBicategoricalModelEquivalence C B}
    {HF : FullScaledDuskinMapCertificate F}
    {HG : FullScaledDuskinMapCertificate G}
    (H : ScaledHornRoundTripBoundaryHomotopy F G HF HG)
    {n : Nat} {i : Fin (n + 1)}
    {P : ScaledHornExtensionProblem
      (duskinNerve B) (duskinScaling B) n i}
    (h : Nonempty
      (ScaledHornFiller
        (transportGlobalDuskinHornProblem HG
          (transportGlobalDuskinHornProblem HF P)))) :
    Nonempty (HomotopyScaledHornFiller P) := by
  rcases h with ⟨Q⟩
  exact ⟨sourceHomotopyFillerOfRoundTrip H Q⟩

/-- Nonempty target round-trip fillers yield nonempty target homotopy fillers. -/
theorem targetRoundTripFiller_to_homotopyFiller
    {B C : Type u₁}
    [Bicategory.{w₁, v₁} B] [Bicategory.{w₁, v₁} C]
    {F : StrictlyUnitaryBicategoricalModelEquivalence B C}
    {G : StrictlyUnitaryBicategoricalModelEquivalence C B}
    {HF : FullScaledDuskinMapCertificate F}
    {HG : FullScaledDuskinMapCertificate G}
    (H : ScaledHornRoundTripBoundaryHomotopy F G HF HG)
    {n : Nat} {i : Fin (n + 1)}
    {Q : ScaledHornExtensionProblem
      (duskinNerve C) (duskinScaling C) n i}
    (h : Nonempty
      (ScaledHornFiller
        (transportGlobalDuskinHornProblem HF
          (transportGlobalDuskinHornProblem HG Q)))) :
    Nonempty (HomotopyScaledHornFiller Q) := by
  rcases h with ⟨R⟩
  exact ⟨targetHomotopyFillerOfRoundTrip H R⟩

/--
Hornwise round-trip homotopy plus homotopy rectification implies the exact
`ScaledHornRoundTripDescent` certificate required by v1.32.

The reverse directions of both equivalences are theorem-level already: an
original strict filler is simply postcomposed with the two scaled Duskin maps.
-/
theorem scaledHornRoundTripDescent_of_homotopy_rectification
    {B C : Type u₁}
    [Bicategory.{w₁, v₁} B] [Bicategory.{w₁, v₁} C]
    (HB : GlobalDuskinScaledHornFamily B)
    (HC : GlobalDuskinScaledHornFamily C)
    (F : StrictlyUnitaryBicategoricalModelEquivalence B C)
    (G : StrictlyUnitaryBicategoricalModelEquivalence C B)
    (HF : FullScaledDuskinMapCertificate F)
    (HG : FullScaledDuskinMapCertificate G)
    (H : ScaledHornRoundTripBoundaryHomotopy F G HF HG)
    (RB : ScaledHornHomotopyRectification
      (duskinNerve B) (duskinScaling B))
    (RC : ScaledHornHomotopyRectification
      (duskinNerve C) (duskinScaling C)) :
    ScaledHornRoundTripDescent HB HC F G HF HG where
  source_roundTrip_filler_equiv := by
    intro n i P
    constructor
    · intro h
      exact RB.rectify P (sourceRoundTripFiller_to_homotopyFiller H h)
    · intro h
      exact mapScaledHornFiller_nonempty HG.map_scaled
        (mapScaledHornFiller_nonempty HF.map_scaled h)
  target_roundTrip_filler_equiv := by
    intro n i Q
    constructor
    · intro h
      exact RC.rectify Q (targetRoundTripFiller_to_homotopyFiller H h)
    · intro h
      exact mapScaledHornFiller_nonempty HF.map_scaled
        (mapScaledHornFiller_nonempty HG.map_scaled h)

/--
Construction-level package replacing the primitive horn-descent field of v1.32
by its two mathematically distinct ingredients: Duskin hornwise homotopy and
homotopy rectification.
-/
structure CoherentNormalizedScaledHomotopyModelEquivalence
    {B C : Type u₁}
    [Bicategory.{w₁, v₁} B] [Bicategory.{w₁, v₁} C]
    (E : BicategoricalModelEquivalence B C)
    (G : BicategoricalModelEquivalence C B)
    (HB : GlobalDuskinScaledHornFamily B)
    (HC : GlobalDuskinScaledHornFamily C) where
  forwardNormalization : StrictlyUnitaryNormalizationCertificate E
  backwardNormalization : StrictlyUnitaryNormalizationCertificate G
  quasiInverse :
    NormalizedCoherentQuasiInverse
      forwardNormalization.normal backwardNormalization.normal
  forwardScaled : FullScaledDuskinMapCertificate forwardNormalization.normal
  backwardScaled : FullScaledDuskinMapCertificate backwardNormalization.normal
  forwardFamily : ScaledHornFamilyMap forwardScaled.map_scaled HB HC
  backwardFamily : ScaledHornFamilyMap backwardScaled.map_scaled HC HB
  homotopyRealization :
    NormalizedQuasiInverseDuskinHomotopyRealization
      quasiInverse forwardScaled backwardScaled
  sourceRectification :
    ScaledHornHomotopyRectification (duskinNerve B) (duskinScaling B)
  targetRectification :
    ScaledHornHomotopyRectification (duskinNerve C) (duskinScaling C)

namespace CoherentNormalizedScaledHomotopyModelEquivalence

variable
    {B C : Type u₁}
    [Bicategory.{w₁, v₁} B] [Bicategory.{w₁, v₁} C]
    {E : BicategoricalModelEquivalence B C}
    {G : BicategoricalModelEquivalence C B}
    {HB : GlobalDuskinScaledHornFamily B}
    {HC : GlobalDuskinScaledHornFamily C}
    (K : CoherentNormalizedScaledHomotopyModelEquivalence E G HB HC)

/-- The homotopy-level construction supplies the exact v1.32 package. -/
def toCoherentNormalizedScaledModelEquivalence :
    CoherentNormalizedScaledModelEquivalence E G HB HC where
  forwardNormalization := K.forwardNormalization
  backwardNormalization := K.backwardNormalization
  quasiInverse := K.quasiInverse
  forwardScaled := K.forwardScaled
  backwardScaled := K.backwardScaled
  forwardFamily := K.forwardFamily
  backwardFamily := K.backwardFamily
  hornDescent :=
    scaledHornRoundTripDescent_of_homotopy_rectification
      HB HC
      K.forwardNormalization.normal K.backwardNormalization.normal
      K.forwardScaled K.backwardScaled
      K.homotopyRealization.hornwise
      K.sourceRectification K.targetRectification

/-- Hence global scaled-Duskin fibrancy is invariant. -/
theorem globalDuskinScaledFibrancy_iff :
    HasScaledHornFillers (duskinNerve B) (duskinScaling B) HB ↔
      HasScaledHornFillers (duskinNerve C) (duskinScaling C) HC :=
  KUOS.DependentOriginationCoherentNormalizedScaledModelEquivalenceV1_32.CoherentNormalizedScaledModelEquivalence.globalDuskinScaledFibrancy_iff
    (toCoherentNormalizedScaledModelEquivalence K)

end CoherentNormalizedScaledHomotopyModelEquivalence

/-!
The v1.33 boundary is therefore more precise than v1.32:

```text
native strong quasi-inverse
  -> hornwise Duskin round-trip homotopy             -- isolated realization problem
round-trip strict filler + hornwise homotopy
  -> homotopy filler                                 -- proved here
homotopy filler + homotopy rectification
  -> strict filler                                   -- explicit rectification property
original strict filler
  -> round-trip strict filler                        -- automatic by scaled postcomposition

therefore
hornwise homotopy + rectification
  -> ScaledHornRoundTripDescent                      -- proved here
  -> presentation-independent scaled fibrancy        -- v1.32/v1.31/v1.30.
```

The next construction problem is now sharply split in two: realize the native
strong transformations as hornwise simplicial homotopies of the global Duskin
nerve, and establish rectification for the chosen standard scaled-horn family.
-/

end KUOS.DependentOriginationScaledHornHomotopyDescentV1_33