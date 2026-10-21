import Kuu.F112.PolygonNativeF55RawStrictificationBoundary

/-!
# F112-P59 — native raw F55 vertical normalization to a strict free path

The free Type-valued F55 cell syntax is not a strict category: P58
proves that raw units and raw associators remain distinct trees.
This file instead gives an explicit proof-recursive normalization
INTO the independent, typed free path category already constructed.

The raw identity constructor maps to the genuine empty path.
The raw vertical composition constructor maps to path concatenation.
All other seven raw constructors (physical pentagon, physical square,
inverse, the two contexts and the two route whiskerings) remain
their own SINGLE GENERATOR paths, with no illicit source equality,
exchange axiom, Gray import or fabricated inverse cancellation.

The results prove strict unit and associativity AFTER normalization
and show normalization is necessarily noninjective on raw proof terms.
This is an honest choice of presentation, not a proof of global
strict 3-category or dependent-origination hyperdescent.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

/-- One exact proof-recursive vertical normalization:
only the distinguished raw unit and raw vertical-paste constructor
become structural categorical operations. The other seven real
F55 source constructors are retained as atomic edges. -/
def KuuNativeF45Tree.DepthRotationRoute.PresentedCell.toNativeStrictPath
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb} :
    ∀ {r s : KuuNativeF45Tree.DepthRotationRoute p first last},
      KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s →
      Quiver.Path
        (⟨r⟩ : NativeF55RawRouteVertex first last)
        (⟨s⟩ : NativeF55RawRouteVertex first last)
  | _, _, .ident _ => .nil
  | _, _, .trans left right =>
      left.toNativeStrictPath |>.comp right.toNativeStrictPath
  | _, _, raw => raw.toPath

/-- Strict unit is true for the *normalized path*, not for the
raw source proof tree (which P58 proves unequal). -/
@[simp] theorem KuuNativeF45Tree.DepthRotationRoute.PresentedCell.toNativeStrictPath_ident
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (r : KuuNativeF45Tree.DepthRotationRoute p first last) :
    (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident r).toNativeStrictPath =
      (Quiver.Path.nil :
        Quiver.Path (⟨r⟩ : NativeF55RawRouteVertex first last) ⟨r⟩) := rfl

/-- Actual typed vertical source pasting normalizes to strict path
concatenation, for arbitrary original F54 route endpoints. -/
@[simp] theorem KuuNativeF45Tree.DepthRotationRoute.PresentedCell.toNativeStrictPath_trans
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s)
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p s t) :
    (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans f g).toNativeStrictPath =
      f.toNativeStrictPath.comp g.toNativeStrictPath := rfl

/-- On the source the raw equality is false; on normalized paths
right-unit cancellation is explicitly proved from Mathlib paths. -/
theorem KuuNativeF45Tree.DepthRotationRoute.PresentedCell.toNativeStrictPath_rightUnit
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans f (.ident s)).toNativeStrictPath =
      f.toNativeStrictPath := by
  simp only [KuuNativeF45Tree.DepthRotationRoute.PresentedCell.toNativeStrictPath_trans,
    KuuNativeF45Tree.DepthRotationRoute.PresentedCell.toNativeStrictPath_ident,
    Quiver.Path.comp_nil]

theorem KuuNativeF45Tree.DepthRotationRoute.PresentedCell.toNativeStrictPath_leftUnit
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans (.ident r) f).toNativeStrictPath =
      f.toNativeStrictPath := by
  simp only [KuuNativeF45Tree.DepthRotationRoute.PresentedCell.toNativeStrictPath_trans,
    KuuNativeF45Tree.DepthRotationRoute.PresentedCell.toNativeStrictPath_ident,
    Quiver.Path.nil_comp]

/-- True strict associativity of the NORMALIZED path representation.
P58 proves the underlying two raw F55 syntax trees remain unequal. -/
theorem KuuNativeF45Tree.DepthRotationRoute.PresentedCell.toNativeStrictPath_assoc
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s t u : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s)
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p s t)
    (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p t u) :
    (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans
      (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans f g) h).toNativeStrictPath =
    (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans
      f (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans g h)).toNativeStrictPath := by
  simp only [KuuNativeF45Tree.DepthRotationRoute.PresentedCell.toNativeStrictPath_trans,
    Quiver.Path.comp_assoc]

/-- A strictly normalized source observation cannot be inverted to
recover EVERY original proof tree. This follows for each inhabited
raw F55 Hom from the certified P58 raw-unit noncollapse. -/
theorem KuuNativeF45Tree.DepthRotationRoute.PresentedCell.toNativeStrictPath_notInjective
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    ¬ Function.Injective
      (fun c : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s =>
        c.toNativeStrictPath) := by
  intro hinj
  exact f.ne_trans_ident (hinj f.toNativeStrictPath_rightUnit.symm)

/-- The chosen strictification does not silently erase the actual
C60 pentagon generator. Its free-path length is one. -/
theorem northNativeF55PentagonCell_normalized_length :
    northNativeF55PentagonCell.toNativeStrictPath.length = 1 := by
  rfl

/-- Likewise the actual C60 six-sector square survives normalization
as a single proof-relevant edge with its own actual F54 boundaries. -/
theorem northHexagonNativeF55SquareCell_normalized_length :
    northHexagonNativeF55SquareCell.toNativeStrictPath.length = 1 := by
  rfl

#print axioms KuuNativeF45Tree.DepthRotationRoute.PresentedCell.toNativeStrictPath
#print axioms KuuNativeF45Tree.DepthRotationRoute.PresentedCell.toNativeStrictPath_ident
#print axioms KuuNativeF45Tree.DepthRotationRoute.PresentedCell.toNativeStrictPath_trans
#print axioms KuuNativeF45Tree.DepthRotationRoute.PresentedCell.toNativeStrictPath_rightUnit
#print axioms KuuNativeF45Tree.DepthRotationRoute.PresentedCell.toNativeStrictPath_leftUnit
#print axioms KuuNativeF45Tree.DepthRotationRoute.PresentedCell.toNativeStrictPath_assoc
#print axioms KuuNativeF45Tree.DepthRotationRoute.PresentedCell.toNativeStrictPath_notInjective
#print axioms northNativeF55PentagonCell_normalized_length
#print axioms northHexagonNativeF55SquareCell_normalized_length

end
end Kuu.F112.Physical
