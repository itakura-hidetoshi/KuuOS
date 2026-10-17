import Kuu.F112.PolygonNativeF54PackedCastRotation

/-!
# F112-E7Q5-F4-I2 — genuine root associator transport via Sigma packet

Test whether the original generated local F54 associator, after
correct typed F45 double-cast transport, becomes the genuine mapped
root constructor, instead of a manufactured shadow or Gray cell.
Then extract naturality of the full F54 raw assoc route by projection
from the proof-relevant intermediate packet. The statements refer
only to independent native original-shaped F41/F45/F54 source.
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

/-- Normalize the actual proof-relevant root LocalRotation witness
AFTER transporting its dependent source tree equality as one unit. -/
theorem KuuNativeF45Tree.LocalRotation.mapAxes_assoc_transport
    (F : A ⥤ C) (G : B ⥤ D)
    {p : Polygon} {a b : A} {x y : B}
    {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
    {p₀ p₁ p₂ p₃ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ q₃ : KuuNativeBlocks x y}
    (t₁ : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁)
    (t₂ : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂)
    (t₃ : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃) :
    (KuuNativeF45Tree.mapAxes_castDepths F G
       (Nat.add_assoc n₁ n₂ n₃) (Nat.add_assoc m₁ m₂ m₃)
       (KuuNativeF45Tree.node (KuuNativeF45Tree.node t₁ t₂) t₃)) ▸
      ((KuuNativeF45Tree.LocalRotation.assoc t₁ t₂ t₃).mapAxes F G) =
        KuuNativeF45Tree.LocalRotation.assoc
          (t₁.mapAxes F G) (t₂.mapAxes F G) (t₃.mapAxes F G) := by
  have ht := KuuNativeF45Tree.mapAxes_castDepths F G
    (Nat.add_assoc n₁ n₂ n₃) (Nat.add_assoc m₁ m₂ m₃)
    (KuuNativeF45Tree.node (KuuNativeF45Tree.node t₁ t₂) t₃)
  have htype :
      KuuNativeF45Tree.LocalRotation p
        ((KuuNativeF45Tree.castDepths
          (Nat.add_assoc n₁ n₂ n₃) (Nat.add_assoc m₁ m₂ m₃)
          (KuuNativeF45Tree.node (KuuNativeF45Tree.node t₁ t₂) t₃)).mapAxes F G)
        ((KuuNativeF45Tree.node t₁ (KuuNativeF45Tree.node t₂ t₃)).mapAxes F G) =
      KuuNativeF45Tree.LocalRotation p
        (KuuNativeF45Tree.castDepths
          (Nat.add_assoc n₁ n₂ n₃) (Nat.add_assoc m₁ m₂ m₃)
          ((KuuNativeF45Tree.node (KuuNativeF45Tree.node t₁ t₂) t₃).mapAxes F G))
        ((KuuNativeF45Tree.node t₁ (KuuNativeF45Tree.node t₂ t₃)).mapAxes F G) :=
    congrArg
      (fun mid => KuuNativeF45Tree.LocalRotation p mid
        ((KuuNativeF45Tree.node t₁ (KuuNativeF45Tree.node t₂ t₃)).mapAxes F G)) ht
  change htype.mp
    (htype.mpr (KuuNativeF45Tree.LocalRotation.assoc
      (t₁.mapAxes F G) (t₂.mapAxes F G) (t₃.mapAxes F G))) =
        KuuNativeF45Tree.LocalRotation.assoc
          (t₁.mapAxes F G) (t₂.mapAxes F G) (t₃.mapAxes F G)
  have lemma {X Y : Sort _} (h : X = Y) (v : Y) :
      h.mp (h.mpr v) = v := by
    cases h
    rfl
  exact lemma htype _

/-- Transport full original root Sigma packet with actual
source and target, exact intermediate tree, path and oriented edge. -/
theorem nativeRootCastPacket_mapAxes
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
      (KuuNativeF45Tree.LocalRotation.assoc
        (t₁.mapAxes F G) (t₂.mapAxes F G) (t₃.mapAxes F G)) := by
  rw [KuuNativeF54CastRotationPacket.mapAxes_ofCastAndRotation]
  rw [KuuNativeF45Tree.LocalRotation.mapAxes_assoc_transport]
  rfl

/-- General six-Nat original root F54 strict naturality, as an
EXACT theorem of the full paired intermediate source witness. -/
theorem nativeGeneralNatRootAssoc_mapAxes
    (F : A ⥤ C) (G : B ⥤ D)
    {p : Polygon} {a b : A} {x y : B}
    {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
    {p₀ p₁ p₂ p₃ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ q₃ : KuuNativeBlocks x y}
    (t₁ : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁)
    (t₂ : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂)
    (t₃ : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃) :
    (KuuNativeF45Tree.DepthRotationRoute.assoc t₁ t₂ t₃).mapAxes F G =
      KuuNativeF45Tree.DepthRotationRoute.assoc
        (t₁.mapAxes F G) (t₂.mapAxes F G) (t₃.mapAxes F G) := by
  calc
    (KuuNativeF45Tree.DepthRotationRoute.assoc t₁ t₂ t₃).mapAxes F G =
      (KuuNativeF54CastRotationPacket.ofCastAndRotation
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
    _ = (KuuNativeF54CastRotationPacket.ofCastAndRotation
        (Nat.add_assoc n₁ n₂ n₃) (Nat.add_assoc m₁ m₂ m₃)
        (KuuNativeF45Tree.node
          (KuuNativeF45Tree.node (t₁.mapAxes F G) (t₂.mapAxes F G))
          (t₃.mapAxes F G))
        (KuuNativeF45Tree.node (t₁.mapAxes F G)
          (KuuNativeF45Tree.node (t₂.mapAxes F G) (t₃.mapAxes F G)))
        (KuuNativeF45Tree.LocalRotation.assoc
          (t₁.mapAxes F G) (t₂.mapAxes F G) (t₃.mapAxes F G))).toRoute := by
      rw [nativeRootCastPacket_mapAxes F G t₁ t₂ t₃]
    _ = KuuNativeF45Tree.DepthRotationRoute.assoc
        (t₁.mapAxes F G) (t₂.mapAxes F G) (t₃.mapAxes F G) := rfl

#print axioms KuuNativeF45Tree.LocalRotation.mapAxes_assoc_transport
#print axioms nativeRootCastPacket_mapAxes
#print axioms nativeGeneralNatRootAssoc_mapAxes
end
end Kuu.F112.Physical
