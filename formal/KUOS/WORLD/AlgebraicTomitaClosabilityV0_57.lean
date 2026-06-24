import Mathlib

/-!
A Mathlib-only graph kernel for the first closability step in Tomita theory.

The module does not construct a von Neumann algebra, a standard form, or a
relative modular operator.  It isolates the analytic implication used in the
usual proof of closability: a densely represented dual core and the Tomita
pairing identity force every vertical limit in the closure of the algebraic
Tomita graph to vanish.
-/

namespace KUOS
namespace WORLD

noncomputable section

open Filter Topology

variable {A B H : Type*}
variable [NormedAddCommGroup H] [InnerProductSpace ℂ H]

/--
A representation-level pair of algebraic Tomita cores.

`leftVector a` models `a Ω`, `leftStar a` models `a⋆`, and `rightVector b`
models a dense commutant core.  The pairing field is the concrete input used
in the standard closability argument.  No modular operator is assumed.
-/
structure AlgebraicTomitaDualCore (A B H : Type*)
    [NormedAddCommGroup H] [InnerProductSpace ℂ H] where
  leftVector : A → H
  leftStar : A → A
  leftStar_involutive : Function.Involutive leftStar
  leftVector_injective : Function.Injective leftVector
  leftDense : DenseRange leftVector
  rightVector : B → H
  rightStar : B → B
  rightDense : DenseRange rightVector
  pairing : ∀ a b,
    inner ℂ (leftVector (leftStar a)) (rightVector b) =
      inner ℂ (leftVector a) (rightVector (rightStar b))

namespace AlgebraicTomitaDualCore

variable (T : AlgebraicTomitaDualCore A B H)

/-- The algebraic Tomita domain represented inside the Hilbert space. -/
def domain : Set H := Set.range T.leftVector

/-- The graph of the algebraic Tomita map `a Ω ↦ a⋆ Ω`. -/
def graph : Set (H × H) :=
  {p | ∃ a, p.1 = T.leftVector a ∧ p.2 = T.leftVector (T.leftStar a)}

/-- The represented algebraic domain is dense. -/
theorem domain_dense : Dense T.domain :=
  T.leftDense

/-- Separating injectivity makes the Tomita value independent of a representative. -/
theorem tomita_value_independent {a₁ a₂ : A}
    (h : T.leftVector a₁ = T.leftVector a₂) :
    T.leftVector (T.leftStar a₁) = T.leftVector (T.leftStar a₂) := by
  exact congrArg (fun a => T.leftVector (T.leftStar a))
    (T.leftVector_injective h)

/-- The algebraic Tomita graph is single-valued. -/
theorem graph_right_unique {x y z : H}
    (hxy : (x, y) ∈ T.graph) (hxz : (x, z) ∈ T.graph) : y = z := by
  rcases hxy with ⟨a, hxa, hya⟩
  rcases hxz with ⟨b, hxb, hzb⟩
  have hab : a = b :=
    T.leftVector_injective (hxa.symm.trans hxb)
  calc
    y = T.leftVector (T.leftStar a) := hya
    _ = T.leftVector (T.leftStar b) := by rw [hab]
    _ = z := hzb.symm

/-- Algebraic involutivity flips the Tomita graph. -/
theorem graph_flip {x y : H} (hxy : (x, y) ∈ T.graph) :
    (y, x) ∈ T.graph := by
  rcases hxy with ⟨a, hxa, hya⟩
  refine ⟨T.leftStar a, hya, ?_⟩
  simpa only [T.leftStar_involutive a] using hxa

/-- Applying the represented algebraic Tomita value twice returns the original vector. -/
theorem tomita_value_sq (a : A) :
    T.leftVector (T.leftStar (T.leftStar a)) = T.leftVector a := by
  rw [T.leftStar_involutive a]

/--
A graph is closable when the closure of its graph has no nonzero vertical
vector above zero.
-/
def IsClosableGraph (G : Set (H × H)) : Prop :=
  ∀ z, (0, z) ∈ closure G → z = 0

/--
The dense dual core and the Tomita pairing identity imply the sequential
closability criterion for represented algebra elements.
-/
theorem representative_sequential_closability
    (a : ℕ → A) (z : H)
    (ha : Tendsto (fun n => T.leftVector (a n)) atTop (𝓝 0))
    (hTa : Tendsto (fun n => T.leftVector (T.leftStar (a n))) atTop (𝓝 z)) :
    z = 0 := by
  apply T.rightDense.eq_zero_of_inner_left ℂ
  intro b
  have hz :
      Tendsto
        (fun n => inner ℂ (T.leftVector (T.leftStar (a n))) (T.rightVector b))
        atTop (𝓝 (inner ℂ z (T.rightVector b))) :=
    hTa.inner tendsto_const_nhds
  have hzero :
      Tendsto
        (fun n => inner ℂ (T.leftVector (a n))
          (T.rightVector (T.rightStar b)))
        atTop (𝓝 0) := by
    simpa using ha.inner tendsto_const_nhds
  have hfun :
      (fun n => inner ℂ (T.leftVector (T.leftStar (a n))) (T.rightVector b)) =
        (fun n => inner ℂ (T.leftVector (a n))
          (T.rightVector (T.rightStar b))) := by
    funext n
    exact T.pairing (a n) b
  have hzero' :
      Tendsto
        (fun n => inner ℂ (T.leftVector (T.leftStar (a n))) (T.rightVector b))
        atTop (𝓝 0) := by
    rw [hfun]
    exact hzero
  exact tendsto_nhds_unique hz hzero'

/-- The algebraic Tomita graph satisfies the sequential graph criterion. -/
theorem graph_sequentially_closable
    (x y : ℕ → H) (z : H)
    (hgraph : ∀ n, (x n, y n) ∈ T.graph)
    (hx : Tendsto x atTop (𝓝 0))
    (hy : Tendsto y atTop (𝓝 z)) :
    z = 0 := by
  choose a hxa hya using hgraph
  have hleft : (fun n => T.leftVector (a n)) = x := by
    funext n
    exact (hxa n).symm
  have hright : (fun n => T.leftVector (T.leftStar (a n))) = y := by
    funext n
    exact (hya n).symm
  apply T.representative_sequential_closability a z
  · rw [hleft]
    exact hx
  · rw [hright]
    exact hy

/--
The algebraic Tomita graph is closable in the standard graph-closure sense.

This is the first genuine analytic bridge beyond representative independence:
it converts the dense commutant-core pairing into uniqueness of the vertical
limit in `closure graph`.
-/
theorem graph_closable : T.IsClosableGraph T.graph := by
  intro z hz
  obtain ⟨p, hpGraph, hpLimit⟩ :=
    (mem_closure_iff_seq_limit.mp hz)
  have hfst : Tendsto (fun n => (p n).1) atTop (𝓝 0) := by
    simpa using (continuous_fst.tendsto (0, z)).comp hpLimit
  have hsnd : Tendsto (fun n => (p n).2) atTop (𝓝 z) := by
    simpa using (continuous_snd.tendsto (0, z)).comp hpLimit
  exact T.graph_sequentially_closable
    (fun n => (p n).1) (fun n => (p n).2) z hpGraph hfst hsnd

end AlgebraicTomitaDualCore
end
end WORLD
end KUOS
