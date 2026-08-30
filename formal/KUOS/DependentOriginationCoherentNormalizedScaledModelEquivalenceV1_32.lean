import KUOS.DependentOriginationModelEquivalenceScaledHornPresentationV1_31
import Mathlib.CategoryTheory.Bicategory.NaturalTransformation.Oplax

namespace KUOS.DependentOriginationCoherentNormalizedScaledModelEquivalenceV1_32

open CategoryTheory
open CategoryTheory.Category
open CategoryTheory.Bicategory
open scoped Bicategory
open KUOS.DependentOriginationPresentationIndependentInvariantV1_25
open KUOS.DependentOriginationBiequivalencePresentationInvariantV1_26
open KUOS.DependentOriginationStrictlyUnitaryDuskinModelTransportV1_27
open KUOS.DependentOriginationNormalizationChoiceInvariantV1_28
open KUOS.DependentOriginationGlobalDuskinScaledNerveV1_21
open KUOS.DependentOriginationGlobalDuskinScaledHornCoherenceV1_22
open KUOS.DependentOriginationScaledDuskinHornTransportV1_29
open KUOS.DependentOriginationModelEquivalenceScaledHornPresentationV1_31

universe u₁ u₂ v₁ v₂ w₁ w₂

/-!
# Coherent normalized scaled model equivalence v1.32

Version 1.31 identified the exact bidirectional scaled-Duskin package sufficient
for presentation-independent scaled fibrancy.  This layer resolves the next
part of its existence problem: normalization and bicategorical quasi-inverse
coherence are now represented separately and natively.

For normalized model maps `F : B -> C` and `G : C -> B`, the quasi-inverse data
is expressed by Mathlib `Oplax.StrongTrans` comparisons

```text
G F  ==> id_B
F G  ==> id_C
```

whose object components are bicategorical equivalence 1-cells.  Thus the
round-trip is not required to be definitionally equal to the identity.

The remaining gap from coherent bicategorical equivalence to the current horn
interface is isolated as `ScaledHornRoundTripDescent`: filler existence must be
shown invariant under those coherent round trips.  Once that single descent
certificate is supplied, the v1.31 bidirectional scaled-Duskin model equivalence
is constructed automatically.
-/

/--
Native coherent quasi-inverse data between two strictly-unitary normalized
model equivalences.
-/
structure NormalizedCoherentQuasiInverse
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (F : StrictlyUnitaryBicategoricalModelEquivalence B C)
    (G : StrictlyUnitaryBicategoricalModelEquivalence C B) where
  sourceCounit :
    CategoryTheory.Oplax.StrongTrans
      (F.forward.toPseudofunctor.comp G.forward.toPseudofunctor).toOplax
      (Pseudofunctor.id B).toOplax
  targetCounit :
    CategoryTheory.Oplax.StrongTrans
      (G.forward.toPseudofunctor.comp F.forward.toPseudofunctor).toOplax
      (Pseudofunctor.id C).toOplax
  source_component_equivalence :
    ∀ X : B, IntrinsicEquivalenceOneCell (sourceCounit.app X)
  target_component_equivalence :
    ∀ Y : C, IntrinsicEquivalenceOneCell (targetCounit.app Y)

namespace NormalizedCoherentQuasiInverse

variable
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    {F : StrictlyUnitaryBicategoricalModelEquivalence B C}
    {G : StrictlyUnitaryBicategoricalModelEquivalence C B}
    (K : NormalizedCoherentQuasiInverse F G)

/-- The `G ∘ F` round trip is coherently the identity on every source 1-cell. -/
def sourceRoundTripOneCellIso
    {X Y : B} (f : X ⟶ Y) :
    (F.forward.toPseudofunctor.comp
        G.forward.toPseudofunctor).toOplax.map f ≫
        K.sourceCounit.app Y ≅
      K.sourceCounit.app X ≫
        (Pseudofunctor.id B).toOplax.map f :=
  K.sourceCounit.naturality f

/-- The `F ∘ G` round trip is coherently the identity on every target 1-cell. -/
def targetRoundTripOneCellIso
    {X Y : C} (f : X ⟶ Y) :
    (G.forward.toPseudofunctor.comp
        F.forward.toPseudofunctor).toOplax.map f ≫
        K.targetCounit.app Y ≅
      K.targetCounit.app X ≫
        (Pseudofunctor.id C).toOplax.map f :=
  K.targetCounit.naturality f

/-- The source round-trip comparison satisfies the native 2-cell naturality square. -/
theorem sourceRoundTripTwoCellNaturality
    {X Y : B} {f g : X ⟶ Y} (α : f ⟶ g) :
    (F.forward.toPseudofunctor.comp
        G.forward.toPseudofunctor).toOplax.map₂ α ▷
        K.sourceCounit.app Y ≫
        (K.sourceRoundTripOneCellIso g).hom =
      (K.sourceRoundTripOneCellIso f).hom ≫
        K.sourceCounit.app X ◁
          (Pseudofunctor.id B).toOplax.map₂ α := by
  exact K.sourceCounit.naturality_naturality α

/-- The target round-trip comparison satisfies the native 2-cell naturality square. -/
theorem targetRoundTripTwoCellNaturality
    {X Y : C} {f g : X ⟶ Y} (α : f ⟶ g) :
    (G.forward.toPseudofunctor.comp
        F.forward.toPseudofunctor).toOplax.map₂ α ▷
        K.targetCounit.app Y ≫
        (K.targetRoundTripOneCellIso g).hom =
      (K.targetRoundTripOneCellIso f).hom ≫
        K.targetCounit.app X ◁
          (Pseudofunctor.id C).toOplax.map₂ α := by
  exact K.targetCounit.naturality_naturality α

end NormalizedCoherentQuasiInverse

/--
The precise remaining bridge from coherent normalized round trips to the
current strict horn/filler presentation.

This certificate does not duplicate the bicategorical quasi-inverse: it records
only the additional fact that filler existence descends through the two
round-trip global Duskin transports.

The bundled global Duskin maps of v1.27-v1.29 are deliberately constructed
inside one universe triple, so this descent layer keeps exactly that boundary.
-/
structure ScaledHornRoundTripDescent
    {B C : Type u₁}
    [Bicategory.{w₁, v₁} B] [Bicategory.{w₁, v₁} C]
    (HB : GlobalDuskinScaledHornFamily B)
    (HC : GlobalDuskinScaledHornFamily C)
    (F : StrictlyUnitaryBicategoricalModelEquivalence B C)
    (G : StrictlyUnitaryBicategoricalModelEquivalence C B)
    (HF : FullScaledDuskinMapCertificate F)
    (HG : FullScaledDuskinMapCertificate G) : Prop where
  source_roundTrip_filler_equiv :
    ∀ {n : Nat} {i : Fin (n + 1)}
      (P : ScaledHornExtensionProblem
        (duskinNerve B) (duskinScaling B) n i),
      Nonempty
        (ScaledHornFiller
          (transportGlobalDuskinHornProblem HG
            (transportGlobalDuskinHornProblem HF P))) ↔
        Nonempty (ScaledHornFiller P)
  target_roundTrip_filler_equiv :
    ∀ {n : Nat} {i : Fin (n + 1)}
      (Q : ScaledHornExtensionProblem
        (duskinNerve C) (duskinScaling C) n i),
      Nonempty
        (ScaledHornFiller
          (transportGlobalDuskinHornProblem HF
            (transportGlobalDuskinHornProblem HG Q))) ↔
        Nonempty (ScaledHornFiller Q)

/--
General model-equivalence data together with chosen normalizations, a coherent
quasi-inverse between the normal representatives, full scaling, admissible
family preservation, and the final horn-descent bridge.

As soon as full scaled Duskin maps are bundled, source and target stay in the
same universe triple, exactly as in v1.29.
-/
structure CoherentNormalizedScaledModelEquivalence
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
  forwardScaled :
    FullScaledDuskinMapCertificate forwardNormalization.normal
  backwardScaled :
    FullScaledDuskinMapCertificate backwardNormalization.normal
  forwardFamily :
    ScaledHornFamilyMap forwardScaled.map_scaled HB HC
  backwardFamily :
    ScaledHornFamilyMap backwardScaled.map_scaled HC HB
  hornDescent :
    ScaledHornRoundTripDescent HB HC
      forwardNormalization.normal backwardNormalization.normal
      forwardScaled backwardScaled

namespace CoherentNormalizedScaledModelEquivalence

variable
    {B C : Type u₁}
    [Bicategory.{w₁, v₁} B] [Bicategory.{w₁, v₁} C]
    {E : BicategoricalModelEquivalence B C}
    {G : BicategoricalModelEquivalence C B}
    {HB : GlobalDuskinScaledHornFamily B}
    {HC : GlobalDuskinScaledHornFamily C}
    (K : CoherentNormalizedScaledModelEquivalence E G HB HC)

/-- Forget the construction layers and recover the v1.31 bidirectional package. -/
def toBidirectionalScaledDuskinModelEquivalence :
    BidirectionalScaledDuskinModelEquivalence HB HC where
  forwardModel := K.forwardNormalization.normal
  backwardModel := K.backwardNormalization.normal
  forwardScaled := K.forwardScaled
  backwardScaled := K.backwardScaled
  forwardFamily := K.forwardFamily
  backwardFamily := K.backwardFamily
  forward_backward_filler_equiv :=
    K.hornDescent.target_roundTrip_filler_equiv
  backward_forward_filler_equiv :=
    K.hornDescent.source_roundTrip_filler_equiv

/-- Coherent normalized model equivalence induces an actual horn-presentation equivalence. -/
def toScaledHornPresentationEquivalence :
    KUOS.DependentOriginationScaledHornPresentationInvariantV1_30.ScaledHornPresentationEquivalence
      HB HC :=
  KUOS.DependentOriginationModelEquivalenceScaledHornPresentationV1_31.
    BidirectionalScaledDuskinModelEquivalence.toScaledHornPresentationEquivalence
      (toBidirectionalScaledDuskinModelEquivalence K)

/-- Global scaled-Duskin fibrancy is invariant under the coherent normalized model equivalence. -/
theorem globalDuskinScaledFibrancy_iff :
    HasScaledHornFillers (duskinNerve B) (duskinScaling B) HB ↔
      HasScaledHornFillers (duskinNerve C) (duskinScaling C) HC :=
  KUOS.DependentOriginationModelEquivalenceScaledHornPresentationV1_31.
    BidirectionalScaledDuskinModelEquivalence.globalDuskinScaledFibrancy_iff
      (toBidirectionalScaledDuskinModelEquivalence K)

end CoherentNormalizedScaledModelEquivalence

/-!
The v1.32 boundary is now sharp:

```text
general Whitehead-style model maps E : B -> C and G : C -> B
  + chosen strictly-unitary normalizations
  + native strong coherence G_normal F_normal ==> id_B
  + native strong coherence F_normal G_normal ==> id_C
  + full scaled Duskin transport
  + admissible-family preservation
  + horn filler descent through coherent round trips
  -> BidirectionalScaledDuskinModelEquivalence
  -> ScaledHornPresentationEquivalence
  -> scaled fibrancy invariant.
```

The remaining theorem is no longer "find a quasi-inverse".  The bicategorical
quasi-inverse is now formalized.  What remains is to prove that the chosen
scaled-horn filler notion is invariant under the resulting coherent simplicial
round-trip comparison; that is exactly the `ScaledHornRoundTripDescent` field.
-/

end KUOS.DependentOriginationCoherentNormalizedScaledModelEquivalenceV1_32
