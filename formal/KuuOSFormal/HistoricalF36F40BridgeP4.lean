import Kuu.F112.PolygonF36F40ShapeFunctorC60
import KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137

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
  simp only [oldPathToNative_map, oldPathToNative_nativePathToOld]

/-- The inverse real historical F40 Blocks reconstruction is natural
too, preserving every subdivision and inner categorical Hom. -/
theorem nativeBlocksToOld_map (F : C ⥤ D)
    {x y : C} (s : KuuNativeBlocks x y) :
    mapBlocks F (nativeBlocksToOld s) =
      nativeBlocksToOld (s.map F) := by
  apply (oldBlocksEquivNative (C := D)).injective
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
end
end KUOS.F112ActualHistoricalF36F40BridgeP4
