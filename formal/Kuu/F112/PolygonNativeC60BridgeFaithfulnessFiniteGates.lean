import Kuu.F112.PolygonNativeC60BridgeReplacementContextReflection
import Kuu.F112.PolygonNativeC60FiniteStrictFunctorComposition

/-!
# F112-P94D3BV — strict Hom faithfulness frontier of genuine AQ bridge transport

The genuinely typed BC 16D grammar retains a complete closed-generator
certificate: finite prefix word, both original dependent 15D endpoints,
and the actual underlying AX generator. Any finite AQ prefix is injective
on these GENERATOR CERTIFICATES. This does not assert strict Hom
faithfulness merely from equality of generator labels.

The EXACT strict-Hom faithfulness criterion is reflection of the
selected Kuu replacement of ALL full typed raw16D bridge pairs.
Because BA proves EVERY strict morphism has a real AX comparison
representative, this is an equivalence, not just a sufficient test.

NONFAITHFULNESS has an exact existential typed witness: two original
bridges that are not selected-replaceable but become replaceable after
the finite AQ word. The witness is mathematically explicit as a Sigma
predicate; existence for any particular nonempty genuine C60 context
is not assumed.

For the BC no-extra-relations quotient, faithfulness at ALL finite
AQ words is equivalent to faithfulness at precisely the false and true
singleton actions, by the already PROVEN BF strict functor action.
The empty word is automatically faithful. This isolates two concrete
strict gates without inventing a missing geometric 16-cell filler.

BT's independently proven Hom equivalence translates each gate
into reflection of TWO-INPUT BS bridge-gluing equality. These
are exact strict quotient equalities; original free syntax and
noncommutative Peiffer information are NOT identified by observation.

No unproved global faithfulness, no new axioms, sorry, admit, Gray,
global BB horizontal composition, or change to 107 public roots.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u uD vD uE vE

/-- The FULL provenance of a genuine context-closed AX generator,
independent of proof-irrelevant endpoint equality certificates. -/
abbrev NativeC60BVGeneratorCode {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) :=
  List Bool × (Σ a : L.Total, Σ b : L.Total, S.Gen a b)

def nativeC60BVGeneratorCode {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {x y : L.Total}
    (gen : (nativeC60BCClosedSignature S F).Gen x y) :
    NativeC60BVGeneratorCode S :=
  ⟨gen.1, gen.2.1, gen.2.2.1, gen.2.2.2.1⟩

/-- For fixed dependent 15D endpoints, the recorded original generator
and finite-context word determine the complete BC generator. -/
theorem nativeC60BVGeneratorCode_injective
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {x y : L.Total} :
    Function.Injective (fun gen : (nativeC60BCClosedSignature S F).Gen x y =>
      nativeC60BVGeneratorCode S F gen) := by
  intro g h heq
  rcases g with ⟨wg, ag, bg, ⟨gg, hxg, hyg⟩⟩
  rcases h with ⟨wh, ah, bh, ⟨gh, hxh, hyh⟩⟩
  cases heq
  rfl

/-- A true AQ prefix preserves the *entire* generator certificate
after adjoining that prefix. Both original endpoints and the actual
higher generator remain independently recorded. -/
theorem nativeC60BVGeneratorCode_shift
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (word : List Bool) {x y : L.Total}
    (g : (nativeC60BCClosedSignature S F).Gen x y) :
    nativeC60BVGeneratorCode S F (nativeC60BCShiftGen S F word g) =
      (word ++ (nativeC60BVGeneratorCode S F g).1,
        (nativeC60BVGeneratorCode S F g).2) := by
  rcases g with ⟨inner, a, b, ⟨gen, hx, hy⟩⟩
  rfl

/-- All finite AQ prefixes are injective on actual BC higher
generators, EVEN without an injectivity hypothesis on the lower
fourteen-dimensional object action. This is a statement about
GENERATOR SYNTAX, not about the strict quotient Hom map. -/
theorem nativeC60BVShiftGen_injective
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (word : List Bool) {x y : L.Total} :
    Function.Injective
      (fun g : (nativeC60BCClosedSignature S F).Gen x y =>
        nativeC60BCShiftGen S F word g) := by
  intro g h heq
  apply nativeC60BVGeneratorCode_injective S F
  have hc := congrArg (nativeC60BVGeneratorCode S F) heq
  rw [nativeC60BVGeneratorCode_shift S F word g,
    nativeC60BVGeneratorCode_shift S F word h] at hc
  have hw :
      (nativeC60BVGeneratorCode S F g).1 =
        (nativeC60BVGeneratorCode S F h).1 :=
    (List.append_right_inj word).mp (congrArg Prod.fst hc)
  have hp :
      (nativeC60BVGeneratorCode S F g).2 =
        (nativeC60BVGeneratorCode S F h).2 :=
    (Prod.mk.inj hc).2
  exact Prod.ext hw hp

/-- Full Hom faithfulness can be checked entirely on REAL original
raw16D comparison pairs, because BA proves each strict arrow has a
typed representative. No observer quotient is introduced. -/
def NativeC60BVBridgeReflection
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (R : NativeC60AZParallelRelation (nativeC60BCClosedSignature S F))
    (word : List Bool) : Prop :=
  ∀ {a b : L.Total}
    (k k' : NativeC60AXStep (nativeC60BCClosedSignature S F) a b),
    NativeC60BUBridgeReplaceable S F R
        (nativeC60BCMapClosedStep S F word k)
        (nativeC60BCMapClosedStep S F word k') →
      NativeC60BUBridgeReplaceable S F R k k'

/-- Exact necessary-and-sufficient criterion, NOT merely a
one-way faithfulness hypothesis: raw bridge-reflection is equivalent
to strict faithfulness on EVERY existing dependent Hom set. -/
theorem nativeC60BVBridgeReflection_iff_faithful
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (R : NativeC60AZParallelRelation (nativeC60BCClosedSignature S F))
    (word : List Bool) (stable : NativeC60BDContextCongruence S F R word) :
    NativeC60BVBridgeReflection S F R word ↔
      NativeC60BUContextHomFaithful S F R word stable := by
  constructor
  · intro href a b f g hmap
    let T := nativeC60BCClosedSignature S F
    obtain ⟨k, rfl⟩ := nativeC60BAStep_surjective T R a b f
    obtain ⟨k', rfl⟩ := nativeC60BAStep_surjective T R a b g
    apply (nativeC60AZStrictStep_exact T R k k').mpr
    apply href k k'
    apply (nativeC60AZStrictStep_exact T R
      (nativeC60BCMapClosedStep S F word k)
      (nativeC60BCMapClosedStep S F word k')).mp
    simpa only [nativeC60BDStrictContext_step] using hmap
  · intro faithful a b k k' h
    exact nativeC60BUBridge_replaceable_reflect
      S F R word stable faithful k k' h

/-- A fully typed existential collapse of TWO genuine original
raw16D bridges, not the collapse of Peiffer or integer shadows. -/
def NativeC60BVBridgeCollapse
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (R : NativeC60AZParallelRelation (nativeC60BCClosedSignature S F))
    (word : List Bool) : Prop :=
  ∃ (a b : L.Total)
    (k k' : NativeC60AXStep (nativeC60BCClosedSignature S F) a b),
    ¬ NativeC60BUBridgeReplaceable S F R k k' ∧
      NativeC60BUBridgeReplaceable S F R
        (nativeC60BCMapClosedStep S F word k)
        (nativeC60BCMapClosedStep S F word k')

/-- A genuine collapsed raw bridge pair is necessary AND sufficient
for nonfaithfulness of the selected strict quotient AQ context action.
This upgrades BU's conditional one-way obstruction to an EXACT
witness theorem using BA strict-arrow representability. -/
theorem nativeC60BVBridgeCollapse_iff_nonfaithful
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (R : NativeC60AZParallelRelation (nativeC60BCClosedSignature S F))
    (word : List Bool) (stable : NativeC60BDContextCongruence S F R word) :
    NativeC60BVBridgeCollapse S F R word ↔
      ¬ NativeC60BUContextHomFaithful S F R word stable := by
  classical
  constructor
  · rintro ⟨a, b, k, k', hne, hc⟩
    exact nativeC60BUContext_nonfaithful_of_bridge_collapse
      S F R word stable k k' hne hc
  · intro hnf
    by_contra hno
    apply hnf
    apply (nativeC60BVBridgeReflection_iff_faithful
      S F R word stable).mp
    intro a b k k' hctx
    by_contra hbase
    exact hno ⟨a, b, k, k', hbase, hctx⟩

/-- Unconditional faithfulness of the EMPTY physical AQ word in the
no-extra-relations selected strict Kuu presentation. -/
theorem nativeC60BVNoRelations_nil_faithful
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L) :
    NativeC60BUContextHomFaithful S F
      (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
      [] (nativeC60BDNoRelations_context S F []) := by
  intro a b f g h
  change (nativeC60BDNoRelations_strictFunctor S F []).map f =
    (nativeC60BDNoRelations_strictFunctor S F []).map g at h
  rw [nativeC60BFStrictFunctor_nil S F] at h
  exact h

/-- FINITE REDUCTION: full strict-Hom faithfulness for ALL genuine AQ
words is EQUIVALENT to the two TRUE physical singleton gates.
The proof uses actual BF strict FUNCTOR composition, not a
supposed interchange or observer injectivity. The two gates are
obligations, not silently supplied as axioms. -/
theorem nativeC60BVNoRelations_all_faithful_iff_letters
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L) :
    (∀ word : List Bool,
      NativeC60BUContextHomFaithful S F
        (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
        word (nativeC60BDNoRelations_context S F word)) ↔
      NativeC60BUContextHomFaithful S F
          (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
          [false] (nativeC60BDNoRelations_context S F [false]) ∧
        NativeC60BUContextHomFaithful S F
          (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
          [true] (nativeC60BDNoRelations_context S F [true]) := by
  constructor
  · intro h
    exact ⟨h [false], h [true]⟩
  · rintro ⟨hf, ht⟩ word
    induction word with
    | nil =>
        exact nativeC60BVNoRelations_nil_faithful S F
    | cons side rest ih =>
        intro a b f g h
        change
          (nativeC60BDNoRelations_strictFunctor S F (side :: rest)).map f =
          (nativeC60BDNoRelations_strictFunctor S F (side :: rest)).map g at h
        have houter :
            (nativeC60BDNoRelations_strictFunctor S F [side]).map
                ((nativeC60BDNoRelations_strictFunctor S F rest).map f) =
              (nativeC60BDNoRelations_strictFunctor S F [side]).map
                ((nativeC60BDNoRelations_strictFunctor S F rest).map g) := by
          rw [nativeC60BFStrictFunctor_cons S F side rest] at h
          exact h
        have hinner :
            (nativeC60BDNoRelations_strictFunctor S F rest).map f =
              (nativeC60BDNoRelations_strictFunctor S F rest).map g := by
          cases side with
          | false => exact hf _ _ houter
          | true => exact ht _ _ houter
        exact ih f g hinner

/-- The TWO singleton gates are equivalently the complete absence
of collapsed strict bridge replacement classes in the corresponding
typed AQ images. No actual collapse is assumed. -/
theorem nativeC60BVNoRelations_all_faithful_iff_no_letter_collapse
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L) :
    (∀ word : List Bool,
      NativeC60BUContextHomFaithful S F
        (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
        word (nativeC60BDNoRelations_context S F word)) ↔
      ¬ NativeC60BVBridgeCollapse S F
          (nativeC60AZNoRelations (nativeC60BCClosedSignature S F)) [false] ∧
        ¬ NativeC60BVBridgeCollapse S F
          (nativeC60AZNoRelations (nativeC60BCClosedSignature S F)) [true] := by
  rw [nativeC60BVNoRelations_all_faithful_iff_letters S F]
  constructor
  · rintro ⟨hf, ht⟩
    exact ⟨
      fun h => (nativeC60BVBridgeCollapse_iff_nonfaithful S F _
        [false] (nativeC60BDNoRelations_context S F [false])).mp h hf,
      fun h => (nativeC60BVBridgeCollapse_iff_nonfaithful S F _
        [true] (nativeC60BDNoRelations_context S F [true])).mp h ht⟩
  · rintro ⟨hfalse, htrue⟩
    constructor
    · by_contra h
      exact hfalse ((nativeC60BVBridgeCollapse_iff_nonfaithful S F _
        [false] (nativeC60BDNoRelations_context S F [false])).mpr h)
    · by_contra h
      exact htrue ((nativeC60BVBridgeCollapse_iff_nonfaithful S F _
        [true] (nativeC60BDNoRelations_context S F [true])).mpr h)

/-- If a fixed AQ context is faithful on real strict Hom sets, then
equality of the TWO-INPUT strict bridge gluing is preserved AND
REFLECTED by transport, for EVERY independently supplied typed bridge. -/
theorem nativeC60BVStrictGluing_eq_iff_frame
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (R : NativeC60AZParallelRelation (nativeC60BCClosedSignature S F))
    (word : List Bool) (stable : NativeC60BDContextCongruence S F R word)
    (faithful : NativeC60BUContextHomFaithful S F R word stable)
    (q r : NativeC60BGRawArrowBundle S F)
    (k k' : NativeC60AXStep (nativeC60BCClosedSignature S F)
      q.1.1 r.1.1) :
    nativeC60BTStrictGluing (nativeC60BCClosedSignature S F) R q r k =
        nativeC60BTStrictGluing (nativeC60BCClosedSignature S F) R q r k' ↔
      nativeC60BTStrictGluing (nativeC60BCClosedSignature S F) R
          (nativeC60BGRawContext S F word q)
          (nativeC60BGRawContext S F word r)
          (nativeC60BCMapClosedStep S F word k) =
        nativeC60BTStrictGluing (nativeC60BCClosedSignature S F) R
          (nativeC60BGRawContext S F word q)
          (nativeC60BGRawContext S F word r)
          (nativeC60BCMapClosedStep S F word k') := by
  constructor
  · intro h
    exact nativeC60BUGluing_choice_transport S F R word stable q r k k' h
  · intro h
    apply (nativeC60BTStrictGluing_eq_iff_replaceable
      (nativeC60BCClosedSignature S F) R q r k k').mpr
    apply nativeC60BUBridge_replaceable_reflect S F R word stable faithful
      k k'
    exact (nativeC60BTStrictGluing_eq_iff_replaceable
      (nativeC60BCClosedSignature S F) R
      (nativeC60BGRawContext S F word q)
      (nativeC60BGRawContext S F word r)
      (nativeC60BCMapClosedStep S F word k)
      (nativeC60BCMapClosedStep S F word k')).mp h

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

/-- For the real 14D C60 left/right singleton contexts, ALL-WORD
strict Hom faithfulness is precisely a TWO-GATE problem.
This does not assert either gate's validity. -/
theorem nativeK5BVPhysical_all_faithful_iff_two_AQ
    (W : NativeK5StructuralThirteenCell p U V) :
    (∀ word : List Bool,
      NativeC60BUContextHomFaithful
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
        (nativeC60AZNoRelations (nativeK5BCSignature W))
        word
        (nativeC60BDNoRelations_context
          (nativeK5AXKuuSignature W) (nativeK5BCFrame W) word)) ↔
      NativeC60BUContextHomFaithful
          (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
          (nativeC60AZNoRelations (nativeK5BCSignature W))
          [false]
          (nativeC60BDNoRelations_context
            (nativeK5AXKuuSignature W) (nativeK5BCFrame W) [false]) ∧
        NativeC60BUContextHomFaithful
          (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
          (nativeC60AZNoRelations (nativeK5BCSignature W))
          [true]
          (nativeC60BDNoRelations_context
            (nativeK5AXKuuSignature W) (nativeK5BCFrame W) [true]) :=
  nativeC60BVNoRelations_all_faithful_iff_letters
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W)

end OriginalC60

#print axioms nativeC60BVGeneratorCode_injective
#print axioms nativeC60BVGeneratorCode_shift
#print axioms nativeC60BVShiftGen_injective
#print axioms nativeC60BVBridgeReflection_iff_faithful
#print axioms nativeC60BVBridgeCollapse_iff_nonfaithful
#print axioms nativeC60BVNoRelations_nil_faithful
#print axioms nativeC60BVNoRelations_all_faithful_iff_letters
#print axioms nativeC60BVNoRelations_all_faithful_iff_no_letter_collapse
#print axioms nativeC60BVStrictGluing_eq_iff_frame
#print axioms nativeK5BVPhysical_all_faithful_iff_two_AQ

end
end Kuu.F112.Physical
