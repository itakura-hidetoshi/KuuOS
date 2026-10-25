import Kuu.F112.PolygonNativeF55P94DK5FifteenCellPhysicalBridge
import Kuu.F112.PolygonNativeF55P94DIndexedFifteenCellUniversalDescent

/-!
# F112-P94D3AP — original C60 dependent fifteen-cell transport

The original fourteen-cell proof fiber between the EXACT source-dependent
thirteen-cell inverse-square boundaries is unchanged.  Specialize the
indexed independent-15D universal construction to the genuine critical
pair of P94D3AN/P94D3AO, with an EXPLICIT independent charge witness.

Establish a Type-level equivalence of the resulting quotient
presentations, not merely equality of scalar observations.  The
universal descent criterion distinguishes conservative history/charge
compatibility from preservation of the independently adjoined exchange.

No unproved 16-cell geometry, complete P92B descent, or arbitrary
higher coherence is claimed.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uD vD uE vE uB
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

section OriginalFourteenFiber

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
variable {U V : NativeK5StructuralTwelveCell p H K}

/-- The SINGLETON exchange still lives in the original dependent
fourteen-cell proof type, not in a graph of erased paths. -/
abbrev nativeK5APLeft (W : NativeK5StructuralThirteenCell p U V) :
    Unit → NativeK5FifteenFourteenFiber W :=
  fun _ => nativeK5FifteenCriticalLeft W

abbrev nativeK5APRight (W : NativeK5StructuralThirteenCell p U V) :
    Unit → NativeK5FifteenFourteenFiber W :=
  fun _ => nativeK5FifteenCriticalRight W

/-- A PROOF of charge compatibility, separate from the freely adjoined
15D generator; the count equality alone is not a raw coherence cell. -/
def nativeK5APChargeEq (W : NativeK5StructuralThirteenCell p U V) :
    ∀ i : Unit,
      nativeK5FifteenChargeObserver W (nativeK5APLeft W i) =
        nativeK5FifteenChargeObserver W (nativeK5APRight W i) := by
  intro _
  exact nativeK5FourteenPasting_integerBlind
    (NativeK5StructuralFourteenCell.squareExchange W)

/-- The indexed quotient on the exact ORIGINAL raw 14-cell fiber. -/
abbrev NativeK5APClasses (W : NativeK5StructuralThirteenCell p U V) :=
  NativeFifteenFamilyClasses
    (nativeK5FifteenHistoryObserver W)
    (nativeK5FifteenChargeObserver W)
    (nativeK5APLeft W) (nativeK5APRight W)
    (nativeK5APChargeEq W)

def nativeK5APClass
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W) : NativeK5APClasses W :=
  Quotient.mk _ R

/-- An equivalence BETWEEN PRESENTATIONS, induced by recursions on
true Type-valued 15D syntax; both preserve every raw witness. -/
def nativeK5APPresentationEquiv
    (W : NativeK5StructuralThirteenCell p U V) :
    NativeK5APClasses W ≃ NativeK5FifteenFourteenClasses W :=
  nativeFifteenSingleton_quotientEquiv
    (nativeK5FifteenHistoryObserver W)
    (nativeK5FifteenChargeObserver W)
    (nativeK5FifteenCriticalLeft W)
    (nativeK5FifteenCriticalRight W)
    (nativeK5FourteenPasting_integerBlind
      (NativeK5StructuralFourteenCell.squareExchange W))

/-- Presentation transport fixes EVERY original source-typed
fourteen-cell representative, not only the critical pair. -/
theorem nativeK5APPresentationEquiv_mk
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W) :
    nativeK5APPresentationEquiv W (nativeK5APClass W R) =
      nativeK5FifteenClass W R := rfl

/-- The exact criterion for a general observation to descend from the
original C60 proof fiber: compatible conservative pairs AND the actual
independent exchange are separately necessary and sufficient. -/
theorem nativeK5AP_factors_iff
    (W : NativeK5StructuralThirteenCell p U V)
    {B : Type uB} (obs : NativeK5FifteenFourteenFiber W → B) :
    (∃ F : NativeK5APClasses W → B,
      ∀ R : NativeK5FifteenFourteenFiber W,
        F (nativeK5APClass W R) = obs R) ↔
    (∀ R S : NativeK5FifteenFourteenFiber W,
      R.historyWord = S.historyWord →
        R.squareCount = S.squareCount → obs R = obs S) ∧
    (obs (nativeK5FifteenCriticalLeft W) =
      obs (nativeK5FifteenCriticalRight W)) := by
  have universal := nativeFifteenFamily_factors_iff
    (nativeK5FifteenHistoryObserver W)
    (nativeK5FifteenChargeObserver W)
    (nativeK5APLeft W) (nativeK5APRight W)
    (nativeK5APChargeEq W) obs
  constructor
  · intro h
    obtain ⟨hcore, hexchange⟩ := universal.mp h
    exact ⟨hcore, hexchange ()⟩
  · rintro ⟨hcore, hexchange⟩
    apply universal.mpr
    exact ⟨hcore, fun _ => hexchange⟩

/-- The original integer square count descends through the indexed
presentation on ALL raw fourteen-cell witnesses. -/
def nativeK5APCharge
    (W : NativeK5StructuralThirteenCell p U V) :
    NativeK5APClasses W → ℤ :=
  nativeFifteenFamilyCharge
    (nativeK5FifteenHistoryObserver W)
    (nativeK5FifteenChargeObserver W)
    (nativeK5APLeft W) (nativeK5APRight W)
    (nativeK5APChargeEq W)

theorem nativeK5APCharge_mk
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W) :
    nativeK5APCharge W (nativeK5APClass W R) = R.squareCount := rfl

/-- The old free-group word cannot be transported to this quotient
because of an actual original source-dependent critical pair. -/
theorem nativeK5AP_historyNoDescent
    (W : NativeK5StructuralThirteenCell p U V) :
    ¬ ∃ F : NativeK5APClasses W → NativeK5FourteenHistoryWord,
      ∀ R : NativeK5FifteenFourteenFiber W,
        F (nativeK5APClass W R) = R.historyWord :=
  nativeFifteenFamily_history_noDescent
    (nativeK5FifteenHistoryObserver W)
    (nativeK5FifteenChargeObserver W)
    (nativeK5APLeft W) (nativeK5APRight W)
    (nativeK5APChargeEq W)
    ()
    (nativeK5FourteenSquareExchange_pastingWord_ne W)

/-- No finite observer-conservative fourteen-cell closure can replace
the independent named fifteen-cell at this exact physical boundary. -/
theorem nativeK5AP_noFiniteCoreFiller
    (W : NativeK5StructuralThirteenCell p U V)
    (depth : Nat) :
    ¬ Nonempty (NativeConservativeTower
      (NativeK5FifteenCorePresentation W)
      depth
      (nativeK5FifteenCriticalLeft W)
      (nativeK5FifteenCriticalRight W)) :=
  nativeFifteenFamily_noFiniteCoreFiller
    (nativeK5FifteenHistoryObserver W)
    (nativeK5FifteenChargeObserver W)
    (nativeK5APLeft W) (nativeK5APRight W)
    (nativeK5APChargeEq W) ()
    (nativeK5FourteenSquareExchange_pastingWord_ne W) depth

end OriginalFourteenFiber

section GenuineFiveStage

variable {p : Polygon} {a b : D} {x y : E}
variable {n₁ n₂ n₃ n₄ n₅ m₁ m₂ m₃ m₄ m₅ : Nat}
variable {p₀ p₁ p₂ p₃ p₄ p₅ : KuuNativeBlocks a b}
variable {q₀ q₁ q₂ q₃ q₄ q₅ : KuuNativeBlocks x y}
variable
  (t1 : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁)
  (t2 : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂)
  (t3 : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃)
  (t4 : KuuNativeF45Tree p n₄ m₄ p₃ q₃ p₄ q₄)
  (t5 : KuuNativeF45Tree p n₅ m₅ p₄ q₄ p₅ q₅)

/-- The true original C60 K5 five-stage instance transports the
15D quotient comparison into AO's quotient without creating raw
fourteen-cell equality or any independent 16D coherence. -/
theorem nativeK5PentagonatorAP_quotient_transport :
    nativeK5APPresentationEquiv
      (nativeK5PentagonatorFourteenExchangeThirteen t1 t2 t3 t4 t5)
      (nativeK5APClass
        (nativeK5PentagonatorFourteenExchangeThirteen t1 t2 t3 t4 t5)
        (nativeK5PentagonatorFifteenLeftFirst t1 t2 t3 t4 t5)) =
    nativeK5APPresentationEquiv
      (nativeK5PentagonatorFourteenExchangeThirteen t1 t2 t3 t4 t5)
      (nativeK5APClass
        (nativeK5PentagonatorFourteenExchangeThirteen t1 t2 t3 t4 t5)
        (nativeK5PentagonatorFifteenRightFirst t1 t2 t3 t4 t5)) := by
  change nativeK5FifteenClass
      (nativeK5PentagonatorFourteenExchangeThirteen t1 t2 t3 t4 t5)
      (nativeK5PentagonatorFifteenLeftFirst t1 t2 t3 t4 t5) =
    nativeK5FifteenClass
      (nativeK5PentagonatorFourteenExchangeThirteen t1 t2 t3 t4 t5)
      (nativeK5PentagonatorFifteenRightFirst t1 t2 t3 t4 t5)
  exact nativeK5PentagonatorFifteen_quotient_eq t1 t2 t3 t4 t5

/-- Actual five-stage word obstruction still survives an equivalent
presentation even while scalar charge does descend. -/
theorem nativeK5PentagonatorAP_historyNoDescent :
    ¬ ∃ F : NativeK5APClasses
        (nativeK5PentagonatorFourteenExchangeThirteen t1 t2 t3 t4 t5) →
          NativeK5FourteenHistoryWord,
      ∀ R : NativeK5FifteenFourteenFiber
        (nativeK5PentagonatorFourteenExchangeThirteen t1 t2 t3 t4 t5),
        F (nativeK5APClass
          (nativeK5PentagonatorFourteenExchangeThirteen t1 t2 t3 t4 t5)
          R) = R.historyWord :=
  nativeK5AP_historyNoDescent
    (nativeK5PentagonatorFourteenExchangeThirteen t1 t2 t3 t4 t5)

end GenuineFiveStage

#print axioms nativeK5APLeft
#print axioms nativeK5APRight
#print axioms nativeK5APChargeEq
#print axioms NativeK5APClasses
#print axioms nativeK5APClass
#print axioms nativeK5APPresentationEquiv
#print axioms nativeK5APPresentationEquiv_mk
#print axioms nativeK5AP_factors_iff
#print axioms nativeK5APCharge
#print axioms nativeK5APCharge_mk
#print axioms nativeK5AP_historyNoDescent
#print axioms nativeK5AP_noFiniteCoreFiller
#print axioms nativeK5PentagonatorAP_quotient_transport
#print axioms nativeK5PentagonatorAP_historyNoDescent

end
end Kuu.F112.Physical
