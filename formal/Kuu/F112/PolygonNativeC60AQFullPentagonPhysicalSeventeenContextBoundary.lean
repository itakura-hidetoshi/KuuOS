import Kuu.F112.PolygonNativeC60AQFullPentagonSeventeenContextFiberObstruction

/-!
# F112-P94D3FD — finite physical AQ trees and exact 17D-object fiber gate

Specialize FD's 17D contextual object-fiber obstruction to the ACTUAL
chronological word of a finite K5/C60 AQ context tree. The target
remains DV's separately context-closed 18D presentation, not an
invented original geometric 19D filler.

If two distinct ORIGINAL dependent 17D objects collapse after the
actual DR finite tree action, their three-reflexivity original 18D
associator codes collide and generate an explicit nontrivial
unquotiented original FreeGroup kernel element. Conversely full
faithfulness necessarily implies injectivity on every underlying
17D tree-context object. Neither direction asserts a collision
exists in every frame, or asserts full DV faithfulness without proof.

Chronologically identical AQ trees are stable under reparenthesization.
No new proof roots, axioms/sorry/admit, Gray or abelianization.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u

section ActualFiniteTreeObjectFiber

variable {L : NativeC60AXLayer.{u}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- A genuine AQ context tree whose full DV signed word transport is
injective MUST act injectively on actual original dependent 17D
objects. This is a necessary condition, not an unproved assumption. -/
theorem nativeC60FDActualTree_context_injective_necessary
    (tree : NativeK5DOContextTree)
    (htransport : Function.Injective (nativeC60DVFullWordTransport S F
      (nativeK5DOTreeWord tree))) :
    Function.Injective (nativeC60BCContextTotal
      (nativeC60DRSeventeenFrame S F) (nativeK5DOTreeWord tree)) :=
  nativeC60FDContext_injective_of_DVTransport_injective S F
    (nativeK5DOTreeWord tree) htransport

/-- The ORIGINAL 17D objects of a real finite AQ context can be used
to name an explicit (conditionally existing) nontrivial signed
two-letter 18D kernel witness; these are not invented quotient
generators or parity classes. -/
theorem nativeC60FDActualTree_fiber_kernel_witness
    (tree : NativeK5DOContextTree)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (hne : a ≠ b)
    (hab : nativeC60BCContextTotal
        (nativeC60DRSeventeenFrame S F)
          (nativeK5DOTreeWord tree) a =
      nativeC60BCContextTotal
        (nativeC60DRSeventeenFrame S F)
          (nativeK5DOTreeWord tree) b) :
    ∃ z : NativeC60DTFullFree S F,
      z ≠ 1 ∧
        (nativeC60DVFullWordTransport S F (nativeK5DOTreeWord tree)) z = 1 := by
  let z := nativeC60FCCodeFiberDefect S F
    (nativeC60FDAssocReflCode S F a)
    (nativeC60FDAssocReflCode S F b)
  have hz := nativeC60FDContextCollision_nontrivial_kernel S F
    (nativeK5DOTreeWord tree) hne hab
  exact ⟨z, hz.1, hz.2⟩

/-- Any real finite AQ tree with noninjective 17D-object context
action fails to give an injective unquotiented original-to-closed
DV full FreeGroup transport. Not an unconditional existence claim. -/
theorem nativeC60FDActualTree_context_obstruction
    (tree : NativeK5DOContextTree)
    (hcontext : ¬ Function.Injective (nativeC60BCContextTotal
      (nativeC60DRSeventeenFrame S F) (nativeK5DOTreeWord tree))) :
    ¬ Function.Injective
      (nativeC60DVFullWordTransport S F (nativeK5DOTreeWord tree)) :=
  nativeC60FDNotContextInjective_blocks_DVTransport S F
    (nativeK5DOTreeWord tree) hcontext

/-- Genuine AQ tree regrouping does not modify the chronological
word, hence cannot introduce or remove the 17D object-fiber
injectivity gate established above. -/
theorem nativeC60FDActualTree_context_injective_refinement
    {left right : NativeK5DOContextTree}
    (hsteps : nativeK5DOTreeSteps left = nativeK5DOTreeSteps right) :
    Function.Injective (nativeC60BCContextTotal
      (nativeC60DRSeventeenFrame S F) (nativeK5DOTreeWord left)) ↔
    Function.Injective (nativeC60BCContextTotal
      (nativeC60DRSeventeenFrame S F) (nativeK5DOTreeWord right)) := by
  rw [nativeK5DOTreeWord_eq_of_steps_eq hsteps]

end ActualFiniteTreeObjectFiber

#print axioms nativeC60FDActualTree_context_injective_necessary
#print axioms nativeC60FDActualTree_fiber_kernel_witness
#print axioms nativeC60FDActualTree_context_obstruction
#print axioms nativeC60FDActualTree_context_injective_refinement

end
end Kuu.F112.Physical
