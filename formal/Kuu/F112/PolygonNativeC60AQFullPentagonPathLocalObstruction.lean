import Kuu.F112.PolygonNativeC60AQFullPentagonEvidenceLiftGate

/-!
# F112-P94D3EW — path-local primitive obstruction with original typed provenance

DS proved that a candidate 19D pentagon filler cannot preserve EVERY
original complete signed noncommutative 18D free word. EV extracted a
generator somewhere in a proposed 19D signature which loses evidence.

EW strengthens this to the PARTICULAR PROVIDED TYPE-VALUED PATH:
a witness tracks the precise atom of the original path and its original
dependent endpoints, whether the atom occurs forwards, reversed, or in
either half of a composite. No ambient unrelated generator suffices.

The generic path-local certificate is defined for ANY observation on
an explicitly specified dependent NativeC60AXStep signature. From
the absence of a bad atom ALONG A GIVEN PATH, the observation at
that path's endpoints must agree. Contraposition extracts an actual
path-local bad atom whenever the observations disagree. This relies on
the original 4-constructor Type-valued path grammar, NOT a new quotient,
proof irrelevance, synthetic geometric filler, or an abstract graph.

Preserve strict Kuu, independent Kuu as a presentation, original
14D--18D evidence, DS complete-evidence no-go, 107 public roots,
C60 gauge context, pinned Lean/mathlib, append-only/same-root,
no-Gray. No new axiom, sorry or admit.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u v

/-- A genuinely path-local certificate of a nonpreserving generator.
The constructor records that the violating atom is part of THIS
original dependent path, even inside inverse and composite terms. -/
inductive NativeC60EWBadAtomOn
    {L : NativeC60AXLayer.{u}}
    (T : NativeC60AXSignature L)
    {B : Type v} (obs : L.Total → B) :
    {x y : L.Total} → NativeC60AXStep T x y → Prop where
  | atom {x y : L.Total}
      (g : T.Gen x y) (hne : obs x ≠ obs y) :
      NativeC60EWBadAtomOn T obs (.atom g)
  | symm {x y : L.Total} {p : NativeC60AXStep T x y}
      (h : NativeC60EWBadAtomOn T obs p) :
      NativeC60EWBadAtomOn T obs (.symm p)
  | transLeft {x y z : L.Total}
      {p : NativeC60AXStep T x y} {q : NativeC60AXStep T y z}
      (h : NativeC60EWBadAtomOn T obs p) :
      NativeC60EWBadAtomOn T obs (.trans p q)
  | transRight {x y z : L.Total}
      {p : NativeC60AXStep T x y} {q : NativeC60AXStep T y z}
      (h : NativeC60EWBadAtomOn T obs q) :
      NativeC60EWBadAtomOn T obs (.trans p q)

/-- If a SPECIFIC dependent path has no bad primitive atom anywhere
in its own signed/composite syntax, then the observer agrees at its
endpoints. Proof proceeds by structural induction on that path. -/
theorem nativeC60EWNoBadOnPath_sound
    {L : NativeC60AXLayer.{u}}
    (T : NativeC60AXSignature L)
    {B : Type v} (obs : L.Total → B) :
    ∀ {x y : L.Total} (p : NativeC60AXStep T x y),
      ¬ NativeC60EWBadAtomOn T obs p → obs x = obs y := by
  intro x y p
  induction p with
  | atom g =>
      intro hnone
      by_contra hneq
      exact hnone (.atom g hneq)
  | refl _ =>
      intro _
      rfl
  | symm p ih =>
      intro hnone
      exact (ih (by
        intro h
        exact hnone (.symm h))).symm
  | trans p q ihp ihq =>
      intro hnone
      exact (ihp (by
        intro h
        exact hnone (.transLeft h))).trans (ihq (by
          intro h
          exact hnone (.transRight h)))

/-- The path-local obstruction is unavoidable when the original
endpoint observations differ. The resulting witness refers to a
generator OCCURRING IN THIS PATH, not merely somewhere in T. -/
theorem nativeC60EWBadOnPath_of_endpoint_ne
    {L : NativeC60AXLayer.{u}}
    (T : NativeC60AXSignature L)
    {B : Type v} (obs : L.Total → B)
    {x y : L.Total} (p : NativeC60AXStep T x y)
    (hne : obs x ≠ obs y) :
    NativeC60EWBadAtomOn T obs p := by
  classical
  by_contra hnone
  exact hne (nativeC60EWNoBadOnPath_sound T obs p hnone)

/-- Extract the actual dependent primitive generator from a
path-local certificate. The proof recurses through its recorded
reversal/left/right occurrence rather than inspecting unrelated
generators of the ambient signature. -/
theorem nativeC60EWBadOnPath_has_generator
    {L : NativeC60AXLayer.{u}}
    (T : NativeC60AXSignature L)
    {B : Type v} (obs : L.Total → B)
    {x y : L.Total} {p : NativeC60AXStep T x y}
    (h : NativeC60EWBadAtomOn T obs p) :
    ∃ (a b : L.Total) (g : T.Gen a b), obs a ≠ obs b := by
  induction h with
  | atom g hne => exact ⟨_, _, g, hne⟩
  | symm _ ih => exact ih
  | transLeft _ ih => exact ih
  | transRight _ ih => exact ih

/-- No bad primitive in the actual concatenation implies equality
of the original observation on the whole composite's boundaries,
including both true dependent intermediate endpoints. -/
theorem nativeC60EWNoBadComposite_sound
    {L : NativeC60AXLayer.{u}}
    (T : NativeC60AXSignature L)
    {B : Type v} (obs : L.Total → B)
    {x y z : L.Total}
    (p : NativeC60AXStep T x y) (q : NativeC60AXStep T y z)
    (h : ¬ NativeC60EWBadAtomOn T obs (.trans p q)) :
    obs x = obs z :=
  nativeC60EWNoBadOnPath_sound T obs (.trans p q) h

#print axioms NativeC60EWBadAtomOn
#print axioms nativeC60EWNoBadOnPath_sound
#print axioms nativeC60EWBadOnPath_of_endpoint_ne
#print axioms nativeC60EWBadOnPath_has_generator
#print axioms nativeC60EWNoBadComposite_sound

end
end Kuu.F112.Physical
