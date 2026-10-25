import Kuu.F112.PolygonNativeF55P94DK5PeifferNormalKernelExactDescent
import Mathlib.Tactic

/-!
# F112-P94D3AT — Peiffer naturality in arbitrary typed finite contexts

We retain the ORIGINAL dependent C60 fourteen-cell source/target fiber.
Every Boolean context is an ACTUAL finite word in its two typed fourteen-cell
whiskerings. We separately accumulate LEFT and RIGHT noncommutative history
frames, prove their different composition orders, and then transport the
ordered fourteen-cell defect by right-frame conjugation.

A proof of an AQ Type-valued fifteen-cell supplies a genuine element of the
AS Peiffer relation kernel. Its arbitrary finite context transport agrees
with the algebraic AS Peiffer action, on the nose in that kernel. This does
NOT identify different fifteen-cell proofs or construct a geometric 16-cell.

The group-valued receiver criterion is context-uniform, but a full
source-typed old-P92B boundary functor remains UNCONSTRUCTED. There are no
new axioms, sorry/admit, Gray structures, or global strict-n assertions.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uD vD uE vE uG
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

/-- Left frames in the ORIGINAL noncommutative raw history group.
The list head applies OUTERMOST, as in AQ. -/
def nativeK5ATLeftContextWord
    (W : NativeK5StructuralThirteenCell p U V) :
    List Bool → NativeK5FourteenHistoryWord
  | [] => 1
  | side :: rest =>
      if side then
        (nativeK5AQLeftFrame W).historyWord *
          nativeK5ATLeftContextWord W rest
      else nativeK5ATLeftContextWord W rest

/-- Right frames accumulate in the REVERSED composition order; this
order is essential even though each elementary frame is fixed. -/
def nativeK5ATRightContextWord
    (W : NativeK5StructuralThirteenCell p U V) :
    List Bool → NativeK5FourteenHistoryWord
  | [] => 1
  | side :: rest =>
      if side then nativeK5ATRightContextWord W rest
      else nativeK5ATRightContextWord W rest *
        (nativeK5AQRightFrame W).historyWord

/-- Every ACTUAL source-dependent typed fourteen-cell context has
two-sided noncommutative history, without erasing its endpoints. -/
theorem nativeK5ATContext_history
    (W : NativeK5StructuralThirteenCell p U V)
    (steps : List Bool) (R : NativeK5FifteenFourteenFiber W) :
    (nativeK5AQContext W steps R).historyWord =
      nativeK5ATLeftContextWord W steps * R.historyWord *
        nativeK5ATRightContextWord W steps := by
  induction steps with
  | nil =>
      change R.historyWord =
        (1 : NativeK5FourteenHistoryWord) * R.historyWord * 1
      group
  | cons side rest ih =>
      cases side with
      | false =>
          change (nativeK5AQContext W rest R).historyWord *
              (nativeK5AQRightFrame W).historyWord =
            nativeK5ATLeftContextWord W rest * R.historyWord *
              (nativeK5ATRightContextWord W rest *
                (nativeK5AQRightFrame W).historyWord)
          rw [ih]
          group
      | true =>
          change (nativeK5AQLeftFrame W).historyWord *
              (nativeK5AQContext W rest R).historyWord =
            ((nativeK5AQLeftFrame W).historyWord *
              nativeK5ATLeftContextWord W rest) * R.historyWord *
                nativeK5ATRightContextWord W rest
          rw [ih]
          group

/-- The left frame is a monoid homomorphism in context concatenation. -/
theorem nativeK5ATLeftContextWord_append
    (W : NativeK5StructuralThirteenCell p U V)
    (xs ys : List Bool) :
    nativeK5ATLeftContextWord W (xs ++ ys) =
      nativeK5ATLeftContextWord W xs *
        nativeK5ATLeftContextWord W ys := by
  induction xs with
  | nil =>
      change nativeK5ATLeftContextWord W ys =
        (1 : NativeK5FourteenHistoryWord) * nativeK5ATLeftContextWord W ys
      group
  | cons side rest ih =>
      cases side with
      | false =>
          change nativeK5ATLeftContextWord W (rest ++ ys) =
            nativeK5ATLeftContextWord W rest *
              nativeK5ATLeftContextWord W ys
          exact ih
      | true =>
          change (nativeK5AQLeftFrame W).historyWord *
              nativeK5ATLeftContextWord W (rest ++ ys) =
            ((nativeK5AQLeftFrame W).historyWord *
              nativeK5ATLeftContextWord W rest) *
                nativeK5ATLeftContextWord W ys
          rw [ih]
          group

/-- Right-frame concatenation reverses order in the free history.
No commutativity of the original free group is assumed. -/
theorem nativeK5ATRightContextWord_append
    (W : NativeK5StructuralThirteenCell p U V)
    (xs ys : List Bool) :
    nativeK5ATRightContextWord W (xs ++ ys) =
      nativeK5ATRightContextWord W ys *
        nativeK5ATRightContextWord W xs := by
  induction xs with
  | nil =>
      change nativeK5ATRightContextWord W ys =
        nativeK5ATRightContextWord W ys * (1 : NativeK5FourteenHistoryWord)
      group
  | cons side rest ih =>
      cases side with
      | false =>
          change (nativeK5ATRightContextWord W (rest ++ ys) *
              (nativeK5AQRightFrame W).historyWord) =
            nativeK5ATRightContextWord W ys *
              (nativeK5ATRightContextWord W rest *
                (nativeK5AQRightFrame W).historyWord)
          rw [ih]
          group
      | true =>
          change nativeK5ATRightContextWord W (rest ++ ys) =
            nativeK5ATRightContextWord W ys *
              nativeK5ATRightContextWord W rest
          exact ih

/-- The Peiffer gauge acting on ordered defects is the inverse of
the ACTUAL accumulated right-end fourteen-cell history frame. -/
def nativeK5ATGaugeWord
    (W : NativeK5StructuralThirteenCell p U V)
    (steps : List Bool) : NativeK5FourteenHistoryWord :=
  (nativeK5ATRightContextWord W steps)⁻¹

theorem nativeK5ATGaugeWord_left
    (W : NativeK5StructuralThirteenCell p U V)
    (steps : List Bool) :
    nativeK5ATGaugeWord W (true :: steps) =
      nativeK5ATGaugeWord W steps := rfl

theorem nativeK5ATGaugeWord_right
    (W : NativeK5StructuralThirteenCell p U V)
    (steps : List Bool) :
    nativeK5ATGaugeWord W (false :: steps) =
      (nativeK5AQRightFrame W).historyWord⁻¹ *
        nativeK5ATGaugeWord W steps := by
  change (nativeK5ATRightContextWord W steps *
      (nativeK5AQRightFrame W).historyWord)⁻¹ =
    (nativeK5AQRightFrame W).historyWord⁻¹ *
      (nativeK5ATRightContextWord W steps)⁻¹
  group

/-- The inverse right-frame gauge composes COVARIANTLY.
This is the noncommutative order required by the AS Peiffer action. -/
theorem nativeK5ATGaugeWord_append
    (W : NativeK5StructuralThirteenCell p U V)
    (xs ys : List Bool) :
    nativeK5ATGaugeWord W (xs ++ ys) =
      nativeK5ATGaugeWord W xs * nativeK5ATGaugeWord W ys := by
  change (nativeK5ATRightContextWord W (xs ++ ys))⁻¹ =
    (nativeK5ATRightContextWord W xs)⁻¹ *
      (nativeK5ATRightContextWord W ys)⁻¹
  rw [nativeK5ATRightContextWord_append]
  group

/-- Arbitrary finite ORIGINAL source-typed whiskering transforms
the ordered free-history defect by noncommutative conjugation. -/
theorem nativeK5ATContext_defect
    (W : NativeK5StructuralThirteenCell p U V)
    (steps : List Bool)
    (R S : NativeK5FifteenFourteenFiber W) :
    nativeK5ARWordDefect W
      (nativeK5AQContext W steps R) (nativeK5AQContext W steps S) =
    nativeK5ATGaugeWord W steps *
      nativeK5ARWordDefect W R S *
        (nativeK5ATGaugeWord W steps)⁻¹ := by
  unfold nativeK5ARWordDefect
  rw [nativeK5ATContext_history W steps R,
      nativeK5ATContext_history W steps S]
  unfold nativeK5ATGaugeWord
  group

/-- Each PROVEN Type-valued AQ fifteen-cell, not just its named
generator, determines an ordered defect INSIDE the AS Peiffer kernel.
Only this normal group SHADOW is asserted. -/
def nativeK5ATCellDefect
    (W : NativeK5StructuralThirteenCell p U V)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S) :
    NativeK5ASPeifferKernel W := by
  refine ⟨nativeK5ARWordDefect W R S, ?_⟩
  have heq := nativeK5ARWordClass_cell_sound W cell
  change R.historyWord⁻¹ * S.historyWord ∈ nativeK5ARHistoryKernel W
  change (R.historyWord : NativeK5ARHistoryQuotient W) =
    (S.historyWord : NativeK5ARHistoryQuotient W) at heq
  exact (QuotientGroup.eq).mp heq

theorem nativeK5ATCellDefect_boundary
    (W : NativeK5StructuralThirteenCell p U V)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S) :
    nativeK5ASPeifferBoundary W (nativeK5ATCellDefect W cell) =
      nativeK5ARWordDefect W R S := rfl

/-- Fundamental AT naturality. Transport actual Type-valued AQ
15D evidence through any finite 14D context, and its Peiffer-kernel
defect transforms by the EXACT conjugation action. This is NOT equality
of the two fifteen-cell witnesses or a geometrical 16-cell filler. -/
theorem nativeK5ATCellDefect_context
    (W : NativeK5StructuralThirteenCell p U V)
    (steps : List Bool)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S) :
    nativeK5ATCellDefect W (nativeK5AQContextCell W steps cell) =
      nativeK5ASPeifferAct W (nativeK5ATGaugeWord W steps)
        (nativeK5ATCellDefect W cell) := by
  apply Subtype.ext
  change nativeK5ARWordDefect W
      (nativeK5AQContext W steps R) (nativeK5AQContext W steps S) =
    nativeK5ATGaugeWord W steps *
      nativeK5ARWordDefect W R S *
        (nativeK5ATGaugeWord W steps)⁻¹
  exact nativeK5ATContext_defect W steps R S

/-- For every SOURCE-indexed 15D exchange, the typed geometric
context defect is Peiffer-conjugate to the original physical relator. -/
theorem nativeK5ATPhysicalDefect_context
    (W : NativeK5StructuralThirteenCell p U V)
    (steps : List Bool) :
    nativeK5ASPhysicalDefect W steps =
      nativeK5ASPeifferAct W (nativeK5ATGaugeWord W steps)
        (nativeK5ASPhysicalDefect W []) := by
  apply Subtype.ext
  change nativeK5ARWordDefect W
      (nativeK5AQContext W steps (nativeK5FifteenCriticalLeft W))
      (nativeK5AQContext W steps (nativeK5FifteenCriticalRight W)) =
    nativeK5ATGaugeWord W steps *
      nativeK5ARWordDefect W
        (nativeK5FifteenCriticalLeft W) (nativeK5FifteenCriticalRight W) *
          (nativeK5ATGaugeWord W steps)⁻¹
  exact nativeK5ATContext_defect W steps _ _

/-- Finite concatenation of contexts acts on the AS Peiffer kernel
by the correct ORDERED group action; no strict higher-cell interchange. -/
theorem nativeK5ATPeiffer_context_append
    (W : NativeK5StructuralThirteenCell p U V)
    (xs ys : List Bool)
    (z : NativeK5ASPeifferKernel W) :
    nativeK5ASPeifferAct W (nativeK5ATGaugeWord W (xs ++ ys)) z =
      nativeK5ASPeifferAct W (nativeK5ATGaugeWord W xs)
        (nativeK5ASPeifferAct W (nativeK5ATGaugeWord W ys) z) := by
  rw [nativeK5ATGaugeWord_append]
  exact nativeK5ASPeifferAct_comp W _ _ _

/-- Two-sided finite-context equivariance of the UNIVERSALLY
DESCENDED AQ gauge history on every quotient class. Both noncommuting
frames and their original source-dependent provenance are retained. -/
theorem nativeK5ATGaugeHistory_context
    (W : NativeK5StructuralThirteenCell p U V)
    (steps : List Bool)
    (q : NativeK5AQClasses W) :
    nativeK5ARGaugeHistory W (nativeK5AQContextClass W steps q) =
      nativeK5ARWordClass W (nativeK5ATLeftContextWord W steps) *
        nativeK5ARGaugeHistory W q *
          nativeK5ARWordClass W (nativeK5ATRightContextWord W steps) := by
  refine Quotient.inductionOn q ?_
  intro R
  change nativeK5ARWordClass W
      (nativeK5AQContext W steps R).historyWord =
    nativeK5ARWordClass W (nativeK5ATLeftContextWord W steps) *
      nativeK5ARWordClass W R.historyWord *
        nativeK5ARWordClass W (nativeK5ATRightContextWord W steps)
  rw [nativeK5ATContext_history W steps R]
  simp only [map_mul]

/-- For ANY group-valued possible old-P92B history receiver,
compatibility with EVERY actually typed context exchange is equivalent
to compatibility with the SINGLE original C60 critical boundary.
No old-P92B typed functor or geometric 16-cell is manufactured. -/
theorem nativeK5ATGroupReceiver_allContexts_iff
    (W : NativeK5StructuralThirteenCell p U V)
    {G : Type uG} [Group G]
    (f : NativeK5FourteenHistoryWord →* G) :
    (∀ steps : List Bool,
      f (nativeK5AQLeft W steps).historyWord =
        f (nativeK5AQRight W steps).historyWord) ↔
      f (nativeK5FifteenCriticalLeft W).historyWord =
        f (nativeK5FifteenCriticalRight W).historyWord := by
  constructor
  · intro h
    exact h []
  · intro hbase steps
    change f (nativeK5AQContext W steps
        (nativeK5FifteenCriticalLeft W)).historyWord =
      f (nativeK5AQContext W steps
        (nativeK5FifteenCriticalRight W)).historyWord
    rw [nativeK5ATContext_history W steps (nativeK5FifteenCriticalLeft W),
        nativeK5ATContext_history W steps (nativeK5FifteenCriticalRight W)]
    simp only [map_mul]
    exact congrArg
      (fun z : G =>
        f (nativeK5ATLeftContextWord W steps) * z *
          f (nativeK5ATRightContextWord W steps)) hbase

/-- A receiver distinguishing ANY actual source-typed contextual
exchange cannot descend to the AQ Type-valued fifteen-cell quotient.
This is a precise conditional obstruction for a future P92B receiver. -/
theorem nativeK5ATGroupReceiver_context_noDescent
    (W : NativeK5StructuralThirteenCell p U V)
    {G : Type uG} [Group G]
    (f : NativeK5FourteenHistoryWord →* G)
    (steps : List Bool)
    (hsep : f (nativeK5AQLeft W steps).historyWord ≠
      f (nativeK5AQRight W steps).historyWord) :
    ¬ ∃ F : NativeK5AQClasses W → G,
      ∀ R : NativeK5FifteenFourteenFiber W,
        F (nativeK5AQClass W R) = f R.historyWord := by
  rintro ⟨F, hF⟩
  apply hsep
  calc
    f (nativeK5AQLeft W steps).historyWord =
        F (nativeK5AQClass W (nativeK5AQLeft W steps)) := (hF _).symm
    _ = F (nativeK5AQClass W (nativeK5AQRight W steps)) :=
      congrArg F (nativeK5AQ_exchange_eq W steps)
    _ = f (nativeK5AQRight W steps).historyWord := hF _

end OriginalFourteenFiber

#print axioms nativeK5ATLeftContextWord
#print axioms nativeK5ATRightContextWord
#print axioms nativeK5ATContext_history
#print axioms nativeK5ATLeftContextWord_append
#print axioms nativeK5ATRightContextWord_append
#print axioms nativeK5ATGaugeWord
#print axioms nativeK5ATGaugeWord_left
#print axioms nativeK5ATGaugeWord_right
#print axioms nativeK5ATGaugeWord_append
#print axioms nativeK5ATContext_defect
#print axioms nativeK5ATCellDefect
#print axioms nativeK5ATCellDefect_boundary
#print axioms nativeK5ATCellDefect_context
#print axioms nativeK5ATPhysicalDefect_context
#print axioms nativeK5ATPeiffer_context_append
#print axioms nativeK5ATGaugeHistory_context
#print axioms nativeK5ATGroupReceiver_allContexts_iff
#print axioms nativeK5ATGroupReceiver_context_noDescent

end
end Kuu.F112.Physical
