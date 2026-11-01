import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4BMCompatibleFunctorCategoryEquivalence
import Mathlib.CategoryTheory.Whiskering
import Mathlib.Tactic

/-!
F112-P94D3GK4BN — the exact target-category postcomposition
naturality of genuine AH observation-kernel descent.

GK4BJ: an actual source-derived fully typed original F45
structural category S -> genuinely attained old AH category A.
GK4BK: precisely AH-kernel-compatible functors S -> T admit a
unique genuine factor through A.
GK4BL: natural transformations descend, giving fully faithful
precomposition for arbitrary target T.
GK4BM: true Mathlib category equivalence
  (A ⥤ T) ≌ FullSubcategory (AH-compatible S ⥤ T).

GK4BN now takes ANY genuine target functor R : T ⥤ U and
proves that the original AH-kernel compatibility is preserved by
R-postcomposition, and that the two honest functor categories
and the genuine compatible full subcategories have an exact
commutative square of Mathlib functors. We also construct and
check target natural-transformation action; its naturality and
composition are pinned Mathlib whiskering and genuine
original Hom comparisons, NOT invented Type-valued 3-cells.

Do NOT infer raw original F54 equality, original Q category laws,
unconditional S faithfulness, unattained integer matrices,
global strict higher coherence or hyperdescent.
Strict 空 center, independent Kuu one presentation, no Gray.
Append-only / tighten-only / overwrite-forbidden / same-root107.
Lean v4.30.0-rc2, pinned mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Validation-only #1558 Draft/OPEN/unmerged.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section
universe uD vD uE vE uT vT uU vU uV vV

section ExactTargetPostcomposition
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {T : Type uT} [Category.{vT} T]
variable {U : Type uU} [Category.{vU} U]
variable {V : Type uV} [Category.{vV} V]

/-- The exact original S-side old-AH kernel is stable under
POSTCOMPOSITION BY ANY target-category functor, regardless of
whether that target functor is faithful. -/
theorem nativeGK4BNCompatible_postcompose
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (H : NativeGK4IStage p ma mb pa pb ⥤ T)
    (hH : nativeGK4BKAHKernelCompatible p ma mb pa pb H)
    (R : T ⥤ U) :
    nativeGK4BKAHKernelCompatible p ma mb pa pb (H ⋙ R) := by
  intro X Y f g h
  exact congrArg (fun w : H.obj X ⟶ H.obj Y => R.map w) (hH X Y f g h)

/-- The pinned Mathlib target postcomposition acting on functors
out of the ACTUALLY attained AH matrix category. -/
def nativeGK4BNPostcompAttained
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (R : T ⥤ U) :
    (NativeGK4BFAttainedAHStage p ma mb pa pb ⥤ T) ⥤
      (NativeGK4BFAttainedAHStage p ma mb pa pb ⥤ U) :=
  (Functor.whiskeringRight _ _ _).obj R

/-- The pinned Mathlib target postcomposition acting on ALL
real original F45 structural-source functors, not a quotient
category or a synthetic path action. -/
def nativeGK4BNPostcompStructural
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (R : T ⥤ U) :
    (NativeGK4IStage p ma mb pa pb ⥤ T) ⥤
      (NativeGK4IStage p ma mb pa pb ⥤ U) :=
  (Functor.whiskeringRight _ _ _).obj R

/-- A TRUE functor from the compatible full subcategory for T
to the compatible full subcategory for U, assembled via the
existing Mathlib FullSubcategory inclusion and lift. -/
def nativeGK4BNPostcompCompatible
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (R : T ⥤ U) :
    NativeGK4BMCompatibleFunctorCategory (T := T) p ma mb pa pb ⥤
      NativeGK4BMCompatibleFunctorCategory (T := U) p ma mb pa pb :=
  ObjectProperty.lift
    (nativeGK4BMCompatibleProperty (T := U) p ma mb pa pb)
    (nativeGK4BMCompatibleInclusion (T := T) p ma mb pa pb ⋙
      nativeGK4BNPostcompStructural p ma mb pa pb R)
    (by
      intro H
      exact nativeGK4BNCompatible_postcompose
        p ma mb pa pb H.obj H.property R)

/-- The target-category change keeps the exact genuine
structural underlying functor: H.obj ⋙ R, not a new source
presentation or a new original P92B quotient. -/
@[simp] theorem nativeGK4BNPostcompCompatible_obj
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (R : T ⥤ U)
    (H : NativeGK4BMCompatibleFunctorCategory (T := T) p ma mb pa pb) :
    ((nativeGK4BNPostcompCompatible p ma mb pa pb R).obj H).obj =
      H.obj ⋙ R := rfl

/-- The true Hom action in the compatible full subcategory is
Mathlib right-whiskering of an ACTUAL natural transformation. -/
@[simp] theorem nativeGK4BNPostcompCompatible_map
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (R : T ⥤ U)
    (H K : NativeGK4BMCompatibleFunctorCategory (T := T) p ma mb pa pb)
    (η : H ⟶ K) :
    ((nativeGK4BNPostcompCompatible p ma mb pa pb R).map η).hom =
      Functor.whiskerRight η.hom R := rfl

/-- Inclusion from the compatible full subcategory and target
postcomposition commute as EXACT Mathlib functors. -/
theorem nativeGK4BNPostcomp_inclusion
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (R : T ⥤ U) :
    nativeGK4BNPostcompCompatible p ma mb pa pb R ⋙
      nativeGK4BMCompatibleInclusion (T := U) p ma mb pa pb =
    nativeGK4BMCompatibleInclusion (T := T) p ma mb pa pb ⋙
      nativeGK4BNPostcompStructural p ma mb pa pb R := rfl

/-- MAIN GK4BN STRICT SQUARE. For ANY true target functor R,
the GK4BM comparison after target postcomposition equals the
genuine compatible full-subcategory postcomposition after GK4BM
comparison. This is equality of WHOLE Mathlib Functors, including
all object maps and all natural transformation maps. -/
theorem nativeGK4BNPostcomp_precomposition_square
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (R : T ⥤ U) :
    nativeGK4BNPostcompAttained p ma mb pa pb R ⋙
      nativeGK4BMPrecompositionLift (T := U) p ma mb pa pb =
    nativeGK4BMPrecompositionLift (T := T) p ma mb pa pb ⋙
      nativeGK4BNPostcompCompatible p ma mb pa pb R := by
  apply CategoryTheory.Functor.toPrefunctor_injective
  refine Prefunctor.ext (fun G => rfl) ?_
  intro G H η
  rfl

/-- At an arbitrary ACTUALLY attained AH functor object the
strict square retains the same original fully typed
structural observation and genuine target R. -/
theorem nativeGK4BNPostcomp_precomposition_obj
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (R : T ⥤ U)
    (G : NativeGK4BFAttainedAHStage p ma mb pa pb ⥤ T) :
    ((nativeGK4BNPostcompAttained p ma mb pa pb R ⋙
      nativeGK4BMPrecompositionLift (T := U) p ma mb pa pb).obj G).obj =
        nativeGK4BJStructuralAHFunctor p ma mb pa pb ⋙ (G ⋙ R) := rfl

/-- Arbitrary target postcomposition commutes STRICTLY with
the concrete original GK4BK chosen Hom inverse and factor
Functor, not merely up to a guessed pseudo-natural isomorphism. -/
theorem nativeGK4BNFactorFunctor_postcompose
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (H : NativeGK4IStage p ma mb pa pb ⥤ T)
    (hH : nativeGK4BKAHKernelCompatible p ma mb pa pb H)
    (R : T ⥤ U) :
    nativeGK4BKFactorFunctor p ma mb pa pb (H ⋙ R)
      (nativeGK4BNCompatible_postcompose p ma mb pa pb H hH R) =
    nativeGK4BKFactorFunctor p ma mb pa pb H hH ⋙ R := rfl

/-- Target natural transformation rho induces an ACTUAL natural
transformation between the genuinely compatible postcomposition
functors. Naturality is the exact pinned Mathlib
whiskerLeft_comp_whiskerRight interchange. -/
def nativeGK4BNPostcompCompatibleNat
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    {R R' : T ⥤ U}
    (ρ : R ⟶ R') :
    nativeGK4BNPostcompCompatible p ma mb pa pb R ⟶
      nativeGK4BNPostcompCompatible p ma mb pa pb R' where
  app H := ObjectProperty.homMk (Functor.whiskerLeft H.obj ρ)
  naturality := by
    intro H K η
    apply ObjectProperty.hom_ext
    change Functor.whiskerRight η.hom R ≫ Functor.whiskerLeft K.obj ρ =
      Functor.whiskerLeft H.obj ρ ≫ Functor.whiskerRight η.hom R'
    exact (Functor.whiskerLeft_comp_whiskerRight η.hom ρ).symm

/-- The compatible target naturality has the original
H.obj stage value as its actual natural transformation. -/
@[simp] theorem nativeGK4BNPostcompCompatibleNat_app
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    {R R' : T ⥤ U}
    (ρ : R ⟶ R')
    (H : NativeGK4BMCompatibleFunctorCategory (T := T) p ma mb pa pb) :
    (nativeGK4BNPostcompCompatibleNat p ma mb pa pb ρ).app H =
      ObjectProperty.homMk (Functor.whiskerLeft H.obj ρ) := rfl

/-- The target postcomposition action on a genuine attained-AH
functor category is precisely Mathlib's whiskeringRight
natural transformation on target functors. -/
def nativeGK4BNPostcompAttainedNat
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    {R R' : T ⥤ U}
    (ρ : R ⟶ R') :
    nativeGK4BNPostcompAttained p ma mb pa pb R ⟶
      nativeGK4BNPostcompAttained p ma mb pa pb R' :=
  (Functor.whiskeringRight _ _ _).map ρ

/-- Target natural transformations are compatible with the
GK4BM exact square on each ACTUAL attained AH functor object:
both sides are the same original source F45 natural component
postcomposed by rho. -/
theorem nativeGK4BNPostcomp_nat_square_app
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    {R R' : T ⥤ U}
    (ρ : R ⟶ R')
    (G : NativeGK4BFAttainedAHStage p ma mb pa pb ⥤ T) :
    ((nativeGK4BNPostcompCompatibleNat p ma mb pa pb ρ).app
      ((nativeGK4BMPrecompositionLift (T := T) p ma mb pa pb).obj G)).hom =
    (nativeGK4BMPrecompositionLift (T := U) p ma mb pa pb).map
      ((nativeGK4BNPostcompAttainedNat p ma mb pa pb ρ).app G) := rfl

/-- The same target-category naturality holds as an equality
of whole NATURAL TRANSFORMATIONS between precomposed functors,
not only as componentwise statements. -/
theorem nativeGK4BNPostcomp_nat_square
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    {R R' : T ⥤ U}
    (ρ : R ⟶ R') :
    Functor.whiskerLeft
      (nativeGK4BMPrecompositionLift (T := T) p ma mb pa pb)
      (nativeGK4BNPostcompCompatibleNat p ma mb pa pb ρ) =
    Functor.whiskerRight
      (nativeGK4BNPostcompAttainedNat p ma mb pa pb ρ)
      (nativeGK4BMPrecompositionLift (T := U) p ma mb pa pb) := by
  ext G
  rfl

/-- The natural-transformation lift from genuine structural
data into the attained AH category commutes STRICTLY with
the target functor R. This is a real naturality preservation
fact about GK4BL's explicit lift, not a raw-F54 inverse. -/
theorem nativeGK4BNNatTransLift_postcompose
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (G H : NativeGK4BFAttainedAHStage p ma mb pa pb ⥤ T)
    (η : nativeGK4BJStructuralAHFunctor p ma mb pa pb ⋙ G ⟶
      nativeGK4BJStructuralAHFunctor p ma mb pa pb ⋙ H)
    (R : T ⥤ U) :
    nativeGK4BLNatTransLift p ma mb pa pb (G ⋙ R) (H ⋙ R)
      (Functor.whiskerRight η R) =
    Functor.whiskerRight
      (nativeGK4BLNatTransLift p ma mb pa pb G H η) R := by
  ext X
  rfl

/-- In the genuine compatible functor category, target identity
preserves each object and genuine natural-transformation arrow
without changing the original F45 source context. -/
theorem nativeGK4BNPostcompCompatible_id
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :
    nativeGK4BNPostcompCompatible p ma mb pa pb (𝟭 T) =
      𝟭 (NativeGK4BMCompatibleFunctorCategory (T := T) p ma mb pa pb) := by
  apply CategoryTheory.Functor.toPrefunctor_injective
  refine Prefunctor.ext (fun H => rfl) ?_
  intro H K η
  rfl

/-- Postcomposition in the compatible full subcategories obeys
the strict two-target composition law, not merely some unproved
higher coherence. The order is T --R--> U --Q--> V. -/
theorem nativeGK4BNPostcompCompatible_comp
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (R : T ⥤ U) (Q : U ⥤ V) :
    nativeGK4BNPostcompCompatible p ma mb pa pb (R ⋙ Q) =
      nativeGK4BNPostcompCompatible p ma mb pa pb R ⋙
        nativeGK4BNPostcompCompatible p ma mb pa pb Q := by
  apply CategoryTheory.Functor.toPrefunctor_injective
  refine Prefunctor.ext (fun H => rfl) ?_
  intro H K η
  rfl

end ExactTargetPostcomposition

#print axioms nativeGK4BNCompatible_postcompose
#print axioms nativeGK4BNPostcompAttained
#print axioms nativeGK4BNPostcompStructural
#print axioms nativeGK4BNPostcompCompatible
#print axioms nativeGK4BNPostcompCompatible_obj
#print axioms nativeGK4BNPostcompCompatible_map
#print axioms nativeGK4BNPostcomp_inclusion
#print axioms nativeGK4BNPostcomp_precomposition_square
#print axioms nativeGK4BNPostcomp_precomposition_obj
#print axioms nativeGK4BNFactorFunctor_postcompose
#print axioms nativeGK4BNPostcompCompatibleNat
#print axioms nativeGK4BNPostcompCompatibleNat_app
#print axioms nativeGK4BNPostcompAttainedNat
#print axioms nativeGK4BNPostcomp_nat_square_app
#print axioms nativeGK4BNPostcomp_nat_square
#print axioms nativeGK4BNNatTransLift_postcompose
#print axioms nativeGK4BNPostcompCompatible_id
#print axioms nativeGK4BNPostcompCompatible_comp

end
end Kuu.F112.Physical
