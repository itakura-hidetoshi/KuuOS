import Kuu.F112.PolygonNativeF55PentagonBoundaryDescent

/-!
# F112-E7Q5-F4-C — concrete C60 north-pentagon mapped F54 raw endpoints

F4-B isolates two exact raw-route pentagon boundary equations as
sufficient for constructing a genuine, proof-relevant F55 higher
generator. General F54 naturality across an arbitrary pair of Nat
casts has not been proved.

Here we specialize to the FOUR ACTUAL consecutively typed original
C60 north-pentagon F45 stages; every leaf has exact axis depth 1,1
and genuine F41 original-shaped native Blocks histories. First try
constructor-level naturality on those *concrete* paths, for arbitrary
independent ordinary functors out of the Site incidence category.

No equality of charges or full-shadow quotient is substituted for
a raw typed route equation. No historical KUOS/Gray/F51/F77 imports.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
noncomputable section

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

/-- The ACTUAL C60 north-pentagon long three-rotation F54 route
commutes with transporting both original fully typed categorical
axes of all four concrete C60 physical sector stages. -/
theorem northNativeF45PentagonLong_mapAxes_naturality
    (F : Site ⥤ D) (G : Site ⥤ E) :
    northNativeF45PentagonLong.mapAxes F G =
      KuuNativeF45Tree.DepthRotationRoute.pentagonLong
        (northNativeF45FirstStage.mapAxes F G)
        (northNativeF45SecondStage.mapAxes F G)
        (northNativeF45ThirdStage.mapAxes F G)
        (northNativeF45FourthStage.mapAxes F G) := by
  rfl

/-- The equally genuine, but distinct, two-rotation C60 F54 route
commutes with both independent source-functor transport operations. -/
theorem northNativeF45PentagonShort_mapAxes_naturality
    (F : Site ⥤ D) (G : Site ⥤ E) :
    northNativeF45PentagonShort.mapAxes F G =
      KuuNativeF45Tree.DepthRotationRoute.pentagonShort
        (northNativeF45FirstStage.mapAxes F G)
        (northNativeF45SecondStage.mapAxes F G)
        (northNativeF45ThirdStage.mapAxes F G)
        (northNativeF45FourthStage.mapAxes F G) := by
  rfl

/-- With the two ACTUAL source identities proven, the new F55 free
pentagon constructor furnishes an actual witness on the precise
transported three-versus-two original C60 F54 routes. This is not
obtained from an equality of signed charges or a Gray law. -/
def northNativeF55PentagonCell_mapAxes
    (F : Site ⥤ D) (G : Site ⥤ E) :
    KuuNativeF45Tree.DepthRotationRoute.PresentedCell (.pentagon .north)
      (northNativeF45PentagonLong.mapAxes F G)
      (northNativeF45PentagonShort.mapAxes F G) := by
  rw [northNativeF45PentagonLong_mapAxes_naturality F G,
    northNativeF45PentagonShort_mapAxes_naturality F G]
  exact .pentagon
    (northNativeF45FirstStage.mapAxes F G)
    (northNativeF45SecondStage.mapAxes F G)
    (northNativeF45ThirdStage.mapAxes F G)
    (northNativeF45FourthStage.mapAxes F G)

/-- Source constructor tag, not just numerical grade, witnesses
the transported F55 pentagon is a GENUINE pentagon generator. -/
theorem northNativeF55PentagonCell_mapAxes_shapeTag
    (F : Site ⥤ D) (G : Site ⥤ E) :
    (northNativeF55PentagonCell_mapAxes F G).shapeTag = 1 := by
  rw [northNativeF55PentagonCell_mapAxes]
  rfl

/-- Its complete chosen pentagon calibration is derived from the
raw free F55 constructor shape, not supplied as a third axiom. -/
theorem northNativeF55PentagonCell_mapAxes_shadow
    (F : Site ⥤ D) (G : Site ⥤ E) :
    (northNativeF55PentagonCell_mapAxes F G).nativeShadow =
      (((1 : Int), (0 : Int)), (0 : ZMod 2)) :=
  (northNativeF55PentagonCell_mapAxes F G).nativeShadow_of_pentagonTag
    (northNativeF55PentagonCell_mapAxes_shapeTag F G)

#print axioms northNativeF45PentagonLong_mapAxes_naturality
#print axioms northNativeF45PentagonShort_mapAxes_naturality
#print axioms northNativeF55PentagonCell_mapAxes
#print axioms northNativeF55PentagonCell_mapAxes_shapeTag
#print axioms northNativeF55PentagonCell_mapAxes_shadow
end
end Kuu.F112.Physical
