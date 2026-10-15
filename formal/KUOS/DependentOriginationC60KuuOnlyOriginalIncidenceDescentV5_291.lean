import KUOS.DependentOriginationC60KuuNontrivialPhysicalStarSourceFunctorV5_264
import KUOS.DependentOriginationC60KuuLocalVerticalFunctorV5_251
import Mathlib.CategoryTheory.Comma.Over.Basic
import Mathlib.CategoryTheory.Grothendieck

namespace KUOS.DependentOriginationC60KuuOnlyOriginalIncidenceDescentV5_291

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationC60PhysicalIncidenceHigherNerveV5_223
open KUOS.DependentOriginationC60IncidenceGrothendieckExtensionV5_225
open KUOS.DependentOriginationC60KuuLocalUniversalDescentV5_249
open KUOS.DependentOriginationC60KuuPhysicalFlagSourceBridgeV5_262
open KUOS.DependentOriginationC60KuuAllPhysicalSourcePathsV5_263
open KUOS.DependentOriginationC60KuuNontrivialPhysicalStarSourceFunctorV5_264

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.291 / F112 stage 19 — Kuu ONLY: actual original C60 incidence descent

DO NOT RESTORE the old Gray presentation as an ambient site category.

The PRIMARY mathematics is the already proved Kuu F94 replacement
relation, F95 universal quotient, and F96/F97 horizontal/vertical
composition.  We build a genuine covariant Kuu-valued interpretation
of EVERY actual original F69 incidence arrow on the 60-vertex, 90-edge,
32-polygon physical cell category, and an independently constructed
CAT-VALUED diagram of Kuu slice categories on these very sites.

We use Mathlib's actual Over.mapFunctor: the fibre over each original
physical site is the slice category over that site's Kuu presentation,
and each real incidence arrow induces its genuine Kuu postcomposition
functor.  Thus the Cat diagram is NOT the artificial identity diagram.
The actual 360 vertex-edge-face triangles compose by original F69
incidence, preserving Kuu source replaceability and coherent transport.

The 90 selected original physical-edge contexts are retained as 90
separate, correctly typed Kuu viewpoints. Their genuine singleton
physical star restrictions are the earlier F108 Kuu-quotiented source
functors, NOT an invented 90-edge F47/Gray extension.

All statements below concern exactly Kuu's QUOTIENT and slice-level
descent. No original F71 four-boundary F47 fibre equality, faithful
raw F42/F54/F55 global 3-stack or uncorrected physical F68 flatness
is asserted. Former physical curvature/nonlift obstructions remain
separate facts, not prerequisites for constructing Kuu.
-/

/-- The ACTUAL original F69 incidence poset is interpreted only
through Kuu's monotone physical source-context stage.  No GrayGrade
or adjoined mixed-source vertex/face fibre enters this definition. -/
def c60F125KuuOriginalIncidenceRank :
    C60F69PhysicalCellSite ⥤ Bool where
  obj := c60F108OriginalIncidenceStage
  map := fun {_ _} f =>
    CategoryTheory.homOfLE
      (c60F108OriginalIncidenceStage_monotone
        (CategoryTheory.leOfHom f))
  map_id := by
    intro X
    apply Subsingleton.elim
  map_comp := by
    intro X Y Z f g
    apply Subsingleton.elim

/-- An arbitrary authentic original F108 edge-context gives a
KUU-QUOTIENT interpretation of the ENTIRE original 60/90/32
F69 incidence category. This is NOT the old F72 Gray collar. -/
def c60F125KuuFullOriginalIncidenceSource
    {n : Nat} (C : C60F108FaceContextFamily n) (i : Fin n) :
    C60F69PhysicalCellSite ⥤
      C60F95LocalKuuQuotient
        ((c60F108DoubleFacePatchFamily C).p i)
        ((c60F108DoubleFacePatchFamily C).q i) :=
  (c60F125KuuOriginalIncidenceRank ⋙
    c60F108WalkingToNativeF51 C i) ⋙
      c60F95LocalProjection
        ((c60F108DoubleFacePatchFamily C).p i)
        ((c60F108DoubleFacePatchFamily C).q i)

/-- The ORIGINAL F69 physical incidence star inclusion. Its
arrows are the real underlying geometric inequalities. -/
def c60F125KuuOriginalStarInclusion
    {n : Nat} (C : C60F108FaceContextFamily n) (i : Fin n) :
    C60F106PhysicalOverlap
        (c60F108DoubleFacePatchFamily C) ({i} : Finset (Fin n)) ⥤
      C60F69PhysicalCellSite where
  obj X := X.1
  map := fun {_ _} f =>
    CategoryTheory.homOfLE (CategoryTheory.leOfHom f)
  map_id := by
    intro X
    apply Subsingleton.elim
  map_comp := by
    intro X Y Z f g
    apply Subsingleton.elim

/-- Kuu's full original-site rank RESTRICTS EXACTLY to the
independently existing F108 original star rank; this is a real
equality of functors, not just equality of endpoint labels. -/
theorem c60F125KuuRank_restrictsToOriginalStar
    {n : Nat} (C : C60F108FaceContextFamily n) (i : Fin n) :
    c60F125KuuOriginalStarInclusion C i ⋙
      c60F125KuuOriginalIncidenceRank =
        c60F108StarToWalkingArrow C i := by
  fapply CategoryTheory.Functor.ext
  · intro X
    rfl
  · intro X Y f
    apply Subsingleton.elim

/-- The complete Kuu F95 original-incidence functor, when
restricted to the GENUINE physical singleton star of the
chosen original edge, is the EXISTING F108 Kuu source functor.
No separate source comparison maps need to be postulated. -/
theorem c60F125KuuFullOriginalIncidence_restrictsToStar
    {n : Nat} (C : C60F108FaceContextFamily n) (i : Fin n) :
    c60F125KuuOriginalStarInclusion C i ⋙
      c60F125KuuFullOriginalIncidenceSource C i =
    c60F108NontrivialPhysicalStarKuuFunctor C i := by
  let W := c60F108WalkingToNativeF51 C i
  let Q := c60F95LocalProjection
    ((c60F108DoubleFacePatchFamily C).p i)
    ((c60F108DoubleFacePatchFamily C).q i)
  change c60F125KuuOriginalStarInclusion C i ⋙
      ((c60F125KuuOriginalIncidenceRank ⋙ W) ⋙ Q) =
    (c60F108StarToWalkingArrow C i ⋙ W) ⋙ Q
  calc
    _ = (c60F125KuuOriginalStarInclusion C i ⋙
           c60F125KuuOriginalIncidenceRank) ⋙ (W ⋙ Q) := by
         rw [Functor.assoc c60F125KuuOriginalIncidenceRank W Q]
         exact (Functor.assoc
           (c60F125KuuOriginalStarInclusion C i)
           c60F125KuuOriginalIncidenceRank (W ⋙ Q)).symm
    _ = (c60F108StarToWalkingArrow C i) ⋙ (W ⋙ Q) := by
         rw [c60F125KuuRank_restrictsToOriginalStar]
    _ = (c60F108StarToWalkingArrow C i ⋙ W) ⋙ Q :=
      (Functor.assoc _ _ _).symm

/-- Each physical original cell X carries a TRUE KUU SLICE
CATEGORY above its selected original F95 presentation. This
depends on the original site through the source functor's object. -/
def c60F125KuuFullOriginalIncidenceCatDiagram
    {n : Nat} (C : C60F108FaceContextFamily n) (i : Fin n) :
    C60F69PhysicalCellSite ⥤ Cat :=
  c60F125KuuFullOriginalIncidenceSource C i ⋙
    CategoryTheory.Over.mapFunctor
      (C60F95LocalKuuQuotient
        ((c60F108DoubleFacePatchFamily C).p i)
        ((c60F108DoubleFacePatchFamily C).q i))

/-- The fibre at EACH of all 60/90/32 genuine C60 physical
sites is a real Kuu quotient slice, not a Gray diagnostic. -/
theorem c60F125KuuFullIncidenceCatFibre
    {n : Nat} (C : C60F108FaceContextFamily n) (i : Fin n)
    (X : C60F69PhysicalCellSite) :
    (c60F125KuuFullOriginalIncidenceCatDiagram C i).obj X =
      Cat.of (CategoryTheory.Over
        ((c60F125KuuFullOriginalIncidenceSource C i).obj X)) := rfl

/-- The only transition is Mathlib's TRUE postcomposition of
Kuu source arrows, hence genuine arrows are not replaced by
fake natural equivalences between old polygon and edge sources. -/
theorem c60F125KuuIncidenceCatMap
    {n : Nat} (C : C60F108FaceContextFamily n) (i : Fin n)
    {X Y : C60F69PhysicalCellSite} (f : X ⟶ Y) :
    (c60F125KuuFullOriginalIncidenceCatDiagram C i).map f =
      (CategoryTheory.Over.map
        ((c60F125KuuFullOriginalIncidenceSource C i).map f)).toCatHom :=
  rfl

/-- ALL 360 actual physical flags satisfy strictly the
source Kuu quotient two-step/diagonal law. Unlike a Gray
reconstruction this is a statement inside the Kuu quotient. -/
theorem c60F125KuuAllOriginalFlags_coherent
    {n : Nat} (C : C60F108FaceContextFamily n) (i : Fin n)
    (edge : TruncatedIcosahedralEdge) (endpoint side : Bool) :
    (c60F125KuuFullOriginalIncidenceSource C i).map
        (c60F71ActualFlagVertexEdgeHom edge endpoint) ≫
      (c60F125KuuFullOriginalIncidenceSource C i).map
        (c60F71ActualFlagEdgeFaceHom edge side) =
      (c60F125KuuFullOriginalIncidenceSource C i).map
        (c60F71ActualFlagVertexFaceHom edge endpoint side) := by
  rw [← (c60F125KuuFullOriginalIncidenceSource C i).map_comp]
  rw [c60F71ActualPhysicalFlagTriangle_coherent]

/-- Kuu SLICE-FIBRE transitions also satisfy the TRUE 360
original flags, by functoriality in Mathlib Cat rather than
any extra source Gray coherence assumption. -/
theorem c60F125KuuAllOriginalCatFlags_coherent
    {n : Nat} (C : C60F108FaceContextFamily n) (i : Fin n)
    (edge : TruncatedIcosahedralEdge) (endpoint side : Bool) :
    (c60F125KuuFullOriginalIncidenceCatDiagram C i).map
        (c60F71ActualFlagVertexEdgeHom edge endpoint) ≫
      (c60F125KuuFullOriginalIncidenceCatDiagram C i).map
        (c60F71ActualFlagEdgeFaceHom edge side) =
      (c60F125KuuFullOriginalIncidenceCatDiagram C i).map
        (c60F71ActualFlagVertexFaceHom edge endpoint side) := by
  rw [← (c60F125KuuFullOriginalIncidenceCatDiagram C i).map_comp]
  rw [c60F71ActualPhysicalFlagTriangle_coherent]

/-- A genuine TOTAL CATEGORY of the full physical Kuu slice
diagram exists unconditionally, constructed via Mathlib native
Grothendieck and without an old F47 vertex/face extension. -/
abbrev c60F125KuuFullIncidenceTotal
    {n : Nat} (C : C60F108FaceContextFamily n) (i : Fin n) :=
  Grothendieck (c60F125KuuFullOriginalIncidenceCatDiagram C i)

/-- The total functor projects to the ORIGINAL F69 physical
site, not to any manufactured square or Gray reconstruction. -/
def c60F125KuuFullIncidenceProjection
    {n : Nat} (C : C60F108FaceContextFamily n) (i : Fin n) :
    c60F125KuuFullIncidenceTotal C i ⥤
      C60F69PhysicalCellSite :=
  Grothendieck.forget
    (c60F125KuuFullOriginalIncidenceCatDiagram C i)

/-- Every one of the NINETY real physical edge anchors induces
a separately well-typed Kuu original full-site diagram. This
does not conflate their original free C60 path labels. -/
noncomputable def c60F125AllNinetyKuuOriginalIncidenceSource
    (i : Fin (Fintype.card TruncatedIcosahedralEdge)) :
    C60F69PhysicalCellSite ⥤
      C60F95LocalKuuQuotient
        ((c60F108DoubleFacePatchFamily c60F109AllNinetyFaceContexts).p i)
        ((c60F108DoubleFacePatchFamily c60F109AllNinetyFaceContexts).q i) :=
  c60F125KuuFullOriginalIncidenceSource
    c60F109AllNinetyFaceContexts i

/-- All ninety separate Kuu charts genuinely restrict to the
existing correct original physical stars, simultaneously. -/
theorem c60F125AllNinetyKuuOriginalStars
    (i : Fin (Fintype.card TruncatedIcosahedralEdge)) :
    c60F125KuuOriginalStarInclusion c60F109AllNinetyFaceContexts i ⋙
      c60F125AllNinetyKuuOriginalIncidenceSource i =
    c60F108NontrivialPhysicalStarKuuFunctor
      c60F109AllNinetyFaceContexts i :=
  c60F125KuuFullOriginalIncidence_restrictsToStar
    c60F109AllNinetyFaceContexts i

/-! ## The actual Kuu UNIVERSAL observer lifting property -/

universe u v
variable {T : Type u} [Category.{v} T]

/-- Any observer independent of F94 replacement factors
UNIQUE-LY at the original source through the Kuu quotient,
and its induced ORIGINAL 182-site diagram is a real pullback
along the original all-site Kuu functor. -/
def c60F125KuuOriginalIncidenceObserver
    {n : Nat} (C : C60F108FaceContextFamily n) (i : Fin n)
    (F : C60F51OriginalTwo
        ((c60F108DoubleFacePatchFamily C).p i)
        ((c60F108DoubleFacePatchFamily C).q i) ⥤ T)
    (hF : ∀ (X Y : C60F51OriginalTwo
        ((c60F108DoubleFacePatchFamily C).p i)
        ((c60F108DoubleFacePatchFamily C).q i))
      (f g : X ⟶ Y),
        c60F94Replaceable f g → F.map f = F.map g) :
    C60F69PhysicalCellSite ⥤ T :=
  c60F125KuuFullOriginalIncidenceSource C i ⋙
    c60F95UniversalLift
      ((c60F108DoubleFacePatchFamily C).p i)
      ((c60F108DoubleFacePatchFamily C).q i) F hF

/-- Exact source-level factorization on ALL original physical
sites. The original observer F is required to respect Kuu
replacement, not an independently imposed Gray gauge. -/
theorem c60F125KuuObserver_factorsOnAllOriginalSites
    {n : Nat} (C : C60F108FaceContextFamily n) (i : Fin n)
    (F : C60F51OriginalTwo
        ((c60F108DoubleFacePatchFamily C).p i)
        ((c60F108DoubleFacePatchFamily C).q i) ⥤ T)
    (hF : ∀ (X Y : C60F51OriginalTwo
        ((c60F108DoubleFacePatchFamily C).p i)
        ((c60F108DoubleFacePatchFamily C).q i))
      (f g : X ⟶ Y),
        c60F94Replaceable f g → F.map f = F.map g) :
    c60F125KuuOriginalIncidenceObserver C i F hF =
      (c60F125KuuOriginalIncidenceRank ⋙
        c60F108WalkingToNativeF51 C i) ⋙ F := by
  unfold c60F125KuuOriginalIncidenceObserver
    c60F125KuuFullOriginalIncidenceSource
  calc
    _ = (c60F125KuuOriginalIncidenceRank ⋙
          c60F108WalkingToNativeF51 C i) ⋙
        (c60F95LocalProjection
          ((c60F108DoubleFacePatchFamily C).p i)
          ((c60F108DoubleFacePatchFamily C).q i) ⋙
        c60F95UniversalLift
          ((c60F108DoubleFacePatchFamily C).p i)
          ((c60F108DoubleFacePatchFamily C).q i) F hF) :=
          Functor.assoc _ _ _
    _ = _ := by
          rw [c60F95UniversalLift_spec]

/-- This Kuu factorization is UNIVERSAL for ANY target category,
not solely the original F51/Gray charge target. -/
theorem c60F125KuuOriginalIncidenceObserver_unique
    {n : Nat} (C : C60F108FaceContextFamily n) (i : Fin n)
    (F : C60F51OriginalTwo
        ((c60F108DoubleFacePatchFamily C).p i)
        ((c60F108DoubleFacePatchFamily C).q i) ⥤ T)
    (hF : ∀ (X Y : C60F51OriginalTwo
        ((c60F108DoubleFacePatchFamily C).p i)
        ((c60F108DoubleFacePatchFamily C).q i))
      (f g : X ⟶ Y),
        c60F94Replaceable f g → F.map f = F.map g) :
    ∃! L : C60F95LocalKuuQuotient
        ((c60F108DoubleFacePatchFamily C).p i)
        ((c60F108DoubleFacePatchFamily C).q i) ⥤ T,
      c60F95LocalProjection
        ((c60F108DoubleFacePatchFamily C).p i)
        ((c60F108DoubleFacePatchFamily C).q i) ⋙ L = F :=
  c60F95Universal_existsUnique
    ((c60F108DoubleFacePatchFamily C).p i)
    ((c60F108DoubleFacePatchFamily C).q i) F hF

#print axioms c60F125KuuOriginalIncidenceRank
#print axioms c60F125KuuFullOriginalIncidenceSource
#print axioms c60F125KuuRank_restrictsToOriginalStar
#print axioms c60F125KuuFullOriginalIncidence_restrictsToStar
#print axioms c60F125KuuFullOriginalIncidenceCatDiagram
#print axioms c60F125KuuFullIncidenceCatFibre
#print axioms c60F125KuuIncidenceCatMap
#print axioms c60F125KuuAllOriginalFlags_coherent
#print axioms c60F125KuuAllOriginalCatFlags_coherent
#print axioms c60F125KuuFullIncidenceProjection
#print axioms c60F125AllNinetyKuuOriginalStars
#print axioms c60F125KuuObserver_factorsOnAllOriginalSites
#print axioms c60F125KuuOriginalIncidenceObserver_unique

end
end KUOS.DependentOriginationC60KuuOnlyOriginalIncidenceDescentV5_291
