import KUOS.DependentOriginationGrayC60IntegralChainComplexV5_160
import Mathlib.Algebra.Homology.HomologicalComplex
import Mathlib.Algebra.Category.ModuleCat.Basic

namespace KUOS.DependentOriginationGrayC60NativeChainComplexV5_160

open CategoryTheory
open KUOS.DependentOriginationGrayC60IntegralBoundaryLinearMapV5_159
open KUOS.DependentOriginationGrayC60IntegralChainComplexV5_160

set_option autoImplicit false
noncomputable section

/-!
# F59-F11 / v5.160: native mathlib ChainComplex of actual C60 surface

F59-F10 proved a genuine oriented integer cellular complex:
32 original pentagon/hexagon faces, 90 physical edges, 60 dart
vertices, with Z-linear d₂, d₁, and d₁ comp d₂ = zero.
Here build an actual Mathlib ChainComplex (ModuleCat Z) Nat,
not merely an unbundled pair of composable maps.

Degrees 0, 1, 2 are the original Finsupp free integer modules.
Every higher chain group is the ZERO object. Differential in degree
1 is EXACTLY the verified d₁ and degree 2 is EXACTLY d₂.
No three-dimensional C60 cells are postulated, and no global
source F55 Gray 3-functor or Stage-II omega equality is asserted.
-/

/-- Native integer modules in degrees 0, 1, 2, and the zero
object in every degree 3 and above. -/
def c60NativeChainObjects : ℕ → ModuleCat ℤ
  | 0 => ModuleCat.of ℤ C60IntegralZeroChains
  | 1 => ModuleCat.of ℤ C60IntegralOneChains
  | 2 => ModuleCat.of ℤ C60IntegralTwoChains
  | _ + 3 => ModuleCat.of ℤ PUnit

/-- Native ModuleCat differentials induced by the exact original
C60 signed integer cellular face-edge-vertex maps. -/
def c60NativeChainDifferential :
    ∀ n : ℕ, c60NativeChainObjects (n + 1) ⟶
      c60NativeChainObjects n
  | 0 => ModuleCat.ofHom c60IntegralBoundaryOne
  | 1 => ModuleCat.ofHom c60IntegralBoundaryTwo
  | _ + 2 => 0

/-- The complete native categorical square-zero law at EVERY
degree, not only on the fundamental face cycle. -/
theorem c60NativeChainDifferential_comp_zero
    (n : ℕ) :
    c60NativeChainDifferential (n + 1) ≫
      c60NativeChainDifferential n = 0 := by
  cases n with
  | zero =>
      apply ModuleCat.hom_ext
      exact c60IntegralBoundaryOne_comp_boundaryTwo_zero
  | succ n =>
      cases n <;> simp [c60NativeChainDifferential]

/-- Actual Mathlib chain-complex API object, with the original
finite combinatorial C60 source as its underlying chain groups. -/
def c60NativeIntegralCellularComplex :
    ChainComplex (ModuleCat ℤ) ℕ :=
  ChainComplex.of c60NativeChainObjects
    c60NativeChainDifferential
    c60NativeChainDifferential_comp_zero

theorem c60NativeIntegralCellularComplex_X0 :
    c60NativeIntegralCellularComplex.X 0 =
      ModuleCat.of ℤ C60IntegralZeroChains := rfl

theorem c60NativeIntegralCellularComplex_X1 :
    c60NativeIntegralCellularComplex.X 1 =
      ModuleCat.of ℤ C60IntegralOneChains := rfl

theorem c60NativeIntegralCellularComplex_X2 :
    c60NativeIntegralCellularComplex.X 2 =
      ModuleCat.of ℤ C60IntegralTwoChains := rfl

theorem c60NativeIntegralCellularComplex_X3 :
    c60NativeIntegralCellularComplex.X 3 = ModuleCat.of ℤ PUnit := rfl

/-- Native first differential exactly recovers physical d₁. -/
theorem c60NativeIntegralCellularComplex_d10 :
    c60NativeIntegralCellularComplex.d 1 0 =
      ModuleCat.ofHom c60IntegralBoundaryOne := by
  exact ChainComplex.of_d c60NativeChainObjects
    c60NativeChainDifferential c60NativeChainDifferential_comp_zero 0

/-- Native second differential exactly recovers physical d₂. -/
theorem c60NativeIntegralCellularComplex_d21 :
    c60NativeIntegralCellularComplex.d 2 1 =
      ModuleCat.ofHom c60IntegralBoundaryTwo := by
  exact ChainComplex.of_d c60NativeChainObjects
    c60NativeChainDifferential c60NativeChainDifferential_comp_zero 1

/-- No nonzero differential from dimension three to two. -/
theorem c60NativeIntegralCellularComplex_d32 :
    c60NativeIntegralCellularComplex.d 3 2 = 0 := by
  exact ChainComplex.of_d c60NativeChainObjects
    c60NativeChainDifferential c60NativeChainDifferential_comp_zero 2

/-- Genuine bundled native mathematical chain-complex law. -/
theorem c60NativeIntegralCellularComplex_d21_d10 :
    c60NativeIntegralCellularComplex.d 2 1 ≫
      c60NativeIntegralCellularComplex.d 1 0 = 0 :=
  c60NativeIntegralCellularComplex.d_comp_d 2 1 0

#print axioms c60NativeChainObjects
#print axioms c60NativeChainDifferential
#print axioms c60NativeChainDifferential_comp_zero
#print axioms c60NativeIntegralCellularComplex
#print axioms c60NativeIntegralCellularComplex_X0
#print axioms c60NativeIntegralCellularComplex_X1
#print axioms c60NativeIntegralCellularComplex_X2
#print axioms c60NativeIntegralCellularComplex_X3
#print axioms c60NativeIntegralCellularComplex_d10
#print axioms c60NativeIntegralCellularComplex_d21
#print axioms c60NativeIntegralCellularComplex_d32
#print axioms c60NativeIntegralCellularComplex_d21_d10

end
end KUOS.DependentOriginationGrayC60NativeChainComplexV5_160
