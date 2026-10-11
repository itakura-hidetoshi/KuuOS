import KUOS.DependentOriginationCoherentBiadjunctionBracketTreeRightMateCoherenceV5_149

namespace KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid

open CategoryTheory
open scoped CategoryTheory.Bicategory CategoryTheory.Oplax.LaxTrans
open KUOS.DependentOriginationCoherentBiadjunctionFiniteRectangularSubdivisionV5_137.Grid
open KUOS.DependentOriginationCoherentBiadjunctionExchangeQuotientConcatenationV5_141.Grid

set_option autoImplicit false
noncomputable section

/-!
# F53-A / v5.150 — the five genuinely typed vertices of the fourfold pentagon

F52 proved one three-subtree reassociation in the ORIGINAL F44
generated adjacent-exchange quotient. F53 records FIVE different
parenthesizations of FOUR already arbitrary finite original F45
subtrees, together with the five ACTUAL associativity edges.

Each vertex is an element of the original generated F44 quotient.
The arrows are equalities only AFTER the necessary independent
Nat-valued F19 and F28 depth casts — not fictitious definitional
identifications of differently associated natural-number sums.
The three-edge and two-edge routes around the Mac Lane pentagon
both reach the same final vertex. Equality proofs themselves are
proof-irrelevant Prop witnesses here: this is quotient-level
pentagon coherence, NOT an unproved tricategorical 3-cell law.

Every category, intermediate Blocks presentation, within-axis
primitive step order and original nonstrict mate remains unchanged.
-/

universe uD vD uE vE
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]

/-- An exact natural-number cast at the outer right context of a
genuine F44 original exchange-class composition. -/
theorem ExchangeClass.castDepths_appendLeft
    {a b : D} {x y : E}
    {n n' m m' k l : Nat}
    {ma mb mc : Blocks a b} {pa pb pc : Blocks x y}
    (en : n = n') (em : m = m')
    (first : ExchangeClass n m ma mb pa pb)
    (second : ExchangeClass k l mb mc pb pc) :
    ExchangeClass.castDepths
      (congrArg (fun t => t + k) en)
      (congrArg (fun t => t + l) em)
      (ExchangeClass.append first second) =
    ExchangeClass.append (ExchangeClass.castDepths en em first) second := by
  cases en
  cases em
  rfl

/-- Independent two-depth equality transport inside the right
context of F44 quotient concatenation; no cross-axis Hom coercion. -/
theorem ExchangeClass.castDepths_appendRight
    {a b : D} {x y : E}
    {n n' m m' k l : Nat}
    {ma mb mc : Blocks a b} {pa pb pc : Blocks x y}
    (en : n = n') (em : m = m')
    (first : ExchangeClass k l ma mb pa pb)
    (second : ExchangeClass n m mb mc pb pc) :
    ExchangeClass.castDepths
      (congrArg (fun t => k + t) en)
      (congrArg (fun t => l + t) em)
      (ExchangeClass.append first second) =
    ExchangeClass.append first (ExchangeClass.castDepths en em second) := by
  cases en
  cases em
  rfl

/-- Two consecutive genuine dependent depth casts compose EXACTLY
as the transitive equality proof in the original F44 quotient. -/
theorem ExchangeClass.castDepths_comp
    {a b : D} {x y : E}
    {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
    {ma mb : Blocks a b} {pa pb : Blocks x y}
    (en₁ : n₁ = n₂) (en₂ : n₂ = n₃)
    (em₁ : m₁ = m₂) (em₂ : m₂ = m₃)
    (c : ExchangeClass n₁ m₁ ma mb pa pb) :
    ExchangeClass.castDepths en₂ em₂
      (ExchangeClass.castDepths en₁ em₁ c) =
    ExchangeClass.castDepths (en₁.trans en₂) (em₁.trans em₂) c := by
  cases en₁
  cases en₂
  cases em₁
  cases em₂
  rfl

namespace F53Depth

/-- Pentagon edge (((ab)c)d) → ((a(bc))d). -/
def e01 (a b c d : Nat) :
    (((a + b) + c) + d) = ((a + (b + c)) + d) :=
  congrArg (fun t => t + d) (Nat.add_assoc a b c)

/-- Pentagon edge ((a(bc))d) → (a((bc)d)). -/
def e12 (a b c d : Nat) :
    ((a + (b + c)) + d) = (a + ((b + c) + d)) :=
  Nat.add_assoc a (b + c) d

/-- Pentagon edge (a((bc)d)) → (a(b(cd))). -/
def e23 (a b c d : Nat) :
    (a + ((b + c) + d)) = (a + (b + (c + d))) :=
  congrArg (fun t => a + t) (Nat.add_assoc b c d)

/-- Pentagon edge (((ab)c)d) → ((ab)(cd)). -/
def e04 (a b c d : Nat) :
    (((a + b) + c) + d) = ((a + b) + (c + d)) :=
  Nat.add_assoc (a + b) c d

/-- Pentagon edge ((ab)(cd)) → (a(b(cd))). -/
def e43 (a b c d : Nat) :
    ((a + b) + (c + d)) = (a + (b + (c + d))) :=
  Nat.add_assoc a b (c + d)

/-- The depth transport along the three-edge route. -/
def long (a b c d : Nat) :
    (((a + b) + c) + d) = (a + (b + (c + d))) :=
  (e01 a b c d).trans ((e12 a b c d).trans (e23 a b c d))

/-- The depth transport along the two-edge route. -/
def short (a b c d : Nat) :
    (((a + b) + c) + d) = (a + (b + (c + d))) :=
  (e04 a b c d).trans (e43 a b c d)

/-- The ORIGINAL two possible Nat depth transports agree as
equality proofs (in Prop), not by an added higher-dimensional axiom. -/
theorem long_eq_short (a b c d : Nat) :
    long a b c d = short a b c d :=
  Subsingleton.elim _ _

end F53Depth

section Fourfold

variable {a b : D} {x y : E}
variable {n₁ n₂ n₃ n₄ m₁ m₂ m₃ m₄ : Nat}
variable {p₀ p₁ p₂ p₃ p₄ : Blocks a b}
variable {q₀ q₁ q₂ q₃ q₄ : Blocks x y}
variable
  (h₁ : ExchangeClass n₁ m₁ p₀ p₁ q₀ q₁)
  (h₂ : ExchangeClass n₂ m₂ p₁ p₂ q₁ q₂)
  (h₃ : ExchangeClass n₃ m₃ p₂ p₃ q₂ q₃)
  (h₄ : ExchangeClass n₄ m₄ p₃ p₄ q₃ q₄)

/-- Vertex 0: (((A ⋆ B) ⋆ C) ⋆ D). -/
def ExchangeClass.pentagon0 :
    ExchangeClass (((n₁ + n₂) + n₃) + n₄)
      (((m₁ + m₂) + m₃) + m₄) p₀ p₄ q₀ q₄ :=
  ExchangeClass.append
    (ExchangeClass.append (ExchangeClass.append h₁ h₂) h₃) h₄

/-- Vertex 1: ((A ⋆ (B ⋆ C)) ⋆ D). -/
def ExchangeClass.pentagon1 :
    ExchangeClass ((n₁ + (n₂ + n₃)) + n₄)
      ((m₁ + (m₂ + m₃)) + m₄) p₀ p₄ q₀ q₄ :=
  ExchangeClass.append
    (ExchangeClass.append h₁ (ExchangeClass.append h₂ h₃)) h₄

/-- Vertex 2: (A ⋆ ((B ⋆ C) ⋆ D)). -/
def ExchangeClass.pentagon2 :
    ExchangeClass (n₁ + ((n₂ + n₃) + n₄))
      (m₁ + ((m₂ + m₃) + m₄)) p₀ p₄ q₀ q₄ :=
  ExchangeClass.append h₁
    (ExchangeClass.append (ExchangeClass.append h₂ h₃) h₄)

/-- Vertex 3: (A ⋆ (B ⋆ (C ⋆ D))). -/
def ExchangeClass.pentagon3 :
    ExchangeClass (n₁ + (n₂ + (n₃ + n₄)))
      (m₁ + (m₂ + (m₃ + m₄))) p₀ p₄ q₀ q₄ :=
  ExchangeClass.append h₁
    (ExchangeClass.append h₂ (ExchangeClass.append h₃ h₄))

/-- Vertex 4: ((A ⋆ B) ⋆ (C ⋆ D)). -/
def ExchangeClass.pentagon4 :
    ExchangeClass ((n₁ + n₂) + (n₃ + n₄))
      ((m₁ + m₂) + (m₃ + m₄)) p₀ p₄ q₀ q₄ :=
  ExchangeClass.append (ExchangeClass.append h₁ h₂)
    (ExchangeClass.append h₃ h₄)

/-- 0 → 1: the actual three-factor associator in the LEFT
context, followed by a fourth original F44 quotient path. -/
theorem ExchangeClass.pentagon01 :
    ExchangeClass.castDepths
      (F53Depth.e01 n₁ n₂ n₃ n₄)
      (F53Depth.e01 m₁ m₂ m₃ m₄)
      (ExchangeClass.pentagon0 h₁ h₂ h₃ h₄) =
    ExchangeClass.pentagon1 h₁ h₂ h₃ h₄ := by
  calc
    _ = ExchangeClass.append
          (ExchangeClass.castDepths
            (Nat.add_assoc n₁ n₂ n₃) (Nat.add_assoc m₁ m₂ m₃)
            (ExchangeClass.append (ExchangeClass.append h₁ h₂) h₃)) h₄ :=
      ExchangeClass.castDepths_appendLeft
        (Nat.add_assoc n₁ n₂ n₃) (Nat.add_assoc m₁ m₂ m₃)
        (ExchangeClass.append (ExchangeClass.append h₁ h₂) h₃) h₄
    _ = _ := congrArg (fun c => ExchangeClass.append c h₄)
      (ExchangeClass.append_assoc h₁ h₂ h₃)

/-- 1 → 2: the original F51 associator applied at the root. -/
theorem ExchangeClass.pentagon12 :
    ExchangeClass.castDepths
      (F53Depth.e12 n₁ n₂ n₃ n₄)
      (F53Depth.e12 m₁ m₂ m₃ m₄)
      (ExchangeClass.pentagon1 h₁ h₂ h₃ h₄) =
    ExchangeClass.pentagon2 h₁ h₂ h₃ h₄ :=
  ExchangeClass.append_assoc h₁ (ExchangeClass.append h₂ h₃) h₄

/-- 2 → 3: the actual three-factor associator within a RIGHT
context, retaining the FIRST original F19/F28 quotient path. -/
theorem ExchangeClass.pentagon23 :
    ExchangeClass.castDepths
      (F53Depth.e23 n₁ n₂ n₃ n₄)
      (F53Depth.e23 m₁ m₂ m₃ m₄)
      (ExchangeClass.pentagon2 h₁ h₂ h₃ h₄) =
    ExchangeClass.pentagon3 h₁ h₂ h₃ h₄ := by
  calc
    _ = ExchangeClass.append h₁
          (ExchangeClass.castDepths
            (Nat.add_assoc n₂ n₃ n₄) (Nat.add_assoc m₂ m₃ m₄)
            (ExchangeClass.append (ExchangeClass.append h₂ h₃) h₄)) :=
      ExchangeClass.castDepths_appendRight
        (Nat.add_assoc n₂ n₃ n₄) (Nat.add_assoc m₂ m₃ m₄)
        h₁ (ExchangeClass.append (ExchangeClass.append h₂ h₃) h₄)
    _ = _ := congrArg (fun c => ExchangeClass.append h₁ c)
      (ExchangeClass.append_assoc h₂ h₃ h₄)

/-- 0 → 4: the original F51 associator applied at the root. -/
theorem ExchangeClass.pentagon04 :
    ExchangeClass.castDepths
      (F53Depth.e04 n₁ n₂ n₃ n₄)
      (F53Depth.e04 m₁ m₂ m₃ m₄)
      (ExchangeClass.pentagon0 h₁ h₂ h₃ h₄) =
    ExchangeClass.pentagon4 h₁ h₂ h₃ h₄ :=
  ExchangeClass.append_assoc (ExchangeClass.append h₁ h₂) h₃ h₄

/-- 4 → 3: the original F51 associator for A, B, (C ⋆ D). -/
theorem ExchangeClass.pentagon43 :
    ExchangeClass.castDepths
      (F53Depth.e43 n₁ n₂ n₃ n₄)
      (F53Depth.e43 m₁ m₂ m₃ m₄)
      (ExchangeClass.pentagon4 h₁ h₂ h₃ h₄) =
    ExchangeClass.pentagon3 h₁ h₂ h₃ h₄ :=
  ExchangeClass.append_assoc h₁ h₂ (ExchangeClass.append h₃ h₄)

/-- The LONG (three-associator) pentagon route has the actual
right-associated F44 class as its endpoint after BOTH depth casts. -/
theorem ExchangeClass.pentagonLong :
    ExchangeClass.castDepths
      (F53Depth.long n₁ n₂ n₃ n₄)
      (F53Depth.long m₁ m₂ m₃ m₄)
      (ExchangeClass.pentagon0 h₁ h₂ h₃ h₄) =
    ExchangeClass.pentagon3 h₁ h₂ h₃ h₄ := by
  calc
    _ = ExchangeClass.castDepths
          ((F53Depth.e12 n₁ n₂ n₃ n₄).trans
            (F53Depth.e23 n₁ n₂ n₃ n₄))
          ((F53Depth.e12 m₁ m₂ m₃ m₄).trans
            (F53Depth.e23 m₁ m₂ m₃ m₄))
          (ExchangeClass.castDepths
            (F53Depth.e01 n₁ n₂ n₃ n₄)
            (F53Depth.e01 m₁ m₂ m₃ m₄)
            (ExchangeClass.pentagon0 h₁ h₂ h₃ h₄)) :=
      (ExchangeClass.castDepths_comp _ _ _ _
        (ExchangeClass.pentagon0 h₁ h₂ h₃ h₄)).symm
    _ = ExchangeClass.castDepths
          (F53Depth.e23 n₁ n₂ n₃ n₄)
          (F53Depth.e23 m₁ m₂ m₃ m₄)
          (ExchangeClass.castDepths
            (F53Depth.e12 n₁ n₂ n₃ n₄)
            (F53Depth.e12 m₁ m₂ m₃ m₄)
            (ExchangeClass.castDepths
              (F53Depth.e01 n₁ n₂ n₃ n₄)
              (F53Depth.e01 m₁ m₂ m₃ m₄)
              (ExchangeClass.pentagon0 h₁ h₂ h₃ h₄))) :=
      (ExchangeClass.castDepths_comp _ _ _ _
        (ExchangeClass.castDepths
          (F53Depth.e01 n₁ n₂ n₃ n₄)
          (F53Depth.e01 m₁ m₂ m₃ m₄)
          (ExchangeClass.pentagon0 h₁ h₂ h₃ h₄))).symm
    _ = ExchangeClass.pentagon3 h₁ h₂ h₃ h₄ := by
      rw [ExchangeClass.pentagon01, ExchangeClass.pentagon12,
        ExchangeClass.pentagon23]

/-- The SHORT (two-associator) pentagon route arrives at the EXACT
same original generated exchange class, with two independent casts. -/
theorem ExchangeClass.pentagonShort :
    ExchangeClass.castDepths
      (F53Depth.short n₁ n₂ n₃ n₄)
      (F53Depth.short m₁ m₂ m₃ m₄)
      (ExchangeClass.pentagon0 h₁ h₂ h₃ h₄) =
    ExchangeClass.pentagon3 h₁ h₂ h₃ h₄ := by
  calc
    _ = ExchangeClass.castDepths
          (F53Depth.e43 n₁ n₂ n₃ n₄)
          (F53Depth.e43 m₁ m₂ m₃ m₄)
          (ExchangeClass.castDepths
            (F53Depth.e04 n₁ n₂ n₃ n₄)
            (F53Depth.e04 m₁ m₂ m₃ m₄)
            (ExchangeClass.pentagon0 h₁ h₂ h₃ h₄)) :=
      (ExchangeClass.castDepths_comp _ _ _ _
        (ExchangeClass.pentagon0 h₁ h₂ h₃ h₄)).symm
    _ = ExchangeClass.pentagon3 h₁ h₂ h₃ h₄ := by
      rw [ExchangeClass.pentagon04, ExchangeClass.pentagon43]

/-- THE FOURFOLD PENTAGON. Both distinct actual paths of F51
associativity through the FIVE explicitly constructed F44 vertices
reach the SAME exact original quotient class, and their two
independent depth transports agree as Prop equality witnesses.
No new tricategorical modification equality is asserted. -/
theorem ExchangeClass.fourfoldPentagon :
    (ExchangeClass.castDepths
      (F53Depth.long n₁ n₂ n₃ n₄)
      (F53Depth.long m₁ m₂ m₃ m₄)
      (ExchangeClass.pentagon0 h₁ h₂ h₃ h₄) =
     ExchangeClass.pentagon3 h₁ h₂ h₃ h₄) ∧
    (ExchangeClass.castDepths
      (F53Depth.short n₁ n₂ n₃ n₄)
      (F53Depth.short m₁ m₂ m₃ m₄)
      (ExchangeClass.pentagon0 h₁ h₂ h₃ h₄) =
     ExchangeClass.pentagon3 h₁ h₂ h₃ h₄) ∧
    (F53Depth.long n₁ n₂ n₃ n₄ =
      F53Depth.short n₁ n₂ n₃ n₄) ∧
    (F53Depth.long m₁ m₂ m₃ m₄ =
      F53Depth.short m₁ m₂ m₃ m₄) :=
  ⟨ExchangeClass.pentagonLong h₁ h₂ h₃ h₄,
   ExchangeClass.pentagonShort h₁ h₂ h₃ h₄,
   F53Depth.long_eq_short _ _ _ _,
   F53Depth.long_eq_short _ _ _ _⟩

end Fourfold

#print axioms ExchangeClass.castDepths_appendLeft
#print axioms ExchangeClass.castDepths_appendRight
#print axioms ExchangeClass.castDepths_comp
#print axioms F53Depth.e01
#print axioms F53Depth.e12
#print axioms F53Depth.e23
#print axioms F53Depth.e04
#print axioms F53Depth.e43
#print axioms F53Depth.long
#print axioms F53Depth.short
#print axioms F53Depth.long_eq_short
#print axioms ExchangeClass.pentagon0
#print axioms ExchangeClass.pentagon1
#print axioms ExchangeClass.pentagon2
#print axioms ExchangeClass.pentagon3
#print axioms ExchangeClass.pentagon4
#print axioms ExchangeClass.pentagon01
#print axioms ExchangeClass.pentagon12
#print axioms ExchangeClass.pentagon23
#print axioms ExchangeClass.pentagon04
#print axioms ExchangeClass.pentagon43
#print axioms ExchangeClass.pentagonLong
#print axioms ExchangeClass.pentagonShort
#print axioms ExchangeClass.fourfoldPentagon

end
end KUOS.DependentOriginationCoherentBiadjunctionInterleavingExchangeQuotientV5_141.Grid
