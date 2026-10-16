import Kuu.F112.PolygonThreeCell

/-!
# F112-E5B / raw proof-relevant, globular C60 rotation 3-source

E5A constructed a THIN kernel 3-Hom using a new, independently
labelled signed generator-degree invariant. E5B now freely presents
RAW THREE-PROOF TREES over the actual E4 rotation two-squares.

Raw identity, unit, reassociation, disjoint-exchange, inverse,
sequential proof composition, two-cell vertical congruences, and actual
left/right Zigzag contexts are DISTINCT syntax constructors.
Horizontal composition of 3-proofs is derived from vertical congruence
and genuine E4 whiskering, not postulated as an extra constructor.

EVERY constructor is independently checked by a proof into the
E5A degree-kernel 3-Hom. In particular exchange is interpreted via
the proven integer-addition interchange theorem, not a new axiom.

No quotient is imposed on the raw THREE-proof terms. This is not an
equivalence with frozen F55 PresentedCell, and it does not assert any
historical exchange phase, global curvature, or missing Δ lift.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
noncomputable section

/-- A freely generated, correctly globular, Type-valued 3-proof
between ORIGINAL E4 two-squares sharing the same source and target
physical zigzag words. This does not impose raw category equations. -/
inductive PolygonRotationThreeProof :
    {s t : Site} → {q r : Zigzag s t} →
    (a b : PolygonRotationSquare q r) → Type where
  | ident {s t : Site} {q r : Zigzag s t}
      (a : PolygonRotationSquare q r) : PolygonRotationThreeProof a a
  | leftUnit {s t : Site} {q r : Zigzag s t}
      (a : PolygonRotationSquare q r) :
      PolygonRotationThreeProof
        (.vertical (.ident q) a) a
  | rightUnit {s t : Site} {q r : Zigzag s t}
      (a : PolygonRotationSquare q r) :
      PolygonRotationThreeProof
        (.vertical a (.ident r)) a
  | reassoc {s t : Site} {q r u v : Zigzag s t}
      (a : PolygonRotationSquare q r)
      (b : PolygonRotationSquare r u)
      (c : PolygonRotationSquare u v) :
      PolygonRotationThreeProof
        (.vertical (.vertical a b) c)
        (.vertical a (.vertical b c))
  | exchange {s t u : Site}
      {q r : Zigzag s t} {v w : Zigzag t u}
      (a : PolygonRotationSquare q r)
      (b : PolygonRotationSquare v w) :
      PolygonRotationThreeProof
        (polygonRotationLeftFirst a b)
        (polygonRotationRightFirst a b)
  | inverse {s t : Site} {q r : Zigzag s t}
      {a b : PolygonRotationSquare q r}
      (h : PolygonRotationThreeProof a b) :
      PolygonRotationThreeProof b a
  | vertical {s t : Site} {q r : Zigzag s t}
      {a b c : PolygonRotationSquare q r}
      (h : PolygonRotationThreeProof a b)
      (j : PolygonRotationThreeProof b c) :
      PolygonRotationThreeProof a c
  | verticalLeft {s t : Site} {q r u : Zigzag s t}
      {a a' : PolygonRotationSquare q r}
      (h : PolygonRotationThreeProof a a')
      (b : PolygonRotationSquare r u) :
      PolygonRotationThreeProof (.vertical a b) (.vertical a' b)
  | verticalRight {s t : Site} {q r u : Zigzag s t}
      (a : PolygonRotationSquare q r)
      {b b' : PolygonRotationSquare r u}
      (h : PolygonRotationThreeProof b b') :
      PolygonRotationThreeProof (.vertical a b) (.vertical a b')
  | leftContext {s t u : Site} (w : Zigzag s t)
      {q r : Zigzag t u} {a b : PolygonRotationSquare q r}
      (h : PolygonRotationThreeProof a b) :
      PolygonRotationThreeProof (.leftContext w a) (.leftContext w b)
  | rightContext {s t u : Site}
      {q r : Zigzag s t} {a b : PolygonRotationSquare q r}
      (h : PolygonRotationThreeProof a b) (w : Zigzag t u) :
      PolygonRotationThreeProof (.rightContext a w) (.rightContext b w)

/-- Every freely presented RAW 3-proof respects the independent
generator-degree comparison, including BOTH separately formed
exchange paths. This is proved by induction over ALL constructors. -/
theorem PolygonRotationThreeProof.degree_sound
    {s t : Site} {q r : Zigzag s t}
    {a b : PolygonRotationSquare q r}
    (h : PolygonRotationThreeProof a b) :
    a.degree = b.degree := by
  induction h with
  | ident a => rfl
  | leftUnit a =>
      funext j
      change (0 : Int) + a.degree j = a.degree j
      simp
  | rightUnit a =>
      funext j
      change a.degree j + (0 : Int) = a.degree j
      simp
  | reassoc a b c =>
      funext j
      change (a.degree j + b.degree j) + c.degree j =
        a.degree j + (b.degree j + c.degree j)
      exact add_assoc _ _ _
  | exchange a b =>
      exact polygonRotationInterchange_degree a b
  | inverse h ih =>
      exact ih.symm
  | vertical h k ihh ihk =>
      exact ihh.trans ihk
  | verticalLeft h b ih =>
      funext j
      change _ + b.degree j = _ + b.degree j
      exact congrArg (fun x : Int => x + b.degree j) (congrFun ih j)
  | verticalRight a h ih =>
      funext j
      change a.degree j + _ = a.degree j + _
      exact congrArg (fun x : Int => a.degree j + x) (congrFun ih j)
  | leftContext w h ih =>
      exact ih
  | rightContext h w ih =>
      exact ih

/-- Every actual raw source 3-proof has a sound, correctly globular
interpretation in the independently PROVED E5A kernel 3-Hom. -/
def PolygonRotationThreeProof.toKernel
    {s t : Site} {q r : Zigzag s t}
    {a b : PolygonRotationSquare q r}
    (h : PolygonRotationThreeProof a b) :
    PolygonRotationThreeCell a b :=
  ⟨h.degree_sound⟩

/-- True horizontal composition of proof-relevant RAW 3-cells:
first a 2-cell vertical congruence on the original first interval,
then congruence on the original second interval. It is NOT a new
primitive horizontal axiom or a shortcut via equalized raw words. -/
def PolygonRotationThreeProof.horizontal
    {s t u : Site} {q r : Zigzag s t} {v w : Zigzag t u}
    {a a' : PolygonRotationSquare q r}
    {b b' : PolygonRotationSquare v w}
    (h : PolygonRotationThreeProof a a')
    (k : PolygonRotationThreeProof b b') :
    PolygonRotationThreeProof
      (polygonRotationLeftFirst a b)
      (polygonRotationLeftFirst a' b') :=
  .vertical
    (.verticalLeft (.rightContext h v) (.leftContext r b))
    (.verticalRight (.rightContext a' v) (.leftContext r k))

/-- The derived raw horizontal pasting is sound in the genuinely
independent degree-kernel 3-Hom, with precisely matching endpoints. -/
theorem PolygonRotationThreeProof.horizontal_sound
    {s t u : Site} {q r : Zigzag s t} {v w : Zigzag t u}
    {a a' : PolygonRotationSquare q r}
    {b b' : PolygonRotationSquare v w}
    (h : PolygonRotationThreeProof a a')
    (k : PolygonRotationThreeProof b b') :
    (h.horizontal k).toKernel =
      PolygonRotationThreeCell.horizontal h.toKernel k.toKernel := by
  exact Subsingleton.elim _ _

/-- An actual E4 C60 rotation square has a RAW three-proof
witness connecting its unit-prefixed and canonical trees. -/
def polygonRotationUnitRawThreeProof (p : Polygon) (k l : Nat)
    (hkl : k ≤ l) (hl : l ≤ polygonSideCount p) :
    PolygonRotationThreeProof
      (polygonRotationSquareWithUnit p k l hkl hl)
      (polygonRotationSquare p k l hkl hl) :=
  .leftUnit (polygonRotationSquare p k l hkl hl)

/-- Raw 3-proof trees are themselves nontrivial: the direct identity
and two identities pasted sequentially are not definitionally equal.
Only their E5A degree-kernel 3-Hom images are identical. -/
theorem polygonThreeProof_ident_ne_withUnit
    {s t : Site} {q r : Zigzag s t}
    (a : PolygonRotationSquare q r) :
    (PolygonRotationThreeProof.ident a) ≠
      (PolygonRotationThreeProof.vertical
        (PolygonRotationThreeProof.ident a)
        (PolygonRotationThreeProof.ident a)) := by
  intro h
  cases h

/-- A fully concrete original C60 north pentagon E4 source, together
with the true empty right interval based at its actual target dart. -/
def northPentagonRotationRightIdentitySquare :
    PolygonRotationSquare
      (Zigzag.nil (Site.vertex
        (cyclicBoundaryDart (.pentagon .north) 1)))
      (Zigzag.nil (Site.vertex
        (cyclicBoundaryDart (.pentagon .north) 1))) :=
  .ident (Zigzag.nil _)

/-- A concrete new raw 3-dimensional interchange between two
DISTINCT raw E4 proof trees over the real north pentagon. -/
def northPentagonRotationRawExchange :
    PolygonRotationThreeProof
      (polygonRotationLeftFirst northPentagonFirstRotationSquare
        northPentagonRotationRightIdentitySquare)
      (polygonRotationRightFirst northPentagonFirstRotationSquare
        northPentagonRotationRightIdentitySquare) :=
  .exchange northPentagonFirstRotationSquare
    northPentagonRotationRightIdentitySquare

#print axioms PolygonRotationThreeProof
#print axioms PolygonRotationThreeProof.degree_sound
#print axioms PolygonRotationThreeProof.toKernel
#print axioms PolygonRotationThreeProof.horizontal
#print axioms PolygonRotationThreeProof.horizontal_sound
#print axioms polygonRotationUnitRawThreeProof
#print axioms polygonThreeProof_ident_ne_withUnit
#print axioms northPentagonRotationRawExchange
end
end Kuu.F112.Physical
