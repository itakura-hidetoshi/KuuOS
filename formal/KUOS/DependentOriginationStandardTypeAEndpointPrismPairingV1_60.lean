import KUOS.DependentOriginationStandardABCLeibnizCellularComparisonV1_59
import Mathlib.AlgebraicTopology.SimplicialSet.AnodyneExtensions.RelativeCellComplex
import Mathlib.AlgebraicTopology.SimplicialSet.AnodyneExtensions.RankNat
import Mathlib.AlgebraicTopology.SimplicialSet.ProdStdSimplexOne
import Mathlib.AlgebraicTopology.SimplicialSet.Boundary

namespace KUOS.DependentOriginationStandardTypeAEndpointPrismPairingV1_60

open CategoryTheory
open CategoryTheory.Category
open MonoidalCategory
open Opposite
open Simplicial
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationScaledHornAttachmentLiftingV1_40
open KUOS.DependentOriginationScaledTerminalRLPV1_41
open KUOS.DependentOriginationScaledAnodyneAttachmentFactorizationV1_48
open KUOS.DependentOriginationStandardTypeAScaledHornFamilyV1_49
open KUOS.DependentOriginationStandardTypeAEndpointPushoutProductV1_50
open KUOS.DependentOriginationStandardTypeAScaledPushoutSourceEnrichmentV1_53
open KUOS.DependentOriginationStandardTypeAScaledLeibnizPushoutV1_55
open KUOS.DependentOriginationStandardABCLeibnizCellularComparisonV1_59

universe u

/-!
# Standard type-(A) endpoint prism pairing v1.60

The endpoint Leibniz inclusion is not attacked by attaching the staircase top
simplices one by one.  We first factor its underlying prism inclusion through
the full interval-boundary union

```text
A_epsilon
  = (Lambda_i^n x Delta[1]) union (Delta[n] x {epsilon})
       |
       v
A_boundary
  = (Lambda_i^n x Delta[1]) union (Delta[n] x boundary Delta[1])
       |
       v
Delta[n] x Delta[1].
```

This factorization has two advantages.

* `A_epsilon -> A_boundary` is the single missing endpoint copy of the same
  standard type-(A) horn attachment.
* `A_boundary -> Delta[n] x Delta[1]` is exactly the ordinary geometry to
  which Mathlib's `Subcomplex.PairingCore` / rank / relative-cell-complex
  infrastructure applies: a complementary simplex is a strictly monotone walk
  whose interval coordinate is surjective and whose simplex coordinate meets
  every vertex except possibly the distinguished horn vertex.

The present file fixes this factorization at the scaled level using pullback
scaling from the already canonical cylinder.  Subsequent sections build the
proper regular pairing on `A_boundary`, classify its cells by the standard
A/B/C presentation, and exit through
`StandardABCTypeAEndpointLeibnizCellularCertificate`.

No newer Mathlib scaled/anodyne API is imported: all imports above exist at the
repository's pinned Mathlib revision.
-/

/-! ## The interval endpoint lies in the interval boundary -/

/-- Every endpoint vertex of `Delta[1]` lies in `boundary Delta[1]`. -/
theorem intervalEndpoint_le_boundary (epsilon : Fin 2) :
    (intervalEndpoint epsilon : (Δ[1] : SSet.{u}).Subcomplex) <=
      (∂Δ[1] : (Δ[1] : SSet.{u}).Subcomplex) := by
  refine (SSet.Subcomplex.ofSimplex_le_iff
    (SSet.stdSimplex.obj₀Equiv.{u}.symm epsilon)
    (∂Δ[1] : (Δ[1] : SSet.{u}).Subcomplex)).2 ?_
  rw [SSet.boundary_obj_eq_univ 0 1 (by omega)]
  exact Set.mem_univ _

/-! ## Factor the endpoint prism through the full boundary prism -/

/-- The ordinary intermediate prism subcomplex
`(Lambda_i^n x Delta[1]) union (Delta[n] x boundary Delta[1])`. -/
def standardTypeABoundaryPrismSubcomplex
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    ((Δ[g.n] : SSet.{u}) ⊗ Δ[1]).Subcomplex :=
  (SSet.horn g.n g.i).unionProd (∂Δ[1])

/-- The endpoint union-product subcomplex is contained in the full-boundary
union-product subcomplex. -/
theorem standardTypeAEndpointPrism_le_boundaryPrism
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    (SSet.horn g.n g.i).unionProd (intervalEndpoint g.endpoint) <=
      standardTypeABoundaryPrismSubcomplex g := by
  dsimp [standardTypeABoundaryPrismSubcomplex, SSet.Subcomplex.unionProd]
  apply sup_le_sup
  · exact SSet.Subcomplex.prod_monotone (by rfl)
      (intervalEndpoint_le_boundary g.endpoint)
  · rfl

/-- Underlying simplicial inclusion from the endpoint prism source to the
boundary-prism source. -/
def standardTypeAEndpointToBoundaryPrismMap
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    ((SSet.horn g.n g.i).unionProd
        (intervalEndpoint g.endpoint) : SSet.{u}) ⟶
      (standardTypeABoundaryPrismSubcomplex g : SSet.{u}) :=
  SSet.Subcomplex.homOfLE
    (standardTypeAEndpointPrism_le_boundaryPrism g)

@[reassoc]
theorem standardTypeAEndpointToBoundaryPrismMap_ι
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    standardTypeAEndpointToBoundaryPrismMap g ≫
        (standardTypeABoundaryPrismSubcomplex g).ι =
      ((SSet.horn g.n g.i).unionProd
        (intervalEndpoint g.endpoint)).ι := by
  exact SSet.Subcomplex.homOfLE_ι
    (standardTypeAEndpointPrism_le_boundaryPrism g)

/-! ## Pull the canonical cylinder scaling back to the boundary prism -/

/-- The intermediate boundary prism carries exactly the pullback of the
canonical standard type-(A) cylinder scaling. -/
def standardTypeABoundaryPrismScaling
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    ScaledSimplicialSet
      (standardTypeABoundaryPrismSubcomplex g : SSet.{u}) :=
  pullbackScaling
    (scaledSimplexCylinder (standardTypeASimplexScaling g.i)).scaling
    (standardTypeABoundaryPrismSubcomplex g).ι

/-- The scaled intermediate boundary-prism object. -/
def standardTypeABoundaryPrism
    (g : StandardTypeAHornAttachmentGeneratorIndex) : ScaledSSet.{u} :=
  ScaledSSet.of
    (standardTypeABoundaryPrismSubcomplex g : SSet.{u})
    (standardTypeABoundaryPrismScaling g)

/-- The boundary-prism inclusion into the full scaled cylinder is scaled by
construction. -/
def standardTypeABoundaryPrismToCylinder
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    standardTypeABoundaryPrism g ⟶
      scaledSimplexCylinder (standardTypeASimplexScaling g.i) where
  map := (standardTypeABoundaryPrismSubcomplex g).ι
  scaled := pullbackScaling_map _ _

/-- The least-generated endpoint Leibniz source maps canonically to the
boundary prism.  Scaledness is inherited from the already-proved genuine
scaled Leibniz map into the cylinder and the defining pullback scaling on the
intermediate object. -/
def standardTypeAEndpointToBoundaryPrism
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    standardTypeAEndpointGeneratedPushoutSource g ⟶
      standardTypeABoundaryPrism g where
  map := standardTypeAEndpointToBoundaryPrismMap g
  scaled := by
    intro t ht
    change
      (scaledSimplexCylinder
        (standardTypeASimplexScaling g.i)).scaling.thin
        ((standardTypeABoundaryPrismSubcomplex g).ι.app (op ⦋2⦌)
          ((standardTypeAEndpointToBoundaryPrismMap g).app (op ⦋2⦌) t))
    rw [← NatTrans.comp_app_apply]
    rw [standardTypeAEndpointToBoundaryPrismMap_ι]
    rw [← standardTypeAEndpointScaledLeibnizPushoutProductHom_map g]
    exact (standardTypeAEndpointScaledLeibnizPushoutProductHom g).scaled t ht

/-- The genuine scaled endpoint Leibniz map factors exactly through the
boundary prism. -/
theorem standardTypeAEndpointLeibniz_factor_boundaryPrism
    (g : StandardTypeAHornAttachmentGeneratorIndex) :
    standardTypeAEndpointToBoundaryPrism g ≫
        standardTypeABoundaryPrismToCylinder g =
      standardTypeAEndpointScaledLeibnizPushoutProductHom g := by
  apply ScaledSSet.ScaledMap.ext
  change
    standardTypeAEndpointToBoundaryPrismMap g ≫
        (standardTypeABoundaryPrismSubcomplex g).ι =
      (standardTypeAEndpointScaledLeibnizPushoutProductHom g).map
  rw [standardTypeAEndpointToBoundaryPrismMap_ι,
    standardTypeAEndpointScaledLeibnizPushoutProductHom_map]

/-! ## Complement as monotone-walk data -/

/-- A simplex lies outside the boundary prism exactly when neither coordinate
lies in the corresponding union-product leg. -/
theorem standardTypeABoundaryPrism_notMem_iff
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    {d : SimplexCategoryᵒᵖ}
    (z : ((Δ[g.n] : SSet.{u}) ⊗ Δ[1]).obj d) :
    z ∉ (standardTypeABoundaryPrismSubcomplex g).obj d ↔
      z.1 ∉ (SSet.horn g.n g.i).obj d ∧
        z.2 ∉ (∂Δ[1] : (Δ[1] : SSet.{u}).Subcomplex).obj d := by
  have hmem :
      z ∈ ((SSet.horn g.n g.i).unionProd
          (∂Δ[1] : (Δ[1] : SSet.{u}).Subcomplex)).obj d ↔
        z.2 ∈ (∂Δ[1] : (Δ[1] : SSet.{u}).Subcomplex).obj d ∨
          z.1 ∈ (SSet.horn g.n g.i).obj d :=
    SSet.Subcomplex.mem_unionProd_iff
      (SSet.horn g.n g.i)
      (∂Δ[1] : (Δ[1] : SSet.{u}).Subcomplex) z
  change
    z ∉ ((SSet.horn g.n g.i).unionProd
        (∂Δ[1] : (Δ[1] : SSet.{u}).Subcomplex)).obj d ↔ _
  constructor
  · intro hz
    constructor
    · intro hs
      apply hz
      exact hmem.mpr (Or.inr hs)
    · intro ht
      apply hz
      exact hmem.mpr (Or.inl ht)
  · rintro ⟨hs, ht⟩ hz
    rcases hmem.mp hz with h | h
    · exact ht h
    · exact hs h

/-- Equivalently, outside the boundary prism the simplex-coordinate range,
together with the distinguished horn vertex, is all of `Fin (n+1)`, while the
interval coordinate is surjective.  This is the exact walk condition consumed
by the pairing construction. -/
theorem standardTypeABoundaryPrism_notMem_iff_ranges
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    {d : SimplexCategoryᵒᵖ}
    (z : ((Δ[g.n] : SSet.{u}) ⊗ Δ[1]).obj d) :
    z ∉ (standardTypeABoundaryPrismSubcomplex g).obj d ↔
      Set.range (SSet.stdSimplex.asOrderHom z.1) ∪ {g.i} = Set.univ ∧
        Function.Surjective (SSet.stdSimplex.asOrderHom z.2) := by
  rw [standardTypeABoundaryPrism_notMem_iff]
  change
    ¬ (Set.range (SSet.stdSimplex.asOrderHom z.1) ∪ {g.i} ≠ Set.univ) ∧
        ¬ (¬ Function.Surjective (SSet.stdSimplex.asOrderHom z.2)) ↔ _
  simp

/-- Nondegenerate prism simplices are precisely strictly monotone walks in the
product poset.  We keep this theorem at the v1.60 namespace boundary so the
scaled cell classification below does not need to unfold simplicial
nondegeneracy. -/
theorem standardTypeAPrism_nonDegenerate_iff_strictMono
    (g : StandardTypeAHornAttachmentGeneratorIndex)
    {d : Nat}
    (z : ((Δ[g.n] : SSet.{u}) ⊗ Δ[1]) _⦋d⦌) :
    z ∈ ((Δ[g.n] : SSet.{u}) ⊗ Δ[1]).nonDegenerate d ↔
      StrictMono (SSet.prodStdSimplex.objEquiv z) :=
  SSet.prodStdSimplex.nonDegenerate_iff_strictMono_objEquiv z

/-!
At this point the endpoint geometry has been reduced without any model-
structure assertion to

```text
A_epsilon --(one opposite-endpoint type-A cell)--> A_boundary
A_boundary --(proper regular prism pairing)-----> Delta[n] x Delta[1].
```

The next section constructs that pairing using the pinned `PairingCore`, then
uses the pinned `RankFunction.relativeCellComplex` theorem to obtain the actual
coproduct/pushout/transfinite filtration.  Only after that ordinary filtration
is fixed do we classify the induced scalings into standard type-(A) cells and
the low-dimensional type-(B) completion cases required by the distinguished
thin triangle.  Type-(C) is not assumed in advance.
-/

end KUOS.DependentOriginationStandardTypeAEndpointPrismPairingV1_60
