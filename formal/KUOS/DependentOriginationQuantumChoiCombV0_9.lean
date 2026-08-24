import Mathlib
import KUOS.DependentOriginationProcessTensorMemoryBridgeV0_8

namespace KUOS.DependentOriginationQuantumChoiCombV0_9

open scoped BigOperators

universe u v

/-!
# Quantum Choi / comb representation v0.9

This layer upgrades the v0.8 operational real-linear process-tensor interface to
an explicit finite-dimensional complex matrix-algebra Choi representation.

The mathematical commitments are kept exact and separated:

* every complex-linear map between finite matrix algebras has an explicit Choi
  matrix and an explicit inverse reconstruction;
* trace preservation is equivalent to the Choi output partial-trace
  normalization;
* composition is represented by an explicit Choi link product;
* a finite intervention word is reconstructed exactly from its Choi word;
* a deterministic finite quantum comb is represented by a positive
  semidefinite Choi matrix at each level together with the recursive causal
  partial-trace normalization;
* promotion from the v0.8 real-linear process tensor to this quantum layer
  requires an explicit lift witness.  No real-linear process is silently
  declared quantum.

No Yang--Mills physical theorem is asserted here.
-/

/-- Finite-dimensional complex matrix algebra used by the Choi layer. -/
abbrev QMat (d : ℕ) := Matrix (Fin d) (Fin d) ℂ

/-- Row/column index of the Choi matrix of a map `M_n → M_m`. -/
abbrev ChoiIndex (n m : ℕ) := Fin n × Fin m

/-- Choi matrix carrier. -/
abbrev ChoiMat (n m : ℕ) :=
  Matrix (ChoiIndex n m) (ChoiIndex n m) ℂ

section ExactChoi

variable {n m k : ℕ}

/--
The Choi matrix of a complex-linear map `Φ : M_n → M_m`, in the convention

`J_Φ[(i,a),(j,b)] = Φ(E_ij)[a,b]`.
-/
def choiMatrix (Φ : QMat n →ₗ[ℂ] QMat m) : ChoiMat n m :=
  fun p q => Φ (Matrix.single p.1 q.1 1) p.2 q.2

/--
Inverse Choi reconstruction:

`Φ_J(X)[a,b] = ∑_{i,j} X[i,j] J[(i,a),(j,b)]`.
-/
def fromChoi (J : ChoiMat n m) : QMat n →ₗ[ℂ] QMat m where
  toFun := fun X a b =>
    ∑ i : Fin n, ∑ j : Fin n, X i j * J (i, a) (j, b)
  map_add' := by
    intro X Y
    ext a b
    simp [Finset.sum_add_distrib, add_mul]
  map_smul' := by
    intro c X
    ext a b
    simp [Finset.mul_sum, mul_assoc]

@[simp] theorem fromChoi_single_one
    (J : ChoiMat n m)
    (i j : Fin n) (a b : Fin m) :
    fromChoi J (Matrix.single i j 1) a b = J (i, a) (j, b) := by
  simp [fromChoi]

/-- Encoding after decoding recovers every Choi matrix entrywise. -/
@[simp] theorem choiMatrix_fromChoi
    (J : ChoiMat n m) :
    choiMatrix (fromChoi J) = J := by
  ext p q
  simp [choiMatrix]

/-- Reconstruction is exact on every scalar matrix unit. -/
@[simp] theorem fromChoi_choiMatrix_single
    (Φ : QMat n →ₗ[ℂ] QMat m)
    (i j : Fin n) (c : ℂ) :
    fromChoi (choiMatrix Φ) (Matrix.single i j c) =
      Φ (Matrix.single i j c) := by
  have hsingle :
      c • Matrix.single i j (1 : ℂ) = Matrix.single i j c := by
    simpa using Matrix.smul_single c i j (1 : ℂ)
  have hbase :
      fromChoi (choiMatrix Φ) (Matrix.single i j (1 : ℂ)) =
        Φ (Matrix.single i j (1 : ℂ)) := by
    ext a b
    simp [choiMatrix]
  calc
    fromChoi (choiMatrix Φ) (Matrix.single i j c) =
        fromChoi (choiMatrix Φ) (c • Matrix.single i j (1 : ℂ)) := by
          rw [hsingle]
    _ = c • fromChoi (choiMatrix Φ) (Matrix.single i j (1 : ℂ)) := by
          rw [map_smul]
    _ = c • Φ (Matrix.single i j (1 : ℂ)) := by
          rw [hbase]
    _ = Φ (c • Matrix.single i j (1 : ℂ)) :=
          (Φ.map_smul c (Matrix.single i j (1 : ℂ))).symm
    _ = Φ (Matrix.single i j c) := by
          rw [hsingle]

/--
Decoding after encoding recovers the original complex-linear map.  Together
with `choiMatrix_fromChoi`, this is the exact finite-dimensional Choi
bijection at the level of linear maps and matrices.
-/
@[simp] theorem fromChoi_choiMatrix
    (Φ : QMat n →ₗ[ℂ] QMat m) :
    fromChoi (choiMatrix Φ) = Φ := by
  apply Matrix.ext_linearMap ℂ
  intro i j
  apply LinearMap.ext
  intro c
  change
    fromChoi (choiMatrix Φ) (Matrix.single i j c) =
      Φ (Matrix.single i j c)
  exact fromChoi_choiMatrix_single Φ i j c

/-- Pointwise reconstruction formula for an arbitrary linear map. -/
theorem apply_eq_sum_choi
    (Φ : QMat n →ₗ[ℂ] QMat m)
    (X : QMat n) (a b : Fin m) :
    Φ X a b =
      ∑ i : Fin n, ∑ j : Fin n,
        X i j * choiMatrix Φ (i, a) (j, b) := by
  have h := LinearMap.congr_fun (fromChoi_choiMatrix Φ) X
  have hentry := congrArg (fun M : QMat m => M a b) h
  simpa [fromChoi] using hentry.symm

end ExactChoi

section TraceNormalization

variable {n m : ℕ}

/-- Matrix trace as a complex-linear functional. -/
def matrixTraceLinear (d : ℕ) : QMat d →ₗ[ℂ] ℂ where
  toFun := fun X => ∑ i : Fin d, X i i
  map_add' := by
    intro X Y
    simp [Finset.sum_add_distrib]
  map_smul' := by
    intro c X
    simp [Finset.mul_sum]

/-- Trace preservation expressed as equality of linear functionals. -/
def TracePreserving (Φ : QMat n →ₗ[ℂ] QMat m) : Prop :=
  (matrixTraceLinear m).comp Φ = matrixTraceLinear n

/-- Partial trace of a Choi matrix over its output leg. -/
def partialTraceOutput (J : ChoiMat n m) : QMat n :=
  fun i j => ∑ a : Fin m, J (i, a) (j, a)

/--
Trace preservation implies the standard Choi normalization
`Tr_output J_Φ = I_input`.
-/
theorem partialTraceOutput_eq_one_of_tracePreserving
    (Φ : QMat n →ₗ[ℂ] QMat m)
    (hTP : TracePreserving Φ) :
    partialTraceOutput (choiMatrix Φ) = 1 := by
  ext i j
  have hbasis := LinearMap.congr_fun hTP (Matrix.single i j (1 : ℂ))
  simpa [TracePreserving, partialTraceOutput, choiMatrix,
    matrixTraceLinear] using hbasis

/--
Conversely, Choi output-partial-trace normalization forces trace preservation.
Thus trace preservation and Choi normalization are exactly equivalent.
-/
theorem tracePreserving_of_partialTraceOutput_eq_one
    (Φ : QMat n →ₗ[ℂ] QMat m)
    (hNorm : partialTraceOutput (choiMatrix Φ) = 1) :
    TracePreserving Φ := by
  unfold TracePreserving
  apply Matrix.ext_linearMap ℂ
  intro i j
  apply LinearMap.ext
  intro c
  change
    matrixTraceLinear m (Φ (Matrix.single i j c)) =
      matrixTraceLinear n (Matrix.single i j c)
  have hbase :
      matrixTraceLinear m (Φ (Matrix.single i j (1 : ℂ))) =
        matrixTraceLinear n (Matrix.single i j (1 : ℂ)) := by
    have hij := congrArg (fun M : QMat n => M i j) hNorm
    simpa [partialTraceOutput, choiMatrix, matrixTraceLinear] using hij
  have hsingle :
      c • Matrix.single i j (1 : ℂ) = Matrix.single i j c := by
    simpa using Matrix.smul_single c i j (1 : ℂ)
  calc
    matrixTraceLinear m (Φ (Matrix.single i j c)) =
        matrixTraceLinear m (Φ (c • Matrix.single i j (1 : ℂ))) := by
          rw [hsingle]
    _ = c • matrixTraceLinear m (Φ (Matrix.single i j (1 : ℂ))) := by
          rw [Φ.map_smul, (matrixTraceLinear m).map_smul]
    _ = c • matrixTraceLinear n (Matrix.single i j (1 : ℂ)) := by
          rw [hbase]
    _ = matrixTraceLinear n (c • Matrix.single i j (1 : ℂ)) :=
          ((matrixTraceLinear n).map_smul c
            (Matrix.single i j (1 : ℂ))).symm
    _ = matrixTraceLinear n (Matrix.single i j c) := by
          rw [hsingle]

/-- Exact equivalence between trace preservation and Choi normalization. -/
theorem tracePreserving_iff_partialTraceOutput
    (Φ : QMat n →ₗ[ℂ] QMat m) :
    TracePreserving Φ ↔ partialTraceOutput (choiMatrix Φ) = 1 := by
  constructor
  · exact partialTraceOutput_eq_one_of_tracePreserving Φ
  · exact tracePreserving_of_partialTraceOutput_eq_one Φ

end TraceNormalization

section ChoiChannelCertificates

variable {n m : ℕ}

/--
Operator-side channel certificate in Choi language: the represented map has a
positive-semidefinite Choi matrix and is trace preserving.

This file deliberately states the matrix-side positivity obligation explicitly;
it does not silently identify it with an unrelated external CP-map class.
-/
structure ChoiChannelCertificate (n m : ℕ) where
  map : QMat n →ₗ[ℂ] QMat m
  choiPositive : (choiMatrix map).PosSemidef
  tracePreserving : TracePreserving map

/-- Pure matrix-side form of the same channel certificate. -/
structure ChoiMatrixChannelCertificate (n m : ℕ) where
  choi : ChoiMat n m
  positive : choi.PosSemidef
  normalized : partialTraceOutput choi = 1

namespace ChoiChannelCertificate

/-- Encode an operator-side channel certificate as its Choi matrix certificate. -/
def toMatrixCertificate
    (C : ChoiChannelCertificate n m) :
    ChoiMatrixChannelCertificate n m where
  choi := choiMatrix C.map
  positive := C.choiPositive
  normalized :=
    partialTraceOutput_eq_one_of_tracePreserving C.map C.tracePreserving

/-- The matrix certificate retains the exact operator Choi matrix. -/
@[simp] theorem toMatrixCertificate_choi
    (C : ChoiChannelCertificate n m) :
    C.toMatrixCertificate.choi = choiMatrix C.map :=
  rfl

end ChoiChannelCertificate

namespace ChoiMatrixChannelCertificate

/-- Decode a normalized positive Choi certificate back into an operator-side certificate. -/
def toOperatorCertificate
    (C : ChoiMatrixChannelCertificate n m) :
    ChoiChannelCertificate n m where
  map := fromChoi C.choi
  choiPositive := by
    rw [choiMatrix_fromChoi]
    exact C.positive
  tracePreserving := by
    apply tracePreserving_of_partialTraceOutput_eq_one
    rw [choiMatrix_fromChoi]
    exact C.normalized

/-- Decoding a Choi certificate reproduces its Choi matrix exactly. -/
@[simp] theorem toOperatorCertificate_choi
    (C : ChoiMatrixChannelCertificate n m) :
    choiMatrix C.toOperatorCertificate.map = C.choi := by
  simp [toOperatorCertificate]

end ChoiMatrixChannelCertificate

/-- Operator → Choi → operator is exact. -/
@[simp] theorem channel_operator_roundtrip
    (C : ChoiChannelCertificate n m) :
    C.toMatrixCertificate.toOperatorCertificate.map = C.map := by
  simp [ChoiChannelCertificate.toMatrixCertificate,
    ChoiMatrixChannelCertificate.toOperatorCertificate]

/-- Choi → operator → Choi is exact. -/
@[simp] theorem channel_choi_roundtrip
    (C : ChoiMatrixChannelCertificate n m) :
    C.toOperatorCertificate.toMatrixCertificate.choi = C.choi := by
  simp [ChoiChannelCertificate.toMatrixCertificate,
    ChoiMatrixChannelCertificate.toOperatorCertificate]

end ChoiChannelCertificates

section LinkProduct

variable {n m k : ℕ}

/--
Choi link product for causal composition `M_n → M_m → M_k` in the current
index convention.
-/
def choiLink
    (J₁ : ChoiMat n m) (J₂ : ChoiMat m k) : ChoiMat n k :=
  fun p q =>
    ∑ a : Fin m, ∑ b : Fin m,
      J₁ (p.1, a) (q.1, b) * J₂ (a, p.2) (b, q.2)

/-- Choi representation converts operator composition into link product exactly. -/
theorem choiMatrix_comp
    (Ψ : QMat m →ₗ[ℂ] QMat k)
    (Φ : QMat n →ₗ[ℂ] QMat m) :
    choiMatrix (Ψ.comp Φ) =
      choiLink (choiMatrix Φ) (choiMatrix Ψ) := by
  ext p q
  change
    Ψ (Φ (Matrix.single p.1 q.1 1)) p.2 q.2 =
      ∑ a : Fin m, ∑ b : Fin m,
        Φ (Matrix.single p.1 q.1 1) a b *
          Ψ (Matrix.single a b 1) p.2 q.2
  exact apply_eq_sum_choi Ψ
    (Φ (Matrix.single p.1 q.1 1)) p.2 q.2

/-- Complex-linear operator represented by a finite ordered intervention word. -/
def complexInterventionWordOperator (d : ℕ) :
    List (QMat d →ₗ[ℂ] QMat d) → QMat d →ₗ[ℂ] QMat d
  | [] => LinearMap.id
  | intervention :: tail =>
      intervention.comp (complexInterventionWordOperator d tail)

/-- Choi matrix of the identity intervention. -/
def identityChoi (d : ℕ) : ChoiMat d d :=
  choiMatrix (LinearMap.id : QMat d →ₗ[ℂ] QMat d)

/-- Link-product evaluation of a finite word of Choi matrices. -/
def choiWord (d : ℕ) : List (ChoiMat d d) → ChoiMat d d
  | [] => identityChoi d
  | J :: tail => choiLink (choiWord d tail) J

/--
A finite complex intervention word and the recursively linked Choi word encode
exactly the same operator.
-/
theorem choiMatrix_complexInterventionWordOperator
    (d : ℕ)
    (word : List (QMat d →ₗ[ℂ] QMat d)) :
    choiMatrix (complexInterventionWordOperator d word) =
      choiWord d (word.map choiMatrix) := by
  induction word with
  | nil =>
      rfl
  | cons A tail ih =>
      simp [complexInterventionWordOperator, choiWord,
        choiMatrix_comp, ih]

end LinkProduct

section ComplexOperationalProcessTensor

/--
Complex finite-dimensional operational process tensor.  It is the direct
quantum-compatible refinement of the v0.8 real-linear carrier before imposing
a Choi-comb positivity/normalization certificate.
-/
structure OperationalComplexProcessTensor (d : ℕ) where
  initial : QMat d
  readout : QMat d →ₗ[ℂ] ℂ

namespace OperationalComplexProcessTensor

variable {d : ℕ}

/-- Response to a finite ordered word of complex-linear interventions. -/
def response
    (P : OperationalComplexProcessTensor d)
    (word : List (QMat d →ₗ[ℂ] QMat d)) : ℂ :=
  P.readout (complexInterventionWordOperator d word P.initial)

/-- The same response reconstructed purely from the linked Choi word. -/
def choiResponse
    (P : OperationalComplexProcessTensor d)
    (word : List (QMat d →ₗ[ℂ] QMat d)) : ℂ :=
  P.readout
    (fromChoi (choiWord d (word.map choiMatrix)) P.initial)

/--
Complete Choi response theorem: replacing the whole intervention word by its
linked Choi representation changes no operational response.
-/
theorem response_eq_choiResponse
    (P : OperationalComplexProcessTensor d)
    (word : List (QMat d →ₗ[ℂ] QMat d)) :
    P.response word = P.choiResponse word := by
  unfold response choiResponse
  rw [← choiMatrix_complexInterventionWordOperator]
  rw [fromChoi_choiMatrix]

end OperationalComplexProcessTensor

end ComplexOperationalProcessTensor

section QuantumComb

/--
Recursive basis index for a uniform `n`-slot process tensor.  Each slot adds an
input/output pair.  The nested-product presentation makes the causal partial
trace explicit without hiding tensor-leg permutations.
-/
def CombIndex (d : ℕ) : ℕ → Type
  | 0 => Unit
  | Nat.succ n => CombIndex d n × (Fin d × Fin d)

/--
Partial trace over the output leg of the newest slot.  The remaining index is
`previous-history × newest-input`.
-/
def partialTraceLastOutput
    {d n : ℕ}
    (W : Matrix (CombIndex d (Nat.succ n))
      (CombIndex d (Nat.succ n)) ℂ) :
    Matrix (CombIndex d n × Fin d) (CombIndex d n × Fin d) ℂ :=
  fun r c =>
    ∑ o : Fin d,
      W (r.1, (r.2, o)) (c.1, (c.2, o))

/-- `I_input ⊗ previousComb` in explicit index form. -/
def liftInputIdentity
    {d n : ℕ}
    (W : Matrix (CombIndex d n) (CombIndex d n) ℂ) :
    Matrix (CombIndex d n × Fin d) (CombIndex d n × Fin d) ℂ :=
  fun r c => if r.2 = c.2 then W r.1 c.1 else 0

/--
Recursive deterministic quantum-comb condition in Choi form.

At level zero the scalar comb is normalized to `1`.  Every positive-length
level is positive semidefinite and has output partial trace equal to
`I_input ⊗ previous`, where `previous` itself satisfies the same recursive
condition.
-/
def CombNormalized (d : ℕ) :
    (n : ℕ) →
      Matrix (CombIndex d n) (CombIndex d n) ℂ → Prop
  | 0, W => W = 1
  | Nat.succ n, W =>
      W.PosSemidef ∧
        ∃ previous : Matrix (CombIndex d n) (CombIndex d n) ℂ,
          CombNormalized d n previous ∧
            partialTraceLastOutput W = liftInputIdentity previous

/-- Deterministic quantum process tensor / quantum comb in complete Choi form. -/
structure QuantumCombChoi (d n : ℕ) where
  choi : Matrix (CombIndex d n) (CombIndex d n) ℂ
  normalized : CombNormalized d n choi

namespace QuantumCombChoi

/-- Zero-slot comb normalization is exactly the scalar identity. -/
theorem zero_normalization
    (Q : QuantumCombChoi d 0) :
    Q.choi = 1 := by
  simpa [CombNormalized] using Q.normalized

/-- Every positive-length deterministic comb has a positive-semidefinite Choi matrix. -/
theorem positive_succ
    (Q : QuantumCombChoi d (Nat.succ n)) :
    Q.choi.PosSemidef := by
  simpa [CombNormalized] using Q.normalized.1

/--
Every positive-length comb exposes an explicitly normalized previous comb Choi
matrix.  This is the causal no-future-to-past recursion.
-/
theorem exists_previous
    (Q : QuantumCombChoi d (Nat.succ n)) :
    ∃ previous : Matrix (CombIndex d n) (CombIndex d n) ℂ,
      CombNormalized d n previous ∧
        partialTraceLastOutput Q.choi = liftInputIdentity previous := by
  simpa [CombNormalized] using Q.normalized.2

end QuantumCombChoi

end QuantumComb

section ExplicitQuantumLift

open KUOS.DependentOriginationProcessTensorMemoryBridgeV0_8

variable {State : Type u} {Output : Type v}
variable [AddCommGroup State] [Module ℝ State]
variable [AddCommGroup Output] [Module ℝ Output]

/--
Explicit witness required to promote a v0.8 real-linear operational process
tensor into the finite-dimensional complex Choi layer.

The lift specifies how each real intervention is represented as a complex
matrix-algebra intervention and how the complex scalar readout is decoded back
to the original output carrier.  The response bridge is an equality obligation,
not an automatic coercion.
-/
structure QuantumChoiLift
    (P : OperationalLinearProcessTensor State Output)
    (d : ℕ) where
  liftIntervention :
    (State →ₗ[ℝ] State) → (QMat d →ₗ[ℂ] QMat d)
  complexProcess : OperationalComplexProcessTensor d
  decode : ℂ →ₗ[ℝ] Output
  response_bridge : ∀ word : List (State →ₗ[ℝ] State),
    P.response word =
      decode (complexProcess.response (word.map liftIntervention))

namespace QuantumChoiLift

variable {P : OperationalLinearProcessTensor State Output}

/--
Once a quantum lift witness exists, every original v0.8 response is represented
exactly by the linked Choi word of the lifted interventions.
-/
theorem response_eq_complete_choi
    (L : QuantumChoiLift P d)
    (word : List (State →ₗ[ℝ] State)) :
    P.response word =
      L.decode
        (L.complexProcess.choiResponse
          (word.map L.liftIntervention)) := by
  rw [L.response_bridge]
  rw [OperationalComplexProcessTensor.response_eq_choiResponse]

end QuantumChoiLift

end ExplicitQuantumLift

end KUOS.DependentOriginationQuantumChoiCombV0_9
