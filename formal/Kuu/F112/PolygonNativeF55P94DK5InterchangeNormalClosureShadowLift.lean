import Kuu.F112.PolygonNativeF55P94DK5InterchangeWordNoDescent
import Mathlib.Algebra.Group.Subgroup.Basic
import Mathlib.Algebra.Group.Subgroup.Ker
import Mathlib.GroupTheory.QuotientGroup.Defs
import Mathlib.Tactic.AddGroup
import Mathlib.Tactic

/-!
# F112-P94D4 — normal-closure response to the genuine K5 interchange obstruction

P94D3B proved that an EXISTING P94A Type-valued 4-cell identifies the
two genuinely constructed noncommuting source word orders P+N and N+P,
so the ORIGINAL pre-four-cell free-group word cannot descend as-is.

This file forms exactly the MINIMAL NORMAL additive subgroup generated
by their nontrivial commutator. In the corresponding quotient (a
one-dimensional truncation of that relation, not a replacement for
Type-valued 4-cell data), P and N commute.

CRUCIALLY, the full original signed F55 (pentagon, square, odd C60
phase) shadow annihilates this new relation and hence DESCENDS as an
AddMonoidHom to the quotient, preserving all three original charges.
This proves a mathematical compatibility condition for the selected
presentation; it is not a construction of global K5 spherical
3-pasting, independent 4D pentagonator, crossed-module Peiffer lifts,
or strict 3/n-category coherence.

No Gray, no new logical axioms, no sorry/admit, old proof roots retained.
-/

namespace Kuu.F112.Physical

set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

/-- The two already-verified NONCOMMUTING authentic P92B source tags
on the original P94C3 free additive group. -/
def nativeK5PentagonGeneratorWord : NativeF55P94CWord :=
  FreeAddGroup.of .pentagon

def nativeK5NaturalityGeneratorWord : NativeF55P94CWord :=
  FreeAddGroup.of .assocNaturality

/-- Nonabelian commutator of an original F55 pentagon and the NEW
P92B associator-naturality proof letter. Neither word order is
silently identified in the free group. -/
def nativeK5InterchangeCommutatorWord : NativeF55P94CWord :=
  nativeK5PentagonGeneratorWord + nativeK5NaturalityGeneratorWord +
    (-nativeK5PentagonGeneratorWord) +
    (-nativeK5NaturalityGeneratorWord)

/-- The genuine P94D3B S3 finite receiver rules out this commutator
being zero PRIOR to the chosen 4-cell congruence. -/
theorem nativeK5InterchangeCommutatorWord_nonzero :
    nativeK5InterchangeCommutatorWord ≠
      (0 : NativeF55P94CWord) := by
  intro h
  have hcomm :
      nativeK5PentagonGeneratorWord + nativeK5NaturalityGeneratorWord =
      nativeK5NaturalityGeneratorWord + nativeK5PentagonGeneratorWord := by
    calc
      nativeK5PentagonGeneratorWord + nativeK5NaturalityGeneratorWord =
          nativeK5InterchangeCommutatorWord +
            (nativeK5NaturalityGeneratorWord + nativeK5PentagonGeneratorWord) := by
            unfold nativeK5InterchangeCommutatorWord
            add_group
      _ = (0 : NativeF55P94CWord) +
            (nativeK5NaturalityGeneratorWord + nativeK5PentagonGeneratorWord) := by
              rw [h]
      _ = nativeK5NaturalityGeneratorWord + nativeK5PentagonGeneratorWord := by
            simp
  exact nativeK5Word_pentagon_naturality_noncommute
    (by simpa [nativeK5PentagonGeneratorWord,
       nativeK5NaturalityGeneratorWord] using hcomm)

/-- The COMPLETE original F55 abelian shadow vanishes on this
nontrivial NONABELIAN commutator. Necessary but not by itself
sufficient to manufacture any 4-dimensional witness. -/
theorem nativeK5InterchangeCommutatorWord_shadow_zero :
    nativeF55P94CWordToShadow nativeK5InterchangeCommutatorWord =
      (0 : KuuNativeF55Shadow) := by
  unfold nativeK5InterchangeCommutatorWord
  simp only [map_add, map_neg]
  abel

/-- Smallest normal subgroup containing the ACTUALLY WITNESSED
P94A interchange relator. This is one chosen, minimal normal-closure
presentation, NOT the full set of independent K5 4-cell coherences. -/
def nativeK5InterchangeNormalClosure : AddSubgroup NativeF55P94CWord :=
  AddSubgroup.normalClosure {nativeK5InterchangeCommutatorWord}

theorem nativeK5InterchangeRelator_mem_normalClosure :
    nativeK5InterchangeCommutatorWord ∈
      nativeK5InterchangeNormalClosure := by
  unfold nativeK5InterchangeNormalClosure
  apply AddSubgroup.subset_normalClosure
  rfl

/-- Universal minimality of this normal closure among normal
additive subgroups containing the authentic interchange relator. -/
theorem nativeK5InterchangeNormalClosure_minimal
    (N : AddSubgroup NativeF55P94CWord) [N.Normal]
    (hN : nativeK5InterchangeCommutatorWord ∈ N) :
    nativeK5InterchangeNormalClosure ≤ N := by
  unfold nativeK5InterchangeNormalClosure
  apply AddSubgroup.normalClosure_le_normal
  intro z hz
  have heq : z = nativeK5InterchangeCommutatorWord := by
    simpa only [Set.mem_singleton_iff] using hz
  subst z
  exact hN

/-- The ORIGINAL signed/odd F55 shadow kills every conjugate of
the authentic P/N interchange relator: its full kernel is normal.
This yields a mathematically genuine descent condition. -/
theorem nativeK5InterchangeNormalClosure_le_shadowKernel :
    nativeK5InterchangeNormalClosure ≤
      nativeF55P94CWordToShadow.ker := by
  apply nativeK5InterchangeNormalClosure_minimal
    nativeF55P94CWordToShadow.ker
  change nativeF55P94CWordToShadow nativeK5InterchangeCommutatorWord = 0
  exact nativeK5InterchangeCommutatorWord_shadow_zero

/-- Selected NONABELIAN 1-truncation by the necessary interchange
commutator. This does NOT erase the separate 4-cell witness from
the original Type-valued presentation. -/
abbrev NativeK5InterchangeWordQuotient :=
  NativeF55P94CWord ⧸ nativeK5InterchangeNormalClosure

/-- Canonical group homomorphism from original free group to the
minimal interchange quotient. -/
def nativeK5InterchangeWordQuotientMk :
    NativeF55P94CWord →+ NativeK5InterchangeWordQuotient :=
  QuotientAddGroup.mk' nativeK5InterchangeNormalClosure

/-- The nonzero free-group commutator is zero in the selected
normal-closure quotient, precisely because an independent
P94A Type-valued interchange 4-cell already witnessed its relation. -/
theorem nativeK5InterchangeWordRelator_quotient_zero :
    nativeK5InterchangeWordQuotientMk
      nativeK5InterchangeCommutatorWord = 0 := by
  change
    ((nativeK5InterchangeCommutatorWord : NativeF55P94CWord) :
      NativeK5InterchangeWordQuotient) =
    ((0 : NativeF55P94CWord) : NativeK5InterchangeWordQuotient)
  apply (QuotientAddGroup.eq).2
  simpa using nativeK5InterchangeNormalClosure.neg_mem
    nativeK5InterchangeRelator_mem_normalClosure

/-- The necessary P/N interchange relation is truly imposed in
this normal-closure quotient. This uses NONCOMMUTATIVE group rules,
not a false \`abel\` tactic on the original free group. -/
theorem nativeK5InterchangeWordQuotient_pentagon_naturality_commute :
    nativeK5InterchangeWordQuotientMk nativeK5PentagonGeneratorWord +
        nativeK5InterchangeWordQuotientMk nativeK5NaturalityGeneratorWord =
    nativeK5InterchangeWordQuotientMk nativeK5NaturalityGeneratorWord +
        nativeK5InterchangeWordQuotientMk nativeK5PentagonGeneratorWord := by
  have hr :
      nativeK5InterchangeWordQuotientMk nativeK5PentagonGeneratorWord +
          nativeK5InterchangeWordQuotientMk nativeK5NaturalityGeneratorWord +
        (-nativeK5InterchangeWordQuotientMk nativeK5PentagonGeneratorWord) +
        (-nativeK5InterchangeWordQuotientMk nativeK5NaturalityGeneratorWord) =
          (0 : NativeK5InterchangeWordQuotient) := by
    simpa only [nativeK5InterchangeCommutatorWord,
      map_add, map_neg] using
      nativeK5InterchangeWordRelator_quotient_zero
  calc
    nativeK5InterchangeWordQuotientMk nativeK5PentagonGeneratorWord +
        nativeK5InterchangeWordQuotientMk nativeK5NaturalityGeneratorWord =
      (nativeK5InterchangeWordQuotientMk nativeK5PentagonGeneratorWord +
          nativeK5InterchangeWordQuotientMk nativeK5NaturalityGeneratorWord +
        (-nativeK5InterchangeWordQuotientMk nativeK5PentagonGeneratorWord) +
        (-nativeK5InterchangeWordQuotientMk nativeK5NaturalityGeneratorWord)) +
        (nativeK5InterchangeWordQuotientMk nativeK5NaturalityGeneratorWord +
          nativeK5InterchangeWordQuotientMk nativeK5PentagonGeneratorWord) := by
            add_group
    _ = (0 : NativeK5InterchangeWordQuotient) +
        (nativeK5InterchangeWordQuotientMk nativeK5NaturalityGeneratorWord +
          nativeK5InterchangeWordQuotientMk nativeK5PentagonGeneratorWord) := by
            rw [hr]
    _ = nativeK5InterchangeWordQuotientMk nativeK5NaturalityGeneratorWord +
        nativeK5InterchangeWordQuotientMk nativeK5PentagonGeneratorWord := by
          simp

/-- The ENTIRE original F55 three-coordinate shadow descends,
homomorphically, through the minimal normal interchange quotient.
No pentagon charge, square charge or odd C60 parity is discarded. -/
def nativeK5InterchangeWordToFullShadow :
    NativeK5InterchangeWordQuotient →+ KuuNativeF55Shadow :=
  QuotientAddGroup.lift nativeK5InterchangeNormalClosure
    nativeF55P94CWordToShadow
    nativeK5InterchangeNormalClosure_le_shadowKernel

theorem nativeK5InterchangeWordToFullShadow_spec
    (word : NativeF55P94CWord) :
    nativeK5InterchangeWordToFullShadow
      (nativeK5InterchangeWordQuotientMk word) =
      nativeF55P94CWordToShadow word := by
  simp [nativeK5InterchangeWordToFullShadow,
    nativeK5InterchangeWordQuotientMk]

/-- Existing genuinely nonzero C60 odd phase survives the new
normal relation on the square generator, as a formal symbolic
specialization of the proved full shadow map. -/
theorem nativeK5InterchangeWord_square_phase_preserved :
    (nativeK5InterchangeWordToFullShadow
      (nativeK5InterchangeWordQuotientMk
        (FreeAddGroup.of .square : NativeF55P94CWord))).2 =
        (1 : ZMod 2) := by
  rw [nativeK5InterchangeWordToFullShadow_spec]
  rfl

/-- The original nonzero F55 pentagon integer is also still
visible, despite imposing only the missing horizontal interchange
word relation. -/
theorem nativeK5InterchangeWord_pentagon_charge_preserved :
    (nativeK5InterchangeWordToFullShadow
      (nativeK5InterchangeWordQuotientMk
        (FreeAddGroup.of .pentagon : NativeF55P94CWord))).1.1 =
        (1 : Int) := by
  rw [nativeK5InterchangeWordToFullShadow_spec]
  rfl

#print axioms nativeK5InterchangeCommutatorWord_nonzero
#print axioms nativeK5InterchangeCommutatorWord_shadow_zero
#print axioms nativeK5InterchangeNormalClosure
#print axioms nativeK5InterchangeRelator_mem_normalClosure
#print axioms nativeK5InterchangeNormalClosure_minimal
#print axioms nativeK5InterchangeNormalClosure_le_shadowKernel
#print axioms NativeK5InterchangeWordQuotient
#print axioms nativeK5InterchangeWordQuotientMk
#print axioms nativeK5InterchangeWordRelator_quotient_zero
#print axioms nativeK5InterchangeWordQuotient_pentagon_naturality_commute
#print axioms nativeK5InterchangeWordToFullShadow
#print axioms nativeK5InterchangeWordToFullShadow_spec
#print axioms nativeK5InterchangeWord_square_phase_preserved
#print axioms nativeK5InterchangeWord_pentagon_charge_preserved

end
end Kuu.F112.Physical
