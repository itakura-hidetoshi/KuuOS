import Kuu.F112.PolygonNativeF55P94DK5PentagonatorSingleSquareMinimality
import Mathlib.Tactic

/-!
# F112-P94D3AD — independent signed provenance on genuine six-cell witnesses

P94D3AC proves that a single primitive horizontal-square family is
sufficient for *existence* of six-cell witnesses. It does NOT prove
that its derived witness is equal to the original six-cell proof.

Here preserve the genuine Type-valued dependent 5-cell source/target
indices while counting the TWO distinct primitive six-cell square
constructors in the OLD full P94D3Z six-cell syntax.

Signed provenance distinguishes the primitive target square from
the target square derived through source, and vice versa. Both
witnesses fill the EXACT SAME dependent five-cell boundaries.
No group word or four-cell Peiffer image is taken as proof equality.

Counts are primitive-constructor observations, not a claim that a
7D comparison exists without an additional presentation.
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

/-- Signed source/target SQUARE-GENERATOR provenance of original
source-typed SIX-cell proof syntax. Select the target or source
primitive square separately; all naturality and core constructors
are zero. This is a genuine *6D witness* observer, not a boundary
invariant of five-cells. -/
def NativeK5StructuralSixCell.squareProvenance
    (selectTarget : Bool)
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55StructuralComparison p r s}
    {alpha beta : NativeK5StructuralFourCell p f g}
    {w z : NativeK5StructuralFiveCell p alpha beta}
    (u : NativeK5StructuralSixCell p w z) : ℤ :=
  match u with
  | .refl _ => 0
  | .symm v => -v.squareProvenance selectTarget
  | .trans v q => v.squareProvenance selectTarget + q.squareProvenance selectTarget
  | .verticalLeft v _ => v.squareProvenance selectTarget
  | .verticalRight _ v => v.squareProvenance selectTarget
  | .verticalAssoc _ _ _ => 0
  | .verticalLeftUnit _ => 0
  | .verticalRightUnit _ => 0
  | .inverseLeft _ => 0
  | .inverseRight _ => 0
  | .inverseRespect v => -v.squareProvenance selectTarget
  | .interchangerLeftNaturality _ _ => 0
  | .interchangerRightNaturality _ _ => 0
  | .horizontalTargetSquare _ _ => if selectTarget then 1 else 0
  | .horizontalSourceSquare _ _ => if selectTarget then 0 else 1
  | .precompose _ v => v.squareProvenance selectTarget
  | .postcompose v _ => v.squareProvenance selectTarget

/-- Genuine direct source-typed target-square SIX-cell proof. -/
def nativeK5SixTargetSquareDirect
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
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
      (NativeK5StructuralFiveCell.targetSquareRightThenLeft w v) :=
  .horizontalTargetSquare w v

/-- The ALTERNATIVE full six-cell proof of the same TARGET
boundary, constructed by the old source-only policy, its two
naturality cubes and the actual six-cell right cancellation. -/
def nativeK5SixTargetSquareViaSource
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
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
      (NativeK5StructuralFiveCell.targetSquareRightThenLeft w v) :=
  (nativeK5SourceOnly_generatesTargetSquare w v).toFull

/-- Genuine direct source-typed SOURCE-square SIX-cell witness. -/
def nativeK5SixSourceSquareDirect
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
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
      (NativeK5StructuralFiveCell.sourceSquareRightThenLeft w v) :=
  .horizontalSourceSquare w v

/-- Alternative full SOURCE-square 6D proof derived ONLY from
the target square, two naturality cubes and left cancellation. -/
def nativeK5SixSourceSquareViaTarget
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
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
      (NativeK5StructuralFiveCell.sourceSquareRightThenLeft w v) :=
  (nativeK5TargetOnly_generatesSourceSquare w v).toFull

/-- EXACT 6D primitive-generator provenance on TWO parallel
genuine target-square SIX-cell proofs. One chooses target, the
other instead uses source. No raw equality is asserted. -/
theorem nativeK5TargetSquare_sixProvenance
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
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
    (nativeK5SixTargetSquareDirect w v).squareProvenance true = 1 ∧
    (nativeK5SixTargetSquareViaSource w v).squareProvenance true = 0 ∧
    (nativeK5SixTargetSquareDirect w v).squareProvenance false = 0 ∧
    (nativeK5SixTargetSquareViaSource w v).squareProvenance false = 1 := by
  exact ⟨rfl, rfl, rfl, rfl⟩

/-- EXACT complementary provenance for the genuine SOURCE-square
pair of 6D witnesses. -/
theorem nativeK5SourceSquare_sixProvenance
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
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
    (nativeK5SixSourceSquareDirect w v).squareProvenance true = 0 ∧
    (nativeK5SixSourceSquareViaTarget w v).squareProvenance true = 1 ∧
    (nativeK5SixSourceSquareDirect w v).squareProvenance false = 1 ∧
    (nativeK5SixSourceSquareViaTarget w v).squareProvenance false = 0 := by
  exact ⟨rfl, rfl, rfl, rfl⟩

/-- Two genuine same-boundary target six-cell proofs are NEVER
judgmentally/propositionally equal as RAW freely generated 6D
terms. They will require separate 7D comparison evidence. -/
theorem nativeK5TargetSquare_sixRaw_ne
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
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
    nativeK5SixTargetSquareDirect w v ≠
      nativeK5SixTargetSquareViaSource w v := by
  intro heq
  have hc := congrArg
    (fun t => NativeK5StructuralSixCell.squareProvenance true t) heq
  change (1 : ℤ) = 0 at hc
  norm_num at hc

/-- The complementary source six-cell comparison is equally
NOT an equality of raw Type-valued higher evidence terms. -/
theorem nativeK5SourceSquare_sixRaw_ne
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
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
    nativeK5SixSourceSquareDirect w v ≠
      nativeK5SixSourceSquareViaTarget w v := by
  intro heq
  have hc := congrArg
    (fun t => NativeK5StructuralSixCell.squareProvenance false t) heq
  change (1 : ℤ) = 0 at hc
  norm_num at hc

#print axioms NativeK5StructuralSixCell.squareProvenance
#print axioms nativeK5SixTargetSquareDirect
#print axioms nativeK5SixTargetSquareViaSource
#print axioms nativeK5SixSourceSquareDirect
#print axioms nativeK5SixSourceSquareViaTarget
#print axioms nativeK5TargetSquare_sixProvenance
#print axioms nativeK5SourceSquare_sixProvenance
#print axioms nativeK5TargetSquare_sixRaw_ne
#print axioms nativeK5SourceSquare_sixRaw_ne

end
end Kuu.F112.Physical
