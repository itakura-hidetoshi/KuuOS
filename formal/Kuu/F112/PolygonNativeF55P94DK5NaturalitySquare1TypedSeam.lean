import Kuu.F112.PolygonNativeF55P94DK5NaturalitySquare0TypedSeam
import Mathlib.Tactic

/-!
# F112-P94D3P — genuine original K5 naturality square1 F54 seams

The actual P92B source associator-naturality face #1 uses an
original typed F54 associator in the SECOND argument and genuine
F54 identities in the first and third arguments. We normalize its
true P90 horizontal routes using proof-relevant F54 structural
unit/context transformations, rather than graph equality.

The resulting square source and target F54 routes are exactly
the original tagged-edge paths e16;e8 and e9;e7, respectively.
True 13→0 transport uses the original 13→12→10 prefix and
3→1→0 suffix, preserving all Nat depth casts, original F45
Blocks and genuine P92B 3-cell. The combined Type-valued face
lives in the distinctly named STRUCTURAL comparison presentation,
NOT in historical unextended P92B.

Original noncommutative P/N ordering and its naturality charge
are preserved. The last square and global Peiffer 4D coherence
remain independent obligations. No Gray, sorry/admit, added
logical axiom or replacement of original C60 geometry.
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

/-- Genuine F54 right-hand identity normalization in the distinct
source-level structural seam presentation, not route equality. -/
def nativeF54StructuralHorizontalRightUnit
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' k l : Nat}
    {p₀ p₁ p₂ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ : KuuNativeBlocks x y}
    {before : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
    {after : KuuNativeF45Tree p n' m' p₀ q₀ p₁ q₁}
    (route : KuuNativeF45Tree.DepthRotationRoute p before after)
    (later : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂) :
    NativeF54StructuralSeam p
      (nativeF54P90HorizontalRoute route (.chain (.refl later)))
      (.leftContext route later) :=
  .trans
    (.precompose (.leftContext route later) (.rightContextUnit after later))
    (.rightUnit (.leftContext route later))

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

/-- Genuine square1 local source: the P90 two-stage horizontal
transport normalizes to tagged e16;e8, NOT a graph inferred 3-cell. -/
def nativeK5NaturalitySquare1LocalSourceSeam :
    NativeF54StructuralSeam p
      (nativeK5AnchoredFace t1 t2 t3 t4 t5 .square1).2.1
      (.trans (nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5 .e16)
        (nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5 .e8)) := by
  let e := nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5
  let w := KuuNativeF45Tree.DepthRotationRoute.assoc t2 t3 t4
  let h12 := nativeF54P90HorizontalRoute (nativeK5RouteUnit t1) w
  let h := nativeF54P90HorizontalRoute h12 (nativeK5RouteUnit t5)
  have hh : NativeF54StructuralSeam p h (e .e16) :=
    .trans
      (nativeF54StructuralHorizontalRightUnit h12 t5)
      (.leftContextCongruence
        (nativeF54StructuralHorizontalLeftUnit t1 w) t5)
  change NativeF54StructuralSeam p (.trans h (e .e8))
    (.trans (e .e16) (e .e8))
  exact .postcompose hh (e .e8)

/-- Genuine square1 local target: its source associator followed
by the real P90 horizontal(natural,unit) route equals e9;e7
ONLY inside the chosen typed structural comparison source. -/
def nativeK5NaturalitySquare1LocalTargetSeam :
    NativeF54StructuralSeam p
      (nativeK5AnchoredFace t1 t2 t3 t4 t5 .square1).2.2.1
      (.trans (nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5 .e9)
        (nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5 .e7)) := by
  let e := nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5
  let w := KuuNativeF45Tree.DepthRotationRoute.assoc t2 t3 t4
  let h25 := nativeF54P90HorizontalRoute w (nativeK5RouteUnit t5)
  let h := nativeF54P90HorizontalRoute (nativeK5RouteUnit t1) h25
  have hh : NativeF54StructuralSeam p h (e .e7) :=
    .trans
      (nativeF54StructuralHorizontalLeftUnit t1 h25)
      (.rightContextCongruence t1
        (nativeF54StructuralHorizontalRightUnit w t5))
  change NativeF54StructuralSeam p (.trans (e .e9) h)
    (.trans (e .e9) (e .e7))
  exact .precompose (e .e9) hh

/-- True 13→0 local-to-global square1 source seam:
13→12→10 prefix, genuine e16;e8 square, 3→1→0 suffix. -/
def nativeK5NaturalitySquare1GlobalSourceSeam :
    NativeF54StructuralSeam p
      (nativeK5TypedGlobalF54Route t1 t2 t3 t4 t5 8)
      (nativeK5WhiskeredFaceSource t1 t2 t3 t4 t5 .square1) := by
  let e := nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5
  let preRoute := KuuNativeF45Tree.DepthRotationRoute.trans (e .e20) (e .e18)
  let localLong := KuuNativeF45Tree.DepthRotationRoute.trans (e .e16) (e .e8)
  let tail := KuuNativeF45Tree.DepthRotationRoute.trans (e .e3) (e .e0)
  change NativeF54StructuralSeam p
    (.trans (e .e20) (.trans (e .e18)
      (.trans (e .e16) (.trans (e .e8) tail))))
    (.trans preRoute
      (.trans (nativeK5AnchoredFace t1 t2 t3 t4 t5 .square1).2.1 tail))
  exact .trans
    (.symm (.reassoc (e .e20) (e .e18)
      (.trans (e .e16) (.trans (e .e8) tail))))
    (.precompose preRoute
      (.trans
        (.symm (.reassoc (e .e16) (e .e8) tail))
        (.postcompose
          (.symm (nativeK5NaturalitySquare1LocalSourceSeam t1 t2 t3 t4 t5))
          tail)))

/-- True 13→0 local-to-global square1 target:
the genuine old e9;e7 opposite leg, same F54 prefix and suffix. -/
def nativeK5NaturalitySquare1GlobalTargetSeam :
    NativeF54StructuralSeam p
      (nativeK5TypedGlobalF54Route t1 t2 t3 t4 t5 7)
      (nativeK5WhiskeredFaceTarget t1 t2 t3 t4 t5 .square1) := by
  let e := nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5
  let preRoute := KuuNativeF45Tree.DepthRotationRoute.trans (e .e20) (e .e18)
  let tail := KuuNativeF45Tree.DepthRotationRoute.trans (e .e3) (e .e0)
  change NativeF54StructuralSeam p
    (.trans (e .e20) (.trans (e .e18)
      (.trans (e .e9) (.trans (e .e7) tail))))
    (.trans preRoute
      (.trans (nativeK5AnchoredFace t1 t2 t3 t4 t5 .square1).2.2.1 tail))
  exact .trans
    (.symm (.reassoc (e .e20) (e .e18)
      (.trans (e .e9) (.trans (e .e7) tail))))
    (.precompose preRoute
      (.trans
        (.symm (.reassoc (e .e9) (e .e7) tail))
        (.postcompose
          (.symm (nativeK5NaturalitySquare1LocalTargetSeam t1 t2 t3 t4 t5))
          tail)))

/-- Actual original P92B naturality square1, transported to one
common 13→0 Type-valued pair in the DISTINCT structural extension. -/
def nativeK5NaturalitySquare1ExtendedFace :
    NativeF55StructuralComparison p
      (nativeK5TypedGlobalF54Route t1 t2 t3 t4 t5 8)
      (nativeK5TypedGlobalF54Route t1 t2 t3 t4 t5 7) :=
  nativeK5StructuralGluedFace t1 t2 t3 t4 t5 .square1 _ _
    (nativeK5NaturalitySquare1GlobalSourceSeam t1 t2 t3 t4 t5)
    (nativeK5NaturalitySquare1GlobalTargetSeam t1 t2 t3 t4 t5)

theorem nativeK5NaturalitySquare1ExtendedFace_word :
    (nativeK5NaturalitySquare1ExtendedFace t1 t2 t3 t4 t5).p94cGroupWord =
      (nativeK5AnchoredFace t1 t2 t3 t4 t5 .square1).2.2.2.p94cGroupWord := by
  exact nativeK5StructuralGluedFace_word t1 t2 t3 t4 t5 .square1 _ _ _ _

#print axioms nativeF54StructuralHorizontalRightUnit
#print axioms nativeK5NaturalitySquare1LocalSourceSeam
#print axioms nativeK5NaturalitySquare1LocalTargetSeam
#print axioms nativeK5NaturalitySquare1GlobalSourceSeam
#print axioms nativeK5NaturalitySquare1GlobalTargetSeam
#print axioms nativeK5NaturalitySquare1ExtendedFace_word

end FiveNativeStages
end
end Kuu.F112.Physical
