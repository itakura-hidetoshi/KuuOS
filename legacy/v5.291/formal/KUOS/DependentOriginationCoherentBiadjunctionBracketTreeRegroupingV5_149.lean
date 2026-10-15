import KUOS.DependentOriginationCoherentBiadjunctionArbitraryBracketTreeV5_149

namespace KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionExchangeQuotientConcatenationV5_141.Grid

set_option autoImplicit false
noncomputable section

/-!
# F52-B / v5.149 — arbitrary re-segmentation and genuine functoriality

The F51 finite snoc chain is one left-associated presentation of
a finite sequence of real ORIGINAL F45 primitive-refinement stages.
The F52-A full binary tree is a different and strictly more general
bracket-sensitive presentation of the SAME original staged process.

We recover F51 by a TYPE-VALUED construction of a left-associated
binary tree with precisely the same per-stage original F45 order,
intermediate independent F19/F28 Blocks, and exact n/m depths.
The two interpretations are equal IN THE GENUINE F44 exchange quotient,
rather than only after evaluating categorical Hom composites.

A full binary tree is also transported stage-by-stage through any
independent pair of honest original-category functors. The resulting
map commutes with both original Type-level history projection and
the actual generated exchange-quotient interpretation.
-/

universe uD vD uE vE uD' vD' uE' vE'
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

/-- Embed the ACTUAL F51 finite original F45 snoc-stage carrier into
the full F52 binary-tree carrier, without changing any original stage,
F19/F28 intermediate Blocks, primitive step, depth, or order choice. -/
def OriginalF45Stages.toBracketTree
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (stages : OriginalF45Stages n m ma pa mb pb) :
    OriginalF45BracketTree n m ma pa mb pb := by
  induction stages with
  | refl mods pq =>
      exact OriginalF45BracketTree.refl mods pq
  | snoc stages order hm hc ih =>
      exact OriginalF45BracketTree.node ih
        (OriginalF45BracketTree.leaf order hm hc)

/-- Every genuine F51 original stage-chain execution and its
corresponding F52 binary-tree presentation have precisely the same
complete F19 and F28 native primitive operation histories. -/
theorem OriginalF45Stages.toBracketTree_axisHistories
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (stages : OriginalF45Stages n m ma pa mb pb) :
    stages.toBracketTree.axisHistories = stages.axisHistories := by
  induction stages with
  | refl mods pq =>
      rfl
  | snoc stages order hm hc ih =>
      change
        (AxisTrace.append stages.toBracketTree.axisHistories.1 hm,
         AxisTrace.append stages.toBracketTree.axisHistories.2 hc) =
        (AxisTrace.append stages.axisHistories.1 hm,
         AxisTrace.append stages.axisHistories.2 hc)
      rw [ih]

/-- The F51 and F52 ACTUAL generated F44 exchange-class
interpretations coincide ON THE NOSE. The original finite snoc list
is hence a genuine special case of the full binary-bracketing theory. -/
theorem OriginalF45Stages.toBracketTree_toExchangeClass
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (stages : OriginalF45Stages n m ma pa mb pb) :
    stages.toBracketTree.toExchangeClass = stages.toExchangeClass := by
  apply (ExchangeClass.eq_iff_axisTraces_eq _ _).2
  calc
    stages.toBracketTree.toExchangeClass.axisTraces =
        stages.toBracketTree.axisHistories :=
      OriginalF45BracketTree.toExchangeClass_axisTraces _
    _ = stages.axisHistories :=
      OriginalF45Stages.toBracketTree_axisHistories stages
    _ = stages.toExchangeClass.axisTraces :=
      (OriginalF45Stages.toExchangeClass_axisTraces stages).symm

/-- ANY full F52 binary bracketing of original F45 stages has the
same actual exchange-quotient class as ANY F51 stage chain with
the same TWO complete original Type-valued axis histories.
Different segmentations and parentheses therefore cannot create
new exchange-class data; same-axis histories must still agree. -/
theorem OriginalF45BracketTree.eq_stageChain_of_histories
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (tree : OriginalF45BracketTree n m ma pa mb pb)
    (stages : OriginalF45Stages n m ma pa mb pb)
    (h : tree.axisHistories = stages.axisHistories) :
    tree.toExchangeClass = stages.toExchangeClass := by
  apply (ExchangeClass.eq_iff_axisTraces_eq _ _).2
  calc
    tree.toExchangeClass.axisTraces = tree.axisHistories :=
      OriginalF45BracketTree.toExchangeClass_axisTraces tree
    _ = stages.axisHistories := h
    _ = stages.toExchangeClass.axisTraces :=
      (OriginalF45Stages.toExchangeClass_axisTraces stages).symm

/-- An arbitrary parenthesized binary tree can always be represented
by ONE genuinely ORIGINAL F45 F19-first or F28-first stage at its
full recorded primitive depth. This is a CLASS equality, never
a claim of definitional equality of two differently shaped trees. -/
theorem OriginalF45BracketTree.toExchangeClass_eq_leaf
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (tree : OriginalF45BracketTree n m ma pa mb pb)
    (order : OriginalF45Order) :
    tree.toExchangeClass =
      (OriginalF45BracketTree.leaf order
        tree.axisHistories.1 tree.axisHistories.2).toExchangeClass :=
  OriginalF45BracketTree.toExchangeClass_eq_originalF45 tree order

/-- Reorder the original F19/F28 categories only by applying genuine
INDEPENDENT honest functors to EVERY actual original leaf, preserving
its original F45 order and the full binary parenthesization. -/
def OriginalF45BracketTree.mapBoth
    {D' : Type uD'} [Category.{vD'} D']
    {E' : Type uE'} [Category.{vE'} E']
    (H : D ⥤ D') (K : E ⥤ E')
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (tree : OriginalF45BracketTree n m ma pa mb pb) :
    OriginalF45BracketTree n m
      (KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid.mapBlocks H ma)
      (KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid.mapBlocks K pa)
      (KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid.mapBlocks H mb)
      (KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid.mapBlocks K pb) := by
  induction tree with
  | refl ma pa =>
      exact OriginalF45BracketTree.refl
        (KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid.mapBlocks H ma)
        (KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid.mapBlocks K pa)
  | leaf order hm hc =>
      exact OriginalF45BracketTree.leaf order
        (AxisTrace.mapBlocks H hm) (AxisTrace.mapBlocks K hc)
  | node before after ih₁ ih₂ =>
      exact OriginalF45BracketTree.node ih₁ ih₂

/-- Mapping all genuine original F45 leaves and then computing the
pair of native F19/F28 histories is exactly computing their full
Type-level histories and mapping BOTH complete histories afterward. -/
theorem OriginalF45BracketTree.mapBoth_axisHistories
    {D' : Type uD'} [Category.{vD'} D']
    {E' : Type uE'} [Category.{vE'} E']
    (H : D ⥤ D') (K : E ⥤ E')
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (tree : OriginalF45BracketTree n m ma pa mb pb) :
    (OriginalF45BracketTree.mapBoth H K tree).axisHistories =
      (AxisTrace.mapBlocks H tree.axisHistories.1,
       AxisTrace.mapBlocks K tree.axisHistories.2) := by
  induction tree with
  | refl ma pa =>
      rfl
  | leaf order hm hc =>
      rfl
  | node before after ih₁ ih₂ =>
      change
        (AxisTrace.append
          (OriginalF45BracketTree.mapBoth H K before).axisHistories.1
          (OriginalF45BracketTree.mapBoth H K after).axisHistories.1,
         AxisTrace.append
          (OriginalF45BracketTree.mapBoth H K before).axisHistories.2
          (OriginalF45BracketTree.mapBoth H K after).axisHistories.2) =
        (AxisTrace.mapBlocks H
          (AxisTrace.append before.axisHistories.1 after.axisHistories.1),
         AxisTrace.mapBlocks K
          (AxisTrace.append before.axisHistories.2 after.axisHistories.2))
      rw [ih₁, ih₂, AxisTrace.mapBlocks_append, AxisTrace.mapBlocks_append]

/-- The ACTUAL full binary-parenthesized generated F44 quotient is
natural under any two independent original-category functors. -/
theorem OriginalF45BracketTree.mapBoth_toExchangeClass
    {D' : Type uD'} [Category.{vD'} D']
    {E' : Type uE'} [Category.{vE'} E']
    (H : D ⥤ D') (K : E ⥤ E')
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (tree : OriginalF45BracketTree n m ma pa mb pb) :
    ExchangeClass.mapBoth H K tree.toExchangeClass =
      (OriginalF45BracketTree.mapBoth H K tree).toExchangeClass := by
  apply (ExchangeClass.eq_iff_axisTraces_eq _ _).2
  calc
    (ExchangeClass.mapBoth H K tree.toExchangeClass).axisTraces =
        (AxisTrace.mapBlocks H tree.toExchangeClass.axisTraces.1,
         AxisTrace.mapBlocks K tree.toExchangeClass.axisTraces.2) :=
      ExchangeClass.axisTraces_mapBoth H K _
    _ = (AxisTrace.mapBlocks H tree.axisHistories.1,
         AxisTrace.mapBlocks K tree.axisHistories.2) := by
      rw [OriginalF45BracketTree.toExchangeClass_axisTraces]
    _ = (OriginalF45BracketTree.mapBoth H K tree).axisHistories :=
      (OriginalF45BracketTree.mapBoth_axisHistories H K tree).symm
    _ = (OriginalF45BracketTree.mapBoth H K tree).toExchangeClass.axisTraces :=
      (OriginalF45BracketTree.toExchangeClass_axisTraces _).symm

#print axioms OriginalF45Stages.toBracketTree
#print axioms OriginalF45Stages.toBracketTree_axisHistories
#print axioms OriginalF45Stages.toBracketTree_toExchangeClass
#print axioms OriginalF45BracketTree.eq_stageChain_of_histories
#print axioms OriginalF45BracketTree.toExchangeClass_eq_leaf
#print axioms OriginalF45BracketTree.mapBoth
#print axioms OriginalF45BracketTree.mapBoth_axisHistories
#print axioms OriginalF45BracketTree.mapBoth_toExchangeClass

end
end KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid
