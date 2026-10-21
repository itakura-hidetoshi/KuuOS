import Kuu.F112.PolygonNativeF55HigherHomTransportBoundaryP69

/-!
F112-P70: explicit Type-valued representative-change higher-arrow witnesses.

P69 packages genuine raw F55 cells over the context-closed P68 F54
quotient classes. An object-class equality is only an existence
statement; it does NOT canonically select F55 transport or define
an associative quotient higher-Hom composition.

With actual source F55 square-only comparison witnesses in hand,
this file constructs:
* transport of a P69 higher arrow to new F54 representatives;
* witness-indexed vertical composition over a common middle class;
* exact original raw-history and chosen shadow contribution formulas;
* a REAL six-sector C60 counterexample to numerical-shadow
  invariance under representative change: the initial identity
  has zero odd exchange phase, and an explicit representative
  change along the genuine square has nonzero phase, while both
  P69 packages have the SAME quotient source and target classes.

No equality of raw source terms follows from equality of numerical
shadows. This does not establish a total quotient 3-Hom or global
strict interchange; it isolates the coherence obstruction.
No Gray, sorry, admit, or added axioms.
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

/-- Given explicit original source left and right square-only F55
comparisons, move the representatives of the SAME quotient-class
higher arrow by genuine vertically pasted Type-valued source terms. -/
def NativeF55HigherArrowOverClasses.changeRepresentatives
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {source target : NativeF55ContextSquareRouteClasses first last}
    (arrow : NativeF55HigherArrowOverClasses first last source target)
    {newBefore newAfter : KuuNativeF45Tree.DepthRotationRoute p first last}
    (left : NativeF55SquareOnlyCell
      (p := p) (u := newBefore) (v := arrow.before))
    (right : NativeF55SquareOnlyCell
      (p := p) (u := arrow.after) (v := newAfter)) :
    NativeF55HigherArrowOverClasses first last source target where
  before := newBefore
  after := newAfter
  source_eq :=
    ((nativeF55ContextSquareRouteClass_eq_iff
      first last newBefore arrow.before).2 ⟨left⟩).trans arrow.source_eq
  target_eq :=
    ((nativeF55ContextSquareRouteClass_eq_iff
      first last arrow.after newAfter).2 ⟨right⟩).symm.trans arrow.target_eq
  raw := .trans left.1 (.trans arrow.raw right.1)

/-- The raw history is exactly the three original proof-relevant
pieces; it is not erased or replaced by an equality of phases. -/
theorem NativeF55HigherArrowOverClasses.changeRepresentatives_raw
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {source target : NativeF55ContextSquareRouteClasses first last}
    (arrow : NativeF55HigherArrowOverClasses first last source target)
    {newBefore newAfter : KuuNativeF45Tree.DepthRotationRoute p first last}
    (left : NativeF55SquareOnlyCell
      (p := p) (u := newBefore) (v := arrow.before))
    (right : NativeF55SquareOnlyCell
      (p := p) (u := arrow.after) (v := newAfter)) :
    (arrow.changeRepresentatives left right).raw =
      .trans left.1 (.trans arrow.raw right.1) := rfl

/-- The chosen numerical observation has an explicitly
comparison-witness-dependent additive correction. -/
theorem NativeF55HigherArrowOverClasses.changeRepresentatives_shadow
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {source target : NativeF55ContextSquareRouteClasses first last}
    (arrow : NativeF55HigherArrowOverClasses first last source target)
    {newBefore newAfter : KuuNativeF45Tree.DepthRotationRoute p first last}
    (left : NativeF55SquareOnlyCell
      (p := p) (u := newBefore) (v := arrow.before))
    (right : NativeF55SquareOnlyCell
      (p := p) (u := arrow.after) (v := newAfter)) :
    (arrow.changeRepresentatives left right).raw.nativeShadow =
      left.1.nativeShadow +
        (arrow.raw.nativeShadow + right.1.nativeShadow) := rfl

/-- Two P69 higher arrows compose after selecting an ACTUAL typed
original square-only F55 bridge between their middle representatives.
There is deliberately no claimed witness-independent composition. -/
def NativeF55HigherArrowOverClasses.composeWithBridge
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {source middle target : NativeF55ContextSquareRouteClasses first last}
    (f : NativeF55HigherArrowOverClasses first last source middle)
    (g : NativeF55HigherArrowOverClasses first last middle target)
    (bridge : NativeF55SquareOnlyCell
      (p := p) (u := f.after) (v := g.before)) :
    NativeF55HigherArrowOverClasses first last source target where
  before := f.before
  after := g.after
  source_eq := f.source_eq
  target_eq := g.target_eq
  raw := .trans f.raw (.trans bridge.1 g.raw)

/-- Explicit chosen-bridge vertical composition is reflected by
the sum of all three original selected shadow values. -/
theorem NativeF55HigherArrowOverClasses.composeWithBridge_shadow
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {source middle target : NativeF55ContextSquareRouteClasses first last}
    (f : NativeF55HigherArrowOverClasses first last source middle)
    (g : NativeF55HigherArrowOverClasses first last middle target)
    (bridge : NativeF55SquareOnlyCell
      (p := p) (u := f.after) (v := g.before)) :
    (f.composeWithBridge g bridge).raw.nativeShadow =
      f.raw.nativeShadow +
        (bridge.1.nativeShadow + g.raw.nativeShadow) := rfl

/-- Original north C60 square-left raw identity packaged over its
single P68 quotient route class. -/
def northHexagonNativeIdentityHigherArrowOverClasses :=
  nativeF55HigherArrowOverClasses_ofRaw _ _
    (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident
      northHexagonNativeSquareLeft)

/-- Transport the identity along the actual north C60 odd
exchange square, but keep EXACTLY the same quotient class endpoints. -/
def northHexagonNativeIdentityTransportedHigherArrow :=
  northHexagonNativeIdentityHigherArrowOverClasses.changeRepresentatives
    (newBefore := northHexagonNativeSquareLeft)
    (newAfter := northHexagonNativeSquareRight)
    (⟨KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident
      northHexagonNativeSquareLeft, rfl⟩)
    (⟨northHexagonNativeF55SquareCell, rfl⟩)

theorem northHexagonNativeIdentityHigherArrow_phase_zero :
    northHexagonNativeIdentityHigherArrowOverClasses.raw.nativeShadow.2 =
      (0 : ZMod 2) := rfl

/-- The transported physical square has odd phase, although the
source and target quotient objects did not change. -/
theorem northHexagonNativeIdentityTransportedHigherArrow_phase_nonzero :
    northHexagonNativeIdentityTransportedHigherArrow.raw.nativeShadow.2 ≠
      (0 : ZMod 2) := by
  change
    ((0 : KuuNativeF55Shadow) +
      ((0 : KuuNativeF55Shadow) +
        northHexagonNativeF55SquareCell.nativeShadow)).2 ≠
      (0 : ZMod 2)
  simpa only [zero_add] using
    northHexagonNativeF55SquareCell_phase_nonzero

/-- Selected full raw shadow is not invariant under this explicitly
witnessed representative change, even at FIXED quotient endpoints.
This identifies a necessary coherence and information-boundary
obligation, not impossibility of constructing richer 3-Hom data. -/
theorem northHexagonNativeIdentityTransport_changes_chosen_shadow :
    northHexagonNativeIdentityHigherArrowOverClasses.raw.nativeShadow ≠
      northHexagonNativeIdentityTransportedHigherArrow.raw.nativeShadow := by
  intro h
  have hp := congrArg (fun z : KuuNativeF55Shadow => z.2) h
  have hid := northHexagonNativeIdentityHigherArrow_phase_zero
  rw [hid] at hp
  exact northHexagonNativeIdentityTransportedHigherArrow_phase_nonzero hp.symm

#print axioms NativeF55HigherArrowOverClasses.changeRepresentatives
#print axioms NativeF55HigherArrowOverClasses.changeRepresentatives_raw
#print axioms NativeF55HigherArrowOverClasses.changeRepresentatives_shadow
#print axioms NativeF55HigherArrowOverClasses.composeWithBridge
#print axioms NativeF55HigherArrowOverClasses.composeWithBridge_shadow
#print axioms northHexagonNativeIdentityHigherArrowOverClasses
#print axioms northHexagonNativeIdentityTransportedHigherArrow
#print axioms northHexagonNativeIdentityHigherArrow_phase_zero
#print axioms northHexagonNativeIdentityTransportedHigherArrow_phase_nonzero
#print axioms northHexagonNativeIdentityTransport_changes_chosen_shadow

end
end Kuu.F112.Physical
