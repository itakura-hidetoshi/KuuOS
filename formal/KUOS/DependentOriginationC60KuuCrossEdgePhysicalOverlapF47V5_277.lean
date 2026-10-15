import KUOS.DependentOriginationC60KuuIndependentMixedPhysicalBaseChangeV5_276

namespace KUOS.DependentOriginationC60KuuCrossEdgePhysicalOverlapF47V5_277

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationTruncatedIcosahedralFlagSquaresV5_154
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationGrayF55PhaseRealizationV5_156
open KUOS.DependentOriginationGrayC60NativePathFunctorV5_189
open KUOS.DependentOriginationGrayC60PresentedFaceTwoCellsV5_190
open KUOS.DependentOriginationGrayC60PresentedInterchangerV5_191
open KUOS.DependentOriginationGrayC60ThreeHomCategoriesV5_192
open KUOS.DependentOriginationGrayC60OriginalF55ThreeHomV5_192
open KUOS.DependentOriginationGrayC60F55SourcePhaseLockedAtlasV5_175
open KUOS.DependentOriginationGrayC60PhysicalFlagF55BridgeV5_194
open KUOS.DependentOriginationGrayC60AllNinetyEdgePastingV5_157
open KUOS.DependentOriginationGrayC60MixedBoundaryThreeHomV5_195
open KUOS.DependentOriginationGrayC60AllNinetyMixedBoundaryV5_196
open KUOS.DependentOriginationGrayC60F55MixedOriginalContextV5_205
open KUOS.DependentOriginationC60FiniteAtlasCechCoherenceV5_221
open KUOS.DependentOriginationC60PhysicalIncidenceHigherNerveV5_223
open KUOS.DependentOriginationC60KuuActualIncidenceOverlapRefinementV5_260
open KUOS.DependentOriginationC60KuuTwoActualFaceInterchangeV5_265
open KUOS.DependentOriginationC60KuuIndependentPhysicalFaceSiteSourceV5_274
open KUOS.DependentOriginationC60KuuIndependentFaceMixedF55FrameV5_275
open KUOS.DependentOriginationC60KuuIndependentMixedPhysicalBaseChangeV5_276
open KUOS.DependentOriginationC60PhysicalCechCurvatureRepairV5_222
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.277 / F112 fifth stage — genuine DISTINCT-edge F69 physical overlaps

F112/v5.276 proved native-phase-preserving ORIGINAL F47 source change
between different original F42 face/path descriptions of ONE AND THE
SAME real C60 physical edge. The F56 contextual transport intentionally
required identical physical edges.

This module does NOT discard that requirement and invent a comparison.
It constructs a DIFFERENT, guarded local reindexing interface:
* a certificate of TWO genuinely DISTINCT ORIGINAL physical edges,
* a true F106 F69-incidence star-intersection site, proving these two
  different edges share an ACTUAL old dart endpoint or a pentagon/
  hexagon face, without adding any fictitious quadrilateral face,
* TWO separately original-boundary-typed odd F42 face-site pairs and
  the actual old original F43/F44/F54/F55 physical F47 frames.

Although the original source boundaries and the real physical edge
labels are distinct, both genuine odd/odd original F43 exchanges have
the SAME full native (0,0;1) image, and each separately original F55
physical flag-square has the SAME full native (0,1;1) image. These
facts are separately DERIVED, rather than assumed as cross-edge
compatibility. We construct a precisely guarded F47 source functor
between the local four-boundary CATEGORIES by reindexing the six
genuine mixed raw constructors, proving preservation of BOTH
integer charges and the INDEPENDENT exchange phase for ALL Homs,
faithfulness and source square transport.

For a genuine common physical incidence site of THREE distinct
edges, the three guarded source transports obey a full-Hom Cech
cocycle in correctly dependent HEq form. The original F55
nine-constructor Delta nonlift and the original signed F68 north
pentagon second charge -5 remain explicit simultaneous obstructions.

LIMITS: A guarded LOCAL F47 source reindexing is NOT a functor
from the entire F69 physical incidence category to a global F47
three-stack. A shared F69 site is a REAL geometric overlap, but
its existence alone does not imply source-term identifications,
a Grothendieck topology, or effective global source descent.
-/

/-! ## I. True nonempty F106 intersection of DISTINCT physical edges -/

/-- Unlike a bare full-native arrow equality, this structure
requires TWO DIFFERENT ORIGINAL C60 edges AND a genuine site in
the exact intersection of their two ACTUAL F69 incidence stars. -/
structure C60F112DistinctEdgeOverlap
    {n : Nat} (C : C60F108BothFaceContexts n)
    (i j : Fin n) where
  edge_ne : C.edge i ≠ C.edge j
  common :
    C60F106PhysicalOverlap
      (c60F108BothFacePatchFamily C) ({i, j} : Finset (Fin n))

/-- A common TRUE original pentagonal/hexagonal face supplies a
proof-carrying distinct-edge F69 overlap, with exactly that face
as its actual site and no invented source geometry. -/
def c60F112DistinctEdgeSharedFace
    {n : Nat} (C : C60F108BothFaceContexts n)
    (i j : Fin n) (face : TruncatedIcosahedralSeedFace)
    (hne : C.edge i ≠ C.edge j)
    (hi : truncatedEdgeOnSeedFace (C.edge i) face)
    (hj : truncatedEdgeOnSeedFace (C.edge j) face) :
    C60F112DistinctEdgeOverlap C i j where
  edge_ne := hne
  common := ⟨.face face, by
    intro k hk
    rcases Finset.mem_insert.mp hk with hki | hkj
    · subst k
      exact Or.inr (c60F69PhysicalEdgeFace (C.edge i) face hi)
    · have hk' : k = j := Finset.mem_singleton.mp hkj
      subst k
      exact Or.inr (c60F69PhysicalEdgeFace (C.edge j) face hj)⟩

/-- A common ORIGINAL dart endpoint is also sufficient for
genuine nonempty F69 star intersection between distinct edges. -/
def c60F112DistinctEdgeSharedEndpoint
    {n : Nat} (C : C60F108BothFaceContexts n)
    (i j : Fin n) (v : IcosahedralDart)
    (hne : C.edge i ≠ C.edge j)
    (hi : v = (truncatedIcosahedralEdgeEndpoints (C.edge i)).1 ∨
      v = (truncatedIcosahedralEdgeEndpoints (C.edge i)).2)
    (hj : v = (truncatedIcosahedralEdgeEndpoints (C.edge j)).1 ∨
      v = (truncatedIcosahedralEdgeEndpoints (C.edge j)).2) :
    C60F112DistinctEdgeOverlap C i j where
  edge_ne := hne
  common := ⟨.vertex v, by
    intro k hk
    rcases Finset.mem_insert.mp hk with hki | hkj
    · subst k
      exact Or.inl (c60F69PhysicalVertexEdge v (C.edge i) hi)
    · have hk' : k = j := Finset.mem_singleton.mp hkj
      subst k
      exact Or.inl (c60F69PhysicalVertexEdge v (C.edge j) hj)⟩

/-- The shared face in the real pair overlap stays the ORIGINAL
polygon site; no purely synthetic overlap object is substituted. -/
theorem c60F112DistinctEdgeSharedFace_site
    {n : Nat} (C : C60F108BothFaceContexts n)
    (i j : Fin n) (face : TruncatedIcosahedralSeedFace)
    (hne : C.edge i ≠ C.edge j)
    (hi : truncatedEdgeOnSeedFace (C.edge i) face)
    (hj : truncatedEdgeOnSeedFace (C.edge j) face) :
    (c60F112DistinctEdgeSharedFace C i j face hne hi hj).common.1 =
      C60F69PhysicalCellSite.face face := rfl

/-- Two DISTINCT original C60 physical edges have NO direct
edge-to-edge incidence arrow. Cross-edge comparison must be
mediated by an actual shared lower/upper incident site. -/
theorem c60F112DistinctEdge_noDirectPhysicalHom
    {n : Nat} (C : C60F108BothFaceContexts n)
    (i j : Fin n) (W : C60F112DistinctEdgeOverlap C i j) :
    ¬ (C60F69PhysicalCellSite.edge (C.edge i) ≤
      C60F69PhysicalCellSite.edge (C.edge j)) := by
  intro h
  exact W.edge_ne h

/-- Each genuine shared site restricts to BOTH true physical
singleton stars, preserving EXACTLY the same original F69 site.
These are actual F106 geometric restriction functors. -/
theorem c60F112DistinctEdge_twoActualRestrictions
    {n : Nat} (C : C60F108BothFaceContexts n)
    (i j : Fin n) (W : C60F112DistinctEdgeOverlap C i j) :
    ((c60F106ToSingleton
      (c60F108BothFacePatchFamily C) ({i, j} : Finset (Fin n))
      i (by simp)).obj W.common).1 = W.common.1 ∧
    ((c60F106ToSingleton
      (c60F108BothFacePatchFamily C) ({i, j} : Finset (Fin n))
      j (by simp)).obj W.common).1 = W.common.1 :=
  ⟨rfl, rfl⟩

/-! ## II. Cross-edge ORIGINAL F47 four-boundary source reindexing -/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

section ActualCrossEdgeSources
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

abbrev c60F112CrossEdgeFrame {n : Nat}
    (C : C60F108BothFaceContexts n) (i : Fin n)
    (P : C60F112IndependentOddFacePair C i) :=
  c60F112IndependentFaceOriginalMixedFrame t₁ t₂ left right C i P

/-- The full ORIGINAL F43/F44 native image is IDENTICAL
for independent odd/odd F42 sources on DIFFERENT real
physical C60 edges, WITHOUT making their source Hom types
or original path boundaries equal. -/
theorem c60F112CrossEdgeFace_fullNative
    {n : Nat} (C : C60F108BothFaceContexts n)
    (i j : Fin n)
    (P : C60F112IndependentOddFacePair C i)
    (Q : C60F112IndependentOddFacePair C j) :
    c60F44FaceThreeEval
      (c60F112CrossEdgeFrame t₁ t₂ left right C i P).faceStep =
    c60F44FaceThreeEval
      (c60F112CrossEdgeFrame t₁ t₂ left right C j Q).faceStep := by
  change (c60F112IndependentFaceOriginalF43 C i P).toNative =
    (c60F112IndependentFaceOriginalF43 C j Q).toNative
  rw [c60F112IndependentFaceOriginalF43_native,
    c60F112IndependentFaceOriginalF43_native]

/-- On ANY pair of actual C60 physical edges, the old ORIGINAL
F54/F55 source flag-square has the same complete native F59
value (0,1;phase1). This is a proven target equality, not
an equality of different ORIGINAL edge-local source witnesses. -/
theorem c60F112CrossEdgeF55_fullNative
    {n : Nat} (C : C60F108BothFaceContexts n)
    (i j : Fin n)
    (P : C60F112IndependentOddFacePair C i)
    (Q : C60F112IndependentOddFacePair C j) :
    c60F44OriginalF55Eval
      (c60F112CrossEdgeFrame t₁ t₂ left right C i P).rotationStep =
    c60F44OriginalF55Eval
      (c60F112CrossEdgeFrame t₁ t₂ left right C j Q).rotationStep := by
  change c60F44OriginalF55GrayFunctor.map
      (c60F46PhysicalFlagOriginalF55Arrow
        t₁ t₂ left right (C.edge i)) =
    c60F44OriginalF55GrayFunctor.map
      (c60F46PhysicalFlagOriginalF55Arrow
        t₁ t₂ left right (C.edge j))
  simp only [c60F46PhysicalFlagOriginalF55Arrow_fullNative,
    c60AllNinetyGrayCell_eq]

/-- A NEW GUARDED cross-physical-edge source reindexing. Its
existence is licensed by an ACTUAL nonempty original F69
incidence-star overlap of two DISTINCT physical edges.
The four original F42/F54 boundary types remain different.
The only new comparison arrows are the already ADJOINED
F47 raw mixed constructors, NOT old F55 ten-generator terms. -/
def c60F112CrossEdgeMixedSourceChange
    {n : Nat} (C : C60F108BothFaceContexts n)
    (i j : Fin n) (_W : C60F112DistinctEdgeOverlap C i j)
    (P : C60F112IndependentOddFacePair C i)
    (Q : C60F112IndependentOddFacePair C j) :
    C60F47BoundaryPoint
      (c60F112CrossEdgeFrame t₁ t₂ left right C i P) ⥤
    C60F47BoundaryPoint
      (c60F112CrossEdgeFrame t₁ t₂ left right C j Q) where
  obj := c60F56ContextMixedPoint
    (c60F112CrossEdgeFrame t₁ t₂ left right C i P)
    (c60F112CrossEdgeFrame t₁ t₂ left right C j Q)
  map := fun {_ _} f =>
    Quot.liftOn f
      (fun raw => c60F47MixedOf
        (c60F56ContextMixedRaw
          (c60F112CrossEdgeFrame t₁ t₂ left right C i P)
          (c60F112CrossEdgeFrame t₁ t₂ left right C j Q) raw))
      (by
        intro u v h
        apply Quot.sound
        calc
          _ = u.toNative :=
            c60F56ContextMixedRaw_native
              (c60F112CrossEdgeFrame t₁ t₂ left right C i P)
              (c60F112CrossEdgeFrame t₁ t₂ left right C j Q)
              (c60F112CrossEdgeFace_fullNative t₁ t₂ left right C i j P Q)
              (c60F112CrossEdgeF55_fullNative t₁ t₂ left right C i j P Q) u
          _ = v.toNative := h
          _ = _ :=
            (c60F56ContextMixedRaw_native
              (c60F112CrossEdgeFrame t₁ t₂ left right C i P)
              (c60F112CrossEdgeFrame t₁ t₂ left right C j Q)
              (c60F112CrossEdgeFace_fullNative t₁ t₂ left right C i j P Q)
              (c60F112CrossEdgeF55_fullNative t₁ t₂ left right C i j P Q) v).symm)
  map_id := by
    intro X
    apply Quot.sound
    rfl
  map_comp := by
    intro X Y Z f g
    refine Quot.inductionOn f (fun f => ?_)
    refine Quot.inductionOn g (fun g => ?_)
    apply Quot.sound
    rfl

/-- Unlike the F77 observer, guarded cross-edge source
reindexing preserves BOTH original Int charges AND native
ZMod2 phase on EVERY arrow of the original F47 category. -/
theorem c60F112CrossEdgeMixedSourceChange_fullNative
    {n : Nat} (C : C60F108BothFaceContexts n)
    (i j : Fin n) (W : C60F112DistinctEdgeOverlap C i j)
    (P : C60F112IndependentOddFacePair C i)
    (Q : C60F112IndependentOddFacePair C j)
    {X Y : C60F47BoundaryPoint
      (c60F112CrossEdgeFrame t₁ t₂ left right C i P)}
    (f : X ⟶ Y) :
    c60F47MixedEval
      ((c60F112CrossEdgeMixedSourceChange
        t₁ t₂ left right C i j W P Q).map f) =
      c60F47MixedEval f := by
  refine Quot.inductionOn f (fun raw => ?_)
  exact c60F56ContextMixedRaw_native
    (c60F112CrossEdgeFrame t₁ t₂ left right C i P)
    (c60F112CrossEdgeFrame t₁ t₂ left right C j Q)
    (c60F112CrossEdgeFace_fullNative t₁ t₂ left right C i j P Q)
    (c60F112CrossEdgeF55_fullNative t₁ t₂ left right C i j P Q) raw

/-- Faithfulness is a full ORIGINAL F47 source Hom property,
not a claim of invertibility of the phase-forgetting F77
quotient or an equality of unrelated original F42 cells. -/
theorem c60F112CrossEdgeMixedSourceChange_faithful
    {n : Nat} (C : C60F108BothFaceContexts n)
    (i j : Fin n) (W : C60F112DistinctEdgeOverlap C i j)
    (P : C60F112IndependentOddFacePair C i)
    (Q : C60F112IndependentOddFacePair C j)
    {X Y : C60F47BoundaryPoint
      (c60F112CrossEdgeFrame t₁ t₂ left right C i P)}
    {f g : X ⟶ Y}
    (h : (c60F112CrossEdgeMixedSourceChange
      t₁ t₂ left right C i j W P Q).map f =
      (c60F112CrossEdgeMixedSourceChange
        t₁ t₂ left right C i j W P Q).map g) : f = g := by
  apply c60F47MixedGrayFunctor_faithful
    (c60F112CrossEdgeFrame t₁ t₂ left right C i P)
  have hh := congrArg (fun z => c60F47MixedEval z) h
  change
    c60F47MixedEval
      ((c60F112CrossEdgeMixedSourceChange
        t₁ t₂ left right C i j W P Q).map f) =
    c60F47MixedEval
      ((c60F112CrossEdgeMixedSourceChange
        t₁ t₂ left right C i j W P Q).map g) at hh
  rw [c60F112CrossEdgeMixedSourceChange_fullNative,
    c60F112CrossEdgeMixedSourceChange_fullNative] at hh
  exact hh

/-- The old original F43 face arrow and F55 physical
flag-square form a TRUE commuting source F47 mixed square;
cross-edge guarded source reindexing preserves the WHOLE
old/source-new comparison, not merely the native image. -/
theorem c60F112CrossEdgeMixedSourceChange_square
    {n : Nat} (C : C60F108BothFaceContexts n)
    (i j : Fin n) (W : C60F112DistinctEdgeOverlap C i j)
    (P : C60F112IndependentOddFacePair C i)
    (Q : C60F112IndependentOddFacePair C j) :
    (c60F112CrossEdgeMixedSourceChange
      t₁ t₂ left right C i j W P Q).map
      (c60F47FaceArrow (c60F112CrossEdgeFrame t₁ t₂ left right C i P) ≫
        c60F47CompareAfter
          (c60F112CrossEdgeFrame t₁ t₂ left right C i P)) =
    c60F47FaceArrow (c60F112CrossEdgeFrame t₁ t₂ left right C j Q) ≫
      c60F47CompareAfter
        (c60F112CrossEdgeFrame t₁ t₂ left right C j Q) := by
  apply Quot.sound
  rfl

/-! ## III. Genuine triple intersection and dependent F47 Cech transport -/

/-- A REAL original physical intersection of THREE actual
edge stars restricts to each of its real two-edge overlaps,
but only after proof that the selected pair belongs to the
actual triple family. No physical triple intersection is
manufactured by merely having three unrelated pair overlaps. -/
def c60F112TriplePhysicalToDistinctPair
    {n : Nat} (C : C60F108BothFaceContexts n)
    (i j k a b : Fin n)
    (X : C60F106PhysicalOverlap
      (c60F108BothFacePatchFamily C) ({i, j, k} : Finset (Fin n)))
    (hne : C.edge a ≠ C.edge b)
    (hsub : ({a, b} : Finset (Fin n)) ⊆ ({i, j, k} : Finset (Fin n))) :
    C60F112DistinctEdgeOverlap C a b where
  edge_ne := hne
  common :=
    (c60F106OverlapRestrict
      (c60F108BothFacePatchFamily C) hsub).obj X

/-- THREE distinct original physical edge stars with a common
ACTUAL original F69 site support a genuine source comparison
triangle on ALL mixed F47 Homs. Because the Hom target types
depend on different original F42/F54 boundary presentations,
the fully source-typed cocycle is an HEq, not fake raw equality. -/
theorem c60F112CrossEdgeTriplePhysicalCech
    {n : Nat} (C : C60F108BothFaceContexts n)
    (i j k : Fin n)
    (X₃ : C60F106PhysicalOverlap
      (c60F108BothFacePatchFamily C) ({i, j, k} : Finset (Fin n)))
    (hij : C.edge i ≠ C.edge j)
    (hjk : C.edge j ≠ C.edge k)
    (hik : C.edge i ≠ C.edge k)
    (P : C60F112IndependentOddFacePair C i)
    (Q : C60F112IndependentOddFacePair C j)
    (R : C60F112IndependentOddFacePair C k)
    {U V : C60F47BoundaryPoint
      (c60F112CrossEdgeFrame t₁ t₂ left right C i P)}
    (f : U ⟶ V) :
    HEq
      (((c60F112CrossEdgeMixedSourceChange
        t₁ t₂ left right C i j
          (c60F112TriplePhysicalToDistinctPair C i j k i j X₃ hij
            (by intro z hz; simp only [Finset.mem_insert, Finset.mem_singleton]
              at hz ⊢; tauto)) P Q) ⋙
        (c60F112CrossEdgeMixedSourceChange
          t₁ t₂ left right C j k
            (c60F112TriplePhysicalToDistinctPair C i j k j k X₃ hjk
              (by intro z hz; simp only [Finset.mem_insert, Finset.mem_singleton]
                at hz ⊢; tauto)) Q R)).map f)
      ((c60F112CrossEdgeMixedSourceChange
        t₁ t₂ left right C i k
          (c60F112TriplePhysicalToDistinctPair C i j k i k X₃ hik
            (by intro z hz; simp only [Finset.mem_insert, Finset.mem_singleton]
              at hz ⊢; tauto)) P R).map f) := by
  cases U <;> cases V
  all_goals
    apply heq_of_eq
    apply c60F47MixedGrayFunctor_faithful
      (c60F112CrossEdgeFrame t₁ t₂ left right C k R)
    change
      c60F47MixedEval
        ((c60F112CrossEdgeMixedSourceChange
          t₁ t₂ left right C j k
            (c60F112TriplePhysicalToDistinctPair C i j k j k X₃ hjk
              (by intro z hz; simp only [Finset.mem_insert, Finset.mem_singleton]
                at hz ⊢; tauto)) Q R).map
          ((c60F112CrossEdgeMixedSourceChange
            t₁ t₂ left right C i j
              (c60F112TriplePhysicalToDistinctPair C i j k i j X₃ hij
                (by intro z hz; simp only [Finset.mem_insert, Finset.mem_singleton]
                  at hz ⊢; tauto)) P Q).map f)) =
      c60F47MixedEval
        ((c60F112CrossEdgeMixedSourceChange
          t₁ t₂ left right C i k
            (c60F112TriplePhysicalToDistinctPair C i j k i k X₃ hik
              (by intro z hz; simp only [Finset.mem_insert, Finset.mem_singleton]
                at hz ⊢; tauto)) P R).map f)
    rw [c60F112CrossEdgeMixedSourceChange_fullNative,
      c60F112CrossEdgeMixedSourceChange_fullNative,
      c60F112CrossEdgeMixedSourceChange_fullNative]

/-! ## IV. Original source obstruction is NOT glued away -/

/-- Cross-edge ORIGINAL F47 source comparison, even on a
nonempty TRUE old C60 incidence overlap, never supplies a
NINE-CONSTRUCTOR original F55 source for the adjoined
Delta comparison at the first physical edge. -/
theorem c60F112CrossEdgeOriginalF55_nonlift
    {n : Nat} (C : C60F108BothFaceContexts n)
    (i j : Fin n) (W : C60F112DistinctEdgeOverlap C i j)
    (P : C60F112IndependentOddFacePair C i)
    (Q : C60F112IndependentOddFacePair C j) :
    (¬ ∃ cell :
      OriginalF45BracketTree.DepthRotationRoute.PresentedCell
        (OriginalF45BracketTree.DepthRotationRoute.squareLeftFirst left right)
        (OriginalF45BracketTree.DepthRotationRoute.squareRightFirst left right),
      c60F44FaceThreeEval
        (c60F112CrossEdgeFrame t₁ t₂ left right C i P).faceStep +
          c60F55SourceNative cell =
        c60F44OriginalF55Eval
          (c60F112CrossEdgeFrame t₁ t₂ left right C i P).rotationStep) ∧
    (¬ ∃ cell :
      OriginalF45BracketTree.DepthRotationRoute.PresentedCell
        (OriginalF45BracketTree.DepthRotationRoute.squareLeftFirst left right)
        (OriginalF45BracketTree.DepthRotationRoute.squareRightFirst left right),
      c60F44FaceThreeEval
        (c60F112CrossEdgeFrame t₁ t₂ left right C j Q).faceStep +
          c60F55SourceNative cell =
        c60F44OriginalF55Eval
          (c60F112CrossEdgeFrame t₁ t₂ left right C j Q).rotationStep) := by
  exact ⟨
    c60F112IndependentFaceOriginalMixed_noF55Lift t₁ t₂ left right C i P,
    c60F112IndependentFaceOriginalMixed_noF55Lift t₁ t₂ left right C j Q⟩

/-- On any ACTUAL cross-edge overlap with independently
typed F47 sources, the original F68 north pentagon retains
signed second charge -5 and nonzero curvature. No alleged
source-level descent follows from the guarded F47 comparison. -/
theorem c60F112CrossEdge_withNorthCurvature
    {n : Nat} (C : C60F108BothFaceContexts n)
    (i j : Fin n) (W : C60F112DistinctEdgeOverlap C i j)
    (P : C60F112IndependentOddFacePair C i)
    (Q : C60F112IndependentOddFacePair C j)
    (sigma : C60F67Atlas) :
    (c60F68PhysicalPatchCurvature t₁ t₂ left right sigma
      (Finsupp.single (.aroundVertex .north) (1 : ℤ))).charge.2 =
      (-5 : ℤ) ∧
    c60F68PhysicalPatchCurvature t₁ t₂ left right sigma ≠ 0 ∧
    (¬ ∃ cell :
      OriginalF45BracketTree.DepthRotationRoute.PresentedCell
        (OriginalF45BracketTree.DepthRotationRoute.squareLeftFirst left right)
        (OriginalF45BracketTree.DepthRotationRoute.squareRightFirst left right),
      c60F44FaceThreeEval
        (c60F112CrossEdgeFrame t₁ t₂ left right C i P).faceStep +
          c60F55SourceNative cell =
        c60F44OriginalF55Eval
          (c60F112CrossEdgeFrame t₁ t₂ left right C i P).rotationStep) := by
  exact ⟨
    c60F68PhysicalPatchCurvature_northSecondCharge t₁ t₂ left right sigma,
    c60F68PhysicalPatchCurvature_ne_zero t₁ t₂ left right sigma,
    (c60F112CrossEdgeOriginalF55_nonlift t₁ t₂ left right C i j W P Q).1⟩

#print axioms c60F112DistinctEdgeSharedFace_site
#print axioms c60F112DistinctEdge_noDirectPhysicalHom
#print axioms c60F112DistinctEdge_twoActualRestrictions
#print axioms c60F112CrossEdgeFace_fullNative
#print axioms c60F112CrossEdgeF55_fullNative
#print axioms c60F112CrossEdgeMixedSourceChange
#print axioms c60F112CrossEdgeMixedSourceChange_fullNative
#print axioms c60F112CrossEdgeMixedSourceChange_faithful
#print axioms c60F112CrossEdgeMixedSourceChange_square
#print axioms c60F112CrossEdgeTriplePhysicalCech
#print axioms c60F112CrossEdgeOriginalF55_nonlift
#print axioms c60F112CrossEdge_withNorthCurvature

end ActualCrossEdgeSources
end
end KUOS.DependentOriginationC60KuuCrossEdgePhysicalOverlapF47V5_277
