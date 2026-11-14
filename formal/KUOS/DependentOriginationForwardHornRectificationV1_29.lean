import KUOS.DependentOriginationIndependentAdmissibilityRectificationV1_29

/-!
# Forward-only geometric horn rectification and type-(A) admissibility descent

The v1.33 homotopy filler has a directed boundary homotopy FROM the
scaled simplex's existing horn boundary TO the prescribed target horn.
It therefore requires only the endpoint-zero horn-cylinder attachment
lifting property, not a second endpoint-one lifting property.
We build the resulting strict filler from a genuinely typed forward
cylinder extension and preserve the exact target horn equation.

Separately, the actual scaling-sensitive standard type-(A) family is a
subfamily of the indexed inner-horn family. Hence independently proved
inner-horn fibrancy transfers to type-(A) fibrancy, without identifying
different scalings or arbitrary external scaled-anodyne generators.

Nothing asserts a general Duskin nerve has this lifting property.
-/

namespace KUOS.DependentOriginationForwardHornRectificationV1_29

open CategoryTheory Simplicial
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationGlobalDuskinScaledNerveV1_21
open KUOS.DependentOriginationGlobalDuskinScaledHornCoherenceV1_22
open KUOS.DependentOriginationScaledHornHomotopyDescentV1_33
open KUOS.DependentOriginationScaledHornCylinderExtensionV1_39
open KUOS.DependentOriginationScaledHornAttachmentLiftingV1_40
open KUOS.DependentOriginationScaledTerminalRLPV1_41
open KUOS.DependentOriginationScaledAnodyneGeneratorClosureV1_42
open KUOS.DependentOriginationStandardTypeAScaledHornFamilyV1_49
open KUOS.DependentOriginationStrictlyUnitaryDuskinModelTransportV1_27
open KUOS.DependentOriginationScaledDuskinHornTransportV1_29
open KUOS.DependentOriginationCoherentNormalizedScaledModelEquivalenceV1_32
open KUOS.DependentOriginationIndexedDuskinAdmissibilityV1_29
open KUOS.DependentOriginationArbitraryFamilyAdmissibilityDescentV1_29

universe u u₁ u₂ v₁ v₂ w₁ w₂

/-- Only endpoint-zero scaled horn-cylinder RLP is needed, and only for
the exact simplex scaling of each problem. This is weaker than the
two-sided attachment-fibrancy hypothesis used in v1.42. -/
structure ForwardEndpointScaledHornRLP
    (X : SSet.{u}) (sX : ScaledSimplicialSet X) : Prop where
  lifting :
    ∀ {n : Nat} {i : Fin (n + 1)}
      (P : ScaledHornExtensionProblem X sX n i),
      HasLiftingProperty
        (scaledHornCylinderAttachmentInclusion i 0 P.simplexScaling)
        (ScaledSSet.toPoint (ScaledSSet.of X sX))

/-- A directed homotopy filler admits literal strict rectification from
ONE genuine endpoint-zero attachment lift. No backward endpoint RLP and
no assumption of filler equivalence are hidden here. -/
noncomputable def homotopyRectification_of_forwardEndpointRLP
    {X : SSet.{u}} {sX : ScaledSimplicialSet X}
    (R : ForwardEndpointScaledHornRLP X sX) :
    ScaledHornHomotopyRectification X sX where
  rectify := by
    intro n i P h
    rcases h with ⟨Q⟩
    let f : HornRelativeMap X n i :=
      SSet.RelativeMorphism.botEquiv.symm (Λ[n, i].ι ≫ Q.simplexMap)
    let g : HornRelativeMap X n i :=
      SSet.RelativeMorphism.botEquiv.symm P.hornMap
    have H : f.Homotopy g := by
      change SSet.Homotopy (Λ[n, i].ι ≫ Q.simplexMap) P.hornMap
      exact Q.boundaryHomotopy
    let Qf : ScaledHornBoundaryRealization sX P.simplexScaling f :=
      { simplexMap := Q.simplexMap
        boundary_eq := by rfl
        simplexMap_scaled := Q.simplexMap_scaled }
    let L := forwardAttachmentLiftingOfTerminalRLP (R.lifting P)
    obtain ⟨E⟩ := L.toCylinderExtension H Qf
    let T := E.toTarget
    refine ⟨{
      simplexMap := T.simplexMap
      extends_horn := ?_
      simplexMap_scaled := T.simplexMap_scaled
    }⟩
    change P.hornMap = Λ[n, i].ι ≫ T.simplexMap
    exact T.boundary_eq

/-- The full canonical attachment-fibrancy certificate supplies the
weaker one-sided RLP; the converse is NOT asserted. -/
def forwardEndpointRLP_of_attachmentFibrant
    {X : SSet.{u}} {sX : ScaledSimplicialSet X}
    (hX : IsAttachmentFibrant (ScaledSSet.of X sX)) :
    ForwardEndpointScaledHornRLP X sX where
  lifting := by
    intro n i P
    exact attachmentFibrant_hasLiftingProperty hX i 0 P.simplexScaling

/-- Real type-(A) geometric admissibility is a subfamily of the
inner-index selection, regardless of the target's scaled simplices. -/
theorem standardTypeA_admissibility_subfamily_inner
    (X : SSet.{u}) (sX : ScaledSimplicialSet X) :
    AdmissibilitySubfamily
      (standardTypeAScaledHornFamily X sX)
      (allInnerScaledHornFamily sX) := by
  intro n i P h
  exact ⟨h.1, h.2.1⟩

/-- Hence inner-horn fibrancy implies actual type-(A) scaled-horn
fibrancy on the same carrier, without collapsing either scaling predicate. -/
theorem standardTypeA_fibrancy_of_inner
    (X : SSet.{u}) (sX : ScaledSimplicialSet X)
    (h : HasScaledHornFillers X sX (allInnerScaledHornFamily sX)) :
    HasScaledHornFillers X sX
      (standardTypeAScaledHornFamily X sX) :=
  hasScaledHornFillers_of_subfamily
    (allInnerScaledHornFamily sX)
    (standardTypeAScaledHornFamily X sX)
    (standardTypeA_admissibility_subfamily_inner X sX) h

/-- The actual original unlifted B/C inner-horn fibrancy equivalence
requires only one forward endpoint attachment RLP on each normalized
carrier, plus the native coherent quasi-inverse. Neither a reverse
endpoint lifting property nor strict inverse nerve map is assumed. -/
theorem unliftedInnerHornFibrancy_iff_of_forwardEndpointRLP
    (B : Type u₁) [Bicategory.{w₁, v₁} B]
    (C : Type u₂) [Bicategory.{w₂, v₂} C]
    (F : StrictlyUnitaryBicategoricalModelEquivalence B C)
    (G : StrictlyUnitaryBicategoricalModelEquivalence C B)
    (K : NormalizedCoherentQuasiInverse F G)
    (RB : ForwardEndpointScaledHornRLP
      (normalizedDuskinSource B C) (normalizedDuskinSourceScaling B C))
    (RC : ForwardEndpointScaledHornRLP
      (normalizedDuskinTarget B C) (normalizedDuskinTargetScaling B C)) :
    HasScaledHornFillers (duskinNerve B) (duskinScaling B)
      (allInnerScaledHornFamily (duskinScaling B)) ↔
    HasScaledHornFillers (duskinNerve C) (duskinScaling C)
      (allInnerScaledHornFamily (duskinScaling C)) :=
  unliftedInnerHornFibrancy_iff_of_nativeQuasiInverse
    B C F G K
    (homotopyRectification_of_forwardEndpointRLP RB)
    (homotopyRectification_of_forwardEndpointRLP RC)

#print axioms homotopyRectification_of_forwardEndpointRLP
#print axioms forwardEndpointRLP_of_attachmentFibrant
#print axioms standardTypeA_admissibility_subfamily_inner
#print axioms standardTypeA_fibrancy_of_inner
#print axioms unliftedInnerHornFibrancy_iff_of_forwardEndpointRLP

end KUOS.DependentOriginationForwardHornRectificationV1_29
