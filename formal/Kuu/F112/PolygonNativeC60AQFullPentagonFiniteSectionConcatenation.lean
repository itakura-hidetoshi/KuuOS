import Kuu.F112.PolygonNativeC60AQFullPentagonSecondBlockResidualFibers

/-!
# F112-P94D3EM — finite-support concatenation of genuine AQ sections

EI's genuine group-homomorphic sections are obtained by embedding the
zero-extended finite integer vectors into the actual abelianized
C60 AQ obstruction-kernel complement. This file establishes exact
compatibility of the underlying finite-support data under Fin.append.

No abstract splitting choice or equality of residual fibers is assumed.
The comparison remains inside the actual abelianization of the
noncommutative source kernel. Strict Kuu, independent-Kuu presentation,
DS no-go, original 14D--18D evidence, all public roots and the pinned
Lean/mathlib environment are retained. No Gray category, 19D filler,
new axiom, sorry or admit. Copyright Hidetoshi Itakura / 板倉英俊.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u

section FiniteSupportConcatenation

/-- Beyond its finite length, EE's actual finite integer
zero-extension has zero coefficients. -/
theorem nativeC60EMFiniteExtension_after (rank : ℕ)
    (v : Fin rank → ℤ) (i : ℕ) (h : rank ≤ i) :
    nativeC60EEFiniteExtension rank v i = 0 := by
  change (Finsupp.mapDomain (fun j : Fin rank => j.val)
    ((Finsupp.linearEquivFunOnFinite ℤ ℤ (Fin rank)).symm v)) i = 0
  apply Finsupp.mapDomain_notin_range
  rintro ⟨j, hj⟩
  have hlt : j.val < rank := j.isLt
  change j.val = i at hj
  omega

/-- A shifted finite integer vector is zero before its start. -/
theorem nativeC60EMShiftedExtension_before (start rank : ℕ)
    (v : Fin rank → ℤ) (i : ℕ) (h : i < start) :
    nativeC60EGTailShift start (nativeC60EEFiniteExtension rank v) i = 0 := by
  exact nativeC60EGTailShift_initial_zero start
    (nativeC60EEFiniteExtension rank v) ⟨i, h⟩

/-- Within its finite support, a shifted vector evaluates to
the original Fin-indexed coordinate. -/
theorem nativeC60EMShiftedExtension_inside (start rank : ℕ)
    (v : Fin rank → ℤ) (i : ℕ)
    (hlo : start ≤ i) (hhi : i < start + rank) :
    nativeC60EGTailShift start
      (nativeC60EEFiniteExtension rank v) i =
      v ⟨i - start, by omega⟩ := by
  have hj : i - start < rank := by omega
  calc
    nativeC60EGTailShift start (nativeC60EEFiniteExtension rank v) i =
        nativeC60EGTailShift start (nativeC60EEFiniteExtension rank v)
          (start + (i - start)) := by rw [Nat.add_sub_of_le hlo]
    _ = nativeC60EEFiniteExtension rank v (i - start) :=
      nativeC60EHTailShift_apply start
        (nativeC60EEFiniteExtension rank v) (i - start)
    _ = v ⟨i - start, hj⟩ :=
      nativeC60EEFiniteExtension_apply rank v ⟨i - start, hj⟩

/-- A shifted finite vector is zero after the end of its support. -/
theorem nativeC60EMShiftedExtension_after (start rank : ℕ)
    (v : Fin rank → ℤ) (i : ℕ) (h : start + rank ≤ i) :
    nativeC60EGTailShift start
      (nativeC60EEFiniteExtension rank v) i = 0 := by
  have hlo : start ≤ i := by omega
  calc
    nativeC60EGTailShift start (nativeC60EEFiniteExtension rank v) i =
        nativeC60EGTailShift start (nativeC60EEFiniteExtension rank v)
          (start + (i - start)) := by rw [Nat.add_sub_of_le hlo]
    _ = nativeC60EEFiniteExtension rank v (i - start) :=
      nativeC60EHTailShift_apply start
        (nativeC60EEFiniteExtension rank v) (i - start)
    _ = 0 := nativeC60EMFiniteExtension_after rank v (i - start) (by omega)

/-- KEY EM FINITE-SUPPORT IDENTITY. The shifted zero-extension of
two truly concatenated finite integer vectors is the exact sum of
their individually shifted finite-support extensions. This includes
all zero ranks and is not an assertion about infinite products. -/
theorem nativeC60EMFiniteSupport_concat (start m k : ℕ)
    (v : Fin m → ℤ) (w : Fin k → ℤ) :
    nativeC60EGTailShift start
        (nativeC60EEFiniteExtension (m + k) (Fin.append v w)) =
      nativeC60EGTailShift start (nativeC60EEFiniteExtension m v) +
        nativeC60EGTailShift (start + m)
          (nativeC60EEFiniteExtension k w) := by
  apply Finsupp.ext
  intro i
  change
    nativeC60EGTailShift start
      (nativeC60EEFiniteExtension (m + k) (Fin.append v w)) i =
    nativeC60EGTailShift start (nativeC60EEFiniteExtension m v) i +
      nativeC60EGTailShift (start + m)
        (nativeC60EEFiniteExtension k w) i
  by_cases h0 : i < start
  · have hm : i < start + m := by omega
    rw [nativeC60EMShiftedExtension_before start (m + k)
      (Fin.append v w) i h0,
      nativeC60EMShiftedExtension_before start m v i h0,
      nativeC60EMShiftedExtension_before (start + m) k w i hm]
    simp
  · have hstart : start ≤ i := by omega
    by_cases h1 : i < start + m
    · have hsum : i < start + (m + k) := by omega
      have hleft :
          (Fin.append v w) (⟨i - start, by omega⟩ : Fin (m + k)) =
            v (⟨i - start, by omega⟩ : Fin m) := by
        have heq : (⟨i - start, by omega⟩ : Fin (m + k)) =
            Fin.castAdd k (⟨i - start, by omega⟩ : Fin m) :=
          Fin.ext rfl
        rw [heq]
        exact Fin.append_left v w _
      rw [nativeC60EMShiftedExtension_inside start (m + k)
        (Fin.append v w) i hstart hsum,
        nativeC60EMShiftedExtension_inside start m v i hstart h1,
        nativeC60EMShiftedExtension_before (start + m) k w i h1]
      simpa only [add_zero] using hleft
    · have hm : start + m ≤ i := by omega
      by_cases h2 : i < start + (m + k)
      · have hright :
            (Fin.append v w) (⟨i - start, by omega⟩ : Fin (m + k)) =
              w (⟨i - (start + m), by omega⟩ : Fin k) := by
          have heq : (⟨i - start, by omega⟩ : Fin (m + k)) =
              Fin.natAdd m
                (⟨i - (start + m), by omega⟩ : Fin k) := by
            apply Fin.ext
            dsimp
            omega
          rw [heq]
          exact Fin.append_right v w _
        rw [nativeC60EMShiftedExtension_inside start (m + k)
          (Fin.append v w) i hstart h2,
          nativeC60EMShiftedExtension_after start m v i hm,
          nativeC60EMShiftedExtension_inside (start + m) k w i hm
            (by omega)]
        simpa only [zero_add] using hright
      · have hsum : start + (m + k) ≤ i := by omega
        rw [nativeC60EMShiftedExtension_after start (m + k)
          (Fin.append v w) i hsum,
          nativeC60EMShiftedExtension_after start m v i hm,
          nativeC60EMShiftedExtension_after (start + m) k w i
            (by omega)]
        simp

end FiniteSupportConcatenation

section ActualAQFiniteSections

variable {L : NativeC60AXLayer.{u}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- Genuine inclusion of the cumulative character kernel
C_(n+m) into C_n, using EJ's exact coordinate restriction. -/
def nativeC60EMKernelInclusion (word : List Bool) (n m : ℕ) :
    (nativeC60EBAbelianReceiver S F word (n + m)).ker →*
      (nativeC60EBAbelianReceiver S F word n).ker where
  toFun x := ⟨x.1, MonoidHom.mem_ker.mpr
    (nativeC60EJFirstZero_of_fullZero S F word n m x.1
      (MonoidHom.mem_ker.mp x.2))⟩
  map_one' := by
    apply Subtype.ext
    rfl
  map_mul' x y := by
    apply Subtype.ext
    rfl

/-- The additive finite coordinates of multiplicative
Fin.append are literally the Fin.append of additive coordinates. -/
theorem nativeC60EMAppend_toAdd (m k : ℕ)
    (v : Fin m → Multiplicative ℤ)
    (w : Fin k → Multiplicative ℤ) :
    (fun i : Fin (m + k) => ((Fin.append v w) i).toAdd) =
      Fin.append (fun i : Fin m => (v i).toAdd)
        (fun j : Fin k => (w j).toAdd) := by
  funext i
  refine Fin.addCases (fun j => ?_) (fun j => ?_) i
  · simp only [Fin.append_left]
  · simp only [Fin.append_right]

/-- MAIN EM SECTION LAW: the genuinely constructed EI finite-rank
section concatenates by multiplication of its first section and
the included next-tail section, inside the actual kernel C_n.
It is an equality of subgroup elements, not merely of observations. -/
theorem nativeC60EMTailFiniteSection_concat (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n m k : ℕ)
    (v : Fin m → Multiplicative ℤ)
    (w : Fin k → Multiplicative ℤ) :
    nativeC60EITailFiniteSection S F word r n (m + k)
        (Fin.append v w) =
      nativeC60EITailFiniteSection S F word r n m v *
        nativeC60EMKernelInclusion S F word n m
          (nativeC60EITailFiniteSection S F word r (n + m) k w) := by
  have hcoords := nativeC60EMAppend_toAdd m k v w
  apply Subtype.ext
  change
    (nativeC60EDFiniteSupportEmbedding S F word r
      (nativeC60EGTailShift n
        (nativeC60EEFiniteExtension (m + k)
          (fun i => ((Fin.append v w) i).toAdd)))).toMul =
    (nativeC60EDFiniteSupportEmbedding S F word r
      (nativeC60EGTailShift n
        (nativeC60EEFiniteExtension m (fun i => (v i).toAdd)))).toMul *
      (nativeC60EDFiniteSupportEmbedding S F word r
        (nativeC60EGTailShift (n + m)
          (nativeC60EEFiniteExtension k (fun j => (w j).toAdd)))).toMul
  rw [hcoords, nativeC60EMFiniteSupport_concat, map_add]
  rfl

end ActualAQFiniteSections

#print axioms nativeC60EMFiniteSupport_concat
#print axioms nativeC60EMKernelInclusion
#print axioms nativeC60EMTailFiniteSection_concat

end
end Kuu.F112.Physical
