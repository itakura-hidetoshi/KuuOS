import Kuu.Incidence

/-! # Concrete noncollapse and replacement checks on independent boundary data -/
namespace Kuu.Checks
open CategoryTheory
set_option autoImplicit false

inductive Point where
  | source | target

inductive Step : Point → Point → Type where
  | first : Step .source .target
  | second : Step .source .target

instance : Quiver Point := ⟨Step⟩

def firstPath : Quiver.Path Point.source Point.target :=
  Quiver.Hom.toPath Step.first

def secondPath : Quiver.Path Point.source Point.target :=
  Quiver.Hom.toPath Step.second

theorem raw_distinct : firstPath ≠ secondPath := by
  intro h
  have hcons :
      (Quiver.Path.nil : Quiver.Path Point.source Point.source).cons
          (Step.first : Step Point.source Point.target) =
      (Quiver.Path.nil : Quiver.Path Point.source Point.source).cons
          (Step.second : Step Point.source Point.target) := by
    exact h
  have he : (Step.first : Step Point.source Point.target) = Step.second :=
    eq_of_heq (Quiver.Path.hom_heq_of_cons_eq_cons hcons)
  cases he

theorem quotient_not_indiscrete :
    (project Point (identityRelations Point)).map firstPath ≠
      (project Point (identityRelations Point)).map secondPath := by
  intro h
  exact raw_distinct ((identity_projection_reflects firstPath secondPath).mp h)

def declared : Relations Point := fun {_ _} _ _ => True

theorem declared_paths_replace :
    (project Point declared).map firstPath = (project Point declared).map secondPath :=
  declared_replacement declared True.intro

#print axioms raw_distinct
#print axioms quotient_not_indiscrete
#print axioms declared_paths_replace
end Kuu.Checks
