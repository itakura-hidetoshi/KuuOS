import Kuu.F112.PolygonBracketRoutes

/-!
# F112-E6B / nine-constructor F55-shaped C60-sector 3-source

This is an INDEPENDENT physical-bracket source, rather than the original
F55 PresentedCell imported from the frozen KUOS/Gray tree. Its real
leaves come from original C60 sectors in E6A. We now construct BOTH
orders of two independent contextual F54-like reassociations, the
freely presented pentagon and square 3-generators, and all SIX
remaining original F55-shaped operations, for NINE constructors total.

An explicit additive (Int × Int) × ZMod 2 interpretation is proved
for the full new source. The generator charges are (1,0) for pentagon
and (0,1) for square, with nonzero square phase 1. This is a chosen
INDEPENDENT SHADOW semantics, NOT a proof of the historical original
F55 charge/phase comparison. Its phase-parity obstruction is derived
by induction for the ENTIRE raw grammar (not postulated).

No old KUOS/Gray/F51/F77 import or nonstandard axiom is introduced.
-/

namespace Kuu.F112.Physical
set_option autoImplicit false
noncomputable section

/-- Two actual independent, contextual local association changes:
the first genuine bracket rotation is on the LEFT subtree. -/
def polygonBracketSquareLeftFirst {p : Polygon}
    {a b c d : PolygonBracketTree p}
    (left : PolygonBracketRotation p a b)
    (right : PolygonBracketRotation p c d) :
    PolygonBracketRoute p (.node a c) (.node b d) :=
  .trans
    (.leftContext (.step left) c)
    (.rightContext b (.step right))

/-- The RIGHT reassociation is performed before the left one.
Both routes have precisely the same (genuine typed) endpoints. -/
def polygonBracketSquareRightFirst {p : Polygon}
    {a b c d : PolygonBracketTree p}
    (left : PolygonBracketRotation p a b)
    (right : PolygonBracketRotation p c d) :
    PolygonBracketRoute p (.node a c) (.node b d) :=
  .trans
    (.rightContext a (.step right))
    (.leftContext (.step left) d)

theorem polygonBracketSquareLeftFirst_count {p : Polygon}
    {a b c d : PolygonBracketTree p}
    (left : PolygonBracketRotation p a b)
    (right : PolygonBracketRotation p c d) :
    (polygonBracketSquareLeftFirst left right).rotationCount = 2 := by
  rfl

theorem polygonBracketSquareRightFirst_count {p : Polygon}
    {a b c d : PolygonBracketTree p}
    (left : PolygonBracketRotation p a b)
    (right : PolygonBracketRotation p c d) :
    (polygonBracketSquareRightFirst left right).rotationCount = 2 := by
  rfl

/-- An internal raw-grammar discriminator; this does not identify
two different type-indexed source brackets. -/
def PolygonBracketRoute.leadingContextTag
    {p : Polygon} {a b : PolygonBracketTree p} :
    PolygonBracketRoute p a b → Nat
  | .leftContext _ _ => 1
  | .rightContext _ _ => 2
  | _ => 0

def PolygonBracketRoute.firstPastingTag
    {p : Polygon} {a b : PolygonBracketTree p} :
    PolygonBracketRoute p a b → Nat
  | .trans f _ => f.leadingContextTag
  | _ => 0

/-- The two genuine 2-step routes are DISTINCT RAW witnesses.
They are connected only by the explicit, separately typed 3-source
generator below, never by path equality or quotient evaluation. -/
theorem polygonBracketSquareLeft_ne_right {p : Polygon}
    {a b c d : PolygonBracketTree p}
    (left : PolygonBracketRotation p a b)
    (right : PolygonBracketRotation p c d) :
    polygonBracketSquareLeftFirst left right ≠
      polygonBracketSquareRightFirst left right := by
  intro h
  have ht := congrArg PolygonBracketRoute.firstPastingTag h
  change (1 : Nat) = 2 at ht
  exact (by decide : (1 : Nat) ≠ 2) ht

/-- Exactly NINE old-F55-shaped raw 3-proof constructors, over
actually typed C60-sector bracket routes. In particular the
pentagon relates DISTINCT 3-vs-2 paths; the square relates
distinct ordered 2-vs-2 contextual rotation paths. -/
inductive PolygonBracketCell (p : Polygon) :
    {a b : PolygonBracketTree p} →
    PolygonBracketRoute p a b → PolygonBracketRoute p a b → Type where
  | ident {a b : PolygonBracketTree p}
      (f : PolygonBracketRoute p a b) : PolygonBracketCell p f f
  | pentagon (a b c d : PolygonBracketTree p) :
      PolygonBracketCell p
        (polygonBracketPentagonLong a b c d)
        (polygonBracketPentagonShort a b c d)
  | disjointSquare {a b c d : PolygonBracketTree p}
      (left : PolygonBracketRotation p a b)
      (right : PolygonBracketRotation p c d) :
      PolygonBracketCell p
        (polygonBracketSquareLeftFirst left right)
        (polygonBracketSquareRightFirst left right)
  | symm {a b : PolygonBracketTree p}
      {f g : PolygonBracketRoute p a b}
      (cell : PolygonBracketCell p f g) : PolygonBracketCell p g f
  | trans {a b : PolygonBracketTree p}
      {f g h : PolygonBracketRoute p a b}
      (cell : PolygonBracketCell p f g)
      (other : PolygonBracketCell p g h) :
      PolygonBracketCell p f h
  | leftContext {a b : PolygonBracketTree p}
      {f g : PolygonBracketRoute p a b}
      (cell : PolygonBracketCell p f g) (c : PolygonBracketTree p) :
      PolygonBracketCell p (.leftContext f c) (.leftContext g c)
  | rightContext (a : PolygonBracketTree p)
      {b c : PolygonBracketTree p} {f g : PolygonBracketRoute p b c}
      (cell : PolygonBracketCell p f g) :
      PolygonBracketCell p (.rightContext a f) (.rightContext a g)
  | precompose {a b c : PolygonBracketTree p}
      (prior : PolygonBracketRoute p a b)
      {f g : PolygonBracketRoute p b c}
      (cell : PolygonBracketCell p f g) :
      PolygonBracketCell p (.trans prior f) (.trans prior g)
  | postcompose {a b c : PolygonBracketTree p}
      {f g : PolygonBracketRoute p a b}
      (cell : PolygonBracketCell p f g)
      (suffix : PolygonBracketRoute p b c) :
      PolygonBracketCell p (.trans f suffix) (.trans g suffix)

/-- Three proof-relevant shadow coordinates:
two integer generator counts, and the separately retained
ZMod 2 exchange phase. No phase is inferred from E4 localization. -/
abbrev PolygonBracketNativeShadow := (Int × Int) × ZMod 2

/-- A real source term gets its shadow by RECURSION over all
nine 3-generators. Crucially exchange has phase 1 and
is not mapped to zero just because its two paths share endpoints. -/
def PolygonBracketCell.nativeShadow
    {p : Polygon} {a b : PolygonBracketTree p}
    {f g : PolygonBracketRoute p a b}
    (cell : PolygonBracketCell p f g) : PolygonBracketNativeShadow :=
  match cell with
  | .ident _ => 0
  | .pentagon _ _ _ _ => (((1 : Int), (0 : Int)), (0 : ZMod 2))
  | .disjointSquare _ _ => (((0 : Int), (1 : Int)), (1 : ZMod 2))
  | .symm c => -c.nativeShadow
  | .trans c d => c.nativeShadow + d.nativeShadow
  | .leftContext c _ => c.nativeShadow
  | .rightContext _ c => c.nativeShadow
  | .precompose _ c => c.nativeShadow
  | .postcompose c _ => c.nativeShadow

/-- Native pentagon generator carries its own nonzero (1,0) charge,
distinct from the physical C60 polygon's five boundary edges. -/
theorem polygonBracketPentagon_nativeShadow {p : Polygon}
    (a b c d : PolygonBracketTree p) :
    (PolygonBracketCell.pentagon a b c d).nativeShadow =
      (((1 : Int), (0 : Int)), (0 : ZMod 2)) := by
  rfl

/-- The genuine disjoint rotation square has independent integer
square charge and a NONZERO exchange phase in this new receiver. -/
theorem polygonBracketSquare_nativeShadow {p : Polygon}
    {a b c d : PolygonBracketTree p}
    (left : PolygonBracketRotation p a b)
    (right : PolygonBracketRotation p c d) :
    (PolygonBracketCell.disjointSquare left right).nativeShadow =
      (((0 : Int), (1 : Int)), (1 : ZMod 2)) := by
  rfl

/-- The chosen phase equals square charge mod 2 FOR ALL NINE
constructors. This is PROVED by full induction, not imposed as
an axiom or retroactively inferred from the old F55 target. -/
theorem PolygonBracketCell.phase_squareParity
    {p : Polygon} {a b : PolygonBracketTree p}
    {f g : PolygonBracketRoute p a b}
    (cell : PolygonBracketCell p f g) :
    ((cell.nativeShadow.1.2 : Int) : ZMod 2) =
      cell.nativeShadow.2 := by
  induction cell with
  | ident _ => rfl
  | pentagon _ _ _ _ => rfl
  | disjointSquare _ _ => rfl
  | symm c ih =>
      change ((-c.nativeShadow.1.2 : Int) : ZMod 2) =
        -c.nativeShadow.2
      simpa using congrArg (fun z : ZMod 2 => -z) ih
  | trans c d ihc ihd =>
      change ((c.nativeShadow.1.2 + d.nativeShadow.1.2 : Int) :
        ZMod 2) = c.nativeShadow.2 + d.nativeShadow.2
      simpa using congrArg₂ (fun x y : ZMod 2 => x + y) ihc ihd
  | leftContext c w ih => exact ih
  | rightContext w c ih => exact ih
  | precompose w c ih => exact ih
  | postcompose c w ih => exact ih

/-- A concrete independent source obstruction:
the odd square charge ONE cannot have phase ZERO.
This is an E6B SHADOW non-lift, NOT the original historical F55 Δ
non-lift before a type-faithful old/new source comparison. -/
theorem PolygonBracketCell.no_shadow_delta
    {p : Polygon} {a b : PolygonBracketTree p}
    {f g : PolygonBracketRoute p a b}
    (cell : PolygonBracketCell p f g) :
    cell.nativeShadow ≠
      (((0 : Int), (1 : Int)), (0 : ZMod 2)) := by
  intro h
  have hs := congrArg
    (fun z : PolygonBracketNativeShadow => z.1.2) h
  have hp := congrArg
    (fun z : PolygonBracketNativeShadow => z.2) h
  change cell.nativeShadow.1.2 = (1 : Int) at hs
  change cell.nativeShadow.2 = (0 : ZMod 2) at hp
  have hpar := cell.phase_squareParity
  rw [hs, hp] at hpar
  exact (by decide : (1 : ZMod 2) ≠ 0) (by simpa using hpar)

/-- Horizontal composition of raw 3-cells uses the TWO actual
F54-shaped route contexts and their genuinely typed pre/post
pasting. It is derived from the original nine-constructor grammar. -/
def PolygonBracketCell.horizontal
    {p : Polygon}
    {a b c d : PolygonBracketTree p}
    {left left' : PolygonBracketRoute p a b}
    {right right' : PolygonBracketRoute p c d}
    (f : PolygonBracketCell p left left')
    (g : PolygonBracketCell p right right') :
    PolygonBracketCell p
      (.trans (.leftContext left c) (.rightContext b right))
      (.trans (.leftContext left' c) (.rightContext b right')) :=
  .trans
    (.postcompose (.leftContext f c) (.rightContext b right))
    (.precompose (.leftContext left' c) (.rightContext b g))

/-- The derived horizontal 3-cell pasting preserves BOTH independent
integer charges and the exchange phase, rather than assuming an
unproved global Gray interchange law. -/
theorem PolygonBracketCell.horizontal_nativeShadow
    {p : Polygon}
    {a b c d : PolygonBracketTree p}
    {left left' : PolygonBracketRoute p a b}
    {right right' : PolygonBracketRoute p c d}
    (f : PolygonBracketCell p left left')
    (g : PolygonBracketCell p right right') :
    (f.horizontal g).nativeShadow = f.nativeShadow + g.nativeShadow := by
  rfl

/-- Every actual C60 hexagon supplies all SIX independent physical
boundary sectors, so both disjoint associators really are built from
distinct original polygon-side witnesses. -/
def physicalHexagonBracketLeaf (t : Triangle) (i : Fin 6) :
    PolygonBracketTree (.hexagon t) :=
  .leaf ⟨i, by simp [polygonSideCount]⟩

def physicalHexagonLeftRotation (t : Triangle) :
    PolygonBracketRotation (.hexagon t)
      (.node
        (.node (physicalHexagonBracketLeaf t 0) (physicalHexagonBracketLeaf t 1))
        (physicalHexagonBracketLeaf t 2))
      (.node (physicalHexagonBracketLeaf t 0)
        (.node (physicalHexagonBracketLeaf t 1) (physicalHexagonBracketLeaf t 2))) :=
  .assoc _ _ _

def physicalHexagonRightRotation (t : Triangle) :
    PolygonBracketRotation (.hexagon t)
      (.node
        (.node (physicalHexagonBracketLeaf t 3) (physicalHexagonBracketLeaf t 4))
        (physicalHexagonBracketLeaf t 5))
      (.node (physicalHexagonBracketLeaf t 3)
        (.node (physicalHexagonBracketLeaf t 4) (physicalHexagonBracketLeaf t 5))) :=
  .assoc _ _ _

/-- An ACTUAL geometric north-adjacent C60 hexagon, with
six ORIGINAL ordered physical boundary sides, has an F55-like
freely presented source interchanger with nonzero shadow phase. -/
def northTopHexagonBracketSquare :
    PolygonBracketCell (.hexagon (.top 0))
      (polygonBracketSquareLeftFirst
        (physicalHexagonLeftRotation (.top 0))
        (physicalHexagonRightRotation (.top 0)))
      (polygonBracketSquareRightFirst
        (physicalHexagonLeftRotation (.top 0))
        (physicalHexagonRightRotation (.top 0))) :=
  .disjointSquare
    (physicalHexagonLeftRotation (.top 0))
    (physicalHexagonRightRotation (.top 0))

theorem northTopHexagonBracketSquare_phase_nonzero :
    northTopHexagonBracketSquare.nativeShadow.2 ≠ (0 : ZMod 2) := by
  decide

#print axioms polygonBracketSquareLeftFirst_count
#print axioms polygonBracketSquareRightFirst_count
#print axioms polygonBracketSquareLeft_ne_right
#print axioms PolygonBracketCell
#print axioms PolygonBracketCell.nativeShadow
#print axioms polygonBracketPentagon_nativeShadow
#print axioms polygonBracketSquare_nativeShadow
#print axioms PolygonBracketCell.phase_squareParity
#print axioms PolygonBracketCell.no_shadow_delta
#print axioms PolygonBracketCell.horizontal
#print axioms PolygonBracketCell.horizontal_nativeShadow
#print axioms northTopHexagonBracketSquare_phase_nonzero
end
end Kuu.F112.Physical
