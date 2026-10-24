import Kuu.F112.PolygonNativeF55P94DK5OrientedNaturalityObstruction
import Mathlib.Tactic

/-!
# F112 — K5 independent typed C60 gauge, replacing graph as coherence authority

The previously verified 14-vertex/21-edge/9-face K5 graph is
finite *geometry*, not a coherence proof.  The forward presentation
uses only the NINE ACTUAL oriented dependent F45/F54/F55/P92B
face certificates and the genuine typed P94A/P94C2 four-cell kernel.

Their cyclically ordered noncommutative gauge boundary is built
directly from those actual face proof terms.  A change of algebraic
frame acts by CONJUGATION, never by permuting noncommutative words.
The two genuinely conserved receivers (full original F55 shadow
and independent P92B N-charge) are invariant under every reframe.

Since its N-charge is +1, no change of gauge puts this boundary
in the existing P94A typed 4-cell normal closure; neither a
global typed sphere nor a 4D pentagonator is fabricated. A
Type-valued gauge change needs an actual higher comparison witness,
and is not inferred from an algebraic frame change.

No C60 graph equality used as a descent condition, no Gray,
no new logical axioms, sorry/admit or removal of historical results.
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

/-- A noncommutative change of local presentation at one chosen
3-cell word boundary, not a new physical C60 edge. -/
def nativeK5GaugeReframe
    (g w : NativeF55P94CWord) : NativeF55P94CWord :=
  g + w - g

theorem nativeK5GaugeReframe_identity (w : NativeF55P94CWord) :
    nativeK5GaugeReframe 0 w = w := by
  simp [nativeK5GaugeReframe]

theorem nativeK5GaugeReframe_comp
    (g h w : NativeF55P94CWord) :
    nativeK5GaugeReframe g (nativeK5GaugeReframe h w) =
      nativeK5GaugeReframe (g + h) w := by
  simp [nativeK5GaugeReframe, sub_eq_add_neg, neg_add_rev, add_assoc]

/-- The new independent naturality count is gauge invariant.
Do not abelianize the underlying source word. -/
theorem nativeK5GaugeReframe_NCount
    (g w : NativeF55P94CWord) :
    nativeK5NaturalityCount (nativeK5GaugeReframe g w) =
      nativeK5NaturalityCount w := by
  simp only [nativeK5GaugeReframe, map_sub, map_add]
  abel

/-- The FULL original two-signed-charge plus odd-phase shadow
is also gauge invariant; the zero older shadow will not
erase the separate nonzero naturality gauge obstruction. -/
theorem nativeK5GaugeReframe_shadow
    (g w : NativeF55P94CWord) :
    nativeF55P94CWordToShadow (nativeK5GaugeReframe g w) =
      nativeF55P94CWordToShadow w := by
  simp only [nativeK5GaugeReframe, map_sub, map_add]
  abel

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

/-- The genuine K5 boundary in the oriented global cyclic order:
P7,N0,P5,P8,N1,P3,P6,N2,P4. Each summand is read from an
ACTUAL, dependent original P92B Type-valued source face,
never from a graph-only loop or a guessed signed shadow. -/
def nativeK5GenuineGaugeBoundary : NativeF55P94CWord :=
  (nativeK5AnchoredFace t1 t2 t3 t4 t5 .pentagon7).2.2.2.p94cGroupWord +
  (nativeK5AnchoredFace t1 t2 t3 t4 t5 .square0).2.2.2.p94cGroupWord +
  (nativeK5AnchoredFace t1 t2 t3 t4 t5 .pentagon5).2.2.2.p94cGroupWord +
  (nativeK5AnchoredFace t1 t2 t3 t4 t5 .pentagon8).2.2.2.p94cGroupWord +
  (nativeK5AnchoredFace t1 t2 t3 t4 t5 .square1).2.2.2.p94cGroupWord +
  (nativeK5AnchoredFace t1 t2 t3 t4 t5 .pentagon3).2.2.2.p94cGroupWord +
  (nativeK5AnchoredFace t1 t2 t3 t4 t5 .pentagon6).2.2.2.p94cGroupWord +
  (nativeK5AnchoredFace t1 t2 t3 t4 t5 .square2).2.2.2.p94cGroupWord +
  (nativeK5AnchoredFace t1 t2 t3 t4 t5 .pentagon4).2.2.2.p94cGroupWord

/-- Genuine face-based naturality number +1. No reordering of
noncommutative summands is used; the calculation occurs only
after applying the integer homomorphism. -/
theorem nativeK5GenuineGaugeBoundary_NCount_one :
    nativeK5NaturalityCount
      (nativeK5GenuineGaugeBoundary t1 t2 t3 t4 t5) = 1 := by
  simp only [nativeK5GenuineGaugeBoundary, map_add]
  change
    nativeK5AnchoredFaceNCount t1 t2 t3 t4 t5 .pentagon7 +
    nativeK5AnchoredFaceNCount t1 t2 t3 t4 t5 .square0 +
    nativeK5AnchoredFaceNCount t1 t2 t3 t4 t5 .pentagon5 +
    nativeK5AnchoredFaceNCount t1 t2 t3 t4 t5 .pentagon8 +
    nativeK5AnchoredFaceNCount t1 t2 t3 t4 t5 .square1 +
    nativeK5AnchoredFaceNCount t1 t2 t3 t4 t5 .pentagon3 +
    nativeK5AnchoredFaceNCount t1 t2 t3 t4 t5 .pentagon6 +
    nativeK5AnchoredFaceNCount t1 t2 t3 t4 t5 .square2 +
    nativeK5AnchoredFaceNCount t1 t2 t3 t4 t5 .pentagon4 = 1
  simp [nativeK5AnchoredFaceNCount_exact, nativeK5FaceExpectedNCount]

/-- Every genuinely anchored face contributes its REAL old shadow,
so the complete original F55 signed/odd coordinate balances. -/
theorem nativeK5GenuineGaugeBoundary_shadow_zero :
    nativeF55P94CWordToShadow
      (nativeK5GenuineGaugeBoundary t1 t2 t3 t4 t5) = 0 := by
  simp only [nativeK5GenuineGaugeBoundary, map_add,
    NativeF55P92AssocComparison.p94cGroupWord_shadow]
  simp [nativeK5AnchoredFace_fullShadow, nativeK5CandidateFaceShadow,
    nativeK5FaceTagFin]

/-- Genuine typed P94A relations conserve the naturality gauge
obstruction: arbitrary algebraic reframing CANNOT make the
nine-face boundary a genuine existing P94A/P94C2 four-cell. -/
theorem nativeK5GenuineGaugeBoundary_no_old_filler_under_reframe
    (g : NativeF55P94CWord) :
    nativeK5GaugeReframe g
      (nativeK5GenuineGaugeBoundary t1 t2 t3 t4 t5) ∉
        nativeK5P94ATypedNormalClosure D E := by
  intro h
  have hz := nativeK5P94ATypedNormalClosure_le_NCount_ker (D := D) (E := E) h
  change nativeK5NaturalityCount
    (nativeK5GaugeReframe g
      (nativeK5GenuineGaugeBoundary t1 t2 t3 t4 t5)) = 0 at hz
  rw [nativeK5GaugeReframe_NCount,
    nativeK5GenuineGaugeBoundary_NCount_one] at hz
  norm_num at hz

/-- Under every gauge change, the complete old signed/odd
shadow stays ZERO while the separate naturality number stays ONE. -/
theorem nativeK5GenuineGaugeBoundary_fullGaugeObstruction
    (g : NativeF55P94CWord) :
    nativeF55P94CWordToShadow
        (nativeK5GaugeReframe g
          (nativeK5GenuineGaugeBoundary t1 t2 t3 t4 t5)) = 0 ∧
    nativeK5NaturalityCount
        (nativeK5GaugeReframe g
          (nativeK5GenuineGaugeBoundary t1 t2 t3 t4 t5)) = 1 := by
  constructor
  · rw [nativeK5GaugeReframe_shadow,
      nativeK5GenuineGaugeBoundary_shadow_zero]
  · rw [nativeK5GaugeReframe_NCount,
      nativeK5GenuineGaugeBoundary_NCount_one]

end FiveNativeStages

/-- Any ACTUAL Type-valued P94A four-cell is sound under genuine
gauge comparison: no algebraic gauge frame creates the missing
source 4-cell. This is a higher-source statement, not merely
an untyped word-level equivalence. -/
theorem nativeK5TypedFourCell_gauge_NCount_sound
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55P92AssocComparison p r s}
    (frame : NativeF55P94CWord)
    (comparison : NativeF55P94UnitFourCell f g) :
    nativeK5NaturalityCount (nativeK5GaugeReframe frame f.p94cGroupWord) =
      nativeK5NaturalityCount (nativeK5GaugeReframe frame g.p94cGroupWord) := by
  rw [nativeK5GaugeReframe_NCount, nativeK5GaugeReframe_NCount]
  exact comparison.nCount_sound

#print axioms nativeK5GaugeReframe_comp
#print axioms nativeK5GaugeReframe_NCount
#print axioms nativeK5GaugeReframe_shadow
#print axioms nativeK5GenuineGaugeBoundary_NCount_one
#print axioms nativeK5GenuineGaugeBoundary_shadow_zero
#print axioms nativeK5GenuineGaugeBoundary_no_old_filler_under_reframe
#print axioms nativeK5GenuineGaugeBoundary_fullGaugeObstruction
#print axioms nativeK5TypedFourCell_gauge_NCount_sound

end
end Kuu.F112.Physical
