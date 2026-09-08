import Mathlib.CategoryTheory.Bicategory.FunctorBicategory.Pseudo
import Mathlib.CategoryTheory.Bicategory.InducedBicategory
import KUOS.DependentOriginationHigherStackDescentV2_8

namespace KUOS.DependentOriginationHigherStackCarrierV2_9

open CategoryTheory
open CategoryTheory.Limits
open Opposite
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationHigherStackDescentV2_8

open scoped CategoryTheory.Pseudofunctor.StrongTrans

universe u v uH vH

/-!
# The Cat-valued W + J + H carrier as a full sub-bicategory v2.9

The v2.8 layer proves that a Cat-valued pseudofunctor on the presentation-independent
localized opposite site satisfies the KuuOS higher descent condition exactly when it is a
Mathlib stack for the generated Grothendieck topology (equivalently, under the standard
precoverage closure hypotheses, when all declared root-to-descent-data functors are category
equivalences).

This file packages those stack objects into their natural higher carrier.

Mathlib already provides two pieces of native bicategorical infrastructure:

* `Pseudofunctor B C` carries a bicategory structure whose 1-morphisms are strong natural
  transformations and whose 2-morphisms are modifications;
* `Bicategory.InducedBicategory` constructs the full sub-bicategory on any chosen collection
  of objects.

Accordingly we define

```text
DO₂(C,W,A)
```

as the full sub-bicategory of Cat-valued pseudofunctors on the localized site whose objects
satisfy `F.IsStack A.generatedTopology`.

This is the correct higher carrier after presentation localization and stack descent.  It is
not yet the raw `W`-inverting classification theorem.  In particular, the ordinary
1-categorical localization theorem used in v2.7 does not by itself classify weak Cat-valued
pseudofunctors that send `W` to equivalences of categories.  That requires a separate
bicategorical localization / coherence theorem and is deliberately not asserted here.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- Objects of the higher dependent-origination carrier: Cat-valued contextual systems on the
localized site satisfying genuine stack descent for the generated KuuOS topology. -/
def HigherStackObject
    (A : RefinementAtlas (LocalizedContext W)) :=
  { F : HigherLocalizedDescentSystem (W := W) (uH := uH) (vH := vH) //
      IsHigherGrothendieckDescentComplete W A F }

/-- Forget the stack witness and retain the underlying Cat-valued pseudofunctor. -/
abbrev higherStackObjectVal
    (A : RefinementAtlas (LocalizedContext W)) :
    HigherStackObject (W := W) (uH := uH) (vH := vH) A →
      HigherLocalizedDescentSystem (W := W) (uH := uH) (vH := vH) :=
  Subtype.val

/-- The Cat-valued `W + J + H` carrier.

The `W`-axis is built into the domain through `LocalizedContext W`; the `J + H` condition is
Mathlib stackness.  The induced bicategory makes the carrier full on strong transformations and
modifications, so no ad hoc higher morphism structure is introduced. -/
abbrev DependentOriginationCompletion2
    (A : RefinementAtlas (LocalizedContext W)) :=
  CategoryTheory.Bicategory.InducedBicategory
    (HigherLocalizedDescentSystem (W := W) (uH := uH) (vH := vH))
    (higherStackObjectVal (W := W) (uH := uH) (vH := vH) A)

/-- Every object of `DO₂` carries the native Mathlib stack instance represented by its subtype
witness. -/
instance completion2ObjectIsStack
    (A : RefinementAtlas (LocalizedContext W))
    (X : HigherStackObject (W := W) (uH := uH) (vH := vH) A) :
    (X.1).IsStack A.generatedTopology := by
  exact X.2

/-- The canonical strict pseudofunctor from the full stack sub-bicategory back to the ambient
bicategory of all Cat-valued contextual pseudofunctors. -/
def completion2Forget
    (A : RefinementAtlas (LocalizedContext W)) :
    StrictPseudofunctor
      (DependentOriginationCompletion2 (W := W) (uH := uH) (vH := vH) A)
      (HigherLocalizedDescentSystem (W := W) (uH := uH) (vH := vH)) :=
  CategoryTheory.Bicategory.InducedBicategory.forget

/-- `DO₂` is full on 1-morphisms: every ambient strong natural transformation between two stack
objects defines a 1-morphism in the carrier. -/
def completion2MkHom
    (A : RefinementAtlas (LocalizedContext W))
    {X Y : DependentOriginationCompletion2 (W := W) (uH := uH) (vH := vH) A}
    (η :
      higherStackObjectVal (W := W) (uH := uH) (vH := vH) A X ⟶
        higherStackObjectVal (W := W) (uH := uH) (vH := vH) A Y) :
    X ⟶ Y :=
  CategoryTheory.Bicategory.InducedBicategory.mkHom η

/-- Global stack descent for an object of `DO₂` gives a category equivalence from every declared
KuuOS root to its category of descent data. -/
theorem completion2Object_declaredDescentEquivalences
    (A : RefinementAtlas (LocalizedContext W))
    (X : HigherStackObject (W := W) (uH := uH) (vH := vH) A)
    (S : HigherLocalizedSite W) :
    (X.1.toDescentData
      (fun i : A.Index (unop S) => (A.toChart (unop S) i).op)).IsEquivalence := by
  exact declaredCover_toDescentData_isEquivalence W A X.1 X.2 S

section LocalToGlobal

variable (A : RefinementAtlas (LocalizedContext W))
variable [HasPullbacks (HigherLocalizedSite W)]
variable [A.precoverage.HasIsos]
variable [A.precoverage.IsStableUnderBaseChange]
variable [A.precoverage.IsStableUnderComposition]

/-- Under the standard precoverage closure hypotheses, a Cat-valued contextual pseudofunctor
whose declared root-to-descent-data functors are all equivalences canonically determines an
object of `DO₂`. -/
def completion2ObjectOfDeclaredDescentEquivalences
    (F : HigherLocalizedDescentSystem (W := W) (uH := uH) (vH := vH))
    (hF : ∀ S : HigherLocalizedSite W,
      (F.toDescentData
        (fun i : A.Index (unop S) => (A.toChart (unop S) i).op)).IsEquivalence) :
    DependentOriginationCompletion2 (W := W) (uH := uH) (vH := vH) A :=
  ⟨F,
    (isHigherGrothendieckDescentComplete_iff_declaredDescentEquivalences W A F).2 hF⟩

end LocalToGlobal

/-!
Thus the first fully native higher carrier in the universal dependent-origination program is

```text
DO₂(C,W,A)
  = full sub-bicategory of
      [LocallyDiscrete ((((C[W⁻¹])ᵒᵖ)ᵒᵖ), Cat)]_pseudo
    on F with F.IsStack(J_A).
```

Its 1-cells are strong natural transformations and its 2-cells are modifications inherited from
Mathlib.  The remaining universal step is not to invent more cells, but to prove an appropriate
bicategorical localization/classification theorem relating raw `W`-admissible higher contextual
systems to this localized stack carrier, and then to compare that carrier with the existing KuuOS
bicategorical/globular/scaled-simplicial coherence spine.
-/

end KUOS.DependentOriginationHigherStackCarrierV2_9
