import KUOS.Architecture.QiWuxingGK5CHP77IdentityBalanceHiddenCriticalPeaksV4_97

/-!
Qi v4.98 — IDENTITY / DOUBLE-INVERSE LOCAL HIGHER COMPLETION.

The actual v4.97 R-obstruction is resolved by ONE new primitive
higher comparison:
  doubleInverse(refl(w))  <==>  inverseId(w); inverseId(w).
It is added only to a SEPARATE IdentityEightCell presentation;
the old original, triangle, involution, and inverseComp eighth
presentations remain completely unchanged.

The new grammar has typed equivalence closure, whiskering,
inverse and composite contexts. The chosen restricted critical
family has a constructive filler for EVERY constructor.
Its quotient is strictly coarser than the v4.95 final quotient,
with explicit old R=0 versus R=2 witnesses. Therefore R does NOT
descend to the new quotient, even though it is conserved by ALL
comparisons of the old v4.95 grammar.

Most importantly the v4.97 HIDDEN three-charge-invisible composite
pair is now filled by explicit typed compositeContext of exactly
three existing/new comparison witnesses, without declaring it equal
as raw seven-cell syntax. The genuine GK5CG original P77 source and
its strict equality-interpreter no-go are preserved.

No unrestricted thinness, all-parallel seventh history comparison,
source equality, or ninth-cell constructor is postulated.
Append-only / tighten-only / same-root / root107 unchanged.
Pinned Lean v4.30.0-rc2 and mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
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

/-- The actual primitive double-inverse/identity critical pair:
old v4.95 R is zero on one path and two on the other. -/
theorem sevenIdentityDouble_balanceGap (w : W) :
    sevenIdentityBalance
      (sevenIdentityDoubleDirect (long := long) (short := short) w) = 0 ∧
    sevenIdentityBalance
      (sevenIdentityDoubleVia (long := long) (short := short) w) = 2 := by
  constructor <;>
    norm_num [sevenIdentityDoubleDirect, sevenIdentityDoubleVia,
      sevenIdentityBalance]

/-- No comparison exists between these two actually typed
old seven-cell histories in the COMPLETE v4.95 comparison grammar. -/
theorem sevenIdentityDouble_noPrevious (w : W) :
    ¬ Nonempty (InverseCompEightCell W long short
      (sevenIdentityDoubleDirect (long := long) (short := short) w)
      (sevenIdentityDoubleVia (long := long) (short := short) w)) := by
  rintro ⟨q⟩
  have hb := inverseCompEightCell_preservesIdentityBalance q
  have hv := sevenIdentityDouble_balanceGap (long := long) (short := short) w
  rw [hv.1, hv.2] at hb
  norm_num at hb

/-- One new and separate higher presentation. Exactly one primitive
identity/doubleInverse constructor is adjoined, plus the same typed
equivalence/congruence closure as in v4.95. No old constructor is
replaced or quotiented at source. -/
inductive IdentityEightCell (W : Type uSix) (l r : W) :
    {w z : W} →
    {c d : PentagonAdjoinedSixCell W l r w z} →
    SevenRewrite W l r c d →
    SevenRewrite W l r c d → Type uSix where
  | previous {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (q : InverseCompEightCell W l r s t) :
      IdentityEightCell W l r s t
  | identityDouble (w : W) :
      IdentityEightCell W l r
        (sevenIdentityDoubleDirect (long := l) (short := r) w)
        (sevenIdentityDoubleVia (long := l) (short := r) w)
  | reverse {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (q : IdentityEightCell W l r s t) :
      IdentityEightCell W l r t s
  | chain {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
      {s t u : SevenRewrite W l r c d}
      (q : IdentityEightCell W l r s t)
      (q' : IdentityEightCell W l r t u) :
      IdentityEightCell W l r s u
  | whiskerLeft {w z : W}
      {c d e : PentagonAdjoinedSixCell W l r w z}
      (before : SevenRewrite W l r c d)
      {s t : SevenRewrite W l r d e}
      (q : IdentityEightCell W l r s t) :
      IdentityEightCell W l r (.trans before s) (.trans before t)
  | whiskerRight {w z : W}
      {c d e : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (q : IdentityEightCell W l r s t)
      (after : SevenRewrite W l r d e) :
      IdentityEightCell W l r (.trans s after) (.trans t after)
  | inverseContext {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (q : IdentityEightCell W l r s t) :
      IdentityEightCell W l r (.congrInv s) (.congrInv t)
  | compositeContext {w x z : W}
      {c c' : PentagonAdjoinedSixCell W l r w x}
      {d d' : PentagonAdjoinedSixCell W l r x z}
      {s s' : SevenRewrite W l r c c'}
      {t t' : SevenRewrite W l r d d'}
      (q : IdentityEightCell W l r s s')
      (q' : IdentityEightCell W l r t t') :
      IdentityEightCell W l r
        (.congrComp s t) (.congrComp s' t')

/-- Every v4.95 comparison survives in the new independent grammar. -/
def identityEightCell_ofPrevious {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (q : InverseCompEightCell W long short s t) :
    IdentityEightCell W long short s t :=
  .previous q

/-- Exactly one new primitive peak has a higher comparison in
the new presentation, and provably no comparison in the old one. -/
theorem identityEightCell_strictlyNew (w : W) :
    Nonempty (IdentityEightCell W long short
      (sevenIdentityDoubleDirect (long := long) (short := short) w)
      (sevenIdentityDoubleVia (long := long) (short := short) w)) ∧
    ¬ Nonempty (InverseCompEightCell W long short
      (sevenIdentityDoubleDirect (long := long) (short := short) w)
      (sevenIdentityDoubleVia (long := long) (short := short) w)) :=
  ⟨⟨.identityDouble w⟩,
    sevenIdentityDouble_noPrevious (long := long) (short := short) w⟩

/-- There can be no universal interpreter sending ALL the new
eighth-cell proof values back into the old eighth presentation. -/
theorem identityEightCell_noPreviousInterpreter (l r : W) :
    ¬ Nonempty (∀ {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      (s t : SevenRewrite W l r c d),
      IdentityEightCell W l r s t →
        InverseCompEightCell W l r s t) := by
  rintro ⟨interpret⟩
  have q : InverseCompEightCell W l r
      (sevenIdentityDoubleDirect (long := l) (short := r) l)
      (sevenIdentityDoubleVia (long := l) (short := r) l) :=
    interpret _ _ (.identityDouble l)
  exact sevenIdentityDouble_noPrevious (long := l) (short := r) l ⟨q⟩

/-- The new comparison does not become raw strict equality of the
unchanged seventh-level proof history syntax. -/
theorem identityEightCell_noStrictInterpreter (l r : W) :
    ¬ (∀ {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
      (s t : SevenRewrite W l r c d),
      IdentityEightCell W l r s t → s = t) := by
  intro interpret
  apply inverseCompEightCell_noStrictInterpreter l r
  intro w z c d s t q
  exact interpret s t (.previous q)

/-- The entire three-factor v4.97 HIDDEN critical pair can now be
filled, not by a new ad-hoc constructor, but by the one new primitive
identityDouble, an OLD involution overlap, and an OLD triangle
overlap, all pasted using the existing typed composite context. -/
def identityHiddenCritical_fill (w : W) :
    IdentityEightCell W long short
      (sevenHiddenCriticalFirst (long := long) (short := short) w)
      (sevenHiddenCriticalSecond (long := long) (short := short) w) :=
  .compositeContext
    (.compositeContext
      (.identityDouble w)
      (.previous (.previous (.leftOverlap (.refl w)))))
    (.previous (.previous (.previous
      (.reverse (.leftTriangle (.refl w) (.refl w))))))

/-- The hidden composite has become joinable in the NEW independent
eight-cell grammar, although it was a certified v4.95 obstruction. -/
theorem identityHiddenCritical_newVsOld (w : W) :
    Nonempty (IdentityEightCell W long short
      (sevenHiddenCriticalFirst (long := long) (short := short) w)
      (sevenHiddenCriticalSecond (long := long) (short := short) w)) ∧
    ¬ Nonempty (InverseCompEightCell W long short
      (sevenHiddenCriticalFirst (long := long) (short := short) w)
      (sevenHiddenCriticalSecond (long := long) (short := short) w)) :=
  ⟨⟨identityHiddenCritical_fill (long := long) (short := short) w⟩,
    sevenHiddenCritical_noComparison (long := long) (short := short) w⟩

/-- Selected recursively generated local critical peaks:
all old v4.95 peaks, one genuine new generator, the now-filled
composite hidden overlap, and their listed typed contexts.
Not a claim of universal all-parallel critical-peak completeness. -/
inductive IdentityCriticalPeak (W : Type uSix) (l r : W) :
    {w z : W} →
    {c d : PentagonAdjoinedSixCell W l r w z} →
    SevenRewrite W l r c d →
    SevenRewrite W l r c d → Type uSix where
  | previous {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (q : InverseCompCriticalPeak W l r s t) :
      IdentityCriticalPeak W l r s t
  | identityDouble (w : W) :
      IdentityCriticalPeak W l r
        (sevenIdentityDoubleDirect (long := l) (short := r) w)
        (sevenIdentityDoubleVia (long := l) (short := r) w)
  | hiddenComposite (w : W) :
      IdentityCriticalPeak W l r
        (sevenHiddenCriticalFirst (long := l) (short := r) w)
        (sevenHiddenCriticalSecond (long := l) (short := r) w)
  | reverse {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (q : IdentityCriticalPeak W l r s t) :
      IdentityCriticalPeak W l r t s
  | chain {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
      {s t u : SevenRewrite W l r c d}
      (q : IdentityCriticalPeak W l r s t)
      (q' : IdentityCriticalPeak W l r t u) :
      IdentityCriticalPeak W l r s u
  | whiskerLeft {w z : W}
      {c d e : PentagonAdjoinedSixCell W l r w z}
      (before : SevenRewrite W l r c d)
      {s t : SevenRewrite W l r d e}
      (q : IdentityCriticalPeak W l r s t) :
      IdentityCriticalPeak W l r (.trans before s) (.trans before t)
  | whiskerRight {w z : W}
      {c d e : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (q : IdentityCriticalPeak W l r s t)
      (after : SevenRewrite W l r d e) :
      IdentityCriticalPeak W l r (.trans s after) (.trans t after)
  | inverseContext {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (q : IdentityCriticalPeak W l r s t) :
      IdentityCriticalPeak W l r (.congrInv s) (.congrInv t)
  | compositeContext {w x z : W}
      {c c' : PentagonAdjoinedSixCell W l r w x}
      {d d' : PentagonAdjoinedSixCell W l r x z}
      {s s' : SevenRewrite W l r c c'}
      {t t' : SevenRewrite W l r d d'}
      (q : IdentityCriticalPeak W l r s s')
      (q' : IdentityCriticalPeak W l r t t') :
      IdentityCriticalPeak W l r
        (.congrComp s t) (.congrComp s' t')

/-- Constructive, type-indexed induction: EVERY selected critical
peak has an actual new eighth-cell Type-valued filler. -/
def identityCriticalPeak_fill {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (p : IdentityCriticalPeak W long short s t) :
    IdentityEightCell W long short s t := by
  induction p with
  | previous p => exact .previous (inverseCompCriticalPeak_fill p)
  | identityDouble w => exact .identityDouble w
  | hiddenComposite w => exact identityHiddenCritical_fill w
  | reverse p ih => exact .reverse ih
  | chain p q ihp ihq => exact .chain ihp ihq
  | whiskerLeft before p ih => exact .whiskerLeft before ih
  | whiskerRight p after ih => exact .whiskerRight ih after
  | inverseContext p ih => exact .inverseContext ih
  | compositeContext p q ihp ihq => exact .compositeContext ihp ihq

theorem identityCriticalPeak_joinable {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (p : IdentityCriticalPeak W long short s t) :
    Nonempty (IdentityEightCell W long short s t) :=
  ⟨identityCriticalPeak_fill p⟩

/-- New chosen higher-history quotient; raw seven-cell evidence,
old eighth-cell presentations and all prior quotients stay intact. -/
def identityHistorySetoid (W : Type uSix) (l r : W)
    {w z : W} {c d : PentagonAdjoinedSixCell W l r w z} :
    Setoid (SevenRewrite W l r c d) where
  r := fun s t => Nonempty (IdentityEightCell W l r s t)
  iseqv := by
    constructor
    · intro s
      exact ⟨.previous (.previous (.previous (.original (.reflexive s))))⟩
    · intro s t h
      rcases h with ⟨q⟩
      exact ⟨.reverse q⟩
    · intro s t u hs ht
      rcases hs with ⟨hs⟩
      rcases ht with ⟨ht⟩
      exact ⟨.chain hs ht⟩

def identityHistoryClass {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s : SevenRewrite W long short c d) :
    Quotient (identityHistorySetoid W long short (c := c) (d := d)) :=
  Quotient.mk _ s

theorem identityHistoryClass_eq_iff {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s t : SevenRewrite W long short c d) :
    identityHistoryClass s = identityHistoryClass t ↔
      Nonempty (IdentityEightCell W long short s t) := by
  constructor
  · intro h
    exact Quotient.exact h
  · intro h
    exact Quotient.sound h

/-- All v4.95 higher classes descend to the new chosen quotient. -/
theorem inverseCompHistoryClass_descendsToIdentity {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s t : SevenRewrite W long short c d)
    (h : inverseCompHistoryClass s = inverseCompHistoryClass t) :
    identityHistoryClass s = identityHistoryClass t := by
  rcases (inverseCompHistoryClass_eq_iff s t).1 h with ⟨q⟩
  exact (identityHistoryClass_eq_iff s t).2 ⟨.previous q⟩

/-- The new quotient is STRICTLY coarser: one genuine new peak
becomes equal only after the new eighth comparison is added. -/
theorem identityHistoryClass_strictlyNew (w : W) :
    (identityHistoryClass
        (sevenIdentityDoubleDirect (long := long) (short := short) w) =
      identityHistoryClass
        (sevenIdentityDoubleVia (long := long) (short := short) w)) ∧
    (inverseCompHistoryClass
        (sevenIdentityDoubleDirect (long := long) (short := short) w) ≠
      inverseCompHistoryClass
        (sevenIdentityDoubleVia (long := long) (short := short) w)) := by
  constructor
  · exact (identityHistoryClass_eq_iff _ _).2 ⟨.identityDouble w⟩
  · intro h
    exact sevenIdentityDouble_noPrevious (long := long) (short := short) w
      ((inverseCompHistoryClass_eq_iff _ _).1 h)

/-- The ORIGINAL three-charge-invisible composite pair is an
independent second strictness witness at the quotient-class level. -/
theorem identityHiddenCritical_strictlyNew (w : W) :
    (identityHistoryClass
        (sevenHiddenCriticalFirst (long := long) (short := short) w) =
      identityHistoryClass
        (sevenHiddenCriticalSecond (long := long) (short := short) w)) ∧
    (inverseCompHistoryClass
        (sevenHiddenCriticalFirst (long := long) (short := short) w) ≠
      inverseCompHistoryClass
        (sevenHiddenCriticalSecond (long := long) (short := short) w)) := by
  constructor
  · exact (identityHistoryClass_eq_iff _ _).2
      ⟨identityHiddenCritical_fill (long := long) (short := short) w⟩
  · exact sevenHiddenCritical_distinctClasses (long := long) (short := short) w

theorem identityCriticalPeak_classEq {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (p : IdentityCriticalPeak W long short s t) :
    identityHistoryClass s = identityHistoryClass t :=
  (identityHistoryClass_eq_iff _ _).2
    (identityCriticalPeak_joinable p)

/-- The fourth integer observation is NOT well-defined on the new
quotient, although it WAS well-defined on all v4.95 classes.
This is a proved failure of descent, not a new axiom. -/
theorem identityHistoryClass_noBalanceDescent (l r : W) :
    ¬ (∀ {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      (s t : SevenRewrite W l r c d),
      identityHistoryClass s = identityHistoryClass t →
        sevenIdentityBalance s = sevenIdentityBalance t) := by
  intro preserve
  have heq := (identityHistoryClass_strictlyNew
    (long := l) (short := r) l).1
  have h := preserve
    (sevenIdentityDoubleDirect (long := l) (short := r) l)
    (sevenIdentityDoubleVia (long := l) (short := r) l) heq
  have vals := sevenIdentityDouble_balanceGap (long := l) (short := r) l
  rw [vals.1, vals.2] at h
  norm_num at h

/-- New quotient equality cannot be reinterpreted universally as
OLD v4.95 quotient equality. -/
theorem identityHistoryClass_noPreviousReturn (l r : W) :
    ¬ (∀ {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      (s t : SevenRewrite W l r c d),
      identityHistoryClass s = identityHistoryClass t →
        inverseCompHistoryClass s = inverseCompHistoryClass t) := by
  intro interpret
  have witness := (identityHistoryClass_strictlyNew
    (long := l) (short := r) l)
  exact witness.2 (interpret
    (sevenIdentityDoubleDirect (long := l) (short := r) l)
    (sevenIdentityDoubleVia (long := l) (short := r) l) witness.1)

/-- No collapse of chosen eighth-history classes into original raw
seventh syntax is implied by this new local completion. -/
theorem identityHistoryClass_noStrictReturn (l r : W) :
    ¬ (∀ {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
      (s t : SevenRewrite W l r c d),
      identityHistoryClass s = identityHistoryClass t → s = t) := by
  intro interpret
  apply identityEightCell_noStrictInterpreter l r
  intro w z c d s t q
  exact interpret s t ((identityHistoryClass_eq_iff s t).2 ⟨q⟩)

end PentagonAdjoinedSixCell

section ActualOriginalP77IdentityDoubleLocalCompletion
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

/-- At EVERY genuine original P77 terminal raw index, the three-charge
invisible v4.97 composite becomes joinable in the new v4.98 chosen
presentation, was not joinable in the old v4.95 presentation, and
the original GK5CG five-cell strict-equality interpretation remains
impossible. No extra source witness or axiom is introduced. -/
theorem pentagonActualHiddenCriticalCompletionWithSourceObstruction
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄)) :
    Nonempty (PentagonAdjoinedSixCell.IdentityEightCell
      (pentagonFinalConservativeLoop f g h k i)
      (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
      (pentagonShortConservativeFiveCell f g h k A B C D₄ i)
      (PentagonAdjoinedSixCell.sevenHiddenCriticalFirst
        (long := pentagonLongConservativeFiveCell f g h k A B C D₄ i)
        (short := pentagonShortConservativeFiveCell f g h k A B C D₄ i)
        (pentagonLongConservativeFiveCell f g h k A B C D₄ i))
      (PentagonAdjoinedSixCell.sevenHiddenCriticalSecond
        (long := pentagonLongConservativeFiveCell f g h k A B C D₄ i)
        (short := pentagonShortConservativeFiveCell f g h k A B C D₄ i)
        (pentagonLongConservativeFiveCell f g h k A B C D₄ i))) ∧
    ¬ Nonempty (PentagonAdjoinedSixCell.InverseCompEightCell
      (pentagonFinalConservativeLoop f g h k i)
      (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
      (pentagonShortConservativeFiveCell f g h k A B C D₄ i)
      (PentagonAdjoinedSixCell.sevenHiddenCriticalFirst
        (long := pentagonLongConservativeFiveCell f g h k A B C D₄ i)
        (short := pentagonShortConservativeFiveCell f g h k A B C D₄ i)
        (pentagonLongConservativeFiveCell f g h k A B C D₄ i))
      (PentagonAdjoinedSixCell.sevenHiddenCriticalSecond
        (long := pentagonLongConservativeFiveCell f g h k A B C D₄ i)
        (short := pentagonShortConservativeFiveCell f g h k A B C D₄ i)
        (pentagonLongConservativeFiveCell f g h k A B C D₄ i))) ∧
    ¬ PentagonAdjoinedSixCellEqualityInterpreter f g h k A B C D₄ i := by
  exact ⟨⟨PentagonAdjoinedSixCell.identityHiddenCritical_fill
      (long := pentagonLongConservativeFiveCell f g h k A B C D₄ i)
      (short := pentagonShortConservativeFiveCell f g h k A B C D₄ i)
      (pentagonLongConservativeFiveCell f g h k A B C D₄ i)⟩,
    PentagonAdjoinedSixCell.sevenHiddenCritical_noComparison
      (long := pentagonLongConservativeFiveCell f g h k A B C D₄ i)
      (short := pentagonShortConservativeFiveCell f g h k A B C D₄ i)
      (pentagonLongConservativeFiveCell f g h k A B C D₄ i),
    pentagonAdjoinedSixCell_noEqualityInterpreter f g h k A B C D₄ i⟩

#print axioms PentagonAdjoinedSixCell.sevenIdentityDouble_balanceGap
#print axioms PentagonAdjoinedSixCell.sevenIdentityDouble_noPrevious
#print axioms PentagonAdjoinedSixCell.IdentityEightCell
#print axioms PentagonAdjoinedSixCell.identityEightCell_ofPrevious
#print axioms PentagonAdjoinedSixCell.identityEightCell_strictlyNew
#print axioms PentagonAdjoinedSixCell.identityEightCell_noPreviousInterpreter
#print axioms PentagonAdjoinedSixCell.identityEightCell_noStrictInterpreter
#print axioms PentagonAdjoinedSixCell.identityHiddenCritical_fill
#print axioms PentagonAdjoinedSixCell.identityHiddenCritical_newVsOld
#print axioms PentagonAdjoinedSixCell.IdentityCriticalPeak
#print axioms PentagonAdjoinedSixCell.identityCriticalPeak_fill
#print axioms PentagonAdjoinedSixCell.identityCriticalPeak_joinable
#print axioms PentagonAdjoinedSixCell.identityHistorySetoid
#print axioms PentagonAdjoinedSixCell.identityHistoryClass
#print axioms PentagonAdjoinedSixCell.identityHistoryClass_eq_iff
#print axioms PentagonAdjoinedSixCell.inverseCompHistoryClass_descendsToIdentity
#print axioms PentagonAdjoinedSixCell.identityHistoryClass_strictlyNew
#print axioms PentagonAdjoinedSixCell.identityHiddenCritical_strictlyNew
#print axioms PentagonAdjoinedSixCell.identityCriticalPeak_classEq
#print axioms PentagonAdjoinedSixCell.identityHistoryClass_noBalanceDescent
#print axioms PentagonAdjoinedSixCell.identityHistoryClass_noPreviousReturn
#print axioms PentagonAdjoinedSixCell.identityHistoryClass_noStrictReturn
#print axioms pentagonActualHiddenCriticalCompletionWithSourceObstruction

end ActualOriginalP77IdentityDoubleLocalCompletion
end FivefoldP77FiniteRefinement
end
end KUOS.Architecture.WuxingPentagonUnified
