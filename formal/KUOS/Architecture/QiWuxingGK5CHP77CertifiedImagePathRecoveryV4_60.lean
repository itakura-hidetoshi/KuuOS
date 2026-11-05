import KUOS.Architecture.QiWuxingGK5CHP77ChargeIncompleteImageObstructionV4_59
import Mathlib.CategoryTheory.Equivalence
import Mathlib.Combinatorics.Quiver.Path
import Mathlib.Tactic

/-!
Qi v4.60 — GENUINE ORIGINAL P77 CERTIFIED-IMAGE PATH RECOVERY.

Qi v4.58 proved the true Mathlib equivalence of original directed
FivefoldEdge free paths with the original P77 conservative 5-cell
CERTIFIED IMAGE, and Qi v4.59 proved that signed charge alone is
not an image-membership certificate, even for charge ZERO.

We now construct a *source-typed* normal form for every actual
original-P77 proof-class arrow in that image, NOT for the entire
original P77 target. Its chosen original free path is unique,
respects identities and composition, and yields an actual functor.
We prove both source/image round trips on actual typed Homs and
objects; exhibit an actual Hom Equiv, and show that original
GK5CG associator charge equals the length of the recovered path.

The new recovery functor is a pointwise strict inverse of the
v4.57 source-to-image factor; it is an explicit representative of
the equivalence confirmed in v4.58. We do NOT identify it by
definitional equality with v4.58's choice-dependent
Equivalence.inverse, do not extract computational witnesses from
the Prop-valued reachability certificate, and do not claim
extension to the whole original P77 quotient category.

A universal typed source-path reconstruction across the FULL
original P77 target is impossible by the already verified genuine
zero-charge off-diagonal original four-proof obstruction.

Append-only, same-root, public roots 107 unchanged; strict 空 center,
independent Kuu one presentation. Original F54/F55/P77/P94A
evidence and C60 physical traces remain separate authorities.
Lean v4.30.0-rc2; pinned mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Protected validation-only PR #1558 stays Draft/open/unmerged.
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

/-- Recover the unique genuinely typed directed finite path of an
original-P77 image Hom. The actual stored *proposition* of source
reachability permits Classical choice, not a fake computational
inverse from the integer charge. -/
def fivefoldP77ImageRecoverPath
    {X Y : FivefoldP77ImagePoint f g h k}
    (A : FivefoldP77ImageHom f g h k X Y) :
    Quiver.Path X.vertex Y.vertex :=
  Classical.choose A.property

/-- Exact original conservative P77 quotient certificate for the
chosen typed path, not an equality between raw P77 syntax trees. -/
theorem fivefoldP77ImageRecoverPath_spec
    {X Y : FivefoldP77ImagePoint f g h k}
    (A : FivefoldP77ImageHom f g h k X Y) :
    (fivefoldP77ConservativeFunctor f g h k).map
      (fivefoldP77ImageRecoverPath f g h k A) = A.val :=
  Classical.choose_spec A.property

/-- The genuinely typed source path normal form is UNIQUE for its
original-P77 proof class by the actual v4.55 faithfulness result. -/
theorem fivefoldP77ImageRecoverPath_unique
    {X Y : FivefoldP77ImagePoint f g h k}
    (A : FivefoldP77ImageHom f g h k X Y)
    (path : Quiver.Path X.vertex Y.vertex)
    (hpath : (fivefoldP77ConservativeFunctor f g h k).map path = A.val) :
    fivefoldP77ImageRecoverPath f g h k A = path := by
  letI := fivefoldP77ConservativeCategory f g h k
  apply (fivefoldP77ConservativeFunctor_faithful_genuine f g h k).map_injective
  exact (fivefoldP77ImageRecoverPath_spec f g h k A).trans hpath.symm

/-- The v4.57 source-to-certified-image factor maps the recovered
path EXACTLY to its original image Hom, retaining actual class. -/
theorem fivefoldP77ImageRecoverPath_factor
    {X Y : FivefoldP77ImagePoint f g h k}
    (A : FivefoldP77ImageHom f g h k X Y) :
    (fivefoldP77ImageFactor f g h k).map
      (fivefoldP77ImageRecoverPath f g h k A) = A := by
  letI := fivefoldP77ConservativeCategory f g h k
  letI := fivefoldP77ImageCategory f g h k
  apply Subtype.ext
  exact fivefoldP77ImageRecoverPath_spec f g h k A

/-- Recovery after image evaluation is the EXACT original typed
free path, not merely an integer-length observational equality. -/
theorem fivefoldP77ImageRecoverPath_of_factor
    {u v : FivefoldPathVertex} (path : Quiver.Path u v) :
    fivefoldP77ImageRecoverPath f g h k
      ((fivefoldP77ImageFactor f g h k).map path) = path := by
  letI := fivefoldP77ConservativeCategory f g h k
  letI := fivefoldP77ImageCategory f g h k
  apply (fivefoldP77ImageFactor_faithful f g h k).map_injective
  exact fivefoldP77ImageRecoverPath_factor f g h k
    ((fivefoldP77ImageFactor f g h k).map path)

/-- The original image identity normalizes to the actual EMPTY
typed finite path, using the faithful source factor and its true
Functor.map_id rather than numerical zero charge. -/
theorem fivefoldP77ImageRecoverPath_id
    (X : FivefoldP77ImagePoint f g h k) :
    fivefoldP77ImageRecoverPath f g h k (𝟙 X) =
      (Quiver.Path.nil : Quiver.Path X.vertex X.vertex) := by
  letI := fivefoldP77ConservativeCategory f g h k
  letI := fivefoldP77ImageCategory f g h k
  apply fivefoldP77ImageRecoverPath_unique f g h k (𝟙 X)
  change (fivefoldP77ConservativeFunctor f g h k).map
      (Quiver.Path.nil : Quiver.Path X.vertex X.vertex) =
    (fivefoldP77ImageId f g h k X).val
  exact (fivefoldP77ConservativeFunctor f g h k).map_id X.vertex

/-- Original image composition normalizes to genuine source
path composition, retaining all original typed endpoints. -/
theorem fivefoldP77ImageRecoverPath_comp
    {X Y Z : FivefoldP77ImagePoint f g h k}
    (A : X ⟶ Y) (B : Y ⟶ Z) :
    fivefoldP77ImageRecoverPath f g h k (A ≫ B) =
      (fivefoldP77ImageRecoverPath f g h k A).comp
        (fivefoldP77ImageRecoverPath f g h k B) := by
  letI := fivefoldP77ConservativeCategory f g h k
  letI := fivefoldP77ImageCategory f g h k
  apply fivefoldP77ImageRecoverPath_unique f g h k (A ≫ B)
  change (fivefoldP77ConservativeFunctor f g h k).map
      ((fivefoldP77ImageRecoverPath f g h k A).comp
        (fivefoldP77ImageRecoverPath f g h k B)) =
    fivefoldP77ConservativeCompose f g h k A.val B.val
  calc
    (fivefoldP77ConservativeFunctor f g h k).map
        ((fivefoldP77ImageRecoverPath f g h k A).comp
          (fivefoldP77ImageRecoverPath f g h k B)) =
      (fivefoldP77ConservativeFunctor f g h k).map
          (fivefoldP77ImageRecoverPath f g h k A) ≫
        (fivefoldP77ConservativeFunctor f g h k).map
          (fivefoldP77ImageRecoverPath f g h k B) :=
      (fivefoldP77ConservativeFunctor f g h k).map_comp _ _
    _ = fivefoldP77ConservativeCompose f g h k A.val B.val := by
      rw [fivefoldP77ImageRecoverPath_spec f g h k A,
        fivefoldP77ImageRecoverPath_spec f g h k B]
      rfl

/-- Concrete Mathlib functor realizing P77 image path recovery,
not an abstract Hom existence statement or a numeric map. -/
def fivefoldP77ImageRecoveryFunctor :
    FivefoldP77ImagePoint f g h k ⥤ FivefoldFreePathCategory := by
  letI := fivefoldP77ConservativeCategory f g h k
  letI := fivefoldP77ImageCategory f g h k
  refine {
    obj := fun X => X.vertex
    map := fun {_ _} A => fivefoldP77ImageRecoverPath f g h k A
    map_id := ?_
    map_comp := ?_
  }
  · intro X
    exact fivefoldP77ImageRecoverPath_id f g h k X
  · intro X Y Z A B
    exact fivefoldP77ImageRecoverPath_comp f g h k A B

/-- The source-to-image and back composite is STRICTLY identity
on every original free-path category object. -/
theorem fivefoldP77ImageRecovery_left_obj
    (u : FivefoldPathVertex) :
    ((fivefoldP77ImageFactor f g h k ⋙
      fivefoldP77ImageRecoveryFunctor f g h k).obj u) = u := rfl

/-- The source-to-image and back composite is STRICTLY identity
on every genuine typed original free-path Hom. -/
theorem fivefoldP77ImageRecovery_left_map
    {u v : FivefoldPathVertex} (path : Quiver.Path u v) :
    (fivefoldP77ImageFactor f g h k ⋙
      fivefoldP77ImageRecoveryFunctor f g h k).map path = path := by
  letI := fivefoldP77ConservativeCategory f g h k
  letI := fivefoldP77ImageCategory f g h k
  exact fivefoldP77ImageRecoverPath_of_factor f g h k path

/-- The image-to-source and back composite is identity on each
actual original-P77 certified-image object, not on the whole target. -/
theorem fivefoldP77ImageRecovery_right_obj
    (X : FivefoldP77ImagePoint f g h k) :
    (fivefoldP77ImageRecoveryFunctor f g h k ⋙
      fivefoldP77ImageFactor f g h k).obj X = X := by
  cases X
  rfl

/-- The image-to-source and back composite is identity on each
actual original-P77 class with genuine finite-path reachability. -/
theorem fivefoldP77ImageRecovery_right_map
    {X Y : FivefoldP77ImagePoint f g h k}
    (A : X ⟶ Y) :
    (fivefoldP77ImageRecoveryFunctor f g h k ⋙
      fivefoldP77ImageFactor f g h k).map A = A := by
  letI := fivefoldP77ConservativeCategory f g h k
  letI := fivefoldP77ImageCategory f g h k
  exact fivefoldP77ImageRecoverPath_factor f g h k A

/-- A full Type-level bijection of actual original-P77 image
Hom with genuine typed original finite paths, using the proof-
relevant source-certified classes and faithful path recovery. -/
def fivefoldP77ImageHomPathEquiv
    (X Y : FivefoldP77ImagePoint f g h k) :
    Quiver.Path X.vertex Y.vertex ≃ FivefoldP77ImageHom f g h k X Y := by
  letI := fivefoldP77ConservativeCategory f g h k
  letI := fivefoldP77ImageCategory f g h k
  refine {
    toFun := fun path => (fivefoldP77ImageFactor f g h k).map path
    invFun := fivefoldP77ImageRecoverPath f g h k
    left_inv := ?_
    right_inv := ?_
  }
  · intro path
    exact fivefoldP77ImageRecoverPath_of_factor f g h k path
  · intro A
    exact fivefoldP77ImageRecoverPath_factor f g h k A

/-- The signed original P77 associator charge of ANY certified
image Hom is exactly the NAT length of its genuinely recovered
typed free path; the charge is an observer AFTER reconstruction. -/
theorem fivefoldP77ImageRecoverPath_charge_length
    {X Y : FivefoldP77ImagePoint f g h k}
    (A : FivefoldP77ImageHom f g h k X Y) :
    fivefoldP77ConservativeCharge f g h k A.val =
      ((fivefoldP77ImageRecoverPath f g h k A).length : ℤ) := by
  letI := fivefoldP77ConservativeCategory f g h k
  calc
    fivefoldP77ConservativeCharge f g h k A.val =
        fivefoldP77ConservativeCharge f g h k
          ((fivefoldP77ConservativeFunctor f g h k).map
            (fivefoldP77ImageRecoverPath f g h k A)) :=
      congrArg (fivefoldP77ConservativeCharge f g h k)
        (fivefoldP77ImageRecoverPath_spec f g h k A).symm
    _ = ((fivefoldP77ImageRecoverPath f g h k A).length : ℤ) :=
      fivefoldP77ConservativeFunctor_charge_length f g h k
        (fivefoldP77ImageRecoverPath f g h k A)

/-- The normalization of original-P77 image composition intertwines
GK5CG charge with the length of the actual composed typed path. -/
theorem fivefoldP77ImageRecoverPath_comp_charge
    {X Y Z : FivefoldP77ImagePoint f g h k}
    (A : X ⟶ Y) (B : Y ⟶ Z) :
    fivefoldP77ConservativeCharge f g h k (A ≫ B).val =
      (((fivefoldP77ImageRecoverPath f g h k A).comp
        (fivefoldP77ImageRecoverPath f g h k B)).length : ℤ) := by
  letI := fivefoldP77ConservativeCategory f g h k
  letI := fivefoldP77ImageCategory f g h k
  calc
    fivefoldP77ConservativeCharge f g h k (A ≫ B).val =
        ((fivefoldP77ImageRecoverPath f g h k (A ≫ B)).length : ℤ) :=
      fivefoldP77ImageRecoverPath_charge_length f g h k (A ≫ B)
    _ = (((fivefoldP77ImageRecoverPath f g h k A).comp
          (fivefoldP77ImageRecoverPath f g h k B)).length : ℤ) := by
      rw [fivefoldP77ImageRecoverPath_comp]

/-- Zero charge of a certified image Hom forces an empty path,
hence actual equality of the original typed endpoints; this does
NOT extend to the genuine v4.59 zero-charge arrow 1 -> 0. -/
theorem fivefoldP77ImageRecoverPath_zero_charge_endpoints
    {X Y : FivefoldP77ImagePoint f g h k}
    (A : FivefoldP77ImageHom f g h k X Y)
    (hz : fivefoldP77ConservativeCharge f g h k A.val = 0) :
    X.vertex = Y.vertex := by
  have hc := fivefoldP77ImageRecoverPath_charge_length f g h k A
  rw [hz] at hc
  have hlen :
      (fivefoldP77ImageRecoverPath f g h k A).length = 0 := by
    exact_mod_cast hc.symm
  exact (fivefoldP77ImageRecoverPath f g h k A).eq_of_length_zero hlen

/-- A global source-path section of the ENTIRE original P77
quotient target cannot exist: v4.59's authentic off-diagonal
zero-charge P77 four-proof cannot be reconstructed as any
original directed FivefoldEdge path. -/
theorem fivefoldP77NoGlobalHomRecovery :
    ¬ (∃ rec :
        (u v : FivefoldPathVertex) →
          FivefoldP77ConservativeClasses f g h k u v → Quiver.Path u v,
       ∀ (u v : FivefoldPathVertex)
         (z : FivefoldP77ConservativeClasses f g h k u v),
         (fivefoldP77ConservativeFunctor f g h k).map (rec u v z) = z) := by
  letI := fivefoldP77ConservativeCategory f g h k
  rintro ⟨rec, hrec⟩
  let u := fivefoldPathVertex 1
  let v := fivefoldPathVertex 0
  let z : FivefoldP77ConservativeClasses f g h k u v :=
    fivefoldP77OriginalZeroChargeReverse01 f g h k
  exact fivefoldP77OriginalZeroChargeReverse01_not_reachable f g h k
    ⟨rec u v z, hrec u v z⟩

#print axioms fivefoldP77ImageRecoverPath
#print axioms fivefoldP77ImageRecoverPath_spec
#print axioms fivefoldP77ImageRecoverPath_unique
#print axioms fivefoldP77ImageRecoverPath_factor
#print axioms fivefoldP77ImageRecoverPath_of_factor
#print axioms fivefoldP77ImageRecoverPath_id
#print axioms fivefoldP77ImageRecoverPath_comp
#print axioms fivefoldP77ImageRecoveryFunctor
#print axioms fivefoldP77ImageRecovery_left_obj
#print axioms fivefoldP77ImageRecovery_left_map
#print axioms fivefoldP77ImageRecovery_right_obj
#print axioms fivefoldP77ImageRecovery_right_map
#print axioms fivefoldP77ImageHomPathEquiv
#print axioms fivefoldP77ImageRecoverPath_charge_length
#print axioms fivefoldP77ImageRecoverPath_comp_charge
#print axioms fivefoldP77ImageRecoverPath_zero_charge_endpoints
#print axioms fivefoldP77NoGlobalHomRecovery

end
end KUOS.Architecture.WuxingPentagonUnified
