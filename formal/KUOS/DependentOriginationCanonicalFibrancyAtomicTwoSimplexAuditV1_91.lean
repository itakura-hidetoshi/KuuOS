import KUOS.DependentOriginationSingleTriangleScalingFiltrationV1_90

namespace KUOS.DependentOriginationCanonicalFibrancyAtomicTwoSimplexAuditV1_91

open CategoryTheory
open CategoryTheory.Category
open Opposite
open Simplicial
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationGlobalDuskinScaledNerveV1_21
open KUOS.DependentOriginationScaledTerminalRLPV1_41
open KUOS.DependentOriginationScaledAnodyneGeneratorClosureV1_42
open KUOS.DependentOriginationExternalScaledAnodyneGeneratorComparisonV1_46
open KUOS.DependentOriginationStandardTypeAScaledPushoutSourceEnrichmentV1_53
open KUOS.DependentOriginationStandardTypeBScalingPushoutV1_56
open KUOS.DependentOriginationGeneratedPresentationQuotientInvariantV1_81
open KUOS.DependentOriginationGeneratedPresentationOrderReflectionV1_84
open KUOS.DependentOriginationStandardCanonicalPresentationGapV1_87
open KUOS.DependentOriginationCanonicalAttachmentScalingObstructionRetractV1_88
open KUOS.DependentOriginationSingleTriangleScalingFiltrationV1_90

universe u v w

/-!
# Canonical fibrancy audit through the atomic 2-simplex scaling retract v1.91

Version v1.88 proved that every identity-underlying simplex-scaling enrichment
is an arrow retract of a canonical horn-cylinder attachment.  Version v1.90
then reduced the entire arbitrary-scaling obstruction to atomic one-triangle
enrichments.

This file audits the smallest atomic case, in dimension two.  Let `id₂` be the
Yoneda identity 2-simplex of `Δ[2]`, and enlarge the minimal scaling only by
making `id₂` thin.  The corresponding enrichment

```text
(Δ[2], minimal) -> (Δ[2], minimal + {id₂})
```

has terminal RLP against a scaled target exactly when every 2-simplex of the
target is thin.  The forward implication is Yoneda evaluation at `id₂`; the
reverse implication simply reuses the same underlying simplicial map and uses
the all-thin hypothesis for the one newly thin triangle.

Because v1.88 places this atomic enrichment in the canonical generated left
class, canonical attachment fibrancy forces the target scaling to be maximal.
For the global Duskin scaling this says that every 2-simplex has invertible
comparison or is degenerate.  Thus the arbitrary-scaling content of the
canonical attachment presentation is not neutral: its right class is already
maximal-scaling in degree two.

No standard/canonical inequality is asserted without a standard-right-class
witness.  The final criterion isolates exactly what such a witness must supply:
a standard-fibrant scaled object with one non-thin 2-simplex disproves the
canonical-to-standard order.
-/

/-! ## The atomic identity triangle in dimension two -/

/-- The Yoneda identity 2-simplex of the standard 2-simplex. -/
def identityTwoSimplex :
    (Δ[2] : SSet.{u}).obj (op ⦋2⦌) :=
  SSet.stdSimplex.objEquiv.symm (𝟙 ⦋2⦌)

/-- Minimal scaling on `Δ[2]` enlarged only by the Yoneda identity
2-simplex. -/
@[implicit_reducible]
def atomicTwoSimplexScaling :
    ScaledSimplicialSet (Δ[2] : SSet.{u}) :=
  singleTriangleScaling identityTwoSimplex

/-- The atomic identity-underlying enrichment in dimension two. -/
def atomicTwoSimplexEnrichment :
    minimallyScaledSimplex 2 ⟶ scaledSimplex atomicTwoSimplexScaling :=
  minimalToSingleTriangleScaling identityTwoSimplex

@[simp]
theorem atomicTwoSimplexScaling_identity_thin :
    atomicTwoSimplexScaling.thin identityTwoSimplex := by
  unfold atomicTwoSimplexScaling singleTriangleScaling
  exact Or.inr rfl

/-! ## Canonical left-class membership -/

/-- Every atomic one-triangle enrichment is already in the canonical generated
left class, by the arbitrary-scaling retract theorem of v1.88. -/
theorem minimalToSingleTriangleScaling_mem_canonicalGenerated
    {n : Nat}
    (t : (Δ[n] : SSet.{u}).obj (op ⦋2⦌)) :
    (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u}))
      (minimalToSingleTriangleScaling t) := by
  have h :=
    minimalToChosenSimplexScaling_mem_canonicalGenerated
      (singleTriangleScaling t)
  have heq :
      minimalToSingleTriangleScaling t =
        minimalToChosenSimplexScaling (singleTriangleScaling t) := by
    apply ScaledSSet.ScaledMap.ext
    rfl
  rw [heq]
  exact h

/-- In particular the dimension-two identity-triangle enrichment is
canonical-generated. -/
theorem atomicTwoSimplexEnrichment_mem_canonicalGenerated :
    (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u}))
      atomicTwoSimplexEnrichment := by
  exact minimalToSingleTriangleScaling_mem_canonicalGenerated identityTwoSimplex

/-! ## Exact terminal-RLP characterization -/

/-- Terminal RLP for the single identity-triangle enrichment is equivalent to
all 2-simplices of the target being thin. -/
theorem atomicTwoSimplexRLP_iff_all_two_simplices_thin
    (X : ScaledSSet.{u}) :
    HasLiftingProperty
        atomicTwoSimplexEnrichment
        (ScaledSSet.toPoint X) ↔
      ∀ σ : X.carrier.obj (op ⦋2⦌), X.scaling.thin σ := by
  constructor
  · intro h σ
    let f : minimallyScaledSimplex 2 ⟶ X :=
      { map := SSet.yonedaEquiv.symm σ
        scaled := minimalScaling_map X.scaling _ }
    rcases
        (ScaledSSet.hasLiftingProperty_toPoint_iff
          atomicTwoSimplexEnrichment).1 h f with
      ⟨l, hl⟩
    have hlmap : l.map = f.map := by
      have hmap := congrArg ScaledSSet.ScaledMap.map hl
      set_option backward.isDefEq.respectTransparency false in
        change (𝟙 (Δ[2] : SSet.{u}) ≫ l.map) = f.map at hmap
      simpa only [Category.id_comp] using hmap
    have hthin :=
      l.scaled identityTwoSimplex atomicTwoSimplexScaling_identity_thin
    rw [hlmap] at hthin
    have hthin' :
        X.scaling.thin
          ((SSet.yonedaEquiv.symm σ).app (op ⦋2⦌) identityTwoSimplex) := by
      set_option backward.isDefEq.respectTransparency false in
        exact hthin
    simpa [identityTwoSimplex,
      SSet.yonedaEquiv_symm_app_objEquiv_symm] using hthin'
  · intro hall
    apply
      (ScaledSSet.hasLiftingProperty_toPoint_iff
        atomicTwoSimplexEnrichment).2
    intro f
    let l : scaledSimplex atomicTwoSimplexScaling ⟶ X :=
      { map := f.map
        scaled := by
          intro t ht
          change
            (minimalScaling (Δ[2] : SSet.{u})).thin t ∨
              t = identityTwoSimplex at ht
          rcases ht with hmin | hident
          · exact f.scaled t hmin
          · subst t
            exact hall _ }
    refine ⟨l, ?_⟩
    apply ScaledSSet.ScaledMap.ext
    set_option backward.isDefEq.respectTransparency false in
      change 𝟙 (Δ[2] : SSet.{u}) ≫ f.map = f.map
    simp only [Category.id_comp]

/-- The same atomic RLP can be stated intrinsically as maximality of the target
scaling. -/
theorem atomicTwoSimplexRLP_iff_scaling_eq_maximal
    (X : ScaledSSet.{u}) :
    HasLiftingProperty
        atomicTwoSimplexEnrichment
        (ScaledSSet.toPoint X) ↔
      X.scaling = ScaledSimplicialSet.maximal X.carrier := by
  rw [atomicTwoSimplexRLP_iff_all_two_simplices_thin]
  constructor
  · intro hall
    apply scaling_eq_of_le_antisymm
    · intro t _
      exact ScaledSimplicialSet.maximal_thin _ _
    · intro t _
      exact hall t
  · intro hmax t
    rw [hmax]
    exact ScaledSimplicialSet.maximal_thin _ _

/-! ## Canonical attachment fibrancy forces maximal scaling -/

/-- Attachment fibrancy lifts against every morphism in the canonical
generated left class, not only against the literal attachment generators. -/
theorem attachmentFibrant_hasLiftingProperty_of_canonicalGenerated
    {X : ScaledSSet.{u}}
    (hX : IsAttachmentFibrant X)
    {A B : ScaledSSet.{u}}
    (i : A ⟶ B)
    (hi :
      (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u})) i) :
    HasLiftingProperty i (ScaledSSet.toPoint X) := by
  have hcanonical :
      (canonicalGeneratedScaledAnodyne : MorphismProperty (ScaledSSet.{u})).rlp
        (ScaledSSet.toPoint X) := by
    rw [canonicalGeneratedScaledAnodyne_rlp]
    exact hX
  exact hcanonical i hi

/-- Canonical attachment fibrancy forces every 2-simplex to be thin. -/
theorem attachmentFibrant_all_two_simplices_thin
    {X : ScaledSSet.{u}}
    (hX : IsAttachmentFibrant X) :
    ∀ σ : X.carrier.obj (op ⦋2⦌), X.scaling.thin σ := by
  apply (atomicTwoSimplexRLP_iff_all_two_simplices_thin X).1
  exact
    attachmentFibrant_hasLiftingProperty_of_canonicalGenerated
      hX atomicTwoSimplexEnrichment
      atomicTwoSimplexEnrichment_mem_canonicalGenerated

/-- Equivalently, an attachment-fibrant target has the maximal scaling. -/
theorem attachmentFibrant_scaling_eq_maximal
    {X : ScaledSSet.{u}}
    (hX : IsAttachmentFibrant X) :
    X.scaling = ScaledSimplicialSet.maximal X.carrier := by
  apply scaling_eq_of_le_antisymm
  · intro t _
    exact ScaledSimplicialSet.maximal_thin _ _
  · intro t _
    exact attachmentFibrant_all_two_simplices_thin hX t

/-- Any explicitly non-thin 2-simplex obstructs canonical attachment
fibrancy. -/
theorem not_attachmentFibrant_of_nonThin_two_simplex
    {X : ScaledSSet.{u}}
    (σ : X.carrier.obj (op ⦋2⦌))
    (hσ : ¬ X.scaling.thin σ) :
    ¬ IsAttachmentFibrant X := by
  intro hX
  exact hσ (attachmentFibrant_all_two_simplices_thin hX σ)

/-! ## Global Duskin specialization -/

/-- Attachment fibrancy of the global Duskin scaled object forces every
Duskin 2-simplex to have invertible comparison or to be degenerate. -/
theorem globalDuskin_attachmentFibrant_implies_thin_comparison
    {B : Type u} [Bicategory.{w, v} B]
    (hB :
      IsAttachmentFibrant
        (ScaledSSet.of (duskinNerve B) (duskinScaling B))) :
    ∀ σ : (duskinNerve B).obj (op ⦋2⦌),
      IsIso (duskinComparison σ) ∨ IsDegenerateDuskinTwoSimplex σ := by
  intro σ
  change (duskinScaling B).thin σ
  exact attachmentFibrant_all_two_simplices_thin hB σ

/-- On a nondegenerate Duskin 2-simplex, attachment fibrancy therefore forces
the comparison 2-cell itself to be invertible. -/
theorem globalDuskin_attachmentFibrant_implies_comparison_isIso_of_nondegenerate
    {B : Type u} [Bicategory.{w, v} B]
    (hB :
      IsAttachmentFibrant
        (ScaledSSet.of (duskinNerve B) (duskinScaling B)))
    (σ : (duskinNerve B).obj (op ⦋2⦌))
    (hσ : ¬ IsDegenerateDuskinTwoSimplex σ) :
    IsIso (duskinComparison σ) := by
  rcases globalDuskin_attachmentFibrant_implies_thin_comparison hB σ with
    hIso | hdeg
  · exact hIso
  · exact False.elim (hσ hdeg)

/-- A nondegenerate Duskin triangle with noninvertible comparison is therefore
a direct obstruction to canonical attachment fibrancy. -/
theorem not_globalDuskin_attachmentFibrant_of_noninvertible_nondegenerate
    {B : Type u} [Bicategory.{w, v} B]
    (σ : (duskinNerve B).obj (op ⦋2⦌))
    (hnotIso : ¬ IsIso (duskinComparison σ))
    (hnotDeg : ¬ IsDegenerateDuskinTwoSimplex σ) :
    ¬ IsAttachmentFibrant
        (ScaledSSet.of (duskinNerve B) (duskinScaling B)) := by
  intro hB
  rcases globalDuskin_attachmentFibrant_implies_thin_comparison hB σ with
    hIso | hdeg
  · exact hnotIso hIso
  · exact hnotDeg hdeg

/-! ## Conditional separation from the standard A/B/C presentation -/

/-- If canonical were below standard, every standard-right terminal map would
also be canonically attachment-fibrant. -/
theorem attachmentFibrant_of_standardRLP_of_canonical_le_standard
    {X : ScaledSSet.{u}}
    (horder :
      (canonicalKuuOSPresentation : GeneratedScaledAnodynePresentation.{u}) ≤
        standardABCPresentation)
    (hstd :
      (KUOS.DependentOriginationStandardTypeCCollapsedEdgeV1_58.standardGeneratedScaledAnodyneABC :
        MorphismProperty (ScaledSSet.{u})).rlp
        (ScaledSSet.toPoint X)) :
    IsAttachmentFibrant X := by
  have hgen :
      (scaledHornAttachmentGenerators : MorphismProperty (ScaledSSet.{u})) ≤
        (KUOS.DependentOriginationStandardTypeCCollapsedEdgeV1_58.standardGeneratedScaledAnodyneABC :
          MorphismProperty (ScaledSSet.{u})) :=
    canonicalKuuOS_le_standardABC_iff_canonicalGenerators_le_standardGenerated.1
      horder
  change
    (scaledHornAttachmentGenerators : MorphismProperty (ScaledSSet.{u})).rlp
      (ScaledSSet.toPoint X)
  exact (MorphismProperty.antitone_rlp hgen) _ hstd

/-- Hence a standard-right target with one non-thin 2-simplex disproves the
canonical-to-standard presentation order. -/
theorem not_canonicalKuuOS_le_standardABC_of_standardRLP_nonThin
    {X : ScaledSSet.{u}}
    (hstd :
      (KUOS.DependentOriginationStandardTypeCCollapsedEdgeV1_58.standardGeneratedScaledAnodyneABC :
        MorphismProperty (ScaledSSet.{u})).rlp
        (ScaledSSet.toPoint X))
    (σ : X.carrier.obj (op ⦋2⦌))
    (hσ : ¬ X.scaling.thin σ) :
    ¬ ((canonicalKuuOSPresentation : GeneratedScaledAnodynePresentation.{u}) ≤
      standardABCPresentation) := by
  intro horder
  have hX :=
    attachmentFibrant_of_standardRLP_of_canonical_le_standard horder hstd
  exact hσ (attachmentFibrant_all_two_simplices_thin hX σ)

/-- For a global Duskin object, it is enough to exhibit standard A/B/C
terminal RLP together with one nondegenerate noninvertible comparison
2-simplex. -/
theorem not_canonicalKuuOS_le_standardABC_of_standardRLP_duskin_witness
    {B : Type u} [Bicategory.{w, v} B]
    (hstd :
      (KUOS.DependentOriginationStandardTypeCCollapsedEdgeV1_58.standardGeneratedScaledAnodyneABC :
        MorphismProperty (ScaledSSet.{max (max w v) u})).rlp
        (ScaledSSet.toPoint
          (ScaledSSet.of (duskinNerve B) (duskinScaling B))))
    (σ : (duskinNerve B).obj (op ⦋2⦌))
    (hnotIso : ¬ IsIso (duskinComparison σ))
    (hnotDeg : ¬ IsDegenerateDuskinTwoSimplex σ) :
    ¬ ((canonicalKuuOSPresentation :
        GeneratedScaledAnodynePresentation.{max (max w v) u}) ≤
      standardABCPresentation) := by
  apply not_canonicalKuuOS_le_standardABC_of_standardRLP_nonThin hstd σ
  intro hthin
  change IsIso (duskinComparison σ) ∨ IsDegenerateDuskinTwoSimplex σ at hthin
  rcases hthin with hIso | hdeg
  · exact hnotIso hIso
  · exact hnotDeg hdeg

/-!
The audit therefore changes the comparison frontier from an undirected search
for equality into a sharp separation test:

```text
canonical attachment fibrant X
  -> atomic identity-triangle RLP
  <-> every X_2 simplex is thin
  <-> X.scaling is maximal.

For the global Duskin nerve:

canonical attachment fibrant
  -> every nondegenerate comparison 2-cell is invertible.

Therefore a future standard-right-class witness carrying one genuine
noninvertible nondegenerate 2-cell immediately proves

  not (canonicalKuuOSPresentation <= standardABCPresentation).
```

This file does not assume such a standard-right witness.  It isolates that
single remaining burden without weakening any hypothesis and without asserting
standard/canonical inequality prematurely.
-/

end KUOS.DependentOriginationCanonicalFibrancyAtomicTwoSimplexAuditV1_91
