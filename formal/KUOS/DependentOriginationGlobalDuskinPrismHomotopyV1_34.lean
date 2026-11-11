import KUOS.DependentOriginationScaledHornHomotopyDescentV1_33

namespace KUOS.DependentOriginationGlobalDuskinPrismHomotopyV1_34

open CategoryTheory
open CategoryTheory.Category
open Simplicial
open KUOS.DependentOriginationBiequivalencePresentationInvariantV1_26
open MonoidalCategory
open KUOS.DependentOriginationGlobalDuskinScaledNerveV1_21
open KUOS.DependentOriginationGlobalDuskinScaledHornCoherenceV1_22
open KUOS.DependentOriginationStrictlyUnitaryDuskinModelTransportV1_27
open KUOS.DependentOriginationNormalizationChoiceInvariantV1_28
open KUOS.DependentOriginationScaledDuskinHornTransportV1_29
open KUOS.DependentOriginationCoherentNormalizedScaledModelEquivalenceV1_32
open KUOS.DependentOriginationScaledHornHomotopyDescentV1_33
open KUOS.DependentOriginationScaledHornPresentationInvariantV1_30

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
homotopy precomposition construction.  The only nontrivial relative boundary
condition is the bottom-subcomplex condition built into `SSet.Homotopy`.
-/
noncomputable def precompSSetHomotopy
    {W X Y : SSet.{u}}
    {f g : X ⟶ Y}
    (H : SSet.Homotopy f g)
    (k : W ⟶ X) :
    SSet.Homotopy (k ≫ f) (k ≫ g) where
  h := k ▷ Δ[1] ≫ H.h
  rel := by
    rw [Category.assoc, ← comp_whiskerRight_assoc,
      (SSet.RelativeMorphism.botEquiv.symm k).comm,
      comp_whiskerRight_assoc, H.rel, whiskerRight_fst_assoc]
    cat_disch

/-! ## One global prism replaces all hornwise round-trip homotopies -/

/--
A global Duskin-prism realization of a normalized coherent quasi-inverse.

The source component compares the composite normalized Duskin map
`N(B) -> N(C) -> N(B)` with the identity.  The target component is analogous.
The parameter `K` records which native strong quasi-inverse this prism is meant
to realize; no claim is made here that every strong transformation has already
been converted to such a prism.
-/
structure GlobalDuskinRoundTripPrismRealization
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    {F : StrictlyUnitaryBicategoricalModelEquivalence B C}
    {G : StrictlyUnitaryBicategoricalModelEquivalence C B}
    (K : NormalizedCoherentQuasiInverse F G) where
  sourcePrism :
    SSet.Homotopy
      (normalizedDuskinNerveMap F ≫ normalizedDuskinNerveMap G)
      (𝟙 (normalizedDuskinSource B C))
  targetPrism :
    SSet.Homotopy
      (normalizedDuskinNerveMap G ≫ normalizedDuskinNerveMap F)
      (𝟙 (normalizedDuskinTarget B C))

namespace GlobalDuskinRoundTripPrismRealization

variable
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    {F : StrictlyUnitaryBicategoricalModelEquivalence B C}
    {G : StrictlyUnitaryBicategoricalModelEquivalence C B}
    {K : NormalizedCoherentQuasiInverse F G}

/-- Restrict the source global prism along one prescribed horn map. -/
noncomputable def sourceHornHomotopy
    (R : GlobalDuskinRoundTripPrismRealization K)
    {n : Nat} {i : Fin (n + 1)}
    (P : ScaledHornExtensionProblem
      (normalizedDuskinSource B C) (normalizedDuskinSourceScaling B C) n i) :
    SSet.Homotopy
      (P.hornMap ≫
        (normalizedDuskinNerveMap F ≫ normalizedDuskinNerveMap G))
      P.hornMap := by
  simpa using precompSSetHomotopy R.sourcePrism P.hornMap

/-- Restrict the target global prism along one prescribed horn map. -/
noncomputable def targetHornHomotopy
    (R : GlobalDuskinRoundTripPrismRealization K)
    {n : Nat} {i : Fin (n + 1)}
    (Q : ScaledHornExtensionProblem
      (normalizedDuskinTarget B C) (normalizedDuskinTargetScaling B C) n i) :
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
    (R : GlobalDuskinRoundTripPrismRealization K)
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
    (R : GlobalDuskinRoundTripPrismRealization K)
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
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
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
  liftedSourceFamily : ScaledHornFamily
    (normalizedDuskinSource B C) (normalizedDuskinSourceScaling B C)
  liftedTargetFamily : ScaledHornFamily
    (normalizedDuskinTarget B C) (normalizedDuskinTargetScaling B C)
  sourceBridge : ScaledHornPresentationEquivalence HB liftedSourceFamily
  targetBridge : ScaledHornPresentationEquivalence HC liftedTargetFamily
  forwardFamily : ScaledHornFamilyMap forwardScaled.map_scaled
    liftedSourceFamily liftedTargetFamily
  backwardFamily : ScaledHornFamilyMap backwardScaled.map_scaled
    liftedTargetFamily liftedSourceFamily
  globalPrism : GlobalDuskinRoundTripPrismRealization quasiInverse
  sourceRectification :
    ScaledHornHomotopyRectification (normalizedDuskinSource B C) (normalizedDuskinSourceScaling B C)
  targetRectification :
    ScaledHornHomotopyRectification (normalizedDuskinTarget B C) (normalizedDuskinTargetScaling B C)
  /-- Preserve the original unlifted rectification requirements separately. -/
  unliftedSourceRectification :
    ScaledHornHomotopyRectification (duskinNerve B) (duskinScaling B)
  unliftedTargetRectification :
    ScaledHornHomotopyRectification (duskinNerve C) (duskinScaling C)

namespace CoherentNormalizedScaledPrismModelEquivalence

variable
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    {E : BicategoricalModelEquivalence B C}
    {G : BicategoricalModelEquivalence C B}
    {HB : GlobalDuskinScaledHornFamily B}
    {HC : GlobalDuskinScaledHornFamily C}

/-- Forget the global-prism presentation and recover the v1.33 package. -/
noncomputable def toHomotopyModelEquivalence
    (K : CoherentNormalizedScaledPrismModelEquivalence E G HB HC) :
    CoherentNormalizedScaledHomotopyModelEquivalence E G HB HC where
  forwardNormalization := K.forwardNormalization
  backwardNormalization := K.backwardNormalization
  quasiInverse := K.quasiInverse
  forwardScaled := K.forwardScaled
  backwardScaled := K.backwardScaled
  liftedSourceFamily := K.liftedSourceFamily
  liftedTargetFamily := K.liftedTargetFamily
  sourceBridge := K.sourceBridge
  targetBridge := K.targetBridge
  forwardFamily := K.forwardFamily
  backwardFamily := K.backwardFamily
  homotopyRealization :=
    K.globalPrism.toNormalizedQuasiInverseDuskinHomotopyRealization
      K.forwardScaled K.backwardScaled
  sourceRectification := K.unliftedSourceRectification
  targetRectification := K.unliftedTargetRectification
  liftedSourceRectification := K.sourceRectification
  liftedTargetRectification := K.targetRectification

/-- Global scaled-Duskin fibrancy is invariant under the global-prism package. -/
theorem globalDuskinScaledFibrancy_iff
    (K : CoherentNormalizedScaledPrismModelEquivalence E G HB HC) :
    HasScaledHornFillers (duskinNerve B) (duskinScaling B) HB ↔
      HasScaledHornFillers (duskinNerve C) (duskinScaling C) HC :=
  K.toHomotopyModelEquivalence.globalDuskinScaledFibrancy_iff

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
