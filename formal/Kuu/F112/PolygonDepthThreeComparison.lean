import Kuu.F112.PolygonDepthRoutes

/-!
# F112-E7C / depth-preserving source-to-3-Hom comparison

E7B reconstructs independently double-Nat-indexed F54-shaped routes
over actual C60 polygon sectors and proves a typed erasure into E6A
physical bracket routes, preserving their elementary rotation count.

This file derives the source depth obstruction: every original
dependent rotation route preserves BOTH Nat totals independently,
so the two different depth weights on the same north physical sector
are NOT joined by an invented route.

For any fixed genuinely typed pair of depth trees, the existing
E6B/E6C nine-constructor raw F55-like 3-cells and exact native-shadow
3-Hom category can be pulled back along the E7B erasure map.
We prove a real Mathlib category on typed depth routes and its
comparison functor into the already established E6 source category.
On EACH 3-Hom the map is identity on the exact E6 kernel quotient,
hence injective, and the full (Int × Int) × ZMod2 obstruction survives.

This is a precise *pullback source comparison*, NOT equivalence with
historical F19/F28 Blocks, original F54/F55 typed witnesses or F47
Beck-Chevalley. The depth indices are not forgotten at the objects.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
noncomputable section

/-- Even under arbitrary nested physical contextual rotations and
two-axis equality transports, BOTH total depth indices are separately
invariant. In particular, a raw route cannot invent a depth-change. -/
theorem PolygonDepthRoute.indices_eq {p : Polygon}
    {n m n' m' : Nat}
    {a : PolygonDepthTree p n m}
    {b : PolygonDepthTree p n' m'}
    (r : PolygonDepthRoute p a b) :
    n = n' ∧ m = m' := by
  induction r with
  | ident a =>
      exact ⟨rfl, rfl⟩
  | assoc a b c =>
      exact ⟨rfl, rfl⟩
  | castDepths hn hm a =>
      exact ⟨hn, hm⟩
  | trans f g ihf ihg =>
      exact ⟨ihf.1.trans ihg.1, ihf.2.trans ihg.2⟩
  | leftContext f c ih =>
      cases ih.1
      cases ih.2
      exact ⟨rfl, rfl⟩
  | rightContext a f ih =>
      cases ih.1
      cases ih.2
      exact ⟨rfl, rfl⟩

/-- Distinct original physical sectors are not fabricated to witness
an impossible axis exchange: the SAME genuine north sector with
weights (1,0) and (0,1) admits NO typed E7B rotation route. -/
theorem northDepthAxes_no_route :
    ¬ Nonempty (PolygonDepthRoute (.pentagon .north)
      northDepthFirst northDepthSecond) := by
  rintro ⟨r⟩
  exact (by decide : (1 : Nat) ≠ 0) r.indices_eq.1

/-- A genuinely dependent 3-Hom between separately typed E7B routes.
Its 3-arrow data are precisely the already proved E6C complete-shadow
quotient on their correctly typed erasures, not a new free generator. -/
abbrev PolygonDepthThreeHom {p : Polygon}
    {n m n' m' : Nat}
    {a : PolygonDepthTree p n m}
    {b : PolygonDepthTree p n' m'}
    (f g : PolygonDepthRoute p a b) : Type :=
  PolygonBracketThreeHom f.toBracketRoute g.toBracketRoute

/-- Fully defined third-dimensional vertical composition on the
typed double-depth source, with no guessed exchange or 3-cell axiom. -/
def polygonDepthThreeComp {p : Polygon}
    {n m n' m' : Nat}
    {a : PolygonDepthTree p n m}
    {b : PolygonDepthTree p n' m'}
    {f g h : PolygonDepthRoute p a b}
    (x : PolygonDepthThreeHom f g)
    (y : PolygonDepthThreeHom g h) :
    PolygonDepthThreeHom f h :=
  polygonBracketThreeComp x y

/-- The actual double-depth F54-shaped paths form a 3-Hom category
using only the previously verified exact E6C native-shadow kernel.
Categorical identity/associativity are proved by quotient induction. -/
instance polygonDepthThreeCategory {p : Polygon}
    {n m n' m' : Nat}
    (a : PolygonDepthTree p n m)
    (b : PolygonDepthTree p n' m') :
    Category (PolygonDepthRoute p a b) where
  Hom := PolygonDepthThreeHom
  id f := polygonBracketThreeOf
    (PolygonBracketCell.ident f.toBracketRoute)
  comp x y := polygonDepthThreeComp x y
  id_comp := by
    intro X Y f
    refine Quot.inductionOn f (fun raw => ?_)
    apply Quot.sound
    change (0 : PolygonBracketNativeShadow) + raw.nativeShadow =
      raw.nativeShadow
    exact zero_add _
  comp_id := by
    intro X Y f
    refine Quot.inductionOn f (fun raw => ?_)
    apply Quot.sound
    change raw.nativeShadow + (0 : PolygonBracketNativeShadow) =
      raw.nativeShadow
    exact add_zero _
  assoc := by
    intro W X Y Z f g h
    refine Quot.inductionOn f (fun first => ?_)
    refine Quot.inductionOn g (fun second => ?_)
    refine Quot.inductionOn h (fun third => ?_)
    apply Quot.sound
    change (first.nativeShadow + second.nativeShadow) +
      third.nativeShadow =
      first.nativeShadow + (second.nativeShadow + third.nativeShadow)
    exact add_assoc _ _ _

/-- Each typed E7B path maps to the exact E6A physical bracket
source; each typed quotient 3-cell maps unchanged to the E6C arrow.
This does not identify the two different Nat source depth indices. -/
def polygonDepthToBracketFunctor {p : Polygon}
    {n m n' m' : Nat}
    (a : PolygonDepthTree p n m)
    (b : PolygonDepthTree p n' m') :
    (PolygonDepthRoute p a b) ⥤
      (PolygonBracketRoute p a.erase b.erase) where
  obj r := r.toBracketRoute
  map := fun {_ _} x => x
  map_id := by
    intro r
    rfl
  map_comp := by
    intro r s t x y
    rfl

/-- Faithfulness holds at the actual 3-Hom kernel-quotient level
by a pointwise identity map; it says NOTHING about injectivity on
the *raw* depth-route objects or the historical old-F54 source. -/
theorem polygonDepthToBracketFunctor_map_injective {p : Polygon}
    {n m n' m' : Nat}
    (a : PolygonDepthTree p n m)
    (b : PolygonDepthTree p n' m')
    {f g : PolygonDepthRoute p a b}
    {x y : PolygonDepthThreeHom f g}
    (h : (polygonDepthToBracketFunctor a b).map x =
      (polygonDepthToBracketFunctor a b).map y) :
    x = y := by
  exact h

/-- A concrete source-side 3-morphism exists only when an ACTUAL
proof-relevant nine-constructor E6B raw 3-cell is provided on the
precisely erased boundaries, not from numeric grade coincidence. -/
def polygonDepthThreeOf {p : Polygon}
    {n m n' m' : Nat}
    {a : PolygonDepthTree p n m}
    {b : PolygonDepthTree p n' m'}
    {f g : PolygonDepthRoute p a b}
    (cell : PolygonBracketCell p
      f.toBracketRoute g.toBracketRoute) :
    PolygonDepthThreeHom f g :=
  polygonBracketThreeOf cell

/-- Full independent native-charge and ZMod2 phase evaluation of
one correctly typed double-depth 3-arrow. No E4 localization claim. -/
def polygonDepthThreeEval {p : Polygon}
    {n m n' m' : Nat}
    {a : PolygonDepthTree p n m}
    {b : PolygonDepthTree p n' m'}
    {f g : PolygonDepthRoute p a b}
    (cell : PolygonDepthThreeHom f g) :
    PolygonBracketNativeShadow :=
  polygonBracketThreeEval cell

/-- Genuine 3-arrow vertical pasting preserves BOTH charges and the
separately observable exchange phase in the independent receiver. -/
theorem polygonDepthThreeEval_comp {p : Polygon}
    {n m n' m' : Nat}
    {a : PolygonDepthTree p n m}
    {b : PolygonDepthTree p n' m'}
    {f g h : PolygonDepthRoute p a b}
    (x : PolygonDepthThreeHom f g)
    (y : PolygonDepthThreeHom g h) :
    polygonDepthThreeEval (polygonDepthThreeComp x y) =
      polygonDepthThreeEval x + polygonDepthThreeEval y :=
  polygonBracketThreeEval_comp x y

/-- The already PROVED E6C native shadow obstruction survives
along every precisely typed E7B route pair. This is NOT yet the
historical F55 Delta non-lift. -/
theorem PolygonDepthThreeHom.no_shadow_delta {p : Polygon}
    {n m n' m' : Nat}
    {a : PolygonDepthTree p n m}
    {b : PolygonDepthTree p n' m'}
    {f g : PolygonDepthRoute p a b}
    (x : PolygonDepthThreeHom f g) :
    polygonDepthThreeEval x ≠
      (((0 : Int), (1 : Int)), (0 : ZMod 2)) :=
  PolygonBracketThreeHom.no_shadow_delta x

/-- A concrete 3-identity at a real north pentagon, respecting
both original Nat depth axes through the witnessed E7B associator. -/
def northThreeSectorDepthThreeIdentity :
    PolygonDepthThreeHom
      northThreeSectorDepthRotation northThreeSectorDepthRotation :=
  polygonDepthThreeOf
    (.ident northThreeSectorDepthRotation.toBracketRoute)

theorem northThreeSectorDepthThreeIdentity_shadow_zero :
    polygonDepthThreeEval northThreeSectorDepthThreeIdentity =
      (0 : PolygonBracketNativeShadow) := rfl

#print axioms PolygonDepthRoute.indices_eq
#print axioms northDepthAxes_no_route
#print axioms polygonDepthThreeComp
#print axioms polygonDepthThreeCategory
#print axioms polygonDepthToBracketFunctor
#print axioms polygonDepthToBracketFunctor_map_injective
#print axioms polygonDepthThreeOf
#print axioms polygonDepthThreeEval_comp
#print axioms PolygonDepthThreeHom.no_shadow_delta
#print axioms northThreeSectorDepthThreeIdentity_shadow_zero
end
end Kuu.F112.Physical
