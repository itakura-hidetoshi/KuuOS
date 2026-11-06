import KUOS.Architecture.QiWuxingGK5CHP77DirectNormalAssociativityUnitsV4_80

/-!
Qi v4.81 — ACTUAL FINITE TYPED DIRECT FRONT-NORMAL CHAINS.
Every link is an original FrontNormal with the real intermediate Family and
partial State as dependent indices. Concatenation retains the actual links.
The chosen right fold has the same full-domain observations as the original
sequential Plan and as composition of separately folded chains.
Actual GK5CG five-cell Type values are retained separately, not identified.
No injective normalization, strict word associativity, or higher cell is claimed.
Append-only, tighten-only, same-root; strict 空 center; Kuu is presentation.
Lean v4.30.0-rc2 / mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Public roots107; protected validation-only #1558 stays Draft/open/unmerged.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace KUOS.Architecture.WuxingPentagonUnified
open KUOS.Architecture.WuxingCyclicPaths
open Kuu.F112.Physical
open CategoryTheory

set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {p : Polygon} {a b : D} {x y : E}
variable {n n' m m' : Nat}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}
variable {first : KuuNativeF45Tree p n m ma pa mb pb}
variable {last : KuuNativeF45Tree p n' m' ma pa mb pb}
variable {r₀ r₁ r₂ r₃ r₄ :
  KuuNativeF45Tree.DepthRotationRoute p first last}
variable
  (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₀ r₁)
  (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₁ r₂)
  (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₂ r₃)
  (k : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₃ r₄)

namespace FivefoldP77FiniteRefinement

/-- A genuine finite chain, with ALL intermediate Family, partial State,
route word and transported finite Schedule values retained in its Type.
An empty chain exists at any partial state; no reachability is postulated. -/
inductive DirectNormalChain
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₀ r₁)
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₁ r₂)
    (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₂ r₃)
    (k : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r₃ r₄)
    {u v : FivefoldPathVertex} :
    (source : Family f g h k u v) → State f g h k source →
    (target : Family f g h k u v) → State f g h k target →
      Type (max (max (max (max uD uE) vD) vE) 1)
  | nil (family : Family f g h k u v) (s : State f g h k family) :
      DirectNormalChain f g h k family s family s
  | cons {source middle target : Family f g h k u v}
      {s : State f g h k source} {m : State f g h k middle}
      {t : State f g h k target}
      (normal : FrontNormal f g h k source s middle m)
      (rest : DirectNormalChain f g h k middle m target t) :
      DirectNormalChain f g h k source s target t

/-- Compile the complete ACTUAL chain to the old original Plan Type,
retaining its selected normal plans and their original GK5CG five-cells. -/
def directChainPlan {u v : FivefoldPathVertex}
    {source target : Family f g h k u v}
    {s : State f g h k source} {t : State f g h k target}
    (chain : DirectNormalChain f g h k source s target t) :
    FivefoldP77RawPatchRefinementPlan f g h k
      (tree f g h k source s) (tree f g h k target t) := by
  induction chain with
  | nil family state =>
      exact .presentation (.recut (.refl (tree f g h k family state)))
  | cons normal rest ih =>
      exact .trans (frontPlan f g h k normal) ih

/-- Right-associated direct fold of the actual finite chain.
The ending unit is the original reflexive recut and empty Schedule.
Its Type value is kept separately from the chain and from its Plan. -/
def directChainFold {u v : FivefoldPathVertex}
    {source target : Family f g h k u v}
    {s : State f g h k source} {t : State f g h k target}
    (chain : DirectNormalChain f g h k source s target t) :
    FrontNormal f g h k source s target t := by
  induction chain with
  | nil family state =>
      exact directNormalUnit f g h k family state
  | cons normal rest ih =>
      exact directComposeFrontNormal f g h k normal ih

/-- An original single normal as a one-element true typed chain. -/
def directChainSingleton {u v : FivefoldPathVertex}
    {source target : Family f g h k u v}
    {s : State f g h k source} {t : State f g h k target}
    (normal : FrontNormal f g h k source s target t) :
    DirectNormalChain f g h k source s target t :=
  .cons normal (.nil target t)

/-- A single actual normal is observed unchanged after the chosen fold.
Its folded normal Type value is not identified with the original normal. -/
theorem directChainSingleton_observed {u v : FivefoldPathVertex}
    {source target : Family f g h k u v}
    {s : State f g h k source} {t : State f g h k target}
    (normal : FrontNormal f g h k source s target t) :
    PlanObservedEq f g h k
      (frontPlan f g h k (directChainFold f g h k
        (directChainSingleton f g h k normal)))
      (frontPlan f g h k normal) :=
  directCompose_rightUnit_observed f g h k normal

/-- EVERY finite chain has the full-domain original Plan observations of its
direct right-associated normal fold, without source-witness subsingletonness. -/
theorem directChainFold_observed {u v : FivefoldPathVertex}
    {source target : Family f g h k u v}
    {s : State f g h k source} {t : State f g h k target}
    (chain : DirectNormalChain f g h k source s target t) :
    PlanObservedEq f g h k
      (frontPlan f g h k (directChainFold f g h k chain))
      (directChainPlan f g h k chain) := by
  induction chain with
  | nil family state =>
      exact directNormalUnit_observed f g h k family state
  | cons normal rest ih =>
      exact planObservedEq_trans f g h k
        (directComposeFrontNormal_observed f g h k normal
          (directChainFold f g h k rest))
        (planObservedEq_comp f g h k
          (planObservedEq_refl f g h k (frontPlan f g h k normal)) ih)

/-- Concatenate original finite chains at an EXACT shared Family and State,
without reconstructing normal words, erasing routes or quotienting histories. -/
def directChainAppend {u v : FivefoldPathVertex}
    {source middle : Family f g h k u v}
    {s : State f g h k source} {m : State f g h k middle}
    (firstChain : DirectNormalChain f g h k source s middle m) :
    ∀ {target : Family f g h k u v} {t : State f g h k target},
      DirectNormalChain f g h k middle m target t →
        DirectNormalChain f g h k source s target t := by
  induction firstChain with
  | nil family state =>
      intro target t secondChain
      exact secondChain
  | cons normal rest ih =>
      intro target t secondChain
      exact .cons normal (ih secondChain)

/-- An empty original chain is a strict LEFT unit for chain concatenation. -/
theorem directChainAppend_nil_left {u v : FivefoldPathVertex}
    {source target : Family f g h k u v}
    {s : State f g h k source} {t : State f g h k target}
    (chain : DirectNormalChain f g h k source s target t) :
    directChainAppend f g h k (.nil source s) chain = chain := rfl

/-- Empty original chain is a strict RIGHT unit for the chain syntax alone.
This does not assert a strict unit law for the folded FrontNormal values. -/
theorem directChainAppend_nil_right {u v : FivefoldPathVertex}
    {source target : Family f g h k u v}
    {s : State f g h k source} {t : State f g h k target}
    (chain : DirectNormalChain f g h k source s target t) :
    directChainAppend f g h k chain (.nil target t) = chain := by
  induction chain with
  | nil family state => rfl
  | cons normal rest ih =>
      exact congrArg (fun tail => DirectNormalChain.cons normal tail) ih

/-- Original finite chain append is strictly associative as a CHAIN value.
No strict associativity of its front normal fold or GK5CG history follows. -/
theorem directChainAppend_assoc {u v : FivefoldPathVertex}
    {family₀ family₁ family₂ family₃ : Family f g h k u v}
    {s₀ : State f g h k family₀} {s₁ : State f g h k family₁}
    {s₂ : State f g h k family₂} {s₃ : State f g h k family₃}
    (C₁ : DirectNormalChain f g h k family₀ s₀ family₁ s₁)
    (C₂ : DirectNormalChain f g h k family₁ s₁ family₂ s₂)
    (C₃ : DirectNormalChain f g h k family₂ s₂ family₃ s₃) :
    directChainAppend f g h k (directChainAppend f g h k C₁ C₂) C₃ =
      directChainAppend f g h k C₁ (directChainAppend f g h k C₂ C₃) := by
  induction C₁ with
  | nil family state => rfl
  | cons normal rest ih =>
      exact congrArg (fun tail => DirectNormalChain.cons normal tail) ih

/-- Concatenation of ACTUAL finite chains compiles to sequential original
plans up to full-domain observations; its nil case uses the original recut. -/
theorem directChainPlan_append_observed {u v : FivefoldPathVertex}
    {source middle : Family f g h k u v}
    {s : State f g h k source} {m : State f g h k middle}
    (firstChain : DirectNormalChain f g h k source s middle m) :
    ∀ {target : Family f g h k u v} {t : State f g h k target}
      (secondChain : DirectNormalChain f g h k middle m target t),
      PlanObservedEq f g h k
        (directChainPlan f g h k (directChainAppend f g h k firstChain secondChain))
        (.trans (directChainPlan f g h k firstChain)
          (directChainPlan f g h k secondChain)) := by
  induction firstChain with
  | nil family state =>
      intro target t secondChain
      exact planObservedEq_symm f g h k
        (planObservedEq_left_refl f g h k
          (directChainPlan f g h k secondChain))
  | cons normal rest ih =>
      intro target t secondChain
      exact planObservedEq_trans f g h k
        (planObservedEq_comp f g h k
          (planObservedEq_refl f g h k (frontPlan f g h k normal))
          (ih secondChain))
        (planObservedEq_symm f g h k (planObservedEq_assoc f g h k _ _ _))

/-- MAIN finite-chain coherence. Folding a concatenated true chain and
directly composing two individually folded chains agree on every original
forward/backward raw index and every genuine source witness pullback. -/
theorem directChainFold_append_observed {u v : FivefoldPathVertex}
    {source middle target : Family f g h k u v}
    {s : State f g h k source} {m : State f g h k middle}
    {t : State f g h k target}
    (firstChain : DirectNormalChain f g h k source s middle m)
    (secondChain : DirectNormalChain f g h k middle m target t) :
    PlanObservedEq f g h k
      (frontPlan f g h k (directChainFold f g h k
        (directChainAppend f g h k firstChain secondChain)))
      (frontPlan f g h k (directComposeFrontNormal f g h k
        (directChainFold f g h k firstChain)
        (directChainFold f g h k secondChain))) := by
  have hWhole := directChainFold_observed f g h k
    (directChainAppend f g h k firstChain secondChain)
  have hAppend := directChainPlan_append_observed f g h k firstChain secondChain
  have hParts := planObservedEq_comp f g h k
    (planObservedEq_symm f g h k (directChainFold_observed f g h k firstChain))
    (planObservedEq_symm f g h k (directChainFold_observed f g h k secondChain))
  have hCompose := directComposeFrontNormal_observed f g h k
    (directChainFold f g h k firstChain)
    (directChainFold f g h k secondChain)
  exact planObservedEq_trans f g h k hWhole
    (planObservedEq_trans f g h k hAppend
      (planObservedEq_trans f g h k hParts
        (planObservedEq_symm f g h k hCompose)))

section ChainConsequences
variable {u v : FivefoldPathVertex}
variable {source target : Family f g h k u v}
variable {s : State f g h k source} {t : State f g h k target}
variable (chain : DirectNormalChain f g h k source s target t)

/-- Target raw indices agree on their ENTIRE domain. -/
theorem directChainFold_forward
    (i : FivefoldP77RawPatchTreeIndex f g h k (tree f g h k target t)) :
    (fivefoldP77RawPatchRefinementPlanRawComparison f g h k
      (frontPlan f g h k (directChainFold f g h k chain))).forwardIndex i =
    (fivefoldP77RawPatchRefinementPlanRawComparison f g h k
      (directChainPlan f g h k chain)).forwardIndex i :=
  (directChainFold_observed f g h k chain).forward i

/-- Source raw indices agree on their ENTIRE domain, without inverse coverage. -/
theorem directChainFold_backward
    (i : FivefoldP77RawPatchTreeIndex f g h k (tree f g h k source s)) :
    (fivefoldP77RawPatchRefinementPlanRawComparison f g h k
      (frontPlan f g h k (directChainFold f g h k chain))).backwardIndex i =
    (fivefoldP77RawPatchRefinementPlanRawComparison f g h k
      (directChainPlan f g h k chain)).backwardIndex i :=
  (directChainFold_observed f g h k chain).backward i

/-- The two plans reconstruct the SAME genuine original source Type value. -/
theorem directChainFold_pullback
    (witness : FivefoldP77RawPatchTreeWitness f g h k (tree f g h k target t)) :
    fivefoldP77RawPatchRefinementPlanPullback f g h k
      (frontPlan f g h k (directChainFold f g h k chain)) witness =
    fivefoldP77RawPatchRefinementPlanPullback f g h k
      (directChainPlan f g h k chain) witness :=
  (directChainFold_observed f g h k chain).pullback witness

/-- Both ACTUAL original GK5CG five-cell values survive independently. -/
def directChainFold_rawSquare
    (i : FivefoldP77RawPatchTreeIndex f g h k (tree f g h k target t)) :=
  planRawSquare f g h k
    (frontPlan f g h k (directChainFold f g h k chain))
    (directChainPlan f g h k chain)
    (directChainFold_forward f g h k chain) i

/-- The original loop may be nontrivial; no higher-cell filling is claimed. -/
def directChainFold_rawLoop
    (i : FivefoldP77RawPatchTreeIndex f g h k (tree f g h k target t)) :=
  planRawLoop f g h k
    (frontPlan f g h k (directChainFold f g h k chain))
    (directChainPlan f g h k chain)
    (directChainFold_forward f g h k chain) i

/-- The original source paths are unchanged along either complete chain plan. -/
theorem directChainFold_path
    (witness : FivefoldP77RawPatchTreeWitness f g h k (tree f g h k target t)) :
    (fivefoldP77RawPatchTreePath f g h k (tree f g h k source s)
      (fivefoldP77RawPatchRefinementPlanPullback f g h k
        (frontPlan f g h k (directChainFold f g h k chain)) witness) =
      fivefoldP77RawPatchTreePath f g h k (tree f g h k target t) witness) ∧
    (fivefoldP77RawPatchTreePath f g h k (tree f g h k source s)
      (fivefoldP77RawPatchRefinementPlanPullback f g h k
        (directChainPlan f g h k chain) witness) =
      fivefoldP77RawPatchTreePath f g h k (tree f g h k target t) witness) :=
  ⟨fivefoldP77RawPatchRefinementPlanPullback_path f g h k _ witness,
    fivefoldP77RawPatchRefinementPlanPullback_path f g h k _ witness⟩

/-- The ORIGINAL source-certified P77 partial Hom survives both complete plans. -/
theorem directChainFold_certified
    (witness : FivefoldP77RawPatchTreeWitness f g h k (tree f g h k target t)) :
    (fivefoldP77RawPatchTreeCertified f g h k (tree f g h k source s)
      (fivefoldP77RawPatchRefinementPlanPullback f g h k
        (frontPlan f g h k (directChainFold f g h k chain)) witness) =
      fivefoldP77RawPatchTreeCertified f g h k (tree f g h k target t) witness) ∧
    (fivefoldP77RawPatchTreeCertified f g h k (tree f g h k source s)
      (fivefoldP77RawPatchRefinementPlanPullback f g h k
        (directChainPlan f g h k chain) witness) =
      fivefoldP77RawPatchTreeCertified f g h k (tree f g h k target t) witness) :=
  ⟨fivefoldP77RawPatchRefinementPlanPullback_certified f g h k _ witness,
    fivefoldP77RawPatchRefinementPlanPullback_certified f g h k _ witness⟩

/-- Certification retains each SAME side's chosen raw comparison and five-cells. -/
theorem directChainFold_certify_raw
    (witness : FivefoldP77RawPatchTreeWitness f g h k (tree f g h k target t)) :
    (fivefoldP77RawPatchSubdivisionRouteRawComparison f g h k
      (fivefoldP77RawPatchRefinementPlanCertify f g h k
        (frontPlan f g h k (directChainFold f g h k chain)) witness) =
      fivefoldP77RawPatchRefinementPlanRawComparison f g h k
        (frontPlan f g h k (directChainFold f g h k chain))) ∧
    (fivefoldP77RawPatchSubdivisionRouteRawComparison f g h k
      (fivefoldP77RawPatchRefinementPlanCertify f g h k
        (directChainPlan f g h k chain) witness) =
      fivefoldP77RawPatchRefinementPlanRawComparison f g h k
        (directChainPlan f g h k chain)) :=
  ⟨fivefoldP77RawPatchRefinementPlanCertify_raw f g h k _ witness,
    fivefoldP77RawPatchRefinementPlanCertify_raw f g h k _ witness⟩

/-- All intermediate compatibility requirements of either Plan are exactly
the compatibility of the COMMON FINAL factor tree, even at partial states. -/
theorem directChainFold_allCompatible_iff :
    (fivefoldP77RawPatchRefinementPlanAllCompatible f g h k
      (frontPlan f g h k (directChainFold f g h k chain)) ↔
      fivefoldP77RawPatchTreeCompatible f g h k (tree f g h k target t)) ∧
    (fivefoldP77RawPatchRefinementPlanAllCompatible f g h k
      (directChainPlan f g h k chain) ↔
      fivefoldP77RawPatchTreeCompatible f g h k (tree f g h k target t)) :=
  ⟨fivefoldP77RawPatchRefinementPlan_allCompatible_iff f g h k _,
    fivefoldP77RawPatchRefinementPlan_allCompatible_iff f g h k _⟩

/-- Final-factor obstruction equivalently obstructs either entire Plan.
No claim of obstruction invariance through an arbitrary refinement step. -/
theorem directChainFold_obstructed_iff :
    (¬ fivefoldP77RawPatchRefinementPlanAllCompatible f g h k
      (frontPlan f g h k (directChainFold f g h k chain)) ↔
      fivefoldP77RawPatchTreeObstructed f g h k (tree f g h k target t)) ∧
    (¬ fivefoldP77RawPatchRefinementPlanAllCompatible f g h k
      (directChainPlan f g h k chain) ↔
      fivefoldP77RawPatchTreeObstructed f g h k (tree f g h k target t)) :=
  ⟨fivefoldP77RawPatchRefinementPlan_obstructed_iff f g h k _,
    fivefoldP77RawPatchRefinementPlan_obstructed_iff f g h k _⟩

end ChainConsequences

/- An anonymous empty-chain regression at an arbitrary (possibly partial) state. -/
example {u v : FivefoldPathVertex} (family : Family f g h k u v)
    (s : State f g h k family) :
    PlanObservedEq f g h k
      (frontPlan f g h k
        (directChainFold f g h k (DirectNormalChain.nil family s)))
      (directChainPlan f g h k (DirectNormalChain.nil family s)) :=
  directChainFold_observed f g h k (.nil family s)

#print axioms DirectNormalChain
#print axioms directChainPlan
#print axioms directChainFold
#print axioms directChainSingleton
#print axioms directChainSingleton_observed
#print axioms directChainFold_observed
#print axioms directChainAppend
#print axioms directChainAppend_nil_left
#print axioms directChainAppend_nil_right
#print axioms directChainAppend_assoc
#print axioms directChainPlan_append_observed
#print axioms directChainFold_append_observed
#print axioms directChainFold_forward
#print axioms directChainFold_backward
#print axioms directChainFold_pullback
#print axioms directChainFold_rawSquare
#print axioms directChainFold_rawLoop
#print axioms directChainFold_path
#print axioms directChainFold_certified
#print axioms directChainFold_certify_raw
#print axioms directChainFold_allCompatible_iff
#print axioms directChainFold_obstructed_iff

end FivefoldP77FiniteRefinement
end
end KUOS.Architecture.WuxingPentagonUnified
