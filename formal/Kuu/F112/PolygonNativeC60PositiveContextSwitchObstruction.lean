import Kuu.F112.PolygonNativeC60PositiveConnectivityClassification

/-!
# F112-P94D3CI — non-repeating context obstruction for consecutive positive BC 16-cells

CH classifies all original AQ 15D constructors by the outer syntactic
conservative tag. Its TRUE branch is only a necessary condition for a
second positively oriented BC primitive and leaves conservative inputs open.

CI retains the entire original dependent fourteen-cell tree and considers
the *first intermediate fourteen-cell* in the two AU 15D naturality routes.
At a fixed finite, genuine C60 14D context, a target-first route first
visits L ; (S ; R), while a source-first route first visits
(L ; R') ; R. These raw bracketings have different left-spine depths
for EVERY original S,R'. Finite *common* physical context is injective on
the original 14D syntax; it cannot erase the difference.

Consequently the target of ANY genuinely declared positive AU generator
can never equal the source of ANOTHER positive AU generator in the SAME
finite AQ context. This applies to conservative as well as exchange/symm/
trans input 15D cells. Any existing positive two-step path must switch
context words; each side of a genuine CF positive diamond must do so.

This theorem does NOT forbid successors in a *different* context or assert
that a geometric 16D diamond exists. No collapse of the raw 14D boundary,
new axioms, sorry/admit, Gray, or global strict-n structures.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uD vD uE vE

section PhysicalC60

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

/-- Extract the EXACT original 14D midpoint of the outermost typed
15D trans constructor, not an integer or a Peiffer shadow. -/
def nativeK5CIFirstMiddle
    (W : NativeK5StructuralThirteenCell p U V)
    {R S : NativeK5FifteenFourteenFiber W} :
    NativeK5AQFifteenCell W R S → Option (NativeK5FifteenFourteenFiber W)
  | .trans (y := middle) _ _ => some middle
  | _ => none

/-- The same original midpoint viewed as an observer of the fully
packed proof-relevant 15D object, preserving its dependent endpoints. -/
def nativeK5CIPackedMiddle
    (W : NativeK5StructuralThirteenCell p U V)
    (x : (nativeK5AXBaseLayer W).Total) :
    Option (NativeK5FifteenFourteenFiber W) :=
  nativeK5CIFirstMiddle W x.2.down

/-- The original single 14D frame transports the midpoint of each
trans 15D constructor without altering its top-level proof grammar. -/
theorem nativeK5CIFirstMiddle_whisker
    (W : NativeK5StructuralThirteenCell p U V)
    (side : Bool)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S) :
    nativeK5CIFirstMiddle W (nativeK5AQWhiskerCell W side cell) =
      (nativeK5CIFirstMiddle W cell).map (nativeK5AQWhisker W side) := by
  cases cell <;> rfl

/-- Midpoints commute with EVERY finite actual 14D context, without
forgetting the original 14D fiber or replacing it by a graph. -/
theorem nativeK5CIFirstMiddle_context
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S) :
    nativeK5CIFirstMiddle W (nativeK5AQContextCell W word cell) =
      (nativeK5CIFirstMiddle W cell).map (nativeK5AQContext W word) := by
  induction word with
  | nil =>
      cases nativeK5CIFirstMiddle W cell <;> rfl
  | cons side rest ih =>
      change nativeK5CIFirstMiddle W
          (nativeK5AQWhiskerCell W side (nativeK5AQContextCell W rest cell)) =
        (nativeK5CIFirstMiddle W cell).map
          (nativeK5AQContext W (side :: rest))
      rw [nativeK5CIFirstMiddle_whisker W side, ih]
      cases nativeK5CIFirstMiddle W cell <;> rfl

/-- In source-first AU naturality, the FIRST midpoint is the original
RIGHT-after-LEFT bracketing at the source 14D witness. -/
theorem nativeK5CISource_midpoint
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S) :
    nativeK5CIPackedMiddle W (nativeK5CHSource W word cell) =
      some (nativeK5AQContext W word
        (nativeK5AQWhiskerRight W (nativeK5AQWhiskerLeft W R))) := by
  unfold nativeK5CIPackedMiddle nativeK5CHSource
  rw [nativeK5BCContext_pack W word _]
  change nativeK5CIFirstMiddle W
      (nativeK5AQContextCell W word
        (nativeK5AUNaturalityViaSource W cell)) = _
  rw [nativeK5CIFirstMiddle_context W word]
  rfl

/-- In target-first AU naturality, the FIRST midpoint has the
opposite, original LEFT-after-RIGHT 14D bracketing at the target. -/
theorem nativeK5CITarget_midpoint
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S) :
    nativeK5CIPackedMiddle W (nativeK5CHTarget W word cell) =
      some (nativeK5AQContext W word
        (nativeK5AQWhiskerLeft W (nativeK5AQWhiskerRight W S))) := by
  unfold nativeK5CIPackedMiddle nativeK5CHTarget
  rw [nativeK5BCContext_pack W word _]
  change nativeK5CIFirstMiddle W
      (nativeK5AQContextCell W word
        (nativeK5AUNaturalityViaTarget W cell)) = _
  rw [nativeK5CIFirstMiddle_context W word]
  rfl

/-- The two opposite *original* 14D bracketings are unequal even
when their innermost fourteen-cell witnesses are independently chosen.
The previous BL theorem only required the special case of one common
witness. The left-spine depth distinguishes the GENERAL case. -/
theorem nativeK5CIOpposite_midpoints_raw_ne
    (W : NativeK5StructuralThirteenCell p U V)
    (R S : NativeK5FifteenFourteenFiber W) :
    nativeK5AQWhiskerLeft W (nativeK5AQWhiskerRight W S) ≠
      nativeK5AQWhiskerRight W (nativeK5AQWhiskerLeft W R) := by
  intro h
  have hd := congrArg
    (fun c : NativeK5FifteenFourteenFiber W =>
      nativeK5BLFourteenLeftDepth c) h
  change nativeK5BLFourteenLeftDepth (nativeK5AQLeftFrame W) + 1 =
    nativeK5BLFourteenLeftDepth (nativeK5AQLeftFrame W) + 1 + 1 at hd
  omega

/-- Each genuine original 14D left/right frame is individually
injective as a raw source-dependent proof-term constructor. -/
theorem nativeK5CIWhisker_injective
    (W : NativeK5StructuralThirteenCell p U V)
    (side : Bool) :
    Function.Injective (nativeK5AQWhisker W side) := by
  intro R S h
  cases side with
  | false =>
      change NativeK5StructuralFourteenCell.trans R
          (nativeK5AQRightFrame W) =
        NativeK5StructuralFourteenCell.trans S
          (nativeK5AQRightFrame W) at h
      injection h with hRS
  | true =>
      change NativeK5StructuralFourteenCell.trans
          (nativeK5AQLeftFrame W) R =
        NativeK5StructuralFourteenCell.trans
          (nativeK5AQLeftFrame W) S at h
      injection h with hRS

/-- Arbitrary finite physical AQ context retains injectivity on the
original 14D proof fiber. No group-valued collapse is used. -/
theorem nativeK5CIContext_injective
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool) :
    Function.Injective (nativeK5AQContext W word) := by
  induction word with
  | nil =>
      intro R S h
      exact h
  | cons side rest ih =>
      intro R S h
      apply ih
      exact nativeK5CIWhisker_injective W side h

/-- Every target-first AU term differs from every source-first AU term
constructed in the SAME finite original AQ context, for ANY two input
15D witnesses. No conservative/exchange/symm/trans distinction is
required, since their typed *first midpoints* remain different. -/
theorem nativeK5CISame_context_target_source_ne
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool)
    {R S R' S' : NativeK5FifteenFourteenFiber W}
    (firstCell : NativeK5AQFifteenCell W R S)
    (secondCell : NativeK5AQFifteenCell W R' S') :
    nativeK5CHTarget W word firstCell ≠
      nativeK5CHSource W word secondCell := by
  intro heq
  have hm := congrArg (nativeK5CIPackedMiddle W) heq
  rw [nativeK5CITarget_midpoint W word firstCell,
    nativeK5CISource_midpoint W word secondCell] at hm
  have hraw : nativeK5AQWhiskerLeft W
      (nativeK5AQWhiskerRight W S) =
        nativeK5AQWhiskerRight W
          (nativeK5AQWhiskerLeft W R') :=
    nativeK5CIContext_injective W word (Option.some.inj hm)
  exact nativeK5CIOpposite_midpoints_raw_ne W R' S hraw

/-- An actual outgoing positive BC primitive of any original AU target
must use a DIFFERENT finite 14D AQ context from that of the first edge.
This does not assert such an outgoing primitive exists. -/
theorem nativeK5CISuccessor_forces_context_change
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S)
    (next : (nativeK5AXBaseLayer W).Total)
    (hasNext : Nonempty ((nativeK5BCSignature W).Gen
      (nativeK5CHTarget W word cell) next)) :
    ∃ (outer : List Bool) (R' S' : NativeK5FifteenFourteenFiber W)
      (following : NativeK5AQFifteenCell W R' S'),
      outer ≠ word ∧
      nativeK5CHTarget W word cell =
        nativeK5CHSource W outer following ∧
      next = nativeK5CHTarget W outer following := by
  obtain ⟨outer, R', S', following, hsrc, htgt⟩ :=
    (nativeK5CHSuccessor_iff_boundary_certificate
      W word cell next).mp hasNext
  refine ⟨outer, R', S', following, ?_, hsrc, htgt⟩
  intro hword
  subst outer
  exact nativeK5CISame_context_target_source_ne W word cell following hsrc

/-- The actual context word is part of each genuine dependent BC
generator's data, not an independently guessed label. -/
def nativeK5CIWord
    (W : NativeK5StructuralThirteenCell p U V)
    {source target : (nativeK5AXBaseLayer W).Total}
    (g : (nativeK5BCSignature W).Gen source target) : List Bool :=
  g.1

/-- Two composable, genuinely positive 16D BC PRIMITIVES can never
carry the SAME actual 14D context word. This is unconditional for
the selected BC signature, including conservative inputs. -/
theorem nativeK5CIComposable_positive_words_ne
    (W : NativeK5StructuralThirteenCell p U V)
    {source middle target : (nativeK5AXBaseLayer W).Total}
    (firstGen : (nativeK5BCSignature W).Gen source middle)
    (secondGen : (nativeK5BCSignature W).Gen middle target) :
    nativeK5CIWord W firstGen ≠ nativeK5CIWord W secondGen := by
  rcases firstGen with ⟨word, a, b, ⟨g, hsrc, htgt⟩⟩
  rcases secondGen with ⟨outer, a', b', ⟨g', hsrc', htgt'⟩⟩
  rcases g with ⟨R, S, cell, ha, hb⟩
  rcases g' with ⟨R', S', following, ha', hb'⟩
  change word ≠ outer
  intro hs
  subst outer
  have hmid : nativeK5CHTarget W word cell =
      nativeK5CHSource W word following := by
    calc
      nativeK5CHTarget W word cell =
          nativeK5BCContext W word b :=
        (congrArg (nativeK5BCContext W word) hb).symm
      _ = middle := htgt.symm
      _ = nativeK5BCContext W word a' := hsrc'
      _ = nativeK5CHSource W word following :=
        congrArg (nativeK5BCContext W word) ha'
  exact nativeK5CISame_context_target_source_ne W word cell following hmid

/-- Every genuinely *four-positive-primitive* CF diamond, should one
exist with possibly distinct context words, is necessarily
alternating along BOTH original dependent middle-cell paths. -/
theorem nativeK5CIDiamond_each_leg_changes_context
    (W : NativeK5StructuralThirteenCell p U V)
    (q : NativeC60CFTypedDiamond
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)) :
    nativeK5CIWord W q.leftFirst ≠ nativeK5CIWord W q.leftSecond ∧
      nativeK5CIWord W q.rightFirst ≠ nativeK5CIWord W q.rightSecond :=
  ⟨nativeK5CIComposable_positive_words_ne W q.leftFirst q.leftSecond,
   nativeK5CIComposable_positive_words_ne W q.rightFirst q.rightSecond⟩

end PhysicalC60

#print axioms nativeK5CIFirstMiddle_whisker
#print axioms nativeK5CIFirstMiddle_context
#print axioms nativeK5CISource_midpoint
#print axioms nativeK5CITarget_midpoint
#print axioms nativeK5CIOpposite_midpoints_raw_ne
#print axioms nativeK5CIWhisker_injective
#print axioms nativeK5CIContext_injective
#print axioms nativeK5CISame_context_target_source_ne
#print axioms nativeK5CISuccessor_forces_context_change
#print axioms nativeK5CIComposable_positive_words_ne
#print axioms nativeK5CIDiamond_each_leg_changes_context

end
end Kuu.F112.Physical
