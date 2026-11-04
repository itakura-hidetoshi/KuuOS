import KUOS.Architecture.QiWuxingGK5BRNorthPrimePowerV4_37
import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5BSCRTLocalGlobalGluing
import Mathlib.Tactic

/-!
Qi v4.38 / F112-P94D3GK5BS — TRUE NORTH C60
GENUINE CRT RING-LEVEL LOCAL/GLOBAL GLUING.

Apply independent GK5BS's actual pinned Mathlib CRT ring
equivalence, arbitrary separately specified prime-power
residues, canonical integer representatives, exact uniqueness,
and true GK5BQ integer numerator reassembly to genuine north
C60. Actual original F55 Type-valued sources provide
their ALREADY existing P92B integer depth polynomial values;
original F55/P77 source quotient provides only its ALREADY
descended integer polynomial value. Never identify source
classes or infer Type history from arithmetic congruences.

The actual primitive and distinct double-inverse plus original
F55 right unit both have ZERO observed arithmetic CRT glues,
yet their ORIGINAL phi local seam verdicts are OPPOSITE.
The two actual independently selected north P92B loops have
separate verified degree-three CRT-zero certificates on
the canonical four integer sites {0,1,2,3}.
The true fifth-around physical C60 gauge, conditional P89
BadPair reflection and original F55 history remain independent.

Strict 空; independent Kuu→Qi; genuine F54 two Nat / two
categories / Blocks and original F55 Type values maintained.
No new Type sources, P77 class equality, P94A 4-cells,
GK5AY universal seam, unconditional P89 reflection,
W=1→seam, Gray or GK5BA kit.
Public root107 append-only; protected #1558 Draft/open.
Pinned Lean v4.30.0-rc2 / mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
No new axioms, sorry/admit/native_decide.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace KUOS.Architecture.WuxingPentagonUnified
open KUOS.Architecture.WuxingCyclicPaths
open Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

private def fivefoldGK5BSNorthFirst :=
  KuuNativeF45Tree.pentagon0 northNativeF45FirstStage
    northNativeF45SecondStage northNativeF45ThirdStage
    northNativeF45FourthStage

private def fivefoldGK5BSNorthLast :=
  KuuNativeF45Tree.pentagon3 northNativeF45FirstStage
    northNativeF45SecondStage northNativeF45ThirdStage
    northNativeF45FourthStage

/-- The fully ACTUAL CRT ring equivalence of the true d!
and all of its genuine maximal prime-power factors. -/
def fivefoldGK5BSNorthCRTRingEquiv (d : Nat) :
    ZMod d.factorial ≃+* nativeGK5BSFactorialLocalFamily d :=
  nativeGK5BSFactorialCRTRingEquiv d

/-- Arbitrary separately specified actual prime-power
residues admit a constructed single INTEGER representative
that satisfies every original modulus simultaneously. -/
theorem fivefoldGK5BSNorthArbitraryCRT_integer
    (d : Nat) (residues : nativeGK5BSFactorialLocalFamily d)
    (p : (d.factorial).primeFactors) :
    (nativeGK5BSCRTGlueInt d residues :
      ZMod ((p : Nat) ^ ((d.factorial).factorization (p : Nat)))) =
        residues p :=
  nativeGK5BSCRTGlueInt_local d residues p

/-- Any integer satisfying all independently specified
CRT residue constraints differs from the genuine canonical
integer by an integral multiple of the true factorial. -/
theorem fivefoldGK5BSNorthArbitraryCRT_uniqueness
    (d : Nat) (residues : nativeGK5BSFactorialLocalFamily d)
    (z : Int) :
    (∀ p : (d.factorial).primeFactors,
      (z : ZMod ((p : Nat) ^ ((d.factorial).factorization (p : Nat)))) =
        residues p) ↔
    (d.factorial : Int) ∣
      (z - nativeGK5BSCRTGlueInt d residues) :=
  nativeGK5BSCRTInt_compatible_iff_factorialDvd d residues z

/-- A canonical CRT natural residue can be selected within
the actual exact factorial range [0,d!). -/
theorem fivefoldGK5BSNorthArbitraryCRT_canonicalBound
    (d : Nat) (residues : nativeGK5BSFactorialLocalFamily d) :
    nativeGK5BSCRTGlueNat d residues < d.factorial :=
  nativeGK5BSCRTGlueNat_lt_factorial d residues

/-- The ACTUAL CRT ring-level gluing preserves both sum
and product of arbitrary independent local residue families. -/
theorem fivefoldGK5BSNorthCRTGluing_add_mul
    (d : Nat)
    (a b : nativeGK5BSFactorialLocalFamily d) :
    (nativeGK5BSCRTGlue d (a + b) =
      nativeGK5BSCRTGlue d a + nativeGK5BSCRTGlue d b) ∧
    (nativeGK5BSCRTGlue d (a * b) =
      nativeGK5BSCRTGlue d a * nativeGK5BSCRTGlue d b) :=
  ⟨nativeGK5BSCRTGlue_add d a b, nativeGK5BSCRTGlue_mul d a b⟩

/-- The exact GK5BQ cleared numerator is recovered modulo
d! after gluing its true local prime-power residues. -/
theorem fivefoldGK5BSNorthRaw_CRT_eq_actualNumerator
    (d j : Nat) (values : Nat → Int) :
    nativeGK5BSCRTGlue d (nativeGK5BSObservedLocals d j values) =
      (nativeGK5BQClearedNumerator d j values : ZMod d.factorial) :=
  nativeGK5BSObserved_glue_eq_intCast d j values

/-- Completely finite CRT reassembly test: a single actual
Int[X] Newton source exists iff every true coefficient's
glued CRT class vanishes. Original F55 Type data is NOT
reconstructed by this arithmetic condition. -/
theorem fivefoldGK5BSNorthRaw_integerLift_iff_allCRTZero
    (d : Nat) (values : Nat → Int) :
    (∃ P : Polynomial Int,
      P.map (Int.castRingHom Rat) =
        nativeGK5BPNewtonFromRaw d
          (fun n : Nat => (values n : Rat))) ↔
    (∀ j ∈ Finset.range (d + 1),
      nativeGK5BSCRTGlue d
        (nativeGK5BSObservedLocals d j values) = 0) :=
  nativeGK5BSNewton_integral_iff_allCRTZero d values

/-- The same complete iff for the genuine GK5BL rational
Lagrange polynomial on the canonical original integer grid. -/
theorem fivefoldGK5BSNorthLagrange_integerLift_iff_allCRTZero
    (d : Nat) (values : Nat → Int) :
    (∃ P : Polynomial Int,
      P.map (Int.castRingHom Rat) =
        nativeGK5BLRationalInterpolant
          (nativeGK5BKIntegerGrid d)
          (fun z : Int => (values z.toNat : Rat))) ↔
    (∀ j ∈ Finset.range (d + 1),
      nativeGK5BSCRTGlue d
        (nativeGK5BSObservedLocals d j values) = 0) :=
  nativeGK5BSLagrange_integral_iff_allCRTZero d values

/-- A genuine integer Newton source fails exactly when
some original coefficient produces a nonzero CRT class. -/
theorem fivefoldGK5BSNorthRaw_noLift_iff_nonzeroCRT
    (d : Nat) (values : Nat → Int) :
    (¬ ∃ P : Polynomial Int,
      P.map (Int.castRingHom Rat) =
        nativeGK5BPNewtonFromRaw d
          (fun n : Nat => (values n : Rat))) ↔
    (∃ j ∈ Finset.range (d + 1),
      nativeGK5BSCRTGlue d
        (nativeGK5BSObservedLocals d j values) ≠ 0) :=
  nativeGK5BSNewton_noLift_iff_exists_nonzeroCRT d values

/-- Every actual Int[X] polynomial with its exact degree
bound has ZERO true local CRT glues for all its integer
observations. This follows from GK5BQ's original finite
integer numerator, not a fabricated representative. -/
theorem fivefoldGK5BSIntegerSource_allCRTZero
    (P : Polynomial Int) (d : Nat) (hdegree : P.natDegree ≤ d) :
    ∀ j ∈ Finset.range (d + 1),
      nativeGK5BSCRTGlue d
        (nativeGK5BSObservedLocals d j
          (fun n : Nat => P.eval (n : Int))) = 0 := by
  intro j hj
  exact (nativeGK5BSObserved_glue_zero_iff_factorialDvd d j
    (fun n : Nat => P.eval (n : Int))).2
      (fivefoldGK5BQIntegerSource_divisibility P d hdegree j hj)

/-- Genuine original north F55 Type source supplies an
EXISTING P92B depth polynomial VALUE with all CRT glues
zero. It does not follow that a fresh F55 Type source
can be reconstructed from arbitrary CRT data. -/
theorem fivefoldGK5BSNorthOriginalF55_allCRTZero
    (f : NativeGK5AINorthPentagonCells) (d : Nat)
    (hdegree :
      (nativeGK5AIOriginalToP92Structural f).gk5bgDepthPolynomial.natDegree ≤ d) :
    ∀ j ∈ Finset.range (d + 1),
      nativeGK5BSCRTGlue d
        (nativeGK5BSObservedLocals d j
          (fun n : Nat =>
            (nativeGK5AIOriginalToP92Structural f).gk5bgDepthPolynomial.eval
              (n : Int))) = 0 :=
  fivefoldGK5BSIntegerSource_allCRTZero
    (nativeGK5AIOriginalToP92Structural f).gk5bgDepthPolynomial d hdegree

/-- Genuine original F55/P77 quotient class supplies its
already DESCENDED polynomial VALUE only; CRT arithmetical
gluing is not a new quotient class equality. -/
theorem fivefoldGK5BSNorthP77_allCRTZero
    (q : NativeF55RawVerticalFourClasses
      fivefoldGK5BSNorthFirst fivefoldGK5BSNorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort)
    (d : Nat)
    (hdegree : (nativeGK5BGPolyOnP77Class
      fivefoldGK5BSNorthFirst fivefoldGK5BSNorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort q).natDegree ≤ d) :
    ∀ j ∈ Finset.range (d + 1),
      nativeGK5BSCRTGlue d
        (nativeGK5BSObservedLocals d j
          (fun n : Nat => (nativeGK5BGPolyOnP77Class
            fivefoldGK5BSNorthFirst fivefoldGK5BSNorthLast
            northNativeF45PentagonLong northNativeF45PentagonShort q).eval
              (n : Int))) = 0 :=
  fivefoldGK5BSIntegerSource_allCRTZero
    (nativeGK5BGPolyOnP77Class
      fivefoldGK5BSNorthFirst fivefoldGK5BSNorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort q)
    d hdegree

/-- True original north primitive P=1 with its original
Type witness has zero CRT glues at three integer sites. -/
theorem fivefoldGK5BSNorthPrimitive_threeSite_allCRTZero :
    ∀ j ∈ Finset.range (2 + 1),
      nativeGK5BSCRTGlue 2
        (nativeGK5BSObservedLocals 2 j
          (fun n : Nat =>
            (nativeGK5AIOriginalToP92Structural
              nativeGK5AGNorthOriginalCell).gk5bgDepthPolynomial.eval
                (n : Int))) = 0 :=
  fivefoldGK5BSNorthOriginalF55_allCRTZero
    nativeGK5AGNorthOriginalCell 2
    fivefoldGK5BKNorthPrimitiveDouble_degree_le_two.1

/-- A different genuine original north double-inverse
PLUS right F55 identity P=X² also has ZERO arithmetic
CRT glues at three integer sites; Type histories differ. -/
theorem fivefoldGK5BSNorthDoubleInverse_threeSite_allCRTZero :
    ∀ j ∈ Finset.range (2 + 1),
      nativeGK5BSCRTGlue 2
        (nativeGK5BSObservedLocals 2 j
          (fun n : Nat =>
            (nativeGK5AIOriginalToP92Structural
              fivefoldGK5BFNorthDoubleInverseRightUnit).gk5bgDepthPolynomial.eval
                (n : Int))) = 0 :=
  fivefoldGK5BSNorthOriginalF55_allCRTZero
    fivefoldGK5BFNorthDoubleInverseRightUnit 2
    fivefoldGK5BKNorthPrimitiveDouble_degree_le_two.2

/-- Genuine independent north P92B loops X³+2 and 2X²+X
have separately vanishing degree-three CRT certificates
at canonical integer observations {0,1,2,3}. -/
theorem fivefoldGK5BSNorthTripleLoops_fourSite_allCRTZero :
    (∀ j ∈ Finset.range (3 + 1),
      nativeGK5BSCRTGlue 3
        (nativeGK5BSObservedLocals 3 j
          (fun n : Nat =>
            fivefoldGK5BGNorthTripleLoopA.gk5bgDepthPolynomial.eval (n : Int))) = 0) ∧
    (∀ j ∈ Finset.range (3 + 1),
      nativeGK5BSCRTGlue 3
        (nativeGK5BSObservedLocals 3 j
          (fun n : Nat =>
            fivefoldGK5BGNorthTripleLoopB.gk5bgDepthPolynomial.eval (n : Int))) = 0) := by
  obtain ⟨ha, hb⟩ := fivefoldGK5BKNorthTripleLoops_degree_le_three
  exact ⟨fivefoldGK5BSIntegerSource_allCRTZero
           fivefoldGK5BGNorthTripleLoopA.gk5bgDepthPolynomial 3 ha,
         fivefoldGK5BSIntegerSource_allCRTZero
           fivefoldGK5BGNorthTripleLoopB.gk5bgDepthPolynomial 3 hb⟩

/-- Exact crucial STRUCTURAL OBSTRUCTION: both actual
original north F55 sources have ALL arithmetic CRT glues
zero, while the true original-phi local seam is present
for primitive and provably ABSENT for double inverse.
Arithmetic CRT descent cannot recover F55 Type seams. -/
theorem fivefoldGK5BSNorthBothCRTZeroButOppositeSeams
    (frame : NativeC60FivePhaseGauge) (i : FivefoldIndex) :
    (∀ j ∈ Finset.range (2 + 1),
      nativeGK5BSCRTGlue 2
        (nativeGK5BSObservedLocals 2 j
          (fun n : Nat =>
            (nativeGK5AIOriginalToP92Structural
              nativeGK5AGNorthOriginalCell).gk5bgDepthPolynomial.eval
                (n : Int))) = 0) ∧
    (∀ j ∈ Finset.range (2 + 1),
      nativeGK5BSCRTGlue 2
        (nativeGK5BSObservedLocals 2 j
          (fun n : Nat =>
            (nativeGK5AIOriginalToP92Structural
              fivefoldGK5BFNorthDoubleInverseRightUnit).gk5bgDepthPolynomial.eval
                (n : Int))) = 0) ∧
    Nonempty (nativeGK5AZSeamAt nativeGK5AGNorthOriginalCell) ∧
    ¬ Nonempty (nativeGK5AZSeamAt
      fivefoldGK5BFNorthDoubleInverseRightUnit) := by
  obtain ⟨hyes, hno, _, _⟩ :=
    fivefoldGK5BQNorthPhysicalAndP89Boundary frame i
  exact ⟨fivefoldGK5BSNorthPrimitive_threeSite_allCRTZero,
    fivefoldGK5BSNorthDoubleInverse_threeSite_allCRTZero, hyes, hno⟩

/-- The genuine fifth-around north physical C60 gauge and
old P89 BadPair CONDITIONAL reflection are independent
Type-valued theorems, never consequences of numeric CRT. -/
theorem fivefoldGK5BSNorthPhysicalAndP89Boundary
    (frame : NativeC60FivePhaseGauge) (i : FivefoldIndex) :
    (fivefoldGK5AGNorthPhysicalFifthDarts frame i =
      (nativeC60GaugeDart frame .north (i + 4),
       nativeC60GaugeDart frame .north i)) ∧
    ((¬ Function.Injective
      (fivefoldGK5ANP94NorthPhysicalFourClassMap frame i)) ↔
        fivefoldGK5AQNorthReflectionObstruction) :=
  fivefoldGK5BRNorthPhysicalAndP89Boundary frame i

#print axioms fivefoldGK5BSNorthArbitraryCRT_integer
#print axioms fivefoldGK5BSNorthArbitraryCRT_uniqueness
#print axioms fivefoldGK5BSNorthArbitraryCRT_canonicalBound
#print axioms fivefoldGK5BSNorthCRTGluing_add_mul
#print axioms fivefoldGK5BSNorthRaw_CRT_eq_actualNumerator
#print axioms fivefoldGK5BSNorthRaw_integerLift_iff_allCRTZero
#print axioms fivefoldGK5BSNorthLagrange_integerLift_iff_allCRTZero
#print axioms fivefoldGK5BSNorthRaw_noLift_iff_nonzeroCRT
#print axioms fivefoldGK5BSIntegerSource_allCRTZero
#print axioms fivefoldGK5BSNorthOriginalF55_allCRTZero
#print axioms fivefoldGK5BSNorthP77_allCRTZero
#print axioms fivefoldGK5BSNorthPrimitive_threeSite_allCRTZero
#print axioms fivefoldGK5BSNorthDoubleInverse_threeSite_allCRTZero
#print axioms fivefoldGK5BSNorthTripleLoops_fourSite_allCRTZero
#print axioms fivefoldGK5BSNorthBothCRTZeroButOppositeSeams
#print axioms fivefoldGK5BSNorthPhysicalAndP89Boundary

end
end KUOS.Architecture.WuxingPentagonUnified
