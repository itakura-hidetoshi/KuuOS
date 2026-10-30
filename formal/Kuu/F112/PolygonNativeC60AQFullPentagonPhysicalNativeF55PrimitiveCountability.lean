import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeDepthRouteFullCountability
import Kuu.F112.PolygonNativeF55Presented

/-!
# F112-P94D3GJ — genuine native F55 primitive Type-valued atom countability

GI proves the complete original five-constructor F54-shaped
DepthRotationRoute source total/fiber Countable under explicitly
countable input category objects and every actual category Hom.
GJ begins with the next truly proof-relevant original-shaped source:
parallel original F54 routes and the two TRUE primitive independent
F55 3-cell generator tokens, pentagon and disjointSquare.

All four genuine typed pentagon F45 stages, all five independent
intermediate D/E block presentations and eight Nat indices are
retained. The disjoint square stores both real LocalRotation proofs,
their dependent F45 endpoints, independent grades and three D/E block
boundaries. These are not reduced to rotation counts or observer
classes. Constructor-faithful primitive interpretations land in the
ACTUAL nine-constructor PresentedCell source, retaining full source
and target parallel route witnesses.

The remaining seven recursive constructors will be treated next as
separate original Type-valued dependent syntax. This file neither
assumes its Countable conclusion nor infers old historical F55
equivalence, original 14D Countable, 19D filler or global coherence.

Append-only / same-root / strict Kuu primary / independent Kuu
one presentation / 107 public roots / no Gray reintroduction.
Pinned Lean v4.30.0-rc2; mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uD vD uE vE u v

/-- Two FULL original, genuinely parallel F54 route proofs.
The first independent route is already stored as the proof
component of NativeGIOriginalDepthTotal. The second route is
another true Type-valued proof on EXACTLY the same source boundary. -/
abbrev NativeGJOriginalParallelTotal (p : Polygon)
    (D : Type uD) [Category.{vD} D]
    (E : Type uE) [Category.{vE} E] :
    Type (max (max uD uE) (max vD vE)) :=
  Σ firstRoute : NativeGIOriginalDepthTotal p D E,
    KuuNativeF45Tree.DepthRotationRoute p
      firstRoute.1.first firstRoute.1.last

/-- The entire genuine nine-constructor independent F55 Type-valued
cell total, including BOTH actual original F54 route endpoints.
The countability of this entire source is NOT yet asserted here. -/
abbrev NativeGJOriginalPresentedTotal (p : Polygon)
    (D : Type uD) [Category.{vD} D]
    (E : Type uE) [Category.{vE} E] :
    Type (max (max uD uE) (max vD vE)) :=
  Σ parallel : NativeGJOriginalParallelTotal p D E,
    KuuNativeF45Tree.DepthRotationRoute.PresentedCell p
      parallel.1.2 parallel.2

/-- Package an ACTUAL original PresentedCell with all its typed
two-category block, F45 tree, depth and parallel F54 route indices. -/
def nativeGJPackPresented
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (cell : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p r s) :
    NativeGJOriginalPresentedTotal p D E :=
  ⟨⟨⟨⟨a, b, x, y, ma, pa, mb, pb, n, n', m, m',
      first, last⟩, r⟩, s⟩, cell⟩

/-- The ORIGINAL four consecutive F45 source terms of the
pentagon generator, with EVERY independent intermediate block,
both individual axis depths and ALL original Type-valued histories. -/
abbrev NativeGJPentagonAtomTotal (p : Polygon)
    (D : Type uD) [Category.{vD} D]
    (E : Type uE) [Category.{vE} E] :
    Type (max (max uD uE) (max vD vE)) :=
  Σ a : D, Σ b : D, Σ x : E, Σ y : E,
  Σ p₀ : KuuNativeBlocks a b,
  Σ p₁ : KuuNativeBlocks a b,
  Σ p₂ : KuuNativeBlocks a b,
  Σ p₃ : KuuNativeBlocks a b,
  Σ p₄ : KuuNativeBlocks a b,
  Σ q₀ : KuuNativeBlocks x y,
  Σ q₁ : KuuNativeBlocks x y,
  Σ q₂ : KuuNativeBlocks x y,
  Σ q₃ : KuuNativeBlocks x y,
  Σ q₄ : KuuNativeBlocks x y,
  Σ n₁ : Nat, Σ m₁ : Nat,
  Σ n₂ : Nat, Σ m₂ : Nat,
  Σ n₃ : Nat, Σ m₃ : Nat,
  Σ n₄ : Nat, Σ m₄ : Nat,
    KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁ ×
    KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂ ×
    KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃ ×
    KuuNativeF45Tree p n₄ m₄ p₃ q₃ p₄ q₄

/-- The TRUE original two-rotation disjointSquare source, retaining
the four independent F45 before/after terms, original two Type-valued
LocalRotation proofs and three intermediate independent Blocks. -/
abbrev NativeGJSquareAtomTotal (p : Polygon)
    (D : Type uD) [Category.{vD} D]
    (E : Type uE) [Category.{vE} E] :
    Type (max (max uD uE) (max vD vE)) :=
  Σ a : D, Σ b : D, Σ x : E, Σ y : E,
  Σ p₀ : KuuNativeBlocks a b,
  Σ p₁ : KuuNativeBlocks a b,
  Σ p₂ : KuuNativeBlocks a b,
  Σ q₀ : KuuNativeBlocks x y,
  Σ q₁ : KuuNativeBlocks x y,
  Σ q₂ : KuuNativeBlocks x y,
  Σ n : Nat, Σ m : Nat, Σ n' : Nat, Σ m' : Nat,
  Σ lb : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁,
  Σ la : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁,
  Σ rb : KuuNativeF45Tree p n' m' p₁ q₁ p₂ q₂,
  Σ ra : KuuNativeF45Tree p n' m' p₁ q₁ p₂ q₂,
    KuuNativeF45Tree.LocalRotation p lb la ×
    KuuNativeF45Tree.LocalRotation p rb ra

/-- Only TWO primitive F55 generator kinds. Every atom is an
actual complete source proof with arbitrary depths and categories,
not a symbolic label or a scalar shadow. -/
inductive NativeGJPrimitiveF55PlainSyntax
    (Pentagon : Type u) (Square : Type v) : Type (max u v) where
  | pentagon (source : Pentagon)
  | disjointSquare (source : Square)
  deriving Countable

/-- Genuine full source countability of all original parallel F54
route boundaries, before constructing ANY new F55 raw cells. -/
theorem nativeGJOriginalParallelTotal_countable
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    (hobjD : Countable D)
    (hhomD : ∀ a b : D, Countable (a ⟶ b))
    (hobjE : Countable E)
    (hhomE : ∀ x y : E, Countable (x ⟶ y)) :
    Countable (NativeGJOriginalParallelTotal p D E) := by
  letI : Countable (NativeGIOriginalDepthTotal p D E) :=
    nativeGIOriginalDepthTotal_countable hobjD hhomD hobjE hhomE
  letI : ∀ firstRoute : NativeGIOriginalDepthTotal p D E,
      Countable (KuuNativeF45Tree.DepthRotationRoute p
        firstRoute.1.first firstRoute.1.last) := by
    intro firstRoute
    rcases firstRoute with
      ⟨⟨a, b, x, y, ma, pa, mb, pb, n, n', m, m', first, last⟩, route⟩
    exact nativeGIOriginalDepthFiber_countable
      hobjD hhomD hobjE hhomE first last
  infer_instance

/-- Countably many ACTUAL four-stage original F55 pentagon inputs,
using GH F45 Type-valued source Countable, not a number of sectors. -/
theorem nativeGJPentagonAtomTotal_countable
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    (hobjD : Countable D)
    (hhomD : ∀ a b : D, Countable (a ⟶ b))
    (hobjE : Countable E)
    (hhomE : ∀ x y : E, Countable (x ⟶ y)) :
    Countable (NativeGJPentagonAtomTotal p D E) := by
  letI : Countable D := hobjD
  letI : Countable E := hobjE
  letI : ∀ a b : D, Countable (KuuNativeBlocks a b) :=
    nativeGFOriginalBlocksFiber_countable hobjD hhomD
  letI : ∀ x y : E, Countable (KuuNativeBlocks x y) :=
    nativeGFOriginalBlocksFiber_countable hobjE hhomE
  letI : ∀ (a b : D) (x y : E)
      (n m : Nat) (ma mb : KuuNativeBlocks a b)
      (pa pb : KuuNativeBlocks x y),
      Countable (KuuNativeF45Tree p n m ma pa mb pb) :=
    fun _ _ _ _ n m ma mb pa pb =>
      nativeGHOriginalF45Fiber_countable
        hobjD hhomD hobjE hhomE n m ma mb pa pb
  infer_instance

/-- Countably many ACTUAL disjoint square generator inputs,
including both original independent LocalRotation proofs. -/
theorem nativeGJSquareAtomTotal_countable
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    (hobjD : Countable D)
    (hhomD : ∀ a b : D, Countable (a ⟶ b))
    (hobjE : Countable E)
    (hhomE : ∀ x y : E, Countable (x ⟶ y)) :
    Countable (NativeGJSquareAtomTotal p D E) := by
  letI : Countable D := hobjD
  letI : Countable E := hobjE
  letI : ∀ a b : D, Countable (KuuNativeBlocks a b) :=
    nativeGFOriginalBlocksFiber_countable hobjD hhomD
  letI : ∀ x y : E, Countable (KuuNativeBlocks x y) :=
    nativeGFOriginalBlocksFiber_countable hobjE hhomE
  letI : ∀ (a b : D) (x y : E)
      (n m : Nat) (ma mb : KuuNativeBlocks a b)
      (pa pb : KuuNativeBlocks x y),
      Countable (KuuNativeF45Tree p n m ma pa mb pb) :=
    fun _ _ _ _ n m ma mb pa pb =>
      nativeGHOriginalF45Fiber_countable
        hobjD hhomD hobjE hhomE n m ma mb pa pb
  letI : ∀ (a b : D) (x y : E)
      (n m : Nat) (ma mb : KuuNativeBlocks a b)
      (pa pb : KuuNativeBlocks x y)
      (before after : KuuNativeF45Tree p n m ma pa mb pb),
      Countable (KuuNativeF45Tree.LocalRotation p before after) :=
    fun _ _ _ _ _ _ _ _ _ _ before after =>
      nativeGIOriginalLocalFiber_countable
        hobjD hhomD hobjE hhomE before after
  infer_instance

/-- Both genuinely typed primitive F55 source alphabets form a
countable free finite-code input, BEFORE closing seven operations. -/
theorem nativeGJPrimitiveF55PlainSyntax_countable
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    (hobjD : Countable D)
    (hhomD : ∀ a b : D, Countable (a ⟶ b))
    (hobjE : Countable E)
    (hhomE : ∀ x y : E, Countable (x ⟶ y)) :
    Countable (NativeGJPrimitiveF55PlainSyntax
      (NativeGJPentagonAtomTotal p D E)
      (NativeGJSquareAtomTotal p D E)) := by
  letI : Countable (NativeGJPentagonAtomTotal p D E) :=
    nativeGJPentagonAtomTotal_countable hobjD hhomD hobjE hhomE
  letI : Countable (NativeGJSquareAtomTotal p D E) :=
    nativeGJSquareAtomTotal_countable hobjD hhomD hobjE hhomE
  infer_instance

/-- This is an actual fully typed source *primitive* F55
generator, not an arbitrary F55 3-cell assertion. Both
type-valued parallel routes are stored in the result. -/
def nativeGJInterpretPentagon
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    (source : NativeGJPentagonAtomTotal p D E) :
    NativeGJOriginalPresentedTotal p D E := by
  rcases source with
    ⟨a, b, x, y, p₀, p₁, p₂, p₃, p₄,
      q₀, q₁, q₂, q₃, q₄,
      n₁, m₁, n₂, m₂, n₃, m₃, n₄, m₄,
      t₁, t₂, t₃, t₄⟩
  exact nativeGJPackPresented
    (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.pentagon
      t₁ t₂ t₃ t₄)

/-- A second actually typed primitive, constructed from two
genuine independent LocalRotation proofs and their exact boundaries. -/
def nativeGJInterpretSquare
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    (source : NativeGJSquareAtomTotal p D E) :
    NativeGJOriginalPresentedTotal p D E := by
  rcases source with
    ⟨a, b, x, y, p₀, p₁, p₂, q₀, q₁, q₂,
      n, m, n', m', lb, la, rb, ra, left, right⟩
  exact nativeGJPackPresented
    (KuuNativeF45Tree.DepthRotationRoute.PresentedCell.disjointSquare
      left right)

/-- Constructor-faithful interpretation of BOTH primitive source
alphabets into the actual free, nine-constructor F55 source Total. -/
def nativeGJInterpretPrimitive
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] :
    NativeGJPrimitiveF55PlainSyntax
      (NativeGJPentagonAtomTotal p D E)
      (NativeGJSquareAtomTotal p D E) →
    NativeGJOriginalPresentedTotal p D E
  | .pentagon source => nativeGJInterpretPentagon source
  | .disjointSquare source => nativeGJInterpretSquare source

/-- The TRUE original primitive F55 source image is countable
without making ANY assertion about the remaining seven constructors. -/
theorem nativeGJOriginalPrimitiveImage_countable
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    (hobjD : Countable D)
    (hhomD : ∀ a b : D, Countable (a ⟶ b))
    (hobjE : Countable E)
    (hhomE : ∀ x y : E, Countable (x ⟶ y)) :
    (Set.range (nativeGJInterpretPrimitive (p := p) (D := D) (E := E))).Countable := by
  letI : Countable (NativeGJPrimitiveF55PlainSyntax
      (NativeGJPentagonAtomTotal p D E)
      (NativeGJSquareAtomTotal p D E)) :=
    nativeGJPrimitiveF55PlainSyntax_countable hobjD hhomD hobjE hhomE
  exact Set.countable_range _

/-- Physical C60 parallel route total, with both genuinely typed
independent Site axis proofs: unconditional Countable. -/
theorem nativeGJPhysicalParallelTotal_countable (p : Polygon) :
    Countable (NativeGJOriginalParallelTotal p Site Site) :=
  nativeGJOriginalParallelTotal_countable
    nativeC60GEPhysicalSite_countable
    nativeC60GEPhysicalIncidenceHom_countable
    nativeC60GEPhysicalSite_countable
    nativeC60GEPhysicalIncidenceHom_countable

/-- The exact primitive F55 source symbols on the genuine finite
C60 Site category have unconditional countability. -/
theorem nativeGJPhysicalPrimitiveCountable (p : Polygon) :
    Countable (NativeGJPrimitiveF55PlainSyntax
      (NativeGJPentagonAtomTotal p Site Site)
      (NativeGJSquareAtomTotal p Site Site)) :=
  nativeGJPrimitiveF55PlainSyntax_countable
    nativeC60GEPhysicalSite_countable
    nativeC60GEPhysicalIncidenceHom_countable
    nativeC60GEPhysicalSite_countable
    nativeC60GEPhysicalIncidenceHom_countable

/-- Every true C60 Polygon carries countably many fully typed
native F55 pentagon/square primitive source witnesses. -/
theorem nativeGJPhysicalAllPolygonPrimitive_countable :
    Countable (Σ p : Polygon,
      NativeGJPrimitiveF55PlainSyntax
        (NativeGJPentagonAtomTotal p Site Site)
        (NativeGJSquareAtomTotal p Site Site)) := by
  letI : Countable Polygon := nativeC60GEPhysicalPolygon_countable
  letI : ∀ p : Polygon, Countable (NativeGJPrimitiveF55PlainSyntax
      (NativeGJPentagonAtomTotal p Site Site)
      (NativeGJSquareAtomTotal p Site Site)) :=
    nativeGJPhysicalPrimitiveCountable
  infer_instance

#print axioms nativeGJOriginalParallelTotal_countable
#print axioms nativeGJPentagonAtomTotal_countable
#print axioms nativeGJSquareAtomTotal_countable
#print axioms nativeGJPrimitiveF55PlainSyntax_countable
#print axioms nativeGJInterpretPentagon
#print axioms nativeGJInterpretSquare
#print axioms nativeGJInterpretPrimitive
#print axioms nativeGJOriginalPrimitiveImage_countable
#print axioms nativeGJPhysicalParallelTotal_countable
#print axioms nativeGJPhysicalPrimitiveCountable
#print axioms nativeGJPhysicalAllPolygonPrimitive_countable

end
end Kuu.F112.Physical
