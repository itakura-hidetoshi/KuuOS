import KUOS.DependentOriginationFreshBoundaryCompatibilityV3_47

namespace KUOS.DependentOriginationCollisionObjectGeometryV3_48

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationPointwiseWAdjointEquivalenceV2_56
open KUOS.DependentOriginationQuotientGaugeIndependenceV3_03
open KUOS.DependentOriginationQuotientGaugeIntersectionObstructionV3_11
open KUOS.DependentOriginationQuotientGaugeCoordinateKeyV3_14
open KUOS.DependentOriginationUnitorWitnessCorrelationV3_35
open KUOS.DependentOriginationFreshAssociatorCompletionV3_37
open KUOS.DependentOriginationFiniteAssociatorScheduleV3_38
open KUOS.DependentOriginationAssociatorIncidenceDecompositionV3_41
open KUOS.DependentOriginationFreshBoundaryCompatibilityV3_47

universe u v uH vH

set_option autoImplicit false

noncomputable section

/-!
# Actual collision object geometry v3.48

v3.47 leaves one local residual shape after the fresh-boundary compatibility
equations are imposed: a non-middle associator whose selected leading quotient
gauge coordinate is literally equal to one of the three suffix coordinates.

This layer truth-tests those equalities as equalities of the actual dependent
`QuotientGaugeCoordinate` keys.  It does not cancel dependent constructor
arguments by hand.  Instead it first projects a coordinate to its source,
middle, and target localization objects.

The three collision positions then have unavoidable object geometry:

* first suffix = leading forces both `Y = Z` and `Z = T`;
* second suffix = leading forces `X = Y`;
* trailing suffix = leading forces `Y = Z`.

Hence every leading collision lies over an adjacent object degeneracy
`X = Y ∨ Y = Z`.  In particular, if both adjacent object boundaries are
separated, the task is automatically fresh and cannot belong to the v3.47
collision residual.

This is deliberately weaker than saying that any morphism is an identity.
No split epi/mono, cancellation, semantic EssSurj/Faithful, or unitor
reduction is inferred from object equality alone.  Those are the next
possible reduction mechanisms.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- Source object remembered by a quotient-gauge coordinate.  Identity keys
use their unique object as source. -/
def quotientCoordinateSource : QuotientGaugeCoordinate W → W.Localization
  | .identity X => X
  | .composition (X := X) _ _ => X

/-- Target object remembered by a quotient-gauge coordinate.  Identity keys
use their unique object as target. -/
def quotientCoordinateTarget : QuotientGaugeCoordinate W → W.Localization
  | .identity X => X
  | .composition (Z := Z) _ _ => Z

/-- Collision with the first suffix coordinate `composition f g`. -/
def HasAssociatorFirstLeadingCollision (a : AssociatorTask W) : Prop :=
  associatorTaskFirstSuffixCoordinate W a =
    associatorTaskLeadingCoordinate W a

/-- Collision with the second suffix coordinate `composition g h`. -/
def HasAssociatorSecondLeadingCollision (a : AssociatorTask W) : Prop :=
  associatorTaskSecondSuffixCoordinate W a =
    associatorTaskLeadingCoordinate W a

/-- Collision with the trailing suffix coordinate `composition f (g ≫ h)`. -/
def HasAssociatorTrailingLeadingCollision (a : AssociatorTask W) : Prop :=
  associatorTaskTrailingCoordinate W a =
    associatorTaskLeadingCoordinate W a

/-- The v3.41 collision predicate is exactly the three literal positions. -/
theorem hasAssociatorLeadingCoordinateCollision_iff_three_positions
    (a : AssociatorTask W) :
    HasAssociatorLeadingCoordinateCollision W a ↔
      HasAssociatorFirstLeadingCollision W a ∨
      HasAssociatorSecondLeadingCollision W a ∨
      HasAssociatorTrailingLeadingCollision W a := by
  rfl

/-- A first-suffix collision forces two consecutive object identifications.
This follows only from projecting the dependent coordinate equality. -/
theorem firstLeadingCollision_forces_middle_and_target_objects
    (a : AssociatorTask W)
    (hCollision : HasAssociatorFirstLeadingCollision W a) :
    a.Y = a.Z ∧ a.Z = a.T := by
  constructor
  · have hMiddle :=
      congrArg (quotientCoordinateMiddle W) hCollision
    simpa [HasAssociatorFirstLeadingCollision,
      associatorTaskFirstSuffixCoordinate, associatorTaskLeadingCoordinate,
      quotientCoordinateMiddle] using hMiddle
  · have hTarget :=
      congrArg (quotientCoordinateTarget W) hCollision
    simpa [HasAssociatorFirstLeadingCollision,
      associatorTaskFirstSuffixCoordinate, associatorTaskLeadingCoordinate,
      quotientCoordinateTarget] using hTarget

/-- A second-suffix collision forces the left adjacent objects to coincide. -/
theorem secondLeadingCollision_forces_source_objects
    (a : AssociatorTask W)
    (hCollision : HasAssociatorSecondLeadingCollision W a) :
    a.X = a.Y := by
  have hSource :=
    congrArg (quotientCoordinateSource W) hCollision
  simpa [HasAssociatorSecondLeadingCollision,
    associatorTaskSecondSuffixCoordinate, associatorTaskLeadingCoordinate,
    quotientCoordinateSource] using hSource.symm

/-- A trailing-suffix collision forces the middle adjacent objects to coincide. -/
theorem trailingLeadingCollision_forces_middle_objects
    (a : AssociatorTask W)
    (hCollision : HasAssociatorTrailingLeadingCollision W a) :
    a.Y = a.Z := by
  have hMiddle :=
    congrArg (quotientCoordinateMiddle W) hCollision
  simpa [HasAssociatorTrailingLeadingCollision,
    associatorTaskTrailingCoordinate, associatorTaskLeadingCoordinate,
    quotientCoordinateMiddle] using hMiddle

/-- Every actual leading collision therefore lies over a left or middle object
degeneracy.  No morphism-level identity statement is used. -/
theorem leadingCollision_forces_adjacent_object_degeneracy
    (a : AssociatorTask W)
    (hCollision : HasAssociatorLeadingCoordinateCollision W a) :
    a.X = a.Y ∨ a.Y = a.Z := by
  rcases hCollision with hFirst | hSecond | hTrailing
  · exact Or.inr
      (firstLeadingCollision_forces_middle_and_target_objects
        W a hFirst).1
  · exact Or.inl
      (secondLeadingCollision_forces_source_objects W a hSecond)
  · exact Or.inr
      (trailingLeadingCollision_forces_middle_objects W a hTrailing)

/-- Object-level region in which the two adjacent boundaries relevant to the
collision projection are both separated. -/
def CollisionObjectSeparated (a : AssociatorTask W) : Prop :=
  a.X ≠ a.Y ∧ a.Y ≠ a.Z

/-- Object separation rules out all three actual leading-coordinate collisions. -/
theorem collisionObjectSeparated_not_leadingCollision
    (a : AssociatorTask W)
    (hSeparated : CollisionObjectSeparated W a) :
    ¬ HasAssociatorLeadingCoordinateCollision W a := by
  intro hCollision
  rcases leadingCollision_forces_adjacent_object_degeneracy
      W a hCollision with hXY | hYZ
  · exact hSeparated.1 hXY
  · exact hSeparated.2 hYZ

/-- In the object-separated region, v3.37 freshness follows automatically from
the exact v3.41 collision characterization. -/
theorem freshAssociatorLeadingCoordinate_of_collisionObjectSeparated
    (a : AssociatorTask W)
    (hSeparated : CollisionObjectSeparated W a) :
    FreshAssociatorLeadingCoordinate W a.f a.g a.h := by
  classical
  by_contra hNotFresh
  exact
    collisionObjectSeparated_not_leadingCollision W a hSeparated
      ((not_fresh_iff_hasAssociatorLeadingCoordinateCollision W a).1 hNotFresh)

/-- A v3.47 collision residual can occur only over the same adjacent object
degeneracy.  The non-middle condition is retained but is not needed for this
projection. -/
theorem collisionResidual_forces_adjacent_object_degeneracy
    (a : AssociatorTask W)
    (hResidual : CollisionResidualAssociatorTask W a) :
    a.X = a.Y ∨ a.Y = a.Z :=
  leadingCollision_forces_adjacent_object_degeneracy W a hResidual.2

/-- Consequently an object-separated task is outside the v3.47 collision
residual, independently of whether it lies on the fresh unitor boundary. -/
theorem collisionObjectSeparated_not_collisionResidual
    (a : AssociatorTask W)
    (hSeparated : CollisionObjectSeparated W a) :
    ¬ CollisionResidualAssociatorTask W a := by
  intro hResidual
  exact collisionObjectSeparated_not_leadingCollision W a hSeparated hResidual.2

variable (R : RawHigherContextualSystem.{u, v, uH, vH}
  (Context := Context))
variable (D : PointwiseWAdjointEquivalenceData (W := W) R)

/-- Reuse the v3.47 common-gauge result on the whole object-separated region.
The only additional input here is the proved absence of collision residual. -/
theorem corrected_of_collisionObjectSeparated_of_boundaryCompatible
    (Q : GeneratedQuotientGaugeParameters W R D)
    (hNonresidual :
      ∀ a : AssociatorTask W,
        ¬ ResidualAssociatorIncidence W a →
          Q ∈ quotientRouteCorrectionLocus W R D (associatorTaskRoute W a))
    (hBoundaryCompatible :
      ∀ a : AssociatorTask W,
        FreshBoundaryAssociatorTask W a →
          AssociatorLeadingCompatible W R D Q a.f a.g a.h)
    (a : AssociatorTask W)
    (hSeparated : CollisionObjectSeparated W a) :
    Q ∈ quotientRouteCorrectionLocus W R D (associatorTaskRoute W a) := by
  exact
    corrects_all_except_collisionResidual_of_boundaryCompatible
      W R D Q hNonresidual hBoundaryCompatible a
        (collisionObjectSeparated_not_collisionResidual W a hSeparated)

/-!
## Boundary after v3.48

The actual dependent-key collision sector has now been projected to a strict
object-level necessary geometry.  Any remaining collision residual must live
where `X = Y` or `Y = Z`; a first-suffix collision is even more degenerate,
forcing `Y = Z = T`.

These implications are one-way.  Object equality does not imply coordinate
collision, and none of the proved object equalities makes `f`, `g`, or `h`
an identity.  In particular v3.33-v3.34 split-arrow or semantic separation
hypotheses are not manufactured here.

The next collision unit should inspect constructor injectivity after the
proved object identifications.  The expected morphism-level normal forms are
absorption equations such as `f ≫ g = f` and `g ≫ h = h`.  Only after those
equations are formal should epi/mono or split cancellation be used to test
which collision components reduce to the already solved middle-identity
sector and which remain genuine obstructions.

No schedule independence, seed independence, W/R/D independence, comparison
gauge equations, general Stage I, Stage II, or final DO universality is
asserted.  Protected validation-only #1558 is untouched.
-/

end

end KUOS.DependentOriginationCollisionObjectGeometryV3_48
