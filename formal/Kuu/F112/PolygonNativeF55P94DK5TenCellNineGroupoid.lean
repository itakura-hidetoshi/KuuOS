import Kuu.F112.PolygonNativeF55P94DK5TypedTenCellSquareComparison
import Mathlib.Tactic

/-!
# F112-P94D3AG — 10D connectivity quotient and local NINE-cell groupoid

Relate original source-dependent NINE-cell witness terms by actual
Type-valued TEN-cell evidence, not by equality of selected group
words or equality of raw higher proof terms.

The ten-cell quotient admits a LOCAL strict mathlib Groupoid whose
objects are original EIGHT-cell proof terms and whose morphisms
are TEN-cell classes of original NINE-cell witnesses.  The new
ten-cell squareExchange makes the two original 9D pastings equal
only in this quotient.

Signed nine-cell diamond count descends, while the free-group word
observer does NOT descend because the two 9D paths have different
noncommutative histories. No old P92B 10D descent, global strict
3/n-category or arbitrary 10D coherence is asserted.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

section LocalTenCellQuotient

variable {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable {first : KuuNativeF45Tree p n m ma pa mb pb}
variable {last : KuuNativeF45Tree p n' m' ma pa mb pb}
variable {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
variable {f g : NativeF55StructuralComparison p r s}
variable {alpha beta : NativeK5StructuralFourCell p f g}
variable {w z : NativeK5StructuralFiveCell p alpha beta}
variable {u v : NativeK5StructuralSixCell p w z}
variable {h k : NativeK5StructuralSevenCell p u v}

/-- Actual 10D connectivity between parallel genuinely typed
NINE-cell proof terms, at fixed original EIGHT-cell endpoints. -/
def NativeK5StructuralTenCell.setoid
    {e d : NativeK5StructuralEightCell p h k} :
    Setoid (NativeK5StructuralNineCell p e d) where
  r := fun q t => Nonempty (NativeK5StructuralTenCell p q t)
  iseqv := ⟨
    (fun q => ⟨.core (.refl q)⟩),
    (fun H => H.elim (fun a => ⟨.symm a⟩)),
    (fun H K => H.elim (fun a => K.elim (fun b => ⟨.trans a b⟩)))⟩

/-- Original nine-cell evidence modulo ONLY genuine 10D relations.
No raw proof-term extensionality is imposed. -/
abbrev NativeK5TenCellNineClasses
    (e d : NativeK5StructuralEightCell p h k) :=
  Quotient (NativeK5StructuralTenCell.setoid (e := e) (d := d))

def nativeK5TenCellNineClass
    {e d : NativeK5StructuralEightCell p h k}
    (q : NativeK5StructuralNineCell p e d) :
    NativeK5TenCellNineClasses e d :=
  Quotient.mk _ q

/-- Integer 9D diamond count survives all authentic newly adjoined
10D comparison evidence, including independent squareExchange. -/
def nativeK5TenCellNineDiamondCount
    {e d : NativeK5StructuralEightCell p h k} :
    NativeK5TenCellNineClasses e d → ℤ :=
  Quotient.lift
    (fun q : NativeK5StructuralNineCell p e d => q.diamondCount)
    (by
      intro q t ⟨ten⟩
      exact ten.diamondCount_sound)

/-- Genuine 9D vertical composition respects the new 10D quotient
in BOTH variables, by independent Type-valued 10D congruences. -/
def nativeK5TenCellNineVerticalComp
    {e d t : NativeK5StructuralEightCell p h k}
    (q : NativeK5TenCellNineClasses e d)
    (z : NativeK5TenCellNineClasses d t) :
    NativeK5TenCellNineClasses e t :=
  Quot.liftOn₂ q z
    (fun a b => nativeK5TenCellNineClass (.trans a b))
    (by
      intro a b b' eq
      rcases eq with ⟨ten⟩
      exact Quot.sound ⟨NativeK5StructuralTenCell.nineVerticalRight a ten⟩)
    (by
      intro a a' b eq
      rcases eq with ⟨ten⟩
      exact Quot.sound ⟨NativeK5StructuralTenCell.nineVerticalLeft ten b⟩)

/-- Original nine-cell inversion respects the new 10D quotient. -/
def nativeK5TenCellNineInverse
    {e d : NativeK5StructuralEightCell p h k}
    (q : NativeK5TenCellNineClasses e d) :
    NativeK5TenCellNineClasses d e :=
  Quot.liftOn q
    (fun raw => nativeK5TenCellNineClass (.symm raw))
    (by
      intro a b eq
      rcases eq with ⟨ten⟩
      exact Quot.sound ⟨NativeK5StructuralTenCell.nineSymmRespect ten⟩)

/-- Strict LOCAL mathlib 9-cell groupoid: original EIGHT-cell
objects and classes of original NINE-cell evidence as arrows. -/
@[reducible] def nativeK5TenCellNineVerticalGroupoid
    (w0 z0 : NativeK5StructuralFiveCell p alpha beta)
    (u0 v0 : NativeK5StructuralSixCell p w0 z0)
    (h0 k0 : NativeK5StructuralSevenCell p u0 v0) :
    Groupoid (NativeK5StructuralEightCell p h0 k0) where
  Hom := fun e d => NativeK5TenCellNineClasses e d
  id e := nativeK5TenCellNineClass (.core (.refl e))
  comp q z := nativeK5TenCellNineVerticalComp q z
  id_comp := by
    intro X Y q
    refine Quot.inductionOn q (fun raw => ?_)
    change nativeK5TenCellNineClass (.trans (.core (.refl X)) raw) =
      nativeK5TenCellNineClass raw
    exact Quot.sound ⟨NativeK5StructuralTenCell.core
      (NativeK5CoreTenCell.nineLeftUnit raw)⟩
  comp_id := by
    intro X Y q
    refine Quot.inductionOn q (fun raw => ?_)
    change nativeK5TenCellNineClass (.trans raw (.core (.refl Y))) =
      nativeK5TenCellNineClass raw
    exact Quot.sound ⟨NativeK5StructuralTenCell.core
      (NativeK5CoreTenCell.nineRightUnit raw)⟩
  assoc := by
    intro W X Y Z q z t
    refine Quot.inductionOn q (fun a => ?_)
    refine Quot.inductionOn z (fun b => ?_)
    refine Quot.inductionOn t (fun c => ?_)
    change nativeK5TenCellNineClass (.trans (.trans a b) c) =
      nativeK5TenCellNineClass (.trans a (.trans b c))
    exact Quot.sound ⟨NativeK5StructuralTenCell.core
      (NativeK5CoreTenCell.nineAssoc a b c)⟩
  inv := fun {X Y} q => nativeK5TenCellNineInverse q
  inv_comp := by
    intro X Y q
    refine Quot.inductionOn q (fun raw => ?_)
    change nativeK5TenCellNineClass (.trans (.symm raw) raw) =
      nativeK5TenCellNineClass (.core (.refl Y))
    exact Quot.sound ⟨NativeK5StructuralTenCell.core
      (NativeK5CoreTenCell.nineInverseRight raw)⟩
  comp_inv := by
    intro X Y q
    refine Quot.inductionOn q (fun raw => ?_)
    change nativeK5TenCellNineClass (.trans raw (.symm raw)) =
      nativeK5TenCellNineClass (.core (.refl X))
    exact Quot.sound ⟨NativeK5StructuralTenCell.core
      (NativeK5CoreTenCell.nineInverseLeft raw)⟩

/-- Signed diamond count is additive on the new 10D quotient. -/
theorem nativeK5TenCellNineDiamondCount_comp
    {e d t : NativeK5StructuralEightCell p h k}
    (q : NativeK5TenCellNineClasses e d)
    (z : NativeK5TenCellNineClasses d t) :
    nativeK5TenCellNineDiamondCount
        (nativeK5TenCellNineVerticalComp q z) =
      nativeK5TenCellNineDiamondCount q +
        nativeK5TenCellNineDiamondCount z := by
  refine Quot.inductionOn q (fun a => ?_)
  refine Quot.inductionOn z (fun b => ?_)
  rfl

/-- The source-typed original 9D double-whiskering witnesses are
equal ONLY after quotienting by the actual new Type-valued 10D
square exchange comparison. -/
theorem nativeK5NinePasting_tenQuotient_eq
    {e d : NativeK5StructuralEightCell p h k}
    (q : NativeK5StructuralNineCell p e d) :
    nativeK5TenCellNineClass (nativeK5NinePastingLeftThenRight q) =
      nativeK5TenCellNineClass (nativeK5NinePastingRightThenLeft q) :=
  Quot.sound ⟨NativeK5StructuralTenCell.squareExchange q⟩

/-- Noncommutative free history does NOT descend to the 10D quotient.
The obstruction is witnessed by the real independent 9D unitDiamond. -/
theorem nativeK5NineHistoryWord_noTenDescent
    (h0 : NativeK5StructuralSevenCell p u v) :
    ¬ ∃ (F : NativeK5TenCellNineClasses
        (.trans (nativeK5EightUnitLeftFirst h0)
          (.symm (nativeK5EightUnitLeftFirst h0)))
        (.trans (nativeK5EightUnitRightFirst h0)
          (.symm (nativeK5EightUnitRightFirst h0))) →
        NativeK5NineHistoryWord),
      ∀ q : NativeK5StructuralNineCell p
        (.trans (nativeK5EightUnitLeftFirst h0)
          (.symm (nativeK5EightUnitLeftFirst h0)))
        (.trans (nativeK5EightUnitRightFirst h0)
          (.symm (nativeK5EightUnitRightFirst h0))),
        F (nativeK5TenCellNineClass q) = q.historyWord := by
  rintro ⟨F, hF⟩
  have heq :=
    nativeK5NinePasting_tenQuotient_eq
      (NativeK5StructuralNineCell.unitDiamond h0)
  have hword :
      (nativeK5NinePastingLeftThenRight
        (NativeK5StructuralNineCell.unitDiamond h0)).historyWord =
      (nativeK5NinePastingRightThenLeft
        (NativeK5StructuralNineCell.unitDiamond h0)).historyWord := by
    calc
      (nativeK5NinePastingLeftThenRight
        (NativeK5StructuralNineCell.unitDiamond h0)).historyWord =
          F (nativeK5TenCellNineClass (nativeK5NinePastingLeftThenRight
            (NativeK5StructuralNineCell.unitDiamond h0))) := (hF _).symm
      _ = F (nativeK5TenCellNineClass (nativeK5NinePastingRightThenLeft
            (NativeK5StructuralNineCell.unitDiamond h0))) := congrArg F heq
      _ = (nativeK5NinePastingRightThenLeft
          (NativeK5StructuralNineCell.unitDiamond h0)).historyWord := hF _
  exact nativeK5NineUnitDiamond_pastingWord_ne h0 hword

end LocalTenCellQuotient

#print axioms NativeK5StructuralTenCell.setoid
#print axioms NativeK5TenCellNineClasses
#print axioms nativeK5TenCellNineClass
#print axioms nativeK5TenCellNineDiamondCount
#print axioms nativeK5TenCellNineVerticalComp
#print axioms nativeK5TenCellNineInverse
#print axioms nativeK5TenCellNineVerticalGroupoid
#print axioms nativeK5TenCellNineDiamondCount_comp
#print axioms nativeK5NinePasting_tenQuotient_eq
#print axioms nativeK5NineHistoryWord_noTenDescent

end
end Kuu.F112.Physical
