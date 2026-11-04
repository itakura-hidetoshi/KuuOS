import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5BSCRTLocalGlobalGluing
import Mathlib.Data.Nat.ModEq
import Mathlib.Data.Int.ModEq
import Mathlib.Tactic

/-!
F112-P94D3GK5BT — ACTUAL NON-COPRIME CRT OVERLAP COMPATIBILITY
AND CONDITIONALLY GLUED GLOBAL INTEGER RESIDUE CLASSES.

GK5BS proved the genuine pinned ZMod.equivPi for pairwise
coprime maximal factorial prime powers. GK5BT allows ANY
two natural moduli m,n, including common prime factors and
the zero-modulus edge cases. Their overlap is gcd m n;
compatible local residues a,b glue iff
    a ≡ b [MOD gcd m n],
and the glued global class is unique modulo lcm m n.

The actual pinned Mathlib Nat.chineseRemainder' constructs
the global natural witness from overlap compatibility.
Nat.mod_lcm proves global uniqueness. Obstruction is exactly
a failed overlap congruence: incompatible local residues
admit NO global integer/natural representative. For nonzero
m,n the constructor lands in the genuine interval [0,lcm).

For original GK5BQ signed integer raw observation numerators
N_(d,j)(v), we use genuine Nat.natAbs to retain the exact
factorial divisibility verdict even for negative numerators.
Its two local residues ALWAYS agree on overlap, glue back to
the absolute original numerator modulo lcm, and gluing to
zero is equivalent to lcm-divisibility of the signed numerator.
No coefficient or original F55 Type source is invented.

Arithmetic compatibility is not original F55 Type history,
P77 class equality, P94A four-cells, original-phi seams,
unconditional P89 reflection, or universal GK5AY seams.
Strict 空; independent Kuu→Qi, true F54 two Nat/two
categories/Blocks and original F55 Type history preserved.
Append-only public root107, #1558 Draft/OPEN/unmerged.
Pinned Lean v4.30.0-rc2, mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
No axioms, sorry/admit/native_decide, Gray, GK5BA kit.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

/-- Explicit overlap compatibility at the ACTUAL gcd. -/
def nativeGK5BTOverlapCompatible
    (m n a b : Nat) : Prop :=
  a ≡ b [MOD Nat.gcd m n]

/-- Compatibility is exactly an equality of genuine
remainders modulo the overlap gcd, without coprimality. -/
theorem nativeGK5BTOverlapCompatible_iff_mod_gcd
    (m n a b : Nat) :
    nativeGK5BTOverlapCompatible m n a b ↔
      a % Nat.gcd m n = b % Nat.gcd m n := by
  rfl

/-- NECESSARY AND SUFFICIENT general non-coprime CRT:
the original local residues can be glued to one NATURAL
global representative precisely when they agree on gcd.
This includes zero moduli, handled by pinned Mathlib. -/
theorem nativeGK5BTOverlap_iff_exists_gluing
    (m n a b : Nat) :
    nativeGK5BTOverlapCompatible m n a b ↔
      ∃ x : Nat, x ≡ a [MOD m] ∧ x ≡ b [MOD n] := by
  constructor
  · intro h
    exact ⟨(Nat.chineseRemainder' h).val,
      (Nat.chineseRemainder' h).property⟩
  · rintro ⟨x, hx, hy⟩
    exact ((hx.1.of_dvd (Nat.gcd_dvd_left m n)).symm).trans
      (hx.2.of_dvd (Nat.gcd_dvd_right m n))

/-- Construct the genuine pinned Mathlib CRT natural
representative from an ACTUAL compatibility proof.
No witness is postulated or hidden in an axiom. -/
def nativeGK5BTOverlapGlue
    (m n a b : Nat) (h : nativeGK5BTOverlapCompatible m n a b) : Nat :=
  (Nat.chineseRemainder' h).val

/-- The canonical overlap glue satisfies the first
original modular constraint. -/
theorem nativeGK5BTOverlapGlue_left
    (m n a b : Nat) (h : nativeGK5BTOverlapCompatible m n a b) :
    nativeGK5BTOverlapGlue m n a b h ≡ a [MOD m] :=
  (Nat.chineseRemainder' h).property.1

/-- The canonical overlap glue satisfies the second
original modular constraint. -/
theorem nativeGK5BTOverlapGlue_right
    (m n a b : Nat) (h : nativeGK5BTOverlapCompatible m n a b) :
    nativeGK5BTOverlapGlue m n a b h ≡ b [MOD n] :=
  (Nat.chineseRemainder' h).property.2

/-- Every global candidate satisfying both overlapping
local constraints lies in the SAME class modulo lcm. -/
theorem nativeGK5BTOverlapGlue_unique_mod_lcm
    (m n a b x : Nat)
    (h : nativeGK5BTOverlapCompatible m n a b)
    (hx : x ≡ a [MOD m])
    (hy : x ≡ b [MOD n]) :
    x ≡ nativeGK5BTOverlapGlue m n a b h [MOD Nat.lcm m n] :=
  Nat.mod_lcm
    (hx.trans (nativeGK5BTOverlapGlue_left m n a b h).symm)
    (hy.trans (nativeGK5BTOverlapGlue_right m n a b h).symm)

/-- EXACT characterization of the full solution set:
being a simultaneous local representative is EQUIVALENT
to congruence with the canonical glue modulo lcm. -/
theorem nativeGK5BTOverlap_compatible_iff_mod_lcm
    (m n a b x : Nat)
    (h : nativeGK5BTOverlapCompatible m n a b) :
    (x ≡ a [MOD m] ∧ x ≡ b [MOD n]) ↔
      x ≡ nativeGK5BTOverlapGlue m n a b h [MOD Nat.lcm m n] := by
  constructor
  · intro hx
    exact nativeGK5BTOverlapGlue_unique_mod_lcm
      m n a b x h hx.1 hx.2
  · intro hx
    constructor
    · exact (hx.of_dvd (Nat.dvd_lcm_left m n)).trans
        (nativeGK5BTOverlapGlue_left m n a b h)
    · exact (hx.of_dvd (Nat.dvd_lcm_right m n)).trans
        (nativeGK5BTOverlapGlue_right m n a b h)

/-- With both moduli nonzero, the actual Mathlib CRT
representative is normalized in [0,lcm(m,n)). -/
theorem nativeGK5BTOverlapGlue_lt_lcm
    (m n a b : Nat)
    (h : nativeGK5BTOverlapCompatible m n a b)
    (hm : m ≠ 0) (hn : n ≠ 0) :
    nativeGK5BTOverlapGlue m n a b h < Nat.lcm m n :=
  Nat.chineseRemainder'_lt_lcm h hm hn

/-- For nonzero moduli the representative is the UNIQUE
solution in the genuine normalized interval [0,lcm). -/
theorem nativeGK5BTOverlapGlue_eq_of_lt_lcm
    (m n a b x : Nat)
    (h : nativeGK5BTOverlapCompatible m n a b)
    (hm : m ≠ 0) (hn : n ≠ 0)
    (hx : x ≡ a [MOD m] ∧ x ≡ b [MOD n])
    (hbound : x < Nat.lcm m n) :
    x = nativeGK5BTOverlapGlue m n a b h := by
  exact (nativeGK5BTOverlapGlue_unique_mod_lcm
    m n a b x h hx.1 hx.2).eq_of_lt_of_lt
      hbound (nativeGK5BTOverlapGlue_lt_lcm m n a b h hm hn)

/-- Incompatible residues have no global solution.
This is an ACTUAL arithmetic overlap obstruction, not
an original Type-valued F55 seam obstruction. -/
theorem nativeGK5BTNoGluing_iff_overlapObstruction
    (m n a b : Nat) :
    (¬ ∃ x : Nat, x ≡ a [MOD m] ∧ x ≡ b [MOD n]) ↔
      ¬ nativeGK5BTOverlapCompatible m n a b := by
  exact not_iff_not.mpr
    (nativeGK5BTOverlap_iff_exists_gluing m n a b).symm

/-- A single concrete failed equality on the overlap
gcd is a complete obstruction to the global CRT witness. -/
theorem nativeGK5BTNoGluing_of_gcdResidueMismatch
    (m n a b : Nat)
    (hbad : a % Nat.gcd m n ≠ b % Nat.gcd m n) :
    ¬ ∃ x : Nat, x ≡ a [MOD m] ∧ x ≡ b [MOD n] := by
  exact (nativeGK5BTNoGluing_iff_overlapObstruction m n a b).2
    ((nativeGK5BTOverlapCompatible_iff_mod_gcd m n a b).not.mpr hbad)

/-- Overlap compatibility persists under addition of
two independently compatible residue pairs. -/
theorem nativeGK5BTOverlapCompatible_add
    (m n a b c d : Nat)
    (hab : nativeGK5BTOverlapCompatible m n a b)
    (hcd : nativeGK5BTOverlapCompatible m n c d) :
    nativeGK5BTOverlapCompatible m n (a + c) (b + d) :=
  hab.add hcd

/-- Overlap compatibility also persists under product. -/
theorem nativeGK5BTOverlapCompatible_mul
    (m n a b c d : Nat)
    (hab : nativeGK5BTOverlapCompatible m n a b)
    (hcd : nativeGK5BTOverlapCompatible m n c d) :
    nativeGK5BTOverlapCompatible m n (a * c) (b * d) :=
  hab.mul hcd

/-- The ACTUAL original signed integer GK5BQ numerator
is retained, with natAbs used solely to present its
natural CRT residues without losing divisibility data. -/
def nativeGK5BTObservedNumeratorAbs
    (d j : Nat) (values : Nat → Int) : Nat :=
  (nativeGK5BQClearedNumerator d j values).natAbs

/-- The two independently observed residues of the SAME
true integer numerator always agree on their gcd overlap;
this is not a new assumption or a source-class equality. -/
theorem nativeGK5BTObserved_overlapCompatible
    (m n d j : Nat) (values : Nat → Int) :
    nativeGK5BTOverlapCompatible m n
      (nativeGK5BTObservedNumeratorAbs d j values % m)
      (nativeGK5BTObservedNumeratorAbs d j values % n) := by
  have hm : nativeGK5BTObservedNumeratorAbs d j values ≡
      nativeGK5BTObservedNumeratorAbs d j values % m [MOD m] :=
    (Nat.mod_modEq _ _).symm
  have hn : nativeGK5BTObservedNumeratorAbs d j values ≡
      nativeGK5BTObservedNumeratorAbs d j values % n [MOD n] :=
    (Nat.mod_modEq _ _).symm
  exact ((hm.of_dvd (Nat.gcd_dvd_left m n)).symm).trans
    (hn.of_dvd (Nat.gcd_dvd_right m n))

/-- The CRT glue of the two genuine observed local
residues is precisely the actual signed numerator's
absolute value MODULO the true lcm(m,n), even when the
original integer numerator is negative or zero. -/
theorem nativeGK5BTObserved_glue_eq_original_mod_lcm
    (m n d j : Nat) (values : Nat → Int) :
    nativeGK5BTObservedNumeratorAbs d j values ≡
      nativeGK5BTOverlapGlue m n
        (nativeGK5BTObservedNumeratorAbs d j values % m)
        (nativeGK5BTObservedNumeratorAbs d j values % n)
        (nativeGK5BTObserved_overlapCompatible m n d j values)
      [MOD Nat.lcm m n] := by
  exact nativeGK5BTOverlapGlue_unique_mod_lcm m n
    (nativeGK5BTObservedNumeratorAbs d j values % m)
    (nativeGK5BTObservedNumeratorAbs d j values % n)
    (nativeGK5BTObservedNumeratorAbs d j values)
    (nativeGK5BTObserved_overlapCompatible m n d j values)
    (Nat.mod_modEq _ _).symm
    (Nat.mod_modEq _ _).symm

/-- The ACTUAL signed original integer numerator is
divisible by lcm(m,n) iff its independently sampled
non-coprime CRT glue is ZERO modulo lcm. This precisely
retains negative numerators through Int.natCast_dvd. -/
theorem nativeGK5BTObserved_glue_zero_iff_lcmDvd
    (m n d j : Nat) (values : Nat → Int) :
    (nativeGK5BTOverlapGlue m n
      (nativeGK5BTObservedNumeratorAbs d j values % m)
      (nativeGK5BTObservedNumeratorAbs d j values % n)
      (nativeGK5BTObserved_overlapCompatible m n d j values))
        ≡ 0 [MOD Nat.lcm m n] ↔
    ((Nat.lcm m n : Nat) : Int) ∣
      nativeGK5BQClearedNumerator d j values := by
  constructor
  · intro h
    apply Int.natCast_dvd.mpr
    exact Nat.modEq_zero_iff_dvd.mp
      ((nativeGK5BTObserved_glue_eq_original_mod_lcm
        m n d j values).trans h)
  · intro h
    have hz : nativeGK5BTObservedNumeratorAbs d j values
        ≡ 0 [MOD Nat.lcm m n] :=
      Nat.modEq_zero_iff_dvd.mpr (Int.natCast_dvd.mp h)
    exact (nativeGK5BTObserved_glue_eq_original_mod_lcm
      m n d j values).symm.trans hz

#print axioms nativeGK5BTOverlapCompatible_iff_mod_gcd
#print axioms nativeGK5BTOverlap_iff_exists_gluing
#print axioms nativeGK5BTOverlapGlue_left
#print axioms nativeGK5BTOverlapGlue_right
#print axioms nativeGK5BTOverlapGlue_unique_mod_lcm
#print axioms nativeGK5BTOverlap_compatible_iff_mod_lcm
#print axioms nativeGK5BTOverlapGlue_lt_lcm
#print axioms nativeGK5BTOverlapGlue_eq_of_lt_lcm
#print axioms nativeGK5BTNoGluing_iff_overlapObstruction
#print axioms nativeGK5BTNoGluing_of_gcdResidueMismatch
#print axioms nativeGK5BTOverlapCompatible_add
#print axioms nativeGK5BTOverlapCompatible_mul
#print axioms nativeGK5BTObserved_overlapCompatible
#print axioms nativeGK5BTObserved_glue_eq_original_mod_lcm
#print axioms nativeGK5BTObserved_glue_zero_iff_lcmDvd

end
end Kuu.F112.Physical
