import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5BYIntPolynomialCRTNaturality
import Mathlib.Algebra.MvPolynomial.Eval
import Mathlib.Algebra.MvPolynomial.Basic
import Mathlib.Tactic

/-!
F112-P94D3GK5BZ — GENUINE MULTIVARIABLE INTEGER POLYNOMIAL CRT NATURALITY.

The original complete finite noncoprime CRT RingEquiv (GK5BW),
finite-cover RingHom restriction identity/composition/tower
coherence (GK5BX), and one-variable integer polynomial
naturality (GK5BY) are extended to ACTUAL
  MvPolynomial σ Int
for arbitrary variable types σ, including genuine Fin n
families and the empty set of variables.

At each arbitrary finite original cover of Nat moduli,
define an evaluation RING HOM from MvPolynomial σ Int
into the real global ZMod L and its true gcd-compatible
local ZMod dependent-product SUBRING. Show preservation
of additions and products, coordinate-variable maps,
natural equality of RingHom under restriction in both
global and local rings, and the naturality square of
the true GK5BW CRT RingEquiv. The genuine three-cover
tower of compatible-local and global evaluations
commutes, including the finite-variable case.

We never require pairwise coprimality, positivity, nonzero
moduli, a dominating site, or a nonempty cover; ZMod 0=Int
and empty covers remain included. Original signed integer
assignments are not replaced by natAbs observations.

This is precisely NUMERIC ring-level descent. It does not
manufacture an original F55 Type source, P77 class identity,
P94A four-cells, unconditional P89 reflection, universal
GK5AY seam, or W=1→seam. Strict 空, independent Kuu→Qi,
genuine F54 two Nat/two categories/Blocks and original
F55 Type source history unchanged. Public root107; protected
validation-only PR #1558 remains Draft/open/unmerged.
Lean v4.30.0-rc2 and mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6 pinned.
No axioms, sorry/admit/native_decide, Gray or GK5BA kit.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

/-- A genuine MULTIVARIABLE integer polynomial evaluation
RING HOM into the global LCM residue ring. -/
def nativeGK5BZGlobalMvEvalHom
    {ι σ : Type*} (s : Finset ι) (moduli : ι → Nat)
    (xs : σ → ZMod (nativeGK5BUFiniteModulus s moduli)) :
    MvPolynomial σ Int →+* ZMod (nativeGK5BUFiniteModulus s moduli) :=
  MvPolynomial.eval₂Hom
    (Int.castRingHom (ZMod (nativeGK5BUFiniteModulus s moduli))) xs

/-- An actual MULTIVARIABLE integer polynomial evaluation
RING HOM into the compatible-local dependent-product SUBRING. -/
def nativeGK5BZCompatibleMvEvalHom
    {ι σ : Type*} (s : Finset ι) (moduli : ι → Nat)
    (as : σ → nativeGK5BWCompatibleSubring s moduli) :
    MvPolynomial σ Int →+* nativeGK5BWCompatibleSubring s moduli :=
  MvPolynomial.eval₂Hom
    (Int.castRingHom (nativeGK5BWCompatibleSubring s moduli)) as

/-- Genuine global ZMod multivariable polynomial evaluation
preserves addition of ACTUAL integer polynomials. -/
theorem nativeGK5BZGlobalMvEval_add
    {ι σ : Type*} (s : Finset ι) (moduli : ι → Nat)
    (xs : σ → ZMod (nativeGK5BUFiniteModulus s moduli))
    (P Q : MvPolynomial σ Int) :
    nativeGK5BZGlobalMvEvalHom s moduli xs (P + Q) =
      nativeGK5BZGlobalMvEvalHom s moduli xs P +
        nativeGK5BZGlobalMvEvalHom s moduli xs Q :=
  (nativeGK5BZGlobalMvEvalHom s moduli xs).map_add P Q

/-- Genuine global multivariable evaluation preserves
multiplication, even with ZMod 0 and negative coefficients. -/
theorem nativeGK5BZGlobalMvEval_mul
    {ι σ : Type*} (s : Finset ι) (moduli : ι → Nat)
    (xs : σ → ZMod (nativeGK5BUFiniteModulus s moduli))
    (P Q : MvPolynomial σ Int) :
    nativeGK5BZGlobalMvEvalHom s moduli xs (P * Q) =
      nativeGK5BZGlobalMvEvalHom s moduli xs P *
        nativeGK5BZGlobalMvEvalHom s moduli xs Q :=
  (nativeGK5BZGlobalMvEvalHom s moduli xs).map_mul P Q

/-- Genuine compatible-local subring multivariable
evaluation preserves addition of original polynomials. -/
theorem nativeGK5BZCompatibleMvEval_add
    {ι σ : Type*} (s : Finset ι) (moduli : ι → Nat)
    (as : σ → nativeGK5BWCompatibleSubring s moduli)
    (P Q : MvPolynomial σ Int) :
    nativeGK5BZCompatibleMvEvalHom s moduli as (P + Q) =
      nativeGK5BZCompatibleMvEvalHom s moduli as P +
        nativeGK5BZCompatibleMvEvalHom s moduli as Q :=
  (nativeGK5BZCompatibleMvEvalHom s moduli as).map_add P Q

/-- Genuine compatible-local subring multivariable
evaluation preserves multiplication. -/
theorem nativeGK5BZCompatibleMvEval_mul
    {ι σ : Type*} (s : Finset ι) (moduli : ι → Nat)
    (as : σ → nativeGK5BWCompatibleSubring s moduli)
    (P Q : MvPolynomial σ Int) :
    nativeGK5BZCompatibleMvEvalHom s moduli as (P * Q) =
      nativeGK5BZCompatibleMvEvalHom s moduli as P *
        nativeGK5BZCompatibleMvEvalHom s moduli as Q :=
  (nativeGK5BZCompatibleMvEvalHom s moduli as).map_mul P Q

/-- The actual global finite CRT evaluation respects EVERY
finite-cover inclusion AS AN EQUALITY OF RING HOMOMORPHISMS
from the full multivariable polynomial ring. -/
theorem nativeGK5BZGlobalMvEval_restrictHom
    {ι σ : Type*} (s t : Finset ι) (moduli : ι → Nat)
    (h : t ⊆ s)
    (xs : σ → ZMod (nativeGK5BUFiniteModulus s moduli)) :
    (nativeGK5BXGlobalRestrictHom s t moduli h).comp
      (nativeGK5BZGlobalMvEvalHom s moduli xs) =
    nativeGK5BZGlobalMvEvalHom t moduli
      (fun v => nativeGK5BXGlobalRestrictHom s t moduli h (xs v)) := by
  apply MvPolynomial.ringHom_ext
  · intro z
    change (nativeGK5BXGlobalRestrictHom s t moduli h)
      (z : ZMod (nativeGK5BUFiniteModulus s moduli)) =
      (z : ZMod (nativeGK5BUFiniteModulus t moduli))
    exact map_intCast (nativeGK5BXGlobalRestrictHom s t moduli h) z
  · intro v
    rfl

/-- The true local compatible CRT evaluation respects
all finite-cover restrictions AS RING HOMOMORPHISM EQUALITY
for arbitrary MvPolynomial σ Int. -/
theorem nativeGK5BZCompatibleMvEval_restrictHom
    {ι σ : Type*} (s t : Finset ι) (moduli : ι → Nat)
    (h : t ⊆ s)
    (as : σ → nativeGK5BWCompatibleSubring s moduli) :
    (nativeGK5BXCompatibleRestrictHom s t moduli h).comp
      (nativeGK5BZCompatibleMvEvalHom s moduli as) =
    nativeGK5BZCompatibleMvEvalHom t moduli
      (fun v => nativeGK5BXCompatibleRestrictHom s t moduli h (as v)) := by
  apply MvPolynomial.ringHom_ext
  · intro z
    change (nativeGK5BXCompatibleRestrictHom s t moduli h)
      (z : nativeGK5BWCompatibleSubring s moduli) =
      (z : nativeGK5BWCompatibleSubring t moduli)
    exact map_intCast (nativeGK5BXCompatibleRestrictHom s t moduli h) z
  · intro v
    rfl

/-- The genuine complete finite noncoprime CRT ring
homomorphism commutes with ALL multivariable integer
polynomial evaluations AS AN EQUALITY OF RING HOMS. -/
theorem nativeGK5BZCRTMvEval_naturalHom
    {ι σ : Type*} (s : Finset ι) (moduli : ι → Nat)
    (xs : σ → ZMod (nativeGK5BUFiniteModulus s moduli)) :
    (nativeGK5BWGlobalCompatibleHom s moduli).comp
      (nativeGK5BZGlobalMvEvalHom s moduli xs) =
    nativeGK5BZCompatibleMvEvalHom s moduli
      (fun v => nativeGK5BWGlobalCompatibleHom s moduli (xs v)) := by
  apply MvPolynomial.ringHom_ext
  · intro z
    change (nativeGK5BWGlobalCompatibleHom s moduli)
      (z : ZMod (nativeGK5BUFiniteModulus s moduli)) =
      (z : nativeGK5BWCompatibleSubring s moduli)
    exact map_intCast (nativeGK5BWGlobalCompatibleHom s moduli) z
  · intro v
    rfl

/-- Pointwise genuine global multivariable evaluation
naturality: one finite restriction, any polynomial. -/
theorem nativeGK5BZGlobalMvEval_restrict
    {ι σ : Type*} (s t : Finset ι) (moduli : ι → Nat)
    (h : t ⊆ s)
    (xs : σ → ZMod (nativeGK5BUFiniteModulus s moduli))
    (P : MvPolynomial σ Int) :
    nativeGK5BXGlobalRestrictHom s t moduli h
      (nativeGK5BZGlobalMvEvalHom s moduli xs P) =
    nativeGK5BZGlobalMvEvalHom t moduli
      (fun v => nativeGK5BXGlobalRestrictHom s t moduli h (xs v)) P := by
  simpa only [RingHom.comp_apply] using
    (RingHom.congr_fun (nativeGK5BZGlobalMvEval_restrictHom
      s t moduli h xs) P)

/-- Pointwise true compatible-local multivariable evaluation
naturality under finite-cover restriction. -/
theorem nativeGK5BZCompatibleMvEval_restrict
    {ι σ : Type*} (s t : Finset ι) (moduli : ι → Nat)
    (h : t ⊆ s)
    (as : σ → nativeGK5BWCompatibleSubring s moduli)
    (P : MvPolynomial σ Int) :
    nativeGK5BXCompatibleRestrictHom s t moduli h
      (nativeGK5BZCompatibleMvEvalHom s moduli as P) =
    nativeGK5BZCompatibleMvEvalHom t moduli
      (fun v => nativeGK5BXCompatibleRestrictHom s t moduli h (as v)) P := by
  simpa only [RingHom.comp_apply] using
    (RingHom.congr_fun (nativeGK5BZCompatibleMvEval_restrictHom
      s t moduli h as) P)

/-- Genuine CRT RingEquiv evaluation is natural for EVERY
multivariable integer polynomial, including zero moduli. -/
theorem nativeGK5BZCRTMvEval_apply
    {ι σ : Type*} (s : Finset ι) (moduli : ι → Nat)
    (xs : σ → ZMod (nativeGK5BUFiniteModulus s moduli))
    (P : MvPolynomial σ Int) :
    nativeGK5BWFiniteCRTRingEquiv s moduli
      (nativeGK5BZGlobalMvEvalHom s moduli xs P) =
    nativeGK5BZCompatibleMvEvalHom s moduli
      (fun v => nativeGK5BWFiniteCRTRingEquiv s moduli (xs v)) P := by
  simpa only [RingHom.comp_apply, nativeGK5BWFiniteCRTRingEquiv_apply]
    using (RingHom.congr_fun
      (nativeGK5BZCRTMvEval_naturalHom s moduli xs) P)

/-- Finite-variable form: all n integer polynomial
variables commute with the TRUE CRT RingEquiv. -/
theorem nativeGK5BZFinVariableCRT_natural
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (n : Nat)
    (xs : Fin n → ZMod (nativeGK5BUFiniteModulus s moduli))
    (P : MvPolynomial (Fin n) Int) :
    nativeGK5BWFiniteCRTRingEquiv s moduli
      (nativeGK5BZGlobalMvEvalHom s moduli xs P) =
    nativeGK5BZCompatibleMvEvalHom s moduli
      (fun v => nativeGK5BWFiniteCRTRingEquiv s moduli (xs v)) P :=
  nativeGK5BZCRTMvEval_apply s moduli xs P

/-- Multivariable integer polynomial evaluation commutes
with the full TWO-STEP global ZMod restriction tower,
and the direct smallest-cover evaluation, as a RING HOM. -/
theorem nativeGK5BZGlobalMvEval_towerHom
    {ι σ : Type*} (s t u : Finset ι) (moduli : ι → Nat)
    (h : t ⊆ s) (k : u ⊆ t)
    (xs : σ → ZMod (nativeGK5BUFiniteModulus s moduli)) :
    ((nativeGK5BXGlobalRestrictHom t u moduli k).comp
      (nativeGK5BXGlobalRestrictHom s t moduli h)).comp
      (nativeGK5BZGlobalMvEvalHom s moduli xs) =
    nativeGK5BZGlobalMvEvalHom u moduli
      (fun v => nativeGK5BXGlobalRestrictHom s u moduli
        (fun i hi => h (k hi)) (xs v)) := by
  apply MvPolynomial.ringHom_ext
  · intro z
    simp only [RingHom.comp_apply, MvPolynomial.eval₂Hom_C]
    exact map_intCast
      ((nativeGK5BXGlobalRestrictHom t u moduli k).comp
        (nativeGK5BXGlobalRestrictHom s t moduli h)) z
  · intro v
    change nativeGK5BXGlobalRestrictHom t u moduli k
      (nativeGK5BXGlobalRestrictHom s t moduli h (xs v)) =
      nativeGK5BXGlobalRestrictHom s u moduli
        (fun i hi => h (k hi)) (xs v)
    simpa only [RingHom.comp_apply] using
      (RingHom.congr_fun
        (nativeGK5BXGlobalRestrict_comp s t u moduli h k) (xs v))

/-- The compatible-local multivariable integer polynomial
evaluation also commutes with the full three-cover tower,
as an EQUALITY OF RING HOMOMORPHISMS. -/
theorem nativeGK5BZCompatibleMvEval_towerHom
    {ι σ : Type*} (s t u : Finset ι) (moduli : ι → Nat)
    (h : t ⊆ s) (k : u ⊆ t)
    (as : σ → nativeGK5BWCompatibleSubring s moduli) :
    ((nativeGK5BXCompatibleRestrictHom t u moduli k).comp
      (nativeGK5BXCompatibleRestrictHom s t moduli h)).comp
      (nativeGK5BZCompatibleMvEvalHom s moduli as) =
    nativeGK5BZCompatibleMvEvalHom u moduli
      (fun v => nativeGK5BXCompatibleRestrictHom s u moduli
        (fun i hi => h (k hi)) (as v)) := by
  apply MvPolynomial.ringHom_ext
  · intro z
    simp only [RingHom.comp_apply, MvPolynomial.eval₂Hom_C]
    exact map_intCast
      ((nativeGK5BXCompatibleRestrictHom t u moduli k).comp
        (nativeGK5BXCompatibleRestrictHom s t moduli h)) z
  · intro v
    change nativeGK5BXCompatibleRestrictHom t u moduli k
      (nativeGK5BXCompatibleRestrictHom s t moduli h (as v)) =
      nativeGK5BXCompatibleRestrictHom s u moduli
        (fun i hi => h (k hi)) (as v)
    simpa only [RingHom.comp_apply] using
      (RingHom.congr_fun
        (nativeGK5BXCompatibleRestrict_comp s t u moduli h k) (as v))

/-- The ORIGINAL signed integer assignment to all variables
can be evaluated in the integer ring BEFORE passage to
any actual global finite CRT quotient, with the same result. -/
theorem nativeGK5BZSignedIntMvEval_global
    {ι σ : Type*} (s : Finset ι) (moduli : ι → Nat)
    (zs : σ → Int) (P : MvPolynomial σ Int) :
    nativeGK5BZGlobalMvEvalHom s moduli
      (fun v => (zs v : ZMod (nativeGK5BUFiniteModulus s moduli))) P =
    ((MvPolynomial.eval₂Hom (Int.castRingHom Int) zs P : Int) :
      ZMod (nativeGK5BUFiniteModulus s moduli)) := by
  have heq :
      nativeGK5BZGlobalMvEvalHom s moduli
        (fun v => (zs v : ZMod (nativeGK5BUFiniteModulus s moduli))) =
      (Int.castRingHom (ZMod (nativeGK5BUFiniteModulus s moduli))).comp
        (MvPolynomial.eval₂Hom (Int.castRingHom Int) zs) := by
    apply MvPolynomial.ringHom_ext
    · intro z
      simp [nativeGK5BZGlobalMvEvalHom]
    · intro v
      simp [nativeGK5BZGlobalMvEvalHom]
  simpa only [RingHom.comp_apply] using
    (RingHom.congr_fun heq P)

/-- A complete three-cover CRT diagram of multivariable
polynomial evaluation is strictly commutative: evaluate
globally then glue and restrict twice, or restrict each
variable directly and evaluate in the smallest cover. -/
theorem nativeGK5BZMultivariableCRTTower_natural
    {ι σ : Type*} (s t u : Finset ι) (moduli : ι → Nat)
    (h : t ⊆ s) (k : u ⊆ t)
    (xs : σ → ZMod (nativeGK5BUFiniteModulus s moduli))
    (P : MvPolynomial σ Int) :
    nativeGK5BXCompatibleRestrictHom t u moduli k
      (nativeGK5BXCompatibleRestrictHom s t moduli h
        (nativeGK5BWFiniteCRTRingEquiv s moduli
          (nativeGK5BZGlobalMvEvalHom s moduli xs P))) =
    nativeGK5BWFiniteCRTRingEquiv u moduli
      (nativeGK5BZGlobalMvEvalHom u moduli
        (fun v => nativeGK5BXGlobalRestrictHom s u moduli
          (fun i hi => h (k hi)) (xs v)) P) := by
  have hcomp := congrArg
    (fun f : ZMod (nativeGK5BUFiniteModulus s moduli) →+*
      ZMod (nativeGK5BUFiniteModulus u moduli) =>
        f (nativeGK5BZGlobalMvEvalHom s moduli xs P))
    (nativeGK5BXGlobalRestrict_comp s t u moduli h k)
  calc
    _ = nativeGK5BWFiniteCRTRingEquiv u moduli
          (nativeGK5BXGlobalRestrictHom t u moduli k
            (nativeGK5BXGlobalRestrictHom s t moduli h
              (nativeGK5BZGlobalMvEvalHom s moduli xs P))) := by
        rw [← nativeGK5BXCRTNaturality_apply s t moduli h
          (nativeGK5BZGlobalMvEvalHom s moduli xs P)]
        rw [← nativeGK5BXCRTNaturality_apply t u moduli k
          (nativeGK5BXGlobalRestrictHom s t moduli h
            (nativeGK5BZGlobalMvEvalHom s moduli xs P))]
    _ = nativeGK5BWFiniteCRTRingEquiv u moduli
          (nativeGK5BXGlobalRestrictHom s u moduli
            (fun i hi => h (k hi))
              (nativeGK5BZGlobalMvEvalHom s moduli xs P)) := by
        congr 1
        simpa only [RingHom.comp_apply] using hcomp
    _ = _ := by
        congr 1
        simpa only [RingHom.comp_apply] using
          (RingHom.congr_fun
            (nativeGK5BZGlobalMvEval_restrictHom s u moduli
              (fun i hi => h (k hi)) xs) P)

#print axioms nativeGK5BZGlobalMvEval_add
#print axioms nativeGK5BZGlobalMvEval_mul
#print axioms nativeGK5BZCompatibleMvEval_add
#print axioms nativeGK5BZCompatibleMvEval_mul
#print axioms nativeGK5BZGlobalMvEval_restrictHom
#print axioms nativeGK5BZCompatibleMvEval_restrictHom
#print axioms nativeGK5BZCRTMvEval_naturalHom
#print axioms nativeGK5BZGlobalMvEval_restrict
#print axioms nativeGK5BZCompatibleMvEval_restrict
#print axioms nativeGK5BZCRTMvEval_apply
#print axioms nativeGK5BZFinVariableCRT_natural
#print axioms nativeGK5BZGlobalMvEval_towerHom
#print axioms nativeGK5BZCompatibleMvEval_towerHom
#print axioms nativeGK5BZSignedIntMvEval_global
#print axioms nativeGK5BZMultivariableCRTTower_natural

end
end Kuu.F112.Physical
