import KUOS.DependentOriginationCoherentBiadjunctionActualLiftDoubleBracketedHexagonV5_136

namespace KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionFiniteHorizontalExchangeV5_133

set_option autoImplicit false
noncomputable section

/-!
# F40-A/v5.137: arbitrarily many NATIVE finite-path subdivision blocks

A Blocks x y is a genuinely typed finite sequence of independently
chosen finite CATEGORY paths, not a sequence of F26 comparison chains.
Each block can contain zero or arbitrarily many arrows. Concatenating
the blocks reconstructs an actual F36 native Chain.Path, and its
evaluation is the original CATEGORY composition (with its actual
associativity and identity). The F38 functorial path transport extends
to these arbitrarily long block segmentations.

These are axes of a rectangular diagram, NOT an arbitrary grid
of higher 2-cells. No unquotiented compression faithfulness is claimed.
-/

namespace Grid

universe u v uE vE
variable {D : Type u} [Category.{v} D]

/-- A finite sequence of finite paths: arbitrary finite blocks of
native categorical arrows. It represents a subdivided diagram axis. -/
inductive Blocks : D → D → Type (max u v) where
  | empty (x : D) : Blocks x x
  | snoc {x y z : D} (p : Blocks x y)
      (q : Chain.Path y z) : Blocks x z

/-- Forget the partition boundaries, retaining the exact ordered
native categorical arrows in the F36 finite-path carrier. -/
def Blocks.flatten : ∀ {x y : D}, Blocks x y → Chain.Path x y
  | _, _, .empty x => Chain.Path.nil x
  | _, _, .snoc p q => (flatten p).append q

/-- Evaluate block-by-block, using the original nonstrict categorical
composition rather than silently choosing a strict model. -/
def Blocks.composite : ∀ {x y : D}, Blocks x y → (x ⟶ y)
  | _, _, .empty x => 𝟙 x
  | _, _, .snoc p q => p.composite ≫ q.composite

/-- Arbitrary concatenation of two already subdivided native paths. -/
def Blocks.append {x y z : D} (p : Blocks x y) :
    Blocks y z → Blocks x z
  | .empty _ => p
  | .snoc q r => .snoc (p.append q) r

/-- Evaluation agrees with flattening all subdivision boundaries,
by structural induction on the number of independent blocks. -/
theorem Blocks.composite_eq_flatten {x y : D} (p : Blocks x y) :
    p.composite = p.flatten.composite := by
  induction p with
  | empty =>
      simp only [Blocks.composite, Blocks.flatten, Chain.Path.composite]
  | snoc p q ih =>
      simp only [Blocks.composite, Blocks.flatten,
        Chain.Path.composite_append, ih]

/-- Flattening a concatenation retains exactly the ordered arrows,
even for arbitrary empty blocks or nested subdivisions. -/
theorem Blocks.flatten_append {x y z : D}
    (p : Blocks x y) (q : Blocks y z) :
    (p.append q).flatten = p.flatten.append q.flatten := by
  induction q with
  | empty =>
      simp only [Blocks.append, Blocks.flatten, Chain.Path.append]
  | snoc q r ih =>
      simpa only [Blocks.append, Blocks.flatten, ih] using
        (Chain.Path.append_assoc p.flatten q.flatten r)

/-- Evaluation of an arbitrarily long sequence of blocks respects any
split point, not merely the two original F39 finite paths. -/
theorem Blocks.composite_append {x y z : D}
    (p : Blocks x y) (q : Blocks y z) :
    (p.append q).composite = p.composite ≫ q.composite := by
  calc
    (p.append q).composite =
        (p.append q).flatten.composite :=
      Blocks.composite_eq_flatten (p.append q)
    _ = (p.flatten.append q.flatten).composite :=
      congrArg Chain.Path.composite (Blocks.flatten_append p q)
    _ = p.flatten.composite ≫ q.flatten.composite :=
      Chain.Path.composite_append p.flatten q.flatten
    _ = p.composite ≫ q.composite := by
      rw [← Blocks.composite_eq_flatten p,
        ← Blocks.composite_eq_flatten q]

/-- Finite block concatenation obeys a genuine categorical associativity
at the native carrier level; no arbitrary bracketing remains. -/
theorem Blocks.append_assoc {a b c d : D}
    (p : Blocks a b) (q : Blocks b c) (r : Blocks c d) :
    (p.append q).append r = p.append (q.append r) := by
  induction r with
  | empty => rfl
  | snoc r s ih =>
      simp only [Blocks.append, ih]

/-- Map EVERY native arrow inside EVERY finite block through a genuine
ordinary category functor, with the exact original intermediate objs. -/
def mapBlocks {E : Type uE} [Category.{vE} E]
    (H : D ⥤ E) : ∀ {x y : D},
      Blocks x y → Blocks (H.obj x) (H.obj y)
  | _, _, .empty x => Blocks.empty (H.obj x)
  | _, _, .snoc p q =>
      Blocks.snoc (mapBlocks H p)
        (KUOS.DependentOriginationCoherentBiadjunctionFiniteModificationMatePathsV5_135.Finite.mapPath
          H q)

/-- Mapping blocks and then discarding subdivisions is EXACTLY
mapping the original flattened arrow path, as dependent paths. -/
theorem mapBlocks_flatten {E : Type uE} [Category.{vE} E]
    (H : D ⥤ E) {x y : D} (p : Blocks x y) :
    (mapBlocks H p).flatten =
      KUOS.DependentOriginationCoherentBiadjunctionFiniteModificationMatePathsV5_135.Finite.mapPath
        H p.flatten := by
  induction p with
  | empty =>
      simp only [mapBlocks, Blocks.flatten,
        KUOS.DependentOriginationCoherentBiadjunctionFiniteModificationMatePathsV5_135.Finite.mapPath]
  | snoc p q ih =>
      simp only [mapBlocks, Blocks.flatten,
        KUOS.DependentOriginationCoherentBiadjunctionFiniteModificationMatePathsV5_135.Finite.mapPath_append,
        ih]

/-- The functor sends the fully evaluated block path to the
evaluation of its entire transported subdivision, including units. -/
theorem mapBlocks_composite {E : Type uE} [Category.{vE} E]
    (H : D ⥤ E) {x y : D} (p : Blocks x y) :
    (mapBlocks H p).composite = H.map p.composite := by
  calc
    (mapBlocks H p).composite = (mapBlocks H p).flatten.composite :=
      Blocks.composite_eq_flatten (mapBlocks H p)
    _ = (KUOS.DependentOriginationCoherentBiadjunctionFiniteModificationMatePathsV5_135.Finite.mapPath
        H p.flatten).composite :=
      congrArg Chain.Path.composite (mapBlocks_flatten H p)
    _ = H.map p.flatten.composite :=
      KUOS.DependentOriginationCoherentBiadjunctionFiniteModificationMatePathsV5_135.Finite.mapPath_composite
        H p.flatten
    _ = H.map p.composite := by rw [← Blocks.composite_eq_flatten p]

/-- Any two DIFFERENT block segmentations may have distinct numbers of
blocks and different carrier shapes. If their resulting genuine morphism
is the same, the mapped results are equal, without assuming their
flattened finite paths are definitionally identical. -/
theorem mapBlocks_independent {E : Type uE} [Category.{vE} E]
    (H : D ⥤ E) {x y : D}
    (p q : Blocks x y) (h : p.composite = q.composite) :
    (mapBlocks H p).composite = (mapBlocks H q).composite := by
  rw [mapBlocks_composite, mapBlocks_composite, h]

#print axioms Blocks
#print axioms Blocks.flatten
#print axioms Blocks.composite
#print axioms Blocks.append
#print axioms Blocks.composite_eq_flatten
#print axioms Blocks.flatten_append
#print axioms Blocks.composite_append
#print axioms Blocks.append_assoc
#print axioms mapBlocks
#print axioms mapBlocks_flatten
#print axioms mapBlocks_composite
#print axioms mapBlocks_independent

end Grid

end

end KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137
