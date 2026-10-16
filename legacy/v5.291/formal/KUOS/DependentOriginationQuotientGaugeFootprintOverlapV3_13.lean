import KUOS.DependentOriginationQuotientGaugeCoordinateFootprintV3_12

namespace KUOS.DependentOriginationQuotientGaugeFootprintOverlapV3_13

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationQuotientGaugeIndependenceV3_03
open KUOS.DependentOriginationThreeRouteCorrectionCompatibilityGapV3_09
open KUOS.DependentOriginationQuotientGaugeIntersectionObstructionV3_11
open KUOS.DependentOriginationQuotientGaugeCoordinateFootprintV3_12

universe u v uH vH

/-!
# Pairwise overlap compatibility of quotient-gauge footprints v3.13

v3.12 reduces the first higher-localization obstruction to amalgamation of
finite quotient-gauge coordinate footprints.  This file isolates the first
necessary gluing condition: two local correcting gauges must admit one common
extension over the union of their two inspected footprints.

No Helly theorem, compactness, convexity, topology, or global gluing principle
is assumed.  Pairwise compatibility is proved only as a necessary consequence
of a genuine finite-footprint amalgamation.

The definition below is coordinate-independent but concrete: two local gauges
are compatible on the overlap of route states `s` and `t` when there exists a
single quotient gauge whose restriction to the footprint of `s` agrees with
the first local gauge and whose restriction to the footprint of `t` agrees
with the second.

The explicit lemmas then show that this forces equality on genuinely shared
coordinates such as:

* the common `gId X` coordinate of left/left, right/right, and left/right
  unitor states;
* the common `gComp (𝟙 X) f` coordinate of
  `associator (𝟙 X) f g` and `leftUnitor f`;
* the common `gComp g (𝟙 Z)` coordinate of
  `associator f g (𝟙 Z)` and `rightUnitor g`.

Thus pairwise overlap compatibility is not a semantic proxy: it has observable
coordinate consequences in the actual `gId/gComp` gauge space.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- Two statewise quotient gauges are compatible on their finite route
footprints when one quotient gauge extends both local restrictions
simultaneously.  The extending gauge is allowed to depend on the pair of
states; therefore this is strictly a pairwise condition, not global
amalgamation. -/
def CompatibleOnRouteOverlap
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (s t : ThreeQuotientRouteState W)
    (Qs Qt : GeneratedQuotientGaugeParameters W R D) : Prop :=
  ∃ Q : GeneratedQuotientGaugeParameters W R D,
    QuotientGaugesAgreeOnRouteState W R D Q Qs s ∧
      QuotientGaugesAgreeOnRouteState W R D Q Qt t

/-- Pairwise overlap compatibility is symmetric. -/
theorem compatibleOnRouteOverlap_symm
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (s t : ThreeQuotientRouteState W)
    (Qs Qt : GeneratedQuotientGaugeParameters W R D) :
    CompatibleOnRouteOverlap W R D s t Qs Qt ↔
      CompatibleOnRouteOverlap W R D t s Qt Qs := by
  constructor
  · rintro ⟨Q, hs, ht⟩
    exact ⟨Q, ht, hs⟩
  · rintro ⟨Q, ht, hs⟩
    exact ⟨Q, hs, ht⟩

/-- A common footprint restriction immediately witnesses pairwise overlap
compatibility. -/
theorem compatibleOnRouteOverlap_of_commonRestriction
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (s t : ThreeQuotientRouteState W)
    (Q Qs Qt : GeneratedQuotientGaugeParameters W R D)
    (hs : QuotientGaugesAgreeOnRouteState W R D Q Qs s)
    (ht : QuotientGaugesAgreeOnRouteState W R D Q Qt t) :
    CompatibleOnRouteOverlap W R D s t Qs Qt :=
  ⟨Q, hs, ht⟩

/-- Two left-unitor footprints with the same source object share the identity
coordinate `gId X`; pairwise compatibility forces their local values there to
agree. -/
theorem mapId_eq_of_compatible_leftUnitor_leftUnitor
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y Z : W.Localization}
    (f : X ⟶ Y) (g : X ⟶ Z)
    (Qs Qt : GeneratedQuotientGaugeParameters W R D)
    (H : CompatibleOnRouteOverlap W R D
      (.leftUnitor f) (.leftUnitor g) Qs Qt) :
    Qs.mapIdGauge X = Qt.mapIdGauge X := by
  rcases H with ⟨Q, hs, ht⟩
  have hs' :
      Q.mapCompGauge (𝟙 X) f = Qs.mapCompGauge (𝟙 X) f ∧
        Q.mapIdGauge X = Qs.mapIdGauge X := by
    simpa [QuotientGaugesAgreeOnRouteState] using hs
  have ht' :
      Q.mapCompGauge (𝟙 X) g = Qt.mapCompGauge (𝟙 X) g ∧
        Q.mapIdGauge X = Qt.mapIdGauge X := by
    simpa [QuotientGaugesAgreeOnRouteState] using ht
  exact hs'.2.symm.trans ht'.2

/-- Two right-unitor footprints with the same target object share the identity
coordinate `gId Y`. -/
theorem mapId_eq_of_compatible_rightUnitor_rightUnitor
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Z Y : W.Localization}
    (f : X ⟶ Y) (g : Z ⟶ Y)
    (Qs Qt : GeneratedQuotientGaugeParameters W R D)
    (H : CompatibleOnRouteOverlap W R D
      (.rightUnitor f) (.rightUnitor g) Qs Qt) :
    Qs.mapIdGauge Y = Qt.mapIdGauge Y := by
  rcases H with ⟨Q, hs, ht⟩
  have hs' :
      Q.mapCompGauge f (𝟙 Y) = Qs.mapCompGauge f (𝟙 Y) ∧
        Q.mapIdGauge Y = Qs.mapIdGauge Y := by
    simpa [QuotientGaugesAgreeOnRouteState] using hs
  have ht' :
      Q.mapCompGauge g (𝟙 Y) = Qt.mapCompGauge g (𝟙 Y) ∧
        Q.mapIdGauge Y = Qt.mapIdGauge Y := by
    simpa [QuotientGaugesAgreeOnRouteState] using ht
  exact hs'.2.symm.trans ht'.2

/-- A left-unitor state at `f : X ⟶ Y` and a right-unitor state ending at
`X` share the same identity coordinate `gId X`. -/
theorem mapId_eq_of_compatible_leftUnitor_rightUnitor
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {Z X Y : W.Localization}
    (f : X ⟶ Y) (g : Z ⟶ X)
    (Qs Qt : GeneratedQuotientGaugeParameters W R D)
    (H : CompatibleOnRouteOverlap W R D
      (.leftUnitor f) (.rightUnitor g) Qs Qt) :
    Qs.mapIdGauge X = Qt.mapIdGauge X := by
  rcases H with ⟨Q, hs, ht⟩
  have hs' :
      Q.mapCompGauge (𝟙 X) f = Qs.mapCompGauge (𝟙 X) f ∧
        Q.mapIdGauge X = Qs.mapIdGauge X := by
    simpa [QuotientGaugesAgreeOnRouteState] using hs
  have ht' :
      Q.mapCompGauge g (𝟙 X) = Qt.mapCompGauge g (𝟙 X) ∧
        Q.mapIdGauge X = Qt.mapIdGauge X := by
    simpa [QuotientGaugesAgreeOnRouteState] using ht
  exact hs'.2.symm.trans ht'.2

/-- The associator state `(𝟙 X,f,g)` and the left-unitor state at `f`
share the composition coordinate `gComp (𝟙 X) f`. -/
theorem mapComp_eq_of_compatible_associator_leftUnitor
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y Z : W.Localization}
    (f : X ⟶ Y) (g : Y ⟶ Z)
    (Qs Qt : GeneratedQuotientGaugeParameters W R D)
    (H : CompatibleOnRouteOverlap W R D
      (.associator (𝟙 X) f g) (.leftUnitor f) Qs Qt) :
    Qs.mapCompGauge (𝟙 X) f = Qt.mapCompGauge (𝟙 X) f := by
  rcases H with ⟨Q, hs, ht⟩
  have hs' :
      Q.mapCompGauge ((𝟙 X) ≫ f) g =
          Qs.mapCompGauge ((𝟙 X) ≫ f) g ∧
      Q.mapCompGauge (𝟙 X) f = Qs.mapCompGauge (𝟙 X) f ∧
      Q.mapCompGauge f g = Qs.mapCompGauge f g ∧
      Q.mapCompGauge (𝟙 X) (f ≫ g) =
          Qs.mapCompGauge (𝟙 X) (f ≫ g) := by
    simpa [QuotientGaugesAgreeOnRouteState] using hs
  have ht' :
      Q.mapCompGauge (𝟙 X) f = Qt.mapCompGauge (𝟙 X) f ∧
        Q.mapIdGauge X = Qt.mapIdGauge X := by
    simpa [QuotientGaugesAgreeOnRouteState] using ht
  exact hs'.2.1.symm.trans ht'.1

/-- The associator state `(f,g,𝟙 Z)` and the right-unitor state at `g`
share the composition coordinate `gComp g (𝟙 Z)`. -/
theorem mapComp_eq_of_compatible_associator_rightUnitor
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    {X Y Z : W.Localization}
    (f : X ⟶ Y) (g : Y ⟶ Z)
    (Qs Qt : GeneratedQuotientGaugeParameters W R D)
    (H : CompatibleOnRouteOverlap W R D
      (.associator f g (𝟙 Z)) (.rightUnitor g) Qs Qt) :
    Qs.mapCompGauge g (𝟙 Z) = Qt.mapCompGauge g (𝟙 Z) := by
  rcases H with ⟨Q, hs, ht⟩
  have hs' :
      Q.mapCompGauge (f ≫ g) (𝟙 Z) =
          Qs.mapCompGauge (f ≫ g) (𝟙 Z) ∧
      Q.mapCompGauge f g = Qs.mapCompGauge f g ∧
      Q.mapCompGauge g (𝟙 Z) = Qs.mapCompGauge g (𝟙 Z) ∧
      Q.mapCompGauge f (g ≫ 𝟙 Z) =
          Qs.mapCompGauge f (g ≫ 𝟙 Z) := by
    simpa [QuotientGaugesAgreeOnRouteState] using hs
  have ht' :
      Q.mapCompGauge g (𝟙 Z) = Qt.mapCompGauge g (𝟙 Z) ∧
        Q.mapIdGauge Z = Qt.mapIdGauge Z := by
    simpa [QuotientGaugesAgreeOnRouteState] using ht
  exact hs'.2.2.1.symm.trans ht'.1

/-- Named form of the v3.12 finite-footprint amalgamation condition. -/
def HasFiniteFootprintAmalgamation
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R) : Prop :=
  ∃ Q : GeneratedQuotientGaugeParameters W R D,
    ∀ s : ThreeQuotientRouteState W,
      ∃ Qs : GeneratedQuotientGaugeParameters W R D,
        Qs ∈ quotientRouteCorrectionLocus W R D s ∧
          QuotientGaugesAgreeOnRouteState W R D Q Qs s

/-- v3.12 identifies global quotient correction exactly with the named
finite-footprint amalgamation property. -/
theorem commonLocus_nonempty_iff_hasFiniteFootprintAmalgamation
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R) :
    (commonQuotientRouteCorrectionLocus W R D).Nonempty ↔
      HasFiniteFootprintAmalgamation W R D := by
  exact commonLocus_nonempty_iff_finiteFootprintAmalgamation W R D

/-- Every route has a local correcting gauge, and each such local witness can be
paired with a correcting witness for every second route so that the two
footprints admit one common extension.  No single extension is required to work
for all pairs. -/
def HasPairwiseOverlapCompatibleLocalCorrections
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R) : Prop :=
  ∀ s : ThreeQuotientRouteState W,
    ∃ Qs : GeneratedQuotientGaugeParameters W R D,
      Qs ∈ quotientRouteCorrectionLocus W R D s ∧
        ∀ t : ThreeQuotientRouteState W,
          ∃ Qt : GeneratedQuotientGaugeParameters W R D,
            Qt ∈ quotientRouteCorrectionLocus W R D t ∧
              CompatibleOnRouteOverlap W R D s t Qs Qt

/-- Genuine finite-footprint amalgamation implies pairwise overlap
compatibility of local correcting gauges.  This is the first necessary gluing
condition after v3.12. -/
theorem hasPairwiseOverlapCompatibleLocalCorrections_of_finiteFootprintAmalgamation
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (H : HasFiniteFootprintAmalgamation W R D) :
    HasPairwiseOverlapCompatibleLocalCorrections W R D := by
  rcases H with ⟨Q, hQ⟩
  intro s
  rcases hQ s with ⟨Qs, hQs, hs⟩
  refine ⟨Qs, hQs, ?_⟩
  intro t
  rcases hQ t with ⟨Qt, hQt, ht⟩
  exact ⟨Qt, hQt, ⟨Q, hs, ht⟩⟩

/-- In particular, a genuine common quotient gauge forces pairwise overlap
compatibility. -/
theorem hasPairwiseOverlapCompatibleLocalCorrections_of_commonLocus_nonempty
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (H : (commonQuotientRouteCorrectionLocus W R D).Nonempty) :
    HasPairwiseOverlapCompatibleLocalCorrections W R D := by
  exact
    hasPairwiseOverlapCompatibleLocalCorrections_of_finiteFootprintAmalgamation
      W R D
      ((commonLocus_nonempty_iff_hasFiniteFootprintAmalgamation W R D).1 H)

/-- A pairwise-overlap obstruction is the constructive failure of the first
necessary gluing condition despite statewise local correctability. -/
def PairwiseOverlapCompatibilityObstruction
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R) : Prop :=
  AllThreeQuotientRoutesIndividuallyReachable W R D ∧
    ¬ HasPairwiseOverlapCompatibleLocalCorrections W R D

/-- Failure of pairwise overlap compatibility is already a genuine
quotient-gauge intersection obstruction. -/
theorem quotientGaugeIntersectionObstruction_of_pairwiseOverlapCompatibilityObstruction
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (H : PairwiseOverlapCompatibilityObstruction W R D) :
    QuotientGaugeIntersectionObstruction W R D := by
  rcases H with ⟨hPoint, hNoPairwise⟩
  refine ⟨
    (allThreeQuotientRoutesIndividuallyReachable_iff_loci_nonempty W R D).1
      hPoint,
    ?_⟩
  intro hCommon
  exact hNoPairwise
    (hasPairwiseOverlapCompatibleLocalCorrections_of_commonLocus_nonempty
      W R D hCommon)

/-- The next possible obstruction layer: all local routes are correctable and
all pairwise footprint overlaps can be made compatible, but no one global gauge
amalgamates every footprint.  This file does not assert that such a gap exists;
it isolates the exact proposition that v3.14 should test. -/
def PairwiseCompatibleButNoGlobalAmalgamation
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R) : Prop :=
  AllThreeQuotientRoutesIndividuallyReachable W R D ∧
    HasPairwiseOverlapCompatibleLocalCorrections W R D ∧
      ¬ HasFiniteFootprintAmalgamation W R D

/-- Any pairwise-compatible-but-nonglobal gap is still an instance of the
v3.11 quotient intersection obstruction. -/
theorem quotientGaugeIntersectionObstruction_of_pairwiseCompatibleButNoGlobal
    (R : RawHigherContextualSystem.{u, v, uH, vH}
      (Context := Context))
    (D : PointwiseWAdjointEquivalenceData (W := W) R)
    (H : PairwiseCompatibleButNoGlobalAmalgamation W R D) :
    QuotientGaugeIntersectionObstruction W R D := by
  rcases H with ⟨hPoint, _hPairwise, hNoGlobal⟩
  refine ⟨
    (allThreeQuotientRoutesIndividuallyReachable_iff_loci_nonempty W R D).1
      hPoint,
    ?_⟩
  intro hCommon
  exact hNoGlobal
    ((commonLocus_nonempty_iff_hasFiniteFootprintAmalgamation W R D).1
      hCommon)

/-!
## Factorization frontier after v3.13

The first-stage gluing problem now has three logically distinct levels:

```text
statewise:
  ∀ s, ∃ Qs correcting s

pairwise overlap:
  for each pair (s,t), local correcting gauges can be chosen
  with one common extension over the two finite footprints

global amalgamation:
  ∃ one Q whose restriction matches a correcting local witness
  on every route footprint
```

Global amalgamation implies pairwise overlap compatibility.  The converse is
not assumed.

The explicit overlap lemmas prove that pairwise compatibility forces equality
on actually shared `gId` and `gComp` coordinates.  The next theorem unit
should therefore test whether the generated localization equations propagate
these pairwise equalities strongly enough to force one global gauge, or whether
`PairwiseCompatibleButNoGlobalAmalgamation` can genuinely occur.

That is now the precise higher-order gluing question.  No topological or
convexity principle has been inserted.
-/

end KUOS.DependentOriginationQuotientGaugeFootprintOverlapV3_13
