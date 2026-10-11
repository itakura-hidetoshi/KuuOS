import KUOS.DependentOriginationTruncatedIcosahedralPatchChargeV5_155

namespace KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156

set_option autoImplicit false
noncomputable section

/-!
# F59-A / v5.156: an independent, nontrivial braided Gray 3-cell core

Build a genuine typed, skeletal *braided 3-cell calculus* with:
* parity-graded 2-cell boundaries in ZMod 2;
* parallel 3-cells carrying the independent F58 Int × Int pentagon/square
  generator charge, PLUS a separate ZMod 2 interchanger phase;
* vertical composition/inverse, tensor and associated coherent boundaries;
* a nonidentity odd/odd interchanger with both braid hexagons,
  naturality, associator pentagon and triangle.

These are executable mathematical DATA AND EQUATIONS, not a postulated
Gray-category instance. A complete ambient Gray-category requires its
chosen zero-, one-, and two-cell carriers and coherence interface; a precise
doubly-degenerate Gray-category can be built by delooping the braided
monoidal groupoid specified by this finite algebra. F59-B will connect
it to the original typed F55 PresentedCell and F58 charge interpreter.

The interchanger's nonzero phase is invisible under the existing F58
Int × Int charge: this is an explicit information-rich target rather
than calling the abelian group alone a Gray category. No equality with
the historic Stage-II obstruction omega is asserted.
-/

/-- A *typed* 3-cell from one ZMod 2-graded 2-cell to another.
An arrow exists only between equal grades, but carries two independent
integer-generator charges and one separate, potentially nonzero phase. -/
structure GradedThreeCell (source target : ZMod 2) where
  gradeEq : source = target
  charge : Int × Int
  phase : ZMod 2

/-- Typed 3-cell extensionality: proof-irrelevance affects only the
boundary equality, NOT the integer charges or exchange phase. -/
theorem GradedThreeCell.ext
    {a b : ZMod 2} {f g : GradedThreeCell a b}
    (hc : f.charge = g.charge)
    (hp : f.phase = g.phase) : f = g := by
  cases f with
  | mk hf cf pf =>
    cases g with
    | mk hg cg pg =>
      cases hc
      cases hp
      rfl

/-- The identity 3-cell of a fixed graded 2-cell. -/
def GradedThreeCell.ident (a : ZMod 2) : GradedThreeCell a a :=
  ⟨rfl, (0, 0), 0⟩

/-- Genuine typed vertical 3-cell composition. -/
def GradedThreeCell.comp
    {a b c : ZMod 2}
    (f : GradedThreeCell a b)
    (g : GradedThreeCell b c) : GradedThreeCell a c :=
  ⟨f.gradeEq.trans g.gradeEq, f.charge + g.charge, f.phase + g.phase⟩

/-- The inversion of an invertible skeletal graded 3-cell. -/
def GradedThreeCell.inv
    {a b : ZMod 2} (f : GradedThreeCell a b) :
    GradedThreeCell b a :=
  ⟨f.gradeEq.symm, -f.charge, -f.phase⟩

/-- Left and right tensoring of 3-cells: source and target grades add,
and both independent integer charge and phase add. -/
def GradedThreeCell.tensor
    {a b c d : ZMod 2}
    (f : GradedThreeCell a b)
    (g : GradedThreeCell c d) :
    GradedThreeCell (a + c) (b + d) :=
  ⟨congrArg₂ (· + ·) f.gradeEq g.gradeEq,
    f.charge + g.charge, f.phase + g.phase⟩

theorem GradedThreeCell.ident_comp
    {a b : ZMod 2} (f : GradedThreeCell a b) :
    (GradedThreeCell.ident a).comp f = f := by
  apply GradedThreeCell.ext
  · simp [GradedThreeCell.comp, GradedThreeCell.ident]
  · simp [GradedThreeCell.comp, GradedThreeCell.ident]

theorem GradedThreeCell.comp_ident
    {a b : ZMod 2} (f : GradedThreeCell a b) :
    f.comp (GradedThreeCell.ident b) = f := by
  apply GradedThreeCell.ext
  · simp [GradedThreeCell.comp, GradedThreeCell.ident]
  · simp [GradedThreeCell.comp, GradedThreeCell.ident]

theorem GradedThreeCell.comp_assoc
    {a b c d : ZMod 2}
    (f : GradedThreeCell a b)
    (g : GradedThreeCell b c)
    (h : GradedThreeCell c d) :
    (f.comp g).comp h = f.comp (g.comp h) := by
  apply GradedThreeCell.ext
  · change (f.charge + g.charge) + h.charge =
      f.charge + (g.charge + h.charge)
    exact add_assoc _ _ _
  · change (f.phase + g.phase) + h.phase =
      f.phase + (g.phase + h.phase)
    exact add_assoc _ _ _

theorem GradedThreeCell.comp_inv
    {a b : ZMod 2} (f : GradedThreeCell a b) :
    f.comp f.inv = GradedThreeCell.ident a := by
  apply GradedThreeCell.ext
  · change f.charge + (-f.charge) = (0 : Int × Int)
    exact add_neg_cancel _
  · change f.phase + (-f.phase) = (0 : ZMod 2)
    exact add_neg_cancel _

theorem GradedThreeCell.inv_comp
    {a b : ZMod 2} (f : GradedThreeCell a b) :
    f.inv.comp f = GradedThreeCell.ident b := by
  apply GradedThreeCell.ext
  · change (-f.charge) + f.charge = (0 : Int × Int)
    exact neg_add_cancel _
  · change (-f.phase) + f.phase = (0 : ZMod 2)
    exact neg_add_cancel _

/-- The tensor is bifunctorial: the two independent 3-cell pasting orders
agree exactly, with ALL integer charges and exchange phases retained. -/
theorem GradedThreeCell.tensor_comp
    {a b c d e f : ZMod 2}
    (p : GradedThreeCell a b)
    (q : GradedThreeCell b c)
    (r : GradedThreeCell d e)
    (s : GradedThreeCell e f) :
    (p.tensor r).comp (q.tensor s) =
      (p.comp q).tensor (r.comp s) := by
  apply GradedThreeCell.ext
  · change (p.charge + r.charge) + (q.charge + s.charge) =
      (p.charge + q.charge) + (r.charge + s.charge)
    abel
  · change (p.phase + r.phase) + (q.phase + s.phase) =
      (p.phase + q.phase) + (r.phase + s.phase)
    abel

/-- A genuine associator 3-cell, kept typed rather than silently
identifying propositionally equal parentheses by definitional equality. -/
def GradedThreeCell.associator (a b c : ZMod 2) :
    GradedThreeCell ((a + b) + c) (a + (b + c)) :=
  ⟨add_assoc a b c, (0, 0), 0⟩

def GradedThreeCell.associatorInv (a b c : ZMod 2) :
    GradedThreeCell (a + (b + c)) ((a + b) + c) :=
  (GradedThreeCell.associator a b c).inv

def GradedThreeCell.leftUnitor (a : ZMod 2) :
    GradedThreeCell (0 + a) a :=
  ⟨zero_add a, (0, 0), 0⟩

def GradedThreeCell.rightUnitor (a : ZMod 2) :
    GradedThreeCell (a + 0) a :=
  ⟨add_zero a, (0, 0), 0⟩

/-- The crucial nontrivial interchanger: exchanging two odd graded
2-cells yields the nonzero additional ZMod 2 phase. -/
def GradedThreeCell.exchange (a b : ZMod 2) :
    GradedThreeCell (a + b) (b + a) :=
  ⟨add_comm a b, (0, 0), a * b⟩

/-- The Gray-interchanger can be nontrivial even at ZERO F58 integer
generator-charge. The old pair-valued charge alone cannot distinguish
this odd/odd exchange from the identity 3-cell. -/
theorem GradedThreeCell.exchange_odd_odd_nontrivial :
    (GradedThreeCell.exchange 1 1).charge =
      ((0 : Int), (0 : Int)) ∧
    (GradedThreeCell.exchange 1 1).phase = (1 : ZMod 2) := by
  constructor <;> decide

theorem GradedThreeCell.exchange_odd_odd_ne_ident :
    GradedThreeCell.exchange 1 1 ≠
      GradedThreeCell.ident ((1 : ZMod 2) + 1) := by
  intro h
  have hp := congrArg GradedThreeCell.phase h
  have hphase :
      (GradedThreeCell.exchange 1 1).phase = (1 : ZMod 2) :=
    GradedThreeCell.exchange_odd_odd_nontrivial.2
  rw [hphase] at hp
  exact (by decide : (1 : ZMod 2) ≠ 0) hp

/-- The exchange is natural in genuinely typed 3-cells, not just
an identity at the integer-charge level. -/
theorem GradedThreeCell.exchange_naturality
    {a a' b b' : ZMod 2}
    (p : GradedThreeCell a a')
    (q : GradedThreeCell b b') :
    (p.tensor q).comp (GradedThreeCell.exchange a' b') =
      (GradedThreeCell.exchange a b).comp (q.tensor p) := by
  apply GradedThreeCell.ext
  · change (p.charge + q.charge) + (0 : Int × Int) =
      (0 : Int × Int) + (q.charge + p.charge)
    abel
  · have ha : a = a' := p.gradeEq
    have hb : b = b' := q.gradeEq
    subst a'
    subst b'
    change (p.phase + q.phase) + a * b =
      a * b + (q.phase + p.phase)
    abel

/-- First full typed Gray-interchanger hexagon. -/
theorem GradedThreeCell.exchange_hexagon_forward
    (a b c : ZMod 2) :
    ((GradedThreeCell.associator a b c).comp
      (GradedThreeCell.exchange a (b + c))).comp
      (GradedThreeCell.associator b c a) =
    (((GradedThreeCell.exchange a b).tensor
      (GradedThreeCell.ident c)).comp
      (GradedThreeCell.associator b a c)).comp
        ((GradedThreeCell.ident b).tensor
          (GradedThreeCell.exchange a c)) := by
  apply GradedThreeCell.ext
  · simp [GradedThreeCell.comp, GradedThreeCell.tensor,
      GradedThreeCell.associator, GradedThreeCell.exchange,
      GradedThreeCell.ident]
  · simp [GradedThreeCell.comp, GradedThreeCell.tensor,
      GradedThreeCell.associator, GradedThreeCell.exchange,
      GradedThreeCell.ident, mul_add]

/-- Second full typed Gray-interchanger hexagon. -/
theorem GradedThreeCell.exchange_hexagon_reverse
    (a b c : ZMod 2) :
    ((GradedThreeCell.associatorInv a b c).comp
      (GradedThreeCell.exchange (a + b) c)).comp
      (GradedThreeCell.associatorInv c a b) =
    (((GradedThreeCell.ident a).tensor
      (GradedThreeCell.exchange b c)).comp
      (GradedThreeCell.associatorInv a c b)).comp
        ((GradedThreeCell.exchange a c).tensor
          (GradedThreeCell.ident b)) := by
  apply GradedThreeCell.ext
  · simp [GradedThreeCell.comp, GradedThreeCell.tensor,
      GradedThreeCell.associatorInv, GradedThreeCell.associator,
      GradedThreeCell.inv, GradedThreeCell.exchange,
      GradedThreeCell.ident]
  · simp [GradedThreeCell.comp, GradedThreeCell.tensor,
      GradedThreeCell.associatorInv, GradedThreeCell.associator,
      GradedThreeCell.inv, GradedThreeCell.exchange,
      GradedThreeCell.ident, add_mul]

/-- The explicitly typed associator obeys its original five-vertex
pentagon equation even with independent charge and phase fields. -/
theorem GradedThreeCell.associator_pentagon
    (a b c d : ZMod 2) :
    (((GradedThreeCell.associator a b c).tensor
      (GradedThreeCell.ident d)).comp
      (GradedThreeCell.associator a (b + c) d)).comp
      ((GradedThreeCell.ident a).tensor
        (GradedThreeCell.associator b c d)) =
    (GradedThreeCell.associator (a + b) c d).comp
      (GradedThreeCell.associator a b (c + d)) := by
  apply GradedThreeCell.ext
  · simp [GradedThreeCell.comp, GradedThreeCell.tensor,
      GradedThreeCell.associator, GradedThreeCell.ident]
  · simp [GradedThreeCell.comp, GradedThreeCell.tensor,
      GradedThreeCell.associator, GradedThreeCell.ident]

/-- The two unitors are compatible with the actual associator. -/
theorem GradedThreeCell.associator_triangle
    (a b : ZMod 2) :
    (GradedThreeCell.associator a 0 b).comp
      ((GradedThreeCell.ident a).tensor
        (GradedThreeCell.leftUnitor b)) =
    (GradedThreeCell.rightUnitor a).tensor
      (GradedThreeCell.ident b) := by
  apply GradedThreeCell.ext
  · simp [GradedThreeCell.comp, GradedThreeCell.tensor,
      GradedThreeCell.associator, GradedThreeCell.ident,
      GradedThreeCell.leftUnitor, GradedThreeCell.rightUnitor]
  · simp [GradedThreeCell.comp, GradedThreeCell.tensor,
      GradedThreeCell.associator, GradedThreeCell.ident,
      GradedThreeCell.leftUnitor, GradedThreeCell.rightUnitor]

/-- Recover exactly the original independent pair-valued F58 charge,
while the additional Gray exchange phase is retained in the source. -/
def GradedThreeCell.toHigherCharge
    {a b : ZMod 2} (p : GradedThreeCell a b) : Int × Int :=
  p.charge

theorem GradedThreeCell.toHigherCharge_comp
    {a b c : ZMod 2}
    (p : GradedThreeCell a b) (q : GradedThreeCell b c) :
    (p.comp q).toHigherCharge =
      p.toHigherCharge + q.toHigherCharge := by
  rfl

theorem GradedThreeCell.exchange_charge_zero
    (a b : ZMod 2) :
    (GradedThreeCell.exchange a b).toHigherCharge = (0 : Int × Int) := by
  rfl

#print axioms GradedThreeCell
#print axioms GradedThreeCell.ext
#print axioms GradedThreeCell.ident_comp
#print axioms GradedThreeCell.comp_ident
#print axioms GradedThreeCell.comp_assoc
#print axioms GradedThreeCell.comp_inv
#print axioms GradedThreeCell.inv_comp
#print axioms GradedThreeCell.tensor_comp
#print axioms GradedThreeCell.exchange_odd_odd_nontrivial
#print axioms GradedThreeCell.exchange_odd_odd_ne_ident
#print axioms GradedThreeCell.exchange_naturality
#print axioms GradedThreeCell.exchange_hexagon_forward
#print axioms GradedThreeCell.exchange_hexagon_reverse
#print axioms GradedThreeCell.associator_pentagon
#print axioms GradedThreeCell.associator_triangle
#print axioms GradedThreeCell.toHigherCharge_comp
#print axioms GradedThreeCell.exchange_charge_zero

end
end KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
