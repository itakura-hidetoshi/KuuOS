import KUOS.Architecture.QiWuxingGK5CHP77InvolutionOverlapHigherObstructionV4_94

/-!
Qi v4.95 — INVERSE-OF-COMPOSITE / UNIT OVERLAP HIGHER OBSTRUCTION.

The successive new eight-cell presentations v4.91/4.93/4.94
correct only explicitly certified critical peaks. We identify
two further peaks: inverse-of-composite expansion overlaps with
left/right unit cancellation, on ACTUAL freely generated sixth-
and seventh-level syntax.

A THIRD signed integer charge counts precisely the original
SevenRewrite.inverseComp constructor. We prove that it is preserved
by all twenty-two original EightCell generators, by the two triangle
generators and typed context rules of TriangleEightCell, AND by
both double-inverse generators and contexts of InvolutionEightCell.

Each of two genuine inverse-composite/unit overlaps has two full
seven-cell derivation words with charges 0 and 1, proving that
neither admits an old InvolutionEightCell comparison. We adjoin
exactly two additional higher comparison generators in a distinct
InverseCompEightCell Type, without rewriting any old presentation
or changing source authority. Typed induction proves confluence
of the restricted new critical-peak family. A chosen history
quotient is strictly coarser than the previous quotient.

No arbitrary parallel seven-cell histories, no global higher
thinness, no old strict source Eq, and no nine-cell are asserted.
Append-only/tighten-only/same-root, strict 空 center,
independent Kuu = presentation. Lean v4.30.0-rc2,
mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6,
public roots107, protected #1558 remains Draft/open/unmerged.
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

/-- The third independent signed integer charge counts exactly the
inverse-of-composite local seven-cell generator; all other 13-rule
local generators carry zero charge. Context reversal negates,
composition adds, and six-cell inversion context preserves it. -/
def sevenInverseCompCharge {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s : SevenRewrite W long short c d) : ℤ :=
  match s with
  | .refl _ => 0
  | .symm s => -sevenInverseCompCharge s
  | .trans s t => sevenInverseCompCharge s + sevenInverseCompCharge t
  | .congrInv s => sevenInverseCompCharge s
  | .congrComp s t => sevenInverseCompCharge s + sevenInverseCompCharge t
  | .leftUnit _ => 0
  | .rightUnit _ => 0
  | .assoc _ _ _ => 0
  | .inverseRight _ => 0
  | .inverseLeft _ => 0
  | .doubleInverse _ => 0
  | .inverseId _ => 0
  | .inverseComp _ _ => 1

/-- All twenty-two original higher comparison generators preserve
the third charge. Constructor induction includes inverseComposite,
zigzagDiamond, and independent interchange, rather than assuming
soundness from the previous quotients. -/
theorem eightCell_preservesInverseCompCharge {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q : EightCell W long short s t) :
    sevenInverseCompCharge s = sevenInverseCompCharge t := by
  induction q with
  | reflexive s => rfl
  | reverse q ih => exact ih.symm
  | chain q q' ih ih' => exact ih.trans ih'
  | whiskerLeft before q ih =>
      simpa [sevenInverseCompCharge] using
        congrArg (fun n : ℤ => sevenInverseCompCharge before + n) ih
  | whiskerRight q after ih =>
      simpa [sevenInverseCompCharge] using
        congrArg (fun n : ℤ => n + sevenInverseCompCharge after) ih
  | reverseContext q ih =>
      simpa [sevenInverseCompCharge] using
        congrArg (fun n : ℤ => -n) ih
  | inverseContext q ih =>
      simpa [sevenInverseCompCharge] using ih
  | compositeContext q q' ih ih' =>
      simpa [sevenInverseCompCharge] using
        congrArg₂ (fun n m : ℤ => n + m) ih ih'
  | unitLeft s => simp [sevenInverseCompCharge]
  | unitRight s => simp [sevenInverseCompCharge]
  | associate s t u => simp [sevenInverseCompCharge, add_assoc]
  | cancelRight s => simp [sevenInverseCompCharge]
  | cancelLeft s => simp [sevenInverseCompCharge]
  | involute s => simp [sevenInverseCompCharge]
  | inverseIdentity c => simp [sevenInverseCompCharge]
  | inverseComposite s t =>
      simp [sevenInverseCompCharge] <;> abel
  | inverseCongruenceIdentity c => simp [sevenInverseCompCharge]
  | inverseCongruenceChain s t => simp [sevenInverseCompCharge]
  | compositeCongruenceIdentity c d => simp [sevenInverseCompCharge]
  | compositeCongruenceChain s s' t t' =>
      simp [sevenInverseCompCharge] <;> abel
  | interchange s t =>
      simp [sevenInverseCompCharge] <;> abel
  | zigzagDiamond c => simp [sevenInverseCompCharge]

/-- The entire triangle-extended higher grammar also preserves this
new charge: neither v4.93 triangle generator uses inverseComp. -/
theorem triangleEightCell_preservesInverseCompCharge {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q : TriangleEightCell W long short s t) :
    sevenInverseCompCharge s = sevenInverseCompCharge t := by
  induction q with
  | original q =>
      exact eightCell_preservesInverseCompCharge q
  | leftTriangle c d =>
      simp [sevenLeftTriangleDirect, sevenLeftTriangleViaAssoc,
        sevenInverseCompCharge]
  | rightTriangle c d =>
      simp [sevenRightTriangleDirect, sevenRightTriangleViaAssoc,
        sevenInverseCompCharge]
  | reverse q ih => exact ih.symm
  | chain q q' ih ih' => exact ih.trans ih'
  | whiskerLeft before q ih =>
      simpa [sevenInverseCompCharge] using
        congrArg (fun n : ℤ => sevenInverseCompCharge before + n) ih
  | whiskerRight q after ih =>
      simpa [sevenInverseCompCharge] using
        congrArg (fun n : ℤ => n + sevenInverseCompCharge after) ih
  | inverseContext q ih =>
      simpa [sevenInverseCompCharge] using ih
  | compositeContext q q' ih ih' =>
      simpa [sevenInverseCompCharge] using
        congrArg₂ (fun n m : ℤ => n + m) ih ih'

/-- The v4.94 involution extension, including its two new
doubleInverse/inverse-cancellation overlaps, still preserves the
third independent inverse-composition charge. -/
theorem involutionEightCell_preservesInverseCompCharge {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q : InvolutionEightCell W long short s t) :
    sevenInverseCompCharge s = sevenInverseCompCharge t := by
  induction q with
  | previous q =>
      exact triangleEightCell_preservesInverseCompCharge q
  | leftOverlap c =>
      simp [sevenLeftDoubleInverseDirect, sevenLeftDoubleInverseVia,
        sevenInverseCompCharge]
  | rightOverlap c =>
      simp [sevenRightDoubleInverseDirect, sevenRightDoubleInverseVia,
        sevenInverseCompCharge]
  | reverse q ih => exact ih.symm
  | chain q q' ih ih' => exact ih.trans ih'
  | whiskerLeft before q ih =>
      simpa [sevenInverseCompCharge] using
        congrArg (fun n : ℤ => sevenInverseCompCharge before + n) ih
  | whiskerRight q after ih =>
      simpa [sevenInverseCompCharge] using
        congrArg (fun n : ℤ => n + sevenInverseCompCharge after) ih
  | inverseContext q ih =>
      simpa [sevenInverseCompCharge] using ih
  | compositeContext q q' ih ih' =>
      simpa [sevenInverseCompCharge] using
        congrArg₂ (fun n m : ℤ => n + m) ih ih'

/-- Directly invert the existing LEFT unit proof: on the genuine raw
six-cell word symm (refl(w);c) the source word is retained. -/
def sevenInvCompLeftDirect {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    SevenRewrite W long short
      (.symm (.trans (.refl w) c)) (.symm c) :=
  .congrInv (.leftUnit c)

/-- Competing left overlap: inverse-of-composition first, then
inverse of identity and the right unit. This history uses exactly
ONE inverseComp constructor. -/
def sevenInvCompLeftVia {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    SevenRewrite W long short
      (.symm (.trans (.refl w) c)) (.symm c) :=
  .trans (.inverseComp (.refl w) c)
    (.trans
      (.congrComp (.refl (.symm c)) (.inverseId w))
      (.rightUnit (.symm c)))

/-- Directly invert the RIGHT unit cancellation. -/
def sevenInvCompRightDirect {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    SevenRewrite W long short
      (.symm (.trans c (.refl z))) (.symm c) :=
  .congrInv (.rightUnit c)

/-- Competing right overlap: inverse-of-composite expansion,
then inverse-of-identity, then left unit. -/
def sevenInvCompRightVia {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    SevenRewrite W long short
      (.symm (.trans c (.refl z))) (.symm c) :=
  .trans (.inverseComp c (.refl z))
    (.trans
      (.congrComp (.inverseId z) (.refl (.symm c)))
      (.leftUnit (.symm c)))

/-- Both genuine inverse-of-composite/unit critical peaks separate
under the preserved third integer charge: zero against one. -/
theorem sevenInvCompLeft_chargeGap {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    sevenInverseCompCharge (sevenInvCompLeftDirect c) = 0 ∧
    sevenInverseCompCharge (sevenInvCompLeftVia c) = 1 := by
  constructor <;>
    simp [sevenInvCompLeftDirect, sevenInvCompLeftVia,
      sevenInverseCompCharge]

theorem sevenInvCompRight_chargeGap {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    sevenInverseCompCharge (sevenInvCompRightDirect c) = 0 ∧
    sevenInverseCompCharge (sevenInvCompRightVia c) = 1 := by
  constructor <;>
    simp [sevenInvCompRightDirect, sevenInvCompRightVia,
      sevenInverseCompCharge]

/-- A certified impossibility, stronger than non-discovery: the
entire previous three-stage higher presentation CANNOT join the
left inverse-composition/unit peak. -/
theorem sevenInvCompLeft_noInvolutionEightCell {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    ¬ Nonempty (InvolutionEightCell W long short
      (sevenInvCompLeftDirect c) (sevenInvCompLeftVia c)) := by
  rintro ⟨q⟩
  have h := involutionEightCell_preservesInverseCompCharge q
  have hg := sevenInvCompLeft_chargeGap c
  rw [hg.1, hg.2] at h
  norm_num at h

theorem sevenInvCompRight_noInvolutionEightCell {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    ¬ Nonempty (InvolutionEightCell W long short
      (sevenInvCompRightDirect c) (sevenInvCompRightVia c)) := by
  rintro ⟨q⟩
  have h := involutionEightCell_preservesInverseCompCharge q
  have hg := sevenInvCompRight_chargeGap c
  rw [hg.1, hg.2] at h
  norm_num at h

theorem sevenInvCompLeft_notStrict {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    sevenInvCompLeftDirect c ≠ sevenInvCompLeftVia c := by
  intro heq
  have h := congrArg sevenInverseCompCharge heq
  have hg := sevenInvCompLeft_chargeGap c
  rw [hg.1, hg.2] at h
  norm_num at h

/-- A new and SEPARATE Type-valued higher comparison grammar.
No existing EightCell/TriangleEightCell/InvolutionEightCell is
changed. The only new elementary overlapping peaks are the
left/right inverseComp/unit triangles, plus typed closure rules. -/
inductive InverseCompEightCell (W : Type uSix) (l r : W) :
    {w z : W} →
    {c d : PentagonAdjoinedSixCell W l r w z} →
    SevenRewrite W l r c d →
    SevenRewrite W l r c d → Type uSix where
  | previous {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (q : InvolutionEightCell W l r s t) :
      InverseCompEightCell W l r s t
  | leftOverlap {w z : W}
      (c : PentagonAdjoinedSixCell W l r w z) :
      InverseCompEightCell W l r
        (sevenInvCompLeftDirect c) (sevenInvCompLeftVia c)
  | rightOverlap {w z : W}
      (c : PentagonAdjoinedSixCell W l r w z) :
      InverseCompEightCell W l r
        (sevenInvCompRightDirect c) (sevenInvCompRightVia c)
  | reverse {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (q : InverseCompEightCell W l r s t) :
      InverseCompEightCell W l r t s
  | chain {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
      {s t u : SevenRewrite W l r c d}
      (q : InverseCompEightCell W l r s t)
      (q' : InverseCompEightCell W l r t u) :
      InverseCompEightCell W l r s u
  | whiskerLeft {w z : W}
      {c d e : PentagonAdjoinedSixCell W l r w z}
      (before : SevenRewrite W l r c d)
      {s t : SevenRewrite W l r d e}
      (q : InverseCompEightCell W l r s t) :
      InverseCompEightCell W l r (.trans before s) (.trans before t)
  | whiskerRight {w z : W}
      {c d e : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (q : InverseCompEightCell W l r s t)
      (after : SevenRewrite W l r d e) :
      InverseCompEightCell W l r (.trans s after) (.trans t after)
  | inverseContext {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (q : InverseCompEightCell W l r s t) :
      InverseCompEightCell W l r (.congrInv s) (.congrInv t)
  | compositeContext {w x z : W}
      {c c' : PentagonAdjoinedSixCell W l r w x}
      {d d' : PentagonAdjoinedSixCell W l r x z}
      {s s' : SevenRewrite W l r c c'}
      {t t' : SevenRewrite W l r d d'}
      (q : InverseCompEightCell W l r s s')
      (q' : InverseCompEightCell W l r t t') :
      InverseCompEightCell W l r
        (.congrComp s t) (.congrComp s' t')

/-- No earlier higher comparison is discarded. -/
def inverseCompEightCell_ofInvolution {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q : InvolutionEightCell W long short s t) :
    InverseCompEightCell W long short s t :=
  .previous q

theorem inverseCompEightCell_leftNewNotPrevious {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    Nonempty (InverseCompEightCell W long short
      (sevenInvCompLeftDirect c) (sevenInvCompLeftVia c)) ∧
    ¬ Nonempty (InvolutionEightCell W long short
      (sevenInvCompLeftDirect c) (sevenInvCompLeftVia c)) :=
  ⟨⟨.leftOverlap c⟩, sevenInvCompLeft_noInvolutionEightCell c⟩

theorem inverseCompEightCell_rightNewNotPrevious {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    Nonempty (InverseCompEightCell W long short
      (sevenInvCompRightDirect c) (sevenInvCompRightVia c)) ∧
    ¬ Nonempty (InvolutionEightCell W long short
      (sevenInvCompRightDirect c) (sevenInvCompRightVia c)) :=
  ⟨⟨.rightOverlap c⟩, sevenInvCompRight_noInvolutionEightCell c⟩

/-- Strictly more expressive than the previously adjoined higher
presentation. Nonempty is used since the Pi type is Type-valued. -/
theorem inverseCompEightCell_noPreviousInterpreter (l r : W) :
    ¬ Nonempty (∀ {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      (s t : SevenRewrite W l r c d),
      InverseCompEightCell W l r s t → InvolutionEightCell W l r s t) := by
  rintro ⟨interpret⟩
  let c : PentagonAdjoinedSixCell W l r l l := .refl l
  have h : InvolutionEightCell W l r
      (sevenInvCompLeftDirect c) (sevenInvCompLeftVia c) :=
    interpret _ _ (.leftOverlap c)
  exact sevenInvCompLeft_noInvolutionEightCell c ⟨h⟩

theorem inverseCompEightCell_noStrictInterpreter (l r : W) :
    ¬ (∀ {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
      (s t : SevenRewrite W l r c d),
      InverseCompEightCell W l r s t → s = t) := by
  intro interpret
  apply involutionEightCell_noStrictInterpreter l r
  intro w z c d s t h
  exact interpret s t (.previous h)

/-- The recursively generated, restricted critical-peak family:
all previous involution peaks plus TWO actual inverse-composition
unit overlaps and precisely typed coherence contexts. -/
inductive InverseCompCriticalPeak (W : Type uSix) (l r : W) :
    {w z : W} →
    {c d : PentagonAdjoinedSixCell W l r w z} →
    SevenRewrite W l r c d →
    SevenRewrite W l r c d → Type uSix where
  | previous {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (p : InvolutionCriticalPeak W l r s t) :
      InverseCompCriticalPeak W l r s t
  | leftOverlap {w z : W}
      (c : PentagonAdjoinedSixCell W l r w z) :
      InverseCompCriticalPeak W l r
        (sevenInvCompLeftDirect c) (sevenInvCompLeftVia c)
  | rightOverlap {w z : W}
      (c : PentagonAdjoinedSixCell W l r w z) :
      InverseCompCriticalPeak W l r
        (sevenInvCompRightDirect c) (sevenInvCompRightVia c)
  | reverse {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (p : InverseCompCriticalPeak W l r s t) :
      InverseCompCriticalPeak W l r t s
  | chain {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
      {s t u : SevenRewrite W l r c d}
      (p : InverseCompCriticalPeak W l r s t)
      (q : InverseCompCriticalPeak W l r t u) :
      InverseCompCriticalPeak W l r s u
  | whiskerLeft {w z : W} {c d e : PentagonAdjoinedSixCell W l r w z}
      (before : SevenRewrite W l r c d)
      {s t : SevenRewrite W l r d e}
      (p : InverseCompCriticalPeak W l r s t) :
      InverseCompCriticalPeak W l r (.trans before s) (.trans before t)
  | whiskerRight {w z : W} {c d e : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (p : InverseCompCriticalPeak W l r s t)
      (after : SevenRewrite W l r d e) :
      InverseCompCriticalPeak W l r (.trans s after) (.trans t after)
  | inverseContext {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (p : InverseCompCriticalPeak W l r s t) :
      InverseCompCriticalPeak W l r (.congrInv s) (.congrInv t)
  | compositeContext {w x z : W}
      {c c' : PentagonAdjoinedSixCell W l r w x}
      {d d' : PentagonAdjoinedSixCell W l r x z}
      {s s' : SevenRewrite W l r c c'}
      {t t' : SevenRewrite W l r d d'}
      (p : InverseCompCriticalPeak W l r s s')
      (q : InverseCompCriticalPeak W l r t t') :
      InverseCompCriticalPeak W l r
        (.congrComp s t) (.congrComp s' t')

/-- Constructive, all-generator induction for the selected family. -/
def inverseCompCriticalPeak_fill {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (p : InverseCompCriticalPeak W long short s t) :
    InverseCompEightCell W long short s t := by
  induction p with
  | previous p =>
      exact .previous (involutionCriticalPeak_fill p)
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

theorem inverseCompCriticalPeak_joinable {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (p : InverseCompCriticalPeak W long short s t) :
    Nonempty (InverseCompEightCell W long short s t) :=
  ⟨inverseCompCriticalPeak_fill p⟩

/-- Chosen high-history quotient of original RAW seventh-level
histories, rather than overwriting the old quotient or source. -/
def inverseCompHistorySetoid (W : Type uSix) (l r : W)
    {w z : W} {c d : PentagonAdjoinedSixCell W l r w z} :
    Setoid (SevenRewrite W l r c d) where
  r := fun s t => Nonempty (InverseCompEightCell W l r s t)
  iseqv := by
    constructor
    · intro s
      exact ⟨.previous (.previous (.original (.reflexive s)))⟩
    · intro s t h
      rcases h with ⟨h⟩
      exact ⟨.reverse h⟩
    · intro s t u hs ht
      rcases hs with ⟨hs⟩
      rcases ht with ⟨ht⟩
      exact ⟨.chain hs ht⟩

def inverseCompHistoryClass {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s : SevenRewrite W long short c d) :
    Quotient (inverseCompHistorySetoid W long short (c := c) (d := d)) :=
  Quotient.mk _ s

theorem inverseCompHistoryClass_eq_iff {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s t : SevenRewrite W long short c d) :
    inverseCompHistoryClass s = inverseCompHistoryClass t ↔
      Nonempty (InverseCompEightCell W long short s t) := by
  constructor
  · intro h
    exact Quotient.exact h
  · intro h
    exact Quotient.sound h

theorem involutionHistoryClass_descendsToInverseComp {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s t : SevenRewrite W long short c d)
    (h : involutionHistoryClass s = involutionHistoryClass t) :
    inverseCompHistoryClass s = inverseCompHistoryClass t := by
  rcases (involutionHistoryClass_eq_iff s t).1 h with ⟨q⟩
  exact (inverseCompHistoryClass_eq_iff s t).2 ⟨.previous q⟩

/-- Strict coarsening of the former higher history quotient:
the two explicit left unit/inverseComp histories were separated
before and are equal only in the newly adjoined quotient. -/
theorem inverseCompHistoryClass_strictlyNew {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    (inverseCompHistoryClass (sevenInvCompLeftDirect c) =
      inverseCompHistoryClass (sevenInvCompLeftVia c)) ∧
    involutionHistoryClass (sevenInvCompLeftDirect c) ≠
      involutionHistoryClass (sevenInvCompLeftVia c) := by
  constructor
  · exact (inverseCompHistoryClass_eq_iff _ _).2 ⟨.leftOverlap c⟩
  · intro h
    exact sevenInvCompLeft_noInvolutionEightCell c
      ((involutionHistoryClass_eq_iff _ _).1 h)

theorem inverseCompCriticalPeak_classEq {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (p : InverseCompCriticalPeak W long short s t) :
    inverseCompHistoryClass s = inverseCompHistoryClass t :=
  (inverseCompHistoryClass_eq_iff _ _).2
    (inverseCompCriticalPeak_joinable p)

theorem inverseCompHistoryClass_noStrictReturn (l r : W) :
    ¬ (∀ {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
      (s t : SevenRewrite W l r c d),
      inverseCompHistoryClass s = inverseCompHistoryClass t → s = t) := by
  intro interpret
  apply inverseCompEightCell_noStrictInterpreter l r
  intro w z c d s t q
  exact interpret s t ((inverseCompHistoryClass_eq_iff s t).2 ⟨q⟩)

end PentagonAdjoinedSixCell

section ActualOriginalP77InverseCompositionOverlap
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

/-- At EVERY genuine P77 terminal raw index, the original GK5CG
five-cell endpoints determine an actual adjoined six-cell generator.
Its two seventh-level inverseComp/unit histories gain a NEW higher
comparison while the old comparison remains obstructed. Old source
equality descent is still impossible. -/
theorem pentagonActualInverseCompOverlap_newVsInvolutionWithSourceObstruction
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄)) :
    ∃ (c : pentagonAdjoinedSixCellAt f g h k A B C D₄ i
          (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
          (pentagonShortConservativeFiveCell f g h k A B C D₄ i)),
      Nonempty (PentagonAdjoinedSixCell.InverseCompEightCell
        (pentagonFinalConservativeLoop f g h k i)
        (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
        (pentagonShortConservativeFiveCell f g h k A B C D₄ i)
        (PentagonAdjoinedSixCell.sevenInvCompLeftDirect c)
        (PentagonAdjoinedSixCell.sevenInvCompLeftVia c)) ∧
      ¬ Nonempty (PentagonAdjoinedSixCell.InvolutionEightCell
        (pentagonFinalConservativeLoop f g h k i)
        (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
        (pentagonShortConservativeFiveCell f g h k A B C D₄ i)
        (PentagonAdjoinedSixCell.sevenInvCompLeftDirect c)
        (PentagonAdjoinedSixCell.sevenInvCompLeftVia c)) ∧
      ¬ PentagonAdjoinedSixCellEqualityInterpreter f g h k A B C D₄ i := by
  refine ⟨pentagonAdjoinedSixCell_generator f g h k A B C D₄ i,
    ⟨PentagonAdjoinedSixCell.InverseCompEightCell.leftOverlap _⟩, ?_, ?_⟩
  · exact PentagonAdjoinedSixCell.sevenInvCompLeft_noInvolutionEightCell _
  · exact pentagonAdjoinedSixCell_noEqualityInterpreter f g h k A B C D₄ i

#print axioms PentagonAdjoinedSixCell.sevenInverseCompCharge
#print axioms PentagonAdjoinedSixCell.eightCell_preservesInverseCompCharge
#print axioms PentagonAdjoinedSixCell.triangleEightCell_preservesInverseCompCharge
#print axioms PentagonAdjoinedSixCell.involutionEightCell_preservesInverseCompCharge
#print axioms PentagonAdjoinedSixCell.sevenInvCompLeft_chargeGap
#print axioms PentagonAdjoinedSixCell.sevenInvCompRight_chargeGap
#print axioms PentagonAdjoinedSixCell.sevenInvCompLeft_noInvolutionEightCell
#print axioms PentagonAdjoinedSixCell.sevenInvCompRight_noInvolutionEightCell
#print axioms PentagonAdjoinedSixCell.sevenInvCompLeft_notStrict
#print axioms PentagonAdjoinedSixCell.InverseCompEightCell
#print axioms PentagonAdjoinedSixCell.inverseCompEightCell_ofInvolution
#print axioms PentagonAdjoinedSixCell.inverseCompEightCell_leftNewNotPrevious
#print axioms PentagonAdjoinedSixCell.inverseCompEightCell_rightNewNotPrevious
#print axioms PentagonAdjoinedSixCell.inverseCompEightCell_noPreviousInterpreter
#print axioms PentagonAdjoinedSixCell.inverseCompEightCell_noStrictInterpreter
#print axioms PentagonAdjoinedSixCell.InverseCompCriticalPeak
#print axioms PentagonAdjoinedSixCell.inverseCompCriticalPeak_fill
#print axioms PentagonAdjoinedSixCell.inverseCompCriticalPeak_joinable
#print axioms PentagonAdjoinedSixCell.inverseCompHistorySetoid
#print axioms PentagonAdjoinedSixCell.inverseCompHistoryClass
#print axioms PentagonAdjoinedSixCell.inverseCompHistoryClass_eq_iff
#print axioms PentagonAdjoinedSixCell.involutionHistoryClass_descendsToInverseComp
#print axioms PentagonAdjoinedSixCell.inverseCompHistoryClass_strictlyNew
#print axioms PentagonAdjoinedSixCell.inverseCompCriticalPeak_classEq
#print axioms PentagonAdjoinedSixCell.inverseCompHistoryClass_noStrictReturn
#print axioms pentagonActualInverseCompOverlap_newVsInvolutionWithSourceObstruction

end ActualOriginalP77InverseCompositionOverlap
end FivefoldP77FiniteRefinement
end
end KUOS.Architecture.WuxingPentagonUnified
