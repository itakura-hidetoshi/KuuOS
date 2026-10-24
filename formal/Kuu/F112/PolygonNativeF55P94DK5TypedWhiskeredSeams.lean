import Kuu.F112.PolygonNativeF55P94DK5TypedGlobalF54Routes
import Kuu.F112.PolygonNativeC60K5TypedGaugeCoherence
import Mathlib.Tactic

/-!
# F112-P94D3K: genuine F54 whiskering of all nine Type-valued K5 faces

Every original anchored P92B 3-cell is transported to the common
original 13-to-0 F45 endpoints via ACTUAL F54 typed prefixes and
suffixes built out of existing P94D1 edge witnesses. The
transported 3-cells preserve their EXACT ordered noncommutative
group words. This is unconditional, not inferred from a graph.

A remaining SEAM is an actual P92B proof comparing a whiskered
face leg to the independently constructed canonical global route.
The seam comparisons and their exact zero-word witnesses are
explicit Type-valued obligations; they are NOT filled using
shadow equality or graph equivalence. If supplied, they produce
the old conditional typed-shelling datum and its independent
pentagonator boundary without killing the +1 N-obstruction.

No Gray, sorry/admit, new axioms, or lost public roots.
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

/-- Every original face receives an actual F54 prefix from the
common global source 13 to its genuine anchored source. -/
def nativeK5TypedFacePrefix (tag : NativeK5FaceTag) :
    KuuNativeF45Tree.DepthRotationRoute p
      (nativeK5TypedVertex t1 t2 t3 t4 t5 (13 : Fin 14)).2.2
      (nativeK5TypedVertex t1 t2 t3 t4 t5
        (nativeK5AnchoredFace t1 t2 t3 t4 t5 tag).1.1).2.2 := by
  let e := nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5
  cases tag
  · exact .trans (e .e19) (e .e12)
  · exact .trans (e .e20) (e .e18)
  · exact nativeK5RouteUnit (nativeK5TypedVertex t1 t2 t3 t4 t5 13).2.2
  · exact .trans (e .e20) (.trans (e .e18) (e .e9))
  · exact e .e15
  · exact e .e19
  · exact e .e20
  · exact nativeK5RouteUnit (nativeK5TypedVertex t1 t2 t3 t4 t5 13).2.2
  · exact nativeK5RouteUnit (nativeK5TypedVertex t1 t2 t3 t4 t5 13).2.2

/-- The genuine F54 suffix, starting at each anchored face target
and ending at the common global endpoint 0. -/
def nativeK5TypedFaceSuffix (tag : NativeK5FaceTag) :
    KuuNativeF45Tree.DepthRotationRoute p
      (nativeK5TypedVertex t1 t2 t3 t4 t5
        (nativeK5AnchoredFace t1 t2 t3 t4 t5 tag).1.2).2.2
      (nativeK5TypedVertex t1 t2 t3 t4 t5 (0 : Fin 14)).2.2 := by
  let e := nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5
  cases tag
  · exact nativeK5RouteUnit (nativeK5TypedVertex t1 t2 t3 t4 t5 0).2.2
  · exact .trans (e .e3) (e .e0)
  · exact .trans (e .e6) (e .e1)
  · exact nativeK5RouteUnit (nativeK5TypedVertex t1 t2 t3 t4 t5 0).2.2
  · exact nativeK5RouteUnit (nativeK5TypedVertex t1 t2 t3 t4 t5 0).2.2
  · exact e .e0
  · exact e .e1
  · exact e .e2
  · exact .trans (e .e8) (.trans (e .e3) (e .e0))

/-- Genuine global F54 source leg of a selected original face:
the anchored source route, whiskered by original typed edge routes. -/
def nativeK5WhiskeredFaceSource (tag : NativeK5FaceTag) :
    NativeK5GlobalRoute t1 t2 t3 t4 t5 :=
  .trans (nativeK5TypedFacePrefix t1 t2 t3 t4 t5 tag)
    (.trans (nativeK5AnchoredFace t1 t2 t3 t4 t5 tag).2.1
      (nativeK5TypedFaceSuffix t1 t2 t3 t4 t5 tag))

/-- Genuine global F54 target leg of a selected original face. -/
def nativeK5WhiskeredFaceTarget (tag : NativeK5FaceTag) :
    NativeK5GlobalRoute t1 t2 t3 t4 t5 :=
  .trans (nativeK5TypedFacePrefix t1 t2 t3 t4 t5 tag)
    (.trans (nativeK5AnchoredFace t1 t2 t3 t4 t5 tag).2.2.1
      (nativeK5TypedFaceSuffix t1 t2 t3 t4 t5 tag))

/-- Actual Type-valued P92B 3-cell transported along those
genuine F54 routes. This is UNCONDITIONAL for all nine faces. -/
def nativeK5WhiskeredGenuineFace (tag : NativeK5FaceTag) :
    NativeF55P92AssocComparison p
      (nativeK5WhiskeredFaceSource t1 t2 t3 t4 t5 tag)
      (nativeK5WhiskeredFaceTarget t1 t2 t3 t4 t5 tag) :=
  .precompose (nativeK5TypedFacePrefix t1 t2 t3 t4 t5 tag)
    (.postcompose (nativeK5AnchoredFace t1 t2 t3 t4 t5 tag).2.2.2
      (nativeK5TypedFaceSuffix t1 t2 t3 t4 t5 tag))

/-- Whiskering preserves the FULL ordered NONCOMMUTATIVE word,
not only its integer naturality count or F55 abelian shadow. -/
theorem nativeK5WhiskeredGenuineFace_word (tag : NativeK5FaceTag) :
    (nativeK5WhiskeredGenuineFace t1 t2 t3 t4 t5 tag).p94cGroupWord =
      (nativeK5AnchoredFace t1 t2 t3 t4 t5 tag).2.2.2.p94cGroupWord := by
  rfl

/-- The remaining TYPE-level seam witnesses compare the real
whiskered F54 leg routes with the independently built nine
canonical global F54 routes. No numerical observer supplies them.

Zero-word properties are EXPLICIT separate requirements, since an
arbitrary Type-valued 3-cell may carry nonzero P/N charge. -/
structure NativeK5TypedSeamWitness where
  source : ∀ k : Fin 9,
    NativeF55P92AssocComparison p
      (nativeK5TypedGlobalF54Route t1 t2 t3 t4 t5
        (nativeK5GraphShellingStep k).source)
      (nativeK5WhiskeredFaceSource t1 t2 t3 t4 t5
        (nativeK5FaceTagOfFin (nativeK5GraphShellingStep k).face))
  target : ∀ k : Fin 9,
    NativeF55P92AssocComparison p
      (nativeK5WhiskeredFaceTarget t1 t2 t3 t4 t5
        (nativeK5FaceTagOfFin (nativeK5GraphShellingStep k).face))
      (nativeK5TypedGlobalF54Route t1 t2 t3 t4 t5
        (nativeK5GraphShellingStep k).target)
  source_word_zero : ∀ k : Fin 9, (source k).p94cGroupWord = 0
  target_word_zero : ∀ k : Fin 9, (target k).p94cGroupWord = 0

/-- ONLY actual Type-valued seam proof terms can assemble the
nine unconditional whiskered faces into a global three-cycle.
All chosen F54 global routes and every face whiskering itself
are now concrete, so the sole remaining input is the true seam. -/
def NativeK5TypedSeamWitness.toShellingDatum
    (w : NativeK5TypedSeamWitness t1 t2 t3 t4 t5) :
    NativeK5TypedShellingDatum t1 t2 t3 t4 t5 where
  routes := nativeK5TypedGlobalF54Routes t1 t2 t3 t4 t5
  faces := fun k =>
    .trans (.trans (w.source k)
      (nativeK5WhiskeredGenuineFace t1 t2 t3 t4 t5
        (nativeK5FaceTagOfFin (nativeK5GraphShellingStep k).face)))
      (w.target k)
  face_word := by
    intro k
    change (w.source k).p94cGroupWord +
      (nativeK5WhiskeredGenuineFace t1 t2 t3 t4 t5
        (nativeK5FaceTagOfFin (nativeK5GraphShellingStep k).face)).p94cGroupWord +
      (w.target k).p94cGroupWord =
      (nativeK5AnchoredFace t1 t2 t3 t4 t5
        (nativeK5FaceTagOfFin (nativeK5GraphShellingStep k).face)).2.2.2.p94cGroupWord
    rw [w.source_word_zero k, w.target_word_zero k,
      nativeK5WhiskeredGenuineFace_word]
    simp

/-- A genuine glued cycle, if the required Type-valued seams exist,
still has +1 N-charge under every algebraic gauge reframe. -/
theorem NativeK5TypedSeamWitness.gauge_NCount_one
    (w : NativeK5TypedSeamWitness t1 t2 t3 t4 t5)
    (g : NativeF55P94CWord) :
    nativeK5NaturalityCount
      (nativeK5GaugeReframe g
        (w.toShellingDatum.cycle.p94cGroupWord)) = 1 := by
  rw [nativeK5GaugeReframe_NCount,
    NativeK5TypedShellingDatum.cycle_word,
    nativeK5GraphShellingWord_NCount_one]

/-- Independent pentagonator boundary is *available in the new
presentation*, conditional on actual seams, not in old P94A/P94C2.
This is a constructor and NOT a Peiffer-coherence theorem. -/
def NativeK5TypedSeamWitness.independentPentagonator
    (w : NativeK5TypedSeamWitness t1 t2 t3 t4 t5) :
    NativeK5IndependentPentagonator t1 t2 t3 t4 t5 w.toShellingDatum
      w.toShellingDatum.cycle
      (NativeF55P92AssocComparison.refl
        (w.toShellingDatum.routes 0)) :=
  .generator

/-- The old P94C2 four-cell grammar cannot fill that SAME
Type-valued cycle, preserving the existing Peiffer obstruction. -/
theorem NativeK5TypedSeamWitness.no_old_Peiffer_filler
    (w : NativeK5TypedSeamWitness t1 t2 t3 t4 t5)
    (four : NativeF55P94CGroupFourCell
      w.toShellingDatum.cycle
      (NativeF55P92AssocComparison.refl
        (w.toShellingDatum.routes 0))) : False :=
  NativeK5TypedShellingDatum.no_P94C2_filling t1 t2 t3 t4 t5
    w.toShellingDatum four

#print axioms nativeK5TypedFacePrefix
#print axioms nativeK5TypedFaceSuffix
#print axioms nativeK5WhiskeredFaceSource
#print axioms nativeK5WhiskeredFaceTarget
#print axioms nativeK5WhiskeredGenuineFace
#print axioms nativeK5WhiskeredGenuineFace_word
#print axioms NativeK5TypedSeamWitness.toShellingDatum
#print axioms NativeK5TypedSeamWitness.gauge_NCount_one
#print axioms NativeK5TypedSeamWitness.independentPentagonator
#print axioms NativeK5TypedSeamWitness.no_old_Peiffer_filler

end FiveNativeStages
end
end Kuu.F112.Physical
