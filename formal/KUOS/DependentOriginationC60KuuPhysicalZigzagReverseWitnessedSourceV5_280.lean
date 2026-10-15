import KUOS.DependentOriginationC60KuuWitnessedF69IncidenceZigzagV5_279

namespace KUOS.DependentOriginationC60KuuPhysicalZigzagReverseWitnessedSourceV5_280

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationGrayC60PresentedFaceTwoCellsV5_190
open KUOS.DependentOriginationGrayC60ThreeHomCategoriesV5_192
open KUOS.DependentOriginationGrayC60OriginalF55ThreeHomV5_192
open KUOS.DependentOriginationGrayC60F55SourcePhaseLockedAtlasV5_175
open KUOS.DependentOriginationGrayC60MixedBoundaryThreeHomV5_195
open KUOS.DependentOriginationGrayC60AllNinetyMixedBoundaryV5_196
open KUOS.DependentOriginationGrayC60IntegralChainComplexV5_160
open KUOS.DependentOriginationC60FiniteAtlasCechCoherenceV5_221
open KUOS.DependentOriginationC60PhysicalCechCurvatureRepairV5_222
open KUOS.DependentOriginationC60PhysicalIncidenceHigherNerveV5_223
open KUOS.DependentOriginationC60KuuActualIncidenceOverlapRefinementV5_260
open KUOS.DependentOriginationC60KuuTwoActualFaceInterchangeV5_265
open KUOS.DependentOriginationC60KuuIndependentPhysicalFaceSiteSourceV5_274
open KUOS.DependentOriginationC60KuuIndependentFaceMixedF55FrameV5_275
open KUOS.DependentOriginationC60KuuCrossEdgePhysicalOverlapF47V5_277
open KUOS.DependentOriginationC60KuuWitnessedOverlapPathGrothendieckV5_278
open KUOS.DependentOriginationC60KuuWitnessedF69IncidenceZigzagV5_279
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.280 / F112 stage 8 — formal reversal, source F47 round-trip and RAW obstruction

The original F69 C60 partial order has NO arrows between distinct old
physical edges. F112 stage 6 gave the true category of arbitrary finite
paths of original F106 overlap witnesses, and stage 7 mapped these paths
to F69-incidence FORMAL ZIGZAGS, each built exclusively from genuine
forward F69 inequalities and genuinely FORMALLY REVERSED inequalities.

This stage makes the mathematically essential distinction explicit:
  * reversing a REAL overlap step exchanges the two original physical
    edges but RETAINS the very same original F69 common site;
  * reversing an arbitrary finite witness path is a constructed
    path with all actual geometric witnesses and reversed order;
  * reversing a finite original F69 zigzag interchanges its formal
    forward/backward legs WITHOUT asserting those reverse morphisms
    in the original F69 partial-order category;
  * the reversible source-quotient F47 transport preserves BOTH Int
    charges and the independent nontrivial ZMod2 phase, and a
    genuine round trip acts as ID on all original F47 3-Homs;
  * in contrast, a raw physical witnessed path followed by its
    formal reverse is NOT the empty path: the actual overlap
    witnesses cannot be erased by imposing a false old F69 equality.

Thus source-quotient path equivalence is a proven TARGET PROPERTY,
not an equation of original F69 incidence paths, raw F42 or F54
boundary expressions. Original F55 Delta no-lift and north
pentagon signed physical F68 charge -5 remain unchanged.
This does NOT construct global effective original source 3-descent.
-/

/-! ## I. Original physical F69 site-preserving overlap reversal -/

/-- Reverse a certified pair of DIFFERENT original physical C60
edges. The common ORIGINAL F69 cell is retained literally; its
membership is reproved for the swapped two-edge Finset intersection. -/
def c60F114SwapActualOverlap
    {n : Nat} (C : C60F108BothFaceContexts n)
    {i j : Fin n} (W : C60F112DistinctEdgeOverlap C i j) :
    C60F112DistinctEdgeOverlap C j i where
  edge_ne := W.edge_ne.symm
  common := ⟨W.common.1, by
    intro k hk
    have hki : k ∈ ({i, j} : Finset (Fin n)) := by
      simp only [Finset.mem_insert, Finset.mem_singleton] at hk ⊢
      tauto
    exact W.common.2 k hki⟩

/-- The ORIGINAL common physical site is not moved or replaced by
a synthetic auxiliary C60 face when the edge comparison reverses. -/
theorem c60F114SwapActualOverlap_site
    {n : Nat} (C : C60F108BothFaceContexts n)
    {i j : Fin n} (W : C60F112DistinctEdgeOverlap C i j) :
    (c60F114SwapActualOverlap C W).common.1 = W.common.1 := rfl

/-- Reversing the *same genuine overlap* twice returns the exact
original proof-carrying site (subtype evidence is proof-irrelevant).
It is NOT a new equality of two DISTINCT physical edges. -/
theorem c60F114SwapActualOverlap_involutive
    {n : Nat} (C : C60F108BothFaceContexts n)
    {i j : Fin n} (W : C60F112DistinctEdgeOverlap C i j) :
    c60F114SwapActualOverlap C
      (c60F114SwapActualOverlap C W) = W := by
  cases W with
  | mk hne common =>
      cases common with
      | mk site hsite => rfl

/-- The one-step physical edge comparison retains the precise
REAL overlap witness in the old F106 incidence-star geometry. -/
def c60F114SingleWitnessedOverlap
    {n : Nat} {C : C60F108BothFaceContexts n}
    {i j : Fin n} (W : C60F112DistinctEdgeOverlap C i j) :
    C60F112WitnessedOverlapPath C i j :=
  .step W (.nil j)

/-- Reverse ANY finite chain of distinct, genuinely overlapping
C60 physical edges. Each step is an independently witnessed
original F69/F106 incidence intersection, in reverse order. -/
def c60F114ReverseWitnessedPath
    {n : Nat} {C : C60F108BothFaceContexts n}
    {i j : Fin n} :
    C60F112WitnessedOverlapPath C i j →
    C60F112WitnessedOverlapPath C j i
  | .nil i => .nil i
  | .step (i := i) W tail =>
      c60F112WitnessedOverlapAppend
        (c60F114ReverseWitnessedPath tail)
        (c60F114SingleWitnessedOverlap
          (c60F114SwapActualOverlap C W))

/-- A single REAL overlap reverses to the same actual F69
intersection site, with the physical edges exchanged. -/
theorem c60F114ReverseWitnessedSingle
    {n : Nat} {C : C60F108BothFaceContexts n}
    {i j : Fin n} (W : C60F112DistinctEdgeOverlap C i j) :
    c60F114ReverseWitnessedPath
      (c60F114SingleWitnessedOverlap W) =
    c60F114SingleWitnessedOverlap
      (c60F114SwapActualOverlap C W) := rfl

/-- Reversal changes the order of ANY two concatenated
genuine physical overlap routes, preserving EVERY old shared
site certificate. Nothing is quotienting the raw route. -/
theorem c60F114ReverseWitnessed_append
    {n : Nat} {C : C60F108BothFaceContexts n}
    {i j k : Fin n}
    (first : C60F112WitnessedOverlapPath C i j)
    (second : C60F112WitnessedOverlapPath C j k) :
    c60F114ReverseWitnessedPath
      (c60F112WitnessedOverlapAppend first second) =
    c60F112WitnessedOverlapAppend
      (c60F114ReverseWitnessedPath second)
      (c60F114ReverseWitnessedPath first) := by
  induction first with
  | nil i =>
      change c60F114ReverseWitnessedPath second =
        c60F112WitnessedOverlapAppend
          (c60F114ReverseWitnessedPath second) (.nil i)
      exact (c60F112WitnessedOverlapAppend_nil_right _).symm
  | @step i j k W tail ih =>
      change
        c60F112WitnessedOverlapAppend
          (c60F114ReverseWitnessedPath
            (c60F112WitnessedOverlapAppend tail second))
          (c60F114SingleWitnessedOverlap
            (c60F114SwapActualOverlap C W)) =
        c60F112WitnessedOverlapAppend
          (c60F114ReverseWitnessedPath second)
          (c60F112WitnessedOverlapAppend
            (c60F114ReverseWitnessedPath tail)
            (c60F114SingleWitnessedOverlap
              (c60F114SwapActualOverlap C W)))
      rw [ih]
      exact c60F112WitnessedOverlapAppend_assoc _ _ _

/-- Proof-level involution on finite genuine C60 physical
intersection paths; no original incidence witnesses are lost. -/
theorem c60F114ReverseWitnessed_involutive
    {n : Nat} {C : C60F108BothFaceContexts n}
    {i j : Fin n} (path : C60F112WitnessedOverlapPath C i j) :
    c60F114ReverseWitnessedPath
      (c60F114ReverseWitnessedPath path) = path := by
  induction path with
  | nil i => rfl
  | @step i j k W tail ih =>
      change
        c60F114ReverseWitnessedPath
          (c60F112WitnessedOverlapAppend
            (c60F114ReverseWitnessedPath tail)
            (c60F114SingleWitnessedOverlap
              (c60F114SwapActualOverlap C W))) =
          C60F112WitnessedOverlapPath.step W tail
      rw [c60F114ReverseWitnessed_append,
        c60F114ReverseWitnessedSingle, ih,
        c60F114SwapActualOverlap_involutive]
      rfl

/-! ## II. Formal reversal of TRUE oriented F69 incidence legs -/

/-- A formal reverse reverses and swaps true old F69 INCIDENCE
leg orientations. A backward generator remains FORMAL, and is
never asserted to be an actual opposite-direction old F69 Hom. -/
def c60F114ReverseF69Zigzag
    {s t : C60F69PhysicalCellSite} :
    C60F113IncidenceZigzag s t →
    C60F113IncidenceZigzag t s
  | .nil s => .nil s
  | .forward (s := s) h rest =>
      c60F113ZigzagAppend (c60F114ReverseF69Zigzag rest)
        (.backward h (.nil s))
  | .backward (s := s) h rest =>
      c60F113ZigzagAppend (c60F114ReverseF69Zigzag rest)
        (.forward h (.nil s))

/-- The F69 zigzag's *raw* number of genuinely oriented old
incidence legs, counting also the formally reversed legs. -/
def c60F114F69ZigzagLength
    {s t : C60F69PhysicalCellSite} :
    C60F113IncidenceZigzag s t → Nat
  | .nil _ => 0
  | .forward _ rest => c60F114F69ZigzagLength rest + 1
  | .backward _ rest => c60F114F69ZigzagLength rest + 1

/-- A TRUE incidence leg and its formal opposite each retain
one unit of raw geometric path length. Reverse incidence is
NOT a genuine F69 Hom made invertible in the old poset. -/
theorem c60F114F69ZigzagLength_append
    {s t u : C60F69PhysicalCellSite}
    (p : C60F113IncidenceZigzag s t)
    (q : C60F113IncidenceZigzag t u) :
    c60F114F69ZigzagLength (c60F113ZigzagAppend p q) =
      c60F114F69ZigzagLength p + c60F114F69ZigzagLength q := by
  induction p with
  | nil _ => rfl
  | forward h rest ih =>
      change c60F114F69ZigzagLength
          (c60F113ZigzagAppend rest q) + 1 =
        (c60F114F69ZigzagLength rest + 1) +
          c60F114F69ZigzagLength q
      rw [ih]
      omega
  | backward h rest ih =>
      change c60F114F69ZigzagLength
          (c60F113ZigzagAppend rest q) + 1 =
        (c60F114F69ZigzagLength rest + 1) +
          c60F114F69ZigzagLength q
      rw [ih]
      omega

/-- Source physical-overlap route length counts the actual
intersection certificates, not the F77 observed charges. -/
def c60F114WitnessedLength
    {n : Nat} {C : C60F108BothFaceContexts n}
    {i j : Fin n} :
    C60F112WitnessedOverlapPath C i j → Nat
  | .nil _ => 0
  | .step _ tail => c60F114WitnessedLength tail + 1

/-- The original genuine overlap path and its formal reverse
do NOT become literally empty in the FREE physical path
category. Even one distinct-edge overlap carries two raw
witnesses when traversed forward and back. -/
theorem c60F114RoundTripRawWitnesses_nontrivial
    {n : Nat} {C : C60F108BothFaceContexts n}
    {i j : Fin n} (W : C60F112DistinctEdgeOverlap C i j) :
    c60F112WitnessedOverlapAppend
      (c60F114SingleWitnessedOverlap W)
      (c60F114ReverseWitnessedPath
        (c60F114SingleWitnessedOverlap W)) ≠
    (C60F112WitnessedOverlapPath.nil i) := by
  intro h
  have hlen := congrArg c60F114WitnessedLength h
  simp [c60F114SingleWitnessedOverlap,
    c60F114ReverseWitnessedPath,
    c60F114WitnessedLength,
    c60F112WitnessedOverlapAppend] at hlen

/-! ## III. Original F47 source round-trip becomes identity -/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

section ActualOriginalF47Reverse
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

/-- ANY arbitrarily long true C60 witnessed-overlap path has
a source F47 reverse transport that is a RIGHT INVERSE in
the entire ORIGINAL F47 quotient FUNCTOR CATEGORY, not
just equal after losing the parity phase under F77. -/
theorem c60F114WitnessedF47RoundTrip_rightInverse
    {n : Nat} (C : C60F108BothFaceContexts n)
    (P : (i : Fin n) → C60F112IndependentOddFacePair C i)
    {i j : Fin n} (path : C60F112WitnessedOverlapPath C i j) :
    c60F112WitnessedF47Transport t₁ t₂ left right C P path ⋙
      c60F112WitnessedF47Transport t₁ t₂ left right C P
        (c60F114ReverseWitnessedPath path) =
      𝟭 (c60F112WitnessedF47Fibre t₁ t₂ left right C P i) := by
  calc
    _ = c60F112WitnessedF47Transport t₁ t₂ left right C P
          (c60F112WitnessedOverlapAppend path
            (c60F114ReverseWitnessedPath path)) :=
      (c60F112WitnessedF47Transport_append t₁ t₂ left right C P _ _).symm
    _ = c60F112WitnessedF47Transport t₁ t₂ left right C P
          (.nil i) :=
      c60F112WitnessedF47AnyPaths_functor t₁ t₂ left right C P _ _
    _ = 𝟭 _ := rfl

/-- LEFT inverse as well: the formally reversed genuine
intersection path provides an actual source-level F47 inverse
for the entire functor, without asserting a raw F69 inverse. -/
theorem c60F114WitnessedF47RoundTrip_leftInverse
    {n : Nat} (C : C60F108BothFaceContexts n)
    (P : (i : Fin n) → C60F112IndependentOddFacePair C i)
    {i j : Fin n} (path : C60F112WitnessedOverlapPath C i j) :
    c60F112WitnessedF47Transport t₁ t₂ left right C P
        (c60F114ReverseWitnessedPath path) ⋙
      c60F112WitnessedF47Transport t₁ t₂ left right C P path =
      𝟭 (c60F112WitnessedF47Fibre t₁ t₂ left right C P j) := by
  exact c60F114WitnessedF47RoundTrip_rightInverse
    t₁ t₂ left right C P (c60F114ReverseWitnessedPath path)
      |>.trans (by rw [c60F114ReverseWitnessed_involutive])

/-- Concrete original F47 arrow statement: full native F47
source round trip is identity on EVERY actual original
four-boundary three-Hom, including the nontrivial Gray phase. -/
theorem c60F114WitnessedF47RoundTrip_map_identity
    {n : Nat} (C : C60F108BothFaceContexts n)
    (P : (i : Fin n) → C60F112IndependentOddFacePair C i)
    {i j : Fin n} (path : C60F112WitnessedOverlapPath C i j)
    {X Y : c60F112WitnessedF47Fibre t₁ t₂ left right C P i}
    (f : X ⟶ Y) :
    (c60F112WitnessedF47Transport t₁ t₂ left right C P path ⋙
      c60F112WitnessedF47Transport t₁ t₂ left right C P
        (c60F114ReverseWitnessedPath path)).map f = f := by
  rw [c60F114WitnessedF47RoundTrip_rightInverse]
  rfl

/-- Keep BOTH layers visible simultaneously: an actual old
C60 witness is NOT empty after raw backtracking, yet the
entire ORIGINAL F47 four-boundary source functor is identity
after that path backtracks. This is *representation*
interchangeability, not a literal equality of original
source geometric paths. -/
theorem c60F114WitnessedOriginalRawVersusF47
    {n : Nat} (C : C60F108BothFaceContexts n)
    (P : (i : Fin n) → C60F112IndependentOddFacePair C i)
    {i j : Fin n} (W : C60F112DistinctEdgeOverlap C i j) :
    (c60F112WitnessedOverlapAppend
      (c60F114SingleWitnessedOverlap W)
      (c60F114ReverseWitnessedPath
        (c60F114SingleWitnessedOverlap W)) ≠
       (C60F112WitnessedOverlapPath.nil i)) ∧
    (c60F112WitnessedF47Transport t₁ t₂ left right C P
      (c60F114SingleWitnessedOverlap W) ⋙
       c60F112WitnessedF47Transport t₁ t₂ left right C P
         (c60F114ReverseWitnessedPath
           (c60F114SingleWitnessedOverlap W)) =
       𝟭 (c60F112WitnessedF47Fibre t₁ t₂ left right C P i)) :=
  ⟨c60F114RoundTripRawWitnesses_nontrivial W,
    c60F114WitnessedF47RoundTrip_rightInverse
      t₁ t₂ left right C P (c60F114SingleWitnessedOverlap W)⟩

#print axioms c60F114SwapActualOverlap_involutive
#print axioms c60F114ReverseWitnessedSingle
#print axioms c60F114ReverseWitnessed_append
#print axioms c60F114ReverseWitnessed_involutive
#print axioms c60F114ReverseF69Zigzag
#print axioms c60F114F69ZigzagLength_append
#print axioms c60F114RoundTripRawWitnesses_nontrivial
#print axioms c60F114WitnessedF47RoundTrip_rightInverse
#print axioms c60F114WitnessedF47RoundTrip_leftInverse
#print axioms c60F114WitnessedF47RoundTrip_map_identity
#print axioms c60F114WitnessedOriginalRawVersusF47

end ActualOriginalF47Reverse
end
end KUOS.DependentOriginationC60KuuPhysicalZigzagReverseWitnessedSourceV5_280
