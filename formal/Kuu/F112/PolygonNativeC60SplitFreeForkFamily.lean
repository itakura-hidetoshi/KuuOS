import Kuu.F112.PolygonNativeC60ForkFreeSubgroup

/-!
# F112-P94D3CN — split free families of genuine dependent C60 fork loops

CM proves infinite order and faithful finite powers for one physical fork.
Integer exponent characters cannot detect arbitrary noncommutative words.
CN instead constructs a FREE-GROUP-VALUED LEFT INVERSE.

Fix a genuine BC primitive h:a->b. The alphabet consists of ALL actual
parallel BC certificates g != h. Send its letter g to code(g)*code(h)^-1.
A decoder sends code(g) back to that letter and code(h) to identity.
The resulting homomorphisms compose to identity, proving a split embedding
of the free group on the original parallel-generator alphabet.

Every FINITE signed word is separately realized in CA's original dependent
16D chain syntax, retaining the exact 15D objects a and b. A negative fork
letter is h followed by g inverse, not an ill-typed inverse edge out of a.
The whole typed chain has exactly the embedded free holonomy. Consequently
strict equality after ANY finite genuine AQ context is equivalent to
free-word equality on this alphabet. This is not merely abelianization.

A third physical conservative 15D certificate, symm(refl R), is distinct
from CK's refl R and atom rfl rfl but has the same AU naturality endpoints.
It supplies two distinct alphabet letters relative to the atom certificate.
Their two possible product orders remain unequal in every strict context.

Only the selected BC presentation is used. No assertion identifies this
free family with the ENTIRE isotropy group or with original geometric
16D coherence. No Gray, global horizontal Peiffer, P92B, strict-n or
hyperdescent is inferred. No new axioms, sorry/admit or public roots.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u uD vD uE vE

/-- Every letter is a genuine parallel BC certificate, excluding only
one fixed base certificate. Both original dependent 15D endpoints remain. -/
abbrev NativeC60CNForkAlphabet {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {a b : L.Total} (base : (nativeC60BCClosedSignature S F).Gen a b) :=
  {g : (nativeC60BCClosedSignature S F).Gen a b // g ≠ base}

/-- Full original provenance, not a scalar or a quotient of endpoints. -/
def nativeC60CNLetterCode {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {a b : L.Total} (base : (nativeC60BCClosedSignature S F).Gen a b)
    (i : NativeC60CNForkAlphabet S F base) : NativeC60BVGeneratorCode S :=
  nativeC60BVGeneratorCode S F i.val

theorem nativeC60CNLetterCode_injective {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {a b : L.Total} (base : (nativeC60BCClosedSignature S F).Gen a b) :
    Function.Injective (nativeC60CNLetterCode S F base) := by
  intro i j heq
  apply Subtype.ext
  exact nativeC60BVGeneratorCode_injective S F heq

theorem nativeC60CNLetterCode_ne_base {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {a b : L.Total} (base : (nativeC60BCClosedSignature S F).Gen a b)
    (i : NativeC60CNForkAlphabet S F base) :
    nativeC60CNLetterCode S F base i ≠ nativeC60BVGeneratorCode S F base := by
  intro heq
  exact i.property (nativeC60BVGeneratorCode_injective S F heq)

/-- Nonabelian decoding of the FULL original code alphabet. Classical
choice selects a unique letter only when such a genuine certificate exists. -/
def nativeC60CNDecodeLetter {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {a b : L.Total} (base : (nativeC60BCClosedSignature S F).Gen a b)
    (code : NativeC60BVGeneratorCode S) :
    FreeGroup (NativeC60CNForkAlphabet S F base) := by
  classical
  exact if hc : ∃ i : NativeC60CNForkAlphabet S F base,
      nativeC60CNLetterCode S F base i = code
    then FreeGroup.of (Classical.choose hc) else 1

theorem nativeC60CNDecodeLetter_letter {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {a b : L.Total} (base : (nativeC60BCClosedSignature S F).Gen a b)
    (i : NativeC60CNForkAlphabet S F base) :
    nativeC60CNDecodeLetter S F base (nativeC60CNLetterCode S F base i) =
      FreeGroup.of i := by
  classical
  have hi : ∃ j : NativeC60CNForkAlphabet S F base,
      nativeC60CNLetterCode S F base j = nativeC60CNLetterCode S F base i :=
    ⟨i, rfl⟩
  unfold nativeC60CNDecodeLetter
  rw [dif_pos hi]
  exact congrArg FreeGroup.of
    (nativeC60CNLetterCode_injective S F base (Classical.choose_spec hi))

theorem nativeC60CNDecodeLetter_base {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {a b : L.Total} (base : (nativeC60BCClosedSignature S F).Gen a b) :
    nativeC60CNDecodeLetter S F base (nativeC60BVGeneratorCode S F base) = 1 := by
  classical
  have hn : ¬ ∃ i : NativeC60CNForkAlphabet S F base,
      nativeC60CNLetterCode S F base i = nativeC60BVGeneratorCode S F base := by
    rintro ⟨i, hi⟩
    exact nativeC60CNLetterCode_ne_base S F base i hi
  simp only [nativeC60CNDecodeLetter, dif_neg hn]

/-- The free family of mixed forks, still recording full BC provenance. -/
def nativeC60CNEmbed {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {a b : L.Total} (base : (nativeC60BCClosedSignature S F).Gen a b) :
    FreeGroup (NativeC60CNForkAlphabet S F base) →*
      FreeGroup (NativeC60BVGeneratorCode S) :=
  FreeGroup.lift (fun i => FreeGroup.of (nativeC60CNLetterCode S F base i) *
    (FreeGroup.of (nativeC60BVGeneratorCode S F base))⁻¹)

/-- A genuine group retraction, not an integer exponent character. -/
def nativeC60CNRetraction {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {a b : L.Total} (base : (nativeC60BCClosedSignature S F).Gen a b) :
    FreeGroup (NativeC60BVGeneratorCode S) →*
      FreeGroup (NativeC60CNForkAlphabet S F base) :=
  FreeGroup.lift (nativeC60CNDecodeLetter S F base)

/-- The free-fork homomorphism is SPLIT: every noncommutative word is
recovered, including commutators invisible to the earlier integer character. -/
theorem nativeC60CNRetraction_comp_embed {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {a b : L.Total} (base : (nativeC60BCClosedSignature S F).Gen a b) :
    (nativeC60CNRetraction S F base).comp (nativeC60CNEmbed S F base) =
      MonoidHom.id (FreeGroup (NativeC60CNForkAlphabet S F base)) := by
  apply FreeGroup.ext_hom
  intro i
  change nativeC60CNRetraction S F base
      (nativeC60CNEmbed S F base (FreeGroup.of i)) = FreeGroup.of i
  simp only [nativeC60CNEmbed, FreeGroup.lift_apply_of, map_mul, map_inv]
  -- Evaluating a lifted homomorphism on `of` uses its theorem, not defeq.
  simp only [nativeC60CNRetraction, FreeGroup.lift_apply_of]
  rw [nativeC60CNDecodeLetter_letter, nativeC60CNDecodeLetter_base]
  simp

theorem nativeC60CNRetraction_left_inverse {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {a b : L.Total} (base : (nativeC60BCClosedSignature S F).Gen a b) :
    Function.LeftInverse (nativeC60CNRetraction S F base)
      (nativeC60CNEmbed S F base) := by
  intro x
  exact DFunLike.congr_fun (nativeC60CNRetraction_comp_embed S F base) x

theorem nativeC60CNEmbed_injective {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {a b : L.Total} (base : (nativeC60BCClosedSignature S F).Gen a b) :
    Function.Injective (nativeC60CNEmbed S F base) :=
  (nativeC60CNRetraction_left_inverse S F base).injective

/-- Every finite AQ prefix still preserves the entire free family. -/
theorem nativeC60CNFramed_embed_injective {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (word : List Bool) {a b : L.Total}
    (base : (nativeC60BCClosedSignature S F).Gen a b) :
    Function.Injective (fun x =>
      nativeC60BWFreePrefix S word (nativeC60CNEmbed S F base x)) :=
  (nativeC60BWFreePrefix_injective S word).comp
    (nativeC60CNEmbed_injective S F base)

/-- Interpret arbitrary signed words in the ORIGINAL CA typed chains.
The negative letter uses base ; i inverse, preserving a->b->a typing. -/
def nativeC60CNWordChain {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {a b : L.Total} (base : (nativeC60BCClosedSignature S F).Gen a b) :
    List (NativeC60CNForkAlphabet S F base × Bool) →
      NativeC60CASignedChain S F a a
  | [] => .nil a
  | (i, true) :: rest => .pos i.val (.neg base (nativeC60CNWordChain S F base rest))
  | (i, false) :: rest => .pos base (.neg i.val (nativeC60CNWordChain S F base rest))

/-- Holonomy is the split embedding of the full original signed word.
No 15D skeleton is replaced by a graph or by a scalar observation. -/
theorem nativeC60CNWordChain_holonomy {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {a b : L.Total} (base : (nativeC60BCClosedSignature S F).Gen a b)
    (xs : List (NativeC60CNForkAlphabet S F base × Bool)) :
    nativeC60BWFreeHolonomy S F
        (nativeC60CAChainStep S F (nativeC60CNWordChain S F base xs)) =
      nativeC60CNEmbed S F base (FreeGroup.mk xs) := by
  induction xs with
  | nil =>
      change 1 = (nativeC60CNEmbed S F base) 1
      exact (map_one _).symm
  | cons entry rest ih =>
      rcases entry with ⟨i, sign⟩
      cases sign with
      | true =>
          change FreeGroup.of (nativeC60CNLetterCode S F base i) *
              ((FreeGroup.of (nativeC60BVGeneratorCode S F base))⁻¹ *
                nativeC60BWFreeHolonomy S F
                  (nativeC60CAChainStep S F (nativeC60CNWordChain S F base rest))) =
            nativeC60CNEmbed S F base (FreeGroup.of i * FreeGroup.mk rest)
          rw [ih, map_mul]
          simp only [nativeC60CNEmbed, FreeGroup.lift_apply_of, mul_assoc]
      | false =>
          change FreeGroup.of (nativeC60BVGeneratorCode S F base) *
              ((FreeGroup.of (nativeC60CNLetterCode S F base i))⁻¹ *
                nativeC60BWFreeHolonomy S F
                  (nativeC60CAChainStep S F (nativeC60CNWordChain S F base rest))) =
            nativeC60CNEmbed S F base ((FreeGroup.of i)⁻¹ * FreeGroup.mk rest)
          rw [ih, map_mul, map_inv]
          simp only [nativeC60CNEmbed, FreeGroup.lift_apply_of,
            mul_inv_rev, inv_inv, mul_assoc]

/-- Exact classification of all finite fork-family words in every
selected strict Hom, with the actual original dependent chains retained. -/
theorem nativeC60CNWordChain_strict_iff {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (word : List Bool) {a b : L.Total}
    (base : (nativeC60BCClosedSignature S F).Gen a b)
    (xs ys : List (NativeC60CNForkAlphabet S F base × Bool)) :
    nativeC60CAChainStrictFrame S F word (nativeC60CNWordChain S F base xs) =
      nativeC60CAChainStrictFrame S F word (nativeC60CNWordChain S F base ys) ↔
        FreeGroup.mk xs = FreeGroup.mk ys := by
  constructor
  · intro hstrict
    have hh := (nativeC60CDAll_raw_free_eq_iff_strict S F word
      (nativeC60CAChainStep S F (nativeC60CNWordChain S F base xs))
      (nativeC60CAChainStep S F (nativeC60CNWordChain S F base ys))).mpr hstrict
    rw [nativeC60CNWordChain_holonomy, nativeC60CNWordChain_holonomy] at hh
    exact nativeC60CNEmbed_injective S F base hh
  · intro hfree
    apply (nativeC60CDAll_raw_free_eq_iff_strict S F word
      (nativeC60CAChainStep S F (nativeC60CNWordChain S F base xs))
      (nativeC60CAChainStep S F (nativeC60CNWordChain S F base ys))).mp
    rw [nativeC60CNWordChain_holonomy, nativeC60CNWordChain_holonomy, hfree]

/-- Distinct fork letters cannot commute in any finite strict AQ context.
The proof uses full reduced words, not an abelian exponent character. -/
theorem nativeC60CNWordChain_swapped_ne {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (word : List Bool) {a b : L.Total}
    (base : (nativeC60BCClosedSignature S F).Gen a b)
    (i j : NativeC60CNForkAlphabet S F base) (hne : i ≠ j) :
    nativeC60CAChainStrictFrame S F word
        (nativeC60CNWordChain S F base [(i, true), (j, true)]) ≠
      nativeC60CAChainStrictFrame S F word
        (nativeC60CNWordChain S F base [(j, true), (i, true)]) := by
  intro hstrict
  have hfree := (nativeC60CNWordChain_strict_iff S F word base _ _).mp hstrict
  have hred : ∀ x y : NativeC60CNForkAlphabet S F base,
      FreeGroup.IsReduced [(x, true), (y, true)] := by
    intro x y
    rw [FreeGroup.isReduced_cons_cons]
    exact ⟨fun _ => rfl, FreeGroup.IsReduced.singleton⟩
  obtain ⟨zs, hx, hy⟩ := FreeGroup.Red.exact.mp hfree
  have hwords : [(i, true), (j, true)] = [(j, true), (i, true)] :=
    ((FreeGroup.IsReduced.red_iff_eq (hred i j)).mp hx).symm.trans
      ((FreeGroup.IsReduced.red_iff_eq (hred j i)).mp hy)
  exact hne (congrArg Prod.fst (List.cons.inj hwords).1)

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

/-- A raw syntax discriminator on the ORIGINAL conservative input.
This is used only to separate actual certificates, never to quotient them. -/
def nativeK5CNInputReversedCore
    (W : NativeK5StructuralThirteenCell p U V)
    {R S : NativeK5FifteenFourteenFiber W} : NativeK5AQFifteenCell W R S → Bool
  | .conservative (.symm _) => true
  | _ => false

/-- Read the original input inside a COMPLETE BC provenance code.
The uniform Bool codomain avoids eliminating across dependent AU endpoints. -/
def nativeK5CNCodeReversedCore
    (W : NativeK5StructuralThirteenCell p U V)
    (code : NativeC60BVGeneratorCode (nativeK5AXKuuSignature W)) : Bool :=
  nativeK5CNInputReversedCore W code.2.2.2.2.2.val

/-- A THIRD genuine conservative 15D certificate on the same original
14D boundary. The inverse-of-reflexivity core is retained as Type syntax. -/
def nativeK5CNConservativeReverseRefl
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W) : NativeK5AQFifteenCell W R R :=
  .conservative (.symm (.refl R))

/-- Actual AU transport has the same endpoints as CK's refl certificate,
while the declared BC primitive retains the different original input. -/
def nativeK5CNReverseGenerator
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W) (word : List Bool) :
    (nativeK5BCSignature W).Gen
      (nativeK5CHSource W word (nativeK5CKConservativeRefl W R))
      (nativeK5CHTarget W word (nativeK5CKConservativeRefl W R)) :=
  nativeK5CHPositiveGenerator W word (nativeK5CNConservativeReverseRefl W R)

theorem nativeK5CNReverse_ne_atom
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W) (word : List Bool) :
    nativeK5CNReverseGenerator W R word ≠ nativeK5CKAtomGenerator W R word := by
  intro heq
  have hc := congrArg (nativeC60BVGeneratorCode
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W)) heq
  have htag := congrArg (nativeK5CNCodeReversedCore W) hc
  change true = false at htag
  cases htag

theorem nativeK5CNReverse_ne_refl
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W) (word : List Bool) :
    nativeK5CNReverseGenerator W R word ≠ nativeK5CKReflGenerator W R word := by
  intro heq
  have hc := congrArg (nativeC60BVGeneratorCode
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W)) heq
  have htag := congrArg (nativeK5CNCodeReversedCore W) hc
  change true = false at htag
  cases htag

/-- First physical letter relative to the original atom base certificate. -/
def nativeK5CNReflLetter
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W) (word : List Bool) :
    NativeC60CNForkAlphabet (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
      (nativeK5CKAtomGenerator W R word) :=
  ⟨nativeK5CKReflGenerator W R word,
    nativeK5CKPhysical_parallel_generators_ne W R word⟩

/-- Second independent physical letter at exactly the same typed boundary. -/
def nativeK5CNReverseLetter
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W) (word : List Bool) :
    NativeC60CNForkAlphabet (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
      (nativeK5CKAtomGenerator W R word) :=
  ⟨nativeK5CNReverseGenerator W R word, nativeK5CNReverse_ne_atom W R word⟩

theorem nativeK5CNPhysical_letters_ne
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W) (word : List Bool) :
    nativeK5CNReflLetter W R word ≠ nativeK5CNReverseLetter W R word := by
  intro heq
  have hv : nativeK5CKReflGenerator W R word =
      nativeK5CNReverseGenerator W R word := congrArg Subtype.val heq
  exact nativeK5CNReverse_ne_refl W R word hv.symm

/-- Genuine noncommutativity, not merely infinite order: the two products
of actual C60 fork loops differ at every independent outer AQ context. -/
theorem nativeK5CNPhysical_forks_noncommute
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W) (inner outer : List Bool) :
    nativeC60CAChainStrictFrame
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W) outer
        (nativeC60CNWordChain (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
          (nativeK5CKAtomGenerator W R inner)
          [(nativeK5CNReflLetter W R inner, true),
           (nativeK5CNReverseLetter W R inner, true)]) ≠
      nativeC60CAChainStrictFrame
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W) outer
        (nativeC60CNWordChain (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
          (nativeK5CKAtomGenerator W R inner)
          [(nativeK5CNReverseLetter W R inner, true),
           (nativeK5CNReflLetter W R inner, true)]) :=
  nativeC60CNWordChain_swapped_ne
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W) outer
    (nativeK5CKAtomGenerator W R inner)
    (nativeK5CNReflLetter W R inner) (nativeK5CNReverseLetter W R inner)
    (nativeK5CNPhysical_letters_ne W R inner)

end PhysicalC60

#print axioms nativeC60CNLetterCode_injective
#print axioms nativeC60CNDecodeLetter_letter
#print axioms nativeC60CNDecodeLetter_base
#print axioms nativeC60CNRetraction_comp_embed
#print axioms nativeC60CNRetraction_left_inverse
#print axioms nativeC60CNEmbed_injective
#print axioms nativeC60CNFramed_embed_injective
#print axioms nativeC60CNWordChain_holonomy
#print axioms nativeC60CNWordChain_strict_iff
#print axioms nativeC60CNWordChain_swapped_ne
#print axioms nativeK5CNReverse_ne_atom
#print axioms nativeK5CNReverse_ne_refl
#print axioms nativeK5CNPhysical_letters_ne
#print axioms nativeK5CNPhysical_forks_noncommute

end
end Kuu.F112.Physical
