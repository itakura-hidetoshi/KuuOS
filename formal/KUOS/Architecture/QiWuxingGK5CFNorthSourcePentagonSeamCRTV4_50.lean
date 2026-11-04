import KUOS.Architecture.QiWuxingGK5CENorthFourPentagonCRTV4_49
import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5CFOriginalPhiTypedPentagonComparison
import Mathlib.Tactic

/-!
Qi v4.50 — ACTUAL NORTH C60 ORIGINAL F55 SOURCE PENTAGON
VERSUS SIGNED GK5BQ NUMERATOR / NONCOPRIME CRT RINGHOM PENTAGON.

Independently certified GK5CF makes two genuinely different,
simultaneous presentations: five true heterogeneous polynomial RingHom
parenthesizations and five original F55 Type-valued proof compositions
with original P77 4-cell pentagon edges. A numerical RingHom pentagon
does NOT produce a higher P94A original→recursive-phi seam.

For the exact original north GK5BQ signed Int numerator, retain the
original GK5CE finite noncoprime CRT RingEquiv, original four-part
RingHom, all covers (including empty/ZMod 0), and three-cover tower.
The comparison to a genuine north original F55 source is inhabited
IFF its independent P94A local seam exists. The north primitive source
has a concrete seam; the same-F54-Hom double inverse has none despite
the same numerical CRT pentagon and both source gates N=S=1.

We additionally instantiate the original GK5CF pentagon at FOUR
genuine original F55 source pieces: a north primitive or original
double inverse followed by three actual original F55 identities.
All five P77 source 4-cell edges and two higher paths are genuine.
Right-unit P77/P94A transport makes every primitive vertex
seam-positive, while the double-inverse obstruction makes every
double-inverse vertex seam-negative. No unconstructed associator
2-cell, pentagonator 5-cell, global GK5AY seam, P89 reflection,
or original F55 4-cell is inferred from numerical CRT equalities.

Independent strict 空 → one-way Qi; original F54 and F55 dependent
Type-valued proofs retained; public root107; pinned Lean v4.30.0-rc2
and mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
#1558 remains Draft/open/unmerged. Append-only: no modified old
theorem source, sorry, axiom, admit, native_decide or Gray.
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

/-- TRUE original north C60 signed Int numerator CRT RingHom
naturality is a PROP, not the proof term of the GK5CE theorem. -/
def fivefoldGK5CFNorthSignedCRTRingHomBoundary
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (arity : Nat → Nat)
    (steps : (i : Nat) → Fin (arity i) →
      MvPolynomial (Fin (arity (i+1))) Int)
    (start a b c e depth : Nat)
    (indices : Fin (arity (start+(a+(b+(c+e))))) → Nat)
    (values : Nat → Int) : Prop :=
  (nativeGK5BWGlobalCompatibleHom s moduli).comp
    (fivefoldGK5CENorthGlobalFourEvalHom s moduli arity
      steps start a b c e depth indices values) =
  fivefoldGK5CENorthLocalFourEvalHom s moduli arity
    steps start a b c e depth indices values

/-- The original signed four-part global-to-local CRT
RingHom equation is already certified independently of F55. -/
theorem fivefoldGK5CFNorthSignedCRTRingHomBoundary_valid
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (arity : Nat → Nat)
    (steps : (i : Nat) → Fin (arity i) →
      MvPolynomial (Fin (arity (i+1))) Int)
    (start a b c e depth : Nat)
    (indices : Fin (arity (start+(a+(b+(c+e))))) → Nat)
    (values : Nat → Int) :
    fivefoldGK5CFNorthSignedCRTRingHomBoundary s moduli arity
      steps start a b c e depth indices values :=
  fivefoldGK5CENorthFourCRT_RingHom s moduli arity
    steps start a b c e depth indices values

/-- Joint true north numerical signed CRT and actual
original→phi Type-valued P94A comparison. These are two
separately typed proof layers, NOT an inferred source lift. -/
def fivefoldGK5CFNorthSignedCRTHigherComparison
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (arity : Nat → Nat)
    (steps : (i : Nat) → Fin (arity i) →
      MvPolynomial (Fin (arity (i+1))) Int)
    (start a b c e depth : Nat)
    (indices : Fin (arity (start+(a+(b+(c+e))))) → Nat)
    (values : Nat → Int)
    (src : KuuNativeF45Tree.DepthRotationRoute.PresentedCell
      (.pentagon .north)
      northNativeF45PentagonLong northNativeF45PentagonShort) : Prop :=
  fivefoldGK5CFNorthSignedCRTRingHomBoundary s moduli arity
    steps start a b c e depth indices values ∧
  nativeGK5CFPentagonHigherComparison
    (α := fivefoldGK5CCNorthFiniteVariableTypes arity)
    steps start a b c e src

/-- Sharp descent criterion at the exact north signed CRT
RingHom: the additional higher comparison exists IFF the
independent genuine original F55 seam is supplied. -/
theorem fivefoldGK5CFNorthSignedCRTHigherComparison_iff
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (arity : Nat → Nat)
    (steps : (i : Nat) → Fin (arity i) →
      MvPolynomial (Fin (arity (i+1))) Int)
    (start a b c e depth : Nat)
    (indices : Fin (arity (start+(a+(b+(c+e))))) → Nat)
    (values : Nat → Int)
    (src : KuuNativeF45Tree.DepthRotationRoute.PresentedCell
      (.pentagon .north)
      northNativeF45PentagonLong northNativeF45PentagonShort) :
    fivefoldGK5CFNorthSignedCRTHigherComparison s moduli arity
      steps start a b c e depth indices values src ↔
    Nonempty (nativeGK5AZSeamAt src) := by
  constructor
  · intro h
    exact (nativeGK5CFPentagonHigherComparison_iff
      (α := fivefoldGK5CCNorthFiniteVariableTypes arity)
      steps start a b c e src).mp h.2
  · intro h
    exact ⟨fivefoldGK5CFNorthSignedCRTRingHomBoundary_valid
      s moduli arity steps start a b c e depth indices values,
      (nativeGK5CFPentagonHigherComparison_iff
        (α := fivefoldGK5CCNorthFiniteVariableTypes arity)
        steps start a b c e src).mpr h⟩

/-- A true north original pentagon primitive preserves the
original signed CRT RingHom and has an actual selected P94A
original→phi comparison at the correct original F54 Hom. -/
theorem fivefoldGK5CFNorthPrimitive_signedCRT_positive
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (arity : Nat → Nat)
    (steps : (i : Nat) → Fin (arity i) →
      MvPolynomial (Fin (arity (i+1))) Int)
    (start a b c e depth : Nat)
    (indices : Fin (arity (start+(a+(b+(c+e))))) → Nat)
    (values : Nat → Int) :
    fivefoldGK5CFNorthSignedCRTHigherComparison s moduli arity
      steps start a b c e depth indices values
      nativeGK5AGNorthOriginalCell :=
  (fivefoldGK5CFNorthSignedCRTHigherComparison_iff
    s moduli arity steps start a b c e depth indices values
    nativeGK5AGNorthOriginalCell).mpr ⟨.refl _⟩

/-- The true same-F54-Hom double inverse retains the genuine
signed CRT and numeric pentagon yet its P94A structural source
seam is impossible by GK5BF inversion-depth weight 4 ≠ 1. -/
theorem fivefoldGK5CFNorthDoubleInverse_signedCRT_no
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (arity : Nat → Nat)
    (steps : (i : Nat) → Fin (arity i) →
      MvPolynomial (Fin (arity (i+1))) Int)
    (start a b c e depth : Nat)
    (indices : Fin (arity (start+(a+(b+(c+e))))) → Nat)
    (values : Nat → Int) :
    ¬ fivefoldGK5CFNorthSignedCRTHigherComparison s moduli arity
      steps start a b c e depth indices values
      nativeGK5BFNorthDoubleInverse := by
  intro h
  exact nativeGK5BFNorthDoubleInverse_no_seam
    ((fivefoldGK5CFNorthSignedCRTHigherComparison_iff
      s moduli arity steps start a b c e depth indices values
      nativeGK5BFNorthDoubleInverse).mp h)

/-- Genuine signed GK5BQ numerators, noncoprime finite CRT
RingEquiv and arbitrary four-part MvPolynomial substitution
all work at the SAME two original north F54 source classes;
N(phi)=S(phi)=1 at BOTH, yet only the primitive lifts. -/
theorem fivefoldGK5CFNorthSignedCRT_sameFiber_split
    {ι : Type*} (s : Finset ι) (moduli : ι → Nat)
    (arity : Nat → Nat)
    (steps : (i : Nat) → Fin (arity i) →
      MvPolynomial (Fin (arity (i+1))) Int)
    (start a b c e depth : Nat)
    (indices : Fin (arity (start+(a+(b+(c+e))))) → Nat)
    (values : Nat → Int) :
    fivefoldGK5CFNorthSignedCRTRingHomBoundary s moduli arity
      steps start a b c e depth indices values ∧
    nativeGK5BFCountSignedGate nativeGK5AGNorthOriginalCell ∧
    nativeGK5BFCountSignedGate nativeGK5BFNorthDoubleInverse ∧
    fivefoldGK5CFNorthSignedCRTHigherComparison s moduli arity
      steps start a b c e depth indices values
      nativeGK5AGNorthOriginalCell ∧
    ¬ fivefoldGK5CFNorthSignedCRTHigherComparison s moduli arity
      steps start a b c e depth indices values
      nativeGK5BFNorthDoubleInverse := by
  obtain ⟨hN₁, hS₁, _, hN₂, hS₂, _⟩ :=
    nativeGK5BFNorthSameFiber_joint_gate_not_sufficient
  exact ⟨fivefoldGK5CFNorthSignedCRTRingHomBoundary_valid
    s moduli arity steps start a b c e depth indices values,
    ⟨hN₁, hS₁⟩, ⟨hN₂, hS₂⟩,
    fivefoldGK5CFNorthPrimitive_signedCRT_positive
      s moduli arity steps start a b c e depth indices values,
    fivefoldGK5CFNorthDoubleInverse_signedCRT_no
      s moduli arity steps start a b c e depth indices values⟩

/-- One TRUE original north F55 pentagon source followed
by three ACTUAL original F55 identity 3-cells, not
an invented polynomial-to-F55 source operation. -/
def fivefoldGK5CFNorthFourPrimitiveOriginalSource :
    KuuNativeF45Tree.DepthRotationRoute.PresentedCell (.pentagon .north)
      northNativeF45PentagonLong northNativeF45PentagonShort :=
  nativeGK5CFOriginalLeftLeftLeft
    nativeGK5AGNorthOriginalCell
    (.ident northNativeF45PentagonShort)
    (.ident northNativeF45PentagonShort)
    (.ident northNativeF45PentagonShort)

/-- Same genuine four-input original F55 source pentagon,
but starting at the ORIGINAL double-inverse F55 Type proof. -/
def fivefoldGK5CFNorthFourInverseOriginalSource :
    KuuNativeF45Tree.DepthRotationRoute.PresentedCell (.pentagon .north)
      northNativeF45PentagonLong northNativeF45PentagonShort :=
  nativeGK5CFOriginalLeftLeftLeft
    nativeGK5BFNorthDoubleInverse
    (.ident northNativeF45PentagonShort)
    (.ident northNativeF45PentagonShort)
    (.ident northNativeF45PentagonShort)

/-- A concrete TRUE P94A local original→phi four-cell for
the triple-original-identity primitive source, constructed
by three original P77/P94A right-unit proof transports. -/
def fivefoldGK5CFNorthFourPrimitiveLocalSeam :
    nativeGK5AZSeamAt fivefoldGK5CFNorthFourPrimitiveOriginalSource :=
  nativeGK5BCRightUnitSeam_of_child
    (.trans (.trans nativeGK5AGNorthOriginalCell
      (.ident northNativeF45PentagonShort))
      (.ident northNativeF45PentagonShort))
    (nativeGK5BCRightUnitSeam_of_child
      (.trans nativeGK5AGNorthOriginalCell
        (.ident northNativeF45PentagonShort))
      (nativeGK5BCRightUnitSeam_of_child
        nativeGK5AGNorthOriginalCell (.refl _)))

/-- Three real original F55 right-unit extensions CANNOT
remove the double-inverse P94A seam obstruction. -/
theorem fivefoldGK5CFNorthFourInverseLocalSeam_no :
    ¬ Nonempty (nativeGK5AZSeamAt
      fivefoldGK5CFNorthFourInverseOriginalSource) := by
  rintro ⟨w⟩
  have w₂ := nativeGK5BCRightUnitSeam_to_child
    (.trans (.trans nativeGK5BFNorthDoubleInverse
      (.ident northNativeF45PentagonShort))
      (.ident northNativeF45PentagonShort)) w
  have w₁ := nativeGK5BCRightUnitSeam_to_child
    (.trans nativeGK5BFNorthDoubleInverse
      (.ident northNativeF45PentagonShort)) w₂
  have w₀ := nativeGK5BCRightUnitSeam_to_child
    nativeGK5BFNorthDoubleInverse w₁
  exact nativeGK5BFNorthDoubleInverse_no_seam ⟨w₀⟩

/-- The five genuine original F55 P77 source pentagon edges
are inhabited for the primitive with three right identities.
These are Type-valued source four-cells, not CRT equalities. -/
theorem fivefoldGK5CFNorthPrimitiveOriginalFiveEdges :
    Nonempty (NativeF55RawVerticalFourCell
      (KuuNativeF45Tree.pentagon0 northNativeF45FirstStage
        northNativeF45SecondStage northNativeF45ThirdStage
        northNativeF45FourthStage)
      (KuuNativeF45Tree.pentagon3 northNativeF45FirstStage
        northNativeF45SecondStage northNativeF45ThirdStage
        northNativeF45FourthStage)
      (nativeGK5CFOriginalLeftLeftLeft nativeGK5AGNorthOriginalCell
        (.ident northNativeF45PentagonShort)
        (.ident northNativeF45PentagonShort)
        (.ident northNativeF45PentagonShort))
      (nativeGK5CFOriginalLeftMiddle nativeGK5AGNorthOriginalCell
        (.ident northNativeF45PentagonShort)
        (.ident northNativeF45PentagonShort)
        (.ident northNativeF45PentagonShort))) :=
  (nativeGK5CFOriginalFiveEdges_exist
    nativeGK5AGNorthOriginalCell
    (.ident northNativeF45PentagonShort)
    (.ident northNativeF45PentagonShort)
    (.ident northNativeF45PentagonShort)).1

/-- The full north ORIGINAL F55 primitive pentagon admits
direct local original→phi seams at ALL FIVE real source vertices,
from one actual local seed and the five P77 4-cell edges.
Not a universal GK5AY seam on arbitrary F55 sources. -/
theorem fivefoldGK5CFNorthFourPrimitivePentagon_allSeams :
    Nonempty (nativeGK5AZSeamAt
      (nativeGK5CFOriginalLeftMiddle nativeGK5AGNorthOriginalCell
        (.ident northNativeF45PentagonShort)
        (.ident northNativeF45PentagonShort)
        (.ident northNativeF45PentagonShort))) ∧
    Nonempty (nativeGK5AZSeamAt
      (nativeGK5CFOriginalRightMiddle nativeGK5AGNorthOriginalCell
        (.ident northNativeF45PentagonShort)
        (.ident northNativeF45PentagonShort)
        (.ident northNativeF45PentagonShort))) ∧
    Nonempty (nativeGK5AZSeamAt
      (nativeGK5CFOriginalRightRight nativeGK5AGNorthOriginalCell
        (.ident northNativeF45PentagonShort)
        (.ident northNativeF45PentagonShort)
        (.ident northNativeF45PentagonShort))) ∧
    Nonempty (nativeGK5AZSeamAt
      (nativeGK5CFOriginalMiddle nativeGK5AGNorthOriginalCell
        (.ident northNativeF45PentagonShort)
        (.ident northNativeF45PentagonShort)
        (.ident northNativeF45PentagonShort))) :=
  (nativeGK5CFOriginalSeamPentagon_glue_iff
    nativeGK5AGNorthOriginalCell
    (.ident northNativeF45PentagonShort)
    (.ident northNativeF45PentagonShort)
    (.ident northNativeF45PentagonShort)).mp
      ⟨fivefoldGK5CFNorthFourPrimitiveLocalSeam⟩

/-- The same original F54 north four-part source pentagon
starting at the actual double inverse cannot have a seam at
EVERY vertex, by the P77 pentagon iff and genuine obstruction.
This does NOT deny the five actual P77 four-cell edges. -/
theorem fivefoldGK5CFNorthFourInversePentagon_noAllSeams :
    ¬ (Nonempty (nativeGK5AZSeamAt
        (nativeGK5CFOriginalLeftMiddle nativeGK5BFNorthDoubleInverse
          (.ident northNativeF45PentagonShort)
          (.ident northNativeF45PentagonShort)
          (.ident northNativeF45PentagonShort))) ∧
       Nonempty (nativeGK5AZSeamAt
        (nativeGK5CFOriginalRightMiddle nativeGK5BFNorthDoubleInverse
          (.ident northNativeF45PentagonShort)
          (.ident northNativeF45PentagonShort)
          (.ident northNativeF45PentagonShort))) ∧
       Nonempty (nativeGK5AZSeamAt
        (nativeGK5CFOriginalRightRight nativeGK5BFNorthDoubleInverse
          (.ident northNativeF45PentagonShort)
          (.ident northNativeF45PentagonShort)
          (.ident northNativeF45PentagonShort))) ∧
       Nonempty (nativeGK5AZSeamAt
        (nativeGK5CFOriginalMiddle nativeGK5BFNorthDoubleInverse
          (.ident northNativeF45PentagonShort)
          (.ident northNativeF45PentagonShort)
          (.ident northNativeF45PentagonShort)))) := by
  intro hall
  exact fivefoldGK5CFNorthFourInverseLocalSeam_no
    ((nativeGK5CFOriginalSeamPentagon_glue_iff
      nativeGK5BFNorthDoubleInverse
      (.ident northNativeF45PentagonShort)
      (.ident northNativeF45PentagonShort)
      (.ident northNativeF45PentagonShort)).mpr hall)

/-- Complete true NORTH signed GK5BQ finite CRT triple-cover
RingHom gluing holds INDEPENDENTLY of the missing double inverse
P94A source seam. Thus numeric descent != higher source descent. -/
theorem fivefoldGK5CFNorthSignedThreeCover_and_sourceObstruction
    {ι : Type*} (s t v : Finset ι) (moduli : ι → Nat)
    (inc : t ⊆ s) (inc' : v ⊆ t)
    (arity : Nat → Nat)
    (steps : (i : Nat) → Fin (arity i) →
      MvPolynomial (Fin (arity (i+1))) Int)
    (start a b c e depth : Nat)
    (indices : Fin (arity (start+(a+(b+(c+e))))) → Nat)
    (values : Nat → Int)
    (P : MvPolynomial (Fin (arity start)) Int) :
    (nativeGK5BXCompatibleRestrictHom t v moduli inc'
      (nativeGK5BXCompatibleRestrictHom s t moduli inc
        (nativeGK5BWFiniteCRTRingEquiv s moduli
          (fivefoldGK5CENorthGlobalFourEvalHom s moduli arity
            steps start a b c e depth indices values P))) =
      fivefoldGK5CENorthLocalFourEvalHom v moduli arity
        steps start a b c e depth indices values P) ∧
    ¬ Nonempty (nativeGK5AZSeamAt nativeGK5BFNorthDoubleInverse) :=
  ⟨fivefoldGK5CENorthFourCRT_threeCover s t v moduli inc inc'
     arity steps start a b c e depth indices values P,
   nativeGK5BFNorthDoubleInverse_no_seam⟩

#print axioms fivefoldGK5CFNorthSignedCRTRingHomBoundary
#print axioms fivefoldGK5CFNorthSignedCRTRingHomBoundary_valid
#print axioms fivefoldGK5CFNorthSignedCRTHigherComparison
#print axioms fivefoldGK5CFNorthSignedCRTHigherComparison_iff
#print axioms fivefoldGK5CFNorthPrimitive_signedCRT_positive
#print axioms fivefoldGK5CFNorthDoubleInverse_signedCRT_no
#print axioms fivefoldGK5CFNorthSignedCRT_sameFiber_split
#print axioms fivefoldGK5CFNorthFourPrimitiveOriginalSource
#print axioms fivefoldGK5CFNorthFourInverseOriginalSource
#print axioms fivefoldGK5CFNorthFourPrimitiveLocalSeam
#print axioms fivefoldGK5CFNorthFourInverseLocalSeam_no
#print axioms fivefoldGK5CFNorthPrimitiveOriginalFiveEdges
#print axioms fivefoldGK5CFNorthFourPrimitivePentagon_allSeams
#print axioms fivefoldGK5CFNorthFourInversePentagon_noAllSeams
#print axioms fivefoldGK5CFNorthSignedThreeCover_and_sourceObstruction

end
end KUOS.Architecture.WuxingPentagonUnified
