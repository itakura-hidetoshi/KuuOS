import Kuu.F112.PolygonNativeF55NorthPentagonTransport

/-!
# F112-E7Q5-F4-D — arbitrary C60 polygon, arbitrary unit-depth native axes

F4-C proved exact raw F54 pentagon boundary naturality for the four
ACTUAL north-C60 sectors with genuine original F41 proof-bearing paths
at source depth (1,1) on each of the four stages, and arbitrary pair
of ordinary functors from the Site incidence category.

The crucial question now is whether C60's particular arrow identities
are required. Here we generalize the original typed FOUR-STAGE
F45/F54 pentagon to arbitrary fully dependent categorical Blocks,
all p : Polygon, arbitrary proof-relevant F45 trees at depth (1,1),
and arbitrary source/target ordinary categories and functors.

The two component path identities are PROVED at raw F54 syntax level;
the constructed F55 pentagon generator remains unquotiented. This
result does NOT claim equality of long and short routes: their raw
rotation counts remain distinct 3 versus 2. The higher F55 cell is
a witness between them, not an identification by shadow grade.

No general arbitrary-Nat-depth pentagon naturality or historical old
Gray/F19/F28 equivalence is asserted.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
noncomputable section

universe uA vA uB vB uC vC uD vD
variable {A : Type uA} [Category.{vA} A]
variable {B : Type uB} [Category.{vB} B]
variable {C : Type uC} [Category.{vC} C]
variable {D : Type uD} [Category.{vD} D]

variable {p : Polygon} {a b : A} {x y : B}
variable {p₀ p₁ p₂ p₃ p₄ : KuuNativeBlocks a b}
variable {q₀ q₁ q₂ q₃ q₄ : KuuNativeBlocks x y}
variable
  (t₁ : KuuNativeF45Tree p 1 1 p₀ q₀ p₁ q₁)
  (t₂ : KuuNativeF45Tree p 1 1 p₁ q₁ p₂ q₂)
  (t₃ : KuuNativeF45Tree p 1 1 p₂ q₂ p₃ q₃)
  (t₄ : KuuNativeF45Tree p 1 1 p₃ q₃ p₄ q₄)

/-- The RAW three-step associativity path of ANY four consecutively
typed depth-(1,1) stages is natural on the nose under any two
ordinary functors on its full source-category axes. -/
theorem nativeUnitDepthPentagonLong_mapAxes_naturality
    (F : A ⥤ C) (G : B ⥤ D) :
    (KuuNativeF45Tree.DepthRotationRoute.pentagonLong
      t₁ t₂ t₃ t₄).mapAxes F G =
    KuuNativeF45Tree.DepthRotationRoute.pentagonLong
      (t₁.mapAxes F G) (t₂.mapAxes F G)
      (t₃.mapAxes F G) (t₄.mapAxes F G) := by
  rfl

/-- The RAW two-step alternative associahedral path preserves its
different actual F54 rotation proof under the same two functors. -/
theorem nativeUnitDepthPentagonShort_mapAxes_naturality
    (F : A ⥤ C) (G : B ⥤ D) :
    (KuuNativeF45Tree.DepthRotationRoute.pentagonShort
      t₁ t₂ t₃ t₄).mapAxes F G =
    KuuNativeF45Tree.DepthRotationRoute.pentagonShort
      (t₁.mapAxes F G) (t₂.mapAxes F G)
      (t₃.mapAxes F G) (t₄.mapAxes F G) := by
  rfl

/-- CONSTRUCT the actual unquotiented F55 pentagon cell between
precisely the mapped raw 3-rotation and 2-rotation boundary
presentations, without additional F55 data or numerical axioms. -/
def nativeUnitDepthPentagonCell_mapAxes
    (F : A ⥤ C) (G : B ⥤ D) :
    KuuNativeF45Tree.DepthRotationRoute.PresentedCell p
      ((KuuNativeF45Tree.DepthRotationRoute.pentagonLong
        t₁ t₂ t₃ t₄).mapAxes F G)
      ((KuuNativeF45Tree.DepthRotationRoute.pentagonShort
        t₁ t₂ t₃ t₄).mapAxes F G) := by
  rw [nativeUnitDepthPentagonLong_mapAxes_naturality t₁ t₂ t₃ t₄ F G,
      nativeUnitDepthPentagonShort_mapAxes_naturality t₁ t₂ t₃ t₄ F G]
  exact .pentagon (t₁.mapAxes F G) (t₂.mapAxes F G)
    (t₃.mapAxes F G) (t₄.mapAxes F G)

/-- Real F55 raw pentagon constructor survives the transport. -/
theorem nativeUnitDepthPentagonCell_mapAxes_shapeTag
    (F : A ⥤ C) (G : B ⥤ D) :
    (nativeUnitDepthPentagonCell_mapAxes t₁ t₂ t₃ t₄ F G).shapeTag = 1 := by
  rw [nativeUnitDepthPentagonCell_mapAxes]
  rfl

/-- The full chosen interpretation then follows from the SOURCE
raw pentagon constructor tag; it is not the reason for existence. -/
theorem nativeUnitDepthPentagonCell_mapAxes_shadow
    (F : A ⥤ C) (G : B ⥤ D) :
    (nativeUnitDepthPentagonCell_mapAxes t₁ t₂ t₃ t₄ F G).nativeShadow =
      (((1 : Int), (0 : Int)), (0 : ZMod 2)) :=
  (nativeUnitDepthPentagonCell_mapAxes t₁ t₂ t₃ t₄ F G).nativeShadow_of_pentagonTag
    (nativeUnitDepthPentagonCell_mapAxes_shapeTag t₁ t₂ t₃ t₄ F G)

/-- The raw F54 pentagon legs retain DIFFERENT rotation counts
even after arbitrary functors of either categorical source axis. -/
theorem nativeUnitDepthPentagon_mapAxes_ne
    (F : A ⥤ C) (G : B ⥤ D) :
    (KuuNativeF45Tree.DepthRotationRoute.pentagonLong
      t₁ t₂ t₃ t₄).mapAxes F G ≠
    (KuuNativeF45Tree.DepthRotationRoute.pentagonShort
      t₁ t₂ t₃ t₄).mapAxes F G := by
  intro h
  have hc := congrArg
    KuuNativeF45Tree.DepthRotationRoute.rotationCount h
  rw [KuuNativeF45Tree.DepthRotationRoute.rotationCount_mapAxes,
      KuuNativeF45Tree.DepthRotationRoute.rotationCount_mapAxes,
      KuuNativeF45Tree.DepthRotationRoute.pentagonLong_count,
      KuuNativeF45Tree.DepthRotationRoute.pentagonShort_count] at hc
  exact (by decide : (3 : Nat) ≠ 2) hc

#print axioms nativeUnitDepthPentagonLong_mapAxes_naturality
#print axioms nativeUnitDepthPentagonShort_mapAxes_naturality
#print axioms nativeUnitDepthPentagonCell_mapAxes
#print axioms nativeUnitDepthPentagonCell_mapAxes_shapeTag
#print axioms nativeUnitDepthPentagonCell_mapAxes_shadow
#print axioms nativeUnitDepthPentagon_mapAxes_ne
end
end Kuu.F112.Physical
