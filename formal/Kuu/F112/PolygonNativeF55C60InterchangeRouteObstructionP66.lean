import Kuu.F112.PolygonNativeF55ContextUnitDescentP65

/-!
# F112-P66 — genuine F54 interchange-route obstruction after P65

P65 descends both original proof-relevant F55 context functors to the
minimal P64 category. This does not make distinct SOURCE F54 rotation
orders equal. The actual C60 six-sector disjoint square in P55 supplies
two different Type-valued F54 routes with the same F45 endpoints.

This file proves that P64's strictly VERTICAL structural-unit quotient
preserves the actual original F54 ROUTE OBJECTS injectively. Therefore
the left-first and right-first pasting orders of any two truly disjoint
original local rotations remain different objects in P64's quotient.

At the same time, the genuine physical square remains a typed HIGHER
MORPHISM between those distinct route objects, and its selected phase
remains odd. There is no claim that the higher morphism makes the
two route objects literally equal, nor that a selected phase is a
universal, canonical presentation of emptiness.

The necessary next problem is an honestly typed 2-route comparison or
compatible extra congruence, whose effect on genuine proof history
and C60 odd square evidence must be analyzed before global strict
interchange is asserted. This is an obstruction to deriving strict
interchange solely from P62-P65, NOT a no-go for every strict 3-category.

No Gray, old KUOS dependency, new axioms, sorry or admit.
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

/-- P64's quotient is an arrow congruence: it cannot silently
identify two different original proof-relevant F54 route OBJECTS.
The object map of the actual Mathlib quotient is injective. -/
theorem nativeF55StructuralUnitQuotient_obj_injective
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :
    Function.Injective
      (nativeF55StructuralUnitQuotientFunctor first last).obj := by
  intro u v h
  exact congrArg
    (fun z : NativeF55StructuralUnitCategory first last => z.as) h

/-- BOTH original context orders are still different objects in
the minimal structural-unit category. This is uniform over every
genuinely typed F54 local rotation and both Nat-depth axes; it
follows from physical source constructor tags, not numeric shadow. -/
theorem nativeF55StructuralUnitQuotient_square_objects_distinct
    {p : Polygon} {a b : D} {x y : E}
    {n m k l : Nat}
    {p₀ p₁ p₂ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ : KuuNativeBlocks x y}
    {leftBefore leftAfter : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
    {rightBefore rightAfter : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂}
    (left : KuuNativeF45Tree.LocalRotation p leftBefore leftAfter)
    (right : KuuNativeF45Tree.LocalRotation p rightBefore rightAfter) :
    (nativeF55StructuralUnitQuotientFunctor
      (KuuNativeF45Tree.node leftBefore rightBefore)
      (KuuNativeF45Tree.node leftAfter rightAfter)).obj
      (⟨KuuNativeF45Tree.DepthRotationRoute.squareLeftFirst left right⟩ :
        NativeF55RawRouteVertex
          (KuuNativeF45Tree.node leftBefore rightBefore)
          (KuuNativeF45Tree.node leftAfter rightAfter)) ≠
    (nativeF55StructuralUnitQuotientFunctor
      (KuuNativeF45Tree.node leftBefore rightBefore)
      (KuuNativeF45Tree.node leftAfter rightAfter)).obj
      (⟨KuuNativeF45Tree.DepthRotationRoute.squareRightFirst left right⟩ :
        NativeF55RawRouteVertex
          (KuuNativeF45Tree.node leftBefore rightBefore)
          (KuuNativeF45Tree.node leftAfter rightAfter)) := by
  intro h
  have hRoutes :=
    (nativeF55StructuralUnitQuotient_obj_injective
      (KuuNativeF45Tree.node leftBefore rightBefore)
      (KuuNativeF45Tree.node leftAfter rightAfter)) h
  exact (KuuNativeF45Tree.DepthRotationRoute.squareLeft_ne_right left right)
    (congrArg NativeF55RawRouteVertex.route hRoutes)

/-- The genuine F55 raw DISJOINT SQUARE does not disappear: it is an
actual morphism from the left-first F54 route to the right-first F54
route, even after imposing the minimal P62 identity-only relation. -/
def nativeF55StructuralUnitSquareCell
    {p : Polygon} {a b : D} {x y : E}
    {n m k l : Nat}
    {p₀ p₁ p₂ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ : KuuNativeBlocks x y}
    {leftBefore leftAfter : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
    {rightBefore rightAfter : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂}
    (left : KuuNativeF45Tree.LocalRotation p leftBefore leftAfter)
    (right : KuuNativeF45Tree.LocalRotation p rightBefore rightAfter) :
    (nativeF55StructuralUnitQuotientFunctor
      (KuuNativeF45Tree.node leftBefore rightBefore)
      (KuuNativeF45Tree.node leftAfter rightAfter)).obj
      (⟨KuuNativeF45Tree.DepthRotationRoute.squareLeftFirst left right⟩ :
        NativeF55RawRouteVertex
          (KuuNativeF45Tree.node leftBefore rightBefore)
          (KuuNativeF45Tree.node leftAfter rightAfter))
      ⟶
    (nativeF55StructuralUnitQuotientFunctor
      (KuuNativeF45Tree.node leftBefore rightBefore)
      (KuuNativeF45Tree.node leftAfter rightAfter)).obj
      (⟨KuuNativeF45Tree.DepthRotationRoute.squareRightFirst left right⟩ :
        NativeF55RawRouteVertex
          (KuuNativeF45Tree.node leftBefore rightBefore)
          (KuuNativeF45Tree.node leftAfter rightAfter)) :=
  (nativeF55StructuralUnitQuotientFunctor
    (KuuNativeF45Tree.node leftBefore rightBefore)
    (KuuNativeF45Tree.node leftAfter rightAfter)).map
    ((KuuNativeF45Tree.DepthRotationRoute.PresentedCell.disjointSquare
      left right).toNativeRawEdge.toPath)

/-- Even after the P62/P64 typed structural-unit quotient, the
genuine physical square retains its exact chosen (0,1;odd) shadow.
This is a PRESERVATION theorem, not a defining equality of histories. -/
theorem nativeF55StructuralUnitSquareCell_shadow
    {p : Polygon} {a b : D} {x y : E}
    {n m k l : Nat}
    {p₀ p₁ p₂ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ : KuuNativeBlocks x y}
    {leftBefore leftAfter : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
    {rightBefore rightAfter : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂}
    (left : KuuNativeF45Tree.LocalRotation p leftBefore leftAfter)
    (right : KuuNativeF45Tree.LocalRotation p rightBefore rightAfter) :
    nativeF55ThreeEval
      ((nativeF55StructuralUnitToShadow
        (KuuNativeF45Tree.node leftBefore rightBefore)
        (KuuNativeF45Tree.node leftAfter rightAfter)).map
        (nativeF55StructuralUnitSquareCell left right)) =
      (((0 : Int), (1 : Int)), (1 : ZMod 2)) := by
  simpa only [nativeF55StructuralUnitSquareCell,
    KuuNativeF45Tree.DepthRotationRoute.PresentedCell.nativeShadow] using
    (nativeF55StructuralUnit_preserves_raw_shadow
      (KuuNativeF45Tree.node leftBefore rightBefore)
      (KuuNativeF45Tree.node leftAfter rightAfter)
      (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.disjointSquare
        left right))

/-- Its odd phase remains nonzero after the minimal identity quotient;
strict interchange cannot be inferred merely from erasing unit loops. -/
theorem nativeF55StructuralUnitSquareCell_phase_nonzero
    {p : Polygon} {a b : D} {x y : E}
    {n m k l : Nat}
    {p₀ p₁ p₂ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ : KuuNativeBlocks x y}
    {leftBefore leftAfter : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
    {rightBefore rightAfter : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂}
    (left : KuuNativeF45Tree.LocalRotation p leftBefore leftAfter)
    (right : KuuNativeF45Tree.LocalRotation p rightBefore rightAfter) :
    (nativeF55ThreeEval
      ((nativeF55StructuralUnitToShadow
        (KuuNativeF45Tree.node leftBefore rightBefore)
        (KuuNativeF45Tree.node leftAfter rightAfter)).map
        (nativeF55StructuralUnitSquareCell left right))).2 ≠
      (0 : ZMod 2) := by
  rw [nativeF55StructuralUnitSquareCell_shadow]
  decide

/-- On the ACTUAL original six-sector north C60 hexagon, the
two disjoint rotation orders remain distinct quotient route objects. -/
theorem northHexagonNativeSquare_unitQuotient_objects_distinct :
    (nativeF55StructuralUnitQuotientFunctor _ _).obj
      (⟨northHexagonNativeSquareLeft⟩ : NativeF55RawRouteVertex _ _) ≠
    (nativeF55StructuralUnitQuotientFunctor _ _).obj
      (⟨northHexagonNativeSquareRight⟩ : NativeF55RawRouteVertex _ _) := by
  exact nativeF55StructuralUnitQuotient_square_objects_distinct
    northHexagonNativeLeftRotation northHexagonNativeRightRotation

/-- The actual north C60 physical square also retains its odd
chosen observer coordinate after the minimal structural quotient. -/
theorem northHexagonNativeSquare_unitQuotient_phase_nonzero :
    (nativeF55ThreeEval
      ((nativeF55StructuralUnitToShadow _ _).map
        (nativeF55StructuralUnitSquareCell
          northHexagonNativeLeftRotation
          northHexagonNativeRightRotation))).2 ≠ (0 : ZMod 2) := by
  exact nativeF55StructuralUnitSquareCell_phase_nonzero
    northHexagonNativeLeftRotation northHexagonNativeRightRotation

#print axioms nativeF55StructuralUnitQuotient_obj_injective
#print axioms nativeF55StructuralUnitQuotient_square_objects_distinct
#print axioms nativeF55StructuralUnitSquareCell
#print axioms nativeF55StructuralUnitSquareCell_shadow
#print axioms nativeF55StructuralUnitSquareCell_phase_nonzero
#print axioms northHexagonNativeSquare_unitQuotient_objects_distinct
#print axioms northHexagonNativeSquare_unitQuotient_phase_nonzero

end
end Kuu.F112.Physical
