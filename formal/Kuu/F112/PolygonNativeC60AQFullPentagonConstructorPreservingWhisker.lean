import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalWhiskerNoninjectivity

/-!
# F112-P94D3FK — independent, constructor-preserving Type-valued AQ whiskering

FJ exhibits a genuine physical 15D raw-proof collision in the EXISTING
nativeK5AQWhiskerCell: the entire conservative core is mapped to a
single observer-compatible atom, identifying original conservative
refl and atom proofs. That is a fact about a selected relative
presentation, not an unproved no-go for every possible presentation.

FK constructs a SEPARATE, explicit Type-valued proof transport on
the SAME original physical K5 AQ source and target fourteen-cell
boundaries. Its conservative branch genuinely RECURSES through the
original core refl/atom/symm/trans constructors, rather than
replacing every core proof by an atom. Exchange generators retain
the actual (side :: steps) context index; the outer symm/trans
syntax is also recursively preserved.

We then:
* Prove the genuine original 14D left/right raw whiskerings are
  injective on their actual fixed-boundary proof fiber;
* Show the FJ pair of distinct raw 15D witnesses stays distinct
  under this NEW selected proof transport;
* Show no postprocessing of the OLD whiskering output alone can
  reconstruct the NEW result for every original proof in that fiber;
* Construct the actual alternative boundary-preserving 15D AX frame
  without modifying any existing object, signature or theorem.

This does NOT assert a global injection theorem on all raw15D syntax,
nor erase FJ's valid noninjectivity for the ORIGINAL selected frame.
The original versus closed 18D codes, DS no-go, 107 public roots,
strict Kuu primary, independent Kuu as one presentation, and
Gray non-reintroduction are preserved. No 19D filler, new axioms,
sorry or admit. Apache-2.0. Copyright Hidetoshi Itakura / 板倉英俊.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uD vD uE vE

section PhysicalConstructorPreservingWhisker

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

/-- The ACTUAL original fourteen-cell left/right whiskering simply
adjoins a fixed raw loop by .trans, so it is syntactically injective
on the genuine, dependent fourteen-cell proof fiber. This is
distinct from FJ's false injectivity at the higher fifteen-cell layer. -/
theorem nativeK5FKRawFourteenWhisker_injective
    (W : NativeK5StructuralThirteenCell p U V) (side : Bool) :
    Function.Injective (nativeK5AQWhisker W side) := by
  intro R S heq
  cases side with
  | false =>
      change NativeK5StructuralFourteenCell.trans R (nativeK5AQRightFrame W) =
        NativeK5StructuralFourteenCell.trans S (nativeK5AQRightFrame W) at heq
      injection heq
  | true =>
      change NativeK5StructuralFourteenCell.trans (nativeK5AQLeftFrame W) R =
        NativeK5StructuralFourteenCell.trans (nativeK5AQLeftFrame W) S at heq
      injection heq

/-- ALTERNATIVE faithful-to-constructor-shape TRANSPORT for the
original conservative FIFTEEN-cell core. Atoms carry the existing
exact noncommutative history and signed charge compatibilities,
but a genuine reflexivity proof remains REFLEXIVITY. -/
def nativeK5FKCoreWhisker
    (W : NativeK5StructuralThirteenCell p U V) (side : Bool)
    {R S : NativeK5FifteenFourteenFiber W}
    (h : NativeObserverCoreFifteenCell
      (nativeK5FifteenHistoryObserver W)
      (nativeK5FifteenChargeObserver W) R S) :
    NativeObserverCoreFifteenCell
      (nativeK5FifteenHistoryObserver W)
      (nativeK5FifteenChargeObserver W)
      (nativeK5AQWhisker W side R)
      (nativeK5AQWhisker W side S) := by
  induction h with
  | refl R => exact .refl _
  | atom hw hc =>
      exact .atom (nativeK5AQWhisker_history_congr W side hw)
        (nativeK5AQWhisker_charge_congr W side hc)
  | symm _ ih => exact .symm ih
  | trans _ _ ih1 ih2 => exact .trans ih1 ih2

/-- New, separately declared, original-Type-valued AQ proof
transport on the SAME actual lower source and target witnesses.
Unlike nativeK5AQWhiskerCell it retains ALL constructor tags of
the conservative core, and the actual exchange index. -/
def nativeK5FKWhiskerCell
    (W : NativeK5StructuralThirteenCell p U V) (side : Bool)
    {R S : NativeK5FifteenFourteenFiber W}
    (h : NativeK5AQFifteenCell W R S) :
    NativeK5AQFifteenCell W
      (nativeK5AQWhisker W side R)
      (nativeK5AQWhisker W side S) := by
  induction h with
  | conservative base =>
      exact .conservative (nativeK5FKCoreWhisker W side base)
  | exchange steps => exact .exchange (side :: steps)
  | symm _ ih => exact .symm ih
  | trans _ _ ih1 ih2 => exact .trans ih1 ih2

theorem nativeK5FKWhisker_conservative_refl
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W) (side : Bool) :
    nativeK5FKWhiskerCell W side (nativeK5FJConservativeRefl W R) =
      (NativeFifteenFamilyCell.conservative
        (NativeObserverCoreFifteenCell.refl
          (nativeK5AQWhisker W side R))) := rfl

theorem nativeK5FKWhisker_conservative_atom
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W) (side : Bool) :
    nativeK5FKWhiskerCell W side (nativeK5FJConservativeAtom W R) =
      (NativeFifteenFamilyCell.conservative
        (NativeObserverCoreFifteenCell.atom rfl rfl)) := rfl

/-- The FJ collision is NOT forced by the genuine C60 lower boundary:
the two DISTINCT original 15D proof constructors retain DISTINCT
target proofs under this independent alternative whiskering. -/
theorem nativeK5FKWhisker_preserves_FJ_separation
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W) (side : Bool) :
    nativeK5FKWhiskerCell W side (nativeK5FJConservativeRefl W R) ≠
      nativeK5FKWhiskerCell W side (nativeK5FJConservativeAtom W R) := by
  intro heq
  cases heq

/-- Exact obstruction to reconstructing the original proof history
AFTER the existing FJ-collapsing transport: no function on the
OLD output fiber can reproduce this constructor-preserving
alternative on every original endpoint-fixed fifteen-cell proof. -/
theorem nativeK5FKNoRecovery_from_original_whisker
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W) (side : Bool)
    (decode : NativeK5AQFifteenCell W
      (nativeK5AQWhisker W side R) (nativeK5AQWhisker W side R) →
        NativeK5AQFifteenCell W
          (nativeK5AQWhisker W side R) (nativeK5AQWhisker W side R)) :
    ¬ (∀ h : NativeK5AQFifteenCell W R R,
        decode (nativeK5AQWhiskerCell W side h) =
          nativeK5FKWhiskerCell W side h) := by
  intro h
  have heq :
      nativeK5FKWhiskerCell W side (nativeK5FJConservativeRefl W R) =
        nativeK5FKWhiskerCell W side (nativeK5FJConservativeAtom W R) := by
    calc
      nativeK5FKWhiskerCell W side (nativeK5FJConservativeRefl W R) =
          decode (nativeK5AQWhiskerCell W side
            (nativeK5FJConservativeRefl W R)) :=
        (h _).symm
      _ = decode (nativeK5AQWhiskerCell W side
            (nativeK5FJConservativeAtom W R)) :=
        congrArg decode (nativeK5FJWhisker_conservative_collision W R side)
      _ = nativeK5FKWhiskerCell W side
            (nativeK5FJConservativeAtom W R) := h _
  exact nativeK5FKWhisker_preserves_FJ_separation W R side heq

/-- A genuine separate BC frame, over the exact SAME physical 14D
whiskering on objects, but the newly selected 15D proof-relevant
whiskering on dependent Hom fibers. The old frame is unchanged. -/
def nativeK5FKBCFrame
    (W : NativeK5StructuralThirteenCell p U V) (side : Bool) :
    NativeC60BCFrame (nativeK5AXBaseLayer W) where
  onObj a := ⟨nativeK5AQWhisker W side a.down⟩
  onCell := by
    intro a b cell
    exact ⟨nativeK5FKWhiskerCell W side cell.down⟩

/-- Two genuinely different relative presentations share the
EXACT same lower physical 14D object map, with the difference
localized at proof-relevant 15D transport. -/
theorem nativeK5FKBCFrame_onObj_eq_original
    (W : NativeK5StructuralThirteenCell p U V) (side : Bool) :
    (nativeK5FKBCFrame W side).onObj =
      (nativeK5BCFrame W side).onObj := rfl

/-- The new selected full proof-bearing base frame resolves the
specific FJ source pair that is collapsed by the original frame.
This is an actual typed AX total separation, not just an observer. -/
theorem nativeK5FKBCFrame_distinguishes_FJ_pair
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W) (side : Bool) :
    (nativeK5FKBCFrame W side).mapTotal (nativeK5FJBaseRefl W R) ≠
      (nativeK5FKBCFrame W side).mapTotal (nativeK5FJBaseAtom W R) := by
  intro heq
  have hp :
      (ULift.up (nativeK5FKWhiskerCell W side (nativeK5FJConservativeRefl W R)) :
        (nativeK5AXBaseLayer W).Hom
          (ULift.up (nativeK5AQWhisker W side R))
          (ULift.up (nativeK5AQWhisker W side R))) =
        ULift.up (nativeK5FKWhiskerCell W side
          (nativeK5FJConservativeAtom W R)) :=
    eq_of_heq (Sigma.mk.inj heq).2
  exact (nativeK5FKWhisker_preserves_FJ_separation W R side)
    (congrArg ULift.down hp)

end PhysicalConstructorPreservingWhisker

#print axioms nativeK5FKRawFourteenWhisker_injective
#print axioms nativeK5FKCoreWhisker
#print axioms nativeK5FKWhiskerCell
#print axioms nativeK5FKWhisker_conservative_refl
#print axioms nativeK5FKWhisker_conservative_atom
#print axioms nativeK5FKWhisker_preserves_FJ_separation
#print axioms nativeK5FKNoRecovery_from_original_whisker
#print axioms nativeK5FKBCFrame
#print axioms nativeK5FKBCFrame_onObj_eq_original
#print axioms nativeK5FKBCFrame_distinguishes_FJ_pair

end
end Kuu.F112.Physical
