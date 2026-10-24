import Kuu.F112.PolygonNativeF55P94DK5TypedNineCellUnitObstruction
import Mathlib.Tactic

/-!
# F112-P94D3AF — 9D quotient, strict local 8-cell groupoid,
and universal-word descent obstruction

An actual source-typed nine-cell witness relates TWO original
eight-cell proof terms. Only after quotienting by these new 9D
witnesses do we obtain a strict local 8-cell groupoid on the
ORIGINAL seven-cell objects. The new unitDiamond relates genuinely
distinct raw eight-cell terms.

The signed unit-generator count descends and is additive, but
the noncommutative free-group unitWord does not descend, as
demonstrated by the concrete genuine unit critical pair.
This precisely separates raw 8D evidence, 9D connectivity,
quotient equality and chosen history observers.
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

section LocalNineCellQuotient

variable {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable {first : KuuNativeF45Tree p n m ma pa mb pb}
variable {last : KuuNativeF45Tree p n' m' ma pa mb pb}
variable {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
variable {f g : NativeF55StructuralComparison p r s}
variable {alpha beta : NativeK5StructuralFourCell p f g}
variable {w z : NativeK5StructuralFiveCell p alpha beta}
variable {u v : NativeK5StructuralSixCell p w z}

/-- Exact nine-cell connectivity, NOT raw equality of eight-cells. -/
def NativeK5StructuralNineCell.setoid
    {h k : NativeK5StructuralSevenCell p u v} :
    Setoid (NativeK5StructuralEightCell p h k) where
  r := fun e d => Nonempty (NativeK5StructuralNineCell p e d)
  iseqv := ⟨
    (fun e => ⟨.core (.refl e)⟩),
    (fun he => he.elim (fun q => ⟨.symm q⟩)),
    (fun he hd => he.elim (fun q => hd.elim (fun q' => ⟨.trans q q'⟩)))⟩

/-- Classes of ORIGINAL EIGHT-cell proofs on fixed exact 7D
endpoints, modulo only genuine newly adjoined NINE-cell witnesses. -/
abbrev NativeK5NineCellEightClasses
    (h k : NativeK5StructuralSevenCell p u v) :=
  Quotient (NativeK5StructuralNineCell.setoid (h := h) (k := k))

def nativeK5NineCellEightClass
    {h k : NativeK5StructuralSevenCell p u v}
    (e : NativeK5StructuralEightCell p h k) :
    NativeK5NineCellEightClasses h k :=
  Quotient.mk _ e

/-- Integer-valued unit-normalization count descends through
the entire new nine-cell syntax, including the unitDiamond. -/
def nativeK5NineCellEightUnitCount
    {h k : NativeK5StructuralSevenCell p u v} :
    NativeK5NineCellEightClasses h k → ℤ :=
  Quotient.lift (fun e : NativeK5StructuralEightCell p h k => e.unitCount)
    (by
      intro e d ⟨nine⟩
      exact nine.unitCount_sound)

/-- Original 8D composition respects 9D quotient in each argument. -/
def nativeK5NineCellEightVerticalComp
    {h k l : NativeK5StructuralSevenCell p u v}
    (e : NativeK5NineCellEightClasses h k)
    (d : NativeK5NineCellEightClasses k l) :
    NativeK5NineCellEightClasses h l :=
  Quot.liftOn₂ e d
    (fun x y => nativeK5NineCellEightClass (.trans x y))
    (by
      intro x y y' heq
      rcases heq with ⟨nine⟩
      exact Quot.sound ⟨NativeK5StructuralNineCell.verticalRight x nine⟩)
    (by
      intro x x' y heq
      rcases heq with ⟨nine⟩
      exact Quot.sound ⟨NativeK5StructuralNineCell.verticalLeft nine y⟩)

/-- The original eight-cell inverse is well-defined modulo 9D. -/
def nativeK5NineCellEightInverse
    {h k : NativeK5StructuralSevenCell p u v}
    (e : NativeK5NineCellEightClasses h k) :
    NativeK5NineCellEightClasses k h :=
  Quot.liftOn e
    (fun raw => nativeK5NineCellEightClass (.symm raw))
    (by
      intro x y heq
      rcases heq with ⟨nine⟩
      exact Quot.sound ⟨NativeK5StructuralNineCell.inverseRespect nine⟩)

/-- A LOCAL strict mathlib Groupoid of ORIGINAL Type-valued
seven-cell witnesses as objects and NINE-cell classes of old
eight-cell evidence as arrows. No global strict n-category claim. -/
@[reducible] def nativeK5NineCellEightVerticalGroupoid
    (w0 z0 : NativeK5StructuralFiveCell p alpha beta)
    (u0 v0 : NativeK5StructuralSixCell p w0 z0) :
    Groupoid (NativeK5StructuralSevenCell p u0 v0) where
  Hom := fun h k => NativeK5NineCellEightClasses h k
  id h := nativeK5NineCellEightClass (.core (.refl h))
  comp e d := nativeK5NineCellEightVerticalComp e d
  id_comp := by
    intro X Y e
    refine Quot.inductionOn e (fun raw => ?_)
    change nativeK5NineCellEightClass (.trans (.core (.refl X)) raw) =
      nativeK5NineCellEightClass raw
    exact Quot.sound ⟨NativeK5StructuralNineCell.core
      (NativeK5CoreNineCell.eightLeftUnit raw)⟩
  comp_id := by
    intro X Y e
    refine Quot.inductionOn e (fun raw => ?_)
    change nativeK5NineCellEightClass (.trans raw (.core (.refl Y))) =
      nativeK5NineCellEightClass raw
    exact Quot.sound ⟨NativeK5StructuralNineCell.core
      (NativeK5CoreNineCell.eightRightUnit raw)⟩
  assoc := by
    intro W X Y Z e d t
    refine Quot.inductionOn e (fun x => ?_)
    refine Quot.inductionOn d (fun y => ?_)
    refine Quot.inductionOn t (fun z => ?_)
    change nativeK5NineCellEightClass (.trans (.trans x y) z) =
      nativeK5NineCellEightClass (.trans x (.trans y z))
    exact Quot.sound ⟨NativeK5StructuralNineCell.core
      (NativeK5CoreNineCell.eightAssoc x y z)⟩
  inv := fun {X Y} e => nativeK5NineCellEightInverse e
  inv_comp := by
    intro X Y e
    refine Quot.inductionOn e (fun raw => ?_)
    change nativeK5NineCellEightClass (.trans (.symm raw) raw) =
      nativeK5NineCellEightClass (.core (.refl Y))
    exact Quot.sound ⟨NativeK5StructuralNineCell.core
      (NativeK5CoreNineCell.eightInverseRight raw)⟩
  comp_inv := by
    intro X Y e
    refine Quot.inductionOn e (fun raw => ?_)
    change nativeK5NineCellEightClass (.trans raw (.symm raw)) =
      nativeK5NineCellEightClass (.core (.refl X))
    exact Quot.sound ⟨NativeK5StructuralNineCell.core
      (NativeK5CoreNineCell.eightInverseLeft raw)⟩

/-- The newly identified 8D classes have exact same integer charge. -/
theorem nativeK5NineCellEightUnitCount_comp
    {h k l : NativeK5StructuralSevenCell p u v}
    (e : NativeK5NineCellEightClasses h k)
    (d : NativeK5NineCellEightClasses k l) :
    nativeK5NineCellEightUnitCount (nativeK5NineCellEightVerticalComp e d) =
      nativeK5NineCellEightUnitCount e + nativeK5NineCellEightUnitCount d := by
  refine Quot.inductionOn e (fun x => ?_)
  refine Quot.inductionOn d (fun y => ?_)
  rfl

/-- The two original raw eight-cell proof witnesses become equal
ONLY in the NEW quotient by an actual nine-cell unitDiamond. -/
theorem nativeK5EightUnitPair_nineQuotient_eq
    (h : NativeK5StructuralSevenCell p u v) :
    nativeK5NineCellEightClass (nativeK5EightUnitLeftFirst h) =
      nativeK5NineCellEightClass (nativeK5EightUnitRightFirst h) :=
  Quot.sound ⟨NativeK5StructuralNineCell.unitDiamond h⟩

/-- A noncommutative universal free-word observer CANNOT factor
through the genuine 9D quotient. Otherwise the two same-class
eight-cell witnesses would have equal freely ordered histories,
contradicting the certified noncommutative critical pair. -/
theorem nativeK5EightUnitWord_noNineDescent
    (h : NativeK5StructuralSevenCell p u v) :
    ¬ ∃ (F : NativeK5NineCellEightClasses
        (.trans (.trans (.core (.refl u)) h) (.core (.refl v))) h →
        NativeK5EightUnitWord),
      ∀ e : NativeK5StructuralEightCell p
        (.trans (.trans (.core (.refl u)) h) (.core (.refl v))) h,
        F (nativeK5NineCellEightClass e) = e.unitWord := by
  rintro ⟨F, hF⟩
  have hs := nativeK5EightUnitPair_nineQuotient_eq h
  have hw :
      (nativeK5EightUnitLeftFirst h).unitWord =
        (nativeK5EightUnitRightFirst h).unitWord := by
    calc
      (nativeK5EightUnitLeftFirst h).unitWord =
          F (nativeK5NineCellEightClass (nativeK5EightUnitLeftFirst h)) :=
        (hF _).symm
      _ = F (nativeK5NineCellEightClass (nativeK5EightUnitRightFirst h)) :=
        congrArg F hs
      _ = (nativeK5EightUnitRightFirst h).unitWord := hF _
  exact nativeK5EightUnitPair_word_ne h hw

end LocalNineCellQuotient

#print axioms NativeK5StructuralNineCell.setoid
#print axioms NativeK5NineCellEightClasses
#print axioms nativeK5NineCellEightClass
#print axioms nativeK5NineCellEightUnitCount
#print axioms nativeK5NineCellEightVerticalComp
#print axioms nativeK5NineCellEightInverse
#print axioms nativeK5NineCellEightVerticalGroupoid
#print axioms nativeK5NineCellEightUnitCount_comp
#print axioms nativeK5EightUnitPair_nineQuotient_eq
#print axioms nativeK5EightUnitWord_noNineDescent

end
end Kuu.F112.Physical
