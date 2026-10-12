import KUOS.DependentOriginationGrayC60IntegerSquarePeriodV5_186

namespace KUOS.DependentOriginationGrayC60AtomicSourceRigidityV5_187

open CategoryTheory
open KUOS.DependentOriginationIcosahedralTruncationSeedV3_84
open KUOS.DependentOriginationTruncatedIcosahedralEdgesV3_85
open KUOS.DependentOriginationGrayBraidedThreeCellCoreV5_156
open KUOS.DependentOriginationGrayF55PhaseRealizationV5_156
open KUOS.DependentOriginationGrayC60CyclicGlobalPastingV5_156
open KUOS.DependentOriginationGrayC60IntegralBoundaryLinearMapV5_159
open KUOS.DependentOriginationGrayC60IntegralChainComplexV5_160
open KUOS.DependentOriginationGrayC60CochainDescentV5_166
open KUOS.DependentOriginationGrayC60F55SharpRepairV5_168
open KUOS.DependentOriginationGrayC60F55SourcePhaseLockedAtlasV5_175
open KUOS.DependentOriginationGrayC60WangBiGlobalGrayDescentV5_174
open KUOS.DependentOriginationGrayC60SquareLoopCosetV5_185
open KUOS.DependentOriginationGrayC60FullF55ChargeObstructionV5_184
open KUOS.DependentOriginationGrayC60IntegerSquarePeriodV5_186
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

set_option autoImplicit false
set_option maxRecDepth 4096
set_option maxHeartbeats 4000000
noncomputable section

/-!
# F59-F39 / v5.187 — exact numerical period ZERO on original atomic F54 routes

F59-F38 constructed the source-loop integer period d_r for ALL
original freely generated, proof-relevant F55 PresentedCells and
proved d_r ∈ H_r. Here we determine its ACTUAL numerical value
on a fundamental ORIGINAL source-route class, not an abstract
approximation or an arbitrary assumed constant.

The original F54 DepthRotationRoute has two atomic constructors:
  • genuine Type-valued RotationChain, including a real local rotation;
  • ORIGINAL F19/F28 two-axis dependent-depth castDepths.
All nontrivial original F55 generators have composite / contextual
route boundaries. We prove on ALL NINE original PresentedCell
constructors that an atomic source route CANNOT be connected to a
composite route; even arbitrary inverse, vertical pasting, and
four whiskerings cannot escape the atomic route component.
The square charge of any such original source witness is ZERO,
and its pentagon charge is ZERO on original loops.

Consequently the ACTUAL full-nine-source square loop subgroup at
every original bare chain or cast is {0}; therefore the canonical
nonnegative INTEGER period is exactly d_r=0. Further, ANY original
source 3-cell from an atomic route to itself interprets to the
identity native neutral Gray coefficient. This is a genuine
Type-indexed original source rigidity, not a quotient equality
of distinct raw original PresentedCells.

On the ORIGINAL physical C60, the previously proved flat 27-edge
F55 repair keeps the REAL north-spoke 0 cross edge labelled by the
nonzero original F55 square generator (charge (0,1), phase 1).
This gives a concrete globally 32-face FLAT, all-90-edge
PHASE-COMPATIBLE atlas that cannot lift to original full-nine F55
PresentedCells when the source is an uncomposed bare F54 route.
The incompatibility lies in SOURCE typing and square charge, not
in the target flatness or Gray braid phase.

The numerical period for the COMPOSITE original F54 disjoint-square
left-first/right-first routes remains separate; this theorem
does not silently generalize atomic rigidity to those routes.
No Stage-II omega or historical Wang Bi meaning is inferred.
-/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

section OriginalSourceAtomic
variable {a b : D} {x y : E}
variable {n n' m m' : Nat}
variable {ma mb : Blocks a b} {pa pb : Blocks x y}
variable {first : OriginalF45BracketTree n m ma pa mb pb}
variable {last : OriginalF45BracketTree n' m' ma pa mb pb}
variable {r s : OriginalF45BracketTree.DepthRotationRoute first last}

/-- The two EXACT ORIGINAL F54 atomic route constructors: a
real RotationChain or a double-depth cast. All other constructors
are composite or contextual, and are NOT silently flattened. -/
def c60F39IsAtomicOriginalRoute
    {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    {first : OriginalF45BracketTree n m ma pa mb pb}
    {last : OriginalF45BracketTree n' m' ma pa mb pb}
    (route : OriginalF45BracketTree.DepthRotationRoute first last) : Bool :=
  match route with
  | .chain _ => true
  | .castDepths _ _ _ => true
  | _ => false

/-- INDUCTION OVER ALL NINE original F55 constructors. Neither
pentagon nor square has an atomic route boundary, and no contextual
whiskering creates such a boundary. Identity, reversal and vertical
pasting preserve the Boolean component indicator. -/
theorem c60F39AtomicRoute_preserved
    (cell : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r s) :
    c60F39IsAtomicOriginalRoute r =
      c60F39IsAtomicOriginalRoute s := by
  induction cell with
  | ident route => rfl
  | pentagon t₁ t₂ t₃ t₄ => rfl
  | disjointSquare left right => rfl
  | symm cell ih => exact ih.symm
  | trans left right ihLeft ihRight => exact ihLeft.trans ihRight
  | leftContext cell later ih => rfl
  | rightContext earlier cell ih => rfl
  | precompose priorRoute cell ih => rfl
  | postcompose cell suffix ih => rfl

/-- Strong ORIGINAL F54 boundary isolation: an original full-nine
F55 PresentedCell starting at an ATOMIC route ends at exactly the
SAME unquotiented original route. This does NOT assert that the
source PresentedCell evidence equals the identity constructor. -/
theorem c60F39AtomicSource_onlySameOriginalRoute
    (cell : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r s)
    (hbare : c60F39IsAtomicOriginalRoute r = true) :
    r = s := by
  induction cell with
  | ident route => rfl
  | pentagon t₁ t₂ t₃ t₄ => cases hbare
  | disjointSquare left right => cases hbare
  | symm cell ih =>
      have hb := (c60F39AtomicRoute_preserved cell).trans hbare
      exact (ih hb).symm
  | trans left right ihLeft ihRight =>
      have hm := (c60F39AtomicRoute_preserved left).symm.trans hbare
      exact (ihLeft hbare).trans (ihRight hm)
  | leftContext cell later ih => cases hbare
  | rightContext earlier cell ih => cases hbare
  | precompose priorRoute cell ih => cases hbare
  | postcompose cell suffix ih => cases hbare

/-- Square charge has NO nontrivial full-nine original F55 source
witness beginning at ANY bare original F54 chain or double cast.
This is strictly stronger than the old square-only subgrammar. -/
theorem c60F39AtomicSource_squareCharge_zero
    (cell : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r s)
    (hbare : c60F39IsAtomicOriginalRoute r = true) :
    c60F37SquareCharge cell = 0 := by
  induction cell with
  | ident route =>
      exact c60F37SquareCharge_ident route
  | pentagon t₁ t₂ t₃ t₄ => cases hbare
  | disjointSquare left right => cases hbare
  | symm cell ih =>
      have hb := (c60F39AtomicRoute_preserved cell).trans hbare
      rw [c60F37SquareCharge_symm, ih hb, neg_zero]
  | trans left right ihLeft ihRight =>
      have hm := (c60F39AtomicRoute_preserved left).symm.trans hbare
      rw [c60F37SquareCharge_trans, ihLeft hbare, ihRight hm, add_zero]
  | leftContext cell later ih => cases hbare
  | rightContext earlier cell ih => cases hbare
  | precompose priorRoute cell ih => cases hbare
  | postcompose cell suffix ih => cases hbare

/-- Numerical computation, not merely a formal existence:
H_r is the TRIVIAL INTEGER SUBGROUP on every atomic original
F54 route, even with the full nine original F55 constructors. -/
theorem c60F39AtomicOriginalSquareLoopSubgroup_eq_bot
    (route : OriginalF45BracketTree.DepthRotationRoute first last)
    (hbare : c60F39IsAtomicOriginalRoute route = true) :
    c60F37OriginalSquareLoopSubgroup route = ⊥ := by
  apply le_antisymm
  · intro z hz
    change ∃ loop : OriginalF45BracketTree.DepthRotationRoute.PresentedCell
      route route, c60F37SquareCharge loop = z at hz
    obtain ⟨loop, hloop⟩ := hz
    change z = 0
    exact hloop.symm.trans (c60F39AtomicSource_squareCharge_zero loop hbare)
  · exact bot_le

/-- The canonical F59-F38 period is numerically ZERO at
EVERY original atomic F54 route (real chain or double-depth cast).
The original generator witness from v5.186 is used, so no
assumption of subgroup-period injectivity is hidden. -/
theorem c60F39AtomicOriginalF55SquarePeriod_eq_zero
    (route : OriginalF45BracketTree.DepthRotationRoute first last)
    (hbare : c60F39IsAtomicOriginalRoute route = true) :
    c60F38F55SquarePeriod route = 0 := by
  obtain ⟨loop, hloop⟩ :=
    c60F38F55SquarePeriod_hasOriginalLoopWitness route
  have hz := c60F39AtomicSource_squareCharge_zero loop hbare
  have hi : (c60F38F55SquarePeriod route : ℤ) = 0 :=
    hloop.symm.trans hz
  exact_mod_cast hi

/-- A TRUE original elementary Type-valued F54 RotationChain
always has source-loop period ZERO. -/
theorem c60F39OriginalRotationChain_squarePeriod_zero
    {n m : Nat} {first last : OriginalF45BracketTree n m ma pa mb pb}
    (path : OriginalF45BracketTree.RotationChain first last) :
    c60F38F55SquarePeriod
      (OriginalF45BracketTree.DepthRotationRoute.chain path) = 0 :=
  c60F39AtomicOriginalF55SquarePeriod_eq_zero _ rfl

/-- Even an original double F19/F28 depth cast (NOT a fake source
equality) has zero original full-nine F55 square-loop period. -/
theorem c60F39OriginalDoubleDepthCast_squarePeriod_zero
    (hn : n = n') (hm : m = m')
    (tree : OriginalF45BracketTree n m ma pa mb pb) :
    c60F38F55SquarePeriod
      (OriginalF45BracketTree.DepthRotationRoute.castDepths hn hm tree) = 0 :=
  c60F39AtomicOriginalF55SquarePeriod_eq_zero _ rfl

/-- No F55 source evidence beginning at a bare original F54
route can carry anything but the native ZERO Gray coefficient.
This is genuine target rigidity; the original raw F55 witnesses
are NOT quotient-identified. -/
theorem c60F39AtomicOriginalF55Cell_nativeGray_zero
    (route : OriginalF45BracketTree.DepthRotationRoute first last)
    (hbare : c60F39IsAtomicOriginalRoute route = true)
    (loop : OriginalF45BracketTree.DepthRotationRoute.PresentedCell route route) :
    c60F55SourceNative loop = (0 : GradedThreeCell 0 0) := by
  apply GradedThreeCell.ext
  · change (c60F55SourceNative loop).charge = ((0 : ℤ), (0 : ℤ))
    apply Prod.ext
    · rw [c60F36FullNinePentagonCharge_eq_rotationDifference loop]
      simp
    · exact c60F39AtomicSource_squareCharge_zero loop hbare
  · have hp := c60F55SourceNative_mem loop
    change (c60F55SourceNative loop).phase =
      ((c60F55SourceNative loop).charge.2 : ZMod 2) at hp
    change (c60F55SourceNative loop).phase = 0
    rw [hp]
    have hz := c60F39AtomicSource_squareCharge_zero loop hbare
    change (c60F55SourceNative loop).charge.2 = (0 : ℤ) at hz
    exact congrArg (fun z : ℤ => (z : ZMod 2)) hz

/-- Exact source image criterion for ALL nine original constructors
on any genuine atomic F54 loop: the ONLY realizable native Gray
target is its actual identity. The converse is witnessed by an
actual original F55 PresentedCell.ident source, not an invented cell. -/
theorem c60F39AtomicFullNineLift_iff_zero
    (route : OriginalF45BracketTree.DepthRotationRoute first last)
    (hbare : c60F39IsAtomicOriginalRoute route = true)
    (g : GradedThreeCell 0 0) :
    (∃ loop : OriginalF45BracketTree.DepthRotationRoute.PresentedCell
      route route, c60F55SourceNative loop = g) ↔ g = 0 := by
  constructor
  · rintro ⟨loop, hloop⟩
    rw [← hloop]
    exact c60F39AtomicOriginalF55Cell_nativeGray_zero route hbare loop
  · intro hg
    subst g
    refine ⟨.ident route, ?_⟩
    rfl

/-- The ORIGINAL native F55 physical disjoint square generator
(0,1; phase 1) cannot be presented by ANY original full-nine
F55 source cell with an atomic original F54 route at both
boundaries, although the Gray generator itself is phase-locked. -/
theorem c60F39OriginalF55Square_notAtomicLift
    (route : OriginalF45BracketTree.DepthRotationRoute first last)
    (hbare : c60F39IsAtomicOriginalRoute route = true) :
    ¬ ∃ loop : OriginalF45BracketTree.DepthRotationRoute.PresentedCell
        route route,
      c60F55SourceNative loop = originalF55BraidedSquareGenerator := by
  rintro ⟨loop, hloop⟩
  have hz := c60F39AtomicSource_squareCharge_zero loop hbare
  have heq := congrArg
    (fun g : GradedThreeCell 0 0 => g.charge.2) hloop
  change c60F37SquareCharge loop = 1 at heq
  rw [hz] at heq
  exact (by decide : (0 : ℤ) ≠ 1) heq

end OriginalSourceAtomic

/-! ## Real original C60 source-image counterexample with ZERO curvature -/

section ActualC60
variable {a b : D} {x y : E}
variable {n n' m m' : Nat}
variable {ma mb : Blocks a b} {pa pb : Blocks x y}
variable {first : OriginalF45BracketTree n m ma pa mb pb}
variable {last : OriginalF45BracketTree n' m' ma pa mb pb}

/-- A concrete nonzero original F55 source-image obstruction
on the ACTUAL north spoke zero edge of the FLAT canonical C60
repair. All 90 target labels are phase-locked but this one has
square charge one, so no ORIGINAL F55 bare source loop can lift it. -/
theorem c60F39CanonicalFlatNorthCross_notAtomicSourceLift
    (route : OriginalF45BracketTree.DepthRotationRoute first last)
    (hbare : c60F39IsAtomicOriginalRoute route = true) :
    ¬ ∃ loop : OriginalF45BracketTree.DepthRotationRoute.PresentedCell
        route route,
      c60F55SourceNative loop =
        c60WangBiRepairedEdgeGrade (.cross (.northSpoke 0)) := by
  have heq :
      c60WangBiRepairedEdgeGrade (.cross (.northSpoke 0)) =
        originalF55BraidedSquareGenerator :=
      c60WangBiRepairedEdgeGrade_preserved _ (by decide)
  rw [heq]
  exact c60F39OriginalF55Square_notAtomicLift route hbare

/-- The ACTUAL canonical C60 repair is genuinely face-FLAT on
12 pentagons + 20 hexagons, and necessary-F55-phase-compatible
on ALL ninety edges, but it has NO all-nine original source
lift to bare F54 loops at all real physical edges. -/
theorem c60F39FlatAndLocked_canonicalC60_noAtomicSourceAtlas
    (route : OriginalF45BracketTree.DepthRotationRoute first last)
    (hbare : c60F39IsAtomicOriginalRoute route = true) :
    (∀ face : TruncatedIcosahedralSeedFace,
      c60WangBiSignedGrayFace c60WangBiRepairedEdgeGrade face = 0) ∧
    (∀ e : TruncatedIcosahedralEdge,
      c60WangBiRepairedEdgeGrade e ∈ c60F55PhaseLocked) ∧
    ¬ ∃ cells : ∀ _e : TruncatedIcosahedralEdge,
        OriginalF45BracketTree.DepthRotationRoute.PresentedCell route route,
      ∀ e : TruncatedIcosahedralEdge,
        c60F55SourceNative (cells e) = c60WangBiRepairedEdgeGrade e := by
  refine ⟨c60WangBiRepairedGrade_all32Faces_flat,
    c60F55RepairedGrade_mem, ?_⟩
  rintro ⟨cells, hcells⟩
  exact (c60F39CanonicalFlatNorthCross_notAtomicSourceLift
    route hbare) ⟨cells (.cross (.northSpoke 0)),
      hcells (.cross (.northSpoke 0))⟩

#print axioms c60F39FlatAndLocked_canonicalC60_noAtomicSourceAtlas

end ActualC60

#print axioms c60F39AtomicRoute_preserved
#print axioms c60F39AtomicSource_onlySameOriginalRoute
#print axioms c60F39AtomicSource_squareCharge_zero
#print axioms c60F39AtomicOriginalSquareLoopSubgroup_eq_bot
#print axioms c60F39AtomicOriginalF55SquarePeriod_eq_zero
#print axioms c60F39OriginalRotationChain_squarePeriod_zero
#print axioms c60F39OriginalDoubleDepthCast_squarePeriod_zero
#print axioms c60F39AtomicOriginalF55Cell_nativeGray_zero
#print axioms c60F39AtomicFullNineLift_iff_zero
#print axioms c60F39OriginalF55Square_notAtomicLift
#print axioms c60F39CanonicalFlatNorthCross_notAtomicSourceLift

end
end KUOS.DependentOriginationGrayC60AtomicSourceRigidityV5_187
