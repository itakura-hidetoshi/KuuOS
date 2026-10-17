import Kuu.F112.PolygonNativeF55Target

/-!
# F112-E7Q2 / concrete full-phase and charge-only native F55 receivers

E7Q1 reconstructs the historical F56-style *conditional* nine-field
HigherCellTarget on the new, genuinely dependent C60 F45/F54/F55 raw
source. A generic interpreter is now obtained by actual induction
rather than by assuming Gray tricategorical coherence.

This file supplies TWO SEPARATELY CONSTRUCTED conditional targets:
  • signed full-phase target (Int × Int) × ZMod 2;
  • signed integer-charge-only target Int × Int.

Their native generator calibrations match the SHAPES and numerical
values of historical F58 generatorCharge and F59 braidedPhase.
Every raw F55 identity, pentagon, square, inverse, vertical pasting,
left/right context and pre/post route paste has a typed value.

We prove for ALL nine source constructors that:
  1. interpreting into the full target equals E7P3 nativeShadow;
  2. interpreting into the charge-only target equals E7P3 charge;
  3. forgetting the phase of the full target interpretation equals
     the independently defined charge-only target interpretation.
This is a constructor-complete comparison diagram, not a claim that
the independently reconstructed C60 source IS the frozen old F55,
nor a formal transport of historical F68/F77 physical obstructions.

The old F55/F58/F59 modules are NOT imported into KuuOSStrict.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
noncomputable section

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

/-- An independently supplied F56-shaped receiver containing BOTH
signed integer generator charges and an odd ZMod2 exchange phase.
Its source family remains fully indexed by the actual C60 F54 routes. -/
def nativeF55FullShadowTarget (p : Polygon) :
    KuuNativeF55HigherCellTarget p D E where
  Cell := fun {a b} {x y} {n n' m m'} {ma mb} {pa pb}
    {first last} _ _ => KuuNativeF55Shadow
  ident := fun _ => 0
  pentagon := fun _ _ _ _ => (((1 : Int), (0 : Int)), (0 : ZMod 2))
  disjointSquare := fun _ _ => (((0 : Int), (1 : Int)), (1 : ZMod 2))
  symm := fun z => -z
  trans := fun z w => z + w
  leftContext := fun z _ => z
  rightContext := fun _ z => z
  precompose := fun _ z => z
  postcompose := fun z _ => z

/-- A wholly independently specified F58-shaped SIGNED source
receiver, with no phantom exchange phase in the target Type. -/
def nativeF55ChargeTarget (p : Polygon) :
    KuuNativeF55HigherCellTarget p D E where
  Cell := fun {a b} {x y} {n n' m m'} {ma mb} {pa pb}
    {first last} _ _ => Int × Int
  ident := fun _ => (0, 0)
  pentagon := fun _ _ _ _ => (1, 0)
  disjointSquare := fun _ _ => (0, 1)
  symm := fun z => -z
  trans := fun z w => z + w
  leftContext := fun z _ => z
  rightContext := fun _ z => z
  precompose := fun _ z => z
  postcompose := fun z _ => z

/-- All nine raw source constructors interpret into the full-phase
target EXACTLY as the independent E7P3 source-recursive nativeShadow.
This is a real complete-grammar structural compatibility proof. -/
theorem KuuNativeF45Tree.DepthRotationRoute.PresentedCell.interpret_full_eq_shadow
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (cell : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    cell.interpret (nativeF55FullShadowTarget (D := D) (E := E) p) =
      cell.nativeShadow := by
  induction cell with
  | ident _ => rfl
  | pentagon _ _ _ _ => rfl
  | disjointSquare _ _ => rfl
  | symm c ih =>
      change
        -(c.interpret (nativeF55FullShadowTarget (D := D) (E := E) p)) =
          -c.nativeShadow
      rw [ih]
  | trans c d ihc ihd =>
      change
        c.interpret (nativeF55FullShadowTarget (D := D) (E := E) p) +
          d.interpret (nativeF55FullShadowTarget (D := D) (E := E) p) =
          c.nativeShadow + d.nativeShadow
      rw [ihc, ihd]
  | leftContext c later ih => exact ih
  | rightContext earlier c ih => exact ih
  | precompose prior c ih => exact ih
  | postcompose c suffix ih => exact ih

/-- ALL nine independent native source constructors have exactly
the older F58-shaped signed-charge interpretation under the
independently provided Int×Int target, irrespective of phase. -/
theorem KuuNativeF45Tree.DepthRotationRoute.PresentedCell.interpret_charge_eq_shadow_fst
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (cell : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    cell.interpret (nativeF55ChargeTarget (D := D) (E := E) p) =
      cell.nativeShadow.1 := by
  induction cell with
  | ident _ => rfl
  | pentagon _ _ _ _ => rfl
  | disjointSquare _ _ => rfl
  | symm c ih =>
      change
        -(c.interpret (nativeF55ChargeTarget (D := D) (E := E) p)) =
          -c.nativeShadow.1
      rw [ih]
  | trans c d ihc ihd =>
      change
        c.interpret (nativeF55ChargeTarget (D := D) (E := E) p) +
          d.interpret (nativeF55ChargeTarget (D := D) (E := E) p) =
          c.nativeShadow.1 + d.nativeShadow.1
      rw [ihc, ihd]
  | leftContext c later ih => exact ih
  | rightContext earlier c ih => exact ih
  | precompose prior c ih => exact ih
  | postcompose c suffix ih => exact ih

/-- The original F59-to-F58 SIGNED CHARGE OBSERVATION DIAGRAM,
now proved for EVERY nested Type-valued native C60 F55 3-cell:
forgetting phase after full interpretation gives exactly the
independently chosen charge-only target interpretation.
No historical source-isomorphism is asserted. -/
theorem KuuNativeF45Tree.DepthRotationRoute.PresentedCell.interpret_full_forget_phase
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (cell : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    (cell.interpret (nativeF55FullShadowTarget (D := D) (E := E) p)).1 =
      cell.interpret (nativeF55ChargeTarget (D := D) (E := E) p) := by
  calc
    (cell.interpret
        (nativeF55FullShadowTarget (D := D) (E := E) p)).1 =
        cell.nativeShadow.1 :=
      congrArg Prod.fst cell.interpret_full_eq_shadow
    _ = cell.interpret
        (nativeF55ChargeTarget (D := D) (E := E) p) :=
      cell.interpret_charge_eq_shadow_fst.symm

/-- The independently typed native north C60 source pentagon
calibrates the chosen FULL receiver as first generator charge 1. -/
theorem northNativeF55Pentagon_interpret_full :
    northNativeF55PentagonCell.interpret
      (nativeF55FullShadowTarget
        (D := Site) (E := Site) (.pentagon .north)) =
          (((1 : Int), (0 : Int)), (0 : ZMod 2)) := rfl

/-- The independently typed original-shaped top C60 hexagon
disjoint square has odd phase and signed second generator charge. -/
theorem northHexagonNativeF55Square_interpret_full :
    northHexagonNativeF55SquareCell.interpret
      (nativeF55FullShadowTarget
        (D := Site) (E := Site) (.hexagon (.top 0))) =
          (((0 : Int), (1 : Int)), (1 : ZMod 2)) := rfl

/-- The new universal receiver's full shadow interpretation
AGREES with E7P4's explicitly related raw-cell quotient evaluator
on ACTUAL arrows generated from specific native F55 proof trees. -/
theorem nativeF55ThreeEval_eq_interpret_full
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (cell : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    nativeF55ThreeEval (nativeF55ThreeOf cell) =
      cell.interpret (nativeF55FullShadowTarget (D := D) (E := E) p) := by
  rw [nativeF55ThreeEval_of, cell.interpret_full_eq_shadow]

#print axioms nativeF55FullShadowTarget
#print axioms nativeF55ChargeTarget
#print axioms KuuNativeF45Tree.DepthRotationRoute.PresentedCell.interpret_full_eq_shadow
#print axioms KuuNativeF45Tree.DepthRotationRoute.PresentedCell.interpret_charge_eq_shadow_fst
#print axioms KuuNativeF45Tree.DepthRotationRoute.PresentedCell.interpret_full_forget_phase
#print axioms northNativeF55Pentagon_interpret_full
#print axioms northHexagonNativeF55Square_interpret_full
#print axioms nativeF55ThreeEval_eq_interpret_full
end
end Kuu.F112.Physical
