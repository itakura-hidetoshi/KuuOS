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
    (prefix outer inner : List Bool) :
    nativeK5BLTwoFrame W (prefix ++ outer) inner =
      nativeC60BGRawContext
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W) prefix
        (nativeK5BLTwoFrame W outer inner) := by
  simpa only [nativeK5BLTwoFrame, List.append_assoc] using
    (nativeC60BGRawContext_append
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
      prefix (outer ++ inner) (nativeK5BLParallelSeed W))

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

end
end Kuu.F112.Physical
