import KUOS.DependentOriginationDoubleDeloopingNormalizedCocycleRealizationV1_100

namespace KUOS.DependentOriginationDoubleDeloopingTypeACocycleLiftingV1_101

open CategoryTheory
open CategoryTheory.Category
open Opposite
open Simplicial
open KUOS.DependentOriginationNativeInfinityTwoScaledV1_19
open KUOS.DependentOriginationGlobalDuskinScaledNerveV1_21
open KUOS.DependentOriginationScaledTerminalRLPV1_41
open KUOS.DependentOriginationStandardTypeAScaledHornFamilyV1_49
open KUOS.DependentOriginationStandardTypeAEndpointPushoutProductV1_50
open KUOS.DependentOriginationDoubleDeloopingNatNonthinDuskinWitnessV1_95
open KUOS.DependentOriginationDoubleDeloopingThinComparisonZeroV1_96
open KUOS.DependentOriginationDoubleDeloopingNormalizedCocycleRealizationV1_100

/-!
# Type-(A) lifting as normalized cocycle extension v1.101

Version v1.100 realizes every normalized `Nat`-valued additive 2-cocycle as a
literal Duskin simplex of the concrete double delooping `B²ℕ`.  The remaining
type-(A) lifting problem therefore has two logically separate parts:

* arithmetic: extend the horn comparison labels to a normalized cocycle;
* scaling: force the distinguished consecutive triangle to be thin.

For `B²ℕ`, v1.96 identifies thinness exactly with comparison label zero.  This
file proves that the second clause is *exactly* the vanishing of the cocycle
label on every triangle satisfying the standard type-(A) distinguished
predicate.  Thus a normalized cocycle with that zero condition automatically
realizes to a scaled type-(A) simplex.

We then package the precise remaining completion datum for a literal scaled
horn map:

```text
C : normalized additive cocycle on [n]
restriction(C.toSimplexMap) = hornMap
all type-(A) distinguished labels of C are zero.
```

Such a completion produces the categorical lift against the literal standard
type-(A) horn generator.  Consequently terminal type-(A) RLP for `B²ℕ` is
reduced to one purely cocyclic horn-extension property.  No bicategory
coherence and no scaling argument remains hidden in that property.
-/

namespace NatNormalizedDuskinCocycle

variable {n : Nat}

/-- Arithmetic form of the standard type-(A) scaling condition: every ordered
triangle whose vertices are consecutive around `i` has cocycle label zero. -/
def TypeADistinguishedZero
    (C : NatNormalizedDuskinCocycle n)
    (i : Fin (n + 1)) : Prop :=
  ∀ (a b c : Fin (n + 1))
    (hab : a ≤ b) (hbc : b ≤ c),
    b = i →
    a.val + 1 = i.val →
    i.val + 1 = c.val →
    C.label a b c hab hbc = 0

/-- The identically-zero cocycle, useful for the degree-two type-(A) filler. -/
def zero (n : Nat) : NatNormalizedDuskinCocycle n where
  label := fun _ _ _ _ _ => 0
  left_normalized := by intros; rfl
  right_normalized := by intros; rfl
  tetrahedron := by intros; simp

@[simp]
theorem zero_label
    (a b c : Fin (n + 1))
    (hab : a ≤ b) (hbc : b ≤ c) :
    (zero n).label a b c hab hbc = 0 :=
  rfl

/-- The zero cocycle satisfies the type-(A) distinguished-zero condition at
every index. -/
theorem zero_typeADistinguishedZero
    (i : Fin (n + 1)) :
    (zero n).TypeADistinguishedZero i := by
  intro a b c hab hbc hbi ha hc
  rfl

/-- If the distinguished type-(A) cocycle labels vanish, the realized Yoneda
simplex is a scaled map from the standard type-(A) scaled simplex. -/
theorem toSimplexMap_scaled_standardTypeA_of_distinguishedZero
    (C : NatNormalizedDuskinCocycle n)
    (i : Fin (n + 1))
    (hzero : C.TypeADistinguishedZero i) :
    IsScaledMap
      (standardTypeASimplexScaling i)
      (duskinScaling NatDoubleDelooping)
      C.toSimplexMap := by
  intro t ht
  rcases ht with hmin | hdist
  · exact
      (minimalScaling_map
        (duskinScaling NatDoubleDelooping) C.toSimplexMap) t hmin
  · have h01 : t (0 : Fin 3) ≤ t (1 : Fin 3) :=
      (SSet.stdSimplex.monotone_apply t) (by decide)
    have h12 : t (1 : Fin 3) ≤ t (2 : Fin 3) :=
      (SSet.stdSimplex.monotone_apply t) (by decide)
    have ht :
        t = SSet.stdSimplex.triangle
          (t (0 : Fin 3)) (t (1 : Fin 3)) (t (2 : Fin 3)) h01 h12 := by
      apply SSet.stdSimplex.ext
      intro j
      fin_cases j <;> rfl
    rw [ht]
    apply
      (natDuskin_thin_iff_comparison_eq_zero
        (C.toSimplexMap.app (op ⦋2⦌)
          (SSet.stdSimplex.triangle
            (t (0 : Fin 3)) (t (1 : Fin 3)) (t (2 : Fin 3)) h01 h12))).2
    rw [C.toSimplexMap_triangle_comparison]
    exact hzero
      (t (0 : Fin 3)) (t (1 : Fin 3)) (t (2 : Fin 3))
      h01 h12 hdist.1 hdist.2.1 hdist.2.2

/-- Conversely, if the realized Yoneda simplex is scaled for the standard
 type-(A) scaling, every distinguished cocycle label must vanish. -/
theorem distinguishedZero_of_toSimplexMap_scaled_standardTypeA
    (C : NatNormalizedDuskinCocycle n)
    (i : Fin (n + 1))
    (hscaled :
      IsScaledMap
        (standardTypeASimplexScaling i)
        (duskinScaling NatDoubleDelooping)
        C.toSimplexMap) :
    C.TypeADistinguishedZero i := by
  intro a b c hab hbc hbi ha hc
  let t : (Δ[n] : SSet).obj (op ⦋2⦌) :=
    SSet.stdSimplex.triangle a b c hab hbc
  have hdist : IsStandardTypeADistinguishedTriangle i t := by
    refine ⟨?_, ?_, ?_⟩
    · simpa [t] using hbi
    · simpa [t] using ha
    · simpa [t] using hc
  have hthin := hscaled t (Or.inr hdist)
  have hcomp :=
    (natDuskin_thin_iff_comparison_eq_zero
      (C.toSimplexMap.app (op ⦋2⦌) t)).1 hthin
  dsimp [t] at hcomp
  rw [C.toSimplexMap_triangle_comparison] at hcomp
  exact hcomp

/-- For realized normalized cocycles, standard type-(A) scaledness is exactly
vanishing on the distinguished consecutive triangle. -/
theorem toSimplexMap_scaled_standardTypeA_iff_distinguishedZero
    (C : NatNormalizedDuskinCocycle n)
    (i : Fin (n + 1)) :
    IsScaledMap
        (standardTypeASimplexScaling i)
        (duskinScaling NatDoubleDelooping)
        C.toSimplexMap ↔
      C.TypeADistinguishedZero i := by
  constructor
  · exact C.distinguishedZero_of_toSimplexMap_scaled_standardTypeA i
  · exact C.toSimplexMap_scaled_standardTypeA_of_distinguishedZero i

end NatNormalizedDuskinCocycle

/-! ## Exact cocycle completion datum for one literal type-(A) horn -/

/-- A completed additive cocycle for a literal scaled type-(A) horn map.

The equality `restrict` is equality of the underlying simplicial maps, while
`distinguished_zero` is precisely the target scaledness condition by the
preceding equivalence. -/
structure NatTypeAHornCocycleCompletion
    (g : StandardTypeAHornGeneratorIndex)
    (f : standardTypeAScaledHorn g ⟶ natDoubleDeloopingScaledDuskin) where
  cocycle : NatNormalizedDuskinCocycle g.n
  restrict :
    (Λ[g.n, g.i].ι :
      (Λ[g.n, g.i] : SSet) ⟶ (Δ[g.n] : SSet)) ≫
        cocycle.toSimplexMap = f.map
  distinguished_zero : cocycle.TypeADistinguishedZero g.i

namespace NatTypeAHornCocycleCompletion

variable
    {g : StandardTypeAHornGeneratorIndex}
    {f : standardTypeAScaledHorn g ⟶ natDoubleDeloopingScaledDuskin}

/-- Realize a cocycle completion as a literal scaled map out of the target
simplex of the standard type-(A) generator. -/
def toLift (K : NatTypeAHornCocycleCompletion g f) :
    standardTypeAScaledSimplex g ⟶ natDoubleDeloopingScaledDuskin where
  map := K.cocycle.toSimplexMap
  scaled :=
    K.cocycle.toSimplexMap_scaled_standardTypeA_of_distinguishedZero
      g.i K.distinguished_zero

/-- The realized cocycle lift restricts to the original horn map exactly. -/
theorem toLift_fac
    (K : NatTypeAHornCocycleCompletion g f) :
    standardTypeAScaledHornGeneratorHom g ≫ K.toLift = f := by
  apply ScaledSSet.ScaledMap.ext
  simpa [standardTypeAScaledHornGeneratorHom, toLift] using K.restrict

end NatTypeAHornCocycleCompletion

/-! ## Terminal RLP reduces to pure cocycle completion -/

/-- Pure arithmetic completion property for all literal standard type-(A)
horns into the concrete scaled Duskin nerve. -/
def HasAllStandardTypeAHornCocycleCompletions : Prop :=
  ∀ (g : StandardTypeAHornGeneratorIndex)
    (f : standardTypeAScaledHorn g ⟶ natDoubleDeloopingScaledDuskin),
    Nonempty (NatTypeAHornCocycleCompletion g f)

/-- A cocycle completion theorem for one generator gives its literal terminal
right lifting property. -/
theorem natDoubleDelooping_hasLiftingProperty_standardTypeA_of_cocycleCompletions
    (g : StandardTypeAHornGeneratorIndex)
    (H : ∀ f : standardTypeAScaledHorn g ⟶ natDoubleDeloopingScaledDuskin,
      Nonempty (NatTypeAHornCocycleCompletion g f)) :
    HasLiftingProperty
      (standardTypeAScaledHornGeneratorHom g)
      (ScaledSSet.toPoint natDoubleDeloopingScaledDuskin) := by
  apply
    (ScaledSSet.hasLiftingProperty_toPoint_iff
      (standardTypeAScaledHornGeneratorHom g)).2
  intro f
  rcases H f with ⟨K⟩
  exact ⟨K.toLift, K.toLift_fac⟩

/-- Once all additive horn cocycles can be completed, the terminal map belongs
to the right class of the complete standard type-(A) generator family. -/
theorem natDoubleDelooping_standardTypeA_rlp_of_cocycleCompletions
    (H : HasAllStandardTypeAHornCocycleCompletions) :
    (standardTypeAScaledHornGenerators : MorphismProperty ScaledSSet).rlp
      (ScaledSSet.toPoint natDoubleDeloopingScaledDuskin) := by
  rw [MorphismProperty.rlp_ofHoms_iff_hasLiftingProperty
    StandardTypeAHornGeneratorIndex]
  intro g
  exact
    natDoubleDelooping_hasLiftingProperty_standardTypeA_of_cocycleCompletions
      g (H g)

/-!
The type-(A) frontier is now purely arithmetic:

```text
for every inner horn map f : Lambda_i[n] -> N_D(B²N),
construct C : NatNormalizedDuskinCocycle n
such that
  restriction(C) = f
  and
  C(i-1,i,i+1) = 0.
```

The scaling condition is no longer an independent obligation: for realized
cocycles it is exactly the displayed zero condition.  Version v1.99 already
proves that the genuinely new cocycle equations occur only in dimensions
`2`, `3`, and `4`; from dimension five onward all triangles and tetrahedra are
visible in the horn.  The next unit can therefore prove
`HasAllStandardTypeAHornCocycleCompletions` by finite low-dimensional
completion plus the high-dimensional visibility theorem.
-/

end KUOS.DependentOriginationDoubleDeloopingTypeACocycleLiftingV1_101
