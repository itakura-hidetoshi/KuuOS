import Kuu.F112.PolygonNativeC60PositiveContextSwitchObstruction

/-!
# F112-P94D3CJ — genuine C60 cross-context positive 16D no-go

CI proves that the actual target-first 15D AU proof after context w
cannot equal any source-first one in the SAME context.

CJ now proves that equalities of BOTH exact raw 14D endpoints of
any two contextual AU naturality pairs force equality of their entire
finite context words, even when the underlying original fourteen-cell
inputs differ. This avoids any assumption that a source or target
boundary alone uniquely decodes its context.

The proof uses two *original raw* (not scalar/group) constructor-spine
depths:
  * left depth of the common AU starting 14D boundary;
  * right depth of the common AU ending 14D boundary.
Together their fingerprints recover each outermost genuine 14D frame
(left, right, or no frame), and literal injectivity of the original
dependent 14D constructors recursively recovers the entire word.

Consequently:
  1. NO target-first 15D AU term can equal ANY source-first AU term
     under ANY two finite real C60 AQ contexts.
  2. There are NO TWO COMPOSABLE positive primitive BC 16D generators
     anywhere in the selected context-closed optional presentation.
  3. A positive native C60 chain cannot have length two or more.
  4. In particular, NO four-independent-positive-edge CF diamond
     exists for this selected native C60 BC signature.

There remain genuine single positive edges, mixed-sign zigzags, and
the AU triangle from CF. Nothing is asserted about a DIFFERENT
presentation of geometric 16D fillers, Gray, global horizontal Peiffer,
P92B, or strict 3/n and infinity-hyperdescent.
No new axioms, sorry or admit. All original 14D and 15D boundaries remain.
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

/-- Right-spine depth in the ORIGINAL dependent 14D constructor tree.
CI's left depth and this right depth jointly detect actual context
wrapping at both original AU naturality boundaries. -/
def nativeK5CJFourteenRightDepth
    {A B : NativeK5StructuralThirteenCell p U V} :
    NativeK5StructuralFourteenCell p A B → Nat
  | .trans _ following => nativeK5CJFourteenRightDepth following + 1
  | _ => 0

/-- The precise common original 14D starting boundary of AU
naturality's source-first and target-first 15D paths. -/
def nativeK5CJStart
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W) :
    NativeK5FifteenFourteenFiber W :=
  nativeK5AQWhiskerLeft W (nativeK5AQWhiskerRight W R)

/-- The precise common original 14D ending boundary of both
naturality paths, retaining the original dependent 13D indices. -/
def nativeK5CJFinish
    (W : NativeK5StructuralThirteenCell p U V)
    (S : NativeK5FifteenFourteenFiber W) :
    NativeK5FifteenFourteenFiber W :=
  nativeK5AQWhiskerRight W (nativeK5AQWhiskerLeft W S)

/-- A context-word fingerprint extracted from the left-spine of
the original START boundary. Unlike raw code serialization it can
be computed without knowing the arbitrary input 14D witness. -/
def nativeK5CJStartLeftFingerprint
    (W : NativeK5StructuralThirteenCell p U V) : List Bool → Nat
  | [] => nativeK5BLFourteenLeftDepth (nativeK5AQLeftFrame W) + 1
  | true :: _ => nativeK5BLFourteenLeftDepth (nativeK5AQLeftFrame W) + 1
  | false :: rest => nativeK5CJStartLeftFingerprint W rest + 1

/-- The dual original END-boundary right-spine fingerprint. -/
def nativeK5CJFinishRightFingerprint
    (W : NativeK5StructuralThirteenCell p U V) : List Bool → Nat
  | [] => nativeK5CJFourteenRightDepth (nativeK5AQRightFrame W) + 1
  | true :: rest => nativeK5CJFinishRightFingerprint W rest + 1
  | false :: _ => nativeK5CJFourteenRightDepth (nativeK5AQRightFrame W) + 1

/-- Exact interpretation of the START fingerprint in every finite
original dependent 14D AQ context, for EVERY original raw input. -/
theorem nativeK5CJStart_left_fingerprint
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool) (R : NativeK5FifteenFourteenFiber W) :
    nativeK5BLFourteenLeftDepth
      (nativeK5AQContext W word (nativeK5CJStart W R)) =
    nativeK5CJStartLeftFingerprint W word := by
  induction word with
  | nil => rfl
  | cons side rest ih =>
      cases side with
      | false =>
          change nativeK5BLFourteenLeftDepth
              (nativeK5AQContext W rest (nativeK5CJStart W R)) + 1 =
              nativeK5CJStartLeftFingerprint W rest + 1
          exact congrArg (fun n : Nat => n + 1) ih
      | true => rfl

/-- Exact interpretation of END's dual right-spine fingerprint. -/
theorem nativeK5CJFinish_right_fingerprint
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool) (S : NativeK5FifteenFourteenFiber W) :
    nativeK5CJFourteenRightDepth
      (nativeK5AQContext W word (nativeK5CJFinish W S)) =
    nativeK5CJFinishRightFingerprint W word := by
  induction word with
  | nil => rfl
  | cons side rest ih =>
      cases side with
      | false => rfl
      | true =>
          change nativeK5CJFourteenRightDepth
              (nativeK5AQContext W rest (nativeK5CJFinish W S)) + 1 =
              nativeK5CJFinishRightFingerprint W rest + 1
          exact congrArg (fun n : Nat => n + 1) ih

theorem nativeK5CJStart_left_lower
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool) :
    nativeK5BLFourteenLeftDepth (nativeK5AQLeftFrame W) + 1 ≤
      nativeK5CJStartLeftFingerprint W word := by
  induction word with
  | nil => exact le_refl _
  | cons side rest ih =>
      cases side with
      | false =>
          change nativeK5BLFourteenLeftDepth (nativeK5AQLeftFrame W) + 1 ≤
            nativeK5CJStartLeftFingerprint W rest + 1
          omega
      | true => exact le_refl _

theorem nativeK5CJFinish_right_lower
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool) :
    nativeK5CJFourteenRightDepth (nativeK5AQRightFrame W) + 1 ≤
      nativeK5CJFinishRightFingerprint W word := by
  induction word with
  | nil => exact le_refl _
  | cons side rest ih =>
      cases side with
      | false => exact le_refl _
      | true =>
          change nativeK5CJFourteenRightDepth (nativeK5AQRightFrame W) + 1 ≤
            nativeK5CJFinishRightFingerprint W rest + 1
          omega

/-- The pair of raw-spine fingerprints recovers the OUTER
context frame (or the absence of any frame). It is deliberately
not claimed to recover the entire word from numbers alone. -/
def nativeK5CJDecodeOuter
    (W : NativeK5StructuralThirteenCell p U V)
    (left right : Nat) : Option Bool :=
  if nativeK5BLFourteenLeftDepth (nativeK5AQLeftFrame W) + 1 < left
    then some false
  else if nativeK5CJFourteenRightDepth (nativeK5AQRightFrame W) + 1 < right
    then some true
  else none

theorem nativeK5CJDecodeOuter_correct
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool) :
    nativeK5CJDecodeOuter W
      (nativeK5CJStartLeftFingerprint W word)
      (nativeK5CJFinishRightFingerprint W word) = word.head? := by
  cases word with
  | nil =>
      simp [nativeK5CJDecodeOuter, nativeK5CJStartLeftFingerprint,
        nativeK5CJFinishRightFingerprint]
  | cons side rest =>
      cases side with
      | false =>
          have hlow := nativeK5CJStart_left_lower W rest
          have hlt : nativeK5BLFourteenLeftDepth (nativeK5AQLeftFrame W) + 1 <
              nativeK5CJStartLeftFingerprint W rest + 1 := by omega
          change (if nativeK5BLFourteenLeftDepth (nativeK5AQLeftFrame W) + 1 <
              nativeK5CJStartLeftFingerprint W rest + 1 then some false
              else if nativeK5CJFourteenRightDepth (nativeK5AQRightFrame W) + 1 <
                nativeK5CJFourteenRightDepth (nativeK5AQRightFrame W) + 1
                then some true else none) = some false
          simp only [if_pos hlt]
      | true =>
          have hlow := nativeK5CJFinish_right_lower W rest
          have hlt : nativeK5CJFourteenRightDepth (nativeK5AQRightFrame W) + 1 <
              nativeK5CJFinishRightFingerprint W rest + 1 := by omega
          change (if nativeK5BLFourteenLeftDepth (nativeK5AQLeftFrame W) + 1 <
              nativeK5BLFourteenLeftDepth (nativeK5AQLeftFrame W) + 1
              then some false
              else if nativeK5CJFourteenRightDepth (nativeK5AQRightFrame W) + 1 <
                nativeK5CJFinishRightFingerprint W rest + 1
                then some true else none) = some true
          simp only [lt_irrefl, if_false, if_pos hlt]

/-- TWO original dependent fourteen-dimensional equalities, one at
each end of the AU square, force equality of outer context markers.
A single endpoint equality is deliberately insufficient. -/
theorem nativeK5CJHead_eq_of_both_boundaries
    (W : NativeK5StructuralThirteenCell p U V)
    (xs ys : List Bool)
    (R S R' S' : NativeK5FifteenFourteenFiber W)
    (hs : nativeK5AQContext W xs (nativeK5CJStart W R) =
      nativeK5AQContext W ys (nativeK5CJStart W R'))
    (ht : nativeK5AQContext W xs (nativeK5CJFinish W S) =
      nativeK5AQContext W ys (nativeK5CJFinish W S')) :
    xs.head? = ys.head? := by
  have hl : nativeK5CJStartLeftFingerprint W xs =
      nativeK5CJStartLeftFingerprint W ys := by
    calc
      _ = nativeK5BLFourteenLeftDepth
          (nativeK5AQContext W xs (nativeK5CJStart W R)) :=
        (nativeK5CJStart_left_fingerprint W xs R).symm
      _ = nativeK5BLFourteenLeftDepth
          (nativeK5AQContext W ys (nativeK5CJStart W R')) :=
        congrArg (fun z : NativeK5FifteenFourteenFiber W =>
          nativeK5BLFourteenLeftDepth z) hs
      _ = _ := nativeK5CJStart_left_fingerprint W ys R'
  have hr : nativeK5CJFinishRightFingerprint W xs =
      nativeK5CJFinishRightFingerprint W ys := by
    calc
      _ = nativeK5CJFourteenRightDepth
          (nativeK5AQContext W xs (nativeK5CJFinish W S)) :=
        (nativeK5CJFinish_right_fingerprint W xs S).symm
      _ = nativeK5CJFourteenRightDepth
          (nativeK5AQContext W ys (nativeK5CJFinish W S')) :=
        congrArg (fun z : NativeK5FifteenFourteenFiber W =>
          nativeK5CJFourteenRightDepth z) ht
      _ = _ := nativeK5CJFinish_right_fingerprint W ys S'
  calc
    xs.head? = nativeK5CJDecodeOuter W
        (nativeK5CJStartLeftFingerprint W xs)
        (nativeK5CJFinishRightFingerprint W xs) :=
      (nativeK5CJDecodeOuter_correct W xs).symm
    _ = nativeK5CJDecodeOuter W
        (nativeK5CJStartLeftFingerprint W ys)
        (nativeK5CJFinishRightFingerprint W ys) := by rw [hl, hr]
    _ = ys.head? := nativeK5CJDecodeOuter_correct W ys

/-- COMPLETE raw cross-context rigidity: the PAIR of ORIGINAL
14D endpoints determines the whole finite AQ context word. Individual
frame constructors can then be cancelled by CI's raw injectivity,
and the argument descends recursively along their original trees. -/
theorem nativeK5CJContext_words_unique
    (W : NativeK5StructuralThirteenCell p U V) :
    ∀ (xs ys : List Bool)
      (R S R' S' : NativeK5FifteenFourteenFiber W),
      nativeK5AQContext W xs (nativeK5CJStart W R) =
        nativeK5AQContext W ys (nativeK5CJStart W R') →
      nativeK5AQContext W xs (nativeK5CJFinish W S) =
        nativeK5AQContext W ys (nativeK5CJFinish W S') →
      xs = ys := by
  intro xs
  induction xs with
  | nil =>
      intro ys R S R' S' hs ht
      have hh := nativeK5CJHead_eq_of_both_boundaries
        W [] ys R S R' S' hs ht
      cases ys with
      | nil => rfl
      | cons side rest => cases hh
  | cons side rest ih =>
      intro ys R S R' S' hs ht
      have hh := nativeK5CJHead_eq_of_both_boundaries
        W (side :: rest) ys R S R' S' hs ht
      cases ys with
      | nil => cases hh
      | cons side' rest' =>
          have hside : side = side' := by
            change some side = some side' at hh
            exact Option.some.inj hh
          cases hside
          have hs' : nativeK5AQContext W rest (nativeK5CJStart W R) =
              nativeK5AQContext W rest' (nativeK5CJStart W R') := by
            apply nativeK5CIWhisker_injective W side
            exact hs
          have ht' : nativeK5AQContext W rest (nativeK5CJFinish W S) =
              nativeK5AQContext W rest' (nativeK5CJFinish W S') := by
            apply nativeK5CIWhisker_injective W side
            exact ht
          exact congrArg (List.cons side) (ih rest' R S R' S' hs' ht')

/-- Equality of actual 15D target-first and source-first AU proofs
would force equality of BOTH context words. The witness equality,
not a Peiffer shadow, supplies both raw 14D endpoint equalities. -/
theorem nativeK5CJTarget_source_forces_word_eq
    (W : NativeK5StructuralThirteenCell p U V)
    (xs ys : List Bool)
    {R S R' S' : NativeK5FifteenFourteenFiber W}
    (firstCell : NativeK5AQFifteenCell W R S)
    (secondCell : NativeK5AQFifteenCell W R' S')
    (h : nativeK5CHTarget W xs firstCell =
      nativeK5CHSource W ys secondCell) :
    xs = ys := by
  have hs := congrArg (fun x : (nativeK5AXBaseLayer W).Total =>
    x.1.1.down) h
  have ht := congrArg (fun x : (nativeK5AXBaseLayer W).Total =>
    x.1.2.down) h
  unfold nativeK5CHTarget nativeK5CHSource at hs ht
  rw [nativeK5BCContext_pack W xs _, nativeK5BCContext_pack W ys _] at hs ht
  change nativeK5AQContext W xs (nativeK5CJStart W R) =
    nativeK5AQContext W ys (nativeK5CJStart W R') at hs
  change nativeK5AQContext W xs (nativeK5CJFinish W S) =
    nativeK5AQContext W ys (nativeK5CJFinish W S') at ht
  exact nativeK5CJContext_words_unique W xs ys R S R' S' hs ht

/-- Global no-go in the selected BC presentation. Even a conservative
15D input cannot bridge target-first to source-first under DIFFERENT
actual finite C60 contexts: equality would force the SAME context,
contradicting CI's strict original-midpoint inequality. -/
theorem nativeK5CJAll_contexts_target_source_ne
    (W : NativeK5StructuralThirteenCell p U V)
    (xs ys : List Bool)
    {R S R' S' : NativeK5FifteenFourteenFiber W}
    (firstCell : NativeK5AQFifteenCell W R S)
    (secondCell : NativeK5AQFifteenCell W R' S') :
    nativeK5CHTarget W xs firstCell ≠
      nativeK5CHSource W ys secondCell := by
  intro h
  have hw := nativeK5CJTarget_source_forces_word_eq
    W xs ys firstCell secondCell h
  subst ys
  exact nativeK5CISame_context_target_source_ne
    W xs firstCell secondCell h

/-- Complete positive-successor obstruction, for ANY source proof,
including conservative, exchange, symm and trans constructors. -/
theorem nativeK5CJNo_positive_successor
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S)
    (next : (nativeK5AXBaseLayer W).Total) :
    ¬ Nonempty ((nativeK5BCSignature W).Gen
      (nativeK5CHTarget W word cell) next) := by
  intro h
  obtain ⟨outer, R', S', following, hsrc, _⟩ :=
    (nativeK5CHSuccessor_iff_boundary_certificate W word cell next).mp h
  exact nativeK5CJAll_contexts_target_source_ne
    W word outer cell following hsrc

/-- The no-go propagates to arbitrarily long nonempty oriented tails.
It does NOT prohibit the true inverse-generators used in mixed paths. -/
theorem nativeK5CJNo_nonempty_positive_tail
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S)
    (next : (nativeK5AXBaseLayer W).Total)
    (tail : List (nativeK5AXBaseLayer W).Total) :
    ¬ Nonempty (NativeC60BZPositiveChain
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
      (nativeK5CHTarget W word cell) (next :: tail)) := by
  rintro ⟨chain⟩
  cases chain with
  | cons g _ =>
      exact nativeK5CJNo_positive_successor W word cell next ⟨g⟩

/-- In particular TWO ARBITRARY context-closed BC positive primitives
can NEVER compose in this chosen physical signature. The declared 16D
edges themselves remain nonempty. -/
theorem nativeK5CJNo_composable_positive_generators
    (W : NativeK5StructuralThirteenCell p U V)
    {source middle target : (nativeK5AXBaseLayer W).Total}
    (firstGen : (nativeK5BCSignature W).Gen source middle) :
    ¬ Nonempty ((nativeK5BCSignature W).Gen middle target) := by
  intro h
  rcases firstGen with ⟨word, a, b, ⟨g, hsrc, htgt⟩⟩
  rcases g with ⟨R, S, cell, ha, hb⟩
  have hmid : middle = nativeK5CHTarget W word cell := by
    calc
      middle = nativeK5BCContext W word b := htgt
      _ = nativeK5CHTarget W word cell :=
        congrArg (nativeK5BCContext W word) hb
  rw [hmid] at h
  exact nativeK5CJNo_positive_successor W word cell target h

/-- No native positive two-edge chain with arbitrary original typed
15D middle cells, regardless of its two independently chosen contexts. -/
theorem nativeK5CJNo_two_step_positive_chain
    (W : NativeK5StructuralThirteenCell p U V)
    (source middle target : (nativeK5AXBaseLayer W).Total)
    (tail : List (nativeK5AXBaseLayer W).Total) :
    ¬ Nonempty (NativeC60BZPositiveChain
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
      source (middle :: target :: tail)) := by
  rintro ⟨chain⟩
  cases chain with
  | cons g rest =>
      cases rest with
      | cons h _ =>
          exact nativeK5CJNo_composable_positive_generators W g ⟨h⟩

/-- Consequently there is NO genuine four-independent-positive-edge
CF diamond anywhere in this selected original-C60 BC presentation.
The earlier CF conditional free-holonomy criterion remains valid,
and mixed-sign triangles remain genuine. -/
theorem nativeK5CJNo_positive_four_edge_diamond
    (W : NativeK5StructuralThirteenCell p U V) :
    ¬ Nonempty (NativeC60CFTypedDiamond
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)) := by
  rintro ⟨q⟩
  exact nativeK5CJNo_composable_positive_generators W
    q.leftFirst ⟨q.leftSecond⟩

end PhysicalC60

#print axioms nativeK5CJStart_left_fingerprint
#print axioms nativeK5CJFinish_right_fingerprint
#print axioms nativeK5CJStart_left_lower
#print axioms nativeK5CJFinish_right_lower
#print axioms nativeK5CJDecodeOuter_correct
#print axioms nativeK5CJHead_eq_of_both_boundaries
#print axioms nativeK5CJContext_words_unique
#print axioms nativeK5CJTarget_source_forces_word_eq
#print axioms nativeK5CJAll_contexts_target_source_ne
#print axioms nativeK5CJNo_positive_successor
#print axioms nativeK5CJNo_nonempty_positive_tail
#print axioms nativeK5CJNo_composable_positive_generators
#print axioms nativeK5CJNo_two_step_positive_chain
#print axioms nativeK5CJNo_positive_four_edge_diamond

end
end Kuu.F112.Physical
