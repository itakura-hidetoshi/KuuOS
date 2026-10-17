import Kuu.F112.PolygonNativeF45PropTraceComparison

/-!
# F112-E7Q5-C — positive typed F36/F40/F41 comparison along actual functors

Historical frozen source inspection (read only):
* F36 Chain.Path: nil / snoc of actual categorical Hom, append, composite.
* F40 Blocks: empty / snoc of whole typed Chain.Path, flatten and composite.
* F40 mapBlocks: constructor-recursive mapping along a genuine functor.
* F42 OneStep: Prop-valued split / insertNil / whisker;
  historical F45 AxisTrace is Type-valued with such Prop-valued steps.

This new independent theorem carrier constructs the POSITIVE functorial
part of the historical-shape comparison for EVERY ordinary functor C ⥤ D.
In particular it transports the ENTIRE original native finite arrow
word, every intermediate block boundary, all three refinement
constructors and arbitrary exact-depth histories, rather than only
their evaluated morphisms or integer counts.

We prove path/Blocks append, flatten, counts and categorical composition
compatibility, and compatibility between native Type-valued histories
and the previously constructed old-shaped Prop-step trace erasure.

The historical old KUOS.Chain.Path/Blocks themselves are intentionally
NOT imported: no actual source equivalence or F55 braided compatibility
is asserted without an independently typed old/new categorical bridge.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
noncomputable section

universe uC vC uD vD
variable {C : Type uC} [Category.{vC} C]
variable {D : Type uD} [Category.{vD} D]

/-- Constructor-preserving typed image of every actual native arrow,
with exact intermediate functor-mapped category objects. -/
def KuuNativePath.map (H : C ⥤ D) :
    ∀ {x y : C}, KuuNativePath x y →
      KuuNativePath (H.obj x) (H.obj y)
  | _, _, .nil x => .nil (H.obj x)
  | _, _, .snoc p f => .snoc (p.map H) (H.map f)

/-- Arrow count survives an arbitrary functor without a quotient. -/
theorem KuuNativePath.length_map (H : C ⥤ D)
    {x y : C} (p : KuuNativePath x y) :
    (p.map H).length = p.length := by
  induction p with
  | nil x => rfl
  | snoc p f ih =>
      change (p.map H).length + 1 = p.length + 1
      rw [ih]

/-- Constructor-wise strict concatenation compatibility, BEFORE
any categorical composite or equality quotient is taken. -/
theorem KuuNativePath.map_append (H : C ⥤ D)
    {x y z : C} (p : KuuNativePath x y)
    (q : KuuNativePath y z) :
    (p.append q).map H = (p.map H).append (q.map H) := by
  induction q with
  | nil y => rfl
  | snoc q f ih =>
      change KuuNativePath.snoc ((p.append q).map H) (H.map f) =
        KuuNativePath.snoc ((p.map H).append (q.map H)) (H.map f)
      rw [ih]

/-- Genuine categorical evaluation of the WHOLE typed path maps
naturally for every source/target category and every functor. -/
theorem KuuNativePath.composite_map (H : C ⥤ D)
    {x y : C} (p : KuuNativePath x y) :
    (p.map H).composite = H.map p.composite := by
  induction p with
  | nil x =>
      change (𝟙 (H.obj x)) = H.map (𝟙 x)
      exact (H.map_id x).symm
  | snoc p f ih =>
      change (p.map H).composite ≫ H.map f =
        H.map (p.composite ≫ f)
      rw [ih, H.map_comp]

/-- F40 block-wise path functoriality: do not erase a single
partition boundary or merge adjacent source paths. -/
def KuuNativeBlocks.map (H : C ⥤ D) :
    ∀ {x y : C}, KuuNativeBlocks x y →
      KuuNativeBlocks (H.obj x) (H.obj y)
  | _, _, .empty x => .empty (H.obj x)
  | _, _, .snoc p q => .snoc (p.map H) (q.map H)

/-- Unlike flattening, the fully typed functor map also conserves
the exact number of independently chosen original source blocks. -/
theorem KuuNativeBlocks.blockCount_map (H : C ⥤ D)
    {x y : C} (p : KuuNativeBlocks x y) :
    (p.map H).blockCount = p.blockCount := by
  induction p with
  | empty x => rfl
  | snoc p q ih =>
      change (p.map H).blockCount + 1 = p.blockCount + 1
      rw [ih]

/-- The positive F40 comparison strictly preserves *both* the
original source block boundaries and their ordered concatenation. -/
theorem KuuNativeBlocks.map_append (H : C ⥤ D)
    {x y z : C} (p : KuuNativeBlocks x y)
    (q : KuuNativeBlocks y z) :
    (p.append q).map H = (p.map H).append (q.map H) := by
  induction q with
  | empty y => rfl
  | snoc q r ih =>
      change KuuNativeBlocks.snoc ((p.append q).map H) (r.map H) =
        KuuNativeBlocks.snoc ((p.map H).append (q.map H)) (r.map H)
      rw [ih]

/-- The F36/F40 core square COMMUTES at the raw finite-path level:
map every block THEN flatten = flatten THEN map every path arrow. -/
theorem KuuNativeBlocks.flatten_map (H : C ⥤ D)
    {x y : C} (p : KuuNativeBlocks x y) :
    (p.map H).flatten = p.flatten.map H := by
  induction p with
  | empty x => rfl
  | snoc p q ih =>
      change (p.map H).flatten.append (q.map H) =
        (p.flatten.append q).map H
      rw [ih, KuuNativePath.map_append]

/-- This second square COMMUTES at the actual original categorical
Hom level, including identity and non-strict associative composition. -/
theorem KuuNativeBlocks.composite_map (H : C ⥤ D)
    {x y : C} (p : KuuNativeBlocks x y) :
    (p.map H).composite = H.map p.composite := by
  calc
    (p.map H).composite = (p.map H).flatten.composite :=
      KuuNativeBlocks.composite_eq_flatten _
    _ = (p.flatten.map H).composite :=
      congrArg KuuNativePath.composite (KuuNativeBlocks.flatten_map H p)
    _ = H.map p.flatten.composite :=
      KuuNativePath.composite_map H p.flatten
    _ = H.map p.composite := by
      rw [KuuNativeBlocks.composite_eq_flatten p]

/-- Even if the source has two distinct block presentations,
equality of categorical composites is preserved under the
explicit type-faithful forward functor map. -/
theorem KuuNativeBlocks.map_composite_eq (H : C ⥤ D)
    {x y : C} (p q : KuuNativeBlocks x y)
    (h : p.composite = q.composite) :
    (p.map H).composite = (q.map H).composite := by
  rw [KuuNativeBlocks.composite_map, KuuNativeBlocks.composite_map, h]

/-- Each of the THREE exact F41 primitive proof constructors is
mapped forward through actual category functoriality, without
fabricating a step from equal composites. -/
def KuuNativeOneStep.map (H : C ⥤ D)
    {x y : C} {p q : KuuNativeBlocks x y}
    (h : KuuNativeOneStep p q) :
    KuuNativeOneStep (p.map H) (q.map H) := by
  induction h with
  | split p q r =>
      simpa only [KuuNativeBlocks.map, KuuNativePath.map_append]
        using (KuuNativeOneStep.split (p.map H) (q.map H) (r.map H))
  | insertNil p =>
      exact .insertNil (p.map H)
  | whisker h t ih =>
      exact .whisker ih (t.map H)

/-- Exact-Nat-depth native histories transport along the SAME
functor without changing their full typed intermediate Blocks. -/
def KuuNativeAxisTrace.map (H : C ⥤ D)
    {x y : C} {n : Nat}
    {p q : KuuNativeBlocks x y}
    (h : KuuNativeAxisTrace n p q) :
    KuuNativeAxisTrace n (p.map H) (q.map H) := by
  induction h with
  | refl p => exact .refl _
  | snoc h step ih =>
      exact .snoc ih (step.map H)

/-- The Type-valued old-shaped carrier with PROP primitive fields
also maps forward; use proof elimination ONLY inside its Prop field,
not to invent a Type-valued native source step. -/
def KuuNativePropAxisTrace.map (H : C ⥤ D)
    {x y : C} {n : Nat}
    {p q : KuuNativeBlocks x y}
    (h : KuuNativePropAxisTrace n p q) :
    KuuNativePropAxisTrace n (p.map H) (q.map H) := by
  induction h with
  | refl p => exact .refl _
  | snoc h step ih =>
      refine .snoc ih ?_
      rcases step with ⟨raw⟩
      exact ⟨raw.map H⟩

/-- The positive functor transport respects the LOSS OF primitive
step proof evidence established in E7Q5-B: the following square
commutes while its erasure arrow remains genuinely noninjective. -/
theorem KuuNativeAxisTrace.map_eraseStepEvidence (H : C ⥤ D)
    {x y : C} {n : Nat}
    {p q : KuuNativeBlocks x y}
    (h : KuuNativeAxisTrace n p q) :
    (h.map H).eraseStepEvidence =
      (h.eraseStepEvidence).map H := by
  induction h with
  | refl p => rfl
  | snoc h step ih =>
      change KuuNativePropAxisTrace.snoc
          ((h.map H).eraseStepEvidence) _ =
        KuuNativePropAxisTrace.snoc
          ((h.eraseStepEvidence).map H) _
      rw [ih]

/-- The positive comparison has an actual C60 instance with all
north-pentagon Site arrows and both original source Blocks intact. -/
theorem northPentagonNativeF40_functor_composite
    (H : Site ⥤ D) :
    (northPentagonNativeDualAxisFrame.firstAxis.map H).composite =
      H.map northPentagonNativeDualAxisFrame.firstAxis.composite :=
  KuuNativeBlocks.composite_map H _

#print axioms KuuNativePath.map
#print axioms KuuNativePath.length_map
#print axioms KuuNativePath.map_append
#print axioms KuuNativePath.composite_map
#print axioms KuuNativeBlocks.map
#print axioms KuuNativeBlocks.blockCount_map
#print axioms KuuNativeBlocks.map_append
#print axioms KuuNativeBlocks.flatten_map
#print axioms KuuNativeBlocks.composite_map
#print axioms KuuNativeBlocks.map_composite_eq
#print axioms KuuNativeOneStep.map
#print axioms KuuNativeAxisTrace.map
#print axioms KuuNativePropAxisTrace.map
#print axioms KuuNativeAxisTrace.map_eraseStepEvidence
#print axioms northPentagonNativeF40_functor_composite

end
end Kuu.F112.Physical
