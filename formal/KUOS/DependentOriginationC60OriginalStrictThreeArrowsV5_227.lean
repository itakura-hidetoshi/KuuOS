import KUOS.DependentOriginationC60NativeGrayVertexFaceCollarV5_226
import KUOS.DependentOriginationGrayC60OriginalFaceHorizontalGrayCoherenceV5_199

namespace KUOS.DependentOriginationC60OriginalStrictThreeArrowsV5_227

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationGrayC60CyclicGlobalPastingV5_156
open KUOS.DependentOriginationGrayC60PresentedFaceTwoCellsV5_190
open KUOS.DependentOriginationGrayC60PresentedInterchangerV5_191
open KUOS.DependentOriginationGrayC60ThreeHomCategoriesV5_192
open KUOS.DependentOriginationGrayC60MixedBoundaryThreeHomV5_195
open KUOS.DependentOriginationGrayC60AllNinetyMixedBoundaryV5_196
open KUOS.DependentOriginationGrayC60OriginalFaceHorizontalPresentationV5_199
open KUOS.DependentOriginationGrayC60OriginalFaceHorizontalThreeHomV5_199
open KUOS.DependentOriginationGrayC60OriginalFaceHorizontalCompositionV5_199
open KUOS.DependentOriginationGrayC60OriginalFaceHorizontalGrayCoherenceV5_199
open KUOS.DependentOriginationC60ArbitraryAtlasNerveDescentV5_219
open KUOS.DependentOriginationC60FiniteAtlasCechCoherenceV5_221
open KUOS.DependentOriginationC60PhysicalCechCurvatureRepairV5_222
open KUOS.DependentOriginationC60NativeGrayVertexFaceCollarV5_226
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.227 / F73 (source-first revision): original STRICTLY TYPED three-arrows

IMPORTANT PRIORITY: the original C60 F42/F43 source three-arrows and
the original F54/F55 rotation source three-arrows are PRIMARY;
the F59 braided Gray category is their FAITHFUL EVALUATION TARGET,
not the substitute source data at physical vertices or faces.

I.  For each EXACT parallel pair of original C60 quiver paths,
the original F51 proof-relevant face 2-cell source has actual
Mathlib three-arrow Hom types. Their vertical identity,
composition and associativity are strictly categorical. The
original F43/F44 inclusion and original horizontal 3-arrow
composition are genuine original-source category functors.

II. For EVERY one of the ninety physical four-flag squares,
the distinct original F42 face and F54/F55 rotation boundaries
are retained as separate four tags in the F47 source category.
Its original three-arrows, vertical identity/composition/
associativity and precisely typed physical comparison square are
strict in the actual full-native-kernel QUOTIENT. Every arbitrary
finite F67 atlas transport is a real category functor and strictly
preserves the original three-arrow composition and native value.

III. Crucially, the ORIGINAL north-pentagon F43 interchanger
is a real source THREE-ARROW between different horizontal
pasting orders, with nonzero phase one. Making that interchanger
a strict identity would destroy genuine original evidence.
Therefore this proves locally STRICT three-arrow HOM CATEGORIES,
NOT an unsupported fully strict three-category whose horizontal
2-cell interchange is identically trivial.

No modified physical C60 geometry, no unproved new raw F55
generator, no claim of global original (infinity,3) hyperdescent.
-/

/-! ## Part I: original F42/F43 source strict three-arrow Hom -/

/-- At an EXACT pair of parallel original physical C60 paths,
the source objects are the ORIGINAL proof-relevant F42
two-cell witnesses, not abstract Gray degrees. -/
abbrev C60F73OriginalFaceStrictThreeHom
    {v w : IcosahedralDart}
    (p q : Quiver.Path v w) :=
  C60F51OriginalTwo p q

/-- Strict unit law for the ORIGINAL F43-derived three-arrows,
in the original full-native-kernel F51 quotient category. -/
theorem c60F73OriginalFaceStrictThree_id_comp
    {v w : IcosahedralDart}
    {p q : Quiver.Path v w}
    {X Y : C60F73OriginalFaceStrictThreeHom p q}
    (f : X ⟶ Y) :
    (𝟙 X) ≫ f = f :=
  Category.id_comp f

/-- Strict right unit law on ORIGINAL proof-relevant source
three-arrows rather than on Gray-valued replacement arrows. -/
theorem c60F73OriginalFaceStrictThree_comp_id
    {v w : IcosahedralDart}
    {p q : Quiver.Path v w}
    {X Y : C60F73OriginalFaceStrictThreeHom p q}
    (f : X ⟶ Y) :
    f ≫ (𝟙 Y) = f :=
  Category.comp_id f

/-- STRICT vertical associativity of any three correctly
composable original F43/F51 source three-arrows. -/
theorem c60F73OriginalFaceStrictThree_assoc
    {v w : IcosahedralDart}
    {p q : Quiver.Path v w}
    {A B C D : C60F73OriginalFaceStrictThreeHom p q}
    (f : A ⟶ B) (g : B ⟶ C) (h : C ⟶ D) :
    (f ≫ g) ≫ h = f ≫ (g ≫ h) :=
  Category.assoc f g h

/-- The preexisting original F43/F44 categorical source embeds
into the LARGER original F51 horizontal 3-Hom source; this is
a genuine source-to-source functor, not Gray evaluation. -/
def c60F73OriginalFaceThreeSourceInclusion
    {v w : IcosahedralDart}
    (p q : Quiver.Path v w) :
    C60F42PresentedFaceCell p q ⥤
      C60F73OriginalFaceStrictThreeHom p q :=
  c60F51OriginalInclusion p q

/-- The genuine source-level original F43 inclusion remembers
all original full-native-kernel hom differences faithfully. -/
theorem c60F73OriginalFaceThreeSourceInclusion_faithful
    {v w : IcosahedralDart}
    (p q : Quiver.Path v w)
    {α β : C60F42PresentedFaceCell p q}
    {f g : α ⟶ β}
    (h :
      (c60F73OriginalFaceThreeSourceInclusion p q).map f =
      (c60F73OriginalFaceThreeSourceInclusion p q).map g) :
    f = g :=
  c60F51OriginalInclusion_faithful p q h

/-- A REAL horizontal source THREE-ARROW composition FUNCTOR
on pairs of original F42 proof-relevant 2-cell witnesses,
rather than a tensor of featureless Gray values. -/
def c60F73OriginalSourceHorizontalThreeFunctor
    {v w z : IcosahedralDart}
    (p q : Quiver.Path v w)
    (r s : Quiver.Path w z) :
    (C60F73OriginalFaceStrictThreeHom p q ×
      C60F73OriginalFaceStrictThreeHom r s) ⥤
      C60F73OriginalFaceStrictThreeHom
        (p.comp r) (q.comp s) :=
  c60F51HorizontalThreeHomFunctor p q r s

/-! ## Part II: all actual C60 F42/F55 strictly typed mixed three-arrows -/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

section NinetyPhysicalSquares
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

/-- At each of the original ninety C60 physical edges, keep
the ORIGINAL four tagged mixed F42/F54 boundary objects. -/
abbrev C60F73PhysicalStrictThreeHom
    (sigma : C60F67Atlas)
    (edge : TruncatedIcosahedralEdge) :=
  C60F47BoundaryPoint
    (c60F48EveryRealEdgeMixedFrame
      t₁ t₂ left right edge (sigma edge))

/-- THE original face source three-arrow as a correctly typed
morphism, not merely its Gray charge. -/
def c60F73OriginalPhysicalFaceThreeArrow
    (sigma : C60F67Atlas) (edge : TruncatedIcosahedralEdge) :
    (C60F47BoundaryPoint.faceBefore : C60F73PhysicalStrictThreeHom
      t₁ t₂ left right sigma edge) ⟶
      (C60F47BoundaryPoint.faceAfter : C60F73PhysicalStrictThreeHom
      t₁ t₂ left right sigma edge) :=
  c60F47FaceArrow
    (c60F48EveryRealEdgeMixedFrame
      t₁ t₂ left right edge (sigma edge))

/-- THE original F54/F55 rotation three-arrow, with its
DIFFERENT source two-cell types and original boundary tags. -/
def c60F73OriginalPhysicalF55ThreeArrow
    (sigma : C60F67Atlas) (edge : TruncatedIcosahedralEdge) :
    (C60F47BoundaryPoint.rotationBefore : C60F73PhysicalStrictThreeHom
      t₁ t₂ left right sigma edge) ⟶
      (C60F47BoundaryPoint.rotationAfter : C60F73PhysicalStrictThreeHom
      t₁ t₂ left right sigma edge) :=
  c60F47OriginalF55Arrow
    (c60F48EveryRealEdgeMixedFrame
      t₁ t₂ left right edge (sigma edge))

/-- Real source-side mixed FOUR boundary comparison square,
not an assertion that F42 source two-cells ARE F54/F55 routes.
It holds at every one of the original 90 physical edges. -/
theorem c60F73OriginalPhysicalStrictThreeSquare
    (sigma : C60F67Atlas) (edge : TruncatedIcosahedralEdge) :
    c60F73OriginalPhysicalFaceThreeArrow
        t₁ t₂ left right sigma edge ≫
      c60F47CompareAfter
        (c60F48EveryRealEdgeMixedFrame
          t₁ t₂ left right edge (sigma edge)) =
    c60F47CompareBefore
        (c60F48EveryRealEdgeMixedFrame
          t₁ t₂ left right edge (sigma edge)) ≫
      c60F73OriginalPhysicalF55ThreeArrow
        t₁ t₂ left right sigma edge :=
  c60F47MixedOriginalBoundarySquare
    (c60F48EveryRealEdgeMixedFrame
      t₁ t₂ left right edge (sigma edge))

/-- Exact STRICT categorical associativity for composable
original mixed F42/F55 source 3-arrows, without flattening
their distinct original boundary tags. -/
theorem c60F73OriginalPhysicalStrictThree_assoc
    (sigma : C60F67Atlas) (edge : TruncatedIcosahedralEdge)
    {A B C D : C60F73PhysicalStrictThreeHom
      t₁ t₂ left right sigma edge}
    (f : A ⟶ B) (g : B ⟶ C) (h : C ⟶ D) :
    (f ≫ g) ≫ h = f ≫ (g ≫ h) :=
  Category.assoc f g h

/-- Arbitrary finite F67 changes of the actual ninety-edge
atlas are SOURCE-LEVEL functors and preserve STRICT composition
of genuinely typed original mixed three-arrows. -/
theorem c60F73FiniteAtlasStrictThree_comp
    (sigma tau : C60F67Atlas)
    (edge : TruncatedIcosahedralEdge)
    (via : List C60F67Atlas)
    {A B C : C60F73PhysicalStrictThreeHom
      t₁ t₂ left right sigma edge}
    (f : A ⟶ B) (g : B ⟶ C) :
    (c60F67AtlasRoute
      t₁ t₂ left right sigma tau edge via).map (f ≫ g) =
    (c60F67AtlasRoute
      t₁ t₂ left right sigma tau edge via).map f ≫
      (c60F67AtlasRoute
        t₁ t₂ left right sigma tau edge via).map g :=
  (c60F67AtlasRoute
    t₁ t₂ left right sigma tau edge via).map_comp f g

/-- AFTER constructing the strict SOURCE morphism, the existing
full F59 native Gray evaluation serves as its faithful check;
this is the direction of explanation, not vice versa. -/
theorem c60F73FiniteAtlasStrictThree_fullNative
    (sigma tau : C60F67Atlas)
    (edge : TruncatedIcosahedralEdge)
    (via : List C60F67Atlas)
    {A B : C60F73PhysicalStrictThreeHom
      t₁ t₂ left right sigma edge}
    (f : A ⟶ B) :
    c60F47MixedEval
      ((c60F67AtlasRoute
        t₁ t₂ left right sigma tau edge via).map f) =
    c60F47MixedEval f :=
  c60F67AtlasRoute_fullNative
    t₁ t₂ left right tau edge via sigma f

/-! ## Part III: why original strict three-arrow ≠ fully strict 3-category -/

/-- The ACTUAL original NORTH pentagon has an ORIGINAL F43
SOURCE three-arrow between the two different, well-typed
horizontal F42 pasting orders. No phase-zero replacement. -/
def c60F73NorthOriginalStrictThreeInterchanger :
    c60F51OriginalTwoHorizontal
      c60F51NorthFaceSourceTwo c60F51NorthFaceSourceTwo ⟶
    c60F51OriginalTwoHorizontalRight
      c60F51NorthFaceSourceTwo c60F51NorthFaceSourceTwo :=
  c60F51NorthOriginalInterchanger

/-- Its independent odd/odd native exchange component is ONE,
as proven from original F43 presented source syntax. -/
theorem c60F73NorthOriginalStrictThree_phase_one :
    (c60F51Eval c60F73NorthOriginalStrictThreeInterchanger).phase =
      (1 : ZMod 2) :=
  c60F51NorthOriginalInterchanger_phaseOne

/-- The source three-arrow CANNOT evaluate to the identity
Gray three-cell; requiring fully STRICT IDENTITY INTERCHANGE
would destroy the original north pentagon's phase one. -/
theorem c60F73NorthOriginalStrictThree_noIdentityInterchange :
    c60F51Eval c60F73NorthOriginalStrictThreeInterchanger ≠
      (0 : GradedThreeCell 0 0) :=
  c60F51NorthOriginalInterchanger_nontrivial

/-- Therefore NO original phase-preserving interpretation can
require that this particular genuine source interchange evaluate
as an identity: the basic obstruction is proved, not postulated. -/
theorem c60F73PhasePreservingStrictIdentity_impossible
    (value : GradedThreeCell 0 0)
    (hNative :
      c60F51Eval c60F73NorthOriginalStrictThreeInterchanger = value)
    (hStrictIdentity : value = 0) : False :=
  c60F73NorthOriginalStrictThree_noIdentityInterchange
    (hNative.trans hStrictIdentity)

end NinetyPhysicalSquares

#print axioms c60F73OriginalFaceStrictThree_id_comp
#print axioms c60F73OriginalFaceStrictThree_comp_id
#print axioms c60F73OriginalFaceStrictThree_assoc
#print axioms c60F73OriginalFaceThreeSourceInclusion
#print axioms c60F73OriginalFaceThreeSourceInclusion_faithful
#print axioms c60F73OriginalSourceHorizontalThreeFunctor
#print axioms C60F73PhysicalStrictThreeHom
#print axioms c60F73OriginalPhysicalFaceThreeArrow
#print axioms c60F73OriginalPhysicalF55ThreeArrow
#print axioms c60F73OriginalPhysicalStrictThreeSquare
#print axioms c60F73OriginalPhysicalStrictThree_assoc
#print axioms c60F73FiniteAtlasStrictThree_comp
#print axioms c60F73FiniteAtlasStrictThree_fullNative
#print axioms c60F73NorthOriginalStrictThreeInterchanger
#print axioms c60F73NorthOriginalStrictThree_phase_one
#print axioms c60F73NorthOriginalStrictThree_noIdentityInterchange
#print axioms c60F73PhasePreservingStrictIdentity_impossible

end
end KUOS.DependentOriginationC60OriginalStrictThreeArrowsV5_227
