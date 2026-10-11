import KUOS.DependentOriginationGrayKernelHexagonIncidenceMultiplicityV5_157

namespace KUOS.DependentOriginationGrayKernelHexagonWeightedDoubleCountV5_157

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationTruncatedIcosahedralHexagonsV3_86
open KUOS.DependentOriginationTruncatedIcosahedralKernelHexagonCyclesV5_157
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayF55PhaseRealizationV5_156
open KUOS.DependentOriginationGrayC60CyclicGlobalPastingV5_156
open KUOS.DependentOriginationGrayC60AllNinetyEdgePastingV5_157
open KUOS.DependentOriginationGrayKernelHexagonSixCellPastingV5_157
open KUOS.DependentOriginationGrayKernelHexagonIncidenceMultiplicityV5_157
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false
noncomputable section

/-!
# F59-F6 / v5.157: UNIVERSAL weighted geometric C60 double counting

F59-F3 constructed all twenty original hexagonal six-edge cyclic
boundaries with kernel-certified endpoint equality, not inherited
compiler-specific trust. F59-F5 proved the *edgewise* incidence law:
every around edge occurs ONCE and every cross edge occurs TWICE in
those twenty hexagon boundary lists.

Here the local-to-global accounting is proved not merely for the
F58 integer generator charge or the F59 independent exchange phase,
but for an ARBITRARY edge-dependent weight valued in ANY additive
commutative monoid. No uniformity or independence of weights is
required. The entire set of actual twenty six-edge hexagon boundary
occurrences is counted with the precise edge multiplicities.

We specialize this geometric identity to the F59-C native graded
Gray 3-cell endomorphisms. This yields a NEW, geometrically grounded
proof that F59-F4's native twenty-hexagon boundary composite equals
the native composite of the ninety distinct edge labels plus an
additional thirty cross-edge labels. The prior F59-F4 proof from the
special (0,6) numerical charges is not used in this new derivation.

The result is geometric incidence double-counting IN THE TARGET.
It does not manufacture the original source F55 composition boundaries
or an external unrestricted Gray 3-functor; the historic Stage-II
obstruction omega is not identified with any new group coordinate.
-/

/-- A direct equivalence between the ACTUAL inductive 90-edge
carrier and the disjoint families of 60 around plus 30 cross edges. -/
def c60NinetyEdgeFamilyEquiv :
    TruncatedIcosahedralEdge ≃
      (TruncatedIcosahedralAroundEdge ⊕ IcosahedralEdge) where
  toFun
    | .around a => Sum.inl a
    | .cross e => Sum.inr e
  invFun
    | .inl a => .around a
    | .inr e => .cross e
  left_inv := by
    intro e
    cases e <;> rfl
  right_inv := by
    intro s
    cases s <;> rfl

/-- Truly generic decomposition of a sum on the 90 original
geometric edges by their actual two distinct constructor families. -/
theorem c60SumOverRealEdgeFamilies
    {A : Type*} [AddCommMonoid A]
    (w : TruncatedIcosahedralEdge → A) :
    (∑ e : TruncatedIcosahedralEdge, w e) =
      (∑ a : TruncatedIcosahedralAroundEdge, w (.around a)) +
        (∑ e : IcosahedralEdge, w (.cross e)) := by
  classical
  calc
    (∑ e : TruncatedIcosahedralEdge, w e) =
        ∑ s : TruncatedIcosahedralAroundEdge ⊕ IcosahedralEdge,
          w (c60NinetyEdgeFamilyEquiv.symm s) := by
            apply Fintype.sum_equiv c60NinetyEdgeFamilyEquiv
            intro e
            cases e <;> rfl
    _ = (∑ a : TruncatedIcosahedralAroundEdge, w (.around a)) +
        (∑ e : IcosahedralEdge, w (.cross e)) := by
          rw [Fintype.sum_sum_type]
          rfl

/-- For EVERY list of genuine C60 edges and EVERY additive
commutative weight, summing the list WITH REPETITIONS is identical
to summing its exact occurrence counts over all 90 physical edges. -/
theorem c60ListWeightedSumByMultiplicity
    {A : Type*} [AddCommMonoid A]
    (w : TruncatedIcosahedralEdge → A)
    (l : List TruncatedIcosahedralEdge) :
    (l.map w).sum =
      ∑ e : TruncatedIcosahedralEdge, (l.count e) • w e := by
  classical
  calc
    (l.map w).sum =
        ∑ e ∈ l.toFinset, (l.count e) • w e :=
          Finset.sum_list_map_count l w
    _ = ∑ e : TruncatedIcosahedralEdge,
          (l.count e) • w e := by
            apply Finset.sum_subset (Finset.subset_univ _)
            intro e _ he
            have hnot : e ∉ l := by
              simpa only [List.mem_toFinset] using he
            simp [List.count_eq_zero_of_not_mem hnot]

/-- UNIVERSAL C60 HEXAGON GEOMETRIC DOUBLE-COUNTING, with a
possibly different arbitrary weight attached to EACH physical edge.
This theorem uses the real twenty original six-edge boundaries
and the actual F59-F5 occurrence function, not their total length. -/
theorem kernelC60HexagonWeightedDoubleCount
    {A : Type*} [AddCommMonoid A]
    (w : TruncatedIcosahedralEdge → A) :
    (∑ f : IcosahedralFace,
      ((kernelC60HexagonBoundaryEdges f).map w).sum) =
      ∑ e : TruncatedIcosahedralEdge,
        kernelC60HexagonEdgeMultiplicity e • w e := by
  classical
  calc
    (∑ f : IcosahedralFace,
      ((kernelC60HexagonBoundaryEdges f).map w).sum) =
        ∑ f : IcosahedralFace,
          ∑ e : TruncatedIcosahedralEdge,
            ((kernelC60HexagonBoundaryEdges f).count e) • w e := by
              apply Finset.sum_congr rfl
              intro f _
              exact c60ListWeightedSumByMultiplicity w _
    _ = ∑ e : TruncatedIcosahedralEdge,
          ∑ f : IcosahedralFace,
            ((kernelC60HexagonBoundaryEdges f).count e) • w e := by
              rw [Finset.sum_comm]
    _ = ∑ e : TruncatedIcosahedralEdge,
          (∑ f : IcosahedralFace,
            (kernelC60HexagonBoundaryEdges f).count e) • w e := by
              apply Finset.sum_congr rfl
              intro e _
              rw [Finset.sum_smul]
    _ = ∑ e : TruncatedIcosahedralEdge,
          kernelC60HexagonEdgeMultiplicity e • w e := rfl

/-- UNIVERSAL weighted 60/30 rule in any additive commutative
monoid; no integer charge or mod2 coefficients are presupposed:
each of the 60 around edges counts ONCE and each of the 30
cross edges counts TWICE in the real 20-hexagon boundary multiset. -/
theorem kernelC60HexagonWeightedDoubleCount_byFamilies
    {A : Type*} [AddCommMonoid A]
    (w : TruncatedIcosahedralEdge → A) :
    (∑ f : IcosahedralFace,
      ((kernelC60HexagonBoundaryEdges f).map w).sum) =
      (∑ a : TruncatedIcosahedralAroundEdge, w (.around a)) +
        (∑ e : IcosahedralEdge, (2 : Nat) • w (.cross e)) := by
  calc
    (∑ f : IcosahedralFace,
      ((kernelC60HexagonBoundaryEdges f).map w).sum) =
        ∑ e : TruncatedIcosahedralEdge,
          kernelC60HexagonEdgeMultiplicity e • w e :=
            kernelC60HexagonWeightedDoubleCount w
    _ = (∑ a : TruncatedIcosahedralAroundEdge,
          w (.around a)) +
        (∑ e : IcosahedralEdge,
          (2 : Nat) • w (.cross e)) := by
          rw [c60SumOverRealEdgeFamilies
            (fun e => kernelC60HexagonEdgeMultiplicity e • w e)]
          apply congrArg₂ (· + ·)
          · apply Finset.sum_congr rfl
            intro a _
            rw [kernelC60AroundEdge_hexagonMultiplicity a]
            simp
          · apply Finset.sum_congr rfl
            intro e _
            rw [kernelC60CrossEdge_hexagonMultiplicity e]

/-- Any possibly edge-dependent REAL native F59 Gray 3-cell labels
obey the identical original C60 geometric double-counting identity.
This is an equality OF HIGHER 3-CELLS, not a numerical projection. -/
theorem kernelC60HexagonAnyNativeGrayLabelsDoubleCount
    (w : TruncatedIcosahedralEdge → GradedThreeCell 0 0) :
    (∑ f : IcosahedralFace,
      ((kernelC60HexagonBoundaryEdges f).map w).sum) =
      (∑ a : TruncatedIcosahedralAroundEdge, w (.around a)) +
        (∑ e : IcosahedralEdge, (2 : Nat) • w (.cross e)) :=
  kernelC60HexagonWeightedDoubleCount_byFamilies w

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

section ActualF55Gray
variable {a b : D} {x y : E}
variable {n₁ n₂ m₁ m₂ : Nat}
variable {p₀ p₁ p₂ : Blocks a b}
variable {q₀ q₁ q₂ : Blocks x y}
variable
  (t₁ : OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁)
  (t₂ : OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂)
variable
  {leftAfter : OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁}
  {rightAfter : OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂}
  (left : OriginalF45BracketTree.LocalRotation t₁ leftAfter)
  (right : OriginalF45BracketTree.LocalRotation t₂ rightAfter)

/-- F59-F4's original native twenty-hexagon F55 square-cell paste
reproved via the NEW edgewise geometric double-counting of F59-F5.
No equality of integer charge or parity is used in this argument:
the actual edge-carrier incidence MULTIPLICITIES establish it. -/
theorem kernelC60F55NativeHexagonPasting_geometricDoubleCount :
    kernelC60AllTwentyHexagonGrayTotal t₁ t₂ left right =
      c60AllNinetyGrayTotal t₁ t₂ left right +
        c60CrossThirtyGrayTotal t₁ t₂ left right := by
  calc
    kernelC60AllTwentyHexagonGrayTotal t₁ t₂ left right =
        ∑ f : IcosahedralFace,
          (kernelC60HexagonGraySixSquareList
            t₁ t₂ left right f).sum := by
              unfold kernelC60AllTwentyHexagonGrayTotal
              apply Finset.sum_congr rfl
              intro f _
              exact kernelC60HexagonGrayPasting_eq_sum
                t₁ t₂ left right f
    _ = ∑ f : IcosahedralFace,
          ((kernelC60HexagonBoundaryEdges f).map
            (c60AllNinetyGrayCell t₁ t₂ left right)).sum := by
              apply Finset.sum_congr rfl
              intro f _
              simp only [kernelC60HexagonGraySixSquareList,
                kernelC60HexagonBoundaryEdges, List.map_map,
                Function.comp_def]
    _ = (∑ a : TruncatedIcosahedralAroundEdge,
          c60AllNinetyGrayCell t₁ t₂ left right (.around a)) +
        (∑ e : IcosahedralEdge,
          (2 : Nat) • c60AllNinetyGrayCell t₁ t₂ left right (.cross e)) :=
            kernelC60HexagonAnyNativeGrayLabelsDoubleCount _
    _ = c60AllNinetyGrayTotal t₁ t₂ left right +
        c60CrossThirtyGrayTotal t₁ t₂ left right := by
          have hcross :
              (∑ e : IcosahedralEdge,
                (2 : Nat) •
                  c60AllNinetyGrayCell t₁ t₂ left right (.cross e)) =
                c60CrossThirtyGrayTotal t₁ t₂ left right +
                  c60CrossThirtyGrayTotal t₁ t₂ left right := by
            simp only [c60AllNinetyGrayCell, c60CrossThirtyGrayTotal,
              two_nsmul, Finset.sum_add_distrib]
          rw [hcross]
          change c60AroundSixtyGrayTotal t₁ t₂ left right +
              (c60CrossThirtyGrayTotal t₁ t₂ left right +
                c60CrossThirtyGrayTotal t₁ t₂ left right) =
            c60AllNinetyGrayTotal t₁ t₂ left right +
              c60CrossThirtyGrayTotal t₁ t₂ left right
          rw [c60AllNinetyGrayTotal_split t₁ t₂ left right]
          abel

#print axioms c60NinetyEdgeFamilyEquiv
#print axioms c60SumOverRealEdgeFamilies
#print axioms c60ListWeightedSumByMultiplicity
#print axioms kernelC60HexagonWeightedDoubleCount
#print axioms kernelC60HexagonWeightedDoubleCount_byFamilies
#print axioms kernelC60HexagonAnyNativeGrayLabelsDoubleCount
#print axioms kernelC60F55NativeHexagonPasting_geometricDoubleCount

end ActualF55Gray
end
end KUOS.DependentOriginationGrayKernelHexagonWeightedDoubleCountV5_157
