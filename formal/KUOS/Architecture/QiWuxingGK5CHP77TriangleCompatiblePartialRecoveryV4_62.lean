import KUOS.Architecture.QiWuxingGK5CHP77InverseUniquenessPentagonNormalFormsV4_61
import Mathlib.CategoryTheory.NatIso
import Mathlib.CategoryTheory.Equivalence
import Mathlib.Tactic

/-!
Qi v4.62 — ORIGINAL P77 TRIANGLE-COMPATIBLE PARTIAL PATH RECOVERY.

The original directed FivefoldEdge free paths, the ORIGINAL F55/P77
four-cell conservative quotient by genuine GK5CG Type-valued five-cell
witnesses, and the certified source-path image remain distinct
authorities. Their certified image is a true Mathlib category.

Qi v4.58 produced an actual equivalence E with unit/counit
isomorphisms and a choice-dependent quasi-inverse Q.
Qi v4.60 built a separate genuine source-path recovery functor R
and proved exact round-trips on the original certified-image Homs.
Qi v4.61 constructed a true natural isomorphism theta : Q ≅ R
using the original counit and path-recovery functor.

NEW: transport the *actual equivalence triangle* through R and
theta, verifying that unit followed by the comparison component
is the original free-path identity. Also reflect the original
counit by the source-to-image factor applied to theta. Do not
assert definitional equality of two choice-dependent inverses.

NEW: expose the maximal exact SOURCE-CERTIFIED HOM domain as a
genuine dependent subtype of the ORIGINAL P77 four-proof quotient,
with the real Hom Equiv to original typed source Quiver.Path.
Provide partial recovery, its unique evaluation certificate,
source-identity/composition, and original associator charge=length.
Prove an exact source-Type five-cell iff and identify two distinct
original target missing Homs: charge -1 and charge ZERO from 1 to 0.

The partial domain is NOT defined by charge inequalities. No
global exact typed path section of the whole P77 target exists,
as Qi v4.59/v4.60 proved. No new source pentagonator, inverse edge,
numerical proxy, physical C60 edge equality or Gray data.

Append-only, same-root, public root107. Strict 空 is central and
independent Kuu one presentation. Original F54/F55/P77/P94A
evidence, north C60 CRT and genuine physical gauge preserved.
Lean v4.30.0-rc2, mathlib pinned
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

/-- The original v4.58 equivalence unit followed by the v4.61
comparison Q ≅ R is EXACTLY the genuine identity of the original
source finite-path category. This is a transported triangle
certificate, not a new postulated coherence generator. -/
theorem fivefoldP77Recovery_unit_comparison_triangle
    (u : FivefoldPathVertex) :
    (fivefoldP77ImageEquivalence f g h k).unitIso.hom.app u ≫
      (fivefoldP77QuasiInverseRecoveryNatIso f g h k).hom.app
        ((fivefoldP77ImageEquivalence f g h k).functor.obj u) =
      (Quiver.Path.nil : Quiver.Path u u) := by
  letI := fivefoldP77ConservativeCategory f g h k
  letI := fivefoldP77ImageCategory f g h k
  let EE := fivefoldP77ImageEquivalence f g h k
  let FF := fivefoldP77ImageFactor f g h k
  let RR := fivefoldP77ImageRecoveryFunctor f g h k
  let TH := fivefoldP77QuasiInverseRecoveryNatIso f g h k
  have hCounitTransport :
      FF.map (TH.hom.app (EE.functor.obj u)) =
        EE.counitIso.hom.app (EE.functor.obj u) := by
    change (RR ⋙ FF).map
        (EE.counitIso.hom.app (EE.functor.obj u)) =
      EE.counitIso.hom.app (EE.functor.obj u)
    exact fivefoldP77ImageRecovery_right_map f g h k _
  have hMapComp :
      FF.map (EE.unitIso.hom.app u ≫ TH.hom.app (EE.functor.obj u)) =
        EE.functor.map (EE.unitIso.hom.app u) ≫
          EE.counitIso.hom.app (EE.functor.obj u) := by
    calc
      FF.map (EE.unitIso.hom.app u ≫ TH.hom.app (EE.functor.obj u)) =
          FF.map (EE.unitIso.hom.app u) ≫
            FF.map (TH.hom.app (EE.functor.obj u)) :=
        FF.map_comp _ _
      _ = EE.functor.map (EE.unitIso.hom.app u) ≫
            EE.counitIso.hom.app (EE.functor.obj u) := by
        exact congrArg (fun z =>
          FF.map (EE.unitIso.hom.app u) ≫ z) hCounitTransport
  have hTriangle :
      EE.functor.map (EE.unitIso.hom.app u) ≫
        EE.counitIso.hom.app (EE.functor.obj u) =
          𝟙 (EE.functor.obj u) :=
    EE.functor_unitIso_comp u
  have hId :
      FF.map (Quiver.Path.nil : Quiver.Path u u) =
        𝟙 (EE.functor.obj u) :=
    FF.map_id u
  apply (fivefoldP77ImageFactor_faithful f g h k).map_injective
  exact hMapComp.trans (hTriangle.trans hId.symm)

/-- The v4.61 comparison component followed by the old forward
factor is exactly the original v4.58 counit at EVERY genuine
source-certified image point. The target is NOT whole P77. -/
theorem fivefoldP77Recovery_comparison_reflects_counit
    (X : FivefoldP77ImagePoint f g h k) :
    (fivefoldP77ImageFactor f g h k).map
        ((fivefoldP77QuasiInverseRecoveryNatIso f g h k).hom.app X) =
      (fivefoldP77ImageEquivalence f g h k).counitIso.hom.app X := by
  letI := fivefoldP77ConservativeCategory f g h k
  letI := fivefoldP77ImageCategory f g h k
  cases X with
  | mk u =>
    change (fivefoldP77ImageRecoveryFunctor f g h k ⋙
        fivefoldP77ImageFactor f g h k).map
          ((fivefoldP77ImageEquivalence f g h k).counitIso.hom.app
            (⟨u⟩ : FivefoldP77ImagePoint f g h k)) =
      (fivefoldP77ImageEquivalence f g h k).counitIso.hom.app
        (⟨u⟩ : FivefoldP77ImagePoint f g h k)
    exact fivefoldP77ImageRecovery_right_map f g h k _

/-- Exact coherence boundary between the original adjoint
equivalence triangle and the concrete certified path normalizer. -/
theorem fivefoldP77Recovery_oldTriangle_newInverse_split :
    (∀ u : FivefoldPathVertex,
      (fivefoldP77ImageEquivalence f g h k).unitIso.hom.app u ≫
        (fivefoldP77QuasiInverseRecoveryNatIso f g h k).hom.app
          ((fivefoldP77ImageEquivalence f g h k).functor.obj u) =
        (Quiver.Path.nil : Quiver.Path u u)) ∧
    (∀ X : FivefoldP77ImagePoint f g h k,
      (fivefoldP77ImageFactor f g h k).map
          ((fivefoldP77QuasiInverseRecoveryNatIso f g h k).hom.app X) =
        (fivefoldP77ImageEquivalence f g h k).counitIso.hom.app X) := by
  exact ⟨fivefoldP77Recovery_unit_comparison_triangle f g h k,
    fivefoldP77Recovery_comparison_reflects_counit f g h k⟩

/-- A genuinely dependent PARTIAL domain of ORIGINAL P77
conservative Type-valued four-cell quotient classes: one original
quotient class together with its actual finite-path reachability
certificate, not a charge bound or a synthetic shadow. -/
abbrev FivefoldP77PartialDomain
    (u v : FivefoldPathVertex) :=
  { z : FivefoldP77ConservativeClasses f g h k u v //
      fivefoldP77ConservativeReachable f g h k z }

/-- All and only the authentic source-certified original P77
target Hom classes are equivalent (as actual TYPES) to typed
original FivefoldEdge free paths. -/
def fivefoldP77PartialHomPathEquiv
    (u v : FivefoldPathVertex) :
    Quiver.Path u v ≃ FivefoldP77PartialDomain f g h k u v := by
  letI := fivefoldP77ConservativeCategory f g h k
  letI := fivefoldP77ImageCategory f g h k
  exact fivefoldP77ImageHomPathEquiv f g h k ⟨u⟩ ⟨v⟩

/-- A partial but EXACT typed normalizer from the ORIGINAL P77
target, requiring a genuine GK5CG source-reachability certificate.
The argument retains the original conservative quotient class. -/
def fivefoldP77PartialRecoverPath
    {u v : FivefoldPathVertex}
    (A : FivefoldP77PartialDomain f g h k u v) :
    Quiver.Path u v :=
  fivefoldP77ImageRecoverPath f g h k A

/-- The partial normalizer evaluates to the ORIGINAL P77 target
quotient class, with no raw-four-proof syntax identification. -/
theorem fivefoldP77PartialRecoverPath_spec
    {u v : FivefoldPathVertex}
    (A : FivefoldP77PartialDomain f g h k u v) :
    (fivefoldP77ConservativeFunctor f g h k).map
      (fivefoldP77PartialRecoverPath f g h k A) = A.val := by
  exact fivefoldP77ImageRecoverPath_spec f g h k A

/-- Every exact original-P77 source preimage is the UNIQUE
typed free path recovered from its existing Type-valued certificate. -/
theorem fivefoldP77PartialRecoverPath_unique
    {u v : FivefoldPathVertex}
    (A : FivefoldP77PartialDomain f g h k u v)
    (path : Quiver.Path u v)
    (hpath : (fivefoldP77ConservativeFunctor f g h k).map path = A.val) :
    fivefoldP77PartialRecoverPath f g h k A = path := by
  exact fivefoldP77ImageRecoverPath_unique f g h k A path hpath

/-- Exact round trip of the real partial path normalizer on every
authentic original FivefoldEdge typed free word. -/
theorem fivefoldP77PartialRecoverPath_of_factor
    {u v : FivefoldPathVertex} (path : Quiver.Path u v) :
    fivefoldP77PartialRecoverPath f g h k
      ((fivefoldP77ImageFactor f g h k).map path) = path := by
  letI := fivefoldP77ConservativeCategory f g h k
  letI := fivefoldP77ImageCategory f g h k
  exact fivefoldP77ImageRecoverPath_of_factor f g h k path

/-- Exact original GK5CG charge equals the length of the
recovered typed source path ONLY on the certified partial domain. -/
theorem fivefoldP77PartialRecoverPath_charge_length
    {u v : FivefoldPathVertex}
    (A : FivefoldP77PartialDomain f g h k u v) :
    fivefoldP77ConservativeCharge f g h k A.val =
      ((fivefoldP77PartialRecoverPath f g h k A).length : ℤ) := by
  exact fivefoldP77ImageRecoverPath_charge_length f g h k A

/-- The actual original P77 identity class has the empty
typed path as its uniquely recovered source normal form. -/
theorem fivefoldP77PartialRecoverPath_id
    (u : FivefoldPathVertex) :
    fivefoldP77PartialRecoverPath f g h k
      (fivefoldP77ImageId f g h k
        (⟨u⟩ : FivefoldP77ImagePoint f g h k)) =
      (Quiver.Path.nil : Quiver.Path u u) := by
  letI := fivefoldP77ConservativeCategory f g h k
  letI := fivefoldP77ImageCategory f g h k
  exact fivefoldP77ImageRecoverPath_id f g h k ⟨u⟩

/-- Composition of certified ORIGINAL P77 quotient classes
is closed in this partial domain, with true source-path recovery
respecting typed composition, not just charge addition. -/
theorem fivefoldP77PartialRecoverPath_comp
    {u v w : FivefoldPathVertex}
    (A : FivefoldP77PartialDomain f g h k u v)
    (B : FivefoldP77PartialDomain f g h k v w) :
    fivefoldP77PartialRecoverPath f g h k
      (fivefoldP77ImageComp f g h k A B) =
      (fivefoldP77PartialRecoverPath f g h k A).comp
        (fivefoldP77PartialRecoverPath f g h k B) := by
  letI := fivefoldP77ConservativeCategory f g h k
  letI := fivefoldP77ImageCategory f g h k
  exact fivefoldP77ImageRecoverPath_comp f g h k A B

/-- Exact original P77 target-Hom membership criterion for a
partial source-path section. This is the actual source reachability
Prop, NEVER an integer-charge interval test. -/
theorem fivefoldP77PartialDomain_lift_iff
    {u v : FivefoldPathVertex}
    (z : FivefoldP77ConservativeClasses f g h k u v) :
    (∃ A : FivefoldP77PartialDomain f g h k u v, A.val = z) ↔
      fivefoldP77ConservativeReachable f g h k z := by
  constructor
  · rintro ⟨A, hA⟩
    rw [← hA]
    exact A.property
  · intro hz
    exact ⟨⟨z, hz⟩, rfl⟩

/-- For each GENUINE original F55/P77 four-proof representative,
partial recoverability is equivalent to a real original GK5CG
conservative five-cell from a typed evaluated source path. -/
theorem fivefoldP77PartialDomain_originalFiveCell_iff
    {u v : FivefoldPathVertex}
    (w : NativeF55RawVerticalFourCell first last
      (fivefoldF55OriginalAt f g h k u.phase)
      (fivefoldF55OriginalAt f g h k v.phase)) :
    (∃ A : FivefoldP77PartialDomain f g h k u v,
      A.val = fivefoldP77ConservativeClass f g h k w) ↔
    (∃ path : Quiver.Path u v,
      Nonempty (NativeGK5CGConservativeFiveCell first last
        (fivefoldEvaluateP77 f g h k path) w)) := by
  exact (fivefoldP77PartialDomain_lift_iff f g h k _).trans
    (fivefoldP77ConservativeClass_reachable_iff f g h k w)

/-- Original P77 inverse e01 (charge -1) has no genuinely
typed source-certified partial Hom representative. -/
theorem fivefoldP77PartialDomain_negativeReverse_missing :
    ¬ ∃ A : FivefoldP77PartialDomain f g h k
        (fivefoldPathVertex 1) (fivefoldPathVertex 0),
      A.val = fivefoldP77OriginalReverse01 f g h k := by
  rintro ⟨A, hA⟩
  exact fivefoldP77OriginalReverse01_not_reachable f g h k
    (hA ▸ A.property)

/-- The *distinct* original P77 charge-zero off-diagonal
inverse-plus-pentagon-loop target Hom ALSO has no source-certified
partial Hom representative. Charge sign is insufficient. -/
theorem fivefoldP77PartialDomain_zeroReverse_missing :
    ¬ ∃ A : FivefoldP77PartialDomain f g h k
        (fivefoldPathVertex 1) (fivefoldPathVertex 0),
      A.val = fivefoldP77OriginalZeroChargeReverse01 f g h k := by
  rintro ⟨A, hA⟩
  exact fivefoldP77OriginalZeroChargeReverse01_not_reachable f g h k
    (hA ▸ A.property)

/-- Final sharp boundary: each actual original target Hom is
partially normalizable IFF source-five-cell certified, with
unique typed path recovery and original charge=length; this
does NOT extend to a global exact recovery on all original P77
four-proof quotient classes. -/
theorem fivefoldP77TrianglePartialRecovery_exact_boundary :
    (∀ (u v : FivefoldPathVertex)
       (z : FivefoldP77ConservativeClasses f g h k u v),
      (∃ A : FivefoldP77PartialDomain f g h k u v, A.val = z) ↔
        fivefoldP77ConservativeReachable f g h k z) ∧
    ¬ (∃ rec :
        (u v : FivefoldPathVertex) →
          FivefoldP77ConservativeClasses f g h k u v → Quiver.Path u v,
       ∀ (u v : FivefoldPathVertex)
         (z : FivefoldP77ConservativeClasses f g h k u v),
         (fivefoldP77ConservativeFunctor f g h k).map (rec u v z) = z) := by
  exact ⟨(fun u v z => fivefoldP77PartialDomain_lift_iff f g h k z),
    fivefoldP77NoGlobalHomRecovery f g h k⟩

#print axioms fivefoldP77Recovery_unit_comparison_triangle
#print axioms fivefoldP77Recovery_comparison_reflects_counit
#print axioms fivefoldP77Recovery_oldTriangle_newInverse_split
#print axioms FivefoldP77PartialDomain
#print axioms fivefoldP77PartialHomPathEquiv
#print axioms fivefoldP77PartialRecoverPath
#print axioms fivefoldP77PartialRecoverPath_spec
#print axioms fivefoldP77PartialRecoverPath_unique
#print axioms fivefoldP77PartialRecoverPath_of_factor
#print axioms fivefoldP77PartialRecoverPath_charge_length
#print axioms fivefoldP77PartialRecoverPath_id
#print axioms fivefoldP77PartialRecoverPath_comp
#print axioms fivefoldP77PartialDomain_lift_iff
#print axioms fivefoldP77PartialDomain_originalFiveCell_iff
#print axioms fivefoldP77PartialDomain_negativeReverse_missing
#print axioms fivefoldP77PartialDomain_zeroReverse_missing
#print axioms fivefoldP77TrianglePartialRecovery_exact_boundary

end
end KUOS.Architecture.WuxingPentagonUnified
