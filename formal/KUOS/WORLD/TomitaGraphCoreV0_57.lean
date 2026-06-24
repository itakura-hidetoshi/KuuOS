import Mathlib

namespace KUOS.WORLD

noncomputable section
open Filter Topology

variable {A B H : Type*}
variable [NormedAddCommGroup H] [InnerProductSpace ℂ H]

structure TomitaGraphCore (A B H : Type*)
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

namespace TomitaGraphCore

variable (T : TomitaGraphCore A B H)

def domain : Set H := Set.range T.leftVector

def graph : Set (H × H) :=
  {p | ∃ a, p.1 = T.leftVector a ∧ p.2 = T.leftVector (T.leftStar a)}

theorem domain_dense : Dense T.domain := T.leftDense

theorem value_independent {a₁ a₂ : A}
    (h : T.leftVector a₁ = T.leftVector a₂) :
    T.leftVector (T.leftStar a₁) = T.leftVector (T.leftStar a₂) := by
  exact congrArg (fun a => T.leftVector (T.leftStar a))
    (T.leftVector_injective h)

theorem graph_right_unique {x y z : H}
    (hxy : (x, y) ∈ T.graph) (hxz : (x, z) ∈ T.graph) : y = z := by
  rcases hxy with ⟨a, hxa, hya⟩
  rcases hxz with ⟨b, hxb, hzb⟩
  have hab : a = b := T.leftVector_injective (hxa.symm.trans hxb)
  calc
    y = T.leftVector (T.leftStar a) := hya
    _ = T.leftVector (T.leftStar b) := by rw [hab]
    _ = z := hzb.symm

theorem graph_flip {x y : H} (hxy : (x, y) ∈ T.graph) :
    (y, x) ∈ T.graph := by
  rcases hxy with ⟨a, hxa, hya⟩
  refine ⟨T.leftStar a, hya, ?_⟩
  simpa only [T.leftStar_involutive a] using hxa

def IsClosableGraph (G : Set (H × H)) : Prop :=
  ∀ z, (0, z) ∈ closure G → z = 0

theorem representative_closable
    (a : ℕ → A) (z : H)
    (ha : Tendsto (fun n => T.leftVector (a n)) atTop (𝓝 0))
    (hTa : Tendsto (fun n => T.leftVector (T.leftStar (a n))) atTop (𝓝 z)) :
    z = 0 := by
  refine T.rightDense.eq_zero_of_inner_left (𝐵 := ℂ) (x := z) ?_
  intro b
  have hzj := hTa.inner (tendsto_const_nhds :
    Tendsto (fun _ : ℕ => T.rightVector b) atTop (𝓝 (T.rightVector b)))
  have hzero : Tendsto
      (fun n => inner ℂ (T.leftVector (a n)) (T.rightVector (T.rightStar b)))
      atTop (𝓝 0) := by
    simpa using ha.inner (tendsto_const_nhds :
      Tendsto (fun _ : ℕ => T.rightVector (T.rightStar b)) atTop
        (𝓝 (T.rightVector (T.rightStar b))))
  have heq :
      (fun n => inner ℂ (T.leftVector (T.leftStar (a n))) (T.rightVector b)) =
        (fun n => inner ℂ (T.leftVector (a n)) (T.rightVector (T.rightStar b))) := by
    funext n
    exact T.pairing (a n) b
  have hzero' : Tendsto
      (fun n => inner ℂ (T.leftVector (T.leftStar (a n))) (T.rightVector b))
      atTop (𝓝 0) := by
    rw [heq]
    exact hzero
  exact tendsto_nhds_unique hz hzero'

theorem graph_closable : IsClosableGraph T.graph := by
  intro z hz
  obtain ⟨p, hp, hpLim⟩ := mem_closure_iff_seq_limit.mp hz
  choose a hxa hya using hp
  apply T.representative_closable a z
  · have hfst := (continuous_fst.tendsto (0, z)).comp hpLim
    simpa only [← hxa] using hfst
  · have hsnd := (continuous_snd.tendsto (0, z)).comp hpLim
    simpa only [← hya] using hsnd

end TomitaGraphCore
end
end KUOS.WORLD
