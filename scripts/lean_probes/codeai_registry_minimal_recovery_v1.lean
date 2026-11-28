/- R76: a checked, inclusion-least fresh batch for finite required bindings.
Repeated identical obligations are retained in the input history but need
only one candidate binding. Conflicts are never repaired by overwriting.
This is a pure candidate constructor, not registration authority. -/
namespace KuuOSR76
open KuuOSR69 KuuOSR70 KuuOSR71 KuuOSR72 KuuOSR73 KuuOSR74 KuuOSR75
universe u v

def Compatible {κ : Type v} {α : Type u}
    (reg : κ → Option (Basis α)) (req : List (κ × Basis α)) : Prop :=
  ∀ b ∈ req, reg b.1 = none ∨ reg b.1 = some b.2

def Consistent {κ : Type v} {α : Type u} (req : List (κ × Basis α)) : Prop :=
  ∀ b ∈ req, ∀ c ∈ req, b.1 = c.1 → b = c

def compatibilityCheck {κ : Type v} {α : Type u} [DecidableEq α]
    (reg : κ → Option (Basis α)) (req : List (κ × Basis α)) : Bool :=
  req.all (fun b => decide (reg b.1 = none ∨ reg b.1 = some b.2))

def consistencyCheck {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (req : List (κ × Basis α)) : Bool :=
  req.all (fun b => req.all (fun c => decide (b.1 = c.1 → b = c)))

def minimalBatch {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (reg : κ → Option (Basis α)) (req : List (κ × Basis α)) : List (κ × Basis α) :=
  (missingBindings reg req).dedup

def checkedRecoveryPlan {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (reg : κ → Option (Basis α)) (req : List (κ × Basis α)) :
    Option (List (κ × Basis α)) :=
  if compatibilityCheck reg req = true ∧ consistencyCheck req = true
  then some (minimalBatch reg req) else none

theorem compatibility_check_iff {κ : Type v} {α : Type u} [DecidableEq α]
    (reg : κ → Option (Basis α)) (req : List (κ × Basis α)) :
    compatibilityCheck reg req = true ↔ Compatible reg req := by
  simp only [compatibilityCheck, Compatible, List.all_eq_true, decide_eq_true_eq]

theorem consistency_check_iff {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (req : List (κ × Basis α)) :
    consistencyCheck req = true ↔ Consistent req := by
  simp only [consistencyCheck, Consistent, List.all_eq_true, decide_eq_true_eq]

theorem minimal_batch_mem {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (reg : κ → Option (Basis α)) (req : List (κ × Basis α)) (b : κ × Basis α) :
    b ∈ minimalBatch reg req ↔ b ∈ req ∧ reg b.1 = none :=
  List.mem_dedup.trans (missing_binding_iff reg req b)

theorem minimal_batch_ready {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (reg : κ → Option (Basis α)) (req : List (κ × Basis α))
    (hc : Consistent req) : BatchReady reg (minimalBatch reg req) := by
  refine ⟨fun b hb => ((minimal_batch_mem reg req b).mp hb).2, ?_⟩
  have hd : (minimalBatch reg req).Nodup := List.nodup_dedup _
  refine List.Nodup.map_on (f := Prod.fst) ?_ hd
  intro b hb c hc' he
  exact hc b ((minimal_batch_mem reg req b).mp hb).1
    c ((minimal_batch_mem reg req c).mp hc').1 he

theorem minimal_batch_supplies {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (reg : κ → Option (Basis α)) (req : List (κ × Basis α))
    (hc : Compatible reg req) : Supplies reg (minimalBatch reg req) req := by
  intro b hb
  rcases hc b hb with hn | ho
  · exact Or.inr ((minimal_batch_mem reg req b).mpr ⟨hb,hn⟩)
  · exact Or.inl ho

theorem checked_plan_some_iff {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (reg : κ → Option (Basis α)) (req bs : List (κ × Basis α)) :
    checkedRecoveryPlan reg req = some bs ↔
      Compatible reg req ∧ Consistent req ∧ bs = minimalBatch reg req := by
  unfold checkedRecoveryPlan
  by_cases h : compatibilityCheck reg req = true ∧ consistencyCheck req = true
  · rw [if_pos h]
    constructor
    · intro he
      exact ⟨(compatibility_check_iff reg req).mp h.1,
        (consistency_check_iff req).mp h.2, (Option.some.inj he).symm⟩
    · rintro ⟨_,_,he⟩
      rw [he]
  · rw [if_neg h]
    constructor
    · intro he
      cases he
    · intro he
      exact False.elim (h ⟨(compatibility_check_iff reg req).mpr he.1,
        (consistency_check_iff req).mpr he.2.1⟩)

theorem checked_plan_admits {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (reg : κ → Option (Basis α)) (req bs : List (κ × Basis α))
    (hp : checkedRecoveryPlan reg req = some bs) :
    ∃ next, checkedBatch reg bs = some next ∧ CoversBindings next req := by
  obtain ⟨hc,hn,he⟩ := (checked_plan_some_iff reg req bs).mp hp
  subst bs
  obtain ⟨next,hb⟩ := checked_batch_exists reg (minimalBatch reg req)
    (minimal_batch_ready reg req hn)
  exact ⟨next,hb,(requirements_after_batch_iff reg next (minimalBatch reg req) req hb).mpr
    (minimal_batch_supplies reg req hc)⟩

theorem recovering_batch_contains_minimal {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (reg next : κ → Option (Basis α)) (req bs : List (κ × Basis α))
    (hb : checkedBatch reg bs = some next) (hc : CoversBindings next req)
    (b : κ × Basis α) (hm : b ∈ minimalBatch reg req) : b ∈ bs := by
  have h := (minimal_batch_mem reg req b).mp hm
  rcases (requirements_after_batch_iff reg next bs req hb).mp hc b h.1 with ho | hs
  · have impossible : (none : Option (Basis α)) = some b.2 := h.2.symm.trans ho
    cases impossible
  · exact hs

theorem checked_plan_minimal {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (reg next : κ → Option (Basis α)) (req candidate bs : List (κ × Basis α))
    (hp : checkedRecoveryPlan reg req = some candidate)
    (hb : checkedBatch reg bs = some next) (hc : CoversBindings next req) :
    ∀ b ∈ candidate, b ∈ bs := by
  have he := ((checked_plan_some_iff reg req candidate).mp hp).2.2
  intro b hm
  rw [he] at hm
  exact recovering_batch_contains_minimal reg next req bs hb hc b hm

theorem extension_conditions {κ : Type v} {α : Type u}
    (reg next : κ → Option (Basis α)) (req : List (κ × Basis α))
    (he : RegistryExtends reg next) (hc : CoversBindings next req) :
    Compatible reg req ∧ Consistent req := by
  constructor
  · intro b hb
    cases ho : reg b.1 with
    | none => exact Or.inl rfl
    | some G =>
        exact Or.inr (congrArg some (registered_binding_unique next b.1 G b.2
          (he b.1 G ho) (hc b hb)))
  · intro b hb c hc' hk
    have hval : next b.1 = some c.2 := by
      rw [hk]
      exact hc c hc'
    exact Prod.ext hk (registered_binding_unique next b.1 b.2 c.2 (hc b hb) hval)

theorem checked_plan_exists_iff_extension {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (reg : κ → Option (Basis α)) (req : List (κ × Basis α)) :
    (∃ bs, checkedRecoveryPlan reg req = some bs) ↔
      ∃ next, RegistryExtends reg next ∧ CoversBindings next req := by
  constructor
  · rintro ⟨bs,hp⟩
    obtain ⟨next,hb,hc⟩ := checked_plan_admits reg req bs hp
    exact ⟨next,checked_batch_extends reg next bs hb,hc⟩
  · rintro ⟨next,he,hc⟩
    have h := extension_conditions reg next req he hc
    exact ⟨minimalBatch reg req,(checked_plan_some_iff reg req (minimalBatch reg req)).mpr
      ⟨h.1,h.2,rfl⟩⟩

theorem checked_plan_none_iff_no_extension {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (reg : κ → Option (Basis α)) (req : List (κ × Basis α)) :
    checkedRecoveryPlan reg req = none ↔
      ¬ ∃ next, RegistryExtends reg next ∧ CoversBindings next req := by
  constructor
  · intro hn he
    obtain ⟨bs,hs⟩ := (checked_plan_exists_iff_extension reg req).mpr he
    rw [hn] at hs
    cases hs
  · intro hn
    cases hs : checkedRecoveryPlan reg req with
    | none => rfl
    | some bs =>
        exact False.elim (hn ((checked_plan_exists_iff_extension reg req).mp ⟨bs,hs⟩))

theorem checked_plan_path_recovers {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (reg : κ → Option (Basis α)) (bs : List (κ × Basis α))
    (k l : κ) (F H : Basis α) (path : List (TaggedStep κ α)) (P : Delta α)
    (hp : checkedRecoveryPlan reg (RequiredBindings k l F H path) = some bs)
    (ht : checkedTaggedPath k l F H path = some P) :
    ∃ next, checkedBatch reg bs = some next ∧ checkedRegisteredPath next k l F H path = some P := by
  obtain ⟨next,hb,hc⟩ := checked_plan_admits reg (RequiredBindings k l F H path) bs hp
  exact ⟨next,hb,(recovery_iff_of_tagged next k l F H path P ht).mpr
    ((required_bindings_iff next k l F H path).mp hc)⟩

theorem checked_plan_conflict_hold {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (reg : κ → Option (Basis α)) (req : List (κ × Basis α)) (b : κ × Basis α) (G : Basis α)
    (hm : b ∈ req) (ho : reg b.1 = some G) (hne : G ≠ b.2) :
    checkedRecoveryPlan reg req = none := by
  apply (checked_plan_none_iff_no_extension reg req).mpr
  rintro ⟨next,he,hc⟩
  exact conflicting_requirement_no_extension reg next req b G he hm ho hne hc

theorem checked_plan_inconsistent_hold {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (reg : κ → Option (Basis α)) (req : List (κ × Basis α)) (b c : κ × Basis α)
    (hb : b ∈ req) (hc : c ∈ req) (he : b.1 = c.1) (hne : b.2 ≠ c.2) :
    checkedRecoveryPlan reg req = none := by
  apply (checked_plan_none_iff_no_extension reg req).mpr
  rintro ⟨next,_,hv⟩
  exact inconsistent_requirements_no_registry next req b c hb hc he hne hv

end KuuOSR76
