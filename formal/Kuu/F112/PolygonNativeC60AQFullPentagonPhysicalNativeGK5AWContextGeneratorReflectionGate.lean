import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5AVNestedVerticalSourceChain
import Mathlib.Tactic

/-!
F112-P94D3GK5AW — original P89 generator-wise source reflection gates
and exact localization of P94A/P89 nonreflection under source contexts.

GK5AU audited all 19 P94A and 16 embedded P93C selected constructors
for missing original F55 phi-images. GK5AV built an ACTUAL two-edge
source-vertex chain from the source-saturated selected vertical trans.

The present step addresses eight nonvertical generator families
ALREADY present in genuine original P89: left/right whisker,
left/right F45 context, F54 pre/postcompose, and left/right horizontal
whiskering. Given a TRUE original F55 source for the extra context,
original P89 reflection of the subcomparison produces a true original
P89 reflection of the contextualized comparison. Contrapositively,
a genuine selected P94A/P89 BadPair in one of these source-typed
contextualizations forces a BadPair in its actual inner comparison.
This is a source-typed obstruction LOCALIZATION, not a claim that
P89 comparison reflects automatically from P94A.

For selected P94A whisker and horizontal arguments we ALSO extract
the exact dependent original F55 phi-fiber from GK5AU full-history
source saturation; absence of these source fibers is an independent
obstruction, not a four-cell BadPair. The horizontal interchange
primitive is already a TRUE original P89 generator and cannot itself
be a GK5AQ BadPair on its original typed source pair. Its four
selected P92B argument slots are nonetheless all audited for
phi-membership in a source-saturated P94A interchange proof.

The three original P80 horizontal/left/right-context UNIT primitives
were already shown non-bad in GK5AQ. The NEW P93C generators and
remaining vertical units/associativity still need separate reflection
certificates; no universal 19-constructor normalization is claimed.

Preserve strict 空 authority; independent Kuu -> Qi, same public
root 107, original F54 two Nat/category/Blocks indices, protected
#1558 Draft/open. Additive only, Lean v4.30.0-rc2,
mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
No new axioms, sorry/admit/native_decide, Gray or global gluing.
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
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {p : Polygon} {a b : D} {x y : E}
variable {n n' m m' : Nat}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}
variable {first : KuuNativeF45Tree p n m ma pa mb pb}
variable {last : KuuNativeF45Tree p n' m' ma pa mb pb}

-- Every localization argument uses a REAL P89 constructor, never
-- an inferred old certificate from a numerical shadow or quotient.

/-- A genuine original-source left whisker CANNOT produce a new
nonreflection BadPair without a BadPair in its actual selected
four-cell subcomparison. -/
theorem nativeGK5AWLeftWhisker_bad_localizes
    {u v w : KuuNativeF45Tree.DepthRotationRoute p first last}
    (prior : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v)
    {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p v w}
    (selected : NativeF55P94UnitFourCell
      (nativeGK5AIOriginalToP92Structural f)
      (nativeGK5AIOriginalToP92Structural g))
    (parentBad : nativeGK5AQBadPair first last
      (.trans prior f) (.trans prior g)) :
    nativeGK5AQBadPair first last f g := by
  refine ⟨⟨selected⟩, ?_⟩
  rintro ⟨original⟩
  exact parentBad.2 ⟨.leftWhisker prior original⟩

/-- Exact right whisker localization, with an ORIGINAL suffix
three-proof, not an arbitrary selected P92B proof term. -/
theorem nativeGK5AWRightWhisker_bad_localizes
    {u v w : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v}
    (suffix : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p v w)
    (selected : NativeF55P94UnitFourCell
      (nativeGK5AIOriginalToP92Structural f)
      (nativeGK5AIOriginalToP92Structural g))
    (parentBad : nativeGK5AQBadPair first last
      (.trans f suffix) (.trans g suffix)) :
    nativeGK5AQBadPair first last f g := by
  refine ⟨⟨selected⟩, ?_⟩
  rintro ⟨original⟩
  exact parentBad.2 ⟨.rightWhisker original suffix⟩

/-- LEFT F45 binary context: original P89 leftContext transports
any inner original comparison, so parent nonreflection localizes. -/
theorem nativeGK5AWLeftContext_bad_localizes
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
    {k l : Nat}
    {mc : KuuNativeBlocks a b} {pc : KuuNativeBlocks x y}
    (later : KuuNativeF45Tree p k l mb pb mc pc)
    (selected : NativeF55P94UnitFourCell
      (nativeGK5AIOriginalToP92Structural f)
      (nativeGK5AIOriginalToP92Structural g))
    (parentBad : nativeGK5AQBadPair
      (KuuNativeF45Tree.node first later)
      (KuuNativeF45Tree.node last later)
      (.leftContext f later) (.leftContext g later)) :
    nativeGK5AQBadPair first last f g := by
  refine ⟨⟨selected⟩, ?_⟩
  rintro ⟨original⟩
  exact parentBad.2 ⟨.leftContext original later⟩

/-- RIGHT F45 binary context, preserving independent source and
target original F54 depth indices and category blocks. -/
theorem nativeGK5AWRightContext_bad_localizes
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
    {k l : Nat}
    {mc : KuuNativeBlocks a b} {pc : KuuNativeBlocks x y}
    (earlier : KuuNativeF45Tree p k l mc pc ma pa)
    (selected : NativeF55P94UnitFourCell
      (nativeGK5AIOriginalToP92Structural f)
      (nativeGK5AIOriginalToP92Structural g))
    (parentBad : nativeGK5AQBadPair
      (KuuNativeF45Tree.node earlier first)
      (KuuNativeF45Tree.node earlier last)
      (.rightContext earlier f) (.rightContext earlier g)) :
    nativeGK5AQBadPair first last f g := by
  refine ⟨⟨selected⟩, ?_⟩
  rintro ⟨original⟩
  exact parentBad.2 ⟨.rightContext earlier original⟩

/-- F54 route PREcomposition cannot create P89 nonreflection if
the inner genuine original F55 comparison already reflects. -/
theorem nativeGK5AWPrecompose_bad_localizes
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
    {k l : Nat}
    (before : KuuNativeF45Tree p k l ma pa mb pb)
    (prior : KuuNativeF45Tree.DepthRotationRoute p before first)
    (selected : NativeF55P94UnitFourCell
      (nativeGK5AIOriginalToP92Structural f)
      (nativeGK5AIOriginalToP92Structural g))
    (parentBad : nativeGK5AQBadPair before last
      (.precompose prior f) (.precompose prior g)) :
    nativeGK5AQBadPair first last f g := by
  refine ⟨⟨selected⟩, ?_⟩
  rintro ⟨original⟩
  exact parentBad.2 ⟨.precompose prior original⟩

/-- F54 route POSTcomposition: genuine original-source P89
postcomposition transfers every inner original four-proof. -/
theorem nativeGK5AWPostcompose_bad_localizes
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
    {k l : Nat}
    (after : KuuNativeF45Tree p k l ma pa mb pb)
    (suffix : KuuNativeF45Tree.DepthRotationRoute p last after)
    (selected : NativeF55P94UnitFourCell
      (nativeGK5AIOriginalToP92Structural f)
      (nativeGK5AIOriginalToP92Structural g))
    (parentBad : nativeGK5AQBadPair first after
      (.postcompose f suffix) (.postcompose g suffix)) :
    nativeGK5AQBadPair first last f g := by
  refine ⟨⟨selected⟩, ?_⟩
  rintro ⟨original⟩
  exact parentBad.2 ⟨.postcompose original suffix⟩

/-- LEFT horizontal source comparison: any obstruction of the
originally typed binary extension localizes to its left inner
P94A comparison when the right proof input is ORIGINAL F55. -/
theorem nativeGK5AWHorizontalLeft_bad_localizes
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
    {k k' l l' : Nat}
    {mc : KuuNativeBlocks a b} {pc : KuuNativeBlocks x y}
    {rightBefore : KuuNativeF45Tree p k l mb pb mc pc}
    {rightAfter : KuuNativeF45Tree p k' l' mb pb mc pc}
    {u v : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter}
    (other : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v)
    (selected : NativeF55P94UnitFourCell
      (nativeGK5AIOriginalToP92Structural f)
      (nativeGK5AIOriginalToP92Structural g))
    (parentBad : nativeGK5AQBadPair
      (KuuNativeF45Tree.node first rightBefore)
      (KuuNativeF45Tree.node last rightAfter)
      (f.horizontal other) (g.horizontal other)) :
    nativeGK5AQBadPair first last f g := by
  refine ⟨⟨selected⟩, ?_⟩
  rintro ⟨original⟩
  exact parentBad.2 ⟨.horizontalLeft original other⟩

/-- RIGHT horizontal source comparison: analogous localization
to the right inner edge, requiring an actual original left input. -/
theorem nativeGK5AWHorizontalRight_bad_localizes
    {k k' l l' : Nat}
    {mc : KuuNativeBlocks a b} {pc : KuuNativeBlocks x y}
    {rightBefore : KuuNativeF45Tree p k l mb pb mc pc}
    {rightAfter : KuuNativeF45Tree p k' l' mb pb mc pc}
    {u v : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter}
    {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u v}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (other : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s)
    (selected : NativeF55P94UnitFourCell
      (nativeGK5AIOriginalToP92Structural f)
      (nativeGK5AIOriginalToP92Structural g))
    (parentBad : nativeGK5AQBadPair
      (KuuNativeF45Tree.node first rightBefore)
      (KuuNativeF45Tree.node last rightAfter)
      (other.horizontal f) (other.horizontal g)) :
    nativeGK5AQBadPair rightBefore rightAfter f g := by
  refine ⟨⟨selected⟩, ?_⟩
  rintro ⟨original⟩
  exact parentBad.2 ⟨.horizontalRight other original⟩

/-! ## Exact source-fiber gates for the added SELECTED P92B inputs.
These inspect genuine P94A proof constructors under GK5AU's FULL
history saturation, not only the two outer proof endpoints. -/

/-- A source-saturated selected left-whisker four-proof requires
a genuine original F55 phi-preimage of its P92B prior input. -/
theorem nativeGK5AWLeftWhisker_prior_fiber
    {u v w : KuuNativeF45Tree.DepthRotationRoute p first last}
    (prior : NativeF55P92AssocComparison p u v)
    {f g : NativeF55P92AssocComparison p v w}
    (selected : NativeF55P94UnitFourCell f g)
    (clean : nativeGK5AUP94SourceSaturated
      (NativeF55P94UnitFourCell.leftWhisker prior selected)) :
    Nonempty (nativeGK5ATPhiFiber prior) := by
  apply (nativeGK5ATPhiImage_iff_fiber prior).mp
  by_contra missing
  exact clean (Or.inr (Or.inr (Or.inl missing)))

/-- A source-saturated right whisker requires an EXACT original
F55 preimage of the appended selected P92B suffix proof. -/
theorem nativeGK5AWRightWhisker_suffix_fiber
    {u v w : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55P92AssocComparison p u v}
    (selected : NativeF55P94UnitFourCell f g)
    (suffix : NativeF55P92AssocComparison p v w)
    (clean : nativeGK5AUP94SourceSaturated
      (NativeF55P94UnitFourCell.rightWhisker selected suffix)) :
    Nonempty (nativeGK5ATPhiFiber suffix) := by
  apply (nativeGK5ATPhiImage_iff_fiber suffix).mp
  by_contra missing
  exact clean (Or.inr (Or.inr (Or.inr missing)))

/-- A selected horizontal-left P94A operation cannot be fully
source-saturated unless its independently given RIGHT P92B proof
actually lies in the structural phi-image of original F55. -/
theorem nativeGK5AWHorizontalLeft_other_fiber
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55P92AssocComparison p r s}
    {k k' l l' : Nat}
    {mc : KuuNativeBlocks a b} {pc : KuuNativeBlocks x y}
    {rightBefore : KuuNativeF45Tree p k l mb pb mc pc}
    {rightAfter : KuuNativeF45Tree p k' l' mb pb mc pc}
    {u v : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter}
    (selected : NativeF55P94UnitFourCell f g)
    (other : NativeF55P92AssocComparison p u v)
    (clean : nativeGK5AUP94SourceSaturated
      (NativeF55P94UnitFourCell.horizontalLeft selected other)) :
    Nonempty (nativeGK5ATPhiFiber other) := by
  apply (nativeGK5ATPhiImage_iff_fiber other).mp
  by_contra missing
  exact clean (Or.inr (Or.inr (Or.inr missing)))

/-- The dual horizontal-right P94A operation likewise needs a
genuine F55 phi-fiber for the given LEFT selected P92B proof. -/
theorem nativeGK5AWHorizontalRight_other_fiber
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (other : NativeF55P92AssocComparison p r s)
    {k k' l l' : Nat}
    {mc : KuuNativeBlocks a b} {pc : KuuNativeBlocks x y}
    {rightBefore : KuuNativeF45Tree p k l mb pb mc pc}
    {rightAfter : KuuNativeF45Tree p k' l' mb pb mc pc}
    {u v : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter}
    {f g : NativeF55P92AssocComparison p u v}
    (selected : NativeF55P94UnitFourCell f g)
    (clean : nativeGK5AUP94SourceSaturated
      (NativeF55P94UnitFourCell.horizontalRight other selected)) :
    Nonempty (nativeGK5ATPhiFiber other) := by
  apply (nativeGK5ATPhiImage_iff_fiber other).mp
  by_contra missing
  exact clean (Or.inr (Or.inr (Or.inl missing)))

/-- In a SOURCE-SATURATED actual selected horizontal interchange
generator, all FOUR internal P92B 3-proof arguments have genuine
dependent original F55 phi-preimages, not just matching shadows. -/
theorem nativeGK5AWInterchange_four_internal_fibers
    {k k' l l' : Nat}
    {mc : KuuNativeBlocks a b} {pc : KuuNativeBlocks x y}
    {rightBefore : KuuNativeF45Tree p k l mb pb mc pc}
    {rightAfter : KuuNativeF45Tree p k' l' mb pb mc pc}
    {u₀ u₁ u₂ : KuuNativeF45Tree.DepthRotationRoute p first last}
    {v₀ v₁ v₂ : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter}
    (f₁ : NativeF55P92AssocComparison p u₀ u₁)
    (f₂ : NativeF55P92AssocComparison p u₁ u₂)
    (g₁ : NativeF55P92AssocComparison p v₀ v₁)
    (g₂ : NativeF55P92AssocComparison p v₁ v₂)
    (clean : nativeGK5AUP94SourceSaturated
      (NativeF55P94UnitFourCell.interchange f₁ f₂ g₁ g₂)) :
    Nonempty (nativeGK5ATPhiFiber f₁) ∧
    Nonempty (nativeGK5ATPhiFiber f₂) ∧
    Nonempty (nativeGK5ATPhiFiber g₁) ∧
    Nonempty (nativeGK5ATPhiFiber g₂) := by
  have hf₁ : nativeGK5ATPhiImage f₁ := by
    by_contra h
    exact clean (Or.inr (Or.inr (Or.inl h)))
  have hf₂ : nativeGK5ATPhiImage f₂ := by
    by_contra h
    exact clean (Or.inr (Or.inr (Or.inr (Or.inl h))))
  have hg₁ : nativeGK5ATPhiImage g₁ := by
    by_contra h
    exact clean (Or.inr (Or.inr (Or.inr (Or.inr (Or.inl h)))))
  have hg₂ : nativeGK5ATPhiImage g₂ := by
    by_contra h
    exact clean (Or.inr (Or.inr (Or.inr (Or.inr (Or.inr h)))))
  exact ⟨(nativeGK5ATPhiImage_iff_fiber f₁).mp hf₁,
    (nativeGK5ATPhiImage_iff_fiber f₂).mp hf₂,
    (nativeGK5ATPhiImage_iff_fiber g₁).mp hg₁,
    (nativeGK5ATPhiImage_iff_fiber g₂).mp hg₂⟩

/-- All four ORIGINAL F55 source proofs supply a real original
P89 interchange four-cell. Thus an interchange at THESE ORIGINAL
source endpoints cannot itself be a GK5AQ BadPair, regardless of
the selected P94A presentation's extra generating certificates. -/
theorem nativeGK5AWOriginalInterchange_reflects_not_bad
    {k k' l l' : Nat}
    {mc : KuuNativeBlocks a b} {pc : KuuNativeBlocks x y}
    {rightBefore : KuuNativeF45Tree p k l mb pb mc pc}
    {rightAfter : KuuNativeF45Tree p k' l' mb pb mc pc}
    {u₀ u₁ u₂ : KuuNativeF45Tree.DepthRotationRoute p first last}
    {v₀ v₁ v₂ : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter}
    (f₁ : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u₀ u₁)
    (f₂ : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p u₁ u₂)
    (g₁ : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p v₀ v₁)
    (g₂ : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p v₁ v₂) :
    Nonempty (NativeF55P89InterchangeFourCell
      ((KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans f₁ f₂).horizontal
        (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans g₁ g₂))
      (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans
        (f₁.horizontal g₁) (f₂.horizontal g₂))) ∧
    ¬ nativeGK5AQBadPair
      (KuuNativeF45Tree.node first rightBefore)
      (KuuNativeF45Tree.node last rightAfter)
      ((KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans f₁ f₂).horizontal
        (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans g₁ g₂))
      (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans
        (f₁.horizontal g₁) (f₂.horizontal g₂)) := by
  let original : NativeF55P89InterchangeFourCell
      ((KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans f₁ f₂).horizontal
        (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans g₁ g₂))
      (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans
        (f₁.horizontal g₁) (f₂.horizontal g₂)) :=
    .interchange f₁ f₂ g₁ g₂
  exact ⟨⟨original⟩, fun bad => bad.2 ⟨original⟩⟩

#print axioms nativeGK5AWLeftWhisker_bad_localizes
#print axioms nativeGK5AWRightWhisker_bad_localizes
#print axioms nativeGK5AWLeftContext_bad_localizes
#print axioms nativeGK5AWRightContext_bad_localizes
#print axioms nativeGK5AWPrecompose_bad_localizes
#print axioms nativeGK5AWPostcompose_bad_localizes
#print axioms nativeGK5AWHorizontalLeft_bad_localizes
#print axioms nativeGK5AWHorizontalRight_bad_localizes
#print axioms nativeGK5AWLeftWhisker_prior_fiber
#print axioms nativeGK5AWRightWhisker_suffix_fiber
#print axioms nativeGK5AWHorizontalLeft_other_fiber
#print axioms nativeGK5AWHorizontalRight_other_fiber
#print axioms nativeGK5AWInterchange_four_internal_fibers
#print axioms nativeGK5AWOriginalInterchange_reflects_not_bad

end
end Kuu.F112.Physical
