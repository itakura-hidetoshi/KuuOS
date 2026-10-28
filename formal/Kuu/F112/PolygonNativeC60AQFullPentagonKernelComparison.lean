import Kuu.F112.PolygonNativeC60AQCrossPentagonKernelDescent

/-!
# F112-P94D3DX — genuine closed-grammar pentagons versus transported original pentagons

DW constructs the least normal subgroup of exactly the transported ORIGINAL
four-path C60 pentagon defects. DX compares it with a DIFFERENT, independent
relation family: every four-path pentagon formed inside the entire ACTUAL
context-closed 17D Type-valued grammar of DV. The target relations are not
defined as the image of the source relations.

* Build two complete dependent 18D target pentagon paths from arbitrary four
  composable CLOSED 17D witnesses, including genuinely contextual witnesses.
* Prove that DV transports both original 18D routes to exactly these target
  typed paths, not merely to scalar or parity shadows.
* Prove inclusion of the source-image pair set into the full target pair set.
  Consequently the transported normal kernel is contained in the full
  closed-presentation normal kernel, without assuming equality.
* Construct the actual quotient comparison and the original-to-full quotient
  descent. Establish a necessary-and-sufficient equality test in terms of
  ALL closed Type-valued four-path pentagon defects.
* A genuine closed pentagon defect outside the image normal closure is an
  explicit obstruction to equality. No existence of such a witness is assumed.

This is an exact comparison of EXPLICIT relative algebraic presentations;
neither a geometric original C60 Type-valued 19D filler nor an unconditional
equality of the two normal kernels is claimed. All DS no-go theorems, original
14D-18D evidence, strict Kuu, independent Kuu as a presentation, 107 public
roots, no-Gray rule, pinned Lean/mathlib and protected PR #1558 remain intact.
No new axioms, sorry or admit.
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

section TrueFullClosedPentagons

variable {L : NativeC60AXLayer.{u}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- The long pentagon is genuinely typed over FOUR ARBITRARY closed
17D paths, not merely images of four original raw17D paths. -/
def nativeC60DXClosedPentagonLong
    {a b c d e : (nativeC60DQSeventeenLayer S F).Total}
    (f : NativeC60AXStep (nativeC60DRClosedSeventeenSignature S F) a b)
    (g : NativeC60AXStep (nativeC60DRClosedSeventeenSignature S F) b c)
    (h : NativeC60AXStep (nativeC60DRClosedSeventeenSignature S F) c d)
    (k : NativeC60AXStep (nativeC60DRClosedSeventeenSignature S F) d e) :
    NativeC60AXStep (nativeC60DVClosedEighteenSignature S F)
      (nativeC60DVPackClosedSeventeen S F
        (.trans (.trans (.trans f g) h) k))
      (nativeC60DVPackClosedSeventeen S F
        (.trans f (.trans g (.trans h k)))) :=
  .trans
    (.trans
      (.atom (.post (.assoc f g h) k))
      (.atom (.assoc f (.trans g h) k)))
    (.atom (.pre f (.assoc g h k)))

/-- Independently constructed SHORT target pentagon route on ALL
closed 17D witnesses. Its exact endpoints agree with the long route. -/
def nativeC60DXClosedPentagonShort
    {a b c d e : (nativeC60DQSeventeenLayer S F).Total}
    (f : NativeC60AXStep (nativeC60DRClosedSeventeenSignature S F) a b)
    (g : NativeC60AXStep (nativeC60DRClosedSeventeenSignature S F) b c)
    (h : NativeC60AXStep (nativeC60DRClosedSeventeenSignature S F) c d)
    (k : NativeC60AXStep (nativeC60DRClosedSeventeenSignature S F) d e) :
    NativeC60AXStep (nativeC60DVClosedEighteenSignature S F)
      (nativeC60DVPackClosedSeventeen S F
        (.trans (.trans (.trans f g) h) k))
      (nativeC60DVPackClosedSeventeen S F
        (.trans f (.trans g (.trans h k)))) :=
  .trans
    (.atom (.assoc (.trans f g) h k))
    (.atom (.assoc f g (.trans h k)))

/-- FULL target pentagon relation set: quantify over ALL four
composable closed 17D Type-valued witnesses, not just original images. -/
def nativeC60DXFullClosedPentagonPairs :
    Set (NativeC60DVClosedFullFree S F ×
      NativeC60DVClosedFullFree S F) :=
  fun pair =>
    ∃ (a b c d e : (nativeC60DQSeventeenLayer S F).Total),
    ∃ (f : NativeC60AXStep (nativeC60DRClosedSeventeenSignature S F) a b)
      (g : NativeC60AXStep (nativeC60DRClosedSeventeenSignature S F) b c)
      (h : NativeC60AXStep (nativeC60DRClosedSeventeenSignature S F) c d)
      (k : NativeC60AXStep (nativeC60DRClosedSeventeenSignature S F) d e),
    pair =
      (nativeC60DVClosedFreeWord S F
        (nativeC60DXClosedPentagonLong S F f g h k),
       nativeC60DVClosedFreeWord S F
        (nativeC60DXClosedPentagonShort S F f g h k))

theorem nativeC60DXFullClosedPentagon_pair_mem
    {a b c d e : (nativeC60DQSeventeenLayer S F).Total}
    (f : NativeC60AXStep (nativeC60DRClosedSeventeenSignature S F) a b)
    (g : NativeC60AXStep (nativeC60DRClosedSeventeenSignature S F) b c)
    (h : NativeC60AXStep (nativeC60DRClosedSeventeenSignature S F) c d)
    (k : NativeC60AXStep (nativeC60DRClosedSeventeenSignature S F) d e) :
    (nativeC60DVClosedFreeWord S F
        (nativeC60DXClosedPentagonLong S F f g h k),
     nativeC60DVClosedFreeWord S F
        (nativeC60DXClosedPentagonShort S F f g h k)) ∈
      nativeC60DXFullClosedPentagonPairs S F :=
  ⟨a, b, c, d, e, f, g, h, k, rfl⟩

/-- The TRUE dependent 18D transport sends EACH original long route to
the long route built from its four transported complete 17D proofs. -/
theorem nativeC60DXTransportPentagonLong
    (word : List Bool)
    {a b c d e : (nativeC60DQSeventeenLayer S F).Total}
    (f : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b)
    (g : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) b c)
    (h : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) c d)
    (k : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) d e) :
    nativeC60DVTransportEighteenStep S F word
        (nativeC60DRPentagonLong S F f g h k) =
      nativeC60DXClosedPentagonLong S F
        (nativeC60DVSeventeenWordMap S F word f)
        (nativeC60DVSeventeenWordMap S F word g)
        (nativeC60DVSeventeenWordMap S F word h)
        (nativeC60DVSeventeenWordMap S F word k) := by
  rfl

theorem nativeC60DXTransportPentagonShort
    (word : List Bool)
    {a b c d e : (nativeC60DQSeventeenLayer S F).Total}
    (f : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b)
    (g : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) b c)
    (h : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) c d)
    (k : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) d e) :
    nativeC60DVTransportEighteenStep S F word
        (nativeC60DRPentagonShort S F f g h k) =
      nativeC60DXClosedPentagonShort S F
        (nativeC60DVSeventeenWordMap S F word f)
        (nativeC60DVSeventeenWordMap S F word g)
        (nativeC60DVSeventeenWordMap S F word h)
        (nativeC60DVSeventeenWordMap S F word k) := by
  rfl

/-- Genuine source-image relations form a SUBFAMILY of ALL target
closed-grammar pentagons; no equality or surjectivity of DV is assumed. -/
theorem nativeC60DXImagePairs_subset_full (word : List Bool) :
    nativeC60DWContextPentagonPairs S F word ⊆
      nativeC60DXFullClosedPentagonPairs S F := by
  intro p hp
  rcases hp with ⟨q, hq, rfl⟩
  rcases hq with ⟨a, b, c, d, e, f, g, h, k, rfl⟩
  refine ⟨_, _, _, _, _,
    nativeC60DVSeventeenWordMap S F word f,
    nativeC60DVSeventeenWordMap S F word g,
    nativeC60DVSeventeenWordMap S F word h,
    nativeC60DVSeventeenWordMap S F word k, ?_⟩
  apply Prod.ext
  · change (nativeC60DVFullWordTransport S F word)
        (nativeC60DSFreeWord S F (nativeC60DRPentagonLong S F f g h k)) =
      nativeC60DVClosedFreeWord S F
        (nativeC60DXClosedPentagonLong S F
          (nativeC60DVSeventeenWordMap S F word f)
          (nativeC60DVSeventeenWordMap S F word g)
          (nativeC60DVSeventeenWordMap S F word h)
          (nativeC60DVSeventeenWordMap S F word k))
    rw [nativeC60DVFullWordTransport_natural S F word
      (nativeC60DRPentagonLong S F f g h k),
      nativeC60DXTransportPentagonLong S F word f g h k]
  · change (nativeC60DVFullWordTransport S F word)
        (nativeC60DSFreeWord S F (nativeC60DRPentagonShort S F f g h k)) =
      nativeC60DVClosedFreeWord S F
        (nativeC60DXClosedPentagonShort S F
          (nativeC60DVSeventeenWordMap S F word f)
          (nativeC60DVSeventeenWordMap S F word g)
          (nativeC60DVSeventeenWordMap S F word h)
          (nativeC60DVSeventeenWordMap S F word k))
    rw [nativeC60DVFullWordTransport_natural S F word
      (nativeC60DRPentagonShort S F f g h k),
      nativeC60DXTransportPentagonShort S F word f g h k]

/-- The full closed pentagon kernel is independently generated by
EVERY closed-grammar typed four-path relation. -/
def nativeC60DXFullClosedPentagonNormalClosure :
    Subgroup (NativeC60DVClosedFullFree S F) :=
  nativeC60DTNormalClosure (nativeC60DXFullClosedPentagonPairs S F)

instance nativeC60DXFullClosedPentagonNormalClosure_normal :
    (nativeC60DXFullClosedPentagonNormalClosure S F).Normal :=
  nativeC60DTNormalClosure_normal (nativeC60DXFullClosedPentagonPairs S F)

abbrev NativeC60DXFullClosedPentagonQuotient :=
  NativeC60DVClosedFullFree S F ⧸
    nativeC60DXFullClosedPentagonNormalClosure S F

theorem nativeC60DXFullClosedPentagon_defect_mem
    {a b c d e : (nativeC60DQSeventeenLayer S F).Total}
    (f : NativeC60AXStep (nativeC60DRClosedSeventeenSignature S F) a b)
    (g : NativeC60AXStep (nativeC60DRClosedSeventeenSignature S F) b c)
    (h : NativeC60AXStep (nativeC60DRClosedSeventeenSignature S F) c d)
    (k : NativeC60AXStep (nativeC60DRClosedSeventeenSignature S F) d e) :
    nativeC60DVClosedFreeWord S F
        (nativeC60DXClosedPentagonLong S F f g h k) *
      (nativeC60DVClosedFreeWord S F
        (nativeC60DXClosedPentagonShort S F f g h k))⁻¹ ∈
      nativeC60DXFullClosedPentagonNormalClosure S F :=
  nativeC60DTPairDefect_mem (nativeC60DXFullClosedPentagonPairs S F)
    _ (nativeC60DXFullClosedPentagon_pair_mem S F f g h k)

/-- MAIN DX INCLUSION: the MINIMAL image-relation normal kernel is
contained in the independently defined ALL-CLOSED-pentagon kernel. -/
theorem nativeC60DXImageKernel_le_full (word : List Bool) :
    nativeC60DWContextPentagonNormalClosure S F word ≤
      nativeC60DXFullClosedPentagonNormalClosure S F := by
  apply (nativeC60DTNormalClosure_le_iff
    (nativeC60DWContextPentagonPairs S F word)
    (nativeC60DXFullClosedPentagonNormalClosure S F)).mpr
  intro p hp
  exact nativeC60DTPairDefect_mem
    (nativeC60DXFullClosedPentagonPairs S F) p
    (nativeC60DXImagePairs_subset_full S F word hp)

/-- Natural quotient map from the transported-original presentation to
the larger ALL-CLOSED-pentagon quotient. Its source is not collapsed
in advance by assuming the two distinct kernels are equal. -/
theorem nativeC60DXImageToFullQuotient_factor (word : List Bool) :
    ∃ induced : NativeC60DWContextPentagonQuotient S F word →*
        NativeC60DXFullClosedPentagonQuotient S F,
      induced.comp (QuotientGroup.mk'
        (nativeC60DWContextPentagonNormalClosure S F word)) =
        QuotientGroup.mk' (nativeC60DXFullClosedPentagonNormalClosure S F) := by
  apply (nativeC60DTQuotient_factor_iff
    (nativeC60DWContextPentagonPairs S F word)
    (QuotientGroup.mk' (nativeC60DXFullClosedPentagonNormalClosure S F))).mpr
  intro p hp
  exact nativeC60DTQuotient_pair_equal
    (nativeC60DXFullClosedPentagonPairs S F) p
    (nativeC60DXImagePairs_subset_full S F word hp)

/-- Complete DV source transport therefore factors even through the
full target quotient, by the actual source pentagons, not by fiat. -/
theorem nativeC60DXSourceToFullQuotient_factor (word : List Bool) :
    ∃ induced : NativeC60DTPentagonQuotient S F →*
        NativeC60DXFullClosedPentagonQuotient S F,
      induced.comp (QuotientGroup.mk'
        (nativeC60DTPentagonNormalClosure S F)) =
        (QuotientGroup.mk'
          (nativeC60DXFullClosedPentagonNormalClosure S F)).comp
            (nativeC60DVFullWordTransport S F word) := by
  apply (nativeC60DTQuotient_factor_iff
    (nativeC60DTPentagonPairs S F)
    ((QuotientGroup.mk' (nativeC60DXFullClosedPentagonNormalClosure S F)).comp
      (nativeC60DVFullWordTransport S F word))).mpr
  intro p hp
  exact nativeC60DTQuotient_pair_equal
    (nativeC60DXFullClosedPentagonPairs S F)
    ((nativeC60DVFullWordTransport S F word p.1),
      (nativeC60DVFullWordTransport S F word p.2))
    (nativeC60DXImagePairs_subset_full S F word
      (nativeC60DWPairImage_mem (nativeC60DTPentagonPairs S F)
        (nativeC60DVFullWordTransport S F word) p hp))

/-- Exact equality criterion. Equality is NOT a premise: it holds IFF
EVERY genuine closed-grammar pentagon defect is already a consequence
of the transported ORIGINAL pentagons. This is the new obstruction. -/
theorem nativeC60DXImageKernel_eq_full_iff (word : List Bool) :
    nativeC60DWContextPentagonNormalClosure S F word =
        nativeC60DXFullClosedPentagonNormalClosure S F ↔
      ∀ {a b c d e : (nativeC60DQSeventeenLayer S F).Total}
        (f : NativeC60AXStep (nativeC60DRClosedSeventeenSignature S F) a b)
        (g : NativeC60AXStep (nativeC60DRClosedSeventeenSignature S F) b c)
        (h : NativeC60AXStep (nativeC60DRClosedSeventeenSignature S F) c d)
        (k : NativeC60AXStep (nativeC60DRClosedSeventeenSignature S F) d e),
        nativeC60DVClosedFreeWord S F
            (nativeC60DXClosedPentagonLong S F f g h k) *
          (nativeC60DVClosedFreeWord S F
            (nativeC60DXClosedPentagonShort S F f g h k))⁻¹ ∈
              nativeC60DWContextPentagonNormalClosure S F word := by
  constructor
  · intro heq a b c d e f g h k
    rw [heq]
    exact nativeC60DXFullClosedPentagon_defect_mem S F f g h k
  · intro hall
    apply le_antisymm (nativeC60DXImageKernel_le_full S F word)
    apply (nativeC60DTNormalClosure_le_iff
      (nativeC60DXFullClosedPentagonPairs S F)
      (nativeC60DWContextPentagonNormalClosure S F word)).mpr
    intro p hp
    rcases hp with ⟨a, b, c, d, e, f, g, h, k, rfl⟩
    exact hall f g h k

/-- A SINGLE actual closed-grammar pentagon defect that is not
generated by original-image pentagons obstructs equality of kernels.
It is a conditional obstruction, not an invented counterexample. -/
theorem nativeC60DXNewClosedPentagon_obstructs_equality
    (word : List Bool)
    {a b c d e : (nativeC60DQSeventeenLayer S F).Total}
    (f : NativeC60AXStep (nativeC60DRClosedSeventeenSignature S F) a b)
    (g : NativeC60AXStep (nativeC60DRClosedSeventeenSignature S F) b c)
    (h : NativeC60AXStep (nativeC60DRClosedSeventeenSignature S F) c d)
    (k : NativeC60AXStep (nativeC60DRClosedSeventeenSignature S F) d e)
    (hbad :
      nativeC60DVClosedFreeWord S F
          (nativeC60DXClosedPentagonLong S F f g h k) *
        (nativeC60DVClosedFreeWord S F
          (nativeC60DXClosedPentagonShort S F f g h k))⁻¹ ∉
            nativeC60DWContextPentagonNormalClosure S F word) :
    nativeC60DWContextPentagonNormalClosure S F word ≠
      nativeC60DXFullClosedPentagonNormalClosure S F := by
  intro heq
  have hmem := nativeC60DXFullClosedPentagon_defect_mem S F f g h k
  rw [← heq] at hmem
  exact hbad hmem

/-- Re-parenthesizing one and the same physical finite AQ tree does not
change the image kernel, nor the independent full target kernel. -/
theorem nativeC60DXActualTreeImageKernel_refinement
    {left right : NativeK5DOContextTree}
    (h : nativeK5DOTreeSteps left = nativeK5DOTreeSteps right) :
    nativeC60DWContextPentagonNormalClosure S F
      (nativeK5DOTreeWord left) =
    nativeC60DWContextPentagonNormalClosure S F
      (nativeK5DOTreeWord right) :=
  nativeC60DWActualTreePentagonKernel_refinement S F h

end TrueFullClosedPentagons

section TruePhysicalC60

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

/-- Specialization to genuine physical C60 AU sources and arbitrary
finite actual AQ context trees, retaining all dependent 18D codes. -/
theorem nativeK5DXPhysicalAQ_imageKernel_le_full
    (W : NativeK5StructuralThirteenCell p U V)
    (tree : NativeK5DOContextTree) :
    let S := nativeK5AXKuuSignature W
    let F := nativeK5BCFrame W
    nativeC60DWContextPentagonNormalClosure S F
        (nativeK5DOTreeWord tree) ≤
      nativeC60DXFullClosedPentagonNormalClosure S F := by
  dsimp only
  exact nativeC60DXImageKernel_le_full
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
    (nativeK5DOTreeWord tree)

end TruePhysicalC60

#print axioms nativeC60DXClosedPentagonLong
#print axioms nativeC60DXClosedPentagonShort
#print axioms nativeC60DXFullClosedPentagonPairs
#print axioms nativeC60DXTransportPentagonLong
#print axioms nativeC60DXTransportPentagonShort
#print axioms nativeC60DXImagePairs_subset_full
#print axioms nativeC60DXFullClosedPentagonNormalClosure
#print axioms nativeC60DXImageKernel_le_full
#print axioms nativeC60DXImageToFullQuotient_factor
#print axioms nativeC60DXSourceToFullQuotient_factor
#print axioms nativeC60DXImageKernel_eq_full_iff
#print axioms nativeC60DXNewClosedPentagon_obstructs_equality
#print axioms nativeK5DXPhysicalAQ_imageKernel_le_full

end
end Kuu.F112.Physical
