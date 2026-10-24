import Kuu.F112.PolygonNativeF55P94DK5ReorientedTypedNineCycle
import Kuu.F112.PolygonNativeF55P94DK5ShellingNoncommutativeGap
import Mathlib.Tactic

/-!
# F112-P94D3T — exact genuine Type-valued nine-cycle pentagonator boundary

D3S supplies an ACTUAL nine-face Type-valued 3-cell loop in the
distinct structural P92B extension, with noncommutative word
N=3 and old F55 full shadow zero. This is the reoriented source,
NOT the historical formal shelling word W with N=1.

First define a genuinely dependent, additional 4-cell GENERATOR
on that proved source boundary in a separate Type-valued grammar.
Declaring this freely generated 4-cell is not a coherence proof and
does not retrospectively make it a historical P94A/P94C2 4-cell.

Then construct the corresponding exact normal-closure word kernel,
show it strictly enlarges the genuinely typed old-four-cell kernel
and preserves the old F55 signed/odd shadow, whereas integer N
cannot descend. At the ALGEBRAIC crossed-module layer, mathlib
normality yields a fully proven conjugation action, boundary
equivariance and Peiffer identity, with exact noncommutative order.

These are TWO DIFFERENT levels of evidence: algebraic Peiffer
for the independent relator kernel IS proved, while proof-relevant
4D pentagonator whiskering/interchange coherence in the new
Type-valued four-cell grammar is NOT proved or assumed here.

No Gray, sorry/admit, added logical axioms, altered C60 geometry,
or loss of the 107 retained public proof roots.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

section FiveNativeStages

variable {p : Polygon} {a b : D} {x y : E}
variable {n₁ n₂ n₃ n₄ n₅ m₁ m₂ m₃ m₄ m₅ : Nat}
variable {p₀ p₁ p₂ p₃ p₄ p₅ : KuuNativeBlocks a b}
variable {q₀ q₁ q₂ q₃ q₄ q₅ : KuuNativeBlocks x y}
variable
  (t1 : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁)
  (t2 : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂)
  (t3 : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃)
  (t4 : KuuNativeF45Tree p n₄ m₄ p₃ q₃ p₄ q₄)
  (t5 : KuuNativeF45Tree p n₅ m₅ p₄ q₄ p₅ q₅)

/-- The zero-group-word identity 3-cell at the genuinely typed
global basepoint, NOT identified with the nine-face pasting. -/
def nativeK5ReorientedStructuralIdentity :
    NativeF55StructuralComparison p
      (nativeK5TypedGlobalF54Route t1 t2 t3 t4 t5 0)
      (nativeK5TypedGlobalF54Route t1 t2 t3 t4 t5 0) :=
  .structural (.refl (nativeK5TypedGlobalF54Route t1 t2 t3 t4 t5 0))

/-- A NEW distinct dependent 4D presentation: its generator has
the ACTUALLY CONSTRUCTED D3S nine-face global Type-valued boundary.
Not an old P94A four-cell and not a proof of Peiffer coherence. -/
inductive NativeK5ReorientedIndependentPentagonator :
    NativeF55StructuralComparison p
      (nativeK5TypedGlobalF54Route t1 t2 t3 t4 t5 0)
      (nativeK5TypedGlobalF54Route t1 t2 t3 t4 t5 0) →
    NativeF55StructuralComparison p
      (nativeK5TypedGlobalF54Route t1 t2 t3 t4 t5 0)
      (nativeK5TypedGlobalF54Route t1 t2 t3 t4 t5 0) →
      Type (max (max uD uE) (max vD vE)) where
  | generator :
      NativeK5ReorientedIndependentPentagonator
        (nativeK5NineReorientedExtendedCycle t1 t2 t3 t4 t5)
        (nativeK5ReorientedStructuralIdentity t1 t2 t3 t4 t5)

/-- The new 4D syntax has one explicit, genuinely typed primitive
with exactly the source boundaries just proved in D3S. -/
def nativeK5ReorientedIndependentPentagonator :
    NativeK5ReorientedIndependentPentagonator t1 t2 t3 t4 t5
      (nativeK5NineReorientedExtendedCycle t1 t2 t3 t4 t5)
      (nativeK5ReorientedStructuralIdentity t1 t2 t3 t4 t5) :=
  .generator

/-- The minimal independent NORMAL word-relator module adjoining
the exact proven nine-face group word to the old typed kernel.
The full noncommutative word, not its shadow, is the new relator. -/
abbrev NativeK5ReorientedPentagonatorKernel :=
  nativeK5PentagonatorWordNormalClosure D E
    (nativeK5NineReorientedWord t1 t2 t3 t4 t5)

/-- The actual, independently chosen +3 Type-valued source boundary
is an explicit MEMBER of this independent normal relator module. -/
def nativeK5ReorientedPentagonatorRelator :
    NativeK5ReorientedPentagonatorKernel t1 t2 t3 t4 t5 :=
  ⟨nativeK5NineReorientedWord t1 t2 t3 t4 t5,
    nativeK5PentagonatorWord_mem (D := D) (E := E)
      (nativeK5NineReorientedWord t1 t2 t3 t4 t5)⟩

/-- Inclusion of ALL genuinely typed old P94A four-cell relations
into the independent pentagonator normal kernel. -/
theorem nativeK5P94ATyped_le_reorientedKernel :
    nativeK5P94ATypedNormalClosure D E ≤
      NativeK5ReorientedPentagonatorKernel t1 t2 t3 t4 t5 :=
  nativeK5P94ATyped_le_pentagonatorKernel (D := D) (E := E)
    (nativeK5NineReorientedWord t1 t2 t3 t4 t5)

/-- The new Type-valued genuine nine-face relator is outside the
old 4-cell kernel; hence the enlargement is PROPER. -/
theorem nativeK5ReorientedKernel_proper :
    nativeK5P94ATypedNormalClosure D E ≠
      NativeK5ReorientedPentagonatorKernel t1 t2 t3 t4 t5 := by
  intro h
  have hm :
      nativeK5NineReorientedWord t1 t2 t3 t4 t5 ∈
        nativeK5P94ATypedNormalClosure D E := by
    rw [h]
    exact (nativeK5ReorientedPentagonatorRelator t1 t2 t3 t4 t5).property
  exact nativeK5NineReorientedWord_not_mem_P94ATyped t1 t2 t3 t4 t5 hm

/-- No extension of the old INTEGER N-coordinate can descend to
this new kernel, because its actual generator boundary has N=3. -/
theorem nativeK5ReorientedKernel_not_le_NCount :
    ¬ NativeK5ReorientedPentagonatorKernel t1 t2 t3 t4 t5 ≤
        nativeK5NaturalityCount.ker := by
  intro h
  have hz := h (nativeK5ReorientedPentagonatorRelator t1 t2 t3 t4 t5).property
  change nativeK5NaturalityCount
    (nativeK5NineReorientedWord t1 t2 t3 t4 t5) = 0 at hz
  rw [← nativeK5NineReorientedExtendedCycle_word,
      nativeK5NineReorientedExtendedCycle_NCount_three] at hz
  norm_num at hz

/-- The COMPLETE old signed/odd F55 shadow still factors through
the independent normal kernel. The generator is not invented
from a numerical shadow: its real Type-valued source exists. -/
theorem nativeK5ReorientedKernel_le_shadow_ker :
    NativeK5ReorientedPentagonatorKernel t1 t2 t3 t4 t5 ≤
      nativeF55P94CWordToShadow.ker := by
  apply AddSubgroup.normalClosure_le_normal
  intro z hz
  rcases hz with h | h
  · exact nativeK5P94ATypedNormalClosure_le_shadow_ker
      (AddSubgroup.subset_normalClosure h)
  · have hw : z = nativeK5NineReorientedWord t1 t2 t3 t4 t5 := h
    subst z
    change nativeF55P94CWordToShadow
      (nativeK5NineReorientedWord t1 t2 t3 t4 t5) = 0
    rw [← nativeK5NineReorientedExtendedCycle_word]
    exact nativeK5NineReorientedExtendedCycle_shadow_zero t1 t2 t3 t4 t5

/-- Actual inclusion boundary (not an invented 4D map):
normal relation words embed in the original noncommutative group. -/
def nativeK5ReorientedPeifferBoundary :
    NativeK5ReorientedPentagonatorKernel t1 t2 t3 t4 t5 →+
      NativeF55P94CWord :=
  (NativeK5ReorientedPentagonatorKernel t1 t2 t3 t4 t5).subtype

/-- Exact noncommutative word on the newly declared independent
4D generator agrees with the FULL source Type-valued 3-cell word. -/
theorem nativeK5ReorientedRelator_genuine_boundary :
    nativeK5ReorientedPeifferBoundary t1 t2 t3 t4 t5
      (nativeK5ReorientedPentagonatorRelator t1 t2 t3 t4 t5) =
      (nativeK5NineReorientedExtendedCycle t1 t2 t3 t4 t5).p94cGroupWord := by
  change nativeK5NineReorientedWord t1 t2 t3 t4 t5 =
    (nativeK5NineReorientedExtendedCycle t1 t2 t3 t4 t5).p94cGroupWord
  exact (nativeK5NineReorientedExtendedCycle_word t1 t2 t3 t4 t5).symm

/-- Conjugation acts on the independently generated 4D relation
kernel by mathlib's REAL subgroup normality. No abelianization. -/
def nativeK5ReorientedPeifferAct
    (g : NativeF55P94CWord)
    (r : NativeK5ReorientedPentagonatorKernel t1 t2 t3 t4 t5) :
    NativeK5ReorientedPentagonatorKernel t1 t2 t3 t4 t5 :=
  ⟨g + (r : NativeF55P94CWord) - g, by
    have h :
        g + (r : NativeF55P94CWord) + -g ∈
          NativeK5ReorientedPentagonatorKernel t1 t2 t3 t4 t5 :=
      (inferInstance :
        (NativeK5ReorientedPentagonatorKernel t1 t2 t3 t4 t5).Normal).conj_mem
        (r : NativeF55P94CWord) r.property g
    simpa only [sub_eq_add_neg] using h⟩

theorem nativeK5ReorientedPeifferAct_zero
    (g : NativeF55P94CWord) :
    nativeK5ReorientedPeifferAct t1 t2 t3 t4 t5 g 0 = 0 := by
  apply Subtype.ext
  change g + (0 : NativeF55P94CWord) - g = 0
  simp [sub_eq_add_neg, neg_add_rev, add_assoc]

theorem nativeK5ReorientedPeifferAct_add
    (g : NativeF55P94CWord)
    (r s : NativeK5ReorientedPentagonatorKernel t1 t2 t3 t4 t5) :
    nativeK5ReorientedPeifferAct t1 t2 t3 t4 t5 g (r + s) =
      nativeK5ReorientedPeifferAct t1 t2 t3 t4 t5 g r +
      nativeK5ReorientedPeifferAct t1 t2 t3 t4 t5 g s := by
  apply Subtype.ext
  change g + ((r : NativeF55P94CWord) + (s : NativeF55P94CWord)) - g =
    (g + (r : NativeF55P94CWord) - g) +
      (g + (s : NativeF55P94CWord) - g)
  simp [sub_eq_add_neg, neg_add_rev, add_assoc]

theorem nativeK5ReorientedPeifferAct_identity
    (r : NativeK5ReorientedPentagonatorKernel t1 t2 t3 t4 t5) :
    nativeK5ReorientedPeifferAct t1 t2 t3 t4 t5 0 r = r := by
  apply Subtype.ext
  change (0 : NativeF55P94CWord) + r - 0 = r
  simp

theorem nativeK5ReorientedPeifferAct_comp
    (g h : NativeF55P94CWord)
    (r : NativeK5ReorientedPentagonatorKernel t1 t2 t3 t4 t5) :
    nativeK5ReorientedPeifferAct t1 t2 t3 t4 t5 (g + h) r =
      nativeK5ReorientedPeifferAct t1 t2 t3 t4 t5 g
        (nativeK5ReorientedPeifferAct t1 t2 t3 t4 t5 h r) := by
  apply Subtype.ext
  change (g + h) + (r : NativeF55P94CWord) - (g + h) =
    g + (h + (r : NativeF55P94CWord) - h) - g
  simp [sub_eq_add_neg, neg_add_rev, add_assoc]

/-- EXACT algebraic boundary equivariance for the corrected genuine
nine-face word's independent normal relation module. -/
theorem nativeK5ReorientedPeifferBoundary_equivariant
    (g : NativeF55P94CWord)
    (r : NativeK5ReorientedPentagonatorKernel t1 t2 t3 t4 t5) :
    nativeK5ReorientedPeifferBoundary t1 t2 t3 t4 t5
      (nativeK5ReorientedPeifferAct t1 t2 t3 t4 t5 g r) =
      g + nativeK5ReorientedPeifferBoundary t1 t2 t3 t4 t5 r - g := rfl

/-- Algebraic Peiffer identity for the GENUINE nine-face relator
kernel: boundary-induced ambient conjugation equals internal
conjugation by the same 4D relation word, in the nonabelian group.
This is NOT higher Type-valued 4D interchange coherence. -/
theorem nativeK5ReorientedPeiffer_identity
    (r s : NativeK5ReorientedPentagonatorKernel t1 t2 t3 t4 t5) :
    nativeK5ReorientedPeifferAct t1 t2 t3 t4 t5
      (nativeK5ReorientedPeifferBoundary t1 t2 t3 t4 t5 r) s =
      r + s - r := by
  apply Subtype.ext
  rfl

/-- Fully proved ACTUAL algebraic crossed-module data for the
selected source-grounded relator normal kernel, not a claim about
unconstructed higher interchange 4-cell witnesses. -/
structure NativeK5ReorientedPeifferData where
  boundary :
    NativeK5ReorientedPentagonatorKernel t1 t2 t3 t4 t5 →+
      NativeF55P94CWord
  act :
    NativeF55P94CWord →
      NativeK5ReorientedPentagonatorKernel t1 t2 t3 t4 t5 →
      NativeK5ReorientedPentagonatorKernel t1 t2 t3 t4 t5
  act_identity : ∀ r, act 0 r = r
  act_comp : ∀ g h r, act (g + h) r = act g (act h r)
  act_zero : ∀ g, act g 0 = 0
  act_add : ∀ g r s, act g (r + s) = act g r + act g s
  boundary_equivariant : ∀ g r, boundary (act g r) = g + boundary r - g
  peiffer : ∀ r s, act (boundary r) s = r + s - r

def nativeK5ReorientedPeifferData :
    NativeK5ReorientedPeifferData t1 t2 t3 t4 t5 where
  boundary := nativeK5ReorientedPeifferBoundary t1 t2 t3 t4 t5
  act := nativeK5ReorientedPeifferAct t1 t2 t3 t4 t5
  act_identity := nativeK5ReorientedPeifferAct_identity t1 t2 t3 t4 t5
  act_comp := nativeK5ReorientedPeifferAct_comp t1 t2 t3 t4 t5
  act_zero := nativeK5ReorientedPeifferAct_zero t1 t2 t3 t4 t5
  act_add := nativeK5ReorientedPeifferAct_add t1 t2 t3 t4 t5
  boundary_equivariant := nativeK5ReorientedPeifferBoundary_equivariant t1 t2 t3 t4 t5
  peiffer := nativeK5ReorientedPeiffer_identity t1 t2 t3 t4 t5

/-- Explicitly bind the NEW independent Type-valued 4-cell
constructor to its real source and to the exact normal-word
Peiffer boundary. These two witnesses are NOT falsely identified
as a Type-valued four-interchange coherence theorem. -/
structure NativeK5ReorientedPentagonatorBoundaryCertificate where
  sourceFourCell :
    NativeK5ReorientedIndependentPentagonator t1 t2 t3 t4 t5
      (nativeK5NineReorientedExtendedCycle t1 t2 t3 t4 t5)
      (nativeK5ReorientedStructuralIdentity t1 t2 t3 t4 t5)
  wordBoundary :
    nativeK5ReorientedPeifferBoundary t1 t2 t3 t4 t5
      (nativeK5ReorientedPentagonatorRelator t1 t2 t3 t4 t5) =
    (nativeK5NineReorientedExtendedCycle t1 t2 t3 t4 t5).p94cGroupWord

def nativeK5ReorientedPentagonatorBoundaryCertificate :
    NativeK5ReorientedPentagonatorBoundaryCertificate t1 t2 t3 t4 t5 where
  sourceFourCell := nativeK5ReorientedIndependentPentagonator t1 t2 t3 t4 t5
  wordBoundary := nativeK5ReorientedRelator_genuine_boundary t1 t2 t3 t4 t5

#print axioms nativeK5ReorientedIndependentPentagonator
#print axioms nativeK5ReorientedPentagonatorRelator
#print axioms nativeK5P94ATyped_le_reorientedKernel
#print axioms nativeK5ReorientedKernel_proper
#print axioms nativeK5ReorientedKernel_not_le_NCount
#print axioms nativeK5ReorientedKernel_le_shadow_ker
#print axioms nativeK5ReorientedRelator_genuine_boundary
#print axioms nativeK5ReorientedPeifferAct
#print axioms nativeK5ReorientedPeifferAct_add
#print axioms nativeK5ReorientedPeifferAct_comp
#print axioms nativeK5ReorientedPeifferBoundary_equivariant
#print axioms nativeK5ReorientedPeiffer_identity
#print axioms nativeK5ReorientedPeifferData
#print axioms nativeK5ReorientedPentagonatorBoundaryCertificate

end FiveNativeStages
end
end Kuu.F112.Physical
