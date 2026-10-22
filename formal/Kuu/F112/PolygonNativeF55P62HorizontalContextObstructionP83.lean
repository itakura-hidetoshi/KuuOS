import Kuu.F112.PolygonNativeF55P80HorizontalContextObstructionP82
import Kuu.F112.PolygonNativeF55StructuralUnitQuotientP64
import Mathlib.Combinatorics.Quiver.Path.Weight

/-!
# F112-P83 — genuine P62 path-congruence obstruction to horizontal context repair

P82 proves that the chosen P80 Type-valued 4-cell grammar is too small
for the original raw F55 horizontal operation: the P77 source left
vertical-unit 4-cell is not transported to an output P80 4-cell.

A tempting repair would be to add a contextual 4-cell generator and
claim its soundness in the OLD P62 independently syntactic unit-only
path congruence. We test that claim instead of assuming it.

Use Mathlib's genuine additive Quiver.Path.addWeight to extend P82's
independent raw-source syntactic signature to EVERY ORIGINAL F55
proof-labelled free path. Unlike the selected F55 (Int × Int) × ZMod 2
shadow, this observation discriminates contextual raw syntax.

Prove from all nine original raw 3-cell constructors:
  1. all source unit-only proofs have signature zero;
  2. P59 normalization preserves the exact signature;
  3. Mathlib path composition adds signature;
  4. each of P62's FIVE typed unit-only path congruence constructors
     preserves signature.
Thus the P62 quotient still distinguishes the two *real* original
horizontal pastes of (id ≫ f) and f against a common right identity:
their signature values are 1 and 2.

Specialize to the genuine C60 north-pentagon F55 primitive and the
compatible native right F45 unit from P82. Conclude a concrete
obstruction to adding the missing contextual 4-cell while retaining
P62 path-soundness. This is an obstruction for the SELECTED
P62/P80 pair, not for strict 3-categories in general, nor for
a distinctly enlarged path comparison presentation.

The pre-C60 dependent-origination theory and single published
KuuOSFormal root are preserved; no Gray, sorry, admit, or new axioms.
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

/-- A unit-only ORIGINAL F55 raw 3-cell has zero P82 syntactic
signature. This conclusion is proved from every one of the nine
raw constructors, independently from charge and shadow observers. -/
theorem KuuNativeF45Tree.DepthRotationRoute.PresentedCell.p83_unitOnly_signature_zero
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (cell : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s)
    (h : cell.unitOnly = true) :
    cell.p82ContextSignature = 0 := by
  induction cell with
  | ident _ => rfl
  | pentagon _ _ _ _ => cases h
  | disjointSquare _ _ => cases h
  | symm _ _ => rfl
  | trans c d ihc ihd =>
      have hc : c.unitOnly = true := Bool.and_elim_left h
      have hd : d.unitOnly = true := Bool.and_elim_right h
      change c.p82ContextSignature + d.p82ContextSignature = 0
      rw [ihc hc, ihd hd]
  | leftContext c later ih =>
      change c.unitOnly = true at h
      change (if c.unitOnly then 0 else if c.shapeTag == 4 then 1 else 2) = (0 : Nat)
      rw [h]
      rfl
  | rightContext earlier c ih =>
      change c.unitOnly = true at h
      change (if c.unitOnly then 0 else 2) = (0 : Nat)
      rw [h]
      rfl
  | precompose prior c ih => exact ih h
  | postcompose c suffix ih => exact ih h

/-- Actual additive free-path readout using Mathlib's
Quiver.Path.addWeight. All original dependent F54 route endpoints,
original F55 quiver edges and raw proof labels are retained. -/
def nativeF55P83PathSignature
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {r s : NativeF55RawRouteVertex first last}
    (path : Quiver.Path r s) : Nat :=
  Quiver.Path.addWeight
    (fun {u v : NativeF55RawRouteVertex first last} (edge : u ⟶ v) =>
      KuuNativeF45Tree.DepthRotationRoute.PresentedCell.p82ContextSignature edge) path

/-- P83 signature of the literal empty Mathlib path is zero. -/
@[simp] theorem nativeF55P83PathSignature_nil
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (r : NativeF55RawRouteVertex first last) :
    nativeF55P83PathSignature first last
      (Quiver.Path.nil : Quiver.Path r r) = 0 := by
  simp [nativeF55P83PathSignature]

/-- The signature is strictly additive under typed original
Mathlib free-path composition; no raw quotient is used. -/
theorem nativeF55P83PathSignature_comp
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {r s t : NativeF55RawRouteVertex first last}
    (f : Quiver.Path r s) (g : Quiver.Path s t) :
    nativeF55P83PathSignature first last (f.comp g) =
      nativeF55P83PathSignature first last f +
        nativeF55P83PathSignature first last g := by
  exact Quiver.Path.addWeight_comp _ f g

/-- A SINGLE original raw F55 proof generator has exactly its
SOURCE-syntactic P82 signature when viewed as a length-one path. -/
@[simp] theorem nativeF55P83PathSignature_raw
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (raw : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    nativeF55P83PathSignature first last raw.toNativeRawEdge.toPath =
      raw.p82ContextSignature := by
  simp [nativeF55P83PathSignature, Quiver.Hom.toPath,
    KuuNativeF45Tree.DepthRotationRoute.PresentedCell.toNativeRawEdge]

/-- P59 genuine raw-proof normalizer preserves the P83 source
signature for ALL NINE F55 raw constructors. Only raw id and
raw vertical trans are normalized as strict path operations;
the other seven retain their original raw edge. -/
theorem KuuNativeF45Tree.DepthRotationRoute.PresentedCell.p83_normalized_signature
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (raw : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    nativeF55P83PathSignature first last raw.toNativeStrictPath =
      raw.p82ContextSignature := by
  induction raw with
  | ident route =>
      exact nativeF55P83PathSignature_nil _ _ ⟨route⟩
  | pentagon _ _ _ _ =>
      exact nativeF55P83PathSignature_raw _ _ _
  | disjointSquare _ _ =>
      exact nativeF55P83PathSignature_raw _ _ _
  | symm c ih =>
      exact nativeF55P83PathSignature_raw _ _ _
  | trans c d ihc ihd =>
      change nativeF55P83PathSignature _ _
        (c.toNativeStrictPath.comp d.toNativeStrictPath) =
          c.p82ContextSignature + d.p82ContextSignature
      rw [nativeF55P83PathSignature_comp, ihc, ihd]
  | leftContext c later ih =>
      exact nativeF55P83PathSignature_raw _ _ _
  | rightContext earlier c ih =>
      exact nativeF55P83PathSignature_raw _ _ _
  | precompose prior c ih =>
      exact nativeF55P83PathSignature_raw _ _ _
  | postcompose c suffix ih =>
      exact nativeF55P83PathSignature_raw _ _ _

/-- ALL FIVE constructors of the original P62 typed path
congruence preserve the genuinely additive P83 SOURCE-signature.
The structural-unit constructor is handled by actual raw syntax;
no observer equality is used to manufacture a congruence witness. -/
theorem NativeF55UnitPathRel.p83_signature_sound
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : NativeF55RawRouteVertex first last}
    {f g : Quiver.Path r s}
    (h : NativeF55UnitPathRel first last f g) :
    nativeF55P83PathSignature first last f =
      nativeF55P83PathSignature first last g := by
  induction h with
  | refl path => rfl
  | symm h ih => exact ih.symm
  | trans hfg hgh ihfg ihgh => exact ihfg.trans ihgh
  | comp hf hg ihf ihg =>
      rw [nativeF55P83PathSignature_comp,
        nativeF55P83PathSignature_comp, ihf, ihg]
  | structuralUnit route cell hc =>
      rw [cell.p83_normalized_signature,
        cell.p83_unitOnly_signature_zero hc]
      exact (nativeF55P83PathSignature_nil first last ⟨route⟩).symm

/-- A genuine P80 Type-valued four-cell relates the raw proof
(id ≫ f) to f, but for non-unit, non-trans f the ORIGINAL horizontal
composites against the same right raw identity are NOT related even
by P62's independently generated source structural-unit path relation.
This is stronger than P82's P80-only four-cell nonexistence. -/
theorem nativeF55P83_horizontal_oldLeftUnit_not_P62
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
    ¬ NativeF55UnitPathRel
      (KuuNativeF45Tree.node leftBefore rightBefore)
      (KuuNativeF45Tree.node leftAfter rightAfter)
      ((KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans
        (.ident u) f).horizontal (.ident v)).toNativeStrictPath
      (f.horizontal (.ident v)).toNativeStrictPath := by
  intro hp62
  have hs := hp62.p83_signature_sound
  rw [KuuNativeF45Tree.DepthRotationRoute.PresentedCell.p83_normalized_signature,
    KuuNativeF45Tree.DepthRotationRoute.PresentedCell.p83_normalized_signature] at hs
  have ha :
      ((KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans
        (.ident u) f).horizontal (.ident v)).p82ContextSignature = 1 := by
    rw [KuuNativeF45Tree.DepthRotationRoute.PresentedCell.p82_horizontal_right_ident]
    simp [KuuNativeF45Tree.DepthRotationRoute.PresentedCell.unitOnly,
      KuuNativeF45Tree.DepthRotationRoute.PresentedCell.shapeTag, hNonUnit]
  have hb : (f.horizontal (.ident v)).p82ContextSignature = 2 := by
    rw [KuuNativeF45Tree.DepthRotationRoute.PresentedCell.p82_horizontal_right_ident]
    simp [hNonUnit, hNotTrans]
  rw [ha, hb] at hs
  exact (by decide : (1 : Nat) ≠ 2) hs

/-- Distinctness persists in the ACTUAL P62 Mathlib quotient
category, by its PREVIOUSLY PROVED exact witness kernel.
No novel quotient relation is defined by the P83 signature. -/
theorem nativeF55P83_horizontal_oldLeftUnit_P62Quot_ne
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
    (nativeF55StructuralUnitQuotientFunctor
      (KuuNativeF45Tree.node leftBefore rightBefore)
      (KuuNativeF45Tree.node leftAfter rightAfter)).map
      ((KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans
        (.ident u) f).horizontal (.ident v)).toNativeStrictPath ≠
    (nativeF55StructuralUnitQuotientFunctor
      (KuuNativeF45Tree.node leftBefore rightBefore)
      (KuuNativeF45Tree.node leftAfter rightAfter)).map
      (f.horizontal (.ident v)).toNativeStrictPath := by
  intro heq
  exact (nativeF55P83_horizontal_oldLeftUnit_not_P62 f v hNonUnit hNotTrans)
    ((nativeF55StructuralUnitQuotient_map_eq_iff _ _ _ _).mp heq)

/-- PHYSICAL C60 north-pentagon: two original horizontally composed
F55 raw 3-cell histories are NOT related by the original P62 unit-only
congruence. A mere contextual P80 4-cell adjoinment would therefore
FAIL the established P62 soundness interface. -/
theorem northNativeP83_horizontal_oldLeftUnit_not_P62 :
    ¬ NativeF55UnitPathRel
      (KuuNativeF45Tree.node
        (KuuNativeF45Tree.pentagon0
          northNativeF45FirstStage northNativeF45SecondStage
          northNativeF45ThirdStage northNativeF45FourthStage)
        northNativeP82RightUnitTree)
      (KuuNativeF45Tree.node
        (KuuNativeF45Tree.pentagon3
          northNativeF45FirstStage northNativeF45SecondStage
          northNativeF45ThirdStage northNativeF45FourthStage)
        northNativeP82RightUnitTree)
      ((KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans
        (.ident northNativeF45PentagonLong)
        northNativeF55PentagonCell).horizontal
        (.ident northNativeP82RightUnitRoute)).toNativeStrictPath
      (northNativeF55PentagonCell.horizontal
        (.ident northNativeP82RightUnitRoute)).toNativeStrictPath := by
  exact nativeF55P83_horizontal_oldLeftUnit_not_P62
    northNativeF55PentagonCell northNativeP82RightUnitRoute rfl (by decide)

#print axioms KuuNativeF45Tree.DepthRotationRoute.PresentedCell.p83_unitOnly_signature_zero
#print axioms nativeF55P83PathSignature
#print axioms nativeF55P83PathSignature_nil
#print axioms nativeF55P83PathSignature_comp
#print axioms nativeF55P83PathSignature_raw
#print axioms KuuNativeF45Tree.DepthRotationRoute.PresentedCell.p83_normalized_signature
#print axioms NativeF55UnitPathRel.p83_signature_sound
#print axioms nativeF55P83_horizontal_oldLeftUnit_not_P62
#print axioms nativeF55P83_horizontal_oldLeftUnit_P62Quot_ne
#print axioms northNativeP83_horizontal_oldLeftUnit_not_P62

end
end Kuu.F112.Physical
