import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeF45Countability
import Kuu.F112.PolygonNativeF54DepthRoutes

/-!
# F112-P94D3GI — original Type-valued F54 rotation-to-depth-route countability

GI extends GH's faithful original F45 Tree codes. Every root associator
stores its actual three independently typed F45 stages and all D/E
intermediate original Blocks. Contextual steps retain original entire
subproofs and the unchanged surrounding tree; no shadow scalar, group
quotient or proof-irrelevant collapse of Type-valued histories is used.

The source has genuine LocalRotation, directed RotationEdge,
finite RotationChain, and full five-constructor DepthRotationRoute.
All countability claims about general D/E categories explicitly assume
Countable objects and Countable every category Hom fiber.

Append-only / same-root / no Gray / 107 public roots / no 19D filler.
Pinned Lean v4.30.0-rc2, mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6.
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

/-! ### The full original local rotation constructor source -/

/-- All three actually composable F45 stage proofs, including all
four intermediate original D/E blocks and six individual Nat depths. -/
abbrev NativeGIRootAssocTotal (p : Polygon)
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
  Σ n₁ : Nat, Σ m₁ : Nat,
  Σ n₂ : Nat, Σ m₂ : Nat,
  Σ n₃ : Nat, Σ m₃ : Nat,
    KuuNativeF45Tree p n₁ m₁ p₀ q₀ p₁ q₁ ×
    KuuNativeF45Tree p n₂ m₂ p₁ q₁ p₂ q₂ ×
    KuuNativeF45Tree p n₃ m₃ p₂ q₂ p₃ q₃

/-- The original LOCAL rotation total retains both exact dependent
F45 endpoints and the entire Type-valued local proof. -/
abbrev NativeGIOriginalLocalTotal (p : Polygon)
    (D : Type uD) [Category.{vD} D]
    (E : Type uE) [Category.{vE} E] :
    Type (max (max uD uE) (max vD vE)) :=
  Σ boundary : NativeGHF45Boundary D E,
  Σ before : KuuNativeF45Tree p boundary.n boundary.m
    boundary.ma boundary.pa boundary.mb boundary.pb,
  Σ after : KuuNativeF45Tree p boundary.n boundary.m
    boundary.ma boundary.pa boundary.mb boundary.pb,
    KuuNativeF45Tree.LocalRotation p before after

/-- Full finite local rotation code, retaining actual original
F45 trees at the root and at arbitrary nesting of contexts. -/
inductive NativeGILocalPlainSyntax (p : Polygon)
    (Root : Type u) (Tree : Type v) : Type (max u v) where
  | assoc (triple : Root)
  | leftContext (step : NativeGILocalPlainSyntax p Root Tree)
      (later : Tree)
  | rightContext (earlier : Tree)
      (step : NativeGILocalPlainSyntax p Root Tree)
  deriving Countable

/-- Faithfully encode every original local rotation constructor.
Nested contexts preserve the full original subrotation recursively. -/
def nativeGIEncodeLocal
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] :
    {a b : D} → {x y : E} → {n m : Nat} →
    {ma mb : KuuNativeBlocks a b} →
    {pa pb : KuuNativeBlocks x y} →
    {before after : KuuNativeF45Tree p n m ma pa mb pb} →
    KuuNativeF45Tree.LocalRotation p before after →
    NativeGILocalPlainSyntax p
      (NativeGIRootAssocTotal p D E)
      (NativeGHOriginalF45Total p D E)
  | _, _, _, _, _, _, _, _, _, _, _, _, .assoc first second third =>
      .assoc ⟨_, _, _, _, _, _, _, _, _, _, _, _,
        _, _, _, _, _, _, (first, second, third)⟩
  | _, _, _, _, _, _, _, _, _, _, _, _, .leftContext step later =>
      .leftContext (nativeGIEncodeLocal step) ⟨_, later⟩
  | _, _, _, _, _, _, _, _, _, _, _, _, .rightContext earlier step =>
      .rightContext ⟨_, earlier⟩ (nativeGIEncodeLocal step)

/-- Local left contextualization checks the actual D/E categorical
objects and both original intermediate Blocks for exact equality. -/
noncomputable def nativeGILocalLeftExact
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] :
    NativeGIOriginalLocalTotal p D E →
    NativeGHOriginalF45Total p D E →
    Option (NativeGIOriginalLocalTotal p D E)
  | ⟨⟨a, b, x, y, n, m, ma, pa, mb, pb⟩, before, after, step⟩,
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
                  exact some ⟨⟨a, b, x, y, n + k, m + l,
                    ma, pa, mc, pc⟩,
                    .node before later, .node after later,
                    .leftContext step later⟩
                · exact none
              · exact none
            · exact none
          · exact none
        · exact none
      · exact none

/-- Local right contextualization performs the same dependent
boundary checks before adjoining the untouched earlier proof. -/
noncomputable def nativeGILocalRightExact
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] :
    NativeGHOriginalF45Total p D E →
    NativeGIOriginalLocalTotal p D E →
    Option (NativeGIOriginalLocalTotal p D E)
  | ⟨⟨a, b, x, y, k, l, ma, pa, mb, pb⟩, earlier⟩,
    ⟨⟨a', b', x', y', n, m, mb', pb', mc, pc⟩, before, after, step⟩ => by
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
                  exact some ⟨⟨a, b, x, y, k + n, l + m,
                    ma, pa, mc, pc⟩,
                    .node earlier before, .node earlier after,
                    .rightContext earlier step⟩
                · exact none
              · exact none
            · exact none
          · exact none
        · exact none
      · exact none

/-- Partial decoder rejects non-composable D/E or intermediate
Blocks boundaries, while keeping any valid source rotation intact. -/
noncomputable def nativeGIDecodeLocal
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E] :
    NativeGILocalPlainSyntax p
      (NativeGIRootAssocTotal p D E)
      (NativeGHOriginalF45Total p D E) →
    Option (NativeGIOriginalLocalTotal p D E)
  | .assoc ⟨a, b, x, y, p₀, p₁, p₂, p₃,
      q₀, q₁, q₂, q₃, n₁, m₁, n₂, m₂, n₃, m₃,
      (first, second, third)⟩ =>
      some ⟨⟨a, b, x, y, n₁ + (n₂ + n₃), m₁ + (m₂ + m₃),
        p₀, q₀, p₃, q₃⟩,
        KuuNativeF45Tree.castDepths
          (Nat.add_assoc n₁ n₂ n₃) (Nat.add_assoc m₁ m₂ m₃)
          (.node (.node first second) third),
        .node first (.node second third),
        .assoc first second third⟩
  | .leftContext prior later =>
      (nativeGIDecodeLocal prior).bind (fun step =>
        nativeGILocalLeftExact step later)
  | .rightContext earlier prior =>
      (nativeGIDecodeLocal prior).bind (fun step =>
        nativeGILocalRightExact earlier step)

/-- Exact dependent left-construction of a genuine source rotation. -/
theorem nativeGILocalLeftExact_eq
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E} {n m k l : Nat}
    {ma mb mc : KuuNativeBlocks a b}
    {pa pb pc : KuuNativeBlocks x y}
    {before after : KuuNativeF45Tree p n m ma pa mb pb}
    (step : KuuNativeF45Tree.LocalRotation p before after)
    (later : KuuNativeF45Tree p k l mb pb mc pc) :
    nativeGILocalLeftExact
      (⟨⟨a, b, x, y, n, m, ma, pa, mb, pb⟩,
        before, after, step⟩ : NativeGIOriginalLocalTotal p D E)
      (⟨⟨a, b, x, y, k, l, mb, pb, mc, pc⟩, later⟩ :
        NativeGHOriginalF45Total p D E) =
    some ⟨⟨a, b, x, y, n + k, m + l, ma, pa, mc, pc⟩,
      .node before later, .node after later,
      .leftContext step later⟩ := by
  simp [nativeGILocalLeftExact]

theorem nativeGILocalRightExact_eq
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E} {n m k l : Nat}
    {ma mb mc : KuuNativeBlocks a b}
    {pa pb pc : KuuNativeBlocks x y}
    (earlier : KuuNativeF45Tree p k l ma pa mb pb)
    {before after : KuuNativeF45Tree p n m mb pb mc pc}
    (step : KuuNativeF45Tree.LocalRotation p before after) :
    nativeGILocalRightExact
      (⟨⟨a, b, x, y, k, l, ma, pa, mb, pb⟩, earlier⟩ :
        NativeGHOriginalF45Total p D E)
      (⟨⟨a, b, x, y, n, m, mb, pb, mc, pc⟩,
        before, after, step⟩ : NativeGIOriginalLocalTotal p D E) =
    some ⟨⟨a, b, x, y, k + n, l + m, ma, pa, mc, pc⟩,
      .node earlier before, .node earlier after,
      .rightContext earlier step⟩ := by
  simp [nativeGILocalRightExact]

/-- LocalRotation's exact root and arbitrary nested contextual
Type-valued source terms survive the decoder/encoder cycle. -/
theorem nativeGIDecode_encodeLocal
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {before after : KuuNativeF45Tree p n m ma pa mb pb}
    (step : KuuNativeF45Tree.LocalRotation p before after) :
    nativeGIDecodeLocal (nativeGIEncodeLocal step) =
      some (⟨⟨a, b, x, y, n, m, ma, pa, mb, pb⟩,
        before, after, step⟩ : NativeGIOriginalLocalTotal p D E) := by
  induction step with
  | assoc first second third =>
      simp [nativeGIEncodeLocal, nativeGIDecodeLocal]
  | leftContext step later ih =>
      simp [nativeGIEncodeLocal, nativeGIDecodeLocal,
        ih, nativeGILocalLeftExact_eq]
  | rightContext earlier step ih =>
      simp [nativeGIEncodeLocal, nativeGIDecodeLocal,
        ih, nativeGILocalRightExact_eq]

/-- Countably many original well-typed three-stage assoc atoms,
not merely countably many numeric depth vectors. -/
theorem nativeGIRootAssocTotal_countable
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    (hobjD : Countable D)
    (hhomD : ∀ a b : D, Countable (a ⟶ b))
    (hobjE : Countable E)
    (hhomE : ∀ x y : E, Countable (x ⟶ y)) :
    Countable (NativeGIRootAssocTotal p D E) := by
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

/-- Entire original LocalRotation proof total Countable with
full original D/E object and Hom smallness explicitly retained. -/
theorem nativeGIOriginalLocalTotal_countable
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    (hobjD : Countable D)
    (hhomD : ∀ a b : D, Countable (a ⟶ b))
    (hobjE : Countable E)
    (hhomE : ∀ x y : E, Countable (x ⟶ y)) :
    Countable (NativeGIOriginalLocalTotal p D E) := by
  letI : Countable (NativeGIRootAssocTotal p D E) :=
    nativeGIRootAssocTotal_countable hobjD hhomD hobjE hhomE
  letI : Countable (NativeGHOriginalF45Total p D E) :=
    nativeGHOriginalF45Total_countable hobjD hhomD hobjE hhomE
  haveI : Countable (NativeGILocalPlainSyntax p
      (NativeGIRootAssocTotal p D E)
      (NativeGHOriginalF45Total p D E)) := inferInstance
  have hrange :
      (Set.range (nativeGIDecodeLocal (p := p) (D := D) (E := E))).Countable :=
    Set.countable_range _
  letI : Countable (Set.range
      (nativeGIDecodeLocal (p := p) (D := D) (E := E))) :=
    hrange.to_subtype
  let embedding : NativeGIOriginalLocalTotal p D E →
      Set.range (nativeGIDecodeLocal (p := p) (D := D) (E := E)) :=
    fun raw => ⟨some raw, by
      rcases raw with ⟨boundary, before, after, step⟩
      rcases boundary with ⟨a, b, x, y, n, m, ma, pa, mb, pb⟩
      exact ⟨nativeGIEncodeLocal step, nativeGIDecode_encodeLocal step⟩⟩
  have hinj : Function.Injective embedding := by
    intro first second h
    have hs : (some first : Option (NativeGIOriginalLocalTotal p D E)) =
        some second := congrArg
          (fun t : Set.range
            (nativeGIDecodeLocal (p := p) (D := D) (E := E)) => t.1) h
    exact Option.some.inj hs
  exact hinj.countable

/-- Every fixed original LocalRotation proof fiber is Countable.
The original before and after F45 tree proofs remain distinct. -/
theorem nativeGIOriginalLocalFiber_countable
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    (hobjD : Countable D)
    (hhomD : ∀ a b : D, Countable (a ⟶ b))
    (hobjE : Countable E)
    (hhomE : ∀ x y : E, Countable (x ⟶ y))
    {a b : D} {x y : E} {n m : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    (before after : KuuNativeF45Tree p n m ma pa mb pb) :
    Countable (KuuNativeF45Tree.LocalRotation p before after) := by
  letI : Countable (NativeGIOriginalLocalTotal p D E) :=
    nativeGIOriginalLocalTotal_countable hobjD hhomD hobjE hhomE
  have hinj : Function.Injective
      (fun step : KuuNativeF45Tree.LocalRotation p before after =>
        (⟨⟨a, b, x, y, n, m, ma, pa, mb, pb⟩,
          before, after, step⟩ : NativeGIOriginalLocalTotal p D E)) := by
    intro first second h
    have h₁ : (⟨before, after, first⟩ :
        Σ before : KuuNativeF45Tree p n m ma pa mb pb,
        Σ after : KuuNativeF45Tree p n m ma pa mb pb,
          KuuNativeF45Tree.LocalRotation p before after) =
        ⟨before, after, second⟩ :=
      eq_of_heq (Sigma.mk.inj h).2
    have h₂ : (⟨after, first⟩ :
        Σ after : KuuNativeF45Tree p n m ma pa mb pb,
          KuuNativeF45Tree.LocalRotation p before after) =
        ⟨after, second⟩ :=
      eq_of_heq (Sigma.mk.inj h₁).2
    exact eq_of_heq (Sigma.mk.inj h₂).2
  exact hinj.countable

/-- Genuine physical C60 Site×Site source local rotation total. -/
theorem nativeGIPhysicalLocalTotal_countable (p : Polygon) :
    Countable (NativeGIOriginalLocalTotal p Site Site) :=
  nativeGIOriginalLocalTotal_countable
    nativeC60GEPhysicalSite_countable
    nativeC60GEPhysicalIncidenceHom_countable
    nativeC60GEPhysicalSite_countable
    nativeC60GEPhysicalIncidenceHom_countable

#print axioms nativeGILocalLeftExact_eq
#print axioms nativeGILocalRightExact_eq
#print axioms nativeGIDecode_encodeLocal
#print axioms nativeGIRootAssocTotal_countable
#print axioms nativeGIOriginalLocalTotal_countable
#print axioms nativeGIOriginalLocalFiber_countable
#print axioms nativeGIPhysicalLocalTotal_countable

end
end Kuu.F112.Physical
