/- R75: exact required bindings, conditional recovery and conflict obstruction.
A supplied fresh batch is not authenticated merely by satisfying these conditions.
Required occurrences are retained even when a binding is repeated. -/
namespace KuuOSR75
open KuuOSR69 KuuOSR70 KuuOSR71 KuuOSR72 KuuOSR73 KuuOSR74
universe u v

def StepRequirements {κ : Type v} {α : Type u} :
    List (TaggedStep κ α) → List (κ × Basis α)
  | [] => []
  | s :: tail => (s.sourceKey,s.patch.source) :: (s.targetKey,s.patch.target) :: StepRequirements tail

def RequiredBindings {κ : Type v} {α : Type u}
    (k l : κ) (F H : Basis α) (path : List (TaggedStep κ α)) : List (κ × Basis α) :=
  (k,F) :: (l,H) :: StepRequirements path

def CoversBindings {κ : Type v} {α : Type u}
    (reg : κ → Option (Basis α)) (req : List (κ × Basis α)) : Prop :=
  ∀ b ∈ req, reg b.1 = some b.2

def Supplies {κ : Type v} {α : Type u}
    (reg : κ → Option (Basis α)) (bs req : List (κ × Basis α)) : Prop :=
  ∀ b ∈ req, reg b.1 = some b.2 ∨ b ∈ bs

def supplyCheck {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (reg : κ → Option (Basis α)) (bs req : List (κ × Basis α)) : Bool :=
  req.all (fun b => decide (reg b.1 = some b.2 ∨ b ∈ bs))

def missingBindings {κ : Type v} {α : Type u} [DecidableEq α]
    (reg : κ → Option (Basis α)) (req : List (κ × Basis α)) : List (κ × Basis α) :=
  req.filter (fun b => decide (reg b.1 = none))

theorem covers_cons {κ : Type v} {α : Type u}
    (reg : κ → Option (Basis α)) (b : κ × Basis α) (bs : List (κ × Basis α)) :
    CoversBindings reg (b :: bs) ↔ reg b.1 = some b.2 ∧ CoversBindings reg bs := by
  constructor
  · intro h
    exact ⟨h b List.mem_cons_self, fun c hc => h c (List.mem_cons.mpr (Or.inr hc))⟩
  · intro h c hc
    rcases List.mem_cons.mp hc with he | ht
    · subst c
      exact h.1
    · exact h.2 c ht

theorem step_requirements_iff {κ : Type v} {α : Type u}
    (reg : κ → Option (Basis α)) (path : List (TaggedStep κ α)) :
    CoversBindings reg (StepRequirements path) ↔ RegisteredSteps reg path := by
  induction path with
  | nil =>
      change CoversBindings reg [] ↔ True
      constructor
      · intro _
        exact True.intro
      · intro _ b hb
        cases hb
  | cons s tail ih =>
      change CoversBindings reg ((s.sourceKey,s.patch.source) :: (s.targetKey,s.patch.target) ::
        StepRequirements tail) ↔
        reg s.sourceKey = some s.patch.source ∧ reg s.targetKey = some s.patch.target ∧ RegisteredSteps reg tail
      have hs := covers_cons reg (s.sourceKey,s.patch.source)
        ((s.targetKey,s.patch.target) :: StepRequirements tail)
      have ht := covers_cons reg (s.targetKey,s.patch.target) (StepRequirements tail)
      constructor
      · intro h
        obtain ⟨hsource, hrest⟩ := hs.mp h
        obtain ⟨htarget, htail⟩ := ht.mp hrest
        exact ⟨hsource, htarget, ih.mp htail⟩
      · intro h
        exact hs.mpr ⟨h.1, ht.mpr ⟨h.2.1, ih.mpr h.2.2⟩⟩

theorem required_bindings_iff {κ : Type v} {α : Type u}
    (reg : κ → Option (Basis α)) (k l : κ) (F H : Basis α)
    (path : List (TaggedStep κ α)) :
    CoversBindings reg (RequiredBindings k l F H path) ↔ RegistryValid reg k l F H path := by
  change CoversBindings reg ((k,F) :: (l,H) :: StepRequirements path) ↔
    reg k = some F ∧ reg l = some H ∧ RegisteredSteps reg path
  have hk := covers_cons reg (k,F) ((l,H) :: StepRequirements path)
  have hl := covers_cons reg (l,H) (StepRequirements path)
  have hp := step_requirements_iff reg path
  constructor
  · intro h
    obtain ⟨hsource, hrest⟩ := hk.mp h
    obtain ⟨htarget, htail⟩ := hl.mp hrest
    exact ⟨hsource, htarget, hp.mp htail⟩
  · intro h
    exact hk.mpr ⟨h.1, hl.mpr ⟨h.2.1, hp.mpr h.2.2⟩⟩

theorem supply_check_iff {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (reg : κ → Option (Basis α)) (bs req : List (κ × Basis α)) :
    supplyCheck reg bs req = true ↔ Supplies reg bs req := by
  simp only [supplyCheck, Supplies, List.all_eq_true, decide_eq_true_eq]

theorem binding_after_batch_iff {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (reg next : κ → Option (Basis α)) (bs : List (κ × Basis α)) (b : κ × Basis α)
    (hb : checkedBatch reg bs = some next) :
    next b.1 = some b.2 ↔ reg b.1 = some b.2 ∨ b ∈ bs := by
  constructor
  · intro hn
    classical
    by_cases hm : ∃ c ∈ bs, c.1 = b.1
    · obtain ⟨c,hc,he⟩ := hm
      have hv : next b.1 = some c.2 := by
        rw [← he]
        exact checked_batch_contains reg next bs hb c hc
      have hval : c.2 = b.2 := Option.some.inj (hv.symm.trans hn)
      have heq : c = b := Prod.ext he hval
      exact Or.inr (heq ▸ hc)
    · have ha : ∀ c ∈ bs, b.1 ≠ c.1 :=
        fun c hc he => hm ⟨c,hc,he.symm⟩
      exact Or.inl ((checked_batch_frame reg next bs b.1 hb ha).symm.trans hn)
  · intro h
    rcases h with ho | hm
    · exact checked_batch_extends reg next bs hb b.1 b.2 ho
    · exact checked_batch_contains reg next bs hb b hm

theorem requirements_after_batch_iff {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (reg next : κ → Option (Basis α)) (bs req : List (κ × Basis α))
    (hb : checkedBatch reg bs = some next) :
    CoversBindings next req ↔ Supplies reg bs req := by
  constructor
  · intro h b hm
    exact (binding_after_batch_iff reg next bs b hb).mp (h b hm)
  · intro h b hm
    exact (binding_after_batch_iff reg next bs b hb).mpr (h b hm)

theorem checked_batch_recovery_iff {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (reg next : κ → Option (Basis α)) (bs : List (κ × Basis α))
    (k l : κ) (F H : Basis α) (path : List (TaggedStep κ α)) (P : Delta α)
    (hb : checkedBatch reg bs = some next) (ht : checkedTaggedPath k l F H path = some P) :
    checkedRegisteredPath next k l F H path = some P ↔ Supplies reg bs (RequiredBindings k l F H path) :=
  (recovery_iff_of_tagged next k l F H path P ht).trans
    ((required_bindings_iff next k l F H path).symm.trans
      (requirements_after_batch_iff reg next bs (RequiredBindings k l F H path) hb))

theorem missing_binding_iff {κ : Type v} {α : Type u} [DecidableEq α]
    (reg : κ → Option (Basis α)) (req : List (κ × Basis α)) (b : κ × Basis α) :
    b ∈ missingBindings reg req ↔ b ∈ req ∧ reg b.1 = none := by
  simp only [missingBindings, List.mem_filter, decide_eq_true_eq]

theorem missing_required_in_recovery {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (reg next : κ → Option (Basis α)) (bs : List (κ × Basis α))
    (k l : κ) (F H : Basis α) (path : List (TaggedStep κ α)) (P : Delta α)
    (hb : checkedBatch reg bs = some next) (hp : checkedRegisteredPath next k l F H path = some P)
    (b : κ × Basis α) (hm : b ∈ missingBindings reg (RequiredBindings k l F H path)) :
    b ∈ bs := by
  have h := (missing_binding_iff reg (RequiredBindings k l F H path) b).mp hm
  have hr := (required_bindings_iff next k l F H path).mpr
    ((checked_registered_iff next k l F H path P).mp hp).1
  rcases (binding_after_batch_iff reg next bs b hb).mp (hr b h.1) with ho | hs
  · have impossible : (none : Option (Basis α)) = some b.2 := h.2.symm.trans ho
    cases impossible
  · exact hs

theorem exact_missing_recovers {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (reg next : κ → Option (Basis α)) (bs : List (κ × Basis α))
    (k l : κ) (F H : Basis α) (path : List (TaggedStep κ α)) (P : Delta α)
    (hb : checkedBatch reg bs = some next) (ht : checkedTaggedPath k l F H path = some P)
    (hc : ∀ b ∈ RequiredBindings k l F H path, reg b.1 = none ∨ reg b.1 = some b.2)
    (hm : ∀ b, b ∈ bs ↔ b ∈ missingBindings reg (RequiredBindings k l F H path)) :
    checkedRegisteredPath next k l F H path = some P := by
  apply (checked_batch_recovery_iff reg next bs k l F H path P hb ht).mpr
  intro b h
  rcases hc b h with hn | ho
  · exact Or.inr ((hm b).mpr ((missing_binding_iff reg (RequiredBindings k l F H path) b).mpr ⟨h,hn⟩))
  · exact Or.inl ho

theorem conflicting_requirement_no_extension {κ : Type v} {α : Type u}
    (reg next : κ → Option (Basis α)) (req : List (κ × Basis α)) (b : κ × Basis α) (G : Basis α)
    (he : RegistryExtends reg next) (hm : b ∈ req) (ho : reg b.1 = some G) (hne : G ≠ b.2) :
    ¬ CoversBindings next req := by
  intro hc
  exact hne (registered_binding_unique next b.1 G b.2 (he b.1 G ho) (hc b hm))

theorem inconsistent_requirements_no_registry {κ : Type v} {α : Type u}
    (reg : κ → Option (Basis α)) (req : List (κ × Basis α)) (b c : κ × Basis α)
    (hb : b ∈ req) (hc : c ∈ req) (he : b.1 = c.1) (hne : b.2 ≠ c.2) :
    ¬ CoversBindings reg req := by
  intro hv
  have hc' : reg b.1 = some c.2 := by
    rw [he]
    exact hv c hc
  exact hne (registered_binding_unique reg b.1 b.2 c.2 (hv b hb) hc')

theorem conflicting_path_hold {κ : Type v} {α : Type u} [DecidableEq κ] [DecidableEq α]
    (reg next : κ → Option (Basis α)) (k l : κ) (F H : Basis α)
    (path : List (TaggedStep κ α)) (b : κ × Basis α) (G : Basis α)
    (he : RegistryExtends reg next) (hm : b ∈ RequiredBindings k l F H path)
    (ho : reg b.1 = some G) (hne : G ≠ b.2) :
    checkedRegisteredPath next k l F H path = none := by
  cases hs : checkedRegisteredPath next k l F H path with
  | none => rfl
  | some P =>
      exact False.elim (conflicting_requirement_no_extension reg next (RequiredBindings k l F H path)
        b G he hm ho hne ((required_bindings_iff next k l F H path).mpr
          ((checked_registered_iff next k l F H path P).mp hs).1))

end KuuOSR75
