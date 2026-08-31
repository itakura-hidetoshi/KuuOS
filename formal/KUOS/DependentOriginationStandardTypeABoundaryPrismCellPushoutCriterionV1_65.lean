import KUOS.DependentOriginationStandardTypeABoundaryPrismStaircaseNormalFormV1_64
import KUOS.DependentOriginationStandardTypeBScalingPushoutV1_56

namespace KUOS.DependentOriginationStandardTypeABoundaryPrismCellPushoutCriterionV1_65

open CategoryTheory
open CategoryTheory.Category
open CategoryTheory.Limits
open Opposite
open Simplicial
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationScaledTerminalRLPV1_41
open KUOS.DependentOriginationScaledAnodyneAttachmentFactorizationV1_48
open KUOS.DependentOriginationStandardTypeAScaledHornFamilyV1_49
open KUOS.DependentOriginationStandardTypeAEndpointPushoutProductV1_50
open KUOS.DependentOriginationStandardTypeAScaledPushoutSourceEnrichmentV1_53
open KUOS.DependentOriginationStandardTypeBScalingPushoutV1_56
open KUOS.DependentOriginationStandardTypeABoundaryPrismRelativeCellV1_61
open KUOS.DependentOriginationStandardTypeABoundaryPrismScaledCellsV1_62
open KUOS.DependentOriginationStandardTypeABoundaryPrismDimensionDichotomyV1_63
open KUOS.DependentOriginationStandardTypeABoundaryPrismStaircaseNormalFormV1_64

universe u

noncomputable section

/-!
# Cellwise type-(A) pushout criterion for the boundary prism v1.65

The ordinary relative-cell filtration of v1.61 attaches inner horns.  The
scaled issue is subtler: an ordinary horn cell is not automatically a pushout
of the standard scaled type-(A) generator, because the actual pullback scaling
on the attached simplex can contain additional thin triangles.

This file isolates the exact categorical criterion.

For one rank cell let

* `S_A` be the standard type-(A) scaling on its standard simplex;
* `S_cell` be the exact scaling pulled back from the ambient type-(A) cylinder;
* `H_A` and `H_cell` be the corresponding horn restrictions.

Assume first that `S_A <= S_cell`.  Then also `H_A <= H_cell`, so we can push
out the standard type-(A) horn inclusion along the horn-scaling enrichment
`H_A -> H_cell`.  The generic scaling-enrichment pushout theorem of v1.56
shows that the resulting target scaling consists exactly of

```text
S_A-thin triangles
  or
images of H_cell-thin triangles along the horn inclusion.
```

Therefore this pushout scaling equals the actual cell scaling exactly when
every actual-thin triangle outside the horn is already standard type-(A) thin.
This is the `OutsideACompatible` condition below.

The point of the criterion is that v1.62 immediately discharges the outside
condition in attached dimension at least four: every triangle is already in
the horn.  Thus all high-dimensional cells reduce to one remaining local
calculation, namely `S_A <= S_cell`.  Only dimensions two and three can carry
a genuine scaling-only residual, which is the finite type-(B) frontier handled
next.
-/

/-! ## Type-(A) compatibility on one exact pullback-scaled cell -/

/-- The standard type-(A) target scaling at a cell's own inner horn index is
contained in the exact target scaling pulled back from the ambient prism. -/
def standardTypeABoundaryPrismCellACompatible
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j) : Prop :=
  ScalingLE
    (standardTypeASimplexScaling c.index)
    (standardTypeABoundaryPrismCellScaling g j c)

/-- Type-(A) target compatibility restricts to compatibility of the two horn
scalings on the same ordinary horn carrier. -/
theorem standardTypeABoundaryPrismCellHorn_ACompatible
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j)
    (hA : standardTypeABoundaryPrismCellACompatible g j c) :
    ScalingLE
      (standardTypeAHornScaling c.index)
      (standardTypeABoundaryPrismCellHornScaling g j c) := by
  intro t ht
  change
    (standardTypeABoundaryPrismCellScaling g j c).thin
      (c.horn.ι.app (op ⦋2⦌) t)
  apply hA
  exact ht

/-- The only possible obstruction after the type-(A) horn has been attached:
every triangle that is thin in the actual target but is not already present in
the horn must be standard type-(A) thin. -/
def standardTypeABoundaryPrismCellOutsideACompatible
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j) : Prop :=
  ∀ t : (Δ[c.dim + 1] : SSet.{u}).obj (op ⦋2⦌),
    (standardTypeABoundaryPrismCellScaling g j c).thin t →
    t ∉ c.horn.obj (op ⦋2⦌) →
    (standardTypeASimplexScaling c.index).thin t

/-! ## Push out the standard type-(A) cell along the actual horn scaling -/

/-- The target scaling obtained by pushing the standard type-(A) horn cell
along the horn-scaling enrichment from the standard horn scaling to the exact
ambient horn scaling. -/
def standardTypeABoundaryPrismCellAPushoutScaling
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j) :
    ScaledSimplicialSet (Δ[c.dim + 1] : SSet.{u}) :=
  scalingEnrichmentPushoutScaling
    (standardTypeABoundaryPrismCellHornScaling g j c)
    (standardTypeASimplexScaling c.index)
    c.horn.ι

/-- The scaled target object produced by that type-(A) cobase change. -/
def standardTypeABoundaryPrismCellAPushoutTarget
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j) : ScaledSSet.{u} :=
  ScaledSSet.of (Δ[c.dim + 1] : SSet.{u})
    (standardTypeABoundaryPrismCellAPushoutScaling g j c)

/-- The horn-scaling enrichment used as the left leg of the cellwise cobase
change. -/
def standardTypeABoundaryPrismCellASourceEnrichment
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j)
    (hA : standardTypeABoundaryPrismCellACompatible g j c) :
    ScaledSSet.of (c.horn : SSet.{u}) (standardTypeAHornScaling c.index) ⟶
      standardTypeABoundaryPrismScaledCellSource g j c :=
  scalingEnrichmentHom
    (standardTypeABoundaryPrismCellHorn_ACompatible g j c hA)

/-- The upper map after the type-(A) cobase change.  Its underlying simplicial
map is still the ordinary cell horn inclusion. -/
def standardTypeABoundaryPrismCellAPushoutHom
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j) :
    standardTypeABoundaryPrismScaledCellSource g j c ⟶
      standardTypeABoundaryPrismCellAPushoutTarget g j c :=
  scalingEnrichmentPushoutUpperMap
    (standardTypeABoundaryPrismCellHornScaling g j c)
    (standardTypeASimplexScaling c.index)
    c.horn.ι

/-- Forgetting scaling, the type-(A) cobase-change map is the same ordinary
horn inclusion as the exact cell map. -/
theorem standardTypeABoundaryPrismCellAPushoutHom_map
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j) :
    (standardTypeABoundaryPrismCellAPushoutHom g j c).map = c.horn.ι := by
  rfl

/-- The generic v1.56 scaling-enrichment theorem gives an actual pushout
square.  The top map is exactly the standard type-(A) horn inclusion on this
cell's inner index; the left map enriches its horn scaling to the actual one. -/
noncomputable def standardTypeABoundaryPrismCellA_genericPushout
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j)
    (hA : standardTypeABoundaryPrismCellACompatible g j c) :
    IsPushout
      (scalingEnrichmentPushoutLowerMap
        c.horn.ι (standardTypeAHornInclusion_scaled c.index))
      (standardTypeABoundaryPrismCellASourceEnrichment g j c hA)
      (scalingEnrichmentPushoutTargetEnrichment
        (standardTypeABoundaryPrismCellHornScaling g j c)
        (standardTypeASimplexScaling c.index)
        c.horn.ι)
      (standardTypeABoundaryPrismCellAPushoutHom g j c) := by
  exact scalingEnrichmentPushout_isPushout
    (standardTypeABoundaryPrismCellHorn_ACompatible g j c hA)
    (standardTypeASimplexScaling c.index)
    c.horn.ι
    (standardTypeAHornInclusion_scaled c.index)

/-- The top map in the preceding pushout square is the concrete standard
KuuOS type-(A) generator already assigned to this ordinary rank cell. -/
theorem standardTypeABoundaryPrismCellA_lowerMap_eq_generator
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j) :
    scalingEnrichmentPushoutLowerMap
        c.horn.ι (standardTypeAHornInclusion_scaled c.index) =
      standardTypeAScaledHornGeneratorHom
        (standardTypeABoundaryPrismCellHornIndex g j c) := by
  rfl

/-! ## Exact comparison between the pushout scaling and the actual scaling -/

/-- If the standard type-(A) target scaling is actual-thin, then every triangle
created by the type-(A) cobase change is actual-thin. -/
theorem standardTypeABoundaryPrismCellAPushoutScaling_le_cellScaling
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j)
    (hA : standardTypeABoundaryPrismCellACompatible g j c) :
    ScalingLE
      (standardTypeABoundaryPrismCellAPushoutScaling g j c)
      (standardTypeABoundaryPrismCellScaling g j c) := by
  intro t ht
  change
    (standardTypeASimplexScaling c.index).thin t ∨
      ∃ x : (c.horn : SSet.{u}).obj (op ⦋2⦌),
        (standardTypeABoundaryPrismCellHornScaling g j c).thin x ∧
          c.horn.ι.app (op ⦋2⦌) x = t at ht
  rcases ht with ht | ⟨x, hx, rfl⟩
  · exact hA _ ht
  · exact hx

/-- Conversely, the outside-horn criterion says precisely that every
actual-thin triangle is generated either by the type-(A) target scaling or by
the actual horn scaling. -/
theorem standardTypeABoundaryPrismCell_cellScaling_le_APushoutScaling
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j)
    (hout : standardTypeABoundaryPrismCellOutsideACompatible g j c) :
    ScalingLE
      (standardTypeABoundaryPrismCellScaling g j c)
      (standardTypeABoundaryPrismCellAPushoutScaling g j c) := by
  intro t ht
  change
    (standardTypeASimplexScaling c.index).thin t ∨
      ∃ x : (c.horn : SSet.{u}).obj (op ⦋2⦌),
        (standardTypeABoundaryPrismCellHornScaling g j c).thin x ∧
          c.horn.ι.app (op ⦋2⦌) x = t
  by_cases hm : t ∈ c.horn.obj (op ⦋2⦌)
  · right
    let x : (c.horn : SSet.{u}).obj (op ⦋2⦌) := ⟨t, hm⟩
    refine ⟨x, ?_, ?_⟩
    · change
        (standardTypeABoundaryPrismCellScaling g j c).thin
          (c.horn.ι.app (op ⦋2⦌) x)
      simpa [x] using ht
    · rfl
  · exact Or.inl (hout t ht hm)

/-- Main cellwise scaling criterion: under target type-(A) compatibility, the
standard type-(A) cobase-change target is exactly the actual pullback-scaled
cell target iff the only possible outside-horn thin triangles are already
standard type-(A) thin. -/
theorem standardTypeABoundaryPrismCellAPushoutScaling_eq_cellScaling
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j)
    (hA : standardTypeABoundaryPrismCellACompatible g j c)
    (hout : standardTypeABoundaryPrismCellOutsideACompatible g j c) :
    standardTypeABoundaryPrismCellAPushoutScaling g j c =
      standardTypeABoundaryPrismCellScaling g j c := by
  exact scaling_eq_of_le_antisymm
    (standardTypeABoundaryPrismCellAPushoutScaling_le_cellScaling
      g j c hA)
    (standardTypeABoundaryPrismCell_cellScaling_le_APushoutScaling
      g j c hout)

/-- Object-level form of the exact scaling comparison. -/
theorem standardTypeABoundaryPrismCellAPushoutTarget_eq_cellTarget
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j)
    (hA : standardTypeABoundaryPrismCellACompatible g j c)
    (hout : standardTypeABoundaryPrismCellOutsideACompatible g j c) :
    standardTypeABoundaryPrismCellAPushoutTarget g j c =
      standardTypeABoundaryPrismScaledCellTarget g j c := by
  unfold standardTypeABoundaryPrismCellAPushoutTarget
  unfold standardTypeABoundaryPrismScaledCellTarget
  rw [standardTypeABoundaryPrismCellAPushoutScaling_eq_cellScaling
    g j c hA hout]

/-! ## High-dimensional cells have no outside-horn scaling obstruction -/

/-- In attached dimension at least four, the outside-horn criterion is
vacuous because every triangle of the standard simplex already belongs to the
inner horn. -/
theorem standardTypeABoundaryPrismCellOutsideACompatible_of_four_le
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j)
    (h4 : 4 ≤ c.dim + 1) :
    standardTypeABoundaryPrismCellOutsideACompatible g j c := by
  intro t _ hnot
  exact (hnot
    (standardTypeABoundaryPrism_cell_triangle_mem_horn_of_four_le
      g j c h4 t)).elim

/-- Hence every high-dimensional cell satisfying the local type-(A) target
compatibility has actual target scaling exactly equal to the type-(A)
cobase-change scaling.  No type-(B) or type-(C) scaling cell can be needed in
this range. -/
theorem standardTypeABoundaryPrismCellAPushoutScaling_eq_cellScaling_of_four_le
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j)
    (hA : standardTypeABoundaryPrismCellACompatible g j c)
    (h4 : 4 ≤ c.dim + 1) :
    standardTypeABoundaryPrismCellAPushoutScaling g j c =
      standardTypeABoundaryPrismCellScaling g j c :=
  standardTypeABoundaryPrismCellAPushoutScaling_eq_cellScaling
    g j c hA
    (standardTypeABoundaryPrismCellOutsideACompatible_of_four_le
      g j c h4)

/-- The same high-dimensional conclusion at the object level. -/
theorem standardTypeABoundaryPrismCellAPushoutTarget_eq_cellTarget_of_four_le
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (j : ℕ)
    (c : (standardTypeABoundaryPrismRankFunction g).Cell j)
    (hA : standardTypeABoundaryPrismCellACompatible g j c)
    (h4 : 4 ≤ c.dim + 1) :
    standardTypeABoundaryPrismCellAPushoutTarget g j c =
      standardTypeABoundaryPrismScaledCellTarget g j c :=
  standardTypeABoundaryPrismCellAPushoutTarget_eq_cellTarget
    g j c hA
    (standardTypeABoundaryPrismCellOutsideACompatible_of_four_le
      g j c h4)

/-!
The categorical frontier is now reduced to one local scaling computation:

```text
standard type-A horn
      |
      | cobase change along H_A -> H_cell
      v
A-pushout cell
      |
      | equality iff every actual-thin triangle outside horn is A-thin
      v
actual prism cell
```

For attached dimension at least four the last condition is automatic, because
there is no triangle outside the horn.  Therefore the only remaining work is:

1. prove `S_A <= S_cell` from the v1.64 equal/staircase normal forms;
2. in dimension three, compute the unique missing-face residual exactly;
3. for `n = 2` top staircases identify the post-A target scaling with the
   q12/q23 base scaling and the actual scaling with the corresponding completed
   scaling;
4. lift the resulting A / (A then B) cell classification through coproducts,
   rank pushouts, and the relative-cell transfinite composition.

No type-(C) cell enters this boundary-prism filtration.
-/

end

end KUOS.DependentOriginationStandardTypeABoundaryPrismCellPushoutCriterionV1_65