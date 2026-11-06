import KUOS.Architecture.QiWuxingGK5CHP77EightCellCriticalPeakClosureV4_92

/-!
Qi v4.93 — A GENUINE MISSING HIGHER CRITICAL PEAK: ASSOCIATIVITY/UNIT
TRIANGLES, AN INTEGER OBSTRUCTION, AND A CONSERVATIVE EIGHT-CELL EXTENSION.

The previous v4.91 EightCell has twenty-two generators. v4.92 proved
constructive confluence only for its restricted zigzag/interchange
critical-peak closure. Here we analyze two distinct, previously
unclassified, overlapping seven-cell reductions:
  ((id ; c) ; d) => (c ; d) (left triangle), and
  ((c ; d) ; id) => (c ; d) (right triangle).

A RECURSIVE INTEGER CHARGE on the full original SevenRewrite syntax
counts .assoc plus .inverseRight, with signs on reversed proof paths.
We prove that ALL twenty-two v4.91 eight-cell generators preserve
this charge (induction on actual eight-cell syntax). Both triangles
carry a nonzero charge difference. Hence no original EightCell can
compare either triangle pair. This is a PROVEN relative obstruction,
not a guess that a derivation is difficult to find.

Rather than overwrite or weaken the original EightCell, we freely
adjoin a *separate* TriangleEightCell presentation with an explicit
inclusion of existing eight-cells and TWO precise additional triangle
generators. We then prove construction on the expanded local peak
family, strict separation of old and new higher history quotients,
and old-source equality/descent obstruction at every original P77
terminal raw index. No global coherence or arbitrary-equality
generator is introduced; no old source signature is changed.

Append-only / tighten-only / same-root, strict 空 center,
independent Kuu = presentation. Lean v4.30.0-rc2; pinned mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6;
public roots 107; protected #1558 remains Draft/open/unmerged.
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

/-- Signed integer invariant of the EXACT original 13-rule SevenRewrite
syntax, defined structurally, without quotienting or introducing an
axiom. Associativity and right inverse cancellation carry charge +1.
The choice makes the old v4.91 zigzag critical diamond charge-sound. -/
def sevenTriangleCharge {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s : SevenRewrite W long short c d) : ℤ :=
  match s with
  | .refl _ => 0
  | .symm s => -sevenTriangleCharge s
  | .trans s t => sevenTriangleCharge s + sevenTriangleCharge t
  | .congrInv s => sevenTriangleCharge s
  | .congrComp s t => sevenTriangleCharge s + sevenTriangleCharge t
  | .leftUnit _ => 0
  | .rightUnit _ => 0
  | .assoc _ _ _ => 1
  | .inverseRight _ => 1
  | .inverseLeft _ => 0
  | .doubleInverse _ => 0
  | .inverseId _ => 0
  | .inverseComp _ _ => 0

/-- Every one of the ORIGINAL 22 EightCell constructors preserves
the new seven-level integer charge. This is a substantive induction
over raw eight-cell proof syntax, not a claim about quotient equality. -/
theorem eightCell_preservesTriangleCharge {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q : EightCell W long short s t) :
    sevenTriangleCharge s = sevenTriangleCharge t := by
  induction q with
  | reflexive s => rfl
  | reverse q ih => exact ih.symm
  | chain q q' ih ih' => exact ih.trans ih'
  | whiskerLeft before q ih =>
      simpa [sevenTriangleCharge] using
        congrArg (fun n : ℤ => sevenTriangleCharge before + n) ih
  | whiskerRight q after ih =>
      simpa [sevenTriangleCharge] using
        congrArg (fun n : ℤ => n + sevenTriangleCharge after) ih
  | reverseContext q ih =>
      simpa [sevenTriangleCharge] using
        congrArg (fun n : ℤ => -n) ih
  | inverseContext q ih =>
      simpa [sevenTriangleCharge] using ih
  | compositeContext q q' ih ih' =>
      simpa [sevenTriangleCharge] using
        congrArg₂ (fun n m : ℤ => n + m) ih ih'
  | unitLeft s => simp [sevenTriangleCharge]
  | unitRight s => simp [sevenTriangleCharge]
  | associate s t u => simp [sevenTriangleCharge, add_assoc]
  | cancelRight s => simp [sevenTriangleCharge]
  | cancelLeft s => simp [sevenTriangleCharge]
  | involute s => simp [sevenTriangleCharge]
  | inverseIdentity c => simp [sevenTriangleCharge]
  | inverseComposite s t =>
      simp [sevenTriangleCharge] <;> abel
  | inverseCongruenceIdentity c => simp [sevenTriangleCharge]
  | inverseCongruenceChain s t => simp [sevenTriangleCharge]
  | compositeCongruenceIdentity c d => simp [sevenTriangleCharge]
  | compositeCongruenceChain s s' t t' =>
      simp [sevenTriangleCharge] <;> abel
  | interchange s t =>
      simp [sevenTriangleCharge] <;> abel
  | zigzagDiamond c => simp [sevenTriangleCharge]

/-- First branch of a unit/association critical overlap:
cancel the INNER left unit, then leave the outer composite fixed. -/
def sevenLeftTriangleDirect {w x z : W}
    (c : PentagonAdjoinedSixCell W long short w x)
    (d : PentagonAdjoinedSixCell W long short x z) :
    SevenRewrite W long short
      (.trans (.trans (.refl w) c) d) (.trans c d) :=
  .congrComp (.leftUnit c) (.refl d)

/-- Second branch of the SAME left-unit critical overlap:
reassociate first, then cancel the OUTER left unit. -/
def sevenLeftTriangleViaAssoc {w x z : W}
    (c : PentagonAdjoinedSixCell W long short w x)
    (d : PentagonAdjoinedSixCell W long short x z) :
    SevenRewrite W long short
      (.trans (.trans (.refl w) c) d) (.trans c d) :=
  .trans (.assoc (.refl w) c d) (.leftUnit (.trans c d))

/-- First branch of the right-unit/associator overlap. -/
def sevenRightTriangleDirect {w x z : W}
    (c : PentagonAdjoinedSixCell W long short w x)
    (d : PentagonAdjoinedSixCell W long short x z) :
    SevenRewrite W long short
      (.trans (.trans c d) (.refl z)) (.trans c d) :=
  .rightUnit (.trans c d)

/-- Second branch: associate, then cancel the inner right unit. -/
def sevenRightTriangleViaAssoc {w x z : W}
    (c : PentagonAdjoinedSixCell W long short w x)
    (d : PentagonAdjoinedSixCell W long short x z) :
    SevenRewrite W long short
      (.trans (.trans c d) (.refl z)) (.trans c d) :=
  .trans (.assoc c d (.refl z))
    (.congrComp (.refl c) (.rightUnit d))

/-- The left overlap has an EXACT nonzero charge gap (0 versus 1). -/
theorem sevenLeftTriangle_chargeGap {w x z : W}
    (c : PentagonAdjoinedSixCell W long short w x)
    (d : PentagonAdjoinedSixCell W long short x z) :
    sevenTriangleCharge (sevenLeftTriangleDirect c d) = 0 ∧
    sevenTriangleCharge (sevenLeftTriangleViaAssoc c d) = 1 := by
  constructor <;> simp [sevenLeftTriangleDirect, sevenLeftTriangleViaAssoc,
    sevenTriangleCharge]

/-- The right overlap has the same nonzero charge gap. -/
theorem sevenRightTriangle_chargeGap {w x z : W}
    (c : PentagonAdjoinedSixCell W long short w x)
    (d : PentagonAdjoinedSixCell W long short x z) :
    sevenTriangleCharge (sevenRightTriangleDirect c d) = 0 ∧
    sevenTriangleCharge (sevenRightTriangleViaAssoc c d) = 1 := by
  constructor <;> simp [sevenRightTriangleDirect, sevenRightTriangleViaAssoc,
    sevenTriangleCharge]

/-- PROVED OBSTRUCTION: the original twenty-two-rule EightCell CANNOT
join the left triangle, regardless of the underlying source objects. -/
theorem sevenLeftTriangle_noOldEightCell {w x z : W}
    (c : PentagonAdjoinedSixCell W long short w x)
    (d : PentagonAdjoinedSixCell W long short x z) :
    ¬ Nonempty (EightCell W long short
      (sevenLeftTriangleDirect c d) (sevenLeftTriangleViaAssoc c d)) := by
  rintro ⟨q⟩
  have hc := eightCell_preservesTriangleCharge q
  have hg := sevenLeftTriangle_chargeGap c d
  rw [hg.1, hg.2] at hc
  norm_num at hc

/-- The opposite triangle is independently obstructed too. -/
theorem sevenRightTriangle_noOldEightCell {w x z : W}
    (c : PentagonAdjoinedSixCell W long short w x)
    (d : PentagonAdjoinedSixCell W long short x z) :
    ¬ Nonempty (EightCell W long short
      (sevenRightTriangleDirect c d) (sevenRightTriangleViaAssoc c d)) := by
  rintro ⟨q⟩
  have hc := eightCell_preservesTriangleCharge q
  have hg := sevenRightTriangle_chargeGap c d
  rw [hg.1, hg.2] at hc
  norm_num at hc

/-- These histories differ as RAW seventh-level syntax as well:
equality would contradict the explicitly evaluated integer charge. -/
theorem sevenLeftTriangle_notStrict {w x z : W}
    (c : PentagonAdjoinedSixCell W long short w x)
    (d : PentagonAdjoinedSixCell W long short x z) :
    sevenLeftTriangleDirect c d ≠ sevenLeftTriangleViaAssoc c d := by
  intro heq
  have hc := congrArg sevenTriangleCharge heq
  have hg := sevenLeftTriangle_chargeGap c d
  rw [hg.1, hg.2] at hc
  norm_num at hc

/-- An APPEND-ONLY extension of the ORIGINAL eight-cell grammar.
It preserves every old witness via .original, and adds precisely
two unit/association triangle generators, plus typed context
composition. It does NOT declare arbitrary parallel histories equal. -/
inductive TriangleEightCell (W : Type uSix) (l r : W) :
    {w z : W} →
    {c d : PentagonAdjoinedSixCell W l r w z} →
    SevenRewrite W l r c d →
    SevenRewrite W l r c d → Type uSix where
  | original {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (q : EightCell W l r s t) :
      TriangleEightCell W l r s t
  | leftTriangle {w x z : W}
      (c : PentagonAdjoinedSixCell W l r w x)
      (d : PentagonAdjoinedSixCell W l r x z) :
      TriangleEightCell W l r
        (sevenLeftTriangleDirect c d) (sevenLeftTriangleViaAssoc c d)
  | rightTriangle {w x z : W}
      (c : PentagonAdjoinedSixCell W l r w x)
      (d : PentagonAdjoinedSixCell W l r x z) :
      TriangleEightCell W l r
        (sevenRightTriangleDirect c d) (sevenRightTriangleViaAssoc c d)
  | reverse {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (q : TriangleEightCell W l r s t) :
      TriangleEightCell W l r t s
  | chain {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t u : SevenRewrite W l r c d}
      (q : TriangleEightCell W l r s t)
      (q' : TriangleEightCell W l r t u) :
      TriangleEightCell W l r s u
  | whiskerLeft {w z : W}
      {c d e : PentagonAdjoinedSixCell W l r w z}
      (before : SevenRewrite W l r c d)
      {s t : SevenRewrite W l r d e}
      (q : TriangleEightCell W l r s t) :
      TriangleEightCell W l r (.trans before s) (.trans before t)
  | whiskerRight {w z : W}
      {c d e : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (q : TriangleEightCell W l r s t)
      (after : SevenRewrite W l r d e) :
      TriangleEightCell W l r (.trans s after) (.trans t after)
  | inverseContext {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (q : TriangleEightCell W l r s t) :
      TriangleEightCell W l r (.congrInv s) (.congrInv t)
  | compositeContext {w x z : W}
      {c c' : PentagonAdjoinedSixCell W l r w x}
      {d d' : PentagonAdjoinedSixCell W l r x z}
      {s s' : SevenRewrite W l r c c'}
      {t t' : SevenRewrite W l r d d'}
      (q : TriangleEightCell W l r s s')
      (q' : TriangleEightCell W l r t t') :
      TriangleEightCell W l r
        (.congrComp s t) (.congrComp s' t')

/-- Every old eighth-level comparison stays valid in the extension. -/
def triangleEightCell_ofOld {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q : EightCell W long short s t) :
    TriangleEightCell W long short s t :=
  .original q

/-- The NEW left triangle is now filled, while the original eight-cell
family provably remains unable to fill it. -/
theorem triangleEightCell_leftNewNotOld {w x z : W}
    (c : PentagonAdjoinedSixCell W long short w x)
    (d : PentagonAdjoinedSixCell W long short x z) :
    Nonempty (TriangleEightCell W long short
      (sevenLeftTriangleDirect c d) (sevenLeftTriangleViaAssoc c d)) ∧
    ¬ Nonempty (EightCell W long short
      (sevenLeftTriangleDirect c d) (sevenLeftTriangleViaAssoc c d)) :=
  ⟨⟨.leftTriangle c d⟩, sevenLeftTriangle_noOldEightCell c d⟩

/-- The right triangle is also new relative to the old 22-generator
presentation. -/
theorem triangleEightCell_rightNewNotOld {w x z : W}
    (c : PentagonAdjoinedSixCell W long short w x)
    (d : PentagonAdjoinedSixCell W long short x z) :
    Nonempty (TriangleEightCell W long short
      (sevenRightTriangleDirect c d) (sevenRightTriangleViaAssoc c d)) ∧
    ¬ Nonempty (EightCell W long short
      (sevenRightTriangleDirect c d) (sevenRightTriangleViaAssoc c d)) :=
  ⟨⟨.rightTriangle c d⟩, sevenRightTriangle_noOldEightCell c d⟩

/-- The extension is STRICT: no map that sends every new triangle
comparison into the old eight-cell grammar can exist. -/
theorem triangleEightCell_noOldInterpreter (l r : W) :
    ¬ (∀ {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
        (s t : SevenRewrite W l r c d),
        TriangleEightCell W l r s t → EightCell W l r s t) := by
  intro interpret
  let c : PentagonAdjoinedSixCell W l r l l := .refl l
  have h : EightCell W l r
      (sevenLeftTriangleDirect c c) (sevenLeftTriangleViaAssoc c c) :=
    interpret _ _ (.leftTriangle c c)
  exact sevenLeftTriangle_noOldEightCell c c ⟨h⟩

/-- In particular, new eighth-level comparisons cannot be mistaken
for strict equality of the original seventh-level raw proof terms. -/
theorem triangleEightCell_noStrictInterpreter (l r : W) :
    ¬ (∀ {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
        (s t : SevenRewrite W l r c d),
        TriangleEightCell W l r s t → s = t) := by
  intro interpret
  apply eightCell_noStrictSevenInterpreter l r
  intro w z c d s t h
  exact interpret s t (.original h)

/-- The newly enlarged but still RESTRICTED critical peak family,
built from the previous v4.92 local family plus the TWO proven-missing
triangle overlaps and type-correct congruence/pasting contexts. -/
inductive TriangleCriticalPeak (W : Type uSix) (l r : W) :
    {w z : W} →
    {c d : PentagonAdjoinedSixCell W l r w z} →
    SevenRewrite W l r c d →
    SevenRewrite W l r c d → Type uSix where
  | previous {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (p : LocalCriticalPeak W l r s t) :
      TriangleCriticalPeak W l r s t
  | leftTriangle {w x z : W}
      (c : PentagonAdjoinedSixCell W l r w x)
      (d : PentagonAdjoinedSixCell W l r x z) :
      TriangleCriticalPeak W l r
        (sevenLeftTriangleDirect c d) (sevenLeftTriangleViaAssoc c d)
  | rightTriangle {w x z : W}
      (c : PentagonAdjoinedSixCell W l r w x)
      (d : PentagonAdjoinedSixCell W l r x z) :
      TriangleCriticalPeak W l r
        (sevenRightTriangleDirect c d) (sevenRightTriangleViaAssoc c d)
  | reverse {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (p : TriangleCriticalPeak W l r s t) :
      TriangleCriticalPeak W l r t s
  | chain {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t u : SevenRewrite W l r c d}
      (p : TriangleCriticalPeak W l r s t)
      (q : TriangleCriticalPeak W l r t u) :
      TriangleCriticalPeak W l r s u
  | whiskerLeft {w z : W}
      {c d e : PentagonAdjoinedSixCell W l r w z}
      (before : SevenRewrite W l r c d)
      {s t : SevenRewrite W l r d e}
      (p : TriangleCriticalPeak W l r s t) :
      TriangleCriticalPeak W l r (.trans before s) (.trans before t)
  | whiskerRight {w z : W}
      {c d e : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (p : TriangleCriticalPeak W l r s t)
      (after : SevenRewrite W l r d e) :
      TriangleCriticalPeak W l r (.trans s after) (.trans t after)
  | inverseContext {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (p : TriangleCriticalPeak W l r s t) :
      TriangleCriticalPeak W l r (.congrInv s) (.congrInv t)
  | compositeContext {w x z : W}
      {c c' : PentagonAdjoinedSixCell W l r w x}
      {d d' : PentagonAdjoinedSixCell W l r x z}
      {s s' : SevenRewrite W l r c c'}
      {t t' : SevenRewrite W l r d d'}
      (p : TriangleCriticalPeak W l r s s')
      (q : TriangleCriticalPeak W l r t t') :
      TriangleCriticalPeak W l r
        (.congrComp s t) (.congrComp s' t')

/-- All peaks in the new limited overlap family have REAL higher
witnesses, proved by structural induction without a blanket
all-parallel-history constructor. -/
def triangleCriticalPeak_fill {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (p : TriangleCriticalPeak W long short s t) :
    TriangleEightCell W long short s t := by
  induction p with
  | previous p =>
      exact .original (localCriticalPeak_eightCell p)
  | leftTriangle c d =>
      exact .leftTriangle c d
  | rightTriangle c d =>
      exact .rightTriangle c d
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

/-- Type-valued joinability of precisely the triangle-extended
critical peak class (not global higher confluence). -/
theorem triangleCriticalPeak_joinable {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (p : TriangleCriticalPeak W long short s t) :
    Nonempty (TriangleEightCell W long short s t) :=
  ⟨triangleCriticalPeak_fill p⟩

/-- Equivalence on raw seventh-level histories generated by the
new higher proof witnesses. -/
def triangleHistorySetoid (W : Type uSix) (l r : W)
    {w z : W} {c d : PentagonAdjoinedSixCell W l r w z} :
    Setoid (SevenRewrite W l r c d) where
  r := fun s t => Nonempty (TriangleEightCell W l r s t)
  iseqv := by
    constructor
    · intro s
      exact ⟨.original (.reflexive s)⟩
    · intro s t h
      rcases h with ⟨h⟩
      exact ⟨.reverse h⟩
    · intro s t u hs ht
      rcases hs with ⟨hs⟩
      rcases ht with ⟨ht⟩
      exact ⟨.chain hs ht⟩

def triangleHistoryClass {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s : SevenRewrite W long short c d) :
    Quotient (triangleHistorySetoid W long short (c := c) (d := d)) :=
  Quotient.mk _ s

theorem triangleHistoryClass_eq_iff {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s t : SevenRewrite W long short c d) :
    triangleHistoryClass s = triangleHistoryClass t ↔
      Nonempty (TriangleEightCell W long short s t) := by
  constructor
  · intro h
    exact Quotient.exact h
  · intro h
    exact Quotient.sound h

/-- Every equality from the original v4.92 eighth-history quotient
is still true in the new triangle-extended quotient. -/
theorem oldHistoryClass_descendsToTriangle {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s t : SevenRewrite W long short c d)
    (h : eightHistoryClass s = eightHistoryClass t) :
    triangleHistoryClass s = triangleHistoryClass t := by
  rcases (eightHistoryClass_eq_iff s t).1 h with ⟨q⟩
  exact (triangleHistoryClass_eq_iff s t).2 ⟨.original q⟩

/-- The new quotient is PROVABLY STRICTLY COARSER on every left
triangle: the two classes merge only after adding the two triangles,
while the original EightCell-generated quotient still separates them. -/
theorem triangleHistoryClass_strictlyNew {w x z : W}
    (c : PentagonAdjoinedSixCell W long short w x)
    (d : PentagonAdjoinedSixCell W long short x z) :
    (triangleHistoryClass (sevenLeftTriangleDirect c d) =
      triangleHistoryClass (sevenLeftTriangleViaAssoc c d)) ∧
    eightHistoryClass (sevenLeftTriangleDirect c d) ≠
      eightHistoryClass (sevenLeftTriangleViaAssoc c d) := by
  constructor
  · exact (triangleHistoryClass_eq_iff _ _).2 ⟨.leftTriangle c d⟩
  · intro heq
    exact sevenLeftTriangle_noOldEightCell c d
      ((eightHistoryClass_eq_iff _ _).1 heq)

/-- The old-source authority obstruction is independent of the
new conservative completion; at every original P77 raw index we
exhibit an ACTUAL original five-cell generator used in the triangle. -/
end PentagonAdjoinedSixCell

section ActualOriginalP77TriangleOverlap
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

/-- The missing left associativity/unit triangle exists at EVERY
actual original P77 terminal raw index, with genuine old GK5CG
five-cell endpoint data in the six-cell generator. The OLD
twenty-two-rule eighth-level proof is obstructed by integer charge;
the NEW triangle extension fills it and no original source equality
interpreter is introduced. -/
theorem pentagonActualTriangle_newVsOldWithSourceObstruction
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄)) :
    ∃ (c : pentagonAdjoinedSixCellAt f g h k A B C D₄ i
          (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
          (pentagonShortConservativeFiveCell f g h k A B C D₄ i)),
      Nonempty (PentagonAdjoinedSixCell.TriangleEightCell
        (pentagonFinalConservativeLoop f g h k i)
        (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
        (pentagonShortConservativeFiveCell f g h k A B C D₄ i)
        (PentagonAdjoinedSixCell.sevenLeftTriangleDirect c (.symm c))
        (PentagonAdjoinedSixCell.sevenLeftTriangleViaAssoc c (.symm c))) ∧
      ¬ Nonempty (PentagonAdjoinedSixCell.EightCell
        (pentagonFinalConservativeLoop f g h k i)
        (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
        (pentagonShortConservativeFiveCell f g h k A B C D₄ i)
        (PentagonAdjoinedSixCell.sevenLeftTriangleDirect c (.symm c))
        (PentagonAdjoinedSixCell.sevenLeftTriangleViaAssoc c (.symm c))) ∧
      ¬ PentagonAdjoinedSixCellEqualityInterpreter f g h k A B C D₄ i := by
  refine ⟨pentagonAdjoinedSixCell_generator f g h k A B C D₄ i,
    ⟨PentagonAdjoinedSixCell.TriangleEightCell.leftTriangle _ _⟩, ?_, ?_⟩
  · exact PentagonAdjoinedSixCell.sevenLeftTriangle_noOldEightCell _ _
  · exact pentagonAdjoinedSixCell_noEqualityInterpreter f g h k A B C D₄ i

#print axioms PentagonAdjoinedSixCell.sevenTriangleCharge
#print axioms PentagonAdjoinedSixCell.eightCell_preservesTriangleCharge
#print axioms PentagonAdjoinedSixCell.sevenLeftTriangle_chargeGap
#print axioms PentagonAdjoinedSixCell.sevenRightTriangle_chargeGap
#print axioms PentagonAdjoinedSixCell.sevenLeftTriangle_noOldEightCell
#print axioms PentagonAdjoinedSixCell.sevenRightTriangle_noOldEightCell
#print axioms PentagonAdjoinedSixCell.sevenLeftTriangle_notStrict
#print axioms PentagonAdjoinedSixCell.TriangleEightCell
#print axioms PentagonAdjoinedSixCell.triangleEightCell_ofOld
#print axioms PentagonAdjoinedSixCell.triangleEightCell_leftNewNotOld
#print axioms PentagonAdjoinedSixCell.triangleEightCell_rightNewNotOld
#print axioms PentagonAdjoinedSixCell.triangleEightCell_noOldInterpreter
#print axioms PentagonAdjoinedSixCell.triangleEightCell_noStrictInterpreter
#print axioms PentagonAdjoinedSixCell.TriangleCriticalPeak
#print axioms PentagonAdjoinedSixCell.triangleCriticalPeak_fill
#print axioms PentagonAdjoinedSixCell.triangleCriticalPeak_joinable
#print axioms PentagonAdjoinedSixCell.triangleHistorySetoid
#print axioms PentagonAdjoinedSixCell.triangleHistoryClass
#print axioms PentagonAdjoinedSixCell.triangleHistoryClass_eq_iff
#print axioms PentagonAdjoinedSixCell.oldHistoryClass_descendsToTriangle
#print axioms PentagonAdjoinedSixCell.triangleHistoryClass_strictlyNew
#print axioms pentagonActualTriangle_newVsOldWithSourceObstruction

end ActualOriginalP77TriangleOverlap
end FivefoldP77FiniteRefinement
end
end KUOS.Architecture.WuxingPentagonUnified
