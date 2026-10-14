import KUOS.DependentOriginationC60KuuContextualMixedInterchangeSquareV5_255

namespace KUOS.DependentOriginationC60KuuFourInputDoubleContextCoherenceV5_256

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
open KUOS.DependentOriginationC60KuuContextualMixedInterchangeSquareV5_255

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.256 / F102 — actual four-input double-context / mixed-interchange coherence

Four genuinely independent original F95 local Kuu quotient Hom inputs
are given TWO path contexts each, using one actual shared intermediate
C60 path bridgeOut : b ⟶ m. The LEFT blocks are contextualized by prior
and middle; the RIGHT blocks by middle and suffix. Each factor is
computed independently in both F100 orders, left-then-right and
right-then-left, whose original F42 source presentations are DIFFERENT.

F98's horizontal-after-vertical and vertical-after-horizontal functors
yield FOUR differently contextualized functors into actual F77 Homs.
We prove natural order-exchange isomorphisms for BOTH F98 orders,
and the two original F98 mixed interchange isomorphisms after applying
the TWO independent original four-input context functors.

The F100 context-order comparisons COMMUTE with the F98 mixed exchange
as an equality of Mathlib natural transformations. All eight original
charge contributions remain conserved as the original four independent
Int × Int inputs. The comparison components carry zero ADDED charge,
not zero input charges. Nothing lifts the diagram to unquotiented F42,
restores odd/odd Gray phases, or erases the physical F55 obstruction.
-/


/-- Genuine four-input F95 context functor in left-then-right order,
with correctly typed genuine C60 source and target paths. -/
def c60F102FourLR
    {z a b m c d : IcosahedralDart}
    (prior : Quiver.Path z a)
    (p q r : Quiver.Path a b)
    (bridgeOut : Quiver.Path b m)
    (bridgeIn : Quiver.Path m b)
    (s t u : Quiver.Path b c)
    (suffix : Quiver.Path c d) :
    C60F98FourLocalInputs p q r s t u ⥤
      C60F98FourLocalInputs
        ((prior.comp p).comp bridgeOut) ((prior.comp q).comp bridgeOut) ((prior.comp r).comp bridgeOut)
        ((bridgeIn.comp s).comp suffix) ((bridgeIn.comp t).comp suffix) ((bridgeIn.comp u).comp suffix) where
  obj Z :=
    ((((c60F99RightWhiskerFunctor bridgeOut).obj ((c60F99LeftWhiskerFunctor prior).obj Z.1.1)), ((c60F99RightWhiskerFunctor bridgeOut).obj ((c60F99LeftWhiskerFunctor prior).obj Z.1.2))),
     (((c60F99RightWhiskerFunctor suffix).obj ((c60F99LeftWhiskerFunctor bridgeIn).obj Z.2.1)), ((c60F99RightWhiskerFunctor suffix).obj ((c60F99LeftWhiskerFunctor bridgeIn).obj Z.2.2))))
  map := fun {_ _} f =>
    ((((c60F99RightWhiskerFunctor bridgeOut).map ((c60F99LeftWhiskerFunctor prior).map f.1.1)), ((c60F99RightWhiskerFunctor bridgeOut).map ((c60F99LeftWhiskerFunctor prior).map f.1.2))),
     (((c60F99RightWhiskerFunctor suffix).map ((c60F99LeftWhiskerFunctor bridgeIn).map f.2.1)), ((c60F99RightWhiskerFunctor suffix).map ((c60F99LeftWhiskerFunctor bridgeIn).map f.2.2))))
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


/-- The HV F98 observation after the actual LR context order. -/
def c60F102LRHV
    {z a b m c d : IcosahedralDart}
    (prior : Quiver.Path z a)
    (p q r : Quiver.Path a b)
    (bridgeOut : Quiver.Path b m)
    (bridgeIn : Quiver.Path m b)
    (s t u : Quiver.Path b c)
    (suffix : Quiver.Path c d) :
    C60F98FourLocalInputs p q r s t u ⥤ C60F77NativeQuotient :=
  c60F102FourLR prior p q r bridgeOut bridgeIn s t u suffix ⋙
    c60F98HorizontalAfterVerticalFunctor
      ((prior.comp p).comp bridgeOut) ((prior.comp q).comp bridgeOut) ((prior.comp r).comp bridgeOut)
        ((bridgeIn.comp s).comp suffix) ((bridgeIn.comp t).comp suffix) ((bridgeIn.comp u).comp suffix)


/-- The VH F98 observation after the actual LR context order. -/
def c60F102LRVH
    {z a b m c d : IcosahedralDart}
    (prior : Quiver.Path z a)
    (p q r : Quiver.Path a b)
    (bridgeOut : Quiver.Path b m)
    (bridgeIn : Quiver.Path m b)
    (s t u : Quiver.Path b c)
    (suffix : Quiver.Path c d) :
    C60F98FourLocalInputs p q r s t u ⥤ C60F77NativeQuotient :=
  c60F102FourLR prior p q r bridgeOut bridgeIn s t u suffix ⋙
    c60F98VerticalAfterHorizontalFunctor
      ((prior.comp p).comp bridgeOut) ((prior.comp q).comp bridgeOut) ((prior.comp r).comp bridgeOut)
        ((bridgeIn.comp s).comp suffix) ((bridgeIn.comp t).comp suffix) ((bridgeIn.comp u).comp suffix)


/-- Genuine four-input F95 context functor in right-then-left order,
with correctly typed genuine C60 source and target paths. -/
def c60F102FourRL
    {z a b m c d : IcosahedralDart}
    (prior : Quiver.Path z a)
    (p q r : Quiver.Path a b)
    (bridgeOut : Quiver.Path b m)
    (bridgeIn : Quiver.Path m b)
    (s t u : Quiver.Path b c)
    (suffix : Quiver.Path c d) :
    C60F98FourLocalInputs p q r s t u ⥤
      C60F98FourLocalInputs
        (prior.comp (p.comp bridgeOut)) (prior.comp (q.comp bridgeOut)) (prior.comp (r.comp bridgeOut))
        (middle.comp (s.comp suffix)) (middle.comp (t.comp suffix)) (middle.comp (u.comp suffix)) where
  obj Z :=
    ((((c60F99LeftWhiskerFunctor prior).obj ((c60F99RightWhiskerFunctor bridgeOut).obj Z.1.1)), ((c60F99LeftWhiskerFunctor prior).obj ((c60F99RightWhiskerFunctor bridgeOut).obj Z.1.2))),
     (((c60F99LeftWhiskerFunctor bridgeIn).obj ((c60F99RightWhiskerFunctor suffix).obj Z.2.1)), ((c60F99LeftWhiskerFunctor bridgeIn).obj ((c60F99RightWhiskerFunctor suffix).obj Z.2.2))))
  map := fun {_ _} f =>
    ((((c60F99LeftWhiskerFunctor prior).map ((c60F99RightWhiskerFunctor bridgeOut).map f.1.1)), ((c60F99LeftWhiskerFunctor prior).map ((c60F99RightWhiskerFunctor bridgeOut).map f.1.2))),
     (((c60F99LeftWhiskerFunctor bridgeIn).map ((c60F99RightWhiskerFunctor suffix).map f.2.1)), ((c60F99LeftWhiskerFunctor bridgeIn).map ((c60F99RightWhiskerFunctor suffix).map f.2.2))))
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


/-- The HV F98 observation after the actual RL context order. -/
def c60F102RLHV
    {z a b m c d : IcosahedralDart}
    (prior : Quiver.Path z a)
    (p q r : Quiver.Path a b)
    (bridgeOut : Quiver.Path b m)
    (bridgeIn : Quiver.Path m b)
    (s t u : Quiver.Path b c)
    (suffix : Quiver.Path c d) :
    C60F98FourLocalInputs p q r s t u ⥤ C60F77NativeQuotient :=
  c60F102FourRL prior p q r bridgeOut bridgeIn s t u suffix ⋙
    c60F98HorizontalAfterVerticalFunctor
      (prior.comp (p.comp bridgeOut)) (prior.comp (q.comp bridgeOut)) (prior.comp (r.comp bridgeOut))
        (middle.comp (s.comp suffix)) (middle.comp (t.comp suffix)) (middle.comp (u.comp suffix))


/-- The VH F98 observation after the actual RL context order. -/
def c60F102RLVH
    {z a b m c d : IcosahedralDart}
    (prior : Quiver.Path z a)
    (p q r : Quiver.Path a b)
    (bridgeOut : Quiver.Path b m)
    (bridgeIn : Quiver.Path m b)
    (s t u : Quiver.Path b c)
    (suffix : Quiver.Path c d) :
    C60F98FourLocalInputs p q r s t u ⥤ C60F77NativeQuotient :=
  c60F102FourRL prior p q r bridgeOut bridgeIn s t u suffix ⋙
    c60F98VerticalAfterHorizontalFunctor
      (prior.comp (p.comp bridgeOut)) (prior.comp (q.comp bridgeOut)) (prior.comp (r.comp bridgeOut))
        (middle.comp (s.comp suffix)) (middle.comp (t.comp suffix)) (middle.comp (u.comp suffix))


/-- The two independent F100 context orders have equal observed HV
F77 objects for EACH four-input original C60 tuple, not equal F42 raw syntax. -/
theorem c60F102HVOrder_object_eq
    {z a b m c d : IcosahedralDart}
    (prior : Quiver.Path z a)
    (p q r : Quiver.Path a b)
    (bridgeOut : Quiver.Path b m)
    (bridgeIn : Quiver.Path m b)
    (s t u : Quiver.Path b c)
    (suffix : Quiver.Path c d)
    (Z : C60F98FourLocalInputs p q r s t u) :
    (c60F102LRHV prior p q r bridgeOut bridgeIn s t u suffix).obj Z =
      (c60F102RLHV prior p q r bridgeOut bridgeIn s t u suffix).obj Z := by
  change
    c60F98HorizontalAfterVerticalObj
      ((c60F99RightWhiskerFunctor bridgeOut).obj ((c60F99LeftWhiskerFunctor prior).obj Z.1.1))
      ((c60F99RightWhiskerFunctor bridgeOut).obj ((c60F99LeftWhiskerFunctor prior).obj Z.1.2))
      ((c60F99RightWhiskerFunctor suffix).obj ((c60F99LeftWhiskerFunctor bridgeIn).obj Z.2.1))
      ((c60F99RightWhiskerFunctor suffix).obj ((c60F99LeftWhiskerFunctor bridgeIn).obj Z.2.2)) =
    c60F98HorizontalAfterVerticalObj
      ((c60F99LeftWhiskerFunctor prior).obj ((c60F99RightWhiskerFunctor bridgeOut).obj Z.1.1))
      ((c60F99LeftWhiskerFunctor prior).obj ((c60F99RightWhiskerFunctor bridgeOut).obj Z.1.2))
      ((c60F99LeftWhiskerFunctor bridgeIn).obj ((c60F99RightWhiskerFunctor suffix).obj Z.2.1))
      ((c60F99LeftWhiskerFunctor bridgeIn).obj ((c60F99RightWhiskerFunctor suffix).obj Z.2.2))
  unfold c60F98HorizontalAfterVerticalObj
  simp only [c60F96HorizontalObj_toF77, c60F97VerticalObj_toF77]
  change
    (c60F80QuotientTwoTensor
         (c60F80QuotientTwoTensor
         ((c60F100LeftRightObserved prior bridgeOut).obj Z.1.1)
         ((c60F100LeftRightObserved prior bridgeOut).obj Z.1.2))
         (c60F80QuotientTwoTensor
         ((c60F100LeftRightObserved bridgeIn suffix).obj Z.2.1)
         ((c60F100LeftRightObserved bridgeIn suffix).obj Z.2.2))) =
    (c60F80QuotientTwoTensor
         (c60F80QuotientTwoTensor
         ((c60F100RightLeftObserved prior bridgeOut).obj Z.1.1)
         ((c60F100RightLeftObserved prior bridgeOut).obj Z.1.2))
         (c60F80QuotientTwoTensor
         ((c60F100RightLeftObserved bridgeIn suffix).obj Z.2.1)
         ((c60F100RightLeftObserved bridgeIn suffix).obj Z.2.2)))
  rw [c60F100ObservedObject_eq prior bridgeOut Z.1.1,
      c60F100ObservedObject_eq prior bridgeOut Z.1.2,
      c60F100ObservedObject_eq bridgeIn suffix Z.2.1,
      c60F100ObservedObject_eq bridgeIn suffix Z.2.2]


/-- Both original charge coordinates of EVERY F95 3-Hom are
unchanged when the order of all four F100 contexts is swapped
inside the actual F98 HV pasting functor. -/
theorem c60F102HVOrder_charge_eq
    {z a b m c d : IcosahedralDart}
    (prior : Quiver.Path z a)
    (p q r : Quiver.Path a b)
    (bridgeOut : Quiver.Path b m)
    (bridgeIn : Quiver.Path m b)
    (s t u : Quiver.Path b c)
    (suffix : Quiver.Path c d)
    {X Y : C60F98FourLocalInputs p q r s t u} (f : X ⟶ Y) :
    (c60F77QuotientToStrictCharge.map
      ((c60F102LRHV prior p q r bridgeOut bridgeIn s t u suffix).map f)).charge =
      (c60F77QuotientToStrictCharge.map
        ((c60F102RLHV prior p q r bridgeOut bridgeIn s t u suffix).map f)).charge := by
  change
    (c60F77QuotientToStrictCharge.map
      (c60F98HorizontalAfterVerticalMap
        ((c60F99RightWhiskerFunctor bridgeOut).map ((c60F99LeftWhiskerFunctor prior).map f.1.1))
        ((c60F99RightWhiskerFunctor bridgeOut).map ((c60F99LeftWhiskerFunctor prior).map f.1.2))
        ((c60F99RightWhiskerFunctor suffix).map ((c60F99LeftWhiskerFunctor bridgeIn).map f.2.1))
        ((c60F99RightWhiskerFunctor suffix).map ((c60F99LeftWhiskerFunctor bridgeIn).map f.2.2)))).charge =
    (c60F77QuotientToStrictCharge.map
      (c60F98HorizontalAfterVerticalMap
        ((c60F99LeftWhiskerFunctor prior).map ((c60F99RightWhiskerFunctor bridgeOut).map f.1.1))
        ((c60F99LeftWhiskerFunctor prior).map ((c60F99RightWhiskerFunctor bridgeOut).map f.1.2))
        ((c60F99LeftWhiskerFunctor bridgeIn).map ((c60F99RightWhiskerFunctor suffix).map f.2.1))
        ((c60F99LeftWhiskerFunctor bridgeIn).map ((c60F99RightWhiskerFunctor suffix).map f.2.2)))).charge
  simp only [c60F98HorizontalAfterVerticalMap_charge]
  change
    (((c60F77QuotientToStrictCharge.map
          ((c60F100LeftRightObserved prior bridgeOut).map f.1.1)).charge + (c60F77QuotientToStrictCharge.map
          ((c60F100LeftRightObserved prior bridgeOut).map f.1.2)).charge) +
      ((c60F77QuotientToStrictCharge.map
          ((c60F100LeftRightObserved bridgeIn suffix).map f.2.1)).charge + (c60F77QuotientToStrictCharge.map
          ((c60F100LeftRightObserved bridgeIn suffix).map f.2.2)).charge)) =
    (((c60F77QuotientToStrictCharge.map
          ((c60F100RightLeftObserved prior bridgeOut).map f.1.1)).charge + (c60F77QuotientToStrictCharge.map
          ((c60F100RightLeftObserved prior bridgeOut).map f.1.2)).charge) +
      ((c60F77QuotientToStrictCharge.map
          ((c60F100RightLeftObserved bridgeIn suffix).map f.2.1)).charge + (c60F77QuotientToStrictCharge.map
          ((c60F100RightLeftObserved bridgeIn suffix).map f.2.2)).charge))
  rw [c60F100LeftRight_charge_obs prior bridgeOut f.1.1,
      c60F100LeftRight_charge_obs prior bridgeOut f.1.2,
      c60F100LeftRight_charge_obs bridgeIn suffix f.2.1,
      c60F100LeftRight_charge_obs bridgeIn suffix f.2.2,
      c60F100RightLeft_charge_obs prior bridgeOut f.1.1,
      c60F100RightLeft_charge_obs prior bridgeOut f.1.2,
      c60F100RightLeft_charge_obs bridgeIn suffix f.2.1,
      c60F100RightLeft_charge_obs bridgeIn suffix f.2.2]


/-- Genuine Mathlib F77 natural isomorphism for all HV double-
context Hom arrows, not merely a charge-level correspondence. -/
def c60F102HVOrderNatIso
    {z a b m c d : IcosahedralDart}
    (prior : Quiver.Path z a)
    (p q r : Quiver.Path a b)
    (bridgeOut : Quiver.Path b m)
    (bridgeIn : Quiver.Path m b)
    (s t u : Quiver.Path b c)
    (suffix : Quiver.Path c d) :
    c60F102LRHV prior p q r bridgeOut bridgeIn s t u suffix ≅
      c60F102RLHV prior p q r bridgeOut bridgeIn s t u suffix :=
  NatIso.ofComponents
    (fun Z => eqToIso (c60F102HVOrder_object_eq prior p q r bridgeOut bridgeIn s t u suffix Z))
    (by
      intro X Y f
      change
        (c60F102LRHV prior p q r bridgeOut bridgeIn s t u suffix).map f ≫
          eqToHom (c60F102HVOrder_object_eq prior p q r bridgeOut bridgeIn s t u suffix Y) =
        eqToHom (c60F102HVOrder_object_eq prior p q r bridgeOut bridgeIn s t u suffix X) ≫
          (c60F102RLHV prior p q r bridgeOut bridgeIn s t u suffix).map f
      apply c60F80QuotientThree_ext
      simp only [c60F80QuotientThree_comp_charge,
        c60F82Quotient_eqToHom_charge_zero, add_zero, zero_add]
      exact c60F102HVOrder_charge_eq prior p q r bridgeOut bridgeIn s t u suffix f)


/-- The two independent F100 context orders have equal observed VH
F77 objects for EACH four-input original C60 tuple, not equal F42 raw syntax. -/
theorem c60F102VHOrder_object_eq
    {z a b m c d : IcosahedralDart}
    (prior : Quiver.Path z a)
    (p q r : Quiver.Path a b)
    (bridgeOut : Quiver.Path b m)
    (bridgeIn : Quiver.Path m b)
    (s t u : Quiver.Path b c)
    (suffix : Quiver.Path c d)
    (Z : C60F98FourLocalInputs p q r s t u) :
    (c60F102LRVH prior p q r bridgeOut bridgeIn s t u suffix).obj Z =
      (c60F102RLVH prior p q r bridgeOut bridgeIn s t u suffix).obj Z := by
  change
    c60F98VerticalAfterHorizontalObj
      ((c60F99RightWhiskerFunctor bridgeOut).obj ((c60F99LeftWhiskerFunctor prior).obj Z.1.1))
      ((c60F99RightWhiskerFunctor bridgeOut).obj ((c60F99LeftWhiskerFunctor prior).obj Z.1.2))
      ((c60F99RightWhiskerFunctor suffix).obj ((c60F99LeftWhiskerFunctor bridgeIn).obj Z.2.1))
      ((c60F99RightWhiskerFunctor suffix).obj ((c60F99LeftWhiskerFunctor bridgeIn).obj Z.2.2)) =
    c60F98VerticalAfterHorizontalObj
      ((c60F99LeftWhiskerFunctor prior).obj ((c60F99RightWhiskerFunctor bridgeOut).obj Z.1.1))
      ((c60F99LeftWhiskerFunctor prior).obj ((c60F99RightWhiskerFunctor bridgeOut).obj Z.1.2))
      ((c60F99LeftWhiskerFunctor bridgeIn).obj ((c60F99RightWhiskerFunctor suffix).obj Z.2.1))
      ((c60F99LeftWhiskerFunctor bridgeIn).obj ((c60F99RightWhiskerFunctor suffix).obj Z.2.2))
  unfold c60F98VerticalAfterHorizontalObj
  simp only [c60F96HorizontalObj_toF77, c60F97VerticalObj_toF77]
  change
    (c60F80QuotientTwoTensor
         (c60F80QuotientTwoTensor
         ((c60F100LeftRightObserved prior bridgeOut).obj Z.1.1)
         ((c60F100LeftRightObserved bridgeIn suffix).obj Z.2.1))
         (c60F80QuotientTwoTensor
         ((c60F100LeftRightObserved prior bridgeOut).obj Z.1.2)
         ((c60F100LeftRightObserved bridgeIn suffix).obj Z.2.2))) =
    (c60F80QuotientTwoTensor
         (c60F80QuotientTwoTensor
         ((c60F100RightLeftObserved prior bridgeOut).obj Z.1.1)
         ((c60F100RightLeftObserved bridgeIn suffix).obj Z.2.1))
         (c60F80QuotientTwoTensor
         ((c60F100RightLeftObserved prior bridgeOut).obj Z.1.2)
         ((c60F100RightLeftObserved bridgeIn suffix).obj Z.2.2)))
  rw [c60F100ObservedObject_eq prior bridgeOut Z.1.1,
      c60F100ObservedObject_eq prior bridgeOut Z.1.2,
      c60F100ObservedObject_eq bridgeIn suffix Z.2.1,
      c60F100ObservedObject_eq bridgeIn suffix Z.2.2]


/-- Both original charge coordinates of EVERY F95 3-Hom are
unchanged when the order of all four F100 contexts is swapped
inside the actual F98 VH pasting functor. -/
theorem c60F102VHOrder_charge_eq
    {z a b m c d : IcosahedralDart}
    (prior : Quiver.Path z a)
    (p q r : Quiver.Path a b)
    (bridgeOut : Quiver.Path b m)
    (bridgeIn : Quiver.Path m b)
    (s t u : Quiver.Path b c)
    (suffix : Quiver.Path c d)
    {X Y : C60F98FourLocalInputs p q r s t u} (f : X ⟶ Y) :
    (c60F77QuotientToStrictCharge.map
      ((c60F102LRVH prior p q r bridgeOut bridgeIn s t u suffix).map f)).charge =
      (c60F77QuotientToStrictCharge.map
        ((c60F102RLVH prior p q r bridgeOut bridgeIn s t u suffix).map f)).charge := by
  change
    (c60F77QuotientToStrictCharge.map
      (c60F98VerticalAfterHorizontalMap
        ((c60F99RightWhiskerFunctor bridgeOut).map ((c60F99LeftWhiskerFunctor prior).map f.1.1))
        ((c60F99RightWhiskerFunctor bridgeOut).map ((c60F99LeftWhiskerFunctor prior).map f.1.2))
        ((c60F99RightWhiskerFunctor suffix).map ((c60F99LeftWhiskerFunctor bridgeIn).map f.2.1))
        ((c60F99RightWhiskerFunctor suffix).map ((c60F99LeftWhiskerFunctor bridgeIn).map f.2.2)))).charge =
    (c60F77QuotientToStrictCharge.map
      (c60F98VerticalAfterHorizontalMap
        ((c60F99LeftWhiskerFunctor prior).map ((c60F99RightWhiskerFunctor bridgeOut).map f.1.1))
        ((c60F99LeftWhiskerFunctor prior).map ((c60F99RightWhiskerFunctor bridgeOut).map f.1.2))
        ((c60F99LeftWhiskerFunctor bridgeIn).map ((c60F99RightWhiskerFunctor suffix).map f.2.1))
        ((c60F99LeftWhiskerFunctor bridgeIn).map ((c60F99RightWhiskerFunctor suffix).map f.2.2)))).charge
  simp only [c60F98VerticalAfterHorizontalMap_charge]
  change
    (((c60F77QuotientToStrictCharge.map
          ((c60F100LeftRightObserved prior bridgeOut).map f.1.1)).charge + (c60F77QuotientToStrictCharge.map
          ((c60F100LeftRightObserved bridgeIn suffix).map f.2.1)).charge) +
      ((c60F77QuotientToStrictCharge.map
          ((c60F100LeftRightObserved prior bridgeOut).map f.1.2)).charge + (c60F77QuotientToStrictCharge.map
          ((c60F100LeftRightObserved bridgeIn suffix).map f.2.2)).charge)) =
    (((c60F77QuotientToStrictCharge.map
          ((c60F100RightLeftObserved prior bridgeOut).map f.1.1)).charge + (c60F77QuotientToStrictCharge.map
          ((c60F100RightLeftObserved bridgeIn suffix).map f.2.1)).charge) +
      ((c60F77QuotientToStrictCharge.map
          ((c60F100RightLeftObserved prior bridgeOut).map f.1.2)).charge + (c60F77QuotientToStrictCharge.map
          ((c60F100RightLeftObserved bridgeIn suffix).map f.2.2)).charge))
  rw [c60F100LeftRight_charge_obs prior bridgeOut f.1.1,
      c60F100LeftRight_charge_obs prior bridgeOut f.1.2,
      c60F100LeftRight_charge_obs bridgeIn suffix f.2.1,
      c60F100LeftRight_charge_obs bridgeIn suffix f.2.2,
      c60F100RightLeft_charge_obs prior bridgeOut f.1.1,
      c60F100RightLeft_charge_obs prior bridgeOut f.1.2,
      c60F100RightLeft_charge_obs bridgeIn suffix f.2.1,
      c60F100RightLeft_charge_obs bridgeIn suffix f.2.2]


/-- Genuine Mathlib F77 natural isomorphism for all VH double-
context Hom arrows, not merely a charge-level correspondence. -/
def c60F102VHOrderNatIso
    {z a b m c d : IcosahedralDart}
    (prior : Quiver.Path z a)
    (p q r : Quiver.Path a b)
    (bridgeOut : Quiver.Path b m)
    (bridgeIn : Quiver.Path m b)
    (s t u : Quiver.Path b c)
    (suffix : Quiver.Path c d) :
    c60F102LRVH prior p q r bridgeOut bridgeIn s t u suffix ≅
      c60F102RLVH prior p q r bridgeOut bridgeIn s t u suffix :=
  NatIso.ofComponents
    (fun Z => eqToIso (c60F102VHOrder_object_eq prior p q r bridgeOut bridgeIn s t u suffix Z))
    (by
      intro X Y f
      change
        (c60F102LRVH prior p q r bridgeOut bridgeIn s t u suffix).map f ≫
          eqToHom (c60F102VHOrder_object_eq prior p q r bridgeOut bridgeIn s t u suffix Y) =
        eqToHom (c60F102VHOrder_object_eq prior p q r bridgeOut bridgeIn s t u suffix X) ≫
          (c60F102RLVH prior p q r bridgeOut bridgeIn s t u suffix).map f
      apply c60F80QuotientThree_ext
      simp only [c60F80QuotientThree_comp_charge,
        c60F82Quotient_eqToHom_charge_zero, add_zero, zero_add]
      exact c60F102VHOrder_charge_eq prior p q r bridgeOut bridgeIn s t u suffix f)


/-- The original F98 mixed interchange naturally acts after
all four independently context-whiskered F100 LR inputs. -/
def c60F102LRMixedNatIso
    {z a b m c d : IcosahedralDart}
    (prior : Quiver.Path z a)
    (p q r : Quiver.Path a b)
    (bridgeOut : Quiver.Path b m)
    (bridgeIn : Quiver.Path m b)
    (s t u : Quiver.Path b c)
    (suffix : Quiver.Path c d) :
    c60F102LRHV prior p q r bridgeOut bridgeIn s t u suffix ≅
      c60F102LRVH prior p q r bridgeOut bridgeIn s t u suffix :=
  NatIso.ofComponents
    (fun Z => eqToIso
      (c60F98ObservedMixedObject_eq
        ((c60F99RightWhiskerFunctor bridgeOut).obj ((c60F99LeftWhiskerFunctor prior).obj Z.1.1))
        ((c60F99RightWhiskerFunctor bridgeOut).obj ((c60F99LeftWhiskerFunctor prior).obj Z.1.2))
        ((c60F99RightWhiskerFunctor suffix).obj ((c60F99LeftWhiskerFunctor bridgeIn).obj Z.2.1))
        ((c60F99RightWhiskerFunctor suffix).obj ((c60F99LeftWhiskerFunctor bridgeIn).obj Z.2.2))))
    (by
      intro X Y f
      change
        c60F98HorizontalAfterVerticalMap
          ((c60F99RightWhiskerFunctor bridgeOut).map ((c60F99LeftWhiskerFunctor prior).map f.1.1))
          ((c60F99RightWhiskerFunctor bridgeOut).map ((c60F99LeftWhiskerFunctor prior).map f.1.2))
          ((c60F99RightWhiskerFunctor suffix).map ((c60F99LeftWhiskerFunctor bridgeIn).map f.2.1))
          ((c60F99RightWhiskerFunctor suffix).map ((c60F99LeftWhiskerFunctor bridgeIn).map f.2.2)) ≫
          eqToHom (c60F98ObservedMixedObject_eq
          ((c60F99RightWhiskerFunctor bridgeOut).obj ((c60F99LeftWhiskerFunctor prior).obj Y.1.1))
          ((c60F99RightWhiskerFunctor bridgeOut).obj ((c60F99LeftWhiskerFunctor prior).obj Y.1.2))
          ((c60F99RightWhiskerFunctor suffix).obj ((c60F99LeftWhiskerFunctor bridgeIn).obj Y.2.1))
          ((c60F99RightWhiskerFunctor suffix).obj ((c60F99LeftWhiskerFunctor bridgeIn).obj Y.2.2))) =
        eqToHom (c60F98ObservedMixedObject_eq
          ((c60F99RightWhiskerFunctor bridgeOut).obj ((c60F99LeftWhiskerFunctor prior).obj X.1.1))
          ((c60F99RightWhiskerFunctor bridgeOut).obj ((c60F99LeftWhiskerFunctor prior).obj X.1.2))
          ((c60F99RightWhiskerFunctor suffix).obj ((c60F99LeftWhiskerFunctor bridgeIn).obj X.2.1))
          ((c60F99RightWhiskerFunctor suffix).obj ((c60F99LeftWhiskerFunctor bridgeIn).obj X.2.2))) ≫
          c60F98VerticalAfterHorizontalMap
            ((c60F99RightWhiskerFunctor bridgeOut).map ((c60F99LeftWhiskerFunctor prior).map f.1.1))
            ((c60F99RightWhiskerFunctor bridgeOut).map ((c60F99LeftWhiskerFunctor prior).map f.1.2))
            ((c60F99RightWhiskerFunctor suffix).map ((c60F99LeftWhiskerFunctor bridgeIn).map f.2.1))
            ((c60F99RightWhiskerFunctor suffix).map ((c60F99LeftWhiskerFunctor bridgeIn).map f.2.2))
      exact c60F98ObservedMixed_naturality _ _ _ _)

/-- The LR contextual mixed-exchange comparison itself has
zero ADDITIONAL Int × Int charge on every original 4-input tuple. -/
theorem c60F102LRMixedNatIso_charge_zero
    {z a b m c d : IcosahedralDart}
    (prior : Quiver.Path z a)
    (p q r : Quiver.Path a b)
    (bridgeOut : Quiver.Path b m)
    (bridgeIn : Quiver.Path m b)
    (s t u : Quiver.Path b c)
    (suffix : Quiver.Path c d) (Z : C60F98FourLocalInputs p q r s t u) :
    (c60F77QuotientToStrictCharge.map
      ((c60F102LRMixedNatIso prior p q r bridgeOut bridgeIn s t u suffix).hom.app Z)).charge =
      (0 : Int × Int) := by
  change
    (c60F77QuotientToStrictCharge.map
      (eqToHom (c60F98ObservedMixedObject_eq
        ((c60F99RightWhiskerFunctor bridgeOut).obj ((c60F99LeftWhiskerFunctor prior).obj Z.1.1))
        ((c60F99RightWhiskerFunctor bridgeOut).obj ((c60F99LeftWhiskerFunctor prior).obj Z.1.2))
        ((c60F99RightWhiskerFunctor suffix).obj ((c60F99LeftWhiskerFunctor bridgeIn).obj Z.2.1))
        ((c60F99RightWhiskerFunctor suffix).obj ((c60F99LeftWhiskerFunctor bridgeIn).obj Z.2.2))))).charge = (0 : Int × Int)
  exact c60F82Quotient_eqToHom_charge_zero _


/-- The original F98 mixed interchange naturally acts after
all four independently context-whiskered F100 RL inputs. -/
def c60F102RLMixedNatIso
    {z a b m c d : IcosahedralDart}
    (prior : Quiver.Path z a)
    (p q r : Quiver.Path a b)
    (bridgeOut : Quiver.Path b m)
    (bridgeIn : Quiver.Path m b)
    (s t u : Quiver.Path b c)
    (suffix : Quiver.Path c d) :
    c60F102RLHV prior p q r bridgeOut bridgeIn s t u suffix ≅
      c60F102RLVH prior p q r bridgeOut bridgeIn s t u suffix :=
  NatIso.ofComponents
    (fun Z => eqToIso
      (c60F98ObservedMixedObject_eq
        ((c60F99LeftWhiskerFunctor prior).obj ((c60F99RightWhiskerFunctor bridgeOut).obj Z.1.1))
        ((c60F99LeftWhiskerFunctor prior).obj ((c60F99RightWhiskerFunctor bridgeOut).obj Z.1.2))
        ((c60F99LeftWhiskerFunctor bridgeIn).obj ((c60F99RightWhiskerFunctor suffix).obj Z.2.1))
        ((c60F99LeftWhiskerFunctor bridgeIn).obj ((c60F99RightWhiskerFunctor suffix).obj Z.2.2))))
    (by
      intro X Y f
      change
        c60F98HorizontalAfterVerticalMap
          ((c60F99LeftWhiskerFunctor prior).map ((c60F99RightWhiskerFunctor bridgeOut).map f.1.1))
          ((c60F99LeftWhiskerFunctor prior).map ((c60F99RightWhiskerFunctor bridgeOut).map f.1.2))
          ((c60F99LeftWhiskerFunctor bridgeIn).map ((c60F99RightWhiskerFunctor suffix).map f.2.1))
          ((c60F99LeftWhiskerFunctor bridgeIn).map ((c60F99RightWhiskerFunctor suffix).map f.2.2)) ≫
          eqToHom (c60F98ObservedMixedObject_eq
          ((c60F99LeftWhiskerFunctor prior).obj ((c60F99RightWhiskerFunctor bridgeOut).obj Y.1.1))
          ((c60F99LeftWhiskerFunctor prior).obj ((c60F99RightWhiskerFunctor bridgeOut).obj Y.1.2))
          ((c60F99LeftWhiskerFunctor bridgeIn).obj ((c60F99RightWhiskerFunctor suffix).obj Y.2.1))
          ((c60F99LeftWhiskerFunctor bridgeIn).obj ((c60F99RightWhiskerFunctor suffix).obj Y.2.2))) =
        eqToHom (c60F98ObservedMixedObject_eq
          ((c60F99LeftWhiskerFunctor prior).obj ((c60F99RightWhiskerFunctor bridgeOut).obj X.1.1))
          ((c60F99LeftWhiskerFunctor prior).obj ((c60F99RightWhiskerFunctor bridgeOut).obj X.1.2))
          ((c60F99LeftWhiskerFunctor bridgeIn).obj ((c60F99RightWhiskerFunctor suffix).obj X.2.1))
          ((c60F99LeftWhiskerFunctor bridgeIn).obj ((c60F99RightWhiskerFunctor suffix).obj X.2.2))) ≫
          c60F98VerticalAfterHorizontalMap
            ((c60F99LeftWhiskerFunctor prior).map ((c60F99RightWhiskerFunctor bridgeOut).map f.1.1))
            ((c60F99LeftWhiskerFunctor prior).map ((c60F99RightWhiskerFunctor bridgeOut).map f.1.2))
            ((c60F99LeftWhiskerFunctor bridgeIn).map ((c60F99RightWhiskerFunctor suffix).map f.2.1))
            ((c60F99LeftWhiskerFunctor bridgeIn).map ((c60F99RightWhiskerFunctor suffix).map f.2.2))
      exact c60F98ObservedMixed_naturality _ _ _ _)

/-- The RL contextual mixed-exchange comparison itself has
zero ADDITIONAL Int × Int charge on every original 4-input tuple. -/
theorem c60F102RLMixedNatIso_charge_zero
    {z a b m c d : IcosahedralDart}
    (prior : Quiver.Path z a)
    (p q r : Quiver.Path a b)
    (bridgeOut : Quiver.Path b m)
    (bridgeIn : Quiver.Path m b)
    (s t u : Quiver.Path b c)
    (suffix : Quiver.Path c d) (Z : C60F98FourLocalInputs p q r s t u) :
    (c60F77QuotientToStrictCharge.map
      ((c60F102RLMixedNatIso prior p q r bridgeOut bridgeIn s t u suffix).hom.app Z)).charge =
      (0 : Int × Int) := by
  change
    (c60F77QuotientToStrictCharge.map
      (eqToHom (c60F98ObservedMixedObject_eq
        ((c60F99LeftWhiskerFunctor prior).obj ((c60F99RightWhiskerFunctor bridgeOut).obj Z.1.1))
        ((c60F99LeftWhiskerFunctor prior).obj ((c60F99RightWhiskerFunctor bridgeOut).obj Z.1.2))
        ((c60F99LeftWhiskerFunctor bridgeIn).obj ((c60F99RightWhiskerFunctor suffix).obj Z.2.1))
        ((c60F99LeftWhiskerFunctor bridgeIn).obj ((c60F99RightWhiskerFunctor suffix).obj Z.2.2))))).charge = (0 : Int × Int)
  exact c60F82Quotient_eqToHom_charge_zero _


/-- The F100 order-change square and the two F98 mixed exchanges
COMMUTE as actual F77 quotient three-arrows for arbitrary C60
four-input objects, while retaining original physical curvature. -/
theorem c60F102OrderMixedSquare_component
    {z a b m c d : IcosahedralDart}
    (prior : Quiver.Path z a)
    (p q r : Quiver.Path a b)
    (bridgeOut : Quiver.Path b m)
    (bridgeIn : Quiver.Path m b)
    (s t u : Quiver.Path b c)
    (suffix : Quiver.Path c d) (Z : C60F98FourLocalInputs p q r s t u) :
    (c60F102HVOrderNatIso prior p q r bridgeOut bridgeIn s t u suffix).hom.app Z ≫
        (c60F102RLMixedNatIso prior p q r bridgeOut bridgeIn s t u suffix).hom.app Z =
      (c60F102LRMixedNatIso prior p q r bridgeOut bridgeIn s t u suffix).hom.app Z ≫
        (c60F102VHOrderNatIso prior p q r bridgeOut bridgeIn s t u suffix).hom.app Z := by
  apply c60F80QuotientThree_ext
  change
    (c60F77QuotientToStrictCharge.map
      (eqToHom (c60F102HVOrder_object_eq prior p q r bridgeOut bridgeIn s t u suffix Z) ≫
        eqToHom (c60F98ObservedMixedObject_eq
          ((c60F99LeftWhiskerFunctor prior).obj ((c60F99RightWhiskerFunctor bridgeOut).obj Z.1.1))
          ((c60F99LeftWhiskerFunctor prior).obj ((c60F99RightWhiskerFunctor bridgeOut).obj Z.1.2))
          ((c60F99LeftWhiskerFunctor bridgeIn).obj ((c60F99RightWhiskerFunctor suffix).obj Z.2.1))
          ((c60F99LeftWhiskerFunctor bridgeIn).obj ((c60F99RightWhiskerFunctor suffix).obj Z.2.2))))).charge =
    (c60F77QuotientToStrictCharge.map
      (eqToHom (c60F98ObservedMixedObject_eq
          ((c60F99RightWhiskerFunctor bridgeOut).obj ((c60F99LeftWhiskerFunctor prior).obj Z.1.1))
          ((c60F99RightWhiskerFunctor bridgeOut).obj ((c60F99LeftWhiskerFunctor prior).obj Z.1.2))
          ((c60F99RightWhiskerFunctor suffix).obj ((c60F99LeftWhiskerFunctor bridgeIn).obj Z.2.1))
          ((c60F99RightWhiskerFunctor suffix).obj ((c60F99LeftWhiskerFunctor bridgeIn).obj Z.2.2))) ≫
        eqToHom (c60F102VHOrder_object_eq prior p q r bridgeOut bridgeIn s t u suffix Z))).charge
  simp only [c60F80QuotientThree_comp_charge,
    c60F82Quotient_eqToHom_charge_zero, zero_add]

/-- F102: the square commutes at the genuine Mathlib natural-
transformation level, hence for ALL genuine quotient Hom arrows,
not just one choice of the original F42 2-cell representatives. -/
theorem c60F102OrderMixedSquare_natTrans
    {z a b m c d : IcosahedralDart}
    (prior : Quiver.Path z a)
    (p q r : Quiver.Path a b)
    (bridgeOut : Quiver.Path b m)
    (bridgeIn : Quiver.Path m b)
    (s t u : Quiver.Path b c)
    (suffix : Quiver.Path c d) :
    (c60F102HVOrderNatIso prior p q r bridgeOut bridgeIn s t u suffix).hom ≫
        (c60F102RLMixedNatIso prior p q r bridgeOut bridgeIn s t u suffix).hom =
      (c60F102LRMixedNatIso prior p q r bridgeOut bridgeIn s t u suffix).hom ≫
        (c60F102VHOrderNatIso prior p q r bridgeOut bridgeIn s t u suffix).hom := by
  ext Z
  exact c60F102OrderMixedSquare_component prior p q r bridgeOut bridgeIn s t u suffix Z

#print axioms c60F102FourLR
#print axioms c60F102FourRL
#print axioms c60F102HVOrder_object_eq
#print axioms c60F102VHOrder_object_eq
#print axioms c60F102HVOrder_charge_eq
#print axioms c60F102VHOrder_charge_eq
#print axioms c60F102HVOrderNatIso
#print axioms c60F102VHOrderNatIso
#print axioms c60F102LRMixedNatIso
#print axioms c60F102RLMixedNatIso
#print axioms c60F102LRMixedNatIso_charge_zero
#print axioms c60F102RLMixedNatIso_charge_zero
#print axioms c60F102OrderMixedSquare_component
#print axioms c60F102OrderMixedSquare_natTrans

end
end KUOS.DependentOriginationC60KuuFourInputDoubleContextCoherenceV5_256
