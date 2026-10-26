import Kuu.F112.PolygonNativeC60BridgeChoiceStrictEquivalence

/-!
# F112-P94D3BU — finite AQ transport and conditional reflection of bridges

BT identifies equality of the strict gluing of two genuinely independent
raw16D proofs with precisely the selected Kuu replacement class of their
typed bridge. BD already supplies the necessary-and-sufficient descent
criterion for each finite AQ word, rather than presupposing congruence
for arbitrarily chosen additional higher comparisons.

BU proves that BD's actual strict context functor commutes with BT's
TWO-INPUT bridge conjugation, on whole dependent strict Hom sets. Hence
any selected-replaceable bridge pair remains replaceable in a finite
context whenever that relation admits descent. This is unconditional
for the BC no-extra-relations presentation, including the actual two
false/true AQ generators.

For a fixed nonempty context, reverse reflection is conditional on
faithfulness of the actual strict Hom action; a collapsed bridge pair
with distinct old replacement classes is an explicit obstruction to
that faithfulness. For ALL finite contexts, reflection needs no
faithfulness assumption: the empty word is a member of the family.
The strict Hom condition is NOT raw16D term equality or an original
geometric 16-cell coherence proof. BH/BI Peiffer middle-four remains a
separate binary obligation.

No new axioms, sorry, admit, Gray, global BB whiskering, or public roots.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u uD vD uE vE

/-- Equality in precisely the SELECTED strict Kuu compositional
replacement closure, not equality of arbitrary scalar observations. -/
def NativeC60BUBridgeReplaceable {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (R : NativeC60AZParallelRelation (nativeC60BCClosedSignature S F))
    {a b : L.Total}
    (k k' : NativeC60AXStep (nativeC60BCClosedSignature S F) a b) :
    Prop :=
  Kuu.Replaceable
    (nativeC60AZStrictRelations (nativeC60BCClosedSignature S F) R)
    (nativeC60AZRawArrow (nativeC60BCClosedSignature S F) k)
    (nativeC60AZRawArrow (nativeC60BCClosedSignature S F) k')

/-- The genuine finite AQ strict functor intertwines BT's bridge
conjugation EQUIVALENCES. It acts on both actual proof inputs, not
only on the numerical or Peiffer shadow. -/
theorem nativeC60BUBridgeHomEquiv_frame {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (R : NativeC60AZParallelRelation (nativeC60BCClosedSignature S F))
    (word : List Bool) (stable : NativeC60BDContextCongruence S F R word)
    (q r : NativeC60BGRawArrowBundle S F)
    (k : (nativeC60AZStrictProject (nativeC60BCClosedSignature S F) R).obj
          ⟨q.1.1⟩ ⟶
        (nativeC60AZStrictProject (nativeC60BCClosedSignature S F) R).obj
          ⟨r.1.1⟩) :
    (nativeC60BDStrictContext S F R word stable).map
        ((nativeC60BTBridgeHomEquiv (nativeC60BCClosedSignature S F) R q r) k) =
      (nativeC60BTBridgeHomEquiv (nativeC60BCClosedSignature S F) R
        (nativeC60BGRawContext S F word q)
        (nativeC60BGRawContext S F word r))
        ((nativeC60BDStrictContext S F R word stable).map k) := by
  change (nativeC60BDStrictContext S F R word stable).map
      (nativeC60AZStrictStep (nativeC60BCClosedSignature S F) R (.symm q.2) ≫
        k ≫ nativeC60AZStrictStep (nativeC60BCClosedSignature S F) R r.2) =
    nativeC60AZStrictStep (nativeC60BCClosedSignature S F) R
        (.symm (nativeC60BGRawContext S F word q).2) ≫
      (nativeC60BDStrictContext S F R word stable).map k ≫
      nativeC60AZStrictStep (nativeC60BCClosedSignature S F) R
        (nativeC60BGRawContext S F word r).2
  simp only [Functor.map_comp, nativeC60BDStrictContext_step,
    nativeC60BCMapClosedStep_symm]
  rfl

/-- The commutative square at the raw-input boundary: context of
strict BS gluing equals strict gluing of all three contextual images. -/
theorem nativeC60BUGluing_frame {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (R : NativeC60AZParallelRelation (nativeC60BCClosedSignature S F))
    (word : List Bool) (stable : NativeC60BDContextCongruence S F R word)
    (q r : NativeC60BGRawArrowBundle S F)
    (bridge : NativeC60AXStep (nativeC60BCClosedSignature S F)
        q.1.1 r.1.1) :
    (nativeC60BDStrictContext S F R word stable).map
        (nativeC60BTStrictGluing (nativeC60BCClosedSignature S F) R
          q r bridge) =
      nativeC60BTStrictGluing (nativeC60BCClosedSignature S F) R
        (nativeC60BGRawContext S F word q)
        (nativeC60BGRawContext S F word r)
        (nativeC60BCMapClosedStep S F word bridge) := by
  unfold nativeC60BTStrictGluing
  rw [nativeC60BUBridgeHomEquiv_frame S F R word stable q r,
    nativeC60BDStrictContext_step S F R word stable]

/-- Every finite genuine AQ word preserves SELECTED bridge
replaceability, precisely under BD's selected relation congruence. -/
theorem nativeC60BUBridge_replaceable_transport
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (R : NativeC60AZParallelRelation (nativeC60BCClosedSignature S F))
    (word : List Bool) (stable : NativeC60BDContextCongruence S F R word)
    {a b : L.Total}
    (k k' : NativeC60AXStep (nativeC60BCClosedSignature S F) a b)
    (hk : NativeC60BUBridgeReplaceable S F R k k') :
    NativeC60BUBridgeReplaceable S F R
      (nativeC60BCMapClosedStep S F word k)
      (nativeC60BCMapClosedStep S F word k') := by
  apply (nativeC60AZStrictStep_exact (nativeC60BCClosedSignature S F) R
    (nativeC60BCMapClosedStep S F word k)
    (nativeC60BCMapClosedStep S F word k')).mp
  calc
    nativeC60AZStrictStep (nativeC60BCClosedSignature S F) R
        (nativeC60BCMapClosedStep S F word k) =
      (nativeC60BDStrictContext S F R word stable).map
        (nativeC60AZStrictStep (nativeC60BCClosedSignature S F) R k) :=
          (nativeC60BDStrictContext_step S F R word stable k).symm
    _ = (nativeC60BDStrictContext S F R word stable).map
          (nativeC60AZStrictStep (nativeC60BCClosedSignature S F) R k') :=
      congrArg (fun t => (nativeC60BDStrictContext S F R word stable).map t)
        ((nativeC60AZStrictStep_exact (nativeC60BCClosedSignature S F) R
          k k').mpr hk)
    _ = nativeC60AZStrictStep (nativeC60BCClosedSignature S F) R
          (nativeC60BCMapClosedStep S F word k') :=
      nativeC60BDStrictContext_step S F R word stable k'

/-- BT's EXACT bridge-choice relation continues to hold for the two
contextual outputs. In particular this does not silently identify
the original 16D syntax of the chosen bridges. -/
theorem nativeC60BUGluing_choice_transport
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (R : NativeC60AZParallelRelation (nativeC60BCClosedSignature S F))
    (word : List Bool) (stable : NativeC60BDContextCongruence S F R word)
    (q r : NativeC60BGRawArrowBundle S F)
    (k k' : NativeC60AXStep (nativeC60BCClosedSignature S F)
      q.1.1 r.1.1)
    (hk : nativeC60BTStrictGluing (nativeC60BCClosedSignature S F)
        R q r k =
      nativeC60BTStrictGluing (nativeC60BCClosedSignature S F)
        R q r k') :
    nativeC60BTStrictGluing (nativeC60BCClosedSignature S F) R
        (nativeC60BGRawContext S F word q)
        (nativeC60BGRawContext S F word r)
        (nativeC60BCMapClosedStep S F word k) =
      nativeC60BTStrictGluing (nativeC60BCClosedSignature S F) R
        (nativeC60BGRawContext S F word q)
        (nativeC60BGRawContext S F word r)
        (nativeC60BCMapClosedStep S F word k') := by
  calc
    _ = (nativeC60BDStrictContext S F R word stable).map
        (nativeC60BTStrictGluing (nativeC60BCClosedSignature S F)
          R q r k) :=
            (nativeC60BUGluing_frame S F R word stable q r k).symm
    _ = (nativeC60BDStrictContext S F R word stable).map
        (nativeC60BTStrictGluing (nativeC60BCClosedSignature S F)
          R q r k') :=
      congrArg (fun t => (nativeC60BDStrictContext S F R word stable).map t) hk
    _ = _ := nativeC60BUGluing_frame S F R word stable q r k'

/-- The canonical no-extra-relations strict Kuu quotient transports
bridge replacement with NO hypothesis, for every finite AQ word. -/
theorem nativeC60BUNoRelations_transport
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (word : List Bool) {a b : L.Total}
    (k k' : NativeC60AXStep (nativeC60BCClosedSignature S F) a b)
    (hk : NativeC60BUBridgeReplaceable S F
      (nativeC60AZNoRelations (nativeC60BCClosedSignature S F)) k k') :
    NativeC60BUBridgeReplaceable S F
      (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
      (nativeC60BCMapClosedStep S F word k)
      (nativeC60BCMapClosedStep S F word k') :=
  nativeC60BUBridge_replaceable_transport S F
    (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
    word (nativeC60BDNoRelations_context S F word) k k' hk

/-- Both TRUE physical AQ generators, false and true, are treated
separately; an observer-equality shortcut is never used. -/
theorem nativeC60BUNoRelations_two_letters
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {a b : L.Total}
    (k k' : NativeC60AXStep (nativeC60BCClosedSignature S F) a b)
    (hk : NativeC60BUBridgeReplaceable S F
      (nativeC60AZNoRelations (nativeC60BCClosedSignature S F)) k k') :
    NativeC60BUBridgeReplaceable S F
        (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
        (nativeC60BCMapClosedStep S F [false] k)
        (nativeC60BCMapClosedStep S F [false] k') ∧
      NativeC60BUBridgeReplaceable S F
        (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
        (nativeC60BCMapClosedStep S F [true] k)
        (nativeC60BCMapClosedStep S F [true] k') := by
  constructor
  · exact nativeC60BUNoRelations_transport S F [false] k k' hk
  · exact nativeC60BUNoRelations_transport S F [true] k k' hk

/-- For the collection of ALL finite words the reverse implication
comes from the EMPTY word, and needs no assumed individual-context
faithfulness. This is not reflection for a FIXED nonempty context. -/
theorem nativeC60BUBridge_all_words_iff
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (R : NativeC60AZParallelRelation (nativeC60BCClosedSignature S F))
    (stable : ∀ word, NativeC60BDContextCongruence S F R word)
    {a b : L.Total}
    (k k' : NativeC60AXStep (nativeC60BCClosedSignature S F) a b) :
    (∀ word : List Bool,
      NativeC60BUBridgeReplaceable S F R
        (nativeC60BCMapClosedStep S F word k)
        (nativeC60BCMapClosedStep S F word k')) ↔
      NativeC60BUBridgeReplaceable S F R k k' := by
  constructor
  · intro h
    simpa only [nativeC60BEMapClosedStep_nil] using (h [])
  · intro h word
    exact nativeC60BUBridge_replaceable_transport
      S F R word (stable word) k k' h

/-- Explicit hom-level injectivity of the SELECTED strict AQ functor.
This is an extra hypothesis for fixed-word reflection, not a
consequence of BT's independent conjugation equivalence. -/
def NativeC60BUContextHomFaithful
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (R : NativeC60AZParallelRelation (nativeC60BCClosedSignature S F))
    (word : List Bool) (stable : NativeC60BDContextCongruence S F R word) :
    Prop :=
  ∀ {a b : L.Total}
    (f g : (nativeC60AZStrictProject (nativeC60BCClosedSignature S F) R).obj
          ⟨a⟩ ⟶
        (nativeC60AZStrictProject (nativeC60BCClosedSignature S F) R).obj
          ⟨b⟩),
    (nativeC60BDStrictContext S F R word stable).map f =
      (nativeC60BDStrictContext S F R word stable).map g → f = g

/-- Faithfulness reflects EXACT selected replacement of two actual
original typed bridges from their context-transported strict images. -/
theorem nativeC60BUBridge_replaceable_reflect
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (R : NativeC60AZParallelRelation (nativeC60BCClosedSignature S F))
    (word : List Bool) (stable : NativeC60BDContextCongruence S F R word)
    (faithful : NativeC60BUContextHomFaithful S F R word stable)
    {a b : L.Total}
    (k k' : NativeC60AXStep (nativeC60BCClosedSignature S F) a b)
    (hk : NativeC60BUBridgeReplaceable S F R
      (nativeC60BCMapClosedStep S F word k)
      (nativeC60BCMapClosedStep S F word k')) :
    NativeC60BUBridgeReplaceable S F R k k' := by
  apply (nativeC60AZStrictStep_exact (nativeC60BCClosedSignature S F) R
    k k').mp
  apply faithful
  calc
    (nativeC60BDStrictContext S F R word stable).map
        (nativeC60AZStrictStep (nativeC60BCClosedSignature S F) R k) =
      nativeC60AZStrictStep (nativeC60BCClosedSignature S F) R
        (nativeC60BCMapClosedStep S F word k) :=
      nativeC60BDStrictContext_step S F R word stable k
    _ = nativeC60AZStrictStep (nativeC60BCClosedSignature S F) R
          (nativeC60BCMapClosedStep S F word k') :=
      (nativeC60AZStrictStep_exact (nativeC60BCClosedSignature S F) R
        (nativeC60BCMapClosedStep S F word k)
        (nativeC60BCMapClosedStep S F word k')).mpr hk
    _ = (nativeC60BDStrictContext S F R word stable).map
        (nativeC60AZStrictStep (nativeC60BCClosedSignature S F) R k') :=
      (nativeC60BDStrictContext_step S F R word stable k').symm

/-- Under selected descent and faithful strict Hom transport, each
fixed word preserves AND reflects precisely the bridge classes. -/
theorem nativeC60BUBridge_replaceable_iff
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (R : NativeC60AZParallelRelation (nativeC60BCClosedSignature S F))
    (word : List Bool) (stable : NativeC60BDContextCongruence S F R word)
    (faithful : NativeC60BUContextHomFaithful S F R word stable)
    {a b : L.Total}
    (k k' : NativeC60AXStep (nativeC60BCClosedSignature S F) a b) :
    NativeC60BUBridgeReplaceable S F R
        (nativeC60BCMapClosedStep S F word k)
        (nativeC60BCMapClosedStep S F word k') ↔
      NativeC60BUBridgeReplaceable S F R k k' :=
  ⟨nativeC60BUBridge_replaceable_reflect S F R word stable faithful k k',
    nativeC60BUBridge_replaceable_transport S F R word stable k k'⟩

/-- CONDITIONAL obstruction: any pair of distinct selected replacement
classes collapsed by one context explicitly disproves the relevant
strict Hom faithfulness. Such a pair is NOT asserted to exist here. -/
theorem nativeC60BUContext_nonfaithful_of_bridge_collapse
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (R : NativeC60AZParallelRelation (nativeC60BCClosedSignature S F))
    (word : List Bool) (stable : NativeC60BDContextCongruence S F R word)
    {a b : L.Total}
    (k k' : NativeC60AXStep (nativeC60BCClosedSignature S F) a b)
    (hne : ¬ NativeC60BUBridgeReplaceable S F R k k')
    (hcollapse : NativeC60BUBridgeReplaceable S F R
      (nativeC60BCMapClosedStep S F word k)
      (nativeC60BCMapClosedStep S F word k')) :
    ¬ NativeC60BUContextHomFaithful S F R word stable := by
  intro faithful
  exact hne (nativeC60BUBridge_replaceable_reflect
    S F R word stable faithful k k' hcollapse)

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

/-- Actual AU physical 15D naturality pair: the genuine AQ functor
commutes with the higher bridge gluing at EVERY finite context. -/
theorem nativeK5BUPhysicalNaturality_gluing_frame
    (W : NativeK5StructuralThirteenCell p U V) (word : List Bool)
    (bridge : NativeC60AXStep (nativeK5BCSignature W)
        (nativeK5BSNaturalityFirst W).1.1
        (nativeK5BSNaturalitySecond W).1.1) :
    (nativeK5BDPhysicalStrictContext W word).map
        (nativeC60BTStrictGluing (nativeK5BCSignature W)
          (nativeC60AZNoRelations (nativeK5BCSignature W))
          (nativeK5BSNaturalityFirst W) (nativeK5BSNaturalitySecond W)
          bridge) =
      nativeC60BTStrictGluing (nativeK5BCSignature W)
        (nativeC60AZNoRelations (nativeK5BCSignature W))
        (nativeC60BGRawContext
          (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
          word (nativeK5BSNaturalityFirst W))
        (nativeC60BGRawContext
          (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
          word (nativeK5BSNaturalitySecond W))
        (nativeC60BCMapClosedStep
          (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
          word bridge) :=
  nativeC60BUGluing_frame
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
    (nativeC60AZNoRelations (nativeK5BCSignature W))
    word (nativeC60BDNoRelations_context
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W) word)
    (nativeK5BSNaturalityFirst W) (nativeK5BSNaturalitySecond W)
    bridge

/-- The two separately named genuine AQ false/true physical
whiskerings preserve the replacement class of any two AU bridges. -/
theorem nativeK5BUPhysicalNaturality_two_letters
    (W : NativeK5StructuralThirteenCell p U V)
    (bridge bridge' : NativeC60AXStep (nativeK5BCSignature W)
        (nativeK5BSNaturalityFirst W).1.1
        (nativeK5BSNaturalitySecond W).1.1)
    (hk : NativeC60BUBridgeReplaceable
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
        (nativeC60AZNoRelations (nativeK5BCSignature W))
        bridge bridge') :
    NativeC60BUBridgeReplaceable
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
        (nativeC60AZNoRelations (nativeK5BCSignature W))
        (nativeC60BCMapClosedStep
          (nativeK5AXKuuSignature W) (nativeK5BCFrame W) [false] bridge)
        (nativeC60BCMapClosedStep
          (nativeK5AXKuuSignature W) (nativeK5BCFrame W) [false] bridge') ∧
      NativeC60BUBridgeReplaceable
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
        (nativeC60AZNoRelations (nativeK5BCSignature W))
        (nativeC60BCMapClosedStep
          (nativeK5AXKuuSignature W) (nativeK5BCFrame W) [true] bridge)
        (nativeC60BCMapClosedStep
          (nativeK5AXKuuSignature W) (nativeK5BCFrame W) [true] bridge') :=
  nativeC60BUNoRelations_two_letters
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
    bridge bridge' hk

end OriginalC60

#print axioms NativeC60BUBridgeReplaceable
#print axioms nativeC60BUBridgeHomEquiv_frame
#print axioms nativeC60BUGluing_frame
#print axioms nativeC60BUBridge_replaceable_transport
#print axioms nativeC60BUGluing_choice_transport
#print axioms nativeC60BUNoRelations_transport
#print axioms nativeC60BUNoRelations_two_letters
#print axioms nativeC60BUBridge_all_words_iff
#print axioms NativeC60BUContextHomFaithful
#print axioms nativeC60BUBridge_replaceable_reflect
#print axioms nativeC60BUBridge_replaceable_iff
#print axioms nativeC60BUContext_nonfaithful_of_bridge_collapse
#print axioms nativeK5BUPhysicalNaturality_gluing_frame
#print axioms nativeK5BUPhysicalNaturality_two_letters

end
end Kuu.F112.Physical
