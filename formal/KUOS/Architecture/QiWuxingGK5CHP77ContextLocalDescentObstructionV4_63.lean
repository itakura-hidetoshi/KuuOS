import KUOS.Architecture.QiWuxingGK5CHP77TriangleCompatiblePartialRecoveryV4_62
import Mathlib.Combinatorics.Quiver.Path
import Mathlib.CategoryTheory.Equivalence
import Mathlib.Tactic

/-!
Qi v4.63 — ORIGINAL P77 CONTEXT NATURALITY, LOCAL TYPE-VALUED DESCENT,
AND CHARGE-VERSUS-EVIDENCE OBSTRUCTION SEPARATION.

Keep distinct (1) the original directed FivefoldEdge free paths,
(2) ORIGINAL F55/P77 conservative four-proof quotient Homs, and
(3) the actual source-reachable Type-valued P77 sub-Homs.

The v4.62 partial normalizer is natural under genuine source
pre/postcomposition: its recovered path is exactly the whiskered
original source path. Reachability also survives actual P77 context
composition; NO reflection from a composite is asserted.

NEW LOCAL DESCENT. At fixed ORIGINAL typed endpoints, a nonempty
family of actual raw F55/P77 four-proofs glues to ONE original
finite path precisely when every pair is related by a true GK5CG
conservative Type-valued five-cell and ONE patch has a genuine
source-to-patch Type-valued five-cell. The descended typed path is
UNIQUE by original P77 faithfulness. Numerical charge cannot
substitute for either certificate, and no unproved sheaf/localization
or geometric cover is claimed. The patches are a Hom-wise cover
with EXACT overlapping original five-cell equality.

Separate visible signed-charge-out-of-range failure from
charge-admissible, source-five-cell failure. In particular original
negative reverse 01 is charge-detected, while the different actual
zero-charge reverse-plus-pentagon original P77 class is NOT.
No full-target typed recovery or new reverse source edge.

Append-only, same-root, root107, strict 空 central; independent Kuu
one presentation. Genuine F55/P77/P94A, C60 gauge and CRT
remain independent proof authorities. No pentagonator, Gray,
new axioms, sorry, admit or native_decide.
Lean v4.30.0-rc2; pinned mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Validation-only #1558 stays Draft/open/unmerged.
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

/-- Exact left-context naturality of the partial ORIGINAL P77
typed normalizer, with a genuine source pre. -/
theorem fivefoldP77PartialRecovery_left_context
    {s u v : FivefoldPathVertex}
    (pre : Quiver.Path s u)
    (A : FivefoldP77PartialDomain f g h k u v) :
    fivefoldP77PartialRecoverPath f g h k
      (fivefoldP77ImageComp f g h k
        ((fivefoldP77ImageFactor f g h k).map pre) A) =
      pre.comp (fivefoldP77PartialRecoverPath f g h k A) := by
  letI := fivefoldP77ConservativeCategory f g h k
  letI := fivefoldP77ImageCategory f g h k
  rw [fivefoldP77PartialRecoverPath_comp f g h k,
    fivefoldP77PartialRecoverPath_of_factor f g h k pre]
  rfl

/-- Exact right-context naturality under a genuine source suffix. -/
theorem fivefoldP77PartialRecovery_right_context
    {u v t : FivefoldPathVertex}
    (A : FivefoldP77PartialDomain f g h k u v)
    (suffix : Quiver.Path v t) :
    fivefoldP77PartialRecoverPath f g h k
      (fivefoldP77ImageComp f g h k A
        ((fivefoldP77ImageFactor f g h k).map suffix)) =
      (fivefoldP77PartialRecoverPath f g h k A).comp suffix := by
  letI := fivefoldP77ConservativeCategory f g h k
  letI := fivefoldP77ImageCategory f g h k
  have hs :
      fivefoldP77PartialRecoverPath f g h k
        ((fivefoldP77ImageFactor f g h k).map suffix) = suffix :=
    fivefoldP77PartialRecoverPath_of_factor f g h k suffix
  calc
    fivefoldP77PartialRecoverPath f g h k
        (fivefoldP77ImageComp f g h k A
          ((fivefoldP77ImageFactor f g h k).map suffix)) =
      (fivefoldP77PartialRecoverPath f g h k A).comp
        (fivefoldP77PartialRecoverPath f g h k
          ((fivefoldP77ImageFactor f g h k).map suffix)) :=
      fivefoldP77PartialRecoverPath_comp f g h k _ _
    _ = (fivefoldP77PartialRecoverPath f g h k A).comp suffix :=
      congrArg
        (fun q : Quiver.Path v t =>
          (fivefoldP77PartialRecoverPath f g h k A).comp q) hs

/-- Two-sided context naturality ON the actual certified partial
Hom, retaining actual typed endpoints and original paths. -/
theorem fivefoldP77PartialRecovery_both_contexts
    {s u v t : FivefoldPathVertex}
    (pre : Quiver.Path s u)
    (A : FivefoldP77PartialDomain f g h k u v)
    (suffix : Quiver.Path v t) :
    fivefoldP77PartialRecoverPath f g h k
      (fivefoldP77ImageComp f g h k
        (fivefoldP77ImageComp f g h k
          ((fivefoldP77ImageFactor f g h k).map pre) A)
        ((fivefoldP77ImageFactor f g h k).map suffix)) =
      (pre.comp (fivefoldP77PartialRecoverPath f g h k A)).comp
        suffix := by
  letI := fivefoldP77ConservativeCategory f g h k
  letI := fivefoldP77ImageCategory f g h k
  have hleft := fivefoldP77PartialRecovery_left_context f g h k pre A
  have hright :
      fivefoldP77PartialRecoverPath f g h k
        ((fivefoldP77ImageFactor f g h k).map suffix) = suffix :=
    fivefoldP77PartialRecoverPath_of_factor f g h k suffix
  calc
    fivefoldP77PartialRecoverPath f g h k
        (fivefoldP77ImageComp f g h k
          (fivefoldP77ImageComp f g h k
            ((fivefoldP77ImageFactor f g h k).map pre) A)
          ((fivefoldP77ImageFactor f g h k).map suffix)) =
      (fivefoldP77PartialRecoverPath f g h k
        (fivefoldP77ImageComp f g h k
          ((fivefoldP77ImageFactor f g h k).map pre) A)).comp
        (fivefoldP77PartialRecoverPath f g h k
          ((fivefoldP77ImageFactor f g h k).map suffix)) :=
      fivefoldP77PartialRecoverPath_comp f g h k _ _
    _ = (pre.comp (fivefoldP77PartialRecoverPath f g h k A)).comp
          (fivefoldP77PartialRecoverPath f g h k
            ((fivefoldP77ImageFactor f g h k).map suffix)) :=
      congrArg
        (fun q : Quiver.Path s v =>
          q.comp (fivefoldP77PartialRecoverPath f g h k
            ((fivefoldP77ImageFactor f g h k).map suffix))) hleft
    _ = (pre.comp (fivefoldP77PartialRecoverPath f g h k A)).comp
          suffix :=
      congrArg
        (fun q : Quiver.Path v t =>
          (pre.comp (fivefoldP77PartialRecoverPath f g h k A)).comp q)
        hright

/-- Source-certified original target quotient Homs stay certified
under BOTH genuine typed source contexts. No converse/cancellation
of unreachability is inferred from a reachable composite. -/
theorem fivefoldP77OriginalContext_reachable
    {s u v t : FivefoldPathVertex}
    (pre : Quiver.Path s u)
    (z : FivefoldP77ConservativeClasses f g h k u v)
    (suffix : Quiver.Path v t)
    (hz : fivefoldP77ConservativeReachable f g h k z) :
    fivefoldP77ConservativeReachable f g h k
      (fivefoldP77ConservativeCompose f g h k
        (fivefoldP77ConservativeCompose f g h k
          ((fivefoldP77ConservativeFunctor f g h k).map pre) z)
        ((fivefoldP77ConservativeFunctor f g h k).map suffix)) := by
  letI := fivefoldP77ConservativeCategory f g h k
  obtain ⟨path, hpath⟩ := hz
  refine ⟨(pre.comp path).comp suffix, ?_⟩
  calc
    (fivefoldP77ConservativeFunctor f g h k).map
        ((pre.comp path).comp suffix) =
      (fivefoldP77ConservativeFunctor f g h k).map
          (pre.comp path) ≫
        (fivefoldP77ConservativeFunctor f g h k).map suffix :=
      (fivefoldP77ConservativeFunctor f g h k).map_comp _ _
    _ = ((fivefoldP77ConservativeFunctor f g h k).map pre ≫
          (fivefoldP77ConservativeFunctor f g h k).map path) ≫
        (fivefoldP77ConservativeFunctor f g h k).map suffix := by
      exact (fivefoldP77ConservativeFunctor f g h k).map_comp pre path
    _ = fivefoldP77ConservativeCompose f g h k
        (fivefoldP77ConservativeCompose f g h k
          ((fivefoldP77ConservativeFunctor f g h k).map pre) z)
        ((fivefoldP77ConservativeFunctor f g h k).map suffix) := by
      rw [hpath]
      rfl

/-- If a particular genuine source context has a missing
composite, the middle original class was already missing. This
is the valid contrapositive of closure, not cancellation. -/
theorem fivefoldP77OriginalContext_missing_reflects
    {s u v t : FivefoldPathVertex}
    (pre : Quiver.Path s u)
    (z : FivefoldP77ConservativeClasses f g h k u v)
    (suffix : Quiver.Path v t)
    (hnot : ¬ fivefoldP77ConservativeReachable f g h k
      (fivefoldP77ConservativeCompose f g h k
        (fivefoldP77ConservativeCompose f g h k
          ((fivefoldP77ConservativeFunctor f g h k).map pre) z)
        ((fivefoldP77ConservativeFunctor f g h k).map suffix))) :
    ¬ fivefoldP77ConservativeReachable f g h k z := by
  intro hz
  exact hnot (fivefoldP77OriginalContext_reachable
    f g h k pre z suffix hz)

/-- Actual source-original F55/P77 four-proof data for local
patches at the SAME genuinely typed endpoints. -/
abbrev FivefoldP77LocalRaw (u v : FivefoldPathVertex) :=
  NativeF55RawVerticalFourCell first last
    (fivefoldF55OriginalAt f g h k u.phase)
    (fivefoldF55OriginalAt f g h k v.phase)

/-- EXACT local descent criterion: a NONEMPTY indexed family of
raw original P77 four-proofs descends to ONE source typed path IFF
(1) all pairs agree by original GK5CG Type-valued conservative
five-cell, and (2) at least ONE patch has a true source path
evaluation-to-raw Type-valued five-cell.

This is not an abstract unverified Grothendieck cover or a
charge-only descent criterion. Quotient equality is witnessed by
the actual original five-cell relation. -/
theorem fivefoldP77LocalTypeDescent_iff
    {u v : FivefoldPathVertex} {I : Type} [Nonempty I]
    (raw : I → FivefoldP77LocalRaw f g h k u v) :
    (∃ path : Quiver.Path u v,
      ∀ i : I,
        (fivefoldP77ConservativeFunctor f g h k).map path =
          fivefoldP77ConservativeClass f g h k (raw i)) ↔
    ((∀ i j : I,
        Nonempty (NativeGK5CGConservativeFiveCell first last
          (raw i) (raw j))) ∧
      (∃ i : I, ∃ path : Quiver.Path u v,
        Nonempty (NativeGK5CGConservativeFiveCell first last
          (fivefoldEvaluateP77 f g h k path) (raw i)))) := by
  letI := fivefoldP77ConservativeCategory f g h k
  constructor
  · rintro ⟨path, hpath⟩
    constructor
    · intro i j
      apply (fivefoldP77ConservativeClass_eq_iff
        f g h k (raw i) (raw j)).1
      exact (hpath i).symm.trans (hpath j)
    · let i₀ : I := Classical.choice (inferInstance : Nonempty I)
      refine ⟨i₀, path, ?_⟩
      apply (fivefoldP77ConservativeClass_eq_iff
        f g h k (fivefoldEvaluateP77 f g h k path) (raw i₀)).1
      exact (fivefoldP77ConservativeFunctor_map_spec
        f g h k path).symm.trans (hpath i₀)
  · rintro ⟨hoverlap, ⟨i₀, path, hlocal⟩⟩
    refine ⟨path, ?_⟩
    intro i
    calc
      (fivefoldP77ConservativeFunctor f g h k).map path =
          fivefoldP77ConservativeClass f g h k
            (fivefoldEvaluateP77 f g h k path) :=
        fivefoldP77ConservativeFunctor_map_spec f g h k path
      _ = fivefoldP77ConservativeClass f g h k (raw i₀) :=
        (fivefoldP77ConservativeClass_eq_iff f g h k
          (fivefoldEvaluateP77 f g h k path) (raw i₀)).2 hlocal
      _ = fivefoldP77ConservativeClass f g h k (raw i) :=
        (fivefoldP77ConservativeClass_eq_iff f g h k
          (raw i₀) (raw i)).2 (hoverlap i₀ i)

/-- Effective Hom-wise gluing with UNIQUE genuinely typed original
source free path. Uses faithfulness of original P77 evidence map,
not charge-injectivity over the whole target. -/
theorem fivefoldP77LocalTypeDescent_unique
    {u v : FivefoldPathVertex} {I : Type} [Nonempty I]
    (raw : I → FivefoldP77LocalRaw f g h k u v)
    (hoverlap : ∀ i j : I,
      Nonempty (NativeGK5CGConservativeFiveCell first last
        (raw i) (raw j)))
    (hlocal : ∃ i : I, ∃ path : Quiver.Path u v,
      Nonempty (NativeGK5CGConservativeFiveCell first last
        (fivefoldEvaluateP77 f g h k path) (raw i))) :
    ∃! path : Quiver.Path u v,
      ∀ i : I,
        (fivefoldP77ConservativeFunctor f g h k).map path =
          fivefoldP77ConservativeClass f g h k (raw i) := by
  letI := fivefoldP77ConservativeCategory f g h k
  obtain ⟨path, hpath⟩ :=
    (fivefoldP77LocalTypeDescent_iff f g h k raw).2
      ⟨hoverlap, hlocal⟩
  refine ⟨path, hpath, ?_⟩
  intro other hother
  let i₀ : I := Classical.choice (inferInstance : Nonempty I)
  exact (fivefoldP77ConservativeFunctor_faithful_genuine
    f g h k).map_injective
      ((hother i₀).trans (hpath i₀).symm)

/-- Exhaustive separation of an original raw P77 four-proof's
failure of SOURCE recovery: either its genuine signed charge is
OUTSIDE the necessary [0,3] range, or charge is in range but
EVERY source-path-to-raw Type-valued five-cell is absent.
The latter does not follow from charge alone. -/
theorem fivefoldP77Obstruction_charge_or_type_gap
    {u v : FivefoldPathVertex}
    (w : FivefoldP77LocalRaw f g h k u v) :
    (¬ fivefoldP77ConservativeReachable f g h k
      (fivefoldP77ConservativeClass f g h k w)) ↔
    ((fivefoldP77ConservativeCharge f g h k
        (fivefoldP77ConservativeClass f g h k w) < 0 ∨
      (3 : ℤ) < fivefoldP77ConservativeCharge f g h k
        (fivefoldP77ConservativeClass f g h k w)) ∨
      (0 ≤ fivefoldP77ConservativeCharge f g h k
        (fivefoldP77ConservativeClass f g h k w) ∧
       fivefoldP77ConservativeCharge f g h k
        (fivefoldP77ConservativeClass f g h k w) ≤ (3 : ℤ) ∧
       ∀ path : Quiver.Path u v,
         ¬ Nonempty (NativeGK5CGConservativeFiveCell first last
           (fivefoldEvaluateP77 f g h k path) w))) := by
  constructor
  · intro hmissing
    by_cases hrange :
        0 ≤ fivefoldP77ConservativeCharge f g h k
          (fivefoldP77ConservativeClass f g h k w) ∧
        fivefoldP77ConservativeCharge f g h k
          (fivefoldP77ConservativeClass f g h k w) ≤ (3 : ℤ)
    · exact Or.inr ⟨hrange.1, hrange.2,
        (fivefoldP77OriginalClass_unreachable_iff_noSourceFiveCell
          f g h k w).1 hmissing⟩
    · left
      omega
  · intro hsplit
    rcases hsplit with hout | ⟨_, _, hno⟩
    · exact fivefoldP77_charge_out_of_range_not_reachable
        f g h k _ hout
    · exact (fivefoldP77OriginalClass_unreachable_iff_noSourceFiveCell
        f g h k w).2 hno

/-- Actual negative-charge ORIGINAL reverse e01 obstruction is
detected by the signed-charge range without making a reverse
edge in the source directed quiver. -/
theorem fivefoldP77Obstruction_negativeReverse_charge_detected :
    fivefoldP77ConservativeCharge f g h k
      (fivefoldP77OriginalReverse01 f g h k) < 0 := by
  rw [fivefoldP77OriginalReverse01_charge]
  norm_num

/-- The distinct ORIGINAL zero-charge reverse-plus-pentagon
class passes the necessary charge range, but not ONE source
typed finite path can evaluate to its original P77 quotient class.
Thus an admissible charge is not a Type-valued descent witness. -/
theorem fivefoldP77Obstruction_zeroReverse_charge_silent :
    (0 ≤ fivefoldP77ConservativeCharge f g h k
      (fivefoldP77OriginalZeroChargeReverse01 f g h k) ∧
      fivefoldP77ConservativeCharge f g h k
        (fivefoldP77OriginalZeroChargeReverse01 f g h k) ≤ (3 : ℤ)) ∧
    (∀ path : Quiver.Path (fivefoldPathVertex 1) (fivefoldPathVertex 0),
      (fivefoldP77ConservativeFunctor f g h k).map path ≠
        fivefoldP77OriginalZeroChargeReverse01 f g h k) := by
  constructor
  · rw [fivefoldP77OriginalZeroChargeReverse01_charge]
    norm_num
  · intro path heq
    exact fivefoldP77OriginalZeroChargeReverse01_not_reachable f g h k
      ⟨path, heq⟩

/-- The charge-visible obstruction and charge-silent original
Type-valued five-cell obstruction are distinct target Homs.
They do NOT together define a charge-only recovery procedure. -/
theorem fivefoldP77Obstruction_two_original_reverses_split :
    (fivefoldP77ConservativeCharge f g h k
      (fivefoldP77OriginalReverse01 f g h k) < 0) ∧
    (fivefoldP77ConservativeCharge f g h k
      (fivefoldP77OriginalZeroChargeReverse01 f g h k) = 0) ∧
    (fivefoldP77OriginalZeroChargeReverse01 f g h k ≠
      fivefoldP77OriginalReverse01 f g h k) ∧
    (¬ fivefoldP77ConservativeReachable f g h k
      (fivefoldP77OriginalZeroChargeReverse01 f g h k)) := by
  exact ⟨fivefoldP77Obstruction_negativeReverse_charge_detected f g h k,
    fivefoldP77OriginalZeroChargeReverse01_charge f g h k,
    fivefoldP77OriginalZeroReverse_ne_negativeReverse f g h k,
    fivefoldP77OriginalZeroChargeReverse01_not_reachable f g h k⟩

#print axioms fivefoldP77PartialRecovery_left_context
#print axioms fivefoldP77PartialRecovery_right_context
#print axioms fivefoldP77PartialRecovery_both_contexts
#print axioms fivefoldP77OriginalContext_reachable
#print axioms fivefoldP77OriginalContext_missing_reflects
#print axioms FivefoldP77LocalRaw
#print axioms fivefoldP77LocalTypeDescent_iff
#print axioms fivefoldP77LocalTypeDescent_unique
#print axioms fivefoldP77Obstruction_charge_or_type_gap
#print axioms fivefoldP77Obstruction_negativeReverse_charge_detected
#print axioms fivefoldP77Obstruction_zeroReverse_charge_silent
#print axioms fivefoldP77Obstruction_two_original_reverses_split

end
end KUOS.Architecture.WuxingPentagonUnified
