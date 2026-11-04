import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5BTNoncoprimeCRTOverlapObstruction
import Mathlib.Algebra.GCDMonoid.Finset
import Mathlib.Tactic

/-!
F112-P94D3GK5BU — FINITE COVERS, EXACT PAIRWISE GCD
OBSTRUCTION, AND GLOBAL LCM UNIQUENESS (FIRST STAGE).

GK5BT supplies genuine arbitrary two-modulus noncoprime
CRT. Here an arbitrary finite indexed collection of actual
natural moduli and residual values is treated without
assuming pairwise coprimality.

A global integer-grid natural residue witness necessarily
forces all pairwise gcd-overlap compatibilities, and one
failed pair is an explicit obstruction to ANY global witness.
All global solutions are unique modulo the genuine finset
LCM, including empty covers and zero moduli. When a local
site has a modulus divisible by the other moduli, pairwise
compatibility also constructively yields a global witness.
True observed GK5BQ numerator residues are compatible
with their canonical genuine natural absolute-value source.

NOTE: This first stage deliberately does NOT infer the
full arbitrary-finite pairwise-compatibility sufficiency
theorem: the general descent step is a separate target,
not smuggled in as an axiom or hidden existence assumption.
No new original F55 Type witnesses, P77 class equality,
P94A four-cells, global original-phi seams, unconditional
P89 reflection, GK5BA kit, or Gray.

Strict 空; independent Kuu→Qi, genuine F54 two Nat/two
categories/Blocks and original F55 Type history preserved.
Append-only public root107. Protected PR #1558 Draft/open.
Pinned Lean v4.30.0-rc2, mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
No new axioms, sorry/admit/native_decide.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

/-- A TRUE global residue witness for an arbitrary finite
collection of natural moduli and natural local residues. -/
def nativeGK5BUFiniteGlobal
    {ι : Type*} (s : Finset ι) (moduli residues : ι → Nat)
    (x : Nat) : Prop :=
  ∀ i ∈ s, x ≡ residues i [MOD moduli i]

/-- All pairwise original local residues agree upon their
actual common gcd overlap. This is an arithmetic condition,
NOT a Type-valued structural seam or source identity. -/
def nativeGK5BUFinitePairwise
    {ι : Type*} (s : Finset ι) (moduli residues : ι → Nat) : Prop :=
  ∀ i ∈ s, ∀ j ∈ s,
    residues i ≡ residues j [MOD Nat.gcd (moduli i) (moduli j)]

/-- Original global modulus is the genuine Mathlib finite
LCM, NOT a naive product of possibly overlapping moduli. -/
def nativeGK5BUFiniteModulus
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat) : Nat :=
  s.lcm moduli

/-- A true global witness forces pairwise compatibility on
EVERY gcd overlap, without any nonzero/coprime assumptions. -/
theorem nativeGK5BUFiniteGlobal_implies_pairwise
    {ι : Type*} (s : Finset ι) (moduli residues : ι → Nat)
    (x : Nat) (hx : nativeGK5BUFiniteGlobal s moduli residues x) :
    nativeGK5BUFinitePairwise s moduli residues := by
  intro i hi j hj
  exact ((hx i hi).of_dvd (Nat.gcd_dvd_left (moduli i) (moduli j))).symm.trans
    ((hx j hj).of_dvd (Nat.gcd_dvd_right (moduli i) (moduli j)))

/-- A single failed pairwise gcd-overlap congruence is a
TRUE obstruction to ANY simultaneous global arithmetic
representative. It does not imply a failed F55 Type seam. -/
theorem nativeGK5BUFiniteNoGlobal_of_badPair
    {ι : Type*} (s : Finset ι) (moduli residues : ι → Nat)
    (i j : ι) (hi : i ∈ s) (hj : j ∈ s)
    (hbad : ¬ residues i ≡ residues j
      [MOD Nat.gcd (moduli i) (moduli j)]) :
    ¬ ∃ x : Nat, nativeGK5BUFiniteGlobal s moduli residues x := by
  rintro ⟨x, hx⟩
  exact hbad (nativeGK5BUFiniteGlobal_implies_pairwise
    s moduli residues x hx i hi j hj)

/-- Any TWO simultaneous global arithmetic witnesses
agree modulo the genuine finite LCM of all moduli.
No coprimality, positivity, or nonzero assumptions. -/
theorem nativeGK5BUFiniteGlobal_unique_mod_lcm
    {ι : Type*} (s : Finset ι) (moduli residues : ι → Nat)
    (x y : Nat)
    (hx : nativeGK5BUFiniteGlobal s moduli residues x)
    (hy : nativeGK5BUFiniteGlobal s moduli residues y) :
    x ≡ y [MOD nativeGK5BUFiniteModulus s moduli] := by
  apply (Nat.modEq_iff_dvd).2
  apply Int.natCast_dvd.mpr
  apply Finset.lcm_dvd
  intro i hi
  have hxy : x ≡ y [MOD moduli i] :=
    (hx i hi).trans (hy i hi).symm
  exact Int.natCast_dvd.mp (Nat.modEq_iff_dvd.mp hxy)

/-- Once one genuine global witness z is supplied,
ALL simultaneous solutions are precisely its single
congruence class modulo the finite LCM. -/
theorem nativeGK5BUFiniteGlobal_iff_lcm
    {ι : Type*} (s : Finset ι) (moduli residues : ι → Nat)
    (z x : Nat) (hz : nativeGK5BUFiniteGlobal s moduli residues z) :
    nativeGK5BUFiniteGlobal s moduli residues x ↔
      x ≡ z [MOD nativeGK5BUFiniteModulus s moduli] := by
  constructor
  · intro hx
    exact nativeGK5BUFiniteGlobal_unique_mod_lcm
      s moduli residues x z hx hz
  · intro h i hi
    exact (h.of_dvd (Finset.dvd_lcm hi)).trans (hz i hi)

/-- If two global solutions lie in the SAME normalized
interval [0,LCM), then they are literally equal. -/
theorem nativeGK5BUFiniteGlobal_unique_normalized
    {ι : Type*} (s : Finset ι) (moduli residues : ι → Nat)
    (x y : Nat)
    (hx : nativeGK5BUFiniteGlobal s moduli residues x)
    (hy : nativeGK5BUFiniteGlobal s moduli residues y)
    (hxb : x < nativeGK5BUFiniteModulus s moduli)
    (hyb : y < nativeGK5BUFiniteModulus s moduli) :
    x = y := by
  exact (nativeGK5BUFiniteGlobal_unique_mod_lcm
    s moduli residues x y hx hy).eq_of_lt_of_lt hxb hyb

/-- Genuine finite pairwise gcd compatibility is stable
under pointwise addition of two local residue tables. -/
theorem nativeGK5BUFinitePairwise_add
    {ι : Type*} (s : Finset ι) (moduli a b : ι → Nat)
    (ha : nativeGK5BUFinitePairwise s moduli a)
    (hb : nativeGK5BUFinitePairwise s moduli b) :
    nativeGK5BUFinitePairwise s moduli (fun i => a i + b i) := by
  intro i hi j hj
  exact (ha i hi j hj).add (hb i hi j hj)

/-- Genuine finite pairwise gcd compatibility is stable
under pointwise multiplication of local residue tables. -/
theorem nativeGK5BUFinitePairwise_mul
    {ι : Type*} (s : Finset ι) (moduli a b : ι → Nat)
    (ha : nativeGK5BUFinitePairwise s moduli a)
    (hb : nativeGK5BUFinitePairwise s moduli b) :
    nativeGK5BUFinitePairwise s moduli (fun i => a i * b i) := by
  intro i hi j hj
  exact (ha i hi j hj).mul (hb i hi j hj)

/-- A genuine sufficient finite-cover condition:
if one ACTUAL member's modulus is divisible by every
modulus of the cover, pairwise compatibility CONSTRUCTS
a global witness, namely that anchor's observed value. -/
theorem nativeGK5BUFiniteGlobal_of_dominatingSite
    {ι : Type*} (s : Finset ι) (moduli residues : ι → Nat)
    (anchor : ι) (ha : anchor ∈ s)
    (hdom : ∀ i ∈ s, moduli i ∣ moduli anchor)
    (hpair : nativeGK5BUFinitePairwise s moduli residues) :
    nativeGK5BUFiniteGlobal s moduli residues (residues anchor) := by
  intro i hi
  have h : Nat.gcd (moduli anchor) (moduli i) = moduli i :=
    Nat.gcd_eq_right (hdom i hi)
  simpa only [h] using hpair anchor ha i hi

/-- Constructive existence consequence of a dominating
finite local site, without adding source-Type assumptions. -/
theorem nativeGK5BUFiniteGlobal_exists_of_dominatingSite
    {ι : Type*} (s : Finset ι) (moduli residues : ι → Nat)
    (anchor : ι) (ha : anchor ∈ s)
    (hdom : ∀ i ∈ s, moduli i ∣ moduli anchor)
    (hpair : nativeGK5BUFinitePairwise s moduli residues) :
    ∃ x : Nat, nativeGK5BUFiniteGlobal s moduli residues x :=
  ⟨residues anchor,
    nativeGK5BUFiniteGlobal_of_dominatingSite
      s moduli residues anchor ha hdom hpair⟩

/-- The ORIGINAL signed GK5BQ integer numerator, observed
via its true Nat absolute value, supplies an ACTUAL common
global representative for all finite local moduli. -/
theorem nativeGK5BUObservedGlobal
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (d j : Nat) (values : Nat → Int) :
    nativeGK5BUFiniteGlobal s moduli
      (fun i => nativeGK5BTObservedNumeratorAbs d j values % moduli i)
      (nativeGK5BTObservedNumeratorAbs d j values) := by
  intro i hi
  exact (Nat.mod_modEq _ _).symm

/-- All original integer-numerator local residue tables
automatically agree on every TRUE gcd overlap, with the
signed divisibility data retained by their source. -/
theorem nativeGK5BUObservedPairwise
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (d j : Nat) (values : Nat → Int) :
    nativeGK5BUFinitePairwise s moduli
      (fun i => nativeGK5BTObservedNumeratorAbs d j values % moduli i) := by
  exact nativeGK5BUFiniteGlobal_implies_pairwise
    s moduli
    (fun i => nativeGK5BTObservedNumeratorAbs d j values % moduli i)
    (nativeGK5BTObservedNumeratorAbs d j values)
    (nativeGK5BUObservedGlobal s moduli d j values)

#print axioms nativeGK5BUFiniteGlobal_implies_pairwise
#print axioms nativeGK5BUFiniteNoGlobal_of_badPair
#print axioms nativeGK5BUFiniteGlobal_unique_mod_lcm
#print axioms nativeGK5BUFiniteGlobal_iff_lcm
#print axioms nativeGK5BUFiniteGlobal_unique_normalized
#print axioms nativeGK5BUFinitePairwise_add
#print axioms nativeGK5BUFinitePairwise_mul
#print axioms nativeGK5BUFiniteGlobal_of_dominatingSite
#print axioms nativeGK5BUFiniteGlobal_exists_of_dominatingSite
#print axioms nativeGK5BUObservedGlobal
#print axioms nativeGK5BUObservedPairwise

end
end Kuu.F112.Physical
