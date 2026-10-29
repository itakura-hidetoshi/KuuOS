import Mathlib.Tactic.DeriveCountable
import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalRawCountabilityGate

/-!
# F112-P94D3GA — actual indexed raw17D free syntax has countable fibers
# from countable primitive typed signatures

FZ left the Countable assumption for full raw17D paths explicit.
The existing NativeC60AXStep is a genuinely indexed dependent
inductive with atom/refl/symm/trans constructors. Direct automatic
Countable deriving on the original indexed family is NOT licensed
without arbitrary S.Gen x y evidence being countable.

GA constructs a new *untyped but proof-bearing finite syntax tree*
with primitive tokens holding actual dependent endpoints, and
a partial interpretation BACK to the complete original indexed
AXStep dependent Sigma. Every actual original typed path is a
faithfully decoded syntax tree (no quotation axioms or sorry).
Countability of the finite syntax follows from the countability
of original AX objects and exact original primitive generator
fibers. We do NOT identify original typed proofs with their
untyped syntax shadows: a genuine partial reification certificate
is supplied, and no original definition is overwritten.

FZ's physical 18D full-kernel normal-rank gate is then improved:
the exact original raw17D proof FIBER Countable premise is
derived, under explicit Countable native17D objects and primitive
native17D generator fibers. Countability of the recursive
original 18D assoc/post/pre generator fibers remains separate
until proved.

Pinned Lean v4.30.0-rc2 and mathlib SHA. Append-only, 107 roots,
strict Kuu core primary, independent Kuu presentation, no Gray,
no new axioms, sorry or admit. Retain all original Type-valued
14D–18D witnesses, genuine FJ no-go and distinct FK–FM frame,
no invented geometric 19D filling or global strict hyperdescent.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical

open CategoryTheory Cardinal
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u uD vD uE vE

/-- A finite UNSIGNED syntax expression recording original
primitive proof-bearing atoms and original objects as tokens.
This is only a code; it is NOT the original indexed raw proof
type, nor a quotient of its dependent endpoint data. -/
inductive NativeC60GAPlainRawSyntax (Atom Obj : Type u) : Type u where
  | atom (g : Atom)
  | refl (x : Obj)
  | symm (p : NativeC60GAPlainRawSyntax Atom Obj)
  | trans (p q : NativeC60GAPlainRawSyntax Atom Obj)
  deriving Countable

/-- Exact dependent ORIGINAL primitive proof token, including
both original proof-relevant endpoints. -/
abbrev NativeC60GAOriginalAtomTotal
    {L : NativeC60AXLayer.{u}} (S : NativeC60AXSignature L) : Type u :=
  Σ x : L.Total, Σ y : L.Total, S.Gen x y

/-- The actual original fully typed raw-path total. Its index is
the genuine endpoint PAIR, not a flattened string. -/
abbrev NativeC60GAOriginalPathTotal
    {L : NativeC60AXLayer.{u}} (S : NativeC60AXSignature L) : Type u :=
  Σ ep : L.Total × L.Total, NativeC60AXStep S ep.1 ep.2

/-- Encode any genuinely indexed original proof path by a finite
syntax expression, remembering its ORIGINAL atom witnesses. -/
def nativeC60GAEncodeRaw
    {L : NativeC60AXLayer.{u}} (S : NativeC60AXSignature L) :
    {x y : L.Total} → NativeC60AXStep S x y →
      NativeC60GAPlainRawSyntax (NativeC60GAOriginalAtomTotal S) L.Total
  | _, _, .atom g => .atom ⟨_, _, g⟩
  | _, _, .refl x => .refl x
  | _, _, .symm h => .symm (nativeC60GAEncodeRaw S h)
  | _, _, .trans h k =>
      .trans (nativeC60GAEncodeRaw S h) (nativeC60GAEncodeRaw S k)

/-- Decode syntactic terms PARTIALLY back into the exact
dependent original source/target and original AXStep. In the
trans case, the original endpoints MUST coincide; no
unjustified conversion between different dependent fibers
is introduced. -/
noncomputable def nativeC60GADecodeRaw
    {L : NativeC60AXLayer.{u}} (S : NativeC60AXSignature L) :
    NativeC60GAPlainRawSyntax (NativeC60GAOriginalAtomTotal S) L.Total →
      Option (NativeC60GAOriginalPathTotal S) := by
  classical
  intro e
  induction e with
  | atom token =>
      rcases token with ⟨x, y, g⟩
      exact some ⟨(x, y), .atom g⟩
  | refl x =>
      exact some ⟨(x, x), .refl x⟩
  | symm _ ih =>
      exact ih.bind (fun ⟨⟨x, y⟩, p⟩ =>
        some ⟨(y, x), .symm p⟩)
  | trans _ _ ih ik =>
      exact ih.bind (fun ⟨⟨x, y⟩, p⟩ =>
        ik.bind (fun ⟨⟨z, w⟩, q⟩ =>
          if h : y = z then
            some ⟨(x, w), .trans p (h.symm ▸ q)⟩
          else none))

/-- The partial decoder is an EXACT LEFT INVERSE on every
original dependent raw proof, including arbitrary raw
symmetry and composition nesting. -/
theorem nativeC60GADecode_encodeRaw
    {L : NativeC60AXLayer.{u}} (S : NativeC60AXSignature L)
    {x y : L.Total} (p : NativeC60AXStep S x y) :
    nativeC60GADecodeRaw S (nativeC60GAEncodeRaw S p) =
      some (⟨(x, y), p⟩ : NativeC60GAOriginalPathTotal S) := by
  induction p with
  | atom g => rfl
  | refl a => rfl
  | symm h ih =>
      change
        (nativeC60GADecodeRaw S (nativeC60GAEncodeRaw S h)).bind
          (fun ⟨⟨a, b⟩, q⟩ => some ⟨(b, a), .symm q⟩) = _
      rw [ih]
      rfl
  | trans h k ih ik =>
      change
        (nativeC60GADecodeRaw S (nativeC60GAEncodeRaw S h)).bind
          (fun ⟨⟨a, b⟩, p⟩ =>
            (nativeC60GADecodeRaw S (nativeC60GAEncodeRaw S k)).bind
              (fun ⟨⟨c, d⟩, q⟩ =>
                if heq : b = c then
                  some ⟨(a, d), .trans p (heq.symm ▸ q)⟩
                else none)) = _
      rw [ih, ik]
      simp

/-- The full original AXStep dependent Sigma type is Countable
as soon as its original source/target objects and primitive
typed atom fibers are Countable. This is STRONGER than FZ's
old assumption of Countable arbitrary raw path fibers. -/
theorem nativeC60GAOriginalRawPathTotal_countable
    {L : NativeC60AXLayer.{u}} (S : NativeC60AXSignature L)
    (hobj : Countable L.Total)
    (hgen : ∀ x y : L.Total, Countable (S.Gen x y)) :
    Countable (NativeC60GAOriginalPathTotal S) := by
  letI : Countable L.Total := hobj
  letI : ∀ x y : L.Total, Countable (S.Gen x y) := hgen
  haveI : Countable (NativeC60GAOriginalAtomTotal S) := inferInstance
  haveI : Countable
      (NativeC60GAPlainRawSyntax (NativeC60GAOriginalAtomTotal S) L.Total) :=
    inferInstance
  have hrange :
      (Set.range (nativeC60GADecodeRaw S)).Countable :=
    Set.countable_range _
  letI : Countable (Set.range (nativeC60GADecodeRaw S)) :=
    hrange.to_subtype
  let embedding : NativeC60GAOriginalPathTotal S →
      Set.range (nativeC60GADecodeRaw S) :=
    fun t =>
      ⟨some t, by
        rcases t with ⟨⟨x, y⟩, p⟩
        exact ⟨nativeC60GAEncodeRaw S p,
          nativeC60GADecode_encodeRaw S p⟩⟩
  have hinj : Function.Injective embedding := by
    intro t t' h
    have hsome :
        (some t : Option (NativeC60GAOriginalPathTotal S)) = some t' :=
      congrArg
        (fun z : Set.range (nativeC60GADecodeRaw S) => z.1) h
    exact Option.some.inj hsome
  exact hinj.countable

/-- Every individual indexed original raw AXStep proof fiber is
Countable from original primitive proof fibers, regardless of
the finite number of nested symm/trans constructors. -/
theorem nativeC60GAOriginalRawPathFiber_countable
    {L : NativeC60AXLayer.{u}} (S : NativeC60AXSignature L)
    (hobj : Countable L.Total)
    (hgen : ∀ x y : L.Total, Countable (S.Gen x y))
    (x y : L.Total) :
    Countable (NativeC60AXStep S x y) := by
  letI : Countable (NativeC60GAOriginalPathTotal S) :=
    nativeC60GAOriginalRawPathTotal_countable S hobj hgen
  have hinj : Function.Injective
      (fun p : NativeC60AXStep S x y =>
        (⟨(x, y), p⟩ : NativeC60GAOriginalPathTotal S)) := by
    intro p q h
    exact eq_of_heq (Sigma.mk.inj h).2
  exact hinj.countable

section ActualRawSeventeen

variable {L : NativeC60AXLayer.{u}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- A GENUINE indexed 17D raw-path Countable theorem, derived
from the ACTUAL original triangle primitive Gen fibers and
actual original 17D objects, not postulated for all paths. -/
theorem nativeC60GAOriginal17RawPath_countable_of_primitive
    (hobj : Countable (nativeC60DQSeventeenLayer S F).Total)
    (hgen : ∀ x y : (nativeC60DQSeventeenLayer S F).Total,
      Countable ((nativeC60DQTriangleSeventeenSignature S F).Gen x y))
    (x y : (nativeC60DQSeventeenLayer S F).Total) :
    Countable (NativeC60AXStep
      (nativeC60DQTriangleSeventeenSignature S F) x y) :=
  nativeC60GAOriginalRawPathFiber_countable
    (nativeC60DQTriangleSeventeenSignature S F) hobj hgen x y

/-- Reaching the real full proof-relevant 18D source alphabet
now needs only (i) actual original 17D object Countable,
(ii) actual ORIGINAL primitive triangle generator fibers
Countable, (iii) actual 18D assoc/post/pre generator fibers
Countable. The old FZ raw17D path Countable hypothesis has
been DISCHARGED by the actual four-constructor syntax. -/
theorem nativeC60GAOriginal18_countable_of_primitive17_and_gen18
    (hobj : Countable (nativeC60DQSeventeenLayer S F).Total)
    (hgen17 : ∀ x y : (nativeC60DQSeventeenLayer S F).Total,
      Countable ((nativeC60DQTriangleSeventeenSignature S F).Gen x y))
    (hgen18 : ∀ x y : (nativeC60DREighteenLayer S F).Total,
      Countable ((nativeC60DREighteenAssocSignature S F).Gen x y)) :
    Countable (NativeC60DSCompleteEighteenCode S F) :=
  nativeC60FZFullOriginalEighteen_countable_of_rawAndGen
    S F hobj
    (nativeC60GAOriginal17RawPath_countable_of_primitive S F hobj hgen17)
    hgen18

end ActualRawSeventeen

#print axioms nativeC60GADecode_encodeRaw
#print axioms nativeC60GAOriginalRawPathTotal_countable
#print axioms nativeC60GAOriginalRawPathFiber_countable
#print axioms nativeC60GAOriginal17RawPath_countable_of_primitive
#print axioms nativeC60GAOriginal18_countable_of_primitive17_and_gen18

end
end Kuu.F112.Physical
