import KUOS.DependentOriginationC60KuuTwoSidedContextCoherenceV5_254

namespace KUOS.DependentOriginationC60KuuContextualMixedInterchangeSquareV5_255

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationC60InterchangerStrictChargeQuotientV5_229
open KUOS.DependentOriginationC60NativeExchangeCongruenceQuotientV5_231
open KUOS.DependentOriginationC60NativeQuotientHorizontalTensorV5_234
open KUOS.DependentOriginationC60QuotientTensorNaturalityV5_236
open KUOS.DependentOriginationC60KuuLocalUniversalDescentV5_249
open KUOS.DependentOriginationC60KuuLocalHorizontalFunctorV5_250
open KUOS.DependentOriginationC60KuuLocalVerticalFunctorV5_251
open KUOS.DependentOriginationC60KuuObservedMixedInterchangeV5_252
open KUOS.DependentOriginationC60KuuContextWhiskeringDescentV5_253
open KUOS.DependentOriginationC60KuuTwoSidedContextCoherenceV5_254

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.255 / F101 — genuine contextual four-input interchange and coherence square

F98 proves the observed H-after-V / V-after-H interchange on four
independently typed original local C60 quotient inputs.
F99 supplies ACTUAL left/right path whiskering of each local Kuu Hom.
F100 establishes two-sided contextual order independence after F77
observation, NOT an equality of raw original F42 presentations.

Here each of four local Hom factors is genuinely transported along
an independently selected actual C60 prefix/suffix and kept as a
Mathlib functor on its correct indexed local category. We compare
both contextualized F98 pasting orders with the original observed
pasting orders, and construct the contextual interchange itself.
The resulting natural isomorphism square commutes as actual F77
3-morphisms. Original Int × Int charges are preserved individually,
and EVERY comparison arrow has zero *additional* charge.

We do not identify raw F42 2-cell objects, restore Gray interchange,
assume F55 curvature vanishes, or infer global Čech descent.
-/

/-- Product of four ACTUAL F99 whiskering functors. The source
category and all four independent Hom sets are the genuine F95
quotients, with actual C60 prefix and suffix path indices. -/
def c60F101FourContextFunctor
    {z a b c d : IcosahedralDart}
    (prior : Quiver.Path z a)
    (p q r : Quiver.Path a b) (s t u : Quiver.Path b c)
    (suffix : Quiver.Path c d) :
    C60F98FourLocalInputs p q r s t u ⥤
      C60F98FourLocalInputs
        (prior.comp p) (prior.comp q) (prior.comp r)
        (s.comp suffix) (t.comp suffix) (u.comp suffix) where
  obj Z :=
    (((c60F99LeftWhiskerFunctor prior).obj Z.1.1,
      (c60F99LeftWhiskerFunctor prior).obj Z.1.2),
     ((c60F99RightWhiskerFunctor suffix).obj Z.2.1,
      (c60F99RightWhiskerFunctor suffix).obj Z.2.2))
  map := fun {_ _} f =>
    (((c60F99LeftWhiskerFunctor prior).map f.1.1,
      (c60F99LeftWhiskerFunctor prior).map f.1.2),
     ((c60F99RightWhiskerFunctor suffix).map f.2.1,
      (c60F99RightWhiskerFunctor suffix).map f.2.2))
  map_id := by
    intro Z
    apply Prod.ext
    · apply Prod.ext <;> simp
    · apply Prod.ext <;> simp
  map_comp := by
    intro X Y Z f g
    apply Prod.ext
    · apply Prod.ext <;> simp
    · apply Prod.ext <;> simp

/-- Contextualized horizontal-after-vertical F98 observation,
with no direct identification of its source F42 composites. -/
def c60F101ContextHV
    {z a b c d : IcosahedralDart}
    (prior : Quiver.Path z a)
    (p q r : Quiver.Path a b) (s t u : Quiver.Path b c)
    (suffix : Quiver.Path c d) :
    C60F98FourLocalInputs p q r s t u ⥤ C60F77NativeQuotient :=
  c60F101FourContextFunctor prior p q r s t u suffix ⋙
    c60F98HorizontalAfterVerticalFunctor
      (prior.comp p) (prior.comp q) (prior.comp r)
      (s.comp suffix) (t.comp suffix) (u.comp suffix)

/-- Contextualized vertical-after-horizontal F98 observation. -/
def c60F101ContextVH
    {z a b c d : IcosahedralDart}
    (prior : Quiver.Path z a)
    (p q r : Quiver.Path a b) (s t u : Quiver.Path b c)
    (suffix : Quiver.Path c d) :
    C60F98FourLocalInputs p q r s t u ⥤ C60F77NativeQuotient :=
  c60F101FourContextFunctor prior p q r s t u suffix ⋙
    c60F98VerticalAfterHorizontalFunctor
      (prior.comp p) (prior.comp q) (prior.comp r)
      (s.comp suffix) (t.comp suffix) (u.comp suffix)

/-- Outer C60 context does not change the ORIGINAL observed
horizontal-after-vertical F77 object, for any four raw F42
presentations retained as different local quotient objects. -/
theorem c60F101ContextHV_object_eq
    {z a b c d : IcosahedralDart}
    (prior : Quiver.Path z a)
    (p q r : Quiver.Path a b) (s t u : Quiver.Path b c)
    (suffix : Quiver.Path c d)
    (Z : C60F98FourLocalInputs p q r s t u) :
    (c60F101ContextHV prior p q r s t u suffix).obj Z =
      (c60F98HorizontalAfterVerticalFunctor p q r s t u).obj Z := by
  change
    c60F98HorizontalAfterVerticalObj
      ((c60F99LeftWhiskerFunctor prior).obj Z.1.1)
      ((c60F99LeftWhiskerFunctor prior).obj Z.1.2)
      ((c60F99RightWhiskerFunctor suffix).obj Z.2.1)
      ((c60F99RightWhiskerFunctor suffix).obj Z.2.2) =
    c60F98HorizontalAfterVerticalObj Z.1.1 Z.1.2 Z.2.1 Z.2.2
  unfold c60F98HorizontalAfterVerticalObj
  simp only [c60F96HorizontalObj_toF77, c60F97VerticalObj_toF77,
    c60F99LeftWhisker_object_obs, c60F99RightWhisker_object_obs]

/-- The independent contextual vertical-after-horizontal
observation preserves the same F77 objects. -/
theorem c60F101ContextVH_object_eq
    {z a b c d : IcosahedralDart}
    (prior : Quiver.Path z a)
    (p q r : Quiver.Path a b) (s t u : Quiver.Path b c)
    (suffix : Quiver.Path c d)
    (Z : C60F98FourLocalInputs p q r s t u) :
    (c60F101ContextVH prior p q r s t u suffix).obj Z =
      (c60F98VerticalAfterHorizontalFunctor p q r s t u).obj Z := by
  change
    c60F98VerticalAfterHorizontalObj
      ((c60F99LeftWhiskerFunctor prior).obj Z.1.1)
      ((c60F99LeftWhiskerFunctor prior).obj Z.1.2)
      ((c60F99RightWhiskerFunctor suffix).obj Z.2.1)
      ((c60F99RightWhiskerFunctor suffix).obj Z.2.2) =
    c60F98VerticalAfterHorizontalObj Z.1.1 Z.1.2 Z.2.1 Z.2.2
  unfold c60F98VerticalAfterHorizontalObj
  simp only [c60F97VerticalObj_toF77, c60F96HorizontalObj_toF77,
    c60F99LeftWhisker_object_obs, c60F99RightWhisker_object_obs]

/-- Both integer charges for each of FOUR arbitrary quotient 3-Homs
are independently preserved through contextual H-after-V pasting. -/
theorem c60F101ContextHV_charge_eq
    {z a b c d : IcosahedralDart}
    (prior : Quiver.Path z a)
    (p q r : Quiver.Path a b) (s t u : Quiver.Path b c)
    (suffix : Quiver.Path c d)
    {X Y : C60F98FourLocalInputs p q r s t u}
    (f : X ⟶ Y) :
    (c60F77QuotientToStrictCharge.map
      ((c60F101ContextHV prior p q r s t u suffix).map f)).charge =
      (c60F77QuotientToStrictCharge.map
        ((c60F98HorizontalAfterVerticalFunctor p q r s t u).map f)).charge := by
  change
    (c60F77QuotientToStrictCharge.map
      (c60F98HorizontalAfterVerticalMap
        ((c60F99LeftWhiskerFunctor prior).map f.1.1)
        ((c60F99LeftWhiskerFunctor prior).map f.1.2)
        ((c60F99RightWhiskerFunctor suffix).map f.2.1)
        ((c60F99RightWhiskerFunctor suffix).map f.2.2))).charge =
      (c60F77QuotientToStrictCharge.map
        (c60F98HorizontalAfterVerticalMap
          f.1.1 f.1.2 f.2.1 f.2.2)).charge
  simp only [c60F98HorizontalAfterVerticalMap_charge,
    c60F99LeftWhisker_charge_obs, c60F99RightWhisker_charge_obs]

/-- Same four independent integer charges survive the other
contextual pasting order, with the authentic F98 bracketing. -/
theorem c60F101ContextVH_charge_eq
    {z a b c d : IcosahedralDart}
    (prior : Quiver.Path z a)
    (p q r : Quiver.Path a b) (s t u : Quiver.Path b c)
    (suffix : Quiver.Path c d)
    {X Y : C60F98FourLocalInputs p q r s t u}
    (f : X ⟶ Y) :
    (c60F77QuotientToStrictCharge.map
      ((c60F101ContextVH prior p q r s t u suffix).map f)).charge =
      (c60F77QuotientToStrictCharge.map
        ((c60F98VerticalAfterHorizontalFunctor p q r s t u).map f)).charge := by
  change
    (c60F77QuotientToStrictCharge.map
      (c60F98VerticalAfterHorizontalMap
        ((c60F99LeftWhiskerFunctor prior).map f.1.1)
        ((c60F99LeftWhiskerFunctor prior).map f.1.2)
        ((c60F99RightWhiskerFunctor suffix).map f.2.1)
        ((c60F99RightWhiskerFunctor suffix).map f.2.2))).charge =
      (c60F77QuotientToStrictCharge.map
        (c60F98VerticalAfterHorizontalMap
          f.1.1 f.1.2 f.2.1 f.2.2)).charge
  simp only [c60F98VerticalAfterHorizontalMap_charge,
    c60F99LeftWhisker_charge_obs, c60F99RightWhisker_charge_obs]

/-- Genuine Mathlib natural isomorphism between contextualized and
original F98 horizontal-after-vertical observations, natural on
ALL four original F95 quotient 3-Hom factors. -/
def c60F101ContextHVToBaseNatIso
    {z a b c d : IcosahedralDart}
    (prior : Quiver.Path z a)
    (p q r : Quiver.Path a b) (s t u : Quiver.Path b c)
    (suffix : Quiver.Path c d) :
    c60F101ContextHV prior p q r s t u suffix ≅
      c60F98HorizontalAfterVerticalFunctor p q r s t u :=
  NatIso.ofComponents
    (fun Z => eqToIso (c60F101ContextHV_object_eq prior p q r s t u suffix Z))
    (by
      intro X Y f
      change
        (c60F101ContextHV prior p q r s t u suffix).map f ≫
          eqToHom (c60F101ContextHV_object_eq prior p q r s t u suffix Y) =
        eqToHom (c60F101ContextHV_object_eq prior p q r s t u suffix X) ≫
          (c60F98HorizontalAfterVerticalFunctor p q r s t u).map f
      apply c60F80QuotientThree_ext
      simp only [c60F80QuotientThree_comp_charge,
        c60F82Quotient_eqToHom_charge_zero, add_zero, zero_add]
      exact c60F101ContextHV_charge_eq prior p q r s t u suffix f)

/-- Corresponding independently established natural isomorphism
for contextualized vertical-after-horizontal pasting. -/
def c60F101ContextVHToBaseNatIso
    {z a b c d : IcosahedralDart}
    (prior : Quiver.Path z a)
    (p q r : Quiver.Path a b) (s t u : Quiver.Path b c)
    (suffix : Quiver.Path c d) :
    c60F101ContextVH prior p q r s t u suffix ≅
      c60F98VerticalAfterHorizontalFunctor p q r s t u :=
  NatIso.ofComponents
    (fun Z => eqToIso (c60F101ContextVH_object_eq prior p q r s t u suffix Z))
    (by
      intro X Y f
      change
        (c60F101ContextVH prior p q r s t u suffix).map f ≫
          eqToHom (c60F101ContextVH_object_eq prior p q r s t u suffix Y) =
        eqToHom (c60F101ContextVH_object_eq prior p q r s t u suffix X) ≫
          (c60F98VerticalAfterHorizontalFunctor p q r s t u).map f
      apply c60F80QuotientThree_ext
      simp only [c60F80QuotientThree_comp_charge,
        c60F82Quotient_eqToHom_charge_zero, add_zero, zero_add]
      exact c60F101ContextVH_charge_eq prior p q r s t u suffix f)

/-- The ORIGINAL F98 mixed interchange, evaluated on the four
genuinely contextualized F99 Hom inputs, gives an INDEPENDENT
F77 natural isomorphism between the two contextual pasting orders.
This is not defined by the subsequent commuting-square equation. -/
def c60F101ContextMixedDirectNatIso
    {z a b c d : IcosahedralDart}
    (prior : Quiver.Path z a)
    (p q r : Quiver.Path a b) (s t u : Quiver.Path b c)
    (suffix : Quiver.Path c d) :
    c60F101ContextHV prior p q r s t u suffix ≅
      c60F101ContextVH prior p q r s t u suffix :=
  NatIso.ofComponents
    (fun Z => eqToIso
      (c60F98ObservedMixedObject_eq
        ((c60F99LeftWhiskerFunctor prior).obj Z.1.1)
        ((c60F99LeftWhiskerFunctor prior).obj Z.1.2)
        ((c60F99RightWhiskerFunctor suffix).obj Z.2.1)
        ((c60F99RightWhiskerFunctor suffix).obj Z.2.2)))
    (by
      intro X Y f
      change
        c60F98HorizontalAfterVerticalMap
          ((c60F99LeftWhiskerFunctor prior).map f.1.1)
          ((c60F99LeftWhiskerFunctor prior).map f.1.2)
          ((c60F99RightWhiskerFunctor suffix).map f.2.1)
          ((c60F99RightWhiskerFunctor suffix).map f.2.2) ≫
          eqToHom (c60F98ObservedMixedObject_eq
            ((c60F99LeftWhiskerFunctor prior).obj Y.1.1)
            ((c60F99LeftWhiskerFunctor prior).obj Y.1.2)
            ((c60F99RightWhiskerFunctor suffix).obj Y.2.1)
            ((c60F99RightWhiskerFunctor suffix).obj Y.2.2)) =
        eqToHom (c60F98ObservedMixedObject_eq
            ((c60F99LeftWhiskerFunctor prior).obj X.1.1)
            ((c60F99LeftWhiskerFunctor prior).obj X.1.2)
            ((c60F99RightWhiskerFunctor suffix).obj X.2.1)
            ((c60F99RightWhiskerFunctor suffix).obj X.2.2)) ≫
          c60F98VerticalAfterHorizontalMap
            ((c60F99LeftWhiskerFunctor prior).map f.1.1)
            ((c60F99LeftWhiskerFunctor prior).map f.1.2)
            ((c60F99RightWhiskerFunctor suffix).map f.2.1)
            ((c60F99RightWhiskerFunctor suffix).map f.2.2)
      exact c60F98ObservedMixed_naturality _ _ _ _)

/-- Every component of the genuine contextual exchange NatIso
has zero additional Int × Int charge. -/
theorem c60F101ContextMixedDirectNatIso_charge_zero
    {z a b c d : IcosahedralDart}
    (prior : Quiver.Path z a)
    (p q r : Quiver.Path a b) (s t u : Quiver.Path b c)
    (suffix : Quiver.Path c d)
    (Z : C60F98FourLocalInputs p q r s t u) :
    (c60F77QuotientToStrictCharge.map
      ((c60F101ContextMixedDirectNatIso prior p q r s t u suffix).hom.app Z)).charge =
        (0 : Int × Int) := by
  change
    (c60F77QuotientToStrictCharge.map
      (eqToHom (c60F98ObservedMixedObject_eq
        ((c60F99LeftWhiskerFunctor prior).obj Z.1.1)
        ((c60F99LeftWhiskerFunctor prior).obj Z.1.2)
        ((c60F99RightWhiskerFunctor suffix).obj Z.2.1)
        ((c60F99RightWhiskerFunctor suffix).obj Z.2.2)))).charge =
      (0 : Int × Int)
  exact c60F82Quotient_eqToHom_charge_zero _

/-- The square of original F98 exchange and contextual F98
exchange COMMUTES as an equality of genuinely typed F77
three-morphisms. Its four sides are genuine Mathlib natural
isomorphisms (not mere integer labels). -/
theorem c60F101MixedSquare_component
    {z a b c d : IcosahedralDart}
    (prior : Quiver.Path z a)
    (p q r : Quiver.Path a b) (s t u : Quiver.Path b c)
    (suffix : Quiver.Path c d)
    (Z : C60F98FourLocalInputs p q r s t u) :
    (c60F101ContextHVToBaseNatIso prior p q r s t u suffix).hom.app Z ≫
        (c60F98ObservedMixedNatIso p q r s t u).hom.app Z =
      (c60F101ContextMixedDirectNatIso prior p q r s t u suffix).hom.app Z ≫
        (c60F101ContextVHToBaseNatIso prior p q r s t u suffix).hom.app Z := by
  apply c60F80QuotientThree_ext
  change
    (c60F77QuotientToStrictCharge.map
      (eqToHom (c60F101ContextHV_object_eq prior p q r s t u suffix Z) ≫
        eqToHom (c60F98ObservedMixedObject_eq Z.1.1 Z.1.2 Z.2.1 Z.2.2))).charge =
    (c60F77QuotientToStrictCharge.map
      (eqToHom (c60F98ObservedMixedObject_eq
        ((c60F99LeftWhiskerFunctor prior).obj Z.1.1)
        ((c60F99LeftWhiskerFunctor prior).obj Z.1.2)
        ((c60F99RightWhiskerFunctor suffix).obj Z.2.1)
        ((c60F99RightWhiskerFunctor suffix).obj Z.2.2)) ≫
      eqToHom (c60F101ContextVH_object_eq prior p q r s t u suffix Z))).charge
  simp only [c60F80QuotientThree_comp_charge,
    c60F82Quotient_eqToHom_charge_zero, zero_add]

/-- Stronger functor-category form: the two composition orders of
the F98/F99 contextual exchange natural transformations coincide,
so the component square holds naturally on all four quotient Hom
morphisms simultaneously. -/
theorem c60F101MixedSquare_natTrans
    {z a b c d : IcosahedralDart}
    (prior : Quiver.Path z a)
    (p q r : Quiver.Path a b) (s t u : Quiver.Path b c)
    (suffix : Quiver.Path c d) :
    (c60F101ContextHVToBaseNatIso prior p q r s t u suffix).hom ≫
        (c60F98ObservedMixedNatIso p q r s t u).hom =
      (c60F101ContextMixedDirectNatIso prior p q r s t u suffix).hom ≫
        (c60F101ContextVHToBaseNatIso prior p q r s t u suffix).hom := by
  ext Z
  exact c60F101MixedSquare_component prior p q r s t u suffix Z

#print axioms c60F101FourContextFunctor
#print axioms c60F101ContextHV_object_eq
#print axioms c60F101ContextVH_object_eq
#print axioms c60F101ContextHV_charge_eq
#print axioms c60F101ContextVH_charge_eq
#print axioms c60F101ContextHVToBaseNatIso
#print axioms c60F101ContextVHToBaseNatIso
#print axioms c60F101ContextMixedDirectNatIso
#print axioms c60F101ContextMixedDirectNatIso_charge_zero
#print axioms c60F101MixedSquare_component
#print axioms c60F101MixedSquare_natTrans

end
end KUOS.DependentOriginationC60KuuContextualMixedInterchangeSquareV5_255
