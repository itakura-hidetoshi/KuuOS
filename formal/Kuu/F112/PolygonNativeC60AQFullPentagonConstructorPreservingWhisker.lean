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


/-- A DEFINED, constructor-wise forgetting map on the original
genuine Type-valued 15D grammar: preserve exchange and outer signed
composites, but flatten the inner conservative evidence to its
compatible observer atom. This is exactly the information loss
FJ detected, not a new axiom or quotient. -/
def nativeK5FKForgetConservativeCell
    (W : NativeK5StructuralThirteenCell p U V)
    {R S : NativeK5FifteenFourteenFiber W}
    (h : NativeK5AQFifteenCell W R S) :
    NativeK5AQFifteenCell W R S := by
  induction h with
  | conservative base =>
      exact .conservative (.atom base.history_sound base.charge_sound)
  | exchange steps => exact .exchange steps
  | symm _ ih => exact .symm ih
  | trans _ _ ih1 ih2 => exact .trans ih1 ih2

/-- Exact ORIGINAL-versus-ALTERNATIVE presentation comparison:
the old whiskering is obtained by FIRST using the constructor-
preserving proof transport, THEN forgetting conservative core
construction history. The comparison holds for ALL original
dependent raw15D paths, not only FJ's two selected witnesses.
This is not the reverse factorization, which FK disproves. -/
theorem nativeK5FKOriginalWhisker_factors_through_alternative
    (W : NativeK5StructuralThirteenCell p U V)
    (side : Bool) {R S : NativeK5FifteenFourteenFiber W}
    (h : NativeK5AQFifteenCell W R S) :
    nativeK5AQWhiskerCell W side h =
      nativeK5FKForgetConservativeCell W
        (nativeK5FKWhiskerCell W side h) := by
  induction h with
  | conservative base => rfl
  | exchange steps => rfl
  | symm h ih =>
      change NativeFifteenFamilyCell.symm
          (nativeK5AQWhiskerCell W side h) =
        NativeFifteenFamilyCell.symm
          (nativeK5FKForgetConservativeCell W
            (nativeK5FKWhiskerCell W side h))
      rw [ih]
  | trans h k ih ik =>
      change NativeFifteenFamilyCell.trans
          (nativeK5AQWhiskerCell W side h)
          (nativeK5AQWhiskerCell W side k) =
        NativeFifteenFamilyCell.trans
          (nativeK5FKForgetConservativeCell W
            (nativeK5FKWhiskerCell W side h))
          (nativeK5FKForgetConservativeCell W
            (nativeK5FKWhiskerCell W side k))
      rw [ih, ik]

/-- Preserve the entire typed original 15D history under an
arbitrary finite chronological physical AQ context in the
separately selected constructor-preserving presentation.
The original 14D context action and its boundaries are unchanged. -/
def nativeK5FKContextCell
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool) {R S : NativeK5FifteenFourteenFiber W}
    (h : NativeK5AQFifteenCell W R S) :
    NativeK5AQFifteenCell W
      (nativeK5AQContext W word R)
      (nativeK5AQContext W word S) := by
  induction word with
  | nil => exact h
  | cons side rest ih => exact nativeK5FKWhiskerCell W side ih

/-- Original conservative reflexivity remains a REFLEXIVITY
constructor after EVERY finite physical context, including empty. -/
theorem nativeK5FKContext_conservative_refl
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (word : List Bool) :
    nativeK5FKContextCell W word (nativeK5FJConservativeRefl W R) =
      (NativeFifteenFamilyCell.conservative
        (NativeObserverCoreFifteenCell.refl
          (nativeK5AQContext W word R))) := by
  induction word with
  | nil => rfl
  | cons side rest ih =>
      change
        nativeK5FKWhiskerCell W side
          (nativeK5FKContextCell W rest (nativeK5FJConservativeRefl W R)) =
        NativeFifteenFamilyCell.conservative
          (NativeObserverCoreFifteenCell.refl
            (nativeK5AQWhisker W side
              (nativeK5AQContext W rest R)))
      rw [ih]
      rfl

/-- Original conservative atom stays an ATOM after EVERY finite
context: the original core-constructor distinction remains visible. -/
theorem nativeK5FKContext_conservative_atom
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (word : List Bool) :
    nativeK5FKContextCell W word (nativeK5FJConservativeAtom W R) =
      (NativeFifteenFamilyCell.conservative
        (NativeObserverCoreFifteenCell.atom rfl rfl)) := by
  induction word with
  | nil => rfl
  | cons side rest ih =>
      change
        nativeK5FKWhiskerCell W side
          (nativeK5FKContextCell W rest (nativeK5FJConservativeAtom W R)) =
        NativeFifteenFamilyCell.conservative
          (NativeObserverCoreFifteenCell.atom rfl rfl)
      rw [ih]
      rfl

/-- No finite AQ word erases the selected FJ conservative
refl-versus-atom difference in the ALTERNATIVE Type-valued
presentation, even though FJ's ORIGINAL transport does. -/
theorem nativeK5FKContext_preserves_FJ_separation
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (word : List Bool) :
    nativeK5FKContextCell W word (nativeK5FJConservativeRefl W R) ≠
      nativeK5FKContextCell W word (nativeK5FJConservativeAtom W R) := by
  rw [nativeK5FKContext_conservative_refl W R word,
    nativeK5FKContext_conservative_atom W R word]
  intro heq
  cases heq

/-- In the ORIGINAL selected physical 15D proof transport, the
SAME source refl/atom pair collapses after EVERY nonempty context.
This is a constructor-level derivation, prior to the 17D/18D
obstructions already formalized in FJ. -/
theorem nativeK5FKOriginalContext_FJ_collision_nonempty
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (word : List Bool) (hne : word ≠ []) :
    nativeK5AQContextCell W word (nativeK5FJConservativeRefl W R) =
      nativeK5AQContextCell W word (nativeK5FJConservativeAtom W R) := by
  revert hne
  induction word with
  | nil =>
      intro hnil
      exact (hnil rfl).elim
  | cons side rest ih =>
      intro _
      cases rest with
      | nil =>
          exact nativeK5FJWhisker_conservative_collision W R side
      | cons next tail =>
          change
            nativeK5AQWhiskerCell W side
              (nativeK5AQContextCell W (next :: tail)
                (nativeK5FJConservativeRefl W R)) =
            nativeK5AQWhiskerCell W side
              (nativeK5AQContextCell W (next :: tail)
                (nativeK5FJConservativeAtom W R))
          exact congrArg
            (nativeK5AQWhiskerCell W side) (ih (by simp))

/-- Exact operational distinction between the two SAME-boundary
physical AQ presentations on a common, fixed original witness
pair for EVERY nonempty finite context: the old proof syntax
collapses and the new one does not. No claim is made about ALL
possible witness pairs or injectivity of the whole alternative. -/
theorem nativeK5FKOriginal_vs_alternative_nonempty
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (word : List Bool) (hne : word ≠ []) :
    nativeK5AQContextCell W word (nativeK5FJConservativeRefl W R) =
        nativeK5AQContextCell W word (nativeK5FJConservativeAtom W R) ∧
      nativeK5FKContextCell W word (nativeK5FJConservativeRefl W R) ≠
        nativeK5FKContextCell W word (nativeK5FJConservativeAtom W R) :=
  ⟨nativeK5FKOriginalContext_FJ_collision_nonempty W R word hne,
    nativeK5FKContext_preserves_FJ_separation W R word⟩

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
#print axioms nativeK5FKForgetConservativeCell
#print axioms nativeK5FKOriginalWhisker_factors_through_alternative
#print axioms nativeK5FKContextCell
#print axioms nativeK5FKContext_conservative_refl
#print axioms nativeK5FKContext_conservative_atom
#print axioms nativeK5FKContext_preserves_FJ_separation
#print axioms nativeK5FKOriginalContext_FJ_collision_nonempty
#print axioms nativeK5FKOriginal_vs_alternative_nonempty

end
end Kuu.F112.Physical
