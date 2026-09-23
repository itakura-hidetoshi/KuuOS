import KUOS.DependentOriginationFreshBoundaryRightIdentityReductionV3_53

namespace KUOS.DependentOriginationCompositeIdentityInversePairReductionV3_54

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationQuotientGaugeIndependenceV3_03
open KUOS.DependentOriginationThreeRouteCorrectionCompatibilityGapV3_09
open KUOS.DependentOriginationQuotientGaugeIntersectionObstructionV3_11
open KUOS.DependentOriginationUnitorWitnessCorrelationV3_35
open KUOS.DependentOriginationFreshBoundaryCompatibilityV3_47
open KUOS.DependentOriginationCollisionAbsorptionReductionV3_49
open KUOS.DependentOriginationGlobalCancellationFromSourceComplementsV3_52
open KUOS.DependentOriginationFreshBoundaryRightIdentityReductionV3_53

universe u v uH vH

set_option autoImplicit false

noncomputable section

/-!
# Composite-identity inverse-pair reduction v3.54

v3.53 reduces every still-open fresh-boundary obstruction, under a common
unitor gauge, to the branch

```text
f : X ⟶ Y
g : Y ⟶ X
f ≫ g = 𝟙 X.
```

The next truth test is whether the global cancellation geometry of v3.52 makes
this branch degenerate enough to disappear.

The first part is positive and purely categorical.  If `f` is epi, or
dually if `g` is mono, then `f ≫ g = 𝟙 X` forces

```text
g ≫ f = 𝟙 Y.
```

Thus either directional global source-complement hypothesis from v3.52 turns
the composite-identity branch into an actual inverse pair, and hence an
isomorphism.

The second part is deliberately conservative.  This reduction alone does not
prove the associator corrected.  The v3.37 solved leading value still depends
on the nontrivial suffix coordinate `mapComp f g`.  Common unitors control
unit-composition coordinates, but no theorem proved so far identifies that
inverse-pair composition coordinate with a unitor coordinate.  Therefore this
module records the strongest justified reduction and leaves semantic
elimination of the inverse-pair branch as the next obstruction question.

No weak-admissibility derivation of source complements, no automatic
fresh-boundary correction, and no Stage I/II or final universality claim is
made here.  Protected validation-only PR #1558 is untouched.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- A composite-identity associator whose first two arrows are two-sided
inverses.  The task packaging keeps the original third arrow unchanged. -/
def IsCompositeInversePairAssociatorTask (a : AssociatorTask W) : Prop :=
  ∃ (X Y T : W.Localization)
      (f : X ⟶ Y) (g : Y ⟶ X) (h : X ⟶ T),
    f ≫ g = 𝟙 X ∧
      g ≫ f = 𝟙 Y ∧
      a =
        ({ X := X, Y := Y, Z := X, T := T,
           f := f, g := g, h := h } : AssociatorTask W)

/-- A right inverse of an epi is automatically also a left inverse. -/
theorem compositeIdentity_gf_eq_id_of_epi
    {X Y : W.Localization}
    (f : X ⟶ Y) (g : Y ⟶ X) [Epi f]
    (hfg : f ≫ g = 𝟙 X) :
    g ≫ f = 𝟙 Y := by
  apply endomorphism_eq_id_of_leftAbsorption_of_epi W f (g ≫ f)
  calc
    f = (𝟙 X) ≫ f := by simp
    _ = (f ≫ g) ≫ f := by rw [hfg]
    _ = f ≫ (g ≫ f) := by simp only [Category.assoc]

/-- Dually, a left inverse of a mono is automatically also a right inverse. -/
theorem compositeIdentity_gf_eq_id_of_mono
    {X Y : W.Localization}
    (f : X ⟶ Y) (g : Y ⟶ X) [Mono g]
    (hfg : f ≫ g = 𝟙 X) :
    g ≫ f = 𝟙 Y := by
  apply endomorphism_eq_id_of_rightAbsorption_of_mono W (g ≫ f) g
  calc
    (g ≫ f) ≫ g = g ≫ (f ≫ g) := by simp only [Category.assoc]
    _ = g ≫ 𝟙 X := by rw [hfg]
    _ = g := by simp

/-- The epi route packages the composite-identity pair as an actual
Mathlib isomorphism. -/
def compositeIdentityIsoOfEpi
    {X Y : W.Localization}
    (f : X ⟶ Y) (g : Y ⟶ X) [Epi f]
    (hfg : f ≫ g = 𝟙 X) :
    X ≅ Y where
  hom := f
  inv := g
  hom_inv_id := hfg
  inv_hom_id := compositeIdentity_gf_eq_id_of_epi W f g hfg

/-- The mono route gives the same two-sided inverse package. -/
def compositeIdentityIsoOfMono
    {X Y : W.Localization}
    (f : X ⟶ Y) (g : Y ⟶ X) [Mono g]
    (hfg : f ≫ g = 𝟙 X) :
    X ≅ Y where
  hom := f
  inv := g
  hom_inv_id := hfg
  inv_hom_id := compositeIdentity_gf_eq_id_of_mono W f g hfg

/-- Global left source complements suffice to upgrade every packaged
composite-identity task to the two-sided inverse-pair sector. -/
theorem compositeIdentityTask_isInversePair_of_leftSourceComplements
    (hLeft : HasLeftWCompositeComplements W)
    (a : AssociatorTask W)
    (hComposite : IsCompositeIdentityAssociatorTask W a) :
    IsCompositeInversePairAssociatorTask W a := by
  rcases hComposite with ⟨X, Y, T, f, g, h, hfg, rfl⟩
  have hEpi : Epi f :=
    allLocalizationArrows_epi_of_leftWCompositeComplements W hLeft f
  letI : Epi f := hEpi
  have hgf : g ≫ f = 𝟙 Y :=
    compositeIdentity_gf_eq_id_of_epi W f g hfg
  exact ⟨X, Y, T, f, g, h, hfg, hgf, rfl⟩

/-- Global right source complements give the same upgrade by mono
cancellation. -/
theorem compositeIdentityTask_isInversePair_of_rightSourceComplements
    (hRight : HasRightWCompositeComplements W)
    (a : AssociatorTask W)
    (hComposite : IsCompositeIdentityAssociatorTask W a) :
    IsCompositeInversePairAssociatorTask W a := by
  rcases hComposite with ⟨X, Y, T, f, g, h, hfg, rfl⟩
  have hMono : Mono g :=
    allLocalizationArrows_mono_of_rightWCompositeComplements W hRight g
  letI : Mono g := hMono
  have hgf : g ≫ f = 𝟙 Y :=
    compositeIdentity_gf_eq_id_of_mono W f g hfg
  exact ⟨X, Y, T, f, g, h, hfg, hgf, rfl⟩

variable (R : RawHigherContextualSystem.{u, v, uH, vH}
  (Context := Context))
variable (D : PointwiseWAdjointEquivalenceData (W := W) R)

/-- Under a common unitor gauge, any surviving fresh-boundary obstruction is
not merely composite-identity: one directional global source-complement
hypothesis already makes its first two arrows a genuine inverse pair. -/
theorem freshBoundaryLeadingObstruction_isCompositeInversePair_of_leftSourceComplements
    (Q : GeneratedQuotientGaugeParameters W R D)
    (hUnit : ∀ X (s : UnitorRouteAt W X),
      Q ∈ quotientRouteCorrectionLocus W R D (unitorRouteState W s))
    (hLeft : HasLeftWCompositeComplements W)
    (a : AssociatorTask W)
    (hObstruction : FreshBoundaryLeadingObstruction W R D Q a) :
    IsCompositeInversePairAssociatorTask W a := by
  have hComposite : IsCompositeIdentityAssociatorTask W a :=
    freshBoundaryLeadingObstruction_isCompositeIdentity_of_unitors
      W R D Q hUnit a hObstruction
  exact
    compositeIdentityTask_isInversePair_of_leftSourceComplements
      W hLeft a hComposite

/-- Dual obstruction reduction using the global right-complement hypothesis. -/
theorem freshBoundaryLeadingObstruction_isCompositeInversePair_of_rightSourceComplements
    (Q : GeneratedQuotientGaugeParameters W R D)
    (hUnit : ∀ X (s : UnitorRouteAt W X),
      Q ∈ quotientRouteCorrectionLocus W R D (unitorRouteState W s))
    (hRight : HasRightWCompositeComplements W)
    (a : AssociatorTask W)
    (hObstruction : FreshBoundaryLeadingObstruction W R D Q a) :
    IsCompositeInversePairAssociatorTask W a := by
  have hComposite : IsCompositeIdentityAssociatorTask W a :=
    freshBoundaryLeadingObstruction_isCompositeIdentity_of_unitors
      W R D Q hUnit a hObstruction
  exact
    compositeIdentityTask_isInversePair_of_rightSourceComplements
      W hRight a hComposite

/-!
## Boundary after v3.54

The equation `f ≫ g = 𝟙` is no longer merely a one-sided split condition once
v3.52 cancellation is available: either global complement direction separately
forces `g ≫ f = 𝟙`.  Thus every surviving v3.53 fresh-boundary obstruction
lies over an actual inverse pair.

This is a genuine reduction, but not yet an elimination.  In the associator
equation for `associator f g h`, the suffix still contains the adjusted
composition isomorphism for `f` and `g`.  Two-sided invertibility of the
source arrows does not by itself identify that gauge coordinate with one
already fixed by the left/right unitor equations.

The next theorem unit should therefore truth-test the exact inverse-pair
compatibility equation.  If native bicategory coherence plus the existing
quotient transport data forces it, the fresh-boundary residual disappears.
If not, the inverse-pair equation should be retained as the final explicit
boundary obstruction rather than hidden behind a stronger unsupported claim.
-/

end

end KUOS.DependentOriginationCompositeIdentityInversePairReductionV3_54
