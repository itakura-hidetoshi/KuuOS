import KUOS.DependentOriginationGrayC60NativeH0ConnectivityV5_163
import Mathlib.Algebra.Homology.ShortComplex.ModuleCat
import Mathlib.Algebra.Homology.ShortComplex.HomologicalComplex

namespace KUOS.DependentOriginationGrayC60NativeH1ContractingHomotopyV5_164

open CategoryTheory Limits
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationGrayC60IntegerOrientedSurfaceCycleV5_159
open KUOS.DependentOriginationGrayC60IntegralBoundaryLinearMapV5_159
open KUOS.DependentOriginationGrayC60IntegralChainComplexV5_160
open KUOS.DependentOriginationGrayC60NativeChainComplexV5_160
open KUOS.DependentOriginationGrayC60NativeH0ConnectivityV5_163

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# F59-F16 / v5.164 — C60 integer H₁ vanishes in actual Mathlib complex

The original 60 dart vertices and 90 original signed edges admit a concrete
59-edge primal spanning tree, the one constructed in F59-F15.
The remaining 31 edges form a dual spanning tree on all 32 actual oriented
C60 faces. Both finite trees are explicitly enumerated below as signed
primal root-to-vertex paths and dual cut-filling face lists.

Each of the NINETY physical edge basis chains satisfies, over integers,
  d₂ (faceFill e) + pathLift (d₁ e) = e.
The entire 90x90 integer coefficient assertion is kernel-checked using
`decide` on original pentagonal/hexagonal signed incidence data, without
`native_decide`, sorry, admit, or new axioms. Linearity upgrades this
to d₂ ∘ Q + P ∘ d₁ = id on ALL original integer 1-chains.
Consequently ker d₁ = im d₂ and native Mathlib degree-one homology is zero.

No geometric homeomorphism, Gray-F55 global 3-cell equivalence, or
Stage-II omega identification is inferred.
-/

/-- Explicit signed paths in the original 59-edge spanning tree,
from the north-spoke root to each one of the sixty original darts.
No edges or vertices outside the existing KuuOS C60 carrier. -/
def c60F16PrimalPathList (d : IcosahedralDart) :
    List (TruncatedIcosahedralEdge × ℤ) :=
  if d = (.first (.northSpoke 0) : IcosahedralDart) then
    []
  else if d = (.first (.northSpoke 1) : IcosahedralDart) then
    [
      (.around ⟨.north, .s0⟩, 1)
    ]
  else if d = (.first (.northSpoke 2) : IcosahedralDart) then
    [
      (.around ⟨.north, .s0⟩, 1),
      (.around ⟨.north, .s1⟩, 1)
    ]
  else if d = (.first (.northSpoke 3) : IcosahedralDart) then
    [
      (.around ⟨.north, .s0⟩, 1),
      (.around ⟨.north, .s1⟩, 1),
      (.around ⟨.north, .s2⟩, 1)
    ]
  else if d = (.first (.northSpoke 4) : IcosahedralDart) then
    [
      (.around ⟨.north, .s0⟩, 1),
      (.around ⟨.north, .s1⟩, 1),
      (.around ⟨.north, .s2⟩, 1),
      (.around ⟨.north, .s3⟩, 1)
    ]
  else if d = (.first (.southSpoke 0) : IcosahedralDart) then
    [
      (.cross (.northSpoke 0), 1),
      (.around ⟨.upper 0, .s0⟩, 1),
      (.around ⟨.upper 0, .s1⟩, 1),
      (.cross (.crossAligned 0), 1),
      (.around ⟨.lower 0, .s2⟩, -1),
      (.around ⟨.lower 0, .s1⟩, -1),
      (.around ⟨.lower 0, .s0⟩, -1),
      (.cross (.southSpoke 0), -1)
    ]
  else if d = (.first (.southSpoke 1) : IcosahedralDart) then
    [
      (.cross (.northSpoke 0), 1),
      (.around ⟨.upper 0, .s0⟩, 1),
      (.around ⟨.upper 0, .s1⟩, 1),
      (.cross (.crossAligned 0), 1),
      (.around ⟨.lower 0, .s2⟩, -1),
      (.around ⟨.lower 0, .s1⟩, -1),
      (.around ⟨.lower 0, .s0⟩, -1),
      (.cross (.southSpoke 0), -1),
      (.around ⟨.south, .s0⟩, 1)
    ]
  else if d = (.first (.southSpoke 2) : IcosahedralDart) then
    [
      (.cross (.northSpoke 0), 1),
      (.around ⟨.upper 0, .s0⟩, 1),
      (.around ⟨.upper 0, .s1⟩, 1),
      (.cross (.crossAligned 0), 1),
      (.around ⟨.lower 0, .s2⟩, -1),
      (.around ⟨.lower 0, .s1⟩, -1),
      (.around ⟨.lower 0, .s0⟩, -1),
      (.cross (.southSpoke 0), -1),
      (.around ⟨.south, .s0⟩, 1),
      (.around ⟨.south, .s1⟩, 1)
    ]
  else if d = (.first (.southSpoke 3) : IcosahedralDart) then
    [
      (.cross (.northSpoke 0), 1),
      (.around ⟨.upper 0, .s0⟩, 1),
      (.around ⟨.upper 0, .s1⟩, 1),
      (.cross (.crossAligned 0), 1),
      (.around ⟨.lower 0, .s2⟩, -1),
      (.around ⟨.lower 0, .s1⟩, -1),
      (.around ⟨.lower 0, .s0⟩, -1),
      (.cross (.southSpoke 0), -1),
      (.around ⟨.south, .s0⟩, 1),
      (.around ⟨.south, .s1⟩, 1),
      (.around ⟨.south, .s2⟩, 1)
    ]
  else if d = (.first (.southSpoke 4) : IcosahedralDart) then
    [
      (.cross (.northSpoke 0), 1),
      (.around ⟨.upper 0, .s0⟩, 1),
      (.around ⟨.upper 0, .s1⟩, 1),
      (.cross (.crossAligned 0), 1),
      (.around ⟨.lower 0, .s2⟩, -1),
      (.around ⟨.lower 0, .s1⟩, -1),
      (.around ⟨.lower 0, .s0⟩, -1),
      (.cross (.southSpoke 0), -1),
      (.around ⟨.south, .s0⟩, 1),
      (.around ⟨.south, .s1⟩, 1),
      (.around ⟨.south, .s2⟩, 1),
      (.around ⟨.south, .s3⟩, 1)
    ]
  else if d = (.first (.upperRing 0) : IcosahedralDart) then
    [
      (.cross (.northSpoke 0), 1),
      (.around ⟨.upper 0, .s0⟩, 1)
    ]
  else if d = (.first (.upperRing 1) : IcosahedralDart) then
    [
      (.around ⟨.north, .s0⟩, 1),
      (.cross (.northSpoke 1), 1),
      (.around ⟨.upper 1, .s0⟩, 1)
    ]
  else if d = (.first (.upperRing 2) : IcosahedralDart) then
    [
      (.around ⟨.north, .s0⟩, 1),
      (.around ⟨.north, .s1⟩, 1),
      (.cross (.northSpoke 2), 1),
      (.around ⟨.upper 2, .s0⟩, 1)
    ]
  else if d = (.first (.upperRing 3) : IcosahedralDart) then
    [
      (.around ⟨.north, .s0⟩, 1),
      (.around ⟨.north, .s1⟩, 1),
      (.around ⟨.north, .s2⟩, 1),
      (.cross (.northSpoke 3), 1),
      (.around ⟨.upper 3, .s0⟩, 1)
    ]
  else if d = (.first (.upperRing 4) : IcosahedralDart) then
    [
      (.around ⟨.north, .s0⟩, 1),
      (.around ⟨.north, .s1⟩, 1),
      (.around ⟨.north, .s2⟩, 1),
      (.around ⟨.north, .s3⟩, 1),
      (.cross (.northSpoke 4), 1),
      (.around ⟨.upper 4, .s0⟩, 1)
    ]
  else if d = (.first (.lowerRing 0) : IcosahedralDart) then
    [
      (.cross (.northSpoke 0), 1),
      (.around ⟨.upper 0, .s0⟩, 1),
      (.around ⟨.upper 0, .s1⟩, 1),
      (.cross (.crossAligned 0), 1),
      (.around ⟨.lower 0, .s2⟩, -1),
      (.around ⟨.lower 0, .s1⟩, -1)
    ]
  else if d = (.first (.lowerRing 1) : IcosahedralDart) then
    [
      (.around ⟨.north, .s0⟩, 1),
      (.cross (.northSpoke 1), 1),
      (.around ⟨.upper 1, .s0⟩, 1),
      (.around ⟨.upper 1, .s1⟩, 1),
      (.cross (.crossAligned 1), 1),
      (.around ⟨.lower 1, .s2⟩, -1),
      (.around ⟨.lower 1, .s1⟩, -1)
    ]
  else if d = (.first (.lowerRing 2) : IcosahedralDart) then
    [
      (.around ⟨.north, .s0⟩, 1),
      (.around ⟨.north, .s1⟩, 1),
      (.cross (.northSpoke 2), 1),
      (.around ⟨.upper 2, .s0⟩, 1),
      (.around ⟨.upper 2, .s1⟩, 1),
      (.cross (.crossAligned 2), 1),
      (.around ⟨.lower 2, .s2⟩, -1),
      (.around ⟨.lower 2, .s1⟩, -1)
    ]
  else if d = (.first (.lowerRing 3) : IcosahedralDart) then
    [
      (.around ⟨.north, .s0⟩, 1),
      (.around ⟨.north, .s1⟩, 1),
      (.around ⟨.north, .s2⟩, 1),
      (.cross (.northSpoke 3), 1),
      (.around ⟨.upper 3, .s0⟩, 1),
      (.around ⟨.upper 3, .s1⟩, 1),
      (.cross (.crossAligned 3), 1),
      (.around ⟨.lower 3, .s2⟩, -1),
      (.around ⟨.lower 3, .s1⟩, -1)
    ]
  else if d = (.first (.lowerRing 4) : IcosahedralDart) then
    [
      (.around ⟨.north, .s0⟩, 1),
      (.around ⟨.north, .s1⟩, 1),
      (.around ⟨.north, .s2⟩, 1),
      (.around ⟨.north, .s3⟩, 1),
      (.cross (.northSpoke 4), 1),
      (.around ⟨.upper 4, .s0⟩, 1),
      (.around ⟨.upper 4, .s1⟩, 1),
      (.cross (.crossAligned 4), 1),
      (.around ⟨.lower 4, .s2⟩, -1),
      (.around ⟨.lower 4, .s1⟩, -1)
    ]
  else if d = (.first (.crossAligned 0) : IcosahedralDart) then
    [
      (.cross (.northSpoke 0), 1),
      (.around ⟨.upper 0, .s0⟩, 1),
      (.around ⟨.upper 0, .s1⟩, 1)
    ]
  else if d = (.first (.crossAligned 1) : IcosahedralDart) then
    [
      (.around ⟨.north, .s0⟩, 1),
      (.cross (.northSpoke 1), 1),
      (.around ⟨.upper 1, .s0⟩, 1),
      (.around ⟨.upper 1, .s1⟩, 1)
    ]
  else if d = (.first (.crossAligned 2) : IcosahedralDart) then
    [
      (.around ⟨.north, .s0⟩, 1),
      (.around ⟨.north, .s1⟩, 1),
      (.cross (.northSpoke 2), 1),
      (.around ⟨.upper 2, .s0⟩, 1),
      (.around ⟨.upper 2, .s1⟩, 1)
    ]
  else if d = (.first (.crossAligned 3) : IcosahedralDart) then
    [
      (.around ⟨.north, .s0⟩, 1),
      (.around ⟨.north, .s1⟩, 1),
      (.around ⟨.north, .s2⟩, 1),
      (.cross (.northSpoke 3), 1),
      (.around ⟨.upper 3, .s0⟩, 1),
      (.around ⟨.upper 3, .s1⟩, 1)
    ]
  else if d = (.first (.crossAligned 4) : IcosahedralDart) then
    [
      (.around ⟨.north, .s0⟩, 1),
      (.around ⟨.north, .s1⟩, 1),
      (.around ⟨.north, .s2⟩, 1),
      (.around ⟨.north, .s3⟩, 1),
      (.cross (.northSpoke 4), 1),
      (.around ⟨.upper 4, .s0⟩, 1),
      (.around ⟨.upper 4, .s1⟩, 1)
    ]
  else if d = (.first (.crossShifted 0) : IcosahedralDart) then
    [
      (.around ⟨.north, .s0⟩, 1),
      (.cross (.northSpoke 1), 1),
      (.around ⟨.upper 1, .s0⟩, 1),
      (.around ⟨.upper 1, .s1⟩, 1),
      (.around ⟨.upper 1, .s2⟩, 1)
    ]
  else if d = (.first (.crossShifted 1) : IcosahedralDart) then
    [
      (.around ⟨.north, .s0⟩, 1),
      (.around ⟨.north, .s1⟩, 1),
      (.cross (.northSpoke 2), 1),
      (.around ⟨.upper 2, .s0⟩, 1),
      (.around ⟨.upper 2, .s1⟩, 1),
      (.around ⟨.upper 2, .s2⟩, 1)
    ]
  else if d = (.first (.crossShifted 2) : IcosahedralDart) then
    [
      (.around ⟨.north, .s0⟩, 1),
      (.around ⟨.north, .s1⟩, 1),
      (.around ⟨.north, .s2⟩, 1),
      (.cross (.northSpoke 3), 1),
      (.around ⟨.upper 3, .s0⟩, 1),
      (.around ⟨.upper 3, .s1⟩, 1),
      (.around ⟨.upper 3, .s2⟩, 1)
    ]
  else if d = (.first (.crossShifted 3) : IcosahedralDart) then
    [
      (.around ⟨.north, .s0⟩, 1),
      (.around ⟨.north, .s1⟩, 1),
      (.around ⟨.north, .s2⟩, 1),
      (.around ⟨.north, .s3⟩, 1),
      (.cross (.northSpoke 4), 1),
      (.around ⟨.upper 4, .s0⟩, 1),
      (.around ⟨.upper 4, .s1⟩, 1),
      (.around ⟨.upper 4, .s2⟩, 1)
    ]
  else if d = (.first (.crossShifted 4) : IcosahedralDart) then
    [
      (.cross (.northSpoke 0), 1),
      (.around ⟨.upper 0, .s0⟩, 1),
      (.around ⟨.upper 0, .s1⟩, 1),
      (.around ⟨.upper 0, .s2⟩, 1)
    ]
  else if d = (.second (.northSpoke 0) : IcosahedralDart) then
    [
      (.cross (.northSpoke 0), 1)
    ]
  else if d = (.second (.northSpoke 1) : IcosahedralDart) then
    [
      (.around ⟨.north, .s0⟩, 1),
      (.cross (.northSpoke 1), 1)
    ]
  else if d = (.second (.northSpoke 2) : IcosahedralDart) then
    [
      (.around ⟨.north, .s0⟩, 1),
      (.around ⟨.north, .s1⟩, 1),
      (.cross (.northSpoke 2), 1)
    ]
  else if d = (.second (.northSpoke 3) : IcosahedralDart) then
    [
      (.around ⟨.north, .s0⟩, 1),
      (.around ⟨.north, .s1⟩, 1),
      (.around ⟨.north, .s2⟩, 1),
      (.cross (.northSpoke 3), 1)
    ]
  else if d = (.second (.northSpoke 4) : IcosahedralDart) then
    [
      (.around ⟨.north, .s0⟩, 1),
      (.around ⟨.north, .s1⟩, 1),
      (.around ⟨.north, .s2⟩, 1),
      (.around ⟨.north, .s3⟩, 1),
      (.cross (.northSpoke 4), 1)
    ]
  else if d = (.second (.southSpoke 0) : IcosahedralDart) then
    [
      (.cross (.northSpoke 0), 1),
      (.around ⟨.upper 0, .s0⟩, 1),
      (.around ⟨.upper 0, .s1⟩, 1),
      (.cross (.crossAligned 0), 1),
      (.around ⟨.lower 0, .s2⟩, -1),
      (.around ⟨.lower 0, .s1⟩, -1),
      (.around ⟨.lower 0, .s0⟩, -1)
    ]
  else if d = (.second (.southSpoke 1) : IcosahedralDart) then
    [
      (.around ⟨.north, .s0⟩, 1),
      (.cross (.northSpoke 1), 1),
      (.around ⟨.upper 1, .s0⟩, 1),
      (.around ⟨.upper 1, .s1⟩, 1),
      (.cross (.crossAligned 1), 1),
      (.around ⟨.lower 1, .s2⟩, -1),
      (.around ⟨.lower 1, .s1⟩, -1),
      (.around ⟨.lower 1, .s0⟩, -1)
    ]
  else if d = (.second (.southSpoke 2) : IcosahedralDart) then
    [
      (.around ⟨.north, .s0⟩, 1),
      (.around ⟨.north, .s1⟩, 1),
      (.cross (.northSpoke 2), 1),
      (.around ⟨.upper 2, .s0⟩, 1),
      (.around ⟨.upper 2, .s1⟩, 1),
      (.cross (.crossAligned 2), 1),
      (.around ⟨.lower 2, .s2⟩, -1),
      (.around ⟨.lower 2, .s1⟩, -1),
      (.around ⟨.lower 2, .s0⟩, -1)
    ]
  else if d = (.second (.southSpoke 3) : IcosahedralDart) then
    [
      (.around ⟨.north, .s0⟩, 1),
      (.around ⟨.north, .s1⟩, 1),
      (.around ⟨.north, .s2⟩, 1),
      (.cross (.northSpoke 3), 1),
      (.around ⟨.upper 3, .s0⟩, 1),
      (.around ⟨.upper 3, .s1⟩, 1),
      (.cross (.crossAligned 3), 1),
      (.around ⟨.lower 3, .s2⟩, -1),
      (.around ⟨.lower 3, .s1⟩, -1),
      (.around ⟨.lower 3, .s0⟩, -1)
    ]
  else if d = (.second (.southSpoke 4) : IcosahedralDart) then
    [
      (.around ⟨.north, .s0⟩, 1),
      (.around ⟨.north, .s1⟩, 1),
      (.around ⟨.north, .s2⟩, 1),
      (.around ⟨.north, .s3⟩, 1),
      (.cross (.northSpoke 4), 1),
      (.around ⟨.upper 4, .s0⟩, 1),
      (.around ⟨.upper 4, .s1⟩, 1),
      (.cross (.crossAligned 4), 1),
      (.around ⟨.lower 4, .s2⟩, -1),
      (.around ⟨.lower 4, .s1⟩, -1),
      (.around ⟨.lower 4, .s0⟩, -1)
    ]
  else if d = (.second (.upperRing 0) : IcosahedralDart) then
    [
      (.around ⟨.north, .s0⟩, 1),
      (.cross (.northSpoke 1), 1),
      (.around ⟨.upper 1, .s0⟩, 1),
      (.around ⟨.upper 1, .s1⟩, 1),
      (.around ⟨.upper 1, .s2⟩, 1),
      (.around ⟨.upper 1, .s3⟩, 1)
    ]
  else if d = (.second (.upperRing 1) : IcosahedralDart) then
    [
      (.around ⟨.north, .s0⟩, 1),
      (.around ⟨.north, .s1⟩, 1),
      (.cross (.northSpoke 2), 1),
      (.around ⟨.upper 2, .s0⟩, 1),
      (.around ⟨.upper 2, .s1⟩, 1),
      (.around ⟨.upper 2, .s2⟩, 1),
      (.around ⟨.upper 2, .s3⟩, 1)
    ]
  else if d = (.second (.upperRing 2) : IcosahedralDart) then
    [
      (.around ⟨.north, .s0⟩, 1),
      (.around ⟨.north, .s1⟩, 1),
      (.around ⟨.north, .s2⟩, 1),
      (.cross (.northSpoke 3), 1),
      (.around ⟨.upper 3, .s0⟩, 1),
      (.around ⟨.upper 3, .s1⟩, 1),
      (.around ⟨.upper 3, .s2⟩, 1),
      (.around ⟨.upper 3, .s3⟩, 1)
    ]
  else if d = (.second (.upperRing 3) : IcosahedralDart) then
    [
      (.around ⟨.north, .s0⟩, 1),
      (.around ⟨.north, .s1⟩, 1),
      (.around ⟨.north, .s2⟩, 1),
      (.around ⟨.north, .s3⟩, 1),
      (.cross (.northSpoke 4), 1),
      (.around ⟨.upper 4, .s0⟩, 1),
      (.around ⟨.upper 4, .s1⟩, 1),
      (.around ⟨.upper 4, .s2⟩, 1),
      (.around ⟨.upper 4, .s3⟩, 1)
    ]
  else if d = (.second (.upperRing 4) : IcosahedralDart) then
    [
      (.cross (.northSpoke 0), 1),
      (.around ⟨.upper 0, .s0⟩, 1),
      (.around ⟨.upper 0, .s1⟩, 1),
      (.around ⟨.upper 0, .s2⟩, 1),
      (.around ⟨.upper 0, .s3⟩, 1)
    ]
  else if d = (.second (.lowerRing 0) : IcosahedralDart) then
    [
      (.around ⟨.north, .s0⟩, 1),
      (.cross (.northSpoke 1), 1),
      (.around ⟨.upper 1, .s0⟩, 1),
      (.around ⟨.upper 1, .s1⟩, 1),
      (.cross (.crossAligned 1), 1),
      (.around ⟨.lower 1, .s3⟩, 1)
    ]
  else if d = (.second (.lowerRing 1) : IcosahedralDart) then
    [
      (.around ⟨.north, .s0⟩, 1),
      (.around ⟨.north, .s1⟩, 1),
      (.cross (.northSpoke 2), 1),
      (.around ⟨.upper 2, .s0⟩, 1),
      (.around ⟨.upper 2, .s1⟩, 1),
      (.cross (.crossAligned 2), 1),
      (.around ⟨.lower 2, .s3⟩, 1)
    ]
  else if d = (.second (.lowerRing 2) : IcosahedralDart) then
    [
      (.around ⟨.north, .s0⟩, 1),
      (.around ⟨.north, .s1⟩, 1),
      (.around ⟨.north, .s2⟩, 1),
      (.cross (.northSpoke 3), 1),
      (.around ⟨.upper 3, .s0⟩, 1),
      (.around ⟨.upper 3, .s1⟩, 1),
      (.cross (.crossAligned 3), 1),
      (.around ⟨.lower 3, .s3⟩, 1)
    ]
  else if d = (.second (.lowerRing 3) : IcosahedralDart) then
    [
      (.around ⟨.north, .s0⟩, 1),
      (.around ⟨.north, .s1⟩, 1),
      (.around ⟨.north, .s2⟩, 1),
      (.around ⟨.north, .s3⟩, 1),
      (.cross (.northSpoke 4), 1),
      (.around ⟨.upper 4, .s0⟩, 1),
      (.around ⟨.upper 4, .s1⟩, 1),
      (.cross (.crossAligned 4), 1),
      (.around ⟨.lower 4, .s3⟩, 1)
    ]
  else if d = (.second (.lowerRing 4) : IcosahedralDart) then
    [
      (.cross (.northSpoke 0), 1),
      (.around ⟨.upper 0, .s0⟩, 1),
      (.around ⟨.upper 0, .s1⟩, 1),
      (.cross (.crossAligned 0), 1),
      (.around ⟨.lower 0, .s3⟩, 1)
    ]
  else if d = (.second (.crossAligned 0) : IcosahedralDart) then
    [
      (.cross (.northSpoke 0), 1),
      (.around ⟨.upper 0, .s0⟩, 1),
      (.around ⟨.upper 0, .s1⟩, 1),
      (.cross (.crossAligned 0), 1)
    ]
  else if d = (.second (.crossAligned 1) : IcosahedralDart) then
    [
      (.around ⟨.north, .s0⟩, 1),
      (.cross (.northSpoke 1), 1),
      (.around ⟨.upper 1, .s0⟩, 1),
      (.around ⟨.upper 1, .s1⟩, 1),
      (.cross (.crossAligned 1), 1)
    ]
  else if d = (.second (.crossAligned 2) : IcosahedralDart) then
    [
      (.around ⟨.north, .s0⟩, 1),
      (.around ⟨.north, .s1⟩, 1),
      (.cross (.northSpoke 2), 1),
      (.around ⟨.upper 2, .s0⟩, 1),
      (.around ⟨.upper 2, .s1⟩, 1),
      (.cross (.crossAligned 2), 1)
    ]
  else if d = (.second (.crossAligned 3) : IcosahedralDart) then
    [
      (.around ⟨.north, .s0⟩, 1),
      (.around ⟨.north, .s1⟩, 1),
      (.around ⟨.north, .s2⟩, 1),
      (.cross (.northSpoke 3), 1),
      (.around ⟨.upper 3, .s0⟩, 1),
      (.around ⟨.upper 3, .s1⟩, 1),
      (.cross (.crossAligned 3), 1)
    ]
  else if d = (.second (.crossAligned 4) : IcosahedralDart) then
    [
      (.around ⟨.north, .s0⟩, 1),
      (.around ⟨.north, .s1⟩, 1),
      (.around ⟨.north, .s2⟩, 1),
      (.around ⟨.north, .s3⟩, 1),
      (.cross (.northSpoke 4), 1),
      (.around ⟨.upper 4, .s0⟩, 1),
      (.around ⟨.upper 4, .s1⟩, 1),
      (.cross (.crossAligned 4), 1)
    ]
  else if d = (.second (.crossShifted 0) : IcosahedralDart) then
    [
      (.cross (.northSpoke 0), 1),
      (.around ⟨.upper 0, .s0⟩, 1),
      (.around ⟨.upper 0, .s1⟩, 1),
      (.cross (.crossAligned 0), 1),
      (.around ⟨.lower 0, .s2⟩, -1)
    ]
  else if d = (.second (.crossShifted 1) : IcosahedralDart) then
    [
      (.around ⟨.north, .s0⟩, 1),
      (.cross (.northSpoke 1), 1),
      (.around ⟨.upper 1, .s0⟩, 1),
      (.around ⟨.upper 1, .s1⟩, 1),
      (.cross (.crossAligned 1), 1),
      (.around ⟨.lower 1, .s2⟩, -1)
    ]
  else if d = (.second (.crossShifted 2) : IcosahedralDart) then
    [
      (.around ⟨.north, .s0⟩, 1),
      (.around ⟨.north, .s1⟩, 1),
      (.cross (.northSpoke 2), 1),
      (.around ⟨.upper 2, .s0⟩, 1),
      (.around ⟨.upper 2, .s1⟩, 1),
      (.cross (.crossAligned 2), 1),
      (.around ⟨.lower 2, .s2⟩, -1)
    ]
  else if d = (.second (.crossShifted 3) : IcosahedralDart) then
    [
      (.around ⟨.north, .s0⟩, 1),
      (.around ⟨.north, .s1⟩, 1),
      (.around ⟨.north, .s2⟩, 1),
      (.cross (.northSpoke 3), 1),
      (.around ⟨.upper 3, .s0⟩, 1),
      (.around ⟨.upper 3, .s1⟩, 1),
      (.cross (.crossAligned 3), 1),
      (.around ⟨.lower 3, .s2⟩, -1)
    ]
  else if d = (.second (.crossShifted 4) : IcosahedralDart) then
    [
      (.around ⟨.north, .s0⟩, 1),
      (.around ⟨.north, .s1⟩, 1),
      (.around ⟨.north, .s2⟩, 1),
      (.around ⟨.north, .s3⟩, 1),
      (.cross (.northSpoke 4), 1),
      (.around ⟨.upper 4, .s0⟩, 1),
      (.around ⟨.upper 4, .s1⟩, 1),
      (.cross (.crossAligned 4), 1),
      (.around ⟨.lower 4, .s2⟩, -1)
    ]
  else []

/-- Explicit oriented dual-tree cuts. The faces listed under each
of the 31 non-primal-tree edges are exactly the component of the
32-face dual tree away from the north-pentagon root, with the
original whole-face orientation sign selected to make the coefficient
of the cut edge +1. Tree edges have empty cut-filling lists. -/
def c60F16DualFaceFillList (e : TruncatedIcosahedralEdge) :
    List (TruncatedIcosahedralSeedFace × ℤ) :=
  if e = (.around ⟨.north, .s4⟩ : TruncatedIcosahedralEdge) then
    [
      (.aroundVertex (.south), 1),
      (.aroundVertex (.upper 0), 1),
      (.aroundVertex (.upper 1), 1),
      (.aroundVertex (.upper 2), 1),
      (.aroundVertex (.upper 3), 1),
      (.aroundVertex (.upper 4), 1),
      (.aroundVertex (.lower 0), 1),
      (.aroundVertex (.lower 1), 1),
      (.aroundVertex (.lower 2), 1),
      (.aroundVertex (.lower 3), 1),
      (.aroundVertex (.lower 4), 1),
      (.fromTriangle (.top 0), 1),
      (.fromTriangle (.top 1), 1),
      (.fromTriangle (.top 2), 1),
      (.fromTriangle (.top 3), 1),
      (.fromTriangle (.top 4), 1),
      (.fromTriangle (.bottom 0), 1),
      (.fromTriangle (.bottom 1), 1),
      (.fromTriangle (.bottom 2), 1),
      (.fromTriangle (.bottom 3), 1),
      (.fromTriangle (.bottom 4), 1),
      (.fromTriangle (.beltUpper 0), 1),
      (.fromTriangle (.beltUpper 1), 1),
      (.fromTriangle (.beltUpper 2), 1),
      (.fromTriangle (.beltUpper 3), 1),
      (.fromTriangle (.beltUpper 4), 1),
      (.fromTriangle (.beltLower 0), 1),
      (.fromTriangle (.beltLower 1), 1),
      (.fromTriangle (.beltLower 2), 1),
      (.fromTriangle (.beltLower 3), 1),
      (.fromTriangle (.beltLower 4), 1)
    ]
  else if e = (.around ⟨.south, .s4⟩ : TruncatedIcosahedralEdge) then
    [
      (.aroundVertex (.south), 1)
    ]
  else if e = (.around ⟨.upper 0, .s4⟩ : TruncatedIcosahedralEdge) then
    [
      (.aroundVertex (.upper 0), 1)
    ]
  else if e = (.around ⟨.upper 1, .s4⟩ : TruncatedIcosahedralEdge) then
    [
      (.aroundVertex (.upper 1), 1)
    ]
  else if e = (.around ⟨.upper 2, .s4⟩ : TruncatedIcosahedralEdge) then
    [
      (.aroundVertex (.upper 2), 1)
    ]
  else if e = (.around ⟨.upper 3, .s4⟩ : TruncatedIcosahedralEdge) then
    [
      (.aroundVertex (.upper 3), 1)
    ]
  else if e = (.around ⟨.upper 4, .s4⟩ : TruncatedIcosahedralEdge) then
    [
      (.aroundVertex (.upper 4), 1)
    ]
  else if e = (.around ⟨.lower 0, .s4⟩ : TruncatedIcosahedralEdge) then
    [
      (.aroundVertex (.lower 0), -1)
    ]
  else if e = (.around ⟨.lower 1, .s4⟩ : TruncatedIcosahedralEdge) then
    [
      (.aroundVertex (.lower 1), -1)
    ]
  else if e = (.around ⟨.lower 2, .s4⟩ : TruncatedIcosahedralEdge) then
    [
      (.aroundVertex (.lower 2), -1)
    ]
  else if e = (.around ⟨.lower 3, .s4⟩ : TruncatedIcosahedralEdge) then
    [
      (.aroundVertex (.lower 3), -1)
    ]
  else if e = (.around ⟨.lower 4, .s4⟩ : TruncatedIcosahedralEdge) then
    [
      (.aroundVertex (.lower 4), -1)
    ]
  else if e = (.cross (.southSpoke 1) : TruncatedIcosahedralEdge) then
    [
      (.aroundVertex (.upper 1), -1),
      (.aroundVertex (.lower 1), -1),
      (.fromTriangle (.top 0), -1),
      (.fromTriangle (.bottom 0), -1),
      (.fromTriangle (.beltUpper 0), -1),
      (.fromTriangle (.beltLower 0), -1)
    ]
  else if e = (.cross (.southSpoke 2) : TruncatedIcosahedralEdge) then
    [
      (.aroundVertex (.upper 1), -1),
      (.aroundVertex (.upper 2), -1),
      (.aroundVertex (.lower 1), -1),
      (.aroundVertex (.lower 2), -1),
      (.fromTriangle (.top 0), -1),
      (.fromTriangle (.top 1), -1),
      (.fromTriangle (.bottom 0), -1),
      (.fromTriangle (.bottom 1), -1),
      (.fromTriangle (.beltUpper 0), -1),
      (.fromTriangle (.beltUpper 1), -1),
      (.fromTriangle (.beltLower 0), -1),
      (.fromTriangle (.beltLower 1), -1)
    ]
  else if e = (.cross (.southSpoke 3) : TruncatedIcosahedralEdge) then
    [
      (.aroundVertex (.upper 1), -1),
      (.aroundVertex (.upper 2), -1),
      (.aroundVertex (.upper 3), -1),
      (.aroundVertex (.lower 1), -1),
      (.aroundVertex (.lower 2), -1),
      (.aroundVertex (.lower 3), -1),
      (.fromTriangle (.top 0), -1),
      (.fromTriangle (.top 1), -1),
      (.fromTriangle (.top 2), -1),
      (.fromTriangle (.bottom 0), -1),
      (.fromTriangle (.bottom 1), -1),
      (.fromTriangle (.bottom 2), -1),
      (.fromTriangle (.beltUpper 0), -1),
      (.fromTriangle (.beltUpper 1), -1),
      (.fromTriangle (.beltUpper 2), -1),
      (.fromTriangle (.beltLower 0), -1),
      (.fromTriangle (.beltLower 1), -1),
      (.fromTriangle (.beltLower 2), -1)
    ]
  else if e = (.cross (.southSpoke 4) : TruncatedIcosahedralEdge) then
    [
      (.aroundVertex (.upper 1), -1),
      (.aroundVertex (.upper 2), -1),
      (.aroundVertex (.upper 3), -1),
      (.aroundVertex (.upper 4), -1),
      (.aroundVertex (.lower 1), -1),
      (.aroundVertex (.lower 2), -1),
      (.aroundVertex (.lower 3), -1),
      (.aroundVertex (.lower 4), -1),
      (.fromTriangle (.top 0), -1),
      (.fromTriangle (.top 1), -1),
      (.fromTriangle (.top 2), -1),
      (.fromTriangle (.top 3), -1),
      (.fromTriangle (.bottom 0), -1),
      (.fromTriangle (.bottom 1), -1),
      (.fromTriangle (.bottom 2), -1),
      (.fromTriangle (.bottom 3), -1),
      (.fromTriangle (.beltUpper 0), -1),
      (.fromTriangle (.beltUpper 1), -1),
      (.fromTriangle (.beltUpper 2), -1),
      (.fromTriangle (.beltUpper 3), -1),
      (.fromTriangle (.beltLower 0), -1),
      (.fromTriangle (.beltLower 1), -1),
      (.fromTriangle (.beltLower 2), -1),
      (.fromTriangle (.beltLower 3), -1)
    ]
  else if e = (.cross (.upperRing 0) : TruncatedIcosahedralEdge) then
    [
      (.aroundVertex (.upper 1), -1),
      (.fromTriangle (.top 0), -1)
    ]
  else if e = (.cross (.upperRing 1) : TruncatedIcosahedralEdge) then
    [
      (.aroundVertex (.upper 2), -1),
      (.fromTriangle (.top 1), -1)
    ]
  else if e = (.cross (.upperRing 2) : TruncatedIcosahedralEdge) then
    [
      (.aroundVertex (.upper 3), -1),
      (.fromTriangle (.top 2), -1)
    ]
  else if e = (.cross (.upperRing 3) : TruncatedIcosahedralEdge) then
    [
      (.aroundVertex (.upper 4), -1),
      (.fromTriangle (.top 3), -1)
    ]
  else if e = (.cross (.upperRing 4) : TruncatedIcosahedralEdge) then
    [
      (.aroundVertex (.south), 1),
      (.aroundVertex (.upper 1), 1),
      (.aroundVertex (.upper 2), 1),
      (.aroundVertex (.upper 3), 1),
      (.aroundVertex (.upper 4), 1),
      (.aroundVertex (.lower 0), 1),
      (.aroundVertex (.lower 1), 1),
      (.aroundVertex (.lower 2), 1),
      (.aroundVertex (.lower 3), 1),
      (.aroundVertex (.lower 4), 1),
      (.fromTriangle (.top 0), 1),
      (.fromTriangle (.top 1), 1),
      (.fromTriangle (.top 2), 1),
      (.fromTriangle (.top 3), 1),
      (.fromTriangle (.bottom 0), 1),
      (.fromTriangle (.bottom 1), 1),
      (.fromTriangle (.bottom 2), 1),
      (.fromTriangle (.bottom 3), 1),
      (.fromTriangle (.bottom 4), 1),
      (.fromTriangle (.beltUpper 0), 1),
      (.fromTriangle (.beltUpper 1), 1),
      (.fromTriangle (.beltUpper 2), 1),
      (.fromTriangle (.beltUpper 3), 1),
      (.fromTriangle (.beltUpper 4), 1),
      (.fromTriangle (.beltLower 0), 1),
      (.fromTriangle (.beltLower 1), 1),
      (.fromTriangle (.beltLower 2), 1),
      (.fromTriangle (.beltLower 3), 1),
      (.fromTriangle (.beltLower 4), 1)
    ]
  else if e = (.cross (.lowerRing 0) : TruncatedIcosahedralEdge) then
    [
      (.aroundVertex (.upper 1), -1),
      (.fromTriangle (.top 0), -1),
      (.fromTriangle (.beltUpper 0), -1),
      (.fromTriangle (.beltLower 0), -1)
    ]
  else if e = (.cross (.lowerRing 1) : TruncatedIcosahedralEdge) then
    [
      (.aroundVertex (.upper 2), -1),
      (.fromTriangle (.top 1), -1),
      (.fromTriangle (.beltUpper 1), -1),
      (.fromTriangle (.beltLower 1), -1)
    ]
  else if e = (.cross (.lowerRing 2) : TruncatedIcosahedralEdge) then
    [
      (.aroundVertex (.upper 3), -1),
      (.fromTriangle (.top 2), -1),
      (.fromTriangle (.beltUpper 2), -1),
      (.fromTriangle (.beltLower 2), -1)
    ]
  else if e = (.cross (.lowerRing 3) : TruncatedIcosahedralEdge) then
    [
      (.aroundVertex (.upper 4), -1),
      (.fromTriangle (.top 3), -1),
      (.fromTriangle (.beltUpper 3), -1),
      (.fromTriangle (.beltLower 3), -1)
    ]
  else if e = (.cross (.lowerRing 4) : TruncatedIcosahedralEdge) then
    [
      (.aroundVertex (.south), 1),
      (.aroundVertex (.upper 1), 1),
      (.aroundVertex (.upper 2), 1),
      (.aroundVertex (.upper 3), 1),
      (.aroundVertex (.upper 4), 1),
      (.aroundVertex (.lower 0), 1),
      (.aroundVertex (.lower 1), 1),
      (.aroundVertex (.lower 2), 1),
      (.aroundVertex (.lower 3), 1),
      (.aroundVertex (.lower 4), 1),
      (.fromTriangle (.top 0), 1),
      (.fromTriangle (.top 1), 1),
      (.fromTriangle (.top 2), 1),
      (.fromTriangle (.top 3), 1),
      (.fromTriangle (.bottom 0), 1),
      (.fromTriangle (.bottom 1), 1),
      (.fromTriangle (.bottom 2), 1),
      (.fromTriangle (.bottom 3), 1),
      (.fromTriangle (.bottom 4), 1),
      (.fromTriangle (.beltUpper 0), 1),
      (.fromTriangle (.beltUpper 1), 1),
      (.fromTriangle (.beltUpper 2), 1),
      (.fromTriangle (.beltUpper 3), 1),
      (.fromTriangle (.beltLower 0), 1),
      (.fromTriangle (.beltLower 1), 1),
      (.fromTriangle (.beltLower 2), 1),
      (.fromTriangle (.beltLower 3), 1)
    ]
  else if e = (.cross (.crossShifted 0) : TruncatedIcosahedralEdge) then
    [
      (.aroundVertex (.upper 1), 1),
      (.fromTriangle (.top 0), 1),
      (.fromTriangle (.beltUpper 0), 1)
    ]
  else if e = (.cross (.crossShifted 1) : TruncatedIcosahedralEdge) then
    [
      (.aroundVertex (.upper 2), 1),
      (.fromTriangle (.top 1), 1),
      (.fromTriangle (.beltUpper 1), 1)
    ]
  else if e = (.cross (.crossShifted 2) : TruncatedIcosahedralEdge) then
    [
      (.aroundVertex (.upper 3), 1),
      (.fromTriangle (.top 2), 1),
      (.fromTriangle (.beltUpper 2), 1)
    ]
  else if e = (.cross (.crossShifted 3) : TruncatedIcosahedralEdge) then
    [
      (.aroundVertex (.upper 4), 1),
      (.fromTriangle (.top 3), 1),
      (.fromTriangle (.beltUpper 3), 1)
    ]
  else if e = (.cross (.crossShifted 4) : TruncatedIcosahedralEdge) then
    [
      (.aroundVertex (.south), -1),
      (.aroundVertex (.upper 1), -1),
      (.aroundVertex (.upper 2), -1),
      (.aroundVertex (.upper 3), -1),
      (.aroundVertex (.upper 4), -1),
      (.aroundVertex (.lower 0), -1),
      (.aroundVertex (.lower 1), -1),
      (.aroundVertex (.lower 2), -1),
      (.aroundVertex (.lower 3), -1),
      (.aroundVertex (.lower 4), -1),
      (.fromTriangle (.top 0), -1),
      (.fromTriangle (.top 1), -1),
      (.fromTriangle (.top 2), -1),
      (.fromTriangle (.top 3), -1),
      (.fromTriangle (.bottom 0), -1),
      (.fromTriangle (.bottom 1), -1),
      (.fromTriangle (.bottom 2), -1),
      (.fromTriangle (.bottom 3), -1),
      (.fromTriangle (.bottom 4), -1),
      (.fromTriangle (.beltUpper 0), -1),
      (.fromTriangle (.beltUpper 1), -1),
      (.fromTriangle (.beltUpper 2), -1),
      (.fromTriangle (.beltUpper 3), -1),
      (.fromTriangle (.beltLower 0), -1),
      (.fromTriangle (.beltLower 1), -1),
      (.fromTriangle (.beltLower 2), -1),
      (.fromTriangle (.beltLower 3), -1),
      (.fromTriangle (.beltLower 4), -1)
    ]
  else []

/-- Coefficient of one original edge in a genuine signed primal path. -/
def c60F16PrimalPathCoefficient
    (d : IcosahedralDart) (e : TruncatedIcosahedralEdge) : ℤ :=
  ((c60F16PrimalPathList d).map
    (fun p => if p.1 = e then p.2 else (0 : ℤ))).sum

/-- Coefficient of one original edge in the signed 32-face
combination filling the dual-tree cut associated with another edge. -/
def c60F16DualFaceFillCoefficient
    (e t : TruncatedIcosahedralEdge) : ℤ :=
  ((c60F16DualFaceFillList e).map
    (fun p => p.2 * c60IntegerFaceEdgeCoefficient p.1 t)).sum

/-- THE finite, kernel-checked 90×90 integral incidence certificate:
every original signed C60 edge is a face-filling boundary plus
the tree-path lift of its vertex boundary. -/
theorem c60F16FiniteContractingCertificate :
    ∀ e t : TruncatedIcosahedralEdge,
      c60F16DualFaceFillCoefficient e t +
        (c60F16PrimalPathCoefficient
            (truncatedIcosahedralEdgeEndpoints e).2 t -
          c60F16PrimalPathCoefficient
            (truncatedIcosahedralEdgeEndpoints e).1 t) =
          (if e = t then (1 : ℤ) else 0) := by
  decide

/-- A signed tree path as an actual integral one-chain. -/
def c60F16PrimalPath (d : IcosahedralDart) : C60IntegralOneChains :=
  ((c60F16PrimalPathList d).map
    (fun p => (Finsupp.single p.1 p.2 : C60IntegralOneChains))).sum

/-- A signed dual cut filling as an actual integral two-chain. -/
def c60F16FaceFill (e : TruncatedIcosahedralEdge) : C60IntegralTwoChains :=
  ((c60F16DualFaceFillList e).map
    (fun p => (Finsupp.single p.1 p.2 : C60IntegralTwoChains))).sum

/-- Z-linear primal root-path lift on arbitrary genuine zero chains. -/
def c60F16PrimalPathLift :
    C60IntegralZeroChains →ₗ[ℤ] C60IntegralOneChains :=
  Finsupp.linearCombination ℤ c60F16PrimalPath

/-- Z-linear dual cut-filling lift on arbitrary genuine one chains. -/
def c60F16FaceFillLift :
    C60IntegralOneChains →ₗ[ℤ] C60IntegralTwoChains :=
  Finsupp.linearCombination ℤ c60F16FaceFill

theorem c60F16PrimalPathLift_single
    (d : IcosahedralDart) (z : ℤ) :
    c60F16PrimalPathLift (Finsupp.single d z) =
      z • c60F16PrimalPath d := by
  simp [c60F16PrimalPathLift]

theorem c60F16FaceFillLift_single
    (e : TruncatedIcosahedralEdge) (z : ℤ) :
    c60F16FaceFillLift (Finsupp.single e z) =
      z • c60F16FaceFill e := by
  simp [c60F16FaceFillLift]

theorem c60F16PrimalPath_apply (d : IcosahedralDart)
    (e : TruncatedIcosahedralEdge) :
    c60F16PrimalPath d e = c60F16PrimalPathCoefficient d e := by
  exact c60SignedEdgeList_chain_apply _ e

/-- One genuine physical face generator, with arbitrary integer
coefficient, has its original signed edge-incidence boundary. -/
theorem c60F16FaceBasisBoundary_apply
    (f : TruncatedIcosahedralSeedFace) (z : ℤ)
    (e : TruncatedIcosahedralEdge) :
    (c60IntegralBoundaryTwo (Finsupp.single f z)) e =
      z * c60IntegerFaceEdgeCoefficient f e := by
  simp [c60IntegralBoundaryTwo, c60IntegerFaceBoundaryChain]

/-- The linear boundary of any ordered, signed genuine face list
is exactly the sum of its original physical incidence coefficients. -/
theorem c60F16FaceListBoundary_apply
    (l : List (TruncatedIcosahedralSeedFace × ℤ))
    (e : TruncatedIcosahedralEdge) :
    (c60IntegralBoundaryTwo
      ((l.map (fun p =>
        (Finsupp.single p.1 p.2 : C60IntegralTwoChains))).sum)) e =
      (l.map (fun p =>
        p.2 * c60IntegerFaceEdgeCoefficient p.1 e)).sum := by
  induction l with
  | nil => simp
  | cons p ps ih =>
      simp only [List.map_cons, List.sum_cons, map_add, Finsupp.add_apply]
      rw [ih, c60F16FaceBasisBoundary_apply]

theorem c60F16FaceFill_boundary_apply
    (e t : TruncatedIcosahedralEdge) :
    (c60IntegralBoundaryTwo (c60F16FaceFill e)) t =
      c60F16DualFaceFillCoefficient e t := by
  exact c60F16FaceListBoundary_apply _ t

theorem c60F16PrimalPathLift_edgeBoundary_apply
    (e t : TruncatedIcosahedralEdge) :
    (c60F16PrimalPathLift (c60IntegralEdgeBoundaryChain e)) t =
      c60F16PrimalPathCoefficient
        (truncatedIcosahedralEdgeEndpoints e).2 t -
      c60F16PrimalPathCoefficient
        (truncatedIcosahedralEdgeEndpoints e).1 t := by
  simp only [c60IntegralEdgeBoundaryChain, map_sub,
    Finsupp.sub_apply]
  rw [c60F16PrimalPathLift_single, c60F16PrimalPathLift_single]
  simp only [one_smul, c60F16PrimalPath_apply]

/-- Literal edgewise chain contraction, promoted from the
original 90×90 kernel-checkable integer coefficient certificate. -/
theorem c60F16BasisContractingIdentity (e : TruncatedIcosahedralEdge) :
    c60IntegralBoundaryTwo (c60F16FaceFill e) +
      c60F16PrimalPathLift (c60IntegralEdgeBoundaryChain e) =
        Finsupp.single e (1 : ℤ) := by
  apply Finsupp.ext
  intro t
  rw [Finsupp.add_apply,
    c60F16FaceFill_boundary_apply,
    c60F16PrimalPathLift_edgeBoundary_apply]
  simpa only [Finsupp.single_apply] using
    c60F16FiniteContractingCertificate e t

/-- THE full original integral C60 degree-one contracting identity:
d₂ Q + P d₁ = id on ALL actual 90-edge signed 1-chains. -/
theorem c60F16ContractingIdentity :
    c60IntegralBoundaryTwo.comp c60F16FaceFillLift +
      c60F16PrimalPathLift.comp c60IntegralBoundaryOne =
        LinearMap.id := by
  apply Finsupp.lhom_ext
  intro e z
  change c60IntegralBoundaryTwo
      (c60F16FaceFillLift (Finsupp.single e z)) +
    c60F16PrimalPathLift
      (c60IntegralBoundaryOne (Finsupp.single e z)) =
        Finsupp.single e z
  rw [c60F16FaceFillLift_single,
    c60IntegralBoundaryOne_singleEdge, map_smul, map_smul,
    ← smul_add, c60F16BasisContractingIdentity]
  simp

/-- Every physical integer one-cycle is an integer two-boundary
from the ORIGINAL 32 pentagons and hexagons. -/
theorem c60IntegralBoundaryOne_kernel_le_boundaryTwo_range :
    LinearMap.ker c60IntegralBoundaryOne ≤
      LinearMap.range c60IntegralBoundaryTwo := by
  intro x hx
  have hz : c60IntegralBoundaryOne x = 0 := hx
  have h := LinearMap.congr_fun c60F16ContractingIdentity x
  simp only [LinearMap.add_apply, LinearMap.comp_apply,
    LinearMap.id_apply] at h
  rw [hz, map_zero, add_zero] at h
  exact ⟨c60F16FaceFillLift x, h⟩

/-- The actual 32→90→60 cellular integer chain complex is EXACT
in degree one, with no replacement abstract sphere assumption. -/
theorem c60IntegralH1_range_boundaryTwo_eq_kernel_boundaryOne :
    LinearMap.range c60IntegralBoundaryTwo =
      LinearMap.ker c60IntegralBoundaryOne := by
  apply le_antisymm
  · exact c60IntegralBoundaryTwo_range_le_boundaryOne_kernel
  · exact c60IntegralBoundaryOne_kernel_le_boundaryTwo_range

/-- Actual native Mathlib chain complex is exact at degree one. -/
theorem c60NativeChainComplex_exactAt_one :
    c60NativeIntegralCellularComplex.ExactAt 1 := by
  apply (c60NativeIntegralCellularComplex.exactAt_iff'
    (i := 2) (j := 1) (k := 0) (by simp) (by simp)).mpr
  apply (ShortComplex.moduleCat_exact_iff_range_eq_ker
    (c60NativeIntegralCellularComplex.sc' 2 1 0)).mpr
  change LinearMap.range (c60NativeIntegralCellularComplex.d 2 1).hom =
    LinearMap.ker (c60NativeIntegralCellularComplex.d 1 0).hom
  rw [c60NativeIntegralCellularComplex_d21,
    c60NativeIntegralCellularComplex_d10]
  exact c60IntegralH1_range_boundaryTwo_eq_kernel_boundaryOne

/-- Original C60 integral first homology VANISHES in Mathlib's
own HomologicalComplex.homology object. -/
theorem c60NativeH1_isZero :
    IsZero (c60NativeIntegralCellularComplex.homology 1) :=
  (c60NativeIntegralCellularComplex.exactAt_iff_isZero_homology 1).mp
    c60NativeChainComplex_exactAt_one

#print axioms c60F16FiniteContractingCertificate
#print axioms c60F16PrimalPath_apply
#print axioms c60F16FaceBasisBoundary_apply
#print axioms c60F16FaceListBoundary_apply
#print axioms c60F16BasisContractingIdentity
#print axioms c60F16ContractingIdentity
#print axioms c60IntegralBoundaryOne_kernel_le_boundaryTwo_range
#print axioms c60IntegralH1_range_boundaryTwo_eq_kernel_boundaryOne
#print axioms c60NativeChainComplex_exactAt_one
#print axioms c60NativeH1_isZero

end
end KUOS.DependentOriginationGrayC60NativeH1ContractingHomotopyV5_164
