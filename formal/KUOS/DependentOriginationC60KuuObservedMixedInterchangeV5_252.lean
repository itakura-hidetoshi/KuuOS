import KUOS.DependentOriginationC60KuuLocalVerticalFunctorV5_251
import KUOS.DependentOriginationC60QuotientTensorNaturalityV5_236

namespace KUOS.DependentOriginationC60KuuObservedMixedInterchangeV5_252

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationC60InterchangerStrictChargeQuotientV5_229
open KUOS.DependentOriginationC60NativeExchangeCongruenceQuotientV5_231
open KUOS.DependentOriginationC60NativeQuotientHorizontalTensorV5_234
open KUOS.DependentOriginationC60QuotientTensorNaturalityV5_236
open KUOS.DependentOriginationC60KuuLocalUniversalDescentV5_249
open KUOS.DependentOriginationC60KuuLocalHorizontalFunctorV5_250
open KUOS.DependentOriginationC60KuuLocalVerticalFunctorV5_251

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.252 / F98 — observed mixed horizontal/vertical interchange by Kuu replaceability

F96 and F97 supplied the actual local Kuu quotient 3-Hom horizontal and
vertical composition functors. Their order gives two DIFFERENT
proof-relevant F42 object presentations, which are NOT made equal in
the F95 local source categories (Mathlib's category quotient is on Hom).

The mathematically appropriate compatibility is a genuinely TYPED
NATURAL ISOMORPHISM between the two routes AFTER their canonical
F95-to-F77 descent. This is stronger than merely equating four charge
labels: it is a Mathlib NatIso between complete functors from the
product of four independently indexed original C60 local categories.

Its components are identity transport at F77 observable objects;
naturality is proved by F96/F97 quotient tensor laws and the true
F80 middle-four interchange. Both independent integer charges remain
available and the original Gray phase is NEVER reconstructed.
-/

/-- Four independent correctly path-indexed original Kuu 3-Hom inputs. -/
abbrev C60F98FourLocalInputs
    {a b c : IcosahedralDart}
    (p q r : Quiver.Path a b) (s t u : Quiver.Path b c) :=
  (C60F95LocalKuuQuotient p q × C60F95LocalKuuQuotient q r) ×
    (C60F95LocalKuuQuotient s t × C60F95LocalKuuQuotient t u)

/-- HORIZONTAL after VERTICAL pasting, observed as a true F77 quotient object. -/
def c60F98HorizontalAfterVerticalObj
    {a b c : IcosahedralDart}
    {p q r : Quiver.Path a b} {s t u : Quiver.Path b c}
    (X : C60F95LocalKuuQuotient p q)
    (X' : C60F95LocalKuuQuotient q r)
    (Y : C60F95LocalKuuQuotient s t)
    (Y' : C60F95LocalKuuQuotient t u) : C60F77NativeQuotient :=
  (c60F95DescendedToF77 (p.comp s) (r.comp u)).obj
    (c60F96HorizontalObj
      (c60F97VerticalObj X X')
      (c60F97VerticalObj Y Y'))

/-- VERTICAL after HORIZONTAL pasting, observed on the SAME F77 quotient. -/
def c60F98VerticalAfterHorizontalObj
    {a b c : IcosahedralDart}
    {p q r : Quiver.Path a b} {s t u : Quiver.Path b c}
    (X : C60F95LocalKuuQuotient p q)
    (X' : C60F95LocalKuuQuotient q r)
    (Y : C60F95LocalKuuQuotient s t)
    (Y' : C60F95LocalKuuQuotient t u) : C60F77NativeQuotient :=
  (c60F95DescendedToF77 (p.comp s) (r.comp u)).obj
    (c60F97VerticalObj
      (c60F96HorizontalObj X Y)
      (c60F96HorizontalObj X' Y'))

/-- The two ORIGINAL presentation orders give identical F77
observed objects, without claiming equality of the raw F42 objects. -/
theorem c60F98ObservedMixedObject_eq
    {a b c : IcosahedralDart}
    {p q r : Quiver.Path a b} {s t u : Quiver.Path b c}
    (X : C60F95LocalKuuQuotient p q)
    (X' : C60F95LocalKuuQuotient q r)
    (Y : C60F95LocalKuuQuotient s t)
    (Y' : C60F95LocalKuuQuotient t u) :
    c60F98HorizontalAfterVerticalObj X X' Y Y' =
      c60F98VerticalAfterHorizontalObj X X' Y Y' := by
  unfold c60F98HorizontalAfterVerticalObj
    c60F98VerticalAfterHorizontalObj
  simpa only [c60F96HorizontalObj_toF77,
    c60F97VerticalObj_toF77] using
    (c60F80QuotientTwoTensor_middleFour
      ((c60F95DescendedToF77 p q).obj X)
      ((c60F95DescendedToF77 q r).obj X')
      ((c60F95DescendedToF77 s t).obj Y)
      ((c60F95DescendedToF77 t u).obj Y'))

/-- HORIZONTAL after VERTICAL pasting of arbitrary original
LOCAL QUOTIENT 3-arrows, evaluated as a genuine F77 morphism. -/
def c60F98HorizontalAfterVerticalMap
    {a b c : IcosahedralDart}
    {p q r : Quiver.Path a b} {s t u : Quiver.Path b c}
    {X X₁ : C60F95LocalKuuQuotient p q}
    {X' X₁' : C60F95LocalKuuQuotient q r}
    {Y Y₁ : C60F95LocalKuuQuotient s t}
    {Y' Y₁' : C60F95LocalKuuQuotient t u}
    (f : X ⟶ X₁) (f' : X' ⟶ X₁')
    (g : Y ⟶ Y₁) (g' : Y' ⟶ Y₁') :
    c60F98HorizontalAfterVerticalObj X X' Y Y' ⟶
      c60F98HorizontalAfterVerticalObj X₁ X₁' Y₁ Y₁' :=
  (c60F95DescendedToF77 (p.comp s) (r.comp u)).map
    (c60F96HorizontalThree
      (c60F97VerticalThree f f')
      (c60F97VerticalThree g g'))

/-- VERTICAL after HORIZONTAL, genuinely on the same F77 morphism category. -/
def c60F98VerticalAfterHorizontalMap
    {a b c : IcosahedralDart}
    {p q r : Quiver.Path a b} {s t u : Quiver.Path b c}
    {X X₁ : C60F95LocalKuuQuotient p q}
    {X' X₁' : C60F95LocalKuuQuotient q r}
    {Y Y₁ : C60F95LocalKuuQuotient s t}
    {Y' Y₁' : C60F95LocalKuuQuotient t u}
    (f : X ⟶ X₁) (f' : X' ⟶ X₁')
    (g : Y ⟶ Y₁) (g' : Y' ⟶ Y₁') :
    c60F98VerticalAfterHorizontalObj X X' Y Y' ⟶
      c60F98VerticalAfterHorizontalObj X₁ X₁' Y₁ Y₁' :=
  (c60F95DescendedToF77 (p.comp s) (r.comp u)).map
    (c60F97VerticalThree
      (c60F96HorizontalThree f g)
      (c60F96HorizontalThree f' g'))

/-- The actual FOUR-ARROW middle-four square commutes between
both different original pasting orders AFTER F77 descent.
The equality includes typed source and target transports;
it is not an unsupported equality of distinct raw F42 words. -/
theorem c60F98ObservedMixed_naturality
    {a b c : IcosahedralDart}
    {p q r : Quiver.Path a b} {s t u : Quiver.Path b c}
    {X X₁ : C60F95LocalKuuQuotient p q}
    {X' X₁' : C60F95LocalKuuQuotient q r}
    {Y Y₁ : C60F95LocalKuuQuotient s t}
    {Y' Y₁' : C60F95LocalKuuQuotient t u}
    (f : X ⟶ X₁) (f' : X' ⟶ X₁')
    (g : Y ⟶ Y₁) (g' : Y' ⟶ Y₁') :
    c60F98HorizontalAfterVerticalMap f f' g g' ≫
        eqToHom (c60F98ObservedMixedObject_eq X₁ X₁' Y₁ Y₁') =
      eqToHom (c60F98ObservedMixedObject_eq X X' Y Y') ≫
        c60F98VerticalAfterHorizontalMap f f' g g' := by
  apply c60F80QuotientThree_ext
  unfold c60F98HorizontalAfterVerticalMap
    c60F98VerticalAfterHorizontalMap
  simp only [c60F80QuotientThree_comp_charge,
    c60F82Quotient_eqToHom_charge_zero,
    c60F96HorizontalThree_toF77, c60F97VerticalThree_toF77,
    c60F80QuotientThreeTensor_charge, add_zero, zero_add]
  abel

/-- One real functor for horizontal-after-vertical composition,
from the product of FOUR original C60 Kuu local Hom categories. -/
def c60F98HorizontalAfterVerticalFunctor
    {a b c : IcosahedralDart}
    (p q r : Quiver.Path a b) (s t u : Quiver.Path b c) :
    C60F98FourLocalInputs p q r s t u ⥤ C60F77NativeQuotient where
  obj Z := c60F98HorizontalAfterVerticalObj Z.1.1 Z.1.2 Z.2.1 Z.2.2
  map := fun {_ _} f =>
    c60F98HorizontalAfterVerticalMap f.1.1 f.1.2 f.2.1 f.2.2
  map_id := by
    intro Z
    change
      c60F98HorizontalAfterVerticalMap
        (𝟙 Z.1.1) (𝟙 Z.1.2) (𝟙 Z.2.1) (𝟙 Z.2.2) = 𝟙 _
    unfold c60F98HorizontalAfterVerticalMap
    simp only [c60F97VerticalThree_id, c60F96HorizontalThree_id,
      Functor.map_id]
  map_comp := by
    intro X Y Z f g
    change
      c60F98HorizontalAfterVerticalMap
          (f.1.1 ≫ g.1.1) (f.1.2 ≫ g.1.2)
          (f.2.1 ≫ g.2.1) (f.2.2 ≫ g.2.2) =
        c60F98HorizontalAfterVerticalMap f.1.1 f.1.2 f.2.1 f.2.2 ≫
          c60F98HorizontalAfterVerticalMap g.1.1 g.1.2 g.2.1 g.2.2
    unfold c60F98HorizontalAfterVerticalMap
    simp only [c60F97VerticalThree_middleFour,
      c60F96HorizontalThree_middleFour, Functor.map_comp]

/-- The second functor, vertical-after-horizontal, is constructed
independently on actual input and output Hom types. -/
def c60F98VerticalAfterHorizontalFunctor
    {a b c : IcosahedralDart}
    (p q r : Quiver.Path a b) (s t u : Quiver.Path b c) :
    C60F98FourLocalInputs p q r s t u ⥤ C60F77NativeQuotient where
  obj Z := c60F98VerticalAfterHorizontalObj Z.1.1 Z.1.2 Z.2.1 Z.2.2
  map := fun {_ _} f =>
    c60F98VerticalAfterHorizontalMap f.1.1 f.1.2 f.2.1 f.2.2
  map_id := by
    intro Z
    change
      c60F98VerticalAfterHorizontalMap
        (𝟙 Z.1.1) (𝟙 Z.1.2) (𝟙 Z.2.1) (𝟙 Z.2.2) = 𝟙 _
    unfold c60F98VerticalAfterHorizontalMap
    simp only [c60F96HorizontalThree_id, c60F97VerticalThree_id,
      Functor.map_id]
  map_comp := by
    intro X Y Z f g
    change
      c60F98VerticalAfterHorizontalMap
          (f.1.1 ≫ g.1.1) (f.1.2 ≫ g.1.2)
          (f.2.1 ≫ g.2.1) (f.2.2 ≫ g.2.2) =
        c60F98VerticalAfterHorizontalMap f.1.1 f.1.2 f.2.1 f.2.2 ≫
          c60F98VerticalAfterHorizontalMap g.1.1 g.1.2 g.2.1 g.2.2
    unfold c60F98VerticalAfterHorizontalMap
    simp only [c60F96HorizontalThree_middleFour,
      c60F97VerticalThree_middleFour, Functor.map_comp]

/-- A GENUINE Mathlib natural isomorphism, not a diagrammatic
claim. It witnesses horizontal/vertical exchange after the Kuu
quotient observation while preserving all original path indices. -/
def c60F98ObservedMixedNatIso
    {a b c : IcosahedralDart}
    (p q r : Quiver.Path a b) (s t u : Quiver.Path b c) :
    c60F98HorizontalAfterVerticalFunctor p q r s t u ≅
      c60F98VerticalAfterHorizontalFunctor p q r s t u :=
  NatIso.ofComponents
    (fun Z => eqToIso
      (c60F98ObservedMixedObject_eq Z.1.1 Z.1.2 Z.2.1 Z.2.2))
    (by
      intro X Y f
      change
        c60F98HorizontalAfterVerticalMap f.1.1 f.1.2 f.2.1 f.2.2 ≫
          eqToHom
            (c60F98ObservedMixedObject_eq Y.1.1 Y.1.2 Y.2.1 Y.2.2) =
        eqToHom
            (c60F98ObservedMixedObject_eq X.1.1 X.1.2 X.2.1 X.2.2) ≫
          c60F98VerticalAfterHorizontalMap f.1.1 f.1.2 f.2.1 f.2.2
      exact c60F98ObservedMixed_naturality f.1.1 f.1.2 f.2.1 f.2.2)

/-- The actual interchange natural isomorphism carries ZERO
additional integer charge; it does not set input charges to zero. -/
theorem c60F98ObservedMixedNatIso_charge_zero
    {a b c : IcosahedralDart}
    (p q r : Quiver.Path a b) (s t u : Quiver.Path b c)
    (Z : C60F98FourLocalInputs p q r s t u) :
    (c60F77QuotientToStrictCharge.map
      (c60F98ObservedMixedNatIso p q r s t u).hom.app Z).charge =
      (0 : Int × Int) := by
  change
    (c60F77QuotientToStrictCharge.map
      (eqToHom
        (c60F98ObservedMixedObject_eq Z.1.1 Z.1.2 Z.2.1 Z.2.2))).charge =
      (0 : Int × Int)
  exact c60F82Quotient_eqToHom_charge_zero _

#print axioms c60F98ObservedMixedObject_eq
#print axioms c60F98ObservedMixed_naturality
#print axioms c60F98HorizontalAfterVerticalFunctor
#print axioms c60F98VerticalAfterHorizontalFunctor
#print axioms c60F98ObservedMixedNatIso
#print axioms c60F98ObservedMixedNatIso_charge_zero

end
end KUOS.DependentOriginationC60KuuObservedMixedInterchangeV5_252
