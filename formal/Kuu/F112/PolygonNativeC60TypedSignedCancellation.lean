import Kuu.F112.PolygonNativeC60UnboundedTypedPositiveChains

/-!
# F112-P94D3CA — arbitrary finite typed signed 16D paths and cancellation

BZ establishes positive-chain reflection at any finite length for a fixed
full 15D intermediate-object skeleton. CA permits BOTH orientations of
independently supplied, genuine BC higher generators at EVERY step.
Every edge carries its original dependent 15D endpoints, with arbitrary
finite length and intermediate objects encoded in the indexed constructors.

The full signed provenance trace computes the original noncommutative
FreeGroup holonomy and has a canonical Church–Rosser reduced trace from BY.
For all genuine finite AQ contexts, selected strict Kuu quotient laws
cancel an adjacent generator and its inverse, without equating the raw
dependent constructors. The elementary typed cancellation relation also
supports cancellation below arbitrary positive or negative path prefixes;
its finite reflexive-transitive closure is sound in the existing strict
category.

The equality of reduced free words is a NECESSARY condition for strict
equality, not here asserted to be sufficient for arbitrary different
intermediate 15D skeletons. No global Hom faithfulness, all-geometric
16-cell coherence, Peiffer middle-four, Gray category, new axioms,
sorry/admit, or modifications of the public 107 roots are introduced.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u

/-- A proof-bearing path of any finite length. Every step is one genuine
BC generator, taken either in the positive or in the inverse direction.
The entire original 15D intermediate-object skeleton is kept in TYPES. -/
inductive NativeC60CASignedChain {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L) :
    L.Total → L.Total → Type u where
  | nil (a : L.Total) : NativeC60CASignedChain S F a a
  | pos {a b c : L.Total}
      (g : (nativeC60BCClosedSignature S F).Gen a b)
      (tail : NativeC60CASignedChain S F b c) :
      NativeC60CASignedChain S F a c
  | neg {a b c : L.Total}
      (g : (nativeC60BCClosedSignature S F).Gen b a)
      (tail : NativeC60CASignedChain S F b c) :
      NativeC60CASignedChain S F a c

/-- Interpret the entire typed path in the existing, UNSIMPLIFIED raw
AX comparison syntax. In particular, cancellation is not a raw equality. -/
def nativeC60CAChainStep {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L) :
    {a b : L.Total} → NativeC60CASignedChain S F a b →
      NativeC60AXStep (nativeC60BCClosedSignature S F) a b
  | _, _, .nil a => .refl a
  | _, _, .pos g tail => .trans (.atom g) (nativeC60CAChainStep S F tail)
  | _, _, .neg g tail => .trans (.symm (.atom g)) (nativeC60CAChainStep S F tail)

/-- A COMPLETE signed provenance list, recording each original 16D
generator as well as the orientation of its use. -/
def nativeC60CAChainSignedCodes {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L) :
    {a b : L.Total} → NativeC60CASignedChain S F a b →
      List (NativeC60BVGeneratorCode S × Bool)
  | _, _, .nil _ => []
  | _, _, .pos g tail =>
      (nativeC60BVGeneratorCode S F g, true) ::
        nativeC60CAChainSignedCodes S F tail
  | _, _, .neg g tail =>
      (nativeC60BVGeneratorCode S F g, false) ::
        nativeC60CAChainSignedCodes S F tail

/-- Both signs of every genuinely typed generator contribute exactly
their own FreeGroup letter to the whole 16D comparison. -/
theorem nativeC60CAChain_holonomy
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {a b : L.Total} (p : NativeC60CASignedChain S F a b) :
    nativeC60BWFreeHolonomy S F (nativeC60CAChainStep S F p) =
      FreeGroup.mk (nativeC60CAChainSignedCodes S F p) := by
  induction p with
  | nil a =>
      rfl
  | pos g tail ih =>
      change FreeGroup.mk [(nativeC60BVGeneratorCode S F g, true)] *
          nativeC60BWFreeHolonomy S F (nativeC60CAChainStep S F tail) =
        FreeGroup.mk ((nativeC60BVGeneratorCode S F g, true) ::
          nativeC60CAChainSignedCodes S F tail)
      rw [ih]
      simp only [FreeGroup.mul_mk, List.singleton_append]
  | neg g tail ih =>
      change (FreeGroup.mk [(nativeC60BVGeneratorCode S F g, true)])⁻¹ *
          nativeC60BWFreeHolonomy S F (nativeC60CAChainStep S F tail) =
        FreeGroup.mk ((nativeC60BVGeneratorCode S F g, false) ::
          nativeC60CAChainSignedCodes S F tail)
      rw [ih, FreeGroup.inv_mk, FreeGroup.mul_mk]
      rfl

/-- The BY reduced signed word is EXACTLY the Church–Rosser normal
form of the whole freely composed mixed-sign path. In particular,
the equivalence is not a raw higher-cell equality. -/
theorem nativeC60CAChain_reduced_eq_iff
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {a b : L.Total} (p q : NativeC60CASignedChain S F a b) :
    nativeC60BYReducedTrace S F (nativeC60CAChainStep S F p) =
        nativeC60BYReducedTrace S F (nativeC60CAChainStep S F q) ↔
      FreeGroup.mk (nativeC60CAChainSignedCodes S F p) =
        FreeGroup.mk (nativeC60CAChainSignedCodes S F q) := by
  simpa only [nativeC60CAChain_holonomy S F p,
    nativeC60CAChain_holonomy S F q] using
    (nativeC60BYReducedTrace_eq_iff S F
      (nativeC60CAChainStep S F p) (nativeC60CAChainStep S F q))

/-- Existing selected strict Kuu realization of a genuine signed path
after an arbitrary finite AQ word. -/
def nativeC60CAChainStrictFrame
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (word : List Bool) {a b : L.Total}
    (p : NativeC60CASignedChain S F a b) :=
  nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
    (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
    (nativeC60BCMapClosedStep S F word (nativeC60CAChainStep S F p))

/-- Genuine source a -> b -> a detours are removed in the SELECTED
STRICT QUOTIENT, for every finite AQ context and arbitrary continuation.
The original raw AX syntax remains proof-relevant and unreduced. -/
theorem nativeC60CA_pos_neg_strict_cancel
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (word : List Bool) {a b c : L.Total}
    (g : (nativeC60BCClosedSignature S F).Gen a b)
    (tail : NativeC60CASignedChain S F a c) :
    nativeC60CAChainStrictFrame S F word (.pos g (.neg g tail)) =
      nativeC60CAChainStrictFrame S F word tail := by
  change nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
      (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
      (.trans (.atom (nativeC60BCShiftGen S F word g))
        (.trans (.symm (.atom (nativeC60BCShiftGen S F word g)))
          (nativeC60BCMapClosedStep S F word
            (nativeC60CAChainStep S F tail)))) =
    nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
      (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
      (nativeC60BCMapClosedStep S F word (nativeC60CAChainStep S F tail))
  rw [nativeC60AZStrictStep_comp, nativeC60AZStrictStep_comp,
    ← Category.assoc, nativeC60AZStrictStep_inv_left, Category.id_comp]

/-- The other genuine typed critical pair b -> a -> b cancels under
the existing strict laws, again under ALL finite physical AQ contexts. -/
theorem nativeC60CA_neg_pos_strict_cancel
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (word : List Bool) {a b c : L.Total}
    (g : (nativeC60BCClosedSignature S F).Gen a b)
    (tail : NativeC60CASignedChain S F b c) :
    nativeC60CAChainStrictFrame S F word (.neg g (.pos g tail)) =
      nativeC60CAChainStrictFrame S F word tail := by
  change nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
      (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
      (.trans (.symm (.atom (nativeC60BCShiftGen S F word g)))
        (.trans (.atom (nativeC60BCShiftGen S F word g))
          (nativeC60BCMapClosedStep S F word
            (nativeC60CAChainStep S F tail)))) =
    nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
      (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
      (nativeC60BCMapClosedStep S F word (nativeC60CAChainStep S F tail))
  rw [nativeC60AZStrictStep_comp, nativeC60AZStrictStep_comp,
    ← Category.assoc, nativeC60AZStrictStep_inv_right, Category.id_comp]

/-- Elementary, genuinely TYPED cancellation at an arbitrary position.
The congruence constructors descend below either orientation of prefix
without discarding the intervening original 15D boundary. -/
inductive NativeC60CAElementaryCancel {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L) :
    {a b : L.Total} → NativeC60CASignedChain S F a b →
      NativeC60CASignedChain S F a b → Prop where
  | pos_neg {a b c : L.Total}
      (g : (nativeC60BCClosedSignature S F).Gen a b)
      (tail : NativeC60CASignedChain S F a c) :
      NativeC60CAElementaryCancel S F (.pos g (.neg g tail)) tail
  | neg_pos {a b c : L.Total}
      (g : (nativeC60BCClosedSignature S F).Gen a b)
      (tail : NativeC60CASignedChain S F b c) :
      NativeC60CAElementaryCancel S F (.neg g (.pos g tail)) tail
  | pos_congr {a b c : L.Total}
      (g : (nativeC60BCClosedSignature S F).Gen a b)
      {p q : NativeC60CASignedChain S F b c}
      (h : NativeC60CAElementaryCancel S F p q) :
      NativeC60CAElementaryCancel S F (.pos g p) (.pos g q)
  | neg_congr {a b c : L.Total}
      (g : (nativeC60BCClosedSignature S F).Gen b a)
      {p q : NativeC60CASignedChain S F b c}
      (h : NativeC60CAElementaryCancel S F p q) :
      NativeC60CAElementaryCancel S F (.neg g p) (.neg g q)

/-- Every one-step typed reduction is sound on EXACT original strict
Kuu Hom arrows, including the positive and negative prefix rules. -/
theorem nativeC60CAElementaryCancel_sound
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (word : List Bool) {a b : L.Total}
    {p q : NativeC60CASignedChain S F a b}
    (h : NativeC60CAElementaryCancel S F p q) :
    nativeC60CAChainStrictFrame S F word p =
      nativeC60CAChainStrictFrame S F word q := by
  induction h with
  | pos_neg g tail =>
      exact nativeC60CA_pos_neg_strict_cancel S F word g tail
  | neg_pos g tail =>
      exact nativeC60CA_neg_pos_strict_cancel S F word g tail
  | pos_congr g h ih =>
      simp only [nativeC60CAChainStrictFrame, nativeC60CAChainStep,
        nativeC60BCMapClosedStep_trans, nativeC60AZStrictStep_comp] at ih ⊢
      rw [ih]
  | neg_congr g h ih =>
      simp only [nativeC60CAChainStrictFrame, nativeC60CAChainStep,
        nativeC60BCMapClosedStep_trans, nativeC60AZStrictStep_comp] at ih ⊢
      rw [ih]

/-- Arbitrarily many typed cancellations are sound in the chosen strict
quotient for every finite AQ word; length and intermediate skeleton may
both change. This is NOT the unproved converse normalization theorem. -/
theorem nativeC60CAFiniteCancellation_sound
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (word : List Bool) {a b : L.Total}
    {p q : NativeC60CASignedChain S F a b}
    (h : Relation.ReflTransGen
      (fun x y : NativeC60CASignedChain S F a b =>
        NativeC60CAElementaryCancel S F x y) p q) :
    nativeC60CAChainStrictFrame S F word p =
      nativeC60CAChainStrictFrame S F word q := by
  induction h with
  | refl => rfl
  | tail _ hstep ih =>
      exact ih.trans (nativeC60CAElementaryCancel_sound S F word hstep)

/-- A common-endpoint strict equality NECESSARILY has the same complete
reduced signed 16D provenance trace, even for different 15D skeletons. -/
theorem nativeC60CA_strict_eq_implies_reduced_eq
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (word : List Bool) {a b : L.Total}
    (p q : NativeC60CASignedChain S F a b)
    (h : nativeC60CAChainStrictFrame S F word p =
      nativeC60CAChainStrictFrame S F word q) :
    nativeC60BYReducedTrace S F (nativeC60CAChainStep S F p) =
      nativeC60BYReducedTrace S F (nativeC60CAChainStep S F q) := by
  have hrel :=
    (nativeC60AZStrictStep_exact
      (nativeC60BCClosedSignature S F)
      (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
      (nativeC60BCMapClosedStep S F word (nativeC60CAChainStep S F p))
      (nativeC60BCMapClosedStep S F word (nativeC60CAChainStep S F q))).mp h
  exact (nativeC60BYReducedTrace_eq_iff S F
      (nativeC60CAChainStep S F p) (nativeC60CAChainStep S F q)).mpr
    (nativeC60BWFreeHolonomy_reflects_contextual_replaceable
      S F word (nativeC60CAChainStep S F p)
      (nativeC60CAChainStep S F q) hrel)

#print axioms nativeC60CAChain_holonomy
#print axioms nativeC60CAChain_reduced_eq_iff
#print axioms nativeC60CA_pos_neg_strict_cancel
#print axioms nativeC60CA_neg_pos_strict_cancel
#print axioms nativeC60CAElementaryCancel_sound
#print axioms nativeC60CAFiniteCancellation_sound
#print axioms nativeC60CA_strict_eq_implies_reduced_eq

end
end Kuu.F112.Physical
