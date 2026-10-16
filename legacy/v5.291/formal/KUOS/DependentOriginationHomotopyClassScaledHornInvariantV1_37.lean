import KUOS.DependentOriginationStrongTransformationCylinderUncurryingV1_36

namespace KUOS.DependentOriginationHomotopyClassScaledHornInvariantV1_37

open CategoryTheory
open CategoryTheory.Category
open Simplicial
open KUOS.DependentOriginationGlobalDuskinScaledNerveV1_21
open KUOS.DependentOriginationGlobalDuskinScaledHornCoherenceV1_22
open KUOS.DependentOriginationStrictlyUnitaryDuskinModelTransportV1_27
open KUOS.DependentOriginationNormalizationChoiceInvariantV1_28
open KUOS.DependentOriginationScaledDuskinHornTransportV1_29
open KUOS.DependentOriginationCoherentNormalizedScaledModelEquivalenceV1_32
open KUOS.DependentOriginationScaledHornHomotopyDescentV1_33
open KUOS.DependentOriginationGlobalDuskinPrismHomotopyV1_34
open KUOS.DependentOriginationStrongTransformationCylinderUncurryingV1_36

universe u u₁ u₂ v₁ v₂ w₁ w₂

/-!
# Presentation-independent homotopy-class scaled horn filling v1.37

The strict horn-filler predicate of v1.22 is presentation-sensitive unless a
separate rectification theorem is supplied.  The previous layers constructed
canonical global Duskin prism homotopies from native bicategorical strong
quasi-inverses, but a single simplicial homotopy need not compose with another
single simplicial homotopy to a new single prism.

The correct transitive carrier is therefore Mathlib's relative
`HomotopyClass`.  Equality of homotopy classes composes by ordinary equality,
so a boundary comparison

```text
actual boundary ~ round-trip boundary ~ prescribed boundary
```

can be used without any Kan/fibrancy or strictification assumption.

This file proves that the resulting inner-horn filling property modulo
simplicial homotopy class is invariant under coherent normalized scaled
bicategorical model equivalence.  The global prisms needed for the proof are
not additional data: v1.36 constructs them canonically from the native strong
quasi-inverse.
-/

/-! ## Plain simplicial homotopy classes -/

/-- Homotopy classes of ordinary simplicial maps, implemented as relative
homotopy classes with bottom source and target subcomplexes. -/
abbrev SSetHomotopyClass (X Y : SSet.{u}) :=
  SSet.RelativeMorphism.HomotopyClass
    (⊥ : X.Subcomplex) (⊥ : Y.Subcomplex)
    (SSet.Subcomplex.isInitialBot.to _)

/-- The homotopy class represented by a simplicial map. -/
def homotopyClassOfMap
    {X Y : SSet.{u}} (f : X ⟶ Y) :
    SSetHomotopyClass X Y :=
  (SSet.RelativeMorphism.botEquiv.symm f).homotopyClass

/-- A native simplicial homotopy identifies the represented homotopy classes. -/
theorem homotopyClassOfMap_eq_of_homotopy
    {X Y : SSet.{u}} {f g : X ⟶ Y}
    (H : SSet.Homotopy f g) :
    homotopyClassOfMap f = homotopyClassOfMap g :=
  SSet.RelativeMorphism.Homotopy.eq H

/-- Postcomposition is well-defined on ordinary simplicial homotopy classes. -/
noncomputable def postcompSSetHomotopyClass
    {X Y Z : SSet.{u}} (k : Y ⟶ Z) :
    SSetHomotopyClass X Y → SSetHomotopyClass X Z :=
  fun h =>
    h.postcomp (SSet.RelativeMorphism.botEquiv.symm k) (by cat_disch)

@[simp] theorem postcompSSetHomotopyClass_rep
    {X Y Z : SSet.{u}} (f : X ⟶ Y) (k : Y ⟶ Z) :
    postcompSSetHomotopyClass k (homotopyClassOfMap f) =
      homotopyClassOfMap (f ≫ k) := by
  change
    ((SSet.RelativeMorphism.botEquiv.symm f).comp
      (SSet.RelativeMorphism.botEquiv.symm k) (by cat_disch)).homotopyClass =
      (SSet.RelativeMorphism.botEquiv.symm (f ≫ k)).homotopyClass
  congr 1
  ext
  rfl

/-! ## Scaled horn fillers modulo boundary homotopy class -/

/-- A scaled simplex whose boundary lies in the same simplicial homotopy class
as the prescribed horn map. -/
structure HomotopyClassScaledHornFiller
    {X : SSet.{u}}
    {sX : ScaledSimplicialSet X}
    {n : Nat} {i : Fin (n + 1)}
    (P : ScaledHornExtensionProblem X sX n i) where
  simplexMap : Δ[n] ⟶ X
  boundary_class_eq :
    homotopyClassOfMap (Λ[n, i].ι ≫ simplexMap) =
      homotopyClassOfMap P.hornMap
  simplexMap_scaled : IsScaledMap P.simplexScaling sX simplexMap

/-- A one-step homotopy filler canonically determines a homotopy-class filler. -/
noncomputable def homotopyClassScaledHornFillerOfHomotopy
    {X : SSet.{u}}
    {sX : ScaledSimplicialSet X}
    {n : Nat} {i : Fin (n + 1)}
    {P : ScaledHornExtensionProblem X sX n i}
    (Q : HomotopyScaledHornFiller P) :
    HomotopyClassScaledHornFiller P where
  simplexMap := Q.simplexMap
  boundary_class_eq :=
    homotopyClassOfMap_eq_of_homotopy Q.boundaryHomotopy
  simplexMap_scaled := Q.simplexMap_scaled

/-- In particular, every strict scaled horn filler determines a homotopy-class
filler without any rectification hypothesis. -/
noncomputable def homotopyClassScaledHornFillerOfStrict
    {X : SSet.{u}}
    {sX : ScaledSimplicialSet X}
    {n : Nat} {i : Fin (n + 1)}
    {P : ScaledHornExtensionProblem X sX n i}
    (Q : ScaledHornFiller P) :
    HomotopyClassScaledHornFiller P where
  simplexMap := Q.simplexMap
  boundary_class_eq := by
    rw [Q.extends_horn]
  simplexMap_scaled := Q.simplexMap_scaled

/-- Homotopy-class fillers transport forward along every scaled simplicial map. -/
noncomputable def mapHomotopyClassScaledHornFiller
    {X Y : SSet.{u}}
    {sX : ScaledSimplicialSet X}
    {sY : ScaledSimplicialSet Y}
    {f : X ⟶ Y}
    (hf : IsScaledMap sX sY f)
    {n : Nat} {i : Fin (n + 1)}
    {P : ScaledHornExtensionProblem X sX n i}
    (Q : HomotopyClassScaledHornFiller P) :
    HomotopyClassScaledHornFiller (mapScaledHornProblem hf P) where
  simplexMap := Q.simplexMap ≫ f
  boundary_class_eq := by
    have h := congrArg (postcompSSetHomotopyClass f) Q.boundary_class_eq
    simpa [mapScaledHornProblem, Category.assoc] using h
  simplexMap_scaled := Q.simplexMap_scaled.comp hf

/-- A scaled simplicial set fills every selected inner horn up to boundary
homotopy class.  This is deliberately weaker than `HasScaledHornFillers`. -/
class HasHomotopyClassScaledHornFillers
    (X : SSet.{u})
    (sX : ScaledSimplicialSet X)
    (F : ScaledHornFamily X sX) : Prop where
  fill :
    ∀ {n : Nat} {i : Fin (n + 1)}
      (P : ScaledHornExtensionProblem X sX n i),
      F.admissible P →
      0 < i → i < Fin.last n →
      Nonempty (HomotopyClassScaledHornFiller P)

/-- Strict scaled horn fibrancy implies homotopy-class scaled horn fibrancy. -/
noncomputable def hasHomotopyClassScaledHornFillersOfStrict
    {X : SSet.{u}}
    {sX : ScaledSimplicialSet X}
    {F : ScaledHornFamily X sX}
    [H : HasScaledHornFillers X sX F] :
    HasHomotopyClassScaledHornFillers X sX F where
  fill := by
    intro n i P hP h0 hi
    rcases H.fill P hP h0 hi with ⟨Q⟩
    exact ⟨homotopyClassScaledHornFillerOfStrict Q⟩

/-! ## Round-trip homotopy classes need no strictification -/

/-- The canonical global prism produced theorem-level by the v1.36 strong
transformation cylinder construction. -/
noncomputable def canonicalGlobalDuskinRoundTripPrism
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    {F : StrictlyUnitaryBicategoricalModelEquivalence B C}
    {G : StrictlyUnitaryBicategoricalModelEquivalence C B}
    (K : NormalizedCoherentQuasiInverse F G) :
    GlobalDuskinRoundTripPrismRealization K :=
  KUOS.DependentOriginationStrongTransformationCylinderUncurryingV1_36.
    globalDuskinRoundTripPrismRealization K

/-- A source round-trip homotopy-class filler descends to the original source
horn by transitivity of homotopy-class equality. -/
noncomputable def sourceHomotopyClassFillerOfRoundTrip
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    {F : StrictlyUnitaryBicategoricalModelEquivalence B C}
    {G : StrictlyUnitaryBicategoricalModelEquivalence C B}
    {K : NormalizedCoherentQuasiInverse F G}
    (HF : FullScaledDuskinMapCertificate F)
    (HG : FullScaledDuskinMapCertificate G)
    {n : Nat} {i : Fin (n + 1)}
    {P : ScaledHornExtensionProblem
      (duskinNerve B) (duskinScaling B) n i}
    (Q : HomotopyClassScaledHornFiller
      (transportGlobalDuskinHornProblem HG
        (transportGlobalDuskinHornProblem HF P))) :
    HomotopyClassScaledHornFiller P where
  simplexMap := Q.simplexMap
  boundary_class_eq := by
    refine Q.boundary_class_eq.trans ?_
    exact homotopyClassOfMap_eq_of_homotopy (by
      simpa [transportGlobalDuskinHornProblem, mapScaledHornProblem,
        Category.assoc] using
        (canonicalGlobalDuskinRoundTripPrism K).sourceHornHomotopy P)
  simplexMap_scaled := Q.simplexMap_scaled

/-- Target-side round-trip descent modulo boundary homotopy class. -/
noncomputable def targetHomotopyClassFillerOfRoundTrip
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    {F : StrictlyUnitaryBicategoricalModelEquivalence B C}
    {G : StrictlyUnitaryBicategoricalModelEquivalence C B}
    {K : NormalizedCoherentQuasiInverse F G}
    (HF : FullScaledDuskinMapCertificate F)
    (HG : FullScaledDuskinMapCertificate G)
    {n : Nat} {i : Fin (n + 1)}
    {Q : ScaledHornExtensionProblem
      (duskinNerve C) (duskinScaling C) n i}
    (R : HomotopyClassScaledHornFiller
      (transportGlobalDuskinHornProblem HF
        (transportGlobalDuskinHornProblem HG Q))) :
    HomotopyClassScaledHornFiller Q where
  simplexMap := R.simplexMap
  boundary_class_eq := by
    refine R.boundary_class_eq.trans ?_
    exact homotopyClassOfMap_eq_of_homotopy (by
      simpa [transportGlobalDuskinHornProblem, mapScaledHornProblem,
        Category.assoc] using
        (canonicalGlobalDuskinRoundTripPrism K).targetHornHomotopy Q)
  simplexMap_scaled := R.simplexMap_scaled

/-! ## Presentation-independent model-equivalence package -/

/--
The data needed for homotopy-class horn invariance.

Unlike the strict-fibrancy packages of v1.32--v1.34, no horn rectification and
no separately supplied global prism are fields.  The prism follows canonically
from `quasiInverse` by v1.36, and class-level descent uses equality transitivity.
-/
structure CoherentNormalizedScaledHomotopyClassModelEquivalence
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
  forwardFamily : ScaledHornFamilyMap forwardScaled.map_scaled HB HC
  backwardFamily : ScaledHornFamilyMap backwardScaled.map_scaled HC HB

namespace CoherentNormalizedScaledHomotopyClassModelEquivalence

variable
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    {E : BicategoricalModelEquivalence B C}
    {G : BicategoricalModelEquivalence C B}
    {HB : GlobalDuskinScaledHornFamily B}
    {HC : GlobalDuskinScaledHornFamily C}
    (K : CoherentNormalizedScaledHomotopyClassModelEquivalence E G HB HC)

/-- Homotopy-class horn filling is transported from the source model to the
target model by backward transport, source filling, forward transport, and
canonical target round-trip class descent. -/
noncomputable def forwardHasHomotopyClassScaledHornFillers
    (H : HasHomotopyClassScaledHornFillers
      (duskinNerve B) (duskinScaling B) HB) :
    HasHomotopyClassScaledHornFillers
      (duskinNerve C) (duskinScaling C) HC where
  fill := by
    intro n i Q hQ h0 hi
    have hBack :
        HB.admissible
          (transportGlobalDuskinHornProblem K.backwardScaled Q) :=
      K.backwardFamily.admissible_preserved Q hQ
    rcases H.fill
      (transportGlobalDuskinHornProblem K.backwardScaled Q)
      hBack h0 hi with ⟨R⟩
    let R' := mapHomotopyClassScaledHornFiller
      K.forwardScaled.map_scaled R
    exact ⟨targetHomotopyClassFillerOfRoundTrip
      K.forwardScaled K.backwardScaled R'⟩

/-- Symmetric transport from the target model back to the source model. -/
noncomputable def backwardHasHomotopyClassScaledHornFillers
    (H : HasHomotopyClassScaledHornFillers
      (duskinNerve C) (duskinScaling C) HC) :
    HasHomotopyClassScaledHornFillers
      (duskinNerve B) (duskinScaling B) HB where
  fill := by
    intro n i P hP h0 hi
    have hForward :
        HC.admissible
          (transportGlobalDuskinHornProblem K.forwardScaled P) :=
      K.forwardFamily.admissible_preserved P hP
    rcases H.fill
      (transportGlobalDuskinHornProblem K.forwardScaled P)
      hForward h0 hi with ⟨Q⟩
    let Q' := mapHomotopyClassScaledHornFiller
      K.backwardScaled.map_scaled Q
    exact ⟨sourceHomotopyClassFillerOfRoundTrip
      K.forwardScaled K.backwardScaled Q'⟩

/--
Global scaled Duskin inner-horn filling modulo boundary homotopy class is a
presentation-independent invariant of the coherent normalized scaled
bicategorical model.
-/
theorem globalDuskinHomotopyClassFibrancy_iff :
    HasHomotopyClassScaledHornFillers
        (duskinNerve B) (duskinScaling B) HB ↔
      HasHomotopyClassScaledHornFillers
        (duskinNerve C) (duskinScaling C) HC := by
  constructor
  · exact K.forwardHasHomotopyClassScaledHornFillers
  · exact K.backwardHasHomotopyClassScaledHornFillers

end CoherentNormalizedScaledHomotopyClassModelEquivalence

/-!
The resulting hierarchy is now precise:

```text
strict scaled horn filler
  -> one-step homotopy scaled horn filler
  -> homotopy-class scaled horn filler

coherent normalized scaled bicategorical model equivalence
  -> canonical strong-transformation cylinders                 -- v1.36
  -> canonical global Duskin round-trip prisms                  -- v1.36
  -> round-trip equality of boundary homotopy classes           -- v1.37
  -> presentation-independent homotopy-class horn fibrancy      -- v1.37
```

No converse from homotopy-class filler to strict filler is asserted.  Such a
converse is a separate strictification/lifting theorem and cannot be obtained
from the prism alone.
-/

end KUOS.DependentOriginationHomotopyClassScaledHornInvariantV1_37
