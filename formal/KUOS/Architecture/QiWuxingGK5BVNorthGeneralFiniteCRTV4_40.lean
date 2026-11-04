import KUOS.Architecture.QiWuxingGK5BTNorthNoncoprimeCRTOverlapV4_39
import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5BVGeneralFiniteCRTDescent
import Mathlib.Tactic

/-!
Qi v4.40 / F112-P94D3GK5BV — COMPLETE FINITE
NON-COPRIME CRT DESCENT, TRUE NORTH C60 AND F55 SEAMS.

Independent GK5BV proves for ANY finite set of Nat moduli
(and even zero moduli, with no dominating-site hypothesis):
pairwise gcd compatibility iff existence of a global Nat
residue, unique modulo the finite LCM. An explicit
canonical normalized global representative is constructed.

Here the genuine GK5BQ original signed integer numerators
are projected to local natural residues through natAbs
solely for integer divisibility; their TRUE global gluing
agrees modulo Finset.lcm with the original absolute value.
Integer polynomial source natDegree≤d and
Finset.lcm moduli | d! ensure all observed CRT glues zero.

These numeric statements are applied to ACTUAL north F55
Type witnesses only via existing P92B depth polynomial
VALUES; original F55/P77 classes only via ALREADY descended
polynomial VALUES. Two true original north F55 witnesses
both satisfy CRT arithmetic, but original-phi seam verdicts
are OPPOSITE. Never infer Type gluing from numeric gluing.

A concrete genuinely non-dominating finite cover has
three moduli 4,6,9 and compatible independent residues
1,3,0 with genuine global witness 9.
No new Type sources, quotient class identity, P94A 4-cells,
unconditional P89 reflection, universal GK5AY seam,
W=1→seam, GK5BA kit or Gray.
Strict 空; independent Kuu→Qi; true F54 two Nat/two
categories/Blocks and original F55 Type history.
Append-only public root107; #1558 Draft/open/unmerged.
Pinned Lean v4.30.0-rc2, mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
No axioms, sorry/admit/native_decide.
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

private def fivefoldGK5BVNorthFirst :=
  KuuNativeF45Tree.pentagon0 northNativeF45FirstStage
    northNativeF45SecondStage northNativeF45ThirdStage
    northNativeF45FourthStage
private def fivefoldGK5BVNorthLast :=
  KuuNativeF45Tree.pentagon3 northNativeF45FirstStage
    northNativeF45SecondStage northNativeF45ThirdStage
    northNativeF45FourthStage

/-- A genuine ORIGINAL signed integer GK5BQ numerator's
canonical LOCAL observations for an arbitrary finite cover. -/
abbrev fivefoldGK5BVNorthObservedLocals
    {ι : Type*} (moduli : ι → Nat)
    (d j : Nat) (values : Nat → Int) : ι → Nat :=
  fun i => nativeGK5BTObservedNumeratorAbs d j values % moduli i

/-- A real constructed NORMALIZED global CRT witness of
the actual original signed numerator's local projections. -/
def fivefoldGK5BVNorthObservedGlue
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (d j : Nat) (values : Nat → Int) : Nat :=
  nativeGK5BVFiniteGlueNat s moduli
    (fivefoldGK5BVNorthObservedLocals moduli d j values)
    (nativeGK5BUObservedPairwise s moduli d j values)

/-- Global numeric CRT zeros for ALL the ACTUAL GK5BQ
cleared integer numerators of one true Int polynomial. -/
abbrev fivefoldGK5BVNorthFiniteZero
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (d : Nat) (P : Polynomial Int) : Prop :=
  ∀ j ∈ Finset.range (d + 1),
    fivefoldGK5BVNorthObservedGlue s moduli d j
      (fun n : Nat => P.eval (n : Int)) ≡ 0
        [MOD nativeGK5BUFiniteModulus s moduli]

/-- Necessary and sufficient finite noncoprime arithmetic
CRT criterion, without coprimality or nonzero assumptions. -/
theorem fivefoldGK5BVNorthFinite_pairwise_iff_global
    {ι : Type*} (s : Finset ι)
    (moduli residues : ι → Nat) :
    nativeGK5BUFinitePairwise s moduli residues ↔
      ∃ x : Nat, nativeGK5BUFiniteGlobal s moduli residues x :=
  nativeGK5BVFinitePairwise_iff_exists_global s moduli residues

/-- The same criterion with an exact bad-pair obstruction. -/
theorem fivefoldGK5BVNorthFinite_noGlobal_iff_badPair
    {ι : Type*} (s : Finset ι)
    (moduli residues : ι → Nat) :
    (¬ ∃ x : Nat, nativeGK5BUFiniteGlobal s moduli residues x) ↔
      ∃ i ∈ s, ∃ j ∈ s,
        ¬ residues i ≡ residues j
          [MOD Nat.gcd (moduli i) (moduli j)] :=
  nativeGK5BVFiniteNoGlobal_iff_badPair s moduli residues

/-- The genuine normalized global CRT representative
satisfies every local congruence of a compatible cover. -/
theorem fivefoldGK5BVNorthFinite_normalized_glues
    {ι : Type*} (s : Finset ι)
    (moduli residues : ι → Nat)
    (h : nativeGK5BUFinitePairwise s moduli residues) :
    nativeGK5BUFiniteGlobal s moduli residues
      (nativeGK5BVFiniteGlueNat s moduli residues h) :=
  nativeGK5BVFiniteGlueNat_global s moduli residues h

/-- The ACTUAL original signed numerator's local residue
family is automatically pairwise compatible, with its
genuine finite normalized global representative. -/
theorem fivefoldGK5BVNorthOriginalNumerator_finiteGlobal
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (d j : Nat) (values : Nat → Int) :
    nativeGK5BUFiniteGlobal s moduli
      (fivefoldGK5BVNorthObservedLocals moduli d j values)
      (fivefoldGK5BVNorthObservedGlue s moduli d j values) :=
  nativeGK5BVFiniteGlueNat_global s moduli
    (fivefoldGK5BVNorthObservedLocals moduli d j values)
    (nativeGK5BUObservedPairwise s moduli d j values)

/-- The normalized true finite CRT glue of the ORIGINAL
integer observation numerator is congruent to its genuine
natural absolute value modulo the TRUE finite lcm. -/
theorem fivefoldGK5BVNorthOriginalNumerator_glue_eq_natAbs
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (d j : Nat) (values : Nat → Int) :
    fivefoldGK5BVNorthObservedGlue s moduli d j values ≡
      nativeGK5BTObservedNumeratorAbs d j values
        [MOD nativeGK5BUFiniteModulus s moduli] :=
  nativeGK5BUFiniteGlobal_unique_mod_lcm s moduli
    (fivefoldGK5BVNorthObservedLocals moduli d j values)
    (fivefoldGK5BVNorthObservedGlue s moduli d j values)
    (nativeGK5BTObservedNumeratorAbs d j values)
    (fivefoldGK5BVNorthOriginalNumerator_finiteGlobal s moduli d j values)
    (nativeGK5BUObservedGlobal s moduli d j values)

/-- Genuine exact signed integer arithmetic descent:
normalized CRT glue zero iff the TRUE original GK5BQ
signed integer numerator is divisible by the finite lcm.
Negative values are handled via Int.natCast_dvd. -/
theorem fivefoldGK5BVNorthOriginalNumerator_glueZero_iff_lcmDvd
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (d j : Nat) (values : Nat → Int) :
    (fivefoldGK5BVNorthObservedGlue s moduli d j values ≡ 0
        [MOD nativeGK5BUFiniteModulus s moduli]) ↔
      ((nativeGK5BUFiniteModulus s moduli : Nat) : Int) ∣
        nativeGK5BQClearedNumerator d j values := by
  constructor
  · intro h
    apply Int.natCast_dvd.mpr
    exact Nat.modEq_zero_iff_dvd.mp
      ((fivefoldGK5BVNorthOriginalNumerator_glue_eq_natAbs
        s moduli d j values).symm.trans h)
  · intro h
    have hz : nativeGK5BTObservedNumeratorAbs d j values ≡ 0
        [MOD nativeGK5BUFiniteModulus s moduli] :=
      Nat.modEq_zero_iff_dvd.mpr (Int.natCast_dvd.mp h)
    exact (fivefoldGK5BVNorthOriginalNumerator_glue_eq_natAbs
      s moduli d j values).trans hz

/-- TRUE integer polynomial coefficient source of degree
≤d has every finite CRT glue zero whenever the true
finite LCM divides d!, with no dominating-site condition. -/
theorem fivefoldGK5BVIntegerSource_finiteZero
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (P : Polynomial Int) (d : Nat)
    (hdegree : P.natDegree ≤ d)
    (hlcm : nativeGK5BUFiniteModulus s moduli ∣ d.factorial) :
    fivefoldGK5BVNorthFiniteZero s moduli d P := by
  intro j hj
  apply (fivefoldGK5BVNorthOriginalNumerator_glueZero_iff_lcmDvd
    s moduli d j (fun n : Nat => P.eval (n : Int))).2
  exact (Int.natCast_dvd_natCast.mpr hlcm).trans
    (fivefoldGK5BQIntegerSource_divisibility P d hdegree j hj)

/-- Actual north original F55 Type witness contributes
its existing P92B Int polynomial VALUE only, never a
new F55 Type source from the numeric CRT reconstruction. -/
theorem fivefoldGK5BVNorthOriginalF55_finiteZero
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (f : NativeGK5AINorthPentagonCells) (d : Nat)
    (hdegree :
      (nativeGK5AIOriginalToP92Structural f).gk5bgDepthPolynomial.natDegree ≤ d)
    (hlcm : nativeGK5BUFiniteModulus s moduli ∣ d.factorial) :
    fivefoldGK5BVNorthFiniteZero s moduli d
      (nativeGK5AIOriginalToP92Structural f).gk5bgDepthPolynomial :=
  fivefoldGK5BVIntegerSource_finiteZero s moduli
    (nativeGK5AIOriginalToP92Structural f).gk5bgDepthPolynomial
    d hdegree hlcm

/-- Original north F55/P77 classes provide only their
already-descended Int polynomial VALUES for the finite
cover certificate, not structural Type quotient equalities. -/
theorem fivefoldGK5BVNorthP77_finiteZero
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (q : NativeF55RawVerticalFourClasses
      fivefoldGK5BVNorthFirst fivefoldGK5BVNorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort)
    (d : Nat)
    (hdegree : (nativeGK5BGPolyOnP77Class
      fivefoldGK5BVNorthFirst fivefoldGK5BVNorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort q).natDegree ≤ d)
    (hlcm : nativeGK5BUFiniteModulus s moduli ∣ d.factorial) :
    fivefoldGK5BVNorthFiniteZero s moduli d
      (nativeGK5BGPolyOnP77Class
        fivefoldGK5BVNorthFirst fivefoldGK5BVNorthLast
        northNativeF45PentagonLong northNativeF45PentagonShort q) :=
  fivefoldGK5BVIntegerSource_finiteZero s moduli
    (nativeGK5BGPolyOnP77Class
      fivefoldGK5BVNorthFirst fivefoldGK5BVNorthLast
      northNativeF45PentagonLong northNativeF45PentagonShort q)
    d hdegree hlcm

/-- Actual north primitive P=1 and distinct genuine F55
double inverse+right unit P=X² BOTH satisfy ANY finite
cover of true moduli with finite LCM dividing d!, despite
the original-phi seam existing for one but not the other. -/
theorem fivefoldGK5BVNorthBothFiniteZeroButOppositeSeams
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (d : Nat) (hbound : 2 ≤ d)
    (hlcm : nativeGK5BUFiniteModulus s moduli ∣ d.factorial)
    (frame : NativeC60FivePhaseGauge) (i : FivefoldIndex) :
    fivefoldGK5BVNorthFiniteZero s moduli d
      (nativeGK5AIOriginalToP92Structural
        nativeGK5AGNorthOriginalCell).gk5bgDepthPolynomial ∧
    fivefoldGK5BVNorthFiniteZero s moduli d
      (nativeGK5AIOriginalToP92Structural
        fivefoldGK5BFNorthDoubleInverseRightUnit).gk5bgDepthPolynomial ∧
    Nonempty (nativeGK5AZSeamAt nativeGK5AGNorthOriginalCell) ∧
    ¬ Nonempty (nativeGK5AZSeamAt
      fivefoldGK5BFNorthDoubleInverseRightUnit) := by
  obtain ⟨hyes, hno, _, _⟩ :=
    fivefoldGK5BQNorthPhysicalAndP89Boundary frame i
  exact ⟨fivefoldGK5BVNorthOriginalF55_finiteZero
      s moduli nativeGK5AGNorthOriginalCell d
      (le_trans fivefoldGK5BKNorthPrimitiveDouble_degree_le_two.1 hbound)
      hlcm,
    fivefoldGK5BVNorthOriginalF55_finiteZero
      s moduli fivefoldGK5BFNorthDoubleInverseRightUnit d
      (le_trans fivefoldGK5BKNorthPrimitiveDouble_degree_le_two.2 hbound)
      hlcm,
    hyes, hno⟩

/-- True original fifth-around physical north C60 gauge
and conditional P89 BadPair reflection remain separate. -/
theorem fivefoldGK5BVNorthPhysicalAndP89Boundary
    (frame : NativeC60FivePhaseGauge) (i : FivefoldIndex) :
    (fivefoldGK5AGNorthPhysicalFifthDarts frame i =
      (nativeC60GaugeDart frame .north (i + 4),
       nativeC60GaugeDart frame .north i)) ∧
    ((¬ Function.Injective
      (fivefoldGK5ANP94NorthPhysicalFourClassMap frame i)) ↔
        fivefoldGK5AQNorthReflectionObstruction) :=
  fivefoldGK5BRNorthPhysicalAndP89Boundary frame i

/-- TRUE three-site finite noncoprime test family, without
one locally dominating modulus: 4, 6 and 9 have LCM 36. -/
private def fivefoldGK5BVNorthThreeModuli (i : Fin 3) : Nat :=
  if i.val = 0 then 4 else if i.val = 1 then 6 else 9

/-- Independently chosen compatible local residues for
those moduli: 1 modulo 4, 3 modulo 6, 0 modulo 9. -/
private def fivefoldGK5BVNorthThreeResidues (i : Fin 3) : Nat :=
  if i.val = 0 then 1 else if i.val = 1 then 3 else 0

/-- Concrete TRUE global witness 9 for three overlapping
non-dominating local residue constraints. -/
theorem fivefoldGK5BVNorthThreeSite_globalWitness :
    nativeGK5BUFiniteGlobal (Finset.univ : Finset (Fin 3))
      fivefoldGK5BVNorthThreeModuli fivefoldGK5BVNorthThreeResidues 9 := by
  intro j _
  fin_cases j <;>
    decide

/-- The original three separately specified local
observations pass genuine pairwise gcd compatibility. -/
theorem fivefoldGK5BVNorthThreeSite_pairwise :
    nativeGK5BUFinitePairwise (Finset.univ : Finset (Fin 3))
      fivefoldGK5BVNorthThreeModuli fivefoldGK5BVNorthThreeResidues :=
  nativeGK5BUFiniteGlobal_implies_pairwise
    Finset.univ fivefoldGK5BVNorthThreeModuli
    fivefoldGK5BVNorthThreeResidues 9
    fivefoldGK5BVNorthThreeSite_globalWitness

/-- Concrete global CRT glue lies in same genuine finite
LCM class as the independent observed witness 9. -/
theorem fivefoldGK5BVNorthThreeSite_glue_eq_nine :
    nativeGK5BVFiniteGlueNat (Finset.univ : Finset (Fin 3))
      fivefoldGK5BVNorthThreeModuli fivefoldGK5BVNorthThreeResidues
      fivefoldGK5BVNorthThreeSite_pairwise ≡ 9
        [MOD nativeGK5BUFiniteModulus (Finset.univ : Finset (Fin 3))
          fivefoldGK5BVNorthThreeModuli] :=
  nativeGK5BUFiniteGlobal_unique_mod_lcm
    Finset.univ fivefoldGK5BVNorthThreeModuli
    fivefoldGK5BVNorthThreeResidues
    (nativeGK5BVFiniteGlueNat Finset.univ
      fivefoldGK5BVNorthThreeModuli fivefoldGK5BVNorthThreeResidues
      fivefoldGK5BVNorthThreeSite_pairwise)
    9
    (nativeGK5BVFiniteGlueNat_global
      Finset.univ fivefoldGK5BVNorthThreeModuli
      fivefoldGK5BVNorthThreeResidues
      fivefoldGK5BVNorthThreeSite_pairwise)
    fivefoldGK5BVNorthThreeSite_globalWitness

#print axioms fivefoldGK5BVNorthFinite_pairwise_iff_global
#print axioms fivefoldGK5BVNorthFinite_noGlobal_iff_badPair
#print axioms fivefoldGK5BVNorthFinite_normalized_glues
#print axioms fivefoldGK5BVNorthOriginalNumerator_finiteGlobal
#print axioms fivefoldGK5BVNorthOriginalNumerator_glue_eq_natAbs
#print axioms fivefoldGK5BVNorthOriginalNumerator_glueZero_iff_lcmDvd
#print axioms fivefoldGK5BVIntegerSource_finiteZero
#print axioms fivefoldGK5BVNorthOriginalF55_finiteZero
#print axioms fivefoldGK5BVNorthP77_finiteZero
#print axioms fivefoldGK5BVNorthBothFiniteZeroButOppositeSeams
#print axioms fivefoldGK5BVNorthPhysicalAndP89Boundary
#print axioms fivefoldGK5BVNorthThreeSite_globalWitness
#print axioms fivefoldGK5BVNorthThreeSite_pairwise
#print axioms fivefoldGK5BVNorthThreeSite_glue_eq_nine

end
end KUOS.Architecture.WuxingPentagonUnified
