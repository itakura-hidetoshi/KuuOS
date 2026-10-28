import Kuu.F112.PolygonNativeC60EighteenFullWordNineteenObstruction
import Mathlib.GroupTheory.QuotientGroup.Basic
import Mathlib.Algebra.Group.Subgroup.Basic

/-!
# F112-P94D3DT — all-pentagon normal closure and exact receiver descent

DS established the true, globally noncommutative FULL evidence word of
every dependent C60 18D associator/whiskering and proved that the
three-generator long pentagon differs from the two-generator short
pentagon for all composable original 17D Type-valued paths.

DT does not simply proclaim the pentagon closed. It constructs the
MINIMAL normal subgroup of the entire original complete 18D free
group that must be killed if a stated set of 18D path comparisons is
declared. It then forms its actual quotient group and proves a
universal factorization condition. Specifically:

* For ANY group and set of ordered word pairs, the least normal
  subgroup containing the defects x*y⁻¹ is obtained by
  Subgroup.normalClosure of their genuine difference words.
* The quotient identifies each declared pair. A group receiver can
  descend through this quotient if and only if it identifies EACH
  originally specified pair. No unproved faithfulness assumption.
* Apply this to the set of ALL FOUR-PATH physical-source C60
  pentagon pairs, with actual 17D dependent boundaries and entire
  original 18D code alphabet retained in the free group.
* The quotient identifies every genuine 18D pentagon pair, is minimal
  among normal subgroups forcing those identifications, and has
  EXACT kernel its explicitly constructed normal closure.
* The kernel is NONTRIVIAL for any instantiated four-path pentagon:
  DS free-group nonidentity obstructs an information-preserving
  left inverse or receiver on the full original 18D free group.
* Prove the exact necessary and sufficient condition for a receiver
  of ALL original complete 18D generator codes to descend through
  this ALL-PENTAGON quotient. No other preservation is asserted.

This quotient is a NEW, explicitly selected relative PRESENTATION.
Nothing here constructs a geometric original C60 19D Type-valued
filler; DS already proves the impossibility of a full-evidence-
preserving 19D filler. DT describes the precisely minimal algebraic
normal-kernel price of adding the family of pentagon equalities.

Preserve strict Kuu as the primary kernel, independent Kuu as one
presentation, all original 14D/15D/16D/17D/18D raw certificates,
physical C60 gauge rather than an incidence graph, all earlier no-go
theorems and 107 published roots. No new axioms, sorry, admit, Gray
or hidden quotient identification.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u v w uD vD uE vE

section UniversalNormalClosure

variable {G : Type u} [Group G]

/-- Each explicitly selected pair contributes its ORIGINAL ordered
noncommutative defect x*y⁻¹, not a scalar measure of the two words. -/
def nativeC60DTPairDefects (R : Set (G × G)) : Set G :=
  Set.image (fun p : G × G => p.1 * p.2⁻¹) R

/-- Smallest NORMAL subgroup containing all explicitly chosen
noncommutative difference words. The closure adds only CONSEQUENCES
of the declared pairs, not arbitrary equal-observer identifications. -/
def nativeC60DTNormalClosure (R : Set (G × G)) : Subgroup G :=
  Subgroup.normalClosure (nativeC60DTPairDefects R)

instance nativeC60DTNormalClosure_normal (R : Set (G × G)) :
    (nativeC60DTNormalClosure R).Normal := by
  change (Subgroup.normalClosure (nativeC60DTPairDefects R)).Normal
  infer_instance

/-- Every actual declared pair has its COMPLETE difference word in
the normal closure. -/
theorem nativeC60DTPairDefect_mem
    (R : Set (G × G)) (p : G × G) (hp : p ∈ R) :
    p.1 * p.2⁻¹ ∈ nativeC60DTNormalClosure R :=
  Subgroup.subset_normalClosure ⟨p, hp, rfl⟩

/-- TRUE minimality: no smaller NORMAL subgroup can impose all
declared pair relations. This also characterizes the family of ALL
normal subgroups in which the specified words can become equal. -/
theorem nativeC60DTNormalClosure_le_iff
    (R : Set (G × G)) (H : Subgroup G) [H.Normal] :
    nativeC60DTNormalClosure R ≤ H ↔
      ∀ p : G × G, p ∈ R → p.1 * p.2⁻¹ ∈ H := by
  constructor
  · intro h p hp
    exact h (nativeC60DTPairDefect_mem R p hp)
  · intro h
    apply Subgroup.normalClosure_le_normal
    rintro x ⟨p, hp, rfl⟩
    exact h p hp

/-- The smallest normal kernel is included in an arbitrary receiver
kernel EXACTLY when that receiver equates all stated pairs. -/
theorem nativeC60DTNormalClosure_ker_iff
    (R : Set (G × G)) {H : Type v} [Group H]
    (ρ : G →* H) :
    nativeC60DTNormalClosure R ≤ ρ.ker ↔
      ∀ p : G × G, p ∈ R → ρ p.1 = ρ p.2 := by
  rw [nativeC60DTNormalClosure_le_iff R ρ.ker]
  constructor
  · intro h p hp
    have hh : ρ (p.1 * p.2⁻¹) = 1 :=
      MonoidHom.mem_ker.mp (h p hp)
    rw [map_mul, map_inv] at hh
    exact eq_of_mul_inv_eq_one hh
  · intro h p hp
    apply MonoidHom.mem_ker.mpr
    rw [map_mul, map_inv, h p hp, mul_inv_cancel]

/-- The original group G is quotiented ONLY by the stated smallest
normal closure; no arbitrary global completion is silently added. -/
abbrev NativeC60DTQuotient (R : Set (G × G)) :=
  G ⧸ nativeC60DTNormalClosure R

/-- Each declared pair really is equal IN THE constructed quotient,
with correct left-to-right noncommutative difference order. -/
theorem nativeC60DTQuotient_pair_equal
    (R : Set (G × G)) (p : G × G) (hp : p ∈ R) :
    (QuotientGroup.mk' (nativeC60DTNormalClosure R)) p.1 =
      (QuotientGroup.mk' (nativeC60DTNormalClosure R)) p.2 := by
  apply (QuotientGroup.eq_iff_div_mem).mpr
  rw [div_eq_mul_inv]
  exact nativeC60DTPairDefect_mem R p hp

/-- This is the EXACT kernel of the quotient map; it says what
information is forced to collapse, without asserting injectivity on
all other complete evidence words. -/
theorem nativeC60DTQuotient_kernel
    (R : Set (G × G)) :
    (QuotientGroup.mk' (nativeC60DTNormalClosure R)).ker =
      nativeC60DTNormalClosure R :=
  QuotientGroup.ker_mk' (nativeC60DTNormalClosure R)

/-- UNIVERSAL PROPERTY. A group-valued receiver of the unmodified
full evidence descends through the *minimal* declared-relation
quotient iff it equates precisely the selected 18D word pairs.
No Peiffer parity or scalar observer mediates the implication. -/
theorem nativeC60DTQuotient_factor_iff
    (R : Set (G × G)) {H : Type v} [Group H] (ρ : G →* H) :
    (∃ induced : NativeC60DTQuotient R →* H,
      induced.comp (QuotientGroup.mk' (nativeC60DTNormalClosure R)) = ρ) ↔
      ∀ p : G × G, p ∈ R → ρ p.1 = ρ p.2 := by
  constructor
  · rintro ⟨induced, hcomp⟩ p hp
    have hq := nativeC60DTQuotient_pair_equal R p hp
    calc
      ρ p.1 = induced ((QuotientGroup.mk' (nativeC60DTNormalClosure R)) p.1) :=
        (DFunLike.congr_fun hcomp p.1).symm
      _ = induced ((QuotientGroup.mk' (nativeC60DTNormalClosure R)) p.2) :=
        congrArg induced hq
      _ = ρ p.2 := DFunLike.congr_fun hcomp p.2
  · intro hall
    have hk : nativeC60DTNormalClosure R ≤ ρ.ker :=
      (nativeC60DTNormalClosure_ker_iff R ρ).mpr hall
    exact ⟨QuotientGroup.lift (nativeC60DTNormalClosure R) ρ hk,
      QuotientGroup.lift_comp_mk' (nativeC60DTNormalClosure R) ρ hk⟩

end UniversalNormalClosure

section ActualC60Pentagons

variable {L : NativeC60AXLayer.{u}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- Entire ORIGINAL 18D evidence group with dependent Type-valued
17D source/target and full 18D generator provenance, never replaced by
a count or a freely selected new generator alphabet. -/
abbrev NativeC60DTFullFree :=
  FreeGroup (NativeC60DSCompleteEighteenCode S F)

/-- ALL and ONLY actual four-composable-17D pentagon pairs, each
indexed by its original dependent 16D/17D endpoint data. The raw18D
words themselves are retained by the previous DS free receiver. -/
def nativeC60DTPentagonPairs :
    Set (NativeC60DTFullFree S F × NativeC60DTFullFree S F) :=
  fun pair =>
    ∃ (a b c d e : (nativeC60DQSeventeenLayer S F).Total),
    ∃ (f : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b)
      (g : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) b c)
      (h : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) c d)
      (k : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) d e),
    pair =
      (nativeC60DSFreeWord S F (nativeC60DRPentagonLong S F f g h k),
       nativeC60DSFreeWord S F (nativeC60DRPentagonShort S F f g h k))

/-- Every genuinely typed original 17D four-input datum contributes
exactly its independently proved long/short 18D pentagon pair. -/
theorem nativeC60DTPentagon_pair_mem
    {a b c d e : (nativeC60DQSeventeenLayer S F).Total}
    (f : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b)
    (g : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) b c)
    (h : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) c d)
    (k : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) d e) :
    (nativeC60DSFreeWord S F (nativeC60DRPentagonLong S F f g h k),
     nativeC60DSFreeWord S F (nativeC60DRPentagonShort S F f g h k)) ∈
      nativeC60DTPentagonPairs S F :=
  ⟨a, b, c, d, e, f, g, h, k, rfl⟩

/-- Actual minimum normal kernel of ALL physical-source C60 18D
pentagon equations simultaneously, as a subgroup of the COMPLETE
original noncommutative 18D free evidence. -/
def nativeC60DTPentagonNormalClosure : Subgroup (NativeC60DTFullFree S F) :=
  nativeC60DTNormalClosure (nativeC60DTPentagonPairs S F)

/-- Explicit normality at the C60-specific typeclass target, avoiding
Lean's bounded reducibility search through two independent definitions.
The proof is inherited from the universal minimal normal closure,
not added as an axiom or separate geometric relation. -/
instance nativeC60DTPentagonNormalClosure_normal :
    (nativeC60DTPentagonNormalClosure S F).Normal :=
  nativeC60DTNormalClosure_normal (nativeC60DTPentagonPairs S F)

/-- The full pentagon-normal-closure quotient is explicitly a newly
chosen relative Kuu group presentation. It is NOT a declaration of
genuine original geometric C60 19D fillers. -/
abbrev NativeC60DTPentagonQuotient :=
  NativeC60DTFullFree S F ⧸ nativeC60DTPentagonNormalClosure S F

/-- Each true 18D pentagon difference belongs to the all-pentagon
minimal normal subgroup with exact noncommutative word order. -/
theorem nativeC60DTPentagon_defect_mem
    {a b c d e : (nativeC60DQSeventeenLayer S F).Total}
    (f : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b)
    (g : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) b c)
    (h : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) c d)
    (k : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) d e) :
    nativeC60DSFreeWord S F (nativeC60DRPentagonLong S F f g h k) *
        (nativeC60DSFreeWord S F
          (nativeC60DRPentagonShort S F f g h k))⁻¹ ∈
      nativeC60DTPentagonNormalClosure S F :=
  nativeC60DTPairDefect_mem (nativeC60DTPentagonPairs S F) _
    (nativeC60DTPentagon_pair_mem S F f g h k)

/-- CONSTRUCTIVE POSITIVE QUOTIENT: all independently constructed
four-input pentagon routes become equal after quotienting by exactly
the minimum normally closed all-pentagon relation set. -/
theorem nativeC60DTPentagon_quotient_equal
    {a b c d e : (nativeC60DQSeventeenLayer S F).Total}
    (f : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b)
    (g : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) b c)
    (h : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) c d)
    (k : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) d e) :
    (QuotientGroup.mk' (nativeC60DTPentagonNormalClosure S F))
        (nativeC60DSFreeWord S F (nativeC60DRPentagonLong S F f g h k)) =
      (QuotientGroup.mk' (nativeC60DTPentagonNormalClosure S F))
        (nativeC60DSFreeWord S F
          (nativeC60DRPentagonShort S F f g h k)) :=
  nativeC60DTQuotient_pair_equal (nativeC60DTPentagonPairs S F) _
    (nativeC60DTPentagon_pair_mem S F f g h k)

/-- EXACT MINIMALITY over ALL genuine four-path pentagons. Every
normal subgroup making all true 18D path pairs equal must contain
this single canonical normal closure, no less and no extra axioms. -/
theorem nativeC60DTPentagonNormalClosure_minimal
    (H : Subgroup (NativeC60DTFullFree S F)) [H.Normal]
    (h : ∀ {a b c d e : (nativeC60DQSeventeenLayer S F).Total}
      (f : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b)
      (g : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) b c)
      (i : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) c d)
      (k : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) d e),
      nativeC60DSFreeWord S F (nativeC60DRPentagonLong S F f g i k) *
        (nativeC60DSFreeWord S F
          (nativeC60DRPentagonShort S F f g i k))⁻¹ ∈ H) :
    nativeC60DTPentagonNormalClosure S F ≤ H := by
  apply (nativeC60DTNormalClosure_le_iff
    (nativeC60DTPentagonPairs S F) H).mpr
  intro pair hp
  rcases hp with ⟨a, b, c, d, e, f, g, i, k, rfl⟩
  exact h f g i k

/-- The new quotient map has EXACTLY the normally closed
pentagon-defect kernel: the whole original free evidence survives
up to precisely that explicit normal closure, with no asserted
faithfulness elsewhere. -/
theorem nativeC60DTPentagon_kernel_exact :
    (QuotientGroup.mk' (nativeC60DTPentagonNormalClosure S F)).ker =
      nativeC60DTPentagonNormalClosure S F :=
  nativeC60DTQuotient_kernel (nativeC60DTPentagonPairs S F)

/-- The all-pentagon kernel is provably NONTRIVIAL as soon as one
actual dependent 17D four-input pentagon is provided. The original
full 18D free receiver cannot factor as an unchanged full-evidence
retraction through the quotient. -/
theorem nativeC60DTPentagonNormalClosure_nontrivial
    {a b c d e : (nativeC60DQSeventeenLayer S F).Total}
    (f : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b)
    (g : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) b c)
    (h : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) c d)
    (k : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) d e) :
    nativeC60DTPentagonNormalClosure S F ≠ ⊥ := by
  intro hbot
  have hmem : nativeC60DSFreeWord S F
      (nativeC60DRPentagonLong S F f g h k) *
        (nativeC60DSFreeWord S F
          (nativeC60DRPentagonShort S F f g h k))⁻¹ ∈
      (⊥ : Subgroup (NativeC60DTFullFree S F)) := by
    rw [← hbot]
    exact nativeC60DTPentagon_defect_mem S F f g h k
  have hone : nativeC60DSFreeWord S F
      (nativeC60DRPentagonLong S F f g h k) *
        (nativeC60DSFreeWord S F
          (nativeC60DRPentagonShort S F f g h k))⁻¹ = 1 := by
    simpa using hmem
  exact nativeC60DSPentagon_free_ne S F f g h k
    (eq_of_mul_inv_eq_one hone)

/-- Full-information identity receiver CANNOT factor through
the new all-pentagon quotient, because DS proves all original
pentagon free words were different. This records genuine evidence
loss instead of pretending the quotient remains faithful. -/
theorem nativeC60DTPentagon_no_full_evidence_section
    {a b c d e : (nativeC60DQSeventeenLayer S F).Total}
    (f : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b)
    (g : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) b c)
    (h : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) c d)
    (k : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) d e) :
    ¬ ∃ retraction : NativeC60DTPentagonQuotient S F →*
          NativeC60DTFullFree S F,
        retraction.comp
          (QuotientGroup.mk' (nativeC60DTPentagonNormalClosure S F)) =
          MonoidHom.id (NativeC60DTFullFree S F) := by
  rintro ⟨retraction, hcomp⟩
  have hall := (nativeC60DTQuotient_factor_iff
    (nativeC60DTPentagonPairs S F)
    (MonoidHom.id (NativeC60DTFullFree S F))).mp ⟨retraction, hcomp⟩
  have hwords := hall _
    (nativeC60DTPentagon_pair_mem S F f g h k)
  have heq : nativeC60DSFreeWord S F
      (nativeC60DRPentagonLong S F f g h k) =
        nativeC60DSFreeWord S F
          (nativeC60DRPentagonShort S F f g h k) := by
    simpa using hwords
  exact (nativeC60DSPentagon_free_ne S F f g h k) heq

/-- ALL-PENTAGON DESCENT CRITERION. For ANY concrete group receiver
of every original signed 18D generator code, a unique compatible
relative group transport is available (by quotient surjectivity)
exactly when ALL true 17D-dependent pentagon pairs are identified.
This does not assert an original geometric 19D comparison. -/
theorem nativeC60DTPentagon_receiver_factor_iff
    {H : Type v} [Group H]
    (ρ : NativeC60DTFullFree S F →* H) :
    (∃ induced : NativeC60DTPentagonQuotient S F →* H,
      induced.comp
        (QuotientGroup.mk' (nativeC60DTPentagonNormalClosure S F)) = ρ) ↔
      ∀ {a b c d e : (nativeC60DQSeventeenLayer S F).Total}
        (f : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b)
        (g : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) b c)
        (i : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) c d)
        (k : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) d e),
        ρ (nativeC60DSFreeWord S F (nativeC60DRPentagonLong S F f g i k)) =
          ρ (nativeC60DSFreeWord S F
            (nativeC60DRPentagonShort S F f g i k)) := by
  refine (nativeC60DTQuotient_factor_iff
    (nativeC60DTPentagonPairs S F) ρ).trans ?_
  constructor
  · intro hall a b c d e f g i k
    exact hall _ (nativeC60DTPentagon_pair_mem S F f g i k)
  · intro hall pair hp
    rcases hp with ⟨a, b, c, d, e, f, g, i, k, rfl⟩
    exact hall f g i k

/-- The all-pentagon normal closure contains each SINGLE-pentagon
normal closure, making explicit that simultaneous coherence entails
at least the one-relator cost for every original dependent context. -/
theorem nativeC60DTSinglePentagon_le_all
    {a b c d e : (nativeC60DQSeventeenLayer S F).Total}
    (f : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b)
    (g : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) b c)
    (h : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) c d)
    (k : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) d e) :
    Subgroup.normalClosure
      {nativeC60DSFreeWord S F (nativeC60DRPentagonLong S F f g h k) *
        (nativeC60DSFreeWord S F
          (nativeC60DRPentagonShort S F f g h k))⁻¹} ≤
      nativeC60DTPentagonNormalClosure S F := by
  apply Subgroup.normalClosure_le_normal
  intro x hx
  rw [Set.mem_singleton_iff] at hx
  subst x
  exact nativeC60DTPentagon_defect_mem S F f g h k

end ActualC60Pentagons

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

/-- This is genuinely the ORIGINAL physical C60 AU 15D naturality
source, with an arbitrary finite physical AQ context tree.
Its true 17D triangle roundtrip realizes a four-input pentagon
whose complete DS free word becomes equal to its short route in
the MINIMAL explicit all-pentagon quotient. -/
theorem nativeK5DTPhysicalPentagon_quotient_equal
    (W : NativeK5StructuralThirteenCell p U V)
    (tree : NativeK5DOContextTree) :
    let S := nativeK5AXKuuSignature W
    let F := nativeK5BCFrame W
    let gen := nativeC60BCShiftGen S F (nativeK5DOTreeWord tree)
      (nativeK5CEPhysicalAUGenerator W)
    let route := nativeC60DQSeventeenRoundtrip S F gen
    (QuotientGroup.mk' (nativeC60DTPentagonNormalClosure S F))
        (nativeC60DSFreeWord S F
          (nativeC60DRPentagonLong S F route route route route)) =
      (QuotientGroup.mk' (nativeC60DTPentagonNormalClosure S F))
        (nativeC60DSFreeWord S F
          (nativeC60DRPentagonShort S F route route route route)) := by
  dsimp only
  exact nativeC60DTPentagon_quotient_equal
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W) _ _ _ _

/-- Even for a physically named C60 AU higher pentagon, the
selected normal kernel cannot be trivial. Thus the new quotient
IS a genuine presentation change, not an unnoticed original
geometric 19D cell or an equivalent full-evidence presentation. -/
theorem nativeK5DTPhysicalPentagon_normalClosure_nontrivial
    (W : NativeK5StructuralThirteenCell p U V)
    (tree : NativeK5DOContextTree) :
    nativeC60DTPentagonNormalClosure
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W) ≠ ⊥ := by
  let gen := nativeC60BCShiftGen
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
    (nativeK5DOTreeWord tree) (nativeK5CEPhysicalAUGenerator W)
  let route := nativeC60DQSeventeenRoundtrip
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W) gen
  exact nativeC60DTPentagonNormalClosure_nontrivial
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
    route route route route

end PhysicalC60

#print axioms nativeC60DTPairDefects
#print axioms nativeC60DTNormalClosure
#print axioms nativeC60DTPairDefect_mem
#print axioms nativeC60DTNormalClosure_le_iff
#print axioms nativeC60DTNormalClosure_ker_iff
#print axioms NativeC60DTQuotient
#print axioms nativeC60DTQuotient_pair_equal
#print axioms nativeC60DTQuotient_kernel
#print axioms nativeC60DTQuotient_factor_iff
#print axioms NativeC60DTFullFree
#print axioms nativeC60DTPentagonPairs
#print axioms nativeC60DTPentagon_pair_mem
#print axioms nativeC60DTPentagonNormalClosure
#print axioms NativeC60DTPentagonQuotient
#print axioms nativeC60DTPentagon_defect_mem
#print axioms nativeC60DTPentagon_quotient_equal
#print axioms nativeC60DTPentagonNormalClosure_minimal
#print axioms nativeC60DTPentagon_kernel_exact
#print axioms nativeC60DTPentagonNormalClosure_nontrivial
#print axioms nativeC60DTPentagon_no_full_evidence_section
#print axioms nativeC60DTPentagon_receiver_factor_iff
#print axioms nativeC60DTSinglePentagon_le_all
#print axioms nativeK5DTPhysicalPentagon_quotient_equal
#print axioms nativeK5DTPhysicalPentagon_normalClosure_nontrivial

end
end Kuu.F112.Physical
