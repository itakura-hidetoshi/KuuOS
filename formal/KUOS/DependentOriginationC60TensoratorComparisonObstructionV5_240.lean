import KUOS.DependentOriginationC60TransportedDirectMonoidalEquivalenceV5_239
import Mathlib.CategoryTheory.Monoidal.Functor

namespace KUOS.DependentOriginationC60TensoratorComparisonObstructionV5_240

open CategoryTheory
open scoped CategoryTheory.MonoidalCategory
open KUOS.DependentOriginationC60InterchangerStrictChargeQuotientV5_229
open KUOS.DependentOriginationC60NativeExchangeCongruenceQuotientV5_231
open KUOS.DependentOriginationC60NativeChargeQuotientEquivalenceV5_233
open KUOS.DependentOriginationC60NativeQuotientHorizontalTensorV5_234
open KUOS.DependentOriginationC60NativeQuotientMonoidalCoherenceV5_235
open KUOS.DependentOriginationC60QuotientTensorNaturalityV5_236
open KUOS.DependentOriginationC60DirectQuotientMonoidalV5_237
open KUOS.DependentOriginationC60MonoidalEquivalenceCompatibilityV5_238
open KUOS.DependentOriginationC60TransportedDirectMonoidalEquivalenceV5_239

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.240 / F86 — explicit comparison and obstruction for two tensorators

F82 independently constructed a natural comparison β : tensorTransport ≅ tensorDirect
using the actual F79 quotient equivalence unitIso.
F85 independently constructed a strong monoidal identity-on-quotient functor
from the transported to the direct monoidal quotient; its lax tensorator μ
has the opposite arrow direction to β, hence should be compared with β⁻¹.

A strong monoidal equivalence alone does NOT imply that separately
constructed tensorators coincide. Instead of silently equating them,
we construct both real quotient-Hom isomorphisms and their invertible
composite obstruction Ω = μ ≫ β on the direct quotient. We prove an
exact two-integer-charge criterion for Ω = id, and retain the original
F80 and F82 naturality. This is an actual typed test on Mathlib F77
quotient Hom sets, not an unproved identification of Gray interchange.

The original odd/odd exchange phase was nontrivial before quotient;
both original integer charge components, C60 north curvature -5, and
the unquotiented F42/F54/F55 higher-gluing tasks remain distinct.
-/

/-- Strong monoidal IDENTITY tensorator from the F85 construction:
actual F80 direct-quotient tensor to actual F81 transported tensor. -/
def c60F86F85IdentityTensoratorIso
    (X Y : C60F85TransportedQuotient) :
    c60F80QuotientTwoTensor X Y ≅ (X ⊗ Y) := by
  letI : c60F85UnderlyingIdentity.Monoidal :=
    c60F85UnderlyingIdentityMonoidal
  exact Functor.Monoidal.μIso c60F85UnderlyingIdentity X Y

/-- The separately constructed F82 canonical comparison in the
same direction as the genuine F85 monoidal tensorator. -/
def c60F86F82CanonicalInverseTensorIso
    (X Y : C60F85TransportedQuotient) :
    c60F80QuotientTwoTensor X Y ≅ (X ⊗ Y) :=
  (c60F81TransportedVsOriginalQuotientTensorIso X Y).symm

/-- THEIR POTENTIAL DISAGREEMENT: an automorphism of the actual
F80 direct quotient tensor, not a numerical surrogate.
If this is identity then and only then the two tensorators agree. -/
def c60F86TensoratorObstructionIso
    (X Y : C60F85TransportedQuotient) :
    c60F80QuotientTwoTensor X Y ≅
      c60F80QuotientTwoTensor X Y :=
  c60F86F85IdentityTensoratorIso X Y ≪≫
    c60F81TransportedVsOriginalQuotientTensorIso X Y

/-- The explicit obstruction is the F85 μ followed by the F82 β
on every pair of REAL quotient two-cell objects. -/
theorem c60F86TensoratorObstruction_hom
    (X Y : C60F85TransportedQuotient) :
    (c60F86TensoratorObstructionIso X Y).hom =
      (c60F86F85IdentityTensoratorIso X Y).hom ≫
        (c60F81TransportedVsOriginalQuotientTensorIso X Y).hom := rfl

/-- Exactly the sum of the TWO independent integer-charge images:
no imposed vanishing and no conflation with the old exchange phase. -/
theorem c60F86TensoratorObstruction_charge
    (X Y : C60F85TransportedQuotient) :
    (c60F77QuotientToStrictCharge.map
      (c60F86TensoratorObstructionIso X Y).hom).charge =
      (c60F77QuotientToStrictCharge.map
        (c60F86F85IdentityTensoratorIso X Y).hom).charge +
      (c60F77QuotientToStrictCharge.map
        (c60F81TransportedVsOriginalQuotientTensorIso X Y).hom).charge := by
  exact c60F80QuotientThree_comp_charge _ _

/-- Faithfulness F79: the obstruction IS the identity precisely
when both independent integer charge coordinates vanish. -/
theorem c60F86Obstruction_identity_iff_charge_zero
    (X Y : C60F85TransportedQuotient) :
    (c60F86TensoratorObstructionIso X Y).hom =
        𝟙 (c60F80QuotientTwoTensor X Y) ↔
      (c60F77QuotientToStrictCharge.map
        (c60F86TensoratorObstructionIso X Y).hom).charge =
          (0 : Int × Int) := by
  constructor
  · intro h
    rw [h]
    exact c60F80QuotientThree_id_charge _
  · intro h
    apply c60F80QuotientThree_ext
    simpa only [c60F80QuotientThree_id_charge] using h

/-- The obstruction is trivial iff the exact F85 identity tensorator
equals the inverse component of the original F82 comparison.
This makes the remaining logical obligation explicit. -/
theorem c60F86IdentityTensorator_eq_F82_iff_obstruction
    (X Y : C60F85TransportedQuotient) :
    (c60F86F85IdentityTensoratorIso X Y).hom =
        (c60F81TransportedVsOriginalQuotientTensorIso X Y).inv ↔
      (c60F86TensoratorObstructionIso X Y).hom =
        𝟙 (c60F80QuotientTwoTensor X Y) := by
  constructor
  · intro h
    rw [c60F86TensoratorObstruction_hom, h]
    exact Iso.inv_hom_id _
  · intro h
    rw [c60F86TensoratorObstruction_hom] at h
    have hh := congrArg
      (fun (f : c60F80QuotientTwoTensor X Y ⟶
            c60F80QuotientTwoTensor X Y) =>
          f ≫ (c60F81TransportedVsOriginalQuotientTensorIso X Y).inv) h
    simpa only [Category.assoc, Iso.hom_inv_id,
      Category.comp_id, Category.id_comp] using hh

/-- As a genuinely strong monoidal functor, the identity-on-quotient
F85 tensorator is invertible on every typed pair of two-cells. -/
instance c60F86IdentityTensorator_isIso
    (X Y : C60F85TransportedQuotient) :
    IsIso (c60F86F85IdentityTensoratorIso X Y).hom :=
  (c60F86F85IdentityTensoratorIso X Y).isIso_hom

/-- Independently of possible equality with β⁻¹, the F85 tensorator
satisfies the full naturality equation on original F77 quotient Homs.
This is extracted from the proven strong monoidal functor. -/
theorem c60F86IdentityTensorator_natural
    {X X' Y Y' : C60F85TransportedQuotient}
    (f : X ⟶ X') (g : Y ⟶ Y') :
    c60F80QuotientThreeTensor f g ≫
        (c60F86F85IdentityTensoratorIso X' Y').hom =
      (c60F86F85IdentityTensoratorIso X Y).hom ≫
        (f ⊗ₘ g) := by
  letI : c60F85UnderlyingIdentity.Monoidal :=
    c60F85UnderlyingIdentityMonoidal
  exact Functor.LaxMonoidal.μ_natural c60F85UnderlyingIdentity f g

/-- The difference between the F85 strong tensorator and the F82
canonical natural comparison is itself NATURAL: it commutes with
all directly descended F80 quotient three-Hom tensors. -/
theorem c60F86TensoratorObstruction_natural
    {X X' Y Y' : C60F85TransportedQuotient}
    (f : X ⟶ X') (g : Y ⟶ Y') :
    c60F80QuotientThreeTensor f g ≫
        (c60F86TensoratorObstructionIso X' Y').hom =
      (c60F86TensoratorObstructionIso X Y).hom ≫
        c60F80QuotientThreeTensor f g := by
  rw [c60F86TensoratorObstruction_hom,
      c60F86TensoratorObstruction_hom]
  calc
    c60F80QuotientThreeTensor f g ≫
        ((c60F86F85IdentityTensoratorIso X' Y').hom ≫
          (c60F81TransportedVsOriginalQuotientTensorIso X' Y').hom) =
      (c60F80QuotientThreeTensor f g ≫
        (c60F86F85IdentityTensoratorIso X' Y').hom) ≫
          (c60F81TransportedVsOriginalQuotientTensorIso X' Y').hom := by
            rw [Category.assoc]
    _ = ((c60F86F85IdentityTensoratorIso X Y).hom ≫
          (f ⊗ₘ g)) ≫
          (c60F81TransportedVsOriginalQuotientTensorIso X' Y').hom := by
            rw [c60F86IdentityTensorator_natural f g]
    _ = (c60F86F85IdentityTensoratorIso X Y).hom ≫
          ((f ⊗ₘ g) ≫
            (c60F81TransportedVsOriginalQuotientTensorIso X' Y').hom) := by
            rw [Category.assoc]
    _ = (c60F86F85IdentityTensoratorIso X Y).hom ≫
          ((c60F81TransportedVsOriginalQuotientTensorIso X Y).hom ≫
            c60F80QuotientThreeTensor f g) := by
            rw [c60F82TransportedVsF80_naturality f g]
    _ = ((c60F86F85IdentityTensoratorIso X Y).hom ≫
          (c60F81TransportedVsOriginalQuotientTensorIso X Y).hom) ≫
          c60F80QuotientThreeTensor f g :=
            Category.assoc _ _ _

/-- Consequently the comparison defect is visible and checkable at
the two separately conserved integer-charge coordinates. -/
theorem c60F86TensoratorObstruction_components_zero_iff
    (X Y : C60F85TransportedQuotient) :
    (c60F86F85IdentityTensoratorIso X Y).hom =
        (c60F81TransportedVsOriginalQuotientTensorIso X Y).inv ↔
      (c60F77QuotientToStrictCharge.map
        (c60F86TensoratorObstructionIso X Y).hom).charge =
          (0 : Int × Int) := by
  rw [c60F86IdentityTensorator_eq_F82_iff_obstruction]
  exact c60F86Obstruction_identity_iff_charge_zero X Y

#print axioms c60F86F85IdentityTensoratorIso
#print axioms c60F86F82CanonicalInverseTensorIso
#print axioms c60F86TensoratorObstructionIso
#print axioms c60F86TensoratorObstruction_hom
#print axioms c60F86TensoratorObstruction_charge
#print axioms c60F86Obstruction_identity_iff_charge_zero
#print axioms c60F86IdentityTensorator_eq_F82_iff_obstruction
#print axioms c60F86IdentityTensorator_isIso
#print axioms c60F86IdentityTensorator_natural
#print axioms c60F86TensoratorObstruction_natural
#print axioms c60F86TensoratorObstruction_components_zero_iff

end
end KUOS.DependentOriginationC60TensoratorComparisonObstructionV5_240
