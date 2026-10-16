import KUOS.DependentOriginationDoubleDeloopingTypeBTerminalRLPV1_98
import KUOS.DependentOriginationStandardTypeAEndpointPushoutProductV1_50
import KUOS.DependentOriginationStandardTypeCCollapsedEdgeV1_58
import Mathlib.AlgebraicTopology.SimplicialSet.Horn

namespace KUOS.DependentOriginationDoubleDeloopingHornCoherenceLowDimV1_99

open CategoryTheory
open Opposite
open Simplicial
open KUOS.DependentOriginationStandardTypeAEndpointPushoutProductV1_50
open KUOS.DependentOriginationStandardTypeCCollapsedEdgeV1_58
open KUOS.DependentOriginationDoubleDeloopingNatNonthinDuskinWitnessV1_95
open KUOS.DependentOriginationDoubleDeloopingThinComparisonZeroV1_96
open KUOS.DependentOriginationDoubleDeloopingTypeBTetrahedralZeroV1_97
open KUOS.DependentOriginationDoubleDeloopingTypeBTerminalRLPV1_98

/-!
# Low-dimensional additive horn coherence for `B²ℕ` v1.99

The concrete standard type-(B) terminal RLP is closed in v1.98.  The remaining
standard-right obligations for the additive double delooping are type-(A)
inner scaled horns and type-(C) collapsed outer horns.

The point of this file is to show that their genuinely new *coherence*
content is finite-dimensional.

For `B²ℕ`, a Duskin tetrahedron is governed by the additive equation

```text
a_ijk + a_ikl = a_jkl + a_ijl.
```

In dimension three, the distinguished thin triangle of type-(A) or type-(C)
has label zero, so the missing label is obtained by addition only; no inverse
in `ℕ` is required.  In dimension four, all triangle labels are already
visible in any horn.  The five tetrahedral equations have one dependency, so
any four imply the fifth by cancellation.  From dimension five onward every
3-simplex is already visible in the horn, hence there is no new tetrahedral
coherence equation to prove.

Thus the remaining filler construction can be organized exactly as

```text
n = 2 : type-(A) distinguished comparison is 0
n = 3 : one explicit additive completion
n = 4 : one missing tetrahedron equation follows from the other four
n ≥ 5 : all triangles and tetrahedra already lie in the horn
```

This is the common arithmetic kernel for the subsequent literal type-(A) and
type-(C) terminal lifting proofs.
-/

/-! ## One tetrahedron as a normalized additive cocycle equation -/

/-- The additive Duskin cocycle equation on vertices `0 < 1 < 2 < 3`, written
in the argument order `(012, 013, 023, 123)`. -/
def NatTetrahedronEquation
    (a012 a013 a023 a123 : Nat) : Prop :=
  a012 + a023 = a123 + a013

/-- Type-(A), dimension three, inner index `i = 1`.
The distinguished triangle `012` has label zero.  Given `013` and `123`, the
missing label `023` can be chosen as `123 + 013`. -/
theorem natTypeAThree_i1_additive_completion
    (a013 a123 : Nat) :
    NatTetrahedronEquation 0 a013 (a123 + a013) a123 := by
  simp [NatTetrahedronEquation]

/-- Type-(A), dimension three, inner index `i = 2`.
The distinguished triangle `123` has label zero.  Given `012` and `023`, the
missing label `013` can be chosen as `012 + 023`. -/
theorem natTypeAThree_i2_additive_completion
    (a012 a023 : Nat) :
    NatTetrahedronEquation a012 (a012 + a023) a023 0 := by
  simp [NatTetrahedronEquation]

/-- Type-(C), dimension three.  The distinguished triangle `013` is thin, so
its label is zero.  The missing outer face label `123` can therefore be chosen
as `012 + 023`. -/
theorem natTypeCThree_additive_completion
    (a012 a023 : Nat) :
    NatTetrahedronEquation a012 0 a023 (a012 + a023) := by
  simp [NatTetrahedronEquation]

/-! ## The five tetrahedral equations in a four-simplex -/

/-- The ten triangle labels of an additive four-simplex. -/
structure NatFourSimplexTriangleLabels where
  a012 : Nat
  a013 : Nat
  a014 : Nat
  a023 : Nat
  a024 : Nat
  a034 : Nat
  a123 : Nat
  a124 : Nat
  a134 : Nat
  a234 : Nat

/-- Tetrahedron `0123`. -/
def NatFourSimplexTriangleLabels.eq0123
    (L : NatFourSimplexTriangleLabels) : Prop :=
  NatTetrahedronEquation L.a012 L.a013 L.a023 L.a123

/-- Tetrahedron `0124`. -/
def NatFourSimplexTriangleLabels.eq0124
    (L : NatFourSimplexTriangleLabels) : Prop :=
  NatTetrahedronEquation L.a012 L.a014 L.a024 L.a124

/-- Tetrahedron `0134`. -/
def NatFourSimplexTriangleLabels.eq0134
    (L : NatFourSimplexTriangleLabels) : Prop :=
  NatTetrahedronEquation L.a013 L.a014 L.a034 L.a134

/-- Tetrahedron `0234`. -/
def NatFourSimplexTriangleLabels.eq0234
    (L : NatFourSimplexTriangleLabels) : Prop :=
  NatTetrahedronEquation L.a023 L.a024 L.a034 L.a234

/-- Tetrahedron `1234`. -/
def NatFourSimplexTriangleLabels.eq1234
    (L : NatFourSimplexTriangleLabels) : Prop :=
  NatTetrahedronEquation L.a123 L.a124 L.a134 L.a234

/-- If the four tetrahedra other than `0123` satisfy the cocycle law, then
`0123` satisfies it as well. -/
theorem natFour_eq0123_of_other_four
    (L : NatFourSimplexTriangleLabels)
    (h0124 : L.eq0124)
    (h0134 : L.eq0134)
    (h0234 : L.eq0234)
    (h1234 : L.eq1234) :
    L.eq0123 := by
  simp only [NatFourSimplexTriangleLabels.eq0123,
    NatFourSimplexTriangleLabels.eq0124,
    NatFourSimplexTriangleLabels.eq0134,
    NatFourSimplexTriangleLabels.eq0234,
    NatFourSimplexTriangleLabels.eq1234,
    NatTetrahedronEquation] at *
  omega

/-- If the four tetrahedra other than `0124` satisfy the cocycle law, then
`0124` satisfies it as well. -/
theorem natFour_eq0124_of_other_four
    (L : NatFourSimplexTriangleLabels)
    (h0123 : L.eq0123)
    (h0134 : L.eq0134)
    (h0234 : L.eq0234)
    (h1234 : L.eq1234) :
    L.eq0124 := by
  simp only [NatFourSimplexTriangleLabels.eq0123,
    NatFourSimplexTriangleLabels.eq0124,
    NatFourSimplexTriangleLabels.eq0134,
    NatFourSimplexTriangleLabels.eq0234,
    NatFourSimplexTriangleLabels.eq1234,
    NatTetrahedronEquation] at *
  omega

/-- If the four tetrahedra other than `0134` satisfy the cocycle law, then
`0134` satisfies it as well. -/
theorem natFour_eq0134_of_other_four
    (L : NatFourSimplexTriangleLabels)
    (h0123 : L.eq0123)
    (h0124 : L.eq0124)
    (h0234 : L.eq0234)
    (h1234 : L.eq1234) :
    L.eq0134 := by
  simp only [NatFourSimplexTriangleLabels.eq0123,
    NatFourSimplexTriangleLabels.eq0124,
    NatFourSimplexTriangleLabels.eq0134,
    NatFourSimplexTriangleLabels.eq0234,
    NatFourSimplexTriangleLabels.eq1234,
    NatTetrahedronEquation] at *
  omega

/-- If the four tetrahedra other than `0234` satisfy the cocycle law, then
`0234` satisfies it as well. -/
theorem natFour_eq0234_of_other_four
    (L : NatFourSimplexTriangleLabels)
    (h0123 : L.eq0123)
    (h0124 : L.eq0124)
    (h0134 : L.eq0134)
    (h1234 : L.eq1234) :
    L.eq0234 := by
  simp only [NatFourSimplexTriangleLabels.eq0123,
    NatFourSimplexTriangleLabels.eq0124,
    NatFourSimplexTriangleLabels.eq0134,
    NatFourSimplexTriangleLabels.eq0234,
    NatFourSimplexTriangleLabels.eq1234,
    NatTetrahedronEquation] at *
  omega

/-- If the four tetrahedra other than `1234` satisfy the cocycle law, then
`1234` satisfies it as well.  This is the dimension-four outer-horn equation
needed by type-(C). -/
theorem natFour_eq1234_of_other_four
    (L : NatFourSimplexTriangleLabels)
    (h0123 : L.eq0123)
    (h0124 : L.eq0124)
    (h0134 : L.eq0134)
    (h0234 : L.eq0234) :
    L.eq1234 := by
  simp only [NatFourSimplexTriangleLabels.eq0123,
    NatFourSimplexTriangleLabels.eq0124,
    NatFourSimplexTriangleLabels.eq0134,
    NatFourSimplexTriangleLabels.eq0234,
    NatFourSimplexTriangleLabels.eq1234,
    NatTetrahedronEquation] at *
  omega

/-! ## Exact missing-face forms for the standard generators -/

/-- In a type-(A) four-horn with inner index `1`, the missing 3-face is
`0234`; the other four equations force its cocycle law. -/
theorem natFour_typeA_index1_missing_face
    (L : NatFourSimplexTriangleLabels)
    (h0123 : L.eq0123)
    (h0124 : L.eq0124)
    (h0134 : L.eq0134)
    (h1234 : L.eq1234) :
    L.eq0234 :=
  natFour_eq0234_of_other_four L h0123 h0124 h0134 h1234

/-- In a type-(A) four-horn with inner index `2`, the missing 3-face is
`0134`; the other four equations force its cocycle law. -/
theorem natFour_typeA_index2_missing_face
    (L : NatFourSimplexTriangleLabels)
    (h0123 : L.eq0123)
    (h0124 : L.eq0124)
    (h0234 : L.eq0234)
    (h1234 : L.eq1234) :
    L.eq0134 :=
  natFour_eq0134_of_other_four L h0123 h0124 h0234 h1234

/-- In a type-(A) four-horn with inner index `3`, the missing 3-face is
`0124`; the other four equations force its cocycle law. -/
theorem natFour_typeA_index3_missing_face
    (L : NatFourSimplexTriangleLabels)
    (h0123 : L.eq0123)
    (h0134 : L.eq0134)
    (h0234 : L.eq0234)
    (h1234 : L.eq1234) :
    L.eq0124 :=
  natFour_eq0124_of_other_four L h0123 h0134 h0234 h1234

/-- In the type-(C) dimension-four outer horn, the missing 3-face is `1234`;
the other four equations force its cocycle law. -/
theorem natFour_typeC_missing_outer_face
    (L : NatFourSimplexTriangleLabels)
    (h0123 : L.eq0123)
    (h0124 : L.eq0124)
    (h0134 : L.eq0134)
    (h0234 : L.eq0234) :
    L.eq1234 :=
  natFour_eq1234_of_other_four L h0123 h0124 h0134 h0234

/-! ## Horn visibility in dimensions at least four and five -/

/-- From dimension four onward every 2-simplex of `Delta[n]` already lies in
any horn.  Therefore all additive comparison labels are prescribed by a horn
map; no new triangle label must be invented. -/
theorem horn_all_two_simplices_of_four_le
    {n : Nat} (i : Fin (n + 1)) (hn : 4 ≤ n) :
    (Λ[n, i] : SSet).obj (op ⦋2⦌) = Set.univ := by
  exact SSet.horn_obj_eq_univ i 2 (by omega)

/-- From dimension five onward every 3-simplex of `Delta[n]` already lies in
any horn.  Hence all tetrahedral cocycle equations are already part of the
horn map itself. -/
theorem horn_all_three_simplices_of_five_le
    {n : Nat} (i : Fin (n + 1)) (hn : 5 ≤ n) :
    (Λ[n, i] : SSet).obj (op ⦋3⦌) = Set.univ := by
  exact SSet.horn_obj_eq_univ i 3 (by omega)

/-- Type-(C) has dimension `m + 3`.  For every positive `m`, all triangles are
already visible in its outer horn. -/
theorem typeC_outerHorn_all_two_simplices_of_one_le
    (m : Nat) (hm : 1 ≤ m) :
    (Λ[m + 3, (0 : Fin (m + 4))] : SSet).obj (op ⦋2⦌) = Set.univ := by
  exact horn_all_two_simplices_of_four_le
    (n := m + 3) (0 : Fin (m + 4)) (by omega)

/-- For type-(C) with `m ≥ 2` (dimension at least five), all tetrahedra are
already visible in the outer horn as well. -/
theorem typeC_outerHorn_all_three_simplices_of_two_le
    (m : Nat) (hm : 2 ≤ m) :
    (Λ[m + 3, (0 : Fin (m + 4))] : SSet).obj (op ⦋3⦌) = Set.univ := by
  exact horn_all_three_simplices_of_five_le
    (n := m + 3) (0 : Fin (m + 4)) (by omega)

/-!
The remaining literal filler construction is therefore finite at the level of
new coherence:

* type-(A), `n = 2`: install comparison label `0` on the distinguished triangle;
* type-(A), `n = 3`: use one of the two additive completions above;
* type-(C), `n = 3`: use the outer additive completion above;
* either family, `n = 4`: read all ten triangle labels from the horn and use
  the appropriate four-imply-five theorem;
* `n ≥ 5`: read all triangle labels and all tetrahedral equations directly
  from the horn.

Thus no higher-dimensional algebra remains.  A subsequent realization theorem
can package these labels into the normal-lax simplex and close type-(A) and
type-(C) terminal RLP without introducing any inverse in `ℕ`.
-/

end KUOS.DependentOriginationDoubleDeloopingHornCoherenceLowDimV1_99
