import KUOS.DependentOriginationGrayC60OriginalFacePentagonTransportV5_201

namespace KUOS.DependentOriginationGrayC60OriginalFaceFourAssociatorPentagonV5_202

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayNativeBraidedCategoryV5_156
open KUOS.DependentOriginationGrayC60PresentedFaceTwoCellsV5_190
open KUOS.DependentOriginationGrayC60PresentedInterchangerV5_191
open KUOS.DependentOriginationGrayC60OriginalFaceHorizontalPresentationV5_199
open KUOS.DependentOriginationGrayC60OriginalFaceHorizontalThreeHomV5_199
open KUOS.DependentOriginationGrayC60OriginalFaceAssociatorPresentationV5_200
open KUOS.DependentOriginationGrayC60OriginalFaceAssociatorThreeHomV5_200
open KUOS.DependentOriginationGrayC60OriginalFaceAssociatorNaturalityV5_200
open KUOS.DependentOriginationGrayC60OriginalFacePentagonTransportV5_201

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# v5.202 / F59-F53-B: full source-typed four-F42 associator pentagon

Unlike the v5.201 pentagon of equality PROOFS between one-paths, this
module constructs the two different composites of three-dimensional
source associators as ACTUAL PARALLEL 3-arrows between the same two
original F42 face witness terms, indexed by the two real C60 paths.

The short route uses TWO of the explicitly ADJOINED F52 associators.
The long route uses THREE, including genuine horizontal context and
dependent transports on both physical one-path boundaries.
Both are proved equal in the existing FULL-native-kernel F52 3-Hom;
the original raw F42 source 2-cell witnesses remain distinct objects.
This quotient theorem is NOT a raw-word syntactic equality, and does
not invent old F43 or original F55 associator primitives.
-/

/-- Consecutive dependent transports can be composed without erasing
the ORIGINAL F42 face 2-cell whose path indices are being changed. -/
theorem c60F53BReindexFace_comp
    {a b : IcosahedralDart}
    {p q p' q' p'' q'' : Quiver.Path a b}
    (hp₁ : p = p') (hq₁ : q = q')
    (hp₂ : p' = p'') (hq₂ : q' = q'')
    (α : C60F42PresentedFaceCell p q) :
    c60F52ReindexFace hp₂ hq₂ (c60F52ReindexFace hp₁ hq₁ α) =
      c60F52ReindexFace (hp₁.trans hp₂) (hq₁.trans hq₂) α := by
  cases hp₁
  cases hq₁
  cases hp₂
  cases hq₂
  rfl

theorem c60F53BReindexFace_proofIrrel
    {a b : IcosahedralDart}
    {p q p' q' : Quiver.Path a b}
    (hp hp' : p = p') (hq hq' : q = q')
    (α : C60F42PresentedFaceCell p q) :
    c60F52ReindexFace hp hq α =
      c60F52ReindexFace hp' hq' α := by
  rw [Subsingleton.elim hp hp', Subsingleton.elim hq hq']

/-- Whisker a reindexed original face on the RIGHT. The original
F42 term itself is never replaced by a mere Gray grade. -/
theorem c60F53BHorizontal_reindexLeft
    {a b c : IcosahedralDart}
    {p q p' q' : Quiver.Path a b}
    {r s : Quiver.Path b c}
    (hp : p = p') (hq : q = q')
    (α : C60F42PresentedFaceCell p q)
    (β : C60F42PresentedFaceCell r s) :
    (c60F52ReindexFace hp hq α).horizontalLeftFirst β =
      c60F52ReindexFace
        (congrArg (fun x : Quiver.Path a b => x.comp r) hp)
        (congrArg (fun x : Quiver.Path a b => x.comp s) hq)
        (α.horizontalLeftFirst β) := by
  cases hp
  cases hq
  rfl

/-- Whisker a reindexed original face on the LEFT. -/
theorem c60F53BHorizontal_reindexRight
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b}
    {r s r' s' : Quiver.Path b c}
    (hr : r = r') (hs : s = s')
    (α : C60F42PresentedFaceCell p q)
    (β : C60F42PresentedFaceCell r s) :
    α.horizontalLeftFirst (c60F52ReindexFace hr hs β) =
      c60F52ReindexFace
        (congrArg (fun x : Quiver.Path b c => p.comp x) hr)
        (congrArg (fun x : Quiver.Path b c => q.comp x) hs)
        (α.horizontalLeftFirst β) := by
  cases hr
  cases hs
  rfl

/-- A source 3-word equipped with the PROVED fact of zero full-native
charge and exchange phase. This is a proof-carrying construction, not
a new axiom and not a new original F43 syntax constructor. -/
structure C60F53BZeroCell
    {a b : IcosahedralDart} {p q : Quiver.Path a b}
    (α β : C60F42PresentedFaceCell p q) where
  raw : C60F52PresentedThreeCell α β
  zero : raw.toNative = (0 : GradedThreeCell 0 0)

def c60F53BZeroIdentity
    {a b : IcosahedralDart} {p q : Quiver.Path a b}
    (α : C60F42PresentedFaceCell p q) :
    C60F53BZeroCell α α :=
  ⟨.ident α, rfl⟩

def c60F53BZeroAssociator
    {a b c d : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    {t u : Quiver.Path c d}
    (α : C60F42PresentedFaceCell p q)
    (β : C60F42PresentedFaceCell r s)
    (γ : C60F42PresentedFaceCell t u) :
    C60F53BZeroCell
      ((α.horizontalLeftFirst β).horizontalLeftFirst γ)
      (c60F52AssocRight α β γ) :=
  ⟨.associator α β γ, rfl⟩

def c60F53BZeroHorizontal
    {a b c : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    {α α' : C60F42PresentedFaceCell p q}
    {β β' : C60F42PresentedFaceCell r s}
    (f : C60F53BZeroCell α α')
    (g : C60F53BZeroCell β β') :
    C60F53BZeroCell
      (α.horizontalLeftFirst β)
      (α'.horizontalLeftFirst β') :=
  ⟨.horizontal f.raw g.raw, by
    change f.raw.toNative + g.raw.toNative =
      (0 : GradedThreeCell 0 0)
    rw [f.zero, g.zero]
    exact zero_add _⟩

def c60F53BZeroReindex
    {a b : IcosahedralDart}
    {p q p' q' : Quiver.Path a b}
    (hp : p = p') (hq : q = q')
    {α β : C60F42PresentedFaceCell p q}
    (f : C60F53BZeroCell α β) :
    C60F53BZeroCell
      (c60F52ReindexFace hp hq α)
      (c60F52ReindexFace hp hq β) :=
  ⟨.reindex hp hq f.raw, f.zero⟩

def c60F53BZeroTrans
    {a b : IcosahedralDart} {p q : Quiver.Path a b}
    {α β γ : C60F42PresentedFaceCell p q}
    (f : C60F53BZeroCell α β)
    (g : C60F53BZeroCell β γ) :
    C60F53BZeroCell α γ :=
  ⟨.trans f.raw g.raw, by
    change f.raw.toNative + g.raw.toNative =
      (0 : GradedThreeCell 0 0)
    rw [f.zero, g.zero]
    exact zero_add _⟩

/-- Equality casts here change only a CERTIFIED EQUAL source
witness; they never identify arbitrary distinct F42 terms. -/
def c60F53BZeroChangeSource
    {a b : IcosahedralDart} {p q : Quiver.Path a b}
    {α β γ : C60F42PresentedFaceCell p q}
    (h : α = γ) (f : C60F53BZeroCell α β) :
    C60F53BZeroCell γ β := by
  cases h
  exact f

def c60F53BZeroChangeTarget
    {a b : IcosahedralDart} {p q : Quiver.Path a b}
    {α β γ : C60F42PresentedFaceCell p q}
    (h : β = γ) (f : C60F53BZeroCell α β) :
    C60F53BZeroCell α γ := by
  cases h
  exact f

/-- The common FULLY LEFT ASSOCIATED original F42 2-cell term. -/
def c60F53BFourLeft
    {a b c d e : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    {t u : Quiver.Path c d} {v w : Quiver.Path d e}
    (α : C60F42PresentedFaceCell p q)
    (β : C60F42PresentedFaceCell r s)
    (γ : C60F42PresentedFaceCell t u)
    (δ : C60F42PresentedFaceCell v w) :
    C60F42PresentedFaceCell
      (((p.comp r).comp t).comp v)
      (((q.comp s).comp u).comp w) :=
  (((α.horizontalLeftFirst β).horizontalLeftFirst γ).horizontalLeftFirst δ)

/-- The common FULLY RIGHT ASSOCIATED original witness, cast
to the identical pair of actual left-associated physical paths. -/
def c60F53BFourRight
    {a b c d e : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    {t u : Quiver.Path c d} {v w : Quiver.Path d e}
    (α : C60F42PresentedFaceCell p q)
    (β : C60F42PresentedFaceCell r s)
    (γ : C60F42PresentedFaceCell t u)
    (δ : C60F42PresentedFaceCell v w) :
    C60F42PresentedFaceCell
      (((p.comp r).comp t).comp v)
      (((q.comp s).comp u).comp w) :=
  c60F52ReindexFace
    (c60F53PathPentagonLeft p r t v).symm
    (c60F53PathPentagonLeft q s u w).symm
    (α.horizontalLeftFirst
      (β.horizontalLeftFirst (γ.horizontalLeftFirst δ)))

/-- Two genuinely composable F52 3-associator moves:
((αβ)γ)δ -> (αβ)(γδ) -> α(β(γδ)).
The common final ORIGINAL proof term is NOT redefined as a grade. -/
def c60F53BPentagonShortZero
    {a b c d e : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    {t u : Quiver.Path c d} {v w : Quiver.Path d e}
    (α : C60F42PresentedFaceCell p q)
    (β : C60F42PresentedFaceCell r s)
    (γ : C60F42PresentedFaceCell t u)
    (δ : C60F42PresentedFaceCell v w) :
    C60F53BZeroCell
      (c60F53BFourLeft α β γ δ)
      (c60F53BFourRight α β γ δ) := by
  let hp := (Quiver.Path.comp_assoc (p.comp r) t v).symm
  let hq := (Quiver.Path.comp_assoc (q.comp s) u w).symm
  let f₁ := c60F53BZeroAssociator
    (α.horizontalLeftFirst β) γ δ
  let f₂ := c60F53BZeroReindex hp hq
    (c60F53BZeroAssociator α β (γ.horizontalLeftFirst δ))
  have ht :
      c60F52ReindexFace hp hq
        (c60F52AssocRight α β (γ.horizontalLeftFirst δ)) =
      c60F53BFourRight α β γ δ := by
    change
      c60F52ReindexFace hp hq
        (c60F52ReindexFace
          (Quiver.Path.comp_assoc p r (t.comp v)).symm
          (Quiver.Path.comp_assoc q s (u.comp w)).symm
          (α.horizontalLeftFirst
            (β.horizontalLeftFirst (γ.horizontalLeftFirst δ)))) =
      c60F52ReindexFace
        (c60F53PathPentagonLeft p r t v).symm
        (c60F53PathPentagonLeft q s u w).symm
        (α.horizontalLeftFirst
          (β.horizontalLeftFirst (γ.horizontalLeftFirst δ)))
    rw [c60F53BReindexFace_comp]
  exact c60F53BZeroTrans f₁ (c60F53BZeroChangeTarget ht f₂)

/-- Three genuinely composable F52 3-associator moves:
((αβ)γ)δ -> (α(βγ))δ -> α((βγ)δ) -> α(β(γδ)).
The last whiskering is performed on the REAL F42 right operand. -/
def c60F53BPentagonLongZero
    {a b c d e : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    {t u : Quiver.Path c d} {v w : Quiver.Path d e}
    (α : C60F42PresentedFaceCell p q)
    (β : C60F42PresentedFaceCell r s)
    (γ : C60F42PresentedFaceCell t u)
    (δ : C60F42PresentedFaceCell v w) :
    C60F53BZeroCell
      (c60F53BFourLeft α β γ δ)
      (c60F53BFourRight α β γ δ) := by
  let hp : ((p.comp (r.comp t)).comp v) =
      (((p.comp r).comp t).comp v) :=
    congrArg (fun x : Quiver.Path a d => x.comp v)
      (Quiver.Path.comp_assoc p r t).symm
  let hq : ((q.comp (s.comp u)).comp w) =
      (((q.comp s).comp u).comp w) :=
    congrArg (fun x : Quiver.Path a d => x.comp w)
      (Quiver.Path.comp_assoc q s u).symm
  let h₂p := (Quiver.Path.comp_assoc p (r.comp t) v).symm
  let h₂q := (Quiver.Path.comp_assoc q (s.comp u) w).symm
  let f₁ := c60F53BZeroHorizontal
    (c60F53BZeroAssociator α β γ)
    (c60F53BZeroIdentity δ)
  let f₂raw := c60F53BZeroReindex hp hq
    (c60F53BZeroAssociator α (β.horizontalLeftFirst γ) δ)
  have hs :
      c60F52ReindexFace hp hq
        ((α.horizontalLeftFirst (β.horizontalLeftFirst γ)).horizontalLeftFirst δ) =
      (c60F52AssocRight α β γ).horizontalLeftFirst δ := by
    simpa only [c60F52AssocRight] using
      (c60F53BHorizontal_reindexLeft
        (Quiver.Path.comp_assoc p r t).symm
        (Quiver.Path.comp_assoc q s u).symm
        (α.horizontalLeftFirst (β.horizontalLeftFirst γ)) δ).symm
  let f₂ := c60F53BZeroChangeSource hs f₂raw
  let f₃raw := c60F53BZeroReindex hp hq
    (c60F53BZeroReindex h₂p h₂q
      (c60F53BZeroHorizontal
        (c60F53BZeroIdentity α)
        (c60F53BZeroAssociator β γ δ)))
  have hr :
      α.horizontalLeftFirst (c60F52AssocRight β γ δ) =
      c60F52ReindexFace
        (congrArg (fun x : Quiver.Path b e => p.comp x)
          (Quiver.Path.comp_assoc r t v).symm)
        (congrArg (fun x : Quiver.Path b e => q.comp x)
          (Quiver.Path.comp_assoc s u w).symm)
        (α.horizontalLeftFirst
          (β.horizontalLeftFirst (γ.horizontalLeftFirst δ))) := by
    simpa only [c60F52AssocRight] using
      c60F53BHorizontal_reindexRight
        (Quiver.Path.comp_assoc r t v).symm
        (Quiver.Path.comp_assoc s u w).symm
        α (β.horizontalLeftFirst (γ.horizontalLeftFirst δ))
  have ht :
      c60F52ReindexFace hp hq
        (c60F52ReindexFace h₂p h₂q
          (α.horizontalLeftFirst (c60F52AssocRight β γ δ))) =
      c60F53BFourRight α β γ δ := by
    rw [hr]
    simp only [c60F53BReindexFace_comp]
    exact c60F53BReindexFace_proofIrrel _ _ _ _ _
  exact c60F53BZeroTrans f₁
    (c60F53BZeroTrans f₂ (c60F53BZeroChangeTarget ht f₃raw))

/-- Both routes are source-aware MORPHISMS of the SAME Mathlib
F52 3-Hom, between EXACTLY the original F42 endpoint witnesses. -/
def c60F53BPentagonShort
    {a b c d e : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    {t u : Quiver.Path c d} {v w : Quiver.Path d e}
    (α : C60F42PresentedFaceCell p q)
    (β : C60F42PresentedFaceCell r s)
    (γ : C60F42PresentedFaceCell t u)
    (δ : C60F42PresentedFaceCell v w) :
    C60F52Hom
      (⟨c60F53BFourLeft α β γ δ⟩ :
        C60F52OriginalTwo
          (((p.comp r).comp t).comp v)
          (((q.comp s).comp u).comp w))
      (⟨c60F53BFourRight α β γ δ⟩ :
        C60F52OriginalTwo
          (((p.comp r).comp t).comp v)
          (((q.comp s).comp u).comp w)) :=
  c60F52Of (c60F53BPentagonShortZero α β γ δ).raw

def c60F53BPentagonLong
    {a b c d e : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    {t u : Quiver.Path c d} {v w : Quiver.Path d e}
    (α : C60F42PresentedFaceCell p q)
    (β : C60F42PresentedFaceCell r s)
    (γ : C60F42PresentedFaceCell t u)
    (δ : C60F42PresentedFaceCell v w) :
    C60F52Hom
      (⟨c60F53BFourLeft α β γ δ⟩ :
        C60F52OriginalTwo
          (((p.comp r).comp t).comp v)
          (((q.comp s).comp u).comp w))
      (⟨c60F53BFourRight α β γ δ⟩ :
        C60F52OriginalTwo
          (((p.comp r).comp t).comp v)
          (((q.comp s).comp u).comp w)) :=
  c60F52Of (c60F53BPentagonLongZero α β γ δ).raw

/-- SOURCE-LEVEL four-factor Mac Lane pentagon in the honest
F42-witness-indexed F52 3-Hom QUOTIENT: 2-move and 3-move routes.
The zero evaluation is established compositionally for every
intermediate genuine typed F52 associator, not by equating raw words. -/
theorem c60F53BOriginalFourFacePentagon
    {a b c d e : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    {t u : Quiver.Path c d} {v w : Quiver.Path d e}
    (α : C60F42PresentedFaceCell p q)
    (β : C60F42PresentedFaceCell r s)
    (γ : C60F42PresentedFaceCell t u)
    (δ : C60F42PresentedFaceCell v w) :
    c60F53BPentagonShort α β γ δ =
      c60F53BPentagonLong α β γ δ := by
  apply c60F52Hom_ext
  change (c60F53BPentagonShortZero α β γ δ).raw.toNative =
    (c60F53BPentagonLongZero α β γ δ).raw.toNative
  rw [(c60F53BPentagonShortZero α β γ δ).zero,
    (c60F53BPentagonLongZero α β γ δ).zero]

theorem c60F53BPentagonShort_native
    {a b c d e : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    {t u : Quiver.Path c d} {v w : Quiver.Path d e}
    (α : C60F42PresentedFaceCell p q)
    (β : C60F42PresentedFaceCell r s)
    (γ : C60F42PresentedFaceCell t u)
    (δ : C60F42PresentedFaceCell v w) :
    c60F52Eval (c60F53BPentagonShort α β γ δ) =
      (0 : GradedThreeCell 0 0) :=
  (c60F53BPentagonShortZero α β γ δ).zero

theorem c60F53BPentagonLong_native
    {a b c d e : IcosahedralDart}
    {p q : Quiver.Path a b} {r s : Quiver.Path b c}
    {t u : Quiver.Path c d} {v w : Quiver.Path d e}
    (α : C60F42PresentedFaceCell p q)
    (β : C60F42PresentedFaceCell r s)
    (γ : C60F42PresentedFaceCell t u)
    (δ : C60F42PresentedFaceCell v w) :
    c60F52Eval (c60F53BPentagonLong α β γ δ) =
      (0 : GradedThreeCell 0 0) :=
  (c60F53BPentagonLongZero α β γ δ).zero

#print axioms c60F53BReindexFace_comp
#print axioms c60F53BReindexFace_proofIrrel
#print axioms c60F53BHorizontal_reindexLeft
#print axioms c60F53BHorizontal_reindexRight
#print axioms c60F53BPentagonShortZero
#print axioms c60F53BPentagonLongZero
#print axioms c60F53BOriginalFourFacePentagon
#print axioms c60F53BPentagonShort_native
#print axioms c60F53BPentagonLong_native

end
end KUOS.DependentOriginationGrayC60OriginalFaceFourAssociatorPentagonV5_202
