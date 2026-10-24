import Kuu.F112.PolygonNativeF55P94DK5TypedStructuralSeam
import Mathlib.Tactic

/-!
# F112-P94D3M: more genuine Type-valued K5 F54 structural seams

The exact old F54 tagged-route terms now give actual structural
seams for three additional original outward K5 pentagon faces:
k=2 (pentagon5), k=6 (pentagon6), k=8 (pentagon4).
With P94D3L's k=0 (pentagon7), four of the nine actual faces
have concrete Type-valued source and target seam certificates.

All rebracketings are the explicit F54 structural comparison
presentation, NOT an old P92B equality or a graph-derived filler.
The genuine oriented P92B face is embedded without changing its
complete noncommutative P/N word. Its independent N-charge
and the old F55 shadow are therefore preserved.

The remaining context faces k=3,5 and naturality squares k=1,4,7
still require typed normalization; no global three-sphere, old P92B
seam existence, 4D Peiffer coherence, strict 3/n, or hyperdescent
is asserted. No Gray, sorry/admit, new axioms or root deletions.
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

/-- Generic genuine face transport IN THE DISTINCT EXTENDED
Type-valued comparison. Both seams must be provided as true typed
structural witnesses; the raw P92B face is used unchanged. -/
def nativeK5StructuralGluedFace
    (tag : NativeK5FaceTag)
    (u v : NativeK5GlobalRoute t1 t2 t3 t4 t5)
    (hs : NativeF54StructuralSeam p u
      (nativeK5WhiskeredFaceSource t1 t2 t3 t4 t5 tag))
    (ht : NativeF54StructuralSeam p v
      (nativeK5WhiskeredFaceTarget t1 t2 t3 t4 t5 tag)) :
    NativeF55StructuralComparison p u v :=
  .trans
    (.trans (.structural hs)
      (.original (nativeK5WhiskeredGenuineFace t1 t2 t3 t4 t5 tag)))
    (.structural (.symm ht))

/-- Entire noncommutative group word is preserved by EACH
typed seam pasting, not just its abelian shadow or N-count. -/
theorem nativeK5StructuralGluedFace_word
    (tag : NativeK5FaceTag)
    (u v : NativeK5GlobalRoute t1 t2 t3 t4 t5)
    (hs : NativeF54StructuralSeam p u
      (nativeK5WhiskeredFaceSource t1 t2 t3 t4 t5 tag))
    (ht : NativeF54StructuralSeam p v
      (nativeK5WhiskeredFaceTarget t1 t2 t3 t4 t5 tag)) :
    (nativeK5StructuralGluedFace t1 t2 t3 t4 t5 tag u v hs ht).p94cGroupWord =
      (nativeK5AnchoredFace t1 t2 t3 t4 t5 tag).2.2.2.p94cGroupWord := by
  change 0 +
    (nativeK5WhiskeredGenuineFace t1 t2 t3 t4 t5 tag).p94cGroupWord + 0 =
    (nativeK5AnchoredFace t1 t2 t3 t4 t5 tag).2.2.2.p94cGroupWord
  simpa using nativeK5WhiskeredGenuineFace_word t1 t2 t3 t4 t5 tag

/-- k=2, pentagon5: source 2→4 starts with the original e19
13→11 F54 step, followed by a genuine two-step local pentagon
and original e0 suffix. One reassociation, no graph inference. -/
def nativeK5Pentagon5SourceSeam :
    NativeF54StructuralSeam p
      (nativeK5TypedGlobalF54Route t1 t2 t3 t4 t5 2)
      (nativeK5WhiskeredFaceSource t1 t2 t3 t4 t5 .pentagon5) := by
  let e := nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5
  change NativeF54StructuralSeam p
    (.trans (e .e19) (.trans (e .e12) (.trans (e .e4) (e .e0))))
    (.trans (e .e19) (.trans (.trans (e .e12) (e .e4)) (e .e0)))
  exact .precompose (e .e19)
    (.symm (.reassoc (e .e12) (e .e4) (e .e0)))

/-- k=2, pentagon5 target: the original 3-step pentagon source
history is NOT permuted; two pure reassociations compare its
left-nested source with the chosen right-nested global F54 route. -/
def nativeK5Pentagon5TargetSeam :
    NativeF54StructuralSeam p
      (nativeK5TypedGlobalF54Route t1 t2 t3 t4 t5 4)
      (nativeK5WhiskeredFaceTarget t1 t2 t3 t4 t5 .pentagon5) := by
  let e := nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5
  change NativeF54StructuralSeam p
    (.trans (e .e19)
      (.trans (e .e17) (.trans (e .e8) (.trans (e .e3) (e .e0)))))
    (.trans (e .e19)
      (.trans (.trans (.trans (e .e17) (e .e8)) (e .e3)) (e .e0)))
  exact .precompose (e .e19)
    (.trans
      (.symm (.reassoc (e .e17) (e .e8)
        (.trans (e .e3) (e .e0))))
      (.symm (.reassoc (.trans (e .e17) (e .e8)) (e .e3) (e .e0))))

/-- k=6, pentagon6: the genuine original 3-step F55 long leg
from 12 to 2, with original e20 prefix and e1 suffix. -/
def nativeK5Pentagon6SourceSeam :
    NativeF54StructuralSeam p
      (nativeK5TypedGlobalF54Route t1 t2 t3 t4 t5 6)
      (nativeK5WhiskeredFaceSource t1 t2 t3 t4 t5 .pentagon6) := by
  let e := nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5
  change NativeF54StructuralSeam p
    (.trans (e .e20)
      (.trans (e .e18) (.trans (e .e9) (.trans (e .e5) (e .e1)))))
    (.trans (e .e20)
      (.trans (.trans (.trans (e .e18) (e .e9)) (e .e5)) (e .e1)))
  exact .precompose (e .e20)
    (.trans
      (.symm (.reassoc (e .e18) (e .e9)
        (.trans (e .e5) (e .e1))))
      (.symm (.reassoc (.trans (e .e18) (e .e9)) (e .e5) (e .e1))))

/-- k=6, pentagon6 target: the native e14;e6 short pentagon
transport followed by actual e1, with its real e20 prefix. -/
def nativeK5Pentagon6TargetSeam :
    NativeF54StructuralSeam p
      (nativeK5TypedGlobalF54Route t1 t2 t3 t4 t5 5)
      (nativeK5WhiskeredFaceTarget t1 t2 t3 t4 t5 .pentagon6) := by
  let e := nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5
  change NativeF54StructuralSeam p
    (.trans (e .e20) (.trans (e .e14) (.trans (e .e6) (e .e1))))
    (.trans (e .e20) (.trans (.trans (e .e14) (e .e6)) (e .e1)))
  exact .precompose (e .e20)
    (.symm (.reassoc (e .e14) (e .e6) (e .e1)))

/-- k=8, pentagon4: original positive long leg plus a REAL
identity suffix at vertex 0. Two reassociations and right unit. -/
def nativeK5Pentagon4SourceSeam :
    NativeF54StructuralSeam p
      (nativeK5TypedGlobalF54Route t1 t2 t3 t4 t5 1)
      (nativeK5WhiskeredFaceSource t1 t2 t3 t4 t5 .pentagon4) := by
  let e := nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5
  change NativeF54StructuralSeam p
    (.trans (e .e15) (.trans (e .e13) (.trans (e .e6) (e .e1))))
    (.trans (e .e15)
      (.trans (.trans (.trans (e .e13) (e .e6)) (e .e1))
        (.chain (.refl _))))
  exact .precompose (e .e15)
    (.trans
      (.symm (.reassoc (e .e13) (e .e6) (e .e1)))
      (.symm (.rightUnit _)))

/-- k=8, pentagon4 target: actual e11;e2 short pentagon,
one independent right-unit normalization. -/
def nativeK5Pentagon4TargetSeam :
    NativeF54StructuralSeam p
      (nativeK5TypedGlobalF54Route t1 t2 t3 t4 t5 0)
      (nativeK5WhiskeredFaceTarget t1 t2 t3 t4 t5 .pentagon4) := by
  let e := nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5
  change NativeF54StructuralSeam p
    (.trans (e .e15) (.trans (e .e11) (e .e2)))
    (.trans (e .e15) (.trans (.trans (e .e11) (e .e2))
      (.chain (.refl _))))
  exact .precompose (e .e15)
    (.symm (.rightUnit _))

/-- Unconditional NEW-presentation source-typed K5 3-cell
for k=2 / outward pentagon5, retaining its original F55 proof. -/
def nativeK5Pentagon5ExtendedFace :
    NativeF55StructuralComparison p
      (nativeK5TypedGlobalF54Route t1 t2 t3 t4 t5 2)
      (nativeK5TypedGlobalF54Route t1 t2 t3 t4 t5 4) :=
  nativeK5StructuralGluedFace t1 t2 t3 t4 t5 .pentagon5 _ _
    (nativeK5Pentagon5SourceSeam t1 t2 t3 t4 t5)
    (nativeK5Pentagon5TargetSeam t1 t2 t3 t4 t5)

/-- Unconditional NEW-presentation source-typed K5 3-cell
for k=6 / outward pentagon6. -/
def nativeK5Pentagon6ExtendedFace :
    NativeF55StructuralComparison p
      (nativeK5TypedGlobalF54Route t1 t2 t3 t4 t5 6)
      (nativeK5TypedGlobalF54Route t1 t2 t3 t4 t5 5) :=
  nativeK5StructuralGluedFace t1 t2 t3 t4 t5 .pentagon6 _ _
    (nativeK5Pentagon6SourceSeam t1 t2 t3 t4 t5)
    (nativeK5Pentagon6TargetSeam t1 t2 t3 t4 t5)

/-- Unconditional NEW-presentation source-typed K5 3-cell
for k=8 / outward pentagon4. -/
def nativeK5Pentagon4ExtendedFace :
    NativeF55StructuralComparison p
      (nativeK5TypedGlobalF54Route t1 t2 t3 t4 t5 1)
      (nativeK5TypedGlobalF54Route t1 t2 t3 t4 t5 0) :=
  nativeK5StructuralGluedFace t1 t2 t3 t4 t5 .pentagon4 _ _
    (nativeK5Pentagon4SourceSeam t1 t2 t3 t4 t5)
    (nativeK5Pentagon4TargetSeam t1 t2 t3 t4 t5)

theorem nativeK5Pentagon5ExtendedFace_word :
    (nativeK5Pentagon5ExtendedFace t1 t2 t3 t4 t5).p94cGroupWord =
      (nativeK5AnchoredFace t1 t2 t3 t4 t5 .pentagon5).2.2.2.p94cGroupWord := by
  exact nativeK5StructuralGluedFace_word t1 t2 t3 t4 t5 .pentagon5 _ _ _ _

theorem nativeK5Pentagon6ExtendedFace_word :
    (nativeK5Pentagon6ExtendedFace t1 t2 t3 t4 t5).p94cGroupWord =
      (nativeK5AnchoredFace t1 t2 t3 t4 t5 .pentagon6).2.2.2.p94cGroupWord := by
  exact nativeK5StructuralGluedFace_word t1 t2 t3 t4 t5 .pentagon6 _ _ _ _

theorem nativeK5Pentagon4ExtendedFace_word :
    (nativeK5Pentagon4ExtendedFace t1 t2 t3 t4 t5).p94cGroupWord =
      (nativeK5AnchoredFace t1 t2 t3 t4 t5 .pentagon4).2.2.2.p94cGroupWord := by
  exact nativeK5StructuralGluedFace_word t1 t2 t3 t4 t5 .pentagon4 _ _ _ _

#print axioms nativeK5StructuralGluedFace_word
#print axioms nativeK5Pentagon5SourceSeam
#print axioms nativeK5Pentagon5TargetSeam
#print axioms nativeK5Pentagon6SourceSeam
#print axioms nativeK5Pentagon6TargetSeam
#print axioms nativeK5Pentagon4SourceSeam
#print axioms nativeK5Pentagon4TargetSeam
#print axioms nativeK5Pentagon5ExtendedFace_word
#print axioms nativeK5Pentagon6ExtendedFace_word
#print axioms nativeK5Pentagon4ExtendedFace_word

end FiveNativeStages
end
end Kuu.F112.Physical
