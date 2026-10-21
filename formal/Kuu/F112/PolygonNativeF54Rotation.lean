import Kuu.F112.PolygonNativeF45Source

/-!
# F112-E7M / independent original-shaped typed F54 local rotations

The historical original F54 root LocalRotation is NOT a free
reassociation of untyped C60 sectors. Its source is an ORIGINAL
F45 bracket tree transported along both independent Nat.add_assoc
equalities, with separately typed F19/F28 Blocks at EVERY internal
boundary; arbitrary left/right contexts preserve all four Blocks
endpoints.

We implement the same TYPE SHAPE using the new independent
category-polymorphic KuuNativeF45Tree from E7L. Each primitive
rotation is a genuine Type-valued witness. The two independent Nat
casts are explicit and proved sound under the E7A physical erasure;
full ordered C60 sectors survive any nested local rotation.

This is NOT an import, isomorphism, or equivalence with the historical
original F19/F28 OneStep, AxisTrace, F54 LocalRotation or F55
PresentedCell. In particular equality of arbitrary old raw axis proof
trees has NOT been asserted merely from category composite equality.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
noncomputable section

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

/-- Cast BOTH independent F19/F28-shaped primitive history depths,
while retaining every original C60 sector, block boundary and
actual two-category F45 leaf witness. -/
def KuuNativeF45Tree.castDepths
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (hn : n = n') (hm : m = m')
    (tree : KuuNativeF45Tree p n m ma pa mb pb) :
    KuuNativeF45Tree p n' m' ma pa mb pb := by
  cases hn
  cases hm
  exact tree

/-- Double-Nat cast preserves the full original physical C60-sector
list, not just the two total depths or evaluated native arrows. -/
theorem KuuNativeF45Tree.sectors_castDepths
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (hn : n = n') (hm : m = m')
    (tree : KuuNativeF45Tree p n m ma pa mb pb) :
    (KuuNativeF45Tree.castDepths hn hm tree).sectors =
      tree.sectors := by
  cases hn
  cases hm
  rfl

/-- Reindexing the actual two-category source and THEN projecting
to the E7A physical depth source agrees exactly with transporting
that depth source along BOTH dependent Nat equality proofs. -/
theorem KuuNativeF45Tree.erasePhysical_castDepths
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (hn : n = n') (hm : m = m')
    (tree : KuuNativeF45Tree p n m ma pa mb pb) :
    (KuuNativeF45Tree.castDepths hn hm tree).erasePhysical =
      cast (congrArg₂ (PolygonDepthTree p) hn hm) tree.erasePhysical := by
  cases hn
  cases hm
  rfl

/-- An actual F54-shaped local associator on ORIGINAL-SHAPED
double-axis Blocks stages. Both Nat indices are cast explicitly on
the source, as in the historical F54 constructor; they are NOT
replaced by an untyped binary tree reassociation. -/
inductive KuuNativeF45Tree.LocalRotation (p : Polygon) :
    ∀ {a b : D} {x y : E} {n m : Nat}
      {ma mb : KuuNativeBlocks a b}
      {pa pb : KuuNativeBlocks x y},
      KuuNativeF45Tree p n m ma pa mb pb →
      KuuNativeF45Tree p n m ma pa mb pb →
      Type (max (max uD uE) (max vD vE)) where
  | assoc
      {a b : D} {x y : E}
      {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
      {p₀ p₁ p₂ p₃ : KuuNativeBlocks a b}
      {q₀ q₁ q₂ q₃ : KuuNativeBlocks x y}
      (first : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁)
      (second : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂)
      (third : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃) :
      LocalRotation p
        (KuuNativeF45Tree.castDepths
          (Nat.add_assoc n₁ n₂ n₃) (Nat.add_assoc m₁ m₂ m₃)
          (KuuNativeF45Tree.node
            (KuuNativeF45Tree.node first second) third))
        (KuuNativeF45Tree.node first
          (KuuNativeF45Tree.node second third))
  | leftContext
      {a b : D} {x y : E}
      {n m n' m' : Nat}
      {ma mb mc : KuuNativeBlocks a b}
      {pa pb pc : KuuNativeBlocks x y}
      {before after : KuuNativeF45Tree p n m ma pa mb pb}
      (step : LocalRotation p before after)
      (later : KuuNativeF45Tree p n' m' mb pb mc pc) :
      LocalRotation p
        (KuuNativeF45Tree.node before later)
        (KuuNativeF45Tree.node after later)
  | rightContext
      {a b : D} {x y : E}
      {n m n' m' : Nat}
      {ma mb mc : KuuNativeBlocks a b}
      {pa pb pc : KuuNativeBlocks x y}
      (earlier : KuuNativeF45Tree p n m ma pa mb pb)
      {before after : KuuNativeF45Tree p n' m' mb pb mc pc}
      (step : LocalRotation p before after) :
      LocalRotation p
        (KuuNativeF45Tree.node earlier before)
        (KuuNativeF45Tree.node earlier after)

/-- EVERY independent original-shaped root/contextual F54 rotation
preserves the complete ORDERED ORIGINAL C60 SECTOR LIST.
The root case uses the explicit two-Nat transport and actual
List.append_assoc, never an assumed global Gray interchange. -/
theorem KuuNativeF45Tree.LocalRotation.sectors_eq
    {p : Polygon} {a b : D} {x y : E} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {before after : KuuNativeF45Tree p n m ma pa mb pb}
    (step : KuuNativeF45Tree.LocalRotation p before after) :
    before.sectors = after.sectors := by
  induction step with
  | assoc first second third =>
      rw [KuuNativeF45Tree.sectors_castDepths]
      change
        (first.sectors ++ second.sectors) ++ third.sectors =
          first.sectors ++ (second.sectors ++ third.sectors)
      exact List.append_assoc _ _ _
  | leftContext step later ih =>
      change _ ++ later.sectors = _ ++ later.sectors
      exact congrArg (fun s => s ++ later.sectors) ih
  | rightContext earlier step ih =>
      change earlier.sectors ++ _ = earlier.sectors ++ _
      exact congrArg (fun s => earlier.sectors ++ s) ih

/-- Actual C60 physical E7A bracket erasure preserves the FULL
ordered source sector presentation through every F54-shaped
local rotation, rather than merely counting primitive rotations. -/
theorem KuuNativeF45Tree.LocalRotation.physical_leaves_eq
    {p : Polygon} {a b : D} {x y : E} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {before after : KuuNativeF45Tree p n m ma pa mb pb}
    (step : KuuNativeF45Tree.LocalRotation p before after) :
    before.erasePhysical.erase.leaves =
      after.erasePhysical.erase.leaves := by
  calc
    before.erasePhysical.erase.leaves = before.sectors :=
      before.erasePhysical_leaves
    _ = after.sectors := step.sectors_eq
    _ = after.erasePhysical.erase.leaves :=
      after.erasePhysical_leaves.symm

/-- Both primitive histories still have the exact originally typed
F19/F28-shaped Blocks endpoints and independent depths after ANY
root/contextual rotation. No equality of raw within-axis witnesses
or unsupported old F44 quotient has been assumed. -/
theorem KuuNativeF45Tree.LocalRotation.both_axes_flatten
    {p : Polygon} {a b : D} {x y : E} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {before after : KuuNativeF45Tree p n m ma pa mb pb}
    (_step : KuuNativeF45Tree.LocalRotation p before after) :
    ma.flatten = mb.flatten ∧ pa.flatten = pb.flatten :=
  before.axis_flatten_preserved

/-- Three actual consecutive C60 north-pentagon sector-bearing
stages, retaining separate original categorical axis subdivisions. -/
def northNativeF45FirstThrice :=
  KuuNativeBlocks.snoc northNativeF45FirstTwice
    (KuuNativePath.nil (Site.face (.pentagon .north)))

def northNativeF45SecondThrice :=
  KuuNativeBlocks.snoc northNativeF45SecondTwice
    (KuuNativePath.nil (Site.face (.pentagon .north)))

def northNativeF45ThirdStage :
    KuuNativeF45Tree (.pentagon .north) 1 1
      northNativeF45FirstTwice northNativeF45SecondTwice
      northNativeF45FirstThrice northNativeF45SecondThrice :=
  .leaf (firstFourPolygonSector (.pentagon .north) 2)
    .firstAxisFirst
    (KuuNativeAxisTrace.insertNilOnce _)
    (KuuNativeAxisTrace.insertNilOnce _)

/-- A concrete ORIGINAL-SHAPED, correctly dependent NATIVE F54
root associator using three successive true C60 sectors (0,1,2),
each carrying both real native categorical path/Blocks histories. -/
def northNativeF45TripleRotation :
    KuuNativeF45Tree.LocalRotation (.pentagon .north)
      (KuuNativeF45Tree.castDepths
        (Nat.add_assoc 1 1 1) (Nat.add_assoc 1 1 1)
        (KuuNativeF45Tree.node
          (KuuNativeF45Tree.node
            northNativeF45FirstStage northNativeF45SecondStage)
          northNativeF45ThirdStage))
      (KuuNativeF45Tree.node northNativeF45FirstStage
        (KuuNativeF45Tree.node
          northNativeF45SecondStage northNativeF45ThirdStage)) :=
  .assoc northNativeF45FirstStage northNativeF45SecondStage
    northNativeF45ThirdStage

/-- The real north C60 three-sector bracket rotation preserves the
entire exact physical sector source, not merely its length. -/
theorem northNativeF45TripleRotation_sector_sound :
    (KuuNativeF45Tree.castDepths
        (Nat.add_assoc 1 1 1) (Nat.add_assoc 1 1 1)
        (KuuNativeF45Tree.node
          (KuuNativeF45Tree.node
            northNativeF45FirstStage northNativeF45SecondStage)
          northNativeF45ThirdStage)).sectors =
      (KuuNativeF45Tree.node northNativeF45FirstStage
        (KuuNativeF45Tree.node
          northNativeF45SecondStage northNativeF45ThirdStage)).sectors :=
  northNativeF45TripleRotation.sectors_eq

#print axioms KuuNativeF45Tree.castDepths
#print axioms KuuNativeF45Tree.sectors_castDepths
#print axioms KuuNativeF45Tree.erasePhysical_castDepths
#print axioms KuuNativeF45Tree.LocalRotation
#print axioms KuuNativeF45Tree.LocalRotation.sectors_eq
#print axioms KuuNativeF45Tree.LocalRotation.physical_leaves_eq
#print axioms KuuNativeF45Tree.LocalRotation.both_axes_flatten
#print axioms northNativeF45TripleRotation
#print axioms northNativeF45TripleRotation_sector_sound
end
end Kuu.F112.Physical
