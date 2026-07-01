import KUOS.WORLD.KuuOSRepositoryConstructedCommitPublicationV1_21

namespace KUOS.WORLD.KuuOSRepositorySandboxReflectionV1_23

structure Witness where
  exactSandbox : Prop
  sandboxChanged : Bool
  repositoryRootChanged : Bool
  indexChanged : Bool
  objectDatabaseChanged : Bool
  referenceChanged : Bool
  reflogChanged : Bool

structure Witness.Valid (w : Witness) : Prop where
  exactSandbox : w.exactSandbox
  sandboxChanged : w.sandboxChanged = true
  repositoryRootUnchanged : w.repositoryRootChanged = false
  indexUnchanged : w.indexChanged = false
  objectDatabaseUnchanged : w.objectDatabaseChanged = false
  referenceUnchanged : w.referenceChanged = false
  reflogUnchanged : w.reflogChanged = false


theorem sandbox_reflection_is_scoped
    (w : Witness)
    (h : w.Valid) :
    w.exactSandbox ∧
      w.sandboxChanged = true ∧
      w.repositoryRootChanged = false ∧
      w.indexChanged = false ∧
      w.objectDatabaseChanged = false ∧
      w.referenceChanged = false ∧
      w.reflogChanged = false := by
  exact ⟨h.exactSandbox, h.sandboxChanged, h.repositoryRootUnchanged,
    h.indexUnchanged, h.objectDatabaseUnchanged,
    h.referenceUnchanged, h.reflogUnchanged⟩

end KUOS.WORLD.KuuOSRepositorySandboxReflectionV1_23
