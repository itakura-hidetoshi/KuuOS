import Kuu.F112.PolygonNativeF55P94DK5PeifferInterchangeEnvelope
import Mathlib.Tactic

/-!
# F112-P94D3E — actual six-sector C60 P/S and S/N interchange four-cells

The three P94C3 free-group letters P (original F55 four-stage
pentagon), S (original F55 disjoint-context square), and N (new P92B
associator naturality) need not commute BEFORE a four-cell quotient.

P94D3B/C exhibited an ACTUAL C60 north pentagon P/N interchange
4-cell and imposed only its ONE normal relator, retaining P/S
noncommutativity in that deliberately smaller algebraic quotient.

This module proves a strictly stronger ORIGINAL-SOURCE fact:
on one and the SAME genuine top C60 hexagon polygon, its six
physically different F45 sector units carry:
* the original four-stage F55 pentagon generator P,
* the original six-sector F55 disjoint square generator S, and
* the P92B associator naturality generator N.

Because these six units share the true original F19/F28 Blocks
endpoints, all three source 3-proofs can be paired in genuinely
well-typed P94A horizontal interchange four-cells.

Consequently, the free-group P/S and S/N commutators are ALSO
forced by actual Type-valued P94A and P94C2 comparisons. This
DOES NOT claim a single directly composable four-cell between
the NORTH PENTAGON source and the HEXAGON square source: their
Polygon types differ. It instead proves that the coarse global
P94C3 letter P also occurs in the genuine hexagon context.

We build the normal closure of these THREE genuinely witnessed
pairwise commutators, a sharper proven lower bound on the
four-cell-induced normal kernel. It strictly contains P94D3C's
single P/N relation. Full signed/odd F55 shadow still descends.
The global K5 spherical 3-pasting and independent four-dimensional
pentagonator are NOT asserted. No Gray, sorry, admit or new axioms.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

/-- Four actual top-hexagon F45 sector units, each retaining its
distinct C60 geometric sector but the same exact dual-axis Blocks. -/
def northHexagonOriginalPentagonPSource :=
  nativeF55P94CPentagonThreeCell
    (northHexagonNativeUnit 0)
    (northHexagonNativeUnit 1)
    (northHexagonNativeUnit 2)
    (northHexagonNativeUnit 3)

/-- The unmodified true six-sector disjoint F55 square source. -/
def northHexagonOriginalSquareSSource :=
  NativeF55P92AssocComparison.original northHexagonNativeF55SquareCell

/-- A true P92B naturality constructor on five distinct
top-hexagon sector units; this is not a historical F55 cell. -/
def northHexagonOriginalNaturalityNSource :=
  nativeK5NaturalitySquare0
    (northHexagonNativeUnit 0)
    (northHexagonNativeUnit 1)
    (northHexagonNativeUnit 2)
    (northHexagonNativeUnit 3)
    (northHexagonNativeUnit 4)

theorem northHexagonOriginalPentagonPSource_groupWord :
    northHexagonOriginalPentagonPSource.p94cGroupWord =
      nativeK5PNPentagon := rfl

theorem northHexagonOriginalSquareSSource_groupWord :
    northHexagonOriginalSquareSSource.p94cGroupWord =
      nativeK5PNSquare := rfl

theorem northHexagonOriginalNaturalityNSource_groupWord :
    northHexagonOriginalNaturalityNSource.p94cGroupWord =
      nativeK5PNNaturality := rfl

/-- P/S exchange is witnessed by the actual EXISTING P94A 4-cell
at two simultaneously composable top-hexagon F45 contexts. -/
def northHexagonPSInterchange_actual_fourCell :
    NativeF55P94UnitFourCell
      (nativeK5InterchangeFirstPasting
        northHexagonOriginalPentagonPSource northHexagonOriginalSquareSSource)
      (nativeK5InterchangeSecondPasting
        northHexagonOriginalPentagonPSource northHexagonOriginalSquareSSource) :=
  nativeK5InterchangeFourCell
    northHexagonOriginalPentagonPSource northHexagonOriginalSquareSSource

/-- S/N is also a REAL interchange, not an independent
abstract commutator imposed as a fresh 4D axiom. -/
def northHexagonSNInterchange_actual_fourCell :
    NativeF55P94UnitFourCell
      (nativeK5InterchangeFirstPasting
        northHexagonOriginalSquareSSource northHexagonOriginalNaturalityNSource)
      (nativeK5InterchangeSecondPasting
        northHexagonOriginalSquareSSource northHexagonOriginalNaturalityNSource) :=
  nativeK5InterchangeFourCell
    northHexagonOriginalSquareSSource northHexagonOriginalNaturalityNSource

/-- The third P/N pair also has a witnessed interchange INSIDE
the same original top C60 hexagon context. -/
def northHexagonPNInterchange_actual_fourCell :
    NativeF55P94UnitFourCell
      (nativeK5InterchangeFirstPasting
        northHexagonOriginalPentagonPSource northHexagonOriginalNaturalityNSource)
      (nativeK5InterchangeSecondPasting
        northHexagonOriginalPentagonPSource northHexagonOriginalNaturalityNSource) :=
  nativeK5InterchangeFourCell
    northHexagonOriginalPentagonPSource northHexagonOriginalNaturalityNSource

def nativeK5PSInterchangeRelator : NativeF55P94CWord :=
  (nativeK5PNPentagon + nativeK5PNSquare) -
    (nativeK5PNSquare + nativeK5PNPentagon)

def nativeK5SNInterchangeRelator : NativeF55P94CWord :=
  (nativeK5PNSquare + nativeK5PNNaturality) -
    (nativeK5PNNaturality + nativeK5PNSquare)

/-- The exact coarse free-word defect of a REAL typed source P/S
4-cell equals the named noncommutative P/S commutator. -/
theorem northHexagonPSInterchange_actual_relator :
    (nativeK5InterchangeFirstPasting
        northHexagonOriginalPentagonPSource
        northHexagonOriginalSquareSSource).p94cGroupWord -
    (nativeK5InterchangeSecondPasting
        northHexagonOriginalPentagonPSource
        northHexagonOriginalSquareSSource).p94cGroupWord =
      nativeK5PSInterchangeRelator := by
  rw [nativeK5InterchangeFirstWord, nativeK5InterchangeSecondWord,
    northHexagonOriginalPentagonPSource_groupWord,
    northHexagonOriginalSquareSSource_groupWord]
  rfl

theorem northHexagonSNInterchange_actual_relator :
    (nativeK5InterchangeFirstPasting
        northHexagonOriginalSquareSSource
        northHexagonOriginalNaturalityNSource).p94cGroupWord -
    (nativeK5InterchangeSecondPasting
        northHexagonOriginalSquareSSource
        northHexagonOriginalNaturalityNSource).p94cGroupWord =
      nativeK5SNInterchangeRelator := by
  rw [nativeK5InterchangeFirstWord, nativeK5InterchangeSecondWord,
    northHexagonOriginalSquareSSource_groupWord,
    northHexagonOriginalNaturalityNSource_groupWord]
  rfl

/-- The genuine P/S source four-cell forces equality of classes
in the actual P94A Type-valued quotient (not from shadows). -/
theorem northHexagonPSInterchange_P94A_class_eq :
    nativeF55P94UnitFourClass _ _
      (nativeK5InterchangeFirstPasting
        northHexagonOriginalPentagonPSource northHexagonOriginalSquareSSource) =
    nativeF55P94UnitFourClass _ _
      (nativeK5InterchangeSecondPasting
        northHexagonOriginalPentagonPSource northHexagonOriginalSquareSSource) :=
  Quot.sound ⟨northHexagonPSInterchange_actual_fourCell⟩

theorem northHexagonSNInterchange_P94A_class_eq :
    nativeF55P94UnitFourClass _ _
      (nativeK5InterchangeFirstPasting
        northHexagonOriginalSquareSSource northHexagonOriginalNaturalityNSource) =
    nativeF55P94UnitFourClass _ _
      (nativeK5InterchangeSecondPasting
        northHexagonOriginalSquareSSource northHexagonOriginalNaturalityNSource) :=
  Quot.sound ⟨northHexagonSNInterchange_actual_fourCell⟩

/-- The independently completed P94C2 groupoid also contains
both original Type-valued P94A interchange witnesses. -/
theorem northHexagonPSInterchange_P94C2_class_eq :
    nativeF55P94GroupFourClass _ _
      (nativeK5InterchangeFirstPasting
        northHexagonOriginalPentagonPSource northHexagonOriginalSquareSSource) =
    nativeF55P94GroupFourClass _ _
      (nativeK5InterchangeSecondPasting
        northHexagonOriginalPentagonPSource northHexagonOriginalSquareSSource) :=
  Quot.sound ⟨NativeF55P94GroupFourCell.old
    northHexagonPSInterchange_actual_fourCell⟩

theorem northHexagonSNInterchange_P94C2_class_eq :
    nativeF55P94GroupFourClass _ _
      (nativeK5InterchangeFirstPasting
        northHexagonOriginalSquareSSource northHexagonOriginalNaturalityNSource) =
    nativeF55P94GroupFourClass _ _
      (nativeK5InterchangeSecondPasting
        northHexagonOriginalSquareSSource northHexagonOriginalNaturalityNSource) :=
  Quot.sound ⟨NativeF55P94GroupFourCell.old
    northHexagonSNInterchange_actual_fourCell⟩

/-- The P/S words are STILL distinct before quotient, although
an actual typed 4-cell identifies their pastings afterward. -/
theorem northHexagonPSInterchange_rawWord_ne :
    (nativeK5InterchangeFirstPasting
      northHexagonOriginalPentagonPSource
      northHexagonOriginalSquareSSource).p94cGroupWord ≠
    (nativeK5InterchangeSecondPasting
      northHexagonOriginalPentagonPSource
      northHexagonOriginalSquareSSource).p94cGroupWord := by
  rw [nativeK5InterchangeFirstWord, nativeK5InterchangeSecondWord,
    northHexagonOriginalPentagonPSource_groupWord,
    northHexagonOriginalSquareSSource_groupWord]
  exact nativeF55P94CWord_noncommuting_letters

/-- An independent finite S3 observer sends S=(01), N=(12), P=1,
demonstrating that the S/N source free words do not commute either. -/
def nativeK5SquareNaturalityS3 :
    NativeF55P94CWord →+ Additive (Equiv.Perm (Fin 3)) :=
  FreeAddGroup.lift (fun
    | .pentagon => 0
    | .square => Additive.ofMul (Equiv.swap (0 : Fin 3) (1 : Fin 3))
    | .assocNaturality => Additive.ofMul (Equiv.swap (1 : Fin 3) (2 : Fin 3)))

theorem nativeK5Word_square_naturality_noncommute :
    nativeK5PNSquare + nativeK5PNNaturality ≠
      nativeK5PNNaturality + nativeK5PNSquare := by
  intro h
  have hh := congrArg nativeK5SquareNaturalityS3 h
  simp only [map_add, nativeK5PNSquare, nativeK5PNNaturality,
    FreeAddGroup.lift_apply_of] at hh
  change
    Equiv.swap (0 : Fin 3) (1 : Fin 3) *
      Equiv.swap (1 : Fin 3) (2 : Fin 3) =
    Equiv.swap (1 : Fin 3) (2 : Fin 3) *
      Equiv.swap (0 : Fin 3) (1 : Fin 3) at hh
  exact (by decide :
    Equiv.swap (0 : Fin 3) (1 : Fin 3) *
      Equiv.swap (1 : Fin 3) (2 : Fin 3) ≠
    Equiv.swap (1 : Fin 3) (2 : Fin 3) *
      Equiv.swap (0 : Fin 3) (1 : Fin 3)) hh

theorem northHexagonSNInterchange_rawWord_ne :
    (nativeK5InterchangeFirstPasting
      northHexagonOriginalSquareSSource
      northHexagonOriginalNaturalityNSource).p94cGroupWord ≠
    (nativeK5InterchangeSecondPasting
      northHexagonOriginalSquareSSource
      northHexagonOriginalNaturalityNSource).p94cGroupWord := by
  rw [nativeK5InterchangeFirstWord, nativeK5InterchangeSecondWord,
    northHexagonOriginalSquareSSource_groupWord,
    northHexagonOriginalNaturalityNSource_groupWord]
  exact nativeK5Word_square_naturality_noncommute

/-- ONLY the three PAIRWISE COMMUTATORS now backed by genuine typed
P94A C60 source four-cells are imposed, not all arbitrary group
commutators or hypothetical higher coherence generators. -/
def nativeK5ThreePhysicalPairRelators : Set NativeF55P94CWord :=
  {nativeK5PNInterchangeRelator,
   nativeK5PSInterchangeRelator,
   nativeK5SNInterchangeRelator}

def nativeK5ThreePhysicalPairClosure : AddSubgroup NativeF55P94CWord :=
  AddSubgroup.normalClosure nativeK5ThreePhysicalPairRelators

instance nativeK5ThreePhysicalPairClosure_normal :
    nativeK5ThreePhysicalPairClosure.Normal := by
  unfold nativeK5ThreePhysicalPairClosure
  infer_instance

theorem nativeK5ThreePhysicalPair_PN_mem :
    nativeK5PNInterchangeRelator ∈ nativeK5ThreePhysicalPairClosure := by
  apply AddSubgroup.subset_normalClosure
  simp [nativeK5ThreePhysicalPairRelators]

theorem nativeK5ThreePhysicalPair_PS_mem :
    nativeK5PSInterchangeRelator ∈ nativeK5ThreePhysicalPairClosure := by
  apply AddSubgroup.subset_normalClosure
  simp [nativeK5ThreePhysicalPairRelators]

theorem nativeK5ThreePhysicalPair_SN_mem :
    nativeK5SNInterchangeRelator ∈ nativeK5ThreePhysicalPairClosure := by
  apply AddSubgroup.subset_normalClosure
  simp [nativeK5ThreePhysicalPairRelators]

abbrev NativeK5ThreePhysicalPairWord :=
  NativeF55P94CWord ⧸ nativeK5ThreePhysicalPairClosure

def nativeK5ThreePhysicalPairClass :
    NativeF55P94CWord →+ NativeK5ThreePhysicalPairWord :=
  QuotientAddGroup.mk' nativeK5ThreePhysicalPairClosure

theorem nativeK5ThreePhysicalPair_PN_commute :
    nativeK5ThreePhysicalPairClass
      (nativeK5PNPentagon + nativeK5PNNaturality) =
    nativeK5ThreePhysicalPairClass
      (nativeK5PNNaturality + nativeK5PNPentagon) :=
  (QuotientAddGroup.eq_iff_sub_mem).2 nativeK5ThreePhysicalPair_PN_mem

theorem nativeK5ThreePhysicalPair_PS_commute :
    nativeK5ThreePhysicalPairClass
      (nativeK5PNPentagon + nativeK5PNSquare) =
    nativeK5ThreePhysicalPairClass
      (nativeK5PNSquare + nativeK5PNPentagon) :=
  (QuotientAddGroup.eq_iff_sub_mem).2 nativeK5ThreePhysicalPair_PS_mem

theorem nativeK5ThreePhysicalPair_SN_commute :
    nativeK5ThreePhysicalPairClass
      (nativeK5PNSquare + nativeK5PNNaturality) =
    nativeK5ThreePhysicalPairClass
      (nativeK5PNNaturality + nativeK5PNSquare) :=
  (QuotientAddGroup.eq_iff_sub_mem).2 nativeK5ThreePhysicalPair_SN_mem

/-- P94D3C is strictly weaker as a normal-relation presentation:
P/S did not commute there, but does after adding the actual
top-hexagon four-cell witnessed in THIS module. -/
theorem nativeK5PNNormalClosure_le_threePhysicalPair :
    nativeK5PNNormalClosure ≤ nativeK5ThreePhysicalPairClosure := by
  apply AddSubgroup.normalClosure_le_normal
  intro w hw
  have heq : w = nativeK5PNInterchangeRelator := by
    simpa [nativeK5PNRelators] using hw
  subst w
  exact nativeK5ThreePhysicalPair_PN_mem

theorem nativeK5PNNormalClosure_ne_threePhysicalPair :
    nativeK5PNNormalClosure ≠ nativeK5ThreePhysicalPairClosure := by
  intro h
  have hps : nativeK5PSInterchangeRelator ∈ nativeK5PNNormalClosure := by
    rw [h]
    exact nativeK5ThreePhysicalPair_PS_mem
  have heq :
      nativeK5PNCorrectedClass (nativeK5PNPentagon + nativeK5PNSquare) =
        nativeK5PNCorrectedClass (nativeK5PNSquare + nativeK5PNPentagon) :=
    (QuotientAddGroup.eq_iff_sub_mem).2 hps
  exact nativeK5PNCorrected_pentagon_square_noncommute heq

/-- The complete signed original F55 shadow also survives the
strictly stronger physical THREE-pair normal relation. -/
theorem nativeK5ThreePhysicalPairClosure_le_shadow_ker :
    nativeK5ThreePhysicalPairClosure ≤ nativeF55P94CWordToShadow.ker := by
  apply AddSubgroup.normalClosure_le_normal
  intro w hw
  simp only [nativeK5ThreePhysicalPairRelators,
    Set.mem_insert_iff, Set.mem_singleton_iff] at hw
  rcases hw with h | h | h
  · rw [h]
    exact nativeK5PNInterchangeRelator_shadow_zero
  · rw [h]
    change nativeF55P94CWordToShadow nativeK5PSInterchangeRelator = 0
    simp only [nativeK5PSInterchangeRelator, map_sub, map_add]
    abel
  · rw [h]
    change nativeF55P94CWordToShadow nativeK5SNInterchangeRelator = 0
    simp only [nativeK5SNInterchangeRelator, map_sub, map_add]
    abel

def nativeK5ThreePhysicalPairShadow :
    NativeK5ThreePhysicalPairWord →+ KuuNativeF55Shadow :=
  QuotientAddGroup.lift nativeK5ThreePhysicalPairClosure
    nativeF55P94CWordToShadow
    nativeK5ThreePhysicalPairClosure_le_shadow_ker

theorem nativeK5ThreePhysicalPairShadow_spec (w : NativeF55P94CWord) :
    nativeK5ThreePhysicalPairShadow (nativeK5ThreePhysicalPairClass w) =
      nativeF55P94CWordToShadow w :=
  QuotientAddGroup.lift_mk' nativeK5ThreePhysicalPairClosure
    nativeK5ThreePhysicalPairClosure_le_shadow_ker w

#print axioms northHexagonOriginalPentagonPSource
#print axioms northHexagonOriginalSquareSSource
#print axioms northHexagonOriginalNaturalityNSource
#print axioms northHexagonPSInterchange_actual_fourCell
#print axioms northHexagonSNInterchange_actual_fourCell
#print axioms northHexagonPNInterchange_actual_fourCell
#print axioms northHexagonPSInterchange_actual_relator
#print axioms northHexagonSNInterchange_actual_relator
#print axioms northHexagonPSInterchange_P94A_class_eq
#print axioms northHexagonSNInterchange_P94A_class_eq
#print axioms northHexagonPSInterchange_P94C2_class_eq
#print axioms northHexagonSNInterchange_P94C2_class_eq
#print axioms northHexagonPSInterchange_rawWord_ne
#print axioms nativeK5Word_square_naturality_noncommute
#print axioms northHexagonSNInterchange_rawWord_ne
#print axioms nativeK5ThreePhysicalPair_PN_commute
#print axioms nativeK5ThreePhysicalPair_PS_commute
#print axioms nativeK5ThreePhysicalPair_SN_commute
#print axioms nativeK5PNNormalClosure_le_threePhysicalPair
#print axioms nativeK5PNNormalClosure_ne_threePhysicalPair
#print axioms nativeK5ThreePhysicalPairClosure_le_shadow_ker
#print axioms nativeK5ThreePhysicalPairShadow_spec

end
end Kuu.F112.Physical
