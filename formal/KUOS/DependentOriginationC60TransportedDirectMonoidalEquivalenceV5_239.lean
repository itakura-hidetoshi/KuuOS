import KUOS.DependentOriginationC60MonoidalEquivalenceCompatibilityV5_238
import Mathlib.CategoryTheory.Monoidal.Transport

namespace KUOS.DependentOriginationC60TransportedDirectMonoidalEquivalenceV5_239

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

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.239 / F85 — transported/direct quotient MONOIDAL equivalence

F81 transported the F75 charge monoidal category to the genuine F77
phase quotient along the F79 categorical equivalence. F83 independently
constructed the direct F80 original-representative quotient tensor and
proved its full pentagon and triangle. F84 proved a strong monoidal
equivalence of the DIRECT quotient with the strict Z²-charge groupoid.

We retain two names for the two monoidal structures, and factor the
comparison through the ORIGINAL F75 groupoid:
    F81 transported quotient ≌ F75 ≌ F83 direct quotient.
Mathlib's transport and monoidal equivalence theorems give the
associator, both unitors, tensorator coherence and invertible inverse,
without assuming that F81's and F83's tensors are definitionally equal.
We also transport the resulting strong monoidal structure along the
canonical F79 unit natural isomorphism to the underlying IDENTITY
functor of the actual F77 quotient. Thus the two structures are
monoidally equivalent even with the underlying functor fixed as identity.

F82's separately established natural isomorphism of the corresponding
tensor bifunctors remains available. No assertion is made that the
original nontrivial Gray braiding was already the identity, or that
all raw F42/F54/F55 C60 higher gluing is a strict 3-category.
Both integral charge coordinates and C60 physical -5 curvature remain
distinct from the erased exchange phase.
-/

/-- Exactly F81's transported quotient, packaged via Mathlib's
canonical Transported synonym to keep its structure identifiable. -/
abbrev C60F85TransportedQuotient :=
  CategoryTheory.Monoidal.Transported
    c60F79NativeChargeEquivalence.symm

/-- The carried monoidal data are definitionally F81's actual
transport, and not F83's independently constructed direct tensor. -/
theorem c60F85TransportedStruct_eq_F81 :
    CategoryTheory.Monoidal.transportStruct
      c60F79NativeChargeEquivalence.symm =
        c60F81QuotientMonoidalStruct := rfl

/-- The entire transported monoidal LAW structure agrees with F81. -/
theorem c60F85TransportedLaws_eq_F81 :
    CategoryTheory.Monoidal.transport
      c60F79NativeChargeEquivalence.symm =
        c60F81QuotientMonoidalCategory := rfl

/-- Likewise the separate F84 direct realization uses F83's
independently proved F80 quotient monoidal DATA, not F81's. -/
theorem c60F85DirectStruct_eq_F83 :
    c60F84DirectQuotientMonoidalStruct =
      c60F83DirectMonoidalStruct := rfl

/-- The Mathlib equivalence transporting F75 into F81, reversed.
Its domain really carries the transported monoidal structure. -/
@[implicit_reducible]
def c60F85TransportedToCharge :
    C60F85TransportedQuotient ≌ C60F75StrictChargeGrade :=
  (CategoryTheory.Monoidal.equivalenceTransported
    c60F79NativeChargeEquivalence.symm).symm

/-- This leg is strong monoidal by Mathlib's verified transport
construction, with all its unit and associativity coherence. -/
@[implicit_reducible]
def c60F85TransportedToChargeForwardMonoidal :
    c60F85TransportedToCharge.functor.Monoidal := by
  unfold c60F85TransportedToCharge
  infer_instance

/-- The other leg is exactly F84's genuine DIRECT quotient-to-charge
equivalence reversed, not an equality of unquotiented Gray phases. -/
@[implicit_reducible]
def c60F85ChargeToDirect :
    C60F75StrictChargeGrade ≌ C60F84DirectQuotient :=
  c60F84DirectChargeEquivalence.symm

/-- F84 proved the inverse of its direct-to-charge equivalence
strong monoidal; reuse that proof with the same exact instances. -/
@[implicit_reducible]
def c60F85ChargeToDirectForwardMonoidal :
    c60F85ChargeToDirect.functor.Monoidal := by
  letI : c60F84DirectChargeEquivalence.functor.Monoidal :=
    c60F84DirectChargeEquivalenceForwardMonoidal
  change c60F84DirectChargeEquivalence.inverse.Monoidal
  exact c60F84DirectChargeEquivalenceInverseMonoidal

/-- The genuine categorical equivalence from the transported quotient
to the independent F83 direct quotient, mediated by the original
F79/F84 strict two-coordinate charge groupoid. -/
@[implicit_reducible]
def c60F85TransportedDirectEquivalence :
    C60F85TransportedQuotient ≌ C60F84DirectQuotient :=
  c60F85TransportedToCharge.trans c60F85ChargeToDirect

/-- Strong monoidality of the forward functor: its tensorator and
unit are invertible, and naturality, associator and unit coherence
come from two separately proved genuine strong monoidal legs. -/
@[implicit_reducible]
def c60F85TransportedDirectForwardMonoidal :
    c60F85TransportedDirectEquivalence.functor.Monoidal := by
  letI : c60F85TransportedToCharge.functor.Monoidal :=
    c60F85TransportedToChargeForwardMonoidal
  letI : c60F85ChargeToDirect.functor.Monoidal :=
    c60F85ChargeToDirectForwardMonoidal
  change
    (c60F85TransportedToCharge.functor ⋙
      c60F85ChargeToDirect.functor).Monoidal
  infer_instance

/-- A coherent strong monoidal quasi-inverse, derived from the
proven categorical equivalence and its strong monoidal forward leg. -/
@[implicit_reducible]
def c60F85TransportedDirectInverseMonoidal :
    letI : c60F85TransportedDirectEquivalence.functor.Monoidal :=
      c60F85TransportedDirectForwardMonoidal
    c60F85TransportedDirectEquivalence.inverse.Monoidal := by
  letI : c60F85TransportedDirectEquivalence.functor.Monoidal :=
    c60F85TransportedDirectForwardMonoidal
  exact c60F85TransportedDirectEquivalence.inverseMonoidal

set_option backward.isDefEq.respectTransparency false in
/-- Full Mathlib monoidal equivalence: invertible tensor and unit
comparison maps and the coherent monoidal unit/counit and triangles,
NOT just the F82 natural isomorphism of bifunctors. -/
@[implicit_reducible]
def c60F85TransportedDirectMonoidalEquivalence :
    letI : c60F85TransportedDirectEquivalence.functor.Monoidal :=
      c60F85TransportedDirectForwardMonoidal
    letI : c60F85TransportedDirectEquivalence.inverse.Monoidal :=
      c60F85TransportedDirectEquivalence.inverseMonoidal
    c60F85TransportedDirectEquivalence.IsMonoidal := by
  letI : c60F85TransportedDirectEquivalence.functor.Monoidal :=
    c60F85TransportedDirectForwardMonoidal
  letI : c60F85TransportedDirectEquivalence.inverse.Monoidal :=
    c60F85TransportedDirectEquivalence.inverseMonoidal
  infer_instance

/-! ## Underlying identity and its genuinely strong monoidal lift -/

/-- The source and target are two explicit structure presentations
on the SAME original F77 quotient carrier, not a replacement by F75. -/
def c60F85UnderlyingIdentity :
    C60F85TransportedQuotient ⥤ C60F84DirectQuotient :=
  𝟭 C60F77NativeQuotient

/-- The mediated functor is canonically naturally isomorphic to the
identity on the original F77 quotient, by F79's verified unit. -/
def c60F85MediatedToIdentityNatIso :
    c60F85TransportedDirectEquivalence.functor ≅
      c60F85UnderlyingIdentity :=
  c60F79NativeChargeEquivalence.unitIso.symm

/-- Transport the *proven strong monoidal* structure along that genuine
F79 natural isomorphism: the identity-on-quotient functor itself is
strong monoidal, with no newly postulated associator or unitor law. -/
@[implicit_reducible]
def c60F85UnderlyingIdentityMonoidal :
    c60F85UnderlyingIdentity.Monoidal := by
  letI : c60F85TransportedDirectEquivalence.functor.Monoidal :=
    c60F85TransportedDirectForwardMonoidal
  exact Functor.Monoidal.transport c60F85MediatedToIdentityNatIso

/-- An actual categorical equivalence whose underlying functor is
IDENTITY on the original quotient, carrying distinct F81/F83
monoidal structures in its typed source and target presentations. -/
@[implicit_reducible]
def c60F85IdentityEquivalence :
    C60F85TransportedQuotient ≌ C60F84DirectQuotient :=
  CategoryTheory.Equivalence.refl

/-- The identity functor is strongly monoidal by the coherent
F79-mediated construction, not by a bare tensor NatIso. -/
@[implicit_reducible]
def c60F85IdentityForwardMonoidal :
    c60F85IdentityEquivalence.functor.Monoidal := by
  exact c60F85UnderlyingIdentityMonoidal

/-- Full strong monoidal inverse of the identity-on-quotient
equivalence, with the distinct transported/direct structures. -/
@[implicit_reducible]
def c60F85IdentityInverseMonoidal :
    letI : c60F85IdentityEquivalence.functor.Monoidal :=
      c60F85IdentityForwardMonoidal
    c60F85IdentityEquivalence.inverse.Monoidal := by
  letI : c60F85IdentityEquivalence.functor.Monoidal :=
    c60F85IdentityForwardMonoidal
  exact c60F85IdentityEquivalence.inverseMonoidal

set_option backward.isDefEq.respectTransparency false in
/-- MAIN F85: the F81 transported and F83 directly descended
monoidal structures on the genuine F77 quotient are monoidally
equivalent via the IDENTITY UNDERLYING FUNCTOR, with all Mathlib
monoidal unit/counit and associativity coherence certified. -/
@[implicit_reducible]
def c60F85IdentityMonoidalEquivalence :
    letI : c60F85IdentityEquivalence.functor.Monoidal :=
      c60F85IdentityForwardMonoidal
    letI : c60F85IdentityEquivalence.inverse.Monoidal :=
      c60F85IdentityEquivalence.inverseMonoidal
    c60F85IdentityEquivalence.IsMonoidal := by
  letI : c60F85IdentityEquivalence.functor.Monoidal :=
    c60F85IdentityForwardMonoidal
  letI : c60F85IdentityEquivalence.inverse.Monoidal :=
    c60F85IdentityEquivalence.inverseMonoidal
  infer_instance

/-- The earlier F82 comparison is still a genuine natural iso of
the F81/F83 full tensor bifunctors; F85 upgrades the relation to
a monoidal equivalence, without replacing F82's original proof. -/
def c60F85OriginalTensorNatIso :
    c60F82TransportedTensorFunctor ≅
      c60F83DirectTensorBifunctor :=
  c60F83TransportedVsDirectTensorNatIso

#print axioms c60F85TransportedStruct_eq_F81
#print axioms c60F85TransportedLaws_eq_F81
#print axioms c60F85DirectStruct_eq_F83
#print axioms c60F85TransportedToChargeForwardMonoidal
#print axioms c60F85ChargeToDirectForwardMonoidal
#print axioms c60F85TransportedDirectForwardMonoidal
#print axioms c60F85TransportedDirectInverseMonoidal
#print axioms c60F85TransportedDirectMonoidalEquivalence
#print axioms c60F85MediatedToIdentityNatIso
#print axioms c60F85UnderlyingIdentityMonoidal
#print axioms c60F85IdentityForwardMonoidal
#print axioms c60F85IdentityInverseMonoidal
#print axioms c60F85IdentityMonoidalEquivalence
#print axioms c60F85OriginalTensorNatIso

end
end KUOS.DependentOriginationC60TransportedDirectMonoidalEquivalenceV5_239
