import Kuu.F112.PolygonNativeF55P94DK5IndexedFifteenPresentationTransport

/-!
# F112-P94D3AQ — source-typed contextual fifteen-cell congruence

The raw carrier remains the ORIGINAL dependent C60 fourteen-cell proof
fiber. Its two critical proofs L,R have exactly the same thirteen-cell
boundaries and signed charge, but different nonabelian histories.

Two ACTUAL typed fourteen-dimensional loops are formed from L and R:
  left frame = L ; R⁻¹,   right frame = L⁻¹ ; R.
They whisker every raw proof on its respective thirteen-cell boundary.
Finite words of these two operations give a genuinely non-singleton
INDEX FAMILY of source-typed independent fifteen-cell generators.

The independently ADJOINED 15D constructors remain separate from the
physical raw 14D contexts. We prove that the resulting minimal setoid
is closed under BOTH whiskerings, that it is minimal among all such
observer-conservative congruences, and that the induced quotient actions
have a Peiffer-like comparison from the OBSERVER-CONSERVATIVE grammar.
This does NOT construct a geometric 16-cell or claim strict interchange,
arbitrary high-dimensional coherence, or complete P92B descent.

No new axioms, sorry, assumed raw equality, or Gray strictification.
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

/-- Loop at the actual LEFT thirteen-cell endpoint of the 14D fiber. -/
abbrev NativeK5AQLeftLoopFiber
    (W : NativeK5StructuralThirteenCell p U V) :=
  NativeK5StructuralFourteenCell p
    (.trans (nativeK5ThirteenPastingLeftThenRight W)
      (.symm (nativeK5ThirteenPastingLeftThenRight W)))
    (.trans (nativeK5ThirteenPastingLeftThenRight W)
      (.symm (nativeK5ThirteenPastingLeftThenRight W)))

/-- Loop at the actual RIGHT thirteen-cell endpoint of the 14D fiber. -/
abbrev NativeK5AQRightLoopFiber
    (W : NativeK5StructuralThirteenCell p U V) :=
  NativeK5StructuralFourteenCell p
    (.trans (nativeK5ThirteenPastingRightThenLeft W)
      (.symm (nativeK5ThirteenPastingRightThenLeft W)))
    (.trans (nativeK5ThirteenPastingRightThenLeft W)
      (.symm (nativeK5ThirteenPastingRightThenLeft W)))

/-- Genuine typed left loop L ; R⁻¹, not a graph-level loop. -/
def nativeK5AQLeftFrame
    (W : NativeK5StructuralThirteenCell p U V) :
    NativeK5AQLeftLoopFiber W :=
  .trans (nativeK5FifteenCriticalLeft W)
    (.symm (nativeK5FifteenCriticalRight W))

/-- Genuine typed right loop L⁻¹ ; R. -/
def nativeK5AQRightFrame
    (W : NativeK5StructuralThirteenCell p U V) :
    NativeK5AQRightLoopFiber W :=
  .trans (.symm (nativeK5FifteenCriticalLeft W))
    (nativeK5FifteenCriticalRight W)

/-- Whiskering by a true left-end 14D loop preserves both EXACT
thirteen-cell endpoints of the original dependent fiber. -/
def nativeK5AQWhiskerLeft
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W) :
    NativeK5FifteenFourteenFiber W :=
  .trans (nativeK5AQLeftFrame W) R

/-- Whiskering by a true right-end 14D loop. -/
def nativeK5AQWhiskerRight
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W) :
    NativeK5FifteenFourteenFiber W :=
  .trans R (nativeK5AQRightFrame W)

/-- Both genuine boundary whiskerings in a single finite context alphabet. -/
def nativeK5AQWhisker
    (W : NativeK5StructuralThirteenCell p U V)
    (side : Bool) (R : NativeK5FifteenFourteenFiber W) :
    NativeK5FifteenFourteenFiber W :=
  if side then nativeK5AQWhiskerLeft W R
  else nativeK5AQWhiskerRight W R

/-- Left/right raw whiskerings respect EXACT nonabelian history equality.
They do NOT assert that history itself descends to the fifteen quotient. -/
theorem nativeK5AQWhisker_history_congr
    (W : NativeK5StructuralThirteenCell p U V) (side : Bool)
    {R S : NativeK5FifteenFourteenFiber W}
    (h : R.historyWord = S.historyWord) :
    (nativeK5AQWhisker W side R).historyWord =
      (nativeK5AQWhisker W side S).historyWord := by
  cases side with
  | false =>
      change R.historyWord * (nativeK5AQRightFrame W).historyWord =
        S.historyWord * (nativeK5AQRightFrame W).historyWord
      exact congrArg
        (fun a : NativeK5FourteenHistoryWord =>
          a * (nativeK5AQRightFrame W).historyWord) h
  | true =>
      change (nativeK5AQLeftFrame W).historyWord * R.historyWord =
        (nativeK5AQLeftFrame W).historyWord * S.historyWord
      exact congrArg
        (fun a : NativeK5FourteenHistoryWord =>
          (nativeK5AQLeftFrame W).historyWord * a) h

/-- Every actual raw context also preserves charge EQUALITY, not just
the signed charge of the chosen original critical pair. -/
theorem nativeK5AQWhisker_charge_congr
    (W : NativeK5StructuralThirteenCell p U V) (side : Bool)
    {R S : NativeK5FifteenFourteenFiber W}
    (h : R.squareCount = S.squareCount) :
    (nativeK5AQWhisker W side R).squareCount =
      (nativeK5AQWhisker W side S).squareCount := by
  cases side with
  | false =>
      change R.squareCount + (nativeK5AQRightFrame W).squareCount =
        S.squareCount + (nativeK5AQRightFrame W).squareCount
      exact congrArg
        (fun a : ℤ => a + (nativeK5AQRightFrame W).squareCount) h
  | true =>
      change (nativeK5AQLeftFrame W).squareCount + R.squareCount =
        (nativeK5AQLeftFrame W).squareCount + S.squareCount
      exact congrArg
        (fun a : ℤ => (nativeK5AQLeftFrame W).squareCount + a) h

/-- Since the history observer is group-valued, a separated boundary
stays separated after either actual raw whiskering. -/
theorem nativeK5AQWhisker_history_ne
    (W : NativeK5StructuralThirteenCell p U V) (side : Bool)
    {R S : NativeK5FifteenFourteenFiber W}
    (h : R.historyWord ≠ S.historyWord) :
    (nativeK5AQWhisker W side R).historyWord ≠
      (nativeK5AQWhisker W side S).historyWord := by
  intro heq
  cases side with
  | false =>
      change R.historyWord * (nativeK5AQRightFrame W).historyWord =
        S.historyWord * (nativeK5AQRightFrame W).historyWord at heq
      exact h (mul_right_cancel heq)
  | true =>
      change (nativeK5AQLeftFrame W).historyWord * R.historyWord =
        (nativeK5AQLeftFrame W).historyWord * S.historyWord at heq
      exact h (mul_left_cancel heq)

/-- Actual finite source-typed context words (no erased boundaries).
The head of a word denotes the outermost whiskering. -/
def nativeK5AQContext
    (W : NativeK5StructuralThirteenCell p U V) :
    List Bool → NativeK5FifteenFourteenFiber W →
      NativeK5FifteenFourteenFiber W
  | [], R => R
  | side :: rest, R =>
      nativeK5AQWhisker W side (nativeK5AQContext W rest R)

/-- Source-typed contexts respect exact history equality. -/
theorem nativeK5AQContext_history_congr
    (W : NativeK5StructuralThirteenCell p U V)
    (steps : List Bool) {R S : NativeK5FifteenFourteenFiber W}
    (h : R.historyWord = S.historyWord) :
    (nativeK5AQContext W steps R).historyWord =
      (nativeK5AQContext W steps S).historyWord := by
  induction steps with
  | nil => exact h
  | cons side rest ih =>
      exact nativeK5AQWhisker_history_congr W side ih

/-- Source-typed contexts also respect exact charge equality. -/
theorem nativeK5AQContext_charge_congr
    (W : NativeK5StructuralThirteenCell p U V)
    (steps : List Bool) {R S : NativeK5FifteenFourteenFiber W}
    (h : R.squareCount = S.squareCount) :
    (nativeK5AQContext W steps R).squareCount =
      (nativeK5AQContext W steps S).squareCount := by
  induction steps with
  | nil => exact h
  | cons side rest ih =>
      exact nativeK5AQWhisker_charge_congr W side ih

/-- Genuine nonabelian word separation persists at EVERY indexed
contextual exchange boundary, including arbitrarily long words. -/
theorem nativeK5AQContext_history_ne
    (W : NativeK5StructuralThirteenCell p U V)
    (steps : List Bool) {R S : NativeK5FifteenFourteenFiber W}
    (h : R.historyWord ≠ S.historyWord) :
    (nativeK5AQContext W steps R).historyWord ≠
      (nativeK5AQContext W steps S).historyWord := by
  induction steps with
  | nil => exact h
  | cons side rest ih =>
      exact nativeK5AQWhisker_history_ne W side ih

/-- Evaluation of concatenated context words is true raw composition. -/
theorem nativeK5AQContext_append
    (W : NativeK5StructuralThirteenCell p U V)
    (xs ys : List Bool) (R : NativeK5FifteenFourteenFiber W) :
    nativeK5AQContext W (xs ++ ys) R =
      nativeK5AQContext W xs (nativeK5AQContext W ys R) := by
  induction xs with
  | nil => rfl
  | cons side rest ih =>
      exact congrArg (nativeK5AQWhisker W side) ih

/-- The physical endpoints of EVERY independent indexed 15D exchange
come from ACTUAL source-dependent 14D whiskered proofs. -/
abbrev nativeK5AQLeft
    (W : NativeK5StructuralThirteenCell p U V) :
    List Bool → NativeK5FifteenFourteenFiber W :=
  fun steps => nativeK5AQContext W steps (nativeK5FifteenCriticalLeft W)

abbrev nativeK5AQRight
    (W : NativeK5StructuralThirteenCell p U V) :
    List Bool → NativeK5FifteenFourteenFiber W :=
  fun steps => nativeK5AQContext W steps (nativeK5FifteenCriticalRight W)

/-- Charge compatibility is PROVED from the original physical 14D
square exchange, then transported through each typed context. -/
def nativeK5AQChargeEq
    (W : NativeK5StructuralThirteenCell p U V) :
    ∀ steps : List Bool,
      (nativeK5AQLeft W steps).squareCount =
        (nativeK5AQRight W steps).squareCount := by
  intro steps
  exact nativeK5AQContext_charge_congr W steps (nativeK5APChargeEq W ())

/-- Every family exchange remains history-separated, so none comes
from the named finite observer-conservative grammar alone. -/
theorem nativeK5AQBoundary_history_ne
    (W : NativeK5StructuralThirteenCell p U V)
    (steps : List Bool) :
    (nativeK5AQLeft W steps).historyWord ≠
      (nativeK5AQRight W steps).historyWord :=
  nativeK5AQContext_history_ne W steps
    (nativeK5FourteenSquareExchange_pastingWord_ne W)

/-- ADJOINED independent 15-cell grammar on a non-singleton index:
all finite words in the TWO actual 14D whiskerings. -/
abbrev NativeK5AQFifteenCell
    (W : NativeK5StructuralThirteenCell p U V)
    (R S : NativeK5FifteenFourteenFiber W) :=
  NativeFifteenFamilyCell
    (nativeK5FifteenHistoryObserver W)
    (nativeK5FifteenChargeObserver W)
    (nativeK5AQLeft W) (nativeK5AQRight W)
    (nativeK5AQChargeEq W) R S

abbrev NativeK5AQSetoid
    (W : NativeK5StructuralThirteenCell p U V) :=
  NativeFifteenFamilyCell.setoid
    (nativeK5FifteenHistoryObserver W)
    (nativeK5FifteenChargeObserver W)
    (nativeK5AQLeft W) (nativeK5AQRight W)
    (nativeK5AQChargeEq W)

abbrev NativeK5AQClasses
    (W : NativeK5StructuralThirteenCell p U V) :=
  NativeFifteenFamilyClasses
    (nativeK5FifteenHistoryObserver W)
    (nativeK5FifteenChargeObserver W)
    (nativeK5AQLeft W) (nativeK5AQRight W)
    (nativeK5AQChargeEq W)

def nativeK5AQClass
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W) : NativeK5AQClasses W :=
  Quotient.mk _ R

/-- The named generator is 15D Type evidence, NOT an original 14D
equality and NOT an automatically constructed geometric 16-cell. -/
def nativeK5AQExchange
    (W : NativeK5StructuralThirteenCell p U V)
    (steps : List Bool) :
    NativeK5AQFifteenCell W
      (nativeK5AQLeft W steps) (nativeK5AQRight W steps) :=
  .exchange steps

theorem nativeK5AQ_exchange_eq
    (W : NativeK5StructuralThirteenCell p U V)
    (steps : List Bool) :
    nativeK5AQClass W (nativeK5AQLeft W steps) =
      nativeK5AQClass W (nativeK5AQRight W steps) :=
  Quotient.sound ⟨nativeK5AQExchange W steps⟩

/-- BOTH whiskerings carry each Type-valued 15D witness to another
Type-valued 15D witness. In the generator case, the new index is
side :: steps; it is NOT inferred from scalar charge alone. -/
def nativeK5AQWhiskerCell
    (W : NativeK5StructuralThirteenCell p U V)
    (side : Bool) {R S : NativeK5FifteenFourteenFiber W}
    (h : NativeK5AQFifteenCell W R S) :
    NativeK5AQFifteenCell W
      (nativeK5AQWhisker W side R)
      (nativeK5AQWhisker W side S) := by
  induction h with
  | conservative base =>
      exact .conservative (.atom
        (nativeK5AQWhisker_history_congr W side base.history_sound)
        (nativeK5AQWhisker_charge_congr W side base.charge_sound))
  | exchange steps => exact .exchange (side :: steps)
  | symm _ ih => exact .symm ih
  | trans _ _ ih1 ih2 => exact .trans ih1 ih2

/-- Any FINITE typed context transports arbitrary 15D evidence. -/
def nativeK5AQContextCell
    (W : NativeK5StructuralThirteenCell p U V)
    (steps : List Bool) {R S : NativeK5FifteenFourteenFiber W}
    (h : NativeK5AQFifteenCell W R S) :
    NativeK5AQFifteenCell W
      (nativeK5AQContext W steps R)
      (nativeK5AQContext W steps S) := by
  induction steps with
  | nil => exact h
  | cons side rest ih => exact nativeK5AQWhiskerCell W side ih

/-- Each original geometric whiskering defines an unambiguous
operation on the QUOTIENT: representative independence is PROVED. -/
def nativeK5AQWhiskerClass
    (W : NativeK5StructuralThirteenCell p U V)
    (side : Bool) : NativeK5AQClasses W → NativeK5AQClasses W :=
  Quotient.lift
    (fun R => nativeK5AQClass W (nativeK5AQWhisker W side R))
    (by
      intro R S related
      rcases related with ⟨h⟩
      exact Quotient.sound ⟨nativeK5AQWhiskerCell W side h⟩)

theorem nativeK5AQWhiskerClass_mk
    (W : NativeK5StructuralThirteenCell p U V)
    (side : Bool) (R : NativeK5FifteenFourteenFiber W) :
    nativeK5AQWhiskerClass W side (nativeK5AQClass W R) =
      nativeK5AQClass W (nativeK5AQWhisker W side R) := rfl

/-- All finite contextual operations descend, not just single steps. -/
def nativeK5AQContextClass
    (W : NativeK5StructuralThirteenCell p U V)
    (steps : List Bool) : NativeK5AQClasses W → NativeK5AQClasses W :=
  Quotient.lift
    (fun R => nativeK5AQClass W (nativeK5AQContext W steps R))
    (by
      intro R S related
      rcases related with ⟨h⟩
      exact Quotient.sound ⟨nativeK5AQContextCell W steps h⟩)

theorem nativeK5AQContextClass_mk
    (W : NativeK5StructuralThirteenCell p U V)
    (steps : List Bool) (R : NativeK5FifteenFourteenFiber W) :
    nativeK5AQContextClass W steps (nativeK5AQClass W R) =
      nativeK5AQClass W (nativeK5AQContext W steps R) := rfl

/-- Context-word composition is compatible with quotient presentation
transport; this is a representative-independent ACTION law. -/
theorem nativeK5AQContextClass_append
    (W : NativeK5StructuralThirteenCell p U V)
    (xs ys : List Bool) (q : NativeK5AQClasses W) :
    nativeK5AQContextClass W (xs ++ ys) q =
      nativeK5AQContextClass W xs (nativeK5AQContextClass W ys q) := by
  refine Quotient.inductionOn q ?_
  intro R
  change nativeK5AQClass W (nativeK5AQContext W (xs ++ ys) R) =
    nativeK5AQClass W
      (nativeK5AQContext W xs (nativeK5AQContext W ys R))
  exact congrArg (nativeK5AQClass W) (nativeK5AQContext_append W xs ys R)

/-- LEAST observer-conservative equivalence containing the original
critical exchange and stable under both ACTUAL raw whiskerings.
The proof uses real family generators, not a merely postulated setoid. -/
theorem nativeK5AQ_minimal_closed
    (W : NativeK5StructuralThirteenCell p U V)
    (s : Setoid (NativeK5FifteenFourteenFiber W))
    (hcore : ∀ R S : NativeK5FifteenFourteenFiber W,
      R.historyWord = S.historyWord →
      R.squareCount = S.squareCount → s.r R S)
    (hbase : s.r (nativeK5FifteenCriticalLeft W)
      (nativeK5FifteenCriticalRight W))
    (hctx : ∀ (side : Bool) {R S : NativeK5FifteenFourteenFiber W},
      s.r R S → s.r
        (nativeK5AQWhisker W side R)
        (nativeK5AQWhisker W side S))
    {R S : NativeK5FifteenFourteenFiber W}
    (h : (NativeK5AQSetoid W).r R S) : s.r R S := by
  exact nativeFifteenFamily_setoid_minimal
    (nativeK5FifteenHistoryObserver W)
    (nativeK5FifteenChargeObserver W)
    (nativeK5AQLeft W) (nativeK5AQRight W) (nativeK5AQChargeEq W)
    s hcore
    (by
      intro steps
      induction steps with
      | nil => exact hbase
      | cons side rest ih => exact hctx side ih)
    h

/-- Two-sided Peiffer/associativity comparison at the ORIGINAL typed
fourteen-cell boundary. Its 15D filler belongs only to the specified
OBSERVER-CONSERVATIVE grammar. No geometric 16D generator is asserted. -/
def nativeK5AQPeifferCell
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W) :
    NativeK5AQFifteenCell W
      (nativeK5AQWhiskerLeft W (nativeK5AQWhiskerRight W R))
      (nativeK5AQWhiskerRight W (nativeK5AQWhiskerLeft W R)) :=
  .conservative (.atom
    (by
      change (nativeK5AQLeftFrame W).historyWord *
          (R.historyWord * (nativeK5AQRightFrame W).historyWord) =
        ((nativeK5AQLeftFrame W).historyWord * R.historyWord) *
          (nativeK5AQRightFrame W).historyWord
      exact (mul_assoc _ _ _).symm)
    (by
      change (nativeK5AQLeftFrame W).squareCount +
          (R.squareCount + (nativeK5AQRightFrame W).squareCount) =
        ((nativeK5AQLeftFrame W).squareCount + R.squareCount) +
          (nativeK5AQRightFrame W).squareCount
      exact (add_assoc _ _ _).symm))

/-- The two quotient actions commute BY THE PROVED 15D conservative
comparison, not by identifying raw 14D pasting syntax definitionally. -/
theorem nativeK5AQPeiffer_quotient
    (W : NativeK5StructuralThirteenCell p U V)
    (q : NativeK5AQClasses W) :
    nativeK5AQWhiskerClass W true
      (nativeK5AQWhiskerClass W false q) =
    nativeK5AQWhiskerClass W false
      (nativeK5AQWhiskerClass W true q) := by
  refine Quotient.inductionOn q ?_
  intro R
  change nativeK5AQClass W
      (nativeK5AQWhiskerLeft W (nativeK5AQWhiskerRight W R)) =
    nativeK5AQClass W
      (nativeK5AQWhiskerRight W (nativeK5AQWhiskerLeft W R))
  exact Quotient.sound ⟨nativeK5AQPeifferCell W R⟩

/-- Original AP singleton presentation maps CANONICALLY to the
context-saturated AQ presentation; no inverse/equivalence is assumed. -/
def nativeK5APtoAQ
    (W : NativeK5StructuralThirteenCell p U V) :
    NativeK5APClasses W → NativeK5AQClasses W :=
  nativeFifteenFamily_toCoarser
    (nativeK5FifteenHistoryObserver W)
    (nativeK5FifteenChargeObserver W)
    (nativeK5APLeft W) (nativeK5APRight W) (nativeK5APChargeEq W)
    (NativeK5AQSetoid W)
    (by
      intro R S hword hcharge
      exact ⟨NativeFifteenFamilyCell.conservative
        (NativeObserverCoreFifteenCell.atom hword hcharge)⟩)
    (by
      intro i
      cases i
      exact ⟨nativeK5AQExchange W []⟩)

theorem nativeK5APtoAQ_mk
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W) :
    nativeK5APtoAQ W (nativeK5APClass W R) =
      nativeK5AQClass W R := rfl

/-- Any AQ class retains an original AP raw representative, even though
its equivalence relation may identify MORE context-related witnesses. -/
theorem nativeK5APtoAQ_surjective
    (W : NativeK5StructuralThirteenCell p U V) :
    Function.Surjective (nativeK5APtoAQ W) := by
  intro q
  refine Quotient.inductionOn q ?_
  intro R
  exact ⟨nativeK5APClass W R, rfl⟩

/-- Exact criterion for ALL observers on the true source-dependent
14D fiber, including every independent context-indexed generator. -/
theorem nativeK5AQ_factors_iff
    (W : NativeK5StructuralThirteenCell p U V)
    {B : Type uB} (obs : NativeK5FifteenFourteenFiber W → B) :
    (∃ F : NativeK5AQClasses W → B,
      ∀ R : NativeK5FifteenFourteenFiber W,
        F (nativeK5AQClass W R) = obs R) ↔
    (∀ R S : NativeK5FifteenFourteenFiber W,
      R.historyWord = S.historyWord →
      R.squareCount = S.squareCount → obs R = obs S) ∧
    (∀ steps : List Bool,
      obs (nativeK5AQLeft W steps) =
        obs (nativeK5AQRight W steps)) :=
  nativeFifteenFamily_factors_iff
    (nativeK5FifteenHistoryObserver W)
    (nativeK5FifteenChargeObserver W)
    (nativeK5AQLeft W) (nativeK5AQRight W) (nativeK5AQChargeEq W) obs

/-- Every indexed physical exchange remains impossible to fill by any
FINITE conservative observer grammar. This no-go is relative to that
precisely named grammar, NOT an unrestricted geometric obstruction. -/
theorem nativeK5AQ_noFiniteCoreFiller
    (W : NativeK5StructuralThirteenCell p U V)
    (steps : List Bool) (depth : Nat) :
    ¬ Nonempty (NativeConservativeTower
      (NativeK5FifteenCorePresentation W)
      depth (nativeK5AQLeft W steps) (nativeK5AQRight W steps)) :=
  nativeFifteenFamily_noFiniteCoreFiller
    (nativeK5FifteenHistoryObserver W)
    (nativeK5FifteenChargeObserver W)
    (nativeK5AQLeft W) (nativeK5AQRight W)
    (nativeK5AQChargeEq W) steps
    (nativeK5AQBoundary_history_ne W steps) depth

/-- Integer charge descends along every context-indexed exchange
on all original physical fourteen-cell raw witnesses. -/
def nativeK5AQCharge
    (W : NativeK5StructuralThirteenCell p U V) :
    NativeK5AQClasses W → ℤ :=
  nativeFifteenFamilyCharge
    (nativeK5FifteenHistoryObserver W)
    (nativeK5FifteenChargeObserver W)
    (nativeK5AQLeft W) (nativeK5AQRight W) (nativeK5AQChargeEq W)

theorem nativeK5AQCharge_mk
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W) :
    nativeK5AQCharge W (nativeK5AQClass W R) = R.squareCount := rfl

/-- Nonabelian history still does NOT descend along the newly adjoined
physical context exchanges. It remains an observer of raw witnesses. -/
theorem nativeK5AQ_historyNoDescent
    (W : NativeK5StructuralThirteenCell p U V) :
    ¬ ∃ F : NativeK5AQClasses W → NativeK5FourteenHistoryWord,
      ∀ R : NativeK5FifteenFourteenFiber W,
        F (nativeK5AQClass W R) = R.historyWord :=
  nativeFifteenFamily_history_noDescent
    (nativeK5FifteenHistoryObserver W)
    (nativeK5FifteenChargeObserver W)
    (nativeK5AQLeft W) (nativeK5AQRight W)
    (nativeK5AQChargeEq W) []
    (nativeK5AQBoundary_history_ne W [])

end OriginalFourteenFiber

#print axioms NativeK5AQLeftLoopFiber
#print axioms NativeK5AQRightLoopFiber
#print axioms nativeK5AQLeftFrame
#print axioms nativeK5AQRightFrame
#print axioms nativeK5AQWhiskerLeft
#print axioms nativeK5AQWhiskerRight
#print axioms nativeK5AQWhisker
#print axioms nativeK5AQWhisker_history_congr
#print axioms nativeK5AQWhisker_charge_congr
#print axioms nativeK5AQWhisker_history_ne
#print axioms nativeK5AQContext
#print axioms nativeK5AQContext_history_congr
#print axioms nativeK5AQContext_charge_congr
#print axioms nativeK5AQContext_history_ne
#print axioms nativeK5AQContext_append
#print axioms nativeK5AQLeft
#print axioms nativeK5AQRight
#print axioms nativeK5AQChargeEq
#print axioms nativeK5AQBoundary_history_ne
#print axioms NativeK5AQFifteenCell
#print axioms NativeK5AQSetoid
#print axioms NativeK5AQClasses
#print axioms nativeK5AQClass
#print axioms nativeK5AQExchange
#print axioms nativeK5AQ_exchange_eq
#print axioms nativeK5AQWhiskerCell
#print axioms nativeK5AQContextCell
#print axioms nativeK5AQWhiskerClass
#print axioms nativeK5AQWhiskerClass_mk
#print axioms nativeK5AQContextClass
#print axioms nativeK5AQContextClass_mk
#print axioms nativeK5AQContextClass_append
#print axioms nativeK5AQ_minimal_closed
#print axioms nativeK5AQPeifferCell
#print axioms nativeK5AQPeiffer_quotient
#print axioms nativeK5APtoAQ
#print axioms nativeK5APtoAQ_mk
#print axioms nativeK5APtoAQ_surjective
#print axioms nativeK5AQ_factors_iff
#print axioms nativeK5AQ_noFiniteCoreFiller
#print axioms nativeK5AQCharge
#print axioms nativeK5AQCharge_mk
#print axioms nativeK5AQ_historyNoDescent

end
end Kuu.F112.Physical
