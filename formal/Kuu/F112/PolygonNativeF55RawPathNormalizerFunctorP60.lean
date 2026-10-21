import Kuu.F112.PolygonNativeF55RawVerticalNormalizationP59

/-!
# F112-P60 — genuine typed F55 raw-path normalization functor

P58 proves the nine-constructor raw F55 proof terms are not a strict
category at source. P59 normalizes raw vertical identity/composition
to nil/path concatenation, keeping the other seven source constructors
as actual singleton paths.

This file extends the P59 rule from every raw generator to ALL finite
paths by the pinned Mathlib free-path universal property (Paths.lift).
Raw vertical pasting as a singleton generator and the two-step composite
are identified after normalization, but remain distinct source data.

This is one presentation of F55, not a unique "empty" representation,
not a proof of original/raw 3-category interchange, and not a completed
global strict 3/n-category or (∞,3)-hyperdescent. No Gray or legacy
KUOS imports, no new axioms, sorry or admit.
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

/-- P59's raw generator normal form extended by the Mathlib free-path
universal property to every finite typed raw F55 path word. -/
def nativeF55RawPathNormalizer
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :
    NativeF55RawPathCategory first last ⥤
      NativeF55RawPathCategory first last :=
  CategoryTheory.Paths.lift {
    obj := fun vertex => vertex
    map := fun {_r _s} raw => raw.toNativeStrictPath
  }

/-- Exact compatibility with the earlier genuine P59 structural
normalization for every one of the nine raw F55 constructors. -/
@[simp] theorem nativeF55RawPathNormalizer_map_raw
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (raw : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    (nativeF55RawPathNormalizer first last).map
        (raw.toPath : Quiver.Path
          (⟨r⟩ : NativeF55RawRouteVertex first last)
          (⟨s⟩ : NativeF55RawRouteVertex first last)) =
      raw.toNativeStrictPath := by
  exact CategoryTheory.Paths.lift_toPath _ raw

/-- A SINGLE raw identity generator is sent to the strict categorical
identity: source syntax is not equated with the identity. -/
theorem nativeF55RawPathNormalizer_map_raw_ident
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (r : KuuNativeF45Tree.DepthRotationRoute p first last) :
    (nativeF55RawPathNormalizer first last).map
      ((KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident r).toPath) =
      (𝟙 (⟨r⟩ : NativeF55RawRouteVertex first last)) := by
  rw [nativeF55RawPathNormalizer_map_raw]
  rfl

/-- The chosen normalizer sends the source raw vertical constructor
(single path-generator) to the same path as true categorical
composition of the two raw generators. This is NOT raw term equality. -/
theorem nativeF55RawPathNormalizer_map_raw_trans_eq_composite
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s)
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p s t) :
    (nativeF55RawPathNormalizer first last).map
      ((KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans f g).toPath) =
    (nativeF55RawPathNormalizer first last).map
      (f.toPath.comp g.toPath) := by
  rw [nativeF55RawPathNormalizer_map_raw,
    KuuNativeF45Tree.DepthRotationRoute.PresentedCell.toNativeStrictPath_trans]
  rw [Functor.map_comp,
    nativeF55RawPathNormalizer_map_raw,
    nativeF55RawPathNormalizer_map_raw]
  rfl

/-- Genuine noninjectivity on every inhabited raw Hom persists for
the functor acting on the *original* singleton generators. -/
theorem nativeF55RawPathNormalizer_notInjective_on_raw_generators
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    ¬ Function.Injective
      (fun c : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s =>
        (nativeF55RawPathNormalizer first last).map c.toPath) := by
  intro hinj
  have hSource :
      Function.Injective
        (fun c : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s =>
          c.toNativeStrictPath) := by
    intro left right heq
    apply hinj
    simpa only [nativeF55RawPathNormalizer_map_raw] using heq
  exact f.toNativeStrictPath_notInjective hSource

#print axioms nativeF55RawPathNormalizer
#print axioms nativeF55RawPathNormalizer_map_raw
#print axioms nativeF55RawPathNormalizer_map_raw_ident
#print axioms nativeF55RawPathNormalizer_map_raw_trans_eq_composite
#print axioms nativeF55RawPathNormalizer_notInjective_on_raw_generators

end
end Kuu.F112.Physical
