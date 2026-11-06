import KUOS.Architecture.QiWuxingGK5CHP77DirectFrontNormalCompositionV4_79

/-!
Qi v4.80 — DIRECT FRONT-NORMAL ASSOCIATIVITY AND UNITS.
For genuine typed partial states and actual reassociation / refinement data,
direct front-normal composition is observationally associative and unital.
All forward/backward raw indices and actual source witness pullbacks agree.
Original GK5CG five-cell Type values and loops are retained separately:
NO strict equality of normal words, raw five-cell histories, or higher cells.
Append-only, tighten-only, same-root; strict 空 center; Kuu = presentation.
Lean v4.30.0-rc2 / mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Canonical public roots 107; validation-only PR #1558 remains Draft/open.
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

/-- The ORIGINAL reassociation reflexivity and empty genuine Schedule.
This is a typed normal value at ANY partial state, not a quotient identity. -/
def directNormalUnit {u v : FivefoldPathVertex}
    (family : Family f g h k u v) (s : State f g h k family) :
    FrontNormal f g h k family s family s :=
  ⟨.refl family, .nil family s⟩

/-- The selected reflexive route is the genuine ReassocRoute constructor. -/
theorem directNormalUnit_route {u v : FivefoldPathVertex}
    (family : Family f g h k u v) (s : State f g h k family) :
    (directNormalUnit f g h k family s).route = .refl family := rfl

/-- The selected empty Schedule retains its original Type value. -/
theorem directNormalUnit_schedule {u v : FivefoldPathVertex}
    (family : Family f g h k u v) (s : State f g h k family) :
    (directNormalUnit f g h k family s).schedule = .nil family s := rfl

/-- The actual unit normal has the observations of the ORIGINAL reflexive
recut. Two concrete recut-refl plan constructors are not conflated with
the single recut-refl constructor; only their observations are related. -/
theorem directNormalUnit_observed {u v : FivefoldPathVertex}
    (family : Family f g h k u v) (s : State f g h k family) :
    PlanObservedEq f g h k
      (frontPlan f g h k (directNormalUnit f g h k family s))
      (.presentation (.recut (.refl (tree f g h k family s)))) := by
  change PlanObservedEq f g h k
    (.trans (.presentation (.recut (.refl (tree f g h k family s))))
      (.presentation (.recut (.refl (tree f g h k family s)))))
    (.presentation (.recut (.refl (tree f g h k family s))))
  exact planObservedEq_left_refl f g h k _

section UnitLaws
variable {u v : FivefoldPathVertex}
variable {source target : Family f g h k u v}
variable {s : State f g h k source} {t : State f g h k target}
variable (N : FrontNormal f g h k source s target t)

/-- A source-state identity is a LEFT unit on the entire original raw
index and source-witness observation domains, not on normal-form syntax. -/
theorem directCompose_leftUnit_observed :
    PlanObservedEq f g h k
      (frontPlan f g h k (directComposeFrontNormal f g h k
        (directNormalUnit f g h k source s) N))
      (frontPlan f g h k N) := by
  have hComposite := directComposeFrontNormal_observed f g h k
    (directNormalUnit f g h k source s) N
  have hUnit := planObservedEq_comp f g h k
    (directNormalUnit_observed f g h k source s)
    (planObservedEq_refl f g h k (frontPlan f g h k N))
  exact planObservedEq_trans f g h k hComposite
    (planObservedEq_trans f g h k hUnit
      (planObservedEq_left_refl f g h k (frontPlan f g h k N)))

/-- A target-state identity is a RIGHT unit on the three entire domains. -/
theorem directCompose_rightUnit_observed :
    PlanObservedEq f g h k
      (frontPlan f g h k (directComposeFrontNormal f g h k N
        (directNormalUnit f g h k target t)))
      (frontPlan f g h k N) := by
  have hComposite := directComposeFrontNormal_observed f g h k N
    (directNormalUnit f g h k target t)
  have hUnit := planObservedEq_comp f g h k
    (planObservedEq_refl f g h k (frontPlan f g h k N))
    (directNormalUnit_observed f g h k target t)
  exact planObservedEq_trans f g h k hComposite
    (planObservedEq_trans f g h k hUnit
      (planObservedEq_right_refl f g h k (frontPlan f g h k N)))

/-- Left identity also agrees with the ORIGINAL interleaved history plan. -/
theorem directCompose_leftUnit_history
    (H : InterleavedHistory f g h k source s target t) :
    PlanObservedEq f g h k
      (frontPlan f g h k
        (directComposeFrontNormal f g h k
          (directNormalUnit f g h k source s) (normalizeFront f g h k H)))
      (historyPlan f g h k H) :=
  planObservedEq_trans f g h k
    (directCompose_leftUnit_observed f g h k (normalizeFront f g h k H))
    (planObservedEq_symm f g h k (normalizeFront_observed f g h k H))

/-- Right identity also agrees with the ORIGINAL typed history plan. -/
theorem directCompose_rightUnit_history
    (H : InterleavedHistory f g h k source s target t) :
    PlanObservedEq f g h k
      (frontPlan f g h k
        (directComposeFrontNormal f g h k
          (normalizeFront f g h k H) (directNormalUnit f g h k target t)))
      (historyPlan f g h k H) :=
  planObservedEq_trans f g h k
    (directCompose_rightUnit_observed f g h k (normalizeFront f g h k H))
    (planObservedEq_symm f g h k (normalizeFront_observed f g h k H))

end UnitLaws

/-- The direct composite descends to its full-domain observational relation,
WITHOUT taking a quotient of its actual Type-valued data. -/
theorem directCompose_observed_congr {u v : FivefoldPathVertex}
    {source middle target : Family f g h k u v}
    {s : State f g h k source} {m : State f g h k middle}
    {t : State f g h k target}
    (N₁ N₁' : FrontNormal f g h k source s middle m)
    (N₂ N₂' : FrontNormal f g h k middle m target t)
    (sameFirst : PlanObservedEq f g h k
      (frontPlan f g h k N₁) (frontPlan f g h k N₁'))
    (sameSecond : PlanObservedEq f g h k
      (frontPlan f g h k N₂) (frontPlan f g h k N₂')) :
    PlanObservedEq f g h k
      (frontPlan f g h k (directComposeFrontNormal f g h k N₁ N₂))
      (frontPlan f g h k (directComposeFrontNormal f g h k N₁' N₂')) :=
  planObservedEq_trans f g h k
    (directComposeFrontNormal_observed f g h k N₁ N₂)
    (planObservedEq_trans f g h k
      (planObservedEq_comp f g h k sameFirst sameSecond)
      (planObservedEq_symm f g h k
        (directComposeFrontNormal_observed f g h k N₁' N₂')))

section Associativity
variable {u v : FivefoldPathVertex}
variable {family₀ family₁ family₂ family₃ : Family f g h k u v}
variable {s₀ : State f g h k family₀}
variable {s₁ : State f g h k family₁}
variable {s₂ : State f g h k family₂}
variable {s₃ : State f g h k family₃}
variable (N₁ : FrontNormal f g h k family₀ s₀ family₁ s₁)
variable (N₂ : FrontNormal f g h k family₁ s₁ family₂ s₂)
variable (N₃ : FrontNormal f g h k family₂ s₂ family₃ s₃)

/-- Preserve the first actual parenthesized Type-valued composition. -/
def directAssocLeft : FrontNormal f g h k family₀ s₀ family₃ s₃ :=
  directComposeFrontNormal f g h k
    (directComposeFrontNormal f g h k N₁ N₂) N₃

/-- Preserve the second actual parenthesized Type-valued composition. -/
def directAssocRight : FrontNormal f g h k family₀ s₀ family₃ s₃ :=
  directComposeFrontNormal f g h k N₁
    (directComposeFrontNormal f g h k N₂ N₃)

/-- Explicitly retain the original left-associated ReassocRoute word. -/
theorem directAssocLeft_route :
    (directAssocLeft f g h k N₁ N₂ N₃).route =
      .trans (.trans N₁.route N₂.route) N₃.route := rfl

/-- The other original ReassocRoute word remains a DIFFERENT Type value. -/
theorem directAssocRight_route :
    (directAssocRight f g h k N₁ N₂ N₃).route =
      .trans N₁.route (.trans N₂.route N₃.route) := rfl

/-- MAIN v4.80: two genuine ways of parenthesizing three direct normals
are identical on ALL raw forward/backward indices and genuine Type-valued
source witness pullback, without asserting route/normal/five-cell equality. -/
theorem directCompose_assoc_observed :
    PlanObservedEq f g h k
      (frontPlan f g h k (directAssocLeft f g h k N₁ N₂ N₃))
      (frontPlan f g h k (directAssocRight f g h k N₁ N₂ N₃)) := by
  have hL := directComposeFrontNormal_observed f g h k
    (directComposeFrontNormal f g h k N₁ N₂) N₃
  have hAB := directComposeFrontNormal_observed f g h k N₁ N₂
  have hL' := planObservedEq_comp f g h k hAB
    (planObservedEq_refl f g h k (frontPlan f g h k N₃))
  have hAssoc := planObservedEq_assoc f g h k
    (frontPlan f g h k N₁) (frontPlan f g h k N₂) (frontPlan f g h k N₃)
  have hBC := directComposeFrontNormal_observed f g h k N₂ N₃
  have hR' := planObservedEq_comp f g h k
    (planObservedEq_refl f g h k (frontPlan f g h k N₁))
    (planObservedEq_symm f g h k hBC)
  have hR := directComposeFrontNormal_observed f g h k N₁
    (directComposeFrontNormal f g h k N₂ N₃)
  have hAll := planObservedEq_trans f g h k hL
    (planObservedEq_trans f g h k hL'
      (planObservedEq_trans f g h k hAssoc
        (planObservedEq_trans f g h k hR'
          (planObservedEq_symm f g h k hR))))
  simpa only [directAssocLeft, directAssocRight] using hAll

/-- The ORIGINAL forward maps agree at EVERY final raw index. -/
theorem directCompose_assoc_forward
    (i : FivefoldP77RawPatchTreeIndex f g h k (tree f g h k family₃ s₃)) :
    (fivefoldP77RawPatchRefinementPlanRawComparison f g h k
      (frontPlan f g h k (directAssocLeft f g h k N₁ N₂ N₃))).forwardIndex i =
    (fivefoldP77RawPatchRefinementPlanRawComparison f g h k
      (frontPlan f g h k (directAssocRight f g h k N₁ N₂ N₃))).forwardIndex i :=
  (directCompose_assoc_observed f g h k N₁ N₂ N₃).forward i

/-- The separately retained backward maps agree at EVERY initial index. -/
theorem directCompose_assoc_backward
    (i : FivefoldP77RawPatchTreeIndex f g h k (tree f g h k family₀ s₀)) :
    (fivefoldP77RawPatchRefinementPlanRawComparison f g h k
      (frontPlan f g h k (directAssocLeft f g h k N₁ N₂ N₃))).backwardIndex i =
    (fivefoldP77RawPatchRefinementPlanRawComparison f g h k
      (frontPlan f g h k (directAssocRight f g h k N₁ N₂ N₃))).backwardIndex i :=
  (directCompose_assoc_observed f g h k N₁ N₂ N₃).backward i

/-- The SAME genuine original source Type value is reconstructed at each witness. -/
theorem directCompose_assoc_pullback
    (witness : FivefoldP77RawPatchTreeWitness f g h k (tree f g h k family₃ s₃)) :
    fivefoldP77RawPatchRefinementPlanPullback f g h k
      (frontPlan f g h k (directAssocLeft f g h k N₁ N₂ N₃)) witness =
    fivefoldP77RawPatchRefinementPlanPullback f g h k
      (frontPlan f g h k (directAssocRight f g h k N₁ N₂ N₃)) witness :=
  (directCompose_assoc_observed f g h k N₁ N₂ N₃).pullback witness

/-- Two ORIGINAL five-cell values are retained with their endpoints aligned. -/
def directCompose_assoc_rawSquare
    (i : FivefoldP77RawPatchTreeIndex f g h k (tree f g h k family₃ s₃)) :=
  planRawSquare f g h k
    (frontPlan f g h k (directAssocLeft f g h k N₁ N₂ N₃))
    (frontPlan f g h k (directAssocRight f g h k N₁ N₂ N₃))
    (directCompose_assoc_forward f g h k N₁ N₂ N₃) i

/-- The ORIGINAL loop is present; no triviality or new higher coherence cell. -/
def directCompose_assoc_rawLoop
    (i : FivefoldP77RawPatchTreeIndex f g h k (tree f g h k family₃ s₃)) :=
  planRawLoop f g h k
    (frontPlan f g h k (directAssocLeft f g h k N₁ N₂ N₃))
    (frontPlan f g h k (directAssocRight f g h k N₁ N₂ N₃))
    (directCompose_assoc_forward f g h k N₁ N₂ N₃) i

/-- Both genuine sides preserve the ORIGINAL source path. -/
theorem directCompose_assoc_path
    (witness : FivefoldP77RawPatchTreeWitness f g h k (tree f g h k family₃ s₃)) :
    (fivefoldP77RawPatchTreePath f g h k (tree f g h k family₀ s₀)
      (fivefoldP77RawPatchRefinementPlanPullback f g h k
        (frontPlan f g h k (directAssocLeft f g h k N₁ N₂ N₃)) witness) =
      fivefoldP77RawPatchTreePath f g h k (tree f g h k family₃ s₃) witness) ∧
    (fivefoldP77RawPatchTreePath f g h k (tree f g h k family₀ s₀)
      (fivefoldP77RawPatchRefinementPlanPullback f g h k
        (frontPlan f g h k (directAssocRight f g h k N₁ N₂ N₃)) witness) =
      fivefoldP77RawPatchTreePath f g h k (tree f g h k family₃ s₃) witness) :=
  ⟨fivefoldP77RawPatchRefinementPlanPullback_path f g h k _ witness,
    fivefoldP77RawPatchRefinementPlanPullback_path f g h k _ witness⟩

/-- Both sides retain the actual source-certified original P77 partial Hom. -/
theorem directCompose_assoc_certified
    (witness : FivefoldP77RawPatchTreeWitness f g h k (tree f g h k family₃ s₃)) :
    (fivefoldP77RawPatchTreeCertified f g h k (tree f g h k family₀ s₀)
      (fivefoldP77RawPatchRefinementPlanPullback f g h k
        (frontPlan f g h k (directAssocLeft f g h k N₁ N₂ N₃)) witness) =
      fivefoldP77RawPatchTreeCertified f g h k (tree f g h k family₃ s₃) witness) ∧
    (fivefoldP77RawPatchTreeCertified f g h k (tree f g h k family₀ s₀)
      (fivefoldP77RawPatchRefinementPlanPullback f g h k
        (frontPlan f g h k (directAssocRight f g h k N₁ N₂ N₃)) witness) =
      fivefoldP77RawPatchTreeCertified f g h k (tree f g h k family₃ s₃) witness) :=
  ⟨fivefoldP77RawPatchRefinementPlanPullback_certified f g h k _ witness,
    fivefoldP77RawPatchRefinementPlanPullback_certified f g h k _ witness⟩

/-- Certification of each ACTUAL side retains that SAME side's chosen raw
comparison and Type-valued five-cell data; the sides are NOT identified. -/
theorem directCompose_assoc_certify_raw
    (witness : FivefoldP77RawPatchTreeWitness f g h k (tree f g h k family₃ s₃)) :
    (fivefoldP77RawPatchSubdivisionRouteRawComparison f g h k
      (fivefoldP77RawPatchRefinementPlanCertify f g h k
        (frontPlan f g h k (directAssocLeft f g h k N₁ N₂ N₃)) witness) =
      fivefoldP77RawPatchRefinementPlanRawComparison f g h k
        (frontPlan f g h k (directAssocLeft f g h k N₁ N₂ N₃))) ∧
    (fivefoldP77RawPatchSubdivisionRouteRawComparison f g h k
      (fivefoldP77RawPatchRefinementPlanCertify f g h k
        (frontPlan f g h k (directAssocRight f g h k N₁ N₂ N₃)) witness) =
      fivefoldP77RawPatchRefinementPlanRawComparison f g h k
        (frontPlan f g h k (directAssocRight f g h k N₁ N₂ N₃))) :=
  ⟨fivefoldP77RawPatchRefinementPlanCertify_raw f g h k _ witness,
    fivefoldP77RawPatchRefinementPlanCertify_raw f g h k _ witness⟩

/-- Both complete Plan compatibility predicates are equivalent to the SAME
actual final factor tree, including partial (not just completed) states. -/
theorem directCompose_assoc_allCompatible_iff :
    (fivefoldP77RawPatchRefinementPlanAllCompatible f g h k
      (frontPlan f g h k (directAssocLeft f g h k N₁ N₂ N₃)) ↔
      fivefoldP77RawPatchTreeCompatible f g h k (tree f g h k family₃ s₃)) ∧
    (fivefoldP77RawPatchRefinementPlanAllCompatible f g h k
      (frontPlan f g h k (directAssocRight f g h k N₁ N₂ N₃)) ↔
      fivefoldP77RawPatchTreeCompatible f g h k (tree f g h k family₃ s₃)) :=
  ⟨fivefoldP77RawPatchRefinementPlan_allCompatible_iff f g h k _,
    fivefoldP77RawPatchRefinementPlan_allCompatible_iff f g h k _⟩

/-- An obstruction at that same final tree obstructs either Plan; intermediate
arbitrary refinements do not magically preserve/erase such obstructions. -/
theorem directCompose_assoc_obstructed_iff :
    (¬ fivefoldP77RawPatchRefinementPlanAllCompatible f g h k
      (frontPlan f g h k (directAssocLeft f g h k N₁ N₂ N₃)) ↔
      fivefoldP77RawPatchTreeObstructed f g h k (tree f g h k family₃ s₃)) ∧
    (¬ fivefoldP77RawPatchRefinementPlanAllCompatible f g h k
      (frontPlan f g h k (directAssocRight f g h k N₁ N₂ N₃)) ↔
      fivefoldP77RawPatchTreeObstructed f g h k (tree f g h k family₃ s₃)) :=
  ⟨fivefoldP77RawPatchRefinementPlan_obstructed_iff f g h k _,
    fivefoldP77RawPatchRefinementPlan_obstructed_iff f g h k _⟩

end Associativity

/- Regression: both unit laws apply to arbitrary partial-state original nil
history; the witness Type is not assumed subsingleton or inhabited. -/
example {u v : FivefoldPathVertex} (family : Family f g h k u v)
    (s : State f g h k family) :
    PlanObservedEq f g h k
      (frontPlan f g h k
        (directComposeFrontNormal f g h k
          (directNormalUnit f g h k family s)
          (normalizeFront f g h k (.nil family s))))
      (historyPlan f g h k (.nil family s)) :=
  directCompose_leftUnit_history f g h k (.nil family s)

example {u v : FivefoldPathVertex} (family : Family f g h k u v)
    (s : State f g h k family) :
    PlanObservedEq f g h k
      (frontPlan f g h k
        (directComposeFrontNormal f g h k
          (normalizeFront f g h k (.nil family s))
          (directNormalUnit f g h k family s)))
      (historyPlan f g h k (.nil family s)) :=
  directCompose_rightUnit_history f g h k (.nil family s)

#print axioms directNormalUnit
#print axioms directNormalUnit_route
#print axioms directNormalUnit_schedule
#print axioms directNormalUnit_observed
#print axioms directCompose_leftUnit_observed
#print axioms directCompose_rightUnit_observed
#print axioms directCompose_leftUnit_history
#print axioms directCompose_rightUnit_history
#print axioms directCompose_observed_congr
#print axioms directAssocLeft
#print axioms directAssocRight
#print axioms directAssocLeft_route
#print axioms directAssocRight_route
#print axioms directCompose_assoc_observed
#print axioms directCompose_assoc_forward
#print axioms directCompose_assoc_backward
#print axioms directCompose_assoc_pullback
#print axioms directCompose_assoc_rawSquare
#print axioms directCompose_assoc_rawLoop
#print axioms directCompose_assoc_path
#print axioms directCompose_assoc_certified
#print axioms directCompose_assoc_certify_raw
#print axioms directCompose_assoc_allCompatible_iff
#print axioms directCompose_assoc_obstructed_iff

end FivefoldP77FiniteRefinement
end
end KUOS.Architecture.WuxingPentagonUnified
