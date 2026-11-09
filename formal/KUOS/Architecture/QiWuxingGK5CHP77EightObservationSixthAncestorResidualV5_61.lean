import KUOS.Architecture.QiWuxingGK5CHP77AncestorTowerBridgeSixthWitnessV5_60

/-!
Qi v5.61 — a fully verified EIGHT-observation residual in the
independent seven-constructor v5.50 raw-congruence quotient.

Reuse the genuinely typed v5.60 second shifted suffix pair. Its
C0..C5 counts coincide and C6 differs by exactly 2. Here we
add the missing proof of the complete ordered raw trace, adjacent
reverse count, and true top reverse flag. Together with the
five v5.60 pointwise tower/old-count bridges, this CERTIFIES
equality of all eight previously independent quotient observables:
trace, reverse total, adjacency, top flag, pair, triple, quadruple,
quintuple — and C6 still separates the actual new quotient classes.

Avoid unfolding the giant v5.58 suffix terms inside observation
proofs. First establish arbitrary typed raw A/B shift equations;
then use the certified v5.58 suffix top tags, the genuine v5.60
C0..C5 equality, and contextual right concatenation compatibility.

No original 18D/19D proof values, original 16D/17D boundaries,
old selected19 or new v5.50 seven-generator comparisons, old import,
public root, pinned Lean/mathlib, or protected PR #1558 changed.
No all-n witness family, nine-observation completeness, arbitrary
heterogeneous fiber inhabitance, 20D gluing, or authority claimed.
append-only / tighten-only / overwrite-forbidden / same-root.
-/

set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uSix

namespace KUOS.Architecture.WuxingPentagonUnified
namespace FivefoldP77FiniteRefinement
namespace PentagonAdjoinedSixCell

variable {W : Type uSix}

section ExactFiber

variable (l r : W)
variable {F G : FramedEleven W l r}
variable {P Q : SelectedUnitalCompositionTwelve W l r F G}
variable {C D : SelectedMixedInterchangerThirteen W l r P Q}
variable {V X : SelectedMixedNaturalityFourteen W l r C D}
variable {T U : SelectedContextualFifteen W l r V X}
variable {H K : SelectedContextualSixteen W l r T U}
variable {J N : SelectedContextualSeventeen W l r H K}

/-- Exact eight raw observations are a Prop on real values in the
SAME original dependent 17D endpoint fiber; no numerical surrogate
is substituted for the actual raw values or their quotient. -/
def selectedRawEightSignature
    (X Y : SelectedContextualEighteen W l r J N) : Prop :=
  selectedContextEighteenTrace l r X = selectedContextEighteenTrace l r Y ∧
    selectedContextEighteenReverseCount l r X = selectedContextEighteenReverseCount l r Y ∧
    selectedContextEighteenAdjacentReverseCount l r X = selectedContextEighteenAdjacentReverseCount l r Y ∧
    selectedContextEighteenTopReverseFlag l r X = selectedContextEighteenTopReverseFlag l r Y ∧
    selectedContextEighteenReverseAncestryCount l r X = selectedContextEighteenReverseAncestryCount l r Y ∧
    selectedContextEighteenReverseAncestorTripleCount l r X = selectedContextEighteenReverseAncestorTripleCount l r Y ∧
    selectedContextEighteenReverseAncestorQuadrupleCount l r X = selectedContextEighteenReverseAncestorQuadrupleCount l r Y ∧
    selectedContextEighteenReverseAncestorQuintupleCount l r X = selectedContextEighteenReverseAncestorQuintupleCount l r Y

/-- Any two ACTUAL typed raw values agreeing in all eight existing
invariants have equal actual eight-component NEW quotient observations. -/
theorem selectedRawEightSignature_toObservation
    (X Y : SelectedContextualEighteen W l r J N)
    (h : selectedRawEightSignature l r X Y) :
    selectedRawCongruentSevenQuintupleObservation l r J N
        (selectedRawCongruentClass l r X) =
      selectedRawCongruentSevenQuintupleObservation l r J N
        (selectedRawCongruentClass l r Y) := by
  rcases h with ⟨hTrace, hReverse, hAdjacent, hTop, hPair, hTriple, hQuadruple, hQuintuple⟩
  apply Prod.ext
  · apply Prod.ext
    · apply Prod.ext
      · apply Prod.ext
        · apply Prod.ext
          · apply Prod.ext
            · apply Prod.ext
              · change selectedContextEighteenTrace l r X =
                  selectedContextEighteenTrace l r Y
                exact hTrace
              · change selectedContextEighteenReverseCount l r X =
                  selectedContextEighteenReverseCount l r Y
                exact hReverse
            · change selectedContextEighteenAdjacentReverseCount l r X =
                selectedContextEighteenAdjacentReverseCount l r Y
              exact hAdjacent
          · change selectedContextEighteenTopReverseFlag l r X =
              selectedContextEighteenTopReverseFlag l r Y
            exact hTop
        · change selectedContextEighteenReverseAncestryCount l r X =
            selectedContextEighteenReverseAncestryCount l r Y
          exact hPair
      · change selectedContextEighteenReverseAncestorTripleCount l r X =
          selectedContextEighteenReverseAncestorTripleCount l r Y
        exact hTriple
    · change selectedContextEighteenReverseAncestorQuadrupleCount l r X =
        selectedContextEighteenReverseAncestorQuadrupleCount l r Y
      exact hQuadruple
  · change selectedContextEighteenReverseAncestorQuintupleCount l r X =
      selectedContextEighteenReverseAncestorQuintupleCount l r Y
    exact hQuintuple

/-- Reversing A instead of B changes neither their ordered
exterior raw 17D trace nor its order. This holds for ANY genuine
same-endpoint typed A/B, not only the specific large suffixes. -/
theorem selectedAncestorShift_traceEq
    (N : SelectedContextualSeventeen W l r H K)
    (A B : SelectedContextualEighteen W l r N N) :
    selectedContextEighteenTrace l r (selectedAncestorShiftLeft l r N A B) =
      selectedContextEighteenTrace l r (selectedAncestorShiftRight l r N A B) := by
  rfl

/-- The raw top-reverse flag of a genuine chain is 0, regardless
of its (possibly complicated) typed raw operands. -/
theorem selectedAncestorShift_bothTopZero
    (N : SelectedContextualSeventeen W l r H K)
    (A B : SelectedContextualEighteen W l r N N) :
    selectedContextEighteenTopReverseFlag l r
        (selectedAncestorShiftLeft l r N A B) = 0 ∧
      selectedContextEighteenTopReverseFlag l r
        (selectedAncestorShiftRight l r N A B) = 0 := by
  exact ⟨rfl, rfl⟩

/-- Adjacent raw reversals are preserved by opposite reversal
placement exactly when the SOURCE top reverse flags coincide.
This is a LOCAL compatibility assumption, not a universal claim. -/
theorem selectedAncestorShift_adjacentIfTopEq
    (N : SelectedContextualSeventeen W l r H K)
    (A B : SelectedContextualEighteen W l r N N)
    (h : selectedContextEighteenTopReverseFlag l r A =
      selectedContextEighteenTopReverseFlag l r B) :
    selectedContextEighteenAdjacentReverseCount l r
        (selectedAncestorShiftLeft l r N A B) =
      selectedContextEighteenAdjacentReverseCount l r
        (selectedAncestorShiftRight l r N A B) := by
  change
    (selectedContextEighteenAdjacentReverseCount l r A +
      selectedContextEighteenTopReverseFlag l r A) +
        selectedContextEighteenAdjacentReverseCount l r B =
      selectedContextEighteenAdjacentReverseCount l r A +
        (selectedContextEighteenAdjacentReverseCount l r B +
          selectedContextEighteenTopReverseFlag l r B)
  omega

/-- The existing v5.58 source suffixes have true top tag chain (5),
not reverse (4). Their flags are BOTH zero, without inspecting
their deeply nested constituent Type-valued proofs. -/
theorem selectedSevenQuintuple_sourcesTopZero
    (N : SelectedContextualSeventeen W l r H K) :
    selectedContextEighteenTopReverseFlag l r
        (selectedSevenQuintupleSuffixLeft l r N) = 0 ∧
      selectedContextEighteenTopReverseFlag l r
        (selectedSevenQuintupleSuffixRight l r N) = 0 := by
  exact ⟨rfl, rfl⟩

/-- All EIGHT certified raw invariants actually agree on the
v5.60 N-to-N sixth-residual loop pair. The five ancestor
observations use the v5.60 typed pointwise bridges, not an
unjustified identification of two independently defined quotients. -/
theorem selectedEightTowerShift_eightSignature
    (N : SelectedContextualSeventeen W l r H K) :
    selectedRawEightSignature l r
      (selectedEightTowerShiftLeft l r N)
      (selectedEightTowerShiftRight l r N) := by
  let A : SelectedContextualEighteen W l r N N :=
    selectedSevenQuintupleSuffixLeft l r N
  let B : SelectedContextualEighteen W l r N N :=
    selectedSevenQuintupleSuffixRight l r N
  let X : SelectedContextualEighteen W l r N N :=
    selectedEightTowerShiftLeft l r N
  let Y : SelectedContextualEighteen W l r N N :=
    selectedEightTowerShiftRight l r N
  have hprefix : ∀ k ≤ 5,
      selectedAncestorTowerCount l r k X =
        selectedAncestorTowerCount l r k Y :=
    (selectedEightTowerShift_residualGate l r N).1
  have hAB : selectedContextEighteenTopReverseFlag l r A =
      selectedContextEighteenTopReverseFlag l r B := by
    rcases selectedSevenQuintuple_sourcesTopZero l r N with ⟨hA, hB⟩
    exact hA.trans hB.symm
  have hTrace : selectedContextEighteenTrace l r X =
      selectedContextEighteenTrace l r Y :=
    selectedAncestorShift_traceEq l r N A B
  have hAdjacent : selectedContextEighteenAdjacentReverseCount l r X =
      selectedContextEighteenAdjacentReverseCount l r Y :=
    selectedAncestorShift_adjacentIfTopEq l r N A B hAB
  have hTop : selectedContextEighteenTopReverseFlag l r X =
      selectedContextEighteenTopReverseFlag l r Y := by
    rcases selectedAncestorShift_bothTopZero l r N A B with ⟨hx, hy⟩
    exact hx.trans hy.symm
  have hReverse : selectedContextEighteenReverseCount l r X =
      selectedContextEighteenReverseCount l r Y :=
    (selectedAncestorTower_eqReverseCount l r X).symm.trans
      ((hprefix 1 (by omega)).trans (selectedAncestorTower_eqReverseCount l r Y))
  have hPair : selectedContextEighteenReverseAncestryCount l r X =
      selectedContextEighteenReverseAncestryCount l r Y :=
    (selectedAncestorTower_eqAncestryCount l r X).symm.trans
      ((hprefix 2 (by omega)).trans (selectedAncestorTower_eqAncestryCount l r Y))
  have hTriple : selectedContextEighteenReverseAncestorTripleCount l r X =
      selectedContextEighteenReverseAncestorTripleCount l r Y :=
    (selectedAncestorTower_eqAncestorTripleCount l r X).symm.trans
      ((hprefix 3 (by omega)).trans (selectedAncestorTower_eqAncestorTripleCount l r Y))
  have hQuadruple : selectedContextEighteenReverseAncestorQuadrupleCount l r X =
      selectedContextEighteenReverseAncestorQuadrupleCount l r Y :=
    (selectedAncestorTower_eqAncestorQuadrupleCount l r X).symm.trans
      ((hprefix 4 (by omega)).trans (selectedAncestorTower_eqAncestorQuadrupleCount l r Y))
  have hQuintuple : selectedContextEighteenReverseAncestorQuintupleCount l r X =
      selectedContextEighteenReverseAncestorQuintupleCount l r Y :=
    (selectedAncestorTower_eqAncestorQuintupleCount l r X).symm.trans
      ((hprefix 5 (by omega)).trans (selectedAncestorTower_eqAncestorQuintupleCount l r Y))
  exact ⟨hTrace, hReverse, hAdjacent, hTop,
    hPair, hTriple, hQuadruple, hQuintuple⟩

/-- Appending actual N-to-N raw suffixes to an ACTUAL M:J-to-N
preserves equality of the entire eight-component raw signature.
For the top flag, both resulting raw constructors are chains. -/
theorem selectedRawEightSignature_rightChain
    (M : SelectedContextualEighteen W l r J N)
    (A B : SelectedContextualEighteen W l r N N)
    (h : selectedRawEightSignature l r A B) :
    selectedRawEightSignature l r (.chain M A) (.chain M B) := by
  rcases h with
    ⟨hTrace, hReverse, hAdjacent, hTop, hPair, hTriple, hQuadruple, hQuintuple⟩
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩
  · change (selectedContextEighteenTrace l r M ++ selectedContextEighteenTrace l r A) =
      (selectedContextEighteenTrace l r M ++ selectedContextEighteenTrace l r B)
    exact congrArg (fun x => selectedContextEighteenTrace l r M ++ x) hTrace
  · change (selectedContextEighteenReverseCount l r M + selectedContextEighteenReverseCount l r A) =
      (selectedContextEighteenReverseCount l r M + selectedContextEighteenReverseCount l r B)
    exact congrArg (fun x => selectedContextEighteenReverseCount l r M + x) hReverse
  · change (selectedContextEighteenAdjacentReverseCount l r M + selectedContextEighteenAdjacentReverseCount l r A) =
      (selectedContextEighteenAdjacentReverseCount l r M + selectedContextEighteenAdjacentReverseCount l r B)
    exact congrArg (fun x => selectedContextEighteenAdjacentReverseCount l r M + x) hAdjacent
  · change (0 : Nat) = 0
    rfl
  · change (selectedContextEighteenReverseAncestryCount l r M + selectedContextEighteenReverseAncestryCount l r A) =
      (selectedContextEighteenReverseAncestryCount l r M + selectedContextEighteenReverseAncestryCount l r B)
    exact congrArg (fun x => selectedContextEighteenReverseAncestryCount l r M + x) hPair
  · change (selectedContextEighteenReverseAncestorTripleCount l r M + selectedContextEighteenReverseAncestorTripleCount l r A) =
      (selectedContextEighteenReverseAncestorTripleCount l r M + selectedContextEighteenReverseAncestorTripleCount l r B)
    exact congrArg (fun x => selectedContextEighteenReverseAncestorTripleCount l r M + x) hTriple
  · change (selectedContextEighteenReverseAncestorQuadrupleCount l r M + selectedContextEighteenReverseAncestorQuadrupleCount l r A) =
      (selectedContextEighteenReverseAncestorQuadrupleCount l r M + selectedContextEighteenReverseAncestorQuadrupleCount l r B)
    exact congrArg (fun x => selectedContextEighteenReverseAncestorQuadrupleCount l r M + x) hQuadruple
  · change (selectedContextEighteenReverseAncestorQuintupleCount l r M + selectedContextEighteenReverseAncestorQuintupleCount l r A) =
      (selectedContextEighteenReverseAncestorQuintupleCount l r M + selectedContextEighteenReverseAncestorQuintupleCount l r B)
    exact congrArg (fun x => selectedContextEighteenReverseAncestorQuintupleCount l r M + x) hQuintuple

/-- The same equality of all eight raw values transports to ANY
supplied original M:J-to-N exact dependent fiber. -/
theorem selectedEightTowerFiber_eightSignature
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawEightSignature l r
      (selectedEightTowerFiberLeft l r M)
      (selectedEightTowerFiberRight l r M) :=
  selectedRawEightSignature_rightChain l r M
    (selectedEightTowerShiftLeft l r N)
    (selectedEightTowerShiftRight l r N)
    (selectedEightTowerShift_eightSignature l r N)

/-- All EIGHT actual independent quotient observables coincide
on the true v5.60 typed pair in every actually inhabited fiber. -/
theorem selectedEightTowerFiber_eightObservedEq
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentSevenQuintupleObservation l r J N
        (selectedRawCongruentClass l r (selectedEightTowerFiberLeft l r M)) =
      selectedRawCongruentSevenQuintupleObservation l r J N
        (selectedRawCongruentClass l r (selectedEightTowerFiberRight l r M)) :=
  selectedRawEightSignature_toObservation l r
    (selectedEightTowerFiberLeft l r M)
    (selectedEightTowerFiberRight l r M)
    (selectedEightTowerFiber_eightSignature l r M)

/-- Eight quotient observations are NOT injective in any actually
supplied original J-to-N fiber. The genuine class inequality is
the already-certified v5.60 C6 distinction. -/
theorem selectedRawCongruentEight_notInjective
    (M : SelectedContextualEighteen W l r J N) :
    ¬ Function.Injective
      (selectedRawCongruentSevenQuintupleObservation l r J N) := by
  intro hinj
  exact (selectedEightTowerFiber_classDistinct l r M)
    (hinj (selectedEightTowerFiber_eightObservedEq l r M))

/-- Eight finite measurements cannot reconstruct every new quotient
class in a fiber equipped with one real old18 witness M. -/
theorem selectedRawCongruentEight_noDecoder
    (M : SelectedContextualEighteen W l r J N) :
    ¬ ∃ decode :
        (((((((List Bool × Nat) × Nat) × Nat) × Nat) × Nat) × Nat) × Nat) →
          Quotient (selectedRawCongruentSetoid l r J N),
      ∀ q : Quotient (selectedRawCongruentSetoid l r J N),
        decode (selectedRawCongruentSevenQuintupleObservation l r J N q) = q := by
  rintro ⟨decode, h⟩
  apply selectedRawCongruentEight_notInjective l r M
  intro a b hab
  calc
    a = decode (selectedRawCongruentSevenQuintupleObservation l r J N a) :=
      (h a).symm
    _ = decode (selectedRawCongruentSevenQuintupleObservation l r J N b) :=
      congrArg decode hab
    _ = b := h b

/-- In particular, the newly certified C6 cannot be decoded from
the eight observations, even if the user supplied the exact
underlying J-to-N fiber and its genuine original witness. -/
theorem selectedRawCongruentEight_noSixthDecoder
    (M : SelectedContextualEighteen W l r J N) :
    ¬ ∃ decodeSix :
        (((((((List Bool × Nat) × Nat) × Nat) × Nat) × Nat) × Nat) × Nat) → Nat,
      ∀ q : Quotient (selectedRawCongruentSetoid l r J N),
        decodeSix (selectedRawCongruentSevenQuintupleObservation l r J N q) =
          selectedAncestorTowerOnNewQuotient l r 6 J N q := by
  rintro ⟨decodeSix, h⟩
  have hc :
      selectedAncestorTowerOnNewQuotient l r 6 J N
          (selectedRawCongruentClass l r (selectedEightTowerFiberLeft l r M)) =
        selectedAncestorTowerOnNewQuotient l r 6 J N
          (selectedRawCongruentClass l r (selectedEightTowerFiberRight l r M)) := by
    calc
      _ = decodeSix (selectedRawCongruentSevenQuintupleObservation l r J N
            (selectedRawCongruentClass l r (selectedEightTowerFiberLeft l r M))) :=
        (h _).symm
      _ = decodeSix (selectedRawCongruentSevenQuintupleObservation l r J N
            (selectedRawCongruentClass l r (selectedEightTowerFiberRight l r M))) :=
        congrArg decodeSix (selectedEightTowerFiber_eightObservedEq l r M)
      _ = _ := h _
  change selectedAncestorTowerCount l r 6 (selectedEightTowerFiberLeft l r M) =
    selectedAncestorTowerCount l r 6 (selectedEightTowerFiberRight l r M) at hc
  rw [selectedEightTowerFiber_sixthGap l r M] at hc
  omega

/-- Every specified 17D J has a genuine strict J→J proof; thus the
eight-observation residual is unconditional FOR THAT ENDOMORPHISM
fiber, without asserting arbitrary heterogeneous fiber inhabitance. -/
theorem selectedRawCongruentEight_endomorphismNotInjective
    (J : SelectedContextualSeventeen W l r H K) :
    ¬ Function.Injective
      (selectedRawCongruentSevenQuintupleObservation l r J J) :=
  selectedRawCongruentEight_notInjective l r
    (SelectedContextualEighteen.strict J)

/-- Ninth observable: an explicitly separate, independently certified
C6 quotient lift. No completeness, injectivity, or full reconstruction
of the new NINE-component observer is claimed. -/
def selectedRawCongruentNineObservation
    (J N : SelectedContextualSeventeen W l r H K) :
    Quotient (selectedRawCongruentSetoid l r J N) →
      ((((((((List Bool × Nat) × Nat) × Nat) × Nat) × Nat) × Nat) × Nat) × Nat) :=
  fun q =>
    (selectedRawCongruentSevenQuintupleObservation l r J N q,
      selectedAncestorTowerOnNewQuotient l r 6 J N q)

/-- The ninth C6 coordinate separates this explicitly constructed
same-fiber pair: eighth-observation collision does NOT imply ninth
completeness of the global quotient. -/
theorem selectedRawCongruentNine_sixthDistinguished
    (M : SelectedContextualEighteen W l r J N) :
    selectedRawCongruentNineObservation l r J N
        (selectedRawCongruentClass l r (selectedEightTowerFiberLeft l r M)) ≠
      selectedRawCongruentNineObservation l r J N
        (selectedRawCongruentClass l r (selectedEightTowerFiberRight l r M)) := by
  intro h
  have hc := congrArg Prod.snd h
  change selectedAncestorTowerCount l r 6 (selectedEightTowerFiberLeft l r M) =
    selectedAncestorTowerCount l r 6 (selectedEightTowerFiberRight l r M) at hc
  rw [selectedEightTowerFiber_sixthGap l r M] at hc
  omega

end ExactFiber

#print axioms PentagonAdjoinedSixCell.selectedRawEightSignature
#print axioms PentagonAdjoinedSixCell.selectedRawEightSignature_toObservation
#print axioms PentagonAdjoinedSixCell.selectedAncestorShift_traceEq
#print axioms PentagonAdjoinedSixCell.selectedAncestorShift_bothTopZero
#print axioms PentagonAdjoinedSixCell.selectedAncestorShift_adjacentIfTopEq
#print axioms PentagonAdjoinedSixCell.selectedSevenQuintuple_sourcesTopZero
#print axioms PentagonAdjoinedSixCell.selectedEightTowerShift_eightSignature
#print axioms PentagonAdjoinedSixCell.selectedRawEightSignature_rightChain
#print axioms PentagonAdjoinedSixCell.selectedEightTowerFiber_eightSignature
#print axioms PentagonAdjoinedSixCell.selectedEightTowerFiber_eightObservedEq
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentEight_notInjective
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentEight_noDecoder
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentEight_noSixthDecoder
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentEight_endomorphismNotInjective
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentNineObservation
#print axioms PentagonAdjoinedSixCell.selectedRawCongruentNine_sixthDistinguished

end PentagonAdjoinedSixCell
end FivefoldP77FiniteRefinement
end KUOS.Architecture.WuxingPentagonUnified
