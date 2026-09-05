import KUOS.DependentOriginationHomotopyClassStrictificationV1_38
import Mathlib.AlgebraicTopology.SimplicialSet.AnodyneExtensions.Basic
import Mathlib.Data.Quot
import Mathlib.Tactic

namespace KUOS.DependentOriginationScaledHornCylinderExtensionV1_39

open CategoryTheory
open CategoryTheory.Category
open MonoidalCategory
open Simplicial
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationGlobalDuskinScaledHornCoherenceV1_22
open KUOS.DependentOriginationBiequivalencePresentationInvariantV1_26
open KUOS.DependentOriginationHomotopyClassScaledHornInvariantV1_37
open KUOS.DependentOriginationHomotopyClassStrictificationV1_38

universe u v w

/-!
# Two-sided scaled horn cylinder extension v1.39

Version 1.38 isolated homotopy-class strictification as the exact local input
needed to recover literal strict horn fibrancy from the presentation-independent
homotopy-class invariant.  This layer moves one geometric level below that
interface.

Equality in Mathlib's `RelativeMorphism.HomotopyClass` is equality in a `Quot`.
By `Quot.eqvGen_exact`, such an equality yields the equivalence closure of the
one-step relative-homotopy relation.  Therefore it is enough to be able to
move a scaled simplex across every one-step horn homotopy in both endpoint
directions.  The two-sided requirement is essential: the equivalence closure
contains formal symmetry even though a single `SSet.Homotopy` need not itself
be reversible.

We formulate that one-step transport by an actual relative cylinder extension
`Δ[n] × Δ[1] -> X`.  Restriction to the horn cylinder is the prescribed
homotopy, one endpoint is the current simplex, and the opposite endpoint is
required to remain scaled.  A simultaneous induction on `Relation.EqvGen`
then strictifies an arbitrary homotopy-class filler.

The pinned Mathlib revision already proves that every ordinary horn inclusion
is an anodyne extension.  It explicitly leaves *inner variants* of anodyne
extensions as future work, and it has no scaled-anodyne model structure.
Accordingly this file records the ordinary anodyne fact but does not mislabel
it as a scaled-anodyne theorem.  The genuinely scaled remaining input is the
cylinder-extension property below.
-/

/-! ## Relative horn maps and scaled boundary realizations -/

/-- A horn map viewed as a relative morphism between bottom subcomplexes. -/
abbrev HornRelativeMap
    (X : SSet.{u}) (n : Nat) (i : Fin (n + 1)) :=
  SSet.RelativeMorphism
    (⊥ : (Λ[n, i] : SSet.{u}).Subcomplex)
    (⊥ : X.Subcomplex)
    (SSet.Subcomplex.isInitialBot.to _)

/-- The one-step relation whose equivalence closure defines ordinary simplicial
homotopy-class equality. -/
def HornHomotopyStep
    {X : SSet.{u}} {n : Nat} {i : Fin (n + 1)}
    (f g : HornRelativeMap X n i) : Prop :=
  Nonempty (f.Homotopy g)

/-- A scaled simplex realizing one relative horn map *literally* on its
boundary.  The horn map itself need not be scaled; only the simplex is required
to preserve the chosen simplex scaling.  This is important because intermediate
representatives in a homotopy-class zigzag need not preserve the horn scaling. -/
structure ScaledHornBoundaryRealization
    {X : SSet.{u}}
    (sX : ScaledSimplicialSet X)
    {n : Nat} {i : Fin (n + 1)}
    (sΔ : ScaledSimplicialSet (Δ[n] : SSet.{u}))
    (f : HornRelativeMap X n i) where
  simplexMap : (Δ[n] : SSet.{u}) ⟶ X
  boundary_eq : f.map = Λ[n, i].ι ≫ simplexMap
  simplexMap_scaled : IsScaledMap sΔ sX simplexMap

/-! ## Genuine endpoint cylinder extensions -/

/-- Forward relative cylinder extension.  The current simplex occupies endpoint
`0`; endpoint `1` is the new scaled simplex. -/
structure ForwardScaledHornCylinderExtension
    {X : SSet.{u}}
    (sX : ScaledSimplicialSet X)
    {n : Nat} {i : Fin (n + 1)}
    (sΔ : ScaledSimplicialSet (Δ[n] : SSet.{u}))
    {f g : HornRelativeMap X n i}
    (H : f.Homotopy g)
    (Q : ScaledHornBoundaryRealization sX sΔ f) where
  extension : (Δ[n] : SSet.{u}) ⊗ Δ[1] ⟶ X
  endpoint_zero : SSet.ι₀ ≫ extension = Q.simplexMap
  on_horn : Λ[n, i].ι ▷ Δ[1] ≫ extension = H.h
  endpoint_one_scaled : IsScaledMap sΔ sX (SSet.ι₁ ≫ extension)

namespace ForwardScaledHornCylinderExtension

/-- The opposite endpoint of a forward cylinder is a literal scaled realization
of the target horn map. -/
noncomputable def toTarget
    {X : SSet.{u}}
    {sX : ScaledSimplicialSet X}
    {n : Nat} {i : Fin (n + 1)}
    {sΔ : ScaledSimplicialSet (Δ[n] : SSet.{u})}
    {f g : HornRelativeMap X n i}
    {H : f.Homotopy g}
    {Q : ScaledHornBoundaryRealization sX sΔ f}
    (E : ForwardScaledHornCylinderExtension sX sΔ H Q) :
    ScaledHornBoundaryRealization sX sΔ g where
  simplexMap := SSet.ι₁ ≫ E.extension
  boundary_eq := by
    rw [← H.h₁, ← E.on_horn]
    simp
  simplexMap_scaled := E.endpoint_one_scaled

end ForwardScaledHornCylinderExtension

/-- Backward relative cylinder extension.  The current simplex occupies endpoint
`1`; endpoint `0` is the new scaled simplex.  This second direction is what
allows formal symmetry in `EqvGen` to be handled without assuming that
simplicial homotopies are reversible. -/
structure BackwardScaledHornCylinderExtension
    {X : SSet.{u}}
    (sX : ScaledSimplicialSet X)
    {n : Nat} {i : Fin (n + 1)}
    (sΔ : ScaledSimplicialSet (Δ[n] : SSet.{u}))
    {f g : HornRelativeMap X n i}
    (H : f.Homotopy g)
    (Q : ScaledHornBoundaryRealization sX sΔ g) where
  extension : (Δ[n] : SSet.{u}) ⊗ Δ[1] ⟶ X
  endpoint_one : SSet.ι₁ ≫ extension = Q.simplexMap
  on_horn : Λ[n, i].ι ▷ Δ[1] ≫ extension = H.h
  endpoint_zero_scaled : IsScaledMap sΔ sX (SSet.ι₀ ≫ extension)

namespace BackwardScaledHornCylinderExtension

/-- The opposite endpoint of a backward cylinder is a literal scaled
realization of the source horn map. -/
noncomputable def toSource
    {X : SSet.{u}}
    {sX : ScaledSimplicialSet X}
    {n : Nat} {i : Fin (n + 1)}
    {sΔ : ScaledSimplicialSet (Δ[n] : SSet.{u})}
    {f g : HornRelativeMap X n i}
    {H : f.Homotopy g}
    {Q : ScaledHornBoundaryRealization sX sΔ g}
    (E : BackwardScaledHornCylinderExtension sX sΔ H Q) :
    ScaledHornBoundaryRealization sX sΔ f where
  simplexMap := SSet.ι₀ ≫ E.extension
  boundary_eq := by
    rw [← H.h₀, ← E.on_horn]
    simp
  simplexMap_scaled := E.endpoint_zero_scaled

end BackwardScaledHornCylinderExtension

/-! ## Cylinder-extension property for one horn problem -/

/-- A selected scaled horn problem admits two-sided one-step cylinder extension.
The property is stronger than merely producing a new endpoint: it records an
actual cylinder extending the given horn homotopy. -/
structure ScaledHornProblemCylinderExtension
    {X : SSet.{u}}
    (sX : ScaledSimplicialSet X)
    {n : Nat} {i : Fin (n + 1)}
    (P : ScaledHornExtensionProblem X sX n i) : Prop where
  forward :
    ∀ {f g : HornRelativeMap X n i}
      (H : f.Homotopy g)
      (Q : ScaledHornBoundaryRealization sX P.simplexScaling f),
      Nonempty (ForwardScaledHornCylinderExtension
        sX P.simplexScaling H Q)
  backward :
    ∀ {f g : HornRelativeMap X n i}
      (H : f.Homotopy g)
      (Q : ScaledHornBoundaryRealization sX P.simplexScaling g),
      Nonempty (BackwardScaledHornCylinderExtension
        sX P.simplexScaling H Q)

namespace ScaledHornProblemCylinderExtension

/-- Simultaneously transport literal scaled boundary realizations in both
directions along the equivalence closure of one-step horn homotopies. -/
theorem eqvGen_boundary_realization_bidir
    {X : SSet.{u}}
    {sX : ScaledSimplicialSet X}
    {n : Nat} {i : Fin (n + 1)}
    {P : ScaledHornExtensionProblem X sX n i}
    (R : ScaledHornProblemCylinderExtension sX P)
    {f g : HornRelativeMap X n i}
    (h : Relation.EqvGen HornHomotopyStep f g) :
    (Nonempty (ScaledHornBoundaryRealization sX P.simplexScaling f) →
      Nonempty (ScaledHornBoundaryRealization sX P.simplexScaling g)) ∧
    (Nonempty (ScaledHornBoundaryRealization sX P.simplexScaling g) →
      Nonempty (ScaledHornBoundaryRealization sX P.simplexScaling f)) := by
  induction h with
  | rel x y hxy =>
      rcases hxy with ⟨H⟩
      constructor
      · rintro ⟨Q⟩
        rcases R.forward H Q with ⟨E⟩
        exact ⟨E.toTarget⟩
      · rintro ⟨Q⟩
        rcases R.backward H Q with ⟨E⟩
        exact ⟨E.toSource⟩
  | refl x =>
      exact ⟨id, id⟩
  | symm x y hxy ih =>
      exact ⟨ih.2, ih.1⟩
  | trans x y z hxy hyz ihxy ihyz =>
      exact
        ⟨fun hx => ihyz.1 (ihxy.1 hx),
         fun hz => ihxy.2 (ihyz.2 hz)⟩

/-- Two-sided cylinder extension strictifies an arbitrary homotopy-class
filler of this horn problem. -/
noncomputable def strictify
    {X : SSet.{u}}
    {sX : ScaledSimplicialSet X}
    {n : Nat} {i : Fin (n + 1)}
    {P : ScaledHornExtensionProblem X sX n i}
    (R : ScaledHornProblemCylinderExtension sX P)
    (Q : HomotopyClassScaledHornFiller P) :
    Nonempty (ScaledHornFiller P) := by
  let f : HornRelativeMap X n i :=
    SSet.RelativeMorphism.botEquiv.symm
      (Λ[n, i].ι ≫ Q.simplexMap)
  let g : HornRelativeMap X n i :=
    SSet.RelativeMorphism.botEquiv.symm P.hornMap
  have hEqv : Relation.EqvGen HornHomotopyStep f g := by
    change Relation.EqvGen
      (fun a b : HornRelativeMap X n i => Nonempty (a.Homotopy b)) f g
    simpa [f, g, homotopyClassOfMap] using
      (Quot.eqvGen_exact Q.boundary_class_eq)
  have hStart :
      Nonempty (ScaledHornBoundaryRealization
        sX P.simplexScaling f) := by
    exact ⟨{
      simplexMap := Q.simplexMap
      boundary_eq := by rfl
      simplexMap_scaled := Q.simplexMap_scaled
    }⟩
  rcases (R.eqvGen_boundary_realization_bidir hEqv).1 hStart with ⟨S⟩
  exact ⟨{
    simplexMap := S.simplexMap
    extends_horn := by simpa [g] using S.boundary_eq
    simplexMap_scaled := S.simplexMap_scaled
  }⟩

end ScaledHornProblemCylinderExtension

/-! ## Family-local and universal cylinder extension -/

/-- Two-sided cylinder extension for every problem selected by one horn family. -/
structure ScaledHornFamilyCylinderExtension
    {X : SSet.{u}}
    (sX : ScaledSimplicialSet X)
    (F : ScaledHornFamily X sX) : Prop where
  extension :
    ∀ {n : Nat} {i : Fin (n + 1)}
      (P : ScaledHornExtensionProblem X sX n i),
      F.admissible P →
      ScaledHornProblemCylinderExtension sX P

namespace ScaledHornFamilyCylinderExtension

/-- Geometric cylinder extension implies the family-local class
strictification interface of v1.38. -/
noncomputable def toStrictification
    {X : SSet.{u}}
    {sX : ScaledSimplicialSet X}
    {F : ScaledHornFamily X sX}
    (R : ScaledHornFamilyCylinderExtension sX F) :
    ScaledHornFamilyHomotopyClassStrictification X sX F where
  strictify := by
    intro n i P hP hQ
    rcases hQ with ⟨Q⟩
    exact (R.extension P hP).strictify Q

end ScaledHornFamilyCylinderExtension

/-- Universal two-sided cylinder extension for every scaled horn problem. -/
structure UniversalScaledHornCylinderExtension
    (X : SSet.{u})
    (sX : ScaledSimplicialSet X) : Prop where
  extension :
    ∀ {n : Nat} {i : Fin (n + 1)}
      (P : ScaledHornExtensionProblem X sX n i),
      ScaledHornProblemCylinderExtension sX P

namespace UniversalScaledHornCylinderExtension

/-- Universal cylinder extension restricts to every chosen horn family. -/
def toFamily
    {X : SSet.{u}}
    {sX : ScaledSimplicialSet X}
    (R : UniversalScaledHornCylinderExtension X sX)
    (F : ScaledHornFamily X sX) :
    ScaledHornFamilyCylinderExtension sX F where
  extension := by
    intro n i P hP
    exact R.extension P

/-- Universal cylinder extension implies universal homotopy-class
strictification. -/
noncomputable def toStrictification
    {X : SSet.{u}}
    {sX : ScaledSimplicialSet X}
    (R : UniversalScaledHornCylinderExtension X sX) :
    UniversalScaledHornHomotopyClassStrictification X sX where
  strictify := by
    intro n i P hQ
    rcases hQ with ⟨Q⟩
    exact (R.extension P).strictify Q

end UniversalScaledHornCylinderExtension

/-! ## Canonical all-problem inner-horn presentation -/

/-- The canonical family admitting every scaled horn problem.  Innerness is
still imposed by the `0 < i` and `i < last` hypotheses in the filler
predicates, so this is the all-problem *inner* presentation without choosing a
particular Lurie scaled-anodyne generator list. -/
def canonicalInnerScaledHornFamily
    (X : SSet.{u})
    (sX : ScaledSimplicialSet X) :
    ScaledHornFamily X sX where
  admissible := fun _ => True

/-- Every underlying ordinary inner-horn inclusion occurring here is an
ordinary Mathlib anodyne extension.  This does **not** assert a scaled-anodyne
or inner-anodyne model structure. -/
theorem underlying_innerHorn_anodyne
    {n : Nat} {i : Fin (n + 1)}
    (h0 : 0 < i) :
    SSet.anodyneExtensions.{u} Λ[n, i].ι := by
  letI : NeZero n := ⟨by omega⟩
  exact SSet.anodyneExtensions.horn_ι i

/-! ## Presentation-independent strict fibrancy from geometric cylinders -/

open KUOS.DependentOriginationGlobalDuskinScaledNerveV1_21
open KUOS.DependentOriginationStrictlyUnitaryDuskinModelTransportV1_27
open KUOS.DependentOriginationCoherentNormalizedScaledModelEquivalenceV1_32

/-- A coherent normalized scaled model equivalence whose two presentations
support the geometric two-sided cylinder extension needed for strictification. -/
structure CoherentNormalizedScaledCylinderExtendableModelEquivalence
    {B C : Type u}
    [Bicategory.{w, v} B] [Bicategory.{w, v} C]
    (E : BicategoricalModelEquivalence B C)
    (G : BicategoricalModelEquivalence C B)
    (HB : GlobalDuskinScaledHornFamily B)
    (HC : GlobalDuskinScaledHornFamily C) where
  homotopyClassModel :
    CoherentNormalizedScaledHomotopyClassModelEquivalence E G HB HC
  sourceCylinderExtension :
    ScaledHornFamilyCylinderExtension
      (duskinScaling B) HB
  targetCylinderExtension :
    ScaledHornFamilyCylinderExtension
      (duskinScaling C) HC

namespace CoherentNormalizedScaledCylinderExtendableModelEquivalence

variable
    {B C : Type u}
    [Bicategory.{w, v} B] [Bicategory.{w, v} C]
    {E : BicategoricalModelEquivalence B C}
    {G : BicategoricalModelEquivalence C B}
    {HB : GlobalDuskinScaledHornFamily B}
    {HC : GlobalDuskinScaledHornFamily C}
    (K : CoherentNormalizedScaledCylinderExtendableModelEquivalence E G HB HC)

/-- Forget the geometric witness after deriving the v1.38 strictification
package. -/
noncomputable def toStrictifiableModelEquivalence :
    CoherentNormalizedScaledStrictifiableModelEquivalence E G HB HC where
  homotopyClassModel := K.homotopyClassModel
  sourceStrictification := K.sourceCylinderExtension.toStrictification
  targetStrictification := K.targetCylinderExtension.toStrictification

include K in
/-- Strict global scaled-Duskin fibrancy is presentation-independent under the
geometric two-sided cylinder-extension principle. -/
theorem globalDuskinStrictFibrancy_iff :
    HasScaledHornFillers (duskinNerve B) (duskinScaling B) HB ↔
      HasScaledHornFillers (duskinNerve C) (duskinScaling C) HC :=
  K.toStrictifiableModelEquivalence.globalDuskinStrictFibrancy_iff

end CoherentNormalizedScaledCylinderExtendableModelEquivalence

/-!
The strict-fibrancy spine is now factored geometrically:

```text
homotopy-class boundary equality
  -> Quot.eqvGen_exact
  -> equivalence closure of one-step horn homotopies

two-sided relative horn cylinder extension
  -> strict transport across rel / refl / symm / trans
  -> family-local homotopy-class strictification
  -> strict fibrancy = homotopy-class fibrancy

coherent normalized scaled model equivalence
  -> presentation-independent homotopy-class fibrancy
  + cylinder extension on both presentations
  -> presentation-independent strict scaled fibrancy.
```

Pinned Mathlib supplies ordinary horn anodyne extensions, but its own
`AnodyneExtensions.Basic` file still lists inner variants as TODO and contains
no scaled-anodyne model structure.  The remaining independent theorem is
therefore sharply identified: prove the two-sided *scaled* cylinder-extension
property for a concrete standard scaled-anodyne generator presentation.
-/

end KUOS.DependentOriginationScaledHornCylinderExtensionV1_39