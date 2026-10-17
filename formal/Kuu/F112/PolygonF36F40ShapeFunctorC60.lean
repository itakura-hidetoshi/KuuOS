import Kuu.F112.PolygonF36F40IndependentShapeEquivalence
import Kuu.F112.PolygonNativeF40FunctorComparison

/-!
# F112-E7Q5-F4-P3-B — fully functorial F36/F40 shape bridge on C60

The independent reversible constructor interpretations of P3-A are
natural in arbitrary ordinary category functors. Every actual Hom,
all intermediate category objects, every path arrow and each F40
subdivision boundary remain accounted for. The bridge commutes with
append, flatten, block count and honest categorical evaluation.

Genuine north-pentagon and arbitrary C60 sectors furnish concrete
two-arrow/two-block versus diagonal/one-block noncollapse witnesses.

This proves exact SHAPE compatibility with the frozen historic
F36/F40 constructor signatures, without identifying these NEW Types
with the frozen old KUOS types or importing Gray/old KUOS.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
noncomputable section

universe uA vA uB vB
variable {A : Type uA} [Category.{vA} A]
variable {B : Type uB} [Category.{vB} B]

/-- All intermediate objects and actual categorical arrows map
one-for-one in the independent F36 original-shaped grammar. -/
def KuuF36ShapePath.map (F : A ⥤ B) :
    ∀ {x y : A}, KuuF36ShapePath x y →
      KuuF36ShapePath (F.obj x) (F.obj y)
  | _, _, .nil x => .nil (F.obj x)
  | _, _, .snoc p f => .snoc (p.map F) (F.map f)

/-- The equivalence to genuine independent Kuu finite paths is
NATURAL as a strict equality of complete Type-valued raw paths. -/
theorem KuuF36ShapePath.toNative_map (F : A ⥤ B)
    {x y : A} (p : KuuF36ShapePath x y) :
    (p.map F).toNative = p.toNative.map F := by
  induction p with
  | nil x => rfl
  | snoc p f ih =>
      change KuuNativePath.snoc (p.map F).toNative (F.map f) =
        KuuNativePath.snoc (p.toNative.map F) (F.map f)
      rw [ih]

/-- The opposite direction of the equivalence is also NATURAL,
not merely an agreement of scalar path lengths. -/
theorem KuuF36ShapePath.ofNative_map (F : A ⥤ B)
    {x y : A} (p : KuuNativePath x y) :
    KuuF36ShapePath.ofNative (p.map F) =
      (KuuF36ShapePath.ofNative p).map F := by
  apply (kuuF36ShapePathEquiv (C := B)).injective
  change (KuuF36ShapePath.ofNative (p.map F)).toNative =
    ((KuuF36ShapePath.ofNative p).map F).toNative
  rw [KuuF36ShapePath.toNative_ofNative,
    KuuF36ShapePath.toNative_map,
    KuuF36ShapePath.toNative_ofNative]

theorem KuuF36ShapePath.composite_map (F : A ⥤ B)
    {x y : A} (p : KuuF36ShapePath x y) :
    (p.map F).composite = F.map p.composite := by
  calc
    (p.map F).composite = (p.map F).toNative.composite :=
      (KuuF36ShapePath.toNative_composite (p.map F)).symm
    _ = (p.toNative.map F).composite :=
      congrArg KuuNativePath.composite (p.toNative_map F)
    _ = F.map p.toNative.composite :=
      KuuNativePath.composite_map F p.toNative
    _ = F.map p.composite :=
      congrArg (fun h : x ⟶ y => F.map h) p.toNative_composite

/-- The independently re-presented F40 grammar transports entire
F36 path segments, not just Hom composites or counted blocks. -/
def KuuF40ShapeBlocks.map (F : A ⥤ B) :
    ∀ {x y : A}, KuuF40ShapeBlocks x y →
      KuuF40ShapeBlocks (F.obj x) (F.obj y)
  | _, _, .empty x => .empty (F.obj x)
  | _, _, .snoc p q => .snoc (p.map F) (q.map F)

/-- The precise nested equivalence commutes with ordinary functors,
including arbitrarily many empty block paths and intermediate Hom. -/
theorem KuuF40ShapeBlocks.toNative_map (F : A ⥤ B)
    {x y : A} (p : KuuF40ShapeBlocks x y) :
    (p.map F).toNative = p.toNative.map F := by
  induction p with
  | empty x => rfl
  | snoc p q ih =>
      change KuuNativeBlocks.snoc (p.map F).toNative (q.map F).toNative =
        KuuNativeBlocks.snoc (p.toNative.map F) (q.toNative.map F)
      rw [ih, KuuF36ShapePath.toNative_map]

theorem KuuF40ShapeBlocks.ofNative_map (F : A ⥤ B)
    {x y : A} (p : KuuNativeBlocks x y) :
    KuuF40ShapeBlocks.ofNative (p.map F) =
      (KuuF40ShapeBlocks.ofNative p).map F := by
  apply (kuuF40ShapeBlocksEquiv (C := B)).injective
  change (KuuF40ShapeBlocks.ofNative (p.map F)).toNative =
    ((KuuF40ShapeBlocks.ofNative p).map F).toNative
  rw [KuuF40ShapeBlocks.toNative_ofNative,
    KuuF40ShapeBlocks.toNative_map,
    KuuF40ShapeBlocks.toNative_ofNative]

/-- Flattening BEFORE or AFTER transport yields identical whole
historical-shaped F36 raw paths. Separators are erased only by the
explicit flatten operation, never by the equivalence itself. -/
theorem KuuF40ShapeBlocks.flatten_map (F : A ⥤ B)
    {x y : A} (p : KuuF40ShapeBlocks x y) :
    (p.map F).flatten = (p.flatten).map F := by
  apply (kuuF36ShapePathEquiv (C := B)).injective
  change (p.map F).flatten.toNative = (p.flatten.map F).toNative
  rw [KuuF40ShapeBlocks.toNative_flatten,
    KuuF36ShapePath.toNative_map,
    KuuF40ShapeBlocks.toNative_flatten,
    KuuF40ShapeBlocks.toNative_map]
  exact KuuNativeBlocks.flatten_map F p.toNative

theorem KuuF40ShapeBlocks.composite_map (F : A ⥤ B)
    {x y : A} (p : KuuF40ShapeBlocks x y) :
    (p.map F).composite = F.map p.composite := by
  calc
    (p.map F).composite = (p.map F).toNative.composite :=
      (KuuF40ShapeBlocks.toNative_composite (p.map F)).symm
    _ = (p.toNative.map F).composite :=
      congrArg KuuNativeBlocks.composite (p.toNative_map F)
    _ = F.map p.toNative.composite :=
      KuuNativeBlocks.composite_map F p.toNative
    _ = F.map p.composite :=
      congrArg (fun h : x ⟶ y => F.map h) p.toNative_composite

theorem KuuF40ShapeBlocks.blockCount_map (F : A ⥤ B)
    {x y : A} (p : KuuF40ShapeBlocks x y) :
    (p.map F).blockCount = p.blockCount := by
  calc
    (p.map F).blockCount = (p.map F).toNative.blockCount :=
      (KuuF40ShapeBlocks.toNative_blockCount (p.map F)).symm
    _ = (p.toNative.map F).blockCount :=
      congrArg KuuNativeBlocks.blockCount (p.toNative_map F)
    _ = p.toNative.blockCount := KuuNativeBlocks.blockCount_map F p.toNative
    _ = p.blockCount := p.toNative_blockCount

/-- The real C60 vertex→edge→face path is instantiated on genuine
Site arrows in the new reversible F36 constructor presentation. -/
def polygonSectorF36ShapeTwoStep (p : Polygon)
    (i : PolygonBoundarySector p) :
    KuuF36ShapePath
      (Site.vertex (cyclicBoundaryDart p i.1.val)) (Site.face p) :=
  KuuF36ShapePath.ofNative (polygonSectorNativeTwoStep p i)

/-- A separate real source vertex→face diagonal arrow, not the
two-step physical edge path. -/
def polygonSectorF36ShapeDiagonal (p : Polygon)
    (i : PolygonBoundarySector p) :
    KuuF36ShapePath
      (Site.vertex (cyclicBoundaryDart p i.1.val)) (Site.face p) :=
  KuuF36ShapePath.ofNative (polygonSectorNativeDiagonal p i)

/-- Exact two-versus-one original categorical Hom path distinction
is reflected by the injective constructor bridge. -/
theorem polygonSectorF36Shape_twoStep_ne_diagonal (p : Polygon)
    (i : PolygonBoundarySector p) :
    polygonSectorF36ShapeTwoStep p i ≠
      polygonSectorF36ShapeDiagonal p i := by
  intro h
  apply polygonSectorTwoStep_ne_diagonal p i
  have he := congrArg KuuF36ShapePath.toNative h
  simpa only [polygonSectorF36ShapeTwoStep, polygonSectorF36ShapeDiagonal,
    KuuF36ShapePath.toNative_ofNative] using he

def polygonSectorF40ShapeTwoBlocks (p : Polygon)
    (i : PolygonBoundarySector p) :
    KuuF40ShapeBlocks
      (Site.vertex (cyclicBoundaryDart p i.1.val)) (Site.face p) :=
  KuuF40ShapeBlocks.ofNative (polygonSectorTwoBlocks p i)

def polygonSectorF40ShapeOneBlock (p : Polygon)
    (i : PolygonBoundarySector p) :
    KuuF40ShapeBlocks
      (Site.vertex (cyclicBoundaryDart p i.1.val)) (Site.face p) :=
  KuuF40ShapeBlocks.ofNative (polygonSectorOneBlock p i)

/-- GENUINE C60 source subdivisions remain distinct on the raw F40
original-shaped presentation: TWO real block segments versus ONE. -/
theorem polygonSectorF40Shape_two_ne_one (p : Polygon)
    (i : PolygonBoundarySector p) :
    polygonSectorF40ShapeTwoBlocks p i ≠
      polygonSectorF40ShapeOneBlock p i := by
  intro h
  apply polygonSectorTwoBlocks_ne_oneBlock p i
  have he := congrArg KuuF40ShapeBlocks.toNative h
  simpa only [polygonSectorF40ShapeTwoBlocks, polygonSectorF40ShapeOneBlock,
    KuuF40ShapeBlocks.toNative_ofNative] using he

/-- The two different genuine C60 raw F40 presentations have the
SAME category Hom evaluation, solely by actual Site incidence. -/
theorem polygonSectorF40Shape_composite_eq (p : Polygon)
    (i : PolygonBoundarySector p) :
    (polygonSectorF40ShapeTwoBlocks p i).composite =
      (polygonSectorF40ShapeOneBlock p i).composite := by
  change (KuuF40ShapeBlocks.ofNative (polygonSectorTwoBlocks p i)).composite =
    (KuuF40ShapeBlocks.ofNative (polygonSectorOneBlock p i)).composite
  rw [← KuuF40ShapeBlocks.toNative_composite,
    ← KuuF40ShapeBlocks.toNative_composite,
    KuuF40ShapeBlocks.toNative_ofNative,
    KuuF40ShapeBlocks.toNative_ofNative]
  exact polygonSectorBlocks_composite_eq p i

#print axioms KuuF36ShapePath.toNative_map
#print axioms KuuF36ShapePath.ofNative_map
#print axioms KuuF36ShapePath.composite_map
#print axioms KuuF40ShapeBlocks.toNative_map
#print axioms KuuF40ShapeBlocks.ofNative_map
#print axioms KuuF40ShapeBlocks.flatten_map
#print axioms KuuF40ShapeBlocks.composite_map
#print axioms KuuF40ShapeBlocks.blockCount_map
#print axioms polygonSectorF36Shape_twoStep_ne_diagonal
#print axioms polygonSectorF40Shape_two_ne_one
#print axioms polygonSectorF40Shape_composite_eq
end
end Kuu.F112.Physical
