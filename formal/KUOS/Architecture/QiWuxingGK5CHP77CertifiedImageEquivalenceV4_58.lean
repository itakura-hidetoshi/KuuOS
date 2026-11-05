import KUOS.Architecture.QiWuxingGK5CHP77CertifiedImageFactorizationV4_57
import Mathlib.CategoryTheory.Equivalence
import Mathlib.CategoryTheory.EssentialImage
import Mathlib.Tactic

/-!
Qi v4.58 — GENUINE CATEGORY EQUIVALENCE BETWEEN THE TRUE
FIVEFOLD FREE-PATH CATEGORY AND ITS ORIGINAL-P77 CERTIFIED IMAGE.

The ORIGINAL FivefoldEdge quiver of Qi v3.5/v4.53 has exactly five
directed generators e01, e12, e23, e04, e43. Qi v4.54 built an
original-F55/P77 Type-valued four-proof / GK5CG conservative
five-cell quotient Category. Qi v4.55 proved the free-path functor
faithful, Qi v4.56 proved that it is NOT full using the original
reverse e01 P77 four-proof of signed charge -1, and Qi v4.57
constructed the certified image Category and a FULLY FAITHFUL
factorization through that image.

Here we use the unchanged proof-valued image and show:
* The genuine Mathlib factor functor is surjective ON OBJECTS:
  every independently wrapped FivefoldP77ImagePoint comes from
  its exact original typed FivefoldPathVertex (not a guessed
  numerical or physical representative).
* In particular the factor is genuinely essentially surjective.
* Its already-proved full and faithful maps plus actual essential
  surjectivity give the true Mathlib Functor.IsEquivalence.
* Obtain a DATA-CARRYING Mathlib CategoryTheory.Equivalence from
  the free path Category to the certified image Category, including
  a genuine quasi-inverse Functor and unit/counit natural isomorphisms.
* This equivalence's forward functor is the EXACT original Qi
  v4.57 certified-image factor, without changing source objects
  or target proof classes.
* Composition with the old inclusion is exactly the original
  v4.54 genuine P77 functor. The inclusion remains Faithful
  but NOT Full, while the original whole-target functor is NOT
  an equivalence. No new original P77 inverse edges in the
  FREE quiver, no adjoined pentagonator, no fully-faithful claim
  about the whole original target.

The preserved image-Hom is an ACTUAL original P77 four-proof
conservative 5-cell quotient class with a source-reachability
witness. It is not redefined as a mere path, scalar, charge,
physical C60 Edge, or P94A numerical shadow. Original F54/F55/
P77/P94A source histories, Qi CRT and physical C60 evidence
remain separate authorities; strict 空 remains central and
independent Kuu is one presentation.

Append-only, same-root, public root107. Pinned Lean v4.30.0-rc2,
mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Validation-only PR #1558 Draft/open/unmerged. No new axiom,
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

/-- The TRUE source-to-image factor is surjective on ALL objects:
the proof selects the exact original FivefoldPathVertex stored
inside each independent image wrapper. -/
theorem fivefoldP77ImageFactor_obj_surjective :
    Function.Surjective
      (fivefoldP77ImageFactor f g h k).obj := by
  letI := fivefoldP77ConservativeCategory f g h k
  letI := fivefoldP77ImageCategory f g h k
  intro Y
  exact ⟨Y.vertex, rfl⟩

/-- Hence the actual factor is ESSENTIALLY SURJECTIVE using
its real object-level source preimages, with no numerical
observation or quotient representative selection. -/
theorem fivefoldP77ImageFactor_essSurj :
    (fivefoldP77ImageFactor f g h k).EssSurj := by
  letI := fivefoldP77ConservativeCategory f g h k
  letI := fivefoldP77ImageCategory f g h k
  exact (fivefoldP77ImageFactor f g h k).essSurj_of_surj
    (fivefoldP77ImageFactor_obj_surjective f g h k)

/-- Genuine Mathlib IsEquivalence for the source-to-IMAGE factor:
v4.57 Full + Faithful and actual v4.58 EssSurj. This is NOT an
assertion about the original full conservative P77 target. -/
theorem fivefoldP77ImageFactor_isEquivalence :
    (fivefoldP77ImageFactor f g h k).IsEquivalence := by
  letI := fivefoldP77ConservativeCategory f g h k
  letI := fivefoldP77ImageCategory f g h k
  exact {
    faithful := fivefoldP77ImageFactor_faithful f g h k
    full := fivefoldP77ImageFactor_full f g h k
    essSurj := fivefoldP77ImageFactor_essSurj f g h k
  }

/-- ACTUAL DATA-CARRYING equivalence, not an informal assertion
that the two categories look similar. Mathlib supplies the
quasi-inverse and the unit/counit typed natural isomorphisms. -/
def fivefoldP77ImageEquivalence :
    FivefoldFreePathCategory ≌ FivefoldP77ImagePoint f g h k := by
  letI := fivefoldP77ConservativeCategory f g h k
  letI := fivefoldP77ImageCategory f g h k
  letI : (fivefoldP77ImageFactor f g h k).IsEquivalence :=
    fivefoldP77ImageFactor_isEquivalence f g h k
  exact (fivefoldP77ImageFactor f g h k).asEquivalence

/-- The equivalence's forward functor is EXACTLY the pre-existing
v4.57 original-P77-certified image factor (not just naturally
isomorphic or an unrelated numeric proxy). -/
theorem fivefoldP77ImageEquivalence_functor :
    (fivefoldP77ImageEquivalence f g h k).functor =
      fivefoldP77ImageFactor f g h k := by
  rfl

/-- The constructed equivalence has a genuine inverse functor
from the original source-certified P77 image to the true
fivefold free path category. It is not a functor on all of P77. -/
def fivefoldP77ImageQuasiInverse :
    FivefoldP77ImagePoint f g h k ⥤ FivefoldFreePathCategory :=
  (fivefoldP77ImageEquivalence f g h k).inverse

/-- Unit natural isomorphism of the honest category equivalence,
expressing inverse-after-forward on the original free category. -/
def fivefoldP77ImageUnitIso :
    𝟭 FivefoldFreePathCategory ≅
      fivefoldP77ImageFactor f g h k ⋙
        fivefoldP77ImageQuasiInverse f g h k := by
  letI := fivefoldP77ConservativeCategory f g h k
  letI := fivefoldP77ImageCategory f g h k
  simpa only [fivefoldP77ImageEquivalence_functor,
    fivefoldP77ImageQuasiInverse] using
    (fivefoldP77ImageEquivalence f g h k).unitIso

/-- Counit natural isomorphism, expressing forward-after-inverse
on the actual original-P77 Type-valued certified image Category. -/
def fivefoldP77ImageCounitIso :
    fivefoldP77ImageQuasiInverse f g h k ⋙
      fivefoldP77ImageFactor f g h k ≅
        𝟭 (FivefoldP77ImagePoint f g h k) := by
  letI := fivefoldP77ConservativeCategory f g h k
  letI := fivefoldP77ImageCategory f g h k
  simpa only [fivefoldP77ImageEquivalence_functor,
    fivefoldP77ImageQuasiInverse] using
    (fivefoldP77ImageEquivalence f g h k).counitIso

/-- The equivalence's exact forward factor followed by the
faithful-but-nonfull inclusion is the UNMODIFIED v4.54 original
conservative P77 functor, not an equivalence with that full
target. -/
theorem fivefoldP77ImageEquivalence_comp_inclusion :
    (fivefoldP77ImageEquivalence f g h k).functor ⋙
      fivefoldP77ImageInclusion f g h k =
        fivefoldP77ConservativeFunctor f g h k := by
  rw [fivefoldP77ImageEquivalence_functor]
  exact fivefoldP77Image_factorization f g h k

/-- The ORIGINAL whole-target P77 functor cannot be a Mathlib
IsEquivalence because it is proven nonfull in v4.56. -/
theorem fivefoldP77ConservativeFunctor_not_isEquivalence :
    ¬ (fivefoldP77ConservativeFunctor f g h k).IsEquivalence := by
  letI := fivefoldP77ConservativeCategory f g h k
  intro he
  exact fivefoldP77ConservativeFunctor_not_full f g h k he.full

/-- The inclusion of the certified image into the WHOLE original
P77 conservative quotient is also not a category equivalence
since its reverse e01 target Hom remains unreachable. -/
theorem fivefoldP77ImageInclusion_not_isEquivalence :
    ¬ (fivefoldP77ImageInclusion f g h k).IsEquivalence := by
  letI := fivefoldP77ConservativeCategory f g h k
  letI := fivefoldP77ImageCategory f g h k
  intro he
  exact fivefoldP77ImageInclusion_not_full f g h k he.full

/-- Sharp boundary: the true finite free category is EQUIVALENT
to its exact proof-certified image, while the original full P77
target is NOT equivalent by this factor/inclusion. We preserve
the true P77 inverse and all proof-constructor histories. -/
theorem fivefoldP77ImageEquivalence_obstruction_split :
    Nonempty (FivefoldFreePathCategory ≌
      FivefoldP77ImagePoint f g h k) ∧
    ¬ (fivefoldP77ImageInclusion f g h k).IsEquivalence ∧
    (fivefoldP77ImageEquivalence f g h k).functor ⋙
      fivefoldP77ImageInclusion f g h k =
        fivefoldP77ConservativeFunctor f g h k := by
  exact ⟨⟨fivefoldP77ImageEquivalence f g h k⟩,
    fivefoldP77ImageInclusion_not_isEquivalence f g h k,
    fivefoldP77ImageEquivalence_comp_inclusion f g h k⟩

#print axioms fivefoldP77ImageFactor_obj_surjective
#print axioms fivefoldP77ImageFactor_essSurj
#print axioms fivefoldP77ImageFactor_isEquivalence
#print axioms fivefoldP77ImageEquivalence
#print axioms fivefoldP77ImageEquivalence_functor
#print axioms fivefoldP77ImageQuasiInverse
#print axioms fivefoldP77ImageUnitIso
#print axioms fivefoldP77ImageCounitIso
#print axioms fivefoldP77ImageEquivalence_comp_inclusion
#print axioms fivefoldP77ConservativeFunctor_not_isEquivalence
#print axioms fivefoldP77ImageInclusion_not_isEquivalence
#print axioms fivefoldP77ImageEquivalence_obstruction_split

end
end KUOS.Architecture.WuxingPentagonUnified
