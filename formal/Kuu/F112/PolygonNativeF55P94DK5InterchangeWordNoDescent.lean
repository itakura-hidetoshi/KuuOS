import Kuu.F112.PolygonNativeF55P94DK5NineFaceAnchoredBoundaries
import Mathlib.GroupTheory.FreeGroup.Basic
import Mathlib.Tactic

/-!
# F112-P94D3B — actual K5 pentagon/naturality interchange obstructs free-word descent

P94C3 records each genuine original F55 pentagon (P), new P92B
associator-naturality proof (N), and original F55 disjoint square (S)
as an ORDERED nonabelian free additive group word. Its abelian shadow
is preserved, but the raw nonabelian word has never been shown to
descend to P94A or to the distinct P94C groupoid presentation.

Here PROVE a concrete four-dimensional obstruction rather than merely
saying that descent is unknown:
* P and N do not commute in a finite S3 receiver.
* The ORIGINAL P94A horizontal interchange admits an actual typed
  FOUR-cell between (id;P) ⊗ (N;id) and
  (id⊗N) ; (P⊗id). Their full shadows match, but raw nonabelian
  F55/P92B words are P+N and N+P, which are NOT equal.
* Thus no function from the exact P94A four-cell quotient to this
  original noncommutative free group can factor the word map over
  ALL original 3-proof representatives.
* Instantiate using the genuine five ordered north C60 F45 stages
  (all five real physical sectors) and a following composable
  five-stage genuine original F45 unit context. This is a REAL
  typed source, not independent abstract letters without provenance.

This is an obstruction to the NAIVE PRE-QUOTIENT word observer, not a
proof that 4D K5 pentagonator coherence is impossible. Group-theoretic
normal closure / crossed-module corrections remain required.

No Gray, new logical axioms, sorry or admit.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

/-- A finite nonabelian observer sensitive to the new naturality
generator: unlike the P94C3 receiver that killed N, send
P=(01), N=(12), and S=identity in S3. -/
def nativeK5WordPentagonNaturalityS3 :
    NativeF55P94CWord →+ Additive (Equiv.Perm (Fin 3)) :=
  FreeAddGroup.lift (fun
    | .pentagon => Additive.ofMul (Equiv.swap (0 : Fin 3) (1 : Fin 3))
    | .square => 0
    | .assocNaturality => Additive.ofMul (Equiv.swap (1 : Fin 3) (2 : Fin 3)))

/-- Formal proof that the two actual F55/P92B generator tags do NOT
commute, using distinct transpositions of the finite group S3. -/
theorem nativeK5Word_pentagon_naturality_noncommute :
    (FreeAddGroup.of .pentagon : NativeF55P94CWord) +
        FreeAddGroup.of .assocNaturality ≠
    (FreeAddGroup.of .assocNaturality : NativeF55P94CWord) +
        FreeAddGroup.of .pentagon := by
  intro h
  have hh := congrArg nativeK5WordPentagonNaturalityS3 h
  simp only [map_add, FreeAddGroup.lift_apply_of] at hh
  change
    Equiv.swap (0 : Fin 3) (1 : Fin 3) *
      Equiv.swap (1 : Fin 3) (2 : Fin 3) =
    Equiv.swap (1 : Fin 3) (2 : Fin 3) *
      Equiv.swap (0 : Fin 3) (1 : Fin 3) at hh
  exact (by decide :
    Equiv.swap (0 : Fin 3) (1 : Fin 3) *
      Equiv.swap (1 : Fin 3) (2 : Fin 3) ≠
    Equiv.swap (1 : Fin 3) (2 : Fin 3) *
      Equiv.swap (0 : Fin 3) (1 : Fin 3)) hh

/-- But the COMPLETE original signed F55 shadow is commutative,
so it cannot distinguish the same two ordered group words. -/
theorem nativeK5Word_pentagon_naturality_shadow_commute :
    nativeF55P94CWordToShadow
      ((FreeAddGroup.of .pentagon : NativeF55P94CWord) +
        FreeAddGroup.of .assocNaturality) =
    nativeF55P94CWordToShadow
      ((FreeAddGroup.of .assocNaturality : NativeF55P94CWord) +
        FreeAddGroup.of .pentagon) := by
  simp only [map_add, FreeAddGroup.lift_apply_of]
  exact add_comm _ _

/-- The existing genuine horizontal P92B 3-cell pasting has exactly
the concatenated ordered free-group word of its two ORIGINAL inputs.
Contexts and route whiskers preserve ordering; no new exchange is
silently assumed at the raw witness level. -/
theorem NativeF55P92AssocComparison.horizontal_p94cGroupWord
    {p : Polygon} {a b : D} {x y : E}
    {n n' m m' k k' l l' : Nat}
    {p₀ p₁ p₂ : KuuNativeBlocks a b}
    {q₀ q₁ q₂ : KuuNativeBlocks x y}
    {leftBefore : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
    {leftAfter : KuuNativeF45Tree p n' m' p₀ q₀ p₁ q₁}
    {rightBefore : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂}
    {rightAfter : KuuNativeF45Tree p k' l' p₁ q₁ p₂ q₂}
    {u u' : KuuNativeF45Tree.DepthRotationRoute p leftBefore leftAfter}
    {v v' : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter}
    (f : NativeF55P92AssocComparison p u u')
    (g : NativeF55P92AssocComparison p v v') :
    (f.horizontal g).p94cGroupWord = f.p94cGroupWord + g.p94cGroupWord := rfl

section IndependentTwoFactors

variable {p : Polygon} {a b : D} {x y : E}
variable {n n' m m' k k' l l' : Nat}
variable {p₀ p₁ p₂ : KuuNativeBlocks a b}
variable {q₀ q₁ q₂ : KuuNativeBlocks x y}
variable {leftBefore : KuuNativeF45Tree p n m p₀ q₀ p₁ q₁}
variable {leftAfter : KuuNativeF45Tree p n' m' p₀ q₀ p₁ q₁}
variable {rightBefore : KuuNativeF45Tree p k l p₁ q₁ p₂ q₂}
variable {rightAfter : KuuNativeF45Tree p k' l' p₁ q₁ p₂ q₂}
variable {u u' : KuuNativeF45Tree.DepthRotationRoute p leftBefore leftAfter}
variable {v v' : KuuNativeF45Tree.DepthRotationRoute p rightBefore rightAfter}
variable
  (P : NativeF55P92AssocComparison p u u')
  (N : NativeF55P92AssocComparison p v v')

/-- The two genuinely source-typed P94A INTERCHANGE boundary
proofs share exact F54 route endpoints. No new 4-cell axiom. -/
def nativeK5InterchangeFirstPasting :
    NativeF55P92AssocComparison p
      (nativeF54P90HorizontalRoute u v)
      (nativeF54P90HorizontalRoute u' v') :=
  (NativeF55P92AssocComparison.trans (.refl u) P).horizontal
    (NativeF55P92AssocComparison.trans N (.refl v'))

def nativeK5InterchangeSecondPasting :
    NativeF55P92AssocComparison p
      (nativeF54P90HorizontalRoute u v)
      (nativeF54P90HorizontalRoute u' v') :=
  NativeF55P92AssocComparison.trans
    ((NativeF55P92AssocComparison.refl u).horizontal N)
    (P.horizontal (NativeF55P92AssocComparison.refl v'))

/-- ACTUAL existing Type-valued P94A 4-cell compares the two
pasting orders, independently of their numerical shadows. -/
def nativeK5InterchangeFourCell :
    NativeF55P94UnitFourCell
      (nativeK5InterchangeFirstPasting P N)
      (nativeK5InterchangeSecondPasting P N) :=
  .interchange (.refl u) P N (.refl v')

/-- The FIRST P94A 3-pasting records ordered P-then-N words. -/
theorem nativeK5InterchangeFirstWord :
    (nativeK5InterchangeFirstPasting P N).p94cGroupWord =
      P.p94cGroupWord + N.p94cGroupWord := by
  change ((0 : NativeF55P94CWord) + P.p94cGroupWord) +
      (N.p94cGroupWord + 0) =
        P.p94cGroupWord + N.p94cGroupWord
  simp

/-- The SECOND P94A 3-pasting records ordered N-then-P words. -/
theorem nativeK5InterchangeSecondWord :
    (nativeK5InterchangeSecondPasting P N).p94cGroupWord =
      N.p94cGroupWord + P.p94cGroupWord := by
  change ((0 : NativeF55P94CWord) + N.p94cGroupWord) +
      (P.p94cGroupWord + 0) =
        N.p94cGroupWord + P.p94cGroupWord
  simp

theorem nativeK5InterchangeFourCell_fullShadow :
    (nativeK5InterchangeFirstPasting P N).nativeShadow =
      (nativeK5InterchangeSecondPasting P N).nativeShadow :=
  (nativeK5InterchangeFourCell P N).shadow_sound

/-- A REAL P94A Type-valued 4-witness whose two raw source
words are UNEQUAL whenever the two factor sources carry P and N.
This directly disproves unqualified descent of the P94C3 word map. -/
theorem nativeK5InterchangeFourCell_wordMismatch
    (hP : P.p94cGroupWord =
      (FreeAddGroup.of .pentagon : NativeF55P94CWord))
    (hN : N.p94cGroupWord =
      (FreeAddGroup.of .assocNaturality : NativeF55P94CWord)) :
    Nonempty (NativeF55P94UnitFourCell
      (nativeK5InterchangeFirstPasting P N)
      (nativeK5InterchangeSecondPasting P N)) ∧
    (nativeK5InterchangeFirstPasting P N).p94cGroupWord ≠
      (nativeK5InterchangeSecondPasting P N).p94cGroupWord := by
  constructor
  · exact ⟨nativeK5InterchangeFourCell P N⟩
  · rw [nativeK5InterchangeFirstWord, nativeK5InterchangeSecondWord,
      hP, hN]
    exact nativeK5Word_pentagon_naturality_noncommute

/-- If the free-word map factored through P94A's actual
Type-witness quotient, the two interchange-related classes
would receive the SAME word, contradicting their proven
noncommutativity. Hence such a factorization DOES NOT EXIST. -/
theorem nativeK5Interchange_no_freeWord_descent_P94A
    (hP : P.p94cGroupWord =
      (FreeAddGroup.of .pentagon : NativeF55P94CWord))
    (hN : N.p94cGroupWord =
      (FreeAddGroup.of .assocNaturality : NativeF55P94CWord)) :
    ¬ ∃ (desc :
        NativeF55P94UnitFourClasses
          (KuuNativeF45Tree.node leftBefore rightBefore)
          (KuuNativeF45Tree.node leftAfter rightAfter)
          (nativeF54P90HorizontalRoute u v)
          (nativeF54P90HorizontalRoute u' v') →
          NativeF55P94CWord),
        ∀ (c : NativeF55P92AssocComparison p
          (nativeF54P90HorizontalRoute u v)
          (nativeF54P90HorizontalRoute u' v')),
          desc (nativeF55P94UnitFourClass _ _ c) = c.p94cGroupWord := by
  rintro ⟨desc, hdesc⟩
  have hclass :
      nativeF55P94UnitFourClass _ _
          (nativeK5InterchangeFirstPasting P N) =
      nativeF55P94UnitFourClass _ _
          (nativeK5InterchangeSecondPasting P N) :=
    Quot.sound ⟨nativeK5InterchangeFourCell P N⟩
  have hw :
      (nativeK5InterchangeFirstPasting P N).p94cGroupWord =
      (nativeK5InterchangeSecondPasting P N).p94cGroupWord := by
    calc
      (nativeK5InterchangeFirstPasting P N).p94cGroupWord =
          desc (nativeF55P94UnitFourClass _ _
            (nativeK5InterchangeFirstPasting P N)) := (hdesc _).symm
      _ = desc (nativeF55P94UnitFourClass _ _
            (nativeK5InterchangeSecondPasting P N)) := congrArg desc hclass
      _ = (nativeK5InterchangeSecondPasting P N).p94cGroupWord := hdesc _
  exact (nativeK5InterchangeFourCell_wordMismatch P N hP hN).2 hw

/-- The distinctly completed P94C2 groupoid also retains the
P94A interchange witness, so the same ORIGINAL free word cannot
factor through this groupoid four-cell quotient either. -/
theorem nativeK5Interchange_no_freeWord_descent_groupoid
    (hP : P.p94cGroupWord =
      (FreeAddGroup.of .pentagon : NativeF55P94CWord))
    (hN : N.p94cGroupWord =
      (FreeAddGroup.of .assocNaturality : NativeF55P94CWord)) :
    ¬ ∃ (desc :
        NativeF55P94GroupFourClasses
          (KuuNativeF45Tree.node leftBefore rightBefore)
          (KuuNativeF45Tree.node leftAfter rightAfter)
          (nativeF54P90HorizontalRoute u v)
          (nativeF54P90HorizontalRoute u' v') →
          NativeF55P94CWord),
        ∀ (c : NativeF55P92AssocComparison p
          (nativeF54P90HorizontalRoute u v)
          (nativeF54P90HorizontalRoute u' v')),
          desc (nativeF55P94GroupFourClass _ _ c) = c.p94cGroupWord := by
  rintro ⟨desc, hdesc⟩
  have hclass :
      nativeF55P94GroupFourClass _ _
          (nativeK5InterchangeFirstPasting P N) =
      nativeF55P94GroupFourClass _ _
          (nativeK5InterchangeSecondPasting P N) :=
    Quot.sound ⟨NativeF55P94GroupFourCell.old
      (nativeK5InterchangeFourCell P N)⟩
  have hw :
      (nativeK5InterchangeFirstPasting P N).p94cGroupWord =
      (nativeK5InterchangeSecondPasting P N).p94cGroupWord := by
    calc
      (nativeK5InterchangeFirstPasting P N).p94cGroupWord =
          desc (nativeF55P94GroupFourClass _ _
            (nativeK5InterchangeFirstPasting P N)) := (hdesc _).symm
      _ = desc (nativeF55P94GroupFourClass _ _
            (nativeK5InterchangeSecondPasting P N)) := congrArg desc hclass
      _ = (nativeK5InterchangeSecondPasting P N).p94cGroupWord := hdesc _
  exact (nativeK5InterchangeFourCell_wordMismatch P N hP hN).2 hw

end IndependentTwoFactors

/-- Original north C60 pentagon: FIVE genuinely distinct physical
sectors, exact consecutive F19/F28 Blocks and P92B original proof. -/
def northK5OriginalPentagonPSource :=
  nativeK5PentagonFace3
    northNativeF45FirstStage northNativeF45SecondStage
    northNativeF45ThirdStage northNativeF45FourthStage
    northNativeF45FifthStage

/-- The next five composable original-F45 stages are genuine
zero-depth unit execution witnesses over the OUTPUT native Blocks
of the north five-stage pentagon. This is a second horizontal factor,
not a fictional fifth face on the same four-stage pentagon. -/
def northK5SourceUnitStage :=
  KuuNativeF45Tree.refl northK5FifthSector
    northNativeF45FirstFifth northNativeF45SecondFifth

/-- The explicitly adjoined NEW P92B associator-naturality generator
on three of those physically typed unit stages; no historical F55
naturality witness is invented. -/
def northK5OriginalNaturalityNSource :=
  nativeK5NaturalitySquare0
    northK5SourceUnitStage northK5SourceUnitStage
    northK5SourceUnitStage northK5SourceUnitStage
    northK5SourceUnitStage

theorem northK5OriginalPentagonPSource_groupWord :
    northK5OriginalPentagonPSource.p94cGroupWord =
      (FreeAddGroup.of .pentagon : NativeF55P94CWord) := rfl

theorem northK5OriginalNaturalityNSource_groupWord :
    northK5OriginalNaturalityNSource.p94cGroupWord =
      (FreeAddGroup.of .assocNaturality : NativeF55P94CWord) := rfl

/-- Concrete north C60 source certificate:
an ACTUAL P94A 4-cell exists, preserves full F55 shadow,
but relates two UNEQUAL pre-4-cell free group words. -/
theorem northK5InterchangeFourCell_wordMismatch :
    Nonempty (NativeF55P94UnitFourCell
      (nativeK5InterchangeFirstPasting
        northK5OriginalPentagonPSource northK5OriginalNaturalityNSource)
      (nativeK5InterchangeSecondPasting
        northK5OriginalPentagonPSource northK5OriginalNaturalityNSource)) ∧
    (nativeK5InterchangeFirstPasting
      northK5OriginalPentagonPSource northK5OriginalNaturalityNSource).p94cGroupWord ≠
    (nativeK5InterchangeSecondPasting
      northK5OriginalPentagonPSource northK5OriginalNaturalityNSource).p94cGroupWord :=
  nativeK5InterchangeFourCell_wordMismatch
    northK5OriginalPentagonPSource northK5OriginalNaturalityNSource
    northK5OriginalPentagonPSource_groupWord
    northK5OriginalNaturalityNSource_groupWord

#print axioms nativeK5WordPentagonNaturalityS3
#print axioms nativeK5Word_pentagon_naturality_noncommute
#print axioms nativeK5Word_pentagon_naturality_shadow_commute
#print axioms NativeF55P92AssocComparison.horizontal_p94cGroupWord
#print axioms nativeK5InterchangeFirstPasting
#print axioms nativeK5InterchangeSecondPasting
#print axioms nativeK5InterchangeFourCell
#print axioms nativeK5InterchangeFirstWord
#print axioms nativeK5InterchangeSecondWord
#print axioms nativeK5InterchangeFourCell_fullShadow
#print axioms nativeK5InterchangeFourCell_wordMismatch
#print axioms nativeK5Interchange_no_freeWord_descent_P94A
#print axioms nativeK5Interchange_no_freeWord_descent_groupoid
#print axioms northK5OriginalPentagonPSource
#print axioms northK5SourceUnitStage
#print axioms northK5OriginalNaturalityNSource
#print axioms northK5OriginalPentagonPSource_groupWord
#print axioms northK5OriginalNaturalityNSource_groupWord
#print axioms northK5InterchangeFourCell_wordMismatch

end
end Kuu.F112.Physical
