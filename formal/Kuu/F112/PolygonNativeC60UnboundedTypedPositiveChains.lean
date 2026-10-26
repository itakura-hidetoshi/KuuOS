import Kuu.F112.PolygonNativeC60ReducedWordTwoStepReflection

/-!
# F112-P94D3BZ — arbitrary finite typed positive 16D vertical chains

BY proves strict equality reflection for two genuinely composable BC
higher generators and proves unbounded positive-word injectivity on
their full, noncommutative provenance codes.

BZ constructs an actual dependently typed CHAIN of ANY finite number
of independently supplied original BC 16D primitive comparisons.
The chain is indexed by its COMPLETE ordered list of intermediate
original 15D objects. It is then folded into the EXISTING
NativeC60AXStep syntax using real vertical composition and reflexivity.

The complete ordered higher-generator provenance code is faithful on
such proof-bearing chains with the SAME ORIGINAL 15D OBJECT SKELETON,
for arbitrary finite length, not just two steps. Consequently EVERY
finite true AQ context (including both singleton false/true generators)
reflects equality of these actual complete strict Kuu morphisms if
the original 15D intermediate-object skeleton is fixed.

The signed inverse of a positive chain is also covered using the
existing strict inverse laws; no raw syntax cancellation is introduced.

This theorem does NOT establish unrestricted strict Hom faithfulness
for arbitrary signed composites with different intermediate skeletons.
Its domain is a genuine finite typed positive-chain presentation,
not a graph incidence shortcut, Peiffer scalar or observer quotient.
No new axioms, sorry, admit, Gray, total BB binary whiskering,
original geometric 16-cell or change to the 107 public roots.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u uD vD uE vE

/-- A finite chain of INDEPENDENT positive true BC 16D generators.
The entire list is made of ACTUAL original 15D intermediate objects,
not scalar observations. Any finite number of edges is allowed. -/
inductive NativeC60BZPositiveChain {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L) :
    L.Total → List L.Total → Type u where
  | nil (a : L.Total) : NativeC60BZPositiveChain S F a []
  | cons {a b : L.Total} {tail : List L.Total}
      (g : (nativeC60BCClosedSignature S F).Gen a b)
      (rest : NativeC60BZPositiveChain S F b tail) :
      NativeC60BZPositiveChain S F a (b :: tail)

/-- The exact target of a fixed original 15D object skeleton. -/
def nativeC60BZChainEnd {L : NativeC60AXLayer.{u}} :
    (a : L.Total) → List L.Total → L.Total
  | a, [] => a
  | _, b :: rest => nativeC60BZChainEnd b rest

/-- The actual dependent higher raw16D step represented by an arbitrary
finite generator chain, using the preexisting proof-relevant comparison
syntax without cancelling reversals or inserting fillers. -/
def nativeC60BZChainStep {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L) :
    {a : L.Total} → {tail : List L.Total} →
      NativeC60BZPositiveChain S F a tail →
        NativeC60AXStep (nativeC60BCClosedSignature S F)
          a (nativeC60BZChainEnd a tail)
  | _, _, .nil a => .refl a
  | _, _, .cons g rest => .trans (.atom g) (nativeC60BZChainStep S F rest)

/-- Complete ordered generator provenance codes from all independent
typed 16D steps of an arbitrary finite C60 bridge chain. -/
def nativeC60BZChainCodes {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L) :
    {a : L.Total} → {tail : List L.Total} →
      NativeC60BZPositiveChain S F a tail →
        List (NativeC60BVGeneratorCode S)
  | _, _, .nil _ => []
  | _, _, .cons g rest =>
      nativeC60BVGeneratorCode S F g :: nativeC60BZChainCodes S F rest

/-- The genuine raw16D vertical chain has exactly the fully ordered
positive FreeGroup word, including its whole original generator
provenance, for all finite lengths. -/
theorem nativeC60BZChain_holonomy
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {a : L.Total} {tail : List L.Total}
    (p : NativeC60BZPositiveChain S F a tail) :
    nativeC60BWFreeHolonomy S F (nativeC60BZChainStep S F p) =
      nativeC60BYPositiveFreeWord S (nativeC60BZChainCodes S F p) := by
  induction p with
  | nil a =>
      rfl
  | cons g rest ih =>
      change FreeGroup.mk [(nativeC60BVGeneratorCode S F g, true)] *
          nativeC60BWFreeHolonomy S F (nativeC60BZChainStep S F rest) =
        FreeGroup.mk
          ((nativeC60BVGeneratorCode S F g, true) ::
            (nativeC60BZChainCodes S F rest).map (fun code => (code, true)))
      rw [ih]
      simp only [nativeC60BYPositiveFreeWord,
        nativeC60BYPositiveSigned, FreeGroup.mul_mk,
        List.singleton_append]

/-- Two truly typed positive chains over the SAME explicit complete
15D intermediate-object skeleton are identical IF AND ONLY IF their
ordered complete BC-generator provenance code lists are identical.
This is not a fixed two-atom assertion: any finite number is allowed. -/
theorem nativeC60BZChainCodes_injective
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (a : L.Total) (tail : List L.Total) :
    Function.Injective (fun p : NativeC60BZPositiveChain S F a tail =>
      nativeC60BZChainCodes S F p) := by
  intro p q h
  induction p with
  | nil a =>
      cases q
      rfl
  | cons g rest ih =>
      cases q with
      | cons g' rest' =>
          change nativeC60BVGeneratorCode S F g ::
              nativeC60BZChainCodes S F rest =
            nativeC60BVGeneratorCode S F g' ::
              nativeC60BZChainCodes S F rest' at h
          injection h with hhead htail
          have hg : g = g' :=
            nativeC60BVGeneratorCode_injective S F hhead
          cases hg
          have hrest : rest = rest' := ih htail
          cases hrest
          rfl

/-- COMPLETE positive-chain equality is equivalent to equality of the
true noncommutative full 16D free holonomy, for arbitrary finite length
with preserved original 15D intermediate-object skeleton. -/
theorem nativeC60BZChain_free_eq_iff
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {a : L.Total} {tail : List L.Total}
    (p q : NativeC60BZPositiveChain S F a tail) :
    nativeC60BWFreeHolonomy S F (nativeC60BZChainStep S F p) =
        nativeC60BWFreeHolonomy S F (nativeC60BZChainStep S F q) ↔
      p = q := by
  constructor
  · intro heq
    rw [nativeC60BZChain_holonomy S F p,
      nativeC60BZChain_holonomy S F q] at heq
    exact nativeC60BZChainCodes_injective S F a tail
      ((nativeC60BYPositiveFreeWord_injective S) heq)
  · rintro rfl
    rfl

/-- EXACT reflection of the strict Kuu equality of two genuine
unbounded finite positive 16D vertical chains under ANY ordered finite
physical AQ context word. No source/target/middle 15D object is
inferred merely from the scalar/Peiffer shadow. -/
theorem nativeC60BZChain_strict_frame_eq_iff
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (word : List Bool) {a : L.Total} {tail : List L.Total}
    (p q : NativeC60BZPositiveChain S F a tail) :
    nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
        (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
        (nativeC60BCMapClosedStep S F word
          (nativeC60BZChainStep S F p)) =
      nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
        (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
        (nativeC60BCMapClosedStep S F word
          (nativeC60BZChainStep S F q)) ↔
      p = q := by
  constructor
  · intro heq
    have hrel :=
      (nativeC60AZStrictStep_exact
        (nativeC60BCClosedSignature S F)
        (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
        (nativeC60BCMapClosedStep S F word (nativeC60BZChainStep S F p))
        (nativeC60BCMapClosedStep S F word (nativeC60BZChainStep S F q))).mp heq
    have hfree := nativeC60BWFreeHolonomy_reflects_contextual_replaceable
      S F word (nativeC60BZChainStep S F p)
        (nativeC60BZChainStep S F q) hrel
    exact (nativeC60BZChain_free_eq_iff S F p q).mp hfree
  · rintro rfl
    rfl

/-- Uniform exact strict equality reflection for the formal reversed
arbitrary positive 16D chain. This is a typed reverse of the COMPLETE
chain, not cancellation of freely generated raw proof syntax. -/
theorem nativeC60BZChain_inverse_strict_frame_eq_iff
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (word : List Bool) {a : L.Total} {tail : List L.Total}
    (p q : NativeC60BZPositiveChain S F a tail) :
    nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
        (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
        (nativeC60BCMapClosedStep S F word
          (.symm (nativeC60BZChainStep S F p))) =
      nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
        (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
        (nativeC60BCMapClosedStep S F word
          (.symm (nativeC60BZChainStep S F q))) ↔
      p = q := by
  constructor
  · intro heq
    have hrel := (nativeC60AZStrictStep_exact
        (nativeC60BCClosedSignature S F)
        (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
        (nativeC60BCMapClosedStep S F word
          (.symm (nativeC60BZChainStep S F p)))
        (nativeC60BCMapClosedStep S F word
          (.symm (nativeC60BZChainStep S F q)))).mp heq
    have hfree := nativeC60BWFreeHolonomy_reflects_contextual_replaceable
      S F word (.symm (nativeC60BZChainStep S F p))
        (.symm (nativeC60BZChainStep S F q)) hrel
    have hpositive :
        nativeC60BWFreeHolonomy S F (nativeC60BZChainStep S F p) =
          nativeC60BWFreeHolonomy S F (nativeC60BZChainStep S F q) := by
      apply inv_injective
      exact hfree
    exact (nativeC60BZChain_free_eq_iff S F p q).mp hpositive
  · rintro rfl
    rfl

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

/-- Actual physical C60 15D source/target and ALL intermediate proofs
are fixed as an arbitrary-length list; strict C60 finite-context
transport faithfully reflects the complete positive 16D chain. -/
theorem nativeK5BZPhysical_chain_strict_frame_eq_iff
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool) (a : (nativeK5AXBaseLayer W).Total)
    (tail : List (nativeK5AXBaseLayer W).Total)
    (p q : NativeC60BZPositiveChain
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W) a tail) :
    nativeC60AZStrictStep (nativeK5BCSignature W)
        (nativeC60AZNoRelations (nativeK5BCSignature W))
        (nativeK5BCClosedContextStep W word
          (nativeC60BZChainStep
            (nativeK5AXKuuSignature W) (nativeK5BCFrame W) p)) =
      nativeC60AZStrictStep (nativeK5BCSignature W)
        (nativeC60AZNoRelations (nativeK5BCSignature W))
        (nativeK5BCClosedContextStep W word
          (nativeC60BZChainStep
            (nativeK5AXKuuSignature W) (nativeK5BCFrame W) q)) ↔
      p = q :=
  nativeC60BZChain_strict_frame_eq_iff
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W) word p q

end OriginalC60

#print axioms nativeC60BZChain_holonomy
#print axioms nativeC60BZChainCodes_injective
#print axioms nativeC60BZChain_free_eq_iff
#print axioms nativeC60BZChain_strict_frame_eq_iff
#print axioms nativeC60BZChain_inverse_strict_frame_eq_iff
#print axioms nativeK5BZPhysical_chain_strict_frame_eq_iff

end
end Kuu.F112.Physical
