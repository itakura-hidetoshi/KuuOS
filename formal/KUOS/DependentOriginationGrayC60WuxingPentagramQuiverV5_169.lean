import KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
import Mathlib.Combinatorics.Quiver.Path
import Mathlib.CategoryTheory.PathCategory.Basic

namespace KUOS.DependentOriginationGrayC60WuxingPentagramQuiverV5_169

open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85

set_option autoImplicit false
noncomputable section

/-!
# F59-F21 / v5.169 — an ACTUAL five-phase quiver carried by each C60 pentagon

Five phases are processes, not chemical substances. We put the traditional
generative order on the five original pentagonal slots:

  wood → fire → earth → metal → water → wood.

The controlling path is TWO generative steps, yielding the pentagram:

  wood → earth → water → fire → metal → wood.

The resulting TEN directed arrows form a 5-vertex regular tournament:
every pair of distinct phases has exactly one directed relation. Its
underlying undirected graph is K5, NOT just the original boundary C5.

A genuine mathlib Quiver instance retains both kinds of proof-relevant,
TYPED arrows. Its two 5-arrow cycles are actual Quiver.Path objects and
hence map into mathlib's free Paths category.

This is the ORIGINAL abstract cyclic quiver, not a monad, comonad,
trace or *-autonomous category. Feedback dynamics and the physical
embedding into original C60 are separately constructed below. No
traditional philosophical correspondence is postulated as an
automatic theorem of category theory.
-/

/-- The five traditional mutually related phases, with their
historical generative order. -/
inductive WuxingPhase
  | wood | fire | earth | metal | water
  deriving DecidableEq, Repr, Fintype

/-- 相生, the oriented exterior pentagon. -/
def wuxingSheng : WuxingPhase → WuxingPhase
  | .wood => .fire
  | .fire => .earth
  | .earth => .metal
  | .metal => .water
  | .water => .wood

/-- 相剋, the oriented five-pointed star. -/
def wuxingKe : WuxingPhase → WuxingPhase
  | .wood => .earth
  | .earth => .water
  | .water => .fire
  | .fire => .metal
  | .metal => .wood

/-- The controlling arrow is EXACTLY two generative steps, not
an independently added unrelated arbitrary five-cycle. -/
theorem wuxingKe_eq_sheng_twice (p : WuxingPhase) :
    wuxingKe p = wuxingSheng (wuxingSheng p) := by
  cases p <;> rfl

/-- Both oriented flows close after five original phases. -/
theorem wuxingSheng_five_steps (p : WuxingPhase) :
    wuxingSheng (wuxingSheng (wuxingSheng
      (wuxingSheng (wuxingSheng p)))) = p := by
  cases p <;> rfl

theorem wuxingKe_five_steps (p : WuxingPhase) :
    wuxingKe (wuxingKe (wuxingKe
      (wuxingKe (wuxingKe p)))) = p := by
  cases p <;> rfl

/-- At every phase the generative and controlling targets differ. -/
theorem wuxingSheng_ne_ke (p : WuxingPhase) :
    wuxingSheng p ≠ wuxingKe p := by
  cases p <;> decide

/-- Every phase acts on exactly one generative and one controlling
successor, yielding two distinct directed outgoing arrow types. -/
inductive WuxingArrow : WuxingPhase → WuxingPhase → Type
  | sheng (p : WuxingPhase) : WuxingArrow p (wuxingSheng p)
  | ke (p : WuxingPhase) : WuxingArrow p (wuxingKe p)

/-- Genuine mathlib quiver, not a graph metaphor. -/
instance : Quiver WuxingPhase where
  Hom := WuxingArrow

/-- The original exterior five-arrow cycle is an actual typed
mathlib quiver path based at Wood. -/
def wuxingShengPentagon :
    Quiver.Path WuxingPhase.wood WuxingPhase.wood :=
  (((((Quiver.Path.nil : Quiver.Path WuxingPhase.wood WuxingPhase.wood)
    .cons (WuxingArrow.sheng .wood))
    .cons (WuxingArrow.sheng .fire))
    .cons (WuxingArrow.sheng .earth))
    .cons (WuxingArrow.sheng .metal))
    .cons (WuxingArrow.sheng .water)

/-- The five star diagonals form another original typed 5-arrow
cycle with a different order of the SAME five source vertices. -/
def wuxingKePentagram :
    Quiver.Path WuxingPhase.wood WuxingPhase.wood :=
  (((((Quiver.Path.nil : Quiver.Path WuxingPhase.wood WuxingPhase.wood)
    .cons (WuxingArrow.ke .wood))
    .cons (WuxingArrow.ke .earth))
    .cons (WuxingArrow.ke .water))
    .cons (WuxingArrow.ke .fire))
    .cons (WuxingArrow.ke .metal)

theorem wuxingShengPentagon_length :
    wuxingShengPentagon.length = 5 := by
  rfl

theorem wuxingKePentagram_length :
    wuxingKePentagram.length = 5 := by
  rfl

/-- A real path category exists by mathlib's universal free
category construction on this source quiver. -/
abbrev WuxingPathCategory := CategoryTheory.Paths WuxingPhase

/-- Unlike a directed 5-cycle alone, the combined two relations
orient every unordered pair of distinct five phases exactly once.
This gives the underlying abstract K5 tournament. -/
theorem wuxing_complete_tournament :
    ∀ a b : WuxingPhase,
      a ≠ b ↔
      (b = wuxingSheng a ∨ b = wuxingKe a ∨
       a = wuxingSheng b ∨ a = wuxingKe b) := by
  decide

/-- No two phases are mutually adjacent by any forward relation:
this witnesses the tournament's one-way nature. -/
theorem wuxing_no_two_way_relation :
    ∀ a b : WuxingPhase,
      (b = wuxingSheng a ∨ b = wuxingKe a) →
      ¬ (a = wuxingSheng b ∨ a = wuxingKe b) := by
  decide

theorem wuxingPhase_card : Fintype.card WuxingPhase = 5 := by
  decide

/-- FIX A CHART: Wood at slot 0, Fire at slot 1, Earth at 2,
Metal at 3, Water at 4. This breaks the unpointed C5 symmetry;
a different chart can be chosen without altering the relations. -/
def wuxingSlotEquiv : WuxingPhase ≃ PentagonalSlot where
  toFun
    | .wood => .s0
    | .fire => .s1
    | .earth => .s2
    | .metal => .s3
    | .water => .s4
  invFun
    | .s0 => .wood
    | .s1 => .fire
    | .s2 => .earth
    | .s3 => .metal
    | .s4 => .water
  left_inv := by
    intro p
    cases p <;> rfl
  right_inv := by
    intro s
    cases s <;> rfl

/-- The five elements in the exact around-pentagon slot order. -/
def wuxingGenerativeOrder : List WuxingPhase :=
  [.wood, .fire, .earth, .metal, .water]

theorem wuxingSlotSheng_equivariant (p : WuxingPhase) :
    wuxingSlotEquiv (wuxingSheng p) =
      pentagonalSlotNext (wuxingSlotEquiv p) := by
  cases p <;> rfl

theorem wuxingSlotKe_equivariant (p : WuxingPhase) :
    wuxingSlotEquiv (wuxingKe p) =
      pentagonalSlotNext (pentagonalSlotNext (wuxingSlotEquiv p)) := by
  cases p <;> rfl

/-- The category-theoretic distinction: two typed 5-cycles coexist
in the FREE PATH CATEGORY. They are not declared equal by the
pictorial fact that their line segments share five vertices. -/
theorem wuxingTwoCycles_have_equal_length :
    wuxingShengPentagon.length = wuxingKePentagram.length := by
  rfl

#print axioms wuxingKe_eq_sheng_twice
#print axioms wuxingSheng_five_steps
#print axioms wuxingKe_five_steps
#print axioms wuxingSheng_ne_ke
#print axioms wuxingShengPentagon
#print axioms wuxingKePentagram
#print axioms wuxingShengPentagon_length
#print axioms wuxingKePentagram_length
#print axioms wuxing_complete_tournament
#print axioms wuxing_no_two_way_relation
#print axioms wuxingSlotSheng_equivariant
#print axioms wuxingSlotKe_equivariant

end
end KUOS.DependentOriginationGrayC60WuxingPentagramQuiverV5_169
