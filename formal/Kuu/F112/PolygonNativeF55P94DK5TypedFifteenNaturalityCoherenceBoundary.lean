import Kuu.F112.PolygonNativeF55P94DK5FiniteContextPeifferNaturality
import Mathlib.Tactic

/-!
# F112-P94D3AU — Type-valued fifteen-cell naturality, composition, and limits

All witnesses remain in the ORIGINAL dependent C60 fourteen-cell fiber
with its exact thirteen-cell source and target. AT supplies the
noncommutative Peiffer action on defects. Here we explicitly keep the
underlying AQ Type-valued 15-cell evidence and separately compare:

* two paths around the left/right 15-cell naturality square;
* two 15-cell paths through a composite finite whiskering context;
* their boundary defects in the AS normal Peiffer module.

In each case the two Type-valued paths are CONSTRUCTED but NOT
identified as proofs. Equality of their group defects is not a genuine
geometric 16-cell. We derive precise necessary-and-sufficient descent
criteria for a possible future source-typed P92B receiver, WITHOUT
asserting any P92B boundary functor or any higher-dimensional descent.

No new axioms, sorry/admit, Gray strictification, or global strict-n.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uD vD uE vE uB uG
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

/-- A genuine Type-valued AQ 15-cell between the two ways to evaluate
a concatenated finite 14D context. It is supplied by the actual
source-dependent AQ raw context composition equation, NOT by a
hypothetical 16D coherence. -/
def nativeK5AUContextAssocCell
    (W : NativeK5StructuralThirteenCell p U V)
    (xs ys : List Bool) (R : NativeK5FifteenFourteenFiber W) :
    NativeK5AQFifteenCell W
      (nativeK5AQContext W (xs ++ ys) R)
      (nativeK5AQContext W xs (nativeK5AQContext W ys R)) := by
  have h := nativeK5AQContext_append W xs ys R
  exact .conservative (.atom
    (congrArg (fun T : NativeK5FifteenFourteenFiber W => T.historyWord) h)
    (congrArg (fun T : NativeK5FifteenFourteenFiber W => T.squareCount) h))

/-- The source-typed AQ class equality follows from the displayed
15-cell witness, rather than assuming raw proof equality. -/
theorem nativeK5AUContextAssoc_class
    (W : NativeK5StructuralThirteenCell p U V)
    (xs ys : List Bool) (R : NativeK5FifteenFourteenFiber W) :
    nativeK5AQClass W (nativeK5AQContext W (xs ++ ys) R) =
      nativeK5AQClass W
        (nativeK5AQContext W xs (nativeK5AQContext W ys R)) :=
  Quotient.sound ⟨nativeK5AUContextAssocCell W xs ys R⟩

/-- Context-association has TRIVIAL Peiffer boundary: it does not
contribute a new nonabelian exchange generator. -/
theorem nativeK5AUContextAssoc_defect_one
    (W : NativeK5StructuralThirteenCell p U V)
    (xs ys : List Bool) (R : NativeK5FifteenFourteenFiber W) :
    nativeK5ATCellDefect W (nativeK5AUContextAssocCell W xs ys R) = 1 := by
  apply Subtype.ext
  change nativeK5ARWordDefect W
      (nativeK5AQContext W (xs ++ ys) R)
      (nativeK5AQContext W xs (nativeK5AQContext W ys R)) = 1
  rw [← nativeK5AQContext_append W xs ys R]
  exact nativeK5ARWordDefect_refl W _

/-- First legitimate Type-valued 15D composite-context route:
transport the witness all at once, then associate at its target. -/
def nativeK5AUCompositionViaTarget
    (W : NativeK5StructuralThirteenCell p U V)
    (xs ys : List Bool)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S) :
    NativeK5AQFifteenCell W
      (nativeK5AQContext W (xs ++ ys) R)
      (nativeK5AQContext W xs (nativeK5AQContext W ys S)) :=
  .trans (nativeK5AQContextCell W (xs ++ ys) cell)
    (nativeK5AUContextAssocCell W xs ys S)

/-- Second legitimate Type-valued 15D route:
associate the source, then transport through the nested contexts.
No equation between the two resulting proof TERMS is asserted. -/
def nativeK5AUCompositionViaSource
    (W : NativeK5StructuralThirteenCell p U V)
    (xs ys : List Bool)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S) :
    NativeK5AQFifteenCell W
      (nativeK5AQContext W (xs ++ ys) R)
      (nativeK5AQContext W xs (nativeK5AQContext W ys S)) :=
  .trans (nativeK5AUContextAssocCell W xs ys R)
    (nativeK5AQContextCell W xs (nativeK5AQContextCell W ys cell))

/-- The genuine two Type-valued 15D composite paths have the same
AS Peiffer-KERNEL shadow. This does NOT identify the two 15D proofs. -/
theorem nativeK5AUComposition_defect_eq
    (W : NativeK5StructuralThirteenCell p U V)
    (xs ys : List Bool)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S) :
    nativeK5ATCellDefect W (nativeK5AUCompositionViaTarget W xs ys cell) =
      nativeK5ATCellDefect W (nativeK5AUCompositionViaSource W xs ys cell) := by
  apply Subtype.ext
  rfl

/-- Exact Peiffer value of the target-associated path.
The context concatenation law works at the noncommutative group
boundary even though the Type-valued paths are not collapsed. -/
theorem nativeK5AUCompositionViaTarget_defect
    (W : NativeK5StructuralThirteenCell p U V)
    (xs ys : List Bool)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S) :
    nativeK5ATCellDefect W (nativeK5AUCompositionViaTarget W xs ys cell) =
      nativeK5ASPeifferAct W (nativeK5ATGaugeWord W xs)
        (nativeK5ASPeifferAct W (nativeK5ATGaugeWord W ys)
          (nativeK5ATCellDefect W cell)) := by
  calc
    nativeK5ATCellDefect W (nativeK5AUCompositionViaTarget W xs ys cell) =
        nativeK5ATCellDefect W (nativeK5AQContextCell W (xs ++ ys) cell) := by
          apply Subtype.ext
          change nativeK5ARWordDefect W
            (nativeK5AQContext W (xs ++ ys) R)
            (nativeK5AQContext W xs (nativeK5AQContext W ys S)) =
              nativeK5ARWordDefect W
                (nativeK5AQContext W (xs ++ ys) R)
                (nativeK5AQContext W (xs ++ ys) S)
          rw [← nativeK5AQContext_append W xs ys S]
    _ = nativeK5ASPeifferAct W (nativeK5ATGaugeWord W (xs ++ ys))
          (nativeK5ATCellDefect W cell) :=
        nativeK5ATCellDefect_context W (xs ++ ys) cell
    _ = nativeK5ASPeifferAct W (nativeK5ATGaugeWord W xs)
          (nativeK5ASPeifferAct W (nativeK5ATGaugeWord W ys)
            (nativeK5ATCellDefect W cell)) :=
        nativeK5ATPeiffer_context_append W xs ys _

/-- The source-associated Type-valued 15D path has the SAME
noncommutative Peiffer action, without a manufactured 16D filler. -/
theorem nativeK5AUCompositionViaSource_defect
    (W : NativeK5StructuralThirteenCell p U V)
    (xs ys : List Bool)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S) :
    nativeK5ATCellDefect W (nativeK5AUCompositionViaSource W xs ys cell) =
      nativeK5ASPeifferAct W (nativeK5ATGaugeWord W xs)
        (nativeK5ASPeifferAct W (nativeK5ATGaugeWord W ys)
          (nativeK5ATCellDefect W cell)) := by
  calc
    nativeK5ATCellDefect W (nativeK5AUCompositionViaSource W xs ys cell) =
        nativeK5ATCellDefect W (nativeK5AUCompositionViaTarget W xs ys cell) :=
          (nativeK5AUComposition_defect_eq W xs ys cell).symm
    _ = _ := nativeK5AUCompositionViaTarget_defect W xs ys cell

/-- The Type-valued vertical inversion law is reflected faithfully
as inversion of the ordered defect INSIDE the AS Peiffer subgroup. -/
theorem nativeK5AUCellDefect_symm
    (W : NativeK5StructuralThirteenCell p U V)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S) :
    nativeK5ATCellDefect W (.symm cell) =
      (nativeK5ATCellDefect W cell)⁻¹ := by
  apply Subtype.ext
  change S.historyWord⁻¹ * R.historyWord =
    (R.historyWord⁻¹ * S.historyWord)⁻¹
  group

/-- Two composable, REAL Type-valued AQ 15D witnesses map to the
ORDERED product of defects in the normal Peiffer kernel. -/
theorem nativeK5AUCellDefect_trans
    (W : NativeK5StructuralThirteenCell p U V)
    {R S T : NativeK5FifteenFourteenFiber W}
    (cell₁ : NativeK5AQFifteenCell W R S)
    (cell₂ : NativeK5AQFifteenCell W S T) :
    nativeK5ATCellDefect W (.trans cell₁ cell₂) =
      nativeK5ATCellDefect W cell₁ * nativeK5ATCellDefect W cell₂ := by
  apply Subtype.ext
  change R.historyWord⁻¹ * T.historyWord =
    (R.historyWord⁻¹ * S.historyWord) *
      (S.historyWord⁻¹ * T.historyWord)
  group

/-- The actual independently-adjoined AQ exchange has precisely the
AS physical Peiffer relation as its boundary shadow. -/
theorem nativeK5AUCellDefect_exchange
    (W : NativeK5StructuralThirteenCell p U V)
    (steps : List Bool) :
    nativeK5ATCellDefect W (nativeK5AQExchange W steps) =
      nativeK5ASPhysicalDefect W steps := by
  apply Subtype.ext
  rfl

/-- Observer-conservative 15D evidence adds no normal group defect;
the witness and the free-history equality remain DISTINCT inputs. -/
theorem nativeK5AUCellDefect_conservative
    (W : NativeK5StructuralThirteenCell p U V)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S)
    (h : R.historyWord = S.historyWord) :
    nativeK5ATCellDefect W cell = 1 := by
  apply Subtype.ext
  change R.historyWord⁻¹ * S.historyWord = 1
  rw [← h]
  group

/-- Finite context whiskering of a 15D vertical composite agrees
at the NONCOMMUTATIVE boundary with Peiffer transport of the ordered
product. No equality of transported proof constructors is claimed. -/
theorem nativeK5AUCellDefect_trans_context
    (W : NativeK5StructuralThirteenCell p U V)
    (steps : List Bool)
    {R S T : NativeK5FifteenFourteenFiber W}
    (cell₁ : NativeK5AQFifteenCell W R S)
    (cell₂ : NativeK5AQFifteenCell W S T) :
    nativeK5ATCellDefect W
      (nativeK5AQContextCell W steps (.trans cell₁ cell₂)) =
    nativeK5ASPeifferAct W (nativeK5ATGaugeWord W steps)
      (nativeK5ATCellDefect W cell₁ * nativeK5ATCellDefect W cell₂) := by
  calc
    _ = nativeK5ASPeifferAct W (nativeK5ATGaugeWord W steps)
      (nativeK5ATCellDefect W (.trans cell₁ cell₂)) :=
        nativeK5ATCellDefect_context W steps (.trans cell₁ cell₂)
    _ = _ := congrArg (nativeK5ASPeifferAct W (nativeK5ATGaugeWord W steps))
      (nativeK5AUCellDefect_trans W cell₁ cell₂)

/-- A SOURCE-first route through the true Peiffer naturality square:
first its source-corner 15D comparison, then right-whisker the given
typed witness after left-whiskering it. -/
def nativeK5AUNaturalityViaSource
    (W : NativeK5StructuralThirteenCell p U V)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S) :
    NativeK5AQFifteenCell W
      (nativeK5AQWhiskerLeft W (nativeK5AQWhiskerRight W R))
      (nativeK5AQWhiskerRight W (nativeK5AQWhiskerLeft W S)) :=
  .trans (nativeK5AQPeifferCell W R)
    (nativeK5AQWhiskerCell W false (nativeK5AQWhiskerCell W true cell))

/-- A TARGET-first path through the SAME dependent naturality square:
left-whisker the right-whiskered 15D evidence, then use the target
Peiffer comparison. No equality with the source-first proof is assumed. -/
def nativeK5AUNaturalityViaTarget
    (W : NativeK5StructuralThirteenCell p U V)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S) :
    NativeK5AQFifteenCell W
      (nativeK5AQWhiskerLeft W (nativeK5AQWhiskerRight W R))
      (nativeK5AQWhiskerRight W (nativeK5AQWhiskerLeft W S)) :=
  .trans (nativeK5AQWhiskerCell W true (nativeK5AQWhiskerCell W false cell))
    (nativeK5AQPeifferCell W S)

/-- This is the exact boundary of an UNRESOLVED 16D naturality
comparison: both 15D paths exist, but only their Peiffer SHADOWS are
shown equal. This statement does not identify the proofs themselves. -/
theorem nativeK5AUNaturality_defect_eq
    (W : NativeK5StructuralThirteenCell p U V)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S) :
    nativeK5ATCellDefect W (nativeK5AUNaturalityViaSource W cell) =
      nativeK5ATCellDefect W (nativeK5AUNaturalityViaTarget W cell) := by
  apply Subtype.ext
  rfl

/-- The naturality square's nonabelian defect is exactly conjugated
by the inverse original RIGHT thirteen-cell frame. This is an actual
Peiffer action on the original source-indexed relation kernel. -/
theorem nativeK5AUNaturality_defect_peiffer
    (W : NativeK5StructuralThirteenCell p U V)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S) :
    nativeK5ATCellDefect W (nativeK5AUNaturalityViaSource W cell) =
      nativeK5ASPeifferAct W (nativeK5AQRightFrame W).historyWord⁻¹
        (nativeK5ATCellDefect W cell) := by
  apply Subtype.ext
  change (((nativeK5AQLeftFrame W).historyWord *
      (R.historyWord * (nativeK5AQRightFrame W).historyWord))⁻¹ *
    (((nativeK5AQLeftFrame W).historyWord * S.historyWord) *
      (nativeK5AQRightFrame W).historyWord)) =
    (nativeK5AQRightFrame W).historyWord⁻¹ *
      (R.historyWord⁻¹ * S.historyWord) *
        ((nativeK5AQRightFrame W).historyWord⁻¹)⁻¹
  group

/-- The two Type-valued naturality routes induce the SAME
representative-independent AQ source/target class equation. -/
theorem nativeK5AUNaturality_class
    (W : NativeK5StructuralThirteenCell p U V)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S) :
    nativeK5AQClass W
      (nativeK5AQWhiskerLeft W (nativeK5AQWhiskerRight W R)) =
    nativeK5AQClass W
      (nativeK5AQWhiskerRight W (nativeK5AQWhiskerLeft W S)) :=
  Quotient.sound ⟨nativeK5AUNaturalityViaSource W cell⟩

/-- An arbitrary target B can support a prospective source-typed
old-P92B boundary receiver only if its original raw observation
respects the actual fourteen-cell whiskerings. This closure lemma
does not postulate a geometric old-P92B functor. -/
theorem nativeK5AUTypeReceiver_allContexts
    (W : NativeK5StructuralThirteenCell p U V)
    {B : Type uB} (obs : NativeK5FifteenFourteenFiber W → B)
    (hwhisker : ∀ (side : Bool) {R S : NativeK5FifteenFourteenFiber W},
      obs R = obs S →
        obs (nativeK5AQWhisker W side R) =
          obs (nativeK5AQWhisker W side S))
    (hbase : obs (nativeK5FifteenCriticalLeft W) =
      obs (nativeK5FifteenCriticalRight W)) :
    ∀ steps : List Bool,
      obs (nativeK5AQLeft W steps) =
        obs (nativeK5AQRight W steps) := by
  intro steps
  induction steps with
  | nil => exact hbase
  | cons side rest ih => exact hwhisker side ih

/-- A precise NECESSARY-AND-SUFFICIENT conditional criterion for any
possible TYPE-VALUED P92B-style receiver: conservation of the raw
history/charge core and compatibility with BOTH source-dependent
whiskerings reduce descent to identifying the genuine BASE exchange.
This is not an actual old P92B-to-AQ typed boundary functor. -/
theorem nativeK5AUTypeReceiver_descent_iff
    (W : NativeK5StructuralThirteenCell p U V)
    {B : Type uB} (obs : NativeK5FifteenFourteenFiber W → B)
    (hcore : ∀ R S : NativeK5FifteenFourteenFiber W,
      R.historyWord = S.historyWord →
      R.squareCount = S.squareCount → obs R = obs S)
    (hwhisker : ∀ (side : Bool) {R S : NativeK5FifteenFourteenFiber W},
      obs R = obs S →
        obs (nativeK5AQWhisker W side R) =
          obs (nativeK5AQWhisker W side S)) :
    (∃ F : NativeK5AQClasses W → B,
      ∀ R : NativeK5FifteenFourteenFiber W,
        F (nativeK5AQClass W R) = obs R) ↔
    obs (nativeK5FifteenCriticalLeft W) =
      obs (nativeK5FifteenCriticalRight W) := by
  constructor
  · rintro ⟨F, hF⟩
    calc
      obs (nativeK5FifteenCriticalLeft W) =
          F (nativeK5AQClass W (nativeK5FifteenCriticalLeft W)) :=
            (hF _).symm
      _ = F (nativeK5AQClass W (nativeK5FifteenCriticalRight W)) :=
        congrArg F (nativeK5AQ_exchange_eq W [])
      _ = obs (nativeK5FifteenCriticalRight W) := hF _
  · intro hbase
    exact (nativeK5AQ_factors_iff W obs).mpr
      ⟨hcore, nativeK5AUTypeReceiver_allContexts W obs hwhisker hbase⟩

/-- A GROUP-valued original free-history receiver preserves EVERY
actual Type-valued 15D AQ witness if and only if it identifies the
genuine original C60 base critical pair. This strengthens AT's
all-named-context criterion to the entire AQ 15D proof grammar. -/
theorem nativeK5AUGroupReceiver_allCells_iff
    (W : NativeK5StructuralThirteenCell p U V)
    {G : Type uG} [Group G]
    (f : NativeK5FourteenHistoryWord →* G) :
    (∀ {R S : NativeK5FifteenFourteenFiber W},
      NativeK5AQFifteenCell W R S →
        f R.historyWord = f S.historyWord) ↔
      f (nativeK5FifteenCriticalLeft W).historyWord =
        f (nativeK5FifteenCriticalRight W).historyWord := by
  constructor
  · intro h
    exact h (nativeK5AQExchange W [])
  · intro hbase
    obtain ⟨F, hF⟩ := (nativeK5ASGroupHistoryDescent_iff W f).mpr hbase
    intro R S cell
    have hclass : nativeK5AQClass W R = nativeK5AQClass W S :=
      Quotient.sound ⟨cell⟩
    calc
      f R.historyWord = F (nativeK5AQClass W R) := (hF R).symm
      _ = F (nativeK5AQClass W S) := congrArg F hclass
      _ = f S.historyWord := hF S

end OriginalFourteenFiber

#print axioms nativeK5AUContextAssocCell
#print axioms nativeK5AUContextAssoc_class
#print axioms nativeK5AUContextAssoc_defect_one
#print axioms nativeK5AUCompositionViaTarget
#print axioms nativeK5AUCompositionViaSource
#print axioms nativeK5AUComposition_defect_eq
#print axioms nativeK5AUCompositionViaTarget_defect
#print axioms nativeK5AUCompositionViaSource_defect
#print axioms nativeK5AUCellDefect_symm
#print axioms nativeK5AUCellDefect_trans
#print axioms nativeK5AUCellDefect_exchange
#print axioms nativeK5AUCellDefect_conservative
#print axioms nativeK5AUCellDefect_trans_context
#print axioms nativeK5AUNaturalityViaSource
#print axioms nativeK5AUNaturalityViaTarget
#print axioms nativeK5AUNaturality_defect_eq
#print axioms nativeK5AUNaturality_defect_peiffer
#print axioms nativeK5AUNaturality_class
#print axioms nativeK5AUTypeReceiver_allContexts
#print axioms nativeK5AUTypeReceiver_descent_iff
#print axioms nativeK5AUGroupReceiver_allCells_iff

end
end Kuu.F112.Physical
