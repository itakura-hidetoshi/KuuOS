import KuuOSFormal.HistoricalF36F40BridgeP46

/-!
# F112-P47 — exact original F42 descent criterion for genuine F69 localization

P46 gives a FULL, typed Mathlib functor from every original C60
Quiver.Path (60 true dart objects, 180 genuine oriented arrows) into
the independent F69 physical zigzag localization. P46 does not, alone,
show that all 32 ORIGINAL F42 face 2-cell generators map to identities.

This theorem module isolates that genuine missing premise as the
actual 32-face boundary-loop localization condition, then proves:

  * EVERY actual original F42 proof-relevant cell, including physical
    face, inverse, vertical composition and BOTH whiskerings, carries
    equal independent F69 localized path images under that premise;
  * both original horizontal-pasting orders localize compatibly;
  * the original Mathlib F42 face-HomRel is killed by the independent
    localization under precisely that premise;
  * an ACTUAL functor from the original F42 face-relation quotient
    category to native F69 localization, with exact triangle and
    uniqueness;
  * descent EXISTS if and only if all 32 actual original physical
    face generators are sound after the P46 path interpretation.

There is NO global assumption added as a Lean axiom. The 32-face
condition remains a visible, unsolved physical comparison obligation,
not an asserted fact, and all original proof-relevant raw F42 terms
and F55 phase/curvature information remain distinct.
-/

namespace KUOS.F112ActualHistoricalF36F40BridgeP4
namespace GenuineOriginalC60Geometry
namespace ActualF47

open CategoryTheory
open Kuu.F112.Physical
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationGrayC60NativePathFunctorV5_189
open KUOS.DependentOriginationGrayC60PresentedFaceTwoCellsV5_190

set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 4096
set_option maxHeartbeats 2000000
noncomputable section

/-- The PRECISE missing F42/F69 comparison input: every one of the
32 actual original 5/6-sided physical face boundary paths is sent to
the original base-dart identity by P46's actual native localization
functor. This is a Prop to be PROVED later, not a new axiom. -/
def historicalF42AllOriginalFacesLocalize : Prop :=
  ∀ face : TruncatedIcosahedralSeedFace,
    historicalOldPathsToLocalization.map
      (c60F41PhysicalFaceBoundaryLoop face).2 =
    historicalOldPathsToLocalization.map
      (Quiver.Path.nil :
        Quiver.Path (c60F41PhysicalFaceBoundaryLoop face).1
          (c60F41PhysicalFaceBoundaryLoop face).1)

/-- The complete ORIGINAL Type-valued F42 proof grammar is
sound in genuine independent F69 localization once the actual
32 physical face-relator obligation is supplied. Every source
path and every pasting/whiskering endpoint remains fully typed. -/
theorem historicalF42EveryRawCell_localizes
    (hfaces : historicalF42AllOriginalFacesLocalize)
    {a b : IcosahedralDart} {p q : Quiver.Path a b}
    (cell : C60F42PresentedFaceCell p q) :
    historicalOldPathsToLocalization.map p =
      historicalOldPathsToLocalization.map q := by
  induction cell with
  | ident _ => rfl
  | physicalFace face => exact hfaces face
  | symm cell ih => exact ih.symm
  | trans left right ihLeft ihRight =>
      exact ihLeft.trans ihRight
  | whiskerLeft prior cell ih =>
      simp only [historicalOldPaths_localized_comp]
      rw [ih]
  | whiskerRight cell suffix ih =>
      simp only [historicalOldPaths_localized_comp]
      rw [ih]

/-- Both ACTUAL horizontal pasting orders of original F42 cells
produce the same native localized source/target path image, while
their distinct raw proof trees are never identified by fiat. -/
theorem historicalF42BothHorizontalPastes_localize
    (hfaces : historicalF42AllOriginalFacesLocalize)
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    (α : C60F42PresentedFaceCell p q)
    (β : C60F42PresentedFaceCell r s) :
    historicalOldPathsToLocalization.map (p.comp r) =
      historicalOldPathsToLocalization.map (q.comp s) :=
  historicalF42EveryRawCell_localizes hfaces
    (C60F42PresentedFaceCell.horizontalLeftFirst α β)

/-- The original ACTUAL F42 physical-face HomRel is mapped to equality
of independent localized morphisms: uses the original Type-valued
2-cell witness, never simply a phase/grade comparison. -/
theorem historicalF42OriginalFaceRel_localizes
    (hfaces : historicalF42AllOriginalFacesLocalize)
    {a b : C60F41OriginalPathCategory} (p q : a ⟶ b)
    (h : c60F42OriginalFaceHomRel p q) :
    historicalOldPathsToLocalization.map p =
      historicalOldPathsToLocalization.map q := by
  rcases h with ⟨cell⟩
  exact historicalF42EveryRawCell_localizes hfaces cell

/-- CONDITIONAL but genuine Mathlib quotient functor: original full
F42 face relations descend to the precise independently constructed
F69 Gabriel–Zisman localization if all physical face loops are sound.
Nothing here invents the missing 32 geometric comparison proofs. -/
def historicalF42FaceQuotientToLocalization
    (hfaces : historicalF42AllOriginalFacesLocalize) :
    C60F42FaceRelationPathCategory ⥤ PhysicalLocalization :=
  CategoryTheory.Quotient.lift c60F42OriginalFaceHomRel
    historicalOldPathsToLocalization
    (by
      intro a b p q h
      exact historicalF42OriginalFaceRel_localizes hfaces p q h)

/-- The descending functor commutes with the EXACT original F42
quotient map on every original path, not merely on finite generators. -/
theorem historicalF42FaceQuotient_factors
    (hfaces : historicalF42AllOriginalFacesLocalize) :
    CategoryTheory.Quotient.functor c60F42OriginalFaceHomRel ⋙
      historicalF42FaceQuotientToLocalization hfaces =
        historicalOldPathsToLocalization :=
  CategoryTheory.Quotient.lift_spec _ _ _

/-- No two purported descent maps can disagree when they both
factor the actual historical-to-independent C60 free path functor. -/
theorem historicalF42FaceQuotient_unique
    (hfaces : historicalF42AllOriginalFacesLocalize)
    (F : C60F42FaceRelationPathCategory ⥤ PhysicalLocalization)
    (hF : CategoryTheory.Quotient.functor c60F42OriginalFaceHomRel ⋙ F =
        historicalOldPathsToLocalization) :
    F = historicalF42FaceQuotientToLocalization hfaces :=
  CategoryTheory.Quotient.lift_unique _ _ _ F hF

/-- The missing REAL face condition is necessary and sufficient for
preserving every old F42 presented source 2-cell in F69 localization.
This is an equivalence of obligations, not their discharge. -/
theorem historicalF42AllRawCellsSound_iff_faces :
    (∀ {a b : IcosahedralDart} {p q : Quiver.Path a b},
      C60F42PresentedFaceCell p q →
        historicalOldPathsToLocalization.map p =
          historicalOldPathsToLocalization.map q) ↔
      historicalF42AllOriginalFacesLocalize := by
  constructor
  · intro h face
    exact h (C60F42PresentedFaceCell.physicalFace face)
  · intro h a b p q cell
    exact historicalF42EveryRawCell_localizes h cell

/-- The entire original F42 quotient localization factor exists
IF AND ONLY IF each of the 32 genuinely old polygon boundary loops
maps to the correct physical dart identity in independent F69.
No false full old/new raw source equivalence is asserted. -/
theorem historicalF42LocalizationDescent_iff_actualFaces :
    (∃ F : C60F42FaceRelationPathCategory ⥤ PhysicalLocalization,
      CategoryTheory.Quotient.functor c60F42OriginalFaceHomRel ⋙ F =
        historicalOldPathsToLocalization) ↔
      historicalF42AllOriginalFacesLocalize := by
  constructor
  · rintro ⟨F, hF⟩ face
    have hface := c60F42EveryPhysicalFace_relation_sounds face
    have hh :
        (CategoryTheory.Quotient.functor c60F42OriginalFaceHomRel ⋙ F).map
            (c60F41PhysicalFaceBoundaryLoop face).2 =
          (CategoryTheory.Quotient.functor c60F42OriginalFaceHomRel ⋙ F).map
            (Quiver.Path.nil :
              Quiver.Path (c60F41PhysicalFaceBoundaryLoop face).1
                (c60F41PhysicalFaceBoundaryLoop face).1) := by
      change F.map ((CategoryTheory.Quotient.functor
        c60F42OriginalFaceHomRel).map
          (c60F41PhysicalFaceBoundaryLoop face).2) =
        F.map ((CategoryTheory.Quotient.functor
          c60F42OriginalFaceHomRel).map
            (Quiver.Path.nil :
              Quiver.Path (c60F41PhysicalFaceBoundaryLoop face).1
                (c60F41PhysicalFaceBoundaryLoop face).1))
      exact congrArg (fun g => F.map g) hface
    rw [hF] at hh
    exact hh
  · intro hfaces
    exact ⟨historicalF42FaceQuotientToLocalization hfaces,
      historicalF42FaceQuotient_factors hfaces⟩

#print axioms historicalF42AllOriginalFacesLocalize
#print axioms historicalF42EveryRawCell_localizes
#print axioms historicalF42BothHorizontalPastes_localize
#print axioms historicalF42OriginalFaceRel_localizes
#print axioms historicalF42FaceQuotientToLocalization
#print axioms historicalF42FaceQuotient_factors
#print axioms historicalF42FaceQuotient_unique
#print axioms historicalF42AllRawCellsSound_iff_faces
#print axioms historicalF42LocalizationDescent_iff_actualFaces

end
end ActualF47
end GenuineOriginalC60Geometry
end KUOS.F112ActualHistoricalF36F40BridgeP4
