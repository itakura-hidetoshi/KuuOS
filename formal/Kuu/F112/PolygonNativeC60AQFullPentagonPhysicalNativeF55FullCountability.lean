import Mathlib.Tactic.DeriveCountable
import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeF55PrimitiveCountability

/-!
# F112-P94D3GJ2 — all nine original Type-valued native F55 constructors

GI established complete original F45/LocalRotation/F54 DepthRotationRoute
proof smallness under explicit input-category object and Hom Countable.
GJ1 established the genuine fully typed primitive pentagon and square
source atom alphabets and a faithful interpretation to the raw F55 source.

This file tests the PINNED Mathlib Countable deriving handler on the
ACTUAL original nine-constructor PresentedCell inductive, including
ident, pentagon, disjointSquare, symm, trans, leftContext,
rightContext, precompose and postcompose, without replacing or
quotienting the source Type-valued proof grammar. Its recursive source
certificate should be countable under explicit input-category object
and every individual Hom fiber Countable.

No equivalence to historical P92B or old F19/F28/F54/F55,
unconditional original 14D, 19D filler or global strict coherence.
Strict Kuu primary, independent Kuu remains a presentation,
107 public roots, append-only, Gray not reintroduced.
Pinned Lean v4.30.0-rc2, mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uD vD uE vE

/-! Actual unmodified, proof-relevant native source types receive
local Countable instances only from explicitly small D/E categories. -/

private noncomputable instance nativeGJ2CountableF45
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    [Countable D] [∀ a b : D, Countable (a ⟶ b)]
    {E : Type uE} [Category.{vE} E]
    [Countable E] [∀ x y : E, Countable (x ⟶ y)]
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y} :
    Countable (KuuNativeF45Tree p n m ma pa mb pb) :=
  nativeGHOriginalF45Fiber_countable
    inferInstance (fun _ _ => inferInstance)
    inferInstance (fun _ _ => inferInstance)
    n m ma mb pa pb

private noncomputable instance nativeGJ2CountableLocalRotation
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    [Countable D] [∀ a b : D, Countable (a ⟶ b)]
    {E : Type uE} [Category.{vE} E]
    [Countable E] [∀ x y : E, Countable (x ⟶ y)]
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {before after : KuuNativeF45Tree p n m ma pa mb pb} :
    Countable (KuuNativeF45Tree.LocalRotation p before after) :=
  nativeGIOriginalLocalFiber_countable
    inferInstance (fun _ _ => inferInstance)
    inferInstance (fun _ _ => inferInstance)
    before after

private noncomputable instance nativeGJ2CountableDepthRotationRoute
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    [Countable D] [∀ a b : D, Countable (a ⟶ b)]
    {E : Type uE} [Category.{vE} E]
    [Countable E] [∀ x y : E, Countable (x ⟶ y)]
    {a b : D} {x y : E}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {n n' m m' : Nat}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb} :
    Countable (KuuNativeF45Tree.DepthRotationRoute p first last) :=
  nativeGIOriginalDepthFiber_countable
    inferInstance (fun _ _ => inferInstance)
    inferInstance (fun _ _ => inferInstance)
    first last

section OriginalNineConstructors

variable {D : Type uD} [Category.{vD} D] [Countable D]
variable [∀ a b : D, Countable (a ⟶ b)]
variable {E : Type uE} [Category.{vE} E] [Countable E]
variable [∀ x y : E, Countable (x ⟶ y)]

/-- Derive a faithful Nat code (plus injectivity theorem) for the
ACTUAL dependent nine-constructor F55 Type-valued proof grammar.
No scalar observer, quotient or invented 3-cell operation appears. -/
deriving instance Countable for KuuNativeF45Tree.DepthRotationRoute.PresentedCell

end OriginalNineConstructors

/-- Every original indexed nine-constructor F55 Type-valued
proof fiber is countable under precisely explicit local D/E smallness. -/
theorem nativeGJ2OriginalPresentedFiber_countable
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    (hobjD : Countable D)
    (hhomD : ∀ a b : D, Countable (a ⟶ b))
    (hobjE : Countable E)
    (hhomE : ∀ x y : E, Countable (x ⟶ y))
    {a b : D} {x y : E}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {n n' m m' : Nat}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (r s : KuuNativeF45Tree.DepthRotationRoute p first last) :
    Countable (KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) := by
  letI : Countable D := hobjD
  letI : ∀ a b : D, Countable (a ⟶ b) := hhomD
  letI : Countable E := hobjE
  letI : ∀ x y : E, Countable (x ⟶ y) := hhomE
  infer_instance

/-- The entire ORIGINAL F55 nine-constructor source Type total:
actual D/E categorical objects, all original block/grade/tree/route
boundaries AND the full original Type-valued 3-cell proof. -/
theorem nativeGJ2OriginalPresentedTotal_countable
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    (hobjD : Countable D)
    (hhomD : ∀ a b : D, Countable (a ⟶ b))
    (hobjE : Countable E)
    (hhomE : ∀ x y : E, Countable (x ⟶ y)) :
    Countable (NativeGJOriginalPresentedTotal p D E) := by
  letI : Countable (NativeGJOriginalParallelTotal p D E) :=
    nativeGJOriginalParallelTotal_countable hobjD hhomD hobjE hhomE
  letI : ∀ parallel : NativeGJOriginalParallelTotal p D E,
      Countable (KuuNativeF45Tree.DepthRotationRoute.PresentedCell p
        parallel.1.2 parallel.2) := by
    intro parallel
    rcases parallel with
      ⟨⟨⟨a, b, x, y, ma, pa, mb, pb, n, n', m, m',
          first, last⟩, r⟩, s⟩
    exact nativeGJ2OriginalPresentedFiber_countable
      hobjD hhomD hobjE hhomE r s
  infer_instance

/-- Genuine C60 Site×Site F55 full original raw nine-constructor
proof total is countable: no arbitrary D/E Hom is inferred. -/
theorem nativeGJ2PhysicalPresentedTotal_countable (p : Polygon) :
    Countable (NativeGJOriginalPresentedTotal p Site Site) :=
  nativeGJ2OriginalPresentedTotal_countable
    nativeC60GEPhysicalSite_countable
    nativeC60GEPhysicalIncidenceHom_countable
    nativeC60GEPhysicalSite_countable
    nativeC60GEPhysicalIncidenceHom_countable

/-- Every complete raw F55 nine-constructor proof fiber at genuine
C60 sites is countable, preserving the original parallel F54 proofs. -/
theorem nativeGJ2PhysicalPresentedFiber_countable
    (p : Polygon)
    {a b x y : Site}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {n n' m m' : Nat}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (r s : KuuNativeF45Tree.DepthRotationRoute p first last) :
    Countable (KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :=
  nativeGJ2OriginalPresentedFiber_countable
    nativeC60GEPhysicalSite_countable
    nativeC60GEPhysicalIncidenceHom_countable
    nativeC60GEPhysicalSite_countable
    nativeC60GEPhysicalIncidenceHom_countable r s

/-- Countable all original F55 nine-constructor proof sources
over all 32 actually existing C60 polygon carriers. -/
theorem nativeGJ2PhysicalAllPolygonPresented_countable :
    Countable (Σ p : Polygon,
      NativeGJOriginalPresentedTotal p Site Site) := by
  letI : Countable Polygon := nativeC60GEPhysicalPolygon_countable
  letI : ∀ p : Polygon,
      Countable (NativeGJOriginalPresentedTotal p Site Site) :=
    nativeGJ2PhysicalPresentedTotal_countable
  infer_instance

#print axioms nativeGJ2OriginalPresentedFiber_countable
#print axioms nativeGJ2OriginalPresentedTotal_countable
#print axioms nativeGJ2PhysicalPresentedTotal_countable
#print axioms nativeGJ2PhysicalPresentedFiber_countable
#print axioms nativeGJ2PhysicalAllPolygonPresented_countable

end
end Kuu.F112.Physical
