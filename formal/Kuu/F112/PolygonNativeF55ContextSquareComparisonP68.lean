import Kuu.F112.PolygonNativeF55TypedSquareRouteComparisonP67

/-!
# F112-P68 — context-closed proof-relevant F54 square comparisons

P67 constructs a Type-valued disjoint-square route witness and an exact
Setoid quotient of its mere existence. The original square comparison
only closes under equivalence; horizontal strictness also requires
compatibility with actual F54 contexts and route concatenation.

Instead of silently postulating this on P67's smaller presentation,
P68 provides a distinctly labeled CONTEXT-CLOSED comparison:
all original nine F55 constructors are inspected recursively.
Identity and genuine square are allowed; genuine pentagon is NOT an
elementary comparison. Inversion, vertical pasting, both binary-tree
contexts, and typed pre/post-route whiskering preserve admissibility.

The actual raw F55 Type-valued proof tree is carried in a subtype;
only Nonempty of this carrier is the Prop-valued Setoid relation.
Thus quotient equality neither chooses a raw proof term nor identifies
two original F55 histories from equal numerical shadows.

We construct the two honest context maps on this new quotient of F54
route objects and a canonical comparison map from P67 classes.
True original C60 disjoint-square classes become equal, while the
odd-phase F55 witness still exists in the unquotiented source.

This does NOT build all higher Hom transport needed for strict 3/n,
prove 3-dimensional interchange/associativity, or establish global
(infinity,3)-hyperdescent. No Gray, new axioms, sorry or admit.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

/-- Exactly the EIGHT genuine non-pentagon raw constructors generate
this independently selected context-closed square comparison.
The predicate is SOURCE syntactic, never a shadow test. -/
def KuuNativeF45Tree.DepthRotationRoute.PresentedCell.squareOnly
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb} :
    ∀ {u v : KuuNativeF45Tree.DepthRotationRoute p first last},
      KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v → Bool
  | _, _, .ident _ => true
  | _, _, .pentagon _ _ _ _ => false
  | _, _, .disjointSquare _ _ => true
  | _, _, .symm cell => cell.squareOnly
  | _, _, .trans left right => left.squareOnly && right.squareOnly
  | _, _, .leftContext cell _ => cell.squareOnly
  | _, _, .rightContext _ cell => cell.squareOnly
  | _, _, .precompose _ cell => cell.squareOnly
  | _, _, .postcompose cell _ => cell.squareOnly

/-- Carry the REAL raw F55 proof witness, not only a Prop or phase.
Every member is a completely typed cell of the source presentation. -/
abbrev NativeF55SquareOnlyCell
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {u v : KuuNativeF45Tree.DepthRotationRoute p first last} :=
  {cell : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v //
    cell.squareOnly = true}

/-- The smaller P67 square witness gives a concrete P68 raw witness
by a *Type-valued* recursion, retaining the actual historical tree. -/
def KuuNativeF45Tree.DepthRotationRoute.SquareComparable.toSquareOnlyCell
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb} :
    ∀ {u v : KuuNativeF45Tree.DepthRotationRoute p first last},
      KuuNativeF45Tree.DepthRotationRoute.SquareComparable p u v →
      NativeF55SquareOnlyCell (p := p) (u := u) (v := v)
  | _, _, .refl route => ⟨.ident route, rfl⟩
  | _, _, .symm h =>
      let w := h.toSquareOnlyCell
      ⟨.symm w.1, w.2⟩
  | _, _, .trans h k =>
      let w := h.toSquareOnlyCell
      let z := k.toSquareOnlyCell
      ⟨.trans w.1 z.1, by
        change w.1.squareOnly && z.1.squareOnly = true
        rw [w.2, z.2]
        rfl⟩
  | _, _, .square left right => ⟨.disjointSquare left right, rfl⟩

/-- The context-closed Type carrier yields a Setoid only by the
PROPOSITION that at least one original square-only raw cell exists.
No proof term is extracted from this Prop-valued relation. -/
def nativeF55ContextSquareRouteSetoid
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :
    Setoid (KuuNativeF45Tree.DepthRotationRoute p first last) where
  r := fun u v =>
    Nonempty (NativeF55SquareOnlyCell (p := p) (u := u) (v := v))
  iseqv := ⟨
    (fun u => ⟨⟨.ident u, rfl⟩⟩),
    (fun h => h.elim (fun w => ⟨⟨.symm w.1, w.2⟩⟩)),
    (fun h k => h.elim (fun w => k.elim (fun z =>
      ⟨⟨.trans w.1 z.1, by
        change w.1.squareOnly && z.1.squareOnly = true
        rw [w.2, z.2]
        rfl⟩⟩)))⟩

/-- Context-closed comparison classes on actual F54 route objects:
this is NOT the P64 higher-Hom structural-unit quotient. -/
abbrev NativeF55ContextSquareRouteClasses
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :=
  _root_.Quotient (nativeF55ContextSquareRouteSetoid first last)

/-- Projection of genuine raw F54 route witnesses to the new classes. -/
def nativeF55ContextSquareRouteClass
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (route : KuuNativeF45Tree.DepthRotationRoute p first last) :
    NativeF55ContextSquareRouteClasses first last :=
  _root_.Quotient.mk _ route

/-- Exact relation kernel: quotient class equality iff a REAL
square-only raw 3-cell exists at those typed route endpoints. -/
theorem nativeF55ContextSquareRouteClass_eq_iff
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (u v : KuuNativeF45Tree.DepthRotationRoute p first last) :
    nativeF55ContextSquareRouteClass first last u =
      nativeF55ContextSquareRouteClass first last v ↔
      Nonempty (NativeF55SquareOnlyCell (p := p) (u := u) (v := v)) := by
  constructor
  · intro h
    exact _root_.Quotient.exact h
  · intro h
    exact _root_.Quotient.sound h

/-- Actual left F54 binary-tree context on the full square-only
comparison QUOTIENT, proved by source proof-witness transport. -/
def nativeF55ContextSquareLeftClassMap
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' k l : Nat}
    {ma mb mc : KuuNativeBlocks a b}
    {pa pb pc : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (later : KuuNativeF45Tree p k l mb pb mc pc) :
    NativeF55ContextSquareRouteClasses first last →
      NativeF55ContextSquareRouteClasses
        (KuuNativeF45Tree.node first later)
        (KuuNativeF45Tree.node last later) :=
  _root_.Quotient.lift
    (fun route : KuuNativeF45Tree.DepthRotationRoute p first last =>
      nativeF55ContextSquareRouteClass
        (KuuNativeF45Tree.node first later)
        (KuuNativeF45Tree.node last later)
        (.leftContext route later))
    (by
      intro u v h
      apply _root_.Quotient.sound
      rcases h with ⟨w⟩
      exact ⟨⟨.leftContext w.1 later, w.2⟩⟩)

/-- The same native F54 operation on the right context, with the
original two-category depths and intermediate blocks preserved. -/
def nativeF55ContextSquareRightClassMap
    {p : Polygon} {a b : D} {x y : E}
    {k l n n' m m' : Nat}
    {ma mb mc : KuuNativeBlocks a b}
    {pa pb pc : KuuNativeBlocks x y}
    (earlier : KuuNativeF45Tree p k l ma pa mb pb)
    (first : KuuNativeF45Tree p n m mb pb mc pc)
    (last : KuuNativeF45Tree p n' m' mb pb mc pc) :
    NativeF55ContextSquareRouteClasses first last →
      NativeF55ContextSquareRouteClasses
        (KuuNativeF45Tree.node earlier first)
        (KuuNativeF45Tree.node earlier last) :=
  _root_.Quotient.lift
    (fun route : KuuNativeF45Tree.DepthRotationRoute p first last =>
      nativeF55ContextSquareRouteClass
        (KuuNativeF45Tree.node earlier first)
        (KuuNativeF45Tree.node earlier last)
        (.rightContext earlier route))
    (by
      intro u v h
      apply _root_.Quotient.sound
      rcases h with ⟨w⟩
      exact ⟨⟨.rightContext earlier w.1, w.2⟩⟩)

/-- The derived left action is exactly the original typed raw F54
context followed by quotient: no numerical observer is involved. -/
theorem nativeF55ContextSquareLeftClassMap_spec
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' k l : Nat}
    {ma mb mc : KuuNativeBlocks a b}
    {pa pb pc : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (later : KuuNativeF45Tree p k l mb pb mc pc)
    (route : KuuNativeF45Tree.DepthRotationRoute p first last) :
    nativeF55ContextSquareLeftClassMap first last later
      (nativeF55ContextSquareRouteClass first last route) =
      nativeF55ContextSquareRouteClass
        (KuuNativeF45Tree.node first later)
        (KuuNativeF45Tree.node last later)
        (.leftContext route later) := rfl

theorem nativeF55ContextSquareRightClassMap_spec
    {p : Polygon} {a b : D} {x y : E}
    {k l n n' m m' : Nat}
    {ma mb mc : KuuNativeBlocks a b}
    {pa pb pc : KuuNativeBlocks x y}
    (earlier : KuuNativeF45Tree p k l ma pa mb pb)
    (first : KuuNativeF45Tree p n m mb pb mc pc)
    (last : KuuNativeF45Tree p n' m' mb pb mc pc)
    (route : KuuNativeF45Tree.DepthRotationRoute p first last) :
    nativeF55ContextSquareRightClassMap earlier first last
      (nativeF55ContextSquareRouteClass first last route) =
      nativeF55ContextSquareRouteClass
        (KuuNativeF45Tree.node earlier first)
        (KuuNativeF45Tree.node earlier last)
        (.rightContext earlier route) := rfl

/-- Every P67 comparison class has a canonical IMAGE in the
context-closed P68 quotient, with no asserted inverse or equivalence:
the new presentation may identify further context-related routes. -/
def nativeF55P67ToContextSquareClasses
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :
    NativeF55SquareRouteClasses first last →
      NativeF55ContextSquareRouteClasses first last :=
  _root_.Quotient.lift
    (nativeF55ContextSquareRouteClass first last)
    (by
      intro u v h
      apply _root_.Quotient.sound
      rcases h with ⟨w⟩
      exact ⟨w.toSquareOnlyCell⟩)

/-- The P67-to-P68 comparison does not change representatives, but
does not claim faithful recovery of all original proof histories. -/
theorem nativeF55P67ToContextSquareClasses_spec
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (route : KuuNativeF45Tree.DepthRotationRoute p first last) :
    nativeF55P67ToContextSquareClasses first last
      (nativeF55SquareRouteClass first last route) =
      nativeF55ContextSquareRouteClass first last route := rfl

/-- The actual north C60 hexagon disjointSquare generator still
gives a comparison between the two genuine original F54 orders. -/
theorem northHexagonNativeSquare_context_class_eq :
    nativeF55ContextSquareRouteClass _ _ northHexagonNativeSquareLeft =
      nativeF55ContextSquareRouteClass _ _ northHexagonNativeSquareRight := by
  apply (nativeF55ContextSquareRouteClass_eq_iff _ _ _ _).2
  exact ⟨⟨northHexagonNativeF55SquareCell, rfl⟩⟩

/-- The genuine physical C60 primitive pentagon is NOT an
ELEMENTARY square-only generator. No assertion is made that every
pentagon boundary is noncomparable by some composed square route. -/
theorem northNativeF55PentagonCell_not_squareOnly :
    northNativeF55PentagonCell.squareOnly = false := rfl

/-- The true north C60 six-sector square IS an elementary
source witness, and retains its original proof-relevant parity. -/
theorem northHexagonNativeF55SquareCell_squareOnly :
    northHexagonNativeF55SquareCell.squareOnly = true := rfl

#print axioms KuuNativeF45Tree.DepthRotationRoute.PresentedCell.squareOnly
#print axioms NativeF55SquareOnlyCell
#print axioms KuuNativeF45Tree.DepthRotationRoute.SquareComparable.toSquareOnlyCell
#print axioms nativeF55ContextSquareRouteSetoid
#print axioms NativeF55ContextSquareRouteClasses
#print axioms nativeF55ContextSquareRouteClass
#print axioms nativeF55ContextSquareRouteClass_eq_iff
#print axioms nativeF55ContextSquareLeftClassMap
#print axioms nativeF55ContextSquareRightClassMap
#print axioms nativeF55ContextSquareLeftClassMap_spec
#print axioms nativeF55ContextSquareRightClassMap_spec
#print axioms nativeF55P67ToContextSquareClasses
#print axioms nativeF55P67ToContextSquareClasses_spec
#print axioms northHexagonNativeSquare_context_class_eq
#print axioms northNativeF55PentagonCell_not_squareOnly
#print axioms northHexagonNativeF55SquareCell_squareOnly

end
end Kuu.F112.Physical
