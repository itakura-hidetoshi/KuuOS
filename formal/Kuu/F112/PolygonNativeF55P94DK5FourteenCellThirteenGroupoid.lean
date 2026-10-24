import Kuu.F112.PolygonNativeF55P94DK5TypedFourteenCellSquareComparison
import Mathlib.Tactic

/-!
# F112-P94D3AM — strict LOCAL thirteen-cell groupoid on genuine 14D quotient

Only original source-dependent 14D comparison evidence identifies
two ORIGINAL 13D witnesses. Their raw proof terms remain distinct.
Construct genuine 14D connectivity Setoid, quotiented 13D vertical
composition/inversion, a strict LOCAL mathlib Groupoid on original
12D witnesses, and additive signed 13D count.

For ANY observer on an exact 12D dependent boundary fiber, give
an iff factorization criterion. The independently adjoined genuine
14D square compares two 13D paths that chosen noncommutative
free-group history distinguishes: that history cannot descend.

This is not global strict 3/n or arbitrary higher coherence.
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

section LocalFourteenCellQuotient

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
variable {q t : NativeK5StructuralNineCell p e d}
variable {P Q : NativeK5StructuralTenCell p q t}
variable {H K : NativeK5StructuralElevenCell p P Q}

/-- Nonempty genuine 14D comparison is an equivalence on original
13D evidence at EXACT parallel 12D dependent boundaries. -/
def NativeK5StructuralFourteenCell.setoid
    {U V : NativeK5StructuralTwelveCell p H K} :
    Setoid (NativeK5StructuralThirteenCell p U V) where
  r := fun T S => Nonempty (NativeK5StructuralFourteenCell p T S)
  iseqv := ⟨
    (fun T => ⟨.core (.refl T)⟩),
    (fun related => related.elim (fun R => ⟨.symm R⟩)),
    (fun first second =>
      first.elim (fun R => second.elim (fun S => ⟨.trans R S⟩)))⟩

abbrev NativeK5FourteenCellThirteenClasses
    (U V : NativeK5StructuralTwelveCell p H K) :=
  Quotient (NativeK5StructuralFourteenCell.setoid (U := U) (V := V))

def nativeK5FourteenCellThirteenClass
    {U V : NativeK5StructuralTwelveCell p H K}
    (T : NativeK5StructuralThirteenCell p U V) :
    NativeK5FourteenCellThirteenClasses U V :=
  Quotient.mk _ T

/-- Universal necessary-and-sufficient 14D descent criterion for
an arbitrary observer on the ORIGINAL 12D dependent boundary fiber. -/
theorem nativeK5FourteenObserver_factors_iff
    {U V : NativeK5StructuralTwelveCell p H K}
    {A : Type*}
    (obs : NativeK5StructuralThirteenCell p U V → A) :
    (∃ F : NativeK5FourteenCellThirteenClasses U V → A,
      ∀ T, F (nativeK5FourteenCellThirteenClass T) = obs T) ↔
    (∀ T S : NativeK5StructuralThirteenCell p U V,
      Nonempty (NativeK5StructuralFourteenCell p T S) →
        obs T = obs S) := by
  constructor
  · rintro ⟨F, hF⟩ T S related
    calc
      obs T = F (nativeK5FourteenCellThirteenClass T) := (hF T).symm
      _ = F (nativeK5FourteenCellThirteenClass S) :=
        congrArg F (Quot.sound related)
      _ = obs S := hF S
  · intro compatible
    refine ⟨Quotient.lift obs (by
      intro T S related
      exact compatible T S related), ?_⟩
    intro T
    rfl

/-- Genuine 13D signed square count descends along all 14D witnesses. -/
def nativeK5FourteenCellThirteenSquareCount
    {U V : NativeK5StructuralTwelveCell p H K} :
    NativeK5FourteenCellThirteenClasses U V → ℤ :=
  Quotient.lift
    (fun T : NativeK5StructuralThirteenCell p U V => T.squareCount)
    (by
      intro T S ⟨fourteen⟩
      exact fourteen.squareCount_sound)

/-- Well-defined original 13D vertical composition modulo genuine 14D. -/
def nativeK5FourteenCellThirteenVerticalComp
    {U V W : NativeK5StructuralTwelveCell p H K}
    (T : NativeK5FourteenCellThirteenClasses U V)
    (S : NativeK5FourteenCellThirteenClasses V W) :
    NativeK5FourteenCellThirteenClasses U W :=
  Quot.liftOn₂ T S
    (fun X Y => nativeK5FourteenCellThirteenClass (.trans X Y))
    (by
      intro X Y Y' related
      rcases related with ⟨fourteen⟩
      exact Quot.sound ⟨NativeK5StructuralFourteenCell.thirteenVerticalRight X fourteen⟩)
    (by
      intro X X' Y related
      rcases related with ⟨fourteen⟩
      exact Quot.sound ⟨NativeK5StructuralFourteenCell.thirteenVerticalLeft fourteen Y⟩)

def nativeK5FourteenCellThirteenInverse
    {U V : NativeK5StructuralTwelveCell p H K}
    (T : NativeK5FourteenCellThirteenClasses U V) :
    NativeK5FourteenCellThirteenClasses V U :=
  Quot.liftOn T
    (fun raw => nativeK5FourteenCellThirteenClass (.symm raw))
    (by
      intro X Y related
      rcases related with ⟨fourteen⟩
      exact Quot.sound ⟨NativeK5StructuralFourteenCell.thirteenSymmRespect fourteen⟩)

/-- Strict LOCAL mathlib Groupoid on genuine original 12D witnesses;
it is NOT a global strict 3/n-category. -/
@[reducible] def nativeK5FourteenCellThirteenVerticalGroupoid
    (w0 z0 : NativeK5StructuralFiveCell p alpha beta)
    (u0 v0 : NativeK5StructuralSixCell p w0 z0)
    (h0 k0 : NativeK5StructuralSevenCell p u0 v0)
    (e0 d0 : NativeK5StructuralEightCell p h0 k0)
    (q0 t0 : NativeK5StructuralNineCell p e0 d0)
    (P0 Q0 : NativeK5StructuralTenCell p q0 t0)
    (H0 K0 : NativeK5StructuralElevenCell p P0 Q0) :
    Groupoid (NativeK5StructuralTwelveCell p H0 K0) where
  Hom := fun U V => NativeK5FourteenCellThirteenClasses U V
  id U := nativeK5FourteenCellThirteenClass (.core (.refl U))
  comp T S := nativeK5FourteenCellThirteenVerticalComp T S
  id_comp := by
    intro X Y T
    refine Quot.inductionOn T (fun raw => ?_)
    change nativeK5FourteenCellThirteenClass (.trans (.core (.refl X)) raw) =
      nativeK5FourteenCellThirteenClass raw
    exact Quot.sound ⟨NativeK5StructuralFourteenCell.core
      (NativeK5CoreFourteenCell.thirteenLeftUnit raw)⟩
  comp_id := by
    intro X Y T
    refine Quot.inductionOn T (fun raw => ?_)
    change nativeK5FourteenCellThirteenClass (.trans raw (.core (.refl Y))) =
      nativeK5FourteenCellThirteenClass raw
    exact Quot.sound ⟨NativeK5StructuralFourteenCell.core
      (NativeK5CoreFourteenCell.thirteenRightUnit raw)⟩
  assoc := by
    intro A B C D T S Z
    refine Quot.inductionOn T (fun x => ?_)
    refine Quot.inductionOn S (fun y => ?_)
    refine Quot.inductionOn Z (fun z => ?_)
    change nativeK5FourteenCellThirteenClass (.trans (.trans x y) z) =
      nativeK5FourteenCellThirteenClass (.trans x (.trans y z))
    exact Quot.sound ⟨NativeK5StructuralFourteenCell.core
      (NativeK5CoreFourteenCell.thirteenAssoc x y z)⟩
  inv := fun {X Y} T => nativeK5FourteenCellThirteenInverse T
  inv_comp := by
    intro X Y T
    refine Quot.inductionOn T (fun raw => ?_)
    change nativeK5FourteenCellThirteenClass (.trans (.symm raw) raw) =
      nativeK5FourteenCellThirteenClass (.core (.refl Y))
    exact Quot.sound ⟨NativeK5StructuralFourteenCell.core
      (NativeK5CoreFourteenCell.thirteenInverseRight raw)⟩
  comp_inv := by
    intro X Y T
    refine Quot.inductionOn T (fun raw => ?_)
    change nativeK5FourteenCellThirteenClass (.trans raw (.symm raw)) =
      nativeK5FourteenCellThirteenClass (.core (.refl X))
    exact Quot.sound ⟨NativeK5StructuralFourteenCell.core
      (NativeK5CoreFourteenCell.thirteenInverseLeft raw)⟩

theorem nativeK5FourteenCellThirteenSquareCount_comp
    {U V W : NativeK5StructuralTwelveCell p H K}
    (T : NativeK5FourteenCellThirteenClasses U V)
    (S : NativeK5FourteenCellThirteenClasses V W) :
    nativeK5FourteenCellThirteenSquareCount
      (nativeK5FourteenCellThirteenVerticalComp T S) =
      nativeK5FourteenCellThirteenSquareCount T +
        nativeK5FourteenCellThirteenSquareCount S := by
  refine Quot.inductionOn T (fun X => ?_)
  refine Quot.inductionOn S (fun Y => ?_)
  rfl

/-- Original 13D paths become equal ONLY after genuine 14D
quotienting, via the independently added 14D source-typed witness. -/
theorem nativeK5ThirteenPasting_fourteenQuotient_eq
    {U V : NativeK5StructuralTwelveCell p H K}
    (W : NativeK5StructuralThirteenCell p U V) :
    nativeK5FourteenCellThirteenClass
      (nativeK5ThirteenPastingLeftThenRight W) =
    nativeK5FourteenCellThirteenClass
      (nativeK5ThirteenPastingRightThenLeft W) :=
  Quot.sound ⟨NativeK5StructuralFourteenCell.squareExchange W⟩

/-- Generic non-descent of the chosen full original 13D noncommutative
free-group history at a genuine 14D critical pair. -/
theorem nativeK5ThirteenHistoryWord_noFourteenDescent
    {U V : NativeK5StructuralTwelveCell p H K}
    (W : NativeK5StructuralThirteenCell p U V)
    (hneq : (nativeK5ThirteenPastingLeftThenRight W).historyWord ≠
      (nativeK5ThirteenPastingRightThenLeft W).historyWord) :
    ¬ ∃ (F : NativeK5FourteenCellThirteenClasses
      (.trans U (.symm U)) (.trans V (.symm V)) →
        NativeK5ThirteenHistoryWord),
      ∀ T : NativeK5StructuralThirteenCell p
        (.trans U (.symm U)) (.trans V (.symm V)),
        F (nativeK5FourteenCellThirteenClass T) = T.historyWord := by
  rintro ⟨F, hF⟩
  have heq := nativeK5ThirteenPasting_fourteenQuotient_eq W
  have hword :
      (nativeK5ThirteenPastingLeftThenRight W).historyWord =
        (nativeK5ThirteenPastingRightThenLeft W).historyWord := by
    calc
      (nativeK5ThirteenPastingLeftThenRight W).historyWord =
          F (nativeK5FourteenCellThirteenClass
            (nativeK5ThirteenPastingLeftThenRight W)) := (hF _).symm
      _ = F (nativeK5FourteenCellThirteenClass
          (nativeK5ThirteenPastingRightThenLeft W)) := congrArg F heq
      _ = (nativeK5ThirteenPastingRightThenLeft W).historyWord := hF _
  exact hneq hword

end LocalFourteenCellQuotient

#print axioms NativeK5StructuralFourteenCell.setoid
#print axioms NativeK5FourteenCellThirteenClasses
#print axioms nativeK5FourteenCellThirteenClass
#print axioms nativeK5FourteenObserver_factors_iff
#print axioms nativeK5FourteenCellThirteenSquareCount
#print axioms nativeK5FourteenCellThirteenVerticalComp
#print axioms nativeK5FourteenCellThirteenInverse
#print axioms nativeK5FourteenCellThirteenVerticalGroupoid
#print axioms nativeK5FourteenCellThirteenSquareCount_comp
#print axioms nativeK5ThirteenPasting_fourteenQuotient_eq
#print axioms nativeK5ThirteenHistoryWord_noFourteenDescent

end
end Kuu.F112.Physical
