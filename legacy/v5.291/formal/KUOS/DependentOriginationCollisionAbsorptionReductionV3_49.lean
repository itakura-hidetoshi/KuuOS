import KUOS.DependentOriginationCollisionObjectGeometryV3_48
import Mathlib.CategoryTheory.EpiMono

namespace KUOS.DependentOriginationCollisionAbsorptionReductionV3_49

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationQuotientGaugeCoordinateKeyV3_14
open KUOS.DependentOriginationFiniteAssociatorScheduleV3_38
open KUOS.DependentOriginationAssociatorIncidenceDecompositionV3_41
open KUOS.DependentOriginationFreshBoundaryCompatibilityV3_47
open KUOS.DependentOriginationCollisionObjectGeometryV3_48

universe u v

set_option autoImplicit false

noncomputable section

/-!
# Collision absorption and cancellation reduction v3.49

v3.48 proves the object geometry forced by each literal collision of the
associator leading quotient-gauge coordinate with one of its suffix
coordinates.  This layer continues only after those object identifications
have been made.

At equal endpoints, injectivity of the actual
`QuotientGaugeCoordinate.composition` constructor turns the three collision
positions into ordinary morphism equations:

* first collision: `f = f ≫ g` and `g = h`;
* second collision: `g = f ≫ g`;
* trailing collision: `f = f ≫ g` and `g ≫ h = h`.

These are absorption equations.  Standard categorical cancellation then says:

* if `f` is epi, `f = f ≫ g` forces `g = 𝟙`;
* if `h` is mono, `g ≫ h = h` forces `g = 𝟙`;
* if `g` is mono, `g = f ≫ g` forces `f = 𝟙`.

Consequently first and trailing collisions reduce to the already solved
middle-identity geometry whenever the left factor is epi (and the trailing
case also reduces when the final factor is mono).  A second collision with
mono middle arrow reduces instead to a left-identity associator.

The main residual theorem combines these directions: under `Epi a.f` and
`Mono a.g`, every v3.47 non-middle collision residual is necessarily a
left-identity associator.  This is a strict reduction of residual geometry,
not yet a proof that the left-identity sector is corrected.

No epi/mono hypothesis is inferred merely from coordinate collision.  Split
or semantic criteria may supply cancellation in later layers.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- At fixed dependent endpoints, equality of composition-coordinate keys
reflects equality of the two stored morphisms. -/
theorem compositionCoordinate_eq_sameEndpoints
    {X Y Z : W.Localization}
    {f f' : X ⟶ Y} {g g' : Y ⟶ Z}
    (h :
      (QuotientGaugeCoordinate.composition f g :
        QuotientGaugeCoordinate W) =
      QuotientGaugeCoordinate.composition f' g') :
    f = f' ∧ g = g' := by
  -- The constructor stores endpoint objects before its dependent morphism
  -- fields. Bare named `injection` hypotheses therefore begin with object
  -- equalities, while the morphism fields may be exposed through HEq.
  -- Normalize those dependent equalities before closing the homogeneous goal.
  injection h
  subst_vars
  exact ⟨rfl, rfl⟩

/-- First-collision normal form after v3.48 has identified `Y = Z = T`. -/
theorem firstCollision_absorption
    {X Y : W.Localization}
    (f : X ⟶ Y) (g h : Y ⟶ Y)
    (hCollision :
      (QuotientGaugeCoordinate.composition f g :
        QuotientGaugeCoordinate W) =
      QuotientGaugeCoordinate.composition (f ≫ g) h) :
    f = f ≫ g ∧ g = h :=
  compositionCoordinate_eq_sameEndpoints W hCollision

/-- Second-collision normal form after v3.48 has identified `X = Y`. -/
theorem secondCollision_absorption
    {X Z T : W.Localization}
    (f : X ⟶ X) (g : X ⟶ Z) (h : Z ⟶ T)
    (hCollision :
      (QuotientGaugeCoordinate.composition g h :
        QuotientGaugeCoordinate W) =
      QuotientGaugeCoordinate.composition (f ≫ g) h) :
    g = f ≫ g :=
  (compositionCoordinate_eq_sameEndpoints W hCollision).1

/-- Trailing-collision normal form after v3.48 has identified `Y = Z`. -/
theorem trailingCollision_absorption
    {X Y T : W.Localization}
    (f : X ⟶ Y) (g : Y ⟶ Y) (h : Y ⟶ T)
    (hCollision :
      (QuotientGaugeCoordinate.composition f (g ≫ h) :
        QuotientGaugeCoordinate W) =
      QuotientGaugeCoordinate.composition (f ≫ g) h) :
    f = f ≫ g ∧ g ≫ h = h :=
  compositionCoordinate_eq_sameEndpoints W hCollision

/-- Left absorption against an epi forces the endomorphism to be identity. -/
theorem endomorphism_eq_id_of_leftAbsorption_of_epi
    {X Y : W.Localization}
    (f : X ⟶ Y) (g : Y ⟶ Y) [Epi f]
    (hAbsorb : f = f ≫ g) :
    g = 𝟙 Y :=
  (cancel_epi_id f).1 hAbsorb.symm

/-- Right absorption against a mono forces the endomorphism to be identity. -/
theorem endomorphism_eq_id_of_rightAbsorption_of_mono
    {X Y : W.Localization}
    (g : X ⟶ X) (h : X ⟶ Y) [Mono h]
    (hAbsorb : g ≫ h = h) :
    g = 𝟙 X :=
  (cancel_mono_id h).1 hAbsorb

/-- Package the left-identity associator shape separately from the v3.41
middle-identity shape. -/
def leftIdentityAssociatorTask
    {X Z T : W.Localization} (g : X ⟶ Z) (h : Z ⟶ T) :
    AssociatorTask W where
  X := X
  Y := X
  Z := Z
  T := T
  f := 𝟙 X
  g := g
  h := h

/-- The sector in which the first associator arrow is literally an identity. -/
def IsLeftIdentityAssociatorTask (a : AssociatorTask W) : Prop :=
  ∃ (X Z T : W.Localization) (g : X ⟶ Z) (h : Z ⟶ T),
    a = leftIdentityAssociatorTask W g h

/-- In normalized first-collision geometry, epi cancellation makes both
endomorphisms identities, hence gives the v3.41 middle-identity sector. -/
theorem normalizedFirstCollision_isMiddleIdentity_of_epi
    {X Y : W.Localization}
    (f : X ⟶ Y) (g h : Y ⟶ Y) [Epi f]
    (hCollision :
      (QuotientGaugeCoordinate.composition f g :
        QuotientGaugeCoordinate W) =
      QuotientGaugeCoordinate.composition (f ≫ g) h) :
    IsMiddleIdentityAssociatorTask W
      ({ X := X, Y := Y, Z := Y, T := Y,
         f := f, g := g, h := h } : AssociatorTask W) := by
  have hAbsorb := firstCollision_absorption W f g h hCollision
  have hg : g = 𝟙 Y :=
    endomorphism_eq_id_of_leftAbsorption_of_epi W f g hAbsorb.1
  have hh : h = 𝟙 Y := hAbsorb.2.symm.trans hg
  subst g
  subst h
  exact ⟨X, Y, Y, f, 𝟙 Y, rfl⟩

/-- In normalized trailing geometry, epi cancellation again produces the
middle-identity associator. -/
theorem normalizedTrailingCollision_isMiddleIdentity_of_epi
    {X Y T : W.Localization}
    (f : X ⟶ Y) (g : Y ⟶ Y) (h : Y ⟶ T) [Epi f]
    (hCollision :
      (QuotientGaugeCoordinate.composition f (g ≫ h) :
        QuotientGaugeCoordinate W) =
      QuotientGaugeCoordinate.composition (f ≫ g) h) :
    IsMiddleIdentityAssociatorTask W
      ({ X := X, Y := Y, Z := Y, T := T,
         f := f, g := g, h := h } : AssociatorTask W) := by
  have hAbsorb := trailingCollision_absorption W f g h hCollision
  have hg : g = 𝟙 Y :=
    endomorphism_eq_id_of_leftAbsorption_of_epi W f g hAbsorb.1
  subst g
  exact ⟨X, Y, T, f, h, rfl⟩

/-- The same trailing collision reduces by cancellation on the final mono
factor, without any epi hypothesis on `f`. -/
theorem normalizedTrailingCollision_isMiddleIdentity_of_mono
    {X Y T : W.Localization}
    (f : X ⟶ Y) (g : Y ⟶ Y) (h : Y ⟶ T) [Mono h]
    (hCollision :
      (QuotientGaugeCoordinate.composition f (g ≫ h) :
        QuotientGaugeCoordinate W) =
      QuotientGaugeCoordinate.composition (f ≫ g) h) :
    IsMiddleIdentityAssociatorTask W
      ({ X := X, Y := Y, Z := Y, T := T,
         f := f, g := g, h := h } : AssociatorTask W) := by
  have hAbsorb := trailingCollision_absorption W f g h hCollision
  have hg : g = 𝟙 Y :=
    endomorphism_eq_id_of_rightAbsorption_of_mono W g h hAbsorb.2
  subst g
  exact ⟨X, Y, T, f, h, rfl⟩

/-- A normalized second collision with mono middle arrow forces the first
arrow to be identity.  It therefore lands in the left-identity sector, not
automatically in the already solved middle-identity sector. -/
theorem normalizedSecondCollision_isLeftIdentity_of_mono
    {X Z T : W.Localization}
    (f : X ⟶ X) (g : X ⟶ Z) (h : Z ⟶ T) [Mono g]
    (hCollision :
      (QuotientGaugeCoordinate.composition g h :
        QuotientGaugeCoordinate W) =
      QuotientGaugeCoordinate.composition (f ≫ g) h) :
    IsLeftIdentityAssociatorTask W
      ({ X := X, Y := X, Z := Z, T := T,
         f := f, g := g, h := h } : AssociatorTask W) := by
  have hAbsorb := secondCollision_absorption W f g h hCollision
  have hf : f = 𝟙 X :=
    (cancel_mono_id g).1 hAbsorb.symm
  subst f
  exact ⟨X, Z, T, g, h, rfl⟩

/-- Return from the v3.48 dependent object geometry to an arbitrary actual
first-collision task. -/
theorem firstLeadingCollision_isMiddleIdentity_of_epi
    (a : AssociatorTask W) [Epi a.f]
    (hCollision : HasAssociatorFirstLeadingCollision W a) :
    IsMiddleIdentityAssociatorTask W a := by
  have hObj :=
    firstLeadingCollision_forces_middle_and_target_objects W a hCollision
  rcases a with ⟨X, Y, Z, T, f, g, h⟩
  change Y = Z ∧ Z = T at hObj
  rcases hObj with ⟨hYZ, hZT⟩
  subst Z
  subst T
  change
    (QuotientGaugeCoordinate.composition f g :
      QuotientGaugeCoordinate W) =
    QuotientGaugeCoordinate.composition (f ≫ g) h at hCollision
  exact normalizedFirstCollision_isMiddleIdentity_of_epi
    W f g h hCollision

/-- Return from the v3.48 dependent object geometry to an arbitrary actual
trailing-collision task using epi cancellation. -/
theorem trailingLeadingCollision_isMiddleIdentity_of_epi
    (a : AssociatorTask W) [Epi a.f]
    (hCollision : HasAssociatorTrailingLeadingCollision W a) :
    IsMiddleIdentityAssociatorTask W a := by
  have hObj :=
    trailingLeadingCollision_forces_middle_objects W a hCollision
  rcases a with ⟨X, Y, Z, T, f, g, h⟩
  change Y = Z at hObj
  subst Z
  change
    (QuotientGaugeCoordinate.composition f (g ≫ h) :
      QuotientGaugeCoordinate W) =
    QuotientGaugeCoordinate.composition (f ≫ g) h at hCollision
  exact normalizedTrailingCollision_isMiddleIdentity_of_epi
    W f g h hCollision

/-- The arbitrary trailing-collision task also reduces when its final arrow
is mono. -/
theorem trailingLeadingCollision_isMiddleIdentity_of_mono
    (a : AssociatorTask W) [Mono a.h]
    (hCollision : HasAssociatorTrailingLeadingCollision W a) :
    IsMiddleIdentityAssociatorTask W a := by
  have hObj :=
    trailingLeadingCollision_forces_middle_objects W a hCollision
  rcases a with ⟨X, Y, Z, T, f, g, h⟩
  change Y = Z at hObj
  subst Z
  change
    (QuotientGaugeCoordinate.composition f (g ≫ h) :
      QuotientGaugeCoordinate W) =
    QuotientGaugeCoordinate.composition (f ≫ g) h at hCollision
  exact normalizedTrailingCollision_isMiddleIdentity_of_mono
    W f g h hCollision

/-- Return from the v3.48 dependent object geometry to an arbitrary actual
second-collision task using mono cancellation. -/
theorem secondLeadingCollision_isLeftIdentity_of_mono
    (a : AssociatorTask W) [Mono a.g]
    (hCollision : HasAssociatorSecondLeadingCollision W a) :
    IsLeftIdentityAssociatorTask W a := by
  have hObj :=
    secondLeadingCollision_forces_source_objects W a hCollision
  rcases a with ⟨X, Y, Z, T, f, g, h⟩
  change X = Y at hObj
  subst Y
  change
    (QuotientGaugeCoordinate.composition g h :
      QuotientGaugeCoordinate W) =
    QuotientGaugeCoordinate.composition (f ≫ g) h at hCollision
  exact normalizedSecondCollision_isLeftIdentity_of_mono
    W f g h hCollision

/-- With the two directional cancellation hypotheses naturally matched to
the first two arrows, every actual leading collision reduces to either the
already solved middle-identity geometry or the left-identity geometry. -/
theorem leadingCollision_reduces_to_middle_or_leftIdentity
    (a : AssociatorTask W) [Epi a.f] [Mono a.g]
    (hCollision : HasAssociatorLeadingCoordinateCollision W a) :
    IsMiddleIdentityAssociatorTask W a ∨
      IsLeftIdentityAssociatorTask W a := by
  rcases hCollision with hFirst | hSecond | hTrailing
  · exact Or.inl
      (firstLeadingCollision_isMiddleIdentity_of_epi W a hFirst)
  · exact Or.inr
      (secondLeadingCollision_isLeftIdentity_of_mono W a hSecond)
  · exact Or.inl
      (trailingLeadingCollision_isMiddleIdentity_of_epi W a hTrailing)

/-- The non-middle condition in the v3.47 collision residual eliminates the
first branch of the preceding dichotomy.  Under epi/mono cancellation, the
entire remaining collision residual is therefore forced into the
left-identity sector. -/
theorem collisionResidual_isLeftIdentity_of_epi_mono
    (a : AssociatorTask W) [Epi a.f] [Mono a.g]
    (hResidual : CollisionResidualAssociatorTask W a) :
    IsLeftIdentityAssociatorTask W a := by
  rcases
      leadingCollision_reduces_to_middle_or_leftIdentity
        W a hResidual.2 with hMiddle | hLeft
  · exact False.elim (hResidual.1 hMiddle)
  · exact hLeft

/-!
## Boundary after v3.49

The non-middle collision residual is no longer arbitrary under ordinary
categorical cancellation.  If the first arrow is epi and the middle arrow is
mono, every such residual task has first arrow equal to identity after the
actual dependent object identifications forced by v3.48.

This does not prove that every localization arrow is epi or mono, does not
derive split arrows from collision alone, and does not yet prove correction of
the left-identity associator sector.  In particular, v3.49 does not silently
replace the semantic separation hypotheses of v3.33-v3.34.

The next natural unit is to truth-test the left-identity associator against
the common unitor gauge.  If its correction follows semantically from already
correlated unitor equations, then the epi/mono-reducible collision residual
closes.  If not, the remaining compatibility equation should be exposed
explicitly rather than hidden in a broader residual predicate.

No schedule independence, seed independence, W/R/D independence, comparison
gauge equations, general Stage I, Stage II, or final DO universality is
asserted.  Protected validation-only #1558 is untouched.
-/

end

end KUOS.DependentOriginationCollisionAbsorptionReductionV3_49
