import KUOS.DependentOriginationC60KuuContextWhiskeringDescentV5_253

namespace KUOS.DependentOriginationC60KuuTwoSidedContextCoherenceV5_254

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayC60OriginalFaceHorizontalPresentationV5_199
open KUOS.DependentOriginationGrayC60OriginalFaceHorizontalThreeHomV5_199
open KUOS.DependentOriginationGrayC60OriginalFaceHorizontalCompositionV5_199
open KUOS.DependentOriginationC60InterchangerStrictChargeQuotientV5_229
open KUOS.DependentOriginationC60NativeExchangeCongruenceQuotientV5_231
open KUOS.DependentOriginationC60NativeQuotientHorizontalTensorV5_234
open KUOS.DependentOriginationC60QuotientTensorNaturalityV5_236
open KUOS.DependentOriginationC60KuuLocalUniversalDescentV5_249
open KUOS.DependentOriginationC60KuuContextWhiskeringDescentV5_253

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.254 / F100 — Kuu two-sided C60 path-context observation coherence

We combine the genuinely descended F99 left and right whiskering
FUNCTORS for two independently chosen, actual C60 paths.
Their two orders end in DIFFERENT original F42 presentations:
((prior.comp p).comp suffix) and (prior.comp (p.comp suffix)).
We therefore do not equate original source objects or F51 morphisms.
After their appropriately indexed F77 observations, we construct
a genuine Mathlib NatIso, for all F95 quotient Hom arrows.

The comparison adds zero Int × Int charge, while both original
integer-charge coordinates are preserved. This does not repair
old Gray odd/odd phases or annul genuine local F55 curvature.
-/

/-- Genuine C60 one-path reassociation is available, but it is
not an equality between proof-relevant F42 2-cell objects. -/
theorem c60F100Path_assoc
    {a b c d : IcosahedralDart}
    (prior : Quiver.Path a b) (p : Quiver.Path b c)
    (suffix : Quiver.Path c d) :
    (prior.comp p).comp suffix = prior.comp (p.comp suffix) :=
  Quiver.Path.comp_assoc prior p suffix

/-- First LEFT-context then RIGHT-context, observed at its own
correctly parenthesized C60 path pair in the genuine F77 quotient. -/
def c60F100LeftRightObserved
    {a b c d : IcosahedralDart}
    (prior : Quiver.Path a b)
    {p q : Quiver.Path b c}
    (suffix : Quiver.Path c d) :
    C60F95LocalKuuQuotient p q ⥤ C60F77NativeQuotient :=
  (c60F99LeftWhiskerFunctor (p := p) (q := q) prior ⋙
      c60F99RightWhiskerFunctor
        (p := prior.comp p) (q := prior.comp q) suffix) ⋙
    c60F95DescendedToF77
      ((prior.comp p).comp suffix) ((prior.comp q).comp suffix)

/-- First RIGHT-context then LEFT-context, keeping the genuinely
distinct source presentation instead of silently casting it. -/
def c60F100RightLeftObserved
    {a b c d : IcosahedralDart}
    (prior : Quiver.Path a b)
    {p q : Quiver.Path b c}
    (suffix : Quiver.Path c d) :
    C60F95LocalKuuQuotient p q ⥤ C60F77NativeQuotient :=
  (c60F99RightWhiskerFunctor (p := p) (q := q) suffix ⋙
      c60F99LeftWhiskerFunctor
        (p := p.comp suffix) (q := q.comp suffix) prior) ⋙
    c60F95DescendedToF77
      (prior.comp (p.comp suffix)) (prior.comp (q.comp suffix))

/-- Both observed composite functors have identical F77 objects,
obtained by TWO successive genuine F99 observation invariances.
Nothing here identifies their original raw F42 objects. -/
theorem c60F100ObservedObject_eq
    {a b c d : IcosahedralDart}
    (prior : Quiver.Path a b)
    {p q : Quiver.Path b c}
    (suffix : Quiver.Path c d)
    (X : C60F95LocalKuuQuotient p q) :
    (c60F100LeftRightObserved prior suffix).obj X =
      (c60F100RightLeftObserved prior suffix).obj X := by
  calc
    (c60F100LeftRightObserved prior suffix).obj X =
        (c60F95DescendedToF77
          ((prior.comp p).comp suffix) ((prior.comp q).comp suffix)).obj
          ((c60F99RightWhiskerFunctor suffix).obj
            ((c60F99LeftWhiskerFunctor prior).obj X)) := rfl
    _ = (c60F95DescendedToF77 (prior.comp p) (prior.comp q)).obj
          ((c60F99LeftWhiskerFunctor prior).obj X) :=
        c60F99RightWhisker_object_obs suffix
          ((c60F99LeftWhiskerFunctor prior).obj X)
    _ = (c60F95DescendedToF77 p q).obj X :=
        c60F99LeftWhisker_object_obs prior X
    _ = (c60F95DescendedToF77 (p.comp suffix) (q.comp suffix)).obj
          ((c60F99RightWhiskerFunctor suffix).obj X) :=
        (c60F99RightWhisker_object_obs suffix X).symm
    _ = (c60F95DescendedToF77
          (prior.comp (p.comp suffix)) (prior.comp (q.comp suffix))).obj
          ((c60F99LeftWhiskerFunctor prior).obj
            ((c60F99RightWhiskerFunctor suffix).obj X)) :=
        (c60F99LeftWhisker_object_obs prior
          ((c60F99RightWhiskerFunctor suffix).obj X)).symm
    _ = (c60F100RightLeftObserved prior suffix).obj X := rfl

/-- Neither original integer-charge coordinate changes under
left-then-right contexts, for EVERY true quotient 3-Hom. -/
theorem c60F100LeftRight_charge_obs
    {a b c d : IcosahedralDart}
    (prior : Quiver.Path a b)
    {p q : Quiver.Path b c}
    (suffix : Quiver.Path c d)
    {X Y : C60F95LocalKuuQuotient p q}
    (f : X ⟶ Y) :
    (c60F77QuotientToStrictCharge.map
      ((c60F100LeftRightObserved prior suffix).map f)).charge =
      (c60F77QuotientToStrictCharge.map
        ((c60F95DescendedToF77 p q).map f)).charge := by
  change
    (c60F77QuotientToStrictCharge.map
      ((c60F95DescendedToF77
        ((prior.comp p).comp suffix) ((prior.comp q).comp suffix)).map
        ((c60F99RightWhiskerFunctor suffix).map
          ((c60F99LeftWhiskerFunctor prior).map f)))).charge =
      (c60F77QuotientToStrictCharge.map
        ((c60F95DescendedToF77 p q).map f)).charge
  exact
    (c60F99RightWhisker_charge_obs suffix
      ((c60F99LeftWhiskerFunctor prior).map f)).trans
      (c60F99LeftWhisker_charge_obs prior f)

/-- The reverse context order independently preserves all original
charge data without identifying the original F42 syntax. -/
theorem c60F100RightLeft_charge_obs
    {a b c d : IcosahedralDart}
    (prior : Quiver.Path a b)
    {p q : Quiver.Path b c}
    (suffix : Quiver.Path c d)
    {X Y : C60F95LocalKuuQuotient p q}
    (f : X ⟶ Y) :
    (c60F77QuotientToStrictCharge.map
      ((c60F100RightLeftObserved prior suffix).map f)).charge =
      (c60F77QuotientToStrictCharge.map
        ((c60F95DescendedToF77 p q).map f)).charge := by
  change
    (c60F77QuotientToStrictCharge.map
      ((c60F95DescendedToF77
        (prior.comp (p.comp suffix)) (prior.comp (q.comp suffix))).map
        ((c60F99LeftWhiskerFunctor prior).map
          ((c60F99RightWhiskerFunctor suffix).map f)))).charge =
      (c60F77QuotientToStrictCharge.map
        ((c60F95DescendedToF77 p q).map f)).charge
  exact
    (c60F99LeftWhisker_charge_obs prior
      ((c60F99RightWhiskerFunctor suffix).map f)).trans
      (c60F99RightWhisker_charge_obs suffix f)

/-- F100: the two orders are related by a GENUINE Mathlib natural
isomorphism in F77, for arbitrary prefix/suffix and all original
C60-local quotient Hom arrows. This is observed descent, not
an unproved lift of a full Gray interchange. -/
def c60F100ObservedTwoSidedNatIso
    {a b c d : IcosahedralDart}
    (prior : Quiver.Path a b)
    {p q : Quiver.Path b c}
    (suffix : Quiver.Path c d) :
    c60F100LeftRightObserved prior suffix ≅
      c60F100RightLeftObserved prior suffix :=
  NatIso.ofComponents
    (fun X => eqToIso (c60F100ObservedObject_eq prior suffix X))
    (by
      intro X Y f
      change
        (c60F100LeftRightObserved prior suffix).map f ≫
          eqToHom (c60F100ObservedObject_eq prior suffix Y) =
        eqToHom (c60F100ObservedObject_eq prior suffix X) ≫
          (c60F100RightLeftObserved prior suffix).map f
      apply c60F80QuotientThree_ext
      simp only [c60F80QuotientThree_comp_charge,
        c60F82Quotient_eqToHom_charge_zero, add_zero, zero_add]
      exact
        (c60F100LeftRight_charge_obs prior suffix f).trans
          (c60F100RightLeft_charge_obs prior suffix f).symm)

/-- The comparison itself adds NO integer charge. This is not an
assertion that an input arrow has zero charge. -/
theorem c60F100ObservedTwoSidedNatIso_charge_zero
    {a b c d : IcosahedralDart}
    (prior : Quiver.Path a b)
    {p q : Quiver.Path b c}
    (suffix : Quiver.Path c d)
    (X : C60F95LocalKuuQuotient p q) :
    (c60F77QuotientToStrictCharge.map
      ((c60F100ObservedTwoSidedNatIso prior suffix).hom.app X)).charge =
        (0 : Int × Int) := by
  change
    (c60F77QuotientToStrictCharge.map
      (eqToHom (c60F100ObservedObject_eq prior suffix X))).charge =
        (0 : Int × Int)
  exact c60F82Quotient_eqToHom_charge_zero _

#print axioms c60F100Path_assoc
#print axioms c60F100ObservedObject_eq
#print axioms c60F100LeftRight_charge_obs
#print axioms c60F100RightLeft_charge_obs
#print axioms c60F100ObservedTwoSidedNatIso
#print axioms c60F100ObservedTwoSidedNatIso_charge_zero

end
end KUOS.DependentOriginationC60KuuTwoSidedContextCoherenceV5_254
