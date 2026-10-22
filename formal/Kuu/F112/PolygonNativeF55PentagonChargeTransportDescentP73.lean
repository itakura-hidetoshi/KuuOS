import Kuu.F112.PolygonNativeF55TransportShadowCocycleP72

/-!
# F112-P73 — maximal verified surviving pentagon coordinate

P70-P72 show that the chosen full F55 numerical shadow is NOT
invariant when an original proof-relevant higher arrow is transported
over the F54 context-square comparison classes. In particular, the
physical C60 disjoint square changes its exchange charge and parity.

We now distinguish the TWO independent integer coordinates:
a square-only raw comparison is built from identity, disjoint-square,
and the six structural closure constructors; it contains no original
pentagon primitive, so its original first (pentagon) charge is ZERO.

We prove this on all NINE source constructors, including arbitrary
vertical composition, left and right context and F54 pre/postcompose.
As a consequence:
* pentagon charge is strictly invariant under BOTH chosen
  representative changes of a P69 higher arrow;
* it is additive for witness-bridged P70 vertical composition;
* it is preserved by EVERY constructor of P71's transport relation;
* it therefore defines a genuine function on P71's UNGRADED
  transport quotient, unlike the original full shadow.

This positive partial descent does not turn the P71 higher-arrow
classes into a global strict 3-category. It does not imply that
square charge/parity descend, and no source histories are equated
merely because their chosen observer values agree.

No Gray, new axioms, sorry or admit. Original C60 square and all
historical roots remain in the unified formal package.
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

/-- Any ORIGINAL proof term in the P68 square-only language carries
zero signed pentagon charge, proved by recursion on ALL NINE genuine
F55 constructors. This is NOT the zero selected-shadow criterion:
an actual square can still have square charge one and odd parity. -/
theorem KuuNativeF45Tree.DepthRotationRoute.PresentedCell.squareOnly_pentagon_zero
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
    (cell : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v)
    (h : cell.squareOnly = true) :
    cell.nativeShadow.1.1 = (0 : Int) := by
  induction cell with
  | ident _ => rfl
  | pentagon _ _ _ _ => cases h
  | disjointSquare _ _ => rfl
  | symm c ih =>
      change -c.nativeShadow.1.1 = (0 : Int)
      rw [ih h]
      rfl
  | trans c d ihc ihd =>
      have hc : c.squareOnly = true := Bool.and_elim_left h
      have hd : d.squareOnly = true := Bool.and_elim_right h
      change c.nativeShadow.1.1 + d.nativeShadow.1.1 = (0 : Int)
      rw [ihc hc, ihd hd]
      rfl
  | leftContext c later ih => exact ih h
  | rightContext earlier c ih => exact ih h
  | precompose prior c ih => exact ih h
  | postcompose c suffix ih => exact ih h

/-- The Type-valued P68 comparison witness carries its own precise
certificate of zero pentagon charge; no proof can be recovered from
a mere quotient-class equality unless a witness is actually chosen. -/
theorem NativeF55SquareOnlyCell.pentagon_zero
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {u v : KuuNativeF45Tree.DepthRotationRoute p first last}
    (cell : NativeF55SquareOnlyCell (p := p) (u := u) (v := v)) :
    cell.1.nativeShadow.1.1 = (0 : Int) :=
  cell.1.squareOnly_pentagon_zero cell.2

/-- Both explicitly selected representative-transport witnesses
have zero pentagon charge, so arbitrary ORIGINAL F55 pentagon
charge survives the proof-relevant P70 transport unchanged. -/
theorem NativeF55HigherArrowOverClasses.changeRepresentatives_pentagon
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
    (arrow.changeRepresentatives left right).raw.nativeShadow.1.1 =
      arrow.raw.nativeShadow.1.1 := by
  rw [NativeF55HigherArrowOverClasses.changeRepresentatives_shadow]
  change left.1.nativeShadow.1.1 +
    (arrow.raw.nativeShadow.1.1 + right.1.nativeShadow.1.1) =
      arrow.raw.nativeShadow.1.1
  rw [left.pentagon_zero, right.pentagon_zero]
  simp

/-- The P70 witness-indexed bridge composition preserves the sum
of the original signed pentagon charges independently of which
genuine square-only middle comparison was explicitly selected. -/
theorem NativeF55HigherArrowOverClasses.composeWithBridge_pentagon
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
    (f.composeWithBridge g bridge).raw.nativeShadow.1.1 =
      f.raw.nativeShadow.1.1 + g.raw.nativeShadow.1.1 := by
  rw [NativeF55HigherArrowOverClasses.composeWithBridge_shadow]
  change f.raw.nativeShadow.1.1 +
    (bridge.1.nativeShadow.1.1 + g.raw.nativeShadow.1.1) =
      f.raw.nativeShadow.1.1 + g.raw.nativeShadow.1.1
  rw [bridge.pentagon_zero]
  simp

/-- Pentagon charge is invariant under the WHOLE P71 transport
relation, not just under an example or the primitive generating
transport. This induction checks all four relation constructors. -/
theorem NativeF55HigherTransportRel.pentagon_eq
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {source target : NativeF55ContextSquareRouteClasses first last}
    {f g : NativeF55HigherArrowOverClasses first last source target}
    (h : NativeF55HigherTransportRel first last source target f g) :
    f.raw.nativeShadow.1.1 = g.raw.nativeShadow.1.1 := by
  induction h with
  | refl arrow => rfl
  | symm h ih => exact ih.symm
  | trans hfg hgh ihfg ihgh => exact ihfg.trans ihgh
  | change arrow left right =>
      exact (arrow.changeRepresentatives_pentagon left right).symm

/-- Unlike the full selected numerical F55 shadow, the original
signed PENTAGON integer coordinate is a genuine well-defined
readout of the chosen P71 transport quotient of higher arrows. -/
def nativeF55HigherTransportPentagonCharge
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (source target : NativeF55ContextSquareRouteClasses first last) :
    NativeF55HigherTransportClasses first last source target → Int :=
  _root_.Quotient.lift
    (fun arrow : NativeF55HigherArrowOverClasses first last source target =>
      arrow.raw.nativeShadow.1.1)
    (by
      intro f g h
      exact NativeF55HigherTransportRel.pentagon_eq h)

/-- Pentagon-charge descent commutes strictly with the quotient
projection, on EVERY true source raw higher-arrow presentation. -/
theorem nativeF55HigherTransportPentagonCharge_spec
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (source target : NativeF55ContextSquareRouteClasses first last)
    (arrow : NativeF55HigherArrowOverClasses first last source target) :
    nativeF55HigherTransportPentagonCharge first last source target
      (nativeF55HigherTransportClass first last source target arrow) =
        arrow.raw.nativeShadow.1.1 := rfl

/-- The actual north C60 odd square is an EXPLICIT witness that the
first integer charge survives even though the independent odd
exchange parity does not. -/
theorem northHexagonNativeTransport_pentagon_zero :
    northHexagonNativeIdentityTransportedHigherArrow.raw.nativeShadow.1.1 =
      (0 : Int) := by
  calc
    northHexagonNativeIdentityTransportedHigherArrow.raw.nativeShadow.1.1 =
        northHexagonNativeIdentityHigherArrowOverClasses.raw.nativeShadow.1.1 :=
      (NativeF55HigherTransportRel.pentagon_eq
        northHexagonNativeIdentityTransport_related).symm
    _ = 0 := rfl

/-- An explicit related pair with different ORIGINAL phases rules
out any bare scalar phase function on its P71 transport quotient
that would equal the raw source parity for ALL representatives. -/
theorem nativeF55HigherTransport_no_phase_factor_of_related
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (source target : NativeF55ContextSquareRouteClasses first last)
    (f g : NativeF55HigherArrowOverClasses first last source target)
    (h : NativeF55HigherTransportRel first last source target f g)
    (hne : f.raw.nativeShadow.2 ≠ g.raw.nativeShadow.2) :
    ¬ ∃ readout : NativeF55HigherTransportClasses first last source target →
          ZMod 2,
        ∀ arrow : NativeF55HigherArrowOverClasses first last source target,
          readout (nativeF55HigherTransportClass first last source target arrow) =
            arrow.raw.nativeShadow.2 := by
  rintro ⟨readout, hreadout⟩
  have hclass :=
    (nativeF55HigherTransportClass_eq_iff first last source target f g).2 h
  apply hne
  calc
    f.raw.nativeShadow.2 =
        readout (nativeF55HigherTransportClass first last source target f) :=
      (hreadout f).symm
    _ = readout (nativeF55HigherTransportClass first last source target g) :=
      congrArg readout hclass
    _ = g.raw.nativeShadow.2 := hreadout g

#print axioms KuuNativeF45Tree.DepthRotationRoute.PresentedCell.squareOnly_pentagon_zero
#print axioms NativeF55SquareOnlyCell.pentagon_zero
#print axioms NativeF55HigherArrowOverClasses.changeRepresentatives_pentagon
#print axioms NativeF55HigherArrowOverClasses.composeWithBridge_pentagon
#print axioms NativeF55HigherTransportRel.pentagon_eq
#print axioms nativeF55HigherTransportPentagonCharge
#print axioms nativeF55HigherTransportPentagonCharge_spec
#print axioms northHexagonNativeTransport_pentagon_zero
#print axioms nativeF55HigherTransport_no_phase_factor_of_related

end
end Kuu.F112.Physical
