import Kuu.F112.PolygonNativeF55P94DK5NineActualF54GlobalRoutes
import Mathlib.Tactic

/-!
# F112-P94D3J — nine REAL typed F55/P92B face whiskerings

Each step of P94D3I's exact closed nine-face GRAPH shelling is
lifted to a genuine source P92B Type-valued 3-cell between TWO
real native F54 routes, both from the SAME original dependent
F45 13→0 boundary. The antecedent/suffix F54 transports are
built exclusively from the original twenty-one true P94D1 edges.

The word of each such 3-cell is the word of the original ACTUAL
P94D3A anchored face, with outward orientation unchanged.
Unlike P94D3H's tag-order formal sum, our cyclic word is the
ordered concatenation of NINE genuine whiskered Type-valued
3-proof terms. But their *intermediate route proof terms* need
not match between steps: we do NOT fabricate a global 3-pasting
nor the missing 4-dimensional pentagonator filler.

All original strict-route no-go statements are preserved.
No Gray, sorry/admit, new axioms or root removal.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

inductive NativeK5WhiskeredFaceTag where
  | step0
  | step1
  | step2
  | step3
  | step4
  | step5
  | step6
  | step7
  | step8
  deriving DecidableEq

def nativeK5WhiskeredFaceTagOfFin (i : Fin 9) : NativeK5WhiskeredFaceTag :=
  match i.val with
  | 0 => .step0
  | 1 => .step1
  | 2 => .step2
  | 3 => .step3
  | 4 => .step4
  | 5 => .step5
  | 6 => .step6
  | 7 => .step7
  | 8 => .step8
  | _ => .step8

def nativeK5WhiskeredFaceTagFin : NativeK5WhiskeredFaceTag → Fin 9
  | .step0 => 0
  | .step1 => 1
  | .step2 => 2
  | .step3 => 3
  | .step4 => 4
  | .step5 => 5
  | .step6 => 6
  | .step7 => 7
  | .step8 => 8

theorem nativeK5WhiskeredFaceTag_roundtrip (i : Fin 9) :
    nativeK5WhiskeredFaceTagFin (nativeK5WhiskeredFaceTagOfFin i) = i := by
  fin_cases i <;> rfl

section FiveNativeStages
variable {p : Polygon} {a b : D} {x y : E}
variable {n₁ n₂ n₃ n₄ n₅ m₁ m₂ m₃ m₄ m₅ : Nat}
variable {p₀ p₁ p₂ p₃ p₄ p₅ : KuuNativeBlocks a b}
variable {q₀ q₁ q₂ q₃ q₄ q₅ : KuuNativeBlocks x y}
variable
  (t1 : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁)
  (t2 : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂)
  (t3 : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃)
  (t4 : KuuNativeF45Tree p n₄ m₄ p₃ q₃ p₄ q₄)
  (t5 : KuuNativeF45Tree p n₅ m₅ p₄ q₄ p₅ q₅)

/-- One genuinely typed P92B three-cell at each outward K₅
global rewrite step: the source and target are actual dependent
F54 route witnesses with the SAME original 13→0 F45 trees.
All nine constructors are original face proof terms transported by
actual pre-/postcomposition of original F54 edges. -/
def nativeK5WhiskeredActualFace (step : NativeK5WhiskeredFaceTag) :
    Σ r : NativeK5GlobalRoute t1 t2 t3 t4 t5,
      Σ s : NativeK5GlobalRoute t1 t2 t3 t4 t5,
        NativeF55P92AssocComparison p r s :=
  match step with
  | .step0 => ⟨_, _, (.postcompose (nativeK5PentagonFace7_oriented t1 t2 t3 t4 t5) (nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5 .e2))⟩
  | .step1 => ⟨_, _, (.precompose (.trans (nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5 .e19) (nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5 .e12)) (nativeK5NaturalitySquare0 t1 t2 t3 t4 t5))⟩
  | .step2 => ⟨_, _, (.postcompose (.precompose (nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5 .e19) (nativeK5PentagonFace5_oriented t1 t2 t3 t4 t5)) (nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5 .e0))⟩
  | .step3 => ⟨_, _, (.postcompose (nativeK5PentagonFace8_oriented t1 t2 t3 t4 t5) (.trans (.trans (nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5 .e8) (nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5 .e3)) (nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5 .e0)))⟩
  | .step4 => ⟨_, _, (.postcompose (.precompose (.trans (nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5 .e20) (nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5 .e18)) (nativeK5NaturalitySquare1 t1 t2 t3 t4 t5)) (.trans (nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5 .e3) (nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5 .e0)))⟩
  | .step5 => ⟨_, _, (.precompose (.trans (.trans (nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5 .e20) (nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5 .e18)) (nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5 .e9)) (nativeK5PentagonFace3 t1 t2 t3 t4 t5))⟩
  | .step6 => ⟨_, _, (.postcompose (.precompose (nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5 .e20) (nativeK5PentagonFace6 t1 t2 t3 t4 t5)) (nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5 .e1))⟩
  | .step7 => ⟨_, _, (.postcompose (NativeF55P92AssocComparison.symm (nativeK5NaturalitySquare2 t1 t2 t3 t4 t5)) (.trans (nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5 .e6) (nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5 .e1)))⟩
  | .step8 => ⟨_, _, (.precompose (nativeK5TaggedEdgeRoute t1 t2 t3 t4 t5 .e15) (nativeK5PentagonFace4 t1 t2 t3 t4 t5))⟩

def nativeK5WhiskeredActualFaceFin (k : Fin 9) :
    Σ r : NativeK5GlobalRoute t1 t2 t3 t4 t5,
      Σ s : NativeK5GlobalRoute t1 t2 t3 t4 t5,
        NativeF55P92AssocComparison p r s :=
  nativeK5WhiskeredActualFace t1 t2 t3 t4 t5
    (nativeK5WhiskeredFaceTagOfFin k)

/-- The SOURCE of each actually whiskered face has exactly the
same genuine F54 rotation count as the corresponding graph spine
of P94D3I. The TARGET source proof has its own exact count. -/
theorem nativeK5WhiskeredActualFace_count
    (step : NativeK5WhiskeredFaceTag) :
    let f := nativeK5WhiskeredActualFace t1 t2 t3 t4 t5 step
    let k := nativeK5WhiskeredFaceTagFin step
    (f.1.rotationCount, f.2.1.rotationCount) =
      ((nativeK5GlobalMonotonePath (nativeK5GraphShellingStep k).source).length - 1,
       (nativeK5GlobalMonotonePath (nativeK5GraphShellingStep k).target).length - 1) := by
  cases step <;> rfl

/-- REAL source 3-cell under both F54 whiskerings preserves its
precise oriented ANCHORED P94D3A free word, not a numeric guess. -/
theorem nativeK5WhiskeredActualFace_groupWord
    (step : NativeK5WhiskeredFaceTag) :
    (nativeK5WhiskeredActualFace t1 t2 t3 t4 t5 step).2.2.p94cGroupWord =
      (nativeK5AnchoredFace t1 t2 t3 t4 t5
        (nativeK5FaceTagOfFin
          (nativeK5GraphShellingStep (nativeK5WhiskeredFaceTagFin step)).face)).2.2.2.p94cGroupWord := by
  cases step <;> rfl

/-- The chosen global shelling's noncommutative ordered aggregate
now consists of NINE separately genuinely typed and whiskered
source P92B 3-cells. It is still NOT their global Type-valued
3-pasting: adjacent raw F54 source route terms are not yet linked. -/
def nativeK5NineWhiskeredFaceFormalWord : NativeF55P94CWord :=
  (nativeK5WhiskeredActualFace t1 t2 t3 t4 t5 .step0).2.2.p94cGroupWord +
  (nativeK5WhiskeredActualFace t1 t2 t3 t4 t5 .step1).2.2.p94cGroupWord +
  (nativeK5WhiskeredActualFace t1 t2 t3 t4 t5 .step2).2.2.p94cGroupWord +
  (nativeK5WhiskeredActualFace t1 t2 t3 t4 t5 .step3).2.2.p94cGroupWord +
  (nativeK5WhiskeredActualFace t1 t2 t3 t4 t5 .step4).2.2.p94cGroupWord +
  (nativeK5WhiskeredActualFace t1 t2 t3 t4 t5 .step5).2.2.p94cGroupWord +
  (nativeK5WhiskeredActualFace t1 t2 t3 t4 t5 .step6).2.2.p94cGroupWord +
  (nativeK5WhiskeredActualFace t1 t2 t3 t4 t5 .step7).2.2.p94cGroupWord +
  (nativeK5WhiskeredActualFace t1 t2 t3 t4 t5 .step8).2.2.p94cGroupWord

/-- Exactly the cyclically ordered P94D3I word, not its
different P94D3H tag-ordered formal analogue. -/
theorem nativeK5NineWhiskeredFaceFormalWord_eq_shelling :
    nativeK5NineWhiskeredFaceFormalWord t1 t2 t3 t4 t5 =
      nativeK5GraphShellingWord t1 t2 t3 t4 t5 := by
  rfl

theorem nativeK5NineWhiskeredFaceFormalWord_NCount_one :
    nativeK5NaturalityCount
      (nativeK5NineWhiskeredFaceFormalWord t1 t2 t3 t4 t5) = 1 := by
  rw [nativeK5NineWhiskeredFaceFormalWord_eq_shelling,
    nativeK5GraphShellingWord_NCount_one]

theorem nativeK5NineWhiskeredFaceFormalWord_shadow_zero :
    nativeF55P94CWordToShadow
      (nativeK5NineWhiskeredFaceFormalWord t1 t2 t3 t4 t5) = 0 := by
  rw [nativeK5NineWhiskeredFaceFormalWord_eq_shelling,
    nativeK5GraphShellingWord_shadow_zero]

/-- The word assembled from genuine, whiskered P92B 3-proofs
cannot be filled by any 4-cell from the existing P94A normal
kernel; no global three-cell existence is inferred. -/
theorem nativeK5NineWhiskeredFaceFormalWord_not_mem_P94ATyped :
    nativeK5NineWhiskeredFaceFormalWord t1 t2 t3 t4 t5 ∉
      nativeK5P94ATypedNormalClosure D E := by
  rw [nativeK5NineWhiskeredFaceFormalWord_eq_shelling]
  exact nativeK5GraphShellingWord_not_mem_P94ATyped t1 t2 t3 t4 t5

#print axioms nativeK5WhiskeredFaceTag_roundtrip
#print axioms nativeK5WhiskeredActualFace
#print axioms nativeK5WhiskeredActualFace_count
#print axioms nativeK5WhiskeredActualFace_groupWord
#print axioms nativeK5NineWhiskeredFaceFormalWord_eq_shelling
#print axioms nativeK5NineWhiskeredFaceFormalWord_NCount_one
#print axioms nativeK5NineWhiskeredFaceFormalWord_shadow_zero
#print axioms nativeK5NineWhiskeredFaceFormalWord_not_mem_P94ATyped

end FiveNativeStages
end
end Kuu.F112.Physical
