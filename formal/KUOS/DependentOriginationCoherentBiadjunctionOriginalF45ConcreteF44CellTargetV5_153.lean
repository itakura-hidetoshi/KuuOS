import KUOS.DependentOriginationCoherentBiadjunctionOriginalF45HigherCellPastingObstructionV5_153

namespace KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionExchangeQuotientConcatenationV5_141.Grid

set_option autoImplicit false
noncomputable section

/-!
# F56-C / v5.153 — a CONCRETE original F44 / complete-history target

F56-A's HigherCellTarget is a conditional higher interpretation
interface, with independently provided pentagon, square, vertical
composition and contextual whiskering operations. A general external
tricategorical/Gray-categorical target still needs an explicit model.

Here we prove the interface is actually inhabited by a very precise,
honest *OBSERVATIONAL TRUNCATION* target: each 2-path comparison is
interpreted by FOUR certified equalities, the original F44 generated
exchange classes for both routes and their two independently typed
FULL F19/F28 original histories after both exact depth transports.

The target's cells are a genuine Type-valued structure of original
mathematical proof certificates, not unrestricted external 3-cells.
Every constructor is supplied by F55-C's actual route invariants.
The interpretation FORGETS the higher path's internal pentagon/square
shape and does not identify distinct raw rotation routes.
-/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

/-- Concrete, independently defined certificates interpreting the
two boundaries of a parallel pair of typed original F55 finite paths.
Each side retains its own F19 and F28 exact Nat-depth transports.

The proof certificates are in Type, but their individual statements
are Prop-valued: this is an observational truncation, NOT a claim that
all free F55 higher cells are equal or externally realized. -/
structure OriginalF45BracketTree.DepthRotationRoute.F44ObservedCell
    {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    {first : OriginalF45BracketTree n m ma pa mb pb}
    {last : OriginalF45BracketTree n' m' ma pa mb pb}
    (r s : OriginalF45BracketTree.DepthRotationRoute first last) :
    Type (max (max uD uE) (max vD vE)) where
  firstClass :
    ExchangeClass.castDepths r.depthEq.1 r.depthEq.2
      first.toExchangeClass = last.toExchangeClass
  secondClass :
    ExchangeClass.castDepths s.depthEq.1 s.depthEq.2
      first.toExchangeClass = last.toExchangeClass
  firstHistories :
    (OriginalF45BracketTree.castDepths
      r.depthEq.1 r.depthEq.2 first).axisHistories =
      last.axisHistories
  secondHistories :
    (OriginalF45BracketTree.castDepths
      s.depthEq.1 s.depthEq.2 first).axisHistories =
      last.axisHistories

/-- ANY two typed original F55 routes with the same original boundary
canonically yield the genuine generated F44 and BOTH complete
independent F19/F28 axis-history certificates, by proved theorems. -/
def OriginalF45BracketTree.DepthRotationRoute.F44ObservedCell.canonical
    {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    {first : OriginalF45BracketTree n m ma pa mb pb}
    {last : OriginalF45BracketTree n' m' ma pa mb pb}
    (r s : OriginalF45BracketTree.DepthRotationRoute first last) :
    OriginalF45BracketTree.DepthRotationRoute.F44ObservedCell r s :=
  ⟨r.toExchangeClass_eq, s.toExchangeClass_eq,
   r.axisHistories_eq, s.axisHistories_eq⟩

/-- A fully CONSTRUCTED instance of the F56-A target: its 2-path
comparison witnesses are the original F44/complete-history
certificates. Pentagon/square and all closure operations are realized
by the already proved invariance of the actual endpoint routes.

This is an authentic model of the F56 interface but NOT a
nontrivial target tricategory/Gray-category 3-cell semantics. -/
def OriginalF45BracketTree.DepthRotationRoute.HigherCellTarget.originalF44 :
    OriginalF45BracketTree.DepthRotationRoute.HigherCellTarget D E where
  Cell := fun {a b} {x y} {n n' m m'} {ma mb} {pa pb}
      {first last} r s =>
    OriginalF45BracketTree.DepthRotationRoute.F44ObservedCell r s
  ident := fun route =>
    OriginalF45BracketTree.DepthRotationRoute.F44ObservedCell.canonical route route
  pentagon := fun t₁ t₂ t₃ t₄ =>
    OriginalF45BracketTree.DepthRotationRoute.F44ObservedCell.canonical
      (OriginalF45BracketTree.DepthRotationRoute.pentagonLong t₁ t₂ t₃ t₄)
      (OriginalF45BracketTree.DepthRotationRoute.pentagonShort t₁ t₂ t₃ t₄)
  disjointSquare := fun left right =>
    OriginalF45BracketTree.DepthRotationRoute.F44ObservedCell.canonical
      (OriginalF45BracketTree.DepthRotationRoute.squareLeftFirst left right)
      (OriginalF45BracketTree.DepthRotationRoute.squareRightFirst left right)
  symm := fun _ =>
    OriginalF45BracketTree.DepthRotationRoute.F44ObservedCell.canonical _ _
  trans := fun _ _ =>
    OriginalF45BracketTree.DepthRotationRoute.F44ObservedCell.canonical _ _
  leftContext := fun _ _ =>
    OriginalF45BracketTree.DepthRotationRoute.F44ObservedCell.canonical _ _
  rightContext := fun _ _ =>
    OriginalF45BracketTree.DepthRotationRoute.F44ObservedCell.canonical _ _
  precompose := fun _ _ =>
    OriginalF45BracketTree.DepthRotationRoute.F44ObservedCell.canonical _ _
  postcompose := fun _ _ =>
    OriginalF45BracketTree.DepthRotationRoute.F44ObservedCell.canonical _ _

/-- Interpreting ANY freely presented F55 higher path in this
concrete original target actually yields both original F44 equality
certificates and the FULL native two-axis history certificates. -/
def OriginalF45BracketTree.DepthRotationRoute.PresentedCell.toOriginalF44Observation
    {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    {first : OriginalF45BracketTree n m ma pa mb pb}
    {last : OriginalF45BracketTree n' m' ma pa mb pb}
    {r s : OriginalF45BracketTree.DepthRotationRoute first last}
    (cell : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r s) :
    OriginalF45BracketTree.DepthRotationRoute.F44ObservedCell r s :=
  cell.interpret OriginalF45BracketTree.DepthRotationRoute.HigherCellTarget.originalF44

/-- A concretely interpreted higher cell has the SAME certified
first-route F44 equality as the independently established F55-C
route theorem. We do not identify the source higher-cell evidence. -/
theorem OriginalF45BracketTree.DepthRotationRoute.PresentedCell.toOriginalF44Observation_first
    {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    {first : OriginalF45BracketTree n m ma pa mb pb}
    {last : OriginalF45BracketTree n' m' ma pa mb pb}
    {r s : OriginalF45BracketTree.DepthRotationRoute first last}
    (cell : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r s) :
    cell.toOriginalF44Observation.firstClass = r.toExchangeClass_eq := by
  apply Subsingleton.elim

/-- The second-route original F28/F19 double-depth F44 equality
certificate is likewise exactly the F55-C invariant proposition. -/
theorem OriginalF45BracketTree.DepthRotationRoute.PresentedCell.toOriginalF44Observation_second
    {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    {first : OriginalF45BracketTree n m ma pa mb pb}
    {last : OriginalF45BracketTree n' m' ma pa mb pb}
    {r s : OriginalF45BracketTree.DepthRotationRoute first last}
    (cell : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r s) :
    cell.toOriginalF44Observation.secondClass = s.toExchangeClass_eq := by
  apply Subsingleton.elim

#print axioms OriginalF45BracketTree.DepthRotationRoute.F44ObservedCell
#print axioms OriginalF45BracketTree.DepthRotationRoute.F44ObservedCell.canonical
#print axioms OriginalF45BracketTree.DepthRotationRoute.HigherCellTarget.originalF44
#print axioms OriginalF45BracketTree.DepthRotationRoute.PresentedCell.toOriginalF44Observation
#print axioms OriginalF45BracketTree.DepthRotationRoute.PresentedCell.toOriginalF44Observation_first
#print axioms OriginalF45BracketTree.DepthRotationRoute.PresentedCell.toOriginalF44Observation_second

end
end KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid
