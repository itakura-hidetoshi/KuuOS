import KUOS.DependentOriginationCoherentBiadjunctionActualLiftCompressionV5_124
import Mathlib.Data.Quot

namespace KUOS.DependentOriginationCoherentBiadjunctionComparisonKernelHomQuotientV5_125

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionArbitraryModificationMatesV5_113.Generic
open KUOS.DependentOriginationCoherentBiadjunctionAutomaticModificationMatesV5_114.Generic
open KUOS.DependentOriginationCoherentBiadjunctionFiniteMateComparisonChainsV5_122.Generic
open KUOS.DependentOriginationCoherentBiadjunctionFiniteComparisonChainConcatenationV5_123.Generic
open KUOS.DependentOriginationCoherentBiadjunctionComparisonCompressionFunctorV5_124.Generic

set_option autoImplicit false
noncomputable section

/-!
# F28 / v5.125: original mate boundaries descend to a real hom quotient

The F27 full compression functor has a genuine kernel relation on the
unquotiented F26 dependent finite comparison chains: two presentations
are related precisely when their composite F-side 2-isomorphisms and
arbitrary G-side 2-cells are equal.

We construct an actual Lean Setoid and Quotient of each native 2-Hom,
prove its equivalence to the F27 composite comparison Hom, and prove
that the relation is a congruence for F26 path concatenation. Both
original F25 mate boundaries descend to *functions on the quotient*,
not merely an informal assertion of independence of presentations.

The F-side ISO orientation and the G-side possibly NONINVERTIBLE
comparison are unchanged. No change to the original F/G, source η /
target ε, chosen adjunctions, nonstrict mapId/mapComp or LAX mates.
-/

namespace Generic

universe uB vB wB uC vC wC
variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]

/-- Exact kernel relation of the original F27 comparison-compression
functor: equality of genuine F-ISO and arbitrary G-2-cell composites. -/
def chainKernelSetoid
    {aF bF aG bG : C}
    {fF kF : aF ⟶ bF} {fG kG : aG ⟶ bG} :
    Setoid (BiComparisonChain fF fG kF kG) where
  r c₁ c₂ :=
    c₁.fComposite = c₂.fComposite ∧
    c₁.gComposite = c₂.gComposite
  iseqv := ⟨
    (fun _ => ⟨rfl, rfl⟩),
    (fun h => ⟨h.1.symm, h.2.symm⟩),
    (fun h h' => ⟨h.1.trans h'.1, h.2.trans h'.2⟩)⟩

/-- Actual quotient type of each dependent F/G finite-comparison hom.
Its classes are presentations with exactly the same composite cells. -/
def KernelHom
    {aF bF aG bG : C}
    (fF : aF ⟶ bF) (fG : aG ⟶ bG)
    (kF : aF ⟶ bF) (kG : aG ⟶ bG) :=
  Quotient (chainKernelSetoid (fF := fF) (fG := fG)
    (kF := kF) (kG := kG))

/-- The quotient class of an actual unquotiented dependent comparison
chain retains its original endpoints and is NOT an axiomatically
identified presentation. -/
def chainClass
    {aF bF aG bG : C}
    {fF kF : aF ⟶ bF} {fG kG : aG ⟶ bG}
    (c : BiComparisonChain fF fG kF kG) :
    KernelHom fF fG kF kG :=
  Quotient.mk chainKernelSetoid c

/-- Equality of genuine classes is exactly equality of both composite
comparison 2-cells; no equality of intermediate path choices. -/
theorem chainClass_eq_iff
    {aF bF aG bG : C}
    {fF kF : aF ⟶ bF} {fG kG : aG ⟶ bG}
    (c₁ c₂ : BiComparisonChain fF fG kF kG) :
    chainClass c₁ = chainClass c₂ ↔
      c₁.fComposite = c₂.fComposite ∧
      c₁.gComposite = c₂.gComposite := by
  exact Quotient.eq

/-- F26 concatenation respects the compression kernel on BOTH finite
paths, even if their lengths and intermediate choices differ. -/
theorem chainKernel_append
    {aF bF aG bG : C}
    {fF kF lF : aF ⟶ bF} {fG kG lG : aG ⟶ bG}
    {head₁ head₂ : BiComparisonChain fF fG kF kG}
    {tail₁ tail₂ : BiComparisonChain kF kG lF lG}
    (h : (chainKernelSetoid (fF := fF) (fG := fG)
      (kF := kF) (kG := kG)).r head₁ head₂)
    (t : (chainKernelSetoid (fF := kF) (fG := kG)
      (kF := lF) (kG := lG)).r tail₁ tail₂) :
    (chainKernelSetoid (fF := fF) (fG := fG)
      (kF := lF) (kG := lG)).r
        (Chains.append head₁ tail₁) (Chains.append head₂ tail₂) := by
  rcases h with ⟨hf, hg⟩
  rcases t with ⟨tf, tg⟩
  constructor
  · rw [Chains.fComposite_append, Chains.fComposite_append, hf, tf]
  · rw [Chains.gComposite_append, Chains.gComposite_append, hg, tg]

/-- A genuine map from quotient classes to the original F27 composite
Hom, defined by a Quotient lift and supported by exactly the kernel. -/
def quotientComposite
    {aF bF aG bG : C}
    {fF kF : aF ⟶ bF} {fG kG : aG ⟶ bG}
    (q : KernelHom fF fG kF kG) :
    (fF ≅ kF) × (fG ⟶ kG) :=
  Quotient.liftOn q
    (fun c => (c.fComposite, c.gComposite))
    (by
      intro c₁ c₂ h
      exact Prod.ext h.1 h.2)

/-- Quotient compression maps genuine chain classes to exactly their
F/G composite 2-cells. -/
theorem quotientComposite_chainClass
    {aF bF aG bG : C}
    {fF kF : aF ⟶ bF} {fG kG : aG ⟶ bG}
    (c : BiComparisonChain fF fG kF kG) :
    quotientComposite (chainClass c) =
      (c.fComposite, c.gComposite) := rfl

/-- The original singleton comparison provides a section of quotient
compression. G-side comparison may be noninvertible. -/
def compositeClass
    {aF bF aG bG : C}
    {fF kF : aF ⟶ bF} {fG kG : aG ⟶ bG}
    (pq : (fF ≅ kF) × (fG ⟶ kG)) :
    KernelHom fF fG kF kG :=
  chainClass (BiComparisonChain.snoc BiComparisonChain.nil pq.1 pq.2)

/-- Compression of the actual singleton class is the original pair. -/
theorem quotientComposite_compositeClass
    {aF bF aG bG : C}
    {fF kF : aF ⟶ bF} {fG kG : aG ⟶ bG}
    (pq : (fF ≅ kF) × (fG ⟶ kG)) :
    quotientComposite (compositeClass pq) = pq := by
  rcases pq with ⟨p, q⟩
  change ((Iso.refl fF).trans p, (𝟙 fG) ≫ q) = (p, q)
  simp only [Iso.refl_trans, Category.id_comp]

/-- The kernel quotient map is injective: every two representatives
are identified IF AND ONLY IF their original composites are equal. -/
theorem quotientComposite_injective
    {aF bF aG bG : C}
    {fF kF : aF ⟶ bF} {fG kG : aG ⟶ bG} :
    Function.Injective (quotientComposite :
      KernelHom fF fG kF kG → (fF ≅ kF) × (fG ⟶ kG)) := by
  intro p q h
  induction p using Quotient.inductionOn with
  | _ p =>
      induction q using Quotient.inductionOn with
      | _ q =>
          apply Quotient.sound
          change (p.fComposite, p.gComposite) =
            (q.fComposite, q.gComposite) at h
          exact ⟨congrArg Prod.fst h, congrArg Prod.snd h⟩

/-- Every genuine pair of compressed cells is represented by exactly
one quotient class, with the singleton path a canonical representative. -/
def quotientHomEquiv
    {aF bF aG bG : C}
    {fF kF : aF ⟶ bF} {fG kG : aG ⟶ bG} :
    KernelHom fF fG kF kG ≃ ((fF ≅ kF) × (fG ⟶ kG)) where
  toFun := quotientComposite
  invFun := compositeClass
  left_inv := by
    intro p
    apply quotientComposite_injective
    exact (quotientComposite_compositeClass (quotientComposite p))
  right_inv := quotientComposite_compositeClass

#print axioms chainKernelSetoid
#print axioms KernelHom
#print axioms chainClass
#print axioms chainClass_eq_iff
#print axioms chainKernel_append
#print axioms quotientComposite
#print axioms quotientComposite_chainClass
#print axioms compositeClass
#print axioms quotientComposite_compositeClass
#print axioms quotientComposite_injective
#print axioms quotientHomEquiv

variable {F G : Pseudofunctor B C}
variable {σ θ : Pseudofunctor.StrongTrans F G}

/-- The original F25 left mate boundary, as an ACTUAL function on
kernel classes of finite paths (not just a well-definedness claim). -/
def quotientLeftMateBoundary
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    {X Y : B} (f : X ⟶ Y)
    {kF : F.obj X ⟶ F.obj Y} {kG : G.obj X ⟶ G.obj Y}
    (c : KernelHom (F.map f) (G.map f) kF kG) :=
  Quotient.liftOn c
    (fun path => finiteLeftBoundary dσ dθ Γ f path)
    (by
      intro p q h
      exact (finiteBiComparisonFactorizationIndependent dσ dθ Γ f p q
        h.1 h.2).1)

/-- The original F25 right mate boundary descends INDEPENDENTLY on
the same genuine quotient classes, retaining the full outer G whisker. -/
def quotientRightMateBoundary
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    {X Y : B} (f : X ⟶ Y)
    {kF : F.obj X ⟶ F.obj Y} {kG : G.obj X ⟶ G.obj Y}
    (c : KernelHom (F.map f) (G.map f) kF kG) :=
  Quotient.liftOn c
    (fun path => finiteRightBoundary dσ dθ Γ f path)
    (by
      intro p q h
      exact (finiteBiComparisonFactorizationIndependent dσ dθ Γ f p q
        h.1 h.2).2)

/-- Actual original left boundary is recovered by evaluating the
quotient-descended function on the corresponding class. -/
theorem quotientLeftMateBoundary_chainClass
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    {X Y : B} (f : X ⟶ Y)
    {kF : F.obj X ⟶ F.obj Y} {kG : G.obj X ⟶ G.obj Y}
    (c : BiComparisonChain (F.map f) (G.map f) kF kG) :
    quotientLeftMateBoundary dσ dθ Γ f (chainClass c) =
      finiteLeftBoundary dσ dθ Γ f c := rfl

/-- Actual original right boundary is recovered from the very SAME
kernel quotient class, without a G-comparison inverse. -/
theorem quotientRightMateBoundary_chainClass
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    {X Y : B} (f : X ⟶ Y)
    {kF : F.obj X ⟶ F.obj Y} {kG : G.obj X ⟶ G.obj Y}
    (c : BiComparisonChain (F.map f) (G.map f) kF kG) :
    quotientRightMateBoundary dσ dθ Γ f (chainClass c) =
      finiteRightBoundary dσ dθ Γ f c := rfl

/-- The F25 original native right-mate naturality holds as an
equality of functions evaluated on EVERY genuine quotient class. -/
theorem quotientMateNaturality
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    {X Y : B} (f : X ⟶ Y)
    {kF : F.obj X ⟶ F.obj Y} {kG : G.obj X ⟶ G.obj Y}
    (c : KernelHom (F.map f) (G.map f) kF kG) :
    quotientLeftMateBoundary dσ dθ Γ f c =
      quotientRightMateBoundary dσ dθ Γ f c := by
  induction c using Quotient.inductionOn with
  | _ path =>
      exact finiteBiComparisonNaturality dσ dθ Γ f path

/-- The descended mate boundary is precisely F27's original
compressed boundary evaluated on the canonical quotient-composite. -/
theorem quotientLeftMateBoundary_eq_compressed
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    {X Y : B} (f : X ⟶ Y)
    {kF : F.obj X ⟶ F.obj Y} {kG : G.obj X ⟶ G.obj Y}
    (c : KernelHom (F.map f) (G.map f) kF kG) :
    quotientLeftMateBoundary dσ dθ Γ f c =
      compressedMateLeftBoundary dσ dθ Γ f (quotientComposite c) := by
  induction c using Quotient.inductionOn with
  | _ path =>
      exact finiteLeftBoundary_factorsThroughCompression dσ dθ Γ f path

/-- The RIGHT descended boundary agrees with the F27 compressed
boundary, hence both have exactly the same original 2-cell meaning. -/
theorem quotientRightMateBoundary_eq_compressed
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    {X Y : B} (f : X ⟶ Y)
    {kF : F.obj X ⟶ F.obj Y} {kG : G.obj X ⟶ G.obj Y}
    (c : KernelHom (F.map f) (G.map f) kF kG) :
    quotientRightMateBoundary dσ dθ Γ f c =
      compressedMateRightBoundary dσ dθ Γ f (quotientComposite c) := by
  induction c using Quotient.inductionOn with
  | _ path =>
      exact finiteRightBoundary_factorsThroughCompression dσ dθ Γ f path

#print axioms quotientLeftMateBoundary
#print axioms quotientRightMateBoundary
#print axioms quotientLeftMateBoundary_chainClass
#print axioms quotientRightMateBoundary_chainClass
#print axioms quotientMateNaturality
#print axioms quotientLeftMateBoundary_eq_compressed
#print axioms quotientRightMateBoundary_eq_compressed

end Generic

end

end KUOS.DependentOriginationCoherentBiadjunctionComparisonKernelHomQuotientV5_125
