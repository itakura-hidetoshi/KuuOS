import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeRotationChainCountability

/-!
# F112-P94D3GI — full original five-constructor F54 DepthRotationRoute

This is a faithful countability proof for the actual new independent
two-category KuuNativeF45Tree.DepthRotationRoute source, not its
observer quotient or mere rotation-length scalar. All original Type
values survive: full finite RotationChain, both Nat equality
transports at castDepths, complete intermediate F45 trees at trans,
and all left/right F45 context nodes with original D/E blocks.

The finite code is partially decoded: objects, original D/E blocks,
both source/target Nat-depth indices and the complete middle Type-valued
F45 proof must match exactly. The strict left inverse on every genuine
source proof establishes Countable of the whole original dependent
source and each exact indexed fiber under explicit D/E smallness.
Genuine C60 Site×Site satisfies these premises via GE through GH.

This is NOT an equivalence with frozen historical F19/F28 sources,
nor unconditional original 14D countability, F55 comparison, a
geometric 19D filler, a global strict n-category or hyperdescent.
Copyright Hidetoshi Itakura / 板倉英俊. Pinned Lean v4.30.0-rc2,
mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section
universe uD vD uE vE u v w

/-- Both distinct Nat-grade endpoints, full original categorical
Blocks boundary, and ORIGINAL two dependent F45 proof terms. -/
structure NativeGIDepthBoundary (p : Polygon)
    (D : Type uD) [Category.{vD} D]
    (E : Type uE) [Category.{vE} E] where
  a : D
  b : D
  x : E
  y : E
  ma : KuuNativeBlocks a b
  pa : KuuNativeBlocks x y
  mb : KuuNativeBlocks a b
  pb : KuuNativeBlocks x y
  n : Nat
  n' : Nat
  m : Nat
  m' : Nat
  first : KuuNativeF45Tree p n m ma pa mb pb
  last : KuuNativeF45Tree p n' m' ma pa mb pb

/-- Fully original source Type-valued proof total, without flattening
its five constructors or any intermediate route/Tree witness. -/
abbrev NativeGIOriginalDepthTotal
    (p : Polygon)
    (D : Type uD) [Category.{vD} D]
    (E : Type uE) [Category.{vE} E] :
    Type (max (max uD uE) (max vD vE)) :=
  Σ boundary : NativeGIDepthBoundary p D E,
    KuuNativeF45Tree.DepthRotationRoute p boundary.first boundary.last

/-- A true original cast atom stores its ORIGINAL source F45 proof,
the two target Nat depths and BOTH original equality transports.
The equality data are Prop carried in PLift for the Type-valued syntax, not substituted for original Type evidence. -/
abbrev NativeGICastDepthToken
    (p : Polygon)
    (D : Type uD) [Category.{vD} D]
    (E : Type uE) [Category.{vE} E] :
    Type (max (max uD uE) (max vD vE)) :=
  Σ raw : NativeGHOriginalF45Total p D E,
    Σ n' : Nat, Σ m' : Nat, PLift ((raw.1.n = n') ∧ (raw.1.m = m'))

/-- Original chain/cast/trans/left-context/right-context finite syntax.
The primitive tokens carry complete original F45 proof data. -/
inductive NativeGIDepthPlainSyntax
    (Chain : Type u) (Cast : Type v) (Tree : Type w) :
    Type (max (max u v) w) where
  | chain (prior : Chain)
  | castDepths (cast : Cast)
  | trans (first second : NativeGIDepthPlainSyntax Chain Cast Tree)
  | leftContext (route : NativeGIDepthPlainSyntax Chain Cast Tree)
      (later : Tree)
  | rightContext (earlier : Tree)
      (route : NativeGIDepthPlainSyntax Chain Cast Tree)
  deriving Countable

/-- Exact dependent packaging of a whole original rotation chain. -/
def nativeGIPackChain
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first last : KuuNativeF45Tree p n m ma pa mb pb}
    (chain : KuuNativeF45Tree.RotationChain p first last) :
    NativeGIOriginalChainTotal p D E :=
  ⟨⟨a, b, x, y, n, m, ma, pa, mb, pb⟩, first, last, chain⟩

/-- The genuine five original constructors are encoded recursively
without discarding any independent native source witness or context. -/
def nativeGIEncodeDepth
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] :
    {a b : D} → {x y : E} → {n n' m m' : Nat} →
    {ma mb : KuuNativeBlocks a b} →
    {pa pb : KuuNativeBlocks x y} →
    {first : KuuNativeF45Tree p n m ma pa mb pb} →
    {last : KuuNativeF45Tree p n' m' ma pa mb pb} →
    KuuNativeF45Tree.DepthRotationRoute p first last →
    NativeGIDepthPlainSyntax
      (NativeGIOriginalChainTotal p D E)
      (NativeGICastDepthToken p D E)
      (NativeGHOriginalF45Total p D E)
  | _, _, _, _, _, _, _, _, _, _, _, _, _, _, .chain path =>
      .chain (nativeGIPackChain path)
  | _, _, _, _, _, _, _, _, _, _, _, _, _, _, .castDepths hn hm tree =>
      .castDepths ⟨nativeGIPackTree tree, _, _, ⟨⟨hn, hm⟩⟩⟩
  | _, _, _, _, _, _, _, _, _, _, _, _, _, _, .trans first second =>
      .trans (nativeGIEncodeDepth first) (nativeGIEncodeDepth second)
  | _, _, _, _, _, _, _, _, _, _, _, _, _, _, .leftContext route later =>
      .leftContext (nativeGIEncodeDepth route) (nativeGIPackTree later)
  | _, _, _, _, _, _, _, _, _, _, _, _, _, _, .rightContext earlier route =>
      .rightContext (nativeGIPackTree earlier) (nativeGIEncodeDepth route)

/-- A trans is accepted only when ALL category object and original
D/E blocks and BOTH indexed depths agree, AND the complete middle
original Type-valued F45 tree is literally equal. -/
noncomputable def nativeGIDepthTransExact
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] :
    NativeGIOriginalDepthTotal p D E →
    NativeGIOriginalDepthTotal p D E →
    Option (NativeGIOriginalDepthTotal p D E)
  | ⟨⟨a, b, x, y, ma, pa, mb, pb, n₁, n₂, m₁, m₂,
      first, middle⟩, left⟩,
    ⟨⟨a', b', x', y', ma', pa', mb', pb', n₂', n₃, m₂', m₃,
      middle', last⟩, right⟩ => by
      classical
      by_cases ha : a = a'
      · subst a'
        by_cases hb : b = b'
        · subst b'
          by_cases hx : x = x'
          · subst x'
            by_cases hy : y = y'
            · subst y'
              by_cases hma : ma = ma'
              · subst ma'
                by_cases hpa : pa = pa'
                · subst pa'
                  by_cases hmb : mb = mb'
                  · subst mb'
                    by_cases hpb : pb = pb'
                    · subst pb'
                      by_cases hn : n₂ = n₂'
                      · subst n₂'
                        by_cases hm : m₂ = m₂'
                        · subst m₂'
                          by_cases htree : middle = middle'
                          · subst middle'
                            exact some ⟨⟨a, b, x, y, ma, pa, mb, pb,
                              n₁, n₃, m₁, m₃, first, last⟩,
                              .trans left right⟩
                          · exact none
                        · exact none
                      · exact none
                    · exact none
                  · exact none
                · exact none
              · exact none
            · exact none
          · exact none
        · exact none
      · exact none

/-- Original typed left context: only source objects and BOTH
intermediate D/E Blocks can be glued to an unchanged later stage. -/
noncomputable def nativeGIDepthLeftExact
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] :
    NativeGIOriginalDepthTotal p D E →
    NativeGHOriginalF45Total p D E →
    Option (NativeGIOriginalDepthTotal p D E)
  | ⟨⟨a, b, x, y, ma, pa, mb, pb, n, n', m, m',
      before, after⟩, route⟩,
    ⟨⟨a', b', x', y', k, l, mb', pb', mc, pc⟩, later⟩ => by
      classical
      by_cases ha : a = a'
      · subst a'
        by_cases hb : b = b'
        · subst b'
          by_cases hx : x = x'
          · subst x'
            by_cases hy : y = y'
            · subst y'
              by_cases hmb : mb = mb'
              · subst mb'
                by_cases hpb : pb = pb'
                · subst pb'
                  exact some ⟨⟨a, b, x, y, ma, pa, mc, pc,
                    n + k, n' + k, m + l, m' + l,
                    .node before later, .node after later⟩,
                    .leftContext route later⟩
                · exact none
              · exact none
            · exact none
          · exact none
        · exact none
      · exact none

/-- Original typed right context with exact intermediate Blocks. -/
noncomputable def nativeGIDepthRightExact
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] :
    NativeGHOriginalF45Total p D E →
    NativeGIOriginalDepthTotal p D E →
    Option (NativeGIOriginalDepthTotal p D E)
  | ⟨⟨a, b, x, y, k, l, ma, pa, mb, pb⟩, earlier⟩,
    ⟨⟨a', b', x', y', mb', pb', mc, pc, n, n', m, m',
      before, after⟩, route⟩ => by
      classical
      by_cases ha : a = a'
      · subst a'
        by_cases hb : b = b'
        · subst b'
          by_cases hx : x = x'
          · subst x'
            by_cases hy : y = y'
            · subst y'
              by_cases hmb : mb = mb'
              · subst mb'
                by_cases hpb : pb = pb'
                · subst pb'
                  exact some ⟨⟨a, b, x, y, ma, pa, mc, pc,
                    k + n, k + n', l + m, l + m',
                    .node earlier before, .node earlier after⟩,
                    .rightContext earlier route⟩
                · exact none
              · exact none
            · exact none
          · exact none
        · exact none
      · exact none

/-- The actual partial source interpreter of all five constructors.
It has no fallback inhabitant for mismatched independent boundaries. -/
noncomputable def nativeGIDecodeDepth
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] :
    NativeGIDepthPlainSyntax
      (NativeGIOriginalChainTotal p D E)
      (NativeGICastDepthToken p D E)
      (NativeGHOriginalF45Total p D E) →
    Option (NativeGIOriginalDepthTotal p D E)
  | .chain ⟨⟨a, b, x, y, n, m, ma, pa, mb, pb⟩,
      first, last, chain⟩ =>
      some ⟨⟨a, b, x, y, ma, pa, mb, pb, n, n, m, m,
        first, last⟩, .chain chain⟩
  | .castDepths ⟨⟨⟨a, b, x, y, n, m, ma, pa, mb, pb⟩,
      tree⟩, n', m', ⟨⟨hn, hm⟩⟩⟩ =>
      some ⟨⟨a, b, x, y, ma, pa, mb, pb, n, n', m, m',
        tree, KuuNativeF45Tree.castDepths hn hm tree⟩,
        .castDepths hn hm tree⟩
  | .trans first second =>
      (nativeGIDecodeDepth first).bind (fun rawFirst =>
        (nativeGIDecodeDepth second).bind (fun rawSecond =>
          nativeGIDepthTransExact rawFirst rawSecond))
  | .leftContext prior later =>
      (nativeGIDecodeDepth prior).bind (fun raw =>
        nativeGIDepthLeftExact raw later)
  | .rightContext earlier prior =>
      (nativeGIDecodeDepth prior).bind (fun raw =>
        nativeGIDepthRightExact earlier raw)

/-- The genuine source/target tree and all four individual grades
are returned unmodified when two truly composable routes are joined. -/
theorem nativeGIDepthTransExact_eq
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
    {first : KuuNativeF45Tree p n₁ m₁ ma pa mb pb}
    {middle : KuuNativeF45Tree p n₂ m₂ ma pa mb pb}
    {last : KuuNativeF45Tree p n₃ m₃ ma pa mb pb}
    (left : KuuNativeF45Tree.DepthRotationRoute p first middle)
    (right : KuuNativeF45Tree.DepthRotationRoute p middle last) :
    nativeGIDepthTransExact
      (⟨⟨a, b, x, y, ma, pa, mb, pb, n₁, n₂, m₁, m₂,
        first, middle⟩, left⟩ : NativeGIOriginalDepthTotal p D E)
      (⟨⟨a, b, x, y, ma, pa, mb, pb, n₂, n₃, m₂, m₃,
        middle, last⟩, right⟩ : NativeGIOriginalDepthTotal p D E) =
      some (⟨⟨a, b, x, y, ma, pa, mb, pb, n₁, n₃, m₁, m₃,
        first, last⟩, .trans left right⟩ :
        NativeGIOriginalDepthTotal p D E) := by
  simp [nativeGIDepthTransExact]

theorem nativeGIDepthLeftExact_eq
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    {ma mb mc : KuuNativeBlocks a b}
    {pa pb pc : KuuNativeBlocks x y}
    {n n' m m' k l : Nat}
    {before : KuuNativeF45Tree p n m ma pa mb pb}
    {after : KuuNativeF45Tree p n' m' ma pa mb pb}
    (route : KuuNativeF45Tree.DepthRotationRoute p before after)
    (later : KuuNativeF45Tree p k l mb pb mc pc) :
    nativeGIDepthLeftExact
      (⟨⟨a, b, x, y, ma, pa, mb, pb, n, n', m, m',
        before, after⟩, route⟩ : NativeGIOriginalDepthTotal p D E)
      (nativeGIPackTree later) =
      some (⟨⟨a, b, x, y, ma, pa, mc, pc,
        n + k, n' + k, m + l, m' + l,
        .node before later, .node after later⟩,
        .leftContext route later⟩ : NativeGIOriginalDepthTotal p D E) := by
  simp [nativeGIDepthLeftExact, nativeGIPackTree]

theorem nativeGIDepthRightExact_eq
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    {ma mb mc : KuuNativeBlocks a b}
    {pa pb pc : KuuNativeBlocks x y}
    {n n' m m' k l : Nat}
    (earlier : KuuNativeF45Tree p k l ma pa mb pb)
    {before : KuuNativeF45Tree p n m mb pb mc pc}
    {after : KuuNativeF45Tree p n' m' mb pb mc pc}
    (route : KuuNativeF45Tree.DepthRotationRoute p before after) :
    nativeGIDepthRightExact
      (nativeGIPackTree earlier)
      (⟨⟨a, b, x, y, mb, pb, mc, pc, n, n', m, m',
        before, after⟩, route⟩ : NativeGIOriginalDepthTotal p D E) =
      some (⟨⟨a, b, x, y, ma, pa, mc, pc,
        k + n, k + n', l + m, l + m',
        .node earlier before, .node earlier after⟩,
        .rightContext earlier route⟩ : NativeGIOriginalDepthTotal p D E) := by
  simp [nativeGIDepthRightExact, nativeGIPackTree]

/-- Strict reconstruction of every actual original five-constructor
DepthRotationRoute, including all nested Type-valued intermediates. -/
theorem nativeGIDecode_encodeDepth
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {n n' m m' : Nat}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (route : KuuNativeF45Tree.DepthRotationRoute p first last) :
    nativeGIDecodeDepth (nativeGIEncodeDepth route) =
      some (⟨⟨a, b, x, y, ma, pa, mb, pb, n, n', m, m',
        first, last⟩, route⟩ : NativeGIOriginalDepthTotal p D E) := by
  induction route with
  | chain chain =>
      simp [nativeGIEncodeDepth, nativeGIDecodeDepth, nativeGIPackChain]
  | castDepths hn hm tree =>
      simp [nativeGIEncodeDepth, nativeGIDecodeDepth,
        nativeGIPackTree]
  | trans left right ihLeft ihRight =>
      simp [nativeGIEncodeDepth, nativeGIDecodeDepth,
        ihLeft, ihRight] <;> exact nativeGIDepthTransExact_eq left right
  | leftContext route later ih =>
      simp [nativeGIEncodeDepth, nativeGIDecodeDepth, ih] <;>
        exact nativeGIDepthLeftExact_eq route later
  | rightContext earlier route ih =>
      simp [nativeGIEncodeDepth, nativeGIDecodeDepth, ih] <;>
        exact nativeGIDepthRightExact_eq earlier route

/-- The complete original two-Nat proof-transport constructor tokens
are Countable, including the actual dependent F45 proof and BOTH
original Nat equality witnesses. -/
theorem nativeGICastDepthToken_countable
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    (hobjD : Countable D)
    (hhomD : ∀ a b : D, Countable (a ⟶ b))
    (hobjE : Countable E)
    (hhomE : ∀ x y : E, Countable (x ⟶ y)) :
    Countable (NativeGICastDepthToken p D E) := by
  letI : Countable (NativeGHOriginalF45Total p D E) :=
    nativeGHOriginalF45Total_countable hobjD hhomD hobjE hhomE
  infer_instance

theorem nativeGIOriginalDepthTotal_countable
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    (hobjD : Countable D)
    (hhomD : ∀ a b : D, Countable (a ⟶ b))
    (hobjE : Countable E)
    (hhomE : ∀ x y : E, Countable (x ⟶ y)) :
    Countable (NativeGIOriginalDepthTotal p D E) := by
  letI : Countable (NativeGIOriginalChainTotal p D E) :=
    nativeGIOriginalChainTotal_countable hobjD hhomD hobjE hhomE
  letI : Countable (NativeGICastDepthToken p D E) :=
    nativeGICastDepthToken_countable hobjD hhomD hobjE hhomE
  letI : Countable (NativeGHOriginalF45Total p D E) :=
    nativeGHOriginalF45Total_countable hobjD hhomD hobjE hhomE
  haveI : Countable (NativeGIDepthPlainSyntax
      (NativeGIOriginalChainTotal p D E)
      (NativeGICastDepthToken p D E)
      (NativeGHOriginalF45Total p D E)) := inferInstance
  have hrange :
      (Set.range (nativeGIDecodeDepth (p := p) (D := D) (E := E))).Countable :=
    Set.countable_range _
  letI : Countable (Set.range
      (nativeGIDecodeDepth (p := p) (D := D) (E := E))) :=
    hrange.to_subtype
  let embedding : NativeGIOriginalDepthTotal p D E →
      Set.range (nativeGIDecodeDepth (p := p) (D := D) (E := E)) :=
    fun raw => ⟨some raw, by
      rcases raw with ⟨boundary, route⟩
      rcases boundary with
        ⟨a, b, x, y, ma, pa, mb, pb, n, n', m, m', first, last⟩
      exact ⟨nativeGIEncodeDepth route, nativeGIDecode_encodeDepth route⟩⟩
  have hinj : Function.Injective embedding := by
    intro first second h
    have hs : (some first : Option (NativeGIOriginalDepthTotal p D E)) =
        some second := congrArg
          (fun t : Set.range
            (nativeGIDecodeDepth (p := p) (D := D) (E := E)) => t.1) h
    exact Option.some.inj hs
  exact hinj.countable

/-- Countable EVERY exact original D/E object, block, depth and
F45 endpoint fiber of the full five-constructor depth route source. -/
theorem nativeGIOriginalDepthFiber_countable
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
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :
    Countable (KuuNativeF45Tree.DepthRotationRoute p first last) := by
  letI : Countable (NativeGIOriginalDepthTotal p D E) :=
    nativeGIOriginalDepthTotal_countable hobjD hhomD hobjE hhomE
  have hinj : Function.Injective
      (fun route : KuuNativeF45Tree.DepthRotationRoute p first last =>
        (⟨⟨a, b, x, y, ma, pa, mb, pb, n, n', m, m',
          first, last⟩, route⟩ : NativeGIOriginalDepthTotal p D E)) := by
    intro left right h
    exact eq_of_heq (Sigma.mk.inj h).2
  exact hinj.countable

theorem nativeGIPhysicalDepthTotal_countable (p : Polygon) :
    Countable (NativeGIOriginalDepthTotal p Site Site) :=
  nativeGIOriginalDepthTotal_countable
    nativeC60GEPhysicalSite_countable
    nativeC60GEPhysicalIncidenceHom_countable
    nativeC60GEPhysicalSite_countable
    nativeC60GEPhysicalIncidenceHom_countable

theorem nativeGIPhysicalDepthFiber_countable
    (p : Polygon)
    {a b x y : Site}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {n n' m m' : Nat}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (last : KuuNativeF45Tree p n' m' ma pa mb pb) :
    Countable (KuuNativeF45Tree.DepthRotationRoute p first last) :=
  nativeGIOriginalDepthFiber_countable
    nativeC60GEPhysicalSite_countable
    nativeC60GEPhysicalIncidenceHom_countable
    nativeC60GEPhysicalSite_countable
    nativeC60GEPhysicalIncidenceHom_countable first last

/-- All 32 genuine physical C60 polygon carriers and their entire
original full depth-route evidence total are countable together. -/
theorem nativeGIPhysicalAllPolygonDepth_countable :
    Countable (Σ p : Polygon, NativeGIOriginalDepthTotal p Site Site) := by
  letI : Countable Polygon := nativeC60GEPhysicalPolygon_countable
  letI : ∀ p : Polygon, Countable (NativeGIOriginalDepthTotal p Site Site) :=
    nativeGIPhysicalDepthTotal_countable
  infer_instance

#print axioms nativeGIDepthTransExact_eq
#print axioms nativeGIDepthLeftExact_eq
#print axioms nativeGIDepthRightExact_eq
#print axioms nativeGIDecode_encodeDepth
#print axioms nativeGICastDepthToken_countable
#print axioms nativeGIOriginalDepthTotal_countable
#print axioms nativeGIOriginalDepthFiber_countable
#print axioms nativeGIPhysicalDepthTotal_countable
#print axioms nativeGIPhysicalDepthFiber_countable
#print axioms nativeGIPhysicalAllPolygonDepth_countable
end
end Kuu.F112.Physical
