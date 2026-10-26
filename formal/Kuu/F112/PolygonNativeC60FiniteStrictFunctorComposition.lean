import Kuu.F112.PolygonNativeC60FiniteStrictFullArrowAction

/-!
# F112-P94D3BF — composition of full C60 strict-context endofunctors

BE proved an equality on *every dependent strict-arrow bundle*, not only
on lower objects. BF promotes that equality to genuine functor equality
on the existing selected no-extra-relations strict Kuu quotient.

The order is important: an outer prefix is applied after the inner
context, so the strict functor of `outer ++ inner` is `inner ⋙ outer`.
The comparison includes all objects and all dependent homs via HEq,
extracted from BE's proof-relevant Σ-bundle equality.

This is a unary strict action of finite C60 contexts, not a proof of
binary whiskering, Peiffer interchange, original geometric 16-cell
coherence, global strict 3/n-category or hyperdescent. No Gray, no
new axioms, no sorry/admit or observational collapse.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u v uD vD uE vE

/-- Empty context is equality with the identity FUNCTOR, including
every hom. The arrow equality comes from the full dependent BE bundle. -/
theorem nativeC60BFStrictFunctor_nil {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L) :
    nativeC60BDNoRelations_strictFunctor S F [] =
      𝟭 (NativeC60AZStrictSpace (nativeC60BCClosedSignature S F)
        (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))) := by
  apply Functor.hext
  · rintro ⟨⟨x⟩⟩
    rfl
  · rintro ⟨⟨x⟩⟩ ⟨⟨y⟩⟩ f
    have h := nativeC60BEArrowContext_nil S F
      (⟨(x, y), f⟩ : NativeC60BEStrictArrowBundle S F)
    change (⟨(nativeC60BCContextTotal F [] x,
        nativeC60BCContextTotal F [] y),
        (nativeC60BDNoRelations_strictFunctor S F []).map f⟩ :
          NativeC60BEStrictArrowBundle S F) =
      ⟨(x, y), f⟩ at h
    exact (Sigma.mk.inj_iff.mp h).2

/-- TRUE equality of strict endofunctors, not just the agreement of
object maps. The target hom comparison uses BE's exact dependent
full-arrow equality and Sigma's heterogeneous projection. -/
theorem nativeC60BFStrictFunctor_append {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (outer inner : List Bool) :
    nativeC60BDNoRelations_strictFunctor S F (outer ++ inner) =
      nativeC60BDNoRelations_strictFunctor S F inner ⋙
        nativeC60BDNoRelations_strictFunctor S F outer := by
  apply Functor.hext
  · rintro ⟨⟨x⟩⟩
    change (nativeC60AZStrictProject (nativeC60BCClosedSignature S F)
        (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))).obj
          ⟨nativeC60BCContextTotal F (outer ++ inner) x⟩ =
      (nativeC60AZStrictProject (nativeC60BCClosedSignature S F)
        (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))).obj
          ⟨nativeC60BCContextTotal F outer
            (nativeC60BCContextTotal F inner x)⟩
    exact congrArg
      (fun a : L.Total =>
        (nativeC60AZStrictProject (nativeC60BCClosedSignature S F)
          (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))).obj ⟨a⟩)
      (nativeC60BCContextTotal_append F outer inner x)
  · rintro ⟨⟨x⟩⟩ ⟨⟨y⟩⟩ f
    have h := nativeC60BEArrowContext_append S F outer inner
      (⟨(x, y), f⟩ : NativeC60BEStrictArrowBundle S F)
    change (⟨(nativeC60BCContextTotal F (outer ++ inner) x,
        nativeC60BCContextTotal F (outer ++ inner) y),
        (nativeC60BDNoRelations_strictFunctor S F (outer ++ inner)).map f⟩ :
          NativeC60BEStrictArrowBundle S F) =
      ⟨(nativeC60BCContextTotal F outer
            (nativeC60BCContextTotal F inner x),
          nativeC60BCContextTotal F outer
            (nativeC60BCContextTotal F inner y)),
        (nativeC60BDNoRelations_strictFunctor S F outer).map
          ((nativeC60BDNoRelations_strictFunctor S F inner).map f)⟩ at h
    exact (Sigma.mk.inj_iff.mp h).2

/-- Each nonempty word is an exact composition of its singleton head
with its remaining strict context, over all strict hom-sets. -/
theorem nativeC60BFStrictFunctor_cons {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (side : Bool) (rest : List Bool) :
    nativeC60BDNoRelations_strictFunctor S F (side :: rest) =
      nativeC60BDNoRelations_strictFunctor S F rest ⋙
        nativeC60BDNoRelations_strictFunctor S F [side] :=
  nativeC60BFStrictFunctor_append S F [side] rest

section PhysicalC60

variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable {first : KuuNativeF45Tree p n m ma pa mb pb}
variable {last : KuuNativeF45Tree p n' m' ma pa mb pb}
variable {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
variable {f g : NativeF55StructuralComparison p r s}
variable {alpha beta : NativeK5StructuralFourCell p f g}
variable {w z : NativeK5StructuralFiveCell p alpha beta}
variable {u v : NativeK5StructuralSixCell p w z}
variable {h k : NativeK5StructuralSevenCell p u v}
variable {e d : NativeK5StructuralEightCell p h k}
variable {q t : NativeK5StructuralNineCell p e d}
variable {P Q : NativeK5StructuralTenCell p q t}
variable {H K : NativeK5StructuralElevenCell p P Q}
variable {U V : NativeK5StructuralTwelveCell p H K}

/-- Physical C60 strict endofunctors form a unital finite-word action. -/
theorem nativeK5BFPhysicalStrictContext_nil
    (W : NativeK5StructuralThirteenCell p U V) :
    nativeK5BDPhysicalStrictContext W [] =
      𝟭 (NativeC60AZStrictSpace (nativeK5BCSignature W)
        (nativeC60AZNoRelations (nativeK5BCSignature W))) :=
  nativeC60BFStrictFunctor_nil (nativeK5AXKuuSignature W) (nativeK5BCFrame W)

/-- Full genuine C60 FUNCTOR composition, carrying all original 15D
endpoints and all strict-realized typed 16D comparison arrows. -/
theorem nativeK5BFPhysicalStrictContext_append
    (W : NativeK5StructuralThirteenCell p U V)
    (outer inner : List Bool) :
    nativeK5BDPhysicalStrictContext W (outer ++ inner) =
      nativeK5BDPhysicalStrictContext W inner ⋙
        nativeK5BDPhysicalStrictContext W outer :=
  nativeC60BFStrictFunctor_append
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W) outer inner

/-- The full-word physical functor action remains covariant on actual
noncommutative AS Peiffer values (not an observational identification). -/
theorem nativeK5BFPhysicalStrictContext_composed_peiffer
    (W : NativeK5StructuralThirteenCell p U V)
    (outer inner : List Bool)
    (c : (nativeK5AXBaseLayer W).Total) :
    nativeK5AXPeiffer W
      ((nativeK5BDPhysicalStrictContext W inner ⋙
        nativeK5BDPhysicalStrictContext W outer).obj
        ((nativeC60AZStrictProject (nativeK5BCSignature W)
          (nativeC60AZNoRelations (nativeK5BCSignature W))).obj ⟨c⟩)).as.val =
      nativeK5ASPeifferAct W (nativeK5ATGaugeWord W (outer ++ inner))
        (nativeK5AXPeiffer W c) := by
  change nativeK5AXPeiffer W
    (nativeC60BCContextTotal (nativeK5BCFrame W) outer
      (nativeC60BCContextTotal (nativeK5BCFrame W) inner c)) =
    nativeK5ASPeifferAct W (nativeK5ATGaugeWord W (outer ++ inner))
      (nativeK5AXPeiffer W c)
  rw [← nativeC60BCContextTotal_append (nativeK5BCFrame W) outer inner c]
  exact nativeK5BCContext_peiffer W (outer ++ inner) c

end PhysicalC60

#print axioms nativeC60BFStrictFunctor_nil
#print axioms nativeC60BFStrictFunctor_append
#print axioms nativeC60BFStrictFunctor_cons
#print axioms nativeK5BFPhysicalStrictContext_nil
#print axioms nativeK5BFPhysicalStrictContext_append
#print axioms nativeK5BFPhysicalStrictContext_composed_peiffer

end
end Kuu.F112.Physical
