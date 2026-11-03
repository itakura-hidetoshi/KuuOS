import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5BANineConstructorSeamInduction
import Mathlib.Tactic

/-!
F112-P94D3GK5BB — unconditional higher-cell obstruction for
the genuinely distinct original-F55 versus recursively selected
P92B proof presentations, detected by original-wrapper count.

A new independent NATURAL-NUMBER invariant counts all P92B
'.original' constructors. A raw whole F55 proof uses exactly
ONE original wrapper; selected P92B.refl uses ZERO, while a
selected trans of TWO original wrappers uses TWO.
We prove the invariant is preserved by ALL 16 P93C and ALL
19 P94A genuine Type-valued four-cell constructors, including
embedded original P89, interchange, the chosen horizontal unit
and both added context unit four-cells. This is strictly stronger
than three-coordinate signed C60 physical shadow and distinct
from GK5AM's ZMod2 context parity, which does NOT survive the
P94A context-unit generators.

THEREFORE the original identity-to-selected-refl higher seam
does NOT exist, for ANY genuine well-typed F54 route.
ALSO the raw whole-original-trans to trans-of-two-raw-originals
four-cell shell does NOT exist at ANY genuine composable F55
pair. These are UNCONDITIONAL negative results, not absence of
a construction in the current code.

As a consequence the GK5BA strong constructor-shell KIT
is uninhabited wherever a real original route exists, and
even the weaker GK5AY UNIVERSAL original-to-recursive-phi
seam record is uninhabited at every inhabited route slot,
because it would have to bridge original(ident r) to refl r.

This does NOT establish that every individual composite
original f has no seam: for example the actual north pentagon
with an original right identity has original-wrapper count 1
on BOTH raw and recursive phi sides. Its trans SPLIT SHELL
is absent, but a different 4-cell direct to phi is not ruled
out by this invariant. For two genuine primitive pentagon
proof occurrences, even the final seam can be excluded
when the recursive phi side has original-wrapper count 2.

The inherited conditional GK5AY/GK5BA statements remain true;
their antecedent global kits/seams are now proved impossible
in actually inhabited original F54 contexts. Strict 空 authority,
independent Kuu→Qi, proof-relevant F54 two-Nat/category/Blocks
histories intact, root 107 and PR #1558 Draft/OPEN protected.
Append-only, no Gray, sorry/admit/native_decide/new axioms.
Pinned Lean v4.30.0-rc2 and mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {p : Polygon} {a b : D} {x y : E}
variable {n n' m m' : Nat}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}
variable {first : KuuNativeF45Tree p n m ma pa mb pb}
variable {last : KuuNativeF45Tree p n' m' ma pa mb pb}

/-- Count the exact P92B ORIGINAL F55 wrapper constructor inside
the FULL Type-valued chosen three-proof, not its signed physical
shadow, raw F55 shapeTag, or proof-class projection.
Structural inversion and F45/F54 contexts preserve the number;
vertical and horizontal compositions add counts. -/
def NativeF55P92AssocComparison.gk5bbOriginalCount
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55P92AssocComparison p r s) : Nat := by
  induction f with
  | original old => exact 1
  | assocNaturality u v w => exact 0
  | refl r => exact 0
  | symm f ih => exact ih
  | trans f g ihf ihg => exact ihf + ihg
  | leftContext f later ih => exact ih
  | rightContext earlier f ih => exact ih
  | precompose prior f ih => exact ih
  | postcompose f suffix ih => exact ih

/-- Exact vertical 3-proof computation; using the named lemma
avoids unfolding the dependent recursor inside interchange. -/
theorem NativeF55P92AssocComparison.gk5bbTrans_count
    {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : NativeF55P92AssocComparison p r s)
    (g : NativeF55P92AssocComparison p s t) :
    (NativeF55P92AssocComparison.trans f g).gk5bbOriginalCount =
      f.gk5bbOriginalCount + g.gk5bbOriginalCount := rfl

/-- Exact genuine P92B horizontal pasting: every original wrapper
occurrence in the two input 3-cells occurs exactly once in the
dependent post/pre-context construction of their horizontal cell. -/
theorem NativeF55P92AssocComparison.gk5bbHorizontal_count
    {n₁ n₁' m₁ m₁' n₂ n₂' m₂ m₂' : Nat}
    {p₀ p₁ p₂ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ : KuuNativeBlocks x y}
    {leftBefore : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁}
    {leftAfter : KuuNativeF45Tree p n₁' m₁' p₀ q₀ p₁ q₁}
    {rightBefore : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂}
    {rightAfter : KuuNativeF45Tree p n₂' m₂' p₁ q₁ p₂ q₂}
    {u u' : KuuNativeF45Tree.DepthRotationRoute p leftBefore leftAfter}
    {v v' : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter}
    (f : NativeF55P92AssocComparison p u u')
    (g : NativeF55P92AssocComparison p v v') :
    (f.horizontal g).gk5bbOriginalCount =
      f.gk5bbOriginalCount + g.gk5bbOriginalCount := rfl

/-- ALL SIXTEEN chosen P93C four-cell constructors preserve the
exact number of ORIGINAL F55 raw wrappers. Old P89 four-cells
compare two raw wrappers, regardless of their original F55
internal history. Context and vertical/horizontal congruence
continue to preserve the number by actual induction. -/
theorem NativeF55P93AssocFourCell.gk5bbOriginalCount_sound
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55P92AssocComparison p r s}
    (w : NativeF55P93AssocFourCell f g) :
    f.gk5bbOriginalCount = g.gk5bbOriginalCount := by
  induction w with
  | old w => rfl
  | refl f => rfl
  | symm w ih => exact ih.symm
  | trans fg gh ihfg ihgh => exact ihfg.trans ihgh
  | verticalLeftUnit f =>
      change (0 : Nat) + f.gk5bbOriginalCount = f.gk5bbOriginalCount
      exact zero_add _
  | verticalRightUnit f =>
      change f.gk5bbOriginalCount + (0 : Nat) = f.gk5bbOriginalCount
      exact add_zero _
  | verticalAssoc f g h =>
      change (f.gk5bbOriginalCount + g.gk5bbOriginalCount) +
        h.gk5bbOriginalCount =
        f.gk5bbOriginalCount + (g.gk5bbOriginalCount + h.gk5bbOriginalCount)
      exact add_assoc _ _ _
  | leftWhisker prior w ih =>
      exact congrArg (fun z : Nat => prior.gk5bbOriginalCount + z) ih
  | rightWhisker w suffix ih =>
      exact congrArg (fun z : Nat => z + suffix.gk5bbOriginalCount) ih
  | leftContext w later ih => exact ih
  | rightContext earlier w ih => exact ih
  | precompose prior w ih => exact ih
  | postcompose w suffix ih => exact ih
  | horizontalLeft w other ih =>
      simpa only [NativeF55P92AssocComparison.gk5bbHorizontal_count] using
        congrArg (fun z : Nat => z + other.gk5bbOriginalCount) ih
  | horizontalRight other w ih =>
      simpa only [NativeF55P92AssocComparison.gk5bbHorizontal_count] using
        congrArg (fun z : Nat => other.gk5bbOriginalCount + z) ih
  | interchange f₁ f₂ g₁ g₂ =>
      simp only [NativeF55P92AssocComparison.gk5bbHorizontal_count,
        NativeF55P92AssocComparison.gk5bbTrans_count]
      omega

/-- ALL NINETEEN chosen P94A four-cell constructors preserve the
same stronger natural-number original-wrapper invariant, including
the horizontalUnit and left/rightContextUnit additions. -/
theorem NativeF55P94UnitFourCell.gk5bbOriginalCount_sound
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : NativeF55P92AssocComparison p r s}
    (w : NativeF55P94UnitFourCell f g) :
    f.gk5bbOriginalCount = g.gk5bbOriginalCount := by
  induction w with
  | old w => exact w.gk5bbOriginalCount_sound
  | refl f => rfl
  | symm w ih => exact ih.symm
  | trans fg gh ihfg ihgh => exact ihfg.trans ihgh
  | verticalLeftUnit f =>
      change (0 : Nat) + f.gk5bbOriginalCount = f.gk5bbOriginalCount
      exact zero_add _
  | verticalRightUnit f =>
      change f.gk5bbOriginalCount + (0 : Nat) = f.gk5bbOriginalCount
      exact add_zero _
  | verticalAssoc f g h =>
      change (f.gk5bbOriginalCount + g.gk5bbOriginalCount) +
        h.gk5bbOriginalCount =
        f.gk5bbOriginalCount + (g.gk5bbOriginalCount + h.gk5bbOriginalCount)
      exact add_assoc _ _ _
  | leftWhisker prior w ih =>
      exact congrArg (fun z : Nat => prior.gk5bbOriginalCount + z) ih
  | rightWhisker w suffix ih =>
      exact congrArg (fun z : Nat => z + suffix.gk5bbOriginalCount) ih
  | leftContext w later ih => exact ih
  | rightContext earlier w ih => exact ih
  | precompose prior w ih => exact ih
  | postcompose w suffix ih => exact ih
  | horizontalLeft w other ih =>
      simpa only [NativeF55P92AssocComparison.gk5bbHorizontal_count] using
        congrArg (fun z : Nat => z + other.gk5bbOriginalCount) ih
  | horizontalRight other w ih =>
      simpa only [NativeF55P92AssocComparison.gk5bbHorizontal_count] using
        congrArg (fun z : Nat => other.gk5bbOriginalCount + z) ih
  | interchange f₁ f₂ g₁ g₂ =>
      simp only [NativeF55P92AssocComparison.gk5bbHorizontal_count,
        NativeF55P92AssocComparison.gk5bbTrans_count]
      omega
  | horizontalUnit u v =>
      change (0 : Nat) + 0 = 0
      omega
  | leftContextUnit route later => rfl
  | rightContextUnit earlier route => rfl

/-- Every original F55 raw wrapper has count ONE, even when its
internal proof is a vertically composite or contextual F55 term. -/
theorem nativeGK5BBOriginal_count_one
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    (NativeF55P92AssocComparison.original f).gk5bbOriginalCount = 1 := rfl

/-- The selected identity three-proof has ZERO raw wrappers. -/
theorem nativeGK5BBSelectedRefl_count_zero
    (r : KuuNativeF45Tree.DepthRotationRoute p first last) :
    (NativeF55P92AssocComparison.refl r).gk5bbOriginalCount = 0 := rfl

/-- An ACTUAL original F55 identity wrapper CANNOT be related
to the selected P92B.refl at its same F54 route by any chosen
P94A Type-valued four-proof. This is the REAL local ident
seam obstruction, not merely syntactic non-equality. -/
theorem nativeGK5BBIdent_no_P94
    (r : KuuNativeF45Tree.DepthRotationRoute p first last) :
    ¬ Nonempty (NativeF55P94UnitFourCell
      (NativeF55P92AssocComparison.original
        (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident r))
      (NativeF55P92AssocComparison.refl r)) := by
  rintro ⟨w⟩
  have h := w.gk5bbOriginalCount_sound
  change (1 : Nat) = 0 at h
  omega

/-- The GK5AZ/GK5BA raw trans SPLIT shell is likewise
UNCONDITIONALLY absent: one original wrapper cannot be
equivalent by P94A four-cells to two original wrappers. -/
theorem nativeGK5BBTransShell_no_P94
    {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s)
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p s t) :
    ¬ Nonempty (NativeF55P94UnitFourCell
      (NativeF55P92AssocComparison.original (.trans f g))
      (.trans (NativeF55P92AssocComparison.original f)
        (NativeF55P92AssocComparison.original g))) := by
  rintro ⟨w⟩
  have h := w.gk5bbOriginalCount_sound
  change (1 : Nat) = (1 : Nat) + 1 at h
  omega

/-- The exact constructor-indexed ident condition introduced
in GK5BA is uninhabited at EVERY original F54 route. -/
theorem nativeGK5BBRequiredIdent_empty
    (r : KuuNativeF45Tree.DepthRotationRoute p first last) :
    ¬ Nonempty (nativeGK5BARequiredShell
      (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident r)) :=
  nativeGK5BBIdent_no_P94 r

/-- The exact stronger GK5BA trans split-shell condition is
uninhabited at EVERY genuine composable original F55 pair. -/
theorem nativeGK5BBRequiredTrans_empty
    {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s)
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p s t) :
    ¬ Nonempty (nativeGK5BARequiredShell (.trans f g)) :=
  nativeGK5BBTransShell_no_P94 f g

/-- Any genuine original F54 route prevents the STRONG GK5BA
constructor shell KIT from being inhabited, as that kit would
be forced to provide the impossible ident shell. -/
theorem nativeGK5BBNoConstructorKit_of_route
    (p : Polygon)
    (D : Type uD) [Category.{vD} D]
    (E : Type uE) [Category.{vE} E]
    {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (r : KuuNativeF45Tree.DepthRotationRoute p first last) :
    ¬ Nonempty (NativeGK5BAConstructorShellKit p D E) := by
  rintro ⟨kit⟩
  exact nativeGK5BBRequiredIdent_empty r
    ⟨kit.shell (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident r)⟩

/-- Even the WEAKER GK5AY universal original-to-phi seam
record is impossible on any actually inhabited original F54
route slot. Its identity field contradicts the count invariant. -/
theorem nativeGK5BBNoGlobalSeam_of_route
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (r : KuuNativeF45Tree.DepthRotationRoute p first last) :
    ¬ Nonempty (NativeGK5AYOriginalPhiSeam first last) := by
  rintro ⟨data⟩
  exact nativeGK5BBIdent_no_P94 r
    ⟨data.bridge (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident r)⟩

/-- Original raw P94A comparisons MUST preserve the numerical
number of original wrappers. Consequently any original F55
source f with recursive phi-count different from ONE has NO
local original-to-phi four-cell seam, regardless of kit. -/
theorem nativeGK5BBNoSeam_if_phi_count_ne_one
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s)
    (h : (nativeGK5AIOriginalToP92Structural f).gk5bbOriginalCount ≠ 1) :
    ¬ Nonempty (nativeGK5AZSeamAt f) := by
  rintro ⟨w⟩
  have hc := w.gk5bbOriginalCount_sound
  have hc' :
      (1 : Nat) = (nativeGK5AIOriginalToP92Structural f).gk5bbOriginalCount := by
    exact hc
  exact h hc'.symm

/-- TRUE north-C60 original four-stage pentagon followed by a
genuine F55 right identity has a missing selected trans SPLIT
shell. The composite direct-to-phi seam is NOT independently
refuted by that split-shell obstruction alone: both sides have
original-wrapper count ONE in this specific example. -/
theorem nativeGK5BBNorthRightIdentityTransShell_no_P94 :
    ¬ Nonempty (NativeF55P94UnitFourCell
      (NativeF55P92AssocComparison.original
        nativeGK5AINorthPentagonWithIdentity)
      (.trans (NativeF55P92AssocComparison.original
        nativeGK5AGNorthOriginalCell)
        (NativeF55P92AssocComparison.original
          (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident
            northNativeF45PentagonShort)))) :=
  nativeGK5BBTransShell_no_P94
    nativeGK5AGNorthOriginalCell
    (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident
      northNativeF45PentagonShort)

/-- Genuine north composite: wrapper count is one on BOTH raw
and recursively structural phi endpoints. The invariant does
NOT settle existence of their direct four-cell seam. -/
theorem nativeGK5BBNorthRightIdentity_count_equal :
    (NativeF55P92AssocComparison.original
      nativeGK5AINorthPentagonWithIdentity).gk5bbOriginalCount =
    (nativeGK5AIOriginalToP92Structural
      nativeGK5AINorthPentagonWithIdentity).gk5bbOriginalCount := rfl

/-- A TRUE north physical C60 original F55 3-proof cycle using
the original pentagon and its actual reverse. This has TWO
primitive original wrapper occurrences under structural phi. -/
def nativeGK5BBNorthPentagonReverseCycle :
    KuuNativeF45Tree.DepthRotationRoute.PresentedCell (.pentagon .north)
      northNativeF45PentagonLong northNativeF45PentagonLong :=
  .trans nativeGK5AGNorthOriginalCell (.symm nativeGK5AGNorthOriginalCell)

/-- The structurally recursive phi of the TRUE original
north pentagon–reverse cycle exposes TWO original wrappers,
not the ONE wrapper around its whole original composite. -/
theorem nativeGK5BBNorthPentagonReverseCycle_phi_count_two :
    (nativeGK5AIOriginalToP92Structural
      nativeGK5BBNorthPentagonReverseCycle).gk5bbOriginalCount = 2 := rfl

/-- For a concrete genuine nontrivial north C60 F55 composite,
not only the split shell but the DIRECT raw original→phi seam
is impossible, by 1 versus 2 original-wrapper count. -/
theorem nativeGK5BBNorthPentagonReverseCycle_no_seam :
    ¬ Nonempty (nativeGK5AZSeamAt
      nativeGK5BBNorthPentagonReverseCycle) := by
  apply nativeGK5BBNoSeam_if_phi_count_ne_one
  change (2 : Nat) ≠ 1
  decide

private def nativeGK5BBNorthFirst :=
  KuuNativeF45Tree.pentagon0 northNativeF45FirstStage
    northNativeF45SecondStage northNativeF45ThirdStage
    northNativeF45FourthStage

private def nativeGK5BBNorthLast :=
  KuuNativeF45Tree.pentagon3 northNativeF45FirstStage
    northNativeF45SecondStage northNativeF45ThirdStage
    northNativeF45FourthStage

/-- Genuine north C60 contains a TRUE original F54 route,
hence no all-constructor GK5BA shell KIT exists in the exact
two actual Site source categories; this is an UNCONDITIONAL
mathematical no-go, not a missing runtime registration. -/
theorem nativeGK5BBNorthNoConstructorKit :
    ¬ Nonempty (NativeGK5BAConstructorShellKit
      (.pentagon .north) Site Site) :=
  nativeGK5BBNoConstructorKit_of_route
    (.pentagon .north) Site Site northNativeF45PentagonShort

/-- Even the strictly weaker full GK5AY original-to-recursive
phi seam record is uninhabited on the true north pentagon
source and target, since an actual original F54 route exists. -/
theorem nativeGK5BBNorthNoGlobalSeam :
    ¬ Nonempty (NativeGK5AYOriginalPhiSeam
      nativeGK5BBNorthFirst nativeGK5BBNorthLast) :=
  nativeGK5BBNoGlobalSeam_of_route
    nativeGK5BBNorthFirst nativeGK5BBNorthLast
    northNativeF45PentagonShort

#print axioms NativeF55P92AssocComparison.gk5bbOriginalCount
#print axioms NativeF55P92AssocComparison.gk5bbTrans_count
#print axioms NativeF55P92AssocComparison.gk5bbHorizontal_count
#print axioms NativeF55P93AssocFourCell.gk5bbOriginalCount_sound
#print axioms NativeF55P94UnitFourCell.gk5bbOriginalCount_sound
#print axioms nativeGK5BBOriginal_count_one
#print axioms nativeGK5BBSelectedRefl_count_zero
#print axioms nativeGK5BBIdent_no_P94
#print axioms nativeGK5BBTransShell_no_P94
#print axioms nativeGK5BBRequiredIdent_empty
#print axioms nativeGK5BBRequiredTrans_empty
#print axioms nativeGK5BBNoConstructorKit_of_route
#print axioms nativeGK5BBNoGlobalSeam_of_route
#print axioms nativeGK5BBNoSeam_if_phi_count_ne_one
#print axioms nativeGK5BBNorthRightIdentityTransShell_no_P94
#print axioms nativeGK5BBNorthRightIdentity_count_equal
#print axioms nativeGK5BBNorthPentagonReverseCycle
#print axioms nativeGK5BBNorthPentagonReverseCycle_phi_count_two
#print axioms nativeGK5BBNorthPentagonReverseCycle_no_seam
#print axioms nativeGK5BBNorthNoConstructorKit
#print axioms nativeGK5BBNorthNoGlobalSeam

end
end Kuu.F112.Physical
