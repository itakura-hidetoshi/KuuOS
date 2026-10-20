import Kuu.F112.PolygonNativeHigherDescentObstructions

/-!
# F112-P27 — exact fiberwise descent and witness-preserving calibration

P26 exhibited two genuine C60 obstructions. Here both are placed under
a single precise mathematical descent criterion: a raw predicate or
typed value descends through an observer if and only if it is constant
on that observer's fibers.

For F41, an explicitly dependent Type-valued bundle retains the raw
step together with its historical-shaped erased witness. The bundle
is equivalent to the raw carrier, whereas forgetting its raw component
is not injective on the real C60 north-pentagon witness.

For F55, two independently calibrated receivers of the *same* native
C60 hexagon square have equal signed charges but distinct ZMod 2
phases. A charge-only value cannot descend, while a receiver-tagged
observation admits an explicit decoder. The receiver tag is genuine
extra calibration data; this is not a historical F68/F77 comparison.

No Gray or historical KUOS imports, no extra axioms, sorry, or admit.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
noncomputable section

universe uX uY uZ u v

/-- Exact constructive criterion for the descent of a proposition:
it must be invariant under equality of the observed images.
The implication from fiber constancy needs no choice. -/
theorem nativePredicate_descends_iff_fiberInvariant
    {X : Type uX} {Y : Type uY}
    (observe : X → Y) (P : X → Prop) :
    (∃ Q : Y → Prop, ∀ x : X, Q (observe x) ↔ P x) ↔
      (∀ x x' : X, observe x = observe x' → (P x ↔ P x')) := by
  constructor
  · rintro ⟨Q, hQ⟩ x x' hobs
    calc
      P x ↔ Q (observe x) := (hQ x).symm
      _ ↔ Q (observe x') := by rw [hobs]
      _ ↔ P x' := hQ x'
  · intro hinv
    refine ⟨fun y => ∃ x : X, observe x = y ∧ P x, ?_⟩
    intro x
    constructor
    · rintro ⟨x', hobs, hp⟩
      exact (hinv x' x hobs).mp hp
    · intro hp
      exact ⟨x, rfl, hp⟩

/-- The corresponding typed-value criterion. On empty observation
fibers a default target value is used; on inhabited fibers the decoder
chooses a representative, and fiber constancy makes it well-defined.
The actual source and observer retain their original types. -/
theorem nativeValue_descends_iff_fiberConstant
    {X : Type uX} {Y : Type uY} {Z : Type uZ}
    [Inhabited Z] (observe : X → Y) (value : X → Z) :
    (∃ decode : Y → Z, ∀ x : X, decode (observe x) = value x) ↔
      (∀ x x' : X, observe x = observe x' → value x = value x') := by
  constructor
  · rintro ⟨decode, hdecode⟩ x x' hobs
    calc
      value x = decode (observe x) := (hdecode x).symm
      _ = decode (observe x') := congrArg decode hobs
      _ = value x' := hdecode x'
  · intro hinv
    classical
    let decode : Y → Z := fun y =>
      if h : ∃ x : X, observe x = y then
        value (Classical.choose h)
      else
        default
    refine ⟨decode, ?_⟩
    intro x
    dsimp [decode]
    split_ifs with h
    · exact hinv (Classical.choose h) x (Classical.choose_spec h)
    · exact False.elim (h ⟨x, rfl⟩)

/-- A Type-valued F41 witness bundle retaining the *actual* native
proof object, its exact depth-one endpoints, and the erased
historical-shaped evidence together with their compatibility. -/
structure NativeF41EvidenceBundle
    {C : Type u} [Category.{v} C] {x y : C}
    (p : KuuNativeBlocks x y) where
  historical :
    KuuNativeHistoricalAxisTrace 1
      (nativeF41DoubleNilSource p) (nativeF41DoubleNilTarget p)
  raw :
    KuuNativeAxisTrace 1
      (nativeF41DoubleNilSource p) (nativeF41DoubleNilTarget p)
  compatible : raw.toHistorical = historical

/-- Retaining the raw witness in the corresponding historical fiber
is lossless. This is NOT an equivalence from raw histories to
erased historical histories alone. -/
def nativeF41EvidenceBundleEquiv
    {C : Type u} [Category.{v} C] {x y : C}
    (p : KuuNativeBlocks x y) :
    KuuNativeAxisTrace 1
      (nativeF41DoubleNilSource p) (nativeF41DoubleNilTarget p) ≃
      NativeF41EvidenceBundle p where
  toFun := fun raw => ⟨raw.toHistorical, raw, rfl⟩
  invFun := fun bundle => bundle.raw
  left_inv := fun _ => rfl
  right_inv := by
    intro bundle
    rcases bundle with ⟨historical, raw, hraw⟩
    cases hraw
    rfl

/-- On any native double-nil source, an F41 predicate selecting the
split primitive is NOT constant on historical-erasure fibers.
This is the exact failed hypothesis of the criterion above. -/
theorem nativeF41DoubleNil_split_not_fiberInvariant
    {C : Type u} [Category.{v} C] {x y : C}
    (p : KuuNativeBlocks x y) :
    ¬ ∀ h k : KuuNativeAxisTrace 1
        (nativeF41DoubleNilSource p) (nativeF41DoubleNilTarget p),
      h.toHistorical = k.toHistorical →
        (h = nativeF41DoubleNilSplitTrace p ↔
         k = nativeF41DoubleNilSplitTrace p) := by
  intro hinv
  have heq :=
    (hinv (nativeF41DoubleNilSplitTrace p)
      (nativeF41DoubleNilInsertTrace p)
      (nativeF41DoubleNil_toHistorical_eq p)).mp rfl
  exact nativeF41DoubleNilSplitTrace_ne_insert p heq.symm

/-- The loss of raw proof relevance is not repaired by the
historical projection from the faithful witness bundle: two distinct
bundles over genuine native C60 endpoints share one historical value. -/
theorem nativeF41EvidenceBundle_historical_not_injective
    {C : Type u} [Category.{v} C] {x y : C}
    (p : KuuNativeBlocks x y) :
    ¬ Function.Injective
      (fun witness : NativeF41EvidenceBundle p => witness.historical) := by
  intro hinj
  have heq := hinj (nativeF41DoubleNil_toHistorical_eq p)
  have hraw := congrArg
    (fun witness : NativeF41EvidenceBundle p => witness.raw) heq
  exact nativeF41DoubleNilSplitTrace_ne_insert p hraw

/-- Specialization to the original physical north C60 pentagon frame,
not an unrelated abstract category. -/
theorem northPentagon_nativeF41EvidenceBundle_historical_not_injective :
    ¬ Function.Injective
      (fun witness :
        NativeF41EvidenceBundle northPentagonNativeDualAxisFrame.firstAxis =>
        witness.historical) :=
  nativeF41EvidenceBundle_historical_not_injective
    northPentagonNativeDualAxisFrame.firstAxis

/-- Receiver-indexed signed observation of exactly the same genuinely
constructed north C60 hexagon F55 six-sector source square. -/
def northHexagonReceiverCharge : Bool → Int × Int
  | false => northHexagonEvenShadow.1
  | true => northHexagonOddShadow.1

/-- The separate, target-dependent phase of that same square. -/
def northHexagonReceiverPhase : Bool → ZMod 2
  | false => northHexagonEvenShadow.2
  | true => northHexagonOddShadow.2

theorem northHexagonReceiver_charge_eq :
    northHexagonReceiverCharge false =
      northHexagonReceiverCharge true :=
  northHexagonEvenOddShadow_charge_eq

theorem northHexagonReceiver_phase_ne :
    northHexagonReceiverPhase false ≠
      northHexagonReceiverPhase true :=
  northHexagonEvenOddShadow_phase_ne

/-- Phase is not constant on signed-charge observation fibers of
the two genuinely typed F55 receiver calibrations. -/
theorem northHexagonReceiver_phase_not_fiberConstant :
    ¬ ∀ a b : Bool,
      northHexagonReceiverCharge a = northHexagonReceiverCharge b →
        northHexagonReceiverPhase a = northHexagonReceiverPhase b := by
  intro hinv
  exact northHexagonReceiver_phase_ne
    (hinv false true northHexagonReceiver_charge_eq)

/-- The generic typed descent criterion now proves the precise
F55 impossibility: no *single* signed-charge-only decoder represents
both independent choices of receiver phase. -/
theorem northHexagonReceiver_no_chargeOnlyTypedDescent :
    ¬ ∃ decode : (Int × Int) → ZMod 2,
      ∀ b : Bool,
        decode (northHexagonReceiverCharge b) =
          northHexagonReceiverPhase b := by
  intro h
  apply northHexagonReceiver_phase_not_fiberConstant
  exact (nativeValue_descends_iff_fiberConstant
    northHexagonReceiverCharge northHexagonReceiverPhase).mp h

/-- One explicit, faithful *observation of the calibration choice*:
the signed charge together with the chosen receiver tag. -/
def northHexagonReceiverTaggedCharge (b : Bool) : (Int × Int) × Bool :=
  (northHexagonReceiverCharge b, b)

theorem northHexagonReceiverTaggedCharge_injective :
    Function.Injective northHexagonReceiverTaggedCharge := by
  intro a b hab
  exact congrArg Prod.snd hab

/-- Receiver-calibrated descent is possible: the missing information
is the *supplied target calibration*, not a phase secretly determined
by the uncalibrated source charge. -/
theorem northHexagonReceiver_taggedPhaseDecoder_exists :
    ∃ decode : ((Int × Int) × Bool) → ZMod 2,
      ∀ b : Bool,
        decode (northHexagonReceiverTaggedCharge b) =
          northHexagonReceiverPhase b := by
  exact ⟨fun datum => northHexagonReceiverPhase datum.2, fun _ => rfl⟩

#print axioms nativePredicate_descends_iff_fiberInvariant
#print axioms nativeValue_descends_iff_fiberConstant
#print axioms nativeF41EvidenceBundleEquiv
#print axioms nativeF41DoubleNil_split_not_fiberInvariant
#print axioms nativeF41EvidenceBundle_historical_not_injective
#print axioms northPentagon_nativeF41EvidenceBundle_historical_not_injective
#print axioms northHexagonReceiver_charge_eq
#print axioms northHexagonReceiver_phase_ne
#print axioms northHexagonReceiver_phase_not_fiberConstant
#print axioms northHexagonReceiver_no_chargeOnlyTypedDescent
#print axioms northHexagonReceiverTaggedCharge_injective
#print axioms northHexagonReceiver_taggedPhaseDecoder_exists

end
end Kuu.F112.Physical
