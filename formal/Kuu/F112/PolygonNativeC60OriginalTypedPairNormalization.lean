import Kuu.F112.PolygonNativeC60OriginalTypedPairCNRecovery

/-!
# F112-P94D3CW2 — finite typed parallel-pair normal forms

A strengthened Type-valued presentation classifies not only the genuine
CV two-boundary incidence but the exact signed primitive order at all
four A/B endpoints. Source-closed loops have the canonical finite
g₁h₁⁻¹ ⋯ gₙhₙ⁻¹ form; no generator is replaced or quotient-lifted.
Original 14D/15D evidence, inner/outer AQ frames and strict Kuu persist.

This stage does not assert all outer-framed original generators are
unprefixes of original unframed BC generators, and does not collapse
the original CO/CP/CQ/CR strict kernel on that missing premise.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uCW2 uD vD uE vE

section TypedFourForms

variable {L : NativeC60AXLayer.{uCW2}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- Exact original B→B normal form, dual to CW's A→A paired chain. -/
def nativeC60CWTargetPairChain {A B : L.Total} :
    List ((nativeC60BCClosedSignature S F).Gen A B ×
      (nativeC60BCClosedSignature S F).Gen A B) →
      NativeC60CASignedChain S F B B
  | [] => .nil B
  | (h, g) :: rest => .neg h (.pos g (nativeC60CWTargetPairChain rest))

/-- Four genuinely DEPENDENT original 16D typed path normal forms.
All letters retain their original Type-valued BC proof witnesses. -/
inductive NativeC60CWTypedFourForm (A B : L.Total) :
    {x y : L.Total} → NativeC60CASignedChain S F x y → Type uCW2 where
  | aa (pairs : List ((nativeC60BCClosedSignature S F).Gen A B ×
        (nativeC60BCClosedSignature S F).Gen A B)) :
      NativeC60CWTypedFourForm A B (nativeC60CWPairChain S F pairs)
  | ab (g : (nativeC60BCClosedSignature S F).Gen A B)
      (pairs : List ((nativeC60BCClosedSignature S F).Gen A B ×
        (nativeC60BCClosedSignature S F).Gen A B)) :
      NativeC60CWTypedFourForm A B (.pos g (nativeC60CWTargetPairChain S F pairs))
  | ba (h : (nativeC60BCClosedSignature S F).Gen A B)
      (pairs : List ((nativeC60BCClosedSignature S F).Gen A B ×
        (nativeC60BCClosedSignature S F).Gen A B)) :
      NativeC60CWTypedFourForm A B (.neg h (nativeC60CWPairChain S F pairs))
  | bb (pairs : List ((nativeC60BCClosedSignature S F).Gen A B ×
        (nativeC60BCClosedSignature S F).Gen A B)) :
      NativeC60CWTypedFourForm A B (nativeC60CWTargetPairChain S F pairs)

/-- CV's arbitrary finite typed signed certificate admits one of the
four exact original normal forms whenever A and B are distinct. -/
def NativeC60CVSignedGaugeSector.to_CW_four_form
    {A B : L.Total} (hAB : A ≠ B)
    {x y : L.Total} {path : NativeC60CASignedChain S F x y}
    (certificate : NativeC60CVSignedGaugeSector S F A B path) :
    NativeC60CWTypedFourForm S F A B path := by
  induction certificate with
  | nilSource =>
      exact .aa []
  | nilTarget =>
      exact .bb []
  | positive g tail htail ih =>
      cases ih with
      | aa pairs =>
          exact False.elim (hAB rfl)
      | ab h pairs =>
          exact False.elim (hAB rfl)
      | ba h pairs =>
          exact .aa ((g, h) :: pairs)
      | bb pairs =>
          exact .ab g pairs
  | negative g tail htail ih =>
      cases ih with
      | aa pairs =>
          exact .ba g pairs
      | ab h pairs =>
          exact .bb ((g, h) :: pairs)
      | ba h pairs =>
          exact False.elim (hAB rfl)
      | bb pairs =>
          exact False.elim (hAB rfl)

end TypedFourForms

#print axioms nativeC60CWTargetPairChain
#print axioms NativeC60CVSignedGaugeSector.to_CW_four_form

end
end Kuu.F112.Physical
