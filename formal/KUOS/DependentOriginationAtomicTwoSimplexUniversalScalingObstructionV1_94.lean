import KUOS.DependentOriginationStandardTypeATwoSimplexThinReplacementV1_93

namespace KUOS.DependentOriginationAtomicTwoSimplexUniversalScalingObstructionV1_94

open CategoryTheory
open CategoryTheory.Category
open Opposite
open Simplicial
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationScaledTerminalRLPV1_41
open KUOS.DependentOriginationStandardTypeCCollapsedEdgeV1_58
open KUOS.DependentOriginationStandardABCPositiveCanonicalResidualSplitV1_79
open KUOS.DependentOriginationGeneratedPresentationQuotientInvariantV1_81
open KUOS.DependentOriginationStandardCanonicalPresentationGapV1_87
open KUOS.DependentOriginationStandardArbitraryScalingWaypointV1_89
open KUOS.DependentOriginationSingleTriangleScalingFiltrationV1_90
open KUOS.DependentOriginationCanonicalFibrancyAtomicTwoSimplexAuditV1_91
open KUOS.DependentOriginationCanonicalFibrationThinReflectionV1_92
open KUOS.DependentOriginationStandardTypeATwoSimplexThinReplacementV1_93

universe u

/-!
# The universal atomic two-simplex scaling obstruction v1.94

Version v1.90 reduced every arbitrary simplex scaling to finite composites of
single-triangle enrichments.  Versions v1.91-v1.92 then identified one special
atomic map

```text
i₂ : (Delta[2], minimal) -> (Delta[2], minimal + {id₂})
```

whose right lifting property against a scaled map `p` is exactly reflection of
thin 2-simplices.  Version v1.93 compared this with standard type-(A) lifting,
which guarantees only a thin replacement with the same inner horn and target
image.

The present file closes the remaining quantifier gap in the pure-scaling
obstruction.  Thinness reflection is sufficient for lifting against *every*
single-triangle enrichment in every simplex dimension.  Therefore RLP against
`i₂` implies RLP against the complete atomic family.  Since `i₂` itself is one
member of that family, the standard-generated membership of all atomic
scalings is equivalent to membership of this one map.

Consequently the whole v1.89 pure-scaling waypoint is detected by `i₂`:

```text
W = S
  <-> i₂ is standard-generated
  <-> every standard-right map reflects thin 2-simplices.
```

Negating this gives an exact witness theorem.  The scaling waypoint is open if
and only if there is a standard-right map carrying a non-thin source triangle
to a thin target triangle.  Combining with v1.93 upgrades such a witness to a
distinct thin replacement with the same inner horn and the same image.

No standard/canonical inequality is asserted without such a witness.  The
result is a reduction theorem: the complete arbitrary simplex-scaling layer is
controlled by one universal degree-two atomic enrichment.
-/

/-! ## Thinness reflection lifts every single-triangle enrichment -/

/-- Reflection of thin 2-simplices is sufficient for RLP against an arbitrary
single-triangle scaling enrichment in any simplex dimension.  The lift reuses
the underlying simplicial map; reflection supplies scaledness for the one
newly declared thin triangle. -/
theorem hasLiftingProperty_singleTriangle_of_reflectsThinTwoSimplices
    {n : Nat}
    (t : (Δ[n] : SSet.{u}).obj (op ⦋2⦌))
    {X Y : ScaledSSet.{u}}
    (p : X ⟶ Y)
    (hreflect : ReflectsThinTwoSimplices p) :
    HasLiftingProperty (minimalToSingleTriangleScaling.{u} (n := n) t) p := by
  refine ⟨?_⟩
  intro f g sq
  have hsqmap : f.map ≫ p.map = g.map := by
    have hmap := congrArg ScaledSSet.ScaledMap.map sq.w
    set_option backward.isDefEq.respectTransparency false in
      change
        f.map ≫ p.map =
          𝟙 (scaledSimplex (singleTriangleScaling.{u} (n := n) t)).carrier ≫
            g.map at hmap
    simpa only [Category.id_comp] using hmap
  let l : scaledSimplex (singleTriangleScaling.{u} (n := n) t) ⟶ X :=
    { map := f.map
      scaled := by
        intro s hs
        change
          (minimalScaling (Δ[n] : SSet.{u})).thin s ∨ s = t at hs
        rcases hs with hmin | hst
        · exact f.scaled s hmin
        · subst s
          apply hreflect (f.map.app (op ⦋2⦌) t)
          have hthin := g.scaled t (Or.inr rfl)
          rw [← hsqmap] at hthin
          set_option backward.isDefEq.respectTransparency false in
            change
              Y.scaling.thin
                (p.map.app (op ⦋2⦌)
                  (f.map.app (op ⦋2⦌) t)) at hthin
          exact hthin }
  exact CommSq.HasLift.mk'
    { l := l
      fac_left := by
        apply ScaledSSet.ScaledMap.ext
        set_option backward.isDefEq.respectTransparency false in
          change
            𝟙 (scaledSimplex
              (singleTriangleScaling.{u} (n := n) t)).carrier ≫ f.map =
              f.map
        simp only [Category.id_comp]
      fac_right := by
        apply ScaledSSet.ScaledMap.ext
        set_option backward.isDefEq.respectTransparency false in
          change f.map ≫ p.map = g.map
        exact hsqmap }

/-- RLP against the universal atomic identity triangle therefore implies RLP
against every one-triangle enrichment. -/
theorem singleTriangleRLP_of_atomicTwoSimplexRLP
    {n : Nat}
    (t : (Δ[n] : SSet.{u}).obj (op ⦋2⦌))
    {X Y : ScaledSSet.{u}}
    (p : X ⟶ Y)
    (hatomic : HasLiftingProperty atomicTwoSimplexEnrichment.{u} p) :
    HasLiftingProperty (minimalToSingleTriangleScaling.{u} (n := n) t) p := by
  apply hasLiftingProperty_singleTriangle_of_reflectsThinTwoSimplices.{u}
    (n := n) t p
  exact (atomicTwoSimplexRLP_iff_reflectsThinTwoSimplices p).1 hatomic

/-! ## One atomic map detects the complete standard pure-scaling layer -/

/-- The universal atomic map is standard-generated exactly when every
single-triangle enrichment is standard-generated.  The nontrivial direction
uses orthogonality: membership of `i₂` forces every standard-right map to
reflect thinness, hence to lift against every atomic enrichment. -/
theorem atomicTwoSimplex_standardGenerated_iff_singleTriangles_le :
    (standardGeneratedScaledAnodyneABC : MorphismProperty (ScaledSSet.{u}))
        atomicTwoSimplexEnrichment.{u} ↔
      (singleTriangleScalingEnrichments : MorphismProperty (ScaledSSet.{u})) ≤
        standardGeneratedScaledAnodyneABC := by
  constructor
  · intro hatomic
    intro A B f hf
    dsimp [singleTriangleScalingEnrichments] at hf
    cases hf with
    | mk q =>
        change
          (standardScaledAnodyneGeneratorsABC :
            MorphismProperty (ScaledSSet.{u})).rlp.llp
            (minimalToSingleTriangleScaling.{u} (n := q.n) q.triangle)
        intro X Y p hp
        have hi2 : HasLiftingProperty atomicTwoSimplexEnrichment.{u} p :=
          hatomic p hp
        exact singleTriangleRLP_of_atomicTwoSimplexRLP.{u}
          (n := q.n) q.triangle p hi2
  · intro hall
    have hmem := hall _
      (singleTriangleScalingEnrichment_mem
        ({ n := 2,
           triangle := (identityTwoSimplex :
             (Δ[2] : SSet.{u}).obj (op ⦋2⦌)) } :
          SingleTriangleScalingEnrichmentIndex.{u}))
    simpa [singleTriangleScalingEnrichmentHom,
      atomicTwoSimplexEnrichment, atomicTwoSimplexScaling] using hmem

/-- Hence the v1.90 pure-scaling closure condition is detected by the single
identity-triangle enrichment `i₂`. -/
theorem standardArbitraryScalingObstructionClosed_iff_atomicTwoSimplex :
    StandardArbitraryScalingObstructionClosed.{u} ↔
      (standardGeneratedScaledAnodyneABC : MorphismProperty (ScaledSSet.{u}))
        atomicTwoSimplexEnrichment.{u} := by
  exact
    (standardArbitraryScalingObstructionClosed_iff_singleTriangles.{u}).trans
      (atomicTwoSimplex_standardGenerated_iff_singleTriangles_le.{u}).symm

/-- Literal waypoint form of the same result. -/
theorem standardArbitraryScalingWaypoint_eq_standardABC_iff_atomicTwoSimplex :
    standardArbitraryScalingWaypoint.{u} = standardABCPresentation.{u} ↔
      (standardGeneratedScaledAnodyneABC : MorphismProperty (ScaledSSet.{u}))
        atomicTwoSimplexEnrichment.{u} := by
  simpa [StandardArbitraryScalingObstructionClosed] using
    standardArbitraryScalingObstructionClosed_iff_atomicTwoSimplex.{u}

/-! ## Right-class form: standard reflection is exactly scaling closure -/

/-- Membership of `i₂` in the standard generated left class is equivalent to
thinness reflection for every map in the complete standard right class. -/
theorem atomicTwoSimplex_standardGenerated_iff_all_standardRight_reflect :
    (standardGeneratedScaledAnodyneABC : MorphismProperty (ScaledSSet.{u}))
        atomicTwoSimplexEnrichment.{u} ↔
      ∀ (X Y : ScaledSSet.{u}) (p : X ⟶ Y),
        (standardGeneratedScaledAnodyneABC :
          MorphismProperty (ScaledSSet.{u})).rlp p →
        ReflectsThinTwoSimplices p := by
  constructor
  · intro hatomic X Y p hstd
    apply (atomicTwoSimplexRLP_iff_reflectsThinTwoSimplices p).1
    have hp :
        (standardScaledAnodyneGeneratorsABC :
          MorphismProperty (ScaledSSet.{u})).rlp p := by
      simpa [standardGeneratedScaledAnodyneABC] using hstd
    exact hatomic p hp
  · intro hall
    change
      (standardScaledAnodyneGeneratorsABC :
        MorphismProperty (ScaledSSet.{u})).rlp.llp
        atomicTwoSimplexEnrichment.{u}
    intro X Y p hp
    apply (atomicTwoSimplexRLP_iff_reflectsThinTwoSimplices p).2
    apply hall X Y p
    simpa [standardGeneratedScaledAnodyneABC] using hp

/-- The entire arbitrary-scaling waypoint closes exactly when every
standard-right map reflects thin 2-simplices. -/
theorem standardArbitraryScalingObstructionClosed_iff_all_standardRight_reflect :
    StandardArbitraryScalingObstructionClosed.{u} ↔
      ∀ (X Y : ScaledSSet.{u}) (p : X ⟶ Y),
        (standardGeneratedScaledAnodyneABC :
          MorphismProperty (ScaledSSet.{u})).rlp p →
        ReflectsThinTwoSimplices p := by
  exact
    (standardArbitraryScalingObstructionClosed_iff_atomicTwoSimplex.{u}).trans
      atomicTwoSimplex_standardGenerated_iff_all_standardRight_reflect.{u}

/-! ## Exact negative witness forms -/

/-- Failure of thinness reflection is exactly the existence of a source
2-simplex which is non-thin although its image is thin. -/
theorem not_reflectsThinTwoSimplices_iff_exists
    {X Y : ScaledSSet.{u}}
    (p : X ⟶ Y) :
    ¬ ReflectsThinTwoSimplices p ↔
      ∃ σ : X.carrier.obj (op ⦋2⦌),
        Y.scaling.thin (p.map.app (op ⦋2⦌) σ) ∧
        ¬ X.scaling.thin σ := by
  classical
  constructor
  · intro hnot
    by_contra hnone
    apply hnot
    intro σ himage
    by_contra hsource
    apply hnone
    exact ⟨σ, himage, hsource⟩
  · rintro ⟨σ, himage, hsource⟩ hreflect
    exact hsource (hreflect σ himage)

/-- The pure-scaling waypoint is open exactly when there is a standard-right
map that sends one non-thin source triangle to a thin target triangle. -/
theorem not_standardArbitraryScalingObstructionClosed_iff_exists_standardRight_nonreflecting :
    ¬ StandardArbitraryScalingObstructionClosed.{u} ↔
      ∃ (X Y : ScaledSSet.{u}) (p : X ⟶ Y)
        (σ : X.carrier.obj (op ⦋2⦌)),
        (standardGeneratedScaledAnodyneABC :
          MorphismProperty (ScaledSSet.{u})).rlp p ∧
        Y.scaling.thin (p.map.app (op ⦋2⦌) σ) ∧
        ¬ X.scaling.thin σ := by
  classical
  constructor
  · intro hnot
    have hex :
        ∃ (X Y : ScaledSSet.{u}) (p : X ⟶ Y),
          (standardGeneratedScaledAnodyneABC :
            MorphismProperty (ScaledSSet.{u})).rlp p ∧
          ¬ ReflectsThinTwoSimplices p := by
      by_contra hnone
      apply hnot
      apply
        (standardArbitraryScalingObstructionClosed_iff_all_standardRight_reflect.{u}).2
      intro X Y p hstd
      by_contra hreflect
      apply hnone
      exact ⟨X, Y, p, hstd, hreflect⟩
    rcases hex with ⟨X, Y, p, hstd, hnonreflect⟩
    rcases (not_reflectsThinTwoSimplices_iff_exists p).1 hnonreflect with
      ⟨σ, himage, hsource⟩
    exact ⟨X, Y, p, σ, hstd, himage, hsource⟩
  · rintro ⟨X, Y, p, σ, hstd, himage, hsource⟩ hclosed
    have hreflect :=
      (standardArbitraryScalingObstructionClosed_iff_all_standardRight_reflect.{u}).1
        hclosed X Y p hstd
    exact hsource (hreflect σ himage)

/-- Combining the exact nonreflection witness with v1.93, the pure-scaling
waypoint is open exactly when a standard-right map contains a distinct
non-thin/thin replacement pair with the same inner horn and the same image. -/
theorem not_standardArbitraryScalingObstructionClosed_iff_exists_distinct_thinReplacement :
    ¬ StandardArbitraryScalingObstructionClosed.{u} ↔
      ∃ (X Y : ScaledSSet.{u}) (p : X ⟶ Y)
        (σ τ : X.carrier.obj (op ⦋2⦌)),
        (standardGeneratedScaledAnodyneABC :
          MorphismProperty (ScaledSSet.{u})).rlp p ∧
        Y.scaling.thin (p.map.app (op ⦋2⦌) σ) ∧
        ¬ X.scaling.thin σ ∧
        X.scaling.thin τ ∧
        SameStandardTypeAInnerHorn σ τ ∧
        SameTwoSimplexImage p τ σ ∧
        τ ≠ σ := by
  constructor
  · intro hnot
    rcases
        (not_standardArbitraryScalingObstructionClosed_iff_exists_standardRight_nonreflecting.{u}).1
          hnot with
      ⟨X, Y, p, σ, hstd, himage, hsource⟩
    rcases
        standardRight_nonreflecting_has_distinct_thinReplacement
          hstd σ himage hsource with
      ⟨τ, hτ, hhorn, hpimage, hne⟩
    exact ⟨X, Y, p, σ, τ, hstd, himage, hsource,
      hτ, hhorn, hpimage, hne⟩
  · rintro ⟨X, Y, p, σ, τ, hstd, himage, hsource,
      hτ, hhorn, hpimage, hne⟩
    apply
      (not_standardArbitraryScalingObstructionClosed_iff_exists_standardRight_nonreflecting.{u}).2
    exact ⟨X, Y, p, σ, hstd, himage, hsource⟩

/-! ## Replace the scaling clause in the full presentation criteria -/

/-- The forward canonical-to-standard comparison factors through one atomic
membership test plus the residual post-scaling geometry. -/
theorem canonicalKuuOS_le_standardABC_iff_atomicTwoSimplex_and_residual :
    canonicalKuuOSPresentation.{u} ≤ standardABCPresentation.{u} ↔
      (standardGeneratedScaledAnodyneABC : MorphismProperty (ScaledSSet.{u}))
          atomicTwoSimplexEnrichment.{u} ∧
        CanonicalBelowStandardAfterArbitraryScaling.{u} := by
  rw [canonicalKuuOS_le_standardABC_iff_scalingClosed_and_residual,
    standardArbitraryScalingObstructionClosed_iff_atomicTwoSimplex.{u}]

/-- Full standard/canonical gap closure is equivalently the reverse standard
generator comparison, the single `i₂` standard-generation test, and the
remaining forward geometry after pure scaling has been adjoined. -/
theorem standardCanonicalPresentationGapClosed_iff_reverse_atomic_residual :
    StandardCanonicalPresentationGapClosed.{u} ↔
      StandardABCCanonicalGeneratorwiseReverseComparison.{u} ∧
        (standardGeneratedScaledAnodyneABC : MorphismProperty (ScaledSSet.{u}))
            atomicTwoSimplexEnrichment.{u} ∧
          CanonicalBelowStandardAfterArbitraryScaling.{u} := by
  rw [standardCanonicalPresentationGapClosed_iff_reverse_scaling_residual,
    standardArbitraryScalingObstructionClosed_iff_atomicTwoSimplex.{u}]

/-!
The complete pure-scaling frontier is therefore no longer an infinite family:

```text
all arbitrary simplex scalings
  -> v1.90 finite atomic filtration
  -> v1.94 one universal atomic detector i₂.

W = S
  <-> i₂ ∈ standardGenerated
  <-> every standard-right map reflects thinness.

W != S
  <-> exists a standard-right nonreflecting map
  <-> exists distinct sigma/tau with
       sigma non-thin,
       tau thin,
       same type-(A) inner horn,
       same target image.
```

The remaining task for a strict standard-versus-canonical separation is now
completely concrete: construct one standard A/B/C-right map with the final
finite degree-two replacement geometry.  Until such a map is supplied, no
strict inequality is claimed.
-/

end KUOS.DependentOriginationAtomicTwoSimplexUniversalScalingObstructionV1_94