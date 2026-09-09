import KUOS.DependentOriginationStoredTriangleCorrectionTorsorV2_27

namespace KUOS.DependentOriginationComparisonAutomorphismSectionsV2_28

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationWeakHigherLocalizationUniversalPropertyV2_18
open KUOS.DependentOriginationCoherentWeakHigherLocalizationV2_19
open KUOS.DependentOriginationStoredTriangleCorrectionV2_26
open KUOS.DependentOriginationStoredTriangleCorrectionTorsorV2_27

open scoped CategoryTheory.Pseudofunctor.StrongTrans

universe u v uH vH

/-!
# Comparison automorphism sections v2.28

The v2.27 layer separates correction existence from correction rigidity.  Once
one correction exists, the full correction space is a right torsor under
invertible modification automorphisms of the target comparison StrongTrans
`H.comparison`.  Thus the new rigidity question is intrinsic:

```text
how many invertible modifications H.comparison ≅ H.comparison exist?
```

This file gives that question an exact objectwise normal form.

A comparison-automorphism section is an arbitrary family of objectwise Cat
self-isomorphisms of `H.comparison.app X`, subject only to the modification
naturality equation.  Pinned Mathlib's `Pseudofunctor.StrongTrans.isoMk`
assembles such a coherent family into an invertible modification, and every
invertible modification evaluates to such a family.  Hence we obtain a data-level
equivalence

```text
coherent objectwise automorphism sections
        ≃
invertible modifications H.comparison ≅ H.comparison.
```

Because the identity section always exists, non-rigidity has an exact positive
form: there exists a coherent section different from the identity section.
This identifies the v2.27 rigidity obstruction as a genuine coherent-section
existence problem rather than a vague failure of uniqueness.

Finally, pointwise automorphism rigidity is isolated as a strong sufficient
criterion: if every objectwise Cat self-isomorphism type is subsingleton, then
no nontrivial coherent section can exist.  The converse is deliberately not
claimed; arrowwise coherence may kill nontrivial objectwise automorphisms even
when they exist separately.

No pointwise rigidity, global rigidity, correction existence, strictification,
or weak higher-localization existence theorem is asserted unconditionally.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- A coherent objectwise section presenting an invertible modification
automorphism of `H.comparison`. -/
@[ext]
structure FactorComparisonAutomorphismSection
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (H : HigherLocalizationFactorization (W := W) R) where
  component : ∀ X : Context,
    H.comparison.app (.mk X) ≅ H.comparison.app (.mk X)
  naturality : ∀ {X Y : Context} (f : X ⟶ Y),
    (restrictHigherLocalizedSystem W H.lift).map f.toLoc ◁
          (component Y).hom ≫
        (H.comparison.naturality f.toLoc).hom =
      (H.comparison.naturality f.toLoc).hom ≫
        (component X).hom ▷ R.map f.toLoc

/-- Evaluate an invertible target modification at one raw context object. -/
def factorComparisonAutomorphismComponentIso
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    {H : HigherLocalizationFactorization (W := W) R}
    (g : H.comparison ≅ H.comparison)
    (X : Context) :
    H.comparison.app (.mk X) ≅ H.comparison.app (.mk X) where
  hom := g.hom.as.app (.mk X)
  inv := g.inv.as.app (.mk X)
  hom_inv_id := by
    have h := congrArg (fun m => m.as.app (.mk X)) g.hom_inv_id
    exact h
  inv_hom_id := by
    have h := congrArg (fun m => m.as.app (.mk X)) g.inv_hom_id
    exact h

/-- Extract the coherent objectwise automorphism section carried by an actual
invertible modification. -/
def factorComparisonAutomorphismSectionOfIso
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    {H : HigherLocalizationFactorization (W := W) R}
    (g : H.comparison ≅ H.comparison) :
    FactorComparisonAutomorphismSection (W := W) H where
  component X := factorComparisonAutomorphismComponentIso (W := W) g X
  naturality f := by
    simpa [factorComparisonAutomorphismComponentIso] using g.hom.as.naturality f.toLoc

/-- Assemble a coherent objectwise automorphism section into the corresponding
invertible target modification. -/
def factorComparisonAutomorphismIsoOfSection
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    {H : HigherLocalizationFactorization (W := W) R}
    (P : FactorComparisonAutomorphismSection (W := W) H) :
    H.comparison ≅ H.comparison := by
  refine Pseudofunctor.StrongTrans.isoMk (fun X => P.component X.as) ?_
  intro X Y f
  simpa using P.naturality f.as

/-- Extracting after assembly recovers the original coherent section. -/
theorem sectionOfIso_ofSection
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    {H : HigherLocalizationFactorization (W := W) R}
    (P : FactorComparisonAutomorphismSection (W := W) H) :
    factorComparisonAutomorphismSectionOfIso
        (W := W) (factorComparisonAutomorphismIsoOfSection (W := W) P) = P := by
  ext X
  apply Iso.ext
  rfl

/-- Reassembling the section extracted from a target modification recovers that
modification. -/
theorem isoOfSection_ofIso
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    {H : HigherLocalizationFactorization (W := W) R}
    (g : H.comparison ≅ H.comparison) :
    factorComparisonAutomorphismIsoOfSection
        (W := W) (factorComparisonAutomorphismSectionOfIso (W := W) g) = g := by
  apply Iso.ext
  apply Pseudofunctor.StrongTrans.homCategory.ext
  intro X
  rfl

/-- Exact data-level equivalence between coherent objectwise automorphism
sections and invertible modification automorphisms of `H.comparison`. -/
def factorComparisonAutomorphismSectionEquivIso
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (H : HigherLocalizationFactorization (W := W) R) :
    FactorComparisonAutomorphismSection (W := W) H ≃
      (H.comparison ≅ H.comparison) where
  toFun := factorComparisonAutomorphismIsoOfSection (W := W)
  invFun := factorComparisonAutomorphismSectionOfIso (W := W)
  left_inv := sectionOfIso_ofSection (W := W)
  right_inv := isoOfSection_ofIso (W := W)

/-- The identity coherent automorphism section.  It is obtained from the
identity invertible modification, so coherence is inherited rather than
reproved separately. -/
def identityFactorComparisonAutomorphismSection
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (H : HigherLocalizationFactorization (W := W) R) :
    FactorComparisonAutomorphismSection (W := W) H :=
  factorComparisonAutomorphismSectionOfIso (W := W) (Iso.refl H.comparison)

@[simp] theorem identityFactorComparisonAutomorphismSection_component
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (H : HigherLocalizationFactorization (W := W) R)
    (X : Context) :
    (identityFactorComparisonAutomorphismSection (W := W) H).component X =
      Iso.refl _ := by
  apply Iso.ext
  rfl

/-- Target modification rigidity is exactly subsingleton rigidity of coherent
objectwise automorphism sections. -/
theorem subsingleton_factorComparisonAutomorphismIso_iff_section
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (H : HigherLocalizationFactorization (W := W) R) :
    Subsingleton (H.comparison ≅ H.comparison) ↔
      Subsingleton (FactorComparisonAutomorphismSection (W := W) H) := by
  constructor
  · intro hIso
    constructor
    intro P Q
    let E := factorComparisonAutomorphismSectionEquivIso (W := W) H
    exact E.injective (@Subsingleton.elim _ hIso (E P) (E Q))
  · intro hSection
    constructor
    intro g h
    let E := factorComparisonAutomorphismSectionEquivIso (W := W) H
    exact E.symm.injective
      (@Subsingleton.elim _ hSection (E.symm g) (E.symm h))

/-- A positive witness of target non-rigidity: a coherent automorphism section
that is not the identity section. -/
def HasNontrivialFactorComparisonAutomorphismSection
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (H : HigherLocalizationFactorization (W := W) R) : Prop :=
  ∃ P : FactorComparisonAutomorphismSection (W := W) H,
    P ≠ identityFactorComparisonAutomorphismSection (W := W) H

/-- Since the identity section always exists, failure of section subsingleton
rigidity is exactly existence of a nonidentity coherent section. -/
theorem not_subsingleton_section_iff_hasNontrivialSection
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (H : HigherLocalizationFactorization (W := W) R) :
    (¬ Subsingleton (FactorComparisonAutomorphismSection (W := W) H)) ↔
      HasNontrivialFactorComparisonAutomorphismSection (W := W) H := by
  classical
  constructor
  · intro hNotSub
    by_contra hNoWitness
    apply hNotSub
    constructor
    intro P Q
    have hP : P = identityFactorComparisonAutomorphismSection (W := W) H := by
      by_contra hPne
      exact hNoWitness ⟨P, hPne⟩
    have hQ : Q = identityFactorComparisonAutomorphismSection (W := W) H := by
      by_contra hQne
      exact hNoWitness ⟨Q, hQne⟩
    exact hP.trans hQ.symm
  · rintro ⟨P, hP⟩ hSub
    exact hP
      (@Subsingleton.elim _ hSub P
        (identityFactorComparisonAutomorphismSection (W := W) H))

/-- Exact positive normal form for the v2.27 target non-rigidity condition. -/
theorem not_subsingleton_factorComparisonAutomorphismIso_iff_nontrivialSection
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (H : HigherLocalizationFactorization (W := W) R) :
    (¬ Subsingleton (H.comparison ≅ H.comparison)) ↔
      HasNontrivialFactorComparisonAutomorphismSection (W := W) H := by
  rw [subsingleton_factorComparisonAutomorphismIso_iff_section (W := W) H]
  exact not_subsingleton_section_iff_hasNontrivialSection (W := W) H

/-- Strong pointwise rigidity: each objectwise comparison functor has at most
one Cat self-isomorphism.  This is sufficient, but not asserted necessary, for
global modification rigidity. -/
def FactorComparisonPointwiseAutomorphismRigidity
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (H : HigherLocalizationFactorization (W := W) R) : Prop :=
  ∀ X : Context,
    Subsingleton (H.comparison.app (.mk X) ≅ H.comparison.app (.mk X))

/-- Pointwise automorphism rigidity forces coherent-section rigidity. -/
theorem subsingleton_section_of_pointwiseAutomorphismRigidity
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (H : HigherLocalizationFactorization (W := W) R)
    (hPointwise : FactorComparisonPointwiseAutomorphismRigidity (W := W) H) :
    Subsingleton (FactorComparisonAutomorphismSection (W := W) H) := by
  constructor
  intro P Q
  ext X
  exact @Subsingleton.elim _ (hPointwise X) (P.component X) (Q.component X)

/-- Therefore pointwise automorphism rigidity is a sufficient criterion for
v2.27 target modification rigidity. -/
theorem subsingleton_factorComparisonAutomorphismIso_of_pointwiseRigidity
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (H : HigherLocalizationFactorization (W := W) R)
    (hPointwise : FactorComparisonPointwiseAutomorphismRigidity (W := W) H) :
    Subsingleton (H.comparison ≅ H.comparison) :=
  (subsingleton_factorComparisonAutomorphismIso_iff_section (W := W) H).mpr
    (subsingleton_section_of_pointwiseAutomorphismRigidity W H hPointwise)

/-- Uniform coherent-section rigidity for every factor morphism into one chosen
coherent universal datum. -/
def HigherFactorComparisonAutomorphismSectionRigidity
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) : Prop :=
  ∀ (H : HigherLocalizationFactorization (W := W) R)
    (_alpha : HigherLocalizationFactorMorphism (W := W) H U.chosen),
    Subsingleton (FactorComparisonAutomorphismSection (W := W) H)

/-- Uniform section rigidity is exactly the v2.27 target modification rigidity. -/
theorem higherFactorComparisonSectionRigidity_iff_targetRigidity
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    HigherFactorComparisonAutomorphismSectionRigidity (W := W) U ↔
      HigherFactorComparisonAutomorphismRigidity (W := W) U := by
  constructor
  · intro hSection H alpha
    exact
      (subsingleton_factorComparisonAutomorphismIso_iff_section
        (W := W) H).mpr (hSection H alpha)
  · intro hRigid H alpha
    exact
      (subsingleton_factorComparisonAutomorphismIso_iff_section
        (W := W) H).mp (hRigid H alpha)

/-- Uniform positive non-rigidity: some factor admits a nonidentity coherent
automorphism section. -/
def HigherFactorComparisonNontrivialAutomorphismSection
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) : Prop :=
  ∃ (H : HigherLocalizationFactorization (W := W) R)
    (alpha : HigherLocalizationFactorMorphism (W := W) H U.chosen),
    HasNontrivialFactorComparisonAutomorphismSection (W := W) H

/-- The v2.27 non-rigidity obstruction is exactly existence of a nonidentity
coherent automorphism section. -/
theorem higherFactorComparisonNonRigidity_iff_nontrivialSection
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    HigherFactorComparisonAutomorphismNonRigidity (W := W) U ↔
      HigherFactorComparisonNontrivialAutomorphismSection (W := W) U := by
  constructor
  · rintro ⟨H, alpha, hNonRigid⟩
    exact ⟨H, alpha,
      (not_subsingleton_factorComparisonAutomorphismIso_iff_nontrivialSection
        (W := W) H).mp hNonRigid⟩
  · rintro ⟨H, alpha, hSection⟩
    exact ⟨H, alpha,
      (not_subsingleton_factorComparisonAutomorphismIso_iff_nontrivialSection
        (W := W) H).mpr hSection⟩

/-- Uniform pointwise automorphism rigidity. -/
def HigherFactorComparisonPointwiseAutomorphismRigidity
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) : Prop :=
  ∀ (H : HigherLocalizationFactorization (W := W) R)
    (_alpha : HigherLocalizationFactorMorphism (W := W) H U.chosen),
    FactorComparisonPointwiseAutomorphismRigidity (W := W) H

/-- Pointwise rigidity uniformly implies target modification rigidity. -/
theorem higherFactorComparisonRigidity_of_pointwiseRigidity
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hPointwise : HigherFactorComparisonPointwiseAutomorphismRigidity (W := W) U) :
    HigherFactorComparisonAutomorphismRigidity (W := W) U := by
  intro H alpha
  exact
    subsingleton_factorComparisonAutomorphismIso_of_pointwiseRigidity
      W H (hPointwise H alpha)

/-- Correction existence plus uniform pointwise target rigidity gives uniform
existence-and-uniqueness of corrections. -/
theorem higherUniqueStoredTriangleCorrectionLifting_of_correction_and_pointwiseRigidity
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R)
    (hCorrection : HigherStoredTriangleTargetCorrectionLifting (W := W) U)
    (hPointwise : HigherFactorComparisonPointwiseAutomorphismRigidity (W := W) U) :
    HigherStoredTriangleTargetCorrectionUniqueLifting (W := W) U :=
  (higherUniqueStoredTriangleCorrectionLifting_iff_existence_and_rigidity
    (W := W) U).mpr
      ⟨hCorrection,
        higherFactorComparisonRigidity_of_pointwiseRigidity W U hPointwise⟩

/-- Global coherent-section rigidity principle. -/
def HigherFactorComparisonAutomorphismSectionRigidityPrinciple : Prop :=
  ∀ (R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH))
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R),
    HigherFactorComparisonAutomorphismSectionRigidity (W := W) U

/-- Global pointwise automorphism rigidity principle.  This is an explicit
proposition, not an axiom. -/
def HigherFactorComparisonPointwiseAutomorphismRigidityPrinciple : Prop :=
  ∀ (R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH))
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R),
    HigherFactorComparisonPointwiseAutomorphismRigidity (W := W) U

/-- Global coherent-section rigidity is exactly the v2.27 global target
modification rigidity principle. -/
theorem higherFactorComparisonSectionRigidityPrinciple_iff_targetRigidityPrinciple :
    HigherFactorComparisonAutomorphismSectionRigidityPrinciple
        (W := W) (uH := uH) (vH := vH) ↔
      HigherFactorComparisonAutomorphismRigidityPrinciple
        (W := W) (uH := uH) (vH := vH) := by
  constructor
  · intro h R U
    exact
      (higherFactorComparisonSectionRigidity_iff_targetRigidity
        (W := W) U).mp (h R U)
  · intro h R U
    exact
      (higherFactorComparisonSectionRigidity_iff_targetRigidity
        (W := W) U).mpr (h R U)

/-- Global pointwise rigidity implies the global target modification rigidity
principle. -/
theorem higherFactorComparisonRigidityPrinciple_of_pointwiseRigidity
    (hPointwise : HigherFactorComparisonPointwiseAutomorphismRigidityPrinciple
      (W := W) (uH := uH) (vH := vH)) :
    HigherFactorComparisonAutomorphismRigidityPrinciple
      (W := W) (uH := uH) (vH := vH) := by
  intro R U
  exact higherFactorComparisonRigidity_of_pointwiseRigidity
    W U (hPointwise R U)

/-- Consequently, global correction existence plus global pointwise rigidity
implies the global unique-correction principle.  Both premises remain explicit
unproved propositions. -/
theorem higherUniqueStoredTriangleCorrectionPrinciple_of_correction_and_pointwiseRigidity
    (hCorrection : HigherStoredTriangleTargetCorrectionPrinciple
      (W := W) (uH := uH) (vH := vH))
    (hPointwise : HigherFactorComparisonPointwiseAutomorphismRigidityPrinciple
      (W := W) (uH := uH) (vH := vH)) :
    HigherStoredTriangleTargetCorrectionUniquePrinciple
      (W := W) (uH := uH) (vH := vH) := by
  intro R U
  exact
    higherUniqueStoredTriangleCorrectionLifting_of_correction_and_pointwiseRigidity
      W U (hCorrection R U) (hPointwise R U)

/-!
The rigidity frontier now has an exact coherent-section form:

```text
invertible modifications H.comparison ≅ H.comparison
        ≃
objectwise Cat automorphism families satisfying modification naturality.
```

The identity section is always present, so the v2.27 non-rigidity obstruction is
precisely

```text
there exists a coherent automorphism section different from identity.
```

A stronger objectwise criterion kills that obstruction:

```text
all objectwise Cat automorphism types are subsingletons
        |
        v
all coherent automorphism sections are equal
        |
        v
target modification rigidity.
```

The reverse arrow is not asserted: global naturality constraints can eliminate
nontrivial objectwise automorphisms without making the individual objectwise
automorphism types subsingletons.

Thus v2.26--v2.28 now separate three layers cleanly:

```text
correction existence,
correction moduli as a target-automorphism torsor,
rigidity as absence of nonidentity coherent automorphism sections.
```

None of these classifications supplies the still-open general correction
existence theorem or general weak higher-localization universal principle.
-/

end KUOS.DependentOriginationComparisonAutomorphismSectionsV2_28