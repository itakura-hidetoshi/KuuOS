import Kuu.F112.PolygonNativeF55P94DK5GlobalNineFaceShelling
import Mathlib.Tactic

/-!
# F112-P94D3I — nine-face shelling word and conditional genuine pentagonator

The P94D3I oriented shelling has face order 7,0,5,8,1,3,6,2,4.
Its ordered NONCOMMUTATIVE word must not be identified with the
different tag-order FORMAL word from P94D3H merely because both
have N-charge +1 and original F55 shadow zero.

A genuine global typed three-pasting requires MORE than the proven
graph shelling: a common dependent F54 route for each global path,
and actual P92B 3-cells whiskered/transported from the anchored faces
between consecutive routes.  Record these as explicit, uninhabited-
until-constructed Type-level obligations.  Conditional on the data,
build a genuine nine-step typed closed three-cell and prove that the
old P94C2 four-cell grammar cannot fill it.  Introduce the extra
pentagonator only as a constructor in a DIFFERENT source presentation,
not as a retroactive witness of the old one.

No unconditional global F54 pasting, strict 3/n or hyperdescent claim.
No Gray, sorry, admit, or new Lean logical axioms.
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

/-- The nine TRUE anchored P92B witnesses, but concatenated in
the physically realizable outward GRAPH-SHELLING order.
Still a free word, not a claimed typed global three-cell. -/
def nativeK5GraphShellingWord : NativeF55P94CWord :=
  (nativeK5AnchoredFace t1 t2 t3 t4 t5 .pentagon7).2.2.2.p94cGroupWord +
  (nativeK5AnchoredFace t1 t2 t3 t4 t5 .square0).2.2.2.p94cGroupWord +
  (nativeK5AnchoredFace t1 t2 t3 t4 t5 .pentagon5).2.2.2.p94cGroupWord +
  (nativeK5AnchoredFace t1 t2 t3 t4 t5 .pentagon8).2.2.2.p94cGroupWord +
  (nativeK5AnchoredFace t1 t2 t3 t4 t5 .square1).2.2.2.p94cGroupWord +
  (nativeK5AnchoredFace t1 t2 t3 t4 t5 .pentagon3).2.2.2.p94cGroupWord +
  (nativeK5AnchoredFace t1 t2 t3 t4 t5 .pentagon6).2.2.2.p94cGroupWord +
  (nativeK5AnchoredFace t1 t2 t3 t4 t5 .square2).2.2.2.p94cGroupWord +
  (nativeK5AnchoredFace t1 t2 t3 t4 t5 .pentagon4).2.2.2.p94cGroupWord

/-- The outward global graph shelling retains signed N-charge +1. -/
theorem nativeK5GraphShellingWord_NCount_one :
    nativeK5NaturalityCount
      (nativeK5GraphShellingWord t1 t2 t3 t4 t5) = 1 := by
  simp only [nativeK5GraphShellingWord, map_add]
  change
    nativeK5AnchoredFaceNCount t1 t2 t3 t4 t5 .pentagon7 +
    nativeK5AnchoredFaceNCount t1 t2 t3 t4 t5 .square0 +
    nativeK5AnchoredFaceNCount t1 t2 t3 t4 t5 .pentagon5 +
    nativeK5AnchoredFaceNCount t1 t2 t3 t4 t5 .pentagon8 +
    nativeK5AnchoredFaceNCount t1 t2 t3 t4 t5 .square1 +
    nativeK5AnchoredFaceNCount t1 t2 t3 t4 t5 .pentagon3 +
    nativeK5AnchoredFaceNCount t1 t2 t3 t4 t5 .pentagon6 +
    nativeK5AnchoredFaceNCount t1 t2 t3 t4 t5 .square2 +
    nativeK5AnchoredFaceNCount t1 t2 t3 t4 t5 .pentagon4 = 1
  simp [nativeK5AnchoredFaceNCount_exact, nativeK5FaceExpectedNCount]

/-- The COMPLETE old (signed pentagon, square, odd-phase) shadow
still vanishes for the new genuinely oriented cyclic word. -/
theorem nativeK5GraphShellingWord_shadow_zero :
    nativeF55P94CWordToShadow
      (nativeK5GraphShellingWord t1 t2 t3 t4 t5) = 0 := by
  simp only [nativeK5GraphShellingWord, map_add,
    NativeF55P92AssocComparison.p94cGroupWord_shadow]
  simp [nativeK5AnchoredFace_fullShadow, nativeK5CandidateFaceShadow,
    nativeK5FaceTagFin]

/-- This NEW cyclic order cannot lie in the old P94A normal
kernel: the independent N-obstruction is still 1. -/
theorem nativeK5GraphShellingWord_not_mem_P94ATyped :
    nativeK5GraphShellingWord t1 t2 t3 t4 t5 ∉
      nativeK5P94ATypedNormalClosure D E := by
  intro h
  have hz := nativeK5P94ATypedNormalClosure_le_NCount_ker (D := D) (E := E) h
  change nativeK5NaturalityCount
    (nativeK5GraphShellingWord t1 t2 t3 t4 t5) = 0 at hz
  rw [nativeK5GraphShellingWord_NCount_one] at hz
  norm_num at hz

/-- Actual dependent F54 route *type*, shared by all nine global
13-to-0 graph spines, whose construction from the 21 original typed
edge routes is an independent next step. -/
abbrev NativeK5GlobalRoute :=
  KuuNativeF45Tree.DepthRotationRoute p
    (nativeK5TypedVertex t1 t2 t3 t4 t5 (13 : Fin 14)).2.2
    (nativeK5TypedVertex t1 t2 t3 t4 t5 (0 : Fin 14)).2.2

/-- A genuine TYPE-valued nine-face shelling requires chosen native
F54 realizations of the nine directed graph paths and an actual
P92B proof from each route to its next, with the exact original
anchored face word.  NONE of this data is manufactured from the
graph-level equalities or from shadows.  No instance is asserted. -/
structure NativeK5TypedShellingDatum where
  routes : Fin 9 → NativeK5GlobalRoute t1 t2 t3 t4 t5
  faces : ∀ k : Fin 9,
    NativeF55P92AssocComparison p
      (routes (nativeK5GraphShellingStep k).source)
      (routes (nativeK5GraphShellingStep k).target)
  face_word : ∀ k : Fin 9,
    (faces k).p94cGroupWord =
      (nativeK5AnchoredFace t1 t2 t3 t4 t5
        (nativeK5FaceTagOfFin (nativeK5GraphShellingStep k).face)).2.2.2.p94cGroupWord

/-- GIVEN every actual dependent F54 transport and proof-relevant
face whiskering, the whole nine-face sphere yields one genuine
TYPE-valued P92B three-cell loop at a single F54 route. -/
def NativeK5TypedShellingDatum.cycle
    (d : NativeK5TypedShellingDatum t1 t2 t3 t4 t5) :
    NativeF55P92AssocComparison p (d.routes 0) (d.routes 0) :=
  .trans
    (.trans
      (.trans
        (.trans
          (.trans
            (.trans
              (.trans
                (.trans (d.faces 0) (d.faces 1))
                (d.faces 2))
              (d.faces 3))
            (d.faces 4))
          (d.faces 5))
        (d.faces 6))
      (d.faces 7))
    (d.faces 8)

/-- Exact ordered free-word consequence of a REAL supplied 3-cell
pasting datum, not an identification inferred from graph or shadow. -/
theorem NativeK5TypedShellingDatum.cycle_word
    (d : NativeK5TypedShellingDatum t1 t2 t3 t4 t5) :
    d.cycle.p94cGroupWord =
      nativeK5GraphShellingWord t1 t2 t3 t4 t5 := by
  simp only [NativeK5TypedShellingDatum.cycle,
    NativeF55P92AssocComparison.p94cGroupWord,
    nativeK5GraphShellingWord]
  apply congrArg₂ (fun (u v : NativeF55P94CWord) => u + v)
  · apply congrArg₂ (fun (u v : NativeF55P94CWord) => u + v)
    · apply congrArg₂ (fun (u v : NativeF55P94CWord) => u + v)
      · apply congrArg₂ (fun (u v : NativeF55P94CWord) => u + v)
        · apply congrArg₂ (fun (u v : NativeF55P94CWord) => u + v)
          · apply congrArg₂ (fun (u v : NativeF55P94CWord) => u + v)
            · apply congrArg₂ (fun (u v : NativeF55P94CWord) => u + v)
              · apply congrArg₂ (fun (u v : NativeF55P94CWord) => u + v)
                · simpa only [nativeK5GraphShellingStep, nativeK5FaceTagOfFin] using d.face_word 0
                · simpa only [nativeK5GraphShellingStep, nativeK5FaceTagOfFin] using d.face_word 1
              · simpa only [nativeK5GraphShellingStep, nativeK5FaceTagOfFin] using d.face_word 2
            · simpa only [nativeK5GraphShellingStep, nativeK5FaceTagOfFin] using d.face_word 3
          · simpa only [nativeK5GraphShellingStep, nativeK5FaceTagOfFin] using d.face_word 4
        · simpa only [nativeK5GraphShellingStep, nativeK5FaceTagOfFin] using d.face_word 5
      · simpa only [nativeK5GraphShellingStep, nativeK5FaceTagOfFin] using d.face_word 6
    · simpa only [nativeK5GraphShellingStep, nativeK5FaceTagOfFin] using d.face_word 7
  · simpa only [nativeK5GraphShellingStep, nativeK5FaceTagOfFin] using d.face_word 8

theorem NativeK5TypedShellingDatum.cycle_NCount_one
    (d : NativeK5TypedShellingDatum t1 t2 t3 t4 t5) :
    nativeK5NaturalityCount d.cycle.p94cGroupWord = 1 := by
  rw [d.cycle_word, nativeK5GraphShellingWord_NCount_one]

/-- The existing genuine P94C2 four-cell syntax CANNOT
fill this typed closed nine-face cycle, IF the required global
F54 transport / P92B whiskering data is actually constructed.
The claim is conditional on that data; it does not posit it. -/
theorem NativeK5TypedShellingDatum.no_P94C2_filling
    (d : NativeK5TypedShellingDatum t1 t2 t3 t4 t5)
    (four : NativeF55P94CGroupFourCell
      d.cycle (NativeF55P92AssocComparison.refl (d.routes 0))) : False := by
  have h := four.nCount_sound
  rw [d.cycle_NCount_one] at h
  change (1 : ℤ) = 0 at h
  norm_num at h

/-- A DISTINCT typed 4-cell presentation containing the additional
pentagonator generator.  Its constructor is available ONLY AFTER
a genuine NativeK5TypedShellingDatum has been given; it is NOT a
new axiom and does NOT build the missing nine-face whiskerings.
Closure/coherence and the pentagonator-Peiffer relation are
independent subsequent proof obligations. -/
inductive NativeK5IndependentPentagonator
    (d : NativeK5TypedShellingDatum t1 t2 t3 t4 t5) :
    NativeF55P92AssocComparison p (d.routes 0) (d.routes 0) →
    NativeF55P92AssocComparison p (d.routes 0) (d.routes 0) →
      Type (max (max uD uE) (max vD vE)) where
  | generator :
    NativeK5IndependentPentagonator d
      d.cycle (NativeF55P92AssocComparison.refl (d.routes 0))

#print axioms nativeK5GraphShellingWord_NCount_one
#print axioms nativeK5GraphShellingWord_shadow_zero
#print axioms nativeK5GraphShellingWord_not_mem_P94ATyped
#print axioms NativeK5TypedShellingDatum.cycle
#print axioms NativeK5TypedShellingDatum.cycle_word
#print axioms NativeK5TypedShellingDatum.cycle_NCount_one
#print axioms NativeK5TypedShellingDatum.no_P94C2_filling
#print axioms NativeK5IndependentPentagonator

end FiveNativeStages
end
end Kuu.F112.Physical
