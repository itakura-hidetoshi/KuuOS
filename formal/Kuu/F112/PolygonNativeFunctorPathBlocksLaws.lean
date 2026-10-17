import Kuu.F112.PolygonNativeF45ExchangePacketNaturality

/-!
# F112-E7Q5-F4-O1 — independent F36/F40 functor identity and composition

Identity and composition of the actual recursively typed native
categorical paths and their F40 subdivision Blocks are proved
BEFORE any flattening, proof erasure, exchange quotient or numerical
shadow.  All arrow witnesses and block boundaries remain in Type.

These are strict laws for the independently reconstructed source,
not claims of equivalence with frozen historical KUOS/Gray sources.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
noncomputable section

universe uA vA uB vB uC vC
variable {A : Type uA} [Category.{vA} A]
variable {B : Type uB} [Category.{vB} B]
variable {C : Type uC} [Category.{vC} C]

/-- The independent native finite-arrow source is strictly
unchanged when transported along the identity ordinary functor. -/
theorem KuuNativePath.map_id
    {a b : A} (p : KuuNativePath a b) :
    p.map (𝟭 A) = p := by
  induction p with
  | nil =>
      simp only [KuuNativePath.map, Functor.id_obj]
  | snoc p f ih =>
      simp only [KuuNativePath.map, Functor.id_obj, Functor.id_map, ih]

/-- The same raw finite-path source is compatible with arbitrary
composable category functors, without evaluating its composite Hom. -/
theorem KuuNativePath.map_comp
    (F : A ⥤ B) (G : B ⥤ C)
    {a b : A} (p : KuuNativePath a b) :
    p.map (F ⋙ G) = (p.map F).map G := by
  induction p with
  | nil =>
      simp only [KuuNativePath.map, Functor.comp_obj]
  | snoc p f ih =>
      simp only [KuuNativePath.map, Functor.comp_obj, Functor.comp_map, ih]

/-- Original-shaped F40 Blocks preserve every primitive native
subdivision separator even along the identity functor. -/
theorem KuuNativeBlocks.map_id
    {a b : A} (p : KuuNativeBlocks a b) :
    p.map (𝟭 A) = p := by
  induction p with
  | empty =>
      simp only [KuuNativeBlocks.map, Functor.id_obj]
  | snoc p q ih =>
      simp only [KuuNativeBlocks.map, Functor.id_obj, KuuNativePath.map_id, ih]

/-- Functor composition on F40 Blocks is also strictly compatible
with both the original nested categorical paths and all partitions. -/
theorem KuuNativeBlocks.map_comp
    (F : A ⥤ B) (G : B ⥤ C)
    {a b : A} (p : KuuNativeBlocks a b) :
    p.map (F ⋙ G) = (p.map F).map G := by
  induction p with
  | empty =>
      simp only [KuuNativeBlocks.map, Functor.comp_obj]
  | snoc p q ih =>
      simp only [KuuNativeBlocks.map, Functor.comp_obj,
        KuuNativePath.map_comp, ih]

#print axioms KuuNativePath.map_id
#print axioms KuuNativePath.map_comp
#print axioms KuuNativeBlocks.map_id
#print axioms KuuNativeBlocks.map_comp
end
end Kuu.F112.Physical
