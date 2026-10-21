import Kuu.F112.PolygonNativeF55FunctorCells
import Kuu.F112.PolygonNativeF55PhaseChoice

/-!
# F112-E7Q5-F2 — F55 functor comparison and independent receiver descent

E7Q5-F1 builds an actual NINE-CONSTRUCTOR proof-relevant F55 source
transport PROVIDED a separately supplied mapped pentagon witness with
RAW pentagon shape. The raw constructor shape itself forces canonical
(1,0;0) signed charge/phase: numeric calibration is not assumed.

Here we prove the interpret-then-transport / transport-then-interpret
commuting square for each of THREE independently defined F56-shaped
recipients:
  1. full chosen odd-phase native shadow (Int × Int) × ZMod 2;
  2. signed generator-charge-only recipient Int × Int;
  3. independent even-phase recipient (Int × Int) × ZMod 2.

All identities hold for ALL NINE freely presented native 3-cell
constructors and both arbitrary category functors. On the ACTUAL
original top C60 hexagon, equal signed integer charges but different
odd/even exchange phase remain distinguishable AFTER any such functor
transport.

This does not prove the pentagon lift data exists unconditionally,
nor recover historical F59 Gray braiding or F68/F77 nonreconstruction.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
noncomputable section

universe uA vA uB vB uA₂ vA₂ uB₂ vB₂
variable {A : Type uA} [Category.{vA} A]
variable {B : Type uB} [Category.{vB} B]
variable {A₂ : Type uA₂} [Category.{vA₂} A₂]
variable {B₂ : Type uB₂} [Category.{vB₂} B₂]

/-- FULL shadow receiver naturality, on the actual independent raw
F55 source and an independently supplied typed pentagon lifting. -/
theorem KuuNativeF45Tree.DepthRotationRoute.PresentedCell.interpret_full_mapAxesGivenPentagon
    (F : A ⥤ A₂) (G : B ⥤ B₂)
    (data : KuuNativeF55MappedPentagonData F G)
    {p : Polygon} {a b : A} {x y : B}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (cell : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    (cell.mapAxesGivenPentagon F G data).interpret
      (nativeF55FullShadowTarget (D := A₂) (E := B₂) p) =
    cell.interpret
      (nativeF55FullShadowTarget (D := A) (E := B) p) := by
  rw [(cell.mapAxesGivenPentagon F G data).interpret_full_eq_shadow,
    cell.interpret_full_eq_shadow,
    cell.nativeShadow_mapAxesGivenPentagon F G data]

/-- Integer-charge-only target naturality is separately verified,
not inferred from claiming an unproved old F58 source equivalence. -/
theorem KuuNativeF45Tree.DepthRotationRoute.PresentedCell.interpret_charge_mapAxesGivenPentagon
    (F : A ⥤ A₂) (G : B ⥤ B₂)
    (data : KuuNativeF55MappedPentagonData F G)
    {p : Polygon} {a b : A} {x y : B}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (cell : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    (cell.mapAxesGivenPentagon F G data).interpret
      (nativeF55ChargeTarget (D := A₂) (E := B₂) p) =
    cell.interpret (nativeF55ChargeTarget (D := A) (E := B) p) := by
  rw [(cell.mapAxesGivenPentagon F G data).interpret_charge_eq_shadow_fst,
    cell.interpret_charge_eq_shadow_fst,
    cell.charge_mapAxesGivenPentagon F G data]

/-- EVEN-phase calibration also commutes with all nine constructors.
This is NOT the claim that the even target equals the odd target:
they are still different recipients with the SAME signed charges. -/
theorem KuuNativeF45Tree.DepthRotationRoute.PresentedCell.interpret_evenPhase_mapAxesGivenPentagon
    (F : A ⥤ A₂) (G : B ⥤ B₂)
    (data : KuuNativeF55MappedPentagonData F G)
    {p : Polygon} {a b : A} {x y : B}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (cell : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    (cell.mapAxesGivenPentagon F G data).interpret
      (nativeF55EvenPhaseTarget (D := A₂) (E := B₂) p) =
    cell.interpret
      (nativeF55EvenPhaseTarget (D := A) (E := B) p) := by
  rw [(cell.mapAxesGivenPentagon F G data).interpret_evenPhase_eq_charge_zero,
    cell.interpret_evenPhase_eq_charge_zero,
    cell.charge_mapAxesGivenPentagon F G data]

/-- TRUE top C60 six-sector F55 square: even and odd recipients
AGREE in both signed integer charges, but DIFFER in exchange phase
even after any two chosen functors. The pentagon certificate is used
only to define the whole raw source map, not to invent this square. -/
theorem northHexagonNativeF55Square_mapAxes_phase_choice
    (F : Site ⥤ A₂) (G : Site ⥤ B₂)
    (data : KuuNativeF55MappedPentagonData F G) :
    let mapped := northHexagonNativeF55SquareCell.mapAxesGivenPentagon F G data
    (mapped.interpret
      (nativeF55EvenPhaseTarget (D := A₂) (E := B₂)
        (.hexagon (.top 0)))).1 =
    (mapped.interpret
      (nativeF55FullShadowTarget (D := A₂) (E := B₂)
        (.hexagon (.top 0)))).1 ∧
    (mapped.interpret
      (nativeF55EvenPhaseTarget (D := A₂) (E := B₂)
        (.hexagon (.top 0)))).2 ≠
    (mapped.interpret
      (nativeF55FullShadowTarget (D := A₂) (E := B₂)
        (.hexagon (.top 0)))).2 := by
  dsimp
  constructor
  · exact (northHexagonNativeF55SquareCell.mapAxesGivenPentagon F G data).interpret_evenPhase_charge_eq_full
  · have hEven :=
      (northHexagonNativeF55SquareCell.mapAxesGivenPentagon F G data).interpret_evenPhase_zero
    have hOdd :
        ((northHexagonNativeF55SquareCell.mapAxesGivenPentagon F G data).interpret
          (nativeF55FullShadowTarget (D := A₂) (E := B₂)
            (.hexagon (.top 0)))).2 = (1 : ZMod 2) := by
      rw [(northHexagonNativeF55SquareCell.mapAxesGivenPentagon F G data).interpret_full_eq_shadow]
      rw [northHexagonNativeF55SquareCell.nativeShadow_mapAxesGivenPentagon F G data]
      rw [northHexagonNativeF55SquareCell_shadow]
    rw [hEven, hOdd]
    decide

#print axioms KuuNativeF45Tree.DepthRotationRoute.PresentedCell.interpret_full_mapAxesGivenPentagon
#print axioms KuuNativeF45Tree.DepthRotationRoute.PresentedCell.interpret_charge_mapAxesGivenPentagon
#print axioms KuuNativeF45Tree.DepthRotationRoute.PresentedCell.interpret_evenPhase_mapAxesGivenPentagon
#print axioms northHexagonNativeF55Square_mapAxes_phase_choice
end
end Kuu.F112.Physical
