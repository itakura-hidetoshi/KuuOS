import Kuu.F112.PolygonNativeF55Receivers

/-!
# F112-E7Q3 / exact charge rigidity and raw-source nonfaithfulness

E7P3 proves by induction on all nine native F55 free 3-cell
constructors that the chosen ZMod2 phase equals the second signed
integer charge modulo 2. E7P4 therefore retains phase as an explicit
COORDINATE, but this does NOT make that coordinate algebraically
independent on the IMAGE of this calibrated raw source interpreter.

We rigorously establish the resulting exact no-go:
  • equality of complete chosen (Int×Int)×ZMod2 shadows is
    EQUIVALENT to equality of the two signed integer charges;
  • the charge projection is already INJECTIVE on E7P4's particular
    full-shadow quotient 3-Hom.
Thus this chosen E7P4 quotient alone CANNOT detect any extra phase
distinguishing raw words of identical integer charge.

Separately, an actual north C60 F55 pentagon raw 3-cell and the
same raw cell pasted with an identity are PROVED DISTINCT source
terms but are equal in the full-shadow quotient. This certifies
the exact proof-relevance lost by the particular quotient.

These are important limitations, not old historical F55/F77
obstructions: an independent geometric braid-phase calibration or
a richer receiver is required before claiming original F59/F77
phase nonrestoration from source category equivalence.

No Gray/legacy import, new axioms, sorry, or admit.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
noncomputable section

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

/-- For any two GENUINELY PARALLEL original-shaped F55 raw
3-cells, full shadow equality is EXACTLY equivalent to equality
of their two signed integer charges. The allegedly separate
ZMod2 coordinate is parity-locked on this source image. -/
theorem nativeF55ShadowRel_iff_charge_eq
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
    (c d : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v) :
    nativeF55ShadowRel c d ↔ c.nativeShadow.1 = d.nativeShadow.1 := by
  change (c.nativeShadow = d.nativeShadow) ↔
    (c.nativeShadow.1 = d.nativeShadow.1)
  constructor
  · intro h
    exact congrArg Prod.fst h
  · intro h
    apply Prod.ext
    · exact h
    · calc
        c.nativeShadow.2 =
            ((c.nativeShadow.1.2 : Int) : ZMod 2) :=
          c.phase_squareParity.symm
        _ = ((d.nativeShadow.1.2 : Int) : ZMod 2) := by rw [h]
        _ = d.nativeShadow.2 := d.phase_squareParity

/-- Every actually represented E7P4 quotient 3-Hom has phase
LOCKED by the parity of its second signed integer charge.
The proof is quotient induction on genuine nine-constructor terms. -/
theorem NativeF55ThreeHom.phase_squareParity
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55ThreeHom u v) :
    (((nativeF55ThreeEval f).1.2 : Int) : ZMod 2) =
      (nativeF55ThreeEval f).2 := by
  refine Quot.inductionOn f (fun raw => ?_)
  exact raw.phase_squareParity

/-- Strengthening of E7P4: on each actual typed higher-Hom,
the two signed integer charges ALONE are already a faithful
observer. The extra phase coordinate does not refine this
PARTICULAR parity-calibrated quotient. -/
theorem nativeF55ThreeEval_charge_injective
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55ThreeHom u v}
    (h : (nativeF55ThreeEval f).1 = (nativeF55ThreeEval g).1) :
    f = g := by
  apply nativeF55ThreeEval_injective
  apply Prod.ext
  · exact h
  · calc
      (nativeF55ThreeEval f).2 =
          (((nativeF55ThreeEval f).1.2 : Int) : ZMod 2) :=
        (NativeF55ThreeHom.phase_squareParity f).symm
      _ = (((nativeF55ThreeEval g).1.2 : Int) : ZMod 2) := by rw [h]
      _ = (nativeF55ThreeEval g).2 :=
        NativeF55ThreeHom.phase_squareParity g

/-- The native F55 source still contains the ENTIRE raw proof tree;
pasting a right unit is syntactically observable even though its
chosen additive full-shadow value remains the same. -/
def northNativeF55PentagonWithUnit :
    KuuNativeF45Tree.DepthRotationRoute.PresentedCell (.pentagon .north)
      northNativeF45PentagonLong northNativeF45PentagonShort :=
  .trans northNativeF55PentagonCell
    (.ident northNativeF45PentagonShort)

theorem northNativeF55PentagonWithUnit_raw_ne :
    northNativeF55PentagonCell ≠ northNativeF55PentagonWithUnit :=
  northNativeF55PentagonCell_ne_withUnit

/-- The SAME two PROVABLY DISTINCT raw source 3-cells collapse in
the chosen E7P4 full-shadow quotient, because a unit has grade 0.
This is a concrete proof that the quotient is not raw faithful. -/
theorem northNativeF55Pentagon_quotient_eq_withUnit :
    nativeF55ThreeOf northNativeF55PentagonCell =
      nativeF55ThreeOf northNativeF55PentagonWithUnit := by
  apply Quot.sound
  change northNativeF55PentagonCell.nativeShadow =
    northNativeF55PentagonCell.nativeShadow + (0 : KuuNativeF55Shadow)
  exact (add_zero _).symm

/-- An explicit nonfaithfulness certificate for the chosen
quotient map on genuinely typed original-shaped F55 pentagon
raw-source 3-cells. This does NOT prohibit a richer historical
source/receiver comparison in another faithful carrier. -/
theorem northNativeF55Pentagon_quotient_not_injective :
    ¬ Function.Injective
      (fun c :
          KuuNativeF45Tree.DepthRotationRoute.PresentedCell
            (.pentagon .north)
            northNativeF45PentagonLong northNativeF45PentagonShort =>
          nativeF55ThreeOf c) := by
  intro hinj
  exact northNativeF55PentagonWithUnit_raw_ne
    (hinj northNativeF55PentagonCell northNativeF55PentagonWithUnit
      northNativeF55Pentagon_quotient_eq_withUnit)

/-- The two signed charges observed through the E7Q2 independent
F58-shaped target already determine each E7P4 quotient 3-arrow.
This follows from the complete nine-constructor target comparison,
not a hidden identification of F19/F28 primitive histories. -/
theorem nativeF55ThreeEval_charge_eq_interpret_charge
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
    (c : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v) :
    (nativeF55ThreeEval (nativeF55ThreeOf c)).1 =
      c.interpret (nativeF55ChargeTarget (D := D) (E := E) p) := by
  rw [nativeF55ThreeEval_of]
  exact c.interpret_charge_eq_shadow_fst.symm

#print axioms nativeF55ShadowRel_iff_charge_eq
#print axioms NativeF55ThreeHom.phase_squareParity
#print axioms nativeF55ThreeEval_charge_injective
#print axioms northNativeF55PentagonWithUnit_raw_ne
#print axioms northNativeF55Pentagon_quotient_eq_withUnit
#print axioms northNativeF55Pentagon_quotient_not_injective
#print axioms nativeF55ThreeEval_charge_eq_interpret_charge
end
end Kuu.F112.Physical
