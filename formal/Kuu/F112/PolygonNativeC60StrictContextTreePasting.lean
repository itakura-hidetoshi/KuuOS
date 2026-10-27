import Kuu.F112.PolygonNativeC60FiniteStrictPrefixAction

/-!
# F112-P94D3DO — genuine finite C60 strict context-tree pasting

DN identifies each chronologically ordered finite AQ context family with
its original single-stage DF strict transport on the COMPLETE true C60
isotropy group, using DM, genuine CN letters, BV 16D proof codes and CY.

DO allows an arbitrary finite binary PASTING TREE of independently
grouped finite AQ context families. Leaves are actual DN iterated strict
equivalences. Every internal node independently composes the two
already constructed equivalences and explicitly transports the dependent
target along the original noncommutative word associator.

We prove by tree induction that this independently constructed action
equals the genuine DF strict transport by the ordered word of the tree.
The tree word equals the chronological flattened family word. Thus any
two pasting trees presenting the same finite family induce equal genuine
strict actions after exact dependent reindexing. Three- and four-block
reassociation, original CN-generator naturality, BW-holonomy naturality,
and path independence of the five-vertex associativity pentagon follow.

These are equalities of ORIGINAL strict automorphism group equivalences,
not merely equalities in the DC parity quotient. In particular they do
not postulate or construct an additional geometric Type-valued 16-cell
filler. Existing original 14D/15D endpoints and 16D witnesses, strict
Kuu versus independent Kuu presentation, all 107 published roots, the
old no-go, and no-Gray policy remain untouched.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uD vD uE vE

/-- Finite binary pasting presentations of original C60 AQ context
families. A leaf itself may contain any finite chronological family. -/
inductive NativeK5DOContextTree where
  | leaf : List (List Bool) → NativeK5DOContextTree
  | paste : NativeK5DOContextTree → NativeK5DOContextTree →
      NativeK5DOContextTree

/-- Chronological flattening of a finite context-pasting tree. -/
def nativeK5DOTreeSteps : NativeK5DOContextTree → List (List Bool)
  | .leaf steps => steps
  | .paste left right =>
      nativeK5DOTreeSteps left ++ nativeK5DOTreeSteps right

/-- The true, ordered noncommutative AQ word of a pasting tree.
Later chronological prefixes occur to the LEFT. -/
def nativeK5DOTreeWord : NativeK5DOContextTree → List Bool
  | .leaf steps => nativeK5DNPrefixWord steps
  | .paste left right =>
      nativeK5DOTreeWord right ++ nativeK5DOTreeWord left

/-- A tree's original prefix word is exactly the accumulated prefix
of its flattened chronological context family. -/
theorem nativeK5DOTreeWord_eq_flat (tree : NativeK5DOContextTree) :
    nativeK5DOTreeWord tree =
      nativeK5DNPrefixWord (nativeK5DOTreeSteps tree) := by
  induction tree with
  | leaf steps =>
      rfl
  | paste left right hl hr =>
      change nativeK5DOTreeWord right ++ nativeK5DOTreeWord left =
        nativeK5DNPrefixWord
          (nativeK5DOTreeSteps left ++ nativeK5DOTreeSteps right)
      rw [nativeK5DNPrefixWord_append, ← hl, ← hr]

/-- Two possibly different binary context presentations with the same
ordered flattened leaves have EXACTLY the same true prefix word. -/
theorem nativeK5DOTreeWord_eq_of_steps_eq
    {left right : NativeK5DOContextTree}
    (h : nativeK5DOTreeSteps left = nativeK5DOTreeSteps right) :
    nativeK5DOTreeWord left = nativeK5DOTreeWord right := by
  calc
    nativeK5DOTreeWord left =
        nativeK5DNPrefixWord (nativeK5DOTreeSteps left) :=
      nativeK5DOTreeWord_eq_flat left
    _ = nativeK5DNPrefixWord (nativeK5DOTreeSteps right) :=
      congrArg nativeK5DNPrefixWord h
    _ = nativeK5DOTreeWord right :=
      (nativeK5DOTreeWord_eq_flat right).symm

section PhysicalStrictTreePasting

variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable {first : KuuNativeF45Tree p n m ma pa mb pb}
variable {last : KuuNativeF45Tree p n' m' ma pa mb pb}
variable {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
variable {f g : NativeF55StructuralComparison p r s}
variable {alpha beta : NativeK5StructuralFourCell p f g}
variable {w z : NativeK5StructuralFiveCell p alpha beta}
variable {u v : NativeK5StructuralSixCell p w z}
variable {h k : NativeK5StructuralSevenCell p u v}
variable {e d : NativeK5StructuralEightCell p h k}
variable {q t : NativeK5StructuralNineCell p e d}
variable {P Q : NativeK5StructuralTenCell p q t}
variable {H K : NativeK5StructuralElevenCell p P Q}
variable {U V : NativeK5StructuralTwelveCell p H K}

/-- Independently recursive true strict transport on an arbitrary
finite context tree. At each internal node the original MulEquiv maps
are composed, with the ACTUAL dependent 15D target reindexed by the
ordered append associator. This is not defined as a one-stage action. -/
def nativeK5DOTreeStrict
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (outer : List Bool) :
    (inner : List Bool) → (tree : NativeK5DOContextTree) →
      nativeK5DBIsotropy W R inner outer ≃*
        nativeK5DBIsotropy W R (nativeK5DOTreeWord tree ++ inner) outer
  | inner, .leaf steps =>
      nativeK5DNIteratedStrict W R outer inner steps
  | inner, .paste left right => by
      let firstMap := nativeK5DOTreeStrict W R outer inner left
      let secondMap := nativeK5DOTreeStrict W R outer
        (nativeK5DOTreeWord left ++ inner) right
      exact (List.append_assoc (nativeK5DOTreeWord right)
        (nativeK5DOTreeWord left) inner).symm ▸
          (firstMap.trans secondMap)

/-- At a leaf the binary-tree action is the original independently
recursive DN strict action, retaining all original CN certificates. -/
theorem nativeK5DOTreeStrict_leaf
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer : List Bool) (steps : List (List Bool)) :
    nativeK5DOTreeStrict W R outer inner
        (.leaf steps) =
      nativeK5DNIteratedStrict W R outer inner steps := rfl

/-- MAIN DO induction: EVERY independently composed finite binary
context-tree action equals the ORIGINAL DF one-stage full-strict
transport, including noncommutative CN words and exact 14D/15D types. -/
theorem nativeK5DOTreeStrict_eq_direct
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer : List Bool) (tree : NativeK5DOContextTree) :
    nativeK5DOTreeStrict W R outer inner tree =
      nativeK5DFInnerPrefixStrictEquiv W R inner outer
        (nativeK5DOTreeWord tree) := by
  induction tree generalizing inner with
  | leaf steps =>
      exact nativeK5DNIteratedStrict_eq_direct W R inner outer steps
  | paste left right hl hr =>
      change
        ((List.append_assoc (nativeK5DOTreeWord right)
            (nativeK5DOTreeWord left) inner).symm ▸
          ((nativeK5DOTreeStrict W R outer inner left).trans
            (nativeK5DOTreeStrict W R outer
              (nativeK5DOTreeWord left ++ inner) right))) =
        nativeK5DFInnerPrefixStrictEquiv W R inner outer
          (nativeK5DOTreeWord right ++ nativeK5DOTreeWord left)
      rw [hl inner, hr (nativeK5DOTreeWord left ++ inner)]
      change nativeK5DLTwoStageStrict W R inner outer
          (nativeK5DOTreeWord left) (nativeK5DOTreeWord right) =
        nativeK5DLOneStageStrict W R inner outer
          (nativeK5DOTreeWord left) (nativeK5DOTreeWord right)
      exact nativeK5DMInnerPrefixStrict_comp W R inner outer
        (nativeK5DOTreeWord left) (nativeK5DOTreeWord right)

/-- Transport of the ORIGINAL DF strict group equivalence along exact
equality of finite AQ words introduces no new 16D data. -/
theorem nativeK5DODirectStrict_word_congr
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer : List Bool)
    {s t : List Bool} (hst : s = t) :
    (hst ▸ nativeK5DFInnerPrefixStrictEquiv W R inner outer s) =
      nativeK5DFInnerPrefixStrictEquiv W R inner outer t := by
  cases hst
  rfl

/-- Genuine strict naturality for ANY two context-tree presentations
having the same complete noncommutative prefix word. Equality holds as
MulEquiv on all ORIGINAL strict automorphisms, not modulo parity. -/
theorem nativeK5DOTreeStrict_word_natural
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer : List Bool)
    {left right : NativeK5DOContextTree}
    (hword : nativeK5DOTreeWord left = nativeK5DOTreeWord right) :
    (hword ▸ nativeK5DOTreeStrict W R outer inner left) =
      nativeK5DOTreeStrict W R outer inner right := by
  rw [nativeK5DOTreeStrict_eq_direct W R inner outer left,
    nativeK5DOTreeStrict_eq_direct W R inner outer right]
  exact nativeK5DODirectStrict_word_congr W R inner outer hword

/-- Arbitrary subdivision, regrouping and reassociation of the SAME
flattened finite chronological AQ family are strictly natural.
Dependent target coercion is EXPLICIT and preserves source/target. -/
theorem nativeK5DOTreeStrict_refinement
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer : List Bool)
    {left right : NativeK5DOContextTree}
    (hsteps : nativeK5DOTreeSteps left = nativeK5DOTreeSteps right) :
    (nativeK5DOTreeWord_eq_of_steps_eq hsteps ▸
      nativeK5DOTreeStrict W R outer inner left) =
      nativeK5DOTreeStrict W R outer inner right :=
  nativeK5DOTreeStrict_word_natural W R inner outer
    (nativeK5DOTreeWord_eq_of_steps_eq hsteps)

/-- Naturality evaluated at an ORIGINAL Type-valued CN 16D generator,
through the proven CY full strict isotropy isomorphism. No new filler
is asserted: the already existing generator certificate is preserved. -/
theorem nativeK5DOTreeStrict_refinement_CN
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer : List Bool)
    {left right : NativeK5DOContextTree}
    (hsteps : nativeK5DOTreeSteps left = nativeK5DOTreeSteps right)
    (j : NativeC60CNForkAlphabet
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
      (nativeK5CKAtomGenerator W R inner)) :
    (nativeK5DOTreeWord_eq_of_steps_eq hsteps ▸
      nativeK5DOTreeStrict W R outer inner left)
        (nativeK5CYPhysicalFreeIsotropy W R inner outer
          (FreeGroup.of j)) =
      nativeK5DOTreeStrict W R outer inner right
        (nativeK5CYPhysicalFreeIsotropy W R inner outer
          (FreeGroup.of j)) := by
  rw [nativeK5DOTreeStrict_refinement W R inner outer hsteps]

/-- The same actual strict naturality preserves full original
noncommutative BW holonomy at its correctly indexed 15D source. -/
theorem nativeK5DOTreeStrict_refinement_BW
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer : List Bool)
    {left right : NativeK5DOContextTree}
    (hsteps : nativeK5DOTreeSteps left = nativeK5DOTreeSteps right)
    (z : nativeK5DBIsotropy W R inner outer) :
    nativeC60COHolonomy (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W) outer
        (nativeK5CHSource W (nativeK5DOTreeWord right ++ inner)
          (nativeK5CKConservativeRefl W R))
        ((nativeK5DOTreeWord_eq_of_steps_eq hsteps ▸
          nativeK5DOTreeStrict W R outer inner left) z) =
      nativeC60COHolonomy (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W) outer
        (nativeK5CHSource W (nativeK5DOTreeWord right ++ inner)
          (nativeK5CKConservativeRefl W R))
        (nativeK5DOTreeStrict W R outer inner right z) := by
  rw [nativeK5DOTreeStrict_refinement W R inner outer hsteps]

/-- Equality transport of genuine strict maps respects sequential
composition of dependent AQ context-word identifications. -/
theorem nativeK5DOWordTransport_trans
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer : List Bool)
    {a b c : List Bool} (hab : a = b) (hbc : b = c)
    (F : nativeK5DBIsotropy W R inner outer ≃*
      nativeK5DBIsotropy W R (a ++ inner) outer) :
    (hbc ▸ (hab ▸ F)) = ((hab.trans hbc) ▸ F) := by
  cases hab
  cases hbc
  rfl

/-- Path independence of the associativity PENTAGON at the level of
original dependent strict group transports: a three-edge path and a
two-edge path between the same five presentations agree exactly.
This is a strict algebraic coherence theorem, NOT a geometric 16-cell. -/
theorem nativeK5DOPentagonStrict_transport
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer : List Bool)
    (t0 t1 t2 t3 t4 : NativeK5DOContextTree)
    (h01 : nativeK5DOTreeWord t0 = nativeK5DOTreeWord t1)
    (h13 : nativeK5DOTreeWord t1 = nativeK5DOTreeWord t3)
    (h34 : nativeK5DOTreeWord t3 = nativeK5DOTreeWord t4)
    (h02 : nativeK5DOTreeWord t0 = nativeK5DOTreeWord t2)
    (h24 : nativeK5DOTreeWord t2 = nativeK5DOTreeWord t4) :
    (h34 ▸ (h13 ▸ (h01 ▸
      nativeK5DOTreeStrict W R outer inner t0))) =
    (h24 ▸ (h02 ▸
      nativeK5DOTreeStrict W R outer inner t0)) := by
  let F := nativeK5DOTreeStrict W R outer inner t0
  have hpaths :
      (h01.trans h13).trans h34 = h02.trans h24 :=
    Subsingleton.elim _ _
  calc
    h34 ▸ (h13 ▸ (h01 ▸ F)) =
      h34 ▸ ((h01.trans h13) ▸ F) := by
        rw [nativeK5DOWordTransport_trans W R inner outer h01 h13 F]
    _ = (((h01.trans h13).trans h34) ▸ F) :=
      nativeK5DOWordTransport_trans W R inner outer
        (h01.trans h13) h34 F
    _ = ((h02.trans h24) ▸ F) := by rw [hpaths]
    _ = (h24 ▸ (h02 ▸ F)) :=
      (nativeK5DOWordTransport_trans W R inner outer h02 h24 F).symm

/-- Left-associated pasting of three arbitrary independent finite
chronological context families. -/
def nativeK5DOTripleLeft
    (a b c : List (List Bool)) : NativeK5DOContextTree :=
  .paste (.paste (.leaf a) (.leaf b)) (.leaf c)

/-- Right-associated pasting of the SAME three actual context families. -/
def nativeK5DOTripleRight
    (a b c : List (List Bool)) : NativeK5DOContextTree :=
  .paste (.leaf a) (.paste (.leaf b) (.leaf c))

theorem nativeK5DOTripleSteps_assoc
    (a b c : List (List Bool)) :
    nativeK5DOTreeSteps (nativeK5DOTripleLeft a b c) =
      nativeK5DOTreeSteps (nativeK5DOTripleRight a b c) := by
  change (a ++ b) ++ c = a ++ (b ++ c)
  exact List.append_assoc a b c

/-- ORIGINAL strict three-block associativity, not merely equality of
DC parity: both genuinely composed Type-indexed MulEquiv routes agree. -/
theorem nativeK5DOTripleStrict_assoc
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer : List Bool) (a b c : List (List Bool)) :
    (nativeK5DOTreeWord_eq_of_steps_eq
      (nativeK5DOTripleSteps_assoc a b c) ▸
      nativeK5DOTreeStrict W R outer inner
        (nativeK5DOTripleLeft a b c)) =
      nativeK5DOTreeStrict W R outer inner
        (nativeK5DOTripleRight a b c) :=
  nativeK5DOTreeStrict_refinement W R inner outer
    (nativeK5DOTripleSteps_assoc a b c)

/-- Leftmost vertex of the four-context Mac Lane reassociation pentagon. -/
def nativeK5DOFourLeft
    (a b c d : List (List Bool)) : NativeK5DOContextTree :=
  .paste (.paste (.paste (.leaf a) (.leaf b)) (.leaf c)) (.leaf d)

/-- Rightmost vertex of the four-context reassociation pentagon. -/
def nativeK5DOFourRight
    (a b c d : List (List Bool)) : NativeK5DOContextTree :=
  .paste (.leaf a) (.paste (.leaf b) (.paste (.leaf c) (.leaf d)))

theorem nativeK5DOFourSteps_assoc
    (a b c d : List (List Bool)) :
    nativeK5DOTreeSteps (nativeK5DOFourLeft a b c d) =
      nativeK5DOTreeSteps (nativeK5DOFourRight a b c d) := by
  change (((a ++ b) ++ c) ++ d) = a ++ (b ++ (c ++ d))
  simp only [List.append_assoc]

/-- Four original noncommutative C60 AQ context families agree across
extreme bracketings by actual typed strict transport equality. -/
theorem nativeK5DOFourStrict_assoc
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer : List Bool) (a b c d : List (List Bool)) :
    (nativeK5DOTreeWord_eq_of_steps_eq
      (nativeK5DOFourSteps_assoc a b c d) ▸
      nativeK5DOTreeStrict W R outer inner
        (nativeK5DOFourLeft a b c d)) =
      nativeK5DOTreeStrict W R outer inner
        (nativeK5DOFourRight a b c d) :=
  nativeK5DOTreeStrict_refinement W R inner outer
    (nativeK5DOFourSteps_assoc a b c d)

end PhysicalStrictTreePasting

#print axioms nativeK5DOTreeWord_eq_flat
#print axioms nativeK5DOTreeWord_eq_of_steps_eq
#print axioms nativeK5DOTreeStrict
#print axioms nativeK5DOTreeStrict_leaf
#print axioms nativeK5DOTreeStrict_eq_direct
#print axioms nativeK5DODirectStrict_word_congr
#print axioms nativeK5DOTreeStrict_word_natural
#print axioms nativeK5DOTreeStrict_refinement
#print axioms nativeK5DOTreeStrict_refinement_CN
#print axioms nativeK5DOTreeStrict_refinement_BW
#print axioms nativeK5DOWordTransport_trans
#print axioms nativeK5DOPentagonStrict_transport
#print axioms nativeK5DOTripleSteps_assoc
#print axioms nativeK5DOTripleStrict_assoc
#print axioms nativeK5DOFourSteps_assoc
#print axioms nativeK5DOFourStrict_assoc

end
end Kuu.F112.Physical
