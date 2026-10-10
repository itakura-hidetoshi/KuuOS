import KUOS.DependentOriginationCoherentBiadjunctionActualLiftRectangularSubdivisionV5_137

namespace KUOS.DependentOriginationCoherentBiadjunctionConstructiveRefinementV5_138

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionFiniteHorizontalExchangeV5_133
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137

set_option autoImplicit false
noncomputable section

/-!
# F41-A/v5.138 — CONSTRUCTIVE refinements of actual F40 finite blocks

Refines is NOT defined to mean equality of composite morphisms.
It is the inductively generated directed refinement relation obtained
from splitting an existing block, adding an empty path block,
preserving a prior refinement under an additional right-hand block,
reflexivity and transitivity. In particular, its generators do not
postulate ANY equality of F19 or F28 morphisms.

A structural proof using the actual category associativity and
right-identity axioms shows that every refinement preserves the
original composed morphism. Arbitrary finite sequences of refinements
therefore preserve the original F38 chosen mate functor as well.

F19's strong-modification presentation and F28's compression-kernel
quotient both instantiate this generic category-valued construction.
F26's comparison-chain carrier is NOT substituted for F28 Hom.
-/

namespace Grid

universe u v uE vE
variable {D : Type u} [Category.{v} D]

/-- The reflexive-transitive DIRECTED block-refinement relation.
A split replaces one native path q.append r by TWO successive
native path blocks q and r. An empty block can be inserted anywhere
by right-congruence. There are no unproved equality premises. -/
inductive Refines : ∀ {x y : D}, Blocks x y → Blocks x y → Prop where
  | refl {x y : D} (p : Blocks x y) : Refines p p
  | trans {x y : D} {p q r : Blocks x y} :
      Refines p q → Refines q r → Refines p r
  | whisker {x y z : D} {p q : Blocks x y}
      (h : Refines p q) (t : Chain.Path y z) :
      Refines (.snoc p t) (.snoc q t)
  | split {w x y z : D}
      (p : Blocks w x) (q : Chain.Path x y) (r : Chain.Path y z) :
      Refines (.snoc p (q.append r)) (.snoc (.snoc p q) r)
  | insertNil {x y : D} (p : Blocks x y) :
      Refines p (.snoc p (Chain.Path.nil y))

/-- THE KEY CONSTRUCTIVE RESULT: every directed refinement preserves the
ACTUAL native category Hom evaluation. No equality of composites is an
assumption or constructor of the refinement relation. -/
theorem Refines.composite_eq {x y : D} {p q : Blocks x y}
    (h : Refines p q) : p.composite = q.composite := by
  induction h with
  | refl _ => rfl
  | trans h₁ h₂ ih₁ ih₂ => exact ih₁.trans ih₂
  | whisker h t ih =>
      simp only [Blocks.composite, ih]
  | split p q r =>
      simp only [Blocks.composite, Chain.Path.composite_append]
      exact (Category.assoc _ _ _).symm
  | insertNil p =>
      simp only [Blocks.composite, Chain.Path.composite, Category.comp_id]

/-- Directed refinements remain valid when any sequence of native
blocks is appended AFTER the refined finite block prefix. -/
theorem Refines.append_right {x y z : D} {p q : Blocks x y}
    (h : Refines p q) (tail : Blocks y z) :
    Refines (p.append tail) (q.append tail) := by
  induction tail with
  | empty => exact h
  | snoc tail r ih =>
      exact Refines.whisker ih r

/-- Directed refinements can occur AFTER an arbitrary already completed
prefix of original category blocks, with the same exact 1-cells. -/
theorem Refines.append_left {x y z : D}
    (prefix : Blocks x y) {p q : Blocks y z}
    (h : Refines p q) :
    Refines (prefix.append p) (prefix.append q) := by
  induction h with
  | refl p =>
      exact Refines.refl _
  | trans h₁ h₂ ih₁ ih₂ =>
      exact Refines.trans ih₁ ih₂
  | whisker h t ih =>
      exact Refines.whisker ih t
  | split p q r =>
      exact Refines.split (prefix.append p) q r
  | insertNil p =>
      exact Refines.insertNil (prefix.append p)

/-- Two independently refined segments may themselves be concatenated;
both components are kept as explicit constructive witnesses. -/
theorem Refines.append_both {x y z : D}
    {p p' : Blocks x y} {q q' : Blocks y z}
    (hp : Refines p p') (hq : Refines q q') :
    Refines (p.append q) (p'.append q') :=
  Refines.trans (Refines.append_right hp q)
    (Refines.append_left p' hq)

/-- Refinement is preserved by ANY genuine functor at the level of the
evaluated morphism, derived from the F40 functoriality equation. -/
theorem Refines.mapBlocks_composite_eq
    {E : Type uE} [Category.{vE} E] (H : D ⥤ E)
    {x y : D} {p q : Blocks x y} (h : Refines p q) :
    (mapBlocks H p).composite = (mapBlocks H q).composite :=
  mapBlocks_independent H p q (Refines.composite_eq h)

/-- An independent refinement certificate is recorded for EACH of two
different CATEGORIES, without identifying F19 and F28 carriers. -/
structure RectangleRefines
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (modsA modsB : Blocks a b) (pqA pqB : Blocks x y) : Prop where
  modifications : Refines modsA modsB
  comparisons : Refines pqA pqB

/-- The two actual categorical morphism equalities follow from
refinement witnesses, with NO independent equality assumptions. -/
theorem RectangleRefines.composites
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    {modsA modsB : Blocks a b} {pqA pqB : Blocks x y}
    (h : RectangleRefines modsA modsB pqA pqB) :
    (modsA.composite = modsB.composite) ∧
      (pqA.composite = pqB.composite) :=
  ⟨Refines.composite_eq h.modifications,
    Refines.composite_eq h.comparisons⟩

/-- Trivial subdivision is a genuine reflexive rectangle refinement. -/
theorem RectangleRefines.refl
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (mods : Blocks a b) (pq : Blocks x y) :
    RectangleRefines mods mods pq pq :=
  ⟨Refines.refl mods, Refines.refl pq⟩

/-- Composing two independent two-axis refinement certificates yields
a constructive third certificate, with genuine transitive generators. -/
theorem RectangleRefines.trans
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    {modsA modsB modsC : Blocks a b}
    {pqA pqB pqC : Blocks x y}
    (h₁ : RectangleRefines modsA modsB pqA pqB)
    (h₂ : RectangleRefines modsB modsC pqB pqC) :
    RectangleRefines modsA modsC pqA pqC :=
  ⟨Refines.trans h₁.modifications h₂.modifications,
    Refines.trans h₁.comparisons h₂.comparisons⟩

#print axioms Refines
#print axioms Refines.composite_eq
#print axioms Refines.append_right
#print axioms Refines.append_left
#print axioms Refines.append_both
#print axioms Refines.mapBlocks_composite_eq
#print axioms RectangleRefines
#print axioms RectangleRefines.composites
#print axioms RectangleRefines.refl
#print axioms RectangleRefines.trans

end Grid

end

end KUOS.DependentOriginationCoherentBiadjunctionConstructiveRefinementV5_138
