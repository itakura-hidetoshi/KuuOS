import Kuu.F112.PolygonNativeC60TypedDiamondGeometricCoherence

/-!
# F112-P94D3CG — actual C60 AU positive-diamond existence obstruction

CF supplies a genuine dependent four-primitive positive-16D diamond
and its exact free-holonomy comparison, but DOES NOT assert that four
original C60 AU generators of this shape exist.

CG examines the genuinely specified native C60 context-closed BC
generator family. Every positively oriented AU generator starts at an
original 15D source-first naturality term, whose leading syntactic
constructor is conservatively tagged TRUE. This holds for EVERY
native 15D witness and EVERY finite physical AQ context because
BC's proven genuine whiskering preserves the tag.

In contrast, the target-first 15D term of the ACTUAL physical AQ
EXCHANGE naturality comparison carries FALSE. Its tag stays FALSE
under every actual finite physical context.

It follows unconditionally that the physical exchange 16D arrow has
NO subsequent positive primitive BC generator. No nonempty positive
typed BC chain can begin at that target, and that concrete target
cannot be either internal 15D middle object of CF's positive diamond.
Thus the naive extension of the specific physical AU generator into
a FOUR-INDEPENDENT-POSITIVE-EDGE diamond is obstructed already at
genuine dependent generator typing, BEFORE any holonomy comparison.

This does NOT forbid other positive two-step paths on other original
15D terms, genuine mixed-sign triangles, or independent geometric
fillers in an explicitly DIFFERENT presentation. The physical edge
itself genuinely EXISTS in the chosen optional BC presentation,
preserves the original noncommutative Peiffer values at its two
different 15D endpoints, and has nontrivial full free holonomy.

No new axioms, sorry/admit, Gray, global horizontal Peiffer,
geometric 16D filler, P92B descent, strict 3/n, or root changes.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uD vD uE vE

section PhysicalC60

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

/-- The actual physical contextual source-first 15D AU naturality
proof term, not an observer or a synthetic graph vertex. -/
def nativeK5CGPhysicalSource
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool) : (nativeK5AXBaseLayer W).Total :=
  nativeK5BCContext W word
    (nativeK5AXPack W
      (nativeK5AUNaturalityViaSource W (nativeK5AQExchange W [])))

/-- The actual contextual target-first 15D AU naturality proof term
from the SAME original thirteen-cell and AQ exchange. -/
def nativeK5CGPhysicalTarget
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool) : (nativeK5AXBaseLayer W).Total :=
  nativeK5BCContext W word
    (nativeK5AXPack W
      (nativeK5AUNaturalityViaTarget W (nativeK5AQExchange W [])))

/-- Every positive genuine BC generator, independently of its actual
underlying 15D witness, has a source-first 15D object. The TRUE tag
is preserved under its EXACT given finite C60 context. -/
theorem nativeK5CGAll_positive_sources_true
    (W : NativeK5StructuralThirteenCell p U V)
    {source target : (nativeK5AXBaseLayer W).Total}
    (g : (nativeK5BCSignature W).Gen source target) :
    nativeK5AYRawLeading W source = true := by
  rcases g with ⟨steps, x₀, y₀, ⟨g₀, hx, hy⟩⟩
  rcases g₀ with ⟨R, T, cell, hsrc, htgt⟩
  rw [hx, hsrc]
  change nativeK5AYRawLeading W
      (nativeK5BCContext W steps
        (nativeK5AXPack W (nativeK5AUNaturalityViaSource W cell))) = true
  rw [nativeK5BCContext_pack W steps _]
  change nativeK5AXLeadingConservative W
      (nativeK5AQContextCell W steps
        (nativeK5AUNaturalityViaSource W cell)) = true
  rw [nativeK5BCLeading_context W steps]
  rfl

/-- Physical source-first AU naturality remains TRUE after ANY
finite genuine AQ context word. -/
theorem nativeK5CGPhysical_source_true
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool) :
    nativeK5AYRawLeading W (nativeK5CGPhysicalSource W word) = true := by
  unfold nativeK5CGPhysicalSource
  rw [nativeK5BCContext_pack W word _]
  change nativeK5AXLeadingConservative W
      (nativeK5AQContextCell W word
        (nativeK5AUNaturalityViaSource W (nativeK5AQExchange W []))) = true
  rw [nativeK5BCLeading_context W word]
  rfl

/-- The target-first comparison at the ACTUAL native AQ exchange
has FALSE leading constructor, preserved by each true AQ frame.
This is deliberately NOT asserted for every possible input 15D cell. -/
theorem nativeK5CGPhysical_target_false
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool) :
    nativeK5AYRawLeading W (nativeK5CGPhysicalTarget W word) = false := by
  unfold nativeK5CGPhysicalTarget
  rw [nativeK5BCContext_pack W word _]
  change nativeK5AXLeadingConservative W
      (nativeK5AQContextCell W word
        (nativeK5AUNaturalityViaTarget W (nativeK5AQExchange W []))) = false
  rw [nativeK5BCLeading_context W word]
  rfl

/-- The real, optional AU 16D BC generator at this exact physical
context has both original 15D endpoints explicitly as dependent types. -/
def nativeK5CGPhysicalPositiveGenerator
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool) :
    (nativeK5BCSignature W).Gen
      (nativeK5CGPhysicalSource W word)
      (nativeK5CGPhysicalTarget W word) :=
  nativeC60BCGen (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
    word ⟨_, _, nativeK5AQExchange W [], rfl, rfl⟩

/-- The ACTUAL physical target cannot be the source of even ONE
further positive BC generator, for EVERY independent target 15D proof
object. This is a genuine generator-existence no-go, not a claim
about abstract arrows in the selected groupoid completion. -/
theorem nativeK5CGPhysical_no_positive_successor
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool)
    (next : (nativeK5AXBaseLayer W).Total) :
    ¬ Nonempty ((nativeK5BCSignature W).Gen
      (nativeK5CGPhysicalTarget W word) next) := by
  rintro ⟨g⟩
  have h := nativeK5CGAll_positive_sources_true W g
  rw [nativeK5CGPhysical_target_false W word] at h
  cases h

/-- Indeed, no positive BC chain of ANY nonzero finite length can
start at the target of this actual physical naturality primitive.
All original intermediate 15D objects remain indexed. -/
theorem nativeK5CGPhysical_no_nonempty_positive_chain
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool)
    (next : (nativeK5AXBaseLayer W).Total)
    (tail : List (nativeK5AXBaseLayer W).Total) :
    ¬ Nonempty (NativeC60BZPositiveChain
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
      (nativeK5CGPhysicalTarget W word) (next :: tail)) := by
  rintro ⟨chain⟩
  cases chain with
  | cons g rest =>
      exact nativeK5CGPhysical_no_positive_successor W word next ⟨g⟩

/-- For ANY genuine four-primitive all-positive C60 diamond, BOTH
dependent intermediate objects must be source-first TRUE-tagged.
The existence of its four edges is already encoded in CF's type. -/
theorem nativeK5CGEvery_diamond_midpoints_true
    (W : NativeK5StructuralThirteenCell p U V)
    (q : NativeC60CFTypedDiamond
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)) :
    nativeK5AYRawLeading W q.leftMid = true ∧
      nativeK5AYRawLeading W q.rightMid = true :=
  ⟨nativeK5CGAll_positive_sources_true W q.leftSecond,
    nativeK5CGAll_positive_sources_true W q.rightSecond⟩

/-- The concrete target of the genuine physical AU exchange
comparison can be NEITHER 15D midpoint of ANY four-positive-edge
native C60 diamond. This explicitly closes CF's outstanding
existence question for that physical candidate; it does not rule
out other diamonds with different original 15D middle cells. -/
theorem nativeK5CGPhysical_target_not_diamond_midpoint
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool)
    (q : NativeC60CFTypedDiamond
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)) :
    q.leftMid ≠ nativeK5CGPhysicalTarget W word ∧
      q.rightMid ≠ nativeK5CGPhysicalTarget W word := by
  obtain ⟨hl, hr⟩ := nativeK5CGEvery_diamond_midpoints_true W q
  constructor
  · intro h
    rw [h, nativeK5CGPhysical_target_false W word] at hl
    cases hl
  · intro h
    rw [h, nativeK5CGPhysical_target_false W word] at hr
    cases hr

/-- Actual positive existence versus lack of a positive successor:
the source/target are different original fifteen-dimensional raw proofs,
their physical Peiffer values agree, and the complete free 16D holonomy
of this physical primitive remains nonidentity under ANY finite word.
Thus a nontrivial 16D arrow does NOT imply availability of four
independent positive edges for a geometric diamond. -/
theorem nativeK5CGPhysical_generator_existence_and_obstruction
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool) :
    Nonempty ((nativeK5BCSignature W).Gen
      (nativeK5CGPhysicalSource W word)
      (nativeK5CGPhysicalTarget W word)) ∧
    nativeK5CGPhysicalSource W word ≠ nativeK5CGPhysicalTarget W word ∧
    nativeK5AXPeiffer W (nativeK5CGPhysicalSource W word) =
      nativeK5AXPeiffer W (nativeK5CGPhysicalTarget W word) ∧
    (∀ next : (nativeK5AXBaseLayer W).Total,
      ¬ Nonempty ((nativeK5BCSignature W).Gen
        (nativeK5CGPhysicalTarget W word) next)) ∧
    nativeC60BWFreeHolonomy (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W)
        (nativeK5BCClosedContextStep W word
          (nativeK5BSNaturality_declared_bridge W)) ≠
      (1 : FreeGroup
        (NativeC60BVGeneratorCode (nativeK5AXKuuSignature W))) := by
  refine ⟨⟨nativeK5CGPhysicalPositiveGenerator W word⟩, ?_, ?_, ?_, ?_⟩
  · exact nativeK5BCContextualPacked_raw_ne W word
  · exact nativeK5BCContextualNaturality_peiffer W word
      (nativeK5AQExchange W [])
  · intro next
    exact nativeK5CGPhysical_no_positive_successor W word next
  · exact nativeK5CEPhysicalAU_all_frames_nontrivial W word

end PhysicalC60

#print axioms nativeK5CGAll_positive_sources_true
#print axioms nativeK5CGPhysical_source_true
#print axioms nativeK5CGPhysical_target_false
#print axioms nativeK5CGPhysical_no_positive_successor
#print axioms nativeK5CGPhysical_no_nonempty_positive_chain
#print axioms nativeK5CGEvery_diamond_midpoints_true
#print axioms nativeK5CGPhysical_target_not_diamond_midpoint
#print axioms nativeK5CGPhysical_generator_existence_and_obstruction

end
end Kuu.F112.Physical
