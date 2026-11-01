import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4BIAttainedAHCategoryEquivalence
import Mathlib.CategoryTheory.Equivalence
import Mathlib.Tactic

/-!
F112-P94D3GK4BJ — the original independent structural category S
maps FULLY and OBJECT-SURJECTIVELY to the ACTUALLY attained old-AH
matrix category, with exact kernel = equality of the original true
AH evaluation of structural route classes.

GK4AI: S -> K_AI is an ACTUAL Mathlib functor, surjective on each
genuine original dependent Hom. GK4BI: K_AI ≌ attained old AH,
with a genuine full/faithful and object-surjective forward functor.
Here we compose these actual source functors, identify the exact
original AH observation kernel and classify the remaining obstruction:
whether S itself is faithful into that observation quotient.

No unconditional S faithfulness, no original Q category laws,
no original unquotiented F54 route equality and no identification
with ALL integer matrices. Original F45 types and all original
source witnesses retained; no fake 3-cells, Gray or hyperdescent.
Append-only / tighten-only / same-root107.
Lean v4.30.0-rc2; mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6;
protected validation-only PR #1558 Draft/OPEN/unmerged.
Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section
universe uD vD uE vE

section OriginalStructuralAHDescent
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}

/-- The genuine original structural quotient S maps to EXACTLY the
already attained AH-image category, through the EXISTING K_AI
comparison and the GK4BI equivalence's actual forward functor. -/
def nativeGK4BJStructuralAHFunctor
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :
    NativeGK4IStage p ma mb pa pb ⥤
      NativeGK4BFAttainedAHStage p ma mb pa pb :=
  nativeGK4AIComparisonFunctor p ma mb pa pb ⋙
    nativeGK4BFImageFunctor p ma mb pa pb

/-- The actual composite lands on the same original full dependent
F45 stage; this is not a mapping to a one-object ambient category. -/
@[simp] theorem nativeGK4BJStructuralAH_obj
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (X : NativeGK4IStage p ma mb pa pb) :
    (nativeGK4BJStructuralAHFunctor p ma mb pa pb).obj X =
      ⟨X⟩ := rfl

/-- The actual attained-image Hom equality is exactly the original
S-class old-AH matrix equality, by GK4AI comparison and original
structurally sound AH observation. -/
theorem nativeGK4BJStructuralAH_value
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (X Y : NativeGK4IStage p ma mb pa pb)
    (f : X ⟶ Y) :
    ((nativeGK4BJStructuralAHFunctor p ma mb pa pb).map f).val =
      nativeGK4AHStructuralValue X.2.2 Y.2.2 f := by
  change (nativeGK4AIKernelValue X.2.2 Y.2.2
    (nativeGK4AIComparison X.2.2 Y.2.2 f)).2 =
      nativeGK4AHStructuralValue X.2.2 Y.2.2 f
  exact congrArg (fun z : NativeGK4AIValue => z.2)
    (nativeGK4AIComparison_value X.2.2 Y.2.2 f)

/-- Literal surjectivity on objects follows from the SAME
independent original dependent F45-stage wrapper; no abstract
essential-surjectivity witness needs to be invented. -/
theorem nativeGK4BJStructuralAH_surjective_obj
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :
    Function.Surjective
      (nativeGK4BJStructuralAHFunctor p ma mb pa pb).obj := by
  intro Y
  refine ⟨Y.original, ?_⟩
  cases Y
  rfl

/-- Every actually attained AH matrix on any dependent source-target
Hom has a TRUE independent S-class preimage. This combines the TWO
existing exact source-Hom surjectivity theorems without selecting any
new original F54 witness. -/
theorem nativeGK4BJStructuralAH_surjective_hom
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (X Y : NativeGK4IStage p ma mb pa pb) :
    Function.Surjective
      (fun f : X ⟶ Y =>
        (nativeGK4BJStructuralAHFunctor p ma mb pa pb).map f) := by
  intro z
  obtain ⟨q, hq⟩ := nativeGK4BFImageFunctor_surjective_hom
    p ma mb pa pb (⟨X⟩ : NativeGK4AIKernelStage p ma mb pa pb)
      (⟨Y⟩ : NativeGK4AIKernelStage p ma mb pa pb) z
  obtain ⟨s, hs⟩ :=
    nativeGK4AIComparisonFunctor_surjective_hom
      p ma mb pa pb X Y q
  refine ⟨s, ?_⟩
  change (nativeGK4BFImageFunctor p ma mb pa pb).map
      ((nativeGK4AIComparisonFunctor p ma mb pa pb).map s) = z
  change (nativeGK4AIComparisonFunctor p ma mb pa pb).map s = q at hs
  rw [hs]
  exact hq

/-- Explicit Mathlib FULL property, not merely a slogan:
every actual reached AH Hom has a genuine S-class preimage. -/
@[implicit_reducible] noncomputable def nativeGK4BJStructuralAH_full
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :
    (nativeGK4BJStructuralAHFunctor p ma mb pa pb).Full where
  map_surjective := by
    intro X Y
    exact nativeGK4BJStructuralAH_surjective_hom
      p ma mb pa pb X Y

/-- The same genuine object surjectivity supplies essential
surjectivity in pinned Mathlib's actual categorical sense. -/
@[implicit_reducible] noncomputable def nativeGK4BJStructuralAH_essSurj
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :
    (nativeGK4BJStructuralAHFunctor p ma mb pa pb).EssSurj :=
  Functor.essSurj_of_surj
    (nativeGK4BJStructuralAH_surjective_obj p ma mb pa pb)

/-- EXACT remaining equality kernel at fixed original dependent
F45 endpoints: structural arrow images agree if and only if their
TRUE old AH matrices agree. No claim that S arrows themselves agree. -/
theorem nativeGK4BJStructuralAH_eq_iff
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (X Y : NativeGK4IStage p ma mb pa pb)
    (f g : X ⟶ Y) :
    (nativeGK4BJStructuralAHFunctor p ma mb pa pb).map f =
        (nativeGK4BJStructuralAHFunctor p ma mb pa pb).map g ↔
      nativeGK4AHStructuralValue X.2.2 Y.2.2 f =
        nativeGK4AHStructuralValue X.2.2 Y.2.2 g := by
  constructor
  · intro h
    calc
      nativeGK4AHStructuralValue X.2.2 Y.2.2 f =
          ((nativeGK4BJStructuralAHFunctor p ma mb pa pb).map f).val :=
        (nativeGK4BJStructuralAH_value p ma mb pa pb X Y f).symm
      _ = ((nativeGK4BJStructuralAHFunctor p ma mb pa pb).map g).val :=
        congrArg Subtype.val h
      _ = nativeGK4AHStructuralValue X.2.2 Y.2.2 g :=
        nativeGK4BJStructuralAH_value p ma mb pa pb X Y g
  · intro h
    apply Subtype.ext
    calc
      ((nativeGK4BJStructuralAHFunctor p ma mb pa pb).map f).val =
          nativeGK4AHStructuralValue X.2.2 Y.2.2 f :=
        nativeGK4BJStructuralAH_value p ma mb pa pb X Y f
      _ = nativeGK4AHStructuralValue X.2.2 Y.2.2 g := h
      _ = ((nativeGK4BJStructuralAHFunctor p ma mb pa pb).map g).val :=
        (nativeGK4BJStructuralAH_value p ma mb pa pb X Y g).symm

/-- Thus any remaining lack of local faithfulness of S -> attained AH
is EXACTLY the noninjectivity of the TRUE original structural AH
observer (not a supposed failure of K_AI -> AH). -/
theorem nativeGK4BJStructuralAH_injective_iff
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (X Y : NativeGK4IStage p ma mb pa pb) :
    Function.Injective
      (fun f : X ⟶ Y =>
        (nativeGK4BJStructuralAHFunctor p ma mb pa pb).map f) ↔
      Function.Injective
        (nativeGK4AHStructuralValue X.2.2 Y.2.2) := by
  constructor
  · intro hinj f g h
    exact hinj ((nativeGK4BJStructuralAH_eq_iff
      p ma mb pa pb X Y f g).2 h)
  · intro hinj f g h
    exact hinj ((nativeGK4BJStructuralAH_eq_iff
      p ma mb pa pb X Y f g).1 h)

/-- The exact categorical OBSTRUCTION: the independent structural
S -> actually attained AH comparison is an equivalence if and only
if its original S-side AH observer is injective on EVERY source Hom.
Fullness and essential surjectivity are already PROVED unconditionally.
This iff is NOT an assertion that its right-hand side holds. -/
theorem nativeGK4BJStructuralAH_isEquivalence_iff
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :
    (nativeGK4BJStructuralAHFunctor p ma mb pa pb).IsEquivalence ↔
      (∀ X Y : NativeGK4IStage p ma mb pa pb,
        Function.Injective
          (nativeGK4AHStructuralValue X.2.2 Y.2.2)) := by
  constructor
  · intro heq X Y
    letI : (nativeGK4BJStructuralAHFunctor p ma mb pa pb).IsEquivalence := heq
    exact (nativeGK4BJStructuralAH_injective_iff
      p ma mb pa pb X Y).1
        (nativeGK4BJStructuralAHFunctor p ma mb pa pb).map_injective
  · intro h
    refine {
      faithful := ?_
      full := nativeGK4BJStructuralAH_full p ma mb pa pb
      essSurj := nativeGK4BJStructuralAH_essSurj p ma mb pa pb }
    refine ⟨?_⟩
    intro X Y f g heq
    exact (nativeGK4BJStructuralAH_injective_iff
      p ma mb pa pb X Y).2 (h X Y) heq

end OriginalStructuralAHDescent

#print axioms nativeGK4BJStructuralAHFunctor
#print axioms nativeGK4BJStructuralAH_obj
#print axioms nativeGK4BJStructuralAH_value
#print axioms nativeGK4BJStructuralAH_surjective_obj
#print axioms nativeGK4BJStructuralAH_surjective_hom
#print axioms nativeGK4BJStructuralAH_full
#print axioms nativeGK4BJStructuralAH_essSurj
#print axioms nativeGK4BJStructuralAH_eq_iff
#print axioms nativeGK4BJStructuralAH_injective_iff
#print axioms nativeGK4BJStructuralAH_isEquivalence_iff

end
end Kuu.F112.Physical
