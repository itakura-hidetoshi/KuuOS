import KUOS.WORLD.KuuOSConnectionCandidateCoreV0_62

namespace KUOS.WORLD.KuuOSConnectionCandidateGaugeInvarianceV0_62

open KUOS.WORLD.KuuOSConnectionCandidateCoreV0_62

def IsGaugeInvariantObservable
    {G C O : Type*}
    (act : G → C → C)
    (observable : C → O) : Prop :=
  ∀ g connection, observable (act g connection) = observable connection

theorem gauge_change_preserves_candidate_observables
    {G C R H : Type*} [LE R]
    (act : G → C → C)
    (curvature : C → R)
    (holonomy : C → H)
    (hCurvature : IsGaugeInvariantObservable act curvature)
    (hHolonomy : IsGaugeInvariantObservable act holonomy)
    (g : G)
    (source candidate : C)
    (hOrder : curvature candidate ≤ curvature source)
    (hProtected : holonomy candidate = holonomy source) :
    curvature (act g candidate) ≤ curvature (act g source) ∧
      holonomy (act g candidate) = holonomy (act g source) := by
  constructor
  · rw [hCurvature g candidate, hCurvature g source]
    exact hOrder
  · rw [hHolonomy g candidate, hHolonomy g source]
    exact hProtected

structure FiniteSearchReceipt (Candidate : Type*) where
  evaluatedCandidates : Nat
  admissibleCandidates : Nat
  selected : Option Candidate
  preserveSourceWhenNone : Prop
  candidateOnly : Prop
  noStateWrite : Prop

theorem empty_search_preserves_source
    {Candidate : Type*}
    (receipt : FiniteSearchReceipt Candidate)
    (hNone : receipt.selected = none)
    (hBoundary : receipt.preserveSourceWhenNone) :
    receipt.selected = none ∧ receipt.preserveSourceWhenNone :=
  ⟨hNone, hBoundary⟩

end KUOS.WORLD.KuuOSConnectionCandidateGaugeInvarianceV0_62
