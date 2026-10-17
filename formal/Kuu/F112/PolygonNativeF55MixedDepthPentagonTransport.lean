import Kuu.F112.PolygonNativeF55UnitDepthPentagonTransport

/-!
# F112-E7Q5-F4-E — arbitrary typed mixed nonunit depths

F4-D established strict F54 functor naturality of the whole original
3-versus-2 pentagon when every F45 stage has Nat depths (1,1).
This theorem probes arbitrary nonunit, nonconstant stage depths,
while retaining the same TRUE original typed F40 categorical Blocks,
F41 axis histories, and actual raw F54 routes. Unlike the still-unproved universal-Nat associator equality,
closed mixed-depth arithmetic normalizes the explicit Nat.add_assoc
casts. No shadow equality or new braiding axioms are used.
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
  (t₁ : KuuNativeF45Tree p 2 2 p₀ q₀ p₁ q₁)
  (t₂ : KuuNativeF45Tree p 1 1 p₁ q₁ p₂ q₂)
  (t₃ : KuuNativeF45Tree p 3 1 p₂ q₂ p₃ q₃)
  (t₄ : KuuNativeF45Tree p 1 2 p₃ q₃ p₄ q₄)

/-- Arbitrary categories/paths, with four genuinely mixed depth
profiles (2,2), (1,1), (3,1), (1,2), retain the 3-step pentagon
raw boundary exactly under arbitrary two-axis functors. -/
theorem nativeMixedDepthPentagonLong_mapAxes_naturality
    (F : A ⥤ C) (G : B ⥤ D) :
    (KuuNativeF45Tree.DepthRotationRoute.pentagonLong
      t₁ t₂ t₃ t₄).mapAxes F G =
    KuuNativeF45Tree.DepthRotationRoute.pentagonLong
      (t₁.mapAxes F G) (t₂.mapAxes F G)
      (t₃.mapAxes F G) (t₄.mapAxes F G) := by
  rfl

/-- The raw two-step pentagon path has the same strict functor
naturality for these independently mixed nonunit Nat profiles. -/
theorem nativeMixedDepthPentagonShort_mapAxes_naturality
    (F : A ⥤ C) (G : B ⥤ D) :
    (KuuNativeF45Tree.DepthRotationRoute.pentagonShort
      t₁ t₂ t₃ t₄).mapAxes F G =
    KuuNativeF45Tree.DepthRotationRoute.pentagonShort
      (t₁.mapAxes F G) (t₂.mapAxes F G)
      (t₃.mapAxes F G) (t₄.mapAxes F G) := by
  rfl

/-- A genuine FREE source F55 higher pentagon cell between the
two still distinct raw 3-vs-2 paths at mixed two-axis depths, not a
quotient or derived equality of their underlying F54 routes. -/
def nativeMixedDepthPentagonCell_mapAxes
    (F : A ⥤ C) (G : B ⥤ D) :
    KuuNativeF45Tree.DepthRotationRoute.PresentedCell p
      ((KuuNativeF45Tree.DepthRotationRoute.pentagonLong
        t₁ t₂ t₃ t₄).mapAxes F G)
      ((KuuNativeF45Tree.DepthRotationRoute.pentagonShort
        t₁ t₂ t₃ t₄).mapAxes F G) := by
  rw [nativeMixedDepthPentagonLong_mapAxes_naturality t₁ t₂ t₃ t₄ F G,
      nativeMixedDepthPentagonShort_mapAxes_naturality t₁ t₂ t₃ t₄ F G]
  exact .pentagon (t₁.mapAxes F G) (t₂.mapAxes F G)
    (t₃.mapAxes F G) (t₄.mapAxes F G)

/-- Its pentagon generator is genuinely raw, with chosen phase
calibration subsequently forced by constructor-shape rigidity. -/
theorem nativeMixedDepthPentagonCell_mapAxes_shapeTag
    (F : A ⥤ C) (G : B ⥤ D) :
    (nativeMixedDepthPentagonCell_mapAxes t₁ t₂ t₃ t₄ F G).shapeTag = 1 := by
  rw [nativeMixedDepthPentagonCell_mapAxes]
  rfl

/-- Concrete mixed-depth free pentagon shadow is forced by the
already verified source-level pentagon tag, not by existence of an
unproved old F55 braided interpretation. -/
theorem nativeMixedDepthPentagonCell_mapAxes_shadow
    (F : A ⥤ C) (G : B ⥤ D) :
    (nativeMixedDepthPentagonCell_mapAxes t₁ t₂ t₃ t₄ F G).nativeShadow =
      (((1 : Int), (0 : Int)), (0 : ZMod 2)) :=
  (nativeMixedDepthPentagonCell_mapAxes t₁ t₂ t₃ t₄ F G).nativeShadow_of_pentagonTag
    (nativeMixedDepthPentagonCell_mapAxes_shapeTag t₁ t₂ t₃ t₄ F G)

/-- The transported mixed-depth three-rotation and two-rotation
F54 paths remain RAW DISTINCT under any two ordinary functors. -/
theorem nativeMixedDepthPentagon_mapAxes_ne
    (F : A ⥤ C) (G : B ⥤ D) :
    (KuuNativeF45Tree.DepthRotationRoute.pentagonLong
      t₁ t₂ t₃ t₄).mapAxes F G ≠
    (KuuNativeF45Tree.DepthRotationRoute.pentagonShort
      t₁ t₂ t₃ t₄).mapAxes F G := by
  intro h
  have hc := congrArg KuuNativeF45Tree.DepthRotationRoute.rotationCount h
  rw [KuuNativeF45Tree.DepthRotationRoute.rotationCount_mapAxes,
    KuuNativeF45Tree.DepthRotationRoute.rotationCount_mapAxes,
    KuuNativeF45Tree.DepthRotationRoute.pentagonLong_count,
    KuuNativeF45Tree.DepthRotationRoute.pentagonShort_count] at hc
  exact (by decide : (3 : Nat) ≠ 2) hc

#print axioms nativeMixedDepthPentagonLong_mapAxes_naturality
#print axioms nativeMixedDepthPentagonShort_mapAxes_naturality
#print axioms nativeMixedDepthPentagonCell_mapAxes
#print axioms nativeMixedDepthPentagonCell_mapAxes_shapeTag
#print axioms nativeMixedDepthPentagonCell_mapAxes_shadow
#print axioms nativeMixedDepthPentagon_mapAxes_ne
end
end Kuu.F112.Physical
