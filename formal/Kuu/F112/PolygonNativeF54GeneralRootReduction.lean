import Kuu.F112.PolygonNativeF55PentagonBoundaryDescent
import Kuu.F112.PolygonNativeF54GeneralCastCoherence

/-!
# F112-E7Q5-F4-H — unrestricted-Nat raw F54 pentagon reduction to ONE root law

F4-C through F4-G prove genuine full F55 pentagon cells on successively
larger concrete and unbounded symbolic Nat-depth families. At fully
general Nat depths, the original casted F54 associator's functor image
contains a dependent Eq.rec, and direct conversion to the rebuilt
associator cannot be justified merely by equality of route counts or
shadow grades.

First prove general two-category F54 raw contextuality, and all-Nat
rotation-count and inequivalence invariants. Next make the ONE
missing original root associator naturality law explicit as a
proposition-valued mathematical input, NOT an axiom, and derive the
TWO global long/short pentagon raw equations from it. When supplied,
these actual boundary equalities construct genuine F55 free cells and
a faithful chosen quotient third-level functor through F4-B.

The root law is not claimed proved. The local and global typing is
preserved with all actual original-shaped F40 Blocks and F41 histories.
No old KUOS, Gray, F51 or F77 code is imported.
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

/-- Functor action respects the EXACT free F54 left context under
arbitrary dependent depths, not only an erased C60 boundary. -/
theorem KuuNativeF45Tree.DepthRotationRoute.mapAxes_leftContext
    (F : A ⥤ C) (G : B ⥤ D)
    {p : Polygon} {a b : A} {x y : B}
    {n n' m m' k l : Nat}
    {ma mb mc : KuuNativeBlocks a b}
    {pa pb pc : KuuNativeBlocks x y}
    {before : KuuNativeF45Tree p n m ma pa mb pb}
    {after : KuuNativeF45Tree p n' m' ma pa mb pb}
    (path : KuuNativeF45Tree.DepthRotationRoute p before after)
    (later : KuuNativeF45Tree p k l mb pb mc pc) :
    (KuuNativeF45Tree.DepthRotationRoute.leftContext path later).mapAxes F G =
      KuuNativeF45Tree.DepthRotationRoute.leftContext
        (path.mapAxes F G) (later.mapAxes F G) := by
  rfl

/-- Independent right-context functor naturality on the actual
Type-valued full F54 route grammar, with four separate Nat depths. -/
theorem KuuNativeF45Tree.DepthRotationRoute.mapAxes_rightContext
    (F : A ⥤ C) (G : B ⥤ D)
    {p : Polygon} {a b : A} {x y : B}
    {k l n n' m m' : Nat}
    {ma mb mc : KuuNativeBlocks a b}
    {pa pb pc : KuuNativeBlocks x y}
    (earlier : KuuNativeF45Tree p k l ma pa mb pb)
    {before : KuuNativeF45Tree p n m mb pb mc pc}
    {after : KuuNativeF45Tree p n' m' mb pb mc pc}
    (path : KuuNativeF45Tree.DepthRotationRoute p before after) :
    (KuuNativeF45Tree.DepthRotationRoute.rightContext earlier path).mapAxes F G =
      KuuNativeF45Tree.DepthRotationRoute.rightContext
        (earlier.mapAxes F G) (path.mapAxes F G) := by
  rfl

/-- The three-vs-two original-shaped raw F54 pentagon has EXACT
rotation count 3/2 for ANY FOUR independently Nat-indexed F45
stages, after both arbitrary ordinary category functors. -/
theorem nativeAnyDepthPentagon_mapAxes_counts
    (F : A ⥤ C) (G : B ⥤ D)
    {p : Polygon} {a b : A} {x y : B}
    {n₁ n₂ n₃ n₄ m₁ m₂ m₃ m₄ : Nat}
    {p₀ p₁ p₂ p₃ p₄ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ q₃ q₄ : KuuNativeBlocks x y}
    (t₁ : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁)
    (t₂ : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂)
    (t₃ : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃)
    (t₄ : KuuNativeF45Tree p n₄ m₄ p₃ q₃ p₄ q₄) :
    ((KuuNativeF45Tree.DepthRotationRoute.pentagonLong
      t₁ t₂ t₃ t₄).mapAxes F G).rotationCount = 3 ∧
    ((KuuNativeF45Tree.DepthRotationRoute.pentagonShort
      t₁ t₂ t₃ t₄).mapAxes F G).rotationCount = 2 := by
  constructor
  · rw [KuuNativeF45Tree.DepthRotationRoute.rotationCount_mapAxes]
    exact KuuNativeF45Tree.DepthRotationRoute.pentagonLong_count t₁ t₂ t₃ t₄
  · rw [KuuNativeF45Tree.DepthRotationRoute.rotationCount_mapAxes]
    exact KuuNativeF45Tree.DepthRotationRoute.pentagonShort_count t₁ t₂ t₃ t₄

/-- UNIVERSAL genuine raw long/short inequivalence, independent of
any proof of full Nat-cast strict functoriality: transport cannot
collapse three actual rotation witnesses into two. -/
theorem nativeAnyDepthPentagon_mapAxes_ne
    (F : A ⥤ C) (G : B ⥤ D)
    {p : Polygon} {a b : A} {x y : B}
    {n₁ n₂ n₃ n₄ m₁ m₂ m₃ m₄ : Nat}
    {p₀ p₁ p₂ p₃ p₄ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ q₃ q₄ : KuuNativeBlocks x y}
    (t₁ : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁)
    (t₂ : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂)
    (t₃ : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃)
    (t₄ : KuuNativeF45Tree p n₄ m₄ p₃ q₃ p₄ q₄) :
    (KuuNativeF45Tree.DepthRotationRoute.pentagonLong t₁ t₂ t₃ t₄).mapAxes F G ≠
      (KuuNativeF45Tree.DepthRotationRoute.pentagonShort t₁ t₂ t₃ t₄).mapAxes F G := by
  intro h
  have hc := congrArg KuuNativeF45Tree.DepthRotationRoute.rotationCount h
  obtain ⟨hl, hs⟩ := nativeAnyDepthPentagon_mapAxes_counts F G t₁ t₂ t₃ t₄
  rw [hl, hs] at hc
  exact (by decide : (3 : Nat) ≠ 2) hc

/-- The ONE remaining independent raw F54 root associator
naturality obligation at arbitrary (n₁,n₂,n₃,m₁,m₂,m₃).
This is supplied as PROOF DATA rather than postulated as a Lean
axiom. Existence for arbitrary functors is NOT assumed. -/
structure KuuNativeF54RootAssocComparison
    (F : A ⥤ C) (G : B ⥤ D) where
  root :
    ∀ (p : Polygon) {a b : A} {x y : B}
      {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
      {p₀ p₁ p₂ p₃ : KuuNativeBlocks a b}
      {q₀ q₁ q₂ q₃ : KuuNativeBlocks x y}
      (t₁ : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁)
      (t₂ : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂)
      (t₃ : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃),
      (KuuNativeF45Tree.DepthRotationRoute.assoc t₁ t₂ t₃).mapAxes F G =
        KuuNativeF45Tree.DepthRotationRoute.assoc
          (t₁.mapAxes F G) (t₂.mapAxes F G) (t₃.mapAxes F G)

/-- A root law, IF established, implies all four-stage pentagon long
path equations by actual F54 transitivity and contextuality. -/
theorem KuuNativeF54RootAssocComparison.long
    (F : A ⥤ C) (G : B ⥤ D)
    (h : KuuNativeF54RootAssocComparison F G)
    (p : Polygon) {a b : A} {x y : B}
    {n₁ n₂ n₃ n₄ m₁ m₂ m₃ m₄ : Nat}
    {p₀ p₁ p₂ p₃ p₄ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ q₃ q₄ : KuuNativeBlocks x y}
    (t₁ : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁)
    (t₂ : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂)
    (t₃ : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃)
    (t₄ : KuuNativeF45Tree p n₄ m₄ p₃ q₃ p₄ q₄) :
    (KuuNativeF45Tree.DepthRotationRoute.pentagonLong t₁ t₂ t₃ t₄).mapAxes F G =
      KuuNativeF45Tree.DepthRotationRoute.pentagonLong
        (t₁.mapAxes F G) (t₂.mapAxes F G)
        (t₃.mapAxes F G) (t₄.mapAxes F G) := by
  simp only [KuuNativeF45Tree.DepthRotationRoute.pentagonLong,
    KuuNativeF45Tree.DepthRotationRoute.mapAxes_trans,
    KuuNativeF45Tree.DepthRotationRoute.mapAxes_leftContext,
    KuuNativeF45Tree.DepthRotationRoute.mapAxes_rightContext,
    KuuNativeF45Tree.mapAxes,
    h.root]

/-- Root naturality similarly implies the independently proof-bearing
TWO-rotation pentagon short route naturality with correct four
categorical block endpoints and both original Nat cast witnesses. -/
theorem KuuNativeF54RootAssocComparison.short
    (F : A ⥤ C) (G : B ⥤ D)
    (h : KuuNativeF54RootAssocComparison F G)
    (p : Polygon) {a b : A} {x y : B}
    {n₁ n₂ n₃ n₄ m₁ m₂ m₃ m₄ : Nat}
    {p₀ p₁ p₂ p₃ p₄ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ q₃ q₄ : KuuNativeBlocks x y}
    (t₁ : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁)
    (t₂ : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂)
    (t₃ : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃)
    (t₄ : KuuNativeF45Tree p n₄ m₄ p₃ q₃ p₄ q₄) :
    (KuuNativeF45Tree.DepthRotationRoute.pentagonShort t₁ t₂ t₃ t₄).mapAxes F G =
      KuuNativeF45Tree.DepthRotationRoute.pentagonShort
        (t₁.mapAxes F G) (t₂.mapAxes F G)
        (t₃.mapAxes F G) (t₄.mapAxes F G) := by
  simp only [KuuNativeF45Tree.DepthRotationRoute.pentagonShort,
    KuuNativeF45Tree.DepthRotationRoute.mapAxes_trans,
    KuuNativeF45Tree.mapAxes,
    h.root]

/-- REDUCE the F4-B TWO-axiom-shaped mathematical input to ONE
primitive raw root coherence theorem, without fabricating a new
3-cell from equality of charge or Gray exchange. -/
def KuuNativeF54RootAssocComparison.toBoundary
    (F : A ⥤ C) (G : B ⥤ D)
    (h : KuuNativeF54RootAssocComparison F G) :
    KuuNativeF55PentagonBoundaryComparison F G where
  long := fun p {_a _b} {_x _y}
    {_n₁ _n₂ _n₃ _n₄ _m₁ _m₂ _m₃ _m₄}
    {_p₀ _p₁ _p₂ _p₃ _p₄} {_q₀ _q₁ _q₂ _q₃ _q₄}
    t₁ t₂ t₃ t₄ => h.long F G p t₁ t₂ t₃ t₄
  short := fun p {_a _b} {_x _y}
    {_n₁ _n₂ _n₃ _n₄ _m₁ _m₂ _m₃ _m₄}
    {_p₀ _p₁ _p₂ _p₃ _p₄} {_q₀ _q₁ _q₂ _q₃ _q₄}
    t₁ t₂ t₃ t₄ => h.short F G p t₁ t₂ t₃ t₄

/-- An actual third-level chosen full-shadow-quotient functor then
follows from the ONE root-law proof using previous verified F4-B,
not from an asserted higher Gray or historical F55 coherence axiom. -/
def nativeF55ThreeFunctorOfRootAssoc
    (F : A ⥤ C) (G : B ⥤ D)
    (h : KuuNativeF54RootAssocComparison F G)
    {p : Polygon} {a b : A} {x y : B}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :
    (KuuNativeF45Tree.DepthRotationRoute p first last) ⥤
      (KuuNativeF45Tree.DepthRotationRoute p
        (first.mapAxes F G) (last.mapAxes F G)) :=
  nativeF55ThreeFunctorOfBoundary F G (h.toBoundary F G) first last

#print axioms KuuNativeF45Tree.DepthRotationRoute.mapAxes_leftContext
#print axioms KuuNativeF45Tree.DepthRotationRoute.mapAxes_rightContext
#print axioms nativeAnyDepthPentagon_mapAxes_counts
#print axioms nativeAnyDepthPentagon_mapAxes_ne
#print axioms KuuNativeF54RootAssocComparison
#print axioms KuuNativeF54RootAssocComparison.long
#print axioms KuuNativeF54RootAssocComparison.short
#print axioms KuuNativeF54RootAssocComparison.toBoundary
#print axioms nativeF55ThreeFunctorOfRootAssoc
end
end Kuu.F112.Physical
