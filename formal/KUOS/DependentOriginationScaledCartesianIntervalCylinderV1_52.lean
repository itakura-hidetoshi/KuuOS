import KUOS.DependentOriginationStandardTypeANativeLeibnizLiftingMateV1_51
import Mathlib.AlgebraicTopology.SimplicialSet.Dimension
import Mathlib.AlgebraicTopology.SimplicialSet.StdSimplex

namespace KUOS.DependentOriginationScaledCartesianIntervalCylinderV1_52

open CategoryTheory
open MonoidalCategory
open Opposite
open Simplicial
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationScaledHornAttachmentLiftingV1_40
open KUOS.DependentOriginationScaledTerminalRLPV1_41
open KUOS.DependentOriginationScaledAnodyneAttachmentFactorizationV1_48
open KUOS.DependentOriginationStandardTypeAScaledHornFamilyV1_49
open KUOS.DependentOriginationStandardTypeAEndpointPushoutProductV1_50
open KUOS.DependentOriginationStandardTypeANativeLeibnizLiftingMateV1_51

universe u

/-!
# Scaled cartesian interval cylinder v1.52

Version 1.51 identified the underlying standard type-(A) endpoint attachment
with Mathlib's native Leibniz pushout and exposed its pullback-hom lifting mate.
To transport that result through the scaled category we first identify the
scaling on the cylinder itself.

The KuuOS notion of a scaling asks that both degeneracies of every 1-simplex
are thin.  Since `Delta[1]` has dimension at most one, every 2-simplex of
`Delta[1]` is degenerate, hence every scaling on `Delta[1]` is automatically
maximal.  Consequently, for any scaled simplicial set `(X,T)`, the ordinary
cartesian-product scaling on `X x Delta[1]` reduces to thinness in the `X`
coordinate alone.  This is exactly the existing `simplexCylinderScaling`.

Thus the cylinder target used by the type-(A) endpoint pushout-product is not
an ad hoc scaling: it is canonically the scaled cartesian product with the
interval.  The induced source scaling can therefore also be rewritten as the
pullback of that cartesian-product scaling.
-/

/-! ## Extensionality and cartesian-product scaling -/

/-- Two scalings are equal when they select exactly the same thin 2-simplices. -/
theorem scaling_eq_of_thin_iff
    {X : SSet.{u}}
    {s₁ s₂ : ScaledSimplicialSet X}
    (h : ∀ t, s₁.thin t ↔ s₂.thin t) :
    s₁ = s₂ := by
  cases s₁ with
  | mk thin₁ hzero₁ hone₁ =>
      cases s₂ with
      | mk thin₂ hzero₂ hone₂ =>
          dsimp at h
          have hthin : thin₁ = thin₂ := by
            funext t
            exact propext (h t)
          subst thin₂
          rfl

/-- Cartesian-product scaling: a 2-simplex of `X x Y` is thin exactly when
both coordinate 2-simplices are thin. -/
def cartesianProductScaling
    {X Y : SSet.{u}}
    (sX : ScaledSimplicialSet X)
    (sY : ScaledSimplicialSet Y) :
    ScaledSimplicialSet (X ⊗ Y) where
  thin := fun t => sX.thin t.1 ∧ sY.thin t.2
  thin_sigma_zero := by
    intro x
    constructor
    · simpa using sX.thin_sigma_zero x.1
    · simpa using sY.thin_sigma_zero x.2
  thin_sigma_one := by
    intro x
    constructor
    · simpa using sX.thin_sigma_one x.1
    · simpa using sY.thin_sigma_one x.2

/-- The corresponding object-level cartesian product in the explicit KuuOS
scaled category.  No monoidal-category instance is asserted yet; this object is
the concrete carrier needed for the interval comparison. -/
def scaledCartesianProduct
    (X Y : ScaledSSet.{u}) : ScaledSSet.{u} :=
  ScaledSSet.of (X.carrier ⊗ Y.carrier)
    (cartesianProductScaling X.scaling Y.scaling)

/-! ## Every interval scaling is maximal -/

/-- Every 2-simplex of `Delta[1]` is thin for every admissible KuuOS scaling.
The proof uses the native dimension theorem for the standard 1-simplex and the
native description of degenerate `(n+1)`-simplices as degeneracies. -/
theorem intervalScaling_allThin
    (sI : ScaledSimplicialSet (Δ[1] : SSet.{u}))
    (t : (Δ[1] : SSet.{u}).obj (op ⦋2⦌)) :
    sI.thin t := by
  have ht : t ∈ (Δ[1] : SSet.{u}).degenerate 2 := by
    rw [(Δ[1] : SSet.{u}).degenerate_eq_univ_of_hasDimensionLT 2 2]
    simp
  rw [SSet.degenerate_eq_iUnion_range_σ] at ht
  simp only [Set.mem_iUnion, Set.mem_range] at ht
  obtain ⟨i, x, rfl⟩ := ht
  fin_cases i
  · exact sI.thin_sigma_zero x
  · exact sI.thin_sigma_one x

/-- Hence the scaling on the simplicial interval is unique: every scaling is
literally the maximal scaling. -/
theorem intervalScaling_eq_maximal
    (sI : ScaledSimplicialSet (Δ[1] : SSet.{u})) :
    sI = ScaledSimplicialSet.maximal (Δ[1] : SSet.{u}) := by
  apply scaling_eq_of_thin_iff
  intro t
  constructor
  · intro _
    trivial
  · intro _
    exact intervalScaling_allThin sI t

/-- The interval as an explicit scaled object, for any chosen scaling. -/
def scaledInterval
    (sI : ScaledSimplicialSet (Δ[1] : SSet.{u})) : ScaledSSet.{u} :=
  ScaledSSet.of (Δ[1] : SSet.{u}) sI

/-! ## The existing cylinder is the scaled cartesian product -/

/-- Cartesian product with the interval has exactly the pre-existing KuuOS
cylinder scaling, independently of which interval scaling was chosen. -/
theorem cartesianProductScaling_interval_eq_simplexCylinderScaling
    {n : Nat}
    (sΔ : ScaledSimplicialSet (Δ[n] : SSet.{u}))
    (sI : ScaledSimplicialSet (Δ[1] : SSet.{u})) :
    cartesianProductScaling sΔ sI = simplexCylinderScaling sΔ := by
  apply scaling_eq_of_thin_iff
  intro t
  change (sΔ.thin t.1 ∧ sI.thin t.2) ↔ sΔ.thin t.1
  constructor
  · intro h
    exact h.1
  · intro h
    exact ⟨h, intervalScaling_allThin sI t.2⟩

/-- Object-level form: the scaled simplex cylinder is exactly the concrete
scaled cartesian product of the scaled simplex with the scaled interval. -/
theorem scaledSimplex_product_interval_eq_cylinder
    {n : Nat}
    (sΔ : ScaledSimplicialSet (Δ[n] : SSet.{u}))
    (sI : ScaledSimplicialSet (Δ[1] : SSet.{u})) :
    scaledCartesianProduct (scaledSimplex sΔ) (scaledInterval sI) =
      scaledSimplexCylinder sΔ := by
  dsimp only [scaledCartesianProduct, scaledInterval, scaledSimplex,
    scaledSimplexCylinder, ScaledSSet.of]
  rw [cartesianProductScaling_interval_eq_simplexCylinderScaling sΔ sI]

/-- Specialization to the standard type-(A) simplex scaling. -/
theorem standardTypeAScaledSimplex_product_interval_eq_cylinder
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (sI : ScaledSimplicialSet (Δ[1] : SSet.{u})) :
    scaledCartesianProduct
        (scaledSimplex (standardTypeASimplexScaling g.i))
        (scaledInterval sI) =
      scaledSimplexCylinder (standardTypeASimplexScaling g.i) :=
  scaledSimplex_product_interval_eq_cylinder
    (standardTypeASimplexScaling g.i) sI

/-- The induced scaling on the standard type-(A) endpoint attachment can now
be expressed as the pullback of a genuine cartesian-product scaling. -/
theorem standardTypeAEndpointPushoutProductSource_scaling_eq_pullback_product
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    (sI : ScaledSimplicialSet (Δ[1] : SSet.{u})) :
    (standardTypeAEndpointPushoutProductSource g).scaling =
      pullbackScaling
        (cartesianProductScaling (standardTypeASimplexScaling g.i) sI)
        ((SSet.horn g.n g.i).unionProd
          (intervalEndpoint g.endpoint)).ι := by
  dsimp only [standardTypeAEndpointPushoutProductSource, ScaledSSet.of]
  rw [cartesianProductScaling_interval_eq_simplexCylinderScaling
    (standardTypeASimplexScaling g.i) sI]

/-!
The type-(A) comparison spine now has a genuinely scaled cartesian target:

```text
native SSet Leibniz pushout (v1.51)
  + unique/maximal scaling on Delta[1]
  -> simplexCylinderScaling = cartesian product scaling
  -> induced attachment scaling = pullback of product scaling.
```

The remaining distinction is therefore localized entirely in the source:
the scaled categorical pushout carries the least scaling generated by its two
legs, while the v1.48/v1.50 induced source carries the full pullback scaling
from the product target.  The next step is to compare those two source
scalings explicitly; that comparison is the exact scaling-enrichment left over
between the native Leibniz geometry and the induced attachment.
-/

end KUOS.DependentOriginationScaledCartesianIntervalCylinderV1_52
