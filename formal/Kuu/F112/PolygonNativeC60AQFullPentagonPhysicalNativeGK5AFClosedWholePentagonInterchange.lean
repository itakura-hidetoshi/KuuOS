import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5AEClosedEndpointWholePhiTransport
import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5YDirectPhiFiveEdgeCoherence
import Mathlib.CategoryTheory.EqToHom
import Mathlib.Tactic

/-!
F112-P94D3GK5AF — whole-pentagon coherence after genuine five-step
dependent endpoint return.

The two true four-equivalence pentagon paths, 01;12;23 and 04;43,
are WHOLE Mathlib NatIso values, with the distinct parenthesized
Equivalence records, chosen quasi-inverses and unit/counit retained.
Each path intertwines the original source/target Eq.rec transports
of GK5AE after five actual GK5F index reclassifications.

The physical C60 around Edge/Dart and historical F54/F55/P92B
Type-valued source witnesses are NOT coerced to a NatIso.
The strict 空 / independent Kuu authority boundary is unchanged.
Append-only, canonical main, public root107, protected #1558 untouched.
Pinned Lean v4.30.0-rc2 / mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section
universe uI vC uC

section ClosedWholePentagonInterchange
variable {I : Type uI} {C D E F G : I → Cat.{vC,uC}}
variable (e₁ : ∀ x : I, C x ≌ D x)
variable (e₂ : ∀ x : I, D x ≌ E x)
variable (e₃ : ∀ x : I, E x ≌ F x)
variable (e₄ : ∀ x : I, F x ≌ G x)

/-- The THREE oriented whole NatIso edges 01,12,23. -/
noncomputable def nativeGK5AFLongPath
    {i j : I} (R : C i ⥤ C j) :
    nativeGK5GChangeAtom (nativeGK5XBracket0 e₁ e₂ e₃ e₄) R ≅
      nativeGK5GChangeAtom (nativeGK5XBracket3 e₁ e₂ e₃ e₄) R :=
  (nativeGK5XEdge01 e₁ e₂ e₃ e₄ R ≪≫
    nativeGK5XEdge12 e₁ e₂ e₃ e₄ R) ≪≫
    nativeGK5XEdge23 e₁ e₂ e₃ e₄ R

/-- The other TWO correctly oriented whole NatIso edges 04,43.
They are not reinterpreted as forward physical around edges. -/
noncomputable def nativeGK5AFShortPath
    {i j : I} (R : C i ⥤ C j) :
    nativeGK5GChangeAtom (nativeGK5XBracket0 e₁ e₂ e₃ e₄) R ≅
      nativeGK5GChangeAtom (nativeGK5XBracket3 e₁ e₂ e₃ e₄) R :=
  nativeGK5XEdge04 e₁ e₂ e₃ e₄ R ≪≫
    nativeGK5XEdge43 e₁ e₂ e₃ e₄ R

/-- The genuine categorical pentagon is path-independent as an
equality of complete Mathlib NatIso, not just objectwise components. -/
theorem nativeGK5AFPaths_whole
    {i j : I} (R : C i ⥤ C j) :
    nativeGK5AFLongPath e₁ e₂ e₃ e₄ R =
      nativeGK5AFShortPath e₁ e₂ e₃ e₄ R :=
  nativeGK5XPentagon_whole e₁ e₂ e₃ e₄ R

/-- The actual source-side direct recursive Phi at P0 travels
through the long oriented pentagon route to the direct Phi at P3. -/
theorem nativeGK5AFDirectLong_whole
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    nativeGK5XDirectPhi0 e₁ e₂ e₃ e₄ t ≪≫
      nativeGK5AFLongPath e₁ e₂ e₃ e₄ (nativeGK5DTreeComposite t) =
    nativeGK5XDirectPhi3 e₁ e₂ e₃ e₄ t := by
  rcases nativeGK5YAllFiveEdges_whole e₁ e₂ e₃ e₄ t with
    ⟨h01, h12, h23, _, _⟩
  calc
    _ = (((nativeGK5XDirectPhi0 e₁ e₂ e₃ e₄ t ≪≫
        nativeGK5XEdge01 e₁ e₂ e₃ e₄ (nativeGK5DTreeComposite t)) ≪≫
        nativeGK5XEdge12 e₁ e₂ e₃ e₄ (nativeGK5DTreeComposite t)) ≪≫
        nativeGK5XEdge23 e₁ e₂ e₃ e₄ (nativeGK5DTreeComposite t)) := by
          simp only [nativeGK5AFLongPath, Iso.trans_assoc]
    _ = ((nativeGK5XDirectPhi1 e₁ e₂ e₃ e₄ t ≪≫
        nativeGK5XEdge12 e₁ e₂ e₃ e₄ (nativeGK5DTreeComposite t)) ≪≫
        nativeGK5XEdge23 e₁ e₂ e₃ e₄ (nativeGK5DTreeComposite t)) := by rw [h01]
    _ = nativeGK5XDirectPhi2 e₁ e₂ e₃ e₄ t ≪≫
        nativeGK5XEdge23 e₁ e₂ e₃ e₄ (nativeGK5DTreeComposite t) := by rw [h12]
    _ = nativeGK5XDirectPhi3 e₁ e₂ e₃ e₄ t := h23

/-- The independent short path is also a genuine whole NatIso
comparison, with the two physically reversed edges kept as 04;43. -/
theorem nativeGK5AFDirectShort_whole
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    nativeGK5XDirectPhi0 e₁ e₂ e₃ e₄ t ≪≫
      nativeGK5AFShortPath e₁ e₂ e₃ e₄ (nativeGK5DTreeComposite t) =
    nativeGK5XDirectPhi3 e₁ e₂ e₃ e₄ t := by
  rcases nativeGK5YAllFiveEdges_whole e₁ e₂ e₃ e₄ t with
    ⟨_, _, _, h04, h43⟩
  calc
    _ = (nativeGK5XDirectPhi0 e₁ e₂ e₃ e₄ t ≪≫
        nativeGK5XEdge04 e₁ e₂ e₃ e₄ (nativeGK5DTreeComposite t)) ≪≫
        nativeGK5XEdge43 e₁ e₂ e₃ e₄ (nativeGK5DTreeComposite t) := by
          simp only [nativeGK5AFShortPath, Iso.trans_assoc]
    _ = nativeGK5XDirectPhi4 e₁ e₂ e₃ e₄ t ≪≫
        nativeGK5XEdge43 e₁ e₂ e₃ e₄ (nativeGK5DTreeComposite t) := by rw [h04]
    _ = nativeGK5XDirectPhi3 e₁ e₂ e₃ e₄ t := h43

/-- The real FIVE dependent reindex steps and TWO distinct
whole-NatIso pentagon routes commute, each with both original
family and typed source/target Eq.rec returns.

The right hand source equality is the entire fourfold changed
tree; the target equality is the true P3 conjugated whole functor.
No comparison with a physical Edge or Type-valued raw history is
presumed here. -/
theorem nativeGK5AFClosedBothRoutes_whole
    (f : I → I) (hf : nativeGK5ADFiveIndex f = id)
    {i j : I} (t : NativeGK5DTypedTree C i j) :
    ((nativeGK5XDirectPhi0 e₁ e₂ e₃ e₄
        (nativeGK5AEClosedFiveTree f C hf t) ≪≫
      nativeGK5AFLongPath e₁ e₂ e₃ e₄
        (nativeGK5DTreeComposite (nativeGK5AEClosedFiveTree f C hf t))) ≪≫
      eqToIso (congrArg
        (fun u => nativeGK5GChangeAtom (nativeGK5XBracket3 e₁ e₂ e₃ e₄)
          (nativeGK5DTreeComposite u)) (nativeGK5AEClosedFiveTree_eq f C hf t))) =
    (eqToIso (congrArg
      (fun u => nativeGK5DTreeComposite
        (nativeGK5XFourTree e₁ e₂ e₃ e₄ u)) (nativeGK5AEClosedFiveTree_eq f C hf t)) ≪≫
      nativeGK5XDirectPhi3 e₁ e₂ e₃ e₄ t) ∧
    ((nativeGK5XDirectPhi0 e₁ e₂ e₃ e₄
        (nativeGK5AEClosedFiveTree f C hf t) ≪≫
      nativeGK5AFShortPath e₁ e₂ e₃ e₄
        (nativeGK5DTreeComposite (nativeGK5AEClosedFiveTree f C hf t))) ≪≫
      eqToIso (congrArg
        (fun u => nativeGK5GChangeAtom (nativeGK5XBracket3 e₁ e₂ e₃ e₄)
          (nativeGK5DTreeComposite u)) (nativeGK5AEClosedFiveTree_eq f C hf t))) =
    (eqToIso (congrArg
      (fun u => nativeGK5DTreeComposite
        (nativeGK5XFourTree e₁ e₂ e₃ e₄ u)) (nativeGK5AEClosedFiveTree_eq f C hf t)) ≪≫
      nativeGK5XDirectPhi3 e₁ e₂ e₃ e₄ t) := by
  constructor
  · rw [nativeGK5AFDirectLong_whole e₁ e₂ e₃ e₄
      (nativeGK5AEClosedFiveTree f C hf t)]
    exact nativeGK5AEFourDirectPhi3_return_whole e₁ e₂ e₃ e₄ f hf t
  · rw [nativeGK5AFDirectShort_whole e₁ e₂ e₃ e₄
      (nativeGK5AEClosedFiveTree f C hf t)]
    exact nativeGK5AEFourDirectPhi3_return_whole e₁ e₂ e₃ e₄ f hf t

#print axioms nativeGK5AFPaths_whole
#print axioms nativeGK5AFDirectLong_whole
#print axioms nativeGK5AFDirectShort_whole
#print axioms nativeGK5AFClosedBothRoutes_whole

end ClosedWholePentagonInterchange
end
end Kuu.F112.Physical
