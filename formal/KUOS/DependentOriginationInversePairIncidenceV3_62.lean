import KUOS.DependentOriginationCounterGaugeFiberNontrivialV3_61

namespace KUOS.DependentOriginationInversePairIncidenceV3_62

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationQuotientGaugeCoordinateKeyV3_14
open KUOS.DependentOriginationUnitorWitnessCorrelationV3_35
open KUOS.DependentOriginationAssociatorUnitorBoundaryReductionV3_36
open KUOS.DependentOriginationFreshAssociatorCompletionV3_37
open KUOS.DependentOriginationFiniteAssociatorScheduleV3_38
open KUOS.DependentOriginationFreshBoundaryCompatibilityV3_47
open KUOS.DependentOriginationCollisionObjectGeometryV3_48
open KUOS.DependentOriginationCompositeIdentityInversePairReductionV3_54
open KUOS.DependentOriginationInversePairSuffixPerturbationV3_59

universe u v

set_option autoImplicit false

noncomputable section

/-!
# Object-separated inverse-pair incidence v3.62

v3.61 discharges the exact local algebraic input from v3.60 in the concrete
`C2` countermodel: every composition-coordinate quotient-gauge fiber is
nontrivial.

The remaining suffix-perturbation hypotheses are incidence statements.  This
file isolates their purely object-level content before choosing a concrete
octahedral localization task.

For a composable pair

```text
X --f--> Y --g--> Z
```

a composition coordinate `gComp(f,g)` can lie on the unitor boundary only if
one of the adjacent objects is equal.  This follows by projecting exact
dependent coordinate equalities to their source/middle/target objects.

Specializing to an inverse-pair-shaped associator

```text
X --f--> Y --g--> X --h--> T,
```

the single separation `X ≠ Y` therefore removes `gComp(f,g)` from every
unitor footprint.  Together with `X ≠ T`, it also separates that suffix from
all three other associator coordinates.

If in addition `f ≫ g = 𝟙 X`, the leading coordinate is literally the
left-unitor-visible key `gComp(𝟙 X,h)`.  Object separation also gives leading
freshness.  Hence an object-separated inverse pair automatically supplies the
fresh-boundary and isolated-suffix geometry required by v3.60.

No concrete octahedral arrows are selected here.  The next truth test can
therefore focus only on exhibiting three distinct localization objects and an
inverse pair between the first two.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- A composition coordinate between two genuinely adjacent-distinct object
boundaries cannot occur in any left- or right-unitor footprint. -/
theorem composition_not_unitorVisible_of_adjacent_objects_ne
    {X Y Z : W.Localization}
    (f : X ⟶ Y) (g : Y ⟶ Z)
    (hXY : X ≠ Y) (hYZ : Y ≠ Z) :
    ¬ UnitorVisibleCoordinate W (.composition f g) := by
  intro hVisible
  rcases
      (composition_unitorVisible_iff_unitComposition W f g).1 hVisible with
    hLeft | hRight
  · rcases hLeft with ⟨A, B, k, hEq⟩
    have hSource := congrArg (quotientCoordinateSource W) hEq
    have hMiddle := congrArg (quotientCoordinateMiddle W) hEq
    change X = A at hSource
    change Y = A at hMiddle
    exact hXY (hSource.trans hMiddle.symm)
  · rcases hRight with ⟨A, B, k, hEq⟩
    have hMiddle := congrArg (quotientCoordinateMiddle W) hEq
    have hTarget := congrArg (quotientCoordinateTarget W) hEq
    change Y = B at hMiddle
    change Z = B at hTarget
    exact hYZ (hMiddle.trans hTarget.symm)

/-- For inverse-pair object shape `X -> Y -> X`, separation `X ≠ Y`
already makes the `gComp(f,g)` suffix invisible to every unitor. -/
theorem inversePairShape_fg_not_unitorVisible
    {X Y : W.Localization}
    (f : X ⟶ Y) (g : Y ⟶ X)
    (hXY : X ≠ Y) :
    ¬ UnitorVisibleCoordinate W (.composition f g) := by
  exact
    composition_not_unitorVisible_of_adjacent_objects_ne
      W f g hXY (by
        intro hYX
        exact hXY hYX.symm)

/-- Object separation isolates the `gComp(f,g)` suffix from every other
associator coordinate in an inverse-pair-shaped task.

No inverse equations are needed for this incidence statement. -/
theorem inversePairShape_fgInteriorIsolated_of_objects_ne
    {X Y T : W.Localization}
    (f : X ⟶ Y) (g : Y ⟶ X) (h : X ⟶ T)
    (hXY : X ≠ Y) (hXT : X ≠ T) :
    AssociatorFGInteriorIsolated W f g h := by
  refine ⟨?_, ?_, ?_, ?_⟩
  · intro hEq
    have hMiddle := congrArg (quotientCoordinateMiddle W) hEq
    change Y = X at hMiddle
    exact hXY hMiddle.symm
  · intro hEq
    have hSource := congrArg (quotientCoordinateSource W) hEq
    change X = Y at hSource
    exact hXY hSource
  · intro hEq
    have hTarget := congrArg (quotientCoordinateTarget W) hEq
    change X = T at hTarget
    exact hXT hTarget
  · exact inversePairShape_fg_not_unitorVisible W f g hXY

/-- A composite identity on an object-separated inverse-pair shape is
automatically a fresh-boundary associator task.

Freshness comes from v3.48 object separation; boundary visibility comes from
the literal rewrite `f ≫ g = 𝟙 X`. -/
theorem inversePairShape_freshBoundary_of_compositeIdentity_of_object_ne
    {X Y T : W.Localization}
    (f : X ⟶ Y) (g : Y ⟶ X) (h : X ⟶ T)
    (hfg : f ≫ g = 𝟙 X)
    (hXY : X ≠ Y) :
    FreshBoundaryAssociatorTask W
      ({ X := X, Y := Y, Z := X, T := T,
         f := f, g := g, h := h } : AssociatorTask W) := by
  let a : AssociatorTask W :=
    { X := X, Y := Y, Z := X, T := T,
      f := f, g := g, h := h }
  have hSeparated : CollisionObjectSeparated W a := by
    refine ⟨?_, ?_⟩
    · simpa [a] using hXY
    · dsimp [a]
      intro hYX
      exact hXY hYX.symm
  have hFresh :
      FreshAssociatorLeadingCoordinate W f g h := by
    simpa [a] using
      freshAssociatorLeadingCoordinate_of_collisionObjectSeparated
        W a hSeparated
  have hVisible :
      UnitorVisibleCoordinate W
        (QuotientGaugeCoordinate.composition (f ≫ g) h) := by
    rw [hfg]
    exact
      unitorVisibleCoordinate_of_mem
        W (.left h) (.composition (𝟙 X) h) (Or.inl rfl)
  exact ⟨hFresh, hVisible⟩

/-- Full geometric package used by v3.60: an object-separated two-sided inverse
pair is fresh-boundary and has an isolated `gComp(f,g)` suffix. -/
theorem inversePairTask_freshBoundary_and_fgInteriorIsolated_of_objects_ne
    {X Y T : W.Localization}
    (f : X ⟶ Y) (g : Y ⟶ X) (h : X ⟶ T)
    (hfg : f ≫ g = 𝟙 X)
    (hgf : g ≫ f = 𝟙 Y)
    (hXY : X ≠ Y) (hXT : X ≠ T) :
    FreshBoundaryAssociatorTask W
        ({ X := X, Y := Y, Z := X, T := T,
           f := f, g := g, h := h } : AssociatorTask W) ∧
      IsCompositeInversePairAssociatorTask W
        ({ X := X, Y := Y, Z := X, T := T,
           f := f, g := g, h := h } : AssociatorTask W) ∧
      AssociatorFGInteriorIsolated W f g h := by
  refine ⟨
    inversePairShape_freshBoundary_of_compositeIdentity_of_object_ne
      W f g h hfg hXY,
    ?_,
    inversePairShape_fgInteriorIsolated_of_objects_ne
      W f g h hXY hXT⟩
  exact ⟨X, Y, T, f, g, h, hfg, hgf, rfl⟩

/-!
## Boundary after v3.62

For an inverse-pair-shaped task the v3.60 incidence hypotheses reduce to
ordinary object inequality:

```text
X ≠ Y
X ≠ T
f ≫ g = 𝟙 X
g ≫ f = 𝟙 Y
--------------------------------
fresh-boundary task
+ exact inverse pair
+ isolated gComp(f,g).
```

Combined with v3.61, the concrete `C2` model no longer needs a separate gauge
fiber nontriviality proof or a coordinate-by-coordinate isolation argument.

The next concrete unit should select localization objects corresponding to
three distinct octahedral vertices, use `allMorphisms.Q.map` together with
the Mathlib localization inverse, and prove the two object inequalities through
the canonical localization object equivalence.  Only after that exact
construction is established should v3.60 be invoked.

No common unitor gauge is constructed here, and no concrete v2.69 exact
obstruction is claimed yet.
-/

end

end KUOS.DependentOriginationInversePairIncidenceV3_62
