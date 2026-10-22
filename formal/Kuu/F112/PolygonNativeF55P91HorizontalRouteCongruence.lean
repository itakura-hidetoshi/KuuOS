import Kuu.F112.PolygonNativeF55P91FullWitnessRouteQuotient

/-!
# F112-P91C — original F55-witness congruence for real F54 horizontal operations

P91B supplies a distinct, EXACT original-F55-existence quotient
of genuine Type-valued original F54 depth-rotation routes.

We prove this particular original-witness congruence is actually
closed under FOUR independently typed operations used in real F55:
  - F54 route precomposition and postcomposition;
  - genuine left and right F45 tree contexts;
  - true two-factor F54 horizontal pasting as defined in P90B.

No numerical shadow or choice of quotient representative creates
a comparison. For each congruence claim we construct a real
original F55 PresentedCell using its NINE native constructors.
The horizontal case uses original .horizontal, itself derived from
contexts/pre/post in the original F55 raw source.

This yields two total, representative-independent triple-horizontal
routes (horizontal before vs after F54 reassociation) on P91B
classes. On actual representatives their comparison is EQUIVALENT
to the genuinely still-unfilled P90 source F55 Type-valued slot.
We neither equate the two maps nor postulate the missing filler.

Thus full-witness route congruence descends horizontal composition,
but horizontal associativity/naturality across distinct F54 trees
still requires additional genuine evidence. Original P87/P88 no-go,
P89 strict interchange, full C60 odd phase, 107 roots, no Gray.
No sorry/admit/new axioms.
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

/-- An exact original F54 route PRE-composition descends through
the new F55 witness relation, using a TRUE original F55 3-cell. -/
def nativeF55P91PrecomposeClass
    {p : Polygon} {a b : D} {x y : E}
    {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n₁ m₁ ma pa mb pb}
    {middle : KuuNativeF45Tree p n₂ m₂ ma pa mb pb}
    {last : KuuNativeF45Tree p n₃ m₃ ma pa mb pb}
    (prior : KuuNativeF45Tree.DepthRotationRoute p first middle)
    (q : NativeF55P91FullWitnessRouteClasses middle last) :
    NativeF55P91FullWitnessRouteClasses first last :=
  _root_.Quotient.liftOn q
    (fun route => nativeF55P91FullWitnessRouteClass first last (.trans prior route))
    (by
      intro r s h
      rcases h with ⟨cell⟩
      exact nativeF55P91FullWitnessRouteClass_eq_of_cell first last
        (.precompose prior cell))

/-- Actual F54 POST-composition likewise preserves original
nine-constructor F55 witness existence at typed route endpoints. -/
def nativeF55P91PostcomposeClass
    {p : Polygon} {a b : D} {x y : E}
    {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n₁ m₁ ma pa mb pb}
    {middle : KuuNativeF45Tree p n₂ m₂ ma pa mb pb}
    {last : KuuNativeF45Tree p n₃ m₃ ma pa mb pb}
    (suffix : KuuNativeF45Tree.DepthRotationRoute p middle last)
    (q : NativeF55P91FullWitnessRouteClasses first middle) :
    NativeF55P91FullWitnessRouteClasses first last :=
  _root_.Quotient.liftOn q
    (fun route => nativeF55P91FullWitnessRouteClass first last (.trans route suffix))
    (by
      intro r s h
      rcases h with ⟨cell⟩
      exact nativeF55P91FullWitnessRouteClass_eq_of_cell first last
        (.postcompose cell suffix))

/-- True left binary-tree context operation on the selected
original F55 route-object quotient. -/
def nativeF55P91LeftContextClass
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' k l : Nat}
    {ma mb mc : KuuNativeBlocks a b}
    {pa pb pc : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (later : KuuNativeF45Tree p k l mb pb mc pc)
    (q : NativeF55P91FullWitnessRouteClasses first last) :
    NativeF55P91FullWitnessRouteClasses
      (KuuNativeF45Tree.node first later) (KuuNativeF45Tree.node last later) :=
  _root_.Quotient.liftOn q
    (fun route => nativeF55P91FullWitnessRouteClass _ _ (.leftContext route later))
    (by
      intro r s h
      rcases h with ⟨cell⟩
      exact nativeF55P91FullWitnessRouteClass_eq_of_cell _ _
        (.leftContext cell later))

/-- True right binary-tree context operation retaining both
independent Nat depth indices and original F19/F28 Blocks. -/
def nativeF55P91RightContextClass
    {p : Polygon} {a b : D} {x y : E}
    {k l n n' m m' : Nat}
    {ma mb mc : KuuNativeBlocks a b}
    {pa pb pc : KuuNativeBlocks x y}
    (earlier : KuuNativeF45Tree p k l ma pa mb pb)
    {first : KuuNativeF45Tree p n m mb pb mc pc}
    {last : KuuNativeF45Tree p n' m' mb pb mc pc}
    (q : NativeF55P91FullWitnessRouteClasses first last) :
    NativeF55P91FullWitnessRouteClasses
      (KuuNativeF45Tree.node earlier first) (KuuNativeF45Tree.node earlier last) :=
  _root_.Quotient.liftOn q
    (fun route => nativeF55P91FullWitnessRouteClass _ _ (.rightContext earlier route))
    (by
      intro r s h
      rcases h with ⟨cell⟩
      exact nativeF55P91FullWitnessRouteClass_eq_of_cell _ _
        (.rightContext earlier cell))

/-- P90's ACTUAL two-factor F54 route product descends through
BOTH F55 witness congruences, using a genuinely typed F55 3-cell
on each pair of changed representatives. -/
def nativeF55P91HorizontalClass
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' k k' l l' : Nat}
    {p₀ p₁ p₂ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ : KuuNativeBlocks x y}
    {leftBefore : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
    {leftAfter : KuuNativeF45Tree p n' m' p₀ q₀ p₁ q₁}
    {rightBefore : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂}
    {rightAfter : KuuNativeF45Tree p k' l' p₁ q₁ p₂ q₂}
    (L : NativeF55P91FullWitnessRouteClasses leftBefore leftAfter)
    (R : NativeF55P91FullWitnessRouteClasses rightBefore rightAfter) :
    NativeF55P91FullWitnessRouteClasses
      (KuuNativeF45Tree.node leftBefore rightBefore)
      (KuuNativeF45Tree.node leftAfter rightAfter) :=
  _root_.Quotient.liftOn₂ L R
    (fun u v =>
      nativeF55P91FullWitnessRouteClass _ _
        (nativeF54P90HorizontalRoute u v))
    (by
      intro u v u' v' hu hv
      rcases hu with ⟨f⟩
      rcases hv with ⟨g⟩
      exact nativeF55P91FullWitnessRouteClass_eq_of_cell _ _
        (f.horizontal g))

/-- Kernel-exact horizontal computation on ANY original F54 reps;
the quotient does not replace original source route histories. -/
theorem nativeF55P91HorizontalClass_spec
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' k k' l l' : Nat}
    {p₀ p₁ p₂ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ : KuuNativeBlocks x y}
    {leftBefore : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
    {leftAfter : KuuNativeF45Tree p n' m' p₀ q₀ p₁ q₁}
    {rightBefore : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂}
    {rightAfter : KuuNativeF45Tree p k' l' p₁ q₁ p₂ q₂}
    (u : KuuNativeF45Tree.DepthRotationRoute p leftBefore leftAfter)
    (v : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter) :
    nativeF55P91HorizontalClass
      (nativeF55P91FullWitnessRouteClass leftBefore leftAfter u)
      (nativeF55P91FullWitnessRouteClass rightBefore rightAfter v) =
    nativeF55P91FullWitnessRouteClass
      (KuuNativeF45Tree.node leftBefore rightBefore)
      (KuuNativeF45Tree.node leftAfter rightAfter)
      (nativeF54P90HorizontalRoute u v) := rfl

/-- The first of two well-typed triple-horizontal maps: left
bracketing first, then the GENUINE after-associator. -/
def nativeF55P91TripleLeftClass

    {p : Polygon} {a b : D} {x y : E}
    {n₁ n₁' n₂ n₂' n₃ n₃' m₁ m₁' m₂ m₂' m₃ m₃' : Nat}
    {p₀ p₁ p₂ p₃ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ q₃ : KuuNativeBlocks x y}
    {firstBefore : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁}
    {firstAfter : KuuNativeF45Tree p n₁' m₁' p₀ q₀ p₁ q₁}
    {secondBefore : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂}
    {secondAfter : KuuNativeF45Tree p n₂' m₂' p₁ q₁ p₂ q₂}
    {thirdBefore : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃}
    {thirdAfter : KuuNativeF45Tree p n₃' m₃' p₂ q₂ p₃ q₃}
    (U : NativeF55P91FullWitnessRouteClasses firstBefore firstAfter)
    (V : NativeF55P91FullWitnessRouteClasses secondBefore secondAfter)
    (W : NativeF55P91FullWitnessRouteClasses thirdBefore thirdAfter) :
    NativeF55P91FullWitnessRouteClasses
      (KuuNativeF45Tree.node
        (KuuNativeF45Tree.node firstBefore secondBefore) thirdBefore)
      (KuuNativeF45Tree.node firstAfter
        (KuuNativeF45Tree.node secondAfter thirdAfter)) :=
  nativeF55P91PostcomposeClass
    (KuuNativeF45Tree.DepthRotationRoute.assoc firstAfter secondAfter thirdAfter)
    (nativeF55P91HorizontalClass
      (nativeF55P91HorizontalClass U V) W)

/-- The second of two well-typed triple-horizontal maps: source
F54 associator first, then right-associated true horizontal. -/
def nativeF55P91TripleRightClass

    {p : Polygon} {a b : D} {x y : E}
    {n₁ n₁' n₂ n₂' n₃ n₃' m₁ m₁' m₂ m₂' m₃ m₃' : Nat}
    {p₀ p₁ p₂ p₃ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ q₃ : KuuNativeBlocks x y}
    {firstBefore : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁}
    {firstAfter : KuuNativeF45Tree p n₁' m₁' p₀ q₀ p₁ q₁}
    {secondBefore : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂}
    {secondAfter : KuuNativeF45Tree p n₂' m₂' p₁ q₁ p₂ q₂}
    {thirdBefore : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃}
    {thirdAfter : KuuNativeF45Tree p n₃' m₃' p₂ q₂ p₃ q₃}
    (U : NativeF55P91FullWitnessRouteClasses firstBefore firstAfter)
    (V : NativeF55P91FullWitnessRouteClasses secondBefore secondAfter)
    (W : NativeF55P91FullWitnessRouteClasses thirdBefore thirdAfter) :
    NativeF55P91FullWitnessRouteClasses
      (KuuNativeF45Tree.node
        (KuuNativeF45Tree.node firstBefore secondBefore) thirdBefore)
      (KuuNativeF45Tree.node firstAfter
        (KuuNativeF45Tree.node secondAfter thirdAfter)) :=
  nativeF55P91PrecomposeClass
    (KuuNativeF45Tree.DepthRotationRoute.assoc firstBefore secondBefore thirdBefore)
    (nativeF55P91HorizontalClass U
      (nativeF55P91HorizontalClass V W))

/-- Left triple-horizontal computation is the ACTUAL original
P90B F54 route constructor, not a shadow-based equality. -/
theorem nativeF55P91TripleLeftClass_spec

    {p : Polygon} {a b : D} {x y : E}
    {n₁ n₁' n₂ n₂' n₃ n₃' m₁ m₁' m₂ m₂' m₃ m₃' : Nat}
    {p₀ p₁ p₂ p₃ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ q₃ : KuuNativeBlocks x y}
    {firstBefore : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁}
    {firstAfter : KuuNativeF45Tree p n₁' m₁' p₀ q₀ p₁ q₁}
    {secondBefore : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂}
    {secondAfter : KuuNativeF45Tree p n₂' m₂' p₁ q₁ p₂ q₂}
    {thirdBefore : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃}
    {thirdAfter : KuuNativeF45Tree p n₃' m₃' p₂ q₂ p₃ q₃}
    (u : KuuNativeF45Tree.DepthRotationRoute p firstBefore firstAfter)
    (v : KuuNativeF45Tree.DepthRotationRoute p secondBefore secondAfter)
    (w : KuuNativeF45Tree.DepthRotationRoute p thirdBefore thirdAfter) :
    nativeF55P91TripleLeftClass
      (nativeF55P91FullWitnessRouteClass firstBefore firstAfter u)
      (nativeF55P91FullWitnessRouteClass secondBefore secondAfter v)
      (nativeF55P91FullWitnessRouteClass thirdBefore thirdAfter w) =
    nativeF55P91FullWitnessRouteClass
      (KuuNativeF45Tree.node
        (KuuNativeF45Tree.node firstBefore secondBefore) thirdBefore) (KuuNativeF45Tree.node firstAfter
        (KuuNativeF45Tree.node secondAfter thirdAfter))
      (nativeF54P90AssocNaturalityLeftRoute u v w) := by
  rfl

/-- Right triple-horizontal computes the genuine original P90B
right route, not a freely assumed associator naturality cell. -/
theorem nativeF55P91TripleRightClass_spec

    {p : Polygon} {a b : D} {x y : E}
    {n₁ n₁' n₂ n₂' n₃ n₃' m₁ m₁' m₂ m₂' m₃ m₃' : Nat}
    {p₀ p₁ p₂ p₃ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ q₃ : KuuNativeBlocks x y}
    {firstBefore : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁}
    {firstAfter : KuuNativeF45Tree p n₁' m₁' p₀ q₀ p₁ q₁}
    {secondBefore : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂}
    {secondAfter : KuuNativeF45Tree p n₂' m₂' p₁ q₁ p₂ q₂}
    {thirdBefore : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃}
    {thirdAfter : KuuNativeF45Tree p n₃' m₃' p₂ q₂ p₃ q₃}
    (u : KuuNativeF45Tree.DepthRotationRoute p firstBefore firstAfter)
    (v : KuuNativeF45Tree.DepthRotationRoute p secondBefore secondAfter)
    (w : KuuNativeF45Tree.DepthRotationRoute p thirdBefore thirdAfter) :
    nativeF55P91TripleRightClass
      (nativeF55P91FullWitnessRouteClass firstBefore firstAfter u)
      (nativeF55P91FullWitnessRouteClass secondBefore secondAfter v)
      (nativeF55P91FullWitnessRouteClass thirdBefore thirdAfter w) =
    nativeF55P91FullWitnessRouteClass
      (KuuNativeF45Tree.node
        (KuuNativeF45Tree.node firstBefore secondBefore) thirdBefore) (KuuNativeF45Tree.node firstAfter
        (KuuNativeF45Tree.node secondAfter thirdAfter))
      (nativeF54P90AssocNaturalityRightRoute u v w) := by
  rfl

/-- Exact obstruction to claiming that the two new TOTAL
triple-horizontal maps agree. Equality at arbitrary original
representatives holds IFF a real original F55 associator naturality
witness exists in the still-unfilled P90 Type slot. -/
theorem nativeF55P91TripleClass_eq_iff_original_filler

    {p : Polygon} {a b : D} {x y : E}
    {n₁ n₁' n₂ n₂' n₃ n₃' m₁ m₁' m₂ m₂' m₃ m₃' : Nat}
    {p₀ p₁ p₂ p₃ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ q₃ : KuuNativeBlocks x y}
    {firstBefore : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁}
    {firstAfter : KuuNativeF45Tree p n₁' m₁' p₀ q₀ p₁ q₁}
    {secondBefore : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂}
    {secondAfter : KuuNativeF45Tree p n₂' m₂' p₁ q₁ p₂ q₂}
    {thirdBefore : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃}
    {thirdAfter : KuuNativeF45Tree p n₃' m₃' p₂ q₂ p₃ q₃}
    (u : KuuNativeF45Tree.DepthRotationRoute p firstBefore firstAfter)
    (v : KuuNativeF45Tree.DepthRotationRoute p secondBefore secondAfter)
    (w : KuuNativeF45Tree.DepthRotationRoute p thirdBefore thirdAfter) :
    nativeF55P91TripleLeftClass
      (nativeF55P91FullWitnessRouteClass firstBefore firstAfter u)
      (nativeF55P91FullWitnessRouteClass secondBefore secondAfter v)
      (nativeF55P91FullWitnessRouteClass thirdBefore thirdAfter w) =
    nativeF55P91TripleRightClass
      (nativeF55P91FullWitnessRouteClass firstBefore firstAfter u)
      (nativeF55P91FullWitnessRouteClass secondBefore secondAfter v)
      (nativeF55P91FullWitnessRouteClass thirdBefore thirdAfter w) ↔
      Nonempty (NativeF55P90AssocNaturalityCell u v w) := by
  rw [nativeF55P91TripleLeftClass_spec,
    nativeF55P91TripleRightClass_spec]
  exact nativeF55P91AssocNaturalityFullWitnessClass_eq_iff u v w

#print axioms nativeF55P91PrecomposeClass
#print axioms nativeF55P91PostcomposeClass
#print axioms nativeF55P91LeftContextClass
#print axioms nativeF55P91RightContextClass
#print axioms nativeF55P91HorizontalClass
#print axioms nativeF55P91HorizontalClass_spec
#print axioms nativeF55P91TripleLeftClass
#print axioms nativeF55P91TripleRightClass
#print axioms nativeF55P91TripleLeftClass_spec
#print axioms nativeF55P91TripleRightClass_spec
#print axioms nativeF55P91TripleClass_eq_iff_original_filler

end
end Kuu.F112.Physical
