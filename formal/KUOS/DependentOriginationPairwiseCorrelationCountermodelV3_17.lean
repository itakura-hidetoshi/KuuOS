import KUOS.DependentOriginationGlobalFootprintGluingV3_16

namespace KUOS.DependentOriginationPairwiseCorrelationCountermodelV3_17

/-!
# Finite countermodel for the pairwise witness-correlation implication v3.17

Canonical v3.16 reduces the remaining quotient-stage gluing problem to the
quantifier change

```text
nested pairwise witnesses:
  ∀ s, ∃ Q_s,
    local(s,Q_s) ∧
    ∀ t, ∃ Q_t,
      local(t,Q_t) ∧ overlap-compatible(Q_s,Q_t)

versus

one globally correlated family:
  ∃ Qlocal,
    (∀ s, local(s,Qlocal s)) ∧
    (∀ s t, overlap-compatible(Qlocal s,Qlocal t)).
```

This file truth-tests that implication at the abstract finite-footprint level.

The countermodel has three route states `a,b,c`, three shared coordinates
`ab,ac,bc`, and Boolean coordinate values.  The footprints form a triangle:

```text
a sees ab, ac
b sees ab, bc
c sees ac, bc
```

Local correction constraints are

```text
a : ab = ac
b : ab = bc
c : ac ≠ bc.
```

Every anchor state admits one local witness which can be extended pairwise to
each other state, but no single family of three local witnesses can agree on
all shared coordinates simultaneously.

Therefore the v3.16 witness-correlation upgrade is not a theorem of quantifier
logic plus pairwise overlap equality alone.  Any positive theorem for the
actual quotient-gauge correction loci must use additional structure of the
generated localization route system.

This file does **not** assert that
`PairwiseWitnessCorrelationGap W R D` is inhabited for an actual KuuOS
`RawHigherContextualSystem`.  It proves only the logically sharp finite
countermodel needed to prevent an unjustified pure-choice upgrade.
-/

inductive CorrelationState where
  | a
  | b
  | c
  deriving DecidableEq, Repr

inductive CorrelationCoord where
  | ab
  | ac
  | bc
  deriving DecidableEq, Repr

/-- The triangular two-coordinate footprint carried by each abstract state. -/
def footprint : CorrelationState → CorrelationCoord → Prop
  | .a, .ab => True
  | .a, .ac => True
  | .b, .ab => True
  | .b, .bc => True
  | .c, .ac => True
  | .c, .bc => True
  | _, _ => False

/-- The three local parity constraints. -/
def LocalCorrected :
    CorrelationState → (CorrelationCoord → Bool) → Prop
  | .a, q => q .ab = q .ac
  | .b, q => q .ab = q .bc
  | .c, q => q .ac ≠ q .bc

/-- Two local sections agree on every coordinate in the literal overlap of
their two footprints. -/
def OverlapAgree
    (s t : CorrelationState)
    (qs qt : CorrelationCoord → Bool) : Prop :=
  ∀ k : CorrelationCoord,
    footprint s k →
    footprint t k →
      qs k = qt k

/-- Exact abstract analogue of the nested v3.13/v3.16 pairwise witness shape. -/
def NestedPairwiseCompatible : Prop :=
  ∀ s : CorrelationState,
    ∃ qs : CorrelationCoord → Bool,
      LocalCorrected s qs ∧
        ∀ t : CorrelationState,
          ∃ qt : CorrelationCoord → Bool,
            LocalCorrected t qt ∧
              OverlapAgree s t qs qt

/-- Exact abstract analogue of one globally correlated compatible local family. -/
def GloballyCompatibleFamily : Prop :=
  ∃ qlocal : CorrelationState → CorrelationCoord → Bool,
    (∀ s : CorrelationState,
      LocalCorrected s (qlocal s)) ∧
    ∀ s t : CorrelationState,
      OverlapAgree s t (qlocal s) (qlocal t)

/-- Constant-zero local section. -/
def zeroSection : CorrelationCoord → Bool :=
  fun _ => false

/-- Constant-one local section. -/
def oneSection : CorrelationCoord → Bool :=
  fun _ => true

/-- A `c`-correcting section compatible with the zero `a` section:
`ac = false`, `bc = true`. -/
def cFromA : CorrelationCoord → Bool
  | .ab => false
  | .ac => false
  | .bc => true

/-- A `c`-correcting section compatible with the zero `b` section:
`ac = true`, `bc = false`. -/
def cFromB : CorrelationCoord → Bool
  | .ab => false
  | .ac => true
  | .bc => false

@[simp]
theorem zeroSection_local_a :
    LocalCorrected .a zeroSection := by
  simp [LocalCorrected, zeroSection]

@[simp]
theorem zeroSection_local_b :
    LocalCorrected .b zeroSection := by
  simp [LocalCorrected, zeroSection]

@[simp]
theorem oneSection_local_b :
    LocalCorrected .b oneSection := by
  simp [LocalCorrected, oneSection]

@[simp]
theorem cFromA_local_c :
    LocalCorrected .c cFromA := by
  simp [LocalCorrected, cFromA]

@[simp]
theorem cFromB_local_c :
    LocalCorrected .c cFromB := by
  simp [LocalCorrected, cFromB]

/-- The finite triangle is nested-pairwise compatible.  The witness chosen for
the second state is allowed to depend on the anchor state, exactly as in the
pre-v3.16 quantifier order. -/
theorem nestedPairwiseCompatible :
    NestedPairwiseCompatible := by
  intro s
  cases s with
  | a =>
      refine ⟨zeroSection, zeroSection_local_a, ?_⟩
      intro t
      cases t with
      | a =>
          refine ⟨zeroSection, zeroSection_local_a, ?_⟩
          intro k _ _
          rfl
      | b =>
          refine ⟨zeroSection, zeroSection_local_b, ?_⟩
          intro k _ _
          rfl
      | c =>
          refine ⟨cFromA, cFromA_local_c, ?_⟩
          intro k hka hkc
          cases k <;>
            simp [footprint, zeroSection, cFromA] at hka hkc ⊢
  | b =>
      refine ⟨zeroSection, zeroSection_local_b, ?_⟩
      intro t
      cases t with
      | a =>
          refine ⟨zeroSection, zeroSection_local_a, ?_⟩
          intro k _ _
          rfl
      | b =>
          refine ⟨zeroSection, zeroSection_local_b, ?_⟩
          intro k _ _
          rfl
      | c =>
          refine ⟨cFromB, cFromB_local_c, ?_⟩
          intro k hkb hkc
          cases k <;>
            simp [footprint, zeroSection, cFromB] at hkb hkc ⊢
  | c =>
      refine ⟨cFromA, cFromA_local_c, ?_⟩
      intro t
      cases t with
      | a =>
          refine ⟨zeroSection, zeroSection_local_a, ?_⟩
          intro k hkc hka
          cases k <;>
            simp [footprint, cFromA, zeroSection] at hkc hka ⊢
      | b =>
          refine ⟨oneSection, oneSection_local_b, ?_⟩
          intro k hkc hkb
          cases k <;>
            simp [footprint, cFromA, oneSection] at hkc hkb ⊢
      | c =>
          refine ⟨cFromA, cFromA_local_c, ?_⟩
          intro k _ _
          rfl

/-- No globally correlated compatible local family exists: overlap equality
would identify the three edge coordinates, contradicting the odd `c` parity
constraint. -/
theorem not_globallyCompatibleFamily :
    ¬ GloballyCompatibleFamily := by
  rintro ⟨qlocal, hLocal, hPair⟩
  have hA :
      qlocal .a .ab = qlocal .a .ac := by
    simpa [LocalCorrected] using hLocal .a
  have hB :
      qlocal .b .ab = qlocal .b .bc := by
    simpa [LocalCorrected] using hLocal .b
  have hC :
      qlocal .c .ac ≠ qlocal .c .bc := by
    simpa [LocalCorrected] using hLocal .c
  have hAB :
      qlocal .a .ab = qlocal .b .ab := by
    exact hPair .a .b .ab
      (by simp [footprint])
      (by simp [footprint])
  have hAC :
      qlocal .a .ac = qlocal .c .ac := by
    exact hPair .a .c .ac
      (by simp [footprint])
      (by simp [footprint])
  have hBC :
      qlocal .b .bc = qlocal .c .bc := by
    exact hPair .b .c .bc
      (by simp [footprint])
      (by simp [footprint])
  apply hC
  exact
    hAC.symm.trans
      (hA.symm.trans
        (hAB.trans
          (hB.trans hBC)))

/-- Explicit finite witness that nested pairwise compatibility does not force
one globally correlated compatible family. -/
theorem finite_pairwise_witness_correlation_countermodel :
    NestedPairwiseCompatible ∧
      ¬ GloballyCompatibleFamily :=
  ⟨nestedPairwiseCompatible, not_globallyCompatibleFamily⟩

/-- Named obstruction in the abstract footprint model. -/
def AbstractPairwiseWitnessCorrelationGap : Prop :=
  NestedPairwiseCompatible ∧
    ¬ GloballyCompatibleFamily

theorem abstractPairwiseWitnessCorrelationGap :
    AbstractPairwiseWitnessCorrelationGap := by
  exact finite_pairwise_witness_correlation_countermodel

/-!
## Factorization frontier after v3.17

The v3.16 quantifier gap is now known to be logically genuine.

At the abstract finite-footprint level:

```text
nested pairwise local extendability
  -/->
one globally correlated compatible local family.
```

The obstruction already appears on a three-state triangle with Boolean values
and literal equality on shared coordinates.

Therefore the next positive theorem for the actual KuuOS quotient stage cannot
be obtained by `Classical.choose` alone.  It must exploit additional structure
of the concrete generated-localization route equations and correction loci.

The next theorem-sized tasks are now sharply separated:

1. identify an actual structural hypothesis on the quotient correction loci
   which kills the parity-style correlation obstruction; or
2. realize a comparable cycle inside an actual
   `RawHigherContextualSystem`, proving that the quotient-stage obstruction
   can genuinely survive pairwise consistency.

No claim between those two outcomes is made in v3.17.
-/

end KUOS.DependentOriginationPairwiseCorrelationCountermodelV3_17
