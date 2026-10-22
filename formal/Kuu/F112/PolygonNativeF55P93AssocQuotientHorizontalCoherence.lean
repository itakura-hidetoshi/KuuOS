import Kuu.F112.PolygonNativeF55P92ExplicitAssocNaturalityPresentation
import Mathlib.Tactic

/-!
# F112-P93A — genuine P92B 3-cell congruence, horizontal associator naturality

Work solely in the distinct P92B Type-valued associator-naturality
presentation; do not modify or erase the original nine-constructor F55.
Derive a two-factor horizontal 3-cell using the actual context and route
whiskering constructors, with an exactly additive full signed F55 shadow.
Prove well-defined F54 horizontal composition and pre/post and both
F45 tree context maps on the **new** existence quotient.
Construct both total three-factor composites and show they coincide on
ALL quotient classes, by the explicitly adjoined P92B naturality witness.

Finally exhibit concrete original unit F54 histories that are identified
in this quotient but have distinct ordered context-word readouts. This
records a NONDESCENDING invariant, rather than pretending it is preserved.
The old P92A no-go, signed C60 odd phase, original roots, pinned mathlib,
and no-Gray policy remain in force.

Crucially, equality in this selected F54 route quotient is NOT a
4-cell coherence between distinct P92B 3-proof witnesses; no global
strict 3/n or hyperdescent claim follows.
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

/-- The genuinely typed P92B 3-cell horizontal pasting is derived
only from P92B's existing six closure constructors; the new
associator-naturality generator is not silently coerced to old F55. -/
def NativeF55P92AssocComparison.horizontal
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' k k' l l' : Nat}
    {p₀ p₁ p₂ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ : KuuNativeBlocks x y}
    {leftBefore : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
    {leftAfter : KuuNativeF45Tree p n' m' p₀ q₀ p₁ q₁}
    {rightBefore : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂}
    {rightAfter : KuuNativeF45Tree p k' l' p₁ q₁ p₂ q₂}
    {u u' : KuuNativeF45Tree.DepthRotationRoute p leftBefore leftAfter}
    {v v' : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter}
    (f : NativeF55P92AssocComparison p u u')
    (g : NativeF55P92AssocComparison p v v') :
    NativeF55P92AssocComparison p
      (nativeF54P90HorizontalRoute u v)
      (nativeF54P90HorizontalRoute u' v') :=
  .trans
    (.postcompose (.leftContext f rightBefore)
      (.rightContext leftAfter v))
    (.precompose (.leftContext u' rightBefore)
      (.rightContext leftAfter g))

/-- Complete F55 charge and genuine odd ZMod2 phase add under
derived P92B horizontal pasting: no zeroing of original generators. -/
theorem NativeF55P92AssocComparison.horizontal_nativeShadow
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' k k' l l' : Nat}
    {p₀ p₁ p₂ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ : KuuNativeBlocks x y}
    {leftBefore : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
    {leftAfter : KuuNativeF45Tree p n' m' p₀ q₀ p₁ q₁}
    {rightBefore : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂}
    {rightAfter : KuuNativeF45Tree p k' l' p₁ q₁ p₂ q₂}
    {u u' : KuuNativeF45Tree.DepthRotationRoute p leftBefore leftAfter}
    {v v' : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter}
    (f : NativeF55P92AssocComparison p u u')
    (g : NativeF55P92AssocComparison p v v') :
    (f.horizontal g).nativeShadow =
      f.nativeShadow + g.nativeShadow := rfl

/-- An exact original F54 route PRE-composition descends through
the new F55 witness relation, using a TRUE extended P92B F55 3-cell. -/
def nativeF55P93PrecomposeClass
    {p : Polygon} {a b : D} {x y : E}
    {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n₁ m₁ ma pa mb pb}
    {middle : KuuNativeF45Tree p n₂ m₂ ma pa mb pb}
    {last : KuuNativeF45Tree p n₃ m₃ ma pa mb pb}
    (prior : KuuNativeF45Tree.DepthRotationRoute p first middle)
    (q : NativeF55P92AssocRouteClasses middle last) :
    NativeF55P92AssocRouteClasses first last :=
  _root_.Quotient.liftOn q
    (fun route => nativeF55P92AssocRouteClass first last (.trans prior route))
    (by
      intro r s h
      rcases h with ⟨cell⟩
      exact nativeF55P92AssocRouteClass_eq_of_cell first last
        (.precompose prior cell))

/-- Actual F54 POST-composition likewise preserves original
nine-constructor F55 witness existence at typed route endpoints. -/
def nativeF55P93PostcomposeClass
    {p : Polygon} {a b : D} {x y : E}
    {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n₁ m₁ ma pa mb pb}
    {middle : KuuNativeF45Tree p n₂ m₂ ma pa mb pb}
    {last : KuuNativeF45Tree p n₃ m₃ ma pa mb pb}
    (suffix : KuuNativeF45Tree.DepthRotationRoute p middle last)
    (q : NativeF55P92AssocRouteClasses first middle) :
    NativeF55P92AssocRouteClasses first last :=
  _root_.Quotient.liftOn q
    (fun route => nativeF55P92AssocRouteClass first last (.trans route suffix))
    (by
      intro r s h
      rcases h with ⟨cell⟩
      exact nativeF55P92AssocRouteClass_eq_of_cell first last
        (.postcompose cell suffix))

/-- True left binary-tree context operation on the selected
extended P92B F55 route-object quotient. -/
def nativeF55P93LeftContextClass
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' k l : Nat}
    {ma mb mc : KuuNativeBlocks a b}
    {pa pb pc : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (later : KuuNativeF45Tree p k l mb pb mc pc)
    (q : NativeF55P92AssocRouteClasses first last) :
    NativeF55P92AssocRouteClasses
      (KuuNativeF45Tree.node first later) (KuuNativeF45Tree.node last later) :=
  _root_.Quotient.liftOn q
    (fun route => nativeF55P92AssocRouteClass _ _ (.leftContext route later))
    (by
      intro r s h
      rcases h with ⟨cell⟩
      exact nativeF55P92AssocRouteClass_eq_of_cell _ _
        (.leftContext cell later))

/-- True right binary-tree context operation retaining both
independent Nat depth indices and original F19/F28 Blocks. -/
def nativeF55P93RightContextClass
    {p : Polygon} {a b : D} {x y : E}
    {k l n n' m m' : Nat}
    {ma mb mc : KuuNativeBlocks a b}
    {pa pb pc : KuuNativeBlocks x y}
    (earlier : KuuNativeF45Tree p k l ma pa mb pb)
    {first : KuuNativeF45Tree p n m mb pb mc pc}
    {last : KuuNativeF45Tree p n' m' mb pb mc pc}
    (q : NativeF55P92AssocRouteClasses first last) :
    NativeF55P92AssocRouteClasses
      (KuuNativeF45Tree.node earlier first) (KuuNativeF45Tree.node earlier last) :=
  _root_.Quotient.liftOn q
    (fun route => nativeF55P92AssocRouteClass _ _ (.rightContext earlier route))
    (by
      intro r s h
      rcases h with ⟨cell⟩
      exact nativeF55P92AssocRouteClass_eq_of_cell _ _
        (.rightContext earlier cell))

/-- P90's ACTUAL two-factor F54 route product descends through
BOTH F55 witness congruences, using a genuinely typed F55 3-cell
on each pair of changed representatives. -/
def nativeF55P93HorizontalClass
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' k k' l l' : Nat}
    {p₀ p₁ p₂ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ : KuuNativeBlocks x y}
    {leftBefore : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
    {leftAfter : KuuNativeF45Tree p n' m' p₀ q₀ p₁ q₁}
    {rightBefore : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂}
    {rightAfter : KuuNativeF45Tree p k' l' p₁ q₁ p₂ q₂}
    (L : NativeF55P92AssocRouteClasses leftBefore leftAfter)
    (R : NativeF55P92AssocRouteClasses rightBefore rightAfter) :
    NativeF55P92AssocRouteClasses
      (KuuNativeF45Tree.node leftBefore rightBefore)
      (KuuNativeF45Tree.node leftAfter rightAfter) :=
  _root_.Quotient.liftOn₂ L R
    (fun u v =>
      nativeF55P92AssocRouteClass _ _
        (nativeF54P90HorizontalRoute u v))
    (by
      intro u v u' v' hu hv
      rcases hu with ⟨f⟩
      rcases hv with ⟨g⟩
      exact nativeF55P92AssocRouteClass_eq_of_cell _ _
        (f.horizontal g))

/-- Kernel-exact horizontal computation on ANY original F54 reps;
the quotient does not replace genuine source route histories. -/
theorem nativeF55P93HorizontalClass_spec
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
    nativeF55P93HorizontalClass
      (nativeF55P92AssocRouteClass leftBefore leftAfter u)
      (nativeF55P92AssocRouteClass rightBefore rightAfter v) =
    nativeF55P92AssocRouteClass
      (KuuNativeF45Tree.node leftBefore rightBefore)
      (KuuNativeF45Tree.node leftAfter rightAfter)
      (nativeF54P90HorizontalRoute u v) := rfl

/-- The first of two well-typed triple-horizontal maps: left
bracketing first, then the GENUINE after-associator. -/
def nativeF55P93TripleLeftClass

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
    (U : NativeF55P92AssocRouteClasses firstBefore firstAfter)
    (V : NativeF55P92AssocRouteClasses secondBefore secondAfter)
    (W : NativeF55P92AssocRouteClasses thirdBefore thirdAfter) :
    NativeF55P92AssocRouteClasses
      (KuuNativeF45Tree.node
        (KuuNativeF45Tree.node firstBefore secondBefore) thirdBefore)
      (KuuNativeF45Tree.node firstAfter
        (KuuNativeF45Tree.node secondAfter thirdAfter)) :=
  nativeF55P93PostcomposeClass
    (KuuNativeF45Tree.DepthRotationRoute.assoc firstAfter secondAfter thirdAfter)
    (nativeF55P93HorizontalClass
      (nativeF55P93HorizontalClass U V) W)

/-- The second of two well-typed triple-horizontal maps: source
F54 associator first, then right-associated true horizontal. -/
def nativeF55P93TripleRightClass

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
    (U : NativeF55P92AssocRouteClasses firstBefore firstAfter)
    (V : NativeF55P92AssocRouteClasses secondBefore secondAfter)
    (W : NativeF55P92AssocRouteClasses thirdBefore thirdAfter) :
    NativeF55P92AssocRouteClasses
      (KuuNativeF45Tree.node
        (KuuNativeF45Tree.node firstBefore secondBefore) thirdBefore)
      (KuuNativeF45Tree.node firstAfter
        (KuuNativeF45Tree.node secondAfter thirdAfter)) :=
  nativeF55P93PrecomposeClass
    (KuuNativeF45Tree.DepthRotationRoute.assoc firstBefore secondBefore thirdBefore)
    (nativeF55P93HorizontalClass U
      (nativeF55P93HorizontalClass V W))

/-- Left triple-horizontal computation is the ACTUAL original
P90B F54 route constructor, not a shadow-based equality. -/
theorem nativeF55P93TripleLeftClass_spec

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
    nativeF55P93TripleLeftClass
      (nativeF55P92AssocRouteClass firstBefore firstAfter u)
      (nativeF55P92AssocRouteClass secondBefore secondAfter v)
      (nativeF55P92AssocRouteClass thirdBefore thirdAfter w) =
    nativeF55P92AssocRouteClass
      (KuuNativeF45Tree.node
        (KuuNativeF45Tree.node firstBefore secondBefore) thirdBefore) (KuuNativeF45Tree.node firstAfter
        (KuuNativeF45Tree.node secondAfter thirdAfter))
      (nativeF54P90AssocNaturalityLeftRoute u v w) := by
  rfl

/-- Right triple-horizontal computes the genuine original P90B
right route, not a freely assumed associator naturality cell. -/
theorem nativeF55P93TripleRightClass_spec

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
    nativeF55P93TripleRightClass
      (nativeF55P92AssocRouteClass firstBefore firstAfter u)
      (nativeF55P92AssocRouteClass secondBefore secondAfter v)
      (nativeF55P92AssocRouteClass thirdBefore thirdAfter w) =
    nativeF55P92AssocRouteClass
      (KuuNativeF45Tree.node
        (KuuNativeF45Tree.node firstBefore secondBefore) thirdBefore) (KuuNativeF45Tree.node firstAfter
        (KuuNativeF45Tree.node secondAfter thirdAfter))
      (nativeF54P90AssocNaturalityRightRoute u v w) := by
  rfl


/-- Associator naturality is now well-defined for arbitrary P92B
equivalence classes, not just representatives. It is obtained
through the real NEW P92B Type-valued 3-cell constructor. The
output compares the same original mixed-bracketing F54 boundaries. -/
theorem nativeF55P93TripleClass_assocNaturality
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
    (U : NativeF55P92AssocRouteClasses firstBefore firstAfter)
    (V : NativeF55P92AssocRouteClasses secondBefore secondAfter)
    (W : NativeF55P92AssocRouteClasses thirdBefore thirdAfter) :
    nativeF55P93TripleLeftClass U V W =
      nativeF55P93TripleRightClass U V W := by
  refine _root_.Quotient.inductionOn U (fun u => ?_)
  refine _root_.Quotient.inductionOn V (fun v => ?_)
  refine _root_.Quotient.inductionOn W (fun w => ?_)
  -- Quotient induction exposes `⟦u⟧`, which is definitionally,
  -- but not syntactically, the P92B class constructor. The P91C
  -- representative equations are definitional reductions (rfl).
  change nativeF55P92AssocRouteClass _ _
      (nativeF54P90AssocNaturalityLeftRoute u v w) =
    nativeF55P92AssocRouteClass _ _
      (nativeF54P90AssocNaturalityRightRoute u v w)
  exact nativeF55P92_assocNaturality_new_class_eq u v w

/-- At true original F54 unit inputs the context-word observer
DISTINGUISHES the two associator-naturality histories, while the
NEW P92B quotient identifies them. This records concrete data loss
and does not contradict the original P92A F55 no-go. -/
theorem nativeF55P93_original_unit_contextWords_lost
    {p : Polygon} {a b : D} {x y : E}
    {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
    {p₀ p₁ p₂ p₃ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ q₃ : KuuNativeBlocks x y}
    (t₁ : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁)
    (t₂ : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂)
    (t₃ : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃) :
    (nativeF54P90AssocNaturalityLeftRoute
      (nativeF54P92UnitRoute t₁)
      (nativeF54P92UnitRoute t₂)
      (nativeF54P92UnitRoute t₃)).p92UnitContextWords ≠
    (nativeF54P90AssocNaturalityRightRoute
      (nativeF54P92UnitRoute t₁)
      (nativeF54P92UnitRoute t₂)
      (nativeF54P92UnitRoute t₃)).p92UnitContextWords ∧
    nativeF55P92AssocRouteClass
      (KuuNativeF45Tree.node (KuuNativeF45Tree.node t₁ t₂) t₃)
      (KuuNativeF45Tree.node t₁ (KuuNativeF45Tree.node t₂ t₃))
      (nativeF54P90AssocNaturalityLeftRoute
        (nativeF54P92UnitRoute t₁)
        (nativeF54P92UnitRoute t₂)
        (nativeF54P92UnitRoute t₃)) =
    nativeF55P92AssocRouteClass
      (KuuNativeF45Tree.node (KuuNativeF45Tree.node t₁ t₂) t₃)
      (KuuNativeF45Tree.node t₁ (KuuNativeF45Tree.node t₂ t₃))
      (nativeF54P90AssocNaturalityRightRoute
        (nativeF54P92UnitRoute t₁)
        (nativeF54P92UnitRoute t₂)
        (nativeF54P92UnitRoute t₃)) := by
  constructor
  · rw [nativeF55P92_unit_assoc_left_words,
      nativeF55P92_unit_assoc_right_words]
    decide
  · exact nativeF55P92_assocNaturality_new_class_eq
      (nativeF54P92UnitRoute t₁)
      (nativeF54P92UnitRoute t₂)
      (nativeF54P92UnitRoute t₃)

#print axioms NativeF55P92AssocComparison.horizontal
#print axioms NativeF55P92AssocComparison.horizontal_nativeShadow
#print axioms nativeF55P93PrecomposeClass
#print axioms nativeF55P93PostcomposeClass
#print axioms nativeF55P93LeftContextClass
#print axioms nativeF55P93RightContextClass
#print axioms nativeF55P93HorizontalClass
#print axioms nativeF55P93HorizontalClass_spec
#print axioms nativeF55P93TripleLeftClass
#print axioms nativeF55P93TripleRightClass
#print axioms nativeF55P93TripleLeftClass_spec
#print axioms nativeF55P93TripleRightClass_spec
#print axioms nativeF55P93TripleClass_assocNaturality
#print axioms nativeF55P93_original_unit_contextWords_lost

end
end Kuu.F112.Physical
