import KUOS.DependentOriginationGeneratedHolonomyCountermodelPseudoV2_69
import KUOS.DependentOriginationGeneratedWhiskeringV2_68
import KUOS.DependentOriginationGeneratedCoherenceRoutesV2_68

namespace KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69

open CategoryTheory
open KUOS.DependentOriginationFreePathEvaluatorV2_57
open KUOS.DependentOriginationGeneratedLocalizationHolonomyV2_68
open KUOS.DependentOriginationGeneratedWhiskeringV2_68
open KUOS.DependentOriginationGeneratedCoherenceRoutesV2_68

/-!
# Explicit octahedral generated relation loop v2.69

The direct route is the distinguished composition generator on
`L0 -> M0 -> H0`.  The comparison route goes around the other seven triangular
faces and uses exactly two formal-inverse insertion/cancellation pairs.

Writing `a_ij : L_i -> M_j`, `b_jk : M_j -> H_k`, the long route is

```text
(a00 b00)
  ~ (a01 b10)
  -> a01 b10
  -> a01 b11 b11^-1 b10
  -> (a01 b11) b11^-1 b10
  ~  (a00 b01) b11^-1 b10
  -> a00 b01 b11^-1 b10
  -> a00 a10^-1 a10 b01 b11^-1 b10
  -> a00 a10^-1 (a10 b01) b11^-1 b10
  ~  a00 a10^-1 (a11 b11) b11^-1 b10
  -> a00 a10^-1 a11 b11 b11^-1 b10
  -> a00 a10^-1 a11 b10
  -> a00 a10^-1 (a11 b10)
  ~  a00 a10^-1 (a10 b00)
  -> a00 a10^-1 a10 b00
  -> a00 b00.
```

The four `~` steps use only equality of parallel arrows in the preorder source;
the seven composition steps use precisely the seven untwisted octahedral faces.
The two inverse pairs are `b11 * b11^-1` and `a10^-1 * a10`.
-/

/-- Ordinary localization path generator. -/
abbrev rawPath {X Y : OctahedralVertex} (f : X ⟶ Y) :=
  Localization.Construction.ψ₁ allMorphisms f

/-- Formal inverse localization path generator. -/
abbrev inversePath {X Y : OctahedralVertex} (f : X ⟶ Y) :=
  Localization.Construction.ψ₂ allMorphisms f (by trivial)

/-- Retain one ordinary composition generator in the fully generated syntax. -/
def compositionCell
    {X Y Z : OctahedralVertex} (f : X ⟶ Y) (g : Y ⟶ Z) :
    GeneratedLocalization2Cell allMorphisms
      (rawPath (f ≫ g)) (rawPath f ≫ rawPath g) :=
  generatedLocalization2CellOfGenerating allMorphisms
    (LocalizationGenerating2Cell.comp f g)

/-- Change only the chosen parallel base-arrow presentation.  In the preorder
source any two parallel arrows are equal. -/
def parallelArrowCell
    {X Y : OctahedralVertex} (f g : X ⟶ Y) :
    GeneratedLocalization2Cell allMorphisms (rawPath f) (rawPath g) :=
  generatedLocalization2CellOfEq allMorphisms
    (congrArg
      (fun k : X ⟶ Y => Localization.Construction.ψ₁ allMorphisms k)
      (Subsingleton.elim f g))

/-- Retain the `w * w^-1 -> 1` generator. -/
def forwardInverseCell
    {X Y : OctahedralVertex} (w : X ⟶ Y) :
    GeneratedLocalization2Cell allMorphisms
      (rawPath w ≫ inversePath w) (𝟙 _) :=
  generatedLocalization2CellOfGenerating allMorphisms
    (LocalizationGenerating2Cell.Winv₁ w (by trivial))

/-- Retain the `w^-1 * w -> 1` generator. -/
def inverseForwardCell
    {X Y : OctahedralVertex} (w : X ⟶ Y) :
    GeneratedLocalization2Cell allMorphisms
      (inversePath w ≫ rawPath w) (𝟙 _) :=
  generatedLocalization2CellOfGenerating allMorphisms
    (LocalizationGenerating2Cell.Winv₂ w (by trivial))

/-- Direct distinguished route carrying the single twisted compositor. -/
def counterDirectRoute :
    GeneratedLocalization2Cell allMorphisms
      (rawPath (a00 ≫ b00))
      (rawPath a00 ≫ rawPath b00) :=
  compositionCell a00 b00

/-- First change the direct composite presentation from the `M0` factorization
to the `M1` factorization. -/
def routeStep00 :
    GeneratedLocalization2Cell allMorphisms
      (rawPath (a00 ≫ b00))
      (rawPath (a01 ≫ b10)) :=
  parallelArrowCell (a00 ≫ b00) (a01 ≫ b10)

/-- Expand the untwisted face `L0-M1-H0`. -/
def routeStep01 :
    GeneratedLocalization2Cell allMorphisms
      (rawPath (a01 ≫ b10))
      (rawPath a01 ≫ rawPath b10) :=
  compositionCell a01 b10

/-- Insert `b11 * b11^-1` between `a01` and `b10`. -/
def routeStep02 :
    GeneratedLocalization2Cell allMorphisms
      (rawPath a01 ≫ rawPath b10)
      (rawPath a01 ≫ rawPath b11 ≫ inversePath b11 ≫ rawPath b10) := by
  simpa only [Category.assoc, Category.comp_id, Category.id_comp] using
    (generatedLocalization2CellWhiskerRight allMorphisms (rawPath b10)
      (generatedLocalization2CellWhiskerLeft allMorphisms (rawPath a01)
        (GeneratedLocalization2Cell.symm (forwardInverseCell b11))))

/-- Contract the untwisted face `L0-M1-H1`, retaining the inverse suffix. -/
def routeStep03 :
    GeneratedLocalization2Cell allMorphisms
      (rawPath a01 ≫ rawPath b11 ≫ inversePath b11 ≫ rawPath b10)
      (rawPath (a01 ≫ b11) ≫ inversePath b11 ≫ rawPath b10) := by
  simpa only [Category.assoc] using
    (generatedLocalization2CellWhiskerRight allMorphisms
      (inversePath b11 ≫ rawPath b10)
      (GeneratedLocalization2Cell.symm (compositionCell a01 b11)))

/-- Move the direct `L0 -> H1` presentation from the `M1` to the `M0`
factorization. -/
def routeStep04 :
    GeneratedLocalization2Cell allMorphisms
      (rawPath (a01 ≫ b11) ≫ inversePath b11 ≫ rawPath b10)
      (rawPath (a00 ≫ b01) ≫ inversePath b11 ≫ rawPath b10) := by
  simpa only [Category.assoc] using
    (generatedLocalization2CellWhiskerRight allMorphisms
      (inversePath b11 ≫ rawPath b10)
      (parallelArrowCell (a01 ≫ b11) (a00 ≫ b01)))

/-- Expand the untwisted face `L0-M0-H1`. -/
def routeStep05 :
    GeneratedLocalization2Cell allMorphisms
      (rawPath (a00 ≫ b01) ≫ inversePath b11 ≫ rawPath b10)
      (rawPath a00 ≫ rawPath b01 ≫ inversePath b11 ≫ rawPath b10) := by
  simpa only [Category.assoc] using
    (generatedLocalization2CellWhiskerRight allMorphisms
      (inversePath b11 ≫ rawPath b10)
      (compositionCell a00 b01))

/-- Insert `a10^-1 * a10` after `a00`. -/
def routeStep06 :
    GeneratedLocalization2Cell allMorphisms
      (rawPath a00 ≫ rawPath b01 ≫ inversePath b11 ≫ rawPath b10)
      (rawPath a00 ≫ inversePath a10 ≫ rawPath a10 ≫ rawPath b01 ≫
        inversePath b11 ≫ rawPath b10) := by
  simpa only [Category.assoc, Category.comp_id, Category.id_comp] using
    (generatedLocalization2CellWhiskerRight allMorphisms
      (rawPath b01 ≫ inversePath b11 ≫ rawPath b10)
      (generatedLocalization2CellWhiskerLeft allMorphisms (rawPath a00)
        (GeneratedLocalization2Cell.symm (inverseForwardCell a10))))

/-- Contract the untwisted face `L1-M0-H1` inside the surrounding word. -/
def routeStep07 :
    GeneratedLocalization2Cell allMorphisms
      (rawPath a00 ≫ inversePath a10 ≫ rawPath a10 ≫ rawPath b01 ≫
        inversePath b11 ≫ rawPath b10)
      (rawPath a00 ≫ inversePath a10 ≫ rawPath (a10 ≫ b01) ≫
        inversePath b11 ≫ rawPath b10) := by
  simpa only [Category.assoc] using
    (generatedLocalization2CellWhiskerRight allMorphisms
      (inversePath b11 ≫ rawPath b10)
      (generatedLocalization2CellWhiskerLeft allMorphisms
        (rawPath a00 ≫ inversePath a10)
        (GeneratedLocalization2Cell.symm (compositionCell a10 b01))))

/-- Move the direct `L1 -> H1` presentation from the `M0` to the `M1`
factorization. -/
def routeStep08 :
    GeneratedLocalization2Cell allMorphisms
      (rawPath a00 ≫ inversePath a10 ≫ rawPath (a10 ≫ b01) ≫
        inversePath b11 ≫ rawPath b10)
      (rawPath a00 ≫ inversePath a10 ≫ rawPath (a11 ≫ b11) ≫
        inversePath b11 ≫ rawPath b10) := by
  simpa only [Category.assoc] using
    (generatedLocalization2CellWhiskerRight allMorphisms
      (inversePath b11 ≫ rawPath b10)
      (generatedLocalization2CellWhiskerLeft allMorphisms
        (rawPath a00 ≫ inversePath a10)
        (parallelArrowCell (a10 ≫ b01) (a11 ≫ b11))))

/-- Expand the untwisted face `L1-M1-H1`. -/
def routeStep09 :
    GeneratedLocalization2Cell allMorphisms
      (rawPath a00 ≫ inversePath a10 ≫ rawPath (a11 ≫ b11) ≫
        inversePath b11 ≫ rawPath b10)
      (rawPath a00 ≫ inversePath a10 ≫ rawPath a11 ≫ rawPath b11 ≫
        inversePath b11 ≫ rawPath b10) := by
  simpa only [Category.assoc] using
    (generatedLocalization2CellWhiskerRight allMorphisms
      (inversePath b11 ≫ rawPath b10)
      (generatedLocalization2CellWhiskerLeft allMorphisms
        (rawPath a00 ≫ inversePath a10)
        (compositionCell a11 b11)))

/-- Cancel the previously inserted `b11 * b11^-1` pair. -/
def routeStep10 :
    GeneratedLocalization2Cell allMorphisms
      (rawPath a00 ≫ inversePath a10 ≫ rawPath a11 ≫ rawPath b11 ≫
        inversePath b11 ≫ rawPath b10)
      (rawPath a00 ≫ inversePath a10 ≫ rawPath a11 ≫ rawPath b10) := by
  simpa only [Category.assoc, Category.comp_id, Category.id_comp] using
    (generatedLocalization2CellWhiskerRight allMorphisms (rawPath b10)
      (generatedLocalization2CellWhiskerLeft allMorphisms
        (rawPath a00 ≫ inversePath a10 ≫ rawPath a11)
        (forwardInverseCell b11)))

/-- Contract the untwisted face `L1-M1-H0`. -/
def routeStep11 :
    GeneratedLocalization2Cell allMorphisms
      (rawPath a00 ≫ inversePath a10 ≫ rawPath a11 ≫ rawPath b10)
      (rawPath a00 ≫ inversePath a10 ≫ rawPath (a11 ≫ b10)) := by
  simpa only [Category.assoc] using
    (generatedLocalization2CellWhiskerLeft allMorphisms
      (rawPath a00 ≫ inversePath a10)
      (GeneratedLocalization2Cell.symm (compositionCell a11 b10)))

/-- Move the direct `L1 -> H0` presentation from the `M1` to the `M0`
factorization. -/
def routeStep12 :
    GeneratedLocalization2Cell allMorphisms
      (rawPath a00 ≫ inversePath a10 ≫ rawPath (a11 ≫ b10))
      (rawPath a00 ≫ inversePath a10 ≫ rawPath (a10 ≫ b00)) := by
  simpa only [Category.assoc] using
    (generatedLocalization2CellWhiskerLeft allMorphisms
      (rawPath a00 ≫ inversePath a10)
      (parallelArrowCell (a11 ≫ b10) (a10 ≫ b00)))

/-- Expand the untwisted face `L1-M0-H0`. -/
def routeStep13 :
    GeneratedLocalization2Cell allMorphisms
      (rawPath a00 ≫ inversePath a10 ≫ rawPath (a10 ≫ b00))
      (rawPath a00 ≫ inversePath a10 ≫ rawPath a10 ≫ rawPath b00) := by
  simpa only [Category.assoc] using
    (generatedLocalization2CellWhiskerLeft allMorphisms
      (rawPath a00 ≫ inversePath a10)
      (compositionCell a10 b00))

/-- Cancel the previously inserted `a10^-1 * a10` pair. -/
def routeStep14 :
    GeneratedLocalization2Cell allMorphisms
      (rawPath a00 ≫ inversePath a10 ≫ rawPath a10 ≫ rawPath b00)
      (rawPath a00 ≫ rawPath b00) := by
  simpa only [Category.assoc, Category.comp_id, Category.id_comp] using
    (generatedLocalization2CellWhiskerRight allMorphisms (rawPath b00)
      (generatedLocalization2CellWhiskerLeft allMorphisms (rawPath a00)
        (inverseForwardCell a10)))

/-- The complete generated route around the seven untwisted faces. -/
def counterSevenFaceRoute :
    GeneratedLocalization2Cell allMorphisms
      (rawPath (a00 ≫ b00))
      (rawPath a00 ≫ rawPath b00) :=
  GeneratedLocalization2Cell.trans routeStep00 <|
  GeneratedLocalization2Cell.trans routeStep01 <|
  GeneratedLocalization2Cell.trans routeStep02 <|
  GeneratedLocalization2Cell.trans routeStep03 <|
  GeneratedLocalization2Cell.trans routeStep04 <|
  GeneratedLocalization2Cell.trans routeStep05 <|
  GeneratedLocalization2Cell.trans routeStep06 <|
  GeneratedLocalization2Cell.trans routeStep07 <|
  GeneratedLocalization2Cell.trans routeStep08 <|
  GeneratedLocalization2Cell.trans routeStep09 <|
  GeneratedLocalization2Cell.trans routeStep10 <|
  GeneratedLocalization2Cell.trans routeStep11 <|
  GeneratedLocalization2Cell.trans routeStep12 <|
  GeneratedLocalization2Cell.trans routeStep13 routeStep14

/-- The explicit closed generated loop comparing the twisted face with the
seven-face route. -/
def counterGeneratedLoop :
    GeneratedLocalizationLoop allMorphisms (rawPath a00 ≫ rawPath b00) :=
  generatedLocalization2CellDifference
    allMorphisms counterDirectRoute counterSevenFaceRoute

end KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69
