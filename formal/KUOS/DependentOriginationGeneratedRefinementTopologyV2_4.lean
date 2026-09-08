import Mathlib
import KUOS.DependentOriginationEffectiveDescentComparisonV2_1
import KUOS.DependentOriginationOppositeSiteVarianceBridgeV2_3

namespace KUOS.DependentOriginationGeneratedRefinementTopologyV2_4

open CategoryTheory
open Opposite
open Limits
open KUOS.DependentOriginationFunctorialTransportV0_1
open KUOS.DependentOriginationContextualDescentV1_1
open KUOS.DependentOriginationEffectiveDescentComparisonV2_1
open KUOS.DependentOriginationOppositeSiteVarianceBridgeV2_3

universe u v w

/-!
# Dependent-origination generated refinement topology v2.4

The v2.3 bridge reinterprets KuuOS covariant contextual transport as an ordinary
presheaf on the opposite context category.  This file adds the next exact layer:
KuuOS refinement families become covering presieves on that opposite site, and
Mathlib's `Precoverage.toGrothendieck` freely generates the Grothendieck topology
forced by those declared refinements.

There is one important mathematical boundary.  The old `OverlapSystem` records a
chosen common refinement of two charts, but does not assert a universal property.
Mathlib's matching-family compatibility quantifies over *every* common refinement.
Those notions agree when each chosen overlap square is a pushout in the original
context category (equivalently a pullback after passing to the opposite site).
We therefore state that extra geometric condition explicitly rather than silently
identifying arbitrary common refinements with categorical overlaps.
-/

section OneCover

variable {Context : Type u} [Category.{v} Context]
variable {Index : Type w}

/-- A covariant KuuOS refinement family, viewed as a standard covering presieve
on the opposite refinement site. -/
def coverPresieve (C : RefinementCover Context Index) :
    Presieve (op C.rootContext) :=
  Presieve.ofArrows
    (fun i : Index => op (C.chart i))
    (fun i => (C.toChart i).op)

/-- The chosen pairwise overlaps are genuine categorical overlaps precisely when
each commuting square is a pushout in the original covariant context category. -/
def IsPushoutOverlapSystem
    (C : RefinementCover Context Index)
    (O : OverlapSystem C) : Prop :=
  ∀ i j,
    IsPushout
      (C.toChart i)
      (C.toChart j)
      (O.leftToMeet i j)
      (O.rightToMeet i j)

/-- Under the pushout-overlap condition, KuuOS pairwise compatibility at the
chosen overlaps is exactly Mathlib matching-family compatibility for the
opposite-site covering family. -/
theorem arrowsCompatible_iff_overlapCompatible
    (D : FunctorialTransportSystem Context)
    (C : RefinementCover Context Index)
    (O : OverlapSystem C)
    (hpush : IsPushoutOverlapSystem C O)
    (s : (i : Index) → D.state.obj (C.chart i)) :
    Presieve.Arrows.Compatible
        (asOppositeSitePresheaf D)
        (fun i : Index => (C.toChart i).op)
        s ↔
      (∀ i j,
        D.transport (O.leftToMeet i j) (s i) =
          D.transport (O.rightToMeet i j) (s j)) := by
  constructor
  · intro h i j
    have h' := h i j (op (O.meet i j))
      (O.leftToMeet i j).op (O.rightToMeet i j).op (by
        apply Quiver.Hom.unop_inj
        simpa using O.root_path_coherent i j)
    simpa using h'
  · intro h i j Z gi gj hcomm
    have hcomm' :
        C.toChart i ≫ gi.unop = C.toChart j ≫ gj.unop := by
      have := congrArg Quiver.Hom.unop hcomm
      simpa using this
    let d : O.meet i j ⟶ unop Z :=
      (hpush i j).desc gi.unop gj.unop hcomm'
    change D.transport gi.unop (s i) = D.transport gj.unop (s j)
    calc
      D.transport gi.unop (s i) =
          D.transport d (D.transport (O.leftToMeet i j) (s i)) := by
            rw [← D.transport_comp_apply]
            rw [(hpush i j).inl_desc]
      _ = D.transport d (D.transport (O.rightToMeet i j) (s j)) :=
        congrArg (D.transport d) (h i j)
      _ = D.transport gj.unop (s j) := by
        rw [← D.transport_comp_apply]
        rw [(hpush i j).inr_desc]

/-- For a genuine pushout overlap system, the elementary v2.1 effective descent
condition is exactly the ordinary Type-valued sheaf condition for this single
covering presieve. -/
theorem cover_isSheafFor_iff_effectiveStateDescent
    (D : FunctorialTransportSystem Context)
    (C : RefinementCover Context Index)
    (O : OverlapSystem C)
    (hpush : IsPushoutOverlapSystem C O) :
    Presieve.IsSheafFor (asOppositeSitePresheaf D) (coverPresieve C) ↔
      HasEffectiveStateDescent D C O := by
  rw [coverPresieve, Presieve.isSheafFor_arrows_iff]
  constructor
  · intro h
    refine ⟨?_, ?_⟩
    · intro s hs
      have hcompat : Presieve.Arrows.Compatible
          (asOppositeSitePresheaf D)
          (fun i : Index => (C.toChart i).op)
          s.state :=
        (arrowsCompatible_iff_overlapCompatible D C O hpush s.state).2 hs
      obtain ⟨x, hx, _⟩ := h s.state hcompat
      refine ⟨x, ?_⟩
      intro i
      simpa using hx i
    · intro x y hxy
      let s : (i : Index) → D.state.obj (C.chart i) :=
        fun i => D.transport (C.toChart i) x
      have hs : ∀ i j,
          D.transport (O.leftToMeet i j) (s i) =
            D.transport (O.rightToMeet i j) (s j) := by
        intro i j
        exact root_transport_to_overlap_coherent D C O x i j
      have hcompat : Presieve.Arrows.Compatible
          (asOppositeSitePresheaf D)
          (fun i : Index => (C.toChart i).op)
          s :=
        (arrowsCompatible_iff_overlapCompatible D C O hpush s).2 hs
      obtain ⟨t, _, ht_unique⟩ := h s hcompat
      have hx : x = t := ht_unique x (by
        intro i
        rfl)
      have hy : y = t := ht_unique y (by
        intro i
        simpa [s] using hxy i)
      exact hx.trans hy.symm
  · rintro ⟨hdescent, hseparate⟩ s hs
    let local : LocalStateFamily D C := ⟨s⟩
    have hlocal : OverlapCompatible D C O local :=
      (arrowsCompatible_iff_overlapCompatible D C O hpush s).1 hs
    have hunique := existsUnique_globalState_of_descent_and_separation
      D C O hdescent hseparate local hlocal
    simpa [local] using hunique

end OneCover

section Atlas

variable (Context : Type u) [Category.{v} Context]

/-- A uniform declaration of one refinement family above every context.  No
base-change or composition axiom is imposed here; `Precoverage.toGrothendieck`
will freely add exactly the closure demanded by a Grothendieck topology. -/
structure RefinementAtlas where
  Index : Context → Type w
  chart : (X : Context) → Index X → Context
  toChart : (X : Context) → (i : Index X) → X ⟶ chart X i

namespace RefinementAtlas

variable {Context : Type u} [Category.{v} Context]

/-- The atlas family over an opposite-site object as a covering presieve. -/
def presieveAt (A : RefinementAtlas Context) (X : Contextᵒᵖ) : Presieve X :=
  Presieve.ofArrows
    (fun i : A.Index (unop X) => op (A.chart (unop X) i))
    (fun i => (A.toChart (unop X) i).op)

/-- The raw KuuOS atlas as a Mathlib precoverage: at each object exactly the
declared refinement family is taken as a generating cover. -/
def precoverage (A : RefinementAtlas Context) : Precoverage (Contextᵒᵖ) where
  coverings X := {A.presieveAt X}

/-- The smallest Grothendieck topology forced by the declared KuuOS refinement
families. -/
def generatedTopology (A : RefinementAtlas Context) :
    GrothendieckTopology (Contextᵒᵖ) :=
  A.precoverage.toGrothendieck

/-- Every declared KuuOS cover generates a covering sieve in the freely generated
topology. -/
theorem generate_presieveAt_mem_generatedTopology
    (A : RefinementAtlas Context) (X : Contextᵒᵖ) :
    Sieve.generate (A.presieveAt X) ∈ A.generatedTopology X := by
  apply Precoverage.generate_mem_toGrothendieck
  simp [precoverage]

end RefinementAtlas

end Atlas

/-!
The exact boundary after v2.4 is now:

```text
KuuOS covariant refinement family
        ↓ opposite
covering presieve
        ↓ Precoverage.toGrothendieck
smallest Grothendieck topology containing the declared refinements.
```

For one declared cover whose chosen overlaps are pushouts, v2.1 effective descent
is exactly `Presieve.IsSheafFor` for that cover.  To upgrade this local statement
to an iff for the *whole generated topology*, one must additionally control all
pullbacks of declared covers (or equivalently provide a base-change-closed atlas),
as exposed by Mathlib's `Precoverage.isSheaf_toGrothendieck_iff`.  That is the
next universal theorem layer rather than an implicit assumption here.
-/

end KUOS.DependentOriginationGeneratedRefinementTopologyV2_4
