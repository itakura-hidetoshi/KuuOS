import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeDepthRouteCountability

/-!
# F112-P94D3GI — exact original rotation edges and arbitrary finite chains

The two genuinely distinct original RotationEdge constructors store
opposite orientations of an entire proof-relevant LocalRotation.
RotationChain is an arbitrary finite refl/snoc history with all actual
intermediate native F45 Trees, each LocalRotation and all two-category
blocks and individual Nat depths. Our partial decoder rejects mismatched
intermediate Tree or category/Blocks boundaries and has an exact
decode(encode h)=some(original complete Type-valued h) left inverse.

No unverified F55 filling, raw equality quotient, arbitrary D/E Hom
countability or global coherence is inferred. Copyright Hidetoshi
Itakura / 板倉英俊. Lean v4.30.0-rc2, pinned mathlib.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section
universe uD vD uE vE u v

/-- Full original directed edge proof total. Both endpoint trees
and the exact local source witness remain Type values. -/
abbrev NativeGIOriginalEdgeTotal (p : Polygon)
    (D : Type uD) [Category.{vD} D]
    (E : Type uE) [Category.{vE} E] :
    Type (max (max uD uE) (max vD vE)) :=
  Σ boundary : NativeGHF45Boundary D E,
  Σ before : KuuNativeF45Tree p boundary.n boundary.m
    boundary.ma boundary.pa boundary.mb boundary.pb,
  Σ after : KuuNativeF45Tree p boundary.n boundary.m
    boundary.ma boundary.pa boundary.mb boundary.pb,
    KuuNativeF45Tree.RotationEdge p before after

/-- Preserve the exact categorical block and full tree endpoints. -/
def nativeGIPackLocal
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {before after : KuuNativeF45Tree p n m ma pa mb pb}
    (step : KuuNativeF45Tree.LocalRotation p before after) :
    NativeGIOriginalLocalTotal p D E :=
  ⟨⟨a, b, x, y, n, m, ma, pa, mb, pb⟩, before, after, step⟩

def nativeGIPackEdge
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {before after : KuuNativeF45Tree p n m ma pa mb pb}
    (edge : KuuNativeF45Tree.RotationEdge p before after) :
    NativeGIOriginalEdgeTotal p D E :=
  ⟨⟨a, b, x, y, n, m, ma, pa, mb, pb⟩, before, after, edge⟩

/-- A signed constructor tag PLUS the ORIGINAL complete
LocalRotation and its dependent before/after proof trees. -/
inductive NativeGIEdgePlainSyntax (Local : Type u) : Type u where
  | forward (step : Local)
  | backward (step : Local)
  deriving Countable

def nativeGIEncodeEdge
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] :
    {a b : D} → {x y : E} → {n m : Nat} →
    {ma mb : KuuNativeBlocks a b} →
    {pa pb : KuuNativeBlocks x y} →
    {before after : KuuNativeF45Tree p n m ma pa mb pb} →
    KuuNativeF45Tree.RotationEdge p before after →
    NativeGIEdgePlainSyntax (NativeGIOriginalLocalTotal p D E)
  | _, _, _, _, _, _, _, _, _, _, _, _, .forward step =>
      .forward (nativeGIPackLocal step)
  | _, _, _, _, _, _, _, _, _, _, _, _, .backward step =>
      .backward (nativeGIPackLocal step)

noncomputable def nativeGIDecodeEdge
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] :
    NativeGIEdgePlainSyntax (NativeGIOriginalLocalTotal p D E) →
    Option (NativeGIOriginalEdgeTotal p D E)
  | .forward ⟨boundary, before, after, step⟩ =>
      some ⟨boundary, before, after, .forward step⟩
  | .backward ⟨boundary, before, after, step⟩ =>
      some ⟨boundary, after, before, .backward step⟩

theorem nativeGIDecode_encodeEdge
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {before after : KuuNativeF45Tree p n m ma pa mb pb}
    (edge : KuuNativeF45Tree.RotationEdge p before after) :
    nativeGIDecodeEdge (nativeGIEncodeEdge edge) =
      some (nativeGIPackEdge edge) := by
  cases edge <;> rfl

theorem nativeGIOriginalEdgeTotal_countable
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    (hobjD : Countable D)
    (hhomD : ∀ a b : D, Countable (a ⟶ b))
    (hobjE : Countable E)
    (hhomE : ∀ x y : E, Countable (x ⟶ y)) :
    Countable (NativeGIOriginalEdgeTotal p D E) := by
  letI : Countable (NativeGIOriginalLocalTotal p D E) :=
    nativeGIOriginalLocalTotal_countable hobjD hhomD hobjE hhomE
  haveI : Countable (NativeGIEdgePlainSyntax
      (NativeGIOriginalLocalTotal p D E)) := inferInstance
  have hrange :
      (Set.range (nativeGIDecodeEdge (p := p) (D := D) (E := E))).Countable :=
    Set.countable_range _
  letI : Countable (Set.range
      (nativeGIDecodeEdge (p := p) (D := D) (E := E))) :=
    hrange.to_subtype
  let embedding : NativeGIOriginalEdgeTotal p D E →
      Set.range (nativeGIDecodeEdge (p := p) (D := D) (E := E)) :=
    fun raw => ⟨some raw, by
      rcases raw with ⟨boundary, before, after, edge⟩
      rcases boundary with ⟨a, b, x, y, n, m, ma, pa, mb, pb⟩
      exact ⟨nativeGIEncodeEdge edge, nativeGIDecode_encodeEdge edge⟩⟩
  have hinj : Function.Injective embedding := by
    intro first second h
    have hs : (some first : Option (NativeGIOriginalEdgeTotal p D E)) =
        some second := congrArg
          (fun t : Set.range
            (nativeGIDecodeEdge (p := p) (D := D) (E := E)) => t.1) h
    exact Option.some.inj hs
  exact hinj.countable

/-- Actual original proof-total of all finite rotation chains. -/
abbrev NativeGIOriginalChainTotal (p : Polygon)
    (D : Type uD) [Category.{vD} D]
    (E : Type uE) [Category.{vE} E] :
    Type (max (max uD uE) (max vD vE)) :=
  Σ boundary : NativeGHF45Boundary D E,
  Σ first : KuuNativeF45Tree p boundary.n boundary.m
    boundary.ma boundary.pa boundary.mb boundary.pb,
  Σ last : KuuNativeF45Tree p boundary.n boundary.m
    boundary.ma boundary.pa boundary.mb boundary.pb,
    KuuNativeF45Tree.RotationChain p first last

/-- Every complete proof-bearing chain, with all actual
intermediate F45 Trees and original individual directed edge terms. -/
inductive NativeGIChainPlainSyntax (Tree : Type u)
    (Edge : Type v) : Type (max u v) where
  | refl (tree : Tree)
  | snoc (prior : NativeGIChainPlainSyntax Tree Edge) (edge : Edge)
  deriving Countable

def nativeGIEncodeChain
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] :
    {a b : D} → {x y : E} → {n m : Nat} →
    {ma mb : KuuNativeBlocks a b} →
    {pa pb : KuuNativeBlocks x y} →
    {first last : KuuNativeF45Tree p n m ma pa mb pb} →
    KuuNativeF45Tree.RotationChain p first last →
    NativeGIChainPlainSyntax
      (NativeGHOriginalF45Total p D E)
      (NativeGIOriginalEdgeTotal p D E)
  | _, _, _, _, _, _, _, _, _, _, _, _, .refl tree =>
      .refl (nativeGIPackTree tree)
  | _, _, _, _, _, _, _, _, _, _, _, _, .snoc prior edge =>
      .snoc (nativeGIEncodeChain prior) (nativeGIPackEdge edge)

/-- Reject every incorrect intermediate rotation tree, as well
as mismatched D/E categories, original blocks or two Nat depths. -/
noncomputable def nativeGIChainAppendExact
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] :
    NativeGIOriginalChainTotal p D E →
    NativeGIOriginalEdgeTotal p D E →
    Option (NativeGIOriginalChainTotal p D E)
  | ⟨boundary, first, middle, prior⟩,
    ⟨boundary', before, last, edge⟩ => by
      classical
      by_cases hboundary : boundary = boundary'
      · subst boundary'
        by_cases hmiddle : middle = before
        · subst before
          exact some ⟨boundary, first, last, .snoc prior edge⟩
        · exact none
      · exact none

noncomputable def nativeGIDecodeChain
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] :
    NativeGIChainPlainSyntax
      (NativeGHOriginalF45Total p D E)
      (NativeGIOriginalEdgeTotal p D E) →
    Option (NativeGIOriginalChainTotal p D E)
  | .refl ⟨boundary, tree⟩ =>
      some ⟨boundary, tree, tree, .refl tree⟩
  | .snoc prior edge =>
      (nativeGIDecodeChain prior).bind
        (fun chain => nativeGIChainAppendExact chain edge)

theorem nativeGIChainAppendExact_eq
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first middle last : KuuNativeF45Tree p n m ma pa mb pb}
    (prior : KuuNativeF45Tree.RotationChain p first middle)
    (edge : KuuNativeF45Tree.RotationEdge p middle last) :
    nativeGIChainAppendExact
      (⟨⟨a, b, x, y, n, m, ma, pa, mb, pb⟩, first, middle, prior⟩ :
        NativeGIOriginalChainTotal p D E)
      (nativeGIPackEdge edge) =
      some (⟨⟨a, b, x, y, n, m, ma, pa, mb, pb⟩,
        first, last, .snoc prior edge⟩ :
        NativeGIOriginalChainTotal p D E) := by
  simp [nativeGIChainAppendExact, nativeGIPackEdge]

theorem nativeGIDecode_encodeChain
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first last : KuuNativeF45Tree p n m ma pa mb pb}
    (chain : KuuNativeF45Tree.RotationChain p first last) :
    nativeGIDecodeChain (nativeGIEncodeChain chain) =
      some (⟨⟨a, b, x, y, n, m, ma, pa, mb, pb⟩,
        first, last, chain⟩ : NativeGIOriginalChainTotal p D E) := by
  induction chain with
  | refl =>
      simp [nativeGIEncodeChain, nativeGIDecodeChain, nativeGIPackTree]
  | snoc prior edge ih =>
      simp [nativeGIEncodeChain, nativeGIDecodeChain, ih]
      exact nativeGIChainAppendExact_eq prior edge

theorem nativeGIOriginalChainTotal_countable
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    (hobjD : Countable D)
    (hhomD : ∀ a b : D, Countable (a ⟶ b))
    (hobjE : Countable E)
    (hhomE : ∀ x y : E, Countable (x ⟶ y)) :
    Countable (NativeGIOriginalChainTotal p D E) := by
  letI : Countable (NativeGHOriginalF45Total p D E) :=
    nativeGHOriginalF45Total_countable hobjD hhomD hobjE hhomE
  letI : Countable (NativeGIOriginalEdgeTotal p D E) :=
    nativeGIOriginalEdgeTotal_countable hobjD hhomD hobjE hhomE
  haveI : Countable (NativeGIChainPlainSyntax
      (NativeGHOriginalF45Total p D E)
      (NativeGIOriginalEdgeTotal p D E)) := inferInstance
  have hrange :
      (Set.range (nativeGIDecodeChain (p := p) (D := D) (E := E))).Countable :=
    Set.countable_range _
  letI : Countable (Set.range
      (nativeGIDecodeChain (p := p) (D := D) (E := E))) :=
    hrange.to_subtype
  let embedding : NativeGIOriginalChainTotal p D E →
      Set.range (nativeGIDecodeChain (p := p) (D := D) (E := E)) :=
    fun raw => ⟨some raw, by
      rcases raw with ⟨boundary, first, last, chain⟩
      rcases boundary with ⟨a, b, x, y, n, m, ma, pa, mb, pb⟩
      exact ⟨nativeGIEncodeChain chain, nativeGIDecode_encodeChain chain⟩⟩
  have hinj : Function.Injective embedding := by
    intro first second h
    have hs : (some first : Option (NativeGIOriginalChainTotal p D E)) =
        some second := congrArg
          (fun t : Set.range
            (nativeGIDecodeChain (p := p) (D := D) (E := E)) => t.1) h
    exact Option.some.inj hs
  exact hinj.countable

theorem nativeGIPhysicalEdgeTotal_countable (p : Polygon) :
    Countable (NativeGIOriginalEdgeTotal p Site Site) :=
  nativeGIOriginalEdgeTotal_countable
    nativeC60GEPhysicalSite_countable
    nativeC60GEPhysicalIncidenceHom_countable
    nativeC60GEPhysicalSite_countable
    nativeC60GEPhysicalIncidenceHom_countable

theorem nativeGIPhysicalChainTotal_countable (p : Polygon) :
    Countable (NativeGIOriginalChainTotal p Site Site) :=
  nativeGIOriginalChainTotal_countable
    nativeC60GEPhysicalSite_countable
    nativeC60GEPhysicalIncidenceHom_countable
    nativeC60GEPhysicalSite_countable
    nativeC60GEPhysicalIncidenceHom_countable

#print axioms nativeGIDecode_encodeEdge
#print axioms nativeGIOriginalEdgeTotal_countable
#print axioms nativeGIChainAppendExact_eq
#print axioms nativeGIDecode_encodeChain
#print axioms nativeGIOriginalChainTotal_countable
#print axioms nativeGIPhysicalEdgeTotal_countable
#print axioms nativeGIPhysicalChainTotal_countable
end
end Kuu.F112.Physical
