import Kuu.F112.PolygonNativeF55P94DK5PentagonatorHorizontalSquareNecessity
import Mathlib.Tactic

/-!
# F112-P94D3AC — independent 6D square policies over original typed cells

The P94D3AB observer proves that *neither* horizontal naturality
square family can be omitted together with the other. This file
tests the stronger question of whether the TWO square families
are individually necessary when BOTH existing P94D3Z interchanger
naturality constructors are retained.

An explicit genuinely source-typed optional-square 6-cell grammar
allows either or both square families. The conservative P94D3AA
pre-naturality core and both fundamental left/right naturality
generators are retained, together with typed vertical congruences,
inversions, 6D composition and source F54 whiskering.

Two explicit 6D cancellation constructions are proved using the
original core associativity, inverse and unit witnesses, never
assuming equality of raw five-cell terms or Peiffer images.

Lean/mathlib pinned; no Gray, sorry, admit, or new axioms.
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

/-- Source-typed 6D grammar. Setting a square permission to false
excludes precisely that primitive square constructor while retaining
BOTH independent interchanger naturalities. -/
inductive NativeK5SquarePolicySixCell
    (allowTarget allowSource : Bool) (p : Polygon) :
    ∀ {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g},
      NativeK5StructuralFiveCell p alpha beta →
      NativeK5StructuralFiveCell p alpha beta →
      Type (max (max uD uE) (max vD vE)) where
  | core
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      (u : NativeK5PrenaturalitySixCell p w z) :
      NativeK5SquarePolicySixCell allowTarget allowSource p w z
  | interchangerLeftNaturality
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {h k : NativeF55StructuralComparison p s t}
      {alpha alpha' : NativeK5StructuralFourCell p f g}
      (w : NativeK5StructuralFiveCell p alpha alpha')
      (beta : NativeK5StructuralFourCell p h k) :
      NativeK5SquarePolicySixCell allowTarget allowSource p
        (NativeK5StructuralFiveCell.interchangerLeftPathTarget w beta)
        (NativeK5StructuralFiveCell.interchangerLeftPathSource w beta)
  | interchangerRightNaturality
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {h k : NativeF55StructuralComparison p s t}
      (alpha : NativeK5StructuralFourCell p f g)
      {beta beta' : NativeK5StructuralFourCell p h k}
      (w : NativeK5StructuralFiveCell p beta beta') :
      NativeK5SquarePolicySixCell allowTarget allowSource p
        (NativeK5StructuralFiveCell.interchangerRightPathTarget alpha w)
        (NativeK5StructuralFiveCell.interchangerRightPathSource alpha w)
  | horizontalTargetSquare
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {h k : NativeF55StructuralComparison p s t}
      {alpha alpha' : NativeK5StructuralFourCell p f g}
      {beta beta' : NativeK5StructuralFourCell p h k}
      (allowed : allowTarget = true)
      (w : NativeK5StructuralFiveCell p alpha alpha')
      (v : NativeK5StructuralFiveCell p beta beta') :
      NativeK5SquarePolicySixCell allowTarget allowSource p
        (NativeK5StructuralFiveCell.targetSquareLeftThenRight w v)
        (NativeK5StructuralFiveCell.targetSquareRightThenLeft w v)
  | horizontalSourceSquare
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {h k : NativeF55StructuralComparison p s t}
      {alpha alpha' : NativeK5StructuralFourCell p f g}
      {beta beta' : NativeK5StructuralFourCell p h k}
      (allowed : allowSource = true)
      (w : NativeK5StructuralFiveCell p alpha alpha')
      (v : NativeK5StructuralFiveCell p beta beta') :
      NativeK5SquarePolicySixCell allowTarget allowSource p
        (NativeK5StructuralFiveCell.sourceSquareLeftThenRight w v)
        (NativeK5StructuralFiveCell.sourceSquareRightThenLeft w v)
  | symm
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      (u : NativeK5SquarePolicySixCell allowTarget allowSource p w z) :
      NativeK5SquarePolicySixCell allowTarget allowSource p z w
  | trans
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z q : NativeK5StructuralFiveCell p alpha beta}
      (u : NativeK5SquarePolicySixCell allowTarget allowSource p w z)
      (v : NativeK5SquarePolicySixCell allowTarget allowSource p z q) :
      NativeK5SquarePolicySixCell allowTarget allowSource p w q
  | verticalLeft
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta gamma : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      (u : NativeK5SquarePolicySixCell allowTarget allowSource p w z)
      (v : NativeK5StructuralFiveCell p beta gamma) :
      NativeK5SquarePolicySixCell allowTarget allowSource p
        (.trans w v) (.trans z v)
  | verticalRight
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta gamma : NativeK5StructuralFourCell p f g}
      (w : NativeK5StructuralFiveCell p alpha beta)
      {v z : NativeK5StructuralFiveCell p beta gamma}
      (u : NativeK5SquarePolicySixCell allowTarget allowSource p v z) :
      NativeK5SquarePolicySixCell allowTarget allowSource p
        (.trans w v) (.trans w z)
  | inverseRespect
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      (u : NativeK5SquarePolicySixCell allowTarget allowSource p w z) :
      NativeK5SquarePolicySixCell allowTarget allowSource p
        (.symm w) (.symm z)
  | precompose
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
      (prior : NativeF55StructuralComparison p r s)
      {f g : NativeF55StructuralComparison p s t}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      (u : NativeK5SquarePolicySixCell allowTarget allowSource p w z) :
      NativeK5SquarePolicySixCell allowTarget allowSource p
        (.precompose prior w) (.precompose prior z)
  | postcompose
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      (u : NativeK5SquarePolicySixCell allowTarget allowSource p w z)
      (suffix : NativeF55StructuralComparison p s t) :
      NativeK5SquarePolicySixCell allowTarget allowSource p
        (.postcompose w suffix) (.postcompose z suffix)

/-- Constructorwise inclusion of the optional-square source
presentation into the P94D3Z full dependent six-cell grammar. -/
def NativeK5SquarePolicySixCell.toFull
    {allowTarget allowSource : Bool}
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55StructuralComparison p r s}
    {alpha beta : NativeK5StructuralFourCell p f g}
    {w z : NativeK5StructuralFiveCell p alpha beta}
    (u : NativeK5SquarePolicySixCell allowTarget allowSource p w z) :
    NativeK5StructuralSixCell p w z := by
  induction u with
  | core witness => exact witness.toFull
  | interchangerLeftNaturality w beta =>
      exact .interchangerLeftNaturality w beta
  | interchangerRightNaturality alpha w =>
      exact .interchangerRightNaturality alpha w
  | horizontalTargetSquare _ w v => exact .horizontalTargetSquare w v
  | horizontalSourceSquare _ w v => exact .horizontalSourceSquare w v
  | symm _ ih => exact .symm ih
  | trans _ _ ih₁ ih₂ => exact .trans ih₁ ih₂
  | verticalLeft witness suffix ih => exact .verticalLeft ih suffix
  | verticalRight lead witness ih => exact .verticalRight lead ih
  | inverseRespect witness ih => exact .inverseRespect ih
  | precompose prior witness ih => exact .precompose prior ih
  | postcompose witness suffix ih => exact .postcompose ih suffix

/-- Cancellation on the LEFT by an original genuine five-cell
using nothing but the conservative 6D inverse/associativity/unit
relations and ordinary 6D congruence. -/
def NativeK5SquarePolicySixCell.cancelLeft
    {allowTarget allowSource : Bool}
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55StructuralComparison p r s}
    {alpha beta gamma : NativeK5StructuralFourCell p f g}
    (j : NativeK5StructuralFiveCell p alpha beta)
    {w z : NativeK5StructuralFiveCell p beta gamma}
    (u : NativeK5SquarePolicySixCell allowTarget allowSource p
      (.trans j w) (.trans j z)) :
    NativeK5SquarePolicySixCell allowTarget allowSource p w z := by
  exact .trans (.symm (.core (.verticalLeftUnit w)))
    (.trans (.verticalLeft (.symm (.core (.inverseRight j))) w)
      (.trans (.core (.verticalAssoc (.symm j) j w))
        (.trans (.verticalRight (.symm j) u)
          (.trans (.symm (.core (.verticalAssoc (.symm j) j z)))
            (.trans (.verticalLeft (.core (.inverseRight j)) z)
              (.core (.verticalLeftUnit z))))))

/-- Cancellation on the RIGHT by an original genuine five-cell.
No quotient equality is substituted for actual 6D evidence. -/
def NativeK5SquarePolicySixCell.cancelRight
    {allowTarget allowSource : Bool}
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55StructuralComparison p r s}
    {alpha beta gamma : NativeK5StructuralFourCell p f g}
    {w z : NativeK5StructuralFiveCell p alpha beta}
    (j : NativeK5StructuralFiveCell p beta gamma)
    (u : NativeK5SquarePolicySixCell allowTarget allowSource p
      (.trans w j) (.trans z j)) :
    NativeK5SquarePolicySixCell allowTarget allowSource p w z := by
  exact .trans (.symm (.core (.verticalRightUnit w)))
    (.trans (.verticalRight w (.symm (.core (.inverseLeft j))))
      (.trans (.symm (.core (.verticalAssoc w j (.symm j))))
        (.trans (.verticalLeft u (.symm j))
          (.trans (.core (.verticalAssoc z j (.symm j)))
            (.trans (.verticalRight z (.core (.inverseLeft j)))
              (.core (.verticalRightUnit z))))))

#print axioms NativeK5SquarePolicySixCell
#print axioms NativeK5SquarePolicySixCell.toFull
#print axioms NativeK5SquarePolicySixCell.cancelLeft
#print axioms NativeK5SquarePolicySixCell.cancelRight

end
end Kuu.F112.Physical
