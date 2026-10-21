import Kuu.F112.PolygonNativeHistoricalProofBoundary

/-!
# F112-E7Q5-F4-P1-B — physical C60 F45 comparison and evidence fibers

P1-A recreates the exact frozen F42 OneStep Prop generator shapes
and F45 Type-valued AxisTrace shape independently over native Blocks.
Here the two old-shaped axes are installed on the ACTUAL O9 physical
F45 packets, retaining every original C60 polygon sector, physical
binary parenthesis, all four categorical endpoints, all four Blocks
and all Nat depths.

O9's constructive raw realization is transported to the historical-
shaped Prop-step history space. Primitive proof extraction from Prop
is necessarily an explicitly marked Classical.choice operation.
Every historic-shaped packet has a raw representative, but the
observation is NOT injective: different native split/insertNil evidence
at precisely the same typed C60 boundaries is identified.

This is a formally verified SHAPE comparison and an exact information
boundary. It is NOT an equivalence with the frozen original KUOS F19,
F28, F44, or F45 module nor a Gray/F47/F77 lift.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
noncomputable section

universe uA vA uB vB
variable {A : Type uA} [Category.{vA} A]
variable {B : Type uB} [Category.{vB} B]

/-- Four genuine native Blocks and two OLD-SHAPED Prop-step histories;
the total proof-history packet itself is still Type-valued. -/
structure KuuNativeHistoricalF44Histories
    (a b : A) (x y : B) (n m : Nat) where
  firstSource : KuuNativeBlocks a b
  firstTarget : KuuNativeBlocks a b
  secondSource : KuuNativeBlocks x y
  secondTarget : KuuNativeBlocks x y
  firstHistory : KuuNativeHistoricalAxisTrace n firstSource firstTarget
  secondHistory : KuuNativeHistoricalAxisTrace m secondSource secondTarget

/-- Full C60 bracket together with historical-shaped proof erasure;
no physical sector, Cat endpoint or original Blocks are quotiented. -/
def KuuNativeHistoricalF45PhysicalHistories (p : Polygon) (n m : Nat)
    (A : Type uA) [Category.{vA} A]
    (B : Type uB) [Category.{vB} B] :=
  Σ a : A, Σ b : A, Σ x : B, Σ y : B,
    PolygonDepthTree p n m × KuuNativeHistoricalF44Histories a b x y n m

/-- Forget ONLY each Type-valued primitive proof to the historical-
shaped Prop. The total F45 packet, including physical leaves,
remains genuinely Type-valued. -/
def KuuNativeF45PhysicalHistories.toHistorical
    {p : Polygon} {n m : Nat}
    (s : KuuNativeF45PhysicalHistories p n m A B) :
    KuuNativeHistoricalF45PhysicalHistories p n m A B :=
  match s with
  | ⟨a, b, x, y, physical, ⟨ma, mb, pa, pb, first, second⟩⟩ =>
      ⟨a, b, x, y, physical,
        ⟨ma, mb, pa, pb, first.toHistorical, second.toHistorical⟩⟩

/-- Choose raw Type-valued step witnesses from two independently
typed Prop-valued histories. Requires an explicit Classical.choice
inside P1-A; O9's subsequent physical realization stays constructive. -/
def KuuNativeHistoricalF45PhysicalHistories.chooseNative
    {p : Polygon} {n m : Nat}
    (s : KuuNativeHistoricalF45PhysicalHistories p n m A B) :
    KuuNativeF45PhysicalHistories p n m A B :=
  match s with
  | ⟨a, b, x, y, physical, ⟨ma, mb, pa, pb, first, second⟩⟩ =>
      ⟨a, b, x, y, physical,
        ⟨ma, mb, pa, pb, first.chooseNative, second.chooseNative⟩⟩

/-- Choice is a RIGHT inverse of evidence erasure across the FULL
physical C60 packet, not a source-evidence reconstruction. -/
theorem KuuNativeHistoricalF45PhysicalHistories.toHistorical_chooseNative
    {p : Polygon} {n m : Nat}
    (s : KuuNativeHistoricalF45PhysicalHistories p n m A B) :
    s.chooseNative.toHistorical = s := by
  rcases s with ⟨a, b, x, y, physical, ⟨ma, mb, pa, pb, first, second⟩⟩
  exact congrArg₂
    (fun (h₁ : KuuNativeHistoricalAxisTrace n ma mb)
        (h₂ : KuuNativeHistoricalAxisTrace m pa pb) =>
      (⟨a, b, x, y, physical, ⟨ma, mb, pa, pb, h₁, h₂⟩⟩ :
        KuuNativeHistoricalF45PhysicalHistories p n m A B))
    first.toHistorical_chooseNative second.toHistorical_chooseNative

/-- ACTUAL O9 raw F45 source, then the precise P1 proof-erasure. -/
def KuuNativeF45PhysicalRaw.executeHistorical
    {p : Polygon} {n m : Nat}
    (raw : KuuNativeF45PhysicalRaw p n m A B) :
    KuuNativeHistoricalF45PhysicalHistories p n m A B :=
  raw.executeHistories.toHistorical

/-- Every historical-shaped C60 physical packet is realized by an
ACTUAL independent raw F45 tree; the Type evidence choice, and hence
this particular representative, is noncomputable. -/
def KuuNativeHistoricalF45PhysicalHistories.chooseRaw
    {p : Polygon} {n m : Nat}
    (s : KuuNativeHistoricalF45PhysicalHistories p n m A B) :
    KuuNativeF45PhysicalRaw p n m A B :=
  s.chooseNative.chooseRaw

/-- Exact RIGHT inverse on the entire historical-shaped ambient
packet space, preserving every physical polygon leaf and Nat depth. -/
theorem KuuNativeHistoricalF45PhysicalHistories.executeHistorical_chooseRaw
    {p : Polygon} {n m : Nat}
    (s : KuuNativeHistoricalF45PhysicalHistories p n m A B) :
    s.chooseRaw.executeHistorical = s := by
  calc
    s.chooseRaw.executeHistorical = s.chooseNative.toHistorical := by
      change (s.chooseNative.chooseRaw.executeHistories).toHistorical =
        s.chooseNative.toHistorical
      rw [KuuNativeF45PhysicalHistories.executeHistories_chooseRaw]
    _ = s := s.toHistorical_chooseNative

/-- The historical-shaped observation on a fixed typed raw source
preserves the same physical witness as the certified O8 observation. -/
def KuuNativeF45Tree.physicalHistorical
    {p : Polygon} {a b : A} {x y : B} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (tree : KuuNativeF45Tree p n m ma pa mb pb) :
    KuuNativeHistoricalF45PhysicalHistories p n m A B :=
  tree.physicalHistories.toHistorical

/-- The two genuinely distinct F41 Type evidences yield different
raw F45 trees, even with exactly the SAME sector and F45 order. -/
theorem nativeF45HistoricalDoubleNil_leaf_raw_ne
    {p : Polygon} {a b : A} {x y : B}
    (i : PolygonBoundarySector p)
    (ma : KuuNativeBlocks a b) (pa : KuuNativeBlocks x y) :
    KuuNativeF45Tree.leaf i .firstAxisFirst
      (nativeF41DoubleNilSplitTrace ma) (.refl pa) ≠
    KuuNativeF45Tree.leaf i .firstAxisFirst
      (nativeF41DoubleNilInsertTrace ma) (.refl pa) := by
  intro h
  have hh := congrArg
    (fun t : KuuNativeF45Tree p 1 0
      (nativeF41DoubleNilSource ma) pa
      (nativeF41DoubleNilTarget ma) pa => t.axisHistories.1) h
  exact nativeF41DoubleNilSplitTrace_ne_insert ma hh

/-- But precisely the historical Prop-valued primitive evidence is
erased: EVERY other aspect of their physical packet agrees. -/
theorem nativeF45HistoricalDoubleNil_leaf_observation_eq
    {p : Polygon} {a b : A} {x y : B}
    (i : PolygonBoundarySector p)
    (ma : KuuNativeBlocks a b) (pa : KuuNativeBlocks x y) :
    (KuuNativeF45Tree.leaf i .firstAxisFirst
      (nativeF41DoubleNilSplitTrace ma) (.refl pa)).physicalHistorical =
    (KuuNativeF45Tree.leaf i .firstAxisFirst
      (nativeF41DoubleNilInsertTrace ma) (.refl pa)).physicalHistorical := by
  exact congrArg
    (fun h₁ : KuuNativeHistoricalAxisTrace 1
        (nativeF41DoubleNilSource ma) (nativeF41DoubleNilTarget ma) =>
      (⟨a, b, x, y, polygonDepthLeafAt p i 1 0,
        ⟨nativeF41DoubleNilSource ma, nativeF41DoubleNilTarget ma,
         pa, pa, h₁, KuuNativeHistoricalAxisTrace.refl pa⟩⟩ :
        KuuNativeHistoricalF45PhysicalHistories p 1 0 A B))
    (nativeF41DoubleNil_toHistorical_eq ma)

/-- A physical proof-bearing raw F45 fiber has NO left inverse from
the historical-shaped observed packet, although O9/P1 supply RIGHT
inverses on the full ambient packet types. -/
theorem nativeF45HistoricalDoubleNil_no_leftInverse
    {p : Polygon} {a b : A} {x y : B}
    (i : PolygonBoundarySector p)
    (ma : KuuNativeBlocks a b) (pa : KuuNativeBlocks x y) :
    ¬ ∃ recover : KuuNativeHistoricalF45PhysicalHistories p 1 0 A B →
      KuuNativeF45Tree p 1 0
        (nativeF41DoubleNilSource ma) pa
        (nativeF41DoubleNilTarget ma) pa,
      Function.LeftInverse recover
        (fun tree : KuuNativeF45Tree p 1 0
          (nativeF41DoubleNilSource ma) pa
          (nativeF41DoubleNilTarget ma) pa => tree.physicalHistorical) := by
  rintro ⟨recover, hrecover⟩
  apply nativeF45HistoricalDoubleNil_leaf_raw_ne i ma pa
  apply hrecover.injective
  exact nativeF45HistoricalDoubleNil_leaf_observation_eq i ma pa

/-- An actual north C60 pentagon sector instantiates the full
physical right/left asymmetry; no Bool or numerical proxy is used. -/
theorem northPentagonHistoricalF45_no_leftInverse :
    ¬ ∃ recover :
        KuuNativeHistoricalF45PhysicalHistories (.pentagon .north) 1 0 Site Site →
        KuuNativeF45Tree (.pentagon .north) 1 0
          (nativeF41DoubleNilSource northPentagonNativeDualAxisFrame.firstAxis)
          northPentagonNativeDualAxisFrame.secondAxis
          (nativeF41DoubleNilTarget northPentagonNativeDualAxisFrame.firstAxis)
          northPentagonNativeDualAxisFrame.secondAxis,
      Function.LeftInverse recover
        (fun tree : KuuNativeF45Tree (.pentagon .north) 1 0
          (nativeF41DoubleNilSource northPentagonNativeDualAxisFrame.firstAxis)
          northPentagonNativeDualAxisFrame.secondAxis
          (nativeF41DoubleNilTarget northPentagonNativeDualAxisFrame.firstAxis)
          northPentagonNativeDualAxisFrame.secondAxis => tree.physicalHistorical) :=
  nativeF45HistoricalDoubleNil_no_leftInverse
    (firstFourPolygonSector (.pentagon .north) 0)
    northPentagonNativeDualAxisFrame.firstAxis
    northPentagonNativeDualAxisFrame.secondAxis

#print axioms KuuNativeF45PhysicalHistories.toHistorical
#print axioms KuuNativeHistoricalF45PhysicalHistories.chooseNative
#print axioms KuuNativeHistoricalF45PhysicalHistories.toHistorical_chooseNative
#print axioms KuuNativeF45PhysicalRaw.executeHistorical
#print axioms KuuNativeHistoricalF45PhysicalHistories.chooseRaw
#print axioms KuuNativeHistoricalF45PhysicalHistories.executeHistorical_chooseRaw
#print axioms nativeF45HistoricalDoubleNil_leaf_raw_ne
#print axioms nativeF45HistoricalDoubleNil_leaf_observation_eq
#print axioms nativeF45HistoricalDoubleNil_no_leftInverse
#print axioms northPentagonHistoricalF45_no_leftInverse
end
end Kuu.F112.Physical
