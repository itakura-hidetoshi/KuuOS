import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4AUParametricMatrixInvariant
import Mathlib.Data.Int.ModEq
import Mathlib.Tactic

/-!
F112-P94D3GK4AU -- exact specializations and SHARP modular dependence
of the original F54 parametric family. M(1)=M_AF and M(4)=M_AH;
det M(t)=1 for all integer t. If s=t mod k, then M_r(s)=M_r(t)
entrywise mod k for every genuine typed route r, original Q and S.

A REAL forward/backward LocalRotation backtrack has
  M_B(t)=[[1-t,-1],[t,1]].
It detects the parameter itself. Thus on ANY original self-Hom
with such a true witness, universal entrywise congruence of the
two parameter observers is EQUIVALENT to s=t mod k, or k | t-s.
The same iff holds separately on Q and S. In particular the old
AF/AH pair is universally congruent mod k iff k | 3. This is about
TWO OBSERVERS OF THE SAME ROUTE, not two points of a fixed old fiber.
Distinct parameters give distinct structural observer maps, without
claiming faithfulness of any one observer or a fixed infinite fiber.
All previous AT/AS/AR slice results are retained unchanged. No
whole-family descent through existing K_AI is asserted.
Append-only/tighten-only/same-root107; protect #1558 unmerged.
Lean v4.30.0-rc2; mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section
universe uD vD uE vE

/-- Entrywise congruence for any integer modulus, including zero. -/
def nativeGK4AUMatrixModEq (k : Int) (A B : NativeGK4AHMatrix) : Prop :=
  Int.ModEq k A.1.1 B.1.1 ∧ Int.ModEq k A.1.2 B.1.2 ∧
  Int.ModEq k A.2.1 B.2.1 ∧ Int.ModEq k A.2.2 B.2.2

theorem nativeGK4AUMatrixModEq_refl (k : Int) (A : NativeGK4AHMatrix) :
    nativeGK4AUMatrixModEq k A A :=
  ⟨Int.ModEq.refl _, Int.ModEq.refl _, Int.ModEq.refl _, Int.ModEq.refl _⟩

theorem nativeGK4AUMatrixModEq_mul (k : Int) (A B C D : NativeGK4AHMatrix)
    (hAC : nativeGK4AUMatrixModEq k A C)
    (hBD : nativeGK4AUMatrixModEq k B D) :
    nativeGK4AUMatrixModEq k (nativeGK4AHMul A B) (nativeGK4AHMul C D) := by
  rcases hAC with ⟨ha, hb, hc, hd⟩
  rcases hBD with ⟨he, hf, hg, hh⟩
  exact ⟨(ha.mul he).add (hb.mul hg), (ha.mul hf).add (hb.mul hh),
    (hc.mul he).add (hd.mul hg), (hc.mul hf).add (hd.mul hh)⟩

section GenuineOriginalSource
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}

theorem nativeGK4AUEdge_specialize
    {n m : Nat} {before after : KuuNativeF45Tree p n m ma pa mb pb}
    (edge : KuuNativeF45Tree.RotationEdge p before after) :
    edge.gk4auFamily 1 = edge.gk4afMatrix ∧
      edge.gk4auFamily 4 = edge.gk4ahMatrix := by
  cases edge <;> exact ⟨rfl, rfl⟩

theorem nativeGK4AUChain_specialize
    {n m : Nat} {before after : KuuNativeF45Tree p n m ma pa mb pb}
    (chain : KuuNativeF45Tree.RotationChain p before after) :
    chain.gk4auFamily 1 = chain.gk4afMatrix ∧
      chain.gk4auFamily 4 = chain.gk4ahMatrix := by
  induction chain with
  | refl => exact ⟨rfl, rfl⟩
  | snoc path edge ih =>
      have he := nativeGK4AUEdge_specialize edge
      constructor
      · change nativeGK4AHMul (path.gk4auFamily 1) (edge.gk4auFamily 1) =
          nativeGK4AFMul path.gk4afMatrix edge.gk4afMatrix
        rw [ih.1, he.1]
        rfl
      · change nativeGK4AHMul (path.gk4auFamily 4) (edge.gk4auFamily 4) =
          nativeGK4AHMul path.gk4ahMatrix edge.gk4ahMatrix
        rw [ih.2, he.2]

/-- EXACT recovery, not just recovery of traces or modular classes. -/
theorem nativeGK4AURoute_specialize
    {n n' m m' : Nat}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (route : KuuNativeF45Tree.DepthRotationRoute p first last) :
    route.gk4auFamily 1 = route.gk4afMatrix ∧
      route.gk4auFamily 4 = route.gk4ahMatrix := by
  induction route with
  | chain path => exact nativeGK4AUChain_specialize path
  | castDepths _ _ _ => exact ⟨rfl, rfl⟩
  | trans u v ihu ihv =>
      constructor
      · change nativeGK4AHMul (u.gk4auFamily 1) (v.gk4auFamily 1) =
          nativeGK4AFMul u.gk4afMatrix v.gk4afMatrix
        rw [ihu.1, ihv.1]
        rfl
      · change nativeGK4AHMul (u.gk4auFamily 4) (v.gk4auFamily 4) =
          nativeGK4AHMul u.gk4ahMatrix v.gk4ahMatrix
        rw [ihu.2, ihv.2]
  | leftContext _ _ ih => exact ih
  | rightContext _ _ ih => exact ih

theorem nativeGK4AUEdge_modEq
    {n m : Nat} {before after : KuuNativeF45Tree p n m ma pa mb pb}
    (edge : KuuNativeF45Tree.RotationEdge p before after)
    (k s t : Int) (h : Int.ModEq k s t) :
    nativeGK4AUMatrixModEq k (edge.gk4auFamily s) (edge.gk4auFamily t) := by
  cases edge with
  | forward _ => exact nativeGK4AUMatrixModEq_refl k _
  | backward _ =>
      exact ⟨Int.ModEq.refl _, Int.ModEq.refl _, h, Int.ModEq.refl _⟩

theorem nativeGK4AUChain_modEq
    {n m : Nat} {before after : KuuNativeF45Tree p n m ma pa mb pb}
    (chain : KuuNativeF45Tree.RotationChain p before after)
    (k s t : Int) (h : Int.ModEq k s t) :
    nativeGK4AUMatrixModEq k (chain.gk4auFamily s) (chain.gk4auFamily t) := by
  induction chain with
  | refl => exact nativeGK4AUMatrixModEq_refl k _
  | snoc path edge ih =>
      exact nativeGK4AUMatrixModEq_mul k _ _ _ _ ih
        (nativeGK4AUEdge_modEq edge k s t h)

theorem nativeGK4AURoute_modEq
    {n n' m m' : Nat}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (route : KuuNativeF45Tree.DepthRotationRoute p first last)
    (k s t : Int) (h : Int.ModEq k s t) :
    nativeGK4AUMatrixModEq k (route.gk4auFamily s) (route.gk4auFamily t) := by
  induction route with
  | chain path => exact nativeGK4AUChain_modEq path k s t h
  | castDepths _ _ _ => exact nativeGK4AUMatrixModEq_refl k _
  | trans _ _ ihu ihv => exact nativeGK4AUMatrixModEq_mul k _ _ _ _ ihu ihv
  | leftContext _ _ ih => exact ih
  | rightContext _ _ ih => exact ih

theorem nativeGK4AUEdge_det
    {n m : Nat} {before after : KuuNativeF45Tree p n m ma pa mb pb}
    (edge : KuuNativeF45Tree.RotationEdge p before after) (t : Int) :
    nativeGK4AODet (edge.gk4auFamily t) = 1 := by
  cases edge with
  | forward _ => exact nativeGK4AOIntegralCongruence_forward.1
  | backward _ =>
      simp [KuuNativeF45Tree.RotationEdge.gk4auFamily,
        nativeGK4AUBackward, nativeGK4AODet]

theorem nativeGK4AUChain_det
    {n m : Nat} {before after : KuuNativeF45Tree p n m ma pa mb pb}
    (chain : KuuNativeF45Tree.RotationChain p before after) (t : Int) :
    nativeGK4AODet (chain.gk4auFamily t) = 1 := by
  induction chain with
  | refl => exact nativeGK4AOIntegralCongruence_one.1
  | snoc path edge ih =>
      change nativeGK4AODet
        (nativeGK4AHMul (path.gk4auFamily t) (edge.gk4auFamily t)) = 1
      rw [nativeGK4AODet_mul, ih, nativeGK4AUEdge_det edge t, mul_one]

/-- Determinant one at EVERY integer parameter, not only 1 and 4. -/
theorem nativeGK4AURoute_det
    {n n' m m' : Nat}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (route : KuuNativeF45Tree.DepthRotationRoute p first last) (t : Int) :
    nativeGK4AODet (route.gk4auFamily t) = 1 := by
  induction route with
  | chain path => exact nativeGK4AUChain_det path t
  | castDepths _ _ _ => exact nativeGK4AOIntegralCongruence_cast.1
  | trans u v ihu ihv =>
      change nativeGK4AODet
        (nativeGK4AHMul (u.gk4auFamily t) (v.gk4auFamily t)) = 1
      rw [nativeGK4AODet_mul, ihu, ihv, mul_one]
  | leftContext _ _ ih => exact ih
  | rightContext _ _ ih => exact ih

end GenuineOriginalSource

section GenuineQuotientSpecialization
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable {n n' m m' : Nat}
variable (first : KuuNativeF45Tree p n m ma pa mb pb)
variable (last : KuuNativeF45Tree p n' m' ma pa mb pb)

theorem nativeGK4AUP92_specialize (q : NativeF55P92AssocRouteClasses first last) :
    nativeGK4AUP92Value first last q 1 = nativeGK4AFP92Value first last q ∧
      nativeGK4AUP92Value first last q 4 = nativeGK4AHP92Value first last q := by
  refine _root_.Quotient.inductionOn q ?_
  intro raw
  exact nativeGK4AURoute_specialize raw

theorem nativeGK4AUStructural_specialize
    (q : NativeGK4EStructuralRouteClasses first last) :
    nativeGK4AUStructuralValue first last q 1 = nativeGK4AFStructuralValue first last q ∧
      nativeGK4AUStructuralValue first last q 4 = nativeGK4AHStructuralValue first last q := by
  refine _root_.Quotient.inductionOn q ?_
  intro raw
  exact nativeGK4AURoute_specialize raw

theorem nativeGK4AUP92_modEq (q : NativeF55P92AssocRouteClasses first last)
    (k s t : Int) (h : Int.ModEq k s t) :
    nativeGK4AUMatrixModEq k (nativeGK4AUP92Value first last q s)
      (nativeGK4AUP92Value first last q t) := by
  refine _root_.Quotient.inductionOn q ?_
  intro raw
  exact nativeGK4AURoute_modEq raw k s t h

theorem nativeGK4AUStructural_modEq
    (q : NativeGK4EStructuralRouteClasses first last)
    (k s t : Int) (h : Int.ModEq k s t) :
    nativeGK4AUMatrixModEq k (nativeGK4AUStructuralValue first last q s)
      (nativeGK4AUStructuralValue first last q t) := by
  refine _root_.Quotient.inductionOn q ?_
  intro raw
  exact nativeGK4AURoute_modEq raw k s t h

theorem nativeGK4AUP92_det (q : NativeF55P92AssocRouteClasses first last) (t : Int) :
    nativeGK4AODet (nativeGK4AUP92Value first last q t) = 1 := by
  refine _root_.Quotient.inductionOn q ?_
  intro raw
  exact nativeGK4AURoute_det raw t

theorem nativeGK4AUStructural_det
    (q : NativeGK4EStructuralRouteClasses first last) (t : Int) :
    nativeGK4AODet (nativeGK4AUStructuralValue first last q t) = 1 := by
  refine _root_.Quotient.inductionOn q ?_
  intro raw
  exact nativeGK4AURoute_det raw t

end GenuineQuotientSpecialization

section SharpGenuineSelfHom
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E} {n m : Nat}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable {before after : KuuNativeF45Tree p n m ma pa mb pb}
variable (rot : KuuNativeF45Tree.LocalRotation p before after)

-- The sharp converses require this REAL source witness even when
-- their conclusion mentions only the self-Hom at before.
include rot

/-- An ACTUAL self-route, using the same typed LocalRotation witness
forward and backward. Its lower-left entry is exactly the parameter. -/
theorem nativeGK4AUBacktrack_matrix (t : Int) :
    (nativeGK4FBacktrack rot).gk4auFamily t = ((1 - t, -1), (t, 1)) := by
  change nativeGK4AHMul (nativeGK4AHMul nativeGK4AHOne nativeGK4AHForward)
    (nativeGK4AUBackward t) = ((1 - t, -1), (t, 1))
  simp [nativeGK4AHMul, nativeGK4AHOne, nativeGK4AHForward,
    nativeGK4AUBackward, sub_eq_add_neg]

/-- Exact iff on one fixed, genuinely witnessed original self-Hom. -/
theorem nativeGK4AUSelfHom_modEq_iff (k s t : Int) :
    (∀ r : KuuNativeF45Tree.DepthRotationRoute p before before,
      nativeGK4AUMatrixModEq k (r.gk4auFamily s) (r.gk4auFamily t)) ↔
    Int.ModEq k s t := by
  constructor
  · intro h
    have hc := (h (nativeGK4FBacktrack rot)).2.2.1
    simpa only [nativeGK4AUBacktrack_matrix] using hc
  · intro h r
    exact nativeGK4AURoute_modEq r k s t h

/-- The SAME sharp criterion on the ORIGINAL P92B existence quotient. -/
theorem nativeGK4AUP92SelfHom_modEq_iff (k s t : Int) :
    (∀ q : NativeF55P92AssocRouteClasses before before,
      nativeGK4AUMatrixModEq k (nativeGK4AUP92Value before before q s)
        (nativeGK4AUP92Value before before q t)) ↔ Int.ModEq k s t := by
  constructor
  · intro h
    have hc := (h (nativeF55P92AssocRouteClass before before
      (nativeGK4FBacktrack rot))).2.2.1
    change Int.ModEq k ((nativeGK4FBacktrack rot).gk4auFamily s).2.1
      ((nativeGK4FBacktrack rot).gk4auFamily t).2.1 at hc
    simpa only [nativeGK4AUBacktrack_matrix] using hc
  · intro h q
    exact nativeGK4AUP92_modEq before before q k s t h

/-- Independent S has its OWN genuine descent and same true detector. -/
theorem nativeGK4AUStructuralSelfHom_modEq_iff (k s t : Int) :
    (∀ q : NativeGK4EStructuralRouteClasses before before,
      nativeGK4AUMatrixModEq k (nativeGK4AUStructuralValue before before q s)
        (nativeGK4AUStructuralValue before before q t)) ↔ Int.ModEq k s t := by
  constructor
  · intro h
    have hc := (h (nativeGK4EStructuralRouteClass before before
      (nativeGK4FBacktrack rot))).2.2.1
    change Int.ModEq k ((nativeGK4FBacktrack rot).gk4auFamily s).2.1
      ((nativeGK4FBacktrack rot).gk4auFamily t).2.1 at hc
    simpa only [nativeGK4AUBacktrack_matrix] using hc
  · intro h q
    exact nativeGK4AUStructural_modEq before before q k s t h

/-- Distinct parameters define distinct observer MAPS on the same
structural self-Hom. This is not faithfulness of a single observer. -/
theorem nativeGK4AUStructuralParameters_injective :
    Function.Injective
      (fun t : Int => fun q : NativeGK4EStructuralRouteClasses before before =>
        nativeGK4AUStructuralValue before before q t) := by
  intro s t h
  have hb := congrFun h (nativeGK4EStructuralRouteClass before before
    (nativeGK4FBacktrack rot))
  change (nativeGK4FBacktrack rot).gk4auFamily s =
    (nativeGK4FBacktrack rot).gk4auFamily t at hb
  have hc := congrArg (fun M : NativeGK4AHMatrix => M.2.1) hb
  simpa only [nativeGK4AUBacktrack_matrix] using hc

/-- GK4AT's modulus three is SHARP as a universal cross-observer law:
a modulus works on every true self-route iff it divides 4-1=3. -/
theorem nativeGK4AUOldPair_modulus_iff (k : Int) :
    (∀ r : KuuNativeF45Tree.DepthRotationRoute p before before,
      nativeGK4AUMatrixModEq k r.gk4afMatrix r.gk4ahMatrix) ↔ k ∣ (3 : Int) := by
  constructor
  · intro h
    have hp : Int.ModEq k 1 4 :=
      (nativeGK4AUSelfHom_modEq_iff rot k 1 4).1 (by
        intro r
        rw [(nativeGK4AURoute_specialize r).1, (nativeGK4AURoute_specialize r).2]
        exact h r)
    simpa using hp.dvd
  · intro hd r
    have hp : Int.ModEq k 1 4 := Int.modEq_iff_dvd.mpr (by simpa using hd)
    have hr := nativeGK4AURoute_modEq r k 1 4 hp
    rw [(nativeGK4AURoute_specialize r).1, (nativeGK4AURoute_specialize r).2] at hr
    exact hr

end SharpGenuineSelfHom

/-- No hypothetical source witness: the physical C60 north F45
rotation realizes the exact parameter-divisibility criterion. -/
theorem nativeGK4AUPhysicalNorth_modEq_iff (k s t : Int) :
    (∀ r : KuuNativeF45Tree.DepthRotationRoute _
        nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple,
      nativeGK4AUMatrixModEq k (r.gk4auFamily s) (r.gk4auFamily t)) ↔
    k ∣ t - s :=
  (nativeGK4AUSelfHom_modEq_iff northHexagonNativeLeftRotation k s t).trans
    Int.modEq_iff_dvd

#print axioms nativeGK4AUMatrixModEq
#print axioms nativeGK4AUMatrixModEq_refl
#print axioms nativeGK4AUMatrixModEq_mul
#print axioms nativeGK4AUEdge_specialize
#print axioms nativeGK4AUChain_specialize
#print axioms nativeGK4AURoute_specialize
#print axioms nativeGK4AUEdge_modEq
#print axioms nativeGK4AUChain_modEq
#print axioms nativeGK4AURoute_modEq
#print axioms nativeGK4AUEdge_det
#print axioms nativeGK4AUChain_det
#print axioms nativeGK4AURoute_det
#print axioms nativeGK4AUP92_specialize
#print axioms nativeGK4AUStructural_specialize
#print axioms nativeGK4AUP92_modEq
#print axioms nativeGK4AUStructural_modEq
#print axioms nativeGK4AUP92_det
#print axioms nativeGK4AUStructural_det
#print axioms nativeGK4AUBacktrack_matrix
#print axioms nativeGK4AUSelfHom_modEq_iff
#print axioms nativeGK4AUP92SelfHom_modEq_iff
#print axioms nativeGK4AUStructuralSelfHom_modEq_iff
#print axioms nativeGK4AUStructuralParameters_injective
#print axioms nativeGK4AUOldPair_modulus_iff
#print axioms nativeGK4AUPhysicalNorth_modEq_iff

end
end Kuu.F112.Physical
