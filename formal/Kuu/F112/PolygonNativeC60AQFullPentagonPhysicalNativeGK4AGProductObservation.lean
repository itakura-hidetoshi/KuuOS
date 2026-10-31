import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4AFResidualNonfaithfulness
import Mathlib.Tactic

/-!
F112-P94D3GK4AG — actual four-component plus noncommutative matrix
observation on original fully typed F54 source, original P92B Q and
separately generated structural S. No original Q category axioms are
postulated: second kernels inherit category laws from attained values.

All original F55 (9), P92B (9), structural seams (14) and extended
comparisons (3) are preserved componentwise by the already certified
GK4AE/GK4AF Type-valued soundness theorems. The new observation is a
strict *refinement*, not a claim of global S faithfulness.
Lean v4.30.0-rc2; mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Append-only, same-root 107, protected validation-only PR #1558 unmerged.
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

/-- The fifth observation is a WHOLE matrix, not merely its trace,
determinant or an abelianized count. -/
abbrev NativeGK4AGValue := NativeGK4AEValue × NativeGK4AFMatrix

def nativeGK4AGCombine (u v : NativeGK4AGValue) : NativeGK4AGValue :=
  (nativeGK4AECombine u.1 v.1, nativeGK4AFMul u.2 v.2)

def nativeGK4AGUnit : NativeGK4AGValue :=
  (nativeGK4AEUnit, nativeGK4AFOne)

theorem nativeGK4AGCombine_assoc (u v w : NativeGK4AGValue) :
    nativeGK4AGCombine (nativeGK4AGCombine u v) w =
      nativeGK4AGCombine u (nativeGK4AGCombine v w) := by
  apply Prod.ext
  · exact nativeGK4AECombine_assoc u.1 v.1 w.1
  · exact nativeGK4AFMul_assoc u.2 v.2 w.2

theorem nativeGK4AGCombine_leftUnit (u : NativeGK4AGValue) :
    nativeGK4AGCombine nativeGK4AGUnit u = u := by
  apply Prod.ext
  · exact nativeGK4AECombine_leftUnit u.1
  · exact nativeGK4AFMul_leftUnit u.2

theorem nativeGK4AGCombine_rightUnit (u : NativeGK4AGValue) :
    nativeGK4AGCombine u nativeGK4AGUnit = u := by
  apply Prod.ext
  · exact nativeGK4AECombine_rightUnit u.1
  · exact nativeGK4AFMul_rightUnit u.2

/-- Forget ONLY the matrix value; preserve the full existing
four-component noncommutative GK4AE observation. -/
def nativeGK4AGForgetValue (v : NativeGK4AGValue) :
    NativeGK4AEValue := v.1

theorem nativeGK4AGForgetValue_combine (u v : NativeGK4AGValue) :
    nativeGK4AGForgetValue (nativeGK4AGCombine u v) =
      nativeGK4AECombine
        (nativeGK4AGForgetValue u) (nativeGK4AGForgetValue v) := rfl

theorem nativeGK4AGForgetValue_unit :
    nativeGK4AGForgetValue nativeGK4AGUnit = nativeGK4AEUnit := rfl

section RealOriginalSource
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
variable (first : KuuNativeF45Tree p n₁ m₁ ma pa mb pb)
variable (middle : KuuNativeF45Tree p n₂ m₂ ma pa mb pb)
variable (last : KuuNativeF45Tree p n₃ m₃ ma pa mb pb)

/-- Original P92B quotient's true noncommutative matrix multiplication;
no P92B source category laws are invoked. -/
theorem nativeGK4AGMatrixP92_compose
    (u : NativeF55P92AssocRouteClasses first middle)
    (v : NativeF55P92AssocRouteClasses middle last) :
    nativeGK4AFP92Value first last
        (nativeGK4H_p92Compose first middle last u v) =
      nativeGK4AFMul
        (nativeGK4AFP92Value first middle u)
        (nativeGK4AFP92Value middle last v) := by
  refine _root_.Quotient.inductionOn₂ u v ?_
  intro rawU rawV
  exact nativeGK4AF_trans rawU rawV

@[simp] theorem nativeGK4AGMatrixP92_unit :
    nativeGK4AFP92Value first first (nativeGK4H_p92Unit first) =
      nativeGK4AFOne := rfl

/-- Joint observer descends on ORIGINAL Q, using separately proved
actual F55/P92B cells for both components. -/
def nativeGK4AGP92
    (q : NativeF55P92AssocRouteClasses first middle) :
    NativeGK4AGValue :=
  (nativeGK4AEQuadP92 first middle q, nativeGK4AFP92Value first middle q)

/-- Independent descent on structural S, using all real fourteen
structural seam constructors, not a fabricated original P92B 3-cell. -/
def nativeGK4AGStructural
    (s : NativeGK4EStructuralRouteClasses first middle) :
    NativeGK4AGValue :=
  (nativeGK4AEQuadStructural first middle s,
    nativeGK4AFStructuralValue first middle s)

@[simp] theorem nativeGK4AGP92_class
    (raw : KuuNativeF45Tree.DepthRotationRoute p first middle) :
    nativeGK4AGP92 first middle
        (nativeF55P92AssocRouteClass first middle raw) =
      ((nativeGK4GRawGrade first middle raw, raw.gk4adValue),
        raw.gk4afMatrix) := rfl

@[simp] theorem nativeGK4AGStructural_class
    (raw : KuuNativeF45Tree.DepthRotationRoute p first middle) :
    nativeGK4AGStructural first middle
        (nativeGK4EStructuralRouteClass first middle raw) =
      ((nativeGK4GRawGrade first middle raw, raw.gk4adValue),
        raw.gk4afMatrix) := rfl

/-- The original Q-to-S quotient comparison commutes with the new
pair observation by independently descending BOTH components. -/
theorem nativeGK4AG_commutes
    (q : NativeF55P92AssocRouteClasses first middle) :
    nativeGK4AGStructural first middle
        (nativeGK4EP92ToStructural first middle q) =
      nativeGK4AGP92 first middle q := by
  apply Prod.ext
  · exact nativeGK4AEQuad_commutes first middle q
  · exact nativeGK4AF_commutes first middle q

theorem nativeGK4AGP92_compose
    (u : NativeF55P92AssocRouteClasses first middle)
    (v : NativeF55P92AssocRouteClasses middle last) :
    nativeGK4AGP92 first last
        (nativeGK4H_p92Compose first middle last u v) =
      nativeGK4AGCombine
        (nativeGK4AGP92 first middle u)
        (nativeGK4AGP92 middle last v) := by
  apply Prod.ext
  · exact nativeGK4AEQuadP92_compose first middle last u v
  · exact nativeGK4AGMatrixP92_compose first middle last u v

theorem nativeGK4AGStructural_compose
    (u : NativeGK4EStructuralRouteClasses first middle)
    (v : NativeGK4EStructuralRouteClasses middle last) :
    nativeGK4AGStructural first last
        (nativeGK4H_structuralCompose first middle last u v) =
      nativeGK4AGCombine
        (nativeGK4AGStructural first middle u)
        (nativeGK4AGStructural middle last v) := by
  apply Prod.ext
  · exact nativeGK4AEQuadStructural_compose first middle last u v
  · exact nativeGK4AFStructural_compose first middle last u v

@[simp] theorem nativeGK4AGP92_unit :
    nativeGK4AGP92 first first
        (nativeGK4H_p92Unit first) = nativeGK4AGUnit := rfl

@[simp] theorem nativeGK4AGStructural_unit :
    nativeGK4AGStructural first first
        (nativeGK4H_structuralUnit first) = nativeGK4AGUnit := rfl

end RealOriginalSource

/-- Actual original fully dependent P92B observation family. -/
def nativeGK4AGP92Family
    (p : Polygon)
    (D : Type uD) [Category.{vD} D]
    (E : Type uE) [Category.{vE} E] :
    NativeGK4OObserverFamily p D E NativeGK4AGValue :=
  fun first last q => nativeGK4AGP92 first last q

/-- Genuine F54 composition and both original fully typed contexts act
on the ordered pair by its PRODUCT monoid, never by commutative counts. -/
theorem nativeGK4AGLaws
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] :
    NativeGK4PObservationLaws
      (nativeGK4AGP92Family p D E) nativeGK4AGCombine
      (nativeGK4PIdentityAction p D E NativeGK4AGValue)
      (nativeGK4PIdentityAction p D E NativeGK4AGValue) := by
  constructor
  · intro a b x y ma mb pa pb n₁ n₂ n₃ m₁ m₂ m₃ t₁ t₂ t₃ u v
    change
      ((nativeGK4GRawGrade t₁ t₃ (.trans u v),
        (KuuNativeF45Tree.DepthRotationRoute.trans u v).gk4adValue),
        (KuuNativeF45Tree.DepthRotationRoute.trans u v).gk4afMatrix) =
        nativeGK4AGCombine
          ((nativeGK4GRawGrade t₁ t₂ u, u.gk4adValue), u.gk4afMatrix)
          ((nativeGK4GRawGrade t₂ t₃ v, v.gk4adValue), v.gk4afMatrix)
    apply Prod.ext
    · apply Prod.ext
      · exact nativeGK4H_rawGrade_compose t₁ t₂ t₃ u v
      · exact nativeGK4AD_trans u v
    · exact nativeGK4AF_trans u v
  · intro a b x y n n' m m' k l ma mb mc pa pb pc first last r later
    rfl
  · intro a b x y k l n n' m m' ma mb mc pa pb pc earlier first last r
    rfl

/-- All fourteen ORIGINAL structural seam constructors preserve the
joint observation, with independently certified Type-cell witnesses. -/
theorem nativeGK4AGSeamInvariant
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :
    nativeGK4NSeamInvariant first last
      (nativeGK4AGP92Family p D E first last) := by
  intro r s seam
  apply Prod.ext
  · exact nativeGK4AEQuadSeamInvariant first last r s seam
  · exact nativeGK4AF_seam_sound seam

/-- No original Q category axioms are assumed to obtain descent
to the SECOND attained observation kernel. -/
theorem nativeGK4AGComparisonExists
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :
    NativeGK4TComparisonExists
      (nativeGK4AGP92Family p D E) first last := by
  exact (nativeGK4TComparisonExists_iff_seam
    (nativeGK4AGP92Family p D E) first last).mpr
      (nativeGK4AGSeamInvariant first last)

#print axioms nativeGK4AGCombine_assoc
#print axioms nativeGK4AGCombine_leftUnit
#print axioms nativeGK4AGCombine_rightUnit
#print axioms nativeGK4AGMatrixP92_compose
#print axioms nativeGK4AGP92
#print axioms nativeGK4AGStructural
#print axioms nativeGK4AG_commutes
#print axioms nativeGK4AGP92_compose
#print axioms nativeGK4AGStructural_compose
#print axioms nativeGK4AGLaws
#print axioms nativeGK4AGSeamInvariant
#print axioms nativeGK4AGComparisonExists

end
end Kuu.F112.Physical
