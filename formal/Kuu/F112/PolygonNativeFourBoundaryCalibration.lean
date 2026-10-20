import Kuu.F112.PolygonNativeUniversalDescentCalibration
import Mathlib.Tactic.Abel

/-!
# F112-P29 — four genuinely typed C60 receiver boundaries and calibration

The historical F47 comparison uses FOUR distinctly typed boundary
positions and proof-relevant 3-arrow source data. P26–P28 showed that
a Prop-erased raw F41 history and a signed-charge-only F55 receiver
cannot supply the missing witnesses by fiat.

We construct an independent, receiver-relative FOUR-BOUNDARY source
over the ACTUAL north C60 hexagon F55 six-sector raw square. It stores
the full Type-valued raw PresentedCell with both original F54 routes,
its separate even/odd F56-shaped target evaluations, and an explicitly
specified full-shadow comparison correction.

The four freely generated boundary arrows remain unequal as raw proof
trees. Their chosen full-shadow Kuu quotient is a genuine Mathlib
Category. The native boundary square commutes IF AND ONLY IF the
actual calibration equation holds. For the concrete source the unique
correction is charge-zero but phase-NONZERO; the charge-only/zero
correction cannot close this comparison square.

The odd/even receiver tags are two independently chosen TARGET
calibrations, NOT the historical physical-face/F55 bridge or an
equivalence to frozen original F47, F68 or F77. No KUOS/Gray imports,
new axioms, sorry or admit.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
noncomputable section

/-- A real Type-valued source-level 3-witness on the six-sector top
C60 hexagon, with both genuinely typed F54 source routes preserved.
Even and odd target calibrations are retained separately, not
collapsed to integer charge. The comparison correction is explicit
extra data, not imposed as an axiom or fixed by charges. -/
structure NativeHexagonFourBoundaryData where
  raw :
    KuuNativeF45Tree.DepthRotationRoute.PresentedCell
      (.hexagon (.top 0))
      northHexagonNativeSquareLeft northHexagonNativeSquareRight
  evenValue : KuuNativeF55Shadow
  oddValue : KuuNativeF55Shadow
  even_sound :
    evenValue = raw.interpret
      (nativeF55EvenPhaseTarget
        (D := Site) (E := Site) (.hexagon (.top 0)))
  odd_sound :
    oddValue = raw.interpret
      (nativeF55FullShadowTarget
        (D := Site) (E := Site) (.hexagon (.top 0)))
  correction : KuuNativeF55Shadow

/-- The typed square's coherence is a proof obligation: two
receiver-valued 3-arrows and one new comparison correction must
actually form an additive commutative square. -/
def NativeHexagonFourBoundaryData.Calibrated
    (B : NativeHexagonFourBoundaryData) : Prop :=
  B.evenValue + B.correction = B.oddValue

/-- Four DISTINCT and separately tagged F54-route endpoints.
The original F55 raw source itself is stored in B.raw. -/
inductive NativeHexagonFourBoundary
    (B : NativeHexagonFourBoundaryData) : Type where
  | evenBefore
  | evenAfter
  | oddBefore
  | oddAfter

/-- Free, fully proof-relevant four-boundary 3-arrow grammar.
The comparison arrows are NEW source constructors, not historical
original F55 arrows or automatic identifications of two routes. -/
inductive NativeHexagonFourRaw (B : NativeHexagonFourBoundaryData) :
    NativeHexagonFourBoundary B → NativeHexagonFourBoundary B → Type where
  | ident (X : NativeHexagonFourBoundary B) : NativeHexagonFourRaw B X X
  | evenStep : NativeHexagonFourRaw B .evenBefore .evenAfter
  | oddStep : NativeHexagonFourRaw B .oddBefore .oddAfter
  | compareBefore : NativeHexagonFourRaw B .evenBefore .oddBefore
  | compareAfter : NativeHexagonFourRaw B .evenAfter .oddAfter
  | trans {X Y Z : NativeHexagonFourBoundary B}
      (f : NativeHexagonFourRaw B X Y)
      (g : NativeHexagonFourRaw B Y Z) :
      NativeHexagonFourRaw B X Z

/-- Complete 3-arrow interpretation: the correction is NEVER
silently assigned by signed integer charge. -/
def NativeHexagonFourRaw.toShadow
    {B : NativeHexagonFourBoundaryData}
    {X Y : NativeHexagonFourBoundary B}
    (f : NativeHexagonFourRaw B X Y) : KuuNativeF55Shadow :=
  match f with
  | .ident _ => 0
  | .evenStep => B.evenValue
  | .oddStep => B.oddValue
  | .compareBefore => 0
  | .compareAfter => B.correction
  | .trans f g => f.toShadow + g.toShadow

/-- The first genuine primitive step is preserved before quotient,
so the two four-boundary paste orders stay different raw histories. -/
def NativeHexagonFourRaw.leadingTag
    {B : NativeHexagonFourBoundaryData}
    {X Y : NativeHexagonFourBoundary B}
    (f : NativeHexagonFourRaw B X Y) : Nat :=
  match f with
  | .ident _ => 0
  | .evenStep => 1
  | .oddStep => 2
  | .compareBefore => 3
  | .compareAfter => 4
  | .trans f _ => f.leadingTag

def nativeHexagonRawUpper (B : NativeHexagonFourBoundaryData) :
    NativeHexagonFourRaw B .evenBefore .oddAfter :=
  .trans .evenStep .compareAfter

def nativeHexagonRawLower (B : NativeHexagonFourBoundaryData) :
    NativeHexagonFourRaw B .evenBefore .oddAfter :=
  .trans .compareBefore .oddStep

/-- A real proof-related noncollapse, before ANY quotient by
chosen full-shadow values. -/
theorem nativeHexagonRawUpper_ne_lower (B : NativeHexagonFourBoundaryData) :
    nativeHexagonRawUpper B ≠ nativeHexagonRawLower B := by
  intro h
  have htag := congrArg NativeHexagonFourRaw.leadingTag h
  change (1 : Nat) = 3 at htag
  exact (by decide : (1 : Nat) ≠ 3) htag

/-- Only EXACT equality of complete signed-charge+phase shadows
may identify two parallel raw higher witnesses. -/
abbrev NativeHexagonFourHom
    (B : NativeHexagonFourBoundaryData)
    (X Y : NativeHexagonFourBoundary B) :=
  Quot (fun f g : NativeHexagonFourRaw B X Y =>
    f.toShadow = g.toShadow)

def nativeHexagonFourOf
    {B : NativeHexagonFourBoundaryData}
    {X Y : NativeHexagonFourBoundary B}
    (f : NativeHexagonFourRaw B X Y) :
    NativeHexagonFourHom B X Y :=
  Quot.mk _ f

def nativeHexagonFourEval
    {B : NativeHexagonFourBoundaryData}
    {X Y : NativeHexagonFourBoundary B}
    (f : NativeHexagonFourHom B X Y) : KuuNativeF55Shadow :=
  Quot.liftOn f (fun raw => raw.toShadow) (by
    intro f g h
    exact h)

@[simp] theorem nativeHexagonFourEval_of
    {B : NativeHexagonFourBoundaryData}
    {X Y : NativeHexagonFourBoundary B}
    (f : NativeHexagonFourRaw B X Y) :
    nativeHexagonFourEval (nativeHexagonFourOf f) = f.toShadow := rfl

def nativeHexagonFourComp
    {B : NativeHexagonFourBoundaryData}
    {X Y Z : NativeHexagonFourBoundary B}
    (f : NativeHexagonFourHom B X Y)
    (g : NativeHexagonFourHom B Y Z) :
    NativeHexagonFourHom B X Z :=
  Quot.liftOn₂ f g
    (fun left right => nativeHexagonFourOf (.trans left right))
    (by
      intro left right₁ right₂ heq
      apply Quot.sound
      change left.toShadow + right₁.toShadow =
        left.toShadow + right₂.toShadow
      rw [heq])
    (by
      intro left₁ left₂ right heq
      apply Quot.sound
      change left₁.toShadow + right.toShadow =
        left₂.toShadow + right.toShadow
      rw [heq])

/-- The chosen full shadow computes both correctly typed vertical
source pasting and the true additive target composition. -/
theorem nativeHexagonFourEval_comp
    {B : NativeHexagonFourBoundaryData}
    {X Y Z : NativeHexagonFourBoundary B}
    (f : NativeHexagonFourHom B X Y)
    (g : NativeHexagonFourHom B Y Z) :
    nativeHexagonFourEval (nativeHexagonFourComp f g) =
      nativeHexagonFourEval f + nativeHexagonFourEval g := by
  refine Quot.inductionOn f (fun rawf => ?_)
  refine Quot.inductionOn g (fun rawg => ?_)
  rfl

/-- An ACTUAL Mathlib category on four proof-related higher
boundaries, with strict category laws proved only after the
EXPLICIT full-shadow quotient, never at the raw F55 source level. -/
instance nativeHexagonFourCategory (B : NativeHexagonFourBoundaryData) :
    Category (NativeHexagonFourBoundary B) where
  Hom := NativeHexagonFourHom B
  id X := nativeHexagonFourOf (.ident X)
  comp := nativeHexagonFourComp
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
    refine Quot.inductionOn f (fun rawf => ?_)
    refine Quot.inductionOn g (fun rawg => ?_)
    refine Quot.inductionOn h (fun rawh => ?_)
    apply Quot.sound
    change (rawf.toShadow + rawg.toShadow) + rawh.toShadow =
      rawf.toShadow + (rawg.toShadow + rawh.toShadow)
    exact add_assoc _ _ _

/-- The complete shadow evaluator is INJECTIVE on each true 3-Hom
fiber by the chosen exact quotient; this does not claim raw
source faithfulness nor any historical Gray comparison. -/
theorem nativeHexagonFourEval_injective
    {B : NativeHexagonFourBoundaryData}
    {X Y : NativeHexagonFourBoundary B}
    {f g : NativeHexagonFourHom B X Y}
    (h : nativeHexagonFourEval f = nativeHexagonFourEval g) : f = g := by
  revert h
  refine Quot.inductionOn f (fun rawf => ?_)
  refine Quot.inductionOn g (fun rawg heq => ?_)
  exact Quot.sound heq

def nativeHexagonFourEvenArrow (B : NativeHexagonFourBoundaryData) :
    (NativeHexagonFourBoundary.evenBefore : NativeHexagonFourBoundary B) ⟶
      .evenAfter :=
  nativeHexagonFourOf .evenStep

def nativeHexagonFourOddArrow (B : NativeHexagonFourBoundaryData) :
    (NativeHexagonFourBoundary.oddBefore : NativeHexagonFourBoundary B) ⟶
      .oddAfter :=
  nativeHexagonFourOf .oddStep

def nativeHexagonFourCompareBefore (B : NativeHexagonFourBoundaryData) :
    (NativeHexagonFourBoundary.evenBefore : NativeHexagonFourBoundary B) ⟶
      .oddBefore :=
  nativeHexagonFourOf .compareBefore

def nativeHexagonFourCompareAfter (B : NativeHexagonFourBoundaryData) :
    (NativeHexagonFourBoundary.evenAfter : NativeHexagonFourBoundary B) ⟶
      .oddAfter :=
  nativeHexagonFourOf .compareAfter

/-- The precise local four-boundary coherence criterion, in BOTH
directions. Rather than postulating an exchange or erasing the
receiver phase, square commutativity is EQUIVALENT to the full
calibration equation. -/
theorem nativeHexagonFourSquare_iff_calibrated
    (B : NativeHexagonFourBoundaryData) :
    (nativeHexagonFourEvenArrow B ≫ nativeHexagonFourCompareAfter B =
      nativeHexagonFourCompareBefore B ≫ nativeHexagonFourOddArrow B) ↔
      B.Calibrated := by
  constructor
  · intro h
    have hshadow := congrArg
      (fun f : NativeHexagonFourHom B .evenBefore .oddAfter =>
        nativeHexagonFourEval f) h
    change B.evenValue + B.correction =
      (0 : KuuNativeF55Shadow) + B.oddValue at hshadow
    simpa only [zero_add] using hshadow
  · intro h
    apply Quot.sound
    change B.evenValue + B.correction =
      (0 : KuuNativeF55Shadow) + B.oddValue
    simpa only [zero_add] using h

/-- Two separate target observations of the exact SAME actual C60
F55 raw 3-cell are kept together as Type-valued evidence. -/
def northHexagonFourData : NativeHexagonFourBoundaryData where
  raw := northHexagonNativeF55SquareCell
  evenValue := northHexagonEvenShadow
  oddValue := northHexagonOddShadow
  even_sound := rfl
  odd_sound := rfl
  correction := northHexagonOddShadow - northHexagonEvenShadow

/-- The calibrated receiver comparison is genuine and source-fixed:
its correction equals the mathematically required full difference. -/
theorem northHexagonFourData_calibrated :
    northHexagonFourData.Calibrated := by
  change northHexagonEvenShadow +
    (northHexagonOddShadow - northHexagonEvenShadow) =
      northHexagonOddShadow
  abel

/-- The concrete raw-source comparison square REALLY commutes after
the exact target-kernel quotient and an explicit nonzero calibration. -/
theorem northHexagonFourSquare_commutes :
    nativeHexagonFourEvenArrow northHexagonFourData ≫
        nativeHexagonFourCompareAfter northHexagonFourData =
      nativeHexagonFourCompareBefore northHexagonFourData ≫
        nativeHexagonFourOddArrow northHexagonFourData :=
  (nativeHexagonFourSquare_iff_calibrated northHexagonFourData).2
    northHexagonFourData_calibrated

/-- The correction is UNIQUE for a fixed full pair of receiver
evaluations; independent arbitrary equality of source 3-cells
or integer charges is not enough. -/
theorem nativeHexagonFourCorrection_unique
    (B : NativeHexagonFourBoundaryData)
    (δ : KuuNativeF55Shadow)
    (hB : B.Calibrated)
    (hδ : B.evenValue + δ = B.oddValue) :
    δ = B.correction := by
  apply add_left_cancel (a := B.evenValue)
  calc
    B.evenValue + δ = B.oddValue := hδ
    _ = B.evenValue + B.correction := hB.symm

/-- The true north hexagon receiver comparison has zero EXTRA signed
integer charge: its obstruction lives in the independent phase
coordinate, not in the original pentagon/square charge pair. -/
theorem northHexagonFourCorrection_charge_zero :
    northHexagonFourData.correction.1 = ((0 : Int), (0 : Int)) := by
  change northHexagonOddShadow.1 - northHexagonEvenShadow.1 =
    ((0 : Int), (0 : Int))
  rw [← northHexagonEvenOddShadow_charge_eq]
  simp

/-- The same comparison correction has NONZERO ZMod2 phase, on the
actual six-sector C60 raw source rather than a fabricated square. -/
theorem northHexagonFourCorrection_phase_ne_zero :
    northHexagonFourData.correction.2 ≠ (0 : ZMod 2) := by
  intro h
  change northHexagonOddShadow.2 - northHexagonEvenShadow.2 =
    (0 : ZMod 2) at h
  have heq := sub_eq_zero.mp h
  exact northHexagonEvenOddShadow_phase_ne heq.symm

/-- Replacing that phase correction by ZERO gives another separately
typed frame, but it is provably NOT calibrated. -/
def northHexagonFourZeroData : NativeHexagonFourBoundaryData :=
  { northHexagonFourData with correction := 0 }

/-- Local C60 NO-GO: the uncorrected four-boundary square cannot
commute in the true native full-shadow 3-Hom quotient. -/
theorem northHexagonFourZeroSquare_not_commutative :
    nativeHexagonFourEvenArrow northHexagonFourZeroData ≫
        nativeHexagonFourCompareAfter northHexagonFourZeroData ≠
      nativeHexagonFourCompareBefore northHexagonFourZeroData ≫
        nativeHexagonFourOddArrow northHexagonFourZeroData := by
  intro h
  have hcal :=
    (nativeHexagonFourSquare_iff_calibrated northHexagonFourZeroData).1 h
  change northHexagonEvenShadow + (0 : KuuNativeF55Shadow) =
    northHexagonOddShadow at hcal
  have heq : northHexagonEvenShadow = northHexagonOddShadow := by
    simpa only [add_zero] using hcal
  exact northHexagonEvenOddShadow_phase_ne (congrArg Prod.snd heq)

#print axioms NativeHexagonFourBoundaryData
#print axioms NativeHexagonFourRaw
#print axioms NativeHexagonFourRaw.leadingTag
#print axioms nativeHexagonRawUpper_ne_lower
#print axioms nativeHexagonFourComp
#print axioms nativeHexagonFourEval_comp
#print axioms nativeHexagonFourCategory
#print axioms nativeHexagonFourEval_injective
#print axioms nativeHexagonFourSquare_iff_calibrated
#print axioms northHexagonFourData_calibrated
#print axioms northHexagonFourSquare_commutes
#print axioms nativeHexagonFourCorrection_unique
#print axioms northHexagonFourCorrection_charge_zero
#print axioms northHexagonFourCorrection_phase_ne_zero
#print axioms northHexagonFourZeroSquare_not_commutative

end
end Kuu.F112.Physical
