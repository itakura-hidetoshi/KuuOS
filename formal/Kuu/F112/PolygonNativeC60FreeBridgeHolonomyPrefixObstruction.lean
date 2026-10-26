import Kuu.F112.PolygonNativeC60BridgeFaithfulnessFiniteGates
import Mathlib.GroupTheory.FreeGroup.Basic

/-!
# F112-P94D3BW — free noncommutative bridge holonomy survives finite AQ contexts

BV proves that true BC sixteen-dimensional higher generators preserve
their entire original dependent source/target and independent generator
under finite-prefix transport. BW extends this separation to a genuinely
NONCOMMUTATIVE FREE GROUP of all higher-generator provenance codes.

For every finite AQ word w the induced FreeGroup.map is injective.
The resulting free higher-holonomy evaluates BOTH signed inverse and
arbitrarily long composite raw sixteen-dimensional comparisons in their
correct order, and has EXACT finite-context covariance. This gives a
new unconditional, typed NO-COLLAPSE theorem:

    if two actual raw16D bridges have distinct free-word holonomies,
    then no finite AQ context can make them equal in BC's selected
    no-extra-relations strict Kuu replacement quotient.

Since BV's strict equivalence test ranges over ALL strict Hom arrows,
this free-group obstruction covers only the pairs whose fully ordered
generator-word holonomies are distinct. We do NOT infer strict Hom
faithfulness or a geometric 16-cell filler from the free-group test.
Equal free words need not imply selected replacement, because the
universal free-group readout is not proven faithful on typed Hom sets.

As an application, a conditional BG/BH/BI Peiffer replacement test
cannot be made true by context transport when the ORIGINAL candidate
two-variable RL/LR higher words have unequal free higher-holonomies.

No new axioms, sorry, admit, Gray, unauthorized horizontal operation,
or changes to the 107 public roots.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u uD vD uE vE

/-- The ACTUAL provenance code of a BC higher generator receives one
finite AQ prefix. The entire raw15D source/target and primitive AX
comparison code are retained, rather than just a Peiffer measurement. -/
def nativeC60BWCodePrefix {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (word : List Bool) :
    NativeC60BVGeneratorCode S → NativeC60BVGeneratorCode S :=
  fun code => (word ++ code.1, code.2)

/-- Syntactic prefix insertion preserves all provenance codes. -/
theorem nativeC60BWCodePrefix_injective {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (word : List Bool) :
    Function.Injective (nativeC60BWCodePrefix S word) := by
  intro a b h
  have hword : a.1 = b.1 :=
    (List.append_right_inj word).mp ((Prod.mk.inj h).1)
  exact Prod.ext hword ((Prod.mk.inj h).2)

/-- Noncommutative group extension of the ACTUAL finite AQ prefix map. -/
def nativeC60BWFreePrefix {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (word : List Bool) :
    FreeGroup (NativeC60BVGeneratorCode S) →*
      FreeGroup (NativeC60BVGeneratorCode S) :=
  FreeGroup.map (nativeC60BWCodePrefix S word)

/-- The stronger group-valued NO-COLLAPSE result, using mathlib's
free-group injectivity rather than just generator-code injectivity. -/
theorem nativeC60BWFreePrefix_injective {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (word : List Bool) :
    Function.Injective (nativeC60BWFreePrefix S word) :=
  FreeGroup.map_injective (nativeC60BWCodePrefix_injective S word)

/-- Every genuine BC generator is assigned its OWN signed
noncommutative letter, including the original higher proof identity. -/
def nativeC60BWFreeWeight {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L) :
    ∀ {x y : L.Total},
      (nativeC60BCClosedSignature S F).Gen x y →
        FreeGroup (NativeC60BVGeneratorCode S) :=
  fun {_ _} g => FreeGroup.of (nativeC60BVGeneratorCode S F g)

/-- A completely specified noncommutative holonomy of the ENTIRE
typed free higher comparison, respecting reversal and pasting order. -/
def nativeC60BWFreeHolonomy {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {a b : L.Total}
    (c : NativeC60AXStep (nativeC60BCClosedSignature S F) a b) :
    FreeGroup (NativeC60BVGeneratorCode S) :=
  nativeC60AZHolonomy (nativeC60BCClosedSignature S F)
    (nativeC60BWFreeWeight S F) c

/-- The COMPLETE free word of a contextual image is the injection
of the original COMPLETE free word. Proven for actual dependent raw16D
terms by induction on atom/refl/reverse/composite constructors. -/
theorem nativeC60BWFreeHolonomy_frame
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (word : List Bool)
    {a b : L.Total}
    (c : NativeC60AXStep (nativeC60BCClosedSignature S F) a b) :
    nativeC60BWFreeHolonomy S F
        (nativeC60BCMapClosedStep S F word c) =
      (nativeC60BWFreePrefix S word) (nativeC60BWFreeHolonomy S F c) := by
  induction c with
  | atom g =>
      change FreeGroup.of
          (nativeC60BVGeneratorCode S F
            (nativeC60BCShiftGen S F word g)) =
        (nativeC60BWFreePrefix S word)
          (FreeGroup.of (nativeC60BVGeneratorCode S F g))
      simp only [nativeC60BWFreePrefix, FreeGroup.map.of]
      exact congrArg FreeGroup.of
        (nativeC60BVGeneratorCode_shift S F word g)
  | refl x =>
      change (1 : FreeGroup (NativeC60BVGeneratorCode S)) =
        (nativeC60BWFreePrefix S word) 1
      simp
  | symm c ih =>
      change (nativeC60BWFreeHolonomy S F
          (nativeC60BCMapClosedStep S F word c))⁻¹ =
        (nativeC60BWFreePrefix S word)
          ((nativeC60BWFreeHolonomy S F c)⁻¹)
      rw [ih]
      exact ((nativeC60BWFreePrefix S word).map_inv _).symm
  | trans c d ih ik =>
      change nativeC60BWFreeHolonomy S F
          (nativeC60BCMapClosedStep S F word c) *
          nativeC60BWFreeHolonomy S F
            (nativeC60BCMapClosedStep S F word d) =
        (nativeC60BWFreePrefix S word)
          (nativeC60BWFreeHolonomy S F c *
            nativeC60BWFreeHolonomy S F d)
      rw [ih, ik]
      exact ((nativeC60BWFreePrefix S word).map_mul _ _).symm

/-- The free word remains EQUAL before context if it becomes equal
after context, WITHOUT assuming strict Hom faithfulness. -/
theorem nativeC60BWFreeHolonomy_frame_eq_iff
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (word : List Bool) {a b : L.Total}
    (c d : NativeC60AXStep (nativeC60BCClosedSignature S F) a b) :
    nativeC60BWFreeHolonomy S F
        (nativeC60BCMapClosedStep S F word c) =
      nativeC60BWFreeHolonomy S F
        (nativeC60BCMapClosedStep S F word d) ↔
      nativeC60BWFreeHolonomy S F c =
        nativeC60BWFreeHolonomy S F d := by
  rw [nativeC60BWFreeHolonomy_frame S F word c,
    nativeC60BWFreeHolonomy_frame S F word d]
  exact (nativeC60BWFreePrefix_injective S word).eq_iff

/-- With NO newly selected geometric16D comparison, all original
Kuu strict relations are ONLY units, composites and inverses.
Their free higher holonomy respects the quotient by actual proofs. -/
theorem nativeC60BWFreeWeight_noRelations_sound
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L) :
    NativeC60AZWeightsRespect (nativeC60BCClosedSignature S F)
      (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
      (nativeC60BWFreeWeight S F) := by
  intro a b c d h
  exact False.elim h

/-- The COMPLETE original Kuu strict category admits a genuine
free noncommutative-word functor, not a quotient DEFINED by the
observer's kernel. -/
def nativeC60BWFreeStrictHolonomy
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L) :
    NativeC60AZStrictSpace (nativeC60BCClosedSignature S F)
        (nativeC60AZNoRelations (nativeC60BCClosedSignature S F)) ⥤
      SingleObj (FreeGroup (NativeC60BVGeneratorCode S))ᵐᵒᵖ :=
  nativeC60AZStrictHolonomy (nativeC60BCClosedSignature S F)
    (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
    (nativeC60BWFreeWeight S F)
    (nativeC60BWFreeWeight_noRelations_sound S F)

/-- Strict replacement implies equality of the complete nonabelian
signed 16D words, not merely of Peiffer values or lower boundaries. -/
theorem nativeC60BWFreeHolonomy_eq_of_replaceable
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {a b : L.Total}
    (c d : NativeC60AXStep (nativeC60BCClosedSignature S F) a b)
    (h : NativeC60BUBridgeReplaceable S F
      (nativeC60AZNoRelations (nativeC60BCClosedSignature S F)) c d) :
    nativeC60BWFreeHolonomy S F c =
      nativeC60BWFreeHolonomy S F d := by
  have heq := (nativeC60AZStrictStep_exact
      (nativeC60BCClosedSignature S F)
      (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
      c d).mpr h
  have hf := congrArg
    (fun t : (nativeC60AZStrictProject
        (nativeC60BCClosedSignature S F)
        (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))).obj
          ⟨a⟩ ⟶
      (nativeC60AZStrictProject
        (nativeC60BCClosedSignature S F)
        (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))).obj
          ⟨b⟩ =>
      (nativeC60BWFreeStrictHolonomy S F).map t) heq
  simp only [nativeC60BWFreeStrictHolonomy,
    nativeC60AZStrictHolonomy_arrow] at hf
  exact congrArg MulOpposite.unop hf

/-- ANY fully typed strict bridge collapse after finite AQ transport
must already be invisible to the FULL noncommutative free-word
invariant. This is a much sharper necessary obstruction than a
collapsed numerical/Peiffer observable. -/
theorem nativeC60BWFreeHolonomy_reflects_contextual_replaceable
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (word : List Bool) {a b : L.Total}
    (c d : NativeC60AXStep (nativeC60BCClosedSignature S F) a b)
    (h : NativeC60BUBridgeReplaceable S F
      (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
      (nativeC60BCMapClosedStep S F word c)
      (nativeC60BCMapClosedStep S F word d)) :
    nativeC60BWFreeHolonomy S F c =
      nativeC60BWFreeHolonomy S F d := by
  apply (nativeC60BWFreeHolonomy_frame_eq_iff S F word c d).mp
  exact nativeC60BWFreeHolonomy_eq_of_replaceable S F _ _ h

/-- Unconditional finite-AQ NO-COLLAPSE for every pair of truly
distinct NONCOMMUTATIVE FULL 16D generator-word holonomies. -/
theorem nativeC60BWFreeHolonomy_no_collapse
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (word : List Bool) {a b : L.Total}
    (c d : NativeC60AXStep (nativeC60BCClosedSignature S F) a b)
    (hne : nativeC60BWFreeHolonomy S F c ≠
      nativeC60BWFreeHolonomy S F d) :
    ¬ NativeC60BUBridgeReplaceable S F
      (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
      (nativeC60BCMapClosedStep S F word c)
      (nativeC60BCMapClosedStep S F word d) :=
  fun h => hne (nativeC60BWFreeHolonomy_reflects_contextual_replaceable
    S F word c d h)

/-- A BV-style collapse witness can only involve two strictly
distinct higher bridge arrows with the SAME free noncommutative
word. No assertion that such a witness actually exists. -/
theorem nativeC60BWCollapse_forces_same_free_word
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (word : List Bool)
    (collapse : NativeC60BVBridgeCollapse S F
      (nativeC60AZNoRelations (nativeC60BCClosedSignature S F)) word) :
    ∃ (a b : L.Total)
      (c d : NativeC60AXStep (nativeC60BCClosedSignature S F) a b),
      ¬ NativeC60BUBridgeReplaceable S F
        (nativeC60AZNoRelations (nativeC60BCClosedSignature S F)) c d ∧
      nativeC60BWFreeHolonomy S F c =
        nativeC60BWFreeHolonomy S F d := by
  rcases collapse with ⟨a, b, c, d, hne, hcollapse⟩
  exact ⟨a, b, c, d, hne,
    nativeC60BWFreeHolonomy_reflects_contextual_replaceable
      S F word c d hcollapse⟩

/-- The new free higher-holonomy obstruction applies directly to the
actual typed BG/BI RL versus LR higher composite for ANY explicitly
selected candidate binary whiskering. The binary operation is NOT
manufactured or asserted to satisfy interchange. -/
theorem nativeC60BWPeiffer_free_holonomy_obstruction
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (H : NativeC60BBWhiskering (nativeC60BCClosedSignature S F))
    (word : List Bool)
    (q r : NativeC60BGRawArrowBundle S F)
    (hne : nativeC60BWFreeHolonomy S F
        (nativeC60BBHorizontalRL H q.2 r.2) ≠
      nativeC60BWFreeHolonomy S F
        (nativeC60BBHorizontalLR H q.2 r.2)) :
    ¬ NativeC60BUBridgeReplaceable S F
      (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
      (nativeC60BCMapClosedStep S F word
        (nativeC60BBHorizontalRL H q.2 r.2))
      (nativeC60BCMapClosedStep S F word
        (nativeC60BBHorizontalLR H q.2 r.2)) :=
  nativeC60BWFreeHolonomy_no_collapse S F word _ _ hne

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

/-- The physical true/false source-dependent AU bridge transports
every noncommutative word discrimination, individually and under ALL
finite original C60 AQ contexts. -/
theorem nativeK5BWPhysicalBridge_free_no_collapse
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool)
    {a b : (nativeK5AXBaseLayer W).Total}
    (c d : NativeC60AXStep (nativeK5BCSignature W) a b)
    (hne : nativeC60BWFreeHolonomy
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W) c ≠
      nativeC60BWFreeHolonomy
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W) d) :
    ¬ NativeC60BUBridgeReplaceable
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
      (nativeC60AZNoRelations (nativeK5BCSignature W))
      (nativeK5BCClosedContextStep W word c)
      (nativeK5BCClosedContextStep W word d) :=
  nativeC60BWFreeHolonomy_no_collapse
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W) word c d hne

end OriginalC60

#print axioms nativeC60BWCodePrefix_injective
#print axioms nativeC60BWFreePrefix_injective
#print axioms nativeC60BWFreeHolonomy_frame
#print axioms nativeC60BWFreeHolonomy_frame_eq_iff
#print axioms nativeC60BWFreeWeight_noRelations_sound
#print axioms nativeC60BWFreeStrictHolonomy
#print axioms nativeC60BWFreeHolonomy_eq_of_replaceable
#print axioms nativeC60BWFreeHolonomy_reflects_contextual_replaceable
#print axioms nativeC60BWFreeHolonomy_no_collapse
#print axioms nativeC60BWCollapse_forces_same_free_word
#print axioms nativeC60BWPeiffer_free_holonomy_obstruction
#print axioms nativeK5BWPhysicalBridge_free_no_collapse

end
end Kuu.F112.Physical
