import Kuu.F112.PolygonNativeF54RootTransportCancellation
import Kuu.F112.PolygonNativeF55FunctorReceivers

/-!
# F112-P57 — independent higher-source horizontal naturality

All theorems in this file live ENTIRELY in the independent
`Kuu.F112.Physical` presentation and its mathlib categories.
No historical category, legacy proof tree, or imported external
braiding is used as a logical or definitional foundation.

The original-shaped F54 source has proof-relevant, independently
typed paths on BOTH categorical axes. F4-K already proves that
two-axis functors carry every full nine-constructor F55 raw
three-cell without assuming a missing pentagon filler.

Now prove what is needed to compose such interpreted higher
cells across actual source contexts:
  - all-nine raw source action is unconditional at any Nat depth;
  - it preserves the complete constructor shape and chosen observer;
  - true contextual left/right horizontal three-cell pasting
    commutes with both independent source-category functors;
  - the exact chosen-quotient functor remains faithful and
    preserves the receiver's explicit no-lift obstruction;
  - on the actual six-sector C60 hexagon, odd/even phase choices
    remain different after arbitrary category functors.

The raw Type-valued source is never replaced by its quotient.
The chosen shadow is explicitly ONE possible presentation,
not the uniquely dictated higher geometry.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uA vA uB vB uC vC uD vD
variable {A : Type uA} [Category.{vA} A]
variable {B : Type uB} [Category.{vB} B]
variable {C : Type uC} [Category.{vC} C]
variable {D : Type uD} [Category.{vD} D]

/-- The genuine dependent-Nat F54 root cancellation provides the
missing mapped pentagon filler ONCE AND FOR ALL. No hypotheses or
new axioms: the result is actual constructed Type-valued data. -/
def nativeF55MappedDataFromRootCancellation
    (F : A ⥤ C) (G : B ⥤ D) :
    KuuNativeF55MappedPentagonData F G :=
  (nativeF55BoundaryComparisonOfCancellation F G).toMappedData F G

/-- An unconditional two-category action on EACH of the nine
independent raw F55 three-cell constructors, with actual typed
F54 rotation paths at both source and target. -/
def KuuNativeF45Tree.DepthRotationRoute.PresentedCell.mapAxesNative
    (F : A ⥤ C) (G : B ⥤ D)
    {p : Polygon} {a b : A} {x y : B}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (cell : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    KuuNativeF45Tree.DepthRotationRoute.PresentedCell p
      (r.mapAxes F G) (s.mapAxes F G) :=
  cell.mapAxesGivenPentagon F G
    (nativeF55MappedDataFromRootCancellation F G)

/-- The map is on proof-relevant SOURCE witnesses: each of the
nine constructors keeps its own tag, even before quotienting. -/
theorem KuuNativeF45Tree.DepthRotationRoute.PresentedCell.mapAxesNative_shape
    (F : A ⥤ C) (G : B ⥤ D)
    {p : Polygon} {a b : A} {x y : B}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (cell : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    (cell.mapAxesNative F G).shapeTag = cell.shapeTag :=
  cell.shapeTag_mapAxesGivenPentagon F G
    (nativeF55MappedDataFromRootCancellation F G)

/-- Signed pentagon charge, signed square charge, and the chosen
ZMod 2 phase are conserved. This alone does NOT assert raw
source equality or a unique phase interpretation. -/
theorem KuuNativeF45Tree.DepthRotationRoute.PresentedCell.mapAxesNative_shadow
    (F : A ⥤ C) (G : B ⥤ D)
    {p : Polygon} {a b : A} {x y : B}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (cell : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    (cell.mapAxesNative F G).nativeShadow = cell.nativeShadow :=
  cell.nativeShadow_mapAxesGivenPentagon F G
    (nativeF55MappedDataFromRootCancellation F G)

/-- Actual F54 left/right WHISKERING followed by source-ordered
horizontal pasting commutes strictly with arbitrary independent
axis functors at all Nat depths; no equality of raw distinct
horizontal orders is added. -/
theorem nativeF55HorizontalRoute_mapAxes
    (F : A ⥤ C) (G : B ⥤ D)
    {p : Polygon} {a b : A} {x y : B}
    {n n' m m' k k' l l' : Nat}
    {p₀ p₁ p₂ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ : KuuNativeBlocks x y}
    {leftBefore : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
    {leftAfter : KuuNativeF45Tree p n' m' p₀ q₀ p₁ q₁}
    {rightBefore : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂}
    {rightAfter : KuuNativeF45Tree p k' l' p₁ q₁ p₂ q₂}
    (u : KuuNativeF45Tree.DepthRotationRoute p leftBefore leftAfter)
    (v : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter) :
    (KuuNativeF45Tree.DepthRotationRoute.trans
        (.leftContext u rightBefore) (.rightContext leftAfter v)).mapAxes F G =
      KuuNativeF45Tree.DepthRotationRoute.trans
        (.leftContext (u.mapAxes F G) (rightBefore.mapAxes F G))
        (.rightContext (leftAfter.mapAxes F G) (v.mapAxes F G)) := by
  rfl

/-- This is the positive two-axis F55 HORIZONTAL NATURALITY square:
transport the true Type-generated left-then-right higher paste,
or independently transport the two cells and then paste them.
The result is EQUALITY in the SPECIFIED full-shadow quotient,
proved with its faithful observer, not imposed on raw syntax. -/
theorem nativeF55ThreeHorizontal_mapAxesNative
    (F : A ⥤ C) (G : B ⥤ D)
    {p : Polygon} {a b : A} {x y : B}
    {n n' m m' k k' l l' : Nat}
    {p₀ p₁ p₂ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ : KuuNativeBlocks x y}
    {leftBefore : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
    {leftAfter : KuuNativeF45Tree p n' m' p₀ q₀ p₁ q₁}
    {rightBefore : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂}
    {rightAfter : KuuNativeF45Tree p k' l' p₁ q₁ p₂ q₂}
    {u u' : KuuNativeF45Tree.DepthRotationRoute p leftBefore leftAfter}
    {v v' : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter}
    (f : NativeF55ThreeHom u u')
    (g : NativeF55ThreeHom v v') :
    (nativeF55ThreeHorizontal f g).mapAxesGivenPentagon F G
       (nativeF55MappedDataFromRootCancellation F G) =
      nativeF55ThreeHorizontal
        (f.mapAxesGivenPentagon F G
          (nativeF55MappedDataFromRootCancellation F G))
        (g.mapAxesGivenPentagon F G
          (nativeF55MappedDataFromRootCancellation F G)) := by
  apply nativeF55ThreeEval_injective
  -- Explicitly instantiate the dependent horizontal-evaluation theorem:
  -- the transported route boundaries are definitionally normalized,
  -- but an uninstantiated simp rewrite may leave this instance untouched.
  have hHorizontal :=
    nativeF55ThreeEval_horizontal
      (f.mapAxesGivenPentagon F G
        (nativeF55MappedDataFromRootCancellation F G))
      (g.mapAxesGivenPentagon F G
        (nativeF55MappedDataFromRootCancellation F G))
  simp only [NativeF55ThreeHom.mapAxesGivenPentagon_eval] at hHorizontal
  simpa only [NativeF55ThreeHom.mapAxesGivenPentagon_eval,
    nativeF55ThreeEval_horizontal] using hHorizontal.symm

/-- Actual Mathlib functor of independently typed native F54
rotation-route objects and independently presented nine-generator
F55 shadow-quotient higher morphisms. -/
def nativeF55ThreeFunctorNative
    (F : A ⥤ C) (G : B ⥤ D)
    {p : Polygon} {a b : A} {x y : B}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :
    (KuuNativeF45Tree.DepthRotationRoute p first last) ⥤
      (KuuNativeF45Tree.DepthRotationRoute p
        (first.mapAxes F G) (last.mapAxes F G)) :=
  nativeF55ThreeFunctorGivenPentagon F G
    (nativeF55MappedDataFromRootCancellation F G) first last

/-- The full selected-shadow quotient action is faithful on
EVERY genuine native F55 3-Hom, without requiring faithfulness
of the two original category functors on 1-arrows. -/
theorem nativeF55ThreeFunctorNative_faithful
    (F : A ⥤ C) (G : B ⥤ D)
    {p : Polygon} {a b : A} {x y : B}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : u ⟶ v}
    (h : (nativeF55ThreeFunctorNative F G first last).map f =
      (nativeF55ThreeFunctorNative F G first last).map g) :
    f = g :=
  nativeF55ThreeFunctorGivenPentagon_map_injective F G
    (nativeF55MappedDataFromRootCancellation F G) first last h

/-- Even after arbitrary functorial transport, the chosen native
full-shadow quotient admits NO arrow of the explicit mismatched
second-charge/phase configuration (0,1;0). This is a constraint
on this selected observer, NOT a global obstruction theorem. -/
theorem nativeF55ThreeNative_no_mismatched_phase
    (F : A ⥤ C) (G : B ⥤ D)
    {p : Polygon} {a b : A} {x y : B}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55ThreeHom u v) :
    nativeF55ThreeEval (f.mapAxesGivenPentagon F G
      (nativeF55MappedDataFromRootCancellation F G)) ≠
      (((0 : Int), (1 : Int)), (0 : ZMod 2)) := by
  rw [f.mapAxesGivenPentagon_eval F G
    (nativeF55MappedDataFromRootCancellation F G)]
  exact f.no_shadow_delta

/-- The actual top-hexagon six-sector, two-independent-F54-rotation
square is a REAL source witness. Under arbitrary functors from
the native incidence site, the odd and even phase recipients
have equal signed charges and STILL have different phases. -/
theorem northHexagon_nativeF55_phaseChoice_mapAxes
    (F : Site ⥤ C) (G : Site ⥤ D) :
    let mapped := northHexagonNativeF55SquareCell.mapAxesGivenPentagon
      F G (nativeF55MappedDataFromRootCancellation F G)
    (mapped.interpret
      (nativeF55EvenPhaseTarget (D := C) (E := D)
        (.hexagon (.top 0)))).1 =
    (mapped.interpret
      (nativeF55FullShadowTarget (D := C) (E := D)
        (.hexagon (.top 0)))).1 ∧
    (mapped.interpret
      (nativeF55EvenPhaseTarget (D := C) (E := D)
        (.hexagon (.top 0)))).2 ≠
    (mapped.interpret
      (nativeF55FullShadowTarget (D := C) (E := D)
        (.hexagon (.top 0)))).2 :=
  northHexagonNativeF55Square_mapAxes_phase_choice F G
    (nativeF55MappedDataFromRootCancellation F G)

#print axioms nativeF55MappedDataFromRootCancellation
#print axioms KuuNativeF45Tree.DepthRotationRoute.PresentedCell.mapAxesNative
#print axioms KuuNativeF45Tree.DepthRotationRoute.PresentedCell.mapAxesNative_shape
#print axioms KuuNativeF45Tree.DepthRotationRoute.PresentedCell.mapAxesNative_shadow
#print axioms nativeF55HorizontalRoute_mapAxes
#print axioms nativeF55ThreeHorizontal_mapAxesNative
#print axioms nativeF55ThreeFunctorNative
#print axioms nativeF55ThreeFunctorNative_faithful
#print axioms nativeF55ThreeNative_no_mismatched_phase
#print axioms northHexagon_nativeF55_phaseChoice_mapAxes

end
end Kuu.F112.Physical
