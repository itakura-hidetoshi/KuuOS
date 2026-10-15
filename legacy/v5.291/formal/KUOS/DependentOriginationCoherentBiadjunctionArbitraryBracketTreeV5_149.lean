import KUOS.DependentOriginationCoherentBiadjunctionArbitraryFiniteOriginalF45StagesV5_148

namespace KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionExchangeQuotientConcatenationV5_141.Grid

set_option autoImplicit false
noncomputable section

/-!
# F52-A / v5.149 — FULL arbitrary binary parenthesization of original F45 runs

F51 established a finite snoc-list of ACTUAL old F45 execution stages,
the generated F44 quotient associativity and its genuine units.
This file carries the NEXT distinction: the original finite execution
may have ANY binary bracketing rather than only F51's left-associated
snoc presentation.

The Type-valued tree stores ACTUAL original F45 leaf constructors,
each with its ORIGINAL order choice, F19 and F28 independently typed
primitive histories, every intermediate Blocks carrier, exact two
natural-number depths, and explicit genuine binary composition nodes.
The only quotient is the F44 generated swap quotient itself.

We prove history completeness, reassociation with exact dependent
Nat.add_assoc casts, and genuine left/right units. This does NOT
assert a syntactic equality of differently parenthesized dependent
trees or identify different within-axis primitive histories.
-/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

/-- An arbitrary finite full BINARY TREE of genuinely typed original
F45 execution stages. Unlike a snoc list, its internal composition
nodes retain an arbitrary choice of parentheses. -/
inductive OriginalF45BracketTree :
    ∀ {a b : D} {x y : E}, Nat → Nat →
      Blocks a b → Blocks x y →
      Blocks a b → Blocks x y →
      Type (max (max uD uE) (max vD vE)) where
  | refl {a b : D} {x y : E}
      (ma : Blocks a b) (pa : Blocks x y) :
      OriginalF45BracketTree 0 0 ma pa ma pa
  | leaf {a b : D} {x y : E} {n m : Nat}
      {ma mb : Blocks a b} {pa pb : Blocks x y}
      (order : OriginalF45Order)
      (hm : AxisTrace n ma mb)
      (hc : AxisTrace m pa pb) :
      OriginalF45BracketTree n m ma pa mb pb
  | node {a b : D} {x y : E}
      {n m n' m' : Nat}
      {ma mb mc : Blocks a b} {pa pb pc : Blocks x y}
      (before : OriginalF45BracketTree n m ma pa mb pb)
      (after : OriginalF45BracketTree n' m' mb pb mc pc) :
      OriginalF45BracketTree (n + n') (m + m') ma pa mc pc

/-- Recover both complete original independent primitive-step histories
from ANY binary parenthesization, preserving within-axis order. -/
def OriginalF45BracketTree.axisHistories
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (tree : OriginalF45BracketTree n m ma pa mb pb) :
    AxisTrace n ma mb × AxisTrace m pa pb := by
  induction tree with
  | refl ma pa =>
      exact (AxisTrace.refl ma, AxisTrace.refl pa)
  | leaf order hm hc =>
      exact (hm, hc)
  | node before after ih₁ ih₂ =>
      exact (AxisTrace.append ih₁.1 ih₂.1,
        AxisTrace.append ih₁.2 ih₂.2)

/-- Evaluate the ACTUAL old F45 leaf routes and their arbitrary
binary bracketing in the original F44 generated exchange quotient. -/
def OriginalF45BracketTree.toExchangeClass
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (tree : OriginalF45BracketTree n m ma pa mb pb) :
    ExchangeClass n m ma mb pa pb := by
  induction tree with
  | refl ma pa =>
      exact ExchangeClass.reflClass ma pa
  | leaf order hm hc =>
      exact AxisTrace.originalF45OrderClass order hm hc
  | node before after ih₁ ih₂ =>
      exact ExchangeClass.append ih₁ ih₂

/-- EVERY binary parenthesization preserves both COMPLETE typed
F19/F28 primitive histories under the genuine F44 exchange quotient. -/
theorem OriginalF45BracketTree.toExchangeClass_axisTraces
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (tree : OriginalF45BracketTree n m ma pa mb pb) :
    tree.toExchangeClass.axisTraces = tree.axisHistories := by
  induction tree with
  | refl ma pa =>
      rfl
  | leaf order hm hc =>
      exact AxisTrace.originalF45OrderClass_axisTraces order hm hc
  | node before after ih₁ ih₂ =>
      change
        (ExchangeClass.append before.toExchangeClass
          after.toExchangeClass).axisTraces =
          (AxisTrace.append before.axisHistories.1 after.axisHistories.1,
           AxisTrace.append before.axisHistories.2 after.axisHistories.2)
      rw [ExchangeClass.axisTraces_append, ih₁, ih₂]

/-- F46 completeness is valid for ANY binary bracketing of the
ACTUAL original F45 routes, not just one chosen snoc association. -/
theorem OriginalF45BracketTree.toExchangeClass_eq_pair
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (tree : OriginalF45BracketTree n m ma pa mb pb) :
    tree.toExchangeClass =
      AxisTrace.pairToClass tree.axisHistories := by
  apply (ExchangeClass.eq_iff_axisTraces_eq _ _).2
  simp only [OriginalF45BracketTree.toExchangeClass_axisTraces,
    AxisTrace.pairToClass_axisTraces]

/-- Every binary bracketing of original F45 execution histories
equals ANY selected single original F45 total execution class. -/
theorem OriginalF45BracketTree.toExchangeClass_eq_originalF45
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (tree : OriginalF45BracketTree n m ma pa mb pb)
    (order : OriginalF45Order) :
    tree.toExchangeClass =
      AxisTrace.originalF45OrderClass order
        tree.axisHistories.1 tree.axisHistories.2 := by
  calc
    tree.toExchangeClass = AxisTrace.pairToClass tree.axisHistories :=
      OriginalF45BracketTree.toExchangeClass_eq_pair tree
    _ = AxisTrace.originalF45OrderClass order
          tree.axisHistories.1 tree.axisHistories.2 :=
      (AxisTrace.originalF45OrderClass_eq_pair order _ _).symm

/-- Reindex BOTH independent exact finite depths of a parenthesized
original F45 execution without modifying its underlying constructors. -/
def OriginalF45BracketTree.castDepths
    {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (hn : n = n') (hm : m = m')
    (tree : OriginalF45BracketTree n m ma pa mb pb) :
    OriginalF45BracketTree n' m' ma pa mb pb := by
  cases hn
  cases hm
  exact tree

/-- Transport a bracketed original tree's two exact depths first or
interpret it in F44 and transport the two quotient depths afterward:
the genuine quotient classes agree exactly. -/
theorem OriginalF45BracketTree.castDepths_toExchangeClass
    {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (hn : n = n') (hm : m = m')
    (tree : OriginalF45BracketTree n m ma pa mb pb) :
    (OriginalF45BracketTree.castDepths hn hm tree).toExchangeClass =
      ExchangeClass.castDepths hn hm tree.toExchangeClass := by
  cases hn
  cases hm
  rfl

/-- Core F52 three-subtree coherence: the two actual ORIGINAL
parenthesizations yield the same F44 generated exchange class after
the explicit DOUBLE Nat.add_assoc index transport. Here the three
subtrees may themselves contain arbitrarily many original F45 leaves. -/
theorem OriginalF45BracketTree.reassociate
    {a b : D} {x y : E}
    {n n' n'' m m' m'' : Nat}
    {ma mb mc md : Blocks a b}
    {pa pb pc pd : Blocks x y}
    (first : OriginalF45BracketTree n m ma pa mb pb)
    (second : OriginalF45BracketTree n' m' mb pb mc pc)
    (third : OriginalF45BracketTree n'' m'' mc pc md pd) :
    (OriginalF45BracketTree.castDepths
      (Nat.add_assoc n n' n'') (Nat.add_assoc m m' m'')
      (OriginalF45BracketTree.node
        (OriginalF45BracketTree.node first second) third)).toExchangeClass =
    (OriginalF45BracketTree.node first
      (OriginalF45BracketTree.node second third)).toExchangeClass := by
  calc
    (OriginalF45BracketTree.castDepths
        (Nat.add_assoc n n' n'') (Nat.add_assoc m m' m'')
        (OriginalF45BracketTree.node
          (OriginalF45BracketTree.node first second) third)).toExchangeClass =
      ExchangeClass.castDepths
        (Nat.add_assoc n n' n'') (Nat.add_assoc m m' m'')
        (ExchangeClass.append
          (ExchangeClass.append first.toExchangeClass second.toExchangeClass)
          third.toExchangeClass) :=
      OriginalF45BracketTree.castDepths_toExchangeClass _ _ _
    _ = ExchangeClass.append first.toExchangeClass
          (ExchangeClass.append second.toExchangeClass
            third.toExchangeClass) :=
      ExchangeClass.append_assoc _ _ _
    _ = (OriginalF45BracketTree.node first
          (OriginalF45BracketTree.node second third)).toExchangeClass := rfl

/-- Two parenthesizations with exactly the same original full
Type-valued F19 and F28 histories, rather than only the same counts,
are equal in the ACTUAL F44 generated quotient. This also gives
bracketing invariance for any finite tree height. -/
theorem OriginalF45BracketTree.eq_of_axisHistories_eq
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (first second : OriginalF45BracketTree n m ma pa mb pb)
    (same : first.axisHistories = second.axisHistories) :
    first.toExchangeClass = second.toExchangeClass := by
  apply (ExchangeClass.eq_iff_axisTraces_eq _ _).2
  simpa only [OriginalF45BracketTree.toExchangeClass_axisTraces] using same

#print axioms OriginalF45BracketTree
#print axioms OriginalF45BracketTree.axisHistories
#print axioms OriginalF45BracketTree.toExchangeClass
#print axioms OriginalF45BracketTree.toExchangeClass_axisTraces
#print axioms OriginalF45BracketTree.toExchangeClass_eq_pair
#print axioms OriginalF45BracketTree.toExchangeClass_eq_originalF45
#print axioms OriginalF45BracketTree.castDepths
#print axioms OriginalF45BracketTree.castDepths_toExchangeClass
#print axioms OriginalF45BracketTree.reassociate
#print axioms OriginalF45BracketTree.eq_of_axisHistories_eq

end
end KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid
