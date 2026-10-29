import Mathlib.Tactic.DeriveCountable
import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalRawCountabilityGate

/-!
# F112-P94D3GA — actual indexed raw17D free syntax has countable fibers
# from countable primitive typed signatures

FZ left the Countable assumption for full raw17D paths explicit.
The existing NativeC60AXStep is a genuinely indexed dependent
inductive with atom/refl/symm/trans constructors. Direct automatic
Countable deriving on the original indexed family is NOT licensed
without arbitrary S.Gen x y evidence being countable.

GA constructs a new *untyped but proof-bearing finite syntax tree*
with primitive tokens holding actual dependent endpoints, and
a partial interpretation BACK to the complete original indexed
AXStep dependent Sigma. Every actual original typed path is a
faithfully decoded syntax tree (no quotation axioms or sorry).
Countability of the finite syntax follows from the countability
of original AX objects and exact original primitive generator
fibers. We do NOT identify original typed proofs with their
untyped syntax shadows: a genuine partial reification certificate
is supplied, and no original definition is overwritten.

FZ's physical 18D full-kernel normal-rank gate is then improved:
the exact original raw17D proof FIBER Countable premise is
derived, under explicit Countable native17D objects and primitive
native17D generator fibers. Countability of the recursive
original 18D assoc/post/pre generator fibers remains separate
until proved.

Pinned Lean v4.30.0-rc2 and mathlib SHA. Append-only, 107 roots,
strict Kuu core primary, independent Kuu presentation, no Gray,
no new axioms, sorry or admit. Retain all original Type-valued
14D–18D witnesses, genuine FJ no-go and distinct FK–FM frame,
no invented geometric 19D filling or global strict hyperdescent.
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

/-- A finite UNSIGNED syntax expression recording original
primitive proof-bearing atoms and original objects as tokens.
This is only a code; it is NOT the original indexed raw proof
type, nor a quotient of its dependent endpoint data. -/
inductive NativeC60GAPlainRawSyntax (Atom Obj : Type u) : Type u where
  | atom (g : Atom)
  | refl (x : Obj)
  | symm (p : NativeC60GAPlainRawSyntax Atom Obj)
  | trans (p q : NativeC60GAPlainRawSyntax Atom Obj)
  deriving Countable

/-- Exact dependent ORIGINAL primitive proof token, including
both original proof-relevant endpoints. -/
abbrev NativeC60GAOriginalAtomTotal
    {L : NativeC60AXLayer.{u}} (S : NativeC60AXSignature L) : Type u :=
  Σ x : L.Total, Σ y : L.Total, S.Gen x y

/-- The actual original fully typed raw-path total. Its index is
the genuine endpoint PAIR, not a flattened string. -/
abbrev NativeC60GAOriginalPathTotal
    {L : NativeC60AXLayer.{u}} (S : NativeC60AXSignature L) : Type u :=
  Σ ep : L.Total × L.Total, NativeC60AXStep S ep.1 ep.2

/-- Encode any genuinely indexed original proof path by a finite
syntax expression, remembering its ORIGINAL atom witnesses. -/
def nativeC60GAEncodeRaw
    {L : NativeC60AXLayer.{u}} (S : NativeC60AXSignature L) :
    {x y : L.Total} → NativeC60AXStep S x y →
      NativeC60GAPlainRawSyntax (NativeC60GAOriginalAtomTotal S) L.Total
  | _, _, .atom g => .atom ⟨_, _, g⟩
  | _, _, .refl x => .refl x
  | _, _, .symm h => .symm (nativeC60GAEncodeRaw S h)
  | _, _, .trans h k =>
      .trans (nativeC60GAEncodeRaw S h) (nativeC60GAEncodeRaw S k)

/-- Decode syntactic terms PARTIALLY back into the exact
dependent original source/target and original AXStep. In the
trans case, the original endpoints MUST coincide; no
unjustified conversion between different dependent fibers
is introduced. -/
noncomputable def nativeC60GADecodeRaw
    {L : NativeC60AXLayer.{u}} (S : NativeC60AXSignature L) :
    NativeC60GAPlainRawSyntax (NativeC60GAOriginalAtomTotal S) L.Total →
      Option (NativeC60GAOriginalPathTotal S)
  | .atom ⟨x, y, g⟩ => some ⟨(x, y), .atom g⟩
  | .refl x => some ⟨(x, x), .refl x⟩
  | .symm h =>
      (nativeC60GADecodeRaw S h).bind
        (fun ⟨⟨x, y⟩, p⟩ => some ⟨(y, x), .symm p⟩)
  | .trans h k => by
      classical
      exact (nativeC60GADecodeRaw S h).bind
        (fun ⟨⟨x, y⟩, p⟩ =>
          (nativeC60GADecodeRaw S k).bind
            (fun ⟨⟨z, w⟩, q⟩ =>
              if hz : y = z then
                some ⟨(x, w), .trans p (hz.symm ▸ q)⟩
              else none))

/-- The partial decoder is an EXACT LEFT INVERSE on every
original dependent raw proof, including arbitrary raw
symmetry and composition nesting. -/
theorem nativeC60GADecode_encodeRaw
    {L : NativeC60AXLayer.{u}} (S : NativeC60AXSignature L)
    {x y : L.Total} (p : NativeC60AXStep S x y) :
    nativeC60GADecodeRaw S (nativeC60GAEncodeRaw S p) =
      some (⟨(x, y), p⟩ : NativeC60GAOriginalPathTotal S) := by
  induction p with
  | atom g => rfl
  | refl a => rfl
  | symm h ih =>
      simp [nativeC60GAEncodeRaw, nativeC60GADecodeRaw, ih]
  | trans h k ih ik =>
      simp [nativeC60GAEncodeRaw, nativeC60GADecodeRaw, ih, ik]

/-- The full original AXStep dependent Sigma type is Countable
as soon as its original source/target objects and primitive
typed atom fibers are Countable. This is STRONGER than FZ's
old assumption of Countable arbitrary raw path fibers. -/
theorem nativeC60GAOriginalRawPathTotal_countable
    {L : NativeC60AXLayer.{u}} (S : NativeC60AXSignature L)
    (hobj : Countable L.Total)
    (hgen : ∀ x y : L.Total, Countable (S.Gen x y)) :
    Countable (NativeC60GAOriginalPathTotal S) := by
  letI : Countable L.Total := hobj
  letI : ∀ x y : L.Total, Countable (S.Gen x y) := hgen
  haveI : Countable (NativeC60GAOriginalAtomTotal S) := inferInstance
  haveI : Countable
      (NativeC60GAPlainRawSyntax (NativeC60GAOriginalAtomTotal S) L.Total) :=
    inferInstance
  have hrange :
      (Set.range (nativeC60GADecodeRaw S)).Countable :=
    Set.countable_range _
  letI : Countable (Set.range (nativeC60GADecodeRaw S)) :=
    hrange.to_subtype
  let embedding : NativeC60GAOriginalPathTotal S →
      Set.range (nativeC60GADecodeRaw S) :=
    fun t =>
      ⟨some t, by
        rcases t with ⟨⟨x, y⟩, p⟩
        exact ⟨nativeC60GAEncodeRaw S p,
          nativeC60GADecode_encodeRaw S p⟩⟩
  have hinj : Function.Injective embedding := by
    intro t t' h
    have hsome :
        (some t : Option (NativeC60GAOriginalPathTotal S)) = some t' :=
      congrArg
        (fun z : Set.range (nativeC60GADecodeRaw S) => z.1) h
    exact Option.some.inj hsome
  exact hinj.countable

/-- Every individual indexed original raw AXStep proof fiber is
Countable from original primitive proof fibers, regardless of
the finite number of nested symm/trans constructors. -/
theorem nativeC60GAOriginalRawPathFiber_countable
    {L : NativeC60AXLayer.{u}} (S : NativeC60AXSignature L)
    (hobj : Countable L.Total)
    (hgen : ∀ x y : L.Total, Countable (S.Gen x y))
    (x y : L.Total) :
    Countable (NativeC60AXStep S x y) := by
  letI : Countable (NativeC60GAOriginalPathTotal S) :=
    nativeC60GAOriginalRawPathTotal_countable S hobj hgen
  have hinj : Function.Injective
      (fun p : NativeC60AXStep S x y =>
        (⟨(x, y), p⟩ : NativeC60GAOriginalPathTotal S)) := by
    intro p q h
    exact eq_of_heq (Sigma.mk.inj h).2
  exact hinj.countable

section ActualRawSeventeen

variable {L : NativeC60AXLayer.{u}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- A GENUINE indexed 17D raw-path Countable theorem, derived
from the ACTUAL original triangle primitive Gen fibers and
actual original 17D objects, not postulated for all paths. -/
theorem nativeC60GAOriginal17RawPath_countable_of_primitive
    (hobj : Countable (nativeC60DQSeventeenLayer S F).Total)
    (hgen : ∀ x y : (nativeC60DQSeventeenLayer S F).Total,
      Countable ((nativeC60DQTriangleSeventeenSignature S F).Gen x y))
    (x y : (nativeC60DQSeventeenLayer S F).Total) :
    Countable (NativeC60AXStep
      (nativeC60DQTriangleSeventeenSignature S F) x y) :=
  nativeC60GAOriginalRawPathFiber_countable
    (nativeC60DQTriangleSeventeenSignature S F) hobj hgen x y

/-- Reaching the real full proof-relevant 18D source alphabet
now needs only (i) actual original 17D object Countable,
(ii) actual ORIGINAL primitive triangle generator fibers
Countable, (iii) actual 18D assoc/post/pre generator fibers
Countable. The old FZ raw17D path Countable hypothesis has
been DISCHARGED by the actual four-constructor syntax. -/
theorem nativeC60GAOriginal18_countable_of_primitive17_and_gen18
    (hobj : Countable (nativeC60DQSeventeenLayer S F).Total)
    (hgen17 : ∀ x y : (nativeC60DQSeventeenLayer S F).Total,
      Countable ((nativeC60DQTriangleSeventeenSignature S F).Gen x y))
    (hgen18 : ∀ x y : (nativeC60DREighteenLayer S F).Total,
      Countable ((nativeC60DREighteenAssocSignature S F).Gen x y)) :
    Countable (NativeC60DSCompleteEighteenCode S F) :=
  nativeC60FZFullOriginalEighteen_countable_of_rawAndGen
    S F hobj
    (nativeC60GAOriginal17RawPath_countable_of_primitive S F hobj hgen17)
    hgen18

end ActualRawSeventeen


/-!
## Closed 16D and triangular 17D primitive Countable propagation

The actual BC finite-context closed generator has precisely the
dependent token (List Bool, original endpoint pair, original Gen)
with original endpoint transport equality proofs. The selected
DQ triangle Gen stores TWO original raw16D paths and the
original proof-relevant triangle presentation relation, which
is a Prop and hence cannot introduce an extra cardinal source.

GA's faithful decoder therefore propagates Countable from the
original lower AX layer and its primitive Gen fibers through
the actual BC closed-16D context grammar into the actual DQ
17D object and primitive signature, and THEN through the
raw17D 4-constructor syntax to the actual next 18D layer.
Only the ORIGINAL 18D recursive assoc/post/pre generator
Countable premise remains open.
-/

section ActualClosedAndTrianglePrimitiveCountability

variable {L : NativeC60AXLayer.{u}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- Every TRUE BC context-closed 16D primitive proof fiber is
Countable if the original lower AX objects and primitive Gen
fibers are Countable. The full arbitrary finite Bool context
word and actual original lower Type-valued generator are retained. -/
theorem nativeC60GAClosedPrimitive_countable
    (hobj : Countable L.Total)
    (hgen : ∀ a b : L.Total, Countable (S.Gen a b))
    (x y : L.Total) :
    Countable ((nativeC60BCClosedSignature S F).Gen x y) := by
  letI : Countable L.Total := hobj
  letI : ∀ a b : L.Total, Countable (S.Gen a b) := hgen
  change Countable
    (Σ steps : List Bool, Σ a : L.Total, Σ b : L.Total,
      {g : S.Gen a b //
        x = nativeC60BCContextTotal F steps a ∧
        y = nativeC60BCContextTotal F steps b})
  infer_instance

/-- Whole original BC raw16D proof alphabet, with endpoint pair
and raw proof retained, is Countable under the same lower data. -/
theorem nativeC60GAClosedRawSixteenTotal_countable
    (hobj : Countable L.Total)
    (hgen : ∀ a b : L.Total, Countable (S.Gen a b)) :
    Countable
      (NativeC60GAOriginalPathTotal (nativeC60BCClosedSignature S F)) :=
  nativeC60GAOriginalRawPathTotal_countable
    (nativeC60BCClosedSignature S F)
    hobj
    (nativeC60GAClosedPrimitive_countable S F hobj hgen)

/-- Original DQ next-layer 17D *objects* are precisely the
dependent raw16D total. No proof is quotiented away. -/
theorem nativeC60GASeventeenObject_countable_of_lower_primitive
    (hobj : Countable L.Total)
    (hgen : ∀ a b : L.Total, Countable (S.Gen a b)) :
    Countable (nativeC60DQSeventeenLayer S F).Total := by
  change Countable
    (NativeC60GAOriginalPathTotal (nativeC60BCClosedSignature S F))
  exact nativeC60GAClosedRawSixteenTotal_countable S F hobj hgen

/-- The ACTUAL DQ structural 17D triangle primitive is
Countable under lower original primitive smallness.
Its original original16D pair of raw paths and original
Type-level dependent endpoints are stored, and the
zigzag/cancellation relation witness is a Prop. -/
theorem nativeC60GATrianglePrimitive_countable
    (hobj : Countable L.Total)
    (hgen : ∀ a b : L.Total, Countable (S.Gen a b))
    (x y : (nativeC60DQSeventeenLayer S F).Total) :
    Countable ((nativeC60DQTriangleSeventeenSignature S F).Gen x y) := by
  letI : Countable L.Total := hobj
  letI : ∀ a b : L.Total,
    Countable (NativeC60AXStep (nativeC60BCClosedSignature S F) a b) :=
    fun a b =>
      nativeC60GAOriginalRawPathFiber_countable
        (nativeC60BCClosedSignature S F) hobj
        (nativeC60GAClosedPrimitive_countable S F hobj hgen) a b
  change Countable
    (Σ a : L.Total, Σ b : L.Total,
      Σ c : NativeC60AXStep (nativeC60BCClosedSignature S F) a b,
        Σ d : NativeC60AXStep (nativeC60BCClosedSignature S F) a b,
          {r : NativeC60CFTriangleRelation S F c d //
            x = nativeC60DQPackSixteen S F c ∧
            y = nativeC60DQPackSixteen S F d})
  infer_instance

/-- The full ORIGINAL raw17D indexed proof fiber is Countable
directly from ORIGINAL lower AX primitive data, without any
separately postulated raw17D Countable or triangle primitive
Countable hypotheses. -/
theorem nativeC60GAOriginal17Path_countable_of_lower_primitive
    (hobj : Countable L.Total)
    (hgen : ∀ a b : L.Total, Countable (S.Gen a b))
    (x y : (nativeC60DQSeventeenLayer S F).Total) :
    Countable
      (NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) x y) :=
  nativeC60GAOriginal17RawPath_countable_of_primitive S F
    (nativeC60GASeventeenObject_countable_of_lower_primitive S F hobj hgen)
    (nativeC60GATrianglePrimitive_countable S F hobj hgen)
    x y

/-- The entire genuine original raw18D source alphabet is
Countable from ORIGINAL lower AX objects and primitive
AX Gen fibers, plus ONLY the remaining true recursive
18D assoc/post/pre generator fiber Countable gate. -/
theorem nativeC60GAOriginal18_countable_of_lower_primitive_and_gen18
    (hobj : Countable L.Total)
    (hgen : ∀ a b : L.Total, Countable (S.Gen a b))
    (hgen18 : ∀ x y : (nativeC60DREighteenLayer S F).Total,
      Countable ((nativeC60DREighteenAssocSignature S F).Gen x y)) :
    Countable (NativeC60DSCompleteEighteenCode S F) :=
  nativeC60GAOriginal18_countable_of_primitive17_and_gen18 S F
    (nativeC60GASeventeenObject_countable_of_lower_primitive S F hobj hgen)
    (nativeC60GATrianglePrimitive_countable S F hobj hgen)
    hgen18

end ActualClosedAndTrianglePrimitiveCountability

section ActualPhysicalLowerPrimitiveGate

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

/-- Real old FJ physical original 18D source becomes Countable
from exact primitive base-15D object/Gen Countable and the
still-explicit recursive assoc/post/pre generator-fiber
Countable premise. No categorical Hom or proof witness
countability is inferred from finite C60 geometry alone. -/
theorem nativeK5GAOriginalPhysical18_countable_of_lower_primitive
    (W : NativeK5StructuralThirteenCell p U V)
    (hobj : Countable (nativeK5AXBaseLayer W).Total)
    (hgen : ∀ a b : (nativeK5AXBaseLayer W).Total,
      Countable ((nativeK5AXKuuSignature W).Gen a b))
    (hgen18 : ∀ x y :
      (nativeC60DREighteenLayer
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W)).Total,
      Countable ((nativeC60DREighteenAssocSignature
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W)).Gen x y)) :
    Countable
      (NativeC60DSCompleteEighteenCode
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W)) :=
  nativeC60GAOriginal18_countable_of_lower_primitive_and_gen18
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
    hobj hgen hgen18

/-- The sharp old FJ physical normal rank aleph-null for EVERY
nonempty finite physical AQ context, conditional ONLY on
smallness of original base AX primitive data and original
recursive assoc/post/pre fibers; no full raw17D path-fiber
Countable premise is needed any longer. -/
theorem nativeK5GAPhysical_exactAleph0NormalRank_of_lower_primitive
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool) (hne : word ≠ [])
    (hobj : Countable (nativeK5AXBaseLayer W).Total)
    (hgen : ∀ a b : (nativeK5AXBaseLayer W).Total,
      Countable ((nativeK5AXKuuSignature W).Gen a b))
    (hgen18 : ∀ x y :
      (nativeC60DREighteenLayer
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W)).Total,
      Countable ((nativeC60DREighteenAssocSignature
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W)).Gen x y)) :
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
    (nativeK5GAOriginalPhysical18_countable_of_lower_primitive
      W hobj hgen hgen18)

end ActualPhysicalLowerPrimitiveGate

#print axioms nativeC60GADecode_encodeRaw
#print axioms nativeC60GAOriginalRawPathTotal_countable
#print axioms nativeC60GAOriginalRawPathFiber_countable
#print axioms nativeC60GAOriginal17RawPath_countable_of_primitive
#print axioms nativeC60GAOriginal18_countable_of_primitive17_and_gen18
#print axioms nativeC60GAClosedPrimitive_countable
#print axioms nativeC60GAClosedRawSixteenTotal_countable
#print axioms nativeC60GASeventeenObject_countable_of_lower_primitive
#print axioms nativeC60GATrianglePrimitive_countable
#print axioms nativeC60GAOriginal17Path_countable_of_lower_primitive
#print axioms nativeC60GAOriginal18_countable_of_lower_primitive_and_gen18
#print axioms nativeK5GAOriginalPhysical18_countable_of_lower_primitive
#print axioms nativeK5GAPhysical_exactAleph0NormalRank_of_lower_primitive

end
end Kuu.F112.Physical
