import Mathlib
import KUOS.DependentOriginationGrayC60F55MixedEndomorphismRigidityV5_210

namespace KUOS.DependentOriginationArbitraryPastingCoherenceV5_213

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationGrayC60PresentedFaceTwoCellsV5_190
open KUOS.DependentOriginationGrayC60OriginalF55ThreeHomV5_192
open KUOS.DependentOriginationGrayC60MixedBoundaryThreeHomV5_195
open KUOS.DependentOriginationGrayC60F55MixedEndomorphismRigidityV5_210
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false

/-!
# Arbitrary-pasting coherence, relative to a rigid contextual boundary

The v5.212 three-context result has a mathematical consequence independent of
how many comparison squares have been pasted: in a source 3-Hom category whose
fixed boundary-tag endomorphisms are unique, two already-constructed and
well-typed invertible comparison routes with the same endpoints cannot differ.

The index of the family of routes is arbitrary (including infinite types).
This is an exact uniqueness theorem, NOT an existence theorem for all pastings.
It applies to the complete-native-kernel F47 quotient, not to the original
unquotiented F55 3-cell syntax or to an arbitrary global Gray 3-category.
-/

universe uS vS uT vT uD vD uE vE uI

section AbstractRigidity

variable {S : Type uS} [Category.{vS} S]
variable {T : Type uT} [Category.{vT} T]

/-- Objectwise equality of endpoints together with uniqueness of target
endomorphisms forces uniqueness of parallel natural isomorphisms.  No
subsingleton condition is imposed on unrelated target hom-sets. -/
theorem natIso_eq_of_endomorphism_rigidity
    (F G : S ⥤ T)
    (sameObjects : ∀ X : S, F.obj X = G.obj X)
    (rigid : ∀ (Y : T) (f g : Y ⟶ Y), f = g)
    (η θ : F ≅ G) : η = θ := by
  apply Iso.ext
  apply NatTrans.ext
  funext X
  rw [← sameObjects X]
  exact rigid (F.obj X) _ _

/-- All routes in an arbitrarily indexed family agree once their typed
endpoints agree and those endpoints have rigid endomorphisms. -/
theorem all_routes_equal_of_endomorphism_rigidity
    {I : Type uI}
    (F G : S ⥤ T)
    (sameObjects : ∀ X : S, F.obj X = G.obj X)
    (rigid : ∀ (Y : T) (f g : Y ⟶ Y), f = g)
    (routes : I → (F ≅ G))
    (i j : I) : routes i = routes j :=
  natIso_eq_of_endomorphism_rigidity F G sameObjects rigid (routes i) (routes j)

end AbstractRigidity

section GenuineF47Source

variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {n n' m m' : Nat}
variable {ma mb : Blocks a b} {pa pb : Blocks x y}
variable {first : OriginalF45BracketTree n m ma pa mb pb}
variable {last : OriginalF45BracketTree n' m' ma pa mb pb}
variable {r s : OriginalF45BracketTree.DepthRotationRoute first last}
variable {v w : IcosahedralDart} {p q : Quiver.Path v w}
variable {α β : C60F42PresentedFaceCell p q}
variable (B : C60F47SquareFrame α β r s)

/-- The ACTUAL F47 four-tag full-native-kernel source category provides
endomorphism rigidity using its original source rank proof (v5.210). -/
theorem f47_arbitrary_comparison_coherence
    {S : Type uS} [Category.{vS} S]
    (F G : S ⥤ C60F47BoundaryPoint B)
    (sameObjects : ∀ X : S, F.obj X = G.obj X)
    (η θ : F ≅ G) : η = θ := by
  apply natIso_eq_of_endomorphism_rigidity F G sameObjects
  intro Y f g
  exact c60F61MixedEndomorphism_unique B Y f g

/-- In particular, EVERY already-constructed family of source-level pastings
is coherent, without fixing the length or bracketing of the family. -/
theorem f47_arbitrary_pasting_coherence
    {S : Type uS} [Category.{vS} S]
    {I : Type uI}
    (F G : S ⥤ C60F47BoundaryPoint B)
    (sameObjects : ∀ X : S, F.obj X = G.obj X)
    (routes : I → (F ≅ G))
    (i j : I) : routes i = routes j :=
  f47_arbitrary_comparison_coherence B F G sameObjects (routes i) (routes j)

/-- The five routes of a typed associativity pentagon are forced equal IF
all five are actually constructed with matching F47 endpoints.  Construction
of the physical original four-context routes remains an independent duty. -/
theorem f47_conditional_four_context_pentagon
    {S : Type uS} [Category.{vS} S]
    (F G : S ⥤ C60F47BoundaryPoint B)
    (sameObjects : ∀ X : S, F.obj X = G.obj X)
    (pentagonRoutes : Fin 5 → (F ≅ G)) :
    ∀ i j : Fin 5, pentagonRoutes i = pentagonRoutes j := by
  intro i j
  exact f47_arbitrary_pasting_coherence B F G sameObjects pentagonRoutes i j

end GenuineF47Source

#print axioms natIso_eq_of_endomorphism_rigidity
#print axioms all_routes_equal_of_endomorphism_rigidity
#print axioms f47_arbitrary_comparison_coherence
#print axioms f47_arbitrary_pasting_coherence
#print axioms f47_conditional_four_context_pentagon

end KUOS.DependentOriginationArbitraryPastingCoherenceV5_213
