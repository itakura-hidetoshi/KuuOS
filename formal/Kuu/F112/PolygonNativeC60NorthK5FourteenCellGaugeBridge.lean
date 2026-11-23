import Kuu.F112.PolygonNativeC60NorthK5GaugeBoundaryBridge
import Kuu.F112.PolygonNativeF55P94DK5FourteenCellNonabelianPasting
import Mathlib.Tactic

/-!
# F112 C60 north pentagon: real physical gauge and ORIGINAL 14D K5 pasting

Conditional bridge on five GENUINE F45 stages at the actual C60 north
pentagon. Keep original 182-site gauge field and P94C Type-valued
nine-face word as different typed observers; no equation between them
is assumed. Their combined statement retains:
 - real C60 north-face gauge holonomy under a frame change;
 - original nine-face shadow zero but independent N-charge one;
 - old P94A typed filler obstruction under algebraic reframing;
 - equality of 14D scalar square count;
 - inequality of 14D original free-group and raw proof histories.

The noncommutative 14D statements are relative to exact raw witnesses,
not to a chosen 15D quotient. No physical gauge transformation is
promoted to higher equivalence or globally glued by this theorem.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uA uD vD uE vE
variable {A : Type uA} [AddCommGroup A]
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

section NorthPentagonFiveStage

variable {a b : D} {x y : E}
variable {n₁ n₂ n₃ n₄ n₅ m₁ m₂ m₃ m₄ m₅ : Nat}
variable {p₀ p₁ p₂ p₃ p₄ p₅ : KuuNativeBlocks a b}
variable {q₀ q₁ q₂ q₃ q₄ q₅ : KuuNativeBlocks x y}
variable
  (t1 : KuuNativeF45Tree (.pentagon .north) n₁ m₁ p₀ q₀ p₁ q₁)
  (t2 : KuuNativeF45Tree (.pentagon .north) n₂ m₂ p₁ q₁ p₂ q₂)
  (t3 : KuuNativeF45Tree (.pentagon .north) n₃ m₃ p₂ q₂ p₃ q₃)
  (t4 : KuuNativeF45Tree (.pentagon .north) n₄ m₄ p₃ q₃ p₄ q₄)
  (t5 : KuuNativeF45Tree (.pentagon .north) n₅ m₅ p₄ q₄ p₅ q₅)

/-- The genuine C60 north gauge can be varied without changing its
physical face curvature; simultaneously, the typed K5 gauge obstruction
and original raw 14D noncommutativity remain visible. The conjunction
does NOT identify these independent observers or assert 15D descent. -/
theorem nativeC60NorthK5_fourteen_originalGaugeObstruction
    (field : NativeC60IncidenceGaugeField A)
    (phi : NativeC60LocalGauge A)
    (g : NativeF55P94CWord) :
    nativeC60FaceGaugeCurvature
        (nativeC60GaugeTransform field phi) (.pentagon .north) =
      nativeC60FaceGaugeCurvature field (.pentagon .north) ∧
    nativeF55P94CWordToShadow
      (nativeK5GaugeReframe g (nativeK5GenuineGaugeBoundary t1 t2 t3 t4 t5)) = 0 ∧
    nativeK5NaturalityCount
      (nativeK5GaugeReframe g (nativeK5GenuineGaugeBoundary t1 t2 t3 t4 t5)) = 1 ∧
    nativeK5GaugeReframe g (nativeK5GenuineGaugeBoundary t1 t2 t3 t4 t5)
        ∉ nativeK5P94ATypedNormalClosure D E ∧
    (nativeK5PentagonatorFifteenLeftFirst t1 t2 t3 t4 t5).squareCount =
      (nativeK5PentagonatorFifteenRightFirst t1 t2 t3 t4 t5).squareCount ∧
    (nativeK5PentagonatorFifteenLeftFirst t1 t2 t3 t4 t5).historyWord ≠
      (nativeK5PentagonatorFifteenRightFirst t1 t2 t3 t4 t5).historyWord ∧
    nativeK5PentagonatorFifteenLeftFirst t1 t2 t3 t4 t5 ≠
      nativeK5PentagonatorFifteenRightFirst t1 t2 t3 t4 t5 := by
  have hlocal :=
    nativeC60NorthK5_gauge_invariance_and_typed_obstruction
      t1 t2 t3 t4 t5 field phi g
  refine ⟨hlocal.1, hlocal.2.1, hlocal.2.2.1,
    hlocal.2.2.2, ?_, ?_, ?_⟩
  · exact nativeK5PentagonatorFifteen_integerBlind t1 t2 t3 t4 t5
  · exact nativeK5PentagonatorFifteen_history_ne t1 t2 t3 t4 t5
  · exact nativeK5PentagonatorFifteen_raw_ne t1 t2 t3 t4 t5

end NorthPentagonFiveStage

#print axioms nativeC60NorthK5_fourteen_originalGaugeObstruction

end
end Kuu.F112.Physical
