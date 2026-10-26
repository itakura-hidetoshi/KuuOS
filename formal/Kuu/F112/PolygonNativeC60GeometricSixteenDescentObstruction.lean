import Kuu.F112.PolygonNativeC60AllRawStrictReflection

/-!
# F112-P94D3CE — geometric 16D relation descent and genuine AU obstruction

CD proves full faithfulness of the complete noncommutative free-group
receiver on ALL original proof-relevant raw 16D comparisons in the SELECTED
no-extra-relations strict Kuu presentation, under every finite AQ word.

CE studies a separately proposed family of extra GEOMETRIC 16-cell
coherence relations R, always indexed by exactly parallel original 15D
proof objects. The relations are INPUT DATA, not introduced axioms or
silently inferred from scalar/Peiffer equality.

The exact criterion is rigid:
* a candidate relation preserves full free 16D holonomy iff it already
  holds in the EXISTING selected strict Kuu quotient;
* equivalently, it holds under EVERY finite true AQ context;
* equivalently, the original full noncommutative free receiver factors
  through the additional declared geometric relation;
* a concrete inequality of two original free holonomies is an exact
  obstruction to each of these properties.

Finally the ACTUAL C60 AU naturality bridge, constructed using the
genuine original 15D source/target proofs and an OPTIONAL declared BC
16D generator, is witnessed to have NONIDENTITY full free holonomy
at every finite context. Its physical Peiffer endpoint equality does
not trivialize its 16D generator. This is not an original geometric
16-cell coherence construction, nor a nonparallel pseudo-filler.

No new axioms, sorry, admit, Gray, universal horizontal Peiffer,
global strict 3/n or infinity-hyperdescent. Public roots unchanged.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u uD vD uE vE

/-- A proposed genuinely parallel geometric-16D coherence relation is
compatible when it preserves the COMPLETE noncommutative raw16D word.
This condition retains actual proof-relevant 15D endpoints and is not a
relation on the quotient of Peiffer observations. -/
def NativeC60CEGeometricCompatible
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (R : NativeC60AZParallelRelation (nativeC60BCClosedSignature S F)) :
    Prop :=
  ∀ {a b : L.Total}
    (c d : NativeC60AXStep (nativeC60BCClosedSignature S F) a b),
      R c d →
        nativeC60BWFreeHolonomy S F c =
          nativeC60BWFreeHolonomy S F d

/-- R is compatible with the complete free word precisely when EVERY
extra geometric equation was ALREADY an equality in the chosen original
strict Kuu quotient. This is the no-new-collapse rigidity result from
CD's unconditional all-raw16D fullness. -/
theorem nativeC60CECompatible_iff_original_strict
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (R : NativeC60AZParallelRelation (nativeC60BCClosedSignature S F)) :
    NativeC60CEGeometricCompatible S F R ↔
      ∀ {a b : L.Total}
        (c d : NativeC60AXStep (nativeC60BCClosedSignature S F) a b),
        R c d →
          nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
              (nativeC60AZNoRelations (nativeC60BCClosedSignature S F)) c =
            nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
              (nativeC60AZNoRelations (nativeC60BCClosedSignature S F)) d := by
  constructor
  · intro hc a b c d hr
    exact (nativeC60AZStrictStep_exact
      (nativeC60BCClosedSignature S F)
      (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
      c d).mpr ((nativeC60CDFullFreeComplete S F) c d (hc c d hr))
  · intro hc a b c d hr
    exact nativeC60BWFreeHolonomy_eq_of_replaceable S F c d
      ((nativeC60AZStrictStep_exact
        (nativeC60BCClosedSignature S F)
        (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
        c d).mp (hc c d hr))

/-- The geometric relation agrees in EVERY finite original AQ context
iff it preserves the original full sixteen-dimensional noncommutative
holonomy. No faithfulness hypothesis is left unproved or hidden. -/
theorem nativeC60CECompatible_iff_all_frames
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (R : NativeC60AZParallelRelation (nativeC60BCClosedSignature S F)) :
    NativeC60CEGeometricCompatible S F R ↔
      ∀ (word : List Bool) {a b : L.Total}
        (c d : NativeC60AXStep (nativeC60BCClosedSignature S F) a b),
        R c d →
          nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
              (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
              (nativeC60BCMapClosedStep S F word c) =
            nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
              (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
              (nativeC60BCMapClosedStep S F word d) := by
  constructor
  · intro hc word a b c d hr
    exact (nativeC60CDAll_raw_free_eq_iff_strict S F word c d).mp
      (hc c d hr)
  · intro hc a b c d hr
    exact (nativeC60CDAll_raw_free_eq_iff_strict S F [] c d).mpr
      (hc [] c d hr)

/-- The full free receiver actually FACTORS through a geometric
comparison presentation exactly when that additional selected
relation preserves genuine raw16D holonomy. This uses the existing
Kuu strict quotient's universal observer/descent theorem. -/
theorem nativeC60CECompatible_iff_holonomy_factor
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (R : NativeC60AZParallelRelation (nativeC60BCClosedSignature S F)) :
    NativeC60CEGeometricCompatible S F R ↔
      ∃ G : NativeC60AZStrictSpace (nativeC60BCClosedSignature S F) R ⥤
          SingleObj (FreeGroup (NativeC60BVGeneratorCode S))ᵐᵒᵖ,
        nativeC60AZStrictProject (nativeC60BCClosedSignature S F) R ⋙ G =
          nativeC60AZRawHolonomy (nativeC60BCClosedSignature S F)
            (nativeC60BWFreeWeight S F) := by
  change NativeC60AZWeightsRespect
      (nativeC60BCClosedSignature S F) R
      (nativeC60BWFreeWeight S F) ↔ _
  exact (nativeC60AZStrictHolonomy_iff
    (nativeC60BCClosedSignature S F) R
    (nativeC60BWFreeWeight S F)).symm

/-- A SINGLE typed geometric relator identifying two genuinely
different complete sixteen-dimensional free words is a concrete
obstruction to descent. No hypothetical equality is postulated. -/
theorem nativeC60CEHolonomyMismatch_no_compatibility
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (R : NativeC60AZParallelRelation (nativeC60BCClosedSignature S F))
    {a b : L.Total}
    (c d : NativeC60AXStep (nativeC60BCClosedSignature S F) a b)
    (hr : R c d)
    (hne : nativeC60BWFreeHolonomy S F c ≠
      nativeC60BWFreeHolonomy S F d) :
    ¬ NativeC60CEGeometricCompatible S F R := by
  intro hc
  exact hne (hc c d hr)

/-- An incompatible geometric16D relator cannot become a strict equality
under ANY actual finite AQ context of the original presentation. -/
theorem nativeC60CEHolonomyMismatch_all_frames
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {a b : L.Total}
    (c d : NativeC60AXStep (nativeC60BCClosedSignature S F) a b)
    (hne : nativeC60BWFreeHolonomy S F c ≠
      nativeC60BWFreeHolonomy S F d) (word : List Bool) :
    nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
        (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
        (nativeC60BCMapClosedStep S F word c) ≠
      nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
        (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
        (nativeC60BCMapClosedStep S F word d) := by
  intro h
  exact hne ((nativeC60CDAll_raw_free_eq_iff_strict S F word c d).mpr h)

/-- Hence the proposed geometric quotient has NO receiver extending
the ORIGINAL complete free-holonomy functor on its raw comparison
syntax. This does not assert that an alternate, information-losing
quotient or receiver cannot exist. -/
theorem nativeC60CEHolonomyMismatch_no_factor
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (R : NativeC60AZParallelRelation (nativeC60BCClosedSignature S F))
    {a b : L.Total}
    (c d : NativeC60AXStep (nativeC60BCClosedSignature S F) a b)
    (hr : R c d)
    (hne : nativeC60BWFreeHolonomy S F c ≠
      nativeC60BWFreeHolonomy S F d) :
    ¬ ∃ G : NativeC60AZStrictSpace (nativeC60BCClosedSignature S F) R ⥤
        SingleObj (FreeGroup (NativeC60BVGeneratorCode S))ᵐᵒᵖ,
      nativeC60AZStrictProject (nativeC60BCClosedSignature S F) R ⋙ G =
        nativeC60AZRawHolonomy (nativeC60BCClosedSignature S F)
          (nativeC60BWFreeWeight S F) := by
  intro h
  exact nativeC60CEHolonomyMismatch_no_compatibility S F R c d hr hne
    ((nativeC60CECompatible_iff_holonomy_factor S F R).mpr h)

/-- An ACTUAL genuine primitive sixteen-dimensional BC generator
always carries a NONIDENTITY complete free group holonomy. This is
a mathematical consequence of Church–Rosser reduced-word uniqueness,
not a non-physical assumed 16D filler. -/
theorem nativeC60CEAtomicFree_ne_one
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {a b : L.Total}
    (g : (nativeC60BCClosedSignature S F).Gen a b) :
    nativeC60BWFreeHolonomy S F (.atom g) ≠
      (1 : FreeGroup (NativeC60BVGeneratorCode S)) := by
  change FreeGroup.mk [(nativeC60BVGeneratorCode S F g, true)] ≠
    FreeGroup.mk []
  intro h
  have hwords :
      ([(nativeC60BVGeneratorCode S F g, true)] :
        List (NativeC60BVGeneratorCode S × Bool)) = [] :=
    nativeC60BYReducedSignedWord_unique S _ _
      FreeGroup.IsReduced.singleton FreeGroup.IsReduced.nil h
  cases hwords

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

/-- The ACTUAL AU naturality 16D generator in the OPTIONAL
context-closed BC signature, retaining the two original distinct
15D proof-bearing endpoints, not a geometric filler created by fiat. -/
def nativeK5CEPhysicalAUGenerator (W : NativeK5StructuralThirteenCell p U V) :
    (nativeK5BCSignature W).Gen
      (nativeK5AXPack W
        (nativeK5AUNaturalityViaSource W (nativeK5AQExchange W [])))
      (nativeK5AXPack W
        (nativeK5AUNaturalityViaTarget W (nativeK5AQExchange W []))) :=
  nativeC60BCGen (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
    [] ⟨_, _, nativeK5AQExchange W [], rfl, rfl⟩

/-- The named ORIGINAL AU presentation comparison really is the
single atom represented by the complete physical BC generator. -/
theorem nativeK5CEPhysicalAU_as_atom (W : NativeK5StructuralThirteenCell p U V) :
    nativeK5BSNaturality_declared_bridge W =
      .atom (nativeK5CEPhysicalAUGenerator W) := by
  rfl

/-- Physical corrected AU naturality has equal NONCOMMUTATIVE
Peiffer endpoint observations, even though the original raw 15D
proof objects remain distinct. This equality does not imply any
triviality of the full sixteen-dimensional noncommutative word. -/
theorem nativeK5CEPhysicalAU_peiffer
    (W : NativeK5StructuralThirteenCell p U V) :
    nativeK5AXPeiffer W
        (nativeK5AXPack W
          (nativeK5AUNaturalityViaSource W (nativeK5AQExchange W []))) =
      nativeK5AXPeiffer W
        (nativeK5AXPack W
          (nativeK5AUNaturalityViaTarget W (nativeK5AQExchange W []))) :=
  nativeK5BCSignature_peiffer W (nativeK5CEPhysicalAUGenerator W)

/-- Concrete TRUE physical C60 AU comparison: two distinct original
15D witnesses AND a nontrivial free sixteen-dimensional generator.
No assertion that the raw AU geometry itself supplied that generator. -/
theorem nativeK5CEPhysicalAU_distinct_and_nontrivial
    (W : NativeK5StructuralThirteenCell p U V) :
    (nativeK5BSNaturalityFirst W).1.1 ≠
        (nativeK5BSNaturalitySecond W).1.1 ∧
      nativeC60BWFreeHolonomy (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W)
        (nativeK5BSNaturality_declared_bridge W) ≠
          (1 : FreeGroup
            (NativeC60BVGeneratorCode (nativeK5AXKuuSignature W))) := by
  constructor
  · exact nativeK5BSNaturality_full_sources_ne W
  · rw [nativeK5CEPhysicalAU_as_atom W]
    exact nativeC60CEAtomicFree_ne_one
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
      (nativeK5CEPhysicalAUGenerator W)

/-- Every ACTUAL finite physical AQ context still detects this
independent AU primitive in the complete free receiver. Equating its
free word with the identity would require abandoning that receiver,
not merely asserting equal original Peiffer endpoint values. -/
theorem nativeK5CEPhysicalAU_all_frames_nontrivial
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool) :
    nativeC60BWFreeHolonomy (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W)
        (nativeK5BCClosedContextStep W word
          (nativeK5BSNaturality_declared_bridge W)) ≠
        (1 : FreeGroup
          (NativeC60BVGeneratorCode (nativeK5AXKuuSignature W))) := by
  rw [nativeK5CEPhysicalAU_as_atom W]
  change nativeC60BWFreeHolonomy (nativeK5AXKuuSignature W)
      (nativeK5BCFrame W)
      (.atom (nativeC60BCShiftGen (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W) word (nativeK5CEPhysicalAUGenerator W))) ≠ _
  exact nativeC60CEAtomicFree_ne_one
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
    (nativeC60BCShiftGen (nativeK5AXKuuSignature W)
      (nativeK5BCFrame W) word (nativeK5CEPhysicalAUGenerator W))

end OriginalC60

#print axioms NativeC60CEGeometricCompatible
#print axioms nativeC60CECompatible_iff_original_strict
#print axioms nativeC60CECompatible_iff_all_frames
#print axioms nativeC60CECompatible_iff_holonomy_factor
#print axioms nativeC60CEHolonomyMismatch_no_compatibility
#print axioms nativeC60CEHolonomyMismatch_all_frames
#print axioms nativeC60CEHolonomyMismatch_no_factor
#print axioms nativeC60CEAtomicFree_ne_one
#print axioms nativeK5CEPhysicalAU_as_atom
#print axioms nativeK5CEPhysicalAU_peiffer
#print axioms nativeK5CEPhysicalAU_distinct_and_nontrivial
#print axioms nativeK5CEPhysicalAU_all_frames_nontrivial

end
end Kuu.F112.Physical
