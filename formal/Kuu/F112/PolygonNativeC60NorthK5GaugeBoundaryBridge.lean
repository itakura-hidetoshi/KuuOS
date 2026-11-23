import Kuu.F112.PolygonNativeC60PhysicalGaugeAtlas
import Kuu.F112.PolygonNativeC60K5TypedGaugeCoherence
import Mathlib.Tactic

/-!
# F112 C60 north-pentagon gauge / genuine typed K5 boundary interface

Keep two INDEPENDENT gauge actions visible:
(1) the real 182-site C60 incidence connection on the original north face,
(2) conjugation of the nine ORIGINAL dependent F45/F54/F55/P92B K5 faces.

The SAME five source-dependent F45 stage arguments are over the actual
C60 north pentagon. Their existence is an explicit INPUT: this file does
not manufacture a five-stage loop or identify physical and higher gauges.

The equality of physical holonomy after frame change does NOT establish
a Type-valued pentagonator or a global gluing/descent theorem. The separate
typed N-charge obstruction is preserved without abelianizing raw words.
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

/-- Conditional genuine C60/K5 bridge: the REAL north-pentagon
physical curvature is frame-invariant, while the ORIGINAL nine
Type-valued source faces have N-charge 1 and cannot be filled by
the named old typed P94A kernel under any algebraic reframe.

These are distinct gauges and two separate obstructions; no
unproved compatibility morphism is silently introduced. -/
theorem nativeC60NorthK5_gauge_invariance_and_typed_obstruction
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
        ∉ nativeK5P94ATypedNormalClosure D E := by
  refine ⟨nativeC60FaceGaugeCurvature_invariant field phi (.pentagon .north), ?_, ?_, ?_⟩
  · exact (nativeK5GenuineGaugeBoundary_fullGaugeObstruction t1 t2 t3 t4 t5 g).1
  · exact (nativeK5GenuineGaugeBoundary_fullGaugeObstruction t1 t2 t3 t4 t5 g).2
  · exact nativeK5GenuineGaugeBoundary_no_old_filler_under_reframe t1 t2 t3 t4 t5 g

/-- A conditional nonzero physical north-face curvature cannot be
removed by a chart change. It is not the K5 N-charge: they are
independent quantities on different source types. -/
theorem nativeC60NorthK5_nonflat_and_no_old_filler
    (field : NativeC60IncidenceGaugeField A)
    (phi : NativeC60LocalGauge A)
    (g : NativeF55P94CWord)
    (hcurv : nativeC60FaceGaugeCurvature field (.pentagon .north) ≠ 0) :
    nativeC60FaceGaugeCurvature
        (nativeC60GaugeTransform field phi) (.pentagon .north) ≠ 0 ∧
    nativeK5GaugeReframe g (nativeK5GenuineGaugeBoundary t1 t2 t3 t4 t5)
        ∉ nativeK5P94ATypedNormalClosure D E := by
  constructor
  · exact nativeC60FaceGaugeCurvature_no_flat_gauge field (.pentagon .north) hcurv phi
  · exact nativeK5GenuineGaugeBoundary_no_old_filler_under_reframe t1 t2 t3 t4 t5 g

end NorthPentagonFiveStage

#print axioms nativeC60NorthK5_gauge_invariance_and_typed_obstruction
#print axioms nativeC60NorthK5_nonflat_and_no_old_filler

end
end Kuu.F112.Physical
