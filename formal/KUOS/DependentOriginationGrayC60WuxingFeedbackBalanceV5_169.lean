import KUOS.DependentOriginationGrayC60WuxingPentagramIncidenceV5_169

namespace KUOS.DependentOriginationGrayC60WuxingFeedbackBalanceV5_169

open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationGrayC60WuxingPentagramQuiverV5_169
open KUOS.DependentOriginationGrayC60WuxingPentagramIncidenceV5_169

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 3000000
noncomputable section

/-!
# F59-F21 — signed five-phase feedback, a counterexample and damping theorem

Giving the TWO Wuxing quiver cycles does not automatically establish
dynamical homeostasis. We supply an ACTUAL signed finite-state
linear feedback law, working over the real-valued phase signal space.

  (Lx)_i = x_(Sheng i) - x_(Ke i).

Positive Sheng and negative Ke terms are MODELING COEFFICIENTS,
not theorem-level identifications of all adjunctions or monads.

For the proposed undamped L there is a physical integer-valued
test signal exhibiting strictly POSITIVE instantaneous quadratic
work ⟨x,Lx⟩=4: bare "generation minus control" is not intrinsically
dissipative. Conversely with uniform local damping of strength 2,
an EXACT sum-of-squares identity proves global nonpositive
quadratic work. This gives an explicit, mathematically controlled
sufficient homeostasis criterion and extends independently to
ALL TWELVE original pentagonal C60 patches.

We do not infer biological kinetic parameters, pharmacological
effects or a direct F55 Gray 3-cell representation from this model.
-/

/-- Generating and controlling arrows contribute opposite
signs to an explicit real-valued finite signal operator. -/
def wuxingSignedFeedback (x : WuxingPhase → ℝ)
    (p : WuxingPhase) : ℝ :=
  x (wuxingSheng p) - x (wuxingKe p)

/-- An undamped system with constant input has zero net signed
feedback at each original phase: this does NOT imply stability
for general perturbations. -/
theorem wuxingSignedFeedback_constant (c : ℝ) (p : WuxingPhase) :
    wuxingSignedFeedback (fun _ => c) p = 0 := by
  simp [wuxingSignedFeedback]

/-- Direct real quadratic work of the signed 5×5 feedback matrix,
fully expanded over the TRUE Wood/Fire/Earth/Metal/Water order. -/
def wuxingQuadraticWork (x : WuxingPhase → ℝ) : ℝ :=
    x .wood  * wuxingSignedFeedback x .wood +
    x .fire  * wuxingSignedFeedback x .fire +
    x .earth * wuxingSignedFeedback x .earth +
    x .metal * wuxingSignedFeedback x .metal +
    x .water * wuxingSignedFeedback x .water

/-- Squared norm of the actual five-phase signal. -/
def wuxingSquaredMass (x : WuxingPhase → ℝ) : ℝ :=
    x .wood ^ 2 + x .fire ^ 2 + x .earth ^ 2 +
    x .metal ^ 2 + x .water ^ 2

/-- The FIVE Sheng "neighbour differences", all genuinely
nonnegative when squared over the real field. -/
def wuxingShengDifferenceSquares (x : WuxingPhase → ℝ) : ℝ :=
    (x .wood - x .fire) ^ 2 +
    (x .fire - x .earth) ^ 2 +
    (x .earth - x .metal) ^ 2 +
    (x .metal - x .water) ^ 2 +
    (x .water - x .wood) ^ 2

/-- The FIVE controlling two-step phase pairs, again squares
of genuine real signal expressions. -/
def wuxingKeSumSquares (x : WuxingPhase → ℝ) : ℝ :=
    (x .wood + x .earth) ^ 2 +
    (x .fire + x .metal) ^ 2 +
    (x .earth + x .water) ^ 2 +
    (x .metal + x .wood) ^ 2 +
    (x .water + x .fire) ^ 2

/-- EXACT signed-circulant sum-of-squares certificate:
the undamped feedback, supplemented by uniform damping 2I,
is dissipative, with an explicit nonnegative remainder.
The two cycles are both used essentially. -/
theorem wuxingFeedback_dampingTwo_sumOfSquares
    (x : WuxingPhase → ℝ) :
    (2 : ℝ) * (wuxingQuadraticWork x - 2 * wuxingSquaredMass x) =
      -(wuxingShengDifferenceSquares x + wuxingKeSumSquares x) := by
  dsimp [wuxingQuadraticWork, wuxingSquaredMass,
    wuxingShengDifferenceSquares, wuxingKeSumSquares,
    wuxingSignedFeedback, wuxingSheng, wuxingKe]
  ring

/-- Uniform damping 2 is a mathematically sufficient
energy-dissipation condition; no traditional or biological
stability coefficient was postulated as a measured fact. -/
theorem wuxingFeedback_dampingTwo_nonpositive
    (x : WuxingPhase → ℝ) :
    wuxingQuadraticWork x - 2 * wuxingSquaredMass x ≤ 0 := by
  have hs : 0 ≤ wuxingShengDifferenceSquares x := by
    unfold wuxingShengDifferenceSquares
    positivity
  have hk : 0 ≤ wuxingKeSumSquares x := by
    unfold wuxingKeSumSquares
    positivity
  have h := wuxingFeedback_dampingTwo_sumOfSquares x
  nlinarith only [h, hs, hk]

/-- One ACTUAL positive quadratic-work perturbation of the
five-phase signed feedback operator, all coordinates integral. -/
def wuxingUndampedGrowthWitness : WuxingPhase → ℝ
  | .wood => 1
  | .fire => 1
  | .earth => 0
  | .metal => -1
  | .water => -1

/-- A direct finite arithmetic counterexample to unconditional
homeostasis: the undamped generative-minus-controlling feedback
has positive work +4 in this legitimate five-phase mode. -/
theorem wuxingUndampedGrowthWitness_work :
    wuxingQuadraticWork wuxingUndampedGrowthWitness = 4 := by
  norm_num [wuxingQuadraticWork, wuxingSignedFeedback,
    wuxingUndampedGrowthWitness, wuxingSheng, wuxingKe]

theorem wuxingUndampedGrowthWitness_positive :
    0 < wuxingQuadraticWork wuxingUndampedGrowthWitness := by
  rw [wuxingUndampedGrowthWitness_work]
  norm_num

/-- The real signal on each C60 pentagonal patch is simply the
restriction of an original real function on the TRUE 60 darts
to its five genuine around-vertex dart positions. -/
def c60WuxingPentagonSignal
    (y : IcosahedralDart → ℝ) (v : IcosahedralVertex) :
    WuxingPhase → ℝ :=
  fun p => y (c60WuxingDart v p)

/-- A physically attached five-phase signed quadratic work on
the pentagon belonging to the original icosahedral vertex v. -/
def c60WuxingPentagonDampedWork
    (y : IcosahedralDart → ℝ) (v : IcosahedralVertex) : ℝ :=
  wuxingQuadraticWork (c60WuxingPentagonSignal y v) -
    2 * wuxingSquaredMass (c60WuxingPentagonSignal y v)

/-- Every one of the twelve real C60 pentagonal patches satisfies
the same damping energy inequality. -/
theorem c60WuxingEveryPentagon_damped_nonpositive
    (y : IcosahedralDart → ℝ) (v : IcosahedralVertex) :
    c60WuxingPentagonDampedWork y v ≤ 0 :=
  wuxingFeedback_dampingTwo_nonpositive
    (c60WuxingPentagonSignal y v)

/-- The sum of all TWELVE real pentagonal Wuxing feedback works
is nonpositive with uniform damping 2; the virtual pentagram
arrows are not being added to the original integer chain complex. -/
theorem c60WuxingAllTwelve_damped_nonpositive
    (y : IcosahedralDart → ℝ) :
    (∑ v : IcosahedralVertex,
      c60WuxingPentagonDampedWork y v) ≤ 0 := by
  apply Finset.sum_nonpos
  intro v _
  exact c60WuxingEveryPentagon_damped_nonpositive y v

#print axioms wuxingSignedFeedback_constant
#print axioms wuxingFeedback_dampingTwo_sumOfSquares
#print axioms wuxingFeedback_dampingTwo_nonpositive
#print axioms wuxingUndampedGrowthWitness_work
#print axioms wuxingUndampedGrowthWitness_positive
#print axioms c60WuxingEveryPentagon_damped_nonpositive
#print axioms c60WuxingAllTwelve_damped_nonpositive

end
end KUOS.DependentOriginationGrayC60WuxingFeedbackBalanceV5_169
