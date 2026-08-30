import KUOS.DependentOriginationScaledHornHomotopyDescentV1_33

namespace KUOS.DependentOriginationGlobalDuskinPrismHomotopyV1_34

open CategoryTheory
open CategoryTheory.Category
open Simplicial
open MonoidalCategory
open KUOS.DependentOriginationGlobalDuskinScaledNerveV1_21
open KUOS.DependentOriginationGlobalDuskinScaledHornCoherenceV1_22
open KUOS.DependentOriginationBiequivalencePresentationInvariantV1_26
open KUOS.DependentOriginationStrictlyUnitaryDuskinModelTransportV1_27
open KUOS.DependentOriginationNormalizationChoiceInvariantV1_28
open KUOS.DependentOriginationScaledDuskinHornTransportV1_29
open KUOS.DependentOriginationCoherentNormalizedScaledModelEquivalenceV1_32
open KUOS.DependentOriginationScaledHornHomotopyDescentV1_33

universe u u₁ u₂ v₁ v₂ w₁ w₂

/-!
# Global Duskin prism homotopy v1.34

Version 1.33 reduced strict round-trip filler descent to two independent
ingredients: hornwise simplicial homotopy and homotopy-to-strict
rectification.  The first ingredient was still recorded separately for every
horn.

This layer globalizes that datum.  A single simplicial homotopy

```text
N(F) ; N(G)  ~  id_{N(B)}
```

restricts along every horn map, hence produces all source hornwise homotopies
at once; likewise on the target.  This is the correct global prism object to be
constructed from the native strong transformations `G F ==> id_B` and
`F G ==> id_C`.

The remaining prism-construction problem is therefore no longer quantified over
horns.  It is a single pair of `SSet.Homotopy` values between global Duskin
simplicial maps.
-/

/-! ## Simplicial homotopy is stable under precomposition -/

/--
Precompose a simplicial homotopy with an arbitrary simplicial map.

This is the ordinary `SSet.Homotopy` specialization of Mathlib's relative
homotopy precomposition construction.  The relative bottom-subcomplex
bookkeeping is delegated to the native `RelativeMorphism.Homotopy.precomp`.
-/
noncomputable def precompSSetHomotopy
    {W X Y : SSet.{u}}
    {f g : X ⟶ Y}
    (H : SSet.Homotopy f g)
    (k : W ⟶ X) :
    SSet.Homotopy (k ≫ f) (k ≫ g) := by
  let H' :=
    SSet.RelativeMorphism.Homotopy.precomp H
      (SSet.RelativeMorphism.botEquiv.symm k)
      (φψ := SSet.Subcomplex.isInitialBot.to _)
      (by cat_disch)
  exact {
    h := H'.h
    h₀ := by simpa using H'.h₀
    h₁ := by simpa using H'.h₁
    rel := by simpa using H'.rel
  }

/-! ## One global prism replaces all hornwise round-trip homotopies -/

/--
A global Duskin-prism realization of a normalized coherent quasi-inverse.

The source component compares the composite normalized Duskin map
`N(B) -> N(C) -> N(B)` with the identity.  The target component is analogous.
The parameter `K` records which native strong quasi-inverse this prism is meant
to realize; no claim is made here that every strong transformation has already
been converted to such a prism.

As for the full scaled-Duskin transport layer, source and target live in one
universe triple so that both normalized nerve maps compose as maps of one
simplicial-set universe.
-/
structure GlobalDuskinRoundTripPrismRealization
    {B C : Type u₁}
    [Bicategory.{w₁, v₁} B] [Bicategory.{w₁, v₁} C]
    {F : StrictlyUnitaryBicategoricalModelEquivalence B C}
    {G : StrictlyUnitaryBicategoricalModelEquivalence C B}
    (K : NormalizedCoherentQuasiInverse F G) where
  sourcePrism :
    SSet.Homotopy
      (normalizedDuskinNerveMap F ≫ normalizedDuskinNerveMap G)
      (𝟙 (duskinNerve B))
  targetPrism :
    SSet.Homotopy
      (normalizedDuskinNerveMap G ≫ normalizedDuskinNerveMap F)
      (𝟙 (duskinNerve C))

namespace GlobalDuskinRoundTripPrismRealization

variable
    {B C : Type u₁}
    [Bicategory.{w₁, v₁} B] [Bicategory.{w₁, v₁} C]
    {F : StrictlyUnitaryBicategoricalModelEquivalence B C}
    {G : StrictlyUnitaryBicategoricalModelEquivalence C B}
    {K : NormalizedCoherentQuasiInverse F G}
    (R : GlobalDuskinRoundTripPrismRealization K)

/-- Restrict the source global prism along one prescribed horn map. -/
noncomputable def sourceHornHomotopy
    {n : Nat} {i : Fin (n + 1)}
    (P : ScaledHornExtensionProblem
      (duskinNerve B) (duskinScaling B) n i) :
    SSet.Homotopy
      (P.hornMap ≫
        (normalizedDuskinNerveMap F ≫ normalizedDuskinNerveMap G))
      P.hornMap := by
  simpa using precompSSetHomotopy R.sourcePrism P.hornMap

/-- Restrict the target global prism along one prescribed horn map. -/
noncomputable def targetHornHomotopy
    {n : Nat} {i : Fin (n + 1)}
    (Q : ScaledHornExtensionProblem
      (duskinNerve C) (duskinScaling C) n i) :
    SSet.Homotopy
      (Q.hornMap ≫
        (normalizedDuskinNerveMap G ≫ normalizedDuskinNerveMap F))
      Q.hornMap := by
  simpa using precompSSetHomotopy R.targetPrism Q.hornMap

/--
A global prism automatically supplies the per-horn boundary-homotopy
certificate of v1.33.
-/
noncomputable def toRoundTripBoundaryHomotopy
    (HF : FullScaledDuskinMapCertificate F)
    (HG : FullScaledDuskinMapCertificate G) :
    ScaledHornRoundTripBoundaryHomotopy F G HF HG where
  source := by
    intro n i P
    simpa [transportGlobalDuskinHornProblem, mapScaledHornProblem,
      Category.assoc] using R.sourceHornHomotopy P
  target := by
    intro n i Q
    simpa [transportGlobalDuskinHornProblem, mapScaledHornProblem,
      Category.assoc] using R.targetHornHomotopy Q

/--
Consequently a single global prism realizes the v1.33 normalized quasi-inverse
homotopy certificate for every horn simultaneously.
-/
noncomputable def toNormalizedQuasiInverseDuskinHomotopyRealization
    (HF : FullScaledDuskinMapCertificate F)
    (HG : FullScaledDuskinMapCertificate G) :
    NormalizedQuasiInverseDuskinHomotopyRealization K HF HG where
  hornwise := R.toRoundTripBoundaryHomotopy HF HG

end GlobalDuskinRoundTripPrismRealization

/-! ## Construction-level presentation-independent package -/

/--
A coherent normalized scaled model equivalence whose homotopy data is supplied
by one global Duskin prism in each direction rather than separately on every
horn.
-/
structure CoherentNormalizedScaledPrismModelEquivalence
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
  globalPrism : GlobalDuskinRoundTripPrismRealization quasiInverse
  sourceRectification :
    ScaledHornHomotopyRectification (duskinNerve B) (duskinScaling B)
  targetRectification :
    ScaledHornHomotopyRectification (duskinNerve C) (duskinScaling C)

namespace CoherentNormalizedScaledPrismModelEquivalence

variable
    {B C : Type u₁}
    [Bicategory.{w₁, v₁} B] [Bicategory.{w₁, v₁} C]
    {E : BicategoricalModelEquivalence B C}
    {G : BicategoricalModelEquivalence C B}
    {HB : GlobalDuskinScaledHornFamily B}
    {HC : GlobalDuskinScaledHornFamily C}
    (K : CoherentNormalizedScaledPrismModelEquivalence E G HB HC)

/-- Forget the global-prism presentation and recover the v1.33 package. -/
noncomputable def toHomotopyModelEquivalence :
    CoherentNormalizedScaledHomotopyModelEquivalence E G HB HC where
  forwardNormalization := K.forwardNormalization
  backwardNormalization := K.backwardNormalization
  quasiInverse := K.quasiInverse
  forwardScaled := K.forwardScaled
  backwardScaled := K.backwardScaled
  forwardFamily := K.forwardFamily
  backwardFamily := K.backwardFamily
  homotopyRealization :=
    K.globalPrism.toNormalizedQuasiInverseDuskinHomotopyRealization
      K.forwardScaled K.backwardScaled
  sourceRectification := K.sourceRectification
  targetRectification := K.targetRectification

/-- Global scaled-Duskin fibrancy is invariant under the global-prism package. -/
theorem globalDuskinScaledFibrancy_iff
    (K : CoherentNormalizedScaledPrismModelEquivalence E G HB HC) :
    HasScaledHornFillers (duskinNerve B) (duskinScaling B) HB ↔
      HasScaledHornFillers (duskinNerve C) (duskinScaling C) HC :=
  KUOS.DependentOriginationScaledHornHomotopyDescentV1_33.CoherentNormalizedScaledHomotopyModelEquivalence.globalDuskinScaledFibrancy_iff
    (toHomotopyModelEquivalence K)

end CoherentNormalizedScaledPrismModelEquivalence

/-!
The v1.34 implication is now

```text
native strong quasi-inverse GF ==> id_B, FG ==> id_C
  + one global Duskin prism homotopy in each direction
  -> every hornwise round-trip homotopy automatically
  + homotopy rectification
  -> strict horn descent
  -> presentation-independent scaled fibrancy.
```

The remaining nerve-theoretic construction has become genuinely global:
construct `GlobalDuskinRoundTripPrismRealization K` directly from the two native
`Oplax.StrongTrans` values in `K`.  No horn-by-horn coherence choices remain.
-/

end KUOS.DependentOriginationGlobalDuskinPrismHomotopyV1_34