import Mathlib
import KUOS.DependentOriginationChoiCompletelyPositiveEquivalenceV0_10

namespace KUOS.DependentOriginationCPTPChoiWordV0_11

open scoped BigOperators MatrixOrder CStarAlgebra
open KUOS.DependentOriginationQuantumChoiCombV0_9
open KUOS.DependentOriginationChoiCompletelyPositiveEquivalenceV0_10

noncomputable section

/-!
# Native CPTP composition and finite Choi-word dynamics v0.11

The v0.10 Choi theorem identifies positive Choi matrices with Mathlib native
complete positivity.  This layer closes the operational consequences needed by
the process-tensor / quantum-comb spine:

* Mathlib completely-positive maps between finite complex matrix algebras are
  closed under causal composition;
* trace preservation is closed under the same composition;
* therefore native CPTP channel certificates compose;
* Choi link products of CPTP channels are positive and output-normalized;
* every finite ordered CPTP word has a positive normalized linked Choi matrix;
* every such finite word preserves density matrices exactly, and the evolved
  density matrix is reconstructed exactly from the linked Choi word.

No arbitrary operational readout is called a probability here.  Probability
normalization for instruments/process-comb contraction is a later layer.
-/

section NativeCPComposition

variable {n m k : ℕ}

/--
Composition of Mathlib native completely-positive maps, proved directly from
Mathlib's matrix-amplification positivity field.
-/
def cpComp
    (Ψ : QMat m →CP QMat k)
    (Φ : QMat n →CP QMat m) :
    QMat n →CP QMat k where
  toLinearMap :=
    (Ψ : QMat m →ₗ[ℂ] QMat k).comp
      (Φ : QMat n →ₗ[ℂ] QMat m)
  map_cstarMatrix_nonneg' := by
    intro r M hM
    have hΦ :
        0 ≤ M.map (Φ : QMat n →ₗ[ℂ] QMat m) :=
      Φ.map_cstarMatrix_nonneg' r M hM
    have hΨ :
        0 ≤ (M.map (Φ : QMat n →ₗ[ℂ] QMat m)).map
          (Ψ : QMat m →ₗ[ℂ] QMat k) :=
      Ψ.map_cstarMatrix_nonneg' r
        (M.map (Φ : QMat n →ₗ[ℂ] QMat m)) hΦ
    have hEq :
        M.map
            ((Ψ : QMat m →ₗ[ℂ] QMat k).comp
              (Φ : QMat n →ₗ[ℂ] QMat m)) =
          (M.map (Φ : QMat n →ₗ[ℂ] QMat m)).map
            (Ψ : QMat m →ₗ[ℂ] QMat k) := by
      ext i j
      rfl
    rw [hEq]
    exact hΨ

@[simp] theorem cpComp_toLinearMap
    (Ψ : QMat m →CP QMat k)
    (Φ : QMat n →CP QMat m) :
    (cpComp Ψ Φ : QMat n →ₗ[ℂ] QMat k) =
      (Ψ : QMat m →ₗ[ℂ] QMat k).comp
        (Φ : QMat n →ₗ[ℂ] QMat m) := by
  rfl

/-- Identity channel as a native Mathlib completely-positive map. -/
def cpIdentity (d : ℕ) : QMat d →CP QMat d where
  toLinearMap := LinearMap.id
  map_cstarMatrix_nonneg' := by
    intro r M hM
    simpa using hM

@[simp] theorem cpIdentity_toLinearMap (d : ℕ) :
    (cpIdentity d : QMat d →ₗ[ℂ] QMat d) = LinearMap.id := by
  rfl

/-- Trace preservation is stable under causal composition. -/
theorem tracePreserving_comp
    (Ψ : QMat m →ₗ[ℂ] QMat k)
    (Φ : QMat n →ₗ[ℂ] QMat m)
    (hΨ : TracePreserving Ψ)
    (hΦ : TracePreserving Φ) :
    TracePreserving (Ψ.comp Φ) := by
  unfold TracePreserving at hΨ hΦ ⊢
  apply LinearMap.ext
  intro X
  change matrixTraceLinear k (Ψ (Φ X)) = matrixTraceLinear n X
  calc
    matrixTraceLinear k (Ψ (Φ X)) =
        matrixTraceLinear m (Φ X) :=
      LinearMap.congr_fun hΨ (Φ X)
    _ = matrixTraceLinear n X :=
      LinearMap.congr_fun hΦ X

/-- The identity map is trace preserving. -/
theorem tracePreserving_identity (d : ℕ) :
    TracePreserving (LinearMap.id : QMat d →ₗ[ℂ] QMat d) := by
  unfold TracePreserving
  apply LinearMap.ext
  intro X
  rfl

end NativeCPComposition

/-!
## Native Mathlib CPTP channel category
-/

namespace MathlibCPChannelCertificate

variable {n m k d : ℕ}

/-- Causal composition of native Mathlib CPTP channel certificates. -/
def comp
    (C₂ : MathlibCPChannelCertificate m k)
    (C₁ : MathlibCPChannelCertificate n m) :
    MathlibCPChannelCertificate n k where
  map := cpComp C₂.map C₁.map
  tracePreserving :=
    tracePreserving_comp
      (C₂.map : QMat m →ₗ[ℂ] QMat k)
      (C₁.map : QMat n →ₗ[ℂ] QMat m)
      C₂.tracePreserving C₁.tracePreserving

@[simp] theorem comp_toLinearMap
    (C₂ : MathlibCPChannelCertificate m k)
    (C₁ : MathlibCPChannelCertificate n m) :
    ((C₂.comp C₁).map : QMat n →ₗ[ℂ] QMat k) =
      (C₂.map : QMat m →ₗ[ℂ] QMat k).comp
        (C₁.map : QMat n →ₗ[ℂ] QMat m) := by
  rfl

/-- Identity native CPTP channel. -/
def identity (d : ℕ) : MathlibCPChannelCertificate d d where
  map := cpIdentity d
  tracePreserving := by
    simpa using tracePreserving_identity d

@[simp] theorem identity_toLinearMap (d : ℕ) :
    ((identity d).map : QMat d →ₗ[ℂ] QMat d) = LinearMap.id := by
  rfl

/--
The Choi link of two native CPTP channels is positive semidefinite.
This is derived through native CP composition and the v0.10 Choi theorem.
-/
theorem choiLink_posSemidef
    (C₂ : MathlibCPChannelCertificate m k)
    (C₁ : MathlibCPChannelCertificate n m) :
    (choiLink
      (choiMatrix (C₁.map : QMat n →ₗ[ℂ] QMat m))
      (choiMatrix (C₂.map : QMat m →ₗ[ℂ] QMat k))).PosSemidef := by
  rw [← choiMatrix_comp
    (C₂.map : QMat m →ₗ[ℂ] QMat k)
    (C₁.map : QMat n →ₗ[ℂ] QMat m)]
  simpa [comp_toLinearMap] using
    choi_posSemidef_of_completelyPositive (C₂.comp C₁).map

/-- The same Choi link has the exact trace-preserving normalization. -/
theorem choiLink_normalized
    (C₂ : MathlibCPChannelCertificate m k)
    (C₁ : MathlibCPChannelCertificate n m) :
    partialTraceOutput
      (choiLink
        (choiMatrix (C₁.map : QMat n →ₗ[ℂ] QMat m))
        (choiMatrix (C₂.map : QMat m →ₗ[ℂ] QMat k))) = 1 := by
  rw [← choiMatrix_comp
    (C₂.map : QMat m →ₗ[ℂ] QMat k)
    (C₁.map : QMat n →ₗ[ℂ] QMat m)]
  exact partialTraceOutput_eq_one_of_tracePreserving
    ((C₂.map : QMat m →ₗ[ℂ] QMat k).comp
      (C₁.map : QMat n →ₗ[ℂ] QMat m))
    (tracePreserving_comp
      (C₂.map : QMat m →ₗ[ℂ] QMat k)
      (C₁.map : QMat n →ₗ[ℂ] QMat m)
      C₂.tracePreserving C₁.tracePreserving)

/-- The linked Choi matrix is itself a v0.9 normalized Choi channel certificate. -/
def linkChoiCertificate
    (C₂ : MathlibCPChannelCertificate m k)
    (C₁ : MathlibCPChannelCertificate n m) :
    ChoiMatrixChannelCertificate n k where
  choi :=
    choiLink
      (choiMatrix (C₁.map : QMat n →ₗ[ℂ] QMat m))
      (choiMatrix (C₂.map : QMat m →ₗ[ℂ] QMat k))
  positive := C₂.choiLink_posSemidef C₁
  normalized := C₂.choiLink_normalized C₁

end MathlibCPChannelCertificate

/-!
## Finite ordered CPTP words
-/

section CPTPWord

variable {d : ℕ}

/--
Causal evaluation of a finite ordered word of native CPTP channels.  The head
acts after the recursively evaluated tail, exactly matching the v0.9 finite-word
convention.
-/
def cptpWordOperator (d : ℕ) :
    List (MathlibCPChannelCertificate d d) →
      MathlibCPChannelCertificate d d
  | [] => MathlibCPChannelCertificate.identity d
  | C :: tail => C.comp (cptpWordOperator d tail)

/-- The CPTP word operator has exactly the v0.9 complex intervention-word map. -/
theorem cptpWordOperator_toLinearMap
    (word : List (MathlibCPChannelCertificate d d)) :
    ((cptpWordOperator d word).map : QMat d →ₗ[ℂ] QMat d) =
      complexInterventionWordOperator d
        (word.map fun C => (C.map : QMat d →ₗ[ℂ] QMat d)) := by
  induction word with
  | nil =>
      rfl
  | cons C tail ih =>
      simp [cptpWordOperator, complexInterventionWordOperator, ih,
        MathlibCPChannelCertificate.comp_toLinearMap]

/-- Linked Choi representation of a finite native CPTP word. -/
def cptpChoiWord
    (d : ℕ)
    (word : List (MathlibCPChannelCertificate d d)) : ChoiMat d d :=
  choiWord d
    (word.map fun C =>
      choiMatrix (C.map : QMat d →ₗ[ℂ] QMat d))

/-- The linked Choi word is exactly the Choi matrix of the composed CPTP map. -/
theorem cptpChoiWord_eq_choiMatrix
    (word : List (MathlibCPChannelCertificate d d)) :
    cptpChoiWord d word =
      choiMatrix ((cptpWordOperator d word).map :
        QMat d →ₗ[ℂ] QMat d) := by
  unfold cptpChoiWord
  rw [cptpWordOperator_toLinearMap]
  rw [choiMatrix_complexInterventionWordOperator]
  simp [List.map_map, Function.comp_def]

/-- Every finite linked CPTP Choi word is positive semidefinite. -/
theorem cptpChoiWord_posSemidef
    (word : List (MathlibCPChannelCertificate d d)) :
    (cptpChoiWord d word).PosSemidef := by
  rw [cptpChoiWord_eq_choiMatrix]
  exact choi_posSemidef_of_completelyPositive (cptpWordOperator d word).map

/-- Every finite linked CPTP Choi word has exact TP Choi normalization. -/
theorem cptpChoiWord_normalized
    (word : List (MathlibCPChannelCertificate d d)) :
    partialTraceOutput (cptpChoiWord d word) = 1 := by
  rw [cptpChoiWord_eq_choiMatrix]
  exact partialTraceOutput_eq_one_of_tracePreserving
    ((cptpWordOperator d word).map : QMat d →ₗ[ℂ] QMat d)
    (cptpWordOperator d word).tracePreserving

/-- A complete positive normalized Choi certificate for the entire finite word. -/
def cptpWordChoiCertificate
    (word : List (MathlibCPChannelCertificate d d)) :
    ChoiMatrixChannelCertificate d d where
  choi := cptpChoiWord d word
  positive := cptpChoiWord_posSemidef word
  normalized := cptpChoiWord_normalized word

end CPTPWord

/-!
## Density matrices and exact Choi-word evolution
-/

/-- Finite-dimensional density matrix in the same matrix order used by v0.9/v0.10. -/
structure DensityMatrix (d : ℕ) where
  matrix : QMat d
  positive : matrix.PosSemidef
  trace_one : matrixTraceLinear d matrix = 1

namespace MathlibCPChannelCertificate

variable {n m : ℕ}

/-- A native CPTP channel sends density matrices to density matrices. -/
def mapDensity
    (C : MathlibCPChannelCertificate n m)
    (ρ : DensityMatrix n) : DensityMatrix m where
  matrix := C.map ρ.matrix
  positive := by
    have hIn : 0 ≤ ρ.matrix := ρ.positive.nonneg
    have hOut : 0 ≤ C.map ρ.matrix := map_nonneg C.map hIn
    exact Matrix.nonneg_iff_posSemidef.mp hOut
  trace_one := by
    have hTP := LinearMap.congr_fun C.tracePreserving ρ.matrix
    calc
      matrixTraceLinear m (C.map ρ.matrix) =
          matrixTraceLinear n ρ.matrix := hTP
      _ = 1 := ρ.trace_one

end MathlibCPChannelCertificate

section DensityWord

variable {d : ℕ}

/-- Evolve a density matrix through a finite ordered CPTP word. -/
def evolveDensity
    (word : List (MathlibCPChannelCertificate d d))
    (ρ : DensityMatrix d) : DensityMatrix d :=
  (cptpWordOperator d word).mapDensity ρ

/-- The evolved matrix is reconstructed exactly from the complete linked Choi word. -/
theorem evolveDensity_matrix_eq_fromChoi
    (word : List (MathlibCPChannelCertificate d d))
    (ρ : DensityMatrix d) :
    (evolveDensity word ρ).matrix =
      fromChoi (cptpChoiWord d word) ρ.matrix := by
  rw [cptpChoiWord_eq_choiMatrix, fromChoi_choiMatrix]
  rfl

/-- Finite CPTP history preserves positivity. -/
theorem evolveDensity_positive
    (word : List (MathlibCPChannelCertificate d d))
    (ρ : DensityMatrix d) :
    (evolveDensity word ρ).matrix.PosSemidef :=
  (evolveDensity word ρ).positive

/-- Finite CPTP history preserves unit trace. -/
theorem evolveDensity_trace_one
    (word : List (MathlibCPChannelCertificate d d))
    (ρ : DensityMatrix d) :
    matrixTraceLinear d (evolveDensity word ρ).matrix = 1 :=
  (evolveDensity word ρ).trace_one

end DensityWord

end

end KUOS.DependentOriginationCPTPChoiWordV0_11
