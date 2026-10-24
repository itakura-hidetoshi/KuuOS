import Kuu.F112.PolygonNativeF55P94DK5ReorientedPentagonatorModThreeObstruction
import Mathlib.Tactic

/-!
# F112-P94D3V — genuinely typed 4-cell grammar and Z/3 sound descent

P94D3S constructed an ACTUAL Type-valued nine-face 3-cell loop
in the distinct structural F55 extension with N=3.
P94D3T declares a separate Type-valued independent pentagonator
generator and proves Peiffer for its ALGEBRAIC normal-word kernel.
P94D3U establishes the residual mod-three obstruction.

This file adds the missing TYPE-valued vertical 4-cell PRESENTATION:
- original P94C2 4-cell witnesses, faithfully embedded;
- the existing genuinely source-typed independent 4-cell generator;
- reflexive, inverse, vertically composed 4-cell proofs;
- actual proof-relevant left and right vertical 3-cell whiskering.

For EVERY constructor prove N mod 3 soundness, then obtain a genuine
setoid on ORIGINAL structurally extended 3-cell terms and a function
on their proof-relevant 4-cell quotient. The actual pentagonator
becomes a 4-cell with N=3 vs the identity's N=0, while both have the
same Z/3 readout. Any possible 3-cell representing the historical
N=1 shelling cannot be connected to identity in this new grammar.

This is a FREE four-cell presentation, not yet a strict n-category:
in particular horizontal 4-cell interchange, full inverse/unit
coherence and descent back to OLD P92B are NOT inferred from
the constructors, graph paths or the algebraic Peiffer kernel.
No Gray, sorry/admit, added logical axioms, or changes to C60 and
the 107 retained public roots.
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

/-- A DISTINCT genuinely Type-valued source 4-cell grammar over the
existing structural 3-cell syntax: no arbitrary group-word equality
or shadow equality creates a higher cell. -/
inductive NativeK5StructuralFourCell (p : Polygon) :
    ∀ {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last},
      NativeF55StructuralComparison p r s →
      NativeF55StructuralComparison p r s →
      Type (max (max uD uE) (max vD vE)) where
  | old
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55P92AssocComparison p r s}
      (w : NativeF55P94CGroupFourCell f g) :
      NativeK5StructuralFourCell p (.original f) (.original g)
  | pentagonator
      {a b : D} {x y : E}
      {n₁ n₂ n₃ n₄ n₅ m₁ m₂ m₃ m₄ m₅ : Nat}
      {p₀ p₁ p₂ p₃ p₄ p₅ : KuuNativeBlocks a b}
      {q₀ q₁ q₂ q₃ q₄ q₅ : KuuNativeBlocks x y}
      (t1 : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁)
      (t2 : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂)
      (t3 : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃)
      (t4 : KuuNativeF45Tree p n₄ m₄ p₃ q₃ p₄ q₄)
      (t5 : KuuNativeF45Tree p n₅ m₅ p₄ q₄ p₅ q₅)
      {f g : NativeF55StructuralComparison p
        (nativeK5TypedGlobalF54Route t1 t2 t3 t4 t5 0)
        (nativeK5TypedGlobalF54Route t1 t2 t3 t4 t5 0)}
      (w : NativeK5ReorientedIndependentPentagonator t1 t2 t3 t4 t5 f g) :
      NativeK5StructuralFourCell p f g
  | refl
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      (f : NativeF55StructuralComparison p r s) :
      NativeK5StructuralFourCell p f f
  | symm
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      (w : NativeK5StructuralFourCell p f g) :
      NativeK5StructuralFourCell p g f
  | trans
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g h : NativeF55StructuralComparison p r s}
      (fg : NativeK5StructuralFourCell p f g)
      (gh : NativeK5StructuralFourCell p g h) :
      NativeK5StructuralFourCell p f h
  | precompose
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
      (prior : NativeF55StructuralComparison p r s)
      {f g : NativeF55StructuralComparison p s t}
      (w : NativeK5StructuralFourCell p f g) :
      NativeK5StructuralFourCell p (.trans prior f) (.trans prior g)
  | postcompose
      {a b : D} {x y : E} {n n' m m' : Nat}
      {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
      {first : KuuNativeF45Tree p n m ma pa mb pb}
      {last : KuuNativeF45Tree p n' m' ma pa mb pb}
      {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
      {f g : NativeF55StructuralComparison p r s}
      (w : NativeK5StructuralFourCell p f g)
      (suffix : NativeF55StructuralComparison p s t) :
      NativeK5StructuralFourCell p (.trans f suffix) (.trans g suffix)

/-- Sound for ALL constructors of the genuinely Type-valued
four-cell completion: original P94C2 respects INTEGER N, but
the real independent pentagonator changes N by exactly 3.
Thus Z/3, not integer N, is preserved under arbitrary proof-
relevant vertical composition and both 3-cell whiskerings. -/
theorem NativeK5StructuralFourCell.modThree_sound
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55StructuralComparison p r s}
    (w : NativeK5StructuralFourCell p f g) :
    nativeK5NaturalityCountModThree f.p94cGroupWord =
      nativeK5NaturalityCountModThree g.p94cGroupWord := by
  induction w with
  | old witness =>
      change (((nativeK5NaturalityCount _ : ℤ) : ZMod 3)) =
        ((nativeK5NaturalityCount _ : ℤ) : ZMod 3)
      exact congrArg (fun z : ℤ => (z : ZMod 3)) witness.nCount_sound
  | pentagonator t1 t2 t3 t4 t5 witness =>
      cases witness
      change nativeK5NaturalityCountModThree
          (nativeK5NineReorientedExtendedCycle t1 t2 t3 t4 t5).p94cGroupWord =
        nativeK5NaturalityCountModThree
          (nativeK5ReorientedStructuralIdentity t1 t2 t3 t4 t5).p94cGroupWord
      rw [nativeK5NineReorientedExtendedCycle_word,
        nativeK5ReorientedPentagonatorModThree_zero]
      rfl
  | refl _ => rfl
  | symm _ ih => exact ih.symm
  | trans _ _ ih₁ ih₂ => exact ih₁.trans ih₂
  | precompose prior witness ih =>
      change nativeK5NaturalityCountModThree
        (prior.p94cGroupWord + _) =
        nativeK5NaturalityCountModThree
        (prior.p94cGroupWord + _)
      simpa only [map_add] using congrArg
        (fun z : ZMod 3 =>
          nativeK5NaturalityCountModThree prior.p94cGroupWord + z) ih
  | postcompose witness suffix ih =>
      change nativeK5NaturalityCountModThree
        (_ + suffix.p94cGroupWord) =
        nativeK5NaturalityCountModThree
        (_ + suffix.p94cGroupWord)
      simpa only [map_add] using congrArg
        (fun z : ZMod 3 => z +
          nativeK5NaturalityCountModThree suffix.p94cGroupWord) ih

/-- Four-cell evidence gives a genuine SETOID on original proof-
relevant structural 3-cell terms with FIXED native F54 endpoints.
No numerical-shadow equality is used to invent a 4-cell witness. -/
def NativeK5StructuralFourCell.setoid
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last} :
    Setoid (NativeF55StructuralComparison p r s) where
  r := fun f g => Nonempty (NativeK5StructuralFourCell p f g)
  iseqv := ⟨
    (fun f => ⟨.refl f⟩),
    (fun h => h.elim (fun w => ⟨.symm w⟩)),
    (fun h k => h.elim (fun w => k.elim (fun v => ⟨.trans w v⟩)))⟩

/-- The original complete source-typed mod-three observer descends
to the actual new 4-cell quotient, NOT merely to the algebraic
normal-word kernel constructed earlier. -/
def nativeK5StructuralThreeCellModThree
    {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last} :
    Quotient (NativeK5StructuralFourCell.setoid (r := r) (s := s)) →
      ZMod 3 :=
  Quotient.lift
    (fun f : NativeF55StructuralComparison p r s =>
      nativeK5NaturalityCountModThree f.p94cGroupWord)
    (by
      intro f g ⟨w⟩
      exact w.modThree_sound)

section FiveNativeStages

variable {p : Polygon} {a b : D} {x y : E}
variable {n₁ n₂ n₃ n₄ n₅ m₁ m₂ m₃ m₄ m₅ : Nat}
variable {p₀ p₁ p₂ p₃ p₄ p₅ : KuuNativeBlocks a b}
variable {q₀ q₁ q₂ q₃ q₄ q₅ : KuuNativeBlocks x y}
variable
  (t1 : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁)
  (t2 : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂)
  (t3 : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃)
  (t4 : KuuNativeF45Tree p n₄ m₄ p₃ q₃ p₄ q₄)
  (t5 : KuuNativeF45Tree p n₅ m₅ p₄ q₄ p₅ q₅)

/-- The already constructed independent Type-valued pentagonator
provides an ACTUAL 4-cell in this freely generated completion. -/
def nativeK5ReorientedTypedFourCell :
    NativeK5StructuralFourCell p
      (nativeK5NineReorientedExtendedCycle t1 t2 t3 t4 t5)
      (nativeK5ReorientedStructuralIdentity t1 t2 t3 t4 t5) :=
  .pentagonator t1 t2 t3 t4 t5
    (nativeK5ReorientedIndependentPentagonator t1 t2 t3 t4 t5)

/-- This genuinely Type-valued new 4-cell does NOT preserve
the integer N-count of its boundary: source 3, target 0. -/
theorem nativeK5ReorientedTypedFourCell_integerN_ne :
    nativeK5NaturalityCount
      (nativeK5NineReorientedExtendedCycle t1 t2 t3 t4 t5).p94cGroupWord ≠
    nativeK5NaturalityCount
      (nativeK5ReorientedStructuralIdentity t1 t2 t3 t4 t5).p94cGroupWord := by
  rw [nativeK5NineReorientedExtendedCycle_NCount_three]
  change (3 : ℤ) ≠ 0
  norm_num

/-- This same actual Type-valued higher cell DOES preserve Z/3:
the original source loop is now identified with its identity
3-cell only inside this separately presented 4D completion. -/
theorem nativeK5ReorientedTypedFourCell_modThree :
    nativeK5NaturalityCountModThree
      (nativeK5NineReorientedExtendedCycle t1 t2 t3 t4 t5).p94cGroupWord =
    nativeK5NaturalityCountModThree
      (nativeK5ReorientedStructuralIdentity t1 t2 t3 t4 t5).p94cGroupWord :=
  (nativeK5ReorientedTypedFourCell t1 t2 t3 t4 t5).modThree_sound

/-- A future 3-cell with precisely the original historical formal
W word (N=1) cannot have a 4-cell to identity inside the just
defined source-typed four-cell grammar. This theorem is conditional
on the 3-cell term; it does NOT manufacture a missing old shell. -/
theorem nativeK5HistoricalWord_no_TypedFourCell
    (f : NativeF55StructuralComparison p
      (nativeK5TypedGlobalF54Route t1 t2 t3 t4 t5 0)
      (nativeK5TypedGlobalF54Route t1 t2 t3 t4 t5 0))
    (hword : f.p94cGroupWord =
      nativeK5GraphShellingWord t1 t2 t3 t4 t5) :
    ¬ Nonempty (NativeK5StructuralFourCell p f
      (nativeK5ReorientedStructuralIdentity t1 t2 t3 t4 t5)) := by
  rintro ⟨w⟩
  have h := w.modThree_sound
  rw [hword, nativeK5HistoricalShellingModThree_one] at h
  change (1 : ZMod 3) = 0 at h
  exact (by decide : (1 : ZMod 3) ≠ 0) h

#print axioms NativeK5StructuralFourCell.modThree_sound
#print axioms NativeK5StructuralFourCell.setoid
#print axioms nativeK5StructuralThreeCellModThree
#print axioms nativeK5ReorientedTypedFourCell
#print axioms nativeK5ReorientedTypedFourCell_integerN_ne
#print axioms nativeK5ReorientedTypedFourCell_modThree
#print axioms nativeK5HistoricalWord_no_TypedFourCell

end FiveNativeStages
end
end Kuu.F112.Physical
