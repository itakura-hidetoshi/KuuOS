import KUOS.DependentOriginationCoherentBiadjunctionOriginalF45ObservedHigherCellNonfaithfulnessV5_153

namespace KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionExchangeQuotientConcatenationV5_141.Grid

set_option autoImplicit false
noncomputable section

/-!
# F56-E / v5.153 — no faithful Type-valued higher interpretation
# factoring solely through the original F44 observation

F56-C built a genuine original F44 / complete F19/F28 axis-history
observational target of the separately typed F55 pentagon and
independent rotation square. F56-D proves that the four actual
certificates are subsingletons and that the F44 observation forgets
distinct raw Type-valued PresentedCell constructors.

Here the obstruction is stable under ANY further function out of the
fixed F44 observational target, and hence applies to EVERY
independently chosen F56-A HigherCellTarget interpretation whose
higher-cell map factors through those original four certificates.

This is a precise conditional NONFAITHFULNESS theorem on *raw free*
F55 PresentedCell proof terms, not a proof that an external
tricategory/Gray category cannot coherently identify its own identity
and composite cells. No extra target 3-cells or G.toOplax inverses
are manufactured.
-/

universe uD vD uE vE uT
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

/-- On every original fixed indexed pair of parallel finite routes,
ANY output that factors through the genuine F44/complete-history
observation is CONSTANT on the freely presented higher witnesses.
No assumption is made on the codomain other than its being a Type. -/
theorem OriginalF45BracketTree.DepthRotationRoute.PresentedCell.observationFactor_constant
    {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    {first : OriginalF45BracketTree n m ma pa mb pb}
    {last : OriginalF45BracketTree n' m' ma pa mb pb}
    {r s : OriginalF45BracketTree.DepthRotationRoute first last}
    {T : Type uT}
    (interpretation :
      OriginalF45BracketTree.DepthRotationRoute.PresentedCell r s → T)
    (afterObservation :
      OriginalF45BracketTree.DepthRotationRoute.F44ObservedCell r s → T)
    (factors : ∀ cell : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r s,
      interpretation cell = afterObservation cell.toOriginalF44Observation)
    (cell₁ cell₂ : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r s) :
    interpretation cell₁ = interpretation cell₂ := by
  calc
    interpretation cell₁ =
        afterObservation cell₁.toOriginalF44Observation :=
      factors cell₁
    _ = afterObservation cell₂.toOriginalF44Observation := by
      exact congrArg afterObservation (Subsingleton.elim _ _)
    _ = interpretation cell₂ := (factors cell₂).symm

/-- No codomain can recover a faithful raw proof-relevant higher
cell interpretation IF its map factors through F56-C's genuine F44
and F19/F28 complete-history endpoint certificates.

The counterexample is the original presented identity vs its
two-step vertical identity paste. -/
theorem OriginalF45BracketTree.DepthRotationRoute.PresentedCell.observationFactor_not_injective
    {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    {first : OriginalF45BracketTree n m ma pa mb pb}
    {last : OriginalF45BracketTree n' m' ma pa mb pb}
    (route : OriginalF45BracketTree.DepthRotationRoute first last)
    {T : Type uT}
    (interpretation :
      OriginalF45BracketTree.DepthRotationRoute.PresentedCell route route → T)
    (afterObservation :
      OriginalF45BracketTree.DepthRotationRoute.F44ObservedCell route route → T)
    (factors : ∀ cell : OriginalF45BracketTree.DepthRotationRoute.PresentedCell route route,
      interpretation cell = afterObservation cell.toOriginalF44Observation) :
    ¬ Function.Injective interpretation := by
  intro hinj
  apply OriginalF45BracketTree.DepthRotationRoute.PresentedCell.ident_ne_doubleIdent route
  apply hinj
  exact OriginalF45BracketTree.DepthRotationRoute.PresentedCell.observationFactor_constant
    interpretation afterObservation factors
    (OriginalF45BracketTree.DepthRotationRoute.PresentedCell.ident route)
    (OriginalF45BracketTree.DepthRotationRoute.PresentedCell.trans
      (OriginalF45BracketTree.DepthRotationRoute.PresentedCell.ident route)
      (OriginalF45BracketTree.DepthRotationRoute.PresentedCell.ident route))

/-- No reconstruction from only the four genuine original
F44/complete-history certificates can be a left inverse of the
concrete F55 Type-valued presented-cell observational interpretation. -/
theorem OriginalF45BracketTree.DepthRotationRoute.PresentedCell.observation_no_recovery
    {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    {first : OriginalF45BracketTree n m ma pa mb pb}
    {last : OriginalF45BracketTree n' m' ma pa mb pb}
    (route : OriginalF45BracketTree.DepthRotationRoute first last) :
    ¬ ∃ recover :
        OriginalF45BracketTree.DepthRotationRoute.F44ObservedCell route route →
          OriginalF45BracketTree.DepthRotationRoute.PresentedCell route route,
      ∀ cell : OriginalF45BracketTree.DepthRotationRoute.PresentedCell route route,
        recover cell.toOriginalF44Observation = cell := by
  rintro ⟨recover, hRecover⟩
  apply OriginalF45BracketTree.DepthRotationRoute.PresentedCell.ident_ne_doubleIdent route
  calc
    (OriginalF45BracketTree.DepthRotationRoute.PresentedCell.ident route)
        = recover
          (OriginalF45BracketTree.DepthRotationRoute.PresentedCell.ident
            route).toOriginalF44Observation := (hRecover _).symm
    _ = recover
          (OriginalF45BracketTree.DepthRotationRoute.PresentedCell.trans
            (OriginalF45BracketTree.DepthRotationRoute.PresentedCell.ident route)
            (OriginalF45BracketTree.DepthRotationRoute.PresentedCell.ident route)
          ).toOriginalF44Observation := by
            exact congrArg recover (Subsingleton.elim _ _)
    _ = OriginalF45BracketTree.DepthRotationRoute.PresentedCell.trans
          (OriginalF45BracketTree.DepthRotationRoute.PresentedCell.ident route)
          (OriginalF45BracketTree.DepthRotationRoute.PresentedCell.ident route) :=
      hRecover _

/-- An independent F56-A HigherCellTarget is NOT faithful to raw
F55 higher path syntax whenever its genuine interpretation is
required to factor through the F56-C original F44 observation target.
This theorem does NOT prohibit other, richer targets that retain
more than the original quotient/history boundary information. -/
theorem OriginalF45BracketTree.DepthRotationRoute.HigherCellTarget.no_faithful_observation_factor
    (target : OriginalF45BracketTree.DepthRotationRoute.HigherCellTarget D E)
    {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    {first : OriginalF45BracketTree n m ma pa mb pb}
    {last : OriginalF45BracketTree n' m' ma pa mb pb}
    (route : OriginalF45BracketTree.DepthRotationRoute first last)
    (afterObservation :
      OriginalF45BracketTree.DepthRotationRoute.F44ObservedCell route route →
        target.Cell route route)
    (factors : ∀ cell : OriginalF45BracketTree.DepthRotationRoute.PresentedCell route route,
      cell.interpret target = afterObservation cell.toOriginalF44Observation) :
    ¬ Function.Injective
        (fun cell : OriginalF45BracketTree.DepthRotationRoute.PresentedCell route route =>
          cell.interpret target) := by
  exact OriginalF45BracketTree.DepthRotationRoute.PresentedCell.observationFactor_not_injective
    route (fun cell => cell.interpret target) afterObservation factors

#print axioms OriginalF45BracketTree.DepthRotationRoute.PresentedCell.observationFactor_constant
#print axioms OriginalF45BracketTree.DepthRotationRoute.PresentedCell.observationFactor_not_injective
#print axioms OriginalF45BracketTree.DepthRotationRoute.PresentedCell.observation_no_recovery
#print axioms OriginalF45BracketTree.DepthRotationRoute.HigherCellTarget.no_faithful_observation_factor

end
end KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid
