import Kuu.F112.PolygonNativeF55P94DK5NaturalitySquare2TypedOrientation
import Mathlib.Tactic

/-!
# F112-P94D3R: eight genuine typed K5 faces and square2 gap

The original eight existing P92B faces on the shelling except k=7
really CAN be composed as one source-dependent F54/structural F55
three-cell along 0->3->2->4->8->7->6->5 (seven faces),
and then after k=8's genuine 1->0 pentagon4 (eight faces).
Thus the resulting second boundary is genuinely path1 -> path5.

The original P92B symm-square2 is a DIFFERENT genuine 3-cell
from path1 -> path5. Both are Type-valued, and every original
P92B generator is faithfully embedded. Their FULL ordered free
group words are separately recorded, with N-count 2 and -1.
They cannot be identified by any N-count-preserving 4-cell.

Importantly, this pair is NOT the old ordered nine-face shelling
cycle: the original shelling is 0->...->5->1->0 and its last
square2 source/target structural seams DO NOT exist.
The original formal word W still has chi=0 and N=1; never
silently replace its oriented meaning by the alternative
two-parallel-3-cells boundary or claim a 4D filler.

No Gray, sorry/admit, added axioms, weakened 107 roots or fake
descent into old P92B.
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

/-- All first SEVEN oriented genuine source 3-cells, in the
exact original ordered face sequence 7,0,5,8,1,3,6, provide
a real Type-valued 0->5 comparison in the new presentation. -/
def nativeK5FirstSevenExtendedStructuralPasting :
    NativeF55StructuralComparison p
      (nativeK5TypedGlobalF54Route t1 t2 t3 t4 t5 0)
      (nativeK5TypedGlobalF54Route t1 t2 t3 t4 t5 5) :=
  .trans
    (.trans
      (.trans
        (.trans
          (.trans
            (.trans
              (nativeK5FirstExtendedTypedFace t1 t2 t3 t4 t5)
              (nativeK5NaturalitySquare0ExtendedFace t1 t2 t3 t4 t5))
            (nativeK5Pentagon5ExtendedFace t1 t2 t3 t4 t5))
          (nativeK5Pentagon8ExtendedContextFace t1 t2 t3 t4 t5))
        (nativeK5NaturalitySquare1ExtendedFace t1 t2 t3 t4 t5))
      (nativeK5Pentagon3ExtendedContextFace t1 t2 t3 t4 t5))
    (nativeK5Pentagon6ExtendedFace t1 t2 t3 t4 t5)

/-- The EXACT seven-face ordered P/N group word.
Each group letter originates from its genuine anchored P92B 3-cell. -/
def nativeK5FirstSevenAnchoredWord : NativeF55P94CWord :=
  (nativeK5AnchoredFace t1 t2 t3 t4 t5 .pentagon7).2.2.2.p94cGroupWord +
  (nativeK5AnchoredFace t1 t2 t3 t4 t5 .square0).2.2.2.p94cGroupWord +
  (nativeK5AnchoredFace t1 t2 t3 t4 t5 .pentagon5).2.2.2.p94cGroupWord +
  (nativeK5AnchoredFace t1 t2 t3 t4 t5 .pentagon8).2.2.2.p94cGroupWord +
  (nativeK5AnchoredFace t1 t2 t3 t4 t5 .square1).2.2.2.p94cGroupWord +
  (nativeK5AnchoredFace t1 t2 t3 t4 t5 .pentagon3).2.2.2.p94cGroupWord +
  (nativeK5AnchoredFace t1 t2 t3 t4 t5 .pentagon6).2.2.2.p94cGroupWord

theorem nativeK5FirstSevenExtendedStructuralPasting_word :
    (nativeK5FirstSevenExtendedStructuralPasting t1 t2 t3 t4 t5).p94cGroupWord =
      nativeK5FirstSevenAnchoredWord t1 t2 t3 t4 t5 := by
  simp only [nativeK5FirstSevenExtendedStructuralPasting,
    NativeF55StructuralComparison.p94cGroupWord,
    nativeK5FirstSevenAnchoredWord]
  rw [nativeK5FirstExtendedTypedFace_word,
    nativeK5NaturalitySquare0ExtendedFace_word,
    nativeK5Pentagon5ExtendedFace_word,
    nativeK5Pentagon8ExtendedContextFace_word,
    nativeK5NaturalitySquare1ExtendedFace_word,
    nativeK5Pentagon3ExtendedContextFace_word,
    nativeK5Pentagon6ExtendedFace_word]

/-- Genuine eight-face long boundary in the other connected order:
pentagon4 followed by pentagon7, square0, pentagon5, pentagon8,
square1, pentagon3, pentagon6; both endpoints are true path1/5. -/
def nativeK5EightExtendedStructuralPasting :
    NativeF55StructuralComparison p
      (nativeK5TypedGlobalF54Route t1 t2 t3 t4 t5 1)
      (nativeK5TypedGlobalF54Route t1 t2 t3 t4 t5 5) :=
  .trans
    (nativeK5Pentagon4ExtendedFace t1 t2 t3 t4 t5)
    (nativeK5FirstSevenExtendedStructuralPasting t1 t2 t3 t4 t5)

/-- Exactly the true eight-face word, preserving all ordering. -/
def nativeK5EightAnchoredParallelWord : NativeF55P94CWord :=
  (nativeK5AnchoredFace t1 t2 t3 t4 t5 .pentagon4).2.2.2.p94cGroupWord +
    nativeK5FirstSevenAnchoredWord t1 t2 t3 t4 t5

theorem nativeK5EightExtendedStructuralPasting_word :
    (nativeK5EightExtendedStructuralPasting t1 t2 t3 t4 t5).p94cGroupWord =
      nativeK5EightAnchoredParallelWord t1 t2 t3 t4 t5 := by
  change
    (nativeK5Pentagon4ExtendedFace t1 t2 t3 t4 t5).p94cGroupWord +
    (nativeK5FirstSevenExtendedStructuralPasting t1 t2 t3 t4 t5).p94cGroupWord =
      (nativeK5AnchoredFace t1 t2 t3 t4 t5 .pentagon4).2.2.2.p94cGroupWord +
        nativeK5FirstSevenAnchoredWord t1 t2 t3 t4 t5
  rw [nativeK5Pentagon4ExtendedFace_word,
      nativeK5FirstSevenExtendedStructuralPasting_word]

/-- The true eight-face long path contains BOTH positively oriented
original P92B naturality generators: its N charge is +2. -/
theorem nativeK5EightExtendedStructuralPasting_NCount_two :
    nativeK5NaturalityCount
      (nativeK5EightExtendedStructuralPasting t1 t2 t3 t4 t5).p94cGroupWord =
        2 := by
  rw [nativeK5EightExtendedStructuralPasting_word]
  simp only [nativeK5EightAnchoredParallelWord,
    nativeK5FirstSevenAnchoredWord, map_add]
  change
    nativeK5AnchoredFaceNCount t1 t2 t3 t4 t5 .pentagon4 +
    (nativeK5AnchoredFaceNCount t1 t2 t3 t4 t5 .pentagon7 +
    nativeK5AnchoredFaceNCount t1 t2 t3 t4 t5 .square0 +
    nativeK5AnchoredFaceNCount t1 t2 t3 t4 t5 .pentagon5 +
    nativeK5AnchoredFaceNCount t1 t2 t3 t4 t5 .pentagon8 +
    nativeK5AnchoredFaceNCount t1 t2 t3 t4 t5 .square1 +
    nativeK5AnchoredFaceNCount t1 t2 t3 t4 t5 .pentagon3 +
    nativeK5AnchoredFaceNCount t1 t2 t3 t4 t5 .pentagon6) = 2
  simp [nativeK5AnchoredFaceNCount_exact, nativeK5FaceExpectedNCount]

/-- TWO genuinely typed, PARALLEL extended P92B three-cell
presentations now exist from the SAME F54 path1 to path5.
There is NO declared four-cell between them. -/
def nativeK5Square2ParallelThreeCellBoundary :
    (NativeF55StructuralComparison p
       (nativeK5TypedGlobalF54Route t1 t2 t3 t4 t5 1)
       (nativeK5TypedGlobalF54Route t1 t2 t3 t4 t5 5)) ×
    (NativeF55StructuralComparison p
       (nativeK5TypedGlobalF54Route t1 t2 t3 t4 t5 1)
       (nativeK5TypedGlobalF54Route t1 t2 t3 t4 t5 5)) :=
  (nativeK5EightExtendedStructuralPasting t1 t2 t3 t4 t5,
   nativeK5NaturalitySquare2ReverseExtendedFace t1 t2 t3 t4 t5)

/-- Even though source and target F54 boundaries MATCH, the
chosen two 3-cell presentations have distinct exact ordered
noncommutative words, as witnessed by their N charges (+2 vs -1).
This comparison cannot be an old N-preserving 4-cell. -/
theorem nativeK5Square2ParallelThreeCell_word_ne :
    (nativeK5EightExtendedStructuralPasting t1 t2 t3 t4 t5).p94cGroupWord ≠
      (nativeK5NaturalitySquare2ReverseExtendedFace t1 t2 t3 t4 t5).p94cGroupWord := by
  intro h
  have hn := congrArg nativeK5NaturalityCount h
  rw [nativeK5EightExtendedStructuralPasting_NCount_two,
      nativeK5NaturalitySquare2ReverseExtendedFace_NCount_minus_one] at hn
  omega

/-- A faithful, nine-face shelling made ONLY of the adjoined
F54 STRUCTURAL seams needs both genuine source and target
certificates for every original oriented P92B face. This is a
Type-valued proof obligation, not a declarative coherence axiom. -/
structure NativeK5StructuralShellingSeamDatum where
  source : ∀ k : Fin 9,
    NativeF54StructuralSeam p
      (nativeK5TypedGlobalF54Route t1 t2 t3 t4 t5
        (nativeK5GraphShellingStep k).source)
      (nativeK5WhiskeredFaceSource t1 t2 t3 t4 t5
        (nativeK5FaceTagOfFin (nativeK5GraphShellingStep k).face))
  target : ∀ k : Fin 9,
    NativeF54StructuralSeam p
      (nativeK5TypedGlobalF54Route t1 t2 t3 t4 t5
        (nativeK5GraphShellingStep k).target)
      (nativeK5WhiskeredFaceTarget t1 t2 t3 t4 t5
        (nativeK5FaceTagOfFin (nativeK5GraphShellingStep k).face))

/-- The ORIGINAL nine-face path0->...->path0 shelling is
uninhabited under these structural seam rules: k=7 requests
path5 -> source-square2 despite its truly typed source being
path1 -> path5. This does not prohibit OTHER presentations;
it is a precise non-descent/compatibility obstruction. -/
theorem nativeK5StructuralShellingSeamDatum_no_go :
    ¬ Nonempty (NativeK5StructuralShellingSeamDatum t1 t2 t3 t4 t5) := by
  rintro ⟨d⟩
  have h : NativeF54StructuralSeam p
      (nativeK5TypedGlobalF54Route t1 t2 t3 t4 t5 5)
      (nativeK5WhiskeredFaceSource t1 t2 t3 t4 t5 .square2) := by
    simpa only [nativeK5GraphShellingStep, nativeK5FaceTagOfFin] using d.source 7
  exact nativeK5NaturalitySquare2NoOutwardSourceSeam t1 t2 t3 t4 t5 ⟨h⟩

#print axioms nativeK5FirstSevenExtendedStructuralPasting
#print axioms nativeK5FirstSevenExtendedStructuralPasting_word
#print axioms nativeK5EightExtendedStructuralPasting
#print axioms nativeK5EightExtendedStructuralPasting_word
#print axioms nativeK5EightExtendedStructuralPasting_NCount_two
#print axioms nativeK5Square2ParallelThreeCellBoundary
#print axioms nativeK5Square2ParallelThreeCell_word_ne
#print axioms nativeK5StructuralShellingSeamDatum_no_go

end FiveNativeStages
end
end Kuu.F112.Physical
