import KUOS.Architecture.QiWuxingGK5CHP77ConservativeQuotientFunctorV4_54
import Mathlib.Combinatorics.Quiver.Path
import Mathlib.Tactic

/-!
Qi v4.55 — UNCONDITIONAL FAITHFULNESS OF THE GENUINE P77
CONSERVATIVE-FIVE-CELL QUOTIENT FUNCTOR ON THE REAL FIVEFOLD QUIVER.

The sole source is the original v3.5 FivefoldEdge with precisely
e01, e12, e23, e04 and e43, not Qi's separate FivePhase
generation/control quiver. Prove by exhaustive COMPUTABLE finite
edge-grammar checks and genuine Path constructor decomposition:

* no directed four-edge chain exists (any path has length <= 3);
* each typed one-edge, two-edge and three-edge path is determined
  by its common source, target and length;
* hence for the ACTUAL fivefold free path category the length map
  is injective on every Hom;
* the original proof-relevant P77 evaluator is unconditionally
  injective on each Hom;
* the Qi v4.54 category functor to ORIGINAL P77 FOUR-PROOFS
  modulo GK5CG CONSERVATIVE Type-valued five-cells is FAITHFUL;
* original conservative five-cell evidence between two evaluated
  paths exists iff the two paths are ALREADY equal.

This does NOT identify the original fivefold upper and lower
pentagon routes, whose lengths are 3 and 2. It does NOT adjoin a
historical source pentagonator or claim that arbitrary quivers
have length-faithful presentations. No use of P94A shadow
equality, physical C60 edge-list equality, numeric CRT, or
external axioms to create original Type evidence.

Strict 空 center, independent Kuu one presentation; append-only,
fixed 107 public roots. Lean v4.30.0-rc2, mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6;
protected PR #1558 Draft/open/unmerged.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace KUOS.Architecture.WuxingPentagonUnified
open KUOS.Architecture.WuxingCyclicPaths
open Kuu.F112.Physical
open CategoryTheory

set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

/-! ### True finite FivefoldEdge grammar: no invented directed arrows. -/

/-- The canonical 5 directed edges have pairwise distinct ordered
source/target coordinates. This is a FINITE DECIDABLE edge proof. -/
theorem fivefoldEdge_from_to_injective :
    ∀ (e d : FivefoldEdge),
      fivefoldFrom e = fivefoldFrom d →
      fivefoldTo e = fivefoldTo d → e = d := by
  decide

/-- Faithful wrapper: equality of the indexed phase suffices for
equality of the actual free-path vertex. -/
theorem fivefoldPathVertex_eq_of_phase
    {u v : FivefoldPathVertex} (h : u.phase = v.phase) : u = v := by
  cases u with
  | mk up =>
    cases v with
    | mk vp =>
      cases h
      rfl

/-- At fixed genuinely typed endpoints, there is at most ONE
primitive arrow. No graph edge or P77 proof term is collapsed. -/
instance fivefoldPathArrow_subsingleton
    (u v : FivefoldPathVertex) :
    Subsingleton (FivefoldPathArrow u v) where
  allEq e d := by
    rcases e with ⟨edge, hs, ht⟩
    rcases d with ⟨edge', hs', ht'⟩
    have he : edge = edge' :=
      fivefoldEdge_from_to_injective edge edge'
        (hs.trans hs'.symm) (ht.trans ht'.symm)
    subst edge'
    rfl

/-- Among genuinely composable two-edge words, the common
source and target uniquely determine BOTH edges. -/
theorem fivefoldTwoEdgeWord_unique :
    ∀ (a b c d : FivefoldEdge),
      fivefoldTo a = fivefoldFrom b →
      fivefoldTo c = fivefoldFrom d →
      fivefoldFrom a = fivefoldFrom c →
      fivefoldTo b = fivefoldTo d →
      a = c ∧ b = d := by
  decide

/-- The sole directed three-edge word in the original fivefold
quiver is 01 ; 12 ; 23. -/
theorem fivefoldThreeEdgeWord_unique :
    ∀ (a b c : FivefoldEdge),
      fivefoldTo a = fivefoldFrom b →
      fivefoldTo b = fivefoldFrom c →
      a = .e01 ∧ b = .e12 ∧ c = .e23 := by
  decide

/-- There is no directed four-edge word. The graph is finite and
acyclic in precisely this direction. -/
theorem fivefoldFourEdgeWord_impossible :
    ∀ (a b c d : FivefoldEdge),
      fivefoldTo a = fivefoldFrom b →
      fivefoldTo b = fivefoldFrom c →
      fivefoldTo c = fivefoldFrom d → False := by
  decide

/-! ### Real Quiver.Path length and typed decomposition. -/

/-- A genuine finite path in this particular quiver has at most
three directed edges; any four trailing arrows would contradict
the exact source/target grammar. -/
theorem fivefoldFreePath_length_le_three
    {u v : FivefoldPathVertex} (path : Quiver.Path u v) :
    path.length ≤ 3 := by
  cases path with
  | nil => simp
  | cons p₃ e₄ =>
    cases p₃ with
    | nil => simp
    | cons p₂ e₃ =>
      cases p₂ with
      | nil => simp
      | cons p₁ e₂ =>
        cases p₁ with
        | nil => simp
        | cons p₀ e₁ =>
          exfalso
          exact fivefoldFourEdgeWord_impossible
            e₁.edge e₂.edge e₃.edge e₄.edge
            (e₁.target_eq.trans e₂.source_eq.symm)
            (e₂.target_eq.trans e₃.source_eq.symm)
            (e₃.target_eq.trans e₄.source_eq.symm)

/-- Every typed length-one free path is literally a singleton
constructed from its genuine original FivefoldPathArrow. -/
theorem fivefoldFreePath_one_decomp
    {u v : FivefoldPathVertex} (path : Quiver.Path u v)
    (hl : path.length = 1) :
    ∃ (e : FivefoldPathArrow u v),
      path = (Quiver.Path.nil : Quiver.Path u u).cons e := by
  cases path with
  | nil => simp at hl
  | cons path e =>
    cases path with
    | nil => exact ⟨e, rfl⟩
    | cons path e' =>
      simp only [Quiver.Path.length_cons] at hl
      omega

/-- Length-two paths decompose into two actual typed arrows,
including the intermediate original FivefoldPathVertex. -/
theorem fivefoldFreePath_two_decomp
    {u v : FivefoldPathVertex} (path : Quiver.Path u v)
    (hl : path.length = 2) :
    ∃ (m : FivefoldPathVertex)
      (e₁ : FivefoldPathArrow u m) (e₂ : FivefoldPathArrow m v),
      path = ((Quiver.Path.nil : Quiver.Path u u).cons e₁).cons e₂ := by
  cases path with
  | nil => simp at hl
  | cons path e₂ =>
    cases path with
    | nil => simp at hl
    | cons path e₁ =>
      cases path with
      | nil => exact ⟨_, e₁, e₂, rfl⟩
      | cons path e₀ =>
        simp only [Quiver.Path.length_cons] at hl
        omega

/-- Length-three paths decompose into three genuine typed
FivefoldPathArrow constructors with both intermediate objects. -/
theorem fivefoldFreePath_three_decomp
    {u v : FivefoldPathVertex} (path : Quiver.Path u v)
    (hl : path.length = 3) :
    ∃ (m₁ m₂ : FivefoldPathVertex)
      (e₁ : FivefoldPathArrow u m₁)
      (e₂ : FivefoldPathArrow m₁ m₂)
      (e₃ : FivefoldPathArrow m₂ v),
      path =
        (((Quiver.Path.nil : Quiver.Path u u).cons e₁).cons e₂).cons e₃ := by
  cases path with
  | nil => simp at hl
  | cons path e₃ =>
    cases path with
    | nil => simp at hl
    | cons path e₂ =>
      cases path with
      | nil => simp at hl
      | cons path e₁ =>
        cases path with
        | nil => exact ⟨_, _, e₁, e₂, e₃, rfl⟩
        | cons path e₀ =>
          simp only [Quiver.Path.length_cons] at hl
          omega

/-- Any two one-step paths with the same typed endpoints coincide.
This uses actual primitive arrow subsingleton, not a shadow. -/
theorem fivefoldFreePath_one_unique
    {u v : FivefoldPathVertex}
    (p q : Quiver.Path u v)
    (hp : p.length = 1) (hq : q.length = 1) : p = q := by
  obtain ⟨e, he⟩ := fivefoldFreePath_one_decomp p hp
  obtain ⟨d, hd⟩ := fivefoldFreePath_one_decomp q hq
  have hedge : e = d := Subsingleton.elim _ _
  rw [he, hd, hedge]

/-- Length-two paths are unique for fixed source/target.
The only composable words are 01-12, 12-23, and 04-43,
with distinct ordered endpoints. -/
theorem fivefoldFreePath_two_unique
    {u v : FivefoldPathVertex}
    (p q : Quiver.Path u v)
    (hp : p.length = 2) (hq : q.length = 2) : p = q := by
  obtain ⟨m, e₁, e₂, he⟩ := fivefoldFreePath_two_decomp p hp
  obtain ⟨n, d₁, d₂, hd⟩ := fivefoldFreePath_two_decomp q hq
  obtain ⟨h₁, h₂⟩ :=
    fivefoldTwoEdgeWord_unique e₁.edge e₂.edge d₁.edge d₂.edge
      (e₁.target_eq.trans e₂.source_eq.symm)
      (d₁.target_eq.trans d₂.source_eq.symm)
      (e₁.source_eq.trans d₁.source_eq.symm)
      (e₂.target_eq.trans d₂.target_eq.symm)
  have hmn : m = n :=
    fivefoldPathVertex_eq_of_phase
      (e₁.target_eq.symm.trans
        ((congrArg fivefoldTo h₁).trans d₁.target_eq))
  subst n
  have hed1 : e₁ = d₁ := Subsingleton.elim _ _
  have hed2 : e₂ = d₂ := Subsingleton.elim _ _
  rw [he, hd, hed1, hed2]

/-- Exactly one typed three-edge path is possible: 01-12-23.
The proof retains all intermediate dependent quiver endpoints. -/
theorem fivefoldFreePath_three_unique
    {u v : FivefoldPathVertex}
    (p q : Quiver.Path u v)
    (hp : p.length = 3) (hq : q.length = 3) : p = q := by
  obtain ⟨m₁, m₂, e₁, e₂, e₃, he⟩ :=
    fivefoldFreePath_three_decomp p hp
  obtain ⟨n₁, n₂, d₁, d₂, d₃, hd⟩ :=
    fivefoldFreePath_three_decomp q hq
  obtain ⟨he1, he2, he3⟩ :=
    fivefoldThreeEdgeWord_unique e₁.edge e₂.edge e₃.edge
      (e₁.target_eq.trans e₂.source_eq.symm)
      (e₂.target_eq.trans e₃.source_eq.symm)
  obtain ⟨hd1, hd2, hd3⟩ :=
    fivefoldThreeEdgeWord_unique d₁.edge d₂.edge d₃.edge
      (d₁.target_eq.trans d₂.source_eq.symm)
      (d₂.target_eq.trans d₃.source_eq.symm)
  have hm₁ : m₁ = n₁ :=
    fivefoldPathVertex_eq_of_phase
      (e₁.target_eq.symm.trans
        ((congrArg fivefoldTo (he1.trans hd1.symm)).trans d₁.target_eq))
  have hm₂ : m₂ = n₂ :=
    fivefoldPathVertex_eq_of_phase
      (e₂.target_eq.symm.trans
        ((congrArg fivefoldTo (he2.trans hd2.symm)).trans d₂.target_eq))
  subst n₁
  subst n₂
  have hed1 : e₁ = d₁ := Subsingleton.elim _ _
  have hed2 : e₂ = d₂ := Subsingleton.elim _ _
  have hed3 : e₃ = d₃ := Subsingleton.elim _ _
  rw [he, hd, hed1, hed2, hed3]

/-- This exact finite quiver is LENGTH-FAITHFUL on every original
typed Hom: equal endpoints and equal lengths imply equal paths. -/
theorem fivefoldFreePath_length_injective
    {u v : FivefoldPathVertex} :
    Function.Injective (fun path : Quiver.Path u v => path.length) := by
  intro p q heq
  change p.length = q.length at heq
  have hpbound := fivefoldFreePath_length_le_three p
  have hqbound := fivefoldFreePath_length_le_three q
  by_cases hzero : p.length = 0
  · have hqzero : q.length = 0 := by omega
    have huv : u = v := p.eq_of_length_zero hzero
    subst v
    have he : p = (Quiver.Path.nil : Quiver.Path u u) :=
      p.eq_nil_of_length_zero hzero
    have hd : q = (Quiver.Path.nil : Quiver.Path u u) :=
      q.eq_nil_of_length_zero hqzero
    rw [he, hd]
  by_cases hone : p.length = 1
  · exact fivefoldFreePath_one_unique p q hone (by omega)
  by_cases htwo : p.length = 2
  · exact fivefoldFreePath_two_unique p q htwo (by omega)
  have hthree : p.length = 3 := by omega
  exact fivefoldFreePath_three_unique p q hthree (by omega)

/-! ### Upgrade Qi v4.53 and Qi v4.54 to unconditional faithfulness. -/

universe uD vD uE vE

variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {p : Polygon} {a b : D} {x y : E}
variable {n n' m m' : Nat}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}
variable {first : KuuNativeF45Tree p n m ma pa mb pb}
variable {last : KuuNativeF45Tree p n' m' ma pa mb pb}
variable {r₀ r₁ r₂ r₃ r₄ :
  KuuNativeF45Tree.DepthRotationRoute p first last}
variable
  (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₀ r₁)
  (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₁ r₂)
  (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₂ r₃)
  (k : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₃ r₄)

/-- The ACTUAL original P77 four-proof evaluator is unconditionally
injective on every fixed typed FivefoldEdge finite-path Hom. -/
theorem fivefoldEvaluateP77_injective_genuine
    {u v : FivefoldPathVertex} :
    Function.Injective
      (fivefoldEvaluateP77 f g h k (u := u) (v := v)) := by
  exact fivefoldEvaluateP77_injective_of_length f g h k
    (fun {u v} => fivefoldFreePath_length_injective (u := u) (v := v))

/-- Qi v4.54's genuine category FUNCTOR is UNCONDITIONALLY FAITHFUL
for all actual original F55 source data. The proof uses the original
GK5CG charge soundness descending through the source-defined
conservative-five-cell quotient and the true finite edge grammar. -/
theorem fivefoldP77ConservativeFunctor_faithful_genuine :
    (fivefoldP77ConservativeFunctor f g h k).Faithful := by
  letI := fivefoldP77ConservativeCategory f g h k
  apply (fivefoldP77ConservativeFunctor_faithful_iff f g h k).2
  intro u v A B hcert
  have hmap :
      (fivefoldP77ConservativeFunctor f g h k).map A =
      (fivefoldP77ConservativeFunctor f g h k).map B :=
    (fivefoldP77ConservativeFunctor_map_eq_iff f g h k A B).2 hcert
  have hcharge := congrArg (fivefoldP77ConservativeCharge f g h k) hmap
  have hlen : (A.length : ℤ) = (B.length : ℤ) := by
    simpa only [fivefoldP77ConservativeFunctor_charge_length] using hcharge
  exact fivefoldFreePath_length_injective (by exact_mod_cast hlen)

/-- A conservative source five-cell exists between two evaluated
original P77 paths IFF those very paths were already equal in the
free typed fivefold category. In particular, no phantom pentagonator. -/
theorem fivefoldEvaluateP77_conservativeFiveCell_iff_path_eq
    {u v : FivefoldPathVertex} (A B : Quiver.Path u v) :
    Nonempty (NativeGK5CGConservativeFiveCell first last
      (fivefoldEvaluateP77 f g h k A)
      (fivefoldEvaluateP77 f g h k B)) ↔ A = B := by
  letI := fivefoldP77ConservativeCategory f g h k
  constructor
  · intro hcert
    have hmap :=
      (fivefoldP77ConservativeFunctor_map_eq_iff f g h k A B).2 hcert
    exact (fivefoldP77ConservativeFunctor_faithful_genuine f g h k).map_injective hmap
  · intro hpath
    subst B
    exact ⟨.refl (fivefoldEvaluateP77 f g h k A)⟩

/-- Any distinct, same-endpoint free paths remain structurally
unrelated by original conservative P77 five-cells, even when
a numerical observer cannot distinguish them. -/
theorem fivefoldEvaluateP77_noConservativeFiveCell_of_ne
    {u v : FivefoldPathVertex} (A B : Quiver.Path u v)
    (hne : A ≠ B) :
    ¬ Nonempty (NativeGK5CGConservativeFiveCell first last
      (fivefoldEvaluateP77 f g h k A)
      (fivefoldEvaluateP77 f g h k B)) := by
  intro hcert
  exact hne
    ((fivefoldEvaluateP77_conservativeFiveCell_iff_path_eq f g h k A B).1 hcert)

#print axioms fivefoldEdge_from_to_injective
#print axioms fivefoldPathVertex_eq_of_phase
#print axioms fivefoldPathArrow_subsingleton
#print axioms fivefoldTwoEdgeWord_unique
#print axioms fivefoldThreeEdgeWord_unique
#print axioms fivefoldFourEdgeWord_impossible
#print axioms fivefoldFreePath_length_le_three
#print axioms fivefoldFreePath_one_decomp
#print axioms fivefoldFreePath_two_decomp
#print axioms fivefoldFreePath_three_decomp
#print axioms fivefoldFreePath_one_unique
#print axioms fivefoldFreePath_two_unique
#print axioms fivefoldFreePath_three_unique
#print axioms fivefoldFreePath_length_injective
#print axioms fivefoldEvaluateP77_injective_genuine
#print axioms fivefoldP77ConservativeFunctor_faithful_genuine
#print axioms fivefoldEvaluateP77_conservativeFiveCell_iff_path_eq
#print axioms fivefoldEvaluateP77_noConservativeFiveCell_of_ne

end
end KUOS.Architecture.WuxingPentagonUnified
