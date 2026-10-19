import KuuOSFormal.HistoricalF36F40BridgeP4

/-!
# F112-P15 — genuine signed integral C60 two-chain linear equivalence

The P13 actual native-to-historical signed 32-face transport has an explicit
reverse integer-linear map. The P11 face orientation coefficients square to
one, so the two transports are inverse on every finitely supported integer
2-chain, not only on the fundamental cycle.

Together with P14's separately constructed commuting native boundary this
gives a Z-linear equivalence between the FULL kernels of the native and
historical 32-face-to-90-edge boundaries. All 90 edge coordinates retain
their historical physical-edge carrier. No independent higher F55 lift,
F68/F77 descent or full degree-0/1 chain equivalence is asserted.
-/

namespace KUOS.F112ActualHistoricalF36F40BridgeP4
namespace GenuineOriginalC60Geometry

open Kuu.F112.Physical
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationGrayC60IntegralBoundaryLinearMapV5_159

set_option autoImplicit false
set_option warningAsError true
noncomputable section

/-- The native P11 orientation sign is a unit of Z, including the
negative sign used by the verified P13 face transport. -/
theorem p15_negative_face_sign_square_one (p : Polygon) :
    (-c60SurfaceFaceSign p) * (-c60SurfaceFaceSign p) = (1 : ℤ) := by
  simpa only [neg_mul_neg] using c60SurfaceFaceSign_sq_one p

/-- Reverse orientation-corrected transport on the actual original
F59 32-face Finsupp carrier. This inverse is constructed directly
from the genuine P8 polygon Equiv, not extracted from an assumed
bijection or manufactured homology equivalence. -/
def originalFaceChainToNativeP11 :
    C60IntegralTwoChains →ₗ[ℤ] NativeC60IntegralTwoChains :=
  Finsupp.linearCombination ℤ
    (fun f : TruncatedIcosahedralSeedFace =>
      Finsupp.single (polygonEquiv.symm f)
        (-c60SurfaceFaceSign (polygonEquiv.symm f)))

/-- The reverse map on an arbitrary coefficient of any actual
historical C60 face. -/
theorem originalFaceChainToNativeP11_single
    (f : TruncatedIcosahedralSeedFace) (z : ℤ) :
    originalFaceChainToNativeP11 (Finsupp.single f z) =
      z • Finsupp.single (polygonEquiv.symm f)
        (-c60SurfaceFaceSign (polygonEquiv.symm f)) := by
  simp [originalFaceChainToNativeP11]

/-- Strict left-inverse identity of Z-linear maps on all native
finitely supported 32-face chains. -/
theorem originalFaceChainToNativeP11_comp_native :
    originalFaceChainToNativeP11.comp nativeP11ToOriginalFaceChain =
      LinearMap.id := by
  apply Finsupp.lhom_ext
  intro p z
  change originalFaceChainToNativeP11
      (nativeP11ToOriginalFaceChain (Finsupp.single p z)) =
    Finsupp.single p z
  calc
    originalFaceChainToNativeP11
        (nativeP11ToOriginalFaceChain (Finsupp.single p z)) =
      z • ((-c60SurfaceFaceSign p) •
        (Finsupp.single p (-c60SurfaceFaceSign p) :
          NativeC60IntegralTwoChains)) := by
        rw [nativeP11ToOriginalFaceChain_single, map_smul,
          originalFaceChainToNativeP11_single,
          Equiv.symm_apply_apply]
    _ = z • (Finsupp.single p (1 : ℤ) :
          NativeC60IntegralTwoChains) := by
        rw [Finsupp.smul_single', p15_negative_face_sign_square_one]
    _ = Finsupp.single p z := Finsupp.smul_single_one p z

/-- Strict right-inverse identity of Z-linear maps on the entire
original C60 32-face integer chain group. -/
theorem nativeP11ToOriginalFaceChain_comp_reverse :
    nativeP11ToOriginalFaceChain.comp originalFaceChainToNativeP11 =
      LinearMap.id := by
  apply Finsupp.lhom_ext
  intro f z
  change nativeP11ToOriginalFaceChain
      (originalFaceChainToNativeP11 (Finsupp.single f z)) =
    Finsupp.single f z
  calc
    nativeP11ToOriginalFaceChain
        (originalFaceChainToNativeP11 (Finsupp.single f z)) =
      z • ((-c60SurfaceFaceSign (polygonEquiv.symm f)) •
        (Finsupp.single f
          (-c60SurfaceFaceSign (polygonEquiv.symm f)) :
            C60IntegralTwoChains)) := by
        rw [originalFaceChainToNativeP11_single, map_smul,
          nativeP11ToOriginalFaceChain_single,
          Equiv.apply_symm_apply]
    _ = z • (Finsupp.single f (1 : ℤ) : C60IntegralTwoChains) := by
        rw [Finsupp.smul_single', p15_negative_face_sign_square_one]
    _ = Finsupp.single f z := Finsupp.smul_single_one f z

/-- Pointwise left inverse, derived from the equality of bundled
integer-linear maps instead of a second coordinate proof. -/
theorem originalFaceChainToNativeP11_left_inv
    (c : NativeC60IntegralTwoChains) :
    originalFaceChainToNativeP11 (nativeP11ToOriginalFaceChain c) = c := by
  have h := congrArg
    (fun L : NativeC60IntegralTwoChains →ₗ[ℤ] NativeC60IntegralTwoChains =>
      L c) originalFaceChainToNativeP11_comp_native
  simpa only [LinearMap.comp_apply, LinearMap.id_apply] using h

/-- Pointwise right inverse on every historical integral 2-chain. -/
theorem nativeP11ToOriginalFaceChain_right_inv
    (h : C60IntegralTwoChains) :
    nativeP11ToOriginalFaceChain (originalFaceChainToNativeP11 h) = h := by
  have hh := congrArg
    (fun L : C60IntegralTwoChains →ₗ[ℤ] C60IntegralTwoChains =>
      L h) nativeP11ToOriginalFaceChain_comp_reverse
  simpa only [LinearMap.comp_apply, LinearMap.id_apply] using hh

/-- Genuine sign- and geometry-corrected degree-two Z-linear
isomorphism on ALL 32-face finitely supported integral chains. -/
def nativeP11OriginalFaceChainLinearEquiv :
    NativeC60IntegralTwoChains ≃ₗ[ℤ] C60IntegralTwoChains where
  toLinearMap := nativeP11ToOriginalFaceChain
  invFun := originalFaceChainToNativeP11
  left_inv := originalFaceChainToNativeP11_left_inv
  right_inv := nativeP11ToOriginalFaceChain_right_inv

/-- Every historical 2-cycle has a closed native 2-chain preimage,
using the independently proved P14 boundary commuting square. -/
theorem originalClosedTwoChain_reverse_mem_native_kernel
    (h : C60IntegralTwoChains)
    (hh : h ∈ c60IntegralBoundaryTwo.ker) :
    originalFaceChainToNativeP11 h ∈ nativeC60IntegralBoundaryTwo.ker := by
  change nativeC60IntegralBoundaryTwo (originalFaceChainToNativeP11 h) = 0
  rw [nativeC60IntegralBoundaryTwo_commutes,
    nativeP11ToOriginalFaceChain_right_inv]
  exact hh

/-- F112-P15 central result: the ENTIRE native integral 2-cycle
module is Z-linearly equivalent to the ACTUAL historical original
integral degree-two boundary kernel. This is stronger than transport
of one nonzero surface, but does not claim a higher F55 obstruction
has vanished or degree-0/1 independent chain modules are isomorphic. -/
def nativeC60IntegralClosedTwoChainLinearEquiv :
    nativeC60IntegralBoundaryTwo.ker ≃ₗ[ℤ]
      c60IntegralBoundaryTwo.ker where
  toFun c :=
    ⟨nativeP11ToOriginalFaceChain c.val,
      nativeC60IntegralBoundaryTwo_kernel_transport c.val c.property⟩
  invFun h :=
    ⟨originalFaceChainToNativeP11 h.val,
      originalClosedTwoChain_reverse_mem_native_kernel h.val h.property⟩
  left_inv c := by
    apply Subtype.ext
    exact originalFaceChainToNativeP11_left_inv c.val
  right_inv h := by
    apply Subtype.ext
    exact nativeP11ToOriginalFaceChain_right_inv h.val
  map_add' c d := by
    apply Subtype.ext
    exact map_add nativeP11ToOriginalFaceChain c.val d.val
  map_smul' z c := by
    apply Subtype.ext
    exact map_smul nativeP11ToOriginalFaceChain z c.val

/-- Its value on the actual independently oriented nonzero P11
surface remains exactly the negative of the historical F59
fundamental surface, now under the full kernel-level equivalence. -/
theorem nativeC60IntegralClosedTwoChainLinearEquiv_fundamental :
    (nativeC60IntegralClosedTwoChainLinearEquiv
      ⟨nativeP11FundamentalTwoChain,
        nativeP11FundamentalTwoChain_mem_new_kernel⟩).val =
      -c60IntegralFundamentalSurfaceChain := by
  exact nativeP11ToOriginalFaceChain_fundamental

/-- The full closed-cycle equivalence recovers the original native
fundamental surface after backward/forward transport. -/
theorem nativeC60IntegralClosedTwoChainLinearEquiv_fundamental_roundtrip :
    nativeC60IntegralClosedTwoChainLinearEquiv.symm
      (nativeC60IntegralClosedTwoChainLinearEquiv
        ⟨nativeP11FundamentalTwoChain,
          nativeP11FundamentalTwoChain_mem_new_kernel⟩) =
      ⟨nativeP11FundamentalTwoChain,
        nativeP11FundamentalTwoChain_mem_new_kernel⟩ := by
  exact nativeC60IntegralClosedTwoChainLinearEquiv.symm_apply_apply _

#print axioms p15_negative_face_sign_square_one
#print axioms originalFaceChainToNativeP11
#print axioms originalFaceChainToNativeP11_single
#print axioms originalFaceChainToNativeP11_comp_native
#print axioms nativeP11ToOriginalFaceChain_comp_reverse
#print axioms originalFaceChainToNativeP11_left_inv
#print axioms nativeP11ToOriginalFaceChain_right_inv
#print axioms nativeP11OriginalFaceChainLinearEquiv
#print axioms originalClosedTwoChain_reverse_mem_native_kernel
#print axioms nativeC60IntegralClosedTwoChainLinearEquiv
#print axioms nativeC60IntegralClosedTwoChainLinearEquiv_fundamental
#print axioms nativeC60IntegralClosedTwoChainLinearEquiv_fundamental_roundtrip

end GenuineOriginalC60Geometry
end KUOS.F112ActualHistoricalF36F40BridgeP4
