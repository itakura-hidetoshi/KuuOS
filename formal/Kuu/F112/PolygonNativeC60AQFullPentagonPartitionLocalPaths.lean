import Kuu.F112.PolygonNativeC60AQFullPentagonPartitionPaths

/-!
# F112-P94D3ET — generators of finite local C60 AQ rank-partition paths

ES permits an arbitrary equality-of-total-rank comparison as a single path
step. ET restricts the generators to *local* ordered rank operations:
an adjacent split/merge at an explicitly recorded front/suffix and insertion/
deletion of one rank-zero block at an explicitly recorded location.

The zero moves are essential at the empty boundary: adjacent splitting and
merging alone cannot connect [] and [0]. The path syntax is Type-valued and
records the actual choice and order of operations. No equality between
different Type-valued histories is asserted.

Every local operation preserves the finite rank. By explicit finite
construction, each ordered partition is connected to its singleton total-rank
normal form, including the empty partition. Consequently any two finite
partitions of equal total rank admit a path consisting ONLY of these moves.

No Gray structures, 19D filler, infinite-rank splitting, noncommutative-kernel
abelianity, new axiom, sorry or admit. Preserve strict Kuu, independent Kuu
presentation, the DS no-go, existing 14D--18D Type-valued evidence, all 107
published roots, pinned Lean/mathlib and append-only/same-root policy.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical

set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000

/-- Exactly four kinds of LOCAL finite-rank repartition move. The front
and suffix locate a move in the ordered sequence; no permutation of
the original absolute integer-charge coordinates is permitted. -/
inductive NativeC60ETLocalMove : List ℕ → List ℕ → Type where
  | split (front suffix : List ℕ) (a b : ℕ) :
      NativeC60ETLocalMove
        (front ++ (a + b) :: suffix) (front ++ a :: b :: suffix)
  | merge (front suffix : List ℕ) (a b : ℕ) :
      NativeC60ETLocalMove
        (front ++ a :: b :: suffix) (front ++ (a + b) :: suffix)
  | insertZero (front suffix : List ℕ) :
      NativeC60ETLocalMove (front ++ suffix) (front ++ 0 :: suffix)
  | eraseZero (front suffix : List ℕ) :
      NativeC60ETLocalMove (front ++ 0 :: suffix) (front ++ suffix)

/-- The total integer receiver rank is unchanged by EACH primitive move.
Adjacent rank preservation is the existing genuine ER adjacent-sum theorem. -/
def nativeC60ETLocalMove_rankEq {xs ys : List ℕ}
    (m : NativeC60ETLocalMove xs ys) : xs.sum = ys.sum := by
  cases m with
  | split front suffix a b =>
      exact nativeC60ERAdjacentSum front suffix a b
  | merge front suffix a b =>
      exact (nativeC60ERAdjacentSum front suffix a b).symm
  | insertZero front suffix =>
      simp only [List.sum_append, List.sum_cons, zero_add]
  | eraseZero front suffix =>
      simp only [List.sum_append, List.sum_cons, zero_add]

/-- Each local generator has a literal opposite generator, without
identifying the two distinct Type-valued history witnesses. -/
def nativeC60ETLocalMove_reverse {xs ys : List ℕ}
    (m : NativeC60ETLocalMove xs ys) : NativeC60ETLocalMove ys xs := by
  cases m with
  | split front suffix a b => exact .merge front suffix a b
  | merge front suffix a b => exact .split front suffix a b
  | insertZero front suffix => exact .eraseZero front suffix
  | eraseZero front suffix => exact .insertZero front suffix

/-- Shift one local operation behind a fixed leading integer-charge block. -/
def nativeC60ETLocalMove_cons (c : ℕ) {xs ys : List ℕ}
    (m : NativeC60ETLocalMove xs ys) :
    NativeC60ETLocalMove (c :: xs) (c :: ys) := by
  cases m with
  | split front suffix a b => exact .split (c :: front) suffix a b
  | merge front suffix a b => exact .merge (c :: front) suffix a b
  | insertZero front suffix => exact .insertZero (c :: front) suffix
  | eraseZero front suffix => exact .eraseZero (c :: front) suffix

/-- Type-valued finite local path. Unlike ES, a step CANNOT jump
directly between arbitrary same-rank partitions. -/
inductive NativeC60ETLocalPath : List ℕ → List ℕ → Type where
  | refl (xs : List ℕ) : NativeC60ETLocalPath xs xs
  | step {xs ys zs : List ℕ} (move : NativeC60ETLocalMove xs ys)
      (tail : NativeC60ETLocalPath ys zs) : NativeC60ETLocalPath xs zs

/-- Finite local concatenation, preserving the actual generator history. -/
def nativeC60ETLocalPath_trans {xs ys zs : List ℕ} :
    NativeC60ETLocalPath xs ys → NativeC60ETLocalPath ys zs →
      NativeC60ETLocalPath xs zs
  | .refl _, q => q
  | .step m tail, q =>
      .step m (nativeC60ETLocalPath_trans tail q)

/-- Reverse the ordered local history and each of its generators. -/
def nativeC60ETLocalPath_reverse {xs ys : List ℕ} :
    NativeC60ETLocalPath xs ys → NativeC60ETLocalPath ys xs
  | .refl xs => .refl xs
  | .step m tail =>
      nativeC60ETLocalPath_trans (nativeC60ETLocalPath_reverse tail)
        (.step (nativeC60ETLocalMove_reverse m) (.refl _))

/-- Lift a full finite local path behind a fixed leading block. -/
def nativeC60ETLocalPath_cons (c : ℕ) {xs ys : List ℕ} :
    NativeC60ETLocalPath xs ys →
      NativeC60ETLocalPath (c :: xs) (c :: ys)
  | .refl xs => .refl (c :: xs)
  | .step m tail =>
      .step (nativeC60ETLocalMove_cons c m)
        (nativeC60ETLocalPath_cons c tail)

/-- Every LOCAL path preserves the exact total finite rank. -/
def nativeC60ETLocalPath_rankEq {xs ys : List ℕ}
    (p : NativeC60ETLocalPath xs ys) : xs.sum = ys.sum := by
  induction p with
  | refl _ => rfl
  | step move tail ih =>
      exact (nativeC60ETLocalMove_rankEq move).trans ih

/-- A local path is also an ES partition path, but not conversely by
a single step. This forgetful map retains endpoints and rank evidence. -/
def nativeC60ETLocalToES {xs ys : List ℕ} :
    NativeC60ETLocalPath xs ys → NativeC60ESPartitionPath xs ys
  | .refl xs => .refl xs
  | .step move tail =>
      .step (nativeC60ETLocalMove_rankEq move)
        (nativeC60ETLocalToES tail)

/-- A rank-zero insertion is necessary to connect [] to [0].
The explicit witness is one primitive local operation, not a global jump. -/
def nativeC60ETEmptyToZero : NativeC60ETLocalPath [] [0] :=
  .step (.insertZero [] []) (.refl [0])

/-- Explicit canonical local expansion from ONE combined block to
an arbitrary finite ordered rank partition. The [] case is handled
by erasing [0], not by pretending that [] = [0]. -/
def nativeC60ETLocalExpand :
    (xs : List ℕ) → NativeC60ETLocalPath [xs.sum] xs
  | [] =>
      .step (.eraseZero [] []) (.refl [])
  | x :: xs => by
      have hsplit : NativeC60ETLocalPath [x + xs.sum] (x :: xs) :=
        .step (.split [] [] x xs.sum)
          (nativeC60ETLocalPath_cons x (nativeC60ETLocalExpand xs))
      simpa only [List.sum_cons] using hsplit

/-- Construct a path between ANY equal-total-rank finite partitions,
using only adjacent splits, merges and rank-zero insertions/deletions.
The construction goes through the common one-block normal form. -/
def nativeC60ETLocalConnect (xs ys : List ℕ)
    (h : xs.sum = ys.sum) : NativeC60ETLocalPath xs ys := by
  have hx : NativeC60ETLocalPath xs [xs.sum] :=
    nativeC60ETLocalPath_reverse (nativeC60ETLocalExpand xs)
  have hx' : NativeC60ETLocalPath xs [ys.sum] := by
    simpa only [h] using hx
  exact nativeC60ETLocalPath_trans hx' (nativeC60ETLocalExpand ys)

/-- Every equal-total-rank pair is locally connected; no arbitrary ES
repartition generator is required for this existence claim. -/
theorem nativeC60ETLocalConnected (xs ys : List ℕ)
    (h : xs.sum = ys.sum) : Nonempty (NativeC60ETLocalPath xs ys) :=
  ⟨nativeC60ETLocalConnect xs ys h⟩

/-- In particular, the empty/single-zero boundary has an actual local path. -/
theorem nativeC60ETEmptyZero_connected :
    Nonempty (NativeC60ETLocalPath [] [0]) :=
  ⟨nativeC60ETEmptyToZero⟩

#print axioms nativeC60ETLocalMove_rankEq
#print axioms nativeC60ETLocalPath_rankEq
#print axioms nativeC60ETLocalToES
#print axioms nativeC60ETLocalExpand
#print axioms nativeC60ETLocalConnect
#print axioms nativeC60ETLocalConnected
#print axioms nativeC60ETEmptyZero_connected

end Kuu.F112.Physical
