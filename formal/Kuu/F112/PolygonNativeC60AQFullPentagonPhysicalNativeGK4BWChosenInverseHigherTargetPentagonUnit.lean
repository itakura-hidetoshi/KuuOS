import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4BVChosenInverseCompositionCoherence
import Mathlib.CategoryTheory.Whiskering
import Mathlib.Tactic

/-!
F112-P94D3GK4BW — Higher target-coherence for the ACTUAL chosen-inverse comparison.

The original F45-dependent S, actually attained AH category, true compatible
FullSubcategory Comp_T, GK4BM chosen Q_T, GK4BP explicit P_T, and comparison
kappa_T : Q_T ≅ P_T remain unchanged.  GK4BV already proves exact
two-target composition for Theta, and GK4BU proves target-NatTrans
modification.  This file constructs genuine THREE-stage bracketings
of the WHOLE Mathlib NatIso, together with target identity, coherent
rebracketing, actual target pentagon, and three target-variation squares.

No claim that Q_T is strictly equal to P_T, or that raw F54/F55/P92B
Type-valued higher cells, an original source-Q category, unattained
ambient integer matrices, global Gray or hyperdescent are constructed.
Strict 空 center, independent Kuu one presentation.  Same root 107.
Append-only, tighten-only, overwrite-forbidden.
Lean v4.30.0-rc2; mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Validation-only PR #1558 stays Draft/OPEN/unmerged.
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

section TargetThreeAndUnits
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {T : Type uT} [Category.{vT} T]
variable {U : Type uU} [Category.{vU} U]
variable {V : Type uV} [Category.{vV} V]
variable {W : Type uW} [Category.{vW} W]

/-- A genuine typed two-step pasting operator for arbitrary whole NatIso
witnesses alpha and beta; all transport and associator morphisms remain. -/
noncomputable def nativeGK4BWChosenInverse_binaryPasting
    (p : Polygon)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (R : T ⥤ U) (S : U ⥤ V)
    (α :
      (nativeGK4BNPostcompCompatible p ma mb pa pb R ⋙
        nativeGK4BMCompatibleReverseFunctor (T := U) p ma mb pa pb) ≅
      (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb ⋙
        nativeGK4BNPostcompAttained p ma mb pa pb R))
    (β :
      (nativeGK4BNPostcompCompatible p ma mb pa pb S ⋙
        nativeGK4BMCompatibleReverseFunctor (T := V) p ma mb pa pb) ≅
      (nativeGK4BMCompatibleReverseFunctor (T := U) p ma mb pa pb ⋙
        nativeGK4BNPostcompAttained p ma mb pa pb S)) :
    (nativeGK4BNPostcompCompatible p ma mb pa pb (R ⋙ S) ⋙
      nativeGK4BMCompatibleReverseFunctor (T := V) p ma mb pa pb) ≅
    (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb ⋙
      nativeGK4BNPostcompAttained p ma mb pa pb (R ⋙ S)) :=
  eqToIso (congrArg
    (fun W => W ⋙ nativeGK4BMCompatibleReverseFunctor (T := V) p ma mb pa pb)
    (nativeGK4BNPostcompCompatible_comp p ma mb pa pb R S)) ≪≫
  Functor.associator
    (nativeGK4BNPostcompCompatible p ma mb pa pb R)
    (nativeGK4BNPostcompCompatible p ma mb pa pb S)
    (nativeGK4BMCompatibleReverseFunctor (T := V) p ma mb pa pb) ≪≫
  Functor.isoWhiskerLeft
    (nativeGK4BNPostcompCompatible p ma mb pa pb R)
    β ≪≫
  (Functor.associator
    (nativeGK4BNPostcompCompatible p ma mb pa pb R)
    (nativeGK4BMCompatibleReverseFunctor (T := U) p ma mb pa pb)
    (nativeGK4BNPostcompAttained p ma mb pa pb S)).symm ≪≫
  Functor.isoWhiskerRight
    α
    (nativeGK4BNPostcompAttained p ma mb pa pb S) ≪≫
  Functor.associator
    (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
    (nativeGK4BNPostcompAttained p ma mb pa pb R)
    (nativeGK4BNPostcompAttained p ma mb pa pb S) ≪≫
  eqToIso (congrArg
    (fun W => nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb ⋙ W)
    (nativeGK4BVAttainedTarget_comp p ma mb pa pb R S).symm)

/-- The generic binary pasting with the actual GK4BT comparisons is
DEFINITIONALLY the genuine GK4BV two-target NatIso, not a new model. -/
theorem nativeGK4BWChosenInverse_binaryPasting_ofTheta
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) (R : T ⥤ U) (S : U ⥤ V) :
    nativeGK4BWChosenInverse_binaryPasting p ma mb pa pb R S
      (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb R)
      (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb S) =
    nativeGK4BVChosenInverse_twoTargetCompositeIso p ma mb pa pb R S := by
  rfl

/-- First genuine three-target parenthesization, pasting (R,S) first.
The inner factor is the ACTUAL GK4BV two-target NatIso. -/
noncomputable def nativeGK4BWChosenInverse_threeLeft
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (R : T ⥤ U) (S : U ⥤ V) (L : V ⥤ W) :
    (nativeGK4BNPostcompCompatible p ma mb pa pb (R ⋙ S ⋙ L) ⋙
      nativeGK4BMCompatibleReverseFunctor (T := W) p ma mb pa pb) ≅
    (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb ⋙
      nativeGK4BNPostcompAttained p ma mb pa pb (R ⋙ S ⋙ L)) :=
  nativeGK4BWChosenInverse_binaryPasting p ma mb pa pb (R ⋙ S) L
    (nativeGK4BVChosenInverse_twoTargetCompositeIso p ma mb pa pb R S)
    (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb L)

/-- Second genuine three-target parenthesization, pasting (S,L) first.
All source/target transport and associator morphisms remain typed. -/
noncomputable def nativeGK4BWChosenInverse_threeRight
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (R : T ⥤ U) (S : U ⥤ V) (L : V ⥤ W) :
    (nativeGK4BNPostcompCompatible p ma mb pa pb (R ⋙ S ⋙ L) ⋙
      nativeGK4BMCompatibleReverseFunctor (T := W) p ma mb pa pb) ≅
    (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb ⋙
      nativeGK4BNPostcompAttained p ma mb pa pb (R ⋙ S ⋙ L)) :=
  nativeGK4BWChosenInverse_binaryPasting p ma mb pa pb R (S ⋙ L)
    (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb R)
    (nativeGK4BVChosenInverse_twoTargetCompositeIso p ma mb pa pb S L)

/-- Both actual GK4BV stages, left-first, equal the direct GK4BT Theta
for the composite of THREE arbitrary target functors. -/
theorem nativeGK4BWChosenInverse_threeLeft_eq_direct
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (R : T ⥤ U) (S : U ⥤ V) (L : V ⥤ W) :
    nativeGK4BWChosenInverse_threeLeft p ma mb pa pb R S L =
      nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L) := by
  simp only [nativeGK4BWChosenInverse_threeLeft,
    nativeGK4BVChosenInverse_composition_coherence,
    nativeGK4BWChosenInverse_binaryPasting_ofTheta]
  all_goals rfl

/-- The right-first genuine three-target pasting gives the same
direct whole NatIso, with no strictness postulate on choice inverse. -/
theorem nativeGK4BWChosenInverse_threeRight_eq_direct
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (R : T ⥤ U) (S : U ⥤ V) (L : V ⥤ W) :
    nativeGK4BWChosenInverse_threeRight p ma mb pa pb R S L =
      nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L) := by
  simp only [nativeGK4BWChosenInverse_threeRight,
    nativeGK4BVChosenInverse_composition_coherence,
    nativeGK4BWChosenInverse_binaryPasting_ofTheta]

/-- Exact equality of BOTH genuine three-stage pastings
(no extra assumed raw 3-cell). -/
theorem nativeGK4BWChosenInverse_threeAssociativity
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (R : T ⥤ U) (S : U ⥤ V) (L : V ⥤ W) :
    nativeGK4BWChosenInverse_threeLeft p ma mb pa pb R S L =
      nativeGK4BWChosenInverse_threeRight p ma mb pa pb R S L := by
  rw [nativeGK4BWChosenInverse_threeLeft_eq_direct,
      nativeGK4BWChosenInverse_threeRight_eq_direct]

/-- True LEFT target-unit law for the actual choice inverse comparison,
NOT an unsupported equality Q_T=P_T. -/
theorem nativeGK4BWChosenInverse_leftUnit
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) (R : T ⥤ U) :
    nativeGK4BWChosenInverse_binaryPasting p ma mb pa pb (𝟭 T) R
      (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (𝟭 T))
      (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb R) =
      nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb R := by
  simpa only [nativeGK4BWChosenInverse_binaryPasting_ofTheta,
    Functor.id_comp] using
    (nativeGK4BVChosenInverse_composition_coherence p ma mb pa pb (𝟭 T) R)

/-- True RIGHT target-unit law for the genuine whole NatIso. -/
theorem nativeGK4BWChosenInverse_rightUnit
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) (R : T ⥤ U) :
    nativeGK4BWChosenInverse_binaryPasting p ma mb pa pb R (𝟭 U)
      (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb R)
      (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (𝟭 U)) =
      nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb R := by
  simpa only [nativeGK4BWChosenInverse_binaryPasting_ofTheta,
    Functor.comp_id] using
    (nativeGK4BVChosenInverse_composition_coherence p ma mb pa pb R (𝟭 U))

/-- The whole left-bracketed three-stage comparison respects genuine
target transformations of its FIRST stage, with double whiskering. -/
theorem nativeGK4BWChosenInverse_threeFirstTarget_square
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    {R R' : T ⥤ U} (ρ : R ⟶ R') (S : U ⥤ V) (L : V ⥤ W) :
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (Functor.whiskerRight (Functor.whiskerRight ρ S) L))
        (nativeGK4BMCompatibleReverseFunctor (T := W) p ma mb pa pb) ≫
      (nativeGK4BWChosenInverse_threeLeft p ma mb pa pb R' S L).hom =
    (nativeGK4BWChosenInverse_threeLeft p ma mb pa pb R S L).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (Functor.whiskerRight (Functor.whiskerRight ρ S) L)) := by
  simpa only [nativeGK4BWChosenInverse_threeLeft_eq_direct] using
    (nativeGK4BUChosenInverse_targetNat_square p ma mb pa pb
      (Functor.whiskerRight (Functor.whiskerRight ρ S) L))

/-- The WHOLE right-bracketed three-stage comparison respects actual
target transformations of its SECOND stage. -/
theorem nativeGK4BWChosenInverse_threeMiddleTarget_square
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (R : T ⥤ U) {S S' : U ⥤ V} (σ : S ⟶ S') (L : V ⥤ W) :
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (Functor.whiskerRight (Functor.whiskerLeft R σ) L))
        (nativeGK4BMCompatibleReverseFunctor (T := W) p ma mb pa pb) ≫
      (nativeGK4BWChosenInverse_threeRight p ma mb pa pb R S' L).hom =
    (nativeGK4BWChosenInverse_threeRight p ma mb pa pb R S L).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (Functor.whiskerRight (Functor.whiskerLeft R σ) L)) := by
  simpa only [nativeGK4BWChosenInverse_threeRight_eq_direct] using
    (nativeGK4BUChosenInverse_targetNat_square p ma mb pa pb
      (Functor.whiskerRight (Functor.whiskerLeft R σ) L))

/-- The WHOLE left-bracketed three-stage comparison respects actual
target transformations of its THIRD stage, with no raw higher fillers. -/
theorem nativeGK4BWChosenInverse_threeLastTarget_square
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (R : T ⥤ U) (S : U ⥤ V) {L L' : V ⥤ W} (τ : L ⟶ L') :
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (Functor.whiskerLeft (R ⋙ S) τ))
        (nativeGK4BMCompatibleReverseFunctor (T := W) p ma mb pa pb) ≫
      (nativeGK4BWChosenInverse_threeLeft p ma mb pa pb R S L').hom =
    (nativeGK4BWChosenInverse_threeLeft p ma mb pa pb R S L).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (Functor.whiskerLeft (R ⋙ S) τ)) := by
  simpa only [nativeGK4BWChosenInverse_threeLeft_eq_direct] using
    (nativeGK4BUChosenInverse_targetNat_square p ma mb pa pb
      (Functor.whiskerLeft (R ⋙ S) τ))


/- Actual four-target comparison: all five Catalan bracketings
carry genuine Mathlib NatIso values and explicit GK4BV transports. -/
section FourTargetPentagon
variable {X : Type uX} [Category.{vX} X]

/-- Four-target pasting vertex pathA, with its genuine nested GK4BV comparisons. -/
noncomputable def nativeGK4BWChosenInverse_four_pathA
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (R : T ⥤ U) (S : U ⥤ V) (L : V ⥤ W) (M : W ⥤ X) :
    (nativeGK4BNPostcompCompatible p ma mb pa pb (R ⋙ S ⋙ L ⋙ M) ⋙
      nativeGK4BMCompatibleReverseFunctor (T := X) p ma mb pa pb) ≅
    (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb ⋙
      nativeGK4BNPostcompAttained p ma mb pa pb (R ⋙ S ⋙ L ⋙ M)) :=
  nativeGK4BWChosenInverse_binaryPasting p ma mb pa pb (R ⋙ S ⋙ L) M
    (nativeGK4BWChosenInverse_threeLeft p ma mb pa pb R S L) (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb M)

/-- Full typed four-target vertex pathA is the SAME direct chosen-inverse Θ. -/
theorem nativeGK4BWChosenInverse_four_pathA_eq_direct
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (R : T ⥤ U) (S : U ⥤ V) (L : V ⥤ W) (M : W ⥤ X) :
    nativeGK4BWChosenInverse_four_pathA p ma mb pa pb R S L M =
      nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L ⋙ M) := by
  simp only [nativeGK4BWChosenInverse_four_pathA,
    nativeGK4BWChosenInverse_threeLeft_eq_direct,
    nativeGK4BWChosenInverse_binaryPasting_ofTheta,
    nativeGK4BVChosenInverse_composition_coherence]
  all_goals rfl

/-- Four-target pasting vertex pathB, with its genuine nested GK4BV comparisons. -/
noncomputable def nativeGK4BWChosenInverse_four_pathB
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (R : T ⥤ U) (S : U ⥤ V) (L : V ⥤ W) (M : W ⥤ X) :
    (nativeGK4BNPostcompCompatible p ma mb pa pb (R ⋙ S ⋙ L ⋙ M) ⋙
      nativeGK4BMCompatibleReverseFunctor (T := X) p ma mb pa pb) ≅
    (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb ⋙
      nativeGK4BNPostcompAttained p ma mb pa pb (R ⋙ S ⋙ L ⋙ M)) :=
  nativeGK4BWChosenInverse_binaryPasting p ma mb pa pb (R ⋙ S ⋙ L) M
    (nativeGK4BWChosenInverse_threeRight p ma mb pa pb R S L) (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb M)

/-- Full typed four-target vertex pathB is the SAME direct chosen-inverse Θ. -/
theorem nativeGK4BWChosenInverse_four_pathB_eq_direct
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (R : T ⥤ U) (S : U ⥤ V) (L : V ⥤ W) (M : W ⥤ X) :
    nativeGK4BWChosenInverse_four_pathB p ma mb pa pb R S L M =
      nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L ⋙ M) := by
  simp only [nativeGK4BWChosenInverse_four_pathB,
    nativeGK4BWChosenInverse_threeRight_eq_direct,
    nativeGK4BWChosenInverse_binaryPasting_ofTheta,
    nativeGK4BVChosenInverse_composition_coherence]
  all_goals rfl

/-- Four-target pasting vertex pathC, with its genuine nested GK4BV comparisons. -/
noncomputable def nativeGK4BWChosenInverse_four_pathC
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (R : T ⥤ U) (S : U ⥤ V) (L : V ⥤ W) (M : W ⥤ X) :
    (nativeGK4BNPostcompCompatible p ma mb pa pb (R ⋙ S ⋙ L ⋙ M) ⋙
      nativeGK4BMCompatibleReverseFunctor (T := X) p ma mb pa pb) ≅
    (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb ⋙
      nativeGK4BNPostcompAttained p ma mb pa pb (R ⋙ S ⋙ L ⋙ M)) :=
  nativeGK4BWChosenInverse_binaryPasting p ma mb pa pb (R ⋙ S) (L ⋙ M)
    (nativeGK4BVChosenInverse_twoTargetCompositeIso p ma mb pa pb R S) (nativeGK4BVChosenInverse_twoTargetCompositeIso p ma mb pa pb L M)

/-- Full typed four-target vertex pathC is the SAME direct chosen-inverse Θ. -/
theorem nativeGK4BWChosenInverse_four_pathC_eq_direct
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (R : T ⥤ U) (S : U ⥤ V) (L : V ⥤ W) (M : W ⥤ X) :
    nativeGK4BWChosenInverse_four_pathC p ma mb pa pb R S L M =
      nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L ⋙ M) := by
  simp only [nativeGK4BWChosenInverse_four_pathC,
    nativeGK4BVChosenInverse_composition_coherence,
    nativeGK4BWChosenInverse_binaryPasting_ofTheta,
    nativeGK4BVChosenInverse_composition_coherence]
  all_goals rfl

/-- Four-target pasting vertex pathD, with its genuine nested GK4BV comparisons. -/
noncomputable def nativeGK4BWChosenInverse_four_pathD
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (R : T ⥤ U) (S : U ⥤ V) (L : V ⥤ W) (M : W ⥤ X) :
    (nativeGK4BNPostcompCompatible p ma mb pa pb (R ⋙ S ⋙ L ⋙ M) ⋙
      nativeGK4BMCompatibleReverseFunctor (T := X) p ma mb pa pb) ≅
    (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb ⋙
      nativeGK4BNPostcompAttained p ma mb pa pb (R ⋙ S ⋙ L ⋙ M)) :=
  nativeGK4BWChosenInverse_binaryPasting p ma mb pa pb R (S ⋙ L ⋙ M)
    (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb R) (nativeGK4BWChosenInverse_threeLeft p ma mb pa pb S L M)

/-- Full typed four-target vertex pathD is the SAME direct chosen-inverse Θ. -/
theorem nativeGK4BWChosenInverse_four_pathD_eq_direct
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (R : T ⥤ U) (S : U ⥤ V) (L : V ⥤ W) (M : W ⥤ X) :
    nativeGK4BWChosenInverse_four_pathD p ma mb pa pb R S L M =
      nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L ⋙ M) := by
  simp only [nativeGK4BWChosenInverse_four_pathD,
    nativeGK4BWChosenInverse_threeLeft_eq_direct,
    nativeGK4BWChosenInverse_binaryPasting_ofTheta,
    nativeGK4BVChosenInverse_composition_coherence]
  all_goals rfl

/-- Four-target pasting vertex pathE, with its genuine nested GK4BV comparisons. -/
noncomputable def nativeGK4BWChosenInverse_four_pathE
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (R : T ⥤ U) (S : U ⥤ V) (L : V ⥤ W) (M : W ⥤ X) :
    (nativeGK4BNPostcompCompatible p ma mb pa pb (R ⋙ S ⋙ L ⋙ M) ⋙
      nativeGK4BMCompatibleReverseFunctor (T := X) p ma mb pa pb) ≅
    (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb ⋙
      nativeGK4BNPostcompAttained p ma mb pa pb (R ⋙ S ⋙ L ⋙ M)) :=
  nativeGK4BWChosenInverse_binaryPasting p ma mb pa pb R (S ⋙ L ⋙ M)
    (nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb R) (nativeGK4BWChosenInverse_threeRight p ma mb pa pb S L M)

/-- Full typed four-target vertex pathE is the SAME direct chosen-inverse Θ. -/
theorem nativeGK4BWChosenInverse_four_pathE_eq_direct
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (R : T ⥤ U) (S : U ⥤ V) (L : V ⥤ W) (M : W ⥤ X) :
    nativeGK4BWChosenInverse_four_pathE p ma mb pa pb R S L M =
      nativeGK4BTChosenInverse_targetNatIso p ma mb pa pb (R ⋙ S ⋙ L ⋙ M) := by
  simp only [nativeGK4BWChosenInverse_four_pathE,
    nativeGK4BWChosenInverse_threeRight_eq_direct,
    nativeGK4BWChosenInverse_binaryPasting_ofTheta,
    nativeGK4BVChosenInverse_composition_coherence]
  all_goals rfl

/-- The actual FIVE vertices of the four-target pentagon agree
as WHOLE Mathlib natural isomorphisms.  Each vertex first pastes
genuine two-stage and three-stage comparisons, with no strictness
postulate on the separately chosen inverse. -/
theorem nativeGK4BWChosenInverse_fourTarget_pentagon
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    (R : T ⥤ U) (S : U ⥤ V) (L : V ⥤ W) (M : W ⥤ X) :
    nativeGK4BWChosenInverse_four_pathA p ma mb pa pb R S L M =
      nativeGK4BWChosenInverse_four_pathB p ma mb pa pb R S L M ∧
    nativeGK4BWChosenInverse_four_pathB p ma mb pa pb R S L M =
      nativeGK4BWChosenInverse_four_pathC p ma mb pa pb R S L M ∧
    nativeGK4BWChosenInverse_four_pathC p ma mb pa pb R S L M =
      nativeGK4BWChosenInverse_four_pathD p ma mb pa pb R S L M ∧
    nativeGK4BWChosenInverse_four_pathD p ma mb pa pb R S L M =
      nativeGK4BWChosenInverse_four_pathE p ma mb pa pb R S L M := by
  simp only [
    nativeGK4BWChosenInverse_four_pathA_eq_direct,
    nativeGK4BWChosenInverse_four_pathB_eq_direct,
    nativeGK4BWChosenInverse_four_pathC_eq_direct,
    nativeGK4BWChosenInverse_four_pathD_eq_direct,
    nativeGK4BWChosenInverse_four_pathE_eq_direct]
  all_goals simp

end FourTargetPentagon

/-- Actual three-way horizontal target natural transformation,
built by TWO right-whiskers and a final left-whisker. -/
def nativeGK4BWTargetNat_threeHorizontal
    {R R' : T ⥤ U} (ρ : R ⟶ R')
    {S S' : U ⥤ V} (σ : S ⟶ S')
    {L L' : V ⥤ W} (τ : L ⟶ L') :
    (R ⋙ S ⋙ L) ⟶ (R' ⋙ S' ⋙ L') :=
  Functor.whiskerRight (Functor.whiskerRight ρ S) L ≫
    Functor.whiskerRight (Functor.whiskerLeft R' σ) L ≫
      Functor.whiskerLeft (R' ⋙ S') τ

/-- Three simultaneous target natural transformations preserve
the comparison even when the source and target use DIFFERENT
three-stage bracketings.  This is the actual GK4BU modification
transported through GK4BV, not an assumed strict inverse. -/
theorem nativeGK4BWChosenInverse_threeHorizontal_square
    (p : Polygon) (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y)
    {R R' : T ⥤ U} (ρ : R ⟶ R')
    {S S' : U ⥤ V} (σ : S ⟶ S')
    {L L' : V ⥤ W} (τ : L ⟶ L') :
    Functor.whiskerRight
        (nativeGK4BNPostcompCompatibleNat p ma mb pa pb
          (nativeGK4BWTargetNat_threeHorizontal ρ σ τ))
        (nativeGK4BMCompatibleReverseFunctor (T := W) p ma mb pa pb) ≫
      (nativeGK4BWChosenInverse_threeRight p ma mb pa pb R' S' L').hom =
    (nativeGK4BWChosenInverse_threeLeft p ma mb pa pb R S L).hom ≫
      Functor.whiskerLeft
        (nativeGK4BMCompatibleReverseFunctor (T := T) p ma mb pa pb)
        (nativeGK4BNPostcompAttainedNat p ma mb pa pb
          (nativeGK4BWTargetNat_threeHorizontal ρ σ τ)) := by
  simpa only [nativeGK4BWChosenInverse_threeRight_eq_direct,
    nativeGK4BWChosenInverse_threeLeft_eq_direct] using
    (nativeGK4BUChosenInverse_targetNat_square p ma mb pa pb
      (nativeGK4BWTargetNat_threeHorizontal ρ σ τ))

end TargetThreeAndUnits

#print axioms nativeGK4BWChosenInverse_binaryPasting
#print axioms nativeGK4BWChosenInverse_binaryPasting_ofTheta
#print axioms nativeGK4BWChosenInverse_threeLeft
#print axioms nativeGK4BWChosenInverse_threeRight
#print axioms nativeGK4BWChosenInverse_threeLeft_eq_direct
#print axioms nativeGK4BWChosenInverse_threeRight_eq_direct
#print axioms nativeGK4BWChosenInverse_threeAssociativity
#print axioms nativeGK4BWChosenInverse_leftUnit
#print axioms nativeGK4BWChosenInverse_rightUnit
#print axioms nativeGK4BWChosenInverse_threeFirstTarget_square
#print axioms nativeGK4BWChosenInverse_threeMiddleTarget_square
#print axioms nativeGK4BWChosenInverse_threeLastTarget_square

#print axioms nativeGK4BWChosenInverse_four_pathA
#print axioms nativeGK4BWChosenInverse_four_pathA_eq_direct
#print axioms nativeGK4BWChosenInverse_four_pathB
#print axioms nativeGK4BWChosenInverse_four_pathB_eq_direct
#print axioms nativeGK4BWChosenInverse_four_pathC
#print axioms nativeGK4BWChosenInverse_four_pathC_eq_direct
#print axioms nativeGK4BWChosenInverse_four_pathD
#print axioms nativeGK4BWChosenInverse_four_pathD_eq_direct
#print axioms nativeGK4BWChosenInverse_four_pathE
#print axioms nativeGK4BWChosenInverse_four_pathE_eq_direct
#print axioms nativeGK4BWChosenInverse_fourTarget_pentagon
#print axioms nativeGK4BWTargetNat_threeHorizontal
#print axioms nativeGK4BWChosenInverse_threeHorizontal_square

end
end Kuu.F112.Physical
