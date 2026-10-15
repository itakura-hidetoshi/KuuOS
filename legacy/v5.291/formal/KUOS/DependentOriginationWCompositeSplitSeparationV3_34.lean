import KUOS.DependentOriginationQuotientSplitDirectionalSeparationV3_33
import Mathlib.CategoryTheory.EpiMono

namespace KUOS.DependentOriginationWCompositeSplitSeparationV3_34

open CategoryTheory
open Set
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationCoherentQuotientTransportV2_59
open KUOS.DependentOriginationGeneratedPointwiseChoiceV2_68
open KUOS.DependentOriginationQuotientGaugeIndependenceV3_03
open KUOS.DependentOriginationQuotientGaugeIntersectionObstructionV3_11
open KUOS.DependentOriginationQuotientGaugeCoordinateKeyV3_14
open KUOS.DependentOriginationAssociatorUnitorTriangleResidualV3_26
open KUOS.DependentOriginationAssociatorUnitorOneSidedSeparationV3_28
open KUOS.DependentOriginationQuotientSplitDirectionalSeparationV3_33

universe u v uH vH

set_option autoImplicit false

/-!
# Directional splitting from source W-composites v3.34

v3.33 consumes one-sided inverse equations in the actual localization. This
layer constructs those equations from source-presentation data, using
Mathlib's concrete `Localization.Construction.wIso` rather than adding a
separation assumption or choosing a coherent family of evaluation isomorphisms.

For source arrows

  s : A -> X,  f : X -> Y,  g : Y -> Z,  r : Z -> B,

assume only `W (s ≫ f)` and `W (g ≫ r)`. The auxiliary objects `A` and `B`
need not equal `Y`. In the localization the explicit maps

  Q(s ≫ f)^{-1} ≫ Q(s),    Q(r) ≫ Q(g ≫ r)^{-1}

are respectively a section of `Q(f)` and a retraction of `Q(g)`.

The construction is bundled as Mathlib `SplitEpi` / `SplitMono` data. The
v3.33 semantic results also acquire adapters for the corresponding Mathlib
propositional classes, eliminating their witnesses only into propositions.
Consequently the actual mixed triangle closes under the W-composite criterion,
with all three corrected-route and both anchor-agreement hypotheses retained.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- Inverting the whole left composite supplies an explicit section of the
right factor. No `W f`, `W s`, or equality `A = Y` is required. -/
noncomputable def splitEpiQMapOfWComposite
    {A X Y : Context} (f : X ⟶ Y) (s : A ⟶ X)
    (hs : W (s ≫ f)) : SplitEpi (W.Q.map f) where
  section_ :=
    (Localization.Construction.wIso (s ≫ f) hs).inv ≫ W.Q.map s
  id := by
    rw [Category.assoc, ← W.Q.map_comp]
    exact (Localization.Construction.wIso (s ≫ f) hs).inv_hom_id

/-- Dually, inverting the whole right composite supplies an explicit
retraction of the left factor, even when the auxiliary target differs. -/
noncomputable def splitMonoQMapOfWComposite
    {Y Z B : Context} (g : Y ⟶ Z) (r : Z ⟶ B)
    (hr : W (g ≫ r)) : SplitMono (W.Q.map g) where
  retraction :=
    W.Q.map r ≫ (Localization.Construction.wIso (g ≫ r) hr).inv
  id := by
    rw [← Category.assoc, ← W.Q.map_comp]
    exact (Localization.Construction.wIso (g ≫ r) hr).hom_inv_id

/-- Expose the constructed left splitting through Mathlib's standard class.
This is a theorem, not a global instance-search rule on source complements. -/
theorem isSplitEpi_Q_map_of_W_comp
    {A X Y : Context} (f : X ⟶ Y) (s : A ⟶ X)
    (hs : W (s ≫ f)) : IsSplitEpi (W.Q.map f) :=
  IsSplitEpi.mk' (splitEpiQMapOfWComposite W f s hs)

/-- Expose the constructed right splitting through the dual standard class. -/
theorem isSplitMono_Q_map_of_W_comp
    {Y Z B : Context} (g : Y ⟶ Z) (r : Z ⟶ B)
    (hr : W (g ≫ r)) : IsSplitMono (W.Q.map g) :=
  IsSplitMono.mk' (splitMonoQMapOfWComposite W g r hr)

variable (R : RawHigherContextualSystem.{u, v, uH, vH}
  (Context := Context))
variable (D : PointwiseWAdjointEquivalenceData (W := W) R)

/-- A Mathlib split-epi witness supplies the explicit equation consumed by
v3.33. The existential splitting is eliminated locally into `EssSurj`. -/
theorem quotientRepresentativeMap_essSurj_of_isSplitEpi
    {X Y : W.Localization} (f : X ⟶ Y) [hf : IsSplitEpi f] :
    (quotientRepresentativeMap W R D f).toFunctor.EssSurj := by
  rcases hf.exists_splitEpi with ⟨sf⟩
  exact quotientRepresentativeMap_essSurj_of_section
    W R D f sf.section_ sf.id

/-- A Mathlib split-mono witness supplies the dual v3.33 equation. No
faithfulness of the chosen retraction itself is required. -/
theorem quotientRepresentativeMap_faithful_of_isSplitMono
    {Y Z : W.Localization} (g : Y ⟶ Z) [hg : IsSplitMono g] :
    (quotientRepresentativeMap W R D g).toFunctor.Faithful := by
  rcases hg.exists_splitMono with ⟨rg⟩
  exact quotientRepresentativeMap_faithful_of_retraction
    W R D g rg.retraction rg.id

/-- The standard split classes suffice for the actual middle-identity
separation property, without selecting their witnesses simultaneously. -/
theorem middleIdentityWhiskerSeparating_of_isSplitEpi_isSplitMono
    {X Y Z : W.Localization} (f : X ⟶ Y) (g : Y ⟶ Z)
    [IsSplitEpi f] [IsSplitMono g] :
    MiddleIdentityWhiskerSeparating W R D f g := by
  exact middleIdentityWhiskerSeparating_of_essSurj_faithful W R D f g
    (quotientRepresentativeMap_essSurj_of_isSplitEpi W R D f)
    (quotientRepresentativeMap_faithful_of_isSplitMono W R D g)

/-- A source W-composite ending in `f` makes the evaluation of `Q(f)`
essentially surjective, even without a letterwise certificate for `f`. -/
theorem quotientRepresentativeMap_Q_map_essSurj_of_W_comp
    {A X Y : Context} (f : X ⟶ Y) (s : A ⟶ X)
    (hs : W (s ≫ f)) :
    (quotientRepresentativeMap W R D (W.Q.map f)).toFunctor.EssSurj := by
  letI : IsSplitEpi (W.Q.map f) := isSplitEpi_Q_map_of_W_comp W f s hs
  exact quotientRepresentativeMap_essSurj_of_isSplitEpi W R D (W.Q.map f)

/-- A source W-composite starting in `g` makes the evaluation of `Q(g)`
faithful. This is the left-factor direction of v3.33. -/
theorem quotientRepresentativeMap_Q_map_faithful_of_W_comp
    {Y Z B : Context} (g : Y ⟶ Z) (r : Z ⟶ B)
    (hr : W (g ≫ r)) :
    (quotientRepresentativeMap W R D (W.Q.map g)).toFunctor.Faithful := by
  letI : IsSplitMono (W.Q.map g) := isSplitMono_Q_map_of_W_comp W g r hr
  exact quotientRepresentativeMap_faithful_of_isSplitMono W R D (W.Q.map g)

/-- Source complements whose composites lie in W give separation of the
actual generated quotient evaluations. Neither outer arrow must lie in W. -/
theorem middleIdentityWhiskerSeparating_of_W_composites
    {A X Y Z B : Context} (f : X ⟶ Y) (g : Y ⟶ Z)
    (s : A ⟶ X) (r : Z ⟶ B)
    (hs : W (s ≫ f)) (hr : W (g ≫ r)) :
    MiddleIdentityWhiskerSeparating W R D (W.Q.map f) (W.Q.map g) := by
  exact middleIdentityWhiskerSeparating_of_essSurj_faithful
    W R D (W.Q.map f) (W.Q.map g)
    (quotientRepresentativeMap_Q_map_essSurj_of_W_comp W R D f s hs)
    (quotientRepresentativeMap_Q_map_faithful_of_W_comp W R D g r hr)

/-- The earlier W-edge case is recovered with identity complements. This
requires no identity/composition closure assumption on W itself. -/
theorem middleIdentityWhiskerSeparating_of_W_edges_via_composites
    {X Y Z : Context} (f : X ⟶ Y) (g : Y ⟶ Z)
    (hf : W f) (hg : W g) :
    MiddleIdentityWhiskerSeparating W R D (W.Q.map f) (W.Q.map g) := by
  exact middleIdentityWhiskerSeparating_of_W_composites
    W R D f g (𝟙 X) (𝟙 Z)
    (by simpa only [Category.id_comp] using hf)
    (by simpa only [Category.comp_id] using hg)

/-- Close the actual associator/right-unitor/left-unitor incidence triangle
using constructed source-composite splittings. The correcting witnesses and
the two agreements with the anchor remain explicit hypotheses. -/
theorem associatorAnchor_unitor_overlapStar_triangle_of_W_composites
    {A X Y Z B : Context} (f : X ⟶ Y) (g : Y ⟶ Z)
    (s : A ⟶ X) (r : Z ⟶ B)
    (hs : W (s ≫ f)) (hr : W (g ≫ r))
    (Qs Qt Qu : GeneratedQuotientGaugeParameters W R D)
    (hQs : Qs ∈ quotientRouteCorrectionLocus W R D
      (.associator (W.Q.map f) (𝟙 (W.Q.obj Y)) (W.Q.map g)))
    (hQt : Qt ∈ quotientRouteCorrectionLocus W R D
      (.rightUnitor (W.Q.map f)))
    (hQu : Qu ∈ quotientRouteCorrectionLocus W R D
      (.leftUnitor (W.Q.map g)))
    (hst : AgreeOnRouteFootprintOverlap W R D
      (.associator (W.Q.map f) (𝟙 (W.Q.obj Y)) (W.Q.map g))
      (.rightUnitor (W.Q.map f)) Qs Qt)
    (hsu : AgreeOnRouteFootprintOverlap W R D
      (.associator (W.Q.map f) (𝟙 (W.Q.obj Y)) (W.Q.map g))
      (.leftUnitor (W.Q.map g)) Qs Qu) :
    AgreeOnRouteFootprintOverlap W R D
      (.rightUnitor (W.Q.map f)) (.leftUnitor (W.Q.map g)) Qt Qu := by
  exact associatorAnchor_unitor_overlapStar_triangle_of_separating
    W R D (W.Q.map f) (W.Q.map g) Qs Qt Qu hQs hQt hQu hst hsu
    (middleIdentityWhiskerSeparating_of_W_composites W R D f g s r hs hr)

/-!
## Boundary after v3.34

The new input is concrete source data `W (s ≫ f)` / `W (g ≫ r)`, not an
assumed equality of quotient evaluations or a new gluing axiom. The section
and retraction are built from the formal inverses already in Mathlib's
localization construction. No multiplicativity or saturation of W is needed.

This is a sufficient criterion, not a characterization of split arrows,
semantic EssSurj/Faithful sectors, or the double-whiskering kernel. The W-edge
case is included; strict enlargement is not asserted here. Nor does the
absence of such source complements constitute a noninjectivity witness.

All evaluation statements retain fixed W/R/D. The mixed-triangle theorem
still assumes the three local correcting witnesses and both anchor
agreements. Their existence and simultaneous all-route correlation, general
Stage I, Stage II, and final universality remain separate questions.
-/

end KUOS.DependentOriginationWCompositeSplitSeparationV3_34
