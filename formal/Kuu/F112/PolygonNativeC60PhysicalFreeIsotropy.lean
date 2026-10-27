import Kuu.F112.PolygonNativeC60ConservativeFrameUnprefix

/-!
# F112-P94D3CY — genuine conservative strict isotropy IS a CN free group

CX proves that the actual CP kernel is trivial for every finite inner
and outer original AQ context at the physical conservative C60
fifteen-dimensional base. CY turns that proven theorem into an ACTUAL
group equivalence with CN's free group of genuine BC parallel-generator
certificates, not just an isomorphism of scalar or full BW observations.

The proof is generic group theory plus the exact physical CX theorem.
The group inverse is the EXISTING CO retraction, with original 14D/15D
Type-valued evidence retained in its CN fork alphabet and actual
strict automorphism carrier. This is the selected no-extra-relations
strict Kuu presentation; no Gray, new geometric 16-cell, Peiffer,
hyperdescent, axiom or sorry is introduced.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uCY vCY uD vD uE vE

section AbstractSplit

variable {G : Type uCY} {H : Type vCY} [Group G] [Group H]

/-- Kernel triviality implies injectivity of a genuine group
homomorphism. The proof uses its real kernel subgroup, never a
separately defined observational quotient. -/
theorem nativeC60CYGenericRetraction_injective
    (r : G →* H)
    (hker : ∀ k : r.ker, k = 1) :
    Function.Injective r := by
  intro x y hxy
  have hmem : x * y⁻¹ ∈ r.ker := by
    apply (MonoidHom.mem_ker).mpr
    rw [map_mul, map_inv, hxy, mul_inv_cancel]
  have heq : x * y⁻¹ = (1 : G) := by
    have hk := congrArg (fun k : r.ker => (k : G))
      (hker (⟨x * y⁻¹, hmem⟩ : r.ker))
    simpa only [Subgroup.coe_one] using hk
  calc
    x = (x * y⁻¹) * y := by group
    _ = 1 * y := by rw [heq]
    _ = y := one_mul y

/-- A split group retraction with the REAL kernel proved trivial
gives an explicit multiplication-preserving equivalence. -/
def nativeC60CYGenericSplitMulEquiv
    (r : G →* H) (i : H →* G)
    (split : ∀ h : H, r (i h) = h)
    (hker : ∀ k : r.ker, k = 1) : H ≃* G where
  toFun := i
  invFun := r
  left_inv := split
  right_inv := by
    intro z
    apply nativeC60CYGenericRetraction_injective r hker
    exact split (r z)
  map_mul' := i.map_mul

end AbstractSplit

section PhysicalC60

variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable {first : KuuNativeF45Tree p n m ma pa mb pb}
variable {last : KuuNativeF45Tree p n' m' ma pa mb pb}
variable {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
variable {f g : NativeF55StructuralComparison p r s}
variable {alpha beta : NativeK5StructuralFourCell p f g}
variable {w z : NativeK5StructuralFiveCell p alpha beta}
variable {u v : NativeK5StructuralSixCell p w z}
variable {h k : NativeK5StructuralSevenCell p u v}
variable {e d : NativeK5StructuralEightCell p h k}
variable {q t : NativeK5StructuralNineCell p e d}
variable {P Q : NativeK5StructuralTenCell p q t}
variable {H K : NativeK5StructuralElevenCell p P Q}
variable {U V : NativeK5StructuralTwelveCell p H K}

/-- Every member of the ACTUAL physical conservative CP strict kernel
equals its identity, by the unconditional CX typed-generator recovery. -/
theorem nativeK5CYPhysicalKernel_eq_one
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer : List Bool)
    (k : NativeC60CPKernel
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
      outer (nativeK5CKAtomGenerator W R inner)) :
    k = 1 := by
  by_contra hk
  exact nativeK5CXPhysical_strict_kernel_trivial W R inner outer ⟨k, hk⟩

/-- MAIN CY theorem. The actual genuine C60 conservative strict
automorphism group is the FULL free group on its ORIGINAL typed
parallel BC generators excluding one physical base generator.
This refines the CP semidirect decomposition because its true normal
kernel is now PROVED trivial, not postulated trivial. -/
def nativeK5CYPhysicalFreeIsotropy
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer : List Bool) :
    FreeGroup (NativeC60CNForkAlphabet
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
        (nativeK5CKAtomGenerator W R inner)) ≃*
      NativeC60COIsotropy
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
        outer (nativeK5CHSource W inner (nativeK5CKConservativeRefl W R)) :=
  nativeC60CYGenericSplitMulEquiv
    (nativeC60CORetraction
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
      outer (nativeK5CKAtomGenerator W R inner))
    (nativeC60COEmbed
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
      outer (nativeK5CKAtomGenerator W R inner))
    (nativeC60CORetraction_embed
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
      outer (nativeK5CKAtomGenerator W R inner))
    (nativeK5CYPhysicalKernel_eq_one W R inner outer)

/-- ALL actual conservative strict loops are rebuilt exactly from
their full CN coordinate inside the original strict automorphism
group, not just after application of the BW holonomy receiver. -/
theorem nativeK5CYPhysicalEvery_strict_loop_CN
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer : List Bool)
    (z : NativeC60COIsotropy
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
      outer (nativeK5CHSource W inner (nativeK5CKConservativeRefl W R))) :
    nativeC60COEmbed
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
        outer (nativeK5CKAtomGenerator W R inner)
        (nativeC60CORetraction
          (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
          outer (nativeK5CKAtomGenerator W R inner) z) = z :=
  (nativeK5CYPhysicalFreeIsotropy W R inner outer).right_inv z

/-- In the physically proven trivial-kernel sector, the actual
previously noncommutative CP conjugation action has only the identity
kernel element to act on. Outside this physical sector CQ/CS retain
their original conditional nontrivial-action theorems. -/
theorem nativeK5CYPhysical_kernel_action_trivial
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer : List Bool)
    (x : FreeGroup (NativeC60CNForkAlphabet
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
      (nativeK5CKAtomGenerator W R inner)))
    (k : NativeC60CPKernel
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
      outer (nativeK5CKAtomGenerator W R inner)) :
    nativeC60CPAction
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
      outer (nativeK5CKAtomGenerator W R inner) x k = k := by
  have hk := nativeK5CYPhysicalKernel_eq_one W R inner outer k
  rw [hk]
  simp

end PhysicalC60

#print axioms nativeC60CYGenericRetraction_injective
#print axioms nativeC60CYGenericSplitMulEquiv
#print axioms nativeK5CYPhysicalKernel_eq_one
#print axioms nativeK5CYPhysicalFreeIsotropy
#print axioms nativeK5CYPhysicalEvery_strict_loop_CN
#print axioms nativeK5CYPhysical_kernel_action_trivial

end
end Kuu.F112.Physical
