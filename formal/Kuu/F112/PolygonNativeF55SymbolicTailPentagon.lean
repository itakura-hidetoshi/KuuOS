import Kuu.F112.PolygonNativeF55MixedDepthPentagonTransport

/-!
# F112-E7Q5-F4-F — UNBOUNDED symbolic Nat depths with two zero-depth contexts

F4-D/E proved exact native F54 pentagon functor naturality at genuinely
mixed fixed depths. Fully unrestricted symbolic Nat depths remain an
independent dependent-cast transport problem: Nat.add_assoc generally
does NOT definitionally evaluate when its third argument is a variable.

Here we prove a stronger UNBOUNDED symbolic case: the FIRST TWO
original-shaped proof-bearing F45 stages have arbitrary independent
Nat depths n₁,m₁,n₂,m₂, while the trailing two F45 stages are
zero-depth legitimate original categorical context trees. Each
associator then reindexes using a genuine Nat.add_assoc with the
appropriate zero-depth third argument, so its two dependent casts
reduce without quotienting or inventing a Gray interchange.

The genuine F55 pentagon higher cell is constructed between the
still-distinct raw 3- and 2-rotation routes. No historical KUOS imports.
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

/-- The root associator commutes with both independent functors for
arbitrary two-axis n₁,m₁,n₂,m₂, provided the third genuine stage has
two Nat depths 0; no finite upper bound is imposed on first stages. -/
theorem nativeZeroTailAssoc_mapAxes_naturality
    (F : A ⥤ C) (G : B ⥤ D)
    {p : Polygon} {a b : A} {x y : B}
    {n₁ n₂ m₁ m₂ : Nat}
    {p₀ p₁ p₂ p₃ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ q₃ : KuuNativeBlocks x y}
    (t₁ : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁)
    (t₂ : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂)
    (t₃ : KuuNativeF45Tree p 0 0 p₂ q₂ p₃ q₃) :
    (KuuNativeF45Tree.DepthRotationRoute.assoc t₁ t₂ t₃).mapAxes F G =
      KuuNativeF45Tree.DepthRotationRoute.assoc
        (t₁.mapAxes F G) (t₂.mapAxes F G) (t₃.mapAxes F G) := by
  rfl

variable {p : Polygon} {a b : A} {x y : B}
variable {n₁ n₂ m₁ m₂ : Nat}
variable {p₀ p₁ p₂ p₃ p₄ : KuuNativeBlocks a b}
variable {q₀ q₁ q₂ q₃ q₄ : KuuNativeBlocks x y}
variable
  (t₁ : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁)
  (t₂ : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂)
  (t₃ : KuuNativeF45Tree p 0 0 p₂ q₂ p₃ q₃)
  (t₄ : KuuNativeF45Tree p 0 0 p₃ q₃ p₄ q₄)

/-- The TRUE 3-rotation F54 pentagon long route is strictly natural
for ALL FOUR UNBOUNDED Nat coordinates of its first two stages. -/
theorem nativeSymbolicTailPentagonLong_mapAxes_naturality
    (F : A ⥤ C) (G : B ⥤ D) :
    (KuuNativeF45Tree.DepthRotationRoute.pentagonLong
      t₁ t₂ t₃ t₄).mapAxes F G =
      KuuNativeF45Tree.DepthRotationRoute.pentagonLong
        (t₁.mapAxes F G) (t₂.mapAxes F G)
        (t₃.mapAxes F G) (t₄.mapAxes F G) := by
  rfl

/-- The independently stored short F54 pentagon boundary also
commutes with arbitrary functors without fixing the first depths. -/
theorem nativeSymbolicTailPentagonShort_mapAxes_naturality
    (F : A ⥤ C) (G : B ⥤ D) :
    (KuuNativeF45Tree.DepthRotationRoute.pentagonShort
      t₁ t₂ t₃ t₄).mapAxes F G =
      KuuNativeF45Tree.DepthRotationRoute.pentagonShort
        (t₁.mapAxes F G) (t₂.mapAxes F G)
        (t₃.mapAxes F G) (t₄.mapAxes F G) := by
  rfl

/-- An ACTUAL proof-relevant free F55 pentagon between the
transported raw unequal long and short paths, without any additional
3-cell family assumed from charges or braided Gray principles. -/
def nativeSymbolicTailPentagonCell_mapAxes
    (F : A ⥤ C) (G : B ⥤ D) :
    KuuNativeF45Tree.DepthRotationRoute.PresentedCell p
      ((KuuNativeF45Tree.DepthRotationRoute.pentagonLong
        t₁ t₂ t₃ t₄).mapAxes F G)
      ((KuuNativeF45Tree.DepthRotationRoute.pentagonShort
        t₁ t₂ t₃ t₄).mapAxes F G) := by
  rw [nativeSymbolicTailPentagonLong_mapAxes_naturality t₁ t₂ t₃ t₄ F G,
    nativeSymbolicTailPentagonShort_mapAxes_naturality t₁ t₂ t₃ t₄ F G]
  exact .pentagon (t₁.mapAxes F G) (t₂.mapAxes F G)
    (t₃.mapAxes F G) (t₄.mapAxes F G)

/-- Structural F55 generator tag and its chosen 3-coordinate
interpretation remain exact across unbounded original Nat depths. -/
theorem nativeSymbolicTailPentagonCell_mapAxes_shapeTag
    (F : A ⥤ C) (G : B ⥤ D) :
    (nativeSymbolicTailPentagonCell_mapAxes t₁ t₂ t₃ t₄ F G).shapeTag = 1 := by
  rw [nativeSymbolicTailPentagonCell_mapAxes]
  rfl

theorem nativeSymbolicTailPentagonCell_mapAxes_shadow
    (F : A ⥤ C) (G : B ⥤ D) :
    (nativeSymbolicTailPentagonCell_mapAxes t₁ t₂ t₃ t₄ F G).nativeShadow =
      (((1 : Int), (0 : Int)), (0 : ZMod 2)) :=
  (nativeSymbolicTailPentagonCell_mapAxes t₁ t₂ t₃ t₄ F G).nativeShadow_of_pentagonTag
    (nativeSymbolicTailPentagonCell_mapAxes_shapeTag t₁ t₂ t₃ t₄ F G)

/-- The original three-rotation path is not equal to the
two-rotation path even if its unbounded histories are sent through
nonfaithful ordinary functors. -/
theorem nativeSymbolicTailPentagon_mapAxes_ne
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

#print axioms nativeZeroTailAssoc_mapAxes_naturality
#print axioms nativeSymbolicTailPentagonLong_mapAxes_naturality
#print axioms nativeSymbolicTailPentagonShort_mapAxes_naturality
#print axioms nativeSymbolicTailPentagonCell_mapAxes
#print axioms nativeSymbolicTailPentagonCell_mapAxes_shapeTag
#print axioms nativeSymbolicTailPentagonCell_mapAxes_shadow
#print axioms nativeSymbolicTailPentagon_mapAxes_ne
end
end Kuu.F112.Physical
