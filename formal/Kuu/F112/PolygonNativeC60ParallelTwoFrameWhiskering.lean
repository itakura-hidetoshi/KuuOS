import Kuu.F112.PolygonNativeC60PhysicalParallelBoundaryNoGo

/-!
# F112-P94D3BL — two independent physical frames on parallel AU comparisons

The ACTUAL source and target of AU naturality are distinct raw 15D terms
with IDENTICAL original 14D boundaries. BC gives a typed 16D comparison
only because that explicit presentation adjoins the AU generator.

For this restricted, nontrivial parallel pair we construct a TWO-PARAMETER
action of independent finite C60 frames on the complete raw 16D arrow.
The proof includes exact endpoint transport, strict concatenation at the
dependent arrow-bundle level, physical Peiffer compatibility, and raw
noncollapse for arbitrary frame words.

This is a two-frame action ON ONE COMPARISON. It is NOT an unconditional
BB two-variable horizontal composition of arbitrary pairs of comparisons:
the independent H.obj/H.left/H.right and BG's two singleton equivariance
gates are still separate obligations. No original geometric 16-cell is
claimed, no raw terms are quotiented away, and no Gray structure is used.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uD vD uE vE

section OriginalC60

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

/-- The chosen ORIGINAL physical AU parallel pair, together with its
16D comparison in BC's explicitly adjoined context-closed presentation.
In particular this includes the WHOLE raw 16D Type-valued witness. -/
def nativeK5BLParallelSeed (W : NativeK5StructuralThirteenCell p U V) :
    NativeC60BGRawArrowBundle
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W) :=
  ⟨(nativeK5AXPack W
        (nativeK5AUNaturalityViaSource W (nativeK5AQExchange W [])),
      nativeK5AXPack W
        (nativeK5AUNaturalityViaTarget W (nativeK5AQExchange W []))),
    nativeK5BCContextualNaturality W [] (nativeK5AQExchange W [])⟩

/-- Independent left and right finite context PARAMETERS, acting on
both EXACT 15D endpoints and the original 16D raw comparison. The
chosen order is part of the presentation; no commutativity is assumed. -/
def nativeK5BLTwoFrame (W : NativeK5StructuralThirteenCell p U V)
    (outer inner : List Bool) :
    NativeC60BGRawArrowBundle
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W) :=
  nativeC60BGRawContext
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
    (outer ++ inner) (nativeK5BLParallelSeed W)

/-- Two-parameter raw transport is EXACTLY successive application on
the full dependent arrow bundle, NOT merely equality of Peiffer values. -/
theorem nativeK5BLTwoFrame_stages
    (W : NativeK5StructuralThirteenCell p U V)
    (outer inner : List Bool) :
    nativeK5BLTwoFrame W outer inner =
      nativeC60BGRawContext
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W) outer
        (nativeC60BGRawContext
          (nativeK5AXKuuSignature W) (nativeK5BCFrame W) inner
          (nativeK5BLParallelSeed W)) :=
  nativeC60BGRawContext_append
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
    outer inner (nativeK5BLParallelSeed W)

/-- The two frame parameters preserve order under further
composition, without inventing a commutation of opposite whiskerings. -/
theorem nativeK5BLTwoFrame_extend
    (W : NativeK5StructuralThirteenCell p U V)
    (front outer inner : List Bool) :
    nativeK5BLTwoFrame W (front ++ outer) inner =
      nativeC60BGRawContext
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W) front
        (nativeK5BLTwoFrame W outer inner) := by
  simpa only [nativeK5BLTwoFrame, List.append_assoc] using
    (nativeC60BGRawContext_append
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
      front (outer ++ inner) (nativeK5BLParallelSeed W))

/-- Both genuinely source-dependent fourteen-cell boundaries agree
AFTER BOTH frames. The raw 16D term supplies this equality. -/
theorem nativeK5BLTwoFrame_parallel
    (W : NativeK5StructuralThirteenCell p U V)
    (outer inner : List Bool) :
    (nativeK5BLTwoFrame W outer inner).1.1.1 =
      (nativeK5BLTwoFrame W outer inner).1.2.1 :=
  (nativeK5BLTwoFrame W outer inner).2.boundary

/-- Physical naturality's two distinct fifteen-cell TERMS never collapse
under ANY two finite frame words, despite their parallel 14D boundary. -/
theorem nativeK5BLTwoFrame_raw_ne
    (W : NativeK5StructuralThirteenCell p U V)
    (outer inner : List Bool) :
    (nativeK5BLTwoFrame W outer inner).1.1 ≠
      (nativeK5BLTwoFrame W outer inner).1.2 := by
  exact nativeK5BCContextualPacked_raw_ne W (outer ++ inner)

/-- Physical noncommutative Peiffer evaluations agree on those DISTINCT
15D terms. The equality is verified from the genuine typed generator. -/
theorem nativeK5BLTwoFrame_peiffer
    (W : NativeK5StructuralThirteenCell p U V)
    (outer inner : List Bool) :
    nativeK5AXPeiffer W (nativeK5BLTwoFrame W outer inner).1.1 =
      nativeK5AXPeiffer W (nativeK5BLTwoFrame W outer inner).1.2 :=
  (nativeK5BLTwoFrame W outer inner).2.observer_sound
    (nativeK5AXPeiffer W) (nativeK5BCSignature_peiffer W)

/-- The actual raw comparison can be followed by its inverse, but
this syntax is NOT definitionally an identity: free 16D grammar
retains the original higher witness and does not silently strictify. -/
def nativeK5BLTwoFrameLoop
    (W : NativeK5StructuralThirteenCell p U V)
    (outer inner : List Bool) :
    NativeC60AXStep (nativeK5BCSignature W)
      (nativeK5BLTwoFrame W outer inner).1.1
      (nativeK5BLTwoFrame W outer inner).1.1 :=
  .trans (nativeK5BLTwoFrame W outer inner).2
    (.symm (nativeK5BLTwoFrame W outer inner).2)

/-- Even the simplest reversal retains its raw 16D constructor tree. -/
theorem nativeK5BLTwoFrameLoop_not_refl
    (W : NativeK5StructuralThirteenCell p U V)
    (outer inner : List Bool) :
    nativeK5BLTwoFrameLoop W outer inner ≠
      NativeC60AXStep.refl (nativeK5BLTwoFrame W outer inner).1.1 := by
  intro h
  cases h

/-- A full BB horizontal candidate, if supplied separately, must
respect the physical object action at this NONTRIVIAL parallel pair,
for EACH original singleton generator; BG/BH/BI remain conditional. -/
theorem nativeK5BLParallelFrameGate
    (W : NativeK5StructuralThirteenCell p U V)
    (Hh : NativeC60BBWhiskering (nativeK5BCSignature W))
    (side : Bool)
    (he : NativeC60BGWhiskeringEquivariant
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W) Hh [side])
    (outer inner : List Bool) :
    nativeK5BCContext W [side]
        (Hh.obj (nativeK5BLTwoFrame W outer inner).1.1
          (nativeK5BLTwoFrame W outer inner).1.2) =
      Hh.obj
        (nativeK5BCContext W [side] (nativeK5BLTwoFrame W outer inner).1.1)
        (nativeK5BCContext W [side] (nativeK5BLTwoFrame W outer inner).1.2) :=
  nativeC60BJObjectGate_of_equivariant
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
    Hh [side] he _ _

/-- If a candidate binary object operation fails the preceding
physical singleton compatibility, it cannot satisfy BG's full
two-variable gate. This is a conditional *concrete-pair* obstruction,
not a blanket no-go for parallel naturality 16D comparisons. -/
theorem nativeK5BLParallelFrameMismatch_no_gate
    (W : NativeK5StructuralThirteenCell p U V)
    (Hh : NativeC60BBWhiskering (nativeK5BCSignature W))
    (side : Bool) (outer inner : List Bool)
    (hne : nativeK5BCContext W [side]
        (Hh.obj (nativeK5BLTwoFrame W outer inner).1.1
          (nativeK5BLTwoFrame W outer inner).1.2) ≠
      Hh.obj
        (nativeK5BCContext W [side] (nativeK5BLTwoFrame W outer inner).1.1)
        (nativeK5BCContext W [side] (nativeK5BLTwoFrame W outer inner).1.2)) :
    ¬ NativeC60BGWhiskeringEquivariant
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W) Hh [side] := by
  intro he
  exact hne (nativeK5BLParallelFrameGate W Hh side he outer inner)

/-- Left-spine length is defined on the ORIGINAL dependent 14D
free syntax, not on histories or on a quotient. It detects the
unremoved associativity parentheses of genuine geometric pasting. -/
def nativeK5BLFourteenLeftDepth
    {A B : NativeK5StructuralThirteenCell p U V} :
    NativeK5StructuralFourteenCell p A B → Nat
  | .trans c _ => nativeK5BLFourteenLeftDepth c + 1
  | _ => 0

/-- The two bracketings of three original 14D raw proofs are not
definitionally or propositionally identical in the free syntax.
The proof uses structural left-spine length, not a scalar shadow. -/
theorem nativeK5BLFourteen_assoc_raw_ne
    {A B C X : NativeK5StructuralThirteenCell p U V}
    (c₁ : NativeK5StructuralFourteenCell p A B)
    (c₂ : NativeK5StructuralFourteenCell p B C)
    (c₃ : NativeK5StructuralFourteenCell p C X) :
    NativeK5StructuralFourteenCell.trans c₁ (.trans c₂ c₃) ≠
      NativeK5StructuralFourteenCell.trans (.trans c₁ c₂) c₃ := by
  intro heq
  have hd := congrArg
    (fun c : NativeK5StructuralFourteenCell p A X =>
      nativeK5BLFourteenLeftDepth c) heq
  change nativeK5BLFourteenLeftDepth c₁ + 1 =
    nativeK5BLFourteenLeftDepth c₁ + 1 + 1 at hd
  omega

/-- The ACTUAL left/right physical AQ frames do NOT commute as raw
14D syntax. They are two opposite parenthesizations of the same
three true 14D proof terms. -/
theorem nativeK5BLPhysicalFrames_raw_ne
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W) :
    nativeK5AQWhiskerLeft W (nativeK5AQWhiskerRight W R) ≠
      nativeK5AQWhiskerRight W (nativeK5AQWhiskerLeft W R) :=
  nativeK5BLFourteen_assoc_raw_ne
    (nativeK5AQLeftFrame W) R (nativeK5AQRightFrame W)

/-- The opposite frame orders have the SAME noncommutative history
value (associativity of the ambient group), despite their raw
14D inequality. Equality of observed words is not raw coherence. -/
theorem nativeK5BLPhysicalFrames_history_eq
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W) :
    (nativeK5AQWhiskerLeft W
      (nativeK5AQWhiskerRight W R)).historyWord =
      (nativeK5AQWhiskerRight W
        (nativeK5AQWhiskerLeft W R)).historyWord := by
  change (nativeK5AQLeftFrame W).historyWord *
      (R.historyWord * (nativeK5AQRightFrame W).historyWord) =
    ((nativeK5AQLeftFrame W).historyWord * R.historyWord) *
      (nativeK5AQRightFrame W).historyWord
  group

/-- The actual 15D AU-compatible grammar can transport a physical
15D proof through both frame orders, but the resulting 15D objects
remember their DIFFERENT original 14D source boundaries. -/
def nativeK5BLMixedLeftRight
    (W : NativeK5StructuralThirteenCell p U V)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S) :
    (nativeK5AXBaseLayer W).Total :=
  nativeK5AXPack W
    (nativeK5AQWhiskerCell W true
      (nativeK5AQWhiskerCell W false cell))

def nativeK5BLMixedRightLeft
    (W : NativeK5StructuralThirteenCell p U V)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S) :
    (nativeK5AXBaseLayer W).Total :=
  nativeK5AXPack W
    (nativeK5AQWhiskerCell W false
      (nativeK5AQWhiskerCell W true cell))

/-- Unlike each internal AU source/target pair, the TWO swapped-frame
images of even the same 15D proof do not have a parallel 14D boundary. -/
theorem nativeK5BLMixed_boundary_ne
    (W : NativeK5StructuralThirteenCell p U V)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S) :
    (nativeK5BLMixedLeftRight W cell).1 ≠
      (nativeK5BLMixedRightLeft W cell).1 := by
  intro heq
  have hs := congrArg
    (fun z : (nativeK5AXBaseLayer W).Obj ×
        (nativeK5AXBaseLayer W).Obj => z.1.down) heq
  exact (nativeK5BLPhysicalFrames_raw_ne W R) hs

/-- An obstruction to a NAIVE reordering of the two true context
frames: no AX signature on the ORIGINAL physical layer can compare
these nonparallel 15D terms by a typed 16D step. It does NOT rule
out either ordered AU naturality comparison already provided by BC. -/
theorem nativeK5BLMixed_no_sixteen
    (W : NativeK5StructuralThirteenCell p U V)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S)
    (T : NativeC60AXSignature (nativeK5AXBaseLayer W)) :
    ¬ Nonempty (NativeC60AXStep T
        (nativeK5BLMixedLeftRight W cell)
        (nativeK5BLMixedRightLeft W cell)) := by
  rintro ⟨compare⟩
  exact (nativeK5BLMixed_boundary_ne W cell) compare.boundary

/-- Specialize that genuine boundary obstruction to the SAME
nontrivial source-side AU naturality proof used in our positive
two-frame 16D comparison. The asymmetry is strictly about SWITCHING
frame order, not a general no-go between parallel evidence. -/
theorem nativeK5BLParallelAU_swapped_no_sixteen
    (W : NativeK5StructuralThirteenCell p U V)
    (T : NativeC60AXSignature (nativeK5AXBaseLayer W)) :
    ¬ Nonempty (NativeC60AXStep T
      (nativeK5BLMixedLeftRight W
        (nativeK5AUNaturalityViaSource W (nativeK5AQExchange W [])))
      (nativeK5BLMixedRightLeft W
        (nativeK5AUNaturalityViaSource W (nativeK5AQExchange W [])))) :=
  nativeK5BLMixed_no_sixteen W
    (nativeK5AUNaturalityViaSource W (nativeK5AQExchange W [])) T

end OriginalC60

#print axioms nativeK5BLParallelSeed
#print axioms nativeK5BLTwoFrame
#print axioms nativeK5BLTwoFrame_stages
#print axioms nativeK5BLTwoFrame_extend
#print axioms nativeK5BLTwoFrame_parallel
#print axioms nativeK5BLTwoFrame_raw_ne
#print axioms nativeK5BLTwoFrame_peiffer
#print axioms nativeK5BLTwoFrameLoop
#print axioms nativeK5BLTwoFrameLoop_not_refl
#print axioms nativeK5BLParallelFrameGate
#print axioms nativeK5BLParallelFrameMismatch_no_gate
#print axioms nativeK5BLFourteenLeftDepth
#print axioms nativeK5BLFourteen_assoc_raw_ne
#print axioms nativeK5BLPhysicalFrames_raw_ne
#print axioms nativeK5BLPhysicalFrames_history_eq
#print axioms nativeK5BLMixedLeftRight
#print axioms nativeK5BLMixedRightLeft
#print axioms nativeK5BLMixed_boundary_ne
#print axioms nativeK5BLMixed_no_sixteen
#print axioms nativeK5BLParallelAU_swapped_no_sixteen

end
end Kuu.F112.Physical
