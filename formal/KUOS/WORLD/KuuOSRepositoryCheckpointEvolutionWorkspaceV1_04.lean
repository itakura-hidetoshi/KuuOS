import KUOS.WORLD.KuuOSRepositoryCheckpointCreationReceiptV1_03

namespace KUOS.WORLD.KuuOSRepositoryCheckpointEvolutionWorkspaceV1_04

structure WorkspaceSeed where
  checkpointOID : String
  treeDigest : String
  deriving DecidableEq

structure WorkspaceState where
  seed : WorkspaceSeed
  workspaceId : String
  sequence : Nat
  treeDigest : String
  candidateId : String
  deriving DecidableEq

structure WorkspaceTransition where
  source : WorkspaceState
  final : WorkspaceState
  committed : Bool
  sourcePreservedOnAbort : committed = false → final = source
  sequenceAdvancedOnCommit :
    committed = true → final.sequence = source.sequence + 1
  seedPreserved : final.seed = source.seed

structure WorkspaceReset where
  source : WorkspaceState
  seed : WorkspaceSeed
  final : WorkspaceState
  sourceBound : source.seed = seed
  finalSeed : final.seed = seed
  finalTree : final.treeDigest = seed.treeDigest
  sequenceAdvanced : final.sequence = source.sequence + 1

structure WorkspaceFork where
  seed : WorkspaceSeed
  left : WorkspaceState
  right : WorkspaceState
  leftSeed : left.seed = seed
  rightSeed : right.seed = seed
  distinctIds : left.workspaceId ≠ right.workspaceId


theorem committed_workspace_transition_advances_once
    (transition : WorkspaceTransition)
    (h : transition.committed = true) :
    transition.final.sequence = transition.source.sequence + 1 := by
  exact transition.sequenceAdvancedOnCommit h


theorem aborted_workspace_transition_is_atomic
    (transition : WorkspaceTransition)
    (h : transition.committed = false) :
    transition.final = transition.source := by
  exact transition.sourcePreservedOnAbort h


theorem workspace_transition_preserves_checkpoint_seed
    (transition : WorkspaceTransition) :
    transition.final.seed = transition.source.seed := by
  exact transition.seedPreserved


theorem reset_restores_checkpoint_tree
    (reset : WorkspaceReset) :
    reset.final.seed = reset.seed ∧
      reset.final.treeDigest = reset.seed.treeDigest ∧
      reset.final.sequence = reset.source.sequence + 1 := by
  exact ⟨reset.finalSeed, reset.finalTree, reset.sequenceAdvanced⟩


theorem forks_share_seed_but_not_identity
    (fork : WorkspaceFork) :
    fork.left.seed = fork.right.seed ∧
      fork.left.workspaceId ≠ fork.right.workspaceId := by
  constructor
  · calc
      fork.left.seed = fork.seed := fork.leftSeed
      _ = fork.right.seed := fork.rightSeed.symm
  · exact fork.distinctIds

structure WorkspaceDerivation (Input Output : Type) where
  derive : Input → Output


theorem same_input_has_same_workspace_output
    {Input Output : Type}
    (derivation : WorkspaceDerivation Input Output)
    (left right : Input)
    (sameInput : left = right) :
    derivation.derive left = derivation.derive right := by
  exact congrArg derivation.derive sameInput

end KUOS.WORLD.KuuOSRepositoryCheckpointEvolutionWorkspaceV1_04
