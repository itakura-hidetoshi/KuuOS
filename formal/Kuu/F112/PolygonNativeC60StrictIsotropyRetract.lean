import Kuu.F112.PolygonNativeC60SplitFreeForkFamily
import Mathlib.CategoryTheory.Endomorphism

/-!
# F112-P94D3CO — split free fork families in actual strict isotropy

CN constructs a split embedding into the full free-code group and separately
realizes finite signed words as original dependent CA chains. CO connects
these two constructions inside the EXISTING strict Kuu automorphism group.

Mathlib multiplies automorphisms in reverse categorical composition order.
We therefore explicitly use `(Aut X)ᵐᵒᵖ` for forward traversal order. This
is the actual strict automorphism carrier, not a new quotient or an observer
kernel. A second homomorphism into ordinary `Aut X` reverses each loop.

For every finite genuine AQ context, the fork-family free group embeds
into actual strict isotropy and admits a group-valued retraction from the
WHOLE isotropy group. The retraction is BW holonomy, BX prefix removal, and
CN decoding. CD faithfulness identifies the lifted group element with the
original typed CN word, retaining its original 15D endpoints and provenance.

The associated projector is idempotent. Collapsing a nonidentity fork word
prevents descent of this decoder. No assertion identifies this subgroup
with all isotropy, constructs geometric 16-cell coherence, or adds relations.
No Gray, new axioms, sorry/admit, or additional public roots.

Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u v uD vD uE vE

section Abstract

variable {L : NativeC60AXLayer.{u}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- The actual proof-bearing strict object after the finite AQ context. -/
def nativeC60COObject (word : List Bool) (a : L.Total) :
    NativeC60AZStrictSpace (nativeC60BCClosedSignature S F)
      (nativeC60AZNoRelations (nativeC60BCClosedSignature S F)) :=
  (nativeC60AZStrictProject (nativeC60BCClosedSignature S F)
    (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))).obj
      ⟨nativeC60BCContextTotal F word a⟩

/-- Actual strict automorphisms, with multiplication in path traversal order. -/
abbrev NativeC60COIsotropy (word : List Bool) (a : L.Total) :=
  (Aut (nativeC60COObject S F word a))ᵐᵒᵖ

/-- Package an original typed loop using the already proved strict inverse
laws. Neither the loop nor its inverse is inferred from a receiver value. -/
def nativeC60CORawLoop (word : List Bool) {a : L.Total}
    (c : NativeC60AXStep (nativeC60BCClosedSignature S F) a a) :
    NativeC60COIsotropy S F word a :=
  MulOpposite.op {
    hom := nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
      (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
      (nativeC60BCMapClosedStep S F word c)
    inv := nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
      (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
      (.symm (nativeC60BCMapClosedStep S F word c))
    hom_inv_id := nativeC60AZStrictStep_inv_left _ _ _
    inv_hom_id := nativeC60AZStrictStep_inv_right _ _ _ }

/-- BW's genuine strict functor, now bundled on the entire isotropy group.
The two opposite conventions cancel and give a group homomorphism. -/
def nativeC60COHolonomy (word : List Bool) (a : L.Total) :
    NativeC60COIsotropy S F word a →*
      FreeGroup (NativeC60BVGeneratorCode S) where
  toFun z := MulOpposite.unop
    ((nativeC60BWFreeStrictHolonomy S F).map z.unop.hom)
  map_one' := by
    change MulOpposite.unop ((nativeC60BWFreeStrictHolonomy S F).map
      (𝟙 (nativeC60COObject S F word a))) = 1
    rw [(nativeC60BWFreeStrictHolonomy S F).map_id]
    rfl
  map_mul' x y := by
    change MulOpposite.unop ((nativeC60BWFreeStrictHolonomy S F).map
        (x.unop.hom ≫ y.unop.hom)) =
      MulOpposite.unop ((nativeC60BWFreeStrictHolonomy S F).map x.unop.hom) *
        MulOpposite.unop ((nativeC60BWFreeStrictHolonomy S F).map y.unop.hom)
    rw [(nativeC60BWFreeStrictHolonomy S F).map_comp]
    rfl

/-- Exact agreement with the original raw holonomy under genuine transport. -/
theorem nativeC60CORawLoop_holonomy (word : List Bool) {a : L.Total}
    (c : NativeC60AXStep (nativeC60BCClosedSignature S F) a a) :
    nativeC60COHolonomy S F word a (nativeC60CORawLoop S F word c) =
      nativeC60BWFreePrefix S word (nativeC60BWFreeHolonomy S F c) := by
  change MulOpposite.unop ((nativeC60BWFreeStrictHolonomy S F).map
    (nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
      (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
      (nativeC60BCMapClosedStep S F word c))) = _
  rw [nativeC60BXFreeStrictHolonomy_step, MulOpposite.unop_op,
    nativeC60BWFreeHolonomy_frame]

/-- Faithfulness on actual automorphisms, using CD's all-Hom theorem. -/
theorem nativeC60COHolonomy_injective (word : List Bool) (a : L.Total) :
    Function.Injective (nativeC60COHolonomy S F word a) := by
  intro x y heq
  apply MulOpposite.unop_injective
  apply Aut.ext
  apply nativeC60CDStrictFreeFaithful S F
  exact congrArg MulOpposite.op heq

/-- The free family now lands in ACTUAL strict automorphisms, not merely
in the free-code receiver. Each letter is the original typed mixed fork. -/
def nativeC60COEmbed (word : List Bool) {a b : L.Total}
    (base : (nativeC60BCClosedSignature S F).Gen a b) :
    FreeGroup (NativeC60CNForkAlphabet S F base) →*
      NativeC60COIsotropy S F word a :=
  FreeGroup.lift (fun i => nativeC60CORawLoop S F word
    (nativeC60CKMixedFork S F i.val base))

/-- A commuting diagram of GROUP HOMOMORPHISMS between the actual strict
isotropy construction and CN's independent complete free-code embedding. -/
theorem nativeC60COEmbed_holonomy (word : List Bool) {a b : L.Total}
    (base : (nativeC60BCClosedSignature S F).Gen a b) :
    (nativeC60COHolonomy S F word a).comp
        (nativeC60COEmbed S F word base) =
      (nativeC60BWFreePrefix S word).comp (nativeC60CNEmbed S F base) := by
  apply FreeGroup.ext_hom
  intro i
  change nativeC60COHolonomy S F word a
      (nativeC60COEmbed S F word base (FreeGroup.of i)) =
    nativeC60BWFreePrefix S word (nativeC60CNEmbed S F base (FreeGroup.of i))
  simp only [nativeC60COEmbed, FreeGroup.lift_apply_of]
  rw [nativeC60CORawLoop_holonomy]
  apply congrArg (nativeC60BWFreePrefix S word)
  simp only [nativeC60CNEmbed, FreeGroup.lift_apply_of]
  rfl

theorem nativeC60COEmbed_holonomy_apply (word : List Bool) {a b : L.Total}
    (base : (nativeC60BCClosedSignature S F).Gen a b)
    (x : FreeGroup (NativeC60CNForkAlphabet S F base)) :
    nativeC60COHolonomy S F word a (nativeC60COEmbed S F word base x) =
      nativeC60BWFreePrefix S word (nativeC60CNEmbed S F base x) :=
  DFunLike.congr_fun (nativeC60COEmbed_holonomy S F word base) x

/-- Decode from the WHOLE actual strict isotropy group. Total prefix
removal is only a code operation, never an inverse on original 15D objects. -/
def nativeC60CORetraction (word : List Bool) {a b : L.Total}
    (base : (nativeC60BCClosedSignature S F).Gen a b) :
    NativeC60COIsotropy S F word a →*
      FreeGroup (NativeC60CNForkAlphabet S F base) :=
  (nativeC60CNRetraction S F base).comp
    ((nativeC60BXFreeUnprefix S word).comp (nativeC60COHolonomy S F word a))

theorem nativeC60CORetraction_embed (word : List Bool) {a b : L.Total}
    (base : (nativeC60BCClosedSignature S F).Gen a b)
    (x : FreeGroup (NativeC60CNForkAlphabet S F base)) :
    nativeC60CORetraction S F word base (nativeC60COEmbed S F word base x) =
      x := by
  change nativeC60CNRetraction S F base
    (nativeC60BXFreeUnprefix S word
      (nativeC60COHolonomy S F word a (nativeC60COEmbed S F word base x))) = x
  rw [nativeC60COEmbed_holonomy_apply, nativeC60BXFreeUnprefix_prefix]
  exact nativeC60CNRetraction_left_inverse S F base x

/-- The free family is a RETRACT of actual strict isotropy in every context. -/
theorem nativeC60CORetraction_comp_embed (word : List Bool) {a b : L.Total}
    (base : (nativeC60BCClosedSignature S F).Gen a b) :
    (nativeC60CORetraction S F word base).comp
        (nativeC60COEmbed S F word base) =
      MonoidHom.id (FreeGroup (NativeC60CNForkAlphabet S F base)) := by
  apply MonoidHom.ext
  intro x
  exact nativeC60CORetraction_embed S F word base x

theorem nativeC60COEmbed_injective (word : List Bool) {a b : L.Total}
    (base : (nativeC60BCClosedSignature S F).Gen a b) :
    Function.Injective (nativeC60COEmbed S F word base) :=
  (show Function.LeftInverse (nativeC60CORetraction S F word base)
      (nativeC60COEmbed S F word base) from
    nativeC60CORetraction_embed S F word base).injective

/-- All finite signed words agree with CN's ORIGINAL dependent typed chains.
This rules out a group embedding that merely imitates their observations. -/
theorem nativeC60COEmbed_mk (word : List Bool) {a b : L.Total}
    (base : (nativeC60BCClosedSignature S F).Gen a b)
    (xs : List (NativeC60CNForkAlphabet S F base × Bool)) :
    nativeC60COEmbed S F word base (FreeGroup.mk xs) =
      nativeC60CORawLoop S F word
        (nativeC60CAChainStep S F (nativeC60CNWordChain S F base xs)) := by
  apply nativeC60COHolonomy_injective S F word a
  rw [nativeC60COEmbed_holonomy_apply, nativeC60CORawLoop_holonomy,
    nativeC60CNWordChain_holonomy]

/-- The underlying strict arrow is exactly the already constructed typed word. -/
theorem nativeC60COEmbed_mk_hom (word : List Bool) {a b : L.Total}
    (base : (nativeC60BCClosedSignature S F).Gen a b)
    (xs : List (NativeC60CNForkAlphabet S F base × Bool)) :
    (nativeC60COEmbed S F word base (FreeGroup.mk xs)).unop.hom =
      nativeC60CAChainStrictFrame S F word (nativeC60CNWordChain S F base xs) := by
  rw [nativeC60COEmbed_mk]
  rfl

/-- Ordinary mathlib Aut convention: invert the forward-order loop.
This is a genuine homomorphism into Aut itself, not an antihomomorphism. -/
def nativeC60COAutEmbed (word : List Bool) {a b : L.Total}
    (base : (nativeC60BCClosedSignature S F).Gen a b) :
    FreeGroup (NativeC60CNForkAlphabet S F base) →*
      Aut (nativeC60COObject S F word a) where
  toFun x := (nativeC60COEmbed S F word base x).unop⁻¹
  map_one' := by simp
  map_mul' x y := by simp only [map_mul, MulOpposite.unop_mul, mul_inv_rev]

theorem nativeC60COAutEmbed_injective (word : List Bool) {a b : L.Total}
    (base : (nativeC60BCClosedSignature S F).Gen a b) :
    Function.Injective (nativeC60COAutEmbed S F word base) := by
  intro x y heq
  apply nativeC60COEmbed_injective S F word base
  apply MulOpposite.unop_injective
  change (nativeC60COEmbed S F word base x).unop⁻¹ =
    (nativeC60COEmbed S F word base y).unop⁻¹ at heq
  exact inv_injective heq

/-- Split retraction yields an idempotent endomorphism of the whole isotropy.
Its image is the free fork subgroup; no claim that this image is all isotropy. -/
def nativeC60COProjector (word : List Bool) {a b : L.Total}
    (base : (nativeC60BCClosedSignature S F).Gen a b) :
    NativeC60COIsotropy S F word a →* NativeC60COIsotropy S F word a :=
  (nativeC60COEmbed S F word base).comp (nativeC60CORetraction S F word base)

theorem nativeC60COProjector_idempotent (word : List Bool) {a b : L.Total}
    (base : (nativeC60BCClosedSignature S F).Gen a b) :
    (nativeC60COProjector S F word base).comp
        (nativeC60COProjector S F word base) =
      nativeC60COProjector S F word base := by
  apply MonoidHom.ext
  intro z
  change nativeC60COEmbed S F word base
    (nativeC60CORetraction S F word base
      (nativeC60COEmbed S F word base (nativeC60CORetraction S F word base z))) =
    nativeC60COEmbed S F word base (nativeC60CORetraction S F word base z)
  rw [nativeC60CORetraction_embed]

/-- A proposed further quotient that kills a nonidentity fork word cannot
retain this decoder. The quotient map is input data, not a new axiom. -/
theorem nativeC60COCollapse_no_decoder (word : List Bool) {a b : L.Total}
    (base : (nativeC60BCClosedSignature S F).Gen a b)
    {G : Type v} [Group G]
    (q : NativeC60COIsotropy S F word a →* G)
    (x : FreeGroup (NativeC60CNForkAlphabet S F base)) (hx : x ≠ 1)
    (hcollapse : q (nativeC60COEmbed S F word base x) = 1) :
    ¬ ∃ decoder : G →* FreeGroup (NativeC60CNForkAlphabet S F base),
      decoder.comp q = nativeC60CORetraction S F word base := by
  rintro ⟨decoder, hdecoder⟩
  have heq := DFunLike.congr_fun hdecoder (nativeC60COEmbed S F word base x)
  change decoder (q (nativeC60COEmbed S F word base x)) =
    nativeC60CORetraction S F word base (nativeC60COEmbed S F word base x) at heq
  rw [hcollapse, map_one, nativeC60CORetraction_embed] at heq
  exact hx heq.symm

end Abstract

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

/-- Actual C60 specialization, with independent inner and outer finite AQ
contexts and the original physical conservative atom as base certificate. -/
theorem nativeK5COPhysical_split
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W) (inner outer : List Bool) :
    (nativeC60CORetraction (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
        outer (nativeK5CKAtomGenerator W R inner)).comp
      (nativeC60COEmbed (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
        outer (nativeK5CKAtomGenerator W R inner)) =
      MonoidHom.id (FreeGroup
        (NativeC60CNForkAlphabet (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
          (nativeK5CKAtomGenerator W R inner))) :=
  nativeC60CORetraction_comp_embed (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
    outer (nativeK5CKAtomGenerator W R inner)

end PhysicalC60

#print axioms nativeC60CORawLoop
#print axioms nativeC60COHolonomy
#print axioms nativeC60CORawLoop_holonomy
#print axioms nativeC60COHolonomy_injective
#print axioms nativeC60COEmbed_holonomy
#print axioms nativeC60COEmbed_holonomy_apply
#print axioms nativeC60CORetraction_embed
#print axioms nativeC60CORetraction_comp_embed
#print axioms nativeC60COEmbed_injective
#print axioms nativeC60COEmbed_mk
#print axioms nativeC60COEmbed_mk_hom
#print axioms nativeC60COAutEmbed
#print axioms nativeC60COAutEmbed_injective
#print axioms nativeC60COProjector_idempotent
#print axioms nativeC60COCollapse_no_decoder
#print axioms nativeK5COPhysical_split

end
end Kuu.F112.Physical
