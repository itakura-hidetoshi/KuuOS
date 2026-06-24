import Mathlib

/-!
WORLD v0.57 algebraic Tomita orbit core.

This Mathlib-only module proves the first foundational step beneath the standard
form receipts.  Given an injective cyclic-orbit map and an involutive star on the
algebra carrier, the Tomita operation on represented orbit vectors is
well-defined, unique, and involutive.

No closability, polar decomposition, modular operator, or analytic standard-form
theorem is asserted here.
-/

namespace KUOS
namespace WORLD

noncomputable section

structure AlgebraicTomitaOrbitCore where
  AlgebraCarrier : Type
  HilbertCarrier : Type
  starOp : AlgebraCarrier → AlgebraCarrier
  star_involutive : Function.Involutive starOp
  orbit : AlgebraCarrier → HilbertCarrier
  orbit_injective : Function.Injective orbit

namespace AlgebraicTomitaOrbitCore

variable (T : AlgebraicTomitaOrbitCore)

/-- The represented cyclic orbit, as an actual subtype of the carrier. -/
def Orbit : Type := Set.range T.orbit

/-- Canonical orbit point represented by an algebra element. -/
def orbitPoint (a : T.AlgebraCarrier) : T.Orbit :=
  ⟨T.orbit a, ⟨a, rfl⟩⟩

/-- The unique algebra source of a represented orbit point. -/
noncomputable def source (x : T.Orbit) : T.AlgebraCarrier :=
  Classical.choose x.property

theorem orbit_source (x : T.Orbit) :
    T.orbit (T.source x) = x.1 :=
  Classical.choose_spec x.property

@[simp] theorem source_orbitPoint (a : T.AlgebraCarrier) :
    T.source (T.orbitPoint a) = a := by
  apply T.orbit_injective
  exact T.orbit_source (T.orbitPoint a)

@[simp] theorem orbitPoint_source (x : T.Orbit) :
    T.orbitPoint (T.source x) = x := by
  apply Subtype.ext
  exact T.orbit_source x

/-- The algebraic Tomita operation on the represented cyclic orbit. -/
noncomputable def tomita (x : T.Orbit) : T.Orbit :=
  T.orbitPoint (T.starOp (T.source x))

@[simp] theorem tomita_orbitPoint (a : T.AlgebraCarrier) :
    T.tomita (T.orbitPoint a) = T.orbitPoint (T.starOp a) := by
  unfold tomita
  rw [T.source_orbitPoint]

/-- The algebraic Tomita operation squares to the identity on its orbit core. -/
theorem tomita_involutive : Function.Involutive T.tomita := by
  intro x
  calc
    T.tomita (T.tomita x) =
        T.tomita (T.tomita (T.orbitPoint (T.source x))) := by
          rw [T.orbitPoint_source x]
    _ = T.orbitPoint (T.starOp (T.starOp (T.source x))) := by
          rw [T.tomita_orbitPoint, T.tomita_orbitPoint]
    _ = T.orbitPoint (T.source x) := by
          rw [T.star_involutive]
    _ = x := T.orbitPoint_source x

@[simp] theorem tomita_sq (x : T.Orbit) :
    T.tomita (T.tomita x) = x :=
  T.tomita_involutive x

/-- Any orbit operation satisfying the defining star rule equals `tomita`. -/
theorem tomita_unique
    (S : T.Orbit → T.Orbit)
    (hS : ∀ a, S (T.orbitPoint a) = T.orbitPoint (T.starOp a)) :
    S = T.tomita := by
  funext x
  calc
    S x = S (T.orbitPoint (T.source x)) := by
      rw [T.orbitPoint_source x]
    _ = T.orbitPoint (T.starOp (T.source x)) := hS (T.source x)
    _ = T.tomita x := rfl

/-- Separation makes the algebraic Tomita image independent of representatives. -/
theorem tomita_well_defined
    {a b : T.AlgebraCarrier}
    (hab : T.orbit a = T.orbit b) :
    T.orbit (T.starOp a) = T.orbit (T.starOp b) := by
  have h : a = b := T.orbit_injective hab
  rw [h]

end AlgebraicTomitaOrbitCore
end
end WORLD
end KUOS
