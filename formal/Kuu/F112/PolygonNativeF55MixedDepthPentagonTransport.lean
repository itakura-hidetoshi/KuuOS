import Kuu.F112.PolygonNativeF55UnitDepthPentagonTransport

/-!
# F112-E7Q5-F4-E — arbitrary typed mixed nonunit depths

F4-D established strict F54 functor naturality of the whole original
3-versus-2 pentagon when every F45 stage has Nat depths (1,1).
This theorem probes arbitrary nonunit, nonconstant stage depths,
while retaining the same TRUE original typed F40 categorical Blocks,
F41 axis histories, and actual raw F54 routes. It also includes the
unresolved universal-Nat associativity test in a separate theorem;
neither shadow equality nor new braiding axioms are used.
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

/-- Exact naturality of a single original source F54 associator at
ARBITRARY separately indexed two-axis Nat depths. -/
theorem KuuNativeF45Tree.DepthRotationRoute.mapAxes_assoc_arbitrary
    (F : A ⥤ C) (G : B ⥤ D)
    {p : Polygon} {a b : A} {x y : B}
    {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
    {p₀ p₁ p₂ p₃ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ q₃ : KuuNativeBlocks x y}
    (t₁ : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁)
    (t₂ : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂)
    (t₃ : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃) :
    (KuuNativeF45Tree.DepthRotationRoute.assoc t₁ t₂ t₃).mapAxes F G =
      KuuNativeF45Tree.DepthRotationRoute.assoc
        (t₁.mapAxes F G) (t₂.mapAxes F G) (t₃.mapAxes F G) := by
  rfl

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

#print axioms KuuNativeF45Tree.DepthRotationRoute.mapAxes_assoc_arbitrary
#print axioms nativeMixedDepthPentagonLong_mapAxes_naturality
#print axioms nativeMixedDepthPentagonShort_mapAxes_naturality
#print axioms nativeMixedDepthPentagonCell_mapAxes
#print axioms nativeMixedDepthPentagonCell_mapAxes_shapeTag
end
end Kuu.F112.Physical
