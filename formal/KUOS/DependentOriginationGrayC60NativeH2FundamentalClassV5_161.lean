import KUOS.DependentOriginationGrayC60NativeChainComplexV5_160
import Mathlib.Algebra.Homology.ShortComplex.ModuleCat
import Mathlib.Algebra.Homology.ShortComplex.HomologicalComplex

namespace KUOS.DependentOriginationGrayC60NativeH2FundamentalClassV5_161

open CategoryTheory
open KUOS.DependentOriginationGrayC60IntegralBoundaryLinearMapV5_159
open KUOS.DependentOriginationGrayC60IntegralChainComplexV5_160
open KUOS.DependentOriginationGrayC60NativeChainComplexV5_160

set_option autoImplicit false
noncomputable section

/-!
# F59-F12 / v5.161 — nonzero NATIVE Mathlib H₂ class of actual C60

F59-F8 proved the oriented 12 pentagons + 20 hexagons form a genuine
finite integral 2-cycle. F59-F9 constructed the genuine Z-linear
face-to-edge boundary d₂, a NONZERO integral 2-chain with d₂=0,
and a nontrivial kernel. F59-F10 constructed the physical d₁ and
proved d₁ ∘ d₂=0, and F59-F11 assembled these 60–90–32 free
integer modules into an actual Mathlib ChainComplex (ModuleCat ℤ) ℕ,
with degree 3 and every higher degree ZERO.

Here we use the NATIVE Mathlib HomologicalComplex/ShortComplex
HOMOLOGY API in degree two: K.homology 2, K.cycles 2,
K.homologyπ 2, and the concrete ModuleCat cycles isomorphism.

We construct the class of the ACTUAL oriented 32-face fundamental
2-chain in the native H₂ object. Its representative is a genuine
d₂-cycle and cannot be a d₃-boundary, since the incoming differential
from C₃ is genuinely zero. We PROVE this specific H₂ class is
nonzero, not merely that the kernel of d₂ is nonzero, and we prove
the native H₂ object is not zero and degree two is not exact.

Scope: nonzero H₂ CLASS and genuine homology object. This does
not assert H₂ ≅ ℤ, identify a unique generator, compute H₁/H₀,
or prove C60 homeomorphic to S². Independent F55 higher-cell
pasting and old Stage-II omega remain separately unproved.
-/

/-- The genuine incoming map C₃ → C₂ at native homology degree 2
is zero, because the original C60 CW-complex has no 3-cells. -/
theorem c60NativeH2_incoming_zero :
    (c60NativeIntegralCellularComplex.sc 2).f = 0 := by
  change c60NativeIntegralCellularComplex.d 3 2 = 0
  exact c60NativeIntegralCellularComplex_d32

/-- The outgoing map C₂ → C₁ at the actual H₂ object IS the exact
previously formally verified original oriented integer d₂. -/
theorem c60NativeH2_outgoing_eq_d2 :
    (c60NativeIntegralCellularComplex.sc 2).g =
      ModuleCat.ofHom c60IntegralBoundaryTwo := by
  change c60NativeIntegralCellularComplex.d 2 1 =
    ModuleCat.ofHom c60IntegralBoundaryTwo
  exact c60NativeIntegralCellularComplex_d21

/-- The genuine nonzero sum of all 32 original oriented C60 faces
lies in the ACTUAL native mathlib cycle submodule ker d₂. -/
theorem c60NativeH2_fundamental_mem_native_cycles :
    c60IntegralFundamentalSurfaceChain ∈
      LinearMap.ker
        (c60NativeIntegralCellularComplex.sc 2).g.hom := by
  change c60IntegralBoundaryTwo c60IntegralFundamentalSurfaceChain = 0
  exact c60IntegralBoundaryTwo_fundamental_zero

/-- The same ACTUAL fundamental surface chain is NOT a boundary
from degree three. This proof uses the truly zero native d₃ and
nonzero integral coefficient of the original surface chain, not a
merely modulo-two argument. -/
theorem c60NativeH2_fundamental_not_boundary :
    c60IntegralFundamentalSurfaceChain ∉
      LinearMap.range
        (c60NativeIntegralCellularComplex.sc 2).f.hom := by
  intro h
  obtain ⟨x, hx⟩ := h
  have hz :
      (c60NativeIntegralCellularComplex.sc 2).f.hom x = 0 := by
    rw [c60NativeH2_incoming_zero]
    rfl
  exact c60IntegralFundamentalSurfaceChain_ne_zero (hx.symm.trans hz)

/-- The native cycles object is explicitly connected to Mathlib's
kernel-submodule model, rather than replacing homology by an
independently declared integer charge. -/
def c60NativeH2FundamentalCycle :
    c60NativeIntegralCellularComplex.cycles 2 :=
  (c60NativeIntegralCellularComplex.sc 2).moduleCatCyclesIso.inv
    (⟨c60IntegralFundamentalSurfaceChain,
      c60NativeH2_fundamental_mem_native_cycles⟩ :
      LinearMap.ker
        (c60NativeIntegralCellularComplex.sc 2).g.hom)

/-- The class of the ACTUAL globally oriented original C60
fundamental surface in the NATIVE Mathlib H₂ homology object. -/
def c60NativeH2FundamentalClass :
    c60NativeIntegralCellularComplex.homology 2 :=
  (c60NativeIntegralCellularComplex.homologyπ 2)
    c60NativeH2FundamentalCycle

/-- Its representative is a genuinely NONZERO native cycle,
proved using the actual ModuleCat isomorphism between the
abstract category-theoretic cycles and the concrete ker(d₂). -/
theorem c60NativeH2FundamentalCycle_ne_zero :
    c60NativeH2FundamentalCycle ≠ 0 := by
  intro h
  have hinj :
      Function.Injective
        (c60NativeIntegralCellularComplex.sc 2).moduleCatCyclesIso.inv.hom :=
    (ModuleCat.mono_iff_injective _).mp inferInstance
  have hker :
      (⟨c60IntegralFundamentalSurfaceChain,
        c60NativeH2_fundamental_mem_native_cycles⟩ :
        LinearMap.ker (c60NativeIntegralCellularComplex.sc 2).g.hom) =
          0 := by
    apply hinj
    simpa only [c60NativeH2FundamentalCycle, map_zero] using h
  exact c60IntegralFundamentalSurfaceChain_ne_zero
    (congrArg Subtype.val hker)

/-- MOST IMPORTANT F59-F12 THEOREM: the explicitly constructed
REAL C60 fundamental 2-cycle represents a NONZERO class in the
GENUINE native Mathlib H₂ homology object. This is stronger than
F59-F9's nonzero ker d₂ statement; all genuine boundaries in
degree two are excluded by the proven zero d₃. -/
theorem c60NativeH2FundamentalClass_ne_zero :
    c60NativeH2FundamentalClass ≠ 0 := by
  haveI : IsIso (c60NativeIntegralCellularComplex.homologyπ 2) :=
    c60NativeIntegralCellularComplex.isIso_homologyπ
      3 2 (by rfl) c60NativeIntegralCellularComplex_d32
  have hinj :
      Function.Injective
        (c60NativeIntegralCellularComplex.homologyπ 2).hom :=
    (ModuleCat.mono_iff_injective _).mp inferInstance
  intro h
  apply c60NativeH2FundamentalCycle_ne_zero
  apply hinj
  simpa only [c60NativeH2FundamentalClass, map_zero] using h

/-- H₂ of the true original 60-vertex, 90-edge, 32-face C60
integral cellular chain complex is NOT THE ZERO MODULECAT OBJECT. -/
theorem c60NativeH2_not_isZero :
    ¬ IsZero (c60NativeIntegralCellularComplex.homology 2) := by
  intro hzero
  haveI : Subsingleton (c60NativeIntegralCellularComplex.homology 2) :=
    ModuleCat.isZero_iff_subsingleton.mp hzero
  exact c60NativeH2FundamentalClass_ne_zero (Subsingleton.elim _ _)

/-- Consequently the native cellular complex is NOT exact
at degree 2. This obstruction is rigorously the nontrivial
H₂ fundamental class, not the unrelated old Stage-II omega. -/
theorem c60NativeChainComplex_not_exactAt_two :
    ¬ c60NativeIntegralCellularComplex.ExactAt 2 := by
  intro hexact
  exact c60NativeH2_not_isZero
    ((c60NativeIntegralCellularComplex.exactAt_iff_isZero_homology).mp hexact)

#print axioms c60NativeH2_incoming_zero
#print axioms c60NativeH2_outgoing_eq_d2
#print axioms c60NativeH2_fundamental_mem_native_cycles
#print axioms c60NativeH2_fundamental_not_boundary
#print axioms c60NativeH2FundamentalCycle
#print axioms c60NativeH2FundamentalClass
#print axioms c60NativeH2FundamentalCycle_ne_zero
#print axioms c60NativeH2FundamentalClass_ne_zero
#print axioms c60NativeH2_not_isZero
#print axioms c60NativeChainComplex_not_exactAt_two

end
end KUOS.DependentOriginationGrayC60NativeH2FundamentalClassV5_161
