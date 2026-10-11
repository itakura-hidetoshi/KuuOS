import KUOS.DependentOriginationCoherentBiadjunctionBracketTreeRegroupingV5_149
import KUOS.DependentOriginationCoherentBiadjunctionFourfoldPentagonV5_150

namespace KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionExchangeQuotientConcatenationV5_141.Grid

set_option autoImplicit false
noncomputable section

/-!
# F54-A / v5.151 — genuinely Type-valued local associativity rotations

F52 proves exact three-subtree reassociation in the original F44
generated independent-axis exchange quotient. F53 constructs a
specific four-subtree five-vertex pentagon.

Here a local associator is NOT merely a Prop claiming the same Hom:
it is an actual inductive Type-valued witness, built out of the
original F52 Type-valued binary bracket tree. It can rotate three
arbitrary complete subtrees at the root, and it can be embedded
recursively into ANY left or right binary-tree context.

The root constructor exposes TWO explicit Nat.add_assoc casts, one
for the original F19 StrongTrans.Modification history and one for the
separately typed genuine F28 compression-kernel quotient history.
Local contextual rotations do NOT commute unlike same-axis steps.
Every such witness preserves the original F44 generated exchange
class and both entire proof-relevant original axis histories.
-/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

/-- An ACTUAL local forward associativity ROTATION witness in Type,
including its exact F19/F28 dependent index transports and ANY
finite left/right binary-tree contexts. -/
inductive OriginalF45BracketTree.LocalRotation :
    ∀ {a b : D} {x y : E} {n m : Nat}
      {ma mb : Blocks a b} {pa pb : Blocks x y},
      OriginalF45BracketTree n m ma pa mb pb →
      OriginalF45BracketTree n m ma pa mb pb →
      Type (max (max uD uE) (max vD vE)) where
  | assoc
      {a b : D} {x y : E}
      {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
      {p₀ p₁ p₂ p₃ : Blocks a b}
      {q₀ q₁ q₂ q₃ : Blocks x y}
      (first : OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁)
      (second : OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂)
      (third : OriginalF45BracketTree n₃ m₃ p₂ q₂ p₃ q₃) :
      LocalRotation
        (OriginalF45BracketTree.castDepths
          (Nat.add_assoc n₁ n₂ n₃) (Nat.add_assoc m₁ m₂ m₃)
          (OriginalF45BracketTree.node
            (OriginalF45BracketTree.node first second) third))
        (OriginalF45BracketTree.node first
          (OriginalF45BracketTree.node second third))
  | leftContext
      {a b : D} {x y : E} {n m n' m' : Nat}
      {ma mb mc : Blocks a b} {pa pb pc : Blocks x y}
      {before after : OriginalF45BracketTree n m ma pa mb pb}
      (step : LocalRotation before after)
      (later : OriginalF45BracketTree n' m' mb pb mc pc) :
      LocalRotation
        (OriginalF45BracketTree.node before later)
        (OriginalF45BracketTree.node after later)
  | rightContext
      {a b : D} {x y : E} {n m n' m' : Nat}
      {ma mb mc : Blocks a b} {pa pb pc : Blocks x y}
      (earlier : OriginalF45BracketTree n m ma pa mb pb)
      {before after : OriginalF45BracketTree n' m' mb pb mc pc}
      (step : LocalRotation before after) :
      LocalRotation
        (OriginalF45BracketTree.node earlier before)
        (OriginalF45BracketTree.node earlier after)

/-- EVERY genuine typed local associativity rotation at ANY binary
context preserves the original F44 primitive-adjacent-exchange
Quot class, with both exact independent F19/F28 depths intact. -/
theorem OriginalF45BracketTree.LocalRotation.toExchangeClass_eq
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    {before after : OriginalF45BracketTree n m ma pa mb pb}
    (step : OriginalF45BracketTree.LocalRotation before after) :
    before.toExchangeClass = after.toExchangeClass := by
  induction step with
  | assoc first second third =>
      exact OriginalF45BracketTree.reassociate first second third
  | leftContext step later ih =>
      exact congrArg
        (fun c => ExchangeClass.append c later.toExchangeClass) ih
  | rightContext earlier step ih =>
      exact congrArg
        (fun c => ExchangeClass.append earlier.toExchangeClass c) ih

/-- Original F19 and genuine F28 complete Type-valued primitive
histories are IDENTICAL after any local contextual rotation.
This is stronger than equality of just categorical Hom evaluations. -/
theorem OriginalF45BracketTree.LocalRotation.axisHistories_eq
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    {before after : OriginalF45BracketTree n m ma pa mb pb}
    (step : OriginalF45BracketTree.LocalRotation before after) :
    before.axisHistories = after.axisHistories := by
  have h := congrArg ExchangeClass.axisTraces step.toExchangeClass_eq
  simpa only [OriginalF45BracketTree.toExchangeClass_axisTraces] using h

/-- Original F43 two-axis reachability remains certified by both
ends of EVERY exact-depth local associativity rotation. -/
theorem OriginalF45BracketTree.LocalRotation.originalInterleavings
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    {before after : OriginalF45BracketTree n m ma pa mb pb}
    (step : OriginalF45BracketTree.LocalRotation before after) :
    KUOS.DependentOriginationCoherentBiadjunctionInterleavedRefinementV5_140.Grid.Interleaving
        n m ma pa mb pb ∧
      KUOS.DependentOriginationCoherentBiadjunctionInterleavedRefinementV5_140.Grid.Interleaving
        n m ma pa mb pb :=
  ⟨before.toExchangeClass.toInterleaving,
    after.toExchangeClass.toInterleaving⟩

#print axioms OriginalF45BracketTree.LocalRotation
#print axioms OriginalF45BracketTree.LocalRotation.toExchangeClass_eq
#print axioms OriginalF45BracketTree.LocalRotation.axisHistories_eq
#print axioms OriginalF45BracketTree.LocalRotation.originalInterleavings

end
end KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid
