import KUOS.DependentOriginationC60KuuCrossEdgePhysicalOverlapF47V5_277
import KUOS.DependentOriginationC60PhysicalEdgeGrothendieckV5_224
import Mathlib.CategoryTheory.Grothendieck

namespace KUOS.DependentOriginationC60KuuWitnessedOverlapPathGrothendieckV5_278

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationGrayC60PresentedFaceTwoCellsV5_190
open KUOS.DependentOriginationGrayC60PresentedInterchangerV5_191
open KUOS.DependentOriginationGrayC60ThreeHomCategoriesV5_192
open KUOS.DependentOriginationGrayC60OriginalF55ThreeHomV5_192
open KUOS.DependentOriginationGrayC60IntegralChainComplexV5_160
open KUOS.DependentOriginationGrayC60F55SourcePhaseLockedAtlasV5_175
open KUOS.DependentOriginationGrayC60MixedBoundaryThreeHomV5_195
open KUOS.DependentOriginationGrayC60AllNinetyMixedBoundaryV5_196
open KUOS.DependentOriginationC60FiniteAtlasCechCoherenceV5_221
open KUOS.DependentOriginationC60PhysicalCechCurvatureRepairV5_222
open KUOS.DependentOriginationC60PhysicalIncidenceHigherNerveV5_223
open KUOS.DependentOriginationC60PhysicalEdgeGrothendieckV5_224
open KUOS.DependentOriginationC60KuuActualIncidenceOverlapRefinementV5_260
open KUOS.DependentOriginationC60KuuPhaseReconstructionObstructionV5_269
open KUOS.DependentOriginationC60KuuObservedGluingOriginalPhaseCurvatureV5_268
open KUOS.DependentOriginationC60KuuTwoActualFaceInterchangeV5_265
open KUOS.DependentOriginationC60KuuIndependentPhysicalFaceSiteSourceV5_274
open KUOS.DependentOriginationC60KuuIndependentFaceMixedF55FrameV5_275
open KUOS.DependentOriginationC60KuuCrossEdgePhysicalOverlapF47V5_277
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.278 / F112 sixth stage — arbitrary finite WITNESSED cross-edge
# original F47 source transport, true path category and Grothendieck

The old F70 physical edge base was DISCRETE because F69 does not
contain direct morphisms between different original C60 edges.
F112/v5.277 proved a faithful complete-native-preserving F47
source comparison guarded by a REAL original F106/F69 physical
star overlap and a proof that the two physical edges differ.

Here we DO NOT add fictitious arrows to the ORIGINAL F69 poset.
Instead construct a genuinely distinct, source-labeled category:
  * objects are actual edges in the supplied physical C60 atlas;
  * elementary arrows are CERTIFICATES of nonempty REAL F69
    incidence-star intersections between distinct physical edges;
  * arbitrary composable finite arrows are a proof-relevant
    INDUCTIVE path with each real overlap witness preserved;
  * composition is actual path concatenation, with PROVED
    category axioms, not an imposed global effective descent.

For an INDEPENDENT original odd-degree F42 cell pair at each real
physical edge, build a true F47 source functor for every finite
witnessed path. Prove on EVERY original mixed F47 three-Hom:
  * both integer charges AND independent ZMod2 phase are saved;
  * full-native functoriality and source Hom faithfulness;
  * ANY TWO paths with the same endpoints induce identical F47
    source-Hom values via a correctly dependent HEq;
  * arbitrary path concatenation respects source functor comp.

The resulting Cat-valued functor on the ACTUAL witnessed-overlap
path category supports a Mathlib Grothendieck TOTAL CATEGORY.
This is NOT a diagram on the original F69 incidence category.
Indeed the honest distinct-edge F69 no-Hom theorem gives a new
NO-GO to any incidence-preserving functor from this overlap-path
category to the original F69 poset, if any distinct overlap
witness exists. Physical edges are not magically comparable
in the original incidence partial order.

We keep the F55 nine-constructor Delta non-lift, the original
F110 phase reconstruction obstruction, and signed F68 original
north-pentagon second curvature charge -5, unchanged. Thus no
global original F42/F54/F55 effective three-descent is asserted.
-/

/-! ## I. A category of finite paths of REAL physical overlaps -/

/-- An object is a REAL C60 physical edge index, carrying the
exact physical atlas as a parameter so unrelated atlases cannot
silently share the same source Hom category. -/
structure C60F112WitnessedEdge
    {n : Nat} (C : C60F108BothFaceContexts n) where
  index : Fin n

/-- Proof-relevant ARBITRARY FINITE physical edge routes.
Every step is a certificate of two distinct genuine old C60
edges plus a real common F69 incidence-star site.
A path never supplies an unwitnessed cross-edge comparison. -/
inductive C60F112WitnessedOverlapPath
    {n : Nat} (C : C60F108BothFaceContexts n) :
    Fin n → Fin n → Type where
  | nil (i : Fin n) : C60F112WitnessedOverlapPath C i i
  | step {i j k : Fin n}
      (W : C60F112DistinctEdgeOverlap C i j)
      (tail : C60F112WitnessedOverlapPath C j k) :
      C60F112WitnessedOverlapPath C i k

/-- The actual original geometric site used at EVERY step of
the route; no F69 physical incidence witness is discarded. -/
def c60F112WitnessedOverlapSites
    {n : Nat} {C : C60F108BothFaceContexts n}
    {i j : Fin n} :
    C60F112WitnessedOverlapPath C i j →
      List C60F69PhysicalCellSite
  | .nil _ => []
  | .step W tail => W.common.1 :: c60F112WitnessedOverlapSites tail

/-- Genuine arbitrary finite witness-preserving route splicing.
This is composition on the freely generated physical-overlap
PATH CATEGORY, not composition of original F69 edge arrows. -/
def c60F112WitnessedOverlapAppend
    {n : Nat} {C : C60F108BothFaceContexts n}
    {i j k : Fin n}
    (first : C60F112WitnessedOverlapPath C i j)
    (second : C60F112WitnessedOverlapPath C j k) :
    C60F112WitnessedOverlapPath C i k :=
  match first with
  | .nil _ => second
  | .step W tail => .step W (c60F112WitnessedOverlapAppend tail second)

/-- The empty physical overlap route is LEFT identity. -/
theorem c60F112WitnessedOverlapAppend_nil_left
    {n : Nat} {C : C60F108BothFaceContexts n}
    {i j : Fin n} (p : C60F112WitnessedOverlapPath C i j) :
    c60F112WitnessedOverlapAppend (.nil i) p = p := rfl

/-- The empty physical overlap route is RIGHT identity on
actual proof-relevant overlap witnesses, not just their
fully native source functor images. -/
theorem c60F112WitnessedOverlapAppend_nil_right
    {n : Nat} {C : C60F108BothFaceContexts n}
    {i j : Fin n} (p : C60F112WitnessedOverlapPath C i j) :
    c60F112WitnessedOverlapAppend p (.nil j) = p := by
  induction p with
  | nil i => rfl
  | step W tail ih =>
      change C60F112WitnessedOverlapPath.step W
        (c60F112WitnessedOverlapAppend tail (.nil _)) =
          C60F112WitnessedOverlapPath.step W tail
      rw [ih]

/-- Arbitrary-length witness-path concatenation is ASSOCIATIVE
already at the RAW, typed REAL intersection witness level. -/
theorem c60F112WitnessedOverlapAppend_assoc
    {n : Nat} {C : C60F108BothFaceContexts n}
    {i j k l : Fin n}
    (p : C60F112WitnessedOverlapPath C i j)
    (q : C60F112WitnessedOverlapPath C j k)
    (r : C60F112WitnessedOverlapPath C k l) :
    c60F112WitnessedOverlapAppend
      (c60F112WitnessedOverlapAppend p q) r =
    c60F112WitnessedOverlapAppend p
      (c60F112WitnessedOverlapAppend q r) := by
  induction p with
  | nil i => rfl
  | step W tail ih =>
      change C60F112WitnessedOverlapPath.step W
          (c60F112WitnessedOverlapAppend
            (c60F112WitnessedOverlapAppend tail q) r) =
        C60F112WitnessedOverlapPath.step W
          (c60F112WitnessedOverlapAppend tail
            (c60F112WitnessedOverlapAppend q r))
      rw [ih]

/-- AN HONEST MATHLIB CATEGORY whose arrows are arbitrary
finite genuine distinct-edge overlap witness paths.
Unlike original F69 incidence, arrows between physically
different edges are VALID here exactly because their
successive intersections have certified ACTUAL sites. -/
instance c60F112WitnessedOverlapCategory
    {n : Nat} (C : C60F108BothFaceContexts n) :
    Category (C60F112WitnessedEdge C) where
  Hom X Y := C60F112WitnessedOverlapPath C X.index Y.index
  id X := .nil X.index
  comp f g := c60F112WitnessedOverlapAppend f g
  id_comp := by intro X Y f; rfl
  comp_id := by
    intro X Y f
    exact c60F112WitnessedOverlapAppend_nil_right f
  assoc := by
    intro W X Y Z f g h
    exact c60F112WitnessedOverlapAppend_assoc f g h

/-- ONE true overlap is a REAL morphism in the newly
constructed path category. It is NOT an original direct
F69 edge-to-edge arrow (none exists for distinct edges). -/
def c60F112WitnessedSingleArrow
    {n : Nat} (C : C60F108BothFaceContexts n)
    {i j : Fin n} (W : C60F112DistinctEdgeOverlap C i j) :
    (⟨i⟩ : C60F112WitnessedEdge C) ⟶
      (⟨j⟩ : C60F112WitnessedEdge C) :=
  .step W (.nil j)

/-- A geometric NO-GO: if there is a single witnessed
physical overlap between DISTINCT original physical edges,
then this new overlap-path category cannot be projected to
the original F69 physical incidence CATEGORY by a functor
identically sending each edge to its original old F69 edge
site: that would invent a nonexistent edge-to-edge incidence.
This does NOT obstruct a separately typed span/bicategory. -/
theorem c60F112NoIncidenceEdgePreservingFunctor
    {n : Nat} (C : C60F108BothFaceContexts n)
    {i j : Fin n} (W : C60F112DistinctEdgeOverlap C i j) :
    ¬ ∃ F : C60F112WitnessedEdge C ⥤ C60F69PhysicalCellSite,
      ∀ k : Fin n,
        F.obj (⟨k⟩ : C60F112WitnessedEdge C) =
          C60F69PhysicalCellSite.edge (C.edge k) := by
  rintro ⟨F, hF⟩
  have hinc :
      C60F69PhysicalCellSite.edge (C.edge i) ≤
        C60F69PhysicalCellSite.edge (C.edge j) := by
    rw [← hF i, ← hF j]
    exact CategoryTheory.leOfHom
      (F.map (c60F112WitnessedSingleArrow C W))
  exact W.edge_ne hinc

/-! ## II. Original four-boundary source functors for ANY finite path -/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

section OriginalF47WitnessedPaths
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

/-- Each actual C60 edge independently retains its ORIGINAL
two real polygon F42 cells at their true separate base darts,
and the resulting F43/F54/F55 typed four-boundary F47 fibre. -/
abbrev c60F112WitnessedF47Fibre
    {n : Nat} (C : C60F108BothFaceContexts n)
    (P : (i : Fin n) → C60F112IndependentOddFacePair C i)
    (i : Fin n) :=
  C60F47BoundaryPoint
    (c60F112CrossEdgeFrame t₁ t₂ left right C i (P i))

/-- Actual recursively COMPOSED categorical source F47
transport along ANY finite path of real distinct-edge physical
F69 incidence overlaps; no hidden synthetic cross-edge step. -/
def c60F112WitnessedF47Transport
    {n : Nat} (C : C60F108BothFaceContexts n)
    (P : (i : Fin n) → C60F112IndependentOddFacePair C i)
    {i j : Fin n}
    (path : C60F112WitnessedOverlapPath C i j) :
    c60F112WitnessedF47Fibre t₁ t₂ left right C P i ⥤
      c60F112WitnessedF47Fibre t₁ t₂ left right C P j :=
  match path with
  | .nil _ => 𝟭 _
  | .step (i := i) (j := j) W rest =>
      c60F112CrossEdgeMixedSourceChange
        t₁ t₂ left right C i j W (P i) (P j) ⋙
      c60F112WitnessedF47Transport C P rest

/-- The ENTIRE full original Gray source native image on
EVERY F47 three-Hom is preserved after arbitrary different
real physical edge overlap steps: both independent integer
charges and the nontrivial ZMod2 exchange phase are kept. -/
theorem c60F112WitnessedF47Transport_fullNative
    {n : Nat} (C : C60F108BothFaceContexts n)
    (P : (i : Fin n) → C60F112IndependentOddFacePair C i)
    {i j : Fin n} (path : C60F112WitnessedOverlapPath C i j) :
    ∀ {X Y : c60F112WitnessedF47Fibre t₁ t₂ left right C P i}
      (f : X ⟶ Y),
      c60F47MixedEval
        ((c60F112WitnessedF47Transport
          t₁ t₂ left right C P path).map f) =
        c60F47MixedEval f := by
  induction path with
  | nil i =>
      intro X Y f
      rfl
  | @step i j k W rest ih =>
      intro X Y f
      change c60F47MixedEval
        ((c60F112WitnessedF47Transport
          t₁ t₂ left right C P rest).map
          ((c60F112CrossEdgeMixedSourceChange
            t₁ t₂ left right C i j W (P i) (P j)).map f)) =
        c60F47MixedEval f
      exact (ih ((c60F112CrossEdgeMixedSourceChange
        t₁ t₂ left right C i j W (P i) (P j)).map f)).trans
          (c60F112CrossEdgeMixedSourceChange_fullNative
            t₁ t₂ left right C i j W (P i) (P j) f)

/-- Path transport remains faithful on ALL source F47 three-Homs,
not merely on the old F77 phase-forgetting observation. -/
theorem c60F112WitnessedF47Transport_faithful
    {n : Nat} (C : C60F108BothFaceContexts n)
    (P : (i : Fin n) → C60F112IndependentOddFacePair C i)
    {i j : Fin n} (path : C60F112WitnessedOverlapPath C i j)
    {X Y : c60F112WitnessedF47Fibre t₁ t₂ left right C P i}
    {f g : X ⟶ Y}
    (h :
      (c60F112WitnessedF47Transport
        t₁ t₂ left right C P path).map f =
      (c60F112WitnessedF47Transport
        t₁ t₂ left right C P path).map g) : f = g := by
  apply c60F47MixedGrayFunctor_faithful
    (c60F112CrossEdgeFrame t₁ t₂ left right C i (P i))
  have hh := congrArg (fun z => c60F47MixedEval z) h
  change c60F47MixedEval
      ((c60F112WitnessedF47Transport t₁ t₂ left right C P path).map f) =
    c60F47MixedEval
      ((c60F112WitnessedF47Transport t₁ t₂ left right C P path).map g) at hh
  rw [c60F112WitnessedF47Transport_fullNative,
    c60F112WitnessedF47Transport_fullNative] at hh
  exact hh

/-- ALL path transports act on the four genuine F47
face/rotation boundary tags without ever equating their
different source original F42 and original F54 types. -/
theorem c60F112WitnessedF47Transport_objects
    {n : Nat} (C : C60F108BothFaceContexts n)
    (P : (i : Fin n) → C60F112IndependentOddFacePair C i)
    {i j : Fin n} (path : C60F112WitnessedOverlapPath C i j) :
    ((c60F112WitnessedF47Transport
      t₁ t₂ left right C P path).obj .faceBefore =
        (.faceBefore : c60F112WitnessedF47Fibre
          t₁ t₂ left right C P j)) ∧
    ((c60F112WitnessedF47Transport
      t₁ t₂ left right C P path).obj .faceAfter =
        (.faceAfter : c60F112WitnessedF47Fibre
          t₁ t₂ left right C P j)) ∧
    ((c60F112WitnessedF47Transport
      t₁ t₂ left right C P path).obj .rotationBefore =
        (.rotationBefore : c60F112WitnessedF47Fibre
          t₁ t₂ left right C P j)) ∧
    ((c60F112WitnessedF47Transport
      t₁ t₂ left right C P path).obj .rotationAfter =
        (.rotationAfter : c60F112WitnessedF47Fibre
          t₁ t₂ left right C P j)) := by
  induction path with
  | nil i =>
      exact ⟨rfl, rfl, rfl, rfl⟩
  | @step i j k W rest ih =>
      change
        ((c60F112WitnessedF47Transport
          t₁ t₂ left right C P rest).obj .faceBefore = .faceBefore) ∧
        ((c60F112WitnessedF47Transport
          t₁ t₂ left right C P rest).obj .faceAfter = .faceAfter) ∧
        ((c60F112WitnessedF47Transport
          t₁ t₂ left right C P rest).obj .rotationBefore = .rotationBefore) ∧
        ((c60F112WitnessedF47Transport
          t₁ t₂ left right C P rest).obj .rotationAfter = .rotationAfter)
      exact ih

/-- Canonical REINDEXING of the four distinct originally typed
source boundary tags from one real physical F47 fibre to another.
It is merely an object-tag operation, NOT an equality of their
underlying ORIGINAL F42 and ORIGINAL F54 source 2-cell witnesses. -/
def c60F112WitnessedReindexTag
    {n : Nat} (C : C60F108BothFaceContexts n)
    (P : (i : Fin n) → C60F112IndependentOddFacePair C i)
    {i j : Fin n}
    (X : c60F112WitnessedF47Fibre t₁ t₂ left right C P i) :
    c60F112WitnessedF47Fibre t₁ t₂ left right C P j :=
  match X with
  | .faceBefore => .faceBefore
  | .faceAfter => .faceAfter
  | .rotationBefore => .rotationBefore
  | .rotationAfter => .rotationAfter

/-- All ARBITRARILY LONG witnessed geometric route functors
act on the genuine four F47 boundary tags exactly by their
explicit canonical tag reindexing; this is PROPOSITIONAL and
does not demand impossible definitional equality of recursive
functors whose paths are arbitrary variables. -/
theorem c60F112WitnessedF47Transport_obj
    {n : Nat} (C : C60F108BothFaceContexts n)
    (P : (i : Fin n) → C60F112IndependentOddFacePair C i)
    {i j : Fin n}
    (path : C60F112WitnessedOverlapPath C i j)
    (X : c60F112WitnessedF47Fibre t₁ t₂ left right C P i) :
    (c60F112WitnessedF47Transport
      t₁ t₂ left right C P path).obj X =
    c60F112WitnessedReindexTag t₁ t₂ left right C P X := by
  cases X with
  | faceBefore =>
      exact (c60F112WitnessedF47Transport_objects
        t₁ t₂ left right C P path).1
  | faceAfter =>
      exact (c60F112WitnessedF47Transport_objects
        t₁ t₂ left right C P path).2.1
  | rotationBefore =>
      exact (c60F112WitnessedF47Transport_objects
        t₁ t₂ left right C P path).2.2.1
  | rotationAfter =>
      exact (c60F112WitnessedF47Transport_objects
        t₁ t₂ left right C P path).2.2.2

/-- Two arbitrarily long routes of actual C60 star overlaps
with the SAME physical start and end edges yield equivalent
complete F47 source arrows. HEq is essential for the
different dependent original F42/F54 Hom endpoint types. -/
theorem c60F112WitnessedF47AnyPaths_HEq
    {n : Nat} (C : C60F108BothFaceContexts n)
    (P : (i : Fin n) → C60F112IndependentOddFacePair C i)
    {i j : Fin n}
    (first second : C60F112WitnessedOverlapPath C i j)
    {X Y : c60F112WitnessedF47Fibre t₁ t₂ left right C P i}
    (f : X ⟶ Y) :
    HEq
      ((c60F112WitnessedF47Transport
        t₁ t₂ left right C P first).map f)
      ((c60F112WitnessedF47Transport
        t₁ t₂ left right C P second).map f) := by
  have hxFirst := c60F112WitnessedF47Transport_obj
    t₁ t₂ left right C P first X
  have hyFirst := c60F112WitnessedF47Transport_obj
    t₁ t₂ left right C P first Y
  have hxSecond := c60F112WitnessedF47Transport_obj
    t₁ t₂ left right C P second X
  have hySecond := c60F112WitnessedF47Transport_obj
    t₁ t₂ left right C P second Y
  cases X <;> cases Y
  all_goals
  cases hxFirst
  cases hyFirst
  cases hxSecond
  cases hySecond
  apply heq_of_eq
  apply c60F47MixedGrayFunctor_faithful
    (c60F112CrossEdgeFrame t₁ t₂ left right C j (P j))
  calc
      c60F47MixedEval
          ((c60F112WitnessedF47Transport
            t₁ t₂ left right C P first).map f) =
        c60F47MixedEval f :=
          c60F112WitnessedF47Transport_fullNative
            t₁ t₂ left right C P first f
      _ = c60F47MixedEval
          ((c60F112WitnessedF47Transport
            t₁ t₂ left right C P second).map f) :=
          (c60F112WitnessedF47Transport_fullNative
            t₁ t₂ left right C P second f).symm

/-- Splicing ANY two real witnessed physical-edge routes
commutes with the ACTUAL F47 source functor composition.
The proof is INDUCTION on source witness paths, not a
fragile implicit change-of-object hom equality: the only
coherence required is the proven functor-category associator. -/
theorem c60F112WitnessedF47Transport_append
    {n : Nat} (C : C60F108BothFaceContexts n)
    (P : (i : Fin n) → C60F112IndependentOddFacePair C i)
    {i j k : Fin n}
    (first : C60F112WitnessedOverlapPath C i j)
    (second : C60F112WitnessedOverlapPath C j k) :
    c60F112WitnessedF47Transport t₁ t₂ left right C P
        (c60F112WitnessedOverlapAppend first second) =
    c60F112WitnessedF47Transport t₁ t₂ left right C P first ⋙
      c60F112WitnessedF47Transport t₁ t₂ left right C P second := by
  induction first with
  | nil i =>
      change
        c60F112WitnessedF47Transport t₁ t₂ left right C P second =
        𝟭 _ ⋙
          c60F112WitnessedF47Transport t₁ t₂ left right C P second
      exact (Functor.id_comp
        (c60F112WitnessedF47Transport t₁ t₂ left right C P second)).symm
  | @step i j k W rest ih =>
      change
        c60F112CrossEdgeMixedSourceChange
            t₁ t₂ left right C i j W (P i) (P j) ⋙
          c60F112WitnessedF47Transport t₁ t₂ left right C P
            (c60F112WitnessedOverlapAppend rest second) =
        (c60F112CrossEdgeMixedSourceChange
            t₁ t₂ left right C i j W (P i) (P j) ⋙
          c60F112WitnessedF47Transport t₁ t₂ left right C P rest) ⋙
          c60F112WitnessedF47Transport t₁ t₂ left right C P second
      rw [ih]
      exact (Functor.assoc _ _ _).symm

/-- A fully CONSTRUCTED Cat-valued diagram over the non-discrete
category of arbitrary finite TRUE physical overlap paths.
This is a new witness-path category, NOT the old F69 poset. -/
def c60F112WitnessedF47Diagram
    {n : Nat} (C : C60F108BothFaceContexts n)
    (P : (i : Fin n) → C60F112IndependentOddFacePair C i) :
    C60F112WitnessedEdge C ⥤ Cat where
  obj i := Cat.of (c60F112WitnessedF47Fibre
    t₁ t₂ left right C P i.index)
  map := fun {_ _} f =>
    (c60F112WitnessedF47Transport t₁ t₂ left right C P f).toCatHom
  map_id := by
    intro X
    rfl
  map_comp := by
    intro X Y Z f g
    apply Cat.Hom.ext
    simp only [Cat.Hom.comp_toFunctor, Functor.toCatHom_toFunctor]
    exact c60F112WitnessedF47Transport_append
      t₁ t₂ left right C P f g

/-- The genuine Mathlib Grothendieck category of original F47
face/rotation-boundary pairs over ALL finite real witnessed
cross-edge overlap paths. Its base has nontrivial verified
physical-edge comparisons; unlike the previous F70 base
it is NOT discrete. -/
abbrev c60F112WitnessedF47Grothendieck
    {n : Nat} (C : C60F108BothFaceContexts n)
    (P : (i : Fin n) → C60F112IndependentOddFacePair C i) :=
  Grothendieck (c60F112WitnessedF47Diagram
    t₁ t₂ left right C P)

/-- Exact native projection to the verified witness-path base;
it MUST NOT be conflated with a functor to the original F69
incidence partial-order category (which has no edge-edge Homs). -/
def c60F112WitnessedF47TotalProjection
    {n : Nat} (C : C60F108BothFaceContexts n)
    (P : (i : Fin n) → C60F112IndependentOddFacePair C i) :
    c60F112WitnessedF47Grothendieck
      t₁ t₂ left right C P ⥤ C60F112WitnessedEdge C :=
  Grothendieck.forget
    (c60F112WitnessedF47Diagram t₁ t₂ left right C P)

/-! ## III. Native obstruction and the exact scope of this total category -/

/-- Even after EVERY proof-relevant finite overlap path admits a
full native F47 transport, the original F55 nine-constructor
Delta receiver remains IMPOSSIBLE at each original endpoint. -/
theorem c60F112WitnessedF47Path_originalF55Nonlift
    {n : Nat} (C : C60F108BothFaceContexts n)
    (P : (i : Fin n) → C60F112IndependentOddFacePair C i)
    {i j : Fin n} (_path : C60F112WitnessedOverlapPath C i j) :
    ¬ ∃ cell :
      OriginalF45BracketTree.DepthRotationRoute.PresentedCell
        (OriginalF45BracketTree.DepthRotationRoute.squareLeftFirst left right)
        (OriginalF45BracketTree.DepthRotationRoute.squareRightFirst left right),
      c60F44FaceThreeEval
        (c60F112CrossEdgeFrame t₁ t₂ left right C j (P j)).faceStep +
        c60F55SourceNative cell =
      c60F44OriginalF55Eval
        (c60F112CrossEdgeFrame t₁ t₂ left right C j (P j)).rotationStep :=
  c60F112IndependentFaceOriginalMixed_noF55Lift
    t₁ t₂ left right C j (P j)

/-- The existence of a genuine Cat-valued diagram and Mathlib
Grothendieck total category on the witnessed-overlap path base
does NOT trivialize the genuinely CURVED original physical
F68 cochain: its north signed second charge is -5 and an
uncorrected vertex gauge is impossible. -/
theorem c60F112WitnessedF47Total_originalCurvatureObstruction
    {n : Nat} (C : C60F108BothFaceContexts n)
    (_P : (i : Fin n) → C60F112IndependentOddFacePair C i)
    (sigma : C60F67Atlas) :
    (c60F68PhysicalPatchCurvature t₁ t₂ left right sigma
      (Finsupp.single (.aroundVertex .north) (1 : ℤ))).charge.2 =
        (-5 : ℤ) ∧
    c60F68PhysicalPatchCurvature t₁ t₂ left right sigma ≠ 0 ∧
    (¬ ∃ vertexGauge :
        C60IntegralZeroChains →ₗ[ℤ] GradedThreeCell 0 0,
      c60F68AtlasEdgeCochain t₁ t₂ left right sigma =
        vertexGauge.comp c60IntegralBoundaryOne) := by
  exact ⟨
    c60F68PhysicalPatchCurvature_northSecondCharge
      t₁ t₂ left right sigma,
    c60F68PhysicalPatchCurvature_ne_zero
      t₁ t₂ left right sigma,
    c60F110UncorrectedPhysicalGauge_impossible
      t₁ t₂ left right sigma⟩

#print axioms c60F112WitnessedOverlapAppend_nil_right
#print axioms c60F112WitnessedOverlapAppend_assoc
#print axioms c60F112WitnessedOverlapCategory
#print axioms c60F112WitnessedSingleArrow
#print axioms c60F112NoIncidenceEdgePreservingFunctor
#print axioms c60F112WitnessedF47Transport_fullNative
#print axioms c60F112WitnessedF47Transport_faithful
#print axioms c60F112WitnessedF47Transport_objects
#print axioms c60F112WitnessedF47Transport_obj
#print axioms c60F112WitnessedF47AnyPaths_HEq
#print axioms c60F112WitnessedF47Transport_append
#print axioms c60F112WitnessedF47Diagram
#print axioms c60F112WitnessedF47Grothendieck
#print axioms c60F112WitnessedF47TotalProjection
#print axioms c60F112WitnessedF47Path_originalF55Nonlift
#print axioms c60F112WitnessedF47Total_originalCurvatureObstruction

end OriginalF47WitnessedPaths
end
end KUOS.DependentOriginationC60KuuWitnessedOverlapPathGrothendieckV5_278
