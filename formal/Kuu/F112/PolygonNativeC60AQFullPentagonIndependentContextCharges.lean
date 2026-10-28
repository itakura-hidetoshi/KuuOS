import Kuu.F112.PolygonNativeC60AQFullPentagonInfiniteQuotientObstruction

/-!
# F112-P94D3EA — independently observable finite-AQ context pentagon defects

DZ constructed one infinite-order obstruction in the kernel of the
canonical map from the transported-original to the full-closed 18D
pentagon quotient. EA constructs a COUNTABLE FAMILY of mutually
separated Type-valued context-prefix obstructions without identifying
the original and closed presentations.

For each n : Nat and fixed source AQ word w, choose the genuinely
distinct finite context tag (List.replicate (n+1) false) ++ w.
Read that tag directly from the full context-closed dependent 17D
generator, and lift its complete 18D post-associator coordinate to a
true homomorphism into Multiplicative Int. All original complete 18D
words transported through w vanish under every such character.

Each tag defines an actual new closed 17D atom and an actual long/short
18D pentagon defect. The defect is forced to unity in the full target
pentagon quotient but remains a nonzero class of the image quotient.
The family characters have exact Kronecker evaluation on these
classes, detecting independent context evidence rather than only a
single infinite cyclic obstruction. Natural powers are individually
injective. An actual C60 AU 16D zigzag supplies the typed seed.

The independent characters concern explicit RELATIVE presentations.
No undeclared geometric 19D cell, Gray structure or extra evidence
identification is asserted. Strict Kuu, independent Kuu as a
presentation, original 14D--18D histories, DS no-go, 107 public
roots, append-only and fixed Lean/mathlib are retained.
No new axiom, sorry, admit.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u uD vD uE vE

section IndependentFiniteAQContextCharges

variable {L : NativeC60AXLayer.{u}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- Infinitely many finite distinct AQ context tags, all longer
than the single fixed original transport word. -/
def nativeC60EATag (word : List Bool) (n : ℕ) : List Bool :=
  List.replicate (n + 1) false ++ word

theorem nativeC60EATag_ne_source (word : List Bool) (n : ℕ) :
    nativeC60EATag word n ≠ word := by
  intro h
  have hl := congrArg List.length h
  simp only [nativeC60EATag, List.length_append,
    List.length_replicate] at hl
  omega

theorem nativeC60EATag_injective (word : List Bool) :
    Function.Injective (nativeC60EATag word) := by
  intro m n h
  have hl := congrArg List.length h
  simp only [nativeC60EATag, List.length_append,
    List.length_replicate] at hl
  omega

/-- A generic tag selector on FULL, dependent target 18D letters. -/
def nativeC60EACharge (tag : List Bool)
    (code : NativeC60DVCompleteEighteenCode S F) : Multiplicative ℤ :=
  if nativeC60DYPostAssocPrefix S F code.2.2 = some tag
  then Multiplicative.ofAdd (1 : ℤ) else 1

/-- Independent actual free-group integer character at arbitrary tag. -/
def nativeC60EACharacter (tag : List Bool) :
    NativeC60DVClosedFullFree S F →* Multiplicative ℤ :=
  FreeGroup.lift (nativeC60EACharge S F tag)

theorem nativeC60EACharacter_of (tag : List Bool)
    (code : NativeC60DVCompleteEighteenCode S F) :
    (nativeC60EACharacter S F tag) (FreeGroup.of code) =
      nativeC60EACharge S F tag code := by
  simp only [nativeC60EACharacter, FreeGroup.lift_apply_of]

theorem nativeC60EAClosedPrefix_transport_ne
    (word tag : List Bool) (hne : tag ≠ word)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (p : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b) :
    nativeC60DYClosedAtomPrefix S F
        (nativeC60DVSeventeenWordMap S F word p) ≠ some tag := by
  cases p with
  | atom g =>
      change (some word : Option (List Bool)) ≠ some tag
      intro heq
      exact hne (Option.some.inj heq).symm
  | refl a =>
      change (none : Option (List Bool)) ≠ some tag
      simp
  | symm p =>
      change (none : Option (List Bool)) ≠ some tag
      simp
  | trans p q =>
      change (none : Option (List Bool)) ≠ some tag
      simp

theorem nativeC60EAPostPrefix_transport_ne
    (word tag : List Bool) (hne : tag ≠ word)
    {x y : (nativeC60DREighteenLayer S F).Total}
    (r : (nativeC60DREighteenAssocSignature S F).Gen x y) :
    nativeC60DYPostAssocPrefix S F
      (nativeC60DVTransportEighteenGen S F word r) ≠ some tag := by
  induction r with
  | assoc f g h =>
      change nativeC60DYClosedAtomPrefix S F
        (nativeC60DVSeventeenWordMap S F word f) ≠ some tag
      exact nativeC60EAClosedPrefix_transport_ne S F word tag hne f
  | post r k ih =>
      change nativeC60DYPostAssocPrefix S F
        (nativeC60DVTransportEighteenGen S F word r) ≠ some tag
      exact ih
  | pre h r ih =>
      change (none : Option (List Bool)) ≠ some tag
      simp

theorem nativeC60EACharge_transport_one
    (word tag : List Bool) (hne : tag ≠ word)
    (code : NativeC60DSCompleteEighteenCode S F) :
    nativeC60EACharge S F tag
      (nativeC60DVTransportCompleteCode S F word code) = 1 := by
  rcases code with ⟨x, y, r⟩
  change (if nativeC60DYPostAssocPrefix S F
      (nativeC60DVTransportEighteenGen S F word r) = some tag
    then Multiplicative.ofAdd (1 : ℤ)
    else (1 : Multiplicative ℤ)) = 1
  rw [if_neg (nativeC60EAPostPrefix_transport_ne S F word tag hne r)]

/-- Every genuine original free 18D evidence word maps to the identity
of ANY character carrying a different actual finite AQ tag. -/
theorem nativeC60EACharacter_transport_one
    (word tag : List Bool) (hne : tag ≠ word)
    (x : NativeC60DTFullFree S F) :
    (nativeC60EACharacter S F tag)
      ((nativeC60DVFullWordTransport S F word) x) = 1 := by
  have hcomp :
      (nativeC60EACharacter S F tag).comp
        (nativeC60DVFullWordTransport S F word) =
          (1 : NativeC60DTFullFree S F →* Multiplicative ℤ) := by
    apply FreeGroup.ext_hom
    intro code
    change (nativeC60EACharacter S F tag)
      ((nativeC60DVFullWordTransport S F word) (FreeGroup.of code)) = 1
    rw [nativeC60DVFullWordTransport_of S F word code,
      nativeC60EACharacter_of S F tag _]
    exact nativeC60EACharge_transport_one S F word tag hne code
  simpa using DFunLike.congr_fun hcomp x

theorem nativeC60EAImageKernel_le_character_ker
    (word tag : List Bool) (hne : tag ≠ word) :
    nativeC60DWContextPentagonNormalClosure S F word ≤
      (nativeC60EACharacter S F tag).ker := by
  apply (nativeC60DTNormalClosure_ker_iff
    (nativeC60DWContextPentagonPairs S F word)
    (nativeC60EACharacter S F tag)).mpr
  intro p hp
  rcases hp with ⟨q, hq, rfl⟩
  change (nativeC60EACharacter S F tag)
      ((nativeC60DVFullWordTransport S F word) q.1) =
    (nativeC60EACharacter S F tag)
      ((nativeC60DVFullWordTransport S F word) q.2)
  rw [nativeC60EACharacter_transport_one S F word tag hne,
    nativeC60EACharacter_transport_one S F word tag hne]

/-- Evaluate the true FULL target 18D pentagon defect at any
chosen context tag, without erasing any dependent proof boundary. -/
theorem nativeC60EACharacter_full_pentagon
    (tag : List Bool)
    {a b c d e : (nativeC60DQSeventeenLayer S F).Total}
    (f : NativeC60AXStep (nativeC60DRClosedSeventeenSignature S F) a b)
    (g : NativeC60AXStep (nativeC60DRClosedSeventeenSignature S F) b c)
    (h : NativeC60AXStep (nativeC60DRClosedSeventeenSignature S F) c d)
    (k : NativeC60AXStep (nativeC60DRClosedSeventeenSignature S F) d e) :
    (nativeC60EACharacter S F tag)
      (nativeC60DVClosedFreeWord S F
          (nativeC60DXClosedPentagonLong S F f g h k) *
        (nativeC60DVClosedFreeWord S F
          (nativeC60DXClosedPentagonShort S F f g h k))⁻¹) =
      (if nativeC60DYClosedAtomPrefix S F f = some tag
       then Multiplicative.ofAdd (1 : ℤ) else 1) := by
  change (nativeC60EACharacter S F tag)
      (((FreeGroup.of (⟨_, _, .post (.assoc f g h) k⟩ :
          NativeC60DVCompleteEighteenCode S F) *
        FreeGroup.of (⟨_, _, .assoc f (.trans g h) k⟩ :
          NativeC60DVCompleteEighteenCode S F)) *
        FreeGroup.of (⟨_, _, .pre f (.assoc g h k)⟩ :
          NativeC60DVCompleteEighteenCode S F)) *
        ((FreeGroup.of (⟨_, _, .assoc (.trans f g) h k⟩ :
            NativeC60DVCompleteEighteenCode S F) *
          FreeGroup.of (⟨_, _, .assoc f g (.trans h k)⟩ :
            NativeC60DVCompleteEighteenCode S F))⁻¹)) = _
  simp only [map_mul, map_inv, nativeC60EACharacter_of]
  let q : Multiplicative ℤ :=
    if nativeC60DYClosedAtomPrefix S F f = some tag
    then Multiplicative.ofAdd (1 : ℤ) else 1
  change (q * q * 1) * (1 * q)⁻¹ = q
  group

/-- A closed 17D Type-valued atom at an arbitrary actual AQ tag. -/
def nativeC60EAContextualAtom (tag : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b) :
    NativeC60AXStep (nativeC60DRClosedSeventeenSignature S F)
      (nativeC60BCContextTotal (nativeC60DRSeventeenFrame S F) tag a)
      (nativeC60BCContextTotal (nativeC60DRSeventeenFrame S F) tag b) :=
  .atom (nativeC60BCGen (nativeC60DQTriangleSeventeenSignature S F)
    (nativeC60DRSeventeenFrame S F) tag r)

/-- The entire long/short 18D pentagon defect made from this context
atom and three genuine closed 17D identity proofs. -/
def nativeC60EAContextualDefect (tag : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b) :
    NativeC60DVClosedFullFree S F :=
  let f := nativeC60EAContextualAtom S F tag r
  let id := NativeC60AXStep.refl
    (nativeC60BCContextTotal (nativeC60DRSeventeenFrame S F) tag b)
  nativeC60DVClosedFreeWord S F
    (nativeC60DXClosedPentagonLong S F f id id id) *
  (nativeC60DVClosedFreeWord S F
    (nativeC60DXClosedPentagonShort S F f id id id))⁻¹

theorem nativeC60EAContextualDefect_mem_full
    (tag : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b) :
    nativeC60EAContextualDefect S F tag r ∈
      nativeC60DXFullClosedPentagonNormalClosure S F := by
  unfold nativeC60EAContextualDefect
  exact nativeC60DXFullClosedPentagon_defect_mem S F _ _ _ _

/-- A true Kronecker test on any two original finite context tags. -/
theorem nativeC60EACharacter_contextual_defect
    (tag detect : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b) :
    (nativeC60EACharacter S F detect)
        (nativeC60EAContextualDefect S F tag r) =
      (if tag = detect then Multiplicative.ofAdd (1 : ℤ) else 1) := by
  unfold nativeC60EAContextualDefect
  rw [nativeC60EACharacter_full_pentagon S F detect]
  simp [nativeC60EAContextualAtom, nativeC60DYClosedAtomPrefix,
    nativeC60BCGen]

/-- A distinct tag yields a truly descended integer character on
the quotient by every transported original pentagon. -/
def nativeC60EAImageCharacter (word : List Bool)
    (n : ℕ) :
    NativeC60DWContextPentagonQuotient S F word →* Multiplicative ℤ :=
  QuotientGroup.lift
    (nativeC60DWContextPentagonNormalClosure S F word)
    (nativeC60EACharacter S F (nativeC60EATag word n))
    (nativeC60EAImageKernel_le_character_ker S F word
      (nativeC60EATag word n) (nativeC60EATag_ne_source word n))

theorem nativeC60EAImageCharacter_mk (word : List Bool) (n : ℕ)
    (x : NativeC60DVClosedFullFree S F) :
    (nativeC60EAImageCharacter S F word n)
      ((QuotientGroup.mk'
        (nativeC60DWContextPentagonNormalClosure S F word)) x) =
    (nativeC60EACharacter S F (nativeC60EATag word n)) x :=
  rfl

/-- Every independent context defect is a genuine image-quotient class,
with the same complete 18D Type-valued source/target histories. -/
def nativeC60EAOutsideClass (word : List Bool) (n : ℕ)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b) :
    NativeC60DWContextPentagonQuotient S F word :=
  (QuotientGroup.mk' (nativeC60DWContextPentagonNormalClosure S F word))
    (nativeC60EAContextualDefect S F (nativeC60EATag word n) r)

theorem nativeC60EAOutsideClass_mem_kernel
    (word : List Bool) (n : ℕ)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b) :
    nativeC60EAOutsideClass S F word n r ∈
      (nativeC60DZImageToFull S F word).ker := by
  apply MonoidHom.mem_ker.mpr
  rw [nativeC60EAOutsideClass, nativeC60DZImageToFull_mk S F word]
  exact (QuotientGroup.eq_one_iff _).mpr
    (nativeC60EAContextualDefect_mem_full S F (nativeC60EATag word n) r)

/-- EXACT independently observed charges: character i evaluates
the genuine contextual pentagon defect j to one iff i=j. -/
theorem nativeC60EACharacter_orthogonal
    (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (i j : ℕ) :
    (nativeC60EAImageCharacter S F word i)
      (nativeC60EAOutsideClass S F word j r) =
      (if i = j then Multiplicative.ofAdd (1 : ℤ) else 1) := by
  change (nativeC60EACharacter S F (nativeC60EATag word i))
      (nativeC60EAContextualDefect S F (nativeC60EATag word j) r) =
        (if i = j then Multiplicative.ofAdd (1 : ℤ) else 1)
  rw [nativeC60EACharacter_contextual_defect S F]
  by_cases h : i = j
  · subst j
    simp
  · have ht : nativeC60EATag word j ≠ nativeC60EATag word i := by
      intro htags
      exact h ((nativeC60EATag_injective word htags).symm)
    simp [h, ht]

theorem nativeC60EAOutsideClass_ne_one
    (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (i : ℕ) :
    nativeC60EAOutsideClass S F word i r ≠ 1 := by
  intro hh
  have h := congrArg (nativeC60EAImageCharacter S F word i) hh
  rw [nativeC60EACharacter_orthogonal S F word r i i, if_pos rfl,
    map_one] at h
  have hnonzero := congrArg Multiplicative.toAdd h
  norm_num at hnonzero

/-- ACTUAL distinct AQ context tags yield pairwise distinct nontrivial
members of the same canonical quotient kernel, not just duplicate
observations of the original single DZ witness. -/
theorem nativeC60EAOutsideClass_injective (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b) :
    Function.Injective (fun n : ℕ => nativeC60EAOutsideClass S F word n r) := by
  intro i j heq
  by_contra hne
  have h := congrArg (nativeC60EAImageCharacter S F word i) heq
  rw [nativeC60EACharacter_orthogonal S F word r i i,
    nativeC60EACharacter_orthogonal S F word r i j] at h
  have hn : (1 : ℕ) ≠ 0 := by omega
  simp [hne] at h
  have hs := congrArg Multiplicative.toAdd h
  norm_num at hs

/-- Each of the distinct contextual classes also generates a truly
infinite sequence of different natural powers, by its OWN character. -/
theorem nativeC60EAOutsideClass_powers_injective (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (i : ℕ) :
    Function.Injective (fun n : ℕ =>
      (nativeC60EAOutsideClass S F word i r) ^ n) := by
  intro m n h
  have hh := congrArg (nativeC60EAImageCharacter S F word i) h
  rw [map_pow, map_pow,
    nativeC60EACharacter_orthogonal S F word r i i] at hh
  simp only [if_pos rfl] at hh
  have ha := congrArg Multiplicative.toAdd hh
  rw [nativeC60DZIntegerGeneratorPower m,
    nativeC60DZIntegerGeneratorPower n] at ha
  exact_mod_cast ha

end IndependentFiniteAQContextCharges

section PhysicalC60AU

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

/-- True physical C60 AU provides infinitely many separately
integer-detected independent contextual pentagon obstruction classes
in the kernel of the same image-to-full quotient comparison. -/
theorem nativeK5EAPhysicalAQ_obstruction_family_injective
    (W : NativeK5StructuralThirteenCell p U V)
    (tree : NativeK5DOContextTree) :
    let S := nativeK5AXKuuSignature W
    let F := nativeK5BCFrame W
    Function.Injective (fun n : ℕ =>
      nativeC60EAOutsideClass S F (nativeK5DOTreeWord tree) n
        (nativeC60DYOriginalZigzagGen S F
          (nativeK5CEPhysicalAUGenerator W))) := by
  dsimp only
  exact nativeC60EAOutsideClass_injective
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
    (nativeK5DOTreeWord tree)
    (nativeC60DYOriginalZigzagGen
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
      (nativeK5CEPhysicalAUGenerator W))

end PhysicalC60AU

#print axioms nativeC60EATag
#print axioms nativeC60EATag_ne_source
#print axioms nativeC60EATag_injective
#print axioms nativeC60EACharge
#print axioms nativeC60EACharacter
#print axioms nativeC60EAClosedPrefix_transport_ne
#print axioms nativeC60EAPostPrefix_transport_ne
#print axioms nativeC60EACharacter_transport_one
#print axioms nativeC60EAImageKernel_le_character_ker
#print axioms nativeC60EACharacter_full_pentagon
#print axioms nativeC60EAContextualDefect_mem_full
#print axioms nativeC60EACharacter_contextual_defect
#print axioms nativeC60EAImageCharacter
#print axioms nativeC60EAOutsideClass
#print axioms nativeC60EAOutsideClass_mem_kernel
#print axioms nativeC60EACharacter_orthogonal
#print axioms nativeC60EAOutsideClass_ne_one
#print axioms nativeC60EAOutsideClass_injective
#print axioms nativeC60EAOutsideClass_powers_injective
#print axioms nativeK5EAPhysicalAQ_obstruction_family_injective

end
end Kuu.F112.Physical
