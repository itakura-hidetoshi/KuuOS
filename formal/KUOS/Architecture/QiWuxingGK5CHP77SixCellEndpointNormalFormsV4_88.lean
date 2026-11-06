import KUOS.Architecture.QiWuxingGK5CHP77SixCellWordCoherenceDescentV4_87

/-!
Qi v4.88 — GENUINE P77-INDEXED ENDPOINT NORMAL FORMS
AND DEGREE COMPLETENESS OF THE SEPARATELY ADJOINED SIX-CELL GRAMMAR.

Key new result: where the old selected ORIGINAL GK5CG conservative
five-cell values long and short are provably distinct (Qi v4.85),
the v4.87 signed degree of EVERY adjoined six-cell raw proof word
is determined by its endpoints. Thus parallel raw proof words are
degree-coherent, and their classes in the EXPLICITLY CHOSEN new
coherence quotient are unique. Raw proof words are never thereby
identified by strict equality.

A normal representative is one of: refl (same endpoint),
pentagon (long to short), inverse pentagon (short to long).
Existence and class completeness are proved for all inhabitants,
including ALL actual source-indexed P77 raw terminals. There is no
claim of an original F55/P77/GK5CG six-cell, no canonical old equality
return, and no negation of other higher presentations.

Append-only / tighten-only / same-root; strict 空 center,
independent Kuu = presentation. Pinned Lean v4.30.0-rc2,
mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6,
public roots107; protected #1558 Draft/open/unmerged.
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

universe uD vD uE vE uSix
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
namespace PentagonAdjoinedSixCell

variable {W : Type uSix} {long short : W}

/-- Endpoint potential of the NEW presentation; it is not a charge
on the old F55 four-proofs and depends on a CHOSEN short endpoint. -/
def endpointHeight (short w : W) : ℤ :=
  if w = short then 1 else 0

/-- The crucial non-loop theorem. With DISTINCT endpoints, the
degree of an arbitrary raw sixth-dimensional proof word is exactly
the endpoint potential difference, including arbitrarily nested
symmetry and composition. -/
theorem degree_eq_endpointHeight_sub (l r : W) (hNe : l ≠ r)
    {w z : W} (c : PentagonAdjoinedSixCell W l r w z) :
    degree c = endpointHeight r z - endpointHeight r w := by
  induction c with
  | refl w =>
      simp [degree]
  | symm c ih =>
      simp only [degree, ih]
      abel
  | trans c d ihc ihd =>
      simp only [degree, ihc, ihd]
      abel
  | pentagon =>
      simp [degree, endpointHeight, hNe]

/-- All parallel NEW raw proof words have the same signed degree
when the two adjoined original endpoints are distinct. -/
theorem allParallel_degreeCoherent (l r : W) (hNe : l ≠ r)
    {w z : W}
    (c d : PentagonAdjoinedSixCell W l r w z) :
    DegreeCoherent c d := by
  change degree c = degree d
  rw [degree_eq_endpointHeight_sub l r hNe c,
    degree_eq_endpointHeight_sub l r hNe d]

/-- Genuine raw loops have ZERO degree for distinct adjoined endpoints. -/
theorem loop_degree_zero (l r : W) (hNe : l ≠ r) (w : W)
    (c : PentagonAdjoinedSixCell W l r w w) :
    degree c = 0 := by
  rw [degree_eq_endpointHeight_sub l r hNe c]
  exact sub_self _

/-- A precise, chosen endpoint shape: only identities and crossings
of the two adjoined endpoints can be connected by this grammar. -/
def EndpointShape (l r w z : W) : Prop :=
  w = z ∨ (w = l ∧ z = r) ∨ (w = r ∧ z = l)

/-- Raw six-cell words preserve the pair of distinguished endpoints,
unless the endpoints coincide. This claim is about the NEW grammar. -/
theorem endpointsSupported (l r : W)
    {w z : W} (c : PentagonAdjoinedSixCell W l r w z) :
    w = z ∨ ((w = l ∨ w = r) ∧ (z = l ∨ z = r)) := by
  induction c with
  | refl w =>
      exact Or.inl rfl
  | symm c ih =>
      rcases ih with heq | ⟨hw, hz⟩
      · exact Or.inl heq.symm
      · exact Or.inr ⟨hz, hw⟩
  | trans c d ihc ihd =>
      rcases ihc with hcx | ⟨hw, hx⟩
      · rcases ihd with hxz | ⟨hx', hz⟩
        · exact Or.inl (hcx.trans hxz)
        · exact Or.inr ⟨by rw [hcx]; exact hx', hz⟩
      · rcases ihd with hxz | ⟨_, hz⟩
        · exact Or.inr ⟨hw, by rw [← hxz]; exact hx⟩
        · exact Or.inr ⟨hw, hz⟩
  | pentagon =>
      exact Or.inr ⟨Or.inl rfl, Or.inr rfl⟩

theorem endpointShape_of_raw (l r : W)
    {w z : W} (c : PentagonAdjoinedSixCell W l r w z) :
    EndpointShape l r w z := by
  rcases endpointsSupported l r c with h | ⟨hw, hz⟩
  · exact Or.inl h
  · rcases hw with hwl | hwr
    · rcases hz with hzl | hzr
      · exact Or.inl (hwl.trans hzl.symm)
      · exact Or.inr (Or.inl ⟨hwl, hzr⟩)
    · rcases hz with hzl | hzr
      · exact Or.inr (Or.inr ⟨hwr, hzl⟩)
      · exact Or.inl (hwr.trans hzr.symm)

/-- Exact endpoint connectivity, not merely a one-way shape bound. -/
theorem comparison_nonempty_iff_endpointShape (l r w z : W) :
    Nonempty (PentagonAdjoinedSixCell W l r w z) ↔
      EndpointShape l r w z := by
  constructor
  · rintro ⟨c⟩
    exact endpointShape_of_raw l r c
  · intro hs
    rcases hs with heq | ⟨hw, hz⟩ | ⟨hw, hz⟩
    · subst z
      exact ⟨.refl w⟩
    · subst w
      subst z
      exact ⟨.pentagon⟩
    · subst w
      subst z
      exact ⟨.symm (.pentagon)⟩

/-- Only THREE shapes can serve as normal raw representatives.
This is a predicate on genuinely typed NEW six-cell words. -/
inductive EndpointNormal (W : Type uSix) (l r : W) :
    {w z : W} → PentagonAdjoinedSixCell W l r w z → Prop where
  | identity (w : W) : EndpointNormal W l r (.refl w)
  | forward : EndpointNormal W l r (.pentagon)
  | backward : EndpointNormal W l r (.symm (.pentagon))

/-- EXISTENCE of a three-shape raw representative for any original
free word, with a proof of equality of the chosen SIGNED DEGREES. -/
theorem exists_endpointNormal (l r : W) (hNe : l ≠ r)
    {w z : W} (c : PentagonAdjoinedSixCell W l r w z) :
    ∃ d : PentagonAdjoinedSixCell W l r w z,
      EndpointNormal W l r d ∧ DegreeCoherent c d := by
  rcases endpointShape_of_raw l r c with heq | ⟨hw, hz⟩ | ⟨hw, hz⟩
  · subst z
    refine ⟨.refl w, EndpointNormal.identity w, ?_⟩
    exact allParallel_degreeCoherent l r hNe c (.refl w)
  · subst w
    subst z
    refine ⟨.pentagon, EndpointNormal.forward, ?_⟩
    exact allParallel_degreeCoherent l r hNe c (.pentagon)
  · subst w
    subst z
    refine ⟨.symm (.pentagon), EndpointNormal.backward, ?_⟩
    exact allParallel_degreeCoherent l r hNe c (.symm (.pentagon))

/-- A deliberately separate selection; it does NOT rewrite the raw
six-cell source word by definitional or strict equality. -/
noncomputable def selectEndpointNormal (l r : W) (hNe : l ≠ r)
    {w z : W} (c : PentagonAdjoinedSixCell W l r w z) :
    PentagonAdjoinedSixCell W l r w z :=
  Classical.choose (exists_endpointNormal l r hNe c)

theorem selectEndpointNormal_isNormal (l r : W) (hNe : l ≠ r)
    {w z : W} (c : PentagonAdjoinedSixCell W l r w z) :
    EndpointNormal W l r (selectEndpointNormal l r hNe c) :=
  (Classical.choose_spec (exists_endpointNormal l r hNe c)).1

theorem selectEndpointNormal_degreeCoherent (l r : W) (hNe : l ≠ r)
    {w z : W} (c : PentagonAdjoinedSixCell W l r w z) :
    DegreeCoherent c (selectEndpointNormal l r hNe c) :=
  (Classical.choose_spec (exists_endpointNormal l r hNe c)).2

/-- The complete degree invariant of the EXPLICIT quotient Hom. -/
def homDegree (l r : W) {w z : W} :
    CoherentHom W l r w z → ℤ :=
  Quot.lift (fun c => degree c) (by
    intro c d h
    exact h)

theorem homDegree_mk (l r : W) {w z : W}
    (c : PentagonAdjoinedSixCell W l r w z) :
    homDegree l r (homMk c) = degree c := rfl

theorem homDegree_comp (l r : W) {w x z : W}
    (c : CoherentHom W l r w x)
    (d : CoherentHom W l r x z) :
    homDegree l r (homComp c d) =
      homDegree l r c + homDegree l r d := by
  refine Quot.inductionOn c ?_
  intro a
  refine Quot.inductionOn d ?_
  intro b
  rfl

theorem homDegree_inverse (l r : W) {w z : W}
    (c : CoherentHom W l r w z) :
    homDegree l r (homInv c) = -(homDegree l r c) := by
  refine Quot.inductionOn c ?_
  intro a
  rfl

/-- Soundness AND completeness of signed-degree equality for all
parallel quotient classes, even without distinctness hypotheses. -/
theorem homDegree_eq_iff (l r : W) {w z : W}
    (c d : CoherentHom W l r w z) :
    homDegree l r c = homDegree l r d ↔ c = d := by
  constructor
  · refine Quot.inductionOn c ?_
    intro a
    refine Quot.inductionOn d ?_
    intro b
    intro hab
    change degree a = degree b at hab
    exact Quot.sound hab
  · intro hcd
    exact congrArg (homDegree l r) hcd

/-- Endpoint potential determines every NEW coherence-class degree
when the original selected endpoints are distinct. -/
theorem homDegree_eq_endpointHeight_sub (l r : W) (hNe : l ≠ r)
    {w z : W} (c : CoherentHom W l r w z) :
    homDegree l r c = endpointHeight r z - endpointHeight r w := by
  refine Quot.inductionOn c ?_
  intro a
  exact degree_eq_endpointHeight_sub l r hNe a

/-- Thinness/completeness: every pair of parallel NEW quotient
six-cells is equal; raw representatives may still differ. -/
theorem allParallel_coherentHom_eq (l r : W) (hNe : l ≠ r)
    {w z : W} (c d : CoherentHom W l r w z) :
    c = d := by
  apply (homDegree_eq_iff l r c d).mp
  rw [homDegree_eq_endpointHeight_sub l r hNe c,
    homDegree_eq_endpointHeight_sub l r hNe d]

/-- Every inhabited quotient Hom has a canonical THREE-SHAPE raw
representative. No old five-cell Eq is used. -/
theorem coherentHom_hasEndpointNormal (l r : W) (hNe : l ≠ r)
    {w z : W} (q : CoherentHom W l r w z) :
    ∃ d : PentagonAdjoinedSixCell W l r w z,
      EndpointNormal W l r d ∧ q = homMk d := by
  refine Quot.inductionOn q ?_
  intro c
  refine ⟨selectEndpointNormal l r hNe c,
    selectEndpointNormal_isNormal l r hNe c, ?_⟩
  exact Quot.sound (selectEndpointNormal_degreeCoherent l r hNe c)

/-- Exact (possibly empty) classification of Hom-sets in the chosen
thin coherence groupoid; do NOT infer an old source filler. -/
theorem coherentHom_nonempty_iff_endpointShape (l r w z : W) :
    Nonempty (CoherentHom W l r w z) ↔ EndpointShape l r w z := by
  constructor
  · rintro ⟨q⟩
    refine Quot.inductionOn q ?_
    intro c
    exact endpointShape_of_raw l r c
  · intro hs
    rcases hs with heq | ⟨hw, hz⟩ | ⟨hw, hz⟩
    · subst z
      exact ⟨homId w⟩
    · subst w
      subst z
      exact ⟨homMk (.pentagon)⟩
    · subst w
      subst z
      exact ⟨homMk (.symm (.pentagon))⟩

/-- Every endomorphism in this NEW distinct-endpoint quotient is its
own identity; the original free syntax can have distinct roundtrips. -/
theorem coherentHom_self_eq_id (l r : W) (hNe : l ≠ r)
    (w : W) (q : CoherentHom W l r w w) :
    q = homId w :=
  allParallel_coherentHom_eq l r hNe q (homId w)

/-- The freshly adjoined raw pentagon is NOT a strict equality
between old endpoints, despite its quotient-level normal form. -/
theorem normalForm_doesNotReturnOldEq (l r : W) (hNe : l ≠ r) :
    Nonempty (CoherentHom W l r l r) ∧ ¬ (l = r) :=
  ⟨⟨homMk (.pentagon)⟩, hNe⟩

end PentagonAdjoinedSixCell

section ActualSourceEndpointNormalForms
variable {u v : FivefoldPathVertex}
variable {family₀ family₁ family₂ family₃ family₄ : Family f g h k u v}
variable {s₀ : State f g h k family₀}
variable {s₁ : State f g h k family₁}
variable {s₂ : State f g h k family₂}
variable {s₃ : State f g h k family₃}
variable {s₄ : State f g h k family₄}
variable (A : DirectNormalBracketTree f g h k family₀ s₀ family₁ s₁)
variable (B : DirectNormalBracketTree f g h k family₁ s₁ family₂ s₂)
variable (C : DirectNormalBracketTree f g h k family₂ s₂ family₃ s₃)
variable (D₄ : DirectNormalBracketTree f g h k family₃ s₃ family₄ s₄)

/-- For EVERY genuine terminal P77 raw index, every type-valued
NEW sixth-dimensional word has degree forced by ACTUAL old endpoints. -/
theorem pentagonActualSixCell_degree_endpointPotential
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄))
    {w z : pentagonFinalConservativeLoop f g h k i}
    (c : pentagonAdjoinedSixCellAt f g h k A B C D₄ i w z) :
    PentagonAdjoinedSixCell.degree c =
      PentagonAdjoinedSixCell.endpointHeight
        (pentagonShortConservativeFiveCell f g h k A B C D₄ i) z -
      PentagonAdjoinedSixCell.endpointHeight
        (pentagonShortConservativeFiveCell f g h k A B C D₄ i) w := by
  exact PentagonAdjoinedSixCell.degree_eq_endpointHeight_sub
    (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
    (pentagonShortConservativeFiveCell f g h k A B C D₄ i)
    (pentagonOriginalFiveCell_words_ne f g h k A B C D₄ i) c

/-- Every pair of NEW six-cell raw words with the SAME ORIGINAL
endpoint five-cell values is coherent, with no assumption of Eq
of their raw six-cell syntax. -/
theorem pentagonActualSixCell_allParallelCoherent
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄))
    {w z : pentagonFinalConservativeLoop f g h k i}
    (c d : pentagonAdjoinedSixCellAt f g h k A B C D₄ i w z) :
    PentagonAdjoinedSixCell.DegreeCoherent c d :=
  PentagonAdjoinedSixCell.allParallel_degreeCoherent
    (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
    (pentagonShortConservativeFiveCell f g h k A B C D₄ i)
    (pentagonOriginalFiveCell_words_ne f g h k A B C D₄ i) c d

/-- Strong endpoint-wise normal representative existence FOR ALL
actual P77 raw terminals, relative to the SEPARATELY adjoined six-cells. -/
theorem pentagonActualSixCell_allRawEndpointNormal
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄))
    {w z : pentagonFinalConservativeLoop f g h k i}
    (c : pentagonAdjoinedSixCellAt f g h k A B C D₄ i w z) :
    ∃ d : pentagonAdjoinedSixCellAt f g h k A B C D₄ i w z,
      PentagonAdjoinedSixCell.EndpointNormal
        (pentagonFinalConservativeLoop f g h k i)
        (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
        (pentagonShortConservativeFiveCell f g h k A B C D₄ i) d ∧
      PentagonAdjoinedSixCell.DegreeCoherent c d :=
  PentagonAdjoinedSixCell.exists_endpointNormal
    (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
    (pentagonShortConservativeFiveCell f g h k A B C D₄ i)
    (pentagonOriginalFiveCell_words_ne f g h k A B C D₄ i) c

/-- ACTUAL raw-indexed chosen coherence quotient is locally thin:
at most one class between each fixed pair of ORIGINAL old five-cells. -/
theorem pentagonActualSixCell_allParallelHom_eq
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄))
    {w z : pentagonFinalConservativeLoop f g h k i}
    (q₁ q₂ : PentagonAdjoinedSixCell.CoherentHom
      (pentagonFinalConservativeLoop f g h k i)
      (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
      (pentagonShortConservativeFiveCell f g h k A B C D₄ i) w z) :
    q₁ = q₂ :=
  PentagonAdjoinedSixCell.allParallel_coherentHom_eq
    (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
    (pentagonShortConservativeFiveCell f g h k A B C D₄ i)
    (pentagonOriginalFiveCell_words_ne f g h k A B C D₄ i) q₁ q₂

/-- The actual old five-cell words are distinct yet there is exactly
one newly adjoined coherent comparison class between them. -/
theorem pentagonActualSixCell_endpointComparison_unique
    (i : FivefoldP77RawPatchTreeIndex f g h k
      (tree f g h k family₄ s₄)) :
    Nonempty (PentagonAdjoinedSixCell.CoherentHom
      (pentagonFinalConservativeLoop f g h k i)
      (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
      (pentagonShortConservativeFiveCell f g h k A B C D₄ i)
      (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
      (pentagonShortConservativeFiveCell f g h k A B C D₄ i)) ∧
    (∀ (q₁ q₂ : PentagonAdjoinedSixCell.CoherentHom
      (pentagonFinalConservativeLoop f g h k i)
      (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
      (pentagonShortConservativeFiveCell f g h k A B C D₄ i)
      (pentagonLongConservativeFiveCell f g h k A B C D₄ i)
      (pentagonShortConservativeFiveCell f g h k A B C D₄ i)),
      q₁ = q₂) ∧
    pentagonLongConservativeFiveCell f g h k A B C D₄ i ≠
      pentagonShortConservativeFiveCell f g h k A B C D₄ i := by
  refine ⟨⟨PentagonAdjoinedSixCell.homMk
    (pentagonAdjoinedSixCell_generator f g h k A B C D₄ i)⟩, ?_, ?_⟩
  · intro q₁ q₂
    exact pentagonActualSixCell_allParallelHom_eq
      f g h k A B C D₄ i q₁ q₂
  · exact pentagonOriginalFiveCell_words_ne f g h k A B C D₄ i

#print axioms PentagonAdjoinedSixCell.endpointHeight
#print axioms PentagonAdjoinedSixCell.degree_eq_endpointHeight_sub
#print axioms PentagonAdjoinedSixCell.allParallel_degreeCoherent
#print axioms PentagonAdjoinedSixCell.loop_degree_zero
#print axioms PentagonAdjoinedSixCell.endpointShape_of_raw
#print axioms PentagonAdjoinedSixCell.comparison_nonempty_iff_endpointShape
#print axioms PentagonAdjoinedSixCell.EndpointNormal
#print axioms PentagonAdjoinedSixCell.exists_endpointNormal
#print axioms PentagonAdjoinedSixCell.homDegree
#print axioms PentagonAdjoinedSixCell.homDegree_eq_iff
#print axioms PentagonAdjoinedSixCell.homDegree_eq_endpointHeight_sub
#print axioms PentagonAdjoinedSixCell.allParallel_coherentHom_eq
#print axioms PentagonAdjoinedSixCell.coherentHom_hasEndpointNormal
#print axioms PentagonAdjoinedSixCell.coherentHom_nonempty_iff_endpointShape
#print axioms PentagonAdjoinedSixCell.coherentHom_self_eq_id
#print axioms pentagonActualSixCell_degree_endpointPotential
#print axioms pentagonActualSixCell_allParallelCoherent
#print axioms pentagonActualSixCell_allRawEndpointNormal
#print axioms pentagonActualSixCell_allParallelHom_eq
#print axioms pentagonActualSixCell_endpointComparison_unique

end ActualSourceEndpointNormalForms
end FivefoldP77FiniteRefinement
end
end KUOS.Architecture.WuxingPentagonUnified
