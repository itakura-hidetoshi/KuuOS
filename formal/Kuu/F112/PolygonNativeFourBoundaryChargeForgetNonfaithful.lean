import Kuu.F112.PolygonNativeFourBoundaryCalibration

/-!
# F112-P30 — charge-only observation is not faithful on a real C60 3-Hom

The independent P29 four-boundary native C60 receiver source has an
exact full-shadow higher-Hom quotient retaining both integer charges
and the independent ZMod 2 phase. Here we construct a SECOND, strictly
coarser charge-only quotient of the SAME real raw proof-related source,
and a canonical surjective forget-phase map between these typed Homs.

That map respects every native raw vertical paste. Nevertheless it is
NOT INJECTIVE on the real north-hexagon receiver four-boundary Hom:
the upper and lower squares become equal on charge alone when the
comparison correction is zero, whereas their genuine full-shadow
arrows are distinct because the even/odd target phases differ.

This supplies a source-level obstruction to charge-only faithfulness,
rather than merely a numerical phase decoder counterexample. It is
local to the newly constructed C60 receiver comparison, not a proven
equivalence with the frozen historical F47/F68/F77 3-source. No Gray,
sorry, admit or extra axioms.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
noncomputable section

/-- A genuinely separate quotient of P29's SAME raw Type-valued
four-boundary 3-arrows, now identifying exactly equal integer charge.
This is strictly coarser than the full native phase-aware quotient. -/
abbrev NativeHexagonChargeHom
    (B : NativeHexagonFourBoundaryData)
    (X Y : NativeHexagonFourBoundary B) :=
  Quot (fun f g : NativeHexagonFourRaw B X Y =>
    f.toShadow.1 = g.toShadow.1)

def nativeHexagonChargeOf
    {B : NativeHexagonFourBoundaryData}
    {X Y : NativeHexagonFourBoundary B}
    (f : NativeHexagonFourRaw B X Y) : NativeHexagonChargeHom B X Y :=
  Quot.mk _ f

/-- Canonical typed forget-phase projection, well-defined because
full-shadow equality implies signed-charge equality. -/
def nativeHexagonFourForgetPhase
    {B : NativeHexagonFourBoundaryData}
    {X Y : NativeHexagonFourBoundary B}
    (f : NativeHexagonFourHom B X Y) : NativeHexagonChargeHom B X Y :=
  Quot.liftOn f
    (fun raw => nativeHexagonChargeOf raw)
    (by
      intro left right h
      apply Quot.sound
      exact congrArg Prod.fst h)

@[simp] theorem nativeHexagonFourForgetPhase_of
    {B : NativeHexagonFourBoundaryData}
    {X Y : NativeHexagonFourBoundary B}
    (f : NativeHexagonFourRaw B X Y) :
    nativeHexagonFourForgetPhase (nativeHexagonFourOf f) =
      nativeHexagonChargeOf f := rfl

/-- Every charge-quotient arrow has a full-quotient representative.
No FALSE injectivity statement is inferred from this surjectivity. -/
theorem nativeHexagonFourForgetPhase_surjective
    {B : NativeHexagonFourBoundaryData}
    {X Y : NativeHexagonFourBoundary B} :
    Function.Surjective
      (fun f : NativeHexagonFourHom B X Y =>
        nativeHexagonFourForgetPhase f) := by
  intro f
  refine Quot.inductionOn f (fun raw => ?_)
  exact ⟨nativeHexagonFourOf raw, rfl⟩

/-- Charge-quotient vertical paste is well-defined on arbitrary
representatives, using the same native four-boundary proof syntax. -/
def nativeHexagonChargeComp
    {B : NativeHexagonFourBoundaryData}
    {X Y Z : NativeHexagonFourBoundary B}
    (f : NativeHexagonChargeHom B X Y)
    (g : NativeHexagonChargeHom B Y Z) :
    NativeHexagonChargeHom B X Z :=
  Quot.liftOn₂ f g
    (fun left right => nativeHexagonChargeOf (.trans left right))
    (by
      intro left right₁ right₂ heq
      apply Quot.sound
      change left.toShadow.1 + right₁.toShadow.1 =
        left.toShadow.1 + right₂.toShadow.1
      rw [heq])
    (by
      intro left₁ left₂ right heq
      apply Quot.sound
      change left₁.toShadow.1 + right.toShadow.1 =
        left₂.toShadow.1 + right.toShadow.1
      rw [heq])

/-- Full-to-charge projection COMMUTES with every typed vertical
pasting, not just the concrete hexagon generators. -/
theorem nativeHexagonFourForgetPhase_comp
    {B : NativeHexagonFourBoundaryData}
    {X Y Z : NativeHexagonFourBoundary B}
    (f : NativeHexagonFourHom B X Y)
    (g : NativeHexagonFourHom B Y Z) :
    nativeHexagonFourForgetPhase (nativeHexagonFourComp f g) =
      nativeHexagonChargeComp
        (nativeHexagonFourForgetPhase f)
        (nativeHexagonFourForgetPhase g) := by
  refine Quot.inductionOn f (fun left => ?_)
  refine Quot.inductionOn g (fun right => ?_)
  rfl

/-- The upper and lower genuinely different north-hexagon FOUR-
BOUNDARY raw composites have identical signed integer charge when
the chosen comparison correction is zero. -/
theorem northHexagonZero_fourCharge_upper_eq_lower :
    nativeHexagonChargeOf
        (nativeHexagonRawUpper northHexagonFourZeroData) =
      nativeHexagonChargeOf
        (nativeHexagonRawLower northHexagonFourZeroData) := by
  apply Quot.sound
  change northHexagonEvenShadow.1 + (0 : Int × Int) =
    (0 : Int × Int) + northHexagonOddShadow.1
  simpa only [add_zero, zero_add] using
    northHexagonEvenOddShadow_charge_eq

/-- But the full-shadow source arrow distinction survives in the
genuine native C60 four-boundary quotient, because the two target
calibrations have distinct ZMod 2 phases. -/
theorem northHexagonZero_fullUpper_ne_lower :
    nativeHexagonFourOf
        (nativeHexagonRawUpper northHexagonFourZeroData) ≠
      nativeHexagonFourOf
        (nativeHexagonRawLower northHexagonFourZeroData) := by
  intro h
  have hval := congrArg
    (fun f : NativeHexagonFourHom northHexagonFourZeroData
        .evenBefore .oddAfter => nativeHexagonFourEval f) h
  change northHexagonEvenShadow + (0 : KuuNativeF55Shadow) =
    (0 : KuuNativeF55Shadow) + northHexagonOddShadow at hval
  have heq : northHexagonEvenShadow = northHexagonOddShadow := by
    simpa only [add_zero, zero_add] using hval
  exact northHexagonEvenOddShadow_phase_ne (congrArg Prod.snd heq)

/-- A real source-specific NONFAITHFULNESS witness:
the map from the native full-shadow 3-Hom to its signed-charge-only
shadow is surjective but NOT injective on the actual C60 square.
Its kernel genuinely forgets target calibration information. -/
theorem northHexagonZero_forgetPhase_not_injective :
    ¬ Function.Injective
      (fun f : NativeHexagonFourHom northHexagonFourZeroData
        .evenBefore .oddAfter => nativeHexagonFourForgetPhase f) := by
  intro hinj
  apply northHexagonZero_fullUpper_ne_lower
  apply hinj
  exact northHexagonZero_fourCharge_upper_eq_lower

#print axioms NativeHexagonChargeHom
#print axioms nativeHexagonFourForgetPhase
#print axioms nativeHexagonFourForgetPhase_of
#print axioms nativeHexagonFourForgetPhase_surjective
#print axioms nativeHexagonChargeComp
#print axioms nativeHexagonFourForgetPhase_comp
#print axioms northHexagonZero_fourCharge_upper_eq_lower
#print axioms northHexagonZero_fullUpper_ne_lower
#print axioms northHexagonZero_forgetPhase_not_injective

end
end Kuu.F112.Physical
