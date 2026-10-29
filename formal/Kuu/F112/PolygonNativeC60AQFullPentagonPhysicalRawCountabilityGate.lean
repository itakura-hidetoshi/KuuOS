import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalSourceCardinality

/-!
# F112-P94D3FZ — proof-relevant source countability from actual
# dependent raw17D and recursive assoc/post/pre constructor syntax

The historical FY result requires original 18D source Countable
to conclude exact aleph-null normal rank. This module works toward
an explicit, type-preserving smallness gate from the actual lower
dependent evidence, not just the finite geometric size of C60.

Retain raw original 14D-17D proof witnesses and signed noncommutative
FreeGroup source. No new axioms, sorry/admit, Gray, universal 19D filler,
or unconditional countability claims. Pinned Lean/mathlib and 107
published roots remain invariant.
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

/-! The pinned mathlib Countable deriving handler cannot infer
the heterogeneous original S.Gen x y fiber cardinal hypotheses
from an arbitrary NativeC60AXSignature. We therefore make every
actual lower proof-fiber premise explicit rather than assuming a
nonexistent unconditional Countable instance for indexed raw proof
terms. These are genuine obstruction boundaries, not sorry placeholders.
-/

section TypedCountabilityPropagation

variable {L : NativeC60AXLayer.{u}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- The true raw17D step TOTAL is countable once its original
dependent 17D endpoint codes and each corresponding exact step
fiber are countable, without truncating raw proof data. -/
theorem nativeC60FZRawSeventeenTotal_countable
    (hobjects : Countable (nativeC60DQSeventeenLayer S F).Total)
    (hpaths : ∀ a b : (nativeC60DQSeventeenLayer S F).Total,
      Countable (NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b)) :
    Countable (Σ a : (nativeC60DQSeventeenLayer S F).Total,
      Σ b : (nativeC60DQSeventeenLayer S F).Total,
        NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b) := by
  letI : Countable (nativeC60DQSeventeenLayer S F).Total := hobjects
  letI : ∀ a b : (nativeC60DQSeventeenLayer S F).Total,
      Countable (NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b) :=
    hpaths
  infer_instance

/-- Actual 18D layer objects are dependent raw17D paths, not a
numeric C60-vertex code or a quotient. -/
theorem nativeC60FZEighteenObject_countable_of_rawSeventeen
    (hobjects : Countable (nativeC60DQSeventeenLayer S F).Total)
    (hpaths : ∀ a b : (nativeC60DQSeventeenLayer S F).Total,
      Countable (NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b)) :
    Countable (nativeC60DREighteenLayer S F).Total := by
  have htotal := nativeC60FZRawSeventeenTotal_countable S F hobjects hpaths
  letI : Countable (nativeC60DQSeventeenLayer S F).Total := hobjects
  letI : ∀ a b : (nativeC60DQSeventeenLayer S F).Total,
    Countable (NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b) :=
    hpaths
  change Countable
    (Σ endpoints : ((nativeC60DQSeventeenLayer S F).Total ×
      (nativeC60DQSeventeenLayer S F).Total),
      NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F)
        endpoints.1 endpoints.2)
  infer_instance

/-- Precise sufficient gate for the full original proof-relevant
18D alphabet: Countable endpoints and Countable indexed actual
assoc/post/pre generator fibers. It is NOT an assumption that the
finite C60 geometry makes arbitrary input Hom types countable. -/
theorem nativeC60FZFullOriginalEighteen_countable_of_countable_fibers
    (hobjects : Countable (nativeC60DREighteenLayer S F).Total)
    (hgen : ∀ x y : (nativeC60DREighteenLayer S F).Total,
      Countable ((nativeC60DREighteenAssocSignature S F).Gen x y)) :
    Countable (NativeC60DSCompleteEighteenCode S F) := by
  letI : Countable (nativeC60DREighteenLayer S F).Total := hobjects
  letI : ∀ x y : (nativeC60DREighteenLayer S F).Total,
    Countable ((nativeC60DREighteenAssocSignature S F).Gen x y) := hgen
  exact inferInstance

/-- Compose the exact 17D raw proof family gate with the 18D
recursive generator-family gate, without hiding either premise. -/
theorem nativeC60FZFullOriginalEighteen_countable_of_rawAndGen
    (hobjects : Countable (nativeC60DQSeventeenLayer S F).Total)
    (hpaths : ∀ a b : (nativeC60DQSeventeenLayer S F).Total,
      Countable (NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b))
    (hgen : ∀ x y : (nativeC60DREighteenLayer S F).Total,
      Countable ((nativeC60DREighteenAssocSignature S F).Gen x y)) :
    Countable (NativeC60DSCompleteEighteenCode S F) :=
  nativeC60FZFullOriginalEighteen_countable_of_countable_fibers S F
    (nativeC60FZEighteenObject_countable_of_rawSeventeen S F hobjects hpaths)
    hgen

end TypedCountabilityPropagation

/-- A precise general arithmetic gate: when the actual received
image is countable and the original nonroot rooted-support subtype
is infinite, there is a normal presentation of EXACT cardinal
aleph-null IFF the COMPLETE original source alphabet is countable.

The reverse direction is not a consequence of simply having an
infinite set of independent relations: it uses the sharp FX
cardinality LOWER bound for arbitrary non-rooted group-word families
and FY's exact original source = active + image type decomposition. -/
theorem nativeC60FZSource_countable_iff_exactAleph0NormalRank_of_imageCountable
    {A : Type u} {B : Type v} (f : A → B)
    (himage : Countable (Set.range f))
    (hinfinite : Infinite (nativeC60FSActiveLetters f)) :
    Countable A ↔
      (∃ R : Set (FreeGroup A),
        (FreeGroup.map f).ker = Subgroup.normalClosure R ∧
          #R = ℵ₀) := by
  classical
  constructor
  · intro hsource
    have hactive :
        Countable (nativeC60FSActiveLetters f) :=
      (nativeC60FYSource_countable_iff_active_and_image_countable f).mp
        hsource |>.1
    letI : Countable (nativeC60FSActiveLetters f) := hactive
    letI : Infinite (nativeC60FSActiveLetters f) := hinfinite
    obtain ⟨R, hR, hcard⟩ :=
      nativeC60FXCanonicalNormalGenerators_exact_cardinal f
    exact ⟨R, hR, hcard.trans (Cardinal.mk_eq_aleph0 _)⟩
  · rintro ⟨R, hR, hcard⟩
    have hle : #(nativeC60FSActiveLetters f) ≤ ℵ₀ := by
      calc
        #(nativeC60FSActiveLetters f) ≤ #R :=
          nativeC60FXAnyNormalGenerators_cardinal_lower f R hR
        _ = ℵ₀ := hcard
    have hactive : Countable (nativeC60FSActiveLetters f) :=
      (Cardinal.mk_le_aleph0_iff).mp hle
    exact (nativeC60FYSource_countable_iff_active_and_image_countable f).mpr
      ⟨hactive, himage⟩

/-- If the original source alphabet is uncountable but its actual
received image is countable, the active original-source support
must remain uncountable. It is unsound to drop this obstruction
by replacing the source with a finite graph or numeric shadow. -/
theorem nativeC60FZActive_notCountable_of_source_and_image
    {A : Type u} {B : Type v} (f : A → B)
    (hsource : ¬ Countable A)
    (himage : Countable (Set.range f)) :
    ¬ Countable (nativeC60FSActiveLetters f) := by
  intro hactive
  exact hsource
    ((nativeC60FYSource_countable_iff_active_and_image_countable f).mpr
      ⟨hactive, himage⟩)



section ActualPhysicalRawCountabilityGate

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


/-- The true original proof-relevant 18D source alphabet is
countable if its actual original 17D object type, every dependent
raw17D proof fiber, and every dependent assoc/post/pre generator
fiber are countable. None of these assumptions is inferred
from the finite C60 geometry. -/
theorem nativeK5FZPhysical_original18_countable_of_rawAndGen
    (W : NativeK5StructuralThirteenCell p U V)
    (hobjects :
      Countable
        (nativeC60DQSeventeenLayer
          (nativeK5AXKuuSignature W) (nativeK5BCFrame W)).Total)
    (hpaths : ∀ a b :
        (nativeC60DQSeventeenLayer
          (nativeK5AXKuuSignature W) (nativeK5BCFrame W)).Total,
        Countable
          (NativeC60AXStep
            (nativeC60DQTriangleSeventeenSignature
              (nativeK5AXKuuSignature W) (nativeK5BCFrame W)) a b))
    (hgen : ∀ x y :
        (nativeC60DREighteenLayer
          (nativeK5AXKuuSignature W) (nativeK5BCFrame W)).Total,
        Countable
          ((nativeC60DREighteenAssocSignature
            (nativeK5AXKuuSignature W) (nativeK5BCFrame W)).Gen x y)) :
    Countable (NativeC60DSCompleteEighteenCode
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)) :=
  nativeC60FZFullOriginalEighteen_countable_of_rawAndGen
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
    hobjects hpaths hgen

/-- The first genuine physical conditional rank certificate
whose countability is explicitly traced to actual typed raw17D
objects/path fibers and actual recursive 18D generator fibers.

All actual original signed 18D free-group words are allowed in R;
the conclusion is sharp minimum normal rank aleph-null, not merely
the existence of infinitely many collisions. -/
theorem nativeK5FZPhysical_fullDV_aleph0NormalRank_of_rawAndGen
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool) (hne : word ≠ [])
    (hobjects :
      Countable
        (nativeC60DQSeventeenLayer
          (nativeK5AXKuuSignature W) (nativeK5BCFrame W)).Total)
    (hpaths : ∀ a b :
        (nativeC60DQSeventeenLayer
          (nativeK5AXKuuSignature W) (nativeK5BCFrame W)).Total,
        Countable
          (NativeC60AXStep
            (nativeC60DQTriangleSeventeenSignature
              (nativeK5AXKuuSignature W) (nativeK5BCFrame W)) a b))
    (hgen : ∀ x y :
        (nativeC60DREighteenLayer
          (nativeK5AXKuuSignature W) (nativeK5BCFrame W)).Total,
        Countable
          ((nativeC60DREighteenAssocSignature
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
    (nativeK5FZPhysical_original18_countable_of_rawAndGen
      W hobjects hpaths hgen)

/-- Under an independently established COUNTABLE actual received
image, a countable original physical Type-valued 18D alphabet
is EQUIVALENT to the existence of an exact aleph-null full
noncommutative kernel normal presentation, for EVERY nonempty
genuine AQ word. If the actual image is not known countable,
the equivalence cannot be asserted unconditionally. -/
theorem nativeK5FZPhysical_originalCountable_iff_aleph0NormalRank_of_imageCountable
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool) (hne : word ≠ [])
    (himage : Countable
      (Set.range (nativeC60DVTransportCompleteCode
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W) word))) :
    Countable (NativeC60DSCompleteEighteenCode
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)) ↔
      (∃ R : Set (NativeC60DTFullFree
        (nativeK5AXKuuSignature W) (nativeK5BCFrame W)),
       (nativeC60DVFullWordTransport
          (nativeK5AXKuuSignature W) (nativeK5BCFrame W) word).ker =
        Subgroup.normalClosure R ∧ #R = ℵ₀) := by
  rw [nativeC60FCTransport_eq_freeMap
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W) word]
  exact nativeC60FZSource_countable_iff_exactAleph0NormalRank_of_imageCountable
    (nativeC60DVTransportCompleteCode
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W) word)
    himage (nativeK5FUPhysical_canonicalActiveSource_infinite W word hne)

end ActualPhysicalRawCountabilityGate

#print axioms nativeC60FZRawSeventeenTotal_countable
#print axioms nativeC60FZEighteenObject_countable_of_rawSeventeen
#print axioms nativeC60FZFullOriginalEighteen_countable_of_countable_fibers
#print axioms nativeC60FZFullOriginalEighteen_countable_of_rawAndGen
#print axioms nativeC60FZSource_countable_iff_exactAleph0NormalRank_of_imageCountable
#print axioms nativeC60FZActive_notCountable_of_source_and_image
#print axioms nativeK5FZPhysical_original18_countable_of_rawAndGen
#print axioms nativeK5FZPhysical_fullDV_aleph0NormalRank_of_rawAndGen
#print axioms nativeK5FZPhysical_originalCountable_iff_aleph0NormalRank_of_imageCountable

end
end Kuu.F112.Physical
