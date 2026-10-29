import Kuu.F112.PolygonNativeC60AQFullPentagonGeneratorFaithfulnessGate

/-!
# F112-P94D3FG — actual 18D assoc/post/pre constructor sector separation

The original DR complete 18D generator alphabet is the dependent
assoc / post / pre Type-valued grammar. Its actual DV transport is
constructor-by-constructor recursion into the independently declared
C60 AQ context-closed 18D grammar, with the same three constructor
families. No identification of constructors follows from any
lower-object context collision.

This file proves a new UNCONDITIONAL restriction on possible DV
complete-code collisions: the top-level constructor TAG of an
original generator is preserved exactly, for ANY genuine finite
AQ context and ANY C60 frames. Hence collisions can arise only
within a fixed assoc, post or pre constructor sector. An original
noncommutative two-letter difference across different sectors is
never killed by the actual UNQUOTIENTED full DV FreeGroup transport.

This is an exact constructor obstruction, not a proof that the
within-sector map is injective. The latter remains the explicitly
identified FG criterion requiring the lower original 17D context
object and recursive generator data. Preserve original 14D--18D
Type-valued history, original versus closed target, DS no-go,
strict Kuu primary, independent Kuu presentation, 107 roots,
no Gray, no geometric original 19D filler, no new axioms/sorry/admit.
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

/-- The three primitive shapes in the genuine noncommutative
eighteen-dimensional associator / whiskering Type grammar. -/
inductive NativeC60FGConstructorTag : Type where
  | assoc | post | pre
  deriving DecidableEq

section ActualConstructorSectors

variable {L : NativeC60AXLayer.{u}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- The tag of an ACTUAL original DR full dependent 18D generator
code, retaining its complete source/target in the enclosing code. -/
def nativeC60FGOriginalConstructorTag
    (code : NativeC60DSCompleteEighteenCode S F) :
    NativeC60FGConstructorTag := by
  rcases code with ⟨x, y, g⟩
  cases g with
  | assoc _ _ _ => exact .assoc
  | post _ _ => exact .post
  | pre _ _ => exact .pre

/-- Tag of the ACTUAL separately context-CLOSED receiving
DV complete dependent 18D code; no shadow quotient is involved. -/
def nativeC60FGClosedConstructorTag
    (code : NativeC60DVCompleteEighteenCode S F) :
    NativeC60FGConstructorTag := by
  rcases code with ⟨x, y, g⟩
  cases g with
  | assoc _ _ _ => exact .assoc
  | post _ _ => exact .post
  | pre _ _ => exact .pre

/-- Native DV transport of each original dependent assoc/post/pre
code PRESERVES its actual original constructor category exactly,
without ANY injectivity assumption on the C60 context frame. -/
theorem nativeC60FGConstructorTag_transport
    (word : List Bool)
    (code : NativeC60DSCompleteEighteenCode S F) :
    nativeC60FGClosedConstructorTag S F
        (nativeC60DVTransportCompleteCode S F word code) =
      nativeC60FGOriginalConstructorTag S F code := by
  rcases code with ⟨x, y, g⟩
  induction g with
  | assoc _ _ _ => rfl
  | post _ _ _ => rfl
  | pre _ _ _ => rfl

/-- Possible complete-code DV collisions must have the SAME
original assoc/post/pre tag. In particular, even a noninjective
17D frame can never identify DIFFERENT constructor categories. -/
theorem nativeC60FGCollision_preserves_constructor
    (word : List Bool)
    {a b : NativeC60DSCompleteEighteenCode S F}
    (h : nativeC60DVTransportCompleteCode S F word a =
      nativeC60DVTransportCompleteCode S F word b) :
    nativeC60FGOriginalConstructorTag S F a =
      nativeC60FGOriginalConstructorTag S F b := by
  calc
    nativeC60FGOriginalConstructorTag S F a =
        nativeC60FGClosedConstructorTag S F
          (nativeC60DVTransportCompleteCode S F word a) :=
      (nativeC60FGConstructorTag_transport S F word a).symm
    _ = nativeC60FGClosedConstructorTag S F
          (nativeC60DVTransportCompleteCode S F word b) :=
      congrArg (nativeC60FGClosedConstructorTag S F) h
    _ = nativeC60FGOriginalConstructorTag S F b :=
      nativeC60FGConstructorTag_transport S F word b

/-- Distinct actual original constructor tags prevent DV complete
code equality, even without an injective 17D object context. -/
theorem nativeC60FGCrossConstructor_codes_ne
    (word : List Bool)
    {a b : NativeC60DSCompleteEighteenCode S F}
    (ht : nativeC60FGOriginalConstructorTag S F a ≠
      nativeC60FGOriginalConstructorTag S F b) :
    nativeC60DVTransportCompleteCode S F word a ≠
      nativeC60DVTransportCompleteCode S F word b := by
  intro h
  exact ht (nativeC60FGCollision_preserves_constructor S F word h)

/-- A two-letter difference of ORIGINAL dependent generators
from distinct assoc/pre/post sectors cannot belong to the KERNEL
of the true noncommutative DV full-group transport, even with
arbitrary C60 object-context identifications. -/
theorem nativeC60FGCrossConstructor_defect_not_mem_DVKernel
    (word : List Bool)
    {a b : NativeC60DSCompleteEighteenCode S F}
    (ht : nativeC60FGOriginalConstructorTag S F a ≠
      nativeC60FGOriginalConstructorTag S F b) :
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
  exact nativeC60FGCrossConstructor_codes_ne S F word ht hcodes

/-- The constructor separation is stable for EVERY genuine finite
C60 AQ physical context tree, not only an unspecified abstract word. -/
theorem nativeC60FGActualTree_cross_constructor_not_mem
    (tree : NativeK5DOContextTree)
    {a b : NativeC60DSCompleteEighteenCode S F}
    (ht : nativeC60FGOriginalConstructorTag S F a ≠
      nativeC60FGOriginalConstructorTag S F b) :
    nativeC60FCCodeFiberDefect S F a b ∉
      (nativeC60DVFullWordTransport S F
        (nativeK5DOTreeWord tree)).ker :=
  nativeC60FGCrossConstructor_defect_not_mem_DVKernel S F
    (nativeK5DOTreeWord tree) ht

/-- Faithfulness of the entire ORIGINAL dependent complete-code DV
map inside ONE actual original constructor sector. This is a proof
obligation, not an assumption that arbitrary C60 frames satisfy it. -/
def NativeC60FGSectorFaithful
    (word : List Bool) (tag : NativeC60FGConstructorTag) : Prop :=
  ∀ a b : NativeC60DSCompleteEighteenCode S F,
    nativeC60FGOriginalConstructorTag S F a = tag →
    nativeC60FGOriginalConstructorTag S F b = tag →
    nativeC60DVTransportCompleteCode S F word a =
      nativeC60DVTransportCompleteCode S F word b → a = b

/-- Exact localization: full DV complete-code injectivity is
equivalent to faithfulness within EACH of the three ACTUAL
assoc, post and pre generator sectors. There are NO cross-sector
code collisions by the preceding genuine constructor theorem. -/
theorem nativeC60FGCompleteCode_injective_iff_three_sectors
    (word : List Bool) :
    Function.Injective (nativeC60DVTransportCompleteCode S F word) ↔
      NativeC60FGSectorFaithful S F word .assoc ∧
      NativeC60FGSectorFaithful S F word .post ∧
      NativeC60FGSectorFaithful S F word .pre := by
  constructor
  · intro hinj
    exact ⟨(fun a b _ _ hab => hinj hab),
      (fun a b _ _ hab => hinj hab),
      (fun a b _ _ hab => hinj hab)⟩
  · rintro ⟨ha, hpost, hpre⟩ a b hab
    have htag := nativeC60FGCollision_preserves_constructor S F word hab
    cases htag0 : nativeC60FGOriginalConstructorTag S F a with
    | assoc =>
        exact ha a b htag0 (htag0 ▸ htag.symm) hab
    | post =>
        exact hpost a b htag0 (htag0 ▸ htag.symm) hab
    | pre =>
        exact hpre a b htag0 (htag0 ▸ htag.symm) hab

/-- FC transports the exact three-sector obstruction localization
through the REAL noncommutative FreeGroup.map of complete 18D codes,
not a quotient, parity observer, or geometric 19D filler. -/
theorem nativeC60FGFullFree_injective_iff_three_sectors
    (word : List Bool) :
    Function.Injective (nativeC60DVFullWordTransport S F word) ↔
      NativeC60FGSectorFaithful S F word .assoc ∧
      NativeC60FGSectorFaithful S F word .post ∧
      NativeC60FGSectorFaithful S F word .pre :=
  (nativeC60FCTransport_injective_iff_code S F word).trans
    (nativeC60FGCompleteCode_injective_iff_three_sectors S F word)

end ActualConstructorSectors

#print axioms NativeC60FGConstructorTag
#print axioms nativeC60FGOriginalConstructorTag
#print axioms nativeC60FGClosedConstructorTag
#print axioms nativeC60FGConstructorTag_transport
#print axioms nativeC60FGCollision_preserves_constructor
#print axioms nativeC60FGCrossConstructor_codes_ne
#print axioms nativeC60FGCrossConstructor_defect_not_mem_DVKernel
#print axioms nativeC60FGActualTree_cross_constructor_not_mem
#print axioms NativeC60FGSectorFaithful
#print axioms nativeC60FGCompleteCode_injective_iff_three_sectors
#print axioms nativeC60FGFullFree_injective_iff_three_sectors

end
end Kuu.F112.Physical
