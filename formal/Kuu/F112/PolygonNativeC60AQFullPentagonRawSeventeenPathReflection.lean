import Kuu.F112.PolygonNativeC60AQFullPentagonSeventeenFrameComponentGate

/-!
# F112-P94D3FF — original dependent 17D generator and raw-path reflection

The real BC source-to-closed map is a constructor-by-constructor
translation of ORIGINAL raw Type-valued evidence, with each transported
atom recording its complete original generator, both original typed
endpoints, and the actual finite AQ context word. This is stronger
than mere injectivity of any Peiffer/BV/charge shadow.

The original atom embedding is faithful without assuming context
injectivity. For general composition, the image of an intermediate
lower object must be reflected back to its original source. The
EXPLICIT necessary lower object injectivity gate from FE supplies
this reflection. Under this transparent gate, all four constructors
(atom, refl, symm, trans) reflect equality of original dependent
17D raw paths; no quotient, forbidden 19D filler, Gray or arbitrary
higher equality is used.

No claim that arbitrary physical C60 frame actions satisfy the
object gate unconditionally. Preserve full 14D–18D evidence,
DS complete-evidence no-go, 107 published roots, strict Kuu
primary, independent Kuu as a presentation, no Gray. No
axioms/sorry/admit. Append only, tighten only, same root.
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

section OriginalRawContext

variable {L : NativeC60AXLayer.{u}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- Actual original primitive -> closed-context atom is injective
for any fixed typed original 17D endpoints, without assumptions on
the underlying C60 object frame, because its target atom records
the full original dependent code plus chronological context. -/
theorem nativeC60FFBCOriginalAtom_injective
    (word : List Bool)
    {a b : L.Total} :
    Function.Injective
      (fun g : S.Gen a b => nativeC60BCGen S F word g) := by
  intro g h heq
  have hc := congrArg (nativeC60BVGeneratorCode S F) heq
  change
    (word, (⟨a, b, g⟩ : Σ x : L.Total, Σ y : L.Total, S.Gen x y)) =
      (word, (⟨a, b, h⟩ : Σ x : L.Total, Σ y : L.Total, S.Gen x y)) at hc
  have hcode := (Prod.mk.inj hc).2
  have hpair :
      (⟨b, g⟩ : Σ y : L.Total, S.Gen a y) = ⟨b, h⟩ :=
    eq_of_heq (Sigma.mk.inj hcode).2
  exact eq_of_heq (Sigma.mk.inj hpair).2

/-- Recover the ACTUAL intermediate dependent lower object and the
left raw subpath of a compositional proof; none for other constructors.
The dependent Sigma retains the entire original boundary type. -/
def nativeC60FFTransLeftCode {M : NativeC60AXLayer.{u}}
    (T : NativeC60AXSignature M)
    {a b : M.Total} (p : NativeC60AXStep T a b) :
    Option (Σ mid : M.Total, NativeC60AXStep T a mid) :=
  match p with
  | .trans (y := mid) h _ => some ⟨mid, h⟩
  | _ => none

/-- The right raw subpath likewise remembers the same intermediate
object and the entire original dependent target proof. -/
def nativeC60FFTransRightCode {M : NativeC60AXLayer.{u}}
    (T : NativeC60AXSignature M)
    {a b : M.Total} (p : NativeC60AXStep T a b) :
    Option (Σ mid : M.Total, NativeC60AXStep T mid b) :=
  match p with
  | .trans (y := mid) _ h => some ⟨mid, h⟩
  | _ => none

/-- The actual original-to-context-closed raw proof map reflects
equality of ALL original 17D proof constructors on each dependent
Hom fiber, under an explicit injective context action on full 16D
lower proof objects. This gate is NOT inferred from a BV shadow. -/
theorem nativeC60FFBCOriginalStep_injective
    (word : List Bool)
    (hctx : Function.Injective (nativeC60BCContextTotal F word)) :
    ∀ {a b : L.Total},
      Function.Injective (fun p : NativeC60AXStep S a b =>
        nativeC60BCMapOriginalStep S F word p) := by
  intro a b p q heq
  induction p with
  | atom g =>
      cases q with
      | atom h =>
          have hg : g = h := by
            apply nativeC60FFBCOriginalAtom_injective S F word
            injection heq
          cases hg
          rfl
      | refl _ => cases heq
      | symm _ => cases heq
      | trans _ _ => cases heq
  | refl a =>
      cases q with
      | atom _ => cases heq
      | refl _ => rfl
      | symm _ => cases heq
      | trans _ _ => cases heq
  | symm p ih =>
      cases q with
      | atom _ => cases heq
      | refl _ => cases heq
      | symm q =>
          have hp :
              nativeC60BCMapOriginalStep S F word p =
                nativeC60BCMapOriginalStep S F word q := by
            injection heq
          have hp' : p = q := ih hp
          cases hp'
          rfl
      | trans _ _ => cases heq
  | trans p t ihp iht =>
      cases q with
      | atom _ => cases heq
      | refl _ => cases heq
      | symm _ => cases heq
      | trans q r =>
          have hleftSigma := Option.some.inj
            (congrArg
              (nativeC60FFTransLeftCode (nativeC60BCClosedSignature S F))
              heq)
          have hrightSigma := Option.some.inj
            (congrArg
              (nativeC60FFTransRightCode (nativeC60BCClosedSignature S F))
              heq)
          have hmid := hctx (congrArg Sigma.fst hleftSigma)
          cases hmid
          have hl : nativeC60BCMapOriginalStep S F word p =
              nativeC60BCMapOriginalStep S F word q :=
            eq_of_heq (Sigma.mk.inj hleftSigma).2
          have hr : nativeC60BCMapOriginalStep S F word t =
              nativeC60BCMapOriginalStep S F word r :=
            eq_of_heq (Sigma.mk.inj hrightSigma).2
          have hpl : p = q := ihp hl
          have htr : t = r := iht hr
          cases hpl
          cases htr
          rfl

end OriginalRawContext

#print axioms nativeC60FFBCOriginalAtom_injective
#print axioms nativeC60FFBCOriginalStep_injective

end
end Kuu.F112.Physical
