import Kuu.F112.PolygonNativeF55P94DK5TypedPentagonatorBoundary
import Mathlib.Tactic

/-!
# F112-P94D3I — distinguish TAG-order formal K₅ word from global shelling word

P94D3H's fixed tag-order formal word is NOT the word produced
by the first actual outward graph shelling. Their original full
F55 shadows and independent integer N-count agree, but ordered
noncommutative P/N words do not. Detect the mismatch by the
GENUINE S3 receiver from P94D3B, not by abelianized shadows.

Construct the minimal algebraic normal-kernel enlargement needed
for a new independent pentagonator boundary. Show the old kernel
is properly included and the N-count cannot descend after
killing a +1-charge pentagonator word, while the old F55 shadow
can descend. Algebraic enlargement is NOT Type-valued 4D coherence.
No Gray, sorry, admit, new logical axioms, or root removal.
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

/-- The genuine global outward graph-shelling order is
-P, N, -P, -P, N, P, P, -N, P.  This is a noncommutative
identity obtained by evaluation of the nine ACTUAL typed faces. -/
theorem nativeK5GraphShellingWord_exact_letters :
    nativeK5GraphShellingWord t1 t2 t3 t4 t5 =
      (-nativeK5PNPentagon) + nativeK5PNNaturality +
      (-nativeK5PNPentagon) + (-nativeK5PNPentagon) +
      nativeK5PNNaturality + nativeK5PNPentagon +
      nativeK5PNPentagon + (-nativeK5PNNaturality) +
      nativeK5PNPentagon := rfl

/-- The different P94D3H TAG ordering is N,N,-N,P,P,-P,P,-P,-P.
Do NOT tacitly permute these elements in a NONABELIAN free group. -/
theorem nativeK5NineAnchoredFaceFormalWord_exact_letters :
    nativeK5NineAnchoredFaceFormalWord t1 t2 t3 t4 t5 =
      nativeK5PNNaturality + nativeK5PNNaturality +
      (-nativeK5PNNaturality) + nativeK5PNPentagon +
      nativeK5PNPentagon + (-nativeK5PNPentagon) +
      nativeK5PNPentagon + (-nativeK5PNPentagon) +
      (-nativeK5PNPentagon) := rfl

/-- A concrete finite GROUP receiver separates the cyclic shelling
word from the tag-order formal word: the first gives (02) in S3. -/
theorem nativeK5GraphShellingWord_S3 :
    nativeK5WordPentagonNaturalityS3
      (nativeK5GraphShellingWord t1 t2 t3 t4 t5) =
        Additive.ofMul (Equiv.swap (0 : Fin 3) (2 : Fin 3)) := by
  rw [nativeK5GraphShellingWord_exact_letters]
  simp only [map_add, map_neg, nativeK5PNPentagon, nativeK5PNNaturality,
    nativeK5WordPentagonNaturalityS3, FreeAddGroup.lift_apply_of]
  decide

/-- The tag-order formal word gives N=(12) in that same S3 receiver. -/
theorem nativeK5NineAnchoredFaceFormalWord_S3 :
    nativeK5WordPentagonNaturalityS3
      (nativeK5NineAnchoredFaceFormalWord t1 t2 t3 t4 t5) =
        Additive.ofMul (Equiv.swap (1 : Fin 3) (2 : Fin 3)) := by
  rw [nativeK5NineAnchoredFaceFormalWord_exact_letters]
  simp only [map_add, map_neg, nativeK5PNPentagon, nativeK5PNNaturality,
    nativeK5WordPentagonNaturalityS3, FreeAddGroup.lift_apply_of]
  decide

/-- Essential new P94D3I distinction: no false equality between
the formal word and the actual graph-shelling-order word. -/
theorem nativeK5GraphShellingWord_ne_formal :
    nativeK5GraphShellingWord t1 t2 t3 t4 t5 ≠
      nativeK5NineAnchoredFaceFormalWord t1 t2 t3 t4 t5 := by
  intro h
  have hh := congrArg nativeK5WordPentagonNaturalityS3 h
  rw [nativeK5GraphShellingWord_S3,
    nativeK5NineAnchoredFaceFormalWord_S3] at hh
  exact (by decide :
    Additive.ofMul (Equiv.swap (0 : Fin 3) (2 : Fin 3)) ≠
      Additive.ofMul (Equiv.swap (1 : Fin 3) (2 : Fin 3))) hh

/-- Add EXACTLY the independently chosen pentagonator word
to the normal kernel of ALL P94A genuine typed 4-cells.
A normal closure, not an assertion of a Type-valued filler. -/
def nativeK5PentagonatorWordNormalClosure
    (D : Type uD) [Category.{vD} D]
    (E : Type uE) [Category.{vE} E]
    (w : NativeF55P94CWord) : AddSubgroup NativeF55P94CWord :=
  AddSubgroup.normalClosure (nativeK5P94ATypedRelators D E ∪ {w})

instance nativeK5PentagonatorWordNormalClosure_normal
    (D : Type uD) [Category.{vD} D]
    (E : Type uE) [Category.{vE} E]
    (w : NativeF55P94CWord) :
    (nativeK5PentagonatorWordNormalClosure D E w).Normal := by
  unfold nativeK5PentagonatorWordNormalClosure
  infer_instance

/-- The original normal word kernel embeds in the new independent
4D correction kernel, preserving every old typed 4-cell relation. -/
theorem nativeK5P94ATyped_le_pentagonatorKernel (w : NativeF55P94CWord) :
    nativeK5P94ATypedNormalClosure D E ≤
      nativeK5PentagonatorWordNormalClosure D E w := by
  apply AddSubgroup.normalClosure_le_normal
  intro z hz
  apply AddSubgroup.subset_normalClosure
  exact Or.inl hz

/-- The additional relator is genuinely present in the
new NORMAL closure (not merely in an ad hoc shadow quotient). -/
theorem nativeK5PentagonatorWord_mem (w : NativeF55P94CWord) :
    w ∈ nativeK5PentagonatorWordNormalClosure D E w := by
  apply AddSubgroup.subset_normalClosure
  exact Or.inr rfl

/-- For the true outward K₅ shelling, the normal kernel is a
PROPER enlargement, because the original kernel conserves N-count. -/
theorem nativeK5PentagonatorKernel_proper :
    nativeK5P94ATypedNormalClosure D E ≠
      nativeK5PentagonatorWordNormalClosure D E
        (nativeK5GraphShellingWord t1 t2 t3 t4 t5) := by
  intro heq
  have hm :
      nativeK5GraphShellingWord t1 t2 t3 t4 t5 ∈
        nativeK5P94ATypedNormalClosure D E := by
    rw [heq]
    exact nativeK5PentagonatorWord_mem
      (D := D) (E := E) (nativeK5GraphShellingWord t1 t2 t3 t4 t5)
  exact nativeK5GraphShellingWord_not_mem_P94ATyped t1 t2 t3 t4 t5 hm

/-- No integer N-count lift to this independent kernel could
agree with the ORIGINAL N-count on all raw words; it must kill
charge +1. This does NOT imply a Type-level pentagonator exists. -/
theorem nativeK5PentagonatorKernel_not_le_NCount :
    ¬ nativeK5PentagonatorWordNormalClosure D E
        (nativeK5GraphShellingWord t1 t2 t3 t4 t5) ≤
          nativeK5NaturalityCount.ker := by
  intro h
  have hz := h (nativeK5PentagonatorWord_mem (D := D) (E := E)
    (nativeK5GraphShellingWord t1 t2 t3 t4 t5))
  change nativeK5NaturalityCount
    (nativeK5GraphShellingWord t1 t2 t3 t4 t5) = 0 at hz
  rw [nativeK5GraphShellingWord_NCount_one] at hz
  norm_num at hz

/-- Unlike N-count, the entire OLD F55 shadow still descends through
the new algebraic normal correction, because the new genuine face
shelling word has complete old shadow zero. -/
theorem nativeK5PentagonatorKernel_le_shadow_ker :
    nativeK5PentagonatorWordNormalClosure D E
      (nativeK5GraphShellingWord t1 t2 t3 t4 t5) ≤
        nativeF55P94CWordToShadow.ker := by
  apply AddSubgroup.normalClosure_le_normal
  intro z hz
  rcases hz with h | h
  · exact nativeK5P94ATypedNormalClosure_le_shadow_ker
      (AddSubgroup.subset_normalClosure h)
  · have hword : z = nativeK5GraphShellingWord t1 t2 t3 t4 t5 := h
    subst z
    change nativeF55P94CWordToShadow
      (nativeK5GraphShellingWord t1 t2 t3 t4 t5) = 0
    exact nativeK5GraphShellingWord_shadow_zero t1 t2 t3 t4 t5

#print axioms nativeK5GraphShellingWord_exact_letters
#print axioms nativeK5NineAnchoredFaceFormalWord_exact_letters
#print axioms nativeK5GraphShellingWord_S3
#print axioms nativeK5NineAnchoredFaceFormalWord_S3
#print axioms nativeK5GraphShellingWord_ne_formal
#print axioms nativeK5P94ATyped_le_pentagonatorKernel
#print axioms nativeK5PentagonatorWord_mem
#print axioms nativeK5PentagonatorKernel_proper
#print axioms nativeK5PentagonatorKernel_not_le_NCount
#print axioms nativeK5PentagonatorKernel_le_shadow_ker

end FiveNativeStages
end
end Kuu.F112.Physical
