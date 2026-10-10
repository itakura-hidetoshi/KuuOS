import KUOS.DependentOriginationCoherentBiadjunctionActualLiftFiniteHexagonV5_134
import KUOS.DependentOriginationCoherentBiadjunctionChosenRightMateCategoriesV5_116

namespace KUOS.DependentOriginationCoherentBiadjunctionFiniteModificationMatePathsV5_135

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionFiniteHorizontalExchangeV5_133
open KUOS.DependentOriginationCoherentBiadjunctionChosenRightMateCategoriesV5_116.Generic
open KUOS.DependentOriginationCoherentBiadjunctionAutomaticModificationMatesV5_114.Generic

set_option autoImplicit false
noncomputable section

/-!
# F38-A/v5.135: arbitrary finite VERTICAL strong-modification paths

The original F19 chosen-right-mate presentation category has genuine
StrongTrans.Modification homs, not merely component 2-cells. Its right
mate functor maps into the OPPOSITE presentation category; thus every
vertical composition of original strong modifications reverses as a
composition of the original right lax modifications. The finite path
carrier is the F36 category-valued carrier, but its source category is
F19's chosen strong-modification CATEGORY, NOT F28's quotient category.

We prove functoriality of arbitrary finite paths by structural induction,
including empty paths, concatenation and all binary parenthesizations.
-/

namespace Finite

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

/-- Map each genuine categorical arrow in a finite path through a
functor, keeping all intermediate objects and without using any inverse. -/
def mapPath (H : D ⥤ E) : ∀ {x y : D},
    Chain.Path x y → Chain.Path (H.obj x) (H.obj y)
  | _, _, .nil x => Chain.Path.nil (H.obj x)
  | _, _, .snoc p q => Chain.Path.snoc (mapPath H p) (H.map q)

/-- Evaluation COMMUTES with arbitrary finite-path transport, by
induction, including the original nontrivial functor mapId/mapComp. -/
theorem mapPath_composite (H : D ⥤ E) {x y : D}
    (p : Chain.Path x y) :
    (mapPath H p).composite = H.map p.composite := by
  induction p with
  | nil =>
      simp only [mapPath, Chain.Path.composite, H.map_id]
  | @snoc mid fin p q ih =>
      simpa only [mapPath, Chain.Path.composite, H.map_comp, ih]

/-- Categorical finite-path transport respects every finite split,
without assuming that the functor is strict on its objects. -/
theorem mapPath_append (H : D ⥤ E) {x y z : D}
    (p : Chain.Path x y) (q : Chain.Path y z) :
    mapPath H (p.append q) =
      (mapPath H p).append (mapPath H q) := by
  induction q with
  | nil =>
      simp only [Chain.Path.append, mapPath]
  | @snoc mid fin q r ih =>
      simp only [Chain.Path.append, mapPath, ih]

/-- Transport ALL (including empty and nested) binary parenthesizations
without dropping their actual input 1-cells. -/
def mapBracketing (H : D ⥤ E) : ∀ {x y : D},
    Chain.Bracketing x y → Chain.Bracketing (H.obj x) (H.obj y)
  | _, _, .empty x => Chain.Bracketing.empty (H.obj x)
  | _, _, .arrow q => Chain.Bracketing.arrow (H.map q)
  | _, _, .paste p q => Chain.Bracketing.paste
      (mapBracketing H p) (mapBracketing H q)

/-- Evaluating any transported binary bracketing equals mapping its
original evaluation: categorical pentagon/triangle coherence is
retained through the native functor axioms. -/
theorem mapBracketing_evaluated (H : D ⥤ E) {x y : D}
    (p : Chain.Bracketing x y) :
    (mapBracketing H p).evaluated = H.map p.evaluated := by
  induction p with
  | empty =>
      simp only [mapBracketing, Chain.Bracketing.evaluated, H.map_id]
  | arrow q =>
      simp only [mapBracketing, Chain.Bracketing.evaluated]
  | paste p q ihp ihq =>
      simpa only [mapBracketing, Chain.Bracketing.evaluated,
        H.map_comp, ihp, ihq]

/-- The transported binary tree has EXACTLY the same flattened
finite path as transporting the original flattened path. -/
theorem mapBracketing_flattened (H : D ⥤ E) {x y : D}
    (p : Chain.Bracketing x y) :
    (mapBracketing H p).flattened =
      mapPath H p.flattened := by
  induction p with
  | empty =>
      simp only [mapBracketing, Chain.Bracketing.flattened, mapPath]
  | arrow q =>
      simp only [mapBracketing, Chain.Bracketing.flattened, mapPath]
  | paste p q ihp ihq =>
      simp only [mapBracketing, Chain.Bracketing.flattened,
        mapPath_append, ihp, ihq]

end Finite

namespace Generic

universe uB vB wB uC vC wC
variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]
variable (F G : Pseudofunctor B C)

/-- Arbitrarily many original strong-modification vertical compositions
transport EXACTLY to the original F19 right-opposite category, i.e.
composition of original lax right-mate modifications in reverse order. -/
theorem chosenRightMateFiniteModificationPath
    {a b : LeftMatePresentation F G}
    (p : Chain.Path a b) :
    (Finite.mapPath (rightMateFunctor F G) p).composite =
      (rightMateFunctor F G).map p.composite :=
  Finite.mapPath_composite (rightMateFunctor F G) p

/-- The original right mate is contravariant on ACTUAL modification
composition, without inverting Γ, Δ or any G-side comparison cell. -/
theorem chosenRightMateTwoModificationVcomp
    {a b c : LeftMatePresentation F G}
    (Γ : a ⟶ b) (deltaMod : b ⟶ c) :
    (rightMateFunctor F G).map (Γ ≫ deltaMod) =
      Oplax.LaxTrans.Modification.vcomp
        ((rightMateFunctor F G).map deltaMod)
        ((rightMateFunctor F G).map Γ) := by
  exact rightModification_vcomp
    a.core.datum b.core.datum c.core.datum Γ deltaMod

/-- All finite splits of ORIGINAL strong-modification sequences remain
valid under the chosen right-mate contravariant functor. -/
theorem chosenRightMateFiniteModificationAppend
    {a b c : LeftMatePresentation F G}
    (p : Chain.Path a b) (q : Chain.Path b c) :
    (Finite.mapPath (rightMateFunctor F G) (p.append q)).composite =
      (rightMateFunctor F G).map
        (p.composite ≫ q.composite) := by
  rw [chosenRightMateFiniteModificationPath F G,
    Chain.Path.composite_append]

/-- Every parenthesization of the SAME original strong-modification
sequence yields the same contravariant right-mate modification. -/
theorem chosenRightMateBracketedModification
    {a b : LeftMatePresentation F G}
    (p : Chain.Bracketing a b) :
    (Finite.mapBracketing (rightMateFunctor F G) p).evaluated =
      (rightMateFunctor F G).map p.evaluated :=
  Finite.mapBracketing_evaluated (rightMateFunctor F G) p

#print axioms Finite.mapPath
#print axioms Finite.mapPath_composite
#print axioms Finite.mapPath_append
#print axioms Finite.mapBracketing
#print axioms Finite.mapBracketing_evaluated
#print axioms Finite.mapBracketing_flattened
#print axioms chosenRightMateFiniteModificationPath
#print axioms chosenRightMateTwoModificationVcomp
#print axioms chosenRightMateFiniteModificationAppend
#print axioms chosenRightMateBracketedModification

end Generic
end

end KUOS.DependentOriginationCoherentBiadjunctionFiniteModificationMatePathsV5_135
