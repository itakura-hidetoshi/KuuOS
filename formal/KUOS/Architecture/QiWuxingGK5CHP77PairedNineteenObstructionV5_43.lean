import KUOS.Architecture.QiWuxingGK5CHP77EqualTraceNineteenNonfaithfulnessV5_42
import Mathlib.Data.Nat.Pairing

/-!
Qi v5.43 — two-component genuine 19D quotient observation,
an inhabited anchored LR-to-RL boundary reflecting BOTH components,
and an independent residual double-reversal obstruction.

The ordered exterior trace length and the active 18D chain count
descend together in each exact dependent 19D fiber. The concrete
pointed transport uses Nat.pair and the actual RL typed trace-power
family. It reflects the PAIR of quotient observables, separates the
v5.42 strict-prepend pair, and preserves actual local 19D proofs.
This is not full 19D comparison reflection.

A third quotient invariant counts raw 18D reverse constructors.
Double reversing any genuine 18D proof preserves the entire fine
trace and active chain count, but changes this reverse count by two.
Thus even the two-component observable has nontrivial fibers, and
the specific paired boundary is not faithful. No general nonexistence
claim about other faithful transports is made.

All old F55/P77/GK5CG, 6D–19D typed proofs, independent selected
presentations, public root107, Lean and mathlib pins are unchanged.
No exchange, gluing axiom, proof erasure, or heterogeneous raw Eq.
Append-only / tighten-only / overwrite-forbidden / same-root.
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

/-- The pair of actual 18D syntactic observations, before descent. -/
def selectedContextEighteenLengthActive (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedContextualEighteen W l r J N) : Nat × Nat :=
  ((selectedContextEighteenTrace l r M).length,
    selectedContextEighteenActiveChainCount l r M)

/-- A genuine two-component exact-19D-quotient observation. -/
def selectedNineteenLengthActiveObservation (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedNineteenSetoid l r J N) → Nat × Nat :=
  fun q =>
    ((selectedNineteenTraceOnQuotient l r J N q).length,
      selectedNineteenActiveChainOnQuotient l r J N q)

theorem selectedNineteenLengthActive_onClass (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedContextualEighteen W l r J N) :
    selectedNineteenLengthActiveObservation l r J N
      (selectedNineteenClass l r M) =
        selectedContextEighteenLengthActive l r M :=
  rfl

theorem selectedNineteenLengthActive_eq_iff (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    (J N : SelectedContextualSeventeen W l r H K)
    (q₁ q₂ : Quotient (selectedNineteenSetoid l r J N)) :
    selectedNineteenLengthActiveObservation l r J N q₁ =
      selectedNineteenLengthActiveObservation l r J N q₂ ↔
      (selectedNineteenTraceOnQuotient l r J N q₁).length =
        (selectedNineteenTraceOnQuotient l r J N q₂).length ∧
      selectedNineteenActiveChainOnQuotient l r J N q₁ =
        selectedNineteenActiveChainOnQuotient l r J N q₂ := by
  constructor
  · intro h
    exact ⟨congrArg Prod.fst h, congrArg Prod.snd h⟩
  · rintro ⟨h₁, h₂⟩
    exact Prod.ext h₁ h₂

/-- Reverse nodes are not canceled by any of the five selected
19D generators. This retains a third independent proof history. -/
def selectedContextEighteenReverseCount (l r : W)
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
  | .whiskerLeft _ _ _ M => selectedContextEighteenReverseCount l r M
  | .whiskerRight _ _ M _ => selectedContextEighteenReverseCount l r M
  | .strict _ => 0
  | .reverse M => selectedContextEighteenReverseCount l r M + 1
  | .chain M L =>
      selectedContextEighteenReverseCount l r M +
        selectedContextEighteenReverseCount l r L

theorem selectedLocalNineteen_preservesReverseCount (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    {J N : SelectedContextualSeventeen W l r H K}
    {M L : SelectedContextualEighteen W l r J N}
    (A : SelectedLocalNineteen W l r M L) :
    selectedContextEighteenReverseCount l r M =
      selectedContextEighteenReverseCount l r L := by
  induction A with
  | strict M => rfl
  | unitPrepend M => rfl
  | unitAppend M => rfl
  | reverse A ih => exact ih.symm
  | chain A B ih ih' => exact ih.trans ih'

def selectedNineteenReverseCountOnQuotient (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedNineteenSetoid l r J N) → Nat :=
  Quotient.lift (selectedContextEighteenReverseCount l r) (by
    intro M L h
    rcases h with ⟨A⟩
    exact selectedLocalNineteen_preservesReverseCount l r A)

/-- A new proof in exactly the same dependent 17D endpoint fiber. -/
def selectedContextEighteenDoubleReverse (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedContextualEighteen W l r J N) :
    SelectedContextualEighteen W l r J N :=
  .reverse (.reverse M)

theorem selectedContextEighteenDoubleReverse_trace (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedContextualEighteen W l r J N) :
    selectedContextEighteenTrace l r
      (selectedContextEighteenDoubleReverse l r M) =
        selectedContextEighteenTrace l r M :=
  rfl

theorem selectedContextEighteenDoubleReverse_active (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedContextualEighteen W l r J N) :
    selectedContextEighteenActiveChainCount l r
      (selectedContextEighteenDoubleReverse l r M) =
        selectedContextEighteenActiveChainCount l r M :=
  rfl

theorem selectedContextEighteenDoubleReverse_reverseCount (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedContextualEighteen W l r J N) :
    selectedContextEighteenReverseCount l r
      (selectedContextEighteenDoubleReverse l r M) =
        selectedContextEighteenReverseCount l r M + 2 := by
  change (selectedContextEighteenReverseCount l r M + 1) + 1 =
    selectedContextEighteenReverseCount l r M + 2
  omega

/-- The exact 19D quotient distinguishes double reversal by a
proved count invariant; no raw proof equality is used. -/
theorem selectedNineteenDoubleReverse_classDistinct (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedContextualEighteen W l r J N) :
    selectedNineteenClass l r M ≠
      selectedNineteenClass l r
        (selectedContextEighteenDoubleReverse l r M) := by
  intro h
  have hc := congrArg (selectedNineteenReverseCountOnQuotient l r _ _) h
  change selectedContextEighteenReverseCount l r M =
    selectedContextEighteenReverseCount l r
      (selectedContextEighteenDoubleReverse l r M) at hc
  rw [selectedContextEighteenDoubleReverse_reverseCount l r M] at hc
  omega

/-- Equality of the PAIR of observations is strictly weaker
than equality of actual local 19D proof quotient classes. -/
theorem selectedNineteenLengthActive_doubleReverseEq (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedContextualEighteen W l r J N) :
    selectedNineteenLengthActiveObservation l r J N
      (selectedNineteenClass l r M) =
    selectedNineteenLengthActiveObservation l r J N
      (selectedNineteenClass l r
        (selectedContextEighteenDoubleReverse l r M)) :=
  rfl

theorem selectedNineteenLengthActive_notInjective (l r : W)
    {F G : FramedEleven W l r}
    {P Q : SelectedUnitalCompositionTwelve W l r F G}
    {C D : SelectedMixedInterchangerThirteen W l r P Q}
    {V X : SelectedMixedNaturalityFourteen W l r C D}
    {T U : SelectedContextualFifteen W l r V X}
    {H K : SelectedContextualSixteen W l r T U}
    {J N : SelectedContextualSeventeen W l r H K}
    (M : SelectedContextualEighteen W l r J N) :
    ¬ Function.Injective (selectedNineteenLengthActiveObservation l r J N) := by
  intro hinj
  exact (selectedNineteenDoubleReverse_classDistinct l r M)
    (hinj (selectedNineteenLengthActive_doubleReverseEq l r M))

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

/-- Injective pointed two-coordinate coding into the natural
index of the existing GENUINE RL trace-power witness family. -/
def selectedMixedPairedCode (base p : Nat × Nat) : Nat :=
  selectedMixedLengthCode (Nat.pair base.1 base.2) (Nat.pair p.1 p.2)

theorem selectedMixedPairedCode_injective (base : Nat × Nat) :
    Function.Injective (selectedMixedPairedCode base) := by
  intro p q h
  have hPair : Nat.pair p.1 p.2 = Nat.pair q.1 q.2 :=
    selectedMixedLengthCode_injective (Nat.pair base.1 base.2) h
  exact Prod.ext (Nat.pair_eq_pair.mp hPair).1 (Nat.pair_eq_pair.mp hPair).2

/-- An inhabited, explicitly typed LR-to-RL map, now using both
19D quotient observables rather than only the trace length. -/
def selectedMixedPairedRawTransport
    (M : SelectedContextualEighteen W l r J N)
    (X : selectedMixedLeftNineteenRaw l r left F G J N right) :
    selectedMixedRightNineteenRaw l r left F G J N right :=
  selectedMixedRightTracePower l r left F G J N right
    (selectedEighteenRightAfterLeft l r left F G M right)
    (selectedMixedPairedCode
      (selectedContextEighteenLengthActive l r
        (selectedEighteenLeftAfterRight l r left F G M right))
      (selectedContextEighteenLengthActive l r X))

theorem selectedMixedPairedRawTransport_chosen
    (M : SelectedContextualEighteen W l r J N) :
    selectedMixedPairedRawTransport l r left F G J N right M
      (selectedEighteenLeftAfterRight l r left F G M right) =
        selectedEighteenRightAfterLeft l r left F G M right := by
  simp [selectedMixedPairedRawTransport, selectedMixedPairedCode,
    selectedMixedLengthCode, selectedMixedRightTracePower]

/-- True 19D proof-valued comparison preservation, not merely an
abstract function on observed pairs or a quotient map postulate. -/
def selectedMixedPairedBoundary
    (M : SelectedContextualEighteen W l r J N) :
    SelectedMixedNineteenBoundary l r left F G J N right where
  rawTransport := selectedMixedPairedRawTransport l r left F G J N right M
  localTransport := by
    intro X Y A
    have hTrace := selectedLocalNineteen_preservesEighteenTrace l r A
    have hActive := selectedLocalNineteen_preservesActiveChainCount l r A
    have hObs : selectedContextEighteenLengthActive l r X =
        selectedContextEighteenLengthActive l r Y := by
      exact Prod.ext (congrArg List.length hTrace) hActive
    have hEq :
        selectedMixedPairedRawTransport l r left F G J N right M X =
          selectedMixedPairedRawTransport l r left F G J N right M Y := by
      exact congrArg
        (selectedMixedRightTracePower l r left F G J N right
          (selectedEighteenRightAfterLeft l r left F G M right) ∘
          selectedMixedPairedCode
            (selectedContextEighteenLengthActive l r
              (selectedEighteenLeftAfterRight l r left F G M right))) hObs
    change SelectedLocalNineteen W l r
      (selectedMixedPairedRawTransport l r left F G J N right M X)
      (selectedMixedPairedRawTransport l r left F G J N right M Y)
    rw [hEq]
    exact .strict _

def selectedMixedPairedAnchored
    (M : SelectedContextualEighteen W l r J N) :
    SelectedMixedNineteenAnchored l r left F G J N right M where
  boundary := selectedMixedPairedBoundary l r left F G J N right M
  chosenComparison := by
    change SelectedLocalNineteen W l r
      (selectedMixedPairedRawTransport l r left F G J N right M
        (selectedEighteenLeftAfterRight l r left F G M right))
      (selectedEighteenRightAfterLeft l r left F G M right)
    rw [selectedMixedPairedRawTransport_chosen l r left F G J N right M]
    exact .strict _

/-- Images of the actual paired raw map agree whenever BOTH
source observables agree. -/
theorem selectedMixedPairedRaw_eq_of_observation
    (M : SelectedContextualEighteen W l r J N)
    {X Y : selectedMixedLeftNineteenRaw l r left F G J N right}
    (h : selectedContextEighteenLengthActive l r X =
      selectedContextEighteenLengthActive l r Y) :
    selectedMixedPairedRawTransport l r left F G J N right M X =
      selectedMixedPairedRawTransport l r left F G J N right M Y := by
  unfold selectedMixedPairedRawTransport
  rw [h]

/-- Any TARGET local selected 19D comparison forces equality
of BOTH original source 19D quotient observations. -/
theorem selectedMixedPairedRaw_reflectObservation
    (M : SelectedContextualEighteen W l r J N)
    {X Y : selectedMixedLeftNineteenRaw l r left F G J N right}
    (A : SelectedLocalNineteen W l r
      (selectedMixedPairedRawTransport l r left F G J N right M X)
      (selectedMixedPairedRawTransport l r left F G J N right M Y)) :
    selectedContextEighteenLengthActive l r X =
      selectedContextEighteenLengthActive l r Y := by
  let R := selectedEighteenRightAfterLeft l r left F G M right
  let base := selectedContextEighteenLengthActive l r
    (selectedEighteenLeftAfterRight l r left F G M right)
  have hlen := congrArg List.length
    (selectedLocalNineteen_preservesEighteenTrace l r A)
  change (selectedContextEighteenTrace l r
      (selectedMixedRightTracePower l r left F G J N right R
        (selectedMixedPairedCode base
          (selectedContextEighteenLengthActive l r X)))).length =
    (selectedContextEighteenTrace l r
      (selectedMixedRightTracePower l r left F G J N right R
        (selectedMixedPairedCode base
          (selectedContextEighteenLengthActive l r Y)))).length at hlen
  simp only [selectedMixedRightTracePower_length] at hlen
  have hpos : 0 < (selectedContextEighteenTrace l r R).length :=
    selectedMixedRightSeed_tracePositive l r left F G J N right M
  have hc :
      2 * selectedMixedPairedCode base
          (selectedContextEighteenLengthActive l r X) + 1 =
        2 * selectedMixedPairedCode base
          (selectedContextEighteenLengthActive l r Y) + 1 :=
    Nat.mul_right_cancel hpos hlen
  have hcode :
      selectedMixedPairedCode base (selectedContextEighteenLengthActive l r X) =
        selectedMixedPairedCode base (selectedContextEighteenLengthActive l r Y) := by
    omega
  exact selectedMixedPairedCode_injective base hcode

/-- Exact kernel classification of this PARTICULAR anchored
boundary: target class equality iff both source observables agree. -/
theorem selectedMixedPairedDescend_eq_iff_observation
    (M : SelectedContextualEighteen W l r J N)
    (q₁ q₂ : selectedMixedLeftNineteenQuot l r left F G J N right) :
    selectedMixedBoundaryDescend l r left F G J N right
      (selectedMixedPairedBoundary l r left F G J N right M) q₁ =
    selectedMixedBoundaryDescend l r left F G J N right
      (selectedMixedPairedBoundary l r left F G J N right M) q₂ ↔
    selectedNineteenLengthActiveObservation l r _ _ q₁ =
      selectedNineteenLengthActiveObservation l r _ _ q₂ := by
  constructor
  · intro h
    induction q₁ using Quotient.inductionOn with
    | _ X =>
        induction q₂ using Quotient.inductionOn with
        | _ Y =>
            change selectedNineteenClass l r
                (selectedMixedPairedRawTransport l r left F G J N right M X) =
              selectedNineteenClass l r
                (selectedMixedPairedRawTransport l r left F G J N right M Y) at h
            rcases Quotient.exact h with ⟨A⟩
            exact selectedMixedPairedRaw_reflectObservation
              l r left F G J N right M A
  · intro h
    induction q₁ using Quotient.inductionOn with
    | _ X =>
        induction q₂ using Quotient.inductionOn with
        | _ Y =>
            change selectedContextEighteenLengthActive l r X =
              selectedContextEighteenLengthActive l r Y at h
            change selectedNineteenClass l r
                (selectedMixedPairedRawTransport l r left F G J N right M X) =
              selectedNineteenClass l r
                (selectedMixedPairedRawTransport l r left F G J N right M Y)
            exact congrArg (selectedNineteenClass l r)
              (selectedMixedPairedRaw_eq_of_observation
                l r left F G J N right M h)

/-- Unlike v5.41's length-only transport, the paired boundary
separates the actual strict-prepend source classes. -/
theorem selectedMixedPairedDescend_separatesStrictPrepend
    (M : SelectedContextualEighteen W l r J N) :
    selectedMixedBoundaryDescend l r left F G J N right
      (selectedMixedPairedBoundary l r left F G J N right M)
      (selectedNineteenClass l r
        (selectedEighteenLeftAfterRight l r left F G M right)) ≠
    selectedMixedBoundaryDescend l r left F G J N right
      (selectedMixedPairedBoundary l r left F G J N right M)
      (selectedNineteenClass l r
        (selectedMixedLeftStrictPrepend l r left F G J N right
          (selectedEighteenLeftAfterRight l r left F G M right))) := by
  intro h
  have hobs := (selectedMixedPairedDescend_eq_iff_observation
    l r left F G J N right M _ _).mp h
  have hactive := congrArg Prod.snd hobs
  change selectedContextEighteenActiveChainCount l r
      (selectedEighteenLeftAfterRight l r left F G M right) =
    selectedContextEighteenActiveChainCount l r
      (selectedMixedLeftStrictPrepend l r left F G J N right
        (selectedEighteenLeftAfterRight l r left F G M right)) at hactive
  have hpos : 0 < (selectedContextEighteenTrace l r
      (selectedEighteenLeftAfterRight l r left F G M right)).length := by
    rw [(selectedEighteenMixedTraceValues l r left F G M right).1]
    simp
  rw [selectedMixedLeftStrictPrepend_activeChainCount
    l r left F G J N right
    (selectedEighteenLeftAfterRight l r left F G M right) hpos] at hactive
  omega

/-- Even the paired boundary collapses genuine double-reversal
classes, proved distinct by a THIRD quotient-stable count. -/
theorem selectedMixedPairedDescend_notInjective
    (M : SelectedContextualEighteen W l r J N) :
    ¬ Function.Injective
      (selectedMixedBoundaryDescend l r left F G J N right
        (selectedMixedPairedBoundary l r left F G J N right M)) := by
  intro hinj
  let X := selectedEighteenLeftAfterRight l r left F G M right
  have hObs : selectedNineteenLengthActiveObservation l r _ _
      (selectedNineteenClass l r X) =
    selectedNineteenLengthActiveObservation l r _ _
      (selectedNineteenClass l r
        (selectedContextEighteenDoubleReverse l r X)) :=
    selectedNineteenLengthActive_doubleReverseEq l r X
  have hCollapsed := (selectedMixedPairedDescend_eq_iff_observation
    l r left F G J N right M _ _).2 hObs
  exact (selectedNineteenDoubleReverse_classDistinct l r X) (hinj hCollapsed)

/-- This particular two-observable boundary cannot carry a
full proof-valued reflection field; this is NOT a no-go for every
possible mixed LR-to-RL boundary. -/
theorem selectedMixedPairedBoundary_noReflection
    (M : SelectedContextualEighteen W l r J N) :
    ¬ Nonempty (∀ {X Y : selectedMixedLeftNineteenRaw
          l r left F G J N right},
      SelectedLocalNineteen W l r
        ((selectedMixedPairedBoundary l r left F G J N right M).rawTransport X)
        ((selectedMixedPairedBoundary l r left F G J N right M).rawTransport Y) →
      SelectedLocalNineteen W l r X Y) := by
  rintro ⟨reflectLocal⟩
  let B : SelectedMixedNineteenFaithfulBoundary
      l r left F G J N right :=
    { boundary := selectedMixedPairedBoundary l r left F G J N right M
      reflectLocal := reflectLocal }
  exact (selectedMixedPairedDescend_notInjective
    l r left F G J N right M)
    (selectedMixedFaithfulDescend_injective l r left F G J N right B)

/-- Actual chosen LR and RL witnesses still agree at the
coarse swap quotient; global swap naturality remains unverified. -/
theorem selectedMixedPairedAnchored_chosenSwap
    (M : SelectedContextualEighteen W l r J N) :
    selectedNineteenSwapObservation l r _ _
      (selectedNineteenClass l r
        (selectedEighteenLeftAfterRight l r left F G M right)) =
      selectedNineteenSwapObservation l r _ _
        (selectedMixedBoundaryDescend l r left F G J N right
          (selectedMixedPairedBoundary l r left F G J N right M)
          (selectedNineteenClass l r
            (selectedEighteenLeftAfterRight l r left F G M right))) := by
  exact selectedMixedAnchored_chosenSwap l r left F G J N right
    M (selectedMixedPairedAnchored l r left F G J N right M)

end MixedBoundary

#print axioms PentagonAdjoinedSixCell.selectedContextEighteenLengthActive
#print axioms PentagonAdjoinedSixCell.selectedNineteenLengthActiveObservation
#print axioms PentagonAdjoinedSixCell.selectedNineteenLengthActive_onClass
#print axioms PentagonAdjoinedSixCell.selectedNineteenLengthActive_eq_iff
#print axioms PentagonAdjoinedSixCell.selectedContextEighteenReverseCount
#print axioms PentagonAdjoinedSixCell.selectedLocalNineteen_preservesReverseCount
#print axioms PentagonAdjoinedSixCell.selectedNineteenReverseCountOnQuotient
#print axioms PentagonAdjoinedSixCell.selectedContextEighteenDoubleReverse
#print axioms PentagonAdjoinedSixCell.selectedContextEighteenDoubleReverse_trace
#print axioms PentagonAdjoinedSixCell.selectedContextEighteenDoubleReverse_active
#print axioms PentagonAdjoinedSixCell.selectedContextEighteenDoubleReverse_reverseCount
#print axioms PentagonAdjoinedSixCell.selectedNineteenDoubleReverse_classDistinct
#print axioms PentagonAdjoinedSixCell.selectedNineteenLengthActive_doubleReverseEq
#print axioms PentagonAdjoinedSixCell.selectedNineteenLengthActive_notInjective
#print axioms PentagonAdjoinedSixCell.selectedMixedPairedCode
#print axioms PentagonAdjoinedSixCell.selectedMixedPairedCode_injective
#print axioms PentagonAdjoinedSixCell.selectedMixedPairedRawTransport
#print axioms PentagonAdjoinedSixCell.selectedMixedPairedRawTransport_chosen
#print axioms PentagonAdjoinedSixCell.selectedMixedPairedBoundary
#print axioms PentagonAdjoinedSixCell.selectedMixedPairedAnchored
#print axioms PentagonAdjoinedSixCell.selectedMixedPairedRaw_eq_of_observation
#print axioms PentagonAdjoinedSixCell.selectedMixedPairedRaw_reflectObservation
#print axioms PentagonAdjoinedSixCell.selectedMixedPairedDescend_eq_iff_observation
#print axioms PentagonAdjoinedSixCell.selectedMixedPairedDescend_separatesStrictPrepend
#print axioms PentagonAdjoinedSixCell.selectedMixedPairedDescend_notInjective
#print axioms PentagonAdjoinedSixCell.selectedMixedPairedBoundary_noReflection
#print axioms PentagonAdjoinedSixCell.selectedMixedPairedAnchored_chosenSwap

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
