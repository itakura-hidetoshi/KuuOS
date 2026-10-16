import KUOS.DependentOriginationDoubleDeloopingTypeALowDimensionalFillersV1_102

namespace KUOS.DependentOriginationDoubleDeloopingTypeAHighDimensionalFillersV1_103

open CategoryTheory
open CategoryTheory.Category
open CategoryTheory.Bicategory
open Opposite
open Simplicial
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationGlobalDuskinScaledNerveV1_21
open KUOS.DependentOriginationScaledTerminalRLPV1_41
open KUOS.DependentOriginationStandardTypeAScaledHornFamilyV1_49
open KUOS.DependentOriginationStandardTypeAEndpointPushoutProductV1_50
open KUOS.DependentOriginationDoubleDeloopingNatNonthinDuskinWitnessV1_95
open KUOS.DependentOriginationDoubleDeloopingThinComparisonZeroV1_96
open KUOS.DependentOriginationDoubleDeloopingTypeBTetrahedralZeroV1_97
open KUOS.DependentOriginationDoubleDeloopingHornCoherenceLowDimV1_99
open KUOS.DependentOriginationDoubleDeloopingNormalizedCocycleRealizationV1_100
open KUOS.DependentOriginationDoubleDeloopingTypeACocycleLiftingV1_101
open KUOS.DependentOriginationDoubleDeloopingTypeALowDimensionalFillersV1_102

/-!
# High-dimensional literal type-(A) fillers for `B²ℕ` v1.103

Version v1.102 closes the genuinely low-dimensional type-(A) fillers in
simplicial dimensions two and three.  This file removes all higher-dimensional
algebra from the remaining problem.

For `n >= 4`, every triangle of `Delta[n]` already lies in every horn.  Hence a
horn map into the Duskin nerve of `B²ℕ` prescribes a natural-number comparison
label on every ordered triangle.  We prove a single simplicial-naturality lemma
which identifies the `mapComp` of the image of an arbitrary horn simplex with
the corresponding visible triangle label.

For `n >= 5`, every tetrahedron also lies in the horn.  Applying the additive
Duskin associativity equation to its image proves the cocycle equation for the
visible labels.  Thus these labels form a normalized additive cocycle, whose
Yoneda realization restricts literally to the original horn map.  The standard
type-(A) distinguished triangle is thin in the source, so its visible label is
zero and the realized filler is scaled.

Consequently every standard type-(A) generator of dimension at least five has
the literal terminal RLP.  After this file only dimension four remains in the
type-(A) family; that case is finite and is governed by the four-imply-five
tetrahedron dependency already proved in v1.99.
-/

/-! ## Every ordered triangle is visible from dimension four onward -/

/-- The standard ordered triangle, bundled as a simplex of the horn. -/
def natTypeAHornTriangle
    (g : StandardTypeAHornGeneratorIndex)
    (hn : 4 ≤ g.n)
    (a b c : Fin (g.n + 1))
    (hab : a ≤ b) (hbc : b ≤ c) :
    (Λ[g.n, g.i] : SSet).obj (op ⦋2⦌) :=
  ⟨SSet.stdSimplex.triangle a b c hab hbc, by
    rw [horn_all_two_simplices_of_four_le g.i hn]
    exact Set.mem_univ _⟩

/-- The comparison label prescribed by a type-(A) horn map on an ordered
triangle. -/
def natTypeAHornLabel
    (g : StandardTypeAHornGeneratorIndex)
    (hn : 4 ≤ g.n)
    (f : standardTypeAScaledHorn g ⟶ natDoubleDeloopingScaledDuskin)
    (a b c : Fin (g.n + 1))
    (hab : a ≤ b) (hbc : b ≤ c) : Nat :=
  duskinComparison
    (f.map.app (op ⦋2⦌)
      (natTypeAHornTriangle g hn a b c hab hbc))

/-- A repeated left vertex is a simplicial degeneracy, hence its visible horn
label is zero. -/
theorem natTypeAHornLabel_left_zero
    (g : StandardTypeAHornGeneratorIndex)
    (hn : 4 ≤ g.n)
    (f : standardTypeAScaledHorn g ⟶ natDoubleDeloopingScaledDuskin)
    (a b : Fin (g.n + 1)) (hab : a ≤ b) :
    natTypeAHornLabel g hn f a a b (le_refl a) hab = 0 := by
  apply
    (natDuskin_thin_iff_comparison_eq_zero
      (f.map.app (op ⦋2⦌)
        (natTypeAHornTriangle g hn a a b (le_refl a) hab))).1
  apply f.scaled
  change
    (standardTypeASimplexScaling g.i).thin
      (SSet.stdSimplex.triangle a a b (le_refl a) hab)
  left
  left
  refine ⟨SSet.stdSimplex.edge g.n a b hab, ?_⟩
  apply SSet.stdSimplex.ext
  intro k
  fin_cases k <;> rfl

/-- A repeated right vertex is a simplicial degeneracy, hence its visible horn
label is zero. -/
theorem natTypeAHornLabel_right_zero
    (g : StandardTypeAHornGeneratorIndex)
    (hn : 4 ≤ g.n)
    (f : standardTypeAScaledHorn g ⟶ natDoubleDeloopingScaledDuskin)
    (a b : Fin (g.n + 1)) (hab : a ≤ b) :
    natTypeAHornLabel g hn f a b b hab (le_refl b) = 0 := by
  apply
    (natDuskin_thin_iff_comparison_eq_zero
      (f.map.app (op ⦋2⦌)
        (natTypeAHornTriangle g hn a b b hab (le_refl b)))).1
  apply f.scaled
  change
    (standardTypeASimplexScaling g.i).thin
      (SSet.stdSimplex.triangle a b b hab (le_refl b))
  left
  right
  refine ⟨SSet.stdSimplex.edge g.n a b hab, ?_⟩
  apply SSet.stdSimplex.ext
  intro k
  fin_cases k <;> rfl

/-- The distinguished consecutive type-(A) triangle is source-thin, so its
visible comparison label is zero. -/
theorem natTypeAHornLabel_distinguished_zero
    (g : StandardTypeAHornGeneratorIndex)
    (hn : 4 ≤ g.n)
    (f : standardTypeAScaledHorn g ⟶ natDoubleDeloopingScaledDuskin)
    (a b c : Fin (g.n + 1))
    (hab : a ≤ b) (hbc : b ≤ c)
    (hbi : b = g.i)
    (ha : a.val + 1 = g.i.val)
    (hc : g.i.val + 1 = c.val) :
    natTypeAHornLabel g hn f a b c hab hbc = 0 := by
  apply
    (natDuskin_thin_iff_comparison_eq_zero
      (f.map.app (op ⦋2⦌)
        (natTypeAHornTriangle g hn a b c hab hbc))).1
  apply f.scaled
  change
    (standardTypeASimplexScaling g.i).thin
      (SSet.stdSimplex.triangle a b c hab hbc)
  right
  exact ⟨by simpa using hbi, by simpa using ha, by simpa using hc⟩

/-! ## Simplicial naturality identifies every local mapComp with a visible label -/

/-- The comparison carried by the image of an arbitrary horn simplex on an
ordered triple of its vertices is exactly the comparison label of the
corresponding visible triangle of the ambient standard simplex. -/
theorem natTypeAHornMap_mapComp_eq_label
    (g : StandardTypeAHornGeneratorIndex)
    (hn : 4 ≤ g.n)
    (f : standardTypeAScaledHorn g ⟶ natDoubleDeloopingScaledDuskin)
    {m : Nat}
    (x : (Λ[g.n, g.i] : SSet).obj (op ⦋m⦌))
    {a b c : DuskinOrdinal m}
    (p : a ⟶ b) (q : b ⟶ c) :
    (f.map.app (op ⦋m⦌) x).mapComp p q =
      natTypeAHornLabel g hn f
        (x.val a.as) (x.val b.as) (x.val c.as)
        ((SSet.stdSimplex.monotone_apply x.val) p.as.le)
        ((SSet.stdSimplex.monotone_apply x.val) q.as.le) := by
  let t : (Δ[m] : SSet).obj (op ⦋2⦌) :=
    SSet.stdSimplex.triangle a.as b.as c.as p.as.le q.as.le
  let alpha : ⦋2⦌ ⟶ ⦋m⦌ := SSet.stdSimplex.objEquiv t
  have hsource :
      (Λ[g.n, g.i] : SSet).map alpha.op x =
        natTypeAHornTriangle g hn
          (x.val a.as) (x.val b.as) (x.val c.as)
          ((SSet.stdSimplex.monotone_apply x.val) p.as.le)
          ((SSet.stdSimplex.monotone_apply x.val) q.as.le) := by
    apply Subtype.ext
    apply SSet.stdSimplex.ext
    intro k
    fin_cases k <;> rfl
  have hnat :
      f.map.app (op ⦋2⦌) ((Λ[g.n, g.i] : SSet).map alpha.op x) =
        (duskinNerve NatDoubleDelooping).map alpha.op
          (f.map.app (op ⦋m⦌) x) := by
    exact ConcreteCategory.congr_hom (f.map.naturality alpha.op) x
  calc
    (f.map.app (op ⦋m⦌) x).mapComp p q =
        (f.map.app (op ⦋m⦌) x).mapComp
          (natOrdinalEdge p.as.le) (natOrdinalEdge q.as.le) := by
            congr <;> exact Subsingleton.elim _ _
    _ = duskinComparison
        ((duskinNerve NatDoubleDelooping).map alpha.op
          (f.map.app (op ⦋m⦌) x)) := by
          symm
          simpa [t, alpha] using
            natSimplex_triangle_face_comparison
              (f.map.app (op ⦋m⦌) x)
              a.as b.as c.as p.as.le q.as.le
    _ = duskinComparison
        (f.map.app (op ⦋2⦌)
          (natTypeAHornTriangle g hn
            (x.val a.as) (x.val b.as) (x.val c.as)
            ((SSet.stdSimplex.monotone_apply x.val) p.as.le)
            ((SSet.stdSimplex.monotone_apply x.val) q.as.le))) := by
          apply congrArg duskinComparison
          rw [← hsource]
          exact hnat.symm
    _ = natTypeAHornLabel g hn f
        (x.val a.as) (x.val b.as) (x.val c.as)
        ((SSet.stdSimplex.monotone_apply x.val) p.as.le)
        ((SSet.stdSimplex.monotone_apply x.val) q.as.le) := rfl

/-! ## Every tetrahedron is visible from dimension five onward -/

/-- The ordered tetrahedron with vertices `a <= b <= c <= d`. -/
def natOrderedTetrahedron
    {n : Nat}
    (a b c d : Fin (n + 1))
    (hab : a ≤ b) (hbc : b ≤ c) (hcd : c ≤ d) :
    (Δ[n] : SSet).obj (op ⦋3⦌) := by
  refine SSet.stdSimplex.objMk ⟨![a, b, c, d], ?_⟩
  rw [Fin.monotone_iff_le_succ]
  intro k
  fin_cases k
  · exact hab
  · exact hbc
  · exact hcd

/-- From dimension five onward the ordered tetrahedron is itself a horn
simplex. -/
def natTypeAHornTetrahedron
    (g : StandardTypeAHornGeneratorIndex)
    (hn : 5 ≤ g.n)
    (a b c d : Fin (g.n + 1))
    (hab : a ≤ b) (hbc : b ≤ c) (hcd : c ≤ d) :
    (Λ[g.n, g.i] : SSet).obj (op ⦋3⦌) :=
  ⟨natOrderedTetrahedron a b c d hab hbc hcd, by
    rw [horn_all_three_simplices_of_five_le g.i hn]
    exact Set.mem_univ _⟩

/-- The four visible triangle labels of every ordered tetrahedron satisfy the
additive Duskin cocycle equation. -/
theorem natTypeAHornLabel_tetrahedron_of_five_le
    (g : StandardTypeAHornGeneratorIndex)
    (hn : 5 ≤ g.n)
    (f : standardTypeAScaledHorn g ⟶ natDoubleDeloopingScaledDuskin)
    (a b c d : Fin (g.n + 1))
    (hab : a ≤ b) (hbc : b ≤ c) (hcd : c ≤ d) :
    natTypeAHornLabel g (by omega) f a b c hab hbc +
        natTypeAHornLabel g (by omega) f a c d (hab.trans hbc) hcd =
      natTypeAHornLabel g (by omega) f b c d hbc hcd +
        natTypeAHornLabel g (by omega) f a b d hab (hbc.trans hcd) := by
  let x := natTypeAHornTetrahedron g hn a b c d hab hbc hcd
  let sigma : DuskinSimplex NatDoubleDelooping 3 :=
    f.map.app (op ⦋3⦌) x
  let e01 :
      LocallyDiscrete.mk (0 : Fin 4) ⟶ LocallyDiscrete.mk (1 : Fin 4) :=
    natOrdinalEdge (by decide)
  let e12 :
      LocallyDiscrete.mk (1 : Fin 4) ⟶ LocallyDiscrete.mk (2 : Fin 4) :=
    natOrdinalEdge (by decide)
  let e23 :
      LocallyDiscrete.mk (2 : Fin 4) ⟶ LocallyDiscrete.mk (3 : Fin 4) :=
    natOrdinalEdge (by decide)
  have hcoc := natDuskin_mapComp_additive_cocycle sigma e01 e12 e23
  have h012 :=
    natTypeAHornMap_mapComp_eq_label g (by omega) f x e01 e12
  have h023 :=
    natTypeAHornMap_mapComp_eq_label g (by omega) f x (e01 ≫ e12) e23
  have h123 :=
    natTypeAHornMap_mapComp_eq_label g (by omega) f x e12 e23
  have h013 :=
    natTypeAHornMap_mapComp_eq_label g (by omega) f x e01 (e12 ≫ e23)
  rw [h012, h023, h123, h013] at hcoc
  simpa [x, sigma, natTypeAHornTetrahedron, natOrderedTetrahedron,
    e01, e12, e23] using hcoc

/-! ## The visible labels form the normalized high-dimensional cocycle -/

/-- In dimension at least five, the horn labels themselves are a normalized
additive Duskin cocycle. -/
def natTypeAHighCocycle
    (g : StandardTypeAHornGeneratorIndex)
    (hn : 5 ≤ g.n)
    (f : standardTypeAScaledHorn g ⟶ natDoubleDeloopingScaledDuskin) :
    NatNormalizedDuskinCocycle g.n where
  label := natTypeAHornLabel g (by omega) f
  left_normalized := by
    intro a b hab
    exact natTypeAHornLabel_left_zero g (by omega) f a b hab
  right_normalized := by
    intro a b hab
    exact natTypeAHornLabel_right_zero g (by omega) f a b hab
  tetrahedron := by
    intro a b c d hab hbc hcd
    exact
      natTypeAHornLabel_tetrahedron_of_five_le
        g hn f a b c d hab hbc hcd

namespace NatNormalizedDuskinCocycle

/-- General mapComp formula for the Yoneda realization of a normalized
cocycle, on an arbitrary simplex of the ambient standard simplex. -/
theorem toSimplexMap_mapComp
    {n m : Nat}
    (C : NatNormalizedDuskinCocycle n)
    (x : (Δ[n] : SSet).obj (op ⦋m⦌))
    {a b c : DuskinOrdinal m}
    (p : a ⟶ b) (q : b ⟶ c) :
    (C.toSimplexMap.app (op ⦋m⦌) x).mapComp p q =
      C.label
        (x a.as) (x b.as) (x c.as)
        ((SSet.stdSimplex.monotone_apply x) p.as.le)
        ((SSet.stdSimplex.monotone_apply x) q.as.le) := by
  change
    (C.toDuskinSimplex.mapComp
        ((duskinReindex (SSet.stdSimplex.objEquiv x).op).map p)
        ((duskinReindex (SSet.stdSimplex.objEquiv x).op).map q) ≫
      C.toDuskinSimplex.map₂
        ((duskinReindex (SSet.stdSimplex.objEquiv x).op).mapComp p q)) = _
  rw [C.toDuskinSimplex_map₂]
  change _ + 0 = _
  rw [Nat.add_zero]
  rfl

end NatNormalizedDuskinCocycle

/-- The realized high-dimensional cocycle restricts literally to the original
horn map in every simplicial degree. -/
theorem natTypeAHighCocycle_restrict
    (g : StandardTypeAHornGeneratorIndex)
    (hn : 5 ≤ g.n)
    (f : standardTypeAScaledHorn g ⟶ natDoubleDeloopingScaledDuskin) :
    (Λ[g.n, g.i].ι :
      (Λ[g.n, g.i] : SSet) ⟶ (Δ[g.n] : SSet)) ≫
        (natTypeAHighCocycle g hn f).toSimplexMap = f.map := by
  ext Δ x
  rcases Δ with ⟨⟨m⟩⟩
  apply natDuskinSimplex_eq_of_mapComp_eq
  intro a b c p q
  change
    ((natTypeAHighCocycle g hn f).toSimplexMap.app
      (op ⦋m⦌) x.val).mapComp p q =
      (f.map.app (op ⦋m⦌) x).mapComp p q
  rw [NatNormalizedDuskinCocycle.toSimplexMap_mapComp]
  exact
    (natTypeAHornMap_mapComp_eq_label
      g (by omega) f x p q).symm

/-- The high-dimensional visible cocycle has zero distinguished type-(A)
comparison. -/
theorem natTypeAHighCocycle_distinguished_zero
    (g : StandardTypeAHornGeneratorIndex)
    (hn : 5 ≤ g.n)
    (f : standardTypeAScaledHorn g ⟶ natDoubleDeloopingScaledDuskin) :
    (natTypeAHighCocycle g hn f).TypeADistinguishedZero g.i := by
  intro a b c hab hbc hbi ha hc
  change
    natTypeAHornLabel g (by omega) f a b c hab hbc = 0
  exact
    natTypeAHornLabel_distinguished_zero
      g (by omega) f a b c hab hbc hbi ha hc

/-- Every standard type-(A) horn of dimension at least five has a literal
normalized-cocycle completion. -/
theorem natTypeAHigh_cocycle_completion
    (g : StandardTypeAHornGeneratorIndex)
    (hn : 5 ≤ g.n)
    (f : standardTypeAScaledHorn g ⟶ natDoubleDeloopingScaledDuskin) :
    Nonempty (NatTypeAHornCocycleCompletion g f) := by
  refine ⟨{
    cocycle := natTypeAHighCocycle g hn f
    restrict := natTypeAHighCocycle_restrict g hn f
    distinguished_zero :=
      natTypeAHighCocycle_distinguished_zero g hn f }⟩

/-- Literal terminal RLP for every standard type-(A) generator of dimension at
least five. -/
theorem natDoubleDelooping_hasLiftingProperty_standardTypeA_of_five_le
    (g : StandardTypeAHornGeneratorIndex)
    (hn : 5 ≤ g.n) :
    HasLiftingProperty
      (standardTypeAScaledHornGeneratorHom g)
      (ScaledSSet.toPoint natDoubleDeloopingScaledDuskin) := by
  exact
    natDoubleDelooping_hasLiftingProperty_standardTypeA_of_cocycleCompletions
      g (natTypeAHigh_cocycle_completion g hn)

/-!
The type-(A) lifting frontier is now finite:

```text
n = 2      literal zero filler                    -- v1.102
n = 3      literal additive fillers               -- v1.102
n >= 5     literal visible-cocycle fillers        -- v1.103
n = 4      only remaining type-(A) case
```

For `n = 4`, all ten triangle labels are visible.  The four visible
codimension-one tetrahedra satisfy the additive cocycle law by the same
naturality mechanism developed here, and v1.99 proves that those four equations
force the missing fifth equation for each inner index `1`, `2`, or `3`.
Thus no new algebra remains; the next file only has to package that finite
four-simplex dependency into the same literal cocycle-completion interface.
-/

end KUOS.DependentOriginationDoubleDeloopingTypeAHighDimensionalFillersV1_103
