import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4BXChosenInversePentagonNaturalityUnitorTriangle
import Mathlib.CategoryTheory.Functor.Category
import Mathlib.CategoryTheory.Whiskering
import Mathlib.Tactic

/-!
F112-P94D3GK4BY — all-position four-stage identity insertion
and genuine inverse-unitor pentagon/triangle coherence.

Use the existing F45 original structural source, actually attained AH
target category, genuine AH-kernel-compatible full subcategory,
GK4BM's arbitrary CHOSEN inverse Q_T, explicit inverse P_T, and
true comparison κ_T : Q_T ≅ P_T without claiming Q_T = P_T.
GK4BU provides actual whole NatTrans target modification,
GK4BV provides exact binary pasting, GK4BW supplies genuine
five-path pentagon, and GK4BX supplies its target variation and triangle.

This file considers every position of ONE unit insertion into a
THREE-stage target-change chain. For each of the FOUR positions and
FIVE actual four-stage bracketings, the whole choice-inverse NatIso
reduces to Θ of the original three-stage target composite. Forward
and inverse Mathlib unitor transports satisfy full NatTrans squares.
No new raw source high-dimensional cells, Gray, or hyperdescent.

Append-only, tighten-only, overwrite-forbidden, same-root107;
strict 空 center, independent Kuu one presentation.
Pinned Lean v4.30.0-rc2 / mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Protected validation-only PR #1558 stays Draft/OPEN/unmerged.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section
universe uD vD uE vE uT vT uU vU uV vV uW vW

section AllPositionFourTargetUnit
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {T : Type uT} [Category.{vT} T]
variable {U : Type uU} [Category.{vU} U]
variable {V : Type uV} [Category.{vV} V]
variable {W : Type uW} [Category.{vW} W]


/-- Actual iterated Mathlib unitor natural isomorphism for unit insertion before R. -/
noncomputable def nativeGK4BYTargetUnitIso_head
    (R : T ⥤ U) (S : U ⥤ V) (L : V ⥤ W) :
    𝟭 T ⋙ R ⋙ S ⋙ L ≅ R ⋙ S ⋙ L :=
  Functor.isoWhiskerRight
    (Functor.isoWhiskerRight (Functor.leftUnitor R) S) L


/-- Every ACTUAL five-path GK4BW pentagon bracket agrees with the
same whole Θ after inserting a unit before R. -/
theorem nativeGK4BYChosenInverse_head_fivePath_unit
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) (R : T ⥤ U) (S : U ⥤ V) (L : V ⥤ W) :
    nativeGK4BWChosenInverse_four_pathA p ma mb pa pb (𝟭 T) R S L =
      nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L) ∧
    nativeGK4BWChosenInverse_four_pathB p ma mb pa pb (𝟭 T) R S L =
      nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L) ∧
    nativeGK4BWChosenInverse_four_pathC p ma mb pa pb (𝟭 T) R S L =
      nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L) ∧
    nativeGK4BWChosenInverse_four_pathD p ma mb pa pb (𝟭 T) R S L =
      nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L) ∧
    nativeGK4BWChosenInverse_four_pathE p ma mb pa pb (𝟭 T) R S L =
      nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L) := by
  simp only [nativeGK4BWChosenInverse_four_pathA_eq_direct,
    nativeGK4BWChosenInverse_four_pathB_eq_direct,
    nativeGK4BWChosenInverse_four_pathC_eq_direct,
    nativeGK4BWChosenInverse_four_pathD_eq_direct,
    nativeGK4BWChosenInverse_four_pathE_eq_direct, Functor.id_comp, Functor.comp_id]
  all_goals simp


/-- TRUE Mathlib unit-removal natural transformation before R
commutes with ALL five actually pasted chosen-inverse pentagon NatIso
paths. The result is equality of whole NatTrans, not componentwise
diagram-existence. -/
theorem nativeGK4BYChosenInverse_head_fivePath_unitorSquare
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) (R : T ⥤ U) (S : U ⥤ V) (L : V ⥤ W) :
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_head R S L).hom)
        (nativeGK4BMCompatibleReverseFunctor (T := W) p ma mb pa pb) ≫
      (nativeGK4BWChosenInverse_four_pathA p ma mb pa pb (𝟭 T) R S L).hom =
    (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L)).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_head R S L).hom) ∧
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_head R S L).hom)
        (nativeGK4BMCompatibleReverseFunctor (T := W) p ma mb pa pb) ≫
      (nativeGK4BWChosenInverse_four_pathB p ma mb pa pb (𝟭 T) R S L).hom =
    (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L)).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_head R S L).hom) ∧
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_head R S L).hom)
        (nativeGK4BMCompatibleReverseFunctor (T := W) p ma mb pa pb) ≫
      (nativeGK4BWChosenInverse_four_pathC p ma mb pa pb (𝟭 T) R S L).hom =
    (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L)).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_head R S L).hom) ∧
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_head R S L).hom)
        (nativeGK4BMCompatibleReverseFunctor (T := W) p ma mb pa pb) ≫
      (nativeGK4BWChosenInverse_four_pathD p ma mb pa pb (𝟭 T) R S L).hom =
    (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L)).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_head R S L).hom) ∧
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_head R S L).hom)
        (nativeGK4BMCompatibleReverseFunctor (T := W) p ma mb pa pb) ≫
      (nativeGK4BWChosenInverse_four_pathE p ma mb pa pb (𝟭 T) R S L).hom =
    (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L)).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_head R S L).hom) := by
  have h := nativeGK4BUChosenInverse_targetNat_square p ma mb pa pb
    (nativeGK4BYTargetUnitIso_head R S L).hom
  refine ⟨?_, ?_, ?_, ?_, ?_⟩
  all_goals simpa only [nativeGK4BWChosenInverse_four_pathA_eq_direct,
    nativeGK4BWChosenInverse_four_pathB_eq_direct,
    nativeGK4BWChosenInverse_four_pathC_eq_direct,
    nativeGK4BWChosenInverse_four_pathD_eq_direct,
    nativeGK4BWChosenInverse_four_pathE_eq_direct,
    Functor.id_comp, Functor.comp_id] using h


/-- TRUE inverse unitor (unit insertion before R) commutes
with all FIVE actual pentagon bracket paths, including the Q_T
arbitrary-choice transport without presuming strict target equality. -/
theorem nativeGK4BYChosenInverse_head_fivePath_inverseUnitorSquare
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) (R : T ⥤ U) (S : U ⥤ V) (L : V ⥤ W) :
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_head R S L).inv)
        (nativeGK4BMCompatibleReverseFunctor (T := W) p ma mb pa pb) ≫
      (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L)).hom =
    (nativeGK4BWChosenInverse_four_pathA p ma mb pa pb (𝟭 T) R S L).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_head R S L).inv) ∧
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_head R S L).inv)
        (nativeGK4BMCompatibleReverseFunctor (T := W) p ma mb pa pb) ≫
      (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L)).hom =
    (nativeGK4BWChosenInverse_four_pathB p ma mb pa pb (𝟭 T) R S L).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_head R S L).inv) ∧
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_head R S L).inv)
        (nativeGK4BMCompatibleReverseFunctor (T := W) p ma mb pa pb) ≫
      (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L)).hom =
    (nativeGK4BWChosenInverse_four_pathC p ma mb pa pb (𝟭 T) R S L).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_head R S L).inv) ∧
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_head R S L).inv)
        (nativeGK4BMCompatibleReverseFunctor (T := W) p ma mb pa pb) ≫
      (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L)).hom =
    (nativeGK4BWChosenInverse_four_pathD p ma mb pa pb (𝟭 T) R S L).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_head R S L).inv) ∧
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_head R S L).inv)
        (nativeGK4BMCompatibleReverseFunctor (T := W) p ma mb pa pb) ≫
      (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L)).hom =
    (nativeGK4BWChosenInverse_four_pathE p ma mb pa pb (𝟭 T) R S L).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_head R S L).inv) := by
  have h := nativeGK4BUChosenInverse_targetNat_square p ma mb pa pb
    (nativeGK4BYTargetUnitIso_head R S L).inv
  refine ⟨?_, ?_, ?_, ?_, ?_⟩
  all_goals simpa only [nativeGK4BWChosenInverse_four_pathA_eq_direct,
    nativeGK4BWChosenInverse_four_pathB_eq_direct,
    nativeGK4BWChosenInverse_four_pathC_eq_direct,
    nativeGK4BWChosenInverse_four_pathD_eq_direct,
    nativeGK4BWChosenInverse_four_pathE_eq_direct,
    Functor.id_comp, Functor.comp_id] using h


/-- Actual iterated Mathlib unitor natural isomorphism for unit insertion between R and S. -/
noncomputable def nativeGK4BYTargetUnitIso_afterR
    (R : T ⥤ U) (S : U ⥤ V) (L : V ⥤ W) :
    R ⋙ 𝟭 U ⋙ S ⋙ L ≅ R ⋙ S ⋙ L :=
  Functor.isoWhiskerRight
    (Functor.isoWhiskerRight (Functor.rightUnitor R) S) L


/-- Every ACTUAL five-path GK4BW pentagon bracket agrees with the
same whole Θ after inserting a unit between R and S. -/
theorem nativeGK4BYChosenInverse_afterR_fivePath_unit
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) (R : T ⥤ U) (S : U ⥤ V) (L : V ⥤ W) :
    nativeGK4BWChosenInverse_four_pathA p ma mb pa pb R (𝟭 U) S L =
      nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L) ∧
    nativeGK4BWChosenInverse_four_pathB p ma mb pa pb R (𝟭 U) S L =
      nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L) ∧
    nativeGK4BWChosenInverse_four_pathC p ma mb pa pb R (𝟭 U) S L =
      nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L) ∧
    nativeGK4BWChosenInverse_four_pathD p ma mb pa pb R (𝟭 U) S L =
      nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L) ∧
    nativeGK4BWChosenInverse_four_pathE p ma mb pa pb R (𝟭 U) S L =
      nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L) := by
  simp only [nativeGK4BWChosenInverse_four_pathA_eq_direct,
    nativeGK4BWChosenInverse_four_pathB_eq_direct,
    nativeGK4BWChosenInverse_four_pathC_eq_direct,
    nativeGK4BWChosenInverse_four_pathD_eq_direct,
    nativeGK4BWChosenInverse_four_pathE_eq_direct, Functor.id_comp, Functor.comp_id]
  all_goals simp


/-- TRUE Mathlib unit-removal natural transformation between R and S
commutes with ALL five actually pasted chosen-inverse pentagon NatIso
paths. The result is equality of whole NatTrans, not componentwise
diagram-existence. -/
theorem nativeGK4BYChosenInverse_afterR_fivePath_unitorSquare
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) (R : T ⥤ U) (S : U ⥤ V) (L : V ⥤ W) :
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_afterR R S L).hom)
        (nativeGK4BMCompatibleReverseFunctor (T := W) p ma mb pa pb) ≫
      (nativeGK4BWChosenInverse_four_pathA p ma mb pa pb R (𝟭 U) S L).hom =
    (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L)).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_afterR R S L).hom) ∧
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_afterR R S L).hom)
        (nativeGK4BMCompatibleReverseFunctor (T := W) p ma mb pa pb) ≫
      (nativeGK4BWChosenInverse_four_pathB p ma mb pa pb R (𝟭 U) S L).hom =
    (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L)).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_afterR R S L).hom) ∧
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_afterR R S L).hom)
        (nativeGK4BMCompatibleReverseFunctor (T := W) p ma mb pa pb) ≫
      (nativeGK4BWChosenInverse_four_pathC p ma mb pa pb R (𝟭 U) S L).hom =
    (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L)).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_afterR R S L).hom) ∧
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_afterR R S L).hom)
        (nativeGK4BMCompatibleReverseFunctor (T := W) p ma mb pa pb) ≫
      (nativeGK4BWChosenInverse_four_pathD p ma mb pa pb R (𝟭 U) S L).hom =
    (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L)).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_afterR R S L).hom) ∧
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_afterR R S L).hom)
        (nativeGK4BMCompatibleReverseFunctor (T := W) p ma mb pa pb) ≫
      (nativeGK4BWChosenInverse_four_pathE p ma mb pa pb R (𝟭 U) S L).hom =
    (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L)).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_afterR R S L).hom) := by
  have h := nativeGK4BUChosenInverse_targetNat_square p ma mb pa pb
    (nativeGK4BYTargetUnitIso_afterR R S L).hom
  refine ⟨?_, ?_, ?_, ?_, ?_⟩
  all_goals simpa only [nativeGK4BWChosenInverse_four_pathA_eq_direct,
    nativeGK4BWChosenInverse_four_pathB_eq_direct,
    nativeGK4BWChosenInverse_four_pathC_eq_direct,
    nativeGK4BWChosenInverse_four_pathD_eq_direct,
    nativeGK4BWChosenInverse_four_pathE_eq_direct,
    Functor.id_comp, Functor.comp_id] using h


/-- TRUE inverse unitor (unit insertion between R and S) commutes
with all FIVE actual pentagon bracket paths, including the Q_T
arbitrary-choice transport without presuming strict target equality. -/
theorem nativeGK4BYChosenInverse_afterR_fivePath_inverseUnitorSquare
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) (R : T ⥤ U) (S : U ⥤ V) (L : V ⥤ W) :
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_afterR R S L).inv)
        (nativeGK4BMCompatibleReverseFunctor (T := W) p ma mb pa pb) ≫
      (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L)).hom =
    (nativeGK4BWChosenInverse_four_pathA p ma mb pa pb R (𝟭 U) S L).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_afterR R S L).inv) ∧
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_afterR R S L).inv)
        (nativeGK4BMCompatibleReverseFunctor (T := W) p ma mb pa pb) ≫
      (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L)).hom =
    (nativeGK4BWChosenInverse_four_pathB p ma mb pa pb R (𝟭 U) S L).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_afterR R S L).inv) ∧
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_afterR R S L).inv)
        (nativeGK4BMCompatibleReverseFunctor (T := W) p ma mb pa pb) ≫
      (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L)).hom =
    (nativeGK4BWChosenInverse_four_pathC p ma mb pa pb R (𝟭 U) S L).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_afterR R S L).inv) ∧
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_afterR R S L).inv)
        (nativeGK4BMCompatibleReverseFunctor (T := W) p ma mb pa pb) ≫
      (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L)).hom =
    (nativeGK4BWChosenInverse_four_pathD p ma mb pa pb R (𝟭 U) S L).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_afterR R S L).inv) ∧
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_afterR R S L).inv)
        (nativeGK4BMCompatibleReverseFunctor (T := W) p ma mb pa pb) ≫
      (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L)).hom =
    (nativeGK4BWChosenInverse_four_pathE p ma mb pa pb R (𝟭 U) S L).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_afterR R S L).inv) := by
  have h := nativeGK4BUChosenInverse_targetNat_square p ma mb pa pb
    (nativeGK4BYTargetUnitIso_afterR R S L).inv
  refine ⟨?_, ?_, ?_, ?_, ?_⟩
  all_goals simpa only [nativeGK4BWChosenInverse_four_pathA_eq_direct,
    nativeGK4BWChosenInverse_four_pathB_eq_direct,
    nativeGK4BWChosenInverse_four_pathC_eq_direct,
    nativeGK4BWChosenInverse_four_pathD_eq_direct,
    nativeGK4BWChosenInverse_four_pathE_eq_direct,
    Functor.id_comp, Functor.comp_id] using h


/-- Actual iterated Mathlib unitor natural isomorphism for unit insertion between S and L. -/
noncomputable def nativeGK4BYTargetUnitIso_afterS
    (R : T ⥤ U) (S : U ⥤ V) (L : V ⥤ W) :
    R ⋙ S ⋙ 𝟭 V ⋙ L ≅ R ⋙ S ⋙ L :=
  Functor.isoWhiskerRight (Functor.rightUnitor (R ⋙ S)) L


/-- Every ACTUAL five-path GK4BW pentagon bracket agrees with the
same whole Θ after inserting a unit between S and L. -/
theorem nativeGK4BYChosenInverse_afterS_fivePath_unit
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) (R : T ⥤ U) (S : U ⥤ V) (L : V ⥤ W) :
    nativeGK4BWChosenInverse_four_pathA p ma mb pa pb R S (𝟭 V) L =
      nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L) ∧
    nativeGK4BWChosenInverse_four_pathB p ma mb pa pb R S (𝟭 V) L =
      nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L) ∧
    nativeGK4BWChosenInverse_four_pathC p ma mb pa pb R S (𝟭 V) L =
      nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L) ∧
    nativeGK4BWChosenInverse_four_pathD p ma mb pa pb R S (𝟭 V) L =
      nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L) ∧
    nativeGK4BWChosenInverse_four_pathE p ma mb pa pb R S (𝟭 V) L =
      nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L) := by
  simp only [nativeGK4BWChosenInverse_four_pathA_eq_direct,
    nativeGK4BWChosenInverse_four_pathB_eq_direct,
    nativeGK4BWChosenInverse_four_pathC_eq_direct,
    nativeGK4BWChosenInverse_four_pathD_eq_direct,
    nativeGK4BWChosenInverse_four_pathE_eq_direct, Functor.id_comp, Functor.comp_id]
  all_goals simp


/-- TRUE Mathlib unit-removal natural transformation between S and L
commutes with ALL five actually pasted chosen-inverse pentagon NatIso
paths. The result is equality of whole NatTrans, not componentwise
diagram-existence. -/
theorem nativeGK4BYChosenInverse_afterS_fivePath_unitorSquare
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) (R : T ⥤ U) (S : U ⥤ V) (L : V ⥤ W) :
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_afterS R S L).hom)
        (nativeGK4BMCompatibleReverseFunctor (T := W) p ma mb pa pb) ≫
      (nativeGK4BWChosenInverse_four_pathA p ma mb pa pb R S (𝟭 V) L).hom =
    (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L)).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_afterS R S L).hom) ∧
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_afterS R S L).hom)
        (nativeGK4BMCompatibleReverseFunctor (T := W) p ma mb pa pb) ≫
      (nativeGK4BWChosenInverse_four_pathB p ma mb pa pb R S (𝟭 V) L).hom =
    (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L)).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_afterS R S L).hom) ∧
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_afterS R S L).hom)
        (nativeGK4BMCompatibleReverseFunctor (T := W) p ma mb pa pb) ≫
      (nativeGK4BWChosenInverse_four_pathC p ma mb pa pb R S (𝟭 V) L).hom =
    (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L)).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_afterS R S L).hom) ∧
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_afterS R S L).hom)
        (nativeGK4BMCompatibleReverseFunctor (T := W) p ma mb pa pb) ≫
      (nativeGK4BWChosenInverse_four_pathD p ma mb pa pb R S (𝟭 V) L).hom =
    (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L)).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_afterS R S L).hom) ∧
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_afterS R S L).hom)
        (nativeGK4BMCompatibleReverseFunctor (T := W) p ma mb pa pb) ≫
      (nativeGK4BWChosenInverse_four_pathE p ma mb pa pb R S (𝟭 V) L).hom =
    (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L)).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_afterS R S L).hom) := by
  have h := nativeGK4BUChosenInverse_targetNat_square p ma mb pa pb
    (nativeGK4BYTargetUnitIso_afterS R S L).hom
  refine ⟨?_, ?_, ?_, ?_, ?_⟩
  all_goals simpa only [nativeGK4BWChosenInverse_four_pathA_eq_direct,
    nativeGK4BWChosenInverse_four_pathB_eq_direct,
    nativeGK4BWChosenInverse_four_pathC_eq_direct,
    nativeGK4BWChosenInverse_four_pathD_eq_direct,
    nativeGK4BWChosenInverse_four_pathE_eq_direct,
    Functor.id_comp, Functor.comp_id] using h


/-- TRUE inverse unitor (unit insertion between S and L) commutes
with all FIVE actual pentagon bracket paths, including the Q_T
arbitrary-choice transport without presuming strict target equality. -/
theorem nativeGK4BYChosenInverse_afterS_fivePath_inverseUnitorSquare
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) (R : T ⥤ U) (S : U ⥤ V) (L : V ⥤ W) :
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_afterS R S L).inv)
        (nativeGK4BMCompatibleReverseFunctor (T := W) p ma mb pa pb) ≫
      (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L)).hom =
    (nativeGK4BWChosenInverse_four_pathA p ma mb pa pb R S (𝟭 V) L).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_afterS R S L).inv) ∧
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_afterS R S L).inv)
        (nativeGK4BMCompatibleReverseFunctor (T := W) p ma mb pa pb) ≫
      (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L)).hom =
    (nativeGK4BWChosenInverse_four_pathB p ma mb pa pb R S (𝟭 V) L).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_afterS R S L).inv) ∧
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_afterS R S L).inv)
        (nativeGK4BMCompatibleReverseFunctor (T := W) p ma mb pa pb) ≫
      (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L)).hom =
    (nativeGK4BWChosenInverse_four_pathC p ma mb pa pb R S (𝟭 V) L).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_afterS R S L).inv) ∧
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_afterS R S L).inv)
        (nativeGK4BMCompatibleReverseFunctor (T := W) p ma mb pa pb) ≫
      (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L)).hom =
    (nativeGK4BWChosenInverse_four_pathD p ma mb pa pb R S (𝟭 V) L).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_afterS R S L).inv) ∧
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_afterS R S L).inv)
        (nativeGK4BMCompatibleReverseFunctor (T := W) p ma mb pa pb) ≫
      (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L)).hom =
    (nativeGK4BWChosenInverse_four_pathE p ma mb pa pb R S (𝟭 V) L).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_afterS R S L).inv) := by
  have h := nativeGK4BUChosenInverse_targetNat_square p ma mb pa pb
    (nativeGK4BYTargetUnitIso_afterS R S L).inv
  refine ⟨?_, ?_, ?_, ?_, ?_⟩
  all_goals simpa only [nativeGK4BWChosenInverse_four_pathA_eq_direct,
    nativeGK4BWChosenInverse_four_pathB_eq_direct,
    nativeGK4BWChosenInverse_four_pathC_eq_direct,
    nativeGK4BWChosenInverse_four_pathD_eq_direct,
    nativeGK4BWChosenInverse_four_pathE_eq_direct,
    Functor.id_comp, Functor.comp_id] using h


/-- Actual iterated Mathlib unitor natural isomorphism for unit insertion after L. -/
noncomputable def nativeGK4BYTargetUnitIso_tail
    (R : T ⥤ U) (S : U ⥤ V) (L : V ⥤ W) :
    R ⋙ S ⋙ L ⋙ 𝟭 W ≅ R ⋙ S ⋙ L :=
  Functor.rightUnitor (R ⋙ S ⋙ L)


/-- Every ACTUAL five-path GK4BW pentagon bracket agrees with the
same whole Θ after inserting a unit after L. -/
theorem nativeGK4BYChosenInverse_tail_fivePath_unit
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) (R : T ⥤ U) (S : U ⥤ V) (L : V ⥤ W) :
    nativeGK4BWChosenInverse_four_pathA p ma mb pa pb R S L (𝟭 W) =
      nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L) ∧
    nativeGK4BWChosenInverse_four_pathB p ma mb pa pb R S L (𝟭 W) =
      nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L) ∧
    nativeGK4BWChosenInverse_four_pathC p ma mb pa pb R S L (𝟭 W) =
      nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L) ∧
    nativeGK4BWChosenInverse_four_pathD p ma mb pa pb R S L (𝟭 W) =
      nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L) ∧
    nativeGK4BWChosenInverse_four_pathE p ma mb pa pb R S L (𝟭 W) =
      nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L) := by
  simp only [nativeGK4BWChosenInverse_four_pathA_eq_direct,
    nativeGK4BWChosenInverse_four_pathB_eq_direct,
    nativeGK4BWChosenInverse_four_pathC_eq_direct,
    nativeGK4BWChosenInverse_four_pathD_eq_direct,
    nativeGK4BWChosenInverse_four_pathE_eq_direct, Functor.id_comp, Functor.comp_id]
  all_goals simp


/-- TRUE Mathlib unit-removal natural transformation after L
commutes with ALL five actually pasted chosen-inverse pentagon NatIso
paths. The result is equality of whole NatTrans, not componentwise
diagram-existence. -/
theorem nativeGK4BYChosenInverse_tail_fivePath_unitorSquare
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) (R : T ⥤ U) (S : U ⥤ V) (L : V ⥤ W) :
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_tail R S L).hom)
        (nativeGK4BMCompatibleReverseFunctor (T := W) p ma mb pa pb) ≫
      (nativeGK4BWChosenInverse_four_pathA p ma mb pa pb R S L (𝟭 W)).hom =
    (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L)).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_tail R S L).hom) ∧
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_tail R S L).hom)
        (nativeGK4BMCompatibleReverseFunctor (T := W) p ma mb pa pb) ≫
      (nativeGK4BWChosenInverse_four_pathB p ma mb pa pb R S L (𝟭 W)).hom =
    (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L)).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_tail R S L).hom) ∧
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_tail R S L).hom)
        (nativeGK4BMCompatibleReverseFunctor (T := W) p ma mb pa pb) ≫
      (nativeGK4BWChosenInverse_four_pathC p ma mb pa pb R S L (𝟭 W)).hom =
    (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L)).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_tail R S L).hom) ∧
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_tail R S L).hom)
        (nativeGK4BMCompatibleReverseFunctor (T := W) p ma mb pa pb) ≫
      (nativeGK4BWChosenInverse_four_pathD p ma mb pa pb R S L (𝟭 W)).hom =
    (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L)).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_tail R S L).hom) ∧
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_tail R S L).hom)
        (nativeGK4BMCompatibleReverseFunctor (T := W) p ma mb pa pb) ≫
      (nativeGK4BWChosenInverse_four_pathE p ma mb pa pb R S L (𝟭 W)).hom =
    (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L)).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_tail R S L).hom) := by
  have h := nativeGK4BUChosenInverse_targetNat_square p ma mb pa pb
    (nativeGK4BYTargetUnitIso_tail R S L).hom
  refine ⟨?_, ?_, ?_, ?_, ?_⟩
  all_goals simpa only [nativeGK4BWChosenInverse_four_pathA_eq_direct,
    nativeGK4BWChosenInverse_four_pathB_eq_direct,
    nativeGK4BWChosenInverse_four_pathC_eq_direct,
    nativeGK4BWChosenInverse_four_pathD_eq_direct,
    nativeGK4BWChosenInverse_four_pathE_eq_direct,
    Functor.id_comp, Functor.comp_id] using h


/-- TRUE inverse unitor (unit insertion after L) commutes
with all FIVE actual pentagon bracket paths, including the Q_T
arbitrary-choice transport without presuming strict target equality. -/
theorem nativeGK4BYChosenInverse_tail_fivePath_inverseUnitorSquare
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) (R : T ⥤ U) (S : U ⥤ V) (L : V ⥤ W) :
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_tail R S L).inv)
        (nativeGK4BMCompatibleReverseFunctor (T := W) p ma mb pa pb) ≫
      (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L)).hom =
    (nativeGK4BWChosenInverse_four_pathA p ma mb pa pb R S L (𝟭 W)).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_tail R S L).inv) ∧
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_tail R S L).inv)
        (nativeGK4BMCompatibleReverseFunctor (T := W) p ma mb pa pb) ≫
      (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L)).hom =
    (nativeGK4BWChosenInverse_four_pathB p ma mb pa pb R S L (𝟭 W)).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_tail R S L).inv) ∧
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_tail R S L).inv)
        (nativeGK4BMCompatibleReverseFunctor (T := W) p ma mb pa pb) ≫
      (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L)).hom =
    (nativeGK4BWChosenInverse_four_pathC p ma mb pa pb R S L (𝟭 W)).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_tail R S L).inv) ∧
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_tail R S L).inv)
        (nativeGK4BMCompatibleReverseFunctor (T := W) p ma mb pa pb) ≫
      (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L)).hom =
    (nativeGK4BWChosenInverse_four_pathD p ma mb pa pb R S L (𝟭 W)).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_tail R S L).inv) ∧
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_tail R S L).inv)
        (nativeGK4BMCompatibleReverseFunctor (T := W) p ma mb pa pb) ≫
      (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L)).hom =
    (nativeGK4BWChosenInverse_four_pathE p ma mb pa pb R S L (𝟭 W)).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (nativeGK4BYTargetUnitIso_tail R S L).inv) := by
  have h := nativeGK4BUChosenInverse_targetNat_square p ma mb pa pb
    (nativeGK4BYTargetUnitIso_tail R S L).inv
  refine ⟨?_, ?_, ?_, ?_, ?_⟩
  all_goals simpa only [nativeGK4BWChosenInverse_four_pathA_eq_direct,
    nativeGK4BWChosenInverse_four_pathB_eq_direct,
    nativeGK4BWChosenInverse_four_pathC_eq_direct,
    nativeGK4BWChosenInverse_four_pathD_eq_direct,
    nativeGK4BWChosenInverse_four_pathE_eq_direct,
    Functor.id_comp, Functor.comp_id] using h


end AllPositionFourTargetUnit

section ActualInverseUnitorTriangle
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {T : Type uT} [Category.{vT} T]
variable {U : Type uU} [Category.{vU} U]
variable {V : Type uV} [Category.{vV} V]

/-- The actual INVERSE associator-unitor triangle, expressed as
equality of WHOLE Mathlib target natural transformations. -/
theorem nativeGK4BYTargetNat_inverseUnitor_triangle
    (R : T ⥤ U) (S : U ⥤ V) :
    Functor.whiskerRight (Functor.rightUnitor R).inv S =
      Functor.whiskerLeft R (Functor.leftUnitor S).inv ≫
        (Functor.associator R (𝟭 U) S).inv := by
  ext X
  simp

/-- The genuine left target unitor inverse transports the whole
chosen-inverse comparison in the OPPOSITE target direction. -/
theorem nativeGK4BYChosenInverse_leftInverseUnitor_square
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) (R : T ⥤ U) :
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (Functor.leftUnitor R).inv)
        (nativeGK4BMCompatibleReverseFunctor (T := U) p ma mb pa pb) ≫
      (nativeGK4BWChosenInverse_binaryPasting p ma mb pa pb (𝟭 T) R
        (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (𝟭 T))
        (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb R)).hom =
    (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb R).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (Functor.leftUnitor R).inv) := by
  simpa only [nativeGK4BWChosenInverse_leftUnit, Functor.id_comp] using
    (nativeGK4BUChosenInverse_targetNat_square p ma mb pa pb
      (Functor.leftUnitor R).inv)

/-- The genuine right target unitor inverse also transports the
complete arbitrary-choice inverse comparison as a whole NatTrans. -/
theorem nativeGK4BYChosenInverse_rightInverseUnitor_square
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) (R : T ⥤ U) :
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (Functor.rightUnitor R).inv)
        (nativeGK4BMCompatibleReverseFunctor (T := U) p ma mb pa pb) ≫
      (nativeGK4BWChosenInverse_binaryPasting p ma mb pa pb R (𝟭 U)
        (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb R)
        (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (𝟭 U))).hom =
    (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb R).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (Functor.rightUnitor R).inv) := by
  simpa only [nativeGK4BWChosenInverse_rightUnit, Functor.comp_id] using
    (nativeGK4BUChosenInverse_targetNat_square p ma mb pa pb
      (Functor.rightUnitor R).inv)

/-- The inverse unitor triangle transports Θ through the genuine
GK4BW THREE-stage left-parenthesized comparison. -/
theorem nativeGK4BYChosenInverse_inverseTriangle_left_square
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) (R : T ⥤ U) (S : U ⥤ V) :
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (Functor.whiskerRight (Functor.rightUnitor R).inv S))
        (nativeGK4BMCompatibleReverseFunctor (T := V) p ma mb pa pb) ≫
      (nativeGK4BWChosenInverse_threeLeft p ma mb pa pb R (𝟭 U) S).hom =
    (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S)).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (Functor.whiskerRight (Functor.rightUnitor R).inv S)) := by
  simpa only [nativeGK4BXChosenInverse_middleUnit_threeLeft_eq_direct,
    Functor.comp_id, Functor.id_comp] using
    (nativeGK4BUChosenInverse_targetNat_square p ma mb pa pb
      (Functor.whiskerRight (Functor.rightUnitor R).inv S))

/-- The alternate inverse triangle route, left unitor inverted and
associator inverted, transports Θ through the right-parenthesized
three-stage comparison. -/
theorem nativeGK4BYChosenInverse_inverseTriangle_right_square
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) (R : T ⥤ U) (S : U ⥤ V) :
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (Functor.whiskerLeft R (Functor.leftUnitor S).inv ≫
            (Functor.associator R (𝟭 U) S).inv))
        (nativeGK4BMCompatibleReverseFunctor (T := V) p ma mb pa pb) ≫
      (nativeGK4BWChosenInverse_threeRight p ma mb pa pb R (𝟭 U) S).hom =
    (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S)).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (Functor.whiskerLeft R (Functor.leftUnitor S).inv ≫
            (Functor.associator R (𝟭 U) S).inv)) := by
  simpa only [nativeGK4BXChosenInverse_middleUnit_threeRight_eq_direct,
    Functor.comp_id, Functor.id_comp] using
    (nativeGK4BUChosenInverse_targetNat_square p ma mb pa pb
      (Functor.whiskerLeft R (Functor.leftUnitor S).inv ≫
        (Functor.associator R (𝟭 U) S).inv))

/-- After changing target along the inverse triangle, both whole
chosen-inverse modification SQUARES have the identical left and right
pasting NatTrans. This uses the genuine triangle and real GK4BW
three-target associativity, not invented raw higher morphisms. -/
theorem nativeGK4BYChosenInverse_inverseTriangle_twoPaths
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) (R : T ⥤ U) (S : U ⥤ V) :
    (Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (Functor.whiskerRight (Functor.rightUnitor R).inv S))
        (nativeGK4BMCompatibleReverseFunctor (T := V) p ma mb pa pb) ≫
      (nativeGK4BWChosenInverse_threeLeft p ma mb pa pb R (𝟭 U) S).hom) =
    (Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (Functor.whiskerLeft R (Functor.leftUnitor S).inv ≫
            (Functor.associator R (𝟭 U) S).inv))
        (nativeGK4BMCompatibleReverseFunctor (T := V) p ma mb pa pb) ≫
      (nativeGK4BWChosenInverse_threeRight p ma mb pa pb R (𝟭 U) S).hom) ∧
    ((nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S)).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (Functor.whiskerRight (Functor.rightUnitor R).inv S))) =
    ((nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S)).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (Functor.whiskerLeft R (Functor.leftUnitor S).inv ≫
            (Functor.associator R (𝟭 U) S).inv))) := by
  rw [nativeGK4BYTargetNat_inverseUnitor_triangle R S]
  simp only [nativeGK4BWChosenInverse_threeAssociativity]
  exact ⟨rfl, rfl⟩

end ActualInverseUnitorTriangle


#print axioms nativeGK4BYTargetUnitIso_head
#print axioms nativeGK4BYChosenInverse_head_fivePath_unit
#print axioms nativeGK4BYChosenInverse_head_fivePath_unitorSquare
#print axioms nativeGK4BYChosenInverse_head_fivePath_inverseUnitorSquare

#print axioms nativeGK4BYTargetUnitIso_afterR
#print axioms nativeGK4BYChosenInverse_afterR_fivePath_unit
#print axioms nativeGK4BYChosenInverse_afterR_fivePath_unitorSquare
#print axioms nativeGK4BYChosenInverse_afterR_fivePath_inverseUnitorSquare

#print axioms nativeGK4BYTargetUnitIso_afterS
#print axioms nativeGK4BYChosenInverse_afterS_fivePath_unit
#print axioms nativeGK4BYChosenInverse_afterS_fivePath_unitorSquare
#print axioms nativeGK4BYChosenInverse_afterS_fivePath_inverseUnitorSquare

#print axioms nativeGK4BYTargetUnitIso_tail
#print axioms nativeGK4BYChosenInverse_tail_fivePath_unit
#print axioms nativeGK4BYChosenInverse_tail_fivePath_unitorSquare
#print axioms nativeGK4BYChosenInverse_tail_fivePath_inverseUnitorSquare

#print axioms nativeGK4BYTargetNat_inverseUnitor_triangle
#print axioms nativeGK4BYChosenInverse_leftInverseUnitor_square
#print axioms nativeGK4BYChosenInverse_rightInverseUnitor_square
#print axioms nativeGK4BYChosenInverse_inverseTriangle_left_square
#print axioms nativeGK4BYChosenInverse_inverseTriangle_right_square
#print axioms nativeGK4BYChosenInverse_inverseTriangle_twoPaths

end
end Kuu.F112.Physical
