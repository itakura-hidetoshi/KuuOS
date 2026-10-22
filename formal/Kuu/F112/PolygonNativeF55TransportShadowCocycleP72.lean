import Kuu.F112.PolygonNativeF55HigherTransportQuotientP71
import Mathlib.Tactic.Abel

/-!
# F112-P72 — chosen-witness correction and two-step transport cocycle

P70-P71 identify a concrete obstruction: the ORIGINAL selected F55
shadow is not invariant when one identifies P69 higher arrows by
chosen square-only representative transport. The true north C60
disjoint square contributes odd phase 1 even when quotient class
source/target objects do not change.

The correct next construction is a witness-GRADED candidate:
retain the actual left/right F55 comparison proofs and subtract their
known original signed shadow contributions. This file establishes
the exact correction identity for arbitrary two-axis F54 endpoints,
bridge-corrected vertical pasting, and stepwise two-stage correction.
At the actual C60 hexagon the corrected phase of the transported
identity is zero although the uncorrected original raw phase is odd.

The corrected readout DEPENDS on the selected witnesses. These laws
are neither a canonical scalar factorization of P71's ungraded
transport quotient (ruled out for the raw shadow) nor a proof of
all pentagon/interchange coherence or a global strict 3/n category.
They supply necessary explicit transport-cocycle equations that a
graded higher-Hom construction must respect.

No Gray, new axioms, sorry, admit or historical root deletion.
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

/-- Readout of the transported raw higher arrow CORRECTED by
the chosen left and right original F55 comparison witnesses.
This is a witness-graded datum, not a function of quotient classes
alone. -/
def NativeF55HigherArrowOverClasses.correctedTransportShadow
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
    KuuNativeF55Shadow :=
  (arrow.changeRepresentatives left right).raw.nativeShadow -
    left.1.nativeShadow - right.1.nativeShadow

/-- EXACT correction for every legitimate original F55 source term.
The mathematical reason is the additive group structure of the
selected shadow and P70's proof-relevant transport pasting. -/
theorem NativeF55HigherArrowOverClasses.correctedTransportShadow_eq
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
    arrow.correctedTransportShadow left right =
      arrow.raw.nativeShadow := by
  unfold NativeF55HigherArrowOverClasses.correctedTransportShadow
  rw [NativeF55HigherArrowOverClasses.changeRepresentatives_shadow]
  abel

/-- Bridge-graded selected shadow for two original source higher
arrows, subtracting the actual middle comparison witness contribution
instead of pretending its phase always vanishes. -/
def NativeF55HigherArrowOverClasses.correctedBridgeShadow
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
    KuuNativeF55Shadow :=
  (f.composeWithBridge g bridge).raw.nativeShadow -
    bridge.1.nativeShadow

/-- Corrected witness-indexed vertical paste conserves the chosen
shadow sum of its two true input F55 source proof trees. -/
theorem NativeF55HigherArrowOverClasses.correctedBridgeShadow_eq
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
    f.correctedBridgeShadow g bridge =
      f.raw.nativeShadow + g.raw.nativeShadow := by
  unfold NativeF55HigherArrowOverClasses.correctedBridgeShadow
  rw [NativeF55HigherArrowOverClasses.composeWithBridge_shadow]
  abel

/-- TWO STAGES of chosen F54 representative change admit a coherent
shadow correction: cancel the second comparison pair and then the
first, recovering the unchanged ORIGINAL raw higher arrow value.
This is an additive cocycle identity relative to specified witnesses,
NOT a proof that the higher-arrow transport quotient inherits a
canonical 3-category. -/
theorem NativeF55HigherArrowOverClasses.correctedTransport_twice
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {source target : NativeF55ContextSquareRouteClasses first last}
    (arrow : NativeF55HigherArrowOverClasses first last source target)
    {u₁ v₁ u₂ v₂ : KuuNativeF45Tree.DepthRotationRoute p first last}
    (left₁ : NativeF55SquareOnlyCell
      (p := p) (u := u₁) (v := arrow.before))
    (right₁ : NativeF55SquareOnlyCell
      (p := p) (u := arrow.after) (v := v₁))
    (left₂ : NativeF55SquareOnlyCell (p := p) (u := u₂) (v := u₁))
    (right₂ : NativeF55SquareOnlyCell (p := p) (u := v₁) (v := v₂)) :
    ((arrow.changeRepresentatives left₁ right₁).correctedTransportShadow
      left₂ right₂) - left₁.1.nativeShadow -
        right₁.1.nativeShadow = arrow.raw.nativeShadow := by
  rw [NativeF55HigherArrowOverClasses.correctedTransportShadow_eq]
  rw [NativeF55HigherArrowOverClasses.changeRepresentatives_shadow]
  abel

/-- The actual C60 north disjoint-square transports the raw identity
to odd phase, but after subtracting THAT VERY proof-relevant square
witness phase, the corrected readout has zero phase again. This
retains the witness instead of pretending its original phase is zero. -/
theorem northHexagonNativeIdentityTransport_correctedPhase_zero :
    (northHexagonNativeIdentityTransportedHigherArrow.raw.nativeShadow -
      northHexagonNativeF55SquareCell.nativeShadow).2 =
        (0 : ZMod 2) := by
  have h :
      northHexagonNativeIdentityTransportedHigherArrow.raw.nativeShadow -
        northHexagonNativeF55SquareCell.nativeShadow =
          (0 : KuuNativeF55Shadow) := by
    change
      (0 : KuuNativeF55Shadow) +
        ((0 : KuuNativeF55Shadow) +
          northHexagonNativeF55SquareCell.nativeShadow) -
          northHexagonNativeF55SquareCell.nativeShadow = 0
    abel
  exact congrArg (fun z : KuuNativeF55Shadow => z.2) h

#print axioms NativeF55HigherArrowOverClasses.correctedTransportShadow
#print axioms NativeF55HigherArrowOverClasses.correctedTransportShadow_eq
#print axioms NativeF55HigherArrowOverClasses.correctedBridgeShadow
#print axioms NativeF55HigherArrowOverClasses.correctedBridgeShadow_eq
#print axioms NativeF55HigherArrowOverClasses.correctedTransport_twice
#print axioms northHexagonNativeIdentityTransport_correctedPhase_zero

end
end Kuu.F112.Physical
