import KUOS.Architecture.QiWuxingGK5CHP77SixNineteenTypedBoundaryV5_47

/-!
Qi v5.48 — exact typed unit normal form for the ORIGINAL selected 19D
comparison presentation, and the criterion for comparison reflection.

Only the two existing, old-inherited 18D unit insertion generators
are normalized. The symmetry/transitivity constructors are comparison
paths, not contextual rewriting rules for arbitrary raw constructors.
No original Type-valued evidence, local 19D constructor, original
dependent endpoint, public root, or Lean/mathlib pin is modified.
In particular, no global exchange or general faithful boundary is assumed.
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

section ExactNormal

variable (l r : W)
variable {F G : FramedEleven W l r}
variable {P Q : SelectedUnitalCompositionTwelve W l r F G}
variable {C D : SelectedMixedInterchangerThirteen W l r P Q}
variable {V X : SelectedMixedNaturalityFourteen W l r C D}
variable {T U : SelectedContextualFifteen W l r V X}
variable {H K : SelectedContextualSixteen W l r T U}
variable {J N : SelectedContextualSeventeen W l r H K}

/-- Construct a normal representative TOGETHER WITH an original
Type-valued selected19 comparison, not just an equality of numbers.
Only direct unit insertion around a genuine inherited old18 value is
contracted. All other original constructors are retained as syntax. -/
def selectedNineteenNormalCertified
    (M : SelectedContextualEighteen W l r J N) :
    Σ K : SelectedContextualEighteen W l r J N,
      SelectedLocalNineteen W l r M K :=
  match M with
  | .chain (.strict _) (.inherited X) =>
      ⟨.inherited X, .unitPrepend X⟩
  | .chain (.inherited X) (.strict _) =>
      ⟨.inherited X, .unitAppend X⟩
  | X => ⟨X, .strict X⟩

/-- The representative is still an ORIGINAL exact-fiber raw18D term. -/
def selectedNineteenNormal
    (M : SelectedContextualEighteen W l r J N) :
    SelectedContextualEighteen W l r J N :=
  (selectedNineteenNormalCertified l r M).1

theorem selectedNineteenNormal_rawCertified
    (M : SelectedContextualEighteen W l r J N) :
    SelectedLocalNineteen W l r M (selectedNineteenNormal l r M) :=
  (selectedNineteenNormalCertified l r M).2

/-- Every one of the FIVE actual selected19 constructors preserves
the normalized original Type-valued representative. -/
theorem selectedNineteenNormal_respects
    {M L : SelectedContextualEighteen W l r J N}
    (A : SelectedLocalNineteen W l r M L) :
    selectedNineteenNormal l r M = selectedNineteenNormal l r L := by
  induction A with
  | strict M => rfl
  | unitPrepend M => rfl
  | unitAppend M => rfl
  | reverse A ih => exact ih.symm
  | chain A B ih ih' => exact ih.trans ih'

/-- Classification in ONE exact fiber: equality of the NORMAL
original raw terms is equivalent to existence of a genuine
Type-valued 19D comparison. The direction to a comparison is
constructed from original 19D witnesses, not postulated. -/
theorem selectedNineteenNormal_eq_iff_local
    (M L : SelectedContextualEighteen W l r J N) :
    selectedNineteenNormal l r M = selectedNineteenNormal l r L ↔
      Nonempty (SelectedLocalNineteen W l r M L) := by
  constructor
  · intro h
    have hM := selectedNineteenNormal_rawCertified l r M
    have hL := selectedNineteenNormal_rawCertified l r L
    rw [← h] at hL
    exact ⟨.chain hM (.reverse hL)⟩
  · rintro ⟨A⟩
    exact selectedNineteenNormal_respects l r A

theorem selectedNineteenNormal_eq_iff_class
    (M L : SelectedContextualEighteen W l r J N) :
    selectedNineteenNormal l r M = selectedNineteenNormal l r L ↔
      selectedNineteenClass l r M = selectedNineteenClass l r L := by
  constructor
  · intro h
    exact Quotient.sound ((selectedNineteenNormal_eq_iff_local l r M L).mp h)
  · intro h
    exact (selectedNineteenNormal_eq_iff_local l r M L).mpr (Quotient.exact h)

/-- Normalization is idempotent, without silently replacing the old
Type-valued input evidence or adding normalization equations. -/
theorem selectedNineteenNormal_idempotent
    (M : SelectedContextualEighteen W l r J N) :
    selectedNineteenNormal l r (selectedNineteenNormal l r M) =
      selectedNineteenNormal l r M := by
  exact (selectedNineteenNormal_respects l r
    (selectedNineteenNormal_rawCertified l r M)).symm

/-- Canonical typed representative of each actual selected19 quotient.
The quotient's exact original endpoints are retained. -/
def selectedNineteenNormalOnQuotient
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedNineteenSetoid l r J N) →
      SelectedContextualEighteen W l r J N :=
  Quotient.lift (selectedNineteenNormal l r) (by
    intro M L h
    rcases h with ⟨A⟩
    exact selectedNineteenNormal_respects l r A)

theorem selectedNineteenNormalOnQuotient_onClass
    (M : SelectedContextualEighteen W l r J N) :
    selectedNineteenNormalOnQuotient l r J N (selectedNineteenClass l r M) =
      selectedNineteenNormal l r M := rfl

/-- The original quotient is recovered from its canonical
Type-valued representative; this is NOT original raw equality. -/
theorem selectedNineteenNormalOnQuotient_section
    (J N : SelectedContextualSeventeen W l r H K)
    (q : Quotient (selectedNineteenSetoid l r J N)) :
    selectedNineteenClass l r (selectedNineteenNormalOnQuotient l r J N q) = q := by
  induction q using Quotient.inductionOn with
  | _ M =>
      change selectedNineteenClass l r (selectedNineteenNormal l r M) =
        selectedNineteenClass l r M
      exact Quotient.sound ⟨.reverse (selectedNineteenNormal_rawCertified l r M)⟩

/-- These actual normal representatives distinguish every pair of
different selected19 quotient classes, not only finite observations. -/
theorem selectedNineteenNormalOnQuotient_injective
    (J N : SelectedContextualSeventeen W l r H K) :
    Function.Injective (selectedNineteenNormalOnQuotient l r J N) := by
  intro q1 q2 h
  calc
    q1 = selectedNineteenClass l r
        (selectedNineteenNormalOnQuotient l r J N q1) :=
      (selectedNineteenNormalOnQuotient_section l r J N q1).symm
    _ = selectedNineteenClass l r
        (selectedNineteenNormalOnQuotient l r J N q2) :=
      congrArg (selectedNineteenClass l r) h
    _ = q2 := selectedNineteenNormalOnQuotient_section l r J N q2

/-- The 6-observation residual pair remains distinct after the
complete typed normal form, despite matching ordered trace and I6. -/
theorem selectedNineteenNormal_separatesAdjacentReverse
    (M : SelectedContextualEighteen W l r J N) :
    selectedNineteenNormal l r (selectedAdjacentReverseLeft l r M) ≠
      selectedNineteenNormal l r (selectedAdjacentReverseRight l r M) := by
  intro h
  exact (selectedAdjacentReverse_classDistinct l r M)
    ((selectedNineteenNormal_eq_iff_class l r _ _).mp h)

end ExactNormal

section FaithfulCriterion

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

/-- For ANY SUPPLIED typed 19D boundary, complete Type-valued
comparison reflection is equivalent to injectivity of its genuinely
cross-fiber quotient map. This is a conditional criterion and does
not construct a faithful LR→RL boundary. -/
theorem selectedMixedBoundary_reflection_iff_injective
    (B : SelectedMixedNineteenBoundary l r left F G J N right) :
    Nonempty (∀ {X Y : selectedMixedLeftNineteenRaw l r left F G J N right},
      SelectedLocalNineteen W l r (B.rawTransport X) (B.rawTransport Y) →
        SelectedLocalNineteen W l r X Y) ↔
    Function.Injective
      (selectedMixedBoundaryDescend l r left F G J N right B) := by
  constructor
  · rintro ⟨reflectLocal⟩
    let faithful : SelectedMixedNineteenFaithfulBoundary
        l r left F G J N right :=
      { boundary := B, reflectLocal := reflectLocal }
    exact selectedMixedFaithfulDescend_injective l r left F G J N right faithful
  · intro hInjective
    refine ⟨?_⟩
    intro X Y A
    have hTarget :
        selectedMixedBoundaryDescend l r left F G J N right B
            (selectedNineteenClass l r X) =
          selectedMixedBoundaryDescend l r left F G J N right B
            (selectedNineteenClass l r Y) := by
      change selectedNineteenClass l r (B.rawTransport X) =
        selectedNineteenClass l r (B.rawTransport Y)
      exact Quotient.sound ⟨A⟩
    have hSource := hInjective hTarget
    exact Classical.choice (Quotient.exact hSource)

/-- The same condition is purely a reflection test on canonical
ORIGINAL syntax. Normal forms are compared within each own fiber;
no heterogeneous raw equality is introduced. -/
theorem selectedMixedBoundary_normalReflection_iff_injective
    (B : SelectedMixedNineteenBoundary l r left F G J N right) :
    (∀ X Y : selectedMixedLeftNineteenRaw l r left F G J N right,
      selectedNineteenNormal l r (B.rawTransport X) =
        selectedNineteenNormal l r (B.rawTransport Y) →
      selectedNineteenNormal l r X = selectedNineteenNormal l r Y) ↔
    Function.Injective
      (selectedMixedBoundaryDescend l r left F G J N right B) := by
  constructor
  · intro reflectNormal q1 q2 h
    induction q1 using Quotient.inductionOn with
    | _ X =>
        induction q2 using Quotient.inductionOn with
        | _ Y =>
            change selectedNineteenClass l r (B.rawTransport X) =
              selectedNineteenClass l r (B.rawTransport Y) at h
            have hTarget := (selectedNineteenNormal_eq_iff_class l r
              (B.rawTransport X) (B.rawTransport Y)).mpr h
            exact (selectedNineteenNormal_eq_iff_class l r X Y).mp
              (reflectNormal X Y hTarget)
  · intro hInjective X Y hNormal
    have hTarget : selectedNineteenClass l r (B.rawTransport X) =
      selectedNineteenClass l r (B.rawTransport Y) :=
      (selectedNineteenNormal_eq_iff_class l r _ _).mp hNormal
    have hSource :
        selectedNineteenClass l r X = selectedNineteenClass l r Y :=
      hInjective (by
        change selectedNineteenClass l r (B.rawTransport X) =
          selectedNineteenClass l r (B.rawTransport Y)
        exact hTarget)
    exact (selectedNineteenNormal_eq_iff_class l r X Y).mpr hSource

end FaithfulCriterion

#print axioms PentagonAdjoinedSixCell.selectedNineteenNormalCertified
#print axioms PentagonAdjoinedSixCell.selectedNineteenNormal
#print axioms PentagonAdjoinedSixCell.selectedNineteenNormal_rawCertified
#print axioms PentagonAdjoinedSixCell.selectedNineteenNormal_respects
#print axioms PentagonAdjoinedSixCell.selectedNineteenNormal_eq_iff_local
#print axioms PentagonAdjoinedSixCell.selectedNineteenNormal_eq_iff_class
#print axioms PentagonAdjoinedSixCell.selectedNineteenNormal_idempotent
#print axioms PentagonAdjoinedSixCell.selectedNineteenNormalOnQuotient
#print axioms PentagonAdjoinedSixCell.selectedNineteenNormalOnQuotient_onClass
#print axioms PentagonAdjoinedSixCell.selectedNineteenNormalOnQuotient_section
#print axioms PentagonAdjoinedSixCell.selectedNineteenNormalOnQuotient_injective
#print axioms PentagonAdjoinedSixCell.selectedNineteenNormal_separatesAdjacentReverse
#print axioms PentagonAdjoinedSixCell.selectedMixedBoundary_reflection_iff_injective
#print axioms PentagonAdjoinedSixCell.selectedMixedBoundary_normalReflection_iff_injective

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
