import Kuu.F112.PolygonNativeF55P94DK5PhysicalPairInterchanges
import Mathlib.Algebra.Group.Subgroup.Basic
import Mathlib.Tactic

/-!
# F112-P94D3F — exact normal closure of ALL actual P94A typed 4-cell word defects

P94D3C imposes one actually witnessed P/N commutator.
P94D3E discovers that genuine top-hexagon P94A interchange also forces
P/S and S/N commutators in the coarse global P94C3 three-letter word.

To avoid guessing whether those three relators are enough, build a
SEPARATE, proof-relevant source of word relations from ALL actual
P94A Type-valued four-cell terms, over ALL C60 polygons, F45 source
categories, Blocks, depths, F54 route boundaries and source 3-proofs.

A typed witness in this index family is REQUIRED to generate each
relator. The minimal normal closure of its word differences is then
constructed using pinned mathlib. Any actual P94A 4-cell maps equal
words into the new quotient. The complete signed original F55 shadow,
including the hexagon odd phase, descends because the original Type
witness is shadow-sound.

For the genuine Site×Site C60 source, P94D3E's 3-pair physical normal
closure is a proven LOWER bound on this all-typed normal kernel.
In particular it is strictly stronger than P94D3C's single P/N
normal closure. We do NOT silently identify the typed-kernel quotient
with the whole source 4-cell quotient or assume this algebraic
normal closure is precisely the full universal commutator subgroup.
The source may retain relations beyond the coarse word map.

No Gray, sorry, admit, new axioms or changes to public roots.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uD vD uE vE

/-- A proof-relevant certificate that a free-word difference comes
from an ACTUAL 4-cell with precisely matching native F45/F54 typed
source and target. It is NOT populated from equality of shadows. -/
inductive NativeK5P94ATypedWordRelator
    (D : Type uD) [Category.{vD} D]
    (E : Type uE) [Category.{vE} E] :
    NativeF55P94CWord → Type (max (max uD uE) (max vD vE)) where
  | ofFourCell
      {p : Polygon} {a b : D} {x y : E}
      {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55P92AssocComparison p r s}
      (four : NativeF55P94UnitFourCell f g) :
      NativeK5P94ATypedWordRelator D E
        (f.p94cGroupWord - g.p94cGroupWord)

variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

/-- Exactly the image in the common free word group of all
actually witnessed P94A 4-cell boundaries for fixed D,E. -/
def nativeK5P94ATypedRelators
    (D : Type uD) [Category.{vD} D]
    (E : Type uE) [Category.{vE} E] :
    Set NativeF55P94CWord :=
  {w | Nonempty (NativeK5P94ATypedWordRelator D E w)}

/-- The minimal NORMAL additive subgroup containing the exact
P94A Type-witness word differences (for fixed source categories). -/
def nativeK5P94ATypedNormalClosure
    (D : Type uD) [Category.{vD} D]
    (E : Type uE) [Category.{vE} E] :
    AddSubgroup NativeF55P94CWord :=
  AddSubgroup.normalClosure (nativeK5P94ATypedRelators D E)

instance nativeK5P94ATypedNormalClosure_normal
    (D : Type uD) [Category.{vD} D]
    (E : Type uE) [Category.{vE} E] :
    (nativeK5P94ATypedNormalClosure D E).Normal := by
  unfold nativeK5P94ATypedNormalClosure
  infer_instance

/-- Every actual Type-valued P94A 4-cell contributes its exact
noncommutative source-word relator to the minimal normal kernel. -/
theorem nativeK5P94ATypedFourCell_relator_mem
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55P92AssocComparison p r s}
    (four : NativeF55P94UnitFourCell f g) :
    f.p94cGroupWord - g.p94cGroupWord ∈
      nativeK5P94ATypedNormalClosure D E := by
  apply AddSubgroup.subset_normalClosure
  exact ⟨NativeK5P94ATypedWordRelator.ofFourCell four⟩

/-- This normal closure is minimal among all NORMAL normal-word
quotient kernels that kill EVERY actually typed four-cell relator. -/
theorem nativeK5P94ATypedNormalClosure_minimal
    (H : AddSubgroup NativeF55P94CWord) [H.Normal]
    (h : ∀ w : NativeF55P94CWord,
      NativeK5P94ATypedWordRelator D E w → w ∈ H) :
    nativeK5P94ATypedNormalClosure D E ≤ H := by
  apply AddSubgroup.normalClosure_le_normal
  intro w hw
  rcases hw with ⟨ev⟩
  exact h w ev

abbrev NativeK5P94ATypedCorrectedWord
    (D : Type uD) [Category.{vD} D]
    (E : Type uE) [Category.{vE} E] :=
  NativeF55P94CWord ⧸ nativeK5P94ATypedNormalClosure D E

def nativeK5P94ATypedClass :
    NativeF55P94CWord →+
      NativeK5P94ATypedCorrectedWord D E :=
  QuotientAddGroup.mk' (nativeK5P94ATypedNormalClosure D E)

/-- Crucially: EVERY actual typed P94A 4-cell, not just selected
P/N, P/S or S/N, maps to EQUAL coarse words in the corrected quotient. -/
theorem nativeK5P94ATypedFourCell_word_descends
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55P92AssocComparison p r s}
    (four : NativeF55P94UnitFourCell f g) :
    nativeK5P94ATypedClass (D := D) (E := E) f.p94cGroupWord =
      nativeK5P94ATypedClass (D := D) (E := E) g.p94cGroupWord := by
  apply (QuotientAddGroup.eq_iff_sub_mem).2
  exact nativeK5P94ATypedFourCell_relator_mem four

/-- The source witness proves FULL signed+odd shadow equality
of its two group-word endpoints, not merely word-count parity. -/
theorem NativeK5P94ATypedWordRelator.shadow_zero
    {w : NativeF55P94CWord}
    (ev : NativeK5P94ATypedWordRelator D E w) :
    nativeF55P94CWordToShadow w = 0 := by
  cases ev with
  | ofFourCell four =>
      simp only [map_sub, NativeF55P92AssocComparison.p94cGroupWord_shadow]
      exact sub_eq_zero.mpr four.shadow_sound

/-- All P94A typed relators, including arbitrary binary contexts,
left/right whiskers and interchange, preserve the FULL old F55 shadow. -/
theorem nativeK5P94ATypedNormalClosure_le_shadow_ker :
    nativeK5P94ATypedNormalClosure D E ≤
      nativeF55P94CWordToShadow.ker := by
  apply AddSubgroup.normalClosure_le_normal
  intro w hw
  rcases hw with ⟨ev⟩
  change nativeF55P94CWordToShadow w = 0
  exact ev.shadow_zero

def nativeK5P94ATypedShadow :
    NativeK5P94ATypedCorrectedWord D E →+ KuuNativeF55Shadow :=
  QuotientAddGroup.lift (nativeK5P94ATypedNormalClosure D E)
    nativeF55P94CWordToShadow
    nativeK5P94ATypedNormalClosure_le_shadow_ker

theorem nativeK5P94ATypedShadow_spec (w : NativeF55P94CWord) :
    nativeK5P94ATypedShadow
      (nativeK5P94ATypedClass (D := D) (E := E) w) =
        nativeF55P94CWordToShadow w :=
  QuotientAddGroup.lift_mk' (nativeK5P94ATypedNormalClosure D E)
    nativeK5P94ATypedNormalClosure_le_shadow_ker w

/-- All THREE independently genuine top-hexagon P/S, S/N and
north-pentagon P/N 4-cell relators lie in the ALL-typed word kernel
for the genuine C60 Site×Site categorical source. -/
theorem nativeK5ThreePhysicalPairClosure_le_P94ATypedSite :
    nativeK5ThreePhysicalPairClosure ≤
      nativeK5P94ATypedNormalClosure Site Site := by
  apply AddSubgroup.normalClosure_le_normal
  intro w hw
  simp only [nativeK5ThreePhysicalPairRelators,
    Set.mem_insert_iff, Set.mem_singleton_iff] at hw
  rcases hw with h | h | h
  · rw [h, ← northK5P94AInterchange_actual_relator]
    exact nativeK5P94ATypedFourCell_relator_mem
      northK5P94AInterchange_actual_fourCell
  · rw [h, ← northHexagonPSInterchange_actual_relator]
    exact nativeK5P94ATypedFourCell_relator_mem
      northHexagonPSInterchange_actual_fourCell
  · rw [h, ← northHexagonSNInterchange_actual_relator]
    exact nativeK5P94ATypedFourCell_relator_mem
      northHexagonSNInterchange_actual_fourCell

/-- The original one-relator P/N algebraic quotient CANNOT be the
coarse all-typed four-cell quotient: the ACTUAL P/S exchange already
forces a relation that was proven absent from the smaller kernel. -/
theorem nativeK5PNNormalClosure_ne_P94ATypedSite :
    nativeK5PNNormalClosure ≠
      nativeK5P94ATypedNormalClosure Site Site := by
  intro h
  have hps : nativeK5PSInterchangeRelator ∈ nativeK5PNNormalClosure := by
    rw [h, ← northHexagonPSInterchange_actual_relator]
    exact nativeK5P94ATypedFourCell_relator_mem
      northHexagonPSInterchange_actual_fourCell
  have heq :
      nativeK5PNCorrectedClass (nativeK5PNPentagon + nativeK5PNSquare) =
        nativeK5PNCorrectedClass (nativeK5PNSquare + nativeK5PNPentagon) :=
    (QuotientAddGroup.eq_iff_sub_mem).2 hps
  exact nativeK5PNCorrected_pentagon_square_noncommute heq

#print axioms NativeK5P94ATypedWordRelator
#print axioms nativeK5P94ATypedRelators
#print axioms nativeK5P94ATypedNormalClosure
#print axioms nativeK5P94ATypedFourCell_relator_mem
#print axioms nativeK5P94ATypedNormalClosure_minimal
#print axioms nativeK5P94ATypedFourCell_word_descends
#print axioms NativeK5P94ATypedWordRelator.shadow_zero
#print axioms nativeK5P94ATypedNormalClosure_le_shadow_ker
#print axioms nativeK5P94ATypedShadow_spec
#print axioms nativeK5ThreePhysicalPairClosure_le_P94ATypedSite
#print axioms nativeK5PNNormalClosure_ne_P94ATypedSite

end
end Kuu.F112.Physical
