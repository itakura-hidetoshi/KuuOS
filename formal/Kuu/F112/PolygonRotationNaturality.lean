import Kuu.F112.PolygonRotationTransport

/-!
# F112-E4 / proof-relevant physical F54 rotation naturality squares

The original cyclic polygon loop based at dart k, the loop based at
dart l, and the actual oriented original C60 boundary subpath k->l
produce TWO fully typed composite original raw F69 zigzags:
    transport(k,l) ; rotation(l)
    rotation(k) ; transport(k,l).

Their equality is PROVED only after the actual Gabriel-Zisman
localization (and then its exact kernel quotient) by the already
established independent rotation source and path functoriality.
A new Type-valued square constructor remembers the ORIGINAL
physical k/l/polygon witnesses and retains distinct raw proof trees.

This is NOT the original historical F54/F55 high-order 3-cell or
a proved interchange/naturality 3-coherence between such squares.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
noncomputable section

/-- A genuine C60 local rotation square with two distinct TYPED
original source composites. The raw Site is not extended by a
fabricated direct arrow or a face-independent observation. -/
theorem polygonRotation_naturality_localized (p : Polygon)
    (k l : Nat) (hkl : k ≤ l) (hl : l ≤ polygonSideCount p) :
    zigzagToLocalization
      (append
        (polygonRotationTransport p k l hkl hl)
        (polygonRotatedRawLoop p l hl)) =
    zigzagToLocalization
      (append
        (polygonRotatedRawLoop p k (Nat.le_trans hkl hl))
        (polygonRotationTransport p k l hkl hl)) := by
  rw [zigzagToLocalization_append, zigzagToLocalization_append,
    polygonRotatedRawLoop_localized_id p l hl,
    polygonRotatedRawLoop_localized_id p k (Nat.le_trans hkl hl),
    Category.comp_id, Category.id_comp]

/-- The same PHYSICAL rotation source comparison descends to
the exact localization kernel quotient, not a guessed phase map. -/
theorem polygonRotation_naturality_kernel (p : Polygon)
    (k l : Nat) (hkl : k ≤ l) (hl : l ≤ polygonSideCount p) :
    zigzagKernelQ.map
      (append
        (polygonRotationTransport p k l hkl hl)
        (polygonRotatedRawLoop p l hl)) =
    zigzagKernelQ.map
      (append
        (polygonRotatedRawLoop p k (Nat.le_trans hkl hl))
        (polygonRotationTransport p k l hkl hl)) :=
  (zigzagKernel_exact _ _).2
    (polygonRotation_naturality_localized p k l hkl hl)

/-- Freely generated Type-valued physically based rotation 2-squares,
with independent raw witnesses, inverse, vertical gluing and the two
actually TYPED whiskering/context operations. -/
inductive PolygonRotationSquare :
    {s t : Site} → Zigzag s t → Zigzag s t → Type where
  | ident {s t : Site} (q : Zigzag s t) : PolygonRotationSquare q q
  | physical (p : Polygon) (k l : Nat)
      (hkl : k ≤ l) (hl : l ≤ polygonSideCount p) :
      PolygonRotationSquare
        (append
          (polygonRotationTransport p k l hkl hl)
          (polygonRotatedRawLoop p l hl))
        (append
          (polygonRotatedRawLoop p k (Nat.le_trans hkl hl))
          (polygonRotationTransport p k l hkl hl))
  | inverse {s t : Site} {q r : Zigzag s t}
      (c : PolygonRotationSquare q r) : PolygonRotationSquare r q
  | vertical {s t : Site} {q r u : Zigzag s t}
      (c : PolygonRotationSquare q r)
      (d : PolygonRotationSquare r u) : PolygonRotationSquare q u
  | leftContext {r s t : Site} (h : Zigzag r s)
      {q u : Zigzag s t} (c : PolygonRotationSquare q u) :
      PolygonRotationSquare (append h q) (append h u)
  | rightContext {r s t : Site}
      {q u : Zigzag r s} (c : PolygonRotationSquare q u)
      (h : Zigzag s t) :
      PolygonRotationSquare (append q h) (append u h)

/-- Every freely composed genuine physical rotation square has a
proved interpretation in the exact original F69 localization.
No exchange axiom, Gray charge, or global F55 3-cell is imported. -/
theorem PolygonRotationSquare.localized_sound
    {s t : Site} {q r : Zigzag s t} (c : PolygonRotationSquare q r) :
    zigzagToLocalization q = zigzagToLocalization r := by
  induction c with
  | ident q => rfl
  | physical p k l hkl hl =>
      exact polygonRotation_naturality_localized p k l hkl hl
  | inverse c ih => exact ih.symm
  | vertical c d ihc ihd => exact ihc.trans ihd
  | leftContext h c ih =>
      simpa only [zigzagToLocalization_append] using
        congrArg (fun x => zigzagToLocalization h ≫ x) ih
  | rightContext c h ih =>
      simpa only [zigzagToLocalization_append] using
        congrArg (fun x => x ≫ zigzagToLocalization h) ih

theorem PolygonRotationSquare.kernel_sound
    {s t : Site} {q r : Zigzag s t} (c : PolygonRotationSquare q r) :
    zigzagKernelQ.map q = zigzagKernelQ.map r :=
  (zigzagKernel_exact q r).2 c.localized_sound

/-- Actual Type-valued C60 source term attached to each permitted
oriented change of cyclic polygon basepoint. -/
def polygonRotationSquare (p : Polygon)
    (k l : Nat) (hkl : k ≤ l) (hl : l ≤ polygonSideCount p) :
    PolygonRotationSquare
      (append
        (polygonRotationTransport p k l hkl hl)
        (polygonRotatedRawLoop p l hl))
      (append
        (polygonRotatedRawLoop p k (Nat.le_trans hkl hl))
        (polygonRotationTransport p k l hkl hl)) :=
  .physical p k l hkl hl

def polygonRotationSquareWithUnit (p : Polygon)
    (k l : Nat) (hkl : k ≤ l) (hl : l ≤ polygonSideCount p) :
    PolygonRotationSquare
      (append
        (polygonRotationTransport p k l hkl hl)
        (polygonRotatedRawLoop p l hl))
      (append
        (polygonRotatedRawLoop p k (Nat.le_trans hkl hl))
        (polygonRotationTransport p k l hkl hl)) :=
  .vertical
    (.ident (append
      (polygonRotationTransport p k l hkl hl)
      (polygonRotatedRawLoop p l hl)))
    (.physical p k l hkl hl)

/-- Different proof trees survive at the raw source despite having
the same pair of original physical path boundaries. -/
theorem polygonRotationSquare_ne_withUnit (p : Polygon)
    (k l : Nat) (hkl : k ≤ l) (hl : l ≤ polygonSideCount p) :
    polygonRotationSquare p k l hkl hl ≠
      polygonRotationSquareWithUnit p k l hkl hl := by
  intro h
  cases h

/-- A concrete real north pentagon F54-like rotation source square:
the two base darts are endpoints of its FIRST genuine around-edge. -/
def northPentagonFirstRotationSquare :
    PolygonRotationSquare
      (append
        (polygonRotationTransport (.pentagon .north) 0 1
          (by decide) (by decide))
        (polygonRotatedRawLoop (.pentagon .north) 1 (by decide)))
      (append
        (polygonRotatedRawLoop (.pentagon .north) 0 (by decide))
        (polygonRotationTransport (.pentagon .north) 0 1
          (by decide) (by decide))) :=
  .physical (.pentagon .north) 0 1 (by decide) (by decide)

#print axioms polygonRotation_naturality_localized
#print axioms polygonRotation_naturality_kernel
#print axioms PolygonRotationSquare.localized_sound
#print axioms PolygonRotationSquare.kernel_sound
#print axioms polygonRotationSquare_ne_withUnit
#print axioms northPentagonFirstRotationSquare
end
end Kuu.F112.Physical
