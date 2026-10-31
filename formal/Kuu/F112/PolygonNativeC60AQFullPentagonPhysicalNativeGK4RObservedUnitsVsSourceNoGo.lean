import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4QDependentObservationImage
import Mathlib.Tactic

/-!
# F112-P94D3GK4R — observed unitality versus true original P92B no-unit

Keep the REAL original P92B existence quotient, the two independent D/E
categories, F19/F28 Blocks, paired Nat depths, typed original F45 trees,
and the GK4Q actual observation image at every hom boundary.

The actual GK4G Boolean image multiplication has genuine typed left/right
units: the image of the honest original zero-edge F54 unit route, which has
Boolean observation true. The Boolean image multiplication is associative.
In sharp contrast, GK4J proves no original P92B endomorphism class is a
left/right identity for its ORIGINAL induced composition. Therefore a
nonfaithful observable image may be unital even though its source is not.

The finer GK4K Option Nat image multiplication is also associative
(ambient none-absorbing addition). Its genuine source-witnessed image
contains some 1, but no some 0. For EVERY proposed image left/right
identity e, multiplication with some 1 fails: none is absorbing and
some n with n>0 yields some(n+1), not some 1. Thus no left, right or
two-sided identity exists in the actual Option Nat self-hom image at
ANY inhabited typed original F45 stage. This is not merely ambient
Option Nat's obvious some 0 unit: the argument handles the true image
and every candidate in it.

The original Type-valued F54 unit seams live only in the INDEPENDENT
structural comparison quotient; no new P92B 3-cell or associativity
proof is manufactured. True C60 north F45 triple is an unconditional
physical instance. All observation, non-injectivity and authority
boundaries are preserved.

No historical full P92B/F19/F28/F54/F55 typed equivalence, true 14D
unconditional Countable, true 19D filler, global strict n or hyperdescent.
Lean 4.30.0-rc2, mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Append-only / same-root, 107 public roots unchanged, no Gray. Protect
validation-only PR #1558 Draft/open/unmerged.
Copyright 板倉英俊 / Hidetoshi Itakura. Apache-2.0.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uD vD uE vE

section ObservedProducts
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}
variable {n₁ n₂ n₃ n₄ m₁ m₂ m₃ m₄ : Nat}
variable (t₁ : KuuNativeF45Tree p n₁ m₁ ma pa mb pb)
variable (t₂ : KuuNativeF45Tree p n₂ m₂ ma pa mb pb)
variable (t₃ : KuuNativeF45Tree p n₃ m₃ ma pa mb pb)
variable (t₄ : KuuNativeF45Tree p n₄ m₄ ma pa mb pb)

/-- Genuine GK4Q image-level Boolean composition, not a new source P92B
operation or a P92B category instance. -/
def nativeGK4RBoolCompose
    (u : NativeGK4QImage (nativeGK4OBooleanFamily p D E) t₁ t₂)
    (v : NativeGK4QImage (nativeGK4OBooleanFamily p D E) t₂ t₃) :
    NativeGK4QImage (nativeGK4OBooleanFamily p D E) t₁ t₃ :=
  nativeGK4QImageCompose (nativeGK4OBooleanFamily p D E) Bool.and
    (nativeGK4PIdentityAction p D E Bool)
    (nativeGK4PIdentityAction p D E Bool)
    nativeGK4P_boolean_laws t₁ t₂ t₃ u v

/-- Actual GK4K image-level absorbing addition, only on truly observed
Option Nat values and their genuinely typed P92B source witnesses. -/
def nativeGK4ROptionCompose
    (u : NativeGK4QImage (nativeGK4OOptionFamily p D E) t₁ t₂)
    (v : NativeGK4QImage (nativeGK4OOptionFamily p D E) t₂ t₃) :
    NativeGK4QImage (nativeGK4OOptionFamily p D E) t₁ t₃ :=
  nativeGK4QImageCompose (nativeGK4OOptionFamily p D E) nativeGK4KAdd
    (nativeGK4PIdentityAction p D E (Option Nat))
    (nativeGK4PIdentityAction p D E (Option Nat))
    nativeGK4P_option_laws t₁ t₂ t₃ u v

/-- Boolean image composition inherits associativity from Bool.and. -/
theorem nativeGK4RBoolCompose_assoc
    (u : NativeGK4QImage (nativeGK4OBooleanFamily p D E) t₁ t₂)
    (v : NativeGK4QImage (nativeGK4OBooleanFamily p D E) t₂ t₃)
    (w : NativeGK4QImage (nativeGK4OBooleanFamily p D E) t₃ t₄) :
    nativeGK4RBoolCompose t₁ t₃ t₄
      (nativeGK4RBoolCompose t₁ t₂ t₃ u v) w =
    nativeGK4RBoolCompose t₁ t₂ t₄ u
      (nativeGK4RBoolCompose t₂ t₃ t₄ v w) := by
  exact nativeGK4QImageCompose_assoc (nativeGK4OBooleanFamily p D E) Bool.and
    (nativeGK4PIdentityAction p D E Bool)
    (nativeGK4PIdentityAction p D E Bool)
    nativeGK4P_boolean_laws
    (by intro a b c; cases a <;> cases b <;> cases c <;> rfl)
    t₁ t₂ t₃ t₄ u v w

/-- The finer Option Nat image composition is associative, while
having no unit: this does not prove associativity of its P92B source. -/
theorem nativeGK4ROptionCompose_assoc
    (u : NativeGK4QImage (nativeGK4OOptionFamily p D E) t₁ t₂)
    (v : NativeGK4QImage (nativeGK4OOptionFamily p D E) t₂ t₃)
    (w : NativeGK4QImage (nativeGK4OOptionFamily p D E) t₃ t₄) :
    nativeGK4ROptionCompose t₁ t₃ t₄
      (nativeGK4ROptionCompose t₁ t₂ t₃ u v) w =
    nativeGK4ROptionCompose t₁ t₂ t₄ u
      (nativeGK4ROptionCompose t₂ t₃ t₄ v w) := by
  exact nativeGK4QImageCompose_assoc (nativeGK4OOptionFamily p D E) nativeGK4KAdd
    (nativeGK4PIdentityAction p D E (Option Nat))
    (nativeGK4PIdentityAction p D E (Option Nat))
    nativeGK4P_option_laws nativeGK4KAdd_assoc
    t₁ t₂ t₃ t₄ u v w

end ObservedProducts

section GenuineImageUnits
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}
variable {n m : Nat}
variable (tree : KuuNativeF45Tree p n m ma pa mb pb)

/-- The Boolean image of the actual ORIGINAL P92B zero-edge unit,
not an artificial constant true without original route provenance. -/
def nativeGK4RBoolUnit :
    NativeGK4QImage (nativeGK4OBooleanFamily p D E) tree tree :=
  nativeGK4QOfClass (nativeGK4OBooleanFamily p D E) tree tree
    (nativeGK4H_p92Unit tree)

/-- The original unit-route's real physical zero-rotation observation. -/
theorem nativeGK4RBoolUnit_value :
    (nativeGK4RBoolUnit tree).val = true := by
  rfl

/-- At ANY fully typed original F45 target, the Boolean image of the
zero-route source unit acts as a genuine left image identity. -/
theorem nativeGK4RBool_leftUnit
    {n' m' : Nat}
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (z : NativeGK4QImage (nativeGK4OBooleanFamily p D E) tree last) :
    nativeGK4RBoolCompose tree tree last (nativeGK4RBoolUnit tree) z = z := by
  apply Subtype.ext
  change Bool.and (nativeGK4RBoolUnit tree).val z.val = z.val
  rw [nativeGK4RBoolUnit_value]
  cases z.val <;> rfl

/-- At ANY fully typed original F45 source, the same witnessed Boolean
unit acts as a genuine right image identity. -/
theorem nativeGK4RBool_rightUnit
    {n' m' : Nat}
    (first : KuuNativeF45Tree p n' m' ma pa mb pb)
    (z : NativeGK4QImage (nativeGK4OBooleanFamily p D E) first tree) :
    nativeGK4RBoolCompose first tree tree z (nativeGK4RBoolUnit tree) = z := by
  apply Subtype.ext
  change Bool.and z.val (nativeGK4RBoolUnit tree).val = z.val
  rw [nativeGK4RBoolUnit_value]
  cases z.val <;> rfl

/-- The Boolean image is genuinely two-sided unital even though NONE of
the original source P92B endomorphism classes is a left identity under
the original GK4H composition. There is no reflection of equality. -/
theorem nativeGK4RBool_unital_image_but_no_source_identity :
    (∀ z : NativeGK4QImage (nativeGK4OBooleanFamily p D E) tree tree,
      nativeGK4RBoolCompose tree tree tree (nativeGK4RBoolUnit tree) z = z) ∧
    (∀ z : NativeGK4QImage (nativeGK4OBooleanFamily p D E) tree tree,
      nativeGK4RBoolCompose tree tree tree z (nativeGK4RBoolUnit tree) = z) ∧
    (¬ ∃ e : NativeF55P92AssocRouteClasses tree tree,
      ∀ q : NativeF55P92AssocRouteClasses tree tree,
        nativeGK4H_p92Compose tree tree tree e q = q ∧
        nativeGK4H_p92Compose tree tree tree q e = q) := by
  refine ⟨nativeGK4RBool_leftUnit tree tree,
    nativeGK4RBool_rightUnit tree tree, ?_⟩
  rintro ⟨e, he⟩
  exact nativeGK4J_no_any_P92B_left_identity tree e
    (fun q => (he q).1)

/-- This particular original source unit is genuinely a non-left-unit;
its Boolean projection is the actual image unit above. -/
theorem nativeGK4RBool_specific_source_unit_not_left :
    (∀ z : NativeGK4QImage (nativeGK4OBooleanFamily p D E) tree tree,
      nativeGK4RBoolCompose tree tree tree (nativeGK4RBoolUnit tree) z = z) ∧
    ¬ (∀ q : NativeF55P92AssocRouteClasses tree tree,
      nativeGK4H_p92Compose tree tree tree (nativeGK4H_p92Unit tree) q = q) := by
  exact ⟨nativeGK4RBool_leftUnit tree tree,
    nativeGK4J_no_any_P92B_left_identity tree (nativeGK4H_p92Unit tree)⟩

/-- A TRUE original zero-rotation unit tower supplies SOME ONE in the
actual original P92B numeric image. It is not merely an ambient value. -/
def nativeGK4ROptionOne :
    NativeGK4QImage (nativeGK4OOptionFamily p D E) tree tree :=
  nativeGK4QOfClass (nativeGK4OOptionFamily p D E) tree tree
    (nativeGK4ETowerClass tree 0)

theorem nativeGK4ROptionOne_value :
    (nativeGK4ROptionOne tree).val = some 1 := by
  change nativeGK4KP92Option tree tree (nativeGK4ETowerClass tree 0) = some 1
  simpa using (nativeGK4L_unitTower_option tree 0)

/-- No candidate from the TRUE Option Nat image acts as left identity
even on the single witnessed observation some 1. -/
theorem nativeGK4ROption_no_left_identity_at_one
    (e : NativeGK4QImage (nativeGK4OOptionFamily p D E) tree tree) :
    nativeGK4ROptionCompose tree tree tree e (nativeGK4ROptionOne tree) ≠
      nativeGK4ROptionOne tree := by
  intro heq
  have hv := congrArg Subtype.val heq
  change nativeGK4KAdd e.val (nativeGK4ROptionOne tree).val =
    (nativeGK4ROptionOne tree).val at hv
  rw [nativeGK4ROptionOne_value] at hv
  cases he : e.val with
  | none =>
      simp [he] at hv
  | some k =>
      have hk : 0 < k := by
        obtain ⟨q, hq⟩ := e.property
        exact nativeGK4KP92Option_some_pos tree tree q k (hq.trans he)
      have hnum : k + 1 = 1 := by
        simpa [he, nativeGK4KAdd] using hv
      omega

/-- No actual Option Nat image candidate acts as right identity,
even on the same true zero-rotation primitive unit-route observation. -/
theorem nativeGK4ROption_no_right_identity_at_one
    (e : NativeGK4QImage (nativeGK4OOptionFamily p D E) tree tree) :
    nativeGK4ROptionCompose tree tree tree (nativeGK4ROptionOne tree) e ≠
      nativeGK4ROptionOne tree := by
  intro heq
  have hv := congrArg Subtype.val heq
  change nativeGK4KAdd (nativeGK4ROptionOne tree).val e.val =
    (nativeGK4ROptionOne tree).val at hv
  rw [nativeGK4ROptionOne_value] at hv
  cases he : e.val with
  | none =>
      simp [he] at hv
  | some k =>
      have hk : 0 < k := by
        obtain ⟨q, hq⟩ := e.property
        exact nativeGK4KP92Option_some_pos tree tree q k (hq.trans he)
      have hnum : 1 + k = 1 := by
        simpa [he, nativeGK4KAdd] using hv
      omega

/-- The true numerical image has NO left identity, not even an exotic
none or positive-some candidate. -/
theorem nativeGK4ROption_no_left_identity :
    ¬ ∃ e : NativeGK4QImage (nativeGK4OOptionFamily p D E) tree tree,
      ∀ z : NativeGK4QImage (nativeGK4OOptionFamily p D E) tree tree,
        nativeGK4ROptionCompose tree tree tree e z = z := by
  rintro ⟨e, hleft⟩
  exact nativeGK4ROption_no_left_identity_at_one tree e
    (hleft (nativeGK4ROptionOne tree))

/-- The true numerical image has NO right identity. -/
theorem nativeGK4ROption_no_right_identity :
    ¬ ∃ e : NativeGK4QImage (nativeGK4OOptionFamily p D E) tree tree,
      ∀ z : NativeGK4QImage (nativeGK4OOptionFamily p D E) tree tree,
        nativeGK4ROptionCompose tree tree tree z e = z := by
  rintro ⟨e, hright⟩
  exact nativeGK4ROption_no_right_identity_at_one tree e
    (hright (nativeGK4ROptionOne tree))

/-- Both Boolean and Option Nat observable products are associative,
but their actual unitality differs; no law is reflected back into the
nonfaithful original P92B witness-existence quotient. -/
theorem nativeGK4ROption_assoc_but_no_unit :
    (∀ u v w : NativeGK4QImage (nativeGK4OOptionFamily p D E) tree tree,
      nativeGK4ROptionCompose tree tree tree
          (nativeGK4ROptionCompose tree tree tree u v) w =
        nativeGK4ROptionCompose tree tree tree u
          (nativeGK4ROptionCompose tree tree tree v w)) ∧
    (¬ ∃ e : NativeGK4QImage (nativeGK4OOptionFamily p D E) tree tree,
      (∀ z : NativeGK4QImage (nativeGK4OOptionFamily p D E) tree tree,
        nativeGK4ROptionCompose tree tree tree e z = z) ∧
      (∀ z : NativeGK4QImage (nativeGK4OOptionFamily p D E) tree tree,
        nativeGK4ROptionCompose tree tree tree z e = z)) := by
  constructor
  · intro u v w
    exact nativeGK4ROptionCompose_assoc tree tree tree tree u v w
  · rintro ⟨e, hleft, _⟩
    exact nativeGK4ROption_no_left_identity tree ⟨e, hleft⟩

end GenuineImageUnits

/-- Genuine physical C60 north-hexagon F45 triple: Boolean image has
two-sided unit although the original P92B quotient does not. -/
theorem nativeGK4R_physical_north_boolean_observed_unit :
    (∀ z : NativeGK4QImage
        (nativeGK4OBooleanFamily _ _ _)
        nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple,
      nativeGK4RBoolCompose
          nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple
          nativeGK4FPhysicalNorthTriple
          (nativeGK4RBoolUnit nativeGK4FPhysicalNorthTriple) z = z) ∧
    (¬ ∃ e : NativeF55P92AssocRouteClasses
        nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple,
      ∀ q : NativeF55P92AssocRouteClasses
          nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple,
        nativeGK4H_p92Compose nativeGK4FPhysicalNorthTriple
          nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple e q = q) := by
  exact ⟨nativeGK4RBool_leftUnit
    nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple,
    fun ⟨e, he⟩ =>
      nativeGK4J_no_any_P92B_left_identity nativeGK4FPhysicalNorthTriple e he⟩

/-- Genuine physical C60 north: the TRUE Option Nat observation image
has no left identity despite the ambient Option Nat having some zero. -/
theorem nativeGK4R_physical_north_option_no_left :
    ¬ ∃ e : NativeGK4QImage (nativeGK4OOptionFamily _ _ _)
          nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple,
      ∀ z : NativeGK4QImage (nativeGK4OOptionFamily _ _ _)
          nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple,
        nativeGK4ROptionCompose nativeGK4FPhysicalNorthTriple
          nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple e z = z :=
  nativeGK4ROption_no_left_identity nativeGK4FPhysicalNorthTriple

#print axioms nativeGK4RBoolCompose
#print axioms nativeGK4ROptionCompose
#print axioms nativeGK4RBoolCompose_assoc
#print axioms nativeGK4ROptionCompose_assoc
#print axioms nativeGK4RBoolUnit
#print axioms nativeGK4RBoolUnit_value
#print axioms nativeGK4RBool_leftUnit
#print axioms nativeGK4RBool_rightUnit
#print axioms nativeGK4RBool_unital_image_but_no_source_identity
#print axioms nativeGK4RBool_specific_source_unit_not_left
#print axioms nativeGK4ROptionOne
#print axioms nativeGK4ROptionOne_value
#print axioms nativeGK4ROption_no_left_identity_at_one
#print axioms nativeGK4ROption_no_right_identity_at_one
#print axioms nativeGK4ROption_no_left_identity
#print axioms nativeGK4ROption_no_right_identity
#print axioms nativeGK4ROption_assoc_but_no_unit
#print axioms nativeGK4R_physical_north_boolean_observed_unit
#print axioms nativeGK4R_physical_north_option_no_left

end
end Kuu.F112.Physical
