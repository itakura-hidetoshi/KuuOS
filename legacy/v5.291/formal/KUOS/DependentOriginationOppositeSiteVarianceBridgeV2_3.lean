import Mathlib
import KUOS.DependentOriginationContextualCoreV1_0
import KUOS.DependentOriginationSheafDescentUniversalityV2_2

namespace KUOS.DependentOriginationOppositeSiteVarianceBridgeV2_3

open CategoryTheory
open Opposite
open KUOS.DependentOriginationFunctorialTransportV0_1

universe u v w

/-!
# Dependent-origination opposite-site variance bridge v2.3

KuuOS contextual transport is covariant in refinement:

```text
root context -> finer context.
```

Ordinary sheaf theory is phrased using presheaves, hence contravariantly on a
site.  The variance is reconciled without changing the transport semantics by
using the opposite context category as the site.

If

```text
D.state : Context ⥤ Type
```

is a KuuOS contextual transport system, then a presheaf on the site
`Contextᵒᵖ` is a functor

```text
(Contextᵒᵖ)ᵒᵖ ⥤ Type.
```

Precomposition with Mathlib's `unopUnop Context` gives exactly such a presheaf.
Conversely, precomposition with `opOp Context` recovers a contextual transport
system.  Both round trips are naturally isomorphic to the starting functor.

For a context morphism `f : X ⟶ Y`, the corresponding presheaf restriction map
along the opposite-site arrow `f.op` is represented by `f.op.op`; after the
double-opposite identification this map is definitionally the original KuuOS
transport along `f`.

This closes the variance obstruction between the v2.1 contextual-descent
comparison and the v2.2 Mathlib sheafification universal property.  It does not
yet prove that a declared family of KuuOS refinement covers generates a topology
whose sheaf condition is equivalent to the v2.1 effective comparison condition.
-/

/-- The ordinary sheaf-theoretic site associated with a covariant KuuOS context
category. -/
abbrev OppositeRefinementSite (Context : Type u) := Contextᵒᵖ

/-- Reinterpret a covariant contextual transport system as a presheaf on the
opposite refinement site. -/
def asOppositeSitePresheaf
    {Context : Type u} [Category.{v} Context]
    (D : FunctorialTransportSystem Context) :
    (OppositeRefinementSite Context)ᵒᵖ ⥤ Type _ :=
  unopUnop Context ⋙ D.state

/-- Reinterpret a presheaf on the opposite refinement site as a covariant KuuOS
contextual transport system. -/
def ofOppositeSitePresheaf
    {Context : Type u} [Category.{v} Context]
    (P : (OppositeRefinementSite Context)ᵒᵖ ⥤ Type w) :
    FunctorialTransportSystem Context where
  state := opOp Context ⋙ P

/-- Object fibers are unchanged by the opposite-site reinterpretation. -/
@[simp] theorem asOppositeSitePresheaf_obj
    {Context : Type u} [Category.{v} Context]
    (D : FunctorialTransportSystem Context)
    (X : Context) :
    (asOppositeSitePresheaf D).obj (op (op X)) = D.state.obj X := by
  rfl

/-- A context morphism and its double-opposite presheaf arrow induce exactly the
same state map. -/
@[simp] theorem asOppositeSitePresheaf_map
    {Context : Type u} [Category.{v} Context]
    (D : FunctorialTransportSystem Context)
    {X Y : Context} (f : X ⟶ Y) :
    (asOppositeSitePresheaf D).map f.op.op = D.state.map f := by
  rfl

/-- Elementwise, presheaf restriction on the opposite site is exactly KuuOS
contextual transport. -/
@[simp] theorem asOppositeSitePresheaf_map_apply
    {Context : Type u} [Category.{v} Context]
    (D : FunctorialTransportSystem Context)
    {X Y : Context} (f : X ⟶ Y)
    (x : D.state.obj X) :
    (asOppositeSitePresheaf D).map f.op.op x = D.transport f x := by
  rfl

/-- Conversely, the contextual fiber recovered from a presheaf is its value at
the corresponding double-opposite object. -/
@[simp] theorem ofOppositeSitePresheaf_obj
    {Context : Type u} [Category.{v} Context]
    (P : (OppositeRefinementSite Context)ᵒᵖ ⥤ Type w)
    (X : Context) :
    (ofOppositeSitePresheaf P).state.obj X = P.obj (op (op X)) := by
  rfl

/-- Conversely, contextual transport recovered from a presheaf is its map on
the corresponding double-opposite arrow. -/
@[simp] theorem ofOppositeSitePresheaf_map
    {Context : Type u} [Category.{v} Context]
    (P : (OppositeRefinementSite Context)ᵒᵖ ⥤ Type w)
    {X Y : Context} (f : X ⟶ Y) :
    (ofOppositeSitePresheaf P).state.map f = P.map f.op.op := by
  rfl

/-- Going from a contextual transport system to an opposite-site presheaf and
back changes no intrinsic transport data, up to the canonical natural
isomorphism. -/
def contextualRoundTripIso
    {Context : Type u} [Category.{v} Context]
    (D : FunctorialTransportSystem Context) :
    (ofOppositeSitePresheaf (asOppositeSitePresheaf D)).state ≅ D.state :=
  NatIso.ofComponents
    (fun _ => Iso.refl _)
    (by
      intro X Y f
      rfl)

/-- Going from an opposite-site presheaf to a contextual system and back is
canonically naturally isomorphic to the original presheaf. -/
def presheafRoundTripIso
    {Context : Type u} [Category.{v} Context]
    (P : (OppositeRefinementSite Context)ᵒᵖ ⥤ Type w) :
    asOppositeSitePresheaf (ofOppositeSitePresheaf P) ≅ P :=
  NatIso.ofComponents
    (fun _ => Iso.refl _)
    (by
      intro X Y f
      rfl)

/-- Once a Grothendieck topology is chosen on the opposite refinement site, the
variance-correct sheaf/descent predicate for a KuuOS contextual transport
system is simply the ordinary Mathlib sheaf predicate of its associated
presheaf. -/
def IsGrothendieckDescentComplete
    {Context : Type u} [Category.{v} Context]
    (J : GrothendieckTopology (OppositeRefinementSite Context))
    (D : FunctorialTransportSystem Context) : Prop :=
  Presheaf.IsSheaf J (asOppositeSitePresheaf D)

/-!
The bridge established here is exact:

```text
FunctorialTransportSystem Context
        |  asOppositeSitePresheaf
        v
presheaf on Contextᵒᵖ
```

with the original transport along `f` identified with presheaf restriction on
`f.op` after the canonical double-opposite representation.

The next theorem should connect a uniform family of KuuOS `RefinementCover`s to
a generated Grothendieck topology on `Contextᵒᵖ`, then prove that the v2.1
comparison-map equivalence is the corresponding Mathlib sheaf condition.
-/

end KUOS.DependentOriginationOppositeSiteVarianceBridgeV2_3
