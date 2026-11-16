import KUOS.DependentOriginationDoubleDeloopingTypeCOuterHornCocycleCompletionPinnedV1_121

namespace KUOS.DependentOriginationDoubleDeloopingTypeCTerminalRLPStandardRightV1_106

open CategoryTheory
open CategoryTheory.Category
open CategoryTheory.Limits
open Opposite
open Simplicial
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationGlobalDuskinScaledNerveV1_21
open KUOS.DependentOriginationScaledTerminalRLPV1_41
open KUOS.DependentOriginationScaledAnodyneGeneratorClosureV1_42
open KUOS.DependentOriginationStandardTypeCCollapsedEdgeV1_58
open KUOS.DependentOriginationCanonicalFibrationThinReflectionV1_92
open KUOS.DependentOriginationDoubleDeloopingNatNonthinDuskinWitnessV1_95
open KUOS.DependentOriginationDoubleDeloopingThinComparisonZeroV1_96
open KUOS.DependentOriginationDoubleDeloopingTypeBTerminalRLPV1_98
open KUOS.DependentOriginationDoubleDeloopingNormalizedCocycleRealizationV1_100
open KUOS.DependentOriginationDoubleDeloopingTypeAFaceValueBridgeV1_121
open KUOS.DependentOriginationDoubleDeloopingTypeCOuterHornCocycleCompletionV1_105

noncomputable section

/-!
# Type-(C) terminal RLP and the concrete standard-right certificate v1.106

Version v1.105 closes all arithmetic in the standard type-(C) outer horn:
every scaled source map supplies a normalized additive cocycle on the full
simplex, restricting to the horn leg and vanishing on the distinguished `01n`
triangle.

This file performs the remaining categorical step exactly once.  The realized
simplex map and the original collapsed-point leg agree on the edge `01`, because
that compatibility already holds in the source pushout.  The native target
pushout therefore supplies a map from the collapsed simplex.  Its minimal
scaling is automatic; the single additional target-thin triangle is thin
because the completed cocycle has zero distinguished comparison.

Consequently every standard type-(C) generator has terminal RLP.  Combining
this with the complete type-(A) RLP of v1.104 and the type-(B) RLP of v1.98
constructs the one-field standard-right certificate of v1.96.  We then expose
the resulting separation not only at the presentation-order level, but as an
inequality of right orthogonal classes: the standard right class contains the
terminal map of `B²ℕ`, while every canonical right map reflects thin
2-simplices and this terminal map does not.
-/

namespace NatTypeCSourceCocycleCompletion

variable
    {m : Nat}
    {f : standardTypeCSource m ⟶ natDoubleDeloopingScaledDuskin}

/-- The completed simplex leg and the original point leg agree on the collapsed
edge.  This is exactly the source pushout compatibility transported through
the horn restriction equation. -/
theorem edge_compat
    (K : NatTypeCSourceCocycleCompletion m f) :
    standardTypeCEdgeToSimplex.{0} m ≫ K.cocycle.toSimplexMap =
      standardTypeCEdgeCollapseToPoint.{0} m ≫ natTypeCPointMap m f := by
  calc
    standardTypeCEdgeToSimplex.{0} m ≫ K.cocycle.toSimplexMap =
        standardTypeCEdgeToHorn.{0} m ≫
          ((Λ[m + 3, (0 : Fin (m + 4))].ι :
            (Λ[m + 3, (0 : Fin (m + 4))] : SSet) ⟶
              (Δ[m + 3] : SSet)) ≫ K.cocycle.toSimplexMap) := by
            simpa only [Category.assoc] using
              congrArg (fun q => q ≫ K.cocycle.toSimplexMap)
                (standardTypeCEdgeToHorn_comp_hornInclusion.{0} m).symm
    _ = standardTypeCEdgeToHorn.{0} m ≫ natTypeCHornMap m f := by
          rw [K.restrict]
    _ = standardTypeCEdgeCollapseToPoint.{0} m ≫ natTypeCPointMap m f := by
          have h := congrArg
            (fun q :
                (standardTypeCEdgeFace m : SSet) ⟶
                  standardTypeCSourceCarrier.{0} m => q ≫ f.map)
            (standardTypeCSource_edge_collapsed.{0} m)
          simpa [natTypeCHornMap, natTypeCPointMap,
            natTypeCSourceHornInl, natTypeCSourcePointInr,
            Category.assoc] using h

/-- The underlying map out of the collapsed target simplex supplied by its
native pushout universal property. -/
def toTargetMap
    (K : NatTypeCSourceCocycleCompletion m f) :
    standardTypeCTargetCarrier.{0} m ⟶ duskinNerve NatDoubleDelooping :=
  pushout.desc
    K.cocycle.toSimplexMap
    (natTypeCPointMap m f)
    (KUOS.DependentOriginationDoubleDeloopingTypeCTerminalRLPStandardRightV1_106.NatTypeCSourceCocycleCompletion.edge_compat K)

@[simp, reassoc]
theorem target_inl_desc
    (K : NatTypeCSourceCocycleCompletion m f) :
    pushout.inl
        (standardTypeCEdgeToSimplex.{0} m)
        (standardTypeCEdgeCollapseToPoint.{0} m) ≫
      (KUOS.DependentOriginationDoubleDeloopingTypeCTerminalRLPStandardRightV1_106.NatTypeCSourceCocycleCompletion.toTargetMap K) = K.cocycle.toSimplexMap := by
  exact pushout.inl_desc
    K.cocycle.toSimplexMap (natTypeCPointMap m f) (KUOS.DependentOriginationDoubleDeloopingTypeCTerminalRLPStandardRightV1_106.NatTypeCSourceCocycleCompletion.edge_compat K)

@[simp, reassoc]
theorem target_inr_desc
    (K : NatTypeCSourceCocycleCompletion m f) :
    pushout.inr
        (standardTypeCEdgeToSimplex.{0} m)
        (standardTypeCEdgeCollapseToPoint.{0} m) ≫
      (KUOS.DependentOriginationDoubleDeloopingTypeCTerminalRLPStandardRightV1_106.NatTypeCSourceCocycleCompletion.toTargetMap K) = natTypeCPointMap m f := by
  exact pushout.inr_desc
    K.cocycle.toSimplexMap (natTypeCPointMap m f) (KUOS.DependentOriginationDoubleDeloopingTypeCTerminalRLPStandardRightV1_106.NatTypeCSourceCocycleCompletion.edge_compat K)

/-- The realized completed simplex sends `01n` to a thin Duskin triangle. -/
theorem cocycle_distinguished_thin
    (K : NatTypeCSourceCocycleCompletion m f) :
    (duskinScaling NatDoubleDelooping).thin
      (K.cocycle.toSimplexMap.app (op ⦋2⦌)
        (standardTypeCTriangle01n m)) := by
  apply
    (natDuskin_thin_iff_comparison_eq_zero
      (K.cocycle.toSimplexMap.app (op ⦋2⦌)
        (standardTypeCTriangle01n m))).2
  dsimp only [standardTypeCTriangle01n]
  rw [NatNormalizedDuskinCocycle.toSimplexMap_triangle_comparison]
  exact K.distinguished_zero

/-- The descended target map preserves the full type-(C) target scaling.
Minimal thin triangles are automatic; the only extra triangle is handled by
`cocycle_distinguished_thin`. -/
theorem toTargetMap_scaled
    (K : NatTypeCSourceCocycleCompletion m f) :
    KUOS.DependentOriginationGlobalDuskinScaledHornCoherenceV1_22.IsScaledMap
      (standardTypeCTargetScaling.{0} m)
      (duskinScaling NatDoubleDelooping)
      (KUOS.DependentOriginationDoubleDeloopingTypeCTerminalRLPStandardRightV1_106.NatTypeCSourceCocycleCompletion.toTargetMap K) := by
  intro t ht
  rcases ht with hmin | hdist
  · exact
      (minimalScaling_map
        (duskinScaling NatDoubleDelooping) (KUOS.DependentOriginationDoubleDeloopingTypeCTerminalRLPStandardRightV1_106.NatTypeCSourceCocycleCompletion.toTargetMap K)) t hmin
  · subst t
    have hfac :
        (KUOS.DependentOriginationDoubleDeloopingTypeCTerminalRLPStandardRightV1_106.NatTypeCSourceCocycleCompletion.toTargetMap K).app (op ⦋2⦌)
            (standardTypeCTargetDistinguishedTriangle.{0} m) =
          K.cocycle.toSimplexMap.app (op ⦋2⦌)
            (standardTypeCTriangle01n m) := by
      have h := congrArg
        (fun q : (Δ[m + 3] : SSet.{0}) ⟶ duskinNerve NatDoubleDelooping =>
          q.app (op ⦋2⦌) (standardTypeCTriangle01n.{0} m))
        (KUOS.DependentOriginationDoubleDeloopingTypeCTerminalRLPStandardRightV1_106.NatTypeCSourceCocycleCompletion.target_inl_desc K)
      exact h
    rw [hfac]
    exact (KUOS.DependentOriginationDoubleDeloopingTypeCTerminalRLPStandardRightV1_106.NatTypeCSourceCocycleCompletion.cocycle_distinguished_thin K)

/-- Upgrade the descended carrier map to a scaled map from the standard
collapsed target. -/
def toLift
    (K : NatTypeCSourceCocycleCompletion m f) :
    standardTypeCTarget m ⟶ natDoubleDeloopingScaledDuskin where
  map := (KUOS.DependentOriginationDoubleDeloopingTypeCTerminalRLPStandardRightV1_106.NatTypeCSourceCocycleCompletion.toTargetMap K)
  scaled := (KUOS.DependentOriginationDoubleDeloopingTypeCTerminalRLPStandardRightV1_106.NatTypeCSourceCocycleCompletion.toTargetMap_scaled K)

/-- The descended lift restricts exactly to the original map on the collapsed
source.  The proof is the source pushout hom-extensionality on the horn and
point legs. -/
theorem toLift_fac
    (K : NatTypeCSourceCocycleCompletion m f) :
    standardTypeCGeneratorHom.{0} m ≫ (KUOS.DependentOriginationDoubleDeloopingTypeCTerminalRLPStandardRightV1_106.NatTypeCSourceCocycleCompletion.toLift K) = f := by
  apply ScaledSSet.ScaledMap.ext
  change standardTypeCCarrierMap.{0} m ≫ (KUOS.DependentOriginationDoubleDeloopingTypeCTerminalRLPStandardRightV1_106.NatTypeCSourceCocycleCompletion.toTargetMap K) = f.map
  apply (standardTypeCSourceCarrier_isPushout.{0} m).hom_ext
  · calc
      natTypeCSourceHornInl m ≫
          (standardTypeCCarrierMap.{0} m ≫ (KUOS.DependentOriginationDoubleDeloopingTypeCTerminalRLPStandardRightV1_106.NatTypeCSourceCocycleCompletion.toTargetMap K)) =
        (natTypeCSourceHornInl m ≫ standardTypeCCarrierMap.{0} m) ≫
          (KUOS.DependentOriginationDoubleDeloopingTypeCTerminalRLPStandardRightV1_106.NatTypeCSourceCocycleCompletion.toTargetMap K) := by simp
      _ =
        ((Λ[m + 3, (0 : Fin (m + 4))].ι :
            (Λ[m + 3, (0 : Fin (m + 4))] : SSet) ⟶
              (Δ[m + 3] : SSet)) ≫
          pushout.inl
            (standardTypeCEdgeToSimplex.{0} m)
            (standardTypeCEdgeCollapseToPoint.{0} m)) ≫
          (KUOS.DependentOriginationDoubleDeloopingTypeCTerminalRLPStandardRightV1_106.NatTypeCSourceCocycleCompletion.toTargetMap K) := by
            dsimp only [natTypeCSourceHornInl]
            exact congrArg
              (fun q => q ≫ (KUOS.DependentOriginationDoubleDeloopingTypeCTerminalRLPStandardRightV1_106.NatTypeCSourceCocycleCompletion.toTargetMap K))
              (standardTypeCCarrierMap_inl_horn.{0} m)
      _ =
        (Λ[m + 3, (0 : Fin (m + 4))].ι :
            (Λ[m + 3, (0 : Fin (m + 4))] : SSet) ⟶
              (Δ[m + 3] : SSet)) ≫
          (pushout.inl
              (standardTypeCEdgeToSimplex.{0} m)
              (standardTypeCEdgeCollapseToPoint.{0} m) ≫
            (KUOS.DependentOriginationDoubleDeloopingTypeCTerminalRLPStandardRightV1_106.NatTypeCSourceCocycleCompletion.toTargetMap K)) := by simp
      _ =
        (Λ[m + 3, (0 : Fin (m + 4))].ι :
            (Λ[m + 3, (0 : Fin (m + 4))] : SSet) ⟶
              (Δ[m + 3] : SSet)) ≫ K.cocycle.toSimplexMap := by
            rw [(KUOS.DependentOriginationDoubleDeloopingTypeCTerminalRLPStandardRightV1_106.NatTypeCSourceCocycleCompletion.target_inl_desc K)]
      _ = natTypeCHornMap m f := K.restrict
      _ = natTypeCSourceHornInl m ≫ f.map := rfl
  · calc
      natTypeCSourcePointInr m ≫
          (standardTypeCCarrierMap.{0} m ≫ (KUOS.DependentOriginationDoubleDeloopingTypeCTerminalRLPStandardRightV1_106.NatTypeCSourceCocycleCompletion.toTargetMap K)) =
        (natTypeCSourcePointInr m ≫ standardTypeCCarrierMap.{0} m) ≫
          (KUOS.DependentOriginationDoubleDeloopingTypeCTerminalRLPStandardRightV1_106.NatTypeCSourceCocycleCompletion.toTargetMap K) := by simp
      _ =
        pushout.inr
            (standardTypeCEdgeToSimplex.{0} m)
            (standardTypeCEdgeCollapseToPoint.{0} m) ≫
          (KUOS.DependentOriginationDoubleDeloopingTypeCTerminalRLPStandardRightV1_106.NatTypeCSourceCocycleCompletion.toTargetMap K) := by
            dsimp only [natTypeCSourcePointInr]
            exact congrArg
              (fun q => q ≫ (KUOS.DependentOriginationDoubleDeloopingTypeCTerminalRLPStandardRightV1_106.NatTypeCSourceCocycleCompletion.toTargetMap K))
              (standardTypeCCarrierMap_inr_point.{0} m)
      _ = natTypeCPointMap m f := (KUOS.DependentOriginationDoubleDeloopingTypeCTerminalRLPStandardRightV1_106.NatTypeCSourceCocycleCompletion.target_inr_desc K)
      _ = natTypeCSourcePointInr m ≫ f.map := rfl

end NatTypeCSourceCocycleCompletion

/-! ## Literal type-(C) terminal RLP -/

/-- Every individual standard type-(C) collapsed-edge generator has the
terminal right lifting property against the concrete scaled Duskin nerve. -/
theorem natDoubleDelooping_hasLiftingProperty_standardTypeC
    (m : Nat) :
    HasLiftingProperty
      (standardTypeCGeneratorHom.{0} m)
      (ScaledSSet.toPoint natDoubleDeloopingScaledDuskin) := by
  apply (ScaledSSet.hasLiftingProperty_toPoint_iff
    (standardTypeCGeneratorHom.{0} m)).2
  intro f
  rcases natDoubleDelooping_hasAllStandardTypeCSourceCocycleCompletions
    m f with ⟨K⟩
  exact ⟨(KUOS.DependentOriginationDoubleDeloopingTypeCTerminalRLPStandardRightV1_106.NatTypeCSourceCocycleCompletion.toLift K), (KUOS.DependentOriginationDoubleDeloopingTypeCTerminalRLPStandardRightV1_106.NatTypeCSourceCocycleCompletion.toLift_fac K)⟩

/-- Equivalently, the terminal map belongs to the right class of the complete
standard type-(C) generator family. -/
theorem natDoubleDelooping_standardTypeC_rlp :
    (standardTypeCScaledAnodyneGenerators : MorphismProperty (ScaledSSet.{0})).rlp
      (ScaledSSet.toPoint natDoubleDeloopingScaledDuskin) := by
  intro X Y i hi
  cases hi with
  | mk m => exact natDoubleDelooping_hasLiftingProperty_standardTypeC m

/-! ## Assemble the standard A/B/C right class -/

/-- The concrete terminal map has RLP against every generator in the explicit
standard A/B/C union. -/
theorem natDoubleDelooping_standardABC_generators_rlp :
    (standardScaledAnodyneGeneratorsABC : MorphismProperty (ScaledSSet.{0})).rlp
      (ScaledSSet.toPoint natDoubleDeloopingScaledDuskin) := by
  intro X Y i hi
  rcases hi with (hiA | hiB) | hiC
  · exact natDoubleDelooping_standardTypeA_rlp i hiA
  · exact natDoubleDelooping_standardTypeB_rlp i hiB
  · exact natDoubleDelooping_standardTypeC_rlp i hiC

/-- Passing to the generated left orthogonal closure does not change the right
class, so the concrete terminal map is standard-right in the exact sense
required by the v1.96 certificate. -/
theorem natDoubleDelooping_standardGeneratedABC_rlp :
    (standardGeneratedScaledAnodyneABC : MorphismProperty (ScaledSSet.{0})).rlp
      (ScaledSSet.toPoint natDoubleDeloopingScaledDuskin) := by
  change
    ((standardScaledAnodyneGeneratorsABC : MorphismProperty (ScaledSSet.{0})).rlp.llp).rlp
      (ScaledSSet.toPoint natDoubleDeloopingScaledDuskin)
  rw [MorphismProperty.rlp_llp_rlp]
  exact natDoubleDelooping_standardABC_generators_rlp

/-- The previously conditional one-field separator certificate is now
constructed unconditionally. -/
def natDoubleDeloopingStandardRightCertificate :
    NatDoubleDeloopingStandardRightCertificate where
  standardRight := natDoubleDelooping_standardGeneratedABC_rlp

/-! ## Unconditional separation consequences -/

/-- The standard-right terminal witness is not thinness-reflecting. -/
theorem natDoubleDelooping_terminal_not_reflectsThinTwoSimplices :
    ¬ ReflectsThinTwoSimplices
      (ScaledSSet.toPoint natDoubleDeloopingScaledDuskin) :=
  terminal_not_reflects_of_standardRightCertificate
    natDoubleDeloopingStandardRightCertificate

/-- The arbitrary-scaling standard obstruction cannot be closed. -/
theorem natDoubleDelooping_not_standardArbitraryScalingObstructionClosed :
    ¬ KUOS.DependentOriginationStandardArbitraryScalingWaypointV1_89.StandardArbitraryScalingObstructionClosed.{0} :=
  not_standardArbitraryScalingObstructionClosed_of_standardRightCertificate
    natDoubleDeloopingStandardRightCertificate

/-- The forward presentation order from the stronger canonical KuuOS
presentation to the standard A/B/C presentation fails. -/
theorem natDoubleDelooping_not_canonicalKuuOS_le_standardABC :
    ¬ KUOS.DependentOriginationGeneratedPresentationQuotientInvariantV1_81.canonicalKuuOSPresentation.{0} ≤
      KUOS.DependentOriginationGeneratedPresentationQuotientInvariantV1_81.standardABCPresentation.{0} :=
  not_canonicalKuuOS_le_standardABC_of_standardRightCertificate
    natDoubleDeloopingStandardRightCertificate

/-! ## Presentation-independent right-class invariant -/

/-- The standard right class is not contained in the canonical right class.
The witness is the terminal map of `B²ℕ`: it is standard-right by the theorem
above, but cannot be canonical-right because every canonical-right map reflects
thin 2-simplices. -/
theorem standardGeneratedRight_not_le_canonicalGeneratedRight :
    ¬ (standardGeneratedScaledFibrationABC.{0} : MorphismProperty (ScaledSSet.{0})) ≤
      (canonicalGeneratedScaledAnodyne.{0} : MorphismProperty (ScaledSSet.{0})).rlp := by
  intro hle
  have hcan :
      (canonicalGeneratedScaledAnodyne.{0} : MorphismProperty (ScaledSSet.{0})).rlp
        (ScaledSSet.toPoint natDoubleDeloopingScaledDuskin) :=
    hle (ScaledSSet.toPoint natDoubleDeloopingScaledDuskin) natDoubleDelooping_standardABC_generators_rlp
  have hreflect := canonicalGeneratedRight_reflectsThinTwoSimplices hcan
  exact natDoubleDelooping_terminal_not_reflectsThinTwoSimplices hreflect

/-- In particular the standard and canonical right orthogonal classes are not
equal.  This statement depends only on the resulting right classes, not on a
choice of generating presentation. -/
theorem standardGeneratedRight_ne_canonicalGeneratedRight :
    (standardGeneratedScaledFibrationABC.{0} : MorphismProperty (ScaledSSet.{0})) ≠
      (canonicalGeneratedScaledAnodyne.{0} : MorphismProperty (ScaledSSet.{0})).rlp := by
  intro h
  apply standardGeneratedRight_not_le_canonicalGeneratedRight
  rw [h]

/-!
The standard-right frontier is now closed for the concrete additive double
delooping:

```text
Type A    all dimensions         terminal RLP   -- v1.104
Type B    scaling enrichment     terminal RLP   -- v1.98
Type C    collapsed outer horns  terminal RLP   -- v1.106
---------------------------------------------------------
standard A/B/C generated right class contains B²ℕ -> *
```

The same terminal map is excluded from the canonical right class by thinness
reflection.  Hence the separation has been upgraded from a generator-level
comparison to the right-class invariant

```text
standardGeneratedScaledFibrationABC.{0}
  ≠ canonicalGeneratedScaledAnodyne.rlp.
```

No claim `canonical = standard` is used; the explicit standard-right witness is
now the formal reason the two right classes differ.
-/

end

end KUOS.DependentOriginationDoubleDeloopingTypeCTerminalRLPStandardRightV1_106
