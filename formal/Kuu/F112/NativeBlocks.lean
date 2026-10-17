import Kuu.F112.PolygonDepthTraceCells

/-!
# F112-E7I / independent categorical native paths and true block subdivisions

The historical F40/F54 Blocks grammar does NOT mean a list of C60
sector names: a Block is a *finite sequence of independently chosen
finite native categorical paths*, each typed by actual source and
target objects. F54 subsequently carries two independent such axes.

We reconstruct precisely that TWO-LEVEL combinatorial shape, but in
a NEW, generally category-polymorphic Kuu source. This implementation
retains every native arrow and every partition boundary; its map to
a flattened categorical path is defined and verified, not equated
with the raw source.

This file does not import historical KUOS, Gray, F51 or F77, or claim
an equivalence with the frozen F19/F28 Blocks/AxisTrace definitions.
The next file specializes this structure to the true C60 Site
incidence category and its 5/6 physical polygon-sector witnesses.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
noncomputable section

universe u v
variable {C : Type u} [Category.{v} C]

/-- An original-shaped typed finite native category path, with its
actual arrows retained at every step (unlike one composite Hom). -/
inductive KuuNativePath : C → C → Type (max u v) where
  | nil (x : C) : KuuNativePath x x
  | snoc {x y z : C} (p : KuuNativePath x y)
      (f : y ⟶ z) : KuuNativePath x z

/-- Original-shaped subdivision carrier: a finite sequence of
NATIVE PATHS, not merely a finite word of arrow count labels. -/
inductive KuuNativeBlocks : C → C → Type (max u v) where
  | empty (x : C) : KuuNativeBlocks x x
  | snoc {x y z : C} (p : KuuNativeBlocks x y)
      (q : KuuNativePath y z) : KuuNativeBlocks x z

/-- One original typed category arrow, as a genuine one-step path. -/
def KuuNativePath.single {x y : C} (f : x ⟶ y) :
    KuuNativePath x y :=
  .snoc (.nil x) f

/-- Source path concatenation preserves the original nested
proof terms and concatenates on the RIGHT typed endpoint. -/
def KuuNativePath.append {x y z : C}
    (p : KuuNativePath x y) : KuuNativePath y z → KuuNativePath x z
  | .nil _ => p
  | .snoc q f => .snoc (p.append q) f

/-- Number of actual native arrows, not number of grouped blocks. -/
def KuuNativePath.length {x y : C} : KuuNativePath x y → Nat
  | .nil _ => 0
  | .snoc p _ => p.length + 1

theorem KuuNativePath.length_append {x y z : C}
    (p : KuuNativePath x y) (q : KuuNativePath y z) :
    (p.append q).length = p.length + q.length := by
  induction q with
  | nil =>
      rfl
  | snoc q f ih =>
      change (p.append q).length + 1 = p.length + (q.length + 1)
      simpa only [Nat.add_succ] using congrArg Nat.succ ih

/-- Typed native category composite, independently of the uncollapsed
source path tree (which retains each individual original arrow). -/
def KuuNativePath.composite :
    ∀ {x y : C}, KuuNativePath x y → (x ⟶ y)
  | _, _, .nil x => 𝟙 x
  | _, _, .snoc p f => p.composite ≫ f

theorem KuuNativePath.composite_append {x y z : C}
    (p : KuuNativePath x y) (q : KuuNativePath y z) :
    (p.append q).composite = p.composite ≫ q.composite := by
  induction q with
  | nil =>
      simp only [KuuNativePath.append, KuuNativePath.composite,
        Category.comp_id]
  | snoc q f ih =>
      simp only [KuuNativePath.append, KuuNativePath.composite]
      rw [ih, Category.assoc]

theorem KuuNativePath.append_assoc {w x y z : C}
    (p : KuuNativePath w x) (q : KuuNativePath x y)
    (r : KuuNativePath y z) :
    (p.append q).append r = p.append (q.append r) := by
  induction r with
  | nil =>
      rfl
  | snoc r f ih =>
      change KuuNativePath.snoc ((p.append q).append r) f =
        KuuNativePath.snoc (p.append (q.append r)) f
      rw [ih]

/-- The uncollapsed number of partition blocks, including empty
native paths which are genuine original syntactic partition data. -/
def KuuNativeBlocks.blockCount {x y : C} :
    KuuNativeBlocks x y → Nat
  | .empty _ => 0
  | .snoc p _ => p.blockCount + 1

/-- Native categorical concatenation of subdivided block sequences. -/
def KuuNativeBlocks.append {x y z : C}
    (p : KuuNativeBlocks x y) :
    KuuNativeBlocks y z → KuuNativeBlocks x z
  | .empty _ => p
  | .snoc q r => .snoc (p.append q) r

/-- Crucially, the flattening only forgets subdivision boundaries,
retaining the original ORDER of every native categorical arrow. -/
def KuuNativeBlocks.flatten :
    ∀ {x y : C}, KuuNativeBlocks x y → KuuNativePath x y
  | _, _, .empty x => .nil x
  | _, _, .snoc p q => p.flatten.append q

/-- Evaluate the original independent native blocks in the
underlying category without collapsing their source syntax. -/
def KuuNativeBlocks.composite :
    ∀ {x y : C}, KuuNativeBlocks x y → (x ⟶ y)
  | _, _, .empty x => 𝟙 x
  | _, _, .snoc p q => p.composite ≫ q.composite

/-- Original F40-shaped law: evaluation of a block subdivision is
EXACTLY evaluation of the ordered flattened categorical path. -/
theorem KuuNativeBlocks.composite_eq_flatten {x y : C}
    (p : KuuNativeBlocks x y) :
    p.composite = p.flatten.composite := by
  induction p with
  | empty =>
      simp only [KuuNativeBlocks.composite,
        KuuNativeBlocks.flatten, KuuNativePath.composite]
  | snoc p q ih =>
      calc
        (KuuNativeBlocks.snoc p q).composite =
            p.composite ≫ q.composite := rfl
        _ = p.flatten.composite ≫ q.composite := by rw [ih]
        _ = (p.flatten.append q).composite :=
          (KuuNativePath.composite_append _ _).symm
        _ = (KuuNativeBlocks.snoc p q).flatten.composite := rfl

/-- The precise original-shaped F40 associativity holds on raw
block terms, not merely after category evaluation or a quotient. -/
theorem KuuNativeBlocks.append_assoc {w x y z : C}
    (p : KuuNativeBlocks w x) (q : KuuNativeBlocks x y)
    (r : KuuNativeBlocks y z) :
    (p.append q).append r = p.append (q.append r) := by
  induction r with
  | empty =>
      rfl
  | snoc r s ih =>
      change KuuNativeBlocks.snoc ((p.append q).append r) s =
        KuuNativeBlocks.snoc (p.append (q.append r)) s
      rw [ih]

/-- Independent block partition erasure commutes with arbitrary
native block sequence concatenation, not just two chosen examples. -/
theorem KuuNativeBlocks.flatten_append {x y z : C}
    (p : KuuNativeBlocks x y) (q : KuuNativeBlocks y z) :
    (p.append q).flatten = p.flatten.append q.flatten := by
  induction q with
  | empty =>
      simp only [KuuNativeBlocks.append, KuuNativeBlocks.flatten,
        KuuNativePath.append]
  | snoc q r ih =>
      calc
        (p.append (KuuNativeBlocks.snoc q r)).flatten =
            (p.append q).flatten.append r := rfl
        _ = (p.flatten.append q.flatten).append r :=
          congrArg (fun z => z.append r) ih
        _ = p.flatten.append (q.flatten.append r) :=
          KuuNativePath.append_assoc _ _ _
        _ = p.flatten.append
            (KuuNativeBlocks.snoc q r).flatten := rfl

/-- One actual proof-carrying native path as an independently chosen
block, retaining the block separator even if that path is empty. -/
def KuuNativeBlocks.singleton {x y : C} (p : KuuNativePath x y) :
    KuuNativeBlocks x y :=
  .snoc (.empty x) p

theorem KuuNativeBlocks.singleton_count {x y : C}
    (p : KuuNativePath x y) :
    (KuuNativeBlocks.singleton p).blockCount = 1 := rfl

/-- A SOURCE partition with one nonempty block differs from that
same partition preceded by an independent EMPTY block. This
proof relevance survives even when flattened arrows agree. -/
def KuuNativeBlocks.withEmptyPrefix {x y : C}
    (p : KuuNativePath x y) : KuuNativeBlocks x y :=
  .snoc (.snoc (.empty x) (.nil x)) p

theorem KuuNativeBlocks.singleton_ne_emptyPrefix {x y : C}
    (p : KuuNativePath x y) :
    KuuNativeBlocks.singleton p ≠
      KuuNativeBlocks.withEmptyPrefix p := by
  intro h
  have hc := congrArg KuuNativeBlocks.blockCount h
  change (1 : Nat) = 2 at hc
  exact (by decide : (1 : Nat) ≠ 2) hc

/-- Two truly different block partitions flatten to the EXACT
same underlying original finite arrow word: forgetfulness is real,
and must not be mistaken for full original source faithfulness. -/
theorem KuuNativeBlocks.singleton_flatten_eq_emptyPrefix {x y : C}
    (p : KuuNativePath x y) :
    (KuuNativeBlocks.singleton p).flatten =
      (KuuNativeBlocks.withEmptyPrefix p).flatten := by
  change (KuuNativePath.nil x).append p =
    ((KuuNativePath.nil x).append (KuuNativePath.nil x)).append p
  rfl

#print axioms KuuNativePath.length_append
#print axioms KuuNativePath.composite_append
#print axioms KuuNativePath.append_assoc
#print axioms KuuNativeBlocks.composite_eq_flatten
#print axioms KuuNativeBlocks.append_assoc
#print axioms KuuNativeBlocks.flatten_append
#print axioms KuuNativeBlocks.singleton_ne_emptyPrefix
#print axioms KuuNativeBlocks.singleton_flatten_eq_emptyPrefix
end
end Kuu.F112.Physical
