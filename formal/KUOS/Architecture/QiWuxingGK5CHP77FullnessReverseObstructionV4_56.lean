import KUOS.Architecture.QiWuxingGK5CHFivefoldFinitePathFaithfulV4_55
import Mathlib.CategoryTheory.Functor.FullyFaithful
import Mathlib.Tactic

/-!
Qi v4.56 — EXACT ORIGINAL P77 FULLNESS CRITERION AND
UNCONDITIONAL REVERSE-ARROW OBSTRUCTION.

Qi v4.55 proves that the genuine directed FivefoldEdge free-path
functor into the ORIGINAL P77 four-proof / conservative five-cell
quotient is FAITHFUL. Here we separate fullness from faithfulness.

The source quiver has five directed edges e01, e12, e23, e04, e43.
The target's Hom consists of ORIGINAL dependently typed P77
four-proof syntax modulo existence of GK5CG conservative Type-valued
five-cell witnesses, not merely integer-charge equality.

We prove:
- A target quotient class is in the image precisely when some
  genuinely typed finite source path carries a genuine conservative
  five-cell comparison to its original P77 representative.
- The genuine Mathlib Functor is Full IFF ALL original target P77
  four-proofs admit such exact five-cell certified finite paths.
- The original P77 inverse of e01 exists as a target arrow 1->0.
  Its signed original associator charge is -1, and this charge
  descends through the conservative source five-cell quotient.
- Every source free-path image has charge = Nat path length >= 0.
  Therefore the actual inverse e01 target arrow has NO preimage,
  and the genuine functor is UNCONDITIONALLY NOT FULL.
- Thus the same honest functor is FAITHFUL but NOT FULL.
  No essential surjectivity of Hom maps or fully-faithfulness
  is fabricated. This is a structural oriented arrow obstruction
  in the actual original proof-valued target, not a numeric
  kernel quotient and not an adjoined historical pentagonator.

The original F54/F55/P77/P94A evidence, numerical signed CRT,
physical C60 edge/Dart data, and Qi v3.1 generation/control quiver
remain in their own independent authorities.

Append-only, same-root, public root107. Lean v4.30.0-rc2,
mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Strict 空 center; independent Kuu one presentation.
Protected #1558 Draft/open/unmerged; no sorry/admit/new axioms/Gray.
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

/-- A genuine target class is source reachable only when it is the
image of a genuinely typed finite fivefold free path. -/
def fivefoldP77ConservativeReachable
    {u v : FivefoldPathVertex}
    (z : FivefoldP77ConservativeClasses f g h k u v) : Prop :=
  ∃ path : Quiver.Path u v,
    (fivefoldP77ConservativeFunctor f g h k).map path = z

/-- Exact source Type-valued five-cell criterion for reachability
of a concrete ORIGINAL P77 four-proof representative. Neither
signed charge nor a numerical CRT equality defines this relation. -/
theorem fivefoldP77ConservativeClass_reachable_iff
    {u v : FivefoldPathVertex}
    (w : NativeF55RawVerticalFourCell first last
      (fivefoldF55OriginalAt f g h k u.phase)
      (fivefoldF55OriginalAt f g h k v.phase)) :
    fivefoldP77ConservativeReachable f g h k
      (fivefoldP77ConservativeClass f g h k w) ↔
    ∃ path : Quiver.Path u v,
      Nonempty (NativeGK5CGConservativeFiveCell first last
        (fivefoldEvaluateP77 f g h k path) w) := by
  letI := fivefoldP77ConservativeCategory f g h k
  constructor
  · rintro ⟨path, hmap⟩
    refine ⟨path, ?_⟩
    rw [fivefoldP77ConservativeFunctor_map_spec] at hmap
    exact (fivefoldP77ConservativeClass_eq_iff f g h k _ _).mp hmap
  · rintro ⟨path, hcert⟩
    refine ⟨path, ?_⟩
    rw [fivefoldP77ConservativeFunctor_map_spec]
    exact (fivefoldP77ConservativeClass_eq_iff f g h k _ _).mpr hcert

/-- Exact necessary-and-sufficient FULLNESS condition for the
ACTUAL P77 category functor, quantified over EVERY dependent
original four-proof target representative at EVERY typed endpoint.
In particular, the RHS requires real source five-cell evidence. -/
theorem fivefoldP77ConservativeFunctor_full_iff_originalReachable :
    (fivefoldP77ConservativeFunctor f g h k).Full ↔
      (∀ (u v : FivefoldPathVertex)
        (w : NativeF55RawVerticalFourCell first last
          (fivefoldF55OriginalAt f g h k u.phase)
          (fivefoldF55OriginalAt f g h k v.phase)),
        ∃ path : Quiver.Path u v,
          Nonempty (NativeGK5CGConservativeFiveCell first last
            (fivefoldEvaluateP77 f g h k path) w)) := by
  letI := fivefoldP77ConservativeCategory f g h k
  constructor
  · intro hfull u v w
    haveI : (fivefoldP77ConservativeFunctor f g h k).Full := hfull
    obtain ⟨path, hmap⟩ :=
      (fivefoldP77ConservativeFunctor f g h k).map_surjective
        (fivefoldP77ConservativeClass f g h k w)
    refine ⟨path, ?_⟩
    rw [fivefoldP77ConservativeFunctor_map_spec] at hmap
    exact (fivefoldP77ConservativeClass_eq_iff f g h k _ _).mp hmap
  · intro hreach
    constructor
    intro X Y z
    rcases X with ⟨u⟩
    rcases Y with ⟨v⟩
    refine _root_.Quotient.inductionOn z (fun w => ?_)
    obtain ⟨path, hcert⟩ := hreach ⟨u⟩ ⟨v⟩ w
    refine ⟨path, ?_⟩
    rw [fivefoldP77ConservativeFunctor_map_spec]
    exact (fivefoldP77ConservativeClass_eq_iff f g h k _ _).mpr hcert

/-- Every target P77 class with STRICTLY NEGATIVE original
associator charge is outside the image of the genuine fivefold
functor. All input free paths have nonnegative Nat length. -/
theorem fivefoldP77Conservative_negativeCharge_not_reachable
    {u v : FivefoldPathVertex}
    (z : FivefoldP77ConservativeClasses f g h k u v)
    (hz : fivefoldP77ConservativeCharge f g h k z < 0) :
    ¬ fivefoldP77ConservativeReachable f g h k z := by
  letI := fivefoldP77ConservativeCategory f g h k
  rintro ⟨path, hmap⟩
  have hcharge := congrArg
    (fivefoldP77ConservativeCharge f g h k) hmap
  rw [fivefoldP77ConservativeFunctor_charge_length] at hcharge
  have hnegative : (path.length : ℤ) < 0 :=
    lt_of_eq_of_lt hcharge hz
  exact (not_lt_of_ge (Int.natCast_nonneg _)) hnegative

/-- ACTUAL target original P77 inverse arrow, with exact dependent
original F55/P77 source 1 and target 0. The inverse is a source
P77 symm constructor, NOT a reverse edge in the free quiver. -/
def fivefoldP77OriginalReverse01 :
    FivefoldP77ConservativeClasses f g h k
      (fivefoldPathVertex 1) (fivefoldPathVertex 0) :=
  fivefoldP77ConservativeClass f g h k
    (NativeF55RawVerticalFourCell.symm
      (fivefoldArrowOriginalP77 f g h k
        (fivefoldPathArrowOf .e01)))

/-- The real original reverse 01 four-proof has signed associator
charge -1 in the conservative quotient, by original GK5CG symm
and Qi v4.53's charge +1 for all directed actual generators. -/
theorem fivefoldP77OriginalReverse01_charge :
    fivefoldP77ConservativeCharge f g h k
      (fivefoldP77OriginalReverse01 f g h k) = -1 := by
  change
    -(fivefoldArrowOriginalP77 f g h k
      (fivefoldPathArrowOf .e01)).gk5cgAssocCharge = (-1 : ℤ)
  rw [fivefoldArrowOriginalP77_charge_one]

/-- A concrete genuine ORIGINAL P77 target four-proof class with
no preimage at the real reverse phase boundary 1 -> 0.
The source direction is fixed; the target inverse is real. -/
theorem fivefoldP77OriginalReverse01_not_reachable :
    ¬ fivefoldP77ConservativeReachable f g h k
      (fivefoldP77OriginalReverse01 f g h k) := by
  apply fivefoldP77Conservative_negativeCharge_not_reachable f g h k _
  rw [fivefoldP77OriginalReverse01_charge]
  norm_num

/-- The source-fullness obstruction is visible already at the
genuine original Type-valued conservative five-cell certificate
level, without conflating equality of numerical charges with
the existence of source higher evidence. -/
theorem fivefoldP77OriginalReverse01_noSourceFiveCell
    (path : Quiver.Path (fivefoldPathVertex 1) (fivefoldPathVertex 0)) :
    ¬ Nonempty (NativeGK5CGConservativeFiveCell first last
      (fivefoldEvaluateP77 f g h k path)
      (NativeF55RawVerticalFourCell.symm
        (fivefoldArrowOriginalP77 f g h k
          (fivefoldPathArrowOf .e01)))) := by
  intro witness
  apply fivefoldP77OriginalReverse01_not_reachable f g h k
  apply (fivefoldP77ConservativeClass_reachable_iff
    f g h k _).2
  exact ⟨path, witness⟩

/-- The actual Qi v4.54 source-preserving target Category Functor
is NOT FULL, for all genuinely composable original F55 4-tuples.
Even one reverse ORIGINAL P77 four-proof class is not reachable
by the directed five-edge free path presentation. -/
theorem fivefoldP77ConservativeFunctor_not_full :
    ¬ (fivefoldP77ConservativeFunctor f g h k).Full := by
  letI := fivefoldP77ConservativeCategory f g h k
  intro hfull
  haveI : (fivefoldP77ConservativeFunctor f g h k).Full := hfull
  obtain ⟨path, hmap⟩ :=
    (fivefoldP77ConservativeFunctor f g h k).map_surjective
      (fivefoldP77OriginalReverse01 f g h k)
  exact fivefoldP77OriginalReverse01_not_reachable f g h k
    ⟨path, hmap⟩

/-- Exact split of the Mathlib FULL / FAITHFUL properties on the
actual original fivefold P77 quotient functor. Faithfulness was
proved unconditionally in Qi v4.55; fullness is now refuted by
the original reverse 01 P77 four-proof. -/
theorem fivefoldP77ConservativeFunctor_faithful_and_not_full :
    (fivefoldP77ConservativeFunctor f g h k).Faithful ∧
      ¬ (fivefoldP77ConservativeFunctor f g h k).Full :=
  ⟨fivefoldP77ConservativeFunctor_faithful_genuine f g h k,
   fivefoldP77ConservativeFunctor_not_full f g h k⟩

#print axioms fivefoldP77ConservativeReachable
#print axioms fivefoldP77ConservativeClass_reachable_iff
#print axioms fivefoldP77ConservativeFunctor_full_iff_originalReachable
#print axioms fivefoldP77Conservative_negativeCharge_not_reachable
#print axioms fivefoldP77OriginalReverse01
#print axioms fivefoldP77OriginalReverse01_charge
#print axioms fivefoldP77OriginalReverse01_not_reachable
#print axioms fivefoldP77OriginalReverse01_noSourceFiveCell
#print axioms fivefoldP77ConservativeFunctor_not_full
#print axioms fivefoldP77ConservativeFunctor_faithful_and_not_full

end
end KUOS.Architecture.WuxingPentagonUnified
