import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGKStructuralSeamCode

/-!
# F112-P94D3GK — typed original P92B naturality generator atoms

NativeF55P92AssocComparison is a DISTINCT P92B extension:
it contains the genuine original nine-constructor F55 proofs and
an explicitly ADJOINED associator-naturality generator. The original
F55 nine-constructor proof never implicitly implies P92 naturality.
In the P94 structural extension, a third independently tagged
NativeF54StructuralSeam constructor is adjoined.

The genuine P92B primitive source below retains all six F45 trees
at three independent two-axis stages, all four distinct Blocks
boundaries per axis, all twelve Nat depth indices, and the actual
three Type-valued original F54 DepthRotationRoute proofs.

General Countable results explicitly assume BOTH D/E objects AND
every real categorical Hom fiber are Countable; true C60 Site×Site
satisfies these through GE/GI. No arbitrary Hom or old F55 filler is
inferred. Other recursive P92B constructors and structural seam
original Type-valued Countable are separate further obligations.

Append-only; 107 public roots; no Gray; original P92 no-go retained.
Pinned Lean v4.30.0-rc2 and mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section
universe uD vD uE vE

/-- FULL legitimate associator-naturality primitive of the P92B
extension, with all six original F45 trees and three ACTUAL raw F54
route histories, rather than one chosen shadow or scalar charge. -/
abbrev NativeGKP92NaturalityAtomTotal
    (p : Polygon)
    (D : Type uD) [Category.{vD} D]
    (E : Type uE) [Category.{vE} E] :
    Type (max (max uD uE) (max vD vE)) :=
  Σ a : D, Σ b : D, Σ x : E, Σ y : E,
  Σ p₀ : KuuNativeBlocks a b,
  Σ p₁ : KuuNativeBlocks a b,
  Σ p₂ : KuuNativeBlocks a b,
  Σ p₃ : KuuNativeBlocks a b,
  Σ q₀ : KuuNativeBlocks x y,
  Σ q₁ : KuuNativeBlocks x y,
  Σ q₂ : KuuNativeBlocks x y,
  Σ q₃ : KuuNativeBlocks x y,
  Σ n₁ : Nat, Σ n₁' : Nat,
  Σ n₂ : Nat, Σ n₂' : Nat,
  Σ n₃ : Nat, Σ n₃' : Nat,
  Σ m₁ : Nat, Σ m₁' : Nat,
  Σ m₂ : Nat, Σ m₂' : Nat,
  Σ m₃ : Nat, Σ m₃' : Nat,
  Σ firstBefore : KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁,
  Σ firstAfter : KuuNativeF45Tree p n₁' m₁' p₀ q₀ p₁ q₁,
  Σ secondBefore : KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂,
  Σ secondAfter : KuuNativeF45Tree p n₂' m₂' p₁ q₁ p₂ q₂,
  Σ thirdBefore : KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃,
  Σ thirdAfter : KuuNativeF45Tree p n₃' m₃' p₂ q₂ p₃ q₃,
    KuuNativeF45Tree.DepthRotationRoute p firstBefore firstAfter ×
    KuuNativeF45Tree.DepthRotationRoute p secondBefore secondAfter ×
    KuuNativeF45Tree.DepthRotationRoute p thirdBefore thirdAfter

/-- True P92B original source proof total on ACTUAL parallel
original F54 paths. This is distinct from the nine-constructor
PresentedCell total and the full P94 structural extension. -/
abbrev NativeGKOriginalP92Total
    (p : Polygon)
    (D : Type uD) [Category.{vD} D]
    (E : Type uE) [Category.{vE} E] :
    Type (max (max uD uE) (max vD vE)) :=
  Σ parallel : NativeGJOriginalParallelTotal p D E,
    NativeF55P92AssocComparison p parallel.1.2 parallel.2

/-- The exact P92B naturality primitive retains both actual
original P90 associator-naturality F54 route boundaries. -/
def nativeGKInterpretP92Naturality
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    (atom : NativeGKP92NaturalityAtomTotal p D E) :
    NativeGKOriginalP92Total p D E := by
  rcases atom with
    ⟨a, b, x, y, p₀, p₁, p₂, p₃, q₀, q₁, q₂, q₃,
      n₁, n₁', n₂, n₂', n₃, n₃',
      m₁, m₁', m₂, m₂', m₃, m₃',
      firstBefore, firstAfter, secondBefore, secondAfter,
      thirdBefore, thirdAfter, (u, v, w)⟩
  exact
    ⟨⟨nativeGJ2PackRoute (nativeF54P90AssocNaturalityLeftRoute u v w),
      nativeF54P90AssocNaturalityRightRoute u v w⟩,
      NativeF55P92AssocComparison.assocNaturality u v w⟩

/-- Countably many ACTUAL P92B naturality primitive proof inputs
under precisely explicit smallness of two input category objects
and EVERY original D/E Hom fiber. No P92B naturality quotient. -/
theorem nativeGKP92NaturalityAtomTotal_countable
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    (hobjD : Countable D)
    (hhomD : ∀ a b : D, Countable (a ⟶ b))
    (hobjE : Countable E)
    (hhomE : ∀ x y : E, Countable (x ⟶ y)) :
    Countable (NativeGKP92NaturalityAtomTotal p D E) := by
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
      nativeGHOriginalF45Fiber_countable hobjD hhomD hobjE hhomE
        n m ma mb pa pb
  letI : ∀ (a b : D) (x y : E)
      (ma mb : KuuNativeBlocks a b)
      (pa pb : KuuNativeBlocks x y)
      (n n' m m' : Nat)
      (first : KuuNativeF45Tree p n m ma pa mb pb)
      (last : KuuNativeF45Tree p n' m' ma pa mb pb),
      Countable (KuuNativeF45Tree.DepthRotationRoute p first last) :=
    fun _ _ _ _ _ _ _ _ _ _ _ _ first last =>
      nativeGIOriginalDepthFiber_countable
        hobjD hhomD hobjE hhomE first last
  infer_instance

/-- The complete image of the ACTUAL newly adjoined P92B primitive
inside its own original proof-relevant source total is Countable. -/
theorem nativeGKOriginalP92NaturalityImage_countable
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    (hobjD : Countable D)
    (hhomD : ∀ a b : D, Countable (a ⟶ b))
    (hobjE : Countable E)
    (hhomE : ∀ x y : E, Countable (x ⟶ y)) :
    (Set.range (nativeGKInterpretP92Naturality
      (p := p) (D := D) (E := E))).Countable := by
  letI : Countable (NativeGKP92NaturalityAtomTotal p D E) :=
    nativeGKP92NaturalityAtomTotal_countable hobjD hhomD hobjE hhomE
  exact Set.countable_range _

theorem nativeGKPhysicalP92NaturalityAtom_countable (p : Polygon) :
    Countable (NativeGKP92NaturalityAtomTotal p Site Site) :=
  nativeGKP92NaturalityAtomTotal_countable
    nativeC60GEPhysicalSite_countable
    nativeC60GEPhysicalIncidenceHom_countable
    nativeC60GEPhysicalSite_countable
    nativeC60GEPhysicalIncidenceHom_countable

theorem nativeGKPhysicalAllPolygonP92Atom_countable :
    Countable (Σ p : Polygon,
      NativeGKP92NaturalityAtomTotal p Site Site) := by
  letI : Countable Polygon := nativeC60GEPhysicalPolygon_countable
  letI : ∀ p : Polygon, Countable (NativeGKP92NaturalityAtomTotal p Site Site) :=
    nativeGKPhysicalP92NaturalityAtom_countable
  infer_instance

#print axioms nativeGKP92NaturalityAtomTotal_countable
#print axioms nativeGKInterpretP92Naturality
#print axioms nativeGKOriginalP92NaturalityImage_countable
#print axioms nativeGKPhysicalP92NaturalityAtom_countable
#print axioms nativeGKPhysicalAllPolygonP92Atom_countable

end
end Kuu.F112.Physical
