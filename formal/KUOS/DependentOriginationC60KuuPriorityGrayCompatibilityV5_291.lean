import KUOS.DependentOriginationC60KuuNativeIncidenceCollarV5_291
import KUOS.DependentOriginationC60KuuLocalUniversalDescentV5_249
import KUOS.DependentOriginationGrayC60OriginalFaceHorizontalGrayCoherenceV5_199
import KUOS.DependentOriginationC60InterchangerStrictChargeQuotientV5_229

namespace KUOS.DependentOriginationC60KuuPriorityGrayCompatibilityV5_291

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayC60OriginalFaceHorizontalPresentationV5_199
open KUOS.DependentOriginationGrayC60OriginalFaceHorizontalThreeHomV5_199
open KUOS.DependentOriginationGrayC60OriginalFaceHorizontalGrayCoherenceV5_199
open KUOS.DependentOriginationC60InterchangerStrictChargeQuotientV5_229
open KUOS.DependentOriginationC60NativeExchangeCongruenceQuotientV5_231
open KUOS.DependentOriginationC60StrictChargeGlobularCalculusV5_232
open KUOS.DependentOriginationC60KuuReplacementInterchangeV5_248
open KUOS.DependentOriginationC60KuuLocalUniversalDescentV5_249

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.291 / F112 part 19 — Kuu-first, Gray-compatible source refinement

KUU is the PRIMARY interpretation: the verified F94/F95 local
replacement quotient preserves independent Int×Int charges,
and F96/F97 establish its real horizontal/vertical interchange.
We do NOT demand the obsolete Gray presentation to be rebuilt.

At the same time, Kuu must be a *lossless compatible extension*
for optional ORIGINAL Gray diagnostic information rather than
silently discarding independent ZMod2 phase. We therefore construct
a new KUU-FIRST SOURCE CATEGORY whose Hom consists of:
   (i) the REAL original F95 Kuu replacement-quotient Hom,
   (ii) the *separate* original F59 Gray ZMod2 phase residual.

Identities and composition are genuine Category laws, and the
original F42/F51 proof-relevant source maps into this new category
FAITHFULLY. The Kuu quotient is recovered by the FIRST projection.
The full original Gray evaluation is exactly RECONSTRUCTIBLE
from the Kuu charge quotient AND the independent phase coordinate.
Thus Kuu replaceability is permitted when original Gray phases
differ, but such differences remain available as explicit obstruction
data. No old F55 generator, vertex-edge fidelity or raw F69 3-stack
effectivity is asserted. This is a LOCAL Hom-level upper-compatible
construction, not a global equivalence of Gray and Kuu theories.
-/

/-- Kuu-priority objects retain the original, genuinely typed F42
presentation object without reducing it to an untyped Gray label. -/
structure C60F125KuuGrayTwo
    {a b : IcosahedralDart} (p q : Quiver.Path a b) where
  original : C60F51OriginalTwo p q

/-- Morphisms have PRIMARY Kuu F95 quotient 3-Hom and an
independent ZMod2 phase. No phase is lost by this construction. -/
abbrev C60F125KuuGrayHom
    {a b : IcosahedralDart} {p q : Quiver.Path a b}
    (X Y : C60F125KuuGrayTwo p q) :=
  ((c60F95LocalProjection p q).obj X.original ⟶
     (c60F95LocalProjection p q).obj Y.original) × ZMod 2

/-- A genuine category with original Kuu quotient composition
in the first component and native Gray phase addition in the second. -/
instance c60F125KuuGrayCategory
    {a b : IcosahedralDart} (p q : Quiver.Path a b) :
    Category (C60F125KuuGrayTwo p q) where
  Hom := C60F125KuuGrayHom
  id X := ⟨𝟙 _, 0⟩
  comp f g := ⟨f.1 ≫ g.1, f.2 + g.2⟩
  id_comp := by
    intro X Y f
    apply Prod.ext
    · exact Category.id_comp f.1
    · exact zero_add f.2
  comp_id := by
    intro X Y f
    apply Prod.ext
    · exact Category.comp_id f.1
    · exact add_zero f.2
  assoc := by
    intro W X Y Z f g h
    apply Prod.ext
    · exact Category.assoc f.1 g.1 h.1
    · exact add_assoc f.2 g.2 h.2

/-- The ordinary Kuu quotient is the PRIMARY projection.
This acts on the actual F95 Hom, not just on abstract charges. -/
def c60F125KuuPrimaryProjection
    {a b : IcosahedralDart} (p q : Quiver.Path a b) :
    C60F125KuuGrayTwo p q ⥤ C60F95LocalKuuQuotient p q where
  obj X := (c60F95LocalProjection p q).obj X.original
  map f := f.1
  map_id := by intro X; rfl
  map_comp := by intro X Y Z f g; rfl

/-- Actual original F51 three-arrows inject into the Kuu-first
category without erasing their independent Gray-phase witness. -/
def c60F125KuuFirstOriginalSource
    {a b : IcosahedralDart} (p q : Quiver.Path a b) :
    C60F51OriginalTwo p q ⥤ C60F125KuuGrayTwo p q where
  obj X := ⟨X⟩
  map := fun {_ _} f =>
    ⟨(c60F95LocalProjection p q).map f, (c60F51Eval f).phase⟩
  map_id := by
    intro X
    apply Prod.ext
    · exact (c60F95LocalProjection p q).map_id X
    · rfl
  map_comp := by
    intro X Y Z f g
    apply Prod.ext
    · exact (c60F95LocalProjection p q).map_comp f g
    · change (c60F51Eval (f ≫ g)).phase =
        (c60F51Eval f).phase + (c60F51Eval g).phase
      rw [c60F51Eval_comp]
      exact grayNeutral_add_phase _ _

/-- Kuu's primary forgetful projection exactly recovers the
verified old F95 replacement quotient of every original arrow. -/
theorem c60F125KuuPrimaryProjection_spec
    {a b : IcosahedralDart} (p q : Quiver.Path a b) :
    c60F125KuuFirstOriginalSource p q ⋙
      c60F125KuuPrimaryProjection p q =
        c60F95LocalProjection p q := by
  rfl

/-- The COMPLETE Gray 3-cell is reconstructed from the
PRIMARY Kuu quotient charge and supplementary phase.
This is a genuine reconstruction formula, not a raw F55 lift. -/
def c60F125KuuGrayReconstruction
    {a b : IcosahedralDart} {p q : Quiver.Path a b}
    {X Y : C60F125KuuGrayTwo p q}
    (h : X ⟶ Y) : GradedThreeCell 0 0 :=
  ⟨rfl,
    ((c60F95StrictGlobularInterpretation p q).map h.1).charge,
    h.2⟩

/-- For EVERY original F42/F51 source Hom, combining the
Kuu replacement quotient with its stored Gray-phase witness
recovers EXACTLY the old complete Gray Int×Int×ZMod2 evaluation. -/
theorem c60F125KuuReconstruction_original
    {a b : IcosahedralDart}
    {p q : Quiver.Path a b}
    {X Y : C60F51OriginalTwo p q}
    (f : X ⟶ Y) :
    c60F125KuuGrayReconstruction
      ((c60F125KuuFirstOriginalSource p q).map f) =
        c60F51Eval f := by
  apply GradedThreeCell.ext
  · change
      ((c60F95StrictGlobularInterpretation p q).map
        ((c60F95LocalProjection p q).map f)).charge =
          (c60F51Eval f).charge
    have hF := congrArg
      (fun F : C60F51OriginalTwo p q ⥤ C60F75StrictChargeGrade =>
        (F.map f).charge)
      (c60F95StrictGlobularInterpretation_spec p q)
    change
      ((c60F95StrictGlobularInterpretation p q).map
        ((c60F95LocalProjection p q).map f)).charge =
        ((c60F78OriginalSourceStrictFunctor p q).map f).charge at hF
    calc
      _ = ((c60F78OriginalSourceStrictFunctor p q).map f).charge := hF
      _ = (c60F51Eval f).charge := rfl
  · rfl

/-- The new KUU-FIRST interpretation is FAITHFUL to every
proof-relevant old F51 Hom: the quotient and the separate
phase together determine the original source arrow exactly. -/
theorem c60F125KuuFirst_originalFaithful
    {a b : IcosahedralDart}
    (p q : Quiver.Path a b)
    {X Y : C60F51OriginalTwo p q}
    {f g : X ⟶ Y}
    (h : (c60F125KuuFirstOriginalSource p q).map f =
      (c60F125KuuFirstOriginalSource p q).map g) :
    f = g := by
  have hNative :=
    congrArg c60F125KuuGrayReconstruction h
  rw [c60F125KuuReconstruction_original,
    c60F125KuuReconstruction_original] at hNative
  apply c60F51GrayFunctor_faithful p q
  apply GradedThreeCell.ext
  · exact congrArg GradedThreeCell.charge hNative
  · exact congrArg GradedThreeCell.phase hNative

/-- Forgetting the supplementary phase recovers precisely
Kuu replacement, while native phase equality is the EXACT
extra condition for equality of original F51 Hom arrows. -/
theorem c60F125KuuReplaceable_and_phase_iff_eq
    {a b : IcosahedralDart}
    {p q : Quiver.Path a b}
    {X Y : C60F51OriginalTwo p q}
    (f g : X ⟶ Y) :
    (c60F94Replaceable f g ∧
      (c60F51Eval f).phase = (c60F51Eval g).phase) ↔
        f = g := by
  constructor
  · rintro ⟨hKuu, hPhase⟩
    apply c60F125KuuFirst_originalFaithful p q
    apply Prod.ext
    · exact (c60F95Projection_map_eq_iff f g).mpr hKuu
    · exact hPhase
  · intro h
    subst g
    exact ⟨c60F94Replaceable_refl f, rfl⟩

/-- The actual original north interchanger has nontrivial
Gray-phase ONE, even though the separately chosen strict
Kuu/F75 interpretation collapses the interchange to equality.
Both statements are retained simultaneously, with no fabricated
original F55 Delta preimage. -/
theorem c60F125NorthKuuInterchange_withGrayDiagnostic :
    (c60F51Eval c60F51NorthOriginalInterchanger).phase =
      (1 : ZMod 2) ∧
    (c60F75OriginalFaceStrictification
       ((c60F41PentagonBoundaryLoop .north).comp
          (c60F41PentagonBoundaryLoop .north))
       (Quiver.Path.nil.comp Quiver.Path.nil)).map
         c60F51NorthOriginalInterchanger =
      eqToHom
        (c60F75OriginalInterchanger_objects_identified
          c60F51NorthFaceSourceTwo c60F51NorthFaceSourceTwo) :=
  ⟨c60F51NorthOriginalInterchanger_phaseOne,
    c60F75NorthOriginalInterchanger_collapses⟩

#print axioms c60F125KuuGrayCategory
#print axioms c60F125KuuPrimaryProjection
#print axioms c60F125KuuFirstOriginalSource
#print axioms c60F125KuuPrimaryProjection_spec
#print axioms c60F125KuuGrayReconstruction
#print axioms c60F125KuuReconstruction_original
#print axioms c60F125KuuFirst_originalFaithful
#print axioms c60F125KuuReplaceable_and_phase_iff_eq
#print axioms c60F125NorthKuuInterchange_withGrayDiagnostic

end
end KUOS.DependentOriginationC60KuuPriorityGrayCompatibilityV5_291
