import Kuu.F112.PolygonNativeF55FunctorQuotient

/-!
# F112-E7Q5-F4-A — constructive pentagon-boundary naturality

Compare the RAW independent F54 rotation route created by a real
three-tree associativity against its image under two category functors.
This is not a comparison of charged shadows. In particular the
two Nat.add_assoc casts at the F54 root are treated explicitly.

The aim is to identify the minimal exact dependent coherence needed
to construct an inhabitant of KuuNativeF55MappedPentagonData, rather
than assuming such 3-cells from equality of shadow coordinates.

No legacy KUOS/Gray/F51/F77 dependencies are introduced.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
noncomputable section

universe uA vA uB vB uA₂ vA₂ uB₂ vB₂
variable {A : Type uA} [Category.{vA} A]
variable {B : Type uB} [Category.{vB} B]
variable {A₂ : Type uA₂} [Category.{vA₂} A₂]
variable {B₂ : Type uB₂} [Category.{vB₂} B₂]

/-- The genuinely stored one-step F54 route preserves its original
forward rotation witness under functor transport (not just length). -/
theorem KuuNativeF45Tree.DepthRotationRoute.mapAxes_ofLocalRotation
    (F : A ⥤ A₂) (G : B ⥤ B₂)
    {p : Polygon} {a b : A} {x y : B} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {before after : KuuNativeF45Tree p n m ma pa mb pb}
    (step : KuuNativeF45Tree.LocalRotation p before after) :
    (KuuNativeF45Tree.DepthRotationRoute.ofLocalRotation step).mapAxes F G =
      KuuNativeF45Tree.DepthRotationRoute.ofLocalRotation
        (step.mapAxes F G) := by
  rfl

/-- Even when exact raw pentagon-boundary naturality requires
a further dependent coherence proof, transport of the ACTUAL F54
root-rotation route preserves its single genuine rotation edge. -/
theorem KuuNativeF45Tree.DepthRotationRoute.mapAxes_assoc_count
    (F : A ⥤ A₂) (G : B ⥤ B₂)
    {p : Polygon} {a b : A} {x y : B}
    {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
    {p₀ p₁ p₂ p₃ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ q₃ : KuuNativeBlocks x y}
    (t₁ : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁)
    (t₂ : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂)
    (t₃ : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃) :
    ((KuuNativeF45Tree.DepthRotationRoute.assoc
      t₁ t₂ t₃).mapAxes F G).rotationCount = 1 := by
  rw [KuuNativeF45Tree.DepthRotationRoute.rotationCount_mapAxes]
  exact KuuNativeF45Tree.DepthRotationRoute.assoc_rotationCount t₁ t₂ t₃

/-- The real physical sector boundary is preserved by the mapped
F54 root associativity, without claiming equality of distinct raw
Nat-cast proof trees. -/
theorem KuuNativeF45Tree.DepthRotationRoute.mapAxes_assoc_physical
    (F : A ⥤ A₂) (G : B ⥤ B₂)
    {p : Polygon} {a b : A} {x y : B}
    {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
    {p₀ p₁ p₂ p₃ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ q₃ : KuuNativeBlocks x y}
    (t₁ : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁)
    (t₂ : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂)
    (t₃ : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃) :
    (((KuuNativeF45Tree.node (KuuNativeF45Tree.node t₁ t₂) t₃).mapAxes F G)
      .erasePhysical.erase.leaves) =
    (((KuuNativeF45Tree.node t₁ (KuuNativeF45Tree.node t₂ t₃)).mapAxes F G)
      .erasePhysical.erase.leaves) :=
  (KuuNativeF45Tree.DepthRotationRoute.assoc t₁ t₂ t₃).mapAxes_physical_leaves F G

#print axioms KuuNativeF45Tree.DepthRotationRoute.mapAxes_ofLocalRotation
#print axioms KuuNativeF45Tree.DepthRotationRoute.mapAxes_assoc_count
#print axioms KuuNativeF45Tree.DepthRotationRoute.mapAxes_assoc_physical
end
end Kuu.F112.Physical
