import Kuu.F112.PolygonNativeF54FunctorChains
import Kuu.F112.PolygonNativeF54DepthRoutes

/-!
# F112-E7Q5-E2 — full original-shaped F54 route functor transport

E7Q5-E1 constructed strictly typed transport of true local rotations,
both orientations of primitive rotation edges, and arbitrary finite
rotation chains between source/target F45 proof-bearing trees.

Extend that construction to ALL FIVE genuinely typed independent
F54 DepthRotationRoute constructors:
  chain, castDepths (TWO Nat equality transports), trans,
  leftContext and rightContext.

The comparison is constructor-recursive: it never constructs a
higher 3-cell merely because two shadows or numerical charges agree.
We prove exact rotation count preservation, agreement with indexed
depth casts, exact vertical path composition and contexts, and real
C60 original pentagon long/short preservation and noncollapse even
after arbitrary functors on BOTH categorical axes.

Frozen old F19/F28/legacy F54 and old Gray are read-only comparison
subjects, NOT imported. No historical source equivalence, F55 raw
faithfulness, odd F59 phase or F68/F77 obstruction transfer claimed.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
noncomputable section

universe uA vA uB vB uA₂ vA₂ uB₂ vB₂
variable {A : Type uA} [Category.{vA} A]
variable {B : Type uB} [Category.{vB} B]
variable {A₂ : Type uA₂} [Category.{vA₂} A₂]
variable {B₂ : Type uB₂} [Category.{vB₂} B₂]

/-- A POSITIVE actual source-functor action on ALL five F54 route
constructors with genuine intermediate F45 proof trees and two Nat
index equalities. No source proof is invented from grade equality. -/
def KuuNativeF45Tree.DepthRotationRoute.mapAxes
    (F : A ⥤ A₂) (G : B ⥤ B₂)
    {p : Polygon} {a b : A} {x y : B}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (route : KuuNativeF45Tree.DepthRotationRoute p first last) :
    KuuNativeF45Tree.DepthRotationRoute p
      (first.mapAxes F G) (last.mapAxes F G) := by
  induction route with
  | chain path =>
      exact .chain (path.mapAxes F G)
  | castDepths hn hm tree =>
      rw [KuuNativeF45Tree.mapAxes_castDepths]
      exact .castDepths hn hm (tree.mapAxes F G)
  | trans left right ihLeft ihRight =>
      exact .trans ihLeft ihRight
  | leftContext path later ih =>
      simpa only [KuuNativeF45Tree.mapAxes] using
        (KuuNativeF45Tree.DepthRotationRoute.leftContext
          ih (later.mapAxes F G))
  | rightContext earlier path ih =>
      simpa only [KuuNativeF45Tree.mapAxes] using
        (KuuNativeF45Tree.DepthRotationRoute.rightContext
          (earlier.mapAxes F G) ih)

/-- No functor between the two independent categorical axes can
delete or fabricate an actual F54 rotation edge in this raw syntax:
two Nat casts still contribute exactly zero rotation count. -/
theorem KuuNativeF45Tree.DepthRotationRoute.rotationCount_mapAxes
    (F : A ⥤ A₂) (G : B ⥤ B₂)
    {p : Polygon} {a b : A} {x y : B}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (route : KuuNativeF45Tree.DepthRotationRoute p first last) :
    (route.mapAxes F G).rotationCount = route.rotationCount := by
  induction route with
  | chain path =>
      change (path.mapAxes F G).length = path.length
      exact path.length_mapAxes F G
  | castDepths hn hm tree =>
      rfl
  | trans left right ihLeft ihRight =>
      change (left.mapAxes F G).rotationCount +
        (right.mapAxes F G).rotationCount =
        left.rotationCount + right.rotationCount
      exact congrArg₂ (fun s t : Nat => s + t) ihLeft ihRight
  | leftContext path later ih =>
      exact ih
  | rightContext earlier path ih =>
      exact ih

/-- A genuine DOUBLE Nat-equality route cast is preserved as a
cast constructor, not translated into a fabricated rotation chain. -/
theorem KuuNativeF45Tree.DepthRotationRoute.mapAxes_castDepths
    (F : A ⥤ A₂) (G : B ⥤ B₂)
    {p : Polygon} {a b : A} {x y : B}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (hn : n = n') (hm : m = m')
    (tree : KuuNativeF45Tree p n m ma pa mb pb) :
    (KuuNativeF45Tree.DepthRotationRoute.castDepths hn hm tree).mapAxes F G =
      KuuNativeF45Tree.DepthRotationRoute.castDepths hn hm
        (tree.mapAxes F G) := by
  cases hn
  cases hm
  rfl

/-- The mapped F54 route composition is exactly the composition
of mapped original raw route witnesses, before any quotient. -/
theorem KuuNativeF45Tree.DepthRotationRoute.mapAxes_trans
    (F : A ⥤ A₂) (G : B ⥤ B₂)
    {p : Polygon} {a b : A} {x y : B}
    {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n₁ m₁ ma pa mb pb}
    {middle : KuuNativeF45Tree p n₂ m₂ ma pa mb pb}
    {last : KuuNativeF45Tree p n₃ m₃ ma pa mb pb}
    (r : KuuNativeF45Tree.DepthRotationRoute p first middle)
    (s : KuuNativeF45Tree.DepthRotationRoute p middle last) :
    (KuuNativeF45Tree.DepthRotationRoute.trans r s).mapAxes F G =
      KuuNativeF45Tree.DepthRotationRoute.trans
        (r.mapAxes F G) (s.mapAxes F G) :=
  rfl

/-- The exact original C60 ordered physical polygon-sector list
survives every mapped two-axis route, including both real F54 contexts. -/
theorem KuuNativeF45Tree.DepthRotationRoute.mapAxes_physical_leaves
    (F : A ⥤ A₂) (G : B ⥤ B₂)
    {p : Polygon} {a b : A} {x y : B}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (route : KuuNativeF45Tree.DepthRotationRoute p first last) :
    (first.mapAxes F G).erasePhysical.erase.leaves =
      (last.mapAxes F G).erasePhysical.erase.leaves :=
  (route.mapAxes F G).physical_leaves_eq

/-- For the ACTUAL four-stage north C60 pentagon, long three-rotation
route count stays three under arbitrary pair of source functors. -/
theorem northNativeF45PentagonLong_mapAxes_count
    (F : Site ⥤ A₂) (G : Site ⥤ B₂) :
    (northNativeF45PentagonLong.mapAxes F G).rotationCount = 3 := by
  rw [KuuNativeF45Tree.DepthRotationRoute.rotationCount_mapAxes]
  exact KuuNativeF45Tree.DepthRotationRoute.pentagonLong_count
    northNativeF45FirstStage northNativeF45SecondStage
    northNativeF45ThirdStage northNativeF45FourthStage

/-- The short route remains exactly two original F54 rotation steps. -/
theorem northNativeF45PentagonShort_mapAxes_count
    (F : Site ⥤ A₂) (G : Site ⥤ B₂) :
    (northNativeF45PentagonShort.mapAxes F G).rotationCount = 2 := by
  rw [KuuNativeF45Tree.DepthRotationRoute.rotationCount_mapAxes]
  exact KuuNativeF45Tree.DepthRotationRoute.pentagonShort_count
    northNativeF45FirstStage northNativeF45SecondStage
    northNativeF45ThirdStage northNativeF45FourthStage

/-- The genuine original-shaped C60 F54 pentagon raw paths NEVER
collapse into one raw witness under the constructed map, even if
the two ordinary source functors forget some category Hom data.
This is a proved source obstruction, not a F55/Gray exchange phase. -/
theorem northNativeF45Pentagon_mapAxes_long_ne_short
    (F : Site ⥤ A₂) (G : Site ⥤ B₂) :
    northNativeF45PentagonLong.mapAxes F G ≠
      northNativeF45PentagonShort.mapAxes F G := by
  intro h
  have hc := congrArg
    KuuNativeF45Tree.DepthRotationRoute.rotationCount h
  rw [northNativeF45PentagonLong_mapAxes_count F G,
      northNativeF45PentagonShort_mapAxes_count F G] at hc
  exact (by decide : (3 : Nat) ≠ 2) hc

#print axioms KuuNativeF45Tree.DepthRotationRoute.mapAxes
#print axioms KuuNativeF45Tree.DepthRotationRoute.rotationCount_mapAxes
#print axioms KuuNativeF45Tree.DepthRotationRoute.mapAxes_castDepths
#print axioms KuuNativeF45Tree.DepthRotationRoute.mapAxes_trans
#print axioms KuuNativeF45Tree.DepthRotationRoute.mapAxes_physical_leaves
#print axioms northNativeF45PentagonLong_mapAxes_count
#print axioms northNativeF45PentagonShort_mapAxes_count
#print axioms northNativeF45Pentagon_mapAxes_long_ne_short
end
end Kuu.F112.Physical
