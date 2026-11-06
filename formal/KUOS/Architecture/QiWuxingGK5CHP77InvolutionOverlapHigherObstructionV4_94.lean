import KUOS.Architecture.QiWuxingGK5CHP77TriangleOverlapEightCellObstructionV4_93

/-!
Qi v4.94 — DOUBLE INVERSION / INVERSE-CANCELLATION CRITICAL OVERLAPS.

The original eight-cell 22 generators (v4.91) admit a first signed
integer obstruction (v4.93), and the separate TriangleEightCell
presentation conservatively adds two missing unit/associativity
triangles. This module detects TWO FURTHER critical overlaps that
even the triangle-completed presentation cannot fill.

A SECOND, independent integer invariant counts only the original
SevenRewrite.doubleInverse rule, respecting all 13 constructors'
syntax (symmetry sign, chain and composition sum, inverse context).
We prove this integer is preserved by every original EightCell
constructor AND every v4.93 TriangleEightCell constructor, with
explicit structural induction in Lean4.

For arbitrary genuine raw six-cell c, the two type-correct overlaps
between double inversion and inverse cancellation have histories
of charge 0 and 1. Consequently NO old TriangleEightCell can join
either pair. Rather than altering the old grammar, we adjoin a
separate InvolutionEightCell Type, including the full v4.93 grammar
and precisely the two necessary inverse-cancellation peaks. We
construct the explicitly generated local overlap family, show its
every member is joinable by a witnessed higher cell, and prove that
the chosen new history quotient strictly coarsens the old one.

The new comparison does NOT identify original raw six/seven-cell
syntax, does NOT change F55/P77/GK5CG source authorities, does NOT
add a source higher cell, and does NOT claim global completeness.

Append-only / tighten-only / same-root; strict 空 center;
independent Kuu = presentation. Lean v4.30.0-rc2;
mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6;
public roots 107; protected PR #1558 Draft/open/unmerged.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace KUOS.Architecture.WuxingPentagonUnified
open KUOS.Architecture.WuxingCyclicPaths
open Kuu.F112.Physical
open CategoryTheory

set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uD vD uE vE uSix
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {p : Polygon} {a b : D} {x y : E}
variable {n n' m m' : Nat}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}
variable {first : KuuNativeF45Tree p n m ma pa mb pb}
variable {last : KuuNativeF45Tree p n' m' ma pa mb pb}
variable {r₀ r₁ r₂ r₃ r₄ :
  KuuNativeF45Tree.DepthRotationRoute p first last}
variable
  (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₀ r₁)
  (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₁ r₂)
  (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₂ r₃)
  (k : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₃ r₄)

namespace FivefoldP77FiniteRefinement
namespace PentagonAdjoinedSixCell
variable {W : Type uSix} {long short : W}

/-- A second integer invariant on complete original seven-cell syntax:
ONLY the double-inverse rewrite is assigned +1. The history inversion
reverses its sign, and typed composition/congruence is additive. -/
def sevenInvolutionCharge {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s : SevenRewrite W long short c d) : ℤ :=
  match s with
  | .refl _ => 0
  | .symm s => -sevenInvolutionCharge s
  | .trans s t => sevenInvolutionCharge s + sevenInvolutionCharge t
  | .congrInv s => sevenInvolutionCharge s
  | .congrComp s t => sevenInvolutionCharge s + sevenInvolutionCharge t
  | .leftUnit _ => 0
  | .rightUnit _ => 0
  | .assoc _ _ _ => 0
  | .inverseRight _ => 0
  | .inverseLeft _ => 0
  | .doubleInverse _ => 1
  | .inverseId _ => 0
  | .inverseComp _ _ => 0

/-- All 22 ORIGINAL eight-cell generators preserve the independent
double-inversion charge. This proof examines all constructors, not
only the displayed overlap. -/
theorem eightCell_preservesInvolutionCharge {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q : EightCell W long short s t) :
    sevenInvolutionCharge s = sevenInvolutionCharge t := by
  induction q with
  | reflexive s => rfl
  | reverse q ih => exact ih.symm
  | chain q q' ih ih' => exact ih.trans ih'
  | whiskerLeft before q ih =>
      simpa [sevenInvolutionCharge] using
        congrArg (fun n : ℤ => sevenInvolutionCharge before + n) ih
  | whiskerRight q after ih =>
      simpa [sevenInvolutionCharge] using
        congrArg (fun n : ℤ => n + sevenInvolutionCharge after) ih
  | reverseContext q ih =>
      simpa [sevenInvolutionCharge] using
        congrArg (fun n : ℤ => -n) ih
  | inverseContext q ih =>
      simpa [sevenInvolutionCharge] using ih
  | compositeContext q q' ih ih' =>
      simpa [sevenInvolutionCharge] using
        congrArg₂ (fun n m : ℤ => n + m) ih ih'
  | unitLeft s => simp [sevenInvolutionCharge]
  | unitRight s => simp [sevenInvolutionCharge]
  | associate s t u => simp [sevenInvolutionCharge, add_assoc]
  | cancelRight s => simp [sevenInvolutionCharge]
  | cancelLeft s => simp [sevenInvolutionCharge]
  | involute s => simp [sevenInvolutionCharge]
  | inverseIdentity c => simp [sevenInvolutionCharge]
  | inverseComposite s t =>
      simp [sevenInvolutionCharge] <;> abel
  | inverseCongruenceIdentity c => simp [sevenInvolutionCharge]
  | inverseCongruenceChain s t => simp [sevenInvolutionCharge]
  | compositeCongruenceIdentity c d => simp [sevenInvolutionCharge]
  | compositeCongruenceChain s s' t t' =>
      simp [sevenInvolutionCharge] <;> abel
  | interchange s t =>
      simp [sevenInvolutionCharge] <;> abel
  | zigzagDiamond c => simp [sevenInvolutionCharge]

/-- The NEW triangle-only completion from Qi v4.93 ALSO preserves the
double-inverse charge. Both of its new triangle generators have
charge zero on each side, so the invariant genuinely survives the
earlier completion. -/
theorem triangleEightCell_preservesInvolutionCharge {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q : TriangleEightCell W long short s t) :
    sevenInvolutionCharge s = sevenInvolutionCharge t := by
  induction q with
  | original q =>
      exact eightCell_preservesInvolutionCharge q
  | leftTriangle c d =>
      simp [sevenLeftTriangleDirect, sevenLeftTriangleViaAssoc,
        sevenInvolutionCharge]
  | rightTriangle c d =>
      simp [sevenRightTriangleDirect, sevenRightTriangleViaAssoc,
        sevenInvolutionCharge]
  | reverse q ih =>
      exact ih.symm
  | chain q q' ih ih' =>
      exact ih.trans ih'
  | whiskerLeft before q ih =>
      simpa [sevenInvolutionCharge] using
        congrArg (fun n : ℤ => sevenInvolutionCharge before + n) ih
  | whiskerRight q after ih =>
      simpa [sevenInvolutionCharge] using
        congrArg (fun n : ℤ => n + sevenInvolutionCharge after) ih
  | inverseContext q ih =>
      simpa [sevenInvolutionCharge] using ih
  | compositeContext q q' ih ih' =>
      simpa [sevenInvolutionCharge] using
        congrArg₂ (fun n m : ℤ => n + m) ih ih'

/-- First branch: immediately cancel the inverse of the word
symm(c). Source: (symm(symm c)) ; (symm c). -/
def sevenLeftDoubleInverseDirect {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    SevenRewrite W long short
      (.trans (.symm (.symm c)) (.symm c)) (.refl w) :=
  .inverseLeft (.symm c)

/-- Second branch: reduce the double inversion first, then cancel
c ; symm(c). This is a distinct raw SEVEN-cell proof. -/
def sevenLeftDoubleInverseVia {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    SevenRewrite W long short
      (.trans (.symm (.symm c)) (.symm c)) (.refl w) :=
  .trans
    (.congrComp (.doubleInverse c) (.refl (.symm c)))
    (.inverseRight c)

/-- First branch at the right endpoint: inverse-right cancellation
of the word symm c. -/
def sevenRightDoubleInverseDirect {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    SevenRewrite W long short
      (.trans (.symm c) (.symm (.symm c))) (.refl z) :=
  .inverseRight (.symm c)

/-- Second branch at the right endpoint: simplify double inversion
in the right composite term, then cancel symm c ; c. -/
def sevenRightDoubleInverseVia {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    SevenRewrite W long short
      (.trans (.symm c) (.symm (.symm c))) (.refl z) :=
  .trans
    (.congrComp (.refl (.symm c)) (.doubleInverse c))
    (.inverseLeft c)

/-- Each original double-inversion cancellation peak has the
integer obstruction 0 versus +1. -/
theorem sevenLeftDoubleInverse_chargeGap {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    sevenInvolutionCharge (sevenLeftDoubleInverseDirect c) = 0 ∧
    sevenInvolutionCharge (sevenLeftDoubleInverseVia c) = 1 := by
  constructor <;>
    simp [sevenLeftDoubleInverseDirect, sevenLeftDoubleInverseVia,
      sevenInvolutionCharge]

theorem sevenRightDoubleInverse_chargeGap {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    sevenInvolutionCharge (sevenRightDoubleInverseDirect c) = 0 ∧
    sevenInvolutionCharge (sevenRightDoubleInverseVia c) = 1 := by
  constructor <;>
    simp [sevenRightDoubleInverseDirect, sevenRightDoubleInverseVia,
      sevenInvolutionCharge]

/-- Neither double-inversion critical overlap can be filled by the
already-expanded TriangleEightCell. The obstruction is preserved
across all its original and newly adjoined constructors. -/
theorem sevenLeftDoubleInverse_noTriangleEightCell {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    ¬ Nonempty (TriangleEightCell W long short
      (sevenLeftDoubleInverseDirect c)
      (sevenLeftDoubleInverseVia c)) := by
  rintro ⟨q⟩
  have hq := triangleEightCell_preservesInvolutionCharge q
  have hg := sevenLeftDoubleInverse_chargeGap c
  rw [hg.1, hg.2] at hq
  norm_num at hq

theorem sevenRightDoubleInverse_noTriangleEightCell {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    ¬ Nonempty (TriangleEightCell W long short
      (sevenRightDoubleInverseDirect c)
      (sevenRightDoubleInverseVia c)) := by
  rintro ⟨q⟩
  have hq := triangleEightCell_preservesInvolutionCharge q
  have hg := sevenRightDoubleInverse_chargeGap c
  rw [hg.1, hg.2] at hq
  norm_num at hq

/-- The raw seven-cell derivations are strictly unequal. This
is a stronger, separate statement from the obstruction to filling
them in the previous higher presentation. -/
theorem sevenLeftDoubleInverse_notStrict {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    sevenLeftDoubleInverseDirect c ≠ sevenLeftDoubleInverseVia c := by
  intro h
  have hq := congrArg sevenInvolutionCharge h
  have hg := sevenLeftDoubleInverse_chargeGap c
  rw [hg.1, hg.2] at hq
  norm_num at hq

/-- The independently adjoined third-stage higher comparison
presentation: include ALL previous triangle comparisons unchanged,
and add EXACTLY the two displayed double-inversion cancellation
critical overlaps as new primitive generators. -/
inductive InvolutionEightCell (W : Type uSix) (l r : W) :
    {w z : W} →
    {c d : PentagonAdjoinedSixCell W l r w z} →
    SevenRewrite W l r c d →
    SevenRewrite W l r c d → Type uSix where
  | previous {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (q : TriangleEightCell W l r s t) :
      InvolutionEightCell W l r s t
  | leftOverlap {w z : W}
      (c : PentagonAdjoinedSixCell W l r w z) :
      InvolutionEightCell W l r
        (sevenLeftDoubleInverseDirect c) (sevenLeftDoubleInverseVia c)
  | rightOverlap {w z : W}
      (c : PentagonAdjoinedSixCell W l r w z) :
      InvolutionEightCell W l r
        (sevenRightDoubleInverseDirect c) (sevenRightDoubleInverseVia c)
  | reverse {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (q : InvolutionEightCell W l r s t) :
      InvolutionEightCell W l r t s
  | chain {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
      {s t u : SevenRewrite W l r c d}
      (q : InvolutionEightCell W l r s t)
      (q' : InvolutionEightCell W l r t u) :
      InvolutionEightCell W l r s u
  | whiskerLeft {w z : W}
      {c d e : PentagonAdjoinedSixCell W l r w z}
      (before : SevenRewrite W l r c d)
      {s t : SevenRewrite W l r d e}
      (q : InvolutionEightCell W l r s t) :
      InvolutionEightCell W l r (.trans before s) (.trans before t)
  | whiskerRight {w z : W}
      {c d e : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (q : InvolutionEightCell W l r s t)
      (after : SevenRewrite W l r d e) :
      InvolutionEightCell W l r (.trans s after) (.trans t after)
  | inverseContext {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (q : InvolutionEightCell W l r s t) :
      InvolutionEightCell W l r (.congrInv s) (.congrInv t)
  | compositeContext {w x z : W}
      {c c' : PentagonAdjoinedSixCell W l r w x}
      {d d' : PentagonAdjoinedSixCell W l r x z}
      {s s' : SevenRewrite W l r c c'}
      {t t' : SevenRewrite W l r d d'}
      (q : InvolutionEightCell W l r s s')
      (q' : InvolutionEightCell W l r t t') :
      InvolutionEightCell W l r
        (.congrComp s t) (.congrComp s' t')

/-- Every old TriangleEightCell is retained in the new presentation. -/
def involutionEightCell_ofTriangle {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q : TriangleEightCell W long short s t) :
    InvolutionEightCell W long short s t :=
  .previous q

/-- BOTH inverse overlaps are newly fillable, and provably were
not fillable in the previous triangle-only presentation. -/
theorem involutionEightCell_leftNewNotPrevious {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    Nonempty (InvolutionEightCell W long short
      (sevenLeftDoubleInverseDirect c)
      (sevenLeftDoubleInverseVia c)) ∧
    ¬ Nonempty (TriangleEightCell W long short
      (sevenLeftDoubleInverseDirect c)
      (sevenLeftDoubleInverseVia c)) :=
  ⟨⟨.leftOverlap c⟩, sevenLeftDoubleInverse_noTriangleEightCell c⟩

theorem involutionEightCell_rightNewNotPrevious {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    Nonempty (InvolutionEightCell W long short
      (sevenRightDoubleInverseDirect c)
      (sevenRightDoubleInverseVia c)) ∧
    ¬ Nonempty (TriangleEightCell W long short
      (sevenRightDoubleInverseDirect c)
      (sevenRightDoubleInverseVia c)) :=
  ⟨⟨.rightOverlap c⟩, sevenRightDoubleInverse_noTriangleEightCell c⟩

/-- The new grammar is STRICTLY stronger than the triangle extension:
it has no universal interpretation back into its preceding
presentation. The Pi function space is Type-valued, so nonexistence
is expressed as a proposition via Nonempty. -/
theorem involutionEightCell_noPreviousInterpreter (l r : W) :
    ¬ Nonempty (∀ {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      (s t : SevenRewrite W l r c d),
      InvolutionEightCell W l r s t → TriangleEightCell W l r s t) := by
  rintro ⟨interpret⟩
  let c : PentagonAdjoinedSixCell W l r l l := .refl l
  have h : TriangleEightCell W l r
      (sevenLeftDoubleInverseDirect c) (sevenLeftDoubleInverseVia c) :=
    interpret _ _ (.leftOverlap c)
  exact sevenLeftDoubleInverse_noTriangleEightCell c ⟨h⟩

/-- An involution eight-cell is never claimed to force strict
equality of the distinct raw seventh-level derivation syntax. -/
theorem involutionEightCell_noStrictInterpreter (l r : W) :
    ¬ (∀ {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
        (s t : SevenRewrite W l r c d),
        InvolutionEightCell W l r s t → s = t) := by
  intro interpret
  apply triangleEightCell_noStrictInterpreter l r
  intro w z c d s t h
  exact interpret s t (.previous h)

/-- Explicitly GENERATED local critical peak family: inherit the
entire previous TriangleCriticalPeak family, add the two (and only
two) new inverse-cancellation/double-inversion overlaps, and close
under certified typed contexts. No arbitrary parallel-history case. -/
inductive InvolutionCriticalPeak (W : Type uSix) (l r : W) :
    {w z : W} →
    {c d : PentagonAdjoinedSixCell W l r w z} →
    SevenRewrite W l r c d →
    SevenRewrite W l r c d → Type uSix where
  | previous {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (p : TriangleCriticalPeak W l r s t) :
      InvolutionCriticalPeak W l r s t
  | leftOverlap {w z : W}
      (c : PentagonAdjoinedSixCell W l r w z) :
      InvolutionCriticalPeak W l r
        (sevenLeftDoubleInverseDirect c) (sevenLeftDoubleInverseVia c)
  | rightOverlap {w z : W}
      (c : PentagonAdjoinedSixCell W l r w z) :
      InvolutionCriticalPeak W l r
        (sevenRightDoubleInverseDirect c) (sevenRightDoubleInverseVia c)
  | reverse {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (p : InvolutionCriticalPeak W l r s t) :
      InvolutionCriticalPeak W l r t s
  | chain {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
      {s t u : SevenRewrite W l r c d}
      (p : InvolutionCriticalPeak W l r s t)
      (q : InvolutionCriticalPeak W l r t u) :
      InvolutionCriticalPeak W l r s u
  | whiskerLeft {w z : W}
      {c d e : PentagonAdjoinedSixCell W l r w z}
      (before : SevenRewrite W l r c d)
      {s t : SevenRewrite W l r d e}
      (p : InvolutionCriticalPeak W l r s t) :
      InvolutionCriticalPeak W l r (.trans before s) (.trans before t)
  | whiskerRight {w z : W}
      {c d e : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (p : InvolutionCriticalPeak W l r s t)
      (after : SevenRewrite W l r d e) :
      InvolutionCriticalPeak W l r (.trans s after) (.trans t after)
  | inverseContext {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (p : InvolutionCriticalPeak W l r s t) :
      InvolutionCriticalPeak W l r (.congrInv s) (.congrInv t)
  | compositeContext {w x z : W}
      {c c' : PentagonAdjoinedSixCell W l r w x}
      {d d' : PentagonAdjoinedSixCell W l r x z}
      {s s' : SevenRewrite W l r c c'}
      {t t' : SevenRewrite W l r d d'}
      (p : InvolutionCriticalPeak W l r s s')
      (q : InvolutionCriticalPeak W l r t t') :
      InvolutionCriticalPeak W l r
        (.congrComp s t) (.congrComp s' t')

/-- Structural induction builds a NEW higher comparison certificate
for each actually generated critical peak, retaining both full raw
original seven-cell histories as indices. -/
def involutionCriticalPeak_fill {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (p : InvolutionCriticalPeak W long short s t) :
    InvolutionEightCell W long short s t := by
  induction p with
  | previous p =>
      exact .previous (triangleCriticalPeak_fill p)
  | leftOverlap c =>
      exact .leftOverlap c
  | rightOverlap c =>
      exact .rightOverlap c
  | reverse p ih =>
      exact .reverse ih
  | chain p q ihp ihq =>
      exact .chain ihp ihq
  | whiskerLeft before p ih =>
      exact .whiskerLeft before ih
  | whiskerRight p after ih =>
      exact .whiskerRight ih after
  | inverseContext p ih =>
      exact .inverseContext ih
  | compositeContext p q ihp ihq =>
      exact .compositeContext ihp ihq

theorem involutionCriticalPeak_joinable {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (p : InvolutionCriticalPeak W long short s t) :
    Nonempty (InvolutionEightCell W long short s t) :=
  ⟨involutionCriticalPeak_fill p⟩

/-- Higher-history equivalence, defined solely by existence of the
typed new comparison certificate, not by raw proof identity. -/
def involutionHistorySetoid (W : Type uSix) (l r : W)
    {w z : W} {c d : PentagonAdjoinedSixCell W l r w z} :
    Setoid (SevenRewrite W l r c d) where
  r := fun s t => Nonempty (InvolutionEightCell W l r s t)
  iseqv := by
    constructor
    · intro s
      exact ⟨.previous (.original (.reflexive s))⟩
    · intro s t h
      rcases h with ⟨h⟩
      exact ⟨.reverse h⟩
    · intro s t u hs ht
      rcases hs with ⟨hs⟩
      rcases ht with ⟨ht⟩
      exact ⟨.chain hs ht⟩

def involutionHistoryClass {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s : SevenRewrite W long short c d) :
    Quotient (involutionHistorySetoid W long short (c := c) (d := d)) :=
  Quotient.mk _ s

theorem involutionHistoryClass_eq_iff {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s t : SevenRewrite W long short c d) :
    involutionHistoryClass s = involutionHistoryClass t ↔
      Nonempty (InvolutionEightCell W long short s t) := by
  constructor
  · intro h
    exact Quotient.exact h
  · intro h
    exact Quotient.sound h

/-- The previous triangle quotient embeds as a sound source of
new higher equivalences. The converse is refuted below. -/
theorem triangleHistoryClass_descendsToInvolution {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s t : SevenRewrite W long short c d)
    (h : triangleHistoryClass s = triangleHistoryClass t) :
    involutionHistoryClass s = involutionHistoryClass t := by
  rcases (triangleHistoryClass_eq_iff s t).1 h with ⟨q⟩
  exact (involutionHistoryClass_eq_iff s t).2 ⟨.previous q⟩

/-- The new quotient is STRICTLY coarser than the triangle-only
quotient: it identifies one explicit overlap pair that the older
quotient separates by the independently proven integer invariant. -/
theorem involutionHistoryClass_strictlyNew {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    (involutionHistoryClass (sevenLeftDoubleInverseDirect c) =
      involutionHistoryClass (sevenLeftDoubleInverseVia c)) ∧
    triangleHistoryClass (sevenLeftDoubleInverseDirect c) ≠
      triangleHistoryClass (sevenLeftDoubleInverseVia c) := by
  constructor
  · exact (involutionHistoryClass_eq_iff _ _).2 ⟨.leftOverlap c⟩
  · intro h
    exact sevenLeftDoubleInverse_noTriangleEightCell c
      ((triangleHistoryClass_eq_iff _ _).1 h)

/-- Every explicitly generated involution critical peak has equal
chosen new higher-history class, with the full raw proof syntax
retained outside the quotient. -/
theorem involutionCriticalPeak_classEq {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (p : InvolutionCriticalPeak W long short s t) :
    involutionHistoryClass s = involutionHistoryClass t :=
  (involutionHistoryClass_eq_iff _ _).2
    (involutionCriticalPeak_joinable p)

/-- New higher-history equality cannot be interpreted as universal
raw seventh-level syntactic equality. -/
theorem involutionHistoryClass_noStrictReturn (l r : W) :
    ¬ (∀ {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
      (s t : SevenRewrite W l r c d),
      involutionHistoryClass s = involutionHistoryClass t → s = t) := by
  intro interpret
  apply involutionEightCell_noStrictInterpreter l r
  intro w z c d s t q
  exact interpret s t ((involutionHistoryClass_eq_iff s t).2 ⟨q⟩)

end PentagonAdjoinedSixCell

section ActualOriginalP77InvolutionOverlap
variable {u v : FivefoldPathVertex}
variable {family₀ family₁ family₂ family₃ family₄ : Family f g h k u v}
variable {s₀ : State f g h k family₀}
variable {s₁ : State f g h k family₁}
variable {s₂ : State f g h k family₂}
variable {s₃ : State f g h k family₃}
variable {s₄ : State f g h k family₄}
variable (A : DirectNormalBracketTree f g h k family₀ s₀ family₁ s₁)
variable (B : DirectNormalBracketTree f g h k family₁ s₁ family₂ s₂)
variable (C : DirectNormalBracketTree f g h k family₂ s₂ family₃ s₃)
variable (D₄ : DirectNormalBracketTree f g h k family₃ s₃ family₄ s₄)

/-- At every GENUINE original P77 final raw index, the conservative
old five-cell endpoints determine the new original six-cell pentagon
generator. Two distinct seven-cell inversion/cancellation histories
are comparable in the NEW involution extension, but not the old
triangle extension; old GK5CG source equality/descent remains blocked. -/
theorem pentagonActualInvolutionOverlap_newVsTriangleWithSourceObstruction
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄)) :
    ∃ (c : pentagonAdjoinedSixCellAt f g h k A B C D₄ i
          (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
          (pentagonShortConservativeFiveCell f g h k A B C D₄ i)),
      Nonempty (PentagonAdjoinedSixCell.InvolutionEightCell
        (pentagonFinalConservativeLoop f g h k i)
        (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
        (pentagonShortConservativeFiveCell f g h k A B C D₄ i)
        (PentagonAdjoinedSixCell.sevenLeftDoubleInverseDirect c)
        (PentagonAdjoinedSixCell.sevenLeftDoubleInverseVia c)) ∧
      ¬ Nonempty (PentagonAdjoinedSixCell.TriangleEightCell
        (pentagonFinalConservativeLoop f g h k i)
        (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
        (pentagonShortConservativeFiveCell f g h k A B C D₄ i)
        (PentagonAdjoinedSixCell.sevenLeftDoubleInverseDirect c)
        (PentagonAdjoinedSixCell.sevenLeftDoubleInverseVia c)) ∧
      ¬ PentagonAdjoinedSixCellEqualityInterpreter f g h k A B C D₄ i := by
  refine ⟨pentagonAdjoinedSixCell_generator f g h k A B C D₄ i,
    ⟨PentagonAdjoinedSixCell.InvolutionEightCell.leftOverlap _⟩, ?_, ?_⟩
  · exact PentagonAdjoinedSixCell.sevenLeftDoubleInverse_noTriangleEightCell _
  · exact pentagonAdjoinedSixCell_noEqualityInterpreter f g h k A B C D₄ i

#print axioms PentagonAdjoinedSixCell.sevenInvolutionCharge
#print axioms PentagonAdjoinedSixCell.eightCell_preservesInvolutionCharge
#print axioms PentagonAdjoinedSixCell.triangleEightCell_preservesInvolutionCharge
#print axioms PentagonAdjoinedSixCell.sevenLeftDoubleInverse_chargeGap
#print axioms PentagonAdjoinedSixCell.sevenRightDoubleInverse_chargeGap
#print axioms PentagonAdjoinedSixCell.sevenLeftDoubleInverse_noTriangleEightCell
#print axioms PentagonAdjoinedSixCell.sevenRightDoubleInverse_noTriangleEightCell
#print axioms PentagonAdjoinedSixCell.sevenLeftDoubleInverse_notStrict
#print axioms PentagonAdjoinedSixCell.InvolutionEightCell
#print axioms PentagonAdjoinedSixCell.involutionEightCell_ofTriangle
#print axioms PentagonAdjoinedSixCell.involutionEightCell_leftNewNotPrevious
#print axioms PentagonAdjoinedSixCell.involutionEightCell_rightNewNotPrevious
#print axioms PentagonAdjoinedSixCell.involutionEightCell_noPreviousInterpreter
#print axioms PentagonAdjoinedSixCell.involutionEightCell_noStrictInterpreter
#print axioms PentagonAdjoinedSixCell.InvolutionCriticalPeak
#print axioms PentagonAdjoinedSixCell.involutionCriticalPeak_fill
#print axioms PentagonAdjoinedSixCell.involutionCriticalPeak_joinable
#print axioms PentagonAdjoinedSixCell.involutionHistorySetoid
#print axioms PentagonAdjoinedSixCell.involutionHistoryClass
#print axioms PentagonAdjoinedSixCell.involutionHistoryClass_eq_iff
#print axioms PentagonAdjoinedSixCell.triangleHistoryClass_descendsToInvolution
#print axioms PentagonAdjoinedSixCell.involutionHistoryClass_strictlyNew
#print axioms PentagonAdjoinedSixCell.involutionCriticalPeak_classEq
#print axioms PentagonAdjoinedSixCell.involutionHistoryClass_noStrictReturn
#print axioms pentagonActualInvolutionOverlap_newVsTriangleWithSourceObstruction

end ActualOriginalP77InvolutionOverlap
end FivefoldP77FiniteRefinement
end
end KUOS.Architecture.WuxingPentagonUnified
