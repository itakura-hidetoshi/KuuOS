import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4ARStrictDiagonalSlice
import Mathlib.Tactic

/-!
F112-P94D3GK4AS — the lower-right entry of the TRUE second
integer matrix is FORCED modulo 16 by the already proved GK4AR data:
  d = 1 + 4*((charge+backwardCount)*backwardCount
             - orderedMoment - triangle(backwardCount)) + 16*t.
This is a determinant consequence, NOT a further independent
arithmetic obstruction. The exact trace has the derived residue
  a+d = 2 + 4*(charge+backwardCount)*backwardCount + 16*t.
Give an explicit integer witness from the old AO determinant-one,
AP upper-right mod4, AQ lower-left mod16, AR upper-left mod16
witnesses, rather than assuming an unverified modular API.

Inherit the already certified original F54 Type-valued five route
constructors, genuine P92B Q, independently generated structural S,
K_AI and every fixed old q fiber. The newly defined AS slice is
PROVED EQUAL to AR, never claimed to be strictly narrower. No
new Type-valued cell, Q category laws, fixed infinite fiber,
arithmetic surjectivity, Gray, global strict or hyperdescent.
Append-only/tighten-only/same-root107; #1558 Draft/OPEN/unmerged.
Pinned Lean v4.30.0-rc2 and mathlib
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

/-- The forced lower-right residue uses only the OLD GK4AD observer. -/
def nativeGK4ASOldLowerDiagonalResidue (v : NativeGK4ADValue) : Int :=
  nativeGK4APOldUpperResidue v * (v.1.2 : Int) -
    nativeGK4AROldDiagonalResidue v

/-- The essential algebraic result. Explicitly derive d mod16 from
det=1 and previous three entry residues, preserving every old
condition. This is valid for any integer 2x2 matrix satisfying AR,
whether or not that matrix is actually attained by an F54 route. -/
theorem nativeGK4ASRightDiagonal_forced
    (v : NativeGK4ADValue) (M : NativeGK4AHMatrix)
    (h : nativeGK4ARDiagonalLinked v M) :
    ∃ t : Int,
      M.2.2 = 1 + 4 * nativeGK4ASOldLowerDiagonalResidue v +
        16 * t := by
  rcases h.1.1.1 with ⟨hdet, _, _, ⟨w, hd⟩⟩
  rcases h.1.1.2 with ⟨y, hb⟩
  rcases h.1.2 with ⟨z, hc⟩
  rcases h.2 with ⟨x, ha⟩
  let rho : Int := nativeGK4APOldUpperResidue v
  let beta : Int := (v.1.2 : Int)
  let s : Int := nativeGK4AROldDiagonalResidue v
  let t : Int :=
    -x - s * w - 4 * x * w + rho * z + y * beta + 4 * y * z
  have hdet' :
      (1 + 4 * s + 16 * x) * (1 + 4 * w) -
        (rho + 4 * y) * (4 * beta + 16 * z) = 1 := by
    change M.1.1 * M.2.2 - M.1.2 * M.2.1 = 1 at hdet
    rw [ha, hd, hb, hc] at hdet
    exact hdet
  have hfactor :
      4 * (w - (rho * beta - s) - 4 * t) = 0 := by
    calc
      4 * (w - (rho * beta - s) - 4 * t) =
          (1 + 4 * s + 16 * x) * (1 + 4 * w) -
            (rho + 4 * y) * (4 * beta + 16 * z) - 1 := by
              dsimp [t]
              ring
      _ = 0 := by rw [hdet']; ring
  have hw : w = rho * beta - s + 4 * t := by omega
  refine ⟨t, ?_⟩
  change M.2.2 = 1 + 4 * (rho * beta - s) + 16 * t
  calc
    M.2.2 = 1 + 4 * w := hd
    _ = 1 + 4 * (rho * beta - s) + 16 * t := by
      rw [hw]
      ring

/-- A convenient joint predicate for the AS statement.
Its AR component is deliberately retained in full. -/
def nativeGK4ASDiagonalLinked
    (v : NativeGK4ADValue) (M : NativeGK4AHMatrix) : Prop :=
  nativeGK4ARDiagonalLinked v M ∧
    ∃ t : Int,
      M.2.2 = 1 + 4 * nativeGK4ASOldLowerDiagonalResidue v +
        16 * t

/-- AS adds no independent restriction: the predicates are identical
as propositions, not merely equal on attained source paths. -/
theorem nativeGK4ASDiagonalLinked_iff_AR
    (v : NativeGK4ADValue) (M : NativeGK4AHMatrix) :
    nativeGK4ASDiagonalLinked v M ↔ nativeGK4ARDiagonalLinked v M := by
  constructor
  · intro h
    exact h.1
  · intro h
    exact ⟨h, nativeGK4ASRightDiagonal_forced v M h⟩

/-- Exact multiplicative compatibility is inherited from genuine
noncommutative AD observer combination and AH matrix multiplication. -/
theorem nativeGK4ASDiagonalLinked_mul
    (u v : NativeGK4ADValue) (A B : NativeGK4AHMatrix)
    (hu : nativeGK4ASDiagonalLinked u A)
    (hv : nativeGK4ASDiagonalLinked v B) :
    nativeGK4ASDiagonalLinked (nativeGK4ADCombine u v)
      (nativeGK4AHMul A B) := by
  apply (nativeGK4ASDiagonalLinked_iff_AR _ _).2
  exact nativeGK4ARDiagonalLinked_mul u v A B hu.1 hv.1

/-- The trace mod16 loses the orderedMoment term by cancellation.
It depends on the OLD charge and backwardCount only. -/
theorem nativeGK4ASTrace_forced
    (v : NativeGK4ADValue) (M : NativeGK4AHMatrix)
    (h : nativeGK4ARDiagonalLinked v M) :
    ∃ t : Int,
      M.1.1 + M.2.2 =
        2 + 4 * (nativeGK4APOldUpperResidue v * (v.1.2 : Int)) +
          16 * t := by
  rcases h.2 with ⟨ta, ha⟩
  rcases nativeGK4ASRightDiagonal_forced v M h with ⟨td, hd⟩
  refine ⟨ta + td, ?_⟩
  rw [ha, hd]
  dsimp [nativeGK4ASOldLowerDiagonalResidue]
  ring

section GenuineOriginalDependentSource
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}

/-- An actual forward or backward Type-valued F54 rotation edge. -/
theorem nativeGK4ASEdge_sound
    {n m : Nat}
    {before after : KuuNativeF45Tree p n m ma pa mb pb}
    (edge : KuuNativeF45Tree.RotationEdge p before after) :
    nativeGK4ASDiagonalLinked edge.gk4adValue edge.gk4ahMatrix :=
  (nativeGK4ASDiagonalLinked_iff_AR _ _).2
    (nativeGK4AREdge_sound edge)

/-- An original intermediate-tree-dependent rotation chain. -/
theorem nativeGK4ASChain_sound
    {n m : Nat}
    {before after : KuuNativeF45Tree p n m ma pa mb pb}
    (chain : KuuNativeF45Tree.RotationChain p before after) :
    nativeGK4ASDiagonalLinked chain.gk4adValue chain.gk4ahMatrix :=
  (nativeGK4ASDiagonalLinked_iff_AR _ _).2
    (nativeGK4ARChain_sound chain)

/-- Every original F54 route constructor (chain/cast/trans/left/right)
is covered by the already proved full GK4AR source theorem. -/
theorem nativeGK4ASRoute_sound
    {n n' m m' : Nat}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (route : KuuNativeF45Tree.DepthRotationRoute p first last) :
    nativeGK4ASDiagonalLinked route.gk4adValue route.gk4ahMatrix :=
  (nativeGK4ASDiagonalLinked_iff_AR _ _).2
    (nativeGK4ARRoute_sound route)
end GenuineOriginalDependentSource

section GenuineQuotientsAndFibers
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable {n n' m m' : Nat}
variable (first : KuuNativeF45Tree p n m ma pa mb pb)
variable (last : KuuNativeF45Tree p n' m' ma pa mb pb)

/-- Original P92B Q quotient with preexisting actual F55/P92B cells. -/
theorem nativeGK4ASP92_sound
    (q : NativeF55P92AssocRouteClasses first last) :
    nativeGK4ASDiagonalLinked (nativeGK4ADP92Value first last q)
      (nativeGK4AHP92Value first last q) :=
  (nativeGK4ASDiagonalLinked_iff_AR _ _).2
    (nativeGK4ARP92_sound first last q)

/-- Independently presented structural S, preserving its own seams. -/
theorem nativeGK4ASStructural_sound
    (s : NativeGK4EStructuralRouteClasses first last) :
    nativeGK4ASDiagonalLinked (nativeGK4ADStructuralValue first last s)
      (nativeGK4AHStructuralValue first last s) :=
  (nativeGK4ASDiagonalLinked_iff_AR _ _).2
    (nativeGK4ARStructural_sound first last s)

/-- Genuine K_AI kernel observer, not an arbitrary arithmetic matrix. -/
theorem nativeGK4ASKernel_sound
    (z : NativeGK4SKernelClasses (nativeGK4AIP92Family p D E) first last) :
    nativeGK4ASDiagonalLinked
      ((nativeGK4AIKernelValue first last z).1.1.2)
      ((nativeGK4AIKernelValue first last z).2) :=
  (nativeGK4ASDiagonalLinked_iff_AR _ _).2
    (nativeGK4ARKernel_sound first last z)

/-- Every original old K_AG fixed-q fiber inherits both diagonals. -/
theorem nativeGK4ASFiber_sound
    (target : NativeGK4SKernelClasses
      (nativeGK4AGP92Family p D E) first last)
    (z : nativeGK4AJOldFiber first last target) :
    nativeGK4ASDiagonalLinked
      ((nativeGK4AGKernelValue first last target).1.2)
      (nativeGK4AJFiberMatrix first last target z) :=
  (nativeGK4ASDiagonalLinked_iff_AR _ _).2
    (nativeGK4ARFiber_sound first last target z)

/-- The forced right-diagonal arithmetic slice for a fixed OLD q. -/
def nativeGK4ASFiberArithmeticSlice
    (target : NativeGK4SKernelClasses
      (nativeGK4AGP92Family p D E) first last) : Set NativeGK4AHMatrix :=
  {M | nativeGK4ASDiagonalLinked
    ((nativeGK4AGKernelValue first last target).1.2) M}

/-- The AS slice is EQUAL to AR, not strictly smaller. No new
arithmetical unattainability is fabricated at this step. -/
theorem nativeGK4ASSlice_eq_AR
    (target : NativeGK4SKernelClasses
      (nativeGK4AGP92Family p D E) first last) :
    nativeGK4ASFiberArithmeticSlice first last target =
      nativeGK4ARFiberArithmeticSlice first last target := by
  ext M
  exact nativeGK4ASDiagonalLinked_iff_AR _ _

/-- All actually attained second matrices belong to the same AS/AR
slice; the other direction is NOT established. -/
theorem nativeGK4ASAttained_subset_slice
    (target : NativeGK4SKernelClasses
      (nativeGK4AGP92Family p D E) first last) :
    nativeGK4ALAttainedMatrixSet first last target ⊆
      nativeGK4ASFiberArithmeticSlice first last target := by
  intro M h
  rcases h with ⟨z, rfl⟩
  exact nativeGK4ASFiber_sound first last target z

/-- In the same old q-fiber even the lower-right diagonal residue
is common to any two actual K_AI points. -/
theorem nativeGK4ASSameFiber_lowerDiagonal_residue
    (target : NativeGK4SKernelClasses
      (nativeGK4AGP92Family p D E) first last)
    (x y : nativeGK4AJOldFiber first last target) :
    ∃ t : Int,
      (nativeGK4AJFiberMatrix first last target x).2.2 =
        (nativeGK4AJFiberMatrix first last target y).2.2 +
          16 * t := by
  rcases (nativeGK4ASFiber_sound first last target x).2 with ⟨tx, hx⟩
  rcases (nativeGK4ASFiber_sound first last target y).2 with ⟨ty, hy⟩
  refine ⟨tx - ty, ?_⟩
  rw [hx, hy]
  ring

/-- Previously PROVED strict AR vs AQ relationship still applies,
without falsely asserting a new AS vs AR strictness. -/
theorem nativeGK4ASStrictInsideAQ
    (target : NativeGK4SKernelClasses
      (nativeGK4AGP92Family p D E) first last) :
    nativeGK4ASFiberArithmeticSlice first last target ⊆
      nativeGK4AQFiberArithmeticSlice first last target ∧
    ∃ M : NativeGK4AHMatrix,
      M ∈ nativeGK4AQFiberArithmeticSlice first last target ∧
      M ∉ nativeGK4ASFiberArithmeticSlice first last target := by
  rw [nativeGK4ASSlice_eq_AR]
  exact nativeGK4ARStrictInsideAQ first last target

end GenuineQuotientsAndFibers

#print axioms nativeGK4ASOldLowerDiagonalResidue
#print axioms nativeGK4ASRightDiagonal_forced
#print axioms nativeGK4ASDiagonalLinked
#print axioms nativeGK4ASDiagonalLinked_iff_AR
#print axioms nativeGK4ASDiagonalLinked_mul
#print axioms nativeGK4ASTrace_forced
#print axioms nativeGK4ASEdge_sound
#print axioms nativeGK4ASChain_sound
#print axioms nativeGK4ASRoute_sound
#print axioms nativeGK4ASP92_sound
#print axioms nativeGK4ASStructural_sound
#print axioms nativeGK4ASKernel_sound
#print axioms nativeGK4ASFiber_sound
#print axioms nativeGK4ASFiberArithmeticSlice
#print axioms nativeGK4ASSlice_eq_AR
#print axioms nativeGK4ASAttained_subset_slice
#print axioms nativeGK4ASSameFiber_lowerDiagonal_residue
#print axioms nativeGK4ASStrictInsideAQ

end
end Kuu.F112.Physical
