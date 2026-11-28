import Lean

/-!
# VerifyOS v0.14: contextual sound coverage of verification methods

This is an abstract relational specification. Method admission, scope,
observed reports and semantic soundness are distinct inputs. The exact
entailment criterion quantifies over all truth relations satisfying only
the declared positive soundness obligations. It does not characterize
truth in a fixed external model or establish the Python-to-Lean bridge.
-/
namespace KUOS.VerifyOS.MethodSoundCoverageV0_14

set_option autoImplicit false
universe u v w z

section General
variable {I : Type u} {C : Type v} {X : Type w} {V : Type z}

/-- A report supports a value only at its admitted method and actual scope. -/
def Supported (admitted scope : I → C → X → Prop)
    (report : I → C → X → Option V) (ctx : C) (x : X) (y : V) : Prop :=
  ∃ i, admitted i ctx x ∧ scope i ctx x ∧ report i ctx x = some y

/-- The explicit semantic obligation for admitted, in-scope reports. -/
def Honors (admitted scope : I → C → X → Prop)
    (report : I → C → X → Option V) (valid : C → X → V → Prop) : Prop :=
  ∀ i ctx x y, admitted i ctx x → scope i ctx x →
    report i ctx x = some y → valid ctx x y

/-- Entailment relative ONLY to the supplied positive obligations. -/
def Forced (admitted scope : I → C → X → Prop)
    (report : I → C → X → Option V) (ctx : C) (x : X) (y : V) : Prop :=
  ∀ valid : C → X → V → Prop,
    Honors admitted scope report valid → valid ctx x y

def Covers (admitted scope : I → C → X → Prop)
    (ctx : C) (required : X → Prop) : Prop :=
  ∀ x, required x → ∃ i, admitted i ctx x ∧ scope i ctx x

def Agrees (admitted scope : I → C → X → Prop)
    (report : I → C → X → Option V) (ctx : C)
    (required : X → Prop) (answer : X → V) : Prop :=
  ∀ i x, required x → admitted i ctx x → scope i ctx x →
    report i ctx x = some (answer x)

def Functional (valid : C → X → V → Prop) : Prop :=
  ∀ ctx x y z, valid ctx x y → valid ctx x z → y = z

theorem support_sound
    (admitted scope : I → C → X → Prop)
    (report : I → C → X → Option V) (valid : C → X → V → Prop)
    (hSound : Honors admitted scope report valid)
    (ctx : C) (x : X) (y : V)
    (h : Supported admitted scope report ctx x y) :
    valid ctx x y := by
  obtain ⟨i, ha, hs, hr⟩ := h
  exact hSound i ctx x y ha hs hr

/-- The least relation satisfying the declared obligations is support itself. -/
theorem support_honors
    (admitted scope : I → C → X → Prop)
    (report : I → C → X → Option V) :
    Honors admitted scope report (Supported admitted scope report) := by
  intro i ctx x y ha hs hr
  exact ⟨i, ha, hs, hr⟩

theorem forced_iff_supported
    (admitted scope : I → C → X → Prop)
    (report : I → C → X → Option V) (ctx : C) (x : X) (y : V) :
    Forced admitted scope report ctx x y ↔
      Supported admitted scope report ctx x y := by
  constructor
  · intro h
    exact h (Supported admitted scope report) (support_honors admitted scope report)
  · intro h valid hSound
    exact support_sound admitted scope report valid hSound ctx x y h

/-- A missing support is neither a proof nor a refutation in this theory. -/
theorem missing_support_has_two_models
    (admitted scope : I → C → X → Prop)
    (report : I → C → X → Option V) (ctx : C) (x : X) (y : V)
    (h : ¬ Supported admitted scope report ctx x y) :
    (∃ valid : C → X → V → Prop,
      Honors admitted scope report valid ∧ ¬ valid ctx x y) ∧
    (∃ valid : C → X → V → Prop,
      Honors admitted scope report valid ∧ valid ctx x y) := by
  constructor
  · exact ⟨Supported admitted scope report, support_honors admitted scope report, h⟩
  · refine ⟨fun _ _ _ => True, ?_, True.intro⟩
    intro _ _ _ _ _ _ _
    exact True.intro

theorem agreement_and_cover_give_support
    (admitted scope : I → C → X → Prop)
    (report : I → C → X → Option V) (ctx : C)
    (required : X → Prop) (answer : X → V)
    (hAgree : Agrees admitted scope report ctx required answer)
    (hCover : Covers admitted scope ctx required) :
    ∀ x, required x → Supported admitted scope report ctx x (answer x) := by
  intro x hx
  obtain ⟨i, ha, hs⟩ := hCover x hx
  exact ⟨i, ha, hs, hAgree i x hx ha hs⟩

/-- Exact coverage criterion for a compatible answer over arbitrary relations.
The converse is relative to these obligations, not arbitrary extra axioms. -/
theorem full_answer_forced_iff_cover
    (admitted scope : I → C → X → Prop)
    (report : I → C → X → Option V) (ctx : C)
    (required : X → Prop) (answer : X → V)
    (hAgree : Agrees admitted scope report ctx required answer) :
    (∀ valid : C → X → V → Prop,
      Honors admitted scope report valid →
        ∀ x, required x → valid ctx x (answer x)) ↔
      Covers admitted scope ctx required := by
  constructor
  · intro h x hx
    obtain ⟨i, ha, hs, _⟩ :=
      h (Supported admitted scope report) (support_honors admitted scope report) x hx
    exact ⟨i, ha, hs⟩
  · intro hCover valid hSound x hx
    exact support_sound admitted scope report valid hSound ctx x (answer x)
      (agreement_and_cover_give_support admitted scope report ctx required answer hAgree hCover x hx)

/-- Distinct positively supported values obstruct a single-valued model.
This is an incompatibility of the obligations, not a proof of either value. -/
theorem conflicting_support_no_functional_model
    (admitted scope : I → C → X → Prop)
    (report : I → C → X → Option V) (ctx : C) (x : X) (y z : V)
    (hy : Supported admitted scope report ctx x y)
    (hz : Supported admitted scope report ctx x z) (hne : y ≠ z) :
    ¬ ∃ valid : C → X → V → Prop,
      Honors admitted scope report valid ∧ Functional valid := by
  rintro ⟨valid, hs, hf⟩
  exact hne (hf ctx x y z
    (support_sound admitted scope report valid hs ctx x y hy)
    (support_sound admitted scope report valid hs ctx x z hz))

theorem unavailable_reports_no_support
    (admitted scope : I → C → X → Prop)
    (report : I → C → X → Option V) (ctx : C) (x : X) (y : V)
    (h : ∀ i, admitted i ctx x → scope i ctx x → report i ctx x = none) :
    ¬ Supported admitted scope report ctx x y := by
  rintro ⟨i, ha, hs, hr⟩
  have hn : (none : Option V) = some y := (h i ha hs).symm.trans hr
  cases hn

theorem support_mono_admission
    (admitted larger scope : I → C → X → Prop)
    (report : I → C → X → Option V) (ctx : C) (x : X) (y : V)
    (hsub : ∀ i c a, admitted i c a → larger i c a)
    (h : Supported admitted scope report ctx x y) :
    Supported larger scope report ctx x y := by
  obtain ⟨i, ha, hs, hr⟩ := h
  exact ⟨i, hsub i ctx x ha, hs, hr⟩

theorem honors_restrict_scope
    (admitted scope smaller : I → C → X → Prop)
    (report : I → C → X → Option V) (valid : C → X → V → Prop)
    (hSound : Honors admitted scope report valid)
    (hsub : ∀ i c x, smaller i c x → scope i c x) :
    Honors admitted smaller report valid := by
  intro i ctx x y ha hs hr
  exact hSound i ctx x y ha (hsub i ctx x hs) hr

end General

/-- Two genuinely distinct readout functions share the same erroneous value
at the selected context; this is the abstract shape of the v0.13 fixture. -/
def commonErrorReports (method ctx : Bool) (_ : Unit) : Option Nat :=
  if ctx then some (if method then 12 else 13) else some 11

theorem distinct_methods_can_agree_wrong :
    (commonErrorReports false ≠ commonErrorReports true) ∧
    (∀ method : Bool, commonErrorReports method false () = some 11) ∧
    (11 : Nat) ≠ 10 := by
  refine ⟨?_, ?_, by decide⟩
  · intro h
    have he := congrArg (fun f : Bool → Unit → Option Nat => f true ()) h
    have hn : (some 13 : Option Nat) ≠ some 12 := by decide
    exact hn he
  · intro method
    rfl

def exampleScope (_ : Bool) (ctx : Bool) (_ : Unit) : Prop := ctx = false

def exampleTruth (ctx : Bool) (_ : Unit) (y : Nat) : Prop :=
  if ctx then y = 10 else y = 11

/-- Even a sound method on its declared scope need not be sound elsewhere. -/
theorem scoped_soundness_does_not_transport :
    Honors (fun (_ : Bool) (_ : Bool) (_ : Unit) => True)
      exampleScope commonErrorReports exampleTruth ∧
    commonErrorReports true true () = some 12 ∧
    ¬ exampleTruth true () 12 := by
  constructor
  · intro i ctx x y _ hs hr
    have hctx : ctx = false := hs
    subst ctx
    change some (11 : Nat) = some y at hr
    change y = 11
    exact (Option.some.inj hr).symm
  · exact ⟨rfl, by simp [exampleTruth]⟩

#print axioms Supported
#print axioms Honors
#print axioms Forced
#print axioms Covers
#print axioms Agrees
#print axioms Functional
#print axioms support_sound
#print axioms support_honors
#print axioms forced_iff_supported
#print axioms missing_support_has_two_models
#print axioms agreement_and_cover_give_support
#print axioms full_answer_forced_iff_cover
#print axioms conflicting_support_no_functional_model
#print axioms unavailable_reports_no_support
#print axioms support_mono_admission
#print axioms honors_restrict_scope
#print axioms commonErrorReports
#print axioms distinct_methods_can_agree_wrong
#print axioms exampleScope
#print axioms exampleTruth
#print axioms scoped_soundness_does_not_transport

end KUOS.VerifyOS.MethodSoundCoverageV0_14
