import KUOS.DependentOriginationCanonicalTypeAHigherMaxPrismRigidityV1_116

namespace KUOS.DependentOriginationCanonicalTypeAHigherTopSimplexCoverageObstructionV1_117

open CategoryTheory
open CategoryTheory.Category
open Opposite
open Simplicial
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationScaledTerminalRLPV1_41
open KUOS.DependentOriginationStandardTypeAScaledHornFamilyV1_49
open KUOS.DependentOriginationStandardTypeAEndpointPushoutProductV1_50
open KUOS.DependentOriginationCanonicalTypeAHigherLowerCylinderRetractObstructionV1_112
open KUOS.DependentOriginationCanonicalTypeAHigherMaxPrismRigidityV1_116

universe u

noncomputable section

/-!
# Higher type-(A) top-simplex coverage obstruction v1.117

Version v1.112 proved that no higher type-(A) simplex is a scaled retract of
one one-dimension-lower canonical cylinder.  Version v1.116 separately proved
that the pointwise-max contraction used for object-level fibrancy cannot be
scaled into the sparse standard type-(A) target.

The present file strengthens the one-cylinder obstruction in a direction which
no longer mentions a section or a retract.

Fix `m >= 2`, so the target simplex has dimension `m+1 >= 3`, and let

```text
r : Delta[m] x Delta[1] -> Delta[m+1]
```

be any scaled map from a canonical cylinder over an arbitrary scaling on
`Delta[m]` to a standard type-(A) target.  We prove that the top identity
`(m+1)`-simplex is not in the image of `r`.

Assume a top simplex `z` of the cylinder mapped to the target top simplex.  The
first coordinate of `z` is a monotone map

```text
Fin (m+2) -> Fin (m+1),
```

so finite cardinality forces it to identify one adjacent pair.  Version v1.112
provides, through every adjacent edge, a non-thin standard type-(A) triangle.
Restrict `z` to that triangle.  Its first coordinate is degenerate along the
identified edge, hence the resulting cylinder triangle is thin for every base
scaling.  Simplicial naturality and the top-image assumption say that `r` sends
this thin source triangle exactly to the chosen non-thin target triangle, a
contradiction.

Thus in higher type-(A) dimensions a single lower canonical cylinder cannot
even cover the top target cell.  This is stronger than failure of one chosen
retraction formula: any positive presentation-level reverse construction must
assemble genuinely several relative cells or use a different global mechanism.
-/

/-! ## The top target simplex -/

/-- The Yoneda identity top simplex of `Delta[m+1]`. -/
def typeAHigherTargetTopSimplex (m : Nat) :
    (Delta[m + 1] : SSet.{u}).obj (op ⦋m + 1⦌) :=
  SSet.stdSimplex.objEquiv.symm (𝟙 ⦋m + 1⦌)

/-- Restricting the top identity simplex along any simplex recovers that
simplex. -/
@[simp]
theorem typeAHigherTargetTopSimplex_face
    (m : Nat)
    (t : (Delta[m + 1] : SSet.{u}).obj (op ⦋2⦌)) :
    (Delta[m + 1] : SSet.{u}).map
        (SSet.stdSimplex.objEquiv t).op
        (typeAHigherTargetTopSimplex m) = t := by
  apply SSet.stdSimplex.ext
  intro a
  rfl

/-! ## Every top cylinder simplex collapses an adjacent first-coordinate edge -/

/-- The first coordinate of a top simplex of `Delta[m] x Delta[1]`, viewed as
an order-preserving map on vertices. -/
def typeAHigherLowerCylinderTopFirstCoordinate
    (m : Nat)
    (z : ((Delta[m] : SSet.{u}) ⊗ Delta[1]).obj (op ⦋m + 1⦌)) :
    Fin (m + 2) →o Fin (m + 1) :=
  SSet.stdSimplex.asOrderHom z.1

/-- The first coordinate of a top cylinder simplex cannot be injective. -/
theorem typeAHigherLowerCylinderTopFirstCoordinate_not_injective
    (m : Nat)
    (z : ((Delta[m] : SSet.{u}) ⊗ Delta[1]).obj (op ⦋m + 1⦌)) :
    ¬ Function.Injective
      (typeAHigherLowerCylinderTopFirstCoordinate m z) := by
  intro hinj
  have hcard := Fintype.card_le_of_injective _ hinj
  simp only [Fintype.card_fin] at hcard
  omega

/-- Monotonicity plus the preceding cardinality obstruction forces one
adjacent pair to be identified. -/
theorem typeAHigherLowerCylinderTopFirstCoordinate_exists_adjacent_eq
    (m : Nat)
    (z : ((Delta[m] : SSet.{u}) ⊗ Delta[1]).obj (op ⦋m + 1⦌)) :
    ∃ k : Fin (m + 1),
      typeAHigherLowerCylinderTopFirstCoordinate m z k.castSucc =
        typeAHigherLowerCylinderTopFirstCoordinate m z k.succ := by
  have hnot :=
    typeAHigherLowerCylinderTopFirstCoordinate_not_injective m z
  rw [Fin.orderHom_injective_iff] at hnot
  push_neg at hnot
  exact hnot

/-! ## Restrict a top cylinder simplex to an arbitrary target triangle -/

/-- Pull a top cylinder simplex back along the simplex operator represented by
a target triangle. -/
def typeAHigherLowerCylinderTopFace
    (m : Nat)
    (z : ((Delta[m] : SSet.{u}) ⊗ Delta[1]).obj (op ⦋m + 1⦌))
    (t : (Delta[m + 1] : SSet.{u}).obj (op ⦋2⦌)) :
    ((Delta[m] : SSet.{u}) ⊗ Delta[1]).obj (op ⦋2⦌) :=
  ((Delta[m] : SSet.{u}) ⊗ Delta[1]).map
    (SSet.stdSimplex.objEquiv t).op z

/-- Pointwise description of the first coordinate of the pulled-back
triangle. -/
@[simp]
theorem typeAHigherLowerCylinderTopFace_fst_apply
    (m : Nat)
    (z : ((Delta[m] : SSet.{u}) ⊗ Delta[1]).obj (op ⦋m + 1⦌))
    (t : (Delta[m + 1] : SSet.{u}).obj (op ⦋2⦌))
    (a : Fin 3) :
    (typeAHigherLowerCylinderTopFace m z t).1 a = z.1 (t a) :=
  rfl

/-- If the first coordinate of the top source simplex collapses the adjacent
edge carried by a v1.112 witness triangle, then the corresponding pulled-back
cylinder triangle is thin for every possible base scaling. -/
theorem typeAHigherLowerCylinderTopFace_thin_of_adjacent_collapse
    (m : Nat)
    (i : Fin (m + 2))
    (sΔ : ScaledSimplicialSet (Delta[m] : SSet.{u}))
    (z : ((Delta[m] : SSet.{u}) ⊗ Delta[1]).obj (op ⦋m + 1⦌))
    (k : Fin (m + 1))
    (hk :
      typeAHigherLowerCylinderTopFirstCoordinate m z k.castSucc =
        typeAHigherLowerCylinderTopFirstCoordinate m z k.succ)
    (W : TypeAAdjacentNonthinWitness.{u} m i k) :
    (simplexCylinderScaling sΔ).thin
      (typeAHigherLowerCylinderTopFace m z W.triangle) := by
  change sΔ.thin (typeAHigherLowerCylinderTopFace m z W.triangle).1
  rcases W.containsAdjacent with hfirst | hsecond
  · apply arbitraryScaling_thin_of_zero_eq_one sΔ
    rw [typeAHigherLowerCylinderTopFace_fst_apply,
      typeAHigherLowerCylinderTopFace_fst_apply,
      hfirst.1, hfirst.2]
    simpa [typeAHigherLowerCylinderTopFirstCoordinate] using hk
  · apply arbitraryScaling_thin_of_one_eq_two sΔ
    rw [typeAHigherLowerCylinderTopFace_fst_apply,
      typeAHigherLowerCylinderTopFace_fst_apply,
      hsecond.1, hsecond.2]
    simpa [typeAHigherLowerCylinderTopFirstCoordinate] using hk

/-! ## Naturality transfers top coverage to every triangle face -/

/-- If a top cylinder simplex maps to the target top simplex, then every face
obtained by pulling back along a target triangle maps exactly to that target
triangle. -/
theorem typeAHigherLowerCylinderTopFace_image
    (m : Nat)
    (i : Fin (m + 2))
    {sΔ : ScaledSimplicialSet (Delta[m] : SSet.{u})}
    (r : scaledSimplexCylinder sΔ ⟶
      scaledSimplex (standardTypeASimplexScaling i))
    (z : ((Delta[m] : SSet.{u}) ⊗ Delta[1]).obj (op ⦋m + 1⦌))
    (t : (Delta[m + 1] : SSet.{u}).obj (op ⦋2⦌))
    (hz :
      r.map.app (op ⦋m + 1⦌) z =
        typeAHigherTargetTopSimplex m) :
    r.map.app (op ⦋2⦌)
        (typeAHigherLowerCylinderTopFace m z t) = t := by
  let alpha : ⦋2⦌ ⟶ ⦋m + 1⦌ := SSet.stdSimplex.objEquiv t
  have hnat :
      r.map.app (op ⦋2⦌)
          (((Delta[m] : SSet.{u}) ⊗ Delta[1]).map alpha.op z) =
        (Delta[m + 1] : SSet.{u}).map alpha.op
          (r.map.app (op ⦋m + 1⦌) z) := by
    exact ConcreteCategory.congr_hom (r.map.naturality alpha.op) z
  calc
    r.map.app (op ⦋2⦌)
        (typeAHigherLowerCylinderTopFace m z t) =
      (Delta[m + 1] : SSet.{u}).map alpha.op
        (r.map.app (op ⦋m + 1⦌) z) := by
          simpa [typeAHigherLowerCylinderTopFace, alpha] using hnat
    _ = (Delta[m + 1] : SSet.{u}).map alpha.op
        (typeAHigherTargetTopSimplex m) := by rw [hz]
    _ = t := by
      simpa [alpha] using typeAHigherTargetTopSimplex_face (u := u) m t

/-! ## Main coverage obstruction -/

/-- A scaled map from one lower canonical cylinder to a higher standard
Type-A simplex cannot hit the target top simplex. -/
theorem typeAHigherLowerCylinderMap_not_hits_topSimplex
    (m : Nat)
    (hm : 2 ≤ m)
    (i : Fin (m + 2))
    (hi0 : 0 < i)
    (hilast : i < Fin.last (m + 1))
    (sΔ : ScaledSimplicialSet (Delta[m] : SSet.{u}))
    (r : scaledSimplexCylinder sΔ ⟶
      scaledSimplex (standardTypeASimplexScaling i))
    (z : ((Delta[m] : SSet.{u}) ⊗ Delta[1]).obj (op ⦋m + 1⦌)) :
    r.map.app (op ⦋m + 1⦌) z ≠
      typeAHigherTargetTopSimplex m := by
  intro hz
  obtain ⟨k, hk⟩ :=
    typeAHigherLowerCylinderTopFirstCoordinate_exists_adjacent_eq m z
  obtain ⟨W⟩ :=
    typeAAdjacentNonthinWitness_exists m hm i hi0 hilast k
  have hthin :
      (simplexCylinderScaling sΔ).thin
        (typeAHigherLowerCylinderTopFace m z W.triangle) :=
    typeAHigherLowerCylinderTopFace_thin_of_adjacent_collapse
      m i sΔ z k hk W
  have himage :=
    r.scaled (typeAHigherLowerCylinderTopFace m z W.triangle) hthin
  have hface :
      r.map.app (op ⦋2⦌)
          (typeAHigherLowerCylinderTopFace m z W.triangle) =
        W.triangle :=
    typeAHigherLowerCylinderTopFace_image m i r z W.triangle hz
  rw [hface] at himage
  exact W.nonthin himage

/-- Equivalently, the top-degree component of every such scaled lower-cylinder
map is not surjective. -/
theorem typeAHigherLowerCylinderMap_top_not_surjective
    (m : Nat)
    (hm : 2 ≤ m)
    (i : Fin (m + 2))
    (hi0 : 0 < i)
    (hilast : i < Fin.last (m + 1))
    (sΔ : ScaledSimplicialSet (Delta[m] : SSet.{u}))
    (r : scaledSimplexCylinder sΔ ⟶
      scaledSimplex (standardTypeASimplexScaling i)) :
    ¬ Function.Surjective (r.map.app (op ⦋m + 1⦌)) := by
  intro hsurj
  obtain ⟨z, hz⟩ := hsurj (typeAHigherTargetTopSimplex m)
  exact
    typeAHigherLowerCylinderMap_not_hits_topSimplex
      m hm i hi0 hilast sΔ r z hz

/-- The first higher target dimension, three, is already covered by the same
section-free obstruction. -/
theorem typeAThreeLowerCylinderMap_top_not_surjective
    (i : Fin 4)
    (hi0 : 0 < i)
    (hilast : i < Fin.last 3)
    (sΔ : ScaledSimplicialSet (Delta[2] : SSet.{u}))
    (r : scaledSimplexCylinder sΔ ⟶
      scaledSimplex (standardTypeASimplexScaling i)) :
    ¬ Function.Surjective (r.map.app (op ⦋3⦌)) := by
  exact
    typeAHigherLowerCylinderMap_top_not_surjective
      2 (by decide) i hi0 hilast sΔ r

/-!
The one-lower-cylinder branch is now closed at the level of target coverage:

```text
higher Type A, target dimension >= 3

any scaled map
  Delta[m] x Delta[1] -> Delta[m+1]

cannot hit the top target simplex.
```

Hence a section is impossible for a stronger reason than failure of a chosen
retract formula: the single cylinder does not supply the top cell at all.
The remaining presentation-level work must therefore use a genuine relative
multi-cell construction, or prove that the reverse generated-class inclusion
itself fails by exhibiting an appropriate right-class witness.
-/

end KUOS.DependentOriginationCanonicalTypeAHigherTopSimplexCoverageObstructionV1_117
