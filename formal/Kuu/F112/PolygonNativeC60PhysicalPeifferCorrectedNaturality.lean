import Kuu.F112.PolygonNativeC60ParallelTwoFrameWhiskering

/-!
# F112-P94D3BM — physical Peiffer-corrected naturality for every 15D witness

BL constructs ordered two-frame transport for the original physical exchange.
Here the carrier is enlarged to EVERY actual source-dependent AQ 15D witness,
without introducing a new geometric generator.

The AU 15D naturality paths have the original Peiffer 15D correctors
inserted at source and target, and BC gives a typed 16D comparison
between the two genuinely PARALLEL paths in its explicitly extended
presentation. We construct arbitrary two-frame RAW and STRICT transports,
an explicit nonabelian Peiffer gauge formula, and a genuine strict
isomorphism for each corrected pair.

In sharp contrast, the uncorrected interchange of the two frame
orders has equal LOWER AQ quotient classes and equal history words
but unequal original RAW 14D boundaries. It therefore has no 16D
comparison and no strict morphism for ANY AX signature and ANY chosen
parallel Kuu replacement quotient.

A binary BB whiskering of arbitrary 16D morphisms, BG singleton gates,
original geometric 16D filler, or P92B descent is NOT inferred.
No new axioms, sorry, admit, or Gray categories.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uD vD uE vE

section OriginalC60

variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {p : Polygon} {a b : D} {x y : E} {n n' m m' : Nat}
variable {ma mb : KuuNativeBlocks a b} {pa pb : KuuNativeBlocks x y}
variable {first : KuuNativeF45Tree p n m ma pa mb pb}
variable {last : KuuNativeF45Tree p n' m' ma pa mb pb}
variable {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
variable {f g : NativeF55StructuralComparison p r s}
variable {alpha beta : NativeK5StructuralFourCell p f g}
variable {w z : NativeK5StructuralFiveCell p alpha beta}
variable {u v : NativeK5StructuralSixCell p w z}
variable {h k : NativeK5StructuralSevenCell p u v}
variable {e d : NativeK5StructuralEightCell p h k}
variable {q t : NativeK5StructuralNineCell p e d}
variable {P Q : NativeK5StructuralTenCell p q t}
variable {H K : NativeK5StructuralElevenCell p P Q}
variable {U V : NativeK5StructuralTwelveCell p H K}

/-- Any ACTUAL AQ 15D witness gives TWO 15D naturality routes whose
common original 14D boundary is witnessed by a BC-declared 16D step.
The source and target Peiffer correctors are genuine 15D terms. -/
def nativeK5BMParallelSeed
    (W : NativeK5StructuralThirteenCell p U V)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S) :
    NativeC60BGRawArrowBundle
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W) :=
  ⟨(nativeK5AXPack W (nativeK5AUNaturalityViaSource W cell),
      nativeK5AXPack W (nativeK5AUNaturalityViaTarget W cell)),
    nativeK5BCContextualNaturality W [] cell⟩

/-- Two independent ORDERED physical finite frames act on this entire
original-boundary-dependent 16D comparison, not just an observer. -/
def nativeK5BMTwoFrame
    (W : NativeK5StructuralThirteenCell p U V)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S)
    (outer inner : List Bool) :
    NativeC60BGRawArrowBundle
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W) :=
  nativeC60BGRawContext
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
    (outer ++ inner) (nativeK5BMParallelSeed W cell)

/-- Raw two-frame action composes on the WHOLE dependent 16D bundle,
for every original physical 15D witness. -/
theorem nativeK5BMTwoFrame_stages
    (W : NativeK5StructuralThirteenCell p U V)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S)
    (outer inner : List Bool) :
    nativeK5BMTwoFrame W cell outer inner =
      nativeC60BGRawContext
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W) outer
        (nativeC60BGRawContext
          (nativeK5AXKuuSignature W) (nativeK5BCFrame W) inner
          (nativeK5BMParallelSeed W cell)) :=
  nativeC60BGRawContext_append
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
    outer inner (nativeK5BMParallelSeed W cell)

/-- Corrected AU routes have EXACTLY parallel original 14D boundaries
after arbitrary independent physical context words. -/
theorem nativeK5BMTwoFrame_parallel
    (W : NativeK5StructuralThirteenCell p U V)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S)
    (outer inner : List Bool) :
    (nativeK5BMTwoFrame W cell outer inner).1.1.1 =
      (nativeK5BMTwoFrame W cell outer inner).1.2.1 :=
  (nativeK5BMTwoFrame W cell outer inner).2.boundary

/-- The selected higher comparison respects ACTUAL noncommutative
Peiffer values without equating its raw original 15D endpoints. -/
theorem nativeK5BMTwoFrame_peiffer
    (W : NativeK5StructuralThirteenCell p U V)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S)
    (outer inner : List Bool) :
    nativeK5AXPeiffer W (nativeK5BMTwoFrame W cell outer inner).1.1 =
      nativeK5AXPeiffer W (nativeK5BMTwoFrame W cell outer inner).1.2 :=
  (nativeK5BMTwoFrame W cell outer inner).2.observer_sound
    (nativeK5AXPeiffer W) (nativeK5BCSignature_peiffer W)

/-- Exact NONABELIAN source defect: the original right-frame Peiffer
conjugation occurs first; then the ordered finite-frame gauge action.
No abelianization or replacement of physical history by a scalar. -/
theorem nativeK5BMTwoFrame_source_formula
    (W : NativeK5StructuralThirteenCell p U V)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S)
    (outer inner : List Bool) :
    nativeK5AXPeiffer W (nativeK5BMTwoFrame W cell outer inner).1.1 =
      nativeK5ASPeifferAct W (nativeK5ATGaugeWord W (outer ++ inner))
        (nativeK5ASPeifferAct W (nativeK5AQRightFrame W).historyWord⁻¹
          (nativeK5ATCellDefect W cell)) := by
  change nativeK5AXPeiffer W
    (nativeK5BCContext W (outer ++ inner)
      (nativeK5AXPack W (nativeK5AUNaturalityViaSource W cell))) = _
  calc
    _ = nativeK5ASPeifferAct W (nativeK5ATGaugeWord W (outer ++ inner))
          (nativeK5AXPeiffer W
            (nativeK5AXPack W (nativeK5AUNaturalityViaSource W cell))) :=
      nativeK5BCContext_peiffer W (outer ++ inner) _
    _ = _ := congrArg
      (nativeK5ASPeifferAct W (nativeK5ATGaugeWord W (outer ++ inner)))
      (nativeK5AUNaturality_defect_peiffer W cell)

/-- The TARGET route has the IDENTICAL physical noncommutative defect
by the actual AU naturality identity, not by forcing raw proof equality. -/
theorem nativeK5BMTwoFrame_target_formula
    (W : NativeK5StructuralThirteenCell p U V)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S)
    (outer inner : List Bool) :
    nativeK5AXPeiffer W (nativeK5BMTwoFrame W cell outer inner).1.2 =
      nativeK5ASPeifferAct W (nativeK5ATGaugeWord W (outer ++ inner))
        (nativeK5ASPeifferAct W (nativeK5AQRightFrame W).historyWord⁻¹
          (nativeK5ATCellDefect W cell)) := by
  change nativeK5AXPeiffer W
    (nativeK5BCContext W (outer ++ inner)
      (nativeK5AXPack W (nativeK5AUNaturalityViaTarget W cell))) = _
  calc
    _ = nativeK5ASPeifferAct W (nativeK5ATGaugeWord W (outer ++ inner))
          (nativeK5AXPeiffer W
            (nativeK5AXPack W (nativeK5AUNaturalityViaTarget W cell))) :=
      nativeK5BCContext_peiffer W (outer ++ inner) _
    _ = _ := congrArg
      (nativeK5ASPeifferAct W (nativeK5ATGaugeWord W (outer ++ inner)))
      ((nativeK5AUNaturality_defect_eq W cell).symm.trans
        (nativeK5AUNaturality_defect_peiffer W cell))

/-- The corrected 15D pair becomes ISOMORPHIC as distinct objects in
the already chosen STRICT Kuu category for the BC presentation.
This is not a claim of an original geometric 16-cell. -/
def nativeK5BMCorrectedStrictIso
    (W : NativeK5StructuralThirteenCell p U V)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S)
    (outer inner : List Bool) :
    (nativeC60AZStrictProject (nativeK5BCSignature W)
      (nativeC60AZNoRelations (nativeK5BCSignature W))).obj
        ⟨(nativeK5BMTwoFrame W cell outer inner).1.1⟩ ≅
    (nativeC60AZStrictProject (nativeK5BCSignature W)
      (nativeC60AZNoRelations (nativeK5BCSignature W))).obj
        ⟨(nativeK5BMTwoFrame W cell outer inner).1.2⟩ where
  hom := nativeC60AZStrictStep (nativeK5BCSignature W)
    (nativeC60AZNoRelations (nativeK5BCSignature W))
    (nativeK5BMTwoFrame W cell outer inner).2
  inv := nativeC60AZStrictStep (nativeK5BCSignature W)
    (nativeC60AZNoRelations (nativeK5BCSignature W))
    (.symm (nativeK5BMTwoFrame W cell outer inner).2)
  hom_inv_id := nativeC60AZStrictStep_inv_left
    (nativeK5BCSignature W) (nativeC60AZNoRelations (nativeK5BCSignature W))
    (nativeK5BMTwoFrame W cell outer inner).2
  inv_hom_id := nativeC60AZStrictStep_inv_right
    (nativeK5BCSignature W) (nativeC60AZNoRelations (nativeK5BCSignature W))
    (nativeK5BMTwoFrame W cell outer inner).2

/-- Strict Kuu transport on ALL arrows (not just AX raw generators)
also factors as two ordered context parameters for EVERY corrected AU
naturality square. -/
def nativeK5BMStrictSeed
    (W : NativeK5StructuralThirteenCell p U V)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S) :
    NativeC60BEStrictArrowBundle
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W) :=
  ⟨(nativeK5BMParallelSeed W cell).1,
    nativeC60AZStrictStep (nativeK5BCSignature W)
      (nativeC60AZNoRelations (nativeK5BCSignature W))
      (nativeK5BMParallelSeed W cell).2⟩

def nativeK5BMStrictTwoFrame
    (W : NativeK5StructuralThirteenCell p U V)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S)
    (outer inner : List Bool) :
    NativeC60BEStrictArrowBundle
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W) :=
  nativeK5BEPhysicalArrowContext W (outer ++ inner)
    (nativeK5BMStrictSeed W cell)

theorem nativeK5BMStrictTwoFrame_stages
    (W : NativeK5StructuralThirteenCell p U V)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S)
    (outer inner : List Bool) :
    nativeK5BMStrictTwoFrame W cell outer inner =
      nativeK5BEPhysicalArrowContext W outer
        (nativeK5BEPhysicalArrowContext W inner
          (nativeK5BMStrictSeed W cell)) :=
  nativeK5BEPhysicalArrowContext_append W outer inner
    (nativeK5BMStrictSeed W cell)

/-- The original AQ lower quotient IDENTIFIES each pair of
frame-reordered original 14D boundary terms through the actual
15D conservative Peiffer cell. These are NOT raw 14D equalities. -/
theorem nativeK5BMUncorrected_lower_classes
    (W : NativeK5StructuralThirteenCell p U V)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S) :
    nativeK5AQClass W
        (nativeK5AQWhiskerLeft W (nativeK5AQWhiskerRight W R)) =
      nativeK5AQClass W
        (nativeK5AQWhiskerRight W (nativeK5AQWhiskerLeft W R)) ∧
    nativeK5AQClass W
        (nativeK5AQWhiskerLeft W (nativeK5AQWhiskerRight W S)) =
      nativeK5AQClass W
        (nativeK5AQWhiskerRight W (nativeK5AQWhiskerLeft W S)) := by
  exact ⟨Quotient.sound ⟨nativeK5AQPeifferCell W R⟩,
    Quotient.sound ⟨nativeK5AQPeifferCell W S⟩⟩

/-- Both original 14D endpoints have MATCHING group history under the
two orders, despite their different raw construction trees. -/
theorem nativeK5BMUncorrected_history_equal
    (W : NativeK5StructuralThirteenCell p U V)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S) :
    (nativeK5AQWhiskerLeft W
        (nativeK5AQWhiskerRight W R)).historyWord =
      (nativeK5AQWhiskerRight W
        (nativeK5AQWhiskerLeft W R)).historyWord ∧
    (nativeK5AQWhiskerLeft W
        (nativeK5AQWhiskerRight W S)).historyWord =
      (nativeK5AQWhiskerRight W
        (nativeK5AQWhiskerLeft W S)).historyWord :=
  ⟨nativeK5BLPhysicalFrames_history_eq W R,
    nativeK5BLPhysicalFrames_history_eq W S⟩

/-- There is nevertheless NO strict morphism between the two
UNCORRECTED, nonparallel 15D terms in ANY AX signature and ANY
selected parallel Kuu quotient, by BA's full arrow surjectivity. -/
theorem nativeK5BMUncorrected_no_strict_morphism
    (W : NativeK5StructuralThirteenCell p U V)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S)
    (T : NativeC60AXSignature (nativeK5AXBaseLayer W))
    (P : NativeC60AZParallelRelation T) :
    ¬ Nonempty
      ((nativeC60AZStrictProject T P).obj
          ⟨nativeK5BLMixedLeftRight W cell⟩ ⟶
        (nativeC60AZStrictProject T P).obj
          ⟨nativeK5BLMixedRightLeft W cell⟩) := by
  rintro ⟨arrow⟩
  obtain ⟨comparison, _⟩ := nativeC60BAStep_surjective T P
    (nativeK5BLMixedLeftRight W cell)
    (nativeK5BLMixedRightLeft W cell) arrow
  exact (nativeK5BLMixed_no_sixteen W cell T) ⟨comparison⟩

/-- In particular no quotient can produce a strict iso that forgets
the ORIGINAL 14D source/target boundary mismatch. -/
theorem nativeK5BMUncorrected_no_strict_iso
    (W : NativeK5StructuralThirteenCell p U V)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S)
    (T : NativeC60AXSignature (nativeK5AXBaseLayer W))
    (P : NativeC60AZParallelRelation T) :
    ¬ Nonempty
      ((nativeC60AZStrictProject T P).obj
          ⟨nativeK5BLMixedLeftRight W cell⟩ ≅
        (nativeC60AZStrictProject T P).obj
          ⟨nativeK5BLMixedRightLeft W cell⟩) := by
  rintro ⟨i⟩
  exact nativeK5BMUncorrected_no_strict_morphism W cell T P ⟨i.hom⟩

/-- Structural positive/negative contrast at an arbitrary genuine
original physical 15D witness: PEIFFER-CORRECTED parallel evidence
admits an actual chosen-presentation strict isomorphism, while the
naive swap is absent for EVERY possible higher signature. -/
theorem nativeK5BMCorrected_vs_uncorrected
    (W : NativeK5StructuralThirteenCell p U V)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S)
    (outer inner : List Bool) :
    Nonempty
      ((nativeC60AZStrictProject (nativeK5BCSignature W)
        (nativeC60AZNoRelations (nativeK5BCSignature W))).obj
          ⟨(nativeK5BMTwoFrame W cell outer inner).1.1⟩ ≅
       (nativeC60AZStrictProject (nativeK5BCSignature W)
        (nativeC60AZNoRelations (nativeK5BCSignature W))).obj
          ⟨(nativeK5BMTwoFrame W cell outer inner).1.2⟩) ∧
    (∀ (T : NativeC60AXSignature (nativeK5AXBaseLayer W))
       (P : NativeC60AZParallelRelation T),
       ¬ Nonempty
         ((nativeC60AZStrictProject T P).obj
             ⟨nativeK5BLMixedLeftRight W cell⟩ ⟶
           (nativeC60AZStrictProject T P).obj
             ⟨nativeK5BLMixedRightLeft W cell⟩)) :=
  ⟨⟨nativeK5BMCorrectedStrictIso W cell outer inner⟩,
    fun T P => nativeK5BMUncorrected_no_strict_morphism W cell T P⟩

end OriginalC60

#print axioms nativeK5BMParallelSeed
#print axioms nativeK5BMTwoFrame
#print axioms nativeK5BMTwoFrame_stages
#print axioms nativeK5BMTwoFrame_parallel
#print axioms nativeK5BMTwoFrame_peiffer
#print axioms nativeK5BMTwoFrame_source_formula
#print axioms nativeK5BMTwoFrame_target_formula
#print axioms nativeK5BMCorrectedStrictIso
#print axioms nativeK5BMStrictSeed
#print axioms nativeK5BMStrictTwoFrame
#print axioms nativeK5BMStrictTwoFrame_stages
#print axioms nativeK5BMUncorrected_lower_classes
#print axioms nativeK5BMUncorrected_history_equal
#print axioms nativeK5BMUncorrected_no_strict_morphism
#print axioms nativeK5BMUncorrected_no_strict_iso
#print axioms nativeK5BMCorrected_vs_uncorrected

end
end Kuu.F112.Physical
