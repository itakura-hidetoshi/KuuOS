import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK3P92FullCountability

/-!
# F112-P94D3GK3 — genuinely distinct F55 structural comparison

The independent NativeF55StructuralComparison has exactly three
original constructors: original P92B proof, independent original F54
structural seam, and vertically composable trans. Its finite syntax
retains BOTH prior original raw evidence families as distinct tags.

The strict dependent partial decoder rejects incompatible full
Type-valued F54 middle routes, D/E Blocks, Nat grades and F45 trees.
The left inverse and original source/fiber Countable do NOT assume
the two sub-presentations are interchangeable. No historical typed
equivalence, original 14D Countable, 19D filler or higher descent.
Append-only; no Gray, no new axioms, no sorry; 107 root preservation.
Lean v4.30.0-rc2, pinned mathlib.
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

/-- Three original constructor tags, not a quotient or coercion. -/
inductive NativeGK3StructuralPlainSyntax
    (P92 : Type u) (Seam : Type v) : Type (max u v) where
  | original (cell : P92)
  | structural (w : Seam)
  | trans (left right : NativeGK3StructuralPlainSyntax P92 Seam)
  deriving Countable

abbrev NativeGK3StructuralTypedCode
    (p : Polygon)
    (D : Type uD) [Category.{vD} D]
    (E : Type uE) [Category.{vE} E] :
    Type (max (max uD uE) (max vD vE)) :=
  NativeGK3StructuralPlainSyntax
    (NativeGKOriginalP92Total p D E)
    (NativeGK2OriginalSeamTotal p D E)

/-- Actual fully indexed original structural P94 extension total,
distinct from the source P92B and the source F54 seam. -/
abbrev NativeGK3OriginalStructuralTotal
    (p : Polygon)
    (D : Type uD) [Category.{vD} D]
    (E : Type uE) [Category.{vE} E] :
    Type (max (max uD uE) (max vD vE)) :=
  Σ parallel : NativeGJOriginalParallelTotal p D E,
    NativeF55StructuralComparison p parallel.1.2 parallel.2

def nativeGK3PackStructural
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {n n' m m' : Nat}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (cell : NativeF55StructuralComparison p r s) :
    NativeGK3OriginalStructuralTotal p D E :=
  ⟨⟨nativeGJ2PackRoute r, s⟩, cell⟩

/-- Original three-constructor recursive encoder. -/
def nativeGK3StructuralEncode
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {n n' m m' : Nat}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (cell : NativeF55StructuralComparison p r s) :
    NativeGK3StructuralTypedCode p D E :=
  match cell with
  | .original p92 => .original (nativeGK3PackP92 p92)
  | .structural seam => .structural (nativeGK2PackSeam seam)
  | .trans w v =>
      .trans (nativeGK3StructuralEncode w) (nativeGK3StructuralEncode v)

theorem nativeGK3StructuralTypedCode_countable
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    (hobjD : Countable D)
    (hhomD : ∀ a b : D, Countable (a ⟶ b))
    (hobjE : Countable E)
    (hhomE : ∀ x y : E, Countable (x ⟶ y)) :
    Countable (NativeGK3StructuralTypedCode p D E) := by
  letI : Countable (NativeGKOriginalP92Total p D E) :=
    nativeGK3P92OriginalTotal_countable hobjD hhomD hobjE hhomE
  letI : Countable (NativeGK2OriginalSeamTotal p D E) :=
    nativeGK2OriginalStructuralTotal_countable hobjD hhomD hobjE hhomE
  infer_instance

/-- Exact equality of ALL original F54 middle route evidence is
required before vertically composing a pair of structural proofs. -/
noncomputable def nativeGK3StructuralTransExact
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] :
    NativeGK3OriginalStructuralTotal p D E →
    NativeGK3OriginalStructuralTotal p D E →
    Option (NativeGK3OriginalStructuralTotal p D E)
  | ⟨⟨⟨boundary, r⟩, s⟩, left⟩,
    ⟨⟨⟨boundary', s'⟩, t⟩, right⟩ => by
      classical
      by_cases hb : boundary = boundary'
      · subst boundary'
        by_cases hs : s = s'
        · subst s'
          exact some ⟨⟨⟨boundary, r⟩, t⟩, .trans left right⟩
        · exact none
      · exact none

/-- Fully dependent partial decoder into the exact ORIGINAL F55
structural extension, with three distinct constructor tags. -/
noncomputable def nativeGK3StructuralDecode
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] :
    NativeGK3StructuralTypedCode p D E →
    Option (NativeGK3OriginalStructuralTotal p D E)
  | .original ⟨⟨⟨boundary, r⟩, s⟩, p92⟩ =>
      some ⟨⟨⟨boundary, r⟩, s⟩, .original p92⟩
  | .structural ⟨⟨⟨boundary, r⟩, s⟩, seam⟩ =>
      some ⟨⟨⟨boundary, r⟩, s⟩, .structural seam⟩
  | .trans left right =>
      (nativeGK3StructuralDecode left).bind (fun rawLeft =>
        (nativeGK3StructuralDecode right).bind (fun rawRight =>
          nativeGK3StructuralTransExact rawLeft rawRight))

theorem nativeGK3StructuralTransExact_eq
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {n n' m m' : Nat}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
    (left : NativeF55StructuralComparison p r s)
    (right : NativeF55StructuralComparison p s t) :
    nativeGK3StructuralTransExact
      (nativeGK3PackStructural left : NativeGK3OriginalStructuralTotal p D E)
      (nativeGK3PackStructural right : NativeGK3OriginalStructuralTotal p D E) =
    some (nativeGK3PackStructural (.trans left right) :
      NativeGK3OriginalStructuralTotal p D E) := by
  simp [nativeGK3StructuralTransExact, nativeGK3PackStructural, nativeGJ2PackRoute]

/-- Exact left inverse on all three genuine original constructors. -/
theorem nativeGK3StructuralDecode_encode
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {n n' m m' : Nat}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (cell : NativeF55StructuralComparison p r s) :
    nativeGK3StructuralDecode (nativeGK3StructuralEncode cell) =
      some (nativeGK3PackStructural cell :
        NativeGK3OriginalStructuralTotal p D E) := by
  induction cell with
  | original p92 =>
      simp [nativeGK3StructuralEncode, nativeGK3StructuralDecode,
        nativeGK3PackP92, nativeGK3PackStructural]
  | structural seam =>
      simp [nativeGK3StructuralEncode, nativeGK3StructuralDecode,
        nativeGK2PackSeam, nativeGK3PackStructural]
  | trans left right ihLeft ihRight =>
      simp [nativeGK3StructuralEncode, nativeGK3StructuralDecode,
        ihLeft, ihRight]
      exact nativeGK3StructuralTransExact_eq left right

/-- Countable true original P94 structural total by an injective
embedding in the range of the strict dependent partial decoder. -/
theorem nativeGK3OriginalStructuralTotal_countable
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    (hobjD : Countable D)
    (hhomD : ∀ a b : D, Countable (a ⟶ b))
    (hobjE : Countable E)
    (hhomE : ∀ x y : E, Countable (x ⟶ y)) :
    Countable (NativeGK3OriginalStructuralTotal p D E) := by
  letI : Countable (NativeGK3StructuralTypedCode p D E) :=
    nativeGK3StructuralTypedCode_countable hobjD hhomD hobjE hhomE
  have hrange :
      (Set.range (nativeGK3StructuralDecode (p := p) (D := D) (E := E))).Countable :=
    Set.countable_range _
  letI : Countable (Set.range
      (nativeGK3StructuralDecode (p := p) (D := D) (E := E))) :=
    hrange.to_subtype
  let embedding : NativeGK3OriginalStructuralTotal p D E →
      Set.range (nativeGK3StructuralDecode (p := p) (D := D) (E := E)) :=
    fun raw => ⟨some raw, by
      rcases raw with ⟨⟨⟨boundary, r⟩, s⟩, cell⟩
      rcases boundary with
        ⟨a, b, x, y, ma, pa, mb, pb,
          n, n', m, m', first, last⟩
      exact ⟨nativeGK3StructuralEncode cell,
        nativeGK3StructuralDecode_encode cell⟩⟩
  have hinj : Function.Injective embedding := by
    intro left right h
    have hs : (some left : Option (NativeGK3OriginalStructuralTotal p D E)) =
        some right := congrArg
          (fun t : Set.range
            (nativeGK3StructuralDecode (p := p) (D := D) (E := E)) => t.1) h
    exact Option.some.inj hs
  exact hinj.countable

theorem nativeGK3OriginalStructuralFiber_countable
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    (hobjD : Countable D)
    (hhomD : ∀ a b : D, Countable (a ⟶ b))
    (hobjE : Countable E)
    (hhomE : ∀ x y : E, Countable (x ⟶ y))
    {a b : D} {x y : E}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {n n' m m' : Nat}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (r s : KuuNativeF45Tree.DepthRotationRoute p first last) :
    Countable (NativeF55StructuralComparison p r s) := by
  letI : Countable (NativeGK3OriginalStructuralTotal p D E) :=
    nativeGK3OriginalStructuralTotal_countable hobjD hhomD hobjE hhomE
  have hinj : Function.Injective
      (fun cell : NativeF55StructuralComparison p r s =>
        (nativeGK3PackStructural cell : NativeGK3OriginalStructuralTotal p D E)) := by
    intro left right h
    exact eq_of_heq (Sigma.mk.inj h).2
  exact hinj.countable

theorem nativeGK3PhysicalStructuralTotal_countable (p : Polygon) :
    Countable (NativeGK3OriginalStructuralTotal p Site Site) :=
  nativeGK3OriginalStructuralTotal_countable
    nativeC60GEPhysicalSite_countable
    nativeC60GEPhysicalIncidenceHom_countable
    nativeC60GEPhysicalSite_countable
    nativeC60GEPhysicalIncidenceHom_countable

theorem nativeGK3PhysicalStructuralFiber_countable
    (p : Polygon)
    {a b x y : Site}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {n n' m m' : Nat}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (r s : KuuNativeF45Tree.DepthRotationRoute p first last) :
    Countable (NativeF55StructuralComparison p r s) :=
  nativeGK3OriginalStructuralFiber_countable
    nativeC60GEPhysicalSite_countable
    nativeC60GEPhysicalIncidenceHom_countable
    nativeC60GEPhysicalSite_countable
    nativeC60GEPhysicalIncidenceHom_countable r s

theorem nativeGK3PhysicalAllPolygonStructural_countable :
    Countable (Σ p : Polygon,
      NativeGK3OriginalStructuralTotal p Site Site) := by
  letI : Countable Polygon := nativeC60GEPhysicalPolygon_countable
  letI : ∀ p : Polygon,
      Countable (NativeGK3OriginalStructuralTotal p Site Site) :=
    nativeGK3PhysicalStructuralTotal_countable
  infer_instance

#print axioms nativeGK3StructuralTypedCode_countable
#print axioms nativeGK3StructuralTransExact_eq
#print axioms nativeGK3StructuralDecode_encode
#print axioms nativeGK3OriginalStructuralTotal_countable
#print axioms nativeGK3OriginalStructuralFiber_countable
#print axioms nativeGK3PhysicalStructuralTotal_countable
#print axioms nativeGK3PhysicalStructuralFiber_countable
#print axioms nativeGK3PhysicalAllPolygonStructural_countable

end
end Kuu.F112.Physical
