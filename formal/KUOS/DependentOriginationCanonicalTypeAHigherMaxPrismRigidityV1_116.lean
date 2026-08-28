import KUOS.DependentOriginationCanonicalStandardABCFibrantObjectStrictOrderV1_115
import KUOS.DependentOriginationCanonicalTypeAHigherLowerCylinderRetractObstructionV1_112

namespace KUOS.DependentOriginationCanonicalTypeAHigherMaxPrismRigidityV1_116

open CategoryTheory
open CategoryTheory.Category
open Opposite
open Simplicial
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationScaledTerminalRLPV1_41
open KUOS.DependentOriginationStandardTypeAScaledHornFamilyV1_49
open KUOS.DependentOriginationStandardTypeAEndpointPushoutProductV1_50
open KUOS.DependentOriginationCanonicalInnerHornContractibleFibrancyV1_114
open KUOS.DependentOriginationCanonicalTypeAHigherLowerCylinderRetractObstructionV1_112
open KUOS.DependentOriginationCanonicalStandardABCFibrantObjectStrictOrderV1_115

universe u

noncomputable section

/-!
# Higher type-(A) pointwise-max prism rigidity v1.116

Version v1.114 closed object-level type-(A) fibrancy by contracting every horn
in ordinary simplicial homotopy class.  Its explicit first prism is the
pointwise deformation

```text
(x,t) |-> if t = 0 then x else max(x,i).
```

That argument is intentionally object-level: attachment fibrancy first forces
the *target* scaling to be maximal, after which no scaling obstruction remains.
It is therefore important not to reuse the same homotopy silently in the
presentation-level reverse comparison, where the target still carries the
sparse standard type-(A) scaling.

The present file proves that such a reuse is impossible in every simplex
dimension at least three.  We extend the same formula from the horn to the
whole simplex and use one uniform thin source triangle

```text
first coordinate    [0,0,n]
interval coordinate [0,1,1].
```

The first coordinate is a sigma-zero degeneracy, so the source triangle is
thin in the canonical cylinder over *every possible scaling* on `Delta[n]`.
Its pointwise-max image is

```text
[0,i,n].
```

For an inner index `0 < i < n`, this image is nondegenerate.  If `n >= 3` it
cannot equal the unique distinguished type-(A) triangle
`[i-1,i,i+1]`: equality would force simultaneously `i = 1` and `n = 2`.
Hence the image is not thin.

Consequently the literal contraction used successfully in v1.114 cannot be a
scaled homotopy into the standard type-(A) target in any higher dimension,
independently of how one changes the cylinder base scaling.  Together with the
v1.112 no-one-lower-cylinder-retract theorem, this removes both obvious
one-prism routes.  The remaining presentation-level reverse problem genuinely
requires relative multi-cell geometry rather than an object-level contraction
repackaged as a left-class proof.
-/

/-! ## Ambient version of the v1.114 pointwise-max prism -/

/-- On the full standard simplex, use exactly the same pointwise formula as the
first horn contraction prism of v1.114: keep the simplex coordinate at interval
value zero and replace it by `max(-,i)` after the interval switches to one. -/
def typeAHigherIdToMaxPrismMap
    (g : StandardTypeAHornGeneratorIndex) :
    ((Δ[g.n] : SSet.{u}) ⊗ Δ[1]) ⟶ (Δ[g.n] : SSet.{u}) where
  app := fun ⟨⟨d⟩⟩ => ↾fun z =>
    SSet.stdSimplex.objMk
      { toFun := fun j =>
          if z.2 j = 0 then z.1 j else max (z.1 j) g.i
        monotone' := by
          intro a b hab
          have hx := SSet.stdSimplex.monotone_apply z.1 hab
          have ht := SSet.stdSimplex.monotone_apply z.2 hab
          by_cases ha : z.2 a = 0
          · by_cases hb : z.2 b = 0
            · simpa [ha, hb] using hx
            · simp only [ha, if_pos, hb, if_neg]
              exact hx.trans (le_max_left _ _)
          · have hb : z.2 b ≠ 0 := by
              intro hb
              have hz : z.2 a ≤ 0 := by simpa [hb] using ht
              have : z.2 a = 0 := le_antisymm hz (Fin.zero_le _)
              exact ha this
            simp only [ha, if_neg, hb]
            exact max_le_max hx le_rfl }
  naturality := by
    intro d e f
    ext z j
    rfl

/-! ## A uniform thin source witness -/

/-- The single source triangle used in every dimension and at every inner
index.  Its simplex coordinate is `[0,0,n]`, and its interval coordinate is
`[0,1,1]`. -/
def typeAHigherIdToMaxSourceTriangle
    (g : StandardTypeAHornGeneratorIndex) :
    ((Δ[g.n] : SSet.{u}) ⊗ Δ[1]) _⦋2⦌ :=
  ⟨SSet.stdSimplex.triangle
      (0 : Fin (g.n + 1))
      (0 : Fin (g.n + 1))
      (Fin.last g.n)
      (Fin.zero_le _)
      (Fin.zero_le _),
    SSet.stdSimplex.triangle
      (0 : Fin 2) (1 : Fin 2) (1 : Fin 2)
      (by decide) (by decide)⟩

/-- The first coordinate of the witness is a sigma-zero degeneracy, hence the
witness is cylinder-thin for every possible scaling on the simplex. -/
theorem typeAHigherIdToMaxSourceTriangle_thin
    (g : StandardTypeAHornGeneratorIndex)
    (sΔ : ScaledSimplicialSet (Δ[g.n] : SSet.{u})) :
    (simplexCylinderScaling sΔ).thin
      (typeAHigherIdToMaxSourceTriangle g) := by
  change sΔ.thin (typeAHigherIdToMaxSourceTriangle g).1
  let e : (Δ[g.n] : SSet.{u}) _⦋1⦌ :=
    SSet.stdSimplex.edge
      g.n (0 : Fin (g.n + 1)) (Fin.last g.n) (Fin.zero_le _)
  have hσ :
      (Δ[g.n] : SSet.{u}).σ (0 : Fin 2) e =
        (typeAHigherIdToMaxSourceTriangle g).1 := by
    apply SSet.stdSimplex.ext
    intro j
    fin_cases j <;> rfl
  rw [← hσ]
  exact sΔ.thin_sigma_zero e

/-! ## The forced non-thin target witness -/

/-- The image of the uniform source witness is the triangle `[0,i,n]`. -/
def typeAHigherIdToMaxTargetTriangle
    (g : StandardTypeAHornGeneratorIndex) :
    (Δ[g.n] : SSet.{u}) _⦋2⦌ :=
  SSet.stdSimplex.triangle
    (0 : Fin (g.n + 1))
    g.i
    (Fin.last g.n)
    (Fin.zero_le _)
    g.inner_right.le

/-- The pointwise-max prism sends the uniform source witness exactly to
`[0,i,n]`. -/
theorem typeAHigherIdToMaxPrismMap_sourceTriangle
    (g : StandardTypeAHornGeneratorIndex) :
    (typeAHigherIdToMaxPrismMap g).app (op ⦋2⦌)
        (typeAHigherIdToMaxSourceTriangle g) =
      typeAHigherIdToMaxTargetTriangle g := by
  apply SSet.stdSimplex.ext
  intro j
  fin_cases j
  · rfl
  · change max (0 : Fin (g.n + 1)) g.i = g.i
    exact max_eq_right (Fin.zero_le _)
  · change max (Fin.last g.n) g.i = Fin.last g.n
    exact max_eq_left (Fin.le_last _)

/-- The image triangle `[0,i,n]` is nondegenerate for every inner type-(A)
index. -/
theorem typeAHigherIdToMaxTargetTriangle_nondegenerate
    (g : StandardTypeAHornGeneratorIndex) :
    typeAHigherIdToMaxTargetTriangle g ∈
      (Δ[g.n] : SSet.{u}).nonDegenerate 2 := by
  rw [SSet.stdSimplex.mem_nonDegenerate_iff_strictMono,
    Fin.strictMono_iff_lt_succ]
  intro j
  fin_cases j
  · change (0 : Fin (g.n + 1)) < g.i
    exact g.inner_left
  · change g.i < Fin.last g.n
    exact g.inner_right

/-- In dimension at least three, `[0,i,n]` is not the unique distinguished
consecutive type-(A) triangle. -/
theorem typeAHigherIdToMaxTargetTriangle_not_distinguished
    (g : StandardTypeAHornGeneratorIndex)
    (h3 : 3 ≤ g.n) :
    ¬ IsStandardTypeADistinguishedTriangle
        g.i (typeAHigherIdToMaxTargetTriangle g) := by
  intro hdist
  have hleft : 1 = g.i.val := by
    simpa [typeAHigherIdToMaxTargetTriangle] using hdist.2.1
  have hright : g.i.val + 1 = g.n := by
    simpa [typeAHigherIdToMaxTargetTriangle] using hdist.2.2
  omega

/-- Therefore `[0,i,n]` is not thin in the sparse standard type-(A) scaling
whenever `n >= 3`. -/
theorem typeAHigherIdToMaxTargetTriangle_not_thin
    (g : StandardTypeAHornGeneratorIndex)
    (h3 : 3 ≤ g.n) :
    ¬ (standardTypeASimplexScaling g.i).thin
        (typeAHigherIdToMaxTargetTriangle g) :=
  standardTypeA_not_thin_of_nondegenerate_of_not_distinguished
    g.i
    (typeAHigherIdToMaxTargetTriangle g)
    (typeAHigherIdToMaxTargetTriangle_nondegenerate g)
    (typeAHigherIdToMaxTargetTriangle_not_distinguished g h3)

/-! ## Rigidity: the v1.114 contraction cannot be scaled in higher Type A -/

/-- No choice of base scaling on `Delta[n]` can make the ambient pointwise-max
prism a scaled map into the standard type-(A) simplex when `n >= 3`.

The statement is deliberately stronger than the specialization needed for the
standard type-(A) cylinder: the obstruction comes from a degenerate first
coordinate, so it survives every possible admissible base scaling. -/
theorem typeAHigherIdToMaxPrismMap_not_scaled
    (g : StandardTypeAHornGeneratorIndex)
    (h3 : 3 ≤ g.n)
    (sΔ : ScaledSimplicialSet (Δ[g.n] : SSet.{u})) :
    ¬ IsScaledMap
        (simplexCylinderScaling sΔ)
        (standardTypeASimplexScaling g.i)
        (typeAHigherIdToMaxPrismMap g) := by
  intro hscaled
  have himage :=
    hscaled
      (typeAHigherIdToMaxSourceTriangle g)
      (typeAHigherIdToMaxSourceTriangle_thin g sΔ)
  rw [typeAHigherIdToMaxPrismMap_sourceTriangle g] at himage
  exact typeAHigherIdToMaxTargetTriangle_not_thin g h3 himage

/-- In particular, the standard type-(A) cylinder scaling itself cannot turn
the v1.114 pointwise-max contraction formula into a presentation-level scaled
homotopy in any dimension at least three. -/
theorem standardTypeAHigherIdToMaxPrismMap_not_scaled
    (g : StandardTypeAHornGeneratorIndex)
    (h3 : 3 ≤ g.n) :
    ¬ IsScaledMap
        (simplexCylinderScaling (standardTypeASimplexScaling g.i))
        (standardTypeASimplexScaling g.i)
        (typeAHigherIdToMaxPrismMap g) :=
  typeAHigherIdToMaxPrismMap_not_scaled
    g h3 (standardTypeASimplexScaling g.i)

/-- Existential packaging: there is no alternate simplex scaling that repairs
the pointwise-max prism. -/
theorem no_base_scaling_repairs_typeAHigherIdToMaxPrism
    (g : StandardTypeAHornGeneratorIndex)
    (h3 : 3 ≤ g.n) :
    ¬ ∃ sΔ : ScaledSimplicialSet (Δ[g.n] : SSet.{u}),
        IsScaledMap
          (simplexCylinderScaling sΔ)
          (standardTypeASimplexScaling g.i)
          (typeAHigherIdToMaxPrismMap g) := by
  rintro ⟨sΔ, hs⟩
  exact typeAHigherIdToMaxPrismMap_not_scaled g h3 sΔ hs

/-!
The presentation-level search space is now sharper:

```text
object-level contraction (v1.114)
  id ~ max(-,i) ~ const_i
        |
        | target scaling becomes maximal only after assuming fibrancy
        v
  strict terminal horn fillers

presentation-level reverse comparison
  target retains sparse one-thin Type-A scaling
        |
        +-- one lower-cylinder full retract impossible for n >= 3   (v1.112)
        |
        +-- v1.114 pointwise-max prism impossible for n >= 3       (v1.116)
        v
  genuinely relative multi-cell geometry remains.
```

Thus the successful object-level argument and the still-open left-class
comparison are now separated not only conceptually but by an explicit uniform
scaling obstruction theorem.
-/

end KUOS.DependentOriginationCanonicalTypeAHigherMaxPrismRigidityV1_116