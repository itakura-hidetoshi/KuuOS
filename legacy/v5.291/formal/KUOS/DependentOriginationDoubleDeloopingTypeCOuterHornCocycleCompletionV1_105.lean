import KUOS.DependentOriginationDoubleDeloopingTypeADimensionFourFamilyRLPV1_104

namespace KUOS.DependentOriginationDoubleDeloopingTypeCOuterHornCocycleCompletionV1_105

open CategoryTheory
open CategoryTheory.Category
open CategoryTheory.Bicategory
open CategoryTheory.Limits
open Opposite
open Simplicial
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationGlobalDuskinScaledNerveV1_21
open KUOS.DependentOriginationScaledTerminalRLPV1_41
open KUOS.DependentOriginationStandardTypeCCollapsedEdgeV1_58
open KUOS.DependentOriginationDoubleDeloopingNatNonthinDuskinWitnessV1_95
open KUOS.DependentOriginationDoubleDeloopingThinComparisonZeroV1_96
open KUOS.DependentOriginationDoubleDeloopingTypeBTetrahedralZeroV1_97
open KUOS.DependentOriginationDoubleDeloopingHornCoherenceLowDimV1_99
open KUOS.DependentOriginationDoubleDeloopingNormalizedCocycleRealizationV1_100
open KUOS.DependentOriginationDoubleDeloopingTypeALowDimensionalFillersV1_102
open KUOS.DependentOriginationDoubleDeloopingTypeAHighDimensionalFillersV1_103
open KUOS.DependentOriginationDoubleDeloopingTypeADimensionFourFamilyRLPV1_104

noncomputable section

/-!
# Type-(C) outer-horn cocycle completion for `B²ℕ` v1.105

The standard type-(A) and type-(B) terminal right lifting properties are now
closed.  The remaining standard A/B/C generator family is type-(C):

```text
Λ^n_0 ⨿_{Δ^{01}} Δ^0  -->  Δ^n ⨿_{Δ^{01}} Δ^0,
```

with `n = m + 3` and with the image of the triangle `01n` declared thin.
This file isolates the arithmetic part of the lifting problem from the quotient
pushout geometry.

Given a scaled map from the collapsed source into the scaled Duskin nerve of
`B²ℕ`, restrict it to the outer-horn leg.  We construct a normalized additive
cocycle on the whole simplex which restricts to that horn map and whose `01n`
comparison is zero.

The construction has exactly the finite pattern predicted in v1.99:

* `m = 0`, `n = 3`: read `012` and `023`, set `013 = 0` and
  `123 = 012 + 023`;
* `m = 1`, `n = 4`: all ten triangle labels are visible and the four visible
  tetrahedron equations imply the missing outer equation `1234`;
* `m ≥ 2`, `n ≥ 5`: all triangles and tetrahedra are visible in the outer horn.

The output is deliberately an exact cocycle-completion interface.  The next
layer can descend the realized simplex map through the native pushout without
mixing the finite arithmetic with the quotient universal property.
-/

/-! ## The two source legs and the induced outer-horn map -/

/-- The horn leg into the collapsed type-(C) source carrier. -/
def natTypeCSourceHornInl (m : Nat) :
    (Λ[m + 3, (0 : Fin (m + 4))] : SSet) ⟶
      standardTypeCSourceCarrier m :=
  pushout.inl
    (standardTypeCEdgeToHorn m)
    (standardTypeCEdgeCollapseToPoint m)

/-- The point leg into the collapsed type-(C) source carrier. -/
def natTypeCSourcePointInr (m : Nat) :
    (Δ[0] : SSet) ⟶ standardTypeCSourceCarrier m :=
  pushout.inr
    (standardTypeCEdgeToHorn m)
    (standardTypeCEdgeCollapseToPoint m)

/-- Restrict a source map to its outer-horn leg. -/
def natTypeCHornMap
    (m : Nat)
    (f : standardTypeCSource m ⟶ natDoubleDeloopingScaledDuskin) :
    (Λ[m + 3, (0 : Fin (m + 4))] : SSet) ⟶
      duskinNerve NatDoubleDelooping :=
  natTypeCSourceHornInl m ≫ f.map

/-- Restrict a source map to its collapsed-point leg. -/
def natTypeCPointMap
    (m : Nat)
    (f : standardTypeCSource m ⟶ natDoubleDeloopingScaledDuskin) :
    (Δ[0] : SSet) ⟶ duskinNerve NatDoubleDelooping :=
  natTypeCSourcePointInr m ≫ f.map

/-! ## Exact outer-horn completion interface -/

/-- A normalized additive cocycle completing the horn leg of one type-(C)
source map.  The last field is exactly the extra target-scaledness condition:
the distinguished triangle `01n` has zero comparison. -/
structure NatTypeCSourceCocycleCompletion
    (m : Nat)
    (f : standardTypeCSource m ⟶ natDoubleDeloopingScaledDuskin) where
  cocycle : NatNormalizedDuskinCocycle (m + 3)
  restrict :
    (Λ[m + 3, (0 : Fin (m + 4))].ι :
      (Λ[m + 3, (0 : Fin (m + 4))] : SSet) ⟶
        (Δ[m + 3] : SSet)) ≫
      cocycle.toSimplexMap = natTypeCHornMap m f
  distinguished_zero :
    cocycle.label
      (0 : Fin (m + 4)) 1 (Fin.last (m + 3))
      (by omega) (by omega) = 0

/-! ## Dimension three: the only missing triangle label -/

/-- In `Λ[3,0]`, face `1` is triangle `023`. -/
theorem typeCThree_face1_val
    (h : (1 : Fin 4) ≠ 0) :
    (SSet.horn.face (0 : Fin 4) (1 : Fin 4) h).val =
      SSet.stdSimplex.triangle
        (0 : Fin 4) 2 3 (by decide) (by decide) := by
  apply SSet.stdSimplex.ext
  intro k
  fin_cases k <;> rfl

/-- In `Λ[3,0]`, face `2` is the distinguished triangle `013`. -/
theorem typeCThree_face2_val
    (h : (2 : Fin 4) ≠ 0) :
    (SSet.horn.face (0 : Fin 4) (2 : Fin 4) h).val =
      SSet.stdSimplex.triangle
        (0 : Fin 4) 1 3 (by decide) (by decide) := by
  apply SSet.stdSimplex.ext
  intro k
  fin_cases k <;> rfl

/-- In `Λ[3,0]`, face `3` is triangle `012`. -/
theorem typeCThree_face3_val
    (h : (3 : Fin 4) ≠ 0) :
    (SSet.horn.face (0 : Fin 4) (3 : Fin 4) h).val =
      SSet.stdSimplex.triangle
        (0 : Fin 4) 1 2 (by decide) (by decide) := by
  apply SSet.stdSimplex.ext
  intro k
  fin_cases k <;> rfl

/-- The horn face `013` is literally the distinguished type-(C) horn triangle. -/
theorem typeCThree_face2_eq_distinguished :
    SSet.horn.face (0 : Fin 4) (2 : Fin 4) (by decide) =
      standardTypeCTriangle01nInHorn 0 := by
  apply Subtype.ext
  rw [typeCThree_face2_val]
  rfl

/-- Visible label `012`. -/
def natTypeCThreeLabel012
    (f : standardTypeCSource 0 ⟶ natDoubleDeloopingScaledDuskin) : Nat :=
  duskinComparison
    ((natTypeCHornMap 0 f).app (op ⦋2⦌)
      (SSet.horn.face (0 : Fin 4) (3 : Fin 4) (by decide)))

/-- Visible label `023`. -/
def natTypeCThreeLabel023
    (f : standardTypeCSource 0 ⟶ natDoubleDeloopingScaledDuskin) : Nat :=
  duskinComparison
    ((natTypeCHornMap 0 f).app (op ⦋2⦌)
      (SSet.horn.face (0 : Fin 4) (1 : Fin 4) (by decide)))

/-- The distinguished visible face `013` has zero comparison because the
source quotient declares it thin and `f` is scaled. -/
theorem natTypeCThreeLabel013_eq_zero
    (f : standardTypeCSource 0 ⟶ natDoubleDeloopingScaledDuskin) :
    duskinComparison
      ((natTypeCHornMap 0 f).app (op ⦋2⦌)
        (SSet.horn.face (0 : Fin 4) (2 : Fin 4) (by decide))) = 0 := by
  apply
    (natDuskin_thin_iff_comparison_eq_zero
      ((natTypeCHornMap 0 f).app (op ⦋2⦌)
        (SSet.horn.face (0 : Fin 4) (2 : Fin 4) (by decide)))).1
  have hthin := f.scaled
    (standardTypeCSourceDistinguishedTriangle 0)
    (standardTypeCSource_distinguished_thin 0)
  simpa [natTypeCHornMap, natTypeCSourceHornInl,
    standardTypeCSourceDistinguishedTriangle,
    typeCThree_face2_eq_distinguished] using hthin

/-- The dimension-three outer-horn completion. -/
def natTypeCThreeCompletionCocycle
    (f : standardTypeCSource 0 ⟶ natDoubleDeloopingScaledDuskin) :
    NatNormalizedDuskinCocycle 3 :=
  natThreeCocycleOfLabels
    (natTypeCThreeLabel012 f)
    0
    (natTypeCThreeLabel023 f)
    (natTypeCThreeLabel012 f + natTypeCThreeLabel023 f)
    (natTypeCThree_additive_completion
      (natTypeCThreeLabel012 f) (natTypeCThreeLabel023 f))

/-- The dimension-three completion restricts literally to the outer horn. -/
theorem natTypeCThreeCompletionCocycle_restrict
    (f : standardTypeCSource 0 ⟶ natDoubleDeloopingScaledDuskin) :
    (Λ[3, (0 : Fin 4)].ι :
      (Λ[3, (0 : Fin 4)] : SSet) ⟶ (Δ[3] : SSet)) ≫
        (natTypeCThreeCompletionCocycle f).toSimplexMap =
      natTypeCHornMap 0 f := by
  apply SSet.horn.hom_ext
  intro j hj
  fin_cases j
  · exact (hj rfl).elim
  · apply natDuskinTwoSimplex_eq_of_comparison_eq
    change
      duskinComparison
          ((natTypeCThreeCompletionCocycle f).toSimplexMap.app
            (op ⦋2⦌)
            (SSet.horn.face (0 : Fin 4) (1 : Fin 4) hj).val) =
        duskinComparison
          ((natTypeCHornMap 0 f).app (op ⦋2⦌)
            (SSet.horn.face (0 : Fin 4) (1 : Fin 4) hj))
    rw [typeCThree_face1_val,
      NatNormalizedDuskinCocycle.toSimplexMap_triangle_comparison]
    simp [natTypeCThreeCompletionCocycle, natTypeCThreeLabel023]
  · apply natDuskinTwoSimplex_eq_of_comparison_eq
    change
      duskinComparison
          ((natTypeCThreeCompletionCocycle f).toSimplexMap.app
            (op ⦋2⦌)
            (SSet.horn.face (0 : Fin 4) (2 : Fin 4) hj).val) =
        duskinComparison
          ((natTypeCHornMap 0 f).app (op ⦋2⦌)
            (SSet.horn.face (0 : Fin 4) (2 : Fin 4) hj))
    rw [typeCThree_face2_val,
      NatNormalizedDuskinCocycle.toSimplexMap_triangle_comparison]
    simpa [natTypeCThreeCompletionCocycle] using
      (natTypeCThreeLabel013_eq_zero f).symm
  · apply natDuskinTwoSimplex_eq_of_comparison_eq
    change
      duskinComparison
          ((natTypeCThreeCompletionCocycle f).toSimplexMap.app
            (op ⦋2⦌)
            (SSet.horn.face (0 : Fin 4) (3 : Fin 4) hj).val) =
        duskinComparison
          ((natTypeCHornMap 0 f).app (op ⦋2⦌)
            (SSet.horn.face (0 : Fin 4) (3 : Fin 4) hj))
    rw [typeCThree_face3_val,
      NatNormalizedDuskinCocycle.toSimplexMap_triangle_comparison]
    simp [natTypeCThreeCompletionCocycle, natTypeCThreeLabel012]

/-- Literal cocycle completion in the first type-(C) dimension. -/
theorem natTypeCThree_cocycle_completion
    (f : standardTypeCSource 0 ⟶ natDoubleDeloopingScaledDuskin) :
    Nonempty (NatTypeCSourceCocycleCompletion 0 f) := by
  refine ⟨{
    cocycle := natTypeCThreeCompletionCocycle f
    restrict := natTypeCThreeCompletionCocycle_restrict f
    distinguished_zero := ?_ }⟩
  simp [natTypeCThreeCompletionCocycle]

/-! ## Visible triangles from dimension four onward -/

/-- Every ordered triangle is an outer-horn simplex for positive `m`. -/
def natTypeCHornTriangle
    (m : Nat) (hm : 1 ≤ m)
    (a b c : Fin (m + 4))
    (hab : a ≤ b) (hbc : b ≤ c) :
    (Λ[m + 3, (0 : Fin (m + 4))] : SSet).obj (op ⦋2⦌) :=
  ⟨SSet.stdSimplex.triangle a b c hab hbc, by
    rw [typeC_outerHorn_all_two_simplices_of_one_le m hm]
    exact Set.mem_univ _⟩

/-- Every ordered edge is also present in the positive-dimensional outer horn. -/
def natTypeCHornEdge
    (m : Nat) (hm : 1 ≤ m)
    (a b : Fin (m + 4)) (hab : a ≤ b) :
    (Λ[m + 3, (0 : Fin (m + 4))] : SSet).obj (op ⦋1⦌) :=
  ⟨SSet.stdSimplex.edge (m + 3) a b hab, by
    rw [SSet.horn_obj_eq_univ (0 : Fin (m + 4)) 1 (by omega)]
    exact Set.mem_univ _⟩

/-- Visible comparison label on an ordered triangle. -/
def natTypeCHornLabel
    (m : Nat) (hm : 1 ≤ m)
    (f : standardTypeCSource m ⟶ natDoubleDeloopingScaledDuskin)
    (a b c : Fin (m + 4))
    (hab : a ≤ b) (hbc : b ≤ c) : Nat :=
  duskinComparison
    ((natTypeCHornMap m f).app (op ⦋2⦌)
      (natTypeCHornTriangle m hm a b c hab hbc))

/-- Repeating the left vertex gives zero comparison. -/
theorem natTypeCHornLabel_left_zero
    (m : Nat) (hm : 1 ≤ m)
    (f : standardTypeCSource m ⟶ natDoubleDeloopingScaledDuskin)
    (a b : Fin (m + 4)) (hab : a ≤ b) :
    natTypeCHornLabel m hm f a a b (le_refl a) hab = 0 := by
  apply
    (natDuskin_thin_iff_comparison_eq_zero
      ((natTypeCHornMap m f).app (op ⦋2⦌)
        (natTypeCHornTriangle m hm a a b (le_refl a) hab))).1
  have hmin :
      (minimalScaling
        (Λ[m + 3, (0 : Fin (m + 4))] : SSet)).thin
        (natTypeCHornTriangle m hm a a b (le_refl a) hab) := by
    left
    refine ⟨natTypeCHornEdge m hm a b hab, ?_⟩
    apply Subtype.ext
    apply SSet.stdSimplex.ext
    intro k
    fin_cases k <;> rfl
  have hinl :=
    (minimalScaling_map
      (minimalScaling (standardTypeCSourceCarrier m))
      (natTypeCSourceHornInl m))
      (natTypeCHornTriangle m hm a a b (le_refl a) hab) hmin
  have hsrc :
      (standardTypeCSourceScaling m).thin
        ((natTypeCSourceHornInl m).app (op ⦋2⦌)
          (natTypeCHornTriangle m hm a a b (le_refl a) hab)) :=
    Or.inl hinl
  exact f.scaled _ hsrc

/-- Repeating the right vertex gives zero comparison. -/
theorem natTypeCHornLabel_right_zero
    (m : Nat) (hm : 1 ≤ m)
    (f : standardTypeCSource m ⟶ natDoubleDeloopingScaledDuskin)
    (a b : Fin (m + 4)) (hab : a ≤ b) :
    natTypeCHornLabel m hm f a b b hab (le_refl b) = 0 := by
  apply
    (natDuskin_thin_iff_comparison_eq_zero
      ((natTypeCHornMap m f).app (op ⦋2⦌)
        (natTypeCHornTriangle m hm a b b hab (le_refl b)))).1
  have hmin :
      (minimalScaling
        (Λ[m + 3, (0 : Fin (m + 4))] : SSet)).thin
        (natTypeCHornTriangle m hm a b b hab (le_refl b)) := by
    right
    refine ⟨natTypeCHornEdge m hm a b hab, ?_⟩
    apply Subtype.ext
    apply SSet.stdSimplex.ext
    intro k
    fin_cases k <;> rfl
  have hinl :=
    (minimalScaling_map
      (minimalScaling (standardTypeCSourceCarrier m))
      (natTypeCSourceHornInl m))
      (natTypeCHornTriangle m hm a b b hab (le_refl b)) hmin
  have hsrc :
      (standardTypeCSourceScaling m).thin
        ((natTypeCSourceHornInl m).app (op ⦋2⦌)
          (natTypeCHornTriangle m hm a b b hab (le_refl b))) :=
    Or.inl hinl
  exact f.scaled _ hsrc

/-- The visible triangle `01n` is literally the distinguished horn triangle. -/
theorem natTypeCHornTriangle_distinguished
    (m : Nat) (hm : 1 ≤ m) :
    natTypeCHornTriangle m hm
      (0 : Fin (m + 4)) 1 (Fin.last (m + 3))
      (by omega) (by omega) =
      standardTypeCTriangle01nInHorn m := by
  apply Subtype.ext
  rfl

/-- The distinguished visible comparison is zero. -/
theorem natTypeCHornLabel_distinguished_zero
    (m : Nat) (hm : 1 ≤ m)
    (f : standardTypeCSource m ⟶ natDoubleDeloopingScaledDuskin) :
    natTypeCHornLabel m hm f
      (0 : Fin (m + 4)) 1 (Fin.last (m + 3))
      (by omega) (by omega) = 0 := by
  apply
    (natDuskin_thin_iff_comparison_eq_zero
      ((natTypeCHornMap m f).app (op ⦋2⦌)
        (natTypeCHornTriangle m hm
          (0 : Fin (m + 4)) 1 (Fin.last (m + 3))
          (by omega) (by omega)))).1
  have hthin := f.scaled
    (standardTypeCSourceDistinguishedTriangle m)
    (standardTypeCSource_distinguished_thin m)
  simpa [natTypeCHornMap, natTypeCSourceHornInl,
    standardTypeCSourceDistinguishedTriangle,
    natTypeCHornTriangle_distinguished] using hthin

/-! ## Simplicial naturality for visible outer-horn labels -/

/-- The `mapComp` of the image of any outer-horn simplex is its ambient visible
triangle label. -/
theorem natTypeCHornMap_mapComp_eq_label
    (m : Nat) (hm : 1 ≤ m)
    (f : standardTypeCSource m ⟶ natDoubleDeloopingScaledDuskin)
    {q : Nat}
    (x : (Λ[m + 3, (0 : Fin (m + 4))] : SSet).obj (op ⦋q⦌))
    {a b c : DuskinOrdinal q}
    (p : a ⟶ b) (r : b ⟶ c) :
    ((natTypeCHornMap m f).app (op ⦋q⦌) x).mapComp p r =
      natTypeCHornLabel m hm f
        (x.val a.as) (x.val b.as) (x.val c.as)
        ((SSet.stdSimplex.monotone_apply x.val) p.as.le)
        ((SSet.stdSimplex.monotone_apply x.val) r.as.le) := by
  let t : (Δ[q] : SSet).obj (op ⦋2⦌) :=
    SSet.stdSimplex.triangle a.as b.as c.as p.as.le r.as.le
  let alpha : ⦋2⦌ ⟶ ⦋q⦌ := SSet.stdSimplex.objEquiv t
  have hsource :
      (Λ[m + 3, (0 : Fin (m + 4))] : SSet).map alpha.op x =
        natTypeCHornTriangle m hm
          (x.val a.as) (x.val b.as) (x.val c.as)
          ((SSet.stdSimplex.monotone_apply x.val) p.as.le)
          ((SSet.stdSimplex.monotone_apply x.val) r.as.le) := by
    apply Subtype.ext
    apply SSet.stdSimplex.ext
    intro k
    fin_cases k <;> rfl
  have hnat :
      (natTypeCHornMap m f).app (op ⦋2⦌)
          ((Λ[m + 3, (0 : Fin (m + 4))] : SSet).map alpha.op x) =
        (duskinNerve NatDoubleDelooping).map alpha.op
          ((natTypeCHornMap m f).app (op ⦋q⦌) x) := by
    exact ConcreteCategory.congr_hom
      ((natTypeCHornMap m f).naturality alpha.op) x
  calc
    ((natTypeCHornMap m f).app (op ⦋q⦌) x).mapComp p r =
        ((natTypeCHornMap m f).app (op ⦋q⦌) x).mapComp
          (natOrdinalEdge p.as.le) (natOrdinalEdge r.as.le) := by
            congr <;> exact Subsingleton.elim _ _
    _ = duskinComparison
        ((duskinNerve NatDoubleDelooping).map alpha.op
          ((natTypeCHornMap m f).app (op ⦋q⦌) x)) := by
          symm
          simpa [t, alpha] using
            natSimplex_triangle_face_comparison
              ((natTypeCHornMap m f).app (op ⦋q⦌) x)
              a.as b.as c.as p.as.le r.as.le
    _ = duskinComparison
        ((natTypeCHornMap m f).app (op ⦋2⦌)
          (natTypeCHornTriangle m hm
            (x.val a.as) (x.val b.as) (x.val c.as)
            ((SSet.stdSimplex.monotone_apply x.val) p.as.le)
            ((SSet.stdSimplex.monotone_apply x.val) r.as.le))) := by
          apply congrArg duskinComparison
          rw [← hsource]
          exact hnat.symm
    _ = natTypeCHornLabel m hm f
        (x.val a.as) (x.val b.as) (x.val c.as)
        ((SSet.stdSimplex.monotone_apply x.val) p.as.le)
        ((SSet.stdSimplex.monotone_apply x.val) r.as.le) := rfl

/-! ## Tetrahedral equations from visible outer-horn 3-simplices -/

/-- A visible outer-horn tetrahedron imposes its additive cocycle equation. -/
theorem natTypeCHornLabel_tetrahedron_of_hornSimplex
    (m : Nat) (hm : 1 ≤ m)
    (f : standardTypeCSource m ⟶ natDoubleDeloopingScaledDuskin)
    (a b c d : Fin (m + 4))
    (hab : a ≤ b) (hbc : b ≤ c) (hcd : c ≤ d)
    (x : (Λ[m + 3, (0 : Fin (m + 4))] : SSet).obj (op ⦋3⦌))
    (hx : x.val = natOrderedTetrahedron a b c d hab hbc hcd) :
    NatTetrahedronEquation
      (natTypeCHornLabel m hm f a b c hab hbc)
      (natTypeCHornLabel m hm f a b d hab (hbc.trans hcd))
      (natTypeCHornLabel m hm f a c d (hab.trans hbc) hcd)
      (natTypeCHornLabel m hm f b c d hbc hcd) := by
  let sigma : DuskinSimplex NatDoubleDelooping 3 :=
    (natTypeCHornMap m f).app (op ⦋3⦌) x
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
  have h012 := natTypeCHornMap_mapComp_eq_label m hm f x e01 e12
  have h023 :=
    natTypeCHornMap_mapComp_eq_label m hm f x (e01 ≫ e12) e23
  have h123 := natTypeCHornMap_mapComp_eq_label m hm f x e12 e23
  have h013 :=
    natTypeCHornMap_mapComp_eq_label m hm f x e01 (e12 ≫ e23)
  rw [h012, h023, h123, h013] at hcoc
  have hx0 : x.val (0 : Fin 4) = a := by rw [hx]; rfl
  have hx1 : x.val (1 : Fin 4) = b := by rw [hx]; rfl
  have hx2 : x.val (2 : Fin 4) = c := by rw [hx]; rfl
  have hx3 : x.val (3 : Fin 4) = d := by rw [hx]; rfl
  rw [hx0, hx1, hx2, hx3] at hcoc
  simpa [NatTetrahedronEquation, sigma, e01, e12, e23] using hcoc

/-! ## Dimension four: four visible equations imply the outer fifth -/

/-- The ten visible labels in the dimension-four type-(C) outer horn. -/
def natTypeCFourLabels
    (f : standardTypeCSource 1 ⟶ natDoubleDeloopingScaledDuskin) :
    NatFourSimplexTriangleLabels where
  a012 := natTypeCHornLabel 1 (by decide) f
    (0 : Fin 5) 1 2 (by decide) (by decide)
  a013 := natTypeCHornLabel 1 (by decide) f
    (0 : Fin 5) 1 3 (by decide) (by decide)
  a014 := natTypeCHornLabel 1 (by decide) f
    (0 : Fin 5) 1 4 (by decide) (by decide)
  a023 := natTypeCHornLabel 1 (by decide) f
    (0 : Fin 5) 2 3 (by decide) (by decide)
  a024 := natTypeCHornLabel 1 (by decide) f
    (0 : Fin 5) 2 4 (by decide) (by decide)
  a034 := natTypeCHornLabel 1 (by decide) f
    (0 : Fin 5) 3 4 (by decide) (by decide)
  a123 := natTypeCHornLabel 1 (by decide) f
    (1 : Fin 5) 2 3 (by decide) (by decide)
  a124 := natTypeCHornLabel 1 (by decide) f
    (1 : Fin 5) 2 4 (by decide) (by decide)
  a134 := natTypeCHornLabel 1 (by decide) f
    (1 : Fin 5) 3 4 (by decide) (by decide)
  a234 := natTypeCHornLabel 1 (by decide) f
    (2 : Fin 5) 3 4 (by decide) (by decide)

/-- Visible face `1` gives equation `0234`. -/
theorem natTypeCFour_face1_eq0234
    (f : standardTypeCSource 1 ⟶ natDoubleDeloopingScaledDuskin) :
    (natTypeCFourLabels f).eq0234 := by
  have h := natTypeCHornLabel_tetrahedron_of_hornSimplex
    1 (by decide) f
    (0 : Fin 5) 2 3 4 (by decide) (by decide) (by decide)
    (SSet.horn.face (0 : Fin 5) (1 : Fin 5) (by decide))
    (natTypeAFour_face1_val (0 : Fin 5) (by decide))
  simpa [natTypeCFourLabels, NatFourSimplexTriangleLabels.eq0234] using h

/-- Visible face `2` gives equation `0134`. -/
theorem natTypeCFour_face2_eq0134
    (f : standardTypeCSource 1 ⟶ natDoubleDeloopingScaledDuskin) :
    (natTypeCFourLabels f).eq0134 := by
  have h := natTypeCHornLabel_tetrahedron_of_hornSimplex
    1 (by decide) f
    (0 : Fin 5) 1 3 4 (by decide) (by decide) (by decide)
    (SSet.horn.face (0 : Fin 5) (2 : Fin 5) (by decide))
    (natTypeAFour_face2_val (0 : Fin 5) (by decide))
  simpa [natTypeCFourLabels, NatFourSimplexTriangleLabels.eq0134] using h

/-- Visible face `3` gives equation `0124`. -/
theorem natTypeCFour_face3_eq0124
    (f : standardTypeCSource 1 ⟶ natDoubleDeloopingScaledDuskin) :
    (natTypeCFourLabels f).eq0124 := by
  have h := natTypeCHornLabel_tetrahedron_of_hornSimplex
    1 (by decide) f
    (0 : Fin 5) 1 2 4 (by decide) (by decide) (by decide)
    (SSet.horn.face (0 : Fin 5) (3 : Fin 5) (by decide))
    (natTypeAFour_face3_val (0 : Fin 5) (by decide))
  simpa [natTypeCFourLabels, NatFourSimplexTriangleLabels.eq0124] using h

/-- Visible face `4` gives equation `0123`. -/
theorem natTypeCFour_face4_eq0123
    (f : standardTypeCSource 1 ⟶ natDoubleDeloopingScaledDuskin) :
    (natTypeCFourLabels f).eq0123 := by
  have h := natTypeCHornLabel_tetrahedron_of_hornSimplex
    1 (by decide) f
    (0 : Fin 5) 1 2 3 (by decide) (by decide) (by decide)
    (SSet.horn.face (0 : Fin 5) (4 : Fin 5) (by decide))
    (natTypeAFour_face4_val (0 : Fin 5) (by decide))
  simpa [natTypeCFourLabels, NatFourSimplexTriangleLabels.eq0123] using h

/-- All five dimension-four equations, including the missing outer face. -/
theorem natTypeCFourLabels_all_equations
    (f : standardTypeCSource 1 ⟶ natDoubleDeloopingScaledDuskin) :
    (natTypeCFourLabels f).eq0123 ∧
      (natTypeCFourLabels f).eq0124 ∧
      (natTypeCFourLabels f).eq0134 ∧
      (natTypeCFourLabels f).eq0234 ∧
      (natTypeCFourLabels f).eq1234 := by
  have h0123 := natTypeCFour_face4_eq0123 f
  have h0124 := natTypeCFour_face3_eq0124 f
  have h0134 := natTypeCFour_face2_eq0134 f
  have h0234 := natTypeCFour_face1_eq0234 f
  have h1234 := natFour_typeC_missing_outer_face
    (natTypeCFourLabels f) h0123 h0124 h0134 h0234
  exact ⟨h0123, h0124, h0134, h0234, h1234⟩

/-- The ten visible dimension-four labels form a normalized cocycle. -/
def natTypeCFourCocycle
    (f : standardTypeCSource 1 ⟶ natDoubleDeloopingScaledDuskin) :
    NatNormalizedDuskinCocycle 4 where
  label := natTypeCHornLabel 1 (by decide) f
  left_normalized := by
    intro a b hab
    exact natTypeCHornLabel_left_zero 1 (by decide) f a b hab
  right_normalized := by
    intro a b hab
    exact natTypeCHornLabel_right_zero 1 (by decide) f a b hab
  tetrahedron := by
    intro a b c d hab hbc hcd
    rcases natTypeCFourLabels_all_equations f with
      ⟨h0123, h0124, h0134, h0234, h1234⟩
    by_cases habEq : a = b
    · subst b
      rw [natTypeCHornLabel_left_zero 1 (by decide) f a c hbc,
          natTypeCHornLabel_left_zero 1 (by decide) f a d
            (hbc.trans hcd)]
      simp
    · by_cases hbcEq : b = c
      · subst c
        rw [natTypeCHornLabel_right_zero 1 (by decide) f a b hab,
            natTypeCHornLabel_left_zero 1 (by decide) f b d hcd]
        simp
      · by_cases hcdEq : c = d
        · subst d
          rw [natTypeCHornLabel_right_zero 1 (by decide) f a c
                (hab.trans hbc),
              natTypeCHornLabel_right_zero 1 (by decide) f b c hbc]
          simp
        · have habVal : a.val < b.val := by
            have hne : a.val ≠ b.val := by
              intro h
              exact habEq (Fin.ext h)
            omega
          have hbcVal : b.val < c.val := by
            have hne : b.val ≠ c.val := by
              intro h
              exact hbcEq (Fin.ext h)
            omega
          have hcdVal : c.val < d.val := by
            have hne : c.val ≠ d.val := by
              intro h
              exact hcdEq (Fin.ext h)
            omega
          have haBound := a.isLt
          have hbBound := b.isLt
          have hcBound := c.isLt
          have hdBound := d.isLt
          have hcases :
              (a.val = 0 ∧ b.val = 1 ∧ c.val = 2 ∧ d.val = 3) ∨
              (a.val = 0 ∧ b.val = 1 ∧ c.val = 2 ∧ d.val = 4) ∨
              (a.val = 0 ∧ b.val = 1 ∧ c.val = 3 ∧ d.val = 4) ∨
              (a.val = 0 ∧ b.val = 2 ∧ c.val = 3 ∧ d.val = 4) ∨
              (a.val = 1 ∧ b.val = 2 ∧ c.val = 3 ∧ d.val = 4) := by
            omega
          rcases hcases with h | h | h | h | h
          · rcases h with ⟨ha, hb, hc, hd⟩
            have ha' : a = (0 : Fin 5) := by apply Fin.ext; omega
            have hb' : b = (1 : Fin 5) := by apply Fin.ext; omega
            have hc' : c = (2 : Fin 5) := by apply Fin.ext; omega
            have hd' : d = (3 : Fin 5) := by apply Fin.ext; omega
            subst a; subst b; subst c; subst d
            simpa [natTypeCFourLabels,
              NatFourSimplexTriangleLabels.eq0123,
              NatTetrahedronEquation] using h0123
          · rcases h with ⟨ha, hb, hc, hd⟩
            have ha' : a = (0 : Fin 5) := by apply Fin.ext; omega
            have hb' : b = (1 : Fin 5) := by apply Fin.ext; omega
            have hc' : c = (2 : Fin 5) := by apply Fin.ext; omega
            have hd' : d = (4 : Fin 5) := by apply Fin.ext; omega
            subst a; subst b; subst c; subst d
            simpa [natTypeCFourLabels,
              NatFourSimplexTriangleLabels.eq0124,
              NatTetrahedronEquation] using h0124
          · rcases h with ⟨ha, hb, hc, hd⟩
            have ha' : a = (0 : Fin 5) := by apply Fin.ext; omega
            have hb' : b = (1 : Fin 5) := by apply Fin.ext; omega
            have hc' : c = (3 : Fin 5) := by apply Fin.ext; omega
            have hd' : d = (4 : Fin 5) := by apply Fin.ext; omega
            subst a; subst b; subst c; subst d
            simpa [natTypeCFourLabels,
              NatFourSimplexTriangleLabels.eq0134,
              NatTetrahedronEquation] using h0134
          · rcases h with ⟨ha, hb, hc, hd⟩
            have ha' : a = (0 : Fin 5) := by apply Fin.ext; omega
            have hb' : b = (2 : Fin 5) := by apply Fin.ext; omega
            have hc' : c = (3 : Fin 5) := by apply Fin.ext; omega
            have hd' : d = (4 : Fin 5) := by apply Fin.ext; omega
            subst a; subst b; subst c; subst d
            simpa [natTypeCFourLabels,
              NatFourSimplexTriangleLabels.eq0234,
              NatTetrahedronEquation] using h0234
          · rcases h with ⟨ha, hb, hc, hd⟩
            have ha' : a = (1 : Fin 5) := by apply Fin.ext; omega
            have hb' : b = (2 : Fin 5) := by apply Fin.ext; omega
            have hc' : c = (3 : Fin 5) := by apply Fin.ext; omega
            have hd' : d = (4 : Fin 5) := by apply Fin.ext; omega
            subst a; subst b; subst c; subst d
            simpa [natTypeCFourLabels,
              NatFourSimplexTriangleLabels.eq1234,
              NatTetrahedronEquation] using h1234

/-- The dimension-four realized cocycle restricts to the outer horn. -/
theorem natTypeCFourCocycle_restrict
    (f : standardTypeCSource 1 ⟶ natDoubleDeloopingScaledDuskin) :
    (Λ[4, (0 : Fin 5)].ι :
      (Λ[4, (0 : Fin 5)] : SSet) ⟶ (Δ[4] : SSet)) ≫
        (natTypeCFourCocycle f).toSimplexMap = natTypeCHornMap 1 f := by
  ext Δ x
  rcases Δ with ⟨⟨q⟩⟩
  apply natDuskinSimplex_eq_of_mapComp_eq
  intro a b c p r
  change
    ((natTypeCFourCocycle f).toSimplexMap.app
      (op ⦋q⦌) x.val).mapComp p r =
      ((natTypeCHornMap 1 f).app (op ⦋q⦌) x).mapComp p r
  rw [NatNormalizedDuskinCocycle.toSimplexMap_mapComp]
  exact (natTypeCHornMap_mapComp_eq_label
    1 (by decide) f x p r).symm

/-- Literal dimension-four type-(C) cocycle completion. -/
theorem natTypeCFour_cocycle_completion
    (f : standardTypeCSource 1 ⟶ natDoubleDeloopingScaledDuskin) :
    Nonempty (NatTypeCSourceCocycleCompletion 1 f) := by
  refine ⟨{
    cocycle := natTypeCFourCocycle f
    restrict := natTypeCFourCocycle_restrict f
    distinguished_zero := ?_ }⟩
  exact natTypeCHornLabel_distinguished_zero 1 (by decide) f

/-! ## Dimensions at least five: every tetrahedron is visible -/

/-- Every ordered tetrahedron is an outer-horn simplex for `m ≥ 2`. -/
def natTypeCHornTetrahedron
    (m : Nat) (hm : 2 ≤ m)
    (a b c d : Fin (m + 4))
    (hab : a ≤ b) (hbc : b ≤ c) (hcd : c ≤ d) :
    (Λ[m + 3, (0 : Fin (m + 4))] : SSet).obj (op ⦋3⦌) :=
  ⟨natOrderedTetrahedron a b c d hab hbc hcd, by
    rw [typeC_outerHorn_all_three_simplices_of_two_le m hm]
    exact Set.mem_univ _⟩

/-- Every visible tetrahedron in dimension at least five satisfies the cocycle
law on its four triangle labels. -/
theorem natTypeCHornLabel_tetrahedron_of_two_le
    (m : Nat) (hm : 2 ≤ m)
    (f : standardTypeCSource m ⟶ natDoubleDeloopingScaledDuskin)
    (a b c d : Fin (m + 4))
    (hab : a ≤ b) (hbc : b ≤ c) (hcd : c ≤ d) :
    natTypeCHornLabel m (by omega) f a b c hab hbc +
        natTypeCHornLabel m (by omega) f a c d (hab.trans hbc) hcd =
      natTypeCHornLabel m (by omega) f b c d hbc hcd +
        natTypeCHornLabel m (by omega) f a b d hab (hbc.trans hcd) := by
  let x := natTypeCHornTetrahedron m hm a b c d hab hbc hcd
  have h := natTypeCHornLabel_tetrahedron_of_hornSimplex
    m (by omega) f a b c d hab hbc hcd x rfl
  simpa [NatTetrahedronEquation] using h

/-- The visible labels form a normalized cocycle for `m ≥ 2`. -/
def natTypeCHighCocycle
    (m : Nat) (hm : 2 ≤ m)
    (f : standardTypeCSource m ⟶ natDoubleDeloopingScaledDuskin) :
    NatNormalizedDuskinCocycle (m + 3) where
  label := natTypeCHornLabel m (by omega) f
  left_normalized := by
    intro a b hab
    exact natTypeCHornLabel_left_zero m (by omega) f a b hab
  right_normalized := by
    intro a b hab
    exact natTypeCHornLabel_right_zero m (by omega) f a b hab
  tetrahedron := by
    intro a b c d hab hbc hcd
    exact natTypeCHornLabel_tetrahedron_of_two_le
      m hm f a b c d hab hbc hcd

/-- The high-dimensional realized cocycle restricts to the outer horn. -/
theorem natTypeCHighCocycle_restrict
    (m : Nat) (hm : 2 ≤ m)
    (f : standardTypeCSource m ⟶ natDoubleDeloopingScaledDuskin) :
    (Λ[m + 3, (0 : Fin (m + 4))].ι :
      (Λ[m + 3, (0 : Fin (m + 4))] : SSet) ⟶
        (Δ[m + 3] : SSet)) ≫
      (natTypeCHighCocycle m hm f).toSimplexMap = natTypeCHornMap m f := by
  ext Δ x
  rcases Δ with ⟨⟨q⟩⟩
  apply natDuskinSimplex_eq_of_mapComp_eq
  intro a b c p r
  change
    ((natTypeCHighCocycle m hm f).toSimplexMap.app
      (op ⦋q⦌) x.val).mapComp p r =
      ((natTypeCHornMap m f).app (op ⦋q⦌) x).mapComp p r
  rw [NatNormalizedDuskinCocycle.toSimplexMap_mapComp]
  exact (natTypeCHornMap_mapComp_eq_label
    m (by omega) f x p r).symm

/-- Literal high-dimensional type-(C) cocycle completion. -/
theorem natTypeCHigh_cocycle_completion
    (m : Nat) (hm : 2 ≤ m)
    (f : standardTypeCSource m ⟶ natDoubleDeloopingScaledDuskin) :
    Nonempty (NatTypeCSourceCocycleCompletion m f) := by
  refine ⟨{
    cocycle := natTypeCHighCocycle m hm f
    restrict := natTypeCHighCocycle_restrict m hm f
    distinguished_zero := ?_ }⟩
  exact natTypeCHornLabel_distinguished_zero m (by omega) f

/-! ## Assemble every type-(C) dimension -/

/-- Every scaled type-(C) source map admits an exact normalized outer-horn
cocycle completion. -/
theorem natDoubleDelooping_hasAllStandardTypeCSourceCocycleCompletions :
    ∀ (m : Nat)
      (f : standardTypeCSource m ⟶ natDoubleDeloopingScaledDuskin),
      Nonempty (NatTypeCSourceCocycleCompletion m f) := by
  intro m f
  by_cases hm0 : m = 0
  · subst m
    exact natTypeCThree_cocycle_completion f
  · by_cases hm1 : m = 1
    · subst m
      exact natTypeCFour_cocycle_completion f
    · have hm2 : 2 ≤ m := by omega
      exact natTypeCHigh_cocycle_completion m hm2 f

/-!
At this point the type-(C) arithmetic is finished in every dimension.  The
remaining step is purely categorical: realize the completed cocycle on
`Δ[m+3]`, glue it to the source point leg across the collapsed edge using the
native target pushout, and verify the single distinguished target triangle is
thin.  No further cocycle equation or new assumption is required.
-/

end KUOS.DependentOriginationDoubleDeloopingTypeCOuterHornCocycleCompletionV1_105
