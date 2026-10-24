import Kuu.F112.PolygonNativeF55P94DK5ReorientedPentagonatorPeiffer
import Mathlib.Tactic

/-!
# F112-P94D3U — residual Z/3 obstruction after the true pentagonator

P94D3S constructed a GENUINE nine-face Type-valued 3-cell in the
distinct structural F55 comparison presentation. Its noncommutative
word has naturality charge 3, not the historical shelling word's 1.
P94D3T adjoined an INDEPENDENT typed four-cell generator on this
actual 3-cell and constructed its exact algebraic Peiffer normal
relation kernel, retaining all original typed P94A four-cell relators.

The integer N-homomorphism cannot descend through the new relation:
the new pentagonator generator has N=3. But the composite Z/3-valued
homomorphism DOES vanish on the ENTIRE genuinely typed old P94A
normal kernel plus the new pentagonator and all its conjugates.
Consequently the original historically oriented W (N=1) remains
NONZERO in this independent extension, also after any gauge reframe.
The actual relative reorientation correction (N=2) also survives.

This is an algebraic necessary compatibility obstruction, NOT an
assertion of new higher Type-valued pentagonator coherence or a
physical identification of the Z/3 observer with unique Kuu.
We do not equate the old original shelling and the reoriented
typed cycle. No Gray, sorry/admit, added logical axioms, root removal,
or C60 finite-geometry changes.
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

/-- The exact additive homomorphism from original noncommutative
P/N words to the surviving Z/3 naturality observer. This observer
does not replace, reorder, or abelianize the original source words. -/
def nativeK5NaturalityCountModThree :
    NativeF55P94CWord →+ ZMod 3 :=
  (Int.castAddHom (ZMod 3)).comp nativeK5NaturalityCount

@[simp] theorem nativeK5NaturalityCountModThree_apply
    (w : NativeF55P94CWord) :
    nativeK5NaturalityCountModThree w =
      ((nativeK5NaturalityCount w : ℤ) : ZMod 3) := rfl

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

/-- The independently adjoined, ACTUALLY typed pentagonator has
charge 3, hence is killed by the Z/3 observer. -/
theorem nativeK5ReorientedPentagonatorModThree_zero :
    nativeK5NaturalityCountModThree
      (nativeK5NineReorientedWord t1 t2 t3 t4 t5) = 0 := by
  change (((nativeK5NaturalityCount
    (nativeK5NineReorientedWord t1 t2 t3 t4 t5) : ℤ) : ZMod 3)) = 0
  rw [← nativeK5NineReorientedExtendedCycle_word,
    nativeK5NineReorientedExtendedCycle_NCount_three]
  exact (by decide : (3 : ZMod 3) = 0)

/-- The historical original 9-face formal word has N=1, so
it remains a genuine NONZERO class in the mod-three receiver. -/
theorem nativeK5HistoricalShellingModThree_one :
    nativeK5NaturalityCountModThree
      (nativeK5GraphShellingWord t1 t2 t3 t4 t5) = 1 := by
  change (((nativeK5NaturalityCount
    (nativeK5GraphShellingWord t1 t2 t3 t4 t5) : ℤ) : ZMod 3)) = 1
  rw [nativeK5GraphShellingWord_NCount_one]
  norm_num

/-- ALL old proof-relevant typed P94A 4-cell relators, the
new GENUINE independent +3 pentagonator relator, and every
noncommutative conjugate lie in the Z/3 kernel. This proves
kernel-compatible mod-three descent at the algebraic word level. -/
theorem nativeK5ReorientedKernel_le_ModThree_ker :
    NativeK5ReorientedPentagonatorKernel t1 t2 t3 t4 t5 ≤
      nativeK5NaturalityCountModThree.ker := by
  apply AddSubgroup.normalClosure_le_normal
  intro z hz
  rcases hz with h | h
  · have hN : nativeK5NaturalityCount z = 0 := by
      have hn := nativeK5P94ATypedNormalClosure_le_NCount_ker
        (D := D) (E := E) (AddSubgroup.subset_normalClosure h)
      change nativeK5NaturalityCount z = 0 at hn
      exact hn
    change (((nativeK5NaturalityCount z : ℤ) : ZMod 3)) = 0
    rw [hN]
    norm_num
  · have hz : z = nativeK5NineReorientedWord t1 t2 t3 t4 t5 := h
    subst z
    exact nativeK5ReorientedPentagonatorModThree_zero t1 t2 t3 t4 t5

/-- Stronger obstruction than simply noting the old integer
N cannot descend: the original W of naturality charge ONE is
NOT annihilated by the new independent genuine +3 pentagonator,
even after adding the complete old typed P94A relation kernel. -/
theorem nativeK5HistoricalShelling_not_mem_reorientedKernel :
    nativeK5GraphShellingWord t1 t2 t3 t4 t5 ∉
      NativeK5ReorientedPentagonatorKernel t1 t2 t3 t4 t5 := by
  intro h
  have hzero := nativeK5ReorientedKernel_le_ModThree_ker
    t1 t2 t3 t4 t5 h
  change nativeK5NaturalityCountModThree
    (nativeK5GraphShellingWord t1 t2 t3 t4 t5) = 0 at hzero
  rw [nativeK5HistoricalShellingModThree_one] at hzero
  exact (by decide : (1 : ZMod 3) ≠ 0) hzero

/-- The exact noncommutative difference between the corrected
real nine-face word and the old oriented formal W carries N=2,
so it also cannot be absorbed by the enlarged four-cell kernel. -/
theorem nativeK5ReorientationCorrection_ModThree_two :
    nativeK5NaturalityCountModThree
      (nativeK5NineReorientedWord t1 t2 t3 t4 t5 +
        -(nativeK5GraphShellingWord t1 t2 t3 t4 t5)) = 2 := by
  change (((nativeK5NaturalityCount
    (nativeK5NineReorientedWord t1 t2 t3 t4 t5 +
      -(nativeK5GraphShellingWord t1 t2 t3 t4 t5)) : ℤ) : ZMod 3)) = 2
  rw [nativeK5NineReorientedWord_relative_NCount_two]
  norm_num

theorem nativeK5ReorientationCorrection_not_mem_reorientedKernel :
    nativeK5NineReorientedWord t1 t2 t3 t4 t5 +
        -(nativeK5GraphShellingWord t1 t2 t3 t4 t5) ∉
      NativeK5ReorientedPentagonatorKernel t1 t2 t3 t4 t5 := by
  intro h
  have hzero := nativeK5ReorientedKernel_le_ModThree_ker
    t1 t2 t3 t4 t5 h
  change nativeK5NaturalityCountModThree
    (nativeK5NineReorientedWord t1 t2 t3 t4 t5 +
      -(nativeK5GraphShellingWord t1 t2 t3 t4 t5)) = 0 at hzero
  rw [nativeK5ReorientationCorrection_ModThree_two] at hzero
  exact (by decide : (2 : ZMod 3) ≠ 0) hzero

/-- Arbitrary noncommutative gauge conjugation cannot erase the
surviving Z/3 obstruction of the OLD source word W. -/
theorem nativeK5HistoricalShelling_gauge_not_mem_reorientedKernel
    (g : NativeF55P94CWord) :
    nativeK5GaugeReframe g
        (nativeK5GraphShellingWord t1 t2 t3 t4 t5) ∉
      NativeK5ReorientedPentagonatorKernel t1 t2 t3 t4 t5 := by
  intro h
  have hzero := nativeK5ReorientedKernel_le_ModThree_ker
    t1 t2 t3 t4 t5 h
  change (((nativeK5NaturalityCount
    (nativeK5GaugeReframe g
      (nativeK5GraphShellingWord t1 t2 t3 t4 t5)) : ℤ) : ZMod 3)) = 0 at hzero
  rw [nativeK5GaugeReframe_NCount,
    nativeK5GraphShellingWord_NCount_one] at hzero
  exact (by decide : (1 : ZMod 3) ≠ 0) hzero

#print axioms nativeK5NaturalityCountModThree
#print axioms nativeK5NaturalityCountModThree_apply
#print axioms nativeK5ReorientedPentagonatorModThree_zero
#print axioms nativeK5HistoricalShellingModThree_one
#print axioms nativeK5ReorientedKernel_le_ModThree_ker
#print axioms nativeK5HistoricalShelling_not_mem_reorientedKernel
#print axioms nativeK5ReorientationCorrection_ModThree_two
#print axioms nativeK5ReorientationCorrection_not_mem_reorientedKernel
#print axioms nativeK5HistoricalShelling_gauge_not_mem_reorientedKernel

end FiveNativeStages
end
end Kuu.F112.Physical
