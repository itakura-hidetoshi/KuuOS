import KUOS.DependentOriginationStoredTriangleCorrectionV2_26

namespace KUOS.DependentOriginationStoredTriangleCorrectionTorsorV2_27

open CategoryTheory
open KUOS.DependentOriginationHigherLocalizationInterfaceV2_10
open KUOS.DependentOriginationWeakHigherLocalizationUniversalPropertyV2_18
open KUOS.DependentOriginationCoherentWeakHigherLocalizationV2_19
open KUOS.DependentOriginationStoredTriangleCorrectionV2_26

open scoped CategoryTheory.Pseudofunctor.StrongTrans

universe u v uH vH

/-!
# Stored triangle correction torsor v2.27

The v2.26 layer turns arbitrary coherent replacement into an explicit
nonabelian correction equation relative to the stored v2.18 triangle family.
It settles the existence question exactly:

```text
some stored-family correction exists
        <->
some coherent replacement exists
        <->
some invertible modification triangle exists.
```

This file studies the *space of all solutions* once one solution is present.
For a fixed factor morphism `alpha`, let

```text
A = restrict(alpha.hom) ≫ K.comparison,
B = H.comparison.
```

Every correction corresponds by v2.26 to an isomorphism `A ≅ B`.  Given two
corrections `C,D`, their quotient

```text
(E C)⁻¹ ≪≫ (E D) : B ≅ B
```

is therefore an invertible modification automorphism of the target StrongTrans
`B`.  Conversely, any automorphism `g : B ≅ B` acts on a correction by
postcomposition.

The main result is that the correction solution space, whenever inhabited, is a
right torsor under invertible modification automorphisms of `H.comparison`.
Consequently the higher problem separates cleanly into two independent layers:

* **existence**: does the correction equation have a solution?;
* **rigidity**: once a solution exists, are target modification automorphisms
  trivial enough to make the solution unique?

No correction existence or rigidity theorem is asserted unconditionally.  No
new axiom, strictification principle, additive linearization of 2-cells, or
ordinary-localization substitute is introduced.
-/

variable {Context : Type u} [Category.{v} Context]
variable (W : MorphismProperty Context)

/-- The invertible target modification measuring the difference between two
solutions of the stored-triangle correction equation. -/
def storedTriangleCorrectionDifference
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    {H K : HigherLocalizationFactorization (W := W) R}
    {alpha : HigherLocalizationFactorMorphism (W := W) H K}
    (C D : StoredTriangleTargetCorrection (W := W) alpha) :
    H.comparison ≅ H.comparison :=
  ((storedTriangleTargetCorrectionEquivIso (W := W) alpha) C).symm.trans
    ((storedTriangleTargetCorrectionEquivIso (W := W) alpha) D)

/-- Right action of a target invertible modification on a correction solution.

At the modification-triangle level this is simply postcomposition
`E(C) ≪≫ g`; v2.26 transports the result back to a correction. -/
def storedTriangleCorrectionAct
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    {H K : HigherLocalizationFactorization (W := W) R}
    {alpha : HigherLocalizationFactorMorphism (W := W) H K}
    (C : StoredTriangleTargetCorrection (W := W) alpha)
    (g : H.comparison ≅ H.comparison) :
    StoredTriangleTargetCorrection (W := W) alpha :=
  (storedTriangleTargetCorrectionEquivIso (W := W) alpha).symm
    (((storedTriangleTargetCorrectionEquivIso (W := W) alpha) C).trans g)

/-- The target action has the expected identity law. -/
theorem storedTriangleCorrectionAct_refl
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    {H K : HigherLocalizationFactorization (W := W) R}
    {alpha : HigherLocalizationFactorMorphism (W := W) H K}
    (C : StoredTriangleTargetCorrection (W := W) alpha) :
    storedTriangleCorrectionAct (W := W) C (Iso.refl _) = C := by
  apply (storedTriangleTargetCorrectionEquivIso (W := W) alpha).injective
  apply Iso.ext
  simp [storedTriangleCorrectionAct]

/-- The target action is associative with composition of invertible
modifications. -/
theorem storedTriangleCorrectionAct_assoc
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    {H K : HigherLocalizationFactorization (W := W) R}
    {alpha : HigherLocalizationFactorMorphism (W := W) H K}
    (C : StoredTriangleTargetCorrection (W := W) alpha)
    (g h : H.comparison ≅ H.comparison) :
    storedTriangleCorrectionAct (W := W)
        (storedTriangleCorrectionAct (W := W) C g) h =
      storedTriangleCorrectionAct (W := W) C (g.trans h) := by
  apply (storedTriangleTargetCorrectionEquivIso (W := W) alpha).injective
  apply Iso.ext
  simp [storedTriangleCorrectionAct, Category.assoc]

/-- A correction has trivial difference from itself. -/
theorem storedTriangleCorrectionDifference_self
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    {H K : HigherLocalizationFactorization (W := W) R}
    {alpha : HigherLocalizationFactorMorphism (W := W) H K}
    (C : StoredTriangleTargetCorrection (W := W) alpha) :
    storedTriangleCorrectionDifference (W := W) C C = Iso.refl _ := by
  apply Iso.ext
  simp [storedTriangleCorrectionDifference]

/-- Reversing the pair of corrections inverts their difference. -/
theorem storedTriangleCorrectionDifference_symm
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    {H K : HigherLocalizationFactorization (W := W) R}
    {alpha : HigherLocalizationFactorMorphism (W := W) H K}
    (C D : StoredTriangleTargetCorrection (W := W) alpha) :
    (storedTriangleCorrectionDifference (W := W) C D).symm =
      storedTriangleCorrectionDifference (W := W) D C := by
  apply Iso.ext
  rfl

/-- Differences satisfy the cocycle law.  This is the nonabelian replacement
for subtraction of two correction solutions. -/
theorem storedTriangleCorrectionDifference_trans
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    {H K : HigherLocalizationFactorization (W := W) R}
    {alpha : HigherLocalizationFactorMorphism (W := W) H K}
    (C D E : StoredTriangleTargetCorrection (W := W) alpha) :
    (storedTriangleCorrectionDifference (W := W) C D).trans
        (storedTriangleCorrectionDifference (W := W) D E) =
      storedTriangleCorrectionDifference (W := W) C E := by
  apply Iso.ext
  simp [storedTriangleCorrectionDifference, Category.assoc]

/-- Acting by an automorphism produces exactly that automorphism as the
correction difference.  This is freeness/transitivity in one direction. -/
theorem storedTriangleCorrectionDifference_act
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    {H K : HigherLocalizationFactorization (W := W) R}
    {alpha : HigherLocalizationFactorMorphism (W := W) H K}
    (C : StoredTriangleTargetCorrection (W := W) alpha)
    (g : H.comparison ≅ H.comparison) :
    storedTriangleCorrectionDifference (W := W) C
        (storedTriangleCorrectionAct (W := W) C g) = g := by
  apply Iso.ext
  simp [storedTriangleCorrectionDifference, storedTriangleCorrectionAct,
    Category.assoc]

/-- Acting on `C` by its difference to `D` recovers `D`.  This is the converse
freeness/transitivity statement. -/
theorem storedTriangleCorrectionAct_difference
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    {H K : HigherLocalizationFactorization (W := W) R}
    {alpha : HigherLocalizationFactorMorphism (W := W) H K}
    (C D : StoredTriangleTargetCorrection (W := W) alpha) :
    storedTriangleCorrectionAct (W := W) C
        (storedTriangleCorrectionDifference (W := W) C D) = D := by
  apply (storedTriangleTargetCorrectionEquivIso (W := W) alpha).injective
  apply Iso.ext
  simp [storedTriangleCorrectionAct, storedTriangleCorrectionDifference,
    Category.assoc]

/-- Once a base correction is chosen, all correction solutions are exactly the
invertible modification automorphisms of the target comparison StrongTrans.

This is the precise torsor classification. -/
def storedTriangleCorrectionTorsorEquiv
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    {H K : HigherLocalizationFactorization (W := W) R}
    {alpha : HigherLocalizationFactorMorphism (W := W) H K}
    (C0 : StoredTriangleTargetCorrection (W := W) alpha) :
    StoredTriangleTargetCorrection (W := W) alpha ≃
      (H.comparison ≅ H.comparison) where
  toFun := storedTriangleCorrectionDifference (W := W) C0
  invFun := storedTriangleCorrectionAct (W := W) C0
  left_inv := storedTriangleCorrectionAct_difference (W := W) C0
  right_inv := storedTriangleCorrectionDifference_act (W := W) C0

@[simp] theorem storedTriangleCorrectionTorsorEquiv_apply
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    {H K : HigherLocalizationFactorization (W := W) R}
    {alpha : HigherLocalizationFactorMorphism (W := W) H K}
    (C0 C : StoredTriangleTargetCorrection (W := W) alpha) :
    storedTriangleCorrectionTorsorEquiv (W := W) C0 C =
      storedTriangleCorrectionDifference (W := W) C0 C := by
  rfl

/-- With a base solution present, the correction type is subsingleton exactly
when the target has at most one invertible modification automorphism. -/
theorem subsingleton_storedTriangleCorrection_iff_targetAutomorphism
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    {H K : HigherLocalizationFactorization (W := W) R}
    {alpha : HigherLocalizationFactorMorphism (W := W) H K}
    (C0 : StoredTriangleTargetCorrection (W := W) alpha) :
    Subsingleton (StoredTriangleTargetCorrection (W := W) alpha) ↔
      Subsingleton (H.comparison ≅ H.comparison) := by
  constructor
  · intro hCorrection
    constructor
    intro g h
    let E := storedTriangleCorrectionTorsorEquiv (W := W) C0
    exact E.symm.injective (hCorrection.elim (E.symm g) (E.symm h))
  · intro hAutomorphism
    constructor
    intro C D
    let E := storedTriangleCorrectionTorsorEquiv (W := W) C0
    exact E.injective (hAutomorphism.elim (E C) (E D))

/-- A factor has a unique correction solution when the correction type is both
inhabited and subsingleton. -/
def HasUniqueStoredTriangleTargetCorrection
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    {H K : HigherLocalizationFactorization (W := W) R}
    (alpha : HigherLocalizationFactorMorphism (W := W) H K) : Prop :=
  Nonempty (StoredTriangleTargetCorrection (W := W) alpha) ∧
    Subsingleton (StoredTriangleTargetCorrection (W := W) alpha)

/-- Given one correction, uniqueness is exactly target modification rigidity. -/
theorem hasUniqueStoredTriangleTargetCorrection_iff_targetAutomorphismSubsingleton
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    {H K : HigherLocalizationFactorization (W := W) R}
    {alpha : HigherLocalizationFactorMorphism (W := W) H K}
    (C0 : StoredTriangleTargetCorrection (W := W) alpha) :
    HasUniqueStoredTriangleTargetCorrection (W := W) alpha ↔
      Subsingleton (H.comparison ≅ H.comparison) := by
  constructor
  · rintro ⟨_, hSubsingleton⟩
    exact
      (subsingleton_storedTriangleCorrection_iff_targetAutomorphism
        (W := W) C0).mp hSubsingleton
  · intro hRigid
    exact ⟨⟨C0⟩,
      (subsingleton_storedTriangleCorrection_iff_targetAutomorphism
        (W := W) C0).mpr hRigid⟩

/-- Uniform target-comparison rigidity for all v2.18 factor morphisms into one
chosen coherent universal datum. -/
def HigherFactorComparisonAutomorphismRigidity
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) : Prop :=
  ∀ (H : HigherLocalizationFactorization (W := W) R)
    (_alpha : HigherLocalizationFactorMorphism (W := W) H U.chosen),
    Subsingleton (H.comparison ≅ H.comparison)

/-- Uniform existence-and-uniqueness of stored-triangle corrections. -/
def HigherStoredTriangleTargetCorrectionUniqueLifting
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) : Prop :=
  ∀ (H : HigherLocalizationFactorization (W := W) R)
    (alpha : HigherLocalizationFactorMorphism (W := W) H U.chosen),
    HasUniqueStoredTriangleTargetCorrection (W := W) alpha

/-- Uniform unique correction lifting splits exactly into the already-known
existence problem plus an independent target-automorphism rigidity problem. -/
theorem higherUniqueStoredTriangleCorrectionLifting_iff_existence_and_rigidity
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    HigherStoredTriangleTargetCorrectionUniqueLifting (W := W) U ↔
      HigherStoredTriangleTargetCorrectionLifting (W := W) U ∧
        HigherFactorComparisonAutomorphismRigidity (W := W) U := by
  constructor
  · intro hUnique
    constructor
    · intro H alpha
      exact (hUnique H alpha).1
    · intro H alpha
      rcases (hUnique H alpha).1 with ⟨C0⟩
      exact
        (subsingleton_storedTriangleCorrection_iff_targetAutomorphism
          (W := W) C0).mp (hUnique H alpha).2
  · rintro ⟨hExist, hRigid⟩ H alpha
    rcases hExist H alpha with ⟨C0⟩
    exact ⟨⟨C0⟩,
      (subsingleton_storedTriangleCorrection_iff_targetAutomorphism
        (W := W) C0).mpr (hRigid H alpha)⟩

/-- Explicit failure of target-comparison rigidity. -/
def HigherFactorComparisonAutomorphismNonRigidity
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) : Prop :=
  ∃ (H : HigherLocalizationFactorization (W := W) R)
    (alpha : HigherLocalizationFactorMorphism (W := W) H U.chosen),
    ¬ Subsingleton (H.comparison ≅ H.comparison)

/-- Uniform target rigidity is exactly absence of its explicit non-rigidity
obstruction. -/
theorem higherFactorComparisonAutomorphismRigidity_iff_no_nonRigidity
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    HigherFactorComparisonAutomorphismRigidity (W := W) U ↔
      ¬ HigherFactorComparisonAutomorphismNonRigidity (W := W) U := by
  classical
  constructor
  · intro hRigid hNonRigid
    rcases hNonRigid with ⟨H, alpha, hNot⟩
    exact hNot (hRigid H alpha)
  · intro hNoNonRigid H alpha
    by_contra hNot
    exact hNoNonRigid ⟨H, alpha, hNot⟩

/-- Uniform unique solvability is equivalently simultaneous absence of the
v2.26 existence obstruction and the new target-automorphism rigidity
obstruction. -/
theorem higherUniqueStoredTriangleCorrectionLifting_iff_no_two_obstructions
    {R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH)}
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R) :
    HigherStoredTriangleTargetCorrectionUniqueLifting (W := W) U ↔
      (¬ HigherStoredTriangleTargetCorrectionObstruction (W := W) U) ∧
        (¬ HigherFactorComparisonAutomorphismNonRigidity (W := W) U) := by
  rw [higherUniqueStoredTriangleCorrectionLifting_iff_existence_and_rigidity
    (W := W) U]
  rw [higherStoredTriangleCorrectionLifting_iff_no_obstruction (W := W) U]
  rw [higherFactorComparisonAutomorphismRigidity_iff_no_nonRigidity (W := W) U]

/-- Global target-comparison rigidity principle.  This is an explicit
proposition, not an axiom. -/
def HigherFactorComparisonAutomorphismRigidityPrinciple : Prop :=
  ∀ (R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH))
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R),
    HigherFactorComparisonAutomorphismRigidity (W := W) U

/-- Global existence-and-uniqueness principle for stored-triangle corrections. -/
def HigherStoredTriangleTargetCorrectionUniquePrinciple : Prop :=
  ∀ (R : RawHigherContextualSystem (Context := Context) (uH := uH) (vH := vH))
    (U : CoherentWeakHigherLocalizationUniversalProperty (W := W) R),
    HigherStoredTriangleTargetCorrectionUniqueLifting (W := W) U

/-- The global unique-correction principle decomposes exactly into the v2.26
global correction-existence principle and the independent global rigidity
principle. -/
theorem higherUniqueStoredTriangleCorrectionPrinciple_iff_correction_and_rigidity :
    HigherStoredTriangleTargetCorrectionUniquePrinciple
        (W := W) (uH := uH) (vH := vH) ↔
      HigherStoredTriangleTargetCorrectionPrinciple
          (W := W) (uH := uH) (vH := vH) ∧
        HigherFactorComparisonAutomorphismRigidityPrinciple
          (W := W) (uH := uH) (vH := vH) := by
  constructor
  · intro hUnique
    constructor
    · intro R U
      exact
        (higherUniqueStoredTriangleCorrectionLifting_iff_existence_and_rigidity
          (W := W) U).mp (hUnique R U) |>.1
    · intro R U
      exact
        (higherUniqueStoredTriangleCorrectionLifting_iff_existence_and_rigidity
          (W := W) U).mp (hUnique R U) |>.2
  · rintro ⟨hCorrection, hRigidity⟩ R U
    exact
      (higherUniqueStoredTriangleCorrectionLifting_iff_existence_and_rigidity
        (W := W) U).mpr ⟨hCorrection R U, hRigidity R U⟩

/-!
The correction frontier is now split into existence and moduli/rigidity:

```text
correction equation has one solution C₀
        |
        v
all solutions form a right torsor under
Iso(H.comparison, H.comparison)
```

For any two solutions `C,D`, the canonical difference satisfies

```text
diff(C,C) = 1,
diff(C,D)⁻¹ = diff(D,C),
diff(C,D) · diff(D,E) = diff(C,E).
```

Thus the higher localization problem has two logically independent failure
modes:

```text
existence obstruction:
    no correction solution exists;

rigidity obstruction:
    target comparison admits nontrivial invertible modification automorphisms,
    so an existing correction need not be unique.
```

Only existence is required for the v2.18 weak higher-localization universal
property developed earlier.  The new rigidity layer does not strengthen that
existence claim; it classifies the residual moduli of coherent corrections once
existence is available.
-/

end KUOS.DependentOriginationStoredTriangleCorrectionTorsorV2_27