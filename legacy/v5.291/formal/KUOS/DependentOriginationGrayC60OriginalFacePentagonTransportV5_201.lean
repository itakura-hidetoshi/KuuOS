import KUOS.DependentOriginationGrayC60OriginalFaceAssociatorNaturalityV5_200

namespace KUOS.DependentOriginationGrayC60OriginalFacePentagonTransportV5_201

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationGrayC60PresentedFaceTwoCellsV5_190
open KUOS.DependentOriginationGrayC60PresentedInterchangerV5_191
open KUOS.DependentOriginationGrayC60OriginalFaceHorizontalPresentationV5_199
open KUOS.DependentOriginationGrayC60OriginalFaceHorizontalThreeHomV5_199
open KUOS.DependentOriginationGrayC60OriginalFaceAssociatorPresentationV5_200
open KUOS.DependentOriginationGrayC60OriginalFaceAssociatorThreeHomV5_200
open KUOS.DependentOriginationGrayC60OriginalFaceAssociatorNaturalityV5_200

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.201 / F59-F53-A: source isomorphisms and C60 pentagon transports

The actual F42 two-cell witnesses remain the objects of the F52 3-Hom.
We show that the explicitly ADJOINED F52 associator and unitors are
invertible 3-arrows in that source-aware category. No claim is made
that these comparison generators belonged to the original F43 syntax.

We formalize both routes in the Mac Lane PENTAGON of actual four-factor
C60 one-path reassociations and the two routes in the UNIT TRIANGLE.
Their equality is transported on BOTH genuine F42 boundary paths,
retaining the actual proof-relevant two-cell and three-cell terms.

The path-level pentagon and triangle are prerequisites, not substitutes
for the still-open complete F42 source-3-arrow pasting coherence. No
nonzero F55 obstruction or genuine F43 Gray phase is discarded.
-/

/-- The left, two-associator route through the four-factor C60 path
pentagon, starting at the fully left-associated genuine physical path. -/
def c60F53PathPentagonLeft
    {a b c d e : IcosahedralDart}
    (p : Quiver.Path a b) (r : Quiver.Path b c)
    (t : Quiver.Path c d) (v : Quiver.Path d e) :
    (((p.comp r).comp t).comp v) =
      p.comp (r.comp (t.comp v)) :=
  (Quiver.Path.comp_assoc (p.comp r) t v).trans
    (Quiver.Path.comp_assoc p r (t.comp v))

/-- The right, three-associator route, with the two context
whiskerings expressed as congruences of ACTUAL C60 paths. -/
def c60F53PathPentagonRight
    {a b c d e : IcosahedralDart}
    (p : Quiver.Path a b) (r : Quiver.Path b c)
    (t : Quiver.Path c d) (v : Quiver.Path d e) :
    (((p.comp r).comp t).comp v) =
      p.comp (r.comp (t.comp v)) :=
  ((congrArg (fun x : Quiver.Path a d => x.comp v)
      (Quiver.Path.comp_assoc p r t)).trans
    (Quiver.Path.comp_assoc p (r.comp t) v)).trans
      (congrArg (fun x : Quiver.Path b e => p.comp x)
        (Quiver.Path.comp_assoc r t v))

/-- Both pentagon routes give the SAME dependent path equality;
this does not identify two distinct original F42 face witnesses. -/
theorem c60F53PathPentagon
    {a b c d e : IcosahedralDart}
    (p : Quiver.Path a b) (r : Quiver.Path b c)
    (t : Quiver.Path c d) (v : Quiver.Path d e) :
    c60F53PathPentagonLeft p r t v =
      c60F53PathPentagonRight p r t v :=
  Subsingleton.elim _ _

/-- Two actual 1-path unit-triangle routes from ((p·nil)·r) to p·r. -/
def c60F53PathTriangleAssoc
    {a b c : IcosahedralDart}
    (p : Quiver.Path a b) (r : Quiver.Path b c) :
    ((p.comp Quiver.Path.nil).comp r) = p.comp r :=
  (Quiver.Path.comp_assoc p
      (Quiver.Path.nil : Quiver.Path b b) r).trans
    (congrArg (fun x : Quiver.Path b c => p.comp x)
      (Quiver.Path.nil_comp r))

def c60F53PathTriangleUnit
    {a b c : IcosahedralDart}
    (p : Quiver.Path a b) (r : Quiver.Path b c) :
    ((p.comp Quiver.Path.nil).comp r) = p.comp r :=
  congrArg (fun x : Quiver.Path a b => x.comp r)
    (Quiver.Path.comp_nil p)

theorem c60F53PathTriangle
    {a b c : IcosahedralDart}
    (p : Quiver.Path a b) (r : Quiver.Path b c) :
    c60F53PathTriangleAssoc p r =
      c60F53PathTriangleUnit p r :=
  Subsingleton.elim _ _

/-- The pentagon acts coherently on an ORIGINAL F42 two-cell witness:
no grade projection, and independent transports on both p and q. -/
theorem c60F53OriginalFacePentagon
    {a b c d e : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    {t u : Quiver.Path c d} {v w : Quiver.Path d e}
    (α : C60F42PresentedFaceCell
      (((p.comp r).comp t).comp v)
      (((q.comp s).comp u).comp w)) :
    c60F52ReindexFace
      (c60F53PathPentagonLeft p r t v)
      (c60F53PathPentagonLeft q s u w) α =
    c60F52ReindexFace
      (c60F53PathPentagonRight p r t v)
      (c60F53PathPentagonRight q s u w) α := by
  rw [c60F53PathPentagon p r t v, c60F53PathPentagon q s u w]

theorem c60F53OriginalFaceTriangle
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    (α : C60F42PresentedFaceCell
      ((p.comp Quiver.Path.nil).comp r)
      ((q.comp Quiver.Path.nil).comp s)) :
    c60F52ReindexFace
      (c60F53PathTriangleAssoc p r)
      (c60F53PathTriangleAssoc q s) α =
    c60F52ReindexFace
      (c60F53PathTriangleUnit p r)
      (c60F53PathTriangleUnit q s) α := by
  rw [c60F53PathTriangle p r, c60F53PathTriangle q s]

/-- The same pentagon coherence holds for any typed F52 3-arrow,
and hence for ALL original F43/F51 and new F52 constructors. -/
theorem c60F53OriginalThreePentagon
    {a b c d e : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    {t u : Quiver.Path c d} {v w : Quiver.Path d e}
    {X Y : C60F52OriginalTwo
      (((p.comp r).comp t).comp v)
      (((q.comp s).comp u).comp w)}
    (f : X ⟶ Y) :
    c60F52ReindexMap
      (c60F53PathPentagonLeft p r t v)
      (c60F53PathPentagonLeft q s u w) f =
    c60F52ReindexMap
      (c60F53PathPentagonRight p r t v)
      (c60F53PathPentagonRight q s u w) f := by
  rw [c60F53PathPentagon p r t v, c60F53PathPentagon q s u w]

theorem c60F53OriginalThreeTriangle
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    {X Y : C60F52OriginalTwo
      ((p.comp Quiver.Path.nil).comp r)
      ((q.comp Quiver.Path.nil).comp s)}
    (f : X ⟶ Y) :
    c60F52ReindexMap
      (c60F53PathTriangleAssoc p r)
      (c60F53PathTriangleAssoc q s) f =
    c60F52ReindexMap
      (c60F53PathTriangleUnit p r)
      (c60F53PathTriangleUnit q s) f := by
  rw [c60F53PathTriangle p r, c60F53PathTriangle q s]

/-- Actual C60 path transport is a Mathlib functor on the proof-
relevant F42 two-cell objects and full-native-quotient F52 3-arrows. -/
def c60F53ReindexTwo
    {a b : IcosahedralDart}
    {p q p' q' : Quiver.Path a b}
    (hp : p = p') (hq : q = q')
    (X : C60F52OriginalTwo p q) :
    C60F52OriginalTwo p' q' :=
  ⟨c60F52ReindexFace hp hq X.original⟩

def c60F53ReindexFunctor
    {a b : IcosahedralDart}
    {p q p' q' : Quiver.Path a b}
    (hp : p = p') (hq : q = q') :
    C60F52OriginalTwo p q ⥤ C60F52OriginalTwo p' q' where
  obj X := c60F53ReindexTwo hp hq X
  map := fun {_ _} f => c60F52ReindexMap hp hq f
  map_id := by
    intro X
    apply c60F52Hom_ext
    change c60F52Eval (c60F52ReindexMap hp hq (𝟙 X)) =
      c60F52Eval (𝟙 (c60F53ReindexTwo hp hq X))
    rw [c60F52ReindexMap_eval]
    simp
  map_comp := by
    intro X Y Z f g
    apply c60F52Hom_ext
    change c60F52Eval (c60F52ReindexMap hp hq (f ≫ g)) =
      c60F52Eval (c60F52ReindexMap hp hq f ≫
        c60F52ReindexMap hp hq g)
    simp only [c60F52ReindexMap_eval, c60F52Eval_catComp]

/-- Faithfulness of original-path transport retains the complete
native integer-charge pair and independent Gray exchange phase. -/
theorem c60F53ReindexFunctor_faithful
    {a b : IcosahedralDart}
    {p q p' q' : Quiver.Path a b}
    (hp : p = p') (hq : q = q')
    {X Y : C60F52OriginalTwo p q}
    {f g : X ⟶ Y}
    (h : (c60F53ReindexFunctor hp hq).map f =
      (c60F53ReindexFunctor hp hq).map g) : f = g := by
  have he := congrArg (fun z => c60F52Eval z) h
  change c60F52Eval (c60F52ReindexMap hp hq f) =
    c60F52Eval (c60F52ReindexMap hp hq g) at he
  rw [c60F52ReindexMap_eval, c60F52ReindexMap_eval] at he
  exact c60F52Hom_ext he

/-- The adjoined F52 associator is a typed *isomorphism* in the
actual F42-original-object three-Hom, not a raw two-term equality. -/
def c60F53AssociatorIso
    {a b c d : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    {t u : Quiver.Path c d}
    (X : C60F52OriginalTwo p q)
    (Y : C60F52OriginalTwo r s)
    (Z : C60F52OriginalTwo t u) :
    c60F52OriginalTwoHorizontal (c60F52OriginalTwoHorizontal X Y) Z ≅
      c60F52AssocRightTwo X Y Z where
  hom := c60F52Associator X Y Z
  inv := c60F52Of
    (.symm (.associator X.original Y.original Z.original))
  hom_inv_id := by
    apply c60F52Hom_ext
    rw [c60F52Eval_catComp]
    change (0 : GradedThreeCell 0 0) + -(0 : GradedThreeCell 0 0) = 0
    simp
  inv_hom_id := by
    apply c60F52Hom_ext
    rw [c60F52Eval_catComp]
    change -(0 : GradedThreeCell 0 0) + (0 : GradedThreeCell 0 0) = 0
    simp

def c60F53LeftUnitorIso
    {a b : IcosahedralDart} {p q : Quiver.Path a b}
    (X : C60F52OriginalTwo p q) :
    c60F52LeftUnitTwo X ≅ X where
  hom := c60F52LeftUnitor X
  inv := c60F52Of (.symm (.leftUnitor X.original))
  hom_inv_id := by
    apply c60F52Hom_ext
    rw [c60F52Eval_catComp]
    change (0 : GradedThreeCell 0 0) + -(0 : GradedThreeCell 0 0) = 0
    simp
  inv_hom_id := by
    apply c60F52Hom_ext
    rw [c60F52Eval_catComp]
    change -(0 : GradedThreeCell 0 0) + (0 : GradedThreeCell 0 0) = 0
    simp

def c60F53RightUnitorIso
    {a b : IcosahedralDart} {p q : Quiver.Path a b}
    (X : C60F52OriginalTwo p q) :
    c60F52RightUnitTwo X ≅ X where
  hom := c60F52RightUnitor X
  inv := c60F52Of (.symm (.rightUnitor X.original))
  hom_inv_id := by
    apply c60F52Hom_ext
    rw [c60F52Eval_catComp]
    change (0 : GradedThreeCell 0 0) + -(0 : GradedThreeCell 0 0) = 0
    simp
  inv_hom_id := by
    apply c60F52Hom_ext
    rw [c60F52Eval_catComp]
    change -(0 : GradedThreeCell 0 0) + (0 : GradedThreeCell 0 0) = 0
    simp

#print axioms c60F53PathPentagon
#print axioms c60F53PathTriangle
#print axioms c60F53OriginalFacePentagon
#print axioms c60F53OriginalFaceTriangle
#print axioms c60F53OriginalThreePentagon
#print axioms c60F53OriginalThreeTriangle
#print axioms c60F53ReindexFunctor
#print axioms c60F53ReindexFunctor_faithful
#print axioms c60F53AssociatorIso
#print axioms c60F53LeftUnitorIso
#print axioms c60F53RightUnitorIso

end
end KUOS.DependentOriginationGrayC60OriginalFacePentagonTransportV5_201
