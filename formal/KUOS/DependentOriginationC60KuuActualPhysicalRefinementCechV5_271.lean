import KUOS.DependentOriginationC60KuuActualPhysicalFiniteCechHistoriesV5_270

namespace KUOS.DependentOriginationC60KuuActualPhysicalRefinementCechV5_271

open CategoryTheory
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationC60NativeExchangeCongruenceQuotientV5_231
open KUOS.DependentOriginationC60NativeQuotientHorizontalTensorV5_234
open KUOS.DependentOriginationC60QuotientTensorNaturalityV5_236
open KUOS.DependentOriginationC60KuuActualIncidenceOverlapRefinementV5_260
open KUOS.DependentOriginationC60KuuTwoActualFaceInterchangeV5_265
open KUOS.DependentOriginationC60KuuTwoFacePhysicalOverlapCompatibilityV5_266
open KUOS.DependentOriginationC60KuuTwoFaceObservedObjectCechV5_267
open KUOS.DependentOriginationC60KuuActualPhysicalFiniteCechHistoriesV5_270

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.271 / F111 second stage — finite geometric refinement and source-derived Cech histories

The F106 F69-incidence intersection category O_I restricts
canonically to O_J whenever J is a subset of I: adding more
physical edge stars makes the actual site intersection smaller.

F111/v5.270 proved that, within ONE actual physical finite
intersection, arbitrary histories through only genuine indexed
physical charts strictly agree with direct F77 NatIso.
This module removes the remaining gap between DIFFERENT finite
physical intersections: pull back a chart and all of its
original two-distinct-face F42/F51 observed semantics along the
REAL F106 incidence-overlap refinement functor.

We prove, without any extra assumed object / phase / charge laws:
* the actual F77 observed-object and observed-Hom assignments
  commute with genuine inclusion of physical intersections;
* F109 original-source-derived Čech transition COMPONENTS
  are invariant under such a refinement;
* ANY finite chart history in O_J agrees after geometric
  restriction with ANY finite chart history in O_I, even
  when the intermediate chart labels and lengths differ;
* this refinement comparison retains ZERO ADDED Int×Int charge;
* all statements hold for 90 REAL original C60 physical edges.

This is refinement coherence of the F77 OBSERVED presheaf-like
data on the actual incidence intersection poset. It does not
construct a Grothendieck topology or prove the existence of
effective global ORIGINAL F42/F54/F55 source descent. In
particular original nonzero F51 phase and F68 signed physical
north-pentagon curvature remain independently obstructed.
-/

/-- Every original chart available in a smaller family J is
available in a larger family I when J is included in I. -/
def c60F111RefineChart
    {n : Nat} {I J : Finset (Fin n)} (h : J ⊆ I)
    (i : C60F111PhysicalChart J) :
    C60F111PhysicalChart I :=
  ⟨i.1, h i.2⟩

/-- The ACTUAL original F69 physical-intersection restriction
functor, not a synthetic new chart comparison. -/
def c60F111RefinePhysicalOverlap
    {n : Nat} (C : C60F108BothFaceContexts n)
    {I J : Finset (Fin n)} (h : J ⊆ I) :
    C60F106PhysicalOverlap (c60F108BothFacePatchFamily C) I ⥤
      C60F106PhysicalOverlap (c60F108BothFacePatchFamily C) J :=
  c60F106OverlapRestrict (c60F108BothFacePatchFamily C) h

/-- Under TRUE geometry refinement, each F77 observed OBJECT
is exactly the same original source-derived quotient object.
This is not equality of unquotiented original F42 witnesses. -/
theorem c60F111Refinement_observed_obj
    {n : Nat} (C : C60F108BothFaceContexts n)
    {I J : Finset (Fin n)} (h : J ⊆ I)
    (i : C60F111PhysicalChart J)
    (X : C60F106PhysicalOverlap (c60F108BothFacePatchFamily C) I) :
    (c60F111RefinePhysicalOverlap C h ⋙
        c60F111PhysicalObserved C J i).obj X =
      (c60F111PhysicalObserved C I
        (c60F111RefineChart h i)).obj X := rfl

/-- Restriction ALSO respects every actual source physical
incidence Hom at the original charge-observation level.
Both arrows have EXACT ZERO Int×Int charge in the specific
two-physical-polygon source semantics, so are equal in F77. -/
theorem c60F111Refinement_observed_map
    {n : Nat} (C : C60F108BothFaceContexts n)
    {I J : Finset (Fin n)} (h : J ⊆ I)
    (i : C60F111PhysicalChart J)
    {X Y : C60F106PhysicalOverlap (c60F108BothFacePatchFamily C) I}
    (f : X ⟶ Y) :
    (c60F111RefinePhysicalOverlap C h ⋙
      c60F111PhysicalObserved C J i).map f =
    (c60F111PhysicalObserved C I
      (c60F111RefineChart h i)).map f := by
  apply c60F80QuotientThree_ext
  have hL :
      (c60F77QuotientToStrictCharge.map
        ((c60F111RefinePhysicalOverlap C h ⋙
          c60F111PhysicalObserved C J i).map f)).charge =
        (0 : Int × Int) := by
    change
      (c60F77QuotientToStrictCharge.map
        ((c60F106PhysicalObserved
          (c60F108BothFacePatchFamily C)
          (c60F109BothFaceSingletonSemantics C)
          J i.1 i.2).map
            ((c60F111RefinePhysicalOverlap C h).map f))).charge =
        (0 : Int × Int)
    exact c60F109BothFacePhysicalObserved_charge_zero C J i.1 i.2 _
  have hR :
      (c60F77QuotientToStrictCharge.map
        ((c60F111PhysicalObserved C I
          (c60F111RefineChart h i)).map f)).charge =
        (0 : Int × Int) := by
    exact c60F109BothFacePhysicalObserved_charge_zero
      C I i.1 (h i.2) f
  exact hL.trans hR.symm

/-- Hence physical inclusion followed by the source-derived
F77 observer IS the direct physical I-observer as a genuinely
equal Mathlib functor, not just matching values of curvature. -/
theorem c60F111Refinement_observed_functor
    {n : Nat} (C : C60F108BothFaceContexts n)
    {I J : Finset (Fin n)} (h : J ⊆ I)
    (i : C60F111PhysicalChart J) :
    c60F111RefinePhysicalOverlap C h ⋙
        c60F111PhysicalObserved C J i =
      c60F111PhysicalObserved C I
        (c60F111RefineChart h i) := by
  fapply CategoryTheory.Functor.ext
  · intro X
    exact c60F111Refinement_observed_obj C h i X
  · intro X Y f
    exact c60F111Refinement_observed_map C h i f

/-- A genuine F109 natural-isomorphism COMPONENT survives
a real finite incidence refinement: transporting between
any two actual charts before restricting equals doing the
same transport after restricting them to the bigger family.
Its proof uses exact F77 charge faithfulness, not
original F42 word equality or native phase cancellation. -/
theorem c60F111Refinement_transition_app
    {n : Nat} (C : C60F108BothFaceContexts n)
    {I J : Finset (Fin n)} (h : J ⊆ I)
    (i j : C60F111PhysicalChart J)
    (X : C60F106PhysicalOverlap (c60F108BothFacePatchFamily C) I) :
    (c60F111PhysicalTransition C J i j).hom.app
        ((c60F111RefinePhysicalOverlap C h).obj X) =
      (c60F111PhysicalTransition C I
        (c60F111RefineChart h i)
        (c60F111RefineChart h j)).hom.app X := by
  apply c60F80QuotientThree_ext
  exact (c60F111PhysicalTransition_charge_zero C J i j
    ((c60F111RefinePhysicalOverlap C h).obj X)).trans
      (c60F111PhysicalTransition_charge_zero C I
        (c60F111RefineChart h i)
        (c60F111RefineChart h j) X).symm

/-- ANY finite chart history living in the physical smaller
chart family J agrees after TRUE geometric restriction
with ANY (possibly DIFFERENT-LENGTH) chart history in I.
The intermediate charts in either list are all proved to
belong to their respective real physical intersections. -/
theorem c60F111Refinement_anyHistory_app
    {n : Nat} (C : C60F108BothFaceContexts n)
    {I J : Finset (Fin n)} (h : J ⊆ I)
    (i j : C60F111PhysicalChart J)
    (historyJ : List (C60F111PhysicalChart J))
    (historyI : List (C60F111PhysicalChart I))
    (X : C60F106PhysicalOverlap (c60F108BothFacePatchFamily C) I) :
    (c60F111PhysicalTransitionChain C J i j historyJ).app
        ((c60F111RefinePhysicalOverlap C h).obj X) =
      (c60F111PhysicalTransitionChain C I
        (c60F111RefineChart h i)
        (c60F111RefineChart h j) historyI).app X := by
  rw [c60F111PhysicalTransitionChain_eq_direct,
      c60F111PhysicalTransitionChain_eq_direct]
  exact c60F111Refinement_transition_app C h i j X

/-- The F77 COMPARISON along either real physical refinement
has ZERO ADDED integer charge, while original source phase
and F68 physical two-cochain curvature are still separate. -/
theorem c60F111Refinement_anyHistory_charge_zero
    {n : Nat} (C : C60F108BothFaceContexts n)
    {I J : Finset (Fin n)} (h : J ⊆ I)
    (i j : C60F111PhysicalChart J)
    (historyJ : List (C60F111PhysicalChart J))
    (X : C60F106PhysicalOverlap (c60F108BothFacePatchFamily C) I) :
    (c60F77QuotientToStrictCharge.map
      ((c60F111PhysicalTransitionChain C J i j historyJ).app
        ((c60F111RefinePhysicalOverlap C h).obj X))).charge =
      (0 : Int × Int) :=
  c60F111PhysicalTransitionChain_charge_zero C J i j historyJ
    ((c60F111RefinePhysicalOverlap C h).obj X)

/-- Specialize genuine chart-refinement invariance to
the entire ninety-real-edge original C60 finite atlas.
This does not assert arbitrary intersections are nonempty. -/
theorem c60F111AllNinetyRefinement_anyHistory_app
    {I J : Finset (Fin (Fintype.card TruncatedIcosahedralEdge))}
    (h : J ⊆ I)
    (i j : C60F111PhysicalChart J)
    (historyJ : List (C60F111PhysicalChart J))
    (historyI : List (C60F111PhysicalChart I))
    (X : C60F106PhysicalOverlap
      (c60F108BothFacePatchFamily c60F108AllNinetyBothFaces) I) :
    (c60F111PhysicalTransitionChain
      c60F108AllNinetyBothFaces J i j historyJ).app
        ((c60F111RefinePhysicalOverlap
          c60F108AllNinetyBothFaces h).obj X) =
      (c60F111PhysicalTransitionChain
        c60F108AllNinetyBothFaces I
        (c60F111RefineChart h i)
        (c60F111RefineChart h j) historyI).app X :=
  c60F111Refinement_anyHistory_app
    c60F108AllNinetyBothFaces h i j historyJ historyI X

#print axioms c60F111Refinement_observed_obj
#print axioms c60F111Refinement_observed_map
#print axioms c60F111Refinement_observed_functor
#print axioms c60F111Refinement_transition_app
#print axioms c60F111Refinement_anyHistory_app
#print axioms c60F111Refinement_anyHistory_charge_zero
#print axioms c60F111AllNinetyRefinement_anyHistory_app

end
end KUOS.DependentOriginationC60KuuActualPhysicalRefinementCechV5_271
