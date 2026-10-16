import Kuu.F112.PolygonDepthAxes

/-!
# F112-E7B / dual-depth C60 bracket rotation paths and typed erasure

E7A supplies two independently indexed Nat depth axes on genuine C60
polygon-sector binary trees, including a proved erase_cast theorem.
This file now builds actual, freely generated, *dependent* rotation
routes over those trees. The two Nat indices are retained on BOTH
the start and end of each constructor.

A primitive associativity rotation uses precisely E7A's certified
two-axis cast. Independent depth transports have zero rotation steps.
Route composition and both binary contexts preserve their endpoints.

A separately proved comparison sends EVERY such typed route to the
genuine E6A physical-sector raw bracket-route grammar. This map is
not declared faithful: pure depth casts forget to identity paths,
and historical F19/F28 Blocks/F54/F55 source equivalence remains
unproved. No KUOS.*, Gray, F51 or F77 imports.
-/

namespace Kuu.F112.Physical
set_option autoImplicit false
noncomputable section

/-- A source rotation route with FOUR indexed endpoints: both
independent depth axes at its source and its target. -/
inductive PolygonDepthRoute (p : Polygon) :
    {n m n' m' : Nat} →
      PolygonDepthTree p n m → PolygonDepthTree p n' m' → Type where
  | ident {n m : Nat} (a : PolygonDepthTree p n m) :
      PolygonDepthRoute p a a
  | assoc {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
      (a : PolygonDepthTree p n₁ m₁)
      (b : PolygonDepthTree p n₂ m₂)
      (c : PolygonDepthTree p n₃ m₃) :
      PolygonDepthRoute p (.node (.node a b) c)
        (polygonDepthAssoc a b c)
  | castDepths {n n' m m' : Nat}
      (hn : n = n') (hm : m = m')
      (a : PolygonDepthTree p n m) :
      PolygonDepthRoute p a
        (cast (congrArg₂ (PolygonDepthTree p) hn hm) a)
  | trans {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
      {a : PolygonDepthTree p n₁ m₁}
      {b : PolygonDepthTree p n₂ m₂}
      {c : PolygonDepthTree p n₃ m₃}
      (f : PolygonDepthRoute p a b)
      (g : PolygonDepthRoute p b c) :
      PolygonDepthRoute p a c
  | leftContext {n n' m m' k l : Nat}
      {a : PolygonDepthTree p n m}
      {b : PolygonDepthTree p n' m'}
      (f : PolygonDepthRoute p a b)
      (c : PolygonDepthTree p k l) :
      PolygonDepthRoute p (.node a c) (.node b c)
  | rightContext {n n' m m' k l : Nat}
      (a : PolygonDepthTree p k l)
      {b : PolygonDepthTree p n m}
      {c : PolygonDepthTree p n' m'}
      (f : PolygonDepthRoute p b c) :
      PolygonDepthRoute p (.node a b) (.node a c)

/-- A target cast for the already verified E6A raw bracket routes.
No raw words or original physical sectors are identified by this
function: only a PROVED endpoint equality is transported. -/
def polygonBracketRouteCastTarget {p : Polygon}
    {a b c : PolygonBracketTree p}
    (h : b = c) (r : PolygonBracketRoute p a b) :
    PolygonBracketRoute p a c := by
  cases h
  exact r

/-- Transporting the target endpoint preserves the number of
primitive bracket rotations, by genuine equality induction. -/
theorem polygonBracketRouteCastTarget_count {p : Polygon}
    {a b c : PolygonBracketTree p}
    (h : b = c) (r : PolygonBracketRoute p a b) :
    (polygonBracketRouteCastTarget h r).rotationCount =
      r.rotationCount := by
  cases h
  rfl

/-- Every dependent, independently depth-indexed F54-shaped route
has an explicitly typed original-sector bracket-route erasure.
The physical generator is retained for local rotations; pure
index-equality transports become identity only in this comparison. -/
def PolygonDepthRoute.toBracketRoute {p : Polygon}
    {n m n' m' : Nat}
    {a : PolygonDepthTree p n m}
    {b : PolygonDepthTree p n' m'}
    (r : PolygonDepthRoute p a b) :
    PolygonBracketRoute p a.erase b.erase := by
  induction r with
  | ident a =>
      exact .ident a.erase
  | assoc a b c =>
      exact polygonBracketRouteCastTarget
        (polygonDepthAssoc_erase a b c).symm
        (.step (.assoc a.erase b.erase c.erase))
  | castDepths hn hm a =>
      exact polygonBracketRouteCastTarget
        (PolygonDepthTree.erase_cast hn hm a).symm
        (.ident a.erase)
  | trans f g ihf ihg =>
      exact .trans ihf ihg
  | leftContext f c ih =>
      exact .leftContext ih c.erase
  | rightContext a f ih =>
      exact .rightContext a.erase ih

/-- The dependent source counts genuine binary reassociations,
never the two independent depth casts or syntactic contexts. -/
def PolygonDepthRoute.rotationCount {p : Polygon}
    {n m n' m' : Nat}
    {a : PolygonDepthTree p n m}
    {b : PolygonDepthTree p n' m'} :
    PolygonDepthRoute p a b → Nat
  | .ident _ => 0
  | .assoc _ _ _ => 1
  | .castDepths _ _ _ => 0
  | .trans f g => f.rotationCount + g.rotationCount
  | .leftContext f _ => f.rotationCount
  | .rightContext _ f => f.rotationCount

/-- The comparison is compatible with the genuine number of
F54-shaped primitive rotations, including the two-axis cast steps.
This is not source-equivalence or assertion of a new direct Site arrow. -/
theorem PolygonDepthRoute.toBracketRoute_count {p : Polygon}
    {n m n' m' : Nat}
    {a : PolygonDepthTree p n m}
    {b : PolygonDepthTree p n' m'}
    (r : PolygonDepthRoute p a b) :
    r.toBracketRoute.rotationCount = r.rotationCount := by
  induction r with
  | ident a => rfl
  | assoc a b c =>
      change
        (polygonBracketRouteCastTarget
          (polygonDepthAssoc_erase a b c).symm
          (PolygonBracketRoute.step
            (PolygonBracketRotation.assoc a.erase b.erase c.erase))).rotationCount =
          1
      rw [polygonBracketRouteCastTarget_count]
      rfl
  | castDepths hn hm a =>
      change
        (polygonBracketRouteCastTarget
          (PolygonDepthTree.erase_cast hn hm a).symm
          (PolygonBracketRoute.ident a.erase)).rotationCount = 0
      rw [polygonBracketRouteCastTarget_count]
      rfl
  | trans f g ihf ihg =>
      change
        f.toBracketRoute.rotationCount + g.toBracketRoute.rotationCount =
          f.rotationCount + g.rotationCount
      rw [ihf, ihg]
  | leftContext f c ih =>
      change f.toBracketRoute.rotationCount = f.rotationCount
      exact ih
  | rightContext a f ih =>
      change f.toBracketRoute.rotationCount = f.rotationCount
      exact ih

/-- Real physical polygon-sector order is unchanged along ANY
dual-depth route, even one containing casts on both axes. -/
theorem PolygonDepthRoute.leaves_sound {p : Polygon}
    {n m n' m' : Nat}
    {a : PolygonDepthTree p n m}
    {b : PolygonDepthTree p n' m'}
    (r : PolygonDepthRoute p a b) :
    a.erase.leaves = b.erase.leaves :=
  r.toBracketRoute.leaves_sound

/-- The original three adjoining physical sectors of a true
north C60 pentagon, with independently chosen double depths. -/
def northDepthLeafAt (i : Fin 4) (n m : Nat) :
    PolygonDepthTree (.pentagon .north) n m :=
  polygonDepthLeafAt (.pentagon .north)
    (firstFourPolygonSector (.pentagon .north) i) n m

/-- An actual two-depth F54-shaped associator on three distinct
physical north-pentagon sectors. -/
def northThreeSectorDepthRotation :
    PolygonDepthRoute (.pentagon .north)
      (.node
        (.node (northDepthLeafAt 0 1 0) (northDepthLeafAt 1 0 1))
        (northDepthLeafAt 2 2 3))
      (polygonDepthAssoc
        (northDepthLeafAt 0 1 0)
        (northDepthLeafAt 1 0 1)
        (northDepthLeafAt 2 2 3)) :=
  .assoc _ _ _

/-- That concrete original C60 source has precisely ONE
non-collapsed primitive rotation, even after forgetting Nat indices. -/
theorem northThreeSectorDepthRotation_count :
    northThreeSectorDepthRotation.rotationCount = 1 := rfl

theorem northThreeSectorDepthRotation_erased_count :
    northThreeSectorDepthRotation.toBracketRoute.rotationCount = 1 := by
  rw [PolygonDepthRoute.toBracketRoute_count]
  rfl

/-- Nonidentity raw depth proofs remain distinguishable: inserting
an extra proof-unit is syntactically observable before any kernel. -/
theorem polygonDepthRoute_ident_ne_double {p : Polygon}
    {n m : Nat} (a : PolygonDepthTree p n m) :
    (PolygonDepthRoute.ident a) ≠
      (PolygonDepthRoute.trans
        (PolygonDepthRoute.ident a)
        (PolygonDepthRoute.ident a)) := by
  intro h
  cases h

#print axioms PolygonDepthRoute
#print axioms polygonBracketRouteCastTarget_count
#print axioms PolygonDepthRoute.toBracketRoute
#print axioms PolygonDepthRoute.rotationCount
#print axioms PolygonDepthRoute.toBracketRoute_count
#print axioms PolygonDepthRoute.leaves_sound
#print axioms northThreeSectorDepthRotation_count
#print axioms northThreeSectorDepthRotation_erased_count
#print axioms polygonDepthRoute_ident_ne_double
end
end Kuu.F112.Physical
