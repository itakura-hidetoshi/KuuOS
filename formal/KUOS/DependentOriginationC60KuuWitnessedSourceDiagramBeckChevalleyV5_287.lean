import KUOS.DependentOriginationC60KuuCrossEdgeOriginalSourceBeckChevalleyV5_286
import KUOS.DependentOriginationC60KuuWitnessedOverlapPathGrothendieckV5_278

namespace KUOS.DependentOriginationC60KuuWitnessedSourceDiagramBeckChevalleyV5_287

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationGrayC60MixedBoundaryThreeHomV5_195
open KUOS.DependentOriginationGrayC60IntegralChainComplexV5_160
open KUOS.DependentOriginationC60FiniteAtlasCechCoherenceV5_221
open KUOS.DependentOriginationC60PhysicalCechCurvatureRepairV5_222
open KUOS.DependentOriginationC60KuuIndependentPhysicalFaceSiteSourceV5_274
open KUOS.DependentOriginationC60KuuIndependentMixedPhysicalBaseChangeV5_276
open KUOS.DependentOriginationC60KuuCrossEdgePhysicalOverlapF47V5_277
open KUOS.DependentOriginationC60KuuWitnessedOverlapPathGrothendieckV5_278
open KUOS.DependentOriginationC60KuuCrossEdgeOriginalSourceBeckChevalleyV5_286
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.287 / F112 part 15 — naturality of independent ORIGINAL source presentations
  on arbitrary finite paths of TRUE C60 physical overlaps

F112 part 14 established an honest functor-category Beck-Chevalley
NatIso for TWO DIFFERENT physical C60 edges, requiring their
genuine F69 incidence-star overlap witness.  F112 part 6
independently constructed the category of ALL finite paths of
actual, witnessed overlaps, and the corresponding ORIGINAL fully
native F47 source Cat-valued diagram.

This stage allows TWO independently indexed ORIGINAL odd F42
two-face labels at EVERY actual physical edge of a fixed C60
context C.  At any vertex, there is an ORIGINAL mixed F47
four-boundary source-change functor.  Across ANY finite witnessed
overlap path (of arbitrary length), the local source-change and
physical path transport commute by induction using EACH actual
F120 cross-edge BC theorem, together with the functor-category
associator.  This is not a finite-bound approximation.

The result is a TRUE natural transformation between the two
fully native F47 Cat-valued diagrams over the same witness-path
base category; its components are the actual ORIGINAL F47
source-change functors.  On ALL 3-Homs it preserves both
independent Int charges AND the original ZMod2 phase.

The natural transformation also admits a triple independent
original F42-presentation strict cocycle at each physical edge.
We do NOT replace genuinely different original F42/F54 raw
boundary words by equalities.  We do NOT introduce an old
F69 edge-to-edge Hom or an unconditional F69 site-wide
original-source 3-stack.  Old F55 Delta nonlift, F110 lost
phase after F77 projection, and nonflat F68 north curvature
with signed second charge -5 remain independent obstructions.
-/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

section OriginalF47PathDiagramChange
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

/-- Component at a real physical edge: ORIGINAL independent
F42 source presentation change between its four F47 mixed
boundary objects, preserving the complete native receiver. -/
def c60F121WitnessedLocalSourceChange
    {n : Nat} (C : C60F108BothFaceContexts n)
    (P Q : (i : Fin n) → C60F112IndependentOddFacePair C i)
    (i : Fin n) :
    c60F112WitnessedF47Fibre t₁ t₂ left right C P i ⥤
      c60F112WitnessedF47Fibre t₁ t₂ left right C Q i :=
  c60F120SameEdgeSourceChange
    t₁ t₂ left right C i (P i) (Q i)

/-- The original F47 same-edge chart change preserves each
source three-Hom's FULL signed Int x Int charge and ZMod2
phase, not merely a phase-forgetting observer. -/
theorem c60F121WitnessedLocalSourceChange_fullNative
    {n : Nat} (C : C60F108BothFaceContexts n)
    (P Q : (i : Fin n) → C60F112IndependentOddFacePair C i)
    (i : Fin n)
    {X Y : c60F112WitnessedF47Fibre t₁ t₂ left right C P i}
    (f : X ⟶ Y) :
    c60F47MixedEval
      ((c60F121WitnessedLocalSourceChange
        t₁ t₂ left right C P Q i).map f) =
      c60F47MixedEval f :=
  c60F112MixedPhysicalSourceChange_native
    t₁ t₂ left right C C i (P i) (Q i) rfl f

/-- MAIN arbitrary-length witness-path source BC theorem.
Every individual path step carries an ACTUAL distinct-edge
F69 star-intersection witness, and its original F47
presentation-change interchange is the v5.286 Cat BC 2-cell.

This theorem lives in the category of original four-boundary
F47 source functors, not the raw F42/F54 syntax category. -/
theorem c60F121WitnessedLocalSourceChange_path
    {n : Nat} (C : C60F108BothFaceContexts n)
    (P Q : (i : Fin n) → C60F112IndependentOddFacePair C i)
    {i j : Fin n} (path : C60F112WitnessedOverlapPath C i j) :
    c60F121WitnessedLocalSourceChange
        t₁ t₂ left right C P Q i ⋙
      c60F112WitnessedF47Transport t₁ t₂ left right C Q path =
    c60F112WitnessedF47Transport t₁ t₂ left right C P path ⋙
      c60F121WitnessedLocalSourceChange
        t₁ t₂ left right C P Q j := by
  induction path with
  | nil i =>
      change
        c60F121WitnessedLocalSourceChange
            t₁ t₂ left right C P Q i ⋙ 𝟭 _ =
          𝟭 _ ⋙
            c60F121WitnessedLocalSourceChange
              t₁ t₂ left right C P Q i
      rw [Functor.comp_id, Functor.id_comp]
  | @step i j k W rest ih =>
      change
        c60F121WitnessedLocalSourceChange
          t₁ t₂ left right C P Q i ⋙
          (c60F112CrossEdgeMixedSourceChange
            t₁ t₂ left right C i j W (Q i) (Q j) ⋙
              c60F112WitnessedF47Transport
                t₁ t₂ left right C Q rest) =
        (c60F112CrossEdgeMixedSourceChange
          t₁ t₂ left right C i j W (P i) (P j) ⋙
            c60F112WitnessedF47Transport
              t₁ t₂ left right C P rest) ⋙
          c60F121WitnessedLocalSourceChange
            t₁ t₂ left right C P Q k
      calc
        _ = (c60F121WitnessedLocalSourceChange
              t₁ t₂ left right C P Q i ⋙
            c60F112CrossEdgeMixedSourceChange
              t₁ t₂ left right C i j W (Q i) (Q j)) ⋙
            c60F112WitnessedF47Transport
              t₁ t₂ left right C Q rest :=
                (Functor.assoc _ _ _).symm
        _ = (c60F112CrossEdgeMixedSourceChange
              t₁ t₂ left right C i j W (P i) (P j) ⋙
            c60F121WitnessedLocalSourceChange
              t₁ t₂ left right C P Q j) ⋙
            c60F112WitnessedF47Transport
              t₁ t₂ left right C Q rest := by
                exact congrArg
                  (fun F => F ⋙
                    c60F112WitnessedF47Transport
                      t₁ t₂ left right C Q rest)
                  (c60F120OriginalCrossEdgeSourceBC_strict
                    t₁ t₂ left right C i j W
                    (P i) (Q i) (P j) (Q j))
        _ = c60F112CrossEdgeMixedSourceChange
              t₁ t₂ left right C i j W (P i) (P j) ⋙
            (c60F121WitnessedLocalSourceChange
              t₁ t₂ left right C P Q j ⋙
              c60F112WitnessedF47Transport
                t₁ t₂ left right C Q rest) :=
                  Functor.assoc _ _ _
        _ = c60F112CrossEdgeMixedSourceChange
              t₁ t₂ left right C i j W (P i) (P j) ⋙
            (c60F112WitnessedF47Transport
              t₁ t₂ left right C P rest ⋙
              c60F121WitnessedLocalSourceChange
                t₁ t₂ left right C P Q k) := by
                  rw [ih]
        _ = (c60F112CrossEdgeMixedSourceChange
              t₁ t₂ left right C i j W (P i) (P j) ⋙
              c60F112WitnessedF47Transport
                t₁ t₂ left right C P rest) ⋙
            c60F121WitnessedLocalSourceChange
              t₁ t₂ left right C P Q k :=
                (Functor.assoc _ _ _).symm

/-- A GENUINE natural transformation of Cat-valued ORIGINAL
F47 source diagrams on the SAME witness-path base.
The components are the true old F42 face source changes,
rather than mere equalities of their F77 observer images. -/
def c60F121WitnessedF47DiagramSourceChange
    {n : Nat} (C : C60F108BothFaceContexts n)
    (P Q : (i : Fin n) → C60F112IndependentOddFacePair C i) :
    NatTrans
      (c60F112WitnessedF47Diagram t₁ t₂ left right C P)
      (c60F112WitnessedF47Diagram t₁ t₂ left right C Q) where
  app X :=
    (c60F121WitnessedLocalSourceChange
      t₁ t₂ left right C P Q X.index).toCatHom
  naturality := by
    intro X Y path
    apply Cat.Hom.ext
    simpa only [Cat.Hom.comp_toFunctor, Functor.toCatHom_toFunctor] using
      (c60F121WitnessedLocalSourceChange_path
        t₁ t₂ left right C P Q path).symm

/-- The strict source transport naturality for any two
concatenated genuine physical overlap routes; the same
source diagram-change 2-cell works at every finite length. -/
theorem c60F121WitnessedLocalSourceChange_append
    {n : Nat} (C : C60F108BothFaceContexts n)
    (P Q : (i : Fin n) → C60F112IndependentOddFacePair C i)
    {i j k : Fin n}
    (first : C60F112WitnessedOverlapPath C i j)
    (second : C60F112WitnessedOverlapPath C j k) :
    c60F121WitnessedLocalSourceChange
        t₁ t₂ left right C P Q i ⋙
      (c60F112WitnessedF47Transport t₁ t₂ left right C Q first ⋙
        c60F112WitnessedF47Transport t₁ t₂ left right C Q second) =
    (c60F112WitnessedF47Transport t₁ t₂ left right C P first ⋙
        c60F112WitnessedF47Transport t₁ t₂ left right C P second) ⋙
      c60F121WitnessedLocalSourceChange
        t₁ t₂ left right C P Q k := by
  rw [← c60F112WitnessedF47Transport_append,
    ← c60F112WitnessedF47Transport_append]
  exact c60F121WitnessedLocalSourceChange_path t₁ t₂ left right
    C P Q (c60F112WitnessedOverlapAppend first second)

/-! ## Independently re-presented source labels: exact local Cech cocycle -/

/-- Three independent actual original F42 label families are
strictly coherent at EACH physical edge, in the complete
F47 source category rather than only in the F77 observer.

The three exact boundary presentations are not equated as
raw old F42 two-cell terms. -/
theorem c60F121WitnessedLocalSourceChange_cocycle
    {n : Nat} (C : C60F108BothFaceContexts n)
    (P Q R : (i : Fin n) → C60F112IndependentOddFacePair C i)
    (i : Fin n) :
    c60F121WitnessedLocalSourceChange t₁ t₂ left right C P Q i ⋙
      c60F121WitnessedLocalSourceChange t₁ t₂ left right C Q R i =
    c60F121WitnessedLocalSourceChange t₁ t₂ left right C P R i := by
  fapply CategoryTheory.Functor.ext
  · intro X
    cases X <;> rfl
  · intro X Y f
    apply c60F47MixedGrayFunctor_faithful
      (c60F112CrossEdgeFrame t₁ t₂ left right C i (R i))
    calc
      c60F47MixedEval
          ((c60F121WitnessedLocalSourceChange
            t₁ t₂ left right C P Q i ⋙
            c60F121WitnessedLocalSourceChange
              t₁ t₂ left right C Q R i).map f) =
        c60F47MixedEval
          ((c60F121WitnessedLocalSourceChange
            t₁ t₂ left right C P Q i).map f) :=
          c60F121WitnessedLocalSourceChange_fullNative
            t₁ t₂ left right C Q R i _
      _ = c60F47MixedEval f :=
        c60F121WitnessedLocalSourceChange_fullNative
          t₁ t₂ left right C P Q i f
      _ = c60F47MixedEval
          ((c60F121WitnessedLocalSourceChange
            t₁ t₂ left right C P R i).map f) :=
          (c60F121WitnessedLocalSourceChange_fullNative
            t₁ t₂ left right C P R i f).symm
      _ = c60F47MixedEval
          (eqToHom _ ≫
            (c60F121WitnessedLocalSourceChange
              t₁ t₂ left right C P R i).map f ≫ eqToHom _) := by
          symm
          exact c60F112WitnessedF47EqToHom_conjugate
            t₁ t₂ left right C R i _ _ _

/-- This is the triple-label Čech cocycle at EACH object of
the ACTUAL witness-path base, expressed by equal true
source Cat Homs rather than an untyped formal equality. -/
theorem c60F121WitnessedDiagramChange_cocycle_app
    {n : Nat} (C : C60F108BothFaceContexts n)
    (P Q R : (i : Fin n) → C60F112IndependentOddFacePair C i)
    (X : C60F112WitnessedEdge C) :
    (c60F121WitnessedF47DiagramSourceChange
      t₁ t₂ left right C P Q).app X ≫
      (c60F121WitnessedF47DiagramSourceChange
        t₁ t₂ left right C Q R).app X =
      (c60F121WitnessedF47DiagramSourceChange
        t₁ t₂ left right C P R).app X := by
  apply Cat.Hom.ext
  simpa only [Cat.Hom.comp_toFunctor, Functor.toCatHom_toFunctor] using
    c60F121WitnessedLocalSourceChange_cocycle
      t₁ t₂ left right C P Q R X.index

#print axioms c60F121WitnessedLocalSourceChange_fullNative
#print axioms c60F121WitnessedLocalSourceChange_path
#print axioms c60F121WitnessedF47DiagramSourceChange
#print axioms c60F121WitnessedLocalSourceChange_append
#print axioms c60F121WitnessedLocalSourceChange_cocycle
#print axioms c60F121WitnessedDiagramChange_cocycle_app

end OriginalF47PathDiagramChange
end
end KUOS.DependentOriginationC60KuuWitnessedSourceDiagramBeckChevalleyV5_287
