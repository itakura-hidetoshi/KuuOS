import KUOS.DependentOriginationCanonicalInnerHornContractibleFibrancyV1_114
import KUOS.DependentOriginationPresentationIndependentSeparationTypeBReverseV1_107

namespace KUOS.DependentOriginationCanonicalStandardABCFibrantObjectStrictOrderV1_115

open CategoryTheory
open CategoryTheory.Category
open CategoryTheory.Limits
open Opposite
open Simplicial
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationGlobalDuskinScaledHornCoherenceV1_22
open KUOS.DependentOriginationHomotopyClassScaledHornInvariantV1_37
open KUOS.DependentOriginationScaledTerminalRLPV1_41
open KUOS.DependentOriginationScaledAnodyneGeneratorClosureV1_42
open KUOS.DependentOriginationStandardTypeAScaledHornFamilyV1_49
open KUOS.DependentOriginationStandardTypeBScalingPushoutV1_56
open KUOS.DependentOriginationStandardTypeCCollapsedEdgeV1_58
open KUOS.DependentOriginationCanonicalFibrancyAtomicTwoSimplexAuditV1_91
open KUOS.DependentOriginationDoubleDeloopingTypeCTerminalRLPStandardRightV1_106
open KUOS.DependentOriginationPresentationIndependentSeparationTypeBReverseV1_107
open KUOS.DependentOriginationCanonicalInnerHornContractibleFibrancyV1_114

universe u

noncomputable section

/-!
# Strict canonical versus standard A/B/C fibrant-object semantics v1.115

Version v1.114 proved that every horn of dimension at least two is
contractible in the simplicial homotopy class used by the KuuOS
strictification spine.  Its final wrapper used only inner horns because that
was the type-(A) object-level frontier under discussion.

The contraction itself is not inner-specific.  This file extracts the actual
all-horn consequence and uses it on the outer horns underlying the standard
type-(C) collapsed-edge generators.

For a map from the type-(C) source

```text
Lambda_0^n  ⨿_{Delta^{0,1}} Delta^0 -> X,
```

we first forget to the horn leg and give both horn and simplex minimal scaling.
The v1.114 contraction plus canonical terminal RLP produces a strict simplex
extension.  On the collapsed edge this extension agrees with the original
point leg because the source is already a pushout.  The target pushout then
descends the two maps to

```text
Delta^n  ⨿_{Delta^{0,1}} Delta^0 -> X.
```

Canonical attachment fibrancy forces the scaling of `X` to be maximal by
v1.91, so the descended target map automatically preserves the additional
standard type-(C) thin triangle.  No type-(C) cocycle calculation is required.

Together with v1.114 type-(A) terminal RLP and the already-proved canonical
membership of the type-(B) scaling enrichment, this proves that every
canonical attachment-fibrant object is fibrant for the complete standard
A/B/C generated presentation.

The converse fails concretely: the double delooping `B^2 N` is standard
A/B/C-right by v1.106, while the atomic two-simplex separator of v1.107 shows
that its terminal map is not canonical-right.  Thus the two presentations do
not merely differ as left classes: their fibrant-object semantics are
strictly ordered.

This semantic theorem is independent of the still-open presentation-level
reverse inclusion of standard type-(A)/(C) generators into the canonical
left class.
-/

/-! ## Every dimension-at-least-two horn strictly fills -/

/-- The v1.114 contraction/strictification argument needs only `2 <= n`.
Innerness was used there solely by the `HasScaledHornFillers` interface, not by
the horn contraction itself. -/
theorem attachmentFibrant_hornFiller_of_two_le
    {X : SSet.{u}}
    {sX : ScaledSimplicialSet X}
    (hX : IsAttachmentFibrant (ScaledSSet.of X sX))
    {n : Nat}
    {i : Fin (n + 1)}
    (P : ScaledHornExtensionProblem X sX n i)
    (hn : 2 <= n) :
    Nonempty (ScaledHornFiller P) := by
  obtain ⟨m, hm⟩ : ∃ m : Nat, n = m + 2 :=
    ⟨n - 2, by omega⟩
  subst n
  let Q : HomotopyClassScaledHornFiller P :=
    innerHornHomotopyClassFillerOfMaximalScaling
      m i P (attachmentFibrant_scaling_eq_maximal hX)
  exact (problemTerminalRLPOfAttachmentFibrant hX P).strictify Q

/-! ## Type-(C) outer horn plus pushout descent -/

/-- The underlying horn leg of a standard type-(C) source map. -/
def standardTypeCHornLeg
    {X : ScaledSSet.{u}}
    {m : Nat}
    (f : standardTypeCSource m ⟶ X) :
    (Λ[m + 3, (0 : Fin (m + 4))] : SSet.{u}) ⟶ X.carrier :=
  pushout.inl
      (standardTypeCEdgeToHorn m)
      (standardTypeCEdgeCollapseToPoint m) ≫
    f.map

/-- The collapsed-point leg of a standard type-(C) source map. -/
def standardTypeCPointLeg
    {X : ScaledSSet.{u}}
    {m : Nat}
    (f : standardTypeCSource m ⟶ X) :
    (Δ[0] : SSet.{u}) ⟶ X.carrier :=
  pushout.inr
      (standardTypeCEdgeToHorn m)
      (standardTypeCEdgeCollapseToPoint m) ≫
    f.map

/-- Forget the type-(C) horn leg to a minimally-scaled horn problem.  Minimal
source scaling makes both the horn inclusion and the horn map automatically
scaled. -/
def standardTypeCMinimalHornProblem
    {X : ScaledSSet.{u}}
    {m : Nat}
    (f : standardTypeCSource m ⟶ X) :
    ScaledHornExtensionProblem
      X.carrier X.scaling (m + 3) (0 : Fin (m + 4)) where
  hornScaling :=
    minimalScaling
      (Λ[m + 3, (0 : Fin (m + 4))] : SSet.{u})
  simplexScaling := minimalScaling (Δ[m + 3] : SSet.{u})
  inclusion_scaled :=
    minimalScaling_map
      (minimalScaling (Δ[m + 3] : SSet.{u}))
      (Λ[m + 3, (0 : Fin (m + 4))].ι :
        (Λ[m + 3, (0 : Fin (m + 4))] : SSet.{u}) ⟶
          (Δ[m + 3] : SSet.{u}))
  hornMap := standardTypeCHornLeg f
  hornMap_scaled := minimalScaling_map X.scaling (standardTypeCHornLeg f)

/-- A strict filler of the minimal outer horn is compatible with the original
collapsed-point leg on the edge `{0,1}`. -/
theorem standardTypeC_edge_compat_of_hornFiller
    {X : ScaledSSet.{u}}
    {m : Nat}
    (f : standardTypeCSource m ⟶ X)
    (Q : ScaledHornFiller (standardTypeCMinimalHornProblem f)) :
    standardTypeCEdgeToSimplex m ≫ Q.simplexMap =
      standardTypeCEdgeCollapseToPoint m ≫ standardTypeCPointLeg f := by
  calc
    standardTypeCEdgeToSimplex m ≫ Q.simplexMap =
        standardTypeCEdgeToHorn m ≫
          (standardTypeCMinimalHornProblem f).hornMap := by
      rw [Q.extends_horn]
      simp
    _ = standardTypeCEdgeToHorn m ≫
          (pushout.inl
              (standardTypeCEdgeToHorn m)
              (standardTypeCEdgeCollapseToPoint m) ≫ f.map) := rfl
    _ = standardTypeCEdgeCollapseToPoint m ≫
          (pushout.inr
              (standardTypeCEdgeToHorn m)
              (standardTypeCEdgeCollapseToPoint m) ≫ f.map) := by
      have h := congrArg
        (fun q :
            (standardTypeCEdgeFace m : SSet.{u}) ⟶
              standardTypeCSourceCarrier m => q ≫ f.map)
        (standardTypeCSource_edge_collapsed m)
      simpa [Category.assoc] using h
    _ = standardTypeCEdgeCollapseToPoint m ≫ standardTypeCPointLeg f := rfl

/-- Descend a strict outer-horn filler and the collapsed point leg through the
standard type-(C) target pushout. -/
def standardTypeCTargetMapOfHornFiller
    {X : ScaledSSet.{u}}
    {m : Nat}
    (f : standardTypeCSource m ⟶ X)
    (Q : ScaledHornFiller (standardTypeCMinimalHornProblem f)) :
    standardTypeCTargetCarrier m ⟶ X.carrier :=
  (standardTypeCTargetCarrier_isPushout m).desc
    Q.simplexMap
    (standardTypeCPointLeg f)
    (standardTypeC_edge_compat_of_hornFiller f Q)

@[simp, reassoc]
theorem standardTypeCTargetMapOfHornFiller_inl
    {X : ScaledSSet.{u}}
    {m : Nat}
    (f : standardTypeCSource m ⟶ X)
    (Q : ScaledHornFiller (standardTypeCMinimalHornProblem f)) :
    pushout.inl
        (standardTypeCEdgeToSimplex m)
        (standardTypeCEdgeCollapseToPoint m) ≫
      standardTypeCTargetMapOfHornFiller f Q = Q.simplexMap := by
  exact
    (standardTypeCTargetCarrier_isPushout m).inl_desc
      Q.simplexMap
      (standardTypeCPointLeg f)
      (standardTypeC_edge_compat_of_hornFiller f Q)

@[simp, reassoc]
theorem standardTypeCTargetMapOfHornFiller_inr
    {X : ScaledSSet.{u}}
    {m : Nat}
    (f : standardTypeCSource m ⟶ X)
    (Q : ScaledHornFiller (standardTypeCMinimalHornProblem f)) :
    pushout.inr
        (standardTypeCEdgeToSimplex m)
        (standardTypeCEdgeCollapseToPoint m) ≫
      standardTypeCTargetMapOfHornFiller f Q = standardTypeCPointLeg f := by
  exact
    (standardTypeCTargetCarrier_isPushout m).inr_desc
      Q.simplexMap
      (standardTypeCPointLeg f)
      (standardTypeC_edge_compat_of_hornFiller f Q)

/-- Under attachment fibrancy the descended type-(C) target map is scaled,
because the target scaling is maximal. -/
def standardTypeCLiftOfAttachmentFibrant
    {X : ScaledSSet.{u}}
    {m : Nat}
    (hX : IsAttachmentFibrant X)
    (f : standardTypeCSource m ⟶ X)
    (Q : ScaledHornFiller (standardTypeCMinimalHornProblem f)) :
    standardTypeCTarget m ⟶ X where
  map := standardTypeCTargetMapOfHornFiller f Q
  scaled := by
    intro t ht
    rw [attachmentFibrant_scaling_eq_maximal hX]
    exact ScaledSimplicialSet.maximal_thin X.carrier _

/-- The descended type-(C) lift restricts exactly to the original source map. -/
theorem standardTypeCLiftOfAttachmentFibrant_fac
    {X : ScaledSSet.{u}}
    {m : Nat}
    (hX : IsAttachmentFibrant X)
    (f : standardTypeCSource m ⟶ X)
    (Q : ScaledHornFiller (standardTypeCMinimalHornProblem f)) :
    standardTypeCGeneratorHom m ≫
        standardTypeCLiftOfAttachmentFibrant hX f Q = f := by
  apply ScaledSSet.ScaledMap.ext
  change
    standardTypeCCarrierMap m ≫
        standardTypeCTargetMapOfHornFiller f Q = f.map
  apply (standardTypeCSourceCarrier_isPushout m).hom_ext
  · calc
      pushout.inl
          (standardTypeCEdgeToHorn m)
          (standardTypeCEdgeCollapseToPoint m) ≫
          (standardTypeCCarrierMap m ≫
            standardTypeCTargetMapOfHornFiller f Q) =
        (pushout.inl
            (standardTypeCEdgeToHorn m)
            (standardTypeCEdgeCollapseToPoint m) ≫
          standardTypeCCarrierMap m) ≫
            standardTypeCTargetMapOfHornFiller f Q := by simp
      _ =
        ((Λ[m + 3, (0 : Fin (m + 4))].ι :
            (Λ[m + 3, (0 : Fin (m + 4))] : SSet.{u}) ⟶
              (Δ[m + 3] : SSet.{u})) ≫
          pushout.inl
            (standardTypeCEdgeToSimplex m)
            (standardTypeCEdgeCollapseToPoint m)) ≫
            standardTypeCTargetMapOfHornFiller f Q := by
              rw [standardTypeCCarrierMap_inl_horn]
      _ =
        (Λ[m + 3, (0 : Fin (m + 4))].ι :
            (Λ[m + 3, (0 : Fin (m + 4))] : SSet.{u}) ⟶
              (Δ[m + 3] : SSet.{u})) ≫
          (pushout.inl
              (standardTypeCEdgeToSimplex m)
              (standardTypeCEdgeCollapseToPoint m) ≫
            standardTypeCTargetMapOfHornFiller f Q) := by simp
      _ =
        (Λ[m + 3, (0 : Fin (m + 4))].ι :
            (Λ[m + 3, (0 : Fin (m + 4))] : SSet.{u}) ⟶
              (Δ[m + 3] : SSet.{u})) ≫ Q.simplexMap := by
              rw [standardTypeCTargetMapOfHornFiller_inl]
      _ = (standardTypeCMinimalHornProblem f).hornMap :=
        Q.extends_horn.symm
      _ =
        pushout.inl
            (standardTypeCEdgeToHorn m)
            (standardTypeCEdgeCollapseToPoint m) ≫ f.map := rfl
  · calc
      pushout.inr
          (standardTypeCEdgeToHorn m)
          (standardTypeCEdgeCollapseToPoint m) ≫
          (standardTypeCCarrierMap m ≫
            standardTypeCTargetMapOfHornFiller f Q) =
        (pushout.inr
            (standardTypeCEdgeToHorn m)
            (standardTypeCEdgeCollapseToPoint m) ≫
          standardTypeCCarrierMap m) ≫
            standardTypeCTargetMapOfHornFiller f Q := by simp
      _ =
        pushout.inr
            (standardTypeCEdgeToSimplex m)
            (standardTypeCEdgeCollapseToPoint m) ≫
          standardTypeCTargetMapOfHornFiller f Q := by
            rw [standardTypeCCarrierMap_inr_point]
      _ = standardTypeCPointLeg f :=
        standardTypeCTargetMapOfHornFiller_inr f Q
      _ =
        pushout.inr
            (standardTypeCEdgeToHorn m)
            (standardTypeCEdgeCollapseToPoint m) ≫ f.map := rfl

/-- Every standard type-(C) generator has terminal RLP against an
attachment-fibrant target. -/
theorem attachmentFibrant_hasLiftingProperty_standardTypeC
    {X : ScaledSSet.{u}}
    (hX : IsAttachmentFibrant X)
    (m : Nat) :
    HasLiftingProperty
      (standardTypeCGeneratorHom m)
      (ScaledSSet.toPoint X) := by
  apply
    (ScaledSSet.hasLiftingProperty_toPoint_iff
      (standardTypeCGeneratorHom m)).2
  intro f
  rcases
      attachmentFibrant_hornFiller_of_two_le
        hX (standardTypeCMinimalHornProblem f) (by omega) with
    ⟨Q⟩
  exact
    ⟨standardTypeCLiftOfAttachmentFibrant hX f Q,
      standardTypeCLiftOfAttachmentFibrant_fac hX f Q⟩

/-! ## Assemble the complete standard A/B/C terminal right class -/

/-- Type-(B) terminal RLP follows from its already-proved membership in the
canonical generated left class. -/
theorem attachmentFibrant_hasLiftingProperty_standardTypeB
    {X : ScaledSSet.{u}}
    (hX : IsAttachmentFibrant X) :
    HasLiftingProperty
      standardTypeBGeneratorHom
      (ScaledSSet.toPoint X) :=
  attachmentFibrant_hasLiftingProperty_of_canonicalGenerated
    hX standardTypeBGeneratorHom standardTypeBGenerator_mem_canonicalGenerated

/-- Every canonical attachment-fibrant object is right-orthogonal to all
literal standard A/B/C generators. -/
theorem attachmentFibrant_standardABC_generators_rlp
    {X : ScaledSSet.{u}}
    (hX : IsAttachmentFibrant X) :
    standardGeneratedScaledFibrationABC (ScaledSSet.toPoint X) := by
  intro A B j hj
  rcases hj with (hjA | hjB) | hjC
  · dsimp [standardTypeAScaledHornGenerators] at hjA
    cases hjA with
    | mk g =>
        exact attachmentFibrant_hasStandardTypeATerminalRLP_unconditional hX g
  · dsimp [standardTypeBScaledAnodyneGenerators] at hjB
    cases hjB with
    | mk unitIndex =>
        cases unitIndex
        exact attachmentFibrant_hasLiftingProperty_standardTypeB hX
  · dsimp [standardTypeCScaledAnodyneGenerators] at hjC
    cases hjC with
    | mk m =>
        exact attachmentFibrant_hasLiftingProperty_standardTypeC hX m

/-- Passing from standard generators to their `rlp.llp` closure does not change
the terminal right class. -/
theorem attachmentFibrant_standardGeneratedABC_rlp
    {X : ScaledSSet.{u}}
    (hX : IsAttachmentFibrant X) :
    (standardGeneratedScaledAnodyneABC :
      MorphismProperty (ScaledSSet.{u})).rlp
      (ScaledSSet.toPoint X) := by
  change
    ((standardScaledAnodyneGeneratorsABC :
      MorphismProperty (ScaledSSet.{u})).rlp.llp).rlp
      (ScaledSSet.toPoint X)
  rw [MorphismProperty.rlp_llp_rlp]
  exact attachmentFibrant_standardABC_generators_rlp hX

/-- Object-level fibrancy for the complete standard A/B/C generated
presentation. -/
def IsStandardABCFibrant (X : ScaledSSet.{u}) : Prop :=
  (standardGeneratedScaledAnodyneABC :
    MorphismProperty (ScaledSSet.{u})).rlp
    (ScaledSSet.toPoint X)

/-- Canonical attachment fibrancy is semantically stronger than standard A/B/C
fibrancy on every universe level. -/
theorem attachmentFibrant_implies_standardABCFibrant
    {X : ScaledSSet.{u}}
    (hX : IsAttachmentFibrant X) :
    IsStandardABCFibrant X :=
  attachmentFibrant_standardGeneratedABC_rlp hX

/-! ## Concrete strictness witness and semantic order -/

/-- The existing `B^2 N` witness is standard A/B/C fibrant. -/
theorem natDoubleDelooping_isStandardABCFibrant :
    IsStandardABCFibrant natDoubleDeloopingScaledDuskin := by
  exact natDoubleDelooping_standardGeneratedABC_rlp

/-- The same object is not canonically attachment-fibrant, by the atomic
2-simplex orthogonality separator. -/
theorem natDoubleDelooping_not_attachmentFibrant :
    ¬ IsAttachmentFibrant natDoubleDeloopingScaledDuskin := by
  intro hX
  apply atomicTwoSimplexEnrichment_not_hasLiftingProperty_natDoubleDeloopingTerminal
  exact
    attachmentFibrant_hasLiftingProperty_of_canonicalGenerated
      hX atomicTwoSimplexEnrichment
      atomicTwoSimplexEnrichment_mem_canonicalGenerated

/-- Canonical fibrant-object semantics is strictly contained in standard A/B/C
fibrant-object semantics: inclusion holds for every object, and `B^2 N` is a
concrete object in the difference. -/
theorem canonicalFibrantObjects_strictlyContainedIn_standardABCFibrantObjects :
    (∀ X : ScaledSSet,
      IsAttachmentFibrant X → IsStandardABCFibrant X) ∧
    (∃ X : ScaledSSet,
      IsStandardABCFibrant X ∧ ¬ IsAttachmentFibrant X) := by
  constructor
  · intro X hX
    exact attachmentFibrant_implies_standardABCFibrant hX
  · exact
      ⟨natDoubleDeloopingScaledDuskin,
        natDoubleDelooping_isStandardABCFibrant,
        natDoubleDelooping_not_attachmentFibrant⟩

/-!
The semantic comparison is now unconditional:

```text
canonical attachment fibrancy
  -> maximal target scaling                         -- v1.91
  -> every n >= 2 horn has a homotopy-class filler -- v1.114 contraction
  -> every n >= 2 horn has a strict filler          -- canonical terminal RLP

therefore:
  type A terminal RLP                              -- v1.114
  type B terminal RLP                              -- canonical membership
  type C terminal RLP                              -- outer horn + pushout descent
  -> standard A/B/C generated terminal RLP

and concretely:
  B^2 N -> * is standard A/B/C-right               -- v1.106
  B^2 N -> * is not canonical-right                -- atomic separator

hence:
  Fib_canonical  is strictly contained in  Fib_standardABC.
```

This does not reverse the already-proved left-class separation and does not
assert `standardGeneratedScaledAnodyneABC <= canonicalGeneratedScaledAnodyne`.
The remaining presentation-level type-(A)/(C) reverse geometry is therefore a
strictly finer problem than fibrant-object comparison.
-/

end KUOS.DependentOriginationCanonicalStandardABCFibrantObjectStrictOrderV1_115
