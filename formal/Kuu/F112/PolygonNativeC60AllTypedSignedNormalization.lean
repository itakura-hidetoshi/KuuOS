import Kuu.F112.PolygonNativeC60TypedSignedReducedReflection

/-!
# F112-P94D3CC — normalization of ALL typed signed 16D chains

CA defined the actual dependent finite signed sixteen-dimensional comparison
chains and proved cancellation in the existing selected strict Kuu quotient.
CB showed that the complete provenance code determines every original 15D
intermediate object and every original higher generator, and established
strict/full-free equality reflection whenever typed reduced normal forms
exist.

CC DISCHARGES that normalization-existence hypothesis for EVERY finite
signed BC generator chain. The proof recursively normalizes the genuine
typed tail, then prepends the next original generator. If the two adjacent
opposite signed code letters coincide, the complete code allows recovery
of the exact original 15D intermediate endpoint AND original generator;
the corresponding CA typed reduction removes the adjacent inverse pair.
Otherwise the full signed code list remains FreeGroup.IsReduced under
Mathlib's isReduced_cons_cons criterion. The argument uses no graph-level
fake cancellation or presumed equality of raw proof terms.

Combining unconditional typed normalization with CB yields the genuine
two-sided free-word <-> selected strict Kuu Hom equality reflection for
ALL arbitrary finite signed BC chains, all ordered finite genuine AQ
contexts, and WITHOUT requiring a fixed complete intermediate skeleton.

This is not a claim about arbitrary AX raw terms featuring composite
symmetry/parentheses, geometric 16-cell coherence, original P92B descent,
unconditional horizontal Peiffer or a global strict 3/n-category.
No new axioms, sorry/admit, Gray reintroduction or root changes.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u

/-- Removing the first signed letter from a reduced signed code list
preserves reducedness; this is the adjacency criterion in Mathlib. -/
theorem nativeC60CCReduced_tail
    {α : Type u} (x : α × Bool) (xs : List (α × Bool))
    (h : FreeGroup.IsReduced (x :: xs)) :
    FreeGroup.IsReduced xs := by
  cases xs with
  | nil =>
      exact FreeGroup.IsReduced.nil
  | cons y ys =>
      exact (FreeGroup.isReduced_cons_cons.mp h).2

/-- A typed positive prefix transports any finite CA cancellation
sequence without losing the original 15D intermediate endpoint. -/
theorem nativeC60CCPos_prefix
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {a b c : L.Total}
    (g : (nativeC60BCClosedSignature S F).Gen a b)
    {p q : NativeC60CASignedChain S F b c}
    (h : Relation.ReflTransGen
      (fun x y : NativeC60CASignedChain S F b c =>
        NativeC60CAElementaryCancel S F x y) p q) :
    Relation.ReflTransGen
      (fun x y : NativeC60CASignedChain S F a c =>
        NativeC60CAElementaryCancel S F x y)
      (.pos g p) (.pos g q) := by
  induction h with
  | refl =>
      exact .refl
  | tail _ hstep ih =>
      exact .tail ih (.pos_congr g hstep)

/-- A typed negative prefix likewise preserves genuine dependent
source/target information at every step of finite normalization. -/
theorem nativeC60CCNeg_prefix
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {a b c : L.Total}
    (g : (nativeC60BCClosedSignature S F).Gen b a)
    {p q : NativeC60CASignedChain S F b c}
    (h : Relation.ReflTransGen
      (fun x y : NativeC60CASignedChain S F b c =>
        NativeC60CAElementaryCancel S F x y) p q) :
    Relation.ReflTransGen
      (fun x y : NativeC60CASignedChain S F a c =>
        NativeC60CAElementaryCancel S F x y)
      (.neg g p) (.neg g q) := by
  induction h with
  | refl =>
      exact .refl
  | tail _ hstep ih =>
      exact .tail ih (.neg_congr g hstep)

/-- Prepended positive BC generators normalize in AT MOST ONE further
genuine typed cancellation, provided the original dependent tail is
already reduced. This includes the cancellation of its original
intermediate 15D object, not only its complete FreeGroup code. -/
theorem nativeC60CCPrepend_pos
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {a b c : L.Total}
    (g : (nativeC60BCClosedSignature S F).Gen a b)
    (p : NativeC60CASignedChain S F b c)
    (hp : FreeGroup.IsReduced (nativeC60CAChainSignedCodes S F p)) :
    ∃ q : NativeC60CASignedChain S F a c,
      Relation.ReflTransGen
        (fun x y : NativeC60CASignedChain S F a c =>
          NativeC60CAElementaryCancel S F x y)
        (.pos g p) q ∧
      FreeGroup.IsReduced (nativeC60CAChainSignedCodes S F q) := by
  classical
  cases p with
  | nil _ =>
      refine ⟨.pos g (.nil _), .refl, ?_⟩
      change FreeGroup.IsReduced [(nativeC60BVGeneratorCode S F g, true)]
      exact FreeGroup.IsReduced.singleton
  | pos h rest =>
      refine ⟨.pos g (.pos h rest), .refl, ?_⟩
      change FreeGroup.IsReduced
        ((nativeC60BVGeneratorCode S F g, true) ::
          (nativeC60BVGeneratorCode S F h, true) ::
            nativeC60CAChainSignedCodes S F rest)
      exact (FreeGroup.isReduced_cons_cons).mpr ⟨(fun _ => rfl), hp⟩
  | neg h rest =>
      by_cases heq : nativeC60BVGeneratorCode S F g =
        nativeC60BVGeneratorCode S F h
      · have hmid :=
          (nativeC60CBGen_source S F g).trans
            ((congrArg (fun code : NativeC60BVGeneratorCode S =>
                nativeC60BCContextTotal F code.1 code.2.1) heq).trans
              (nativeC60CBGen_source S F h).symm)
        cases hmid
        have hgen : g = h :=
          nativeC60BVGeneratorCode_injective S F heq
        cases hgen
        refine ⟨rest, Relation.ReflTransGen.single (.pos_neg g rest), ?_⟩
        exact nativeC60CCReduced_tail _ _ hp
      · refine ⟨.pos g (.neg h rest), .refl, ?_⟩
        change FreeGroup.IsReduced
          ((nativeC60BVGeneratorCode S F g, true) ::
            (nativeC60BVGeneratorCode S F h, false) ::
              nativeC60CAChainSignedCodes S F rest)
        exact (FreeGroup.isReduced_cons_cons).mpr
          ⟨(fun hcode => (heq hcode).elim), hp⟩

/-- The fully dual typed reduction step prepends a NEGATIVE actual
16D generator, respecting the opposite original 15D endpoint. -/
theorem nativeC60CCPrepend_neg
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {a b c : L.Total}
    (g : (nativeC60BCClosedSignature S F).Gen b a)
    (p : NativeC60CASignedChain S F b c)
    (hp : FreeGroup.IsReduced (nativeC60CAChainSignedCodes S F p)) :
    ∃ q : NativeC60CASignedChain S F a c,
      Relation.ReflTransGen
        (fun x y : NativeC60CASignedChain S F a c =>
          NativeC60CAElementaryCancel S F x y)
        (.neg g p) q ∧
      FreeGroup.IsReduced (nativeC60CAChainSignedCodes S F q) := by
  classical
  cases p with
  | nil _ =>
      refine ⟨.neg g (.nil _), .refl, ?_⟩
      change FreeGroup.IsReduced [(nativeC60BVGeneratorCode S F g, false)]
      exact FreeGroup.IsReduced.singleton
  | neg h rest =>
      refine ⟨.neg g (.neg h rest), .refl, ?_⟩
      change FreeGroup.IsReduced
        ((nativeC60BVGeneratorCode S F g, false) ::
          (nativeC60BVGeneratorCode S F h, false) ::
            nativeC60CAChainSignedCodes S F rest)
      exact (FreeGroup.isReduced_cons_cons).mpr ⟨(fun _ => rfl), hp⟩
  | pos h rest =>
      by_cases heq : nativeC60BVGeneratorCode S F g =
        nativeC60BVGeneratorCode S F h
      · have hmid :=
          (nativeC60CBGen_target S F g).trans
            ((congrArg (fun code : NativeC60BVGeneratorCode S =>
                nativeC60BCContextTotal F code.1 code.2.2.1) heq).trans
              (nativeC60CBGen_target S F h).symm)
        cases hmid
        have hgen : g = h :=
          nativeC60BVGeneratorCode_injective S F heq
        cases hgen
        refine ⟨rest, Relation.ReflTransGen.single (.neg_pos g rest), ?_⟩
        exact nativeC60CCReduced_tail _ _ hp
      · refine ⟨.neg g (.pos h rest), .refl, ?_⟩
        change FreeGroup.IsReduced
          ((nativeC60BVGeneratorCode S F g, false) ::
            (nativeC60BVGeneratorCode S F h, true) ::
              nativeC60CAChainSignedCodes S F rest)
        exact (FreeGroup.isReduced_cons_cons).mpr
          ⟨(fun hcode => (heq hcode).elim), hp⟩

/-- EVERY finite proof-bearing signed 16D comparison chain has a
genuine typed reduced normal form with the EXACT same original
15D source and target. The witness is a finite sequence of the
ALREADY DECLARED CA adjacent-inverse reduction rules; NO equality
of raw proof syntax is asserted or silently substituted. -/
theorem nativeC60CCEvery_signed_chain_normalizes
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L) :
    ∀ {a b : L.Total} (p : NativeC60CASignedChain S F a b),
      ∃ q : NativeC60CASignedChain S F a b,
        Relation.ReflTransGen
          (fun x y : NativeC60CASignedChain S F a b =>
            NativeC60CAElementaryCancel S F x y) p q ∧
        FreeGroup.IsReduced (nativeC60CAChainSignedCodes S F q) := by
  intro a b p
  induction p with
  | nil x =>
      exact ⟨.nil x, .refl, FreeGroup.IsReduced.nil⟩
  | pos g rest ih =>
      rcases ih with ⟨q, hredseq, hred⟩
      rcases nativeC60CCPrepend_pos S F g q hred with
        ⟨q', hprefix, hred'⟩
      exact ⟨q', (nativeC60CCPos_prefix S F g hredseq).trans hprefix, hred'⟩
  | neg g rest ih =>
      rcases ih with ⟨q, hredseq, hred⟩
      rcases nativeC60CCPrepend_neg S F g q hred with
        ⟨q', hprefix, hred'⟩
      exact ⟨q', (nativeC60CCNeg_prefix S F g hredseq).trans hprefix, hred'⟩

/-- The FULL bidirectional theorem for ALL arbitrary finite genuine
typed signed 16D paths, without ANY restriction on their original
intermediate 15D object lists: strict equality after ANY finite real
AQ context is equivalent to the complete noncommutative free-word
equality. This discharges CB's normalization-existence hypothesis. -/
theorem nativeC60CCAll_signed_free_eq_iff_strict
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (word : List Bool) {a b : L.Total}
    (p q : NativeC60CASignedChain S F a b) :
    FreeGroup.mk (nativeC60CAChainSignedCodes S F p) =
        FreeGroup.mk (nativeC60CAChainSignedCodes S F q) ↔
      nativeC60CAChainStrictFrame S F word p =
        nativeC60CAChainStrictFrame S F word q := by
  rcases nativeC60CCEvery_signed_chain_normalizes S F p with
    ⟨p', hnormalp, hredp⟩
  rcases nativeC60CCEvery_signed_chain_normalizes S F q with
    ⟨q', hnormalq, hredq⟩
  exact nativeC60CBNormalized_free_eq_iff_strict S F word
    p q p' q' hnormalp hnormalq hredp hredq

/-- Canonical BY reduced signed trace is a COMPLETE strict Hom
invariant on all genuine finite signed chains with fixed original
15D endpoints, even when all intermediate 15D objects differ. -/
theorem nativeC60CCAll_signed_reduced_eq_iff_strict
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (word : List Bool) {a b : L.Total}
    (p q : NativeC60CASignedChain S F a b) :
    nativeC60BYReducedTrace S F (nativeC60CAChainStep S F p) =
      nativeC60BYReducedTrace S F (nativeC60CAChainStep S F q) ↔
      nativeC60CAChainStrictFrame S F word p =
        nativeC60CAChainStrictFrame S F word q :=
  (nativeC60CAChain_reduced_eq_iff S F p q).trans
    (nativeC60CCAll_signed_free_eq_iff_strict S F word p q)

#print axioms nativeC60CCReduced_tail
#print axioms nativeC60CCPos_prefix
#print axioms nativeC60CCNeg_prefix
#print axioms nativeC60CCPrepend_pos
#print axioms nativeC60CCPrepend_neg
#print axioms nativeC60CCEvery_signed_chain_normalizes
#print axioms nativeC60CCAll_signed_free_eq_iff_strict
#print axioms nativeC60CCAll_signed_reduced_eq_iff_strict

end
end Kuu.F112.Physical
