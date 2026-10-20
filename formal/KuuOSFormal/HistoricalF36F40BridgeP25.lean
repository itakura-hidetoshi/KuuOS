import KuuOSFormal.HistoricalF36F40BridgeP24

/-!
# F112-P25 — explicit native integral zero-chain contraction and augmentation

P23 constructs the actual independent Kuu Dart/Edge/Polygon free integer
cellular complex. P24 constructs a true native degree-one contraction,
proving every closed one-chain is a boundary. Here we reconstruct the
complementary ZERO-DEGREE chain homotopy from certified old F59
physical root-to-vertex paths, transported using the constructor-wise
independent Dart/Edge equivalences, with no numerical Fin proxies.

The genuine native maps P₀ : C₀ᴺ → C₁ᴺ, ε : C₀ᴺ → ℤ and
ι : ℤ → C₀ᴺ obey d₁ᴺ P₀ + ι ε = id, ε d₁ᴺ = 0 and ε ι = id.
Consequently ker ε = im d₁ᴺ, and the genuine north-dart class is
nonzero modulo physical one-boundaries. Alongside P24, this is the
explicit integral reduced cellular contraction in degrees zero and one.

Neither the original F47/F55 proof-relevant 3-source nor odd braided
exchange is inferred from the integer homology. The F68/F77 descent
obstructions remain separate.
-/

namespace KUOS.F112ActualHistoricalF36F40BridgeP4
namespace GenuineOriginalC60Geometry

open CategoryTheory Limits
open Kuu.F112.Physical
open KUOS.DependentOriginationGrayC60IntegralBoundaryLinearMapV5_159
open KUOS.DependentOriginationGrayC60IntegralChainComplexV5_160
open KUOS.DependentOriginationGrayC60NativeH0AugmentationV5_162
open KUOS.DependentOriginationGrayC60NativeH0ConnectivityV5_163

set_option autoImplicit false
set_option warningAsError true
noncomputable section

/-- A physical native north-dart anchor, constructor-wise inverse
to the original certified F59 north dart. -/
def p25NativeNorthDart : Dart := dartEquiv.symm c60NorthDart

/-- Linear inclusion of the integer north-vertex charge, taking
values in the genuine native free abelian group on sixty darts. -/
def p25NativeRootEmbedding : ℤ →ₗ[ℤ] p23NativeZeroChains :=
  p23NativeZeroToHistorical.symm.toLinearMap.comp c60RootEmbedding

/-- A true signed native physical edge path from the north dart
to every native dart, extended Z-linearly to ALL zero-chains. -/
def p25NativeVertexPathLift :
    p23NativeZeroChains →ₗ[ℤ] p23NativeOneChains :=
  p23NativeOneToHistorical.symm.toLinearMap.comp
    (c60VertexPathLift.comp p23NativeZeroToHistorical.toLinearMap)

/-- Every native root chain is sent to the EXACT historical root
chain under the already-certified constructor-wise dart transport. -/
theorem p25NativeRootEmbedding_transport (z : ℤ) :
    p23NativeZeroToHistorical (p25NativeRootEmbedding z) =
      c60RootEmbedding z := by
  change p23NativeZeroToHistorical
    (p23NativeZeroToHistorical.symm (c60RootEmbedding z)) =
      c60RootEmbedding z
  exact p23NativeZeroToHistorical.apply_symm_apply _

/-- Root embedding has precisely the north physical dart coordinate,
not an arbitrary distinguished finite index. -/
theorem p25NativeRootEmbedding_single (z : ℤ) :
    p25NativeRootEmbedding z =
      Finsupp.single p25NativeNorthDart z := by
  apply p23NativeZeroToHistorical.injective
  rw [p25NativeRootEmbedding_transport]
  change c60RootEmbedding z =
    (Finsupp.domLCongr dartEquiv)
      (Finsupp.single p25NativeNorthDart z)
  rw [c60RootEmbedding_apply, Finsupp.domLCongr_single]
  change Finsupp.single c60NorthDart z =
    Finsupp.single (dartEquiv (dartEquiv.symm c60NorthDart)) z
  rw [Equiv.apply_symm_apply]

/-- The native path-lift agrees with the actual historical
spanning path after transport on EVERY native signed zero-chain. -/
theorem p25NativeVertexPathLift_transport (x : p23NativeZeroChains) :
    p23NativeOneToHistorical (p25NativeVertexPathLift x) =
      c60VertexPathLift (p23NativeZeroToHistorical x) := by
  change p23NativeOneToHistorical
    (p23NativeOneToHistorical.symm
      (c60VertexPathLift (p23NativeZeroToHistorical x))) =
        c60VertexPathLift (p23NativeZeroToHistorical x)
  exact p23NativeOneToHistorical.apply_symm_apply _

/-- Native augmentation detects each original physical north-root
integer coordinate: ε ι = id, not merely an abstract H₀ ≅ ℤ. -/
theorem p25NativeRootEmbedding_augmentation (z : ℤ) :
    p24NativeVertexAugmentation (p25NativeRootEmbedding z) = z := by
  change c60IntegralVertexAugmentation
    (p23NativeZeroToHistorical (p25NativeRootEmbedding z)) = z
  rw [p25NativeRootEmbedding_transport, c60RootEmbedding_apply,
    c60IntegralVertexAugmentation_single]

theorem p25NativeRootAugmentation_retract :
    p24NativeVertexAugmentation.comp p25NativeRootEmbedding =
      LinearMap.id := by
  apply LinearMap.ext
  intro z
  change p24NativeVertexAugmentation (p25NativeRootEmbedding z) = z
  exact p25NativeRootEmbedding_augmentation z

/-- F112-P25 central identity: a *genuine native integer chain homotopy*
d₁ᴺ·P₀ᴺ + ιᴺ·εᴺ = id on ALL sixty physical Dart basis coordinates,
obtained by preserving the original certified 59-edge root paths. -/
theorem p25NativeZeroContractingIdentity :
    p23NativeBoundaryOne.comp p25NativeVertexPathLift +
      p25NativeRootEmbedding.comp p24NativeVertexAugmentation =
        LinearMap.id := by
  apply LinearMap.ext
  intro x
  apply p23NativeZeroToHistorical.injective
  change p23NativeZeroToHistorical
    (p23NativeBoundaryOne (p25NativeVertexPathLift x) +
      p25NativeRootEmbedding (p24NativeVertexAugmentation x)) =
    p23NativeZeroToHistorical x
  rw [map_add, p24NativeBoundaryOne_transport,
    p25NativeVertexPathLift_transport, p25NativeRootEmbedding_transport]
  change c60IntegralBoundaryOne (c60VertexPathLift
      (p23NativeZeroToHistorical x)) +
    c60RootEmbedding (c60IntegralVertexAugmentation
      (p23NativeZeroToHistorical x)) =
    p23NativeZeroToHistorical x
  have h := LinearMap.congr_fun c60VertexPathLift_homotopy
    (p23NativeZeroToHistorical x)
  simpa only [LinearMap.add_apply, LinearMap.comp_apply,
    LinearMap.id_apply] using h

/-- Every native augmentation-zero zero-chain has an explicit
native integer edge path whose boundary equals the chain. -/
theorem p25NativeZeroAugmentationKernel_explicit_path
    (x : p23NativeZeroChains)
    (hx : x ∈ LinearMap.ker p24NativeVertexAugmentation) :
    p23NativeBoundaryOne (p25NativeVertexPathLift x) = x := by
  have h := LinearMap.congr_fun p25NativeZeroContractingIdentity x
  have hz : p24NativeVertexAugmentation x = 0 := hx
  simp only [LinearMap.add_apply, LinearMap.comp_apply,
    LinearMap.id_apply] at h
  rw [hz, map_zero, add_zero] at h
  exact h

/-- Exact native degree-zero conservation: zero total integer
vertex charge is equivalent to being a genuine native edge boundary. -/
theorem p25NativeAugmentation_kernel_eq_boundaryOne_range :
    LinearMap.ker p24NativeVertexAugmentation =
      LinearMap.range p23NativeBoundaryOne := by
  apply le_antisymm
  · intro x hx
    exact ⟨p25NativeVertexPathLift x,
      p25NativeZeroAugmentationKernel_explicit_path x hx⟩
  · intro x hx
    rcases hx with ⟨y, rfl⟩
    change p24NativeVertexAugmentation (p23NativeBoundaryOne y) = 0
    have h := LinearMap.congr_fun
      p24NativeVertexAugmentation_comp_boundaryOne_zero y
    simpa only [LinearMap.comp_apply, LinearMap.zero_apply] using h

/-- The actual north physical dart with +1 integer coefficient is
NOT a boundary: the nontrivial native H₀ generator is geometrically
located, rather than obtained only from an abstract rank identity. -/
theorem p25NativeNorthRoot_not_boundary :
    p25NativeRootEmbedding (1 : ℤ) ∉
      LinearMap.range p23NativeBoundaryOne := by
  intro h
  have hker :
      p25NativeRootEmbedding (1 : ℤ) ∈
        LinearMap.ker p24NativeVertexAugmentation := by
    rw [p25NativeAugmentation_kernel_eq_boundaryOne_range]
    exact h
  have hz :
      p24NativeVertexAugmentation (p25NativeRootEmbedding (1 : ℤ)) = 0 :=
    hker
  rw [p25NativeRootEmbedding_augmentation] at hz
  norm_num at hz

/-- The native augmentation is onto every integer, using the
concrete north-dart physical basis rather than arbitrary choice. -/
theorem p25NativeVertexAugmentation_surjective :
    Function.Surjective p24NativeVertexAugmentation := by
  intro z
  exact ⟨p25NativeRootEmbedding z,
    p25NativeRootEmbedding_augmentation z⟩

#print axioms p25NativeRootEmbedding_single
#print axioms p25NativeVertexPathLift_transport
#print axioms p25NativeRootEmbedding_augmentation
#print axioms p25NativeRootAugmentation_retract
#print axioms p25NativeZeroContractingIdentity
#print axioms p25NativeZeroAugmentationKernel_explicit_path
#print axioms p25NativeAugmentation_kernel_eq_boundaryOne_range
#print axioms p25NativeNorthRoot_not_boundary
#print axioms p25NativeVertexAugmentation_surjective

end
end GenuineOriginalC60Geometry
end KUOS.F112ActualHistoricalF36F40BridgeP4
