import KUOS.DependentOriginationGrayC60F55SourcePhaseLockedAtlasV5_175

namespace KUOS.DependentOriginationGrayC60F55SourceWhiskeringInterchangeV5_176

open CategoryTheory
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationGrayC60CyclicGlobalPastingV5_156
open KUOS.DependentOriginationGrayF55PhaseRealizationV5_156
open KUOS.DependentOriginationGrayC60AllNinetyEdgePastingV5_157
open KUOS.DependentOriginationGrayC60WangBiZhouyiTimeV5_170
open KUOS.DependentOriginationGrayC60WangBiNativeHigherCoherenceV5_171
open KUOS.DependentOriginationGrayC60WangBiFourImageSixQiF55NaturalityV5_172
open KUOS.DependentOriginationGrayC60WangBiGaugeCollarSixQiCoherenceV5_173
open KUOS.DependentOriginationGrayC60F55SourcePhaseLockedAtlasV5_175
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# F59-F28 / v5.176 — original F55 proof-relevant horizontal exchange

v5.175 proved that all nine original F55 PresentedCell constructors
map into the GENUINE native braided F59 3-cell category, and precisely
its phase-locked subgroup. The second integer generator charge
determines the image's odd/odd exchange phase; its raw source cells
are NOT thereby identified.

Here the original F55 freely presented cells, including their
DEPENDENT original F19/F28 Nat depths and F45 bracket-tree endpoints,
are given a higher presentation-sensitive HORIZONTAL COMPOSITION:

  first route:  [α then β] = postcompose α ; precompose β;
  second route: [β then α] = precompose β ; postcompose α.

Both are ACTUAL source PresentedCell syntax, with exactly matching
dependent source/target paths, not merely a formal equation between
F44 quotient classes.

We prove:
* true source identity, inverse and vertical composition land in the
  native Mathlib Cat-neutral endomorphisms of the phase-locked subgroup;
* the original TWO contextual and TWO pre/post whiskering constructors
  map exactly to their original subgroup element (no 2-cell collapsed
  by an assumed raw source equality);
* the two independent horizontal source presentation orderings have
  exactly equal native 3-cell interpretations, preserving BOTH
  integer generator charges and mod-two phase;
* the genuine original F59 braided TENSOR is bifunctorial on
  native images of source F55 vertical composites;
* the higher horizontal comparison transports as equality of
  genuine Wang Bi Mathlib NatTrans across all 90 original C60
  physical edges and their 360 local incidence corners;
* every old original-F54-generated F55 physical square is EXACTLY
  the source disjointSquare image in the v5.175 compatible atlas.

Scope: target image-level coherence, NOT a raw source equation
between two freely presented witnesses, NOR an ambient Gray
3-functor from all original source 0/1/2/3 morphisms. No new
external axioms, no new native_decide, no manufactured C60
quadrilateral faces.
-/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

/-- The interpreted genuinely proof-relevant original F55 cell
WITH its Lean-proved image phase compatibility retained as DATA. -/
def c60F55SourceLocked
    {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    {first : OriginalF45BracketTree n m ma pa mb pb}
    {last : OriginalF45BracketTree n' m' ma pa mb pb}
    {r s : OriginalF45BracketTree.DepthRotationRoute first last}
    (cell : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r s) :
    c60F55PhaseLocked :=
  ⟨c60F55SourceNative cell, c60F55SourceNative_mem cell⟩

/-- The source F55 identity is exactly the identity in the
native neutral-grade 3-cell CATEGORY and zero of its subgroup. -/
theorem c60F55SourceLocked_ident
    {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    {first : OriginalF45BracketTree n m ma pa mb pb}
    {last : OriginalF45BracketTree n' m' ma pa mb pb}
    (route : OriginalF45BracketTree.DepthRotationRoute first last) :
    c60F55SourceLocked
      (OriginalF45BracketTree.DepthRotationRoute.PresentedCell.ident route) =
      (0 : c60F55PhaseLocked) := by
  apply Subtype.ext
  change c60F55SourceNative
    (OriginalF45BracketTree.DepthRotationRoute.PresentedCell.ident route) =
      (0 : GradedThreeCell 0 0)
  exact c60F55SourceNative_ident route

/-- Actual F55 vertical pasting is the native subgroup addition,
hence exactly the genuine Mathlib category composition on the
unchanged neutral Gray-grade 2-cell object. -/
theorem c60F55SourceLocked_trans
    {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    {first : OriginalF45BracketTree n m ma pa mb pb}
    {last : OriginalF45BracketTree n' m' ma pa mb pb}
    {r s t : OriginalF45BracketTree.DepthRotationRoute first last}
    (α : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r s)
    (β : OriginalF45BracketTree.DepthRotationRoute.PresentedCell s t) :
    c60F55SourceLocked
      (OriginalF45BracketTree.DepthRotationRoute.PresentedCell.trans α β) =
      c60F55SourceLocked α + c60F55SourceLocked β := by
  apply Subtype.ext
  change (c60F55SourceNative α).comp (c60F55SourceNative β) =
    c60F55SourceNative α + c60F55SourceNative β
  exact (grayNeutral_add_eq_native_comp _ _).symm

/-- Reversing a GENUINE source PresentedCell gives exactly the
native inverse, with signed F58 charge and signed exchange phase. -/
theorem c60F55SourceLocked_symm
    {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    {first : OriginalF45BracketTree n m ma pa mb pb}
    {last : OriginalF45BracketTree n' m' ma pa mb pb}
    {r s : OriginalF45BracketTree.DepthRotationRoute first last}
    (α : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r s) :
    c60F55SourceLocked
      (OriginalF45BracketTree.DepthRotationRoute.PresentedCell.symm α) =
      -c60F55SourceLocked α := by
  apply Subtype.ext
  change (c60F55SourceNative α).inv = -(c60F55SourceNative α)
  apply GradedThreeCell.ext <;> rfl

/-! FOUR distinct ORIGINAL horizontal whisker constructors preserve the
nontrivial native F55 3-cell value. These are genuine dependent typed
operations; their result's source and target routes differ. -/

theorem c60F55SourceLocked_leftContext
    {a b : D} {x y : E} {n n' m m' k l : Nat}
    {ma mb mc : Blocks a b} {pa pb pc : Blocks x y}
    {first : OriginalF45BracketTree n m ma pa mb pb}
    {last : OriginalF45BracketTree n' m' ma pa mb pb}
    {r s : OriginalF45BracketTree.DepthRotationRoute first last}
    (α : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r s)
    (later : OriginalF45BracketTree k l mb pb mc pc) :
    c60F55SourceLocked
      (OriginalF45BracketTree.DepthRotationRoute.PresentedCell.leftContext α later) =
      c60F55SourceLocked α := by
  rfl

theorem c60F55SourceLocked_rightContext
    {a b : D} {x y : E} {k l n n' m m' : Nat}
    {ma mb mc : Blocks a b} {pa pb pc : Blocks x y}
    (earlier : OriginalF45BracketTree k l ma pa mb pb)
    {first : OriginalF45BracketTree n m mb pb mc pc}
    {last : OriginalF45BracketTree n' m' mb pb mc pc}
    {r s : OriginalF45BracketTree.DepthRotationRoute first last}
    (α : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r s) :
    c60F55SourceLocked
      (OriginalF45BracketTree.DepthRotationRoute.PresentedCell.rightContext earlier α) =
      c60F55SourceLocked α := by
  rfl

theorem c60F55SourceLocked_precompose
    {a b : D} {x y : E} {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    {first : OriginalF45BracketTree n₁ m₁ ma pa mb pb}
    {middle : OriginalF45BracketTree n₂ m₂ ma pa mb pb}
    {last : OriginalF45BracketTree n₃ m₃ ma pa mb pb}
    (prior : OriginalF45BracketTree.DepthRotationRoute first middle)
    {r s : OriginalF45BracketTree.DepthRotationRoute middle last}
    (α : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r s) :
    c60F55SourceLocked
      (OriginalF45BracketTree.DepthRotationRoute.PresentedCell.precompose prior α) =
      c60F55SourceLocked α := by
  rfl

theorem c60F55SourceLocked_postcompose
    {a b : D} {x y : E} {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    {first : OriginalF45BracketTree n₁ m₁ ma pa mb pb}
    {middle : OriginalF45BracketTree n₂ m₂ ma pa mb pb}
    {last : OriginalF45BracketTree n₃ m₃ ma pa mb pb}
    {r s : OriginalF45BracketTree.DepthRotationRoute first middle}
    (α : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r s)
    (suffix : OriginalF45BracketTree.DepthRotationRoute middle last) :
    c60F55SourceLocked
      (OriginalF45BracketTree.DepthRotationRoute.PresentedCell.postcompose α suffix) =
      c60F55SourceLocked α := by
  rfl

section SourceHorizontal
variable {a b : D} {x y : E}
variable {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
variable {ma mb : Blocks a b} {pa pb : Blocks x y}
variable {first : OriginalF45BracketTree n₁ m₁ ma pa mb pb}
variable {middle : OriginalF45BracketTree n₂ m₂ ma pa mb pb}
variable {last : OriginalF45BracketTree n₃ m₃ ma pa mb pb}
variable {r₁ s₁ t₁ : OriginalF45BracketTree.DepthRotationRoute first middle}
variable {r₂ s₂ t₂ : OriginalF45BracketTree.DepthRotationRoute middle last}

/-- FIRST original horizontal order: act on the LEFT segment
with a real proof-relevant cell α, whisker it by the original
right segment r₂, then act on the RIGHT with β whiskered by s₁. -/
def c60F55SourceHorizontalLeftFirst
    (α : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r₁ s₁)
    (β : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r₂ s₂) :
    OriginalF45BracketTree.DepthRotationRoute.PresentedCell
      (OriginalF45BracketTree.DepthRotationRoute.trans r₁ r₂)
      (OriginalF45BracketTree.DepthRotationRoute.trans s₁ s₂) :=
  OriginalF45BracketTree.DepthRotationRoute.PresentedCell.trans
    (OriginalF45BracketTree.DepthRotationRoute.PresentedCell.postcompose α r₂)
    (OriginalF45BracketTree.DepthRotationRoute.PresentedCell.precompose s₁ β)

/-- SECOND original horizontal order: act on the RIGHT segment
with β first, whiskered by the original left route r₁, then
act on the LEFT with α whiskered by the updated right route s₂. -/
def c60F55SourceHorizontalRightFirst
    (α : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r₁ s₁)
    (β : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r₂ s₂) :
    OriginalF45BracketTree.DepthRotationRoute.PresentedCell
      (OriginalF45BracketTree.DepthRotationRoute.trans r₁ r₂)
      (OriginalF45BracketTree.DepthRotationRoute.trans s₁ s₂) :=
  OriginalF45BracketTree.DepthRotationRoute.PresentedCell.trans
    (OriginalF45BracketTree.DepthRotationRoute.PresentedCell.precompose r₁ β)
    (OriginalF45BracketTree.DepthRotationRoute.PresentedCell.postcompose α s₂)

/-- ORIGINAL left-then-right source F55 2-dimensional construction
has the exact NATIVE phase-compatible higher value α+β. -/
theorem c60F55SourceHorizontalLeftFirst_value
    (α : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r₁ s₁)
    (β : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r₂ s₂) :
    c60F55SourceLocked (c60F55SourceHorizontalLeftFirst α β) =
      c60F55SourceLocked α + c60F55SourceLocked β := by
  change c60F55SourceLocked
    (OriginalF45BracketTree.DepthRotationRoute.PresentedCell.trans
      (OriginalF45BracketTree.DepthRotationRoute.PresentedCell.postcompose α r₂)
      (OriginalF45BracketTree.DepthRotationRoute.PresentedCell.precompose s₁ β)) = _
  rw [c60F55SourceLocked_trans,
    c60F55SourceLocked_postcompose, c60F55SourceLocked_precompose]

/-- ORIGINAL right-then-left source F55 construction has
exact phase-compatible value β+α; no raw source equality is used. -/
theorem c60F55SourceHorizontalRightFirst_value
    (α : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r₁ s₁)
    (β : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r₂ s₂) :
    c60F55SourceLocked (c60F55SourceHorizontalRightFirst α β) =
      c60F55SourceLocked β + c60F55SourceLocked α := by
  change c60F55SourceLocked
    (OriginalF45BracketTree.DepthRotationRoute.PresentedCell.trans
      (OriginalF45BracketTree.DepthRotationRoute.PresentedCell.precompose r₁ β)
      (OriginalF45BracketTree.DepthRotationRoute.PresentedCell.postcompose α s₂)) = _
  rw [c60F55SourceLocked_trans,
    c60F55SourceLocked_precompose, c60F55SourceLocked_postcompose]

/-- ACTUAL higher source-presentation interchange theorem:
two distinct honest F55 proof-relevant horizontal pasting
constructions have EQUAL independent braided native 3-cell IMAGES.
Both original integer charges and the extra mod-two exchange
phase are retained. We do not identify the freely presented
source cells themselves. -/
theorem c60F55SourceHorizontalInterchange
    (α : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r₁ s₁)
    (β : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r₂ s₂) :
    c60F55SourceLocked (c60F55SourceHorizontalLeftFirst α β) =
      c60F55SourceLocked (c60F55SourceHorizontalRightFirst α β) := by
  calc
    _ = c60F55SourceLocked α + c60F55SourceLocked β :=
      c60F55SourceHorizontalLeftFirst_value α β
    _ = c60F55SourceLocked β + c60F55SourceLocked α := by
      abel
    _ = _ := (c60F55SourceHorizontalRightFirst_value α β).symm

/-- The two source horizontal composites share the same EXACT
F58 integer charge and hence same preserved exchange phase. -/
theorem c60F55SourceHorizontalInterchange_components
    (α : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r₁ s₁)
    (β : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r₂ s₂) :
    (c60F55SourceNative (c60F55SourceHorizontalLeftFirst α β)).charge =
      (c60F55SourceNative (c60F55SourceHorizontalRightFirst α β)).charge ∧
    (c60F55SourceNative (c60F55SourceHorizontalLeftFirst α β)).phase =
      (c60F55SourceNative (c60F55SourceHorizontalRightFirst α β)).phase := by
  have h := congrArg Subtype.val (c60F55SourceHorizontalInterchange α β)
  exact ⟨congrArg GradedThreeCell.charge h,
    congrArg GradedThreeCell.phase h⟩

/-- GENUINE native braided 3-cell TENSOR bifunctorial interchange
on original source F55 vertical PresentedCell compositions,
not merely on abstract Int×Int charge words. -/
theorem c60F55SourceTensorVerticalInterchange
    (α : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r₁ s₁)
    (α' : OriginalF45BracketTree.DepthRotationRoute.PresentedCell s₁ t₁)
    (β : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r₂ s₂)
    (β' : OriginalF45BracketTree.DepthRotationRoute.PresentedCell s₂ t₂) :
    ((c60F55SourceNative α).tensor (c60F55SourceNative β)).comp
      ((c60F55SourceNative α').tensor (c60F55SourceNative β')) =
    (c60F55SourceNative
      (OriginalF45BracketTree.DepthRotationRoute.PresentedCell.trans α α')).tensor
    (c60F55SourceNative
      (OriginalF45BracketTree.DepthRotationRoute.PresentedCell.trans β β')) := by
  rw [c60F55SourceNative_trans, c60F55SourceNative_trans]
  exact GradedThreeCell.tensor_comp _ _ _ _

/-- All 360 original C60 four-flag corners and ALL Wang Bi chart
changes compare the two genuine source F55 horizontal pastings
by EQUAL REAL MATHLIB natural transformations, preserving the
phase-locked braided 3-cell in the target. -/
theorem c60F55SourceWangBiHorizontalInterchange
    (α : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r₁ s₁)
    (β : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r₂ s₂)
    (side : C60DartSideGauge) :
    c60F55LockedCornerNatTrans side
      (fun _ : TruncatedIcosahedralEdge =>
        c60F55SourceLocked (c60F55SourceHorizontalLeftFirst α β)) =
    c60F55LockedCornerNatTrans side
      (fun _ : TruncatedIcosahedralEdge =>
        c60F55SourceLocked (c60F55SourceHorizontalRightFirst α β)) := by
  rw [c60F55SourceHorizontalInterchange α β]

end SourceHorizontal

/-! ## A completely physical original F55 square, attached to
one of the 90 actual C60 incidence edges with genuine F54 rotations. -/

section OriginalC60Square
variable {a b : D} {x y : E}
variable {n₁ n₂ m₁ m₂ : Nat}
variable {p₀ p₁ p₂ : Blocks a b}
variable {q₀ q₁ q₂ : Blocks x y}
variable
  (t₁ : OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁)
  (t₂ : OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂)
variable
  {leftAfter : OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁}
  {rightAfter : OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂}
  (left : OriginalF45BracketTree.LocalRotation t₁ leftAfter)
  (right : OriginalF45BracketTree.LocalRotation t₂ rightAfter)

/-- Even on EACH of the original 90 physical C60 square edges,
the v5.175 *actually supplied* F54/F55 label is the image
of the literal ORIGINAL disjointSquare PresentedCell constructor. -/
theorem c60F55ActualPhysicalSquare_sourceLocked
    (e : TruncatedIcosahedralEdge) :
    c60ActualF55PresentedLockedGrade t₁ t₂ left right e =
      c60F55SourceLocked
        (OriginalF45BracketTree.DepthRotationRoute.PresentedCell.disjointSquare
          left right) := by
  apply Subtype.ext
  change c60AllNinetyGrayCell t₁ t₂ left right e =
    c60F55SourceNative
      (OriginalF45BracketTree.DepthRotationRoute.PresentedCell.disjointSquare
        left right)
  rw [c60AllNinetyGrayCell_eq t₁ t₂ left right e]
  rfl

/-- All 90 genuine F55-labeled physical edge squares thus
yield EXACTLY the same original v5.175 Wang Bi NatTrans as
the typed source PresentedCell, not a synthetic F55 target. -/
theorem c60F55ActualPhysicalSquare_sourceAtlas
    (side : C60DartSideGauge) :
    c60ActualF55PresentedLockedAtlas t₁ t₂ left right side =
      c60F55LockedCornerNatTrans side
        (fun _ : TruncatedIcosahedralEdge =>
          c60F55SourceLocked
            (OriginalF45BracketTree.DepthRotationRoute.PresentedCell.disjointSquare
              left right)) := by
  change c60F55LockedCornerNatTrans side
    (c60ActualF55PresentedLockedGrade t₁ t₂ left right) = _
  have h : c60ActualF55PresentedLockedGrade t₁ t₂ left right =
    (fun _ : TruncatedIcosahedralEdge =>
      c60F55SourceLocked
        (OriginalF45BracketTree.DepthRotationRoute.PresentedCell.disjointSquare
          left right)) := by
    funext e
    exact c60F55ActualPhysicalSquare_sourceLocked t₁ t₂ left right e
  rw [h]

end OriginalC60Square

#print axioms c60F55SourceLocked
#print axioms c60F55SourceLocked_ident
#print axioms c60F55SourceLocked_trans
#print axioms c60F55SourceLocked_symm
#print axioms c60F55SourceLocked_leftContext
#print axioms c60F55SourceLocked_rightContext
#print axioms c60F55SourceLocked_precompose
#print axioms c60F55SourceLocked_postcompose
#print axioms c60F55SourceHorizontalLeftFirst
#print axioms c60F55SourceHorizontalRightFirst
#print axioms c60F55SourceHorizontalLeftFirst_value
#print axioms c60F55SourceHorizontalRightFirst_value
#print axioms c60F55SourceHorizontalInterchange
#print axioms c60F55SourceHorizontalInterchange_components
#print axioms c60F55SourceTensorVerticalInterchange
#print axioms c60F55SourceWangBiHorizontalInterchange
#print axioms c60F55ActualPhysicalSquare_sourceLocked
#print axioms c60F55ActualPhysicalSquare_sourceAtlas

end
end KUOS.DependentOriginationGrayC60F55SourceWhiskeringInterchangeV5_176
