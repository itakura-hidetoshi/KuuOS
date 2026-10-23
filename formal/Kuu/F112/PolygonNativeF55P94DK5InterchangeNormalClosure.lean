import Kuu.F112.PolygonNativeF55P94DK5InterchangeWordNoDescent
import Mathlib.Algebra.Group.Subgroup.Basic
import Mathlib.GroupTheory.QuotientGroup.Defs
import Mathlib.Tactic

/-!
# F112-P94D3C — first genuine interchange relator and normal-closure quotient

P94D3B proves that an ACTUAL original five-stage C60 F55 pentagon
P and an explicitly adjoined P92B associator-naturality cell N can be
pasted into two P94A 3-proofs, related by an EXISTING Type-valued
4-cell, whose P94C3 ordered words are P+N versus N+P. The raw word
therefore cannot descend to the P94A 4-cell quotient.

Here do NOT force the entire source free group to be commutative.
Instead impose exactly the normal closure of the ONE nontrivial
generator commutator P+N-(N+P) known to be forced by that genuine
interchange. In this independently selected algebraic quotient:

* P and N commute and the raw word map is not injective;
* the ORIGINAL complete F55 signed/odd shadow still descends;
* the P94C3 S3 observer which sends N to 0 still descends;
* original pentagon P and original six-sector square S still DO NOT
  commute, witnessed by true S3 transpositions;
* the normal closure is minimal among all normal subgroups killing
  the particular witnessed interchange commutator.

These are precisely stated GROUP-relator facts. This is NOT a proof
that ALL P94A/P94C2 four-cell relations are killed by this single
normal closure, nor a crossed module, Peiffer law or global K5
pentagonator filling. No Gray, sorry, admit or new logical axiom.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

/-- The two original independent F55/P92B free-group letters. -/
def nativeK5PNPentagon : NativeF55P94CWord :=
  FreeAddGroup.of .pentagon

def nativeK5PNNaturality : NativeF55P94CWord :=
  FreeAddGroup.of .assocNaturality

def nativeK5PNSquare : NativeF55P94CWord :=
  FreeAddGroup.of .square

/-- The exact ordered commutator measured at the ACTUAL P94D3B
C60 interchange four-cell. It is nonzero in the raw free group. -/
def nativeK5PNInterchangeRelator : NativeF55P94CWord :=
  (nativeK5PNPentagon + nativeK5PNNaturality) -
    (nativeK5PNNaturality + nativeK5PNPentagon)

/-- Only this ONE explicitly witnessed interchange word is imposed.
No unrelated four-dimensional coherence law is smuggled in. -/
def nativeK5PNRelators : Set NativeF55P94CWord :=
  {nativeK5PNInterchangeRelator}

/-- The smallest normal additive subgroup containing the selected
genuine interchange relation, using the pinned mathlib kernel. -/
def nativeK5PNNormalClosure : AddSubgroup NativeF55P94CWord :=
  AddSubgroup.normalClosure nativeK5PNRelators

/-- Expose the normality of the explicitly named normal closure to
mathlib's quotient-group typeclass search. A named def is otherwise
opaque to synthesis, even though its unfolding is normal. -/
instance nativeK5PNNormalClosure_normal : nativeK5PNNormalClosure.Normal := by
  unfold nativeK5PNNormalClosure
  infer_instance

/-- The exact original physical 4-cell witnesses this relator:
its SOURCE 3-proof ordered word difference is the generator above. -/
theorem northK5P94AInterchange_actual_relator :
    (nativeK5InterchangeFirstPasting
        northK5OriginalPentagonPSource
        northK5OriginalNaturalityNSource).p94cGroupWord -
    (nativeK5InterchangeSecondPasting
        northK5OriginalPentagonPSource
        northK5OriginalNaturalityNSource).p94cGroupWord =
      nativeK5PNInterchangeRelator := by
  rw [nativeK5InterchangeFirstWord, nativeK5InterchangeSecondWord,
    northK5OriginalPentagonPSource_groupWord,
    northK5OriginalNaturalityNSource_groupWord]
  rfl

/-- The genuine 4-cell witness is still present; the chosen
normal-closure generator comes from this actual typed source. -/
def northK5P94AInterchange_actual_fourCell :
    NativeF55P94UnitFourCell
      (nativeK5InterchangeFirstPasting
        northK5OriginalPentagonPSource
        northK5OriginalNaturalityNSource)
      (nativeK5InterchangeSecondPasting
        northK5OriginalPentagonPSource
        northK5OriginalNaturalityNSource) :=
  nativeK5InterchangeFourCell
    northK5OriginalPentagonPSource northK5OriginalNaturalityNSource

theorem nativeK5PNInterchangeRelator_mem_normal :
    nativeK5PNInterchangeRelator ∈ nativeK5PNNormalClosure := by
  apply AddSubgroup.subset_normalClosure
  simp [nativeK5PNRelators]

/-- A noncommutative quotient group implementing only the selected
four-cell's forced interchange relation. -/
abbrev NativeK5PNCorrectedWord :=
  NativeF55P94CWord ⧸ nativeK5PNNormalClosure

def nativeK5PNCorrectedClass :
    NativeF55P94CWord →+ NativeK5PNCorrectedWord :=
  QuotientAddGroup.mk' nativeK5PNNormalClosure

/-- First actual exchange generator is killed in the corrected
noncommutative group, unlike the original free group. -/
theorem nativeK5PNCorrected_interchange :
    nativeK5PNCorrectedClass
        (nativeK5PNPentagon + nativeK5PNNaturality) =
      nativeK5PNCorrectedClass
        (nativeK5PNNaturality + nativeK5PNPentagon) := by
  apply (QuotientAddGroup.eq_iff_sub_mem).2
  exact nativeK5PNInterchangeRelator_mem_normal

/-- The old noncommutative free word observer really loses
information under this one proven interchange relation. -/
theorem nativeK5PNCorrected_not_injective :
    ¬ Function.Injective nativeK5PNCorrectedClass := by
  intro h
  apply nativeK5Word_pentagon_naturality_noncommute
  exact h nativeK5PNCorrected_interchange

/-- A complete necessary obstruction to any alternate normal
quotient respecting this ONE witnessed P94A interchange: its kernel
must contain our commutator's normal closure. -/
theorem nativeK5PNNormalClosure_minimal
    (H : AddSubgroup NativeF55P94CWord) [H.Normal]
    (h : (nativeK5PNPentagon + nativeK5PNNaturality :
        NativeF55P94CWord ⧸ H) =
      (nativeK5PNNaturality + nativeK5PNPentagon :
        NativeF55P94CWord ⧸ H)) :
    nativeK5PNNormalClosure ≤ H := by
  apply AddSubgroup.normalClosure_le_normal
  intro w hw
  have heq : w = nativeK5PNInterchangeRelator := by
    simpa [nativeK5PNRelators] using hw
  subst w
  exact (QuotientAddGroup.eq_iff_sub_mem).1 h

/-- The entire ORIGINAL (signed pentagon, signed exchange square,
genuine odd C60 phase) shadow vanishes on the actual relator. -/
theorem nativeK5PNInterchangeRelator_shadow_zero :
    nativeF55P94CWordToShadow nativeK5PNInterchangeRelator = 0 := by
  simp only [nativeK5PNInterchangeRelator, map_sub]
  apply sub_eq_zero.mpr
  simpa only [nativeK5PNPentagon, nativeK5PNNaturality] using
    nativeK5Word_pentagon_naturality_shadow_commute

/-- The honest smallest normal relator subgroup lies in the full
original physical shadow kernel, not merely its first charge. -/
theorem nativeK5PNNormalClosure_le_shadow_ker :
    nativeK5PNNormalClosure ≤ nativeF55P94CWordToShadow.ker := by
  apply AddSubgroup.normalClosure_le_normal
  intro w hw
  have heq : w = nativeK5PNInterchangeRelator := by
    simpa [nativeK5PNRelators] using hw
  subst w
  change nativeF55P94CWordToShadow nativeK5PNInterchangeRelator = 0
  exact nativeK5PNInterchangeRelator_shadow_zero

/-- Full original F55 observation genuinely DESCENDS through the
NEW minimal algebraic normal quotient. This does not assert descent
of the raw word or factorization through every P94A 4-cell relation. -/
def nativeK5PNCorrectedShadow :
    NativeK5PNCorrectedWord →+ KuuNativeF55Shadow :=
  QuotientAddGroup.lift nativeK5PNNormalClosure
    nativeF55P94CWordToShadow nativeK5PNNormalClosure_le_shadow_ker

theorem nativeK5PNCorrectedShadow_spec (w : NativeF55P94CWord) :
    nativeK5PNCorrectedShadow (nativeK5PNCorrectedClass w) =
      nativeF55P94CWordToShadow w := by
  exact QuotientAddGroup.lift_mk' nativeK5PNNormalClosure nativeK5PNNormalClosure_le_shadow_ker w

/-- P94C3's second S3 observer kills the NEW naturality word,
and hence the required P/N commutator, retaining original P/S
noncommutativity. -/
theorem nativeK5PNInterchangeRelator_S3_zero :
    nativeF55P94CWordToS3 nativeK5PNInterchangeRelator = 0 := by
  simp only [nativeK5PNInterchangeRelator, map_sub]
  apply sub_eq_zero.mpr
  simp [nativeK5PNPentagon, nativeK5PNNaturality,
    nativeF55P94CWordToS3, map_add]

theorem nativeK5PNNormalClosure_le_S3_ker :
    nativeK5PNNormalClosure ≤ nativeF55P94CWordToS3.ker := by
  apply AddSubgroup.normalClosure_le_normal
  intro w hw
  have heq : w = nativeK5PNInterchangeRelator := by
    simpa [nativeK5PNRelators] using hw
  subst w
  change nativeF55P94CWordToS3 nativeK5PNInterchangeRelator = 0
  exact nativeK5PNInterchangeRelator_S3_zero

def nativeK5PNCorrectedS3 :
    NativeK5PNCorrectedWord →+ Additive (Equiv.Perm (Fin 3)) :=
  QuotientAddGroup.lift nativeK5PNNormalClosure
    nativeF55P94CWordToS3 nativeK5PNNormalClosure_le_S3_ker

theorem nativeK5PNCorrectedS3_spec (w : NativeF55P94CWord) :
    nativeK5PNCorrectedS3 (nativeK5PNCorrectedClass w) =
      nativeF55P94CWordToS3 w := by
  exact QuotientAddGroup.lift_mk' nativeK5PNNormalClosure nativeK5PNNormalClosure_le_S3_ker w

/-- P and the ORIGINAL odd-phase six-sector S do not commute even
AFTER imposing the genuine P94A P/N interchange relation. The
corrected quotient is therefore NOT the forced abelianization. -/
theorem nativeK5PNCorrected_pentagon_square_noncommute :
    nativeK5PNCorrectedClass (nativeK5PNPentagon + nativeK5PNSquare) ≠
      nativeK5PNCorrectedClass (nativeK5PNSquare + nativeK5PNPentagon) := by
  intro h
  have hh := congrArg nativeK5PNCorrectedS3 h
  rw [nativeK5PNCorrectedS3_spec, nativeK5PNCorrectedS3_spec] at hh
  simp only [map_add, nativeK5PNPentagon, nativeK5PNSquare,
    FreeAddGroup.lift_apply_of] at hh
  change
    Equiv.swap (0 : Fin 3) (1 : Fin 3) *
      Equiv.swap (1 : Fin 3) (2 : Fin 3) =
    Equiv.swap (1 : Fin 3) (2 : Fin 3) *
      Equiv.swap (0 : Fin 3) (1 : Fin 3) at hh
  exact (by decide :
    Equiv.swap (0 : Fin 3) (1 : Fin 3) *
      Equiv.swap (1 : Fin 3) (2 : Fin 3) ≠
    Equiv.swap (1 : Fin 3) (2 : Fin 3) *
      Equiv.swap (0 : Fin 3) (1 : Fin 3)) hh

#print axioms nativeK5PNInterchangeRelator
#print axioms northK5P94AInterchange_actual_relator
#print axioms northK5P94AInterchange_actual_fourCell
#print axioms nativeK5PNInterchangeRelator_mem_normal
#print axioms NativeK5PNCorrectedWord
#print axioms nativeK5PNCorrected_interchange
#print axioms nativeK5PNCorrected_not_injective
#print axioms nativeK5PNNormalClosure_minimal
#print axioms nativeK5PNInterchangeRelator_shadow_zero
#print axioms nativeK5PNNormalClosure_le_shadow_ker
#print axioms nativeK5PNCorrectedShadow_spec
#print axioms nativeK5PNInterchangeRelator_S3_zero
#print axioms nativeK5PNNormalClosure_le_S3_ker
#print axioms nativeK5PNCorrectedS3_spec
#print axioms nativeK5PNCorrected_pentagon_square_noncommute

end
end Kuu.F112.Physical
