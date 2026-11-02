import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK5AHTypedHistoryComparisonInterface
import Mathlib.Tactic

/-!
F112-P94D3GK5AI — original F55 nine-constructor structural,
proof-relevant bridge to selected P92B, and genuinely categorical
GK5AF whole-NatIso pentagon boundary.

Prior GK5AH retained all original F54-shaped TWO-Nat, two-category
raw route history. GK5AI additionally keeps the distinct Type-valued
F55 3-cell PROOF HISTORIES, even when both raw endpoints and their
whole categorical NatIso equalities are identical.

Every one of the original F55 NINE constructors is interpreted
structurally inside the chosen P92B Type-valued syntax: ident to
refl, original pentagon/square to original, all seven further
composite/context constructors to their corresponding P92B constructors.
The adjoined P92B assocNaturality is NEVER attributed to old F55.

A true original north-C60 F55 pentagon generator and its distinct
postcomposition with a genuine original identity cell map to
distinct P92B Type-valued comparison terms, while both induce
the very SAME true Mathlib whole NatIso pentagon equality.
A typed packet is faithful precisely because it retains the
original F55 3-cell proof term; an Eq-only evaluation cannot be.

For the real three-north-sector unit naturality obstruction,
P92B has a NEW actual assocNaturality witness but NO original
F55 witness can map to it, by the existing P92A no-go.
No general F54-to-whole-NatIso functor or higher physical
C60 filler is asserted.

Independent Kuu only; Qi imports this module, never conversely.
Append-only, tighten-only, no Gray, same public root107.
Lean v4.30.0-rc2 / mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
No sorry, native_decide, new axioms, or protected #1558 changes.
Copyright (c) 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section
universe uD vD uE vE uI vC uC uT

/-- An ACTUAL structural interpretation of all NINE original
F55 Type-valued 3-cell constructors into the separately chosen
P92B Type-valued syntax. This is NOT the P92B quotient, nor the
claim that its extra assocNaturality generator is derivable from
original F55. Unlike the trivial .original wrapper on an entire
composite proof, this maps ALL original constructors recursively. -/
def nativeGK5AIOriginalToP92Structural
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (cell : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    NativeF55P92AssocComparison p r s := by
  induction cell with
  | ident route => exact .refl route
  | pentagon t₁ t₂ t₃ t₄ =>
      exact .original (.pentagon t₁ t₂ t₃ t₄)
  | disjointSquare left right =>
      exact .original (.disjointSquare left right)
  | symm cell ih => exact .symm ih
  | trans left right ihLeft ihRight =>
      exact .trans ihLeft ihRight
  | leftContext cell later ih => exact .leftContext ih later
  | rightContext earlier cell ih => exact .rightContext earlier ih
  | precompose priorRoute cell ih =>
      exact .precompose priorRoute ih
  | postcompose cell suffix ih =>
      exact .postcompose ih suffix

/-- The complete independently reconstructed Type-valued F54
north pentagon source and target are unchanged from GK5AG/AH. -/
abbrev NativeGK5AINorthPentagonCells :=
  KuuNativeF45Tree.DepthRotationRoute.PresentedCell
    (.pentagon .north)
    northNativeF45PentagonLong northNativeF45PentagonShort

/-- A REAL second original F55 3-cell with the SAME dependent
source/target as the original pentagon: postcompose its true
pentagon 3-cell with a true F55 identity 3-cell. -/
def nativeGK5AINorthPentagonWithIdentity :
    NativeGK5AINorthPentagonCells :=
  .trans nativeGK5AGNorthOriginalCell
    (.ident northNativeF45PentagonShort)

/-- Distinct original nine-constructor Type-valued F55 3-PROOFS,
even though the original F54 source and target are identical. -/
theorem nativeGK5AINorthTwoOriginalCells_distinct :
    (nativeGK5AGNorthOriginalCell : NativeGK5AINorthPentagonCells) ≠
      nativeGK5AINorthPentagonWithIdentity :=
  northNativeF55PentagonCell_ne_withUnit

/-- The original north pentagon generator itself maps to the
TRUE selected P92B .original higher witness, not any invented
assocNaturality evidence. -/
theorem nativeGK5AINorthPentagon_structural :
    nativeGK5AIOriginalToP92Structural nativeGK5AGNorthOriginalCell =
      nativeGK5AGNorthP92Cell := rfl

/-- Original F55 trans is preserved DEFINITIONALLY by the
structural translation; no 0-truncation or equality is used. -/
theorem nativeGK5AINorthStructural_trans
    {r s t : NativeGK5AGNorthHistory}
    (left : KuuNativeF45Tree.DepthRotationRoute.PresentedCell
      (.pentagon .north) r s)
    (right : KuuNativeF45Tree.DepthRotationRoute.PresentedCell
      (.pentagon .north) s t) :
    nativeGK5AIOriginalToP92Structural (.trans left right) =
      NativeF55P92AssocComparison.trans
        (nativeGK5AIOriginalToP92Structural left)
        (nativeGK5AIOriginalToP92Structural right) := rfl

/-- Original F55 symm is preserved DEFINITIONALLY by the
structural map, for all actual north dependent F54 endpoints. -/
theorem nativeGK5AINorthStructural_symm
    {r s : NativeGK5AGNorthHistory}
    (cell : KuuNativeF45Tree.DepthRotationRoute.PresentedCell
      (.pentagon .north) r s) :
    nativeGK5AIOriginalToP92Structural (.symm cell) =
      NativeF55P92AssocComparison.symm
        (nativeGK5AIOriginalToP92Structural cell) := rfl

/-- The two genuinely different source F55 3-proofs give TWO
different proof-relevant selected P92B Type-valued terms.
The translation does not need to quotient their proofs. -/
theorem nativeGK5AINorthStructuralProofs_distinct :
    nativeGK5AIOriginalToP92Structural nativeGK5AGNorthOriginalCell ≠
      nativeGK5AIOriginalToP92Structural
        nativeGK5AINorthPentagonWithIdentity := by
  intro h
  cases h

/-- The original F54 long/short histories still yield equal
P92B CLASS objects, independent of WHICH F55 3-proof compares
them. This is an equality of quotient objects, NOT 3-cells. -/
theorem nativeGK5AINorthSameClasses_withDistinctProofs :
    (nativeGK5AGNorthP92Class northNativeF45PentagonLong =
      nativeGK5AGNorthP92Class northNativeF45PentagonShort) ∧
    (nativeGK5AGNorthOriginalCell ≠
      nativeGK5AINorthPentagonWithIdentity) :=
  ⟨nativeGK5AGNorthP92Classes_equal,
   nativeGK5AINorthTwoOriginalCells_distinct⟩

/-- The genuine P92B extra assocNaturality constructor on the
THREE ACTUAL north C60 F45 unit routes. It is a selected NEW
Type-valued witness, not an original F55 3-cell. -/
def nativeGK5AINorthAddedUnitAssocCell :
    NativeF55P92AssocComparison (.pentagon .north)
      (nativeF54P90AssocNaturalityLeftRoute
        (nativeF54P92UnitRoute northNativeF45FirstStage)
        (nativeF54P92UnitRoute northNativeF45SecondStage)
        (nativeF54P92UnitRoute northNativeF45ThirdStage))
      (nativeF54P90AssocNaturalityRightRoute
        (nativeF54P92UnitRoute northNativeF45FirstStage)
        (nativeF54P92UnitRoute northNativeF45SecondStage)
        (nativeF54P92UnitRoute northNativeF45ThirdStage)) :=
  .assocNaturality
    (nativeF54P92UnitRoute northNativeF45FirstStage)
    (nativeF54P92UnitRoute northNativeF45SecondStage)
    (nativeF54P92UnitRoute northNativeF45ThirdStage)

/-- The EXPLICITLY NEW P92B unit naturality witness has NO
original F55 preimage under the nine-constructor structural map,
using the true original ordered-context no-go. -/
theorem nativeGK5AINorthAddedUnitAssoc_noOriginalPreimage :
    ¬ ∃ old :
        NativeF55P90AssocNaturalityCell
          (nativeF54P92UnitRoute northNativeF45FirstStage)
          (nativeF54P92UnitRoute northNativeF45SecondStage)
          (nativeF54P92UnitRoute northNativeF45ThirdStage),
      nativeGK5AIOriginalToP92Structural old =
        nativeGK5AINorthAddedUnitAssocCell := by
  rintro ⟨old, _⟩
  exact northNativeF55P92_original_unit_naturality_no_filler
    ⟨old⟩

/-- An ACTUAL selected new Type-valued P92B comparison exists
where the original F55 evidence type is EMPTY. Both statements
are about the exact three-unit north C60 native source, not
a universal categorical impossibility. -/
theorem nativeGK5AINorthAddedUnitAssoc_strictBoundary :
    Nonempty (NativeF55P92AssocComparison (.pentagon .north)
      (nativeF54P90AssocNaturalityLeftRoute
        (nativeF54P92UnitRoute northNativeF45FirstStage)
        (nativeF54P92UnitRoute northNativeF45SecondStage)
        (nativeF54P92UnitRoute northNativeF45ThirdStage))
      (nativeF54P90AssocNaturalityRightRoute
        (nativeF54P92UnitRoute northNativeF45FirstStage)
        (nativeF54P92UnitRoute northNativeF45SecondStage)
        (nativeF54P92UnitRoute northNativeF45ThirdStage))) ∧
    ¬ Nonempty (NativeF55P90AssocNaturalityCell
      (nativeF54P92UnitRoute northNativeF45FirstStage)
      (nativeF54P92UnitRoute northNativeF45SecondStage)
      (nativeF54P92UnitRoute northNativeF45ThirdStage)) := by
  exact ⟨⟨nativeGK5AINorthAddedUnitAssocCell⟩,
    northNativeF55P92_original_unit_naturality_no_filler⟩

section GenuineWholeNatIso
variable {I : Type uI} {C D E F G : I → Cat.{vC,uC}}
variable (e₁ : ∀ i : I, C i ≌ D i)
variable (e₂ : ∀ i : I, D i ≌ E i)
variable (e₃ : ∀ i : I, E i ≌ F i)
variable (e₄ : ∀ i : I, F i ≌ G i)
variable {i j : I} (R : C i ⥤ C j)

/-- GENUINE original Type-valued F55 comparison + structurally
mapped Type-valued P92B certificate + true GK5AF Mathlib whole
NatIso equality, WITHOUT identifying any of their evidence types. -/
structure NativeGK5AIOriginalWholeCellPacket where
  original : NativeGK5AINorthPentagonCells
  mappedP92 : NativeF55P92AssocComparison (.pentagon .north)
    northNativeF45PentagonLong northNativeF45PentagonShort
  preservesP92 :
    mappedP92 = nativeGK5AIOriginalToP92Structural original
  wholeNatIso :
    nativeGK5AFLongPath e₁ e₂ e₃ e₄ R =
      nativeGK5AFShortPath e₁ e₂ e₃ e₄ R

/-- EVERY original north F55 cell between the actual 3-vs-2
source histories has a full typed bridge to the TRUE whole
NatIso pentagon equality. This is a LOCAL boundary interface,
not a global source-to-NatIso pseudofunctor/higher filler. -/
def nativeGK5AILocalWholePacket (cell : NativeGK5AINorthPentagonCells) :
    NativeGK5AIOriginalWholeCellPacket e₁ e₂ e₃ e₄ R where
  original := cell
  mappedP92 := nativeGK5AIOriginalToP92Structural cell
  preservesP92 := rfl
  wholeNatIso := nativeGK5AFPaths_whole e₁ e₂ e₃ e₄ R

/-- The proof-relevant local bridge retains each distinct
ORIGINAL F55 higher-cell history, not merely its existence. -/
theorem nativeGK5AILocalWholePacket_injective :
    Function.Injective (nativeGK5AILocalWholePacket e₁ e₂ e₃ e₄ R) := by
  intro x y h
  exact congrArg NativeGK5AIOriginalWholeCellPacket.original h

/-- The two true different north F55 3-proof paths yield
DISTINCT fully typed categorical-comparison packets even
though they have identical source/target and whole Eq boundary. -/
theorem nativeGK5AILocalWholePackets_distinct :
    nativeGK5AILocalWholePacket e₁ e₂ e₃ e₄ R
      nativeGK5AGNorthOriginalCell ≠
    nativeGK5AILocalWholePacket e₁ e₂ e₃ e₄ R
      nativeGK5AINorthPentagonWithIdentity := by
  intro h
  exact nativeGK5AINorthTwoOriginalCells_distinct
    ((nativeGK5AILocalWholePacket_injective e₁ e₂ e₃ e₄ R) h)

/-- The two packets nevertheless have exactly the same
Mathematical whole NatIso EQUALITY PROOF, by proof irrelevance.
No claim is made that their F55 source proof terms are equal. -/
theorem nativeGK5AILocalWholeEqProofs_equal :
    (nativeGK5AILocalWholePacket e₁ e₂ e₃ e₄ R
      nativeGK5AGNorthOriginalCell).wholeNatIso =
    (nativeGK5AILocalWholePacket e₁ e₂ e₃ e₄ R
      nativeGK5AINorthPentagonWithIdentity).wholeNatIso :=
  Subsingleton.elim _ _

/-- No interpretation of the original two distinct Type-valued
F55 proof terms as merely equality proofs of the true whole
Mathlib NatIso can be injective. This is a STRICTER higher-cell
obstruction than GK5AH's raw F54 OBJECT noninjectivity. -/
theorem nativeGK5AIWholeEqProofMap_not_injective
    (interpret : NativeGK5AINorthPentagonCells →
      (nativeGK5AFLongPath e₁ e₂ e₃ e₄ R =
       nativeGK5AFShortPath e₁ e₂ e₃ e₄ R)) :
    ¬ Function.Injective interpret := by
  intro hinj
  apply nativeGK5AINorthTwoOriginalCells_distinct
  apply hinj
  exact Subsingleton.elim _ _

#print axioms nativeGK5AILocalWholePacket
#print axioms nativeGK5AILocalWholePacket_injective
#print axioms nativeGK5AILocalWholePackets_distinct
#print axioms nativeGK5AILocalWholeEqProofs_equal
#print axioms nativeGK5AIWholeEqProofMap_not_injective
end GenuineWholeNatIso

#print axioms nativeGK5AIOriginalToP92Structural
#print axioms nativeGK5AINorthStructural_trans
#print axioms nativeGK5AINorthStructural_symm
#print axioms nativeGK5AINorthStructuralProofs_distinct
#print axioms nativeGK5AINorthSameClasses_withDistinctProofs
#print axioms nativeGK5AINorthAddedUnitAssoc_noOriginalPreimage
#print axioms nativeGK5AINorthAddedUnitAssoc_strictBoundary

end
end Kuu.F112.Physical
