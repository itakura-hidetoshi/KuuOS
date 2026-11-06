import KUOS.Architecture.QiWuxingGK5CHP77EightCellLocalCoherenceV4_91

/-!
Qi v4.92 — CONSTRUCTIVE CRITICAL-PEAK PASTING AND EIGHT-CELL DESCENT.

Qi v4.91 freely generated a NEW EightCell Type indexed by complete,
unquotiented SevenRewrite proof histories. The v4.91 zigzag diamond
and interchange are explicit higher coherence generators; they do
NOT identify all parallel seventh-level histories.

This module does NOT adjoin any new eight-cell generator. It proves
new higher consequences of exactly the existing twenty-two rules:
(1) vertical pasting/naturality of local interchange;
(2) a recursively generated FAMILY OF LOCAL CRITICAL PEAKS, seeded
    ONLY by zigzag and independent-step interchange, and closed
    under certified source/target contexts and higher composition;
(3) EVERY member of that limited critical-peak family has an
    explicitly constructed EightCell witness, by induction;
(4) the eight-cell comparison relation is a Setoid on genuine
    seven-cell syntax, and its quotient agrees precisely with
    existence of an EightCell witness, not raw seven-cell equality;
(5) a real original P77 endpoint instance retains both higher
    quotient equality and original strict equality obstruction.

The local family is NOT the entirety of parallel SevenRewrite paths.
No unproved global seven-history coherence, nine-cell equality,
strict raw equality, or old GK5CG source descent is asserted.

Append-only/tighten-only/same-root; strict 空 center; independent
Kuu is presentation. Lean v4.30.0-rc2; pinned mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6;
public roots 107; protected #1558 stays Draft/open/unmerged.
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

/-- Eighth-level coherence pastes vertically along TWO actual
seventh-level histories, without identifying any raw proof term. -/
def eightCell_verticalPasting {w z : W}
    {c d e : PentagonAdjoinedSixCell W long short w z}
    {s s' : SevenRewrite W long short c d}
    {t t' : SevenRewrite W long short d e}
    (hs : EightCell W long short s s')
    (ht : EightCell W long short t t') :
    EightCell W long short (.trans s t) (.trans s' t') :=
  .chain (.whiskerRight hs t) (.whiskerLeft s' ht)

/-- The interchange of two independent seventh-level rewrites is
NATURAL under higher modifications of BOTH rewrites. It uses the
v4.91 interchange plus nontrivial vertical eight-cell pasting. -/
def eightCell_interchangeNaturality {w x z : W}
    {c c' : PentagonAdjoinedSixCell W long short w x}
    {d d' : PentagonAdjoinedSixCell W long short x z}
    {s s' : SevenRewrite W long short c c'}
    {t t' : SevenRewrite W long short d d'}
    (hs : EightCell W long short s s')
    (ht : EightCell W long short t t') :
    EightCell W long short
      (.trans (.congrComp s (.refl d))
        (.congrComp (.refl c') t))
      (.trans (.congrComp (.refl c) t')
        (.congrComp s' (.refl d'))) := by
  have hsL : EightCell W long short
      (.congrComp s (.refl d))
      (.congrComp s' (.refl d)) :=
    .compositeContext hs (.reflexive (.refl d))
  have htL : EightCell W long short
      (.congrComp (.refl c') t)
      (.congrComp (.refl c') t') :=
    .compositeContext (.reflexive (.refl c')) ht
  exact .chain (eightCell_verticalPasting hsL htL)
    (.interchange s' t')

/-- The same zigzag critical peak stays joinable when surrounded
by arbitrary composable seventh-level prefix/suffix histories. -/
def eightCell_zigzagWhiskered {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z)
    {a b : PentagonAdjoinedSixCell W long short w z}
    (before : SevenRewrite W long short a
      (.trans (.trans c (.symm c)) c))
    (after : SevenRewrite W long short c b) :
    EightCell W long short
      (.trans (.trans before (sevenRewrite_zigzagRight c)) after)
      (.trans (.trans before (sevenZigzagViaAssoc c)) after) :=
  .whiskerRight
    (.whiskerLeft before (eightZigzagCoherence c)) after

/-- The zigzag critical peak survives original six-cell inversion
context, still comparing raw seventh-level histories. -/
def eightCell_zigzagInverseContext {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    EightCell W long short
      (.congrInv (sevenRewrite_zigzagRight c))
      (.congrInv (sevenZigzagViaAssoc c)) :=
  .inverseContext (eightZigzagCoherence c)

/-- The zigzag critical peak survives composition on the right by
an arbitrary original six-cell word with matching endpoint. -/
def eightCell_zigzagRightContext {w x z : W}
    (c : PentagonAdjoinedSixCell W long short w x)
    (d : PentagonAdjoinedSixCell W long short x z) :
    EightCell W long short
      (.congrComp (sevenRewrite_zigzagRight c) (.refl d))
      (.congrComp (sevenZigzagViaAssoc c) (.refl d)) :=
  .compositeContext (eightZigzagCoherence c) (.reflexive (.refl d))

/-- The zigzag critical peak also survives composition on the left. -/
def eightCell_zigzagLeftContext {w x z : W}
    (d : PentagonAdjoinedSixCell W long short w x)
    (c : PentagonAdjoinedSixCell W long short x z) :
    EightCell W long short
      (.congrComp (.refl d) (sevenRewrite_zigzagRight c))
      (.congrComp (.refl d) (sevenZigzagViaAssoc c)) :=
  .compositeContext (.reflexive (.refl d)) (eightZigzagCoherence c)

/-- A finite, EXPLICITLY GENERATED family of seventh-level critical
peak comparisons. It has TWO primitive local peak shapes:
  * the three-factor cancellation/association zigzag,
  * the interchange of independent rewrite steps.
The remaining cases ONLY close those peaks under existing well-typed
proof contexts and composition; there is no arbitrary-parallel case.
This is a restricted family, NOT a classification of every possible
pair of seventh-level derivations. -/
inductive LocalCriticalPeak (W : Type uSix) (l r : W) :
    {w z : W} →
    {c d : PentagonAdjoinedSixCell W l r w z} →
    SevenRewrite W l r c d →
    SevenRewrite W l r c d → Type uSix where
  | zigzag {w z : W}
      (c : PentagonAdjoinedSixCell W l r w z) :
      LocalCriticalPeak W l r
        (sevenRewrite_zigzagRight c) (sevenZigzagViaAssoc c)
  | independent {w x z : W}
      {c c' : PentagonAdjoinedSixCell W l r w x}
      {d d' : PentagonAdjoinedSixCell W l r x z}
      (s : SevenRewrite W l r c c')
      (t : SevenRewrite W l r d d') :
      LocalCriticalPeak W l r
        (.trans (.congrComp s (.refl d))
          (.congrComp (.refl c') t))
        (.trans (.congrComp (.refl c) t)
          (.congrComp s (.refl d')))
  | reversed {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (p : LocalCriticalPeak W l r s t) :
      LocalCriticalPeak W l r t s
  | chained {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t u : SevenRewrite W l r c d}
      (p : LocalCriticalPeak W l r s t)
      (q : LocalCriticalPeak W l r t u) :
      LocalCriticalPeak W l r s u
  | leftWhiskered {w z : W}
      {c d e : PentagonAdjoinedSixCell W l r w z}
      (before : SevenRewrite W l r c d)
      {s t : SevenRewrite W l r d e}
      (p : LocalCriticalPeak W l r s t) :
      LocalCriticalPeak W l r (.trans before s) (.trans before t)
  | rightWhiskered {w z : W}
      {c d e : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (p : LocalCriticalPeak W l r s t)
      (after : SevenRewrite W l r d e) :
      LocalCriticalPeak W l r (.trans s after) (.trans t after)
  | inverseContext {w z : W}
      {c d : PentagonAdjoinedSixCell W l r w z}
      {s t : SevenRewrite W l r c d}
      (p : LocalCriticalPeak W l r s t) :
      LocalCriticalPeak W l r (.congrInv s) (.congrInv t)
  | compositeContext {w x z : W}
      {c c' : PentagonAdjoinedSixCell W l r w x}
      {d d' : PentagonAdjoinedSixCell W l r x z}
      {s s' : SevenRewrite W l r c c'}
      {t t' : SevenRewrite W l r d d'}
      (p : LocalCriticalPeak W l r s s')
      (q : LocalCriticalPeak W l r t t') :
      LocalCriticalPeak W l r
        (.congrComp s t) (.congrComp s' t')
  | verticalPasting {w z : W}
      {c d e : PentagonAdjoinedSixCell W l r w z}
      {s s' : SevenRewrite W l r c d}
      {t t' : SevenRewrite W l r d e}
      (p : LocalCriticalPeak W l r s s')
      (q : LocalCriticalPeak W l r t t') :
      LocalCriticalPeak W l r (.trans s t) (.trans s' t')

/-- A constructive and fully TYPE-INDEXED local peak completion
theorem. Every peak made from the two specifically listed families
and their allowed contexts can be joined by an ACTUAL EightCell,
by induction through the existing 22 v4.91 constructors. -/
def localCriticalPeak_eightCell {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (peak : LocalCriticalPeak W long short s t) :
    EightCell W long short s t := by
  induction peak with
  | zigzag c =>
      exact .zigzagDiamond c
  | independent s t =>
      exact .interchange s t
  | reversed p ih =>
      exact .reverse ih
  | chained p q ihp ihq =>
      exact .chain ihp ihq
  | leftWhiskered before p ih =>
      exact .whiskerLeft before ih
  | rightWhiskered p after ih =>
      exact .whiskerRight ih after
  | inverseContext p ih =>
      exact .inverseContext ih
  | compositeContext p q ihp ihq =>
      exact .compositeContext ihp ihq
  | verticalPasting p q ihp ihq =>
      exact eightCell_verticalPasting ihp ihq

/-- No EightCell is added by fiat for an arbitrary degree equality;
this theorem only certifies the newly DEFINED local critical peaks. -/
theorem localCriticalPeak_joinable {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (peak : LocalCriticalPeak W long short s t) :
    Nonempty (EightCell W long short s t) :=
  ⟨localCriticalPeak_eightCell peak⟩

/-- Eighth-cell existence is an equivalence relation on ACTUAL
seventh-level histories, although it is not their strict equality. -/
def eightHistorySetoid (W : Type uSix) (l r : W)
    {w z : W} {c d : PentagonAdjoinedSixCell W l r w z} :
    Setoid (SevenRewrite W l r c d) where
  r := fun s t => Nonempty (EightCell W l r s t)
  iseqv := by
    constructor
    · intro s
      exact ⟨.reflexive s⟩
    · intro s t h
      rcases h with ⟨h⟩
      exact ⟨.reverse h⟩
    · intro s t u hs ht
      rcases hs with ⟨hs⟩
      rcases ht with ⟨ht⟩
      exact ⟨.chain hs ht⟩

/-- Chosen eighth-level quotient of ACTUAL seventh-level proof words;
the quotient is not imposed on the original SevenRewrite Type. -/
def eightHistoryClass {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s : SevenRewrite W long short c d) :
    Quotient (eightHistorySetoid W long short (c := c) (d := d)) :=
  Quotient.mk _ s

/-- Exact correspondence of the NEW history quotient and actual
eight-cell witnesses. This does not assert raw seven-cell equality. -/
theorem eightHistoryClass_eq_iff {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (s t : SevenRewrite W long short c d) :
    eightHistoryClass s = eightHistoryClass t ↔
      Nonempty (EightCell W long short s t) := by
  constructor
  · intro h
    exact Quotient.exact h
  · intro h
    exact Quotient.sound h

/-- The v4.91 zigzag diamond becomes equal in the CHOSEN new
eighth-level history quotient, not in the raw SevenRewrite Type. -/
theorem eightHistoryClass_zigzag {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    eightHistoryClass (sevenRewrite_zigzagRight c) =
      eightHistoryClass (sevenZigzagViaAssoc c) :=
  (eightHistoryClass_eq_iff _ _).2 ⟨eightZigzagCoherence c⟩

/-- Strong distinction: two strictly different SEVEN-cell proofs
represent the same NEW eighth-level quotient class. -/
theorem eightHistoryClass_zigzag_notStrict {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    (eightHistoryClass (sevenRewrite_zigzagRight c) =
      eightHistoryClass (sevenZigzagViaAssoc c)) ∧
    sevenRewrite_zigzagRight c ≠ sevenZigzagViaAssoc c :=
  ⟨eightHistoryClass_zigzag c,
    sevenZigzag_twoHistories_notStrict c⟩

/-- The verified local peak family also descends to the new chosen
history quotient, using actual higher witnesses, NOT degree equality. -/
theorem localCriticalPeak_classEq {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    {s t : SevenRewrite W long short c d}
    (peak : LocalCriticalPeak W long short s t) :
    eightHistoryClass s = eightHistoryClass t :=
  (eightHistoryClass_eq_iff _ _).2 (localCriticalPeak_joinable peak)

/-- Equality of new eighth-level history classes cannot be read
back as strict equality of original seventh-level derivations. -/
theorem eightHistoryClass_noStrictReturn (l r : W) :
    ¬ (∀ {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
      (s t : SevenRewrite W l r c d),
      eightHistoryClass s = eightHistoryClass t → s = t) := by
  intro interpret
  apply eightCell_noStrictSevenInterpreter l r
  intro w z c d s t h
  exact interpret s t ((eightHistoryClass_eq_iff s t).2 ⟨h⟩)

end PentagonAdjoinedSixCell

section ActualOriginalP77EightHistoryQuotient
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

/-- The actual P77 pentagon index retains STRICTLY DIFFERENT
seven-cell zigzag histories, although they represent the same
NEW eighth-level quotient class. -/
theorem pentagonActualEightHistory_zigzagQuotientNotStrict
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄)) :
    (PentagonAdjoinedSixCell.eightHistoryClass
      (pentagonActualSevenRewrite_zigzag f g h k A B C D₄ i) =
     PentagonAdjoinedSixCell.eightHistoryClass
      (PentagonAdjoinedSixCell.sevenZigzagViaAssoc
        (pentagonAdjoinedSixCell_generator f g h k A B C D₄ i))) ∧
    pentagonActualSevenRewrite_zigzag f g h k A B C D₄ i ≠
      PentagonAdjoinedSixCell.sevenZigzagViaAssoc
        (pentagonAdjoinedSixCell_generator f g h k A B C D₄ i) :=
  PentagonAdjoinedSixCell.eightHistoryClass_zigzag_notStrict
    (pentagonAdjoinedSixCell_generator f g h k A B C D₄ i)

/-- The chosen higher quotient and local peak certificates are
separate from the ORIGINAL GK5CG five-cell equality obstruction. -/
theorem pentagonActualEightHistory_withSourceObstruction
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄)) :
    (PentagonAdjoinedSixCell.eightHistoryClass
      (pentagonActualSevenRewrite_zigzag f g h k A B C D₄ i) =
     PentagonAdjoinedSixCell.eightHistoryClass
      (PentagonAdjoinedSixCell.sevenZigzagViaAssoc
        (pentagonAdjoinedSixCell_generator f g h k A B C D₄ i))) ∧
    ¬ PentagonAdjoinedSixCellEqualityInterpreter f g h k A B C D₄ i :=
  ⟨(pentagonActualEightHistory_zigzagQuotientNotStrict
      f g h k A B C D₄ i).1,
    pentagonAdjoinedSixCell_noEqualityInterpreter f g h k A B C D₄ i⟩

#print axioms PentagonAdjoinedSixCell.eightCell_verticalPasting
#print axioms PentagonAdjoinedSixCell.eightCell_interchangeNaturality
#print axioms PentagonAdjoinedSixCell.eightCell_zigzagWhiskered
#print axioms PentagonAdjoinedSixCell.eightCell_zigzagInverseContext
#print axioms PentagonAdjoinedSixCell.eightCell_zigzagRightContext
#print axioms PentagonAdjoinedSixCell.eightCell_zigzagLeftContext
#print axioms PentagonAdjoinedSixCell.LocalCriticalPeak
#print axioms PentagonAdjoinedSixCell.localCriticalPeak_eightCell
#print axioms PentagonAdjoinedSixCell.localCriticalPeak_joinable
#print axioms PentagonAdjoinedSixCell.eightHistorySetoid
#print axioms PentagonAdjoinedSixCell.eightHistoryClass
#print axioms PentagonAdjoinedSixCell.eightHistoryClass_eq_iff
#print axioms PentagonAdjoinedSixCell.eightHistoryClass_zigzag
#print axioms PentagonAdjoinedSixCell.eightHistoryClass_zigzag_notStrict
#print axioms PentagonAdjoinedSixCell.localCriticalPeak_classEq
#print axioms PentagonAdjoinedSixCell.eightHistoryClass_noStrictReturn
#print axioms pentagonActualEightHistory_zigzagQuotientNotStrict
#print axioms pentagonActualEightHistory_withSourceObstruction

end ActualOriginalP77EightHistoryQuotient
end FivefoldP77FiniteRefinement
end
end KUOS.Architecture.WuxingPentagonUnified
