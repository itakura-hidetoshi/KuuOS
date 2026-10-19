import KuuOSFormal.HistoricalF36F40BridgeP19

/-!
# F112-P20 — compatibility of P17 and direct P19 fundamental H₂ presentations

The P17 class uses the concrete kernel-transport iso; the P19 class
uses ShortComplex.moduleCatCyclesIso.inv and homologyπ.  We prove
that they identify the *same original P11 integer surface* in the
true native kernel, then transport equality back through the genuine
categorical isomorphism.  No new Gray lift or classical free-generator
axiom is introduced.
-/

namespace KUOS.F112ActualHistoricalF36F40BridgeP4
namespace GenuineOriginalC60Geometry

open CategoryTheory Limits
open KUOS.DependentOriginationGrayC60IntegralBoundaryLinearMapV5_159
open KUOS.DependentOriginationGrayC60IntegralChainComplexV5_160
open KUOS.DependentOriginationGrayC60NativeChainComplexV5_160
open KUOS.DependentOriginationGrayC60NativeH2FundamentalClassV5_161

set_option autoImplicit false
set_option warningAsError true
noncomputable section

/-- The directly constructed categorical P11 class has precisely
the actual native oriented P11 surface as its P17 kernel coordinate. -/
theorem p20DirectClass_concreteKernel :
    independentC60H2ConcreteCycleIso.hom.hom
        p19IndependentFundamentalClass =
      (⟨nativeP11FundamentalTwoChain,
        nativeP11FundamentalTwoChain_mem_new_kernel⟩ :
        LinearMap.ker nativeC60IntegralBoundaryTwo) := by
  apply Subtype.ext
  -- P17's concrete-kernel isomorphism was transported through a
  -- propositional equality of kernels. The two arrows cannot be
  -- interchanged by `change` (which requires definitional equality).
  have hcompat :
      (independentC60H2ConcreteCycleIso.hom.hom
        p19IndependentFundamentalClass).val =
      ((independentC60IntegralCellularComplex.sc 2).moduleCatCyclesIso.hom.hom
        (independentC60H2FundamentalπIso.inv.hom
          ((independentC60IntegralCellularComplex.homologyπ 2)
            p19IndependentFundamentalCycle))).val := by
    simp [independentC60H2ConcreteCycleIso,
      p19IndependentFundamentalClass]
    exact independentC60H2KernelPresentationIso_val _
  rw [hcompat]
  change
    ((independentC60IntegralCellularComplex.sc 2).moduleCatCyclesIso.hom.hom
      (independentC60H2FundamentalπIso.inv
        (independentC60H2FundamentalπIso.hom
          p19IndependentFundamentalCycle))).val =
        nativeP11FundamentalTwoChain
  rw [independentC60H2FundamentalπIso.hom_inv_id_apply]
  have h := p19IndependentFundamentalCycle_iCycles
  change (independentC60IntegralCellularComplex.sc 2).iCycles
    p19IndependentFundamentalCycle = nativeP11FundamentalTwoChain at h
  rw [← (independentC60IntegralCellularComplex.sc 2).moduleCatCyclesIso_hom_i] at h
  change
    ((independentC60IntegralCellularComplex.sc 2).moduleCatCyclesIso.hom.hom
      p19IndependentFundamentalCycle).val = nativeP11FundamentalTwoChain at h
  exact h

/-- P17's kernel-iso generator and P19's direct ShortComplex
generator are the same element of genuine categorical H₂. -/
theorem p20P17FundamentalClass_eq_P19Direct :
    independentC60H2FundamentalClass = p19IndependentFundamentalClass := by
  apply (ModuleCat.mono_iff_injective
    independentC60H2ConcreteCycleIso.hom).mp inferInstance
  change
    independentC60H2ConcreteCycleIso.hom.hom
      independentC60H2FundamentalClass =
    independentC60H2ConcreteCycleIso.hom.hom
      p19IndependentFundamentalClass
  rw [independentC60H2FundamentalClass,
    independentC60H2ConcreteCycleIso.inv_hom_id_apply]
  exact p20DirectClass_concreteKernel.symm

/-- Final signed naturality for the ORIGINAL P17 fundamental class,
not only for a newly chosen rank-one generator. -/
theorem p20P17IndependentHistoricalH2_sign :
    independentHistoricalC60H2Iso.hom.hom
        independentC60H2FundamentalClass =
      -c60NativeH2FundamentalClass := by
  rw [p20P17FundamentalClass_eq_P19Direct]
  exact p19IndependentHistoricalH2_sign

#print axioms p20DirectClass_concreteKernel
#print axioms p20P17FundamentalClass_eq_P19Direct
#print axioms p20P17IndependentHistoricalH2_sign


/-! ## P20B — additional direct-class coordinates and infinite-order consequences -/

/-- The concrete-kernel H₂ isomorphism of P17 applied to the
DIRECTLY represented P19 homology class recovers precisely the
real native signed P11 fundamental surface on the 32 native
polygon faces. The statement explicitly identifies the two
kernel PRESENTATIONS rather than asserting that their cast is rfl. -/
theorem p20DirectFundamentalClass_concrete_val :
    (independentC60H2ConcreteCycleIso.hom.hom
      p19IndependentFundamentalClass).val =
        nativeP11FundamentalTwoChain := by
  -- P17's concrete-kernel isomorphism was transported through a
  -- propositional equality of kernels. The two arrows cannot be
  -- interchanged by `change` (which requires definitional equality).
  have hcompat :
      (independentC60H2ConcreteCycleIso.hom.hom
        p19IndependentFundamentalClass).val =
      ((independentC60IntegralCellularComplex.sc 2).moduleCatCyclesIso.hom.hom
        (independentC60H2FundamentalπIso.inv.hom
          ((independentC60IntegralCellularComplex.homologyπ 2)
            p19IndependentFundamentalCycle))).val := by
    simp [independentC60H2ConcreteCycleIso,
      p19IndependentFundamentalClass]
    exact independentC60H2KernelPresentationIso_val _
  rw [hcompat]
  have hπ :
      independentC60H2FundamentalπIso.inv.hom
        ((independentC60IntegralCellularComplex.homologyπ 2)
          p19IndependentFundamentalCycle) =
        p19IndependentFundamentalCycle := by
    change independentC60H2FundamentalπIso.inv.hom
      (independentC60H2FundamentalπIso.hom.hom
        p19IndependentFundamentalCycle) =
      p19IndependentFundamentalCycle
    exact independentC60H2FundamentalπIso.hom_inv_id_apply _
  rw [hπ]
  have h := p19IndependentFundamentalCycle_iCycles
  change (independentC60IntegralCellularComplex.sc 2).iCycles
    p19IndependentFundamentalCycle = nativeP11FundamentalTwoChain at h
  rw [← (independentC60IntegralCellularComplex.sc 2).moduleCatCyclesIso_hom_i] at h
  change
    ((independentC60IntegralCellularComplex.sc 2).moduleCatCyclesIso.hom.hom
      p19IndependentFundamentalCycle).val =
        nativeP11FundamentalTwoChain at h
  exact h

/-- F112-P20 principal theorem. The direct true ShortComplex
fundamental class of P19 and the P17 genuine native H₂ class
are EXACTLY THE SAME element. The proof uses injectivity of the
already constructed mathlib H₂-to-kernel isomorphism, not an
assumed equality of unrelated quotient presentations. -/
theorem p20IndependentFundamentalClass_eq_P17 :
    p19IndependentFundamentalClass =
      independentC60H2FundamentalClass := by
  have hi :
      Function.Injective independentC60H2ConcreteCycleIso.hom.hom :=
    (ModuleCat.mono_iff_injective _).mp inferInstance
  apply hi
  have h17 :
      independentC60H2ConcreteCycleIso.hom.hom
        independentC60H2FundamentalClass =
        (⟨nativeP11FundamentalTwoChain,
          nativeP11FundamentalTwoChain_mem_new_kernel⟩ :
          LinearMap.ker nativeC60IntegralBoundaryTwo) := by
    change independentC60H2ConcreteCycleIso.hom.hom
      (independentC60H2ConcreteCycleIso.inv
        (⟨nativeP11FundamentalTwoChain,
          nativeP11FundamentalTwoChain_mem_new_kernel⟩ :
          LinearMap.ker nativeC60IntegralBoundaryTwo)) = _
    exact independentC60H2ConcreteCycleIso.inv_hom_id_apply _
  rw [h17]
  apply Subtype.ext
  exact p20DirectFundamentalClass_concrete_val

/-- The P19 *directly represented* fundamental H₂ class has
the same genuine integer north-pentagon coordinate +1 as the
P17 independently classified primitive generator. -/
theorem p20DirectFundamentalClass_coordinate :
    independentC60H2IsoInteger.hom.hom
      p19IndependentFundamentalClass = (1 : ℤ) := by
  rw [p20IndependentFundamentalClass_eq_P17]
  exact independentC60H2FundamentalClass_coordinate

/-- The P18 signed historical chain-isomorphism now carries
the ORIGINAL P17 fundamental class (not merely P19's alternative
direct presentation) to the NEGATIVE of the historical F59
genuine fundamental H₂ class. -/
theorem p20P17HistoricalH2_fundamental_sign :
    independentHistoricalC60H2Iso.hom.hom
      independentC60H2FundamentalClass =
        -c60NativeH2FundamentalClass := by
  rw [← p20IndependentFundamentalClass_eq_P17]
  exact p19IndependentHistoricalH2_sign

/-- The P19 direct native class has infinite integer order,
the same canonical P17 generator already certified via true
32-polygon H₂ ≅ Z. -/
theorem p20DirectFundamentalClass_infinite_order :
    Function.Injective (fun n : ℤ =>
      n • p19IndependentFundamentalClass) := by
  simpa only [p20IndependentFundamentalClass_eq_P17] using
    independentC60H2FundamentalClass_infinite_order

#print axioms p20DirectFundamentalClass_concrete_val
#print axioms p20IndependentFundamentalClass_eq_P17
#print axioms p20DirectFundamentalClass_coordinate
#print axioms p20P17HistoricalH2_fundamental_sign
#print axioms p20DirectFundamentalClass_infinite_order


end
end GenuineOriginalC60Geometry
end KUOS.F112ActualHistoricalF36F40BridgeP4
