import Kuu.F112.PolygonNativeC60AQFullPentagonKernelComparison

/-!
# F112-P94D3DY — strict closed-AQ pentagon kernel separation

DX proved the inclusion of image-pentagon normal closure into the
independently constructed full context-closed pentagon normal closure.

DY proves the inclusion is PROPER, whenever the original genuinely
dependent triangle grammar has a primitive (which physical C60 AU does).

The proof does not guess a 19D filler or throw away dependent evidence:
* Read the finite-AQ context word actually STORED in a closed 17D atom.
* Detect a specific "post of associator" 18D code with FIRST argument
  being an atom carrying context tag (false :: word).
* Show every transported ORIGINAL 18D primitive has detector charge zero:
  its 17D atom carries tag word, and all other 18D constructors give zero.
* Lift this coordinate to an actual homomorphism from the full target
  18D FreeGroup into the multiplicative integers.
* Its kernel contains the entire normally closed IMAGE pentagon family.
* An actual, fully dependent closed pentagon made from the freshly tagged
  triangle atom and three identity 17D paths has charge 1. Its defect
  therefore lies in the FULL pentagon normal closure but NOT the image
  normal closure, even if all lower geometric objects happen to coincide.
* Specialize to the physical C60 AU zigzag primitive at every genuine
  finite chronological AQ context tree.

This strictly compares algebraic relative presentations. No original
geometric Type-valued 19D filling is asserted. DS no-go, strict Kuu,
independent Kuu as a presentation, original 14D–18D histories,
107 public roots and no-Gray are preserved. No new axioms, sorry or admit.
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

section ContextPrefixCharacter

variable {L : NativeC60AXLayer.{u}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- Read the genuine finite AQ word in an atomic CLOSED 17D step.
Composite, inverse and identity syntaxes carry no single atom tag. -/
def nativeC60DYClosedAtomPrefix :
    ∀ {a b : (nativeC60DQSeventeenLayer S F).Total},
      NativeC60AXStep (nativeC60DRClosedSeventeenSignature S F) a b →
        Option (List Bool)
  | _, _, .atom g => some g.1
  | _, _, .refl _ => none
  | _, _, .symm _ => none
  | _, _, .trans _ _ => none

/-- Read the first 17D atom tag of an 18D associator, through any
finite chain of right-post-whiskerings. The left-pre constructor has
zero charge. Structural recursion avoids a fragile nested match. -/
def nativeC60DYPostAssocPrefix :
    ∀ {x y : (nativeC60DVClosedEighteenLayer S F).Total},
      (nativeC60DVClosedEighteenSignature S F).Gen x y →
        Option (List Bool)
  | _, _, .assoc f _ _ => nativeC60DYClosedAtomPrefix S F f
  | _, _, .post r _ => nativeC60DYPostAssocPrefix S F r
  | _, _, .pre _ _ => none

/-- A mapped original raw17D path cannot be an atomic closed path
with a tag longer than its entire transported AQ context word. -/
theorem nativeC60DYClosedAtomPrefix_transport_ne
    (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (p : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b) :
    nativeC60DYClosedAtomPrefix S F
        (nativeC60DVSeventeenWordMap S F word p) ≠
      some (false :: word) := by
  cases p with
  | atom g =>
      change (some word : Option (List Bool)) ≠ some (false :: word)
      intro h
      have hw : word = false :: word := Option.some.inj h
      have hn := congrArg List.length hw
      simp at hn
  | refl x =>
      change (none : Option (List Bool)) ≠ some (false :: word)
      simp
  | symm p =>
      change (none : Option (List Bool)) ≠ some (false :: word)
      simp
  | trans p q =>
      change (none : Option (List Bool)) ≠ some (false :: word)
      simp

/-- Every actual source 18D generator is disjoint from the selected
extra-context post-associator coordinate, with full dependent boundaries. -/
theorem nativeC60DYPostAssocPrefix_transport_ne
    (word : List Bool)
    {x y : (nativeC60DREighteenLayer S F).Total}
    (r : (nativeC60DREighteenAssocSignature S F).Gen x y) :
    nativeC60DYPostAssocPrefix S F
        (nativeC60DVTransportEighteenGen S F word r) ≠
      some (false :: word) := by
  induction r with
  | assoc f g h =>
      change nativeC60DYClosedAtomPrefix S F
        (nativeC60DVSeventeenWordMap S F word f) ≠ some (false :: word)
      exact nativeC60DYClosedAtomPrefix_transport_ne S F word f
  | post r k ih =>
      change nativeC60DYPostAssocPrefix S F
          (nativeC60DVTransportEighteenGen S F word r) ≠
            some (false :: word)
      exact ih
  | pre h r ih =>
      change (none : Option (List Bool)) ≠ some (false :: word)
      simp

/-- A selected full 18D letter carries integer charge one exactly
when its genuine proof code has the extra context prefix. -/
def nativeC60DYCodeCharge (word : List Bool)
    (code : NativeC60DVCompleteEighteenCode S F) : Multiplicative ℤ :=
  if nativeC60DYPostAssocPrefix S F code.2.2 = some (false :: word)
  then Multiplicative.ofAdd (1 : ℤ) else 1

/-- Universal character of the ENTIRE full closed 18D evidence group.
This is a real homomorphism, not an informal count or parity observer. -/
def nativeC60DYCharacter (word : List Bool) :
    NativeC60DVClosedFullFree S F →* Multiplicative ℤ :=
  FreeGroup.lift (nativeC60DYCodeCharge S F word)

theorem nativeC60DYCharacter_of (word : List Bool)
    (code : NativeC60DVCompleteEighteenCode S F) :
    (nativeC60DYCharacter S F word) (FreeGroup.of code) =
      nativeC60DYCodeCharge S F word code := by
  simp only [nativeC60DYCharacter, FreeGroup.lift_apply_of]

theorem nativeC60DYCodeCharge_transport_one
    (word : List Bool) (code : NativeC60DSCompleteEighteenCode S F) :
    nativeC60DYCodeCharge S F word
      (nativeC60DVTransportCompleteCode S F word code) = 1 := by
  rcases code with ⟨x, y, r⟩
  change (if nativeC60DYPostAssocPrefix S F
      (nativeC60DVTransportEighteenGen S F word r) =
        some (false :: word)
      then Multiplicative.ofAdd (1 : ℤ)
      else (1 : Multiplicative ℤ)) = 1
  rw [if_neg (nativeC60DYPostAssocPrefix_transport_ne S F word r)]

/-- Every ORIGINAL complete 18D word, including arbitrary inverse
and noncommutative composites, maps to zero integer charge. -/
theorem nativeC60DYCharacter_transport_one
    (word : List Bool) (x : NativeC60DTFullFree S F) :
    (nativeC60DYCharacter S F word)
      ((nativeC60DVFullWordTransport S F word) x) = 1 := by
  have hcomp :
      (nativeC60DYCharacter S F word).comp
          (nativeC60DVFullWordTransport S F word) =
        (1 : NativeC60DTFullFree S F →* Multiplicative ℤ) := by
    apply FreeGroup.ext_hom
    intro code
    change (nativeC60DYCharacter S F word)
      ((nativeC60DVFullWordTransport S F word) (FreeGroup.of code)) = 1
    rw [nativeC60DVFullWordTransport_of S F word code,
      nativeC60DYCharacter_of S F word _]
    exact nativeC60DYCodeCharge_transport_one S F word code
  simpa using DFunLike.congr_fun hcomp x

/-- Stronger than normal-closure inclusion: the FULL image-pentagon
kernel lies in the exact kernel of a real, nontrivial integer character. -/
theorem nativeC60DYImageKernel_le_character_ker (word : List Bool) :
    nativeC60DWContextPentagonNormalClosure S F word ≤
      (nativeC60DYCharacter S F word).ker := by
  apply (nativeC60DTNormalClosure_ker_iff
    (nativeC60DWContextPentagonPairs S F word)
    (nativeC60DYCharacter S F word)).mpr
  intro p hp
  rcases hp with ⟨q, hq, rfl⟩
  change (nativeC60DYCharacter S F word)
      ((nativeC60DVFullWordTransport S F word) q.1) =
    (nativeC60DYCharacter S F word)
      ((nativeC60DVFullWordTransport S F word) q.2)
  rw [nativeC60DYCharacter_transport_one S F word,
    nativeC60DYCharacter_transport_one S F word]

/-- Exact charge of ANY full-closed pentagon defect. The two
long-route associator-spine charges are balanced by the last short
associator; the first short associator and pre-whisker charge zero.
Their uncancelled signed difference is the first path's tag. -/
theorem nativeC60DYCharacter_full_pentagon
    (word : List Bool)
    {a b c d e : (nativeC60DQSeventeenLayer S F).Total}
    (f : NativeC60AXStep (nativeC60DRClosedSeventeenSignature S F) a b)
    (g : NativeC60AXStep (nativeC60DRClosedSeventeenSignature S F) b c)
    (h : NativeC60AXStep (nativeC60DRClosedSeventeenSignature S F) c d)
    (k : NativeC60AXStep (nativeC60DRClosedSeventeenSignature S F) d e) :
    (nativeC60DYCharacter S F word)
      (nativeC60DVClosedFreeWord S F
          (nativeC60DXClosedPentagonLong S F f g h k) *
        (nativeC60DVClosedFreeWord S F
          (nativeC60DXClosedPentagonShort S F f g h k))⁻¹) =
      (if nativeC60DYClosedAtomPrefix S F f = some (false :: word)
       then Multiplicative.ofAdd (1 : ℤ) else 1) := by
  change (nativeC60DYCharacter S F word)
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
  simp only [map_mul, map_inv, nativeC60DYCharacter_of]
  simp [nativeC60DYCodeCharge, nativeC60DYPostAssocPrefix,
    nativeC60DYClosedAtomPrefix, mul_assoc] <;> group

/-- An actual contextual CLOSED 17D atom with an explicitly DIFFERENT
AQ tag. No new geometric cell or additional type assumption is used. -/
def nativeC60DYOutsideSeventeenAtom
    (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b) :
    NativeC60AXStep (nativeC60DRClosedSeventeenSignature S F)
      (nativeC60BCContextTotal (nativeC60DRSeventeenFrame S F)
        (false :: word) a)
      (nativeC60BCContextTotal (nativeC60DRSeventeenFrame S F)
        (false :: word) b) :=
  .atom (nativeC60BCGen (nativeC60DQTriangleSeventeenSignature S F)
    (nativeC60DRSeventeenFrame S F) (false :: word) r)

/-- The genuine 17D contextual primitive and three 17D identities
provide a NEW 18D pentagon defect inside the full target presentation. -/
def nativeC60DYOutsidePentagonDefect
    (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b) :
    NativeC60DVClosedFullFree S F :=
  let f := nativeC60DYOutsideSeventeenAtom S F word r
  let id := NativeC60AXStep.refl
    (nativeC60BCContextTotal (nativeC60DRSeventeenFrame S F)
      (false :: word) b)
  nativeC60DVClosedFreeWord S F
      (nativeC60DXClosedPentagonLong S F f id id id) *
    (nativeC60DVClosedFreeWord S F
      (nativeC60DXClosedPentagonShort S F f id id id))⁻¹

/-- The newly constructed complete 18D defect has integer charge ONE.
In particular its free-group image cannot be a transported original. -/
theorem nativeC60DYOutsidePentagon_charge_one
    (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b) :
    (nativeC60DYCharacter S F word)
        (nativeC60DYOutsidePentagonDefect S F word r) =
      Multiplicative.ofAdd (1 : ℤ) := by
  unfold nativeC60DYOutsidePentagonDefect
  rw [nativeC60DYCharacter_full_pentagon S F word]
  simp [nativeC60DYOutsideSeventeenAtom,
    nativeC60DYClosedAtomPrefix, nativeC60BCGen]

/-- The full target pentagon relation REALLY supplies this defect. -/
theorem nativeC60DYOutsidePentagon_mem_full
    (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b) :
    nativeC60DYOutsidePentagonDefect S F word r ∈
      nativeC60DXFullClosedPentagonNormalClosure S F := by
  unfold nativeC60DYOutsidePentagonDefect
  exact nativeC60DXFullClosedPentagon_defect_mem S F _ _ _ _

/-- A constructed NONZERO integer-character obstruction, with no
supplementary cardinality, injectivity, or independent-geometry axiom. -/
theorem nativeC60DYOutsidePentagon_not_mem_image
    (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b) :
    nativeC60DYOutsidePentagonDefect S F word r ∉
      nativeC60DWContextPentagonNormalClosure S F word := by
  intro hmem
  have hk : (nativeC60DYCharacter S F word)
      (nativeC60DYOutsidePentagonDefect S F word r) = 1 :=
    MonoidHom.mem_ker.mp
      (nativeC60DYImageKernel_le_character_ker S F word hmem)
  rw [nativeC60DYOutsidePentagon_charge_one S F word r] at hk
  have hnonzero := congrArg Multiplicative.toAdd hk
  norm_num at hnonzero

/-- MAIN DY: an actual original 17D triangle generator is enough to
prove the DX normal-kernel inclusion is STRICT for EVERY finite AQ word. -/
theorem nativeC60DYImageKernel_ne_full
    (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b) :
    nativeC60DWContextPentagonNormalClosure S F word ≠
      nativeC60DXFullClosedPentagonNormalClosure S F := by
  intro heq
  have hmem : nativeC60DYOutsidePentagonDefect S F word r ∈
      nativeC60DWContextPentagonNormalClosure S F word := by
    rw [heq]
    exact nativeC60DYOutsidePentagon_mem_full S F word r
  exact nativeC60DYOutsidePentagon_not_mem_image S F word r hmem

theorem nativeC60DYImageKernel_proper
    (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b) :
    nativeC60DWContextPentagonNormalClosure S F word ≤
        nativeC60DXFullClosedPentagonNormalClosure S F ∧
    nativeC60DWContextPentagonNormalClosure S F word ≠
        nativeC60DXFullClosedPentagonNormalClosure S F :=
  ⟨nativeC60DXImageKernel_le_full S F word,
   nativeC60DYImageKernel_ne_full S F word r⟩

/-- Original DQ's real 16D zigzag comparison supplies a concrete
TYPE-valued 17D generator without assuming arbitrary nonempty alphabets. -/
def nativeC60DYOriginalZigzagGen
    {a b : L.Total}
    (g : (nativeC60BCClosedSignature S F).Gen a b) :
    (nativeC60DQTriangleSeventeenSignature S F).Gen
      (nativeC60DQPackSixteen S F (nativeC60DQRawZigzag S F g))
      (nativeC60DQPackSixteen S F (.atom g)) :=
  ⟨a, b, nativeC60DQRawZigzag S F g, .atom g,
    ⟨NativeC60CFTriangleRelation.zigzag g, ⟨rfl, rfl⟩⟩⟩

/-- Every original TRUE closed 16D generator suffices for proper
inclusion, via its constructed original DQ Type-valued 17D witness. -/
theorem nativeC60DYOriginalZigzagKernel_proper
    (word : List Bool)
    {a b : L.Total}
    (g : (nativeC60BCClosedSignature S F).Gen a b) :
    nativeC60DWContextPentagonNormalClosure S F word ≤
        nativeC60DXFullClosedPentagonNormalClosure S F ∧
    nativeC60DWContextPentagonNormalClosure S F word ≠
        nativeC60DXFullClosedPentagonNormalClosure S F :=
  nativeC60DYImageKernel_proper S F word
    (nativeC60DYOriginalZigzagGen S F g)

end ContextPrefixCharacter

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

/-- TRUE physical C60 AU with ANY finite actual AQ context tree:
its independently constructed 17D zigzag guarantees a STRICT
normal-kernel inclusion, not merely the DX conditional equality gate. -/
theorem nativeK5DYPhysicalAQ_fullKernel_proper
    (W : NativeK5StructuralThirteenCell p U V)
    (tree : NativeK5DOContextTree) :
    let S := nativeK5AXKuuSignature W
    let F := nativeK5BCFrame W
    nativeC60DWContextPentagonNormalClosure S F
        (nativeK5DOTreeWord tree) ≤
      nativeC60DXFullClosedPentagonNormalClosure S F ∧
    nativeC60DWContextPentagonNormalClosure S F
        (nativeK5DOTreeWord tree) ≠
      nativeC60DXFullClosedPentagonNormalClosure S F := by
  dsimp only
  exact nativeC60DYOriginalZigzagKernel_proper
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
    (nativeK5DOTreeWord tree) (nativeK5CEPhysicalAUGenerator W)

end PhysicalC60AU

#print axioms nativeC60DYClosedAtomPrefix
#print axioms nativeC60DYPostAssocPrefix
#print axioms nativeC60DYClosedAtomPrefix_transport_ne
#print axioms nativeC60DYPostAssocPrefix_transport_ne
#print axioms nativeC60DYCodeCharge
#print axioms nativeC60DYCharacter
#print axioms nativeC60DYCharacter_transport_one
#print axioms nativeC60DYImageKernel_le_character_ker
#print axioms nativeC60DYCharacter_full_pentagon
#print axioms nativeC60DYOutsidePentagonDefect
#print axioms nativeC60DYOutsidePentagon_charge_one
#print axioms nativeC60DYOutsidePentagon_mem_full
#print axioms nativeC60DYOutsidePentagon_not_mem_image
#print axioms nativeC60DYImageKernel_ne_full
#print axioms nativeC60DYImageKernel_proper
#print axioms nativeC60DYOriginalZigzagGen
#print axioms nativeC60DYOriginalZigzagKernel_proper
#print axioms nativeK5DYPhysicalAQ_fullKernel_proper

end
end Kuu.F112.Physical
