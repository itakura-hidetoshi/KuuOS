import Kuu.F112.PolygonNativeC60AQFullPentagonConstructorPreservingWhisker

/-!
# F112-P94D3FL — full dependent Type-valued Hom reflection for the FK whisker

The *alternative* FK 15D transport is constructor preserving. This file
tests its exact whole-Hom injectivity, retaining both genuinely dependent
14D physical endpoints and the intermediate boundary at each composition.
The original selected FJ whisker remains noninjective; it is NEVER
redefined, replaced or strengthened.

The four raw-proof constructors of the observer-conservative core,
the independent, source-indexed exchange, and outer symmetry/composition
are all handled explicitly. Extracting the intermediate dependent Sigma
from a target trans and reflecting its source via the ALREADY PROVED
14D raw-whisker injection avoids assuming equality of variable midpoints.
The exchange index is recovered from the genuine (side :: steps) index,
not from charge, history, a quotient or an abelianization.

No original 19D filler, Gray reinsertion, strict global n-category or
hyperdescent claim. The original FJ nonfaithfulness and DS obstruction
stay intact. Append-only, same-root, public 107 roots unchanged.
No sorry/admit/new axiom. Apache-2.0. Copyright Hidetoshi Itakura.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uA uB uI uD vD uE vE

/-- Target-side conservative trans exposes its full dependent
intermediate object and LEFT raw subproof, not a scalar trace. -/
def nativeK5FLCoreTransLeftCode
    {A : Type uA} {B : Type uB}
    (history : A → B) (charge : A → ℤ)
    {x y : A}
    (h : NativeObserverCoreFifteenCell history charge x y) :
    Option (Σ mid : A, NativeObserverCoreFifteenCell history charge x mid) :=
  match h with
  | .trans (y := mid) p _ => some ⟨mid, p⟩
  | _ => none

/-- Target-side conservative trans exposes its full dependent
intermediate object and RIGHT raw subproof. -/
def nativeK5FLCoreTransRightCode
    {A : Type uA} {B : Type uB}
    (history : A → B) (charge : A → ℤ)
    {x y : A}
    (h : NativeObserverCoreFifteenCell history charge x y) :
    Option (Σ mid : A, NativeObserverCoreFifteenCell history charge mid y) :=
  match h with
  | .trans (y := mid) _ p => some ⟨mid, p⟩
  | _ => none

/-- The matching dependent full-indexed 15D trans-left extractor. -/
def nativeK5FLFamilyTransLeftCode
    {A : Type uA} {B : Type uB} {I : Type uI}
    (history : A → B) (charge : A → ℤ)
    (left right : I → A)
    (chargeEq : ∀ i : I, charge (left i) = charge (right i))
    {x y : A}
    (h : NativeFifteenFamilyCell history charge left right chargeEq x y) :
    Option (Σ mid : A,
      NativeFifteenFamilyCell history charge left right chargeEq x mid) :=
  match h with
  | .trans (y := mid) p _ => some ⟨mid, p⟩
  | _ => none

/-- The matching dependent full-indexed 15D trans-right extractor. -/
def nativeK5FLFamilyTransRightCode
    {A : Type uA} {B : Type uB} {I : Type uI}
    (history : A → B) (charge : A → ℤ)
    (left right : I → A)
    (chargeEq : ∀ i : I, charge (left i) = charge (right i))
    {x y : A}
    (h : NativeFifteenFamilyCell history charge left right chargeEq x y) :
    Option (Σ mid : A,
      NativeFifteenFamilyCell history charge left right chargeEq mid y) :=
  match h with
  | .trans (y := mid) _ p => some ⟨mid, p⟩
  | _ => none

section FullDependentPhysicalWhisker

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

/-- A fully dependent, boundary-preserving package for each ORIGINAL
independent AQ exchange. A source index equality yields equality of
packages without trying to eliminate equality inside fixed endpoints. -/
def nativeK5FLExchangePack
    (W : NativeK5StructuralThirteenCell p U V)
    (steps : List Bool) :
    Σ pair : NativeK5FifteenFourteenFiber W × NativeK5FifteenFourteenFiber W,
      NativeK5AQFifteenCell W pair.1 pair.2 :=
  ⟨(nativeK5AQLeft W steps, nativeK5AQRight W steps),
    NativeFifteenFamilyCell.exchange steps⟩

/-- Full source/target-fixed conservative Hom injection. Unlike FJ's
flattening operation, the FK core map preserves all FOUR constructors.
The trans case explicitly reflects its variable intermediate 14D
boundary before invoking the two induction hypotheses. -/
theorem nativeK5FLCoreWhisker_injective
    (W : NativeK5StructuralThirteenCell p U V) (side : Bool) :
    ∀ {R S : NativeK5FifteenFourteenFiber W},
      Function.Injective (fun h : NativeObserverCoreFifteenCell
        (nativeK5FifteenHistoryObserver W)
        (nativeK5FifteenChargeObserver W) R S =>
          nativeK5FKCoreWhisker W side h) := by
  intro R S h k heq
  induction h with
  | refl _ =>
      cases k with
      | refl _ => rfl
      | atom _ _ => cases heq
      | symm _ => cases heq
      | trans _ _ => cases heq
  | atom _ _ =>
      cases k with
      | refl _ => cases heq
      | atom _ _ => rfl
      | symm _ => cases heq
      | trans _ _ => cases heq
  | symm h ih =>
      cases k with
      | refl _ => cases heq
      | atom _ _ => cases heq
      | symm k =>
          have hh : nativeK5FKCoreWhisker W side h =
              nativeK5FKCoreWhisker W side k := by
            injection heq
          have hsource : h = k := ih hh
          cases hsource
          rfl
      | trans _ _ => cases heq
  | trans h t ihh iht =>
      cases k with
      | refl _ => cases heq
      | atom _ _ => cases heq
      | symm _ => cases heq
      | trans k r =>
          have hleftSigma := Option.some.inj
            (congrArg
              (nativeK5FLCoreTransLeftCode
                (nativeK5FifteenHistoryObserver W)
                (nativeK5FifteenChargeObserver W)) heq)
          have hrightSigma := Option.some.inj
            (congrArg
              (nativeK5FLCoreTransRightCode
                (nativeK5FifteenHistoryObserver W)
                (nativeK5FifteenChargeObserver W)) heq)
          have hmid :=
            (nativeK5FKRawFourteenWhisker_injective W side)
              (congrArg Sigma.fst hleftSigma)
          cases hmid
          have hl : nativeK5FKCoreWhisker W side h =
              nativeK5FKCoreWhisker W side k :=
            eq_of_heq (Sigma.mk.inj hleftSigma).2
          have hr : nativeK5FKCoreWhisker W side t =
              nativeK5FKCoreWhisker W side r :=
            eq_of_heq (Sigma.mk.inj hrightSigma).2
          have hp : h = k := ihh hl
          have ht : t = r := iht hr
          cases hp
          cases ht
          rfl

/-- Independent family exchange index, if and only if the proof is
directly an exchange constructor. No quotient or boundary erasure. -/
def nativeK5FLExchangeIndex
    (W : NativeK5StructuralThirteenCell p U V)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S) : Option (List Bool) :=
  match cell with
  | .exchange index => some index
  | _ => none

/-- A concrete exchange index identifies its raw proof constructor
heterogeneously, even when the dependent 14D endpoints are variable. -/
theorem nativeK5FLExchangeIndex_sound
    (W : NativeK5StructuralThirteenCell p U V)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S)
    {index : List Bool}
    (hindex : nativeK5FLExchangeIndex W cell = some index) :
    HEq cell (nativeK5AQExchange W index) := by
  cases cell with
  | conservative _ => cases hindex
  | exchange actual =>
      have heq : actual = index := Option.some.inj hindex
      cases heq
      rfl
  | symm _ => cases hindex
  | trans _ _ => cases hindex

/-- The new FK transport preserves the entire independent exchange
index by left-prefixing; the other constructor sectors remain none. -/
theorem nativeK5FLExchangeIndex_whisker
    (W : NativeK5StructuralThirteenCell p U V)
    (side : Bool)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S) :
    nativeK5FLExchangeIndex W (nativeK5FKWhiskerCell W side cell) =
      (nativeK5FLExchangeIndex W cell).map (List.cons side) := by
  cases cell <;> rfl

/-- COMPLETE original physical Type-valued 15D dependent Hom fiber
injection for the new FK presentation, with the independently adjoined
exchange and outer proof constructors included. This says nothing
about the FJ original flattened whisker, which is noninjective. -/
theorem nativeK5FLWhiskerCell_injective
    (W : NativeK5StructuralThirteenCell p U V) (side : Bool) :
    ∀ {R S : NativeK5FifteenFourteenFiber W},
      Function.Injective (fun h : NativeK5AQFifteenCell W R S =>
        nativeK5FKWhiskerCell W side h) := by
  intro R S h k heq
  induction h with
  | conservative base =>
      cases k with
      | conservative other =>
          have hb : nativeK5FKCoreWhisker W side base =
              nativeK5FKCoreWhisker W side other := by
            injection heq
          have hbase : base = other :=
            nativeK5FLCoreWhisker_injective W side hb
          cases hbase
          rfl
      | exchange _ => cases heq
      | symm _ => cases heq
      | trans _ _ => cases heq
  | exchange steps =>
      have hcode : some (side :: steps) =
          (nativeK5FLExchangeIndex W k).map (List.cons side) := by
        simpa only [nativeK5FLExchangeIndex_whisker] using
          congrArg (nativeK5FLExchangeIndex W) heq
      cases hki : nativeK5FLExchangeIndex W k with
      | none =>
          simp [hki] at hcode
      | some other =>
          have hp : side :: steps = side :: other := by
            simpa [hki] using hcode
          have hsteps : steps = other := (List.cons.inj hp).2
          have hsource : HEq k (nativeK5AQExchange W other) :=
            nativeK5FLExchangeIndex_sound W k hki
          cases hsteps
          exact eq_of_heq hsource.symm
  | symm h ih =>
      cases k with
      | conservative _ => cases heq
      | exchange _ => cases heq
      | symm k =>
          have hh : nativeK5FKWhiskerCell W side h =
              nativeK5FKWhiskerCell W side k := by
            injection heq
          have hsource : h = k := ih hh
          cases hsource
          rfl
      | trans _ _ => cases heq
  | trans h t ihh iht =>
      cases k with
      | conservative _ => cases heq
      | exchange _ => cases heq
      | symm _ => cases heq
      | trans k r =>
          have hleftSigma := Option.some.inj
            (congrArg
              (nativeK5FLFamilyTransLeftCode
                (nativeK5FifteenHistoryObserver W)
                (nativeK5FifteenChargeObserver W)
                (nativeK5AQLeft W) (nativeK5AQRight W)
                (nativeK5AQChargeEq W)) heq)
          have hrightSigma := Option.some.inj
            (congrArg
              (nativeK5FLFamilyTransRightCode
                (nativeK5FifteenHistoryObserver W)
                (nativeK5FifteenChargeObserver W)
                (nativeK5AQLeft W) (nativeK5AQRight W)
                (nativeK5AQChargeEq W)) heq)
          have hmid :=
            (nativeK5FKRawFourteenWhisker_injective W side)
              (congrArg Sigma.fst hleftSigma)
          cases hmid
          have hl : nativeK5FKWhiskerCell W side h =
              nativeK5FKWhiskerCell W side k :=
            eq_of_heq (Sigma.mk.inj hleftSigma).2
          have hr : nativeK5FKWhiskerCell W side t =
              nativeK5FKWhiskerCell W side r :=
            eq_of_heq (Sigma.mk.inj hrightSigma).2
          have hp : h = k := ihh hl
          have ht : t = r := iht hr
          cases hp
          cases ht
          rfl

/-- Every finite alternative physical AQ context retains full
original raw15D Hom evidence: induction over the word composes
the proven singleton injectivity, including empty word. -/
theorem nativeK5FLContextCell_injective
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool) :
    ∀ {R S : NativeK5FifteenFourteenFiber W},
      Function.Injective (fun h : NativeK5AQFifteenCell W R S =>
        nativeK5FKContextCell W word h) := by
  induction word with
  | nil =>
      intro R S h k heq
      exact heq
  | cons side rest ih =>
      intro R S h k heq
      apply ih
      exact nativeK5FLWhiskerCell_injective W side heq

/-- The ACTUAL alternative frame action is faithful on every original
fixed-boundary Hom fiber. The full base object action additionally
requires reflecting both 14D endpoints and is addressed separately. -/
theorem nativeK5FLBCFrame_onCell_injective
    (W : NativeK5StructuralThirteenCell p U V)
    (side : Bool)
    (a b : (nativeK5AXBaseLayer W).Obj) :
    Function.Injective ((nativeK5FKBCFrame W side).onCell (a := a) (b := b)) := by
  intro h k heq
  apply ULift.down_injective
  apply nativeK5FLWhiskerCell_injective W side
  exact congrArg ULift.down heq

end FullDependentPhysicalWhisker

#print axioms nativeK5FLCoreWhisker_injective
#print axioms nativeK5FLWhiskerCell_injective
#print axioms nativeK5FLContextCell_injective
#print axioms nativeK5FLBCFrame_onCell_injective

end
end Kuu.F112.Physical
