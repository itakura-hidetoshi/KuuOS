import Kuu.F112.PolygonNativeF55FunctorReceivers

/-!
# F112-E7Q5-F3 — faithful functor on the CHOSEN shadow-quotient F55 3-Homs

The E7P4 native third-level category is a SPECIFIC quotient of
actual proof-relevant, typed F55 free raw 3-cells by equality of
their chosen complete shadow ((Int × Int) × ZMod 2).

E7Q5-F1/F2 construct a conditional action of two ordinary category
functors on ALL nine raw constructors, given genuine mapped-pentagon
cell data with raw pentagon shape, and prove exact shadow preservation.

Here the action DESCENDS to the already proved concrete E7P4
3-Hom quotient. The quotient observer commutes with this action,
which implies injectivity on EACH 3-Hom: even a nonfaithful functor
on either of the underlying two ordinary category axes cannot
identify two different chosen SHADOW QUOTIENT arrows. This does
NOT establish raw F55 faithfulness, nor any historical Gray/F55
comparison, nor essential surjectivity or fullness.

The resulting category functor between TWO true typed F54 route
categories is faithful for the same reason. The conditional
pentagon lift is an explicit parameter, not a fabricated axiom.
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

/-- Genuine well-defined descent from the independently constructed
F55 raw-source functor to the E7P4 chosen complete-shadow quotient.
The proof checks arbitrary representatives and uses ONLY actual
source-recursive shadow preservation, never equality of routes. -/
def NativeF55ThreeHom.mapAxesGivenPentagon
    (F : A ⥤ A₂) (G : B ⥤ B₂)
    (data : KuuNativeF55MappedPentagonData F G)
    {p : Polygon} {a b : A} {x y : B}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55ThreeHom u v) :
    NativeF55ThreeHom (u.mapAxes F G) (v.mapAxes F G) :=
  Quot.liftOn f
    (fun raw => nativeF55ThreeOf
      (raw.mapAxesGivenPentagon F G data))
    (by
      intro left right h
      apply Quot.sound
      change
        (left.mapAxesGivenPentagon F G data).nativeShadow =
        (right.mapAxesGivenPentagon F G data).nativeShadow
      rw [left.nativeShadow_mapAxesGivenPentagon F G data,
        right.nativeShadow_mapAxesGivenPentagon F G data]
      exact h)

/-- The original faithful chosen shadow observer computes exactly
the same FULL three coordinates after the transported quotient arrow. -/
theorem NativeF55ThreeHom.mapAxesGivenPentagon_eval
    (F : A ⥤ A₂) (G : B ⥤ B₂)
    (data : KuuNativeF55MappedPentagonData F G)
    {p : Polygon} {a b : A} {x y : B}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55ThreeHom u v) :
    nativeF55ThreeEval (f.mapAxesGivenPentagon F G data) =
      nativeF55ThreeEval f := by
  refine Quot.inductionOn f (fun raw => ?_)
  exact raw.nativeShadow_mapAxesGivenPentagon F G data

/-- The F55 source functor is FAITHFUL on each actual chosen quotient
3-Hom fiber: same transported quotient arrow implies same original
quotient arrow, since both are determined by complete shadow. -/
theorem NativeF55ThreeHom.mapAxesGivenPentagon_injective
    (F : A ⥤ A₂) (G : B ⥤ B₂)
    (data : KuuNativeF55MappedPentagonData F G)
    {p : Polygon} {a b : A} {x y : B}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55ThreeHom u v}
    (h : f.mapAxesGivenPentagon F G data =
      g.mapAxesGivenPentagon F G data) :
    f = g := by
  apply nativeF55ThreeEval_injective
  have heq := congrArg nativeF55ThreeEval h
  rw [f.mapAxesGivenPentagon_eval F G data,
      g.mapAxesGivenPentagon_eval F G data] at heq
  exact heq

/-- Identities in the SOURCE third-level quotient stay actual
identities under the independent higher-source functor action. -/
theorem NativeF55ThreeHom.mapAxesGivenPentagon_id
    (F : A ⥤ A₂) (G : B ⥤ B₂)
    (data : KuuNativeF55MappedPentagonData F G)
    {p : Polygon} {a b : A} {x y : B}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (u : KuuNativeF45Tree.DepthRotationRoute p first last) :
    (nativeF55ThreeOf
      (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident u) :
      NativeF55ThreeHom u u).mapAxesGivenPentagon F G data =
    nativeF55ThreeOf
      (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident
        (u.mapAxes F G)) := by
  rfl

/-- Actual vertical pasting of two E7P4 higher arrows commutes with
the constructed higher-source comparison BEFORE any claim of
unconditional original tricategorical interchange. -/
theorem NativeF55ThreeHom.mapAxesGivenPentagon_comp
    (F : A ⥤ A₂) (G : B ⥤ B₂)
    (data : KuuNativeF55MappedPentagonData F G)
    {p : Polygon} {a b : A} {x y : B}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {u v w : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55ThreeHom u v) (g : NativeF55ThreeHom v w) :
    (nativeF55ThreeComp f g).mapAxesGivenPentagon F G data =
      nativeF55ThreeComp (f.mapAxesGivenPentagon F G data)
        (g.mapAxesGivenPentagon F G data) := by
  refine Quot.inductionOn f (fun rawf => ?_)
  refine Quot.inductionOn g (fun rawg => ?_)
  rfl

/-- A TRUE Mathlib category functor on actual independently typed
F54 raw depth-route objects and chosen E7P4 quotient 3-Homs.
Object map: fully typed F54 functor action; arrow map: quotient of
ALL NINE raw 3-cell constructors. Both functor laws are PROVED. -/
def nativeF55ThreeFunctorGivenPentagon
    (F : A ⥤ A₂) (G : B ⥤ B₂)
    (data : KuuNativeF55MappedPentagonData F G)
    {p : Polygon} {a b : A} {x y : B}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :
    (KuuNativeF45Tree.DepthRotationRoute p first last) ⥤
      (KuuNativeF45Tree.DepthRotationRoute p
        (first.mapAxes F G) (last.mapAxes F G)) where
  obj := fun u => u.mapAxes F G
  map := fun {u v} f => f.mapAxesGivenPentagon F G data
  map_id := by
    intro u
    rfl
  map_comp := by
    intro u v w f g
    exact NativeF55ThreeHom.mapAxesGivenPentagon_comp F G data f g

/-- Explicit local faithfulness of the mathematically constructed
third-level functor, not of old Gray nor the raw proof presentation.
No assumption that F or G is faithful is needed. -/
theorem nativeF55ThreeFunctorGivenPentagon_map_injective
    (F : A ⥤ A₂) (G : B ⥤ B₂)
    (data : KuuNativeF55MappedPentagonData F G)
    {p : Polygon} {a b : A} {x y : B}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : u ⟶ v}
    (h :
      (nativeF55ThreeFunctorGivenPentagon F G data first last).map f =
      (nativeF55ThreeFunctorGivenPentagon F G data first last).map g) :
    f = g :=
  NativeF55ThreeHom.mapAxesGivenPentagon_injective F G data h

#print axioms NativeF55ThreeHom.mapAxesGivenPentagon
#print axioms NativeF55ThreeHom.mapAxesGivenPentagon_eval
#print axioms NativeF55ThreeHom.mapAxesGivenPentagon_injective
#print axioms NativeF55ThreeHom.mapAxesGivenPentagon_id
#print axioms NativeF55ThreeHom.mapAxesGivenPentagon_comp
#print axioms nativeF55ThreeFunctorGivenPentagon
#print axioms nativeF55ThreeFunctorGivenPentagon_map_injective
end
end Kuu.F112.Physical
