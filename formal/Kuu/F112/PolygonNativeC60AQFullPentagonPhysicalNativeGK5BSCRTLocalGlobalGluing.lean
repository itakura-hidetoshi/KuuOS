import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5BRPrimePowerLocalGlobal
import Mathlib.Data.ZMod.QuotientRing
import Mathlib.Tactic

/-!
F112-P94D3GK5BS — GENUINE PRIME-POWER CRT LOCAL / GLOBAL GLUING.

From GK5BR's actual finite prime-power factors of d! and
GK5BQ's genuine raw integer numerators, construct the
UNCONDITIONAL pinned Mathlib CRT ring equivalence
ZMod(d!) ≃+* Π p∈primeFactors(d!), ZMod(p^v_p(d!)).
For ARBITRARY independently specified residues residues, build
a global residue, prove each residues projection, uniqueness,
an integer representative, its exact congruence class, and
additive / multiplicative compatibility.

For original raw integer observations, the CRT glue of
their genuine residues numerator residues equals the cast
of the genuine GK5BQ numerator, not a new invented value.
The CRT glue vanishes iff the exact coefficient factorial
divisibility certificate holds; reconstruct Int[X] Newton
and GK5BL Lagrange sources iff all finite CRT glues vanish.

This is ARITHMETIC descent only. It constructs no original
F55 Type history, P77 class equality, P94A four-cell,
original-phi seam, universal GK5AY seam, or unconditional P89
reflection. Strict 空; independent Kuu→Qi. Original F54
two Nat/two categories/Blocks and F55 Type history retained.
Public root107 append-only, protected #1558 Draft/open.
Pinned Lean v4.30.0-rc2, mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
No new axioms, sorry/admit/native_decide.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
open Finset
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

/-- The genuine family of independently specified residues
residue rings at ACTUAL maximal prime powers of d!. -/
abbrev nativeGK5BSFactorialLocalFamily (d : Nat) : Type :=
  ∀ p : (d.factorial).primeFactors,
    ZMod ((p : Nat) ^ ((d.factorial).factorization (p : Nat)))

/-- Pinned mathlib's ACTUAL Chinese remainder ring
equivalence, not a merely posited bijection or oracle.
The zero/one factorial cases have an empty residues family. -/
def nativeGK5BSFactorialCRTRingEquiv (d : Nat) :
    ZMod d.factorial ≃+* nativeGK5BSFactorialLocalFamily d :=
  ZMod.equivPi d.factorial (Nat.factorial_ne_zero d)

/-- Glue an ARBITRARY family of prime-power residue values
to its unique global residue class modulo the true d!. -/
def nativeGK5BSCRTGlue
    (d : Nat) (residues : nativeGK5BSFactorialLocalFamily d) :
    ZMod d.factorial :=
  (nativeGK5BSFactorialCRTRingEquiv d).symm residues

/-- Every separately chosen residues residue is recovered
EXACTLY from the single glued global residue class. -/
theorem nativeGK5BSCRTGlue_local
    (d : Nat) (residues : nativeGK5BSFactorialLocalFamily d)
    (p : (d.factorial).primeFactors) :
    (nativeGK5BSFactorialCRTRingEquiv d)
      (nativeGK5BSCRTGlue d residues) p = residues p := by
  exact congrFun
    ((nativeGK5BSFactorialCRTRingEquiv d).apply_symm_apply residues) p

/-- Any global residue with all the prescribed residues
projections is equal to the canonical glued residue. -/
theorem nativeGK5BSCRTGlue_unique
    (d : Nat) (residues : nativeGK5BSFactorialLocalFamily d)
    (z : ZMod d.factorial) :
    (∀ p : (d.factorial).primeFactors,
      (nativeGK5BSFactorialCRTRingEquiv d) z p = residues p) ↔
      z = nativeGK5BSCRTGlue d residues := by
  constructor
  · intro h
    apply (nativeGK5BSFactorialCRTRingEquiv d).injective
    funext p
    exact (h p).trans (nativeGK5BSCRTGlue_local d residues p).symm
  · intro h p
    rw [h]
    exact nativeGK5BSCRTGlue_local d residues p

/-- Actual pinned ring-equivalence naturality on ALL
integer casts: the global integer residue projects to
the SAME integer modulo each genuine residues prime power. -/
theorem nativeGK5BSFactorialCRT_intCast
    (d : Nat) (z : Int) (p : (d.factorial).primeFactors) :
    (nativeGK5BSFactorialCRTRingEquiv d)
      (z : ZMod d.factorial) p =
        (z : ZMod ((p : Nat) ^ ((d.factorial).factorization (p : Nat))) := by
  have h :
      (nativeGK5BSFactorialCRTRingEquiv d)
        (z : ZMod d.factorial) =
          (z : nativeGK5BSFactorialLocalFamily d) :=
    map_intCast (nativeGK5BSFactorialCRTRingEquiv d) z
  exact congrFun h p

/-- A genuine integer representative of the glued residue.
Uses the actual ZMod→Int cast, not an existence axiom. -/
def nativeGK5BSCRTGlueInt
    (d : Nat) (residues : nativeGK5BSFactorialLocalFamily d) : Int :=
  ZMod.cast (nativeGK5BSCRTGlue d residues)

/-- The constructed integer maps back to EXACTLY the
canonically glued global class modulo the true factorial. -/
theorem nativeGK5BSCRTGlueInt_cast
    (d : Nat) (residues : nativeGK5BSFactorialLocalFamily d) :
    (nativeGK5BSCRTGlueInt d residues : ZMod d.factorial) =
      nativeGK5BSCRTGlue d residues := by
  exact ZMod.intCast_zmod_cast _

/-- The constructed integer representative satisfies
EACH separately specified residues modular condition. -/
theorem nativeGK5BSCRTGlueInt_local
    (d : Nat) (residues : nativeGK5BSFactorialLocalFamily d)
    (p : (d.factorial).primeFactors) :
    (nativeGK5BSCRTGlueInt d residues :
      ZMod ((p : Nat) ^ ((d.factorial).factorization (p : Nat)))) =
        residues p := by
  calc
    (nativeGK5BSCRTGlueInt d residues :
      ZMod ((p : Nat) ^ ((d.factorial).factorization (p : Nat)))) =
      (nativeGK5BSFactorialCRTRingEquiv d)
        (nativeGK5BSCRTGlueInt d residues : ZMod d.factorial) p := by
          exact (nativeGK5BSFactorialCRT_intCast d
            (nativeGK5BSCRTGlueInt d residues) p).symm
    _ = (nativeGK5BSFactorialCRTRingEquiv d)
          (nativeGK5BSCRTGlue d residues) p := by
          rw [nativeGK5BSCRTGlueInt_cast]
    _ = residues p := nativeGK5BSCRTGlue_local d residues p

/-- All simultaneous modular solutions are exactly those
integers in the same global residue class modulo d!. -/
theorem nativeGK5BSCRTInt_compatible_iff_global
    (d : Nat) (residues : nativeGK5BSFactorialLocalFamily d)
    (z : Int) :
    (∀ p : (d.factorial).primeFactors,
      (z : ZMod ((p : Nat) ^ ((d.factorial).factorization (p : Nat)))) =
        residues p) ↔
      (z : ZMod d.factorial) = nativeGK5BSCRTGlue d residues := by
  constructor
  · intro h
    apply (nativeGK5BSFactorialCRTRingEquiv d).injective
    funext p
    exact (nativeGK5BSFactorialCRT_intCast d z p).trans
      ((h p).trans (nativeGK5BSCRTGlue_local d residues p).symm)
  · intro h p
    calc
      (z : ZMod ((p : Nat) ^ ((d.factorial).factorization (p : Nat)))) =
        (nativeGK5BSFactorialCRTRingEquiv d)
          (z : ZMod d.factorial) p :=
            (nativeGK5BSFactorialCRT_intCast d z p).symm
      _ = (nativeGK5BSFactorialCRTRingEquiv d)
            (nativeGK5BSCRTGlue d residues) p := by rw [h]
      _ = residues p := nativeGK5BSCRTGlue_local d residues p

/-- Strong uniqueness modulo d! of every integer solution
to ALL independent prime-power residues congruences. -/
theorem nativeGK5BSCRTInt_compatible_iff_factorialDvd
    (d : Nat) (residues : nativeGK5BSFactorialLocalFamily d)
    (z : Int) :
    (∀ p : (d.factorial).primeFactors,
      (z : ZMod ((p : Nat) ^ ((d.factorial).factorization (p : Nat)))) =
        residues p) ↔
      (d.factorial : Int) ∣ (z - nativeGK5BSCRTGlueInt d residues) := by
  rw [← ZMod.intCast_zmod_eq_zero_iff_dvd, Int.cast_sub, sub_eq_zero,
      nativeGK5BSCRTGlueInt_cast]
  exact nativeGK5BSCRTInt_compatible_iff_global d residues z

/-- A concrete canonical natural representative in the
true interval from 0 through d!-1. -/
def nativeGK5BSCRTGlueNat
    (d : Nat) (residues : nativeGK5BSFactorialLocalFamily d) : Nat :=
  (nativeGK5BSCRTGlue d residues).val

/-- The canonical natural CRT representative is STRICTLY
less than the original factorial modulus. -/
theorem nativeGK5BSCRTGlueNat_lt_factorial
    (d : Nat) (residues : nativeGK5BSFactorialLocalFamily d) :
    nativeGK5BSCRTGlueNat d residues < d.factorial := by
  letI : NeZero d.factorial := ⟨Nat.factorial_ne_zero d⟩
  exact ZMod.val_lt _

/-- Canonical natural representative still maps to the
same global residue class modulo d!. -/
theorem nativeGK5BSCRTGlueNat_cast
    (d : Nat) (residues : nativeGK5BSFactorialLocalFamily d) :
    (nativeGK5BSCRTGlueNat d residues : ZMod d.factorial) =
      nativeGK5BSCRTGlue d residues := by
  letI : NeZero d.factorial := ⟨Nat.factorial_ne_zero d⟩
  exact ZMod.natCast_zmod_val _

/-- CRT gluing preserves addition of arbitrary independently
chosen residues prime-power residue families. -/
theorem nativeGK5BSCRTGlue_add
    (d : Nat) (a b : nativeGK5BSFactorialLocalFamily d) :
    nativeGK5BSCRTGlue d (a + b) =
      nativeGK5BSCRTGlue d a + nativeGK5BSCRTGlue d b := by
  exact (nativeGK5BSFactorialCRTRingEquiv d).symm.map_add a b

/-- CRT gluing preserves multiplication of arbitrary residues
prime-power residue families, not just additive cosets. -/
theorem nativeGK5BSCRTGlue_mul
    (d : Nat) (a b : nativeGK5BSFactorialLocalFamily d) :
    nativeGK5BSCRTGlue d (a * b) =
      nativeGK5BSCRTGlue d a * nativeGK5BSCRTGlue d b := by
  exact (nativeGK5BSFactorialCRTRingEquiv d).symm.map_mul a b

/-- The true integer observations yield a *particular*
residues family: residues of their ORIGINAL GK5BQ numerator. -/
def nativeGK5BSObservedLocals
    (d j : Nat) (values : Nat → Int) :
    nativeGK5BSFactorialLocalFamily d :=
  fun p => (nativeGK5BQClearedNumerator d j values :
      ZMod ((p : Nat) ^ ((d.factorial).factorization (p : Nat))))

/-- Gluing all original numerator residues reproduces
the original integer numerator modulo the true d!. -/
theorem nativeGK5BSObserved_glue_eq_intCast
    (d j : Nat) (values : Nat → Int) :
    nativeGK5BSCRTGlue d (nativeGK5BSObservedLocals d j values) =
      (nativeGK5BQClearedNumerator d j values : ZMod d.factorial) := by
  apply (nativeGK5BSFactorialCRTRingEquiv d).injective
  funext p
  calc
    (nativeGK5BSFactorialCRTRingEquiv d)
      (nativeGK5BSCRTGlue d (nativeGK5BSObservedLocals d j values)) p =
        nativeGK5BSObservedLocals d j values p :=
          nativeGK5BSCRTGlue_local d (nativeGK5BSObservedLocals d j values) p
    _ = (nativeGK5BSFactorialCRTRingEquiv d)
          (nativeGK5BQClearedNumerator d j values : ZMod d.factorial) p :=
            (nativeGK5BSFactorialCRT_intCast d
              (nativeGK5BQClearedNumerator d j values) p).symm

/-- The genuine observed CRT glue is ZERO exactly when
GK5BQ's actual constructed integer numerator is divisible
by d!. There is no new integrality assumption. -/
theorem nativeGK5BSObserved_glue_zero_iff_factorialDvd
    (d j : Nat) (values : Nat → Int) :
    nativeGK5BSCRTGlue d (nativeGK5BSObservedLocals d j values) = 0 ↔
      (d.factorial : Int) ∣ nativeGK5BQClearedNumerator d j values := by
  rw [nativeGK5BSObserved_glue_eq_intCast]
  exact ZMod.intCast_zmod_eq_zero_iff_dvd _ _

/-- TRUE finite CRT-gluing version of the necessary and
sufficient original Newton integer coefficient source test. -/
theorem nativeGK5BSNewton_integral_iff_allCRTZero
    (d : Nat) (values : Nat → Int) :
    (∃ P : Polynomial Int,
      P.map (Int.castRingHom Rat) =
        nativeGK5BPNewtonFromRaw d
          (fun n : Nat => (values n : Rat))) ↔
    (∀ j ∈ Finset.range (d + 1),
      nativeGK5BSCRTGlue d (nativeGK5BSObservedLocals d j values) = 0) := by
  rw [nativeGK5BQNewton_integral_iff_divisible]
  constructor
  · intro h j hj
    exact (nativeGK5BSObserved_glue_zero_iff_factorialDvd d j values).2 (h j hj)
  · intro h j hj
    exact (nativeGK5BSObserved_glue_zero_iff_factorialDvd d j values).1 (h j hj)

/-- The same complete CRT-gluing test for genuine GK5BL
Lagrange interpolation at canonical integer sites. -/
theorem nativeGK5BSLagrange_integral_iff_allCRTZero
    (d : Nat) (values : Nat → Int) :
    (∃ P : Polynomial Int,
      P.map (Int.castRingHom Rat) =
        nativeGK5BLRationalInterpolant
          (nativeGK5BKIntegerGrid d)
          (fun z : Int => (values z.toNat : Rat))) ↔
    (∀ j ∈ Finset.range (d + 1),
      nativeGK5BSCRTGlue d (nativeGK5BSObservedLocals d j values) = 0) := by
  rw [nativeGK5BQLagrange_integral_iff_divisible]
  constructor
  · intro h j hj
    exact (nativeGK5BSObserved_glue_zero_iff_factorialDvd d j values).2 (h j hj)
  · intro h j hj
    exact (nativeGK5BSObserved_glue_zero_iff_factorialDvd d j values).1 (h j hj)

/-- No original integer Newton source iff there is
a single finite coefficient index whose authentic CRT
glue is nonzero, an ARITHMETIC obstruction only. -/
theorem nativeGK5BSNewton_noLift_iff_exists_nonzeroCRT
    (d : Nat) (values : Nat → Int) :
    (¬ ∃ P : Polynomial Int,
      P.map (Int.castRingHom Rat) =
        nativeGK5BPNewtonFromRaw d
          (fun n : Nat => (values n : Rat))) ↔
    (∃ j ∈ Finset.range (d + 1),
      nativeGK5BSCRTGlue d (nativeGK5BSObservedLocals d j values) ≠ 0) := by
  rw [nativeGK5BSNewton_integral_iff_allCRTZero]
  push Not
  rfl

#print axioms nativeGK5BSCRTGlue_local
#print axioms nativeGK5BSCRTGlue_unique
#print axioms nativeGK5BSFactorialCRT_intCast
#print axioms nativeGK5BSCRTGlueInt_cast
#print axioms nativeGK5BSCRTGlueInt_local
#print axioms nativeGK5BSCRTInt_compatible_iff_global
#print axioms nativeGK5BSCRTInt_compatible_iff_factorialDvd
#print axioms nativeGK5BSCRTGlueNat_lt_factorial
#print axioms nativeGK5BSCRTGlueNat_cast
#print axioms nativeGK5BSCRTGlue_add
#print axioms nativeGK5BSCRTGlue_mul
#print axioms nativeGK5BSObserved_glue_eq_intCast
#print axioms nativeGK5BSObserved_glue_zero_iff_factorialDvd
#print axioms nativeGK5BSNewton_integral_iff_allCRTZero
#print axioms nativeGK5BSLagrange_integral_iff_allCRTZero
#print axioms nativeGK5BSNewton_noLift_iff_exists_nonzeroCRT

end
end Kuu.F112.Physical
