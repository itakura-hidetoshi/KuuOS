import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalKernelBoundary

/-!
# F112-P94D3FD — real 17D object fibers obstruct faithful typed 18D transport

The ACTUAL DR/DV transport on raw 17D paths is BC's finite original
context map into a distinct context-closed 17D signature. Although each
closed atom remembers its whole original typed generator and context word,
arbitrary C60 frame actions are NOT assumed injective on 17D objects.

For each ORIGINAL 17D object construct the ORIGINAL fully dependent 18D
associator on its three raw reflexive 17D paths. Distinct original objects
produce distinct source complete 18D codes. Their real DV transports are
DEFINITIONALLY the target associator on the respective transported object.

Hence any *specific* collision of 17D contextual objects yields:
* an exact collision of distinct ORIGINAL complete 18D generator codes;
* a nontrivial ORIGINAL signed two-letter FreeGroup element in the
  KERNEL of the actual unquotiented DV transport;
* the necessary 17D-object injectivity condition for global complete
  typed-code or full original FreeGroup transport injectivity.

This is a conditional physical obstruction, not a claim that a particular
C60 frame has a collision, nor a claimed proof of unconditional code
injectivity. All original Type-valued 14D–18D proof histories, DS no-go,
relative-target boundaries, strict/independent Kuu distinction, 107 roots
and no-Gray restriction remain unchanged. Append only, same root, no
axiom/sorry/admit.
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

section OriginalSeventeenObjectFiber

variable {L : NativeC60AXLayer.{u}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- An ORIGINAL fully typed 18D generator. It is the true DR associator
of three identity raw 17D paths at the given original 17D object. -/
def nativeC60FDAssocReflCode
    (a : (nativeC60DQSeventeenLayer S F).Total) :
    NativeC60DSCompleteEighteenCode S F :=
  nativeC60DSCode S F (.assoc (.refl a) (.refl a) (.refl a))

/-- The target is the actual separate DV context-CLOSED 18D signature;
its associated 17D identities are not scalar shadows or quotients. -/
def nativeC60FDClosedAssocReflCode
    (a : (nativeC60DQSeventeenLayer S F).Total) :
    NativeC60DVCompleteEighteenCode S F :=
  ⟨nativeC60DVPackClosedSeventeen S F
      (.trans (.trans (.refl a) (.refl a)) (.refl a)),
    nativeC60DVPackClosedSeventeen S F
      (.trans (.refl a) (.trans (.refl a) (.refl a))),
    .assoc (.refl a) (.refl a) (.refl a)⟩

/-- Original source complete-code letters remember the EXACT original
17D object even in the reflexive case. A collision is impossible in
the original grammar before context transport. -/
theorem nativeC60FDAssocReflCode_injective :
    Function.Injective (nativeC60FDAssocReflCode S F) := by
  intro a b hab
  have h := congrArg
    (fun code : NativeC60DSCompleteEighteenCode S F => code.1.1.1) hab
  exact h

/-- Computation of ACTUAL DV code transport by recursion on the
original DR 18D associator and the real BC 17D context action. -/
theorem nativeC60FDAssocReflCode_transport
    (word : List Bool)
    (a : (nativeC60DQSeventeenLayer S F).Total) :
    nativeC60DVTransportCompleteCode S F word
        (nativeC60FDAssocReflCode S F a) =
      nativeC60FDClosedAssocReflCode S F
        (nativeC60BCContextTotal (nativeC60DRSeventeenFrame S F) word a) := by
  rfl

/-- Every explicit collision of actual transported 17D OBJECTS,
including all of their lower 16D/15D dependent data, forces an
equality of transported COMPLETE 18D code letters. -/
theorem nativeC60FDContextCollision_codes
    (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (hab : nativeC60BCContextTotal
        (nativeC60DRSeventeenFrame S F) word a =
      nativeC60BCContextTotal (nativeC60DRSeventeenFrame S F) word b) :
    nativeC60DVTransportCompleteCode S F word
        (nativeC60FDAssocReflCode S F a) =
      nativeC60DVTransportCompleteCode S F word
        (nativeC60FDAssocReflCode S F b) := by
  rw [nativeC60FDAssocReflCode_transport S F word a,
    nativeC60FDAssocReflCode_transport S F word b]
  exact congrArg (nativeC60FDClosedAssocReflCode S F) hab

/-- An ACTUAL 17D contextual collision with distinct original objects
exhibits the exact explicit nontrivial two-letter source word killed
by the real DV transport. This makes the original complete-code
obstruction fully constructive once the colliding objects are supplied. -/
theorem nativeC60FDContextCollision_nontrivial_kernel
    (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (hne : a ≠ b)
    (hab : nativeC60BCContextTotal
        (nativeC60DRSeventeenFrame S F) word a =
      nativeC60BCContextTotal (nativeC60DRSeventeenFrame S F) word b) :
    let z := nativeC60FCCodeFiberDefect S F
      (nativeC60FDAssocReflCode S F a)
      (nativeC60FDAssocReflCode S F b)
    z ≠ 1 ∧ (nativeC60DVFullWordTransport S F word) z = 1 := by
  dsimp only
  have hcodes : nativeC60FDAssocReflCode S F a ≠
      nativeC60FDAssocReflCode S F b := by
    intro h
    exact hne (nativeC60FDAssocReflCode_injective S F h)
  exact ⟨nativeC60FCCodeFiberDefect_ne_one S F hcodes,
    nativeC60FCCodeFiberDefect_maps_one S F word
      (nativeC60FDContextCollision_codes S F word hab)⟩

/-- NECESSARY (not sufficient) physical condition for full
unquotiented DV free-word faithfulness: the ACTUAL 17D context
object action must be injective. No claim that the frame satisfies
this condition is made. -/
theorem nativeC60FDContext_injective_of_DVTransport_injective
    (word : List Bool)
    (htransport : Function.Injective
      (nativeC60DVFullWordTransport S F word)) :
    Function.Injective (nativeC60BCContextTotal
      (nativeC60DRSeventeenFrame S F) word) := by
  intro a b hab
  apply nativeC60FDAssocReflCode_injective S F
  exact ((nativeC60FCTransport_injective_iff_code S F word).mp
    htransport) (nativeC60FDContextCollision_codes S F word hab)

/-- A genuine 17D-object context noninjectivity obstruction blocks
the WHOLE DV map. This says nothing about noninjectivity of arbitrary
frames without an explicit object collision witness. -/
theorem nativeC60FDNotContextInjective_blocks_DVTransport
    (word : List Bool)
    (hcontext : ¬ Function.Injective (nativeC60BCContextTotal
      (nativeC60DRSeventeenFrame S F) word)) :
    ¬ Function.Injective (nativeC60DVFullWordTransport S F word) := by
  intro htransport
  exact hcontext
    (nativeC60FDContext_injective_of_DVTransport_injective S F word htransport)

end OriginalSeventeenObjectFiber

#print axioms nativeC60FDAssocReflCode
#print axioms nativeC60FDClosedAssocReflCode
#print axioms nativeC60FDAssocReflCode_injective
#print axioms nativeC60FDAssocReflCode_transport
#print axioms nativeC60FDContextCollision_codes
#print axioms nativeC60FDContextCollision_nontrivial_kernel
#print axioms nativeC60FDContext_injective_of_DVTransport_injective
#print axioms nativeC60FDNotContextInjective_blocks_DVTransport

end
end Kuu.F112.Physical
