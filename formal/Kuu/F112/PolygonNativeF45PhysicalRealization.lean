import Kuu.F112.PolygonNativeF45TraceSplit

/-!
# F112-E7Q5-F4-O9-B — constructive realization of every physical packet

For any genuine C60 PolygonDepthTree and any TWO complete native
Type-valued histories with matching total depths, recursively build
an ACTUAL raw KuuNativeF45Tree. At each node, O9-A constructs the
intermediate original Blocks, both independent subtraces and their
literal recomposition certificates. The resulting raw tree has
EXACTLY the selected physical sectors, binary bracketing, leaf Nat
depths and both complete original evidence histories.

A total dependent raw-carrier is constructed and shown to map onto
the ENTIRE ambient O8 physical-history and physical-exchange spaces,
using explicit right inverses. These are not left inverses: raw leaf
ordering and refl-vs-leaf distinctions remain noninjective as proved
in O8. No historical or Gray structure is imported.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
noncomputable section

universe uA vA uB vB
variable {A : Type uA} [Category.{vA} A]
variable {B : Type uB} [Category.{vB} B]

/-- Construct a genuinely typed raw F45 execution witnessing the
chosen C60 physical bracket and BOTH exact Type-valued histories.
The proof packet retains literal equality, not only existence. -/
def KuuNativeF45Tree.realizePacket
    {p : Polygon} {a b : A} {x y : B} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (physical : PolygonDepthTree p n m)
    (firstHistory : KuuNativeAxisTrace n ma mb)
    (secondHistory : KuuNativeAxisTrace m pa pb) :
    { tree : KuuNativeF45Tree p n m ma pa mb pb //
      tree.erasePhysical = physical ∧
        tree.axisHistories = (firstHistory, secondHistory) } := by
  induction physical generalizing ma mb pa pb firstHistory secondHistory with
  | leaf item =>
      cases item with
      | mk sector firstDepth secondDepth =>
          exact ⟨.leaf sector .firstAxisFirst firstHistory secondHistory, ⟨rfl, rfl⟩⟩
  | @node n₁ m₁ n₂ m₂ left right ihLeft ihRight =>
      rcases KuuNativeAxisTrace.splitAppend n₁ n₂ firstHistory with
        ⟨middleFirst, firstLeft, ⟨firstRight, firstJoin⟩⟩
      rcases KuuNativeAxisTrace.splitAppend m₁ m₂ secondHistory with
        ⟨middleSecond, secondLeft, ⟨secondRight, secondJoin⟩⟩
      rcases ihLeft firstLeft secondLeft with
        ⟨treeLeft, physicalLeft, historiesLeft⟩
      rcases ihRight firstRight secondRight with
        ⟨treeRight, physicalRight, historiesRight⟩
      refine ⟨.node treeLeft treeRight, ⟨?_, ?_⟩⟩
      · change PolygonDepthTree.node treeLeft.erasePhysical treeRight.erasePhysical =
          PolygonDepthTree.node left right
        rw [physicalLeft, physicalRight]
      · change
          (treeLeft.axisHistories.1.append treeRight.axisHistories.1,
           treeLeft.axisHistories.2.append treeRight.axisHistories.2) =
            (firstHistory, secondHistory)
        apply Prod.ext
        · rw [congrArg Prod.fst historiesLeft, congrArg Prod.fst historiesRight]
          exact firstJoin
        · rw [congrArg Prod.snd historiesLeft, congrArg Prod.snd historiesRight]
          exact secondJoin

/-- Total dependent carrier of actual native F45 raw trees, without
forgetting category endpoints, the four Blocks or original syntax. -/
def KuuNativeF45PhysicalRaw (p : Polygon) (n m : Nat)
    (A : Type uA) [Category.{vA} A] (B : Type uB) [Category.{vB} B] :=
  Σ a : A, Σ b : A, Σ x : B, Σ y : B,
    Σ ma : KuuNativeBlocks a b, Σ mb : KuuNativeBlocks a b,
      Σ pa : KuuNativeBlocks x y, Σ pb : KuuNativeBlocks x y,
        KuuNativeF45Tree p n m ma pa mb pb

/-- Observe the complete physical bracket and Type-valued histories
from any actual total raw F45 source. -/
def KuuNativeF45PhysicalRaw.executeHistories
    {p : Polygon} {n m : Nat}
    (raw : KuuNativeF45PhysicalRaw p n m A B) :
    KuuNativeF45PhysicalHistories p n m A B :=
  match raw with
  | ⟨_, _, _, _, _, _, _, _, tree⟩ => tree.physicalHistories

/-- Execute the same raw F45 tree to the selected O8 exchange class. -/
def KuuNativeF45PhysicalRaw.executeExchange
    {p : Polygon} {n m : Nat}
    (raw : KuuNativeF45PhysicalRaw p n m A B) :
    KuuNativeF45PhysicalExchange p n m A B :=
  match raw with
  | ⟨_, _, _, _, _, _, _, _, tree⟩ => tree.physicalExchange

/-- The O8 natural classification commutes with EVERY raw tree in
the total dependent source, not only with chosen representatives. -/
theorem KuuNativeF45PhysicalRaw.history_execution_square
    {p : Polygon} {n m : Nat}
    (raw : KuuNativeF45PhysicalRaw p n m A B) :
    kuuNativeF45PhysicalHistoryEquiv p n m A B raw.executeExchange =
      raw.executeHistories := by
  rcases raw with ⟨a, b, x, y, ma, mb, pa, pb, tree⟩
  exact tree.physicalHistoryEquiv_execution

/-- Constructively choose an actual raw F45 representative of EVERY
physical/history packet, preserving its full native evidence. -/
def KuuNativeF45PhysicalHistories.chooseRaw
    {p : Polygon} {n m : Nat}
    (s : KuuNativeF45PhysicalHistories p n m A B) :
    KuuNativeF45PhysicalRaw p n m A B :=
  match s with
  | ⟨a, b, x, y, physical, ⟨ma, mb, pa, pb, first, second⟩⟩ =>
      ⟨a, b, x, y, ma, mb, pa, pb,
        (KuuNativeF45Tree.realizePacket physical first second).1⟩

/-- The constructed representative executes EXACTLY to the input
physical/history packet. This is a RIGHT inverse only. -/
theorem KuuNativeF45PhysicalHistories.executeHistories_chooseRaw
    {p : Polygon} {n m : Nat}
    (s : KuuNativeF45PhysicalHistories p n m A B) :
    s.chooseRaw.executeHistories = s := by
  rcases s with ⟨a, b, x, y, physical, ⟨ma, mb, pa, pb, first, second⟩⟩
  let witness := KuuNativeF45Tree.realizePacket physical first second
  change
    (⟨a, b, x, y, witness.1.erasePhysical,
      ⟨ma, mb, pa, pb, witness.1.axisHistories.1,
        witness.1.axisHistories.2⟩⟩ :
      KuuNativeF45PhysicalHistories p n m A B) =
    ⟨a, b, x, y, physical, ⟨ma, mb, pa, pb, first, second⟩⟩
  exact congrArg₂
    (fun (phys : PolygonDepthTree p n m)
        (hist : KuuNativeAxisTrace n ma mb × KuuNativeAxisTrace m pa pb) =>
      (⟨a, b, x, y, phys,
        ⟨ma, mb, pa, pb, hist.1, hist.2⟩⟩ :
        KuuNativeF45PhysicalHistories p n m A B))
    witness.2.1 witness.2.2

/-- Choose representatives for every generated exchange class by
first applying the already certified O8 natural isomorphism. -/
def KuuNativeF45PhysicalExchange.chooseRaw
    {p : Polygon} {n m : Nat}
    (s : KuuNativeF45PhysicalExchange p n m A B) :
    KuuNativeF45PhysicalRaw p n m A B :=
  (kuuNativeF45PhysicalHistoryEquiv p n m A B s).chooseRaw

/-- Every O8 physical-exchange packet is in the image of ACTUAL raw
F45 execution. This right inverse does not negate O8 noninjectivity
nor claim any historical F45 equivalence. -/
theorem KuuNativeF45PhysicalExchange.executeExchange_chooseRaw
    {p : Polygon} {n m : Nat}
    (s : KuuNativeF45PhysicalExchange p n m A B) :
    s.chooseRaw.executeExchange = s := by
  apply (kuuNativeF45PhysicalHistoryEquiv p n m A B).injective
  calc
    kuuNativeF45PhysicalHistoryEquiv p n m A B
        (s.chooseRaw.executeExchange) =
      s.chooseRaw.executeHistories :=
        s.chooseRaw.history_execution_square
    _ = kuuNativeF45PhysicalHistoryEquiv p n m A B s :=
      KuuNativeF45PhysicalHistories.executeHistories_chooseRaw _

#print axioms KuuNativeF45Tree.realizePacket
#print axioms KuuNativeF45PhysicalRaw
#print axioms KuuNativeF45PhysicalRaw.history_execution_square
#print axioms KuuNativeF45PhysicalHistories.chooseRaw
#print axioms KuuNativeF45PhysicalHistories.executeHistories_chooseRaw
#print axioms KuuNativeF45PhysicalExchange.chooseRaw
#print axioms KuuNativeF45PhysicalExchange.executeExchange_chooseRaw
end
end Kuu.F112.Physical
