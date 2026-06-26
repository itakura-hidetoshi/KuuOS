import KUOS.WORLD.FourGreatPhaseTransitionCriteriaV0_60

/-!
WORLD v0.60 declaration hierarchy.

One analytic channel gives only a candidate.  Two channels give a concordant
candidate.  A strict declaration requires all three channels and a local change of
the four-great coordinate snapshot.
-/

namespace KUOS.WORLD

noncomputable section

section DeclarationHierarchy

variable {𝕜 A : Type*}
variable [CommSemiring 𝕜] [Semiring A] [Algebra 𝕜 A]
variable (System : WorldFourGreatPhaseTransitionSystem 𝕜 A)
variable (critical : ℝ)

structure WorldFourGreatPhaseTransitionCandidate where
  analyticEvidence :
    System.freeEnergyNonanalyticAt critical ∨
    System.spectralGapClosesAt critical ∨
    System.fixedPointAlgebraChangesAt critical
  fourGreatCoordinatesChange :
    System.fourGreatCoordinatesChangeAt critical

structure WorldFourGreatConcordantPhaseTransitionCandidate where
  concordantEvidence :
    (System.freeEnergyNonanalyticAt critical ∧
      System.spectralGapClosesAt critical) ∨
    (System.freeEnergyNonanalyticAt critical ∧
      System.fixedPointAlgebraChangesAt critical) ∨
    (System.spectralGapClosesAt critical ∧
      System.fixedPointAlgebraChangesAt critical)
  fourGreatCoordinatesChange :
    System.fourGreatCoordinatesChangeAt critical

structure WorldFourGreatPhaseTransitionDeclaration where
  freeEnergyNonanalytic :
    System.freeEnergyNonanalyticAt critical
  spectralGapCloses :
    System.spectralGapClosesAt critical
  fixedPointAlgebraChanges :
    System.fixedPointAlgebraChangesAt critical
  fourGreatCoordinatesChange :
    System.fourGreatCoordinatesChangeAt critical

namespace WorldFourGreatPhaseTransitionDeclaration

variable {System : WorldFourGreatPhaseTransitionSystem 𝕜 A}
variable {critical : ℝ}

/-- A strict declaration always determines a concordant candidate. -/
def toConcordant
    (Declaration :
      WorldFourGreatPhaseTransitionDeclaration System critical) :
    WorldFourGreatConcordantPhaseTransitionCandidate System critical where
  concordantEvidence :=
    Or.inl ⟨Declaration.freeEnergyNonanalytic,
      Declaration.spectralGapCloses⟩
  fourGreatCoordinatesChange :=
    Declaration.fourGreatCoordinatesChange

/-- A strict declaration always determines a single-channel candidate. -/
def toCandidate
    (Declaration :
      WorldFourGreatPhaseTransitionDeclaration System critical) :
    WorldFourGreatPhaseTransitionCandidate System critical where
  analyticEvidence :=
    Or.inl Declaration.freeEnergyNonanalytic
  fourGreatCoordinatesChange :=
    Declaration.fourGreatCoordinatesChange

theorem evidence_package
    (Declaration :
      WorldFourGreatPhaseTransitionDeclaration System critical) :
    System.freeEnergyNonanalyticAt critical ∧
    System.spectralGapClosesAt critical ∧
    System.fixedPointAlgebraChangesAt critical ∧
    System.fourGreatCoordinatesChangeAt critical :=
  ⟨Declaration.freeEnergyNonanalytic,
    Declaration.spectralGapCloses,
    Declaration.fixedPointAlgebraChanges,
    Declaration.fourGreatCoordinatesChange⟩

end WorldFourGreatPhaseTransitionDeclaration

namespace WorldFourGreatConcordantPhaseTransitionCandidate

variable {System : WorldFourGreatPhaseTransitionSystem 𝕜 A}
variable {critical : ℝ}

/-- A concordant candidate forgets to a single-channel candidate. -/
def toCandidate
    (Candidate :
      WorldFourGreatConcordantPhaseTransitionCandidate System critical) :
    WorldFourGreatPhaseTransitionCandidate System critical := by
  refine
    { analyticEvidence := ?_
      fourGreatCoordinatesChange := Candidate.fourGreatCoordinatesChange }
  rcases Candidate.concordantEvidence with h | h | h
  · exact Or.inl h.1
  · exact Or.inl h.1
  · exact Or.inr (Or.inl h.1)

end WorldFourGreatConcordantPhaseTransitionCandidate

end DeclarationHierarchy

end
end KUOS.WORLD
