import KUOS.DependentOriginationCoherentBiadjunctionDoubleFiniteNonstrictMatesV5_135

namespace KUOS.DependentOriginationCoherentBiadjunctionDoubleFinitePastingCoreV5_136

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans

open KUOS.DependentOriginationCoherentBiadjunctionFiniteHorizontalExchangeV5_133
open KUOS.DependentOriginationCoherentBiadjunctionFiniteModificationMatePathsV5_135
open KUOS.DependentOriginationCoherentBiadjunctionFiniteModificationMatePathsV5_135.Generic
open KUOS.DependentOriginationCoherentBiadjunctionChosenRightMateCategoriesV5_116.Generic

set_option autoImplicit false
noncomputable section

/-!
# F39-A/v5.136 — arbitrary finite strong-modification pastings

F19's ACTUAL chosen-adjunction presentation category supplies original
StrongTrans.Modification arrows. The F36 native categorical finite-path
carrier stores those arrows and their endpoints, while F38's mapPath
carries them through the original contravariant chosen right-mate functor.

Every finite split and binary parenthesization is independent, including
zero-length paths; on the original right lax mates, vertical composition
reverses in the prescribed mathematical direction without an inverse of
an arbitrary modification or any G comparison 2-cell.

No original adjunction, mapId/mapComp or right mate is altered.
-/

namespace Finite

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

/-- Three arbitrary finite pieces are transported as their own
three independently composable parts, not as selected singleton arrows. -/
theorem mapPath_triple_split (H : D ⥤ E)
    {a b c d : D}
    (p : Chain.Path a b) (q : Chain.Path b c) (r : Chain.Path c d) :
    (mapPath H ((p.append q).append r)).composite =
      ((mapPath H p).composite ≫ (mapPath H q).composite) ≫
        (mapPath H r).composite := by
  simp only [mapPath_append, Chain.Path.composite_append]

/-- All binary parenthesizations of the SAME finite native arrow
sequence evaluate to the same transported morphism. -/
theorem mapBracketing_independent (H : D ⥤ E)
    {a b : D} (p q : Chain.Bracketing a b)
    (h : p.flattened = q.flattened) :
    (mapBracketing H p).evaluated =
      (mapBracketing H q).evaluated := by
  calc
    (mapBracketing H p).evaluated = H.map p.evaluated :=
      mapBracketing_evaluated H p
    _ = H.map q.evaluated :=
      congrArg (fun t => H.map t) (Chain.Bracketing.independent p q h)
    _ = (mapBracketing H q).evaluated :=
      (mapBracketing_evaluated H q).symm

end Finite

namespace Generic

universe uB vB wB uC vC wC
variable {B : Type uB} [Bicategory.{wB, vB} B]
variable {C : Type uC} [Bicategory.{wC, vC} C]
variable (F G : Pseudofunctor B C)

/-- The original right lax mate of three arbitrary finite strong
modification segments is their ACTUAL vertical composition in
reverse order; this is the native F19 contravariant correspondence. -/
theorem chosenRightMateTripleModificationSplit
    {a b c d : LeftMatePresentation F G}
    (p : Chain.Path a b) (q : Chain.Path b c)
    (r : Chain.Path c d) :
    (rightMateFunctor F G).map (((p.append q).append r).composite) =
      Oplax.LaxTrans.Modification.vcomp
        ((rightMateFunctor F G).map r.composite)
        (Oplax.LaxTrans.Modification.vcomp
          ((rightMateFunctor F G).map q.composite)
          ((rightMateFunctor F G).map p.composite)) := by
  simp only [Chain.Path.composite_append]
  calc
    (rightMateFunctor F G).map
        ((p.composite ≫ q.composite) ≫ r.composite) =
      Oplax.LaxTrans.Modification.vcomp
        ((rightMateFunctor F G).map r.composite)
        ((rightMateFunctor F G).map (p.composite ≫ q.composite)) :=
      chosenRightMateTwoModificationVcomp F G
        (p.composite ≫ q.composite) r.composite
    _ = _ := congrArg
      (fun m => Oplax.LaxTrans.Modification.vcomp
        ((rightMateFunctor F G).map r.composite) m)
      (chosenRightMateTwoModificationVcomp F G
        p.composite q.composite)

/-- All independently chosen binary pastings of the same ordered
original strong-modification list give the same genuine RIGHT
lax-modification (as an arrow of F19's right-opposite category). -/
theorem chosenRightMateBracketingsIndependent
    {a b : LeftMatePresentation F G}
    (p q : Chain.Bracketing a b)
    (h : p.flattened = q.flattened) :
    (Finite.mapBracketing (rightMateFunctor F G) p).evaluated =
      (Finite.mapBracketing (rightMateFunctor F G) q).evaluated :=
  Finite.mapBracketing_independent (rightMateFunctor F G) p q h

#print axioms Finite.mapPath_triple_split
#print axioms Finite.mapBracketing_independent
#print axioms chosenRightMateTripleModificationSplit
#print axioms chosenRightMateBracketingsIndependent

end Generic
end

end KUOS.DependentOriginationCoherentBiadjunctionDoubleFinitePastingCoreV5_136
