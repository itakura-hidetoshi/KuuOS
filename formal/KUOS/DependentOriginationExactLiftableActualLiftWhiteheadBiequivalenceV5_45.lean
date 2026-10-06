import KUOS.DependentOriginationExactLiftableActualLiftObjectCoverageV5_44
import KUOS.DependentOriginationExactUniversalLabelledBiequivalenceV4_89
import Mathlib

namespace KUOS.DependentOriginationExactLiftableActualLiftWhiteheadBiequivalenceV5_45

open CategoryTheory
open KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
open KUOS.DependentOriginationLocalizedSheafUniversalityV2_6
open KUOS.DependentOriginationExactUniversalLabelledBiequivalenceV4_89
open KUOS.DependentOriginationExactUniversalClassificationInterfaceV5_17
open KUOS.DependentOriginationExactClassificationMorphismInterfaceV5_21
open KUOS.DependentOriginationExactLiftableActualLiftOneCellV5_40
open KUOS.DependentOriginationExactLiftableClassificationBicategoryV5_41
open KUOS.DependentOriginationExactLiftableActualLiftStrictPseudofunctorV5_42
open KUOS.DependentOriginationExactLiftableActualLiftLocalHomEquivalenceV5_43
open KUOS.DependentOriginationExactLiftableActualLiftObjectCoverageV5_44

set_option autoImplicit false

noncomputable section

/-!
# Actual-lift Whitehead biequivalence v5.45

v5.43 supplies equivalences for the explicit v5.41 actual-lift hom functors.
v5.44 supplies object essential surjectivity for the native v5.42 object map.
The remaining assembly obligation is to identify those explicit hom functors
with the hom functors of the global strict pseudofunctor.

We make the parent projections to Pseudofunctor and PrelaxFunctor explicit,
and prove agreement by small functor extensionality, as in v5.27.  This avoids
asking elaboration to recover the inherited mapFunctor API from the strict
wrapper, or reducing a whole equivalence structure at once.

The resulting four-field WhiteheadBiequivalenceData retains:

* the actual v5.42 forward pseudofunctor;
* the v5.43 local category equivalences;
* equality of their forward functors with the native global hom functors;
* v5.44 object essential surjectivity, with external labels still preserved.

No global quasi-inverse, pseudonatural unit/counit, or triangle modification
is asserted here.  Arbitrary raw StrongTrans are not declared liftable.
-/

universe u v uH vH uW uP

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)
variable (A : RefinementAtlas.{u, max u v, uH} (LocalizedContext W))
variable {WorldLabel : Type uW} {PresentationLabel : Type uP}

/-! ## Close the explicit-local / native-global hom-functor boundary -/

/-- The explicit v5.41 hom functor equals the native hom functor after the
strict pseudofunctor's parent projections are made explicit. -/
theorem actualLiftHomFunctor_eq_nativeMapFunctor
    (X Y : ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    actualLiftHomFunctor (W := W) A X Y =
      (exactLiftableActualLiftStrictPseudofunctor
        (W := W) A).toPseudofunctor.toPrelaxFunctor.mapFunctor X Y := by
  apply CategoryTheory.Functor.hext
  · intro f
    rfl
  · intro f g eta
    exact heq_of_eq rfl

/-- Exact agreement of the local equivalence's forward functor with the
hom functor of the global v5.42 pseudofunctor. -/
theorem actualLiftHomEquivalence_forward
    (X Y : ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    (actualLiftHomEquivalence (W := W) A X Y).functor =
      (exactLiftableActualLiftStrictPseudofunctor
        (W := W) A).toPseudofunctor.toPrelaxFunctor.mapFunctor X Y :=
  (actualLiftHomEquivalence_functor (W := W) A X Y).trans
    (actualLiftHomFunctor_eq_nativeMapFunctor (W := W) A X Y)

/-- The native global hom functor is an equivalence.  Transfer the already
proved local instance through the explicit equality instead of relying on
large definitional reduction during typeclass synthesis. -/
instance exactLiftableActualLiftNativeMapFunctor_isEquivalence
    (X Y : ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    ((exactLiftableActualLiftStrictPseudofunctor
      (W := W) A).toPseudofunctor.toPrelaxFunctor.mapFunctor X Y).IsEquivalence := by
  rw [← actualLiftHomFunctor_eq_nativeMapFunctor (W := W) A X Y]
  exact actualLiftHomFunctor_isEquivalence (W := W) A X Y

/-! ## Assemble the global Whitehead certificate -/

/-- Label-preserving Whitehead biequivalence from the actual-lift exact-liftable
classification bicategory to the exact-universal classification bicategory. -/
def exactLiftableActualLiftWhiteheadBiequivalence :
    WhiteheadBiequivalenceData
      (ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel)
      (ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel) where
  forward :=
    (exactLiftableActualLiftStrictPseudofunctor (W := W) A).toPseudofunctor
  homEquiv X Y :=
    actualLiftHomEquivalence (W := W) A X Y
  homEquiv_functor X Y :=
    actualLiftHomEquivalence_forward (W := W) A X Y
  object_essentially_surjective Y :=
    exactLiftableActualLiftStrictPseudofunctor_object_essentially_surjective
      (W := W) A Y

/-! ## Exact projections and label-preserving coverage -/

@[simp] theorem exactLiftableActualLiftWhiteheadBiequivalence_obj_label
    (X : ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    ((exactLiftableActualLiftWhiteheadBiequivalence
      (W := W) A).forward.obj X).label = X.label :=
  rfl

@[simp] theorem exactLiftableActualLiftWhiteheadBiequivalence_homEquiv
    (X Y : ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    (exactLiftableActualLiftWhiteheadBiequivalence
      (W := W) A).homEquiv X Y = actualLiftHomEquivalence (W := W) A X Y :=
  rfl

/-- The covering source for every target object can still be taken with its
external label literally equal to that target's label. -/
theorem exactLiftableActualLiftWhiteheadBiequivalence_sameLabel_coverage
    (Y : ExactUniversalClassificationObject.{u, v, uH, vH, uW, uP}
      (W := W) A WorldLabel PresentationLabel) :
    ∃ X : ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
        (W := W) A WorldLabel PresentationLabel,
      X.label = Y.label ∧
        Nonempty (Bicategory.Equivalence
          (B := ExactUniversalClassificationObject (W := W) A
            WorldLabel PresentationLabel)
          ((exactLiftableActualLiftWhiteheadBiequivalence
            (W := W) A).forward.obj X) Y) :=
  exists_exactLiftableObject_sameLabel_equivalent (W := W) A Y

/-! ## Native-interface regression checks -/

section Regression

variable
  (X Y : ExactLiftableClassificationObject.{u, v, uH, vH, uW, uP}
    (W := W) A WorldLabel PresentationLabel)

-- The ordinary Pseudofunctor API, not a second ad hoc local functor.
example :
    ((exactLiftableActualLiftStrictPseudofunctor
      (W := W) A).toPseudofunctor.mapFunctor X Y).IsEquivalence :=
  exactLiftableActualLiftNativeMapFunctor_isEquivalence (W := W) A X Y

-- The certificate's local forward map is its own global forward hom functor.
example :
    ((exactLiftableActualLiftWhiteheadBiequivalence
      (W := W) A).homEquiv X Y).functor =
      (exactLiftableActualLiftWhiteheadBiequivalence
        (W := W) A).forward.toPrelaxFunctor.mapFunctor X Y :=
  (exactLiftableActualLiftWhiteheadBiequivalence
    (W := W) A).homEquiv_functor X Y

-- The native forward 1-cell is the stored lift, retaining the prescribed raw map.
example (f : ExactLiftableClassificationActualOneCell (W := W) A X Y) :
    ((exactLiftableActualLiftWhiteheadBiequivalence
      (W := W) A).forward.map f).map.raw = f.raw.map :=
  f.raw_eq

end Regression

/-!
## Boundary after v5.45

Closed: the explicit v5.41 local hom functors agree with the native v5.42
pseudofunctor hom functors; their local equivalences and v5.44 object coverage
are now one WhiteheadBiequivalenceData certificate.

The certificate concerns the v5.40 actual-lift-carrying 1-cells.  It does not
replace these by arbitrary raw morphisms, erase external labels, or identify
independently chosen presentations by equality.

The next higher-coherence problem is to construct an explicit global
quasi-inverse with pseudonatural roundtrip unit/counit.  Objectwise adjoint
equivalences alone are not claimed to constitute those global data.
-/

#print axioms actualLiftHomFunctor_eq_nativeMapFunctor
#print axioms actualLiftHomEquivalence_forward
#print axioms exactLiftableActualLiftNativeMapFunctor_isEquivalence
#print axioms exactLiftableActualLiftWhiteheadBiequivalence
#print axioms exactLiftableActualLiftWhiteheadBiequivalence_sameLabel_coverage

end

end KUOS.DependentOriginationExactLiftableActualLiftWhiteheadBiequivalenceV5_45
