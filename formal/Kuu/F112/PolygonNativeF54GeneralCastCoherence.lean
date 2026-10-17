import Kuu.F112.PolygonNativeF55SymbolicTailPentagon

/-!
# F112-E7Q5-F4-G — explicit dependent cast-congruence for arbitrary Nat depths

The frozen independent E7O original-shaped root associator consists
of a double Nat.add_assoc cast followed by an ACTUAL proof-relevant
forward F54 local rotation. The F4-C/D/E/F positive results show
strict two-axis functor naturality for concrete or constrained depth
profiles. At unrestricted symbolic Nat indices, the tree-cast
comparison holds by the already proved E7Q5-D transport lemma, but
simply rewriting INSIDE the dependent F54 route is ill typed.

We test a mathematically explicit strategy: first extract the exact
casted F45 tree equality, then eliminate it on the whole higher
source proposition. The eventual proof must be genuinely typed,
never inferred from sector lists, rotation counts or shadow grades.
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

/-- Attempt to prove original source F54 root associator naturality
for fully arbitrary n₁,n₂,n₃,m₁,m₂,m₃, using equality elimination
of the independently proved, genuinely dependent double-cast tree
rather than an invalid context-insensitive rewrite. -/
theorem nativeGeneralNatAssoc_mapAxes_naturality
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
  have hcast :=
    KuuNativeF45Tree.mapAxes_castDepths F G
      (Nat.add_assoc n₁ n₂ n₃)
      (Nat.add_assoc m₁ m₂ m₃)
      (KuuNativeF45Tree.node
        (KuuNativeF45Tree.node t₁ t₂) t₃)
  cases hcast
  rfl

#print axioms nativeGeneralNatAssoc_mapAxes_naturality
end
end Kuu.F112.Physical
