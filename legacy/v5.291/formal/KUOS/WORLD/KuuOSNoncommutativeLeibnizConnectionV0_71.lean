import Mathlib
import KUOS.WORLD.KuuOSModuleBundleSelfOrganizationV0_70

/-!
# KuuOS noncommutative Leibniz connections v0.71

The scalar ring is not assumed commutative.  A directional connection obeys
Leibniz with respect to an algebra derivation.  The difference of two
connections with the same derivation is module-linear.  For commuting base
derivations, the connection commutator is also module-linear and therefore
represents curvature on the module fiber.
-/

namespace KUOS.WORLD.KuuOSNoncommutativeLeibnizConnectionV0_71

variable {A M : Type*}
variable [Ring A]
variable [AddCommGroup M] [Module A M]

structure AlgebraDerivation (A : Type*) [Ring A] where
  toFun : A → A
  map_add : ∀ a b, toFun (a + b) = toFun a + toFun b
  leibniz : ∀ a b, toFun (a * b) = toFun a * b + a * toFun b

instance : CoeFun (AlgebraDerivation A) (fun _ => A → A) :=
  ⟨AlgebraDerivation.toFun⟩

structure DirectionalConnection (δ : AlgebraDerivation A) where
  toFun : M → M
  map_add : ∀ x y, toFun (x + y) = toFun x + toFun y
  leibniz : ∀ a x, toFun (a • x) = δ a • x + a • toFun x

instance {δ : AlgebraDerivation A} :
    CoeFun (DirectionalConnection (M := M) δ) (fun _ => M → M) :=
  ⟨DirectionalConnection.toFun⟩

theorem connection_satisfies_leibniz
    (δ : AlgebraDerivation A)
    (nabla : DirectionalConnection (M := M) δ)
    (a : A)
    (x : M) :
    nabla (a • x) = δ a • x + a • nabla x := by
  exact nabla.leibniz a x

def connectionDifference
    (δ : AlgebraDerivation A)
    (first second : DirectionalConnection (M := M) δ) : M →ₗ[A] M where
  toFun x := first x - second x
  map_add' x y := by
    rw [first.map_add x y, second.map_add x y]
    abel
  map_smul' a x := by
    rw [first.leibniz a x, second.leibniz a x, smul_sub]
    abel

theorem difference_of_leibniz_connections_is_module_linear
    (δ : AlgebraDerivation A)
    (first second : DirectionalConnection (M := M) δ)
    (a : A)
    (x : M) :
    connectionDifference δ first second (a • x) =
      a • connectionDifference δ first second x := by
  exact map_smul (connectionDifference δ first second) a x

def addLinearDeformation
    (δ : AlgebraDerivation A)
    (nabla : DirectionalConnection (M := M) δ)
    (alpha : M →ₗ[A] M) : DirectionalConnection (M := M) δ where
  toFun x := nabla x + alpha x
  map_add x y := by
    rw [nabla.map_add x y, alpha.map_add x y]
    abel
  leibniz a x := by
    rw [nabla.leibniz a x, alpha.map_smul a x, smul_add]
    abel

theorem add_module_linear_deformation_preserves_leibniz
    (δ : AlgebraDerivation A)
    (nabla : DirectionalConnection (M := M) δ)
    (alpha : M →ₗ[A] M)
    (a : A)
    (x : M) :
    addLinearDeformation δ nabla alpha (a • x) =
      δ a • x + a • addLinearDeformation δ nabla alpha x := by
  exact (addLinearDeformation δ nabla alpha).leibniz a x

def connectionCommutator
    (δ₀ δ₁ : AlgebraDerivation A)
    (nabla₀ : DirectionalConnection (M := M) δ₀)
    (nabla₁ : DirectionalConnection (M := M) δ₁)
    (x : M) : M :=
  nabla₁ (nabla₀ x) - nabla₀ (nabla₁ x)

theorem connectionCommutator_add
    (δ₀ δ₁ : AlgebraDerivation A)
    (nabla₀ : DirectionalConnection (M := M) δ₀)
    (nabla₁ : DirectionalConnection (M := M) δ₁)
    (x y : M) :
    connectionCommutator δ₀ δ₁ nabla₀ nabla₁ (x + y) =
      connectionCommutator δ₀ δ₁ nabla₀ nabla₁ x +
        connectionCommutator δ₀ δ₁ nabla₀ nabla₁ y := by
  unfold connectionCommutator
  rw [nabla₀.map_add x y, nabla₁.map_add x y]
  rw [nabla₁.map_add (nabla₀ x) (nabla₀ y)]
  rw [nabla₀.map_add (nabla₁ x) (nabla₁ y)]
  abel

theorem connectionCommutator_smul
    (δ₀ δ₁ : AlgebraDerivation A)
    (nabla₀ : DirectionalConnection (M := M) δ₀)
    (nabla₁ : DirectionalConnection (M := M) δ₁)
    (hCommute : ∀ a, δ₁ (δ₀ a) = δ₀ (δ₁ a))
    (a : A)
    (x : M) :
    connectionCommutator δ₀ δ₁ nabla₀ nabla₁ (a • x) =
      a • connectionCommutator δ₀ δ₁ nabla₀ nabla₁ x := by
  unfold connectionCommutator
  rw [nabla₀.leibniz a x, nabla₁.leibniz a x]
  rw [nabla₁.map_add, nabla₀.map_add]
  rw [nabla₁.leibniz (δ₀ a) x, nabla₁.leibniz a (nabla₀ x)]
  rw [nabla₀.leibniz (δ₁ a) x, nabla₀.leibniz a (nabla₁ x)]
  rw [hCommute a, smul_sub]
  abel

def curvatureLinear
    (δ₀ δ₁ : AlgebraDerivation A)
    (nabla₀ : DirectionalConnection (M := M) δ₀)
    (nabla₁ : DirectionalConnection (M := M) δ₁)
    (hCommute : ∀ a, δ₁ (δ₀ a) = δ₀ (δ₁ a)) : M →ₗ[A] M where
  toFun := connectionCommutator δ₀ δ₁ nabla₀ nabla₁
  map_add' := connectionCommutator_add δ₀ δ₁ nabla₀ nabla₁
  map_smul' := connectionCommutator_smul δ₀ δ₁ nabla₀ nabla₁ hCommute

theorem commuting_derivations_make_curvature_module_linear
    (δ₀ δ₁ : AlgebraDerivation A)
    (nabla₀ : DirectionalConnection (M := M) δ₀)
    (nabla₁ : DirectionalConnection (M := M) δ₁)
    (hCommute : ∀ a, δ₁ (δ₀ a) = δ₀ (δ₁ a))
    (a : A)
    (x : M) :
    curvatureLinear δ₀ δ₁ nabla₀ nabla₁ hCommute (a • x) =
      a • curvatureLinear δ₀ δ₁ nabla₀ nabla₁ hCommute x := by
  exact map_smul (curvatureLinear δ₀ δ₁ nabla₀ nabla₁ hCommute) a x

def gaugeTransformLinear
    (g : M ≃ₗ[A] M)
    (alpha : M →ₗ[A] M) : M →ₗ[A] M :=
  g.toLinearMap.comp (alpha.comp g.symm.toLinearMap)

theorem gauge_transform_preserves_module_linearity
    (g : M ≃ₗ[A] M)
    (alpha : M →ₗ[A] M)
    (a : A)
    (x : M) :
    gaugeTransformLinear g alpha (a • x) =
      a • gaugeTransformLinear g alpha x := by
  exact map_smul (gaugeTransformLinear g alpha) a x

theorem rollback_linear_deformation_recovers_connection
    (δ : AlgebraDerivation A)
    (nabla : DirectionalConnection (M := M) δ)
    (alpha : M →ₗ[A] M)
    (x : M) :
    addLinearDeformation δ nabla alpha x - alpha x = nabla x := by
  simp [addLinearDeformation]

end KUOS.WORLD.KuuOSNoncommutativeLeibnizConnectionV0_71
