import Mathlib
import KUOS.WORLD.NoncommutativeOperatorAlgebraModuleV0_29

/-!
Kū–Indra WORLD C⋆-operator-algebra and local-net bridge v0.30.

The v0.29 real algebraic observable layer is embedded densely and faithfully into
an abstract complex C⋆-algebra. The same WORLD regions index local star
subalgebras. Isotony survives norm closure, while algebraic locality is retained
as an explicit commuting condition for spacelike regions.
-/

namespace KUOS
namespace WORLD

structure WorldCStarLocalNetBridge
    (C : RealHilbertL2Carrier)
    (W : WorldNoncommutativeOperatorAlgebra C) where
  A : Type
  [cstarAlgebra : CStarAlgebra A]
  [regionPartialOrder : PartialOrder W.Region]
  algebraicEmbedding : W.global.A →+* A
  embeddingInjective : Function.Injective algebraicEmbedding
  embeddingDense : DenseRange algebraicEmbedding
  localAlgebra : W.Region → StarSubalgebra ℂ A
  isotony : ∀ {i j : W.Region}, i ≤ j → localAlgebra i ≤ localAlgebra j
  sourceLocalIncluded : ∀ (i : W.Region) (x : W.localObservable i),
    algebraicEmbedding (x : W.global.A) ∈ localAlgebra i
  spacelike : W.Region → W.Region → Prop
  spacelikeSymmetric : Symmetric spacelike
  locality : ∀ {i j : W.Region}, spacelike i j →
    ∀ (a : localAlgebra i) (b : localAlgebra j), Commute (a : A) (b : A)
  background : StarSubalgebra ℂ A
  action : StarSubalgebra ℂ A
  sourceBackgroundIncluded : ∀ x : W.background,
    algebraicEmbedding (x : W.global.A) ∈ background
  sourceActionIncluded : ∀ x : W.action,
    algebraicEmbedding (x : W.global.A) ∈ action
  worldNotIdentifiedWithCStarCarrier : Prop
  worldNotIdentifiedProof : worldNotIdentifiedWithCStarCarrier
  localNetReadOnlyAnalyticSidecar : Prop
  localNetReadOnlyProof : localNetReadOnlyAnalyticSidecar
  multiWorldNoncollapsePreserved : Prop
  multiWorldNoncollapseProof : multiWorldNoncollapsePreserved
  twoTruthsGapPreserved : Prop
  twoTruthsGapProof : twoTruthsGapPreserved

attribute [instance] WorldCStarLocalNetBridge.cstarAlgebra
attribute [instance] WorldCStarLocalNetBridge.regionPartialOrder

namespace WorldCStarLocalNetBridge

variable {C : RealHilbertL2Carrier}
variable {W : WorldNoncommutativeOperatorAlgebra C}
variable (B : WorldCStarLocalNetBridge C W)

theorem cstar_identity (x : B.A) :
    ‖star x * x‖ = ‖x‖ * ‖x‖ :=
  CStarRing.norm_star_mul_self

theorem completion_embedding_dense :
    DenseRange B.algebraicEmbedding :=
  B.embeddingDense

theorem embedded_noncommuting :
    ∃ a b : W.global.A,
      B.algebraicEmbedding a * B.algebraicEmbedding b ≠
        B.algebraicEmbedding b * B.algebraicEmbedding a := by
  rcases W.global.noncommutingWitness with ⟨a, b, hab⟩
  refine ⟨a, b, ?_⟩
  intro h
  apply hab
  apply B.embeddingInjective
  calc
    B.algebraicEmbedding (a * b) =
        B.algebraicEmbedding a * B.algebraicEmbedding b := by
          rw [map_mul]
    _ = B.algebraicEmbedding b * B.algebraicEmbedding a := h
    _ = B.algebraicEmbedding (b * a) := by
          rw [map_mul]

theorem local_isotony {i j : W.Region} (h : i ≤ j) :
    B.localAlgebra i ≤ B.localAlgebra j :=
  B.isotony h

def closedLocal (i : W.Region) : StarSubalgebra ℂ B.A :=
  (B.localAlgebra i).topologicalClosure

theorem local_le_closedLocal (i : W.Region) :
    B.localAlgebra i ≤ B.closedLocal i :=
  StarSubalgebra.le_topologicalClosure _

theorem closedLocal_isotony {i j : W.Region} (h : i ≤ j) :
    B.closedLocal i ≤ B.closedLocal j :=
  StarSubalgebra.topologicalClosure_mono (B.isotony h)

theorem closedLocal_isClosed (i : W.Region) :
    IsClosed (B.closedLocal i : Set B.A) := by
  simpa [closedLocal] using
    StarSubalgebra.isClosed_topologicalClosure (B.localAlgebra i)

theorem source_local_mem_closedLocal
    (i : W.Region) (x : W.localObservable i) :
    B.algebraicEmbedding (x : W.global.A) ∈ B.closedLocal i :=
  B.local_le_closedLocal i (B.sourceLocalIncluded i x)

theorem spacelike_symmetric {i j : W.Region} (h : B.spacelike i j) :
    B.spacelike j i :=
  B.spacelikeSymmetric h

theorem local_observables_commute
    {i j : W.Region}
    (h : B.spacelike i j)
    (a : B.localAlgebra i)
    (b : B.localAlgebra j) :
    Commute (a : B.A) (b : B.A) :=
  B.locality h a b

theorem source_background_mem (x : W.background) :
    B.algebraicEmbedding (x : W.global.A) ∈ B.background :=
  B.sourceBackgroundIncluded x

theorem source_action_mem (x : W.action) :
    B.algebraicEmbedding (x : W.global.A) ∈ B.action :=
  B.sourceActionIncluded x

theorem representation_boundary_preserved :
    B.worldNotIdentifiedWithCStarCarrier ∧
    B.localNetReadOnlyAnalyticSidecar ∧
    B.multiWorldNoncollapsePreserved ∧
    B.twoTruthsGapPreserved :=
  ⟨B.worldNotIdentifiedProof, B.localNetReadOnlyProof,
    B.multiWorldNoncollapseProof, B.twoTruthsGapProof⟩

end WorldCStarLocalNetBridge
end WORLD
end KUOS
