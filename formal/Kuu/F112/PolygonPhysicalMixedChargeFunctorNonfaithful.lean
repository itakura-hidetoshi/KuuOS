import Kuu.F112.PolygonPhysicalMixedFourBoundaryThreeCategory

/-!
# F112-P35 — full but nonfaithful C60 physical-face / F55 mixed charge functor

P34 constructed a genuinely separately typed FOUR-BOUNDARY mixed
3-Hom category over the original C60 F42 physical face 3-source and
the independent raw F55 six-sector rotation 3-source. The face
and rotation proofs and the two explicit NEW comparison arrows are
kept distinct; the original source is not a proxy for a numerical grade.

Here we construct the exact CHARGE-ONLY quotient of the SAME typed
mixed raw proof grammar and its genuine Mathlib Category, together
with a source-preserving functor from the complete (charge, phase)
mixed source. It is FULL for every four-boundary higher Hom, since
every charge-only arrow has an actual native full-shadow preimage.

On the genuine physical C60 north-hexagon ZERO-CALIBRATION mixed
source, the upper and lower mixed arrows are different in the
full-shadow quotient, but identical in the integer-charge quotient.
Hence the functor is NOT FAITHFUL on an actual physical-F42 versus
F55-rotation mixed Hom, and admits no pointwise left inverse there.

This categorical nonfaithfulness is a NEW physically anchored
face/rotation source obstruction. It is not a reconstruction of the
frozen historical F47/Gray 3-Hom or of F68/F77 curvature.
No imported KUOS/Gray, new axioms, sorry or admit.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
noncomputable section

/-- A second exact quotient of the SAME P34 raw physical/rotation
three-Hom source, now identifying only the two integer charges.
The independently chosen phase is intentionally discarded. -/
abbrev NativeC60MixedChargeHom
    (B : NativeC60PhysicalMixedCalibration)
    (X Y : NativeC60MixedPoint B) :=
  Quot (fun f g : NativeC60MixedRaw B X Y =>
    f.toShadow.1 = g.toShadow.1)

def nativeC60MixedChargeOf
    {B : NativeC60PhysicalMixedCalibration}
    {X Y : NativeC60MixedPoint B}
    (f : NativeC60MixedRaw B X Y) : NativeC60MixedChargeHom B X Y :=
  Quot.mk _ f

/-- Exact, well-defined full-shadow-to-charge projection; proof
relation implies charge relation by taking Prod.fst. -/
def nativeC60MixedForgetPhase
    {B : NativeC60PhysicalMixedCalibration}
    {X Y : NativeC60MixedPoint B}
    (f : NativeC60MixedHom B X Y) : NativeC60MixedChargeHom B X Y :=
  Quot.liftOn f
    (fun raw => nativeC60MixedChargeOf raw)
    (by
      intro f g h
      apply Quot.sound
      exact congrArg Prod.fst h)

@[simp] theorem nativeC60MixedForgetPhase_of
    {B : NativeC60PhysicalMixedCalibration}
    {X Y : NativeC60MixedPoint B}
    (raw : NativeC60MixedRaw B X Y) :
    nativeC60MixedForgetPhase (nativeC60MixedOf raw) =
      nativeC60MixedChargeOf raw := rfl

/-- Every charge-quotient three-arrow has a full-shadow source
representative at the very same genuinely typed four boundaries. -/
theorem nativeC60MixedForgetPhase_surjective
    {B : NativeC60PhysicalMixedCalibration}
    {X Y : NativeC60MixedPoint B} :
    Function.Surjective
      (fun f : NativeC60MixedHom B X Y =>
        nativeC60MixedForgetPhase f) := by
  intro f
  refine Quot.inductionOn f (fun raw => ?_)
  exact ⟨nativeC60MixedOf raw, rfl⟩

/-- The charge-only vertical composition is well-defined even on
arbitrarily long Type-valued mixed raw face/rotation source pastes. -/
def nativeC60MixedChargeComp
    {B : NativeC60PhysicalMixedCalibration}
    {X Y Z : NativeC60MixedPoint B}
    (f : NativeC60MixedChargeHom B X Y)
    (g : NativeC60MixedChargeHom B Y Z) :
    NativeC60MixedChargeHom B X Z :=
  Quot.liftOn₂ f g
    (fun left right => nativeC60MixedChargeOf (.trans left right))
    (by
      intro left right₁ right₂ h
      apply Quot.sound
      change left.toShadow.1 + right₁.toShadow.1 =
        left.toShadow.1 + right₂.toShadow.1
      rw [h])
    (by
      intro left₁ left₂ right h
      apply Quot.sound
      change left₁.toShadow.1 + right.toShadow.1 =
        left₂.toShadow.1 + right.toShadow.1
      rw [h])

/-- Forgetting phase COMMUTES with all native physical/rotation
mixed vertical pasting, not just the north-hexagon square. -/
theorem nativeC60MixedForgetPhase_comp
    {B : NativeC60PhysicalMixedCalibration}
    {X Y Z : NativeC60MixedPoint B}
    (f : NativeC60MixedHom B X Y)
    (g : NativeC60MixedHom B Y Z) :
    nativeC60MixedForgetPhase (nativeC60MixedComp f g) =
      nativeC60MixedChargeComp
        (nativeC60MixedForgetPhase f)
        (nativeC60MixedForgetPhase g) := by
  refine Quot.inductionOn f (fun left => ?_)
  refine Quot.inductionOn g (fun right => ?_)
  rfl

/-- The TARGET boundary wrapper is a genuinely separate category
type; do not silently install two competing category instances
on the same full-shadow original mixed boundary carrier. -/
structure NativeC60MixedChargePoint
    (B : NativeC60PhysicalMixedCalibration) where
  original : NativeC60MixedPoint B

instance nativeC60MixedChargeCategory
    (B : NativeC60PhysicalMixedCalibration) :
    Category (NativeC60MixedChargePoint B) where
  Hom X Y := NativeC60MixedChargeHom B X.original Y.original
  id X := nativeC60MixedChargeOf (.ident X.original)
  comp := nativeC60MixedChargeComp
  id_comp := by
    intro X Y f
    refine Quot.inductionOn f (fun raw => ?_)
    apply Quot.sound
    change (0 : Int × Int) + raw.toShadow.1 = raw.toShadow.1
    exact zero_add _
  comp_id := by
    intro X Y f
    refine Quot.inductionOn f (fun raw => ?_)
    apply Quot.sound
    change raw.toShadow.1 + (0 : Int × Int) = raw.toShadow.1
    exact add_zero _
  assoc := by
    intro W X Y Z f g h
    refine Quot.inductionOn f (fun f => ?_)
    refine Quot.inductionOn g (fun g => ?_)
    refine Quot.inductionOn h (fun h => ?_)
    apply Quot.sound
    change (f.toShadow.1 + g.toShadow.1) + h.toShadow.1 =
      f.toShadow.1 + (g.toShadow.1 + h.toShadow.1)
    exact add_assoc _ _ _

/-- Genuine Mathlib functor from the complete native mixed
physical-F42/F55 higher category into the integer-charge-only
category, with exactly matching source boundary object tags. -/
def nativeC60MixedChargeFunctor
    (B : NativeC60PhysicalMixedCalibration) :
    (NativeC60MixedPoint B) ⥤ (NativeC60MixedChargePoint B) where
  obj X := ⟨X⟩
  map := fun {_ _} f => nativeC60MixedForgetPhase f
  map_id := by
    intro X
    rfl
  map_comp := by
    intro X Y Z f g
    exact nativeC60MixedForgetPhase_comp f g

/-- Strong Mathlib FULLNESS: every charge-only mixed higher arrow
has a true Type-valued physical/rotation raw preimage and thus an
arrow in the complete chosen source-quotient category. -/
instance nativeC60MixedChargeFunctor_full
    (B : NativeC60PhysicalMixedCalibration) :
    (nativeC60MixedChargeFunctor B).Full where
  map_surjective := by
    intro X Y f
    exact (nativeC60MixedForgetPhase_surjective
      (B := B) (X := X) (Y := Y)) f

/-- Two concrete correctly boundary-typed mixed source 3-arrows from
the ACTUAL C60 original physical face to the native F55 rotation
have the SAME signed integer charge after phase erasure. -/
theorem northC60MixedUncorrected_upper_lower_charge_eq :
    nativeC60MixedChargeOf
        (nativeC60MixedRawUpper northHexagonPhysicalMixedUncorrected) =
      nativeC60MixedChargeOf
        (nativeC60MixedRawLower northHexagonPhysicalMixedUncorrected) := by
  apply Quot.sound
  change northHexagonEvenShadow.1 + (0 : Int × Int) =
    (0 : Int × Int) + northHexagonOddShadow.1
  simpa only [add_zero, zero_add] using
    northHexagonEvenOddShadow_charge_eq

/-- The SAME original physical face and rotation witnesses yield
different higher arrows before forgetting the pure phase. -/
theorem northC60MixedUncorrected_upper_ne_lower :
    nativeC60MixedOf
        (nativeC60MixedRawUpper northHexagonPhysicalMixedUncorrected) ≠
      nativeC60MixedOf
        (nativeC60MixedRawLower northHexagonPhysicalMixedUncorrected) := by
  intro h
  have hh := congrArg
    (fun f : NativeC60MixedHom northHexagonPhysicalMixedUncorrected
        .physicalBefore .rotationAfter => nativeC60MixedEval f) h
  change northHexagonEvenShadow + (0 : KuuNativeF55Shadow) =
    (0 : KuuNativeF55Shadow) + northHexagonOddShadow at hh
  have heq : northHexagonEvenShadow = northHexagonOddShadow := by
    simpa only [add_zero, zero_add] using hh
  exact northHexagonEvenOddShadow_phase_ne (congrArg Prod.snd heq)

/-- A genuine source-level NONINJECTIVITY certificate for the exact
physical face-vs-native F55 rotation mixed four-boundary Hom. -/
theorem northC60MixedUncorrected_forgetPhase_not_injective :
    ¬ Function.Injective
      (fun f : NativeC60MixedHom northHexagonPhysicalMixedUncorrected
        .physicalBefore .rotationAfter =>
          nativeC60MixedForgetPhase f) := by
  intro hinj
  apply northC60MixedUncorrected_upper_ne_lower
  apply hinj
  exact northC60MixedUncorrected_upper_lower_charge_eq

/-- The source-specific Mathlib functor is FULL but NOT FAITHFUL
on the real C60 hexagon mixed physical-face/rotation component. -/
theorem northC60MixedChargeFunctor_not_faithful :
    ¬ (nativeC60MixedChargeFunctor
      northHexagonPhysicalMixedUncorrected).Faithful := by
  intro hFaith
  apply northC60MixedUncorrected_forgetPhase_not_injective
  intro f g h
  exact hFaith.map_injective h

/-- No charge-only exact reconstruction can be a left inverse of
the full-to-charge observation even on this single actual mixed
C60 physical-face/F55 rotation Hom. -/
theorem northC60MixedCharge_no_left_inverse :
    ¬ ∃ recover :
        NativeC60MixedChargeHom northHexagonPhysicalMixedUncorrected
          .physicalBefore .rotationAfter →
        NativeC60MixedHom northHexagonPhysicalMixedUncorrected
          .physicalBefore .rotationAfter,
      Function.LeftInverse recover
        (fun f : NativeC60MixedHom northHexagonPhysicalMixedUncorrected
          .physicalBefore .rotationAfter =>
            nativeC60MixedForgetPhase f) := by
  rintro ⟨recover, hleft⟩
  exact northC60MixedUncorrected_forgetPhase_not_injective hleft.injective

#print axioms NativeC60MixedChargeHom
#print axioms nativeC60MixedForgetPhase
#print axioms nativeC60MixedForgetPhase_surjective
#print axioms nativeC60MixedChargeComp
#print axioms nativeC60MixedForgetPhase_comp
#print axioms nativeC60MixedChargeCategory
#print axioms nativeC60MixedChargeFunctor
#print axioms nativeC60MixedChargeFunctor_full
#print axioms northC60MixedUncorrected_upper_lower_charge_eq
#print axioms northC60MixedUncorrected_upper_ne_lower
#print axioms northC60MixedUncorrected_forgetPhase_not_injective
#print axioms northC60MixedChargeFunctor_not_faithful
#print axioms northC60MixedCharge_no_left_inverse

end
end Kuu.F112.Physical
