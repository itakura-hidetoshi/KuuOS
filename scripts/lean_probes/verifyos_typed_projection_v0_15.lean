import MethodSoundCoverage

/-!
# VerifyOS v0.15: typed receipt projection and contextual support

The input is already decoded and separately admitted. This module checks
the claim value, retains unavailable claims, and instantiates the actual
v0.14 support/entailment theorem. It does not authenticate a JSON parser,
receipt, signature, external truth, or the admission flag itself.
-/
namespace KUOS.VerifyOS.TypedProjectionV0_15

open KUOS.VerifyOS.MethodSoundCoverageV0_14
set_option autoImplicit false

inductive Claim where
  | integrity_status | scope_status | integrity_exit_code | scope_exit_code
  | snapshot_seq | snapshot_tip | rule_count | withdrawn_count
  | obstruction_count | research_certificate_count
  | scope_candidate_count | scope_held_count | scope_no_use_count
  | action_permission | current_tip | external_truth | lean_proof | new_context_validity
  deriving DecidableEq, Repr

inductive Value where
  | nat (n : Nat)
  | text (s : String)
  deriving DecidableEq, Repr

inductive Kind where
  | integrity | scope | zero | natural | digest | unsupported
  deriving DecidableEq

def kind : Claim → Kind
  | .integrity_status => .integrity
  | .scope_status => .scope
  | .integrity_exit_code => .zero
  | .scope_exit_code => .zero
  | .snapshot_seq => .natural
  | .snapshot_tip => .digest
  | .rule_count => .natural
  | .withdrawn_count => .natural
  | .obstruction_count => .natural
  | .research_certificate_count => .natural
  | .scope_candidate_count => .natural
  | .scope_held_count => .natural
  | .scope_no_use_count => .natural
  | .action_permission => .unsupported
  | .current_tip => .unsupported
  | .external_truth => .unsupported
  | .lean_proof => .unsupported
  | .new_context_validity => .unsupported

def hex64 (s : String) : Bool :=
  s.length == 64 && s.toList.all (fun ch => "0123456789abcdef".toList.contains ch)

/-- Executable projection check, separated from its relational specification. -/
def fieldOK (tip : String) : Kind → Value → Bool
  | .integrity, .text s => decide (s = "PASS_INTEGRITY_ONLY")
  | .scope, .text s => decide (s = "PASS_SCOPE_RECORDS_ONLY")
  | .zero, .nat n => decide (n = 0)
  | .natural, .nat _ => true
  | .digest, .text s => decide (s = tip) && hex64 s
  | _, _ => false

def FieldValid (tip : String) : Kind → Value → Prop
  | .integrity, .text s => s = "PASS_INTEGRITY_ONLY"
  | .scope, .text s => s = "PASS_SCOPE_RECORDS_ONLY"
  | .zero, .nat n => n = 0
  | .natural, .nat _ => True
  | .digest, .text s => s = tip ∧ hex64 s = true
  | _, _ => False

theorem fieldOK_iff (tip : String) (k : Kind) (y : Value) :
    fieldOK tip k y = true ↔ FieldValid tip k y := by
  cases k <;> cases y <;> simp [fieldOK, FieldValid, Bool.and_eq_true]

def project (tip : String) (raw : Claim → Option Value) (x : Claim) : Option Value :=
  match raw x with
  | none => none
  | some y => if fieldOK tip (kind x) y = true then some y else none

theorem project_eq_some_iff (tip : String) (raw : Claim → Option Value)
    (x : Claim) (y : Value) :
    project tip raw x = some y ↔ raw x = some y ∧ FieldValid tip (kind x) y := by
  cases h : raw x with
  | none => simp [project, h]
  | some v =>
    constructor
    · intro hp
      by_cases hv : fieldOK tip (kind x) v = true
      · simp only [project, h, if_pos hv] at hp
        have he : v = y := Option.some.inj hp
        subst y
        exact ⟨rfl, (fieldOK_iff tip (kind x) v).1 hv⟩
      · simp [project, h, hv] at hp
    · rintro ⟨he, hv⟩
      have hy : v = y := Option.some.inj he
      subst y
      have hv' := (fieldOK_iff tip (kind x) v).2 hv
      simp [project, h, hv']

theorem valid_kind_supported (tip : String) (x : Claim) (y : Value)
    (h : FieldValid tip (kind x) y) : kind x ≠ .unsupported := by
  intro he
  rw [he] at h
  cases y <;> exact h

structure SnapshotContext where
  binding : String
  tip : String
  deriving DecidableEq, Repr

structure ReceiptView where
  admitted : Bool
  context : SnapshotContext
  raw : Claim → Option Value

def observed (e : ReceiptView) (ctx : SnapshotContext) (x : Claim) : Option Value :=
  if e.admitted = true ∧ e.context = ctx then project ctx.tip e.raw x else none

def SourceValid (e : ReceiptView) (ctx : SnapshotContext) (x : Claim) (y : Value) : Prop :=
  e.admitted = true ∧ e.context = ctx ∧ e.raw x = some y ∧ FieldValid ctx.tip (kind x) y

theorem observed_iff_sourceValid (e : ReceiptView) (ctx : SnapshotContext)
    (x : Claim) (y : Value) :
    observed e ctx x = some y ↔ SourceValid e ctx x y := by
  by_cases h : e.admitted = true ∧ e.context = ctx
  · simp only [observed, if_pos h, project_eq_some_iff, SourceValid]
    exact ⟨fun hp => ⟨h.1, h.2, hp.1, hp.2⟩, fun hp => hp.2.2⟩
  · simp only [observed, if_neg h, SourceValid]
    constructor
    · intro hp
      cases hp
    · intro hp
      exact False.elim (h ⟨hp.1, hp.2.1⟩)

/-- One typed projection method instantiating the actual v0.14 relation. -/
def methodAdmission (e : ReceiptView) (_ : Unit) (ctx : SnapshotContext) (_ : Claim) : Prop :=
  e.admitted = true ∧ e.context = ctx

def methodScope (_ : Unit) (_ : SnapshotContext) (x : Claim) : Prop :=
  kind x ≠ .unsupported

def methodReport (e : ReceiptView) (_ : Unit) (ctx : SnapshotContext)
    (x : Claim) : Option Value := project ctx.tip e.raw x

theorem method_honors (e : ReceiptView) :
    Honors (methodAdmission e) methodScope (methodReport e) (SourceValid e) := by
  intro i ctx x y ha _ hr
  have hp := (project_eq_some_iff ctx.tip e.raw x y).1 hr
  exact ⟨ha.1, ha.2, hp.1, hp.2⟩

theorem observed_iff_supported (e : ReceiptView) (ctx : SnapshotContext)
    (x : Claim) (y : Value) :
    observed e ctx x = some y ↔
      Supported (methodAdmission e) methodScope (methodReport e) ctx x y := by
  rw [observed_iff_sourceValid]
  constructor
  · intro h
    exact ⟨(), ⟨h.1, h.2.1⟩,
      valid_kind_supported ctx.tip x y h.2.2.2,
      (project_eq_some_iff ctx.tip e.raw x y).2 h.2.2⟩
  · exact support_sound (methodAdmission e) methodScope (methodReport e)
      (SourceValid e) (method_honors e) ctx x y

theorem observed_iff_forced (e : ReceiptView) (ctx : SnapshotContext)
    (x : Claim) (y : Value) :
    observed e ctx x = some y ↔
      Forced (methodAdmission e) methodScope (methodReport e) ctx x y :=
  (observed_iff_supported e ctx x y).trans
    (forced_iff_supported (methodAdmission e) methodScope (methodReport e) ctx x y).symm

theorem wrong_context_hold (e : ReceiptView) (ctx : SnapshotContext) (x : Claim)
    (h : e.context ≠ ctx) : observed e ctx x = none := by
  simp [observed, h]

theorem unadmitted_hold (e : ReceiptView) (ctx : SnapshotContext) (x : Claim)
    (h : e.admitted = false) : observed e ctx x = none := by
  simp [observed, h]

theorem unsupported_hold (e : ReceiptView) (ctx : SnapshotContext) (x : Claim)
    (h : kind x = .unsupported) : observed e ctx x = none := by
  cases ho : observed e ctx x with
  | none => rfl
  | some y =>
    have hv := (observed_iff_sourceValid e ctx x y).1 ho
    exact False.elim (valid_kind_supported ctx.tip x y hv.2.2.2 h)

/-- The original required identifiers stay present even for HOLD rows. -/
def rows (e : ReceiptView) (ctx : SnapshotContext) (required : List Claim) :
    List (Claim × Option Value) :=
  required.map (fun x => (x, observed e ctx x))

theorem row_ids_preserved (e : ReceiptView) (ctx : SnapshotContext) (required : List Claim) :
    (rows e ctx required).map Prod.fst = required := by
  induction required with
  | nil => rfl
  | cons x xs ih => simp [rows, ← ih]

def complete (e : ReceiptView) (ctx : SnapshotContext) : List Claim → Bool
  | [] => true
  | x :: xs => (observed e ctx x).isSome && complete e ctx xs

theorem present_iff (v : Option Value) : v.isSome = true ↔ ∃ y, v = some y := by
  cases v <;> simp

theorem complete_iff_observed (e : ReceiptView) (ctx : SnapshotContext)
    (required : List Claim) :
    complete e ctx required = true ↔
      ∀ x ∈ required, ∃ y, observed e ctx x = some y := by
  induction required with
  | nil => simp [complete]
  | cons x xs ih =>
    simp only [complete, Bool.and_eq_true, present_iff, ih]
    constructor
    · rintro ⟨hx, hxs⟩ z hz
      rcases List.mem_cons.mp hz with he | ht
      · subst z
        exact hx
      · exact hxs z ht
    · intro h
      exact ⟨h x (List.mem_cons.mpr (Or.inl rfl)),
        fun z hz => h z (List.mem_cons.mpr (Or.inr hz))⟩

theorem complete_iff_forced (e : ReceiptView) (ctx : SnapshotContext)
    (required : List Claim) :
    complete e ctx required = true ↔
      ∀ x ∈ required, ∃ y,
        Forced (methodAdmission e) methodScope (methodReport e) ctx x y := by
  rw [complete_iff_observed]
  constructor
  · intro h x hx
    obtain ⟨y, hy⟩ := h x hx
    exact ⟨y, (observed_iff_forced e ctx x y).1 hy⟩
  · intro h x hx
    obtain ⟨y, hy⟩ := h x hx
    exact ⟨y, (observed_iff_forced e ctx x y).2 hy⟩

theorem unsupported_forbids_complete (e : ReceiptView) (ctx : SnapshotContext)
    (required : List Claim) (x : Claim) (hx : x ∈ required)
    (hk : kind x = .unsupported) : complete e ctx required ≠ true := by
  intro h
  obtain ⟨y, hy⟩ := (complete_iff_observed e ctx required).1 h x hx
  rw [unsupported_hold e ctx x hk] at hy
  cases hy

theorem authority_and_freshness_not_projected (e : ReceiptView) (ctx : SnapshotContext) :
    observed e ctx .action_permission = none ∧
    observed e ctx .current_tip = none ∧
    observed e ctx .external_truth = none ∧
    observed e ctx .lean_proof = none ∧
    observed e ctx .new_context_validity = none :=
  ⟨unsupported_hold e ctx .action_permission rfl,
   unsupported_hold e ctx .current_tip rfl,
   unsupported_hold e ctx .external_truth rfl,
   unsupported_hold e ctx .lean_proof rfl,
   unsupported_hold e ctx .new_context_validity rfl⟩

#print axioms Claim
#print axioms Value
#print axioms Kind
#print axioms kind
#print axioms hex64
#print axioms fieldOK
#print axioms FieldValid
#print axioms fieldOK_iff
#print axioms project
#print axioms project_eq_some_iff
#print axioms valid_kind_supported
#print axioms SnapshotContext
#print axioms ReceiptView
#print axioms observed
#print axioms SourceValid
#print axioms observed_iff_sourceValid
#print axioms methodAdmission
#print axioms methodScope
#print axioms methodReport
#print axioms method_honors
#print axioms observed_iff_supported
#print axioms observed_iff_forced
#print axioms wrong_context_hold
#print axioms unadmitted_hold
#print axioms unsupported_hold
#print axioms rows
#print axioms row_ids_preserved
#print axioms complete
#print axioms present_iff
#print axioms complete_iff_observed
#print axioms complete_iff_forced
#print axioms unsupported_forbids_complete
#print axioms authority_and_freshness_not_projected

end KUOS.VerifyOS.TypedProjectionV0_15
