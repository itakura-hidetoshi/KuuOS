import KUOS.DependentOriginationGrayC60F55PhysicalDirectPastedBCV5_210
import KUOS.DependentOriginationGrayC60OriginalFaceAssociatorPresentationV5_200

namespace KUOS.DependentOriginationGrayC60F55ThreeOriginalContextV5_211

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationGrayC60PresentedFaceTwoCellsV5_190
open KUOS.DependentOriginationGrayC60PresentedInterchangerV5_191
open KUOS.DependentOriginationGrayC60ThreeHomCategoriesV5_192
open KUOS.DependentOriginationGrayC60FaceWhiskeringFunctorsV5_193
open KUOS.DependentOriginationGrayC60OriginalFaceAssociatorPresentationV5_200
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

universe uD vD uE vE

/-!
# v5.211 / F59-F61-A — genuinely typed three-context source foundations

Three consecutive ORIGINAL C60 F42 Quiver.Path contexts remain
separately indexed. The direct original C60 path uses actual comp,
and the final source F42 2-cell is reindexed across the exact
two applications of path associativity. Full original source face
degree is retained; this does NOT equate raw proof-term syntax.

Three independent original F54/F55 bracket-tree source contexts
are also composed with genuine old .node constructors; two distinct
Nat.add_assoc casts are used in the original F44 exchange quotient.
It remains open to prove the entire 3-context BC pentagon in the F47
four-tag source 3-Hom category; no global physical descent follows.
-/

/-- Correct dependent path association for three genuinely typed
original C60 left path contexts, with the original F42 1-path. -/
theorem c60F62TripleLeftPath_assoc
    {a b c d e : IcosahedralDart}
    (outer : Quiver.Path a b) (middle : Quiver.Path b c)
    (prior : Quiver.Path c d) (p : Quiver.Path d e) :
    (((outer.comp middle).comp prior).comp p) =
      outer.comp (middle.comp (prior.comp p)) := by
  simp only [Quiver.Path.comp_assoc]

/-- Three actual original F42 left whiskerings have typed final
boundaries. The single concatenated ORIGINAL source path is cast
via the proven complete path associativity rather than by erasing
any original source proof term. -/
def c60F62TripleLeftDirectFace
    {a b c d e : IcosahedralDart}
    {p q : Quiver.Path d e}
    (outer : Quiver.Path a b) (middle : Quiver.Path b c)
    (prior : Quiver.Path c d)
    (α : C60F42PresentedFaceCell p q) :
    C60F42PresentedFaceCell
      (outer.comp (middle.comp (prior.comp p)))
      (outer.comp (middle.comp (prior.comp q))) :=
  c60F52ReindexFace
    (c60F62TripleLeftPath_assoc outer middle prior p)
    (c60F62TripleLeftPath_assoc outer middle prior q)
    ((c60F45LeftWhiskerFunctor ((outer.comp middle).comp prior)).obj α)

/-- The original F42 FACE DEGREE is conserved by directly
concatenating all three actual source C60 paths and reindexing
the two dependent source endpoints. -/
theorem c60F62TripleLeftDirectFace_degree
    {a b c d e : IcosahedralDart}
    {p q : Quiver.Path d e}
    (outer : Quiver.Path a b) (middle : Quiver.Path b c)
    (prior : Quiver.Path c d)
    (α : C60F42PresentedFaceCell p q) :
    c60F43FaceDegree
      (c60F62TripleLeftDirectFace outer middle prior α) =
        c60F43FaceDegree α := by
  simp only [c60F62TripleLeftDirectFace,
    c60F52ReindexFace_degree, c60F45LeftWhiskerFaceDegree]

/-- Full ORIGINAL F43 target 3-Hom evaluation survives THREE
separately typed original F42 C60 path-whiskerings, without
projecting away either integer charge or exchange phase. -/
theorem c60F62TripleLeftFullGray
    {a b c d e : IcosahedralDart}
    (outer : Quiver.Path a b) (middle : Quiver.Path b c)
    (prior : Quiver.Path c d)
    {p q : Quiver.Path d e}
    {α β : C60F42PresentedFaceCell p q}
    (f : α ⟶ β) :
    c60F44FaceThreeEval
      ((c60F45LeftWhiskerFunctor outer).map
        ((c60F45LeftWhiskerFunctor middle).map
          ((c60F45LeftWhiskerFunctor prior).map f))) =
        c60F44FaceThreeEval f := by
  rw [c60F45LeftWhiskerGrayMap,
    c60F45LeftWhiskerGrayMap, c60F45LeftWhiskerGrayMap]

/-- Original F54/F55 three-tree reassociation uses TWO exact
independently typed F19/F28 Nat depth transports in F44, not a
false equality between raw old F54 tree proof witnesses. -/
theorem c60F62TripleOriginalTree_reassociate
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    {n₀ n₁ n₂ m₀ m₁ m₂ : Nat}
    {ma mb mc md : Blocks a b}
    {pa pb pc pd : Blocks x y}
    (t₀ : OriginalF45BracketTree n₀ m₀ ma pa mb pb)
    (t₁ : OriginalF45BracketTree n₁ m₁ mb pb mc pc)
    (t₂ : OriginalF45BracketTree n₂ m₂ mc pc md pd) :
    (OriginalF45BracketTree.castDepths
      (Nat.add_assoc n₀ n₁ n₂) (Nat.add_assoc m₀ m₁ m₂)
      (OriginalF45BracketTree.node
        (OriginalF45BracketTree.node t₀ t₁) t₂)).toExchangeClass =
    (OriginalF45BracketTree.node t₀
      (OriginalF45BracketTree.node t₁ t₂)).toExchangeClass :=
  OriginalF45BracketTree.reassociate t₀ t₁ t₂

#print axioms c60F62TripleLeftPath_assoc
#print axioms c60F62TripleLeftDirectFace
#print axioms c60F62TripleLeftDirectFace_degree
#print axioms c60F62TripleLeftFullGray
#print axioms c60F62TripleOriginalTree_reassociate

end
end KUOS.DependentOriginationGrayC60F55ThreeOriginalContextV5_211
