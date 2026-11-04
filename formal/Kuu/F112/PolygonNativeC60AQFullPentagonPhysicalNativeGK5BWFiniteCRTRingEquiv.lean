import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5BVGeneralFiniteCRTDescent
import Mathlib.Data.ZMod.Basic
import Mathlib.Algebra.GCDMonoid.Finset
import Mathlib.Tactic

/-!
F112-P94D3GK5BW — COMPLETE FINITE NONCOPRIME CRT AS A RING EQUIVALENCE.

Independent GK5BV proves genuine finite pairwise gcd-overlap
compatibility iff a global natural representative exists.
We strengthen this to a TRUE ring equivalence from ZMod
(Finset.lcm moduli) onto the subring of all compatible
families in the dependent product of original ZMod rings.

Important zero-modulus boundary: ZMod 0 is the integer ring,
NOT the image of Nat.cast alone. Our surjectivity proof splits
on genuine finite LCM = 0. A zero-modulus original site then
provides the actual signed integer witness; otherwise the
finite natural CRT of GK5BV applies to all nonzero moduli.
No coprimality, positivity, nonzero, dominating-site, or
nonempty-cover assumptions, including empty covers.

The ring-isomorphism is exclusively numeric: it does NOT
reconstruct original F55 Type witnesses, P77 class equality,
P94A four-cells, universal GK5AY seam or unconditional P89
reflection. Genuine original F54 two Nat/two categories/
Blocks and F55 Type source history unchanged. Strict 空,
independent Kuu→Qi, append-only public root107, protected
#1558 Draft/open/unmerged. Pinned Lean v4.30.0-rc2,
mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
No axioms, sorry, admit, native_decide, Gray or GK5BA kit.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

/-- True dependent product of the local ZMod rings on a
finite original cover; index types keep original membership. -/
abbrev nativeGK5BWLocalFamily
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat) : Type _ :=
  (i : {i : ι // i ∈ s}) → ZMod (moduli i.1)

/-- The original local family agrees under genuine ZMod
maps into each exact pairwise gcd overlap. -/
def nativeGK5BWCompatible
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (a : nativeGK5BWLocalFamily s moduli) : Prop :=
  ∀ i j : {i : ι // i ∈ s},
    (ZMod.castHom (Nat.gcd_dvd_left (moduli i.1) (moduli j.1))
      (ZMod (Nat.gcd (moduli i.1) (moduli j.1)))) (a i) =
    (ZMod.castHom (Nat.gcd_dvd_right (moduli i.1) (moduli j.1))
      (ZMod (Nat.gcd (moduli i.1) (moduli j.1)))) (a j)

/-- Compatible local residues form an actual subring
of the full dependent product, not merely a set of witnesses. -/
def nativeGK5BWCompatibleSubring
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat) :
    Subring (nativeGK5BWLocalFamily s moduli) where
  carrier := {a | nativeGK5BWCompatible s moduli a}
  zero_mem' := by
    intro i j
    simp [nativeGK5BWCompatible]
  one_mem' := by
    intro i j
    simp [nativeGK5BWCompatible]
  add_mem' := by
    intro a b ha hb i j
    simp only [Pi.add_apply, map_add]
    rw [ha i j, hb i j]
  mul_mem' := by
    intro a b ha hb i j
    simp only [Pi.mul_apply, map_mul]
    rw [ha i j, hb i j]
  neg_mem' := by
    intro a ha i j
    simp only [Pi.neg_apply, map_neg]
    rw [ha i j]

/-- True coordinatewise ring homomorphism from the
GLOBAL LCM quotient to all local quotient rings. -/
def nativeGK5BWGlobalLocalHom
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat) :
    ZMod (nativeGK5BUFiniteModulus s moduli) →+*
      nativeGK5BWLocalFamily s moduli where
  toFun x i :=
    (ZMod.castHom (Finset.dvd_lcm i.2)
      (ZMod (moduli i.1))) x
  map_zero' := by
    funext i
    exact map_zero (ZMod.castHom (Finset.dvd_lcm i.2) (ZMod (moduli i.1)))
  map_one' := by
    funext i
    exact map_one (ZMod.castHom (Finset.dvd_lcm i.2) (ZMod (moduli i.1)))
  map_add' := by
    intro x y
    funext i
    exact map_add (ZMod.castHom (Finset.dvd_lcm i.2) (ZMod (moduli i.1))) x y
  map_mul' := by
    intro x y
    funext i
    exact map_mul (ZMod.castHom (Finset.dvd_lcm i.2) (ZMod (moduli i.1))) x y

/-- All global residues satisfy the original exact pairwise
overlap conditions: both ways around the square are the
unique ring map out of ZMod L into ZMod gcd. -/
theorem nativeGK5BWGlobalLocalHom_compatible
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (x : ZMod (nativeGK5BUFiniteModulus s moduli)) :
    nativeGK5BWCompatible s moduli
      (nativeGK5BWGlobalLocalHom s moduli x) := by
  intro i j
  change
    ((ZMod.castHom (Nat.gcd_dvd_left (moduli i.1) (moduli j.1))
      (ZMod (Nat.gcd (moduli i.1) (moduli j.1)))).comp
      (ZMod.castHom (Finset.dvd_lcm i.2) (ZMod (moduli i.1)))) x =
    ((ZMod.castHom (Nat.gcd_dvd_right (moduli i.1) (moduli j.1))
      (ZMod (Nat.gcd (moduli i.1) (moduli j.1)))).comp
      (ZMod.castHom (Finset.dvd_lcm j.2) (ZMod (moduli j.1)))) x
  exact congrArg
    (fun f : ZMod (nativeGK5BUFiniteModulus s moduli) →+*
      ZMod (Nat.gcd (moduli i.1) (moduli j.1)) => f x)
    (RingHom.ext_zmod _ _)

/-- The TRUE ring homomorphism into the compatible local
residue subring, preserving addition and multiplication. -/
def nativeGK5BWGlobalCompatibleHom
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat) :
    ZMod (nativeGK5BUFiniteModulus s moduli) →+*
      nativeGK5BWCompatibleSubring s moduli where
  toFun x := ⟨nativeGK5BWGlobalLocalHom s moduli x,
    nativeGK5BWGlobalLocalHom_compatible s moduli x⟩
  map_zero' := Subtype.ext (map_zero (nativeGK5BWGlobalLocalHom s moduli))
  map_one' := Subtype.ext (map_one (nativeGK5BWGlobalLocalHom s moduli))
  map_add' := by
    intro x y
    exact Subtype.ext (map_add (nativeGK5BWGlobalLocalHom s moduli) x y)
  map_mul' := by
    intro x y
    exact Subtype.ext (map_mul (nativeGK5BWGlobalLocalHom s moduli) x y)

/-- Coordinate projection of the global compatible ring
homomorphism is exactly the canonical ZMod.castHom. -/
theorem nativeGK5BWGlobalCompatibleHom_apply
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (x : ZMod (nativeGK5BUFiniteModulus s moduli))
    (i : {i : ι // i ∈ s}) :
    (nativeGK5BWGlobalCompatibleHom s moduli x).1 i =
      (ZMod.castHom (Finset.dvd_lcm i.2) (ZMod (moduli i.1))) x :=
  rfl

/-- Even with modulus zero, equality of ALL genuine local
images forces equality modulo the actual finite LCM. -/
theorem nativeGK5BWGlobalCompatibleHom_injective
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat) :
    Function.Injective (nativeGK5BWGlobalCompatibleHom s moduli) := by
  intro x y h
  obtain ⟨a, rfl⟩ := ZMod.intCast_surjective x
  obtain ⟨b, rfl⟩ := ZMod.intCast_surjective y
  apply (ZMod.intCast_eq_intCast_iff_dvd_sub a b
    (nativeGK5BUFiniteModulus s moduli)).2
  apply Int.natCast_dvd.mpr
  apply Finset.lcm_dvd
  intro i hi
  have hpoint := congrArg
    (fun u : nativeGK5BWCompatibleSubring s moduli =>
      u.1 ⟨i, hi⟩) h
  have hcast : (a : ZMod (moduli i)) = (b : ZMod (moduli i)) := by
    simpa [nativeGK5BWGlobalCompatibleHom,
      nativeGK5BWGlobalLocalHom] using hpoint
  exact Int.natCast_dvd.mp
    ((ZMod.intCast_eq_intCast_iff_dvd_sub a b (moduli i)).1 hcast)

/-- Every compatible local family comes from a genuine
global integer residue, not just from a natural witness.
If the finite LCM is zero, a zero-modulus site supplies
an integer source (allowing negative residues).
Otherwise GK5BV's COMPLETE finite noncoprime Nat CRT
glues the natural representatives at all nonzero sites. -/
theorem nativeGK5BWGlobalCompatibleHom_surjective
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat) :
    Function.Surjective (nativeGK5BWGlobalCompatibleHom s moduli) := by
  classical
  intro y
  by_cases hL : nativeGK5BUFiniteModulus s moduli = 0
  · have hzero : ∃ i ∈ s, moduli i = 0 := by
      exact (Finset.lcm_eq_zero_iff).1 hL
    obtain ⟨i, hi, hmi⟩ := hzero
    let ii : {i : ι // i ∈ s} := ⟨i, hi⟩
    obtain ⟨k, hk⟩ := ZMod.intCast_surjective (y.1 ii)
    refine ⟨(k : ZMod (nativeGK5BUFiniteModulus s moduli)), ?_⟩
    apply Subtype.ext
    funext j
    have hcomp := y.2 ii j
    rw [← hk] at hcomp
    have hlocal : (k : ZMod (moduli j.1)) = y.1 j := by
      simpa [hmi, ZMod.castHom_self] using hcomp
    change (ZMod.castHom (Finset.dvd_lcm j.2) (ZMod (moduli j.1)))
      (k : ZMod (nativeGK5BUFiniteModulus s moduli)) = y.1 j
    simpa only [map_intCast] using hlocal
  · have hnonzero (i : {i : ι // i ∈ s}) :
        moduli i.1 ≠ 0 :=
      (Finset.lcm_ne_zero_iff).1 hL i.1 i.2
    have hval (i : {i : ι // i ∈ s}) :
        (((y.1 i).val : Nat) : ZMod (moduli i.1)) = y.1 i := by
      letI : NeZero (moduli i.1) := ⟨hnonzero i⟩
      exact ZMod.natCast_zmod_val (y.1 i)
    have hpair : nativeGK5BUFinitePairwise
        (Finset.univ : Finset {i : ι // i ∈ s})
        (fun i => moduli i.1) (fun i => (y.1 i).val) := by
      intro i _ j _
      apply (ZMod.natCast_eq_natCast_iff
        (y.1 i).val (y.1 j).val
        (Nat.gcd (moduli i.1) (moduli j.1))).1
      have hc := y.2 i j
      rw [← hval i, ← hval j] at hc
      simpa only [map_natCast] using hc
    obtain ⟨x, hx⟩ :=
      nativeGK5BVFinitePairwise_exists_global
        (Finset.univ : Finset {i : ι // i ∈ s})
        (fun i => moduli i.1) (fun i => (y.1 i).val) hpair
    refine ⟨(x : ZMod (nativeGK5BUFiniteModulus s moduli)), ?_⟩
    apply Subtype.ext
    funext i
    have hxi := hx i (Finset.mem_univ i)
    have hnat : (x : ZMod (moduli i.1)) = y.1 i :=
      ((ZMod.natCast_eq_natCast_iff x (y.1 i).val (moduli i.1)).2 hxi).trans
        (hval i)
    change (ZMod.castHom (Finset.dvd_lcm i.2) (ZMod (moduli i.1)))
      (x : ZMod (nativeGK5BUFiniteModulus s moduli)) = y.1 i
    simpa only [map_natCast] using hnat

/-- COMPLETE ring-level arithmetic CRT descent. This is a
genuine ZMod L ≃+* compatible finite product SUBRING,
including empty covers and arbitrary zero/noncoprime moduli. -/
def nativeGK5BWFiniteCRTRingEquiv
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat) :
    ZMod (nativeGK5BUFiniteModulus s moduli) ≃+*
      nativeGK5BWCompatibleSubring s moduli :=
  RingEquiv.ofBijective (nativeGK5BWGlobalCompatibleHom s moduli)
    ⟨nativeGK5BWGlobalCompatibleHom_injective s moduli,
      nativeGK5BWGlobalCompatibleHom_surjective s moduli⟩

/-- Exact ring-equivalence forward map, with genuine
original local ZMod projections. -/
theorem nativeGK5BWFiniteCRTRingEquiv_apply
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (x : ZMod (nativeGK5BUFiniteModulus s moduli)) :
    nativeGK5BWFiniteCRTRingEquiv s moduli x =
      nativeGK5BWGlobalCompatibleHom s moduli x :=
  rfl

/-- Transport of global ADDITION through every compatible
local residue coordinate is literal coordinate addition. -/
theorem nativeGK5BWFiniteCRTRingEquiv_add
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (x y : ZMod (nativeGK5BUFiniteModulus s moduli))
    (i : {i : ι // i ∈ s}) :
    (nativeGK5BWFiniteCRTRingEquiv s moduli (x + y)).1 i =
      (nativeGK5BWFiniteCRTRingEquiv s moduli x).1 i +
      (nativeGK5BWFiniteCRTRingEquiv s moduli y).1 i := by
  rw [map_add]
  rfl

/-- Transport of global MULTIPLICATION through every
compatible local coordinate is literal multiplication. -/
theorem nativeGK5BWFiniteCRTRingEquiv_mul
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (x y : ZMod (nativeGK5BUFiniteModulus s moduli))
    (i : {i : ι // i ∈ s}) :
    (nativeGK5BWFiniteCRTRingEquiv s moduli (x * y)).1 i =
      (nativeGK5BWFiniteCRTRingEquiv s moduli x).1 i *
      (nativeGK5BWFiniteCRTRingEquiv s moduli y).1 i := by
  rw [map_mul]
  rfl

#print axioms nativeGK5BWGlobalLocalHom_compatible
#print axioms nativeGK5BWGlobalCompatibleHom_apply
#print axioms nativeGK5BWGlobalCompatibleHom_injective
#print axioms nativeGK5BWGlobalCompatibleHom_surjective
#print axioms nativeGK5BWFiniteCRTRingEquiv_apply
#print axioms nativeGK5BWFiniteCRTRingEquiv_add
#print axioms nativeGK5BWFiniteCRTRingEquiv_mul

end
end Kuu.F112.Physical
