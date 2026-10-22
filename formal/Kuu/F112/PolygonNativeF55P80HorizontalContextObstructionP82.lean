import Kuu.F112.PolygonNativeF55P80UnitFourVerticalCategoryP81

/-!
# F112-P82 — source horizontal congruence obstruction in the P80 four-cell presentation

P80 is an honest P62-relative Type-valued presentation: it adds three
unit comparisons to P77's vertical certificates, but it does not add
general contextual transport of 4-cells. This distinction is testable
on ORIGINAL F55 3-proof syntax, independently of any numerical shadow.

We construct an additional finite source-syntactic receiver. It observes
whether a non-unit 3-cell nested under a left context is a literal raw
vertical composite, before any P59 normalization. The receiver respects
all seven old P77 comparison constructors and all nine P80 constructors,
including the three newly selected unit certificates.

For every non-unit non-trans raw proof f and every compatible right
F54 route v, the original P80 comparison (id ≫ f) ~ f is present,
but its ORIGINAL F55 horizontal pastes against id_v have different
receiver values, 1 versus 2. Hence no P80 four-cell relates them;
the two P80 quotient classes are distinct and the prescribed original
horizontal operation does not descend in the left variable.

We specialize the counterexample to the actual C60 north-pentagon
F55 primitive and a separately typed native F45 right-unit tree.
This proves an obstruction for THIS selected P80 four-cell grammar,
not for strict 3-categories in general, not for P62 path congruence,
and not for a future presentation with additional higher coherence.
No Gray, new axioms, sorry, admit, or dropped public roots.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

/-- An independent, explicitly SOURCE-SYNTACTIC additive invariant
for the P80 comparison grammar. It sees a vertical composite nested
under the actual left-context constructor, without identifying source
proofs from numerical shadow equality or P59 path equality.

The nested context unit is ignored exactly when its source syntax is
unit-only. Pre/post route pasting transports the syntactic context
reading; the ORIGINAL vertical paste constructor is additive. -/
def KuuNativeF45Tree.DepthRotationRoute.PresentedCell.p82ContextSignature
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb} :
    ∀ {r s : KuuNativeF45Tree.DepthRotationRoute p first last},
      KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s → Nat
  | _, _, .ident _ => 0
  | _, _, .pentagon _ _ _ _ => 0
  | _, _, .disjointSquare _ _ => 0
  | _, _, .symm _ => 0
  | _, _, .trans c d => c.p82ContextSignature + d.p82ContextSignature
  | _, _, .leftContext c _ =>
      if c.unitOnly then 0 else if c.shapeTag == 4 then 1 else 2
  | _, _, .rightContext _ c => if c.unitOnly then 0 else 2
  | _, _, .precompose _ c => c.p82ContextSignature
  | _, _, .postcompose c _ => c.p82ContextSignature

/-- All original P77 vertical 4-cell witnesses preserve this
independent source reading. Only original vertical unit, associator
and whiskering are used: contextual 4-cell transport is NOT assumed. -/
theorem NativeF55RawVerticalFourCell.p82_signature_sound
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
    (h : NativeF55RawVerticalFourCell first last f g) :
    f.p82ContextSignature = g.p82ContextSignature := by
  induction h with
  | refl raw => rfl
  | symm h ih => exact ih.symm
  | trans hfg hgh ihfg ihgh => exact ihfg.trans ihgh
  | leftWhisker prior h ih =>
      change prior.p82ContextSignature + _ = prior.p82ContextSignature + _
      rw [ih]
  | rightWhisker h suffix ih =>
      change _ + suffix.p82ContextSignature = _ + suffix.p82ContextSignature
      rw [ih]
  | leftUnit raw =>
      change (0 : Nat) + raw.p82ContextSignature = raw.p82ContextSignature
      exact Nat.zero_add _
  | rightUnit raw =>
      change raw.p82ContextSignature + (0 : Nat) = raw.p82ContextSignature
      exact Nat.add_zero _
  | assoc a b c =>
      change (a.p82ContextSignature + b.p82ContextSignature) + c.p82ContextSignature =
        a.p82ContextSignature + (b.p82ContextSignature + c.p82ContextSignature)
      exact Nat.add_assoc _ _ _

/-- Soundness for EVERY constructor of the actual P80 Type-valued
4-cell relation. In particular, the three added unit 4-cells do
not change the new signature, while arbitrary context transport of
an old 4-cell has NOT been added to the inductive grammar. -/
theorem NativeF55P80UnitFourCell.p82_signature_sound
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
    (h : NativeF55P80UnitFourCell f g) :
    f.p82ContextSignature = g.p82ContextSignature := by
  induction h with
  | old w => exact w.p82_signature_sound
  | refl raw => rfl
  | symm h ih => exact ih.symm
  | trans hfg hgh ihfg ihgh => exact ihfg.trans ihgh
  | leftWhisker prior h ih =>
      change prior.p82ContextSignature + _ = prior.p82ContextSignature + _
      rw [ih]
  | rightWhisker h suffix ih =>
      change _ + suffix.p82ContextSignature = _ + suffix.p82ContextSignature
      rw [ih]
  | horizontalUnit u v => rfl
  | leftContextUnit u later => rfl
  | rightContextUnit earlier u => rfl

/-- Under the ORIGINAL (not observer-defined) horizontal composite,
right pasting with a genuine raw identity exposes the nested left
source context. The second horizontal summand is itself unit-only. -/
theorem KuuNativeF45Tree.DepthRotationRoute.PresentedCell.p82_horizontal_right_ident
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' k k' l l' : Nat}
    {p₀ p₁ p₂ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ : KuuNativeBlocks x y}
    {leftBefore : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
    {leftAfter : KuuNativeF45Tree p n' m' p₀ q₀ p₁ q₁}
    {rightBefore : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂}
    {rightAfter : KuuNativeF45Tree p k' l' p₁ q₁ p₂ q₂}
    {u u' : KuuNativeF45Tree.DepthRotationRoute p leftBefore leftAfter}
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u u')
    (v : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter) :
    (f.horizontal (.ident v)).p82ContextSignature =
      (if f.unitOnly then 0 else if f.shapeTag == 4 then 1 else 2) := by
  rfl

/-- P80 explicitly retains the original P77 vertical left-unit
4-cell. This is an ACTUAL source proof, not a shadow coincidence. -/
theorem nativeF55P82_oldLeftUnit_witness
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {u u' : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u u') :
    Nonempty (NativeF55P80UnitFourCell (.trans (.ident u) f) f) :=
  ⟨.old (.leftUnit f)⟩

/-- The first actual horizontal incompatibility of the chosen P80
grammar. Even though an original P80 4-cell compares (id ≫ f) to f,
horizontal pasting each against the SAME original right identity
produces values 1 and 2 of a separately validated source invariant.
Thus an OUTPUT 4-cell is impossible, not merely unimplemented. -/
theorem nativeF55P82_horizontal_oldLeftUnit_noFourCell
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' k k' l l' : Nat}
    {p₀ p₁ p₂ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ : KuuNativeBlocks x y}
    {leftBefore : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
    {leftAfter : KuuNativeF45Tree p n' m' p₀ q₀ p₁ q₁}
    {rightBefore : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂}
    {rightAfter : KuuNativeF45Tree p k' l' p₁ q₁ p₂ q₂}
    {u u' : KuuNativeF45Tree.DepthRotationRoute p leftBefore leftAfter}
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u u')
    (v : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter)
    (hNonUnit : f.unitOnly = false)
    (hNotTrans : f.shapeTag ≠ 4) :
    ¬ Nonempty (NativeF55P80UnitFourCell
      ((.trans (.ident u) f).horizontal (.ident v))
      (f.horizontal (.ident v))) := by
  rintro ⟨certificate⟩
  have hs := certificate.p82_signature_sound
  have ha :
      ((KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans (.ident u) f).horizontal
        (.ident v)).p82ContextSignature = 1 := by
    rw [KuuNativeF45Tree.DepthRotationRoute.PresentedCell.p82_horizontal_right_ident]
    simp [KuuNativeF45Tree.DepthRotationRoute.PresentedCell.unitOnly,
      KuuNativeF45Tree.DepthRotationRoute.PresentedCell.shapeTag, hNonUnit]
  have hb : (f.horizontal (.ident v)).p82ContextSignature = 2 := by
    rw [KuuNativeF45Tree.DepthRotationRoute.PresentedCell.p82_horizontal_right_ident]
    simp [hNonUnit, hNotTrans]
  rw [ha, hb] at hs
  exact (by decide : (1 : Nat) ≠ 2) hs

/-- Distinctness is also EXACTLY visible in the P80 quotient kernel;
P80's new quotient cannot make the prescribed source horizontal
composition independent of representatives. -/
theorem nativeF55P82_horizontal_oldLeftUnit_class_ne
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' k k' l l' : Nat}
    {p₀ p₁ p₂ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ : KuuNativeBlocks x y}
    {leftBefore : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
    {leftAfter : KuuNativeF45Tree p n' m' p₀ q₀ p₁ q₁}
    {rightBefore : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂}
    {rightAfter : KuuNativeF45Tree p k' l' p₁ q₁ p₂ q₂}
    {u u' : KuuNativeF45Tree.DepthRotationRoute p leftBefore leftAfter}
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u u')
    (v : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter)
    (hNonUnit : f.unitOnly = false)
    (hNotTrans : f.shapeTag ≠ 4) :
    nativeF55P80UnitFourClass
      (KuuNativeF45Tree.node leftBefore rightBefore)
      (KuuNativeF45Tree.node leftAfter rightAfter)
      ((.trans (.ident u) f).horizontal (.ident v)) ≠
    nativeF55P80UnitFourClass
      (KuuNativeF45Tree.node leftBefore rightBefore)
      (KuuNativeF45Tree.node leftAfter rightAfter)
      (f.horizontal (.ident v)) := by
  intro h
  apply nativeF55P82_horizontal_oldLeftUnit_noFourCell f v hNonUnit hNotTrans
  exact (nativeF55P80UnitFourClass_eq_iff _ _ _ _).mp h

/-- Genuine north C60 independent-pentagon context for the RIGHT
operand. Its native blocks are the ACTUAL last original fourth-stage
blocks; the source sector is a real north-pentagon sector. -/
def northNativeP82RightUnitTree :
    KuuNativeF45Tree (.pentagon .north) 0 0
      northNativeF45FirstFourth northNativeF45SecondFourth
      northNativeF45FirstFourth northNativeF45SecondFourth :=
  .refl (firstFourPolygonSector (.pentagon .north) 3)
    northNativeF45FirstFourth northNativeF45SecondFourth

/-- Actual typed native F54 identity-like route of that source tree,
without identifying distinct original F54 paths. -/
def northNativeP82RightUnitRoute :
    KuuNativeF45Tree.DepthRotationRoute (.pentagon .north)
      northNativeP82RightUnitTree northNativeP82RightUnitTree :=
  .castDepths rfl rfl northNativeP82RightUnitTree

/-- PHYSICAL C60 counterexample: genuine north pentagon proof history
and a compatible typed right source unit exhibit failure of P80's
original horizontal representative independence. -/
theorem northNativeP82_horizontal_oldLeftUnit_noFourCell :
    ¬ Nonempty (NativeF55P80UnitFourCell
      ((.trans (.ident northNativeF45PentagonLong)
        northNativeF55PentagonCell).horizontal
        (.ident northNativeP82RightUnitRoute))
      (northNativeF55PentagonCell.horizontal
        (.ident northNativeP82RightUnitRoute))) := by
  exact nativeF55P82_horizontal_oldLeftUnit_noFourCell
    northNativeF55PentagonCell northNativeP82RightUnitRoute rfl (by decide)

#print axioms KuuNativeF45Tree.DepthRotationRoute.PresentedCell.p82ContextSignature
#print axioms NativeF55RawVerticalFourCell.p82_signature_sound
#print axioms NativeF55P80UnitFourCell.p82_signature_sound
#print axioms KuuNativeF45Tree.DepthRotationRoute.PresentedCell.p82_horizontal_right_ident
#print axioms nativeF55P82_oldLeftUnit_witness
#print axioms nativeF55P82_horizontal_oldLeftUnit_noFourCell
#print axioms nativeF55P82_horizontal_oldLeftUnit_class_ne
#print axioms northNativeP82RightUnitTree
#print axioms northNativeP82RightUnitRoute
#print axioms northNativeP82_horizontal_oldLeftUnit_noFourCell

end
end Kuu.F112.Physical
