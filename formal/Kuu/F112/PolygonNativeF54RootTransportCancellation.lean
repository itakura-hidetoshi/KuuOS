import Kuu.F112.PolygonNativeF54RootStepNormalization

/-!
# F112-E7Q5-F4-K — cancellation of a dependent local-rotation reindexing

The F4-I cast/rotation packet and F4-J normalized root are proof-relevant.
The root case of `LocalRotation.mapAxes` changes its dependent input via
the F45 `mapAxes_castDepths` equality; the packed construction changes
it back via the SAME equality. Here the cancellation is isolated as a
general Eq.mp/Eq.mpr transport law, before applying it to real raw F54
witnesses. This is not proof irrelevance for LocalRotation; only equality
transport is canceled.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
noncomputable section

universe u v uA vA uB vB uC vC uD vD

private theorem rootTransport_cancel
    {α : Sort u} {a b : α} (h : a = b)
    (P : α → Sort v) (z : P b) :
    Eq.mp (congrArg P h) (Eq.mpr (congrArg P h) z) = z := by
  cases h
  rfl

variable {A : Type uA} [Category.{vA} A]
variable {B : Type uB} [Category.{vB} B]
variable {C : Type uC} [Category.{vC} C]
variable {D : Type uD} [Category.{vD} D]

/-- The actual transported root F54 local rotation is the CANONICAL
root generator at the mapped F45 trees, at arbitrary six Nat depths.
No raw two-path equality or F55 quotient simplification is used. -/
theorem nativePackedRootMappedRotation_eq_assoc
    (F : A ⥤ C) (G : B ⥤ D)
    {p : Polygon} {a b : A} {x y : B}
    {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
    {p₀ p₁ p₂ p₃ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ q₃ : KuuNativeBlocks x y}
    (t₁ : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁)
    (t₂ : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂)
    (t₃ : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃) :
    nativePackedRootMappedRotation F G t₁ t₂ t₃ =
      KuuNativeF45Tree.LocalRotation.assoc
        (t₁.mapAxes F G) (t₂.mapAxes F G) (t₃.mapAxes F G) := by
  let origin := KuuNativeF45Tree.node (KuuNativeF45Tree.node t₁ t₂) t₃
  let target := KuuNativeF45Tree.node
    (t₁.mapAxes F G) (KuuNativeF45Tree.node (t₂.mapAxes F G) (t₃.mapAxes F G))
  let P : KuuNativeF45Tree p
      (n₁ + (n₂ + n₃)) (m₁ + (m₂ + m₃))
      (p₀.map F) (q₀.map G) (p₃.map F) (q₃.map G) → Type _ :=
    fun s => KuuNativeF45Tree.LocalRotation p s target
  let h := KuuNativeF45Tree.mapAxes_castDepths F G
    (Nat.add_assoc n₁ n₂ n₃) (Nat.add_assoc m₁ m₂ m₃) origin
  have hmap :
      (KuuNativeF45Tree.LocalRotation.assoc t₁ t₂ t₃).mapAxes F G =
        Eq.mpr (congrArg P h)
          (KuuNativeF45Tree.LocalRotation.assoc
            (t₁.mapAxes F G) (t₂.mapAxes F G) (t₃.mapAxes F G)) := by
    rfl
  have hpack :
      nativePackedRootMappedRotation F G t₁ t₂ t₃ =
        Eq.mp (congrArg P h)
          ((KuuNativeF45Tree.LocalRotation.assoc t₁ t₂ t₃).mapAxes F G) := by
    rfl
  exact hpack.trans
    ((congrArg (Eq.mp (congrArg P h)) hmap).trans
      (rootTransport_cancel h P _))

/-- Discharge the exact F4-J normalization structure without an axiom. -/
def nativeF54RootStepNormalization
    (F : A ⥤ C) (G : B ⥤ D) :
    KuuNativeF54RootStepNormalization F G where
  step := fun _p {_a _b} {_x _y}
    {_n₁ _n₂ _n₃ _m₁ _m₂ _m₃}
    {_p₀ _p₁ _p₂ _p₃} {_q₀ _q₁ _q₂ _q₃}
    t₁ t₂ t₃ =>
      nativePackedRootMappedRotation_eq_assoc F G t₁ t₂ t₃

#print axioms nativePackedRootMappedRotation_eq_assoc
#print axioms nativeF54RootStepNormalization
end
end Kuu.F112.Physical
