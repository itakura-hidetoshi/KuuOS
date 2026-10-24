import Kuu.F112.PolygonNativeF55P94DK5ContextTypedPentagonSeams
import Mathlib.Tactic

/-!
# F112-P94D3O — actual square0 F54 contextual-unit normalization

We keep the original P92B associator-naturality square (#0) as an
actual Type-valued source face. The separately presented F54
structural seams are extended with genuine zero-rotation context-unit
certificates and proof-relevant context congruence.

The original source- and target-F54 faces are normalized from
the genuine P90 horizontal-route expressions to the two actual
tagged 6-to-0 paths. Whiskering transports these to the genuine
13-to-0 global F54 paths (#3 and #2). The constructed extended
Type-valued face carries the *same ordered noncommutative word*
as the existing original P92B naturality square.

The structural generators remain a DISTINCT presentation; they
are not retroactive P92B witnesses or global 4D coherence.
Preserve N-count obstruction +1 and all original K5/C60 geometry.
No Gray, new axioms, sorry/admit or graph equality used for descent.
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

/-- Actual context-unit normalization on the original P90 horizontal
F54 route: no Type-level equality of route syntax is assumed. -/
def nativeF54StructuralHorizontalLeftUnit
    {p : Polygon} {a b : D} {x y : E}
    {n m k k' l l' : Nat}
    {p₀ p₁ p₂ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ : KuuNativeBlocks x y}
    (earlier : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁)
    {before : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂}
    {after : KuuNativeF45Tree p k' l' p₁ q₁ p₂ q₂}
    (r : KuuNativeF45Tree.DepthRotationRoute p before after) :
    NativeF54StructuralSeam p
      (nativeF54P90HorizontalRoute (.chain (.refl earlier)) r)
      (.rightContext earlier r) :=
  .trans
    (.postcompose (.leftContextUnit earlier before) (.rightContext earlier r))
    (.leftUnit (.rightContext earlier r))

/-- A pair of truly typed original F54 identity routes normalizes
to the identity of their original F45 composite. -/
def nativeF54StructuralHorizontalTwoUnits
    {p : Polygon} {a b : D} {x y : E}
    {n m k l : Nat}
    {p₀ p₁ p₂ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ : KuuNativeBlocks x y}
    (earlier : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁)
    (later : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂) :
    NativeF54StructuralSeam p
      (nativeF54P90HorizontalRoute
        (nativeK5RouteUnit earlier) (nativeK5RouteUnit later))
      (nativeK5RouteUnit (.node earlier later)) :=
  .trans
    (nativeF54StructuralHorizontalLeftUnit earlier (nativeK5RouteUnit later))
    (.rightContextUnit earlier later)

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

/-- First actual F54 naturality square source, not a graph path:
the P90 horizontal transport of (unit,unit,assoc) followed by its
original target associator, normalized to the original e10;e2 F54. -/
def nativeK5NaturalitySquare0LocalSourceSeam :
    NativeF54StructuralSeam p
      (nativeK5AnchoredFace t1 t2 t3 t4 t5 .square0).2.1
      (.trans (nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5 .e10)
        (nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5 .e2)) := by
  let e := nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5
  let w := KuuNativeF45Tree.DepthRotationRoute.assoc t3 t4 t5
  let hpair := nativeF54P90HorizontalRoute
    (nativeK5RouteUnit t1) (nativeK5RouteUnit t2)
  let h := nativeF54P90HorizontalRoute hpair w
  have hpairUnit : NativeF54StructuralSeam p hpair
      (nativeK5RouteUnit (.node t1 t2)) :=
    nativeF54StructuralHorizontalTwoUnits t1 t2
  have hh : NativeF54StructuralSeam p h (e .e10) := by
    change NativeF54StructuralSeam p
      (.trans (.leftContext hpair (.node (.node t3 t4) t5))
        (.rightContext (.node t1 t2) w))
      (.rightContext (.node t1 t2) w)
    exact .trans
      (.postcompose
        (.leftContextCongruence hpairUnit (.node (.node t3 t4) t5))
        (e .e10))
      (.trans
        (.postcompose
          (.leftContextUnit (.node t1 t2) (.node (.node t3 t4) t5))
          (e .e10))
        (.leftUnit (e .e10)))
  change NativeF54StructuralSeam p (.trans h (e .e2))
    (.trans (e .e10) (e .e2))
  exact .postcompose hh (e .e2)

/-- The other original Type-valued N0 source (original second
associator route), normalized to the two existing genuine e4;e0
primitive F54 rotations. -/
def nativeK5NaturalitySquare0LocalTargetSeam :
    NativeF54StructuralSeam p
      (nativeK5AnchoredFace t1 t2 t3 t4 t5 .square0).2.2.1
      (.trans (nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5 .e4)
        (nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5 .e0)) := by
  let e := nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5
  let w := KuuNativeF45Tree.DepthRotationRoute.assoc t3 t4 t5
  let hw2 := nativeF54P90HorizontalRoute (nativeK5RouteUnit t2) w
  let h := nativeF54P90HorizontalRoute (nativeK5RouteUnit t1) hw2
  have hh : NativeF54StructuralSeam p h (e .e0) :=
    .trans
      (nativeF54StructuralHorizontalLeftUnit t1 hw2)
      (.rightContextCongruence t1
        (nativeF54StructuralHorizontalLeftUnit t2 w))
  change NativeF54StructuralSeam p
    (.trans (e .e4) h) (.trans (e .e4) (e .e0))
  exact .precompose (e .e4) hh

/-- The genuine global 13→0 source of the outward square0 (k=1)
normalizes by source Type-valued F54 reassociation/units, not by
an equality of 14-vertex graph paths. -/
def nativeK5NaturalitySquare0GlobalSourceSeam :
    NativeF54StructuralSeam p
      (nativeK5TypedGlobalF54Route t1 t2 t3 t4 t5 3)
      (nativeK5WhiskeredFaceSource t1 t2 t3 t4 t5 .square0) := by
  let e := nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5
  let preRoute := KuuNativeF45Tree.DepthRotationRoute.trans (e .e19) (e .e12)
  let localLong := KuuNativeF45Tree.DepthRotationRoute.trans (e .e10) (e .e2)
  let unit0 := nativeK5RouteUnit
    (nativeK5TypedVertex t1 t2 t3 t4 t5 (0 : Fin 14)).2.2
  change NativeF54StructuralSeam p
    (.trans (e .e19) (.trans (e .e12) localLong))
    (.trans preRoute
      (.trans (nativeK5AnchoredFace t1 t2 t3 t4 t5 .square0).2.1 unit0))
  exact .trans
    (.symm (.reassoc (e .e19) (e .e12) localLong))
    (.precompose preRoute
      (.trans
        (.symm (.rightUnit localLong))
        (.postcompose
          (.symm (nativeK5NaturalitySquare0LocalSourceSeam t1 t2 t3 t4 t5))
          unit0)))

/-- True global target seam from canonical route2 to the original
whiskered P92B square0 source. -/
def nativeK5NaturalitySquare0GlobalTargetSeam :
    NativeF54StructuralSeam p
      (nativeK5TypedGlobalF54Route t1 t2 t3 t4 t5 2)
      (nativeK5WhiskeredFaceTarget t1 t2 t3 t4 t5 .square0) := by
  let e := nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5
  let preRoute := KuuNativeF45Tree.DepthRotationRoute.trans (e .e19) (e .e12)
  let localShort := KuuNativeF45Tree.DepthRotationRoute.trans (e .e4) (e .e0)
  let unit0 := nativeK5RouteUnit
    (nativeK5TypedVertex t1 t2 t3 t4 t5 (0 : Fin 14)).2.2
  change NativeF54StructuralSeam p
    (.trans (e .e19) (.trans (e .e12) localShort))
    (.trans preRoute
      (.trans (nativeK5AnchoredFace t1 t2 t3 t4 t5 .square0).2.2.1 unit0))
  exact .trans
    (.symm (.reassoc (e .e19) (e .e12) localShort))
    (.precompose preRoute
      (.trans
        (.symm (.rightUnit localShort))
        (.postcompose
          (.symm (nativeK5NaturalitySquare0LocalTargetSeam t1 t2 t3 t4 t5))
          unit0)))

/-- An UNCONDITIONAL Type-valued K5 outward naturality square in
the distinct F54-structural extension, using the genuine old P92B
3-cell instead of a numerical shadow or a graph equality. -/
def nativeK5NaturalitySquare0ExtendedFace :
    NativeF55StructuralComparison p
      (nativeK5TypedGlobalF54Route t1 t2 t3 t4 t5 3)
      (nativeK5TypedGlobalF54Route t1 t2 t3 t4 t5 2) :=
  nativeK5StructuralGluedFace t1 t2 t3 t4 t5 .square0 _ _
    (nativeK5NaturalitySquare0GlobalSourceSeam t1 t2 t3 t4 t5)
    (nativeK5NaturalitySquare0GlobalTargetSeam t1 t2 t3 t4 t5)

theorem nativeK5NaturalitySquare0ExtendedFace_word :
    (nativeK5NaturalitySquare0ExtendedFace t1 t2 t3 t4 t5).p94cGroupWord =
      (nativeK5AnchoredFace t1 t2 t3 t4 t5 .square0).2.2.2.p94cGroupWord := by
  exact nativeK5StructuralGluedFace_word t1 t2 t3 t4 t5 .square0 _ _ _ _

#print axioms NativeF54StructuralSeam.rotationCount_sound
#print axioms nativeF54StructuralHorizontalLeftUnit
#print axioms nativeF54StructuralHorizontalTwoUnits
#print axioms nativeK5NaturalitySquare0LocalSourceSeam
#print axioms nativeK5NaturalitySquare0LocalTargetSeam
#print axioms nativeK5NaturalitySquare0GlobalSourceSeam
#print axioms nativeK5NaturalitySquare0GlobalTargetSeam
#print axioms nativeK5NaturalitySquare0ExtendedFace_word

end FiveNativeStages
end
end Kuu.F112.Physical
