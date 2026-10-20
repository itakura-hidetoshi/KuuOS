import Kuu.F112.PolygonNativeCalibratedDescentCriterion

/-!
# F112-P28 — universal native C60 observation/descent obstruction

P27's precise typed fiber criterion is now applied functorially to
postprocessed evidence and charge observations. Neither historical
F41 evidence erasure nor F55 charge-only phase observation can be
made faithful by subsequent coarsening. Conversely, a receiver-relative
F55 observation has a phase decoder iff it actually distinguishes the
two independently calibrated recipients of the same native source.

This is a local, fully typed C60 theorem; not a historical F47/F68/F77
identification. No Gray imports, sorry, admit or extra axioms.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
noncomputable section

universe uX uY uZ uW uT u v

/-- Once a value fails to descend through an observation, no
postprocessing of the observed result can restore it. -/
theorem nativeNoDescent_afterObservationCoarsening
    {X : Type uX} {Y : Type uY}
    {Z : Type uZ} {W : Type uW}
    (observe : X → Y) (coarsen : Y → Z)
    (value : X → W)
    (hNo : ¬ ∃ decode : Y → W,
      ∀ x : X, decode (observe x) = value x) :
    ¬ ∃ decode : Z → W,
      ∀ x : X, decode (coarsen (observe x)) = value x := by
  rintro ⟨decode, hdecode⟩
  apply hNo
  exact ⟨fun y => decode (coarsen y), hdecode⟩

/-- A typed *injective* value factors through an observer iff that
observer is injective, using the exact P27 fiber-descent criterion. -/
theorem nativeInjectiveValue_descends_iff_observerInjective
    {X : Type uX} {Y : Type uY} {Z : Type uZ}
    [Inhabited Z] (observe : X → Y) (value : X → Z)
    (hvalue : Function.Injective value) :
    (∃ decode : Y → Z,
      ∀ x : X, decode (observe x) = value x) ↔
      Function.Injective observe := by
  constructor
  · intro hdecode
    have hinv :=
      (nativeValue_descends_iff_fiberConstant observe value).mp hdecode
    intro x x' hobs
    exact hvalue (hinv x x' hobs)
  · intro hinj
    apply (nativeValue_descends_iff_fiberConstant observe value).mpr
    intro x x' hobs
    exact congrArg value (hinj hobs)

/-- Arbitrary processing of old-shaped F41 evidence still cannot
select the distinguished raw split witness from the native trace. -/
theorem nativeF41Split_noDescent_forAnyHistoricalObserver
    {C : Type u} [Category.{v} C] {x y : C}
    (p : KuuNativeBlocks x y)
    {T : Type uT}
    (observe : KuuNativeHistoricalAxisTrace 1
      (nativeF41DoubleNilSource p) (nativeF41DoubleNilTarget p) → T) :
    ¬ ∃ Q : T → Prop,
        ∀ h : KuuNativeAxisTrace 1
          (nativeF41DoubleNilSource p) (nativeF41DoubleNilTarget p),
          (Q (observe h.toHistorical) ↔
            h = nativeF41DoubleNilSplitTrace p) := by
  rintro ⟨Q, hQ⟩
  apply nativeF41DoubleNil_splitPredicate_noDescent p
  exact ⟨fun hist => Q (observe hist), hQ⟩

/-- Postprocessing historical evidence never turns the full Type
witness bundle into a faithfully observed carrier. -/
theorem nativeF41Bundle_historical_postobserve_not_injective
    {C : Type u} [Category.{v} C] {x y : C}
    (p : KuuNativeBlocks x y)
    {T : Type uT}
    (observe : KuuNativeHistoricalAxisTrace 1
      (nativeF41DoubleNilSource p) (nativeF41DoubleNilTarget p) → T) :
    ¬ Function.Injective
      (fun bundle : NativeF41EvidenceBundle p =>
        observe bundle.historical) := by
  intro hinj
  apply nativeF41EvidenceBundle_historical_not_injective p
  intro a b hab
  exact hinj (congrArg observe hab)

/-- Genuine north C60 pentagon specialization of the universal F41
non-faithfulness statement. -/
theorem northPentagon_nativeF41Bundle_postobserve_not_injective
    {T : Type uT}
    (observe : KuuNativeHistoricalAxisTrace 1
      (nativeF41DoubleNilSource northPentagonNativeDualAxisFrame.firstAxis)
      (nativeF41DoubleNilTarget northPentagonNativeDualAxisFrame.firstAxis)
      → T) :
    ¬ Function.Injective
      (fun bundle :
        NativeF41EvidenceBundle northPentagonNativeDualAxisFrame.firstAxis =>
        observe bundle.historical) :=
  nativeF41Bundle_historical_postobserve_not_injective
    northPentagonNativeDualAxisFrame.firstAxis observe

/-- The two genuine six-sector C60 receivers assign distinct
ZMod 2 values to the SAME source square. Thus their phase is an
injective function of the receiver-calibration choice. -/
theorem northHexagonReceiverPhase_injective :
    Function.Injective northHexagonReceiverPhase := by
  intro a b hab
  cases a <;> cases b
  · rfl
  · exact False.elim (northHexagonReceiver_phase_ne hab)
  · exact False.elim (northHexagonReceiver_phase_ne hab.symm)
  · rfl

/-- The universal, receiver-relative local calibration theorem:
a phase decoder exists precisely for observations that separate the
two genuinely distinct even and odd receiver calibrations. -/
theorem northHexagonReceiver_phaseDescent_iff_injective
    {T : Type uT} (observe : Bool → T) :
    (∃ decode : T → ZMod 2,
      ∀ b : Bool, decode (observe b) = northHexagonReceiverPhase b) ↔
    Function.Injective observe :=
  nativeInjectiveValue_descends_iff_observerInjective
    observe northHexagonReceiverPhase northHexagonReceiverPhase_injective

/-- Every charge-derived statistic, even with nonlinear or quotient
postprocessing, still fails to reconstruct both F55 phases. -/
theorem northHexagonReceiver_noPhaseDescent_fromAnyChargeStatistic
    {T : Type uT} (statistic : (Int × Int) → T) :
    ¬ ∃ decode : T → ZMod 2,
      ∀ b : Bool,
        decode (statistic (northHexagonReceiverCharge b)) =
          northHexagonReceiverPhase b :=
  nativeNoDescent_afterObservationCoarsening
    northHexagonReceiverCharge statistic northHexagonReceiverPhase
    northHexagonReceiver_no_chargeOnlyTypedDescent

/-- Conversely, carrying the receiver choice explicitly permits
typed phase decoding by the universal observer theorem. -/
theorem northHexagonReceiver_taggedPhaseDescent_byUniversality :
    ∃ decode : ((Int × Int) × Bool) → ZMod 2,
      ∀ b : Bool,
        decode (northHexagonReceiverTaggedCharge b) =
          northHexagonReceiverPhase b :=
  (northHexagonReceiver_phaseDescent_iff_injective
    northHexagonReceiverTaggedCharge).mpr
    northHexagonReceiverTaggedCharge_injective

#print axioms nativeNoDescent_afterObservationCoarsening
#print axioms nativeInjectiveValue_descends_iff_observerInjective
#print axioms nativeF41Split_noDescent_forAnyHistoricalObserver
#print axioms nativeF41Bundle_historical_postobserve_not_injective
#print axioms northPentagon_nativeF41Bundle_postobserve_not_injective
#print axioms northHexagonReceiverPhase_injective
#print axioms northHexagonReceiver_phaseDescent_iff_injective
#print axioms northHexagonReceiver_noPhaseDescent_fromAnyChargeStatistic
#print axioms northHexagonReceiver_taggedPhaseDescent_byUniversality

end
end Kuu.F112.Physical
