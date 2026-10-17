import Kuu.F112.PolygonNativeF54PentagonNaturality

/-!
# F112-E7Q5-F4-B — construct the F55 pentagon generator from boundary coherence

The previous F1 conditional map assumed a correctly typed mapped
pentagon 3-cell with raw pentagon constructor tag ONE. This module
isolates the genuinely smaller remaining geometric obligation:
strictly typed naturality of the two RAW F54 pentagon routes,
including every original pair of dependent Nat.add_assoc casts.

If both route equations are supplied, the existing FREE native
F55 pentagon constructor gives a genuine mapped 3-cell; its raw
shape tag ONE follows without any independent higher-cell data.
Thus the conditional target of E7Q5-F1 is obtained constructively
from two explicit F54 boundary equations. No charge equality, Gray
relation, or global 3-cell existence is used to manufacture a cell.

The proof is conditional on the two route equations. This file
does not claim that those equations hold for arbitrary category
functors, nor identify any frozen historical F55 source.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
noncomputable section

universe uA vA uB vB uA₂ vA₂ uB₂ vB₂
variable {A : Type uA} [Category.{vA} A]
variable {B : Type uB} [Category.{vB} B]
variable {A₂ : Type uA₂} [Category.{vA₂} A₂]
variable {B₂ : Type uB₂} [Category.{vB₂} B₂]

/-- The TWO exact raw F54 path equations that are required
to lift all native F55 pentagon generators along source functors.
These are propositions to be PROVED from actual dependent raw
transport, NOT newly introduced Lean axioms or universal laws. -/
structure KuuNativeF55PentagonBoundaryComparison
    (F : A ⥤ A₂) (G : B ⥤ B₂) where
  long :
    ∀ (p : Polygon) {a b : A} {x y : B}
      {n₁ n₂ n₃ n₄ m₁ m₂ m₃ m₄ : Nat}
      {p₀ p₁ p₂ p₃ p₄ : KuuNativeBlocks a b}
      {q₀ q₁ q₂ q₃ q₄ : KuuNativeBlocks x y}
      (t₁ : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁)
      (t₂ : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂)
      (t₃ : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃)
      (t₄ : KuuNativeF45Tree p n₄ m₄ p₃ q₃ p₄ q₄),
      (KuuNativeF45Tree.DepthRotationRoute.pentagonLong
        t₁ t₂ t₃ t₄).mapAxes F G =
      KuuNativeF45Tree.DepthRotationRoute.pentagonLong
        (t₁.mapAxes F G) (t₂.mapAxes F G)
        (t₃.mapAxes F G) (t₄.mapAxes F G)
  short :
    ∀ (p : Polygon) {a b : A} {x y : B}
      {n₁ n₂ n₃ n₄ m₁ m₂ m₃ m₄ : Nat}
      {p₀ p₁ p₂ p₃ p₄ : KuuNativeBlocks a b}
      {q₀ q₁ q₂ q₃ q₄ : KuuNativeBlocks x y}
      (t₁ : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁)
      (t₂ : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂)
      (t₃ : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃)
      (t₄ : KuuNativeF45Tree p n₄ m₄ p₃ q₃ p₄ q₄),
      (KuuNativeF45Tree.DepthRotationRoute.pentagonShort
        t₁ t₂ t₃ t₄).mapAxes F G =
      KuuNativeF45Tree.DepthRotationRoute.pentagonShort
        (t₁.mapAxes F G) (t₂.mapAxes F G)
        (t₃.mapAxes F G) (t₄.mapAxes F G)

/-- From TRUE F54 source boundary naturality, construct the
actual FREE F55 pentagon 3-cell with its raw constructor tag.
The cell does not arise from an observer's equality of charges. -/
def KuuNativeF55PentagonBoundaryComparison.lift
    (F : A ⥤ A₂) (G : B ⥤ B₂)
    (h : KuuNativeF55PentagonBoundaryComparison F G)
    (p : Polygon) {a b : A} {x y : B}
    {n₁ n₂ n₃ n₄ m₁ m₂ m₃ m₄ : Nat}
    {p₀ p₁ p₂ p₃ p₄ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ q₃ q₄ : KuuNativeBlocks x y}
    (t₁ : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁)
    (t₂ : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂)
    (t₃ : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃)
    (t₄ : KuuNativeF45Tree p n₄ m₄ p₃ q₃ p₄ q₄) :
    { cell : KuuNativeF45Tree.DepthRotationRoute.PresentedCell p
        ((KuuNativeF45Tree.DepthRotationRoute.pentagonLong
          t₁ t₂ t₃ t₄).mapAxes F G)
        ((KuuNativeF45Tree.DepthRotationRoute.pentagonShort
          t₁ t₂ t₃ t₄).mapAxes F G) //
      cell.shapeTag = 1 } := by
  rw [h.long p t₁ t₂ t₃ t₄, h.short p t₁ t₂ t₃ t₄]
  exact ⟨.pentagon (t₁.mapAxes F G) (t₂.mapAxes F G)
      (t₃.mapAxes F G) (t₄.mapAxes F G), rfl⟩

/-- Eliminate the conditional NEW higher-cell hypothesis using
only TWO exact raw F54 boundary equations. Neither raw shape nor
pentagon shadow calibration is postulated independently. -/
def KuuNativeF55PentagonBoundaryComparison.toMappedData
    (F : A ⥤ A₂) (G : B ⥤ B₂)
    (h : KuuNativeF55PentagonBoundaryComparison F G) :
    KuuNativeF55MappedPentagonData F G where
  pentagon := fun p {_a _b} {_x _y}
      {_n₁ _n₂ _n₃ _n₄ _m₁ _m₂ _m₃ _m₄}
      {_p₀ _p₁ _p₂ _p₃ _p₄} {_q₀ _q₁ _q₂ _q₃ _q₄}
      t₁ t₂ t₃ t₄ =>
    (h.lift F G p t₁ t₂ t₃ t₄).1
  pentagonTag := fun p {_a _b} {_x _y}
      {_n₁ _n₂ _n₃ _n₄ _m₁ _m₂ _m₃ _m₄}
      {_p₀ _p₁ _p₂ _p₃ _p₄} {_q₀ _q₁ _q₂ _q₃ _q₄}
      t₁ t₂ t₃ t₄ =>
    (h.lift F G p t₁ t₂ t₃ t₄).2

/-- Consequently the already proved faithful third-level quotient
functor is constructed from the two stated source boundary equations,
rather than an independently assumed family of F55 3-cells. -/
def nativeF55ThreeFunctorOfBoundary
    (F : A ⥤ A₂) (G : B ⥤ B₂)
    (h : KuuNativeF55PentagonBoundaryComparison F G)
    {p : Polygon} {a b : A} {x y : B}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :
    (KuuNativeF45Tree.DepthRotationRoute p first last) ⥤
      (KuuNativeF45Tree.DepthRotationRoute p
        (first.mapAxes F G) (last.mapAxes F G)) :=
  nativeF55ThreeFunctorGivenPentagon F G (h.toMappedData F G) first last

#print axioms KuuNativeF55PentagonBoundaryComparison
#print axioms KuuNativeF55PentagonBoundaryComparison.lift
#print axioms KuuNativeF55PentagonBoundaryComparison.toMappedData
#print axioms nativeF55ThreeFunctorOfBoundary
end
end Kuu.F112.Physical
