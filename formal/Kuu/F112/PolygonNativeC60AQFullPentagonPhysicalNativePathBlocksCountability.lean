import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalFourteenSourceCountability
import Kuu.F112.PolygonNativeBlocks

/-!
# F112-P94D3GF — genuine typed native path and independent block Countable

The original KuuNativePath and KuuNativeBlocks are dependent indexed
Type-valued grammars. The raw path stores every ORIGINAL category Hom;
the raw block object also stores every original partition boundary,
including the empty blocks that flattening would erase.

We derive their countability from the exact two SMALLNESS conditions:
countability of actual category objects and countability of ALL
individual original Hom fibers. This is not a theorem for arbitrary
input categories D/E, nor an inference from finite C60 vertices alone.

Our separate finite syntax stores each original Hom in a dependent
source/target Sigma; the block syntax stores each complete original
typed native path in another Sigma. Partial decoders reject incompatible
intermediate category-object endpoints and recover the exact ORIGINAL
dependent Type-valued proof by decode(encode(p))=some(original p).

The source-category case C=Site is discharged using GE's original
60/90/32 finite C60 geometry and genuine incidence Hom smallness.
The genuine two-independent-axes physical frame remains proof-relevant.

Append-only, strict Kuu central / independent Kuu one presentation,
107 public roots, no Gray, no 19D filler or global hyperdescent.
Pinned Lean v4.30.0-rc2 and mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u v w

/-- A plain finite ordered syntax retaining COMPLETE original
atom data, with an independent root object at nil. -/
inductive NativeGFPlainFiniteSyntax (Obj : Type u) (Atom : Type w) :
    Type (max u w) where
  | nil (x : Obj)
  | snoc (r : NativeGFPlainFiniteSyntax Obj Atom) (a : Atom)
  deriving Countable

/-- Every original category Hom with its true dependent endpoints. -/
abbrev NativeGFOriginalArrowTotal (C : Type u) [Category.{v} C] :
    Type (max u v) :=
  Σ x : C, Σ y : C, (x ⟶ y)

/-- The original complete dependent native arrow path, not the
evaluated composite or a quotient of its internal Hom history. -/
abbrev NativeGFOriginalPathTotal (C : Type u) [Category.{v} C] :
    Type (max u v) :=
  Σ x : C, Σ y : C, KuuNativePath x y

/-- Encode the genuine dependent source path into a finite code
which contains every actual original category Hom. -/
def nativeGFEncodePath {C : Type u} [Category.{v} C] :
    {x y : C} → KuuNativePath x y →
      NativeGFPlainFiniteSyntax C (NativeGFOriginalArrowTotal C)
  | _, _, .nil x => .nil x
  | _, _, .snoc p f =>
      .snoc (nativeGFEncodePath p) ⟨_, _, f⟩

/-- Decode only a path with composable original endpoints;
the entire original Type-valued path and every atom are recovered. -/
noncomputable def nativeGFDecodePath {C : Type u} [Category.{v} C] :
    NativeGFPlainFiniteSyntax C (NativeGFOriginalArrowTotal C) →
      Option (NativeGFOriginalPathTotal C)
  | .nil x => some ⟨x, x, .nil x⟩
  | .snoc code ⟨z, w, f⟩ => by
      classical
      exact (nativeGFDecodePath code).bind
        (fun ⟨x, y, p⟩ =>
          if h : y = z then
            some ⟨x, w, .snoc p (h.symm ▸ f)⟩
          else none)

/-- Strict left inverse for EVERY original dependent path,
including original source/target and all original Hom values. -/
theorem nativeGFDecode_encodePath {C : Type u} [Category.{v} C]
    {x y : C} (p : KuuNativePath x y) :
    nativeGFDecodePath (nativeGFEncodePath p) =
      some (⟨x, y, p⟩ : NativeGFOriginalPathTotal C) := by
  induction p with
  | nil x => rfl
  | snoc p f ih =>
      simp [nativeGFEncodePath, nativeGFDecodePath, ih]

/-- If actual C objects and each exact Hom are Countable,
all original arrow tokens including endpoints are Countable. -/
theorem nativeGFOriginalArrowTotal_countable
    {C : Type u} [Category.{v} C]
    (hobj : Countable C)
    (hhom : ∀ x y : C, Countable (x ⟶ y)) :
    Countable (NativeGFOriginalArrowTotal C) := by
  letI : Countable C := hobj
  letI : ∀ x y : C, Countable (x ⟶ y) := hhom
  infer_instance

/-- Original dependent path TOTAL is Countable under explicit
local Hom smallness. A true inverse-certificate embeds the entire
path total in the range of a decoder from countable finite syntax. -/
theorem nativeGFOriginalPathTotal_countable
    {C : Type u} [Category.{v} C]
    (hobj : Countable C)
    (hhom : ∀ x y : C, Countable (x ⟶ y)) :
    Countable (NativeGFOriginalPathTotal C) := by
  letI : Countable C := hobj
  letI : Countable (NativeGFOriginalArrowTotal C) :=
    nativeGFOriginalArrowTotal_countable hobj hhom
  haveI : Countable
      (NativeGFPlainFiniteSyntax C (NativeGFOriginalArrowTotal C)) :=
    inferInstance
  have hrange : (Set.range (nativeGFDecodePath (C := C))).Countable :=
    Set.countable_range _
  letI : Countable (Set.range (nativeGFDecodePath (C := C))) :=
    hrange.to_subtype
  let embedding : NativeGFOriginalPathTotal C →
      Set.range (nativeGFDecodePath (C := C)) :=
    fun t => ⟨some t, by
      rcases t with ⟨x, y, p⟩
      exact ⟨nativeGFEncodePath p, nativeGFDecode_encodePath p⟩⟩
  have hinj : Function.Injective embedding := by
    intro t s h
    have ht : (some t : Option (NativeGFOriginalPathTotal C)) =
        some s := congrArg
          (fun z : Set.range (nativeGFDecodePath (C := C)) => z.1) h
    exact Option.some.inj ht
  exact hinj.countable

/-- Each original indexed raw native path fiber is Countable
without forgetting either endpoint or any original arrow. -/
theorem nativeGFOriginalPathFiber_countable
    {C : Type u} [Category.{v} C]
    (hobj : Countable C)
    (hhom : ∀ x y : C, Countable (x ⟶ y))
    (x y : C) : Countable (KuuNativePath x y) := by
  letI : Countable (NativeGFOriginalPathTotal C) :=
    nativeGFOriginalPathTotal_countable hobj hhom
  have hinj : Function.Injective
      (fun p : KuuNativePath x y =>
        (⟨x, y, p⟩ : NativeGFOriginalPathTotal C)) := by
    intro p q h
    have ht : (⟨y, p⟩ : Σ z : C, KuuNativePath x z) =
        ⟨y, q⟩ := eq_of_heq (Sigma.mk.inj h).2
    exact eq_of_heq (Sigma.mk.inj ht).2
  exact hinj.countable

/-- The original block total contains the whole original path
partition grammar: zero blocks and empty blocks are distinguished. -/
abbrev NativeGFOriginalBlocksTotal (C : Type u) [Category.{v} C] :
    Type (max u v) :=
  Σ x : C, Σ y : C, KuuNativeBlocks x y

/-- Record the original independent partition boundaries AND
each original native path (which contains all its original Homs). -/
def nativeGFEncodeBlocks {C : Type u} [Category.{v} C] :
    {x y : C} → KuuNativeBlocks x y →
      NativeGFPlainFiniteSyntax C (NativeGFOriginalPathTotal C)
  | _, _, .empty x => .nil x
  | _, _, .snoc p q =>
      .snoc (nativeGFEncodeBlocks p) ⟨_, _, q⟩

/-- Partial dependent block interpreter. The original full path
atom must start at the previous block's precise typed target. -/
noncomputable def nativeGFDecodeBlocks {C : Type u} [Category.{v} C] :
    NativeGFPlainFiniteSyntax C (NativeGFOriginalPathTotal C) →
      Option (NativeGFOriginalBlocksTotal C)
  | .nil x => some ⟨x, x, .empty x⟩
  | .snoc code ⟨z, w, q⟩ => by
      classical
      exact (nativeGFDecodeBlocks code).bind
        (fun ⟨x, y, b⟩ =>
          if h : y = z then
            some ⟨x, w, .snoc b (h.symm ▸ q)⟩
          else none)

/-- The dependent decoder is an EXACT left inverse on every
original block subdivision, including inserted empty blocks. -/
theorem nativeGFDecode_encodeBlocks
    {C : Type u} [Category.{v} C]
    {x y : C} (b : KuuNativeBlocks x y) :
    nativeGFDecodeBlocks (nativeGFEncodeBlocks b) =
      some (⟨x, y, b⟩ : NativeGFOriginalBlocksTotal C) := by
  induction b with
  | empty x => rfl
  | snoc b q ih =>
      simp [nativeGFEncodeBlocks, nativeGFDecodeBlocks, ih]

/-- Full original blocks total Countable follows from the
original raw path total Countable, with no flattening of blocks. -/
theorem nativeGFOriginalBlocksTotal_countable
    {C : Type u} [Category.{v} C]
    (hobj : Countable C)
    (hhom : ∀ x y : C, Countable (x ⟶ y)) :
    Countable (NativeGFOriginalBlocksTotal C) := by
  letI : Countable C := hobj
  letI : Countable (NativeGFOriginalPathTotal C) :=
    nativeGFOriginalPathTotal_countable hobj hhom
  haveI : Countable
      (NativeGFPlainFiniteSyntax C (NativeGFOriginalPathTotal C)) :=
    inferInstance
  have hrange : (Set.range (nativeGFDecodeBlocks (C := C))).Countable :=
    Set.countable_range _
  letI : Countable (Set.range (nativeGFDecodeBlocks (C := C))) :=
    hrange.to_subtype
  let embedding : NativeGFOriginalBlocksTotal C →
      Set.range (nativeGFDecodeBlocks (C := C)) :=
    fun t => ⟨some t, by
      rcases t with ⟨x, y, b⟩
      exact ⟨nativeGFEncodeBlocks b, nativeGFDecode_encodeBlocks b⟩⟩
  have hinj : Function.Injective embedding := by
    intro t s h
    have ht : (some t : Option (NativeGFOriginalBlocksTotal C)) =
        some s := congrArg
          (fun z : Set.range (nativeGFDecodeBlocks (C := C)) => z.1) h
    exact Option.some.inj ht
  exact hinj.countable

/-- Every precise source/target-indexed ORIGINAL block partition
is Countable, preserving the original Type-valued partitions. -/
theorem nativeGFOriginalBlocksFiber_countable
    {C : Type u} [Category.{v} C]
    (hobj : Countable C)
    (hhom : ∀ x y : C, Countable (x ⟶ y))
    (x y : C) : Countable (KuuNativeBlocks x y) := by
  letI : Countable (NativeGFOriginalBlocksTotal C) :=
    nativeGFOriginalBlocksTotal_countable hobj hhom
  have hinj : Function.Injective
      (fun b : KuuNativeBlocks x y =>
        (⟨x, y, b⟩ : NativeGFOriginalBlocksTotal C)) := by
    intro p q h
    have ht : (⟨y, p⟩ : Σ z : C, KuuNativeBlocks x z) =
        ⟨y, q⟩ := eq_of_heq (Sigma.mk.inj h).2
    exact eq_of_heq (Sigma.mk.inj ht).2
  exact hinj.countable

/-- Real original physical C60 Site category has countable
native paths under the fully proved GE finite incidence Hom facts. -/
theorem nativeGFPhysicalC60PathTotal_countable :
    Countable (NativeGFOriginalPathTotal Site) :=
  nativeGFOriginalPathTotal_countable
    nativeC60GEPhysicalSite_countable
    nativeC60GEPhysicalIncidenceHom_countable

theorem nativeGFPhysicalC60PathFiber_countable (x y : Site) :
    Countable (KuuNativePath x y) :=
  nativeGFOriginalPathFiber_countable
    nativeC60GEPhysicalSite_countable
    nativeC60GEPhysicalIncidenceHom_countable x y

/-- Real original Site block partitions, not their flattenings. -/
theorem nativeGFPhysicalC60BlocksTotal_countable :
    Countable (NativeGFOriginalBlocksTotal Site) :=
  nativeGFOriginalBlocksTotal_countable
    nativeC60GEPhysicalSite_countable
    nativeC60GEPhysicalIncidenceHom_countable

theorem nativeGFPhysicalC60BlocksFiber_countable (x y : Site) :
    Countable (KuuNativeBlocks x y) :=
  nativeGFOriginalBlocksFiber_countable
    nativeC60GEPhysicalSite_countable
    nativeC60GEPhysicalIncidenceHom_countable x y

/-- A genuine two-axis physical C60 frame retains BOTH raw
block partitions; its composite equality is an attached Prop. -/
theorem nativeGFPhysicalDualAxisFrame_countable
    (p : Polygon) (i : PolygonBoundarySector p) :
    Countable (PolygonNativeDualAxisFrame p i) := by
  letI : Countable (KuuNativeBlocks
      (Site.vertex (cyclicBoundaryDart p i.1.val)) (Site.face p)) :=
    nativeGFPhysicalC60BlocksFiber_countable _ _
  have hinj : Function.Injective
      (fun f : PolygonNativeDualAxisFrame p i =>
        (f.firstAxis, f.secondAxis)) := by
    rintro ⟨a, b, hab⟩ ⟨c, d, hcd⟩ eq
    have hfirst : a = c := congrArg Prod.fst eq
    have hsecond : b = d := congrArg Prod.snd eq
    subst c
    subst d
    rfl
  exact hinj.countable

/-- All original physical polygon-sector dual-axis frames
are Countable, retaining their actual face/sector identifiers. -/
theorem nativeGFPhysicalDualAxisTotal_countable :
    Countable (Σ p : Polygon,
      Σ i : PolygonBoundarySector p, PolygonNativeDualAxisFrame p i) := by
  letI : ∀ p : Polygon, ∀ i : PolygonBoundarySector p,
      Countable (PolygonNativeDualAxisFrame p i) :=
    nativeGFPhysicalDualAxisFrame_countable
  infer_instance

#print axioms nativeGFDecode_encodePath
#print axioms nativeGFOriginalArrowTotal_countable
#print axioms nativeGFOriginalPathTotal_countable
#print axioms nativeGFOriginalPathFiber_countable
#print axioms nativeGFDecode_encodeBlocks
#print axioms nativeGFOriginalBlocksTotal_countable
#print axioms nativeGFOriginalBlocksFiber_countable
#print axioms nativeGFPhysicalC60PathTotal_countable
#print axioms nativeGFPhysicalC60PathFiber_countable
#print axioms nativeGFPhysicalC60BlocksTotal_countable
#print axioms nativeGFPhysicalC60BlocksFiber_countable
#print axioms nativeGFPhysicalDualAxisFrame_countable
#print axioms nativeGFPhysicalDualAxisTotal_countable

end
end Kuu.F112.Physical
