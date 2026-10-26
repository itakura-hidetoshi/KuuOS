import Kuu.F112.PolygonNativeC60PhysicalBinaryHeapBoundaryObstruction

/-!
# F112-P94D3BP — source-size non-erasure contradicts physical diagonal BG

BO excludes a particular two-input pivoted heap boundary law. BP finds a
STRICTLY BROADER obstruction, independent of a concrete polynomial
shape or a fixed pivot.

Let |R| be the constructor size of the ORIGINAL dependent C60 14D
raw proof tree (trans and symm are never collapsed). The two true AQ
left/right frames each increase this size by a positive constant k_side.
A binary 15D-object operation is called source-size non-erasing when

  |source(op(a,b))| >= |source(a)| + |source(b)|

for every pair of ORIGINAL physical 15D objects a,b. This is an explicit
strong sufficient notion of preserving both input construction histories.
No stronger claim is made about every possible nondegenerate operation.

If an operation were BG-equivariant under even ONE genuine C60 frame,
its output along n diagonal applications would grow by n*k_side,
whereas non-erasure forces growth of at least 2*n*k_side. Choosing n
larger than the original output size yields a contradiction.

Both singleton BG gates thus FAIL for every such non-erasing operation,
regardless of its internal term shape, the higher AX comparison
signature, or a selected strict Kuu replacement relation. The BO heap
is an actual instance of this more general obstruction.

This is a theorem about exact original dependent raw 14D boundaries,
not observer equality, not the original missing geometric 16-cell, and
NOT a global no-go for all possible notions of nondegeneracy.
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

/-- Count actual original 14D FREE constructors in the top-level
trans/symm grammar. Other native 14D constructors contribute one
atomic unit: no quotient or observer enters this recursive metric. -/
def nativeK5BPFourteenSize
    {A B : NativeK5StructuralThirteenCell p U V} :
    NativeK5StructuralFourteenCell p A B → Nat
  | .trans c d => nativeK5BPFourteenSize c + nativeK5BPFourteenSize d + 1
  | .symm c => nativeK5BPFourteenSize c + 1
  | _ => 1

/-- The exact SOURCE 14D proof stored inside a proof-relevant physical
15D object, with no forgetting of its genuine 13D endpoint indices. -/
def nativeK5BPSourceSize
    (W : NativeK5StructuralThirteenCell p U V)
    (x : (nativeK5AXBaseLayer W).Total) : Nat :=
  nativeK5BPFourteenSize x.1.1.down

/-- A single original C60 frame adds a positive number of raw
constructors. The size is calculated directly on ACTUAL AQ loops. -/
def nativeK5BPFrameCost
    (W : NativeK5StructuralThirteenCell p U V) : Bool → Nat
  | false => nativeK5BPFourteenSize (nativeK5AQRightFrame W) + 1
  | true => nativeK5BPFourteenSize (nativeK5AQLeftFrame W) + 1

theorem nativeK5BPFrameCost_pos
    (W : NativeK5StructuralThirteenCell p U V)
    (side : Bool) : 1 ≤ nativeK5BPFrameCost W side := by
  cases side <;> simp only [nativeK5BPFrameCost] <;> omega

/-- Genuine original AQ left/right whiskering increases SOURCE
size by exactly k_side. This is a raw constructor equality. -/
theorem nativeK5BPSourceSize_singleton
    (W : NativeK5StructuralThirteenCell p U V)
    (side : Bool) (x : (nativeK5AXBaseLayer W).Total) :
    nativeK5BPSourceSize W (nativeK5BCContext W [side] x) =
      nativeK5BPSourceSize W x + nativeK5BPFrameCost W side := by
  rcases x with ⟨⟨⟨R⟩, ⟨S⟩⟩, ⟨cell⟩⟩
  cases side with
  | false =>
      change nativeK5BPFourteenSize (nativeK5AQWhiskerRight W R) =
        nativeK5BPFourteenSize R +
          (nativeK5BPFourteenSize (nativeK5AQRightFrame W) + 1)
      change nativeK5BPFourteenSize R +
          nativeK5BPFourteenSize (nativeK5AQRightFrame W) + 1 = _
      omega
  | true =>
      change nativeK5BPFourteenSize (nativeK5AQWhiskerLeft W R) =
        nativeK5BPFourteenSize R +
          (nativeK5BPFourteenSize (nativeK5AQLeftFrame W) + 1)
      change nativeK5BPFourteenSize (nativeK5AQLeftFrame W) +
          nativeK5BPFourteenSize R + 1 = _
      omega

/-- Repeated physical frame action on the ENTIRE typed 15D object,
including its proof-carrying target and original lower source. -/
def nativeK5BPIter
    (W : NativeK5StructuralThirteenCell p U V)
    (side : Bool) : Nat → (nativeK5AXBaseLayer W).Total →
      (nativeK5AXBaseLayer W).Total
  | 0, x => x
  | n + 1, x => nativeK5BCContext W [side] (nativeK5BPIter W side n x)

/-- True arithmetic growth along arbitrarily many diagonal physical
contexts. Not an abstract asymptotic or an observer measurement. -/
theorem nativeK5BPSourceSize_iter
    (W : NativeK5StructuralThirteenCell p U V)
    (side : Bool) (n : Nat) (x : (nativeK5AXBaseLayer W).Total) :
    nativeK5BPSourceSize W (nativeK5BPIter W side n x) =
      nativeK5BPSourceSize W x + n * nativeK5BPFrameCost W side := by
  induction n with
  | zero => simp only [nativeK5BPIter, Nat.zero_mul, Nat.add_zero]
  | succ n ih =>
      change nativeK5BPSourceSize W
        (nativeK5BCContext W [side] (nativeK5BPIter W side n x)) = _
      rw [nativeK5BPSourceSize_singleton W side, ih, Nat.succ_mul]
      omega

/-- A physical BG singleton gate forces the binary operation to
intertwine ALL repeated applications of THAT same genuine frame.
No separate, unproved higher coherence is used in the induction. -/
theorem nativeK5BPIter_diagonal
    (W : NativeK5StructuralThirteenCell p U V)
    (Hh : NativeC60BBWhiskering (nativeK5BCSignature W))
    (side : Bool)
    (he : NativeC60BGWhiskeringEquivariant
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W) Hh [side])
    (n : Nat) (x y : (nativeK5AXBaseLayer W).Total) :
    nativeK5BPIter W side n (Hh.obj x y) =
      Hh.obj (nativeK5BPIter W side n x)
        (nativeK5BPIter W side n y) := by
  induction n with
  | zero => rfl
  | succ n ih =>
      change nativeK5BCContext W [side]
          (nativeK5BPIter W side n (Hh.obj x y)) =
        Hh.obj
          (nativeK5BCContext W [side] (nativeK5BPIter W side n x))
          (nativeK5BCContext W [side] (nativeK5BPIter W side n y))
      rw [ih]
      exact nativeC60BJObjectGate_of_equivariant
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
        Hh [side] he _ _

/-- An explicit strong non-erasure requirement on a proposed
two-input operation's ORIGINAL source 14D syntax. This cannot be
replaced by merely observing equal Peiffer numbers or quotient classes. -/
def NativeK5BPSourceSizeNonerasing
    (W : NativeK5StructuralThirteenCell p U V)
    (op : (nativeK5AXBaseLayer W).Total →
      (nativeK5AXBaseLayer W).Total → (nativeK5AXBaseLayer W).Total) : Prop :=
  ∀ x y, nativeK5BPSourceSize W (op x y) ≥
    nativeK5BPSourceSize W x + nativeK5BPSourceSize W y

/-- MAIN NO-GO: ANY binary operation retaining at least the SUM of
the two original raw source complexities cannot satisfy EVEN ONE
physical BG singleton. The contradiction applies the same unary
frame n times: output grows as n*k, input sum as 2*n*k.
Taking n = original output size + 1 makes this impossible. -/
theorem nativeK5BPNonerasing_no_singleton_BG
    (W : NativeK5StructuralThirteenCell p U V)
    (Hh : NativeC60BBWhiskering (nativeK5BCSignature W))
    (hsize : NativeK5BPSourceSizeNonerasing W Hh.obj)
    (side : Bool) :
    ¬ NativeC60BGWhiskeringEquivariant
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W) Hh [side] := by
  intro he
  let x := nativeK5AXPack W (nativeK5AQExchange W [])
  let n := nativeK5BPSourceSize W (Hh.obj x x) + 1
  have hdiag := nativeK5BPIter_diagonal W Hh side he n x x
  have hsz := congrArg (nativeK5BPSourceSize W) hdiag
  have hbound := hsize (nativeK5BPIter W side n x)
    (nativeK5BPIter W side n x)
  rw [nativeK5BPSourceSize_iter W side n (Hh.obj x x)] at hsz
  rw [nativeK5BPSourceSize_iter W side n x] at hbound
  rw [← hsz] at hbound
  have hcost : 1 ≤ nativeK5BPFrameCost W side :=
    nativeK5BPFrameCost_pos W side
  have hiter : n ≤ n * nativeK5BPFrameCost W side := by
    calc
      n = n * 1 := by omega
      _ ≤ n * nativeK5BPFrameCost W side :=
        Nat.mul_le_mul_left n hcost
  dsimp [n] at hbound hiter
  omega

/-- Neither TRUE/LEFT nor FALSE/RIGHT can serve as a BG generating
gate for a source-size non-erasing physical binary operation. -/
theorem nativeK5BPNonerasing_no_both_BG
    (W : NativeK5StructuralThirteenCell p U V)
    (Hh : NativeC60BBWhiskering (nativeK5BCSignature W))
    (hsize : NativeK5BPSourceSizeNonerasing W Hh.obj) :
    (¬ NativeC60BGWhiskeringEquivariant
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W) Hh [false]) ∧
    (¬ NativeC60BGWhiskeringEquivariant
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W) Hh [true]) :=
  ⟨nativeK5BPNonerasing_no_singleton_BG W Hh hsize false,
    nativeK5BPNonerasing_no_singleton_BG W Hh hsize true⟩

/-- Independently of a specific polynomial formula, no source-size
non-erasing physical BB operation satisfies all finite BG words. -/
theorem nativeK5BPNonerasing_no_all_BG
    (W : NativeK5StructuralThirteenCell p U V)
    (Hh : NativeC60BBWhiskering (nativeK5BCSignature W))
    (hsize : NativeK5BPSourceSizeNonerasing W Hh.obj) :
    ¬ ∀ word : List Bool,
      NativeC60BGWhiskeringEquivariant
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W) Hh word := by
  intro hall
  exact nativeK5BPNonerasing_no_singleton_BG W Hh hsize true (hall [true])

/-- The two-input BO HEAP meets this strong raw size non-erasure
criterion for EVERY fixed original 14D pivot. -/
theorem nativeK5BPFourteenSize_heap
    (W : NativeK5StructuralThirteenCell p U V)
    (pivot R S : NativeK5FifteenFourteenFiber W) :
    nativeK5BPFourteenSize (nativeK5BOHeapFourteen W pivot R S) =
      nativeK5BPFourteenSize R + nativeK5BPFourteenSize S +
        nativeK5BPFourteenSize pivot + 3 := by
  change (nativeK5BPFourteenSize R +
      (nativeK5BPFourteenSize pivot + 1) + 1) +
        nativeK5BPFourteenSize S + 1 = _
  omega

/-- BO's explicit heap obstruction is subsumed by the general
source-size non-erasure obstruction, without requiring an
additional AX geometry generator or any selected quotient. -/
theorem nativeK5BPHeapSource_nonerasing
    (W : NativeK5StructuralThirteenCell p U V)
    (pivot : NativeK5FifteenFourteenFiber W)
    (op : (nativeK5AXBaseLayer W).Total →
      (nativeK5AXBaseLayer W).Total → (nativeK5AXBaseLayer W).Total)
    (hlaw : NativeK5BOHeapSourceLaw W pivot op) :
    NativeK5BPSourceSizeNonerasing W op := by
  intro x y
  have hsrc := congrArg
    (fun z : NativeK5FifteenFourteenFiber W => nativeK5BPFourteenSize z)
    (hlaw x y)
  change nativeK5BPSourceSize W (op x y) =
    nativeK5BPFourteenSize
      (nativeK5BOHeapFourteen W pivot x.1.1.down y.1.1.down) at hsrc
  rw [hsrc, nativeK5BPFourteenSize_heap]
  dsimp only [nativeK5BPSourceSize]
  omega

/-- The original BO heap law therefore fails BOTH BG singleton
gates, not merely the left gate established by the direct left-spine
calculation in BO. -/
theorem nativeK5BPHeap_no_two_gates
    (W : NativeK5StructuralThirteenCell p U V)
    (pivot : NativeK5FifteenFourteenFiber W)
    (Hh : NativeC60BBWhiskering (nativeK5BCSignature W))
    (hlaw : NativeK5BOHeapSourceLaw W pivot Hh.obj) :
    (¬ NativeC60BGWhiskeringEquivariant
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W) Hh [false]) ∧
    (¬ NativeC60BGWhiskeringEquivariant
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W) Hh [true]) :=
  nativeK5BPNonerasing_no_both_BG W Hh
    (nativeK5BPHeapSource_nonerasing W pivot Hh.obj hlaw)

end OriginalC60

#print axioms nativeK5BPFourteenSize
#print axioms nativeK5BPSourceSize
#print axioms nativeK5BPFrameCost
#print axioms nativeK5BPFrameCost_pos
#print axioms nativeK5BPSourceSize_singleton
#print axioms nativeK5BPIter
#print axioms nativeK5BPSourceSize_iter
#print axioms nativeK5BPIter_diagonal
#print axioms NativeK5BPSourceSizeNonerasing
#print axioms nativeK5BPNonerasing_no_singleton_BG
#print axioms nativeK5BPNonerasing_no_both_BG
#print axioms nativeK5BPNonerasing_no_all_BG
#print axioms nativeK5BPFourteenSize_heap
#print axioms nativeK5BPHeapSource_nonerasing
#print axioms nativeK5BPHeap_no_two_gates

end
end Kuu.F112.Physical
