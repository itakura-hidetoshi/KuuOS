import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4AHAlternativeMatrixInvariant
import Mathlib.Tactic

/-!
F112-P94D3GK4AH — genuine residual NONFAITHFULNESS of the original
independent S -> joint (four-component, old 2x2 matrix) K_AG comparison.

Let C be the true double-Nat castDepths self-route and B the true
two-edge forward/backward original F54 LocalRotation backtrack.
u=C;B^6;C and v=B^3;C^2;B^3 are truly fully dependent typed
F54 self-routes. BOTH original GK4AE four-component observations
coincide at (false,-2,6,-6); BOTH prior GK4AF integer matrix values
coincide at [[1,2],[0,1]], so K_AG identifies their images.

The independently proved new alternate F54 matrix assigns
u=[[-11,-16],[-24,-35]] and v=[[-155,-64],[264,109]].
All true F55/P92B and structural Type-valued comparisons preserve
the new matrix (proved in the imported alternative invariant file).
Hence [u]_S != [v]_S but F_AG([u]_S)=F_AG([v]_S):
the genuinely refined S -> K_AG comparison is STILL not faithful
on any witnessed original F54 local rotation, including physical
C60 north. No unwarranted S equivalence or original Q category laws.
Append-only, same-root 107, no Gray. Protected #1558 unchanged.
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

section ActualOriginalF54Residual
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E} {n m : Nat}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable {before after : KuuNativeF45Tree p n m ma pa mb pb}
variable (rot : KuuNativeF45Tree.LocalRotation p before after)

/-- Three real physical two-edge F54 backtracks, not a formal word
without original LocalRotation witnesses. -/
def nativeGK4AHBacktrackTriple :
    KuuNativeF45Tree.DepthRotationRoute p before before :=
  .trans (nativeGK4FBacktrack rot)
    (.trans (nativeGK4FBacktrack rot) (nativeGK4FBacktrack rot))

/-- Six true typed F54 backtracks, parenthesized inside this source. -/
def nativeGK4AHBacktrackSix :
    KuuNativeF45Tree.DepthRotationRoute p before before :=
  .trans (nativeGK4AHBacktrackTriple rot) (nativeGK4AHBacktrackTriple rot)

/-- Two true double-Nat original F54 castDepths self-routes. -/
def nativeGK4AHCastTwice
    (tree : KuuNativeF45Tree p n m ma pa mb pb) :
    KuuNativeF45Tree.DepthRotationRoute p tree tree :=
  .trans (nativeGK4WCastRoute tree) (nativeGK4WCastRoute tree)

/-- Genuine original source word C;B^6;C. -/
def nativeGK4AHWordCB6C :
    KuuNativeF45Tree.DepthRotationRoute p before before :=
  .trans (nativeGK4WCastRoute before)
    (.trans (nativeGK4AHBacktrackSix rot) (nativeGK4WCastRoute before))

/-- Genuine original source word B^3;C^2;B^3. -/
def nativeGK4AHWordB3C2B3 :
    KuuNativeF45Tree.DepthRotationRoute p before before :=
  .trans (nativeGK4AHBacktrackTriple rot)
    (.trans (nativeGK4AHCastTwice before) (nativeGK4AHBacktrackTriple rot))

/-- EXACT SAME original four-component GK4AE observer, not
only a projection to cast/backward counts. -/
theorem nativeGK4AHWords_sameFour :
    nativeGK4AEQuadStructural before before
        (nativeGK4EStructuralRouteClass before before (nativeGK4AHWordCB6C rot)) =
      nativeGK4AEQuadStructural before before
        (nativeGK4EStructuralRouteClass before before (nativeGK4AHWordB3C2B3 rot)) := by
  rfl

theorem nativeGK4AHWordCB6C_quad :
    nativeGK4AEQuadStructural before before
      (nativeGK4EStructuralRouteClass before before (nativeGK4AHWordCB6C rot)) =
      (false, (((-2 : Int), (6 : Nat)), (-6 : Int))) := by
  rfl

theorem nativeGK4AHWordB3C2B3_quad :
    nativeGK4AEQuadStructural before before
      (nativeGK4EStructuralRouteClass before before (nativeGK4AHWordB3C2B3 rot)) =
      (false, (((-2 : Int), (6 : Nat)), (-6 : Int))) := by
  rfl

/-- Original GK4AF representation has B^3=-I and B^6=I, hence
these distinct original F54 histories map to the same matrix C^2. -/
theorem nativeGK4AHWordCB6C_oldMatrix :
    (nativeGK4AHWordCB6C rot).gk4afMatrix =
      (((1 : Int), (2 : Int)), ((0 : Int), (1 : Int))) := by
  rfl

theorem nativeGK4AHWordB3C2B3_oldMatrix :
    (nativeGK4AHWordB3C2B3 rot).gk4afMatrix =
      (((1 : Int), (2 : Int)), ((0 : Int), (1 : Int))) := by
  rfl

theorem nativeGK4AHWords_sameOldMatrix :
    (nativeGK4AHWordCB6C rot).gk4afMatrix =
      (nativeGK4AHWordB3C2B3 rot).gk4afMatrix := by
  rw [nativeGK4AHWordCB6C_oldMatrix, nativeGK4AHWordB3C2B3_oldMatrix]

/-- The new independent matrix representation does NOT impose
B^3=-I, so it detects what the old matrix erases. -/
theorem nativeGK4AHWordCB6C_newMatrix :
    (nativeGK4AHWordCB6C rot).gk4ahMatrix =
      (((-11 : Int), (-16 : Int)), ((-24 : Int), (-35 : Int))) := by
  rfl

theorem nativeGK4AHWordB3C2B3_newMatrix :
    (nativeGK4AHWordB3C2B3 rot).gk4ahMatrix =
      (((-155 : Int), (-64 : Int)), ((264 : Int), (109 : Int))) := by
  rfl

/-- Original independent S cannot identify two actual Type-valued
source routes when a genuinely seam-invariant matrix separates them. -/
theorem nativeGK4AHStructuralClasses_ne :
    nativeGK4EStructuralRouteClass before before (nativeGK4AHWordCB6C rot) ≠
      nativeGK4EStructuralRouteClass before before (nativeGK4AHWordB3C2B3 rot) := by
  intro heq
  have hv := congrArg (nativeGK4AHStructuralValue before before) heq
  change (nativeGK4AHWordCB6C rot).gk4ahMatrix =
    (nativeGK4AHWordB3C2B3 rot).gk4ahMatrix at hv
  rw [nativeGK4AHWordCB6C_newMatrix, nativeGK4AHWordB3C2B3_newMatrix] at hv
  have hentry := congrArg (fun m : NativeGK4AHMatrix => m.1.1) hv
  change (-11 : Int) = (-155 : Int) at hentry
  omega

/-- The NEW joint observer O_AG still identifies the pair despite
including all FOUR original GK4AE values and the FULL GK4AF matrix. -/
theorem nativeGK4AHWords_sameJoint :
    nativeGK4AGStructural before before
        (nativeGK4EStructuralRouteClass before before (nativeGK4AHWordCB6C rot)) =
      nativeGK4AGStructural before before
        (nativeGK4EStructuralRouteClass before before (nativeGK4AHWordB3C2B3 rot)) := by
  apply Prod.ext
  · exact nativeGK4AHWords_sameFour rot
  · change (nativeGK4AHWordCB6C rot).gk4afMatrix =
      (nativeGK4AHWordB3C2B3 rot).gk4afMatrix
    exact nativeGK4AHWords_sameOldMatrix rot

theorem nativeGK4AHJointKernel_equal :
    nativeGK4AGComparison before before
        (nativeGK4EStructuralRouteClass before before (nativeGK4AHWordCB6C rot)) =
      nativeGK4AGComparison before before
        (nativeGK4EStructuralRouteClass before before (nativeGK4AHWordB3C2B3 rot)) := by
  exact (nativeGK4AGComparison_eq_iff before before _ _).mpr
    (nativeGK4AHWords_sameJoint rot)

/-- MAIN RESULT: S -> K_AG is still nonfaithful, not even locally
on the original F54 self-Hom containing a real local rotation. -/
theorem nativeGK4AHComparison_not_injective
    (rot : KuuNativeF45Tree.LocalRotation p before after) :
    ¬ Function.Injective (nativeGK4AGComparison before before) := by
  intro hinj
  exact nativeGK4AHStructuralClasses_ne rot
    (hinj (nativeGK4AHJointKernel_equal rot))

end ActualOriginalF54Residual

/-- No synthetic local rotation: the genuine physical C60 north
hexagon supplies an unconditional typed nonfaithfulness witness. -/
theorem nativeGK4AHPhysicalNorth_joint_nonfaithful :
    ¬ Function.Injective
      (nativeGK4AGComparison
        nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple) := by
  exact nativeGK4AHComparison_not_injective northHexagonNativeLeftRotation

#print axioms nativeGK4AHBacktrackTriple
#print axioms nativeGK4AHBacktrackSix
#print axioms nativeGK4AHCastTwice
#print axioms nativeGK4AHWordCB6C
#print axioms nativeGK4AHWordB3C2B3
#print axioms nativeGK4AHWords_sameFour
#print axioms nativeGK4AHWordCB6C_quad
#print axioms nativeGK4AHWordB3C2B3_quad
#print axioms nativeGK4AHWordCB6C_oldMatrix
#print axioms nativeGK4AHWordB3C2B3_oldMatrix
#print axioms nativeGK4AHWords_sameOldMatrix
#print axioms nativeGK4AHWordCB6C_newMatrix
#print axioms nativeGK4AHWordB3C2B3_newMatrix
#print axioms nativeGK4AHStructuralClasses_ne
#print axioms nativeGK4AHWords_sameJoint
#print axioms nativeGK4AHJointKernel_equal
#print axioms nativeGK4AHComparison_not_injective
#print axioms nativeGK4AHPhysicalNorth_joint_nonfaithful

end
end Kuu.F112.Physical
