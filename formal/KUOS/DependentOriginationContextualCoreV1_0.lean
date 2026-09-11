import Mathlib
import KUOS.DependentOriginationFunctorialTransportV0_1
import KUOS.DependentOriginationFreeHistoryFunctorV0_6

namespace KUOS.DependentOriginationContextualCoreV1_0

open CategoryTheory
open KUOS.DependentOriginationFunctorialTransportV0_1
open KUOS.DependentOriginationHistorySensitiveTransportV0_5
open KUOS.DependentOriginationFreeHistoryFunctorV0_6

universe u v w w' z

/-!
# Contextual dependent-origination core v1.0

This file returns to the parent structure of dependent origination itself.

The primary object is still the v0.1 `FunctorialTransportSystem`: a state-valued
functor on a category of contexts.  The new layer does not add quantum,
Hamiltonian, semigroup, groupoid, or process-tensor assumptions.  Instead it
makes explicit the structural operations that belong at the parent level:

* maps between dependent-origination systems commute with contextual transport;
* reversible equivalence of presentations is stronger than ordinary transport;
* changing the contextual lens is pullback along a functor;
* groupoid contexts force reversible transport, while arbitrary categories do not;
* finite histories are recovered as a one-object free-category specialization.

Thus reversible gauge/descent, irreversible dynamics, finite history, memory,
and later quantum realizations remain specializations rather than definitions
of dependent origination itself.
-/

/-!
## Morphisms of dependent-origination systems
-/

/--
A map between two dependent-origination systems over the same context category.
It is fiberwise and commutes with every admissible contextual transport.

This is the elementwise form of a natural transformation between the two
state-valued functors.
-/
structure SystemHom
    {Context : Type u} [Category.{v} Context]
    (D E : FunctorialTransportSystem Context) where
  app : (X : Context) → D.state.obj X → E.state.obj X
  naturality :
    ∀ {X Y : Context} (f : X ⟶ Y) (x : D.state.obj X),
      app Y (D.transport f x) = E.transport f (app X x)

namespace SystemHom

variable {Context : Type u} [Category.{v} Context]
variable {D E F : FunctorialTransportSystem Context}

/-- Identity map of one contextual dependent-origination system. -/
def id (D : FunctorialTransportSystem Context) : SystemHom D D where
  app := fun _ x => x
  naturality := by
    intro X Y f x
    rfl

/-- Composition of transport-compatible system maps. -/
def comp (g : SystemHom E F) (f : SystemHom D E) : SystemHom D F where
  app := fun X x => g.app X (f.app X x)
  naturality := by
    intro X Y h x
    rw [f.naturality h x, g.naturality h (f.app X x)]

@[simp] theorem id_app
    (X : Context) (x : D.state.obj X) :
    (id D).app X x = x := by
  rfl

@[simp] theorem comp_app
    (g : SystemHom E F) (f : SystemHom D E)
    (X : Context) (x : D.state.obj X) :
    (g.comp f).app X x = g.app X (f.app X x) := by
  rfl

/-- Left identity holds pointwise. -/
theorem id_comp_app
    (f : SystemHom D E)
    (X : Context) (x : D.state.obj X) :
    ((id E).comp f).app X x = f.app X x := by
  rfl

/-- Right identity holds pointwise. -/
theorem comp_id_app
    (f : SystemHom D E)
    (X : Context) (x : D.state.obj X) :
    (f.comp (id D)).app X x = f.app X x := by
  rfl

/-- Composition is associative pointwise. -/
theorem comp_assoc_app
    {G : FunctorialTransportSystem Context}
    (h : SystemHom F G) (g : SystemHom E F) (f : SystemHom D E)
    (X : Context) (x : D.state.obj X) :
    ((h.comp g).comp f).app X x =
      (h.comp (g.comp f)).app X x := by
  rfl

end SystemHom

/-!
## Reversible equivalence of presentations
-/

/--
A reversible equivalence between two contextual presentations of dependent
origination.  The forward and backward maps both commute with transport and are
pointwise inverse.

This is additional structure: ordinary dependent-origination transport does not
require a reversible presentation change.
-/
structure SystemEquiv
    {Context : Type u} [Category.{v} Context]
    (D E : FunctorialTransportSystem Context) where
  toHom : SystemHom D E
  invHom : SystemHom E D
  left_inv : ∀ (X : Context) (x : D.state.obj X),
    invHom.app X (toHom.app X x) = x
  right_inv : ∀ (X : Context) (y : E.state.obj X),
    toHom.app X (invHom.app X y) = y

namespace SystemEquiv

variable {Context : Type u} [Category.{v} Context]
variable {D E : FunctorialTransportSystem Context}

/-- Pointwise equivalence of state fibers induced by a system equivalence. -/
def at (e : SystemEquiv D E) (X : Context) :
    D.state.obj X ≃ E.state.obj X where
  toFun := e.toHom.app X
  invFun := e.invHom.app X
  left_inv := e.left_inv X
  right_inv := e.right_inv X

/-- A reversible presentation equivalence preserves contextual transport. -/
theorem transport_commutes
    (e : SystemEquiv D E)
    {X Y : Context} (f : X ⟶ Y) (x : D.state.obj X) :
    e.at Y (D.transport f x) =
      E.transport f (e.at X x) := by
  exact e.toHom.naturality f x

end SystemEquiv

/-!
## Change of contextual lens by pullback
-/

/--
Reindex a dependent-origination system along a functor of context categories.
No reversibility or fullness assumption on the context functor is required.
-/
def reindex
    {Source : Type u} [Category.{v} Source]
    {Target : Type w} [Category.{z} Target]
    (F : Source ⥤ Target)
    (D : FunctorialTransportSystem Target) :
    FunctorialTransportSystem Source where
  state := F ⋙ D.state

@[simp] theorem reindex_transport
    {Source : Type u} [Category.{v} Source]
    {Target : Type w} [Category.{z} Target]
    (F : Source ⥤ Target)
    (D : FunctorialTransportSystem Target)
    {X Y : Source} (f : X ⟶ Y)
    (x : D.state.obj (F.obj X)) :
    (reindex F D).transport f x = D.transport (F.map f) x := by
  rfl

namespace SystemHom

/-- A transport-compatible system map pulls back along any context functor. -/
def reindex
    {Source : Type u} [Category.{v} Source]
    {Target : Type w} [Category.{z} Target]
    {D E : FunctorialTransportSystem Target}
    (F : Source ⥤ Target)
    (η : SystemHom D E) :
    SystemHom (DependentOriginationContextualCoreV1_0.reindex F D)
      (DependentOriginationContextualCoreV1_0.reindex F E) where
  app := fun X => η.app (F.obj X)
  naturality := by
    intro X Y f x
    exact η.naturality (F.map f) x

end SystemHom

/--
A contextual specialization is a choice of a finer context category mapping into
another context category.  Any parent dependent-origination system can then be
viewed through the finer lens by pullback.
-/
structure ContextSpecialization
    (Fine : Type u) [Category.{v} Fine]
    (Coarse : Type w) [Category.{z} Coarse] where
  contextMap : Fine ⥤ Coarse

namespace ContextSpecialization

/-- Pull a parent transport system back to the specialized context category. -/
def pullback
    {Fine : Type u} [Category.{v} Fine]
    {Coarse : Type w} [Category.{z} Coarse]
    (S : ContextSpecialization Fine Coarse)
    (D : FunctorialTransportSystem Coarse) :
    FunctorialTransportSystem Fine :=
  reindex S.contextMap D

/-- Context specializations compose functorially. -/
def comp
    {A : Type u} [Category.{v} A]
    {B : Type w} [Category.{z} B]
    {C : Type w'} [Category C]
    (S₁ : ContextSpecialization A B)
    (S₂ : ContextSpecialization B C) :
    ContextSpecialization A C where
  contextMap := S₁.contextMap ⋙ S₂.contextMap

end ContextSpecialization

/-!
## Reversible contexts are a specialization, not the parent definition
-/

namespace FunctorialTransportSystem

variable {Context : Type u} [Category.{v} Context]

/-- Transport is irreversible at one context morphism when its state map is not bijective. -/
def IsIrreversibleAt
    (D : FunctorialTransportSystem Context)
    {X Y : Context} (f : X ⟶ Y) : Prop :=
  ¬ Function.Bijective (D.transport f)

end FunctorialTransportSystem

section GroupoidContext

variable {Context : Type u} [Groupoid.{v} Context]

namespace FunctorialTransportSystem

/--
In a groupoid context, functorial transport along every morphism is an actual
state equivalence, with inverse supplied by the inverse context morphism.
-/
def transportEquiv
    (D : FunctorialTransportSystem Context)
    {X Y : Context} (f : X ⟶ Y) :
    D.state.obj X ≃ D.state.obj Y where
  toFun := D.transport f
  invFun := D.transport (inv f)
  left_inv := by
    intro x
    rw [← D.transport_comp_apply f (inv f) x]
    simpa using D.transport_id_apply X x
  right_inv := by
    intro y
    rw [← D.transport_comp_apply (inv f) f y]
    simpa using D.transport_id_apply Y y

/-- Therefore a groupoid contextual presentation cannot exhibit irreversible transport. -/
theorem not_irreversibleAt
    (D : FunctorialTransportSystem Context)
    {X Y : Context} (f : X ⟶ Y) :
    ¬ D.IsIrreversibleAt f := by
  intro h
  exact h (D.transportEquiv f).bijective

end FunctorialTransportSystem

end GroupoidContext

/-!
## Finite history as a specialization of the contextual parent
-/

namespace HistoryTransport

variable {Event : Type u} {State : Type w}

/--
The existing finite-history semantics is explicitly recovered as the one-object
free-category specialization of the contextual parent.
-/
def asContextualSystem
    (H : HistoryTransport Event State) :
    FunctorialTransportSystem (FreeHistoryCategory Event) :=
  H.toFunctorialTransportSystem

/-- Its contextual transport is exactly evaluation of the finite event word. -/
theorem asContextualSystem_transport
    (H : HistoryTransport Event State)
    (word : List Event) (x : State) :
    H.asContextualSystem.transport word x = H.eval word x := by
  rfl

end HistoryTransport

end KUOS.DependentOriginationContextualCoreV1_0
