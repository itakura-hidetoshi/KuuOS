import KUOS.DependentOriginationCoherentBiadjunctionTwoStageExchangeMateNaturalityV5_132

namespace KUOS.DependentOriginationCoherentBiadjunctionFiniteHorizontalExchangeV5_133

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionCompressionKernelQuotientCategoryV5_125.Generic
open KUOS.DependentOriginationCoherentBiadjunctionHorizontalQuotientFunctorsV5_127.Generic
open KUOS.DependentOriginationCoherentBiadjunctionKernelQuotientHorizontalExchangeV5_131.Generic

set_option autoImplicit false
noncomputable section

/-!
# F36/v5.133: actual F28 quotient-category finite paths and mixed exchange

These paths consist of arbitrary composable morphisms of a CATEGORY, so
specializing to the F28 compression-kernel quotient does NOT identify
them with F26's comparison-chain representation. Naturality is proved
by induction on the arbitrary finite length (including length zero).
The bracketing construction permits arbitrary binary pasting trees.
-/

namespace Chain

universe u v uE vE
variable {D : Type u} [Category.{v} D]

/-- An arbitrary finite directed path in a genuine category. Unlike F26's
comparison-chain carrier, every arrow here is a native category Hom. -/
inductive Path : D → D → Type (max u v) where
  | nil (x : D) : Path x x
  | snoc {x y z : D} (p : Path x y) (q : y ⟶ z) : Path x z

/-- Compose a finite categorical path in its given order. -/
def Path.composite {x y : D} : Path x y → (x ⟶ y)
  | .nil _ => 𝟙 _
  | .snoc p q => p.composite ≫ q

/-- Append two composable paths without changing any arrow. -/
def Path.append {x y z : D} (p : Path x y) : Path y z → Path x z
  | .nil _ => p
  | .snoc q r => Path.snoc (p.append q) r

theorem Path.composite_append {x y z : D} (p : Path x y)
    (q : Path y z) :
    (p.append q).composite = p.composite ≫ q.composite := by
  induction q with
  | nil y =>
      change p.composite = p.composite ≫ 𝟙 y
      rw [Category.comp_id]
  | @snoc y z w q r ih =>
      change (p.append q).composite ≫ r =
        p.composite ≫ (q.composite ≫ r)
      rw [ih]
      exact Category.assoc _ _ _

theorem Path.append_assoc {w x y z : D}
    (p : Path w x) (q : Path x y) (r : Path y z) :
    (p.append q).append r = p.append (q.append r) := by
  induction r with
  | nil y => rfl
  | @snoc y z t r f ih =>
      change Path.snoc ((p.append q).append r) f =
        Path.snoc (p.append (q.append r)) f
      rw [ih]

theorem Path.nil_append {x y : D} (p : Path x y) :
    (Path.nil x).append p = p := by
  induction p with
  | nil x => rfl
  | @snoc x y z p q ih =>
      change Path.snoc ((Path.nil x).append p) q = Path.snoc p q
      rw [ih]

/-- Real finite-length naturality, proved by induction on the last arrow,
using the intermediate component of the same natural transformation. -/
theorem Path.naturality {E : Type uE} [Category.{vE} E]
    {L R : D ⥤ E} (α : L ⟶ R)
    {x y : D} (p : Path x y) :
    L.map p.composite ≫ α.app y =
      α.app x ≫ R.map p.composite := by
  induction p with
  | nil x =>
      simp only [Path.composite, Functor.map_id, Category.id_comp,
        Category.comp_id]
  | @snoc x y z p q ih =>
      simp only [Path.composite, Functor.map_comp]
      calc
        (L.map p.composite ≫ L.map q) ≫ α.app z =
          L.map p.composite ≫ (L.map q ≫ α.app z) :=
            Category.assoc _ _ _
        _ = L.map p.composite ≫ (α.app y ≫ R.map q) := by
          rw [α.naturality q]
        _ = (L.map p.composite ≫ α.app y) ≫ R.map q :=
          (Category.assoc _ _ _).symm
        _ = (α.app x ≫ R.map p.composite) ≫ R.map q := by
          rw [ih]
        _ = α.app x ≫ (R.map p.composite ≫ R.map q) :=
          Category.assoc _ _ _

/-- All binary parenthesizations of any finite list of genuine arrows.
Different trees are allowed; only their ordered flattened arrows matter. -/
inductive Bracketing : D → D → Type (max u v) where
  | empty (x : D) : Bracketing x x
  | arrow {x y : D} (q : x ⟶ y) : Bracketing x y
  | paste {x y z : D} (p : Bracketing x y)
      (q : Bracketing y z) : Bracketing x z

def Bracketing.flattened {x y : D} : Bracketing x y → Path x y
  | .empty x => Path.nil x
  | .arrow q => Path.snoc (Path.nil _) q
  | .paste p q => p.flattened.append q.flattened

def Bracketing.evaluated {x y : D} : Bracketing x y → (x ⟶ y)
  | .empty x => 𝟙 x
  | .arrow q => q
  | .paste p q => p.evaluated ≫ q.evaluated

theorem Bracketing.evaluated_eq_flattened {x y : D}
    (p : Bracketing x y) :
    p.evaluated = p.flattened.composite := by
  induction p with
  | empty x => rfl
  | arrow q =>
      change q = (𝟙 _ ≫ q)
      simp
  | paste p q ihp ihq =>
      change p.evaluated ≫ q.evaluated =
        (p.flattened.append q.flattened).composite
      rw [ihp, ihq, Path.composite_append]

/-- Arbitrary binary pastings are identical when they have the same
ordered finite sequence of genuine quotient-category arrows. -/
theorem Bracketing.independent {x y : D} (p q : Bracketing x y)
    (h : p.flattened = q.flattened) :
    p.evaluated = q.evaluated := by
  calc
    p.evaluated = p.flattened.composite := p.evaluated_eq_flattened
    _ = q.flattened.composite := by rw [h]
    _ = q.evaluated := q.evaluated_eq_flattened.symm

end Chain

namespace Generic

universe uC vC wC
variable {C : Type uC} [Bicategory.{wC, vC} C]

/-- F36 finite arrows live in the genuine F28 kernel quotient CATEGORY. -/
abbrev finiteKernelQuotientChain (aF bF aG bG : C)
    (x y : compressionKernelCategory aF bF aG bG) :=
  Chain.Path x y

/-- The F34 mixed exchange NatIso is natural for the composite of every
finite F28 quotient-arrow path, not just two arrows. The proof uses
Path.naturality's actual structural induction and does not invert G. -/
theorem kernelHorizontalExchangeFiniteNaturality
    (aF bF aG bG : C)
    {eF eG dF dG : C}
    (uF : eF ⟶ aF) (uG : eG ⟶ aG)
    (vF : bF ⟶ dF) (vG : bG ⟶ dG)
    {x y : compressionKernelCategory aF bF aG bG}
    (p : finiteKernelQuotientChain aF bF aG bG x y) :
    let L := leftKernelQuotientWhiskerFunctor aF bF aG bG uF uG ⋙
      rightKernelQuotientWhiskerFunctor eF bF eG bG vF vG
    let R := rightKernelQuotientWhiskerFunctor aF bF aG bG vF vG ⋙
      leftKernelQuotientWhiskerFunctor aF dF aG dG uF uG
    let exchange := kernelQuotientHorizontalExchangeNatIso
      aF bF aG bG uF uG vF vG
    L.map p.composite ≫ exchange.hom.app y =
      exchange.hom.app x ≫ R.map p.composite := by
  dsimp only
  let L := leftKernelQuotientWhiskerFunctor aF bF aG bG uF uG ⋙
    rightKernelQuotientWhiskerFunctor eF bF eG bG vF vG
  let R := rightKernelQuotientWhiskerFunctor aF bF aG bG vF vG ⋙
    leftKernelQuotientWhiskerFunctor aF dF aG dG uF uG
  let exchange := kernelQuotientHorizontalExchangeNatIso
    aF bF aG bG uF uG vF vG
  change L.map p.composite ≫ exchange.hom.app y =
    exchange.hom.app x ≫ R.map p.composite
  exact Chain.Path.naturality exchange.hom p

/-- Finite exchange naturality also holds for EVERY parenthesized
pasting tree, evaluated without selecting a privileged bracketing. -/
theorem kernelHorizontalExchangeBracketedNaturality
    (aF bF aG bG : C)
    {eF eG dF dG : C}
    (uF : eF ⟶ aF) (uG : eG ⟶ aG)
    (vF : bF ⟶ dF) (vG : bG ⟶ dG)
    {x y : compressionKernelCategory aF bF aG bG}
    (p : Chain.Bracketing x y) :
    let L := leftKernelQuotientWhiskerFunctor aF bF aG bG uF uG ⋙
      rightKernelQuotientWhiskerFunctor eF bF eG bG vF vG
    let R := rightKernelQuotientWhiskerFunctor aF bF aG bG vF vG ⋙
      leftKernelQuotientWhiskerFunctor aF dF aG dG uF uG
    let exchange := kernelQuotientHorizontalExchangeNatIso
      aF bF aG bG uF uG vF vG
    L.map p.evaluated ≫ exchange.hom.app y =
      exchange.hom.app x ≫ R.map p.evaluated := by
  simpa only [Chain.Bracketing.evaluated_eq_flattened] using
    (kernelHorizontalExchangeFiniteNaturality aF bF aG bG
      uF uG vF vG p.flattened)

/-- No finite binary rebracketing can change EITHER naturality route,
provided the ordered native quotient-category arrows are unchanged. -/
theorem kernelHorizontalExchangeBracketingsIndependent
    (aF bF aG bG : C)
    {eF eG dF dG : C}
    (uF : eF ⟶ aF) (uG : eG ⟶ aG)
    (vF : bF ⟶ dF) (vG : bG ⟶ dG)
    {x y : compressionKernelCategory aF bF aG bG}
    (p q : Chain.Bracketing x y)
    (h : p.flattened = q.flattened) :
    let L := leftKernelQuotientWhiskerFunctor aF bF aG bG uF uG ⋙
      rightKernelQuotientWhiskerFunctor eF bF eG bG vF vG
    let R := rightKernelQuotientWhiskerFunctor aF bF aG bG vF vG ⋙
      leftKernelQuotientWhiskerFunctor aF dF aG dG uF uG
    let exchange := kernelQuotientHorizontalExchangeNatIso
      aF bF aG bG uF uG vF vG
    (L.map p.evaluated ≫ exchange.hom.app y =
      L.map q.evaluated ≫ exchange.hom.app y) ∧
      (exchange.hom.app x ≫ R.map p.evaluated =
        exchange.hom.app x ≫ R.map q.evaluated) := by
  dsimp only
  have heval := Chain.Bracketing.independent p q h
  constructor <;> rw [heval]

#print axioms Chain.Path
#print axioms Chain.Path.composite
#print axioms Chain.Path.append
#print axioms Chain.Path.composite_append
#print axioms Chain.Path.append_assoc
#print axioms Chain.Path.nil_append
#print axioms Chain.Path.naturality
#print axioms Chain.Bracketing
#print axioms Chain.Bracketing.flattened
#print axioms Chain.Bracketing.evaluated
#print axioms Chain.Bracketing.evaluated_eq_flattened
#print axioms Chain.Bracketing.independent
#print axioms finiteKernelQuotientChain
#print axioms kernelHorizontalExchangeFiniteNaturality
#print axioms kernelHorizontalExchangeBracketedNaturality
#print axioms kernelHorizontalExchangeBracketingsIndependent

end Generic
end

end KUOS.DependentOriginationCoherentBiadjunctionFiniteHorizontalExchangeV5_133
