import Kuu.F112.PolygonNativeF55P94DK5NineTypedWhiskeredFaces
import Mathlib.Tactic

/-!
# F112-P94D3J — exact inter-face raw F54-route seam obstruction

All nine P94D3J face whiskerings are genuine Type-valued P92B
3-cells, but the TARGET raw F54 route of each 3-cell is not
syntactically equal to the SOURCE raw F54 route of its successor.
The mismatch is not due to a different original F45 boundary:
all belong to the same dependent 13→0 original F45 tree type.

Read the actual outer F54 trans constructor's LEFT subroute
primitive rotation count. Compute it directly on ALL nine real
whiskered source/target pairs. For each boundary seam its values
differ, proving no judgemental identification can concatenate
the chosen nine witnesses via unmodified P92B .trans.

A separate true Type-valued P92B seam comparison (or appropriate
new presentation/transport) is required at each boundary. Its
existence is NOT inferred from these numerical counts, which
are used only to disprove raw source-term equality.
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

/-- A structural (proof-relevant) root observer of the ORIGINAL
F54 route grammar, detecting exact trans bracketing, not a
homomorphism or invariant of the route quotient. -/
def KuuNativeF45Tree.DepthRotationRoute.rootLeftRotationCount
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (route : KuuNativeF45Tree.DepthRotationRoute p first last) : Option Nat :=
  match route with
  | .trans left _ => some left.rotationCount
  | _ => none

/-- Exact root-left primitive rotation counts of the NINE
individually genuine P92B source/target route terms. -/
def nativeK5WhiskeredFaceRootCounts : NativeK5WhiskeredFaceTag → Option Nat × Option Nat
  | .step0 => (some 2, some 3)
  | .step1 => (some 2, some 2)
  | .step2 => (some 3, some 4)
  | .step3 => (some 2, some 3)
  | .step4 => (some 4, some 4)
  | .step5 => (some 3, some 3)
  | .step6 => (some 4, some 3)
  | .step7 => (some 2, some 2)
  | .step8 => (some 1, some 1)

def nativeK5WhiskeredFaceNext : NativeK5WhiskeredFaceTag → NativeK5WhiskeredFaceTag
  | .step0 => .step1
  | .step1 => .step2
  | .step2 => .step3
  | .step3 => .step4
  | .step4 => .step5
  | .step5 => .step6
  | .step6 => .step7
  | .step7 => .step8
  | .step8 => .step0

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

/-- Unlike a graph-path-length guess, these are directly
computed from the two genuinely dependent original-F54
route *terms* of each actual whiskered Type-valued 3-cell. -/
theorem nativeK5WhiskeredFaceRootCounts_exact (tag : NativeK5WhiskeredFaceTag) :
    let f := nativeK5WhiskeredActualFace t1 t2 t3 t4 t5 tag
    (f.1.rootLeftRotationCount, f.2.1.rootLeftRotationCount) =
      nativeK5WhiskeredFaceRootCounts tag := by
  cases tag <;> rfl

/-- EVERY adjacent raw F54 seam along the entire outward K₅
nine-face circuit has genuinely unequal raw source 2-route
proof terms. This is a precise obstruction to naive 3-pasting,
not a no-go for a separately evidenced P92B route comparison. -/
theorem nativeK5WhiskeredFace_next_route_ne
    (tag : NativeK5WhiskeredFaceTag) :
    (nativeK5WhiskeredActualFace t1 t2 t3 t4 t5 tag).2.1 ≠
      (nativeK5WhiskeredActualFace t1 t2 t3 t4 t5
        (nativeK5WhiskeredFaceNext tag)).1 := by
  intro h
  have hh := congrArg
    (fun route : NativeK5GlobalRoute t1 t2 t3 t4 t5 =>
      route.rootLeftRotationCount) h
  have htarget :
      (nativeK5WhiskeredActualFace t1 t2 t3 t4 t5 tag).2.1.rootLeftRotationCount =
        (nativeK5WhiskeredFaceRootCounts tag).2 :=
    congrArg Prod.snd (nativeK5WhiskeredFaceRootCounts_exact t1 t2 t3 t4 t5 tag)
  have hsource :
      (nativeK5WhiskeredActualFace t1 t2 t3 t4 t5
        (nativeK5WhiskeredFaceNext tag)).1.rootLeftRotationCount =
        (nativeK5WhiskeredFaceRootCounts (nativeK5WhiskeredFaceNext tag)).1 :=
    congrArg Prod.fst
      (nativeK5WhiskeredFaceRootCounts_exact t1 t2 t3 t4 t5
        (nativeK5WhiskeredFaceNext tag))
  have hcount :
      (nativeK5WhiskeredFaceRootCounts tag).2 =
        (nativeK5WhiskeredFaceRootCounts (nativeK5WhiskeredFaceNext tag)).1 := by
    calc
      _ = (nativeK5WhiskeredActualFace t1 t2 t3 t4 t5 tag).2.1.rootLeftRotationCount :=
        htarget.symm
      _ = (nativeK5WhiskeredActualFace t1 t2 t3 t4 t5
            (nativeK5WhiskeredFaceNext tag)).1.rootLeftRotationCount := by
        exact hh
      _ = _ := hsource
  cases tag <;>
    simp [nativeK5WhiskeredFaceRootCounts, nativeK5WhiskeredFaceNext] at hcount

/-- A separate, explicitly UNINHABITED-by-default source of
missing TYPE-valued F54 seam comparisons, one for every
consecutive anchored K₅ face. No 3-cell is inferred from
unequal raw routes or equality of old F55 shadows. -/
structure NativeK5WhiskeredFaceSeamEvidence where
  seam : ∀ tag : NativeK5WhiskeredFaceTag,
    NativeF55P92AssocComparison p
      (nativeK5WhiskeredActualFace t1 t2 t3 t4 t5 tag).2.1
      (nativeK5WhiskeredActualFace t1 t2 t3 t4 t5
        (nativeK5WhiskeredFaceNext tag)).1
  seam_zero_word : ∀ tag, (seam tag).p94cGroupWord = 0

/-- With a genuinely supplied Type-valued seam proof, one may
compose one actual original-face 3-cell with its seam. This is
a true P92B 3-cell on the original F54 source, not a word quotient. -/
def NativeK5WhiskeredFaceSeamEvidence.link
    (d : NativeK5WhiskeredFaceSeamEvidence t1 t2 t3 t4 t5)
    (tag : NativeK5WhiskeredFaceTag) :
    NativeF55P92AssocComparison p
      (nativeK5WhiskeredActualFace t1 t2 t3 t4 t5 tag).1
      (nativeK5WhiskeredActualFace t1 t2 t3 t4 t5
        (nativeK5WhiskeredFaceNext tag)).1 :=
  .trans (nativeK5WhiskeredActualFace t1 t2 t3 t4 t5 tag).2.2
    (d.seam tag)

/-- Seam words must vanish independently for the P94D3I
oriented +1 N-charge to remain the EXACT global word. -/
theorem NativeK5WhiskeredFaceSeamEvidence.link_word
    (d : NativeK5WhiskeredFaceSeamEvidence t1 t2 t3 t4 t5)
    (tag : NativeK5WhiskeredFaceTag) :
    (NativeK5WhiskeredFaceSeamEvidence.link t1 t2 t3 t4 t5 d tag).p94cGroupWord =
      (nativeK5WhiskeredActualFace t1 t2 t3 t4 t5 tag).2.2.p94cGroupWord := by
  change
    (nativeK5WhiskeredActualFace t1 t2 t3 t4 t5 tag).2.2.p94cGroupWord +
      (d.seam tag).p94cGroupWord =
        (nativeK5WhiskeredActualFace t1 t2 t3 t4 t5 tag).2.2.p94cGroupWord
  rw [d.seam_zero_word tag]
  exact add_zero _

#print axioms KuuNativeF45Tree.DepthRotationRoute.rootLeftRotationCount
#print axioms nativeK5WhiskeredFaceRootCounts_exact
#print axioms nativeK5WhiskeredFace_next_route_ne
#print axioms NativeK5WhiskeredFaceSeamEvidence
#print axioms NativeK5WhiskeredFaceSeamEvidence.link
#print axioms NativeK5WhiskeredFaceSeamEvidence.link_word

end FiveNativeStages
end
end Kuu.F112.Physical
