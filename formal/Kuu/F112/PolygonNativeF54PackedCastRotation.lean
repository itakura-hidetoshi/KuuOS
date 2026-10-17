import Kuu.F112.PolygonNativeF54GeneralRootReduction

/-!
# F112-E7Q5-F4-I — proof-relevant dependent F54 intermediate packets

The unresolved general root F54 associator naturality is not a
numerical pentagon/sector/phase issue. The F54 source contains a
TWO-Nat index cast of a proof-relevant F45 tree, immediately followed
by an ACTUAL oriented F54 local rotation whose input type depends on
that specific casted intermediate tree.

To avoid rewriting one component while losing the other, retain
the exact pair as a Sigma dependent packet:
  (intermediate F45 tree, F54 route to it, oriented chain from it).
The package is Type-valued, keeps both independent original
categorical Blocks and every actual F41 primitive history, and is
never identified merely by its shadow or length.

This file proves a strict two-category functor action on these
dependent packets, compatibility with pasting of the actual route
pieces, and explicitly tests normalization of a double Nat cast
together with its following oriented rotation witness.

The general naturality of the ROOT '.assoc' constructor of the
existing E7O F54 grammar is a separate, still open proposition.
No frozen KUOS/Gray/F51/F77 imports or new coherence axioms.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
noncomputable section

universe uA vA uB vB uC vC uD vD
variable {A : Type uA} [Category.{vA} A]
variable {B : Type uB} [Category.{vB} B]
variable {C : Type uC} [Category.{vC} C]
variable {D : Type uD} [Category.{vD} D]

/-- ACTUAL proof-relevant higher source packet: not a Prop statement
of existence. The middle F45 tree is carried in Type, together with
the two typed F54 witnesses incident to its exact dependent index. -/
abbrev KuuNativeF54CastRotationPacket
    {p : Polygon} {a b : A} {x y : B}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (source : KuuNativeF45Tree p n m ma pa mb pb)
    (target : KuuNativeF45Tree p n' m' ma pa mb pb) :=
  Σ middle : KuuNativeF45Tree p n' m' ma pa mb pb,
    (KuuNativeF45Tree.DepthRotationRoute p source middle) ×
    (KuuNativeF45Tree.RotationChain p middle target)

/-- Exact transport of all THREE components, not just of the
physical F45 sector list or the number of primitive rotations. -/
def KuuNativeF54CastRotationPacket.mapAxes
    (F : A ⥤ C) (G : B ⥤ D)
    {p : Polygon} {a b : A} {x y : B}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {source : KuuNativeF45Tree p n m ma pa mb pb}
    {target : KuuNativeF45Tree p n' m' ma pa mb pb}
    (packet : KuuNativeF54CastRotationPacket source target) :
    KuuNativeF54CastRotationPacket (source.mapAxes F G) (target.mapAxes F G) :=
  ⟨packet.1.mapAxes F G, packet.2.1.mapAxes F G,
    packet.2.2.mapAxes F G⟩

/-- Form an original-shaped typed F54 intermediate by BOTH Nat
casts and then one genuine oriented local rotation to the target. -/
def KuuNativeF54CastRotationPacket.ofCastAndRotation
    {p : Polygon} {a b : A} {x y : B}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (hn : n = n') (hm : m = m')
    (source : KuuNativeF45Tree p n m ma pa mb pb)
    (target : KuuNativeF45Tree p n' m' ma pa mb pb)
    (step : KuuNativeF45Tree.LocalRotation p
      (KuuNativeF45Tree.castDepths hn hm source) target) :
    KuuNativeF54CastRotationPacket source target :=
  ⟨KuuNativeF45Tree.castDepths hn hm source,
    ⟨.castDepths hn hm source,
      .snoc (.refl _) (.forward step)⟩⟩

/-- The exact F54 path defined by the type-packed cast and
rotation is the original nested 'trans' of those ACTUAL witnesses. -/
def KuuNativeF54CastRotationPacket.toRoute
    {p : Polygon} {a b : A} {x y : B}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {source : KuuNativeF45Tree p n m ma pa mb pb}
    {target : KuuNativeF45Tree p n' m' ma pa mb pb}
    (packet : KuuNativeF54CastRotationPacket source target) :
    KuuNativeF45Tree.DepthRotationRoute p source target :=
  .trans packet.2.1 (.chain packet.2.2)

/-- The packet's genuine typed route strictly commutes with
arbitrary independent categorical axis-functor transport. -/
theorem KuuNativeF54CastRotationPacket.toRoute_mapAxes
    (F : A ⥤ C) (G : B ⥤ D)
    {p : Polygon} {a b : A} {x y : B}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {source : KuuNativeF45Tree p n m ma pa mb pb}
    {target : KuuNativeF45Tree p n' m' ma pa mb pb}
    (packet : KuuNativeF54CastRotationPacket source target) :
    (packet.toRoute.mapAxes F G) = (packet.mapAxes F G).toRoute :=
  rfl

/-- The original double-Nat source cast plus its FOLLOWING rotation
transports as a WHOLE Sigma packet, for arbitrary equality proofs.
This avoids replacing only the intermediate F45 tree and leaving the
source of the next genuine Type-valued rotation out of sync. -/
theorem KuuNativeF54CastRotationPacket.mapAxes_ofCastAndRotation
    (F : A ⥤ C) (G : B ⥤ D)
    {p : Polygon} {a b : A} {x y : B}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (hn : n = n') (hm : m = m')
    (source : KuuNativeF45Tree p n m ma pa mb pb)
    (target : KuuNativeF45Tree p n' m' ma pa mb pb)
    (step : KuuNativeF45Tree.LocalRotation p
      (KuuNativeF45Tree.castDepths hn hm source) target) :
    (KuuNativeF54CastRotationPacket.ofCastAndRotation hn hm source target step).mapAxes F G =
      KuuNativeF54CastRotationPacket.ofCastAndRotation
        hn hm (source.mapAxes F G) (target.mapAxes F G)
        (by
          have ht := KuuNativeF45Tree.mapAxes_castDepths F G hn hm source
          rw [← ht]
          exact step.mapAxes F G) := by
  cases hn
  cases hm
  rfl

#print axioms KuuNativeF54CastRotationPacket
#print axioms KuuNativeF54CastRotationPacket.mapAxes
#print axioms KuuNativeF54CastRotationPacket.ofCastAndRotation
#print axioms KuuNativeF54CastRotationPacket.toRoute
#print axioms KuuNativeF54CastRotationPacket.toRoute_mapAxes
#print axioms KuuNativeF54CastRotationPacket.mapAxes_ofCastAndRotation
end
end Kuu.F112.Physical
