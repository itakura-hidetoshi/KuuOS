import KUOS.DependentOriginationCoboundaryStageSplitV3_02

namespace KUOS.DependentOriginationQuotientGaugeIndependenceV3_03

open CategoryTheory
open CategoryTheory.Bicategory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationQuotientRelationIsoExistenceV2_58
open KUOS.DependentOriginationCoherentQuotientTransportV2_59
open KUOS.DependentOriginationPointwiseGeneralWChoiceV2_61
open KUOS.DependentOriginationFiveGeneratedCorrectionCoboundaryV3_00
open KUOS.DependentOriginationCorrectionCoboundarySolvabilityV3_01
open KUOS.DependentOriginationCoboundaryStageSplitV3_02

universe u v uH vH

/-!
# Quotient-stage gauge independence v3.03

v3.02 splits the five-face correction coboundary into three quotient equations
followed by two comparison equations.  The first stage was still parameterized
by the full v3.00 gauge structure, even though its `mapIsoGauge` field never
appears in the quotient equations.

This file removes that accidental parameter dependence.

A `GeneratedQuotientGaugeParameters` value contains exactly the two
lower-dimensional families consumed by the quotient stage:

* `mapIdGauge`;
* `mapCompGauge`.

Every full generated gauge projects to this quotient-only datum, and every
quotient-only datum extends to a full gauge after an arbitrary choice of
`mapIsoGauge`.  We choose the identity comparison gauge for a canonical
extension.

The main result is

```text
GeneratedGaugeQuotientCoboundary G
  ↔
GeneratedQuotientGaugeCoboundary (quotientPart G).
```

Consequently quotient-stage solvability is exactly an existence problem over
`gId/gComp`; `gIso` is not part of the first obstruction.

No comparison residual is solved here.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- Exactly the lower-dimensional gauge data visible to the three quotient
coherence equations. -/
structure GeneratedQuotientGaugeParameters
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R) where
  mapIdGauge :
    ∀ X : W.Localization,
      (𝟙 (R.obj (.mk X.as.obj))) ≅ 𝟙 (R.obj (.mk X.as.obj))
  mapCompGauge :
    ∀ {X Y Z : W.Localization} (f : X ⟶ Y) (g : Y ⟶ Z),
      (quotientRepresentativeMap W R D f ≫
          quotientRepresentativeMap W R D g) ≅
        (quotientRepresentativeMap W R D f ≫
          quotientRepresentativeMap W R D g)

/-- Forget the comparison gauge family from a full v3.00 gauge. -/
def quotientGaugeParametersOfPointwiseGauge
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (G : GeneratedPointwiseGaugeParameters W R D) :
    GeneratedQuotientGaugeParameters W R D where
  mapIdGauge := G.mapIdGauge
  mapCompGauge := G.mapCompGauge

/-- Extend quotient-only gauge data by an arbitrary comparison gauge family. -/
def extendGeneratedQuotientGaugeParameters
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (Q : GeneratedQuotientGaugeParameters W R D)
    (gIso :
      ∀ {X Y : Context} (f : X ⟶ Y),
        R.map f.toLoc ≅ R.map f.toLoc) :
    GeneratedPointwiseGaugeParameters W R D where
  mapIdGauge := Q.mapIdGauge
  mapCompGauge := Q.mapCompGauge
  mapIsoGauge := gIso

/-- Canonical full extension used to interpret the quotient-only equations.
The identity comparison gauge is deliberately inert at this stage. -/
def canonicalPointwiseGaugeOfQuotientGauge
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (Q : GeneratedQuotientGaugeParameters W R D) :
    GeneratedPointwiseGaugeParameters W R D :=
  extendGeneratedQuotientGaugeParameters W R D Q (fun _ => Iso.refl _)

@[simp]
theorem quotientGaugeParametersOfPointwiseGauge_mapIdGauge
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (G : GeneratedPointwiseGaugeParameters W R D)
    (X : W.Localization) :
    (quotientGaugeParametersOfPointwiseGauge W R D G).mapIdGauge X =
      G.mapIdGauge X := by
  rfl

@[simp]
theorem quotientGaugeParametersOfPointwiseGauge_mapCompGauge
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (G : GeneratedPointwiseGaugeParameters W R D)
    {X Y Z : W.Localization} (f : X ⟶ Y) (g : Y ⟶ Z) :
    (quotientGaugeParametersOfPointwiseGauge W R D G).mapCompGauge f g =
      G.mapCompGauge f g := by
  rfl

@[simp]
theorem canonicalPointwiseGaugeOfQuotientGauge_mapIdGauge
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (Q : GeneratedQuotientGaugeParameters W R D)
    (X : W.Localization) :
    (canonicalPointwiseGaugeOfQuotientGauge W R D Q).mapIdGauge X =
      Q.mapIdGauge X := by
  rfl

@[simp]
theorem canonicalPointwiseGaugeOfQuotientGauge_mapCompGauge
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (Q : GeneratedQuotientGaugeParameters W R D)
    {X Y Z : W.Localization} (f : X ⟶ Y) (g : Y ⟶ Z) :
    (canonicalPointwiseGaugeOfQuotientGauge W R D Q).mapCompGauge f g =
      Q.mapCompGauge f g := by
  rfl

/-- The quotient coboundary stated over the minimal parameter space. -/
def GeneratedQuotientGaugeCoboundary
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (Q : GeneratedQuotientGaugeParameters W R D) : Prop :=
  GeneratedGaugeQuotientCoboundary W R D
    (canonicalPointwiseGaugeOfQuotientGauge W R D Q)

/-- A full-gauge quotient solution descends to its quotient-only projection.
The proof uses only mapId/mapComp projections; mapIso is definitionally absent
from all three equations. -/
theorem generatedQuotientGaugeCoboundary_of_generatedGaugeQuotientCoboundary
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (G : GeneratedPointwiseGaugeParameters W R D)
    (H : GeneratedGaugeQuotientCoboundary W R D G) :
    GeneratedQuotientGaugeCoboundary W R D
      (quotientGaugeParametersOfPointwiseGauge W R D G) := by
  change
    GeneratedGaugeQuotientCoboundary W R D
      (canonicalPointwiseGaugeOfQuotientGauge W R D
        (quotientGaugeParametersOfPointwiseGauge W R D G))
  refine
    { associator := ?_
      leftUnitor := ?_
      rightUnitor := ?_ }
  · intro X Y Z T f g h
    simpa [gaugeAdjustedGeneratedPointwiseChoice,
      canonicalPointwiseGaugeOfQuotientGauge,
      extendGeneratedQuotientGaugeParameters,
      quotientGaugeParametersOfPointwiseGauge] using
      (H.associator f g h)
  · intro X Y f
    simpa [gaugeAdjustedGeneratedPointwiseChoice,
      canonicalPointwiseGaugeOfQuotientGauge,
      extendGeneratedQuotientGaugeParameters,
      quotientGaugeParametersOfPointwiseGauge] using
      (H.leftUnitor f)
  · intro X Y f
    simpa [gaugeAdjustedGeneratedPointwiseChoice,
      canonicalPointwiseGaugeOfQuotientGauge,
      extendGeneratedQuotientGaugeParameters,
      quotientGaugeParametersOfPointwiseGauge] using
      (H.rightUnitor f)

/-- Conversely a quotient-only solution lifts to every full gauge whose
mapId/mapComp projection is the given quotient datum.  In particular it lifts
back to the original G. -/
theorem generatedGaugeQuotientCoboundary_of_generatedQuotientGaugeCoboundary
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (G : GeneratedPointwiseGaugeParameters W R D)
    (H : GeneratedQuotientGaugeCoboundary W R D
      (quotientGaugeParametersOfPointwiseGauge W R D G)) :
    GeneratedGaugeQuotientCoboundary W R D G := by
  change
    GeneratedGaugeQuotientCoboundary W R D
      (canonicalPointwiseGaugeOfQuotientGauge W R D
        (quotientGaugeParametersOfPointwiseGauge W R D G)) at H
  refine
    { associator := ?_
      leftUnitor := ?_
      rightUnitor := ?_ }
  · intro X Y Z T f g h
    simpa [gaugeAdjustedGeneratedPointwiseChoice,
      canonicalPointwiseGaugeOfQuotientGauge,
      extendGeneratedQuotientGaugeParameters,
      quotientGaugeParametersOfPointwiseGauge] using
      (H.associator f g h)
  · intro X Y f
    simpa [gaugeAdjustedGeneratedPointwiseChoice,
      canonicalPointwiseGaugeOfQuotientGauge,
      extendGeneratedQuotientGaugeParameters,
      quotientGaugeParametersOfPointwiseGauge] using
      (H.leftUnitor f)
  · intro X Y f
    simpa [gaugeAdjustedGeneratedPointwiseChoice,
      canonicalPointwiseGaugeOfQuotientGauge,
      extendGeneratedQuotientGaugeParameters,
      quotientGaugeParametersOfPointwiseGauge] using
      (H.rightUnitor f)

/-- Exact parameter-independence theorem for the first obstruction stage. -/
theorem generatedGaugeQuotientCoboundary_iff_quotientGaugeCoboundary
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (G : GeneratedPointwiseGaugeParameters W R D) :
    GeneratedGaugeQuotientCoboundary W R D G ↔
      GeneratedQuotientGaugeCoboundary W R D
        (quotientGaugeParametersOfPointwiseGauge W R D G) := by
  constructor
  · exact
      generatedQuotientGaugeCoboundary_of_generatedGaugeQuotientCoboundary
        W R D G
  · exact
      generatedGaugeQuotientCoboundary_of_generatedQuotientGaugeCoboundary
        W R D G

/-- Quotient-stage solvability over the minimal gId/gComp parameter space. -/
def GeneratedQuotientGaugeCoboundarySolvable
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R) : Prop :=
  ∃ Q : GeneratedQuotientGaugeParameters W R D,
    GeneratedQuotientGaugeCoboundary W R D Q

/-- The v3.02 first-stage existence problem is unchanged after deleting gIso
from its parameter space. -/
theorem generatedQuotientCoboundarySolvable_iff_quotientGaugeCoboundarySolvable
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R) :
    GeneratedQuotientCoboundarySolvable W R D ↔
      GeneratedQuotientGaugeCoboundarySolvable W R D := by
  constructor
  · rintro ⟨G, H⟩
    exact
      ⟨quotientGaugeParametersOfPointwiseGauge W R D G,
        generatedQuotientGaugeCoboundary_of_generatedGaugeQuotientCoboundary
          W R D G H⟩
  · rintro ⟨Q, H⟩
    exact
      ⟨canonicalPointwiseGaugeOfQuotientGauge W R D Q, H⟩

/-!
## Boundary fixed by v3.03

The obstruction filtration is now genuinely staged by dimension:

```text
gId / gComp
    |
    v
three quotient coboundary equations
    |
    v
quotient pseudofunctor carrier
    |
    + choose/lift gIso
    |
    v
two comparison residual equations.
```

The first stage no longer mentions `gIso`, even extensionally.

The next theorem unit should formulate the second stage as an explicit lifting
problem over a fixed solved quotient gauge Q: vary only the comparison gauge
family `gIso`, construct the corresponding full pointwise gauge, and
characterize existence of the two comparison equations.  That is the precise
residual obstruction left after quotient descent.

No claim is made that either stage is automatically solvable from weak
admissibility.
-/

end KUOS.DependentOriginationQuotientGaugeIndependenceV3_03
