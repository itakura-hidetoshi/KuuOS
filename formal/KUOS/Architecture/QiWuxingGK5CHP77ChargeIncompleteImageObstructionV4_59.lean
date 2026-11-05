import KUOS.Architecture.QiWuxingGK5CHP77CertifiedImageEquivalenceV4_58
import Mathlib.CategoryTheory.Functor.FullyFaithful
import Mathlib.Tactic

/-!
Qi v4.59 — ORIGINAL P77 CERTIFIED IMAGE: CHARGE-INCOMPLETE HOM OBSTRUCTIONS.

We retain the true original F55/P77 dependent four-proof classes,
the GK5CG conservative Type-valued five-cell quotient, the genuine
five-edge source quiver and the actual Qi v4.57 fully faithful image.

The new theorem distinguishes three different questions:
1. Exact membership in the source-certified image is equivalent to
   existence of a typed original finite-path conservative five-cell.
2. Reachable target Homs have signed original charge in [0, 3],
   and the charge is injective only AFTER restricting to reachable
   classes at fixed typed endpoints.
3. Charge in [0, 3] is NOT sufficient: a genuine original P77 target
   Hom 1 -> 0 has charge ZERO but no oriented source path preimage.
   Its source is an original inverse e01 followed by the original
   upper/lower pentagon loop of charge +1. It is neither a fabricated
   original 5-cell nor a numerical proxy.

Any genuinely FULL extended source functor with objects over phases
1 and 0 must lift BOTH this zero-charge four-proof class and the
original charge -1 reverse proof class; these are distinct classes.
This is a necessary condition, not a construction of such an
extension or a claim of an original pentagonator.

Append-only, same-root, public root 107 unchanged. Strict 空 center;
independent Kuu is one presentation. The historical F55, P77, P94A
and genuine physical C60 sources remain separate and unmodified.
Pinned Lean v4.30.0-rc2, mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Validation-only #1558 Draft/open/unmerged. No new axioms,
sorry, admit, native_decide or Gray.
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

universe uD vD uE vE uS vS

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

/-- Exact image membership: an actual P77 quotient class lifts to the
wide image Category IFF it has a genuinely typed source path preimage. -/
theorem fivefoldP77Image_lift_iff_reachable
    {X Y : FivefoldP77ImagePoint f g h k}
    (z : FivefoldP77ConservativeClasses f g h k X.vertex Y.vertex) :
    (∃ a : FivefoldP77ImageHom f g h k X Y, a.val = z) ↔
      fivefoldP77ConservativeReachable f g h k z := by
  constructor
  · rintro ⟨a, ha⟩
    rw [← ha]
    exact a.property
  · intro hz
    exact ⟨⟨z, hz⟩, rfl⟩

/-- Image inclusion membership as a true Mathlib Functor Hom image,
not membership of an integer-charge kernel. -/
theorem fivefoldP77ImageInclusion_map_iff_reachable
    {X Y : FivefoldP77ImagePoint f g h k}
    (z : FivefoldP77ConservativeClasses f g h k X.vertex Y.vertex) :
    (∃ a : X ⟶ Y, (fivefoldP77ImageInclusion f g h k).map a = z) ↔
      fivefoldP77ConservativeReachable f g h k z := by
  letI := fivefoldP77ConservativeCategory f g h k
  letI := fivefoldP77ImageCategory f g h k
  exact fivefoldP77Image_lift_iff_reachable f g h k z

/-- Complete original Type-valued source-5-cell characterization of
missing Hom classes, for EVERY original P77 four-proof representative.
No converse is inferred from a mere equality of signed charges. -/
theorem fivefoldP77OriginalClass_unreachable_iff_noSourceFiveCell
    {u v : FivefoldPathVertex}
    (w : NativeF55RawVerticalFourCell first last
      (fivefoldF55OriginalAt f g h k u.phase)
      (fivefoldF55OriginalAt f g h k v.phase)) :
    (¬ fivefoldP77ConservativeReachable f g h k
      (fivefoldP77ConservativeClass f g h k w)) ↔
      (∀ path : Quiver.Path u v,
        ¬ Nonempty (NativeGK5CGConservativeFiveCell first last
          (fivefoldEvaluateP77 f g h k path) w)) := by
  constructor
  · intro hno path cert
    exact hno ((fivefoldP77ConservativeClass_reachable_iff
      f g h k w).2 ⟨path, cert⟩)
  · intro hno hreach
    obtain ⟨path, cert⟩ :=
      (fivefoldP77ConservativeClass_reachable_iff
        f g h k w).1 hreach
    exact (hno path) cert

/-- Reachability forces an ORIGINAL P77 signed charge between
zero and three, since this exact directed quiver has no path
longer than three arrows. This is only a necessary condition. -/
theorem fivefoldP77_reachable_charge_range
    {u v : FivefoldPathVertex}
    (z : FivefoldP77ConservativeClasses f g h k u v)
    (hz : fivefoldP77ConservativeReachable f g h k z) :
    0 ≤ fivefoldP77ConservativeCharge f g h k z ∧
      fivefoldP77ConservativeCharge f g h k z ≤ (3 : ℤ) := by
  letI := fivefoldP77ConservativeCategory f g h k
  obtain ⟨path, hmap⟩ := hz
  have hc : fivefoldP77ConservativeCharge f g h k z =
      (path.length : ℤ) := by
    calc
      fivefoldP77ConservativeCharge f g h k z =
          fivefoldP77ConservativeCharge f g h k
            ((fivefoldP77ConservativeFunctor f g h k).map path) :=
        congrArg (fivefoldP77ConservativeCharge f g h k) hmap.symm
      _ = (path.length : ℤ) :=
        fivefoldP77ConservativeFunctor_charge_length f g h k path
  constructor
  · rw [hc]
    exact Int.natCast_nonneg _
  · rw [hc]
    exact_mod_cast fivefoldFreePath_length_le_three path

/-- Charges outside [0,3] give provable missing Homs. This combines
the original signed-negative obstruction and the finite source
quiver's absolute path-length ceiling. -/
theorem fivefoldP77_charge_out_of_range_not_reachable
    {u v : FivefoldPathVertex}
    (z : FivefoldP77ConservativeClasses f g h k u v)
    (hout : fivefoldP77ConservativeCharge f g h k z < 0 ∨
      (3 : ℤ) < fivefoldP77ConservativeCharge f g h k z) :
    ¬ fivefoldP77ConservativeReachable f g h k z := by
  intro hz
  obtain ⟨hlo, hhi⟩ := fivefoldP77_reachable_charge_range f g h k z hz
  rcases hout with hn | hn
  · exact (not_lt_of_ge hlo) hn
  · exact (not_lt_of_ge hhi) hn

/-- At a fixed pair of typed endpoints the signed charge determines
a reachable class uniquely. Crucially BOTH classes must already
have genuine finite-path preimages: no injectivity is claimed
on the whole ORIGINAL P77 quotient Hom. -/
theorem fivefoldP77_reachable_charge_injective
    {u v : FivefoldPathVertex}
    (z w : FivefoldP77ConservativeClasses f g h k u v)
    (hz : fivefoldP77ConservativeReachable f g h k z)
    (hw : fivefoldP77ConservativeReachable f g h k w)
    (hc : fivefoldP77ConservativeCharge f g h k z =
      fivefoldP77ConservativeCharge f g h k w) :
    z = w := by
  letI := fivefoldP77ConservativeCategory f g h k
  obtain ⟨pathZ, hZ⟩ := hz
  obtain ⟨pathW, hW⟩ := hw
  have hZcharge : fivefoldP77ConservativeCharge f g h k z =
      (pathZ.length : ℤ) := by
    calc
      fivefoldP77ConservativeCharge f g h k z =
          fivefoldP77ConservativeCharge f g h k
            ((fivefoldP77ConservativeFunctor f g h k).map pathZ) :=
        congrArg (fivefoldP77ConservativeCharge f g h k) hZ.symm
      _ = (pathZ.length : ℤ) :=
        fivefoldP77ConservativeFunctor_charge_length f g h k pathZ
  have hWcharge : fivefoldP77ConservativeCharge f g h k w =
      (pathW.length : ℤ) := by
    calc
      fivefoldP77ConservativeCharge f g h k w =
          fivefoldP77ConservativeCharge f g h k
            ((fivefoldP77ConservativeFunctor f g h k).map pathW) :=
        congrArg (fivefoldP77ConservativeCharge f g h k) hW.symm
      _ = (pathW.length : ℤ) :=
        fivefoldP77ConservativeFunctor_charge_length f g h k pathW
  have hlenInt : (pathZ.length : ℤ) = (pathW.length : ℤ) :=
    hZcharge.symm.trans (hc.trans hWcharge)
  have hlen : pathZ.length = pathW.length := by
    exact_mod_cast hlenInt
  have hpaths : pathZ = pathW := fivefoldFreePath_length_injective hlen
  rw [hpaths] at hZ
  exact hZ.symm.trans hW

/-- The real image Category is Hom-wise charge separated: at fixed
typed endpoints the original charge is an injective observer
ON THE IMAGE, but not an image-membership certificate. -/
theorem fivefoldP77Image_charge_injective
    {X Y : FivefoldP77ImagePoint f g h k}
    (A B : FivefoldP77ImageHom f g h k X Y)
    (hc : fivefoldP77ConservativeCharge f g h k A.val =
      fivefoldP77ConservativeCharge f g h k B.val) :
    A = B := by
  apply Subtype.ext
  exact fivefoldP77_reachable_charge_injective
    f g h k A.val B.val A.property B.property hc

/-- Zero charge at DISTINCT original typed endpoints cannot be a
source path image, since a source path with charge zero would
have length zero and hence equal endpoints. -/
theorem fivefoldP77_zeroCharge_offDiagonal_not_reachable
    {u v : FivefoldPathVertex} (hne : u ≠ v)
    (z : FivefoldP77ConservativeClasses f g h k u v)
    (hzero : fivefoldP77ConservativeCharge f g h k z = 0) :
    ¬ fivefoldP77ConservativeReachable f g h k z := by
  letI := fivefoldP77ConservativeCategory f g h k
  rintro ⟨path, hmap⟩
  have hlenInt : (path.length : ℤ) = 0 := by
    calc
      (path.length : ℤ) =
          fivefoldP77ConservativeCharge f g h k
            ((fivefoldP77ConservativeFunctor f g h k).map path) :=
        (fivefoldP77ConservativeFunctor_charge_length f g h k path).symm
      _ = fivefoldP77ConservativeCharge f g h k z :=
        congrArg (fivefoldP77ConservativeCharge f g h k) hmap
      _ = 0 := hzero
  have hlen : path.length = 0 := by
    exact_mod_cast hlenInt
  exact hne (path.eq_of_length_zero hlen)

/-- Concrete ORIGINAL P77 four-proof 1 -> 0 of charge ZERO:
inverse(e01) of charge -1 pasted with the true pentagon loop
upper(0->3) ; inverse(lower(0->3)) of charge 3-2 = +1.
All raw constructors are genuine original F55/P77 four-proofs;
the subsequent quotient is still by GK5CG conservative 5-cells. -/
def fivefoldP77OriginalZeroChargeReverse01 :
    FivefoldP77ConservativeClasses f g h k
      (fivefoldPathVertex 1) (fivefoldPathVertex 0) :=
  fivefoldP77ConservativeClass f g h k
    (.trans
      (.symm (fivefoldArrowOriginalP77 f g h k
        (fivefoldPathArrowOf .e01)))
      (.trans
        (fivefoldEvaluateP77 f g h k fivefoldFreeUpper)
        (.symm (fivefoldEvaluateP77 f g h k fivefoldFreeLower))))

/-- The original four-proof witness has zero signed original
associator charge, despite its nontrivial typed boundary 1 -> 0. -/
theorem fivefoldP77OriginalZeroChargeReverse01_charge :
    fivefoldP77ConservativeCharge f g h k
      (fivefoldP77OriginalZeroChargeReverse01 f g h k) = 0 := by
  change
    -(fivefoldArrowOriginalP77 f g h k
      (fivefoldPathArrowOf .e01)).gk5cgAssocCharge +
      ((fivefoldEvaluateP77 f g h k fivefoldFreeUpper).gk5cgAssocCharge +
        -(fivefoldEvaluateP77 f g h k fivefoldFreeLower).gk5cgAssocCharge) = 0
  simp only [fivefoldArrowOriginalP77_charge_one,
    fivefoldEvaluateP77_charge_length,
    fivefoldFreeUpper_length, fivefoldFreeLower_length]
  norm_num

/-- ZERO charge passes every global charge-range test, but this
actual P77 quotient class is NOT reachable from the original
five-edge free path category. Charge is strictly incomplete
as an image-membership invariant. -/
theorem fivefoldP77OriginalZeroChargeReverse01_not_reachable :
    ¬ fivefoldP77ConservativeReachable f g h k
      (fivefoldP77OriginalZeroChargeReverse01 f g h k) := by
  apply fivefoldP77_zeroCharge_offDiagonal_not_reachable f g h k
    (u := fivefoldPathVertex 1) (v := fivefoldPathVertex 0)
    (by decide)
  exact fivefoldP77OriginalZeroChargeReverse01_charge f g h k

/-- The zero-charge obstruction is genuinely different from the
already known negative-charge original P77 reverse-e01 witness. -/
theorem fivefoldP77OriginalZeroReverse_ne_negativeReverse :
    fivefoldP77OriginalZeroChargeReverse01 f g h k ≠
      fivefoldP77OriginalReverse01 f g h k := by
  intro heq
  have hc := congrArg (fivefoldP77ConservativeCharge f g h k) heq
  rw [fivefoldP77OriginalZeroChargeReverse01_charge,
    fivefoldP77OriginalReverse01_charge] at hc
  norm_num at hc

/-- Precise failure of a charge-only sufficient criterion, exhibited
by a real original P77 proof-class Hom with bounded charge. -/
theorem fivefoldP77_charge_range_not_sufficient_for_reachability :
    ∃ z : FivefoldP77ConservativeClasses f g h k
      (fivefoldPathVertex 1) (fivefoldPathVertex 0),
      (0 ≤ fivefoldP77ConservativeCharge f g h k z ∧
        fivefoldP77ConservativeCharge f g h k z ≤ (3 : ℤ)) ∧
        ¬ fivefoldP77ConservativeReachable f g h k z := by
  refine ⟨fivefoldP77OriginalZeroChargeReverse01 f g h k, ?_, ?_⟩
  · rw [fivefoldP77OriginalZeroChargeReverse01_charge]
    norm_num
  · exact fivefoldP77OriginalZeroChargeReverse01_not_reachable f g h k

/-- The REAL image inclusion misses the new zero-charge class at
the exact original typed endpoints, not only the negative witness. -/
theorem fivefoldP77Image_zeroCharge_missing :
    ¬ ∃ a : FivefoldP77ImageHom f g h k
        (⟨fivefoldPathVertex 1⟩ : FivefoldP77ImagePoint f g h k)
        (⟨fivefoldPathVertex 0⟩ : FivefoldP77ImagePoint f g h k),
      a.val = fivefoldP77OriginalZeroChargeReverse01 f g h k := by
  rintro ⟨A, hA⟩
  exact fivefoldP77OriginalZeroChargeReverse01_not_reachable f g h k
    (hA ▸ A.property)

/-- Necessary structural price of making a future original-P77
extension FULL: at original phase 1 and 0 the extended source must
actually provide BOTH the original charge -1 inverse class AND
the distinct zero-charge inverse+pentagon-loop class.
This asserts necessity only, not existence of an extended source. -/
theorem fivefoldP77FullExtension_requires_reverse_and_zeroCharge
    {S : Type uS} [Category.{vS} S]
    (F : S ⥤ FivefoldP77ConservativePoint f g h k)
    (X Y : S)
    (hX : F.obj X =
      (⟨fivefoldPathVertex 1⟩ : FivefoldP77ConservativePoint f g h k))
    (hY : F.obj Y =
      (⟨fivefoldPathVertex 0⟩ : FivefoldP77ConservativePoint f g h k))
    (hfull : F.Full) :
    (∃ A : X ⟶ Y,
      F.map A = eqToHom hX ≫
        (fivefoldP77OriginalReverse01 f g h k) ≫ eqToHom hY.symm) ∧
    (∃ B : X ⟶ Y,
      F.map B = eqToHom hX ≫
        (fivefoldP77OriginalZeroChargeReverse01 f g h k) ≫
          eqToHom hY.symm) := by
  letI := fivefoldP77ConservativeCategory f g h k
  haveI : F.Full := hfull
  constructor
  · exact F.map_surjective _
  · exact F.map_surjective _

#print axioms fivefoldP77Image_lift_iff_reachable
#print axioms fivefoldP77ImageInclusion_map_iff_reachable
#print axioms fivefoldP77OriginalClass_unreachable_iff_noSourceFiveCell
#print axioms fivefoldP77_reachable_charge_range
#print axioms fivefoldP77_charge_out_of_range_not_reachable
#print axioms fivefoldP77_reachable_charge_injective
#print axioms fivefoldP77Image_charge_injective
#print axioms fivefoldP77_zeroCharge_offDiagonal_not_reachable
#print axioms fivefoldP77OriginalZeroChargeReverse01
#print axioms fivefoldP77OriginalZeroChargeReverse01_charge
#print axioms fivefoldP77OriginalZeroChargeReverse01_not_reachable
#print axioms fivefoldP77OriginalZeroReverse_ne_negativeReverse
#print axioms fivefoldP77_charge_range_not_sufficient_for_reachability
#print axioms fivefoldP77Image_zeroCharge_missing
#print axioms fivefoldP77FullExtension_requires_reverse_and_zeroCharge

end
end KUOS.Architecture.WuxingPentagonUnified
