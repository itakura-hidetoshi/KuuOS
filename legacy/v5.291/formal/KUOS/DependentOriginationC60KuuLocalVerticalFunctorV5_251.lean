import KUOS.DependentOriginationC60KuuLocalHorizontalFunctorV5_250

namespace KUOS.DependentOriginationC60KuuLocalVerticalFunctorV5_251

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayC60CyclicGlobalPastingV5_156
open KUOS.DependentOriginationGrayC60OriginalFaceHorizontalPresentationV5_199
open KUOS.DependentOriginationGrayC60OriginalFaceHorizontalThreeHomV5_199
open KUOS.DependentOriginationGrayC60OriginalFaceHorizontalCompositionV5_199
open KUOS.DependentOriginationC60InterchangerStrictChargeQuotientV5_229
open KUOS.DependentOriginationC60StrictChargeHorizontalInterchangeV5_230
open KUOS.DependentOriginationC60NativeExchangeCongruenceQuotientV5_231
open KUOS.DependentOriginationC60NativeQuotientHorizontalTensorV5_234
open KUOS.DependentOriginationC60KuuReplacementInterchangeV5_248
open KUOS.DependentOriginationC60KuuLocalUniversalDescentV5_249
open KUOS.DependentOriginationC60KuuLocalHorizontalFunctorV5_250

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.251 / F97 — vertical C60 two-cell composition on the genuine local Kuu quotients

F96 made ORIGINAL horizontal source-2-cell composition into a real
Mathlib bifunctor of the F95 local Kuu quotient 3-Hom categories.
F97 builds the INDEPENDENT VERTICAL 2-context composition functor
at actual parallel triples of original C60 paths.

No restoration of the nontrivial original Gray exchange is sought.
Kuu means that presentations may be REPLACED provided both original
integer charge coordinates agree; this replacement is compatible
with vertical as well as horizontal 2-cell composition.

The local F95 category quotient changes only Hom sets and retains
the source F42 presentation objects. Consequently, this file does
not claim distinct original raw F42 vertical/horizontal presentation
objects are literally equal. Their complete strict globular
interpretations agree at the already verified F78/F77 target.
-/

/-- Vertical original F42 two-cell composition at an ACTUAL
C60 triple p→q→r, performed in the local Kuu quotient categories. -/
def c60F97VerticalObj
    {a b : IcosahedralDart}
    {p q r : Quiver.Path a b}
    (X : C60F95LocalKuuQuotient p q)
    (Y : C60F95LocalKuuQuotient q r) :
    C60F95LocalKuuQuotient p r :=
  ⟨c60F51OriginalTwoVertical X.as Y.as⟩

/-- Two compatible source presentations may be replaced
independently BEFORE performing original vertical 2-cell composition.
This statement is in the real original C60 F51 3-Hom semantics. -/
theorem c60F97Replaceable_verticalTwo
    {a b : IcosahedralDart}
    {p q r : Quiver.Path a b}
    {X X' : C60F51OriginalTwo p q}
    {Y Y' : C60F51OriginalTwo q r}
    {f f' : X ⟶ X'} {g g' : Y ⟶ Y'}
    (hf : c60F94Replaceable f f')
    (hg : c60F94Replaceable g g') :
    c60F94Replaceable
      (c60F51VerticalTwoMap f g)
      (c60F51VerticalTwoMap f' g') := by
  apply (c60F94Replaceable_iff_charges _ _).mpr
  have hfc := (c60F94Replaceable_iff_charges f f').mp hf
  have hgc := (c60F94Replaceable_iff_charges g g').mp hg
  calc
    (c60F51Eval (c60F51VerticalTwoMap f g)).charge =
        (c60F51Eval f).charge + (c60F51Eval g).charge := by
          rw [c60F51VerticalTwoMap_eval]
          exact grayNeutral_add_charge _ _
    _ = (c60F51Eval f').charge + (c60F51Eval g').charge := by
          rw [hfc, hgc]
    _ = (c60F51Eval (c60F51VerticalTwoMap f' g')).charge := by
          rw [c60F51VerticalTwoMap_eval]
          exact (grayNeutral_add_charge _ _).symm

/-- The new VERTICAL tensor acts on actual F95 QUOTIENT Hom sets.
Its two Quot.liftOn₂ congruence obligations are proved using
the existing CompClosure-aware F95 quotient map and the
F97 source-level replacement theorem. -/
def c60F97VerticalThree
    {a b : IcosahedralDart}
    {p q r : Quiver.Path a b}
    {X X' : C60F95LocalKuuQuotient p q}
    {Y Y' : C60F95LocalKuuQuotient q r}
    (f : X ⟶ X') (g : Y ⟶ Y') :
    c60F97VerticalObj X Y ⟶ c60F97VerticalObj X' Y' :=
  Quot.liftOn₂ f g
    (fun rf rg =>
      (c60F95LocalProjection p r).map (c60F51VerticalTwoMap rf rg))
    (by
      intro rf rg₁ rg₂ h
      apply (c60F95Projection_map_eq_iff _ _).mpr
      exact c60F97Replaceable_verticalTwo
        (c60F94Replaceable_refl rf)
        ((c60F95Projection_map_eq_iff rg₁ rg₂).mp (Quot.sound h)))
    (by
      intro rf₁ rf₂ rg h
      apply (c60F95Projection_map_eq_iff _ _).mpr
      exact c60F97Replaceable_verticalTwo
        ((c60F95Projection_map_eq_iff rf₁ rf₂).mp (Quot.sound h))
        (c60F94Replaceable_refl rg))

/-- The local quotient VERTICAL tensor agrees on actual original
F51 representatives with the F51 source vertical 3-arrow. -/
@[simp] theorem c60F97VerticalThree_representatives
    {a b : IcosahedralDart}
    {p q r : Quiver.Path a b}
    {X X' : C60F51OriginalTwo p q}
    {Y Y' : C60F51OriginalTwo q r}
    (f : X ⟶ X') (g : Y ⟶ Y') :
    c60F97VerticalThree
      ((c60F95LocalProjection p q).map f)
      ((c60F95LocalProjection q r).map g) =
      (c60F95LocalProjection p r).map
        (c60F51VerticalTwoMap f g) := rfl

/-- The VERTICAL two-context quotient 3-arrow operation carries
identities to identities for all original C60 path boundaries. -/
theorem c60F97VerticalThree_id
    {a b : IcosahedralDart}
    {p q r : Quiver.Path a b}
    (X : C60F95LocalKuuQuotient p q)
    (Y : C60F95LocalKuuQuotient q r) :
    c60F97VerticalThree (𝟙 X) (𝟙 Y) =
      𝟙 (c60F97VerticalObj X Y) := by
  rcases X with ⟨X⟩
  rcases Y with ⟨Y⟩
  change
    (c60F95LocalProjection p r).map
      (c60F51VerticalTwoMap (𝟙 X) (𝟙 Y)) =
    (c60F95LocalProjection p r).map
      (𝟙 (c60F51OriginalTwoVertical X Y))
  have h := (c60F51VerticalTwoThreeHomFunctor p q r).map_id (X, Y)
  change
    c60F51VerticalTwoMap (𝟙 X) (𝟙 Y) =
      𝟙 (c60F51OriginalTwoVertical X Y) at h
  rw [h]

/-- Genuine middle-four for VERTICAL 2-context composition:
both sequential 3-arrow composition and simultaneous vertical
2-cell composition commute in the actual F95 quotient Hom sets. -/
theorem c60F97VerticalThree_middleFour
    {a b : IcosahedralDart}
    {p q r : Quiver.Path a b}
    {X X' X'' : C60F95LocalKuuQuotient p q}
    {Y Y' Y'' : C60F95LocalKuuQuotient q r}
    (f : X ⟶ X') (f' : X' ⟶ X'')
    (g : Y ⟶ Y') (g' : Y' ⟶ Y'') :
    c60F97VerticalThree (f ≫ f') (g ≫ g') =
      c60F97VerticalThree f g ≫
        c60F97VerticalThree f' g' := by
  rcases X with ⟨X⟩
  rcases X' with ⟨X'⟩
  rcases X'' with ⟨X''⟩
  rcases Y with ⟨Y⟩
  rcases Y' with ⟨Y'⟩
  rcases Y'' with ⟨Y''⟩
  refine Quot.inductionOn f (fun rf => ?_)
  refine Quot.inductionOn f' (fun rf' => ?_)
  refine Quot.inductionOn g (fun rg => ?_)
  refine Quot.inductionOn g' (fun rg' => ?_)
  change
    (c60F95LocalProjection p r).map
      (c60F51VerticalTwoMap (rf ≫ rf') (rg ≫ rg')) =
    (c60F95LocalProjection p r).map
      (c60F51VerticalTwoMap rf rg) ≫
    (c60F95LocalProjection p r).map
      (c60F51VerticalTwoMap rf' rg')
  rw [← Functor.map_comp]
  have h := (c60F51VerticalTwoThreeHomFunctor p q r).map_comp
    ((rf, rg) : (X, Y) ⟶ (X', Y'))
    ((rf', rg') : (X', Y') ⟶ (X'', Y''))
  change
    c60F51VerticalTwoMap (rf ≫ rf') (rg ≫ rg') =
      c60F51VerticalTwoMap rf rg ≫ c60F51VerticalTwoMap rf' rg' at h
  rw [h]

/-- Genuine Mathlib bifunctor of local Kuu-quotiented 3-Hom
categories for original vertical C60 2-cell composition. -/
def c60F97LocalVerticalFunctor
    {a b : IcosahedralDart}
    (p q r : Quiver.Path a b) :
    (C60F95LocalKuuQuotient p q ×
      C60F95LocalKuuQuotient q r) ⥤
        C60F95LocalKuuQuotient p r where
  obj Z := c60F97VerticalObj Z.1 Z.2
  map := fun {_ _} f => c60F97VerticalThree f.1 f.2
  map_id := by
    intro Z
    exact c60F97VerticalThree_id Z.1 Z.2
  map_comp := by
    intro X Y Z f g
    exact c60F97VerticalThree_middleFour f.1 g.1 f.2 g.2

/-- Independent vertical original-source quotient composition
agrees with F80's genuine F77 quotient three-arrow tensor.
Both integer charges survive; the old exchange phase is
NOT reintroduced. -/
theorem c60F97VerticalThree_toF77
    {a b : IcosahedralDart}
    {p q r : Quiver.Path a b}
    {X X' : C60F95LocalKuuQuotient p q}
    {Y Y' : C60F95LocalKuuQuotient q r}
    (f : X ⟶ X') (g : Y ⟶ Y') :
    (c60F95DescendedToF77 p r).map
      (c60F97VerticalThree f g) =
    c60F80QuotientThreeTensor
      ((c60F95DescendedToF77 p q).map f)
      ((c60F95DescendedToF77 q r).map g) := by
  refine Quot.inductionOn f (fun rf => ?_)
  refine Quot.inductionOn g (fun rg => ?_)
  apply c60F80QuotientThree_ext
  change
    (c60F51Eval (c60F51VerticalTwoMap rf rg)).charge =
      (c60F51Eval rf).charge + (c60F51Eval rg).charge
  rw [c60F51VerticalTwoMap_eval]
  exact grayNeutral_add_charge _ _

/-- The vertical original F42 object pasting is precisely
the actual F77 quotient two-cell tensor when evaluated,
without equating original distinct F42 source words. -/
theorem c60F97VerticalObj_toF77
    {a b : IcosahedralDart}
    {p q r : Quiver.Path a b}
    (X : C60F95LocalKuuQuotient p q)
    (Y : C60F95LocalKuuQuotient q r) :
    (c60F95DescendedToF77 p r).obj
      (c60F97VerticalObj X Y) =
    c60F80QuotientTwoTensor
      ((c60F95DescendedToF77 p q).obj X)
      ((c60F95DescendedToF77 q r).obj Y) := by
  rcases X with ⟨X⟩
  rcases Y with ⟨Y⟩
  rfl

/-- At the strict globular F78 semantics, the same vertical
quotient functor becomes the strict F76 tensor of two
independent integer-charge arrows. -/
theorem c60F97VerticalThree_toF78
    {a b : IcosahedralDart}
    {p q r : Quiver.Path a b}
    {X X' : C60F95LocalKuuQuotient p q}
    {Y Y' : C60F95LocalKuuQuotient q r}
    (f : X ⟶ X') (g : Y ⟶ Y') :
    (c60F95StrictGlobularInterpretation p r).map
      (c60F97VerticalThree f g) =
    c60F76StrictChargeThreeTensor
      ((c60F95StrictGlobularInterpretation p q).map f)
      ((c60F95StrictGlobularInterpretation q r).map g) := by
  change
    c60F77QuotientToStrictCharge.map
      ((c60F95DescendedToF77 p r).map
        (c60F97VerticalThree f g)) =
    c60F76StrictChargeThreeTensor
      (c60F77QuotientToStrictCharge.map
        ((c60F95DescendedToF77 p q).map f))
      (c60F77QuotientToStrictCharge.map
        ((c60F95DescendedToF77 q r).map g))
  rw [c60F97VerticalThree_toF77]
  exact c60F80QuotientTensor_chargeFunctor _ _

#print axioms c60F97Replaceable_verticalTwo
#print axioms c60F97VerticalThree_representatives
#print axioms c60F97VerticalThree_id
#print axioms c60F97VerticalThree_middleFour
#print axioms c60F97LocalVerticalFunctor
#print axioms c60F97VerticalThree_toF77
#print axioms c60F97VerticalObj_toF77
#print axioms c60F97VerticalThree_toF78

end
end KUOS.DependentOriginationC60KuuLocalVerticalFunctorV5_251
