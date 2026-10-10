import KUOS.DependentOriginationCoherentBiadjunctionFiniteComparisonChainConcatenationV5_123
import Mathlib.CategoryTheory.Functor.FullyFaithful

namespace KUOS.DependentOriginationCoherentBiadjunctionComparisonCompressionFunctorV5_124

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionArbitraryModificationMatesV5_113.Generic
open KUOS.DependentOriginationCoherentBiadjunctionAutomaticModificationMatesV5_114.Generic
open KUOS.DependentOriginationCoherentBiadjunctionBiComparisonMateNaturalityV5_119.Generic
open KUOS.DependentOriginationCoherentBiadjunctionFiniteMateComparisonChainsV5_122.Generic
open KUOS.DependentOriginationCoherentBiadjunctionFiniteComparisonChainConcatenationV5_123.Generic

set_option autoImplicit false
noncomputable section

/-!
# F27 / v5.124: finite comparison paths form a genuine compression functor

F26 constructs an ordinary category whose morphisms are entire dependent
finite F/G comparison paths. Here we construct a SECOND ordinary category
whose morphisms retain only the actual composite F 2-ISO and the actual
composite G 2-cell, with no invertibility imposed on G.

The compression is a REAL FUNCTOR from the original unquotiented F26
path category into the composite-2-cell category. It preserves actual
identities and concatenation. The functor is FULL: every composite pair
has a genuine singleton comparison path. No claim of faithfulness is
made: distinct intermediate presentations may have the same composite.

F25/F22 mate naturality descends to the compressed arrows: equality
of functor images implies equality of BOTH genuine pasted mate boundaries,
for the unchanged original chosen objectwise adjunctions and lax mates.
No strictification or new biequivalence is asserted.
-/

namespace Generic

universe uB vB wB uC vC wC
variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]

/-- The composite-presentation object has the SAME original pair of
parallel 1-cells as its corresponding F26 path-category object. -/
structure CompositeComparisonPair (aF bF aG bG : C) where
  fF : aF ⟶ bF
  fG : aG ⟶ bG

/-- Hom = (genuine F 2-ISO, arbitrary G 2-cell). This is the category
of actual composite comparison pairs, not an equality quotient of paths. -/
instance compositeComparisonPairCategory (aF bF aG bG : C) :
    Category (CompositeComparisonPair aF bF aG bG) where
  Hom a b := (a.fF ≅ b.fF) × (a.fG ⟶ b.fG)
  id a := (Iso.refl a.fF, 𝟙 a.fG)
  comp f g := (f.1.trans g.1, f.2 ≫ g.2)
  id_comp f := by
    rcases f with ⟨p, q⟩
    apply Prod.ext
    · exact Iso.refl_trans p
    · exact Category.id_comp q
  comp_id f := by
    rcases f with ⟨p, q⟩
    apply Prod.ext
    · exact Iso.trans_refl p
    · exact Category.comp_id q
  assoc f g h := by
    rcases f with ⟨p, q⟩
    rcases g with ⟨t, r⟩
    rcases h with ⟨u, s⟩
    apply Prod.ext
    · exact Iso.trans_assoc p t u
    · exact Category.assoc q r s

/-- An actual functor from full F26 dependent chains to their genuine
F ISO / arbitrary G 2-cell composites. Objects retain the same cells. -/
def comparisonCompressionFunctor (aF bF aG bG : C) :
    ComparisonPair aF bF aG bG ⥤ CompositeComparisonPair aF bF aG bG where
  obj a := ⟨a.fF, a.fG⟩
  map {_ _} c := (c.fComposite, c.gComposite)
  map_id _ := rfl
  map_comp f g := by
    change
      ((Chains.append f g).fComposite, (Chains.append f g).gComposite) =
        (f.fComposite.trans g.fComposite, f.gComposite ≫ g.gComposite)
    exact Prod.ext (Chains.fComposite_append f g) (Chains.gComposite_append f g)

/-- Every genuine compressed F-ISO/G-cell pair has a one-step lift to
the unquotiented F26 finite path category; no inverse for G. -/
def singletonLift (aF bF aG bG : C)
    {a b : ComparisonPair aF bF aG bG}
    (p : a.fF ≅ b.fF) (q : a.fG ⟶ b.fG) : a ⟶ b :=
  BiComparisonChain.snoc BiComparisonChain.nil p q

/-- The compressed image of a singleton lift is literally its given
pair of 2-cells, with no additional comparison hypothesis. -/
theorem comparisonCompressionFunctor_map_singleton
    (aF bF aG bG : C)
    {a b : ComparisonPair aF bF aG bG}
    (p : a.fF ≅ b.fF) (q : a.fG ⟶ b.fG) :
    (comparisonCompressionFunctor aF bF aG bG).map
        (singletonLift aF bF aG bG p q) = (p, q) := by
  change ((Iso.refl a.fF).trans p, (𝟙 a.fG) ≫ q) = (p, q)
  simp only [Iso.refl_trans, Category.id_comp]

/-- Compression is genuinely FULL (surjective on every 2-Hom):
every F ISO and arbitrary G 2-cell has a singleton-chain preimage. -/
instance comparisonCompressionFunctorFull (aF bF aG bG : C) :
    (comparisonCompressionFunctor aF bF aG bG).Full where
  map_surjective := by
    intro a b p
    rcases p with ⟨i, q⟩
    exact ⟨singletonLift aF bF aG bG i q,
      comparisonCompressionFunctor_map_singleton aF bF aG bG i q⟩

/-- Equality of compressed FUNCTOR images is precisely equality of
both original composites, not equality of intermediate paths. -/
theorem comparisonCompressionFunctor_map_eq_iff
    (aF bF aG bG : C)
    {a b : ComparisonPair aF bF aG bG}
    (c₁ c₂ : a ⟶ b) :
    (comparisonCompressionFunctor aF bF aG bG).map c₁ =
        (comparisonCompressionFunctor aF bF aG bG).map c₂ ↔
      c₁.fComposite = c₂.fComposite ∧ c₁.gComposite = c₂.gComposite := by
  constructor
  · intro h
    change (c₁.fComposite, c₁.gComposite) =
      (c₂.fComposite, c₂.gComposite) at h
    exact ⟨congrArg Prod.fst h, congrArg Prod.snd h⟩
  · rintro ⟨hp, hq⟩
    change (c₁.fComposite, c₁.gComposite) =
      (c₂.fComposite, c₂.gComposite)
    exact Prod.ext hp hq

#print axioms CompositeComparisonPair
#print axioms compositeComparisonPairCategory
#print axioms comparisonCompressionFunctor
#print axioms singletonLift
#print axioms comparisonCompressionFunctor_map_singleton
#print axioms comparisonCompressionFunctorFull
#print axioms comparisonCompressionFunctor_map_eq_iff

variable {F G : Pseudofunctor B C}
variable {σ θ : Pseudofunctor.StrongTrans F G}

/-- The original mate's left boundary depends only on an ACTUAL
compressed pair of comparison 2-cells, not on its finite path. -/
def compressedMateLeftBoundary
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    {X Y : B} (f : X ⟶ Y)
    {kF : F.obj X ⟶ F.obj Y} {kG : G.obj X ⟶ G.obj Y}
    (pq : (F.map f ≅ kF) × (G.map f ⟶ kG)) :=
  (((rightModification dσ dθ Γ).app X ▷ kF ≫
      dσ.right.app X ◁ pq.1.inv) ≫
    dσ.right.naturality f) ≫ pq.2 ▷ dσ.right.app Y

/-- The opposite genuine mate boundary also depends only on the
same compressed comparison pair, preserving outer whiskering. -/
def compressedMateRightBoundary
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    {X Y : B} (f : X ⟶ Y)
    {kF : F.obj X ⟶ F.obj Y} {kG : G.obj X ⟶ G.obj Y}
    (pq : (F.map f ≅ kF) × (G.map f ⟶ kG)) :=
  (((dθ.right.app X ◁ pq.1.inv ≫ dθ.right.naturality f) ≫
      pq.2 ▷ dθ.right.app Y) ≫
    kG ◁ (rightModification dσ dθ Γ).app Y)

/-- The original F22 naturality descends on the actual compressed
Hom-pair, without invertibility assumptions on the G 2-cell. -/
theorem compressedMateNaturality
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    {X Y : B} (f : X ⟶ Y)
    {kF : F.obj X ⟶ F.obj Y} {kG : G.obj X ⟶ G.obj Y}
    (pq : (F.map f ≅ kF) × (G.map f ⟶ kG)) :
    compressedMateLeftBoundary dσ dθ Γ f pq =
      compressedMateRightBoundary dσ dθ Γ f pq := by
  rcases pq with ⟨p, q⟩
  exact globalConjugateBiComparisonNaturality dσ dθ Γ f p q

/-- Every F25 left finite-path boundary factors through the composite
F ISO/G 2-cell (the actual arrow mapped by compression). -/
theorem finiteLeftBoundary_factorsThroughCompression
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    {X Y : B} (f : X ⟶ Y)
    {kF : F.obj X ⟶ F.obj Y} {kG : G.obj X ⟶ G.obj Y}
    (c : BiComparisonChain (F.map f) (G.map f) kF kG) :
    finiteLeftBoundary dσ dθ Γ f c =
      compressedMateLeftBoundary dσ dθ Γ f (c.fComposite, c.gComposite) := by
  exact finiteLeftBoundary_normalize dσ dθ Γ f c

/-- The F25 right finite-path boundary independently factors through
the SAME composite pair; the original outer G whisker is retained. -/
theorem finiteRightBoundary_factorsThroughCompression
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    {X Y : B} (f : X ⟶ Y)
    {kF : F.obj X ⟶ F.obj Y} {kG : G.obj X ⟶ G.obj Y}
    (c : BiComparisonChain (F.map f) (G.map f) kF kG) :
    finiteRightBoundary dσ dθ Γ f c =
      compressedMateRightBoundary dσ dθ Γ f (c.fComposite, c.gComposite) := by
  exact finiteRightBoundary_normalize dσ dθ Γ f c

/-- A direct descent statement from equality of arrows UNDER THE
ACTUAL compression functor to equality of both original mate pastings.
The two finite paths need not have the same intermediate presentation
or depth; their final F/G composite cells are equal, no G inverse. -/
theorem finiteMateBoundaries_eq_of_compression_map_eq
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    {X Y : B} (f : X ⟶ Y)
    {kF : F.obj X ⟶ F.obj Y} {kG : G.obj X ⟶ G.obj Y}
    (c₁ c₂ : BiComparisonChain (F.map f) (G.map f) kF kG)
    (h : (comparisonCompressionFunctor (F.obj X) (F.obj Y)
        (G.obj X) (G.obj Y)).map
          (X := ⟨F.map f, G.map f⟩) (Y := ⟨kF, kG⟩) c₁ =
        (comparisonCompressionFunctor (F.obj X) (F.obj Y)
        (G.obj X) (G.obj Y)).map
          (X := ⟨F.map f, G.map f⟩) (Y := ⟨kF, kG⟩) c₂) :
    finiteLeftBoundary dσ dθ Γ f c₁ =
      finiteLeftBoundary dσ dθ Γ f c₂ ∧
    finiteRightBoundary dσ dθ Γ f c₁ =
      finiteRightBoundary dσ dθ Γ f c₂ := by
  have hPairs : (c₁.fComposite, c₁.gComposite) =
      (c₂.fComposite, c₂.gComposite) := h
  exact finiteBiComparisonFactorizationIndependent dσ dθ Γ f c₁ c₂
    (congrArg Prod.fst hPairs) (congrArg Prod.snd hPairs)

#print axioms compressedMateLeftBoundary
#print axioms compressedMateRightBoundary
#print axioms compressedMateNaturality
#print axioms finiteLeftBoundary_factorsThroughCompression
#print axioms finiteRightBoundary_factorsThroughCompression
#print axioms finiteMateBoundaries_eq_of_compression_map_eq

end Generic

end

end KUOS.DependentOriginationCoherentBiadjunctionComparisonCompressionFunctorV5_124
