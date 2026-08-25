import Mathlib.CategoryTheory.Bicategory.Coherence
import Mathlib.CategoryTheory.Bicategory.LocallyDiscrete
import KUOS.DependentOriginationTwoCellCoherenceV1_5

namespace KUOS.DependentOriginationBicategoricalCoherenceV1_6

open CategoryTheory
open KUOS.DependentOriginationFunctorialTransportV0_1

universe u v w x y

/-!
# Native bicategorical dependent-origination coherence v1.6

The v1.5 layer retained explicit two-cell data over an ordinary category, but it
deliberately stopped short of a full bicategory.  This layer moves the parent
higher-categorical carrier to Mathlib's native `CategoryTheory.Bicategory`.

Consequently the source now has, as part of its actual typeclass structure:

* categories of 1-morphisms and 2-morphisms;
* left and right whiskering;
* associator 2-isomorphisms;
* left and right unitor 2-isomorphisms;
* whiskering exchange;
* the pentagon equation;
* the triangle equation.

The current state semantics remains set-truncated: a represented 2-morphism is
sent to equality of state transport maps.  This preserves the distinction
between source-level higher path structure and the present `Type`-valued
readout layer.
-/

/--
A dependent-origination transport realization on a genuine bicategory.

`respects₂` is the current set-truncated target condition.  It does not erase
2-morphisms from the source bicategory; it says only that the present state
carrier does not distinguish their induced transport maps.
-/
structure BicategoricalTransportSystem
    (B : Type u) [Bicategory.{w, v} B] where
  state : B -> Type x
  transport : {X Y : B} -> (X ⟶ Y) -> state X -> state Y
  transport_id : forall (X : B) (s : state X),
    transport (𝟙 X) s = s
  transport_comp : forall {X Y Z : B}
    (f : X ⟶ Y) (g : Y ⟶ Z) (s : state X),
    transport (f ≫ g) s = transport g (transport f s)
  respects₂ : forall {X Y : B} {f g : X ⟶ Y},
    (f ⟶ g) -> transport f = transport g

namespace BicategoricalTransportSystem

/-- A source 2-morphism acts trivially after the current set truncation. -/
theorem transport_eq_of_twoCell
    {B : Type u} [Bicategory.{w, v} B]
    (D : BicategoricalTransportSystem B)
    {X Y : B} {f g : X ⟶ Y}
    (η : f ⟶ g) (s : D.state X) :
    D.transport f s = D.transport g s := by
  exact congrFun (D.respects₂ η) s

/-- The native bicategory associator is respected by state transport. -/
theorem transport_associator
    {B : Type u} [Bicategory.{w, v} B]
    (D : BicategoricalTransportSystem B)
    {a b c d : B}
    (f : a ⟶ b) (g : b ⟶ c) (h : c ⟶ d)
    (s : D.state a) :
    D.transport ((f ≫ g) ≫ h) s =
      D.transport (f ≫ (g ≫ h)) s := by
  exact transport_eq_of_twoCell D (Bicategory.associator f g h).hom s

/-- The native left unitor is respected by state transport. -/
theorem transport_leftUnitor
    {B : Type u} [Bicategory.{w, v} B]
    (D : BicategoricalTransportSystem B)
    {a b : B} (f : a ⟶ b) (s : D.state a) :
    D.transport (𝟙 a ≫ f) s = D.transport f s := by
  exact transport_eq_of_twoCell D (Bicategory.leftUnitor f).hom s

/-- The native right unitor is respected by state transport. -/
theorem transport_rightUnitor
    {B : Type u} [Bicategory.{w, v} B]
    (D : BicategoricalTransportSystem B)
    {a b : B} (f : a ⟶ b) (s : D.state a) :
    D.transport (f ≫ 𝟙 b) s = D.transport f s := by
  exact transport_eq_of_twoCell D (Bicategory.rightUnitor f).hom s

/-- Horizontal composition of 2-morphisms via whiskering and vertical composition. -/
def horizontalComp
    {B : Type u} [Bicategory.{w, v} B]
    {a b c : B}
    {f g : a ⟶ b} {h i : b ⟶ c}
    (η : f ⟶ g) (θ : h ⟶ i) :
    f ≫ h ⟶ g ≫ i :=
  Bicategory.whiskerLeft f θ ≫ Bicategory.whiskerRight η i

/-- The two whiskering orders for horizontal composition agree. -/
theorem horizontalComp_exchange
    {B : Type u} [Bicategory.{w, v} B]
    {a b c : B}
    {f g : a ⟶ b} {h i : b ⟶ c}
    (η : f ⟶ g) (θ : h ⟶ i) :
    horizontalComp η θ =
      Bicategory.whiskerRight η h ≫ Bicategory.whiskerLeft g θ := by
  exact Bicategory.whisker_exchange η θ

/-- Re-export the native bicategory pentagon equation at the KuuOS boundary. -/
theorem source_pentagon
    {B : Type u} [Bicategory.{w, v} B]
    {a b c d e : B}
    (f : a ⟶ b) (g : b ⟶ c) (h : c ⟶ d) (i : d ⟶ e) :
    Bicategory.whiskerRight (Bicategory.associator f g h).hom i ≫
          (Bicategory.associator f (g ≫ h) i).hom ≫
            Bicategory.whiskerLeft f (Bicategory.associator g h i).hom =
      (Bicategory.associator (f ≫ g) h i).hom ≫
        (Bicategory.associator f g (h ≫ i)).hom := by
  exact Bicategory.pentagon f g h i

/-- Re-export the native bicategory triangle equation at the KuuOS boundary. -/
theorem source_triangle
    {B : Type u} [Bicategory.{w, v} B]
    {a b c : B}
    (f : a ⟶ b) (g : b ⟶ c) :
    (Bicategory.associator f (𝟙 b) g).hom ≫
        Bicategory.whiskerLeft f (Bicategory.leftUnitor g).hom =
      Bicategory.whiskerRight (Bicategory.rightUnitor f).hom g := by
  exact Bicategory.triangle f g

/-- Invariant semantics for a bicategorical transport realization. -/
structure InvariantReadout
    {B : Type u} [Bicategory.{w, v} B]
    (D : BicategoricalTransportSystem B)
    (Semantic : Type y) where
  readout : (X : B) -> D.state X -> Semantic
  transport_invariant : forall {X Y : B}
    (f : X ⟶ Y) (s : D.state X),
    readout Y (D.transport f s) = readout X s

namespace InvariantReadout

/-- Related 1-morphism paths have the same represented readout. -/
theorem readout_eq_of_twoCell
    {B : Type u} [Bicategory.{w, v} B]
    {D : BicategoricalTransportSystem B}
    {Semantic : Type y}
    (Q : InvariantReadout D Semantic)
    {X Y : B} {f g : X ⟶ Y}
    (η : f ⟶ g) (s : D.state X) :
    Q.readout Y (D.transport f s) =
      Q.readout Y (D.transport g s) := by
  rw [D.transport_eq_of_twoCell η s]

/-- Reassociation changes no invariant semantic value. -/
theorem readout_associator
    {B : Type u} [Bicategory.{w, v} B]
    {D : BicategoricalTransportSystem B}
    {Semantic : Type y}
    (Q : InvariantReadout D Semantic)
    {a b c d : B}
    (f : a ⟶ b) (g : b ⟶ c) (h : c ⟶ d)
    (s : D.state a) :
    Q.readout d (D.transport ((f ≫ g) ≫ h) s) =
      Q.readout d (D.transport (f ≫ (g ≫ h)) s) := by
  rw [D.transport_associator f g h s]

end InvariantReadout

end BicategoricalTransportSystem

/-!
## Strict one-categorical core as a locally discrete specialization
-/

/--
Every existing one-categorical dependent-origination system embeds into the
native bicategorical layer through Mathlib's locally discrete bicategory.
Only equality 2-morphisms occur in this specialization.
-/
def FunctorialTransportSystem.toLocallyDiscreteBicategorical
    {C : Type u} [Category.{v} C]
    (D : FunctorialTransportSystem C) :
    BicategoricalTransportSystem (LocallyDiscrete C) where
  state := fun X => D.state.obj X.as
  transport := fun f => D.transport f.as
  transport_id := by
    intro X s
    exact D.transport_id_apply X.as s
  transport_comp := by
    intro X Y Z f g s
    exact D.transport_comp_apply f.as g.as s
  respects₂ := by
    intro X Y f g η
    have hfg : f = g := LocallyDiscrete.eq_of_hom η
    subst g
    rfl

/-- The locally discrete bridge preserves one-step state transport definitionally. -/
@[simp] theorem toLocallyDiscreteBicategorical_transport
    {C : Type u} [Category.{v} C]
    (D : FunctorialTransportSystem C)
    {X Y : C} (f : X ⟶ Y) (s : D.state.obj X) :
    (D.toLocallyDiscreteBicategorical).transport f.toLoc s =
      D.transport f s := by
  rfl

/-!
The hierarchy is therefore additive:

```text
ordinary category transport
  -> locally discrete strict bicategory
  -> v1.5 explicit two-cell carrier
  -> native bicategory with associators, unitors, exchange, pentagon, triangle
```

The v1.5 carrier remains useful as an intermediate interface.  v1.6 does not
identify every v1.5 carrier with a bicategory; the missing coherence data must
actually be supplied before the stronger word is used.
-/

end KUOS.DependentOriginationBicategoricalCoherenceV1_6
