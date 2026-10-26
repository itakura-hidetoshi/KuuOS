import Kuu.F112.PolygonNativeC60FreeBridgeHolonomyPrefixObstruction

/-!
# F112-P94D3BX — split free-prefix action and exact atomic bridge completeness

BW proved noncommutative FreeGroup-map injectivity for all finite
genuine AQ contexts. BX strengthens this by constructing an EXPLICIT
left inverse using suffix recovery from the generator's complete
context-prefixed provenance code. The induced free-group homomorphism
SPLITS every finite AQ prefix on ALL group words; no inverse is
inferred for physical 15D object maps.

For TWO actual parallel single-generator raw16D proofs, equality of
complete free group values is NECESSARY AND SUFFICIENT for equality
in the existing BC no-extra-relations strict Kuu quotient. Therefore
transport of such atomic bridges through any finite genuine AQ word
preserves and REFLECTS their strict replacement class, unconditionally,
including the separate true/false physical frames.

The remaining frontier for ARBITRARY vertical higher composites and
inverse terms is isolated precisely: completeness of this particular
FreeGroup-valued strict functor on every typed Hom is EQUIVALENT to
reflection of the selected strict replacement closure for ALL raw16D
bridges. By BA representative surjectivity, this is not just a
sufficient criterion. If that full completeness holds, then EVERY
finite AQ context is faithful on strict Hom and BT's two-input bridge
gluing is reflected. The full assumption itself is NOT asserted;
there is no false recovery of raw proof terms from observer values.

No new axioms, sorry, admit, Gray, total BB whiskering,
unconditional middle-four, or modification of 107 public roots.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u uD vD uE vE

/-- Forget one finite AQ prefix from every complete sixteen-dimensional
generator certificate. This is total even on words not beginning
with that prefix, and is NOT asserted to invert lower 15D objects. -/
def nativeC60BXCodeUnprefix {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (word : List Bool) :
    NativeC60BVGeneratorCode S → NativeC60BVGeneratorCode S :=
  fun code => (code.1.drop word.length, code.2)

/-- Every actual prefixed generator certificate can be recovered
exactly; independent source and target 15D evidence remain present. -/
theorem nativeC60BXCodeUnprefix_prefix
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (word : List Bool)
    (code : NativeC60BVGeneratorCode S) :
    nativeC60BXCodeUnprefix S word (nativeC60BWCodePrefix S word code) =
      code := by
  rcases code with ⟨inner, payload⟩
  change ((word ++ inner).drop word.length, payload) = (inner, payload)
  simp only [List.drop_left]

/-- The EXPLICIT free-group retraction, distinct from and stronger than
the injectivity established in BW. -/
def nativeC60BXFreeUnprefix {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (word : List Bool) :
    FreeGroup (NativeC60BVGeneratorCode S) →*
      FreeGroup (NativeC60BVGeneratorCode S) :=
  FreeGroup.map (nativeC60BXCodeUnprefix S word)

/-- Actual left inverse on ALL reduced AND unreduced
noncommutative free words, using FreeGroup.map composition. -/
theorem nativeC60BXFreeUnprefix_prefix
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (word : List Bool)
    (z : FreeGroup (NativeC60BVGeneratorCode S)) :
    nativeC60BXFreeUnprefix S word (nativeC60BWFreePrefix S word z) =
      z := by
  change (FreeGroup.map (nativeC60BXCodeUnprefix S word))
      ((FreeGroup.map (nativeC60BWCodePrefix S word)) z) = z
  rw [FreeGroup.map.comp]
  have h : nativeC60BXCodeUnprefix S word ∘ nativeC60BWCodePrefix S word =
      id := by
    funext code
    exact nativeC60BXCodeUnprefix_prefix S word code
  rw [h]
  exact FreeGroup.map.id z

/-- Recover the ORIGINAL complete higher free word AFTER finite
genuine AQ transport, without a faithfulness hypothesis on any
15D object or any strict Hom functor. -/
theorem nativeC60BXFreeHolonomy_recover
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (word : List Bool) {a b : L.Total}
    (c : NativeC60AXStep (nativeC60BCClosedSignature S F) a b) :
    nativeC60BXFreeUnprefix S word
        (nativeC60BWFreeHolonomy S F
          (nativeC60BCMapClosedStep S F word c)) =
      nativeC60BWFreeHolonomy S F c := by
  rw [nativeC60BWFreeHolonomy_frame]
  exact nativeC60BXFreeUnprefix_prefix S word _

/-- Atomic higher bridges have COMPLETE free-word discrimination
on the ORIGINAL strict Kuu replacement classes. This includes
their full original 15D endpoints and independent higher generator. -/
theorem nativeC60BXAtomicFreeComplete
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {a b : L.Total}
    (g h : (nativeC60BCClosedSignature S F).Gen a b) :
    nativeC60BWFreeHolonomy S F (.atom g) =
        nativeC60BWFreeHolonomy S F (.atom h) ↔
      NativeC60BUBridgeReplaceable S F
        (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
        (.atom g) (.atom h) := by
  constructor
  · intro heq
    change FreeGroup.of (nativeC60BVGeneratorCode S F g) =
        FreeGroup.of (nativeC60BVGeneratorCode S F h) at heq
    have hg : g = h :=
      nativeC60BVGeneratorCode_injective S F (FreeGroup.of_injective heq)
    subst h
    exact (nativeC60AZStrictStep_exact
      (nativeC60BCClosedSignature S F)
      (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
      (.atom g) (.atom g)).mp rfl
  · intro hrel
    exact nativeC60BWFreeHolonomy_eq_of_replaceable S F (.atom g) (.atom h) hrel

/-- Every finite AQ context reflects equality of two actual
positive ATOMIC higher-generator strict arrows, not merely their
noncommutative group-valued measurements. -/
theorem nativeC60BXAtomicContext_replaceable_iff
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (word : List Bool) {a b : L.Total}
    (g h : (nativeC60BCClosedSignature S F).Gen a b) :
    NativeC60BUBridgeReplaceable S F
        (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
        (nativeC60BCMapClosedStep S F word (.atom g))
        (nativeC60BCMapClosedStep S F word (.atom h)) ↔
      g = h := by
  constructor
  · intro hrel
    have heq := nativeC60BWFreeHolonomy_reflects_contextual_replaceable
      S F word (.atom g) (.atom h) hrel
    change FreeGroup.of (nativeC60BVGeneratorCode S F g) =
        FreeGroup.of (nativeC60BVGeneratorCode S F h) at heq
    exact nativeC60BVGeneratorCode_injective S F
      (FreeGroup.of_injective heq)
  · intro heq
    subst h
    apply (nativeC60AZStrictStep_exact
      (nativeC60BCClosedSignature S F)
      (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
      (nativeC60BCMapClosedStep S F word (.atom g))
      (nativeC60BCMapClosedStep S F word (.atom g))).mp
    rfl

/-- The atomic strict morphism equality itself (not just the raw
replacement predicate) is equivalent to equality of genuine higher
generators for every finite AQ context. -/
theorem nativeC60BXAtomicContext_strict_eq_iff
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (word : List Bool) {a b : L.Total}
    (g h : (nativeC60BCClosedSignature S F).Gen a b) :
    nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
        (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
        (nativeC60BCMapClosedStep S F word (.atom g)) =
      nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
        (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
        (nativeC60BCMapClosedStep S F word (.atom h)) ↔
      g = h :=
  (nativeC60AZStrictStep_exact
      (nativeC60BCClosedSignature S F)
      (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
      (nativeC60BCMapClosedStep S F word (.atom g))
      (nativeC60BCMapClosedStep S F word (.atom h))).trans
    (nativeC60BXAtomicContext_replaceable_iff S F word g h)

/-- EXACT remaining obstruction: the particular complete free word
would have to reflect the selected strict quotient for all typed raw
sixteen-dimensional proofs, not only atomic generators. -/
def NativeC60BXFullFreeComplete
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L) : Prop :=
  ∀ {a b : L.Total}
    (c d : NativeC60AXStep (nativeC60BCClosedSignature S F) a b),
    nativeC60BWFreeHolonomy S F c = nativeC60BWFreeHolonomy S F d →
      NativeC60BUBridgeReplaceable S F
        (nativeC60AZNoRelations (nativeC60BCClosedSignature S F)) c d

/-- Full categorical faithfulness of the existing strict quotient
free-holonomy FUNCTOR on every original exact-boundary Hom set. -/
def NativeC60BXStrictFreeFaithful
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L) : Prop :=
  ∀ {a b : L.Total}
    (f g : (nativeC60AZStrictProject (nativeC60BCClosedSignature S F)
        (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))).obj
          ⟨a⟩ ⟶
      (nativeC60AZStrictProject (nativeC60BCClosedSignature S F)
        (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))).obj
          ⟨b⟩),
    (nativeC60BWFreeStrictHolonomy S F).map f =
      (nativeC60BWFreeStrictHolonomy S F).map g → f = g

/-- Necessary-and-sufficient completeness criterion by actual BA
representability of all strict higher arrows. This statement does
NOT assume or assert that the criterion itself holds. -/
theorem nativeC60BXFullFreeComplete_iff_strict_faithful
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L) :
    NativeC60BXFullFreeComplete S F ↔
      NativeC60BXStrictFreeFaithful S F := by
  let T := nativeC60BCClosedSignature S F
  let R : NativeC60AZParallelRelation T := nativeC60AZNoRelations T
  constructor
  · intro complete a b f g hmap
    obtain ⟨c, rfl⟩ := nativeC60BAStep_surjective T R a b f
    obtain ⟨d, rfl⟩ := nativeC60BAStep_surjective T R a b g
    apply (nativeC60AZStrictStep_exact T R c d).mpr
    apply complete c d
    have hw : MulOpposite.op (nativeC60BWFreeHolonomy S F c) =
        MulOpposite.op (nativeC60BWFreeHolonomy S F d) := by
      simpa only [nativeC60BWFreeStrictHolonomy,
        nativeC60AZStrictHolonomy_arrow] using hmap
    exact congrArg MulOpposite.unop hw
  · intro faithful a b c d hw
    apply (nativeC60AZStrictStep_exact T R c d).mp
    apply faithful
    have hh : MulOpposite.op (nativeC60BWFreeHolonomy S F c) =
        MulOpposite.op (nativeC60BWFreeHolonomy S F d) :=
      congrArg MulOpposite.op hw
    simpa only [nativeC60BWFreeStrictHolonomy,
      nativeC60AZStrictHolonomy_arrow] using hh

/-- The complete missing obstruction as an EXISTENTIAL pair of
different strict bridges with identical full noncommutative words.
BW already proves that every genuine context-collapse witness must
be of this exact form, but its existence is not claimed here. -/
theorem nativeC60BXFullFreeComplete_iff_no_invisible_gap
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L) :
    NativeC60BXFullFreeComplete S F ↔
      ¬ ∃ (a b : L.Total)
        (c d : NativeC60AXStep (nativeC60BCClosedSignature S F) a b),
        ¬ NativeC60BUBridgeReplaceable S F
          (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
          c d ∧
        nativeC60BWFreeHolonomy S F c =
          nativeC60BWFreeHolonomy S F d := by
  classical
  constructor
  · intro complete ⟨a, b, c, d, hne, heq⟩
    exact hne (complete c d heq)
  · intro hgap a b c d heq
    by_contra hne
    exact hgap ⟨a, b, c, d, hne, heq⟩

/-- If and ONLY IF the still-open complete higher-word reflection
obligation is established, BW's unconditional free-word transport
proves faithful strict bridge transport for EVERY finite AQ context.
This implication does not insert the obligation as a new axiom. -/
theorem nativeC60BXComplete_implies_all_context_faithful
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (complete : NativeC60BXFullFreeComplete S F)
    (word : List Bool) :
    NativeC60BUContextHomFaithful S F
      (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
      word (nativeC60BDNoRelations_context S F word) := by
  apply (nativeC60BVBridgeReflection_iff_faithful S F
    (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
    word (nativeC60BDNoRelations_context S F word)).mp
  intro a b c d hcontext
  exact complete c d
    (nativeC60BWFreeHolonomy_reflects_contextual_replaceable
      S F word c d hcontext)

/-- Consequently the exact BT strict two-input bridge gluing would
be both preserved and reflected at EVERY finite original AQ word. -/
theorem nativeC60BXComplete_implies_gluing_reflection
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (complete : NativeC60BXFullFreeComplete S F)
    (word : List Bool) (q r : NativeC60BGRawArrowBundle S F)
    (k k' : NativeC60AXStep (nativeC60BCClosedSignature S F)
      q.1.1 r.1.1) :
    nativeC60BTStrictGluing (nativeC60BCClosedSignature S F)
        (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
        q r k =
      nativeC60BTStrictGluing (nativeC60BCClosedSignature S F)
        (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
        q r k' ↔
      nativeC60BTStrictGluing (nativeC60BCClosedSignature S F)
        (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
        (nativeC60BGRawContext S F word q)
        (nativeC60BGRawContext S F word r)
        (nativeC60BCMapClosedStep S F word k) =
      nativeC60BTStrictGluing (nativeC60BCClosedSignature S F)
        (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
        (nativeC60BGRawContext S F word q)
        (nativeC60BGRawContext S F word r)
        (nativeC60BCMapClosedStep S F word k') :=
  nativeC60BVStrictGluing_eq_iff_frame S F
    (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
    word (nativeC60BDNoRelations_context S F word)
    (nativeC60BXComplete_implies_all_context_faithful S F complete word)
    q r k k'

section PhysicalC60

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

/-- Actual C60 source-dependent finite AQ left/right contexts reflect
strict equality for arbitrary parallel raw16D ATOMIC generators.
No use of unproved composite-word completeness. -/
theorem nativeK5BXPhysical_atomic_context_strict_eq_iff
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool)
    {a b : (nativeK5AXBaseLayer W).Total}
    (g h : (nativeK5BCSignature W).Gen a b) :
    nativeC60AZStrictStep (nativeK5BCSignature W)
        (nativeC60AZNoRelations (nativeK5BCSignature W))
        (nativeK5BCClosedContextStep W word (.atom g)) =
      nativeC60AZStrictStep (nativeK5BCSignature W)
        (nativeC60AZNoRelations (nativeK5BCSignature W))
        (nativeK5BCClosedContextStep W word (.atom h)) ↔
      g = h :=
  nativeC60BXAtomicContext_strict_eq_iff
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W) word g h

end PhysicalC60

#print axioms nativeC60BXCodeUnprefix_prefix
#print axioms nativeC60BXFreeUnprefix_prefix
#print axioms nativeC60BXFreeHolonomy_recover
#print axioms nativeC60BXAtomicFreeComplete
#print axioms nativeC60BXAtomicContext_replaceable_iff
#print axioms nativeC60BXAtomicContext_strict_eq_iff
#print axioms nativeC60BXFullFreeComplete_iff_strict_faithful
#print axioms nativeC60BXFullFreeComplete_iff_no_invisible_gap
#print axioms nativeC60BXComplete_implies_all_context_faithful
#print axioms nativeC60BXComplete_implies_gluing_reflection
#print axioms nativeK5BXPhysical_atomic_context_strict_eq_iff

end
end Kuu.F112.Physical
