import Kuu.F112.PolygonF36F40ShapeFunctorC60
import KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137
import Kuu.F112.PolygonNativeF41ComparisonObstruction
import KUOS.DependentOriginationCoherentBiadjunctionProofRelevantAxisTracesV5_142

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

/-- The independent Type-valued primitive refinement is realized as
the SAME genuinely historical F42 Prop generator on original F40 Blocks.
Only the split case needs P4's proved full-path concatenation lemma. -/
def nativeOneStepToHistorical {x y : C}
    {p q : KuuNativeBlocks x y}
    (h : KuuNativeOneStep p q) :
    HistoricalOneStep (nativeBlocksToOld p) (nativeBlocksToOld q) := by
  induction h with
  | split p q r =>
      change HistoricalOneStep
        (.snoc (nativeBlocksToOld p) (nativePathToOld (q.append r)))
        (.snoc (.snoc (nativeBlocksToOld p) (nativePathToOld q))
          (nativePathToOld r))
      rw [nativePathToOld_append]
      exact OneStep.split (nativeBlocksToOld p)
        (nativePathToOld q) (nativePathToOld r)
  | insertNil p =>
      change HistoricalOneStep (nativeBlocksToOld p)
        (.snoc (nativeBlocksToOld p) (.nil _))
      exact OneStep.insertNil (nativeBlocksToOld p)
  | whisker h t ih =>
      exact OneStep.whisker ih (nativePathToOld t)

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
      change Nonempty (KuuNativeOneStep
        (.snoc (oldBlocksToNative p) (oldPathToNative (q.append r)))
        (.snoc (.snoc (oldBlocksToNative p) (oldPathToNative q))
          (oldPathToNative r)))
      rw [oldPathToNative_append]
      exact ⟨KuuNativeOneStep.split (oldBlocksToNative p)
        (oldPathToNative q) (oldPathToNative r)⟩
  | insertNil p =>
      exact ⟨KuuNativeOneStep.insertNil (oldBlocksToNative p)⟩
  | whisker h t ih =>
      rcases ih with ⟨witness⟩
      exact ⟨KuuNativeOneStep.whisker witness (oldPathToNative t)⟩

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

end
end KUOS.F112ActualHistoricalF36F40BridgeP4
