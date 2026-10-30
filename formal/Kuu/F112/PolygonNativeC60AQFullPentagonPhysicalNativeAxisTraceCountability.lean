import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativePathBlocksCountability
import Kuu.F112.NativeAxisTraces

/-!
# F112-P94D3GG — original Type-valued OneStep and AxisTrace countability

GF proved Countable for full original KuuNativePath and KuuNativeBlocks
without forgetting their original category Hom values or independent
empty block boundaries. GG proves the NEXT authentic source step:

* the original split/insertNil/whisker proof-relevant KuuNativeOneStep;
* the original arbitrary finite refl/snoc KuuNativeAxisTrace.

The code stores complete original typed blocks and paths and an
arbitrary recursive prior OneStep or prior AxisTrace proof. The
partial decoders reject source/target or intermediate boundary type
mismatches; strict decode-after-encode recovers the actual dependent
original proof term, including all intermediate independent partitions.

We distinguish locally countable categories (Countable objects and
Countable every Hom fiber) from arbitrary input D/E categories.
We specialize to the genuine finite C60 Site incidence category and
its full original proof-bearing paths and partitions. This does NOT
automatically prove the full original F45/F55 through 14D Type values
Countable, nor an unconditional physical exact aleph-null normal rank.

Append only. 107 public roots, independent Kuu presentation retained,
strict Kuu primary, no Gray, no 19D filler. Lean v4.30.0-rc2,
pinned mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
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

/-- All ORIGINAL arguments to split in their true source-dependent
C objects, blocks and unflattened native categorical paths. -/
abbrev NativeGGOriginalSplitTotal (C : Type u) [Category.{v} C] :
    Type (max u v) :=
  Σ w : C, Σ x : C, Σ y : C, Σ z : C,
    KuuNativeBlocks w x × KuuNativePath x y × KuuNativePath y z

/-- The complete actual original source/target and TWO block
endpoints of any independent OneStep proof. -/
abbrev NativeGGOriginalOneStepTotal (C : Type u) [Category.{v} C] :
    Type (max u v) :=
  Σ x : C, Σ y : C, Σ p : KuuNativeBlocks x y,
    Σ q : KuuNativeBlocks x y, KuuNativeOneStep p q

/-- A finite free syntax whose atoms keep entire original source
tokens and whose whisker branch recursively retains the entire
original lower OneStep grammar. -/
inductive NativeGGOneStepPlainSyntax
    (Split : Type u) (Nil : Type v) (Path : Type w) :
    Type (max (max u v) w) where
  | split (s : Split)
  | insertNil (b : Nil)
  | whisker (h : NativeGGOneStepPlainSyntax Split Nil Path) (p : Path)
  deriving Countable

/-- Exact original three-constructor KuuNativeOneStep encoder. -/
def nativeGGEncodeOneStep {C : Type u} [Category.{v} C] :
    {x y : C} → {p q : KuuNativeBlocks x y} →
    KuuNativeOneStep p q →
    NativeGGOneStepPlainSyntax
      (NativeGGOriginalSplitTotal C)
      (NativeGFOriginalBlocksTotal C)
      (NativeGFOriginalPathTotal C)
  | _, _, _, _, .split p q r => .split ⟨_, _, _, _, (p, q, r)⟩
  | _, _, _, _, .insertNil p => .insertNil ⟨_, _, p⟩
  | _, _, _, _, .whisker h t =>
      .whisker (nativeGGEncodeOneStep h) ⟨_, _, t⟩

/-- Partial typed interpretation of full original OneStep proofs.
The only forgettable information is the failed branch of a
non-composable arbitrary code, NEVER an existing original proof. -/
noncomputable def nativeGGDecodeOneStep {C : Type u} [Category.{v} C] :
    NativeGGOneStepPlainSyntax
      (NativeGGOriginalSplitTotal C)
      (NativeGFOriginalBlocksTotal C)
      (NativeGFOriginalPathTotal C) →
    Option (NativeGGOriginalOneStepTotal C)
  | .split ⟨w, x, y, z, (p, q, r)⟩ =>
      some ⟨w, z, .snoc p (q.append r),
        .snoc (.snoc p q) r, .split p q r⟩
  | .insertNil ⟨x, y, p⟩ =>
      some ⟨x, y, p, .snoc p (.nil y), .insertNil p⟩
  | .whisker code ⟨z, w, t⟩ => by
      classical
      exact (nativeGGDecodeOneStep code).bind
        (fun ⟨x, y, p, q, h⟩ =>
          if hz : y = z then
            some ⟨x, w, .snoc p (hz.symm ▸ t),
              .snoc q (hz.symm ▸ t), .whisker h (hz.symm ▸ t)⟩
          else none)

/-- The full dependent OneStep proof, including all original
source/target blocks and nested whisker evidence, is reproduced
exactly from the finite code for arbitrary finite recursion. -/
theorem nativeGGDecode_encodeOneStep {C : Type u} [Category.{v} C]
    {x y : C} {p q : KuuNativeBlocks x y}
    (h : KuuNativeOneStep p q) :
    nativeGGDecodeOneStep (nativeGGEncodeOneStep h) =
      some (⟨x, y, p, q, h⟩ : NativeGGOriginalOneStepTotal C) := by
  induction h with
  | split p q r =>
      simp [nativeGGEncodeOneStep, nativeGGDecodeOneStep]
  | insertNil p =>
      simp [nativeGGEncodeOneStep, nativeGGDecodeOneStep]
  | whisker h t ih =>
      simp [nativeGGEncodeOneStep, nativeGGDecodeOneStep, ih]

/-- Source smallness for split's ORIGINAL three proof-carrying
primitive arguments and all their actual categorical endpoints. -/
theorem nativeGGOriginalSplitTotal_countable
    {C : Type u} [Category.{v} C]
    (hobj : Countable C)
    (hhom : ∀ x y : C, Countable (x ⟶ y)) :
    Countable (NativeGGOriginalSplitTotal C) := by
  letI : Countable C := hobj
  letI : ∀ x y : C, Countable (KuuNativePath x y) :=
    nativeGFOriginalPathFiber_countable hobj hhom
  letI : ∀ x y : C, Countable (KuuNativeBlocks x y) :=
    nativeGFOriginalBlocksFiber_countable hobj hhom
  infer_instance

/-- All original Type-valued source-indexed OneStep proof objects
and their four exact endpoints form a Countable alphabet. -/
theorem nativeGGOriginalOneStepTotal_countable
    {C : Type u} [Category.{v} C]
    (hobj : Countable C)
    (hhom : ∀ x y : C, Countable (x ⟶ y)) :
    Countable (NativeGGOriginalOneStepTotal C) := by
  letI : Countable (NativeGGOriginalSplitTotal C) :=
    nativeGGOriginalSplitTotal_countable hobj hhom
  letI : Countable (NativeGFOriginalBlocksTotal C) :=
    nativeGFOriginalBlocksTotal_countable hobj hhom
  letI : Countable (NativeGFOriginalPathTotal C) :=
    nativeGFOriginalPathTotal_countable hobj hhom
  haveI : Countable (NativeGGOneStepPlainSyntax
      (NativeGGOriginalSplitTotal C)
      (NativeGFOriginalBlocksTotal C)
      (NativeGFOriginalPathTotal C)) :=
    inferInstance
  have hrange : (Set.range (nativeGGDecodeOneStep (C := C))).Countable :=
    Set.countable_range _
  letI : Countable (Set.range (nativeGGDecodeOneStep (C := C))) :=
    hrange.to_subtype
  let embedding : NativeGGOriginalOneStepTotal C →
      Set.range (nativeGGDecodeOneStep (C := C)) :=
    fun t => ⟨some t, by
      rcases t with ⟨x, y, p, q, h⟩
      exact ⟨nativeGGEncodeOneStep h, nativeGGDecode_encodeOneStep h⟩⟩
  have hinj : Function.Injective embedding := by
    intro t s h
    have ht : (some t : Option (NativeGGOriginalOneStepTotal C)) =
        some s := congrArg
          (fun z : Set.range (nativeGGDecodeOneStep (C := C)) => z.1) h
    exact Option.some.inj ht
  exact hinj.countable

/-- Countable every exact ORIGINAL source/target block comparison
fiber, not an observer quotient or a generic F45 proxy. -/
theorem nativeGGOriginalOneStepFiber_countable
    {C : Type u} [Category.{v} C]
    (hobj : Countable C)
    (hhom : ∀ x y : C, Countable (x ⟶ y))
    (x y : C) (p q : KuuNativeBlocks x y) :
    Countable (KuuNativeOneStep p q) := by
  letI : Countable (NativeGGOriginalOneStepTotal C) :=
    nativeGGOriginalOneStepTotal_countable hobj hhom
  have hinj : Function.Injective
      (fun h : KuuNativeOneStep p q =>
        (⟨x, y, p, q, h⟩ : NativeGGOriginalOneStepTotal C)) := by
    intro h k eq
    have e1 :
        (⟨y, p, q, h⟩ :
          Σ y : C, Σ p : KuuNativeBlocks x y,
            Σ q : KuuNativeBlocks x y, KuuNativeOneStep p q) =
        ⟨y, p, q, k⟩ :=
      eq_of_heq (Sigma.mk.inj eq).2
    have e2 :
        (⟨p, q, h⟩ :
          Σ p : KuuNativeBlocks x y,
            Σ q : KuuNativeBlocks x y, KuuNativeOneStep p q) =
        ⟨p, q, k⟩ :=
      eq_of_heq (Sigma.mk.inj e1).2
    have e3 :
        (⟨q, h⟩ :
          Σ q : KuuNativeBlocks x y, KuuNativeOneStep p q) =
        ⟨q, k⟩ :=
      eq_of_heq (Sigma.mk.inj e2).2
    exact eq_of_heq (Sigma.mk.inj e3).2
  exact hinj.countable

/-- The full original EXACT n-step trace total retains the
source/target category objects, start/end original block proofs,
each independent primitive step, and all intermediate blocks. -/
abbrev NativeGGOriginalAxisTraceTotal (C : Type u) [Category.{v} C] :
    Type (max u v) :=
  Σ x : C, Σ y : C, Σ n : Nat,
    Σ p : KuuNativeBlocks x y, Σ q : KuuNativeBlocks x y,
      KuuNativeAxisTrace n p q

/-- Finite recursive source representation with original complete
block tokens at refl, and full original OneStep proof at each snoc. -/
inductive NativeGGAxisTracePlainSyntax
    (Block : Type u) (Step : Type v) : Type (max u v) where
  | refl (b : Block)
  | snoc (h : NativeGGAxisTracePlainSyntax Block Step) (s : Step)
  deriving Countable

/-- Encode the genuine original source-indexed trace. Every
intermediate ORIGINAL Type-valued OneStep is stored exactly. -/
def nativeGGEncodeAxisTrace {C : Type u} [Category.{v} C] :
    {x y : C} → {n : Nat} → {p q : KuuNativeBlocks x y} →
    KuuNativeAxisTrace n p q →
    NativeGGAxisTracePlainSyntax
      (NativeGFOriginalBlocksTotal C) (NativeGGOriginalOneStepTotal C)
  | _, _, _, _, _, .refl p => .refl ⟨_, _, p⟩
  | _, _, _, _, _, .snoc h step =>
      .snoc (nativeGGEncodeAxisTrace h) ⟨_, _, _, _, step⟩

/-- Only genuinely matching original source/target and intermediate
block boundaries can be concatenated into an original trace. -/
noncomputable def nativeGGAxisTraceAppendExact {C : Type u}
    [Category.{v} C]
    (raw : NativeGGOriginalAxisTraceTotal C)
    (atom : NativeGGOriginalOneStepTotal C) :
    Option (NativeGGOriginalAxisTraceTotal C) := by
  classical
  rcases raw with ⟨x, y, n, p, q, h⟩
  rcases atom with ⟨x', y', q', r, step⟩
  by_cases hx : x = x'
  · subst x'
    by_cases hy : y = y'
    · subst y'
      by_cases hq : q = q'
      · subst q'
        exact some ⟨x, y, n + 1, p, r, .snoc h step⟩
      · exact none
    · exact none
  · exact none

/-- Partial decoder of every genuine finite indexed trace, without
assuming comparison proof terms are mere propositional equality. -/
noncomputable def nativeGGDecodeAxisTrace {C : Type u}
    [Category.{v} C] :
    NativeGGAxisTracePlainSyntax
      (NativeGFOriginalBlocksTotal C) (NativeGGOriginalOneStepTotal C) →
    Option (NativeGGOriginalAxisTraceTotal C)
  | .refl ⟨x, y, p⟩ => some ⟨x, y, 0, p, p, .refl p⟩
  | .snoc priorCode step =>
      (nativeGGDecodeAxisTrace priorCode).bind
        (fun prior => nativeGGAxisTraceAppendExact prior step)

/-- The exact append of two correctly matching genuine original
sources is the genuine original recursive trace snoc, not its
flattened or evaluated image. -/
theorem nativeGGAxisTraceAppendExact_eq {C : Type u}
    [Category.{v} C] {x y : C} {n : Nat}
    {p q r : KuuNativeBlocks x y}
    (h : KuuNativeAxisTrace n p q) (s : KuuNativeOneStep q r) :
    nativeGGAxisTraceAppendExact
      (⟨x, y, n, p, q, h⟩ : NativeGGOriginalAxisTraceTotal C)
      (⟨x, y, q, r, s⟩ : NativeGGOriginalOneStepTotal C) =
    some ⟨x, y, n + 1, p, r, .snoc h s⟩ := by
  simp [nativeGGAxisTraceAppendExact]

/-- The full source-indexed ORIGINAL AXIS TRACE, including every
independent intermediate Type-valued block and proof, survives the
exact dependent encode/decode cycle for arbitrary finite n. -/
theorem nativeGGDecode_encodeAxisTrace {C : Type u}
    [Category.{v} C] {x y : C} {n : Nat}
    {p q : KuuNativeBlocks x y}
    (h : KuuNativeAxisTrace n p q) :
    nativeGGDecodeAxisTrace (nativeGGEncodeAxisTrace h) =
      some (⟨x, y, n, p, q, h⟩ :
        NativeGGOriginalAxisTraceTotal C) := by
  induction h with
  | refl =>
      simp [nativeGGEncodeAxisTrace, nativeGGDecodeAxisTrace]
  | snoc h step ih =>
      simp [nativeGGEncodeAxisTrace, nativeGGDecodeAxisTrace,
        ih, nativeGGAxisTraceAppendExact_eq]

/-- Countable the full original arbitrary-n trace total follows
from Countable the ORIGINAL blocks and full ORIGINAL OneStep atoms,
NOT from an arbitrarily simplified trace length or scalar charge. -/
theorem nativeGGOriginalAxisTraceTotal_countable
    {C : Type u} [Category.{v} C]
    (hobj : Countable C)
    (hhom : ∀ x y : C, Countable (x ⟶ y)) :
    Countable (NativeGGOriginalAxisTraceTotal C) := by
  letI : Countable (NativeGFOriginalBlocksTotal C) :=
    nativeGFOriginalBlocksTotal_countable hobj hhom
  letI : Countable (NativeGGOriginalOneStepTotal C) :=
    nativeGGOriginalOneStepTotal_countable hobj hhom
  haveI : Countable (NativeGGAxisTracePlainSyntax
      (NativeGFOriginalBlocksTotal C) (NativeGGOriginalOneStepTotal C)) :=
    inferInstance
  have hrange : (Set.range (nativeGGDecodeAxisTrace (C := C))).Countable :=
    Set.countable_range _
  letI : Countable (Set.range (nativeGGDecodeAxisTrace (C := C))) :=
    hrange.to_subtype
  let embedding : NativeGGOriginalAxisTraceTotal C →
      Set.range (nativeGGDecodeAxisTrace (C := C)) :=
    fun t => ⟨some t, by
      rcases t with ⟨x, y, n, p, q, h⟩
      exact ⟨nativeGGEncodeAxisTrace h, nativeGGDecode_encodeAxisTrace h⟩⟩
  have hinj : Function.Injective embedding := by
    intro t s h
    have ht : (some t : Option (NativeGGOriginalAxisTraceTotal C)) =
        some s := congrArg
          (fun z : Set.range (nativeGGDecodeAxisTrace (C := C)) => z.1) h
    exact Option.some.inj ht
  exact hinj.countable

/-- For ANY genuine finite n and any original source and target
blocks, the exact n-step Type-valued trace fiber is Countable. -/
theorem nativeGGOriginalAxisTraceFiber_countable
    {C : Type u} [Category.{v} C]
    (hobj : Countable C)
    (hhom : ∀ x y : C, Countable (x ⟶ y))
    (x y : C) (n : Nat) (p q : KuuNativeBlocks x y) :
    Countable (KuuNativeAxisTrace n p q) := by
  letI : Countable (NativeGGOriginalAxisTraceTotal C) :=
    nativeGGOriginalAxisTraceTotal_countable hobj hhom
  have hinj : Function.Injective
      (fun h : KuuNativeAxisTrace n p q =>
        (⟨x, y, n, p, q, h⟩ :
          NativeGGOriginalAxisTraceTotal C)) := by
    intro h k eq
    have e1 :
        (⟨y, n, p, q, h⟩ :
          Σ y : C, Σ n : Nat, Σ p : KuuNativeBlocks x y,
            Σ q : KuuNativeBlocks x y, KuuNativeAxisTrace n p q) =
        ⟨y, n, p, q, k⟩ :=
      eq_of_heq (Sigma.mk.inj eq).2
    have e2 :
        (⟨n, p, q, h⟩ :
          Σ n : Nat, Σ p : KuuNativeBlocks x y,
            Σ q : KuuNativeBlocks x y, KuuNativeAxisTrace n p q) =
        ⟨n, p, q, k⟩ :=
      eq_of_heq (Sigma.mk.inj e1).2
    have e3 :
        (⟨p, q, h⟩ :
          Σ p : KuuNativeBlocks x y,
            Σ q : KuuNativeBlocks x y, KuuNativeAxisTrace n p q) =
        ⟨p, q, k⟩ :=
      eq_of_heq (Sigma.mk.inj e2).2
    have e4 :
        (⟨q, h⟩ :
          Σ q : KuuNativeBlocks x y, KuuNativeAxisTrace n p q) =
        ⟨q, k⟩ :=
      eq_of_heq (Sigma.mk.inj e3).2
    exact eq_of_heq (Sigma.mk.inj e4).2
  exact hinj.countable

/-- Specialize all source-sized theorem gates to the TRUE finite
C60 incidence Site category, without postulating extra Hom. -/
theorem nativeGGPhysicalOneStepTotal_countable :
    Countable (NativeGGOriginalOneStepTotal Site) :=
  nativeGGOriginalOneStepTotal_countable
    nativeC60GEPhysicalSite_countable
    nativeC60GEPhysicalIncidenceHom_countable

theorem nativeGGPhysicalOneStepFiber_countable
    (x y : Site) (p q : KuuNativeBlocks x y) :
    Countable (KuuNativeOneStep p q) :=
  nativeGGOriginalOneStepFiber_countable
    nativeC60GEPhysicalSite_countable
    nativeC60GEPhysicalIncidenceHom_countable x y p q

theorem nativeGGPhysicalAxisTraceTotal_countable :
    Countable (NativeGGOriginalAxisTraceTotal Site) :=
  nativeGGOriginalAxisTraceTotal_countable
    nativeC60GEPhysicalSite_countable
    nativeC60GEPhysicalIncidenceHom_countable

theorem nativeGGPhysicalAxisTraceFiber_countable
    (x y : Site) (n : Nat) (p q : KuuNativeBlocks x y) :
    Countable (KuuNativeAxisTrace n p q) :=
  nativeGGOriginalAxisTraceFiber_countable
    nativeC60GEPhysicalSite_countable
    nativeC60GEPhysicalIncidenceHom_countable x y n p q

#print axioms nativeGGDecode_encodeOneStep
#print axioms nativeGGOriginalSplitTotal_countable
#print axioms nativeGGOriginalOneStepTotal_countable
#print axioms nativeGGOriginalOneStepFiber_countable
#print axioms nativeGGAxisTraceAppendExact_eq
#print axioms nativeGGDecode_encodeAxisTrace
#print axioms nativeGGOriginalAxisTraceTotal_countable
#print axioms nativeGGOriginalAxisTraceFiber_countable
#print axioms nativeGGPhysicalOneStepTotal_countable
#print axioms nativeGGPhysicalOneStepFiber_countable
#print axioms nativeGGPhysicalAxisTraceTotal_countable
#print axioms nativeGGPhysicalAxisTraceFiber_countable

end
end Kuu.F112.Physical
