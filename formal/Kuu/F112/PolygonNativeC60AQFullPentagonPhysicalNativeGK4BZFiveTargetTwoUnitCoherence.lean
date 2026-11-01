import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4BYChosenInverseUnitInsertionPentagonInverse
import Mathlib.CategoryTheory.Functor.Category
import Mathlib.CategoryTheory.Whiskering
import Mathlib.Tactic

/-!
F112-P94D3GK4BZ — all 14 ACTUAL five-target associhedron vertices
and two independent target-unit removal orders, with typed Mathlib
NatIso and whole target-NatTrans comparison.

GK4BM's chosen inverse Q is not definitionally GK4BP's P.
All results remain within existing Mathlib functor categories over
the original F45-typed structural source and actually attained AH
image with the GK4BM genuine compatible FullSubcategory.

Real binary pasting: GK4BW, exact two-target coherence: GK4BV,
three/four target pentagon: GK4BW, target modification: GK4BU,
one-unit pentagon and true inverse unitors: GK4BY.
Five-stage 14 paths and two independently removed units are new;
no raw F54/F55/P92B higher Type-valued cells, unconditional original
source faithfulness, global Gray, arbitrary matrix reachability,
or unrestricted higher hyperdescent follow.
Strict 空 center; independent Kuu one presentation.
Append-only / tighten-only / overwrite-forbidden / same-root107.
Lean v4.30.0-rc2, pinned mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Validation-only #1558 stays Draft/OPEN/unmerged.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section
universe uD vD uE vE uT vT uU vU uV vV uW vW uX vX uY vY

section FiveTargetFourteenVertices
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {T : Type uT} [Category.{vT} T]
variable {U : Type uU} [Category.{vU} U]
variable {V : Type uV} [Category.{vV} V]
variable {W : Type uW} [Category.{vW} W]
variable {X : Type uX} [Category.{vX} X]
variable {Y : Type uY} [Category.{vY} Y]

/-- Actual five-stage path 1A, with real GK4BV/GK4BW nested
Mathlib NatIso pastings; no assumed extra 3-cells. -/
noncomputable def nativeGK4BZChosenInverse_fivePath_1A
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (R : T ⥤ U) (S : U ⥤ V) (L : V ⥤ W)
    (M : W ⥤ X) (N : X ⥤ Y) :
    (nativeGK4BNPostcompCompatible p ma mb pa pb (R ⋙ S ⋙ L ⋙ M ⋙ N) ⋙
      nativeGK4BMCompatibleReverseFunctor (T := Y) p ma mb pa pb) ≅
    (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb ⋙
      nativeGK4BNPostcompAttained p ma mb pa pb (R ⋙ S ⋙ L ⋙ M ⋙ N)) :=
  nativeGK4BWChosenInverse_binaryPasting p ma mb pa pb R (S ⋙ L ⋙ M ⋙ N)
    (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb R) (nativeGK4BWChosenInverse_four_pathA p ma mb pa pb S L M N)

/-- Five-path 1A equals the direct whole chosen-inverse Θ. -/
theorem nativeGK4BZChosenInverse_fivePath_1A_eq_direct
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (R : T ⥤ U) (S : U ⥤ V) (L : V ⥤ W)
    (M : W ⥤ X) (N : X ⥤ Y) :
    nativeGK4BZChosenInverse_fivePath_1A p ma mb pa pb R S L M N =
      nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L ⋙ M ⋙ N) := by
  simp only [nativeGK4BZChosenInverse_fivePath_1A,
    nativeGK4BWChosenInverse_four_pathA_eq_direct,
    nativeGK4BWChosenInverse_binaryPasting_ofTheta,
    nativeGK4BVChosenInverse_composition_coherence]
  all_goals rfl

/-- Actual five-stage path 1B, with real GK4BV/GK4BW nested
Mathlib NatIso pastings; no assumed extra 3-cells. -/
noncomputable def nativeGK4BZChosenInverse_fivePath_1B
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (R : T ⥤ U) (S : U ⥤ V) (L : V ⥤ W)
    (M : W ⥤ X) (N : X ⥤ Y) :
    (nativeGK4BNPostcompCompatible p ma mb pa pb (R ⋙ S ⋙ L ⋙ M ⋙ N) ⋙
      nativeGK4BMCompatibleReverseFunctor (T := Y) p ma mb pa pb) ≅
    (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb ⋙
      nativeGK4BNPostcompAttained p ma mb pa pb (R ⋙ S ⋙ L ⋙ M ⋙ N)) :=
  nativeGK4BWChosenInverse_binaryPasting p ma mb pa pb R (S ⋙ L ⋙ M ⋙ N)
    (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb R) (nativeGK4BWChosenInverse_four_pathB p ma mb pa pb S L M N)

/-- Five-path 1B equals the direct whole chosen-inverse Θ. -/
theorem nativeGK4BZChosenInverse_fivePath_1B_eq_direct
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (R : T ⥤ U) (S : U ⥤ V) (L : V ⥤ W)
    (M : W ⥤ X) (N : X ⥤ Y) :
    nativeGK4BZChosenInverse_fivePath_1B p ma mb pa pb R S L M N =
      nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L ⋙ M ⋙ N) := by
  simp only [nativeGK4BZChosenInverse_fivePath_1B,
    nativeGK4BWChosenInverse_four_pathB_eq_direct,
    nativeGK4BWChosenInverse_binaryPasting_ofTheta,
    nativeGK4BVChosenInverse_composition_coherence]
  all_goals rfl

/-- Actual five-stage path 1C, with real GK4BV/GK4BW nested
Mathlib NatIso pastings; no assumed extra 3-cells. -/
noncomputable def nativeGK4BZChosenInverse_fivePath_1C
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (R : T ⥤ U) (S : U ⥤ V) (L : V ⥤ W)
    (M : W ⥤ X) (N : X ⥤ Y) :
    (nativeGK4BNPostcompCompatible p ma mb pa pb (R ⋙ S ⋙ L ⋙ M ⋙ N) ⋙
      nativeGK4BMCompatibleReverseFunctor (T := Y) p ma mb pa pb) ≅
    (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb ⋙
      nativeGK4BNPostcompAttained p ma mb pa pb (R ⋙ S ⋙ L ⋙ M ⋙ N)) :=
  nativeGK4BWChosenInverse_binaryPasting p ma mb pa pb R (S ⋙ L ⋙ M ⋙ N)
    (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb R) (nativeGK4BWChosenInverse_four_pathC p ma mb pa pb S L M N)

/-- Five-path 1C equals the direct whole chosen-inverse Θ. -/
theorem nativeGK4BZChosenInverse_fivePath_1C_eq_direct
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (R : T ⥤ U) (S : U ⥤ V) (L : V ⥤ W)
    (M : W ⥤ X) (N : X ⥤ Y) :
    nativeGK4BZChosenInverse_fivePath_1C p ma mb pa pb R S L M N =
      nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L ⋙ M ⋙ N) := by
  simp only [nativeGK4BZChosenInverse_fivePath_1C,
    nativeGK4BWChosenInverse_four_pathC_eq_direct,
    nativeGK4BWChosenInverse_binaryPasting_ofTheta,
    nativeGK4BVChosenInverse_composition_coherence]
  all_goals rfl

/-- Actual five-stage path 1D, with real GK4BV/GK4BW nested
Mathlib NatIso pastings; no assumed extra 3-cells. -/
noncomputable def nativeGK4BZChosenInverse_fivePath_1D
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (R : T ⥤ U) (S : U ⥤ V) (L : V ⥤ W)
    (M : W ⥤ X) (N : X ⥤ Y) :
    (nativeGK4BNPostcompCompatible p ma mb pa pb (R ⋙ S ⋙ L ⋙ M ⋙ N) ⋙
      nativeGK4BMCompatibleReverseFunctor (T := Y) p ma mb pa pb) ≅
    (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb ⋙
      nativeGK4BNPostcompAttained p ma mb pa pb (R ⋙ S ⋙ L ⋙ M ⋙ N)) :=
  nativeGK4BWChosenInverse_binaryPasting p ma mb pa pb R (S ⋙ L ⋙ M ⋙ N)
    (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb R) (nativeGK4BWChosenInverse_four_pathD p ma mb pa pb S L M N)

/-- Five-path 1D equals the direct whole chosen-inverse Θ. -/
theorem nativeGK4BZChosenInverse_fivePath_1D_eq_direct
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (R : T ⥤ U) (S : U ⥤ V) (L : V ⥤ W)
    (M : W ⥤ X) (N : X ⥤ Y) :
    nativeGK4BZChosenInverse_fivePath_1D p ma mb pa pb R S L M N =
      nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L ⋙ M ⋙ N) := by
  simp only [nativeGK4BZChosenInverse_fivePath_1D,
    nativeGK4BWChosenInverse_four_pathD_eq_direct,
    nativeGK4BWChosenInverse_binaryPasting_ofTheta,
    nativeGK4BVChosenInverse_composition_coherence]
  all_goals rfl

/-- Actual five-stage path 1E, with real GK4BV/GK4BW nested
Mathlib NatIso pastings; no assumed extra 3-cells. -/
noncomputable def nativeGK4BZChosenInverse_fivePath_1E
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (R : T ⥤ U) (S : U ⥤ V) (L : V ⥤ W)
    (M : W ⥤ X) (N : X ⥤ Y) :
    (nativeGK4BNPostcompCompatible p ma mb pa pb (R ⋙ S ⋙ L ⋙ M ⋙ N) ⋙
      nativeGK4BMCompatibleReverseFunctor (T := Y) p ma mb pa pb) ≅
    (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb ⋙
      nativeGK4BNPostcompAttained p ma mb pa pb (R ⋙ S ⋙ L ⋙ M ⋙ N)) :=
  nativeGK4BWChosenInverse_binaryPasting p ma mb pa pb R (S ⋙ L ⋙ M ⋙ N)
    (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb R) (nativeGK4BWChosenInverse_four_pathE p ma mb pa pb S L M N)

/-- Five-path 1E equals the direct whole chosen-inverse Θ. -/
theorem nativeGK4BZChosenInverse_fivePath_1E_eq_direct
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (R : T ⥤ U) (S : U ⥤ V) (L : V ⥤ W)
    (M : W ⥤ X) (N : X ⥤ Y) :
    nativeGK4BZChosenInverse_fivePath_1E p ma mb pa pb R S L M N =
      nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L ⋙ M ⋙ N) := by
  simp only [nativeGK4BZChosenInverse_fivePath_1E,
    nativeGK4BWChosenInverse_four_pathE_eq_direct,
    nativeGK4BWChosenInverse_binaryPasting_ofTheta,
    nativeGK4BVChosenInverse_composition_coherence]
  all_goals rfl

/-- Actual five-stage path 2Left, with real GK4BV/GK4BW nested
Mathlib NatIso pastings; no assumed extra 3-cells. -/
noncomputable def nativeGK4BZChosenInverse_fivePath_2Left
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (R : T ⥤ U) (S : U ⥤ V) (L : V ⥤ W)
    (M : W ⥤ X) (N : X ⥤ Y) :
    (nativeGK4BNPostcompCompatible p ma mb pa pb (R ⋙ S ⋙ L ⋙ M ⋙ N) ⋙
      nativeGK4BMCompatibleReverseFunctor (T := Y) p ma mb pa pb) ≅
    (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb ⋙
      nativeGK4BNPostcompAttained p ma mb pa pb (R ⋙ S ⋙ L ⋙ M ⋙ N)) :=
  nativeGK4BWChosenInverse_binaryPasting p ma mb pa pb (R ⋙ S) (L ⋙ M ⋙ N)
    (nativeGK4BVChosenInverse_twoTargetCompositeIso p ma mb pa pb R S) (nativeGK4BWChosenInverse_threeLeft p ma mb pa pb L M N)

/-- Five-path 2Left equals the direct whole chosen-inverse Θ. -/
theorem nativeGK4BZChosenInverse_fivePath_2Left_eq_direct
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (R : T ⥤ U) (S : U ⥤ V) (L : V ⥤ W)
    (M : W ⥤ X) (N : X ⥤ Y) :
    nativeGK4BZChosenInverse_fivePath_2Left p ma mb pa pb R S L M N =
      nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L ⋙ M ⋙ N) := by
  simp only [nativeGK4BZChosenInverse_fivePath_2Left,
    nativeGK4BVChosenInverse_composition_coherence,
    nativeGK4BWChosenInverse_threeLeft_eq_direct,
    nativeGK4BWChosenInverse_binaryPasting_ofTheta,
    nativeGK4BVChosenInverse_composition_coherence]
  all_goals rfl

/-- Actual five-stage path 2Right, with real GK4BV/GK4BW nested
Mathlib NatIso pastings; no assumed extra 3-cells. -/
noncomputable def nativeGK4BZChosenInverse_fivePath_2Right
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (R : T ⥤ U) (S : U ⥤ V) (L : V ⥤ W)
    (M : W ⥤ X) (N : X ⥤ Y) :
    (nativeGK4BNPostcompCompatible p ma mb pa pb (R ⋙ S ⋙ L ⋙ M ⋙ N) ⋙
      nativeGK4BMCompatibleReverseFunctor (T := Y) p ma mb pa pb) ≅
    (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb ⋙
      nativeGK4BNPostcompAttained p ma mb pa pb (R ⋙ S ⋙ L ⋙ M ⋙ N)) :=
  nativeGK4BWChosenInverse_binaryPasting p ma mb pa pb (R ⋙ S) (L ⋙ M ⋙ N)
    (nativeGK4BVChosenInverse_twoTargetCompositeIso p ma mb pa pb R S) (nativeGK4BWChosenInverse_threeRight p ma mb pa pb L M N)

/-- Five-path 2Right equals the direct whole chosen-inverse Θ. -/
theorem nativeGK4BZChosenInverse_fivePath_2Right_eq_direct
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (R : T ⥤ U) (S : U ⥤ V) (L : V ⥤ W)
    (M : W ⥤ X) (N : X ⥤ Y) :
    nativeGK4BZChosenInverse_fivePath_2Right p ma mb pa pb R S L M N =
      nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L ⋙ M ⋙ N) := by
  simp only [nativeGK4BZChosenInverse_fivePath_2Right,
    nativeGK4BVChosenInverse_composition_coherence,
    nativeGK4BWChosenInverse_threeRight_eq_direct,
    nativeGK4BWChosenInverse_binaryPasting_ofTheta,
    nativeGK4BVChosenInverse_composition_coherence]
  all_goals rfl

/-- Actual five-stage path 3Left, with real GK4BV/GK4BW nested
Mathlib NatIso pastings; no assumed extra 3-cells. -/
noncomputable def nativeGK4BZChosenInverse_fivePath_3Left
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (R : T ⥤ U) (S : U ⥤ V) (L : V ⥤ W)
    (M : W ⥤ X) (N : X ⥤ Y) :
    (nativeGK4BNPostcompCompatible p ma mb pa pb (R ⋙ S ⋙ L ⋙ M ⋙ N) ⋙
      nativeGK4BMCompatibleReverseFunctor (T := Y) p ma mb pa pb) ≅
    (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb ⋙
      nativeGK4BNPostcompAttained p ma mb pa pb (R ⋙ S ⋙ L ⋙ M ⋙ N)) :=
  nativeGK4BWChosenInverse_binaryPasting p ma mb pa pb (R ⋙ S ⋙ L) (M ⋙ N)
    (nativeGK4BWChosenInverse_threeLeft p ma mb pa pb R S L) (nativeGK4BVChosenInverse_twoTargetCompositeIso p ma mb pa pb M N)

/-- Five-path 3Left equals the direct whole chosen-inverse Θ. -/
theorem nativeGK4BZChosenInverse_fivePath_3Left_eq_direct
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (R : T ⥤ U) (S : U ⥤ V) (L : V ⥤ W)
    (M : W ⥤ X) (N : X ⥤ Y) :
    nativeGK4BZChosenInverse_fivePath_3Left p ma mb pa pb R S L M N =
      nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L ⋙ M ⋙ N) := by
  simp only [nativeGK4BZChosenInverse_fivePath_3Left,
    nativeGK4BWChosenInverse_threeLeft_eq_direct,
    nativeGK4BVChosenInverse_composition_coherence,
    nativeGK4BWChosenInverse_binaryPasting_ofTheta,
    nativeGK4BVChosenInverse_composition_coherence]
  all_goals rfl

/-- Actual five-stage path 3Right, with real GK4BV/GK4BW nested
Mathlib NatIso pastings; no assumed extra 3-cells. -/
noncomputable def nativeGK4BZChosenInverse_fivePath_3Right
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (R : T ⥤ U) (S : U ⥤ V) (L : V ⥤ W)
    (M : W ⥤ X) (N : X ⥤ Y) :
    (nativeGK4BNPostcompCompatible p ma mb pa pb (R ⋙ S ⋙ L ⋙ M ⋙ N) ⋙
      nativeGK4BMCompatibleReverseFunctor (T := Y) p ma mb pa pb) ≅
    (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb ⋙
      nativeGK4BNPostcompAttained p ma mb pa pb (R ⋙ S ⋙ L ⋙ M ⋙ N)) :=
  nativeGK4BWChosenInverse_binaryPasting p ma mb pa pb (R ⋙ S ⋙ L) (M ⋙ N)
    (nativeGK4BWChosenInverse_threeRight p ma mb pa pb R S L) (nativeGK4BVChosenInverse_twoTargetCompositeIso p ma mb pa pb M N)

/-- Five-path 3Right equals the direct whole chosen-inverse Θ. -/
theorem nativeGK4BZChosenInverse_fivePath_3Right_eq_direct
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (R : T ⥤ U) (S : U ⥤ V) (L : V ⥤ W)
    (M : W ⥤ X) (N : X ⥤ Y) :
    nativeGK4BZChosenInverse_fivePath_3Right p ma mb pa pb R S L M N =
      nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L ⋙ M ⋙ N) := by
  simp only [nativeGK4BZChosenInverse_fivePath_3Right,
    nativeGK4BWChosenInverse_threeRight_eq_direct,
    nativeGK4BVChosenInverse_composition_coherence,
    nativeGK4BWChosenInverse_binaryPasting_ofTheta,
    nativeGK4BVChosenInverse_composition_coherence]
  all_goals rfl

/-- Actual five-stage path 4A, with real GK4BV/GK4BW nested
Mathlib NatIso pastings; no assumed extra 3-cells. -/
noncomputable def nativeGK4BZChosenInverse_fivePath_4A
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (R : T ⥤ U) (S : U ⥤ V) (L : V ⥤ W)
    (M : W ⥤ X) (N : X ⥤ Y) :
    (nativeGK4BNPostcompCompatible p ma mb pa pb (R ⋙ S ⋙ L ⋙ M ⋙ N) ⋙
      nativeGK4BMCompatibleReverseFunctor (T := Y) p ma mb pa pb) ≅
    (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb ⋙
      nativeGK4BNPostcompAttained p ma mb pa pb (R ⋙ S ⋙ L ⋙ M ⋙ N)) :=
  nativeGK4BWChosenInverse_binaryPasting p ma mb pa pb (R ⋙ S ⋙ L ⋙ M) N
    (nativeGK4BWChosenInverse_four_pathA p ma mb pa pb R S L M) (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb N)

/-- Five-path 4A equals the direct whole chosen-inverse Θ. -/
theorem nativeGK4BZChosenInverse_fivePath_4A_eq_direct
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (R : T ⥤ U) (S : U ⥤ V) (L : V ⥤ W)
    (M : W ⥤ X) (N : X ⥤ Y) :
    nativeGK4BZChosenInverse_fivePath_4A p ma mb pa pb R S L M N =
      nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L ⋙ M ⋙ N) := by
  simp only [nativeGK4BZChosenInverse_fivePath_4A,
    nativeGK4BWChosenInverse_four_pathA_eq_direct,
    nativeGK4BWChosenInverse_binaryPasting_ofTheta,
    nativeGK4BVChosenInverse_composition_coherence]
  all_goals rfl

/-- Actual five-stage path 4B, with real GK4BV/GK4BW nested
Mathlib NatIso pastings; no assumed extra 3-cells. -/
noncomputable def nativeGK4BZChosenInverse_fivePath_4B
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (R : T ⥤ U) (S : U ⥤ V) (L : V ⥤ W)
    (M : W ⥤ X) (N : X ⥤ Y) :
    (nativeGK4BNPostcompCompatible p ma mb pa pb (R ⋙ S ⋙ L ⋙ M ⋙ N) ⋙
      nativeGK4BMCompatibleReverseFunctor (T := Y) p ma mb pa pb) ≅
    (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb ⋙
      nativeGK4BNPostcompAttained p ma mb pa pb (R ⋙ S ⋙ L ⋙ M ⋙ N)) :=
  nativeGK4BWChosenInverse_binaryPasting p ma mb pa pb (R ⋙ S ⋙ L ⋙ M) N
    (nativeGK4BWChosenInverse_four_pathB p ma mb pa pb R S L M) (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb N)

/-- Five-path 4B equals the direct whole chosen-inverse Θ. -/
theorem nativeGK4BZChosenInverse_fivePath_4B_eq_direct
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (R : T ⥤ U) (S : U ⥤ V) (L : V ⥤ W)
    (M : W ⥤ X) (N : X ⥤ Y) :
    nativeGK4BZChosenInverse_fivePath_4B p ma mb pa pb R S L M N =
      nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L ⋙ M ⋙ N) := by
  simp only [nativeGK4BZChosenInverse_fivePath_4B,
    nativeGK4BWChosenInverse_four_pathB_eq_direct,
    nativeGK4BWChosenInverse_binaryPasting_ofTheta,
    nativeGK4BVChosenInverse_composition_coherence]
  all_goals rfl

/-- Actual five-stage path 4C, with real GK4BV/GK4BW nested
Mathlib NatIso pastings; no assumed extra 3-cells. -/
noncomputable def nativeGK4BZChosenInverse_fivePath_4C
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (R : T ⥤ U) (S : U ⥤ V) (L : V ⥤ W)
    (M : W ⥤ X) (N : X ⥤ Y) :
    (nativeGK4BNPostcompCompatible p ma mb pa pb (R ⋙ S ⋙ L ⋙ M ⋙ N) ⋙
      nativeGK4BMCompatibleReverseFunctor (T := Y) p ma mb pa pb) ≅
    (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb ⋙
      nativeGK4BNPostcompAttained p ma mb pa pb (R ⋙ S ⋙ L ⋙ M ⋙ N)) :=
  nativeGK4BWChosenInverse_binaryPasting p ma mb pa pb (R ⋙ S ⋙ L ⋙ M) N
    (nativeGK4BWChosenInverse_four_pathC p ma mb pa pb R S L M) (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb N)

/-- Five-path 4C equals the direct whole chosen-inverse Θ. -/
theorem nativeGK4BZChosenInverse_fivePath_4C_eq_direct
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (R : T ⥤ U) (S : U ⥤ V) (L : V ⥤ W)
    (M : W ⥤ X) (N : X ⥤ Y) :
    nativeGK4BZChosenInverse_fivePath_4C p ma mb pa pb R S L M N =
      nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L ⋙ M ⋙ N) := by
  simp only [nativeGK4BZChosenInverse_fivePath_4C,
    nativeGK4BWChosenInverse_four_pathC_eq_direct,
    nativeGK4BWChosenInverse_binaryPasting_ofTheta,
    nativeGK4BVChosenInverse_composition_coherence]
  all_goals rfl

/-- Actual five-stage path 4D, with real GK4BV/GK4BW nested
Mathlib NatIso pastings; no assumed extra 3-cells. -/
noncomputable def nativeGK4BZChosenInverse_fivePath_4D
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (R : T ⥤ U) (S : U ⥤ V) (L : V ⥤ W)
    (M : W ⥤ X) (N : X ⥤ Y) :
    (nativeGK4BNPostcompCompatible p ma mb pa pb (R ⋙ S ⋙ L ⋙ M ⋙ N) ⋙
      nativeGK4BMCompatibleReverseFunctor (T := Y) p ma mb pa pb) ≅
    (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb ⋙
      nativeGK4BNPostcompAttained p ma mb pa pb (R ⋙ S ⋙ L ⋙ M ⋙ N)) :=
  nativeGK4BWChosenInverse_binaryPasting p ma mb pa pb (R ⋙ S ⋙ L ⋙ M) N
    (nativeGK4BWChosenInverse_four_pathD p ma mb pa pb R S L M) (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb N)

/-- Five-path 4D equals the direct whole chosen-inverse Θ. -/
theorem nativeGK4BZChosenInverse_fivePath_4D_eq_direct
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (R : T ⥤ U) (S : U ⥤ V) (L : V ⥤ W)
    (M : W ⥤ X) (N : X ⥤ Y) :
    nativeGK4BZChosenInverse_fivePath_4D p ma mb pa pb R S L M N =
      nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L ⋙ M ⋙ N) := by
  simp only [nativeGK4BZChosenInverse_fivePath_4D,
    nativeGK4BWChosenInverse_four_pathD_eq_direct,
    nativeGK4BWChosenInverse_binaryPasting_ofTheta,
    nativeGK4BVChosenInverse_composition_coherence]
  all_goals rfl

/-- Actual five-stage path 4E, with real GK4BV/GK4BW nested
Mathlib NatIso pastings; no assumed extra 3-cells. -/
noncomputable def nativeGK4BZChosenInverse_fivePath_4E
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (R : T ⥤ U) (S : U ⥤ V) (L : V ⥤ W)
    (M : W ⥤ X) (N : X ⥤ Y) :
    (nativeGK4BNPostcompCompatible p ma mb pa pb (R ⋙ S ⋙ L ⋙ M ⋙ N) ⋙
      nativeGK4BMCompatibleReverseFunctor (T := Y) p ma mb pa pb) ≅
    (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb ⋙
      nativeGK4BNPostcompAttained p ma mb pa pb (R ⋙ S ⋙ L ⋙ M ⋙ N)) :=
  nativeGK4BWChosenInverse_binaryPasting p ma mb pa pb (R ⋙ S ⋙ L ⋙ M) N
    (nativeGK4BWChosenInverse_four_pathE p ma mb pa pb R S L M) (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb N)

/-- Five-path 4E equals the direct whole chosen-inverse Θ. -/
theorem nativeGK4BZChosenInverse_fivePath_4E_eq_direct
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (R : T ⥤ U) (S : U ⥤ V) (L : V ⥤ W)
    (M : W ⥤ X) (N : X ⥤ Y) :
    nativeGK4BZChosenInverse_fivePath_4E p ma mb pa pb R S L M N =
      nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L ⋙ M ⋙ N) := by
  simp only [nativeGK4BZChosenInverse_fivePath_4E,
    nativeGK4BWChosenInverse_four_pathE_eq_direct,
    nativeGK4BWChosenInverse_binaryPasting_ofTheta,
    nativeGK4BVChosenInverse_composition_coherence]
  all_goals rfl

/-- Every Catalan vertex of the *actual five-stage*
associahedron is represented by a genuine Mathlib chosen-inverse
NatIso, not merely by a theoretical existence claim. -/
noncomputable def nativeGK4BZChosenInverse_fivePathIndexed
    (i : Fin 14)
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (R : T ⥤ U) (S : U ⥤ V) (L : V ⥤ W)
    (M : W ⥤ X) (N : X ⥤ Y) :
    (nativeGK4BNPostcompCompatible p ma mb pa pb (R ⋙ S ⋙ L ⋙ M ⋙ N) ⋙
      nativeGK4BMCompatibleReverseFunctor (T := Y) p ma mb pa pb) ≅
    (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb ⋙
      nativeGK4BNPostcompAttained p ma mb pa pb (R ⋙ S ⋙ L ⋙ M ⋙ N)) :=
  match i.val with
  | 0 => nativeGK4BZChosenInverse_fivePath_1A p ma mb pa pb R S L M N
  | 1 => nativeGK4BZChosenInverse_fivePath_1B p ma mb pa pb R S L M N
  | 2 => nativeGK4BZChosenInverse_fivePath_1C p ma mb pa pb R S L M N
  | 3 => nativeGK4BZChosenInverse_fivePath_1D p ma mb pa pb R S L M N
  | 4 => nativeGK4BZChosenInverse_fivePath_1E p ma mb pa pb R S L M N
  | 5 => nativeGK4BZChosenInverse_fivePath_2Left p ma mb pa pb R S L M N
  | 6 => nativeGK4BZChosenInverse_fivePath_2Right p ma mb pa pb R S L M N
  | 7 => nativeGK4BZChosenInverse_fivePath_3Left p ma mb pa pb R S L M N
  | 8 => nativeGK4BZChosenInverse_fivePath_3Right p ma mb pa pb R S L M N
  | 9 => nativeGK4BZChosenInverse_fivePath_4A p ma mb pa pb R S L M N
  | 10 => nativeGK4BZChosenInverse_fivePath_4B p ma mb pa pb R S L M N
  | 11 => nativeGK4BZChosenInverse_fivePath_4C p ma mb pa pb R S L M N
  | 12 => nativeGK4BZChosenInverse_fivePath_4D p ma mb pa pb R S L M N
  | _ => nativeGK4BZChosenInverse_fivePath_4E p ma mb pa pb R S L M N

/-- A UNIFORM whole NatIso coherence theorem for ALL 14 vertices.
No extra source axioms or inaccessible matrix objects are used. -/
theorem nativeGK4BZChosenInverse_fivePathIndexed_eq_direct
    (i : Fin 14)
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (R : T ⥤ U) (S : U ⥤ V) (L : V ⥤ W)
    (M : W ⥤ X) (N : X ⥤ Y) :
    nativeGK4BZChosenInverse_fivePathIndexed i p ma mb pa pb R S L M N =
      nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L ⋙ M ⋙ N) := by
  fin_cases i <;> simp [nativeGK4BZChosenInverse_fivePathIndexed,
    nativeGK4BZChosenInverse_fivePath_1A_eq_direct,
    nativeGK4BZChosenInverse_fivePath_1B_eq_direct,
    nativeGK4BZChosenInverse_fivePath_1C_eq_direct,
    nativeGK4BZChosenInverse_fivePath_1D_eq_direct,
    nativeGK4BZChosenInverse_fivePath_1E_eq_direct,
    nativeGK4BZChosenInverse_fivePath_2Left_eq_direct,
    nativeGK4BZChosenInverse_fivePath_2Right_eq_direct,
    nativeGK4BZChosenInverse_fivePath_3Left_eq_direct,
    nativeGK4BZChosenInverse_fivePath_3Right_eq_direct,
    nativeGK4BZChosenInverse_fivePath_4A_eq_direct,
    nativeGK4BZChosenInverse_fivePath_4B_eq_direct,
    nativeGK4BZChosenInverse_fivePath_4C_eq_direct,
    nativeGK4BZChosenInverse_fivePath_4D_eq_direct,
    nativeGK4BZChosenInverse_fivePath_4E_eq_direct]

/-- Uniform whole target-NatTrans modification for ANY of the
14 genuinely constructed five-target pentagon/associahedron paths,
under ANY true target natural transformation of the composite. -/
theorem nativeGK4BZChosenInverse_fivePathIndexed_targetNat_square
    (i : Fin 14) (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    {R R' : T ⥤ U} (ρ : R ⟶ R')
    (S : U ⥤ V) (L : V ⥤ W)
    (M : W ⥤ X) (N : X ⥤ Y) :
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (Functor.whiskerRight
            (Functor.whiskerRight
              (Functor.whiskerRight
                (Functor.whiskerRight ρ S) L) M) N))
        (nativeGK4BMCompatibleReverseFunctor (T := Y) p ma mb pa pb) ≫
      (nativeGK4BZChosenInverse_fivePathIndexed i p ma mb pa pb R' S L M N).hom =
    (nativeGK4BZChosenInverse_fivePathIndexed i p ma mb pa pb R S L M N).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (Functor.whiskerRight
            (Functor.whiskerRight
              (Functor.whiskerRight
                (Functor.whiskerRight ρ S) L) M) N)) := by
  simpa only [nativeGK4BZChosenInverse_fivePathIndexed_eq_direct] using
    (nativeGK4BUChosenInverse_targetNat_square p ma mb pa pb
      (Functor.whiskerRight
        (Functor.whiskerRight
          (Functor.whiskerRight
            (Functor.whiskerRight ρ S) L) M) N))

end FiveTargetFourteenVertices

section TwoIndependentUnits
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {T : Type uT} [Category.{vT} T]
variable {U : Type uU} [Category.{vU} U]
variable {V : Type uV} [Category.{vV} V]
variable {W : Type uW} [Category.{vW} W]

/-- Remove the first of TWO independently inserted target identities. -/
noncomputable def nativeGK4BZDoubleUnit_Afirst
    (R : T ⥤ U) (S : U ⥤ V) (L : V ⥤ W) :
    R ⋙ 𝟭 U ⋙ S ⋙ 𝟭 V ⋙ L ≅ R ⋙ S ⋙ 𝟭 V ⋙ L :=
  Functor.isoWhiskerRight (Functor.rightUnitor R) (S ⋙ 𝟭 V ⋙ L)

/-- Remove the remaining second target identity after the first. -/
noncomputable def nativeGK4BZDoubleUnit_Asecond
    (R : T ⥤ U) (S : U ⥤ V) (L : V ⥤ W) :
    R ⋙ S ⋙ 𝟭 V ⋙ L ≅ R ⋙ S ⋙ L :=
  nativeGK4BYTargetUnitIso_afterS R S L

/-- Independent removal order A: first gap U, then gap V. -/
noncomputable def nativeGK4BZDoubleUnit_orderA
    (R : T ⥤ U) (S : U ⥤ V) (L : V ⥤ W) :
    R ⋙ 𝟭 U ⋙ S ⋙ 𝟭 V ⋙ L ≅ R ⋙ S ⋙ L :=
  nativeGK4BZDoubleUnit_Afirst R S L ≪≫
    nativeGK4BZDoubleUnit_Asecond R S L

/-- Remove the second independently inserted unit FIRST. -/
noncomputable def nativeGK4BZDoubleUnit_Bfirst
    (R : T ⥤ U) (S : U ⥤ V) (L : V ⥤ W) :
    R ⋙ 𝟭 U ⋙ S ⋙ 𝟭 V ⋙ L ≅ R ⋙ 𝟭 U ⋙ S ⋙ L :=
  Functor.isoWhiskerLeft (R ⋙ 𝟭 U ⋙ S) (Functor.leftUnitor L)

/-- Then remove the original first unit in gap U. -/
noncomputable def nativeGK4BZDoubleUnit_Bsecond
    (R : T ⥤ U) (S : U ⥤ V) (L : V ⥤ W) :
    R ⋙ 𝟭 U ⋙ S ⋙ L ≅ R ⋙ S ⋙ L :=
  nativeGK4BYTargetUnitIso_afterR R S L

/-- Independent removal order B: first gap V, then gap U. -/
noncomputable def nativeGK4BZDoubleUnit_orderB
    (R : T ⥤ U) (S : U ⥤ V) (L : V ⥤ W) :
    R ⋙ 𝟭 U ⋙ S ⋙ 𝟭 V ⋙ L ≅ R ⋙ S ⋙ L :=
  nativeGK4BZDoubleUnit_Bfirst R S L ≪≫
    nativeGK4BZDoubleUnit_Bsecond R S L

/-- The TWO honest Mathlib NatIso removal orders agree as WHOLE
natural isomorphisms. The comparison is not merely componentwise. -/
theorem nativeGK4BZDoubleUnit_twoOrders_eq
    (R : T ⥤ U) (S : U ⥤ V) (L : V ⥤ W) :
    nativeGK4BZDoubleUnit_orderA R S L =
      nativeGK4BZDoubleUnit_orderB R S L := by
  apply Iso.ext
  ext Z
  simp [nativeGK4BZDoubleUnit_orderA, nativeGK4BZDoubleUnit_orderB,
    nativeGK4BZDoubleUnit_Afirst, nativeGK4BZDoubleUnit_Asecond,
    nativeGK4BZDoubleUnit_Bfirst, nativeGK4BZDoubleUnit_Bsecond,
    nativeGK4BYTargetUnitIso_afterR, nativeGK4BYTargetUnitIso_afterS]

/-- Apply the genuine five-stage path theorem to TWO separate
unit insertions: ALL 14 actual bracketings reduce to the same
direct chosen-inverse comparison as a whole Mathlib NatIso. -/
theorem nativeGK4BZChosenInverse_doubleUnit_fourteen
    (i : Fin 14)
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (R : T ⥤ U) (S : U ⥤ V) (L : V ⥤ W) :
    nativeGK4BZChosenInverse_fivePathIndexed i p ma mb pa pb
        R (𝟭 U) S (𝟭 V) L =
      nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L) := by
  simpa only [nativeGK4BZChosenInverse_fivePathIndexed_eq_direct,
    Functor.id_comp, Functor.comp_id]

/-- Whole NatTrans modification square, with the true two-unit
removal iso (order A), holds UNIFORMLY for all 14 genuine paths. -/
theorem nativeGK4BZChosenInverse_doubleUnit_orderA_square
    (i : Fin 14)
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (R : T ⥤ U) (S : U ⥤ V) (L : V ⥤ W) :
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (nativeGK4BZDoubleUnit_orderA R S L).hom)
        (nativeGK4BMCompatibleReverseFunctor (T := W) p ma mb pa pb) ≫
      (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L)).hom =
    (nativeGK4BZChosenInverse_fivePathIndexed i p ma mb pa pb
        R (𝟭 U) S (𝟭 V) L).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (nativeGK4BZDoubleUnit_orderA R S L).hom) := by
  simpa only [nativeGK4BZChosenInverse_doubleUnit_fourteen] using
    (nativeGK4BUChosenInverse_targetNat_square p ma mb pa pb
      (nativeGK4BZDoubleUnit_orderA R S L).hom)

/-- The other order B gives exactly the same type-correct
whole NatTrans square with the same 14 actual five-stage paths. -/
theorem nativeGK4BZChosenInverse_doubleUnit_orderB_square
    (i : Fin 14)
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (R : T ⥤ U) (S : U ⥤ V) (L : V ⥤ W) :
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (nativeGK4BZDoubleUnit_orderB R S L).hom)
        (nativeGK4BMCompatibleReverseFunctor (T := W) p ma mb pa pb) ≫
      (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L)).hom =
    (nativeGK4BZChosenInverse_fivePathIndexed i p ma mb pa pb
        R (𝟭 U) S (𝟭 V) L).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (nativeGK4BZDoubleUnit_orderB R S L).hom) := by
  simpa only [nativeGK4BZDoubleUnit_twoOrders_eq] using
    (nativeGK4BZChosenInverse_doubleUnit_orderA_square i p ma mb pa pb R S L)

/-- The whole left/right NatTrans transports from both orderings
are EXACTLY equal for every one of the 14 genuine five-stage paths. -/
theorem nativeGK4BZChosenInverse_doubleUnit_orderIndependent
    (i : Fin 14)
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (R : T ⥤ U) (S : U ⥤ V) (L : V ⥤ W) :
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (nativeGK4BZDoubleUnit_orderA R S L).hom)
        (nativeGK4BMCompatibleReverseFunctor (T := W) p ma mb pa pb) ≫
      (nativeGK4BZChosenInverse_fivePathIndexed i p ma mb pa pb
        R (𝟭 U) S (𝟭 V) L).hom =
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (nativeGK4BZDoubleUnit_orderB R S L).hom)
        (nativeGK4BMCompatibleReverseFunctor (T := W) p ma mb pa pb) ≫
      (nativeGK4BZChosenInverse_fivePathIndexed i p ma mb pa pb
        R (𝟭 U) S (𝟭 V) L).hom ∧
    (nativeGK4BZChosenInverse_fivePathIndexed i p ma mb pa pb
        R (𝟭 U) S (𝟭 V) L).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (nativeGK4BZDoubleUnit_orderA R S L).hom) =
    (nativeGK4BZChosenInverse_fivePathIndexed i p ma mb pa pb
        R (𝟭 U) S (𝟭 V) L).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (nativeGK4BZDoubleUnit_orderB R S L).hom) := by
  rw [nativeGK4BZDoubleUnit_twoOrders_eq]
  all_goals simp

end TwoIndependentUnits

#print axioms nativeGK4BZChosenInverse_fivePath_1A
#print axioms nativeGK4BZChosenInverse_fivePath_1A_eq_direct
#print axioms nativeGK4BZChosenInverse_fivePath_1B
#print axioms nativeGK4BZChosenInverse_fivePath_1B_eq_direct
#print axioms nativeGK4BZChosenInverse_fivePath_1C
#print axioms nativeGK4BZChosenInverse_fivePath_1C_eq_direct
#print axioms nativeGK4BZChosenInverse_fivePath_1D
#print axioms nativeGK4BZChosenInverse_fivePath_1D_eq_direct
#print axioms nativeGK4BZChosenInverse_fivePath_1E
#print axioms nativeGK4BZChosenInverse_fivePath_1E_eq_direct
#print axioms nativeGK4BZChosenInverse_fivePath_2Left
#print axioms nativeGK4BZChosenInverse_fivePath_2Left_eq_direct
#print axioms nativeGK4BZChosenInverse_fivePath_2Right
#print axioms nativeGK4BZChosenInverse_fivePath_2Right_eq_direct
#print axioms nativeGK4BZChosenInverse_fivePath_3Left
#print axioms nativeGK4BZChosenInverse_fivePath_3Left_eq_direct
#print axioms nativeGK4BZChosenInverse_fivePath_3Right
#print axioms nativeGK4BZChosenInverse_fivePath_3Right_eq_direct
#print axioms nativeGK4BZChosenInverse_fivePath_4A
#print axioms nativeGK4BZChosenInverse_fivePath_4A_eq_direct
#print axioms nativeGK4BZChosenInverse_fivePath_4B
#print axioms nativeGK4BZChosenInverse_fivePath_4B_eq_direct
#print axioms nativeGK4BZChosenInverse_fivePath_4C
#print axioms nativeGK4BZChosenInverse_fivePath_4C_eq_direct
#print axioms nativeGK4BZChosenInverse_fivePath_4D
#print axioms nativeGK4BZChosenInverse_fivePath_4D_eq_direct
#print axioms nativeGK4BZChosenInverse_fivePath_4E
#print axioms nativeGK4BZChosenInverse_fivePath_4E_eq_direct
#print axioms nativeGK4BZChosenInverse_fivePathIndexed
#print axioms nativeGK4BZChosenInverse_fivePathIndexed_eq_direct
#print axioms nativeGK4BZChosenInverse_fivePathIndexed_targetNat_square
#print axioms nativeGK4BZDoubleUnit_Afirst
#print axioms nativeGK4BZDoubleUnit_Asecond
#print axioms nativeGK4BZDoubleUnit_orderA
#print axioms nativeGK4BZDoubleUnit_Bfirst
#print axioms nativeGK4BZDoubleUnit_Bsecond
#print axioms nativeGK4BZDoubleUnit_orderB
#print axioms nativeGK4BZDoubleUnit_twoOrders_eq
#print axioms nativeGK4BZChosenInverse_doubleUnit_fourteen
#print axioms nativeGK4BZChosenInverse_doubleUnit_orderA_square
#print axioms nativeGK4BZChosenInverse_doubleUnit_orderB_square
#print axioms nativeGK4BZChosenInverse_doubleUnit_orderIndependent

end
end Kuu.F112.Physical
