import KUOS.DependentOriginationCoherentBiadjunctionActualLiftKernelDescentV5_125

namespace KUOS.DependentOriginationCoherentBiadjunctionNonstrictKernelWhiskeringV5_126

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionFiniteMateComparisonChainsV5_122.Generic
open KUOS.DependentOriginationCoherentBiadjunctionFiniteComparisonChainConcatenationV5_123.Generic
open KUOS.DependentOriginationCoherentBiadjunctionComparisonCompressionFunctorV5_124.Generic
open KUOS.DependentOriginationCoherentBiadjunctionComparisonKernelHomQuotientV5_125.Generic
open KUOS.DependentOriginationCoherentBiadjunctionCompressionKernelQuotientCategoryV5_125.Generic
open KUOS.DependentOriginationCoherentBiadjunctionArbitraryModificationMatesV5_113.Generic

set_option autoImplicit false
noncomputable section

/-!
# F29 / v5.126: original nonstrict comparisons and horizontal quotient whiskering

The genuine original F.mapId/F.mapComp isomorphisms and potentially
noninvertible G.toOplax.mapId/mapComp cells induce actual functions on the
F28 quotient Homs. Their composite descriptions retain BOTH components
and agree with F27 compression. Both left and right horizontal whiskering
of the genuine F ISO/G arbitrary-cell pair also descend as actual
Quotient.liftOn functions. No ambient-bicategory biequivalence or
invertibility of G-side cells is asserted.
-/

namespace Generic

universe uB vB wB uC vC wC
variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]
variable {F G : Pseudofunctor B C}

/-- The actual original nonstrict mapId pair remains at the front of
the F/G composites of an arbitrary continuation. -/
theorem originalMapIdPrepend_composites (X : B)
    {kF : F.obj X ⟶ F.obj X} {kG : G.obj X ⟶ G.obj X}
    (tail : BiComparisonChain (𝟙 (F.obj X)) (𝟙 (G.obj X)) kF kG) :
    (originalMapIdFiniteChain (F := F) (G := G) X tail).fComposite =
        (F.mapId X).trans tail.fComposite ∧
    (originalMapIdFiniteChain (F := F) (G := G) X tail).gComposite =
        (G.toOplax.mapId X) ≫ tail.gComposite := by
  constructor
  · simp only [originalMapIdFiniteChain, Chains.prepend_eq_singleton_append,
      Chains.fComposite_append, BiComparisonChain.fComposite, Iso.refl_trans]
  · simp only [originalMapIdFiniteChain, Chains.prepend_eq_singleton_append,
      Chains.gComposite_append, BiComparisonChain.gComposite, Category.id_comp]

/-- Composition comparisons are retained with their genuine nonstrict
orientation, for any continuation (the G part need not invert). -/
theorem originalMapCompPrepend_composites
    {X Y Z : B} (f : X ⟶ Y) (g : Y ⟶ Z)
    {kF : F.obj X ⟶ F.obj Z} {kG : G.obj X ⟶ G.obj Z}
    (tail : BiComparisonChain (F.map f ≫ F.map g)
      (G.map f ≫ G.map g) kF kG) :
    (originalMapCompFiniteChain (F := F) (G := G) f g tail).fComposite =
        (F.mapComp f g).trans tail.fComposite ∧
    (originalMapCompFiniteChain (F := F) (G := G) f g tail).gComposite =
        (G.toOplax.mapComp f g) ≫ tail.gComposite := by
  constructor
  · simp only [originalMapCompFiniteChain, Chains.prepend_eq_singleton_append,
      Chains.fComposite_append, BiComparisonChain.fComposite, Iso.refl_trans]
  · simp only [originalMapCompFiniteChain, Chains.prepend_eq_singleton_append,
      Chains.gComposite_append, BiComparisonChain.gComposite, Category.id_comp]

/-- Prepending original mapId preserves EXACTLY the F28 compression
kernel, on both the invertible F and noninvertible G components. -/
theorem originalMapIdPrepend_respects_kernel (X : B)
    {kF : F.obj X ⟶ F.obj X} {kG : G.obj X ⟶ G.obj X}
    {p q : BiComparisonChain (𝟙 (F.obj X)) (𝟙 (G.obj X)) kF kG}
    (h : (chainKernelSetoid (fF := 𝟙 (F.obj X))
      (fG := 𝟙 (G.obj X)) (kF := kF) (kG := kG)).r p q) :
    (chainKernelSetoid (fF := F.map (𝟙 X))
      (fG := G.map (𝟙 X)) (kF := kF) (kG := kG)).r
        (originalMapIdFiniteChain (F := F) (G := G) X p)
        (originalMapIdFiniteChain (F := F) (G := G) X q) := by
  rcases h with ⟨hp, hq⟩
  constructor
  · rw [(originalMapIdPrepend_composites (F := F) (G := G) X p).1,
        (originalMapIdPrepend_composites (F := F) (G := G) X q).1, hp]
  · rw [(originalMapIdPrepend_composites (F := F) (G := G) X p).2,
        (originalMapIdPrepend_composites (F := F) (G := G) X q).2, hq]

/-- Same kernel preservation for the authentic original mapComp pair. -/
theorem originalMapCompPrepend_respects_kernel
    {X Y Z : B} (f : X ⟶ Y) (g : Y ⟶ Z)
    {kF : F.obj X ⟶ F.obj Z} {kG : G.obj X ⟶ G.obj Z}
    {p q : BiComparisonChain (F.map f ≫ F.map g)
      (G.map f ≫ G.map g) kF kG}
    (h : (chainKernelSetoid (fF := F.map f ≫ F.map g)
      (fG := G.map f ≫ G.map g) (kF := kF) (kG := kG)).r p q) :
    (chainKernelSetoid (fF := F.map (f ≫ g))
      (fG := G.map (f ≫ g)) (kF := kF) (kG := kG)).r
        (originalMapCompFiniteChain (F := F) (G := G) f g p)
        (originalMapCompFiniteChain (F := F) (G := G) f g q) := by
  rcases h with ⟨hp, hq⟩
  constructor
  · rw [(originalMapCompPrepend_composites (F := F) (G := G) f g p).1,
        (originalMapCompPrepend_composites (F := F) (G := G) f g q).1, hp]
  · rw [(originalMapCompPrepend_composites (F := F) (G := G) f g p).2,
        (originalMapCompPrepend_composites (F := F) (G := G) f g q).2, hq]

/-- Actual induced mapId operation ON kernel quotient classes, not
merely on a chosen representative. -/
def originalMapIdQuotientPrepend (X : B)
    {kF : F.obj X ⟶ F.obj X} {kG : G.obj X ⟶ G.obj X}
    (q : KernelHom (𝟙 (F.obj X)) (𝟙 (G.obj X)) kF kG) :
    KernelHom (F.map (𝟙 X)) (G.map (𝟙 X)) kF kG :=
  Quotient.liftOn q
    (fun tail => chainClass
      (originalMapIdFiniteChain (F := F) (G := G) X tail))
    (by
      intro p r h
      apply Quotient.sound
      exact originalMapIdPrepend_respects_kernel (F := F) (G := G) X h)

/-- Actual induced original mapComp operation on kernel classes. -/
def originalMapCompQuotientPrepend
    {X Y Z : B} (f : X ⟶ Y) (g : Y ⟶ Z)
    {kF : F.obj X ⟶ F.obj Z} {kG : G.obj X ⟶ G.obj Z}
    (q : KernelHom (F.map f ≫ F.map g) (G.map f ≫ G.map g) kF kG) :
    KernelHom (F.map (f ≫ g)) (G.map (f ≫ g)) kF kG :=
  Quotient.liftOn q
    (fun tail => chainClass
      (originalMapCompFiniteChain (F := F) (G := G) f g tail))
    (by
      intro p r h
      apply Quotient.sound
      exact originalMapCompPrepend_respects_kernel (F := F) (G := G) f g h)

/-- The genuine mapId quotient function commutes exactly with F27/F28
compression. The G component remains an arbitrary forward 2-cell. -/
theorem originalMapIdQuotientPrepend_composite (X : B)
    {kF : F.obj X ⟶ F.obj X} {kG : G.obj X ⟶ G.obj X}
    (q : KernelHom (𝟙 (F.obj X)) (𝟙 (G.obj X)) kF kG) :
    quotientComposite (originalMapIdQuotientPrepend (F := F) (G := G) X q) =
      ((F.mapId X).trans (quotientComposite q).1,
       G.toOplax.mapId X ≫ (quotientComposite q).2) := by
  induction q using Quotient.inductionOn with
  | _ tail =>
      change
        ((originalMapIdFiniteChain (F := F) (G := G) X tail).fComposite,
         (originalMapIdFiniteChain (F := F) (G := G) X tail).gComposite) =
        ((F.mapId X).trans tail.fComposite,
         G.toOplax.mapId X ≫ tail.gComposite)
      exact Prod.ext
        (originalMapIdPrepend_composites (F := F) (G := G) X tail).1
        (originalMapIdPrepend_composites (F := F) (G := G) X tail).2

/-- Original mapComp quotient function also commutes exactly with
compression, without treating its comparison as an identity. -/
theorem originalMapCompQuotientPrepend_composite
    {X Y Z : B} (f : X ⟶ Y) (g : Y ⟶ Z)
    {kF : F.obj X ⟶ F.obj Z} {kG : G.obj X ⟶ G.obj Z}
    (q : KernelHom (F.map f ≫ F.map g) (G.map f ≫ G.map g) kF kG) :
    quotientComposite (originalMapCompQuotientPrepend (F := F) (G := G) f g q) =
      ((F.mapComp f g).trans (quotientComposite q).1,
       G.toOplax.mapComp f g ≫ (quotientComposite q).2) := by
  induction q using Quotient.inductionOn with
  | _ tail =>
      change
        ((originalMapCompFiniteChain (F := F) (G := G) f g tail).fComposite,
         (originalMapCompFiniteChain (F := F) (G := G) f g tail).gComposite) =
        ((F.mapComp f g).trans tail.fComposite,
         G.toOplax.mapComp f g ≫ tail.gComposite)
      exact Prod.ext
        (originalMapCompPrepend_composites (F := F) (G := G) f g tail).1
        (originalMapCompPrepend_composites (F := F) (G := G) f g tail).2

/-- Genuine left horizontal whiskering descends as an actual function
on F28 kernel classes. Crucially the F result is still an ISO, but
the G result is only the original whiskered 2-cell. -/
def quotientLeftWhiskering
    {aF bF aG bG : C} {fF kF : aF ⟶ bF} {fG kG : aG ⟶ bG}
    {eF eG : C} (uF : eF ⟶ aF) (uG : eG ⟶ aG)
    (q : KernelHom fF fG kF kG) :
    ((uF ≫ fF) ≅ (uF ≫ kF)) × ((uG ≫ fG) ⟶ (uG ≫ kG)) :=
  Quotient.liftOn q
    (fun c => (Bicategory.whiskerLeftIso uF c.fComposite,
      uG ◁ c.gComposite))
    (by
      intro c d h
      exact Prod.ext
        (congrArg (fun p => Bicategory.whiskerLeftIso uF p) h.1)
        (congrArg (fun r => uG ◁ r) h.2))

/-- Genuine right horizontal whiskering descends to F28 quotient
classes; G is not made invertible. -/
def quotientRightWhiskering
    {aF bF aG bG : C} {fF kF : aF ⟶ bF} {fG kG : aG ⟶ bG}
    {eF eG : C} (vF : bF ⟶ eF) (vG : bG ⟶ eG)
    (q : KernelHom fF fG kF kG) :
    ((fF ≫ vF) ≅ (kF ≫ vF)) × ((fG ≫ vG) ⟶ (kG ≫ vG)) :=
  Quotient.liftOn q
    (fun c => (Bicategory.whiskerRightIso c.fComposite vF,
      c.gComposite ▷ vG))
    (by
      intro c d h
      exact Prod.ext
        (congrArg (fun p => Bicategory.whiskerRightIso p vF) h.1)
        (congrArg (fun r => r ▷ vG) h.2))

/-- Left whiskering of the quotient is literally left whiskering of
its F27 compressed composite, on BOTH original 2-cell components. -/
theorem quotientLeftWhiskering_eq_compressed
    {aF bF aG bG : C} {fF kF : aF ⟶ bF} {fG kG : aG ⟶ bG}
    {eF eG : C} (uF : eF ⟶ aF) (uG : eG ⟶ aG)
    (q : KernelHom fF fG kF kG) :
    quotientLeftWhiskering uF uG q =
      (Bicategory.whiskerLeftIso uF (quotientComposite q).1,
        uG ◁ (quotientComposite q).2) := by
  induction q using Quotient.inductionOn with
  | _ path => rfl

/-- The right whisker commutes exactly with the F28 quotient Hom
equivalence and keeps all native bicategorical 2-cell directions. -/
theorem quotientRightWhiskering_eq_compressed
    {aF bF aG bG : C} {fF kF : aF ⟶ bF} {fG kG : aG ⟶ bG}
    {eF eG : C} (vF : bF ⟶ eF) (vG : bG ⟶ eG)
    (q : KernelHom fF fG kF kG) :
    quotientRightWhiskering vF vG q =
      (Bicategory.whiskerRightIso (quotientComposite q).1 vF,
        (quotientComposite q).2 ▷ vG) := by
  induction q using Quotient.inductionOn with
  | _ path => rfl

variable {σ θ : Pseudofunctor.StrongTrans F G}

/-- MapId quotient descent is compatible with the original lax right
mate square: both independently descended boundaries are equal. -/
theorem originalMapIdQuotientMateNaturality
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ) (X : B)
    {kF : F.obj X ⟶ F.obj X} {kG : G.obj X ⟶ G.obj X}
    (q : KernelHom (𝟙 (F.obj X)) (𝟙 (G.obj X)) kF kG) :
    quotientLeftMateBoundary dσ dθ Γ (𝟙 X)
      (originalMapIdQuotientPrepend (F := F) (G := G) X q) =
    quotientRightMateBoundary dσ dθ Γ (𝟙 X)
      (originalMapIdQuotientPrepend (F := F) (G := G) X q) :=
  quotientMateNaturality dσ dθ Γ (𝟙 X) _

/-- MapComp quotient descent likewise preserves the actual right mate
boundary at the composite original 1-cell. -/
theorem originalMapCompQuotientMateNaturality
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    {X Y Z : B} (f : X ⟶ Y) (g : Y ⟶ Z)
    {kF : F.obj X ⟶ F.obj Z} {kG : G.obj X ⟶ G.obj Z}
    (q : KernelHom (F.map f ≫ F.map g) (G.map f ≫ G.map g) kF kG) :
    quotientLeftMateBoundary dσ dθ Γ (f ≫ g)
      (originalMapCompQuotientPrepend (F := F) (G := G) f g q) =
    quotientRightMateBoundary dσ dθ Γ (f ≫ g)
      (originalMapCompQuotientPrepend (F := F) (G := G) f g q) :=
  quotientMateNaturality dσ dθ Γ (f ≫ g) _

#print axioms originalMapIdPrepend_composites
#print axioms originalMapCompPrepend_composites
#print axioms originalMapIdPrepend_respects_kernel
#print axioms originalMapCompPrepend_respects_kernel
#print axioms originalMapIdQuotientPrepend
#print axioms originalMapCompQuotientPrepend
#print axioms originalMapIdQuotientPrepend_composite
#print axioms originalMapCompQuotientPrepend_composite
#print axioms quotientLeftWhiskering
#print axioms quotientRightWhiskering
#print axioms quotientLeftWhiskering_eq_compressed
#print axioms quotientRightWhiskering_eq_compressed
#print axioms originalMapIdQuotientMateNaturality
#print axioms originalMapCompQuotientMateNaturality

end Generic

end

end KUOS.DependentOriginationCoherentBiadjunctionNonstrictKernelWhiskeringV5_126
