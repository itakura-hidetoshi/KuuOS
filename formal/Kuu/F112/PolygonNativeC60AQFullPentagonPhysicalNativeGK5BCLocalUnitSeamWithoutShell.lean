import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5BBOriginalWrapperCountObstruction
import Mathlib.Tactic

/-!
F112-P94D3GK5BC — constructive LOCAL original-to-structural-phi
four-cell seam, without the impossible GK5BA trans split-shell.

GK5BB established that original-wrapper count is preserved by
all 16 chosen P93C and all 19 P94A four-cell constructors.
Original(F55.ident) to P92B.refl is therefore impossible, and
Original(F55.trans f g) to trans(original f, original g) is
also impossible. Consequently neither a full GK5BA constructor
shell-kit nor a GK5AY UNIVERSAL seam exists over inhabited F54.

These no-go theorems do NOT prohibit all particular original→phi
four-cells. The original P77 *vertical right/left unit* 4-proofs
survive through the actual P80→P85→P86→P87→P89→P93C→P94A
SEVEN old-wrapper embeddings. The chosen P94A vertical unit
4-proofs then construct the direct seam for f followed by an
original F55 identity from a local seam of f. The dual left
unit obeys the analogous constructive law. Both directions
actually give exact existence equivalences between a local
seam of f and of its unit-extended source: no uninhabited
GK5BA shell is supplied or inferred.

More generally, an actual P77 four-proof f→g yields a selected
4-cell between both raw wrappers AND a structurally mapped P93C
four-proof between phi f and phi g (via existing GK5AJ). These
transport local seams in either direction. This is genuinely
proof-relevant 4-cell gluing over real original F54 slots, NOT
a global seam or an arbitrary P94A normalization.

In particular the TRUE north C60 original pentagon atom has
an unconditional reflexive seam. The original pentagon followed
by an actual F55 right identity therefore ALSO has a true
direct selected P94A four-cell seam, although GK5BB proved its
raw trans SPLIT shell is impossible. It supplies a concrete
counterexample to sufficiency being necessary: nonempty
SeamAt(f) does NOT imply nonempty RequiredShell(f).
The original-wrapper count is ONE at both direct endpoints,
fully compatible with GK5BB's all-19-constructor theorem.

This never manufactures a seam at the true identity itself,
never yields the full GK5AY seam record or the GK5BA universal
constructor kit, and makes no unconditional P89 class-map
faithfulness/nonfaithfulness claim. Original F54 double-Nat,
two-category and Blocks history unchanged, strict 空 authority,
independent Kuu→Qi, root107 and protected #1558 Draft/open.
Pinned Lean v4.30.0-rc2, mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Append-only; no Gray, sorry, admit, native_decide, new axioms.
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

/-- The complete exact ORIGINAL P77→P80→P85→P86→P87→P89→P93C
→P94A embedding, retaining every Type-valued old witness as one
genuine higher four-proof with RAW P92B.original endpoints. -/
def nativeGK5BCP77_to_rawP94
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
    (w : NativeF55RawVerticalFourCell first last f g) :
    NativeF55P94UnitFourCell
      (NativeF55P92AssocComparison.original f)
      (NativeF55P92AssocComparison.original g) :=
  .old (.old (.old (.old (.old (.old (.old w))))))

/-- The original F55 right-unit comparison genuinely exists
between TWO raw ORIGINAL P92B wrappers; no equality of original
three-proof syntax or a GK5BA trans-shell is being assumed. -/
def nativeGK5BCRawRightUnit
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    NativeF55P94UnitFourCell
      (NativeF55P92AssocComparison.original (.trans f (.ident s)))
      (NativeF55P92AssocComparison.original f) :=
  nativeGK5BCP77_to_rawP94
    (NativeF55RawVerticalFourCell.rightUnit f)

/-- The genuine original F55 left unit has an analogous RAW
P94A four-cell through the same seven old inclusions. -/
def nativeGK5BCRawLeftUnit
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    NativeF55P94UnitFourCell
      (NativeF55P92AssocComparison.original (.trans (.ident r) f))
      (NativeF55P92AssocComparison.original f) :=
  nativeGK5BCP77_to_rawP94
    (NativeF55RawVerticalFourCell.leftUnit f)

/-- A *LOCAL* direct seam of f extends to original F55 right
identity composition WITHOUT its impossible trans decomposition
shell and WITHOUT an independent seam of the original identity.
The last edge is chosen P94A verticalRightUnit in REVERSE. -/
def nativeGK5BCRightUnitSeam_of_child
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s)
    (bridge : nativeGK5AZSeamAt f) :
    nativeGK5AZSeamAt (.trans f (.ident s)) :=
  .trans
    (.trans (nativeGK5BCRawRightUnit f) bridge)
    (.symm (.verticalRightUnit (nativeGK5AIOriginalToP92Structural f)))

/-- Dual LEFT original F55 unit extension, relying only on the
existing local seam of f, raw P77 leftUnit, and chosen P94A
verticalLeftUnit; no original identity seam is required. -/
def nativeGK5BCLeftUnitSeam_of_child
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s)
    (bridge : nativeGK5AZSeamAt f) :
    nativeGK5AZSeamAt (.trans (.ident r) f) :=
  .trans
    (.trans (nativeGK5BCRawLeftUnit f) bridge)
    (.symm (.verticalLeftUnit (nativeGK5AIOriginalToP92Structural f)))

/-- Conversely, a DIRECT seam of the right-unit-extended
original F55 source transports BACK to a local seam of f.
Both raw and selected vertical 4-cell units are actual proofs. -/
def nativeGK5BCRightUnitSeam_to_child
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s)
    (bridge : nativeGK5AZSeamAt (.trans f (.ident s))) :
    nativeGK5AZSeamAt f :=
  .trans
    (.trans (.symm (nativeGK5BCRawRightUnit f)) bridge)
    (.verticalRightUnit (nativeGK5AIOriginalToP92Structural f))

/-- Left-unit cancellation for exact local seams, without any
separately inhabited full constructor shell-kit. -/
def nativeGK5BCLeftUnitSeam_to_child
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s)
    (bridge : nativeGK5AZSeamAt (.trans (.ident r) f)) :
    nativeGK5AZSeamAt f :=
  .trans
    (.trans (.symm (nativeGK5BCRawLeftUnit f)) bridge)
    (.verticalLeftUnit (nativeGK5AIOriginalToP92Structural f))

/-- Genuine right F55 identity extension preserves and REFLECTS
the existence of a direct original→phi seam. No trans split shell
is supplied in either direction. -/
theorem nativeGK5BCRightUnitSeam_nonempty_iff
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    Nonempty (nativeGK5AZSeamAt (.trans f (.ident s))) ↔
      Nonempty (nativeGK5AZSeamAt f) := by
  constructor
  · rintro ⟨w⟩
    exact ⟨nativeGK5BCRightUnitSeam_to_child f w⟩
  · rintro ⟨w⟩
    exact ⟨nativeGK5BCRightUnitSeam_of_child f w⟩

/-- Left F55 identity extension also preserves and REFLECTS
local seam existence through genuine original and selected
vertical units, not any raw syntax equation. -/
theorem nativeGK5BCLeftUnitSeam_nonempty_iff
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    Nonempty (nativeGK5AZSeamAt (.trans (.ident r) f)) ↔
      Nonempty (nativeGK5AZSeamAt f) := by
  constructor
  · rintro ⟨w⟩
    exact ⟨nativeGK5BCLeftUnitSeam_to_child f w⟩
  · rintro ⟨w⟩
    exact ⟨nativeGK5BCLeftUnitSeam_of_child f w⟩

/-- Any TRUE original P77 four-proof can be used to transport
individual direct seams from the genuine original source g to f.
It glues ACTUAL RAW P94A old(w), the given seam of g and the
INVERSE of GK5AJ's actual structural P93C proof for f→g.
It never supplies a universal global GK5AY seam. -/
def nativeGK5BCSeam_transport_P77
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
    (w : NativeF55RawVerticalFourCell first last f g)
    (bridge : nativeGK5AZSeamAt g) :
    nativeGK5AZSeamAt f :=
  .trans
    (.trans (nativeGK5BCP77_to_rawP94 w) bridge)
    (.symm (.old (nativeGK5AJOriginalFourToP93 first last w)))

/-- A full original P77 four-cell makes direct local seam
EXISTENCE equivalent between the two actual original F55
Type-valued three-proof terms. This is a source-typed local
transport equivalence, not a global seam nor quotient equality. -/
theorem nativeGK5BCSeam_nonempty_iff_P77
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    {f g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s}
    (w : NativeF55RawVerticalFourCell first last f g) :
    Nonempty (nativeGK5AZSeamAt f) ↔
      Nonempty (nativeGK5AZSeamAt g) := by
  constructor
  · rintro ⟨bridge⟩
    exact ⟨nativeGK5BCSeam_transport_P77 (.symm w) bridge⟩
  · rintro ⟨bridge⟩
    exact ⟨nativeGK5BCSeam_transport_P77 w bridge⟩

/-- With the original P77 associativity four-cell, local seam
existence can be transferred in BOTH DIRECTIONS between the
actually different parenthesized ORIGINAL F55 3-proof trees. -/
theorem nativeGK5BCAssoc_seam_nonempty_iff
    {r s t u : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s)
    (g : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p s t)
    (h : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p t u) :
    Nonempty (nativeGK5AZSeamAt (.trans (.trans f g) h)) ↔
      Nonempty (nativeGK5AZSeamAt (.trans f (.trans g h))) :=
  nativeGK5BCSeam_nonempty_iff_P77
    (NativeF55RawVerticalFourCell.assoc f g h)

/-- A TRUE original F55 right-unit extension has a direct seam
whenever f already has a local seam, even though the STRONG
constructor-specific raw trans shell is mathematically impossible.
This is a precise strict separation between GK5AZ and GK5BA
local sufficient conditions and real direct seam existence. -/
theorem nativeGK5BCRightUnitSeam_with_no_split_shell
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s)
    (bridge : nativeGK5AZSeamAt f) :
    Nonempty (nativeGK5AZSeamAt (.trans f (.ident s))) ∧
    ¬ Nonempty (nativeGK5BARequiredShell (.trans f (.ident s))) :=
  ⟨⟨nativeGK5BCRightUnitSeam_of_child f bridge⟩,
   nativeGK5BBRequiredTrans_empty f (.ident s)⟩

/-- The LEFT unit extension exhibits the same strong-shell
absence despite a local direct seam constructed without it. -/
theorem nativeGK5BCLeftUnitSeam_with_no_split_shell
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (f : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s)
    (bridge : nativeGK5AZSeamAt f) :
    Nonempty (nativeGK5AZSeamAt (.trans (.ident r) f)) ∧
    ¬ Nonempty (nativeGK5BARequiredShell (.trans (.ident r) f)) :=
  ⟨⟨nativeGK5BCLeftUnitSeam_of_child f bridge⟩,
   nativeGK5BBRequiredTrans_empty (.ident r) f⟩

/-- A REAL original north-C60 pentagon atom has a definitional
P94A.refl local seam, which extends across its ACTUAL original
F55 right identity via raw P77 and selected P94A vertical units.
This direct proof does not require any nonexisting trans shell. -/
def nativeGK5BCNorthRightIdentityDirectSeam :
    nativeGK5AZSeamAt nativeGK5AINorthPentagonWithIdentity :=
  nativeGK5BCRightUnitSeam_of_child
    nativeGK5AGNorthOriginalCell (.refl _)

/-- A genuinely proven NORTH C60 direct seam coexists with the
UNCONDITIONAL no-go for the raw trans SPLIT shell, not a shadow
or a propositionally postulated bridge. This settles GK5BB's
specific equal-wrapper-count direct-seam research question. -/
theorem nativeGK5BCNorthDirectSeam_and_no_split :
    Nonempty (nativeGK5AZSeamAt
      nativeGK5AINorthPentagonWithIdentity) ∧
    ¬ Nonempty (nativeGK5BARequiredShell
      nativeGK5AINorthPentagonWithIdentity) :=
  ⟨⟨nativeGK5BCNorthRightIdentityDirectSeam⟩,
   nativeGK5BBRequiredTrans_empty
     nativeGK5AGNorthOriginalCell
     (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.ident
       northNativeF45PentagonShort)⟩

/-- The direct north seam is a genuine comparison between two
UNEQUAL original-versus-structural P92B proof terms with the
SAME original-wrapper count one, consistent with GK5BB. -/
theorem nativeGK5BCNorthNontrivialDirectSeam :
    ((NativeF55P92AssocComparison.original
        nativeGK5AINorthPentagonWithIdentity) ≠
      nativeGK5AIOriginalToP92Structural
        nativeGK5AINorthPentagonWithIdentity) ∧
    Nonempty (nativeGK5AZSeamAt
      nativeGK5AINorthPentagonWithIdentity) ∧
    ((NativeF55P92AssocComparison.original
        nativeGK5AINorthPentagonWithIdentity).gk5bbOriginalCount =
      (nativeGK5AIOriginalToP92Structural
        nativeGK5AINorthPentagonWithIdentity).gk5bbOriginalCount) :=
  ⟨nativeGK5AYNorthRawOriginal_ne_structuralPhi,
    ⟨nativeGK5BCNorthRightIdentityDirectSeam⟩,
    nativeGK5BBNorthRightIdentity_count_equal⟩

/-- This genuine north example gives a counterexample to the
reverse of GK5BA's sufficient local shell gate, at an EXACT
source-typed original F55 proof term. The strong required
trans shell is impossible despite an actual local seam. -/
theorem nativeGK5BCNorthSeam_does_not_force_requiredShell :
    ¬ (Nonempty (nativeGK5AZSeamAt
          nativeGK5AINorthPentagonWithIdentity) →
        Nonempty (nativeGK5BARequiredShell
          nativeGK5AINorthPentagonWithIdentity)) := by
  intro h
  exact nativeGK5BCNorthDirectSeam_and_no_split.2
    (h nativeGK5BCNorthDirectSeam_and_no_split.1)

/-- In the SAME north C60 original F54 slot, a LOCAL direct seam
does exist but the GK5AY UNIVERSAL seam record is impossible.
Local proof transport and global gluing must remain distinct. -/
private def nativeGK5BCNorthFirst :=
  KuuNativeF45Tree.pentagon0 northNativeF45FirstStage
    northNativeF45SecondStage northNativeF45ThirdStage
    northNativeF45FourthStage

private def nativeGK5BCNorthLast :=
  KuuNativeF45Tree.pentagon3 northNativeF45FirstStage
    northNativeF45SecondStage northNativeF45ThirdStage
    northNativeF45FourthStage

theorem nativeGK5BCNorthLocal_yes_global_no :
    Nonempty (nativeGK5AZSeamAt
      nativeGK5AINorthPentagonWithIdentity) ∧
    ¬ Nonempty (NativeGK5AYOriginalPhiSeam
      nativeGK5BCNorthFirst nativeGK5BCNorthLast) :=
  ⟨⟨nativeGK5BCNorthRightIdentityDirectSeam⟩,
    nativeGK5BBNorthNoGlobalSeam⟩

#print axioms nativeGK5BCP77_to_rawP94
#print axioms nativeGK5BCRawRightUnit
#print axioms nativeGK5BCRawLeftUnit
#print axioms nativeGK5BCRightUnitSeam_of_child
#print axioms nativeGK5BCLeftUnitSeam_of_child
#print axioms nativeGK5BCRightUnitSeam_to_child
#print axioms nativeGK5BCLeftUnitSeam_to_child
#print axioms nativeGK5BCRightUnitSeam_nonempty_iff
#print axioms nativeGK5BCLeftUnitSeam_nonempty_iff
#print axioms nativeGK5BCSeam_transport_P77
#print axioms nativeGK5BCSeam_nonempty_iff_P77
#print axioms nativeGK5BCAssoc_seam_nonempty_iff
#print axioms nativeGK5BCRightUnitSeam_with_no_split_shell
#print axioms nativeGK5BCLeftUnitSeam_with_no_split_shell
#print axioms nativeGK5BCNorthRightIdentityDirectSeam
#print axioms nativeGK5BCNorthDirectSeam_and_no_split
#print axioms nativeGK5BCNorthNontrivialDirectSeam
#print axioms nativeGK5BCNorthSeam_does_not_force_requiredShell
#print axioms nativeGK5BCNorthLocal_yes_global_no

end
end Kuu.F112.Physical
