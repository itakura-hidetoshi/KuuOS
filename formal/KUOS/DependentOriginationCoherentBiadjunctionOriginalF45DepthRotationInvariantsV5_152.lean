import KUOS.DependentOriginationCoherentBiadjunctionOriginalF45PresentedRotationCellsV5_152

namespace KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionExchangeQuotientConcatenationV5_141.Grid

set_option autoImplicit false
noncomputable section

/-!
# F55-C1 / v5.152 — true depth-cast invariance of any actual F55 path

F55-A/B retain all original F54 Type-valued local rotation witnesses
inside the constructors of DepthRotationRoute, with explicit and
INDEPENDENT casts for original F19 modification and F28
compression-kernel primitive depths.

We now prove, by genuine induction on EVERY constructor of the
higher path carrier, the exact two depth equalities, F44 generated
independent-axis exchange quotient preservation, and complete original
F19/F28 axis-history preservation after both required casts.

The pentagon and independent rotation square are constructed paths;
PresentedCell is a separately specified higher presentation, not
a previously postulated equivalence in an external tricategory.
-/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

/-- The two original primitive counts of the ends of an ACTUAL
finite depth-aware route agree, with INDEPENDENT equality witnesses.
The casts are not an identification of F19 and F28 Hom types. -/
def OriginalF45BracketTree.DepthRotationRoute.depthEq
    {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    {first : OriginalF45BracketTree n m ma pa mb pb}
    {last : OriginalF45BracketTree n' m' ma pa mb pb}
    (route : OriginalF45BracketTree.DepthRotationRoute first last) :
    n = n' ∧ m = m' := by
  induction route with
  | chain _ =>
      exact ⟨rfl, rfl⟩
  | castDepths hn hm _ =>
      exact ⟨hn, hm⟩
  | trans left right ihLeft ihRight =>
      exact ⟨ihLeft.1.trans ihRight.1, ihLeft.2.trans ihRight.2⟩
  | leftContext path later ih =>
      exact ⟨congrArg (fun k : Nat => k + _) ih.1,
        congrArg (fun k : Nat => k + _) ih.2⟩
  | rightContext earlier path ih =>
      exact ⟨congrArg (fun k : Nat => _ + k) ih.1,
        congrArg (fun k : Nat => _ + k) ih.2⟩

/-- An arbitrary REAL finite route in the original F45 binary-tree
presentation preserves the entire F44 generated independent-axis
exchange class, AFTER its two separately necessary Nat-index casts.

This proof is structural on the original F55-A constructors. In
particular, the trans, left-context and right-context cases explicitly
apply F53's dependent cast composition/congruence, rather than
assuming that Nat.add_assoc is a definitional equality. -/
theorem OriginalF45BracketTree.DepthRotationRoute.toExchangeClass_eq
    {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    {first : OriginalF45BracketTree n m ma pa mb pb}
    {last : OriginalF45BracketTree n' m' ma pa mb pb}
    (route : OriginalF45BracketTree.DepthRotationRoute first last) :
    ExchangeClass.castDepths route.depthEq.1 route.depthEq.2
      first.toExchangeClass = last.toExchangeClass := by
  induction route with
  | chain path =>
      change _ = _
      simpa only [OriginalF45BracketTree.DepthRotationRoute.depthEq,
        ExchangeClass.castDepths] using path.toExchangeClass_eq
  | castDepths hn hm tree =>
      simpa only [OriginalF45BracketTree.DepthRotationRoute.depthEq] using
        (OriginalF45BracketTree.castDepths_toExchangeClass hn hm tree).symm
  | trans left right ihLeft ihRight =>
      change ExchangeClass.castDepths
        (left.depthEq.1.trans right.depthEq.1)
        (left.depthEq.2.trans right.depthEq.2) _ = _
      rw [← ExchangeClass.castDepths_comp]
      rw [ihLeft, ihRight]
  | leftContext path later ih =>
      change ExchangeClass.castDepths
        (congrArg (fun k : Nat => k + _) path.depthEq.1)
        (congrArg (fun k : Nat => k + _) path.depthEq.2)
        (ExchangeClass.append _ _) =
        ExchangeClass.append _ _
      rw [ExchangeClass.castDepths_appendLeft, ih]
  | rightContext earlier path ih =>
      change ExchangeClass.castDepths
        (congrArg (fun k : Nat => _ + k) path.depthEq.1)
        (congrArg (fun k : Nat => _ + k) path.depthEq.2)
        (ExchangeClass.append _ _) =
        ExchangeClass.append _ _
      rw [ExchangeClass.castDepths_appendRight, ih]

/-- Preservation is stronger than equality of evaluated Hom composites:
BOTH complete originally typed F19 and F28 primitive-operation
histories agree after the two exact depth transports. -/
theorem OriginalF45BracketTree.DepthRotationRoute.axisHistories_eq
    {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    {first : OriginalF45BracketTree n m ma pa mb pb}
    {last : OriginalF45BracketTree n' m' ma pa mb pb}
    (route : OriginalF45BracketTree.DepthRotationRoute first last) :
    (OriginalF45BracketTree.castDepths
        route.depthEq.1 route.depthEq.2 first).axisHistories =
      last.axisHistories := by
  have heq := route.toExchangeClass_eq
  have hh := congrArg ExchangeClass.axisTraces heq
  simpa only [OriginalF45BracketTree.toExchangeClass_axisTraces] using hh

/-- Each real F55-A 3-edge pentagon route has the F44 class of the
SAME original right-deep tree after its exactly recorded two casts. -/
theorem OriginalF45BracketTree.DepthRotationRoute.pentagonLong_toClass
    {a b : D} {x y : E}
    {n₁ n₂ n₃ n₄ m₁ m₂ m₃ m₄ : Nat}
    {p₀ p₁ p₂ p₃ p₄ : Blocks a b}
    {q₀ q₁ q₂ q₃ q₄ : Blocks x y}
    (t₁ : OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁)
    (t₂ : OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂)
    (t₃ : OriginalF45BracketTree n₃ m₃ p₂ q₂ p₃ q₃)
    (t₄ : OriginalF45BracketTree n₄ m₄ p₃ q₃ p₄ q₄) :
    ExchangeClass.castDepths
      (OriginalF45BracketTree.DepthRotationRoute.pentagonLong
        t₁ t₂ t₃ t₄).depthEq.1
      (OriginalF45BracketTree.DepthRotationRoute.pentagonLong
        t₁ t₂ t₃ t₄).depthEq.2
      (OriginalF45BracketTree.pentagon0 t₁ t₂ t₃ t₄).toExchangeClass =
        (OriginalF45BracketTree.pentagon3 t₁ t₂ t₃ t₄).toExchangeClass :=
  (OriginalF45BracketTree.DepthRotationRoute.pentagonLong t₁ t₂ t₃ t₄).toExchangeClass_eq

/-- Analogous class equality from the separately stored, shorter,
genuinely two-edge original F54 pentagon route. -/
theorem OriginalF45BracketTree.DepthRotationRoute.pentagonShort_toClass
    {a b : D} {x y : E}
    {n₁ n₂ n₃ n₄ m₁ m₂ m₃ m₄ : Nat}
    {p₀ p₁ p₂ p₃ p₄ : Blocks a b}
    {q₀ q₁ q₂ q₃ q₄ : Blocks x y}
    (t₁ : OriginalF45BracketTree n₁ m₁ p₀ q₀ p₁ q₁)
    (t₂ : OriginalF45BracketTree n₂ m₂ p₁ q₁ p₂ q₂)
    (t₃ : OriginalF45BracketTree n₃ m₃ p₂ q₂ p₃ q₃)
    (t₄ : OriginalF45BracketTree n₄ m₄ p₃ q₃ p₄ q₄) :
    ExchangeClass.castDepths
      (OriginalF45BracketTree.DepthRotationRoute.pentagonShort
        t₁ t₂ t₃ t₄).depthEq.1
      (OriginalF45BracketTree.DepthRotationRoute.pentagonShort
        t₁ t₂ t₃ t₄).depthEq.2
      (OriginalF45BracketTree.pentagon0 t₁ t₂ t₃ t₄).toExchangeClass =
        (OriginalF45BracketTree.pentagon3 t₁ t₂ t₃ t₄).toExchangeClass :=
  (OriginalF45BracketTree.DepthRotationRoute.pentagonShort t₁ t₂ t₃ t₄).toExchangeClass_eq

/-- All distinct F55-B presented path-cell generators preserve the
F44 boundary interpretation. We KEEP the Type-valued proof-relevant
cell: the two actual paths are not declared equal as raw routes. -/
theorem OriginalF45BracketTree.DepthRotationRoute.PresentedCell.both_routes_toClass
    {a b : D} {x y : E} {n n' m m' : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    {first : OriginalF45BracketTree n m ma pa mb pb}
    {last : OriginalF45BracketTree n' m' ma pa mb pb}
    {r s : OriginalF45BracketTree.DepthRotationRoute first last}
    (cell : OriginalF45BracketTree.DepthRotationRoute.PresentedCell r s) :
    (ExchangeClass.castDepths r.depthEq.1 r.depthEq.2
      first.toExchangeClass = last.toExchangeClass) ∧
    (ExchangeClass.castDepths s.depthEq.1 s.depthEq.2
      first.toExchangeClass = last.toExchangeClass) :=
  ⟨r.toExchangeClass_eq, s.toExchangeClass_eq⟩

#print axioms OriginalF45BracketTree.DepthRotationRoute.depthEq
#print axioms OriginalF45BracketTree.DepthRotationRoute.toExchangeClass_eq
#print axioms OriginalF45BracketTree.DepthRotationRoute.axisHistories_eq
#print axioms OriginalF45BracketTree.DepthRotationRoute.pentagonLong_toClass
#print axioms OriginalF45BracketTree.DepthRotationRoute.pentagonShort_toClass
#print axioms OriginalF45BracketTree.DepthRotationRoute.PresentedCell.both_routes_toClass

end
end KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid
