import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4AIForgetful
import Mathlib.Tactic

/-!
F112-P94D3GK4AJ — a genuine THREE-CLASS fixed observer fiber of
the original F54 typed forgetful K_AI -> K_AG, improving the certified
GK4AI two-class witness. All three share *one* old GK4AG observation:
the original four-coordinate value and the first full integer matrix.
The second independently structurally sound integer matrix separates
them into three different K_AI classes. No synthetic generators:
C = actual original double-Nat castDepths self-route,
B = actual two-edge physical forward/backward F54 LocalRotation
backtrack, preserving every dependent intermediate F45 tree.

Words at 12 true physical backtracks:
  w0 = C ; B^12 ; C
  w1 = B^3 ; C ; B^6 ; C ; B^3
  w2 = B^6 ; C^2 ; B^6
The OLD matrix B1^3=-I and B1^6=I forces the same M_AF=C^2.
The true four-component observation also agrees in all three.
But the new GK4AH matrix separates all three in one SAME K_AG fiber.

This proves a THREE-class lower bound on a real attained forgetful
fiber (including the physical C60 north), without any claim of
faithfulness of S->K_AI, original Q category axioms, Gray, historical
full equivalence or hyperdescent. Append-only, same-root 107,
strict 空 central; independent Kuu one presentation.
Protect validation-only PR #1558 Draft/open/unmerged.
Lean v4.30.0-rc2, pinned mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section
universe uD vD uE vE

section OriginalTypedTriple
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E} {n m : Nat}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable {before after : KuuNativeF45Tree p n m ma pa mb pb}
variable (rot : KuuNativeF45Tree.LocalRotation p before after)

/-- Twelve genuinely witnessed physical original F54 backtracks. -/
def nativeGK4AJBacktrackTwelve :
    KuuNativeF45Tree.DepthRotationRoute p before before :=
  .trans (nativeGK4AHBacktrackSix rot) (nativeGK4AHBacktrackSix rot)

/-- Original route: cast, twelve physical backtracks, cast. -/
def nativeGK4AJWord0 :
    KuuNativeF45Tree.DepthRotationRoute p before before :=
  .trans (nativeGK4WCastRoute before)
    (.trans (nativeGK4AJBacktrackTwelve rot) (nativeGK4WCastRoute before))

/-- Original route: three backtracks, cast, six backtracks, cast,
three backtracks. The endpoint and every intermediate tree are real. -/
def nativeGK4AJWord1 :
    KuuNativeF45Tree.DepthRotationRoute p before before :=
  .trans (nativeGK4AHBacktrackTriple rot)
    (.trans (nativeGK4WCastRoute before)
      (.trans (nativeGK4AHBacktrackSix rot)
        (.trans (nativeGK4WCastRoute before)
          (nativeGK4AHBacktrackTriple rot))))

/-- Original route: six backtracks, two true double-Nat casts,
six backtracks. -/
def nativeGK4AJWord2 :
    KuuNativeF45Tree.DepthRotationRoute p before before :=
  .trans (nativeGK4AHBacktrackSix rot)
    (.trans (nativeGK4AHCastTwice before) (nativeGK4AHBacktrackSix rot))

/-- All three original source words have THE SAME actual four-
component observation plus complete previous GK4AF matrix,
not merely the same counts. -/
theorem nativeGK4AJWord01_sameOld :
    nativeGK4AGStructural before before
      (nativeGK4EStructuralRouteClass before before (nativeGK4AJWord0 rot)) =
    nativeGK4AGStructural before before
      (nativeGK4EStructuralRouteClass before before (nativeGK4AJWord1 rot)) := by
  rfl

theorem nativeGK4AJWord02_sameOld :
    nativeGK4AGStructural before before
      (nativeGK4EStructuralRouteClass before before (nativeGK4AJWord0 rot)) =
    nativeGK4AGStructural before before
      (nativeGK4EStructuralRouteClass before before (nativeGK4AJWord2 rot)) := by
  rfl

/-- The actual old observable value is the same fixed value for
the three words (not three different target K_AG classes). -/
theorem nativeGK4AJWord0_oldValue :
    nativeGK4AGStructural before before
      (nativeGK4EStructuralRouteClass before before (nativeGK4AJWord0 rot)) =
      ((false, (((-22 : Int), (12 : Nat)), (-132 : Int))),
        (((1 : Int), (2 : Int)), ((0 : Int), (1 : Int)))) := by
  rfl

/-- Three exact and different integer matrix evaluations of genuinely
typed F54 routes; all previous original P92B/structural seams preserve
the GK4AH matrix by the imported soundness theorem. -/
theorem nativeGK4AJWord0_matrix :
    (nativeGK4AJWord0 rot).gk4ahMatrix =
      (((-23 : Int), (-34 : Int)), ((-48 : Int), (-71 : Int))) := by
  rfl

theorem nativeGK4AJWord1_matrix :
    (nativeGK4AJWord1 rot).gk4ahMatrix =
      (((1561 : Int), (638 : Int)), ((-2640 : Int), (-1079 : Int))) := by
  rfl

theorem nativeGK4AJWord2_matrix :
    (nativeGK4AJWord2 rot).gk4ahMatrix =
      (((-599 : Int), (-274 : Int)), ((1104 : Int), (505 : Int))) := by
  rfl

/-- Genuine new second-kernel classes of the ORIGINAL P92B Q quotient
after independent structural comparison; never raw history strings. -/
def nativeGK4AJClass0 :
    NativeGK4SKernelClasses (nativeGK4AIP92Family p D E) before before :=
  nativeGK4AIComparison before before
    (nativeGK4EStructuralRouteClass before before (nativeGK4AJWord0 rot))

def nativeGK4AJClass1 :
    NativeGK4SKernelClasses (nativeGK4AIP92Family p D E) before before :=
  nativeGK4AIComparison before before
    (nativeGK4EStructuralRouteClass before before (nativeGK4AJWord1 rot))

def nativeGK4AJClass2 :
    NativeGK4SKernelClasses (nativeGK4AIP92Family p D E) before before :=
  nativeGK4AIComparison before before
    (nativeGK4EStructuralRouteClass before before (nativeGK4AJWord2 rot))

@[simp] theorem nativeGK4AJClass0_matrix :
    (nativeGK4AIKernelValue before before (nativeGK4AJClass0 rot)).2 =
      (((-23 : Int), (-34 : Int)), ((-48 : Int), (-71 : Int))) := by
  rfl

@[simp] theorem nativeGK4AJClass1_matrix :
    (nativeGK4AIKernelValue before before (nativeGK4AJClass1 rot)).2 =
      (((1561 : Int), (638 : Int)), ((-2640 : Int), (-1079 : Int))) := by
  rfl

@[simp] theorem nativeGK4AJClass2_matrix :
    (nativeGK4AIKernelValue before before (nativeGK4AJClass2 rot)).2 =
      (((-599 : Int), (-274 : Int)), ((1104 : Int), (505 : Int))) := by
  rfl

/-- Three pairwise different REAL second-kernel classes, even though
their old joint observation is identical. -/
theorem nativeGK4AJClass0_ne_1 : nativeGK4AJClass0 rot ≠ nativeGK4AJClass1 rot := by
  intro h
  have hm := congrArg
    (fun z : NativeGK4SKernelClasses (nativeGK4AIP92Family p D E) before before =>
      (nativeGK4AIKernelValue before before z).2) h
  change (nativeGK4AIKernelValue before before (nativeGK4AJClass0 rot)).2 =
    (nativeGK4AIKernelValue before before (nativeGK4AJClass1 rot)).2 at hm
  rw [nativeGK4AJClass0_matrix, nativeGK4AJClass1_matrix] at hm
  have hentry := congrArg (fun q : NativeGK4AHMatrix => q.1.1) hm
  change (-23 : Int) = (1561 : Int) at hentry
  omega

theorem nativeGK4AJClass0_ne_2 : nativeGK4AJClass0 rot ≠ nativeGK4AJClass2 rot := by
  intro h
  have hm := congrArg
    (fun z : NativeGK4SKernelClasses (nativeGK4AIP92Family p D E) before before =>
      (nativeGK4AIKernelValue before before z).2) h
  change (nativeGK4AIKernelValue before before (nativeGK4AJClass0 rot)).2 =
    (nativeGK4AIKernelValue before before (nativeGK4AJClass2 rot)).2 at hm
  rw [nativeGK4AJClass0_matrix, nativeGK4AJClass2_matrix] at hm
  have hentry := congrArg (fun q : NativeGK4AHMatrix => q.1.1) hm
  change (-23 : Int) = (-599 : Int) at hentry
  omega

theorem nativeGK4AJClass1_ne_2 : nativeGK4AJClass1 rot ≠ nativeGK4AJClass2 rot := by
  intro h
  have hm := congrArg
    (fun z : NativeGK4SKernelClasses (nativeGK4AIP92Family p D E) before before =>
      (nativeGK4AIKernelValue before before z).2) h
  change (nativeGK4AIKernelValue before before (nativeGK4AJClass1 rot)).2 =
    (nativeGK4AIKernelValue before before (nativeGK4AJClass2 rot)).2 at hm
  rw [nativeGK4AJClass1_matrix, nativeGK4AJClass2_matrix] at hm
  have hentry := congrArg (fun q : NativeGK4AHMatrix => q.1.1) hm
  change (1561 : Int) = (-599 : Int) at hentry
  omega

/-- All three distinct new classes share ONE actual old K_AG class. -/
theorem nativeGK4AJClass0_forget_eq_1 :
    nativeGK4AIForgetMatrix before before (nativeGK4AJClass0 rot) =
      nativeGK4AIForgetMatrix before before (nativeGK4AJClass1 rot) := by
  simpa only [nativeGK4AJClass0, nativeGK4AJClass1,
    nativeGK4AIForgetMatrix_comparison] using
    ((nativeGK4AGComparison_eq_iff before before _ _).mpr
      (nativeGK4AJWord01_sameOld rot))

theorem nativeGK4AJClass0_forget_eq_2 :
    nativeGK4AIForgetMatrix before before (nativeGK4AJClass0 rot) =
      nativeGK4AIForgetMatrix before before (nativeGK4AJClass2 rot) := by
  simpa only [nativeGK4AJClass0, nativeGK4AJClass2,
    nativeGK4AIForgetMatrix_comparison] using
    ((nativeGK4AGComparison_eq_iff before before _ _).mpr
      (nativeGK4AJWord02_sameOld rot))

/-- A stronger obstruction than GK4AI: the forgetful has a fiber
containing THREE DISTINCT original attained K_AI classes, all on
one and the SAME original fully typed self-Hom. -/
theorem nativeGK4AJ_three_classes_one_fiber
    (rot : KuuNativeF45Tree.LocalRotation p before after) :
    ∃ x y z : NativeGK4SKernelClasses
        (nativeGK4AIP92Family p D E) before before,
      x ≠ y ∧ x ≠ z ∧ y ≠ z ∧
      nativeGK4AIForgetMatrix before before x =
        nativeGK4AIForgetMatrix before before y ∧
      nativeGK4AIForgetMatrix before before x =
        nativeGK4AIForgetMatrix before before z := by
  exact ⟨nativeGK4AJClass0 rot, nativeGK4AJClass1 rot, nativeGK4AJClass2 rot,
    nativeGK4AJClass0_ne_1 rot, nativeGK4AJClass0_ne_2 rot,
    nativeGK4AJClass1_ne_2 rot, nativeGK4AJClass0_forget_eq_1 rot,
    nativeGK4AJClass0_forget_eq_2 rot⟩

end OriginalTypedTriple

#print axioms nativeGK4AJBacktrackTwelve
#print axioms nativeGK4AJWord0
#print axioms nativeGK4AJWord1
#print axioms nativeGK4AJWord2
#print axioms nativeGK4AJWord01_sameOld
#print axioms nativeGK4AJWord02_sameOld
#print axioms nativeGK4AJWord0_oldValue
#print axioms nativeGK4AJWord0_matrix
#print axioms nativeGK4AJWord1_matrix
#print axioms nativeGK4AJWord2_matrix
#print axioms nativeGK4AJClass0
#print axioms nativeGK4AJClass1
#print axioms nativeGK4AJClass2
#print axioms nativeGK4AJClass0_matrix
#print axioms nativeGK4AJClass1_matrix
#print axioms nativeGK4AJClass2_matrix
#print axioms nativeGK4AJClass0_ne_1
#print axioms nativeGK4AJClass0_ne_2
#print axioms nativeGK4AJClass1_ne_2
#print axioms nativeGK4AJClass0_forget_eq_1
#print axioms nativeGK4AJClass0_forget_eq_2
#print axioms nativeGK4AJ_three_classes_one_fiber

end
end Kuu.F112.Physical
