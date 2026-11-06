import KUOS.Architecture.QiWuxingGK5CHP77SixCellEndpointNormalFormsV4_88

/-!
Qi v4.89 — HISTORY-PRESERVING TYPE-VALUED SEVEN-CELL REWRITES.

Qi v4.87/4.88 intentionally identify parallel SIX-cell raw proof words
only after a chosen degree quotient. The present file adds a SEPARATE
Type-valued, explicitly generated SEVENTH-dimensional rewrite grammar
whose indices preserve BOTH full original six-cell raw proof words.
Its constructors record structural rewrite history: reflexivity,
reversal, chaining, inverse/composition context, units, associativity,
cancellation, involution and inverse-of-composite.

Every such rewrite is proved signed-degree sound and therefore
induces equality in the NEW quotient, but NOT strict raw-word equality.
Crucially, generic degree equality does not silently generate a
seven-cell rewrite: completeness of the local rewrite grammar is NOT
asserted. An explicit winding obstruction remains when long=short.

Original GK5CG conservative five-cell values remain endpoints of the
separately adjoined new six-cells; no old F55/P77/GK5CG six- or
seven-cell source constructor is claimed. Genuine P77 all-index
roundtrip and zigzag witnesses are built without changing old source.

Append-only/tighten-only/same-root; strict 空 center; independent Kuu
is presentation. Fixed Lean v4.30.0-rc2; mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6;
public roots107; protected validation-only PR #1558 Draft/unmerged.
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

/-- A separate, freely GENERATED seventh-level proof-of-rewrite Type.
Indices are the full, UNQUOTIENTED source/target six-cell words.
Only explicitly listed local coherence rules create history. -/
inductive SevenRewrite (W : Type uSix) (l r : W) :
    {w z : W} →
    PentagonAdjoinedSixCell W l r w z →
    PentagonAdjoinedSixCell W l r w z → Type uSix where
  | refl {w z : W} (c : PentagonAdjoinedSixCell W l r w z) :
      SevenRewrite W l r c c
  | symm {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
      (e : SevenRewrite W l r c d) :
      SevenRewrite W l r d c
  | trans {w z : W} {c d e : PentagonAdjoinedSixCell W l r w z}
      (s : SevenRewrite W l r c d) (t : SevenRewrite W l r d e) :
      SevenRewrite W l r c e
  | congrInv {w z : W} {c d : PentagonAdjoinedSixCell W l r w z}
      (e : SevenRewrite W l r c d) :
      SevenRewrite W l r (.symm c) (.symm d)
  | congrComp {w x z : W}
      {c c' : PentagonAdjoinedSixCell W l r w x}
      {d d' : PentagonAdjoinedSixCell W l r x z}
      (s : SevenRewrite W l r c c')
      (t : SevenRewrite W l r d d') :
      SevenRewrite W l r (.trans c d) (.trans c' d')
  | leftUnit {w z : W} (c : PentagonAdjoinedSixCell W l r w z) :
      SevenRewrite W l r (.trans (.refl w) c) c
  | rightUnit {w z : W} (c : PentagonAdjoinedSixCell W l r w z) :
      SevenRewrite W l r (.trans c (.refl z)) c
  | assoc {w x y z : W}
      (c : PentagonAdjoinedSixCell W l r w x)
      (d : PentagonAdjoinedSixCell W l r x y)
      (e : PentagonAdjoinedSixCell W l r y z) :
      SevenRewrite W l r (.trans (.trans c d) e)
        (.trans c (.trans d e))
  | inverseRight {w z : W}
      (c : PentagonAdjoinedSixCell W l r w z) :
      SevenRewrite W l r (.trans c (.symm c)) (.refl w)
  | inverseLeft {w z : W}
      (c : PentagonAdjoinedSixCell W l r w z) :
      SevenRewrite W l r (.trans (.symm c) c) (.refl z)
  | doubleInverse {w z : W}
      (c : PentagonAdjoinedSixCell W l r w z) :
      SevenRewrite W l r (.symm (.symm c)) c
  | inverseId (w : W) :
      SevenRewrite W l r (.symm (.refl w)) (.refl w)
  | inverseComp {w x z : W}
      (c : PentagonAdjoinedSixCell W l r w x)
      (d : PentagonAdjoinedSixCell W l r x z) :
      SevenRewrite W l r (.symm (.trans c d))
        (.trans (.symm d) (.symm c))

/-- Explicit original-word equality embeds in new rewrite evidence.
The converse is false and is disproved below. -/
def sevenRewrite_ofEq {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (eq : c = d) : SevenRewrite W long short c d := by
  cases eq
  exact .refl c

/-- Every history-carrying new seventh-level witness preserves signed
degree; this is proved by induction over ALL constructors, not assumed. -/
theorem sevenRewrite_degreeSound {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (e : SevenRewrite W long short c d) :
    degree c = degree d := by
  induction e with
  | refl c => rfl
  | symm e ih => exact ih.symm
  | trans s t ihs iht => exact ihs.trans iht
  | congrInv e ih =>
      change -(degree _) = -(degree _)
      exact congrArg (fun t : ℤ => -t) ih
  | congrComp s t ihs iht =>
      change degree _ + degree _ = degree _ + degree _
      exact congrArg₂ (· + ·) ihs iht
  | leftUnit c =>
      change (0 : ℤ) + degree c = degree c
      exact zero_add _
  | rightUnit c =>
      change degree c + (0 : ℤ) = degree c
      exact add_zero _
  | assoc c d e =>
      change (degree c + degree d) + degree e =
        degree c + (degree d + degree e)
      exact add_assoc _ _ _
  | inverseRight c =>
      change degree c + -(degree c) = (0 : ℤ)
      exact add_neg_cancel _
  | inverseLeft c =>
      change -(degree c) + degree c = (0 : ℤ)
      exact neg_add_cancel _
  | doubleInverse c =>
      change -(-(degree c)) = degree c
      exact neg_neg _
  | inverseId w =>
      simp [degree]
  | inverseComp c d =>
      change -(degree c + degree d) =
        -(degree d) + -(degree c)
      abel

/-- Forgetting the explicit rewrite history produces a degree equality,
hence equality ONLY IN the chosen v4.87 quotient, not in raw syntax. -/
theorem sevenRewrite_quotientSound {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (e : SevenRewrite W long short c d) :
    homMk c = homMk d :=
  Quot.sound (sevenRewrite_degreeSound e)

/-- The opposite implication (same quotient class implies an explicit
local rewrite history) is NOT claimed in this version. -/
theorem sevenRewrite_degreeObstruction {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (hNe : degree c ≠ degree d) :
    ¬ Nonempty (SevenRewrite W long short c d) := by
  rintro ⟨e⟩
  exact hNe (sevenRewrite_degreeSound e)

/-- When BOTH designated endpoints coincide, pentagon can wind as a
nonzero-degree loop; there is NO degree-sound seventh-level rewrite
from that generator to the zero-degree raw identity. -/
theorem selfPentagonLoop_noSevenRewrite (w : W) :
    ¬ Nonempty
      (SevenRewrite W w w
        (.pentagon : PentagonAdjoinedSixCell W w w w w)
        (.refl w)) := by
  rintro ⟨e⟩
  have hdeg := sevenRewrite_degreeSound e
  change (1 : ℤ) = 0 at hdeg
  norm_num at hdeg

/-- A constructive zigzag witness made ONLY from elementary
SEVENTH-level congruence + inverse cancellation + left unit. -/
def sevenRewrite_zigzagRight {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    SevenRewrite W long short
      (.trans (.trans c (.symm c)) c) c :=
  .trans
    (.congrComp (.inverseRight c) (.refl c))
    (.leftUnit c)

/-- The other zigzag; the original raw six-cell construction remains
visible at each indexed position in the nested proof. -/
def sevenRewrite_zigzagLeft {w z : W}
    (c : PentagonAdjoinedSixCell W long short w z) :
    SevenRewrite W long short
      (.trans (.trans (.symm c) c) (.symm c)) (.symm c) :=
  .trans
    (.congrComp (.inverseLeft c) (.refl (.symm c)))
    (.leftUnit (.symm c))

/-- Both words exist as distinct raw six-cell constructors, yet a
NONEMPTY seventh-level type-valued rewrite connects them. -/
theorem sevenRewrite_roundtrip_exists_notStrict (l r : W) :
    Nonempty (SevenRewrite W l r
      (.trans (.pentagon : PentagonAdjoinedSixCell W l r l r)
        (.symm (.pentagon)))
      (.refl l)) ∧
    (show PentagonAdjoinedSixCell W l r l l from
      .trans (.pentagon) (.symm (.pentagon))) ≠ (.refl l) :=
  ⟨⟨.inverseRight (.pentagon : PentagonAdjoinedSixCell W l r l r)⟩,
    raw_inverseCancellation_notStrict l r⟩

/-- There cannot be an endpoint-preserving map interpreting ALL newly
adjoined seventh-level REWRITES as strict six-cell raw constructor Eq. -/
theorem sevenRewrite_noStrictInterpreter (l r : W) :
    ¬ (∀ (w z : W)
        (c d : PentagonAdjoinedSixCell W l r w z),
        SevenRewrite W l r c d → c = d) := by
  intro interpret
  have hEq := interpret l l
    (.trans (.pentagon : PentagonAdjoinedSixCell W l r l r)
      (.symm (.pentagon))) (.refl l)
    (.inverseRight (.pentagon : PentagonAdjoinedSixCell W l r l r))
  exact raw_inverseCancellation_notStrict l r hEq

/-- A true raw equality is an explicit rewrite, and every explicit
rewrite descends; the two abstraction directions are deliberately
kept distinct. -/
theorem sevenRewrite_eqEmbedding_and_quotientSound {w z : W}
    {c d : PentagonAdjoinedSixCell W long short w z}
    (hEq : c = d) :
    Nonempty (SevenRewrite W long short c d) ∧
      homMk c = homMk d :=
  ⟨⟨sevenRewrite_ofEq hEq⟩,
    sevenRewrite_quotientSound (sevenRewrite_ofEq hEq)⟩

end PentagonAdjoinedSixCell

section ActualSourceTypedSevenRewrite
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

/-- A GENUINE P77 terminal raw index supplies ACTUAL old five-cell
endpoints, while the rewrite between new six-cell raw words is an
EXPLICIT, separately added Type-valued seven-cell presentation. -/
def pentagonActualSevenRewrite_roundtrip
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄)) :
    PentagonAdjoinedSixCell.SevenRewrite
      (pentagonFinalConservativeLoop f g h k i)
      (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
      (pentagonShortConservativeFiveCell f g h k A B C D₄ i)
      (pentagonAdjoinedSixCell_roundtrip f g h k A B C D₄ i)
      (.refl (pentagonLongConservativeFiveCell f g h k A B C D₄ i)) :=
  .inverseRight (pentagonAdjoinedSixCell_generator f g h k A B C D₄ i)

/-- Type-valued seventh-level evidence AND failure of strict raw
six-cell equality are jointly true at EVERY original P77 raw index. -/
theorem pentagonActualSevenRewrite_exists_notStrict
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄)) :
    Nonempty (PentagonAdjoinedSixCell.SevenRewrite
      (pentagonFinalConservativeLoop f g h k i)
      (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
      (pentagonShortConservativeFiveCell f g h k A B C D₄ i)
      (pentagonAdjoinedSixCell_roundtrip f g h k A B C D₄ i)
      (.refl (pentagonLongConservativeFiveCell f g h k A B C D₄ i))) ∧
    pentagonAdjoinedSixCell_roundtrip f g h k A B C D₄ i ≠
      (.refl (pentagonLongConservativeFiveCell f g h k A B C D₄ i)) :=
  ⟨⟨pentagonActualSevenRewrite_roundtrip f g h k A B C D₄ i⟩,
    pentagonActualSixCell_roundtrip_notStrict f g h k A B C D₄ i⟩

/-- A constructive nontrivial two-step higher witness: the raw six
word p;p⁻¹;p rewrites to p while retaining p and both local steps. -/
def pentagonActualSevenRewrite_zigzag
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄)) :
    PentagonAdjoinedSixCell.SevenRewrite
      (pentagonFinalConservativeLoop f g h k i)
      (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
      (pentagonShortConservativeFiveCell f g h k A B C D₄ i)
      (.trans (pentagonAdjoinedSixCell_roundtrip f g h k A B C D₄ i)
        (pentagonAdjoinedSixCell_generator f g h k A B C D₄ i))
      (pentagonAdjoinedSixCell_generator f g h k A B C D₄ i) :=
  PentagonAdjoinedSixCell.sevenRewrite_zigzagRight
    (pentagonAdjoinedSixCell_generator f g h k A B C D₄ i)

/-- Its new quotient image agrees, but the only input is the
history-preserving Type-valued seventh-level term, not old Eq. -/
theorem pentagonActualSevenRewrite_zigzagQuotientSound
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄)) :
    PentagonAdjoinedSixCell.homMk
      (.trans (pentagonAdjoinedSixCell_roundtrip f g h k A B C D₄ i)
        (pentagonAdjoinedSixCell_generator f g h k A B C D₄ i)) =
    PentagonAdjoinedSixCell.homMk
      (pentagonAdjoinedSixCell_generator f g h k A B C D₄ i) :=
  PentagonAdjoinedSixCell.sevenRewrite_quotientSound
    (pentagonActualSevenRewrite_zigzag f g h k A B C D₄ i)

/-- The actual OLD equality interpreter is still impossible even
though the explicitly NEW seventh-level rewrite exists. -/
theorem pentagonActualSevenRewrite_withOriginalNoGo
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄)) :
    Nonempty (PentagonAdjoinedSixCell.SevenRewrite
      (pentagonFinalConservativeLoop f g h k i)
      (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
      (pentagonShortConservativeFiveCell f g h k A B C D₄ i)
      (pentagonAdjoinedSixCell_roundtrip f g h k A B C D₄ i)
      (.refl (pentagonLongConservativeFiveCell f g h k A B C D₄ i))) ∧
    ¬ PentagonAdjoinedSixCellEqualityInterpreter f g h k A B C D₄ i :=
  ⟨⟨pentagonActualSevenRewrite_roundtrip f g h k A B C D₄ i⟩,
    pentagonAdjoinedSixCell_noEqualityInterpreter f g h k A B C D₄ i⟩

/-- Stronger obstruction: interpreting EVERY seventh-level rewrite as
raw sixth-level equality is impossible, even for genuine P77 endpoints. -/
theorem pentagonActualSevenRewrite_noStrictInterpreter
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄)) :
    ¬ (∀ (w z : pentagonFinalConservativeLoop f g h k i)
        (c d : pentagonAdjoinedSixCellAt f g h k A B C D₄ i w z),
        PentagonAdjoinedSixCell.SevenRewrite
          (pentagonFinalConservativeLoop f g h k i)
          (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
          (pentagonShortConservativeFiveCell f g h k A B C D₄ i)
          c d → c = d) :=
  PentagonAdjoinedSixCell.sevenRewrite_noStrictInterpreter _ _

#print axioms PentagonAdjoinedSixCell.SevenRewrite
#print axioms PentagonAdjoinedSixCell.sevenRewrite_ofEq
#print axioms PentagonAdjoinedSixCell.sevenRewrite_degreeSound
#print axioms PentagonAdjoinedSixCell.sevenRewrite_quotientSound
#print axioms PentagonAdjoinedSixCell.sevenRewrite_degreeObstruction
#print axioms PentagonAdjoinedSixCell.selfPentagonLoop_noSevenRewrite
#print axioms PentagonAdjoinedSixCell.sevenRewrite_zigzagRight
#print axioms PentagonAdjoinedSixCell.sevenRewrite_zigzagLeft
#print axioms PentagonAdjoinedSixCell.sevenRewrite_roundtrip_exists_notStrict
#print axioms PentagonAdjoinedSixCell.sevenRewrite_noStrictInterpreter
#print axioms PentagonAdjoinedSixCell.sevenRewrite_eqEmbedding_and_quotientSound
#print axioms pentagonActualSevenRewrite_roundtrip
#print axioms pentagonActualSevenRewrite_exists_notStrict
#print axioms pentagonActualSevenRewrite_zigzag
#print axioms pentagonActualSevenRewrite_zigzagQuotientSound
#print axioms pentagonActualSevenRewrite_withOriginalNoGo
#print axioms pentagonActualSevenRewrite_noStrictInterpreter

end ActualSourceTypedSevenRewrite
end FivefoldP77FiniteRefinement
end
end KUOS.Architecture.WuxingPentagonUnified
