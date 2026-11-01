import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4BWChosenInverseHigherTargetPentagonUnit
import Mathlib.CategoryTheory.Functor.Category
import Mathlib.CategoryTheory.Whiskering
import Mathlib.Tactic

/-!
F112-P94D3GK4BX — target-NatTrans-compatible FOUR-stage pentagon,
actual Mathlib target unitors, and the associator/unitor triangle.

All comparisons are genuine whole Mathlib NatIso/NatTrans values.
This transports the already proved GK4BU modification through each of
GK4BW's FIVE actual nested GK4BV pastings; the source is the original
F45 typed structural category, the target is the actually attained AH
category, and Q is still GK4BM's arbitrary CHOSEN inverse.
No strict equation Q=P, raw higher cell, Gray category, source-Q
category axiom, ambient-matrix reachability, or hyperdescent follows.

Append-only / tighten-only / overwrite-forbidden / same-root107.
Strict 空 center; independent Kuu is one presentation.
Lean v4.30.0-rc2 / mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Protected validation-only #1558 remains Draft/OPEN/unmerged.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section
universe uD vD uE vE uT vT uU vU uV vV uW vW uX vX

section FourStageNaturality
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {T : Type uT} [Category.{vT} T]
variable {U : Type uU} [Category.{vU} U]
variable {V : Type uV} [Category.{vV} V]
variable {W : Type uW} [Category.{vW} W]
variable {X : Type uX} [Category.{vX} X]

/-- A concrete four-stage horizontal target natural transformation,
not a fictitious high-dimensional cell. -/
def nativeGK4BXTargetNat_fourHorizontal
    {R R' : T ⥤ U} (ρ : R ⟶ R')
    {S S' : U ⥤ V} (σ : S ⟶ S')
    {L L' : V ⥤ W} (τ : L ⟶ L')
    {M M' : W ⥤ X} (υ : M ⟶ M') :
    R ⋙ S ⋙ L ⋙ M ⟶ R' ⋙ S' ⋙ L' ⋙ M' :=
  Functor.whiskerRight
      (nativeGK4BWTargetNat_threeHorizontal ρ σ τ) M ≫
    Functor.whiskerLeft (R' ⋙ S' ⋙ L') υ

/-- Whole NatTrans square of the genuine GK4BW four-stage pathA;
target variations are simultaneous in all four stages. -/
theorem nativeGK4BXChosenInverse_four_pathA_square
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    {R R' : T ⥤ U} (ρ : R ⟶ R')
    {S S' : U ⥤ V} (σ : S ⟶ S')
    {L L' : V ⥤ W} (τ : L ⟶ L')
    {M M' : W ⥤ X} (υ : M ⟶ M') :
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (nativeGK4BXTargetNat_fourHorizontal ρ σ τ υ))
        (nativeGK4BMCompatibleReverseFunctor (T := X) p ma mb pa pb) ≫
      (nativeGK4BWChosenInverse_four_pathA p ma mb pa pb R' S' L' M').hom =
    (nativeGK4BWChosenInverse_four_pathA p ma mb pa pb R S L M).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (nativeGK4BXTargetNat_fourHorizontal ρ σ τ υ)) := by
  simpa only [nativeGK4BWChosenInverse_four_pathA_eq_direct] using
    (nativeGK4BUChosenInverse_targetNat_square p ma mb pa pb
      (nativeGK4BXTargetNat_fourHorizontal ρ σ τ υ))

/-- Whole NatTrans square of the genuine GK4BW four-stage pathB;
target variations are simultaneous in all four stages. -/
theorem nativeGK4BXChosenInverse_four_pathB_square
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    {R R' : T ⥤ U} (ρ : R ⟶ R')
    {S S' : U ⥤ V} (σ : S ⟶ S')
    {L L' : V ⥤ W} (τ : L ⟶ L')
    {M M' : W ⥤ X} (υ : M ⟶ M') :
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (nativeGK4BXTargetNat_fourHorizontal ρ σ τ υ))
        (nativeGK4BMCompatibleReverseFunctor (T := X) p ma mb pa pb) ≫
      (nativeGK4BWChosenInverse_four_pathB p ma mb pa pb R' S' L' M').hom =
    (nativeGK4BWChosenInverse_four_pathB p ma mb pa pb R S L M).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (nativeGK4BXTargetNat_fourHorizontal ρ σ τ υ)) := by
  simpa only [nativeGK4BWChosenInverse_four_pathB_eq_direct] using
    (nativeGK4BUChosenInverse_targetNat_square p ma mb pa pb
      (nativeGK4BXTargetNat_fourHorizontal ρ σ τ υ))

/-- Whole NatTrans square of the genuine GK4BW four-stage pathC;
target variations are simultaneous in all four stages. -/
theorem nativeGK4BXChosenInverse_four_pathC_square
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    {R R' : T ⥤ U} (ρ : R ⟶ R')
    {S S' : U ⥤ V} (σ : S ⟶ S')
    {L L' : V ⥤ W} (τ : L ⟶ L')
    {M M' : W ⥤ X} (υ : M ⟶ M') :
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (nativeGK4BXTargetNat_fourHorizontal ρ σ τ υ))
        (nativeGK4BMCompatibleReverseFunctor (T := X) p ma mb pa pb) ≫
      (nativeGK4BWChosenInverse_four_pathC p ma mb pa pb R' S' L' M').hom =
    (nativeGK4BWChosenInverse_four_pathC p ma mb pa pb R S L M).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (nativeGK4BXTargetNat_fourHorizontal ρ σ τ υ)) := by
  simpa only [nativeGK4BWChosenInverse_four_pathC_eq_direct] using
    (nativeGK4BUChosenInverse_targetNat_square p ma mb pa pb
      (nativeGK4BXTargetNat_fourHorizontal ρ σ τ υ))

/-- Whole NatTrans square of the genuine GK4BW four-stage pathD;
target variations are simultaneous in all four stages. -/
theorem nativeGK4BXChosenInverse_four_pathD_square
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    {R R' : T ⥤ U} (ρ : R ⟶ R')
    {S S' : U ⥤ V} (σ : S ⟶ S')
    {L L' : V ⥤ W} (τ : L ⟶ L')
    {M M' : W ⥤ X} (υ : M ⟶ M') :
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (nativeGK4BXTargetNat_fourHorizontal ρ σ τ υ))
        (nativeGK4BMCompatibleReverseFunctor (T := X) p ma mb pa pb) ≫
      (nativeGK4BWChosenInverse_four_pathD p ma mb pa pb R' S' L' M').hom =
    (nativeGK4BWChosenInverse_four_pathD p ma mb pa pb R S L M).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (nativeGK4BXTargetNat_fourHorizontal ρ σ τ υ)) := by
  simpa only [nativeGK4BWChosenInverse_four_pathD_eq_direct] using
    (nativeGK4BUChosenInverse_targetNat_square p ma mb pa pb
      (nativeGK4BXTargetNat_fourHorizontal ρ σ τ υ))

/-- Whole NatTrans square of the genuine GK4BW four-stage pathE;
target variations are simultaneous in all four stages. -/
theorem nativeGK4BXChosenInverse_four_pathE_square
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    {R R' : T ⥤ U} (ρ : R ⟶ R')
    {S S' : U ⥤ V} (σ : S ⟶ S')
    {L L' : V ⥤ W} (τ : L ⟶ L')
    {M M' : W ⥤ X} (υ : M ⟶ M') :
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (nativeGK4BXTargetNat_fourHorizontal ρ σ τ υ))
        (nativeGK4BMCompatibleReverseFunctor (T := X) p ma mb pa pb) ≫
      (nativeGK4BWChosenInverse_four_pathE p ma mb pa pb R' S' L' M').hom =
    (nativeGK4BWChosenInverse_four_pathE p ma mb pa pb R S L M).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (nativeGK4BXTargetNat_fourHorizontal ρ σ τ υ)) := by
  simpa only [nativeGK4BWChosenInverse_four_pathE_eq_direct] using
    (nativeGK4BUChosenInverse_targetNat_square p ma mb pa pb
      (nativeGK4BXTargetNat_fourHorizontal ρ σ τ υ))

/-- The LEFT sides of all five pentagon-path modification squares
are literally equal as whole NatTrans after horizontal target variation.
This is stronger than comparing componentwise truth values. -/
theorem nativeGK4BXChosenInverse_four_pentagon_leftNatTrans
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    {R R' : T ⥤ U} (ρ : R ⟶ R')
    {S S' : U ⥤ V} (σ : S ⟶ S')
    {L L' : V ⥤ W} (τ : L ⟶ L')
    {M M' : W ⥤ X} (υ : M ⟶ M') :
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (nativeGK4BXTargetNat_fourHorizontal ρ σ τ υ))
        (nativeGK4BMCompatibleReverseFunctor (T := X) p ma mb pa pb) ≫
      (nativeGK4BWChosenInverse_four_pathA p ma mb pa pb R' S' L' M').hom =
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (nativeGK4BXTargetNat_fourHorizontal ρ σ τ υ))
        (nativeGK4BMCompatibleReverseFunctor (T := X) p ma mb pa pb) ≫
      (nativeGK4BWChosenInverse_four_pathB p ma mb pa pb R' S' L' M').hom ∧
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (nativeGK4BXTargetNat_fourHorizontal ρ σ τ υ))
        (nativeGK4BMCompatibleReverseFunctor (T := X) p ma mb pa pb) ≫
      (nativeGK4BWChosenInverse_four_pathB p ma mb pa pb R' S' L' M').hom =
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (nativeGK4BXTargetNat_fourHorizontal ρ σ τ υ))
        (nativeGK4BMCompatibleReverseFunctor (T := X) p ma mb pa pb) ≫
      (nativeGK4BWChosenInverse_four_pathC p ma mb pa pb R' S' L' M').hom ∧
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (nativeGK4BXTargetNat_fourHorizontal ρ σ τ υ))
        (nativeGK4BMCompatibleReverseFunctor (T := X) p ma mb pa pb) ≫
      (nativeGK4BWChosenInverse_four_pathC p ma mb pa pb R' S' L' M').hom =
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (nativeGK4BXTargetNat_fourHorizontal ρ σ τ υ))
        (nativeGK4BMCompatibleReverseFunctor (T := X) p ma mb pa pb) ≫
      (nativeGK4BWChosenInverse_four_pathD p ma mb pa pb R' S' L' M').hom ∧
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (nativeGK4BXTargetNat_fourHorizontal ρ σ τ υ))
        (nativeGK4BMCompatibleReverseFunctor (T := X) p ma mb pa pb) ≫
      (nativeGK4BWChosenInverse_four_pathD p ma mb pa pb R' S' L' M').hom =
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (nativeGK4BXTargetNat_fourHorizontal ρ σ τ υ))
        (nativeGK4BMCompatibleReverseFunctor (T := X) p ma mb pa pb) ≫
      (nativeGK4BWChosenInverse_four_pathE p ma mb pa pb R' S' L' M').hom := by
  simp only [nativeGK4BWChosenInverse_four_pathA_eq_direct,
    nativeGK4BWChosenInverse_four_pathB_eq_direct,
    nativeGK4BWChosenInverse_four_pathC_eq_direct,
    nativeGK4BWChosenInverse_four_pathD_eq_direct,
    nativeGK4BWChosenInverse_four_pathE_eq_direct]
  all_goals simp

/-- The RIGHT sides of the same five modification squares also
agree as full NatTrans, with all transports retained. -/
theorem nativeGK4BXChosenInverse_four_pentagon_rightNatTrans
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    {R R' : T ⥤ U} (ρ : R ⟶ R')
    {S S' : U ⥤ V} (σ : S ⟶ S')
    {L L' : V ⥤ W} (τ : L ⟶ L')
    {M M' : W ⥤ X} (υ : M ⟶ M') :
    (nativeGK4BWChosenInverse_four_pathA p ma mb pa pb R S L M).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (nativeGK4BXTargetNat_fourHorizontal ρ σ τ υ)) =
    (nativeGK4BWChosenInverse_four_pathB p ma mb pa pb R S L M).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (nativeGK4BXTargetNat_fourHorizontal ρ σ τ υ)) ∧
    (nativeGK4BWChosenInverse_four_pathB p ma mb pa pb R S L M).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (nativeGK4BXTargetNat_fourHorizontal ρ σ τ υ)) =
    (nativeGK4BWChosenInverse_four_pathC p ma mb pa pb R S L M).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (nativeGK4BXTargetNat_fourHorizontal ρ σ τ υ)) ∧
    (nativeGK4BWChosenInverse_four_pathC p ma mb pa pb R S L M).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (nativeGK4BXTargetNat_fourHorizontal ρ σ τ υ)) =
    (nativeGK4BWChosenInverse_four_pathD p ma mb pa pb R S L M).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (nativeGK4BXTargetNat_fourHorizontal ρ σ τ υ)) ∧
    (nativeGK4BWChosenInverse_four_pathD p ma mb pa pb R S L M).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (nativeGK4BXTargetNat_fourHorizontal ρ σ τ υ)) =
    (nativeGK4BWChosenInverse_four_pathE p ma mb pa pb R S L M).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (nativeGK4BXTargetNat_fourHorizontal ρ σ τ υ)) := by
  simp only [nativeGK4BWChosenInverse_four_pathA_eq_direct,
    nativeGK4BWChosenInverse_four_pathB_eq_direct,
    nativeGK4BWChosenInverse_four_pathC_eq_direct,
    nativeGK4BWChosenInverse_four_pathD_eq_direct,
    nativeGK4BWChosenInverse_four_pathE_eq_direct]
  all_goals simp

end FourStageNaturality

section ActualUnitorAndTriangle
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {T : Type uT} [Category.{vT} T]
variable {U : Type uU} [Category.{vU} U]
variable {V : Type uV} [Category.{vV} V]

/-- The chosen inverse Θ respects the REAL left Mathlib
target unitor, after inserting the actual GK4BW binary pasting. -/
theorem nativeGK4BXChosenInverse_leftUnitor_square
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) (R : T ⥤ U) :
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (Functor.leftUnitor R).hom)
        (nativeGK4BMCompatibleReverseFunctor (T := U) p ma mb pa pb) ≫
      (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb R).hom =
    (nativeGK4BWChosenInverse_binaryPasting p ma mb pa pb (𝟭 T) R
        (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (𝟭 T))
        (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb R)).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (Functor.leftUnitor R).hom) := by
  simpa only [nativeGK4BWChosenInverse_leftUnit, Functor.id_comp] using
    (nativeGK4BUChosenInverse_targetNat_square p ma mb pa pb
      (Functor.leftUnitor R).hom)

/-- The chosen inverse Θ respects the REAL right Mathlib
target unitor; the chosen Q and explicit P remain distinct. -/
theorem nativeGK4BXChosenInverse_rightUnitor_square
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) (R : T ⥤ U) :
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (Functor.rightUnitor R).hom)
        (nativeGK4BMCompatibleReverseFunctor (T := U) p ma mb pa pb) ≫
      (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb R).hom =
    (nativeGK4BWChosenInverse_binaryPasting p ma mb pa pb R (𝟭 U)
        (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb R)
        (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (𝟭 U))).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (Functor.rightUnitor R).hom) := by
  simpa only [nativeGK4BWChosenInverse_rightUnit, Functor.comp_id] using
    (nativeGK4BUChosenInverse_targetNat_square p ma mb pa pb
      (Functor.rightUnitor R).hom)

/-- Mac Lane's genuine associator/unitor TRIANGLE in the existing
Mathlib functor category, as an equality of full NatTrans. -/
theorem nativeGK4BXTargetNat_associatorUnitor_triangle
    (R : T ⥤ U) (S : U ⥤ V) :
    Functor.whiskerRight (Functor.rightUnitor R).hom S =
      (Functor.associator R (𝟭 U) S).hom ≫
        Functor.whiskerLeft R (Functor.leftUnitor S).hom := by
  ext X
  simp

/-- Left-first parenthesization with a middle identity collapses
to the direct comparison at the true composite target functor. -/
theorem nativeGK4BXChosenInverse_middleUnit_threeLeft_eq_direct
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) (R : T ⥤ U) (S : U ⥤ V) :
    nativeGK4BWChosenInverse_threeLeft p ma mb pa pb R (𝟭 U) S =
      nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S) := by
  simpa only [Functor.comp_id, Functor.id_comp] using
    (nativeGK4BWChosenInverse_threeLeft_eq_direct p ma mb pa pb R (𝟭 U) S)

/-- Right-first parenthesization with the same middle identity
also collapses as a whole NatIso, without choice strictification. -/
theorem nativeGK4BXChosenInverse_middleUnit_threeRight_eq_direct
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) (R : T ⥤ U) (S : U ⥤ V) :
    nativeGK4BWChosenInverse_threeRight p ma mb pa pb R (𝟭 U) S =
      nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S) := by
  simpa only [Functor.comp_id, Functor.id_comp] using
    (nativeGK4BWChosenInverse_threeRight_eq_direct p ma mb pa pb R (𝟭 U) S)

/-- Triangle compatibility, left parenthesization: the
right-unitor whiskering has a fully typed Θ modification square. -/
theorem nativeGK4BXChosenInverse_triangle_left_square
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) (R : T ⥤ U) (S : U ⥤ V) :
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (Functor.whiskerRight (Functor.rightUnitor R).hom S))
        (nativeGK4BMCompatibleReverseFunctor (T := V) p ma mb pa pb) ≫
      (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S)).hom =
    (nativeGK4BWChosenInverse_threeLeft p ma mb pa pb R (𝟭 U) S).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (Functor.whiskerRight (Functor.rightUnitor R).hom S)) := by
  simpa only [nativeGK4BXChosenInverse_middleUnit_threeLeft_eq_direct,
    Functor.comp_id, Functor.id_comp] using
    (nativeGK4BUChosenInverse_targetNat_square p ma mb pa pb
      (Functor.whiskerRight (Functor.rightUnitor R).hom S))

/-- Triangle compatibility, right parenthesization: the
actual associator followed by left unitor yields the same
Θ-modification square. -/
theorem nativeGK4BXChosenInverse_triangle_right_square
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) (R : T ⥤ U) (S : U ⥤ V) :
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          ((Functor.associator R (𝟭 U) S).hom ≫
            Functor.whiskerLeft R (Functor.leftUnitor S).hom))
        (nativeGK4BMCompatibleReverseFunctor (T := V) p ma mb pa pb) ≫
      (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S)).hom =
    (nativeGK4BWChosenInverse_threeRight p ma mb pa pb R (𝟭 U) S).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          ((Functor.associator R (𝟭 U) S).hom ≫
            Functor.whiskerLeft R (Functor.leftUnitor S).hom)) := by
  simpa only [nativeGK4BXChosenInverse_middleUnit_threeRight_eq_direct,
    Functor.comp_id, Functor.id_comp] using
    (nativeGK4BUChosenInverse_targetNat_square p ma mb pa pb
      ((Functor.associator R (𝟭 U) S).hom ≫
        Functor.whiskerLeft R (Functor.leftUnitor S).hom))

end ActualUnitorAndTriangle

#print axioms nativeGK4BXTargetNat_fourHorizontal
#print axioms nativeGK4BXChosenInverse_four_pathA_square
#print axioms nativeGK4BXChosenInverse_four_pathB_square
#print axioms nativeGK4BXChosenInverse_four_pathC_square
#print axioms nativeGK4BXChosenInverse_four_pathD_square
#print axioms nativeGK4BXChosenInverse_four_pathE_square
#print axioms nativeGK4BXChosenInverse_four_pentagon_leftNatTrans
#print axioms nativeGK4BXChosenInverse_four_pentagon_rightNatTrans
#print axioms nativeGK4BXChosenInverse_leftUnitor_square
#print axioms nativeGK4BXChosenInverse_rightUnitor_square
#print axioms nativeGK4BXTargetNat_associatorUnitor_triangle
#print axioms nativeGK4BXChosenInverse_middleUnit_threeLeft_eq_direct
#print axioms nativeGK4BXChosenInverse_middleUnit_threeRight_eq_direct
#print axioms nativeGK4BXChosenInverse_triangle_left_square
#print axioms nativeGK4BXChosenInverse_triangle_right_square

end
end Kuu.F112.Physical
