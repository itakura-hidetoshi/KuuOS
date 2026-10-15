import KUOS.DependentOriginationC60KuuWitnessedSourceDiagramBeckChevalleyV5_287
import Mathlib.CategoryTheory.Grothendieck

namespace KUOS.DependentOriginationC60KuuWitnessedGrothendieckSourceEquivalenceV5_288

open CategoryTheory
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationGrayC60ThreeHomCategoriesV5_192
open KUOS.DependentOriginationGrayC60OriginalF55ThreeHomV5_192
open KUOS.DependentOriginationGrayC60F55SourcePhaseLockedAtlasV5_175
open KUOS.DependentOriginationGrayC60MixedBoundaryThreeHomV5_195
open KUOS.DependentOriginationGrayC60IntegralChainComplexV5_160
open KUOS.DependentOriginationC60FiniteAtlasCechCoherenceV5_221
open KUOS.DependentOriginationC60PhysicalCechCurvatureRepairV5_222
open KUOS.DependentOriginationC60KuuTwoActualFaceInterchangeV5_265
open KUOS.DependentOriginationC60KuuIndependentPhysicalFaceSiteSourceV5_274
open KUOS.DependentOriginationC60KuuCrossEdgePhysicalOverlapF47V5_277
open KUOS.DependentOriginationC60KuuWitnessedOverlapPathGrothendieckV5_278
open KUOS.DependentOriginationC60KuuWitnessedSourceDiagramBeckChevalleyV5_287
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.288 / F112 part 16 — true witnessed F47 source Grothendieck equivalence

F112/v5.278 built the ACTUAL finite, proof-carrying physical
C60-overlap path category and a complete original F47 mixed-source
Cat-valued diagram. F112/v5.287 proved that arbitrary independently
typed odd F42 face presentations of the same physical patches give
a genuine diagram-level NatIso on EVERY finite path, with a strict
three-presentation Cech cocycle and identity.

In the PINNED mathlib, Grothendieck.map sends that exact NatTrans
to a FUNCTOR on the corresponding genuine total categories. We
prove directly, with exact source typing:
  1. every original F69 witness-path base object and base arrow is
     unchanged by source re-presentation;
  2. the total-category functor COMMUTES STRICTLY with the true
     Grothendieck projection to the witnessed-overlap path base;
  3. exact self-identification and three-presentation cocycle are
     preserved at the level of ENTIRE total-category FUNCTORS;
  4. hence the true Grothendieck total categories for any two
     independent original F42 face-presentation families are
     ISOMORPHIC as Cat objects and EQUIVALENT as categories;
  5. full original F55 Delta nonlift and F68 signed north charge
     -5 still obstruct uncorrected source-side global descent.

This is NOT a functor from the entire original F69 partial order
to a hypothetical original F42/F54/F55 three-stack. Physical
overlap witnesses are not erased in the base. The F47 mixed
native-kernel quotient keeps Int x Int AND the independent ZMod2
phase, without equating old raw original F42/F54 expressions.
No new original F55 Delta, F77 phase inverse, global original
source stack effectivity, or flat original F68 vertex potential
is asserted.
-/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

section WitnessedF47TotalSourceEquivalence
variable {a b : D} {x y : E}
variable {n₁ n₂ m₁ m₂ : Nat}
variable {p₀ p₁ p₂ : Blocks a b} {q₀ q₁ q₂ : Blocks x y}
variable
  (t₁ : OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁)
  (t₂ : OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂)
variable
  {leftAfter : OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁}
  {rightAfter : OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂}
  (left : OriginalF45BracketTree.LocalRotation t₁ leftAfter)
  (right : OriginalF45BracketTree.LocalRotation t₂ rightAfter)

/-- The actual diagram-level original F42 re-presentation,
lifted via the PINNED mathlib Grothendieck.map construction
to the entire mixed-F47 source total category. -/
def c60F122WitnessedF47TotalSourceChange
    {n : Nat} (C : C60F108BothFaceContexts n)
    (P Q : (i : Fin n) → C60F112IndependentOddFacePair C i) :
    c60F112WitnessedF47Grothendieck t₁ t₂ left right C P ⥤
      c60F112WitnessedF47Grothendieck t₁ t₂ left right C Q :=
  Grothendieck.map
    (c60F121WitnessedF47DiagramSourceChange t₁ t₂ left right C P Q)

/-- Every object of the Grothendieck total category retains
the SAME genuine C60 witnessed physical-edge index in the base.
Only its independently chosen original F42/F54/F55 F47 fibre
presentation is changed. -/
theorem c60F122WitnessedF47TotalSourceChange_obj_base
    {n : Nat} (C : C60F108BothFaceContexts n)
    (P Q : (i : Fin n) → C60F112IndependentOddFacePair C i)
    (X : c60F112WitnessedF47Grothendieck t₁ t₂ left right C P) :
    (c60F122WitnessedF47TotalSourceChange
      t₁ t₂ left right C P Q).obj X |>.base = X.base := rfl

/-- Every total Hom retains its literal finite
proof-carrying physical overlap PATH as its base arrow.
No direct edge-to-edge Hom is added to original F69. -/
theorem c60F122WitnessedF47TotalSourceChange_map_base
    {n : Nat} (C : C60F108BothFaceContexts n)
    (P Q : (i : Fin n) → C60F112IndependentOddFacePair C i)
    {X Y : c60F112WitnessedF47Grothendieck t₁ t₂ left right C P}
    (f : X ⟶ Y) :
    ((c60F122WitnessedF47TotalSourceChange
      t₁ t₂ left right C P Q).map f).base = f.base := rfl

/-- The total source-change functor is STRICTLY over the
genuine finite-overlap path base, not over original F69:
the Grothendieck projection is unchanged as a functor. -/
theorem c60F122WitnessedF47TotalSourceChange_overBase
    {n : Nat} (C : C60F108BothFaceContexts n)
    (P Q : (i : Fin n) → C60F112IndependentOddFacePair C i) :
    c60F122WitnessedF47TotalSourceChange
        t₁ t₂ left right C P Q ⋙
      c60F112WitnessedF47TotalProjection t₁ t₂ left right C Q =
    c60F112WitnessedF47TotalProjection t₁ t₂ left right C P :=
  Grothendieck.functor_comp_forget

/-- Re-presenting original source labels by themselves is
IDENTITY of the actual total-category functor, not a
proposition about old original raw F42 cell equality. -/
theorem c60F122WitnessedF47TotalSourceChange_self
    {n : Nat} (C : C60F108BothFaceContexts n)
    (P : (i : Fin n) → C60F112IndependentOddFacePair C i) :
    c60F122WitnessedF47TotalSourceChange
      t₁ t₂ left right C P P =
      𝟭 (c60F112WitnessedF47Grothendieck t₁ t₂ left right C P) := by
  change Grothendieck.map
    (c60F121WitnessedF47DiagramSourceChange
      t₁ t₂ left right C P P) = _
  rw [c60F121WitnessedDiagramChange_self]
  exact Grothendieck.map_id_eq

/-- EXACT three independent original F42-presentation
Cech cocycle lifts to strict equality of WHOLE Grothendieck
total functors. The proof uses real diagram NatTrans
composition, not equality of original F42 raw face terms. -/
theorem c60F122WitnessedF47TotalSourceChange_cocycle
    {n : Nat} (C : C60F108BothFaceContexts n)
    (P Q R : (i : Fin n) → C60F112IndependentOddFacePair C i) :
    c60F122WitnessedF47TotalSourceChange
        t₁ t₂ left right C P Q ⋙
      c60F122WitnessedF47TotalSourceChange
        t₁ t₂ left right C Q R =
    c60F122WitnessedF47TotalSourceChange
        t₁ t₂ left right C P R := by
  let α := c60F121WitnessedF47DiagramSourceChange
    t₁ t₂ left right C P Q
  let β := c60F121WitnessedF47DiagramSourceChange
    t₁ t₂ left right C Q R
  calc
    _ = Grothendieck.map (α ≫ β) :=
      (Grothendieck.map_comp_eq α β).symm
    _ = Grothendieck.map
          (c60F121WitnessedF47DiagramSourceChange
            t₁ t₂ left right C P R) := by
          exact congrArg Grothendieck.map
            (c60F121WitnessedDiagramChange_cocycle
              t₁ t₂ left right C P Q R)

/-- The ACTUAL original F47 total categories of any two
independently presented physical face-source families are
ISOMORPHIC in Cat. The inverse is the true opposite
presentation change, with its two strict inverse identities
proved from the real source Cech cocycle and self-unit. -/
def c60F122WitnessedF47TotalCatIso
    {n : Nat} (C : C60F108BothFaceContexts n)
    (P Q : (i : Fin n) → C60F112IndependentOddFacePair C i) :
    Cat.of (c60F112WitnessedF47Grothendieck
      t₁ t₂ left right C P) ≅
      Cat.of (c60F112WitnessedF47Grothendieck
        t₁ t₂ left right C Q) where
  hom := (c60F122WitnessedF47TotalSourceChange
    t₁ t₂ left right C P Q).toCatHom
  inv := (c60F122WitnessedF47TotalSourceChange
    t₁ t₂ left right C Q P).toCatHom
  hom_inv_id := by
    apply Cat.Hom.ext
    simpa only [Cat.Hom.comp_toFunctor, Functor.toCatHom_toFunctor,
      Cat.Hom.id_toFunctor] using
      (c60F122WitnessedF47TotalSourceChange_cocycle
        t₁ t₂ left right C P Q P).trans
        (c60F122WitnessedF47TotalSourceChange_self
          t₁ t₂ left right C P)
  inv_hom_id := by
    apply Cat.Hom.ext
    simpa only [Cat.Hom.comp_toFunctor, Functor.toCatHom_toFunctor,
      Cat.Hom.id_toFunctor] using
      (c60F122WitnessedF47TotalSourceChange_cocycle
        t₁ t₂ left right C Q P Q).trans
        (c60F122WitnessedF47TotalSourceChange_self
          t₁ t₂ left right C Q)

/-- Therefore the genuine mixed-F47 Grothendieck total
categories are CATEGORICALLY EQUIVALENT, over the same
actual witnessed overlap path category, preserving both
integer charges and the separate original phase at their
F47 fibres. This follows from the genuine Cat isomorphism,
NOT from an invented raw original F42/F54/F55 equality. -/
def c60F122WitnessedF47TotalEquivalence
    {n : Nat} (C : C60F108BothFaceContexts n)
    (P Q : (i : Fin n) → C60F112IndependentOddFacePair C i) :
    c60F112WitnessedF47Grothendieck t₁ t₂ left right C P ≌
      c60F112WitnessedF47Grothendieck t₁ t₂ left right C Q :=
  Cat.equivOfIso
    (c60F122WitnessedF47TotalCatIso t₁ t₂ left right C P Q)

/-- This total categorical equivalence is compatible with
the EXACT source-projection map to each real physical-overlap
path witness. It cannot thereby imply effective descent in
the original F69 vertex/edge/face incidence category. -/
theorem c60F122WitnessedF47TotalEquivalence_overBase
    {n : Nat} (C : C60F108BothFaceContexts n)
    (P Q : (i : Fin n) → C60F112IndependentOddFacePair C i) :
    (c60F122WitnessedF47TotalEquivalence
      t₁ t₂ left right C P Q).functor ⋙
      c60F112WitnessedF47TotalProjection t₁ t₂ left right C Q =
    c60F112WitnessedF47TotalProjection t₁ t₂ left right C P :=
  c60F122WitnessedF47TotalSourceChange_overBase
    t₁ t₂ left right C P Q

/-- A verified source-diagram equivalence over physical
witnesses does NOT erase an original signed nonflat C60
curvature. The raw nine-constructor F55 Delta remains
non-liftable at any chosen genuine witnessed path endpoint. -/
theorem c60F122WitnessedF47Totals_curvedSourceObstruction
    {n : Nat} (C : C60F108BothFaceContexts n)
    (P Q : (i : Fin n) → C60F112IndependentOddFacePair C i)
    {i j : Fin n}
    (path : C60F112WitnessedOverlapPath C i j)
    (sigma : C60F67Atlas) :
    (c60F68PhysicalPatchCurvature t₁ t₂ left right sigma
      (Finsupp.single (.aroundVertex .north) (1 : ℤ))).charge.2 =
        (-5 : ℤ) ∧
    c60F68PhysicalPatchCurvature t₁ t₂ left right sigma ≠ 0 ∧
    (¬ ∃ vertexGauge :
        C60IntegralZeroChains →ₗ[ℤ] GradedThreeCell 0 0,
      c60F68AtlasEdgeCochain t₁ t₂ left right sigma =
        vertexGauge.comp c60IntegralBoundaryOne) ∧
    (¬ ∃ cell :
      OriginalF45BracketTree.DepthRotationRoute.PresentedCell
        (OriginalF45BracketTree.DepthRotationRoute.squareLeftFirst left right)
        (OriginalF45BracketTree.DepthRotationRoute.squareRightFirst left right),
      c60F44FaceThreeEval
        (c60F112CrossEdgeFrame t₁ t₂ left right C j (P j)).faceStep +
          c60F55SourceNative cell =
        c60F44OriginalF55Eval
          (c60F112CrossEdgeFrame t₁ t₂ left right C j (P j)).rotationStep) ∧
    (¬ ∃ cell :
      OriginalF45BracketTree.DepthRotationRoute.PresentedCell
        (OriginalF45BracketTree.DepthRotationRoute.squareLeftFirst left right)
        (OriginalF45BracketTree.DepthRotationRoute.squareRightFirst left right),
      c60F44FaceThreeEval
        (c60F112CrossEdgeFrame t₁ t₂ left right C j (Q j)).faceStep +
          c60F55SourceNative cell =
        c60F44OriginalF55Eval
          (c60F112CrossEdgeFrame t₁ t₂ left right C j (Q j)).rotationStep) := by
  rcases c60F112WitnessedF47Total_originalCurvatureObstruction
    t₁ t₂ left right C P sigma with ⟨hc, hn, hg⟩
  exact ⟨hc, hn, hg,
    c60F112WitnessedF47Path_originalF55Nonlift
      t₁ t₂ left right C P path,
    c60F112WitnessedF47Path_originalF55Nonlift
      t₁ t₂ left right C Q path⟩

#print axioms c60F122WitnessedF47TotalSourceChange_obj_base
#print axioms c60F122WitnessedF47TotalSourceChange_map_base
#print axioms c60F122WitnessedF47TotalSourceChange_overBase
#print axioms c60F122WitnessedF47TotalSourceChange_self
#print axioms c60F122WitnessedF47TotalSourceChange_cocycle
#print axioms c60F122WitnessedF47TotalCatIso
#print axioms c60F122WitnessedF47TotalEquivalence
#print axioms c60F122WitnessedF47TotalEquivalence_overBase
#print axioms c60F122WitnessedF47Totals_curvedSourceObstruction

end WitnessedF47TotalSourceEquivalence
end
end KUOS.DependentOriginationC60KuuWitnessedGrothendieckSourceEquivalenceV5_288
