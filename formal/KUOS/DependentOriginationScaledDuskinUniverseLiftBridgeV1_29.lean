import KUOS.DependentOriginationGlobalDuskinScaledHornCoherenceV1_22
import KUOS.DependentOriginationStrictlyUnitaryDuskinModelTransportV1_27

namespace KUOS.DependentOriginationScaledDuskinUniverseLiftBridgeV1_29

open CategoryTheory
open Simplicial
open Opposite
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationGlobalDuskinScaledHornCoherenceV1_22
open KUOS.DependentOriginationGlobalDuskinScaledNerveV1_21
open KUOS.DependentOriginationStrictlyUnitaryDuskinModelTransportV1_27

universe u v
universe u₁ u₂ v₁ v₂ w₁ w₂

/-!
# Universe-safe scaling bridge (append-only)

The existing scalings on `SSet.{u}` are transported to the literal
`SSet.uliftFunctor.{v,u}` at the pinned mathlib API. This does not identify
different universes or silently change an existing scaled-horn certificate.
The converse descent and compatibility with both Duskin nerves remain separate
proof obligations.
-/

/-- Lift a scaling without changing which underlying 2-simplices are thin. -/
@[reducible] def uliftScaling
    {X : SSet.{u}} (sX : ScaledSimplicialSet X) :
    ScaledSimplicialSet ((SSet.uliftFunctor.{v, u}).obj X) where
  thin := fun x => sX.thin x.down
  thin_sigma_zero := by
    intro x
    change sX.thin (X.σ 0 x.down)
    exact sX.thin_sigma_zero x.down
  thin_sigma_one := by
    intro x
    change sX.thin (X.σ 1 x.down)
    exact sX.thin_sigma_one x.down

/-- Lifting reflects and preserves the original thinness predicate exactly. -/
@[simp] theorem uliftScaling_thin_iff
    {X : SSet.{u}} (sX : ScaledSimplicialSet X)
    (x : X.obj (op ⦋2⦌)) :
    (uliftScaling.{u, v} sX).thin (ULift.up x) ↔ sX.thin x := by
  rfl

/-- Every scaled map lifts to a scaled map at the common universe. -/
theorem isScaledMap_ulift
    {X Y : SSet.{u}}
    {sX : ScaledSimplicialSet X} {sY : ScaledSimplicialSet Y}
    {f : X ⟶ Y} (hf : IsScaledMap sX sY f) :
    IsScaledMap (uliftScaling.{u, v} sX) (uliftScaling.{u, v} sY)
      ((SSet.uliftFunctor.{v, u}).map f) := by
  intro x hx
  change sY.thin (f.app (op ⦋2⦌) x.down)
  exact hf x.down hx

/--
Correctly typed full scaled certificate for independent source and target
universe levels. The original legacy v1.29 certificate is preserved verbatim;
compatibility of its unlifted horn domains with these lifted carriers is still
an independent descent/gluing obligation.
-/
structure LiftedFullScaledDuskinMapCertificate
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (E : StrictlyUnitaryBicategoricalModelEquivalence B C) : Prop where
  map_scaled :
    IsScaledMap
      (uliftScaling.{max (max w₁ v₁) u₁, max (max w₂ v₂) u₂} (duskinScaling B))
      (uliftScaling.{max (max w₂ v₂) u₂, max (max w₁ v₁) u₁} (duskinScaling C))
      (normalizedDuskinNerveMap E)

/--
The original nondegenerate-thinness theorem survives the simultaneous universe
lift exactly: no independent-universe equality or thinness hypothesis is added.
-/
theorem nondegenerateThin_preserved_lift
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (E : StrictlyUnitaryBicategoricalModelEquivalence B C)
    (σ : DuskinSimplex B 2)
    (hnd : ¬ IsDegenerateDuskinTwoSimplex σ)
    (hthin : (duskinScaling B).thin σ) :
    (uliftScaling.{max (max w₂ v₂) u₂, max (max w₁ v₁) u₁}
      (duskinScaling C)).thin
      ((normalizedDuskinNerveMap E).app (op ⦋2⦌) (ULift.up σ)) := by
  change (duskinScaling C).thin (transportDuskinSimplex E σ)
  exact nondegenerateThin_transport_isThin E σ hnd hthin

/--
Preservation of every thin 2-simplex after the common universe lift.
The invertible-comparison case uses the certified local hom equivalence;
the two degenerate cases use the naturality of the genuine Duskin nerve map.
-/
theorem allThin_preserved_lift
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (E : StrictlyUnitaryBicategoricalModelEquivalence B C) :
    IsScaledMap
      (uliftScaling.{max (max w₁ v₁) u₁, max (max w₂ v₂) u₂} (duskinScaling B))
      (uliftScaling.{max (max w₂ v₂) u₂, max (max w₁ v₁) u₁} (duskinScaling C))
      (normalizedDuskinNerveMap E) := by
  intro τ hthin
  change IsIso (duskinComparison τ.down) ∨ IsDegenerateDuskinTwoSimplex τ.down at hthin
  change IsIso (duskinComparison (transportDuskinSimplex E τ.down)) ∨
    IsDegenerateDuskinTwoSimplex (transportDuskinSimplex E τ.down)
  rcases hthin with hiso | hdeg
  · exact Or.inl (transportDuskinComparison_isIso E τ.down hiso)
  · rcases hdeg with ⟨e, he⟩ | ⟨e, he⟩
    · refine Or.inr (Or.inl ⟨transportDuskinSimplex E e, ?_⟩)
      rw [he]
      change
        transportDuskinSimplex E
          ((duskinReindex ((SimplexCategory.σ 0).op)).comp e) =
        (duskinReindex ((SimplexCategory.σ 0).op)).comp (transportDuskinSimplex E e)
      exact transportDuskinSimplex_reindex E _ e
    · refine Or.inr (Or.inr ⟨transportDuskinSimplex E e, ?_⟩)
      rw [he]
      change
        transportDuskinSimplex E
          ((duskinReindex ((SimplexCategory.σ 1).op)).comp e) =
        (duskinReindex ((SimplexCategory.σ 1).op)).comp (transportDuskinSimplex E e)
      exact transportDuskinSimplex_reindex E _ e

/-- No extra full-thinness assumption is required after well-typed lifting. -/
def canonicalLiftedFullScaledDuskinMapCertificate
    {B : Type u₁} [Bicategory.{w₁, v₁} B]
    {C : Type u₂} [Bicategory.{w₂, v₂} C]
    (E : StrictlyUnitaryBicategoricalModelEquivalence B C) :
    LiftedFullScaledDuskinMapCertificate E where
  map_scaled := allThin_preserved_lift E

#print axioms allThin_preserved_lift
#print axioms canonicalLiftedFullScaledDuskinMapCertificate

#print axioms LiftedFullScaledDuskinMapCertificate
#print axioms nondegenerateThin_preserved_lift

#print axioms uliftScaling
#print axioms uliftScaling_thin_iff
#print axioms isScaledMap_ulift

end KUOS.DependentOriginationScaledDuskinUniverseLiftBridgeV1_29
