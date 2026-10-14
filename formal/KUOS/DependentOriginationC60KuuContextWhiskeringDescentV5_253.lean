import KUOS.DependentOriginationC60KuuObservedMixedInterchangeV5_252

namespace KUOS.DependentOriginationC60KuuContextWhiskeringDescentV5_253

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayC60PresentedInterchangerV5_191
open KUOS.DependentOriginationGrayC60OriginalFaceHorizontalPresentationV5_199
open KUOS.DependentOriginationGrayC60OriginalFaceHorizontalThreeHomV5_199
open KUOS.DependentOriginationGrayC60OriginalFaceHorizontalCompositionV5_199
open KUOS.DependentOriginationC60InterchangerStrictChargeQuotientV5_229
open KUOS.DependentOriginationC60NativeExchangeCongruenceQuotientV5_231
open KUOS.DependentOriginationC60NativeQuotientHorizontalTensorV5_234
open KUOS.DependentOriginationC60QuotientTensorNaturalityV5_236
open KUOS.DependentOriginationC60KuuReplacementInterchangeV5_248
open KUOS.DependentOriginationC60KuuLocalUniversalDescentV5_249
open KUOS.DependentOriginationC60KuuLocalHorizontalFunctorV5_250
open KUOS.DependentOriginationC60KuuLocalVerticalFunctorV5_251
open KUOS.DependentOriginationC60KuuObservedMixedInterchangeV5_252

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.253 / F99 — genuine C60 path-context whiskering descent for Kuu local quotients

The original F51 presentation has LEFT/RIGHT path whiskering functors,
but the F95 Kuu relation deliberately identifies 3-arrows modulo only
their two independently conserved integer charges. This file proves the
whiskering functors respect precisely that relation and therefore descend
uniquely to ACTUAL F95 local quotient categories, for arbitrary genuine
C60 source and target paths.

Each descended whiskering operation is a bundled Mathlib Functor.
Its composite with F77's observable target is canonically naturally
isomorphic to the original local F77 observation. The natural
isomorphisms have 0 additional Int × Int charge; their naturality
holds for ALL actual quotient 3-morphisms.

This extends F98's 4-input observed interchange to path contexts:
the local context action is a genuine functor, not a new raw 3-cell,
and cannot reintroduce the exchange phase eliminated by F77.
The original unquotiented F42/F55 global comparison is not asserted.
-/

/-! ## Left path whiskering: replaceability is an actual congruence -/

/-- Independent replacement of F51 three-arrow presentations remains
valid after whiskering by an arbitrary actual C60 prefix path. -/
theorem c60F99LeftWhisker_respects
    {a b c : IcosahedralDart}
    (prior : Quiver.Path a b)
    {p q : Quiver.Path b c} :
    ∀ (X Y : C60F51OriginalTwo p q) (f g : X ⟶ Y),
      c60F94Replaceable f g →
        (c60F51LeftWhiskerFunctor prior ⋙
            c60F95LocalProjection (prior.comp p) (prior.comp q)).map f =
          (c60F51LeftWhiskerFunctor prior ⋙
            c60F95LocalProjection (prior.comp p) (prior.comp q)).map g := by
  intro X Y f g h
  change
    (c60F95LocalProjection (prior.comp p) (prior.comp q)).map
        ((c60F51LeftWhiskerFunctor prior).map f) =
      (c60F95LocalProjection (prior.comp p) (prior.comp q)).map
        ((c60F51LeftWhiskerFunctor prior).map g)
  apply (c60F95Projection_map_eq_iff_charges _ _).mpr
  calc
    (c60F51Eval ((c60F51LeftWhiskerFunctor prior).map f)).charge =
        (c60F51Eval f).charge :=
          congrArg GradedThreeCell.charge (c60F51LeftWhisker_eval prior f)
    _ = (c60F51Eval g).charge :=
      (c60F94Replaceable_iff_charges f g).mp h
    _ = (c60F51Eval ((c60F51LeftWhiskerFunctor prior).map g)).charge :=
      (congrArg GradedThreeCell.charge
        (c60F51LeftWhisker_eval prior g)).symm

/-- An actual bundled functor acting by LEFT C60 path context on the
local Kuu quotient, built using F95's universal descent. -/
def c60F99LeftWhiskerFunctor
    {a b c : IcosahedralDart}
    (prior : Quiver.Path a b)
    {p q : Quiver.Path b c} :
    C60F95LocalKuuQuotient p q ⥤
      C60F95LocalKuuQuotient (prior.comp p) (prior.comp q) :=
  c60F95UniversalLift p q
    (c60F51LeftWhiskerFunctor prior ⋙
      c60F95LocalProjection (prior.comp p) (prior.comp q))
    (c60F99LeftWhisker_respects prior)

/-- The genuinely descended functor agrees ON THE NOSE with
the original proof-relevant F51 whisker after projection. -/
theorem c60F99LeftWhisker_spec
    {a b c : IcosahedralDart}
    (prior : Quiver.Path a b)
    {p q : Quiver.Path b c} :
    c60F95LocalProjection p q ⋙ c60F99LeftWhiskerFunctor prior =
      c60F51LeftWhiskerFunctor prior ⋙
        c60F95LocalProjection (prior.comp p) (prior.comp q) :=
  c60F95UniversalLift_spec p q
    (c60F51LeftWhiskerFunctor prior ⋙
      c60F95LocalProjection (prior.comp p) (prior.comp q))
    (c60F99LeftWhisker_respects prior)

/-! ## Right path whiskering, independently from a genuine suffix -/

/-- Independent replacement also persists after arbitrary RIGHT
whiskering by a genuine C60 suffix path. -/
theorem c60F99RightWhisker_respects
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b}
    (suffix : Quiver.Path b c) :
    ∀ (X Y : C60F51OriginalTwo p q) (f g : X ⟶ Y),
      c60F94Replaceable f g →
        (c60F51RightWhiskerFunctor suffix ⋙
            c60F95LocalProjection (p.comp suffix) (q.comp suffix)).map f =
          (c60F51RightWhiskerFunctor suffix ⋙
            c60F95LocalProjection (p.comp suffix) (q.comp suffix)).map g := by
  intro X Y f g h
  change
    (c60F95LocalProjection (p.comp suffix) (q.comp suffix)).map
        ((c60F51RightWhiskerFunctor suffix).map f) =
      (c60F95LocalProjection (p.comp suffix) (q.comp suffix)).map
        ((c60F51RightWhiskerFunctor suffix).map g)
  apply (c60F95Projection_map_eq_iff_charges _ _).mpr
  calc
    (c60F51Eval ((c60F51RightWhiskerFunctor suffix).map f)).charge =
        (c60F51Eval f).charge :=
          congrArg GradedThreeCell.charge (c60F51RightWhisker_eval suffix f)
    _ = (c60F51Eval g).charge :=
      (c60F94Replaceable_iff_charges f g).mp h
    _ = (c60F51Eval ((c60F51RightWhiskerFunctor suffix).map g)).charge :=
      (congrArg GradedThreeCell.charge
        (c60F51RightWhisker_eval suffix g)).symm

def c60F99RightWhiskerFunctor
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b}
    (suffix : Quiver.Path b c) :
    C60F95LocalKuuQuotient p q ⥤
      C60F95LocalKuuQuotient (p.comp suffix) (q.comp suffix) :=
  c60F95UniversalLift p q
    (c60F51RightWhiskerFunctor suffix ⋙
      c60F95LocalProjection (p.comp suffix) (q.comp suffix))
    (c60F99RightWhisker_respects suffix)

theorem c60F99RightWhisker_spec
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b}
    (suffix : Quiver.Path b c) :
    c60F95LocalProjection p q ⋙ c60F99RightWhiskerFunctor suffix =
      c60F51RightWhiskerFunctor suffix ⋙
        c60F95LocalProjection (p.comp suffix) (q.comp suffix) :=
  c60F95UniversalLift_spec p q
    (c60F51RightWhiskerFunctor suffix ⋙
      c60F95LocalProjection (p.comp suffix) (q.comp suffix))
    (c60F99RightWhisker_respects suffix)

/-! ## Exact preservation of global F77 observation on objects/Homs -/

/-- Contextual replacement never changes the F77 observed
two-cell degree, for ANY actual C60 prefix. -/
theorem c60F99LeftWhisker_object_obs
    {a b c : IcosahedralDart}
    (prior : Quiver.Path a b)
    {p q : Quiver.Path b c}
    (X : C60F95LocalKuuQuotient p q) :
    (c60F95DescendedToF77 (prior.comp p) (prior.comp q)).obj
      ((c60F99LeftWhiskerFunctor prior).obj X) =
      (c60F95DescendedToF77 p q).obj X := by
  rcases X with ⟨X⟩
  rfl

theorem c60F99RightWhisker_object_obs
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b}
    (suffix : Quiver.Path b c)
    (X : C60F95LocalKuuQuotient p q) :
    (c60F95DescendedToF77 (p.comp suffix) (q.comp suffix)).obj
      ((c60F99RightWhiskerFunctor suffix).obj X) =
      (c60F95DescendedToF77 p q).obj X := by
  rcases X with ⟨X⟩
  rfl

/-- The two integer charge coordinates of an arbitrary TRUE local
Kuu quotient Hom are unaffected by LEFT path whiskering. -/
theorem c60F99LeftWhisker_charge_obs
    {a b c : IcosahedralDart}
    (prior : Quiver.Path a b)
    {p q : Quiver.Path b c}
    {X Y : C60F95LocalKuuQuotient p q}
    (f : X ⟶ Y) :
    (c60F77QuotientToStrictCharge.map
      ((c60F95DescendedToF77 (prior.comp p) (prior.comp q)).map
        ((c60F99LeftWhiskerFunctor prior).map f))).charge =
      (c60F77QuotientToStrictCharge.map
        ((c60F95DescendedToF77 p q).map f)).charge := by
  rcases X with ⟨X⟩
  rcases Y with ⟨Y⟩
  refine Quot.inductionOn f (fun rf => ?_)
  change
    (c60F51Eval ((c60F51LeftWhiskerFunctor prior).map rf)).charge =
      (c60F51Eval rf).charge
  exact congrArg GradedThreeCell.charge (c60F51LeftWhisker_eval prior rf)

/-- The right-context calculation is independent of LEFT
whiskering: it too preserves all native integer charges. -/
theorem c60F99RightWhisker_charge_obs
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b}
    (suffix : Quiver.Path b c)
    {X Y : C60F95LocalKuuQuotient p q}
    (f : X ⟶ Y) :
    (c60F77QuotientToStrictCharge.map
      ((c60F95DescendedToF77 (p.comp suffix) (q.comp suffix)).map
        ((c60F99RightWhiskerFunctor suffix).map f))).charge =
      (c60F77QuotientToStrictCharge.map
        ((c60F95DescendedToF77 p q).map f)).charge := by
  rcases X with ⟨X⟩
  rcases Y with ⟨Y⟩
  refine Quot.inductionOn f (fun rf => ?_)
  change
    (c60F51Eval ((c60F51RightWhiskerFunctor suffix).map rf)).charge =
      (c60F51Eval rf).charge
  exact congrArg GradedThreeCell.charge (c60F51RightWhisker_eval suffix rf)

/-! ## Genuine natural equivalence of observations, not a raw phase lift -/

/-- For every prefix, the F77 observation of the actual descended
Kuu whiskering functor is NATURALLY ISOMORPHIC to the original
F77 observation. Coherence is an equality of actual quotient 3-Homs. -/
def c60F99LeftWhiskerObservedNatIso
    {a b c : IcosahedralDart}
    (prior : Quiver.Path a b)
    {p q : Quiver.Path b c} :
    c60F99LeftWhiskerFunctor prior ⋙
      c60F95DescendedToF77 (prior.comp p) (prior.comp q) ≅
        c60F95DescendedToF77 p q :=
  NatIso.ofComponents
    (fun X => eqToIso (c60F99LeftWhisker_object_obs prior X))
    (by
      intro X Y f
      change
        (c60F95DescendedToF77 (prior.comp p) (prior.comp q)).map
            ((c60F99LeftWhiskerFunctor prior).map f) ≫
          eqToHom (c60F99LeftWhisker_object_obs prior Y) =
        eqToHom (c60F99LeftWhisker_object_obs prior X) ≫
          (c60F95DescendedToF77 p q).map f
      apply c60F80QuotientThree_ext
      simp only [c60F80QuotientThree_comp_charge,
        c60F82Quotient_eqToHom_charge_zero, add_zero, zero_add]
      exact c60F99LeftWhisker_charge_obs prior f)

/-- The RIGHT context has the independent corresponding natural
isomorphism, equally independent of source exchange phases. -/
def c60F99RightWhiskerObservedNatIso
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b}
    (suffix : Quiver.Path b c) :
    c60F99RightWhiskerFunctor suffix ⋙
      c60F95DescendedToF77 (p.comp suffix) (q.comp suffix) ≅
        c60F95DescendedToF77 p q :=
  NatIso.ofComponents
    (fun X => eqToIso (c60F99RightWhisker_object_obs suffix X))
    (by
      intro X Y f
      change
        (c60F95DescendedToF77 (p.comp suffix) (q.comp suffix)).map
            ((c60F99RightWhiskerFunctor suffix).map f) ≫
          eqToHom (c60F99RightWhisker_object_obs suffix Y) =
        eqToHom (c60F99RightWhisker_object_obs suffix X) ≫
          (c60F95DescendedToF77 p q).map f
      apply c60F80QuotientThree_ext
      simp only [c60F80QuotientThree_comp_charge,
        c60F82Quotient_eqToHom_charge_zero, add_zero, zero_add]
      exact c60F99RightWhisker_charge_obs suffix f)

/-- The true observed LEFT-context natural isomorphism adds
ZERO integer charge, not an assumption that input charges vanish. -/
theorem c60F99LeftWhiskerObservedNatIso_charge_zero
    {a b c : IcosahedralDart}
    (prior : Quiver.Path a b)
    {p q : Quiver.Path b c}
    (X : C60F95LocalKuuQuotient p q) :
    (c60F77QuotientToStrictCharge.map
      ((c60F99LeftWhiskerObservedNatIso prior).hom.app X)).charge =
      (0 : Int × Int) := by
  change
    (c60F77QuotientToStrictCharge.map
      (eqToHom (c60F99LeftWhisker_object_obs prior X))).charge =
        (0 : Int × Int)
  exact c60F82Quotient_eqToHom_charge_zero _

theorem c60F99RightWhiskerObservedNatIso_charge_zero
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b}
    (suffix : Quiver.Path b c)
    (X : C60F95LocalKuuQuotient p q) :
    (c60F77QuotientToStrictCharge.map
      ((c60F99RightWhiskerObservedNatIso suffix).hom.app X)).charge =
      (0 : Int × Int) := by
  change
    (c60F77QuotientToStrictCharge.map
      (eqToHom (c60F99RightWhisker_object_obs suffix X))).charge =
        (0 : Int × Int)
  exact c60F82Quotient_eqToHom_charge_zero _

#print axioms c60F99LeftWhisker_respects
#print axioms c60F99LeftWhisker_spec
#print axioms c60F99RightWhisker_respects
#print axioms c60F99RightWhisker_spec
#print axioms c60F99LeftWhisker_object_obs
#print axioms c60F99RightWhisker_object_obs
#print axioms c60F99LeftWhisker_charge_obs
#print axioms c60F99RightWhisker_charge_obs
#print axioms c60F99LeftWhiskerObservedNatIso
#print axioms c60F99RightWhiskerObservedNatIso
#print axioms c60F99LeftWhiskerObservedNatIso_charge_zero
#print axioms c60F99RightWhiskerObservedNatIso_charge_zero

end
end KUOS.DependentOriginationC60KuuContextWhiskeringDescentV5_253
