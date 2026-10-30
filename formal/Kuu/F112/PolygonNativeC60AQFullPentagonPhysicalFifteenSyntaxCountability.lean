import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalLowerAXCountability

/-!
# F112-P94D3GD — actual original indexed 15D Countable from 14D

GC discharged the independent Countable hypothesis for all genuine
original K5 primitive AX generator fibers, leaving just Countable
of the ORIGINAL AX base total, including all genuine 14D and 15D
Type-valued proof witnesses.

GD faithfully reifies the actual observer-conservative 15D proof
grammar atom/refl/symm/trans and the actual independent indexed
15D grammar conservative/exchange/symm/trans.

The lower atom code retains both original endpoints and their
exact proposition-valued observer equalities. The higher
conservative token stores the entire ORIGINAL lower 15D raw
proof with its genuine endpoints. The independent exchange
retains its original List Bool index. Partial dependent decoders
reject ill-typed compositions, and decode after encode is the
original proof, for arbitrary finite nesting.

No quotient, scalar shadow, truncation, new axiom or 19D filler
is used. No assumption that arbitrary source-category Hom or
original 14D witness fibers are automatically Countable.
The independent Kuu presentation is retained; strict Kuu is
primary. Lean v4.30.0-rc2, pinned mathlib, append-only 107 roots.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical

open CategoryTheory Cardinal
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u v w uD vD uE vE

/-- The complete primitive conservative 15D token. Only its two
equality proofs live in Prop; original object endpoint Types and
raw proof constructor histories are never quotiented. -/
abbrev NativeC60GDCoreAtomTotal
    {A : Type u} {H : Type v}
    (history : A → H) (charge : A → ℤ) : Type u :=
  { ep : A × A //
    history ep.1 = history ep.2 ∧ charge ep.1 = charge ep.2 }

/-- The original entire indexed observer-conservative 15D
proof total, NOT its quotient or free-word history observer. -/
abbrev NativeC60GDOriginalCoreTotal
    {A : Type u} {H : Type v}
    (history : A → H) (charge : A → ℤ) : Type (max u v) :=
  Σ ep : A × A,
    NativeObserverCoreFifteenCell history charge ep.1 ep.2

/-- The old GA finite raw syntax is reused, but its atoms here
are the true complete observer-compatible primitive tokens. -/
def nativeC60GDEncodeCore
    {A : Type u} {H : Type v}
    (history : A → H) (charge : A → ℤ) :
    {x y : A} → NativeObserverCoreFifteenCell history charge x y →
      NativeC60GAPlainRawSyntax (NativeC60GDCoreAtomTotal history charge) A
  | x, y, .atom hword hcharge => .atom ⟨(x, y), ⟨hword, hcharge⟩⟩
  | _, _, .refl x => .refl x
  | _, _, .symm h => .symm (nativeC60GDEncodeCore history charge h)
  | _, _, .trans h k =>
      .trans (nativeC60GDEncodeCore history charge h)
        (nativeC60GDEncodeCore history charge k)

/-- Decode only genuinely composable core raw proofs, retaining
all original source and target objects and observer-compatible
atom proof evidence. -/
noncomputable def nativeC60GDDecodeCore
    {A : Type u} {H : Type v}
    (history : A → H) (charge : A → ℤ) :
    NativeC60GAPlainRawSyntax (NativeC60GDCoreAtomTotal history charge) A →
      Option (NativeC60GDOriginalCoreTotal history charge)
  | .atom atom =>
      some ⟨atom.1, .atom atom.2.1 atom.2.2⟩
  | .refl x => some ⟨(x, x), .refl x⟩
  | .symm h =>
      (nativeC60GDDecodeCore history charge h).bind
        (fun ⟨⟨x, y⟩, p⟩ => some ⟨(y, x), .symm p⟩)
  | .trans h k => by
      classical
      exact (nativeC60GDDecodeCore history charge h).bind
        (fun ⟨⟨x, y⟩, p⟩ =>
          (nativeC60GDDecodeCore history charge k).bind
            (fun ⟨⟨z, w⟩, q⟩ =>
              if hz : y = z then
                some ⟨(x, w), .trans p (hz.symm ▸ q)⟩
              else none))

/-- Exact dependent original core proof reification, including
arbitrary nested symmetries, compositions, endpoints, and the
original hword/hcharge proof objects (which are Props). -/
theorem nativeC60GDDecode_encodeCore
    {A : Type u} {H : Type v}
    (history : A → H) (charge : A → ℤ)
    {x y : A} (p : NativeObserverCoreFifteenCell history charge x y) :
    nativeC60GDDecodeCore history charge (nativeC60GDEncodeCore history charge p) =
      some (⟨(x, y), p⟩ : NativeC60GDOriginalCoreTotal history charge) := by
  induction p with
  | atom hword hcharge =>
      simp [nativeC60GDEncodeCore, nativeC60GDDecodeCore]
  | refl a => rfl
  | symm h ih =>
      simp [nativeC60GDDecodeCore, nativeC60GDEncodeCore, ih]
  | trans h k ih ik =>
      simp [nativeC60GDDecodeCore, nativeC60GDEncodeCore, ih, ik]

/-- The original full Type-valued conservative 15D proof total
is Countable when the original 14D object alphabet is Countable.
No Countable assumption on the observer target H is needed:
its equality evidence is proposition-valued. -/
theorem nativeC60GDOriginalCoreTotal_countable
    {A : Type u} {H : Type v}
    (history : A → H) (charge : A → ℤ)
    (hA : Countable A) :
    Countable (NativeC60GDOriginalCoreTotal history charge) := by
  letI : Countable A := hA
  haveI : Countable (NativeC60GDCoreAtomTotal history charge) :=
    inferInstance
  haveI : Countable
      (NativeC60GAPlainRawSyntax (NativeC60GDCoreAtomTotal history charge) A) :=
    inferInstance
  have hrange :
      (Set.range (nativeC60GDDecodeCore history charge)).Countable :=
    Set.countable_range _
  letI : Countable (Set.range (nativeC60GDDecodeCore history charge)) :=
    hrange.to_subtype
  let embedding : NativeC60GDOriginalCoreTotal history charge →
      Set.range (nativeC60GDDecodeCore history charge) :=
    fun t =>
      ⟨some t, by
        rcases t with ⟨⟨x, y⟩, p⟩
        exact ⟨nativeC60GDEncodeCore history charge p,
          nativeC60GDDecode_encodeCore history charge p⟩⟩
  have hinj : Function.Injective embedding := by
    intro t t' h
    have hsome :
        (some t : Option (NativeC60GDOriginalCoreTotal history charge)) = some t' :=
      congrArg
        (fun z : Set.range (nativeC60GDDecodeCore history charge) => z.1) h
    exact Option.some.inj hsome
  exact hinj.countable

/-- Countable finite code for genuine original indexed 15D
conservative/exchange/symm/trans syntax. Each conservative
atom retains its entire ORIGINAL lower core 15D proof;
exchange retains its original chosen index. -/
inductive NativeC60GDPlainFamilySyntax
    (CoreAtom : Type u) (I : Type w) : Type (max u w) where
  | conservative (h : CoreAtom)
  | exchange (i : I)
  | symm (h : NativeC60GDPlainFamilySyntax CoreAtom I)
  | trans (h k : NativeC60GDPlainFamilySyntax CoreAtom I)
  deriving Countable

/-- Genuine original dependent indexed family 15D proof total. -/
abbrev NativeC60GDOriginalFamilyTotal
    {A : Type u} {H : Type v} {I : Type w}
    (history : A → H) (charge : A → ℤ)
    (left right : I → A)
    (chargeEq : ∀ i : I, charge (left i) = charge (right i)) :
    Type (max (max u v) w) :=
  Σ ep : A × A,
    NativeFifteenFamilyCell history charge left right chargeEq ep.1 ep.2

/-- Encode the complete ORIGINAL indexed 15D proof by its
real conservative 15D proof tokens and exchange indices. -/
def nativeC60GDEncodeFamily
    {A : Type u} {H : Type v} {I : Type w}
    (history : A → H) (charge : A → ℤ)
    (left right : I → A)
    (chargeEq : ∀ i : I, charge (left i) = charge (right i)) :
    {x y : A} →
      NativeFifteenFamilyCell history charge left right chargeEq x y →
      NativeC60GDPlainFamilySyntax
        (NativeC60GDOriginalCoreTotal history charge) I
  | _, _, .conservative h => .conservative ⟨(_, _), h⟩
  | _, _, .exchange i => .exchange i
  | _, _, .symm h =>
      .symm (nativeC60GDEncodeFamily history charge left right chargeEq h)
  | _, _, .trans h k =>
      .trans (nativeC60GDEncodeFamily history charge left right chargeEq h)
        (nativeC60GDEncodeFamily history charge left right chargeEq k)

/-- Partial dependent decoder of the ORIGINAL indexed 15D
grammar. Uncomposable endpoints return none, with no forced
identification of Type-valued 14D/15D proof terms. -/
noncomputable def nativeC60GDDecodeFamily
    {A : Type u} {H : Type v} {I : Type w}
    (history : A → H) (charge : A → ℤ)
    (left right : I → A)
    (chargeEq : ∀ i : I, charge (left i) = charge (right i)) :
    NativeC60GDPlainFamilySyntax
        (NativeC60GDOriginalCoreTotal history charge) I →
      Option (NativeC60GDOriginalFamilyTotal history charge left right chargeEq)
  | .conservative ⟨⟨x, y⟩, h⟩ =>
      some ⟨(x, y), .conservative h⟩
  | .exchange i =>
      some ⟨(left i, right i), .exchange i⟩
  | .symm h =>
      (nativeC60GDDecodeFamily history charge left right chargeEq h).bind
        (fun ⟨⟨x, y⟩, p⟩ => some ⟨(y, x), .symm p⟩)
  | .trans h k => by
      classical
      exact (nativeC60GDDecodeFamily history charge left right chargeEq h).bind
        (fun ⟨⟨x, y⟩, p⟩ =>
          (nativeC60GDDecodeFamily history charge left right chargeEq k).bind
            (fun ⟨⟨z, w⟩, q⟩ =>
              if hz : y = z then
                some ⟨(x, w), .trans p (hz.symm ▸ q)⟩
              else none))

/-- Every original indexed dependent 15D proof is recovered
exactly after finite coding, for arbitrary recursive depth.
The conservative core proof and exchange index survive. -/
theorem nativeC60GDDecode_encodeFamily
    {A : Type u} {H : Type v} {I : Type w}
    (history : A → H) (charge : A → ℤ)
    (left right : I → A)
    (chargeEq : ∀ i : I, charge (left i) = charge (right i))
    {x y : A}
    (p : NativeFifteenFamilyCell history charge left right chargeEq x y) :
    nativeC60GDDecodeFamily history charge left right chargeEq
      (nativeC60GDEncodeFamily history charge left right chargeEq p) =
      some (⟨(x, y), p⟩ :
        NativeC60GDOriginalFamilyTotal history charge left right chargeEq) := by
  induction p with
  | conservative h => rfl
  | exchange i => rfl
  | symm h ih =>
      simp [nativeC60GDDecodeFamily, nativeC60GDEncodeFamily, ih]
  | trans h k ih ik =>
      simp [nativeC60GDDecodeFamily, nativeC60GDEncodeFamily, ih, ik]

/-- True original entire indexed 15D raw proof total is
Countable from only original A and exchange-index I Countable,
not from a countable scalar observation or quotient. -/
theorem nativeC60GDOriginalFamilyTotal_countable
    {A : Type u} {H : Type v} {I : Type w}
    (history : A → H) (charge : A → ℤ)
    (left right : I → A)
    (chargeEq : ∀ i : I, charge (left i) = charge (right i))
    (hA : Countable A) (hI : Countable I) :
    Countable
      (NativeC60GDOriginalFamilyTotal history charge left right chargeEq) := by
  letI : Countable I := hI
  letI : Countable (NativeC60GDOriginalCoreTotal history charge) :=
    nativeC60GDOriginalCoreTotal_countable history charge hA
  haveI : Countable (NativeC60GDPlainFamilySyntax
      (NativeC60GDOriginalCoreTotal history charge) I) :=
    inferInstance
  have hrange :
      (Set.range (nativeC60GDDecodeFamily history charge left right chargeEq)).Countable :=
    Set.countable_range _
  letI : Countable (Set.range
      (nativeC60GDDecodeFamily history charge left right chargeEq)) :=
    hrange.to_subtype
  let embedding :
      NativeC60GDOriginalFamilyTotal history charge left right chargeEq →
      Set.range (nativeC60GDDecodeFamily history charge left right chargeEq) :=
    fun t =>
      ⟨some t, by
        rcases t with ⟨⟨x, y⟩, p⟩
        exact ⟨nativeC60GDEncodeFamily history charge left right chargeEq p,
          nativeC60GDDecode_encodeFamily history charge left right chargeEq p⟩⟩
  have hinj : Function.Injective embedding := by
    intro t t' h
    have hsome :
        (some t : Option
          (NativeC60GDOriginalFamilyTotal history charge left right chargeEq)) =
          some t' :=
      congrArg
        (fun z : Set.range
          (nativeC60GDDecodeFamily history charge left right chargeEq) => z.1) h
    exact Option.some.inj hsome
  exact hinj.countable

/-- Every original family indexed source/target proof fiber is
Countable, by injectivity into the original complete total. -/
theorem nativeC60GDOriginalFamilyFiber_countable
    {A : Type u} {H : Type v} {I : Type w}
    (history : A → H) (charge : A → ℤ)
    (left right : I → A)
    (chargeEq : ∀ i : I, charge (left i) = charge (right i))
    (hA : Countable A) (hI : Countable I) (x y : A) :
    Countable (NativeFifteenFamilyCell history charge left right chargeEq x y) := by
  letI : Countable
      (NativeC60GDOriginalFamilyTotal history charge left right chargeEq) :=
    nativeC60GDOriginalFamilyTotal_countable history charge left right chargeEq hA hI
  have hinj : Function.Injective
      (fun p : NativeFifteenFamilyCell history charge left right chargeEq x y =>
        (⟨(x, y), p⟩ :
          NativeC60GDOriginalFamilyTotal history charge left right chargeEq)) := by
    intro p q h
    exact eq_of_heq (Sigma.mk.inj h).2
  exact hinj.countable

section ActualOriginalPhysicalFifteen

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

/-- The ACTUAL original physical AQ 15D proof fibers, with
all original 14D source and target witnesses, are Countable
from the actual original 14D fiber Countable alone. No
separate 15D Gen Countable premise remains. -/
theorem nativeK5GDOriginalPhysicalFifteen_countable_of_fourteen
    (W : NativeK5StructuralThirteenCell p U V)
    (h14 : Countable (NativeK5FifteenFourteenFiber W))
    (R S : NativeK5FifteenFourteenFiber W) :
    Countable (NativeK5AQFifteenCell W R S) :=
  nativeC60GDOriginalFamilyFiber_countable
    (nativeK5FifteenHistoryObserver W)
    (nativeK5FifteenChargeObserver W)
    (nativeK5AQLeft W) (nativeK5AQRight W)
    (nativeK5AQChargeEq W) h14 inferInstance R S

/-- Discharge the separate indexed 15D proof-fiber gate:
the actual entire physical AX base Total is Countable whenever
the true lower original 14D witness fiber is Countable. -/
theorem nativeK5GDBaseTotal_countable_of_fourteen
    (W : NativeK5StructuralThirteenCell p U V)
    (h14 : Countable (NativeK5FifteenFourteenFiber W)) :
    Countable (nativeK5AXBaseLayer W).Total :=
  nativeK5GCBaseTotal_countable_of_fourteen_fifteen W h14
    (nativeK5GDOriginalPhysicalFifteen_countable_of_fourteen W h14)

/-- The full true old FJ 18D source alphabet is Countable
from the genuine 14D witness fiber Countable alone; GA, GB,
GC, and GD discharge ALL separate 15D–18D syntax and Gen
cardinality premises. -/
theorem nativeK5GDPhysicalOriginal18_countable_of_fourteen
    (W : NativeK5StructuralThirteenCell p U V)
    (h14 : Countable (NativeK5FifteenFourteenFiber W)) :
    Countable (NativeC60DSCompleteEighteenCode
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)) :=
  nativeK5GCPhysicalOriginal18_countable_of_baseTotal W
    (nativeK5GDBaseTotal_countable_of_fourteen W h14)

/-- Exact aleph-null minimal noncommutative normal-generator
rank for every genuine nonempty finite physical AQ word, under
only Countable of the actual original 14D proof fiber.
Unconditional Countable arbitrary category Hom is NOT claimed. -/
theorem nativeK5GDPhysical_exactAleph0NormalRank_of_fourteen
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool) (hne : word ≠ [])
    (h14 : Countable (NativeK5FifteenFourteenFiber W)) :
    (∀ R : Set (NativeC60DTFullFree
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W)),
      (nativeC60DVFullWordTransport
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W) word).ker =
        Subgroup.normalClosure R → ℵ₀ ≤ #R) ∧
    (∃ R : Set (NativeC60DTFullFree
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W)),
      (nativeC60DVFullWordTransport
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W) word).ker =
        Subgroup.normalClosure R ∧ #R = ℵ₀) :=
  nativeK5GCPhysical_exactAleph0NormalRank_of_baseTotal
    W word hne (nativeK5GDBaseTotal_countable_of_fourteen W h14)

end ActualOriginalPhysicalFifteen

#print axioms nativeC60GDDecode_encodeCore
#print axioms nativeC60GDOriginalCoreTotal_countable
#print axioms nativeC60GDDecode_encodeFamily
#print axioms nativeC60GDOriginalFamilyTotal_countable
#print axioms nativeC60GDOriginalFamilyFiber_countable
#print axioms nativeK5GDOriginalPhysicalFifteen_countable_of_fourteen
#print axioms nativeK5GDBaseTotal_countable_of_fourteen
#print axioms nativeK5GDPhysicalOriginal18_countable_of_fourteen
#print axioms nativeK5GDPhysical_exactAleph0NormalRank_of_fourteen

end
end Kuu.F112.Physical
