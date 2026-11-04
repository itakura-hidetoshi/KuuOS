import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5BUFiniteCoverOverlap
import Mathlib.Data.Nat.Factorization.Basic
import Mathlib.Algebra.GCDMonoid.Finset
import Mathlib.Tactic

/-!
F112-P94D3GK5BV — COMPLETE FINITE NON-COPRIME CRT DESCENT.

GK5BU established the necessity of pairwise gcd compatibility,
finite-cover lcm uniqueness and concrete bad-pair obstruction.
We now PROVE the converse for ANY finite family of genuine
natural moduli, with NO dominating-site, nonzero, coprime,
or source-Type existence assumptions.

A key genuine arithmetic lemma proves distributivity of gcd
over lcm (including zero arguments), by using the PINNED
Mathlib NAT prime factorization lattice only in nonzero case.
An induction on Finset then glues the current true global
representative to the next site with GK5BT's real
Nat.chineseRemainder'. All overlap compatibility checks come
from the ORIGINAL pairwise congruences on gcd; no synthetic
source or hidden postulated witness is introduced.

The complete theorem is:
  (∀i∈s,∀j∈s, a_i ≡ a_j [MOD gcd(m_i,m_j)])
    ↔ ∃x:Nat,∀i∈s, x ≡ a_i [MOD m_i].
All x are a SINGLE class modulo Finset.lcm; a canonical
chosen x and its normalized representative are defined,
together with an exact incompatible-pair obstruction.
The empty cover and moduli equal to zero are included.

Arithmetic descent ≠ original F55 Type-valued history,
P77 class equality, P94A four-cell, unconditional P89,
GK5AY global seam, or an implied W=1→seam.
Strict 空; independent Kuu→Qi; true original F54 two Nat/
two categories/Blocks, F55 Type history retained.
Append-only public root107, protected #1558 Draft/open.
Pinned Lean v4.30.0-rc2, mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
No new axioms, sorry/admit/native_decide, Gray or GK5BA kit.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

/-- TRUE distributivity of gcd over lcm for arbitrary Nat,
including zero moduli. The nonzero branch uses pinned
mathlib factorization equality into a distributive lattice,
with no unverified number-theory assertion. -/
theorem nativeGK5BVGcd_lcm_distrib
    (a b c : Nat) :
    Nat.gcd (Nat.lcm a b) c =
      Nat.lcm (Nat.gcd a c) (Nat.gcd b c) := by
  by_cases ha : a = 0
  · subst a
    simp only [Nat.lcm_zero_left, Nat.gcd_zero_left]
    exact ((Nat.lcm_eq_left_iff_dvd).2 (Nat.gcd_dvd_right b c)).symm
  by_cases hb : b = 0
  · subst b
    simp only [Nat.lcm_zero_right, Nat.gcd_zero_left]
    exact ((Nat.lcm_eq_right_iff_dvd).2 (Nat.gcd_dvd_right a c)).symm
  by_cases hc : c = 0
  · subst c
    simp
  have hl : Nat.lcm a b ≠ 0 := Nat.lcm_ne_zero ha hb
  have hla : Nat.gcd a c ≠ 0 := Nat.gcd_ne_zero_left ha
  have hlb : Nat.gcd b c ≠ 0 := Nat.gcd_ne_zero_left hb
  apply Nat.factorization_inj
    (Nat.gcd_ne_zero_left hl) (Nat.lcm_ne_zero hla hlb)
  rw [Nat.factorization_gcd hl hc,
    Nat.factorization_lcm ha hb,
    Nat.factorization_lcm hla hlb,
    Nat.factorization_gcd ha hc,
    Nat.factorization_gcd hb hc]
  ext p
  simp only [Finsupp.inf_apply, Finsupp.sup_apply]
  exact min_max_distrib_right _ _ _

/-- The gcd of the genuine finite LCM of all original
moduli with a new modulus distributes over that finite
cover, including empty s and zero moduli. -/
theorem nativeGK5BVFiniteGcd_lcm
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat) (m : Nat) :
    Nat.gcd (s.lcm moduli) m =
      s.lcm (fun i => Nat.gcd (moduli i) m) := by
  classical
  induction s using Finset.induction_on with
  | empty =>
      simp
  | @insert i t hi ih =>
      simp only [Finset.lcm_insert, lcm_eq_nat_lcm]
      rw [nativeGK5BVGcd_lcm_distrib, ih]

/-- All pairwise-compatible finite local residues glue to
one genuine global representative. Unlike the earlier
dominating-site theorem this has NO extra assumptions:
no nonzero, coprime, or max-modulus condition. -/
theorem nativeGK5BVFinitePairwise_exists_global
    {ι : Type*} (s : Finset ι)
    (moduli residues : ι → Nat)
    (hpair : nativeGK5BUFinitePairwise s moduli residues) :
    ∃ x : Nat, nativeGK5BUFiniteGlobal s moduli residues x := by
  classical
  induction s using Finset.induction_on with
  | empty =>
      exact ⟨0, by simp [nativeGK5BUFiniteGlobal]⟩
  | @insert i t hi ih =>
      have hpair_t : nativeGK5BUFinitePairwise t moduli residues := by
        intro j hj k hk
        exact hpair j (Finset.mem_insert_of_mem hj)
          k (Finset.mem_insert_of_mem hk)
      obtain ⟨x, hx⟩ := ih hpair_t
      have hoverlap_each (j : ι) (hj : j ∈ t) :
          x ≡ residues i [MOD Nat.gcd (moduli j) (moduli i)] := by
        exact ((hx j hj).of_dvd
          (Nat.gcd_dvd_left (moduli j) (moduli i))).trans
            (hpair j (Finset.mem_insert_of_mem hj)
              i (Finset.mem_insert_self i t))
      have hoverlap_lcm :
          x ≡ residues i
            [MOD t.lcm (fun j => Nat.gcd (moduli j) (moduli i))] := by
        apply (Nat.modEq_iff_dvd).2
        apply Int.natCast_dvd.mpr
        apply Finset.lcm_dvd
        intro j hj
        exact Int.natCast_dvd.mp
          (Nat.modEq_iff_dvd.mp (hoverlap_each j hj))
      have hoverlap : nativeGK5BTOverlapCompatible
          (t.lcm moduli) (moduli i) x (residues i) := by
        change x ≡ residues i
          [MOD Nat.gcd (t.lcm moduli) (moduli i)]
        rw [nativeGK5BVFiniteGcd_lcm]
        exact hoverlap_lcm
      obtain ⟨y, hy, hiy⟩ :=
        (nativeGK5BTOverlap_iff_exists_gluing
          (t.lcm moduli) (moduli i) x (residues i)).1 hoverlap
      refine ⟨y, ?_⟩
      intro j hj
      rcases Finset.mem_insert.mp hj with rfl | hj
      · exact hiy
      · exact (hy.of_dvd (Finset.dvd_lcm hj)).trans (hx j hj)

/-- NECESSARY AND SUFFICIENT FINITE NON-COPRIME CRT:
pairwise gcd compatibility is EXACTLY the existence of a
global witness on the whole finite cover. No extra
hypothesis even for the empty cover and zero moduli. -/
theorem nativeGK5BVFinitePairwise_iff_exists_global
    {ι : Type*} (s : Finset ι)
    (moduli residues : ι → Nat) :
    nativeGK5BUFinitePairwise s moduli residues ↔
      ∃ x : Nat, nativeGK5BUFiniteGlobal s moduli residues x := by
  constructor
  · exact nativeGK5BVFinitePairwise_exists_global s moduli residues
  · rintro ⟨x, hx⟩
    exact nativeGK5BUFiniteGlobal_implies_pairwise
      s moduli residues x hx

/-- The exact obstruction for arbitrary finite covers:
no global arithmetic witness iff SOME actual pair of
indices fails congruence on the genuine pairwise gcd. -/
theorem nativeGK5BVFiniteNoGlobal_iff_badPair
    {ι : Type*} (s : Finset ι)
    (moduli residues : ι → Nat) :
    (¬ ∃ x : Nat, nativeGK5BUFiniteGlobal s moduli residues x) ↔
    (∃ i ∈ s, ∃ j ∈ s,
      ¬ residues i ≡ residues j
        [MOD Nat.gcd (moduli i) (moduli j)]) := by
  rw [← nativeGK5BVFinitePairwise_iff_exists_global]
  simp only [nativeGK5BUFinitePairwise]
  push Not
  rfl

/-- The true global witness is constructed by extracting
the real Finset induction / pinned two-modulus CRT proof,
not by a new numerical oracle. -/
def nativeGK5BVFiniteGlue
    {ι : Type*} (s : Finset ι)
    (moduli residues : ι → Nat)
    (hpair : nativeGK5BUFinitePairwise s moduli residues) : Nat :=
  Classical.choose (nativeGK5BVFinitePairwise_exists_global
    s moduli residues hpair)

/-- Every original local congruence is satisfied by the
actual canonical chosen finite noncoprime CRT witness. -/
theorem nativeGK5BVFiniteGlue_global
    {ι : Type*} (s : Finset ι)
    (moduli residues : ι → Nat)
    (hpair : nativeGK5BUFinitePairwise s moduli residues) :
    nativeGK5BUFiniteGlobal s moduli residues
      (nativeGK5BVFiniteGlue s moduli residues hpair) :=
  Classical.choose_spec (nativeGK5BVFinitePairwise_exists_global
    s moduli residues hpair)

/-- The chosen finite CRT witness is UNIQUE modulo the
true finite LCM, with no coprime/nonzero assumptions. -/
theorem nativeGK5BVFiniteGlue_unique_mod_lcm
    {ι : Type*} (s : Finset ι)
    (moduli residues : ι → Nat)
    (hpair : nativeGK5BUFinitePairwise s moduli residues)
    (x : Nat) (hx : nativeGK5BUFiniteGlobal s moduli residues x) :
    x ≡ nativeGK5BVFiniteGlue s moduli residues hpair
      [MOD nativeGK5BUFiniteModulus s moduli] :=
  nativeGK5BUFiniteGlobal_unique_mod_lcm
    s moduli residues x
    (nativeGK5BVFiniteGlue s moduli residues hpair)
    hx (nativeGK5BVFiniteGlue_global s moduli residues hpair)

/-- A definite normalized natural representative of the
true finite arithmetic CRT class; when L=0 its value is
the unnormalized original representative (mod 0 = id). -/
def nativeGK5BVFiniteGlueNat
    {ι : Type*} (s : Finset ι)
    (moduli residues : ι → Nat)
    (hpair : nativeGK5BUFinitePairwise s moduli residues) : Nat :=
  nativeGK5BVFiniteGlue s moduli residues hpair %
    nativeGK5BUFiniteModulus s moduli

/-- The normalized representative still satisfies ALL
genuine local congruences, including modulus-zero sites. -/
theorem nativeGK5BVFiniteGlueNat_global
    {ι : Type*} (s : Finset ι)
    (moduli residues : ι → Nat)
    (hpair : nativeGK5BUFinitePairwise s moduli residues) :
    nativeGK5BUFiniteGlobal s moduli residues
      (nativeGK5BVFiniteGlueNat s moduli residues hpair) := by
  intro i hi
  exact ((Nat.mod_modEq _ _).of_dvd
      (Finset.dvd_lcm hi)).trans
        (nativeGK5BVFiniteGlue_global
          s moduli residues hpair i hi)

/-- If the cover has nonzero global LCM, the canonical
normalization lives strictly inside [0,LCM). -/
theorem nativeGK5BVFiniteGlueNat_lt_lcm
    {ι : Type*} (s : Finset ι)
    (moduli residues : ι → Nat)
    (hpair : nativeGK5BUFinitePairwise s moduli residues)
    (hL : nativeGK5BUFiniteModulus s moduli ≠ 0) :
    nativeGK5BVFiniteGlueNat s moduli residues hpair <
      nativeGK5BUFiniteModulus s moduli :=
  Nat.mod_lt _ (Nat.pos_of_ne_zero hL)

#print axioms nativeGK5BVGcd_lcm_distrib
#print axioms nativeGK5BVFiniteGcd_lcm
#print axioms nativeGK5BVFinitePairwise_exists_global
#print axioms nativeGK5BVFinitePairwise_iff_exists_global
#print axioms nativeGK5BVFiniteNoGlobal_iff_badPair
#print axioms nativeGK5BVFiniteGlue_global
#print axioms nativeGK5BVFiniteGlue_unique_mod_lcm
#print axioms nativeGK5BVFiniteGlueNat_global
#print axioms nativeGK5BVFiniteGlueNat_lt_lcm

end
end Kuu.F112.Physical
