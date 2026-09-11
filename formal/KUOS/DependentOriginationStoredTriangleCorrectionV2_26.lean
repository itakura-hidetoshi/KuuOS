import KUOS.DependentOriginationArbitraryTrianglePresentationV2_25

namespace KUOS.DependentOriginationStoredTriangleCorrectionV2_26

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationWeakHigherLocalizationUniversalPropertyV2_18
open KUOS.DependentOriginationCoherentWeakHigherLocalizationV2_19
open KUOS.DependentOriginationModificationTriangleNormalFormV2_22
open KUOS.DependentOriginationStoredTriangleModificationNaturalityV2_23
open KUOS.DependentOriginationStoredTriangleModificationRealizationV2_24
open KUOS.DependentOriginationArbitraryTrianglePresentationV2_25

open scoped CategoryTheory.Pseudofunctor.StrongTrans

universe u v uH vH

/-!
# Stored triangle correction theory v2.26

The v2.25 layer identifies the genuine general obstruction: for a fixed v2.18
factor morphism `alpha`, no coherent objectwise 2-isomorphism family with the
required endpoints may exist.  The particular objectwise family stored by v2.18
is only one candidate.

This file turns that coherent-replacement problem into an exact correction
problem relative to the stored family.

For every raw context object `X`, the stored v2.18 triangle already supplies an
isomorphism

```text
stored_X : A_X ≅ B_X,
```

where

```text
A = restrict(alpha.hom) ≫ K.comparison,
B = H.comparison.
```

A target-side correction is an arbitrary automorphism

```text
c_X : B_X ≅ B_X.
```

We do **not** require the family `c_X` itself to be a modification.  Instead we
require only that the corrected family

```text
stored_X ≪≫ c_X : A_X ≅ B_X
```

satisfy the modification naturality equation.  Thus this formalism genuinely
allows the stored family to fail while a nontrivial pointwise correction repairs
it.

The main result is a data-level equivalence

```text
stored target-side corrections
        ≃
coherent arbitrary presentations
        ≃
invertible modification triangles.
```

Consequently, the v2.25 coherent-replacement existence problem is exactly the
solvability of this correction equation.  The identity correction solves the
equation exactly when the originally stored family is modification-natural.

No correction is asserted to exist unconditionally.  No additive subtraction of
2-cells, strictification theorem, or ordinary-localization replacement is used.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- A pointwise target-side correction of the stored v2.18 triangle family.

The correction components themselves need not be natural.  The only coherence
condition is that postcomposing the stored triangle component by the correction
produces a valid modification-natural family. -/
@[ext]
structure StoredTriangleTargetCorrection
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    {H K : HigherLocalizationFactorization (W := W) R}
    (alpha : HigherLocalizationFactorMorphism (W := W) H K) where
  component : ∀ X : Context,
    H.comparison.app (.mk X) ≅ H.comparison.app (.mk X)
  corrected_naturality : ∀ {X Y : Context} (f : X ⟶ Y),
    (restrictHigherLocalizedSystem W H.lift).map f.toLoc ◁
          ((storedV2_18ComparisonComponentIso (W := W) alpha Y).trans
            (component Y)).hom ≫
        (H.comparison.naturality f.toLoc).hom =
      ((restrictHigherLocalizedStrongTrans (W := W) alpha.hom ≫
          K.comparison).naturality f.toLoc).hom ≫
        ((storedV2_18ComparisonComponentIso (W := W) alpha X).trans
          (component X)).hom ▷ R.map f.toLoc

/-- Apply a stored-family correction to obtain the corresponding arbitrary
coherent presentation. -/
def factorModificationTrianglePresentationOfStoredCorrection
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    {H K : HigherLocalizationFactorization (W := W) R}
    {alpha : HigherLocalizationFactorMorphism (W := W) H K}
    (C : StoredTriangleTargetCorrection (W := W) alpha) :
    FactorModificationTrianglePresentation (W := W) alpha where
  component X :=
    (storedV2_18ComparisonComponentIso (W := W) alpha X).trans (C.component X)
  naturality f := C.corrected_naturality f

/-- Every arbitrary coherent presentation determines a unique pointwise
correction relative to the stored v2.18 family, obtained by cancelling the
stored isomorphism on the left. -/
def storedTriangleTargetCorrectionOfPresentation
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    {H K : HigherLocalizationFactorization (W := W) R}
    {alpha : HigherLocalizationFactorMorphism (W := W) H K}
    (P : FactorModificationTrianglePresentation (W := W) alpha) :
    StoredTriangleTargetCorrection (W := W) alpha where
  component X :=
    (storedV2_18ComparisonComponentIso (W := W) alpha X).symm.trans (P.component X)
  corrected_naturality f := by
    simpa [Category.assoc] using P.naturality f

/-- Cancelling the stored family and then reapplying it recovers the original
coherent presentation. -/
theorem presentationOfStoredCorrection_ofPresentation
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    {H K : HigherLocalizationFactorization (W := W) R}
    {alpha : HigherLocalizationFactorMorphism (W := W) H K}
    (P : FactorModificationTrianglePresentation (W := W) alpha) :
    factorModificationTrianglePresentationOfStoredCorrection
        (W := W) (storedTriangleTargetCorrectionOfPresentation (W := W) P) = P := by
  ext X
  apply Iso.ext
  simp [factorModificationTrianglePresentationOfStoredCorrection,
    storedTriangleTargetCorrectionOfPresentation, Category.assoc]

/-- Reapplying the stored family and then cancelling it recovers the original
pointwise correction. -/
theorem storedCorrectionOfPresentation_ofStoredCorrection
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    {H K : HigherLocalizationFactorization (W := W) R}
    {alpha : HigherLocalizationFactorMorphism (W := W) H K}
    (C : StoredTriangleTargetCorrection (W := W) alpha) :
    storedTriangleTargetCorrectionOfPresentation
        (W := W)
        (factorModificationTrianglePresentationOfStoredCorrection (W := W) C) = C := by
  ext X
  apply Iso.ext
  simp [factorModificationTrianglePresentationOfStoredCorrection,
    storedTriangleTargetCorrectionOfPresentation, Category.assoc]

/-- Exact data-level equivalence between stored-family target corrections and
arbitrary coherent modification-triangle presentations. -/
def storedTriangleTargetCorrectionEquivPresentation
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    {H K : HigherLocalizationFactorization (W := W) R}
    (alpha : HigherLocalizationFactorMorphism (W := W) H K) :
    StoredTriangleTargetCorrection (W := W) alpha ≃
      FactorModificationTrianglePresentation (W := W) alpha where
  toFun := factorModificationTrianglePresentationOfStoredCorrection (W := W)
  invFun := storedTriangleTargetCorrectionOfPresentation (W := W)
  left_inv := storedCorrectionOfPresentation_ofStoredCorrection (W := W)
  right_inv := presentationOfStoredCorrection_ofPresentation (W := W)

/-- Exact data-level equivalence between stored-family target corrections and
actual invertible modification triangles. -/
def storedTriangleTargetCorrectionEquivIso
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    {H K : HigherLocalizationFactorization (W := W) R}
    (alpha : HigherLocalizationFactorMorphism (W := W) H K) :
    StoredTriangleTargetCorrection (W := W) alpha ≃
      ((restrictHigherLocalizedStrongTrans (W := W) alpha.hom ≫ K.comparison) ≅
        H.comparison) :=
  (storedTriangleTargetCorrectionEquivPresentation (W := W) alpha).trans
    (factorModificationTrianglePresentationEquiv (W := W) alpha)

/-- Solvability of the stored-family correction equation for one factor. -/
def HasStoredTriangleTargetCorrection
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    {H K : HigherLocalizationFactorization (W := W) R}
    (alpha : HigherLocalizationFactorMorphism (W := W) H K) : Prop :=
  Nonempty (StoredTriangleTargetCorrection (W := W) alpha)

/-- The correction equation is solvable exactly when an arbitrary coherent
presentation exists. -/
theorem hasStoredTriangleTargetCorrection_iff_hasCoherentPresentation
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    {H K : HigherLocalizationFactorization (W := W) R}
    (alpha : HigherLocalizationFactorMorphism (W := W) H K) :
    HasStoredTriangleTargetCorrection (W := W) alpha ↔
      HasCoherentFactorModificationTrianglePresentation (W := W) alpha := by
  constructor
  · rintro ⟨C⟩
    exact ⟨factorModificationTrianglePresentationOfStoredCorrection (W := W) C⟩
  · rintro ⟨P⟩
    exact ⟨storedTriangleTargetCorrectionOfPresentation (W := W) P⟩

/-- Equivalently, solvability of the correction equation is exactly the v2.22
arbitrary modification-triangle condition. -/
theorem hasStoredTriangleTargetCorrection_iff_hasFactorModificationTriangle
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    {H K : HigherLocalizationFactorization (W := W) R}
    (alpha : HigherLocalizationFactorMorphism (W := W) H K) :
    HasStoredTriangleTargetCorrection (W := W) alpha ↔
      HasFactorModificationTriangle (W := W) alpha := by
  rw [hasStoredTriangleTargetCorrection_iff_hasCoherentPresentation (W := W) alpha]
  exact (hasFactorModificationTriangle_iff_hasCoherentPresentation
    (W := W) alpha).symm

/-- When the stored family is already modification-natural, the identity
pointwise automorphism is a correction solution. -/
def identityStoredTriangleTargetCorrection
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    {H K : HigherLocalizationFactorization (W := W) R}
    (alpha : HigherLocalizationFactorMorphism (W := W) H K)
    (hNatural : StoredV2_18TriangleIsModificationNatural (W := W) alpha) :
    StoredTriangleTargetCorrection (W := W) alpha where
  component X := Iso.refl _
  corrected_naturality f := by
    simpa using hNatural f

@[simp] theorem identityStoredTriangleTargetCorrection_component
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    {H K : HigherLocalizationFactorization (W := W) R}
    (alpha : HigherLocalizationFactorMorphism (W := W) H K)
    (hNatural : StoredV2_18TriangleIsModificationNatural (W := W) alpha)
    (X : Context) :
    (identityStoredTriangleTargetCorrection (W := W) alpha hNatural).component X =
      Iso.refl _ := by
  rfl

/-- The identity correction solves the correction equation exactly when the
stored v2.18 family itself is modification-natural.

This makes the distinction from v2.25 precise: arbitrary correction solvability
may hold even when the identity correction does not. -/
theorem storedTriangleNaturality_iff_exists_identityCorrection
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    {H K : HigherLocalizationFactorization (W := W) R}
    (alpha : HigherLocalizationFactorMorphism (W := W) H K) :
    StoredV2_18TriangleIsModificationNatural (W := W) alpha ↔
      ∃ C : StoredTriangleTargetCorrection (W := W) alpha,
        ∀ X : Context, C.component X = Iso.refl _ := by
  constructor
  · intro hNatural
    refine ⟨identityStoredTriangleTargetCorrection (W := W) alpha hNatural, ?_⟩
    intro X
    rfl
  · rintro ⟨C, hIdentity⟩
    intro X Y f
    have h := C.corrected_naturality f
    rw [hIdentity X, hIdentity Y] at h
    simpa using h

/-- Uniform solvability of the stored-family correction equation over all v2.18
factors into one chosen coherent universal datum. -/
def HigherStoredTriangleTargetCorrectionLifting
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) : Prop :=
  ∀ (H : HigherLocalizationFactorization (W := W) R)
    (alpha : HigherLocalizationFactorMorphism (W := W) H U.chosen),
    HasStoredTriangleTargetCorrection (W := W) alpha

/-- Uniform correction solvability is exactly uniform arbitrary coherent-
presentation lifting. -/
theorem higherStoredTriangleCorrectionLifting_iff_coherentPresentationLifting
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    HigherStoredTriangleTargetCorrectionLifting (W := W) U ↔
      HigherCoherentFactorModificationTrianglePresentationLifting (W := W) U := by
  constructor
  · intro h H alpha
    exact
      (hasStoredTriangleTargetCorrection_iff_hasCoherentPresentation
        (W := W) alpha).mp (h H alpha)
  · intro h H alpha
    exact
      (hasStoredTriangleTargetCorrection_iff_hasCoherentPresentation
        (W := W) alpha).mpr (h H alpha)

/-- Uniform correction solvability is therefore exactly the existing v2.22
modification-triangle lifting condition. -/
theorem higherStoredTriangleCorrectionLifting_iff_modificationTriangleLifting
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    HigherStoredTriangleTargetCorrectionLifting (W := W) U ↔
      HigherFactorModificationTriangleLifting (W := W) U := by
  rw [higherStoredTriangleCorrectionLifting_iff_coherentPresentationLifting
    (W := W) U]
  exact higherCoherentPresentationLifting_iff_modificationTriangleLifting
    (W := W) U

/-- Failure of the correction equation for some factor. -/
def HigherStoredTriangleTargetCorrectionObstruction
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) : Prop :=
  ∃ (H : HigherLocalizationFactorization (W := W) R)
    (alpha : HigherLocalizationFactorMorphism (W := W) H U.chosen),
    ¬ HasStoredTriangleTargetCorrection (W := W) alpha

/-- The correction obstruction is exactly the v2.25 coherent-presentation
obstruction. -/
theorem higherStoredTriangleCorrectionObstruction_iff_coherentPresentationObstruction
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    HigherStoredTriangleTargetCorrectionObstruction (W := W) U ↔
      HigherCoherentFactorModificationTrianglePresentationObstruction (W := W) U := by
  constructor
  · rintro ⟨H, alpha, hNoCorrection⟩
    refine ⟨H, alpha, ?_⟩
    intro hPresentation
    exact hNoCorrection
      ((hasStoredTriangleTargetCorrection_iff_hasCoherentPresentation
        (W := W) alpha).mpr hPresentation)
  · rintro ⟨H, alpha, hNoPresentation⟩
    refine ⟨H, alpha, ?_⟩
    intro hCorrection
    exact hNoPresentation
      ((hasStoredTriangleTargetCorrection_iff_hasCoherentPresentation
        (W := W) alpha).mp hCorrection)

/-- The correction obstruction is also exactly the v2.22 modification-triangle
obstruction. -/
theorem higherStoredTriangleCorrectionObstruction_iff_modificationTriangleObstruction
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    HigherStoredTriangleTargetCorrectionObstruction (W := W) U ↔
      HigherFactorModificationTriangleObstruction (W := W) U := by
  rw [higherStoredTriangleCorrectionObstruction_iff_coherentPresentationObstruction
    (W := W) U]
  exact higherCoherentPresentationObstruction_iff_modificationTriangleObstruction
    (W := W) U

/-- Uniform correction solvability is exactly absence of the explicit correction
obstruction. -/
theorem higherStoredTriangleCorrectionLifting_iff_no_obstruction
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    HigherStoredTriangleTargetCorrectionLifting (W := W) U ↔
      ¬ HigherStoredTriangleTargetCorrectionObstruction (W := W) U := by
  rw [higherStoredTriangleCorrectionLifting_iff_modificationTriangleLifting
    (W := W) U]
  rw [higherFactorModificationTriangleLifting_iff_no_obstruction (W := W) U]
  rw [← higherStoredTriangleCorrectionObstruction_iff_modificationTriangleObstruction
    (W := W) U]

/-- Uniform stored-family naturality is the special case of uniform correction
solvability in which the identity correction works for every factor. -/
theorem higherStoredTriangleCorrectionLifting_of_storedTriangleNaturality
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hNatural : HigherStoredV2_18TriangleModificationNaturality (W := W) U) :
    HigherStoredTriangleTargetCorrectionLifting (W := W) U := by
  intro H alpha
  exact ⟨identityStoredTriangleTargetCorrection (W := W) alpha (hNatural H alpha)⟩

/-- Global correction-solvability principle. -/
def HigherStoredTriangleTargetCorrectionPrinciple : Prop :=
  ∀ (R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH))
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R),
    HigherStoredTriangleTargetCorrectionLifting (W := W) U

/-- The global correction principle is exactly the v2.25 global coherent-
presentation principle. -/
theorem higherStoredTriangleCorrectionPrinciple_iff_coherentPresentationPrinciple :
    HigherStoredTriangleTargetCorrectionPrinciple
        (W := W) (uH := uH) (vH := vH) ↔
      HigherCoherentFactorModificationTrianglePresentationPrinciple
        (W := W) (uH := uH) (vH := vH) := by
  constructor
  · intro h R U
    exact
      (higherStoredTriangleCorrectionLifting_iff_coherentPresentationLifting
        (W := W) U).mp (h R U)
  · intro h R U
    exact
      (higherStoredTriangleCorrectionLifting_iff_coherentPresentationLifting
        (W := W) U).mpr (h R U)

/-- The global correction principle is exactly the existing v2.22 global
modification-triangle lifting principle. -/
theorem higherStoredTriangleCorrectionPrinciple_iff_modificationTrianglePrinciple :
    HigherStoredTriangleTargetCorrectionPrinciple
        (W := W) (uH := uH) (vH := vH) ↔
      HigherFactorModificationTriangleLiftingPrinciple
        (W := W) (uH := uH) (vH := vH) := by
  rw [higherStoredTriangleCorrectionPrinciple_iff_coherentPresentationPrinciple
    (W := W) (uH := uH) (vH := vH)]
  exact higherCoherentPresentationPrinciple_iff_modificationTrianglePrinciple
    (W := W) (uH := uH) (vH := vH)

/-- Hence the coherent higher universal principle plus global correction
solvability implies the v2.18 weak higher-localization universal principle.

This is still conditional: neither global premise is asserted here. -/
theorem higherWeakLocalizationUniversalPrinciple_of_coherent_and_corrections
    (hCoherent : CoherentHigherWeakLocalizationUniversalPrinciple
      (W := W) (uH := uH) (vH := vH))
    (hCorrections : HigherStoredTriangleTargetCorrectionPrinciple
      (W := W) (uH := uH) (vH := vH)) :
    HigherWeakLocalizationUniversalPrinciple
      (W := W) (uH := uH) (vH := vH) :=
  higherWeakLocalizationUniversalPrinciple_of_coherent_and_presentations
    W hCoherent
      ((higherStoredTriangleCorrectionPrinciple_iff_coherentPresentationPrinciple
        (W := W) (uH := uH) (vH := vH)).mp hCorrections)

/-!
The coherent-replacement frontier now has an exact correction form:

```text
stored objectwise triangle family
        +
pointwise target automorphisms c_X
        +
corrected modification naturality
        |
        v
coherent arbitrary presentation
        <->
invertible modification triangle.
```

The identity correction is special:

```text
identity correction solves
        <->
stored family itself is modification-natural.
```

Therefore failure of stored-family naturality means only that the identity
correction fails.  The true general obstruction is stronger:

```text
no pointwise target-side correction solves the corrected naturality equation.
```

This is exactly the v2.25 coherent-presentation obstruction and exactly the v2.22
modification-triangle obstruction.  The remaining problem is now an explicit
nonabelian correction-equation existence problem rather than a vague search over
unrelated replacement triangles.
-/

end KUOS.DependentOriginationStoredTriangleCorrectionV2_26
