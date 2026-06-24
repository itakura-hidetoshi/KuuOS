import Mathlib

namespace KUOS.WORLD

noncomputable section

open Filter Topology

variable {A B H : Type*}
variable [NormedAddCommGroup H] [InnerProductSpace Complex H]

structure TomitaGraphCore (A B H : Type*)
    [NormedAddCommGroup H] [InnerProductSpace Complex H] where
  leftVector : A -> H
  leftStar : A -> A
  leftStar_involutive : Function.Involutive leftStar
  leftVector_injective : Function.Injective leftVector
  leftDense : DenseRange leftVector
  rightVector : B -> H
  rightStar : B -> B
  rightDense : DenseRange rightVector
  pairing : forall a b,
    inner Complex (leftVector (leftStar a)) (rightVector b) =
      inner Complex (leftVector a) (rightVector (rightStar b))

namespace TomitaGraphCore

variable (T : TomitaGraphCore A B H)

def domain : Set H := Set.range T.leftVector

def graph : Set (Prod H H) :=
  fun p => Exists fun a =>
    And (p.1 = T.leftVector a)
      (p.2 = T.leftVector (T.leftStar a))

theorem domain_dense : Dense T.domain := T.leftDense

theorem value_independent {a1 a2 : A}
    (h : T.leftVector a1 = T.leftVector a2) :
    T.leftVector (T.leftStar a1) = T.leftVector (T.leftStar a2) := by
  exact congrArg (fun a => T.leftVector (T.leftStar a))
    (T.leftVector_injective h)

theorem graph_right_unique {x y z : H}
    (hxy : Set.mem T.graph (x, y))
    (hxz : Set.mem T.graph (x, z)) :
    y = z := by
  let a : A := Classical.choose hxy
  let b : A := Classical.choose hxz
  have hxa : x = T.leftVector a := (Classical.choose_spec hxy).1
  have hya : y = T.leftVector (T.leftStar a) :=
    (Classical.choose_spec hxy).2
  have hxb : x = T.leftVector b := (Classical.choose_spec hxz).1
  have hzb : z = T.leftVector (T.leftStar b) :=
    (Classical.choose_spec hxz).2
  have hab : a = b :=
    T.leftVector_injective (hxa.symm.trans hxb)
  calc
    y = T.leftVector (T.leftStar a) := hya
    _ = T.leftVector (T.leftStar b) := by rw [hab]
    _ = z := hzb.symm

theorem graph_flip {x y : H}
    (hxy : Set.mem T.graph (x, y)) :
    Set.mem T.graph (y, x) := by
  let a : A := Classical.choose hxy
  have hxa : x = T.leftVector a := (Classical.choose_spec hxy).1
  have hya : y = T.leftVector (T.leftStar a) :=
    (Classical.choose_spec hxy).2
  exact Exists.intro (T.leftStar a)
    (And.intro hya
      (by simpa only [T.leftStar_involutive a] using hxa))

def IsClosableGraph (G : Set (Prod H H)) : Prop :=
  forall z, Set.mem (closure G) (0, z) -> z = 0

theorem representative_closable
    (a : Nat -> A) (z : H)
    (ha : Tendsto (fun n => T.leftVector (a n)) atTop (nhds 0))
    (hTa : Tendsto
      (fun n => T.leftVector (T.leftStar (a n))) atTop (nhds z)) :
    z = 0 := by
  refine DenseRange.eq_zero_of_inner_left Complex T.rightDense ?_
  intro b
  have hz :
      Tendsto
        (fun n =>
          inner Complex
            (T.leftVector (T.leftStar (a n)))
            (T.rightVector b))
        atTop
        (nhds (inner Complex z (T.rightVector b))) :=
    hTa.inner tendsto_const_nhds
  have hzero :
      Tendsto
        (fun n =>
          inner Complex
            (T.leftVector (a n))
            (T.rightVector (T.rightStar b)))
        atTop
        (nhds 0) := by
    simpa using ha.inner tendsto_const_nhds
  have heq :
      (fun n =>
        inner Complex
          (T.leftVector (T.leftStar (a n)))
          (T.rightVector b)) =
      (fun n =>
        inner Complex
          (T.leftVector (a n))
          (T.rightVector (T.rightStar b))) := by
    funext n
    exact T.pairing (a n) b
  have hzero' :
      Tendsto
        (fun n =>
          inner Complex
            (T.leftVector (T.leftStar (a n)))
            (T.rightVector b))
        atTop
        (nhds 0) := by
    rw [heq]
    exact hzero
  exact tendsto_nhds_unique hz hzero'

theorem graph_closable : IsClosableGraph T.graph := by
  intro z hz
  let closureWitness := mem_closure_iff_seq_limit.mp hz
  let p : Nat -> Prod H H := Classical.choose closureWitness
  have hp : forall n, Set.mem T.graph (p n) :=
    (Classical.choose_spec closureWitness).1
  have hpLim : Tendsto p atTop (nhds (0, z)) :=
    (Classical.choose_spec closureWitness).2
  let a : Nat -> A := fun n => Classical.choose (hp n)
  have hxa : forall n, T.leftVector (a n) = (p n).1 := by
    intro n
    exact (Classical.choose_spec (hp n)).1.symm
  have hya :
      forall n, T.leftVector (T.leftStar (a n)) = (p n).2 := by
    intro n
    exact (Classical.choose_spec (hp n)).2.symm
  apply T.representative_closable a z
  . have hfst : Tendsto (fun n => (p n).1) atTop (nhds 0) :=
      (continuous_fst.tendsto (0, z)).comp hpLim
    simpa only [hxa] using hfst
  . have hsnd : Tendsto (fun n => (p n).2) atTop (nhds z) :=
      (continuous_snd.tendsto (0, z)).comp hpLim
    simpa only [hya] using hsnd

end TomitaGraphCore
end
end KUOS.WORLD
