import Kuu.F112.PolygonNativeF55P93AssocQuotientHorizontalCoherence
import Mathlib.Tactic

/-!
# F112-P93B — exact old-to-new F55 route quotient map and strict nonfaithfulness

P93A proved that all associator-naturality triples agree on the
SEPARATELY SELECTED P92B source-existence F54 route-object quotient.
Here we construct the canonical map from P91B's true ORIGINAL
nine-constructor F55 route quotient to the new P92B quotient, and
prove that it is (1) total and surjective and (2) NOT injective,
using true old F54 identity-chain contexts and P92A's original
nonexistence theorem. A genuinely non-descending readout is exhibited.

This is not a claim that P92B's new comparison was derived in old F55.
The P92A no-go remains mathematically true; the nonfaithfulness
exactly measures the new equality adjoined in the other presentation.
All original full signed F55/C60 odd phase evidence remains in the
original constructors. No new 4-cell coherence or strict 3/n claim.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

/-- The identity on true F54 raw routes induces a canonical
surjection from the OLD P91 original F55 quotient to the DISTINCT
P92B new associator-naturality quotient. Every old evidence
witness maps by the explicit P92B `original` constructor. -/
def nativeF55P93OriginalToAssocClass
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (q : NativeF55P91FullWitnessRouteClasses first last) :
    NativeF55P92AssocRouteClasses first last :=
  _root_.Quotient.liftOn q
    (fun route => nativeF55P92AssocRouteClass first last route)
    (by
      intro u v h
      rcases h with ⟨old⟩
      exact nativeF55P92AssocRouteClass_eq_of_cell first last
        (.original old))

/-- Computation is literally the identity on original F54
representatives; no shadow-based equation is manufactured. -/
theorem nativeF55P93OriginalToAssocClass_spec
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (route : KuuNativeF45Tree.DepthRotationRoute p first last) :
    nativeF55P93OriginalToAssocClass first last
      (nativeF55P91FullWitnessRouteClass first last route) =
      nativeF55P92AssocRouteClass first last route := rfl

/-- Every new class has an OLD route representative, even though
the evidence relations differ. Surjectivity does not imply fidelity. -/
theorem nativeF55P93OriginalToAssocClass_surjective
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :
    Function.Surjective (nativeF55P93OriginalToAssocClass first last) := by
  intro q
  refine _root_.Quotient.inductionOn q (fun route => ?_)
  exact ⟨nativeF55P91FullWitnessRouteClass first last route, rfl⟩

/-- The actual original F54 zero-chain associator-naturality
histories are genuinely DISTINGUISHED by the original P91B quotient.
The P92A nine-constructor no-go supplies the contradiction. -/
theorem nativeF55P93_original_unit_classes_distinct
    {p : Polygon} {a b : D} {x y : E}
    {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
    {p₀ p₁ p₂ p₃ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ q₃ : KuuNativeBlocks x y}
    (t₁ : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁)
    (t₂ : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂)
    (t₃ : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃) :
    nativeF55P91FullWitnessRouteClass
      (KuuNativeF45Tree.node (KuuNativeF45Tree.node t₁ t₂) t₃)
      (KuuNativeF45Tree.node t₁ (KuuNativeF45Tree.node t₂ t₃))
      (nativeF54P90AssocNaturalityLeftRoute
        (nativeF54P92UnitRoute t₁)
        (nativeF54P92UnitRoute t₂)
        (nativeF54P92UnitRoute t₃)) ≠
    nativeF55P91FullWitnessRouteClass
      (KuuNativeF45Tree.node (KuuNativeF45Tree.node t₁ t₂) t₃)
      (KuuNativeF45Tree.node t₁ (KuuNativeF45Tree.node t₂ t₃))
      (nativeF54P90AssocNaturalityRightRoute
        (nativeF54P92UnitRoute t₁)
        (nativeF54P92UnitRoute t₂)
        (nativeF54P92UnitRoute t₃)) := by
  intro h
  have old : Nonempty (NativeF55P90AssocNaturalityCell
      (nativeF54P92UnitRoute t₁)
      (nativeF54P92UnitRoute t₂)
      (nativeF54P92UnitRoute t₃)) :=
    (nativeF55P91FullWitnessRouteClass_eq_iff _ _ _ _).mp h
  exact (nativeF55P92_original_unit_naturality_no_filler t₁ t₂ t₃) old

/-- This surjection is STRICTLY NON-INJECTIVE for any three
composable true original F45 trees: the new associator-naturality
constructor identifies two old-source-inequivalent classes. -/
theorem nativeF55P93OriginalToAssocClass_not_injective
    {p : Polygon} {a b : D} {x y : E}
    {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
    {p₀ p₁ p₂ p₃ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ q₃ : KuuNativeBlocks x y}
    (t₁ : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁)
    (t₂ : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂)
    (t₃ : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃) :
    ¬ Function.Injective
      (nativeF55P93OriginalToAssocClass
        (KuuNativeF45Tree.node (KuuNativeF45Tree.node t₁ t₂) t₃)
        (KuuNativeF45Tree.node t₁ (KuuNativeF45Tree.node t₂ t₃))) := by
  intro hinj
  apply nativeF55P93_original_unit_classes_distinct t₁ t₂ t₃
  apply hinj
  change nativeF55P92AssocRouteClass _ _
    (nativeF54P90AssocNaturalityLeftRoute
      (nativeF54P92UnitRoute t₁)
      (nativeF54P92UnitRoute t₂)
      (nativeF54P92UnitRoute t₃)) =
    nativeF55P92AssocRouteClass _ _
    (nativeF54P90AssocNaturalityRightRoute
      (nativeF54P92UnitRoute t₁)
      (nativeF54P92UnitRoute t₂)
      (nativeF54P92UnitRoute t₃))
  exact nativeF55P92_assocNaturality_new_class_eq
    (nativeF54P92UnitRoute t₁)
    (nativeF54P92UnitRoute t₂)
    (nativeF54P92UnitRoute t₃)

/-- There is NO value of the original ordered unit-context-word
observer on the new P92B quotient compatible with ALL raw F54
routes: the same selected new class has two distinct readouts.
This is stronger than merely exhibiting a false preservation law. -/
theorem nativeF55P93OriginalWords_cannot_descend
    {p : Polygon} {a b : D} {x y : E}
    {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
    {p₀ p₁ p₂ p₃ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ q₃ : KuuNativeBlocks x y}
    (t₁ : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁)
    (t₂ : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂)
    (t₃ : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃) :
    ¬ ∃ readout :
      NativeF55P92AssocRouteClasses
        (KuuNativeF45Tree.node (KuuNativeF45Tree.node t₁ t₂) t₃)
        (KuuNativeF45Tree.node t₁ (KuuNativeF45Tree.node t₂ t₃)) →
        List (List Bool),
      ∀ route : KuuNativeF45Tree.DepthRotationRoute p
          (KuuNativeF45Tree.node (KuuNativeF45Tree.node t₁ t₂) t₃)
          (KuuNativeF45Tree.node t₁ (KuuNativeF45Tree.node t₂ t₃)),
        readout (nativeF55P92AssocRouteClass _ _ route) =
          route.p92UnitContextWords := by
  rintro ⟨readout, sound⟩
  let l := nativeF54P90AssocNaturalityLeftRoute
    (nativeF54P92UnitRoute t₁)
    (nativeF54P92UnitRoute t₂)
    (nativeF54P92UnitRoute t₃)
  let r := nativeF54P90AssocNaturalityRightRoute
    (nativeF54P92UnitRoute t₁)
    (nativeF54P92UnitRoute t₂)
    (nativeF54P92UnitRoute t₃)
  have hne : l.p92UnitContextWords ≠ r.p92UnitContextWords :=
    (nativeF55P93_original_unit_contextWords_lost t₁ t₂ t₃).1
  have heq : nativeF55P92AssocRouteClass _ _ l =
      nativeF55P92AssocRouteClass _ _ r :=
    (nativeF55P93_original_unit_contextWords_lost t₁ t₂ t₃).2
  apply hne
  calc
    l.p92UnitContextWords =
        readout (nativeF55P92AssocRouteClass _ _ l) := (sound l).symm
    _ = readout (nativeF55P92AssocRouteClass _ _ r) :=
      congrArg readout heq
    _ = r.p92UnitContextWords := sound r

/-- A physical north C60 triple already exhibits the failure of
faithfulness of the old-to-new quotient map. -/
theorem northNativeF55P93OriginalToAssoc_not_injective :
    ¬ Function.Injective
      (nativeF55P93OriginalToAssocClass
        (KuuNativeF45Tree.node
          (KuuNativeF45Tree.node
            northNativeF45FirstStage northNativeF45SecondStage)
          northNativeF45ThirdStage)
        (KuuNativeF45Tree.node northNativeF45FirstStage
          (KuuNativeF45Tree.node
            northNativeF45SecondStage northNativeF45ThirdStage))) :=
  nativeF55P93OriginalToAssocClass_not_injective
    northNativeF45FirstStage northNativeF45SecondStage
    northNativeF45ThirdStage

#print axioms nativeF55P93OriginalToAssocClass
#print axioms nativeF55P93OriginalToAssocClass_spec
#print axioms nativeF55P93OriginalToAssocClass_surjective
#print axioms nativeF55P93_original_unit_classes_distinct
#print axioms nativeF55P93OriginalToAssocClass_not_injective
#print axioms nativeF55P93OriginalWords_cannot_descend
#print axioms northNativeF55P93OriginalToAssoc_not_injective

end
end Kuu.F112.Physical
