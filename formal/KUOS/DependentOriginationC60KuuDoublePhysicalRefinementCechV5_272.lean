import KUOS.DependentOriginationC60KuuActualPhysicalRefinementCechV5_271

namespace KUOS.DependentOriginationC60KuuDoublePhysicalRefinementCechV5_272

open CategoryTheory
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationC60NativeExchangeCongruenceQuotientV5_231
open KUOS.DependentOriginationC60KuuActualIncidenceOverlapRefinementV5_260
open KUOS.DependentOriginationC60KuuTwoActualFaceInterchangeV5_265
open KUOS.DependentOriginationC60KuuTwoFaceObservedObjectCechV5_267
open KUOS.DependentOriginationC60KuuActualPhysicalFiniteCechHistoriesV5_270
open KUOS.DependentOriginationC60KuuActualPhysicalRefinementCechV5_271

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.272 / F111 third stage — two successive genuine physical refinements

The actual F106 physical incidence intersections O_I are determined
by real original C60 edge stars, not by arbitrary synthetic points.
Under inclusions K ⊆ J ⊆ I there is a TRUE two-step restriction
from O_I to O_J and then O_K, or a direct original O_I→O_K map.

F111/v5.270 already constructs arbitrary finite F77 Čech histories
for the original two-distinct-face F42/F51 source semantics.
F111/v5.271 constructs compatibility of a single true physical
refinement with all F77 observed objects, Hom maps and arbitrary
finite physical chart histories.

This third stage proves the HIGHER PATH-INDEPENDENCE of two successive
geometric physical refinements with the DIRECT physical refinement,
and independent choice of finite Čech histories in all three
physical chart families. Intermediate chart indices carry actual
membership witnesses, so no illicit chart not belonging to the
intersection can enter a history. Results are equalities of actual
Mathlib F77 morphisms, not only numerical flux or charges.

These are precise OBSERVED finite physical refinement theorems:
they do NOT construct a Grothendieck topology, a global original
F42/F54/F55 source-level 3-descent object, a way to recover the
original native F51 phase from F77, or an uncorrected flat F68
north-pentagon physical gauge.
-/

/-- Subtype chart proof transports compose under the genuine
physical finite-chart inclusions K⊆J⊆I. -/
theorem c60F111RefineChart_twoSteps
    {n : Nat} {I J K : Finset (Fin n)}
    (hJI : J ⊆ I) (hKJ : K ⊆ J)
    (i : C60F111PhysicalChart K) :
    c60F111RefineChart hJI (c60F111RefineChart hKJ i) =
      c60F111RefineChart (Finset.Subset.trans hKJ hJI) i := rfl

/-- Original 60/90/32-cell incidence objects survive the two-step
real refinement exactly as they survive the direct refinement.
This is the ORIGINAL F106 categorical restriction theorem. -/
theorem c60F111PhysicalDoubleRefinement_obj
    {n : Nat} (C : C60F108BothFaceContexts n)
    {I J K : Finset (Fin n)}
    (hJI : J ⊆ I) (hKJ : K ⊆ J)
    (X : C60F106PhysicalOverlap
      (c60F108BothFacePatchFamily C) I) :
    (c60F111RefinePhysicalOverlap C hJI ⋙
        c60F111RefinePhysicalOverlap C hKJ).obj X =
      (c60F111RefinePhysicalOverlap C
        (Finset.Subset.trans hKJ hJI)).obj X :=
  c60F106OverlapRestrict_trans_obj
    (c60F108BothFacePatchFamily C) hJI hKJ X

/-- Actual physical incidence Homs also have STRICT
two-step versus one-step refinement coherence. -/
theorem c60F111PhysicalDoubleRefinement_map
    {n : Nat} (C : C60F108BothFaceContexts n)
    {I J K : Finset (Fin n)}
    (hJI : J ⊆ I) (hKJ : K ⊆ J)
    {X Y : C60F106PhysicalOverlap
      (c60F108BothFacePatchFamily C) I}
    (f : X ⟶ Y) :
    (c60F111RefinePhysicalOverlap C hJI ⋙
        c60F111RefinePhysicalOverlap C hKJ).map f =
      (c60F111RefinePhysicalOverlap C
        (Finset.Subset.trans hKJ hJI)).map f :=
  c60F106OverlapRestrict_trans_map
    (c60F108BothFacePatchFamily C) hJI hKJ f

/-- In the concrete two-original-polygon source semantics,
a double restriction's actual F77 observed OBJECT equals the
directly restricted original F77 observed object. This is
not equality of the old raw original F42 source strings. -/
theorem c60F111PhysicalDoubleRefinement_observed_obj
    {n : Nat} (C : C60F108BothFaceContexts n)
    {I J K : Finset (Fin n)}
    (hJI : J ⊆ I) (hKJ : K ⊆ J)
    (i : C60F111PhysicalChart K)
    (X : C60F106PhysicalOverlap
      (c60F108BothFacePatchFamily C) I) :
    ((c60F111RefinePhysicalOverlap C hJI ⋙
        c60F111RefinePhysicalOverlap C hKJ) ⋙
      c60F111PhysicalObserved C K i).obj X =
        (c60F111PhysicalObserved C I
          (c60F111RefineChart hJI
            (c60F111RefineChart hKJ i))).obj X := by
  rfl

/-- DOUBLE physical refinement compatibility for an arbitrary
F77-observed chart transition: one step K→J followed by J→I
has the same exact natural-transformation component as
the direct original physical restriction K→I. -/
theorem c60F111PhysicalDoubleRefinement_transition_app
    {n : Nat} (C : C60F108BothFaceContexts n)
    {I J K : Finset (Fin n)}
    (hJI : J ⊆ I) (hKJ : K ⊆ J)
    (i j : C60F111PhysicalChart K)
    (X : C60F106PhysicalOverlap
      (c60F108BothFacePatchFamily C) I) :
    (c60F111PhysicalTransition C K i j).hom.app
      ((c60F111RefinePhysicalOverlap C hKJ).obj
        ((c60F111RefinePhysicalOverlap C hJI).obj X)) =
    (c60F111PhysicalTransition C I
      (c60F111RefineChart hJI (c60F111RefineChart hKJ i))
      (c60F111RefineChart hJI (c60F111RefineChart hKJ j))).hom.app X := by
  apply c60F80QuotientThree_ext
  exact
    (c60F111PhysicalTransition_charge_zero C K i j
      ((c60F111RefinePhysicalOverlap C hKJ).obj
        ((c60F111RefinePhysicalOverlap C hJI).obj X))).trans
      (c60F111PhysicalTransition_charge_zero C I
        (c60F111RefineChart hJI (c60F111RefineChart hKJ i))
        (c60F111RefineChart hJI (c60F111RefineChart hKJ j)) X).symm

/-- Arbitrarily many intermediate physical charts are permitted
in EACH of K, J and I, with possibly unrelated chart histories
and lengths. BOTH physical refinements commute strictly with
ALL chosen F77 Čech histories and with their direct comparison.
This is the exact two-step higher refinement-coherence property. -/
theorem c60F111PhysicalDoubleRefinement_anyHistories
    {n : Nat} (C : C60F108BothFaceContexts n)
    {I J K : Finset (Fin n)}
    (hJI : J ⊆ I) (hKJ : K ⊆ J)
    (i j : C60F111PhysicalChart K)
    (historyK : List (C60F111PhysicalChart K))
    (historyJ : List (C60F111PhysicalChart J))
    (historyI : List (C60F111PhysicalChart I))
    (X : C60F106PhysicalOverlap
      (c60F108BothFacePatchFamily C) I) :
    ((c60F111PhysicalTransitionChain C K i j historyK).app
      ((c60F111RefinePhysicalOverlap C hKJ).obj
        ((c60F111RefinePhysicalOverlap C hJI).obj X)) =
      (c60F111PhysicalTransitionChain C J
        (c60F111RefineChart hKJ i)
        (c60F111RefineChart hKJ j) historyJ).app
          ((c60F111RefinePhysicalOverlap C hJI).obj X)) ∧
    ((c60F111PhysicalTransitionChain C J
      (c60F111RefineChart hKJ i)
      (c60F111RefineChart hKJ j) historyJ).app
        ((c60F111RefinePhysicalOverlap C hJI).obj X) =
      (c60F111PhysicalTransitionChain C I
        (c60F111RefineChart hJI (c60F111RefineChart hKJ i))
        (c60F111RefineChart hJI (c60F111RefineChart hKJ j))
        historyI).app X) := by
  constructor
  · exact c60F111Refinement_anyHistory_app C hKJ i j
      historyK historyJ
      ((c60F111RefinePhysicalOverlap C hJI).obj X)
  · exact c60F111Refinement_anyHistory_app C hJI
      (c60F111RefineChart hKJ i)
      (c60F111RefineChart hKJ j)
      historyJ historyI X

/-- Any original two-face F51-derived Čech history in K carries
zero ADDITIONAL integer charge, including after two genuine
physical refinements. This does not measure F68 curvature. -/
theorem c60F111PhysicalDoubleRefinement_historyCharge_zero
    {n : Nat} (C : C60F108BothFaceContexts n)
    {I J K : Finset (Fin n)}
    (hJI : J ⊆ I) (hKJ : K ⊆ J)
    (i j : C60F111PhysicalChart K)
    (historyK : List (C60F111PhysicalChart K))
    (X : C60F106PhysicalOverlap
      (c60F108BothFacePatchFamily C) I) :
    (c60F77QuotientToStrictCharge.map
      ((c60F111PhysicalTransitionChain C K i j historyK).app
        ((c60F111RefinePhysicalOverlap C hKJ).obj
          ((c60F111RefinePhysicalOverlap C hJI).obj X)))).charge =
      (0 : Int × Int) :=
  c60F111PhysicalTransitionChain_charge_zero C K i j historyK
    ((c60F111RefinePhysicalOverlap C hKJ).obj
      ((c60F111RefinePhysicalOverlap C hJI).obj X))

/-- ALL ninety real physical C60 edge charts support the
arbitrary-history double-refinement result, without creating
synthetic physical quadrilaterals or filling empty intersections. -/
theorem c60F111AllNinetyPhysicalDoubleRefinement_anyHistories
    {I J K : Finset (Fin (Fintype.card TruncatedIcosahedralEdge))}
    (hJI : J ⊆ I) (hKJ : K ⊆ J)
    (i j : C60F111PhysicalChart K)
    (historyK : List (C60F111PhysicalChart K))
    (historyJ : List (C60F111PhysicalChart J))
    (historyI : List (C60F111PhysicalChart I))
    (X : C60F106PhysicalOverlap
      (c60F108BothFacePatchFamily c60F108AllNinetyBothFaces) I) :
    ((c60F111PhysicalTransitionChain
      c60F108AllNinetyBothFaces K i j historyK).app
        ((c60F111RefinePhysicalOverlap c60F108AllNinetyBothFaces hKJ).obj
          ((c60F111RefinePhysicalOverlap c60F108AllNinetyBothFaces hJI).obj X)) =
      (c60F111PhysicalTransitionChain
        c60F108AllNinetyBothFaces J
        (c60F111RefineChart hKJ i)
        (c60F111RefineChart hKJ j) historyJ).app
          ((c60F111RefinePhysicalOverlap c60F108AllNinetyBothFaces hJI).obj X)) ∧
    ((c60F111PhysicalTransitionChain
      c60F108AllNinetyBothFaces J
      (c60F111RefineChart hKJ i)
      (c60F111RefineChart hKJ j) historyJ).app
        ((c60F111RefinePhysicalOverlap c60F108AllNinetyBothFaces hJI).obj X) =
      (c60F111PhysicalTransitionChain
        c60F108AllNinetyBothFaces I
        (c60F111RefineChart hJI (c60F111RefineChart hKJ i))
        (c60F111RefineChart hJI (c60F111RefineChart hKJ j))
        historyI).app X) :=
  c60F111PhysicalDoubleRefinement_anyHistories
    c60F108AllNinetyBothFaces hJI hKJ i j historyK historyJ historyI X

#print axioms c60F111RefineChart_twoSteps
#print axioms c60F111PhysicalDoubleRefinement_obj
#print axioms c60F111PhysicalDoubleRefinement_map
#print axioms c60F111PhysicalDoubleRefinement_observed_obj
#print axioms c60F111PhysicalDoubleRefinement_transition_app
#print axioms c60F111PhysicalDoubleRefinement_anyHistories
#print axioms c60F111PhysicalDoubleRefinement_historyCharge_zero
#print axioms c60F111AllNinetyPhysicalDoubleRefinement_anyHistories

end
end KUOS.DependentOriginationC60KuuDoublePhysicalRefinementCechV5_272
