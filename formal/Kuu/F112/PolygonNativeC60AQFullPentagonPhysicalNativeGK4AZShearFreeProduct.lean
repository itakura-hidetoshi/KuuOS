import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4AYShearPingPong
import Mathlib.GroupTheory.CoprodI
import Mathlib.Tactic

/-!
F112-P94D3GK4AZ — the true Sanov free-product ping-pong action,
without assuming a new free-group axiom.

Using ONLY fixed mathlib Monoid.CoprodI.lift_injective_of_ping_pong
and the integer cone inequalities Lean-proved in GK4AY, we show that
the two separate additive Z one-parameter shear families produce
a faithful action of the FREE PRODUCT of two infinite cyclic groups
on Z². Their generators are conjugate (by (u,v) ↦ (2u,v)) to
the genuinely evaluated KuuOS original F54 C and R(4).

This is a theorem about explicit integer permutations and free product.
Transfer to the full original F54 dependent polynomial observer,
including C,F=C⁻¹,R(X), is a further task. The full "t=4 determines
all polynomial histories" claim is not assumed.
No Type-valued comparison cells are created from observation equality.
Append-only/tighten-only/root107. Lean 4.30.0-rc2, pinned mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6; preserve #1558.
Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
open Cardinal
open scoped Function Pointwise
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

/-- Upper shear as a group homomorphism from additive integers,
written multiplicatively, into integer permutations. -/
def nativeGK4AZUpperHom : Multiplicative Int →* Equiv.Perm (Int × Int) where
  toFun h := nativeGK4AYUpperPerm (Multiplicative.toAdd h)
  map_one' := by
    apply Equiv.ext
    intro z
    change nativeGK4AYUpperShear 0 z = z
    exact nativeGK4AYUpperShear_zero z
  map_mul' a b := by
    apply Equiv.ext
    intro z
    change nativeGK4AYUpperShear
      (Multiplicative.toAdd a + Multiplicative.toAdd b) z =
      nativeGK4AYUpperShear (Multiplicative.toAdd a)
        (nativeGK4AYUpperShear (Multiplicative.toAdd b) z)
    exact (nativeGK4AYUpperShear_add _ _ z).symm

/-- Lower shear as a SECOND genuinely independent cyclic group action. -/
def nativeGK4AZLowerHom : Multiplicative Int →* Equiv.Perm (Int × Int) where
  toFun h := nativeGK4AYLowerPerm (Multiplicative.toAdd h)
  map_one' := by
    apply Equiv.ext
    intro z
    change nativeGK4AYLowerShear 0 z = z
    exact nativeGK4AYLowerShear_zero z
  map_mul' a b := by
    apply Equiv.ext
    intro z
    change nativeGK4AYLowerShear
      (Multiplicative.toAdd a + Multiplicative.toAdd b) z =
      nativeGK4AYLowerShear (Multiplicative.toAdd a)
        (nativeGK4AYLowerShear (Multiplicative.toAdd b) z)
    exact (nativeGK4AYLowerShear_add _ _ z).symm

/-- The two independent cyclic factors are indexed by Bool. -/
def nativeGK4AZFactors (i : Bool) :
    Multiplicative Int →* Equiv.Perm (Int × Int) :=
  if i then nativeGK4AZLowerHom else nativeGK4AZUpperHom

/-- The two disjoint nonempty strict cones are indexed by the
very SAME generator label as the corresponding cyclic factor. -/
def nativeGK4AZCones (i : Bool) : Set (Int × Int) :=
  if i then {z | nativeGK4AYVertical z}
  else {z | nativeGK4AYHorizontal z}

theorem nativeGK4AZCones_nonempty :
    ∀ i : Bool, (nativeGK4AZCones i).Nonempty := by
  intro i
  cases i
  · exact nativeGK4AYHorizontal_nonempty
  · exact nativeGK4AYVertical_nonempty

theorem nativeGK4AZCones_pairwise_disjoint :
    Pairwise (Disjoint on nativeGK4AZCones) := by
  intro i j hij
  cases i <;> cases j
  · exact (hij rfl).elim
  · apply Set.disjoint_left.mpr
    intro z hz hv
    exact nativeGK4AYCones_disjoint z hz hv
  · apply Set.disjoint_left.mpr
    intro z hz hv
    exact nativeGK4AYCones_disjoint z hv hz
  · exact (hij rfl).elim

/-- The infinite cyclic group contains at least 3 elements, supplying
the nondegenerate cardinality hypothesis of the pinned ping-pong lemma. -/
theorem nativeGK4AZCyclic_card_three :
    (3 : Cardinal) ≤ #(Multiplicative Int) := by
  have hf : Function.Injective
      (fun i : Fin 3 => Multiplicative.ofAdd (i.val : Int)) := by
    intro i j hij
    apply Fin.ext
    have h : (i.val : Int) = (j.val : Int) :=
      congrArg Multiplicative.toAdd hij
    exact_mod_cast h
  simpa using (Cardinal.mk_le_of_injective hf)

/-- The genuine all-nonzero-integer-power set inclusion hypothesis:
a cyclic factor maps the OTHER strict cone into its OWN cone. -/
theorem nativeGK4AZPingPong :
    Pairwise (fun i j : Bool =>
      ∀ (h : Multiplicative Int), h ≠ 1 →
        (nativeGK4AZFactors i h) • nativeGK4AZCones j ⊆
          nativeGK4AZCones i) := by
  intro i j hij h hh z hz
  have hn : Multiplicative.toAdd h ≠ 0 := by
    change Multiplicative.toAdd h ≠ 0 at hh
    exact hh
  have hz' : (nativeGK4AZFactors i h)⁻¹ • z ∈ nativeGK4AZCones j :=
    (Set.mem_smul_set_iff_inv_smul_mem).mp hz
  cases i <;> cases j
  · exact (hij rfl).elim
  ·
    change nativeGK4AYVertical ((nativeGK4AZUpperHom h)⁻¹ • z) at hz'
    have hs := nativeGK4AYUpper_maps_vertical
      (Multiplicative.toAdd h) hn
      ((nativeGK4AZUpperHom h)⁻¹ • z) hz'
    change nativeGK4AYHorizontal
      ((nativeGK4AZUpperHom h) • ((nativeGK4AZUpperHom h)⁻¹ • z)) at hs
    have hr : (nativeGK4AZUpperHom h) •
      ((nativeGK4AZUpperHom h)⁻¹ • z) = z := by simp
    rw [hr] at hs
    exact hs
  ·
    change nativeGK4AYHorizontal ((nativeGK4AZLowerHom h)⁻¹ • z) at hz'
    have hs := nativeGK4AYLower_maps_horizontal
      (Multiplicative.toAdd h) hn
      ((nativeGK4AZLowerHom h)⁻¹ • z) hz'
    change nativeGK4AYVertical
      ((nativeGK4AZLowerHom h) • ((nativeGK4AZLowerHom h)⁻¹ • z)) at hs
    have hr : (nativeGK4AZLowerHom h) •
      ((nativeGK4AZLowerHom h)⁻¹ • z) = z := by simp
    rw [hr] at hs
    exact hs
  · exact (hij rfl).elim

/-- Formal Sanov free-product theorem for the EXACT integral shears:
Z * Z injects into Perm(Z²), proved from the pinned mathlib theorem. -/
theorem nativeGK4AZFreeProduct_injective :
    Function.Injective
      (Monoid.CoprodI.lift nativeGK4AZFactors :
        Monoid.CoprodI (fun _ : Bool => Multiplicative Int) →
          Equiv.Perm (Int × Int)) := by
  exact Monoid.CoprodI.lift_injective_of_ping_pong
    nativeGK4AZFactors
    (Or.inr ⟨false, nativeGK4AZCyclic_card_three⟩)
    nativeGK4AZCones nativeGK4AZCones_nonempty
    nativeGK4AZCones_pairwise_disjoint nativeGK4AZPingPong

#print axioms nativeGK4AZUpperHom
#print axioms nativeGK4AZLowerHom
#print axioms nativeGK4AZFactors
#print axioms nativeGK4AZCones
#print axioms nativeGK4AZCones_nonempty
#print axioms nativeGK4AZCones_pairwise_disjoint
#print axioms nativeGK4AZCyclic_card_three
#print axioms nativeGK4AZPingPong
#print axioms nativeGK4AZFreeProduct_injective

end
end Kuu.F112.Physical
