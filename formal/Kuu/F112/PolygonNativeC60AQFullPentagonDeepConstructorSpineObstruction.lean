import Kuu.F112.PolygonNativeC60AQFullPentagonRecursiveGeneratorReflection

/-!
# F112-P94D3FI — exact full recursive 18D constructor-spine reflection

FG rules out collisions across the three TOP-LEVEL original 18D
assoc/post/pre sectors, while FH reflects variable-inner post/pre
arguments under an explicit fixed-boundary inner faithfulness gate.

FI goes beyond the top-level sector tag and observes the ENTIRE
arbitrarily nested original dependent 18D constructor grammar.
For each genuine original generator, its finite ordered recursion
spine is the exact word of post/pre whiskering constructors ending
in the primitive assoc. The actual separately context-closed
DV transport preserves this WHOLE spine without any injectivity
hypothesis on the C60 frame and without erasing a Type-valued
source or target. Consequently every actual complete-code collision
preserves all nested constructor tags and the exact recursion depth.
Any two original full codes with distinct spines have a nontrivial
two-letter defect outside the true full noncommutative DV kernel.

This proves a precise unrestricted SHAPE obstruction, not a
claim that same-spine original path arguments, original 17D context
objects or variable inner generators are always injective.
The fixed-boundary FH conditions and DS complete-evidence no-go
remain visible. No Gray, original C60 geometric 19D filler,
new axioms/sorry/admit, root replacement or quotient collapse.
107 public roots, strict Kuu primary, independent Kuu as
one presentation, append-only / tighten-only / same-root.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u

section FullRecursiveEighteenConstructorSpine

variable {L : NativeC60AXLayer.{u}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- ALL original 18D recursion constructors, including the final
primitive assoc, in their actual outer-to-inner order. This
observer retains the nested 18D constructor history rather than
only the top-level sector or a parity charge. It does NOT claim
to retain the complete original 17D path arguments. -/
def nativeC60FIOriginalConstructorSpine
    {x y : (nativeC60DREighteenLayer S F).Total}
    (g : (nativeC60DREighteenAssocSignature S F).Gen x y) :
    List NativeC60FGConstructorTag := by
  induction g with
  | assoc _ _ _ => exact [.assoc]
  | post _ _ ih => exact .post :: ih
  | pre _ _ ih => exact .pre :: ih

/-- An independently declared target 18D constructor-spine
observer, applied to the actual context-CLOSED 18D alphabet. -/
def nativeC60FIClosedConstructorSpine
    {x y : (nativeC60DVClosedEighteenLayer S F).Total}
    (g : (nativeC60DVClosedEighteenSignature S F).Gen x y) :
    List NativeC60FGConstructorTag := by
  induction g with
  | assoc _ _ _ => exact [.assoc]
  | post _ _ ih => exact .post :: ih
  | pre _ _ ih => exact .pre :: ih

/-- ORIGINAL entire nested constructor chain on a complete
dependent 18D code (including all its typed endpoints). -/
def nativeC60FIOriginalCodeSpine
    (code : NativeC60DSCompleteEighteenCode S F) :
    List NativeC60FGConstructorTag :=
  nativeC60FIOriginalConstructorSpine S F code.2.2

/-- Receiving entire nested constructor chain on a genuine
context-CLOSED complete dependent 18D code. -/
def nativeC60FIClosedCodeSpine
    (code : NativeC60DVCompleteEighteenCode S F) :
    List NativeC60FGConstructorTag :=
  nativeC60FIClosedConstructorSpine S F code.2.2

/-- The ACTUAL raw17D finite C60 AQ transport recursively
preserves EVERY original 18D assoc/post/pre constructor tag
in order, not just the FG top-level tag. Crucially no context
object or path injectivity premise is required. -/
theorem nativeC60FIConstructorSpine_transport
    (word : List Bool)
    {x y : (nativeC60DREighteenLayer S F).Total}
    (g : (nativeC60DREighteenAssocSignature S F).Gen x y) :
    nativeC60FIClosedConstructorSpine S F
        (nativeC60DVTransportEighteenGen S F word g) =
      nativeC60FIOriginalConstructorSpine S F g := by
  induction g with
  | assoc _ _ _ => rfl
  | post r h ih =>
      change
        (.post :: nativeC60FIClosedConstructorSpine S F
            (nativeC60DVTransportEighteenGen S F word r)) =
          (.post :: nativeC60FIOriginalConstructorSpine S F r)
      exact congrArg (List.cons NativeC60FGConstructorTag.post) ih
  | pre h r ih =>
      change
        (.pre :: nativeC60FIClosedConstructorSpine S F
            (nativeC60DVTransportEighteenGen S F word r)) =
          (.pre :: nativeC60FIOriginalConstructorSpine S F r)
      exact congrArg (List.cons NativeC60FGConstructorTag.pre) ih

/-- Entire source/target-typed original DV complete-code map
preserves the complete recursive shape, with NO assumption
of injectivity on original context frames. -/
theorem nativeC60FICompleteCodeSpine_transport
    (word : List Bool)
    (code : NativeC60DSCompleteEighteenCode S F) :
    nativeC60FIClosedCodeSpine S F
        (nativeC60DVTransportCompleteCode S F word code) =
      nativeC60FIOriginalCodeSpine S F code := by
  rcases code with ⟨x, y, g⟩
  exact nativeC60FIConstructorSpine_transport S F word g

/-- A collision of actual transported original full 18D
complete codes forces agreement of the ENTIRE original nested
assoc/post/pre constructor history, not only its first tag. -/
theorem nativeC60FICompleteCodeCollision_preserves_spine
    (word : List Bool)
    {a b : NativeC60DSCompleteEighteenCode S F}
    (hab : nativeC60DVTransportCompleteCode S F word a =
      nativeC60DVTransportCompleteCode S F word b) :
    nativeC60FIOriginalCodeSpine S F a =
      nativeC60FIOriginalCodeSpine S F b := by
  calc
    nativeC60FIOriginalCodeSpine S F a =
        nativeC60FIClosedCodeSpine S F
          (nativeC60DVTransportCompleteCode S F word a) :=
      (nativeC60FICompleteCodeSpine_transport S F word a).symm
    _ = nativeC60FIClosedCodeSpine S F
          (nativeC60DVTransportCompleteCode S F word b) :=
      congrArg (nativeC60FIClosedCodeSpine S F) hab
    _ = nativeC60FIOriginalCodeSpine S F b :=
      nativeC60FICompleteCodeSpine_transport S F word b

/-- Distinct full recursive constructor histories CANNOT collide
under actual unquotiented DV code transport, even with arbitrary
noninjective underlying C60 context frames. -/
theorem nativeC60FIDistinct_spines_codes_ne
    (word : List Bool)
    {a b : NativeC60DSCompleteEighteenCode S F}
    (hspine : nativeC60FIOriginalCodeSpine S F a ≠
      nativeC60FIOriginalCodeSpine S F b) :
    nativeC60DVTransportCompleteCode S F word a ≠
      nativeC60DVTransportCompleteCode S F word b := by
  intro hab
  exact hspine
    (nativeC60FICompleteCodeCollision_preserves_spine S F word hab)

/-- Full recursive whiskering depth is the number of actual
assoc/post/pre nested constructor layers; no path history is
mistaken for a quotient. -/
def nativeC60FIOriginalCodeDepth
    (code : NativeC60DSCompleteEighteenCode S F) : Nat :=
  (nativeC60FIOriginalCodeSpine S F code).length

def nativeC60FIClosedCodeDepth
    (code : NativeC60DVCompleteEighteenCode S F) : Nat :=
  (nativeC60FIClosedCodeSpine S F code).length

/-- The exact original recursive 18D constructor depth is
preserved by ANY physical finite AQ word, unconditionally. -/
theorem nativeC60FICompleteCodeDepth_transport
    (word : List Bool)
    (code : NativeC60DSCompleteEighteenCode S F) :
    nativeC60FIClosedCodeDepth S F
        (nativeC60DVTransportCompleteCode S F word code) =
      nativeC60FIOriginalCodeDepth S F code :=
  congrArg List.length
    (nativeC60FICompleteCodeSpine_transport S F word code)

/-- In particular every 18D code collision has identical
full recursion depth; differing depth is a sufficient no-collision
obstruction even when no original frame injectivity is known. -/
theorem nativeC60FICompleteCodeCollision_same_depth
    (word : List Bool)
    {a b : NativeC60DSCompleteEighteenCode S F}
    (hab : nativeC60DVTransportCompleteCode S F word a =
      nativeC60DVTransportCompleteCode S F word b) :
    nativeC60FIOriginalCodeDepth S F a =
      nativeC60FIOriginalCodeDepth S F b :=
  congrArg List.length
    (nativeC60FICompleteCodeCollision_preserves_spine S F word hab)

/-- The genuine noncommutative two-letter code-fiber defect
cannot lie in DV's actual kernel when original dependent 18D
generators differ ANYWHERE along the complete nested constructor
spine. This is a stronger shape obstruction than the FG
top-constructor separation; it is not a full kernel classifier. -/
theorem nativeC60FIDistinct_spines_defect_not_mem_DVKernel
    (word : List Bool)
    {a b : NativeC60DSCompleteEighteenCode S F}
    (hspine : nativeC60FIOriginalCodeSpine S F a ≠
      nativeC60FIOriginalCodeSpine S F b) :
    nativeC60FCCodeFiberDefect S F a b ∉
      (nativeC60DVFullWordTransport S F word).ker := by
  intro hz
  have hzero :
      (nativeC60DVFullWordTransport S F word)
        (nativeC60FCCodeFiberDefect S F a b) = 1 :=
    MonoidHom.mem_ker.mp hz
  have hprod :
      (FreeGroup.of (nativeC60DVTransportCompleteCode S F word a) :
        NativeC60DVClosedFullFree S F) *
          (FreeGroup.of (nativeC60DVTransportCompleteCode S F word b))⁻¹ = 1 := by
    simpa only [nativeC60FCCodeFiberDefect, map_mul, map_inv,
      nativeC60DVFullWordTransport_of] using hzero
  have hcodes := FreeGroup.of_injective (eq_of_mul_inv_eq_one hprod)
  exact nativeC60FIDistinct_spines_codes_ne S F word hspine hcodes

/-- Conversely, any ACTUAL two-letter DV kernel element forces
the complete original nested constructor spine to agree. -/
theorem nativeC60FICodeFiberKernel_preserves_spine
    (word : List Bool)
    {a b : NativeC60DSCompleteEighteenCode S F}
    (hker : nativeC60FCCodeFiberDefect S F a b ∈
      (nativeC60DVFullWordTransport S F word).ker) :
    nativeC60FIOriginalCodeSpine S F a =
      nativeC60FIOriginalCodeSpine S F b := by
  by_contra hspine
  exact (nativeC60FIDistinct_spines_defect_not_mem_DVKernel
    S F word hspine) hker

/-- Genuine finite C60 AQ trees inherit the same FULL recursive
constructor-spine obstruction with their actual chronological
context words, not merely a hypothetical abstract action. -/
theorem nativeC60FIActualTree_distinct_spines_not_mem
    (tree : NativeK5DOContextTree)
    {a b : NativeC60DSCompleteEighteenCode S F}
    (hspine : nativeC60FIOriginalCodeSpine S F a ≠
      nativeC60FIOriginalCodeSpine S F b) :
    nativeC60FCCodeFiberDefect S F a b ∉
      (nativeC60DVFullWordTransport S F
        (nativeK5DOTreeWord tree)).ker :=
  nativeC60FIDistinct_spines_defect_not_mem_DVKernel S F
    (nativeK5DOTreeWord tree) hspine


/-- A noncommutative FreeGroup of complete finite, recursively
ordered original assoc/post/pre constructor histories. It forgets
raw17D PATH ARGUMENTS but retains all nested constructor order,
unlike an abelian or parity charge. This is an auxiliary
necessary invariant, never the full physical 18D receiver. -/
def nativeC60FIOriginalSpineHom :
    NativeC60DTFullFree S F →*
      FreeGroup (List NativeC60FGConstructorTag) :=
  FreeGroup.map (nativeC60FIOriginalCodeSpine S F)

def nativeC60FIClosedSpineHom :
    NativeC60DVClosedFullFree S F →*
      FreeGroup (List NativeC60FGConstructorTag) :=
  FreeGroup.map (nativeC60FIClosedCodeSpine S F)

/-- TRUE noncommutative whole-word NATURALITY:
The complete original nested constructor-spine observable factors
exactly through the actual DV map into the separately declared
context-CLOSED 18D evidence, for every signed, ordered finite
original free word and every C60 AQ context word. -/
theorem nativeC60FIWholeSpineHom_natural
    (word : List Bool) (z : NativeC60DTFullFree S F) :
    (nativeC60FIClosedSpineHom S F)
        ((nativeC60DVFullWordTransport S F word) z) =
      (nativeC60FIOriginalSpineHom S F) z := by
  rw [nativeC60FCTransport_eq_freeMap S F word]
  change
    FreeGroup.map (nativeC60FIClosedCodeSpine S F)
        (FreeGroup.map (nativeC60DVTransportCompleteCode S F word) z) =
      FreeGroup.map (nativeC60FIOriginalCodeSpine S F) z
  rw [FreeGroup.map.comp]
  have hcomp :
      (nativeC60FIClosedCodeSpine S F) ∘
        (nativeC60DVTransportCompleteCode S F word) =
      nativeC60FIOriginalCodeSpine S F := by
    funext code
    exact nativeC60FICompleteCodeSpine_transport S F word code
  rw [hcomp]

/-- NEW GROUP-LEVEL OBSTRUCTION: The ENTIRE genuine original DV
full noncommutative free-word kernel lies inside the kernel of the
original nested-constructor-spine free-group receiver. This is
STRICTLY a necessary kernel restriction, NOT a claim that the two
kernels are equal, nor a normal-generation classification. -/
theorem nativeC60FIDVKernel_le_recursive_spine_kernel
    (word : List Bool) :
    (nativeC60DVFullWordTransport S F word).ker ≤
      (nativeC60FIOriginalSpineHom S F).ker := by
  intro z hz
  apply MonoidHom.mem_ker.mpr
  calc
    (nativeC60FIOriginalSpineHom S F) z =
        (nativeC60FIClosedSpineHom S F)
          ((nativeC60DVFullWordTransport S F word) z) :=
      (nativeC60FIWholeSpineHom_natural S F word z).symm
    _ = 1 := by rw [MonoidHom.mem_ker.mp hz, map_one]

/-- Every signed source 18D word killed by actual DV transport
already has trivial FULL NONCOMMUTATIVE NESTED-SHAPE free word:
its potentially nontrivial original 17D payload must therefore
reside entirely inside shape-neutral fibers. -/
theorem nativeC60FIKernel_signedWord_spine_neutral
    (word : List Bool)
    (xs : List (NativeC60DSCompleteEighteenCode S F × Bool))
    (hker : FreeGroup.mk xs ∈
      (nativeC60DVFullWordTransport S F word).ker) :
    FreeGroup.mk (xs.map (fun z =>
        (nativeC60FIOriginalCodeSpine S F z.1, z.2))) =
      (1 : FreeGroup (List NativeC60FGConstructorTag)) := by
  have hspine :
      (nativeC60FIOriginalSpineHom S F) (FreeGroup.mk xs) = 1 :=
    MonoidHom.mem_ker.mp
      (nativeC60FIDVKernel_le_recursive_spine_kernel S F word hker)
  simpa only [nativeC60FIOriginalSpineHom, FreeGroup.map.mk] using hspine

end FullRecursiveEighteenConstructorSpine

#print axioms nativeC60FIOriginalConstructorSpine
#print axioms nativeC60FIClosedConstructorSpine
#print axioms nativeC60FIOriginalCodeSpine
#print axioms nativeC60FIClosedCodeSpine
#print axioms nativeC60FIConstructorSpine_transport
#print axioms nativeC60FICompleteCodeSpine_transport
#print axioms nativeC60FICompleteCodeCollision_preserves_spine
#print axioms nativeC60FIDistinct_spines_codes_ne
#print axioms nativeC60FIOriginalCodeDepth
#print axioms nativeC60FIClosedCodeDepth
#print axioms nativeC60FICompleteCodeDepth_transport
#print axioms nativeC60FICompleteCodeCollision_same_depth
#print axioms nativeC60FIDistinct_spines_defect_not_mem_DVKernel
#print axioms nativeC60FICodeFiberKernel_preserves_spine
#print axioms nativeC60FIActualTree_distinct_spines_not_mem
#print axioms nativeC60FIOriginalSpineHom
#print axioms nativeC60FIClosedSpineHom
#print axioms nativeC60FIWholeSpineHom_natural
#print axioms nativeC60FIDVKernel_le_recursive_spine_kernel
#print axioms nativeC60FIKernel_signedWord_spine_neutral

end
end Kuu.F112.Physical
