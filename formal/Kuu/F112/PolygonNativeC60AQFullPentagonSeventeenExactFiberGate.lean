import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalSeventeenContextBoundary

/-!
# F112-P94D3FE — exact original 17D object-fiber / full 18D code-reflection gate

FD constructs the real original fully dependent three-reflexivity 18D
associator code for every original 17D object, and proves that
collisions after the actual DR finite context action force
nontrivial kernel elements in DV's unquotiented complete free group.

FE strengthens this to a CONVERSE:
the real target closed 18D reflexive associator preserves its entire
target 17D object, so two of these transported full 18D codes are
identical IFF the original 17D objects have identical CONTEXT IMAGES.

We also prove that the actual signed two-letter source defect lies
in the true full DV kernel IFF those two contextual objects collide,
and that finite C60 context object injectivity over ALL words reduces
exactly to two genuine singleton DR frame injectivity conditions.

These are exact results on an actual nontrivial class of complete
dependent 18D generator codes, NOT an assertion of global code
injectivity or an assumption that the C60 frames are injective.
The full arbitrary-17D-path and arbitrary-18D-whiskering faithfulness
gates remain separate. All original Type-valued 14D–18D witnesses,
DS no-go and the relative closed target remain. Strict Kuu primary,
independent Kuu a presentation, 107 roots, no Gray, no new
axioms/sorry/admit. Append-only, tighten-only, same-root.
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

section ExactOriginalSeventeenFibers

variable {L : NativeC60AXLayer.{u}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- Exact recovery of the COMPLETE target 17D object from a genuine
closed 18D associator with three original transported reflexivities.
The full original dependent generator is retained; no observer shadow. -/
theorem nativeC60FEClosedAssocReflCode_injective :
    Function.Injective (nativeC60FDClosedAssocReflCode S F) := by
  intro a b hab
  have h := congrArg
    (fun code : NativeC60DVCompleteEighteenCode S F => code.1.1.1) hab
  exact h

/-- EXACT 17D-OBJECT FIBER CRITERION: the images of two original
complete 18D associator codes are equal IFF their underlying original
17D objects have the same real DR finite C60 contextual image. -/
theorem nativeC60FEAssocReflCode_collision_iff
    (word : List Bool)
    (a b : (nativeC60DQSeventeenLayer S F).Total) :
    nativeC60DVTransportCompleteCode S F word
        (nativeC60FDAssocReflCode S F a) =
      nativeC60DVTransportCompleteCode S F word
        (nativeC60FDAssocReflCode S F b) ↔
      nativeC60BCContextTotal (nativeC60DRSeventeenFrame S F) word a =
        nativeC60BCContextTotal (nativeC60DRSeventeenFrame S F) word b := by
  constructor
  · intro hab
    rw [nativeC60FDAssocReflCode_transport S F word a,
      nativeC60FDAssocReflCode_transport S F word b] at hab
    exact nativeC60FEClosedAssocReflCode_injective S F hab
  · intro hab
    exact nativeC60FDContextCollision_codes S F word hab

/-- Complete CODE faithfulness RESTRICTED to actual reflexivity
associators is IFF injectivity of the actual underlying 17D context
object map. It is intentionally not global code-map faithfulness. -/
theorem nativeC60FEAssocReflCodes_injective_iff_context
    (word : List Bool) :
    Function.Injective
      (fun a : (nativeC60DQSeventeenLayer S F).Total =>
        nativeC60DVTransportCompleteCode S F word
          (nativeC60FDAssocReflCode S F a)) ↔
    Function.Injective
      (nativeC60BCContextTotal (nativeC60DRSeventeenFrame S F) word) := by
  constructor
  · intro hc a b hab
    apply hc
    exact (nativeC60FEAssocReflCode_collision_iff S F word a b).mpr hab
  · intro hctx a b hab
    apply hctx
    exact (nativeC60FEAssocReflCode_collision_iff S F word a b).mp hab

/-- Exact two-letter ORIGINAL FreeGroup obstruction, with the reverse
direction obtained from genuine free-generator injectivity, not
by confusing the target relative quotient with DV's full free group. -/
theorem nativeC60FEAssocReflDefect_maps_one_iff
    (word : List Bool)
    (a b : (nativeC60DQSeventeenLayer S F).Total) :
    (nativeC60DVFullWordTransport S F word)
        (nativeC60FCCodeFiberDefect S F
          (nativeC60FDAssocReflCode S F a)
          (nativeC60FDAssocReflCode S F b)) = 1 ↔
      nativeC60BCContextTotal (nativeC60DRSeventeenFrame S F) word a =
        nativeC60BCContextTotal (nativeC60DRSeventeenFrame S F) word b := by
  constructor
  · intro h
    apply (nativeC60FEAssocReflCode_collision_iff S F word a b).mp
    apply FreeGroup.of_injective
    change (nativeC60DVFullWordTransport S F word)
      (FreeGroup.of (nativeC60FDAssocReflCode S F a) *
        (FreeGroup.of (nativeC60FDAssocReflCode S F b))⁻¹) = 1 at h
    rw [map_mul, map_inv,
      nativeC60DVFullWordTransport_of S F word,
      nativeC60DVFullWordTransport_of S F word] at h
    exact eq_of_mul_inv_eq_one h
  · intro hab
    exact nativeC60FCCodeFiberDefect_maps_one S F word
      ((nativeC60FEAssocReflCode_collision_iff S F word a b).mpr hab)

/-- The exact subgroup KERNEL test for genuine original dependent
reflexive-associator defects; not an arbitrary scalar or parity test. -/
theorem nativeC60FEAssocReflDefect_mem_kernel_iff
    (word : List Bool)
    (a b : (nativeC60DQSeventeenLayer S F).Total) :
    nativeC60FCCodeFiberDefect S F
        (nativeC60FDAssocReflCode S F a)
        (nativeC60FDAssocReflCode S F b) ∈
      (nativeC60DVFullWordTransport S F word).ker ↔
      nativeC60BCContextTotal (nativeC60DRSeventeenFrame S F) word a =
        nativeC60BCContextTotal (nativeC60DRSeventeenFrame S F) word b := by
  rw [MonoidHom.mem_ker]
  exact nativeC60FEAssocReflDefect_maps_one_iff S F word a b

end ExactOriginalSeventeenFibers

/-- All finite context OBJECT actions are injective if and only if
the TWO GENUINE singleton frame actions are injective. The original
chronological order (head applied outermost) is preserved. This does
not assert either singleton hypothesis in arbitrary C60 frames. -/
theorem nativeC60FEAllBCContexts_injective_iff_singletons
    {L : NativeC60AXLayer.{u}}
    (F : Bool → NativeC60BCFrame L) :
    (∀ word : List Bool, Function.Injective (nativeC60BCContextTotal F word)) ↔
      Function.Injective ((F false).mapTotal) ∧
      Function.Injective ((F true).mapTotal) := by
  constructor
  · intro hall
    exact ⟨hall [false], hall [true]⟩
  · rintro ⟨hf, ht⟩ word
    induction word with
    | nil =>
        intro a b hab
        exact hab
    | cons side rest ih =>
        intro a b hab
        change (F side).mapTotal (nativeC60BCContextTotal F rest a) =
          (F side).mapTotal (nativeC60BCContextTotal F rest b) at hab
        apply ih
        cases side with
        | false => exact hf hab
        | true => exact ht hab

section ActualTwoFrameGate

variable {L : NativeC60AXLayer.{u}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- EXACT ALL-FINITE-WORD GATE on the original reflexivity
18D associator sector, reduced to the two genuine DR 17D singleton
frames. This retains all original 14D–18D Type-valued histories. -/
theorem nativeC60FEAllAssocReflCodes_injective_iff_singletons :
    (∀ word : List Bool,
      Function.Injective
        (fun a : (nativeC60DQSeventeenLayer S F).Total =>
          nativeC60DVTransportCompleteCode S F word
            (nativeC60FDAssocReflCode S F a))) ↔
      Function.Injective ((nativeC60DRSeventeenFrame S F false).mapTotal) ∧
      Function.Injective ((nativeC60DRSeventeenFrame S F true).mapTotal) := by
  constructor
  · intro hall
    exact (nativeC60FEAllBCContexts_injective_iff_singletons
      (nativeC60DRSeventeenFrame S F)).mp
      (fun word =>
        (nativeC60FEAssocReflCodes_injective_iff_context S F word).mp
          (hall word))
  · intro hsingle word
    exact (nativeC60FEAssocReflCodes_injective_iff_context S F word).mpr
      ((nativeC60FEAllBCContexts_injective_iff_singletons
        (nativeC60DRSeventeenFrame S F)).mpr hsingle word)

/-- A NECESSARY physical 17D singleton condition for global full
unquotiented DV faithfulness over every finite AQ word. The converse
is explicitly NOT claimed for arbitrary original 18D codes. -/
theorem nativeC60FEAllDVTransport_injective_implies_frames
    (hall : ∀ word : List Bool,
      Function.Injective (nativeC60DVFullWordTransport S F word)) :
    Function.Injective ((nativeC60DRSeventeenFrame S F false).mapTotal) ∧
    Function.Injective ((nativeC60DRSeventeenFrame S F true).mapTotal) := by
  exact (nativeC60FEAllBCContexts_injective_iff_singletons
    (nativeC60DRSeventeenFrame S F)).mp
    (fun word =>
      nativeC60FDContext_injective_of_DVTransport_injective S F word
        (hall word))

end ActualTwoFrameGate

#print axioms nativeC60FEClosedAssocReflCode_injective
#print axioms nativeC60FEAssocReflCode_collision_iff
#print axioms nativeC60FEAssocReflCodes_injective_iff_context
#print axioms nativeC60FEAssocReflDefect_maps_one_iff
#print axioms nativeC60FEAssocReflDefect_mem_kernel_iff
#print axioms nativeC60FEAllBCContexts_injective_iff_singletons
#print axioms nativeC60FEAllAssocReflCodes_injective_iff_singletons
#print axioms nativeC60FEAllDVTransport_injective_implies_frames

end
end Kuu.F112.Physical
