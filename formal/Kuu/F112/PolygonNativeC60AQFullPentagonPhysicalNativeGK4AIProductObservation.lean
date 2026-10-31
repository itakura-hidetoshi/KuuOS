import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4AHJointResidualNonfaithfulness
import Mathlib.Tactic

/-!
F112-P94D3GK4AI — original F54 fully typed THREE-factor observer:
O_AI(r) := (O_AG(r), M_AH(r)) = ((O_AE(r), M_AF(r)), M_AH(r)).
The two distinct independently sound integer 2x2 matrix evaluations
preserve original F55 9, P92B 9 (including assocNaturality), original
structural seams 14 and extended comparisons 3 Type-valued proofs.
No Type-valued P92B 3-cell is generated from an equality of numbers.
Original Q and independent structural S receive distinct descents;
all actual F54 composition and both fully typed contexts are retained.
No original Q category axioms, no historical full typed equivalence,
no Gray or hyperdescent. Append-only, same-root 107.
Strict 空 central, independent Kuu one presentation; protected
validation-only PR #1558 Draft/OPEN/unmerged.
Lean v4.30.0-rc2; mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
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
abbrev NativeGK4AIValue := NativeGK4AGValue × NativeGK4AHMatrix

def nativeGK4AICombine (u v : NativeGK4AIValue) : NativeGK4AIValue :=
  (nativeGK4AGCombine u.1 v.1, nativeGK4AHMul u.2 v.2)

def nativeGK4AIUnit : NativeGK4AIValue :=
  (nativeGK4AGUnit, nativeGK4AHOne)

theorem nativeGK4AICombine_assoc (u v w : NativeGK4AIValue) :
    nativeGK4AICombine (nativeGK4AICombine u v) w =
      nativeGK4AICombine u (nativeGK4AICombine v w) := by
  apply Prod.ext
  · exact nativeGK4AGCombine_assoc u.1 v.1 w.1
  · exact nativeGK4AHMul_assoc u.2 v.2 w.2

theorem nativeGK4AICombine_leftUnit (u : NativeGK4AIValue) :
    nativeGK4AICombine nativeGK4AIUnit u = u := by
  apply Prod.ext
  · exact nativeGK4AGCombine_leftUnit u.1
  · exact nativeGK4AHMul_leftUnit u.2

theorem nativeGK4AICombine_rightUnit (u : NativeGK4AIValue) :
    nativeGK4AICombine u nativeGK4AIUnit = u := by
  apply Prod.ext
  · exact nativeGK4AGCombine_rightUnit u.1
  · exact nativeGK4AHMul_rightUnit u.2

/-- Forget ONLY the matrix value; preserve the full existing
four-component noncommutative GK4AG observation. -/
def nativeGK4AIForgetValue (v : NativeGK4AIValue) :
    NativeGK4AGValue := v.1

theorem nativeGK4AIForgetValue_combine (u v : NativeGK4AIValue) :
    nativeGK4AIForgetValue (nativeGK4AICombine u v) =
      nativeGK4AGCombine
        (nativeGK4AIForgetValue u) (nativeGK4AIForgetValue v) := rfl

theorem nativeGK4AIForgetValue_unit :
    nativeGK4AIForgetValue nativeGK4AIUnit = nativeGK4AGUnit := rfl

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
theorem nativeGK4AIMatrixP92_compose
    (u : NativeF55P92AssocRouteClasses first middle)
    (v : NativeF55P92AssocRouteClasses middle last) :
    nativeGK4AHP92Value first last
        (nativeGK4H_p92Compose first middle last u v) =
      nativeGK4AHMul
        (nativeGK4AHP92Value first middle u)
        (nativeGK4AHP92Value middle last v) := by
  refine _root_.Quotient.inductionOn₂ u v ?_
  intro rawU rawV
  exact nativeGK4AH_trans rawU rawV

@[simp] theorem nativeGK4AIMatrixP92_unit :
    nativeGK4AHP92Value first first (nativeGK4H_p92Unit first) =
      nativeGK4AHOne := rfl

/-- Joint observer descends on ORIGINAL Q, using separately proved
actual F55/P92B cells for both components. -/
def nativeGK4AIP92
    (q : NativeF55P92AssocRouteClasses first middle) :
    NativeGK4AIValue :=
  (nativeGK4AGP92 first middle q, nativeGK4AHP92Value first middle q)

/-- Independent descent on structural S, using all real fourteen
structural seam constructors, not a fabricated original P92B 3-cell. -/
def nativeGK4AIStructural
    (s : NativeGK4EStructuralRouteClasses first middle) :
    NativeGK4AIValue :=
  (nativeGK4AGStructural first middle s,
    nativeGK4AHStructuralValue first middle s)

@[simp] theorem nativeGK4AIP92_class
    (raw : KuuNativeF45Tree.DepthRotationRoute p first middle) :
    nativeGK4AIP92 first middle
        (nativeF55P92AssocRouteClass first middle raw) =
      (((nativeGK4GRawGrade first middle raw, raw.gk4adValue),
          raw.gk4afMatrix), raw.gk4ahMatrix) := rfl

@[simp] theorem nativeGK4AIStructural_class
    (raw : KuuNativeF45Tree.DepthRotationRoute p first middle) :
    nativeGK4AIStructural first middle
        (nativeGK4EStructuralRouteClass first middle raw) =
      (((nativeGK4GRawGrade first middle raw, raw.gk4adValue),
          raw.gk4afMatrix), raw.gk4ahMatrix) := rfl

/-- The original Q-to-S quotient comparison commutes with the new
pair observation by independently descending BOTH components. -/
theorem nativeGK4AI_commutes
    (q : NativeF55P92AssocRouteClasses first middle) :
    nativeGK4AIStructural first middle
        (nativeGK4EP92ToStructural first middle q) =
      nativeGK4AIP92 first middle q := by
  apply Prod.ext
  · exact nativeGK4AG_commutes first middle q
  · exact nativeGK4AH_commutes first middle q

theorem nativeGK4AIP92_compose
    (u : NativeF55P92AssocRouteClasses first middle)
    (v : NativeF55P92AssocRouteClasses middle last) :
    nativeGK4AIP92 first last
        (nativeGK4H_p92Compose first middle last u v) =
      nativeGK4AICombine
        (nativeGK4AIP92 first middle u)
        (nativeGK4AIP92 middle last v) := by
  apply Prod.ext
  · exact nativeGK4AGP92_compose first middle last u v
  · exact nativeGK4AIMatrixP92_compose first middle last u v

theorem nativeGK4AIStructural_compose
    (u : NativeGK4EStructuralRouteClasses first middle)
    (v : NativeGK4EStructuralRouteClasses middle last) :
    nativeGK4AIStructural first last
        (nativeGK4H_structuralCompose first middle last u v) =
      nativeGK4AICombine
        (nativeGK4AIStructural first middle u)
        (nativeGK4AIStructural middle last v) := by
  apply Prod.ext
  · exact nativeGK4AGStructural_compose first middle last u v
  · exact nativeGK4AHStructural_compose first middle last u v

@[simp] theorem nativeGK4AIP92_unit :
    nativeGK4AIP92 first first
        (nativeGK4H_p92Unit first) = nativeGK4AIUnit := rfl

@[simp] theorem nativeGK4AIStructural_unit :
    nativeGK4AIStructural first first
        (nativeGK4H_structuralUnit first) = nativeGK4AIUnit := rfl

end RealOriginalSource

/-- Actual original fully dependent P92B observation family. -/
def nativeGK4AIP92Family
    (p : Polygon)
    (D : Type uD) [Category.{vD} D]
    (E : Type uE) [Category.{vE} E] :
    NativeGK4OObserverFamily p D E NativeGK4AIValue :=
  fun first last q => nativeGK4AIP92 first last q

/-- Genuine F54 composition and both original fully typed contexts act
on the ordered pair by its PRODUCT monoid, never by commutative counts. -/
theorem nativeGK4AILaws
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] :
    NativeGK4PObservationLaws
      (nativeGK4AIP92Family p D E) nativeGK4AICombine
      (nativeGK4PIdentityAction p D E NativeGK4AIValue)
      (nativeGK4PIdentityAction p D E NativeGK4AIValue) := by
  constructor
  · intro a b x y ma mb pa pb n₁ n₂ n₃ m₁ m₂ m₃ t₁ t₂ t₃ u v
    change
      (((nativeGK4GRawGrade t₁ t₃ (.trans u v),
          (KuuNativeF45Tree.DepthRotationRoute.trans u v).gk4adValue),
          (KuuNativeF45Tree.DepthRotationRoute.trans u v).gk4afMatrix),
          (KuuNativeF45Tree.DepthRotationRoute.trans u v).gk4ahMatrix) =
        nativeGK4AICombine
          (((nativeGK4GRawGrade t₁ t₂ u, u.gk4adValue),
            u.gk4afMatrix), u.gk4ahMatrix)
          (((nativeGK4GRawGrade t₂ t₃ v, v.gk4adValue),
            v.gk4afMatrix), v.gk4ahMatrix)
    apply Prod.ext
    · apply Prod.ext
      · apply Prod.ext
        · exact nativeGK4H_rawGrade_compose t₁ t₂ t₃ u v
        · exact nativeGK4AD_trans u v
      · exact nativeGK4AF_trans u v
    · exact nativeGK4AH_trans u v
  · intro a b x y n n' m m' k l ma mb mc pa pb pc first last r later
    rfl
  · intro a b x y k l n n' m m' ma mb mc pa pb pc earlier first last r
    rfl

/-- All fourteen ORIGINAL structural seam constructors preserve the
joint observation, with independently certified Type-cell witnesses. -/
theorem nativeGK4AISeamInvariant
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :
    nativeGK4NSeamInvariant first last
      (nativeGK4AIP92Family p D E first last) := by
  intro r s seam
  apply Prod.ext
  · exact nativeGK4AGSeamInvariant first last r s seam
  · exact nativeGK4AH_seam_sound seam

/-- No original Q category axioms are assumed to obtain descent
to the SECOND attained observation kernel. -/
theorem nativeGK4AIComparisonExists
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :
    NativeGK4TComparisonExists
      (nativeGK4AIP92Family p D E) first last := by
  exact (nativeGK4TComparisonExists_iff_seam
    (nativeGK4AIP92Family p D E) first last).mpr
      (nativeGK4AISeamInvariant first last)

#print axioms nativeGK4AICombine_assoc
#print axioms nativeGK4AICombine_leftUnit
#print axioms nativeGK4AICombine_rightUnit
#print axioms nativeGK4AIMatrixP92_compose
#print axioms nativeGK4AIP92
#print axioms nativeGK4AIStructural
#print axioms nativeGK4AI_commutes
#print axioms nativeGK4AIP92_compose
#print axioms nativeGK4AIStructural_compose
#print axioms nativeGK4AILaws
#print axioms nativeGK4AISeamInvariant
#print axioms nativeGK4AIComparisonExists

end
end Kuu.F112.Physical
