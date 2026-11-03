import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5ARContextUnitParityNormalForm
import Mathlib.Tactic

/-!
F112-P94D3GK5AS — exact local-to-global source-vertex
four-cell comparison obstruction and a zero-grade no-descent test.

GK5AQ proved a genuine original P89→selected P94A nonreflection
BadPair iff failure of the original four-class map's injectivity.
GK5AR proved EVERY selected P94A four-cell's two context primitive
count parities are endpoint determined, but these source-provenance
grades DO NOT imply original-F55 evidence recoverability.

We now isolate a FINITE SOURCE-VERTEX comparison chain whose
vertices are original F55 Type-valued 3-proof terms (not merely
C60 shadows or selected P92B quotient classes). Each edge carries
a genuine P94A four-cell between the GK5AI structural phi-images.
The chain itself gives a selected P94A comparison. By induction,
each such chain either reflects its endpoints to a P89 4-cell OR
contains an actual source-typed nonreflecting P94A edge. Hence
every bad pair obstructs every source-vertex chain between its
endpoints at SOME local step. This does NOT assert arbitrary
P94A proof terms decompose into source-vertex-saturated substeps:
their intermediate selected P92B evidence can be outside phi.

Separately, for the GENUINE north C60 three-stage unit
assocNaturality P92B witness with NO original F55 preimage,
every P94A endomorphism 4-cell has ZERO left/right context-unit
parity by GK5AR, and an explicit reflexive such 4-cell exists.
Consequently grade (0,0) does NOT imply source preimage or descent.
This is not a counterexample to original P89→P94A injectivity:
the missing original source is not a pair of original F55 proofs.

Keep all original P89/P93/P94A signatures unchanged, genuine
F54 two-Nat histories and proof authority uncollapsed.
No new logical axioms, sorry/admit/native_decide, Gray, global
gluing, or unconditional nonfaithfulness. Independent Kuu→Qi,
strict 空 authority, public root107, protected #1558 Draft/open.
Lean v4.30.0-rc2 / mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
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

/-- Actual source-vertex finite selected comparison chain.
The intermediate VERTICES are original F55 3-proof histories.
Edges are freely selected P94A 4-cell evidence: no false
assumption that each edge is already original P89 reflectable. -/
inductive NativeGK5ASSourceVertexChain
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last} :
    (KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) → (KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) →
    Type (max (max uD uE) (max vD vE)) where
  | nil (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
      NativeGK5ASSourceVertexChain f f
  | step {f g h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
      (selected : NativeF55P94UnitFourCell
        (nativeGK5AIOriginalToP92Structural f)
        (nativeGK5AIOriginalToP92Structural g))
      (tail : NativeGK5ASSourceVertexChain g h) :
      NativeGK5ASSourceVertexChain f h

/-- A genuine selected P94A comparison is built by vertical
composition of all actual links of a source-vertex chain. -/
def NativeGK5ASSourceVertexChain.toSelected
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
    (chain : NativeGK5ASSourceVertexChain f g) :
    NativeF55P94UnitFourCell
      (nativeGK5AIOriginalToP92Structural f)
      (nativeGK5AIOriginalToP92Structural g) := by
  induction chain with
  | nil f => exact .refl _
  | step w tail ih => exact .trans w ih

/-- A precisely localized selected comparison edge that has
NO original P89 four-cell source comparison. This is Prop-valued
but the offending P94A proof itself remains genuinely Type-valued. -/
inductive NativeGK5ASSourceVertexChain.HasBadStep
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last} :
    {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s} →
      NativeGK5ASSourceVertexChain f g → Prop where
  | atHead {f g h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
      (w : NativeF55P94UnitFourCell
        (nativeGK5AIOriginalToP92Structural f)
        (nativeGK5AIOriginalToP92Structural g))
      (tail : NativeGK5ASSourceVertexChain g h)
      (missing : ¬ Nonempty (NativeF55P89InterchangeFourCell f g)) :
      NativeGK5ASSourceVertexChain.HasBadStep
        (NativeGK5ASSourceVertexChain.step w tail)
  | inTail {f g h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
      (w : NativeF55P94UnitFourCell
        (nativeGK5AIOriginalToP92Structural f)
        (nativeGK5AIOriginalToP92Structural g))
      (tail : NativeGK5ASSourceVertexChain g h)
      (bad : NativeGK5ASSourceVertexChain.HasBadStep tail) :
      NativeGK5ASSourceVertexChain.HasBadStep
        (NativeGK5ASSourceVertexChain.step w tail)

/-- Local-to-global source reflection or an ACTUAL offending step.
No assumption of global P89 faithfulness, and no chosen normal form. -/
theorem NativeGK5ASSourceVertexChain.reflects_or_badStep
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
    (chain : NativeGK5ASSourceVertexChain f g) :
    Nonempty (NativeF55P89InterchangeFourCell f g) ∨
      chain.HasBadStep := by
  induction chain with
  | nil f =>
      exact .inl ⟨.refl f⟩
  | step (f := leftSource) (g := rightSource) w tail ih =>
      by_cases hlocal :
          Nonempty (NativeF55P89InterchangeFourCell leftSource rightSource)
      · rcases ih with hrest | hbad
        · rcases hlocal with ⟨hfg⟩
          rcases hrest with ⟨hgh⟩
          exact .inl ⟨.trans hfg hgh⟩
        · exact .inr (.inTail w tail hbad)
      · exact .inr (.atHead w tail hlocal)

/-- Absence of any locally nonreflecting source-vertex link
is a sufficient and unconditional proof of original P89
comparison between the endpoint F55 proof histories. -/
theorem NativeGK5ASSourceVertexChain.reflects_of_no_badStep
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
    (chain : NativeGK5ASSourceVertexChain f g)
    (h : ¬ chain.HasBadStep) :
    Nonempty (NativeF55P89InterchangeFourCell f g) :=
  (chain.reflects_or_badStep).resolve_right h

/-- Every genuinely typed nonreflection bad pair forces an
offending local edge in ANY selected source-vertex chain between
those two ORIGINAL F55 endpoints, whenever such a chain is given. -/
theorem NativeGK5ASSourceVertexChain.badPair_forces_badStep
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
    (chain : NativeGK5ASSourceVertexChain f g)
    (h : nativeGK5AQBadPair first last f g) :
    chain.HasBadStep := by
  rcases chain.reflects_or_badStep with hsource | hbad
  · exact False.elim (h.2 hsource)
  · exact hbad

/-- An offending local edge always supplies a genuine global
GK5AQ-style BAD PAIR for SOME ORIGINAL F55 source proof terms,
not just numerical C60 shadows or an arbitrary P92B 3-cell. -/
theorem NativeGK5ASSourceVertexChain.HasBadStep.exists_badPair
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
    {chain : NativeGK5ASSourceVertexChain f g}
    (h : chain.HasBadStep) :
    ∃ u v : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s,
      nativeGK5AQBadPair first last u v := by
  induction h with
  | atHead w tail missing =>
      exact ⟨_, _, ⟨⟨w⟩, missing⟩⟩
  | inTail w tail bad ih =>
      exact ih

/-- Full P89→P94A injectivity is EQUIVALENT to no bad edge
in ANY finite selected chain whose vertices have TRUE original
F55 proof histories. This is an exact GENERATOR-LOCAL GATE,
NOT the assertion that arbitrary selected 4-cells are already
decomposed into source-saturated primitive normal forms. -/
theorem nativeGK5ASAllSourceVertexChains_noBad_iff_injective
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (r s : KuuNativeF45Tree.DepthRotationRoute p first last) :
    (∀ {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
        (chain : NativeGK5ASSourceVertexChain f g),
      ¬ chain.HasBadStep) ↔
    Function.Injective
      (nativeGK5ANP89ToP94FourClassMap first last r s) := by
  constructor
  · intro hno
    apply (nativeGK5ANP89ToP94_injective_iff_reflect first last r s).2
    intro f g hselected
    by_contra hsource
    rcases hselected with ⟨w⟩
    let chain : NativeGK5ASSourceVertexChain f g :=
      .step w (.nil g)
    exact hno chain (.atHead w (.nil g) hsource)
  · intro hinj f g chain hbad
    rcases hbad.exists_badPair with ⟨u, v, h⟩
    exact h.2
      ((nativeGK5ANP89ToP94_injective_iff_reflect first last r s).1
        hinj u v h.1)

/-- Exactly the original F55 source evidence type for the real
north C60 first-three-F45 unit associator-naturality slot. -/
private abbrev nativeGK5ASNorthOriginalUnitAssoc :=
  NativeF55P90AssocNaturalityCell
    (nativeF54P92UnitRoute northNativeF45FirstStage)
    (nativeF54P92UnitRoute northNativeF45SecondStage)
    (nativeF54P92UnitRoute northNativeF45ThirdStage)

/-- An ACTUAL selected 4-cell on the new, unliftable P92B
assocNaturality three-proof: P94A reflexivity, no fake original. -/
def nativeGK5ASNorthAssocIdentityFour :
    NativeF55P94UnitFourCell
      nativeGK5AINorthAddedUnitAssocCell
      nativeGK5AINorthAddedUnitAssocCell :=
  .refl nativeGK5AINorthAddedUnitAssocCell

/-- All P94A four-cell histories looping at the selected added
assocNaturality have zero left AND zero right context-unit
parity. This follows from GK5AR on true Type-valued endpoints. -/
theorem nativeGK5ASNorthAssocLoop_zeroGrade
    (w : NativeF55P94UnitFourCell
      nativeGK5AINorthAddedUnitAssocCell
      nativeGK5AINorthAddedUnitAssocCell) :
    (((w.gk5apLeftUnitCount : Nat) : ZMod 2) = 0) ∧
    (((w.gk5apRightUnitCount : Nat) : ZMod 2) = 0) := by
  have h := w.gk5arContextParity_normalForm
  simp only [sub_self] at h
  exact ⟨congrArg Prod.fst h, congrArg Prod.snd h⟩

/-- Concrete obstruction to using the zero-grade criterion as a
surrogate for genuine original-F55 source preimage. An actual
P94A 4-cell exists with grade (0,0), but its P92B 3-cell endpoint
has NO original F55 preimage. This is not a P89 BAD PAIR. -/
theorem nativeGK5ASNorthZeroGrade_not_sourceRecovery :
    Nonempty (NativeF55P94UnitFourCell
      nativeGK5AINorthAddedUnitAssocCell
      nativeGK5AINorthAddedUnitAssocCell) ∧
    (∀ w : NativeF55P94UnitFourCell
      nativeGK5AINorthAddedUnitAssocCell
      nativeGK5AINorthAddedUnitAssocCell,
      (((w.gk5apLeftUnitCount : Nat) : ZMod 2) = 0) ∧
      (((w.gk5apRightUnitCount : Nat) : ZMod 2) = 0)) ∧
    (¬ ∃ old : nativeGK5ASNorthOriginalUnitAssoc,
      nativeGK5AIOriginalToP92Structural old =
        nativeGK5AINorthAddedUnitAssocCell) := by
  exact ⟨⟨nativeGK5ASNorthAssocIdentityFour⟩,
    nativeGK5ASNorthAssocLoop_zeroGrade,
    fun ⟨old, heq⟩ =>
      nativeGK5AINorthAddedUnitAssoc_noOriginalPreimage ⟨old, heq⟩⟩

#print axioms NativeGK5ASSourceVertexChain.toSelected
#print axioms NativeGK5ASSourceVertexChain.reflects_or_badStep
#print axioms NativeGK5ASSourceVertexChain.reflects_of_no_badStep
#print axioms NativeGK5ASSourceVertexChain.badPair_forces_badStep
#print axioms NativeGK5ASSourceVertexChain.HasBadStep.exists_badPair
#print axioms nativeGK5ASAllSourceVertexChains_noBad_iff_injective
#print axioms nativeGK5ASNorthAssocIdentityFour
#print axioms nativeGK5ASNorthAssocLoop_zeroGrade
#print axioms nativeGK5ASNorthZeroGrade_not_sourceRecovery

end
end Kuu.F112.Physical
