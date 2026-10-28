import Kuu.F112.PolygonNativeC60AQFullPentagonPartitionLocalAction

/-!
# F112-P94D3EU — stepwise localization of ALL finite C60 AQ repartition paths

ES paths can jump from one arbitrary rank partition to another in one step.
ET gave an actual finite path of adjacent splits/merges and zero-block
insertions/deletions between any equal-total-rank pair. EU now recursively
REPLACES EACH original ES step by its ET local path, retaining the order
and intermediate endpoints of the original finite history.

The localized path and the ES path are not identified as Type-valued
witnesses. Instead their actual ER/EJ C60 AQ actions are PROVED equal.
Consequently there is a constructive local lift for every global ES path,
not just for every equal-total-rank endpoint pair. The charge receiver and
genuine residual subgroup are unchanged throughout.

This is only finite AQ repartition coherence, NOT proof of the missing
19D C60 geometric Type-valued filler, noncommutative-source abelianity,
infinite-rank splitting, or equality of distinct Type-valued histories.
Preserve strict Kuu, independent Kuu as a presentation, DS no-go, the
14D--18D original evidence, all 107 public roots, pinned Lean/mathlib,
and append-only/same-root. No new axioms, sorry or admit.
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

/-- Constructively replace EACH step of any ES global finite rank
path by a finite concatenation of ET's four locally allowed moves.
This preserves intermediate ES vertices instead of replacing the
entire input path by a single arbitrary endpoint comparison. -/
def nativeC60EULocalizeGlobal {xs ys : List ℕ} :
    NativeC60ESPartitionPath xs ys → NativeC60ETLocalPath xs ys
  | .refl xs => .refl xs
  | .step h tail =>
      nativeC60ETLocalPath_trans (nativeC60ETLocalConnect _ _ h)
        (nativeC60EULocalizeGlobal tail)

/-- The stepwise localizer inherits the exact original total finite
rank. No additional equality on natural-number charges is assumed. -/
theorem nativeC60EULocalizeGlobal_rankEq {xs ys : List ℕ}
    (p : NativeC60ESPartitionPath xs ys) :
    nativeC60ETLocalPath_rankEq (nativeC60EULocalizeGlobal p) =
      nativeC60ESPathRankEq p :=
  Subsingleton.elim _ _

/-- Canonical ES paths are represented by their individually
localized ET steps, with no new global-jump generator. -/
theorem nativeC60EULocalizeGlobal_exists {xs ys : List ℕ}
    (p : NativeC60ESPartitionPath xs ys) :
    Nonempty (NativeC60ETLocalPath xs ys) :=
  ⟨nativeC60EULocalizeGlobal p⟩

/-- An ES path can be represented as a typed local path. We DO NOT
claim the raw ES path equals its localized image; only the endpoints
and the rank character agree. -/
def nativeC60EULocalizeThenForget {xs ys : List ℕ}
    (p : NativeC60ESPartitionPath xs ys) :
    NativeC60ESPartitionPath xs ys :=
  nativeC60ETLocalToES (nativeC60EULocalizeGlobal p)

/-- A local path can itself be passed to ES, then localized again:
the new local history may differ, but still carries the same rank. -/
theorem nativeC60EULocalizeThenForget_rankEq {xs ys : List ℕ}
    (p : NativeC60ESPartitionPath xs ys) :
    nativeC60ESPathRankEq (nativeC60EULocalizeThenForget p) =
      nativeC60ESPathRankEq p :=
  Subsingleton.elim _ _

section GenuineC60AQLocalization

variable {L : NativeC60AXLayer.{u}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- EU MAIN theorem: stepwise localization of ANY global ES path
has EXACTLY the same actual finite integer-charge and residual
C60 AQ GROUP EQUIVALENCE as the original path. -/
theorem nativeC60EULocalizeGlobal_action (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (start : ℕ) {xs ys : List ℕ}
    (p : NativeC60ESPartitionPath xs ys) :
    nativeC60ETLocalPathEquiv S F word start
      (nativeC60EULocalizeGlobal p) =
    nativeC60ESPathEquiv S F word start p := by
  calc
    nativeC60ETLocalPathEquiv S F word start
        (nativeC60EULocalizeGlobal p) =
      nativeC60ERCanonicalRepartition S F word start xs ys
        (nativeC60ETLocalPath_rankEq
          (nativeC60EULocalizeGlobal p)) :=
            nativeC60ETLocalPathEquiv_canonical S F word r start
              (nativeC60EULocalizeGlobal p)
    _ = nativeC60ERCanonicalRepartition S F word start xs ys
          (nativeC60ESPathRankEq p) := by
            rw [nativeC60EULocalizeGlobal_rankEq p]
    _ = nativeC60ESPathEquiv S F word start p :=
          (nativeC60ESPathEquiv_eq_canonical S F word r start p).symm

/-- The locally realized global path action is natural with respect
to the ACTUALLY and independently constructed EJ/EQ finite splitting
of the original C60 AQ obstruction kernel. -/
theorem nativeC60EULocalizeGlobal_natural (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (start : ℕ) {xs ys : List ℕ}
    (p : NativeC60ESPartitionPath xs ys) :
    (nativeC60EQSequentialNormalForm S F word r start xs).trans
      (nativeC60ETLocalPathEquiv S F word start
        (nativeC60EULocalizeGlobal p)) =
    nativeC60EQSequentialNormalForm S F word r start ys := by
  rw [nativeC60EULocalizeGlobal_action S F word r start p]
  exact nativeC60ESPathEquiv_natural S F word r start p

/-- Localizing and then forgetting the localization does not
alter the actual global ES action. The cycle is NOT claimed to be
an identity on the Type-valued history syntax. -/
theorem nativeC60EULocalizeThenForget_action (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (start : ℕ) {xs ys : List ℕ}
    (p : NativeC60ESPartitionPath xs ys) :
    nativeC60ESPathEquiv S F word start
      (nativeC60EULocalizeThenForget p) =
    nativeC60ESPathEquiv S F word start p := by
  exact nativeC60EULocalizeGlobal_action S F word r start p

/-- A constructive localized witness for the action of ANY
global finite AQ repartition history; this is the explicit
finite local GENERATION theorem, not an abstract choice axiom. -/
theorem nativeC60EUGlobalPath_hasLocalRealization (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (start : ℕ) {xs ys : List ℕ}
    (p : NativeC60ESPartitionPath xs ys) :
    ∃ q : NativeC60ETLocalPath xs ys,
      nativeC60ETLocalPathEquiv S F word start q =
      nativeC60ESPathEquiv S F word start p :=
  ⟨nativeC60EULocalizeGlobal p,
    nativeC60EULocalizeGlobal_action S F word r start p⟩

/-- The same genuine residual C60 AQ obstruction class survives
the localization of every ES history. -/
theorem nativeC60EULocalizeGlobal_residual (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (start : ℕ) {xs ys : List ℕ}
    (p : NativeC60ESPartitionPath xs ys)
    (z : nativeC60EQChargeTower xs ×
      (nativeC60EBAbelianReceiver S F word (start + xs.sum)).ker) :
    ((nativeC60ETLocalPathEquiv S F word start
       (nativeC60EULocalizeGlobal p) z).2).1 = z.2.1 :=
  nativeC60ETLocalPathEquiv_residual S F word r start
    (nativeC60EULocalizeGlobal p) z

/-- Actual receiver coordinates, indexed absolutely by Fin of
the common finite rank, also survive global-to-local replacement. -/
theorem nativeC60EULocalizeGlobal_coordinate (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (start : ℕ) {xs ys : List ℕ}
    (p : NativeC60ESPartitionPath xs ys)
    (z : nativeC60EQChargeTower xs ×
      (nativeC60EBAbelianReceiver S F word (start + xs.sum)).ker)
    (i : Fin xs.sum) :
    ((nativeC60EQFiniteCoordinatePartition ys).symm
      (nativeC60ETLocalPathEquiv S F word start
        (nativeC60EULocalizeGlobal p) z).1)
        (Fin.cast (nativeC60ETLocalPath_rankEq
          (nativeC60EULocalizeGlobal p)) i) =
    ((nativeC60EQFiniteCoordinatePartition xs).symm z.1) i :=
  nativeC60ETLocalPathEquiv_coordinate S F word r start
    (nativeC60EULocalizeGlobal p) z i

end GenuineC60AQLocalization

#print axioms nativeC60EULocalizeGlobal
#print axioms nativeC60EULocalizeGlobal_rankEq
#print axioms nativeC60EULocalizeThenForget
#print axioms nativeC60EULocalizeGlobal_action
#print axioms nativeC60EULocalizeGlobal_natural
#print axioms nativeC60EULocalizeThenForget_action
#print axioms nativeC60EUGlobalPath_hasLocalRealization
#print axioms nativeC60EULocalizeGlobal_residual
#print axioms nativeC60EULocalizeGlobal_coordinate

end
end Kuu.F112.Physical
