import Kuu.F112.PolygonNativeF55RawVerticalNormalizationP59

/-!
# F112-P60 — independent strict path envelope / chosen observer boundary

This continues P58/P59 with no Gray, historical KUOS, or assumed
higher interchange. Every actual Type-valued native F55 source cell
is a generating arrow of the separately defined free path category.
Its chosen quotient interpretation factors through the Mathlib
free-path universal extension, with no loss at the GENERATOR map.

However the free-path functor to the chosen shadow quotient is not
faithful: the genuine raw F55 identity constructor is a length-one
generating edge, whereas the free-path categorical identity is an
empty path. Both map to the same quotient identity. This proves a
strict concrete no-go for reconstructing arbitrary raw path histories
from that chosen observer, not a no-go for strict 3-category itself.

The previous P59 normalization deliberately maps raw identities to
empty paths. It therefore differs from the singleton-edge embedding:
that difference is recorded, never suppressed by substituting shadow
equality for equality of proof-relevant syntax.

No new axioms, no sorry/admit, no Gray imports.
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

/-- Every actual, typed raw F55 proof-cell generator maps
to its own original chosen-shadow quotient class, NOT to an
invented numeric generator. This is Mathlib's path-lift property
for the genuine independent F55 typed source quiver. -/
theorem nativeF55RawPathsToShadow_generator
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (cell : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    (nativeF55RawPathsToShadow first last).map
      (cell.toNativeRawEdge.toPath) =
      nativeF55ThreeOf cell := by
  let phi :
      NativeF55RawRouteVertex first last ⥤q
        (KuuNativeF45Tree.DepthRotationRoute p first last) :=
    { obj := fun vertex => vertex.route
      map := fun {_X _Y} raw => nativeF55ThreeOf raw }
  change (CategoryTheory.Paths.lift phi).map
      cell.toNativeRawEdge.toPath = phi.map cell.toNativeRawEdge
  exact CategoryTheory.Paths.lift_toPath phi cell.toNativeRawEdge

/-- The COMPLETE independent nine-constructor raw F55 cell
normalization commutes with the selected shadow observer:
canonical empty paths and concatenation account for raw identity
and vertical paste, and all seven other constructors remain genuine
singleton paths under Mathlib's free-path functor. This equality is
ONLY in the selected proof-term quotient, never in raw syntax. -/
theorem KuuNativeF45Tree.DepthRotationRoute.PresentedCell.toNativeStrictPath_shadow
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (cell : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    (nativeF55RawPathsToShadow first last).map cell.toNativeStrictPath =
      nativeF55ThreeOf cell := by
  induction cell with
  | ident route =>
      rfl
  | pentagon t₁ t₂ t₃ t₄ =>
      exact nativeF55RawPathsToShadow_generator _ _
        (.pentagon t₁ t₂ t₃ t₄)
  | disjointSquare left right =>
      exact nativeF55RawPathsToShadow_generator _ _
        (.disjointSquare left right)
  | symm c _ =>
      exact nativeF55RawPathsToShadow_generator _ _ (.symm c)
  | trans c d ihc ihd =>
      change (nativeF55RawPathsToShadow first last).map
          (c.toNativeStrictPath.comp d.toNativeStrictPath) =
        nativeF55ThreeOf (.trans c d)
      have hcomp := (nativeF55RawPathsToShadow first last).map_comp
        c.toNativeStrictPath d.toNativeStrictPath
      rw [hcomp, ihc, ihd]
      rfl
  | leftContext c later _ =>
      exact nativeF55RawPathsToShadow_generator _ _
        (.leftContext c later)
  | rightContext earlier c _ =>
      exact nativeF55RawPathsToShadow_generator _ _
        (.rightContext earlier c)
  | precompose prior c _ =>
      exact nativeF55RawPathsToShadow_generator _ _
        (.precompose prior c)
  | postcompose c suffix _ =>
      exact nativeF55RawPathsToShadow_generator _ _
        (.postcompose c suffix)

/-- The FULL selected charge and odd exchange phase of an arbitrary
normalized raw cell are therefore the original raw source shadow,
not a replacement determined by an unproved historical comparison. -/
theorem KuuNativeF45Tree.DepthRotationRoute.PresentedCell.toNativeStrictPath_shadow_eval
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (cell : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    nativeF55ThreeEval
      ((nativeF55RawPathsToShadow first last).map cell.toNativeStrictPath) =
      cell.nativeShadow := by
  rw [cell.toNativeStrictPath_shadow]
  rfl

/-- The chosen quotient cannot distinguish the length-zero
identity path from the length-one genuine F55 raw identity GENERATOR.
No blanket claim about the original Type-valued source equality. -/
theorem nativeF55RawPathsToShadow_notInjectiveAt
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (r : KuuNativeF45Tree.DepthRotationRoute p first last) :
    ¬ Function.Injective
      (fun path :
        Quiver.Path
          (⟨r⟩ : NativeF55RawRouteVertex first last)
          (⟨r⟩ : NativeF55RawRouteVertex first last) =>
          (nativeF55RawPathsToShadow first last).map path) := by
  intro hinj
  let e : (⟨r⟩ : NativeF55RawRouteVertex first last) ⟶
      (⟨r⟩ : NativeF55RawRouteVertex first last) :=
    KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident r
  have hmap :
      (nativeF55RawPathsToShadow first last).map
        (Quiver.Path.nil :
          Quiver.Path
            (⟨r⟩ : NativeF55RawRouteVertex first last)
            (⟨r⟩ : NativeF55RawRouteVertex first last)) =
      (nativeF55RawPathsToShadow first last).map e.toPath := by
    change nativeF55ThreeOf
        (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident r) =
      (nativeF55RawPathsToShadow first last).map e.toPath
    exact (nativeF55RawPathsToShadow_generator first last
      (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident r)).symm
  have hlength := congrArg Quiver.Path.length (hinj hmap)
  simp at hlength

#print axioms nativeF55RawPathsToShadow_generator
#print axioms nativeF55RawPathsToShadow_notInjectiveAt
#print axioms KuuNativeF45Tree.DepthRotationRoute.PresentedCell.toNativeStrictPath_shadow
#print axioms KuuNativeF45Tree.DepthRotationRoute.PresentedCell.toNativeStrictPath_shadow_eval

end
end Kuu.F112.Physical
