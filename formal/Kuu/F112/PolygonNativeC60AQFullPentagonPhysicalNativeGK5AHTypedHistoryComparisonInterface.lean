import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5AGOriginalHistoryComparisonFiber
import Mathlib.Tactic

/-!
F112-P94D3GK5AH — history-sensitive typed comparison interface.

The carrier is the ACTUAL F54-shaped north-C60 doubly Nat-dependent,
two-category Type-valued raw route, together with its verified actual
P92B comparison-existence class.  The agreement proof is stored, not
assumed from a coarse substitute.  The resulting fiber is equivalent
to full raw history rather than to the quotient.

An original F55 (all nine constructors, without any adjoined axiom)
3-cell gives a typed comparison between two potentially DIFFERENT
fiber objects, and has a chosen image in the separate P92B extension.
In particular the real 3-versus-2 north pentagon paths admit that
comparison but remain unequal.  P92B assocNaturality remains an
additional generator and is not promoted to an original F55 cell.

The exact P92B factorization criterion holds for arbitrary set-valued
fiber observations. Any equality-valued interpretation respecting all
original F55 comparison cells is noninjective already on the real
pentagon witness.  A proposed genuine GK5AF whole-NatIso interpretation
is packaged as a CONDITIONAL, fully typed candidate: the two required
path matches are fields, never asserted to hold for a canonical map.
No physical Edge-to-NatIso identification or higher filler is invented.

Append-only / tighten-only / no overwrite. Independent Kuu only;
Qi imports Kuu, never conversely. Same public root107, no Gray.
Pinned Lean v4.30.0-rc2 / mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
No sorry, native_decide, new axioms or protection-PR change.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section
universe uT uI vC uC

/-- Original P92B classes at the SAME actual doubly Nat-dependent
north-C60 F45 pentagon endpoints as GK5AG. -/
abbrev NativeGK5AHNorthP92Classes :=
  NativeF55P92AssocRouteClasses
    (KuuNativeF45Tree.pentagon0
      northNativeF45FirstStage northNativeF45SecondStage
      northNativeF45ThirdStage northNativeF45FourthStage)
    (KuuNativeF45Tree.pentagon3
      northNativeF45FirstStage northNativeF45SecondStage
      northNativeF45ThirdStage northNativeF45FourthStage)

/-- Dependent fiber of an ACTUAL original F54 Type-valued history
over its P92B class. The two independent depth indices, F45 Blocks,
AxisTrace and source/target endpoints are retained by rawHistory. -/
structure NativeGK5AHNorthHistoryFiber where
  rawHistory : NativeGK5AGNorthHistory
  comparisonClass : NativeGK5AHNorthP92Classes
  comparisonAgrees :
    comparisonClass = nativeGK5AGNorthP92Class rawHistory

/-- Canonical full-history lift into the verified P92B fiber. -/
def nativeGK5AHEmbed (route : NativeGK5AGNorthHistory) :
    NativeGK5AHNorthHistoryFiber :=
  ⟨route, nativeGK5AGNorthP92Class route, rfl⟩

theorem nativeGK5AHFiberRoundtrip (fiber : NativeGK5AHNorthHistoryFiber) :
    nativeGK5AHEmbed fiber.rawHistory = fiber := by
  rcases fiber with ⟨route, cls, agreement⟩
  cases agreement
  rfl

/-- The fully history-tagged fiber recovers ALL original dependent
F54 route data. This equivalence is NOT a splitting of P92B itself. -/
def nativeGK5AHNorthHistoryEquiv :
    NativeGK5AGNorthHistory ≃ NativeGK5AHNorthHistoryFiber where
  toFun := nativeGK5AHEmbed
  invFun := fun fiber => fiber.rawHistory
  left_inv := by intro route; rfl
  right_inv := nativeGK5AHFiberRoundtrip

theorem nativeGK5AHEmbed_injective :
    Function.Injective nativeGK5AHEmbed :=
  nativeGK5AHNorthHistoryEquiv.injective

/-- ORIGINAL nine-constructor F55 Type-valued 3-cell between
full-history fiber objects, with their actual typed route indices. -/
abbrev NativeGK5AHOriginalCell
    (x y : NativeGK5AHNorthHistoryFiber) :=
  KuuNativeF45Tree.DepthRotationRoute.PresentedCell
    (.pentagon .north) x.rawHistory y.rawHistory

/-- SELECTED P92B comparison: it may also contain the explicitly
adjoined assocNaturality generator, unlike original F55. -/
abbrev NativeGK5AHP92Cell
    (x y : NativeGK5AHNorthHistoryFiber) :=
  NativeF55P92AssocComparison
    (.pentagon .north) x.rawHistory y.rawHistory

/-- A true original F55 witness and its deliberately chosen P92B
image, with a TYPED proof that the latter is the original embedding.
No equation between the two source histories is required. -/
structure NativeGK5AHOriginalComparison
    (x y : NativeGK5AHNorthHistoryFiber) where
  original : NativeGK5AHOriginalCell x y
  chosen : NativeGK5AHP92Cell x y
  chosen_is_original :
    chosen = NativeF55P92AssocComparison.original original

/-- Every real original F55 3-cell (all NINE source constructors)
has a typed P92B image. The reverse direction is NOT asserted. -/
def nativeGK5AHOriginalComparison_of_cell
    {x y : NativeGK5AHNorthHistoryFiber}
    (cell : NativeGK5AHOriginalCell x y) :
    NativeGK5AHOriginalComparison x y where
  original := cell
  chosen := .original cell
  chosen_is_original := rfl

/-- Comparison forces agreement of P92B classes, but not equality
of the underlying original full-history fiber objects. -/
theorem nativeGK5AHOriginalComparison_classes_equal
    {x y : NativeGK5AHNorthHistoryFiber}
    (w : NativeGK5AHOriginalComparison x y) :
    x.comparisonClass = y.comparisonClass := by
  have hclass :
      nativeGK5AGNorthP92Class x.rawHistory =
        nativeGK5AGNorthP92Class y.rawHistory :=
    nativeF55P92AssocRouteClass_eq_of_cell _ _ w.chosen
  exact x.comparisonAgrees.trans (hclass.trans y.comparisonAgrees.symm)

/-- Real north C60 original pentagon has an F55 higher witness
between the fully dependent three-rotation and two-rotation routes. -/
def nativeGK5AHNorthOriginalComparison :
    NativeGK5AHOriginalComparison
      (nativeGK5AHEmbed northNativeF45PentagonLong)
      (nativeGK5AHEmbed northNativeF45PentagonShort) :=
  nativeGK5AHOriginalComparison_of_cell nativeGK5AGNorthOriginalCell

/-- The actual distinct F54 histories REMAIN distinct in the
history-sensitive comparison fiber. -/
theorem nativeGK5AHNorthFibers_distinct :
    nativeGK5AHEmbed northNativeF45PentagonLong ≠
      nativeGK5AHEmbed northNativeF45PentagonShort := by
  intro heq
  exact nativeGK5AGNorthOriginalHistories_distinct
    (congrArg NativeGK5AHNorthHistoryFiber.rawHistory heq)

/-- This is precisely the difference between higher Type-valued
comparison and 0-truncated equality of history objects. -/
theorem nativeGK5AHNorthTypedCell_withoutEq :
    Nonempty (NativeGK5AHOriginalComparison
      (nativeGK5AHEmbed northNativeF45PentagonLong)
      (nativeGK5AHEmbed northNativeF45PentagonShort)) ∧
    (nativeGK5AHEmbed northNativeF45PentagonLong ≠
      nativeGK5AHEmbed northNativeF45PentagonShort) ∧
    ((nativeGK5AHEmbed northNativeF45PentagonLong).comparisonClass =
      (nativeGK5AHEmbed northNativeF45PentagonShort).comparisonClass) := by
  exact ⟨⟨nativeGK5AHNorthOriginalComparison⟩,
    nativeGK5AHNorthFibers_distinct,
    nativeGK5AHOriginalComparison_classes_equal
      nativeGK5AHNorthOriginalComparison⟩

/-- No putative P92B-class readout can recover all raw-history
fiber objects, even though those objects genuinely exist. -/
theorem nativeGK5AHNorthNoP92FiberRetraction :
    ¬ ∃ recover : NativeGK5AHNorthP92Classes →
        NativeGK5AHNorthHistoryFiber,
      ∀ route : NativeGK5AGNorthHistory,
        recover (nativeGK5AGNorthP92Class route) =
          nativeGK5AHEmbed route := by
  rintro ⟨recover, hreturn⟩
  have heq :
      nativeGK5AHEmbed northNativeF45PentagonLong =
        nativeGK5AHEmbed northNativeF45PentagonShort := by
    exact (hreturn _).symm.trans
      ((congrArg recover nativeGK5AGNorthP92Classes_equal).trans
        (hreturn _))
  exact nativeGK5AHNorthFibers_distinct heq

/-- Exact descent criterion for ANY 0-truncated readout of the
history-sensitive fiber, using the actual P92B Type-valued relation.
No original F55 or P92B comparison is silently strengthened. -/
theorem nativeGK5AHNorthFiberFactor_iff
    {T : Type uT} (readout : NativeGK5AHNorthHistoryFiber → T) :
    (∃ qReadout : NativeGK5AHNorthP92Classes → T,
      ∀ x : NativeGK5AHNorthHistoryFiber,
        qReadout x.comparisonClass = readout x) ↔
    (∀ x y : NativeGK5AHNorthHistoryFiber,
      Nonempty (NativeGK5AHP92Cell x y) →
        readout x = readout y) := by
  constructor
  · rintro ⟨qReadout, hq⟩ x y hcell
    rcases hcell with ⟨cell⟩
    have hclasses : x.comparisonClass = y.comparisonClass := by
      have hraw :
          nativeGK5AGNorthP92Class x.rawHistory =
            nativeGK5AGNorthP92Class y.rawHistory :=
        nativeF55P92AssocRouteClass_eq_of_cell _ _ cell
      exact x.comparisonAgrees.trans
        (hraw.trans y.comparisonAgrees.symm)
    calc
      readout x = qReadout x.comparisonClass := (hq x).symm
      _ = qReadout y.comparisonClass := congrArg qReadout hclasses
      _ = readout y := hq y
  · intro hcompat
    have hsource :
        ∀ r s : NativeGK5AGNorthHistory,
          Nonempty (NativeF55P92AssocComparison (.pentagon .north) r s) →
            readout (nativeGK5AHEmbed r) =
              readout (nativeGK5AHEmbed s) := by
      intro r s cell
      exact hcompat (nativeGK5AHEmbed r) (nativeGK5AHEmbed s) cell
    obtain ⟨qReadout, hq⟩ :=
      (nativeGK5AGNorthFactor_throughP92_iff
        (fun route => readout (nativeGK5AHEmbed route))).2 hsource
    refine ⟨qReadout, ?_⟩
    intro x
    calc
      qReadout x.comparisonClass =
          qReadout (nativeGK5AGNorthP92Class x.rawHistory) :=
        congrArg qReadout x.comparisonAgrees
      _ = readout (nativeGK5AHEmbed x.rawHistory) := hq x.rawHistory
      _ = readout x := congrArg readout (nativeGK5AHFiberRoundtrip x)

/-- Any equality-valued interpretation that sends ALL ORIGINAL
F55 3-cells to equality loses faithfulness already on the true
north pentagon. A higher, proof-relevant interpretation is needed
if both original cells and distinct histories must survive. -/
theorem nativeGK5AHOriginalEqPolicy_not_injective
    {T : Type uT} (interpret : NativeGK5AHNorthHistoryFiber → T)
    (respectsOriginal : ∀ x y : NativeGK5AHNorthHistoryFiber,
      NativeGK5AHOriginalCell x y → interpret x = interpret y) :
    ¬ Function.Injective interpret := by
  intro hinj
  apply nativeGK5AHNorthFibers_distinct
  apply hinj
  exact respectsOriginal _ _ nativeGK5AGNorthOriginalCell

/-- The stronger chosen P92B equality policy is necessarily
nonfaithful too; its extra assocNaturality is not old F55. -/
theorem nativeGK5AHP92EqPolicy_not_injective
    {T : Type uT} (interpret : NativeGK5AHNorthHistoryFiber → T)
    (respectsP92 : ∀ x y : NativeGK5AHNorthHistoryFiber,
      NativeGK5AHP92Cell x y → interpret x = interpret y) :
    ¬ Function.Injective interpret := by
  apply nativeGK5AHOriginalEqPolicy_not_injective interpret
  intro x y cell
  exact respectsP92 x y (.original cell)

section GenuineWholeNatIso
variable {I : Type uI} {C D E F G : I → Cat.{vC,uC}}
variable (e₁ : ∀ i : I, C i ≌ D i)
variable (e₂ : ∀ i : I, D i ≌ E i)
variable (e₃ : ∀ i : I, E i ≌ F i)
variable (e₄ : ∀ i : I, F i ≌ G i)
variable {i j : I} (R : C i ⥤ C j)

/-- Actual GK5AF whole NatIso carrier, NOT a physical C60 Edge. -/
abbrev NativeGK5AHWholeCarrier :=
  nativeGK5GChangeAtom
    (nativeGK5XBracket0 e₁ e₂ e₃ e₄) R ≅
  nativeGK5GChangeAtom
    (nativeGK5XBracket3 e₁ e₂ e₃ e₄) R

/-- Explicit CONDITIONS required of a proposed full-history to
Mathlib whole-NatIso interpretation; no canonical map is postulated.
The source F54 witness, F55 witness and chosen P92B witness remain
available as independently typed data above. -/
structure NativeGK5AHWholeCandidate where
  interpret :
    NativeGK5AHNorthHistoryFiber →
      NativeGK5AHWholeCarrier e₁ e₂ e₃ e₄ R
  longMatches :
    interpret (nativeGK5AHEmbed northNativeF45PentagonLong) =
      nativeGK5AFLongPath e₁ e₂ e₃ e₄ R
  shortMatches :
    interpret (nativeGK5AHEmbed northNativeF45PentagonShort) =
      nativeGK5AFShortPath e₁ e₂ e₃ e₄ R

/-- Any candidate satisfying the actual two whole pentagon path
matches necessarily loses full original F54 history injectivity. -/
theorem nativeGK5AHWholeCandidate_not_injective
    (candidate : NativeGK5AHWholeCandidate e₁ e₂ e₃ e₄ R) :
    ¬ Function.Injective candidate.interpret := by
  intro hinj
  apply nativeGK5AHNorthFibers_distinct
  apply hinj
  calc
    candidate.interpret (nativeGK5AHEmbed northNativeF45PentagonLong) =
        nativeGK5AFLongPath e₁ e₂ e₃ e₄ R := candidate.longMatches
    _ = nativeGK5AFShortPath e₁ e₂ e₃ e₄ R :=
      nativeGK5AFPaths_whole e₁ e₂ e₃ e₄ R
    _ = candidate.interpret (nativeGK5AHEmbed northNativeF45PentagonShort) :=
      candidate.shortMatches.symm

/-- Even joint P92B and whole-NatIso readout remains nonfaithful.
In contrast, the fully typed history fiber itself is recoverable. -/
theorem nativeGK5AHWholeCandidate_joint_not_injective
    (candidate : NativeGK5AHWholeCandidate e₁ e₂ e₃ e₄ R) :
    ¬ Function.Injective
      (fun x : NativeGK5AHNorthHistoryFiber =>
        (x.comparisonClass, candidate.interpret x)) := by
  intro hinj
  apply nativeGK5AHNorthFibers_distinct
  apply hinj
  apply Prod.ext
  · exact nativeGK5AHOriginalComparison_classes_equal
      nativeGK5AHNorthOriginalComparison
  · calc
      candidate.interpret (nativeGK5AHEmbed northNativeF45PentagonLong) =
          nativeGK5AFLongPath e₁ e₂ e₃ e₄ R := candidate.longMatches
      _ = nativeGK5AFShortPath e₁ e₂ e₃ e₄ R :=
        nativeGK5AFPaths_whole e₁ e₂ e₃ e₄ R
      _ = candidate.interpret (nativeGK5AHEmbed northNativeF45PentagonShort) :=
        candidate.shortMatches.symm

/-- The EXISTENCE and exact criterion for descent of a proposed
whole interpretation follow from ACTUAL chosen P92B comparisons,
including its explicit extras; these are not F55 theorems. -/
theorem nativeGK5AHWholeCandidate_descent_iff
    (candidate : NativeGK5AHWholeCandidate e₁ e₂ e₃ e₄ R) :
    (∃ q : NativeGK5AHNorthP92Classes →
        NativeGK5AHWholeCarrier e₁ e₂ e₃ e₄ R,
      ∀ x : NativeGK5AHNorthHistoryFiber,
        q x.comparisonClass = candidate.interpret x) ↔
    (∀ x y : NativeGK5AHNorthHistoryFiber,
      Nonempty (NativeGK5AHP92Cell x y) →
        candidate.interpret x = candidate.interpret y) :=
  nativeGK5AHNorthFiberFactor_iff candidate.interpret

#print axioms nativeGK5AHWholeCandidate_not_injective
#print axioms nativeGK5AHWholeCandidate_joint_not_injective
#print axioms nativeGK5AHWholeCandidate_descent_iff
end GenuineWholeNatIso

#print axioms nativeGK5AHNorthHistoryEquiv
#print axioms nativeGK5AHOriginalComparison_of_cell
#print axioms nativeGK5AHNorthTypedCell_withoutEq
#print axioms nativeGK5AHNorthNoP92FiberRetraction
#print axioms nativeGK5AHNorthFiberFactor_iff
#print axioms nativeGK5AHOriginalEqPolicy_not_injective
#print axioms nativeGK5AHP92EqPolicy_not_injective

end
end Kuu.F112.Physical
