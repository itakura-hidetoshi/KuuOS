import Kuu.F112.PolygonNativeC60FiniteSignedGaugeSector
import Mathlib.Tactic.Group

/-!
# F112-P94D3CW — original typed parallel-pair CN recovery

Each finite pair g h⁻¹ uses two COMPLETE original BC generators with the
same genuinely dependent 15D source and target. CN decoding followed by
the existing fork embedding recovers its FULL noncommutative BW holonomy,
and hence also any finite concatenation of such typed original pairs.

The sufficient outer-AQ closure condition is stated separately: all
original framed strict loops must have a genuinely typed unframed
parallel-pair lift with exact complete BW holonomy. CT/CU/CV classify
the physical endpoints, but do NOT yet provide that unprefix lift of
EVERY original framed generator certificate. No kernel triviality is
asserted without the remaining premise. No new geometric 16-cell,
no Gray reconstruction, and no axioms or sorry.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uCW

section OriginalTypedPairs

variable {L : NativeC60AXLayer.{uCW}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- A finite original 16D path in which every pair has EXACT original
15D A/B endpoints. Each original generator is retained in Type, not
replaced by a code or an abstract graph edge. -/
def nativeC60CWPairChain {A B : L.Total} :
    List ((nativeC60BCClosedSignature S F).Gen A B ×
      (nativeC60BCClosedSignature S F).Gen A B) →
      NativeC60CASignedChain S F A A
  | [] => .nil A
  | (g, h) :: rest => .pos g (.neg h (nativeC60CWPairChain rest))

/-- Every original 16D witness contributes its exact signed provenance,
including all finite AQ contexts and the unsimplified primitive payload. -/
theorem nativeC60CWPairChain_codes {A B : L.Total}
    (pairs : List ((nativeC60BCClosedSignature S F).Gen A B ×
      (nativeC60BCClosedSignature S F).Gen A B)) :
    nativeC60CAChainSignedCodes S F (nativeC60CWPairChain S F pairs) =
      pairs.flatMap (fun gh =>
        [(nativeC60BVGeneratorCode S F gh.1, true),
         (nativeC60BVGeneratorCode S F gh.2, false)]) := by
  induction pairs with
  | nil => rfl
  | cons gh tail ih =>
      rcases gh with ⟨g, h⟩
      simp [nativeC60CWPairChain, nativeC60CAChainSignedCodes, ih]

/-- Exact CN reconstruction on one ORIGINAL positive BC certificate.
The selected baseline contributes identity to the decoder, but its
full code is not discarded before reconstruction. -/
theorem nativeC60CWParallel_letter_reconstruct {A B : L.Total}
    (base g : (nativeC60BCClosedSignature S F).Gen A B) :
    nativeC60CNEmbed S F base
      (nativeC60CNRetraction S F base
        (FreeGroup.of (nativeC60BVGeneratorCode S F g))) =
      FreeGroup.of (nativeC60BVGeneratorCode S F g) *
        (FreeGroup.of (nativeC60BVGeneratorCode S F base))⁻¹ := by
  classical
  by_cases hg : g = base
  · subst g
    simp only [nativeC60CNRetraction, FreeGroup.lift_apply_of]
    rw [nativeC60CNDecodeLetter_base, map_one]
    exact (mul_inv_cancel _).symm
  · let i : NativeC60CNForkAlphabet S F base := ⟨g, hg⟩
    have hdecode :
        nativeC60CNRetraction S F base
          (FreeGroup.of (nativeC60BVGeneratorCode S F g)) =
            FreeGroup.of i := by
      simpa only [nativeC60CNRetraction, FreeGroup.lift_apply_of] using
        (nativeC60CNDecodeLetter_letter S F base i)
    rw [hdecode]
    simp only [nativeC60CNEmbed, FreeGroup.lift_apply_of]
    rfl

/-- For any two genuine parallel BC certificates, the base-letter
factors cancel in the NONCOMMUTATIVE group in the correct order. -/
theorem nativeC60CWParallel_pair_reconstruct {A B : L.Total}
    (base g h : (nativeC60BCClosedSignature S F).Gen A B) :
    nativeC60CNEmbed S F base
      (nativeC60CNRetraction S F base
        (FreeGroup.of (nativeC60BVGeneratorCode S F g) *
          (FreeGroup.of (nativeC60BVGeneratorCode S F h))⁻¹)) =
      FreeGroup.of (nativeC60BVGeneratorCode S F g) *
        (FreeGroup.of (nativeC60BVGeneratorCode S F h))⁻¹ := by
  simp only [map_mul, map_inv]
  rw [nativeC60CWParallel_letter_reconstruct S F base g,
      nativeC60CWParallel_letter_reconstruct S F base h]
  group

/-- The genuine dependent CA holonomy of one original pair followed
by a continuation is the exact product of its two signed BW letters. -/
theorem nativeC60CWPairChain_holonomy_cons {A B : L.Total}
    (g h : (nativeC60BCClosedSignature S F).Gen A B)
    (rest : List ((nativeC60BCClosedSignature S F).Gen A B ×
      (nativeC60BCClosedSignature S F).Gen A B)) :
    nativeC60BWFreeHolonomy S F
        (nativeC60CAChainStep S F
          (nativeC60CWPairChain S F ((g, h) :: rest))) =
      (FreeGroup.of (nativeC60BVGeneratorCode S F g) *
        (FreeGroup.of (nativeC60BVGeneratorCode S F h))⁻¹) *
      nativeC60BWFreeHolonomy S F
        (nativeC60CAChainStep S F (nativeC60CWPairChain S F rest)) := by
  change FreeGroup.of (nativeC60BVGeneratorCode S F g) *
      ((FreeGroup.of (nativeC60BVGeneratorCode S F h))⁻¹ *
        nativeC60BWFreeHolonomy S F
          (nativeC60CAChainStep S F (nativeC60CWPairChain S F rest))) = _
  group

/-- MAIN CW finite-pair theorem: decoding the COMPLETE original BW
word and re-embedding reconstructs EVERY genuinely typed parallel-pair
closed chain. No abelianization, no loss of the original BC witnesses. -/
theorem nativeC60CWPairChain_complete_CN {A B : L.Total}
    (base : (nativeC60BCClosedSignature S F).Gen A B)
    (pairs : List ((nativeC60BCClosedSignature S F).Gen A B ×
      (nativeC60BCClosedSignature S F).Gen A B)) :
    nativeC60CNEmbed S F base
      (nativeC60CNRetraction S F base
        (nativeC60BWFreeHolonomy S F
          (nativeC60CAChainStep S F (nativeC60CWPairChain S F pairs)))) =
      nativeC60BWFreeHolonomy S F
        (nativeC60CAChainStep S F (nativeC60CWPairChain S F pairs)) := by
  induction pairs with
  | nil =>
      change nativeC60CNEmbed S F base
        (nativeC60CNRetraction S F base 1) = 1
      simp
  | cons gh rest ih =>
      rcases gh with ⟨g, h⟩
      rw [nativeC60CWPairChain_holonomy_cons S F g h rest]
      calc
        _ = nativeC60CNEmbed S F base
              (nativeC60CNRetraction S F base
                (FreeGroup.of (nativeC60BVGeneratorCode S F g) *
                  (FreeGroup.of (nativeC60BVGeneratorCode S F h))⁻¹)) *
            nativeC60CNEmbed S F base
              (nativeC60CNRetraction S F base
                (nativeC60BWFreeHolonomy S F
                  (nativeC60CAChainStep S F (nativeC60CWPairChain S F rest)))) := by
            rw [map_mul, map_mul]
        _ = _ := by
          rw [nativeC60CWParallel_pair_reconstruct S F base g h, ih]

/-- Exact complete-code pair normality is sufficient for actual CN
reconstruction on an arbitrary original typed A-based 16D loop. -/
theorem nativeC60CWOriginal_loop_complete_CN_of_pairs {A B : L.Total}
    (base : (nativeC60BCClosedSignature S F).Gen A B)
    (path : NativeC60CASignedChain S F A A)
    (hpair : ∃ pairs : List
      ((nativeC60BCClosedSignature S F).Gen A B ×
       (nativeC60BCClosedSignature S F).Gen A B),
      nativeC60CWPairChain S F pairs = path) :
    nativeC60CNEmbed S F base
      (nativeC60CNRetraction S F base
        (nativeC60BWFreeHolonomy S F (nativeC60CAChainStep S F path))) =
      nativeC60BWFreeHolonomy S F (nativeC60CAChainStep S F path) := by
  rcases hpair with ⟨pairs, hpairs⟩
  rw [← hpairs]
  exact nativeC60CWPairChain_complete_CN S F base pairs


end OriginalTypedPairs

section OuterContextObstruction

variable {L : NativeC60AXLayer.{uCW}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- Missing physical all-loop condition, made precise WITHOUT adopting
it as an axiom: every ACTUAL original framed signed loop must have a
complete-holonomy lift to finite typed original BC parallel pairs,
before outer finite AQ framing. CT/CU endpoint rigidity alone does not
give this all-generator unprefix claim. -/
def NativeC60CWOuterPairCodeComplete
    (outer : List Bool) (A B : L.Total) : Prop :=
  ∀ path : NativeC60CASignedChain S F
      (nativeC60BCContextTotal F outer A)
      (nativeC60BCContextTotal F outer A),
    ∃ pairs : List ((nativeC60BCClosedSignature S F).Gen A B ×
      (nativeC60BCClosedSignature S F).Gen A B),
      FreeGroup.mk (nativeC60CAChainSignedCodes S F path) =
        nativeC60BWFreePrefix S outer
          (nativeC60BWFreeHolonomy S F
            (nativeC60CAChainStep S F (nativeC60CWPairChain S F pairs)))

/-- Precisely isolates the remaining geometric obstruction:
an exact ORIGINAL typed pair lift of ALL outer-framed strict loops
forces the actual CN strict kernel to be trivial. The premise is
NOT derived here, nor is it confused with CV's two-boundary incidence.
This uses CR's complete necessary-and-sufficient kernel witness test. -/
theorem nativeC60CWStrict_kernel_trivial_of_outer_pair_codes
    (outer : List Bool) {A B : L.Total}
    (base : (nativeC60BCClosedSignature S F).Gen A B)
    (hlift : NativeC60CWOuterPairCodeComplete S F outer A B) :
    ¬ ∃ k : NativeC60CPKernel S F outer base, k ≠ 1 := by
  intro hkernel
  obtain ⟨path, hdecode, hfull⟩ :=
    (nativeC60CRKernel_nontrivial_iff_signed S F outer base).mp hkernel
  obtain ⟨pairs, hfactor⟩ := hlift path
  let q := nativeC60CWPairChain S F pairs
  have hunprefix :
      nativeC60BXFreeUnprefix S outer
        (FreeGroup.mk (nativeC60CAChainSignedCodes S F path)) =
      nativeC60BWFreeHolonomy S F (nativeC60CAChainStep S F q) := by
    rw [hfactor]
    exact nativeC60BXFreeUnprefix_prefix S outer _
  have hpair_decode :
      nativeC60CNRetraction S F base
        (nativeC60BWFreeHolonomy S F (nativeC60CAChainStep S F q)) = 1 := by
    simpa only [hunprefix] using hdecode
  have hpair_full :
      nativeC60BWFreeHolonomy S F (nativeC60CAChainStep S F q) = 1 := by
    calc
      _ = nativeC60CNEmbed S F base
            (nativeC60CNRetraction S F base
              (nativeC60BWFreeHolonomy S F
                (nativeC60CAChainStep S F q))) :=
          (nativeC60CWPairChain_complete_CN S F base pairs).symm
      _ = 1 := by rw [hpair_decode, map_one]
  apply hfull
  rw [hfactor, hpair_full, map_one]

end OuterContextObstruction

#print axioms nativeC60CWPairChain
#print axioms nativeC60CWPairChain_codes
#print axioms nativeC60CWParallel_letter_reconstruct
#print axioms nativeC60CWParallel_pair_reconstruct
#print axioms nativeC60CWPairChain_holonomy_cons
#print axioms nativeC60CWPairChain_complete_CN
#print axioms nativeC60CWOriginal_loop_complete_CN_of_pairs

end
end Kuu.F112.Physical
