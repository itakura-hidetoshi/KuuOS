import KUOS.DependentOriginationHomotopyClassScaledHornInvariantV1_37

namespace KUOS.DependentOriginationHomotopyClassStrictificationV1_38

open CategoryTheory
open CategoryTheory.Category
open Simplicial
open KUOS.DependentOriginationGlobalDuskinScaledNerveV1_21
open KUOS.DependentOriginationGlobalDuskinScaledHornCoherenceV1_22
open KUOS.DependentOriginationStrictlyUnitaryDuskinModelTransportV1_27
open KUOS.DependentOriginationScaledDuskinHornTransportV1_29
open KUOS.DependentOriginationScaledHornHomotopyDescentV1_33
open KUOS.DependentOriginationHomotopyClassScaledHornInvariantV1_37

universe u u₁ u₂ v₁ v₂ w₁ w₂

/-!
# Homotopy-class horn strictification v1.38

Version 1.37 identified the genuinely presentation-independent horn carrier:
a scaled simplex whose horn boundary agrees with the prescribed horn map in
Mathlib's simplicial homotopy class.  This layer isolates exactly what extra
lifting principle is needed to return from that invariant carrier to literal
strict scaled horn filling.

There are two levels.

* `UniversalScaledHornHomotopyClassStrictification` strictifies every scaled
  horn problem in one scaled simplicial set.  It therefore implies the earlier
  one-step homotopy rectification property from v1.33.
* `ScaledHornFamilyHomotopyClassStrictification` only strictifies horn problems
  selected by one admissible family.  This is exactly the amount of
  strictification needed to identify strict fibrancy with homotopy-class
  fibrancy for that presentation.

No such strictification is constructed from a prism or from fibrancy itself.
Consequently the final strict-fibrancy invariance theorem below is conditional
on explicit local strictification data and contains no circular lifting
argument.
-/

/-! ## Universal and family-local strictification -/

/-- Every homotopy-class filler of every scaled horn problem can be replaced by
an honest strict scaled filler.  This is a strong target-level lifting
property, independent of any chosen horn family. -/
structure UniversalScaledHornHomotopyClassStrictification
    (X : SSet.{u})
    (sX : ScaledSimplicialSet X) : Prop where
  strictify :
    ∀ {n : Nat} {i : Fin (n + 1)}
      (P : ScaledHornExtensionProblem X sX n i),
      Nonempty (HomotopyClassScaledHornFiller P) →
      Nonempty (ScaledHornFiller P)

/-- The weaker and usually sufficient property: strictification is required
only for horn problems selected by one admissible family. -/
structure ScaledHornFamilyHomotopyClassStrictification
    (X : SSet.{u})
    (sX : ScaledSimplicialSet X)
    (F : ScaledHornFamily X sX) : Prop where
  strictify :
    ∀ {n : Nat} {i : Fin (n + 1)}
      (P : ScaledHornExtensionProblem X sX n i),
      F.admissible P →
      Nonempty (HomotopyClassScaledHornFiller P) →
      Nonempty (ScaledHornFiller P)

namespace UniversalScaledHornHomotopyClassStrictification

/-- Universal strictification restricts to every selected horn family. -/
def toFamily
    {X : SSet.{u}}
    {sX : ScaledSimplicialSet X}
    (R : UniversalScaledHornHomotopyClassStrictification X sX)
    (F : ScaledHornFamily X sX) :
    ScaledHornFamilyHomotopyClassStrictification X sX F where
  strictify := by
    intro n i P hP h
    exact R.strictify P h

/-- Universal homotopy-class strictification is stronger than the one-step
homotopy rectification property isolated in v1.33. -/
noncomputable def toHomotopyRectification
    {X : SSet.{u}}
    {sX : ScaledSimplicialSet X}
    (R : UniversalScaledHornHomotopyClassStrictification X sX) :
    ScaledHornHomotopyRectification X sX where
  rectify := by
    intro n i P h
    rcases h with ⟨Q⟩
    exact R.strictify P
      ⟨homotopyClassScaledHornFillerOfHomotopy Q⟩

end UniversalScaledHornHomotopyClassStrictification

/-! ## Strict and homotopy-class fibrancy coincide under local strictification -/

/-- A strict filler property always descends to the homotopy-class filler
property, phrased without a typeclass argument so it composes cleanly below. -/
noncomputable def homotopyClassFibrancyOfStrict
    {X : SSet.{u}}
    {sX : ScaledSimplicialSet X}
    {F : ScaledHornFamily X sX}
    (H : HasScaledHornFillers X sX F) :
    HasHomotopyClassScaledHornFillers X sX F where
  fill := by
    intro n i P hP h0 hi
    rcases H.fill P hP h0 hi with ⟨Q⟩
    exact ⟨homotopyClassScaledHornFillerOfStrict Q⟩

/-- Family-local strictification upgrades homotopy-class fibrancy back to
literal strict scaled-horn fibrancy. -/
def strictFibrancyOfHomotopyClass
    {X : SSet.{u}}
    {sX : ScaledSimplicialSet X}
    {F : ScaledHornFamily X sX}
    (R : ScaledHornFamilyHomotopyClassStrictification X sX F)
    (H : HasHomotopyClassScaledHornFillers X sX F) :
    HasScaledHornFillers X sX F where
  fill := by
    intro n i P hP h0 hi
    exact R.strictify P hP (H.fill P hP h0 hi)

/-- The strictification property identifies the two fibrancy predicates for one
chosen presentation. -/
theorem strictFibrancy_iff_homotopyClassFibrancy
    {X : SSet.{u}}
    {sX : ScaledSimplicialSet X}
    {F : ScaledHornFamily X sX}
    (R : ScaledHornFamilyHomotopyClassStrictification X sX F) :
    HasScaledHornFillers X sX F ↔
      HasHomotopyClassScaledHornFillers X sX F := by
  constructor
  · exact homotopyClassFibrancyOfStrict
  · exact strictFibrancyOfHomotopyClass R

/-! ## Presentation-independent strict fibrancy -/

/--
A coherent normalized scaled model equivalence together with the local lifting
principle that identifies homotopy-class and strict horn filling in each
presentation.

The model-comparison content itself is exactly the v1.37 package.  The two new
fields are target-local strictification statements; they do not mention the
opposite presentation and do not duplicate the canonical prism data.
-/
structure CoherentNormalizedScaledStrictifiableModelEquivalence
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (E : BicategoricalModelEquivalence B C)
    (G : BicategoricalModelEquivalence C B)
    (HB : GlobalDuskinScaledHornFamily B)
    (HC : GlobalDuskinScaledHornFamily C) where
  homotopyClassModel :
    CoherentNormalizedScaledHomotopyClassModelEquivalence E G HB HC
  sourceStrictification :
    ScaledHornFamilyHomotopyClassStrictification
      (duskinNerve B) (duskinScaling B) HB
  targetStrictification :
    ScaledHornFamilyHomotopyClassStrictification
      (duskinNerve C) (duskinScaling C) HC

namespace CoherentNormalizedScaledStrictifiableModelEquivalence

variable
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    {E : BicategoricalModelEquivalence B C}
    {G : BicategoricalModelEquivalence C B}
    {HB : GlobalDuskinScaledHornFamily B}
    {HC : GlobalDuskinScaledHornFamily C}
    (K : CoherentNormalizedScaledStrictifiableModelEquivalence E G HB HC)

/--
Strict global scaled-Duskin fibrancy is presentation-independent once each
presentation admits family-local homotopy-class strictification.

The proof factors through the invariant v1.37 carrier rather than transporting
strict fillers directly:

`strict_B <-> class_B <-> class_C <-> strict_C`.
-/
theorem globalDuskinStrictFibrancy_iff :
    HasScaledHornFillers (duskinNerve B) (duskinScaling B) HB ↔
      HasScaledHornFillers (duskinNerve C) (duskinScaling C) HC := by
  rw [strictFibrancy_iff_homotopyClassFibrancy K.sourceStrictification,
    strictFibrancy_iff_homotopyClassFibrancy K.targetStrictification]
  exact K.homotopyClassModel.globalDuskinHomotopyClassFibrancy_iff

end CoherentNormalizedScaledStrictifiableModelEquivalence

/-!
The resulting implication hierarchy is now explicit:

```text
coherent normalized scaled model equivalence
  -> presentation-independent homotopy-class horn fibrancy          -- v1.37

family-local homotopy-class strictification on both presentations
  + presentation-independent homotopy-class horn fibrancy
  -> presentation-independent strict scaled horn fibrancy           -- v1.38

universal homotopy-class strictification
  -> family-local strictification for every family
  -> one-step homotopy rectification of v1.33
```

Still not claimed: that an arbitrary scaled Duskin nerve automatically has the
strictification property.  Establishing that for a specific standard
scaled-anodyne generator family is the next independent lifting theorem.
-/

end KUOS.DependentOriginationHomotopyClassStrictificationV1_38
