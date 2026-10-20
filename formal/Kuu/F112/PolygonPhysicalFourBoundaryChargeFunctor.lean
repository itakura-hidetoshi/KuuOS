import Kuu.F112.PolygonPhysicalF47SourcePacket

/-!
# F112-P32 — full but nonfaithful C60 higher-source charge functor

P29/P30 constructed two different quotients of the SAME genuine
north-hexagon four-boundary Type-valued proof-relevant 3-source:
one retains signed charge AND ZMod 2 exchange phase; the other
retains ONLY integer charges. P30 proved fiberwise surjectivity and
noninjectivity of forget-phase, and compatibility with all vertical
raw four-boundary compositions.

Here we organize the second quotient as an actual Mathlib Category,
and the forget-phase observation as an honest Mathlib Functor from
the already proven full-shadow higher-source category. It is FULL
on every Hom, by constructive representative lifting, but is NOT
FAITHFUL on the actual C60 zero-calibration hexagon Hom. Consequently
no function can be a left inverse to this source-level projection.

The P31 physical F42 fan/disk remains genuinely Type-valued and
fixed throughout; forgetting the separate calibrated phase does
not turn the old historical F47 source into an equivalence.

No original KUOS/Gray imports, no extra axioms, sorry, or admit.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
noncomputable section

/-- A separate category of charge observations with OBJECTS kept
tagged relative to the same original four-boundary C60 frame.
The wrapper avoids falsely reusing the full-shadow category instance
on exactly the same boundary type. -/
structure NativeHexagonChargeBoundary
    (B : NativeHexagonFourBoundaryData) where
  original : NativeHexagonFourBoundary B

/-- The ordinary category structure on the charge-only quotient.
All category laws are proved using exact signed-charge equality,
not by equating the distinct raw proof trees. -/
instance nativeHexagonChargeCategory
    (B : NativeHexagonFourBoundaryData) :
    Category (NativeHexagonChargeBoundary B) where
  Hom X Y := NativeHexagonChargeHom B X.original Y.original
  id X := nativeHexagonChargeOf (.ident X.original)
  comp := nativeHexagonChargeComp
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
    refine Quot.inductionOn f (fun a => ?_)
    refine Quot.inductionOn g (fun b => ?_)
    refine Quot.inductionOn h (fun c => ?_)
    apply Quot.sound
    change (a.toShadow.1 + b.toShadow.1) + c.toShadow.1 =
      a.toShadow.1 + (b.toShadow.1 + c.toShadow.1)
    exact add_assoc _ _ _

/-- The charge evaluator is EXACT on the source-defined quotient,
not an arbitrary extra value attached to its morphisms. -/
def nativeHexagonChargeEval
    {B : NativeHexagonFourBoundaryData}
    {X Y : NativeHexagonChargeBoundary B}
    (f : X ⟶ Y) : Int × Int :=
  Quot.liftOn f (fun raw => raw.toShadow.1) (by
    intro a b h
    exact h)

@[simp] theorem nativeHexagonChargeEval_of
    {B : NativeHexagonFourBoundaryData}
    {X Y : NativeHexagonFourBoundary B}
    (f : NativeHexagonFourRaw B X Y) :
    nativeHexagonChargeEval
      (X := ⟨X⟩) (Y := ⟨Y⟩) (nativeHexagonChargeOf f) =
      f.toShadow.1 := rfl

/-- Every charge-quotient Hom is faithfully observed by its signed
integer pair, because that pair is precisely its kernel relation. -/
theorem nativeHexagonChargeEval_injective
    {B : NativeHexagonFourBoundaryData}
    {X Y : NativeHexagonChargeBoundary B}
    {f g : X ⟶ Y}
    (h : nativeHexagonChargeEval f = nativeHexagonChargeEval g) :
    f = g := by
  revert h
  refine Quot.inductionOn f (fun a => ?_)
  refine Quot.inductionOn g (fun b hab => ?_)
  exact Quot.sound hab

/-- Genuine Mathlib functor from the full signed-charge+phase
P29 four-boundary higher category to the coarser category of P30
charge observations, with both identity and composition laws proved. -/
def nativeHexagonFourToChargeFunctor
    (B : NativeHexagonFourBoundaryData) :
    (NativeHexagonFourBoundary B) ⥤ (NativeHexagonChargeBoundary B) where
  obj X := ⟨X⟩
  map := fun {_ _} f => nativeHexagonFourForgetPhase f
  map_id := by
    intro X
    rfl
  map_comp := by
    intro X Y Z f g
    exact nativeHexagonFourForgetPhase_comp f g

/-- A full shadow arrow's charge is EXACTLY the charge of its image
under the source category functor, at arbitrary typed endpoints. -/
theorem nativeHexagonFourToChargeFunctor_eval
    (B : NativeHexagonFourBoundaryData)
    {X Y : NativeHexagonFourBoundary B}
    (f : X ⟶ Y) :
    nativeHexagonChargeEval
      ((nativeHexagonFourToChargeFunctor B).map f) =
      (nativeHexagonFourEval f).1 := by
  refine Quot.inductionOn f (fun raw => ?_)
  rfl

/-- Mathlib FULLNESS, not only an informal statement: every arrow
in the charge-quotient category is the image of an ACTUAL native
full-shadow higher arrow, at the identical four boundary positions. -/
instance nativeHexagonFourToChargeFunctor_full
    (B : NativeHexagonFourBoundaryData) :
    (nativeHexagonFourToChargeFunctor B).Full where
  map_surjective := by
    intro X Y f
    exact (nativeHexagonFourForgetPhase_surjective
      (B := B) (X := X) (Y := Y)) f

/-- On the physically constructed six-sector C60 zero-correction
frame, this full source functor is NOT faithful: the two higher
3-arrows from P30 are charge-equal but fully phase-distinct. -/
theorem northHexagonZero_fourToCharge_not_faithful :
    ¬ (nativeHexagonFourToChargeFunctor
      northHexagonFourZeroData).Faithful := by
  intro hFaith
  apply northHexagonZero_forgetPhase_not_injective
  intro f g h
  exact hFaith.map_injective h

/-- The physical face fan/disk source of P31 is not changed by
the charge functor: its category map is solely on native higher
receiver arrows, and its input higher frame remains the original
C60 zero-correction four-boundary source. -/
def NativeHexagonPhysicalF47Frame.chargeFunctor
    (F : NativeHexagonPhysicalF47Frame) :=
  nativeHexagonFourToChargeFunctor F.higher

theorem northHexagonPhysicalZero_fourToCharge_not_faithful :
    ¬ northHexagonPhysicalF47ZeroFrame.chargeFunctor.Faithful :=
  northHexagonZero_fourToCharge_not_faithful

/-- There can be no source-level exact reconstruction from the
integer-charge Hom to the full charge+phase Hom, even at the one
actual physical C60 hexagon four-boundary component. -/
theorem northHexagonZero_fourToCharge_no_left_inverse :
    ¬ ∃ recover :
        NativeHexagonChargeHom northHexagonFourZeroData
          .evenBefore .oddAfter →
          NativeHexagonFourHom northHexagonFourZeroData
            .evenBefore .oddAfter,
      Function.LeftInverse recover
        (fun f : NativeHexagonFourHom northHexagonFourZeroData
          .evenBefore .oddAfter =>
            nativeHexagonFourForgetPhase f) := by
  rintro ⟨recover, hleft⟩
  exact northHexagonZero_forgetPhase_not_injective hleft.injective

#print axioms nativeHexagonChargeCategory
#print axioms nativeHexagonChargeEval
#print axioms nativeHexagonChargeEval_injective
#print axioms nativeHexagonFourToChargeFunctor
#print axioms nativeHexagonFourToChargeFunctor_eval
#print axioms nativeHexagonFourToChargeFunctor_full
#print axioms northHexagonZero_fourToCharge_not_faithful
#print axioms northHexagonPhysicalZero_fourToCharge_not_faithful
#print axioms northHexagonZero_fourToCharge_no_left_inverse

end
end Kuu.F112.Physical
