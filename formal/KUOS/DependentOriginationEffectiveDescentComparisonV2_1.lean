import Mathlib
import KUOS.DependentOriginationContextualDescentV1_1

namespace KUOS.DependentOriginationEffectiveDescentComparisonV2_1

open CategoryTheory
open KUOS.DependentOriginationFunctorialTransportV0_1
open KUOS.DependentOriginationContextualDescentV1_1

universe u v w

/-!
# Dependent-origination effective descent comparison v2.1

The contextual-descent layer v1.1 deliberately separates two questions:

1. existence of a root state inducing every overlap-compatible local family;
2. separation of root states by their restrictions to all local charts.

This file packages both conditions into one canonical comparison map.  For a
refinement cover `C` with overlap system `O`, define the type of compatible
local states and the map

```text
D.state.obj C.rootContext
  ->
CompatibleLocalStates D C O.
```

The existing v1.1 notions are exactly surjectivity and injectivity of this map.
Consequently effective state descent (existence plus uniqueness) is exactly
bijectivity, and therefore yields a genuine equivalence between root states and
overlap-compatible local families.

This is the first step from the elementary pairwise formulation toward a
Cech/limit formulation of the future descent datum `J`.  No Grothendieck
topology, stackification, or universal dependent-origination completion is
assumed here.
-/

variable {Context : Type u} [Category.{v} Context]
variable {Index : Type w}

/-- A dependent family of local states satisfying the v1.1 pairwise overlap
compatibility equations. -/
def CompatibleLocalStates
    (D : FunctorialTransportSystem Context)
    (C : RefinementCover Context Index)
    (O : OverlapSystem C) : Type _ :=
  { s : (i : Index) -> D.state.obj (C.chart i) //
      forall i j,
        D.transport (O.leftToMeet i j) (s i) =
          D.transport (O.rightToMeet i j) (s j) }

namespace CompatibleLocalStates

variable {D : FunctorialTransportSystem Context}
variable {C : RefinementCover Context Index}
variable {O : OverlapSystem C}

/-- Forget the compatibility proof and recover the existing v1.1 local-state
family. -/
def toLocalStateFamily
    (s : CompatibleLocalStates D C O) :
    LocalStateFamily D C where
  state := s.1

/-- The forgotten family is overlap-compatible by construction. -/
theorem overlapCompatible
    (s : CompatibleLocalStates D C O) :
    OverlapCompatible D C O s.toLocalStateFamily := by
  intro i j
  exact s.2 i j

end CompatibleLocalStates

/-- Restrict one root state to every local chart, remembering the automatically
induced pairwise compatibility. -/
def globalToCompatible
    (D : FunctorialTransportSystem Context)
    (C : RefinementCover Context Index)
    (O : OverlapSystem C) :
    D.state.obj C.rootContext -> CompatibleLocalStates D C O :=
  fun x =>
    ⟨fun i => D.transport (C.toChart i) x,
      fun i j => root_transport_to_overlap_coherent D C O x i j⟩

/-- The v1.1 state-descent condition is exactly surjectivity of the canonical
root-to-compatible-family map. -/
theorem globalToCompatible_surjective_iff_hasStateDescent
    (D : FunctorialTransportSystem Context)
    (C : RefinementCover Context Index)
    (O : OverlapSystem C) :
    Function.Surjective (globalToCompatible D C O) ↔
      HasStateDescent D C O := by
  constructor
  · intro hsurj s hs
    let t : CompatibleLocalStates D C O := ⟨s.state, hs⟩
    rcases hsurj t with ⟨x, hx⟩
    refine ⟨x, ?_⟩
    intro i
    have hval :
        (globalToCompatible D C O x : CompatibleLocalStates D C O).1 = t.1 :=
      congrArg Subtype.val hx
    exact congrFun hval i
  · intro hdescent t
    let s : LocalStateFamily D C :=
      { state := t.1 }
    have hs : OverlapCompatible D C O s := by
      intro i j
      exact t.2 i j
    rcases hdescent s hs with ⟨x, hx⟩
    refine ⟨x, ?_⟩
    apply Subtype.ext
    funext i
    exact hx i

/-- The v1.1 separation condition is exactly injectivity of the same canonical
comparison map. -/
theorem globalToCompatible_injective_iff_coverSeparates
    (D : FunctorialTransportSystem Context)
    (C : RefinementCover Context Index)
    (O : OverlapSystem C) :
    Function.Injective (globalToCompatible D C O) ↔
      CoverSeparatesGlobalStates D C := by
  constructor
  · intro hinj x y hlocal
    apply hinj
    apply Subtype.ext
    funext i
    exact hlocal i
  · intro hseparate x y hxy
    apply hseparate x y
    intro i
    have hval :
        (globalToCompatible D C O x : CompatibleLocalStates D C O).1 =
          (globalToCompatible D C O y : CompatibleLocalStates D C O).1 :=
      congrArg Subtype.val hxy
    exact congrFun hval i

/-- Effective state descent means both existence of a global state for every
compatible local family and separation/uniqueness of global states. -/
def HasEffectiveStateDescent
    (D : FunctorialTransportSystem Context)
    (C : RefinementCover Context Index)
    (O : OverlapSystem C) : Prop :=
  HasStateDescent D C O ∧ CoverSeparatesGlobalStates D C

/-- Effective state descent is exactly bijectivity of the canonical Cech-style
comparison map. -/
theorem globalToCompatible_bijective_iff_effectiveStateDescent
    (D : FunctorialTransportSystem Context)
    (C : RefinementCover Context Index)
    (O : OverlapSystem C) :
    Function.Bijective (globalToCompatible D C O) ↔
      HasEffectiveStateDescent D C O := by
  constructor
  · rintro ⟨hinj, hsurj⟩
    exact
      ⟨(globalToCompatible_surjective_iff_hasStateDescent D C O).1 hsurj,
        (globalToCompatible_injective_iff_coverSeparates D C O).1 hinj⟩
  · rintro ⟨hdescent, hseparate⟩
    exact
      ⟨(globalToCompatible_injective_iff_coverSeparates D C O).2 hseparate,
        (globalToCompatible_surjective_iff_hasStateDescent D C O).2 hdescent⟩

/-- Under effective descent, the root-state fiber is genuinely equivalent to
the type of overlap-compatible local families. -/
noncomputable def effectiveStateDescentEquiv
    (D : FunctorialTransportSystem Context)
    (C : RefinementCover Context Index)
    (O : OverlapSystem C)
    (h : HasEffectiveStateDescent D C O) :
    D.state.obj C.rootContext ≃ CompatibleLocalStates D C O :=
  Equiv.ofBijective (globalToCompatible D C O)
    ((globalToCompatible_bijective_iff_effectiveStateDescent D C O).2 h)

@[simp] theorem effectiveStateDescentEquiv_apply
    (D : FunctorialTransportSystem Context)
    (C : RefinementCover Context Index)
    (O : OverlapSystem C)
    (h : HasEffectiveStateDescent D C O)
    (x : D.state.obj C.rootContext) :
    effectiveStateDescentEquiv D C O h x = globalToCompatible D C O x := by
  rfl

/-!
The future `J`-axis can now be stated without ambiguity: a chosen family of
refinement covers is an effective descent family for `D` precisely when all of
its canonical comparison maps are equivalences.  The next construction should
package such covers uniformly and identify the categorical completion that
freely enforces these comparison equivalences, rather than assuming in advance
that ordinary localization or stackification is the correct carrier.
-/

end KUOS.DependentOriginationEffectiveDescentComparisonV2_1
