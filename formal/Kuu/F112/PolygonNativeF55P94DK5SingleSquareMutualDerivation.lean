import Kuu.F112.PolygonNativeF55P94DK5SingleSquareSixCellPolicy
import Mathlib.Tactic

/-!
# F112-P94D3AC — one horizontal square entails the other

The genuine mixed 6D naturality cube from P94D3Z is reconstructed
INSIDE the source-typed optional-square grammar WITHOUT using either
horizontal square generator. Both orders of two five-cell changes
admit independently constructed cubes.

Pasting them with just ONE horizontal naturality square and
cancelling the authentic 5D interchanger by the explicit 6D
inverse/associativity/unit evidence of the core yields the OTHER
square in both directions.

Consequently, *either* family of horizontal square generators,
plus both fundamental interchanger naturality generators, gives
exactly the SAME source-typed 5-cell connectivity as the full P94D3Z
six-cell presentation. The two raw proof terms are not identified;
what is shown is actual Type-valued 6-cell existence.

No conversion of formal Peiffer equality into higher evidence.
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

section TwoVariableNaturality

variable {allowTarget allowSource : Bool}
variable {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable {first : KuuNativeF45Tree p n m ma pa mb pb}
variable {last : KuuNativeF45Tree p n' m' ma pa mb pb}
variable {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
variable {f g : NativeF55StructuralComparison p r s}
variable {h k : NativeF55StructuralComparison p s t}

/-- The FIRST two-variable source-typed 6D naturality cube is a
composite of only the LEFT/RIGHT naturalities and core 6D
associators, even when both horizontal square families are OFF. -/
def NativeK5SquarePolicySixCell.mixedLeftThenRight
    {alpha alpha' : NativeK5StructuralFourCell p f g}
    {beta beta' : NativeK5StructuralFourCell p h k}
    (w : NativeK5StructuralFiveCell p alpha alpha')
    (v : NativeK5StructuralFiveCell p beta beta') :
    NativeK5SquarePolicySixCell allowTarget allowSource p
      (.trans (NativeK5StructuralFiveCell.targetSquareLeftThenRight w v)
        (nativeK5TypedInterchanger alpha' beta'))
      (.trans (nativeK5TypedInterchanger alpha beta)
        (NativeK5StructuralFiveCell.sourceSquareLeftThenRight w v)) := by
  let a := NativeK5StructuralFiveCell.horizontalViaTarget_left w beta
  let b := NativeK5StructuralFiveCell.horizontalViaTarget_right alpha' v
  let c := nativeK5TypedInterchanger alpha' beta'
  let i := nativeK5TypedInterchanger alpha' beta
  let j := nativeK5TypedInterchanger alpha beta
  let d := NativeK5StructuralFiveCell.horizontalViaSource_right alpha' v
  let e := NativeK5StructuralFiveCell.horizontalViaSource_left w beta
  change NativeK5SquarePolicySixCell allowTarget allowSource p
    (.trans (.trans a b) c) (.trans j (.trans e d))
  exact .trans (.core (.verticalAssoc a b c))
    (.trans (.verticalRight a (.interchangerRightNaturality alpha' v))
      (.trans (.symm (.core (.verticalAssoc a i d)))
        (.trans (.verticalLeft (.interchangerLeftNaturality w beta) d)
          (.core (.verticalAssoc j e d))))

/-- The SECOND two-variable source-typed 6D naturality cube is
also independently derived from the two naturality generators,
with the right five-cell change performed FIRST. -/
def NativeK5SquarePolicySixCell.mixedRightThenLeft
    {alpha alpha' : NativeK5StructuralFourCell p f g}
    {beta beta' : NativeK5StructuralFourCell p h k}
    (w : NativeK5StructuralFiveCell p alpha alpha')
    (v : NativeK5StructuralFiveCell p beta beta') :
    NativeK5SquarePolicySixCell allowTarget allowSource p
      (.trans (NativeK5StructuralFiveCell.targetSquareRightThenLeft w v)
        (nativeK5TypedInterchanger alpha' beta'))
      (.trans (nativeK5TypedInterchanger alpha beta)
        (NativeK5StructuralFiveCell.sourceSquareRightThenLeft w v)) := by
  let a := NativeK5StructuralFiveCell.horizontalViaTarget_right alpha v
  let b := NativeK5StructuralFiveCell.horizontalViaTarget_left w beta'
  let c := nativeK5TypedInterchanger alpha' beta'
  let i := nativeK5TypedInterchanger alpha beta'
  let j := nativeK5TypedInterchanger alpha beta
  let d := NativeK5StructuralFiveCell.horizontalViaSource_left w beta'
  let e := NativeK5StructuralFiveCell.horizontalViaSource_right alpha v
  change NativeK5SquarePolicySixCell allowTarget allowSource p
    (.trans (.trans a b) c) (.trans j (.trans e d))
  exact .trans (.core (.verticalAssoc a b c))
    (.trans (.verticalRight a (.interchangerLeftNaturality w beta'))
      (.trans (.symm (.core (.verticalAssoc a i d)))
        (.trans (.verticalLeft (.interchangerRightNaturality alpha v) d)
          (.core (.verticalAssoc j e d))))

/-- ONE target-square 6D filler produces a genuine source-square
6D filler by two mixed naturality cubes and left cancellation.
Works for arbitrary original dependent five-cell evidence. -/
def NativeK5SquarePolicySixCell.sourceFromTarget
    {alpha alpha' : NativeK5StructuralFourCell p f g}
    {beta beta' : NativeK5StructuralFourCell p h k}
    (w : NativeK5StructuralFiveCell p alpha alpha')
    (v : NativeK5StructuralFiveCell p beta beta')
    (q : NativeK5SquarePolicySixCell allowTarget allowSource p
      (NativeK5StructuralFiveCell.targetSquareLeftThenRight w v)
      (NativeK5StructuralFiveCell.targetSquareRightThenLeft w v)) :
    NativeK5SquarePolicySixCell allowTarget allowSource p
      (NativeK5StructuralFiveCell.sourceSquareLeftThenRight w v)
      (NativeK5StructuralFiveCell.sourceSquareRightThenLeft w v) := by
  let i := nativeK5TypedInterchanger alpha beta
  let j := nativeK5TypedInterchanger alpha' beta'
  have hLR : NativeK5SquarePolicySixCell allowTarget allowSource p
      (.trans (NativeK5StructuralFiveCell.targetSquareLeftThenRight w v) j)
      (.trans i (NativeK5StructuralFiveCell.sourceSquareLeftThenRight w v)) :=
    NativeK5SquarePolicySixCell.mixedLeftThenRight w v
  have hRL : NativeK5SquarePolicySixCell allowTarget allowSource p
      (.trans (NativeK5StructuralFiveCell.targetSquareRightThenLeft w v) j)
      (.trans i (NativeK5StructuralFiveCell.sourceSquareRightThenLeft w v)) :=
    NativeK5SquarePolicySixCell.mixedRightThenLeft w v
  have h : NativeK5SquarePolicySixCell allowTarget allowSource p
      (.trans i (NativeK5StructuralFiveCell.sourceSquareLeftThenRight w v))
      (.trans i (NativeK5StructuralFiveCell.sourceSquareRightThenLeft w v)) :=
    .trans (.symm hLR) (.trans (.verticalLeft q j) hRL)
  exact NativeK5SquarePolicySixCell.cancelLeft i h

/-- Conversely, ONE source-square filler yields the genuine
target-square filler; right cancellation uses the original
P94D3Y invertible 5D interchanger, not a Peiffer word equality. -/
def NativeK5SquarePolicySixCell.targetFromSource
    {alpha alpha' : NativeK5StructuralFourCell p f g}
    {beta beta' : NativeK5StructuralFourCell p h k}
    (w : NativeK5StructuralFiveCell p alpha alpha')
    (v : NativeK5StructuralFiveCell p beta beta')
    (q : NativeK5SquarePolicySixCell allowTarget allowSource p
      (NativeK5StructuralFiveCell.sourceSquareLeftThenRight w v)
      (NativeK5StructuralFiveCell.sourceSquareRightThenLeft w v)) :
    NativeK5SquarePolicySixCell allowTarget allowSource p
      (NativeK5StructuralFiveCell.targetSquareLeftThenRight w v)
      (NativeK5StructuralFiveCell.targetSquareRightThenLeft w v) := by
  let i := nativeK5TypedInterchanger alpha beta
  let j := nativeK5TypedInterchanger alpha' beta'
  have hLR : NativeK5SquarePolicySixCell allowTarget allowSource p
      (.trans (NativeK5StructuralFiveCell.targetSquareLeftThenRight w v) j)
      (.trans i (NativeK5StructuralFiveCell.sourceSquareLeftThenRight w v)) :=
    NativeK5SquarePolicySixCell.mixedLeftThenRight w v
  have hRL : NativeK5SquarePolicySixCell allowTarget allowSource p
      (.trans (NativeK5StructuralFiveCell.targetSquareRightThenLeft w v) j)
      (.trans i (NativeK5StructuralFiveCell.sourceSquareRightThenLeft w v)) :=
    NativeK5SquarePolicySixCell.mixedRightThenLeft w v
  have h : NativeK5SquarePolicySixCell allowTarget allowSource p
      (.trans (NativeK5StructuralFiveCell.targetSquareLeftThenRight w v) j)
      (.trans (NativeK5StructuralFiveCell.targetSquareRightThenLeft w v) j) :=
    .trans hLR (.trans (.verticalRight i q) (.symm hRL))
  exact NativeK5SquarePolicySixCell.cancelRight j h

/-- Target-ONLY policy already constructs the missing source
horizontal naturality square for ALL original typed 5-cell terms. -/
def nativeK5TargetOnly_generatesSourceSquare
    {alpha alpha' : NativeK5StructuralFourCell p f g}
    {beta beta' : NativeK5StructuralFourCell p h k}
    (w : NativeK5StructuralFiveCell p alpha alpha')
    (v : NativeK5StructuralFiveCell p beta beta') :
    NativeK5SquarePolicySixCell true false p
      (NativeK5StructuralFiveCell.sourceSquareLeftThenRight w v)
      (NativeK5StructuralFiveCell.sourceSquareRightThenLeft w v) :=
  NativeK5SquarePolicySixCell.sourceFromTarget w v
    (.horizontalTargetSquare rfl w v)

/-- Source-ONLY policy similarly generates the missing target
horizontal square for ALL original dependent 5-cell terms. -/
def nativeK5SourceOnly_generatesTargetSquare
    {alpha alpha' : NativeK5StructuralFourCell p f g}
    {beta beta' : NativeK5StructuralFourCell p h k}
    (w : NativeK5StructuralFiveCell p alpha alpha')
    (v : NativeK5StructuralFiveCell p beta beta') :
    NativeK5SquarePolicySixCell false true p
      (NativeK5StructuralFiveCell.targetSquareLeftThenRight w v)
      (NativeK5StructuralFiveCell.targetSquareRightThenLeft w v) :=
  NativeK5SquarePolicySixCell.targetFromSource w v
    (.horizontalSourceSquare rfl w v)

end TwoVariableNaturality

/-- Map EVERY source-typed full P94D3Z six-cell to target-square
ONLY grammar. The missing source-square constructor is provided
by the *derived* source 6D composite above. -/
def NativeK5StructuralSixCell.toTargetOnly
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55StructuralComparison p r s}
    {alpha beta : NativeK5StructuralFourCell p f g}
    {w z : NativeK5StructuralFiveCell p alpha beta}
    (u : NativeK5StructuralSixCell p w z) :
    NativeK5SquarePolicySixCell true false p w z := by
  induction u with
  | refl w => exact .core (.refl w)
  | symm _ ih => exact .symm ih
  | trans _ _ ih₁ ih₂ => exact .trans ih₁ ih₂
  | verticalLeft witness suffix ih => exact .verticalLeft ih suffix
  | verticalRight lead witness ih => exact .verticalRight lead ih
  | verticalAssoc a b c => exact .core (.verticalAssoc a b c)
  | verticalLeftUnit w => exact .core (.verticalLeftUnit w)
  | verticalRightUnit w => exact .core (.verticalRightUnit w)
  | inverseLeft w => exact .core (.inverseLeft w)
  | inverseRight w => exact .core (.inverseRight w)
  | inverseRespect witness ih => exact .inverseRespect ih
  | interchangerLeftNaturality w beta =>
      exact .interchangerLeftNaturality w beta
  | interchangerRightNaturality alpha w =>
      exact .interchangerRightNaturality alpha w
  | horizontalTargetSquare w v => exact .horizontalTargetSquare rfl w v
  | horizontalSourceSquare w v =>
      exact nativeK5TargetOnly_generatesSourceSquare w v
  | precompose prior witness ih => exact .precompose prior ih
  | postcompose witness suffix ih => exact .postcompose ih suffix

/-- Map EVERY source-typed full 6-cell to SOURCE-square ONLY
grammar. The omitted target-square family is entirely DERIVED. -/
def NativeK5StructuralSixCell.toSourceOnly
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55StructuralComparison p r s}
    {alpha beta : NativeK5StructuralFourCell p f g}
    {w z : NativeK5StructuralFiveCell p alpha beta}
    (u : NativeK5StructuralSixCell p w z) :
    NativeK5SquarePolicySixCell false true p w z := by
  induction u with
  | refl w => exact .core (.refl w)
  | symm _ ih => exact .symm ih
  | trans _ _ ih₁ ih₂ => exact .trans ih₁ ih₂
  | verticalLeft witness suffix ih => exact .verticalLeft ih suffix
  | verticalRight lead witness ih => exact .verticalRight lead ih
  | verticalAssoc a b c => exact .core (.verticalAssoc a b c)
  | verticalLeftUnit w => exact .core (.verticalLeftUnit w)
  | verticalRightUnit w => exact .core (.verticalRightUnit w)
  | inverseLeft w => exact .core (.inverseLeft w)
  | inverseRight w => exact .core (.inverseRight w)
  | inverseRespect witness ih => exact .inverseRespect ih
  | interchangerLeftNaturality w beta =>
      exact .interchangerLeftNaturality w beta
  | interchangerRightNaturality alpha w =>
      exact .interchangerRightNaturality alpha w
  | horizontalTargetSquare w v =>
      exact nativeK5SourceOnly_generatesTargetSquare w v
  | horizontalSourceSquare w v => exact .horizontalSourceSquare rfl w v
  | precompose prior witness ih => exact .precompose prior ih
  | postcompose witness suffix ih => exact .postcompose ih suffix

/-- The entire 5D connectivity of the genuinely source-typed
full 6D presentation descends to the target-only grammar and back.
This is NOT equality of raw 6D witnesses. -/
theorem nativeK5TargetOnly_fullConnectivity
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55StructuralComparison p r s}
    {alpha beta : NativeK5StructuralFourCell p f g}
    (w z : NativeK5StructuralFiveCell p alpha beta) :
    Nonempty (NativeK5SquarePolicySixCell true false p w z) ↔
      Nonempty (NativeK5StructuralSixCell p w z) := by
  constructor
  · rintro ⟨u⟩
    exact ⟨u.toFull⟩
  · rintro ⟨u⟩
    exact ⟨u.toTargetOnly⟩

/-- Source-only square grammar gives exactly the same 5D
connectivity relation as the entire full P94D3Z six-cell grammar. -/
theorem nativeK5SourceOnly_fullConnectivity
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55StructuralComparison p r s}
    {alpha beta : NativeK5StructuralFourCell p f g}
    (w z : NativeK5StructuralFiveCell p alpha beta) :
    Nonempty (NativeK5SquarePolicySixCell false true p w z) ↔
      Nonempty (NativeK5StructuralSixCell p w z) := by
  constructor
  · rintro ⟨u⟩
    exact ⟨u.toFull⟩
  · rintro ⟨u⟩
    exact ⟨u.toSourceOnly⟩

/-- Thus the two apparently separate horizontal square families
are INTERDERIVABLE once both higher interchanger naturalities
are retained: one single family suffices for every 6D filler
existence assertion in the complete P94D3Z source presentation. -/
theorem nativeK5TargetSourceOnly_equivalentConnectivity
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55StructuralComparison p r s}
    {alpha beta : NativeK5StructuralFourCell p f g}
    (w z : NativeK5StructuralFiveCell p alpha beta) :
    Nonempty (NativeK5SquarePolicySixCell true false p w z) ↔
      Nonempty (NativeK5SquarePolicySixCell false true p w z) := by
  exact (nativeK5TargetOnly_fullConnectivity w z).trans
    (nativeK5SourceOnly_fullConnectivity w z).symm

#print axioms NativeK5SquarePolicySixCell.mixedLeftThenRight
#print axioms NativeK5SquarePolicySixCell.mixedRightThenLeft
#print axioms NativeK5SquarePolicySixCell.sourceFromTarget
#print axioms NativeK5SquarePolicySixCell.targetFromSource
#print axioms nativeK5TargetOnly_generatesSourceSquare
#print axioms nativeK5SourceOnly_generatesTargetSquare
#print axioms NativeK5StructuralSixCell.toTargetOnly
#print axioms NativeK5StructuralSixCell.toSourceOnly
#print axioms nativeK5TargetOnly_fullConnectivity
#print axioms nativeK5SourceOnly_fullConnectivity
#print axioms nativeK5TargetSourceOnly_equivalentConnectivity

end
end Kuu.F112.Physical
