import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGKP92AssocAtom

/-!
# F112-P94D3GK2 — genuine typed F54 seam primitive source atoms

Four distinct dependent primitive source types for the fourteen-
constructor original NativeF54StructuralSeam proof grammar:

* reassoc: three ACTUAL composable original F54 routes over four full
  F45 stage proofs sharing the same two-category Blocks boundaries;
* leftContextTrans: two composed original F54 routes and a later
  original typed F45 tree in the right binary context;
* rightContextTrans: an earlier typed F45 tree followed by two
  original source routes in the right binary context;
* adjacentTrees: two truly composable, distinct original F45
  proof objects, for the structural left/right context-unit atoms.

No weakening of the original D/E object, Hom, Blocks, Nat-depth or
actual Type-valued proof data, no shadow quotient or global coherence.

These primitive types are Countable only under explicitly Countable
D/E objects and ALL categorical Hom fibers. They are consumed by a
separate fourteen-constructor partial decoder and strict left inverse.

Append-only / 107 roots / no Gray. Copyright Hidetoshi Itakura /
板倉英俊. Lean v4.30.0-rc2 and pinned mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section
universe uD vD uE vE u v w z t h

/-- Three EXACT F54 routes linking four truly original dependent
F45 stages, preserving every intermediate stage proof. -/
abbrev NativeGK2ReassocAtom
    (p : Polygon)
    (D : Type uD) [Category.{vD} D]
    (E : Type uE) [Category.{vE} E] :
    Type (max (max uD uE) (max vD vE)) :=
  Σ a : D, Σ b : D, Σ x : E, Σ y : E,
  Σ ma : KuuNativeBlocks a b,
  Σ pa : KuuNativeBlocks x y,
  Σ mb : KuuNativeBlocks a b,
  Σ pb : KuuNativeBlocks x y,
  Σ n₁ : Nat, Σ n₂ : Nat, Σ n₃ : Nat, Σ n₄ : Nat,
  Σ m₁ : Nat, Σ m₂ : Nat, Σ m₃ : Nat, Σ m₄ : Nat,
  Σ t₁ : KuuNativeF45Tree p n₁ m₁ ma pa mb pb,
  Σ t₂ : KuuNativeF45Tree p n₂ m₂ ma pa mb pb,
  Σ t₃ : KuuNativeF45Tree p n₃ m₃ ma pa mb pb,
  Σ t₄ : KuuNativeF45Tree p n₄ m₄ ma pa mb pb,
    KuuNativeF45Tree.DepthRotationRoute p t₁ t₂ ×
    KuuNativeF45Tree.DepthRotationRoute p t₂ t₃ ×
    KuuNativeF45Tree.DepthRotationRoute p t₃ t₄

/-- Right F45 stage remains literally typed after two left
context F54 route steps, with BOTH Nat index families. -/
abbrev NativeGK2LeftContextTransAtom
    (p : Polygon)
    (D : Type uD) [Category.{vD} D]
    (E : Type uE) [Category.{vE} E] :
    Type (max (max uD uE) (max vD vE)) :=
  Σ a : D, Σ b : D, Σ x : E, Σ y : E,
  Σ ma : KuuNativeBlocks a b,
  Σ pa : KuuNativeBlocks x y,
  Σ mb : KuuNativeBlocks a b,
  Σ pb : KuuNativeBlocks x y,
  Σ mc : KuuNativeBlocks a b,
  Σ pc : KuuNativeBlocks x y,
  Σ n₁ : Nat, Σ n₂ : Nat, Σ n₃ : Nat,
  Σ m₁ : Nat, Σ m₂ : Nat, Σ m₃ : Nat,
  Σ k : Nat, Σ l : Nat,
  Σ t₁ : KuuNativeF45Tree p n₁ m₁ ma pa mb pb,
  Σ t₂ : KuuNativeF45Tree p n₂ m₂ ma pa mb pb,
  Σ t₃ : KuuNativeF45Tree p n₃ m₃ ma pa mb pb,
  Σ later : KuuNativeF45Tree p k l mb pb mc pc,
    KuuNativeF45Tree.DepthRotationRoute p t₁ t₂ ×
    KuuNativeF45Tree.DepthRotationRoute p t₂ t₃

/-- Left F45 stage remains literally typed while a two-edge
original F54 depth route is reassociated inside the right context. -/
abbrev NativeGK2RightContextTransAtom
    (p : Polygon)
    (D : Type uD) [Category.{vD} D]
    (E : Type uE) [Category.{vE} E] :
    Type (max (max uD uE) (max vD vE)) :=
  Σ a : D, Σ b : D, Σ x : E, Σ y : E,
  Σ ma : KuuNativeBlocks a b,
  Σ pa : KuuNativeBlocks x y,
  Σ mb : KuuNativeBlocks a b,
  Σ pb : KuuNativeBlocks x y,
  Σ mc : KuuNativeBlocks a b,
  Σ pc : KuuNativeBlocks x y,
  Σ k : Nat, Σ l : Nat,
  Σ n₁ : Nat, Σ n₂ : Nat, Σ n₃ : Nat,
  Σ m₁ : Nat, Σ m₂ : Nat, Σ m₃ : Nat,
  Σ earlier : KuuNativeF45Tree p k l ma pa mb pb,
  Σ t₁ : KuuNativeF45Tree p n₁ m₁ mb pb mc pc,
  Σ t₂ : KuuNativeF45Tree p n₂ m₂ mb pb mc pc,
  Σ t₃ : KuuNativeF45Tree p n₃ m₃ mb pb mc pc,
    KuuNativeF45Tree.DepthRotationRoute p t₁ t₂ ×
    KuuNativeF45Tree.DepthRotationRoute p t₂ t₃

/-- Two original directly composable Type-valued F45 proof trees
with separately stored D/E middle Blocks and independent Nat depths. -/
abbrev NativeGK2AdjacentTreesAtom
    (p : Polygon)
    (D : Type uD) [Category.{vD} D]
    (E : Type uE) [Category.{vE} E] :
    Type (max (max uD uE) (max vD vE)) :=
  Σ a : D, Σ b : D, Σ x : E, Σ y : E,
  Σ ma : KuuNativeBlocks a b,
  Σ pa : KuuNativeBlocks x y,
  Σ mb : KuuNativeBlocks a b,
  Σ pb : KuuNativeBlocks x y,
  Σ mc : KuuNativeBlocks a b,
  Σ pc : KuuNativeBlocks x y,
  Σ n : Nat, Σ m : Nat, Σ k : Nat, Σ l : Nat,
    KuuNativeF45Tree p n m ma pa mb pb ×
    KuuNativeF45Tree p k l mb pb mc pc

/-- Strictly typed packed original 14-constructor structural seam
with two full original parallel F54 route boundaries. -/
abbrev NativeGK2OriginalSeamTotal
    (p : Polygon)
    (D : Type uD) [Category.{vD} D]
    (E : Type uE) [Category.{vE} E] :
    Type (max (max uD uE) (max vD vE)) :=
  Σ parallel : NativeGJOriginalParallelTotal p D E,
    NativeF54StructuralSeam p parallel.1.2 parallel.2

/-- Package the ORIGINAL typed 14-constructor structural seam
without any erase/quotient/observer and with full F54 routes. -/
def nativeGK2PackSeam
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (w : NativeF54StructuralSeam p r s) :
    NativeGK2OriginalSeamTotal p D E :=
  ⟨⟨nativeGJ2PackRoute r, s⟩, w⟩

/-- Typed real original F54 triple atom with no omitted Tree. -/
def nativeGK2PackReassoc
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {n₁ n₂ n₃ n₄ m₁ m₂ m₃ m₄ : Nat}
    {t₁ : KuuNativeF45Tree p n₁ m₁ ma pa mb pb}
    {t₂ : KuuNativeF45Tree p n₂ m₂ ma pa mb pb}
    {t₃ : KuuNativeF45Tree p n₃ m₃ ma pa mb pb}
    {t₄ : KuuNativeF45Tree p n₄ m₄ ma pa mb pb}
    (u : KuuNativeF45Tree.DepthRotationRoute p t₁ t₂)
    (v : KuuNativeF45Tree.DepthRotationRoute p t₂ t₃)
    (w : KuuNativeF45Tree.DepthRotationRoute p t₃ t₄) :
    NativeGK2ReassocAtom p D E :=
  ⟨a, b, x, y, ma, pa, mb, pb,
    n₁, n₂, n₃, n₄, m₁, m₂, m₃, m₄,
    t₁, t₂, t₃, t₄, (u, v, w)⟩

def nativeGK2PackLeftContextTrans
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    {ma mb mc : KuuNativeBlocks a b}
    {pa pb pc : KuuNativeBlocks x y}
    {n₁ n₂ n₃ m₁ m₂ m₃ k l : Nat}
    {t₁ : KuuNativeF45Tree p n₁ m₁ ma pa mb pb}
    {t₂ : KuuNativeF45Tree p n₂ m₂ ma pa mb pb}
    {t₃ : KuuNativeF45Tree p n₃ m₃ ma pa mb pb}
    (u : KuuNativeF45Tree.DepthRotationRoute p t₁ t₂)
    (v : KuuNativeF45Tree.DepthRotationRoute p t₂ t₃)
    (later : KuuNativeF45Tree p k l mb pb mc pc) :
    NativeGK2LeftContextTransAtom p D E :=
  ⟨a, b, x, y, ma, pa, mb, pb, mc, pc,
    n₁, n₂, n₃, m₁, m₂, m₃, k, l,
    t₁, t₂, t₃, later, (u, v)⟩

def nativeGK2PackRightContextTrans
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    {ma mb mc : KuuNativeBlocks a b}
    {pa pb pc : KuuNativeBlocks x y}
    {k l n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
    (earlier : KuuNativeF45Tree p k l ma pa mb pb)
    {t₁ : KuuNativeF45Tree p n₁ m₁ mb pb mc pc}
    {t₂ : KuuNativeF45Tree p n₂ m₂ mb pb mc pc}
    {t₃ : KuuNativeF45Tree p n₃ m₃ mb pb mc pc}
    (u : KuuNativeF45Tree.DepthRotationRoute p t₁ t₂)
    (v : KuuNativeF45Tree.DepthRotationRoute p t₂ t₃) :
    NativeGK2RightContextTransAtom p D E :=
  ⟨a, b, x, y, ma, pa, mb, pb, mc, pc,
    k, l, n₁, n₂, n₃, m₁, m₂, m₃,
    earlier, t₁, t₂, t₃, (u, v)⟩

def nativeGK2PackAdjacentTrees
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    {ma mb mc : KuuNativeBlocks a b}
    {pa pb pc : KuuNativeBlocks x y}
    {n m k l : Nat}
    (earlier : KuuNativeF45Tree p n m ma pa mb pb)
    (later : KuuNativeF45Tree p k l mb pb mc pc) :
    NativeGK2AdjacentTreesAtom p D E :=
  ⟨a, b, x, y, ma, pa, mb, pb, mc, pc,
    n, m, k, l, (earlier, later)⟩

/-- Countable all original F45/route dependent proof fibers once
both input categories satisfy explicit objects and each Hom smallness. -/
private theorem nativeGK2OriginalInputCountable
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    (hobjD : Countable D)
    (hhomD : ∀ a b : D, Countable (a ⟶ b))
    (hobjE : Countable E)
    (hhomE : ∀ x y : E, Countable (x ⟶ y)) :
    Countable (NativeGK2AdjacentTreesAtom p D E) := by
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
  infer_instance

/-- The three original route steps of a true 4-stage reassociation
have a Countable complete proof-bearing Type-valued source. -/
theorem nativeGK2ReassocAtom_countable
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    (hobjD : Countable D)
    (hhomD : ∀ a b : D, Countable (a ⟶ b))
    (hobjE : Countable E)
    (hhomE : ∀ x y : E, Countable (x ⟶ y)) :
    Countable (NativeGK2ReassocAtom p D E) := by
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
      nativeGIOriginalDepthFiber_countable hobjD hhomD hobjE hhomE
        first last
  infer_instance

/-- Both original F54 routes and original later context proof. -/
theorem nativeGK2LeftContextTransAtom_countable
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    (hobjD : Countable D)
    (hhomD : ∀ a b : D, Countable (a ⟶ b))
    (hobjE : Countable E)
    (hhomE : ∀ x y : E, Countable (x ⟶ y)) :
    Countable (NativeGK2LeftContextTransAtom p D E) := by
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
      nativeGIOriginalDepthFiber_countable hobjD hhomD hobjE hhomE
        first last
  infer_instance

/-- Both original F54 routes and original earlier context proof. -/
theorem nativeGK2RightContextTransAtom_countable
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    (hobjD : Countable D)
    (hhomD : ∀ a b : D, Countable (a ⟶ b))
    (hobjE : Countable E)
    (hhomE : ∀ x y : E, Countable (x ⟶ y)) :
    Countable (NativeGK2RightContextTransAtom p D E) := by
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
      nativeGIOriginalDepthFiber_countable hobjD hhomD hobjE hhomE
        first last
  infer_instance

theorem nativeGK2AdjacentTreesAtom_countable
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    (hobjD : Countable D)
    (hhomD : ∀ a b : D, Countable (a ⟶ b))
    (hobjE : Countable E)
    (hhomE : ∀ x y : E, Countable (x ⟶ y)) :
    Countable (NativeGK2AdjacentTreesAtom p D E) :=
  nativeGK2OriginalInputCountable hobjD hhomD hobjE hhomE

#print axioms nativeGK2ReassocAtom_countable
#print axioms nativeGK2LeftContextTransAtom_countable
#print axioms nativeGK2RightContextTransAtom_countable
#print axioms nativeGK2AdjacentTreesAtom_countable

end
end Kuu.F112.Physical
