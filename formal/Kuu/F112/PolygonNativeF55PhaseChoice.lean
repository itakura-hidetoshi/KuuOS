import Kuu.F112.PolygonNativeF55ChargeRigidity

/-!
# F112-E7Q4 / odd exchange phase is EXTRA target data, not forced by F55 syntax

E7Q3 proves that the CHOSEN E7P3 odd-square-phase shadow satisfies
phase = square charge mod 2 on every native free F55 cell, hence its
full-shadow quotient loses no more information than the integer-charge
quotient. This does not make odd phase intrinsic to the F55 free
presentation: the native F56-shaped target interface only requires
that pentagon/square values and nine operations be SUPPLIED.

We construct a SECOND fully typed F56-shaped target with exactly the
SAME (Int × Int) signed pentagon/square charges and all the SAME
additive/contextual operations, but TRIVIAL ZMod2 exchange phase.

We then prove by induction over ALL NINE source constructors that
the even-phase target agrees on the signed charges of every raw
F55 source cell, while the concrete six-sector C60 square has phase
ZERO there but phase ONE in the independently odd-calibrated target.

This is an explicit, formal source-level NON-UNIQUENESS theorem:
native F54/F55 syntax and signed charges ALONE cannot force the
historical F59 odd-odd braided exchange calibration. A genuine
historical braided-source receiver and a type-faithful old/new
comparison are necessary before transporting F68/F77 obstructions.

No KUOS/Gray/F51/F77 imports and no axioms or sorry.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
noncomputable section

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

/-- A fully typed NINE-operation higher-cell target, separately
supplied just like E7Q2's odd target, with IDENTICAL signed charges
and ZERO exchange phase at BOTH generators. No raw source 3-cell
is identified with a Prop or created from numerical grade equality. -/
def nativeF55EvenPhaseTarget (p : Polygon) :
    KuuNativeF55HigherCellTarget p D E where
  Cell := fun {a b} {x y} {n n' m m'} {ma mb} {pa pb}
    {first last} _ _ => KuuNativeF55Shadow
  ident := fun _ => 0
  pentagon := fun _ _ _ _ => (((1 : Int), (0 : Int)), (0 : ZMod 2))
  disjointSquare := fun _ _ => (((0 : Int), (1 : Int)), (0 : ZMod 2))
  symm := fun z => -z
  trans := fun z w => z + w
  leftContext := fun z _ => z
  rightContext := by
    intros
    assumption
  precompose := by
    intros
    assumption
  postcompose := fun z _ => z

/-- Induction over ALL NINE free native F55 constructors: the
independently calibrated zero-phase target retains EXACTLY the
same signed charge as E7P3 nativeShadow while killing ONLY phase.
Crucially this does not identify or erase raw proof objects. -/
theorem KuuNativeF45Tree.DepthRotationRoute.PresentedCell.interpret_evenPhase_eq_charge_zero
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (cell : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    cell.interpret (nativeF55EvenPhaseTarget (D := D) (E := E) p) =
      (cell.nativeShadow.1, (0 : ZMod 2)) := by
  induction cell with
  | ident _ => rfl
  | pentagon _ _ _ _ => rfl
  | disjointSquare _ _ => rfl
  | symm c ih =>
      change
        (nativeF55EvenPhaseTarget (D := D) (E := E) p).symm
          (c.interpret (nativeF55EvenPhaseTarget (D := D) (E := E) p)) =
          (-c.nativeShadow.1, (0 : ZMod 2))
      rw [ih]
      simp [nativeF55EvenPhaseTarget]
  | trans c d ihc ihd =>
      change
        (nativeF55EvenPhaseTarget (D := D) (E := E) p).trans
          (c.interpret (nativeF55EvenPhaseTarget (D := D) (E := E) p))
          (d.interpret (nativeF55EvenPhaseTarget (D := D) (E := E) p)) =
          (c.nativeShadow.1 + d.nativeShadow.1, (0 : ZMod 2))
      rw [ihc, ihd]
      simp [nativeF55EvenPhaseTarget]
  | leftContext c later ih => exact ih
  | rightContext earlier c ih => exact ih
  | precompose prior c ih => exact ih
  | postcompose c suffix ih => exact ih

/-- The even-phase target's ZMod2 phase is ZERO for ANY native F55
raw 3-cell, including arbitrary inversions and nested pastings. -/
theorem KuuNativeF45Tree.DepthRotationRoute.PresentedCell.interpret_evenPhase_zero
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (cell : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    (cell.interpret (nativeF55EvenPhaseTarget (D := D) (E := E) p)).2 =
      (0 : ZMod 2) := by
  rw [cell.interpret_evenPhase_eq_charge_zero]

/-- Signed F58-shaped charges agree for ALL nine raw constructors
between the separately chosen odd-phase and zero-phase recipients.
Thus no charge-only observation can resolve the two targets. -/
theorem KuuNativeF45Tree.DepthRotationRoute.PresentedCell.interpret_evenPhase_charge_eq_full
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (cell : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    (cell.interpret
      (nativeF55EvenPhaseTarget (D := D) (E := E) p)).1 =
    (cell.interpret
      (nativeF55FullShadowTarget (D := D) (E := E) p)).1 := by
  calc
    (cell.interpret
      (nativeF55EvenPhaseTarget (D := D) (E := E) p)).1 =
      cell.nativeShadow.1 := by
        rw [cell.interpret_evenPhase_eq_charge_zero]
    _ = (cell.interpret
      (nativeF55FullShadowTarget (D := D) (E := E) p)).1 :=
        (congrArg Prod.fst cell.interpret_full_eq_shadow).symm

/-- NONTRIVIAL geometry-independent CALIBRATION CHOICE on an ACTUAL
C60 six-sector native F55 square: the two conditional recipients
assign equal (0,1) signed charges but DIFFERENT ZMod2 exchange phases.
This proves odd braided exchange is NOT forced by free source syntax. -/
theorem northHexagonNativeF55Square_phase_not_forced_by_charge :
    (northHexagonNativeF55SquareCell.interpret
      (nativeF55EvenPhaseTarget
        (D := Site) (E := Site) (.hexagon (.top 0)))).1 =
    (northHexagonNativeF55SquareCell.interpret
      (nativeF55FullShadowTarget
        (D := Site) (E := Site) (.hexagon (.top 0)))).1 ∧
    (northHexagonNativeF55SquareCell.interpret
      (nativeF55EvenPhaseTarget
        (D := Site) (E := Site) (.hexagon (.top 0)))).2 ≠
    (northHexagonNativeF55SquareCell.interpret
      (nativeF55FullShadowTarget
        (D := Site) (E := Site) (.hexagon (.top 0)))).2 := by
  constructor
  · exact northHexagonNativeF55SquareCell.interpret_evenPhase_charge_eq_full
  · have hEven :=
      northHexagonNativeF55SquareCell.interpret_evenPhase_zero
    have hOdd := congrArg Prod.snd
      northHexagonNativeF55Square_interpret_full
    rw [hEven, hOdd]
    decide

#print axioms nativeF55EvenPhaseTarget
#print axioms KuuNativeF45Tree.DepthRotationRoute.PresentedCell.interpret_evenPhase_eq_charge_zero
#print axioms KuuNativeF45Tree.DepthRotationRoute.PresentedCell.interpret_evenPhase_zero
#print axioms KuuNativeF45Tree.DepthRotationRoute.PresentedCell.interpret_evenPhase_charge_eq_full
#print axioms northHexagonNativeF55Square_phase_not_forced_by_charge
end
end Kuu.F112.Physical
