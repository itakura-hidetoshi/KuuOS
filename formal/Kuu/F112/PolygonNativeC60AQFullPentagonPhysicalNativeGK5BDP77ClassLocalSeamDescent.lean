import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5BCLocalUnitSeamWithoutShell
import Mathlib.Tactic

/-!
F112-P94D3GK5BD — finite genuine P77 source-certificate words,
source-typed local seam transport, and an actual descent of
SEAM EXISTENCE to the pre-existing P77 four-cell quotient.

The source relation is genuine Type-valued P77 four-cell
existence, not equality of shadows, strict-path observations,
or structural P92B proof syntax. We retain finite words of
actual P77 certificates with their full F54 endpoint indices.

GK5BC transports actual P94A local seams along any P77 cell.
Consequently the PROPOSITION that a local seam exists is a
well-defined property of the exact P77 quotient class, by a
real Quotient.lift proved using the P77 relation. This is a
local property descent; it is NOT an unconditional global
GK5AY original-to-phi bridge, and does not identify Type-valued
seam inhabitants across quotient representatives.

The original pentagon and disjointSquare generators each
have a genuine reflexive seam; all terms connected to either
by finite true P77 words therefore have direct local seams.
Conversely the original identity class and every P77 class
whose chosen phi original-wrapper count differs from one
have NO local seam. We do NOT claim the two atomic orbits
exhaust the positive seam locus. GK5BB trans-shell and global
no-go, GK5AT/AW source-image obstructions, and GK5AX P89
BadPair conditions remain distinct.

Strict 空 authority; independent Kuu (never imports Qi).
Append-only/tighten-only, original F54 two-Nat/category/Blocks
histories unchanged; public root 107; protected #1558 remains
Draft/open and unmerged. No Gray, sorry, admit, native_decide,
new axioms, or unconditional P89 faithfulness assertions.
Pinned Lean v4.30.0-rc2, mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊.
Apache-2.0.
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

/-- An explicitly FINITE, proof-relevant word of genuine P77
certificates starting at one original F55 proof. Each step
retains the complete dependent F54 source and target history.
P77 itself already contains all unit, associativity, whiskering,
symmetry and concatenation generators. -/
inductive NativeGK5BDP77Word
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (seed : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s →
      Type (max (max uD uE) (max vD vE)) where
  | nil : NativeGK5BDP77Word first last seed seed
  | snoc
      {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
      (prefix : NativeGK5BDP77Word first last seed f)
      (step : NativeF55RawVerticalFourCell first last f g) :
      NativeGK5BDP77Word first last seed g

/-- Fold a finite certificate word into ONE true P77 four-cell,
using only source-level reflexivity and transitivity. -/
def NativeGK5BDP77Word.toP77
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {seed target : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
    (w : NativeGK5BDP77Word first last seed target) :
    NativeF55RawVerticalFourCell first last seed target := by
  induction w with
  | nil => exact .refl _
  | snoc prefix step ih => exact .trans ih step

/-- Every original P77 certificate is in turn a finite
one-step word, so finite-word accessibility is neither
weaker nor stronger than the genuine P77 relation. -/
theorem nativeGK5BDWord_nonempty_iff_P77
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (seed target : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    Nonempty (NativeGK5BDP77Word first last seed target) ↔
      Nonempty (NativeF55RawVerticalFourCell first last seed target) := by
  constructor
  · rintro ⟨w⟩
    exact ⟨w.toP77⟩
  · rintro ⟨w⟩
    exact ⟨.snoc .nil w⟩

/-- A finite P77 word transports an actual local chosen P94A
four-cell, preserving the proof inhabitant rather than only
its Boolean/propositional existence. -/
def nativeGK5BDSeam_of_word
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {seed target : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
    (w : NativeGK5BDP77Word first last seed target)
    (bridge : nativeGK5AZSeamAt seed) :
    nativeGK5AZSeamAt target :=
  nativeGK5BCSeam_transport_P77 (.symm w.toP77) bridge

/-- Exact two-way local-seam existence along any finite genuine
P77 word. No global seam is produced. -/
theorem nativeGK5BDWord_seam_iff
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {seed target : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
    (w : NativeGK5BDP77Word first last seed target) :
    Nonempty (nativeGK5AZSeamAt seed) ↔
      Nonempty (nativeGK5AZSeamAt target) :=
  nativeGK5BCSeam_nonempty_iff_P77 w.toP77

/-- The exact original P77 quotient was constructed at P77.
Membership in one finite-word orbit is EXACTLY equality of
genuine source four-cell classes. -/
theorem nativeGK5BDWord_iff_same_P77_class
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (seed target : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    Nonempty (NativeGK5BDP77Word first last seed target) ↔
      nativeF55RawVerticalFourClass first last seed =
        nativeF55RawVerticalFourClass first last target :=
  (nativeGK5BDWord_nonempty_iff_P77 seed target).trans
    (nativeF55RawVerticalFourClass_eq_iff first last seed target).symm

/-- Genuine QUOTIENT DESCENT: local seam EXISTENCE, as a Prop,
is well-defined on each full source-typed P77 four-cell class.
The proof of representative-independence uses GK5BC source
transport; a shadow equality alone is not sufficient. -/
def nativeGK5BDSeamExistsOnP77Class
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb)
    (r s : KuuNativeF45Tree.DepthRotationRoute p first last) :
    NativeF55RawVerticalFourClasses first last r s → Prop :=
  _root_.Quotient.lift
    (fun f => Nonempty (nativeGK5AZSeamAt f))
    (by
      intro f g related
      rcases related with ⟨w⟩
      exact propext (nativeGK5BCSeam_nonempty_iff_P77 w))

/-- The class-level descent recovers precisely the local direct
P94A seam existence statement at every original representative. -/
theorem nativeGK5BDSeamExistsOnP77Class_mk
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    nativeGK5BDSeamExistsOnP77Class first last r s
      (nativeF55RawVerticalFourClass first last f) ↔
        Nonempty (nativeGK5AZSeamAt f) :=
  Iff.rfl

/-- A positive local seam saturates its true P77 class;
there is no statement that all P77 classes are positive. -/
theorem nativeGK5BDPositiveClass_of_word
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {seed target : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
    (w : NativeGK5BDP77Word first last seed target)
    (seedBridge : nativeGK5AZSeamAt seed) :
    nativeGK5BDSeamExistsOnP77Class first last r s
      (nativeF55RawVerticalFourClass first last target) :=
  ⟨nativeGK5BDSeam_of_word w seedBridge⟩

/-- The entire TRUE original F55 identity class is outside
the positive local-seam locus, by the GK5BB 1-versus-0
original-wrapper obstruction. -/
theorem nativeGK5BDIdentityClass_no_seam
    (r : KuuNativeF45Tree.DepthRotationRoute p first last) :
    ¬ nativeGK5BDSeamExistsOnP77Class first last r r
      (nativeF55RawVerticalFourClass first last
        (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident r)) :=
  nativeGK5BBIdent_no_P94 r

/-- No finite P77 chain originating at an original identity
can enter a positive local-seam class: this is an exact orbit
exclusion, not a failure to find a direct construction. -/
theorem nativeGK5BDIdentityWord_no_seam
    {r : KuuNativeF45Tree.DepthRotationRoute p first last}
    {target : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r r}
    (w : NativeGK5BDP77Word first last
      (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident r) target) :
    ¬ Nonempty (nativeGK5AZSeamAt target) := by
  rintro ⟨bridge⟩
  exact nativeGK5BBIdent_no_P94 r
    ⟨nativeGK5BCSeam_transport_P77 w.toP77 bridge⟩

/-- More generally, a witness of GK5BB's numerical obstruction
at ONE source blocks local seam existence over its entire
finite P77 four-cell orbit. This is distinct from P89 BadPair
and from the impossible raw trans decomposition shell. -/
theorem nativeGK5BDOriginalCount_obstructs_word
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {seed target : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
    (countHole :
      (nativeGK5AIOriginalToP92Structural seed).gk5bbOriginalCount ≠ 1)
    (w : NativeGK5BDP77Word first last seed target) :
    ¬ Nonempty (nativeGK5AZSeamAt target) := by
  rintro ⟨bridge⟩
  exact nativeGK5BBNoSeam_if_phi_count_ne_one seed countHole
    ⟨nativeGK5BCSeam_transport_P77 w.toP77 bridge⟩

private def nativeGK5BDNorthFirst :=
  KuuNativeF45Tree.pentagon0 northNativeF45FirstStage
    northNativeF45SecondStage northNativeF45ThirdStage
    northNativeF45FourthStage

private def nativeGK5BDNorthLast :=
  KuuNativeF45Tree.pentagon3 northNativeF45FirstStage
    northNativeF45SecondStage northNativeF45ThirdStage
    northNativeF45FourthStage

/-- Any genuinely finite P77 word out of the ORIGINAL north
pentagon lies in the positive local-seam class. In particular,
unit insertions, associativity, and their whiskered compositions
require no new global or constructor-indexed shell. -/
theorem nativeGK5BDNorthPentagonWord_seam
    {target : KuuNativeF45Tree.DepthRotationRoute.PresentedCell
      (.pentagon .north)
      northNativeF45PentagonLong northNativeF45PentagonShort}
    (w : NativeGK5BDP77Word nativeGK5BDNorthFirst
      nativeGK5BDNorthLast nativeGK5AGNorthOriginalCell target) :
    Nonempty (nativeGK5AZSeamAt target) :=
  ⟨nativeGK5BDSeam_of_word w (.refl _)⟩

/-- The independent original C60 disjoint-square atom also
extends to a true composite with a LEFT F55 identity, with
no raw trans decomposition shell required. -/
def nativeGK5BDNorthSquareLeftUnitDirectSeam :
    nativeGK5AZSeamAt
      (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans
        (.ident northHexagonNativeSquareLeft)
        northHexagonNativeF55SquareCell) :=
  nativeGK5BCLeftUnitSeam_of_child
    northHexagonNativeF55SquareCell
    nativeGK5AZNorthDisjointSquareAtom

/-- Actual north pentagon followed by TWO original right
identity insertions has an explicit local 4-cell direct seam. -/
def nativeGK5BDNorthDoubleRightUnitDirectSeam :
    nativeGK5AZSeamAt
      (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans
        nativeGK5AINorthPentagonWithIdentity
        (.ident northNativeF45PentagonShort)) :=
  nativeGK5BCRightUnitSeam_of_child
    nativeGK5AINorthPentagonWithIdentity
    nativeGK5BCNorthRightIdentityDirectSeam

/-- Even after TWO genuine original right identity insertions,
the local seam exists while the stronger GK5BA trans split
shell is impossible. The GLOBAL north seam remains impossible
by GK5BB, independently of this positive local witness. -/
theorem nativeGK5BDNorthDoubleRightUnit_seam_but_no_shell :
    Nonempty (nativeGK5AZSeamAt
      (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans
        nativeGK5AINorthPentagonWithIdentity
        (.ident northNativeF45PentagonShort))) ∧
    ¬ Nonempty (nativeGK5BARequiredShell
      (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.trans
        nativeGK5AINorthPentagonWithIdentity
        (.ident northNativeF45PentagonShort))) :=
  nativeGK5BCRightUnitSeam_with_no_split_shell
    nativeGK5AINorthPentagonWithIdentity
    nativeGK5BCNorthRightIdentityDirectSeam

#print axioms NativeGK5BDP77Word
#print axioms NativeGK5BDP77Word.toP77
#print axioms nativeGK5BDWord_nonempty_iff_P77
#print axioms nativeGK5BDSeam_of_word
#print axioms nativeGK5BDWord_seam_iff
#print axioms nativeGK5BDWord_iff_same_P77_class
#print axioms nativeGK5BDSeamExistsOnP77Class
#print axioms nativeGK5BDSeamExistsOnP77Class_mk
#print axioms nativeGK5BDPositiveClass_of_word
#print axioms nativeGK5BDIdentityClass_no_seam
#print axioms nativeGK5BDIdentityWord_no_seam
#print axioms nativeGK5BDOriginalCount_obstructs_word
#print axioms nativeGK5BDNorthPentagonWord_seam
#print axioms nativeGK5BDNorthSquareLeftUnitDirectSeam
#print axioms nativeGK5BDNorthDoubleRightUnitDirectSeam
#print axioms nativeGK5BDNorthDoubleRightUnit_seam_but_no_shell

end
end Kuu.F112.Physical
