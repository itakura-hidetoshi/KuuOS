import KUOS.DependentOriginationInversePairIncidenceV3_62

namespace KUOS.DependentOriginationOctahedralInversePairV3_63

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationGeneratedHolonomyCountermodelV2_69
open KUOS.DependentOriginationQuotientGaugeCoordinateKeyV3_14
open KUOS.DependentOriginationFreshAssociatorCompletionV3_37
open KUOS.DependentOriginationFiniteAssociatorScheduleV3_38
open KUOS.DependentOriginationFreshBoundaryCompatibilityV3_47
open KUOS.DependentOriginationCompositeIdentityInversePairReductionV3_54
open KUOS.DependentOriginationInversePairSuffixPerturbationV3_59
open KUOS.DependentOriginationCounterGaugeFiberNontrivialV3_61
open KUOS.DependentOriginationInversePairIncidenceV3_62

set_option autoImplicit false

noncomputable section

/-!
# Concrete octahedral inverse-pair task v3.63

v3.61 proves that every composition-coordinate gauge fiber of the concrete
v2.69 C2 model is nontrivial.  v3.62 reduces the remaining fresh-boundary and
suffix-isolation incidence to ordinary object inequalities together with an
actual two-sided inverse pair.

This file discharges those geometric inputs inside the same v2.69 octahedral
model.

We use the source edge

  a00 : L0 ⟶ M0

and the canonical Mathlib localization isomorphism attached to it.  Its hom is
literally allMorphisms.Q.map a00 and its inverse is wInv a00.  Thus the two
localization arrows satisfy both inverse equations by the hom_inv_id and
inv_hom_id fields of wIso.

For the third arrow we use the direct edge

  c00 : L0 ⟶ H0.

The canonical object equivalence

  Localization.Construction.objEquiv allMorphisms

identifies source vertices with localization objects.  Hence the decidable
source inequalities L0 != M0 and L0 != H0 transport to the exact localization
object inequalities needed by v3.62.

The result is one fully explicit inverse-pair fresh-boundary task with isolated
gComp(f,g), together with the already-proved nontrivial exact dependent gauge
fiber at that suffix coordinate.

No common unitor-correcting gauge is constructed in this file.  That remains
the final missing input before applying v3.60 to obtain an exact concrete
fixed-gauge obstruction.
-/

/-- Distinct source vertices remain distinct as objects of the canonical
localization.  This is object-level injectivity of Mathlib's canonical
`objEquiv`, not a statement about morphisms. -/
theorem localizationObject_ne_of_vertex_ne
    {A B : OctahedralVertex}
    (hAB : A ≠ B) :
    allMorphisms.Q.obj A ≠ allMorphisms.Q.obj B := by
  intro hQ
  apply hAB
  exact
    (CategoryTheory.Localization.Construction.objEquiv allMorphisms).injective
      hQ

/-- The first concrete localization object. -/
abbrev counterX : allMorphisms.Localization :=
  allMorphisms.Q.obj L0

/-- The second concrete localization object. -/
abbrev counterY : allMorphisms.Localization :=
  allMorphisms.Q.obj M0

/-- The third concrete localization object. -/
abbrev counterT : allMorphisms.Localization :=
  allMorphisms.Q.obj H0

/-- Forward member of the concrete inverse pair. -/
def counterInversePairForward : counterX ⟶ counterY :=
  allMorphisms.Q.map a00

/-- The source edge belongs to the all-morphisms property.  Keep this witness
named so every localization inverse law is elaborated against the same
MorphismProperty proof. -/
theorem a00_mem_allMorphisms : allMorphisms a00 := by
  trivial

/-- Formal localization inverse of the forward member. -/
def counterInversePairBackward : counterY ⟶ counterX :=
  CategoryTheory.Localization.Construction.wInv
    (W := allMorphisms) a00 a00_mem_allMorphisms

/-- Third arrow of the concrete associator task. -/
def counterInversePairThird : counterX ⟶ counterT :=
  allMorphisms.Q.map c00

/-- The forward map followed by its formal localization inverse is identity. -/
@[simp]
theorem counterInversePairForward_comp_backward :
    counterInversePairForward ≫ counterInversePairBackward = 𝟙 counterX := by
  change
    (CategoryTheory.Localization.Construction.wIso
      (W := allMorphisms) a00 a00_mem_allMorphisms).hom ≫
        (CategoryTheory.Localization.Construction.wIso
          (W := allMorphisms) a00 a00_mem_allMorphisms).inv =
      𝟙 counterX
  exact
    (CategoryTheory.Localization.Construction.wIso
      (W := allMorphisms) a00 a00_mem_allMorphisms).hom_inv_id

/-- The formal localization inverse followed by the forward map is identity. -/
@[simp]
theorem counterInversePairBackward_comp_forward :
    counterInversePairBackward ≫ counterInversePairForward = 𝟙 counterY := by
  change
    (CategoryTheory.Localization.Construction.wIso
      (W := allMorphisms) a00 a00_mem_allMorphisms).inv ≫
        (CategoryTheory.Localization.Construction.wIso
          (W := allMorphisms) a00 a00_mem_allMorphisms).hom =
      𝟙 counterY
  exact
    (CategoryTheory.Localization.Construction.wIso
      (W := allMorphisms) a00 a00_mem_allMorphisms).inv_hom_id

/-- L0 and M0 remain distinct after localization. -/
theorem counterX_ne_counterY : counterX ≠ counterY := by
  exact localizationObject_ne_of_vertex_ne (by decide)

/-- L0 and H0 remain distinct after localization. -/
theorem counterX_ne_counterT : counterX ≠ counterT := by
  exact localizationObject_ne_of_vertex_ne (by decide)

/-- The explicit octahedral task satisfies the complete v3.62 geometric
package: fresh boundary, exact inverse pair, and isolated gComp(f,g). -/
theorem counterInversePairTask_geometry :
    FreshBoundaryAssociatorTask allMorphisms
        ({ X := counterX, Y := counterY, Z := counterX, T := counterT,
           f := counterInversePairForward,
           g := counterInversePairBackward,
           h := counterInversePairThird } : AssociatorTask allMorphisms) ∧
      IsCompositeInversePairAssociatorTask allMorphisms
        ({ X := counterX, Y := counterY, Z := counterX, T := counterT,
           f := counterInversePairForward,
           g := counterInversePairBackward,
           h := counterInversePairThird } : AssociatorTask allMorphisms) ∧
      AssociatorFGInteriorIsolated allMorphisms
        counterInversePairForward counterInversePairBackward
        counterInversePairThird := by
  exact
    inversePairTask_freshBoundary_and_fgInteriorIsolated_of_objects_ne
      allMorphisms
      counterInversePairForward
      counterInversePairBackward
      counterInversePairThird
      counterInversePairForward_comp_backward
      counterInversePairBackward_comp_forward
      counterX_ne_counterY
      counterX_ne_counterT

/-- The exact dependent gauge fiber at the isolated suffix of the concrete
octahedral task is nontrivial. -/
theorem counterInversePairTask_fgFiber_nontrivial :
    Nontrivial
      (QuotientGaugeCoordinateFiber
        allMorphisms counterSystem counterD
        (.composition counterInversePairForward counterInversePairBackward)) := by
  exact
    counterCompositionGaugeFiber_nontrivial_counterD
      counterInversePairForward counterInversePairBackward

/-- Combined concrete local package available before the final common-unitor
gauge construction. -/
theorem counterInversePairTask_geometry_and_nontrivialFiber :
    (FreshBoundaryAssociatorTask allMorphisms
        ({ X := counterX, Y := counterY, Z := counterX, T := counterT,
           f := counterInversePairForward,
           g := counterInversePairBackward,
           h := counterInversePairThird } : AssociatorTask allMorphisms) ∧
      IsCompositeInversePairAssociatorTask allMorphisms
        ({ X := counterX, Y := counterY, Z := counterX, T := counterT,
           f := counterInversePairForward,
           g := counterInversePairBackward,
           h := counterInversePairThird } : AssociatorTask allMorphisms) ∧
      AssociatorFGInteriorIsolated allMorphisms
        counterInversePairForward counterInversePairBackward
        counterInversePairThird) ∧
      Nontrivial
        (QuotientGaugeCoordinateFiber
          allMorphisms counterSystem counterD
          (.composition counterInversePairForward counterInversePairBackward)) := by
  exact ⟨counterInversePairTask_geometry,
    counterInversePairTask_fgFiber_nontrivial⟩

/-!
## Boundary after v3.63

The v2.69 model now supplies, constructively and at exact dependent types,

* three separated localization objects;
* a literal two-sided inverse pair between the first two;
* a fresh-boundary associator task;
* an isolated gComp(f,g) suffix;
* a Nontrivial exact quotient-gauge fiber at that suffix.

Therefore the only remaining hypothesis in the v3.60 concrete obstruction
mechanism is a fixed quotient gauge correcting every unitor route.

The next theorem unit should truth-test that global unitor gauge directly in
the concrete C2 model.  In particular, it must not infer such a gauge merely
from local unitor correctability or from permissive holonomy correction
authority.
-/

end

end KUOS.DependentOriginationOctahedralInversePairV3_63
