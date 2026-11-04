import KUOS.Architecture.QiWuxingGK5CGUnifiedFivefoldTypedEdgesV4_52
import Mathlib.CategoryTheory.PathCategory.Basic
import Mathlib.Tactic

/-!
Qi v4.53 — GENUINE FREE FIVEFOLD PATHS INTO ORIGINAL F55/P77 PROOF TERMS.

Keep the ONE canonical FivefoldIndex = FivePhase = ZMod 5 and
FivefoldEdge of Qi v3.5/v4.52. Because Qi v3.1 already has a different
quiver on FivePhase (generation/control), this true five-edge quiver
uses an explicit wrapped vertex type; it does NOT replace that quiver.

The actual original P77 four-cell for every edge is the existing
Qi v4.52 dependently typed proof, including the true reverse
e04/e43 orientations. A structural recursion sends an arbitrary
finite typed free path to a REAL original P77 four-proof.
Unlike a quotient or a numerical proxy, this evaluator preserves
P77 proof constructors (including identity and composition).

The signed original GK5CG four-associator charge of the evaluation
is EXACTLY the length of the typed free path. Thus the two pentagon
routes have 3 vs 2 and remain different even after typed evaluation;
a conservative source 5-cell cannot bridge them. A length-faithful
path presentation is sufficient for the evaluator to be faithful.
No assertion that every possible higher presentation is faithful.

The matching physical trace uses original C60 around-edges without
fabricated graph-to-higher relations. Original C60 evidence, raw
F55/P77/P94A and Qi v4.51 CRT proofs remain distinct authorities.
Append-only, original 107 roots, pinned Lean v4.30.0-rc2,
mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6,
strict 空 center and independent Kuu one presentation,
#1558 Draft/open/unmerged. No new axioms/sorry/admit/Gray.
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

/-- Distinct quiver authority: it does not modify Qi v3.1's
generation/control arrows on the underlying FivePhase type. -/
structure FivefoldPathVertex where
  phase : FivefoldIndex
  deriving DecidableEq

def fivefoldPathVertex (phase : FivefoldIndex) : FivefoldPathVertex :=
  ⟨phase⟩

/-- An edge includes genuine Qi v3.5 endpoints as equality proofs. -/
structure FivefoldPathArrow (a b : FivefoldPathVertex) where
  edge : FivefoldEdge
  source_eq : fivefoldFrom edge = a.phase
  target_eq : fivefoldTo edge = b.phase

instance fivefoldPathQuiver : Quiver FivefoldPathVertex where
  Hom := FivefoldPathArrow

/-- The original five directed edges as genuine typed quiver generators. -/
def fivefoldPathArrowOf (edge : FivefoldEdge) :
    FivefoldPathArrow (fivefoldPathVertex (fivefoldFrom edge))
      (fivefoldPathVertex (fivefoldTo edge)) :=
  ⟨edge, rfl, rfl⟩

/-- Actual Mathlib free category, not the source P77 proof grammar
wrongly asserted to already satisfy strict categorical equations. -/
abbrev FivefoldFreePathCategory := CategoryTheory.Paths FivefoldPathVertex

/-- The three-edge top route of the genuine fivefold source quiver. -/
def fivefoldFreeUpper :
    Quiver.Path (fivefoldPathVertex 0) (fivefoldPathVertex 3) :=
  (((Quiver.Path.nil :
        Quiver.Path (fivefoldPathVertex 0) (fivefoldPathVertex 0)).cons
      (fivefoldPathArrowOf .e01)).cons (fivefoldPathArrowOf .e12)).cons
      (fivefoldPathArrowOf .e23)

/-- The two-edge bottom route, retaining genuine e04/e43 direction. -/
def fivefoldFreeLower :
    Quiver.Path (fivefoldPathVertex 0) (fivefoldPathVertex 3) :=
  ((Quiver.Path.nil :
       Quiver.Path (fivefoldPathVertex 0) (fivefoldPathVertex 0)).cons
     (fivefoldPathArrowOf .e04)).cons (fivefoldPathArrowOf .e43)

theorem fivefoldFreeUpper_length : fivefoldFreeUpper.length = 3 := rfl

theorem fivefoldFreeLower_length : fivefoldFreeLower.length = 2 := rfl

/-- The two free paths are provably different even though
they have exactly the same typed endpoints. -/
theorem fivefoldFreeUpper_ne_lower : fivefoldFreeUpper ≠ fivefoldFreeLower := by
  intro eq
  have h := congrArg Quiver.Path.length eq
  rw [fivefoldFreeUpper_length, fivefoldFreeLower_length] at h
  omega

section OriginalFourProofEvaluation
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

/-- A proof-carrying arrow maps to the EXACT original P77 four-cell
at its indexed F55 source and target, with no quotient or shadow. -/
def fivefoldArrowOriginalP77 {u v : FivefoldPathVertex}
    (arrow : FivefoldPathArrow u v) :
    NativeF55RawVerticalFourCell first last
      (fivefoldF55OriginalAt f g h k u.phase)
      (fivefoldF55OriginalAt f g h k v.phase) := by
  rcases u with ⟨u⟩
  rcases v with ⟨v⟩
  rcases arrow with ⟨edge, hs, ht⟩
  cases hs
  cases ht
  exact fivefoldF55OriginalP77Edge f g h k edge

/-- The original P77 integer associator charge of every authentic
directed edge is +1. The source/target proof casts are discharged
before applying the original charge certificate. -/
theorem fivefoldArrowOriginalP77_charge_one
    {u v : FivefoldPathVertex} (arrow : FivefoldPathArrow u v) :
    (fivefoldArrowOriginalP77 f g h k arrow).gk5cgAssocCharge = 1 := by
  rcases u with ⟨u⟩
  rcases v with ⟨v⟩
  rcases arrow with ⟨edge, hs, ht⟩
  cases hs
  cases ht
  exact fivefoldF55OriginalP77Edge_assocCharge_one f g h k edge

/-- Genuine proof-relevant evaluator from ANY typed finite fivefold
free path to an ORIGINAL P77 four-cell between the corresponding
F55 source terms. Recurse over real Quiver.Path constructors. -/
def fivefoldEvaluateP77
    {u v : FivefoldPathVertex} (path : Quiver.Path u v) :
    NativeF55RawVerticalFourCell first last
      (fivefoldF55OriginalAt f g h k u.phase)
      (fivefoldF55OriginalAt f g h k v.phase) :=
  @Quiver.Path.rec FivefoldPathVertex fivefoldPathQuiver u
    (fun z _ =>
      NativeF55RawVerticalFourCell first last
        (fivefoldF55OriginalAt f g h k u.phase)
        (fivefoldF55OriginalAt f g h k z.phase))
    (.refl (fivefoldF55OriginalAt f g h k u.phase))
    (fun _ _ edge ih =>
      .trans ih (fivefoldArrowOriginalP77 f g h k edge))
    v path

/-- Evaluation of an empty free path is the genuine P77 reflexivity
constructor, not an invented numerical identity. -/
theorem fivefoldEvaluateP77_nil (u : FivefoldPathVertex) :
    fivefoldEvaluateP77 f g h k
      (Quiver.Path.nil : Quiver.Path u u) =
    (NativeF55RawVerticalFourCell.refl
      (fivefoldF55OriginalAt f g h k u.phase)) := rfl

/-- Appending a genuine edge is original P77 vertical pasting. -/
theorem fivefoldEvaluateP77_cons
    {u v w : FivefoldPathVertex}
    (path : Quiver.Path u v) (edge : FivefoldPathArrow v w) :
    fivefoldEvaluateP77 f g h k (path.cons edge) =
      NativeF55RawVerticalFourCell.trans
        (fivefoldEvaluateP77 f g h k path)
        (fivefoldArrowOriginalP77 f g h k edge) := rfl

/-- Complete arbitrary-length source charge certificate.
Every original P77 associator generator contributes exactly one. -/
theorem fivefoldEvaluateP77_charge_length
    {u v : FivefoldPathVertex} (path : Quiver.Path u v) :
    (fivefoldEvaluateP77 f g h k path).gk5cgAssocCharge =
      (path.length : ℤ) := by
  induction path with
  | nil =>
      rfl
  | cons path edge ih =>
      rw [fivefoldEvaluateP77_cons,
        nativeGK5CGAssocCharge_trans,
        fivefoldArrowOriginalP77_charge_one, ih]
      simp only [Quiver.Path.length_cons, Nat.cast_add, Nat.cast_one]

/-- Typed evaluator equality necessarily reflects the actual
number of original generating 4-proofs (no path-length collapse). -/
theorem fivefoldEvaluateP77_eq_implies_length
    {u v : FivefoldPathVertex} (a b : Quiver.Path u v)
    (heq : fivefoldEvaluateP77 f g h k a =
      fivefoldEvaluateP77 f g h k b) :
    a.length = b.length := by
  have charge := congrArg
    (fun w : NativeF55RawVerticalFourCell first last
       (fivefoldF55OriginalAt f g h k u.phase)
       (fivefoldF55OriginalAt f g h k v.phase) =>
       w.gk5cgAssocCharge) heq
  rw [fivefoldEvaluateP77_charge_length,
    fivefoldEvaluateP77_charge_length] at charge
  exact_mod_cast charge

/-- Exact CONDITIONAL faithfulness statement: any specified free-path
presentation in which length reflects same-endpoint equality has an
injective original four-proof evaluator. This does not assume such a
property for arbitrary unrelated quivers or higher categories. -/
theorem fivefoldEvaluateP77_injective_of_length
    (hLength : ∀ {u v : FivefoldPathVertex},
      Function.Injective (fun path : Quiver.Path u v => path.length))
    {u v : FivefoldPathVertex} :
    Function.Injective
      (fivefoldEvaluateP77 f g h k (u := u) (v := v)) := by
  intro a b eq
  exact hLength (fivefoldEvaluateP77_eq_implies_length f g h k a b eq)

/-- On both true pentagon paths the resulting ACTUAL P77 source
four-proofs have charge 3 and 2, respectively. -/
theorem fivefoldFreeTwoEvaluations_charge :
    (fivefoldEvaluateP77 f g h k fivefoldFreeUpper).gk5cgAssocCharge = 3 ∧
    (fivefoldEvaluateP77 f g h k fivefoldFreeLower).gk5cgAssocCharge = 2 := by
  constructor
  · rw [fivefoldEvaluateP77_charge_length]
    exact_mod_cast fivefoldFreeUpper_length
  · rw [fivefoldEvaluateP77_charge_length]
    exact_mod_cast fivefoldFreeLower_length

/-- The genuine original four-proof values cannot be identified. -/
theorem fivefoldFreeTwoEvaluations_ne :
    fivefoldEvaluateP77 f g h k fivefoldFreeUpper ≠
      fivefoldEvaluateP77 f g h k fivefoldFreeLower := by
  intro heq
  have hl := fivefoldEvaluateP77_eq_implies_length f g h k
    fivefoldFreeUpper fivefoldFreeLower heq
  rw [fivefoldFreeUpper_length, fivefoldFreeLower_length] at hl
  omega

/-- More strongly: there is no conservative ORIGINAL P77
five-cell between the evaluated typed paths, by charge soundness. -/
theorem fivefoldFreeTwoEvaluations_noConservativeFiveCell :
    ¬ Nonempty (NativeGK5CGConservativeFiveCell first last
      (fivefoldEvaluateP77 f g h k fivefoldFreeUpper)
      (fivefoldEvaluateP77 f g h k fivefoldFreeLower)) := by
  rintro ⟨v⟩
  have hc := v.assocCharge_sound
  obtain ⟨ha, hb⟩ := fivefoldFreeTwoEvaluations_charge f g h k
  rw [ha, hb] at hc
  omega

end OriginalFourProofEvaluation

/-- The same true five-edge free syntax also gives a physical
C60 trace without changing incidence or identifying higher cells. -/
def fivefoldFreePhysicalTrace
    (frame : NativeC60FivePhaseGauge) (v : Vertex)
    {u w : FivefoldPathVertex} (path : Quiver.Path u w) : List Edge :=
  @Quiver.Path.rec FivefoldPathVertex fivefoldPathQuiver u
    (fun _ _ => List Edge) []
    (fun _ _ edge ih => ih ++ [fivefoldPhysicalEdge frame v edge.edge])
    w path

theorem fivefoldFreePhysicalTrace_nil
    (frame : NativeC60FivePhaseGauge) (v : Vertex)
    (u : FivefoldPathVertex) :
    fivefoldFreePhysicalTrace frame v
      (Quiver.Path.nil : Quiver.Path u u) = [] := rfl

theorem fivefoldFreePhysicalTrace_cons
    (frame : NativeC60FivePhaseGauge) (v : Vertex)
    {u x y : FivefoldPathVertex}
    (path : Quiver.Path u x) (edge : FivefoldPathArrow x y) :
    fivefoldFreePhysicalTrace frame v (path.cons edge) =
      fivefoldFreePhysicalTrace frame v path ++
        [fivefoldPhysicalEdge frame v edge.edge] := rfl

/-- No actual C60 edge is created or destroyed when moving from the
proof-indexed finite path to its geometrical edge list. -/
theorem fivefoldFreePhysicalTrace_length
    (frame : NativeC60FivePhaseGauge) (v : Vertex)
    {u w : FivefoldPathVertex} (path : Quiver.Path u w) :
    (fivefoldFreePhysicalTrace frame v path).length = path.length := by
  induction path with
  | nil => rfl
  | cons path edge ih =>
      rw [fivefoldFreePhysicalTrace_cons]
      simp only [List.length_append, List.length_singleton, ih,
        Quiver.Path.length_cons]

#print axioms fivefoldFreeUpper_length
#print axioms fivefoldFreeLower_length
#print axioms fivefoldFreeUpper_ne_lower
#print axioms fivefoldArrowOriginalP77
#print axioms fivefoldArrowOriginalP77_charge_one
#print axioms fivefoldEvaluateP77_nil
#print axioms fivefoldEvaluateP77_cons
#print axioms fivefoldEvaluateP77_charge_length
#print axioms fivefoldEvaluateP77_eq_implies_length
#print axioms fivefoldEvaluateP77_injective_of_length
#print axioms fivefoldFreeTwoEvaluations_charge
#print axioms fivefoldFreeTwoEvaluations_ne
#print axioms fivefoldFreeTwoEvaluations_noConservativeFiveCell
#print axioms fivefoldFreePhysicalTrace_length

end
end KUOS.Architecture.WuxingPentagonUnified
