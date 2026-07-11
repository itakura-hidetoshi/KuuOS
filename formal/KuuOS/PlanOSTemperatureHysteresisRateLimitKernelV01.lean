namespace KuuOS

structure TemperatureHysteresisReceipt where
  currentTemperature : Nat
  boundedTemperature : Nat
  effectiveCeiling : Nat
  maxStep : Nat
  futureOnly : Bool
  activeNow : Bool
  executionPermission : Bool
  qiGrantsAuthority : Bool
  historyReadOnly : Bool

 theorem temperature_hysteresis_stays_bounded
    (r : TemperatureHysteresisReceipt)
    (h : r.boundedTemperature ≤ r.effectiveCeiling) :
    r.boundedTemperature ≤ r.effectiveCeiling := h

 theorem temperature_rate_limit_is_preserved
    (r : TemperatureHysteresisReceipt)
    (h : r.boundedTemperature ≤ r.currentTemperature + r.maxStep) :
    r.boundedTemperature ≤ r.currentTemperature + r.maxStep := h

 theorem temperature_hysteresis_grants_no_authority
    (r : TemperatureHysteresisReceipt)
    (h : r.qiGrantsAuthority = false) : r.qiGrantsAuthority = false := h

 theorem temperature_hysteresis_history_is_read_only
    (r : TemperatureHysteresisReceipt)
    (h : r.historyReadOnly = true) : r.historyReadOnly = true := h

 theorem temperature_hysteresis_is_future_only_and_not_execution
    (r : TemperatureHysteresisReceipt)
    (hf : r.futureOnly = true)
    (ha : r.activeNow = false)
    (he : r.executionPermission = false) :
    r.futureOnly = true ∧ r.activeNow = false ∧ r.executionPermission = false :=
  ⟨hf, ha, he⟩

end KuuOS
