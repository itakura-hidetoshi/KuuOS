import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4TStructuralKernelComparison
import Mathlib.Tactic

/-!
# F112-P94D3GK4U — compositional comparison and genuine Boolean kernel functor

The original genuine F54/P92B witness-existence quotient Q retains its
actual dependent composition WITHOUT an assumed associativity or unit.
The independently extended F54 structural-comparison quotient S is a
true Category by GK4H/GK4I, while GK4S's observation-kernel SECOND
quotient K_O carries an induced composition precisely under GK4P's
original, typed observation laws.

This file proves a general triangle => composition theorem: ANY triple
of actual GK4T-like comparison maps commuting with the canonical
surjections pi : Q -> S and kappa : Q -> K_O automatically preserves
the actual three-boundary composition. The proof uses surjectivity of
pi, the original GK4H nonfaithful multiplicative projection and the
GK4S transported image composition. It does NOT infer associativity
or identities on the original Q from those on S/K.

An explicit local iff characterizes existence of such a compositional
comparison triple by the GK4N FULL original Type-valued F54 seam
preservation at all THREE genuine F45 boundaries, assuming the GK4P
three observation laws. There is no extra unproved kernel-reflection
assumption: the compatibility is forced by the two triangles.

The TRUE Boolean GK4G observation enjoys those conditions uniformly.
Build a fully dependent Boolean observation-kernel category on WRAPPED
original F45 stage objects, with witnessed unit from original P92B
zero-edge history, transported composition, associative Bool.and,
and image-level left/right identity from GK4R. Build an actual Mathlib
Functor from GK4I's independent structural category to this separate
Boolean kernel category, show it is surjective on every typed Hom.
The structurally independent quotient and observational quotient are
not identified; the functor need not be faithful or an equivalence.

By contrast, GK4K Option Nat does not even admit the comparison on
any original inhabited F45 self-Hom (GK4T true F54 leftUnit obstruction).
The physical C60 north F45 triple is an unconditional instance.
The original Type-valued P92B 3-cell history is not fabricated
from equality of observed values.

Do NOT assert original Q associativity/units, an alternative Q
composition, complete historical typed equivalence, original genuine
14D unconditional Countable, original 19D filler, global strict n,
or hyperdescent. No Gray/new axiom/sorry/admit. Append-only,
tighten-only, same-root, public root 107. Pin Lean v4.30.0-rc2,
mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Protect validation-only #1558 Draft/OPEN/unmerged.
Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uD vD uE vE uB

section ArbitraryTypedTriangle

variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {B : Type uB}
variable (observe : NativeGK4OObserverFamily p D E B)
variable (combine : B → B → B)
variable (leftAction rightAction : NativeGK4PContextAction p D E B)
variable (laws : NativeGK4PObservationLaws observe combine leftAction rightAction)
variable {a b : D} {x y : E}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}
variable {n₁ n₂ n₃ m₁ m₂ m₃ m₁' m₂' m₃' : Nat}
variable (t₁ : KuuNativeF45Tree p n₁ m₁ ma pa mb pb)
variable (t₂ : KuuNativeF45Tree p n₂ m₂ ma pa mb pb)
variable (t₃ : KuuNativeF45Tree p n₃ m₃ ma pa mb pb)

/-- GENERAL DIAGRAMMATIC COMPOSITION: all THREE triangles commuting
with the true original P92B quotient force preservation of composition
between the independent structural and observed-kernel quotients.
Neither the original Q associativity nor unitality is assumed. -/
theorem nativeGK4U_any_triangle_preserves_compose
    (F₁₂ : NativeGK4EStructuralRouteClasses t₁ t₂ →
      NativeGK4SKernelClasses observe t₁ t₂)
    (F₂₃ : NativeGK4EStructuralRouteClasses t₂ t₃ →
      NativeGK4SKernelClasses observe t₂ t₃)
    (F₁₃ : NativeGK4EStructuralRouteClasses t₁ t₃ →
      NativeGK4SKernelClasses observe t₁ t₃)
    (h₁₂ : ∀ q : NativeF55P92AssocRouteClasses t₁ t₂,
      F₁₂ (nativeGK4EP92ToStructural t₁ t₂ q) =
        nativeGK4SKernelClass observe t₁ t₂ q)
    (h₂₃ : ∀ q : NativeF55P92AssocRouteClasses t₂ t₃,
      F₂₃ (nativeGK4EP92ToStructural t₂ t₃ q) =
        nativeGK4SKernelClass observe t₂ t₃ q)
    (h₁₃ : ∀ q : NativeF55P92AssocRouteClasses t₁ t₃,
      F₁₃ (nativeGK4EP92ToStructural t₁ t₃ q) =
        nativeGK4SKernelClass observe t₁ t₃ q)
    (u : NativeGK4EStructuralRouteClasses t₁ t₂)
    (v : NativeGK4EStructuralRouteClasses t₂ t₃) :
    F₁₃ (nativeGK4H_structuralCompose t₁ t₂ t₃ u v) =
      nativeGK4SKernelCompose observe combine leftAction rightAction laws t₁ t₂ t₃
        (F₁₂ u) (F₂₃ v) := by
  obtain ⟨q, rfl⟩ := nativeGK4EP92ToStructural_surjective t₁ t₂ u
  obtain ⟨r, rfl⟩ := nativeGK4EP92ToStructural_surjective t₂ t₃ v
  calc
    F₁₃ (nativeGK4H_structuralCompose t₁ t₂ t₃
      (nativeGK4EP92ToStructural t₁ t₂ q)
      (nativeGK4EP92ToStructural t₂ t₃ r)) =
        F₁₃ (nativeGK4EP92ToStructural t₁ t₃
          (nativeGK4H_p92Compose t₁ t₂ t₃ q r)) :=
      congrArg F₁₃ (nativeGK4H_comparison_preserves_compose t₁ t₂ t₃ q r).symm
    _ = nativeGK4SKernelClass observe t₁ t₃
        (nativeGK4H_p92Compose t₁ t₂ t₃ q r) := h₁₃ _
    _ = nativeGK4SKernelCompose observe combine leftAction rightAction laws t₁ t₂ t₃
        (nativeGK4SKernelClass observe t₁ t₂ q)
        (nativeGK4SKernelClass observe t₂ t₃ r) :=
      (nativeGK4SKernelCompose_class observe combine leftAction rightAction laws
        t₁ t₂ t₃ q r).symm
    _ = nativeGK4SKernelCompose observe combine leftAction rightAction laws t₁ t₂ t₃
        (F₁₂ (nativeGK4EP92ToStructural t₁ t₂ q))
        (F₂₃ (nativeGK4EP92ToStructural t₂ t₃ r)) := by
      rw [h₁₂ q, h₂₃ r]

/-- A commuting comparison always maps the true GK4I structural
identity to the K_O class of the ACTUAL original P92B zero-edge
route. This states the image of the unit; it does NOT say Q has a unit. -/
theorem nativeGK4U_any_triangle_preserves_unit
    (F : NativeGK4EStructuralRouteClasses t₁ t₁ →
      NativeGK4SKernelClasses observe t₁ t₁)
    (hF : ∀ q : NativeF55P92AssocRouteClasses t₁ t₁,
      F (nativeGK4EP92ToStructural t₁ t₁ q) =
        nativeGK4SKernelClass observe t₁ t₁ q) :
    F (nativeGK4H_structuralUnit t₁) =
      nativeGK4SKernelClass observe t₁ t₁ (nativeGK4H_p92Unit t₁) := by
  exact hF (nativeGK4H_p92Unit t₁)

/-- GK4T's SPECIFIC canonical comparison preserves the true fully
dependent structural composition whenever its three local seam
obligations and GK4P's genuine source observation laws hold. -/
theorem nativeGK4U_comparison_preserves_compose
    (h₁₂ : nativeGK4NSeamInvariant t₁ t₂ (observe t₁ t₂))
    (h₂₃ : nativeGK4NSeamInvariant t₂ t₃ (observe t₂ t₃))
    (h₁₃ : nativeGK4NSeamInvariant t₁ t₃ (observe t₁ t₃))
    (u : NativeGK4EStructuralRouteClasses t₁ t₂)
    (v : NativeGK4EStructuralRouteClasses t₂ t₃) :
    nativeGK4TComparison observe t₁ t₃ h₁₃
      (nativeGK4H_structuralCompose t₁ t₂ t₃ u v) =
    nativeGK4SKernelCompose observe combine leftAction rightAction laws t₁ t₂ t₃
      (nativeGK4TComparison observe t₁ t₂ h₁₂ u)
      (nativeGK4TComparison observe t₂ t₃ h₂₃ v) := by
  exact nativeGK4U_any_triangle_preserves_compose observe combine
    leftAction rightAction laws t₁ t₂ t₃
    (nativeGK4TComparison observe t₁ t₂ h₁₂)
    (nativeGK4TComparison observe t₂ t₃ h₂₃)
    (nativeGK4TComparison observe t₁ t₃ h₁₃)
    (nativeGK4TComparison_class observe t₁ t₂ h₁₂)
    (nativeGK4TComparison_class observe t₂ t₃ h₂₃)
    (nativeGK4TComparison_class observe t₁ t₃ h₁₃) u v

/-- The structural unit's comparison image is exactly the original
source-zero-edge observation kernel class, without any original Q
identity law. -/
theorem nativeGK4U_comparison_preserves_unit
    (h₁₁ : nativeGK4NSeamInvariant t₁ t₁ (observe t₁ t₁)) :
    nativeGK4TComparison observe t₁ t₁ h₁₁
      (nativeGK4H_structuralUnit t₁) =
      nativeGK4SKernelClass observe t₁ t₁ (nativeGK4H_p92Unit t₁) := by
  exact nativeGK4U_any_triangle_preserves_unit observe t₁
    (nativeGK4TComparison observe t₁ t₁ h₁₁)
    (nativeGK4TComparison_class observe t₁ t₁ h₁₁)

/-- The three-boundary compositional comparison problem. All three
comparison maps MUST commute with actual pi/kappa, not merely preserve
one arbitrarily chosen multiplication. -/
def NativeGK4UCompositionalComparisonExists : Prop :=
  ∃ (F₁₂ : NativeGK4EStructuralRouteClasses t₁ t₂ →
        NativeGK4SKernelClasses observe t₁ t₂)
    (F₂₃ : NativeGK4EStructuralRouteClasses t₂ t₃ →
        NativeGK4SKernelClasses observe t₂ t₃)
    (F₁₃ : NativeGK4EStructuralRouteClasses t₁ t₃ →
        NativeGK4SKernelClasses observe t₁ t₃),
    (∀ q : NativeF55P92AssocRouteClasses t₁ t₂,
      F₁₂ (nativeGK4EP92ToStructural t₁ t₂ q) =
        nativeGK4SKernelClass observe t₁ t₂ q) ∧
    (∀ q : NativeF55P92AssocRouteClasses t₂ t₃,
      F₂₃ (nativeGK4EP92ToStructural t₂ t₃ q) =
        nativeGK4SKernelClass observe t₂ t₃ q) ∧
    (∀ q : NativeF55P92AssocRouteClasses t₁ t₃,
      F₁₃ (nativeGK4EP92ToStructural t₁ t₃ q) =
        nativeGK4SKernelClass observe t₁ t₃ q) ∧
    (∀ (u : NativeGK4EStructuralRouteClasses t₁ t₂)
      (v : NativeGK4EStructuralRouteClasses t₂ t₃),
      F₁₃ (nativeGK4H_structuralCompose t₁ t₂ t₃ u v) =
        nativeGK4SKernelCompose observe combine leftAction rightAction laws t₁ t₂ t₃
          (F₁₂ u) (F₂₃ v))

/-- MAIN NECESSARY AND SUFFICIENT CONDITION: the existence of an
actual composition-preserving, three-boundary comparison triple is
equivalent to the ORIGINAL full F54 seam conditions at these three
fully typed boundaries. Compositionality needs NO EXTRA obstruction
beyond the GK4P observation laws and the three genuine triangles. -/
theorem nativeGK4U_compositional_iff_three_seams :
    NativeGK4UCompositionalComparisonExists observe combine
      leftAction rightAction laws t₁ t₂ t₃ ↔
    nativeGK4NSeamInvariant t₁ t₂ (observe t₁ t₂) ∧
    nativeGK4NSeamInvariant t₂ t₃ (observe t₂ t₃) ∧
    nativeGK4NSeamInvariant t₁ t₃ (observe t₁ t₃) := by
  constructor
  · rintro ⟨F₁₂, F₂₃, F₁₃, h₁₂, h₂₃, h₁₃, _⟩
    exact ⟨(nativeGK4TComparisonExists_iff_seam observe t₁ t₂).mp ⟨F₁₂, h₁₂⟩,
      (nativeGK4TComparisonExists_iff_seam observe t₂ t₃).mp ⟨F₂₃, h₂₃⟩,
      (nativeGK4TComparisonExists_iff_seam observe t₁ t₃).mp ⟨F₁₃, h₁₃⟩⟩
  · rintro ⟨h₁₂, h₂₃, h₁₃⟩
    refine ⟨nativeGK4TComparison observe t₁ t₂ h₁₂,
      nativeGK4TComparison observe t₂ t₃ h₂₃,
      nativeGK4TComparison observe t₁ t₃ h₁₃,
      nativeGK4TComparison_class observe t₁ t₂ h₁₂,
      nativeGK4TComparison_class observe t₂ t₃ h₂₃,
      nativeGK4TComparison_class observe t₁ t₃ h₁₃, ?_⟩
    intro u v
    exact nativeGK4U_comparison_preserves_compose observe combine
      leftAction rightAction laws t₁ t₂ t₃ h₁₂ h₂₃ h₁₃ u v

end ArbitraryTypedTriangle

section BooleanKernelCategory

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

/-- Witnessed Boolean observation-kernel identity: the class of
the ACTUAL original P92B zero-edge route, even though this route
is NOT an identity in the original P92B existence quotient. -/
def nativeGK4UBoolKernelUnit :
    NativeGK4SKernelClasses (nativeGK4OBooleanFamily p D E) t₁ t₁ :=
  nativeGK4SKernelClass (nativeGK4OBooleanFamily p D E) t₁ t₁
    (nativeGK4H_p92Unit t₁)

/-- The actual GK4S transported composition on the observational
SECOND quotient, NOT the original P92B quotient composition. -/
def nativeGK4UBoolKernelCompose
    (u : NativeGK4SKernelClasses (nativeGK4OBooleanFamily p D E) t₁ t₂)
    (v : NativeGK4SKernelClasses (nativeGK4OBooleanFamily p D E) t₂ t₃) :
    NativeGK4SKernelClasses (nativeGK4OBooleanFamily p D E) t₁ t₃ :=
  nativeGK4SKernelCompose (nativeGK4OBooleanFamily p D E) Bool.and
    (nativeGK4PIdentityAction p D E Bool)
    (nativeGK4PIdentityAction p D E Bool)
    nativeGK4P_boolean_laws t₁ t₂ t₃ u v

/-- Original P92B composition projects to the REAL Boolean
kernel composition; the projection is not faithful. -/
@[simp] theorem nativeGK4UBoolKernelCompose_class
    (u : NativeF55P92AssocRouteClasses t₁ t₂)
    (v : NativeF55P92AssocRouteClasses t₂ t₃) :
    nativeGK4UBoolKernelCompose t₁ t₂ t₃
      (nativeGK4SKernelClass (nativeGK4OBooleanFamily p D E) t₁ t₂ u)
      (nativeGK4SKernelClass (nativeGK4OBooleanFamily p D E) t₂ t₃ v) =
    nativeGK4SKernelClass (nativeGK4OBooleanFamily p D E) t₁ t₃
      (nativeGK4H_p92Compose t₁ t₂ t₃ u v) :=
  nativeGK4SKernelCompose_class (nativeGK4OBooleanFamily p D E) Bool.and
    (nativeGK4PIdentityAction p D E Bool)
    (nativeGK4PIdentityAction p D E Bool)
    nativeGK4P_boolean_laws t₁ t₂ t₃ u v

/-- Associativity holds in K_Bool from the BINARY VALUE operation
Bool.and, not from any unproved associativity law of original P92B. -/
theorem nativeGK4UBoolKernelCompose_assoc
    (u : NativeGK4SKernelClasses (nativeGK4OBooleanFamily p D E) t₁ t₂)
    (v : NativeGK4SKernelClasses (nativeGK4OBooleanFamily p D E) t₂ t₃)
    (w : NativeGK4SKernelClasses (nativeGK4OBooleanFamily p D E) t₃ t₄) :
    nativeGK4UBoolKernelCompose t₁ t₃ t₄
      (nativeGK4UBoolKernelCompose t₁ t₂ t₃ u v) w =
    nativeGK4UBoolKernelCompose t₁ t₂ t₄
      u (nativeGK4UBoolKernelCompose t₂ t₃ t₄ v w) := by
  exact nativeGK4SKernelCompose_assoc
    (nativeGK4OBooleanFamily p D E) Bool.and
    (nativeGK4PIdentityAction p D E Bool)
    (nativeGK4PIdentityAction p D E Bool)
    nativeGK4P_boolean_laws
    (by intro x y z; cases x <;> cases y <;> cases z <;> rfl)
    t₁ t₂ t₃ t₄ u v w

/-- The true Boolean observer-kernel unit is a LEFT identity,
as witnessed by the original GK4R image-level unit under the proven
GK4S equivalence. Does NOT reflect back to original Q. -/
theorem nativeGK4UBoolKernelCompose_leftUnit
    (u : NativeGK4SKernelClasses (nativeGK4OBooleanFamily p D E) t₁ t₂) :
    nativeGK4UBoolKernelCompose t₁ t₁ t₂
      (nativeGK4UBoolKernelUnit t₁) u = u := by
  apply (nativeGK4SKernelImageEquiv (nativeGK4OBooleanFamily p D E) t₁ t₂).injective
  simpa only [nativeGK4UBoolKernelCompose, nativeGK4UBoolKernelUnit,
    nativeGK4SKernelCompose, Equiv.apply_symm_apply,
    nativeGK4SKernelImageEquiv_class, nativeGK4RBoolCompose,
    nativeGK4RBoolUnit] using
    (nativeGK4RBool_leftUnit t₁ t₂
      (nativeGK4SKernelImageEquiv (nativeGK4OBooleanFamily p D E) t₁ t₂ u))

/-- The same true Boolean source-zero-edge observed class is a
RIGHT identity of the second kernel quotient, not of original Q. -/
theorem nativeGK4UBoolKernelCompose_rightUnit
    (u : NativeGK4SKernelClasses (nativeGK4OBooleanFamily p D E) t₁ t₂) :
    nativeGK4UBoolKernelCompose t₁ t₂ t₂
      u (nativeGK4UBoolKernelUnit t₂) = u := by
  apply (nativeGK4SKernelImageEquiv (nativeGK4OBooleanFamily p D E) t₁ t₂).injective
  simpa only [nativeGK4UBoolKernelCompose, nativeGK4UBoolKernelUnit,
    nativeGK4SKernelCompose, Equiv.apply_symm_apply,
    nativeGK4SKernelImageEquiv_class, nativeGK4RBoolCompose,
    nativeGK4RBoolUnit] using
    (nativeGK4RBool_rightUnit t₂ t₁
      (nativeGK4SKernelImageEquiv (nativeGK4OBooleanFamily p D E) t₁ t₂ u))

end BooleanKernelCategory

/-! ### Exact separate category and functor, with all true F45
dependent source objects and the genuine original source Blocks. -/

/-- Wrap the ORIGINAL fully typed F45 stage into a separate target
category presentation; do not install two conflicting Category
instances on the identical stage Type. -/
structure NativeGK4UBoolKernelStage
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) where
  original : NativeGK4IStage p ma mb pa pb

/-- A genuine Mathlib Category built on the actually double
quotiented P92B Boolean OBSERVATION KERNEL homs. Its laws are
the true GK4S/GK4R image laws, NOT original P92B class laws. -/
instance nativeGK4UBoolKernelCategory
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :
    Category (NativeGK4UBoolKernelStage p ma mb pa pb) where
  Hom X Y := NativeGK4SKernelClasses (nativeGK4OBooleanFamily p D E)
    X.original.2.2 Y.original.2.2
  id X := nativeGK4UBoolKernelUnit X.original.2.2
  comp f g := nativeGK4UBoolKernelCompose _ _ _ f g
  id_comp := by
    intro X Y f
    exact nativeGK4UBoolKernelCompose_leftUnit
      X.original.2.2 Y.original.2.2 f
  comp_id := by
    intro X Y f
    exact nativeGK4UBoolKernelCompose_rightUnit
      X.original.2.2 Y.original.2.2 f
  assoc := by
    intro W X Y Z f g h
    exact nativeGK4UBoolKernelCompose_assoc
      W.original.2.2 X.original.2.2 Y.original.2.2 Z.original.2.2 f g h

/-- GK4T's true comparison is not merely a set map: by GK4U's
triangle composition and witnessed observed units, it is a FULLY
TYPED Mathlib FUNCTOR between the original independent STRUCTURAL
category and the distinct Boolean OBSERVER-KERNEL category.
It does not identify their homs, import a P92B category instance or
claim faithfulness. -/
def nativeGK4UBoolKernelComparisonFunctor
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :
    NativeGK4IStage p ma mb pa pb ⥤
      NativeGK4UBoolKernelStage p ma mb pa pb where
  obj X := ⟨X⟩
  map := fun {X Y} f =>
    nativeGK4TComparison (nativeGK4OBooleanFamily p D E)
      X.2.2 Y.2.2 (nativeGK4N_boolean_seam_invariant X.2.2 Y.2.2) f
  map_id := by
    intro X
    exact nativeGK4U_comparison_preserves_unit
      (nativeGK4OBooleanFamily p D E)
      X.2.2 (nativeGK4N_boolean_seam_invariant X.2.2 X.2.2)
  map_comp := by
    intro X Y Z f g
    exact nativeGK4U_comparison_preserves_compose
      (nativeGK4OBooleanFamily p D E) Bool.and
      (nativeGK4PIdentityAction p D E Bool)
      (nativeGK4PIdentityAction p D E Bool)
      nativeGK4P_boolean_laws
      X.2.2 Y.2.2 Z.2.2
      (nativeGK4N_boolean_seam_invariant X.2.2 Y.2.2)
      (nativeGK4N_boolean_seam_invariant Y.2.2 Z.2.2)
      (nativeGK4N_boolean_seam_invariant X.2.2 Z.2.2) f g

/-- The comparison functor is FULL on every genuine dependent Hom:
each kernel class has an actual structural class above it. This is
surjectivity, NOT injectivity or an isomorphism of the different
proof-existence presentations. -/
theorem nativeGK4UBoolKernelFunctor_surjective_hom
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (X Y : NativeGK4IStage p ma mb pa pb) :
    Function.Surjective
      (fun f : X ⟶ Y =>
        (nativeGK4UBoolKernelComparisonFunctor p ma mb pa pb).map f) := by
  exact nativeGK4TComparison_surjective (nativeGK4OBooleanFamily p D E)
    X.2.2 Y.2.2 (nativeGK4N_boolean_seam_invariant X.2.2 Y.2.2)

/-- The Boolean observation admits fully compositional comparisons
at all genuine F45 triples, not merely set-level factorization at
a single stage. -/
theorem nativeGK4U_boolean_compositional
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
    (t₁ : KuuNativeF45Tree p n₁ m₁ ma pa mb pb)
    (t₂ : KuuNativeF45Tree p n₂ m₂ ma pa mb pb)
    (t₃ : KuuNativeF45Tree p n₃ m₃ ma pa mb pb) :
    NativeGK4UCompositionalComparisonExists
      (nativeGK4OBooleanFamily p D E) Bool.and
      (nativeGK4PIdentityAction p D E Bool)
      (nativeGK4PIdentityAction p D E Bool)
      nativeGK4P_boolean_laws t₁ t₂ t₃ := by
  exact (nativeGK4U_compositional_iff_three_seams
    (nativeGK4OBooleanFamily p D E) Bool.and
    (nativeGK4PIdentityAction p D E Bool)
    (nativeGK4PIdentityAction p D E Bool)
    nativeGK4P_boolean_laws t₁ t₂ t₃).mpr
    ⟨nativeGK4N_boolean_seam_invariant t₁ t₂,
     nativeGK4N_boolean_seam_invariant t₂ t₃,
     nativeGK4N_boolean_seam_invariant t₁ t₃⟩

/-- The GK4K Option Nat observer does NOT have a
composition-preserving structural comparison on an inhabited
self-Hom, because even one genuine Type-valued F54 leftUnit
seam makes its initial triangle impossible. -/
theorem nativeGK4U_option_compositional_not_exists
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {n m : Nat}
    (tree : KuuNativeF45Tree p n m ma pa mb pb) :
    ¬ NativeGK4UCompositionalComparisonExists
      (nativeGK4OOptionFamily p D E) nativeGK4KAdd
      (nativeGK4PIdentityAction p D E (Option Nat))
      (nativeGK4PIdentityAction p D E (Option Nat))
      nativeGK4P_option_laws tree tree tree := by
  intro h
  have hseam := (nativeGK4U_compositional_iff_three_seams
    (nativeGK4OOptionFamily p D E) nativeGK4KAdd
    (nativeGK4PIdentityAction p D E (Option Nat))
    (nativeGK4PIdentityAction p D E (Option Nat))
    nativeGK4P_option_laws tree tree tree).mp h
  exact nativeGK4N_original_option_fails_seam tree hseam.1

/-- In the ACTUAL physical C60 north triple the GK4I structural
category maps by a real Boolean kernel functor, whose hom map is
surjective; yet the GK4K Option Nat comparison is obstructed
unconditionally. No synthetic F45 or unproved global conditions. -/
theorem nativeGK4U_physical_north_functor_and_option_obstruction :
    Function.Surjective
      (fun f :
        nativeGK4IPhysicalNorthTripleStage ⟶
          nativeGK4IPhysicalNorthTripleStage =>
        (nativeGK4UBoolKernelComparisonFunctor (.hexagon (.top 0))
          northHexagonNativeFrame.firstAxis northHexagonNativeFrame.firstAxis
          northHexagonNativeFrame.secondAxis northHexagonNativeFrame.secondAxis).map f) ∧
    ¬ NativeGK4UCompositionalComparisonExists
      (nativeGK4OOptionFamily _ _ _) nativeGK4KAdd
      (nativeGK4PIdentityAction _ _ _ (Option Nat))
      (nativeGK4PIdentityAction _ _ _ (Option Nat))
      nativeGK4P_option_laws
      nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple
      nativeGK4FPhysicalNorthTriple := by
  constructor
  · exact nativeGK4UBoolKernelFunctor_surjective_hom
      (.hexagon (.top 0))
      northHexagonNativeFrame.firstAxis northHexagonNativeFrame.firstAxis
      northHexagonNativeFrame.secondAxis northHexagonNativeFrame.secondAxis
      nativeGK4IPhysicalNorthTripleStage nativeGK4IPhysicalNorthTripleStage
  · exact nativeGK4U_option_compositional_not_exists nativeGK4FPhysicalNorthTriple

#print axioms nativeGK4U_any_triangle_preserves_compose
#print axioms nativeGK4U_any_triangle_preserves_unit
#print axioms nativeGK4U_comparison_preserves_compose
#print axioms nativeGK4U_comparison_preserves_unit
#print axioms NativeGK4UCompositionalComparisonExists
#print axioms nativeGK4U_compositional_iff_three_seams
#print axioms nativeGK4UBoolKernelUnit
#print axioms nativeGK4UBoolKernelCompose
#print axioms nativeGK4UBoolKernelCompose_class
#print axioms nativeGK4UBoolKernelCompose_assoc
#print axioms nativeGK4UBoolKernelCompose_leftUnit
#print axioms nativeGK4UBoolKernelCompose_rightUnit
#print axioms NativeGK4UBoolKernelStage
#print axioms nativeGK4UBoolKernelCategory
#print axioms nativeGK4UBoolKernelComparisonFunctor
#print axioms nativeGK4UBoolKernelFunctor_surjective_hom
#print axioms nativeGK4U_boolean_compositional
#print axioms nativeGK4U_option_compositional_not_exists
#print axioms nativeGK4U_physical_north_functor_and_option_obstruction

end
end Kuu.F112.Physical
