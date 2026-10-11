import KUOS.DependentOriginationCoherentBiadjunctionOriginalF45ConcreteF44CellTargetV5_153

namespace KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionExchangeQuotientConcatenationV5_141.Grid

set_option autoImplicit false
noncomputable section

/-!
# F56-D / v5.153 — exact information loss of the actual F44 observation target

F56-C constructed a genuine Type-valued concrete interpretation of the
original F55 presented higher path cells into four ORIGINAL certificates:
the two F44 generated-exchange class equalities and both independent
complete F19/F28 original axis-history equalities. Each certificate
is a proof in Prop; the packaging in Type does NOT turn it into an
independent higher 3-cell.

We prove that for any parallel actual depth-aware rotation routes,
the fiber of these observational certificates is a subsingleton and
is equivalently PUnit. Consequently all presented higher path cells
with a fixed source/target pair have the same observed certificate.

This is a STRICT, concrete non-faithfulness obstruction: a genuine
presented identity cell and its formal double vertical paste are
distinct raw Type-valued witnesses, yet their F44 observations agree.
Thus observational F44 semantics cannot reconstruct the original
proof-relevant presented higher path data. No external Gray or
tricategorical 3-cell equality is asserted.
-/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

/-- The four original F44 and full F19/F28 axis-history certificates
are each propositions. Any two witnesses of the same concrete
observational boundary must be equal as certificate structures. -/
theorem OriginalF45BracketTree.DepthRotationRoute.F44ObservedCell.eq_canonical
    {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    {first : OriginalF45BracketTree n m ma pa mb pb}
    {last : OriginalF45BracketTree n' m' ma pa mb pb}
    {r s : OriginalF45BracketTree.DepthRotationRoute first last}
    (observation : OriginalF45BracketTree.DepthRotationRoute.F44ObservedCell r s) :
    observation =
      OriginalF45BracketTree.DepthRotationRoute.F44ObservedCell.canonical r s := by
  cases observation
  rfl

/-- The authentic original F44 observational target retains full
WITHIN-AXIS primitive histories but no distinguishable higher witness
between any fixed pair of concrete parallel Type-valued routes. -/
instance OriginalF45BracketTree.DepthRotationRoute.F44ObservedCell.instSubsingleton
    {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    {first : OriginalF45BracketTree n m ma pa mb pb}
    {last : OriginalF45BracketTree n' m' ma pa mb pb}
    {r s : OriginalF45BracketTree.DepthRotationRoute first last} :
    Subsingleton (OriginalF45BracketTree.DepthRotationRoute.F44ObservedCell r s) where
  allEq observation₁ observation₂ :=
    observation₁.eq_canonical.trans observation₂.eq_canonical.symm

/-- Every fixed parallel-route observational fiber is equivalent to
one point. This is a real Type equivalence, not an assumed equality
between the different original F55 source paths. -/
def OriginalF45BracketTree.DepthRotationRoute.F44ObservedCell.equivPUnit
    {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    {first : OriginalF45BracketTree n m ma pa mb pb}
    {last : OriginalF45BracketTree n' m' ma pa mb pb}
    (r s : OriginalF45BracketTree.DepthRotationRoute first last) :
    OriginalF45BracketTree.DepthRotationRoute.F44ObservedCell r s ≃ PUnit where
  toFun := fun _ => PUnit.unit
  invFun := fun _ =>
    OriginalF45BracketTree.DepthRotationRoute.F44ObservedCell.canonical r s
  left_inv := by
    intro _
    exact Subsingleton.elim _ _
  right_inv := by
    intro _
    rfl

/-- The F56-C interpretation forgets which freely presented higher
cell produced the four original quotient/history certificates. -/
theorem OriginalF45BracketTree.DepthRotationRoute.PresentedCell.observation_eq
    {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    {first : OriginalF45BracketTree n m ma pa mb pb}
    {last : OriginalF45BracketTree n' m' ma pa mb pb}
    {r s : OriginalF45BracketTree.DepthRotationRoute first last}
    (cell₁ cell₂ : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r s) :
    cell₁.toOriginalF44Observation = cell₂.toOriginalF44Observation :=
  Subsingleton.elim _ _

/-- The genuine original Type-valued higher identity witness and a
TWO-STAGE vertical paste of that identity are NOT identical raw
constructor witnesses. No proof irrelevance is used to erase the
source PresentedCell. -/
theorem OriginalF45BracketTree.DepthRotationRoute.PresentedCell.ident_ne_doubleIdent
    {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    {first : OriginalF45BracketTree n m ma pa mb pb}
    {last : OriginalF45BracketTree n' m' ma pa mb pb}
    (route : OriginalF45BracketTree.DepthRotationRoute first last) :
    (OriginalF45BracketTree.DepthRotationRoute.PresentedCell.ident route) ≠
      (OriginalF45BracketTree.DepthRotationRoute.PresentedCell.trans
        (OriginalF45BracketTree.DepthRotationRoute.PresentedCell.ident route)
        (OriginalF45BracketTree.DepthRotationRoute.PresentedCell.ident route)) := by
  intro h
  cases h

/-- CONCRETE no-go: the F56-C original F44/complete-history
interpretation of Type-valued higher witnesses is not injective on
any inhabited parallel route endomorphism cell type.

The source has genuinely distinct formal pasting syntax, whereas
the observation remembers only the independently verified F44
and complete F19/F28 axis-history endpoint propositions. -/
theorem OriginalF45BracketTree.DepthRotationRoute.PresentedCell.observation_not_injective
    {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    {first : OriginalF45BracketTree n m ma pa mb pb}
    {last : OriginalF45BracketTree n' m' ma pa mb pb}
    (route : OriginalF45BracketTree.DepthRotationRoute first last) :
    ¬ Function.Injective
      (fun cell : OriginalF45BracketTree.DepthRotationRoute.PresentedCell route route =>
        cell.toOriginalF44Observation) := by
  intro hinjective
  apply OriginalF45BracketTree.DepthRotationRoute.PresentedCell.ident_ne_doubleIdent route
  apply hinjective
  exact Subsingleton.elim _ _

#print axioms OriginalF45BracketTree.DepthRotationRoute.F44ObservedCell.eq_canonical
#print axioms OriginalF45BracketTree.DepthRotationRoute.F44ObservedCell.instSubsingleton
#print axioms OriginalF45BracketTree.DepthRotationRoute.F44ObservedCell.equivPUnit
#print axioms OriginalF45BracketTree.DepthRotationRoute.PresentedCell.observation_eq
#print axioms OriginalF45BracketTree.DepthRotationRoute.PresentedCell.ident_ne_doubleIdent
#print axioms OriginalF45BracketTree.DepthRotationRoute.PresentedCell.observation_not_injective

end
end KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid
