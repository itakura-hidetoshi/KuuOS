import Kuu.F112.PolygonNativeF55SymbolicTailPentagon

/-!
# F112-E7Q5-F4-G — UNBOUNDED symbolic Nat depths, genuine NONZERO tail

F4-F proved exact original-shaped 3-vs-2 F54 pentagon functor
naturality with unrestricted symbolic Nat depths on the first two
stages and two trailing zero-depth contexts.

A stronger genuine four-stage result retains arbitrary (unbounded)
source depths n₁,m₁,n₂,m₂ on the first two proof-bearing stages AND
uses nonzero (1,1) original native F41 histories on the final two.
Nat.add_assoc with a closed third argument 1 (or its finite sum)
computes definitionally in the pinned Lean kernel, so the actual
doubly indexed casted F54 rotation witnesses are preserved STRICTLY.

A separate initial experiment tried to apply Eq.casesOn to the
complex mapped-cast tree at fully symbolic third depths. The kernel
correctly refused dependent elimination: the Eq.rec transport is
NOT definitionally identical to the target raw tree. We make NO
unproved claim of general arbitrary third/fourth Nat naturality,
and DO NOT add a Gray source axiom or shadow-based cell existence.
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

/-- Real one-step F54 associator naturality at UNBOUNDED independent
first two depths, and a nontrivial third native stage of depth (1,1). -/
theorem nativeNonzeroTailAssoc_mapAxes_naturality
    (F : A ⥤ C) (G : B ⥤ D)
    {p : Polygon} {a b : A} {x y : B}
    {n₁ n₂ m₁ m₂ : Nat}
    {p₀ p₁ p₂ p₃ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ q₃ : KuuNativeBlocks x y}
    (t₁ : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁)
    (t₂ : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂)
    (t₃ : KuuNativeF45Tree p 1 1 p₂ q₂ p₃ q₃) :
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
  (t₃ : KuuNativeF45Tree p 1 1 p₂ q₂ p₃ q₃)
  (t₄ : KuuNativeF45Tree p 1 1 p₃ q₃ p₄ q₄)

/-- All four original proof-bearing F45 stages may be genuinely
nontrivial; the first two axes have NO upper Nat-depth bound. -/
theorem nativeNonzeroTailPentagonLong_mapAxes_naturality
    (F : A ⥤ C) (G : B ⥤ D) :
    (KuuNativeF45Tree.DepthRotationRoute.pentagonLong
      t₁ t₂ t₃ t₄).mapAxes F G =
      KuuNativeF45Tree.DepthRotationRoute.pentagonLong
        (t₁.mapAxes F G) (t₂.mapAxes F G)
        (t₃.mapAxes F G) (t₄.mapAxes F G) := by
  rfl

/-- Exact raw short path source naturality, again preserving
both proof-relevant source Nat casts and unquotiented F54 routes. -/
theorem nativeNonzeroTailPentagonShort_mapAxes_naturality
    (F : A ⥤ C) (G : B ⥤ D) :
    (KuuNativeF45Tree.DepthRotationRoute.pentagonShort
      t₁ t₂ t₃ t₄).mapAxes F G =
      KuuNativeF45Tree.DepthRotationRoute.pentagonShort
        (t₁.mapAxes F G) (t₂.mapAxes F G)
        (t₃.mapAxes F G) (t₄.mapAxes F G) := by
  rfl

/-- CONSTRUCT the FREE pentagon F55 3-cell between the genuinely
distinct raw 3-rotation and 2-rotation boundaries, without a
separately supplied mapped-cell hypothesis. -/
def nativeNonzeroTailPentagonCell_mapAxes
    (F : A ⥤ C) (G : B ⥤ D) :
    KuuNativeF45Tree.DepthRotationRoute.PresentedCell p
      ((KuuNativeF45Tree.DepthRotationRoute.pentagonLong
        t₁ t₂ t₃ t₄).mapAxes F G)
      ((KuuNativeF45Tree.DepthRotationRoute.pentagonShort
        t₁ t₂ t₃ t₄).mapAxes F G) := by
  rw [nativeNonzeroTailPentagonLong_mapAxes_naturality t₁ t₂ t₃ t₄ F G,
    nativeNonzeroTailPentagonShort_mapAxes_naturality t₁ t₂ t₃ t₄ F G]
  exact .pentagon (t₁.mapAxes F G) (t₂.mapAxes F G)
    (t₃.mapAxes F G) (t₄.mapAxes F G)

/-- Original F55 proof shape, not grade agreement, proves generator
identity; the chosen native phase is subsequently forced. -/
theorem nativeNonzeroTailPentagonCell_mapAxes_shapeTag
    (F : A ⥤ C) (G : B ⥤ D) :
    (nativeNonzeroTailPentagonCell_mapAxes t₁ t₂ t₃ t₄ F G).shapeTag = 1 := by
  rw [nativeNonzeroTailPentagonCell_mapAxes]
  rfl

theorem nativeNonzeroTailPentagonCell_mapAxes_shadow
    (F : A ⥤ C) (G : B ⥤ D) :
    (nativeNonzeroTailPentagonCell_mapAxes t₁ t₂ t₃ t₄ F G).nativeShadow =
      (((1 : Int), (0 : Int)), (0 : ZMod 2)) :=
  (nativeNonzeroTailPentagonCell_mapAxes t₁ t₂ t₃ t₄ F G).nativeShadow_of_pentagonTag
    (nativeNonzeroTailPentagonCell_mapAxes_shapeTag t₁ t₂ t₃ t₄ F G)

/-- Strictly distinct unquotiented F54 paths, even after applying
two possibly nonfaithful original-category functors. -/
theorem nativeNonzeroTailPentagon_mapAxes_ne
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

#print axioms nativeNonzeroTailAssoc_mapAxes_naturality
#print axioms nativeNonzeroTailPentagonLong_mapAxes_naturality
#print axioms nativeNonzeroTailPentagonShort_mapAxes_naturality
#print axioms nativeNonzeroTailPentagonCell_mapAxes
#print axioms nativeNonzeroTailPentagonCell_mapAxes_shapeTag
#print axioms nativeNonzeroTailPentagonCell_mapAxes_shadow
#print axioms nativeNonzeroTailPentagon_mapAxes_ne
end
end Kuu.F112.Physical
