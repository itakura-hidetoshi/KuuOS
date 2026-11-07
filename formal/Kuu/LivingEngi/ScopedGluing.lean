import Mathlib

/-!
# Living Engi Cycle: scoped function gluing and evidence-gated promotion

LEC-01 (the sheaf of ALL set-theoretic functions): local function values
on a covering family glue uniquely exactly when they agree on every
nonempty overlap. This is not an unproved assertion of effectiveness
for arbitrary prestacks, higher stacks or source proof histories.

LEC-02: a function factors through a surjective quotient precisely if
it is constant on quotient fibers. Integer orientation does not factor
through reduction modulo two: the quotient forgets a genuine difference.

LEC-04: unchecked, refuted and certified states are separate typed
constructors. Only certification carries a proof of the selected
mathematical proposition and admits that *scoped* proposition.

No existing Kuu source, F55/P77/GK5CG proof history, or Qi/Gray
presentation is imported or identified. Mathematical admission here
does not provide truth or action authority outside the proved scope.

See docs/LIVING_ENGI_CYCLE_VEDANA_TANHA_UPADANA_BHAVA_v0_1.md.
-/

namespace Kuu.LivingEngi

set_option autoImplicit false

universe u v w

section LocalGluing

variable {X : Type u} {I : Type v} {A : Type w}

/-- A source-indexed family of genuine local functions on a cover.
The domain subtype remembers which local support was used. -/
abbrev LocalSections (U : I → Set X) (A : Type w) :=
  (i : I) → {x : X // x ∈ U i} → A

/-- The declared local supports cover every point of the global carrier. -/
def Covers (U : I → Set X) : Prop :=
  ∀ x : X, ∃ i : I, x ∈ U i

/-- Exact overlap compatibility in the concrete function sheaf. -/
def Compatible (U : I → Set X) (s : LocalSections U A) : Prop :=
  ∀ (i j : I) (x : X) (hi : x ∈ U i) (hj : x ∈ U j),
    s i ⟨x, hi⟩ = s j ⟨x, hj⟩

/-- A global function agreeing with every ORIGINAL local value,
not merely with an observation quotient of that value. -/
def HasGlobal (U : I → Set X) (s : LocalSections U A) : Prop :=
  ∃ g : X → A,
    ∀ (i : I) (x : {y : X // y ∈ U i}), g x.1 = s i x

/-- Any actual global witness necessarily preserves local compatibility.
No cover assumption or arbitrary stack effectivity is smuggled in. -/
theorem global_implies_compatible
    (U : I → Set X) (s : LocalSections U A)
    (hglobal : HasGlobal U s) : Compatible U s := by
  rcases hglobal with ⟨g, hg⟩
  intro i j x hi hj
  exact (hg i ⟨x, hi⟩).symm.trans (hg j ⟨x, hj⟩)

/-- A concrete choice of a global function for a compatible cover.
The choice is an implementation detail; uniqueness is proved below. -/
noncomputable def glue
    (U : I → Set X) (s : LocalSections U A)
    (hcover : Covers U) (_hcompat : Compatible U s) : X → A :=
  fun x =>
    s (Classical.choose (hcover x))
      ⟨x, Classical.choose_spec (hcover x)⟩

/-- The glued function agrees with every original local section. -/
theorem glue_agrees
    (U : I → Set X) (s : LocalSections U A)
    (hcover : Covers U) (hcompat : Compatible U s)
    (i : I) (x : {y : X // y ∈ U i}) :
    glue U s hcover hcompat x.1 = s i x := by
  change
    s (Classical.choose (hcover x.1))
        ⟨x.1, Classical.choose_spec (hcover x.1)⟩ = s i x
  exact hcompat (Classical.choose (hcover x.1)) i x.1
    (Classical.choose_spec (hcover x.1)) x.2

/-- Explicit and bidirectional local-to-global existence criterion
for the SHEAF OF FUNCTIONS under the stated cover condition. -/
theorem compatible_iff_hasGlobal
    (U : I → Set X) (s : LocalSections U A)
    (hcover : Covers U) :
    Compatible U s ↔ HasGlobal U s := by
  constructor
  · intro hcompat
    refine ⟨glue U s hcover hcompat, ?_⟩
    intro i x
    exact glue_agrees U s hcover hcompat i x
  · exact global_implies_compatible U s

/-- Under a cover, even independent choices of the global function
agree pointwise: uniqueness is not assumed as an extra axiom. -/
theorem global_unique
    (U : I → Set X) (s : LocalSections U A)
    (hcover : Covers U)
    {g₁ g₂ : X → A}
    (hg₁ : ∀ (i : I) (x : {y : X // y ∈ U i}), g₁ x.1 = s i x)
    (hg₂ : ∀ (i : I) (x : {y : X // y ∈ U i}), g₂ x.1 = s i x) :
    g₁ = g₂ := by
  funext x
  obtain ⟨i, hi⟩ := hcover x
  exact (hg₁ i ⟨x, hi⟩).trans (hg₂ i ⟨x, hi⟩).symm

/-- A single concrete overlap disagreement obstructs any global
function matching *both* given local values. -/
theorem no_global_of_disagreement
    (U : I → Set X) (s : LocalSections U A)
    (i j : I) (x : X)
    (hi : x ∈ U i) (hj : x ∈ U j)
    (hneq : s i ⟨x, hi⟩ ≠ s j ⟨x, hj⟩) :
    ¬ HasGlobal U s := by
  intro hglobal
  exact hneq ((global_implies_compatible U s hglobal) i j x hi hj)

end LocalGluing

section QuotientDescent

variable {X : Type u} {Q : Type v} {A : Type w}

/-- Exact factorization through a specified observation/quotient map. -/
def Factors (q : X → Q) (f : X → A) : Prop :=
  ∃ g : Q → A, ∀ x : X, g (q x) = f x

/-- Factoring through q forces constancy on each q-fiber. -/
theorem factors_constant_on_fibers
    (q : X → Q) (f : X → A)
    (hfactor : Factors q f)
    (x y : X) (hxy : q x = q y) : f x = f y := by
  rcases hfactor with ⟨g, hg⟩
  calc
    f x = g (q x) := (hg x).symm
    _ = g (q y) := congrArg g hxy
    _ = f y := hg y

/-- For surjective q, fiber-constancy is exactly the needed
and sufficient certificate for ordinary function factorization. -/
theorem factors_iff_fiber_constant
    (q : X → Q) (f : X → A)
    (hq : Function.Surjective q) :
    Factors q f ↔
      ∀ x y : X, q x = q y → f x = f y := by
  constructor
  · intro hfactor x y hxy
    exact factors_constant_on_fibers q f hfactor x y hxy
  · intro hconstant
    classical
    refine ⟨fun y => f (Classical.choose (hq y)), ?_⟩
    intro x
    exact hconstant (Classical.choose (hq (q x))) x
      (Classical.choose_spec (hq (q x)))

/-- A genuine collision in the quotient with distinct source values
is an explicit non-descent certificate. -/
theorem no_factor_of_collision
    (q : X → Q) (f : X → A)
    (x y : X) (hxy : q x = q y) (hne : f x ≠ f y) :
    ¬ Factors q f := by
  intro hfactor
  exact hne (factors_constant_on_fibers q f hfactor x y hxy)

/-- A concrete source-versus-quotient obstruction.
Reduction ℤ → ZMod 2 identifies the two opposite integer signs.
The integer identity cannot be reconstructed as a function of mod-two
data; this does not declare the mod-two quotient itself invalid. -/
theorem integer_sign_not_modTwo_factor :
    ¬ Factors (fun n : ℤ => (n : ZMod 2)) (fun n : ℤ => n) := by
  have hcast :
      ((1 : ℤ) : ZMod 2) = ((-1 : ℤ) : ZMod 2) := by
    change (1 : ZMod 2) = -1
    exact (ZMod.neg_eq_self_mod_two (1 : ZMod 2)).symm
  exact no_factor_of_collision
    (fun n : ℤ => (n : ZMod 2))
    (fun n : ℤ => n)
    (1 : ℤ) (-1 : ℤ) hcast (by norm_num)

end QuotientDescent

section PromotionEvidence

/-- Proof-relevant promotion state for one *specified* proposition.
Missing evidence is not a proof of nonexistence. A refutation carries
an actual negative proof, whereas certification carries a positive one. -/
inductive PromotionEvidence (P : Prop) : Type where
  | unchecked : PromotionEvidence P
  | refuted (proof : ¬ P) : PromotionEvidence P
  | certified (proof : P) : PromotionEvidence P

/-- Only a certified proposition can pass the mathematical admission gate.
This predicate is NOT an ActOS or external execution authority. -/
def Admissible {P : Prop} : PromotionEvidence P → Prop
  | .unchecked => False
  | .refuted _ => False
  | .certified _ => True

/-- Admitted evidence always contains a proof of precisely that proposition. -/
theorem admitted_sound {P : Prop}
    (e : PromotionEvidence P) (h : Admissible e) : P := by
  cases e with
  | unchecked => exact False.elim h
  | refuted _ => exact False.elim h
  | certified hp => exact hp

theorem unchecked_not_admitted (P : Prop) :
    ¬ Admissible (PromotionEvidence.unchecked : PromotionEvidence P) := by
  intro h
  exact h

theorem refuted_not_admitted {P : Prop} (hnot : ¬ P) :
    ¬ Admissible (PromotionEvidence.refuted hnot) := by
  intro h
  exact h

theorem certified_admitted {P : Prop} (hp : P) :
    Admissible (PromotionEvidence.certified hp) := by
  trivial

/-- Never admit global gluing if its original local values are
PROVEN incompatible. A missing proof alone is not this assumption. -/
theorem incompatible_no_promotion
    {X : Type u} {I : Type v} {A : Type w}
    (U : I → Set X) (s : LocalSections U A)
    (hbad : ¬ Compatible U s)
    (e : PromotionEvidence (HasGlobal U s)) :
    ¬ Admissible e := by
  intro hallowed
  exact hbad (global_implies_compatible U s (admitted_sound e hallowed))

end PromotionEvidence

#print axioms global_implies_compatible
#print axioms glue_agrees
#print axioms compatible_iff_hasGlobal
#print axioms global_unique
#print axioms no_global_of_disagreement
#print axioms factors_constant_on_fibers
#print axioms factors_iff_fiber_constant
#print axioms no_factor_of_collision
#print axioms integer_sign_not_modTwo_factor
#print axioms admitted_sound
#print axioms incompatible_no_promotion

end Kuu.LivingEngi
