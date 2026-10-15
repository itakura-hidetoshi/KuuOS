import KUOS.DependentOriginationMemoryLiftedHistoryTransportV0_7

namespace KUOS.DependentOriginationTransportSpineV0_7

open KUOS.DependentOriginationHistorySensitiveTransportV0_5
open KUOS.DependentOriginationMemoryLiftedHistoryTransportV0_7

universe u v w

namespace MemoryLiftedStep

variable {Event : Type u} {Visible : Type v} {Memory : Type w}

/-- The enlarged visible-plus-memory carrier remains exactly compositional. -/
theorem full_state_history_composition
    (S : MemoryLiftedStep Event Visible Memory)
    (left right : List Event)
    (state : Visible × Memory) :
    S.toHistoryTransport.eval (left ++ right) state =
      S.toHistoryTransport.eval left
        (S.toHistoryTransport.eval right state) :=
  S.extended_eval_append left right state

/--
After projecting away memory, composition must carry forward the memory created
by the earlier/right history.
-/
theorem visible_history_composition_with_memory
    (S : MemoryLiftedStep Event Visible Memory)
    (initialMemory : Memory)
    (left right : List Event)
    (x : Visible) :
    S.visibleEval initialMemory (left ++ right) x =
      S.visibleEval (S.memoryEval initialMemory right x) left
        (S.visibleEval initialMemory right x) :=
  S.visibleEval_append initialMemory left right x

end MemoryLiftedStep

section AdditiveSummary

variable {Time : Type u} [AddMonoid Time]
variable {Visible : Type v} {Memory : Type w}

namespace MemoryLiftedStep

/--
Visible same-summary history sensitivity is incompatible with any total-time
semigroup factorization of the enlarged state transport.
-/
theorem visible_history_sensitivity_rules_out_total_time_semigroup
    (S : MemoryLiftedStep Time Visible Memory)
    (initialMemory : Memory)
    (h : S.GenuinelyVisibleHistorySensitive initialMemory) :
    ¬ Nonempty (TotalTimeFactorization S.toHistoryTransport) :=
  S.no_totalTimeFactorization_of_visible_history_sensitive initialMemory h

end MemoryLiftedStep

end AdditiveSummary

end KUOS.DependentOriginationTransportSpineV0_7
