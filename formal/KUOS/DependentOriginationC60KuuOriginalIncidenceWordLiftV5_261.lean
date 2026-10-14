import KUOS.DependentOriginationC60KuuActualIncidenceOverlapRefinementV5_260
import KUOS.DependentOriginationGrayC60OriginalFaceHorizontalCompositionV5_199

namespace KUOS.DependentOriginationC60KuuOriginalIncidenceWordLiftV5_261

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayC60CyclicGlobalPastingV5_156
open KUOS.DependentOriginationGrayC60PresentedInterchangerV5_191
open KUOS.DependentOriginationGrayC60PresentedFaceTwoCellsV5_190
open KUOS.DependentOriginationGrayC60OriginalFaceHorizontalPresentationV5_199
open KUOS.DependentOriginationGrayC60OriginalFaceHorizontalThreeHomV5_199
open KUOS.DependentOriginationGrayC60OriginalFaceHorizontalCompositionV5_199
open KUOS.DependentOriginationC60NativeExchangeCongruenceQuotientV5_231
open KUOS.DependentOriginationC60KuuReplacementInterchangeV5_248
open KUOS.DependentOriginationC60KuuLocalUniversalDescentV5_249
open KUOS.DependentOriginationC60KuuPhysicalOverlapObstructionV5_259
open KUOS.DependentOriginationC60KuuActualIncidenceOverlapRefinementV5_260

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.261 / F107 — original F42/F51 words as a sufficient physical incidence semantics

F106 constructed ACTUAL C60 incidence-star overlap categories and all
finite refinement functors, but correctly left the semantic functors
from each singleton star to its own original F95 Hom category as
explicit extra data. A physical incidence arrow is NOT by itself
an original F42 two-cell or an original F51 three-cell.

This module breaks down the missing input into the ORIGINAL syntax:
* each actual physical incidence cell is labelled by a genuinely
  path-indexed original F42 face-two-cell;
* each actual physical incidence arrow is labelled by a TYPED F51
  three-cell term between the two precisely chosen F42 boundaries;
* only the two independent Int × Int charge coordinates need satisfy
  the categorical identity and composition laws for F95 descent.

Those charge-level conditions construct ACTUAL bundled Mathlib
functors into F95 on all ninety original edge-incidence stars.
By the verified F106 geometric inclusions this supplies semantics
for arbitrary finite intersections. Distinct raw words with the
same native integer charge yield the same F95 Hom, irrespective of
their independent ZMod 2 Gray exchange phase.

Full ORIGINAL F51 categorical lifting is STRONGER: the phase must
also satisfy identity and composition. We construct that lift
conditional on the extra phase equations and exhibit the nonzero
phase-composition defect as an explicit obstruction to the proposed
raw F51 source functor. Original F42 degree mismatch provides an
independent obstruction to even choosing a typed raw F51 word.

This is a constructive SUFFICIENT input interface, not a claim
that arbitrary real C60 incidence arrows canonically choose F42
objects or F51/F55 three-cell words. We neither restore old Gray
interchange nor erase nonzero genuine F55 physical curvature.
-/

/-! ## I. ORIGINAL F42 source boundaries for the real incidence cells -/

/-- Data of original F42 face-two-cell presentations, indexed by
each of the actual original ninety C60 edge stars. Both source
and target C60 1-paths are EXACTLY the chosen F105 physical paths. -/
structure C60F107OriginalF42Labels
    {n : Nat} (A : C60F105PhysicalEdgePatchFamily n) where
  face : (i : Fin n) →
    C60F106PhysicalOverlap A ({i} : Finset (Fin n)) →
      C60F42PresentedFaceCell (A.p i) (A.q i)

/-- A chosen, correctly boundary-typed ORIGINAL F51 raw 3-arrow
for EVERY true incidence arrow. The source category is the real
F69 incidence subposet, not a freely invented category of cells. -/
structure C60F107OriginalF51Words
    {n : Nat} (A : C60F105PhysicalEdgePatchFamily n)
    (L : C60F107OriginalF42Labels A) where
  word : (i : Fin n) →
    {X Y : C60F106PhysicalOverlap A ({i} : Finset (Fin n))} →
    (f : X ⟶ Y) →
      C60F51PresentedThreeCell (L.face i X) (L.face i Y)

/-- Any chosen ORIGINAL F51 three-cell label necessarily preserves
the ORIGINAL F42 face parity at its true incidence-arrow endpoints.
The incidence geometry alone imposes no such face-label equality. -/
theorem c60F107OriginalFaceDegree_preserved
    {n : Nat} (A : C60F105PhysicalEdgePatchFamily n)
    (L : C60F107OriginalF42Labels A)
    (W : C60F107OriginalF51Words A L)
    (i : Fin n)
    {X Y : C60F106PhysicalOverlap A ({i} : Finset (Fin n))}
    (f : X ⟶ Y) :
    c60F43FaceDegree (L.face i X) =
      c60F43FaceDegree (L.face i Y) :=
  (W.word i f).preservesFaceDegree

/-- A mismatch of the original F42 boundary degrees for ONE
ACTUAL incidence arrow obstructs every global choice of
correctly typed original F51 words with those F42 labels. -/
theorem c60F107FaceDegreeMismatch_obstruction
    {n : Nat} (A : C60F105PhysicalEdgePatchFamily n)
    (L : C60F107OriginalF42Labels A)
    (i : Fin n)
    {X Y : C60F106PhysicalOverlap A ({i} : Finset (Fin n))}
    (f : X ⟶ Y)
    (hbad : c60F43FaceDegree (L.face i X) ≠
      c60F43FaceDegree (L.face i Y)) :
    ¬ Nonempty (C60F107OriginalF51Words A L) := by
  rintro ⟨W⟩
  exact hbad (c60F107OriginalFaceDegree_preserved A L W i f)

/-! ## II. Charge-only coherence constructs the genuine F95 semantics -/

/-- Exactly the Kuu quotient-required identity and composition
laws: TWO integer charges, not the original independent phase.
We never assume the raw F51 syntactic equations themselves. -/
structure C60F107ChargeCoherence
    {n : Nat} {A : C60F105PhysicalEdgePatchFamily n}
    {L : C60F107OriginalF42Labels A}
    (W : C60F107OriginalF51Words A L) : Prop where
  id :
    ∀ (i : Fin n)
      (X : C60F106PhysicalOverlap A ({i} : Finset (Fin n))),
      (W.word i (𝟙 X)).toNative.charge = (0 : Int × Int)
  comp :
    ∀ (i : Fin n)
      {X Y Z : C60F106PhysicalOverlap A ({i} : Finset (Fin n))}
      (f : X ⟶ Y) (g : Y ⟶ Z),
      (W.word i (f ≫ g)).toNative.charge =
        (W.word i f).toNative.charge +
          (W.word i g).toNative.charge

/-- SOURCE-FREE at the phase level, but nontrivial and fully
original-source-typed at the F42/F51 level: an actual Mathlib
Functor from the real C60 physical singleton-star incidence
category into its correctly indexed F95 Kuu category. -/
def c60F107SingletonKuuFunctor
    {n : Nat} (A : C60F105PhysicalEdgePatchFamily n)
    (L : C60F107OriginalF42Labels A)
    (W : C60F107OriginalF51Words A L)
    (h : C60F107ChargeCoherence W)
    (i : Fin n) :
    C60F106PhysicalOverlap A ({i} : Finset (Fin n)) ⥤
      C60F95LocalKuuQuotient (A.p i) (A.q i) where
  obj X := ⟨⟨L.face i X⟩⟩
  map := fun {_ _} f =>
    (c60F95LocalProjection (A.p i) (A.q i)).map
      (c60F51Of (W.word i f))
  map_id := by
    intro X
    calc
      (c60F95LocalProjection (A.p i) (A.q i)).map
          (c60F51Of (W.word i (𝟙 X))) =
        (c60F95LocalProjection (A.p i) (A.q i)).map
          (𝟙 (⟨L.face i X⟩ : C60F51OriginalTwo (A.p i) (A.q i))) := by
            apply (c60F95Projection_map_eq_iff_charges _ _).mpr
            simpa only [c60F51Eval_of] using h.id i X
      _ = _ := (c60F95LocalProjection (A.p i) (A.q i)).map_id _
  map_comp := by
    intro X Y Z f g
    calc
      (c60F95LocalProjection (A.p i) (A.q i)).map
          (c60F51Of (W.word i (f ≫ g))) =
        (c60F95LocalProjection (A.p i) (A.q i)).map
          (c60F51Of (W.word i f) ≫ c60F51Of (W.word i g)) := by
            apply (c60F95Projection_map_eq_iff_charges _ _).mpr
            simpa only [c60F51Eval_of, c60F51Eval_comp,
              grayNeutral_add_charge] using h.comp i f g
      _ = _ := (c60F95LocalProjection (A.p i) (A.q i)).map_comp _ _

/-- F107 DISCHARGES F106's missing per-patch SEMANTIC input
from precisely stated ORIGINAL F42/F51 source words and their
two-component charge coherence. No F95 functor is postulated. -/
def c60F107DerivedSingletonSemantics
    {n : Nat} (A : C60F105PhysicalEdgePatchFamily n)
    (L : C60F107OriginalF42Labels A)
    (W : C60F107OriginalF51Words A L)
    (h : C60F107ChargeCoherence W) :
    C60F106SingletonF95Semantics A where
  patch i := c60F107SingletonKuuFunctor A L W h i

/-- The exact original raw F51 word appears on every genuine
singleton-star Hom AFTER the honest F95 categorical projection. -/
theorem c60F107Singleton_map_spec
    {n : Nat} (A : C60F105PhysicalEdgePatchFamily n)
    (L : C60F107OriginalF42Labels A)
    (W : C60F107OriginalF51Words A L)
    (h : C60F107ChargeCoherence W)
    (i : Fin n)
    {X Y : C60F106PhysicalOverlap A ({i} : Finset (Fin n))}
    (f : X ⟶ Y) :
    (c60F107SingletonKuuFunctor A L W h i).map f =
      (c60F95LocalProjection (A.p i) (A.q i)).map
        (c60F51Of (W.word i f)) := rfl

/-- All finite genuine physical overlap restrictions are DERIVED
through F106, from the single physical-patch raw source words. -/
def c60F107PhysicalOverlapKuuFunctor
    {n : Nat} (A : C60F105PhysicalEdgePatchFamily n)
    (L : C60F107OriginalF42Labels A)
    (W : C60F107OriginalF51Words A L)
    (h : C60F107ChargeCoherence W)
    (I : Finset (Fin n)) (i : Fin n) (hi : i ∈ I) :
    C60F106PhysicalOverlap A I ⥤
      C60F95LocalKuuQuotient (A.p i) (A.q i) :=
  c60F106PhysicalToF95 A
    (c60F107DerivedSingletonSemantics A L W h) I i hi

/-- The new physical-overlap functors factor as the actual
geometric refinement followed by the original F51-word F95
projection. This is on ALL overlap objects and Homs. -/
theorem c60F107PhysicalOverlapKuuFunctor_spec
    {n : Nat} (A : C60F105PhysicalEdgePatchFamily n)
    (L : C60F107OriginalF42Labels A)
    (W : C60F107OriginalF51Words A L)
    (h : C60F107ChargeCoherence W)
    (I : Finset (Fin n)) (i : Fin n) (hi : i ∈ I) :
    c60F107PhysicalOverlapKuuFunctor A L W h I i hi =
      c60F106ToSingleton A I i hi ⋙
        c60F107SingletonKuuFunctor A L W h i := rfl

/-! ## III. Exactly which changes to F51 raw words are forgotten -/

/-- Two different ORIGINAL F51 presentations with the SAME original
F42 object labels have identical F95 arrows IFF BOTH charge
coordinates agree; NO equality of Gray exchange phases is required. -/
theorem c60F107ReplaceRawWords_iff_charges
    {n : Nat} (A : C60F105PhysicalEdgePatchFamily n)
    (L : C60F107OriginalF42Labels A)
    (W₁ W₂ : C60F107OriginalF51Words A L)
    (h₁ : C60F107ChargeCoherence W₁)
    (h₂ : C60F107ChargeCoherence W₂)
    (i : Fin n)
    {X Y : C60F106PhysicalOverlap A ({i} : Finset (Fin n))}
    (f : X ⟶ Y) :
    (c60F107SingletonKuuFunctor A L W₁ h₁ i).map f =
      (c60F107SingletonKuuFunctor A L W₂ h₂ i).map f ↔
    (W₁.word i f).toNative.charge =
      (W₂.word i f).toNative.charge := by
  change
    (c60F95LocalProjection (A.p i) (A.q i)).map
      (c60F51Of (W₁.word i f)) =
    (c60F95LocalProjection (A.p i) (A.q i)).map
      (c60F51Of (W₂.word i f)) ↔ _
  exact (c60F95Projection_map_eq_iff_charges _ _)

/-! ## IV. The separate original Gray phase determines SOURCE liftability -/

/-- The ADDITIONAL source-phase coherence needed to lift the
SAME original words to a full-original-native F51 Mathlib Functor.
It is stronger than the F95 charge coherence already proved. -/
structure C60F107PhaseCoherence
    {n : Nat} {A : C60F105PhysicalEdgePatchFamily n}
    {L : C60F107OriginalF42Labels A}
    (W : C60F107OriginalF51Words A L) : Prop where
  id :
    ∀ (i : Fin n)
      (X : C60F106PhysicalOverlap A ({i} : Finset (Fin n))),
      (W.word i (𝟙 X)).toNative.phase = (0 : ZMod 2)
  comp :
    ∀ (i : Fin n)
      {X Y Z : C60F106PhysicalOverlap A ({i} : Finset (Fin n))}
      (f : X ⟶ Y) (g : Y ⟶ Z),
      (W.word i (f ≫ g)).toNative.phase =
        (W.word i f).toNative.phase +
          (W.word i g).toNative.phase

/-- A full-original-native F51 functor can be constructed ONLY
after BOTH independent charges AND the separate braided phase
have been proved coherent. All F42 object boundary terms remain. -/
def c60F107NativeF51Functor
    {n : Nat} (A : C60F105PhysicalEdgePatchFamily n)
    (L : C60F107OriginalF42Labels A)
    (W : C60F107OriginalF51Words A L)
    (hc : C60F107ChargeCoherence W)
    (hp : C60F107PhaseCoherence W)
    (i : Fin n) :
    C60F106PhysicalOverlap A ({i} : Finset (Fin n)) ⥤
      C60F51OriginalTwo (A.p i) (A.q i) where
  obj X := ⟨L.face i X⟩
  map := fun {_ _} f => c60F51Of (W.word i f)
  map_id := by
    intro X
    apply Quot.sound
    change (W.word i (𝟙 X)).toNative = (0 : GradedThreeCell 0 0)
    apply GradedThreeCell.ext
    · exact hc.id i X
    · exact hp.id i X
  map_comp := by
    intro X Y Z f g
    apply Quot.sound
    change (W.word i (f ≫ g)).toNative =
      (W.word i f).toNative + (W.word i g).toNative
    apply GradedThreeCell.ext
    · simpa only [grayNeutral_add_charge] using hc.comp i f g
    · simpa only [grayNeutral_add_phase] using hp.comp i f g

/-- When phase coherence does hold, the OLD full-native F51
functor factors to EXACTLY THE SAME F95 semantic functor built
using the weaker Kuu charge coherence. No phase is recovered
FROM F95: the full native lift was separately supplied. -/
theorem c60F107NativeProjection_equalsKuu
    {n : Nat} (A : C60F105PhysicalEdgePatchFamily n)
    (L : C60F107OriginalF42Labels A)
    (W : C60F107OriginalF51Words A L)
    (hc : C60F107ChargeCoherence W)
    (hp : C60F107PhaseCoherence W)
    (i : Fin n) :
    c60F107NativeF51Functor A L W hc hp i ⋙
      c60F95LocalProjection (A.p i) (A.q i) =
        c60F107SingletonKuuFunctor A L W hc i := rfl

/-- A real phase obstruction is the failure of one original F51
incidence-word composite to respect native ZMod 2 evaluation.
This is NOT a nonzero Kuu integer-charge obstruction. -/
def c60F107PhaseCompositionDefect
    {n : Nat} {A : C60F105PhysicalEdgePatchFamily n}
    {L : C60F107OriginalF42Labels A}
    (W : C60F107OriginalF51Words A L)
    (i : Fin n)
    {X Y Z : C60F106PhysicalOverlap A ({i} : Finset (Fin n))}
    (f : X ⟶ Y) (g : Y ⟶ Z) : ZMod 2 :=
  (W.word i (f ≫ g)).toNative.phase -
    ((W.word i f).toNative.phase + (W.word i g).toNative.phase)

/-- The original native F51 Hom carried by one genuinely typed
physical incidence arrow, before deliberate F95 phase forgetting. -/
def c60F107NativeWordHom
    {n : Nat} (A : C60F105PhysicalEdgePatchFamily n)
    (L : C60F107OriginalF42Labels A)
    (W : C60F107OriginalF51Words A L)
    (i : Fin n)
    {X Y : C60F106PhysicalOverlap A ({i} : Finset (Fin n))}
    (f : X ⟶ Y) :
    (⟨L.face i X⟩ : C60F51OriginalTwo (A.p i) (A.q i)) ⟶
      (⟨L.face i Y⟩ : C60F51OriginalTwo (A.p i) (A.q i)) :=
  c60F51Of (W.word i f)

/-- A NONZERO phase-composition defect OBSTRUCTS a genuine
source F51 functor taking these exact raw word choices to arrows,
even if the charges alone form a valid F95 functor. -/
theorem c60F107NonzeroPhase_obstructsNativeComp
    {n : Nat} (A : C60F105PhysicalEdgePatchFamily n)
    (L : C60F107OriginalF42Labels A)
    (W : C60F107OriginalF51Words A L)
    (i : Fin n)
    {X Y Z : C60F106PhysicalOverlap A ({i} : Finset (Fin n))}
    (f : X ⟶ Y) (g : Y ⟶ Z)
    (hbad : c60F107PhaseCompositionDefect W i f g ≠ 0) :
    c60F107NativeWordHom A L W i (f ≫ g) ≠
      c60F107NativeWordHom A L W i f ≫
        c60F107NativeWordHom A L W i g := by
  intro heq
  have hn := congrArg
    (fun z : (⟨L.face i X⟩ : C60F51OriginalTwo (A.p i) (A.q i)) ⟶
        (⟨L.face i Z⟩ : C60F51OriginalTwo (A.p i) (A.q i)) =>
       (c60F51Eval z).phase) heq
  simp only [c60F107NativeWordHom, c60F51Eval_of] at hn
  exact hbad (sub_eq_zero.mpr hn)

#print axioms c60F107OriginalFaceDegree_preserved
#print axioms c60F107FaceDegreeMismatch_obstruction
#print axioms c60F107SingletonKuuFunctor
#print axioms c60F107DerivedSingletonSemantics
#print axioms c60F107Singleton_map_spec
#print axioms c60F107PhysicalOverlapKuuFunctor_spec
#print axioms c60F107ReplaceRawWords_iff_charges
#print axioms c60F107NativeF51Functor
#print axioms c60F107NativeProjection_equalsKuu
#print axioms c60F107NonzeroPhase_obstructsNativeComp

end
end KUOS.DependentOriginationC60KuuOriginalIncidenceWordLiftV5_261
