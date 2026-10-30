import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalTypedSyntaxCountability

/-!
# F112-P94D3GB — countability of TRUE recursive indexed 18D
# assoc/post/pre Type-valued generators from countable original
# lower AX primitive witnesses

GA faithfully reified original raw AXStep atom/refl/symm/trans syntax
by a partial dependent decoder and proved true raw17D Countable
from only countability of the original lower AX object and generator
families.

GB addresses the remaining original 18D recursive
NativeC60DREighteenAssocGen. The recursively nested associator
and pre/post whiskerings retain the complete ORIGINAL raw17D
Type-valued evidence and dependent endpoints. We encode this
specific indexed family into a separate FINITE plain three-
constructor syntax tree whose atom tokens are the complete raw17D
proof total. A partial dependent decoder checks actual original
endpoints before constructing each assoc/post/pre term. A strict
decode-encode left inverse witnesses faithful reification.

This proves the full 18D generator total and EVERY dependent
generator fiber Countable from countable original raw17D path
total. With GA, all required original source 18D Countable
follows from the LOWER original AX object and primitive Gen
Countable assumptions alone; the independent hgen18 hypothesis
from FZ/GA is removed. On genuine old FJ physical nonempty finite
AQ words, FU/FX/FY yield exact noncommutative normal generator
cardinality aleph-null under those explicit lower primitive
Countable assumptions. These assumptions are not inferred from
finite C60 geometric vertices.

Append-only. No sorry/admit/new axioms, Gray or invented geometric
19D filler. Retain 107 published roots, strict Kuu core and
independent Kuu presentation, genuine signed noncommutative
free group and all original 14D–18D Type-valued proof data.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical

open CategoryTheory Cardinal
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u uD vD uE vE

/-- Finite unindexed SYNTAX only. An Atom is the WHOLE original
dependent source/target and original raw17D proof term, not a
numerical/parity/proof-truncated observation. Typed semantics
is recovered ONLY by the partial decoder below. -/
inductive NativeC60GBPlainAssocSyntax (Atom : Type u) : Type u where
  | assoc (f g h : Atom)
  | post (r : NativeC60GBPlainAssocSyntax Atom) (h : Atom)
  | pre (h : Atom) (r : NativeC60GBPlainAssocSyntax Atom)
  deriving Countable

/-- Original full raw17D path, with the entire lower Type-valued
source and target proofs stored in its dependent Sigma. -/
abbrev NativeC60GBOriginalRaw17Total
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L) : Type u :=
  NativeC60GAOriginalPathTotal (nativeC60DQTriangleSeventeenSignature S F)

/-- The actual total of the original INDEXED 18D recursive
assoc/post/pre generators with original source and target
objects. Distinct Type-valued proofs are not quotiented. -/
abbrev NativeC60GBOriginalEighteenGenTotal
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L) : Type u :=
  Σ ep : ((nativeC60DREighteenLayer S F).Total ×
    (nativeC60DREighteenLayer S F).Total),
    NativeC60DREighteenAssocGen S F ep.1 ep.2

/-- Encode each original 18D indexed generator into finite
syntax with COMPLETE raw17D proof tokens, by true recursion on
the original three constructor families. -/
def nativeC60GBEncodeGen
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L) :
    {x y : (nativeC60DREighteenLayer S F).Total} →
    NativeC60DREighteenAssocGen S F x y →
      NativeC60GBPlainAssocSyntax (NativeC60GBOriginalRaw17Total S F)
  | _, _, .assoc f g h =>
      .assoc ⟨(_, _), f⟩ ⟨(_, _), g⟩ ⟨(_, _), h⟩
  | _, _, .post r h =>
      .post (nativeC60GBEncodeGen S F r) ⟨(_, _), h⟩
  | _, _, .pre h r =>
      .pre ⟨(_, _), h⟩ (nativeC60GBEncodeGen S F r)

/-- Decode a proposed assoc triple ONLY when all ORIGINAL
dependent raw17D path boundaries compose, retaining actual
three raw17D paths and genuine source/target bracketings. -/
noncomputable def nativeC60GBDecodeAssoc
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (ff gg hh : NativeC60GBOriginalRaw17Total S F) :
    Option (NativeC60GBOriginalEighteenGenTotal S F) := by
  classical
  rcases ff with ⟨⟨a, b⟩, f⟩
  rcases gg with ⟨⟨b', c⟩, g⟩
  rcases hh with ⟨⟨c', d⟩, h⟩
  by_cases hbg : b = b'
  · subst b'
    by_cases hch : c = c'
    · subst c'
      exact some ⟨
        (nativeC60DRPackSeventeen S F (.trans (.trans f g) h),
         nativeC60DRPackSeventeen S F (.trans f (.trans g h))),
        .assoc f g h⟩
    · exact none
  · exact none

/-- Decode genuine POST whiskering only when original
complete source/target raw17D endpoints are parallel and
the new raw17D path starts at the precise shared target. -/
noncomputable def nativeC60GBDecodePost
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (rr : NativeC60GBOriginalEighteenGenTotal S F)
    (hh : NativeC60GBOriginalRaw17Total S F) :
    Option (NativeC60GBOriginalEighteenGenTotal S F) := by
  classical
  rcases rr with ⟨⟨⟨⟨a, b⟩, p⟩, ⟨⟨a', b'⟩, q⟩⟩, r⟩
  rcases hh with ⟨⟨z, c⟩, h⟩
  by_cases heq : a = a' ∧ b = b'
  · rcases heq with ⟨ha, hb⟩
    subst a'
    subst b'
    by_cases hmatch : b = z
    · subst z
      exact some ⟨
        (nativeC60DRPackSeventeen S F (.trans p h),
         nativeC60DRPackSeventeen S F (.trans q h)),
        .post r h⟩
    · exact none
  · exact none

/-- Decode genuine PRE whiskering only when all original
dependent raw17D source/target boundaries compose. -/
noncomputable def nativeC60GBDecodePre
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (hh : NativeC60GBOriginalRaw17Total S F)
    (rr : NativeC60GBOriginalEighteenGenTotal S F) :
    Option (NativeC60GBOriginalEighteenGenTotal S F) := by
  classical
  rcases hh with ⟨⟨a, z⟩, h⟩
  rcases rr with ⟨⟨⟨⟨b, c⟩, p⟩, ⟨⟨b', c'⟩, q⟩⟩, r⟩
  by_cases heq : b = b' ∧ c = c'
  · rcases heq with ⟨hb, hc⟩
    subst b'
    subst c'
    by_cases hmatch : z = b
    · subst z
      exact some ⟨
        (nativeC60DRPackSeventeen S F (.trans h p),
         nativeC60DRPackSeventeen S F (.trans h q)),
        .pre h r⟩
    · exact none
  · exact none

/-- A partial decoder for actual 18D original assoc/post/pre
grammar; ill-typed proposed compositions return none.
The original indexed generator object is recovered in full
for every genuine source 18D generator. -/
noncomputable def nativeC60GBDecodeGen
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L) :
    NativeC60GBPlainAssocSyntax (NativeC60GBOriginalRaw17Total S F) →
      Option (NativeC60GBOriginalEighteenGenTotal S F)
  | .assoc f g h => nativeC60GBDecodeAssoc S F f g h
  | .post r h =>
      (nativeC60GBDecodeGen S F r).bind
        (fun rr => nativeC60GBDecodePost S F rr h)
  | .pre h r =>
      (nativeC60GBDecodeGen S F r).bind
        (fun rr => nativeC60GBDecodePre S F h rr)

/-- Strict faithfulness: decode-encode is the identity on
EVERY original recursively indexed 18D generator. No quotient,
proposition-only truncation or encoding irreversibility. -/
theorem nativeC60GBDecode_encodeGen
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {x y : (nativeC60DREighteenLayer S F).Total}
    (r : NativeC60DREighteenAssocGen S F x y) :
    nativeC60GBDecodeGen S F (nativeC60GBEncodeGen S F r) =
      some (⟨(x, y), r⟩ : NativeC60GBOriginalEighteenGenTotal S F) := by
  induction r with
  | assoc f g h =>
      simp [nativeC60GBDecodeGen, nativeC60GBEncodeGen,
        nativeC60GBDecodeAssoc]
  | post r h ih =>
      simp [nativeC60GBDecodeGen, nativeC60GBEncodeGen, ih,
        nativeC60GBDecodePost, nativeC60DRPackSeventeen]
  | pre h r ih =>
      simp [nativeC60GBDecodeGen, nativeC60GBEncodeGen, ih,
        nativeC60GBDecodePre, nativeC60DRPackSeventeen]

/-- All original 18D recursively typed generators are Countable
under countability of the ACTUAL complete raw17D path total;
the proof uses a true reification certificate, not a scalar
projection of dependent source proofs. -/
theorem nativeC60GBOriginalEighteenGenTotal_countable
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (hraw : Countable (NativeC60GBOriginalRaw17Total S F)) :
    Countable (NativeC60GBOriginalEighteenGenTotal S F) := by
  letI : Countable (NativeC60GBOriginalRaw17Total S F) := hraw
  haveI : Countable
      (NativeC60GBPlainAssocSyntax (NativeC60GBOriginalRaw17Total S F)) :=
    inferInstance
  have hrange :
      (Set.range (nativeC60GBDecodeGen S F)).Countable :=
    Set.countable_range _
  letI : Countable (Set.range (nativeC60GBDecodeGen S F)) :=
    hrange.to_subtype
  let embedding : NativeC60GBOriginalEighteenGenTotal S F →
      Set.range (nativeC60GBDecodeGen S F) :=
    fun t =>
      ⟨some t, by
        rcases t with ⟨⟨x, y⟩, r⟩
        exact ⟨nativeC60GBEncodeGen S F r,
          nativeC60GBDecode_encodeGen S F r⟩⟩
  have hinj : Function.Injective embedding := by
    intro t t' h
    have hsome :
        (some t : Option (NativeC60GBOriginalEighteenGenTotal S F)) = some t' :=
      congrArg
        (fun z : Set.range (nativeC60GBDecodeGen S F) => z.1) h
    exact Option.some.inj hsome
  exact hinj.countable

/-- Every actual dependent assoc/post/pre original Gen x y
fiber is Countable; no separate hgen18 condition is needed
once original raw17D proof total is Countable. -/
theorem nativeC60GBOriginalEighteenGenFiber_countable
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (hraw : Countable (NativeC60GBOriginalRaw17Total S F))
    (x y : (nativeC60DREighteenLayer S F).Total) :
    Countable (NativeC60DREighteenAssocGen S F x y) := by
  letI : Countable (NativeC60GBOriginalEighteenGenTotal S F) :=
    nativeC60GBOriginalEighteenGenTotal_countable S F hraw
  have hinj : Function.Injective
      (fun r : NativeC60DREighteenAssocGen S F x y =>
        (⟨(x, y), r⟩ : NativeC60GBOriginalEighteenGenTotal S F)) := by
    intro r s h
    exact eq_of_heq (Sigma.mk.inj h).2
  exact hinj.countable

section OriginalDependentEighteenClosure

variable {L : NativeC60AXLayer.{u}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- FULL ORIGINAL 18D proof-bearing source Countable from
only original lower AX object and primitive AX Gen smallness.
GA discharges all 16D/17D raw syntax. GB now discharges the
18D recursive assoc/post/pre generator fiber as well. -/
theorem nativeC60GBOriginal18_countable_of_lower_primitive
    (hobj : Countable L.Total)
    (hgen : ∀ x y : L.Total, Countable (S.Gen x y)) :
    Countable (NativeC60DSCompleteEighteenCode S F) := by
  have hobj17 :
      Countable (nativeC60DQSeventeenLayer S F).Total :=
    nativeC60GASeventeenObject_countable_of_lower_primitive S F hobj hgen
  have hgen17 : ∀ x y : (nativeC60DQSeventeenLayer S F).Total,
      Countable ((nativeC60DQTriangleSeventeenSignature S F).Gen x y) :=
    nativeC60GATrianglePrimitive_countable S F hobj hgen
  have hraw :
      Countable (NativeC60GBOriginalRaw17Total S F) :=
    nativeC60GAOriginalRawPathTotal_countable
      (nativeC60DQTriangleSeventeenSignature S F) hobj17 hgen17
  exact nativeC60GAOriginal18_countable_of_lower_primitive_and_gen18 S F
    hobj hgen
    (nativeC60GBOriginalEighteenGenFiber_countable S F hraw)

end OriginalDependentEighteenClosure

section ActualPhysicalClosure

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

/-- Countability of the ORIGINAL true physical 18D alphabet is
concluded from ORIGINAL base AX object and primitive Gen fibers
only. No 18D assoc/post/pre fiber Countable is postulated. -/
theorem nativeK5GBPhysicalOriginal18_countable_of_lower_primitive
    (W : NativeK5StructuralThirteenCell p U V)
    (hobj : Countable (nativeK5AXBaseLayer W).Total)
    (hgen : ∀ x y : (nativeK5AXBaseLayer W).Total,
      Countable ((nativeK5AXKuuSignature W).Gen x y)) :
    Countable (NativeC60DSCompleteEighteenCode
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)) :=
  nativeC60GBOriginal18_countable_of_lower_primitive
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W) hobj hgen

/-- On every nonempty genuine physical C60 AQ word, the WHOLE
original signed NONCOMMUTATIVE full-DV kernel has exact minimum
normal-generator cardinal aleph-null from only Countable original
base AX objects and original primitive Gen fibers. Lower 14D
categorical/proof source Countable is still explicitly required. -/
theorem nativeK5GBPhysical_exactAleph0NormalRank_of_lower_primitive
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool) (hne : word ≠ [])
    (hobj : Countable (nativeK5AXBaseLayer W).Total)
    (hgen : ∀ x y : (nativeK5AXBaseLayer W).Total,
      Countable ((nativeK5AXKuuSignature W).Gen x y)) :
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
  nativeK5FYPhysical_fullDV_exactAleph0NormalRank_of_sourceCountable
    W word hne
    (nativeK5GBPhysicalOriginal18_countable_of_lower_primitive W hobj hgen)

end ActualPhysicalClosure

#print axioms nativeC60GBDecode_encodeGen
#print axioms nativeC60GBOriginalEighteenGenTotal_countable
#print axioms nativeC60GBOriginalEighteenGenFiber_countable
#print axioms nativeC60GBOriginal18_countable_of_lower_primitive
#print axioms nativeK5GBPhysicalOriginal18_countable_of_lower_primitive
#print axioms nativeK5GBPhysical_exactAleph0NormalRank_of_lower_primitive

end
end Kuu.F112.Physical
