import Kuu.F112.PolygonNativeF55P94DK5InterchangeNormalClosure
import Mathlib.Algebra.Group.Subgroup.Basic
import Mathlib.Tactic

/-!
# F112-P94D3D — interchange conjugacy envelope and a genuine Peiffer kernel

The ACTUAL north C60 P94A typed interchange in P94D3B forces the
P/N commutator. P94D3C quotients by its minimal normal closure only.

Here distinguish two normal closures:
* the exact single witnessed P/N kernel from P94D3C;
* the UNIVERSAL ALGEBRAIC commutator envelope for arbitrary ordered
  P92B proof words. This latter envelope is an upper bound on
  interchange-induced word relations, NOT a claimed computation of the
  full source-typed P94A/P94C2 4-cell congruence.

The arbitrary middle-four interchange word defect is the conjugate
of the middle commutator. Explicitly, left vertical whiskering acts
by conjugation, and the normal-closure inclusion N -> FreeAddGroup
forms a genuine (nonabelian) crossed-module certificate with its
Peiffer identity. A Type-valued bridge packages the existing genuine
P94A source four-cell and its exactly computed normal relator.

The single-relation kernel is STRICTLY smaller than the universal
commutator envelope, witnessed by the surviving P/S noncommutation
from P94D3C. Thus no assumption that every P/S commutator is required
by source typing has been made. The global K5 spherical pasting and
independent pentagonator remain open.

No Gray, sorry, admit, new logical axioms or changes to prior roots.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

/-- The generic middle-four group word defect is a conjugate of
the inner interchange commutator, not an assumed abelian identity.
All four words keep their noncommutative order. -/
theorem nativeK5Interchange_word_defect_conjugate
    (a b c d : NativeF55P94CWord) :
    ((a + b) + (c + d)) - ((a + c) + (b + d)) =
      a + ((b + c) - (c + b)) - a := by
  add_group

/-- Algebraic envelope of all ordered interchange commutators.
It is NOT asserted that every pair is realizable by typed F45
horizontal factors in the physical C60 presentation. -/
def nativeK5AllWordInterchangeRelators : Set NativeF55P94CWord :=
  {w | ∃ x y : NativeF55P94CWord, w = (x + y) - (y + x)}

def nativeK5AllWordInterchangeClosure : AddSubgroup NativeF55P94CWord :=
  AddSubgroup.normalClosure nativeK5AllWordInterchangeRelators

instance nativeK5AllWordInterchangeClosure_normal :
    nativeK5AllWordInterchangeClosure.Normal := by
  unfold nativeK5AllWordInterchangeClosure
  infer_instance

theorem nativeK5AllWordInterchange_commutator_mem
    (x y : NativeF55P94CWord) :
    (x + y) - (y + x) ∈ nativeK5AllWordInterchangeClosure := by
  apply AddSubgroup.subset_normalClosure
  exact ⟨x, y, rfl⟩

/-- Every formally shaped middle-four interchange difference
belongs to the envelope, via the actual conjugacy formula. -/
theorem nativeK5AllWordInterchange_defect_mem
    (a b c d : NativeF55P94CWord) :
    ((a + b) + (c + d)) - ((a + c) + (b + d)) ∈
      nativeK5AllWordInterchangeClosure := by
  rw [nativeK5Interchange_word_defect_conjugate]
  have h := nativeK5AllWordInterchange_commutator_mem b c
  have hc :
      a + ((b + c) - (c + b)) + -a ∈
        nativeK5AllWordInterchangeClosure :=
    (inferInstance : nativeK5AllWordInterchangeClosure.Normal).conj_mem
      ((b + c) - (c + b)) h a
  simpa only [sub_eq_add_neg] using hc

/-- The genuine P/N relator is one member of this larger universal
algebraic envelope. -/
theorem nativeK5PNNormalClosure_le_allWordInterchange :
    nativeK5PNNormalClosure ≤ nativeK5AllWordInterchangeClosure := by
  apply AddSubgroup.normalClosure_le_normal
  intro w hw
  have heq : w = nativeK5PNInterchangeRelator := by
    simpa [nativeK5PNRelators] using hw
  subst w
  change (nativeK5PNPentagon + nativeK5PNNaturality) -
      (nativeK5PNNaturality + nativeK5PNPentagon) ∈
        nativeK5AllWordInterchangeClosure
  exact nativeK5AllWordInterchange_commutator_mem _ _

/-- The P/S commutator is in the all-word envelope, but NOT in the
single genuinely witnessed P/N normal closure. This separation
prevents incorrectly promoting P94D3C into an all-4-cell quotient. -/
theorem nativeK5AllWordInterchange_square_mem :
    (nativeK5PNPentagon + nativeK5PNSquare) -
      (nativeK5PNSquare + nativeK5PNPentagon) ∈
        nativeK5AllWordInterchangeClosure :=
  nativeK5AllWordInterchange_commutator_mem _ _

theorem nativeK5PNNormalClosure_ne_allWordInterchange :
    nativeK5PNNormalClosure ≠ nativeK5AllWordInterchangeClosure := by
  intro h
  have hps :
      (nativeK5PNPentagon + nativeK5PNSquare) -
        (nativeK5PNSquare + nativeK5PNPentagon) ∈
          nativeK5PNNormalClosure := by
    rw [h]
    exact nativeK5AllWordInterchange_square_mem
  have heq :
      nativeK5PNCorrectedClass (nativeK5PNPentagon + nativeK5PNSquare) =
        nativeK5PNCorrectedClass (nativeK5PNSquare + nativeK5PNPentagon) :=
    (QuotientAddGroup.eq_iff_sub_mem).2 hps
  exact nativeK5PNCorrected_pentagon_square_noncommute heq

/-- The complete signed F55 shadow, including odd C60 phase,
survives EVERY algebraic interchange commutator. -/
theorem nativeK5AllWordInterchangeClosure_le_shadow_ker :
    nativeK5AllWordInterchangeClosure ≤
      nativeF55P94CWordToShadow.ker := by
  apply AddSubgroup.normalClosure_le_normal
  intro w hw
  rcases hw with ⟨x, y, rfl⟩
  change nativeF55P94CWordToShadow ((x + y) - (y + x)) = 0
  simp only [map_sub, map_add]
  abel

abbrev NativeK5AllWordInterchangeQuotient :=
  NativeF55P94CWord ⧸ nativeK5AllWordInterchangeClosure

def nativeK5AllWordInterchangeShadow :
    NativeK5AllWordInterchangeQuotient →+ KuuNativeF55Shadow :=
  QuotientAddGroup.lift nativeK5AllWordInterchangeClosure
    nativeF55P94CWordToShadow
    nativeK5AllWordInterchangeClosure_le_shadow_ker

/-- Relation module of the FIRST physically witnessed 4-cell.
This subgroup is normal and need NOT be abelian. -/
abbrev NativeK5PNPeifferKernel := nativeK5PNNormalClosure

/-- The boundary map is the faithful inclusion of the exact
4-cell relation module into the freely generated word group. -/
def nativeK5PNPeifferBoundary :
    NativeK5PNPeifferKernel →+ NativeF55P94CWord :=
  nativeK5PNNormalClosure.subtype

/-- Conjugation by an ambient 3-proof word stays in the normal
closure; this is the algebraic image of a 4-cell whiskering. -/
def nativeK5PNPeifferConjugate
    (g : NativeF55P94CWord) (r : NativeK5PNPeifferKernel) :
    NativeK5PNPeifferKernel :=
  ⟨g + (r : NativeF55P94CWord) - g, by
    have h :
        g + (r : NativeF55P94CWord) + -g ∈ nativeK5PNNormalClosure :=
      (inferInstance : nativeK5PNNormalClosure.Normal).conj_mem
        (r : NativeF55P94CWord) r.property g
    simpa only [sub_eq_add_neg] using h⟩

theorem nativeK5PNPeifferConjugate_zero
    (g : NativeF55P94CWord) :
    nativeK5PNPeifferConjugate g 0 = 0 := by
  apply Subtype.ext
  change g + (0 : NativeF55P94CWord) - g = 0
  add_group

theorem nativeK5PNPeifferConjugate_add
    (g : NativeF55P94CWord)
    (r s : NativeK5PNPeifferKernel) :
    nativeK5PNPeifferConjugate g (r + s) =
      nativeK5PNPeifferConjugate g r +
        nativeK5PNPeifferConjugate g s := by
  apply Subtype.ext
  change g + ((r : NativeF55P94CWord) + (s : NativeF55P94CWord)) - g =
    (g + (r : NativeF55P94CWord) - g) +
      (g + (s : NativeF55P94CWord) - g)
  add_group

theorem nativeK5PNPeifferConjugate_identity
    (r : NativeK5PNPeifferKernel) :
    nativeK5PNPeifferConjugate 0 r = r := by
  apply Subtype.ext
  change (0 : NativeF55P94CWord) + r - 0 = r
  add_group

theorem nativeK5PNPeifferConjugate_comp
    (g h : NativeF55P94CWord)
    (r : NativeK5PNPeifferKernel) :
    nativeK5PNPeifferConjugate (g + h) r =
      nativeK5PNPeifferConjugate g (nativeK5PNPeifferConjugate h r) := by
  apply Subtype.ext
  change (g + h) + (r : NativeF55P94CWord) - (g + h) =
    g + (h + (r : NativeF55P94CWord) - h) - g
  add_group

/-- Crossed-module boundary equivariance is an ACTUAL equality
in the noncommutative free group. -/
theorem nativeK5PNPeifferBoundary_equivariant
    (g : NativeF55P94CWord)
    (r : NativeK5PNPeifferKernel) :
    nativeK5PNPeifferBoundary (nativeK5PNPeifferConjugate g r) =
      g + nativeK5PNPeifferBoundary r - g := rfl

/-- Genuine Peiffer identity for the normal inclusion N -> F:
action by the boundary of r coincides with internal conjugation
by r. It is NOT a claim that P94A has all possible 4-cells. -/
theorem nativeK5PNPeiffer_identity
    (r s : NativeK5PNPeifferKernel) :
    nativeK5PNPeifferConjugate (nativeK5PNPeifferBoundary r) s =
      r + s - r := by
  apply Subtype.ext
  rfl

/-- Proof-relevant crossed-module laws, all established using
mathlib AddSubgroup normal closure, actual action and inclusion. -/
structure NativeK5PNCrossedModuleData where
  boundary : NativeK5PNPeifferKernel →+ NativeF55P94CWord
  act : NativeF55P94CWord → NativeK5PNPeifferKernel → NativeK5PNPeifferKernel
  act_identity : ∀ r, act 0 r = r
  act_comp : ∀ g h r, act (g + h) r = act g (act h r)
  act_zero : ∀ g, act g 0 = 0
  act_add : ∀ g r s, act g (r + s) = act g r + act g s
  boundary_equivariant :
    ∀ g r, boundary (act g r) = g + boundary r - g
  peiffer : ∀ r s, act (boundary r) s = r + s - r

def nativeK5PNCrossedModule : NativeK5PNCrossedModuleData :=
  { boundary := nativeK5PNPeifferBoundary
    act := nativeK5PNPeifferConjugate
    act_identity := nativeK5PNPeifferConjugate_identity
    act_comp := nativeK5PNPeifferConjugate_comp
    act_zero := nativeK5PNPeifferConjugate_zero
    act_add := nativeK5PNPeifferConjugate_add
    boundary_equivariant := nativeK5PNPeifferBoundary_equivariant
    peiffer := nativeK5PNPeiffer_identity }

/-- The selected Type-valued 4-cell relator is an actual MEMBER of
the normal relation module, not merely an equality of shadows. -/
def nativeK5PNFourCellRelator : NativeK5PNPeifferKernel :=
  ⟨nativeK5PNInterchangeRelator, nativeK5PNInterchangeRelator_mem_normal⟩

/-- A Type-valued source certificate couples the ORIGINAL typed
P94A 4-cell to its exact noncommutative crossed-module boundary.
The algebraic Peiffer law is proved for this selected kernel;
no global K5 pentagonator filler is thereby asserted. -/
structure NorthK5PNFourCellPeifferBridge where
  sourceFourCell :
    NativeF55P94UnitFourCell
      (nativeK5InterchangeFirstPasting
        northK5OriginalPentagonPSource northK5OriginalNaturalityNSource)
      (nativeK5InterchangeSecondPasting
        northK5OriginalPentagonPSource northK5OriginalNaturalityNSource)
  wordBoundary :
    (nativeK5InterchangeFirstPasting
        northK5OriginalPentagonPSource
        northK5OriginalNaturalityNSource).p94cGroupWord -
      (nativeK5InterchangeSecondPasting
        northK5OriginalPentagonPSource
        northK5OriginalNaturalityNSource).p94cGroupWord =
      nativeK5PNPeifferBoundary nativeK5PNFourCellRelator

def northK5PNFourCellPeifferBridge : NorthK5PNFourCellPeifferBridge :=
  { sourceFourCell := northK5P94AInterchange_actual_fourCell
    wordBoundary := northK5P94AInterchange_actual_relator }

theorem nativeK5PNFourCell_whisker_mem
    (g : NativeF55P94CWord) :
    g + nativeK5PNInterchangeRelator - g ∈ nativeK5PNNormalClosure := by
  have h := (inferInstance : nativeK5PNNormalClosure.Normal).conj_mem
    nativeK5PNInterchangeRelator nativeK5PNInterchangeRelator_mem_normal g
  simpa only [sub_eq_add_neg] using h

#print axioms nativeK5Interchange_word_defect_conjugate
#print axioms nativeK5AllWordInterchange_defect_mem
#print axioms nativeK5PNNormalClosure_le_allWordInterchange
#print axioms nativeK5AllWordInterchange_square_mem
#print axioms nativeK5PNNormalClosure_ne_allWordInterchange
#print axioms nativeK5AllWordInterchangeClosure_le_shadow_ker
#print axioms nativeK5AllWordInterchangeShadow
#print axioms nativeK5PNPeifferBoundary
#print axioms nativeK5PNPeifferConjugate
#print axioms nativeK5PNPeifferConjugate_add
#print axioms nativeK5PNPeifferConjugate_comp
#print axioms nativeK5PNPeifferBoundary_equivariant
#print axioms nativeK5PNPeiffer_identity
#print axioms nativeK5PNCrossedModule
#print axioms northK5PNFourCellPeifferBridge
#print axioms nativeK5PNFourCell_whisker_mem

end
end Kuu.F112.Physical
