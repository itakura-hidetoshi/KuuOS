import Kuu.F112.PolygonF36F40ShapeFunctorC60
import KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137
import Kuu.F112.PolygonNativeF41ComparisonObstruction
import KUOS.DependentOriginationCoherentBiadjunctionProofRelevantAxisTracesV5_142
import KUOS.DependentOriginationCoherentBiadjunctionExchangeAxisPairEquivalenceV5_143
import KUOS.DependentOriginationCoherentBiadjunctionChosenRightMateCategoriesV5_116
import KUOS.DependentOriginationCoherentBiadjunctionCompressionKernelQuotientCategoryV5_125
import KUOS.DependentOriginationGrayC60MixedBoundaryThreeHomV5_195
import KUOS.DependentOriginationCoherentBiadjunctionOriginalF45DepthRotationInvariantsV5_152

/-!
# F112-E7Q5-F4-P4 — ACTUAL original F36 Chain.Path and F40 Grid.Blocks bridge

This OLD-SIDE-only validation module (under the existing canonical public library root, never imported by the Kuu independent foundation) imports the ACTUAL preserved theorem-carrying
F36 and F40 Lean source modules, as well as the P3 independent Kuu
theorems. It never enters the KuuOSStrict / Kuu.F112 import closure.

All the below Equiv domains are the true original historical Lean
types (not new "shape" copies), for every ordinary category.
Both Hom arrows and all intermediate objects, including exact empty
path subdivisions, are transported constructor-by-constructor.
The original F19/F28 semantic categories are not identified, and no
Gray/F55/F77 transport is postulated.
-/

namespace KUOS.F112ActualHistoricalF36F40BridgeP4
open CategoryTheory
open Kuu.F112.Physical
open KUOS.DependentOriginationCoherentBiadjunctionFiniteHorizontalExchangeV5_133.Chain
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
set_option autoImplicit false
-- Strict diagnostic authority applies to this new P4 theorem carrier even
-- while accepted historical prerequisites retain visible nonfatal lint warnings.
set_option warningAsError true
noncomputable section

universe u v uD vD
variable {C : Type u} [Category.{v} C]
variable {D : Type uD} [Category.{vD} D]

/-- The ACTUAL original F36 Chain.Path: no replacement or copied Type. -/
abbrev OldPath (x y : C) :=
  KUOS.DependentOriginationCoherentBiadjunctionFiniteHorizontalExchangeV5_133.Chain.Path x y

/-- The ACTUAL original F40 Grid.Blocks: its snoc stores old Paths. -/
abbrev OldBlocks (x y : C) :=
  KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid.Blocks x y

/-- Interpret the historical Path's genuine Hom sequence without
evaluating any of its ordered arrows. -/
def oldPathToNative : ∀ {x y : C}, OldPath x y → KuuNativePath x y
  | _, _, .nil x => .nil x
  | _, _, .snoc p f => .snoc (oldPathToNative p) f

/-- Construct a genuine original F36 Path from all native raw arrows. -/
def nativePathToOld : ∀ {x y : C}, KuuNativePath x y → OldPath x y
  | _, _, .nil x => .nil x
  | _, _, .snoc p f => .snoc (nativePathToOld p) f

theorem oldPathToNative_nativePathToOld
    {x y : C} (p : KuuNativePath x y) :
    oldPathToNative (nativePathToOld p) = p := by
  induction p with
  | nil =>
      simp only [nativePathToOld, oldPathToNative]
  | snoc p f ih =>
      simp only [nativePathToOld, oldPathToNative, ih]

theorem nativePathToOld_oldPathToNative
    {x y : C} (p : OldPath x y) :
    nativePathToOld (oldPathToNative p) = p := by
  induction p with
  | nil =>
      simp only [oldPathToNative, nativePathToOld]
  | snoc p f ih =>
      simp only [oldPathToNative, nativePathToOld, ih]

/-- The first genuine historical ↔ independent native Type equivalence. -/
def oldPathEquivNative {x y : C} :
    OldPath x y ≃ KuuNativePath x y where
  toFun := oldPathToNative
  invFun := nativePathToOld
  left_inv := nativePathToOld_oldPathToNative
  right_inv := oldPathToNative_nativePathToOld

/-- Compare the actual OLD Type with the P3 new constructor model,
through proved equivalences rather than calling them definitionally equal. -/
def oldPathEquivShape {x y : C} :
    OldPath x y ≃ KuuF36ShapePath x y :=
  oldPathEquivNative.trans (kuuF36ShapePathEquiv (C := C)).symm

theorem oldPathToNative_append {x y z : C}
    (p : OldPath x y) (q : OldPath y z) :
    oldPathToNative (p.append q) =
      (oldPathToNative p).append (oldPathToNative q) := by
  induction q with
  | nil =>
      simp only [Path.append, oldPathToNative, KuuNativePath.append]
  | snoc q f ih =>
      simp only [Path.append, oldPathToNative, KuuNativePath.append, ih]

theorem oldPathToNative_composite {x y : C} (p : OldPath x y) :
    (oldPathToNative p).composite = p.composite := by
  induction p with
  | nil =>
      simp only [oldPathToNative, Path.composite, KuuNativePath.composite]
  | snoc p f ih =>
      simp only [oldPathToNative, Path.composite, KuuNativePath.composite, ih]

/-- Read the entire TRUE original F40 Blocks structure including
independent empty paths and its actual intermediate category objects. -/
def oldBlocksToNative : ∀ {x y : C}, OldBlocks x y → KuuNativeBlocks x y
  | _, _, .empty x => .empty x
  | _, _, .snoc p q => .snoc (oldBlocksToNative p) (oldPathToNative q)

/-- Reconstruct a genuine original Grid.Blocks from native raw Blocks. -/
def nativeBlocksToOld : ∀ {x y : C}, KuuNativeBlocks x y → OldBlocks x y
  | _, _, .empty x => .empty x
  | _, _, .snoc p q => .snoc (nativeBlocksToOld p) (nativePathToOld q)

theorem oldBlocksToNative_nativeBlocksToOld
    {x y : C} (s : KuuNativeBlocks x y) :
    oldBlocksToNative (nativeBlocksToOld s) = s := by
  induction s with
  | empty =>
      simp only [nativeBlocksToOld, oldBlocksToNative]
  | snoc s q ih =>
      simp only [nativeBlocksToOld, oldBlocksToNative,
        oldPathToNative_nativePathToOld, ih]

theorem nativeBlocksToOld_oldBlocksToNative
    {x y : C} (s : OldBlocks x y) :
    nativeBlocksToOld (oldBlocksToNative s) = s := by
  induction s with
  | empty =>
      simp only [oldBlocksToNative, nativeBlocksToOld]
  | snoc s q ih =>
      simp only [oldBlocksToNative, nativeBlocksToOld,
        nativePathToOld_oldPathToNative, ih]

/-- Actual F40 historical Lean Type ↔ independent native Lean Type,
retaining EVERY path and independent block boundary. -/
def oldBlocksEquivNative {x y : C} :
    OldBlocks x y ≃ KuuNativeBlocks x y where
  toFun := oldBlocksToNative
  invFun := nativeBlocksToOld
  left_inv := nativeBlocksToOld_oldBlocksToNative
  right_inv := oldBlocksToNative_nativeBlocksToOld

def oldBlocksEquivShape {x y : C} :
    OldBlocks x y ≃ KuuF40ShapeBlocks x y :=
  oldBlocksEquivNative.trans (kuuF40ShapeBlocksEquiv (C := C)).symm

/-- Exact preservation of the flattened, original ordered F36 raw
Hom word. Only explicit flattening forgets the F40 separators. -/
theorem oldBlocksToNative_flatten {x y : C} (s : OldBlocks x y) :
    oldPathToNative s.flatten = (oldBlocksToNative s).flatten := by
  induction s with
  | empty =>
      simp only [Blocks.flatten, oldPathToNative,
        oldBlocksToNative, KuuNativeBlocks.flatten]
  | snoc s q ih =>
      simp only [Blocks.flatten, oldBlocksToNative,
        KuuNativeBlocks.flatten, oldPathToNative_append, ih]

theorem oldBlocksToNative_composite {x y : C} (s : OldBlocks x y) :
    (oldBlocksToNative s).composite = s.composite := by
  induction s with
  | empty =>
      simp only [oldBlocksToNative, Blocks.composite, KuuNativeBlocks.composite]
  | snoc s q ih =>
      simp only [oldBlocksToNative, Blocks.composite,
        KuuNativeBlocks.composite, oldPathToNative_composite, ih]

theorem oldBlocksToNative_append {x y z : C}
    (s : OldBlocks x y) (t : OldBlocks y z) :
    oldBlocksToNative (s.append t) =
      (oldBlocksToNative s).append (oldBlocksToNative t) := by
  induction t with
  | empty =>
      simp only [Blocks.append, oldBlocksToNative, KuuNativeBlocks.append]
  | snoc t q ih =>
      simp only [Blocks.append, oldBlocksToNative,
        KuuNativeBlocks.append, ih]

/-- Original F36 functor map transports the SAME actual categorical
Hom arrows as the independent Kuu path map, at arbitrary depths. -/
theorem oldPathToNative_map (F : C ⥤ D)
    {x y : C} (p : OldPath x y) :
    oldPathToNative
      (KUOS.DependentOriginationCoherentBiadjunctionFiniteModificationMatePathsV5_135.Finite.mapPath F p) =
    (oldPathToNative p).map F := by
  induction p with
  | nil =>
      simp only [
        KUOS.DependentOriginationCoherentBiadjunctionFiniteModificationMatePathsV5_135.Finite.mapPath,
        oldPathToNative, KuuNativePath.map]
  | snoc p f ih =>
      simp only [
        KUOS.DependentOriginationCoherentBiadjunctionFiniteModificationMatePathsV5_135.Finite.mapPath,
        oldPathToNative, KuuNativePath.map, ih]

/-- The two nested historical F40 and independent Kuu maps commute
strictly on the WHOLE segmented raw syntax. -/
theorem oldBlocksToNative_map (F : C ⥤ D)
    {x y : C} (s : OldBlocks x y) :
    oldBlocksToNative (mapBlocks F s) =
      (oldBlocksToNative s).map F := by
  induction s with
  | empty =>
      simp only [mapBlocks, oldBlocksToNative, KuuNativeBlocks.map]
  | snoc s q ih =>
      simp only [mapBlocks, oldBlocksToNative, KuuNativeBlocks.map,
        oldPathToNative_map, ih]

/-- An actual C60 original Site path, with a real intermediate edge. -/
def physicalOldTwoStep (p : Polygon) (i : PolygonBoundarySector p) :
    OldPath (Site.vertex (cyclicBoundaryDart p i.1.val)) (Site.face p) :=
  nativePathToOld (polygonSectorNativeTwoStep p i)

/-- The separate direct vertex-to-face original Site Hom is ONE step. -/
def physicalOldDiagonal (p : Polygon) (i : PolygonBoundarySector p) :
    OldPath (Site.vertex (cyclicBoundaryDart p i.1.val)) (Site.face p) :=
  nativePathToOld (polygonSectorNativeDiagonal p i)

theorem physicalOldTwoStep_ne_diagonal (p : Polygon)
    (i : PolygonBoundarySector p) :
    physicalOldTwoStep p i ≠ physicalOldDiagonal p i := by
  intro h
  apply polygonSectorTwoStep_ne_diagonal p i
  have hh := congrArg
    (fun s : OldPath (Site.vertex (cyclicBoundaryDart p i.1.val)) (Site.face p) =>
      oldPathToNative s) h
  simpa only [physicalOldTwoStep, physicalOldDiagonal,
    oldPathToNative_nativePathToOld] using hh

def physicalOldTwoBlocks (p : Polygon) (i : PolygonBoundarySector p) :
    OldBlocks (Site.vertex (cyclicBoundaryDart p i.1.val)) (Site.face p) :=
  nativeBlocksToOld (polygonSectorTwoBlocks p i)

def physicalOldOneBlock (p : Polygon) (i : PolygonBoundarySector p) :
    OldBlocks (Site.vertex (cyclicBoundaryDart p i.1.val)) (Site.face p) :=
  nativeBlocksToOld (polygonSectorOneBlock p i)

theorem physicalOldTwoBlocks_ne_one (p : Polygon)
    (i : PolygonBoundarySector p) :
    physicalOldTwoBlocks p i ≠ physicalOldOneBlock p i := by
  intro h
  apply polygonSectorTwoBlocks_ne_oneBlock p i
  have hh := congrArg
    (fun s : OldBlocks (Site.vertex (cyclicBoundaryDart p i.1.val)) (Site.face p) =>
      oldBlocksToNative s) h
  simpa only [physicalOldTwoBlocks, physicalOldOneBlock,
    oldBlocksToNative_nativeBlocksToOld] using hh

theorem physicalOldBlocks_composite_eq (p : Polygon)
    (i : PolygonBoundarySector p) :
    (physicalOldTwoBlocks p i).composite =
      (physicalOldOneBlock p i).composite := by
  change (nativeBlocksToOld (polygonSectorTwoBlocks p i)).composite =
    (nativeBlocksToOld (polygonSectorOneBlock p i)).composite
  rw [← oldBlocksToNative_composite, ← oldBlocksToNative_composite,
    oldBlocksToNative_nativeBlocksToOld, oldBlocksToNative_nativeBlocksToOld]
  exact polygonSectorBlocks_composite_eq p i

/-- The inverse historical F36 reconstruction is also natural for
actual category functors; this is an equality of whole raw paths. -/
theorem nativePathToOld_map (F : C ⥤ D)
    {x y : C} (p : KuuNativePath x y) :
    KUOS.DependentOriginationCoherentBiadjunctionFiniteModificationMatePathsV5_135.Finite.mapPath
        F (nativePathToOld p) =
      nativePathToOld (p.map F) := by
  apply (oldPathEquivNative (C := D)).injective
  change
    oldPathToNative
        (KUOS.DependentOriginationCoherentBiadjunctionFiniteModificationMatePathsV5_135.Finite.mapPath
          F (nativePathToOld p)) =
      oldPathToNative (nativePathToOld (p.map F))
  simp only [oldPathToNative_map, oldPathToNative_nativePathToOld]

/-- The inverse real historical F40 Blocks reconstruction is natural
too, preserving every subdivision and inner categorical Hom. -/
theorem nativeBlocksToOld_map (F : C ⥤ D)
    {x y : C} (s : KuuNativeBlocks x y) :
    mapBlocks F (nativeBlocksToOld s) =
      nativeBlocksToOld (s.map F) := by
  apply (oldBlocksEquivNative (C := D)).injective
  change oldBlocksToNative (mapBlocks F (nativeBlocksToOld s)) =
    oldBlocksToNative (nativeBlocksToOld (s.map F))
  simp only [oldBlocksToNative_map, oldBlocksToNative_nativeBlocksToOld]

#print axioms oldPathToNative_nativePathToOld
#print axioms nativePathToOld_oldPathToNative
#print axioms oldBlocksToNative_nativeBlocksToOld
#print axioms nativeBlocksToOld_oldBlocksToNative
#print axioms nativePathToOld_map
#print axioms nativeBlocksToOld_map
#print axioms oldPathEquivNative
#print axioms oldPathEquivShape
#print axioms oldPathToNative_append
#print axioms oldPathToNative_composite
#print axioms oldBlocksEquivNative
#print axioms oldBlocksEquivShape
#print axioms oldBlocksToNative_flatten
#print axioms oldBlocksToNative_composite
#print axioms oldBlocksToNative_append
#print axioms oldPathToNative_map
#print axioms oldBlocksToNative_map
#print axioms physicalOldTwoStep_ne_diagonal
#print axioms physicalOldTwoBlocks_ne_one
#print axioms physicalOldBlocks_composite_eq

/-!
## F112-E7Q5-F4-P5 — ACTUAL historical F42/F45 primitive evidence boundary

This old-side extension uses the proved genuine F36/F40 equivalences of P4,
the true old F42 Prop-valued OneStep, and the true old F45 Type-valued
AxisTrace. A source-preserving erasure is constructed from the independent
Type-valued KuuNativeOneStep/KuuNativeAxisTrace.

The erasure preserves *entire* old finite arrow paths and endpoints, not
merely their evaluated Hom morphisms. However, the old F42 primitive
proof is in Prop; two distinct native split/insertNil primitive proofs
with the EXACT same original C60 block boundaries become definitionally
equal original F45 one-step histories. Hence this exact erasure is NOT
injective, even though both the source and target F45 histories are Type.

This is a precise obstruction to a naive historical equivalence, not a
claim about an enriched history model or any F47 global descent.
-/

open KUOS.DependentOriginationCoherentBiadjunctionFiniteRefinementTracesV5_139.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

/-- This is the ACTUAL frozen historical F42 primitive Prop, rather
than a new mimic of its constructor signatures. -/
abbrev HistoricalOneStep {x y : C} (p q : OldBlocks x y) : Prop :=
  KUOS.DependentOriginationCoherentBiadjunctionFiniteRefinementTracesV5_139.Grid.OneStep p q

/-- This is the ACTUAL historical F45 dependent Type whose step
fields are historical F42 Prop proofs. -/
abbrev HistoricalAxisTrace {x y : C} (n : Nat)
    (p q : OldBlocks x y) :=
  KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid.AxisTrace n p q

/-- The genuine P4 inverse transports full concatenated paths,
including their exact intermediate Hom arrows, without evaluation. -/
theorem nativePathToOld_append {x y z : C}
    (p : KuuNativePath x y) (q : KuuNativePath y z) :
    nativePathToOld (p.append q) =
      (nativePathToOld p).append (nativePathToOld q) := by
  apply (oldPathEquivNative (C := C)).injective
  change oldPathToNative (nativePathToOld (p.append q)) =
    oldPathToNative ((nativePathToOld p).append (nativePathToOld q))
  simp only [oldPathToNative_nativePathToOld, oldPathToNative_append]

/-- The genuine inverse of original F40 block concatenation retains
all independent empty and nonempty segment boundaries. -/
theorem nativeBlocksToOld_append {x y z : C}
    (p : KuuNativeBlocks x y) (q : KuuNativeBlocks y z) :
    nativeBlocksToOld (p.append q) =
      (nativeBlocksToOld p).append (nativeBlocksToOld q) := by
  apply (oldBlocksEquivNative (C := C)).injective
  change oldBlocksToNative (nativeBlocksToOld (p.append q)) =
    oldBlocksToNative ((nativeBlocksToOld p).append (nativeBlocksToOld q))
  simp only [oldBlocksToNative_nativeBlocksToOld, oldBlocksToNative_append]

/-- Forgetting block boundaries AFTER actual reconstruction equals
reconstructing the whole ordered original F36 arrow word. -/
theorem nativeBlocksToOld_flatten {x y : C}
    (s : KuuNativeBlocks x y) :
    (nativeBlocksToOld s).flatten = nativePathToOld s.flatten := by
  apply (oldPathEquivNative (C := C)).injective
  change oldPathToNative ((nativeBlocksToOld s).flatten) =
    oldPathToNative (nativePathToOld s.flatten)
  simp only [oldBlocksToNative_flatten,
    oldBlocksToNative_nativeBlocksToOld,
    oldPathToNative_nativePathToOld]

/-- Dependent F40 constructors require an explicit source equality:
change cannot manufacture the equation of this indexed recursive map. -/
theorem nativeBlocksToOld_snoc {x y z : C}
    (p : KuuNativeBlocks x y) (q : KuuNativePath y z) :
    nativeBlocksToOld (KuuNativeBlocks.snoc p q) =
      Blocks.snoc (nativeBlocksToOld p) (nativePathToOld q) := by
  simp only [nativeBlocksToOld]

/-- The reverse constructor equation is also a proved equality, not
an assumption identifying old and new types definitionally. -/
theorem oldBlocksToNative_snoc {x y z : C}
    (p : OldBlocks x y) (q : OldPath y z) :
    oldBlocksToNative (Blocks.snoc p q) =
      KuuNativeBlocks.snoc (oldBlocksToNative p) (oldPathToNative q) := by
  simp only [oldBlocksToNative]

theorem nativePathToOld_nil (x : C) :
    nativePathToOld (KuuNativePath.nil x) = Path.nil x := by
  simp only [nativePathToOld]

theorem oldPathToNative_nil (x : C) :
    oldPathToNative (Path.nil x) = KuuNativePath.nil x := by
  simp only [oldPathToNative]

/-- The independent Type-valued primitive refinement is realized as
the SAME genuinely historical F42 Prop generator on original F40 Blocks.
Only the split case needs P4's proved full-path concatenation lemma. -/
def nativeOneStepToHistorical {x y : C}
    {p q : KuuNativeBlocks x y}
    (h : KuuNativeOneStep p q) :
    HistoricalOneStep (nativeBlocksToOld p) (nativeBlocksToOld q) := by
  induction h with
  | split p q r =>
      simpa only [nativeBlocksToOld_snoc, nativePathToOld_append] using
        (OneStep.split (nativeBlocksToOld p)
          (nativePathToOld q) (nativePathToOld r))
  | insertNil p =>
      simpa only [nativeBlocksToOld_snoc, nativePathToOld_nil] using
        (OneStep.insertNil (nativeBlocksToOld p))
  | whisker h t ih =>
      simpa only [nativeBlocksToOld_snoc] using
        (OneStep.whisker ih (nativePathToOld t))

/-- Stronger than original F42 composite equality: every primitive
erasure preserves the WHOLE original F36 ordered arrow path. -/
theorem nativeOneStepToHistorical_flatten_eq
    {x y : C} {p q : KuuNativeBlocks x y}
    (h : KuuNativeOneStep p q) :
    (nativeBlocksToOld p).flatten = (nativeBlocksToOld q).flatten := by
  apply (oldPathEquivNative (C := C)).injective
  change oldPathToNative ((nativeBlocksToOld p).flatten) =
    oldPathToNative ((nativeBlocksToOld q).flatten)
  simp only [oldBlocksToNative_flatten,
    oldBlocksToNative_nativeBlocksToOld, h.flatten_eq]

/-- Entire arbitrarily long Type-valued primitive histories descend
to the ACTUAL historical F45 dependent Type, at exact Nat depth and
with exactly reconstructed F40 source, target and intermediates. -/
def nativeAxisTraceToHistorical {x y : C}
    {n : Nat} {p q : KuuNativeBlocks x y}
    (h : KuuNativeAxisTrace n p q) :
    HistoricalAxisTrace n (nativeBlocksToOld p) (nativeBlocksToOld q) := by
  induction h with
  | refl p =>
      exact AxisTrace.refl (nativeBlocksToOld p)
  | snoc h step ih =>
      exact AxisTrace.snoc ih (nativeOneStepToHistorical step)

/-- The genuine historical F45 trace conserves actual F19/F28
categorical evaluation after primitive Type-to-Prop erasure. -/
theorem nativeAxisTraceToHistorical_composite_eq
    {x y : C} {n : Nat} {p q : KuuNativeBlocks x y}
    (h : KuuNativeAxisTrace n p q) :
    (nativeBlocksToOld p).composite =
      (nativeBlocksToOld q).composite :=
  Trace.composite_eq (AxisTrace.toTrace (nativeAxisTraceToHistorical h))

/-!
## F112-P5-B — exact primitive image and choice-lift of old F45 evidence

The converse to erasure does exist at the level of inhabited raw
evidence: every ACTUAL old F42 generator is realized by at least one
independent Type-valued primitive with exactly transported original
F40 indices. The proof eliminates the historical Prop into Prop only.

Classical.choice subsequently selects one witness in Type; this
selection is intentionally NOT claimed to invert every native raw
proof constructor. Exact-Nat-depth historical F45 histories are
also realized, retaining each old intermediate block boundary.
-/

/-- Every actual historical F42 primitive move has a genuine native
witness on the exactly inverse-translated original F40 Blocks.
The elimination of old Prop evidence is INTO Prop (Nonempty). -/
theorem historicalOneStep_nonempty_native
    {x y : C} {p q : OldBlocks x y}
    (h : HistoricalOneStep p q) :
    Nonempty (KuuNativeOneStep (oldBlocksToNative p) (oldBlocksToNative q)) := by
  induction h with
  | split p q r =>
      simpa only [oldBlocksToNative_snoc, oldPathToNative_append] using
        (Nonempty.intro (KuuNativeOneStep.split (oldBlocksToNative p)
          (oldPathToNative q) (oldPathToNative r)))
  | insertNil p =>
      simpa only [oldBlocksToNative_snoc, oldPathToNative_nil] using
        (Nonempty.intro (KuuNativeOneStep.insertNil (oldBlocksToNative p)))
  | whisker h t ih =>
      rcases ih with ⟨witness⟩
      simpa only [oldBlocksToNative_snoc] using
        (Nonempty.intro (KuuNativeOneStep.whisker witness
          (oldPathToNative t)))

/-- This is an exact existence characterization of original F42
primitive operations, not an equivalence of their proof objects. -/
theorem historicalOneStep_iff_nonempty_native
    {x y : C} {p q : OldBlocks x y} :
    HistoricalOneStep p q ↔
      Nonempty (KuuNativeOneStep (oldBlocksToNative p) (oldBlocksToNative q)) := by
  constructor
  · exact historicalOneStep_nonempty_native
  · rintro ⟨witness⟩
    have old := nativeOneStepToHistorical witness
    simpa only [nativeBlocksToOld_oldBlocksToNative] using old

/-- A chosen independent primitive witness always exists, but it is
NOT a canonical left inverse to proof-relevant native erasure. -/
noncomputable def historicalOneStep_chooseNative
    {x y : C} {p q : OldBlocks x y}
    (h : HistoricalOneStep p q) :
    KuuNativeOneStep (oldBlocksToNative p) (oldBlocksToNative q) :=
  Classical.choice (historicalOneStep_nonempty_native h)

/-- Every actual old F45 Type-valued history has an independent
raw Type-valued representative of EXACTLY the same Nat length,
with all intermediate old F40 block objects transported. -/
theorem historicalAxisTrace_nonempty_native
    {x y : C} {n : Nat} {p q : OldBlocks x y}
    (h : HistoricalAxisTrace n p q) :
    Nonempty (KuuNativeAxisTrace n (oldBlocksToNative p) (oldBlocksToNative q)) := by
  induction h with
  | refl p =>
      exact ⟨KuuNativeAxisTrace.refl (oldBlocksToNative p)⟩
  | snoc h step ih =>
      rcases ih with ⟨history⟩
      rcases historicalOneStep_nonempty_native step with ⟨primitive⟩
      exact ⟨KuuNativeAxisTrace.snoc history primitive⟩

/-- Choose one realization of the ORIGINAL F45 history. It keeps
exact depth and boundaries, but independent primitive identity is
not recovered after historical Prop erasure. -/
noncomputable def historicalAxisTrace_chooseNative
    {x y : C} {n : Nat} {p q : OldBlocks x y}
    (h : HistoricalAxisTrace n p q) :
    KuuNativeAxisTrace n (oldBlocksToNative p) (oldBlocksToNative q) :=
  Classical.choice (historicalAxisTrace_nonempty_native h)

/-- A stronger historical F45 conservation theorem: the ENTIRE
ordered original F36 path is unchanged by a genuine old F45
refinement history, not merely its final categorical composite.
The proof transports to independent raw Kuu witnesses and back. -/
theorem historicalAxisTrace_flatten_eq
    {x y : C} {n : Nat} {p q : OldBlocks x y}
    (h : HistoricalAxisTrace n p q) :
    p.flatten = q.flatten := by
  apply (oldPathEquivNative (C := C)).injective
  change oldPathToNative p.flatten = oldPathToNative q.flatten
  simpa only [oldBlocksToNative_flatten] using
    (historicalAxisTrace_chooseNative h).flatten_eq

/-- The source-level F45 invariant also holds on true C60 Site
vertex/face incidence paths for arbitrary genuine physical sectors. -/
theorem physicalC60HistoricalAxisTrace_flatten_eq
    (p : Polygon) (i : PolygonBoundarySector p)
    {n : Nat}
    {s t : OldBlocks (Site.vertex (cyclicBoundaryDart p i.1.val)) (Site.face p)}
    (h : HistoricalAxisTrace n s t) :
    s.flatten = t.flatten :=
  historicalAxisTrace_flatten_eq h

#print axioms historicalOneStep_nonempty_native
#print axioms historicalOneStep_iff_nonempty_native
#print axioms historicalOneStep_chooseNative
#print axioms historicalAxisTrace_nonempty_native
#print axioms historicalAxisTrace_chooseNative
#print axioms historicalAxisTrace_flatten_eq
#print axioms physicalC60HistoricalAxisTrace_flatten_eq

/-- The two distinct native primitive constructors on exactly the
same original F40 double-nil boundaries erase to ONE historical F45
Type history: the embedded F42 primitive evidence is Prop-valued. -/
theorem nativeDoubleNilHistoricalTrace_eq
    {x y : C} (p : KuuNativeBlocks x y) :
    nativeAxisTraceToHistorical (nativeF41DoubleNilSplitTrace p) =
      nativeAxisTraceToHistorical (nativeF41DoubleNilInsertTrace p) := by
  rfl

/-- Therefore the actual F42 primitive erasure cannot be faithful
on all independent source proof constructors, EVEN ON FIXED BOUNDARIES. -/
theorem actualF42PrimitiveErasure_not_injective
    {x y : C} (p : KuuNativeBlocks x y) :
    ¬ Function.Injective
        (fun h : KuuNativeOneStep
          (nativeF41DoubleNilSource p) (nativeF41DoubleNilTarget p) =>
            nativeOneStepToHistorical h) := by
  intro hi
  exact nativeF41DoubleNilSplit_ne_insert p
    (hi (Subsingleton.elim _ _))

/-- The original F45 history is Type-valued, but storing F42 Prop
steps does NOT recover the split-versus-insertNil primitive witness.
This is a concrete failure of injection, not just unequal block counts. -/
theorem actualF45HistoryErasure_not_injective
    {x y : C} (p : KuuNativeBlocks x y) :
    ¬ Function.Injective
        (fun h : KuuNativeAxisTrace 1
          (nativeF41DoubleNilSource p) (nativeF41DoubleNilTarget p) =>
            nativeAxisTraceToHistorical h) := by
  intro hi
  exact nativeF41DoubleNilSplitTrace_ne_insert p
    (hi (nativeDoubleNilHistoricalTrace_eq p))

/-- The obstruction is already present on a genuine C60 physical
vertex→edge→face sector; it is not an abstract surrogate site. -/
theorem physicalC60ActualF45Erasure_not_injective
    (p : Polygon) (i : PolygonBoundarySector p) :
    ¬ Function.Injective
        (fun h : KuuNativeAxisTrace 1
          (nativeF41DoubleNilSource (polygonSectorTwoBlocks p i))
          (nativeF41DoubleNilTarget (polygonSectorTwoBlocks p i)) =>
            nativeAxisTraceToHistorical h) :=
  actualF45HistoryErasure_not_injective (polygonSectorTwoBlocks p i)

#print axioms nativeBlocksToOld_snoc
#print axioms oldBlocksToNative_snoc
#print axioms nativePathToOld_nil
#print axioms oldPathToNative_nil
#print axioms nativePathToOld_append
#print axioms nativeBlocksToOld_append
#print axioms nativeBlocksToOld_flatten
#print axioms nativeOneStepToHistorical
#print axioms nativeOneStepToHistorical_flatten_eq
#print axioms nativeAxisTraceToHistorical
#print axioms nativeAxisTraceToHistorical_composite_eq
#print axioms nativeDoubleNilHistoricalTrace_eq
#print axioms actualF42PrimitiveErasure_not_injective
#print axioms actualF45HistoryErasure_not_injective
#print axioms physicalC60ActualF45Erasure_not_injective


/-!
## F112-P6 — actual F44 exchange quotient on independent Kuu two-axis histories

P4 constructs real F36/F40 typed constructor equivalences. P5 proved both
directions of existence for original F42 primitive steps and F45 histories,
while exposing the actual F42 Prop-vs-Type information loss.

This P6 uses the F46 theorem about the ACTUAL original F44 exchange
quotient, not a fresh freely chosen quotient or a Boolean surrogate.
The original historical F19 chosen-right-mate category and the F28
compression-kernel quotient remain distinct axes throughout.
-/

/-- Two genuinely Type-valued independent axes are mapped to an
ACTUAL original F44 generated interchange quotient class. All
original finite F40 block indices and primitive depth counts survive. -/
def nativeTwoAxisToActualExchange
    {a b : C} {x y : D} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (histories : KuuNativeAxisTrace n ma mb ×
      KuuNativeAxisTrace m pa pb) :
    ExchangeClass n m
      (nativeBlocksToOld ma) (nativeBlocksToOld mb)
      (nativeBlocksToOld pa) (nativeBlocksToOld pb) :=
  AxisTrace.pairToClass
    (nativeAxisTraceToHistorical histories.1,
      nativeAxisTraceToHistorical histories.2)

/-- The actual F44 class remembers precisely the TWO historical F45
histories produced by erasure, not just their composed Hom arrows. -/
theorem nativeTwoAxisToActualExchange_axisTraces
    {a b : C} {x y : D} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (histories : KuuNativeAxisTrace n ma mb ×
      KuuNativeAxisTrace m pa pb) :
    (nativeTwoAxisToActualExchange histories).axisTraces =
      (nativeAxisTraceToHistorical histories.1,
        nativeAxisTraceToHistorical histories.2) :=
  AxisTrace.pairToClass_axisTraces _

/-- The actual historical F44 exchange relation preserves both
ordered original F36 Hom paths, not only their categorical evaluations.
There is NO identification of the F19 and F28 categories. -/
theorem actualExchange_twoAxis_flatten_eq
    {a b : C} {x y : D} {n m : Nat}
    {ma mb : OldBlocks a b}
    {pa pb : OldBlocks x y}
    (c : ExchangeClass n m ma mb pa pb) :
    ma.flatten = mb.flatten ∧ pa.flatten = pb.flatten :=
  ⟨historicalAxisTrace_flatten_eq c.axisTraces.1,
    historicalAxisTrace_flatten_eq c.axisTraces.2⟩

/-- Every ACTUAL original F44 exchange class has independently
realizable original F19/F28 primitive histories, with exact depths
and exactly transported F40 intermediate objects on both axes. -/
theorem actualExchange_nativeTwoAxis_nonempty
    {a b : C} {x y : D} {n m : Nat}
    {ma mb : OldBlocks a b}
    {pa pb : OldBlocks x y}
    (c : ExchangeClass n m ma mb pa pb) :
    Nonempty (
      KuuNativeAxisTrace n (oldBlocksToNative ma) (oldBlocksToNative mb) ×
      KuuNativeAxisTrace m (oldBlocksToNative pa) (oldBlocksToNative pb)) :=
  ⟨(historicalAxisTrace_chooseNative c.axisTraces.1,
      historicalAxisTrace_chooseNative c.axisTraces.2)⟩

/-- F42 primitive proof irrelevance produces a real F44 NON-INJECTIVE
two-axis map, even when the second axis is entirely unchanged. -/
theorem nativeTwoAxisToActualExchange_not_injective_first
    {a b : C} {x y : D}
    (p : KuuNativeBlocks a b) (q : KuuNativeBlocks x y) :
    ¬ Function.Injective
      (fun histories :
        KuuNativeAxisTrace 1
          (nativeF41DoubleNilSource p) (nativeF41DoubleNilTarget p) ×
        KuuNativeAxisTrace 0 q q =>
        nativeTwoAxisToActualExchange histories) := by
  intro hinj
  have heq :
      nativeTwoAxisToActualExchange
          (nativeF41DoubleNilSplitTrace p, KuuNativeAxisTrace.refl q) =
        nativeTwoAxisToActualExchange
          (nativeF41DoubleNilInsertTrace p, KuuNativeAxisTrace.refl q) := by
    change
      AxisTrace.pairToClass
          (nativeAxisTraceToHistorical (nativeF41DoubleNilSplitTrace p),
            nativeAxisTraceToHistorical (KuuNativeAxisTrace.refl q)) =
        AxisTrace.pairToClass
          (nativeAxisTraceToHistorical (nativeF41DoubleNilInsertTrace p),
            nativeAxisTraceToHistorical (KuuNativeAxisTrace.refl q))
    rw [nativeDoubleNilHistoricalTrace_eq p]
  exact nativeF41DoubleNilSplitTrace_ne_insert p
    (congrArg Prod.fst (hinj heq))

/-- Symmetrically, the genuine F28 axis can lose a distinct primitive
Type witness while the original F19 axis is held fixed. -/
theorem nativeTwoAxisToActualExchange_not_injective_second
    {a b : C} {x y : D}
    (p : KuuNativeBlocks a b) (q : KuuNativeBlocks x y) :
    ¬ Function.Injective
      (fun histories :
        KuuNativeAxisTrace 0 p p ×
        KuuNativeAxisTrace 1
          (nativeF41DoubleNilSource q) (nativeF41DoubleNilTarget q) =>
        nativeTwoAxisToActualExchange histories) := by
  intro hinj
  have heq :
      nativeTwoAxisToActualExchange
          (KuuNativeAxisTrace.refl p, nativeF41DoubleNilSplitTrace q) =
        nativeTwoAxisToActualExchange
          (KuuNativeAxisTrace.refl p, nativeF41DoubleNilInsertTrace q) := by
    change
      AxisTrace.pairToClass
          (nativeAxisTraceToHistorical (KuuNativeAxisTrace.refl p),
            nativeAxisTraceToHistorical (nativeF41DoubleNilSplitTrace q)) =
        AxisTrace.pairToClass
          (nativeAxisTraceToHistorical (KuuNativeAxisTrace.refl p),
            nativeAxisTraceToHistorical (nativeF41DoubleNilInsertTrace q))
    rw [nativeDoubleNilHistoricalTrace_eq q]
  exact nativeF41DoubleNilSplitTrace_ne_insert q
    (congrArg Prod.snd (hinj heq))

namespace GenuineF19F28

open KUOS.DependentOriginationCoherentBiadjunctionChosenRightMateCategoriesV5_116.Generic
open KUOS.DependentOriginationCoherentBiadjunctionCompressionKernelQuotientCategoryV5_125.Generic

universe uB vB wB uE vE wE
variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {E : Type uE} [Bicategory.{wE, vE} E]

/-- This is the ACTUAL historical F19 category whose Hom consists
of original strong modifications between chosen mate presentations. -/
abbrev F19 (F G : Pseudofunctor B E) :=
  LeftMatePresentation F G

/-- This is the ACTUAL mathlib category quotient by the F28 compression
kernel congruence; it is not an unquotiented F26 comparison chain. -/
abbrev F28 (aF bF aG bG : E) :=
  compressionKernelCategory aF bF aG bG

/-- Real F19/F28 two-axis primitive exchange classes preserve the full
finite F36 paths separately on each historical source category. -/
theorem originalF19F28_exchange_rawPaths
    (F G : Pseudofunctor B E) (aF bF aG bG : E)
    {a b : F19 F G} {x y : F28 aF bF aG bG}
    {n m : Nat}
    {ma mb : OldBlocks a b} {pa pb : OldBlocks x y}
    (c : ExchangeClass n m ma mb pa pb) :
    ma.flatten = mb.flatten ∧ pa.flatten = pb.flatten :=
  actualExchange_twoAxis_flatten_eq c

/-- The actual F19 chosen RIGHT-mate functor and the actual F28
compression-quotient functor preserve BOTH original raw path words.
This is a fact about two distinct functors on their original categories,
not an invented F19/F28 equivalence or higher Gray descent. -/
theorem originalF19F28_exchange_mate_compression_paths
    (F G : Pseudofunctor B E) (aF bF aG bG : E)
    {a b : F19 F G} {x y : F28 aF bF aG bG}
    {n m : Nat}
    {ma mb : OldBlocks a b} {pa pb : OldBlocks x y}
    (c : ExchangeClass n m ma mb pa pb) :
    (mapBlocks (rightMateFunctor F G) ma).flatten =
      (mapBlocks (rightMateFunctor F G) mb).flatten ∧
    (mapBlocks (quotientCompositeFunctor aF bF aG bG) pa).flatten =
      (mapBlocks (quotientCompositeFunctor aF bF aG bG) pb).flatten := by
  rcases originalF19F28_exchange_rawPaths F G aF bF aG bG c with ⟨h19, h28⟩
  constructor
  · simpa only [mapBlocks_flatten] using
      congrArg
        (KUOS.DependentOriginationCoherentBiadjunctionFiniteModificationMatePathsV5_135.Finite.mapPath
          (rightMateFunctor F G)) h19
  · simpa only [mapBlocks_flatten] using
      congrArg
        (KUOS.DependentOriginationCoherentBiadjunctionFiniteModificationMatePathsV5_135.Finite.mapPath
          (quotientCompositeFunctor aF bF aG bG)) h28

/-- Every genuine F19/F28 exchange class has Type-valued Kuu raw
representatives on both independently typed axes. Existence is in Prop
and makes no unproved claim of a faithful history equivalence. -/
theorem originalF19F28_exchange_has_native_histories
    (F G : Pseudofunctor B E) (aF bF aG bG : E)
    {a b : F19 F G} {x y : F28 aF bF aG bG}
    {n m : Nat}
    {ma mb : OldBlocks a b} {pa pb : OldBlocks x y}
    (c : ExchangeClass n m ma mb pa pb) :
    Nonempty (
      KuuNativeAxisTrace n (oldBlocksToNative ma) (oldBlocksToNative mb) ×
      KuuNativeAxisTrace m (oldBlocksToNative pa) (oldBlocksToNative pb)) :=
  actualExchange_nativeTwoAxis_nonempty c

end GenuineF19F28

#print axioms nativeTwoAxisToActualExchange
#print axioms nativeTwoAxisToActualExchange_axisTraces
#print axioms actualExchange_twoAxis_flatten_eq
#print axioms actualExchange_nativeTwoAxis_nonempty
#print axioms nativeTwoAxisToActualExchange_not_injective_first
#print axioms nativeTwoAxisToActualExchange_not_injective_second
#print axioms GenuineF19F28.F19
#print axioms GenuineF19F28.F28
#print axioms GenuineF19F28.originalF19F28_exchange_rawPaths
#print axioms GenuineF19F28.originalF19F28_exchange_mate_compression_paths
#print axioms GenuineF19F28.originalF19F28_exchange_has_native_histories


/-!
## F112-P7 — actual original F47 four-boundary square with two native axes

Unlike an artificial face/rotation product, the historical F47 frame
B stores a real truncated-icosahedron physical edge, an original F42
face comparison between genuinely typed polygon cells, and an actual
F55 rotation 3-arrow between TWO independently typed original F54
routes, together with its proved full-native calibration.

The two routes have the SAME original bracket-tree endpoints. Their
F44 exchange classes admit independently reconstructed Kuu witnesses
of exact original F19/F28 primitive depths (P5/P6). The original
F55 route equations and F47 mixed source square remain genuine
proofs with their separately typed four boundaries. The nonzero
comparison charge is retained; no F47 ≌ independent Kuu equivalence
or forbidden Gray import into KuuOSStrict is claimed.
-/

namespace GenuineOriginalF47
open KUOS.DependentOriginationGrayC60MixedBoundaryThreeHomV5_195
open KUOS.DependentOriginationGrayC60PresentedFaceTwoCellsV5_190
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84

variable {a b : C} {x y : D}
variable {n n' m m' : Nat}
variable {ma mb : OldBlocks a b} {pa pb : OldBlocks x y}
variable {first : OriginalF45BracketTree n m ma pa mb pb}
variable {last : OriginalF45BracketTree n' m' ma pa mb pb}
variable {v w : IcosahedralDart} {p q : Quiver.Path v w}
variable {α β : C60F42PresentedFaceCell p q}
variable {r s : OriginalF45BracketTree.DepthRotationRoute first last}

/-- A witness on an ACTUAL old F47 calibrated four-boundary frame.
The complete original F42 face and F55 route arrows, physical edge,
and four separate source positions are retained by the INDEX B.
Each native axis is a genuine Type-valued refinement history over
the original F19/F28 F40 blocks, not a numerical grade or a Bool site.

The relation is intentionally one-way: historical F42 primitive
proof irrelevance prevents recovering a unique native history. -/
structure F47NativeBoundaryWitness
    (B : C60F47SquareFrame α β r s) where
  firstNative :
    KuuNativeAxisTrace n (oldBlocksToNative ma) (oldBlocksToNative mb) ×
      KuuNativeAxisTrace m (oldBlocksToNative pa) (oldBlocksToNative pb)
  lastNative :
    KuuNativeAxisTrace n' (oldBlocksToNative ma) (oldBlocksToNative mb) ×
      KuuNativeAxisTrace m' (oldBlocksToNative pa) (oldBlocksToNative pb)
  firstRouteF44 :
    ExchangeClass.castDepths r.depthEq.1 r.depthEq.2
      first.toExchangeClass = last.toExchangeClass
  secondRouteF44 :
    ExchangeClass.castDepths s.depthEq.1 s.depthEq.2
      first.toExchangeClass = last.toExchangeClass
  originalMixedSquare :
    c60F47FaceArrow B ≫ c60F47CompareAfter B =
      c60F47CompareBefore B ≫ c60F47OriginalF55Arrow B

/-- Build the native witness over any ACTUAL calibrated F47 source
frame, using previously proved reverse existence of historical F45
histories. No original face or F55 rotation source is replaced. -/
noncomputable def F47NativeBoundaryWitness.ofFrame
    (B : C60F47SquareFrame α β r s) :
    F47NativeBoundaryWitness B where
  firstNative :=
    (historicalAxisTrace_chooseNative first.axisHistories.1,
      historicalAxisTrace_chooseNative first.axisHistories.2)
  lastNative :=
    (historicalAxisTrace_chooseNative last.axisHistories.1,
      historicalAxisTrace_chooseNative last.axisHistories.2)
  firstRouteF44 := r.toExchangeClass_eq
  secondRouteF44 := s.toExchangeClass_eq
  originalMixedSquare := c60F47MixedOriginalBoundarySquare B

/-- The ACTUAL reconstructed first F19/F28 histories preserve both
complete ordered original F36 words, derived from their native traces
through the P4 constructor-level equivalences. This does not merely
assert equality of their final categorical composite Homs. -/
theorem F47NativeBoundaryWitness.first_raw_paths
    {B : C60F47SquareFrame α β r s}
    (packet : F47NativeBoundaryWitness B) :
    ma.flatten = mb.flatten ∧ pa.flatten = pb.flatten := by
  constructor
  · apply (oldPathEquivNative (C := C)).injective
    calc
      oldPathToNative ma.flatten = (oldBlocksToNative ma).flatten :=
        oldBlocksToNative_flatten ma
      _ = (oldBlocksToNative mb).flatten :=
        packet.firstNative.1.flatten_eq
      _ = oldPathToNative mb.flatten :=
        (oldBlocksToNative_flatten mb).symm
  · apply (oldPathEquivNative (C := D)).injective
    calc
      oldPathToNative pa.flatten = (oldBlocksToNative pa).flatten :=
        oldBlocksToNative_flatten pa
      _ = (oldBlocksToNative pb).flatten :=
        packet.firstNative.2.flatten_eq
      _ = oldPathToNative pb.flatten :=
        (oldBlocksToNative_flatten pb).symm

/-- The same original F36 word conservation holds for the separately
typed LAST F54/F55 bracket-tree endpoint, even if its two Nat depths
differ syntactically before the proved F55 depth casts. -/
theorem F47NativeBoundaryWitness.last_raw_paths
    {B : C60F47SquareFrame α β r s}
    (packet : F47NativeBoundaryWitness B) :
    ma.flatten = mb.flatten ∧ pa.flatten = pb.flatten := by
  constructor
  · apply (oldPathEquivNative (C := C)).injective
    calc
      oldPathToNative ma.flatten = (oldBlocksToNative ma).flatten :=
        oldBlocksToNative_flatten ma
      _ = (oldBlocksToNative mb).flatten :=
        packet.lastNative.1.flatten_eq
      _ = oldPathToNative mb.flatten :=
        (oldBlocksToNative_flatten mb).symm
  · apply (oldPathEquivNative (C := D)).injective
    calc
      oldPathToNative pa.flatten = (oldBlocksToNative pa).flatten :=
        oldBlocksToNative_flatten pa
      _ = (oldBlocksToNative pb).flatten :=
        packet.lastNative.2.flatten_eq
      _ = oldPathToNative pb.flatten :=
        (oldBlocksToNative_flatten pb).symm

/-- The witness keeps BOTH independently typed actual F55 routes
and the genuinely commuting mixed F47 source four-boundary square.
The casted F44 equations are not claimed to identify original
F42 face source objects with old F54 rotation source objects. -/
theorem F47NativeBoundaryWitness.actual_square_and_routes
    {B : C60F47SquareFrame α β r s}
    (packet : F47NativeBoundaryWitness B) :
    (ExchangeClass.castDepths r.depthEq.1 r.depthEq.2
      first.toExchangeClass = last.toExchangeClass) ∧
    (ExchangeClass.castDepths s.depthEq.1 s.depthEq.2
      first.toExchangeClass = last.toExchangeClass) ∧
    (c60F47FaceArrow B ≫ c60F47CompareAfter B =
      c60F47CompareBefore B ≫ c60F47OriginalF55Arrow B) :=
  ⟨packet.firstRouteF44, packet.secondRouteF44, packet.originalMixedSquare⟩

/-- Even with both full original F36 words conserved and the F44
route classes agreeing, the genuine MIXED F47 after-comparison keeps
its independent, calibrated nonzero square charge and phase zero.
The original F55/F42 three-Hom comparison is not erased by a Kuu
primitive refinement history. -/
theorem F47NativeBoundaryWitness.square_charge_retained
    {B : C60F47SquareFrame α β r s}
    (packet : F47NativeBoundaryWitness B) :
    (c60F47FaceArrow B ≫ c60F47CompareAfter B =
      c60F47CompareBefore B ≫ c60F47OriginalF55Arrow B) ∧
    ((c60F47MixedGrayFunctor B).map
      (c60F47CompareAfter B)).charge = ((0 : Int), (1 : Int)) ∧
    ((c60F47MixedGrayFunctor B).map
      (c60F47CompareAfter B)).phase = (0 : ZMod 2) :=
  ⟨packet.originalMixedSquare,
    (c60F47CompareAfter_native_components B).1,
    (c60F47CompareAfter_native_components B).2⟩

/-- Every actually calibrated F47 frame on an original physical edge
admits this four-boundary/native-history witness with independently
typed source axes. Existence is in Prop; no faithful inverse is inferred. -/
theorem actualF47Frame_has_native_boundary
    (B : C60F47SquareFrame α β r s) :
    Nonempty (F47NativeBoundaryWitness B) :=
  ⟨F47NativeBoundaryWitness.ofFrame B⟩

#print axioms F47NativeBoundaryWitness
#print axioms F47NativeBoundaryWitness.ofFrame
#print axioms F47NativeBoundaryWitness.first_raw_paths
#print axioms F47NativeBoundaryWitness.last_raw_paths
#print axioms F47NativeBoundaryWitness.actual_square_and_routes
#print axioms F47NativeBoundaryWitness.square_charge_retained
#print axioms actualF47Frame_has_native_boundary

end GenuineOriginalF47


/-!
## F112-P8 — exact independent Kuu ↔ original C60 combinatorial geometry

The independent C60 physical seed and the historical F47 physics
were constructed separately. All their 12 original vertices,
30 original edges, 20 original triangles, 60 dart sites, 32
polygon sites and 90 true C60 edges are now compared by genuine
Mathlib Equiv maps, not by cardinalities, a Bool surrogate or
an inferred isomorphism of the entire higher source category.

The maps also commute with original oriented endpoints, the
five-slot cyclic incident-dart order and every 90-edge pair
of physical dart endpoints. Consequently the edge stored by
ANY actually calibrated F47 four-boundary square is transported
into an independent Kuu C60 physical edge with its EXACT
incidence preserved. F42 face cells and F54/F55 routes remain
independently typed original source witnesses.
-/

namespace GenuineOriginalC60Geometry

open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85

/-- All twelve actual source vertices are matched constructor-wise. -/
def vertexEquiv : Vertex ≃ IcosahedralVertex where
  toFun
    | .north => .north
    | .south => .south
    | .upper i => .upper i
    | .lower i => .lower i
  invFun
    | .north => .north
    | .south => .south
    | .upper i => .upper i
    | .lower i => .lower i
  left_inv := by
    intro v
    cases v <;> rfl
  right_inv := by
    intro v
    cases v <;> rfl

/-- All six real original icosahedral edge families, retaining
the original ordered ZMod 5 coordinate. -/
def origEdgeEquiv : OrigEdge ≃ IcosahedralEdge where
  toFun
    | .northSpoke i => .northSpoke i
    | .southSpoke i => .southSpoke i
    | .upperRing i => .upperRing i
    | .lowerRing i => .lowerRing i
    | .crossAligned i => .crossAligned i
    | .crossShifted i => .crossShifted i
  invFun
    | .northSpoke i => .northSpoke i
    | .southSpoke i => .southSpoke i
    | .upperRing i => .upperRing i
    | .lowerRing i => .lowerRing i
    | .crossAligned i => .crossAligned i
    | .crossShifted i => .crossShifted i
  left_inv := by
    intro e
    cases e <;> rfl
  right_inv := by
    intro e
    cases e <;> rfl

/-- All twenty original triangles, preserving their real incidence
family and unchanged ZMod 5 rotational index. -/
def triangleEquiv : Triangle ≃ IcosahedralFace where
  toFun
    | .top i => .top i
    | .bottom i => .bottom i
    | .beltUpper i => .beltUpper i
    | .beltLower i => .beltLower i
  invFun
    | .top i => .top i
    | .bottom i => .bottom i
    | .beltUpper i => .beltUpper i
    | .beltLower i => .beltLower i
  left_inv := by
    intro t
    cases t <;> rfl
  right_inv := by
    intro t
    cases t <;> rfl

/-- The FIVE original cyclic pentagon slots, not an abstract
equicardinality proof. -/
def slotEquiv : Slot ≃ PentagonalSlot where
  toFun
    | .s0 => .s0
    | .s1 => .s1
    | .s2 => .s2
    | .s3 => .s3
    | .s4 => .s4
  invFun
    | .s0 => .s0
    | .s1 => .s1
    | .s2 => .s2
    | .s3 => .s3
    | .s4 => .s4
  left_inv := by
    intro s
    cases s <;> rfl
  right_inv := by
    intro s
    cases s <;> rfl

/-- Historical and native pentagon cyclic-index functions agree
EXACTLY, on every one of the five actual physical slots. -/
theorem slotIndex_equiv (s : Slot) :
    pentagonalSlotIndex (slotEquiv s) = slotIndex s := by
  cases s <;> rfl

/-- Historical and independent rotations have the SAME five-step
successor on real incident darts, not an arbitrary permutation. -/
theorem slotNext_equiv (s : Slot) :
    slotEquiv (slotNext s) = pentagonalSlotNext (slotEquiv s) := by
  cases s <;> rfl

/-- Each actual physical C60 vertex is an original directed dart
and the source choice of first versus second remains unchanged. -/
def dartEquiv : Dart ≃ IcosahedralDart where
  toFun
    | .first e => .first (origEdgeEquiv e)
    | .second e => .second (origEdgeEquiv e)
  invFun
    | .first e => .first (origEdgeEquiv.symm e)
    | .second e => .second (origEdgeEquiv.symm e)
  left_inv := by
    intro d
    cases d with
    | first e => cases e <;> rfl
    | second e => cases e <;> rfl
  right_inv := by
    intro d
    cases d with
    | first e => cases e <;> rfl
    | second e => cases e <;> rfl

/-- Actual 32 polygonal sites: the twelve vertex-origin pentagons
and twenty triangle-origin hexagons are preserved without mixing. -/
def polygonEquiv : Polygon ≃ TruncatedIcosahedralSeedFace where
  toFun
    | .pentagon v => .aroundVertex (vertexEquiv v)
    | .hexagon t => .fromTriangle (triangleEquiv t)
  invFun
    | .aroundVertex v => .pentagon (vertexEquiv.symm v)
    | .fromTriangle t => .hexagon (triangleEquiv.symm t)
  left_inv := by
    intro p
    cases p with
    | pentagon v => cases v <;> rfl
    | hexagon t => cases t <;> rfl
  right_inv := by
    intro p
    cases p with
    | aroundVertex v => cases v <;> rfl
    | fromTriangle t => cases t <;> rfl

/-- The sixty around-pentagon edges carry BOTH their physical
icosahedral center and their exact cyclic slot. -/
def aroundEquiv : AroundEdge ≃ TruncatedIcosahedralAroundEdge where
  toFun a := ⟨vertexEquiv a.center, slotEquiv a.slot⟩
  invFun a := ⟨vertexEquiv.symm a.center, slotEquiv.symm a.slot⟩
  left_inv := by
    rintro ⟨v, s⟩
    cases v <;> cases s <;> rfl
  right_inv := by
    rintro ⟨v, s⟩
    cases v <;> cases s <;> rfl

/-- True 90-edge C60 equivalence: 30 cross-dart edges and 60
around-vertex consecutive-dart edges. No numerical-only argument. -/
def edgeEquiv : Edge ≃ TruncatedIcosahedralEdge where
  toFun
    | .cross e => .cross (origEdgeEquiv e)
    | .around a => .around (aroundEquiv a)
  invFun
    | .cross e => .cross (origEdgeEquiv.symm e)
    | .around a => .around (aroundEquiv.symm a)
  left_inv := by
    intro e
    cases e with
    | cross e => cases e <;> rfl
    | around a =>
        rcases a with ⟨v,s⟩
        cases v <;> cases s <;> rfl
  right_inv := by
    intro e
    cases e with
    | cross e => cases e <;> rfl
    | around a =>
        rcases a with ⟨v,s⟩
        cases v <;> cases s <;> rfl

/-- This is stronger than the equality of 30 old-edge counts:
the exact first and second original endpoints agree. -/
theorem origEdgeEndpoints_equiv (e : OrigEdge) :
    (icosahedralEdgeEndpoints (origEdgeEquiv e)).1 =
      vertexEquiv (endpoints e).1 ∧
    (icosahedralEdgeEndpoints (origEdgeEquiv e)).2 =
      vertexEquiv (endpoints e).2 := by
  cases e <;> exact ⟨rfl, rfl⟩

/-- The original endpoint vertex of EVERY independently constructed
C60 dart is preserved by the nontrivial old/new equivalence. -/
theorem dartEndpoint_equiv (d : Dart) :
    (dartEquiv d).endpoint = vertexEquiv d.endpoint := by
  cases d with
  | first e => cases e <;> rfl
  | second e => cases e <;> rfl

/-- The cyclic order at all 12 original vertices and all 5 slots
is literally preserved. Hence neither the pentagon orientation
nor any of its dart-boundary incidence data is collapsed. -/
theorem incidentDart_equiv (v : Vertex) (s : Slot) :
    dartEquiv (incidentDart v s) =
      icosahedralIncidentDartAt (vertexEquiv v) (slotEquiv s) := by
  cases v <;> cases s <;> rfl

/-- The actual old truncated around-edge preserves BOTH ordered
real dart endpoints, derived from cyclic-slot compatibility. -/
theorem aroundEndpoints_equiv (a : AroundEdge) :
    (truncatedIcosahedralAroundEdgeEndpoints (aroundEquiv a)).1 =
      dartEquiv (aroundEndpoints a).1 ∧
    (truncatedIcosahedralAroundEdgeEndpoints (aroundEquiv a)).2 =
      dartEquiv (aroundEndpoints a).2 := by
  rcases a with ⟨v, s⟩
  constructor
  · exact (incidentDart_equiv v s).symm
  · rw [← slotNext_equiv s]
    exact (incidentDart_equiv v (slotNext s)).symm

/-- All ninety physically realized independent edge incidences
are transported to the ACTUAL old C60 ordered dart endpoints. -/
theorem edgeEndpoints_equiv (e : Edge) :
    (truncatedIcosahedralEdgeEndpoints (edgeEquiv e)).1 =
      dartEquiv (edgeEndpoints e).1 ∧
    (truncatedIcosahedralEdgeEndpoints (edgeEquiv e)).2 =
      dartEquiv (edgeEndpoints e).2 := by
  cases e with
  | cross e => exact ⟨rfl, rfl⟩
  | around a => exact aroundEndpoints_equiv a

namespace ActualF47
open KUOS.DependentOriginationGrayC60MixedBoundaryThreeHomV5_195
open KUOS.DependentOriginationGrayC60PresentedFaceTwoCellsV5_190

variable {a b : C} {x y : D} {n n' m m' : Nat}
variable {ma mb : OldBlocks a b} {pa pb : OldBlocks x y}
variable {first : OriginalF45BracketTree n m ma pa mb pb}
variable {last : OriginalF45BracketTree n' m' ma pa mb pb}
variable {v w : IcosahedralDart} {p q : Quiver.Path v w}
variable {α β : C60F42PresentedFaceCell p q}
variable {r s : OriginalF45BracketTree.DepthRotationRoute first last}

/-- The REAL physical edge stored by an existing original F47
four-boundary source frame, now reconstructed as a Kuu physical
C60 edge (not an arbitrary member of Fin 90). -/
def frameKuuEdge (B : C60F47SquareFrame α β r s) : Edge :=
  edgeEquiv.symm B.edge

/-- The actual F47 physical edge is recovered exactly, including
its cross/around tag, and not merely its full native charge. -/
theorem frameKuuEdge_roundtrip (B : C60F47SquareFrame α β r s) :
    edgeEquiv (frameKuuEdge B) = B.edge :=
  edgeEquiv.apply_symm_apply B.edge

/-- Every real F47 boundary frame thus carries the same two
ordered physical dart endpoints as its independent Kuu edge. -/
theorem frameKuuEdge_endpoints (B : C60F47SquareFrame α β r s) :
    (truncatedIcosahedralEdgeEndpoints B.edge).1 =
      dartEquiv (edgeEndpoints (frameKuuEdge B)).1 ∧
    (truncatedIcosahedralEdgeEndpoints B.edge).2 =
      dartEquiv (edgeEndpoints (frameKuuEdge B)).2 := by
  simpa only [frameKuuEdge_roundtrip] using
    edgeEndpoints_equiv (frameKuuEdge B)

end ActualF47

#print axioms vertexEquiv
#print axioms origEdgeEquiv
#print axioms triangleEquiv
#print axioms slotEquiv
#print axioms slotIndex_equiv
#print axioms slotNext_equiv
#print axioms dartEquiv
#print axioms polygonEquiv
#print axioms aroundEquiv
#print axioms edgeEquiv
#print axioms origEdgeEndpoints_equiv
#print axioms dartEndpoint_equiv
#print axioms incidentDart_equiv
#print axioms aroundEndpoints_equiv
#print axioms edgeEndpoints_equiv
#print axioms ActualF47.frameKuuEdge
#print axioms ActualF47.frameKuuEdge_roundtrip
#print axioms ActualF47.frameKuuEdge_endpoints

end GenuineOriginalC60Geometry

end
end KUOS.F112ActualHistoricalF36F40BridgeP4
