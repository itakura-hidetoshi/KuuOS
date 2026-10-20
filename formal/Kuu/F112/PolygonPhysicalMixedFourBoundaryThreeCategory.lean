import Kuu.F112.PolygonPhysicalMixedFaceRotationNonlift

/-!
# F112-P34 — native C60 physical F42-face / F55-rotation mixed 3-Hom

P33 proved that the genuine C60 physical F42 fan-2-proof comparison
and the independent six-sector F54/F55 rotation raw 3-proof can be
retained in ONE fully typed source. It also established a true
nonlift: the required pure-phase face-to-rotation comparison cannot
be supplied by native F55 raw 3-cells or their quotient.

Here we construct the FIRST separately tagged, truly mixed
physical-face / native-F55 higher Hom-category over that source.
Its two vertical source 3-arrows are different formal generators
backed by DIFFERENT Type-valued witnesses; the two comparison
generators are EXPLICITLY NEW. The two pasting orders remain distinct
raw proof trees. We quotient only by equality of their full
(Int × Int) × ZMod 2 shadows, prove all Mathlib Category laws, a
faithful complete-shadow functor, and the exact conditional mixed
commuting-square criterion.

The concrete original C60 mixed square with its explicit calibration
commutes. The otherwise identical uncorrected mixed square does NOT.
The required comparison arrow has a nonzero pure-phase shadow not
represented by any arrow in the native F55 source three-Hom.

This is a NEW independent source-specific mixed category, NOT a
reconstruction of historical frozen F47/Gray 3-Hom, Beck-Chevalley
naturality or F68/F77 curvature. No KUOS, Gray, new axioms or sorry.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
noncomputable section

/-- Exactly FOUR distinct typed boundary positions of the physical
face-vs-native-rotation comparison. The frame parameter retains all
actual original F42 face fan/disk and F55 route/3-cell witnesses. -/
inductive NativeC60MixedPoint (B : NativeC60PhysicalMixedCalibration)
    : Type where
  | physicalBefore | physicalAfter | rotationBefore | rotationAfter
  deriving DecidableEq

/-- FREE, Type-valued mixed 3-source grammar. A physical face step is
not *identified* with an F55 rotation step; each has a separately
typed source proof in B.source. Two new comparison steps are explicit,
not silently imported as a nonexistent native F55 pure-phase arrow. -/
inductive NativeC60MixedRaw (B : NativeC60PhysicalMixedCalibration) :
    NativeC60MixedPoint B → NativeC60MixedPoint B → Type where
  | ident (X : NativeC60MixedPoint B) : NativeC60MixedRaw B X X
  | physicalStep :
      NativeC60MixedRaw B .physicalBefore .physicalAfter
  | rotationStep :
      NativeC60MixedRaw B .rotationBefore .rotationAfter
  | compareBefore :
      NativeC60MixedRaw B .physicalBefore .rotationBefore
  | compareAfter :
      NativeC60MixedRaw B .physicalAfter .rotationAfter
  | trans {X Y Z : NativeC60MixedPoint B}
      (f : NativeC60MixedRaw B X Y)
      (g : NativeC60MixedRaw B Y Z) :
      NativeC60MixedRaw B X Z

/-- Source-level proof term discriminator. It records the genuine
first formal generator, not its numerical grade. -/
def NativeC60MixedRaw.leadingTag
    {B : NativeC60PhysicalMixedCalibration}
    {X Y : NativeC60MixedPoint B}
    (f : NativeC60MixedRaw B X Y) : Nat :=
  match f with
  | .ident _ => 0
  | .physicalStep => 1
  | .rotationStep => 2
  | .compareBefore => 3
  | .compareAfter => 4
  | .trans f _ => f.leadingTag

def nativeC60MixedRawUpper (B : NativeC60PhysicalMixedCalibration) :
    NativeC60MixedRaw B .physicalBefore .rotationAfter :=
  .trans .physicalStep .compareAfter

def nativeC60MixedRawLower (B : NativeC60PhysicalMixedCalibration) :
    NativeC60MixedRaw B .physicalBefore .rotationAfter :=
  .trans .compareBefore .rotationStep

/-- The original typed mixed 3-cell source retains two different
pasting histories, even before any target calibration is considered. -/
theorem nativeC60MixedRawUpper_ne_lower
    (B : NativeC60PhysicalMixedCalibration) :
    nativeC60MixedRawUpper B ≠ nativeC60MixedRawLower B := by
  intro h
  have hh := congrArg NativeC60MixedRaw.leadingTag h
  change (1 : Nat) = 3 at hh
  exact (by decide : (1 : Nat) ≠ 3) hh

/-- Completely typed chosen full-shadow interpretation. Crucially,
a physical face 3-generator receives the EXPLICIT P33 face observer,
while the rotation generator uses its separately source-sound F55
observer; neither source type is ever made equal to the other. -/
def NativeC60MixedRaw.toShadow
    {B : NativeC60PhysicalMixedCalibration}
    {X Y : NativeC60MixedPoint B}
    (f : NativeC60MixedRaw B X Y) : KuuNativeF55Shadow :=
  match f with
  | .ident _ => 0
  | .physicalStep => B.faceValue
  | .rotationStep => B.rotationValue
  | .compareBefore => B.compareBefore
  | .compareAfter => B.compareAfter
  | .trans f g => f.toShadow + g.toShadow

/-- Exact shadow kernel only on parallel arrows. This quotient does
NOT identify distinct raw physical or F55 source witness trees. -/
abbrev NativeC60MixedHom (B : NativeC60PhysicalMixedCalibration)
    (X Y : NativeC60MixedPoint B) :=
  Quot (fun f g : NativeC60MixedRaw B X Y =>
    f.toShadow = g.toShadow)

def nativeC60MixedOf
    {B : NativeC60PhysicalMixedCalibration}
    {X Y : NativeC60MixedPoint B}
    (f : NativeC60MixedRaw B X Y) : NativeC60MixedHom B X Y :=
  Quot.mk _ f

def nativeC60MixedEval
    {B : NativeC60PhysicalMixedCalibration}
    {X Y : NativeC60MixedPoint B}
    (f : NativeC60MixedHom B X Y) : KuuNativeF55Shadow :=
  Quot.liftOn f (fun raw => raw.toShadow) (by
    intro f g h
    exact h)

@[simp] theorem nativeC60MixedEval_of
    {B : NativeC60PhysicalMixedCalibration}
    {X Y : NativeC60MixedPoint B}
    (f : NativeC60MixedRaw B X Y) :
    nativeC60MixedEval (nativeC60MixedOf f) = f.toShadow := rfl

def nativeC60MixedComp
    {B : NativeC60PhysicalMixedCalibration}
    {X Y Z : NativeC60MixedPoint B}
    (f : NativeC60MixedHom B X Y)
    (g : NativeC60MixedHom B Y Z) :
    NativeC60MixedHom B X Z :=
  Quot.liftOn₂ f g
    (fun left right => nativeC60MixedOf (.trans left right))
    (by
      intro left right₁ right₂ h
      apply Quot.sound
      change left.toShadow + right₁.toShadow =
        left.toShadow + right₂.toShadow
      rw [h])
    (by
      intro left₁ left₂ right h
      apply Quot.sound
      change left₁.toShadow + right.toShadow =
        left₂.toShadow + right.toShadow
      rw [h])

theorem nativeC60MixedEval_comp
    {B : NativeC60PhysicalMixedCalibration}
    {X Y Z : NativeC60MixedPoint B}
    (f : NativeC60MixedHom B X Y)
    (g : NativeC60MixedHom B Y Z) :
    nativeC60MixedEval (nativeC60MixedComp f g) =
      nativeC60MixedEval f + nativeC60MixedEval g := by
  refine Quot.inductionOn f (fun f => ?_)
  refine Quot.inductionOn g (fun g => ?_)
  rfl

/-- Full Mathlib Category on FOUR genuinely source-distinct mixed
boundary positions. Identity, composition and associativity
are proved in exactly the specified complete-shadow quotient. -/
instance nativeC60MixedCategory (B : NativeC60PhysicalMixedCalibration) :
    Category (NativeC60MixedPoint B) where
  Hom := NativeC60MixedHom B
  id X := nativeC60MixedOf (.ident X)
  comp := nativeC60MixedComp
  id_comp := by
    intro X Y f
    refine Quot.inductionOn f (fun raw => ?_)
    apply Quot.sound
    change (0 : KuuNativeF55Shadow) + raw.toShadow = raw.toShadow
    exact zero_add _
  comp_id := by
    intro X Y f
    refine Quot.inductionOn f (fun raw => ?_)
    apply Quot.sound
    change raw.toShadow + (0 : KuuNativeF55Shadow) = raw.toShadow
    exact add_zero _
  assoc := by
    intro W X Y Z f g h
    refine Quot.inductionOn f (fun f => ?_)
    refine Quot.inductionOn g (fun g => ?_)
    refine Quot.inductionOn h (fun h => ?_)
    apply Quot.sound
    change (f.toShadow + g.toShadow) + h.toShadow =
      f.toShadow + (g.toShadow + h.toShadow)
    exact add_assoc _ _ _

/-- Complete-shadow evaluation is faithful on this explicitly chosen
kernel quotient, not on the native raw F42 or F55 source syntax. -/
theorem nativeC60MixedEval_injective
    {B : NativeC60PhysicalMixedCalibration}
    {X Y : NativeC60MixedPoint B}
    {f g : X ⟶ Y}
    (h : nativeC60MixedEval f = nativeC60MixedEval g) : f = g := by
  revert h
  refine Quot.inductionOn f (fun f => ?_)
  refine Quot.inductionOn g (fun g hh => ?_)
  exact Quot.sound hh

def nativeC60MixedPhysicalArrow (B : NativeC60PhysicalMixedCalibration) :
    (NativeC60MixedPoint.physicalBefore : NativeC60MixedPoint B) ⟶
      .physicalAfter :=
  nativeC60MixedOf .physicalStep

def nativeC60MixedRotationArrow (B : NativeC60PhysicalMixedCalibration) :
    (NativeC60MixedPoint.rotationBefore : NativeC60MixedPoint B) ⟶
      .rotationAfter :=
  nativeC60MixedOf .rotationStep

def nativeC60MixedCompareBefore (B : NativeC60PhysicalMixedCalibration) :
    (NativeC60MixedPoint.physicalBefore : NativeC60MixedPoint B) ⟶
      .rotationBefore :=
  nativeC60MixedOf .compareBefore

def nativeC60MixedCompareAfter (B : NativeC60PhysicalMixedCalibration) :
    (NativeC60MixedPoint.physicalAfter : NativeC60MixedPoint B) ⟶
      .rotationAfter :=
  nativeC60MixedOf .compareAfter

/-- The new source-specific genuine mixed four-boundary square
COMMUTES IF AND ONLY IF its independently supplied full target
calibration equation holds. This is a two-direction proof, not
an assumed higher interchange coherence. -/
theorem nativeC60MixedSquare_iff_calibrated
    (B : NativeC60PhysicalMixedCalibration) :
    (nativeC60MixedPhysicalArrow B ≫ nativeC60MixedCompareAfter B =
      nativeC60MixedCompareBefore B ≫ nativeC60MixedRotationArrow B) ↔
      B.Calibrated := by
  constructor
  · intro h
    have hh := congrArg
      (fun f : NativeC60MixedHom B .physicalBefore .rotationAfter =>
        nativeC60MixedEval f) h
    change B.faceValue + B.compareAfter =
      B.compareBefore + B.rotationValue at hh
    exact hh
  · intro h
    apply Quot.sound
    change B.faceValue + B.compareAfter =
      B.compareBefore + B.rotationValue
    exact h

/-- A real genuinely physical C60 face/rotation square whose extra
pure phase correction was separately verified at P33. -/
theorem northHexagonC60MixedSquare_commutes :
    nativeC60MixedPhysicalArrow northHexagonPhysicalMixedCalibrated ≫
      nativeC60MixedCompareAfter northHexagonPhysicalMixedCalibrated =
    nativeC60MixedCompareBefore northHexagonPhysicalMixedCalibrated ≫
      nativeC60MixedRotationArrow northHexagonPhysicalMixedCalibrated :=
  (nativeC60MixedSquare_iff_calibrated
    northHexagonPhysicalMixedCalibrated).2
      northHexagonPhysicalMixedCalibrated_valid

/-- With exactly the same physical F42 and F55 raw source, choosing
zero comparison correction instead produces a noncommuting square. -/
theorem northHexagonC60MixedUncorrected_not_commutative :
    nativeC60MixedPhysicalArrow northHexagonPhysicalMixedUncorrected ≫
        nativeC60MixedCompareAfter northHexagonPhysicalMixedUncorrected ≠
      nativeC60MixedCompareBefore northHexagonPhysicalMixedUncorrected ≫
        nativeC60MixedRotationArrow northHexagonPhysicalMixedUncorrected := by
  intro h
  exact northHexagonPhysicalMixedUncorrected_not_calibrated
    ((nativeC60MixedSquare_iff_calibrated
      northHexagonPhysicalMixedUncorrected).1 h)

/-- The mixed comparison arrow has the exact independently required
pure-phase shadow, which lives outside the native F55 image. -/
theorem northHexagonC60MixedCompareAfter_shadow :
    nativeC60MixedEval
        (nativeC60MixedCompareAfter northHexagonPhysicalMixedCalibrated) =
      northHexagonPhysicalMixedCalibrated.compareAfter := rfl

/-- This is the actual source-specific mixed bridge obstruction:
NO native original-shaped F55 3-Hom arrow with the same real C60
rotation boundaries can represent the new face-to-rotation
comparison arrow. Its nonzero phase and zero charge force a
separate mixed generator. -/
theorem northHexagonC60MixedCompareAfter_not_nativeF55
    (f : NativeF55ThreeHom
      northHexagonNativeSquareLeft northHexagonNativeSquareRight) :
    nativeF55ThreeEval f ≠
      nativeC60MixedEval
        (nativeC60MixedCompareAfter northHexagonPhysicalMixedCalibrated) := by
  rw [northHexagonC60MixedCompareAfter_shadow]
  exact northHexagonPhysicalMixedCorrection_no_nativeF55_hom f

#print axioms NativeC60MixedPoint
#print axioms NativeC60MixedRaw
#print axioms NativeC60MixedRaw.leadingTag
#print axioms nativeC60MixedRawUpper_ne_lower
#print axioms nativeC60MixedComp
#print axioms nativeC60MixedEval_comp
#print axioms nativeC60MixedCategory
#print axioms nativeC60MixedEval_injective
#print axioms nativeC60MixedSquare_iff_calibrated
#print axioms northHexagonC60MixedSquare_commutes
#print axioms northHexagonC60MixedUncorrected_not_commutative
#print axioms northHexagonC60MixedCompareAfter_shadow
#print axioms northHexagonC60MixedCompareAfter_not_nativeF55

end
end Kuu.F112.Physical
