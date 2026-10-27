import Kuu.F112.PolygonNativeC60GeometricTreeFillingGate

/-!
# F112-P94D3DQ — a Type-valued 17D structural certificate, and its exact obstruction

DO constructs all finite genuine strict context-tree transports. DP
isolates the exact all-tree sixteen-dimensional BV holonomy gate. DQ
CONSTRUCTS a genuinely dependent NEXT-DIMENSION witness, while
distinguishing an explicitly declared structural 17D presentation from
a previously established ORIGINAL geometric C60 17-cell.

The original lower layer is the true C60 14D/15D fiber. Its context-
closed BC 16D syntax preserves all genuine 15D witnesses, all original
CN generators and complete BV provenance codes. The NEXT AX layer
has genuine RAW 16D proof terms as objects, with their exact dependent
15D boundaries. Its limited signature contains ONLY the three
structural CF triangles (left/right cancellations and zigzag), with
both raw16D paths and the CF relation certificate stored in a Type-valued
higher generator. No horizontal interchange, arbitrary filler, or
new relation between nonparallel original 15D terms is declared.

We construct the positive 17D triangle between the actual three-step
zigzag and its independent single 16D atom, under EVERY finite genuine
C60 AQ context tree. Its endpoints are distinct raw16D proof terms
even though their original selected strict Kuu arrows agree. Every
finite composite of such DECLARED 17D proof terms preserves COMPLETE
original noncommutative BV holonomy, by induction over its true
higher-dimensional constructors.

This yields an exact negative: a genuine positive 16D diamond with
distinct original 15D midpoint evidence has NO 17D comparison in
the structural triangle-only next-level signature, even after
arbitrary finite C60 context trees. The free-word obstruction survives
context by BW's proved injectivity. This is a signature-specific
obstruction and not an unconditional no-go for all conceivable
alternative geometric extensions.

The physical AU comparison has a positive 17D certificate in this
explicitly adjoined relative presentation at every tree. The
nonparallel physical forward/reverse exchange continues to have NO
raw16D comparison in ANY original AX signature by BK. No geometric
17-cell in the original unextended C60 is claimed or manufactured.

Strict Kuu is the primary kernel; independent Kuu is a presentation.
All original 14D/15D boundaries, old no-go, 107 public roots, and
finite C60 gauge provenance are unchanged. No Gray, new logical
axioms, sorry or admit. Copyright Hidetoshi Itakura / 板倉英俊.
Apache-2.0.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u uD vD uE vE

/-- The ACTUAL next relative layer: its objects are genuine typed RAW
sixteen-dimensional terms, not their quotient, code, or Peiffer value. -/
def nativeC60DQSeventeenLayer
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L) :
    NativeC60AXLayer.{u} :=
  nativeC60AXNext L (nativeC60BCClosedSignature S F)

/-- Pack a genuine RAW 16D proof as an OBJECT of the 17D layer,
retaining both original dependent 15D endpoints without quotienting. -/
def nativeC60DQPackSixteen
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {a b : L.Total}
    (c : NativeC60AXStep (nativeC60BCClosedSignature S F) a b) :
    (nativeC60DQSeventeenLayer S F).Total :=
  ⟨(a, b), c⟩

/-- Exactly the limited CF structural triangles become NEW Type-valued
17D generator certificates. No comparison is added for an unrelated
parallel pair, and no underlying original geometric 17D relation is
assumed. The original complete raw16D terms c,d are both retained. -/
def nativeC60DQTriangleSeventeenSignature
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L) :
    NativeC60AXSignature (nativeC60DQSeventeenLayer S F) where
  Gen := fun x y =>
    Σ a : L.Total, Σ b : L.Total,
    Σ c : NativeC60AXStep (nativeC60BCClosedSignature S F) a b,
    Σ d : NativeC60AXStep (nativeC60BCClosedSignature S F) a b,
      {r : NativeC60CFTriangleRelation S F c d //
        x = nativeC60DQPackSixteen S F c ∧
        y = nativeC60DQPackSixteen S F d}
  boundary := by
    intro x y g
    rcases g with ⟨a, b, c, d, r⟩
    rw [r.property.1, r.property.2]
    rfl

/-- The original three-step 16D zigzag stores BOTH the chosen
forward atom, its reverse, and the same original atom again. -/
def nativeC60DQRawZigzag
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {a b : L.Total}
    (g : (nativeC60BCClosedSignature S F).Gen a b) :
    NativeC60AXStep (nativeC60BCClosedSignature S F) a b :=
  .trans (.trans (.atom g) (.symm (.atom g))) (.atom g)

/-- Construct the ACTUAL dependent 17D primitive comparing the
three-step raw16D zigzag with the one-step primitive. The witness is
explicitly declared and not an original geometric C60 filler. -/
def nativeC60DQZigzagSeventeen
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {a b : L.Total}
    (g : (nativeC60BCClosedSignature S F).Gen a b) :
    NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F)
      (nativeC60DQPackSixteen S F (nativeC60DQRawZigzag S F g))
      (nativeC60DQPackSixteen S F (.atom g)) :=
  .atom ⟨a, b, nativeC60DQRawZigzag S F g, .atom g,
    ⟨NativeC60CFTriangleRelation.zigzag g, ⟨rfl, rfl⟩⟩⟩

/-- True 17D globularity of the constructed certificate is verified
from the ORIGINAL proof-relevant 15D dependent endpoints. -/
theorem nativeC60DQZigzagSeventeen_boundary
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {a b : L.Total}
    (g : (nativeC60BCClosedSignature S F).Gen a b) :
    (nativeC60DQPackSixteen S F (nativeC60DQRawZigzag S F g)).1 =
      (nativeC60DQPackSixteen S F
        (.atom g : NativeC60AXStep (nativeC60BCClosedSignature S F) a b)).1 :=
  (nativeC60DQZigzagSeventeen S F g).boundary

/-- In original raw sixteen-dimensional syntax the zigzag is NOT the
atomic term: structural 17D evidence does not erase 16D provenance. -/
theorem nativeC60DQRawZigzag_ne_atom
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {a b : L.Total}
    (g : (nativeC60BCClosedSignature S F).Gen a b) :
    nativeC60DQRawZigzag S F g ≠
      (NativeC60AXStep.atom g) := by
  intro h
  cases h

/-- The complete original noncommutative BV holonomy of a RAW 16D
proof object is the invariant used at the next dimension. -/
def nativeC60DQSeventeenHolonomy
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L) :
    (nativeC60DQSeventeenLayer S F).Total →
      FreeGroup (NativeC60BVGeneratorCode S) :=
  fun x => nativeC60BWFreeHolonomy S F x.2

/-- Every ADJOINED 17D triangle generator preserves the WHOLE original
signed noncommutative free word, not only Peiffer/parity. The proof
uses the typed CF triangle compatibility theorem. -/
theorem nativeC60DQSeventeenGenerator_BV
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {x y : (nativeC60DQSeventeenLayer S F).Total}
    (g : (nativeC60DQTriangleSeventeenSignature S F).Gen x y) :
    nativeC60DQSeventeenHolonomy S F x =
      nativeC60DQSeventeenHolonomy S F y := by
  rcases g with ⟨a, b, c, d, ⟨r, ⟨hx, hy⟩⟩⟩
  rw [hx, hy]
  exact nativeC60CFTriangle_compatible S F c d r

/-- TRUE 17D induction: all arbitrarily composed, inverted and
parenthesized structural triangle certificates preserve FULL BV
provenance. No additional 17D equality axiom is introduced. -/
theorem nativeC60DQSeventeenPath_BV
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {x y : (nativeC60DQSeventeenLayer S F).Total}
    (path : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) x y) :
    nativeC60DQSeventeenHolonomy S F x =
      nativeC60DQSeventeenHolonomy S F y := by
  exact NativeC60AXStep.observer_sound
    (nativeC60DQSeventeenHolonomy S F)
    (by
      intro x y g
      exact nativeC60DQSeventeenGenerator_BV S F g) path

/-- The exact proof-relevant nonexistence gate: distinct BV free words
preclude even a Type-valued 17D path in the chosen triangle-only
structural higher grammar, regardless of its finite length. -/
theorem nativeC60DQNoSeventeen_of_BV_mismatch
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (x y : (nativeC60DQSeventeenLayer S F).Total)
    (hne : nativeC60DQSeventeenHolonomy S F x ≠
      nativeC60DQSeventeenHolonomy S F y) :
    ¬ Nonempty
      (NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) x y) := by
  rintro ⟨path⟩
  exact hne (nativeC60DQSeventeenPath_BV S F path)

/-- An arbitrary finite chronological C60 AQ tree transports the
ENTIRE original 16D zigzag into a new, actually typed raw16D zigzag
with its physically ordered inner prefix and unchanged proof source. -/
theorem nativeC60DQTreeZigzag_raw_transport
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (tree : NativeK5DOContextTree)
    {a b : L.Total}
    (g : (nativeC60BCClosedSignature S F).Gen a b) :
    nativeC60BCMapClosedStep S F (nativeK5DOTreeWord tree)
        (nativeC60DQRawZigzag S F g) =
      nativeC60DQRawZigzag S F
        (nativeC60BCShiftGen S F (nativeK5DOTreeWord tree) g) :=
  rfl

/-- For EVERY finite genuine AQ tree there is a CONSTRUCTED typed
structural 17D comparison between the entire transported original
16D zigzag and the original contextual 16D primitive. This does NOT
create an unprovided original C60 geometric 17-cell. -/
def nativeC60DQTreeZigzagSeventeen
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (tree : NativeK5DOContextTree)
    {a b : L.Total}
    (g : (nativeC60BCClosedSignature S F).Gen a b) :
    let shifted := nativeC60BCShiftGen S F (nativeK5DOTreeWord tree) g
    NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F)
      (nativeC60DQPackSixteen S F (nativeC60DQRawZigzag S F shifted))
      (nativeC60DQPackSixteen S F (.atom shifted)) :=
  nativeC60DQZigzagSeventeen S F
    (nativeC60BCShiftGen S F (nativeK5DOTreeWord tree) g)

/-- The context-framed original RAW 16D zigzag is still distinct
from its underlying original generator at EVERY finite AQ tree. -/
theorem nativeC60DQTreeZigzag_raw_ne_atom
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (tree : NativeK5DOContextTree)
    {a b : L.Total}
    (g : (nativeC60BCClosedSignature S F).Gen a b) :
    nativeC60BCMapClosedStep S F (nativeK5DOTreeWord tree)
        (nativeC60DQRawZigzag S F g) ≠
      nativeC60BCMapClosedStep S F (nativeK5DOTreeWord tree)
        (NativeC60AXStep.atom g) := by
  rw [nativeC60DQTreeZigzag_raw_transport S F tree g]
  change nativeC60DQRawZigzag S F
      (nativeC60BCShiftGen S F (nativeK5DOTreeWord tree) g) ≠
    NativeC60AXStep.atom (nativeC60BCShiftGen S F
      (nativeK5DOTreeWord tree) g)
  exact nativeC60DQRawZigzag_ne_atom S F _

/-- A positive 16D diamond with two DIFFERENT actual 15D middle
proof witnesses cannot admit a 17D triangle-only certificate. The
failure is deduced from ORIGINAL complete free holonomy, not a
fabricated higher obstruction class. -/
theorem nativeC60DQDiamond_no_seventeen
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (q : NativeC60CFTypedDiamond S F)
    (hne : q.leftMid ≠ q.rightMid) :
    ¬ Nonempty (NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F)
      (nativeC60DQPackSixteen S F (nativeC60CFDiamondLeft S F q))
      (nativeC60DQPackSixteen S F (nativeC60CFDiamondRight S F q))) := by
  apply nativeC60DQNoSeventeen_of_BV_mismatch S F
  intro hfree
  exact (nativeC60CFDiamond_distinct_midpoint_no_strict S F [] q hne)
    ((nativeC60CDAll_raw_free_eq_iff_strict S F []
      (nativeC60CFDiamondLeft S F q)
      (nativeC60CFDiamondRight S F q)).mp hfree)

/-- THE STRONG OBSTRUCTION: arbitrary 14D AQ context-tree framing
cannot manufacture a structural 17D path between distinct-midpoint
ORIGINAL 16D diamond routes. Injectivity of the full BV prefix
retains the original noncommutative generator separation. -/
theorem nativeC60DQDiamond_no_seventeen_all_trees
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (q : NativeC60CFTypedDiamond S F)
    (hne : q.leftMid ≠ q.rightMid)
    (tree : NativeK5DOContextTree) :
    ¬ Nonempty (NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F)
      (nativeC60DQPackSixteen S F
        (nativeC60BCMapClosedStep S F (nativeK5DOTreeWord tree)
          (nativeC60CFDiamondLeft S F q)))
      (nativeC60DQPackSixteen S F
        (nativeC60BCMapClosedStep S F (nativeK5DOTreeWord tree)
          (nativeC60CFDiamondRight S F q)))) := by
  apply nativeC60DQNoSeventeen_of_BV_mismatch S F
  have horiginal : nativeC60BWFreeHolonomy S F
      (nativeC60CFDiamondLeft S F q) ≠
      nativeC60BWFreeHolonomy S F
        (nativeC60CFDiamondRight S F q) := by
    intro hf
    exact (nativeC60CFDiamond_distinct_midpoint_no_strict S F [] q hne)
      ((nativeC60CDAll_raw_free_eq_iff_strict S F [] _ _).mp hf)
  intro hframed
  change nativeC60BWFreeHolonomy S F
      (nativeC60BCMapClosedStep S F (nativeK5DOTreeWord tree)
        (nativeC60CFDiamondLeft S F q)) =
    nativeC60BWFreeHolonomy S F
      (nativeC60BCMapClosedStep S F (nativeK5DOTreeWord tree)
        (nativeC60CFDiamondRight S F q)) at hframed
  rw [nativeC60BWFreeHolonomy_frame S F (nativeK5DOTreeWord tree)
      (nativeC60CFDiamondLeft S F q),
    nativeC60BWFreeHolonomy_frame S F (nativeK5DOTreeWord tree)
      (nativeC60CFDiamondRight S F q)] at hframed
  exact horiginal ((nativeC60BWFreePrefix_injective S
    (nativeK5DOTreeWord tree)) hframed)

/-- Compose genuine Type-valued 17D structural triangle and its
inverse to obtain an original boundary-typed 17D roundtrip. -/
def nativeC60DQSeventeenRoundtrip
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {a b : L.Total}
    (g : (nativeC60BCClosedSignature S F).Gen a b) :
    NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F)
      (nativeC60DQPackSixteen S F (nativeC60DQRawZigzag S F g))
      (nativeC60DQPackSixteen S F (nativeC60DQRawZigzag S F g)) :=
  .trans (nativeC60DQZigzagSeventeen S F g)
    (.symm (nativeC60DQZigzagSeventeen S F g))

/-- The actual 17D roundtrip is STRICTLY the identity in its
SELECTED Kuu structural presentation. No raw17D path is erased. -/
theorem nativeC60DQSeventeenRoundtrip_strict_id
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {a b : L.Total}
    (g : (nativeC60BCClosedSignature S F).Gen a b) :
    nativeC60AZStrictStep (nativeC60DQTriangleSeventeenSignature S F)
        (nativeC60AZNoRelations (nativeC60DQTriangleSeventeenSignature S F))
        (nativeC60DQSeventeenRoundtrip S F g) =
      𝟙 ((nativeC60AZStrictProject
        (nativeC60DQTriangleSeventeenSignature S F)
        (nativeC60AZNoRelations (nativeC60DQTriangleSeventeenSignature S F))).obj
        ⟨nativeC60DQPackSixteen S F (nativeC60DQRawZigzag S F g)⟩) :=
  nativeC60AZStrictStep_inv_left
    (nativeC60DQTriangleSeventeenSignature S F)
    (nativeC60AZNoRelations (nativeC60DQTriangleSeventeenSignature S F))
    (nativeC60DQZigzagSeventeen S F g)

section OriginalPhysicalC60

variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable {first : KuuNativeF45Tree p n m ma pa mb pb}
variable {last : KuuNativeF45Tree p n' m' ma pa mb pb}
variable {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
variable {f g : NativeF55StructuralComparison p r s}
variable {alpha beta : NativeK5StructuralFourCell p f g}
variable {w z : NativeK5StructuralFiveCell p alpha beta}
variable {u v : NativeK5StructuralSixCell p w z}
variable {h k : NativeK5StructuralSevenCell p u v}
variable {e d : NativeK5StructuralEightCell p h k}
variable {q t : NativeK5StructuralNineCell p e d}
variable {P Q : NativeK5StructuralTenCell p q t}
variable {H K : NativeK5StructuralElevenCell p P Q}
variable {U V : NativeK5StructuralTwelveCell p H K}

/-- For every original C60 context tree, the physical AU comparison
has a genuinely constructed Type-valued 17D triangle certificate in
the EXPLICITLY DECLARED relative extension. In the same physical
context, BK still forbids ANY original typed 16D comparator between
the NONPARALLEL exchange and its inverse, for ANY AX signature. -/
theorem nativeK5DQPhysicalAU_seventeen_and_nonparallel_no_sixteen
    (W : NativeK5StructuralThirteenCell p U V)
    (tree : NativeK5DOContextTree)
    (T : NativeC60AXSignature (nativeK5AXBaseLayer W)) :
    let S := nativeK5AXKuuSignature W
    let F := nativeK5BCFrame W
    let shifted := nativeC60BCShiftGen S F (nativeK5DOTreeWord tree)
      (nativeK5CEPhysicalAUGenerator W)
    Nonempty (NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F)
      (nativeC60DQPackSixteen S F (nativeC60DQRawZigzag S F shifted))
      (nativeC60DQPackSixteen S F (.atom shifted))) ∧
      ¬ Nonempty (NativeC60AXStep T
        (nativeK5BKExchangeForward W (nativeK5DOTreeWord tree))
        (nativeK5BKExchangeBackward W (nativeK5DOTreeWord tree))) := by
  dsimp only
  exact ⟨⟨nativeC60DQTreeZigzagSeventeen
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W) tree
      (nativeK5CEPhysicalAUGenerator W)⟩,
    nativeK5BKExchange_no_sixteen_cell W (nativeK5DOTreeWord tree) T⟩

end OriginalPhysicalC60

#print axioms nativeC60DQSeventeenLayer
#print axioms nativeC60DQPackSixteen
#print axioms nativeC60DQTriangleSeventeenSignature
#print axioms nativeC60DQRawZigzag
#print axioms nativeC60DQZigzagSeventeen
#print axioms nativeC60DQZigzagSeventeen_boundary
#print axioms nativeC60DQRawZigzag_ne_atom
#print axioms nativeC60DQSeventeenHolonomy
#print axioms nativeC60DQSeventeenGenerator_BV
#print axioms nativeC60DQSeventeenPath_BV
#print axioms nativeC60DQNoSeventeen_of_BV_mismatch
#print axioms nativeC60DQTreeZigzag_raw_transport
#print axioms nativeC60DQTreeZigzagSeventeen
#print axioms nativeC60DQTreeZigzag_raw_ne_atom
#print axioms nativeC60DQDiamond_no_seventeen
#print axioms nativeC60DQDiamond_no_seventeen_all_trees
#print axioms nativeC60DQSeventeenRoundtrip
#print axioms nativeC60DQSeventeenRoundtrip_strict_id
#print axioms nativeK5DQPhysicalAU_seventeen_and_nonparallel_no_sixteen

end
end Kuu.F112.Physical
