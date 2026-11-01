import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4BHGradeRankFaithfulness
import Mathlib.CategoryTheory.Equivalence
import Mathlib.Tactic

/-!
F112-P94D3GK4BI — an ACTUAL Mathlib equivalence of the existing
K_AI second-kernel category with the category of genuinely attained
old-AH integer matrices.

GK4BF constructs the actual-image Category and the genuine
K_AI -> attained-AH Functor. GK4BH proves its map bijective on
EVERY original typed Hom, by the first polynomial jet and real
physical source-rank/Boolean-grade criterion. The two stage wrappers
also have exactly the SAME original F45 typed boundary objects.
We now supply object and Hom Equiv data, construct full/faithful and
essential surjectivity, and invoke pinned Mathlib Functor.asEquivalence
to produce true natural unit and counit isomorphisms.

Never identifies any unattained ambient integer matrix, raw original
F54 route, independent structural S, or original Q category law.
No Type-valued 3-cell, Gray reintroduction, global strictness or
hyperdescent. Append-only/tighten-only/overwrite-forbidden/same-root107.
Lean v4.30.0-rc2; pinned mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Protected validation PR #1558 remains Draft/OPEN/unmerged.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section
universe uD vD uE vE

section GenuineAttainedAHCategoryEquivalence
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}

/-- The two EXISTING category wrappers have exactly the same
actual, dependently typed original F45 boundary objects. -/
def nativeGK4BIObjectEquiv
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :
    NativeGK4AIKernelStage p ma mb pa pb ≃
      NativeGK4BFAttainedAHStage p ma mb pa pb where
  toFun X := ⟨X.original⟩
  invFun Y := ⟨Y.original⟩
  left_inv := by
    intro X
    cases X
    rfl
  right_inv := by
    intro Y
    cases Y
    rfl

/-- The TRUE old-AH image map is a bijection on each actual K_AI
Hom; the inverse here is an inverse of the already-established
K_AI quotient Hom, not of the source F54 path type. -/
noncomputable def nativeGK4BIHomEquiv
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (X Y : NativeGK4AIKernelStage p ma mb pa pb) :
    (X ⟶ Y) ≃
      ((nativeGK4BFImageFunctor p ma mb pa pb).obj X ⟶
       (nativeGK4BFImageFunctor p ma mb pa pb).obj Y) :=
  Equiv.ofBijective
    (fun f : X ⟶ Y =>
      (nativeGK4BFImageFunctor p ma mb pa pb).map f)
    (nativeGK4BHImageFunctor_bijective_hom p ma mb pa pb X Y)

/-- Actual inverse on the map of each typed Hom, defined by
GK4BH bijectivity, with no fabricated source witness. -/
noncomputable def nativeGK4BIHomInverse
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (X Y : NativeGK4AIKernelStage p ma mb pa pb)
    (f : (nativeGK4BFImageFunctor p ma mb pa pb).obj X ⟶
         (nativeGK4BFImageFunctor p ma mb pa pb).obj Y) :
    X ⟶ Y :=
  (nativeGK4BIHomEquiv p ma mb pa pb X Y).symm f

/-- Taking an actual AH value back to K_AI and observing it
again returns exactly the original attained matrix. -/
theorem nativeGK4BIMap_homInverse
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (X Y : NativeGK4AIKernelStage p ma mb pa pb)
    (f : (nativeGK4BFImageFunctor p ma mb pa pb).obj X ⟶
         (nativeGK4BFImageFunctor p ma mb pa pb).obj Y) :
    (nativeGK4BFImageFunctor p ma mb pa pb).map
      (nativeGK4BIHomInverse p ma mb pa pb X Y f) = f := by
  exact (nativeGK4BIHomEquiv p ma mb pa pb X Y).apply_symm_apply f

/-- The inverse sends an actual K_AI Hom's observation back to
that same K_AI Hom (not to its original raw F54 representative). -/
theorem nativeGK4BIHomInverse_map
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (X Y : NativeGK4AIKernelStage p ma mb pa pb)
    (f : X ⟶ Y) :
    nativeGK4BIHomInverse p ma mb pa pb X Y
      ((nativeGK4BFImageFunctor p ma mb pa pb).map f) = f := by
  exact (nativeGK4BIHomEquiv p ma mb pa pb X Y).symm_apply_apply f

/-- Explicit pinned-Mathlib FullyFaithful data, derived from
proven genuine Hom bijectivity, rather than from an assumption. -/
noncomputable def nativeGK4BIFullyFaithful
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :
    (nativeGK4BFImageFunctor p ma mb pa pb).FullyFaithful where
  preimage {X Y} f := nativeGK4BIHomInverse p ma mb pa pb X Y f
  map_preimage {X Y} f := nativeGK4BIMap_homInverse p ma mb pa pb X Y f
  preimage_map {X Y} f := nativeGK4BIHomInverse_map p ma mb pa pb X Y f

/-- Object surjectivity is literal, not only up to abstract
essential surjectivity: both wrappers preserve the same F45 stage. -/
theorem nativeGK4BIImage_obj_surjective
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :
    Function.Surjective
      (nativeGK4BFImageFunctor p ma mb pa pb).obj := by
  intro Y
  refine ⟨⟨Y.original⟩, ?_⟩
  cases Y
  rfl

/-- The actual category-image functor meets exactly the Mathlib
faithful/full/essentially-surjective criterion for equivalence. -/
@[implicit_reducible] noncomputable def nativeGK4BIImageIsEquivalence
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :
    (nativeGK4BFImageFunctor p ma mb pa pb).IsEquivalence := by
  let hFF := nativeGK4BIFullyFaithful p ma mb pa pb
  exact
    { faithful := hFF.faithful
      full := hFF.full
      essSurj := Functor.essSurj_of_surj
        (nativeGK4BIImage_obj_surjective p ma mb pa pb) }

/-- MAIN GK4BI RESULT: a true Mathlib equivalence of categories,
whose forward Functor is the GENUINE GK4BF old-AH image functor,
whose reverse is a genuine Mathlib Functor, and whose unit/counit
are actual natural isomorphisms, not a hom-set slogan. -/
noncomputable def nativeGK4BIAttainedAHEquivalence
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :
    NativeGK4AIKernelStage p ma mb pa pb ≌
      NativeGK4BFAttainedAHStage p ma mb pa pb := by
  letI : (nativeGK4BFImageFunctor p ma mb pa pb).IsEquivalence :=
    nativeGK4BIImageIsEquivalence p ma mb pa pb
  exact (nativeGK4BFImageFunctor p ma mb pa pb).asEquivalence

/-- No functor was replaced by a mere isomorphic substitute:
the forward equivalence Functor is definitionally the old actual
K_AI -> genuinely attained AH image Functor. -/
@[simp] theorem nativeGK4BIAttainedAHEquivalence_functor
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :
    (nativeGK4BIAttainedAHEquivalence p ma mb pa pb).functor =
      nativeGK4BFImageFunctor p ma mb pa pb := rfl

/-- Mathlib's actual quasi-inverse Functor, including its proven
map-id and map-comp obligations, not a choice of raw source routes. -/
noncomputable def nativeGK4BIReverseFunctor
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :
    NativeGK4BFAttainedAHStage p ma mb pa pb ⥤
      NativeGK4AIKernelStage p ma mb pa pb :=
  (nativeGK4BIAttainedAHEquivalence p ma mb pa pb).inverse

/-- The genuine natural unit isomorphism of GK4BI. -/
noncomputable def nativeGK4BIUnitIso
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :
    (𝟭 (NativeGK4AIKernelStage p ma mb pa pb)) ≅
      (nativeGK4BIAttainedAHEquivalence p ma mb pa pb).functor ⋙
        nativeGK4BIReverseFunctor p ma mb pa pb :=
  (nativeGK4BIAttainedAHEquivalence p ma mb pa pb).unitIso

/-- The genuine natural counit isomorphism of GK4BI. -/
noncomputable def nativeGK4BICounitIso
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :
    nativeGK4BIReverseFunctor p ma mb pa pb ⋙
      (nativeGK4BIAttainedAHEquivalence p ma mb pa pb).functor ≅
        (𝟭 (NativeGK4BFAttainedAHStage p ma mb pa pb)) :=
  (nativeGK4BIAttainedAHEquivalence p ma mb pa pb).counitIso

/-- The exact triangle identity, a genuine componentwise equation
between natural-isomorphism parts in Mathlib, supplied by the
constructed Equivalence. -/
theorem nativeGK4BI_triangle
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (X : NativeGK4AIKernelStage p ma mb pa pb) :
    (nativeGK4BIAttainedAHEquivalence p ma mb pa pb).functor.map
      ((nativeGK4BIUnitIso p ma mb pa pb).hom.app X) ≫
      (nativeGK4BICounitIso p ma mb pa pb).hom.app
        ((nativeGK4BIAttainedAHEquivalence p ma mb pa pb).functor.obj X) =
    𝟙 ((nativeGK4BIAttainedAHEquivalence p ma mb pa pb).functor.obj X) :=
  (nativeGK4BIAttainedAHEquivalence p ma mb pa pb).functor_unitIso_comp X

end GenuineAttainedAHCategoryEquivalence

#print axioms nativeGK4BIObjectEquiv
#print axioms nativeGK4BIHomEquiv
#print axioms nativeGK4BIHomInverse
#print axioms nativeGK4BIMap_homInverse
#print axioms nativeGK4BIHomInverse_map
#print axioms nativeGK4BIFullyFaithful
#print axioms nativeGK4BIImage_obj_surjective
#print axioms nativeGK4BIImageIsEquivalence
#print axioms nativeGK4BIAttainedAHEquivalence
#print axioms nativeGK4BIAttainedAHEquivalence_functor
#print axioms nativeGK4BIReverseFunctor
#print axioms nativeGK4BIUnitIso
#print axioms nativeGK4BICounitIso
#print axioms nativeGK4BI_triangle

end
end Kuu.F112.Physical
