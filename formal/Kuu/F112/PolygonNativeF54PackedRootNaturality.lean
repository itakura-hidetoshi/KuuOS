import Kuu.F112.PolygonNativeF54PackedCastRotation

/-!
# F112-E7Q5-F4-I2 — exact type-correct transport of a root F54 packet

At genuinely arbitrary Nat depths, the F45 double-Nat cast alters
the type of the REAL, proof-relevant F54 root rotation witness.
The previously attempted equations saying that its transported
witness equals the new canonical LocalRotation.assoc are NOT yet
proven: Eq.rec term conversion remains a proof-engineering obstacle.

Here do NOT assert that missing equality. Instead explicitly
construct the transported root rotation with its CORRECT new
dependent start tree using the already certified F45 cast equation.
Show that the full original dependent Sigma packet, including its
intermediate tree, preceding cast route and oriented outgoing
rotation chain, is exactly transported to that new well-typed
source packet at ALL six independent symbolic Nat depths.

Projecting this equality back to a genuine F54 raw route gives an
unconditional factorization of the mapped original associator
through the correctly typed packed intermediate proof. Neither
the canonical associated path nor the two raw pentagon paths are
identified by numerical shadow or a supposed Gray law.

No frozen KUOS/Gray/F51/F77 imports or axioms.
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

/-- Fully type-correct arbitrary-Nat transfer of the actual
original root F54 associativity generator. The dependent input
tree is transported TOGETHER with the witness, not detached from
the following genuine proof-relevant F54 rotation. -/
def nativePackedRootMappedRotation
    (F : A ⥤ C) (G : B ⥤ D)
    {p : Polygon} {a b : A} {x y : B}
    {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
    {p₀ p₁ p₂ p₃ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ q₃ : KuuNativeBlocks x y}
    (t₁ : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁)
    (t₂ : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂)
    (t₃ : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃) :
    KuuNativeF45Tree.LocalRotation p
      (KuuNativeF45Tree.castDepths
        (Nat.add_assoc n₁ n₂ n₃) (Nat.add_assoc m₁ m₂ m₃)
        (KuuNativeF45Tree.node
          (KuuNativeF45Tree.node (t₁.mapAxes F G) (t₂.mapAxes F G))
          (t₃.mapAxes F G)))
      (KuuNativeF45Tree.node
        (t₁.mapAxes F G) (KuuNativeF45Tree.node
          (t₂.mapAxes F G) (t₃.mapAxes F G))) := by
  have ht := KuuNativeF45Tree.mapAxes_castDepths F G
    (Nat.add_assoc n₁ n₂ n₃) (Nat.add_assoc m₁ m₂ m₃)
    (KuuNativeF45Tree.node (KuuNativeF45Tree.node t₁ t₂) t₃)
  rw [← ht]
  exact (KuuNativeF45Tree.LocalRotation.assoc t₁ t₂ t₃).mapAxes F G

/-- The COMPLETE original Type-valued Sigma intermediate packet
commutes with BOTH arbitrary categorical functors for all six
independently symbolic Nat depths. This does not silently replace
the transported raw rotation by the different canonical constructor. -/
theorem nativeRootCastPacket_mapAxes_exact
    (F : A ⥤ C) (G : B ⥤ D)
    {p : Polygon} {a b : A} {x y : B}
    {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
    {p₀ p₁ p₂ p₃ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ q₃ : KuuNativeBlocks x y}
    (t₁ : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁)
    (t₂ : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂)
    (t₃ : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃) :
    (KuuNativeF54CastRotationPacket.ofCastAndRotation
      (Nat.add_assoc n₁ n₂ n₃) (Nat.add_assoc m₁ m₂ m₃)
      (KuuNativeF45Tree.node (KuuNativeF45Tree.node t₁ t₂) t₃)
      (KuuNativeF45Tree.node t₁ (KuuNativeF45Tree.node t₂ t₃))
      (KuuNativeF45Tree.LocalRotation.assoc t₁ t₂ t₃)).mapAxes F G =
    KuuNativeF54CastRotationPacket.ofCastAndRotation
      (Nat.add_assoc n₁ n₂ n₃) (Nat.add_assoc m₁ m₂ m₃)
      (KuuNativeF45Tree.node
        (KuuNativeF45Tree.node (t₁.mapAxes F G) (t₂.mapAxes F G))
        (t₃.mapAxes F G))
      (KuuNativeF45Tree.node (t₁.mapAxes F G)
        (KuuNativeF45Tree.node (t₂.mapAxes F G) (t₃.mapAxes F G)))
      (nativePackedRootMappedRotation F G t₁ t₂ t₃) := by
  simpa only [KuuNativeF45Tree.mapAxes,
    nativePackedRootMappedRotation] using
    (KuuNativeF54CastRotationPacket.mapAxes_ofCastAndRotation
      F G
      (Nat.add_assoc n₁ n₂ n₃) (Nat.add_assoc m₁ m₂ m₃)
      (KuuNativeF45Tree.node (KuuNativeF45Tree.node t₁ t₂) t₃)
      (KuuNativeF45Tree.node t₁ (KuuNativeF45Tree.node t₂ t₃))
      (KuuNativeF45Tree.LocalRotation.assoc t₁ t₂ t₃))

/-- Unconditional factorization of the ORIGINAL F54 root assoc
raw route through the actually transported dependent Sigma packet,
with the explicit correctly typed mapped rotation witness. -/
theorem nativeGeneralRootAssoc_mapAxes_packed
    (F : A ⥤ C) (G : B ⥤ D)
    {p : Polygon} {a b : A} {x y : B}
    {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
    {p₀ p₁ p₂ p₃ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ q₃ : KuuNativeBlocks x y}
    (t₁ : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁)
    (t₂ : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂)
    (t₃ : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃) :
    (KuuNativeF45Tree.DepthRotationRoute.assoc t₁ t₂ t₃).mapAxes F G =
      (KuuNativeF54CastRotationPacket.ofCastAndRotation
        (Nat.add_assoc n₁ n₂ n₃) (Nat.add_assoc m₁ m₂ m₃)
        (KuuNativeF45Tree.node
          (KuuNativeF45Tree.node (t₁.mapAxes F G) (t₂.mapAxes F G))
          (t₃.mapAxes F G))
        (KuuNativeF45Tree.node (t₁.mapAxes F G)
          (KuuNativeF45Tree.node (t₂.mapAxes F G) (t₃.mapAxes F G)))
        (nativePackedRootMappedRotation F G t₁ t₂ t₃)).toRoute := by
  calc
    _ = (KuuNativeF54CastRotationPacket.ofCastAndRotation
        (Nat.add_assoc n₁ n₂ n₃) (Nat.add_assoc m₁ m₂ m₃)
        (KuuNativeF45Tree.node (KuuNativeF45Tree.node t₁ t₂) t₃)
        (KuuNativeF45Tree.node t₁ (KuuNativeF45Tree.node t₂ t₃))
        (KuuNativeF45Tree.LocalRotation.assoc t₁ t₂ t₃)).toRoute.mapAxes F G := rfl
    _ = ((KuuNativeF54CastRotationPacket.ofCastAndRotation
        (Nat.add_assoc n₁ n₂ n₃) (Nat.add_assoc m₁ m₂ m₃)
        (KuuNativeF45Tree.node (KuuNativeF45Tree.node t₁ t₂) t₃)
        (KuuNativeF45Tree.node t₁ (KuuNativeF45Tree.node t₂ t₃))
        (KuuNativeF45Tree.LocalRotation.assoc t₁ t₂ t₃)).mapAxes F G).toRoute :=
      KuuNativeF54CastRotationPacket.toRoute_mapAxes F G _
    _ = _ := congrArg KuuNativeF54CastRotationPacket.toRoute
      (nativeRootCastPacket_mapAxes_exact F G t₁ t₂ t₃)

#print axioms nativePackedRootMappedRotation
#print axioms nativeRootCastPacket_mapAxes_exact
#print axioms nativeGeneralRootAssoc_mapAxes_packed
end
end Kuu.F112.Physical
