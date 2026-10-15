import Mathlib
import KUOS.DependentOriginationFundamentalGroupoidTransportV0_4

namespace KUOS.DependentOriginationFundamentalGroupoidDescentObstructionV0_5

open CategoryTheory
open KUOS.DependentOriginationFunctorialTransportV0_1
open KUOS.DependentOriginationFundamentalGroupoidTransportV0_4

universe u v w

/-!
# Fundamental-groupoid descent obstruction v0.5

The v0.4 layer realizes ordinary endpoint-fixed path-homotopy-invariant
transport as a functor on `FundamentalGroupoid X`.

This file isolates the exact categorical boundary between such transport and a
finer reversible path context.  Let

```text
Q : P ⥤ FundamentalGroupoid X
```

be a quotient/forgetful functor from a finer context `P`.  A transport

```text
S : P ⥤ Type
```

descends to the ordinary fundamental groupoid when it is naturally isomorphic
to the pullback `Q ⋙ T` of some fundamental-groupoid transport `T`.

A necessary consequence is the kernel-containment law

```text
Q.map f = Q.map g  ->  S.map f = S.map g.
```

Thus any pair of fine morphisms that becomes equal after `Q` but still induces
different transport maps is a rigorous obstruction to ordinary-homotopy
descent.

This distinction is deliberately independent of reversibility.  Even if `P`
is a groupoid, so every `S.map f` is invertible, `S` need not descend through
`Q`.  Hence

```text
reversible transport != ordinary-homotopy-invariant transport.
```

No smooth connection, thin-homotopy groupoid, curvature, Yang--Mills action,
quantization, Hamiltonian, continuum limit, or mass-gap statement is asserted
here.
-/

variable {P : Type u} [Category P]
variable {X : Type w} [TopologicalSpace X]

/--
Witness that a fine-context transport is obtained, up to natural isomorphism,
by pulling back a transport on the ordinary fundamental groupoid.
-/
structure FundamentalDescent
    (Q : P ⥤ FundamentalGroupoid X)
    (S : P ⥤ Type v) where
  quotientTransport : FundamentalTransport (v := v) X
  comparison : S ≅ Q ⋙ quotientTransport

/--
The kernel-compatibility condition required of any transport that descends
through `Q`: arrows identified by `Q` must have identical transport maps.
-/
def QuotientKernelCompatible
    (Q : P ⥤ FundamentalGroupoid X)
    (S : P ⥤ Type v) : Prop :=
  ∀ {a b : P} (f g : a ⟶ b),
    Q.map f = Q.map g → S.map f = S.map g

/--
A concrete obstruction witness: two fine arrows are identified by the quotient
but remain distinguishable by the transport.
-/
def HasQuotientKernelObstruction
    (Q : P ⥤ FundamentalGroupoid X)
    (S : P ⥤ Type v) : Prop :=
  ∃ (a b : P) (f g : a ⟶ b),
    Q.map f = Q.map g ∧ S.map f ≠ S.map g

namespace FundamentalDescent

variable {Q : P ⥤ FundamentalGroupoid X}
variable {S : P ⥤ Type v}

/--
Descent forces equality of transport maps on every pair in the morphism kernel
of the quotient functor.
-/
theorem map_eq_of_quotient_map_eq
    (D : FundamentalDescent Q S)
    {a b : P} (f g : a ⟶ b)
    (hQ : Q.map f = Q.map g) :
    S.map f = S.map g := by
  apply (cancel_mono (D.comparison.hom.app b)).1
  calc
    S.map f ≫ D.comparison.hom.app b =
        D.comparison.hom.app a ≫ (Q ⋙ D.quotientTransport).map f :=
      D.comparison.hom.naturality f
    _ = D.comparison.hom.app a ≫ (Q ⋙ D.quotientTransport).map g := by
      simp only [Functor.comp_map, hQ]
    _ = S.map g ≫ D.comparison.hom.app b :=
      (D.comparison.hom.naturality g).symm

/-- Every actual descent witness satisfies quotient-kernel compatibility. -/
theorem kernelCompatible
    (D : FundamentalDescent Q S) :
    QuotientKernelCompatible Q S := by
  intro a b f g hQ
  exact D.map_eq_of_quotient_map_eq f g hQ

end FundamentalDescent

/--
Literal pullback from a fundamental-groupoid transport is the canonical example
of descent.
-/
def pullbackDescent
    (Q : P ⥤ FundamentalGroupoid X)
    (T : FundamentalTransport (v := v) X) :
    FundamentalDescent Q (Q ⋙ T) where
  quotientTransport := T
  comparison := Iso.refl _

/--
A quotient-kernel witness rules out every possible fundamental-groupoid descent
presentation.
-/
theorem noFundamentalDescent_of_kernel_witness
    {Q : P ⥤ FundamentalGroupoid X}
    {S : P ⥤ Type v}
    {a b : P} {f g : a ⟶ b}
    (hQ : Q.map f = Q.map g)
    (hS : S.map f ≠ S.map g) :
    ¬ Nonempty (FundamentalDescent Q S) := by
  rintro ⟨D⟩
  exact hS (D.map_eq_of_quotient_map_eq f g hQ)

/-- Packaged obstruction witnesses imply non-descent. -/
theorem noFundamentalDescent_of_obstruction
    {Q : P ⥤ FundamentalGroupoid X}
    {S : P ⥤ Type v}
    (h : HasQuotientKernelObstruction Q S) :
    ¬ Nonempty (FundamentalDescent Q S) := by
  rintro ⟨D⟩
  rcases h with ⟨a, b, f, g, hQ, hS⟩
  exact hS (D.map_eq_of_quotient_map_eq f g hQ)

/-- Failure of kernel compatibility is already enough to rule out descent. -/
theorem noFundamentalDescent_of_not_kernelCompatible
    {Q : P ⥤ FundamentalGroupoid X}
    {S : P ⥤ Type v}
    (h : ¬ QuotientKernelCompatible Q S) :
    ¬ Nonempty (FundamentalDescent Q S) := by
  rintro ⟨D⟩
  exact h D.kernelCompatible

/-! ## Reversibility is logically separate from descent -/

/-- Package any fine transport as a KuuOS dependent-origination system. -/
def fineAsDependentOrigination
    (S : P ⥤ Type v) :
    FunctorialTransportSystem P where
  state := S

/--
If the fine context itself is a groupoid, its transport canonically lands in
`Core (Type)`, whether or not it descends through the ordinary fundamental
groupoid.
-/
noncomputable def fineCoreFunctor
    [Groupoid P]
    (S : P ⥤ Type v) :
    P ⥤ Core (Type v) :=
  FunctorialTransportSystem.coreStateFunctor (fineAsDependentOrigination S)

/-- Every fine transport arrow is invertible when the fine context is a groupoid. -/
theorem fineTransport_map_isIso
    [Groupoid P]
    (S : P ⥤ Type v)
    {a b : P} (f : a ⟶ b) :
    IsIso (S.map f) := by
  infer_instance

/--
The fine groupoid transport has an explicit equivalence along every arrow,
again without assuming ordinary-homotopy descent.
-/
noncomputable def fineTransportEquiv
    [Groupoid P]
    (S : P ⥤ Type v)
    {a b : P} (f : a ⟶ b) :
    S.obj a ≃ S.obj b :=
  (fineAsDependentOrigination S).transportEquiv f

end KUOS.DependentOriginationFundamentalGroupoidDescentObstructionV0_5
