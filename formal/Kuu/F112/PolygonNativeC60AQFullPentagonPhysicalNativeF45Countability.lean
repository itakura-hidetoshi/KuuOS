import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeAxisTraceCountability
import Kuu.F112.PolygonNativeF45Source

/-!
# F112-P94D3GH — full original Type-valued native F45 tree countability

GF and GG established exact source-dependent countability of original
native Path, Blocks, OneStep and arbitrary finite AxisTrace proofs.
GH extends the faithfully decoded finite code to the genuine two-axis
KuuNativeF45Tree with all three constructors: refl, leaf, node.

Both independent D/E categories, every C60 sector, original F45 order,
all original axis traces, complete intermediate native Blocks, and
both Nat-depth indices are retained. Nodes are accepted only at
identical dependent D/E object and Blocks boundaries; an indexed
decoder additionally rejects an incompatible claimed full boundary
(including both Nat-depths). On any genuine source tree the exact
decode/encode cycle recovers the complete original dependent Type term.

General D/E conclusions assume Countable objects and Countable EACH
categorical Hom fiber. Genuine physical C60 Site conclusions discharge
these assumptions by the previously proved GE incidence-category
results. No 14D countability, original F55, 19D filler, Gray coherence,
global strict n-category or hyperdescent is inferred.

Append-only; 107 public roots; strict Kuu primary, independent Kuu
retained as a presentation; pinned Lean v4.30.0-rc2 and mathlib
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

universe uD vD uE vE u v w z

/-- Distinct original physical execution orders remain distinct
Countable source tokens, never a commuting quotient. -/
instance : Countable KuuNativeF45Order := by
  let encode : KuuNativeF45Order → Bool
    | .firstAxisFirst => false
    | .secondAxisFirst => true
  have hinj : Function.Injective encode := by
    intro a b h
    cases a <;> cases b <;> simp [encode] at h ⊢
  exact hinj.countable

/-- The full original 2-category dependent boundary, including
independent block presentations and exact Nat grades. -/
structure NativeGHF45Boundary
    (D : Type uD) [Category.{vD} D]
    (E : Type uE) [Category.{vE} E] where
  a : D
  b : D
  x : E
  y : E
  n : Nat
  m : Nat
  ma : KuuNativeBlocks a b
  pa : KuuNativeBlocks x y
  mb : KuuNativeBlocks a b
  pb : KuuNativeBlocks x y

/-- The actual ORIGINAL proof total, not an observer quotient.
A single dependent Sigma retains the complete original F45 proof. -/
abbrev NativeGHOriginalF45Total
    (p : Polygon)
    (D : Type uD) [Category.{vD} D]
    (E : Type uE) [Category.{vE} E] :
    Type (max (max uD uE) (max vD vE)) :=
  Σ boundary : NativeGHF45Boundary D E,
    KuuNativeF45Tree p boundary.n boundary.m
      boundary.ma boundary.pa boundary.mb boundary.pb

/-- Finite full binary syntax. The tokens carry ORIGINAL native
blocks and whole original trace proofs, not scalar counts. -/
inductive NativeGHF45PlainSyntax (p : Polygon)
    (BlocksD : Type u) (BlocksE : Type v)
    (TraceD : Type w) (TraceE : Type z) :
    Type (max (max u v) (max w z)) where
  | refl (sector : PolygonBoundarySector p)
      (first : BlocksD) (second : BlocksE)
  | leaf (sector : PolygonBoundarySector p)
      (order : KuuNativeF45Order)
      (first : TraceD) (second : TraceE)
  | node (first second :
      NativeGHF45PlainSyntax p BlocksD BlocksE TraceD TraceE)
  deriving Countable

/-- Full source constructor-preserving code, with all ORIGINAL
Type-valued leaves, primitive order and two independent histories. -/
def nativeGHEncodeF45
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] :
    {a b : D} → {x y : E} → {n m : Nat} →
    {ma mb : KuuNativeBlocks a b} →
    {pa pb : KuuNativeBlocks x y} →
    KuuNativeF45Tree p n m ma pa mb pb →
    NativeGHF45PlainSyntax p
      (NativeGFOriginalBlocksTotal D)
      (NativeGFOriginalBlocksTotal E)
      (NativeGGOriginalAxisTraceTotal D)
      (NativeGGOriginalAxisTraceTotal E)
  | _, _, _, _, _, _, _, _, _, _, .refl sector first second =>
      .refl sector ⟨_, _, first⟩ ⟨_, _, second⟩
  | _, _, _, _, _, _, _, _, _, _, .leaf sector order first second =>
      .leaf sector order
        ⟨_, _, _, _, _, first⟩
        ⟨_, _, _, _, _, second⟩
  | _, _, _, _, _, _, _, _, _, _, .node first second =>
      .node (nativeGHEncodeF45 first) (nativeGHEncodeF45 second)

/-- Partial node composition: accept only identical two-category
objects AND original intermediate Blocks, with no invented Hom.
Both result Nat depths are the actual source sums. -/
noncomputable def nativeGHJoinExact
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] :
    NativeGHOriginalF45Total p D E →
    NativeGHOriginalF45Total p D E →
    Option (NativeGHOriginalF45Total p D E)
  | ⟨⟨a, b, x, y, n, m, ma, pa, mb, pb⟩, first⟩,
    ⟨⟨a', b', x', y', n', m', ma', pa', mc, pc⟩, second⟩ => by
      classical
      by_cases ha : a = a'
      · subst a'
        by_cases hb : b = b'
        · subst b'
          by_cases hx : x = x'
          · subst x'
            by_cases hy : y = y'
            · subst y'
              by_cases hma : mb = ma'
              · subst ma'
                by_cases hpa : pb = pa'
                · subst pa'
                  exact some ⟨⟨a, b, x, y, n + n', m + m',
                    ma, pa, mc, pc⟩, .node first second⟩
                · exact none
              · exact none
            · exact none
          · exact none
        · exact none
      · exact none

/-- Every original constructor has a faithful partial
interpretation; malformed independently typed nodes return none. -/
noncomputable def nativeGHDecodeF45
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] :
    NativeGHF45PlainSyntax p
      (NativeGFOriginalBlocksTotal D)
      (NativeGFOriginalBlocksTotal E)
      (NativeGGOriginalAxisTraceTotal D)
      (NativeGGOriginalAxisTraceTotal E) →
    Option (NativeGHOriginalF45Total p D E)
  | .refl sector ⟨a, b, first⟩ ⟨x, y, second⟩ =>
      some ⟨⟨a, b, x, y, 0, 0,
        first, second, first, second⟩, .refl sector first second⟩
  | .leaf sector order
      ⟨a, b, n, ma, mb, first⟩
      ⟨x, y, m, pa, pb, second⟩ =>
      some ⟨⟨a, b, x, y, n, m, ma, pa, mb, pb⟩,
        .leaf sector order first second⟩
  | .node first second =>
      (nativeGHDecodeF45 first).bind (fun rawFirst =>
        (nativeGHDecodeF45 second).bind (fun rawSecond =>
          nativeGHJoinExact rawFirst rawSecond))

/-- Joining two ACTUALLY composable source trees returns their
unmodified original node, at the exact added pair of Nat depths. -/
theorem nativeGHJoinExact_eq
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb mc : KuuNativeBlocks a b}
    {pa pb pc : KuuNativeBlocks x y}
    (first : KuuNativeF45Tree p n m ma pa mb pb)
    (second : KuuNativeF45Tree p n' m' mb pb mc pc) :
    nativeGHJoinExact
      (⟨⟨a, b, x, y, n, m, ma, pa, mb, pb⟩, first⟩ :
        NativeGHOriginalF45Total p D E)
      (⟨⟨a, b, x, y, n', m', mb, pb, mc, pc⟩, second⟩ :
        NativeGHOriginalF45Total p D E) =
    some ⟨⟨a, b, x, y, n + n', m + m', ma, pa, mc, pc⟩,
      .node first second⟩ := by
  simp [nativeGHJoinExact]

/-- Strict left inverse on the ENTIRE genuine original F45
dependent proof, including both original order/trace axes and every
intermediate node/Blocks boundary; no proof term is truncated. -/
theorem nativeGHDecode_encodeF45
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (tree : KuuNativeF45Tree p n m ma pa mb pb) :
    nativeGHDecodeF45 (nativeGHEncodeF45 tree) =
      some (⟨⟨a, b, x, y, n, m, ma, pa, mb, pb⟩, tree⟩ :
        NativeGHOriginalF45Total p D E) := by
  induction tree with
  | refl sector first second =>
      simp [nativeGHEncodeF45, nativeGHDecodeF45]
  | leaf sector order first second =>
      simp [nativeGHEncodeF45, nativeGHDecodeF45]
  | node first second ihFirst ihSecond =>
      simp [nativeGHEncodeF45, nativeGHDecodeF45,
        ihFirst, ihSecond, nativeGHJoinExact_eq]

/-- A boundary-aware partial decoder also rejects incorrect
source/target objects, original Blocks or either Nat depth. -/
noncomputable def nativeGHDecodeF45At
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (code : NativeGHF45PlainSyntax p
      (NativeGFOriginalBlocksTotal D)
      (NativeGFOriginalBlocksTotal E)
      (NativeGGOriginalAxisTraceTotal D)
      (NativeGGOriginalAxisTraceTotal E)) :
    Option (KuuNativeF45Tree p n m ma pa mb pb) := by
  classical
  exact (nativeGHDecodeF45 code).bind (fun ⟨boundary, tree⟩ =>
    if h : boundary = (⟨a, b, x, y, n, m, ma, pa, mb, pb⟩ :
        NativeGHF45Boundary D E) then
      some (Eq.ndrec
        (motive := fun q : NativeGHF45Boundary D E =>
          KuuNativeF45Tree p q.n q.m q.ma q.pa q.mb q.pb)
        tree h)
    else none)

/-- Exact indexed left inverse at ANY original dependent F45
fiber, not merely the unindexed total source. -/
theorem nativeGHDecode_encodeF45At
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (tree : KuuNativeF45Tree p n m ma pa mb pb) :
    nativeGHDecodeF45At (nativeGHEncodeF45 tree) = some tree := by
  simp [nativeGHDecodeF45At, nativeGHDecode_encodeF45]

/-- The complete genuine F45 source TOTAL is Countable under
explicit countability of D/E objects and EACH original Hom fiber. -/
theorem nativeGHOriginalF45Total_countable
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    (hobjD : Countable D)
    (hhomD : ∀ a b : D, Countable (a ⟶ b))
    (hobjE : Countable E)
    (hhomE : ∀ x y : E, Countable (x ⟶ y)) :
    Countable (NativeGHOriginalF45Total p D E) := by
  letI : Countable (NativeGFOriginalBlocksTotal D) :=
    nativeGFOriginalBlocksTotal_countable hobjD hhomD
  letI : Countable (NativeGFOriginalBlocksTotal E) :=
    nativeGFOriginalBlocksTotal_countable hobjE hhomE
  letI : Countable (NativeGGOriginalAxisTraceTotal D) :=
    nativeGGOriginalAxisTraceTotal_countable hobjD hhomD
  letI : Countable (NativeGGOriginalAxisTraceTotal E) :=
    nativeGGOriginalAxisTraceTotal_countable hobjE hhomE
  haveI : Countable (NativeGHF45PlainSyntax p
      (NativeGFOriginalBlocksTotal D)
      (NativeGFOriginalBlocksTotal E)
      (NativeGGOriginalAxisTraceTotal D)
      (NativeGGOriginalAxisTraceTotal E)) := inferInstance
  have hrange :
      (Set.range (nativeGHDecodeF45 (p := p) (D := D) (E := E))).Countable :=
    Set.countable_range _
  letI : Countable (Set.range
      (nativeGHDecodeF45 (p := p) (D := D) (E := E))) :=
    hrange.to_subtype
  let embedding : NativeGHOriginalF45Total p D E →
      Set.range (nativeGHDecodeF45 (p := p) (D := D) (E := E)) :=
    fun raw => ⟨some raw, by
      rcases raw with ⟨⟨a, b, x, y, n, m, ma, pa, mb, pb⟩, tree⟩
      exact ⟨nativeGHEncodeF45 tree, nativeGHDecode_encodeF45 tree⟩⟩
  have hinj : Function.Injective embedding := by
    intro left right h
    have hs : (some left : Option (NativeGHOriginalF45Total p D E)) =
        some right := congrArg
          (fun t : Set.range
            (nativeGHDecodeF45 (p := p) (D := D) (E := E)) => t.1) h
    exact Option.some.inj hs
  exact hinj.countable

/-- Every fully original F45 dependent indexed Type-valued
fiber is Countable, without identifying distinct source histories. -/
theorem nativeGHOriginalF45Fiber_countable
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    (hobjD : Countable D)
    (hhomD : ∀ a b : D, Countable (a ⟶ b))
    (hobjE : Countable E)
    (hhomE : ∀ x y : E, Countable (x ⟶ y))
    {a b : D} {x y : E} (n m : Nat)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :
    Countable (KuuNativeF45Tree p n m ma pa mb pb) := by
  letI : Countable (NativeGHOriginalF45Total p D E) :=
    nativeGHOriginalF45Total_countable hobjD hhomD hobjE hhomE
  have hinj : Function.Injective
      (fun tree : KuuNativeF45Tree p n m ma pa mb pb =>
        (⟨⟨a, b, x, y, n, m, ma, pa, mb, pb⟩, tree⟩ :
          NativeGHOriginalF45Total p D E)) := by
    intro first second heq
    exact eq_of_heq (Sigma.mk.inj heq).2
  exact hinj.countable

/-- Unconditional full Type-valued F45 total at a true physical
C60 polygon: BOTH native category axes are the actual Site category. -/
theorem nativeGHPhysicalF45Total_countable (p : Polygon) :
    Countable (NativeGHOriginalF45Total p Site Site) :=
  nativeGHOriginalF45Total_countable
    nativeC60GEPhysicalSite_countable
    nativeC60GEPhysicalIncidenceHom_countable
    nativeC60GEPhysicalSite_countable
    nativeC60GEPhysicalIncidenceHom_countable

/-- Every original physically indexed two-Site F45 Type fiber
is Countable, with sector, order, both depths and all blocks intact. -/
theorem nativeGHPhysicalF45Fiber_countable
    (p : Polygon)
    {a b x y : Site}
    (n m : Nat)
    (ma mb : KuuNativeBlocks a b)
    (pa pb : KuuNativeBlocks x y) :
    Countable (KuuNativeF45Tree p n m ma pa mb pb) :=
  nativeGHOriginalF45Fiber_countable
    nativeC60GEPhysicalSite_countable
    nativeC60GEPhysicalIncidenceHom_countable
    nativeC60GEPhysicalSite_countable
    nativeC60GEPhysicalIncidenceHom_countable
    n m ma mb pa pb

/-- The full genuine C60 polygon index is itself countable:
all real sector-anchored F45 source proofs across all 32 faces. -/
theorem nativeGHPhysicalAllPolygonF45_countable :
    Countable (Σ p : Polygon, NativeGHOriginalF45Total p Site Site) := by
  letI : Countable Polygon := nativeC60GEPhysicalPolygon_countable
  letI : ∀ p : Polygon, Countable (NativeGHOriginalF45Total p Site Site) :=
    nativeGHPhysicalF45Total_countable
  infer_instance

#print axioms nativeGHJoinExact_eq
#print axioms nativeGHDecode_encodeF45
#print axioms nativeGHDecode_encodeF45At
#print axioms nativeGHOriginalF45Total_countable
#print axioms nativeGHOriginalF45Fiber_countable
#print axioms nativeGHPhysicalF45Total_countable
#print axioms nativeGHPhysicalF45Fiber_countable
#print axioms nativeGHPhysicalAllPolygonF45_countable

end
end Kuu.F112.Physical
