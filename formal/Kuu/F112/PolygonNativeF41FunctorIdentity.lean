import Kuu.F112.PolygonNativeF41DependentWhiskerPacket

/-!
# F112-E7Q5-F4-O2-B — ALL nested original F41 primitives satisfy identity

The previous O2-A source certified the two primitive root cases:
split and insertNil. O2-B additionally constructs a genuinely
Type-valued, dependent-cast-aware whisker congruence and proves
the actual mapped whisker constructor agrees heterogeneously
with the whisker of the mapped Type-valued primitive witness.

We use both facts to prove arbitrary nested whisker depth by
induction, WITHOUT collapsing the primitive proof to Prop and
without assuming that the two indexed OneStep types are
definitionally identical. No historical KUOS/Gray imports.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
noncomputable section

universe uA vA
variable {A : Type uA} [Category.{vA} A]

/-- For EVERY Type-valued F41 primitive witness, including any
finite depth of nested whisker constructors, the actual
independently defined functor map along the identity is HEq to
the original proof term. This is structural proof relevance,
not equality inferred from the endpoints. -/
theorem KuuNativeOneStep.map_id_heq
    {a b : A} {p q : KuuNativeBlocks a b}
    (h : KuuNativeOneStep p q) :
    HEq (h.map (𝟭 A)) h := by
  induction h with
  | split p q r =>
      exact KuuNativeOneStep.map_id_split_heq p q r
  | insertNil p =>
      exact KuuNativeOneStep.map_id_insertNil_heq p
  | whisker h t ih =>
      obtain ⟨hp, hq⟩ := KuuNativeOneStep.map_id_endpoints h
      exact
        (KuuNativeOneStep.map_whisker_heq (𝟭 A) h t).trans
          (KuuNativeOneStep.whisker_heq_of_heq
            (h.map (𝟭 A)) h hp hq ih (KuuNativePath.map_id t))

#print axioms KuuNativeOneStep.map_id_heq
end
end Kuu.F112.Physical
