import KUOS.Architecture.QiWuxingGK5CHP77TraceLengthReflectingNineteenBoundaryV5_41

/-!
Qi v5.42 — the remaining nonfaithfulness of the concrete v5.41
nonconstant boundary, even for two source witnesses with the SAME
complete ordered exterior List Bool trace.

The selected 19D comparison has only strict, old-inherited
unitPrepend/unitAppend, reverse, and chain constructors. Its two
unit comparisons insert chain nodes over inherited 18D terms,
whose external 7D traces are empty. Hence a new raw 18D invariant
counts only chain nodes with nonempty exterior history. The proof
that all FIVE genuine selected local 19D constructors preserve
this active-chain count gives a second exact-fiber quotient
observable, independent of the previously descended fine trace.

Given the actual LR double-context proof X with nonempty trace,
construct in the SAME dependent source fiber the strict-left
pasting Y = chain (strict source) X. Its COMPLETE ordered exterior
trace is exactly Trace(X), but the active-chain count increases by
one. Thus its selected 19D class is genuinely distinct from X.

The actual v5.41 nonconstant boundary depends only on the
source trace LENGTH, so it maps this pair to the SAME genuine RL
raw 18D proof and hence to the same target 19D class. This
constructs an unconditional noninjectivity obstruction for the
particular v5.41 boundary, while retaining its positive
trace-length reflection and chosen anchoring results.

No unrestricted original 19D unit law is assumed or added.
No arbitrary faithful mixed boundary, raw Eq, heterogeneous
20D exchange, full swap naturality, or same-trace comparison
is postulated. Existing source Type witnesses and independent
presentations remain unchanged. Public root107, Lean/mathlib pins,
protected #1558 unchanged. Append-only / tighten-only /
overwrite-forbidden / same-root.
-/

set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uSix

namespace KUOS.Architecture.WuxingPentagonUnified
namespace FivefoldP77FiniteRefinement
namespace PentagonAdjoinedSixCell

variable {W : Type uSix}

/-- Count 18D raw chain nodes whose concatenated EXTERIOR 7D
history is nonempty. An old inherited 18D proof and a strict
identity both have empty exterior history; the two genuine 19D
unit-pasting generators therefore do not change this number.
Unlike the ordinary raw top tag, this observation respects all
chosen local 19D comparison constructors. -/
def selectedContextEighteenActiveChainCount (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedContextualEighteen W l r J N) : Nat :=
  match M with
  | .inherited _ => 0
  | .whiskerLeft _ _ _ M =>
      selectedContextEighteenActiveChainCount l r M
  | .whiskerRight _ _ M _ =>
      selectedContextEighteenActiveChainCount l r M
  | .strict _ => 0
  | .reverse M =>
      selectedContextEighteenActiveChainCount l r M
  | .chain M L =>
      selectedContextEighteenActiveChainCount l r M +
        selectedContextEighteenActiveChainCount l r L +
        (if 0 < (selectedContextEighteenTrace l r M).length +
            (selectedContextEighteenTrace l r L).length then 1 else 0)

/-- This second observation is genuinely invariant under each
existing Type-valued selected 19D generator. In particular,
unitPrepend/unitAppend apply only to inherited old 18D values,
not to an arbitrary contextual 18D term. -/
theorem selectedLocalNineteen_preservesActiveChainCount (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    {J N : SelectedContextualSeventeen W l r H K}
    {M L : SelectedContextualEighteen W l r J N}
    (A : SelectedLocalNineteen W l r M L) :
    selectedContextEighteenActiveChainCount l r M =
      selectedContextEighteenActiveChainCount l r L := by
  induction A with
  | strict M => rfl
  | unitPrepend M => rfl
  | unitAppend M => rfl
  | reverse A ih => exact ih.symm
  | chain A B ih ih' => exact ih.trans ih'

/-- This additional proof-value-sensitive observable descends
through the ACTUAL same-fiber 19D quotient by a true Quotient.lift. -/
def selectedNineteenActiveChainOnQuotient (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedNineteenSetoid l r J N) → Nat :=
  Quotient.lift (selectedContextEighteenActiveChainCount l r) (by
    intro M L h
    rcases h with ⟨A⟩
    exact selectedLocalNineteen_preservesActiveChainCount l r A)

/-- The active-chain quotient observable evaluates to the actual
raw Type-valued proof's active-chain count. -/
theorem selectedNineteenActiveChain_onClass (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedContextualEighteen W l r J N) :
    selectedNineteenActiveChainOnQuotient l r J N
        (selectedNineteenClass l r M) =
      selectedContextEighteenActiveChainCount l r M :=
  rfl

section MixedBoundary

variable (l r : W) {w z : W}
variable {a b c d : PentagonAdjoinedSixCell W l r w z}
variable (left : SevenRewrite W l r a b)
variable (F G : ContextFrameEleven W l r b c)
variable {P Q : SelectedUnitalCompositionTwelve W l r
  (contextFramePack l r F) (contextFramePack l r G)}
variable {C D : SelectedMixedInterchangerThirteen W l r P Q}
variable {V X : SelectedMixedNaturalityFourteen W l r C D}
variable {T U : SelectedContextualFifteen W l r V X}
variable {H K : SelectedContextualSixteen W l r T U}
variable (J N : SelectedContextualSeventeen W l r H K)
variable (right : SevenRewrite W l r c d)

/-- Insert a true contextual 18D strict identity on the left
of an arbitrary genuine LR source 18D proof. Its original
dependent 17D endpoints are preserved exactly. This is NOT
an assumed 19D comparison. -/
def selectedMixedLeftStrictPrepend
    (X : selectedMixedLeftNineteenRaw l r left F G J N right) :
    selectedMixedLeftNineteenRaw l r left F G J N right :=
  .chain (.strict _) X

/-- This strict-left pasting preserves the ENTIRE fine ordered
external history, not merely its length or swap observation. -/
theorem selectedMixedLeftStrictPrepend_trace
    (X : selectedMixedLeftNineteenRaw l r left F G J N right) :
    selectedContextEighteenTrace l r
        (selectedMixedLeftStrictPrepend l r left F G J N right X) =
      selectedContextEighteenTrace l r X :=
  rfl

/-- For a source proof with at least one exterior event, adding
a strict-left chain increases the quotient-stable active-chain
count by EXACTLY one, despite preserving its fine trace. -/
theorem selectedMixedLeftStrictPrepend_activeChainCount
    (X : selectedMixedLeftNineteenRaw l r left F G J N right)
    (hpos : 0 < (selectedContextEighteenTrace l r X).length) :
    selectedContextEighteenActiveChainCount l r
        (selectedMixedLeftStrictPrepend l r left F G J N right X) =
      selectedContextEighteenActiveChainCount l r X + 1 := by
  change (0 : Nat) + selectedContextEighteenActiveChainCount l r X +
      (if 0 < 0 + (selectedContextEighteenTrace l r X).length
       then 1 else 0) =
    selectedContextEighteenActiveChainCount l r X + 1
  simp [hpos]

/-- The actual LR double-context proof has nonempty fine trace,
so strict-left pasting gives two proofs with different values of
the additional 19D-quotient-stable active-chain observable. -/
theorem selectedMixedLeftStrictPrepend_classDistinct
    (M : SelectedContextualEighteen W l r J N) :
    selectedNineteenClass l r
        (selectedEighteenLeftAfterRight l r left F G M right) ≠
      selectedNineteenClass l r
        (selectedMixedLeftStrictPrepend l r left F G J N right
          (selectedEighteenLeftAfterRight l r left F G M right)) := by
  have hpos : 0 < (selectedContextEighteenTrace l r
      (selectedEighteenLeftAfterRight l r left F G M right)).length := by
    rw [(selectedEighteenMixedTraceValues l r left F G M right).1]
    simp
  intro hclass
  have hcount := congrArg (selectedNineteenActiveChainOnQuotient l r _ _)
    hclass
  change selectedContextEighteenActiveChainCount l r
        (selectedEighteenLeftAfterRight l r left F G M right) =
      selectedContextEighteenActiveChainCount l r
        (selectedMixedLeftStrictPrepend l r left F G J N right
          (selectedEighteenLeftAfterRight l r left F G M right)) at hcount
  rw [selectedMixedLeftStrictPrepend_activeChainCount
    l r left F G J N right
    (selectedEighteenLeftAfterRight l r left F G M right) hpos] at hcount
  omega

/-- No true selected local 19D Type-valued comparison exists
between this ACTUAL pair, even though their complete ordered
traces agree. This does not exclude some other presentation's
comparison or added generator. -/
theorem selectedMixedLeftStrictPrepend_noLocal
    (M : SelectedContextualEighteen W l r J N) :
    ¬ Nonempty (SelectedLocalNineteen W l r
      (selectedEighteenLeftAfterRight l r left F G M right)
      (selectedMixedLeftStrictPrepend l r left F G J N right
        (selectedEighteenLeftAfterRight l r left F G M right))) := by
  rintro ⟨A⟩
  exact (selectedMixedLeftStrictPrepend_classDistinct
    l r left F G J N right M) (Quotient.sound ⟨A⟩)

/-- The v5.41 raw LR-to-RL map factors through source exterior
TRACE LENGTH. Hence equal source lengths force equal genuine
target raw 18D values, without any assumption of original
heterogeneous comparison. -/
theorem selectedMixedLengthRawTransport_eq_of_length
    (M : SelectedContextualEighteen W l r J N)
    {X Y : selectedMixedLeftNineteenRaw l r left F G J N right}
    (h : (selectedContextEighteenTrace l r X).length =
      (selectedContextEighteenTrace l r Y).length) :
    selectedMixedLengthRawTransport l r left F G J N right M X =
      selectedMixedLengthRawTransport l r left F G J N right M Y := by
  unfold selectedMixedLengthRawTransport
  rw [h]

/-- EXACT kernel classification of the particular v5.41
nonconstant descended boundary: two source quotient classes
have equal target images IFF their original exterior trace
LENGTHS coincide. The reverse direction was not previously
stated; it uses the actual length-factorizing raw function.
No claim of reflecting the whole ordered trace or 19D proof. -/
theorem selectedMixedLengthDescend_eq_iff_traceLength
    (M : SelectedContextualEighteen W l r J N)
    (q₁ q₂ : selectedMixedLeftNineteenQuot l r left F G J N right) :
    selectedMixedBoundaryDescend l r left F G J N right
        (selectedMixedLengthBoundary l r left F G J N right M) q₁ =
      selectedMixedBoundaryDescend l r left F G J N right
        (selectedMixedLengthBoundary l r left F G J N right M) q₂ ↔
      (selectedNineteenTraceOnQuotient l r _ _ q₁).length =
        (selectedNineteenTraceOnQuotient l r _ _ q₂).length := by
  constructor
  · exact selectedMixedLengthDescend_reflectTraceLength
      l r left F G J N right M q₁ q₂
  · intro h
    induction q₁ using Quotient.inductionOn with
    | _ X =>
        induction q₂ using Quotient.inductionOn with
        | _ Y =>
            change (selectedContextEighteenTrace l r X).length =
              (selectedContextEighteenTrace l r Y).length at h
            change selectedNineteenClass l r
                (selectedMixedLengthRawTransport l r left F G J N right M X) =
              selectedNineteenClass l r
                (selectedMixedLengthRawTransport l r left F G J N right M Y)
            exact congrArg (selectedNineteenClass l r)
              (selectedMixedLengthRawTransport_eq_of_length
                l r left F G J N right M h)

/-- Two ACTUAL distinct LR 19D classes have even the SAME
COMPLETE ordered fine trace, so their v5.41 boundary images
are equal. This is a strictly stronger nonfaithfulness witness
than a mere length-preserving map without explicit kernel data. -/
theorem selectedMixedLengthDescend_collapsesStrictPrepend
    (M : SelectedContextualEighteen W l r J N) :
    selectedMixedBoundaryDescend l r left F G J N right
        (selectedMixedLengthBoundary l r left F G J N right M)
        (selectedNineteenClass l r
          (selectedEighteenLeftAfterRight l r left F G M right)) =
      selectedMixedBoundaryDescend l r left F G J N right
        (selectedMixedLengthBoundary l r left F G J N right M)
        (selectedNineteenClass l r
          (selectedMixedLeftStrictPrepend l r left F G J N right
            (selectedEighteenLeftAfterRight l r left F G M right))) := by
  apply (selectedMixedLengthDescend_eq_iff_traceLength
    l r left F G J N right M _ _).2
  change (selectedContextEighteenTrace l r
      (selectedEighteenLeftAfterRight l r left F G M right)).length =
    (selectedContextEighteenTrace l r
      (selectedMixedLeftStrictPrepend l r left F G J N right
        (selectedEighteenLeftAfterRight l r left F G M right))).length
  exact (congrArg List.length
    (selectedMixedLeftStrictPrepend_trace l r left F G J N right
      (selectedEighteenLeftAfterRight l r left F G M right))).symm

/-- Thus the inhabited nonconstant v5.41 boundary is STILL
noninjective on its actual source/target 19D quotient types.
Its certified length reflection is fully compatible with
this new kernel obstruction. -/
theorem selectedMixedLengthDescend_notInjective
    (M : SelectedContextualEighteen W l r J N) :
    ¬ Function.Injective
      (selectedMixedBoundaryDescend l r left F G J N right
        (selectedMixedLengthBoundary l r left F G J N right M)) := by
  intro hinj
  exact (selectedMixedLeftStrictPrepend_classDistinct
    l r left F G J N right M)
    (hinj (selectedMixedLengthDescend_collapsesStrictPrepend
      l r left F G J N right M))

/-- The actual v5.41 length-based boundary does NOT admit
comparison reflection on every original selected local 19D
Type-valued proof. In particular, it is not an inhabitant
of the stronger v5.40 faithful boundary with this raw map. -/
theorem selectedMixedLengthBoundary_noReflection
    (M : SelectedContextualEighteen W l r J N) :
    ¬ Nonempty (∀ {X Y : selectedMixedLeftNineteenRaw
          l r left F G J N right},
      SelectedLocalNineteen W l r
        ((selectedMixedLengthBoundary l r left F G J N right M).rawTransport X)
        ((selectedMixedLengthBoundary l r left F G J N right M).rawTransport Y) →
      SelectedLocalNineteen W l r X Y) := by
  rintro ⟨reflectLocal⟩
  let B : SelectedMixedNineteenFaithfulBoundary
      l r left F G J N right :=
    { boundary := selectedMixedLengthBoundary l r left F G J N right M
      reflectLocal := reflectLocal }
  exact (selectedMixedLengthDescend_notInjective
    l r left F G J N right M)
    (selectedMixedFaithfulDescend_injective l r left F G J N right B)

/-- No comparison-reflecting certificate may have the same
underlying transport as this constructed length-only map. -/
theorem selectedMixedFaithful_notLengthBoundary
    (M : SelectedContextualEighteen W l r J N)
    (B : SelectedMixedNineteenFaithfulBoundary l r left F G J N right) :
    B.boundary ≠ selectedMixedLengthBoundary
      l r left F G J N right M := by
  intro h
  have hi := selectedMixedFaithfulDescend_injective
    l r left F G J N right B
  rw [h] at hi
  exact (selectedMixedLengthDescend_notInjective
    l r left F G J N right M) hi

end MixedBoundary

#print axioms PentagonAdjoinedSixCell.selectedContextEighteenActiveChainCount
#print axioms PentagonAdjoinedSixCell.selectedLocalNineteen_preservesActiveChainCount
#print axioms PentagonAdjoinedSixCell.selectedNineteenActiveChainOnQuotient
#print axioms PentagonAdjoinedSixCell.selectedNineteenActiveChain_onClass
#print axioms PentagonAdjoinedSixCell.selectedMixedLeftStrictPrepend
#print axioms PentagonAdjoinedSixCell.selectedMixedLeftStrictPrepend_trace
#print axioms PentagonAdjoinedSixCell.selectedMixedLeftStrictPrepend_activeChainCount
#print axioms PentagonAdjoinedSixCell.selectedMixedLeftStrictPrepend_classDistinct
#print axioms PentagonAdjoinedSixCell.selectedMixedLeftStrictPrepend_noLocal
#print axioms PentagonAdjoinedSixCell.selectedMixedLengthRawTransport_eq_of_length
#print axioms PentagonAdjoinedSixCell.selectedMixedLengthDescend_eq_iff_traceLength
#print axioms PentagonAdjoinedSixCell.selectedMixedLengthDescend_collapsesStrictPrepend
#print axioms PentagonAdjoinedSixCell.selectedMixedLengthDescend_notInjective
#print axioms PentagonAdjoinedSixCell.selectedMixedLengthBoundary_noReflection
#print axioms PentagonAdjoinedSixCell.selectedMixedFaithful_notLengthBoundary

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
