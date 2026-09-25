import KUOS.DependentOriginationCountermodelSufficientConditionFailuresV4_04
import KUOS.DependentOriginationCounterGaugeFiberNontrivialV3_61
import Mathlib

namespace KUOS.DependentOriginationExplicitInvertibleIsotropyV4_05

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationFiberIsoThinV2_64
open KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69
open KUOS.DependentOriginationCounterGaugeFiberNontrivialV3_61
open KUOS.DependentOriginationCountermodelSufficientConditionFailuresV4_04

set_option autoImplicit false

noncomputable section

/-!
# Explicit invertible isotropy witness v4.05

v4.04 proves contrapositively that the concrete C2 countermodel cannot satisfy
the earlier automorphism-trivial / iso-thin sufficient conditions.

This file makes that failure constructive.

The unique object of CounterFiber has a nontrivial automorphism represented by
zeta.  One categorical level higher, the identity endofunctor carries the
nontrivial natural automorphism scalarIdNatIso zeta already constructed in the
countermodel carrier.

Thus the residual coherence ambiguity identified abstractly by v2.64-v2.66 is
visible directly as invertible C2 isotropy.
-/

/-- The unique countermodel fiber object has the zeta automorphism. -/
noncomputable def counterFiberZetaIso :
    (SingleObj.star C2 : CounterFiber) ≅
      (SingleObj.star C2 : CounterFiber) :=
  asIso (SingleObj.toEnd C2 zeta)

/-- The zeta automorphism of the unique fiber object is genuinely nonidentity. -/
theorem counterFiberZetaIso_ne_refl :
    counterFiberZetaIso ≠
      Iso.refl (SingleObj.star C2 : CounterFiber) := by
  intro h
  have hHom := congrArg Iso.hom h
  have hz : zeta = 1 := by
    simpa [counterFiberZetaIso, SingleObj.toEnd_def] using hHom
  exact zeta_ne_one hz

/-- Explicit object-level witness for failure of trivial fiber automorphisms. -/
theorem counterSystem_not_trivialFiberAutomorphisms_explicit :
    ¬ IsFiberAutomorphismTrivial counterSystem := by
  intro htriv
  letI :
      Subsingleton
        ((SingleObj.star C2 : counterSystem.obj (.mk L0)) ≅
          (SingleObj.star C2 : counterSystem.obj (.mk L0))) :=
    htriv L0 (SingleObj.star C2)
  have hEq :
      counterFiberZetaIso =
        Iso.refl (SingleObj.star C2 : CounterFiber) :=
    Subsingleton.elim _ _
  exact counterFiberZetaIso_ne_refl hEq

/-- Explicit functor-2-cell witness for failure of fiber-functor iso-thinness. -/
theorem counterSystem_not_fiberFunctorIsoThin_explicit :
    ¬ IsFiberFunctorIsoThin counterSystem := by
  intro hiso
  letI :
      Subsingleton
        ((𝟭 CounterFiber) ≅ (𝟭 CounterFiber)) :=
    hiso L0 L0 (𝟭 CounterFiber) (𝟭 CounterFiber)
  have hEq :
      scalarIdNatIso zeta = Iso.refl (𝟭 CounterFiber) :=
    Subsingleton.elim _ _
  exact scalarIdNatIso_zeta_ne_refl hEq

/-- Every quotient composition-coordinate gauge fiber also carries explicit
nontrivial invertible isotropy. -/
theorem counterSystem_every_compositionGaugeFiber_nontrivial
    {X Y Z : allMorphisms.Localization}
    (f : X ⟶ Y) (g : Y ⟶ Z) :
    Nontrivial
      (QuotientGaugeCoordinateFiber
        allMorphisms counterSystem counterD (.composition f g)) :=
  counterCompositionGaugeFiber_nontrivial_counterD f g

/-!
## Boundary after v4.05

The structural source of the finite obstruction is now explicit rather than
only contrapositively inferred:

* the unique C2 fiber object has the nonidentity automorphism zeta;
* the identity endofunctor has the nonidentity natural automorphism
  scalarIdNatIso zeta;
* every composition-coordinate quotient-gauge fiber is nontrivial.

This is exactly the invertible 2-dimensional isotropy sector that v2.64-v2.66
had isolated as the remaining place where coherence choices can carry a
nontrivial obstruction.
-/

end

end KUOS.DependentOriginationExplicitInvertibleIsotropyV4_05
