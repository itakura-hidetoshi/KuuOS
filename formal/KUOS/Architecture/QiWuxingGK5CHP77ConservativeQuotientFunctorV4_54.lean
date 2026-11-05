import KUOS.Architecture.QiWuxingGK5CHFivefoldFreePathOriginalP77V4_53
import Mathlib.CategoryTheory.PathCategory.Basic
import Mathlib.Tactic

/-!
Qi v4.54 — GENUINE ORIGINAL P77 4-PROOF QUOTIENT BY CONSERVATIVE 5-CELLS.

The quotient below is NOT a numeric charge-kernel or a quotient of
the physical C60 edge list. Each Hom is the quotient of the ACTUAL
dependently typed original P77 four-proof terms, and its Setoid is
defined ONLY by existence of a GK5CG conservative Type-valued 5-cell.
This evidence includes vertical congruence, associativity, units,
inverses and the original F55 whisker congruences, but does NOT
contain an adjoined pentagonator.

A new, independently indexed fivefold target object wrapper prevents
Category instances from silently changing the existing Qi or free
path presentations. Genuine quotient vertical composition is induced
by the original P77 trans constructor, and category equations are
proved from conservative five-cell certificates.

Mathlib Paths.lift then constructs the actual functor from the
fivefold free path category. Its arrow map is proved equal to the
quotient class of the original recursively evaluated P77 four-proof,
for ALL typed finite paths. Equality of functor images has an exact
source five-cell witness iff. This yields the sharp per-Hom and global
faithfulness criteria; no unconditional faithfulness is assumed.

Original GK5CG associator charge descends to the conservative quotient.
The upper three-edge and lower two-edge paths still have different
images. The original P77 five-cell obstruction survives genuine
categorification instead of being erased by an observational shadow.

Strict 空 is the center; independent Kuu remains one presentation.
Append-only; original 107 roots and historical proof sources unchanged.
Lean v4.30.0-rc2; mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Protected validation-only #1558 stays Draft/open/unmerged.
No new axioms/sorry/admit/Gray.
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

/-- The exact conservative source-five-cell relation, not charge
equality. All endpoints retain their actual dependent original
P77/F55 source and target types. -/
def fivefoldP77ConservativeSetoid
    {u v : FivefoldPathVertex} :
    Setoid (NativeF55RawVerticalFourCell first last
      (fivefoldF55OriginalAt f g h k u.phase)
      (fivefoldF55OriginalAt f g h k v.phase)) where
  r := fun w z =>
    Nonempty (NativeGK5CGConservativeFiveCell first last w z)
  iseqv := ⟨
    (fun w => ⟨.refl w⟩),
    (fun w => w.elim (fun cert => ⟨.symm cert⟩)),
    (fun w z => w.elim (fun a =>
      z.elim (fun b => ⟨.trans a b⟩)))⟩

/-- Genuine P77 Hom modulo EXACT conservative 5-cell evidence,
rather than equality of numerical or physical observations. -/
abbrev FivefoldP77ConservativeClasses
    (u v : FivefoldPathVertex) :=
  _root_.Quotient (fivefoldP77ConservativeSetoid f g h k (u := u) (v := v))

/-- Projection of an original typed four-proof, with source history
available upstream and no replacement of the original datatype. -/
def fivefoldP77ConservativeClass
    {u v : FivefoldPathVertex}
    (w : NativeF55RawVerticalFourCell first last
      (fivefoldF55OriginalAt f g h k u.phase)
      (fivefoldF55OriginalAt f g h k v.phase)) :
    FivefoldP77ConservativeClasses f g h k u v :=
  _root_.Quotient.mk _ w

/-- The quotient's exact kernel is source Type-valued conservative
5-cell EXISTENCE, not GK5CG charge equality. -/
theorem fivefoldP77ConservativeClass_eq_iff
    {u v : FivefoldPathVertex}
    (w z : NativeF55RawVerticalFourCell first last
      (fivefoldF55OriginalAt f g h k u.phase)
      (fivefoldF55OriginalAt f g h k v.phase)) :
    fivefoldP77ConservativeClass f g h k w =
      fivefoldP77ConservativeClass f g h k z ↔
    Nonempty (NativeGK5CGConservativeFiveCell first last w z) := by
  constructor
  · intro eq
    exact _root_.Quotient.exact eq
  · intro cert
    exact _root_.Quotient.sound cert

/-- True quotient of original four-proof vertical pasting, well
defined using the two ORIGINAL GK5CG five-cell congruence rules. -/
def fivefoldP77ConservativeCompose
    {u v w : FivefoldPathVertex}
    (A : FivefoldP77ConservativeClasses f g h k u v)
    (B : FivefoldP77ConservativeClasses f g h k v w) :
    FivefoldP77ConservativeClasses f g h k u w :=
  _root_.Quotient.liftOn₂ A B
    (fun x y => fivefoldP77ConservativeClass f g h k (.trans x y))
    (by
      intro x x' y y' hxx' hyy'
      apply _root_.Quotient.sound
      rcases hxx' with ⟨certX⟩
      rcases hyy' with ⟨certY⟩
      exact ⟨.trans (.verticalLeft certX y)
        (.verticalRight x' certY)⟩)

/-- Representative equation for the ACTUAL original P77 vertical
constructor; not an equality between raw proof trees. -/
theorem fivefoldP77ConservativeCompose_class
    {u v w : FivefoldPathVertex}
    (A : NativeF55RawVerticalFourCell first last
      (fivefoldF55OriginalAt f g h k u.phase)
      (fivefoldF55OriginalAt f g h k v.phase))
    (B : NativeF55RawVerticalFourCell first last
      (fivefoldF55OriginalAt f g h k v.phase)
      (fivefoldF55OriginalAt f g h k w.phase)) :
    fivefoldP77ConservativeCompose f g h k
        (fivefoldP77ConservativeClass f g h k A)
        (fivefoldP77ConservativeClass f g h k B) =
      fivefoldP77ConservativeClass f g h k (.trans A B) := rfl

/-- NEW target presentation. This object wrapper avoids conflicting
Category instances on the free path category or on FivePhase. -/
structure FivefoldP77ConservativePoint where
  vertex : FivefoldPathVertex

/-- The fully dependent ORIGINAL P77 target category with Homs equal
to conservative-five-cell classes. Strictness is derived ONLY AFTER
quotienting by the explicit source Type-valued five-cells. -/
instance fivefoldP77ConservativeCategory :
    Category (FivefoldP77ConservativePoint) where
  Hom X Y := FivefoldP77ConservativeClasses f g h k X.vertex Y.vertex
  id X := fivefoldP77ConservativeClass f g h k
    (.refl (fivefoldF55OriginalAt f g h k X.vertex.phase))
  comp A B := fivefoldP77ConservativeCompose f g h k A B
  id_comp := by
    intro X Y q
    refine _root_.Quotient.inductionOn q (fun raw => ?_)
    change fivefoldP77ConservativeClass f g h k
        (.trans (.refl (fivefoldF55OriginalAt f g h k X.vertex.phase)) raw) =
      fivefoldP77ConservativeClass f g h k raw
    exact _root_.Quotient.sound ⟨.verticalLeftUnit raw⟩
  comp_id := by
    intro X Y q
    refine _root_.Quotient.inductionOn q (fun raw => ?_)
    change fivefoldP77ConservativeClass f g h k
        (.trans raw (.refl (fivefoldF55OriginalAt f g h k Y.vertex.phase))) =
      fivefoldP77ConservativeClass f g h k raw
    exact _root_.Quotient.sound ⟨.verticalRightUnit raw⟩
  assoc := by
    intro W X Y Z A B C
    refine _root_.Quotient.inductionOn A (fun a => ?_)
    refine _root_.Quotient.inductionOn B (fun b => ?_)
    refine _root_.Quotient.inductionOn C (fun c => ?_)
    change fivefoldP77ConservativeClass f g h k
        (.trans (.trans a b) c) =
      fivefoldP77ConservativeClass f g h k
        (.trans a (.trans b c))
    exact _root_.Quotient.sound ⟨.verticalAssoc a b c⟩

/-- An original fivefold generator maps to the CLASS of the ACTUAL
P77 four-proof selected by its typed FivefoldEdge. -/
def fivefoldP77ConservativeEdgePrefunctor :
    FivefoldPathVertex ⥤q FivefoldP77ConservativePoint :=
  letI := fivefoldP77ConservativeCategory f g h k
  {
    obj := fun vertex => ⟨vertex⟩
    map := fun {_ _} arrow =>
      fivefoldP77ConservativeClass f g h k
        (fivefoldArrowOriginalP77 f g h k arrow)
  }

/-- Genuine Mathlib FUNCTOR from the real free typed fivefold path
category into the conservative source-P77 quotient target category. -/
def fivefoldP77ConservativeFunctor :
    FivefoldFreePathCategory ⥤ FivefoldP77ConservativePoint :=
  letI := fivefoldP77ConservativeCategory f g h k
  CategoryTheory.Paths.lift (fivefoldP77ConservativeEdgePrefunctor f g h k)

/-- Evaluating a FINITE PATH by the functor is exactly the
conservative class of its ORIGINAL recursively constructed P77
four-proof. This holds for every typed finite path, not just the
two displayed pentagon routes. -/
theorem fivefoldP77ConservativeFunctor_map_spec
    {u v : FivefoldPathVertex} (path : Quiver.Path u v) :
    (fivefoldP77ConservativeFunctor f g h k).map path =
      fivefoldP77ConservativeClass f g h k
        (fivefoldEvaluateP77 f g h k path) := by
  letI := fivefoldP77ConservativeCategory f g h k
  induction path with
  | nil =>
      rfl
  | cons path arrow ih =>
      change
        fivefoldP77ConservativeCompose f g h k
          ((fivefoldP77ConservativeFunctor f g h k).map path)
          (fivefoldP77ConservativeClass f g h k
            (fivefoldArrowOriginalP77 f g h k arrow)) =
        fivefoldP77ConservativeClass f g h k
          (.trans (fivefoldEvaluateP77 f g h k path)
            (fivefoldArrowOriginalP77 f g h k arrow))
      rw [ih]
      rfl

/-- Precise kernel of the actual quotient functor:
two free paths have the same target morphism IFF their ORIGINAL P77
four-proofs are connected by an ACTUAL conservative 5-cell. -/
theorem fivefoldP77ConservativeFunctor_map_eq_iff
    {u v : FivefoldPathVertex} (A B : Quiver.Path u v) :
    (fivefoldP77ConservativeFunctor f g h k).map A =
      (fivefoldP77ConservativeFunctor f g h k).map B ↔
    Nonempty (NativeGK5CGConservativeFiveCell first last
      (fivefoldEvaluateP77 f g h k A)
      (fivefoldEvaluateP77 f g h k B)) := by
  letI := fivefoldP77ConservativeCategory f g h k
  rw [fivefoldP77ConservativeFunctor_map_spec,
    fivefoldP77ConservativeFunctor_map_spec]
  exact fivefoldP77ConservativeClass_eq_iff f g h k _ _

/-- Exact NECESSARY AND SUFFICIENT faithfulness condition on a
fixed typed Hom. The condition is source-five-cell reflection,
not injectivity of an invented charge-only quotient. -/
theorem fivefoldP77ConservativeFunctor_injective_iff
    {u v : FivefoldPathVertex} :
    Function.Injective
      (fun path : Quiver.Path u v =>
        (fivefoldP77ConservativeFunctor f g h k).map path) ↔
    (∀ A B : Quiver.Path u v,
      Nonempty (NativeGK5CGConservativeFiveCell first last
        (fivefoldEvaluateP77 f g h k A)
        (fivefoldEvaluateP77 f g h k B)) → A = B) := by
  letI := fivefoldP77ConservativeCategory f g h k
  constructor
  · intro inj A B hcert
    exact inj ((fivefoldP77ConservativeFunctor_map_eq_iff
      f g h k A B).2 hcert)
  · intro reflect A B eq
    exact reflect A B ((fivefoldP77ConservativeFunctor_map_eq_iff
      f g h k A B).1 eq)

/-- Global categorical faithfulness is equivalent to reflection of
all source conservative five-cell witnesses between evaluated paths.
No unverified claim that this condition always holds. -/
theorem fivefoldP77ConservativeFunctor_faithful_iff :
    (fivefoldP77ConservativeFunctor f g h k).Faithful ↔
    (∀ {u v : FivefoldPathVertex} (A B : Quiver.Path u v),
      Nonempty (NativeGK5CGConservativeFiveCell first last
        (fivefoldEvaluateP77 f g h k A)
        (fivefoldEvaluateP77 f g h k B)) → A = B) := by
  letI := fivefoldP77ConservativeCategory f g h k
  constructor
  · intro hf u v A B cert
    exact hf.map_injective
      ((fivefoldP77ConservativeFunctor_map_eq_iff f g h k A B).2 cert)
  · intro reflect
    constructor
    intro X Y A B eq
    exact reflect A B
      ((fivefoldP77ConservativeFunctor_map_eq_iff f g h k A B).1 eq)

/-- The ACTUAL original P77 signed four-associator charge DESCENDS
to the conservative quotient by GK5CG five-cell soundness. It does
not identify classes having equal integer charge. -/
def fivefoldP77ConservativeCharge
    {u v : FivefoldPathVertex} :
    FivefoldP77ConservativeClasses f g h k u v → ℤ :=
  _root_.Quotient.lift
    (fun w => w.gk5cgAssocCharge)
    (by
      intro w z h5
      rcases h5 with ⟨cert⟩
      exact cert.assocCharge_sound)

/-- The functor's charge is the EXACT finite-path length, now in
the genuine conservative P77 target category. -/
theorem fivefoldP77ConservativeFunctor_charge_length
    {u v : FivefoldPathVertex} (path : Quiver.Path u v) :
    fivefoldP77ConservativeCharge f g h k
      ((fivefoldP77ConservativeFunctor f g h k).map path) =
        (path.length : ℤ) := by
  letI := fivefoldP77ConservativeCategory f g h k
  rw [fivefoldP77ConservativeFunctor_map_spec]
  exact fivefoldEvaluateP77_charge_length f g h k path

/-- The real upper and lower pentagon free paths REMAIN DISTINCT in
the conservative P77 TARGET category. Their original five-cell
obstruction is preserved under quotient descent. -/
theorem fivefoldP77ConservativeFunctor_upper_ne_lower :
    (fivefoldP77ConservativeFunctor f g h k).map fivefoldFreeUpper ≠
      (fivefoldP77ConservativeFunctor f g h k).map fivefoldFreeLower := by
  letI := fivefoldP77ConservativeCategory f g h k
  intro heq
  exact fivefoldFreeTwoEvaluations_noConservativeFiveCell f g h k
    ((fivefoldP77ConservativeFunctor_map_eq_iff
      f g h k fivefoldFreeUpper fivefoldFreeLower).1 heq)

#print axioms fivefoldP77ConservativeSetoid
#print axioms FivefoldP77ConservativeClasses
#print axioms fivefoldP77ConservativeClass
#print axioms fivefoldP77ConservativeClass_eq_iff
#print axioms fivefoldP77ConservativeCompose
#print axioms fivefoldP77ConservativeCompose_class
#print axioms FivefoldP77ConservativePoint
#print axioms fivefoldP77ConservativeCategory
#print axioms fivefoldP77ConservativeEdgePrefunctor
#print axioms fivefoldP77ConservativeFunctor
#print axioms fivefoldP77ConservativeFunctor_map_spec
#print axioms fivefoldP77ConservativeFunctor_map_eq_iff
#print axioms fivefoldP77ConservativeFunctor_injective_iff
#print axioms fivefoldP77ConservativeFunctor_faithful_iff
#print axioms fivefoldP77ConservativeCharge
#print axioms fivefoldP77ConservativeFunctor_charge_length
#print axioms fivefoldP77ConservativeFunctor_upper_ne_lower

end
end KUOS.Architecture.WuxingPentagonUnified
