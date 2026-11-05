import KUOS.Architecture.QiWuxingGK5CHP77CertifiedImagePathRecoveryV4_60
import Mathlib.CategoryTheory.NatIso
import Mathlib.CategoryTheory.Equivalence
import Mathlib.Tactic

/-!
Qi v4.61 — GENUINE P77 IMAGE QUASI-INVERSE COMPARISON
AND EXACT TYPED UPPER/LOWER PENTAGON PATH NORMAL FORMS.

Keep the TRUE original FivefoldEdge free path category and genuine
F55/P77 four-proof quotient classes by conservative GK5CG
Type-valued five-cell evidence; the source-certified image retains
actual finite-path reachability, not charge equality or a C60
physical Edge shadow.

Qi v4.58 constructs a genuine Mathlib Equivalence with a
choice-dependent quasi-inverse Q. Qi v4.60 independently constructs
the explicit proof-relevant path recovery functor R satisfying
genuine pointwise two-sided inverse laws. We compare Q and R by a
true Mathlib natural ISOMORPHISM, not by a fabricated definitional
equality. Its components are the image under R of the original
v4.58 equivalence counit isomorphism. Its naturality is derived
from the same genuine counit naturality and source recovery.

The true pentagon upper/lower finite paths have their original
typed P77 image classes and recover EXACTLY the original free
words. Their original GK5CG charges remain 3 and 2, and the
natural isomorphism comparison respects both arrows. No new
pentagonator or forbidden original 5-cell is introduced.

The comparison applies ONLY on the genuine source-certified image.
Qi v4.59's charge-zero off-diagonal original P77 target Hom is
not a new source arrow and remains an obstruction to whole-target
path recovery.

Append-only, same-root; strict 空 central, independent Kuu one
presentation. Original F54/F55/P77/P94A, actual C60 physical gauge
and CRT authorities unchanged. Public root107 maintained.
Pinned Lean v4.30.0-rc2, mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Validation-only PR #1558 remains Draft/open/unmerged.
No new axioms, sorry, admit, native_decide or Gray.
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

/-- An ACTUAL original typed source-path iso from the v4.58
choice-dependent quasi-inverse object to the v4.60 explicit
recovery object. It is obtained by mapping the genuine counit
Iso of the original equivalence, not by assuming object equality. -/
def fivefoldP77InverseRecoveryComponent
    (X : FivefoldP77ImagePoint f g h k) :
    (fivefoldP77ImageQuasiInverse f g h k).obj X ≅
      (fivefoldP77ImageRecoveryFunctor f g h k).obj X := by
  letI := fivefoldP77ConservativeCategory f g h k
  letI := fivefoldP77ImageCategory f g h k
  exact (fivefoldP77ImageRecoveryFunctor f g h k).mapIso
    ((fivefoldP77ImageEquivalence f g h k).counitIso.app X)

/-- Explicit naturality of the counit-induced comparison.
This is genuine Mathlib NATURALITY, not merely objectwise
isomorphisms or numerical equality of recovered lengths. -/
theorem fivefoldP77InverseRecoveryComponent_natural
    {X Y : FivefoldP77ImagePoint f g h k} (A : X ⟶ Y) :
    (fivefoldP77ImageQuasiInverse f g h k).map A ≫
      (fivefoldP77InverseRecoveryComponent f g h k Y).hom =
    (fivefoldP77InverseRecoveryComponent f g h k X).hom ≫
      (fivefoldP77ImageRecoveryFunctor f g h k).map A := by
  letI := fivefoldP77ConservativeCategory f g h k
  letI := fivefoldP77ImageCategory f g h k
  let EE := fivefoldP77ImageEquivalence f g h k
  let RR := fivefoldP77ImageRecoveryFunctor f g h k
  let QQ := fivefoldP77ImageQuasiInverse f g h k
  have hLeft :
      RR.map ((EE.inverse ⋙ EE.functor).map A) = QQ.map A := by
    change (fivefoldP77ImageRecoveryFunctor f g h k).map
      ((fivefoldP77ImageFactor f g h k).map
        ((fivefoldP77ImageQuasiInverse f g h k).map A)) =
      (fivefoldP77ImageQuasiInverse f g h k).map A
    exact fivefoldP77ImageRecovery_left_map f g h k (QQ.map A)
  have hCounit := EE.counitIso.hom.naturality A
  have hMapped := congrArg (fun z => RR.map z) hCounit
  change QQ.map A ≫ RR.map (EE.counitIso.hom.app Y) =
    RR.map (EE.counitIso.hom.app X) ≫ RR.map A
  simpa only [Functor.map_comp, hLeft] using hMapped

/-- A true natural ISO between the old Mathlib equivalence
quasi-inverse and the NEW typed path recovery functor.
This does NOT claim definitional equality of choice functions. -/
def fivefoldP77QuasiInverseRecoveryNatIso :
    fivefoldP77ImageQuasiInverse f g h k ≅
      fivefoldP77ImageRecoveryFunctor f g h k := by
  letI := fivefoldP77ConservativeCategory f g h k
  letI := fivefoldP77ImageCategory f g h k
  exact NatIso.ofComponents
    (fivefoldP77InverseRecoveryComponent f g h k)
    (fun {_ _} A =>
      fivefoldP77InverseRecoveryComponent_natural f g h k A)

/-- In particular both inverse presentations are isomorphic as
genuine Mathlib functors on the certified P77 image Category. -/
theorem fivefoldP77QuasiInverseRecovery_iso_exists :
    Nonempty (fivefoldP77ImageQuasiInverse f g h k ≅
      fivefoldP77ImageRecoveryFunctor f g h k) :=
  ⟨fivefoldP77QuasiInverseRecoveryNatIso f g h k⟩

/-- The genuine source upper three-step route mapped into the
original P77 proof-relevant certified-image Hom. -/
def fivefoldP77CertifiedUpper :
    FivefoldP77ImageHom f g h k
      (⟨fivefoldPathVertex 0⟩ : FivefoldP77ImagePoint f g h k)
      (⟨fivefoldPathVertex 3⟩ : FivefoldP77ImagePoint f g h k) := by
  letI := fivefoldP77ConservativeCategory f g h k
  letI := fivefoldP77ImageCategory f g h k
  exact (fivefoldP77ImageFactor f g h k).map fivefoldFreeUpper

/-- The genuine source lower two-step route mapped into the
original P77 proof-relevant certified-image Hom. -/
def fivefoldP77CertifiedLower :
    FivefoldP77ImageHom f g h k
      (⟨fivefoldPathVertex 0⟩ : FivefoldP77ImagePoint f g h k)
      (⟨fivefoldPathVertex 3⟩ : FivefoldP77ImagePoint f g h k) := by
  letI := fivefoldP77ConservativeCategory f g h k
  letI := fivefoldP77ImageCategory f g h k
  exact (fivefoldP77ImageFactor f g h k).map fivefoldFreeLower

/-- Recovery of the ORIGINAL upper P77 evidence retains the exact
source 01-12-23 word, not a length-three numerical surrogate. -/
theorem fivefoldP77CertifiedUpper_recover :
    fivefoldP77ImageRecoverPath f g h k
      (fivefoldP77CertifiedUpper f g h k) = fivefoldFreeUpper := by
  letI := fivefoldP77ConservativeCategory f g h k
  letI := fivefoldP77ImageCategory f g h k
  exact fivefoldP77ImageRecoverPath_of_factor f g h k fivefoldFreeUpper

/-- Recovery of the ORIGINAL lower P77 evidence retains the exact
source 04-43 word, which is different from the upper word. -/
theorem fivefoldP77CertifiedLower_recover :
    fivefoldP77ImageRecoverPath f g h k
      (fivefoldP77CertifiedLower f g h k) = fivefoldFreeLower := by
  letI := fivefoldP77ConservativeCategory f g h k
  letI := fivefoldP77ImageCategory f g h k
  exact fivefoldP77ImageRecoverPath_of_factor f g h k fivefoldFreeLower

/-- Original GK5CG P77 conservative charge on the upper REAL
four-proof class is exactly three, as the true recovered path. -/
theorem fivefoldP77CertifiedUpper_charge :
    fivefoldP77ConservativeCharge f g h k
      (fivefoldP77CertifiedUpper f g h k).val = 3 := by
  letI := fivefoldP77ConservativeCategory f g h k
  letI := fivefoldP77ImageCategory f g h k
  calc
    fivefoldP77ConservativeCharge f g h k
        (fivefoldP77CertifiedUpper f g h k).val =
      ((fivefoldP77ImageRecoverPath f g h k
        (fivefoldP77CertifiedUpper f g h k)).length : ℤ) :=
      fivefoldP77ImageRecoverPath_charge_length f g h k
        (fivefoldP77CertifiedUpper f g h k)
    _ = 3 := by
      rw [fivefoldP77CertifiedUpper_recover, fivefoldFreeUpper_length]
      norm_num

/-- Original GK5CG P77 conservative charge on the lower REAL
four-proof class is exactly two, as the true recovered path. -/
theorem fivefoldP77CertifiedLower_charge :
    fivefoldP77ConservativeCharge f g h k
      (fivefoldP77CertifiedLower f g h k).val = 2 := by
  letI := fivefoldP77ConservativeCategory f g h k
  letI := fivefoldP77ImageCategory f g h k
  calc
    fivefoldP77ConservativeCharge f g h k
        (fivefoldP77CertifiedLower f g h k).val =
      ((fivefoldP77ImageRecoverPath f g h k
        (fivefoldP77CertifiedLower f g h k)).length : ℤ) :=
      fivefoldP77ImageRecoverPath_charge_length f g h k
        (fivefoldP77CertifiedLower f g h k)
    _ = 2 := by
      rw [fivefoldP77CertifiedLower_recover, fivefoldFreeLower_length]
      norm_num

/-- True upper/lower typed original P77 source-certified image
Homs remain distinct. No historical pentagonator is fabricated. -/
theorem fivefoldP77CertifiedUpper_ne_lower :
    fivefoldP77CertifiedUpper f g h k ≠
      fivefoldP77CertifiedLower f g h k := by
  intro heq
  have hcharge := congrArg
    (fun z : FivefoldP77ImageHom f g h k
      (⟨fivefoldPathVertex 0⟩ : FivefoldP77ImagePoint f g h k)
      (⟨fivefoldPathVertex 3⟩ : FivefoldP77ImagePoint f g h k) =>
      fivefoldP77ConservativeCharge f g h k z.val) heq
  change fivefoldP77ConservativeCharge f g h k
      (fivefoldP77CertifiedUpper f g h k).val =
    fivefoldP77ConservativeCharge f g h k
      (fivefoldP77CertifiedLower f g h k).val at hcharge
  rw [fivefoldP77CertifiedUpper_charge,
    fivefoldP77CertifiedLower_charge] at hcharge
  norm_num at hcharge

/-- Naturality identifies the old v4.58 quasi-inverse action on
the genuine UPPER image Hom with the explicitly recovered
three-edge source word, via the actual component isomorphisms. -/
theorem fivefoldP77QuasiInverse_upper_naturality :
    (fivefoldP77ImageQuasiInverse f g h k).map
      (fivefoldP77CertifiedUpper f g h k) ≫
      (fivefoldP77QuasiInverseRecoveryNatIso f g h k).hom.app
        (⟨fivefoldPathVertex 3⟩ : FivefoldP77ImagePoint f g h k) =
    (fivefoldP77QuasiInverseRecoveryNatIso f g h k).hom.app
        (⟨fivefoldPathVertex 0⟩ : FivefoldP77ImagePoint f g h k) ≫
      fivefoldFreeUpper := by
  letI := fivefoldP77ConservativeCategory f g h k
  letI := fivefoldP77ImageCategory f g h k
  have hnat :=
    (fivefoldP77QuasiInverseRecoveryNatIso f g h k).hom.naturality
      (fivefoldP77CertifiedUpper f g h k)
  change _ =
      (fivefoldP77QuasiInverseRecoveryNatIso f g h k).hom.app
        (⟨fivefoldPathVertex 0⟩ : FivefoldP77ImagePoint f g h k) ≫
      (fivefoldP77ImageRecoverPath f g h k
        (fivefoldP77CertifiedUpper f g h k)) at hnat
  have hword := congrArg
    (fun path : Quiver.Path (fivefoldPathVertex 0) (fivefoldPathVertex 3) =>
      (fivefoldP77QuasiInverseRecoveryNatIso f g h k).hom.app
        (⟨fivefoldPathVertex 0⟩ : FivefoldP77ImagePoint f g h k) ≫ path)
    (fivefoldP77CertifiedUpper_recover f g h k)
  exact hnat.trans hword

/-- The corresponding naturality square for the true LOWER
original P77 word 04-43, rather than a numerical path substitute. -/
theorem fivefoldP77QuasiInverse_lower_naturality :
    (fivefoldP77ImageQuasiInverse f g h k).map
      (fivefoldP77CertifiedLower f g h k) ≫
      (fivefoldP77QuasiInverseRecoveryNatIso f g h k).hom.app
        (⟨fivefoldPathVertex 3⟩ : FivefoldP77ImagePoint f g h k) =
    (fivefoldP77QuasiInverseRecoveryNatIso f g h k).hom.app
        (⟨fivefoldPathVertex 0⟩ : FivefoldP77ImagePoint f g h k) ≫
      fivefoldFreeLower := by
  letI := fivefoldP77ConservativeCategory f g h k
  letI := fivefoldP77ImageCategory f g h k
  have hnat :=
    (fivefoldP77QuasiInverseRecoveryNatIso f g h k).hom.naturality
      (fivefoldP77CertifiedLower f g h k)
  change _ =
      (fivefoldP77QuasiInverseRecoveryNatIso f g h k).hom.app
        (⟨fivefoldPathVertex 0⟩ : FivefoldP77ImagePoint f g h k) ≫
      (fivefoldP77ImageRecoverPath f g h k
        (fivefoldP77CertifiedLower f g h k)) at hnat
  have hword := congrArg
    (fun path : Quiver.Path (fivefoldPathVertex 0) (fivefoldPathVertex 3) =>
      (fivefoldP77QuasiInverseRecoveryNatIso f g h k).hom.app
        (⟨fivefoldPathVertex 0⟩ : FivefoldP77ImagePoint f g h k) ≫ path)
    (fivefoldP77CertifiedLower_recover f g h k)
  exact hnat.trans hword

/-- The correct combined boundary is a NATURAL isomorphism of
genuine source-path reconstruction functors, *two distinct*
original P77 evidence-bearing pentagon Homs, and both exact
typed normal forms with original GK5CG charge 3/2. -/
theorem fivefoldP77InverseComparison_pentagon_split :
    Nonempty (fivefoldP77ImageQuasiInverse f g h k ≅
      fivefoldP77ImageRecoveryFunctor f g h k) ∧
    fivefoldP77CertifiedUpper f g h k ≠
      fivefoldP77CertifiedLower f g h k ∧
    fivefoldP77ImageRecoverPath f g h k
      (fivefoldP77CertifiedUpper f g h k) = fivefoldFreeUpper ∧
    fivefoldP77ImageRecoverPath f g h k
      (fivefoldP77CertifiedLower f g h k) = fivefoldFreeLower :=
  ⟨fivefoldP77QuasiInverseRecovery_iso_exists f g h k,
   fivefoldP77CertifiedUpper_ne_lower f g h k,
   fivefoldP77CertifiedUpper_recover f g h k,
   fivefoldP77CertifiedLower_recover f g h k⟩

#print axioms fivefoldP77InverseRecoveryComponent
#print axioms fivefoldP77InverseRecoveryComponent_natural
#print axioms fivefoldP77QuasiInverseRecoveryNatIso
#print axioms fivefoldP77QuasiInverseRecovery_iso_exists
#print axioms fivefoldP77CertifiedUpper
#print axioms fivefoldP77CertifiedLower
#print axioms fivefoldP77CertifiedUpper_recover
#print axioms fivefoldP77CertifiedLower_recover
#print axioms fivefoldP77CertifiedUpper_charge
#print axioms fivefoldP77CertifiedLower_charge
#print axioms fivefoldP77CertifiedUpper_ne_lower
#print axioms fivefoldP77QuasiInverse_upper_naturality
#print axioms fivefoldP77QuasiInverse_lower_naturality
#print axioms fivefoldP77InverseComparison_pentagon_split

end
end KUOS.Architecture.WuxingPentagonUnified
