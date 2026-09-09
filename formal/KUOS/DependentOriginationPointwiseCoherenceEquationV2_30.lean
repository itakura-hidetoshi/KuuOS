import KUOS.DependentOriginationPointwiseExtensionObstructionV2_29

namespace KUOS.DependentOriginationPointwiseCoherenceEquationV2_30

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationWeakHigherLocalizationUniversalPropertyV2_18
open KUOS.DependentOriginationCoherentWeakHigherLocalizationV2_19
open KUOS.DependentOriginationStoredTriangleCorrectionTorsorV2_27
open KUOS.DependentOriginationComparisonAutomorphismSectionsV2_28
open KUOS.DependentOriginationPointwiseExtensionObstructionV2_29

universe u v uH vH

/-!
# Pointwise coherence equation normal form v2.30

The v2.29 layer isolated the exact gap between a nontrivial local comparison
automorphism and a genuine target modification: the local witness must extend
to a coherent automorphism section. This file opens that remaining existence
problem into an explicit system of arrowwise modification-naturality equations.

For one chosen nontrivial pointwise witness `q`, we separate objectwise extension
data, the arrowwise equations, and a complete equation solution. The central
normal form is

```text
coherence-equation solutions for q
  ≃
coherent automorphism sections whose q-component is the chosen witness.
```

Consequently, coherent extension exists exactly when the arrowwise equation
system has a solution, and failure means that every candidate extension family
has a witnessed defect on some arrow.

No equation-solvability, extension, rigidity, correction-existence,
strictification, or general weak higher-localization theorem is asserted
unconditionally.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

@[ext]
structure FactorComparisonPointwiseExtensionFamily
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    {H : HigherLocalizationFactorization (W := W) R}
    (q : FactorComparisonPointwiseAutomorphismWitness (W := W) H) where
  component : ∀ X : Context,
    H.comparison.app (.mk X) ≅ H.comparison.app (.mk X)
  atWitness : component q.object = q.automorphism

def FactorComparisonPointwiseExtensionFamily.SatisfiesCoherenceEquations
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    {H : HigherLocalizationFactorization (W := W) R}
    {q : FactorComparisonPointwiseAutomorphismWitness (W := W) H}
    (F : FactorComparisonPointwiseExtensionFamily (W := W) q) : Prop :=
  ∀ {X Y : Context} (f : X ⟶ Y),
    (restrictHigherLocalizedSystem W H.lift).map f.toLoc ◁
          (F.component Y).hom ≫
        (H.comparison.naturality f.toLoc).hom =
      (H.comparison.naturality f.toLoc).hom ≫
        (F.component X).hom ▷ R.map f.toLoc

def FactorComparisonPointwiseExtensionFamily.HasArrowwiseCoherenceDefect
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    {H : HigherLocalizationFactorization (W := W) R}
    {q : FactorComparisonPointwiseAutomorphismWitness (W := W) H}
    (F : FactorComparisonPointwiseExtensionFamily (W := W) q) : Prop :=
  ∃ (X Y : Context) (f : X ⟶ Y),
    (restrictHigherLocalizedSystem W H.lift).map f.toLoc ◁
          (F.component Y).hom ≫
        (H.comparison.naturality f.toLoc).hom ≠
      (H.comparison.naturality f.toLoc).hom ≫
        (F.component X).hom ▷ R.map f.toLoc

theorem not_satisfiesCoherenceEquations_iff_hasArrowwiseDefect
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    {H : HigherLocalizationFactorization (W := W) R}
    {q : FactorComparisonPointwiseAutomorphismWitness (W := W) H}
    (F : FactorComparisonPointwiseExtensionFamily (W := W) q) :
    (¬ F.SatisfiesCoherenceEquations (W := W)) ↔
      F.HasArrowwiseCoherenceDefect (W := W) := by
  classical
  constructor
  · intro hNot
    by_contra hNoDefect
    apply hNot
    intro X Y f
    by_contra hNe
    exact hNoDefect ⟨X, Y, f, hNe⟩
  · rintro ⟨X, Y, f, hNe⟩ hCoherence
    exact hNe (hCoherence f)

@[ext]
structure FactorComparisonPointwiseCoherenceEquationSolution
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    {H : HigherLocalizationFactorization (W := W) R}
    (q : FactorComparisonPointwiseAutomorphismWitness (W := W) H) where
  family : FactorComparisonPointwiseExtensionFamily (W := W) q
  coherence : family.SatisfiesCoherenceEquations (W := W)

def coherentSectionOfPointwiseCoherenceEquationSolution
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    {H : HigherLocalizationFactorization (W := W) R}
    {q : FactorComparisonPointwiseAutomorphismWitness (W := W) H}
    (S : FactorComparisonPointwiseCoherenceEquationSolution (W := W) q) :
    FactorComparisonAutomorphismSection (W := W) H where
  component := S.family.component
  naturality := S.coherence

def pointwiseCoherenceEquationSolutionOfSection
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    {H : HigherLocalizationFactorization (W := W) R}
    (q : FactorComparisonPointwiseAutomorphismWitness (W := W) H)
    (P : FactorComparisonAutomorphismSection (W := W) H)
    (hAt : P.component q.object = q.automorphism) :
    FactorComparisonPointwiseCoherenceEquationSolution (W := W) q where
  family := {
    component := P.component
    atWitness := hAt
  }
  coherence := P.naturality

theorem coherentSection_solutionOfSection
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    {H : HigherLocalizationFactorization (W := W) R}
    (q : FactorComparisonPointwiseAutomorphismWitness (W := W) H)
    (P : FactorComparisonAutomorphismSection (W := W) H)
    (hAt : P.component q.object = q.automorphism) :
    coherentSectionOfPointwiseCoherenceEquationSolution
      (W := W) (pointwiseCoherenceEquationSolutionOfSection
        (W := W) q P hAt) = P := by
  ext X
  rfl

theorem solutionOfSection_coherentSection
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    {H : HigherLocalizationFactorization (W := W) R}
    {q : FactorComparisonPointwiseAutomorphismWitness (W := W) H}
    (S : FactorComparisonPointwiseCoherenceEquationSolution (W := W) q) :
    pointwiseCoherenceEquationSolutionOfSection
      (W := W) q
      (coherentSectionOfPointwiseCoherenceEquationSolution (W := W) S)
      S.family.atWitness = S := by
  ext X
  rfl

def pointwiseCoherenceEquationSolutionEquivExtensionSection
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    {H : HigherLocalizationFactorization (W := W) R}
    (q : FactorComparisonPointwiseAutomorphismWitness (W := W) H) :
    FactorComparisonPointwiseCoherenceEquationSolution (W := W) q ≃
      { P : FactorComparisonAutomorphismSection (W := W) H //
        P.component q.object = q.automorphism } where
  toFun S :=
    ⟨coherentSectionOfPointwiseCoherenceEquationSolution (W := W) S,
      S.family.atWitness⟩
  invFun P :=
    pointwiseCoherenceEquationSolutionOfSection (W := W) q P.1 P.2
  left_inv := solutionOfSection_coherentSection (W := W)
  right_inv := by
    intro P
    apply Subtype.ext
    exact coherentSection_solutionOfSection (W := W) q P.1 P.2

theorem hasCoherentExtension_iff_nonemptyCoherenceEquationSolution
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    {H : HigherLocalizationFactorization (W := W) R}
    (q : FactorComparisonPointwiseAutomorphismWitness (W := W) H) :
    q.HasCoherentExtension (W := W) ↔
      Nonempty (FactorComparisonPointwiseCoherenceEquationSolution
        (W := W) q) := by
  constructor
  · rintro ⟨P, hAt⟩
    exact ⟨pointwiseCoherenceEquationSolutionOfSection (W := W) q P hAt⟩
  · rintro ⟨S⟩
    exact ⟨coherentSectionOfPointwiseCoherenceEquationSolution (W := W) S,
      S.family.atWitness⟩

theorem not_hasCoherentExtension_iff_everyFamily_hasArrowwiseDefect
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    {H : HigherLocalizationFactorization (W := W) R}
    (q : FactorComparisonPointwiseAutomorphismWitness (W := W) H) :
    (¬ q.HasCoherentExtension (W := W)) ↔
      ∀ F : FactorComparisonPointwiseExtensionFamily (W := W) q,
        F.HasArrowwiseCoherenceDefect (W := W) := by
  constructor
  · intro hNoExtension F
    apply
      (not_satisfiesCoherenceEquations_iff_hasArrowwiseDefect
        (W := W) F).mp
    intro hCoherence
    apply hNoExtension
    exact
      (hasCoherentExtension_iff_nonemptyCoherenceEquationSolution
        (W := W) q).mpr
        ⟨{ family := F, coherence := hCoherence }⟩
  · intro hEveryDefect hExtension
    rcases
      (hasCoherentExtension_iff_nonemptyCoherenceEquationSolution
        (W := W) q).mp hExtension with ⟨S⟩
    have hNotCoherence :
        ¬ S.family.SatisfiesCoherenceEquations (W := W) :=
      (not_satisfiesCoherenceEquations_iff_hasArrowwiseDefect
        (W := W) S.family).mpr (hEveryDefect S.family)
    exact hNotCoherence S.coherence

def FactorComparisonPointwiseArrowwiseCoherenceObstruction
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    {H : HigherLocalizationFactorization (W := W) R}
    (q : FactorComparisonPointwiseAutomorphismWitness (W := W) H) : Prop :=
  ∀ F : FactorComparisonPointwiseExtensionFamily (W := W) q,
    F.HasArrowwiseCoherenceDefect (W := W)

theorem pointwiseArrowwiseObstruction_iff_not_hasCoherentExtension
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    {H : HigherLocalizationFactorization (W := W) R}
    (q : FactorComparisonPointwiseAutomorphismWitness (W := W) H) :
    FactorComparisonPointwiseArrowwiseCoherenceObstruction (W := W) q ↔
      ¬ q.HasCoherentExtension (W := W) :=
  (not_hasCoherentExtension_iff_everyFamily_hasArrowwiseDefect
    (W := W) q).symm

def FactorComparisonArrowwiseCoherenceObstruction
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (H : HigherLocalizationFactorization (W := W) R) : Prop :=
  HasNontrivialFactorComparisonPointwiseAutomorphism (W := W) H ∧
    ∀ q : FactorComparisonPointwiseAutomorphismWitness (W := W) H,
      FactorComparisonPointwiseArrowwiseCoherenceObstruction (W := W) q

theorem arrowwiseCoherenceObstruction_iff_coherenceExtensionObstruction
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (H : HigherLocalizationFactorization (W := W) R) :
    FactorComparisonArrowwiseCoherenceObstruction (W := W) H ↔
      FactorComparisonCoherenceExtensionObstruction (W := W) H := by
  constructor
  · rintro ⟨hWitness, hArrow⟩
    exact ⟨hWitness, fun q =>
      (pointwiseArrowwiseObstruction_iff_not_hasCoherentExtension
        (W := W) q).mp (hArrow q)⟩
  · rintro ⟨hWitness, hNoExtension⟩
    exact ⟨hWitness, fun q =>
      (pointwiseArrowwiseObstruction_iff_not_hasCoherentExtension
        (W := W) q).mpr (hNoExtension q)⟩

theorem arrowwiseCoherenceObstruction_iff_pointwiseNonrigid_and_targetRigid
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (H : HigherLocalizationFactorization (W := W) R) :
    FactorComparisonArrowwiseCoherenceObstruction (W := W) H ↔
      (¬ FactorComparisonPointwiseAutomorphismRigidity (W := W) H) ∧
        Subsingleton (H.comparison ≅ H.comparison) := by
  rw [arrowwiseCoherenceObstruction_iff_coherenceExtensionObstruction
    (W := W) H]
  exact
    coherenceExtensionObstruction_iff_pointwiseNonrigid_and_targetRigid
      (W := W) H

def FactorComparisonPointwiseCoherenceEquationSolvability
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (H : HigherLocalizationFactorization (W := W) R) : Prop :=
  ∀ q : FactorComparisonPointwiseAutomorphismWitness (W := W) H,
    Nonempty (FactorComparisonPointwiseCoherenceEquationSolution (W := W) q)

theorem pointwiseCoherenceEquationSolvability_iff_extensionProperty
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (H : HigherLocalizationFactorization (W := W) R) :
    FactorComparisonPointwiseCoherenceEquationSolvability (W := W) H ↔
      FactorComparisonPointwiseAutomorphismExtensionProperty (W := W) H := by
  constructor
  · intro hSolve q
    exact
      (hasCoherentExtension_iff_nonemptyCoherenceEquationSolution
        (W := W) q).mpr (hSolve q)
  · intro hExtension q
    exact
      (hasCoherentExtension_iff_nonemptyCoherenceEquationSolution
        (W := W) q).mp (hExtension q)

theorem pointwiseRigidity_iff_targetRigidity_of_coherenceEquationSolvability
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (H : HigherLocalizationFactorization (W := W) R)
    (hSolve : FactorComparisonPointwiseCoherenceEquationSolvability
      (W := W) H) :
    FactorComparisonPointwiseAutomorphismRigidity (W := W) H ↔
      Subsingleton (H.comparison ≅ H.comparison) :=
  pointwiseRigidity_iff_targetRigidity_of_extensionProperty
    (W := W) H
    ((pointwiseCoherenceEquationSolvability_iff_extensionProperty
      (W := W) H).mp hSolve)

def HigherFactorComparisonPointwiseCoherenceEquationSolvability
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) : Prop :=
  ∀ (H : HigherLocalizationFactorization (W := W) R)
    (_alpha : HigherLocalizationFactorMorphism (W := W) H U.chosen),
    FactorComparisonPointwiseCoherenceEquationSolvability (W := W) H

theorem higherPointwiseCoherenceEquationSolvability_iff_extensionProperty
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    HigherFactorComparisonPointwiseCoherenceEquationSolvability (W := W) U ↔
      HigherFactorComparisonPointwiseAutomorphismExtensionProperty
        (W := W) U := by
  constructor
  · intro hSolve H alpha
    exact
      (pointwiseCoherenceEquationSolvability_iff_extensionProperty
        (W := W) H).mp (hSolve H alpha)
  · intro hExtension H alpha
    exact
      (pointwiseCoherenceEquationSolvability_iff_extensionProperty
        (W := W) H).mpr (hExtension H alpha)

def HigherFactorComparisonArrowwiseCoherenceObstruction
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) : Prop :=
  ∃ (H : HigherLocalizationFactorization (W := W) R)
    (alpha : HigherLocalizationFactorMorphism (W := W) H U.chosen),
    FactorComparisonArrowwiseCoherenceObstruction (W := W) H

theorem higherArrowwiseCoherenceObstruction_iff_extensionObstruction
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    HigherFactorComparisonArrowwiseCoherenceObstruction (W := W) U ↔
      HigherFactorComparisonCoherenceExtensionObstruction (W := W) U := by
  constructor
  · rintro ⟨H, alpha, hArrow⟩
    exact ⟨H, alpha,
      (arrowwiseCoherenceObstruction_iff_coherenceExtensionObstruction
        (W := W) H).mp hArrow⟩
  · rintro ⟨H, alpha, hExtension⟩
    exact ⟨H, alpha,
      (arrowwiseCoherenceObstruction_iff_coherenceExtensionObstruction
        (W := W) H).mpr hExtension⟩

theorem higherArrowwiseCoherenceObstruction_iff_not_pointwiseRigidity_of_targetRigidity
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hTarget : HigherFactorComparisonAutomorphismRigidity (W := W) U) :
    HigherFactorComparisonArrowwiseCoherenceObstruction (W := W) U ↔
      ¬ HigherFactorComparisonPointwiseAutomorphismRigidity (W := W) U := by
  rw [higherArrowwiseCoherenceObstruction_iff_extensionObstruction
    (W := W) U]
  exact
    higherCoherenceExtensionObstruction_iff_not_pointwiseRigidity_of_targetRigidity
      (W := W) U hTarget

def HigherFactorComparisonPointwiseCoherenceEquationSolvabilityPrinciple : Prop :=
  ∀ (R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH))
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R),
    HigherFactorComparisonPointwiseCoherenceEquationSolvability (W := W) U

theorem pointwiseRigidity_iff_targetRigidity_of_globalCoherenceEquationSolvability
    (hSolve : HigherFactorComparisonPointwiseCoherenceEquationSolvabilityPrinciple
      (W := W) (uH := uH) (vH := vH)) :
    ∀ (R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH))
      (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R),
      HigherFactorComparisonPointwiseAutomorphismRigidity (W := W) U ↔
        HigherFactorComparisonAutomorphismRigidity (W := W) U := by
  intro R U
  exact
    higherPointwiseRigidity_iff_targetRigidity_of_extensionProperty
      (W := W) U
      ((higherPointwiseCoherenceEquationSolvability_iff_extensionProperty
        (W := W) U).mp (hSolve R U))

/-!
The v2.29 extension obstruction now has an explicit equation-theoretic normal
form:

```text
coherent extension
  <->
objectwise extension family + all arrowwise naturality equations.

not coherent extension
  <->
for every candidate family, some arrow witnesses a naturality defect.
```

Thus `pointwise non-rigidity + target rigidity` is exactly an arrowwise
coherence-equation obstruction. Equation solvability remains an explicit
unproved property. No general correction existence, arbitrary pseudofunctor
strictification, or general weak higher-localization universal principle is
asserted here.
-/

end KUOS.DependentOriginationPointwiseCoherenceEquationV2_30