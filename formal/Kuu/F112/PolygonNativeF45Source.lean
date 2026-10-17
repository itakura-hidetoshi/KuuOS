import Kuu.F112.NativeAxisTraces

/-!
# F112-E7L / original-shaped two-category F45 source over genuine C60 sectors

The frozen historical F45 source is NOT just two numbers: it carries
independent typed F19 and F28 Blocks/AxisTrace histories, an original
execution-order choice, both intermediate block presentations, and
arbitrary binary bracketing of individually typed stages.

E7I/E7J/E7K reconstruct the strictly independent generic native
category-path/Blocks/OneStep/AxisTrace shapes and real C60 polygon
sector carriers. Here we combine TWO COMPLETELY INDEPENDENT CATEGORIES
D and E into an original-shaped, Type-valued source grammar over
genuine C60 polygon-side witnesses.

The source stores BOTH precisely indexed n/m axis histories at every
leaf. Binary nodes are typeable ONLY when the intermediate original
Blocks agree on EACH axis, with no inferred direct arrow between two
different original C60 Site objects. Every full tree restores the
complete two native histories via proven source concatenation; it
erases to an E7A independently depth-indexed C60 physical bracket
tree, preserving each original sector and both Nat depths.

This is a NEW exact independent source, not an equivalence with the
frozen original F19 StrongTrans.Modification, F28 compression kernel,
historical F45 ordered shuffle or old F54/F55. No forbidden
KUOS.*, Gray, F51 or F77 imports and no new axioms.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
noncomputable section

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

/-- The TWO primitive F45 execution orders remain distinguished
as RAW source constructors, not identified by a commuting quotient. -/
inductive KuuNativeF45Order : Type where
  | firstAxisFirst
  | secondAxisFirst
  deriving DecidableEq

/-- An arbitrary full binary bracketing of C60-sector-anchored
proof-relevant native stages, with independent CATEGORY TYPES,
intermediate F40-shaped Blocks and exact Nat axis depths. -/
inductive KuuNativeF45Tree (p : Polygon) :
    ∀ {a b : D} {x y : E}, Nat → Nat →
      KuuNativeBlocks a b → KuuNativeBlocks x y →
      KuuNativeBlocks a b → KuuNativeBlocks x y →
      Type (max (max uD uE) (max vD vE)) where
  | refl {a b : D} {x y : E}
      (i : PolygonBoundarySector p)
      (ma : KuuNativeBlocks a b)
      (pa : KuuNativeBlocks x y) :
      KuuNativeF45Tree p 0 0 ma pa ma pa
  | leaf {a b : D} {x y : E}
      {n m : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      (i : PolygonBoundarySector p)
      (order : KuuNativeF45Order)
      (firstAxis : KuuNativeAxisTrace n ma mb)
      (secondAxis : KuuNativeAxisTrace m pa pb) :
      KuuNativeF45Tree p n m ma pa mb pb
  | node {a b : D} {x y : E}
      {n n' m m' : Nat}
      {ma mb mc : KuuNativeBlocks a b}
      {pa pb pc : KuuNativeBlocks x y}
      (first : KuuNativeF45Tree p n m ma pa mb pb)
      (second : KuuNativeF45Tree p n' m' mb pb mc pc) :
      KuuNativeF45Tree p (n + n') (m + m') ma pa mc pc

/-- Recover both COMPLETE Type-valued native axis histories from
ANY original-shaped tree, not merely their evaluated categorical
Hom or their two natural-number lengths. -/
def KuuNativeF45Tree.axisHistories
    {p : Polygon} {a b : D} {x y : E} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (tree : KuuNativeF45Tree p n m ma pa mb pb) :
    KuuNativeAxisTrace n ma mb × KuuNativeAxisTrace m pa pb := by
  induction tree with
  | refl i ma pa =>
      exact ⟨.refl ma, .refl pa⟩
  | leaf i order firstAxis secondAxis =>
      exact ⟨firstAxis, secondAxis⟩
  | node first second ihFirst ihSecond =>
      exact ⟨KuuNativeAxisTrace.append ihFirst.1 ihSecond.1,
        KuuNativeAxisTrace.append ihFirst.2 ihSecond.2⟩

/-- The genuine physical C60 sector witnesses survive projection
of the two independently typed native history axes. -/
def KuuNativeF45Tree.erasePhysical
    {p : Polygon} {a b : D} {x y : E} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (tree : KuuNativeF45Tree p n m ma pa mb pb) :
    PolygonDepthTree p n m := by
  induction tree with
  | refl i ma pa =>
      exact polygonDepthLeafAt p i 0 0
  | leaf i order firstAxis secondAxis =>
      exact polygonDepthLeafAt p i _ _
  | node first second ihFirst ihSecond =>
      exact .node ihFirst ihSecond

/-- Each original F45 leaf retains its ACTUAL geometrical C60
sector, including a separately chosen sector for original units. -/
def KuuNativeF45Tree.sectors
    {p : Polygon} {a b : D} {x y : E} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (tree : KuuNativeF45Tree p n m ma pa mb pb) :
    List (PolygonBoundarySector p) := by
  induction tree with
  | refl i ma pa =>
      exact [i]
  | leaf i order firstAxis secondAxis =>
      exact [i]
  | node first second ihFirst ihSecond =>
      exact ihFirst ++ ihSecond

/-- Stronger than grade preservation: the projected physical
C60 bracket preserves the ENTIRE ordered list of source sectors. -/
theorem KuuNativeF45Tree.erasePhysical_leaves
    {p : Polygon} {a b : D} {x y : E} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (tree : KuuNativeF45Tree p n m ma pa mb pb) :
    tree.erasePhysical.leaves = tree.sectors := by
  induction tree with
  | refl i ma pa =>
      rfl
  | leaf i order firstAxis secondAxis =>
      rfl
  | node first second ihFirst ihSecond =>
      change first.erasePhysical.leaves ++ second.erasePhysical.leaves =
        first.sectors ++ second.sectors
      rw [ihFirst, ihSecond]

/-- The TWO fully original-shaped native F19/F28 replacement axis
histories preserve their ordered primitive CATEGORY ARROWS
independently, not merely a coincidental final composite. -/
theorem KuuNativeF45Tree.axis_flatten_preserved
    {p : Polygon} {a b : D} {x y : E} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (tree : KuuNativeF45Tree p n m ma pa mb pb) :
    ma.flatten = mb.flatten ∧ pa.flatten = pb.flatten :=
  ⟨tree.axisHistories.1.flatten_eq, tree.axisHistories.2.flatten_eq⟩

/-- Independent original-shaped native axis categorical composite
invariance is inherited from the actual Type-valued histories, not
postulated by a source-exchange or Gray axiom. -/
theorem KuuNativeF45Tree.axis_composite_preserved
    {p : Polygon} {a b : D} {x y : E} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (tree : KuuNativeF45Tree p n m ma pa mb pb) :
    ma.composite = mb.composite ∧ pa.composite = pb.composite :=
  ⟨tree.axisHistories.1.composite_eq, tree.axisHistories.2.composite_eq⟩

/-- Real physical C60 first axis after ONE explicitly typed native
empty-block insertion, keeping its genuine initial two-block path. -/
def northNativeF45FirstOnce :=
  KuuNativeBlocks.snoc northPentagonNativeDualAxisFrame.firstAxis
    (KuuNativePath.nil (Site.face (.pentagon .north)))

/-- Real second native axis is an INDEPENDENT block presentation,
not identified with the first axis at the raw source. -/
def northNativeF45SecondOnce :=
  KuuNativeBlocks.snoc northPentagonNativeDualAxisFrame.secondAxis
    (KuuNativePath.nil (Site.face (.pentagon .north)))

/-- A second proof-relevant refinement on the same first-axis
native path, keeping the previous result as its exact input. -/
def northNativeF45FirstTwice :=
  KuuNativeBlocks.snoc northNativeF45FirstOnce
    (KuuNativePath.nil (Site.face (.pentagon .north)))

def northNativeF45SecondTwice :=
  KuuNativeBlocks.snoc northNativeF45SecondOnce
    (KuuNativePath.nil (Site.face (.pentagon .north)))

/-- A genuine C60 north pentagon first original-shaped F45 leaf,
with both separate Type-valued native axis histories at depth 1. -/
def northNativeF45FirstStage :
    KuuNativeF45Tree (.pentagon .north) 1 1
      northPentagonNativeDualAxisFrame.firstAxis
      northPentagonNativeDualAxisFrame.secondAxis
      northNativeF45FirstOnce northNativeF45SecondOnce :=
  .leaf (firstFourPolygonSector (.pentagon .north) 0)
    .firstAxisFirst
    (KuuNativeAxisTrace.insertNilOnce _)
    (KuuNativeAxisTrace.insertNilOnce _)

/-- A second composable C60 stage has the EXACT two intermediate
native block presentations reached by the first stage. -/
def northNativeF45SecondStage :
    KuuNativeF45Tree (.pentagon .north) 1 1
      northNativeF45FirstOnce northNativeF45SecondOnce
      northNativeF45FirstTwice northNativeF45SecondTwice :=
  .leaf (firstFourPolygonSector (.pentagon .north) 1)
    .secondAxisFirst
    (KuuNativeAxisTrace.insertNilOnce _)
    (KuuNativeAxisTrace.insertNilOnce _)

/-- ORIGINAL-SHAPED two-stage binary bracketing on TWO actual,
distinct, consecutive C60 north pentagon sectors. Each axis's
intermediate blocks are checked definitionally at the node. -/
def northNativeF45TwoStages :
    KuuNativeF45Tree (.pentagon .north) 2 2
      northPentagonNativeDualAxisFrame.firstAxis
      northPentagonNativeDualAxisFrame.secondAxis
      northNativeF45FirstTwice northNativeF45SecondTwice :=
  .node northNativeF45FirstStage northNativeF45SecondStage

/-- The physical projection of a true two-category ordered source
node is a doubly Nat-indexed E7A tree over its genuine C60 sectors. -/
theorem northNativeF45TwoStages_leaves :
    northNativeF45TwoStages.erasePhysical.leaves =
      [firstFourPolygonSector (.pentagon .north) 0,
       firstFourPolygonSector (.pentagon .north) 1] := by
  rfl

/-- BOTH complete original-shaped native histories preserve
their original ordered categorical arrows independently, even after
the two composable source refinement stages. -/
theorem northNativeF45TwoStages_axis_preserved :
    northPentagonNativeDualAxisFrame.firstAxis.flatten =
      northNativeF45FirstTwice.flatten ∧
    northPentagonNativeDualAxisFrame.secondAxis.flatten =
      northNativeF45SecondTwice.flatten :=
  northNativeF45TwoStages.axis_flatten_preserved

#print axioms KuuNativeF45Tree.axisHistories
#print axioms KuuNativeF45Tree.erasePhysical
#print axioms KuuNativeF45Tree.erasePhysical_leaves
#print axioms KuuNativeF45Tree.axis_flatten_preserved
#print axioms KuuNativeF45Tree.axis_composite_preserved
#print axioms northNativeF45TwoStages
#print axioms northNativeF45TwoStages_leaves
#print axioms northNativeF45TwoStages_axis_preserved
end
end Kuu.F112.Physical
