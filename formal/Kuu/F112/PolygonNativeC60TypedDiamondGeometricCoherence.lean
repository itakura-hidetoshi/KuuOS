import Kuu.F112.PolygonNativeC60GeometricSixteenDescentObstruction

/-!
# F112-P94D3CF — genuinely typed positive 16D diamonds and AU triangle

CE gives an exact free-holonomy descent criterion for any additional
candidate geometric coherence relation in the selected Kuu strict
presentation. CF now tests ACTUAL DEPENDENT 16D PASTING PATHS:

1. A two-sided positive diamond has four INDEPENDENT genuine BC higher
   generators, with exact 15D source, target, and TWO original
   intermediate proof objects. No replacement of those with a graph
   node, scalar shadow or a priori equal intermediate object is made.
2. A diamond commutes in the original selected strict Kuu quotient
   under any finite genuine AQ context iff the two complete ordered
   generator-code pairs agree. In particular, a diamond with unequal
   original intermediate 15D witnesses CANNOT commute; if geometry
   declares it, the complete free receiver cannot descend.
3. The REAL physical AU naturality generator is subjected to three
   independently typed 16D edges (forward, backward, forward). Its
   zigzag triangle DOES commute in the original strict quotient at
   every finite physical AQ context. Nevertheless it retains the
   distinct original 15D endpoints and its single-letter holonomy is
   nonidentity. Raw syntax equality is NOT asserted.
4. Structural cancellation and zigzag triangles are encoded as an
   EXPLICIT candidate geometric relation, proved compatible with the
   noncommutative free receiver and shown to admit an actual factor
   through its declared strict quotient.

A general new geometric 16-cell filling an independent diamond has
NOT been built. Any horizontal Peiffer, P92B descent, strict 3/n,
infinity-hyperdescent or Gray reintroduction remains outside scope.
No new axioms, sorry/admit, or change to 107 public roots.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u uD vD uE vE

/-- A truly dependent 2-by-2 diamond of independently provided BC
sixteen-dimensional generator certificates. Both potential intermediate
15D proofs are explicit, not identified or merely observed. -/
structure NativeC60CFTypedDiamond {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L) where
  source : L.Total
  target : L.Total
  leftMid : L.Total
  rightMid : L.Total
  leftFirst : (nativeC60BCClosedSignature S F).Gen source leftMid
  leftSecond : (nativeC60BCClosedSignature S F).Gen leftMid target
  rightFirst : (nativeC60BCClosedSignature S F).Gen source rightMid
  rightSecond : (nativeC60BCClosedSignature S F).Gen rightMid target

/-- First raw16D path with the first original middle 15D object. -/
def nativeC60CFDiamondLeft
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (q : NativeC60CFTypedDiamond S F) :
    NativeC60AXStep (nativeC60BCClosedSignature S F) q.source q.target :=
  .trans (.atom q.leftFirst) (.atom q.leftSecond)

/-- Second raw16D path with the independent second middle 15D object. -/
def nativeC60CFDiamondRight
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (q : NativeC60CFTypedDiamond S F) :
    NativeC60AXStep (nativeC60BCClosedSignature S F) q.source q.target :=
  .trans (.atom q.rightFirst) (.atom q.rightSecond)

/-- The exact two-letter comparison criterion for a genuine positive
diamond. NO intermediate equality is assumed: it is reflected by the
entire original signed noncommutative free holonomy at any AQ context. -/
theorem nativeC60CFDiamond_strict_iff_complete_codes
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (word : List Bool) (q : NativeC60CFTypedDiamond S F) :
    nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
        (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
        (nativeC60BCMapClosedStep S F word
          (nativeC60CFDiamondLeft S F q)) =
      nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
        (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
        (nativeC60BCMapClosedStep S F word
          (nativeC60CFDiamondRight S F q)) ↔
      nativeC60BVGeneratorCode S F q.leftFirst =
        nativeC60BVGeneratorCode S F q.rightFirst ∧
      nativeC60BVGeneratorCode S F q.leftSecond =
        nativeC60BVGeneratorCode S F q.rightSecond := by
  constructor
  · intro hstrict
    have hfree := (nativeC60CDAll_raw_free_eq_iff_strict S F word
      (nativeC60CFDiamondLeft S F q)
      (nativeC60CFDiamondRight S F q)).mpr hstrict
    change nativeC60BWFreeHolonomy S F
        (.trans (.atom q.leftFirst) (.atom q.leftSecond)) =
      nativeC60BWFreeHolonomy S F
        (.trans (.atom q.rightFirst) (.atom q.rightSecond)) at hfree
    rw [nativeC60BYTwoAtomic_holonomy S F q.leftFirst q.leftSecond,
      nativeC60BYTwoAtomic_holonomy S F q.rightFirst q.rightSecond] at hfree
    have hcodes := (nativeC60BYPositiveFreeWord_injective S) hfree
    injection hcodes with hfirst htail
    injection htail with hsecond hnil
    exact ⟨hfirst, hsecond⟩
  · rintro ⟨hfirst, hsecond⟩
    apply (nativeC60CDAll_raw_free_eq_iff_strict S F word
      (nativeC60CFDiamondLeft S F q)
      (nativeC60CFDiamondRight S F q)).mp
    change nativeC60BWFreeHolonomy S F
        (.trans (.atom q.leftFirst) (.atom q.leftSecond)) =
      nativeC60BWFreeHolonomy S F
        (.trans (.atom q.rightFirst) (.atom q.rightSecond))
    rw [nativeC60BYTwoAtomic_holonomy S F q.leftFirst q.leftSecond,
      nativeC60BYTwoAtomic_holonomy S F q.rightFirst q.rightSecond]
    have hlist :
        ([nativeC60BVGeneratorCode S F q.leftFirst,
          nativeC60BVGeneratorCode S F q.leftSecond] :
            List (NativeC60BVGeneratorCode S)) =
        [nativeC60BVGeneratorCode S F q.rightFirst,
          nativeC60BVGeneratorCode S F q.rightSecond] := by
      simp only [hfirst, hsecond]
    exact congrArg (nativeC60BYPositiveFreeWord S) hlist

/-- A commuting positive diamond MUST in fact recover equality of
the two original proof-relevant intermediate 15D cells, not just their
14D boundaries or an observer/Peiffer shadow. -/
theorem nativeC60CFDiamond_midpoint_eq_of_strict
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (word : List Bool) (q : NativeC60CFTypedDiamond S F)
    (h : nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
        (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
        (nativeC60BCMapClosedStep S F word
          (nativeC60CFDiamondLeft S F q)) =
      nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
        (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
        (nativeC60BCMapClosedStep S F word
          (nativeC60CFDiamondRight S F q))) :
    q.leftMid = q.rightMid := by
  have hc := (nativeC60CFDiamond_strict_iff_complete_codes S F word q).mp h
  exact (nativeC60CBGen_target S F q.leftFirst).trans
    ((congrArg (fun code : NativeC60BVGeneratorCode S =>
        nativeC60BCContextTotal F code.1 code.2.2.1) hc.1).trans
      (nativeC60CBGen_target S F q.rightFirst).symm)

/-- A genuinely DIFFERENT original intermediate 15D witness is an
unconditional obstruction to commuting the two positive raw16D routes
in the existing selected strict Kuu quotient at EVERY finite AQ word. -/
theorem nativeC60CFDiamond_distinct_midpoint_no_strict
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (word : List Bool) (q : NativeC60CFTypedDiamond S F)
    (hne : q.leftMid ≠ q.rightMid) :
    nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
        (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
        (nativeC60BCMapClosedStep S F word
          (nativeC60CFDiamondLeft S F q)) ≠
      nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
        (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
        (nativeC60BCMapClosedStep S F word
          (nativeC60CFDiamondRight S F q)) := by
  intro h
  exact hne (nativeC60CFDiamond_midpoint_eq_of_strict S F word q h)

/-- Any additional proposed 16D geometric diamond equation with
different actual intermediate 15D proofs fails CE compatibility;
its full original noncommutative holonomy is necessarily unequal. -/
theorem nativeC60CFDiamond_distinct_midpoint_no_descent
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (R : NativeC60AZParallelRelation (nativeC60BCClosedSignature S F))
    (q : NativeC60CFTypedDiamond S F)
    (hne : q.leftMid ≠ q.rightMid)
    (hrel : R (nativeC60CFDiamondLeft S F q)
      (nativeC60CFDiamondRight S F q)) :
    ¬ NativeC60CEGeometricCompatible S F R := by
  have hfree : nativeC60BWFreeHolonomy S F
      (nativeC60CFDiamondLeft S F q) ≠
    nativeC60BWFreeHolonomy S F
      (nativeC60CFDiamondRight S F q) := by
    intro hf
    exact (nativeC60CFDiamond_distinct_midpoint_no_strict S F [] q hne)
      ((nativeC60CDAll_raw_free_eq_iff_strict S F [] _ _).mp hf)
  exact nativeC60CEHolonomyMismatch_no_compatibility
    S F R _ _ hrel hfree

/-- The same genuine diamond is an obstruction to a free receiver
factorization through any chosen extra geometric relator forcing the
two different-intermediate paths to agree. -/
theorem nativeC60CFDiamond_distinct_midpoint_no_factor
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (R : NativeC60AZParallelRelation (nativeC60BCClosedSignature S F))
    (q : NativeC60CFTypedDiamond S F)
    (hne : q.leftMid ≠ q.rightMid)
    (hrel : R (nativeC60CFDiamondLeft S F q)
      (nativeC60CFDiamondRight S F q)) :
    ¬ ∃ G : NativeC60AZStrictSpace (nativeC60BCClosedSignature S F) R ⥤
        SingleObj (FreeGroup (NativeC60BVGeneratorCode S))ᵐᵒᵖ,
      nativeC60AZStrictProject (nativeC60BCClosedSignature S F) R ⋙ G =
        nativeC60AZRawHolonomy (nativeC60BCClosedSignature S F)
          (nativeC60BWFreeWeight S F) := by
  intro h
  exact nativeC60CFDiamond_distinct_midpoint_no_descent
    S F R q hne hrel
      ((nativeC60CECompatible_iff_holonomy_factor S F R).mpr h)

/-- Actual structural unit/cancellation/zigzag triangle candidates at
exact original 15D boundaries. These are strictly PRESENTATION-SIDE
laws, not newly fabricated geometric 16-cell witnesses. -/
inductive NativeC60CFTriangleRelation
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L) :
    {a b : L.Total} →
    NativeC60AXStep (nativeC60BCClosedSignature S F) a b →
    NativeC60AXStep (nativeC60BCClosedSignature S F) a b → Prop where
  | cancel_left {a b : L.Total}
      (g : (nativeC60BCClosedSignature S F).Gen a b) :
      NativeC60CFTriangleRelation S F
        (.trans (.atom g) (.symm (.atom g))) (.refl a)
  | cancel_right {a b : L.Total}
      (g : (nativeC60BCClosedSignature S F).Gen a b) :
      NativeC60CFTriangleRelation S F
        (.trans (.symm (.atom g)) (.atom g)) (.refl b)
  | zigzag {a b : L.Total}
      (g : (nativeC60BCClosedSignature S F).Gen a b) :
      NativeC60CFTriangleRelation S F
        (.trans (.trans (.atom g) (.symm (.atom g))) (.atom g))
        (.atom g)

/-- Each concrete genuine BC triangle preserves the entire
noncommutative free-group sixteen-dimensional word. -/
theorem nativeC60CFTriangle_compatible
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L) :
    NativeC60CEGeometricCompatible S F (NativeC60CFTriangleRelation S F) := by
  intro a b c d h
  cases h with
  | cancel_left g =>
      change FreeGroup.of (nativeC60BVGeneratorCode S F g) *
          (FreeGroup.of (nativeC60BVGeneratorCode S F g))⁻¹ = 1
      exact mul_inv_cancel _
  | cancel_right g =>
      change (FreeGroup.of (nativeC60BVGeneratorCode S F g))⁻¹ *
          FreeGroup.of (nativeC60BVGeneratorCode S F g) = 1
      exact inv_mul_cancel _
  | zigzag g =>
      change (FreeGroup.of (nativeC60BVGeneratorCode S F g) *
          (FreeGroup.of (nativeC60BVGeneratorCode S F g))⁻¹) *
            FreeGroup.of (nativeC60BVGeneratorCode S F g) =
          FreeGroup.of (nativeC60BVGeneratorCode S F g)
      rw [mul_inv_cancel, one_mul]

/-- Therefore the original COMPLETE free-group receiver really
factors through this specified structural triangle-coherence
presentation, without adding any geometric fillers or axioms. -/
theorem nativeC60CFTriangle_receiver_factor
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L) :
    ∃ G : NativeC60AZStrictSpace (nativeC60BCClosedSignature S F)
        (NativeC60CFTriangleRelation S F) ⥤
        SingleObj (FreeGroup (NativeC60BVGeneratorCode S))ᵐᵒᵖ,
      nativeC60AZStrictProject (nativeC60BCClosedSignature S F)
          (NativeC60CFTriangleRelation S F) ⋙ G =
        nativeC60AZRawHolonomy (nativeC60BCClosedSignature S F)
          (nativeC60BWFreeWeight S F) :=
  (nativeC60CECompatible_iff_holonomy_factor S F
    (NativeC60CFTriangleRelation S F)).mp
      (nativeC60CFTriangle_compatible S F)

/-- The genuine zigzag triangle commutes as a selected STRICT
Kuu equality at EVERY finite original AQ context. -/
theorem nativeC60CFTriangle_strict_frame
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (word : List Bool) {a b : L.Total}
    (g : (nativeC60BCClosedSignature S F).Gen a b) :
    nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
        (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
        (nativeC60BCMapClosedStep S F word
          (.trans (.trans (.atom g) (.symm (.atom g))) (.atom g))) =
      nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
        (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
        (nativeC60BCMapClosedStep S F word (.atom g)) :=
  (nativeC60CECompatible_iff_all_frames S F
    (NativeC60CFTriangleRelation S F)).mp
    (nativeC60CFTriangle_compatible S F)
      word _ _ (.zigzag g)

section PhysicalC60

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

/-- An ACTUAL physical AU naturality zigzag with THREE genuine
16D raw steps (forward, reverse, forward) has the same selected strict
arrow as the independent original forward BC primitive at EVERY
original C60 AQ context. The raw syntax remains different. -/
theorem nativeK5CFPhysicalAU_zigzag_strict
    (W : NativeK5StructuralThirteenCell p U V) (word : List Bool) :
    nativeC60AZStrictStep (nativeK5BCSignature W)
        (nativeC60AZNoRelations (nativeK5BCSignature W))
        (nativeK5BCClosedContextStep W word
          (.trans
            (.trans (.atom (nativeK5CEPhysicalAUGenerator W))
              (.symm (.atom (nativeK5CEPhysicalAUGenerator W))))
            (.atom (nativeK5CEPhysicalAUGenerator W)))) =
      nativeC60AZStrictStep (nativeK5BCSignature W)
        (nativeC60AZNoRelations (nativeK5BCSignature W))
        (nativeK5BCClosedContextStep W word
          (.atom (nativeK5CEPhysicalAUGenerator W))) :=
  nativeC60CFTriangle_strict_frame
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
    word (nativeK5CEPhysicalAUGenerator W)

/-- In ORIGINAL raw16D constructors the physically sourced zigzag
and the singleton generator are visibly DIFFERENT terms. The strict
equation above is not a raw proof-object identity. -/
theorem nativeK5CFPhysicalAU_zigzag_raw_ne
    (W : NativeK5StructuralThirteenCell p U V) :
    (NativeC60AXStep.trans
      (NativeC60AXStep.trans
        (NativeC60AXStep.atom (nativeK5CEPhysicalAUGenerator W))
        (NativeC60AXStep.symm
          (NativeC60AXStep.atom (nativeK5CEPhysicalAUGenerator W))))
      (NativeC60AXStep.atom (nativeK5CEPhysicalAUGenerator W))) ≠
        NativeC60AXStep.atom (nativeK5CEPhysicalAUGenerator W) := by
  intro h
  cases h

/-- The same TRUE physical C60 AU triangle retains its distinct
15D naturality proofs and NONIDENTITY primitive free word. Hence the
coherence is a genuine strict cancellation, not erasure of the AU
primitive nor an unsourced geometric 16-cell. -/
theorem nativeK5CFPhysicalAU_coherence_nontrivial
    (W : NativeK5StructuralThirteenCell p U V) (word : List Bool) :
    ((nativeK5BSNaturalityFirst W).1.1 ≠
      (nativeK5BSNaturalitySecond W).1.1) ∧
    (nativeC60BWFreeHolonomy (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W)
        (nativeK5BCClosedContextStep W word
          (nativeK5BSNaturality_declared_bridge W)) ≠
        (1 : FreeGroup
          (NativeC60BVGeneratorCode (nativeK5AXKuuSignature W)))) ∧
    (nativeC60AZStrictStep (nativeK5BCSignature W)
        (nativeC60AZNoRelations (nativeK5BCSignature W))
        (nativeK5BCClosedContextStep W word
          (.trans
            (.trans (.atom (nativeK5CEPhysicalAUGenerator W))
              (.symm (.atom (nativeK5CEPhysicalAUGenerator W))))
            (.atom (nativeK5CEPhysicalAUGenerator W)))) =
      nativeC60AZStrictStep (nativeK5BCSignature W)
        (nativeC60AZNoRelations (nativeK5BCSignature W))
        (nativeK5BCClosedContextStep W word
          (.atom (nativeK5CEPhysicalAUGenerator W)))) := by
  exact ⟨nativeK5BSNaturality_full_sources_ne W,
    nativeK5CEPhysicalAU_all_frames_nontrivial W word,
    nativeK5CFPhysicalAU_zigzag_strict W word⟩

end PhysicalC60

#print axioms nativeC60CFDiamond_strict_iff_complete_codes
#print axioms nativeC60CFDiamond_midpoint_eq_of_strict
#print axioms nativeC60CFDiamond_distinct_midpoint_no_strict
#print axioms nativeC60CFDiamond_distinct_midpoint_no_descent
#print axioms nativeC60CFDiamond_distinct_midpoint_no_factor
#print axioms nativeC60CFTriangle_compatible
#print axioms nativeC60CFTriangle_receiver_factor
#print axioms nativeC60CFTriangle_strict_frame
#print axioms nativeK5CFPhysicalAU_zigzag_strict
#print axioms nativeK5CFPhysicalAU_zigzag_raw_ne
#print axioms nativeK5CFPhysicalAU_coherence_nontrivial

end
end Kuu.F112.Physical
