import Kuu.F112.PolygonNativeC60AQFullPentagonFiniteListStrictCoherence

/-!
# F112-P94D3EQ — concatenation and reassociation of arbitrary finite AQ block lists

The previous EQ construction splits an arbitrary finite ordered list
of genuine C60 AQ integer blocks. This file shows that the actual
splitting is compatible with arbitrary finite list concatenation.
It also proves the strict three-list associativity (two paths to
append three lists) as equality of the real group isomorphisms,
transporting only the canonical List.append_assoc equality.

Each split still uses EJ's actual kernel and genuine finite integer
receivers. The proof is by induction on the front length, not an
assumption that arbitrary ordered decompositions already agree.
All finite lengths and zero blocks are covered. The terminal
factor remains the genuine abelianized AQ character subgroup,
with no extra quotient, infinite product, 19D filler, Gray structure,
or original noncommutative kernel abelianity.

Preserve strict Kuu, independent Kuu as a presentation, DS no-go,
original 14D--18D Type-valued witnesses, 107 public roots, pinned
Lean 4.30.0-rc2 / mathlib and append-only/same-root. No new axiom,
sorry or admit. Copyright Hidetoshi Itakura / 板倉英俊.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u

section ArbitraryFiniteListAppend

variable {L : NativeC60AXLayer.{u}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- The honest cumulative rank does not depend on where a finite
ordered list is divided into two consecutive sublists. -/
theorem nativeC60EQFinalRank_append (start : ℕ)
    (front suffix : List ℕ) :
    nativeC60EQFinalRank start (front ++ suffix) =
      nativeC60EQFinalRank
        (nativeC60EQFinalRank start front) suffix := by
  induction front generalizing start with
  | nil => rfl
  | cons rank tail ih =>
      change nativeC60EQFinalRank (start + rank) (tail ++ suffix) =
        nativeC60EQFinalRank
          (nativeC60EQFinalRank (start + rank) tail) suffix
      exact ih (start + rank)

/-- Given a genuine recursively split front tower, CONTINUE
splitting its ACTUAL final kernel by the finite suffix list.
There are no chosen coordinate representatives. -/
def nativeC60EQAppendTail (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (start : ℕ) :
    (front suffix : List ℕ) →
      nativeC60EQBlocks S F word start front ≃*
        nativeC60EQBlocks S F word start (front ++ suffix)
  | [], suffix =>
      nativeC60EQIteratedDirectProduct S F word r start suffix
  | rank :: front, suffix =>
      MulEquiv.prodCongr
        (MulEquiv.refl (Fin rank → Multiplicative ℤ))
        (nativeC60EQAppendTail word r (start + rank) front suffix)

/-- MAIN APPEND LAW: splitting the initial list and then its
ACTUAL terminal AQ kernel along a suffix is STRICTLY identical
to splitting the concatenated list in one recursive procedure. -/
theorem nativeC60EQIterated_append (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (start : ℕ) (front suffix : List ℕ) :
    (nativeC60EQIteratedDirectProduct S F word r start front).trans
      (nativeC60EQAppendTail S F word r start front suffix) =
      nativeC60EQIteratedDirectProduct S F word r start (front ++ suffix) := by
  induction front generalizing start with
  | nil =>
      apply MulEquiv.ext
      intro x
      rfl
  | cons rank tail ih =>
      apply MulEquiv.ext
      intro x
      let e := nativeC60EJCumulativeDirectProduct S F word r start rank
      let y := (e x).2
      have htail :
          nativeC60EQAppendTail S F word r (start + rank) tail suffix
            (nativeC60EQIteratedDirectProduct S F word r
              (start + rank) tail y) =
          nativeC60EQIteratedDirectProduct S F word r
            (start + rank) (tail ++ suffix) y :=
        DFunLike.congr_fun (ih (start + rank)) y
      change
        ((e x).1,
          nativeC60EQAppendTail S F word r (start + rank) tail suffix
            (nativeC60EQIteratedDirectProduct S F word r
              (start + rank) tail y)) =
        ((e x).1,
          nativeC60EQIteratedDirectProduct S F word r
            (start + rank) (tail ++ suffix) y)
      exact congrArg (fun z => ((e x).1, z)) htail

/-- Purely typed transport along equality of finite rank lists.
The map is the identity after rewriting its index equality,
and never identifies distinct actual C60 obstruction classes. -/
def nativeC60EQBlockListCast (word : List Bool)
    (start : ℕ) {xs ys : List ℕ} (h : xs = ys) :
    nativeC60EQBlocks S F word start xs ≃*
      nativeC60EQBlocks S F word start ys := by
  cases h
  exact MulEquiv.refl _

/-- List transport commutes with EVERY genuine recursively split
AQ class; this follows by dependent equality elimination on the
list, not an equality assumption about the obstruction kernel. -/
theorem nativeC60EQBlockListCast_iterated (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (start : ℕ) {xs ys : List ℕ} (h : xs = ys)
    (x : (nativeC60EBAbelianReceiver S F word start).ker) :
    nativeC60EQBlockListCast S F word start h
        (nativeC60EQIteratedDirectProduct S F word r start xs x) =
      nativeC60EQIteratedDirectProduct S F word r start ys x := by
  cases h
  rfl

/-- The two ways to divide an ordered finite list into THREE
successive pieces commute exactly after the canonical list
associator. This is path independence at arbitrary finite
sublist lengths, over the genuine cumulative AQ obstruction. -/
theorem nativeC60EQAppend_associativity (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (start : ℕ) (first second third : List ℕ) :
    ((nativeC60EQAppendTail S F word r start first second).trans
      (nativeC60EQAppendTail S F word r start (first ++ second) third)).trans
      (nativeC60EQBlockListCast S F word start
        (List.append_assoc first second third)) =
      nativeC60EQAppendTail S F word r start first (second ++ third) := by
  apply MulEquiv.ext
  intro v
  obtain ⟨x, rfl⟩ :=
    (nativeC60EQIteratedDirectProduct S F word r start first).surjective v
  have hfirst := DFunLike.congr_fun
    (nativeC60EQIterated_append S F word r start first second) x
  have hsecond := DFunLike.congr_fun
    (nativeC60EQIterated_append S F word r start
      (first ++ second) third) x
  have hwhole := DFunLike.congr_fun
    (nativeC60EQIterated_append S F word r start
      first (second ++ third)) x
  change
    nativeC60EQAppendTail S F word r start first second
      (nativeC60EQIteratedDirectProduct S F word r start first x) =
      nativeC60EQIteratedDirectProduct S F word r start (first ++ second) x
    at hfirst
  change
    nativeC60EQAppendTail S F word r start (first ++ second) third
      (nativeC60EQIteratedDirectProduct S F word r
        start (first ++ second) x) =
      nativeC60EQIteratedDirectProduct S F word r
        start ((first ++ second) ++ third) x
    at hsecond
  change
    nativeC60EQAppendTail S F word r start first (second ++ third)
      (nativeC60EQIteratedDirectProduct S F word r start first x) =
      nativeC60EQIteratedDirectProduct S F word r
        start (first ++ (second ++ third)) x
    at hwhole
  change
    nativeC60EQBlockListCast S F word start
      (List.append_assoc first second third)
      (nativeC60EQAppendTail S F word r start
        (first ++ second) third
        (nativeC60EQAppendTail S F word r start first second
          (nativeC60EQIteratedDirectProduct S F word r start first x))) =
    nativeC60EQAppendTail S F word r start first (second ++ third)
      (nativeC60EQIteratedDirectProduct S F word r start first x)
  rw [hfirst, hsecond, hwhole]
  exact nativeC60EQBlockListCast_iterated S F word r start
    (List.append_assoc first second third) x

end ArbitraryFiniteListAppend

#print axioms nativeC60EQFinalRank_append
#print axioms nativeC60EQAppendTail
#print axioms nativeC60EQIterated_append
#print axioms nativeC60EQBlockListCast
#print axioms nativeC60EQBlockListCast_iterated
#print axioms nativeC60EQAppend_associativity

end
end Kuu.F112.Physical
