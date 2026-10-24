import Kuu.F112.PolygonNativeF55P94DK5TypedFiveCellHorizontalNaturality
import Mathlib.Tactic

/-!
# F112-P94D3Z — source-typed 6-cell naturality cube

Construct the two dependent FIVE-cell paths for each choice of
interchanger naturality and for both binary horizontal squares.

Then explicitly adjoin a NEW dependent six-cell presentation:
source-typed 6D interchange-naturalities and both squares, plus
the proof-relevant six-cell vertical pasting/reversal/congruences,
five-cell associator, unit and inverse fillers and original 3-cell
whiskerings. NONE of these generators is claimed to follow from
mere universal Peiffer equality or the previous five-cell grammar.

The MIXED two-variable naturality cube, by contrast, is DERIVED
as a composite of two exact six-cell naturality generators and
six-cell vertical associativity/whiskering, not postulated afresh.
No old P92B descent, global strict 3/n coherence, hyperdescent,
Gray, sorry/admit, new logical axioms or root/C60 deletion.
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

section NaturalityPaths

variable {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable {first : KuuNativeF45Tree p n m ma pa mb pb}
variable {last : KuuNativeF45Tree p n' m' ma pa mb pb}
variable {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
variable {f g : NativeF55StructuralComparison p r s}
variable {h k : NativeF55StructuralComparison p s t}

/-- Left naturality: first transport the 4-cell, then interchange. -/
def NativeK5StructuralFiveCell.interchangerLeftPathTarget
    {alpha alpha' : NativeK5StructuralFourCell p f g}
    (w : NativeK5StructuralFiveCell p alpha alpha')
    (beta : NativeK5StructuralFourCell p h k) :
    NativeK5StructuralFiveCell p
      (alpha.horizontalViaTarget beta)
      (alpha'.horizontalViaSource beta) :=
  .trans (.horizontalViaTarget_left w beta) (nativeK5TypedInterchanger alpha' beta)

/-- Left naturality: first interchange, then transport the 4-cell. -/
def NativeK5StructuralFiveCell.interchangerLeftPathSource
    {alpha alpha' : NativeK5StructuralFourCell p f g}
    (w : NativeK5StructuralFiveCell p alpha alpha')
    (beta : NativeK5StructuralFourCell p h k) :
    NativeK5StructuralFiveCell p
      (alpha.horizontalViaTarget beta)
      (alpha'.horizontalViaSource beta) :=
  .trans (nativeK5TypedInterchanger alpha beta) (.horizontalViaSource_left w beta)

/-- Right naturality: first transport the right 4-cell. -/
def NativeK5StructuralFiveCell.interchangerRightPathTarget
    (alpha : NativeK5StructuralFourCell p f g)
    {beta beta' : NativeK5StructuralFourCell p h k}
    (w : NativeK5StructuralFiveCell p beta beta') :
    NativeK5StructuralFiveCell p
      (alpha.horizontalViaTarget beta)
      (alpha.horizontalViaSource beta') :=
  .trans (.horizontalViaTarget_right alpha w) (nativeK5TypedInterchanger alpha beta')

/-- Right naturality: first interchange, then transport. -/
def NativeK5StructuralFiveCell.interchangerRightPathSource
    (alpha : NativeK5StructuralFourCell p f g)
    {beta beta' : NativeK5StructuralFourCell p h k}
    (w : NativeK5StructuralFiveCell p beta beta') :
    NativeK5StructuralFiveCell p
      (alpha.horizontalViaTarget beta)
      (alpha.horizontalViaSource beta') :=
  .trans (nativeK5TypedInterchanger alpha beta) (.horizontalViaSource_right alpha w)

/-- Both orders of two source-typed 5-cell changes at the
target-ordered horizontal 4-cell composite. -/
def NativeK5StructuralFiveCell.targetSquareLeftThenRight
    {alpha alpha' : NativeK5StructuralFourCell p f g}
    {beta beta' : NativeK5StructuralFourCell p h k}
    (w : NativeK5StructuralFiveCell p alpha alpha')
    (v : NativeK5StructuralFiveCell p beta beta') :
    NativeK5StructuralFiveCell p
      (alpha.horizontalViaTarget beta)
      (alpha'.horizontalViaTarget beta') :=
  .trans (.horizontalViaTarget_left w beta) (.horizontalViaTarget_right alpha' v)

def NativeK5StructuralFiveCell.targetSquareRightThenLeft
    {alpha alpha' : NativeK5StructuralFourCell p f g}
    {beta beta' : NativeK5StructuralFourCell p h k}
    (w : NativeK5StructuralFiveCell p alpha alpha')
    (v : NativeK5StructuralFiveCell p beta beta') :
    NativeK5StructuralFiveCell p
      (alpha.horizontalViaTarget beta)
      (alpha'.horizontalViaTarget beta') :=
  .trans (.horizontalViaTarget_right alpha v) (.horizontalViaTarget_left w beta')

/-- Both orders of two 5-cell changes at the independent
source-ordered horizontal 4-cell composite. -/
def NativeK5StructuralFiveCell.sourceSquareLeftThenRight
    {alpha alpha' : NativeK5StructuralFourCell p f g}
    {beta beta' : NativeK5StructuralFourCell p h k}
    (w : NativeK5StructuralFiveCell p alpha alpha')
    (v : NativeK5StructuralFiveCell p beta beta') :
    NativeK5StructuralFiveCell p
      (alpha.horizontalViaSource beta)
      (alpha'.horizontalViaSource beta') :=
  .trans (.horizontalViaSource_left w beta) (.horizontalViaSource_right alpha' v)

def NativeK5StructuralFiveCell.sourceSquareRightThenLeft
    {alpha alpha' : NativeK5StructuralFourCell p f g}
    {beta beta' : NativeK5StructuralFourCell p h k}
    (w : NativeK5StructuralFiveCell p alpha alpha')
    (v : NativeK5StructuralFiveCell p beta beta') :
    NativeK5StructuralFiveCell p
      (alpha.horizontalViaSource beta)
      (alpha'.horizontalViaSource beta') :=
  .trans (.horizontalViaSource_right alpha v) (.horizontalViaSource_left w beta')

end NaturalityPaths

/-- An INDEPENDENT Type-valued 6-cell presentation between
actual 5-cell evidence terms with identical dependent boundaries. -/
inductive NativeK5StructuralSixCell (p : Polygon) :
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
  | refl
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      (w : NativeK5StructuralFiveCell p alpha beta) :
      NativeK5StructuralSixCell p w w
  | symm
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      (u : NativeK5StructuralSixCell p w z) :
      NativeK5StructuralSixCell p z w
  | trans
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z q : NativeK5StructuralFiveCell p alpha beta}
      (u : NativeK5StructuralSixCell p w z)
      (v : NativeK5StructuralSixCell p z q) :
      NativeK5StructuralSixCell p w q
  | verticalLeft
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta gamma : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      (u : NativeK5StructuralSixCell p w z)
      (v : NativeK5StructuralFiveCell p beta gamma) :
      NativeK5StructuralSixCell p (.trans w v) (.trans z v)
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
      (u : NativeK5StructuralSixCell p v z) :
      NativeK5StructuralSixCell p (.trans w v) (.trans w z)
  | verticalAssoc
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta gamma delta : NativeK5StructuralFourCell p f g}
      (w : NativeK5StructuralFiveCell p alpha beta)
      (v : NativeK5StructuralFiveCell p beta gamma)
      (z : NativeK5StructuralFiveCell p gamma delta) :
      NativeK5StructuralSixCell p
        (.trans (.trans w v) z) (.trans w (.trans v z))
  | verticalLeftUnit
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      (w : NativeK5StructuralFiveCell p alpha beta) :
      NativeK5StructuralSixCell p (.trans (.refl alpha) w) w
  | verticalRightUnit
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      (w : NativeK5StructuralFiveCell p alpha beta) :
      NativeK5StructuralSixCell p (.trans w (.refl beta)) w
  | inverseLeft
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      (w : NativeK5StructuralFiveCell p alpha beta) :
      NativeK5StructuralSixCell p (.trans w (.symm w)) (.refl alpha)
  | inverseRight
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      (w : NativeK5StructuralFiveCell p alpha beta) :
      NativeK5StructuralSixCell p (.trans (.symm w) w) (.refl beta)
  | inverseRespect
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      (u : NativeK5StructuralSixCell p w z) :
      NativeK5StructuralSixCell p (.symm w) (.symm z)
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
      NativeK5StructuralSixCell p
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
      NativeK5StructuralSixCell p
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
      (w : NativeK5StructuralFiveCell p alpha alpha')
      (v : NativeK5StructuralFiveCell p beta beta') :
      NativeK5StructuralSixCell p
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
      (w : NativeK5StructuralFiveCell p alpha alpha')
      (v : NativeK5StructuralFiveCell p beta beta') :
      NativeK5StructuralSixCell p
        (NativeK5StructuralFiveCell.sourceSquareLeftThenRight w v)
        (NativeK5StructuralFiveCell.sourceSquareRightThenLeft w v)
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
      (u : NativeK5StructuralSixCell p w z) :
      NativeK5StructuralSixCell p (.precompose prior w) (.precompose prior z)
  | postcompose
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      {alpha beta : NativeK5StructuralFourCell p f g}
      {w z : NativeK5StructuralFiveCell p alpha beta}
      (u : NativeK5StructuralSixCell p w z)
      (suffix : NativeF55StructuralComparison p s t) :
      NativeK5StructuralSixCell p (.postcompose w suffix) (.postcompose z suffix)

section MixedSixCell

variable {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable {first : KuuNativeF45Tree p n m ma pa mb pb}
variable {last : KuuNativeF45Tree p n' m' ma pa mb pb}
variable {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
variable {f g : NativeF55StructuralComparison p r s}
variable {h k : NativeF55StructuralComparison p s t}

/-- A DERIVED six-dimensional mixed-naturality cube. The path on
the left changes BOTH four-cell variables before interchanging;
the path on the right interchanges first then changes BOTH.
The proof has five genuine source-typed 6-cell steps, not an
untyped word observer nor a new mixed cube generator. -/
def NativeK5StructuralSixCell.interchangerMixedNaturality
    {alpha alpha' : NativeK5StructuralFourCell p f g}
    {beta beta' : NativeK5StructuralFourCell p h k}
    (w : NativeK5StructuralFiveCell p alpha alpha')
    (v : NativeK5StructuralFiveCell p beta beta') :
    NativeK5StructuralSixCell p
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
  change NativeK5StructuralSixCell p (.trans (.trans a b) c)
    (.trans j (.trans e d))
  exact .trans (.verticalAssoc a b c)
    (.trans (.verticalRight a (.interchangerRightNaturality alpha' v))
      (.trans (.symm (.verticalAssoc a i d))
        (.trans (.verticalLeft (.interchangerLeftNaturality w beta) d)
          (.verticalAssoc j e d))))

#print axioms NativeK5StructuralFiveCell.interchangerLeftPathTarget
#print axioms NativeK5StructuralFiveCell.interchangerLeftPathSource
#print axioms NativeK5StructuralFiveCell.interchangerRightPathTarget
#print axioms NativeK5StructuralFiveCell.interchangerRightPathSource
#print axioms NativeK5StructuralFiveCell.targetSquareLeftThenRight
#print axioms NativeK5StructuralFiveCell.targetSquareRightThenLeft
#print axioms NativeK5StructuralFiveCell.sourceSquareLeftThenRight
#print axioms NativeK5StructuralFiveCell.sourceSquareRightThenLeft
#print axioms NativeK5StructuralSixCell
#print axioms NativeK5StructuralSixCell.interchangerMixedNaturality

end MixedSixCell
end
end Kuu.F112.Physical
