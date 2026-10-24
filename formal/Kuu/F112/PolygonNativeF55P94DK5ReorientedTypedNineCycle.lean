import Kuu.F112.PolygonNativeF55P94DK5EightFaceTypedParallelBoundary
import Mathlib.Tactic

/-!
# F112-P94D3S: a genuine nine-face Type-valued K5 loop, with an honest orientation correction

The previous P94D3Q/R proofs give every original F54 route and all nine
P92B face witnesses, but the previously fixed *minus*-naturality
square2 is oriented path1 -> path5, whereas the cyclic shelling
needs path5 -> path1. The old signed shelling word N = 1 remains
an exact algebraic invariant but is NOT the word of this pasted cycle.

In this distinct STRUCTURAL extension of P92B, we define a
recursive inverse of actual 3-cell proofs (original P92B inversion,
F54 structural inversion, reversed order of vertical composition).
The full noncommutative P/N word of the inverse is the group inverse;
nothing is abelianized.

Using the actual inverse of the anchored square2 proof, we then build
a completely genuine nine-face Type-valued closed 3-cell based at
canonical route0. Its exact order is the original K5 shelling
7,0,5,8,1,3,6,2,4, but *square2 has the opposite 3-cell direction*.
Consequently N = 3, NOT 1, and it does not descend through any old
N-preserving P94A/P94C2 normal kernel. Its full historical F55 shadow
still vanishes.

The correction is not a formal commutative difference: its exact
noncommutative defect against the old algebraic shelling word is
a conjugate of two negative square2 letters; the integer N-defect
is +2. No fictitious same-word 4-cell or pentagonator coherence
is introduced here. Existing old no-go results and 107 public roots
are retained. No Gray, sorry/admit or added logical axioms.
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

/-- A genuine inverse of EVERY generated extended Type-valued
3-cell, including nested noncommutative vertical pastings.
The inverse is a new proof-term operation, not equality of
unrelated source routes or a higher-dimensional 4-cell. -/
def NativeF55StructuralComparison.reverse
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (w : NativeF55StructuralComparison p r s) :
    NativeF55StructuralComparison p s r := by
  induction w with
  | original originalCell => exact .original (.symm originalCell)
  | structural seam => exact .structural (.symm seam)
  | trans left right ihLeft ihRight => exact .trans ihRight ihLeft

/-- The ACTUAL inverse constructor reverses the original ordered
noncommutative group word, not only its integer charge. -/
theorem NativeF55StructuralComparison.reverse_word
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (w : NativeF55StructuralComparison p r s) :
    w.reverse.p94cGroupWord = -w.p94cGroupWord := by
  induction w with
  | original originalCell => rfl
  | structural seam =>
      change (0 : NativeF55P94CWord) = -0
      simp
  | trans left right ihLeft ihRight =>
      change right.reverse.p94cGroupWord + left.reverse.p94cGroupWord =
        -(left.p94cGroupWord + right.p94cGroupWord)
      rw [ihRight, ihLeft]
      exact (neg_add_rev _ _).symm

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

/-- REAL outward Type-valued square2 comparison, achieved by
inverting the already constructed REVERSED original P92B 3-cell.
This proof goes path5 -> path1, but has N=+1, unlike the old
anchored square2's N=-1. -/
def nativeK5NaturalitySquare2ForwardExtendedFace :
    NativeF55StructuralComparison p
      (nativeK5TypedGlobalF54Route t1 t2 t3 t4 t5 5)
      (nativeK5TypedGlobalF54Route t1 t2 t3 t4 t5 1) :=
  (nativeK5NaturalitySquare2ReverseExtendedFace t1 t2 t3 t4 t5).reverse

theorem nativeK5NaturalitySquare2ForwardExtendedFace_word :
    (nativeK5NaturalitySquare2ForwardExtendedFace t1 t2 t3 t4 t5).p94cGroupWord =
      -(nativeK5AnchoredFace t1 t2 t3 t4 t5 .square2).2.2.2.p94cGroupWord := by
  rw [nativeK5NaturalitySquare2ForwardExtendedFace,
    NativeF55StructuralComparison.reverse_word,
    nativeK5NaturalitySquare2ReverseExtendedFace_word]

theorem nativeK5NaturalitySquare2ForwardExtendedFace_NCount_one :
    nativeK5NaturalityCount
      (nativeK5NaturalitySquare2ForwardExtendedFace t1 t2 t3 t4 t5).p94cGroupWord =
        1 := by
  rw [nativeK5NaturalitySquare2ForwardExtendedFace_word, map_neg]
  change -(nativeK5AnchoredFaceNCount t1 t2 t3 t4 t5 .square2) = 1
  rw [nativeK5AnchoredFaceNCount_exact]
  rfl

/-- First seven already-proved genuine Type-valued shelling
faces have N=2 (naturality square0 and square1). -/
theorem nativeK5FirstSevenExtendedStructuralPasting_NCount_two :
    nativeK5NaturalityCount
      (nativeK5FirstSevenExtendedStructuralPasting t1 t2 t3 t4 t5).p94cGroupWord =
      2 := by
  rw [nativeK5FirstSevenExtendedStructuralPasting_word]
  simp only [nativeK5FirstSevenAnchoredWord, map_add]
  change
    nativeK5AnchoredFaceNCount t1 t2 t3 t4 t5 .pentagon7 +
    nativeK5AnchoredFaceNCount t1 t2 t3 t4 t5 .square0 +
    nativeK5AnchoredFaceNCount t1 t2 t3 t4 t5 .pentagon5 +
    nativeK5AnchoredFaceNCount t1 t2 t3 t4 t5 .pentagon8 +
    nativeK5AnchoredFaceNCount t1 t2 t3 t4 t5 .square1 +
    nativeK5AnchoredFaceNCount t1 t2 t3 t4 t5 .pentagon3 +
    nativeK5AnchoredFaceNCount t1 t2 t3 t4 t5 .pentagon6 = 2
  simp [nativeK5AnchoredFaceNCount_exact, nativeK5FaceExpectedNCount]

/-- Nine ACTUAL original P92B face proof terms genuinely compose
at the ORIGINAL common F54 route0, with no abstract-graph
substitution. They follow global route0->...->5->1->0.
The eighth 3-cell is the genuine inverse of the old symm-square2. -/
def nativeK5NineReorientedExtendedCycle :
    NativeF55StructuralComparison p
      (nativeK5TypedGlobalF54Route t1 t2 t3 t4 t5 0)
      (nativeK5TypedGlobalF54Route t1 t2 t3 t4 t5 0) :=
  .trans
    (.trans
      (nativeK5FirstSevenExtendedStructuralPasting t1 t2 t3 t4 t5)
      (nativeK5NaturalitySquare2ForwardExtendedFace t1 t2 t3 t4 t5))
    (nativeK5Pentagon4ExtendedFace t1 t2 t3 t4 t5)

/-- Explicit corrected, STILL NONCOMMUTATIVE nine-face ordered word.
Only square2 is inverted relative to the historical formal shelling
word. Pentagon4 remains the final face (never commuted to front). -/
def nativeK5NineReorientedWord : NativeF55P94CWord :=
  nativeK5FirstSevenAnchoredWord t1 t2 t3 t4 t5 +
  (-(nativeK5AnchoredFace t1 t2 t3 t4 t5 .square2).2.2.2.p94cGroupWord) +
  (nativeK5AnchoredFace t1 t2 t3 t4 t5 .pentagon4).2.2.2.p94cGroupWord

theorem nativeK5NineReorientedExtendedCycle_word :
    (nativeK5NineReorientedExtendedCycle t1 t2 t3 t4 t5).p94cGroupWord =
      nativeK5NineReorientedWord t1 t2 t3 t4 t5 := by
  change
    (nativeK5FirstSevenExtendedStructuralPasting t1 t2 t3 t4 t5).p94cGroupWord +
    (nativeK5NaturalitySquare2ForwardExtendedFace t1 t2 t3 t4 t5).p94cGroupWord +
    (nativeK5Pentagon4ExtendedFace t1 t2 t3 t4 t5).p94cGroupWord =
      nativeK5FirstSevenAnchoredWord t1 t2 t3 t4 t5 +
      (-(nativeK5AnchoredFace t1 t2 t3 t4 t5 .square2).2.2.2.p94cGroupWord) +
      (nativeK5AnchoredFace t1 t2 t3 t4 t5 .pentagon4).2.2.2.p94cGroupWord
  rw [nativeK5FirstSevenExtendedStructuralPasting_word,
    nativeK5NaturalitySquare2ForwardExtendedFace_word,
    nativeK5Pentagon4ExtendedFace_word]

/-- Genuine Type-valued nine-face pasting carries +3, because
the genuinely pastable square2 contributes +1 (not the -1
assigned to the graph-shelling's differently oriented witness). -/
theorem nativeK5NineReorientedExtendedCycle_NCount_three :
    nativeK5NaturalityCount
      (nativeK5NineReorientedExtendedCycle t1 t2 t3 t4 t5).p94cGroupWord = 3 := by
  change nativeK5NaturalityCount
      ((nativeK5FirstSevenExtendedStructuralPasting t1 t2 t3 t4 t5).p94cGroupWord +
       (nativeK5NaturalitySquare2ForwardExtendedFace t1 t2 t3 t4 t5).p94cGroupWord +
       (nativeK5Pentagon4ExtendedFace t1 t2 t3 t4 t5).p94cGroupWord) = 3
  simp only [map_add]
  rw [nativeK5FirstSevenExtendedStructuralPasting_NCount_two,
    nativeK5NaturalitySquare2ForwardExtendedFace_NCount_one]
  have hp :
      nativeK5NaturalityCount
        (nativeK5Pentagon4ExtendedFace t1 t2 t3 t4 t5).p94cGroupWord = 0 := by
    rw [nativeK5Pentagon4ExtendedFace_word]
    change nativeK5AnchoredFaceNCount t1 t2 t3 t4 t5 .pentagon4 = 0
    simpa [nativeK5FaceExpectedNCount] using
      nativeK5AnchoredFaceNCount_exact t1 t2 t3 t4 t5 .pentagon4
  rw [hp]
  norm_num

/-- Genuine new nine-face Type-valued loop still vanishes under
the complete old F55 signed-pentagon/square/odd-phase shadow. -/
theorem nativeK5NineReorientedExtendedCycle_shadow_zero :
    nativeF55P94CWordToShadow
      (nativeK5NineReorientedExtendedCycle t1 t2 t3 t4 t5).p94cGroupWord = 0 := by
  rw [nativeK5NineReorientedExtendedCycle_word]
  simp only [nativeK5NineReorientedWord, nativeK5FirstSevenAnchoredWord,
    map_add, map_neg, NativeF55P92AssocComparison.p94cGroupWord_shadow]
  simp [nativeK5AnchoredFace_fullShadow,
    nativeK5CandidateFaceShadow, nativeK5FaceTagFin]

/-- True old shelling word has the same ordered prefix and suffix,
but the square2 middle letter is the OPPOSITE original witness. -/
theorem nativeK5GraphShellingWord_prefix_square2_suffix :
    nativeK5GraphShellingWord t1 t2 t3 t4 t5 =
      nativeK5FirstSevenAnchoredWord t1 t2 t3 t4 t5 +
        (nativeK5AnchoredFace t1 t2 t3 t4 t5 .square2).2.2.2.p94cGroupWord +
        (nativeK5AnchoredFace t1 t2 t3 t4 t5 .pentagon4).2.2.2.p94cGroupWord := by
  rfl

/-- EXACT correction in the NONCOMMUTATIVE group: conjugate
of two negative square2 witness words by the REAL first-seven
prefix. Not a permutation or a sum in an abelianized group. -/
theorem nativeK5NineReorientedWord_relative_correction :
    nativeK5NineReorientedWord t1 t2 t3 t4 t5 +
       -(nativeK5GraphShellingWord t1 t2 t3 t4 t5) =
       nativeK5FirstSevenAnchoredWord t1 t2 t3 t4 t5 +
       (-(nativeK5AnchoredFace t1 t2 t3 t4 t5 .square2).2.2.2.p94cGroupWord) +
       (-(nativeK5AnchoredFace t1 t2 t3 t4 t5 .square2).2.2.2.p94cGroupWord) +
       -(nativeK5FirstSevenAnchoredWord t1 t2 t3 t4 t5) := by
  let s := nativeK5FirstSevenAnchoredWord t1 t2 t3 t4 t5
  let q := (nativeK5AnchoredFace t1 t2 t3 t4 t5 .square2).2.2.2.p94cGroupWord
  let a := (nativeK5AnchoredFace t1 t2 t3 t4 t5 .pentagon4).2.2.2.p94cGroupWord
  change (s + (-q) + a) + -(s + q + a) = s + (-q) + (-q) + (-s)
  simp [neg_add_rev, add_assoc]

/-- The correction changes the old integer N-charge by +2.
The +1 historical result remains unchanged and distinct. -/
theorem nativeK5NineReorientedWord_relative_NCount_two :
    nativeK5NaturalityCount
      (nativeK5NineReorientedWord t1 t2 t3 t4 t5 +
        -(nativeK5GraphShellingWord t1 t2 t3 t4 t5)) = 2 := by
  rw [map_add, map_neg]
  have hnew :
      nativeK5NaturalityCount (nativeK5NineReorientedWord t1 t2 t3 t4 t5) = 3 := by
    rw [← nativeK5NineReorientedExtendedCycle_word]
    exact nativeK5NineReorientedExtendedCycle_NCount_three t1 t2 t3 t4 t5
  rw [hnew, nativeK5GraphShellingWord_NCount_one]
  norm_num

/-- Every OLD N-preserving P94A 4-cell word kernel still obstructs
the genuine corrected Type-valued nine-face cycle. -/
theorem nativeK5NineReorientedWord_not_mem_P94ATyped :
    nativeK5NineReorientedWord t1 t2 t3 t4 t5 ∉
      nativeK5P94ATypedNormalClosure D E := by
  intro h
  have hz := nativeK5P94ATypedNormalClosure_le_NCount_ker (D := D) (E := E) h
  change nativeK5NaturalityCount
      (nativeK5NineReorientedWord t1 t2 t3 t4 t5) = 0 at hz
  have hN : nativeK5NaturalityCount
      (nativeK5NineReorientedWord t1 t2 t3 t4 t5) = 3 := by
    rw [← nativeK5NineReorientedExtendedCycle_word]
    exact nativeK5NineReorientedExtendedCycle_NCount_three t1 t2 t3 t4 t5
  rw [hN] at hz
  norm_num at hz

/-- Gauge reframing preserves the genuine new nine-face source
boundary obstruction +3 and the entire old full-shadow zero. -/
theorem nativeK5NineReorientedGaugeObstruction
    (g : NativeF55P94CWord) :
    nativeF55P94CWordToShadow
      (nativeK5GaugeReframe g
        (nativeK5NineReorientedExtendedCycle t1 t2 t3 t4 t5).p94cGroupWord) = 0 ∧
    nativeK5NaturalityCount
      (nativeK5GaugeReframe g
        (nativeK5NineReorientedExtendedCycle t1 t2 t3 t4 t5).p94cGroupWord) = 3 := by
  constructor
  · rw [nativeK5GaugeReframe_shadow,
      nativeK5NineReorientedExtendedCycle_shadow_zero]
  · rw [nativeK5GaugeReframe_NCount,
      nativeK5NineReorientedExtendedCycle_NCount_three]

#print axioms NativeF55StructuralComparison.reverse
#print axioms NativeF55StructuralComparison.reverse_word
#print axioms nativeK5NaturalitySquare2ForwardExtendedFace
#print axioms nativeK5NaturalitySquare2ForwardExtendedFace_word
#print axioms nativeK5NaturalitySquare2ForwardExtendedFace_NCount_one
#print axioms nativeK5FirstSevenExtendedStructuralPasting_NCount_two
#print axioms nativeK5NineReorientedExtendedCycle
#print axioms nativeK5NineReorientedExtendedCycle_word
#print axioms nativeK5NineReorientedExtendedCycle_NCount_three
#print axioms nativeK5NineReorientedExtendedCycle_shadow_zero
#print axioms nativeK5GraphShellingWord_prefix_square2_suffix
#print axioms nativeK5NineReorientedWord_relative_correction
#print axioms nativeK5NineReorientedWord_relative_NCount_two
#print axioms nativeK5NineReorientedWord_not_mem_P94ATyped
#print axioms nativeK5NineReorientedGaugeObstruction

end FiveNativeStages
end
end Kuu.F112.Physical
