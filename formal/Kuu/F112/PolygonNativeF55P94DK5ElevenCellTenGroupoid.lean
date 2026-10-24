import Kuu.F112.PolygonNativeF55P94DK5TypedElevenCellSquareComparison
import Mathlib.Tactic

/-!
# F112-P94D3AH — genuine eleven-cell quotient and local ten-cell groupoid

Only actual Type-valued ELEVEN-cell evidence identifies two old
TEN-cell proof terms. This defines a setoid and quotient at EXACT
original nine-cell endpoints, and a strict LOCAL mathlib Groupoid
on the old 9D objects with 11D classes of 10D evidence as arrows.

The independently adjoined 11D squareExchange identifies the two
distinct raw ten-cell pastings in the new quotient. The signed
10D exchange count is additive and descends; the chosen nonabelian
free-group 10D history does not.

We also prove an EXACT necessary-and-sufficient criterion for any
observer to factor through each genuine 11D quotient fiber. This
clarifies the obstruction a future boundary-preserving P92B
comparison must meet, without pretending such a map exists now.
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

section LocalElevenCellQuotient

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
variable {e d : NativeK5StructuralEightCell p h k}

/-- Genuine 11D connectivity on original 10D proof evidence.
It is NOT raw equality of Type-valued ten-cell witnesses. -/
def NativeK5StructuralElevenCell.setoid
    {q t : NativeK5StructuralNineCell p e d} :
    Setoid (NativeK5StructuralTenCell p q t) where
  r := fun P Q => Nonempty (NativeK5StructuralElevenCell p P Q)
  iseqv := ⟨
    (fun P => ⟨.core (.refl P)⟩),
    (fun H => H.elim (fun R => ⟨.symm R⟩)),
    (fun H K => H.elim (fun R => K.elim (fun S => ⟨.trans R S⟩)))⟩

/-- Original 10D evidence classes modulo source-typed 11D
comparisons, at fixed original dependent NINE-cell boundaries. -/
abbrev NativeK5ElevenCellTenClasses
    (q t : NativeK5StructuralNineCell p e d) :=
  Quotient (NativeK5StructuralElevenCell.setoid (q := q) (t := t))

def nativeK5ElevenCellTenClass
    {q t : NativeK5StructuralNineCell p e d}
    (P : NativeK5StructuralTenCell p q t) :
    NativeK5ElevenCellTenClasses q t :=
  Quotient.mk _ P

/-- Exact criterion for a candidate (possibly noncommutative)
observer to descend through the genuine eleven-cell quotient.
This is an iff in the existing dependent boundary fiber, not an
assertion of existence of an external P92B 11D carrier. -/
theorem nativeK5ElevenObserver_factors_iff
    {q t : NativeK5StructuralNineCell p e d}
    {A : Type*}
    (obs : NativeK5StructuralTenCell p q t → A) :
    (∃ F : NativeK5ElevenCellTenClasses q t → A,
        ∀ P, F (nativeK5ElevenCellTenClass P) = obs P) ↔
      (∀ P Q : NativeK5StructuralTenCell p q t,
        Nonempty (NativeK5StructuralElevenCell p P Q) →
          obs P = obs Q) := by
  constructor
  · rintro ⟨F, hF⟩ P Q related
    calc
      obs P = F (nativeK5ElevenCellTenClass P) := (hF P).symm
      _ = F (nativeK5ElevenCellTenClass Q) :=
        congrArg F (Quot.sound related)
      _ = obs Q := hF Q
  · intro compatible
    refine ⟨Quotient.lift obs (by
      intro P Q related
      exact compatible P Q related), ?_⟩
    intro P
    rfl

/-- Coarse signed 10D exchange count descends through all genuine
ELEVEN-cell comparisons, including the new squareExchange. -/
def nativeK5ElevenCellTenExchangeCount
    {q t : NativeK5StructuralNineCell p e d} :
    NativeK5ElevenCellTenClasses q t → ℤ :=
  Quotient.lift
    (fun P : NativeK5StructuralTenCell p q t => P.exchangeCount)
    (by
      intro P Q ⟨eleven⟩
      exact eleven.exchangeCount_sound)

/-- Vertical ten-cell composition preserves genuine 11D quotient
classes in BOTH variables using original 11D congruence witnesses. -/
def nativeK5ElevenCellTenVerticalComp
    {q t j : NativeK5StructuralNineCell p e d}
    (P : NativeK5ElevenCellTenClasses q t)
    (Q : NativeK5ElevenCellTenClasses t j) :
    NativeK5ElevenCellTenClasses q j :=
  Quot.liftOn₂ P Q
    (fun a b => nativeK5ElevenCellTenClass (.trans a b))
    (by
      intro a b b' hb
      rcases hb with ⟨eleven⟩
      exact Quot.sound ⟨NativeK5StructuralElevenCell.tenVerticalRight a eleven⟩)
    (by
      intro a a' b ha
      rcases ha with ⟨eleven⟩
      exact Quot.sound ⟨NativeK5StructuralElevenCell.tenVerticalLeft eleven b⟩)

/-- Inverting a ten-cell is well-defined on the new quotient,
by actual Type-valued 11D inverse congruence. -/
def nativeK5ElevenCellTenInverse
    {q t : NativeK5StructuralNineCell p e d}
    (P : NativeK5ElevenCellTenClasses q t) :
    NativeK5ElevenCellTenClasses t q :=
  Quot.liftOn P
    (fun raw => nativeK5ElevenCellTenClass (.symm raw))
    (by
      intro a b related
      rcases related with ⟨eleven⟩
      exact Quot.sound ⟨NativeK5StructuralElevenCell.tenSymmRespect eleven⟩)

/-- Strict LOCAL mathlib TEN-cell groupoid after quotienting by
genuine 11D evidence: original 9D proof objects, 10D witnesses
modulo 11D comparisons as morphisms. -/
@[reducible] def nativeK5ElevenCellTenVerticalGroupoid
    (w0 z0 : NativeK5StructuralFiveCell p alpha beta)
    (u0 v0 : NativeK5StructuralSixCell p w0 z0)
    (h0 k0 : NativeK5StructuralSevenCell p u0 v0)
    (e0 d0 : NativeK5StructuralEightCell p h0 k0) :
    Groupoid (NativeK5StructuralNineCell p e0 d0) where
  Hom := fun q t => NativeK5ElevenCellTenClasses q t
  id q := nativeK5ElevenCellTenClass (.core (.refl q))
  comp P Q := nativeK5ElevenCellTenVerticalComp P Q
  id_comp := by
    intro X Y P
    refine Quot.inductionOn P (fun raw => ?_)
    change nativeK5ElevenCellTenClass (.trans (.core (.refl X)) raw) =
      nativeK5ElevenCellTenClass raw
    exact Quot.sound ⟨NativeK5StructuralElevenCell.core
      (NativeK5CoreElevenCell.tenLeftUnit raw)⟩
  comp_id := by
    intro X Y P
    refine Quot.inductionOn P (fun raw => ?_)
    change nativeK5ElevenCellTenClass (.trans raw (.core (.refl Y))) =
      nativeK5ElevenCellTenClass raw
    exact Quot.sound ⟨NativeK5StructuralElevenCell.core
      (NativeK5CoreElevenCell.tenRightUnit raw)⟩
  assoc := by
    intro W X Y Z P Q R
    refine Quot.inductionOn P (fun a => ?_)
    refine Quot.inductionOn Q (fun b => ?_)
    refine Quot.inductionOn R (fun c => ?_)
    change nativeK5ElevenCellTenClass (.trans (.trans a b) c) =
      nativeK5ElevenCellTenClass (.trans a (.trans b c))
    exact Quot.sound ⟨NativeK5StructuralElevenCell.core
      (NativeK5CoreElevenCell.tenAssoc a b c)⟩
  inv := fun {X Y} P => nativeK5ElevenCellTenInverse P
  inv_comp := by
    intro X Y P
    refine Quot.inductionOn P (fun raw => ?_)
    change nativeK5ElevenCellTenClass (.trans (.symm raw) raw) =
      nativeK5ElevenCellTenClass (.core (.refl Y))
    exact Quot.sound ⟨NativeK5StructuralElevenCell.core
      (NativeK5CoreElevenCell.tenInverseRight raw)⟩
  comp_inv := by
    intro X Y P
    refine Quot.inductionOn P (fun raw => ?_)
    change nativeK5ElevenCellTenClass (.trans raw (.symm raw)) =
      nativeK5ElevenCellTenClass (.core (.refl X))
    exact Quot.sound ⟨NativeK5StructuralElevenCell.core
      (NativeK5CoreElevenCell.tenInverseLeft raw)⟩

/-- Signed 10D exchange charge is strictly additive on the
actual 11D quotient under original 10D vertical composition. -/
theorem nativeK5ElevenCellTenExchangeCount_comp
    {q t j : NativeK5StructuralNineCell p e d}
    (P : NativeK5ElevenCellTenClasses q t)
    (Q : NativeK5ElevenCellTenClasses t j) :
    nativeK5ElevenCellTenExchangeCount
        (nativeK5ElevenCellTenVerticalComp P Q) =
      nativeK5ElevenCellTenExchangeCount P +
        nativeK5ElevenCellTenExchangeCount Q := by
  refine Quot.inductionOn P (fun a => ?_)
  refine Quot.inductionOn Q (fun b => ?_)
  rfl

/-- Two genuinely different raw TEN-cell pasting witnesses share
a quotient class ONLY by the new Type-valued ELEVEN-cell. -/
theorem nativeK5TenPasting_elevenQuotient_eq
    {q t : NativeK5StructuralNineCell p e d}
    (P : NativeK5StructuralTenCell p q t) :
    nativeK5ElevenCellTenClass (nativeK5TenPastingLeftThenRight P) =
      nativeK5ElevenCellTenClass (nativeK5TenPastingRightThenLeft P) :=
  Quot.sound ⟨NativeK5StructuralElevenCell.squareExchange P⟩

/-- The original noncommutative history does NOT factor through
the new 11D quotient: it would identify distinct free words of
the authentic primitive 10D squareExchange. This is a concrete
failure of the iff-criterion above. -/
theorem nativeK5TenHistoryWord_noElevenDescent
    {q t : NativeK5StructuralNineCell p e d}
    (P : NativeK5StructuralTenCell p q t)
    (hneq : (nativeK5TenPastingLeftThenRight P).historyWord ≠
      (nativeK5TenPastingRightThenLeft P).historyWord) :
    ¬ ∃ (F : NativeK5ElevenCellTenClasses
        (.trans q (.symm q)) (.trans t (.symm t)) →
        NativeK5TenHistoryWord),
      ∀ R : NativeK5StructuralTenCell p
        (.trans q (.symm q)) (.trans t (.symm t)),
        F (nativeK5ElevenCellTenClass R) = R.historyWord := by
  rintro ⟨F, hF⟩
  have hrel := nativeK5TenPasting_elevenQuotient_eq P
  have heq :
      (nativeK5TenPastingLeftThenRight P).historyWord =
        (nativeK5TenPastingRightThenLeft P).historyWord := by
    calc
      (nativeK5TenPastingLeftThenRight P).historyWord =
          F (nativeK5ElevenCellTenClass
            (nativeK5TenPastingLeftThenRight P)) := (hF _).symm
      _ = F (nativeK5ElevenCellTenClass
          (nativeK5TenPastingRightThenLeft P)) := congrArg F hrel
      _ = (nativeK5TenPastingRightThenLeft P).historyWord := hF _
  exact hneq heq

end LocalElevenCellQuotient

#print axioms NativeK5StructuralElevenCell.setoid
#print axioms NativeK5ElevenCellTenClasses
#print axioms nativeK5ElevenCellTenClass
#print axioms nativeK5ElevenObserver_factors_iff
#print axioms nativeK5ElevenCellTenExchangeCount
#print axioms nativeK5ElevenCellTenVerticalComp
#print axioms nativeK5ElevenCellTenInverse
#print axioms nativeK5ElevenCellTenVerticalGroupoid
#print axioms nativeK5ElevenCellTenExchangeCount_comp
#print axioms nativeK5TenPasting_elevenQuotient_eq
#print axioms nativeK5TenHistoryWord_noElevenDescent

end
end Kuu.F112.Physical
