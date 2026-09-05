import KUOS.DependentOriginationCanonicalFibrationThinReflectionV1_92
import Mathlib.AlgebraicTopology.SimplicialSet.Dimension

namespace KUOS.DependentOriginationStandardTypeATwoSimplexThinReplacementV1_93

open CategoryTheory
open CategoryTheory.Category
open Opposite
open Simplicial
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationGlobalDuskinScaledHornCoherenceV1_22
open KUOS.DependentOriginationScaledTerminalRLPV1_41
open KUOS.DependentOriginationStandardTypeAScaledHornFamilyV1_49
open KUOS.DependentOriginationStandardTypeAEndpointPushoutProductV1_50
open KUOS.DependentOriginationStandardTypeCCollapsedEdgeV1_58
open KUOS.DependentOriginationCanonicalFibrancyAtomicTwoSimplexAuditV1_91
open KUOS.DependentOriginationCanonicalFibrationThinReflectionV1_92

universe u

/-!
# Standard type-(A) degree-two lifting is thin replacement v1.93

Versions v1.91-v1.92 showed that the arbitrary-scaling canonical presentation
contains the atomic enrichment

```text
(Delta[2], minimal) -> (Delta[2], minimal + {id_2})
```

and therefore every canonical right map *reflects* thin 2-simplices.

The standard type-(A) inner horn in dimension two has a different semantics.
If a 2-simplex `sigma` has thin image under a standard-right map `p`, the
standard horn RLP does not force `sigma` itself to be thin.  It only forces the
existence of a thin replacement `tau` with

* the same inner horn as `sigma`; and
* the same image under `p`.

This file proves that statement directly from the literal `n = 2, i = 1`
standard type-(A) generator.  It then isolates the exact extra uniqueness
condition under which thin replacement collapses to thin reflection.
Consequently any standard-right map which fails thin reflection must contain a
genuine pair of distinct parallel 2-simplices: one non-thin and one thin, with
the same inner horn and the same image.

This identifies the geometry required of a future explicit
standard-versus-canonical separation witness without asserting such a witness
before its standard A/B/C lifting property has been proved.
-/

/-! ## The unique degree-two standard type-(A) inner horn -/

/-- The standard type-(A) generator index `n = 2, i = 1`. -/
def standardTypeATwoSimplexIndex : StandardTypeAHornGeneratorIndex where
  n := 2
  i := 1
  inner_left := by decide
  inner_right := by decide

/-- Every 2-simplex of `Lambda[2,1]` is minimally thin.  Mathlib knows that a
horn `Lambda[n,i]` has dimension `< n`; in degree two this says that every
2-simplex of `Lambda[2,1]` is degenerate, hence is one of the two simplicial
degeneracies used by `minimalScaling`. -/
theorem standardTypeATwoHorn_every_two_simplex_minimally_thin
    (t : (Λ[2, (1 : Fin 3)] : SSet.{u}).obj (op ⦋2⦌)) :
    (minimalScaling (Λ[2, (1 : Fin 3)] : SSet.{u})).thin t := by
  have hdeg :
      t ∈ (Λ[2, (1 : Fin 3)] : SSet.{u}).degenerate 2 := by
    rw [SSet.degenerate_eq_univ_of_hasDimensionLT
      (Λ[2, (1 : Fin 3)] : SSet.{u}) 2 2]
    simp
  rw [SSet.degenerate_eq_iUnion_range_σ] at hdeg
  simp only [Set.mem_iUnion, Set.mem_range] at hdeg
  rcases hdeg with ⟨i, x, rfl⟩
  fin_cases i
  · exact Or.inl ⟨x, rfl⟩
  · exact Or.inr ⟨x, rfl⟩

/-- Consequently every simplicial map out of the degree-two standard inner
horn is scaled for the standard type-(A) horn scaling, independently of the
target scaling. -/
theorem standardTypeATwoHornMap_scaled
    {X : ScaledSSet.{u}}
    (f : (Λ[2, (1 : Fin 3)] : SSet.{u}) ⟶ X.carrier) :
    IsScaledMap
      (standardTypeAHornScaling (1 : Fin 3)) X.scaling f := by
  intro t _
  exact (minimalScaling_map X.scaling f) t
    (standardTypeATwoHorn_every_two_simplex_minimally_thin t)

/-- The Yoneda identity triangle is the distinguished type-(A) triangle for
`n = 2, i = 1`. -/
theorem identityTwoSimplex_isStandardTypeADistinguishedTriangle :
    IsStandardTypeADistinguishedTriangle
      (1 : Fin 3) (identityTwoSimplex : (Δ[2] : SSet.{u}).obj (op ⦋2⦌)) := by
  simp [IsStandardTypeADistinguishedTriangle, identityTwoSimplex]

/-- Hence the identity triangle is thin in the standard type-(A) simplex
scaling in dimension two. -/
theorem identityTwoSimplex_standardTypeA_thin :
    (standardTypeASimplexScaling (1 : Fin 3)).thin
      (identityTwoSimplex : (Δ[2] : SSet.{u}).obj (op ⦋2⦌)) := by
  exact Or.inr identityTwoSimplex_isStandardTypeADistinguishedTriangle

/-- In `Delta[2]` the distinguished type-(A) triangle is unique: it is the
Yoneda identity triangle. -/
theorem standardTypeATwo_distinguished_eq_identity
    (t : (Δ[2] : SSet.{u}).obj (op ⦋2⦌))
    (ht : IsStandardTypeADistinguishedTriangle (1 : Fin 3) t) :
    t = identityTwoSimplex := by
  rcases ht with ⟨h1, h0, h2⟩
  ext j
  fin_cases j <;> apply Fin.ext <;>
    simp [identityTwoSimplex] <;> omega

/-- A map out of the standard type-(A) `Delta[2]` is scaled as soon as the
image of the identity triangle is thin.  The minimally thin triangles are
automatic and the only additional type-(A) triangle is `id_2`. -/
theorem standardTypeATwoSimplexMap_scaled_of_identity_thin
    {Y : ScaledSSet.{u}}
    (f : (Δ[2] : SSet.{u}) ⟶ Y.carrier)
    (hthin :
      Y.scaling.thin
        (f.app (op ⦋2⦌)
          (identityTwoSimplex : (Δ[2] : SSet.{u}).obj (op ⦋2⦌)))) :
    IsScaledMap
      (standardTypeASimplexScaling (1 : Fin 3)) Y.scaling f := by
  intro t ht
  rcases ht with hmin | hdist
  · exact (minimalScaling_map Y.scaling f) t hmin
  · rw [standardTypeATwo_distinguished_eq_identity t hdist]
    exact hthin

/-! ## Inner-horn and image relations on two-simplices -/

/-- Two 2-simplices have the same standard inner horn when their Yoneda maps
agree after restriction along `Lambda[2,1] -> Delta[2]`. -/
def SameStandardTypeAInnerHorn
    {X : ScaledSSet.{u}}
    (σ τ : X.carrier.obj (op ⦋2⦌)) : Prop :=
  (Λ[2, (1 : Fin 3)].ι :
      (Λ[2, (1 : Fin 3)] : SSet.{u}) ⟶ (Δ[2] : SSet.{u})) ≫
      SSet.yonedaEquiv.symm σ =
    (Λ[2, (1 : Fin 3)].ι :
      (Λ[2, (1 : Fin 3)] : SSet.{u}) ⟶ (Δ[2] : SSet.{u})) ≫
      SSet.yonedaEquiv.symm τ

/-- Two source 2-simplices have the same image under a scaled morphism. -/
def SameTwoSimplexImage
    {X Y : ScaledSSet.{u}}
    (p : X ⟶ Y)
    (σ τ : X.carrier.obj (op ⦋2⦌)) : Prop :=
  p.map.app (op ⦋2⦌) σ = p.map.app (op ⦋2⦌) τ

/-- Degree-two thin-replacement property: whenever `p sigma` is thin there is
a thin `tau` with the same standard inner horn and the same `p`-image. -/
def HasStandardTypeAThinReplacement
    {X Y : ScaledSSet.{u}}
    (p : X ⟶ Y) : Prop :=
  ∀ σ : X.carrier.obj (op ⦋2⦌),
    Y.scaling.thin (p.map.app (op ⦋2⦌) σ) →
      ∃ τ : X.carrier.obj (op ⦋2⦌),
        X.scaling.thin τ ∧
        SameStandardTypeAInnerHorn σ τ ∧
        SameTwoSimplexImage p τ σ

/-- Relative two-simplex separation: a 2-simplex is determined by its standard
inner horn together with its image under `p`. -/
def IsStandardTypeATwoSimplexSeparated
    {X Y : ScaledSSet.{u}}
    (p : X ⟶ Y) : Prop :=
  ∀ σ τ : X.carrier.obj (op ⦋2⦌),
    SameStandardTypeAInnerHorn σ τ →
    SameTwoSimplexImage p σ τ →
    σ = τ

/-! ## Standard type-(A) RLP produces thin replacements -/

/-- RLP against the literal `n = 2, i = 1` type-(A) generator produces the
thin replacement of every source 2-simplex whose image is thin. -/
theorem thinReplacement_of_standardTypeATwoRLP
    {X Y : ScaledSSet.{u}}
    {p : X ⟶ Y}
    (hp : HasLiftingProperty
      (standardTypeAScaledHornGeneratorHom standardTypeATwoSimplexIndex) p) :
    HasStandardTypeAThinReplacement p := by
  intro σ hσ
  let f : standardTypeAScaledHorn standardTypeATwoSimplexIndex ⟶ X :=
    { map :=
        (Λ[2, (1 : Fin 3)].ι :
          (Λ[2, (1 : Fin 3)] : SSet.{u}) ⟶ (Δ[2] : SSet.{u})) ≫
          SSet.yonedaEquiv.symm σ
      scaled := by
        exact standardTypeATwoHornMap_scaled _ }
  let g : standardTypeAScaledSimplex standardTypeATwoSimplexIndex ⟶ Y :=
    { map := SSet.yonedaEquiv.symm σ ≫ p.map
      scaled := by
        apply standardTypeATwoSimplexMap_scaled_of_identity_thin
        simpa [identityTwoSimplex] using hσ }
  let sq : CommSq f
      (standardTypeAScaledHornGeneratorHom standardTypeATwoSimplexIndex)
      p g :=
    { w := by
        apply ScaledSSet.ScaledMap.ext
        simp [f, g, standardTypeATwoSimplexIndex,
          standardTypeAScaledHornGeneratorHom, Category.assoc] }
  rcases (hp.sq_hasLift sq).exists_lift with ⟨L⟩
  let τ : X.carrier.obj (op ⦋2⦌) :=
    L.l.map.app (op ⦋2⦌)
      (identityTwoSimplex : (Δ[2] : SSet.{u}).obj (op ⦋2⦌))
  refine ⟨τ, ?_, ?_, ?_⟩
  · exact L.l.scaled _ identityTwoSimplex_standardTypeA_thin
  · have hleft := congrArg ScaledSSet.ScaledMap.map L.fac_left
    have hYoneda : SSet.yonedaEquiv.symm τ = L.l.map := by
      simp [τ, identityTwoSimplex]
    dsimp [SameStandardTypeAInnerHorn]
    rw [hYoneda]
    simpa [f, standardTypeATwoSimplexIndex,
      standardTypeAScaledHornGeneratorHom] using hleft.symm
  · have hright := congrArg ScaledSSet.ScaledMap.map L.fac_right
    have hpoint := ConcreteCategory.congr_hom
      (congr_app hright (op ⦋2⦌))
      (identityTwoSimplex : (Δ[2] : SSet.{u}).obj (op ⦋2⦌))
    simpa [SameTwoSimplexImage, τ, g, identityTwoSimplex] using hpoint

/-- Every map in the complete standard A/B/C right class therefore has the
degree-two thin-replacement property. -/
theorem standardRight_hasStandardTypeAThinReplacement
    {X Y : ScaledSSet.{u}}
    {p : X ⟶ Y}
    (hstd :
      (standardGeneratedScaledAnodyneABC :
        MorphismProperty (ScaledSSet.{u})).rlp p) :
    HasStandardTypeAThinReplacement p := by
  apply thinReplacement_of_standardTypeATwoRLP
  exact hstd
    (standardTypeAScaledHornGeneratorHom standardTypeATwoSimplexIndex)
    (standardTypeAGenerator_mem_standardGenerated standardTypeATwoSimplexIndex)

/-! ## When replacement collapses to reflection -/

/-- Thin replacement becomes thin reflection exactly under the additional
relative separation condition: the replacement must then equal the original
2-simplex. -/
theorem reflectsThinTwoSimplices_of_thinReplacement_of_separated
    {X Y : ScaledSSet.{u}}
    {p : X ⟶ Y}
    (hrep : HasStandardTypeAThinReplacement p)
    (hsep : IsStandardTypeATwoSimplexSeparated p) :
    ReflectsThinTwoSimplices p := by
  intro σ hσ
  rcases hrep σ hσ with ⟨τ, hτ, hhorn, himage⟩
  have hEq : σ = τ := hsep σ τ hhorn himage.symm
  simpa [hEq] using hτ

/-- Hence a standard A/B/C-right map which is relatively separated in degree
two already has the canonical atomic RLP. -/
theorem atomicTwoSimplexRLP_of_standardRight_of_separated
    {X Y : ScaledSSet.{u}}
    {p : X ⟶ Y}
    (hstd :
      (standardGeneratedScaledAnodyneABC :
        MorphismProperty (ScaledSSet.{u})).rlp p)
    (hsep : IsStandardTypeATwoSimplexSeparated p) :
    HasLiftingProperty atomicTwoSimplexEnrichment p := by
  apply (atomicTwoSimplexRLP_iff_reflectsThinTwoSimplices p).2
  exact reflectsThinTwoSimplices_of_thinReplacement_of_separated
    (standardRight_hasStandardTypeAThinReplacement hstd) hsep

/-- Conversely, if a standard-right map sends a non-thin source triangle to a
thin target triangle, its type-(A) RLP supplies a *distinct* thin replacement
with the same inner horn and the same image.  This is the exact geometry that
a future standard-versus-canonical separation witness must exhibit. -/
theorem standardRight_nonreflecting_has_distinct_thinReplacement
    {X Y : ScaledSSet.{u}}
    {p : X ⟶ Y}
    (hstd :
      (standardGeneratedScaledAnodyneABC :
        MorphismProperty (ScaledSSet.{u})).rlp p)
    (σ : X.carrier.obj (op ⦋2⦌))
    (himage : Y.scaling.thin (p.map.app (op ⦋2⦌) σ))
    (hsource : ¬ X.scaling.thin σ) :
    ∃ τ : X.carrier.obj (op ⦋2⦌),
      X.scaling.thin τ ∧
      SameStandardTypeAInnerHorn σ τ ∧
      SameTwoSimplexImage p τ σ ∧
      τ ≠ σ := by
  rcases standardRight_hasStandardTypeAThinReplacement hstd σ himage with
    ⟨τ, hτ, hhorn, hpimage⟩
  refine ⟨τ, hτ, hhorn, hpimage, ?_⟩
  intro hEq
  apply hsource
  simpa [hEq] using hτ

/-- In particular every standard-right nonreflecting witness necessarily fails
relative two-simplex separation. -/
theorem not_separated_of_standardRight_nonreflecting
    {X Y : ScaledSSet.{u}}
    {p : X ⟶ Y}
    (hstd :
      (standardGeneratedScaledAnodyneABC :
        MorphismProperty (ScaledSSet.{u})).rlp p)
    (σ : X.carrier.obj (op ⦋2⦌))
    (himage : Y.scaling.thin (p.map.app (op ⦋2⦌) σ))
    (hsource : ¬ X.scaling.thin σ) :
    ¬ IsStandardTypeATwoSimplexSeparated p := by
  intro hsep
  have hreflect := reflectsThinTwoSimplices_of_thinReplacement_of_separated
    (standardRight_hasStandardTypeAThinReplacement hstd) hsep
  exact hsource (hreflect σ himage)

/-!
The degree-two comparison is now structurally exact at the level needed for a
separation witness:

```text
canonical atomic RLP:
  p sigma thin  ->  sigma thin

standard type-(A) n=2 RLP:
  p sigma thin
    -> exists thin tau,
         innerHorn(tau) = innerHorn(sigma)
         and p(tau) = p(sigma)

standard-right + relative separation
  -> tau = sigma
  -> canonical atomic RLP

standard-right + failure of canonical reflection
  -> distinct nonthin sigma / thin tau
     with the same inner horn and the same p-image.
```

Thus standard-versus-canonical separation is not merely a question of finding
a non-thin triangle.  The standard right class can tolerate it precisely when
a separate thin representative solves the same inner-horn lifting problem over
the same target simplex.  This is the finite degree-two geometry that a
concrete future witness must realize.
-/

end KUOS.DependentOriginationStandardTypeATwoSimplexThinReplacementV1_93
