import KUOS.Architecture.QiWuxingNativeC60GaugeV3_4
import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5YDirectPhiFiveEdgeCoherence
import Mathlib.Tactic

/-!
# Qi v3.5 — one five-phase carrier for Wuxing, actual C60 pentagons, and categorical pentagons

The same `FivePhase = ZMod 5` indexes (a) Qi generation/control, (b) the
five actual slots of each of twelve C60 pentagonal faces, and (c) the five
genuine Mathlib four-equivalence parenthesizations in GK5X/GK5Y.

The bridge supplies a genuine slot equivalence, actual C60 around-edges
for every directed GK5 pentagon edge, and an endpoint-typed whole NatIso
over the same five-phase edge signature. The source-to-target orientation
of two categorical edges is opposite to the geometric positive cycle.
No raw F54/F55/P92B proof history, physical face, equivalence record or
higher-dimensional cell is identified merely from cardinality five.

This is an additive cross-family presentation: it does NOT make all three
mathematical objects definitionally equal or assert new 4-cell fillers.
All original strict Kuu, independent Kuu, Qi, physical geometry, and
GK5Y whole-NatIso pentagon evidence remain authoritative at their scopes.
-/ 

namespace KUOS.Architecture.WuxingPentagonUnified

open KUOS.Architecture.WuxingCyclicPaths
open Kuu.F112.Physical
open CategoryTheory

set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uI vC uC

/-- Exactly the existing Qi phase carrier, not a copied five-point enumeration. -/
abbrev FivefoldIndex := FivePhase

/-- Every REAL C60 pentagonal chart is exactly one translated five-phase torsor. -/
def fivefoldSlotEquiv (frame : NativeC60FivePhaseGauge) (v : Vertex) :
    FivefoldIndex ≃ Slot where
  toFun := nativeC60GaugeSlot frame v
  invFun := fun s => slotIndex s - frame v
  left_inv := by
    intro p
    change slotIndex (nativeC60GaugeSlot frame v p) - frame v = p
    rw [nativeC60GaugeSlot_index]
    change p + frame v - frame v = p
    abel
  right_inv := by
    intro s
    apply nativeC60SlotIndex_injective
    change slotIndex (nativeC60GaugeSlot frame v (slotIndex s - frame v)) =
      slotIndex s
    rw [nativeC60GaugeSlot_index]
    change (slotIndex s - frame v) + frame v = slotIndex s
    abel

/-- Physical rotation by one slot is LITERALLY Qi's +1 on the common phase. -/
theorem fivefoldSlot_successor (frame : NativeC60FivePhaseGauge)
    (v : Vertex) (p : FivefoldIndex) :
    slotNext (fivefoldSlotEquiv frame v p) =
      fivefoldSlotEquiv frame v (p + 1) := by
  apply nativeC60SlotIndex_injective
  have hnext (s : Slot) :
      slotIndex (slotNext s) = slotIndex s + 1 := by
    cases s <;> decide
  rw [hnext, nativeC60GaugeSlot_index, nativeC60GaugeSlot_index]
  change (p + frame v) + 1 = (p + 1) + frame v
  abel

/-- The single phase chooses a real C60 edge, not an invented graph edge. -/
def fivefoldSide (frame : NativeC60FivePhaseGauge) (v : Vertex)
    (p : FivefoldIndex) : Edge :=
  .around ⟨v, fivefoldSlotEquiv frame v p⟩

theorem fivefoldSide_endpoints (frame : NativeC60FivePhaseGauge)
    (v : Vertex) (p : FivefoldIndex) :
    edgeEndpoints (fivefoldSide frame v p) =
      (nativeC60GaugeDart frame v p,
       nativeC60GaugeDart frame v (p + 1)) := by
  change
    (incidentDart v (fivefoldSlotEquiv frame v p),
      incidentDart v (slotNext (fivefoldSlotEquiv frame v p))) =
    (incidentDart v (fivefoldSlotEquiv frame v p),
      incidentDart v (fivefoldSlotEquiv frame v (p + 1)))
  rw [fivefoldSlot_successor]

/-- The TRUE five directed GK5X edges, sharing five-phase endpoints. -/
inductive FivefoldEdge where
  | e01 | e12 | e23 | e04 | e43
  deriving DecidableEq, Repr, Fintype

def fivefoldFrom : FivefoldEdge → FivefoldIndex
  | .e01 => 0
  | .e12 => 1
  | .e23 => 2
  | .e04 => 0
  | .e43 => 4

def fivefoldTo : FivefoldEdge → FivefoldIndex
  | .e01 => 1
  | .e12 => 2
  | .e23 => 3
  | .e04 => 4
  | .e43 => 3

/-- For 04 and 43 the actual C60 edge is traversed in reverse. -/
def fivefoldFoot : FivefoldEdge → FivefoldIndex
  | .e01 => 0
  | .e12 => 1
  | .e23 => 2
  | .e04 => 4
  | .e43 => 3

theorem fivefoldEdge_orientation (edge : FivefoldEdge) :
    (fivefoldFrom edge = fivefoldFoot edge ∧
      fivefoldTo edge = fivefoldFoot edge + 1) ∨
    (fivefoldTo edge = fivefoldFoot edge ∧
      fivefoldFrom edge = fivefoldFoot edge + 1) := by
  cases edge <;> decide

/-- The actual physical C60 around-edge selected by a GK5X pentagon edge. -/
def fivefoldPhysicalEdge (frame : NativeC60FivePhaseGauge)
    (v : Vertex) (edge : FivefoldEdge) : Edge :=
  fivefoldSide frame v (fivefoldFoot edge)

/-- A GK5X oriented pentagon edge has precisely the two real physical darts. -/
theorem fivefoldPhysicalEdge_joins (frame : NativeC60FivePhaseGauge)
    (v : Vertex) (edge : FivefoldEdge) :
    edgeJoins (fivefoldPhysicalEdge frame v edge)
      (nativeC60GaugeDart frame v (fivefoldFrom edge))
      (nativeC60GaugeDart frame v (fivefoldTo edge)) := by
  unfold edgeJoins
  change
    edgeEndpoints (fivefoldPhysicalEdge frame v edge) =
        (nativeC60GaugeDart frame v (fivefoldFrom edge),
          nativeC60GaugeDart frame v (fivefoldTo edge)) ∨
    edgeEndpoints (fivefoldPhysicalEdge frame v edge) =
        (nativeC60GaugeDart frame v (fivefoldTo edge),
          nativeC60GaugeDart frame v (fivefoldFrom edge))
  rw [fivefoldPhysicalEdge, fivefoldSide_endpoints]
  rcases fivefoldEdge_orientation edge with ⟨hsrc, hdst⟩ | ⟨hdst, hsrc⟩
  · left
    rw [hsrc, hdst]
  · right
    rw [hdst, hsrc]

/-- ONE programmatic five-phase index also selects the actual GK5X equivalence. -/
noncomputable def fivefoldBracket
    {I : Type uI} {C D E F G : I → Cat.{vC,uC}}
    (e : ∀ i : I, C i ≌ D i)
    (g : ∀ i : I, D i ≌ E i)
    (h : ∀ i : I, E i ≌ F i)
    (k : ∀ i : I, F i ≌ G i)
    (p : FivefoldIndex) : ∀ i : I, C i ≌ G i :=
  if p = 0 then nativeGK5XBracket0 e g h k
  else if p = 1 then nativeGK5XBracket1 e g h k
  else if p = 2 then nativeGK5XBracket2 e g h k
  else if p = 3 then nativeGK5XBracket3 e g h k
  else nativeGK5XBracket4 e g h k

/-- Actual five categorical parenthesizations are carried by the same Qi phase. -/
theorem fivefoldBracket_0
    {I : Type uI} {C D E F G : I → Cat.{vC,uC}}
    (e : ∀ i : I, C i ≌ D i)
    (g : ∀ i : I, D i ≌ E i)
    (h : ∀ i : I, E i ≌ F i)
    (k : ∀ i : I, F i ≌ G i) :
    fivefoldBracket e g h k 0 = nativeGK5XBracket0 e g h k := by
  simp [fivefoldBracket]

theorem fivefoldBracket_1
    {I : Type uI} {C D E F G : I → Cat.{vC,uC}}
    (e : ∀ i : I, C i ≌ D i)
    (g : ∀ i : I, D i ≌ E i)
    (h : ∀ i : I, E i ≌ F i)
    (k : ∀ i : I, F i ≌ G i) :
    fivefoldBracket e g h k 1 = nativeGK5XBracket1 e g h k := by
  norm_num [fivefoldBracket]

theorem fivefoldBracket_2
    {I : Type uI} {C D E F G : I → Cat.{vC,uC}}
    (e : ∀ i : I, C i ≌ D i)
    (g : ∀ i : I, D i ≌ E i)
    (h : ∀ i : I, E i ≌ F i)
    (k : ∀ i : I, F i ≌ G i) :
    fivefoldBracket e g h k 2 = nativeGK5XBracket2 e g h k := by
  norm_num [fivefoldBracket]

theorem fivefoldBracket_3
    {I : Type uI} {C D E F G : I → Cat.{vC,uC}}
    (e : ∀ i : I, C i ≌ D i)
    (g : ∀ i : I, D i ≌ E i)
    (h : ∀ i : I, E i ≌ F i)
    (k : ∀ i : I, F i ≌ G i) :
    fivefoldBracket e g h k 3 = nativeGK5XBracket3 e g h k := by
  norm_num [fivefoldBracket]

theorem fivefoldBracket_4
    {I : Type uI} {C D E F G : I → Cat.{vC,uC}}
    (e : ∀ i : I, C i ≌ D i)
    (g : ∀ i : I, D i ≌ E i)
    (h : ∀ i : I, E i ≌ F i)
    (k : ∀ i : I, F i ≌ G i) :
    fivefoldBracket e g h k 4 = nativeGK5XBracket4 e g h k := by
  norm_num [fivefoldBracket]

/-- A genuine whole NatIso, indexed by the SAME oriented phase edge as its
physical C60 around-edge. Categorical equality is not a physical path equality. -/
noncomputable def fivefoldCategoricalEdge
    {I : Type uI} {C D E F G : I → Cat.{vC,uC}}
    (e : ∀ i : I, C i ≌ D i)
    (g : ∀ i : I, D i ≌ E i)
    (h : ∀ i : I, E i ≌ F i)
    (k : ∀ i : I, F i ≌ G i)
    (edge : FivefoldEdge) {i j : I} (R : C i ⥤ C j) :
    nativeGK5GChangeAtom (fivefoldBracket e g h k (fivefoldFrom edge)) R ≅
      nativeGK5GChangeAtom (fivefoldBracket e g h k (fivefoldTo edge)) R := by
  cases edge with
  | e01 =>
      simpa [fivefoldFrom, fivefoldTo, fivefoldBracket] using
        (nativeGK5XEdge01 e g h k R)
  | e12 =>
      simpa [fivefoldFrom, fivefoldTo, fivefoldBracket] using
        (nativeGK5XEdge12 e g h k R)
  | e23 =>
      simpa [fivefoldFrom, fivefoldTo, fivefoldBracket] using
        (nativeGK5XEdge23 e g h k R)
  | e04 =>
      simpa [fivefoldFrom, fivefoldTo, fivefoldBracket] using
        (nativeGK5XEdge04 e g h k R)
  | e43 =>
      simpa [fivefoldFrom, fivefoldTo, fivefoldBracket] using
        (nativeGK5XEdge43 e g h k R)

/-- The five physical-edge labels also satisfy the FULL genuine Mathlib
pentagon law on their independently constructed categorical NatIso values. -/
theorem fivefoldCategoricalPentagon
    {I : Type uI} {C D E F G : I → Cat.{vC,uC}}
    (e : ∀ i : I, C i ≌ D i)
    (g : ∀ i : I, D i ≌ E i)
    (h : ∀ i : I, E i ≌ F i)
    (k : ∀ i : I, F i ≌ G i)
    {i j : I} (R : C i ⥤ C j) :
    (fivefoldCategoricalEdge e g h k .e01 R ≪≫
      fivefoldCategoricalEdge e g h k .e12 R) ≪≫
      fivefoldCategoricalEdge e g h k .e23 R =
    fivefoldCategoricalEdge e g h k .e04 R ≪≫
      fivefoldCategoricalEdge e g h k .e43 R := by
  simpa [fivefoldCategoricalEdge, fivefoldFrom, fivefoldTo,
    fivefoldBracket] using
    (nativeGK5XPentagon_whole e g h k R)

/-- In the same unified five-phase programmatic presentation, the five
independently recursive GK5Y comparison squares ALL commute. -/
theorem fivefoldDirectPhi_allEdges
    {I : Type uI} {C D E F G : I → Cat.{vC,uC}}
    (e : ∀ i : I, C i ≌ D i)
    (g : ∀ i : I, D i ≌ E i)
    (h : ∀ i : I, E i ≌ F i)
    (k : ∀ i : I, F i ≌ G i)
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    (nativeGK5XDirectPhi0 e g h k t ≪≫
        fivefoldCategoricalEdge e g h k .e01 (nativeGK5DTreeComposite t) =
      nativeGK5XDirectPhi1 e g h k t) ∧
    (nativeGK5XDirectPhi1 e g h k t ≪≫
        fivefoldCategoricalEdge e g h k .e12 (nativeGK5DTreeComposite t) =
      nativeGK5XDirectPhi2 e g h k t) ∧
    (nativeGK5XDirectPhi2 e g h k t ≪≫
        fivefoldCategoricalEdge e g h k .e23 (nativeGK5DTreeComposite t) =
      nativeGK5XDirectPhi3 e g h k t) ∧
    (nativeGK5XDirectPhi0 e g h k t ≪≫
        fivefoldCategoricalEdge e g h k .e04 (nativeGK5DTreeComposite t) =
      nativeGK5XDirectPhi4 e g h k t) ∧
    (nativeGK5XDirectPhi4 e g h k t ≪≫
        fivefoldCategoricalEdge e g h k .e43 (nativeGK5DTreeComposite t) =
      nativeGK5XDirectPhi3 e g h k t) := by
  simpa [fivefoldCategoricalEdge, fivefoldBracket, fivefoldFrom, fivefoldTo]
    using (nativeGK5YAllFiveEdges_whole e g h k t)

#print axioms fivefoldSlot_successor
#print axioms fivefoldSide_endpoints
#print axioms fivefoldEdge_orientation
#print axioms fivefoldPhysicalEdge_joins
#print axioms fivefoldBracket_0
#print axioms fivefoldBracket_4
#print axioms fivefoldCategoricalPentagon
#print axioms fivefoldDirectPhi_allEdges

end
end KUOS.Architecture.WuxingPentagonUnified
