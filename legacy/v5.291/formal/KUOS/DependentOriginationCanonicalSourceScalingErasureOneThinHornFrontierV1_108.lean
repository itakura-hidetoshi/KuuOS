import KUOS.DependentOriginationPresentationIndependentSeparationTypeBReverseV1_107

namespace KUOS.DependentOriginationCanonicalSourceScalingErasureOneThinHornFrontierV1_108

open CategoryTheory
open CategoryTheory.Category
open CategoryTheory.Limits
open Opposite
open Simplicial
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationScaledTerminalRLPV1_41
open KUOS.DependentOriginationScaledAnodyneGeneratorClosureV1_42
open KUOS.DependentOriginationScaledAnodyneAttachmentFactorizationV1_48
open KUOS.DependentOriginationStandardTypeAScaledHornFamilyV1_49
open KUOS.DependentOriginationStandardTypeAEndpointPushoutProductV1_50
open KUOS.DependentOriginationStandardTypeBScalingPushoutV1_56
open KUOS.DependentOriginationStandardTypeCCollapsedEdgeV1_58
open KUOS.DependentOriginationCanonicalEndpointLeibnizEpiDescentV1_82
open KUOS.DependentOriginationCanonicalFibrationThinReflectionV1_92
open KUOS.DependentOriginationPresentationIndependentSeparationTypeBReverseV1_107

universe u

/-!
# Canonical source-scaling erasure and the common one-thin horn frontier v1.108

Version v1.107 closed the standard type-(B) reverse comparison and left the
standard type-(A) and type-(C) families as the genuine geometric frontier.
The apparent source scalings of those two families are not, however, part of
that frontier.

The canonical right class reflects thin two-simplices.  Consequently a square
against *any* identity-underlying scaling enlargement

```text
(X, s₁) --> (X, s₂),     s₁ <= s₂,
```

has a lift against every canonical-right map: reuse the underlying upper map;
for every `s₂`-thin triangle, commutativity makes its image thin downstairs and
thinness reflection makes it thin upstairs.  Thus every scaling enlargement on
an arbitrary simplicial carrier, not only on a standard simplex, already lies
in the canonical generated left class.

This has a useful exact consequence.  For a fixed underlying simplicial map
`f : X -> Y` and fixed target scaling, canonical-generated membership is
independent of the chosen source scaling.  One may replace the source scaling
by the minimal scaling without changing membership.  The forward implication
uses closure under composition with the canonical source enrichment; the
reverse implication is epi right-factor descent through the identity-underlying
source enrichment.

We then apply this source-scaling erasure to the two remaining standard
families:

* type-(A) reverse membership is equivalent to the same inner horn inclusion
  with minimal source scaling and the standard one-distinguished-triangle
  target scaling;
* type-(C) reverse membership is equivalent to the same collapsed-edge carrier
  map with minimal source scaling and its one-distinguished-triangle target
  scaling.

For type-(C), the collapse itself is also formal rather than new horn geometry.
If the uncollapsed outer horn

```text
Lambda[ m+3, 0 ] --> Delta[m+3]
```

with minimal source scaling and the single target-thin triangle `01n` is
canonical-generated, then its cobase descent along the edge collapse gives the
minimal-source type-(C) generator.  Restoring the original source scaling is
then automatic by source-scaling erasure.

Therefore the post-v1.107 reverse problem has one common mathematical core:
minimal-source horn inclusions into a simplex carrying one distinguished thin
triangle.  Type-(A) is the inner consecutive-triangle family; type-(C) is the
outer `01n` family followed by edge-collapse descent.  Type-(B) is already
closed.

This file deliberately does not assert that those one-thin horn maps are
canonical-generated.  That is now the irreducible reverse-geometry question.
-/

/-! ## Every arbitrary-carrier scaling enlargement is canonical-generated -/

/-- Minimal scaling is contained in every scaling on the same simplicial
carrier. -/
theorem minimalScaling_le_any
    {X : SSet.{u}}
    (sX : ScaledSimplicialSet X) :
    ScalingLE (minimalScaling X) sX := by
  intro t ht
  rcases ht with ⟨x, rfl⟩ | ⟨x, rfl⟩
  · exact sX.thin_sigma_zero x
  · exact sX.thin_sigma_one x

/-- An identity-underlying scaling enlargement is an epimorphism in
`ScaledSSet`. -/
instance scalingEnrichmentHom_epi
    {X : SSet.{u}}
    {s₁ s₂ : ScaledSimplicialSet X}
    (h₁₂ : ScalingLE s₁ s₂) :
    Epi (scalingEnrichmentHom h₁₂) where
  left_cancellation := by
    intro Z f g h
    apply ScaledSSet.ScaledMap.ext
    have hmap := congrArg ScaledSSet.ScaledMap.map h
    simpa [scalingEnrichmentHom] using hmap

/-- Thinness reflection gives RLP against an arbitrary identity-underlying
scaling enlargement on an arbitrary simplicial carrier. -/
theorem hasLiftingProperty_scalingEnrichment_of_reflectsThinTwoSimplices
    {K : SSet.{u}}
    {s₁ s₂ : ScaledSimplicialSet K}
    (h₁₂ : ScalingLE s₁ s₂)
    {X Y : ScaledSSet.{u}}
    (p : X ⟶ Y)
    (hreflect : ReflectsThinTwoSimplices p) :
    HasLiftingProperty (scalingEnrichmentHom h₁₂) p := by
  refine ⟨?_⟩
  intro f g sq
  have hsqmap : f.map ≫ p.map = g.map := by
    have hmap := congrArg ScaledSSet.ScaledMap.map sq.w
    simpa [scalingEnrichmentHom] using hmap
  let l : ScaledSSet.of K s₂ ⟶ X :=
    { map := f.map
      scaled := by
        intro t ht
        apply hreflect (f.map.app (op ⦋2⦌) t)
        have hthin := g.scaled t ht
        rw [← hsqmap] at hthin
        simpa using hthin }
  exact CommSq.HasLift.mk'
    { l := l
      fac_left := by
        apply ScaledSSet.ScaledMap.ext
        simp [l, scalingEnrichmentHom]
      fac_right := by
        apply ScaledSSet.ScaledMap.ext
        simpa [l] using hsqmap }

/-- Every scaling enlargement on every simplicial carrier lies in the
canonical generated left class.  This strictly generalizes the standard-simplex
specialization used for type-(B) in v1.107. -/
theorem arbitraryCarrierScalingEnrichment_mem_canonicalGenerated
    {K : SSet.{u}}
    {s₁ s₂ : ScaledSimplicialSet K}
    (h₁₂ : ScalingLE s₁ s₂) :
    (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u}))
      (scalingEnrichmentHom h₁₂) := by
  change
    (scaledHornAttachmentGenerators : MorphismProperty (ScaledSSet.{u})).rlp.llp
      (scalingEnrichmentHom h₁₂)
  intro X Y p hp
  exact
    hasLiftingProperty_scalingEnrichment_of_reflectsThinTwoSimplices
      h₁₂ p (canonicalAttachmentRight_reflectsThinTwoSimplices hp)

/-! ## Canonical generated membership forgets source scaling -/

/-- Repackage a scaled map with the same underlying simplicial map but minimal
source scaling. -/
def withMinimalSource
    {X Y : SSet.{u}}
    {sX : ScaledSimplicialSet X}
    {sY : ScaledSimplicialSet Y}
    (f : ScaledSSet.of X sX ⟶ ScaledSSet.of Y sY) :
    ScaledSSet.of X (minimalScaling X) ⟶ ScaledSSet.of Y sY where
  map := f.map
  scaled := minimalScaling_map sY f.map

/-- The minimal-source version factors through the source scaling enrichment
exactly. -/
theorem scalingEnrichmentToSource_comp_original
    {X Y : SSet.{u}}
    {sX : ScaledSimplicialSet X}
    {sY : ScaledSimplicialSet Y}
    (f : ScaledSSet.of X sX ⟶ ScaledSSet.of Y sY) :
    scalingEnrichmentHom (minimalScaling_le_any sX) ≫ f =
      withMinimalSource f := by
  apply ScaledSSet.ScaledMap.ext
  simp [scalingEnrichmentHom, withMinimalSource]

/-- If the original scaled map is canonical-generated, then so is its
minimal-source version: prepend the canonical source scaling enrichment. -/
theorem withMinimalSource_mem_canonicalGenerated_of_mem
    {X Y : SSet.{u}}
    {sX : ScaledSimplicialSet X}
    {sY : ScaledSimplicialSet Y}
    (f : ScaledSSet.of X sX ⟶ ScaledSSet.of Y sY)
    (hf :
      (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u})) f) :
    (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u}))
      (withMinimalSource f) := by
  rw [← scalingEnrichmentToSource_comp_original f]
  exact MorphismProperty.comp_mem
    (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u}))
    _ _
    (arbitraryCarrierScalingEnrichment_mem_canonicalGenerated
      (minimalScaling_le_any sX))
    hf

/-- Conversely, canonical membership of the minimal-source version descends
through the epi identity enrichment to the original source scaling. -/
theorem mem_canonicalGenerated_of_withMinimalSource_mem
    {X Y : SSet.{u}}
    {sX : ScaledSimplicialSet X}
    {sY : ScaledSimplicialSet Y}
    (f : ScaledSSet.of X sX ⟶ ScaledSSet.of Y sY)
    (hmin :
      (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u}))
        (withMinimalSource f)) :
    (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u})) f := by
  change
    (scaledHornAttachmentGenerators : MorphismProperty (ScaledSSet.{u})).rlp.llp f
  apply llp_mem_of_epi_precomp
    ((scaledHornAttachmentGenerators : MorphismProperty (ScaledSSet.{u})).rlp)
    (scalingEnrichmentHom (minimalScaling_le_any sX))
    f
  rw [scalingEnrichmentToSource_comp_original]
  exact hmin

/-- Exact source-scaling erasure: for fixed underlying map and target scaling,
canonical-generated membership is independent of the source scaling. -/
theorem mem_canonicalGenerated_iff_withMinimalSource
    {X Y : SSet.{u}}
    {sX : ScaledSimplicialSet X}
    {sY : ScaledSimplicialSet Y}
    (f : ScaledSSet.of X sX ⟶ ScaledSSet.of Y sY) :
    (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u})) f ↔
      (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u}))
        (withMinimalSource f) := by
  constructor
  · exact withMinimalSource_mem_canonicalGenerated_of_mem f
  · exact mem_canonicalGenerated_of_withMinimalSource_mem f

/-! ## Type-(A): remove the horn source scaling exactly -/

/-- The standard type-(A) horn inclusion with minimal source scaling and the
unchanged standard target scaling. -/
def standardTypeAMinimalSourceHornHom
    (g : StandardTypeAHornGeneratorIndex) :
    ScaledSSet.of (Λ[g.n, g.i] : SSet.{u})
        (minimalScaling (Λ[g.n, g.i] : SSet.{u})) ⟶
      standardTypeAScaledSimplex g where
  map := Λ[g.n, g.i].ι
  scaled := minimalScaling_map _ _

/-- The minimal-source map is literally the source-erased form of the standard
type-(A) generator. -/
theorem standardTypeA_withMinimalSource_eq
    (g : StandardTypeAHornGeneratorIndex) :
    withMinimalSource (standardTypeAScaledHornGeneratorHom g) =
      standardTypeAMinimalSourceHornHom g := by
  apply ScaledSSet.ScaledMap.ext
  rfl

/-- Type-(A) reverse membership is exactly the minimal-source one-thin inner
horn problem. -/
theorem standardTypeA_mem_canonicalGenerated_iff_minimalSource
    (g : StandardTypeAHornGeneratorIndex) :
    (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u}))
        (standardTypeAScaledHornGeneratorHom g) ↔
      (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u}))
        (standardTypeAMinimalSourceHornHom g) := by
  rw [mem_canonicalGenerated_iff_withMinimalSource]
  rw [standardTypeA_withMinimalSource_eq]

/-! ## Type-(C): remove source scaling and isolate the uncollapsed outer horn -/

/-- The type-(C) collapsed-edge carrier map with minimal source scaling and the
unchanged one-distinguished-triangle target scaling. -/
def standardTypeCMinimalSourceGeneratorHom
    (m : Nat) :
    ScaledSSet.of (standardTypeCSourceCarrier m)
        (minimalScaling (standardTypeCSourceCarrier m)) ⟶
      standardTypeCTarget m where
  map := standardTypeCCarrierMap m
  scaled := minimalScaling_map _ _

/-- The minimal-source collapsed map is the source-erased standard type-(C)
generator. -/
theorem standardTypeC_withMinimalSource_eq
    (m : Nat) :
    withMinimalSource (standardTypeCGeneratorHom m) =
      standardTypeCMinimalSourceGeneratorHom m := by
  apply ScaledSSet.ScaledMap.ext
  rfl

/-- Type-(C) reverse membership is exactly equivalent to its minimal-source
collapsed form. -/
theorem standardTypeC_mem_canonicalGenerated_iff_minimalSource
    (m : Nat) :
    (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u}))
        (standardTypeCGeneratorHom m) ↔
      (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u}))
        (standardTypeCMinimalSourceGeneratorHom m) := by
  rw [mem_canonicalGenerated_iff_withMinimalSource]
  rw [standardTypeC_withMinimalSource_eq]

/-- On the uncollapsed simplex, mark exactly the type-(C) distinguished `01n`
triangle in addition to the minimal scaling. -/
def standardTypeCUncollapsedTargetScaling
    (m : Nat) : ScaledSimplicialSet (Δ[m + 3] : SSet.{u}) :=
  minimalPlusTriangleScaling (standardTypeCTriangle01n m)

/-- The common outer-horn core of type-(C): minimal source scaling, one-thin
simplex target. -/
def standardTypeCOuterOneThinHornHom
    (m : Nat) :
    ScaledSSet.of
        (Λ[m + 3, (0 : Fin (m + 4))] : SSet.{u})
        (minimalScaling (Λ[m + 3, (0 : Fin (m + 4))] : SSet.{u})) ⟶
      ScaledSSet.of (Δ[m + 3] : SSet.{u})
        (standardTypeCUncollapsedTargetScaling m) where
  map := Λ[m + 3, (0 : Fin (m + 4))].ι
  scaled := minimalScaling_map _ _

/-- The simplex leg into the collapsed type-(C) target preserves the one-thin
scaling: minimal triangles are automatic, and `01n` maps to the distinguished
thin target triangle. -/
def standardTypeCUncollapsedToTarget
    (m : Nat) :
    ScaledSSet.of (Δ[m + 3] : SSet.{u})
        (standardTypeCUncollapsedTargetScaling m) ⟶
      standardTypeCTarget m where
  map :=
    pushout.inl
      (standardTypeCEdgeToSimplex m)
      (standardTypeCEdgeCollapseToPoint m)
  scaled := by
    intro t ht
    rcases ht with hmin | hdist
    · exact
        (minimalScaling_map
          (standardTypeCTargetScaling m)
          (pushout.inl
            (standardTypeCEdgeToSimplex m)
            (standardTypeCEdgeCollapseToPoint m))) t hmin
    · subst t
      exact standardTypeCTarget_distinguished_thin m

/-- Restrict a map out of the minimal-source collapsed type-(C) source to its
horn leg. -/
def standardTypeCMinimalSourceHornLeg
    {m : Nat}
    {X : ScaledSSet.{u}}
    (f :
      ScaledSSet.of (standardTypeCSourceCarrier m)
          (minimalScaling (standardTypeCSourceCarrier m)) ⟶ X) :
    ScaledSSet.of
        (Λ[m + 3, (0 : Fin (m + 4))] : SSet.{u})
        (minimalScaling (Λ[m + 3, (0 : Fin (m + 4))] : SSet.{u})) ⟶ X where
  map :=
    pushout.inl
      (standardTypeCEdgeToHorn m)
      (standardTypeCEdgeCollapseToPoint m) ≫ f.map
  scaled := minimalScaling_map _ _

/-- Restrict a map out of the minimal-source collapsed type-(C) source to its
collapsed point leg. -/
def standardTypeCMinimalSourcePointLeg
    {m : Nat}
    {X : ScaledSSet.{u}}
    (f :
      ScaledSSet.of (standardTypeCSourceCarrier m)
          (minimalScaling (standardTypeCSourceCarrier m)) ⟶ X) :
    ScaledSSet.of (Δ[0] : SSet.{u}) (minimalScaling (Δ[0] : SSet.{u})) ⟶ X where
  map :=
    pushout.inr
      (standardTypeCEdgeToHorn m)
      (standardTypeCEdgeCollapseToPoint m) ≫ f.map
  scaled := minimalScaling_map _ _

/-- The simplex leg of a map out of the type-(C) target, before the edge
collapse. -/
def standardTypeCTargetSimplexLeg
    {m : Nat}
    {Y : ScaledSSet.{u}}
    (g : standardTypeCTarget m ⟶ Y) :
    ScaledSSet.of (Δ[m + 3] : SSet.{u})
        (standardTypeCUncollapsedTargetScaling m) ⟶ Y :=
  standardTypeCUncollapsedToTarget m ≫ g

/-- The horn-restricted top and simplex bottom maps form a square against the
uncollapsed one-thin outer horn whenever the original collapsed square
commutes. -/
theorem standardTypeC_outer_square_commutes
    {m : Nat}
    {X Y : ScaledSSet.{u}}
    (p : X ⟶ Y)
    (f :
      ScaledSSet.of (standardTypeCSourceCarrier m)
          (minimalScaling (standardTypeCSourceCarrier m)) ⟶ X)
    (g : standardTypeCTarget m ⟶ Y)
    (w : standardTypeCMinimalSourceGeneratorHom m ≫ g = f ≫ p) :
    standardTypeCMinimalSourceHornLeg f ≫ p =
      standardTypeCOuterOneThinHornHom m ≫
        standardTypeCTargetSimplexLeg g := by
  apply ScaledSSet.ScaledMap.ext
  have hw := congrArg ScaledSSet.ScaledMap.map w
  change
    (pushout.inl
        (standardTypeCEdgeToHorn m)
        (standardTypeCEdgeCollapseToPoint m) ≫ f.map) ≫ p.map =
      (Λ[m + 3, (0 : Fin (m + 4))].ι :
          (Λ[m + 3, (0 : Fin (m + 4))] : SSet.{u}) ⟶
            (Δ[m + 3] : SSet.{u})) ≫
        (pushout.inl
            (standardTypeCEdgeToSimplex m)
            (standardTypeCEdgeCollapseToPoint m) ≫ g.map)
  rw [← Category.assoc, ← hw]
  simp [standardTypeCMinimalSourceGeneratorHom,
    standardTypeCCarrierMap_inl_horn, Category.assoc]

/-- A lift of the uncollapsed one-thin outer-horn square descends through the
collapsed target pushout to a lift of the minimal-source type-(C) square. -/
theorem hasLiftingProperty_standardTypeCMinimalSource_of_outerOneThin
    (m : Nat)
    {X Y : ScaledSSet.{u}}
    (p : X ⟶ Y)
    (houter : HasLiftingProperty (standardTypeCOuterOneThinHornHom m) p) :
    HasLiftingProperty (standardTypeCMinimalSourceGeneratorHom m) p := by
  refine ⟨?_⟩
  intro f g sq
  let outerSq : CommSq
      (standardTypeCMinimalSourceHornLeg f)
      (standardTypeCOuterOneThinHornHom m)
      p
      (standardTypeCTargetSimplexLeg g) :=
    { w := standardTypeC_outer_square_commutes p f g sq.w }
  rcases (houter.sq_hasLift outerSq).exists_lift with ⟨L⟩
  let pointLeg := standardTypeCMinimalSourcePointLeg f
  have hedge :
      standardTypeCEdgeToSimplex m ≫ L.l.map =
        standardTypeCEdgeCollapseToPoint m ≫ pointLeg.map := by
    calc
      standardTypeCEdgeToSimplex m ≫ L.l.map =
          standardTypeCEdgeToHorn m ≫
            ((Λ[m + 3, (0 : Fin (m + 4))].ι :
                (Λ[m + 3, (0 : Fin (m + 4))] : SSet.{u}) ⟶
                  (Δ[m + 3] : SSet.{u})) ≫ L.l.map) := by
            rw [← standardTypeCEdgeToHorn_comp_hornInclusion]
            simp
      _ = standardTypeCEdgeToHorn m ≫
          (standardTypeCMinimalSourceHornLeg f).map := by
            have hleft := congrArg ScaledSSet.ScaledMap.map L.fac_left
            simpa [standardTypeCOuterOneThinHornHom] using
              congrArg (fun q => standardTypeCEdgeToHorn m ≫ q) hleft
      _ = standardTypeCEdgeCollapseToPoint m ≫ pointLeg.map := by
            have hcollapsed := congrArg
              (fun q :
                  (standardTypeCEdgeFace m : SSet.{u}) ⟶
                    standardTypeCSourceCarrier m => q ≫ f.map)
              (standardTypeCSource_edge_collapsed m)
            simpa [standardTypeCMinimalSourceHornLeg,
              standardTypeCMinimalSourcePointLeg, pointLeg,
              Category.assoc] using hcollapsed
  let liftMap : standardTypeCTargetCarrier m ⟶ X.carrier :=
    (standardTypeCTargetCarrier_isPushout m).desc
      L.l.map pointLeg.map hedge
  have hinl :
      pushout.inl
          (standardTypeCEdgeToSimplex m)
          (standardTypeCEdgeCollapseToPoint m) ≫ liftMap = L.l.map := by
    exact (standardTypeCTargetCarrier_isPushout m).inl_desc
      L.l.map pointLeg.map hedge
  have hinr :
      pushout.inr
          (standardTypeCEdgeToSimplex m)
          (standardTypeCEdgeCollapseToPoint m) ≫ liftMap = pointLeg.map := by
    exact (standardTypeCTargetCarrier_isPushout m).inr_desc
      L.l.map pointLeg.map hedge
  let lift : standardTypeCTarget m ⟶ X :=
    { map := liftMap
      scaled := by
        intro t ht
        rcases ht with hmin | hdist
        · exact (minimalScaling_map X.scaling liftMap) t hmin
        · subst t
          have hpoint := ConcreteCategory.congr_hom
            (congr_app hinl (op ⦋2⦌)) (standardTypeCTriangle01n m)
          change X.scaling.thin
            (liftMap.app (op ⦋2⦌)
              ((pushout.inl
                (standardTypeCEdgeToSimplex m)
                (standardTypeCEdgeCollapseToPoint m)).app
                  (op ⦋2⦌) (standardTypeCTriangle01n m)))
          rw [hpoint]
          exact L.l.scaled _ (Or.inr rfl) }
  exact CommSq.HasLift.mk'
    { l := lift
      fac_left := by
        apply ScaledSSet.ScaledMap.ext
        apply (standardTypeCSourceCarrier_isPushout m).hom_ext
        · calc
            pushout.inl
                (standardTypeCEdgeToHorn m)
                (standardTypeCEdgeCollapseToPoint m) ≫
                (standardTypeCMinimalSourceGeneratorHom m).map ≫ liftMap =
              (Λ[m + 3, (0 : Fin (m + 4))].ι :
                  (Λ[m + 3, (0 : Fin (m + 4))] : SSet.{u}) ⟶
                    (Δ[m + 3] : SSet.{u})) ≫
                (pushout.inl
                    (standardTypeCEdgeToSimplex m)
                    (standardTypeCEdgeCollapseToPoint m) ≫ liftMap) := by
                  simp [standardTypeCMinimalSourceGeneratorHom,
                    standardTypeCCarrierMap_inl_horn, Category.assoc]
            _ =
              (Λ[m + 3, (0 : Fin (m + 4))].ι :
                  (Λ[m + 3, (0 : Fin (m + 4))] : SSet.{u}) ⟶
                    (Δ[m + 3] : SSet.{u})) ≫ L.l.map := by rw [hinl]
            _ = (standardTypeCMinimalSourceHornLeg f).map := by
              have hleft := congrArg ScaledSSet.ScaledMap.map L.fac_left
              simpa [standardTypeCOuterOneThinHornHom] using hleft
            _ = pushout.inl
                (standardTypeCEdgeToHorn m)
                (standardTypeCEdgeCollapseToPoint m) ≫ f.map := rfl
        · calc
            pushout.inr
                (standardTypeCEdgeToHorn m)
                (standardTypeCEdgeCollapseToPoint m) ≫
                (standardTypeCMinimalSourceGeneratorHom m).map ≫ liftMap =
              pushout.inr
                  (standardTypeCEdgeToSimplex m)
                  (standardTypeCEdgeCollapseToPoint m) ≫ liftMap := by
                simp [standardTypeCMinimalSourceGeneratorHom,
                  standardTypeCCarrierMap_inr_point, Category.assoc]
            _ = pointLeg.map := hinr
            _ = pushout.inr
                (standardTypeCEdgeToHorn m)
                (standardTypeCEdgeCollapseToPoint m) ≫ f.map := rfl
      fac_right := by
        apply ScaledSSet.ScaledMap.ext
        apply (standardTypeCTargetCarrier_isPushout m).hom_ext
        · have hright := congrArg ScaledSSet.ScaledMap.map L.fac_right
          calc
            pushout.inl
                (standardTypeCEdgeToSimplex m)
                (standardTypeCEdgeCollapseToPoint m) ≫ liftMap ≫ p.map =
              L.l.map ≫ p.map := by rw [hinl]
            _ = (standardTypeCTargetSimplexLeg g).map := hright
            _ = pushout.inl
                (standardTypeCEdgeToSimplex m)
                (standardTypeCEdgeCollapseToPoint m) ≫ g.map := rfl
        · have hw := congrArg ScaledSSet.ScaledMap.map sq.w
          calc
            pushout.inr
                (standardTypeCEdgeToSimplex m)
                (standardTypeCEdgeCollapseToPoint m) ≫ liftMap ≫ p.map =
              pointLeg.map ≫ p.map := by rw [hinr]
            _ =
              pushout.inr
                  (standardTypeCEdgeToHorn m)
                  (standardTypeCEdgeCollapseToPoint m) ≫ f.map ≫ p.map := rfl
            _ =
              pushout.inr
                  (standardTypeCEdgeToHorn m)
                  (standardTypeCEdgeCollapseToPoint m) ≫
                (standardTypeCMinimalSourceGeneratorHom m).map ≫ g.map := by
                  rw [← hw]
            _ = pushout.inr
                (standardTypeCEdgeToSimplex m)
                (standardTypeCEdgeCollapseToPoint m) ≫ g.map := by
                  simp [standardTypeCMinimalSourceGeneratorHom,
                    standardTypeCCarrierMap_inr_point, Category.assoc] }

/-- Canonical generation of the uncollapsed one-thin outer horn implies
canonical generation of the actual standard type-(C) collapsed-edge generator. -/
theorem standardTypeC_mem_canonicalGenerated_of_outerOneThin
    (m : Nat)
    (houter :
      (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u}))
        (standardTypeCOuterOneThinHornHom m)) :
    (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u}))
      (standardTypeCGeneratorHom m) := by
  apply (standardTypeC_mem_canonicalGenerated_iff_minimalSource m).2
  change
    (scaledHornAttachmentGenerators : MorphismProperty (ScaledSSet.{u})).rlp.llp
      (standardTypeCMinimalSourceGeneratorHom m)
  intro X Y p hp
  apply hasLiftingProperty_standardTypeCMinimalSource_of_outerOneThin m p
  exact houter p hp

/-! ## The common reverse frontier after type-(B) -/

/-- Sufficient common horn data for the entire standard A/B/C reverse
comparison: minimal-source type-(A) inner horns and uncollapsed type-(C) outer
one-thin horns.  Type-(B) is filled by v1.107. -/
def standardABCCanonicalGeneratorwiseReverseComparison_of_oneThinHorns
    (hA :
      ∀ g : StandardTypeAHornGeneratorIndex,
        (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u}))
          (standardTypeAMinimalSourceHornHom g))
    (hC :
      ∀ m : Nat,
        (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u}))
          (standardTypeCOuterOneThinHornHom m)) :
    StandardABCCanonicalGeneratorwiseReverseComparison.{u} :=
  standardABCCanonicalGeneratorwiseReverseComparison_of_typeAC
    (fun g =>
      (standardTypeA_mem_canonicalGenerated_iff_minimalSource g).2 (hA g))
    (fun m => standardTypeC_mem_canonicalGenerated_of_outerOneThin m (hC m))

/-!
The reverse-comparison geometry has therefore been compressed without assuming
its answer:

```text
all source-scaling enrichments on arbitrary carriers
  ⊂ canonicalGenerated

canonical membership of f
  <-> canonical membership of the same underlying f with minimal source

standard type-B
  closed in v1.107

standard type-A
  <-> minimal-source inner horn -> one-thin simplex

standard type-C
  <-> minimal-source collapsed outer horn
  <- uncollapsed minimal-source outer horn -> one-thin simplex
     by native edge-collapse pushout descent

Hence the remaining sufficient common frontier is

  inner consecutive one-thin horns (A)
  outer 01n one-thin horns (C).
```

The old contraction/retract idea is not smuggled back in: the canonical
cylinder target still contains mixed thin triangles whose first simplex
coordinate is degenerate.  Whether those force a scaled cellular filtration,
or instead obstruct one of the one-thin horn maps, is now the next exact
question.  Source scaling itself is no longer part of that question.
-/

end KUOS.DependentOriginationCanonicalSourceScalingErasureOneThinHornFrontierV1_108
