import KUOS.Architecture.QiWuxingGK5CHP77FullnessReverseObstructionV4_56
import Mathlib.CategoryTheory.Functor.FullyFaithful
import Mathlib.Tactic

/-!
Qi v4.57 — EXACT GENUINE P77 CERTIFIED IMAGE CATEGORY AND
FULLY FAITHFUL FACTORIZATION WITH NON-FULL ORIGINAL INCLUSION.

The original independent Kuu GK5CG source conservatively generated
five-cell witnesses, Qi v4.53 true typed FivefoldEdge free paths,
Qi v4.54 honest P77 quotient target, Qi v4.55 faithfulness and
Qi v4.56 non-fullness are all retained without alteration.

The image is NOT an observational integer-charge kernel or a
fabricated quotient of C60 geometric Edge lists. Its Hom consists
of an ACTUAL original P77 conservative-five-cell quotient class
together with a proposition that a genuine typed FivefoldEdge
finite path evaluates to that class. The class remains the actual
original four-proof quotient, and the reachability predicate is
precisely Qi v4.56's source-five-cell-certified property.

1. Explicit new wrapped fivefold image objects, avoiding Category
   instance collisions with the original free path and P77 target.
2. Image-Hom subtype of actual original P77 conservative quotient
   classes, with genuine finite-path reachability.
3. Actual Mathlib Category on the image, with id and composition
   inherited from original P77 quotient target AND proved closed
   under source finite-path evaluation and composition.
4. An honest Mathlib functor from original FivefoldFreePathCategory
   to this image Category, which is Full, Faithful and carries
   a genuine Mathlib FullyFaithful witness.
5. A separate inclusion functor into the original conservative
   P77 quotient target, faithful but not full, by the original
   reverse-e01 P77 four-proof charge -1 counterexample.
6. The original v4.54 P77 functor factors EXACTLY through the
   certified image followed by this inclusion. No historical
   higher pentagonator is created or recovered.

The inclusion is a WIDE, NOT FULL, proof-relevant subcategory:
the objects are the same fivefold phases, but its Homs are only
those actual source P77 classes with real finite-path preimages.
The full target retains its genuine inverse P77 four-proofs.
No claim of equivalence with the original FULL P77 target,
no original→phi universal seam, no strict global higher category.

Strict 空 center; independent Kuu is one presentation.
Append-only, same-root. 107 public roots kept unchanged.
Pinned Lean v4.30.0-rc2 / mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Validation-only PR #1558 stays Draft/open/unmerged.
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

/-- An independently wrapped image object, preserving the ORIGINAL
single FivefoldIndex phase without altering the generating quiver. -/
structure FivefoldP77ImagePoint
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₀ r₁)
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₁ r₂)
    (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₂ r₃)
    (k : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₃ r₄) where
  vertex : FivefoldPathVertex

/-- Image HOM: original source P77 proof-relevant 5-cell quotient
class PLUS genuinely typed FivefoldEdge finite-path reachability.
The class is not replaced by its numerical charge or an invented
source arrow. -/
abbrev FivefoldP77ImageHom
    (X Y : FivefoldP77ImagePoint f g h k) :=
  { z : FivefoldP77ConservativeClasses f g h k X.vertex Y.vertex //
    fivefoldP77ConservativeReachable f g h k z }

/-- The true P77 target identity class is reachable by the actual
empty FivefoldEdge free path, preserving exact typed endpoints. -/
def fivefoldP77ImageId
    (X : FivefoldP77ImagePoint f g h k) :
    FivefoldP77ImageHom f g h k X X := by
  letI := fivefoldP77ConservativeCategory f g h k
  refine ⟨(𝟙 (⟨X.vertex⟩ : FivefoldP77ConservativePoint f g h k)), ?_⟩
  refine ⟨(Quiver.Path.nil : Quiver.Path X.vertex X.vertex), ?_⟩
  exact (fivefoldP77ConservativeFunctor f g h k).map_id X.vertex

/-- Source-evaluation image classes are closed under ACTUAL
original-P77 quotient composition; use the original finite-path
composition and the functor law, not integer charge equalities. -/
def fivefoldP77ImageComp
    {X Y Z : FivefoldP77ImagePoint f g h k}
    (A : FivefoldP77ImageHom f g h k X Y)
    (B : FivefoldP77ImageHom f g h k Y Z) :
    FivefoldP77ImageHom f g h k X Z := by
  letI := fivefoldP77ConservativeCategory f g h k
  refine ⟨fivefoldP77ConservativeCompose f g h k A.val B.val, ?_⟩
  obtain ⟨pathA, hA⟩ := A.property
  obtain ⟨pathB, hB⟩ := B.property
  refine ⟨pathA.comp pathB, ?_⟩
  calc
    (fivefoldP77ConservativeFunctor f g h k).map (pathA.comp pathB) =
        (fivefoldP77ConservativeFunctor f g h k).map pathA ≫
          (fivefoldP77ConservativeFunctor f g h k).map pathB :=
      (fivefoldP77ConservativeFunctor f g h k).map_comp pathA pathB
    _ = fivefoldP77ConservativeCompose f g h k A.val B.val := by
      rw [hA, hB]
      rfl

/-- The genuine ORIGINAL P77 target identity is the exact value
of the image identity. Its reachability proof does not alter
the underlying source-conservative quotient class. -/
@[simp] theorem fivefoldP77ImageId_val
    (X : FivefoldP77ImagePoint f g h k) :
    (fivefoldP77ImageId f g h k X).val =
      fivefoldP77ConservativeClass f g h k
        (.refl (fivefoldF55OriginalAt f g h k X.vertex.phase)) := rfl

/-- Genuine image composition projects EXACTLY to existing
original conservative P77 quotient composition. This lemma
exposes the value BEFORE quotient induction on representatives. -/
@[simp] theorem fivefoldP77ImageComp_val
    {X Y Z : FivefoldP77ImagePoint f g h k}
    (A : FivefoldP77ImageHom f g h k X Y)
    (B : FivefoldP77ImageHom f g h k Y Z) :
    (fivefoldP77ImageComp f g h k A B).val =
      fivefoldP77ConservativeCompose f g h k A.val B.val := rfl

/-- The image is an ACTUAL Mathlib Category, not just a type family
or a collection of numerically equal charges. Every category law is
inherited from the TRUE original-P77 conservative-five-cell quotient,
and closure is proved by the honest original path functor. -/
instance fivefoldP77ImageCategory :
    Category (FivefoldP77ImagePoint f g h k) := by
  letI := fivefoldP77ConservativeCategory f g h k
  refine {
    Hom := FivefoldP77ImageHom f g h k
    id := fivefoldP77ImageId f g h k
    comp A B := fivefoldP77ImageComp f g h k A B
    id_comp := ?_
    comp_id := ?_
    assoc := ?_
  }
  · intro X Y A
    apply Subtype.ext
    simp only [fivefoldP77ImageComp_val, fivefoldP77ImageId_val]
    refine _root_.Quotient.inductionOn A.val (fun raw => ?_)
    change fivefoldP77ConservativeClass f g h k
        (.trans (.refl (fivefoldF55OriginalAt f g h k X.vertex.phase)) raw) =
      fivefoldP77ConservativeClass f g h k raw
    exact _root_.Quotient.sound ⟨.verticalLeftUnit raw⟩
  · intro X Y A
    apply Subtype.ext
    simp only [fivefoldP77ImageComp_val, fivefoldP77ImageId_val]
    refine _root_.Quotient.inductionOn A.val (fun raw => ?_)
    change fivefoldP77ConservativeClass f g h k
        (.trans raw (.refl (fivefoldF55OriginalAt f g h k Y.vertex.phase))) =
      fivefoldP77ConservativeClass f g h k raw
    exact _root_.Quotient.sound ⟨.verticalRightUnit raw⟩
  · intro W X Y Z A B C
    apply Subtype.ext
    simp only [fivefoldP77ImageComp_val]
    refine _root_.Quotient.inductionOn A.val (fun a => ?_)
    refine _root_.Quotient.inductionOn B.val (fun b => ?_)
    refine _root_.Quotient.inductionOn C.val (fun c => ?_)
    change fivefoldP77ConservativeClass f g h k
        (.trans (.trans a b) c) =
      fivefoldP77ConservativeClass f g h k
        (.trans a (.trans b c))
    exact _root_.Quotient.sound ⟨.verticalAssoc a b c⟩

/-- Inclusion maps each genuinely reachable ORIGINAL P77 conservative
class to the SAME actual target class. It never changes the class
or reduces it to a charge/physical observation. -/
def fivefoldP77ImageInclusion :
    FivefoldP77ImagePoint f g h k ⥤
      FivefoldP77ConservativePoint f g h k := by
  letI := fivefoldP77ConservativeCategory f g h k
  letI := fivefoldP77ImageCategory f g h k
  refine {
    obj := fun X => ⟨X.vertex⟩
    map := fun {_ _} z => z.val
    map_id := ?_
    map_comp := ?_
  }
  · intro X
    rfl
  · intro X Y Z A B
    rfl

/-- Exact source path to image-category FACTORIZATION. The Hom
value is the real image of the already proved v4.54 original-P77
Functor, equipped with its actual same-path reachability witness. -/
def fivefoldP77ImageFactor :
    FivefoldFreePathCategory ⥤ FivefoldP77ImagePoint f g h k := by
  letI := fivefoldP77ConservativeCategory f g h k
  letI := fivefoldP77ImageCategory f g h k
  refine {
    obj := fun v => ⟨v⟩
    map := fun {_ _} path =>
      ⟨(fivefoldP77ConservativeFunctor f g h k).map path, ⟨path, rfl⟩⟩
    map_id := ?_
    map_comp := ?_
  }
  · intro X
    apply Subtype.ext
    exact (fivefoldP77ConservativeFunctor f g h k).map_id X
  · intro X Y Z A B
    apply Subtype.ext
    exact (fivefoldP77ConservativeFunctor f g h k).map_comp A B

/-- Exact typed FUNCTOR factorization, with no equality of the
original raw P77 proof syntax asserted outside the conservative
five-cell quotient. -/
theorem fivefoldP77Image_factorization :
    fivefoldP77ImageFactor f g h k ⋙
      fivefoldP77ImageInclusion f g h k =
    fivefoldP77ConservativeFunctor f g h k := by
  letI := fivefoldP77ConservativeCategory f g h k
  letI := fivefoldP77ImageCategory f g h k
  rfl

/-- Every HOM in the actual source-certified image Category has a
genuinely typed free FivefoldEdge path preimage. This is true FULL
for the factor, not for its inclusion in the original full P77
quotient target. -/
theorem fivefoldP77ImageFactor_full :
    (fivefoldP77ImageFactor f g h k).Full := by
  letI := fivefoldP77ConservativeCategory f g h k
  letI := fivefoldP77ImageCategory f g h k
  constructor
  intro X Y z
  rcases z with ⟨z, hreach⟩
  obtain ⟨path, hmap⟩ := hreach
  exact ⟨path, Subtype.ext hmap⟩

/-- The source-to-image factor is FAITHFUL because v4.55 already
proved genuine original-P77 target faithfulness for this exact
finite FivefoldEdge quiver. No restriction of the old functor's
source or history is necessary. -/
theorem fivefoldP77ImageFactor_faithful :
    (fivefoldP77ImageFactor f g h k).Faithful := by
  letI := fivefoldP77ConservativeCategory f g h k
  letI := fivefoldP77ImageCategory f g h k
  constructor
  intro X Y A B heq
  have hval := congrArg Subtype.val heq
  exact (fivefoldP77ConservativeFunctor_faithful_genuine f g h k).map_injective hval

/-- Genuine Mathlib FullyFaithful evidence on the exact certified
P77 image Category. A nonfull embedding into the original target
does NOT spoil the full and faithful source-to-image factor. -/
def fivefoldP77ImageFactor_fullyFaithful :
    (fivefoldP77ImageFactor f g h k).FullyFaithful := by
  letI := fivefoldP77ConservativeCategory f g h k
  letI := fivefoldP77ImageCategory f g h k
  letI : (fivefoldP77ImageFactor f g h k).Full :=
    fivefoldP77ImageFactor_full f g h k
  letI : (fivefoldP77ImageFactor f g h k).Faithful :=
    fivefoldP77ImageFactor_faithful f g h k
  exact CategoryTheory.Functor.FullyFaithful.ofFullyFaithful _

/-- The inclusion is faithful: distinct genuinely reachable
classes are distinct actual original P77 conservative target
classes. This is a SUBTYPE embedding, not a charge observation. -/
theorem fivefoldP77ImageInclusion_faithful :
    (fivefoldP77ImageInclusion f g h k).Faithful := by
  letI := fivefoldP77ConservativeCategory f g h k
  letI := fivefoldP77ImageCategory f g h k
  constructor
  intro X Y A B heq
  exact Subtype.ext heq

/-- The original reverse P77 e01 four-proof of signed charge -1
is outside this image Category's Hom at the true phase 1->0.
This is the SAME genuine v4.56 target certificate, not an invented
reverse edge or numerical-quotient shadow. -/
theorem fivefoldP77Image_reverse01_not_included :
    ¬ fivefoldP77ConservativeReachable f g h k
      (fivefoldP77OriginalReverse01 f g h k) :=
  fivefoldP77OriginalReverse01_not_reachable f g h k

/-- Even though the source-to-image factor is FULL, the image
INCLUSION into the actual whole P77 conservative quotient is
NOT FULL. The same original reverse e01 target Hom has no
source-certified image Hom preimage. -/
theorem fivefoldP77ImageInclusion_not_full :
    ¬ (fivefoldP77ImageInclusion f g h k).Full := by
  letI := fivefoldP77ConservativeCategory f g h k
  letI := fivefoldP77ImageCategory f g h k
  intro hfull
  haveI : (fivefoldP77ImageInclusion f g h k).Full := hfull
  let X : FivefoldP77ImagePoint f g h k :=
    ⟨fivefoldPathVertex 1⟩
  let Y : FivefoldP77ImagePoint f g h k :=
    ⟨fivefoldPathVertex 0⟩
  obtain ⟨z, hmap⟩ :=
    (fivefoldP77ImageInclusion f g h k).map_surjective
      (X := X) (Y := Y) (fivefoldP77OriginalReverse01 f g h k)
  have hreach :
      fivefoldP77ConservativeReachable f g h k
        (fivefoldP77OriginalReverse01 f g h k) := by
    change z.val = fivefoldP77OriginalReverse01 f g h k at hmap
    rw [← hmap]
    exact z.property
  exact fivefoldP77Image_reverse01_not_included f g h k hreach

/-- Final exact boundary: an honest P77 proof-relevant fully
faithful factorization, an inclusion faithful but not full, and
its composite equal to the original v4.54 functor. -/
theorem fivefoldP77Image_exact_factorization_split :
    Nonempty (fivefoldP77ImageFactor f g h k).FullyFaithful ∧
    (fivefoldP77ImageInclusion f g h k).Faithful ∧
    ¬ (fivefoldP77ImageInclusion f g h k).Full ∧
    (fivefoldP77ImageFactor f g h k ⋙
      fivefoldP77ImageInclusion f g h k =
      fivefoldP77ConservativeFunctor f g h k) := by
  exact ⟨⟨fivefoldP77ImageFactor_fullyFaithful f g h k⟩,
    fivefoldP77ImageInclusion_faithful f g h k,
    fivefoldP77ImageInclusion_not_full f g h k,
    fivefoldP77Image_factorization f g h k⟩

#print axioms FivefoldP77ImagePoint
#print axioms FivefoldP77ImageHom
#print axioms fivefoldP77ImageId
#print axioms fivefoldP77ImageComp
#print axioms fivefoldP77ImageId_val
#print axioms fivefoldP77ImageComp_val
#print axioms fivefoldP77ImageCategory
#print axioms fivefoldP77ImageInclusion
#print axioms fivefoldP77ImageFactor
#print axioms fivefoldP77Image_factorization
#print axioms fivefoldP77ImageFactor_full
#print axioms fivefoldP77ImageFactor_faithful
#print axioms fivefoldP77ImageFactor_fullyFaithful
#print axioms fivefoldP77ImageInclusion_faithful
#print axioms fivefoldP77Image_reverse01_not_included
#print axioms fivefoldP77ImageInclusion_not_full
#print axioms fivefoldP77Image_exact_factorization_split

end
end KUOS.Architecture.WuxingPentagonUnified
