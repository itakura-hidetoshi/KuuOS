import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4SObserverKernelImageEquiv
import Mathlib.Tactic

/-!
# F112-P94D3GK4T — structural quotient to genuine P92B observer-kernel quotient

At EVERY genuinely typed F45 source and target retain THREE DISTINCT
authorities:
  Q = original Type-valued P92B witness-existence quotient;
  S = independently extended F54 structural-comparison quotient (GK4E);
  K = a SECOND quotient of Q by observational equality (GK4S).
Write pi : Q -> S and kappa : Q -> K for the actual canonical
surjections. We classify precisely when a comparison F : S -> K
commutes with them, F (pi q) = kappa q.

For any GK4O original P92B observer family, prove the comparison exists
IFF it preserves ALL genuine Type-valued F54 structural seams (GK4N).
An admitted F is UNIQUE (GK4E surjectivity). Construct the comparison
explicitly by lifting actual structural route representatives using
the GK4S observational kernel equality: no representatives are selected
by Classical.choice. Prove the triangle on original P92B classes, the
actual GK4Q image triangle, surjectivity, and an exact criterion for
injectivity in terms of reflected structural equality.

The TRUE GK4G Boolean physical rotation-zero observation admits a
comparison at all typed boundaries, even though its original P92B
kernel projection is demonstrably noninjective. The finer GK4K Option
Nat observer admits NO such comparison on any inhabited F45 self-stage:
one genuine F54 leftUnit seam changes some 2 to some 1. Both contrasts
hold unconditionally on the physical C60 north F45 triple.

No claim of original P92B associativity, left/right identities, an
alternative composition, historical P92B/F19/F28/F54/F55 typed
equivalence, unconditional 14D Countable, original 19D filler, global
strict n or hyperdescent. The image-level algebra never generates
an original Type-valued P92B 3-cell. No new axiom, sorry/admit or Gray.

Append-only / tighten-only / same-root; 107 public roots untouched.
Pinned Lean v4.30.0-rc2, mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Preserve validation-only PR #1558 Draft/open/unmerged.
Copyright 板倉英俊 / Hidetoshi Itakura. Apache-2.0.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uD vD uE vE uB

section UniversalComparison

variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {B : Type uB}
variable (observe : NativeGK4OObserverFamily p D E B)
variable {a b : D} {x y : E} {n n' m m' : Nat}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}
variable (first : KuuNativeF45Tree p n m ma pa mb pb)
variable (last : KuuNativeF45Tree p n' m' ma pa mb pb)

/-- The precise commuting comparison problem between two DIFFERENT
quotients of the same actual ORIGINAL P92B witness-existence quotient. -/
def NativeGK4TComparisonExists : Prop :=
  ∃ F : NativeGK4EStructuralRouteClasses first last →
      NativeGK4SKernelClasses observe first last,
    ∀ q : NativeF55P92AssocRouteClasses first last,
      F (nativeGK4EP92ToStructural first last q) =
        nativeGK4SKernelClass observe first last q

/-- Construct the comparison DIRECTLY on genuine structural comparison
classes, under the exact GK4N seam-invariance hypothesis. No arbitrary
section of pi and no Type-valued proof is inferred from observer values. -/
def nativeGK4TComparison
    (hseam : nativeGK4NSeamInvariant first last (observe first last)) :
    NativeGK4EStructuralRouteClasses first last →
      NativeGK4SKernelClasses observe first last :=
  _root_.Quotient.lift
    (fun route : KuuNativeF45Tree.DepthRotationRoute p first last =>
      nativeGK4SKernelClass observe first last
        (nativeF55P92AssocRouteClass first last route))
    (by
      intro r s hstruct
      apply (nativeGK4SKernelClass_eq_iff observe first last _ _).mpr
      obtain ⟨cell⟩ := hstruct
      exact nativeGK4N_structuralComparison_sound first last
        (observe first last) hseam cell)

/-- The comparison maps each actual structural route class to the
second kernel class of its own ORIGINAL P92B route class. -/
@[simp] theorem nativeGK4TComparison_route
    (hseam : nativeGK4NSeamInvariant first last (observe first last))
    (route : KuuNativeF45Tree.DepthRotationRoute p first last) :
    nativeGK4TComparison observe first last hseam
        (nativeGK4EStructuralRouteClass first last route) =
      nativeGK4SKernelClass observe first last
        (nativeF55P92AssocRouteClass first last route) := by
  rfl

/-- Required commuting triangle for EVERY original P92B class;
this is not restricted to a chosen F54 representative. -/
@[simp] theorem nativeGK4TComparison_class
    (hseam : nativeGK4NSeamInvariant first last (observe first last))
    (q : NativeF55P92AssocRouteClasses first last) :
    nativeGK4TComparison observe first last hseam
        (nativeGK4EP92ToStructural first last q) =
      nativeGK4SKernelClass observe first last q := by
  refine _root_.Quotient.inductionOn q ?_
  intro route
  simpa only [nativeGK4EP92ToStructural_class, nativeGK4TComparison_route]

/-- The commuting triangle as an equality of genuine typed maps. -/
theorem nativeGK4TComparison_triangle
    (hseam : nativeGK4NSeamInvariant first last (observe first last)) :
    (fun q : NativeF55P92AssocRouteClasses first last =>
      nativeGK4TComparison observe first last hseam
        (nativeGK4EP92ToStructural first last q)) =
      nativeGK4SKernelClass observe first last := by
  funext q
  exact nativeGK4TComparison_class observe first last hseam q

/-- Fiber formulation: a structural-to-kernel comparison exists
EXACTLY when the original observer is constant on every true pi fiber.
This does not assert pi is injective, nor equate S with Q or K. -/
theorem nativeGK4TComparisonExists_iff_fiber :
    NativeGK4TComparisonExists observe first last ↔
      (∀ q r : NativeF55P92AssocRouteClasses first last,
        nativeGK4EP92ToStructural first last q =
          nativeGK4EP92ToStructural first last r →
        observe first last q = observe first last r) := by
  constructor
  · rintro ⟨F, hF⟩ q r hp
    apply (nativeGK4SKernelClass_eq_iff observe first last q r).mp
    calc
      nativeGK4SKernelClass observe first last q =
          F (nativeGK4EP92ToStructural first last q) := (hF q).symm
      _ = F (nativeGK4EP92ToStructural first last r) :=
        congrArg F hp
      _ = nativeGK4SKernelClass observe first last r := hF r
  · intro hfiber
    have hfactor :
        ∃ lift : NativeGK4EStructuralRouteClasses first last → B,
          ∀ q : NativeF55P92AssocRouteClasses first last,
            lift (nativeGK4EP92ToStructural first last q) =
              observe first last q :=
      (nativeGK4L_factor_iff_fiber_constant first last
        (observe first last)).mpr hfiber
    have hseam : nativeGK4NSeamInvariant first last
        (observe first last) :=
      (nativeGK4N_observer_factor_iff_seam first last
        (observe first last)).mp hfactor
    exact ⟨nativeGK4TComparison observe first last hseam,
      nativeGK4TComparison_class observe first last hseam⟩

/-- GK4T main theorem. The EXISTENCE of F commuting with pi and kappa
is equivalent to preservation of ALL 14 genuine F54 structure seams,
not merely the seven primitive ones without the four kernel laws. -/
theorem nativeGK4TComparisonExists_iff_seam :
    NativeGK4TComparisonExists observe first last ↔
      nativeGK4NSeamInvariant first last (observe first last) := by
  constructor
  · intro hF
    have hfiber :=
      (nativeGK4TComparisonExists_iff_fiber observe first last).mp hF
    have hfactor :
        ∃ lift : NativeGK4EStructuralRouteClasses first last → B,
          ∀ q : NativeF55P92AssocRouteClasses first last,
            lift (nativeGK4EP92ToStructural first last q) =
              observe first last q :=
      (nativeGK4L_factor_iff_fiber_constant first last
        (observe first last)).mpr hfiber
    exact (nativeGK4N_observer_factor_iff_seam first last
      (observe first last)).mp hfactor
  · intro hseam
    exact ⟨nativeGK4TComparison observe first last hseam,
      nativeGK4TComparison_class observe first last hseam⟩

/-- Every commuting F is forced to be the directly constructed one:
no synthetic inverse to pi is introduced. -/
theorem nativeGK4TComparison_unique
    (hseam : nativeGK4NSeamInvariant first last (observe first last))
    (F : NativeGK4EStructuralRouteClasses first last →
      NativeGK4SKernelClasses observe first last)
    (hF : ∀ q : NativeF55P92AssocRouteClasses first last,
      F (nativeGK4EP92ToStructural first last q) =
        nativeGK4SKernelClass observe first last q) :
    F = nativeGK4TComparison observe first last hseam := by
  exact nativeGK4N_factor_unique first last
    (nativeGK4SKernelClass observe first last)
    F (nativeGK4TComparison observe first last hseam)
    hF (nativeGK4TComparison_class observe first last hseam)

/-- Strengthened universal property: existence AND uniqueness of the
structural/kernel comparison is equivalent to all-seam preservation. -/
theorem nativeGK4TComparison_existsUnique_iff_seam :
    (∃! F : NativeGK4EStructuralRouteClasses first last →
        NativeGK4SKernelClasses observe first last,
      ∀ q : NativeF55P92AssocRouteClasses first last,
        F (nativeGK4EP92ToStructural first last q) =
          nativeGK4SKernelClass observe first last q) ↔
      nativeGK4NSeamInvariant first last (observe first last) := by
  constructor
  · rintro ⟨F, hF, _⟩
    exact (nativeGK4TComparisonExists_iff_seam observe first last).mp
      ⟨F, hF⟩
  · intro hseam
    refine ⟨nativeGK4TComparison observe first last hseam,
      nativeGK4TComparison_class observe first last hseam, ?_⟩
    intro F hF
    exact nativeGK4TComparison_unique observe first last hseam F hF

/-- The admitted comparison is surjective, since kappa is the
actual second-quotient projection and pi is defined on the same Q.
Surjectivity does NOT imply injectivity or an original P92B equivalence. -/
theorem nativeGK4TComparison_surjective
    (hseam : nativeGK4NSeamInvariant first last (observe first last)) :
    Function.Surjective (nativeGK4TComparison observe first last hseam) := by
  intro z
  refine _root_.Quotient.inductionOn z ?_
  intro q
  exact ⟨nativeGK4EP92ToStructural first last q,
    nativeGK4TComparison_class observe first last hseam q⟩

/-- The comparison is injective precisely if observational equality
reflects structural equality. No such reflection is postulated. -/
theorem nativeGK4TComparison_injective_iff_reflects
    (hseam : nativeGK4NSeamInvariant first last (observe first last)) :
    Function.Injective (nativeGK4TComparison observe first last hseam) ↔
      (∀ q r : NativeF55P92AssocRouteClasses first last,
        observe first last q = observe first last r →
          nativeGK4EP92ToStructural first last q =
            nativeGK4EP92ToStructural first last r) := by
  constructor
  · intro hinj q r hobs
    apply hinj
    calc
      nativeGK4TComparison observe first last hseam
          (nativeGK4EP92ToStructural first last q) =
        nativeGK4SKernelClass observe first last q :=
          nativeGK4TComparison_class observe first last hseam q
      _ = nativeGK4SKernelClass observe first last r :=
        (nativeGK4SKernelClass_eq_iff observe first last q r).mpr hobs
      _ = nativeGK4TComparison observe first last hseam
          (nativeGK4EP92ToStructural first last r) :=
        (nativeGK4TComparison_class observe first last hseam r).symm
  · intro hreflect s t hst
    obtain ⟨q, hq⟩ := nativeGK4EP92ToStructural_surjective first last s
    obtain ⟨r, hr⟩ := nativeGK4EP92ToStructural_surjective first last t
    have hclasses :
        nativeGK4SKernelClass observe first last q =
          nativeGK4SKernelClass observe first last r := by
      calc
        nativeGK4SKernelClass observe first last q =
          nativeGK4TComparison observe first last hseam
            (nativeGK4EP92ToStructural first last q) :=
              (nativeGK4TComparison_class observe first last hseam q).symm
        _ = nativeGK4TComparison observe first last hseam s :=
          congrArg (nativeGK4TComparison observe first last hseam) hq
        _ = nativeGK4TComparison observe first last hseam t := hst
        _ = nativeGK4TComparison observe first last hseam
              (nativeGK4EP92ToStructural first last r) :=
          congrArg (nativeGK4TComparison observe first last hseam) hr.symm
        _ = nativeGK4SKernelClass observe first last r :=
          nativeGK4TComparison_class observe first last hseam r
    calc
      s = nativeGK4EP92ToStructural first last q := hq.symm
      _ = nativeGK4EP92ToStructural first last r :=
        hreflect q r
          ((nativeGK4SKernelClass_eq_iff observe first last q r).mp hclasses)
      _ = t := hr

/-- Compose F with the true GK4S kernel-image equivalence. This is
the TRUE GK4Q image triangle, not an identification of the original
Type-valued P92B evidence with observed equality. -/
theorem nativeGK4TComparison_image_triangle
    (hseam : nativeGK4NSeamInvariant first last (observe first last))
    (q : NativeF55P92AssocRouteClasses first last) :
    nativeGK4SKernelImageEquiv observe first last
        (nativeGK4TComparison observe first last hseam
          (nativeGK4EP92ToStructural first last q)) =
      nativeGK4QOfClass observe first last q := by
  rw [nativeGK4TComparison_class, nativeGK4SKernelImageEquiv_class]

end UniversalComparison

section BooleanVsOption

variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E} {n n' m m' : Nat}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}
variable (first : KuuNativeF45Tree p n m ma pa mb pb)
variable (last : KuuNativeF45Tree p n' m' ma pa mb pb)

/-- Genuine Boolean structural-to-kernel comparison exists at EVERY
fully dependent original F45 boundary. -/
theorem nativeGK4T_boolean_comparison_exists :
    NativeGK4TComparisonExists
      (nativeGK4OBooleanFamily p D E) first last := by
  exact (nativeGK4TComparisonExists_iff_seam
    (nativeGK4OBooleanFamily p D E) first last).mpr
      (nativeGK4N_boolean_seam_invariant first last)

/-- In fact the Boolean comparison is uniquely determined by
its commuting ORIGINAL P92B triangle. -/
theorem nativeGK4T_boolean_comparison_unique :
    ∃! F : NativeGK4EStructuralRouteClasses first last →
        NativeGK4SKernelClasses (nativeGK4OBooleanFamily p D E) first last,
      ∀ q : NativeF55P92AssocRouteClasses first last,
        F (nativeGK4EP92ToStructural first last q) =
          nativeGK4SKernelClass
            (nativeGK4OBooleanFamily p D E) first last q := by
  exact (nativeGK4TComparison_existsUnique_iff_seam
    (nativeGK4OBooleanFamily p D E) first last).mpr
      (nativeGK4N_boolean_seam_invariant first last)

end BooleanVsOption

section OptionObstruction

variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E} {n m : Nat}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}
variable (tree : KuuNativeF45Tree p n m ma pa mb pb)

/-- A real F54 leftUnit seam has Option Nat some 2 vs some 1.
Hence NO S -> K_Option comparison can commute with pi and kappa at
ANY inhabited original F45 self-boundary. -/
theorem nativeGK4T_option_comparison_not_exists :
    ¬ NativeGK4TComparisonExists
      (nativeGK4OOptionFamily p D E) tree tree := by
  intro h
  have hseam :=
    (nativeGK4TComparisonExists_iff_seam
      (nativeGK4OOptionFamily p D E) tree tree).mp h
  exact nativeGK4N_original_option_fails_seam tree hseam

/-- Side-by-side classification at one genuine F45 stage: the Boolean
kernel has a UNIQUE structural comparison, the strictly finer Option
Nat kernel has NONE. -/
theorem nativeGK4T_boolean_yes_option_no :
    NativeGK4TComparisonExists
        (nativeGK4OBooleanFamily p D E) tree tree ∧
      ¬ NativeGK4TComparisonExists
        (nativeGK4OOptionFamily p D E) tree tree := by
  exact ⟨nativeGK4T_boolean_comparison_exists tree tree,
    nativeGK4T_option_comparison_not_exists tree⟩

end OptionObstruction

section PhysicalNorth

/-- Genuine physical C60 north F45 triple: Boolean comparison exists
but the source P92B-to-Boolean-kernel map is NOT injective; separately
Option Nat lacks any structural-to-kernel comparison. These are three
different exact authority statements, without original associativity. -/
theorem nativeGK4T_physical_north_boundary_contrast :
    NativeGK4TComparisonExists
        (nativeGK4OBooleanFamily _ _ _)
        nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple ∧
      ¬ NativeGK4TComparisonExists
        (nativeGK4OOptionFamily _ _ _)
        nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple ∧
      ¬ Function.Injective
        (nativeGK4SKernelClass (nativeGK4OBooleanFamily _ _ _)
          nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple) := by
  exact ⟨nativeGK4T_boolean_comparison_exists
      nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple,
    nativeGK4T_option_comparison_not_exists nativeGK4FPhysicalNorthTriple,
    nativeGK4SPhysicalNorthBooleanKernel_not_injective⟩

end PhysicalNorth

#print axioms NativeGK4TComparisonExists
#print axioms nativeGK4TComparison
#print axioms nativeGK4TComparison_route
#print axioms nativeGK4TComparison_class
#print axioms nativeGK4TComparison_triangle
#print axioms nativeGK4TComparisonExists_iff_fiber
#print axioms nativeGK4TComparisonExists_iff_seam
#print axioms nativeGK4TComparison_unique
#print axioms nativeGK4TComparison_existsUnique_iff_seam
#print axioms nativeGK4TComparison_surjective
#print axioms nativeGK4TComparison_injective_iff_reflects
#print axioms nativeGK4TComparison_image_triangle
#print axioms nativeGK4T_boolean_comparison_exists
#print axioms nativeGK4T_boolean_comparison_unique
#print axioms nativeGK4T_option_comparison_not_exists
#print axioms nativeGK4T_boolean_yes_option_no
#print axioms nativeGK4T_physical_north_boundary_contrast

end
end Kuu.F112.Physical
