import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4BJStructuralAttainedAHDescent
import Mathlib.CategoryTheory.Equivalence
import Mathlib.Tactic

/-!
F112-P94D3GK4BK — universal factorization through the *actually attained*
old-AH image of the independent original F45-typed structural category.

F : S -> A_AH^att is the exact GK4BJ full and object-surjective functor.
For an arbitrary Mathlib target category T and actual functor H : S -> T,
we explicitly specify that H kills the same *genuine* AH observation
kernel (on EVERY dependent Hom). Under precisely this condition we
construct the genuine factor functor A_AH^att -> T, prove preservation
of identities and compositions, equality of WHOLE Mathlib functors,
and its uniqueness by source object/Hom surjectivity. We also establish
a necessary and sufficient descent criterion and existence-uniqueness.

No assertion of S faithfulness, original Q category laws, original
Type-valued F54 path equality, missing source 3-cells, or universal
surjectivity onto ALL integer matrices. This is 1-categorical descent,
not hyperdescent. Append-only/tighten-only/same-root107.
Lean v4.30.0-rc2 / pinned mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Protect #1558 Draft/OPEN/unmerged. No Gray reintroduction.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section
universe uD vD uE vE uT vT

section GenuineAHUniversalFactorization
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {T : Type uT} [Category.{vT} T]

/-- Exact source-based condition: a genuine target functor H
cannot distinguish two independent structural S arrows whenever
their ORIGINAL old AH matrices coincide. No source arrows are
declared equal in order to impose this condition. -/
def nativeGK4BKAHKernelCompatible
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (H : NativeGK4IStage p ma mb pa pb ⥤ T) : Prop :=
  ∀ (X Y : NativeGK4IStage p ma mb pa pb) (f g : X ⟶ Y),
    nativeGK4AHStructuralValue X.2.2 Y.2.2 f =
      nativeGK4AHStructuralValue X.2.2 Y.2.2 g →
        H.map f = H.map g

/-- Equivalent statement directly in terms of the ACTUAL
GK4BJ composite's kernel, on every true dependent source Hom. -/
theorem nativeGK4BKCompatible_iff_imageKernel
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (H : NativeGK4IStage p ma mb pa pb ⥤ T) :
    nativeGK4BKAHKernelCompatible p ma mb pa pb H ↔
      (∀ (X Y : NativeGK4IStage p ma mb pa pb) (f g : X ⟶ Y),
        (nativeGK4BJStructuralAHFunctor p ma mb pa pb).map f =
          (nativeGK4BJStructuralAHFunctor p ma mb pa pb).map g →
            H.map f = H.map g) := by
  constructor
  · intro h X Y f g heq
    exact h X Y f g
      ((nativeGK4BJStructuralAH_eq_iff p ma mb pa pb X Y f g).1 heq)
  · intro h X Y f g heq
    exact h X Y f g
      ((nativeGK4BJStructuralAH_eq_iff p ma mb pa pb X Y f g).2 heq)

/-- A genuine original structural S-class representative of each
ACTUALLY reached AH matrix, chosen from the verified GK4BJ
Hom-surjectivity. This is NOT a raw F54 route inverse or a new cell. -/
noncomputable def nativeGK4BKPreimage
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (X Y : NativeGK4BFAttainedAHStage p ma mb pa pb)
    (f : X ⟶ Y) :
    X.original ⟶ Y.original :=
  (nativeGK4BJStructuralAH_surjective_hom
    p ma mb pa pb X.original Y.original f).choose

/-- This chosen preimage reobserves to EXACTLY the given attained
AH matrix at the same original typed F45 endpoints. -/
theorem nativeGK4BKPreimage_spec
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (X Y : NativeGK4BFAttainedAHStage p ma mb pa pb)
    (f : X ⟶ Y) :
    (nativeGK4BJStructuralAHFunctor p ma mb pa pb).map
      (nativeGK4BKPreimage p ma mb pa pb X Y f) = f := by
  exact (nativeGK4BJStructuralAH_surjective_hom
    p ma mb pa pb X.original Y.original f).choose_spec

/-- The lift of the genuine original independent structural
functor H on a single actually attained AH Hom. -/
noncomputable def nativeGK4BKLiftHom
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (H : NativeGK4IStage p ma mb pa pb ⥤ T)
    (X Y : NativeGK4BFAttainedAHStage p ma mb pa pb)
    (f : X ⟶ Y) :
    H.obj X.original ⟶ H.obj Y.original :=
  H.map (nativeGK4BKPreimage p ma mb pa pb X Y f)

/-- As soon as the original AH equality kernel is H-compatible,
the chosen preimage is IMMATERIAL: all source classes realizing the
same attained AH morphism have exactly the same target H-value. -/
theorem nativeGK4BKLiftHom_independent
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (H : NativeGK4IStage p ma mb pa pb ⥤ T)
    (h : nativeGK4BKAHKernelCompatible p ma mb pa pb H)
    (X Y : NativeGK4BFAttainedAHStage p ma mb pa pb)
    (f : X ⟶ Y)
    (s : X.original ⟶ Y.original)
    (hs : (nativeGK4BJStructuralAHFunctor p ma mb pa pb).map s = f) :
    nativeGK4BKLiftHom p ma mb pa pb H X Y f = H.map s := by
  apply h X.original Y.original
    (nativeGK4BKPreimage p ma mb pa pb X Y f) s
  apply (nativeGK4BJStructuralAH_eq_iff
    p ma mb pa pb X.original Y.original _ _).1
  exact (nativeGK4BKPreimage_spec p ma mb pa pb X Y f).trans hs.symm

/-- Actual map-level commutativity on EVERY structural S class. -/
theorem nativeGK4BKLiftHom_on_source
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (H : NativeGK4IStage p ma mb pa pb ⥤ T)
    (h : nativeGK4BKAHKernelCompatible p ma mb pa pb H)
    (X Y : NativeGK4IStage p ma mb pa pb)
    (s : X ⟶ Y) :
    nativeGK4BKLiftHom p ma mb pa pb H
      ⟨X⟩ ⟨Y⟩ ((nativeGK4BJStructuralAHFunctor p ma mb pa pb).map s) =
        H.map s := by
  exact nativeGK4BKLiftHom_independent
    p ma mb pa pb H h ⟨X⟩ ⟨Y⟩
      ((nativeGK4BJStructuralAHFunctor p ma mb pa pb).map s) s rfl

/-- MAIN CONSTRUCTION. The original H genuinely descends through
the old-AH kernel to a Mathlib FUNCTOR on the actual reached AH
category; both source identities and compositions are respected. -/
noncomputable def nativeGK4BKFactorFunctor
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (H : NativeGK4IStage p ma mb pa pb ⥤ T)
    (h : nativeGK4BKAHKernelCompatible p ma mb pa pb H) :
    NativeGK4BFAttainedAHStage p ma mb pa pb ⥤ T where
  obj X := H.obj X.original
  map := fun {X Y} f => nativeGK4BKLiftHom p ma mb pa pb H X Y f
  map_id := by
    intro X
    have hmap :
        (nativeGK4BJStructuralAHFunctor p ma mb pa pb).map
            (𝟙 X.original) = 𝟙 X := by
      exact (nativeGK4BJStructuralAHFunctor p ma mb pa pb).map_id X.original
    have heq := nativeGK4BKLiftHom_independent
      p ma mb pa pb H h X X (𝟙 X) (𝟙 X.original) hmap
    calc
      nativeGK4BKLiftHom p ma mb pa pb H X X (𝟙 X) =
          H.map (𝟙 X.original) := heq
      _ = 𝟙 (H.obj X.original) := H.map_id X.original
  map_comp := by
    intro X Y Z f g
    let sf := nativeGK4BKPreimage p ma mb pa pb X Y f
    let sg := nativeGK4BKPreimage p ma mb pa pb Y Z g
    have hfg :
        (nativeGK4BJStructuralAHFunctor p ma mb pa pb).map
            (sf ≫ sg) = f ≫ g := by
      calc
        (nativeGK4BJStructuralAHFunctor p ma mb pa pb).map (sf ≫ sg) =
            (nativeGK4BJStructuralAHFunctor p ma mb pa pb).map sf ≫
              (nativeGK4BJStructuralAHFunctor p ma mb pa pb).map sg :=
          (nativeGK4BJStructuralAHFunctor p ma mb pa pb).map_comp sf sg
        _ = f ≫ g := by
          rw [nativeGK4BKPreimage_spec, nativeGK4BKPreimage_spec]
    have heq := nativeGK4BKLiftHom_independent
      p ma mb pa pb H h X Z (f ≫ g) (sf ≫ sg) hfg
    calc
      nativeGK4BKLiftHom p ma mb pa pb H X Z (f ≫ g) =
          H.map (sf ≫ sg) := heq
      _ = H.map sf ≫ H.map sg := H.map_comp sf sg

/-- The factor respects all structural Hom classes, not only
the original generators. -/
theorem nativeGK4BKFactor_map
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (H : NativeGK4IStage p ma mb pa pb ⥤ T)
    (h : nativeGK4BKAHKernelCompatible p ma mb pa pb H)
    (X Y : NativeGK4IStage p ma mb pa pb)
    (s : X ⟶ Y) :
    (nativeGK4BKFactorFunctor p ma mb pa pb H h).map
        ((nativeGK4BJStructuralAHFunctor p ma mb pa pb).map s) =
      H.map s := by
  exact nativeGK4BKLiftHom_on_source
    p ma mb pa pb H h X Y s

/-- Exact equality of WHOLE Mathlib functors, including
dependent object maps, identity and composition. -/
theorem nativeGK4BKFactor_functor
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (H : NativeGK4IStage p ma mb pa pb ⥤ T)
    (h : nativeGK4BKAHKernelCompatible p ma mb pa pb H) :
    nativeGK4BJStructuralAHFunctor p ma mb pa pb ⋙
      nativeGK4BKFactorFunctor p ma mb pa pb H h = H := by
  fapply CategoryTheory.Functor.ext
  · intro X
    rfl
  · intro X Y f
    simpa only [eqToHom_refl, Category.id_comp, Category.comp_id] using
      nativeGK4BKFactor_map p ma mb pa pb H h X Y f

/-- The converse: ANY categorical factorization through the
actually attained AH image must respect the true original
structural AH observation kernel. -/
theorem nativeGK4BKKernelNecessary
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (H : NativeGK4IStage p ma mb pa pb ⥤ T)
    (G : NativeGK4BFAttainedAHStage p ma mb pa pb ⥤ T)
    (hg : nativeGK4BJStructuralAHFunctor p ma mb pa pb ⋙ G = H) :
    nativeGK4BKAHKernelCompatible p ma mb pa pb H := by
  intro X Y f g hAH
  have hfg : (nativeGK4BJStructuralAHFunctor p ma mb pa pb).map f =
      (nativeGK4BJStructuralAHFunctor p ma mb pa pb).map g :=
    (nativeGK4BJStructuralAH_eq_iff p ma mb pa pb X Y f g).2 hAH
  have hgg := congrArg
    (fun z => G.map z) hfg
  have hcomp :
      (nativeGK4BJStructuralAHFunctor p ma mb pa pb ⋙ G).map f =
        (nativeGK4BJStructuralAHFunctor p ma mb pa pb ⋙ G).map g := by
    exact hgg
  simpa only [hg] using hcomp

/-- Exact existence criterion: compatibility with the genuine
original S-side AH observation kernel is both NECESSARY and SUFFICIENT
for a target functor to descend through the genuinely reached
AH matrix category. -/
theorem nativeGK4BKFactor_exists_iff
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (H : NativeGK4IStage p ma mb pa pb ⥤ T) :
    (∃ G : NativeGK4BFAttainedAHStage p ma mb pa pb ⥤ T,
      nativeGK4BJStructuralAHFunctor p ma mb pa pb ⋙ G = H) ↔
      nativeGK4BKAHKernelCompatible p ma mb pa pb H := by
  constructor
  · rintro ⟨G, hG⟩
    exact nativeGK4BKKernelNecessary p ma mb pa pb H G hG
  · intro h
    exact ⟨nativeGK4BKFactorFunctor p ma mb pa pb H h,
      nativeGK4BKFactor_functor p ma mb pa pb H h⟩

/-- Uniqueness of the actual Mathlib factor functor, not just
of its value on a representative source morphism. The proof
uses verified SURJECTIVITY on ORIGINAL objects and all Homs,
rather than introducing a new raw path inverse. -/
theorem nativeGK4BKFactor_unique
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (H : NativeGK4IStage p ma mb pa pb ⥤ T)
    (h : nativeGK4BKAHKernelCompatible p ma mb pa pb H)
    (G : NativeGK4BFAttainedAHStage p ma mb pa pb ⥤ T)
    (hg : nativeGK4BJStructuralAHFunctor p ma mb pa pb ⋙ G = H) :
    G = nativeGK4BKFactorFunctor p ma mb pa pb H h := by
  have hfun :
      nativeGK4BJStructuralAHFunctor p ma mb pa pb ⋙ G =
        nativeGK4BJStructuralAHFunctor p ma mb pa pb ⋙
          nativeGK4BKFactorFunctor p ma mb pa pb H h :=
    hg.trans (nativeGK4BKFactor_functor p ma mb pa pb H h).symm
  fapply CategoryTheory.Functor.ext
  · intro X
    cases X with
    | mk original =>
      exact Functor.congr_obj hfun original
  · intro X Y f
    cases X with
    | mk x =>
      cases Y with
      | mk y =>
        obtain ⟨s, hs⟩ :=
          nativeGK4BJStructuralAH_surjective_hom p ma mb pa pb x y f
        change (nativeGK4BJStructuralAHFunctor p ma mb pa pb).map s = f at hs
        subst f
        exact Functor.congr_hom hfun s

/-- Exact UNIVERSAL PROPERTY, expressed as unique existence
of a genuine factor functor at every target category. -/
theorem nativeGK4BKFactor_existsUnique
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (H : NativeGK4IStage p ma mb pa pb ⥤ T)
    (h : nativeGK4BKAHKernelCompatible p ma mb pa pb H) :
    ∃! G : NativeGK4BFAttainedAHStage p ma mb pa pb ⥤ T,
      nativeGK4BJStructuralAHFunctor p ma mb pa pb ⋙ G = H := by
  refine ⟨nativeGK4BKFactorFunctor p ma mb pa pb H h,
    nativeGK4BKFactor_functor p ma mb pa pb H h, ?_⟩
  intro G hg
  exact nativeGK4BKFactor_unique p ma mb pa pb H h G hg

end GenuineAHUniversalFactorization

#print axioms nativeGK4BKAHKernelCompatible
#print axioms nativeGK4BKCompatible_iff_imageKernel
#print axioms nativeGK4BKPreimage
#print axioms nativeGK4BKPreimage_spec
#print axioms nativeGK4BKLiftHom
#print axioms nativeGK4BKLiftHom_independent
#print axioms nativeGK4BKLiftHom_on_source
#print axioms nativeGK4BKFactorFunctor
#print axioms nativeGK4BKFactor_map
#print axioms nativeGK4BKFactor_functor
#print axioms nativeGK4BKKernelNecessary
#print axioms nativeGK4BKFactor_exists_iff
#print axioms nativeGK4BKFactor_unique
#print axioms nativeGK4BKFactor_existsUnique

end
end Kuu.F112.Physical
