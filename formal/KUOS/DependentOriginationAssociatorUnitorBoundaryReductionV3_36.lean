import KUOS.DependentOriginationUnitorWitnessCorrelationV3_35

namespace KUOS.DependentOriginationAssociatorUnitorBoundaryReductionV3_36

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationQuotientGaugeIndependenceV3_03
open KUOS.DependentOriginationThreeRouteCorrectionCompatibilityGapV3_09
open KUOS.DependentOriginationQuotientGaugeIntersectionObstructionV3_11
open KUOS.DependentOriginationQuotientGaugeFootprintOverlapV3_13
open KUOS.DependentOriginationQuotientGaugeCoordinateKeyV3_14
open KUOS.DependentOriginationGlobalFootprintGluingV3_16
open KUOS.DependentOriginationUnitorWitnessCorrelationV3_35

universe u v uH vH

set_option autoImplicit false

/-!
# Associator overlap reduction relative to the unitor boundary v3.36

v3.35 correlates the actual unitor subsystem. This layer identifies exactly
which remaining associator overlap tests can already be mediated through
that same unitor family.

A unitor-visible coordinate is an identity key or a composition key having
an identity factor. On such a key, choose a covering unitor and read its
value. Pairwise compatibility of the unitor restriction proves that the
value agrees with every covering unitor, regardless of that local choice.

An associator family must agree with this boundary wherever visible. Two
associators meeting at a visible coordinate then agree through the same
boundary value. Only their shared coordinates outside the unitor boundary
need a separate associator/associator test.

The result is an equivalence of tests for one fixed selected family, not a
new assertion that compatible associator witnesses exist. The final bridge
retains all route corrections, the v3.35 object-anchor agreements, and both
residual tests before invoking the already proved v3.16 gluing theorem.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- A coordinate in the union of all actual left/right unitor footprints.
The dependent pair keeps the route and its identity object together. -/
def UnitorVisibleCoordinate (c : QuotientGaugeCoordinate W) : Prop :=
  ∃ a : (Σ X : W.Localization, UnitorRouteAt W X),
    RouteFootprintContains W (unitorRouteState W a.2) c

/-- Membership in one unitor footprint supplies a visible-coordinate witness. -/
theorem unitorVisibleCoordinate_of_mem
    {X : W.Localization} (s : UnitorRouteAt W X)
    (c : QuotientGaugeCoordinate W)
    (hc : RouteFootprintContains W (unitorRouteState W s) c) :
    UnitorVisibleCoordinate W c :=
  ⟨⟨X, s⟩, hc⟩

/-- Every identity coordinate belongs to the unitor boundary. -/
theorem identity_unitorVisibleCoordinate (X : W.Localization) :
    UnitorVisibleCoordinate W (.identity X) :=
  unitorVisibleCoordinate_of_mem W (.left (𝟙 X)) (.identity X)
    (unitor_identity_mem W (.left (𝟙 X)))

/-- The boundary is exactly the identity keys and composition keys with an
identity factor. Equalities are equalities of the actual dependent keys. -/
theorem unitorVisibleCoordinate_iff_identity_or_unitComposition
    (c : QuotientGaugeCoordinate W) :
    UnitorVisibleCoordinate W c ↔
      (∃ X : W.Localization, c = .identity X) ∨
      (∃ (X Y : W.Localization) (f : X ⟶ Y), c = .composition (𝟙 X) f) ∨
      (∃ (X Y : W.Localization) (f : X ⟶ Y), c = .composition f (𝟙 Y)) := by
  constructor
  · rintro ⟨⟨X, s⟩, hc⟩
    cases s with
    | left f =>
        change c = .composition (𝟙 X) f ∨ c = .identity X at hc
        rcases hc with hc | hc
        · exact Or.inr (Or.inl ⟨_, _, f, hc⟩)
        · exact Or.inl ⟨X, hc⟩
    | right f =>
        change c = .composition f (𝟙 X) ∨ c = .identity X at hc
        rcases hc with hc | hc
        · exact Or.inr (Or.inr ⟨_, _, f, hc⟩)
        · exact Or.inl ⟨X, hc⟩
  · rintro (⟨X, rfl⟩ | ⟨X, Y, f, rfl⟩ | ⟨X, Y, f, rfl⟩)
    · exact identity_unitorVisibleCoordinate W X
    · exact unitorVisibleCoordinate_of_mem W (.left f)
        (.composition (𝟙 X) f) (Or.inl rfl)
    · exact unitorVisibleCoordinate_of_mem W (.right f)
        (.composition f (𝟙 Y)) (Or.inl rfl)

variable (R : RawHigherContextualSystem.{u, v, uH, vH}
  (Context := Context))
variable (D : PointwiseWAdjointEquivalenceData (W := W) R)

/-- Pairwise compatibility of the unitor restriction of one full family.
No assertion about associator witnesses is built into this predicate. -/
def UnitorRestrictionPairwise
    (Qlocal : ThreeQuotientRouteState W → GeneratedQuotientGaugeParameters W R D) : Prop :=
  ∀ X Y (s : UnitorRouteAt W X) (t : UnitorRouteAt W Y),
    AgreeOnRouteFootprintOverlap W R D
      (unitorRouteState W s) (unitorRouteState W t)
      (Qlocal (unitorRouteState W s)) (Qlocal (unitorRouteState W t))

/-- Read a boundary value from one covering unitor. This is only a section
on visible coordinates, not a newly selected coherent quotient transport. -/
noncomputable def unitorBoundaryValue
    (Qlocal : ThreeQuotientRouteState W → GeneratedQuotientGaugeParameters W R D)
    (c : QuotientGaugeCoordinate W) (hc : UnitorVisibleCoordinate W c) :
    QuotientGaugeCoordinateFiber W R D c :=
  quotientGaugeCoordinateValue W R D
    (Qlocal (unitorRouteState W (Classical.choose hc).2)) c

/-- The boundary read agrees with every covering unitor. Thus the choice of
covering route cannot change the value for this fixed compatible family. -/
theorem unitorBoundaryValue_eq_of_mem
    (Qlocal : ThreeQuotientRouteState W → GeneratedQuotientGaugeParameters W R D)
    (hUnit : UnitorRestrictionPairwise W R D Qlocal)
    {X : W.Localization} (s : UnitorRouteAt W X)
    (c : QuotientGaugeCoordinate W) (hc : UnitorVisibleCoordinate W c)
    (hs : RouteFootprintContains W (unitorRouteState W s) c) :
    unitorBoundaryValue W R D Qlocal c hc =
      quotientGaugeCoordinateValue W R D (Qlocal (unitorRouteState W s)) c := by
  exact hUnit (Classical.choose hc).1 X (Classical.choose hc).2 s c
    (Classical.choose_spec hc) hs

/-- Each selected associator agrees with the same unitor boundary on every
visible coordinate in its actual four-coordinate footprint. -/
def AssociatorBoundaryTests
    (Qlocal : ThreeQuotientRouteState W → GeneratedQuotientGaugeParameters W R D) : Prop :=
  ∀ {X Y Z T : W.Localization} (f : X ⟶ Y) (g : Y ⟶ Z) (h : Z ⟶ T)
      (c : QuotientGaugeCoordinate W),
    RouteFootprintContains W (.associator f g h) c →
    ∀ hc : UnitorVisibleCoordinate W c,
      quotientGaugeCoordinateValue W R D (Qlocal (.associator f g h)) c =
        unitorBoundaryValue W R D Qlocal c hc

/-- Only associator/associator overlaps outside all unitor footprints remain.
"Interior" refers to this set complement, not to a topological interior. -/
def AssociatorInteriorOverlapTests
    (Qlocal : ThreeQuotientRouteState W → GeneratedQuotientGaugeParameters W R D) : Prop :=
  ∀ {X Y Z T X' Y' Z' T' : W.Localization}
      (f : X ⟶ Y) (g : Y ⟶ Z) (h : Z ⟶ T)
      (f' : X' ⟶ Y') (g' : Y' ⟶ Z') (h' : Z' ⟶ T')
      (c : QuotientGaugeCoordinate W),
    RouteFootprintContains W (.associator f g h) c →
    RouteFootprintContains W (.associator f' g' h') c →
    ¬ UnitorVisibleCoordinate W c →
      quotientGaugeCoordinateValue W R D (Qlocal (.associator f g h)) c =
        quotientGaugeCoordinateValue W R D (Qlocal (.associator f' g' h')) c

/-- Lossless reduction of all v3.35 associator overlap tests. The visible
associator/associator comparisons factor through one common boundary value. -/
theorem associatorOverlapTests_iff_boundary_and_interior
    (Qlocal : ThreeQuotientRouteState W → GeneratedQuotientGaugeParameters W R D)
    (hUnit : UnitorRestrictionPairwise W R D Qlocal) :
    AssociatorOverlapTests W R D Qlocal ↔
      AssociatorBoundaryTests W R D Qlocal ∧
        AssociatorInteriorOverlapTests W R D Qlocal := by
  classical
  constructor
  · intro hAll
    constructor
    · intro X Y Z T f g h c hsc hc
      exact hAll f g h (unitorRouteState W (Classical.choose hc).2) c hsc
        (Classical.choose_spec hc)
    · intro X Y Z T X' Y' Z' T' f g h f' g' h' c hsc htc _hc
      exact hAll f g h (.associator f' g' h') c hsc htc
  · rintro ⟨hBoundary, hInterior⟩
    intro X Y Z T f g h t c hsc htc
    by_cases hc : UnitorVisibleCoordinate W c
    · have hs := hBoundary f g h c hsc hc
      cases t with
      | associator f' g' h' =>
          exact hs.trans (hBoundary f' g' h' c htc hc).symm
      | leftUnitor f' =>
          exact hs.trans
            (unitorBoundaryValue_eq_of_mem W R D Qlocal hUnit (.left f') c hc htc)
      | rightUnitor f' =>
          exact hs.trans
            (unitorBoundaryValue_eq_of_mem W R D Qlocal hUnit (.right f') c hc htc)
    · cases t with
      | associator f' g' h' =>
          exact hInterior f g h f' g' h' c hsc htc hc
      | leftUnitor f' =>
          exact False.elim (hc (unitorVisibleCoordinate_of_mem W (.left f') c htc))
      | rightUnitor f' =>
          exact False.elim (hc (unitorVisibleCoordinate_of_mem W (.right f') c htc))

/-- The actual v3.35 object-anchor construction supplies the unitor premise
of the reduction. All associator hypotheses remain on the same full family. -/
theorem globalFamily_of_unitorAnchors_of_boundary_and_interior
    (Qlocal : ThreeQuotientRouteState W → GeneratedQuotientGaugeParameters W R D)
    (hCorrect : ∀ s, Qlocal s ∈ quotientRouteCorrectionLocus W R D s)
    (Q0 : W.Localization → GeneratedQuotientGaugeParameters W R D)
    (hAnchor : ∀ X (s : UnitorRouteAt W X),
      AgreeOnRouteFootprintOverlap W R D (.leftUnitor (𝟙 X))
        (unitorRouteState W s) (Q0 X) (Qlocal (unitorRouteState W s)))
    (hBoundary : AssociatorBoundaryTests W R D Qlocal)
    (hInterior : AssociatorInteriorOverlapTests W R D Qlocal) :
    HasGloballyCompatibleLocalCorrectionFamily W R D := by
  have hUnit : UnitorRestrictionPairwise W R D Qlocal :=
    unitorFamily_pairwise_of_identity_anchors W R D Q0
      (fun X s => Qlocal (unitorRouteState W s))
      (fun X s => hCorrect (unitorRouteState W s)) hAnchor
  exact globalFamily_of_unitorAnchors_of_associatorTests W R D
    Qlocal hCorrect Q0 hAnchor
    ((associatorOverlapTests_iff_boundary_and_interior W R D Qlocal hUnit).2
      ⟨hBoundary, hInterior⟩)

/-- Invoke v3.16 gluing after the reduced tests, without redoing patching. -/
theorem finiteFootprintAmalgamation_of_unitorAnchors_of_boundary_and_interior
    (Qlocal : ThreeQuotientRouteState W → GeneratedQuotientGaugeParameters W R D)
    (hCorrect : ∀ s, Qlocal s ∈ quotientRouteCorrectionLocus W R D s)
    (Q0 : W.Localization → GeneratedQuotientGaugeParameters W R D)
    (hAnchor : ∀ X (s : UnitorRouteAt W X),
      AgreeOnRouteFootprintOverlap W R D (.leftUnitor (𝟙 X))
        (unitorRouteState W s) (Q0 X) (Qlocal (unitorRouteState W s)))
    (hBoundary : AssociatorBoundaryTests W R D Qlocal)
    (hInterior : AssociatorInteriorOverlapTests W R D Qlocal) :
    HasFiniteFootprintAmalgamation W R D := by
  exact hasFiniteFootprintAmalgamation_of_globalFamily W R D
    (globalFamily_of_unitorAnchors_of_boundary_and_interior
      W R D Qlocal hCorrect Q0 hAnchor hBoundary hInterior)

/-!
## Boundary

This is a test-reduction theorem relative to one full selected family. The
v3.35 unitor existence theorem does not by itself produce associator witnesses
satisfying the boundary and interior tests. Nor is the residual interior test
inferred from the absence of a unitor coordinate.

The local covering choice is value-independent for a fixed compatible unitor
restriction; no independence from W/R/D or from a different unitor family is
claimed. No new gluing axiom, separation assumption, normalization assumption,
or all-route star-transitivity premise is introduced. Existing corrected
route equations and mixed-triangle hypotheses are unchanged. General Stage I,
Stage II, comparison coherence and final universality remain separate goals.
-/

end KUOS.DependentOriginationAssociatorUnitorBoundaryReductionV3_36
