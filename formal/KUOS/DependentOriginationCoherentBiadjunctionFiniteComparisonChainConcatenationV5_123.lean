import KUOS.DependentOriginationCoherentBiadjunctionFiniteOriginalUnitCounitV5_122

namespace KUOS.DependentOriginationCoherentBiadjunctionFiniteComparisonChainConcatenationV5_123

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionArbitraryModificationMatesV5_113.Generic
open KUOS.DependentOriginationCoherentBiadjunctionAutomaticModificationMatesV5_114.Generic
open KUOS.DependentOriginationCoherentBiadjunctionFiniteMateComparisonChainsV5_122.Generic

set_option autoImplicit false
noncomputable section

/-!
# F26/v5.123: genuine concatenation of finite comparison chains

F25 constructs dependent finite sequences of pairs of bicategorical 2-cells.
We now compose TWO whole finite paths at any intermediate pair of 1-cells,
without collapsing the intermediate choices. The resulting operation
satisfies actual identity and associativity laws as equalities of
dependent chain values, not merely equalities of their composites.

The F comparison remains a genuine 2-ISO at each step; all G steps
may be noninvertible. Genuine expanded left/right mate corrections
compose in opposite/forward order, and the exact final composite
F/G correction is functorial. Thus both pasted boundaries remain
the original F22/F25 right-mate squares. Nothing is strictified.
-/

namespace Generic

universe uB vB wB uC vC wC
variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]

namespace Chains

variable {aF bF aG bG : C}
variable {fF : aF ⟶ bF} {fG : aG ⟶ bG}

/-- Concatenate two genuinely dependent F/G finite paths. Recurse on
the second path, preserving every intermediate original 1-cell. -/
def append
    {kF lF : aF ⟶ bF} {kG lG : aG ⟶ bG}
    (head : BiComparisonChain fF fG kF kG) :
    BiComparisonChain kF kG lF lG → BiComparisonChain fF fG lF lG
  | .nil => head
  | .snoc previous t r => .snoc (append head previous) t r

/-- Zero-step right unit: a chain followed by an empty chain. -/
theorem append_nil
    {kF : aF ⟶ bF} {kG : aG ⟶ bG}
    (head : BiComparisonChain fF fG kF kG) :
    append head (.nil : BiComparisonChain kF kG kF kG) = head := rfl

/-- Zero-step left unit: an empty chain followed by any chain. -/
theorem nil_append
    {kF : aF ⟶ bF} {kG : aG ⟶ bG}
    (tail : BiComparisonChain fF fG kF kG) :
    append (.nil : BiComparisonChain fF fG fF fG) tail = tail := by
  induction tail with
  | nil => rfl
  | snoc previous t r ih =>
      change .snoc (append (.nil : BiComparisonChain fF fG fF fG) previous) t r =
        .snoc previous t r
      rw [ih]

/-- Concatenation is associative as a typed CHAIN, including all
intermediate cells and not just their F/G composites. -/
theorem append_assoc
    {kF lF mF : aF ⟶ bF} {kG lG mG : aG ⟶ bG}
    (c₁ : BiComparisonChain fF fG kF kG)
    (c₂ : BiComparisonChain kF kG lF lG)
    (c₃ : BiComparisonChain lF lG mF mG) :
    append (append c₁ c₂) c₃ = append c₁ (append c₂ c₃) := by
  induction c₃ with
  | nil => rfl
  | snoc previous t r ih =>
      change .snoc (append (append c₁ c₂) previous) t r =
        .snoc (append c₁ (append c₂ previous)) t r
      rw [ih]

/-- Total finite depth is additive under path concatenation. -/
theorem depth_append
    {kF lF : aF ⟶ bF} {kG lG : aG ⟶ bG}
    (head : BiComparisonChain fF fG kF kG)
    (tail : BiComparisonChain kF kG lF lG) :
    (append head tail).depth = head.depth + tail.depth := by
  induction tail with
  | nil => simp only [append, BiComparisonChain.depth, Nat.add_zero]
  | snoc previous t r ih =>
      change (append head previous).depth + 1 =
        head.depth + (previous.depth + 1)
      rw [ih, Nat.add_succ]

/-- Original F-side 2-ISO composites respect concatenation. -/
theorem fComposite_append
    {kF lF : aF ⟶ bF} {kG lG : aG ⟶ bG}
    (head : BiComparisonChain fF fG kF kG)
    (tail : BiComparisonChain kF kG lF lG) :
    (append head tail).fComposite = head.fComposite.trans tail.fComposite := by
  induction tail with
  | nil =>
      change head.fComposite = head.fComposite.trans (Iso.refl kF)
      exact (Iso.trans_refl head.fComposite).symm
  | snoc previous t r ih =>
      change (append head previous).fComposite.trans t =
        head.fComposite.trans (previous.fComposite.trans t)
      rw [ih, Iso.trans_assoc]

/-- Original potentially NONINVERTIBLE G-side 2-cells compose
in their original forward direction. -/
theorem gComposite_append
    {kF lF : aF ⟶ bF} {kG lG : aG ⟶ bG}
    (head : BiComparisonChain fF fG kF kG)
    (tail : BiComparisonChain kF kG lF lG) :
    (append head tail).gComposite = head.gComposite ≫ tail.gComposite := by
  induction tail with
  | nil =>
      change head.gComposite = head.gComposite ≫ 𝟙 kG
      exact (Category.comp_id head.gComposite).symm
  | snoc previous t r ih =>
      change (append head previous).gComposite ≫ r =
        head.gComposite ≫ (previous.gComposite ≫ r)
      rw [ih, Category.assoc]

/-- Expanded F-side correction of a concatenated path is the
REVERSED-ORDER composite of the full tail and full head corrections. -/
theorem leftCorrection_append {a : C} (d : a ⟶ aF)
    {kF lF : aF ⟶ bF} {kG lG : aG ⟶ bG}
    (head : BiComparisonChain fF fG kF kG)
    (tail : BiComparisonChain kF kG lF lG) :
    (append head tail).leftCorrection d =
      tail.leftCorrection d ≫ head.leftCorrection d := by
  induction tail with
  | nil =>
      change head.leftCorrection d = 𝟙 (d ≫ kF) ≫ head.leftCorrection d
      exact (Category.id_comp (head.leftCorrection d)).symm
  | snoc previous t r ih =>
      change (d ◁ t.inv) ≫ (append head previous).leftCorrection d =
        ((d ◁ t.inv) ≫ previous.leftCorrection d) ≫ head.leftCorrection d
      rw [ih, Category.assoc]

/-- Expanded G-side correction of a concatenated path is the
FORWARD-ORDER composite of the full head and full tail corrections. -/
theorem rightCorrection_append {e : C} (h : bG ⟶ e)
    {kF lF : aF ⟶ bF} {kG lG : aG ⟶ bG}
    (head : BiComparisonChain fF fG kF kG)
    (tail : BiComparisonChain kF kG lF lG) :
    (append head tail).rightCorrection h =
      head.rightCorrection h ≫ tail.rightCorrection h := by
  induction tail with
  | nil =>
      change head.rightCorrection h = head.rightCorrection h ≫ 𝟙 (kG ≫ h)
      exact (Category.comp_id (head.rightCorrection h)).symm
  | snoc previous t r ih =>
      change (append head previous).rightCorrection h ≫ r ▷ h =
        (head.rightCorrection h ≫ previous.rightCorrection h) ≫ r ▷ h
      rw [ih]

/-- Existing F25 prepend is exactly a singleton chain concatenated
with its full original finite tail. -/
theorem prepend_eq_singleton_append
    {mF lF : aF ⟶ bF} {mG lG : aG ⟶ bG}
    (p : fF ≅ mF) (q : fG ⟶ mG)
    (tail : BiComparisonChain mF mG lF lG) :
    BiComparisonChain.prepend p q tail =
      append (.snoc .nil p q) tail := by
  induction tail with
  | nil => rfl
  | snoc previous t r ih =>
      change .snoc (BiComparisonChain.prepend p q previous) t r =
        .snoc (append (.snoc .nil p q) previous) t r
      rw [ih]

#print axioms append
#print axioms append_nil
#print axioms nil_append
#print axioms append_assoc
#print axioms depth_append
#print axioms fComposite_append
#print axioms gComposite_append
#print axioms leftCorrection_append
#print axioms rightCorrection_append
#print axioms prepend_eq_singleton_append

end Chains

/-- The objects of the native finite-path category are pairs of
ORIGINAL parallel 1-cells in C (F-side and G-side). -/
structure ComparisonPair (aF bF aG bG : C) where
  fF : aF ⟶ bF
  fG : aG ⟶ bG

/-- The category's actual homs are finite dependent comparison chains,
rather than quotient or composite cells. Identities and composition
are the genuine empty chain and F26 concatenation. -/
instance comparisonPairCategory (aF bF aG bG : C) :
    Category (ComparisonPair aF bF aG bG) where
  Hom X Y := BiComparisonChain X.fF X.fG Y.fF Y.fG
  id _ := .nil
  comp f g := Chains.append f g
  id_comp f := Chains.nil_append f
  comp_id f := Chains.append_nil f
  assoc f g h := Chains.append_assoc f g h

#print axioms ComparisonPair
#print axioms comparisonPairCategory

variable {F G : Pseudofunctor B C}
variable {σ θ : Pseudofunctor.StrongTrans F G}

/-- The real F25 global mate square holds for concatenated complete
finite paths, with all intermediate source and target 1-cells present. -/
def finiteAppendNaturality
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    {X Y : B} (f : X ⟶ Y)
    {kF lF : F.obj X ⟶ F.obj Y}
    {kG lG : G.obj X ⟶ G.obj Y}
    (head : BiComparisonChain (F.map f) (G.map f) kF kG)
    (tail : BiComparisonChain kF kG lF lG) :=
  finiteBiComparisonNaturality dσ dθ Γ f (Chains.append head tail)

/-- Normal form of the genuine expanded left mate boundary after
composing the TWO distinct original finite F/G comparison paths. -/
theorem finiteAppendLeftBoundary_normalize
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    {X Y : B} (f : X ⟶ Y)
    {kF lF : F.obj X ⟶ F.obj Y}
    {kG lG : G.obj X ⟶ G.obj Y}
    (head : BiComparisonChain (F.map f) (G.map f) kF kG)
    (tail : BiComparisonChain kF kG lF lG) :
    finiteLeftBoundary dσ dθ Γ f (Chains.append head tail) =
      (((rightModification dσ dθ Γ).app X ▷ lF ≫
          dσ.right.app X ◁
            ((head.fComposite).trans tail.fComposite).inv) ≫
        dσ.right.naturality f) ≫
        (head.gComposite ≫ tail.gComposite) ▷ dσ.right.app Y := by
  rw [finiteLeftBoundary_normalize, Chains.fComposite_append,
    Chains.gComposite_append]

/-- Normal form of the genuine expanded right mate boundary after
concatenation, retaining the actual terminal G whisker. -/
theorem finiteAppendRightBoundary_normalize
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    {X Y : B} (f : X ⟶ Y)
    {kF lF : F.obj X ⟶ F.obj Y}
    {kG lG : G.obj X ⟶ G.obj Y}
    (head : BiComparisonChain (F.map f) (G.map f) kF kG)
    (tail : BiComparisonChain kF kG lF lG) :
    finiteRightBoundary dσ dθ Γ f (Chains.append head tail) =
      (((dθ.right.app X ◁
          ((head.fComposite).trans tail.fComposite).inv ≫
          dθ.right.naturality f) ≫
        (head.gComposite ≫ tail.gComposite) ▷ dθ.right.app Y) ≫
        lG ◁ (rightModification dσ dθ Γ).app Y := by
  rw [finiteRightBoundary_normalize, Chains.fComposite_append,
    Chains.gComposite_append]

/-- Replacing BOTH finite subpaths by any others with the same original
composite F ISOs and G 2-cells leaves the entire concatenated mate
square unchanged on BOTH sides. No G invertibility or equal depth. -/
theorem finiteAppendFactorizationIndependent
    (dσ : RightMateLaxData σ) (dθ : RightMateLaxData θ)
    (Γ : Pseudofunctor.StrongTrans.Modification σ θ)
    {X Y : B} (f : X ⟶ Y)
    {kF lF : F.obj X ⟶ F.obj Y}
    {kG lG : G.obj X ⟶ G.obj Y}
    (head₁ head₂ : BiComparisonChain (F.map f) (G.map f) kF kG)
    (tail₁ tail₂ : BiComparisonChain kF kG lF lG)
    (hF : head₁.fComposite = head₂.fComposite)
    (hG : head₁.gComposite = head₂.gComposite)
    (tF : tail₁.fComposite = tail₂.fComposite)
    (tG : tail₁.gComposite = tail₂.gComposite) :
    finiteLeftBoundary dσ dθ Γ f (Chains.append head₁ tail₁) =
      finiteLeftBoundary dσ dθ Γ f (Chains.append head₂ tail₂) ∧
    finiteRightBoundary dσ dθ Γ f (Chains.append head₁ tail₁) =
      finiteRightBoundary dσ dθ Γ f (Chains.append head₂ tail₂) := by
  exact finiteBiComparisonFactorizationIndependent dσ dθ Γ f
    (Chains.append head₁ tail₁) (Chains.append head₂ tail₂)
    (by rw [Chains.fComposite_append, Chains.fComposite_append, hF, tF])
    (by rw [Chains.gComposite_append, Chains.gComposite_append, hG, tG])

#print axioms finiteAppendNaturality
#print axioms finiteAppendLeftBoundary_normalize
#print axioms finiteAppendRightBoundary_normalize
#print axioms finiteAppendFactorizationIndependent

end Generic

end

end KUOS.DependentOriginationCoherentBiadjunctionFiniteComparisonChainConcatenationV5_123
