import KUOS.DependentOriginationC60KuuLocalUniversalDescentV5_249
import KUOS.DependentOriginationC60NativeQuotientHorizontalTensorV5_234

namespace KUOS.DependentOriginationC60KuuLocalHorizontalFunctorV5_250

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationGrayC60OriginalFaceHorizontalPresentationV5_199
open KUOS.DependentOriginationGrayC60OriginalFaceHorizontalThreeHomV5_199
open KUOS.DependentOriginationGrayC60OriginalFaceHorizontalCompositionV5_199
open KUOS.DependentOriginationC60NativeExchangeCongruenceQuotientV5_231
open KUOS.DependentOriginationC60NativeQuotientHorizontalTensorV5_234
open KUOS.DependentOriginationC60KuuReplacementInterchangeV5_248
open KUOS.DependentOriginationC60KuuLocalUniversalDescentV5_249

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.250 / F96 — genuine horizontally composable local Kuu quotient categories

F95 proved each original C60 path pair has a Kuu quotient category
and a universal observer descent, but horizontal substitution was
stated only for original F51 representatives. F96 constructs the
horizontal COMPOSITION FUNCTOR of the actual new local quotient
categories. The construction is by Quot.liftOn₂ on true Hom
quotients, and relies on separately proved independence of BOTH
presentations, not on a primitive equality of Gray exchanges.

Strict identity and middle-four functoriality are inherited from
the original proof-relevant F51 horizontal 3-Hom functor and hold
as honest equalities in the F95 local Kuu quotient.

An additional commuting square compares the functor to F80's
already verified native F77 tensor, with both original independent
Int × Int charges preserved. No reintroduction of the erased
Gray phase, and no assertion of full F55 hyperdescent.
-/

/-- The actual horizontal composite of two original C60
proof-relevant 2-cell presentations IN THEIR LOCAL QUOTIENTS. -/
def c60F96HorizontalObj
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    (X : C60F95LocalKuuQuotient p q)
    (Y : C60F95LocalKuuQuotient r s) :
    C60F95LocalKuuQuotient (p.comp r) (q.comp s) :=
  ⟨c60F51OriginalTwoHorizontal X.as Y.as⟩

/-- Horizontal 3-arrow COMPOSITION on GENUINE LOCAL QUOTIENT HOM SETS,
not a reapplication of quotient to original representatives.
Well-definedness in EACH variable is proved from F94 replacement. -/
def c60F96HorizontalThree
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    {X X' : C60F95LocalKuuQuotient p q}
    {Y Y' : C60F95LocalKuuQuotient r s}
    (f : X ⟶ X') (g : Y ⟶ Y') :
    c60F96HorizontalObj X Y ⟶ c60F96HorizontalObj X' Y' :=
  Quot.liftOn₂ f g
    (fun rf rg =>
      (c60F95LocalProjection (p.comp r) (q.comp s)).map
        (c60F51HorizontalMap rf rg))
    (by
      intro rf rg₁ rg₂ h
      apply (c60F95Projection_map_eq_iff _ _).mpr
      exact c60F94Replaceable_horizontal
        (c60F94Replaceable_refl rf)
        ((c60F95Projection_map_eq_iff rg₁ rg₂).mp (Quot.sound h)))
    (by
      intro rf₁ rf₂ rg h
      apply (c60F95Projection_map_eq_iff _ _).mpr
      exact c60F94Replaceable_horizontal
        ((c60F95Projection_map_eq_iff rf₁ rf₂).mp (Quot.sound h))
        (c60F94Replaceable_refl rg))

/-- On original C60 presentations the new horizontal tensor is
exactly projection of the ORIGINAL horizontal source 3-arrow. -/
@[simp] theorem c60F96HorizontalThree_representatives
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    {X X' : C60F51OriginalTwo p q}
    {Y Y' : C60F51OriginalTwo r s}
    (f : X ⟶ X') (g : Y ⟶ Y') :
    c60F96HorizontalThree
      ((c60F95LocalProjection p q).map f)
      ((c60F95LocalProjection r s).map g) =
    (c60F95LocalProjection (p.comp r) (q.comp s)).map
      (c60F51HorizontalMap f g) := rfl

/-- Horizontal quotient composition takes identities to identity
on every pair of true C60 path-indexed local quotient objects. -/
theorem c60F96HorizontalThree_id
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    (X : C60F95LocalKuuQuotient p q)
    (Y : C60F95LocalKuuQuotient r s) :
    c60F96HorizontalThree (𝟙 X) (𝟙 Y) =
      𝟙 (c60F96HorizontalObj X Y) := by
  rcases X with ⟨X⟩
  rcases Y with ⟨Y⟩
  change
    (c60F95LocalProjection (p.comp r) (q.comp s)).map
      (c60F51HorizontalMap (𝟙 X) (𝟙 Y)) =
    (c60F95LocalProjection (p.comp r) (q.comp s)).map
      (𝟙 (c60F51OriginalTwoHorizontal X Y))
  have h := (c60F51HorizontalThreeHomFunctor p q r s).map_id (X, Y)
  change
    c60F51HorizontalMap (𝟙 X) (𝟙 Y) =
      𝟙 (c60F51OriginalTwoHorizontal X Y) at h
  rw [h]

/-- Full middle-four law holds as a REAL equality of local
Kuu quotient 3-morphisms after descent, for arbitrary
morphisms of the quotient Hom types. -/
theorem c60F96HorizontalThree_middleFour
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    {X X' X'' : C60F95LocalKuuQuotient p q}
    {Y Y' Y'' : C60F95LocalKuuQuotient r s}
    (f : X ⟶ X') (f' : X' ⟶ X'')
    (g : Y ⟶ Y') (g' : Y' ⟶ Y'') :
    c60F96HorizontalThree (f ≫ f') (g ≫ g') =
      c60F96HorizontalThree f g ≫
        c60F96HorizontalThree f' g' := by
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
    (c60F95LocalProjection (p.comp r) (q.comp s)).map
      (c60F51HorizontalMap (rf ≫ rf') (rg ≫ rg')) =
    (c60F95LocalProjection (p.comp r) (q.comp s)).map
      (c60F51HorizontalMap rf rg) ≫
    (c60F95LocalProjection (p.comp r) (q.comp s)).map
      (c60F51HorizontalMap rf' rg')
  rw [← Functor.map_comp]
  have h := (c60F51HorizontalThreeHomFunctor p q r s).map_comp
    ((rf, rg) : (X, Y) ⟶ (X', Y'))
    ((rf', rg') : (X', Y') ⟶ (X'', Y''))
  change
    c60F51HorizontalMap (rf ≫ rf') (rg ≫ rg') =
      c60F51HorizontalMap rf rg ≫ c60F51HorizontalMap rf' rg' at h
  rw [h]

/-- A genuine Mathlib horizontal bifunctor of F95's local Kuu
quotient categories, indexed by the actual original C60 paths. -/
def c60F96LocalHorizontalFunctor
    {a b c : IcosahedralDart}
    (p q : Quiver.Path a b) (r s : Quiver.Path b c) :
    (C60F95LocalKuuQuotient p q × C60F95LocalKuuQuotient r s) ⥤
      C60F95LocalKuuQuotient (p.comp r) (q.comp s) where
  obj Z := c60F96HorizontalObj Z.1 Z.2
  map := fun {_ _} f => c60F96HorizontalThree f.1 f.2
  map_id := by
    intro Z
    exact c60F96HorizontalThree_id Z.1 Z.2
  map_comp := by
    intro X Y Z f g
    exact c60F96HorizontalThree_middleFour f.1 g.1 f.2 g.2

/-- Horizontal local descent COMMUTES with the preexisting real
F77 native horizontal tensor on every true quotient Hom element. -/
theorem c60F96HorizontalThree_toF77
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    {X X' : C60F95LocalKuuQuotient p q}
    {Y Y' : C60F95LocalKuuQuotient r s}
    (f : X ⟶ X') (g : Y ⟶ Y') :
    (c60F95DescendedToF77 (p.comp r) (q.comp s)).map
      (c60F96HorizontalThree f g) =
    c60F80QuotientThreeTensor
      ((c60F95DescendedToF77 p q).map f)
      ((c60F95DescendedToF77 r s).map g) := by
  refine Quot.inductionOn f (fun rf => ?_)
  refine Quot.inductionOn g (fun rg => ?_)
  exact c60F80OriginalF51_horizontal_quotient rf rg

/-- The new quotient horizontal bifunctor agrees with the real
F80 direct quotient tensor at the object level, preserving the
original source and target paths and all integer charges. -/
theorem c60F96HorizontalObj_toF77
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    (X : C60F95LocalKuuQuotient p q)
    (Y : C60F95LocalKuuQuotient r s) :
    (c60F95DescendedToF77 (p.comp r) (q.comp s)).obj
      (c60F96HorizontalObj X Y) =
    c60F80QuotientTwoTensor
      ((c60F95DescendedToF77 p q).obj X)
      ((c60F95DescendedToF77 r s).obj Y) := by
  rcases X with ⟨X⟩
  rcases Y with ⟨Y⟩
  rfl

#print axioms c60F96HorizontalThree_representatives
#print axioms c60F96HorizontalThree_id
#print axioms c60F96HorizontalThree_middleFour
#print axioms c60F96LocalHorizontalFunctor
#print axioms c60F96HorizontalThree_toF77
#print axioms c60F96HorizontalObj_toF77

end
end KUOS.DependentOriginationC60KuuLocalHorizontalFunctorV5_250
