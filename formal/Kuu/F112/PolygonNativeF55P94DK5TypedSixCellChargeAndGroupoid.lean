import Kuu.F112.PolygonNativeF55P94DK5TypedSixCellNaturalityCube
import Mathlib.Tactic

/-!
# F112-P94D3Z — higher typed 5/6 congruence and signed interchanger charge

The INDEPENDENT Type-valued 6-cell syntax of P94D3Z supplies
genuine relations between 5-cell terms. Prove closure, descend
vertical 5-cell operations, and construct the locally strict Mathlib
groupoid of 4-cell objects and 5-cell quotient morphisms.

A new SIGNED integer observer counts fundamental 5D interchanger
generators, rather than treating equality of old Peiffer *images*
as evidence of a 6-cell. It is proved sound for ALL 6-cell
constructors, including independent naturality 6-cells and both
5-cell horizontal squares. The count descends to the proof-evidence
quotient; unequal counts strictly obstruct any source-typed 6-cell.

This is a relative consistency/obstruction result for a NEW free
higher presentation, not an old P92B 6-cell existence theorem,
not global strict 3/n, and not hyperdescent.
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

/-- A SIGNED integer charge on proof-relevant FIVE-cell terms.
The generator interchanger has charge +1; the reverse has -1.
Each original structural functoriality rule is independently
assigned its strictly stated formal charge. It is NOT inferred
from the Peiffer boundary (which is fixed by endpoints). -/
def NativeK5StructuralFiveCell.interchangerCharge
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55StructuralComparison p r s}
    {alpha beta : NativeK5StructuralFourCell p f g}
    (w : NativeK5StructuralFiveCell p alpha beta) : ℤ :=
  match w with
  | .refl _ => 0
  | .symm w => -w.interchangerCharge
  | .trans w z => w.interchangerCharge + z.interchangerCharge
  | .verticalLeft w _ => w.interchangerCharge
  | .verticalRight _ w => w.interchangerCharge
  | .verticalAssoc _ _ _ => 0
  | .verticalLeftUnit _ => 0
  | .verticalRightUnit _ => 0
  | .inverseLeft _ => 0
  | .inverseRight _ => 0
  | .inverseRespect w => -w.interchangerCharge
  | .interchanger _ _ => 1
  | .precompose _ w => w.interchangerCharge
  | .postcompose w _ => w.interchangerCharge

/-- Every chosen 6D elementary coherence respects the signed
interchanger count, including the mixed naturality consequences.
This proof is a complete induction over ALL six-cell generators. -/
theorem NativeK5StructuralSixCell.charge_sound
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55StructuralComparison p r s}
    {alpha beta : NativeK5StructuralFourCell p f g}
    {w z : NativeK5StructuralFiveCell p alpha beta}
    (u : NativeK5StructuralSixCell p w z) :
    w.interchangerCharge = z.interchangerCharge := by
  induction u with
  | refl _ => rfl
  | symm _ ih => exact ih.symm
  | trans _ _ ih₁ ih₂ => exact ih₁.trans ih₂
  | verticalLeft witness suffix ih =>
      simpa only [NativeK5StructuralFiveCell.interchangerCharge] using
        congrArg (fun t : ℤ => t + suffix.interchangerCharge) ih
  | verticalRight lead witness ih =>
      simpa only [NativeK5StructuralFiveCell.interchangerCharge] using
        congrArg (fun t : ℤ => lead.interchangerCharge + t) ih
  | verticalAssoc a b c =>
      change (a.interchangerCharge + b.interchangerCharge) +
        c.interchangerCharge =
        a.interchangerCharge + (b.interchangerCharge + c.interchangerCharge)
      exact add_assoc _ _ _
  | verticalLeftUnit _ => simp [NativeK5StructuralFiveCell.interchangerCharge]
  | verticalRightUnit _ => simp [NativeK5StructuralFiveCell.interchangerCharge]
  | inverseLeft _ => simp [NativeK5StructuralFiveCell.interchangerCharge]
  | inverseRight _ => simp [NativeK5StructuralFiveCell.interchangerCharge]
  | inverseRespect witness ih =>
      simpa only [NativeK5StructuralFiveCell.interchangerCharge] using
        congrArg (fun t : ℤ => -t) ih
  | interchangerLeftNaturality w beta =>
      change w.interchangerCharge + (1 : ℤ) =
        1 + w.interchangerCharge
      exact add_comm _ _
  | interchangerRightNaturality alpha w =>
      change w.interchangerCharge + (1 : ℤ) =
        1 + w.interchangerCharge
      exact add_comm _ _
  | horizontalTargetSquare w v =>
      change w.interchangerCharge + v.interchangerCharge =
        v.interchangerCharge + w.interchangerCharge
      exact add_comm _ _
  | horizontalSourceSquare w v =>
      change w.interchangerCharge + v.interchangerCharge =
        v.interchangerCharge + w.interchangerCharge
      exact add_comm _ _
  | precompose _ witness ih => exact ih
  | postcompose witness _ ih => exact ih

/-- A mismatch of five-cell interchanger charge is a TRUE obstruction
to any six-cell in THIS proof-relevant higher presentation. -/
theorem nativeK5SixCell_charge_obstruction
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55StructuralComparison p r s}
    {alpha beta : NativeK5StructuralFourCell p f g}
    (w z : NativeK5StructuralFiveCell p alpha beta)
    (h : w.interchangerCharge ≠ z.interchangerCharge) :
    ¬ Nonempty (NativeK5StructuralSixCell p w z) := by
  rintro ⟨u⟩
  exact h u.charge_sound

/-- The genuine source-typed K5 two-four-cell interchanger has
strictly positive unit 5D charge. -/
theorem nativeK5TypedInterchanger_charge_one
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55StructuralComparison p r s}
    {h k : NativeF55StructuralComparison p s t}
    (alpha : NativeK5StructuralFourCell p f g)
    (beta : NativeK5StructuralFourCell p h k) :
    (nativeK5TypedInterchanger alpha beta).interchangerCharge = 1 := rfl

/-- Source proof-relevant six-cell connectivity is a SETOID,
not a quotient by integer charge equality. -/
def NativeK5StructuralSixCell.setoid
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55StructuralComparison p r s}
    {alpha beta : NativeK5StructuralFourCell p f g} :
    Setoid (NativeK5StructuralFiveCell p alpha beta) where
  r := fun w z => Nonempty (NativeK5StructuralSixCell p w z)
  iseqv := ⟨
    (fun w => ⟨.refl w⟩),
    (fun h => h.elim (fun u => ⟨.symm u⟩)),
    (fun h k => h.elim (fun u => k.elim (fun v => ⟨.trans u v⟩)))⟩

abbrev NativeK5SixCellFiveClasses
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55StructuralComparison p r s}
    (alpha beta : NativeK5StructuralFourCell p f g) :=
  Quotient (NativeK5StructuralSixCell.setoid (alpha := alpha) (beta := beta))

def nativeK5SixCellFiveClass
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55StructuralComparison p r s}
    {alpha beta : NativeK5StructuralFourCell p f g}
    (w : NativeK5StructuralFiveCell p alpha beta) :
    NativeK5SixCellFiveClasses alpha beta :=
  Quotient.mk _ w

/-- The signed charge descends through genuine 6-cell evidence
even though it does NOT classify the new 6-cell relation. -/
def nativeK5SixCellFiveCharge
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55StructuralComparison p r s}
    {alpha beta : NativeK5StructuralFourCell p f g} :
    NativeK5SixCellFiveClasses alpha beta → ℤ :=
  Quotient.lift
    (fun w : NativeK5StructuralFiveCell p alpha beta => w.interchangerCharge)
    (by intro w z ⟨u⟩; exact u.charge_sound)

/-- Vertical five-cell pasting respects independently typed
six-cell congruences in BOTH variables. -/
def nativeK5SixCellFiveVerticalComp
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55StructuralComparison p r s}
    {alpha beta gamma : NativeK5StructuralFourCell p f g}
    (w : NativeK5SixCellFiveClasses alpha beta)
    (z : NativeK5SixCellFiveClasses beta gamma) :
    NativeK5SixCellFiveClasses alpha gamma :=
  Quot.liftOn₂ w z
    (fun a b => nativeK5SixCellFiveClass (.trans a b))
    (by
      intro a b b' h
      rcases h with ⟨u⟩
      exact Quot.sound ⟨NativeK5StructuralSixCell.verticalRight a u⟩)
    (by
      intro a a' b h
      rcases h with ⟨u⟩
      exact Quot.sound ⟨NativeK5StructuralSixCell.verticalLeft u b⟩)

/-- Inverse of a five-cell class, backed by an explicit
source-level reversal-respect six-cell. -/
def nativeK5SixCellFiveInverse
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55StructuralComparison p r s}
    {alpha beta : NativeK5StructuralFourCell p f g}
    (w : NativeK5SixCellFiveClasses alpha beta) :
    NativeK5SixCellFiveClasses beta alpha :=
  Quot.liftOn w
    (fun raw => nativeK5SixCellFiveClass (.symm raw))
    (by
      intro a b h
      rcases h with ⟨u⟩
      exact Quot.sound ⟨NativeK5StructuralSixCell.inverseRespect u⟩)

/-- A strict local FIVE-cell Groupoid on actual four-cell evidence,
after quotienting ONLY the freely chosen six-cell 6D relations. -/
@[reducible] def nativeK5SixCellFiveVerticalGroupoid
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (r s : KuuNativeF45Tree.DepthRotationRoute p first last)
    (f g : NativeF55StructuralComparison p r s) :
    Groupoid (NativeK5StructuralFourCell p f g) where
  Hom := fun alpha beta => NativeK5SixCellFiveClasses alpha beta
  id alpha := nativeK5SixCellFiveClass (.refl alpha)
  comp w z := nativeK5SixCellFiveVerticalComp w z
  id_comp := by
    intro X Y w
    refine Quot.inductionOn w (fun raw => ?_)
    change nativeK5SixCellFiveClass (.trans (.refl X) raw) =
      nativeK5SixCellFiveClass raw
    exact Quot.sound ⟨NativeK5StructuralSixCell.verticalLeftUnit raw⟩
  comp_id := by
    intro X Y w
    refine Quot.inductionOn w (fun raw => ?_)
    change nativeK5SixCellFiveClass (.trans raw (.refl Y)) =
      nativeK5SixCellFiveClass raw
    exact Quot.sound ⟨NativeK5StructuralSixCell.verticalRightUnit raw⟩
  assoc := by
    intro W X Y Z w z q
    refine Quot.inductionOn w (fun a => ?_)
    refine Quot.inductionOn z (fun b => ?_)
    refine Quot.inductionOn q (fun c => ?_)
    change nativeK5SixCellFiveClass (.trans (.trans a b) c) =
      nativeK5SixCellFiveClass (.trans a (.trans b c))
    exact Quot.sound ⟨NativeK5StructuralSixCell.verticalAssoc a b c⟩
  inv := fun {X Y} w => nativeK5SixCellFiveInverse w
  inv_comp := by
    intro X Y w
    refine Quot.inductionOn w (fun raw => ?_)
    change nativeK5SixCellFiveClass (.trans (.symm raw) raw) =
      nativeK5SixCellFiveClass (.refl Y)
    exact Quot.sound ⟨NativeK5StructuralSixCell.inverseRight raw⟩
  comp_inv := by
    intro X Y w
    refine Quot.inductionOn w (fun raw => ?_)
    change nativeK5SixCellFiveClass (.trans raw (.symm raw)) =
      nativeK5SixCellFiveClass (.refl X)
    exact Quot.sound ⟨NativeK5StructuralSixCell.inverseLeft raw⟩

/-- The genuine six-cell quotient has an ADDITIVE horizontal
interchanger-charge law for vertical 5-cell composition. -/
theorem nativeK5SixCellFiveCharge_comp
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55StructuralComparison p r s}
    {alpha beta gamma : NativeK5StructuralFourCell p f g}
    (w : NativeK5SixCellFiveClasses alpha beta)
    (z : NativeK5SixCellFiveClasses beta gamma) :
    nativeK5SixCellFiveCharge (nativeK5SixCellFiveVerticalComp w z) =
      nativeK5SixCellFiveCharge w + nativeK5SixCellFiveCharge z := by
  refine Quot.inductionOn w (fun a => ?_)
  refine Quot.inductionOn z (fun b => ?_)
  rfl

#print axioms NativeK5StructuralFiveCell.interchangerCharge
#print axioms NativeK5StructuralSixCell.charge_sound
#print axioms nativeK5SixCell_charge_obstruction
#print axioms nativeK5TypedInterchanger_charge_one
#print axioms NativeK5StructuralSixCell.setoid
#print axioms NativeK5SixCellFiveClasses
#print axioms nativeK5SixCellFiveCharge
#print axioms nativeK5SixCellFiveVerticalComp
#print axioms nativeK5SixCellFiveInverse
#print axioms nativeK5SixCellFiveVerticalGroupoid
#print axioms nativeK5SixCellFiveCharge_comp

end
end Kuu.F112.Physical
