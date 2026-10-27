import Kuu.F112.PolygonNativeC60StrictContextTreePasting
import Kuu.F112.PolygonNativeC60TypedDiamondGeometricCoherence
import Kuu.F112.PolygonNativeC60PhysicalParallelBoundaryNoGo

/-!
# F112-P94D3DP — exact geometric filling gate for genuine C60 strict context trees

DO proves strict transport coherence for arbitrary finite binary trees of
independently ordered C60 AQ contexts. DP makes the AUTHORITY BOUNDARY
explicit: equality of those original strict group maps does NOT produce
a Type-valued 16D geometric comparison between arbitrary 15D objects.

This module connects the independently constructed DO context trees to
the already proved CE/CF exact free-word geometric-relation criterion:
a proposed parallel geometric coherence relation on ORIGINAL raw16D
paths respects all binary AQ context trees iff it respects the complete
noncommutative BV free holonomy of the original proof certificates. By
CE this is equivalent to already holding in the selected no-extra-relations
strict quotient and to factorization of the complete free receiver.

The criterion is constructive on the positive side: CF structural
cancellation/zigzag triangle relations satisfy it for every tree.
It is sharply obstructed on a real dependent positive diamond with
distinct ORIGINAL 15D midpoint witnesses, irrespective of context tree.
The genuine physical AU zigzag commutes STRICTLY after every tree context,
but its raw16D proof terms are unequal and its true BC primitive remains
nontrivial in the complete free receiver.

Finally, BK supplies a physical no-go at every finite AQ context: the
actual forward 15D exchange and its inverse carry different 14D source
and target histories and admit NO typed 16D comparison for ANY original
AX signature. This obstruction coexists with DO's actual full-strict
tree naturality. By contrast, the parallel AU 15D naturality witnesses
have an EXPLICITLY ADJOINED 16D bridge in the BC presentation, not an
unsourced original geometric filler.

A declared relation between two raw16D proof paths is *comparison
data* at the next coherence level; it is not itself a new original
geometric sixteen-cell. No new 16D generator or 17D filler is added.
All 14D/15D dependent boundaries, CN/BV16D certificates, 107 published
roots, old no-go, strict/independent Kuu distinction, and no-Gray
policy remain intact. No new axioms, sorry or admit.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u uD vD uE vE

/-- Interpret an EXISTING dependent raw16D path at the genuine ordered
AQ word of a context tree, in the original selected strict Kuu
presentation. Unlike DO's strict GROUP transport, this is a morphism
between genuine context-framed original 15D objects. -/
def nativeC60DPTreeStrictStep
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (tree : NativeK5DOContextTree)
    {a b : L.Total}
    (c : NativeC60AXStep (nativeC60BCClosedSignature S F) a b) :=
  nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
    (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
    (nativeC60BCMapClosedStep S F (nativeK5DOTreeWord tree) c)

/-- A separately proposed, genuinely PARALLEL geometric relation on
existing original Type-valued raw16D paths is admissible if it
respects the selected strict interpretation after EVERY FINITE binary
context tree. Relation data are an INPUT, never a newly assumed filler. -/
def NativeC60DPTreeCompatible
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (R : NativeC60AZParallelRelation (nativeC60BCClosedSignature S F)) :
    Prop :=
  ∀ (tree : NativeK5DOContextTree) {a b : L.Total}
    (c d : NativeC60AXStep (nativeC60BCClosedSignature S F) a b),
      R c d →
        nativeC60DPTreeStrictStep S F tree c =
          nativeC60DPTreeStrictStep S F tree d

/-- MAIN DP gate: ALL independently bracketed finite AQ trees respect a
proposed raw16D geometric relation iff that relation preserves the
COMPLETE ORIGINAL noncommutative free holonomy. The converse uses a
one-leaf tree carrying an arbitrary single finite AQ prefix. -/
theorem nativeC60DPTreeCompatible_iff_complete_BV
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (R : NativeC60AZParallelRelation (nativeC60BCClosedSignature S F)) :
    NativeC60DPTreeCompatible S F R ↔
      NativeC60CEGeometricCompatible S F R := by
  constructor
  · intro hc
    apply (nativeC60CECompatible_iff_all_frames S F R).mpr
    intro word a b c d hr
    simpa [nativeC60DPTreeStrictStep, nativeK5DOTreeWord,
      nativeK5DNPrefixWord] using
      (hc (.leaf [word]) c d hr)
  · intro hc tree a b c d hr
    simpa only [nativeC60DPTreeStrictStep] using
      ((nativeC60CECompatible_iff_all_frames S F R).mp hc)
        (nativeK5DOTreeWord tree) c d hr

/-- No-new-collapse rigidity: any raw16D relation compatible with EVERY
tree already holds in the original strict quotient at the UNFRAMED
source/target boundary. This does not assert a geometric filler. -/
theorem nativeC60DPTreeCompatible_iff_original_strict
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (R : NativeC60AZParallelRelation (nativeC60BCClosedSignature S F)) :
    NativeC60DPTreeCompatible S F R ↔
      ∀ {a b : L.Total}
        (c d : NativeC60AXStep (nativeC60BCClosedSignature S F) a b),
        R c d →
          nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
              (nativeC60AZNoRelations (nativeC60BCClosedSignature S F)) c =
            nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
              (nativeC60AZNoRelations (nativeC60BCClosedSignature S F)) d :=
  (nativeC60DPTreeCompatible_iff_complete_BV S F R).trans
    (nativeC60CECompatible_iff_original_strict S F R)

/-- The complete ORIGINAL free-BV receiver factors through any
proposed parallel geometric presentation exactly when the relation
survives EVERY finite, differently bracketed context tree. -/
theorem nativeC60DPTreeCompatible_iff_receiver_factor
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (R : NativeC60AZParallelRelation (nativeC60BCClosedSignature S F)) :
    NativeC60DPTreeCompatible S F R ↔
      ∃ G : NativeC60AZStrictSpace (nativeC60BCClosedSignature S F) R ⥤
          SingleObj (FreeGroup (NativeC60BVGeneratorCode S))ᵐᵒᵖ,
        nativeC60AZStrictProject (nativeC60BCClosedSignature S F) R ⋙ G =
          nativeC60AZRawHolonomy (nativeC60BCClosedSignature S F)
            (nativeC60BWFreeWeight S F) :=
  (nativeC60DPTreeCompatible_iff_complete_BV S F R).trans
    (nativeC60CECompatible_iff_holonomy_factor S F R)

/-- FULL original noncommutative free-holonomy is invariant under ANY
regrouping of the SAME chronologically ordered finite AQ context family.
No original 15D objects or 16D generator codes are erased. -/
theorem nativeC60DPTreeBW_refinement
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {left right : NativeK5DOContextTree}
    (hsteps : nativeK5DOTreeSteps left = nativeK5DOTreeSteps right)
    {a b : L.Total}
    (c : NativeC60AXStep (nativeC60BCClosedSignature S F) a b) :
    nativeC60BWFreeHolonomy S F
        (nativeC60BCMapClosedStep S F (nativeK5DOTreeWord left) c) =
      nativeC60BWFreeHolonomy S F
        (nativeC60BCMapClosedStep S F (nativeK5DOTreeWord right) c) := by
  rw [nativeK5DOTreeWord_eq_of_steps_eq hsteps]

/-- Exact genuine POSITIVE 16D diamond criterion in any binary AQ tree:
strict commutation is equivalent to equality of the TWO complete
original BV 16D generator codes IN THEIR ORIGINAL ORDER. -/
theorem nativeC60DPDiamond_tree_iff_complete_codes
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (tree : NativeK5DOContextTree) (q : NativeC60CFTypedDiamond S F) :
    nativeC60DPTreeStrictStep S F tree
        (nativeC60CFDiamondLeft S F q) =
      nativeC60DPTreeStrictStep S F tree
        (nativeC60CFDiamondRight S F q) ↔
      nativeC60BVGeneratorCode S F q.leftFirst =
        nativeC60BVGeneratorCode S F q.rightFirst ∧
      nativeC60BVGeneratorCode S F q.leftSecond =
        nativeC60BVGeneratorCode S F q.rightSecond := by
  exact nativeC60CFDiamond_strict_iff_complete_codes S F
    (nativeK5DOTreeWord tree) q

/-- The same complete BV code condition exactly characterizes
commutation of a positive dependent 16D diamond in EVERY possible
finite binary AQ context tree. No parity inference is used. -/
theorem nativeC60DPDiamond_all_trees_iff_complete_codes
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (q : NativeC60CFTypedDiamond S F) :
    (∀ tree : NativeK5DOContextTree,
      nativeC60DPTreeStrictStep S F tree
          (nativeC60CFDiamondLeft S F q) =
        nativeC60DPTreeStrictStep S F tree
          (nativeC60CFDiamondRight S F q)) ↔
      nativeC60BVGeneratorCode S F q.leftFirst =
        nativeC60BVGeneratorCode S F q.rightFirst ∧
      nativeC60BVGeneratorCode S F q.leftSecond =
        nativeC60BVGeneratorCode S F q.rightSecond := by
  constructor
  · intro hall
    exact (nativeC60DPDiamond_tree_iff_complete_codes S F (.leaf []) q).mp
      (hall (.leaf []))
  · intro hcodes tree
    exact (nativeC60DPDiamond_tree_iff_complete_codes S F tree q).mpr
      hcodes

/-- Genuine distinct 15D intermediate witnesses obstruct strict
commutation of a physical 16D positive diamond after EVERY binary
AQ tree, even when all its leaf/context regroupings are coherent. -/
theorem nativeC60DPDiamond_midpoint_no_strict_all_trees
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (q : NativeC60CFTypedDiamond S F)
    (hne : q.leftMid ≠ q.rightMid) :
    ∀ tree : NativeK5DOContextTree,
      nativeC60DPTreeStrictStep S F tree
          (nativeC60CFDiamondLeft S F q) ≠
        nativeC60DPTreeStrictStep S F tree
          (nativeC60CFDiamondRight S F q) := by
  intro tree
  exact nativeC60CFDiamond_distinct_midpoint_no_strict S F
    (nativeK5DOTreeWord tree) q hne

/-- A proposed relation identifying two positive raw16D paths with
distinct original 15D midpoints is NOT admissible for all finite
trees: the precise complete-BV obstruction survives every frame. -/
theorem nativeC60DPDiamond_distinct_no_tree_descent
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (R : NativeC60AZParallelRelation (nativeC60BCClosedSignature S F))
    (q : NativeC60CFTypedDiamond S F)
    (hne : q.leftMid ≠ q.rightMid)
    (hrel : R (nativeC60CFDiamondLeft S F q)
      (nativeC60CFDiamondRight S F q)) :
    ¬ NativeC60DPTreeCompatible S F R := by
  intro hc
  exact nativeC60CFDiamond_distinct_midpoint_no_descent S F R q hne hrel
    ((nativeC60DPTreeCompatible_iff_complete_BV S F R).mp hc)

/-- The explicitly declared CF structural triangle/cancellation
relations DO satisfy the FULL all-tree gate without silently
introducing a new original geometric comparison. -/
theorem nativeC60DPTriangle_all_trees_compatible
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L) :
    NativeC60DPTreeCompatible S F (NativeC60CFTriangleRelation S F) :=
  (nativeC60DPTreeCompatible_iff_complete_BV S F
    (NativeC60CFTriangleRelation S F)).mpr
      (nativeC60CFTriangle_compatible S F)

/-- The complete noncommutative receiver is indeed constructively
factorable through the selected structural triangles at all trees. -/
theorem nativeC60DPTriangle_all_trees_receiver
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L) :
    ∃ G : NativeC60AZStrictSpace (nativeC60BCClosedSignature S F)
        (NativeC60CFTriangleRelation S F) ⥤
        SingleObj (FreeGroup (NativeC60BVGeneratorCode S))ᵐᵒᵖ,
      nativeC60AZStrictProject (nativeC60BCClosedSignature S F)
          (NativeC60CFTriangleRelation S F) ⋙ G =
        nativeC60AZRawHolonomy (nativeC60BCClosedSignature S F)
          (nativeC60BWFreeWeight S F) :=
  (nativeC60DPTreeCompatible_iff_receiver_factor S F
    (NativeC60CFTriangleRelation S F)).mp
      (nativeC60DPTriangle_all_trees_compatible S F)

section OriginalPhysicalC60

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

/-- ACTUAL physical counterexample to interpreting DO strict coherence
as general 16D filling: the full genuine strict maps agree under
arbitrary reassociation, while NO typed 16D comparison exists between
the nonparallel forward/backward ORIGINAL 15D physical exchanges.
This quantifies over EVERY physical AX signature, not an empty one. -/
theorem nativeK5DPStrict_tree_no_automatic_sixteen
    (W : NativeK5StructuralThirteenCell p U V)
    (F14 : NativeK5FifteenFourteenFiber W)
    (inner outer : List Bool)
    {left right : NativeK5DOContextTree}
    (hsteps : nativeK5DOTreeSteps left = nativeK5DOTreeSteps right)
    (T : NativeC60AXSignature (nativeK5AXBaseLayer W)) :
    ((nativeK5DOTreeWord_eq_of_steps_eq hsteps ▸
      nativeK5DOTreeStrict W F14 outer inner left) =
        nativeK5DOTreeStrict W F14 outer inner right) ∧
    ¬ Nonempty (NativeC60AXStep T
      (nativeK5BKExchangeForward W (nativeK5DOTreeWord right))
      (nativeK5BKExchangeBackward W (nativeK5DOTreeWord right))) :=
  ⟨nativeK5DOTreeStrict_refinement W F14 inner outer hsteps,
    nativeK5BKExchange_no_sixteen_cell W (nativeK5DOTreeWord right) T⟩

/-- The POSITIVE TYPING CONTRAST at each context tree: genuine AU
parallel 15D naturality witnesses are different but have a named
16D bridge ONLY in the explicitly adjoined BC presentation. In the
same exact context, the nonparallel physical exchange has no raw
16D comparator for ANY original physical signature. -/
theorem nativeK5DPPhysical_parallel_gate
    (W : NativeK5StructuralThirteenCell p U V)
    (tree : NativeK5DOContextTree) :
    let word := nativeK5DOTreeWord tree
    let a := nativeK5BCContext W word
      (nativeK5AXPack W
        (nativeK5AUNaturalityViaSource W (nativeK5AQExchange W [])))
    let b := nativeK5BCContext W word
      (nativeK5AXPack W
        (nativeK5AUNaturalityViaTarget W (nativeK5AQExchange W [])))
    a ≠ b ∧
      Nonempty (NativeC60AXStep (nativeK5BCSignature W) a b) ∧
      (∀ T : NativeC60AXSignature (nativeK5AXBaseLayer W),
        ¬ Nonempty (NativeC60AXStep T
          (nativeK5BKExchangeForward W word)
          (nativeK5BKExchangeBackward W word))) := by
  have hp := nativeK5BKParallelNaturality_has_comparison W
    (nativeK5DOTreeWord tree)
  exact ⟨hp.1, hp.2, fun T =>
    nativeK5BKExchange_no_sixteen_cell W (nativeK5DOTreeWord tree) T⟩

/-- Genuine physical AU zigzag: at ANY finite AQ context tree the
three-step raw16D path and the single 16D primitive have EQUAL strict
Kuu images, but the ACTUAL original raw16D proof terms are UNEQUAL.
Thus strict coherence is NOT a raw-geometric reification theorem. -/
theorem nativeK5DPPhysicalAU_tree_strict_not_raw
    (W : NativeK5StructuralThirteenCell p U V)
    (tree : NativeK5DOContextTree) :
    (nativeC60AZStrictStep (nativeK5BCSignature W)
        (nativeC60AZNoRelations (nativeK5BCSignature W))
        (nativeK5BCClosedContextStep W (nativeK5DOTreeWord tree)
          (.trans
            (.trans (.atom (nativeK5CEPhysicalAUGenerator W))
              (.symm (.atom (nativeK5CEPhysicalAUGenerator W))))
            (.atom (nativeK5CEPhysicalAUGenerator W)))) =
      nativeC60AZStrictStep (nativeK5BCSignature W)
        (nativeC60AZNoRelations (nativeK5BCSignature W))
        (nativeK5BCClosedContextStep W (nativeK5DOTreeWord tree)
          (.atom (nativeK5CEPhysicalAUGenerator W)))) ∧
      ((NativeC60AXStep.trans
        (NativeC60AXStep.trans
          (NativeC60AXStep.atom (nativeK5CEPhysicalAUGenerator W))
          (NativeC60AXStep.symm
            (NativeC60AXStep.atom (nativeK5CEPhysicalAUGenerator W))))
        (NativeC60AXStep.atom (nativeK5CEPhysicalAUGenerator W))) ≠
          NativeC60AXStep.atom (nativeK5CEPhysicalAUGenerator W)) :=
  ⟨nativeK5CFPhysicalAU_zigzag_strict W (nativeK5DOTreeWord tree),
    nativeK5CFPhysicalAU_zigzag_raw_ne W⟩

/-- Even where the parallel AU bridge is adjoined, its original
primitive noncommutative BV holonomy is NONIDENTITY at every binary
context tree. Geometric compatibility does not erase evidence. -/
theorem nativeK5DPPhysicalAU_tree_primitive_nontrivial
    (W : NativeK5StructuralThirteenCell p U V)
    (tree : NativeK5DOContextTree) :
    ((nativeK5BSNaturalityFirst W).1.1 ≠
      (nativeK5BSNaturalitySecond W).1.1) ∧
      (nativeC60BWFreeHolonomy (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W)
        (nativeK5BCClosedContextStep W (nativeK5DOTreeWord tree)
          (nativeK5BSNaturality_declared_bridge W)) ≠
        (1 : FreeGroup
          (NativeC60BVGeneratorCode (nativeK5AXKuuSignature W)))) :=
  ⟨nativeK5BSNaturality_full_sources_ne W,
    nativeK5CEPhysicalAU_all_frames_nontrivial W
      (nativeK5DOTreeWord tree)⟩

end OriginalPhysicalC60

#print axioms nativeC60DPTreeStrictStep
#print axioms NativeC60DPTreeCompatible
#print axioms nativeC60DPTreeCompatible_iff_complete_BV
#print axioms nativeC60DPTreeCompatible_iff_original_strict
#print axioms nativeC60DPTreeCompatible_iff_receiver_factor
#print axioms nativeC60DPTreeBW_refinement
#print axioms nativeC60DPDiamond_tree_iff_complete_codes
#print axioms nativeC60DPDiamond_all_trees_iff_complete_codes
#print axioms nativeC60DPDiamond_midpoint_no_strict_all_trees
#print axioms nativeC60DPDiamond_distinct_no_tree_descent
#print axioms nativeC60DPTriangle_all_trees_compatible
#print axioms nativeC60DPTriangle_all_trees_receiver
#print axioms nativeK5DPStrict_tree_no_automatic_sixteen
#print axioms nativeK5DPPhysical_parallel_gate
#print axioms nativeK5DPPhysicalAU_tree_strict_not_raw
#print axioms nativeK5DPPhysicalAU_tree_primitive_nontrivial

end
end Kuu.F112.Physical
