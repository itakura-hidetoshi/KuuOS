import KUOS.Architecture.QiWuxingGK5CHP77ContextLocalDescentObstructionV4_63
import Mathlib.CategoryTheory.Equivalence
import Mathlib.Combinatorics.Quiver.Path
import Mathlib.Tactic

/-!
Qi v4.64 — GENUINE ORIGINAL P77 TWO-SEGMENT TYPE-VALUED DESCENT.

The v4.63 single-Hom local-gluing criterion is now transported
through the ACTUAL original P77 vertical composition at two
consecutive, authentically typed FivefoldEdge source boundaries.

For two nonempty original F55/P77 raw-four-cell patch families
at u→v and v→w, their Type-valued conservative GK5CG five-cell
pairwise overlap certificates, together with at least one ORIGINAL
typed source evaluation certificate per segment, are necessary
and sufficient for a PAIR of genuine original free source paths
mapping to all corresponding original P77 raw quotient classes.
The path PAIR is unique. The genuine source composite maps to
each pair of target P77 classes under original quotient composition;
its v4.62 partial recovery is EXACTLY the source composite.

This is source-factorized local descent, not a claim that EVERY
reachable composite target can be factorized by arbitrary raw
intermediate classes. Original charge -1 and charge-zero inverse
obstructions remain genuine and are NOT completed by a new reverse
source edge, numerical charge, or a fake five-cell.

A source typed path already represents an arbitrary finite
concatenation of original FivefoldEdge generators. No unproved
general sheaf gluing, new pentagonator, Gray, or definitionally
equal choice-dependent quasi-inverses.

Append-only, same-root; strict 空 central, independent Kuu a
presentation. Keep original F55/P77/P94A, C60 physical gauge,
north C60 CRT and their proofs distinct. No new axioms,
sorry/admit/native_decide. Published root107 unchanged.
Lean v4.30.0-rc2, pinned mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Protected validation-only PR #1558 Draft/open/unmerged.
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

universe uD vD uE vE

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

/-- A genuine pair of typed source path segments has exact patch
classes on BOTH sides iff each nonempty patch family admits
Type-valued overlap five-cells and at least one genuine source
five-cell anchor. There is no inference from merely equal charge. -/
theorem fivefoldP77TwoPatchLocalDescent_iff
    {u v w : FivefoldPathVertex} {I J : Type} [Nonempty I] [Nonempty J]
    (left : I → FivefoldP77LocalRaw f g h k u v)
    (right : J → FivefoldP77LocalRaw f g h k v w) :
    (∃ pair : Quiver.Path u v × Quiver.Path v w,
      (∀ i : I, (fivefoldP77ConservativeFunctor f g h k).map pair.1 =
        fivefoldP77ConservativeClass f g h k (left i)) ∧
      (∀ j : J, (fivefoldP77ConservativeFunctor f g h k).map pair.2 =
        fivefoldP77ConservativeClass f g h k (right j))) ↔
    ((∀ i i' : I,
        Nonempty (NativeGK5CGConservativeFiveCell first last
          (left i) (left i'))) ∧
      (∃ i : I, ∃ path : Quiver.Path u v,
        Nonempty (NativeGK5CGConservativeFiveCell first last
          (fivefoldEvaluateP77 f g h k path) (left i)))) ∧
    ((∀ j j' : J,
        Nonempty (NativeGK5CGConservativeFiveCell first last
          (right j) (right j'))) ∧
      (∃ j : J, ∃ path : Quiver.Path v w,
        Nonempty (NativeGK5CGConservativeFiveCell first last
          (fivefoldEvaluateP77 f g h k path) (right j)))) := by
  letI := fivefoldP77ConservativeCategory f g h k
  constructor
  · rintro ⟨⟨pathL, pathR⟩, hL, hR⟩
    exact ⟨
      (fivefoldP77LocalTypeDescent_iff f g h k left).1
        ⟨pathL, hL⟩,
      (fivefoldP77LocalTypeDescent_iff f g h k right).1
        ⟨pathR, hR⟩⟩
  · rintro ⟨hL, hR⟩
    obtain ⟨pathL, hpathL⟩ :=
      (fivefoldP77LocalTypeDescent_iff f g h k left).2 hL
    obtain ⟨pathR, hpathR⟩ :=
      (fivefoldP77LocalTypeDescent_iff f g h k right).2 hR
    exact ⟨(pathL, pathR), hpathL, hpathR⟩

/-- Factorwise source-path uniqueness on ORIGINAL segment patches.
Do not claim that every full target P77 composite has such a pair. -/
theorem fivefoldP77TwoPatchLocalDescent_unique
    {u v w : FivefoldPathVertex} {I J : Type} [Nonempty I] [Nonempty J]
    (left : I → FivefoldP77LocalRaw f g h k u v)
    (right : J → FivefoldP77LocalRaw f g h k v w)
    (hL :
      (∀ i i' : I,
        Nonempty (NativeGK5CGConservativeFiveCell first last
          (left i) (left i'))) ∧
      (∃ i : I, ∃ path : Quiver.Path u v,
        Nonempty (NativeGK5CGConservativeFiveCell first last
          (fivefoldEvaluateP77 f g h k path) (left i))))
    (hR :
      (∀ j j' : J,
        Nonempty (NativeGK5CGConservativeFiveCell first last
          (right j) (right j'))) ∧
      (∃ j : J, ∃ path : Quiver.Path v w,
        Nonempty (NativeGK5CGConservativeFiveCell first last
          (fivefoldEvaluateP77 f g h k path) (right j)))) :
    ∃! pair : Quiver.Path u v × Quiver.Path v w,
      (∀ i : I, (fivefoldP77ConservativeFunctor f g h k).map pair.1 =
        fivefoldP77ConservativeClass f g h k (left i)) ∧
      (∀ j : J, (fivefoldP77ConservativeFunctor f g h k).map pair.2 =
        fivefoldP77ConservativeClass f g h k (right j)) := by
  letI := fivefoldP77ConservativeCategory f g h k
  obtain ⟨pathL, hpathL, huniqueL⟩ :=
    fivefoldP77LocalTypeDescent_unique f g h k left hL.1 hL.2
  obtain ⟨pathR, hpathR, huniqueR⟩ :=
    fivefoldP77LocalTypeDescent_unique f g h k right hR.1 hR.2
  refine ⟨(pathL, pathR), ⟨hpathL, hpathR⟩, ?_⟩
  rintro ⟨otherL, otherR⟩ ⟨hotherL, hotherR⟩
  have hl : otherL = pathL := huniqueL otherL hotherL
  have hr : otherR = pathR := huniqueR otherR hotherR
  cases hl
  cases hr
  rfl

/-- Actual ORIGINAL P77 target quotient composition of any
two certified segment paths equals the source functor evaluated
at their typed composite, simultaneously at every patch pair. -/
theorem fivefoldP77TwoPatch_composition_evaluates
    {u v w : FivefoldPathVertex} {I J : Type}
    (left : I → FivefoldP77LocalRaw f g h k u v)
    (right : J → FivefoldP77LocalRaw f g h k v w)
    (pathL : Quiver.Path u v) (pathR : Quiver.Path v w)
    (hL : ∀ i : I, (fivefoldP77ConservativeFunctor f g h k).map pathL =
      fivefoldP77ConservativeClass f g h k (left i))
    (hR : ∀ j : J, (fivefoldP77ConservativeFunctor f g h k).map pathR =
      fivefoldP77ConservativeClass f g h k (right j)) :
    ∀ (i : I) (j : J),
      (fivefoldP77ConservativeFunctor f g h k).map
        (pathL.comp pathR) =
      fivefoldP77ConservativeCompose f g h k
        (fivefoldP77ConservativeClass f g h k (left i))
        (fivefoldP77ConservativeClass f g h k (right j)) := by
  letI := fivefoldP77ConservativeCategory f g h k
  intro i j
  calc
    (fivefoldP77ConservativeFunctor f g h k).map
        (pathL.comp pathR) =
        (fivefoldP77ConservativeFunctor f g h k).map pathL ≫
          (fivefoldP77ConservativeFunctor f g h k).map pathR :=
      (fivefoldP77ConservativeFunctor f g h k).map_comp pathL pathR
    _ = fivefoldP77ConservativeCompose f g h k
          (fivefoldP77ConservativeClass f g h k (left i))
          (fivefoldP77ConservativeClass f g h k (right j)) := by
      rw [hL i, hR j]
      rfl

/-- The REAL composite of arbitrary original typed finite source
paths belongs to the genuinely source-reachable P77 partial
domain, irrespective of how patches were presented. -/
def fivefoldP77TwoPatchCertifiedComposite
    {u v w : FivefoldPathVertex}
    (pathL : Quiver.Path u v) (pathR : Quiver.Path v w) :
    FivefoldP77PartialDomain f g h k u w := by
  letI := fivefoldP77ConservativeCategory f g h k
  letI := fivefoldP77ImageCategory f g h k
  exact (fivefoldP77ImageFactor f g h k).map (pathL.comp pathR)

/-- Certified partial domain preserves the exact original P77
vertical quotient value at every left/right raw patch pair. -/
theorem fivefoldP77TwoPatchCertifiedComposite_val
    {u v w : FivefoldPathVertex} {I J : Type}
    (left : I → FivefoldP77LocalRaw f g h k u v)
    (right : J → FivefoldP77LocalRaw f g h k v w)
    (pathL : Quiver.Path u v) (pathR : Quiver.Path v w)
    (hL : ∀ i : I, (fivefoldP77ConservativeFunctor f g h k).map pathL =
      fivefoldP77ConservativeClass f g h k (left i))
    (hR : ∀ j : J, (fivefoldP77ConservativeFunctor f g h k).map pathR =
      fivefoldP77ConservativeClass f g h k (right j)) :
    ∀ (i : I) (j : J),
      (fivefoldP77TwoPatchCertifiedComposite f g h k pathL pathR).val =
        fivefoldP77ConservativeCompose f g h k
          (fivefoldP77ConservativeClass f g h k (left i))
          (fivefoldP77ConservativeClass f g h k (right j)) := by
  letI := fivefoldP77ConservativeCategory f g h k
  letI := fivefoldP77ImageCategory f g h k
  intro i j
  change (fivefoldP77ConservativeFunctor f g h k).map
    (pathL.comp pathR) =
      fivefoldP77ConservativeCompose f g h k
        (fivefoldP77ConservativeClass f g h k (left i))
        (fivefoldP77ConservativeClass f g h k (right j))
  exact fivefoldP77TwoPatch_composition_evaluates
    f g h k left right pathL pathR hL hR i j

/-- Recovering the certified composite gives the EXACT original
concatenation of both source finite paths, not its charge or a
choice-dependent merely isomorphic path. -/
theorem fivefoldP77TwoPatchCertifiedComposite_recover
    {u v w : FivefoldPathVertex}
    (pathL : Quiver.Path u v) (pathR : Quiver.Path v w) :
    fivefoldP77PartialRecoverPath f g h k
      (fivefoldP77TwoPatchCertifiedComposite f g h k pathL pathR) =
        pathL.comp pathR := by
  letI := fivefoldP77ConservativeCategory f g h k
  letI := fivefoldP77ImageCategory f g h k
  change fivefoldP77PartialRecoverPath f g h k
    ((fivefoldP77ImageFactor f g h k).map (pathL.comp pathR)) =
      pathL.comp pathR
  exact fivefoldP77PartialRecoverPath_of_factor f g h k
    (pathL.comp pathR)

/-- The original GK5CG charge of this actual certified
composition is exactly the LENGTH of its whole source path;
this observer does not determine target-image membership. -/
theorem fivefoldP77TwoPatchCertifiedComposite_charge_length
    {u v w : FivefoldPathVertex}
    (pathL : Quiver.Path u v) (pathR : Quiver.Path v w) :
    fivefoldP77ConservativeCharge f g h k
      (fivefoldP77TwoPatchCertifiedComposite f g h k pathL pathR).val =
        ((pathL.comp pathR).length : ℤ) := by
  letI := fivefoldP77ConservativeCategory f g h k
  calc
    fivefoldP77ConservativeCharge f g h k
        (fivefoldP77TwoPatchCertifiedComposite f g h k pathL pathR).val =
      ((fivefoldP77PartialRecoverPath f g h k
        (fivefoldP77TwoPatchCertifiedComposite f g h k pathL pathR)).length : ℤ) :=
      fivefoldP77PartialRecoverPath_charge_length
        f g h k (fivefoldP77TwoPatchCertifiedComposite f g h k pathL pathR)
    _ = ((pathL.comp pathR).length : ℤ) := by
      rw [fivefoldP77TwoPatchCertifiedComposite_recover]

/-- Original Type-valued local compatibility of two patch families
constructs a true certified original P77 composite for EVERY pair
of patches. The witness is an ACTUAL source path pair. -/
theorem fivefoldP77TwoPatchDescent_composite_exists
    {u v w : FivefoldPathVertex} {I J : Type} [Nonempty I] [Nonempty J]
    (left : I → FivefoldP77LocalRaw f g h k u v)
    (right : J → FivefoldP77LocalRaw f g h k v w)
    (hL :
      (∀ i i' : I,
        Nonempty (NativeGK5CGConservativeFiveCell first last
          (left i) (left i'))) ∧
      (∃ i : I, ∃ path : Quiver.Path u v,
        Nonempty (NativeGK5CGConservativeFiveCell first last
          (fivefoldEvaluateP77 f g h k path) (left i))))
    (hR :
      (∀ j j' : J,
        Nonempty (NativeGK5CGConservativeFiveCell first last
          (right j) (right j'))) ∧
      (∃ j : J, ∃ path : Quiver.Path v w,
        Nonempty (NativeGK5CGConservativeFiveCell first last
          (fivefoldEvaluateP77 f g h k path) (right j)))) :
    ∃ (pathL : Quiver.Path u v) (pathR : Quiver.Path v w),
      ∀ (i : I) (j : J),
        (fivefoldP77TwoPatchCertifiedComposite f g h k pathL pathR).val =
        fivefoldP77ConservativeCompose f g h k
          (fivefoldP77ConservativeClass f g h k (left i))
          (fivefoldP77ConservativeClass f g h k (right j)) := by
  letI := fivefoldP77ConservativeCategory f g h k
  obtain ⟨⟨pathL, pathR⟩, hpL, hpR⟩ :=
    (fivefoldP77TwoPatchLocalDescent_iff f g h k left right).2
      ⟨hL, hR⟩
  exact ⟨pathL, pathR,
    fivefoldP77TwoPatchCertifiedComposite_val
      f g h k left right pathL pathR hpL hpR⟩

/-- A patch lacking ALL original source-evaluation Type-valued
five-cell witnesses obstructs the segmentwise TWO-PATCH descent.
This does NOT imply that an unrelated whole-target composite
cannot be recovered by some other factorization. -/
theorem fivefoldP77TwoPatch_leftTypeGap_blocks_factorization
    {u v w : FivefoldPathVertex} {I J : Type}
    (left : I → FivefoldP77LocalRaw f g h k u v)
    (right : J → FivefoldP77LocalRaw f g h k v w)
    (i₀ : I)
    (hmissing : ∀ path : Quiver.Path u v,
      ¬ Nonempty (NativeGK5CGConservativeFiveCell first last
        (fivefoldEvaluateP77 f g h k path) (left i₀))) :
    ¬ ∃ pair : Quiver.Path u v × Quiver.Path v w,
      (∀ i : I, (fivefoldP77ConservativeFunctor f g h k).map pair.1 =
        fivefoldP77ConservativeClass f g h k (left i)) ∧
      (∀ j : J, (fivefoldP77ConservativeFunctor f g h k).map pair.2 =
        fivefoldP77ConservativeClass f g h k (right j)) := by
  letI := fivefoldP77ConservativeCategory f g h k
  rintro ⟨⟨pathL, _⟩, hL, _⟩
  have hreach : fivefoldP77ConservativeReachable f g h k
      (fivefoldP77ConservativeClass f g h k (left i₀)) :=
    ⟨pathL, hL i₀⟩
  obtain ⟨path, hcert⟩ :=
    (fivefoldP77ConservativeClass_reachable_iff
      f g h k (left i₀)).1 hreach
  exact hmissing path hcert

/-- Charge ZERO cannot rescue a genuinely missing original P77
reverse-plus-pentagon segment at the source phase boundary 1→0,
even if ANY second family of target raw four-proofs is supplied.
This is an obstruction to the specified FACTORWISE descent only. -/
theorem fivefoldP77TwoPatch_zeroReverse_blocks_first_segment
    {w : FivefoldPathVertex} {I J : Type}
    (left : I → FivefoldP77LocalRaw f g h k
      (fivefoldPathVertex 1) (fivefoldPathVertex 0))
    (right : J → FivefoldP77LocalRaw f g h k (fivefoldPathVertex 0) w)
    (i₀ : I)
    (hzero : fivefoldP77ConservativeClass f g h k (left i₀) =
      fivefoldP77OriginalZeroChargeReverse01 f g h k) :
    ¬ ∃ pair :
      Quiver.Path (fivefoldPathVertex 1) (fivefoldPathVertex 0) ×
        Quiver.Path (fivefoldPathVertex 0) w,
      (∀ i : I, (fivefoldP77ConservativeFunctor f g h k).map pair.1 =
        fivefoldP77ConservativeClass f g h k (left i)) ∧
      (∀ j : J, (fivefoldP77ConservativeFunctor f g h k).map pair.2 =
        fivefoldP77ConservativeClass f g h k (right j)) := by
  letI := fivefoldP77ConservativeCategory f g h k
  rintro ⟨⟨pathL, _⟩, hL, _⟩
  exact fivefoldP77OriginalZeroChargeReverse01_not_reachable f g h k
    ⟨pathL, (hL i₀).trans hzero⟩

#print axioms fivefoldP77TwoPatchLocalDescent_iff
#print axioms fivefoldP77TwoPatchLocalDescent_unique
#print axioms fivefoldP77TwoPatch_composition_evaluates
#print axioms fivefoldP77TwoPatchCertifiedComposite
#print axioms fivefoldP77TwoPatchCertifiedComposite_val
#print axioms fivefoldP77TwoPatchCertifiedComposite_recover
#print axioms fivefoldP77TwoPatchCertifiedComposite_charge_length
#print axioms fivefoldP77TwoPatchDescent_composite_exists
#print axioms fivefoldP77TwoPatch_leftTypeGap_blocks_factorization
#print axioms fivefoldP77TwoPatch_zeroReverse_blocks_first_segment

end
end KUOS.Architecture.WuxingPentagonUnified
