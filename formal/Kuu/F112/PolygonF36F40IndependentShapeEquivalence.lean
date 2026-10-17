import Kuu.F112.PolygonNativeHistoricalPhysicalNatTrans

/-!
# F112-E7Q5-F4-P3-A — independent faithful F36/F40 constructor presentation

Source inspection (frozen, read only):
  legacy/v5.291/formal/KUOS/
  DependentOriginationCoherentBiadjunctionFiniteHorizontalExchangeV5_133.lean
    Chain.Path: nil, snoc (original CATEGORY Hom)
  DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.lean
    Grid.Blocks: empty, snoc (entire Chain.Path).

P3 supplies an independent SECOND PRESENTATION of those precise TWO
nested inductive grammars. We prove fiberwise Type equivalences to the
already-certified KuuNativePath/KuuNativeBlocks, preserving actual
categorical Hom arrows, intermediate objects and empty block separators,
without importing historical KUOS or claiming that the NEW presentation
is definitionally the FROZEN historical type.

This is a grammar-level equivalence and a certified comparison model;
it does not import or reconstruct the original F19/F28 categories.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
noncomputable section

universe u v
variable {C : Type u} [Category.{v} C]

/-- Literally the frozen F36 Chain.Path TWO-CONSTRUCTOR SHAPE,
but a NEW independent type, not an alias of frozen KUOS.Chain.Path. -/
inductive KuuF36ShapePath : C → C → Type (max u v) where
  | nil (x : C) : KuuF36ShapePath x x
  | snoc {x y z : C} (p : KuuF36ShapePath x y)
      (f : y ⟶ z) : KuuF36ShapePath x z

/-- Forward constructor interpretation: no Hom is evaluated or erased. -/
def KuuF36ShapePath.toNative :
    ∀ {x y : C}, KuuF36ShapePath x y → KuuNativePath x y
  | _, _, .nil x => .nil x
  | _, _, .snoc p f => .snoc p.toNative f

/-- Reverse constructor interpretation retaining all intermediate data. -/
def KuuF36ShapePath.ofNative :
    ∀ {x y : C}, KuuNativePath x y → KuuF36ShapePath x y
  | _, _, .nil x => .nil x
  | _, _, .snoc p f => .snoc (ofNative p) f

theorem KuuF36ShapePath.toNative_ofNative
    {x y : C} (p : KuuNativePath x y) :
    (KuuF36ShapePath.ofNative p).toNative = p := by
  induction p with
  | nil => rfl
  | snoc p f ih =>
      change KuuNativePath.snoc
        (KuuF36ShapePath.ofNative p).toNative f = .snoc p f
      rw [ih]

theorem KuuF36ShapePath.ofNative_toNative
    {x y : C} (p : KuuF36ShapePath x y) :
    KuuF36ShapePath.ofNative p.toNative = p := by
  induction p with
  | nil => rfl
  | snoc p f ih =>
      change KuuF36ShapePath.snoc
        (KuuF36ShapePath.ofNative p.toNative) f = .snoc p f
      rw [ih]

/-- REAL independent fiberwise Type equivalence of exact two-
constructor presentations, not a historical KUOS type identity. -/
def kuuF36ShapePathEquiv {x y : C} :
    KuuF36ShapePath x y ≃ KuuNativePath x y where
  toFun := KuuF36ShapePath.toNative
  invFun := KuuF36ShapePath.ofNative
  left_inv := KuuF36ShapePath.ofNative_toNative
  right_inv := KuuF36ShapePath.toNative_ofNative

/-- Composition is defined on the NEW historical-shaped syntax,
without replacing it with an already evaluated Hom. -/
def KuuF36ShapePath.composite :
    ∀ {x y : C}, KuuF36ShapePath x y → (x ⟶ y)
  | _, _, .nil x => 𝟙 x
  | _, _, .snoc p f => p.composite ≫ f

def KuuF36ShapePath.append {x y z : C}
    (p : KuuF36ShapePath x y) :
    KuuF36ShapePath y z → KuuF36ShapePath x z
  | .nil _ => p
  | .snoc q f => .snoc (p.append q) f

def KuuF36ShapePath.length {x y : C} :
    KuuF36ShapePath x y → Nat
  | .nil _ => 0
  | .snoc p _ => p.length + 1

theorem KuuF36ShapePath.toNative_composite
    {x y : C} (p : KuuF36ShapePath x y) :
    p.toNative.composite = p.composite := by
  induction p with
  | nil => rfl
  | snoc p f ih =>
      change p.toNative.composite ≫ f = p.composite ≫ f
      rw [ih]

theorem KuuF36ShapePath.toNative_length
    {x y : C} (p : KuuF36ShapePath x y) :
    p.toNative.length = p.length := by
  induction p with
  | nil => rfl
  | snoc p f ih =>
      change p.toNative.length + 1 = p.length + 1
      rw [ih]

theorem KuuF36ShapePath.toNative_append
    {x y z : C} (p : KuuF36ShapePath x y)
    (q : KuuF36ShapePath y z) :
    (p.append q).toNative = p.toNative.append q.toNative := by
  induction q with
  | nil => rfl
  | snoc q f ih =>
      change KuuNativePath.snoc (p.append q).toNative f =
        KuuNativePath.snoc (p.toNative.append q.toNative) f
      rw [ih]

/-- Exactly the frozen F40 Grid.Blocks TWO-CONSTRUCTOR SHAPE over
the independently defined F36 paths. Each snoc stores a WHOLE path. -/
inductive KuuF40ShapeBlocks : C → C → Type (max u v) where
  | empty (x : C) : KuuF40ShapeBlocks x x
  | snoc {x y z : C} (p : KuuF40ShapeBlocks x y)
      (q : KuuF36ShapePath y z) : KuuF40ShapeBlocks x z

def KuuF40ShapeBlocks.toNative :
    ∀ {x y : C}, KuuF40ShapeBlocks x y → KuuNativeBlocks x y
  | _, _, .empty x => .empty x
  | _, _, .snoc p q => .snoc p.toNative q.toNative

def KuuF40ShapeBlocks.ofNative :
    ∀ {x y : C}, KuuNativeBlocks x y → KuuF40ShapeBlocks x y
  | _, _, .empty x => .empty x
  | _, _, .snoc p q => .snoc (ofNative p) (KuuF36ShapePath.ofNative q)

theorem KuuF40ShapeBlocks.toNative_ofNative
    {x y : C} (p : KuuNativeBlocks x y) :
    (KuuF40ShapeBlocks.ofNative p).toNative = p := by
  induction p with
  | empty => rfl
  | snoc p q ih =>
      change KuuNativeBlocks.snoc
        (KuuF40ShapeBlocks.ofNative p).toNative
        (KuuF36ShapePath.ofNative q).toNative = .snoc p q
      rw [ih, KuuF36ShapePath.toNative_ofNative]

theorem KuuF40ShapeBlocks.ofNative_toNative
    {x y : C} (p : KuuF40ShapeBlocks x y) :
    KuuF40ShapeBlocks.ofNative p.toNative = p := by
  induction p with
  | empty => rfl
  | snoc p q ih =>
      change KuuF40ShapeBlocks.snoc
        (KuuF40ShapeBlocks.ofNative p.toNative)
        (KuuF36ShapePath.ofNative q.toNative) = .snoc p q
      rw [ih, KuuF36ShapePath.ofNative_toNative]

/-- Retains ALL original-shaped categorical Hom arrows, EVERY
intermediate C object and ALL F40 segmentation boundaries. -/
def kuuF40ShapeBlocksEquiv {x y : C} :
    KuuF40ShapeBlocks x y ≃ KuuNativeBlocks x y where
  toFun := KuuF40ShapeBlocks.toNative
  invFun := KuuF40ShapeBlocks.ofNative
  left_inv := KuuF40ShapeBlocks.ofNative_toNative
  right_inv := KuuF40ShapeBlocks.toNative_ofNative

def KuuF40ShapeBlocks.flatten :
    ∀ {x y : C}, KuuF40ShapeBlocks x y → KuuF36ShapePath x y
  | _, _, .empty x => .nil x
  | _, _, .snoc p q => p.flatten.append q

def KuuF40ShapeBlocks.blockCount {x y : C} :
    KuuF40ShapeBlocks x y → Nat
  | .empty _ => 0
  | .snoc p _ => p.blockCount + 1

def KuuF40ShapeBlocks.composite :
    ∀ {x y : C}, KuuF40ShapeBlocks x y → (x ⟶ y)
  | _, _, .empty x => 𝟙 x
  | _, _, .snoc p q => p.composite ≫ q.composite

def KuuF40ShapeBlocks.append {x y z : C}
    (p : KuuF40ShapeBlocks x y) :
    KuuF40ShapeBlocks y z → KuuF40ShapeBlocks x z
  | .empty _ => p
  | .snoc q s => .snoc (p.append q) s

theorem KuuF40ShapeBlocks.toNative_blockCount
    {x y : C} (p : KuuF40ShapeBlocks x y) :
    p.toNative.blockCount = p.blockCount := by
  induction p with
  | empty => rfl
  | snoc p q ih =>
      change p.toNative.blockCount + 1 = p.blockCount + 1
      rw [ih]

theorem KuuF40ShapeBlocks.toNative_flatten
    {x y : C} (p : KuuF40ShapeBlocks x y) :
    p.flatten.toNative = p.toNative.flatten := by
  induction p with
  | empty => rfl
  | snoc p q ih =>
      change (p.flatten.append q).toNative =
        p.toNative.flatten.append q.toNative
      rw [KuuF36ShapePath.toNative_append, ih]

theorem KuuF40ShapeBlocks.toNative_composite
    {x y : C} (p : KuuF40ShapeBlocks x y) :
    p.toNative.composite = p.composite := by
  induction p with
  | empty => rfl
  | snoc p q ih =>
      change p.toNative.composite ≫ q.toNative.composite =
        p.composite ≫ q.composite
      rw [ih, KuuF36ShapePath.toNative_composite]

theorem KuuF40ShapeBlocks.toNative_append
    {x y z : C} (p : KuuF40ShapeBlocks x y)
    (q : KuuF40ShapeBlocks y z) :
    (p.append q).toNative = p.toNative.append q.toNative := by
  induction q with
  | empty => rfl
  | snoc q s ih =>
      change KuuNativeBlocks.snoc (p.append q).toNative s.toNative =
        KuuNativeBlocks.snoc (p.toNative.append q.toNative) s.toNative
      rw [ih]

/-- The HISTORICAL-shaped F40 raw block boundary is NEVER silently
flattened away. Even a block containing an empty path remains data. -/
def KuuF40ShapeBlocks.oneBlock {x y : C}
    (p : KuuF36ShapePath x y) : KuuF40ShapeBlocks x y :=
  .snoc (.empty x) p

def KuuF40ShapeBlocks.prependEmpty {x y : C}
    (p : KuuF36ShapePath x y) : KuuF40ShapeBlocks x y :=
  .snoc (.snoc (.empty x) (.nil x)) p

theorem KuuF40ShapeBlocks.oneBlock_ne_prependEmpty
    {x y : C} (p : KuuF36ShapePath x y) :
    KuuF40ShapeBlocks.oneBlock p ≠
      KuuF40ShapeBlocks.prependEmpty p := by
  intro h
  have hc := congrArg KuuF40ShapeBlocks.blockCount h
  change (1 : Nat) = 2 at hc
  exact (by decide : (1 : Nat) ≠ 2) hc

theorem KuuF40ShapeBlocks.oneBlock_flatten_eq_prependEmpty
    {x y : C} (p : KuuF36ShapePath x y) :
    (KuuF40ShapeBlocks.oneBlock p).flatten =
      (KuuF40ShapeBlocks.prependEmpty p).flatten := by
  apply (kuuF36ShapePathEquiv (C := C)).injective
  change (KuuF40ShapeBlocks.oneBlock p).flatten.toNative =
    (KuuF40ShapeBlocks.prependEmpty p).flatten.toNative
  rw [KuuF40ShapeBlocks.toNative_flatten,
    KuuF40ShapeBlocks.toNative_flatten]
  simpa only [KuuF40ShapeBlocks.oneBlock, KuuF40ShapeBlocks.prependEmpty,
    KuuF40ShapeBlocks.toNative,
    KuuNativeBlocks.singleton, KuuNativeBlocks.withEmptyPrefix] using
      (KuuNativeBlocks.singleton_flatten_eq_emptyPrefix p.toNative)

#print axioms kuuF36ShapePathEquiv
#print axioms KuuF36ShapePath.toNative_composite
#print axioms KuuF36ShapePath.toNative_length
#print axioms KuuF36ShapePath.toNative_append
#print axioms kuuF40ShapeBlocksEquiv
#print axioms KuuF40ShapeBlocks.toNative_blockCount
#print axioms KuuF40ShapeBlocks.toNative_flatten
#print axioms KuuF40ShapeBlocks.toNative_composite
#print axioms KuuF40ShapeBlocks.toNative_append
#print axioms KuuF40ShapeBlocks.oneBlock_ne_prependEmpty
#print axioms KuuF40ShapeBlocks.oneBlock_flatten_eq_prependEmpty
end
end Kuu.F112.Physical
