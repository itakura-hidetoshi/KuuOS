import Mathlib
import KUOS.DependentOriginationQuantumChoiCombV0_9

namespace KUOS.DependentOriginationChoiCompletelyPositiveEquivalenceV0_10

open scoped BigOperators MatrixOrder CStarAlgebra
open KUOS.DependentOriginationQuantumChoiCombV0_9

noncomputable section

/-!
# Choi positivity iff Mathlib complete positivity v0.10

This file closes the finite-dimensional positivity gap left explicit in v0.9.
For complex matrix algebras, it proves that positivity of the Choi matrix is
exactly equivalent to representability by Mathlib's `CompletelyPositiveMap`.

The proof is constructive in both directions.

* CP -> Choi positivity: apply the amplified positive-map axiom to the
  maximally-entangled block probe whose image is exactly the Choi matrix.
* Choi positivity -> CP: factor the Choi matrix as `Bᴴ * B`, read the rows of
  `B` as Kraus operators, and prove every matrix amplification is a finite sum
  of positive congruences.

No external Choi theorem is assumed.
-/

/-- The `k × k` block amplification over the `d × d` complex matrix algebra. -/
abbrev AmplifiedQMat (k d : ℕ) :=
  CStarMatrix (Fin k) (Fin k) (QMat d)

/-- Flatten a block matrix to the scalar matrix on the product index. -/
def blockFlatten {k d : ℕ} (M : AmplifiedQMat k d) :
    Matrix (Fin k × Fin d) (Fin k × Fin d) ℂ :=
  fun p q => M p.1 q.1 p.2 q.2

/-- Inverse operation to `blockFlatten`. -/
def blockUnflatten {k d : ℕ}
    (A : Matrix (Fin k × Fin d) (Fin k × Fin d) ℂ) :
    AmplifiedQMat k d :=
  fun i j a b => A (i, a) (j, b)

@[simp] theorem blockFlatten_blockUnflatten {k d : ℕ}
    (A : Matrix (Fin k × Fin d) (Fin k × Fin d) ℂ) :
    blockFlatten (blockUnflatten A) = A := by
  rfl

@[simp] theorem blockUnflatten_blockFlatten {k d : ℕ}
    (M : AmplifiedQMat k d) :
    blockUnflatten (blockFlatten M) = M := by
  rfl

/-- Flattening is injective. -/
theorem blockFlatten_injective {k d : ℕ} :
    Function.Injective (@blockFlatten k d) := by
  intro A B h
  have h' := congrArg (@blockUnflatten k d) h
  simpa using h'

/-- Flattening respects the involution. -/
@[simp] theorem blockFlatten_star {k d : ℕ}
    (M : AmplifiedQMat k d) :
    blockFlatten (star M) = star (blockFlatten M) := by
  ext p q
  simp [blockFlatten, CStarMatrix.star_apply, Matrix.star_eq_conjTranspose]

/-- Flattening respects block-matrix multiplication. -/
@[simp] theorem blockFlatten_mul {k d : ℕ}
    (A B : AmplifiedQMat k d) :
    blockFlatten (A * B) = blockFlatten A * blockFlatten B := by
  ext p q
  rcases p with ⟨p, a⟩
  rcases q with ⟨q, b⟩
  simp [blockFlatten, CStarMatrix.mul_apply, Matrix.mul_apply,
    Fintype.sum_prod_type]

/--
A positive block matrix flattens to a positive-semidefinite scalar matrix.
This is proved from the C-star factorization `M = X* X`, not postulated as an
order-identification theorem.
-/
theorem blockFlatten_posSemidef_of_nonneg {k d : ℕ}
    (M : AmplifiedQMat k d) (hM : 0 ≤ M) :
    (blockFlatten M).PosSemidef := by
  obtain ⟨X, hX⟩ := CStarAlgebra.nonneg_iff_eq_star_mul_self.mp hM
  rw [hX, blockFlatten_mul, blockFlatten_star]
  simpa [Matrix.star_eq_conjTranspose] using
    (Matrix.posSemidef_conjTranspose_mul_self (blockFlatten X))

/--
Conversely, scalar positive-semidefiniteness of the flattening implies
C-star nonnegativity of the block matrix.
-/
theorem block_nonneg_of_flatten_posSemidef {k d : ℕ}
    (M : AmplifiedQMat k d)
    (hM : (blockFlatten M).PosSemidef) :
    0 ≤ M := by
  have hFlatNonneg : 0 ≤ blockFlatten M := hM.nonneg
  obtain ⟨B, hB⟩ :=
    CStarAlgebra.nonneg_iff_eq_star_mul_self.mp hFlatNonneg
  apply CStarAlgebra.nonneg_iff_eq_star_mul_self.mpr
  refine ⟨blockUnflatten B, ?_⟩
  apply blockFlatten_injective
  rw [blockFlatten_mul, blockFlatten_star, blockFlatten_blockUnflatten]
  simpa using hB

/-!
## The Choi probe and the CP -> Choi-positive direction
-/

/-- Diagonal maximally-entangled coordinate vector. -/
def diagonalBellVector (n : ℕ) : ChoiIndex n n → ℂ :=
  fun p => if p.1 = p.2 then 1 else 0

/--
Block form of `|Ω><Ω|`: its `(i,j)` block is the scalar matrix unit `E_ij`.
-/
def choiProbe (n : ℕ) : AmplifiedQMat n n :=
  fun i j => Matrix.single i j (1 : ℂ)

/-- The flattened Choi probe is the rank-one Bell Gram matrix. -/
theorem blockFlatten_choiProbe (n : ℕ) :
    blockFlatten (choiProbe n) =
      Matrix.vecMulVec (star (diagonalBellVector n)) (diagonalBellVector n) := by
  classical
  ext p q
  rcases p with ⟨i, a⟩
  rcases q with ⟨j, b⟩
  by_cases hia : i = a <;> by_cases hjb : j = b <;>
    simp [blockFlatten, choiProbe, diagonalBellVector, Matrix.vecMulVec, hia, hjb]

/-- The maximally-entangled Choi probe is positive in every dimension, including zero. -/
theorem choiProbe_nonneg (n : ℕ) :
    0 ≤ choiProbe n := by
  apply block_nonneg_of_flatten_posSemidef
  rw [blockFlatten_choiProbe]
  exact Matrix.posSemidef_vecMulVec_star_self (diagonalBellVector n)

/-- Mapping the Choi probe blockwise produces exactly the Choi matrix. -/
@[simp] theorem blockFlatten_map_choiProbe {n m : ℕ}
    (Φ : QMat n →ₗ[ℂ] QMat m) :
    blockFlatten ((choiProbe n).map Φ) = choiMatrix Φ := by
  ext p q
  rfl

/-- Mathlib complete positivity implies positive-semidefiniteness of the Choi matrix. -/
theorem choi_posSemidef_of_completelyPositive {n m : ℕ}
    (Φ : QMat n →CP QMat m) :
    (choiMatrix (Φ : QMat n →ₗ[ℂ] QMat m)).PosSemidef := by
  have hMapped :
      0 ≤ (choiProbe n).map (Φ : QMat n →ₗ[ℂ] QMat m) :=
    Φ.map_cstarMatrix_nonneg' n (choiProbe n) (choiProbe_nonneg n)
  have hFlat :=
    blockFlatten_posSemidef_of_nonneg
      ((choiProbe n).map (Φ : QMat n →ₗ[ℂ] QMat m)) hMapped
  simpa using hFlat

/-!
## Choi factorization and the Choi-positive -> CP direction
-/

/-- Kraus operator read from one row of a Choi square-root factor. -/
def krausOfChoiFactor {n m : ℕ}
    (B : ChoiMat n m) (r : ChoiIndex n m) :
    Matrix (Fin m) (Fin n) ℂ :=
  fun a i => star (B r (i, a))

/-- Block-diagonal amplification `I_k ⊗ K` without choosing an arithmetic reindexing. -/
def amplifiedKraus {n m : ℕ}
    (k : ℕ) (K : Matrix (Fin m) (Fin n) ℂ) :
    Matrix (Fin k × Fin m) (Fin k × Fin n) ℂ :=
  fun p q => if p.1 = q.1 then K p.2 q.2 else 0

/-- Entrywise congruence formula for an amplified Kraus operator. -/
theorem amplifiedKraus_congruence_apply {k n m : ℕ}
    (K : Matrix (Fin m) (Fin n) ℂ)
    (X : Matrix (Fin k × Fin n) (Fin k × Fin n) ℂ)
    (p q : Fin k) (a b : Fin m) :
    (amplifiedKraus k K * X * (amplifiedKraus k K)ᴴ)
        (p, a) (q, b) =
      ∑ i : Fin n, ∑ j : Fin n,
        K a i * X (p, i) (q, j) * star (K b j) := by
  classical
  simp [amplifiedKraus, Matrix.mul_apply, Fintype.sum_prod_type,
    Finset.mul_sum, Finset.sum_mul, mul_assoc]

/-- Cyclically move the third finite summation to the front. -/
theorem sum3_cycle
    {α β γ R : Type*}
    [Fintype α] [Fintype β] [Fintype γ]
    [AddCommMonoid R]
    (f : α → β → γ → R) :
    (∑ a, ∑ b, ∑ c, f a b c) =
      ∑ c, ∑ a, ∑ b, f a b c := by
  calc
    (∑ a, ∑ b, ∑ c, f a b c) =
        ∑ a, ∑ c, ∑ b, f a b c := by
          apply Finset.sum_congr rfl
          intro a ha
          rw [Fintype.sum_comm]
    _ = ∑ c, ∑ a, ∑ b, f a b c := by
          rw [Fintype.sum_comm]

/--
If `J_Φ = B* B`, every amplification is exactly the finite Kraus congruence
sum built from the rows of `B`.
-/
theorem blockFlatten_map_eq_kraus_sum {k n m : ℕ}
    (Φ : QMat n →ₗ[ℂ] QMat m)
    (B : ChoiMat n m)
    (hFactor : choiMatrix Φ = star B * B)
    (M : AmplifiedQMat k n) :
    blockFlatten (M.map Φ) =
      ∑ r : ChoiIndex n m,
        amplifiedKraus k (krausOfChoiFactor B r) * blockFlatten M *
          (amplifiedKraus k (krausOfChoiFactor B r))ᴴ := by
  classical
  ext p q
  rcases p with ⟨p, a⟩
  rcases q with ⟨q, b⟩
  calc
    blockFlatten (M.map Φ) (p, a) (q, b) = Φ (M p q) a b := rfl
    _ = ∑ i : Fin n, ∑ j : Fin n,
          M p q i j * choiMatrix Φ (i, a) (j, b) :=
      apply_eq_sum_choi Φ (M p q) a b
    _ = ∑ i : Fin n, ∑ j : Fin n,
          M p q i j * (star B * B) (i, a) (j, b) := by
      rw [hFactor]
    _ = ∑ i : Fin n, ∑ j : Fin n,
          M p q i j *
            (∑ r : ChoiIndex n m, star (B r (i, a)) * B r (j, b)) := by
      simp [Matrix.mul_apply, Matrix.star_eq_conjTranspose]
    _ = ∑ i : Fin n, ∑ j : Fin n, ∑ r : ChoiIndex n m,
          M p q i j * (star (B r (i, a)) * B r (j, b)) := by
      simp [Finset.mul_sum]
    _ = ∑ r : ChoiIndex n m, ∑ i : Fin n, ∑ j : Fin n,
          M p q i j * (star (B r (i, a)) * B r (j, b)) := by
      exact sum3_cycle
        (fun i j r => M p q i j * (star (B r (i, a)) * B r (j, b)))
    _ = ∑ r : ChoiIndex n m, ∑ i : Fin n, ∑ j : Fin n,
          star (B r (i, a)) * M p q i j * B r (j, b) := by
      apply Finset.sum_congr rfl
      intro r hr
      apply Finset.sum_congr rfl
      intro i hi
      apply Finset.sum_congr rfl
      intro j hj
      ring
    _ = (∑ r : ChoiIndex n m,
          amplifiedKraus k (krausOfChoiFactor B r) * blockFlatten M *
            (amplifiedKraus k (krausOfChoiFactor B r))ᴴ) (p, a) (q, b) := by
      simp [amplifiedKraus_congruence_apply, krausOfChoiFactor, blockFlatten]

/--
Positive Choi matrix implies positivity of every flattened matrix amplification.
-/
theorem blockFlatten_map_posSemidef_of_choi_posSemidef {k n m : ℕ}
    (Φ : QMat n →ₗ[ℂ] QMat m)
    (hChoi : (choiMatrix Φ).PosSemidef)
    (M : AmplifiedQMat k n)
    (hM : (blockFlatten M).PosSemidef) :
    (blockFlatten (M.map Φ)).PosSemidef := by
  have hChoiNonneg : 0 ≤ choiMatrix Φ := hChoi.nonneg
  obtain ⟨B, hFactor⟩ :=
    CStarAlgebra.nonneg_iff_eq_star_mul_self.mp hChoiNonneg
  rw [blockFlatten_map_eq_kraus_sum Φ B hFactor M]
  apply Matrix.posSemidef_sum Finset.univ
  intro r hr
  exact hM.mul_mul_conjTranspose_same
    (amplifiedKraus k (krausOfChoiFactor B r))

/--
Construct the actual Mathlib completely-positive map from a positive Choi
matrix.  This proves all matrix-amplification positivity obligations.
-/
def completelyPositiveMapOfChoiPosSemidef {n m : ℕ}
    (Φ : QMat n →ₗ[ℂ] QMat m)
    (hChoi : (choiMatrix Φ).PosSemidef) :
    QMat n →CP QMat m where
  toLinearMap := Φ
  map_cstarMatrix_nonneg' := by
    intro k M hM
    apply block_nonneg_of_flatten_posSemidef
    exact blockFlatten_map_posSemidef_of_choi_posSemidef Φ hChoi M
      (blockFlatten_posSemidef_of_nonneg M hM)

@[simp] theorem completelyPositiveMapOfChoiPosSemidef_toLinearMap {n m : ℕ}
    (Φ : QMat n →ₗ[ℂ] QMat m)
    (hChoi : (choiMatrix Φ).PosSemidef) :
    (completelyPositiveMapOfChoiPosSemidef Φ hChoi :
      QMat n →ₗ[ℂ] QMat m) = Φ := by
  rfl

/-- Predicate saying that a linear map is the underlying map of a Mathlib CP map. -/
def MathlibCompletelyPositive {n m : ℕ}
    (Φ : QMat n →ₗ[ℂ] QMat m) : Prop :=
  ∃ Ψ : QMat n →CP QMat m,
    (Ψ : QMat n →ₗ[ℂ] QMat m) = Φ

/--
Finite-dimensional Choi theorem, stated directly against Mathlib's CP-map type:

`J_Φ` is positive semidefinite iff `Φ` is a Mathlib completely-positive map.
-/
theorem choi_posSemidef_iff_mathlibCompletelyPositive {n m : ℕ}
    (Φ : QMat n →ₗ[ℂ] QMat m) :
    (choiMatrix Φ).PosSemidef ↔ MathlibCompletelyPositive Φ := by
  constructor
  · intro hChoi
    exact ⟨completelyPositiveMapOfChoiPosSemidef Φ hChoi, rfl⟩
  · rintro ⟨Ψ, hΨ⟩
    rw [← hΨ]
    exact choi_posSemidef_of_completelyPositive Ψ

/-!
## Channel certificate equivalence
-/

/-- Channel certificate using Mathlib complete positivity plus v0.9 trace preservation. -/
structure MathlibCPChannelCertificate (n m : ℕ) where
  map : QMat n →CP QMat m
  tracePreserving : TracePreserving (map : QMat n →ₗ[ℂ] QMat m)

/-- Every v0.9 Choi channel certificate canonically yields a Mathlib CP channel certificate. -/
def ChoiChannelCertificate.toMathlibCP {n m : ℕ}
    (C : ChoiChannelCertificate n m) :
    MathlibCPChannelCertificate n m where
  map := completelyPositiveMapOfChoiPosSemidef C.map C.choiPositive
  tracePreserving := by
    simpa using C.tracePreserving

/-- Every Mathlib CP channel certificate canonically yields the v0.9 Choi certificate. -/
def MathlibCPChannelCertificate.toChoi {n m : ℕ}
    (C : MathlibCPChannelCertificate n m) :
    ChoiChannelCertificate n m where
  map := C.map
  choiPositive := choi_posSemidef_of_completelyPositive C.map
  tracePreserving := C.tracePreserving

/-- The Mathlib-CP -> Choi conversion preserves the underlying linear map. -/
@[simp] theorem MathlibCPChannelCertificate.toChoi_map {n m : ℕ}
    (C : MathlibCPChannelCertificate n m) :
    C.toChoi.map = (C.map : QMat n →ₗ[ℂ] QMat m) := by
  rfl

/-- The Choi -> Mathlib-CP conversion preserves the underlying linear map. -/
@[simp] theorem ChoiChannelCertificate.toMathlibCP_map {n m : ℕ}
    (C : ChoiChannelCertificate n m) :
    (C.toMathlibCP.map : QMat n →ₗ[ℂ] QMat m) = C.map := by
  rfl

end

end KUOS.DependentOriginationChoiCompletelyPositiveEquivalenceV0_10
