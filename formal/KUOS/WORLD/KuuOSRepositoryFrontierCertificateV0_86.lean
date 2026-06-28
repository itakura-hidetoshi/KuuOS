import KUOS.WORLD.KuuOSRepositoryRevisionDagV0_85

namespace KUOS.WORLD.KuuOSRepositoryFrontierCertificateV0_86

open KUOS.WORLD.KuuOSRepositoryRevisionDagV0_85


def ForwardEdge
    {Revision : Type*}
    [DecidableEq Revision]
    (dag : RankedRevisionDag Revision)
    (parent child : Revision) : Prop :=
  parent ∈ dag.parents child


structure RevisionFrontier
    {Revision : Type*}
    [DecidableEq Revision]
    (dag : RankedRevisionDag Revision) where
  tips : Finset Revision
  tipsSubset : tips ⊆ dag.nodes
  terminal : ∀ {tip child},
    tip ∈ tips → child ∈ dag.nodes → tip ∉ dag.parents child
  covers : ∀ {revision},
    revision ∈ dag.nodes →
      ∃ tip, tip ∈ tips ∧
        Relation.ReflTransGen (ForwardEdge dag) revision tip
  exactTerminal : ∀ {revision},
    revision ∈ dag.nodes →
      (revision ∈ tips ↔
        ∀ {child}, child ∈ dag.nodes → revision ∉ dag.parents child)


structure FrontierWitness where
  sourceDagBound : Prop
  sourceEdgesBound : Prop
  exactTerminalFrontier : Prop
  frontierNonempty : Prop
  frontierAntichain : Prop
  allNodesFrontierCovered : Prop
  mergedAncestorsExcluded : Prop
  normalFormPreserved : Prop


structure FrontierWitness.Valid (witness : FrontierWitness) : Prop where
  sourceDagBound : witness.sourceDagBound
  sourceEdgesBound : witness.sourceEdgesBound
  exactTerminalFrontier : witness.exactTerminalFrontier
  frontierNonempty : witness.frontierNonempty
  frontierAntichain : witness.frontierAntichain
  allNodesFrontierCovered : witness.allNodesFrontierCovered
  mergedAncestorsExcluded : witness.mergedAncestorsExcluded
  normalFormPreserved : witness.normalFormPreserved


theorem frontier_nonempty
    {Revision : Type*}
    [DecidableEq Revision]
    (dag : RankedRevisionDag Revision)
    (frontier : RevisionFrontier dag) :
    frontier.tips.Nonempty := by
  rcases frontier.covers dag.rootMem with ⟨tip, hTip, _⟩
  exact ⟨tip, hTip⟩


theorem frontier_card_le_node_card
    {Revision : Type*}
    [DecidableEq Revision]
    (dag : RankedRevisionDag Revision)
    (frontier : RevisionFrontier dag) :
    frontier.tips.card ≤ dag.nodes.card := by
  exact Finset.card_le_card frontier.tipsSubset


theorem parent_revision_not_in_frontier
    {Revision : Type*}
    [DecidableEq Revision]
    (dag : RankedRevisionDag Revision)
    (frontier : RevisionFrontier dag)
    {parent child : Revision}
    (hChild : child ∈ dag.nodes)
    (hParent : parent ∈ dag.parents child) :
    parent ∉ frontier.tips := by
  intro hParentTip
  exact frontier.terminal hParentTip hChild hParent


theorem distinct_frontier_tips_are_not_directly_comparable
    {Revision : Type*}
    [DecidableEq Revision]
    (dag : RankedRevisionDag Revision)
    (frontier : RevisionFrontier dag)
    {first second : Revision}
    (hFirst : first ∈ frontier.tips)
    (hSecond : second ∈ frontier.tips) :
    first ∉ dag.parents second ∧ second ∉ dag.parents first := by
  constructor
  · exact frontier.terminal hFirst (frontier.tipsSubset hSecond)
  · exact frontier.terminal hSecond (frontier.tipsSubset hFirst)


theorem exact_terminal_membership
    {Revision : Type*}
    [DecidableEq Revision]
    (dag : RankedRevisionDag Revision)
    (frontier : RevisionFrontier dag)
    {revision : Revision}
    (hRevision : revision ∈ dag.nodes) :
    revision ∈ frontier.tips ↔
      ∀ {child}, child ∈ dag.nodes → revision ∉ dag.parents child := by
  exact frontier.exactTerminal hRevision


theorem valid_frontier_certificate
    (witness : FrontierWitness)
    (h : witness.Valid) :
    witness.sourceDagBound ∧
      witness.sourceEdgesBound ∧
      witness.exactTerminalFrontier ∧
      witness.frontierNonempty ∧
      witness.frontierAntichain ∧
      witness.allNodesFrontierCovered ∧
      witness.mergedAncestorsExcluded ∧
      witness.normalFormPreserved := by
  exact ⟨h.sourceDagBound, h.sourceEdgesBound,
    h.exactTerminalFrontier, h.frontierNonempty,
    h.frontierAntichain, h.allNodesFrontierCovered,
    h.mergedAncestorsExcluded, h.normalFormPreserved⟩

end KUOS.WORLD.KuuOSRepositoryFrontierCertificateV0_86
