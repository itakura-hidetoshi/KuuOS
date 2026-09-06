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
  map₂ _ := by
    change Nat
    exact 0
  map₂_id _ := rfl
  map₂_comp _ _ := rfl
  mapComp {a b c} _f _g :=
    C.label a.as b.as c.as _f.as.le _g.as.le
  mapComp_naturality_left := by
    intro a b c f f' η g
    set_option backward.isDefEq.respectTransparency false in
      change
        C.label a.as b.as c.as f.as.le g.as.le + 0 =
          0 + C.label a.as b.as c.as f'.as.le g.as.le
    simp only [Nat.add_zero, Nat.zero_add]
  mapComp_naturality_right := by
    intro a b c f g g' η
    set_option backward.isDefEq.respectTransparency false in
      change
        C.label a.as b.as c.as f.as.le g.as.le + 0 =
          0 + C.label a.as b.as c.as f.as.le g'.as.le
    simp only [Nat.add_zero, Nat.zero_add]
  map₂_leftUnitor := by
    intro a b f
    have hnorm := C.left_normalized a.as b.as f.as.le
    rw [hnorm]
    set_option backward.isDefEq.respectTransparency false in
      change (0 : Nat) = (0 : Nat) + 0
    rfl
  map₂_rightUnitor := by
    intro a b f
    have hnorm := C.right_normalized a.as b.as f.as.le
    rw [hnorm]
    set_option backward.isDefEq.respectTransparency false in
      change (0 : Nat) = (0 : Nat) + 0
    rfl
  map₂_associator := by
    intro a b c d f g h
    set_option backward.isDefEq.respectTransparency false in
      change
        C.label a.as b.as c.as f.as.le g.as.le +
            (C.label a.as c.as d.as (f ≫ g).as.le h.as.le + 0) =
          0 +
            (C.label b.as c.as d.as g.as.le h.as.le +
              C.label a.as b.as d.as f.as.le (g ≫ h).as.le)
    have hcoc :=
      C.tetrahedron a.as b.as c.as d.as
        f.as.le g.as.le h.as.le
    omega

/-- Realize a normalized additive cocycle as an actual Duskin simplex. -/
def toDuskinSimplex (C : NatNormalizedDuskinCocycle n) :
    DuskinSimplex NatDoubleDelooping n :=
  StrictlyUnitaryLaxFunctor.mk' C.toCore

/-- `mk'` preserves the cocycle comparison field literally.  Keeping this
projection bridge explicit avoids dependent reduction through the bundled
strictly-unitary lax functor. -/
@[simp]
theorem toDuskinSimplex_mapComp
    (C : NatNormalizedDuskinCocycle n)
    {a b c : DuskinOrdinal n}
    (f : a ⟶ b) (g : b ⟶ c) :
    C.toDuskinSimplex.mapComp f g =
      C.label a.as b.as c.as f.as.le g.as.le := by
  change C.toCore.mapComp f g = _
  rfl

/-- `mk'` preserves the zero action on source 2-cells. -/
@[simp]
theorem toDuskinSimplex_map₂
    (C : NatNormalizedDuskinCocycle n)
    {a b : DuskinOrdinal n} {f g : a ⟶ b}
    (eta : f ⟶ g) :
    C.toDuskinSimplex.map₂ eta = (0 : Nat) := by
  change C.toCore.map₂ eta = (0 : Nat)
  rfl

/-- The realized simplex maps every source edge to the unique 1-cell. -/
@[simp]
theorem toDuskinSimplex_map
    (C : NatNormalizedDuskinCocycle n)
    {a b : DuskinOrdinal n} (f : a ⟶ b) :
    C.toDuskinSimplex.map f = NatOneCell.star := by
  change C.toCore.map f = NatOneCell.star
  rfl

/-- The realized simplex maps every source vertex to the unique object. -/
@[simp]
theorem toDuskinSimplex_obj
    (C : NatNormalizedDuskinCocycle n)
    (a : DuskinOrdinal n) :
    C.toDuskinSimplex.obj a = NatDoubleDelooping.star := by
  change C.toCore.obj a = NatDoubleDelooping.star
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
          𝟙 (LocallyDiscrete.mk a) := by
      apply Discrete.ext
      apply Subsingleton.elim
    rw [haa]
    exact natDuskin_mapComp_id_left_eq_zero sigma (natOrdinalEdge hab)
  right_normalized := by
    intro a b hab
    have hbb :
        natOrdinalEdge (n := n) (le_refl b) =
          𝟙 (LocallyDiscrete.mk b) := by
      apply Discrete.ext
      apply Subsingleton.elim
    rw [hbb]
    exact natDuskin_mapComp_id_right_eq_zero sigma (natOrdinalEdge hab)
  tetrahedron := by
    intro a b c d hab hbc hcd
    let eab := natOrdinalEdge hab
    let ebc := natOrdinalEdge hbc
    let ecd := natOrdinalEdge hcd
    let eac := natOrdinalEdge (hab.trans hbc)
    let ebd := natOrdinalEdge (hbc.trans hcd)
    have heac : eab ≫ ebc = eac := by
      apply Discrete.ext
      apply Subsingleton.elim
    have hebd : ebc ≫ ecd = ebd := by
      apply Discrete.ext
      apply Subsingleton.elim
    have hcoc :=
      natDuskin_mapComp_additive_cocycle sigma eab ebc ecd
    rw [heac, hebd] at hcoc
    simpa [natDuskinMapCompLabel, eab, ebc, ecd, eac, ebd] using hcoc

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
  rw [toDuskinSimplex_mapComp, ofDuskinSimplex_label]
  have hf : natOrdinalEdge f.as.le = f := by
    apply Discrete.ext
    apply Subsingleton.elim
  have hg : natOrdinalEdge g.as.le = g := by
    apply Discrete.ext
    apply Subsingleton.elim
  rw [hf, hg]

/-- The same extract-realize construction recovers every mapped 2-cell. -/
theorem realize_ofDuskinSimplex_map₂
    (sigma : DuskinSimplex NatDoubleDelooping n)
    {a b : DuskinOrdinal n} {f g : a ⟶ b}
    (eta : f ⟶ g) :
    (ofDuskinSimplex sigma).toDuskinSimplex.map₂ eta =
      sigma.map₂ eta := by
  rw [toDuskinSimplex_map₂, natDuskin_map₂_eq_zero]

/-- It also recovers every mapped 1-cell; both sides are the unique 1-cell of
`B²ℕ`. -/
theorem realize_ofDuskinSimplex_map
    (sigma : DuskinSimplex NatDoubleDelooping n)
    {a b : DuskinOrdinal n} (f : a ⟶ b) :
    (ofDuskinSimplex sigma).toDuskinSimplex.map f =
      sigma.map f := by
  calc
    (ofDuskinSimplex sigma).toDuskinSimplex.map f = NatOneCell.star :=
      toDuskinSimplex_map (ofDuskinSimplex sigma) f
    _ = sigma.map f := Subsingleton.elim _ _

/-- It likewise recovers every mapped object. -/
theorem realize_ofDuskinSimplex_obj
    (sigma : DuskinSimplex NatDoubleDelooping n)
    (a : DuskinOrdinal n) :
    (ofDuskinSimplex sigma).toDuskinSimplex.obj a =
      sigma.obj a := by
  calc
    (ofDuskinSimplex sigma).toDuskinSimplex.obj a =
        NatDoubleDelooping.star :=
      toDuskinSimplex_obj (ofDuskinSimplex sigma) a
    _ = sigma.obj a := Subsingleton.elim _ _

/-! ## General ordered-triangle comparison under Yoneda -/

/-- The concrete standard triangle with ordered vertices `a <= b <= c`. -/
def natSimplexTriangle
    {n : Nat}
    (a b c : Fin (n + 1))
    (hab : a <= b) (hbc : b <= c) :
    (Δ[n] : SSet).obj (op ⦋2⦌) :=
  SSet.stdSimplex.triangle a b c hab hbc

/-- The face map `[2] -> [n]` selected by `natSimplexTriangle`.  The explicit
universe-0 specialization fixes the hidden `ULift` universe exactly as in the
validated degree-four Yoneda bridge of v1.98. -/
def natSimplexTriangleFace
    {n : Nat}
    (a b c : Fin (n + 1))
    (hab : a <= b) (hbc : b <= c) :
    ⦋2⦌ ⟶ ⦋n⦌ :=
  SSet.stdSimplex.objEquiv.{0}
    (natSimplexTriangle.{0} a b c hab hbc)

/-- Restricting an arbitrary `B²ℕ` Duskin `n`-simplex to the standard ordered
triangle with vertices `a <= b <= c` sends the triangle comparison to the
corresponding comparison label in the original simplex. -/
theorem natSimplex_triangle_face_comparison
    (sigma : DuskinSimplex NatDoubleDelooping n)
    (a b c : Fin (n + 1))
    (hab : a <= b) (hbc : b <= c) :
    (duskinComparison
        ((duskinNerve NatDoubleDelooping).map
          (SSet.stdSimplex.objEquiv
            (SSet.stdSimplex.triangle a b c hab hbc)).op sigma) : Nat) =
      (sigma.mapComp (natOrdinalEdge hab) (natOrdinalEdge hbc) : Nat) := by
  change
    (sigma.mapComp
        ((duskinReindex
          (natSimplexTriangleFace a b c hab hbc).op).map edge01)
        ((duskinReindex
          (natSimplexTriangleFace a b c hab hbc).op).map edge12) ≫
      sigma.map₂
        ((duskinReindex
          (natSimplexTriangleFace a b c hab hbc).op).mapComp
              edge01 edge12)) = _
  rw [natDuskin_map₂_eq_zero]
  change _ + 0 = _
  exact (Nat.add_zero _).trans (by
    congr 1)

/-- For a realized normalized cocycle, the comparison of the image of every
ordered standard triangle is exactly the cocycle label on that triangle. -/
theorem toSimplexMap_triangle_comparison
    (C : NatNormalizedDuskinCocycle n)
    (a b c : Fin (n + 1))
    (hab : a <= b) (hbc : b <= c) :
    (duskinComparison
        (C.toSimplexMap.app (op ⦋2⦌)
          (SSet.stdSimplex.triangle a b c hab hbc)) : Nat) =
      C.label a b c hab hbc := by
  change
    (duskinComparison
        ((SSet.yonedaEquiv.symm C.toDuskinSimplex).app (op ⦋2⦌)
          (natSimplexTriangle a b c hab hbc)) : Nat) =
      C.label a b c hab hbc
  calc
    (duskinComparison
        ((SSet.yonedaEquiv.symm C.toDuskinSimplex).app (op ⦋2⦌)
          (natSimplexTriangle a b c hab hbc)) : Nat) =
      (duskinComparison
        ((duskinNerve NatDoubleDelooping).map
          (natSimplexTriangleFace a b c hab hbc).op
          C.toDuskinSimplex) : Nat) := by
      have hyoneda :
          ((SSet.yonedaEquiv.symm C.toDuskinSimplex).app (op ⦋2⦌)
              (natSimplexTriangle a b c hab hbc)) =
            (duskinNerve NatDoubleDelooping).map
              (natSimplexTriangleFace a b c hab hbc).op
              C.toDuskinSimplex :=
        (SSet.stdSimplex.map_objEquiv_op_apply
          (X := duskinNerve NatDoubleDelooping)
          C.toDuskinSimplex
          (natSimplexTriangle a b c hab hbc)).symm
      exact congrArg
        (fun sigma : DuskinSimplex NatDoubleDelooping 2 =>
          (duskinComparison sigma : Nat))
        hyoneda
    _ = (C.toDuskinSimplex.mapComp
          (natOrdinalEdge hab) (natOrdinalEdge hbc) : Nat) := by
      exact natSimplex_triangle_face_comparison
        C.toDuskinSimplex a b c hab hbc
    _ = C.label a b c hab hbc := by
      exact toDuskinSimplex_mapComp C
        (natOrdinalEdge hab) (natOrdinalEdge hbc)

/-! ## Degree two: thinness is exactly zero cocycle label -/

/-- For a realized degree-two cocycle, Duskin thinness is precisely vanishing
of its unique strict triangle label. -/
theorem realized_two_simplex_thin_iff_label_zero
    (C : NatNormalizedDuskinCocycle 2) :
    (duskinScaling NatDoubleDelooping).thin C.toDuskinSimplex ↔
      C.label (0 : Fin 3) 1 2 (by decide) (by decide) = 0 := by
  rw [natDuskin_thin_iff_comparison_eq_zero]
  change C.toDuskinSimplex.mapComp edge01 edge12 = (0 : Nat) ↔ _
  rw [toDuskinSimplex_mapComp]

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
