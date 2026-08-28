import KUOS.DependentOriginationDoubleDeloopingHornCoherenceLowDimV1_99

namespace KUOS.DependentOriginationDoubleDeloopingNormalizedCocycleRealizationV1_100

open CategoryTheory
open CategoryTheory.Category
open CategoryTheory.Bicategory
open Opposite
open Simplicial
open KUOS.DependentOriginationGlobalDuskinScaledNerveV1_21
open KUOS.DependentOriginationDoubleDeloopingNatNonthinDuskinWitnessV1_95
open KUOS.DependentOriginationDoubleDeloopingThinComparisonZeroV1_96
open KUOS.DependentOriginationDoubleDeloopingTypeBTetrahedralZeroV1_97
open KUOS.DependentOriginationDoubleDeloopingHornCoherenceLowDimV1_99

/-!
# Normalized additive cocycles realize Duskin simplices in `B²ℕ` v1.100

The v1.99 arithmetic kernel shows that the remaining type-(A) / type-(C)
horn coherence is finite-dimensional.  This file supplies the representation
layer needed to turn those arithmetic labels back into actual simplices of the
Duskin nerve.

For a fixed ordinal `[n]`, a normalized additive cocycle consists of one
natural-number label on every ordered triangle

```text
a <= b <= c
```

such that triangles with a repeated adjacent vertex have label zero and every
ordered tetrahedron satisfies

```text
c(a,b,c) + c(a,c,d) = c(b,c,d) + c(a,b,d).
```

Because `B²ℕ` has one object, one 1-cell, and additive natural-number 2-cells,
this data is exactly the nontrivial part of a strictly unitary lax functor
`[n] -> B²ℕ`.  We construct that lax functor, bundle it as a Duskin simplex,
and then apply simplicial Yoneda to obtain a map

```text
Delta[n] -> N_D(B²ℕ).
```

Conversely every Duskin simplex yields such a normalized cocycle by reading
its composition comparisons.  The extract-then-realize construction recovers
all object, 1-cell, 2-cell, and comparison data of the original simplex.

Finally, the comparison of the image of any standard ordered triangle under
the realized Yoneda map is proved to be exactly its cocycle label.  This is the
precise bridge needed by the next type-(A) / type-(C) terminal lifting unit.
-/

/-! ## Ordered ordinal edges -/

/-- The unique edge `i -> j` in the locally discrete ordinal whenever
`i <= j`. -/
def natOrdinalEdge
    {n : Nat} {i j : Fin (n + 1)} (hij : i <= j) :
    LocallyDiscrete.mk i ⟶ LocallyDiscrete.mk j :=
  (homOfLE hij).toLoc

/-! ## Normalized additive cocycles -/

/-- A normalized natural-number-valued Duskin 2-cocycle on `[n]`.

The label is only asked for ordered triples.  The two normalization axioms are
exactly strict unitarity, while `tetrahedron` is the lax associativity law. -/
structure NatNormalizedDuskinCocycle (n : Nat) where
  label :
    ∀ (a b c : Fin (n + 1)), a <= b -> b <= c -> Nat
  left_normalized :
    ∀ (a b : Fin (n + 1)) (hab : a <= b),
      label a a b (le_refl a) hab = 0
  right_normalized :
    ∀ (a b : Fin (n + 1)) (hab : a <= b),
      label a b b hab (le_refl b) = 0
  tetrahedron :
    ∀ (a b c d : Fin (n + 1))
      (hab : a <= b) (hbc : b <= c) (hcd : c <= d),
      label a b c hab hbc +
          label a c d (hab.trans hbc) hcd =
        label b c d hbc hcd +
          label a b d hab (hbc.trans hcd)

namespace NatNormalizedDuskinCocycle

variable {n : Nat}

/-! ## Realization as a normal lax simplex -/

/-- A normalized additive cocycle determines the strictly unitary lax-functor
core of a Duskin simplex in `B²ℕ`. -/
def toCore (C : NatNormalizedDuskinCocycle n) :
    StrictlyUnitaryLaxFunctorCore
      (DuskinOrdinal n) NatDoubleDelooping where
  obj _ := NatDoubleDelooping.star
  map _ := NatOneCell.star
  map_id _ := rfl
  map₂ _ := 0
  map₂_id _ := rfl
  map₂_comp _ _ := rfl
  mapComp {a b c} _f _g :=
    C.label a.as b.as c.as _f.as.le _g.as.le
  mapComp_naturality_left := by
    intros
    simp
  mapComp_naturality_right := by
    intros
    simp
  map₂_leftUnitor := by
    intro a b f
    have hnorm := C.left_normalized a.as b.as f.as.le
    simpa using hnorm.symm
  map₂_rightUnitor := by
    intro a b f
    have hnorm := C.right_normalized a.as b.as f.as.le
    simpa using hnorm.symm
  map₂_associator := by
    intro a b c d f g h
    have hcoc :=
      C.tetrahedron a.as b.as c.as d.as
        f.as.le g.as.le h.as.le
    simpa using hcoc

/-- Realize a normalized additive cocycle as an actual Duskin simplex. -/
def toDuskinSimplex (C : NatNormalizedDuskinCocycle n) :
    DuskinSimplex NatDoubleDelooping n :=
  StrictlyUnitaryLaxFunctor.mk' C.toCore

@[simp]
theorem toDuskinSimplex_mapComp
    (C : NatNormalizedDuskinCocycle n)
    {a b c : DuskinOrdinal n}
    (f : a ⟶ b) (g : b ⟶ c) :
    C.toDuskinSimplex.mapComp f g =
      C.label a.as b.as c.as f.as.le g.as.le := by
  rfl

@[simp]
theorem toDuskinSimplex_map₂
    (C : NatNormalizedDuskinCocycle n)
    {a b : DuskinOrdinal n} {f g : a ⟶ b}
    (eta : f ⟶ g) :
    C.toDuskinSimplex.map₂ eta = 0 := by
  rfl

/-- Simplicial Yoneda turns the realized Duskin simplex into the corresponding
map out of the standard `n`-simplex. -/
def toSimplexMap (C : NatNormalizedDuskinCocycle n) :
    (Δ[n] : SSet) ⟶ duskinNerve NatDoubleDelooping :=
  SSet.yonedaEquiv.symm C.toDuskinSimplex

@[simp]
theorem yonedaEquiv_toSimplexMap
    (C : NatNormalizedDuskinCocycle n) :
    SSet.yonedaEquiv C.toSimplexMap = C.toDuskinSimplex := by
  exact Equiv.apply_symm_apply _ _

/-! ## Read a normalized cocycle from an arbitrary Duskin simplex -/

/-- Every Duskin simplex in `B²ℕ` has a canonical normalized additive cocycle,
obtained by reading its composition-comparison labels on ordered triangles. -/
def ofDuskinSimplex
    (sigma : DuskinSimplex NatDoubleDelooping n) :
    NatNormalizedDuskinCocycle n where
  label a b c hab hbc :=
    sigma.mapComp (natOrdinalEdge hab) (natOrdinalEdge hbc)
  left_normalized := by
    intro a b hab
    have haa :
        natOrdinalEdge (n := n) (le_refl a) =
          𝟙 (LocallyDiscrete.mk a) :=
      Subsingleton.elim _ _
    rw [haa]
    exact natDuskin_mapComp_id_left_eq_zero sigma (natOrdinalEdge hab)
  right_normalized := by
    intro a b hab
    have hbb :
        natOrdinalEdge (n := n) (le_refl b) =
          𝟙 (LocallyDiscrete.mk b) :=
      Subsingleton.elim _ _
    rw [hbb]
    exact natDuskin_mapComp_id_right_eq_zero sigma (natOrdinalEdge hab)
  tetrahedron := by
    intro a b c d hab hbc hcd
    let eab := natOrdinalEdge hab
    let ebc := natOrdinalEdge hbc
    let ecd := natOrdinalEdge hcd
    let eac := natOrdinalEdge (hab.trans hbc)
    let ebd := natOrdinalEdge (hbc.trans hcd)
    have heac : eab ≫ ebc = eac := Subsingleton.elim _ _
    have hebd : ebc ≫ ecd = ebd := Subsingleton.elim _ _
    have hcoc :=
      natDuskin_mapComp_additive_cocycle sigma eab ebc ecd
    rw [heac, hebd] at hcoc
    simpa [eab, ebc, ecd, eac, ebd] using hcoc

@[simp]
theorem ofDuskinSimplex_label
    (sigma : DuskinSimplex NatDoubleDelooping n)
    (a b c : Fin (n + 1))
    (hab : a <= b) (hbc : b <= c) :
    (ofDuskinSimplex sigma).label a b c hab hbc =
      sigma.mapComp (natOrdinalEdge hab) (natOrdinalEdge hbc) := by
  rfl

/-! ## Extract-then-realize recovers all non-proof data -/

/-- Extracting the normalized cocycle of a simplex and realizing it again
recovers every composition-comparison 2-cell. -/
theorem realize_ofDuskinSimplex_mapComp
    (sigma : DuskinSimplex NatDoubleDelooping n)
    {a b c : DuskinOrdinal n}
    (f : a ⟶ b) (g : b ⟶ c) :
    (ofDuskinSimplex sigma).toDuskinSimplex.mapComp f g =
      sigma.mapComp f g := by
  change
    sigma.mapComp
        (natOrdinalEdge f.as.le)
        (natOrdinalEdge g.as.le) =
      sigma.mapComp f g
  rw [show natOrdinalEdge f.as.le = f from Subsingleton.elim _ _,
    show natOrdinalEdge g.as.le = g from Subsingleton.elim _ _]

/-- The same extract-realize construction recovers every mapped 2-cell. -/
theorem realize_ofDuskinSimplex_map₂
    (sigma : DuskinSimplex NatDoubleDelooping n)
    {a b : DuskinOrdinal n} {f g : a ⟶ b}
    (eta : f ⟶ g) :
    (ofDuskinSimplex sigma).toDuskinSimplex.map₂ eta =
      sigma.map₂ eta := by
  rw [natDuskin_map₂_eq_zero sigma eta]
  rfl

/-- It also recovers every mapped 1-cell; both sides are the unique 1-cell of
`B²ℕ`. -/
theorem realize_ofDuskinSimplex_map
    (sigma : DuskinSimplex NatDoubleDelooping n)
    {a b : DuskinOrdinal n} (f : a ⟶ b) :
    (ofDuskinSimplex sigma).toDuskinSimplex.map f =
      sigma.map f := by
  exact Subsingleton.elim _ _

/-- It likewise recovers every mapped object. -/
theorem realize_ofDuskinSimplex_obj
    (sigma : DuskinSimplex NatDoubleDelooping n)
    (a : DuskinOrdinal n) :
    (ofDuskinSimplex sigma).toDuskinSimplex.obj a =
      sigma.obj a := by
  exact Subsingleton.elim _ _

/-! ## General ordered-triangle comparison under Yoneda -/

/-- Restricting an arbitrary `B²ℕ` Duskin `n`-simplex to the standard ordered
triangle with vertices `a <= b <= c` sends the triangle comparison to the
corresponding comparison label in the original simplex. -/
theorem natSimplex_triangle_face_comparison
    (sigma : DuskinSimplex NatDoubleDelooping n)
    (a b c : Fin (n + 1))
    (hab : a <= b) (hbc : b <= c) :
    duskinComparison
        ((duskinNerve NatDoubleDelooping).map
          (SSet.stdSimplex.objEquiv
            (SSet.stdSimplex.triangle a b c hab hbc)).op sigma) =
      sigma.mapComp (natOrdinalEdge hab) (natOrdinalEdge hbc) := by
  change
    (sigma.mapComp
        ((duskinReindex
          (SSet.stdSimplex.objEquiv
            (SSet.stdSimplex.triangle a b c hab hbc)).op).map edge01)
        ((duskinReindex
          (SSet.stdSimplex.objEquiv
            (SSet.stdSimplex.triangle a b c hab hbc)).op).map edge12) ≫
      sigma.map₂
        ((duskinReindex
          (SSet.stdSimplex.objEquiv
            (SSet.stdSimplex.triangle a b c hab hbc)).op).mapComp
              edge01 edge12)) = _
  rw [natDuskin_map₂_eq_zero]
  change _ + 0 = _
  rw [Nat.add_zero]
  rfl

/-- For a realized normalized cocycle, the comparison of the image of every
ordered standard triangle is exactly the cocycle label on that triangle. -/
theorem toSimplexMap_triangle_comparison
    (C : NatNormalizedDuskinCocycle n)
    (a b c : Fin (n + 1))
    (hab : a <= b) (hbc : b <= c) :
    duskinComparison
        (C.toSimplexMap.app (op ⦋2⦌)
          (SSet.stdSimplex.triangle a b c hab hbc)) =
      C.label a b c hab hbc := by
  simp only [toSimplexMap, SSet.yonedaEquiv_symm_app]
  rw [natSimplex_triangle_face_comparison]
  rfl

/-! ## Degree two: thinness is exactly zero cocycle label -/

/-- For a realized degree-two cocycle, Duskin thinness is precisely vanishing
of its unique strict triangle label. -/
theorem realized_two_simplex_thin_iff_label_zero
    (C : NatNormalizedDuskinCocycle 2) :
    (duskinScaling NatDoubleDelooping).thin C.toDuskinSimplex ↔
      C.label (0 : Fin 3) 1 2 (by decide) (by decide) = 0 := by
  rw [natDuskin_thin_iff_comparison_eq_zero]
  rfl

/-!
The representation layer is now exact enough for literal horn lifting:

```text
normalized additive cocycle C on [n]
  -> C.toDuskinSimplex : N_D(B²ℕ)_n
  -> C.toSimplexMap   : Delta[n] -> N_D(B²ℕ)

comparison(image of triangle abc) = C.label a b c.
```

Conversely, every existing Duskin simplex determines `ofDuskinSimplex sigma`,
and realizing it again recovers all non-proof data of `sigma`.

The next unit can therefore work entirely with the finite label arithmetic of
v1.99, construct one completed normalized cocycle, realize it through the
present file, and verify horn extension plus scaledness by the final ordered-
triangle comparison theorem above.  No further bicategory-coherence
construction is required.
-/

end NatNormalizedDuskinCocycle

end KUOS.DependentOriginationDoubleDeloopingNormalizedCocycleRealizationV1_100
