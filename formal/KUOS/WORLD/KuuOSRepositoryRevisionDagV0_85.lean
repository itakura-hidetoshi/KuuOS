import Mathlib

namespace KUOS.WORLD.KuuOSRepositoryRevisionDagV0_85

structure RankedRevisionDag (Revision : Type*) [DecidableEq Revision] where
  nodes : Finset Revision
  root : Revision
  parents : Revision → Finset Revision
  rank : Revision → Nat
  rootMem : root ∈ nodes
  parentClosed : ∀ {child parent},
    child ∈ nodes → parent ∈ parents child → parent ∈ nodes
  rootParentless : parents root = ∅
  parentRankStrict : ∀ {child parent},
    child ∈ nodes → parent ∈ parents child → rank parent < rank child

structure RevisionDagWitness where
  sourceCertificatesBound : Prop
  sourceReferenceClosed : Prop
  finiteNodeBound : Prop
  finiteEdgeBound : Prop
  singleRoot : Prop
  parentArityValid : Prop
  allNodesReachable : Prop
  acyclic : Prop
  normalFormPreserved : Prop

structure RevisionDagWitness.Valid (witness : RevisionDagWitness) : Prop where
  sourceCertificatesBound : witness.sourceCertificatesBound
  sourceReferenceClosed : witness.sourceReferenceClosed
  finiteNodeBound : witness.finiteNodeBound
  finiteEdgeBound : witness.finiteEdgeBound
  singleRoot : witness.singleRoot
  parentArityValid : witness.parentArityValid
  allNodesReachable : witness.allNodesReachable
  acyclic : witness.acyclic
  normalFormPreserved : witness.normalFormPreserved

theorem no_revision_is_its_own_parent
    {Revision : Type*}
    [DecidableEq Revision]
    (dag : RankedRevisionDag Revision)
    {revision : Revision}
    (hRevision : revision ∈ dag.nodes) :
    revision ∉ dag.parents revision := by
  intro hParent
  have hStrict := dag.parentRankStrict hRevision hParent
  exact (Nat.lt_irrefl (dag.rank revision)) hStrict

theorem opposite_parent_edges_are_impossible
    {Revision : Type*}
    [DecidableEq Revision]
    (dag : RankedRevisionDag Revision)
    {first second : Revision}
    (hFirst : first ∈ dag.nodes)
    (hSecond : second ∈ dag.nodes)
    (hFirstParent : first ∈ dag.parents second) :
    second ∉ dag.parents first := by
  intro hSecondParent
  have hForward := dag.parentRankStrict hSecond hFirstParent
  have hBackward := dag.parentRankStrict hFirst hSecondParent
  exact (Nat.lt_asymm hForward hBackward)

theorem valid_revision_dag_certificate
    (witness : RevisionDagWitness)
    (h : witness.Valid) :
    witness.sourceCertificatesBound ∧
      witness.sourceReferenceClosed ∧
      witness.finiteNodeBound ∧
      witness.finiteEdgeBound ∧
      witness.singleRoot ∧
      witness.parentArityValid ∧
      witness.allNodesReachable ∧
      witness.acyclic ∧
      witness.normalFormPreserved := by
  exact ⟨h.sourceCertificatesBound, h.sourceReferenceClosed,
    h.finiteNodeBound, h.finiteEdgeBound, h.singleRoot,
    h.parentArityValid, h.allNodesReachable, h.acyclic,
    h.normalFormPreserved⟩

end KUOS.WORLD.KuuOSRepositoryRevisionDagV0_85
