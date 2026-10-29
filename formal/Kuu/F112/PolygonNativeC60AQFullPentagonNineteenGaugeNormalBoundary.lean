import Kuu.F112.PolygonNativeC60AQFullPentagonFiniteGaugeNormalTransport
import Kuu.F112.PolygonNativeC60AQFullPentagonNineteenNormalDescent

/-!
# F112-P94D3EZ — original C60 18D complete evidence, 19D gauge boundary

EZ specializes the finite signed typed normal covariance of a GIVEN
candidate 19D path to the ORIGINAL DS noncommutative complete 18D
FreeGroup, including actual original 14D--18D dependent boundaries.

For any original four-composable 17D paths and any ACTUALLY PROVIDED
candidate 19D typed filler:
  (i) conjugating every signed primitive defect in order equals
      conjugating the exact ORIGINAL long⁻¹ * short full free-word ratio;
 (ii) the gauge-conjugated ratio is NONIDENTITY in the original
      complete-evidence group;
(iii) the same ratio belongs to both the path-selected normal kernel
      and the independently selected DT all-pentagon normal kernel;
 (iv) its image is identity in each separately declared quotient;
  (v) the path-selected normal closure is invariant under a common
      gauge conjugation of its actual finite primitive relators;
 (vi) descent of a proposed full 18D endomorphism is equivalent to
      explicit checks on the actual path-occurring typed primitives.

No inclusion of the two normal subgroups is asserted; only their
common particular original defect is certified. No hypothetical
19D filler is manufactured; no raw Type-valued history is equated
and no quotient is passed off as full 18D evidence preservation.

Strict Kuu primary, independent Kuu a presentation, DS no-go,
107 public roots, no Gray, no abelianization, no sorry/new axiom;
pinned Lean/mathlib, append-only/same-root.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u w

section OriginalC60FullEvidenceGaugeBoundary

variable {L : NativeC60AXLayer.{u}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- Every actual signed 19D generator defect, conjugated by the SAME
complete original 18D free group element, multiplies IN PATH ORDER
to the exact gauge-conjugated long⁻¹ * short original 18D word. -/
theorem nativeC60EZNineteen_gauge_signed_ratio
    {a b d e z : (nativeC60DQSeventeenLayer S F).Total}
    (f : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b)
    (g : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) b d)
    (h : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) d e)
    (k : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) e z)
    (T : NativeC60AXSignature (nativeC60DSNineteenLayer S F))
    (filler : NativeC60AXStep T
      (nativeC60DSPackEighteen S F
        (nativeC60DRPentagonLong S F f g h k))
      (nativeC60DSPackEighteen S F
        (nativeC60DRPentagonShort S F f g h k)))
    (c : NativeC60DTFullFree S F) :
    ((nativeC60EYSignedAtoms T filler).map (fun atom =>
      c * nativeC60EYSignedDefect T
          (nativeC60DSNineteenHolonomy S F) atom * c⁻¹)).prod =
      c * ((nativeC60DSFreeWord S F
        (nativeC60DRPentagonLong S F f g h k))⁻¹ *
        nativeC60DSFreeWord S F
          (nativeC60DRPentagonShort S F f g h k)) * c⁻¹ := by
  rw [nativeC60EZConjugation_path_product
    T (nativeC60DSNineteenHolonomy S F) filler c]
  rw [nativeC60EXPentagon_defect_eq_full_ratio S F f g h k T filler]

/-- Gauge conjugating the ACTUAL finite original 19D path-relators
does not alter the exact path-selected least DT normal subgroup.
No 18D generator code has been deleted or abelianized. -/
theorem nativeC60EZNineteen_conjugated_path_normal_eq
    {a b d e z : (nativeC60DQSeventeenLayer S F).Total}
    (f : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b)
    (g : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) b d)
    (h : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) d e)
    (k : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) e z)
    (T : NativeC60AXSignature (nativeC60DSNineteenLayer S F))
    (filler : NativeC60AXStep T
      (nativeC60DSPackEighteen S F
        (nativeC60DRPentagonLong S F f g h k))
      (nativeC60DSPackEighteen S F
        (nativeC60DRPentagonShort S F f g h k)))
    (c : NativeC60DTFullFree S F) :
    nativeC60DTNormalClosure
      (nativeC60EZConjugatedSelectedPairs T
        (nativeC60DSNineteenHolonomy S F)
        (nativeC60EYPathAtoms T filler) c) =
      nativeC60DTNormalClosure
        (nativeC60EYSelectedPairs T
          (nativeC60DSNineteenHolonomy S F)
          (nativeC60EYPathAtoms T filler)) :=
  nativeC60EZConjugatedNormal_eq T
    (nativeC60DSNineteenHolonomy S F)
    (nativeC60EYPathAtoms T filler) c

/-- Fundamental original-evidence distinction: even after arbitrary
inner gauge conjugation the full pentagon defect remains nonidentity,
while belonging simultaneously to two DIFFERENT selected relative
normal kernels. This makes no claim of an inclusion of full kernels. -/
theorem nativeC60EZNineteen_gauge_two_kernels_nontrivial
    {a b d e z : (nativeC60DQSeventeenLayer S F).Total}
    (f : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b)
    (g : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) b d)
    (h : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) d e)
    (k : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) e z)
    (T : NativeC60AXSignature (nativeC60DSNineteenLayer S F))
    (filler : NativeC60AXStep T
      (nativeC60DSPackEighteen S F
        (nativeC60DRPentagonLong S F f g h k))
      (nativeC60DSPackEighteen S F
        (nativeC60DRPentagonShort S F f g h k)))
    (c : NativeC60DTFullFree S F) :
    let defect := (nativeC60DSFreeWord S F
      (nativeC60DRPentagonLong S F f g h k))⁻¹ *
        nativeC60DSFreeWord S F
          (nativeC60DRPentagonShort S F f g h k)
    c * defect * c⁻¹ ∈
      nativeC60DTNormalClosure
        (nativeC60EYSelectedPairs T
          (nativeC60DSNineteenHolonomy S F)
          (nativeC60EYPathAtoms T filler)) ∧
    c * defect * c⁻¹ ∈
      nativeC60DTPentagonNormalClosure S F ∧
    c * defect * c⁻¹ ≠ 1 := by
  dsimp only
  constructor
  · apply nativeC60EZConjugation_stable_DT
      (nativeC60EYSelectedPairs T
        (nativeC60DSNineteenHolonomy S F)
        (nativeC60EYPathAtoms T filler)) c
    exact nativeC60EYNineteen_ratio_mem_path_normal S F f g h k T filler
  constructor
  · apply nativeC60EZConjugation_stable_DT
      (nativeC60DTPentagonPairs S F) c
    exact nativeC60EYNineteen_ratio_mem_DT S F f g h k
  · apply nativeC60EZConjugate_ne_one c
    rw [← nativeC60EXPentagon_defect_eq_full_ratio S F f g h k T filler]
    exact nativeC60EXPentagon_defect_ne_one S F f g h k T filler

/-- The exact same conjugated original evidence defect becomes 1 in
BOTH EXPLICITLY CHOSEN relative quotients. The ORIGINAL free word
remains nonidentity as separately established above. -/
theorem nativeC60EZNineteen_gauge_two_quotients_one
    {a b d e z : (nativeC60DQSeventeenLayer S F).Total}
    (f : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b)
    (g : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) b d)
    (h : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) d e)
    (k : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) e z)
    (T : NativeC60AXSignature (nativeC60DSNineteenLayer S F))
    (filler : NativeC60AXStep T
      (nativeC60DSPackEighteen S F
        (nativeC60DRPentagonLong S F f g h k))
      (nativeC60DSPackEighteen S F
        (nativeC60DRPentagonShort S F f g h k)))
    (c : NativeC60DTFullFree S F) :
    let defect := (nativeC60DSFreeWord S F
      (nativeC60DRPentagonLong S F f g h k))⁻¹ *
        nativeC60DSFreeWord S F
          (nativeC60DRPentagonShort S F f g h k)
    (QuotientGroup.mk' (nativeC60DTNormalClosure
      (nativeC60EYSelectedPairs T
        (nativeC60DSNineteenHolonomy S F)
        (nativeC60EYPathAtoms T filler))))
      (c * defect * c⁻¹) = 1 ∧
    (QuotientGroup.mk' (nativeC60DTPentagonNormalClosure S F))
      (c * defect * c⁻¹) = 1 := by
  dsimp only
  have h := nativeC60EZNineteen_gauge_two_kernels_nontrivial
    S F f g h k T filler c
  dsimp only at h
  constructor
  · apply MonoidHom.mem_ker.mp
    rw [nativeC60DTQuotient_kernel
      (nativeC60EYSelectedPairs T
        (nativeC60DSNineteenHolonomy S F)
        (nativeC60EYPathAtoms T filler))]
    exact h.1
  · apply MonoidHom.mem_ker.mp
    rw [nativeC60DTPentagon_kernel_exact]
    exact h.2.1

/-- Necessary and sufficient test for an endomorphism of the ORIGINAL
complete noncommutative 18D free group to descend to the selected
actual path-local relative quotient: test exactly those ORIGINAL
typed generators which occurred in this particular signed 19D path. -/
theorem nativeC60EZNineteen_transport_factor_iff
    {a b d e z : (nativeC60DQSeventeenLayer S F).Total}
    (f : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b)
    (g : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) b d)
    (h : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) d e)
    (k : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) e z)
    (T : NativeC60AXSignature (nativeC60DSNineteenLayer S F))
    (filler : NativeC60AXStep T
      (nativeC60DSPackEighteen S F
        (nativeC60DRPentagonLong S F f g h k))
      (nativeC60DSPackEighteen S F
        (nativeC60DRPentagonShort S F f g h k)))
    (τ : NativeC60DTFullFree S F →* NativeC60DTFullFree S F) :
    (∃ induced : NativeC60DTQuotient
        (nativeC60EYSelectedPairs T
          (nativeC60DSNineteenHolonomy S F)
          (nativeC60EYPathAtoms T filler)) →*
      NativeC60DTQuotient
        (nativeC60EYSelectedPairs T
          (nativeC60DSNineteenHolonomy S F)
          (nativeC60EYPathAtoms T filler)),
      induced.comp (QuotientGroup.mk' (nativeC60DTNormalClosure
        (nativeC60EYSelectedPairs T
          (nativeC60DSNineteenHolonomy S F)
          (nativeC60EYPathAtoms T filler)))) =
        (QuotientGroup.mk' (nativeC60DTNormalClosure
          (nativeC60EYSelectedPairs T
            (nativeC60DSNineteenHolonomy S F)
            (nativeC60EYPathAtoms T filler)))).comp τ) ↔
      ∀ atom : NativeC60EYPrimitive T,
        atom ∈ nativeC60EYPathAtoms T filler →
          (QuotientGroup.mk' (nativeC60DTNormalClosure
            (nativeC60EYSelectedPairs T
              (nativeC60DSNineteenHolonomy S F)
              (nativeC60EYPathAtoms T filler))))
            (τ (nativeC60EYPrimitiveDefect T
              (nativeC60DSNineteenHolonomy S F) atom)) = 1 :=
  nativeC60EZSelectedTransport_factor_iff T
    (nativeC60DSNineteenHolonomy S F)
    (nativeC60EYPathAtoms T filler) τ

end OriginalC60FullEvidenceGaugeBoundary

#print axioms nativeC60EZNineteen_gauge_signed_ratio
#print axioms nativeC60EZNineteen_conjugated_path_normal_eq
#print axioms nativeC60EZNineteen_gauge_two_kernels_nontrivial
#print axioms nativeC60EZNineteen_gauge_two_quotients_one
#print axioms nativeC60EZNineteen_transport_factor_iff

end
end Kuu.F112.Physical
