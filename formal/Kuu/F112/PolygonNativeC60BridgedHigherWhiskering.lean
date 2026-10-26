import Kuu.F112.PolygonNativeC60SharedRawPairDescentObstruction

/-!
# F112-P94D3BS — genuinely two-proof partial raw 16D gluing via typed bridges

BR identifies a lower 14D source-boundary matching condition and an
unconditional obstruction to a universal *literal* double-source
flattening. BS does not replace exact original 15D endpoints by their
14D images, observer charges, or quotient classes.

A typed higher bridge k : source(q) => source(r) permits a genuinely
two-proof raw16D comparison between the TARGETS of any complete
original-dependent raw16D bundles q,r:

    BS(q,k,r) := ((symm q);k);r

Both q and r occur as independent raw proof constructors. No new
geometric generator, groupoid law, or raw cancellation is postulated.

The bridge is also a COMPLETE existence criterion: a comparison of
the two targets gives a bridge back by q;(-);(symm r). We do NOT
assert these forward and backward constructions are inverse as
raw-term equalities; freely generated syntax lacks cancellation.

Both true/false actual AQ frame words transport the entire bridged
triple and its glued raw16D output, on exact dependent endpoints.
Selected strict Kuu equalities of bridge proofs suffice for equality
of the resulting strict output arrows; equality of Peiffer observers
alone is NOT used as a substitute.

The physical AU naturality pair supplies a sharp example:
* its two 15D sources have IDENTICAL original 14D lower boundaries,
  but are DIFFERENT free 15D objects;
* the structural-only AX signature has NO bridge between them;
* the explicitly declared, context-closed Kuu 16D signature has one,
  yielding a genuine typed (but presentation-relative) gluing.

This is a partial, bridge-dependent 16D construction, NOT a total BB
whiskering, unconditional BG/BH/BI interchange, or the still-missing
original geometric 16-cell coherence. No new axioms, sorry, admit,
Gray categories, or modification of the 107 public roots.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u uD vD uE vE

/-- A genuine TWO-input raw16D configuration with one typed bridge
between the EXACT original 15D sources. -/
structure NativeC60BSBridgedPair {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L) where
  first : NativeC60BGRawArrowBundle S F
  second : NativeC60BGRawArrowBundle S F
  bridge : NativeC60AXStep (nativeC60BCClosedSignature S F)
    first.1.1 second.1.1

/-- The physical two-input partial gluing is an actual raw16D term:
reverse q, use the independently supplied source bridge, then r.
Both input 16D proofs occur, and all 15D endpoints are typed. -/
def nativeC60BSGluedStep {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (z : NativeC60BSBridgedPair S F) :
    NativeC60AXStep (nativeC60BCClosedSignature S F)
      z.first.1.2 z.second.1.2 :=
  .trans (.trans (.symm z.first.2) z.bridge) z.second.2

/-- Carry the exact original 15D source/target of the new typed 16D
comparison in one sigma, without a scalar projection. -/
def nativeC60BSGluedBundle {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (z : NativeC60BSBridgedPair S F) : NativeC60BGRawArrowBundle S F :=
  ⟨(z.first.1.2, z.second.1.2), nativeC60BSGluedStep S F z⟩

/-- The glued output is lower-globular in the ORIGINAL layer because
its original 15D endpoint pair is connected by a typed raw16D step. -/
theorem nativeC60BSGlued_lower_boundary {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (z : NativeC60BSBridgedPair S F) :
    z.first.1.2.1 = z.second.1.2.1 :=
  (nativeC60BSGluedStep S F z).boundary

/-- The missing source bridge is an exact NECESSARY condition
whenever a typed target-to-target comparison already exists. -/
def nativeC60BSBridgeFromTargets {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (q r : NativeC60BGRawArrowBundle S F)
    (target : NativeC60AXStep (nativeC60BCClosedSignature S F)
      q.1.2 r.1.2) :
    NativeC60AXStep (nativeC60BCClosedSignature S F) q.1.1 r.1.1 :=
  .trans (.trans q.2 target) (.symm r.2)

/-- Exact bridge existence CRITERION between full original 15D
proof objects: raw source reachability iff raw target reachability.
This does NOT assert an inverse equality between free 16D terms. -/
theorem nativeC60BSBridge_iff_target_comparison
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (q r : NativeC60BGRawArrowBundle S F) :
    Nonempty (NativeC60AXStep (nativeC60BCClosedSignature S F)
        q.1.1 r.1.1) ↔
      Nonempty (NativeC60AXStep (nativeC60BCClosedSignature S F)
        q.1.2 r.1.2) := by
  constructor
  · rintro ⟨bridge⟩
    exact ⟨nativeC60BSGluedStep S F ⟨q, r, bridge⟩⟩
  · rintro ⟨target⟩
    exact ⟨nativeC60BSBridgeFromTargets S F q r target⟩

/-- An EXACT match of the full original 15D source witnesses gives
a raw bridge by reflexivity, hence a genuine two-proof raw16D target
comparison. Matching only the lower 14D pair is weaker. -/
def nativeC60BSSameSourceBridge {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (q r : NativeC60BGRawArrowBundle S F) (h : q.1.1 = r.1.1) :
    NativeC60AXStep (nativeC60BCClosedSignature S F) q.1.1 r.1.1 := by
  cases h
  exact .refl _

/-- A same-15D-source pair is a special case of BR's typed bridged
operation; the two 16D proofs remain separate in the input. -/
def nativeC60BSSameSourcePair {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (q r : NativeC60BGRawArrowBundle S F) (h : q.1.1 = r.1.1) :
    NativeC60BSBridgedPair S F :=
  ⟨q, r, nativeC60BSSameSourceBridge S F q r h⟩

/-- A bridge gives both original lower 14D boundaries parallel, as a
consequence of higher typing, not as a license to identify raw terms. -/
theorem nativeC60BSBridge_implies_source_boundary
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (z : NativeC60BSBridgedPair S F) :
    z.first.1.1.1 = z.second.1.1.1 :=
  z.bridge.boundary

/-- AQ words transport the ENTIRE proof-carrying bridge configuration,
not merely the Peiffer observations. -/
def nativeC60BSFrame {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (word : List Bool) (z : NativeC60BSBridgedPair S F) :
    NativeC60BSBridgedPair S F := by
  rcases z with ⟨⟨⟨a,b⟩,f⟩, ⟨⟨c,d⟩,g⟩, bridge⟩
  exact ⟨nativeC60BGRawContext S F word ⟨(a,b),f⟩,
    nativeC60BGRawContext S F word ⟨(c,d),g⟩,
    nativeC60BCMapClosedStep S F word bridge⟩

/-- TYPE-VALUED NATURALITY. Every physical finite AQ word acts on the
entire two-input glued raw16D comparison exactly: both singleton
generators and all their ordered composites are supported. -/
theorem nativeC60BSGlued_frame
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (word : List Bool) (z : NativeC60BSBridgedPair S F) :
    nativeC60BSGluedBundle S F (nativeC60BSFrame S F word z) =
      nativeC60BGRawContext S F word (nativeC60BSGluedBundle S F z) := by
  rcases z with ⟨⟨⟨a,b⟩,f⟩, ⟨⟨c,d⟩,g⟩, bridge⟩
  rfl

/-- The source and target boundaries of the glued raw16D term
remain genuine original lower objects under each AQ frame. -/
theorem nativeC60BSGlued_frame_boundary
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (word : List Bool) (z : NativeC60BSBridgedPair S F) :
    (nativeC60BSGluedBundle S F (nativeC60BSFrame S F word z)).1 =
      (nativeC60BGRawContext S F word (nativeC60BSGluedBundle S F z)).1 :=
  congrArg (fun q : NativeC60BGRawArrowBundle S F => q.1)
    (nativeC60BSGlued_frame S F word z)

/-- Strict Kuu realization respects the fully raw bridged action.
This is a CONDITIONAL partial operation, not an everywhere-defined
BB object whiskering. -/
theorem nativeC60BSGlued_strict_frame
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (word : List Bool) (z : NativeC60BSBridgedPair S F) :
    nativeC60BNStrictify S F
        (nativeC60BSGluedBundle S F (nativeC60BSFrame S F word z)) =
      nativeC60BEArrowContext S F word
        (nativeC60BNStrictify S F (nativeC60BSGluedBundle S F z)) := by
  rw [nativeC60BSGlued_frame S F word z]
  exact (nativeC60BNStrictify_context S F word _).symm

/-- A sufficient CONDITIONAL BH-style replacement criterion:
if two bridges have the same selected strict Kuu arrow, their glued
raw16D outputs have the same strict arrow too. No Peiffer observer
is used to identify unrelated raw proof terms. -/
theorem nativeC60BSBridge_strict_choice_independent
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (q r : NativeC60BGRawArrowBundle S F)
    (bridge bridge' : NativeC60AXStep (nativeC60BCClosedSignature S F)
      q.1.1 r.1.1)
    (h : nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
          (nativeC60AZNoRelations (nativeC60BCClosedSignature S F)) bridge =
        nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
          (nativeC60AZNoRelations (nativeC60BCClosedSignature S F)) bridge') :
    nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
        (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
        (nativeC60BSGluedStep S F ⟨q,r,bridge⟩) =
      nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
        (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
        (nativeC60BSGluedStep S F ⟨q,r,bridge'⟩) := by
  simp only [nativeC60BSGluedStep, nativeC60AZStrictStep_comp]
  rw [h]

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

/-- The two ACTUAL C60 AU-naturalities, separately regarded as
reflexive raw16D proofs over DIFFERENT original 15D proof objects. -/
def nativeK5BSNaturalityFirst
    (W : NativeK5StructuralThirteenCell p U V) :
    NativeC60BGRawArrowBundle
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W) :=
  let a := nativeK5AXPack W
    (nativeK5AUNaturalityViaSource W (nativeK5AQExchange W []))
  ⟨(a, a), .refl a⟩

def nativeK5BSNaturalitySecond
    (W : NativeK5StructuralThirteenCell p U V) :
    NativeC60BGRawArrowBundle
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W) :=
  let b := nativeK5AXPack W
    (nativeK5AUNaturalityViaTarget W (nativeK5AQExchange W []))
  ⟨(b, b), .refl b⟩

/-- Exact original 14D source/target boundaries agree for these TWO
different original 15D proof objects: BR's condition is satisfied. -/
theorem nativeK5BSNaturality_lower_boundary_match
    (W : NativeK5StructuralThirteenCell p U V) :
    (nativeK5BSNaturalityFirst W).1.1.1 =
      (nativeK5BSNaturalitySecond W).1.1.1 := rfl

/-- Their whole original 15D proofs are unequal in the FREE syntax,
so lower 14D boundary matching is not full-source matching. -/
theorem nativeK5BSNaturality_full_sources_ne
    (W : NativeK5StructuralThirteenCell p U V) :
    (nativeK5BSNaturalityFirst W).1.1 ≠
      (nativeK5BSNaturalitySecond W).1.1 := by
  change nativeK5AXPack W
      (nativeK5AUNaturalityViaSource W (nativeK5AQExchange W [])) ≠
    nativeK5AXPack W
      (nativeK5AUNaturalityViaTarget W (nativeK5AQExchange W []))
  exact nativeK5AYPackedNaturality_ne W

/-- Even though the ORIGINAL lower 14D boundaries agree, the
structural-only signature contains NO 16D bridge for these true
distinct original AU 15D witnesses. -/
theorem nativeK5BSNaturality_no_structural_bridge
    (W : NativeK5StructuralThirteenCell p U V) :
    ¬ Nonempty (NativeC60AXStep
      (nativeC60AXStructuralSignature (nativeK5AXBaseLayer W))
      (nativeK5BSNaturalityFirst W).1.1
      (nativeK5BSNaturalitySecond W).1.1) := by
  change ¬ Nonempty (NativeC60AXStep
    (nativeC60AXStructuralSignature (nativeK5AXBaseLayer W))
    (nativeK5AXPack W (nativeK5AUNaturalityViaSource W (nativeK5AQExchange W [])))
    (nativeK5AXPack W (nativeK5AUNaturalityViaTarget W (nativeK5AQExchange W []))))
  exact nativeK5AYNoStructuralNaturality W

/-- The OPTIONAL Kuu context-closed signature supplies the bridge
as the NAMED, already declared genuine typed 16D AU comparison;
it does not pretend that this comparison is original geometry. -/
def nativeK5BSNaturality_declared_bridge
    (W : NativeK5StructuralThirteenCell p U V) :
    NativeC60AXStep (nativeK5BCSignature W)
      (nativeK5BSNaturalityFirst W).1.1
      (nativeK5BSNaturalitySecond W).1.1 :=
  nativeK5BCContextualNaturality W [] (nativeK5AQExchange W [])

/-- Positive TRUE physical instance: both separate ORIGINAL
proof-carrying AU 15D objects are connected by a declared 16D
bridge and hence form a valid two-input typed higher gluing. -/
def nativeK5BSNaturality_bridged
    (W : NativeK5StructuralThirteenCell p U V) :
    NativeC60BSBridgedPair
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W) :=
  ⟨nativeK5BSNaturalityFirst W, nativeK5BSNaturalitySecond W,
    nativeK5BSNaturality_declared_bridge W⟩

/-- The glued output is a 16D witness of a GENUINE non-identical
original 15D pair (not merely a reflexive comparison of one proof). -/
theorem nativeK5BSNaturality_glued_endpoints_ne
    (W : NativeK5StructuralThirteenCell p U V) :
    (nativeC60BSGluedBundle
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
      (nativeK5BSNaturality_bridged W)).1.1 ≠
    (nativeC60BSGluedBundle
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
      (nativeK5BSNaturality_bridged W)).1.2 :=
  nativeK5BSNaturality_full_sources_ne W

/-- This NEW partial operation respects the ACTUAL noncommutative
physical Peiffer kernel on its exact original 15D endpoints. -/
theorem nativeK5BSNaturality_glued_peiffer
    (W : NativeK5StructuralThirteenCell p U V) :
    nativeK5AXPeiffer W (nativeC60BSGluedBundle
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
      (nativeK5BSNaturality_bridged W)).1.1 =
    nativeK5AXPeiffer W (nativeC60BSGluedBundle
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
      (nativeK5BSNaturality_bridged W)).1.2 :=
  (nativeC60BSGluedBundle (nativeK5AXKuuSignature W)
    (nativeK5BCFrame W) (nativeK5BSNaturality_bridged W)).2.observer_sound
      (nativeK5AXPeiffer W) (nativeK5BCSignature_peiffer W)

end OriginalC60

#print axioms NativeC60BSBridgedPair
#print axioms nativeC60BSGluedStep
#print axioms nativeC60BSGluedBundle
#print axioms nativeC60BSGlued_lower_boundary
#print axioms nativeC60BSBridgeFromTargets
#print axioms nativeC60BSBridge_iff_target_comparison
#print axioms nativeC60BSSameSourceBridge
#print axioms nativeC60BSSameSourcePair
#print axioms nativeC60BSBridge_implies_source_boundary
#print axioms nativeC60BSFrame
#print axioms nativeC60BSGlued_frame
#print axioms nativeC60BSGlued_frame_boundary
#print axioms nativeC60BSGlued_strict_frame
#print axioms nativeC60BSBridge_strict_choice_independent
#print axioms nativeK5BSNaturalityFirst
#print axioms nativeK5BSNaturalitySecond
#print axioms nativeK5BSNaturality_lower_boundary_match
#print axioms nativeK5BSNaturality_full_sources_ne
#print axioms nativeK5BSNaturality_no_structural_bridge
#print axioms nativeK5BSNaturality_declared_bridge
#print axioms nativeK5BSNaturality_bridged
#print axioms nativeK5BSNaturality_glued_endpoints_ne
#print axioms nativeK5BSNaturality_glued_peiffer

end
end Kuu.F112.Physical
