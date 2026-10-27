import Kuu.F112.PolygonNativeC60FiniteAQPartialGaugeNaturality

/-!
# F112-P94D3DE — strict BF covariance and genuinely typed inner-sector parity

DD supplies a canonical CN-coordinate group isomorphism across arbitrary
additional OUTER finite AQ contexts at one fixed original 15D inner boundary.
DE makes its relationship with the ORIGINAL BF strict functor explicit:
the full BW holonomy of every actual transported strict arrow is exactly
the noncommutative BV prefix of the original holonomy. Because CD proved
faithfulness on ALL genuine selected strict Hom sets, the full value has
a unique original strict-arrow realization.

For genuinely DIFFERENT inner AQ words, CU exhibits the exact original
15D Type-valued source and target after prefixing, while the original
CH positive sixteen-dimensional generator stores the same 15D proof
payload. At a single common ORIGINAL conservative lower 14D fiber R,
the countably many CZ higher certificates are present in EVERY finite
inner and outer context, and their entire noncommutative FreeGroup Nat
family has the SAME parity readout. This is a genuine common typed
subgroup comparison, not an automatic comparison of all strict loops.

An independently provided whole-group transport respects this entire
typed CZ sector exactly when its values on the original CZ generators
agree. Parity is then preserved on the whole typed sector. Unconditional
whole-group transport between arbitrary different inner words is NOT
asserted. DD's kernel criterion remains the exact obstruction.

Outer strict transport has actual unit/composition laws; therefore
the proven partial parity squares form a coherent finite-word action.
No new geometric 16-cell, no quotient of raw 15D evidence, Gray,
sorry, admit, axioms, or changes to existing public roots.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uDE uD vD uE vE

section FullStrictBFHomCovariance

variable {L : NativeC60AXLayer.{uDE}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- BF's ACTUAL full-arrow strict functor, when followed by the
original BW noncommutative word, is precisely finite-prefix insertion.
This is proved for EVERY strict arrow using BA's typed 16D
representability, not only for specially chosen physical generators. -/
theorem nativeC60DEFullStrictBF_BW
    (prefix : List Bool) {a b : L.Total}
    (f : (nativeC60AZStrictProject
          (nativeC60BCClosedSignature S F)
          (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))).obj ⟨a⟩ ⟶
        (nativeC60AZStrictProject
          (nativeC60BCClosedSignature S F)
          (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))).obj ⟨b⟩) :
    MulOpposite.unop
        ((nativeC60BWFreeStrictHolonomy S F).map
          ((nativeC60BDNoRelations_strictFunctor S F prefix).map f)) =
      nativeC60BWFreePrefix S prefix
        (MulOpposite.unop ((nativeC60BWFreeStrictHolonomy S F).map f)) := by
  obtain ⟨c, rfl⟩ := nativeC60BAStep_surjective
    (nativeC60BCClosedSignature S F)
    (nativeC60AZNoRelations (nativeC60BCClosedSignature S F)) a b f
  rw [nativeC60BDStrictContext_step,
    nativeC60BXFreeStrictHolonomy_step,
    nativeC60BXFreeStrictHolonomy_step,
    nativeC60BWFreeHolonomy_frame]
  rfl

/-- The full BF map is faithful on EVERY genuine strict Hom set:
no nontrivial typed 16D comparison can become equal merely by
adding a finite AQ context in the selected no-extra-relations Kuu. -/
theorem nativeC60DEFullStrictBF_faithful
    (prefix : List Bool) {a b : L.Total}
    (f g : (nativeC60AZStrictProject
          (nativeC60BCClosedSignature S F)
          (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))).obj ⟨a⟩ ⟶
        (nativeC60AZStrictProject
          (nativeC60BCClosedSignature S F)
          (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))).obj ⟨b⟩) :
    (nativeC60BDNoRelations_strictFunctor S F prefix).map f =
        (nativeC60BDNoRelations_strictFunctor S F prefix).map g ↔
      f = g := by
  constructor
  · intro heq
    apply nativeC60CDStrictFreeFaithful S F
    apply (nativeC60BWFreePrefix_injective S prefix)
    have hh := congrArg
      (fun k => MulOpposite.unop ((nativeC60BWFreeStrictHolonomy S F).map k))
      heq
    simpa only [nativeC60DEFullStrictBF_BW] using hh
  · intro heq
    rw [heq]

end FullStrictBFHomCovariance

section PhysicalStrictOuterCoherence

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

/-- The original CY exact CN reconstruction shows that an EMPTY
outer AQ context acts as identity on EVERY actual strict loop. -/
theorem nativeK5DEOuterStrictTransport_nil
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer : List Bool)
    (z : nativeK5DBIsotropy W R inner outer) :
    nativeK5DDOuterStrictTransport W R inner outer [] z = z := by
  change nativeC60COEmbed (nativeK5AXKuuSignature W)
      (nativeK5BCFrame W) outer (nativeK5CKAtomGenerator W R inner)
      (nativeC60CORetraction (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W) outer
        (nativeK5CKAtomGenerator W R inner) z) = z
  exact nativeK5CYPhysicalEvery_strict_loop_CN W R inner outer z

/-- True composition for arbitrary finite outer AQ contexts on ALL
conservative strict automorphisms, keeping the correct concatenation
order and every original 15D dependent proof certificate. -/
theorem nativeK5DEOuterStrictTransport_comp
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer more extra : List Bool)
    (z : nativeK5DBIsotropy W R inner outer) :
    nativeK5DDOuterStrictTransport W R inner (more ++ outer) extra
        (nativeK5DDOuterStrictTransport W R inner outer more z) =
      nativeK5DDOuterStrictTransport W R inner outer (extra ++ more) z := by
  change nativeC60COEmbed (nativeK5AXKuuSignature W)
      (nativeK5BCFrame W) (extra ++ (more ++ outer))
      (nativeK5CKAtomGenerator W R inner)
      (nativeC60CORetraction (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W) (more ++ outer)
        (nativeK5CKAtomGenerator W R inner)
        (nativeC60COEmbed (nativeK5AXKuuSignature W)
          (nativeK5BCFrame W) (more ++ outer)
          (nativeK5CKAtomGenerator W R inner)
          (nativeC60CORetraction (nativeK5AXKuuSignature W)
            (nativeK5BCFrame W) outer
            (nativeK5CKAtomGenerator W R inner) z))) =
    nativeC60COEmbed (nativeK5AXKuuSignature W)
      (nativeK5BCFrame W) ((extra ++ more) ++ outer)
      (nativeK5CKAtomGenerator W R inner)
      (nativeC60CORetraction (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W) outer
        (nativeK5CKAtomGenerator W R inner) z)
  rw [nativeC60CORetraction_embed, List.append_assoc]

/-- Coherent unit as an exact equality of actual strict group maps. -/
theorem nativeK5DEOuterStrictTransport_nil_hom
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer : List Bool) :
    nativeK5DDOuterStrictTransport W R inner outer [] =
      MonoidHom.id (nativeK5DBIsotropy W R inner outer) := by
  apply MonoidHom.ext
  intro z
  exact nativeK5DEOuterStrictTransport_nil W R inner outer z

/-- Coherent finite-word composition of actual group maps, not merely
commuting scalar readouts. -/
theorem nativeK5DEOuterStrictTransport_comp_hom
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer more extra : List Bool) :
    (nativeK5DDOuterStrictTransport W R inner (more ++ outer) extra).comp
        (nativeK5DDOuterStrictTransport W R inner outer more) =
      nativeK5DDOuterStrictTransport W R inner outer (extra ++ more) := by
  apply MonoidHom.ext
  intro z
  exact nativeK5DEOuterStrictTransport_comp W R inner outer more extra z

/-- The original Type-valued source 15D certificate has exactly
its original CU context, not merely an equal Peiffer readout. -/
theorem nativeK5DEInnerSource_prefix
    (W : NativeK5StructuralThirteenCell p U V)
    (inner prefix : List Bool)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S) :
    nativeK5CHSource W (prefix ++ inner) cell =
      nativeK5BCContext W prefix (nativeK5CHSource W inner cell) :=
  (nativeK5CUPhysical_source_frame_append W inner prefix cell).symm

/-- Independently preserve the genuine target-first 15D history. -/
theorem nativeK5DEInnerTarget_prefix
    (W : NativeK5StructuralThirteenCell p U V)
    (inner prefix : List Bool)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S) :
    nativeK5CHTarget W (prefix ++ inner) cell =
      nativeK5BCContext W prefix (nativeK5CHTarget W inner cell) :=
  (nativeK5CUPhysical_target_frame_append W inner prefix cell).symm

/-- The TRUE original positive BC sixteen-dimensional generator
retains its entire ORIGINAL primitive 15D proof witness under inner
prefixing. It is NOT a newly asserted 16-cell comparison. -/
theorem nativeK5DEOriginalPositiveCode_prefix
    (W : NativeK5StructuralThirteenCell p U V)
    (inner prefix : List Bool)
    {R S : NativeK5FifteenFourteenFiber W}
    (cell : NativeK5AQFifteenCell W R S) :
    nativeC60BVGeneratorCode (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W)
        (nativeK5CHPositiveGenerator W (prefix ++ inner) cell) =
      nativeC60BWCodePrefix (nativeK5AXKuuSignature W) prefix
        (nativeC60BVGeneratorCode (nativeK5AXKuuSignature W)
          (nativeK5BCFrame W) (nativeK5CHPositiveGenerator W inner cell)) := by
  rfl

/-- The original conservative n-times symm witness remains n even
after an arbitrary genuine inner AQ prefix. This is equality of
original 16D certificate indices, not geometrical 16-cell filling. -/
theorem nativeK5DEOriginalCZIndex_inner_prefix
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner prefix : List Bool) (n : Nat) :
    nativeK5CZCodeIndex W
      (nativeC60BVGeneratorCode (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W)
        (nativeK5CZGenerator W R (prefix ++ inner) n)) =
      nativeK5CZCodeIndex W
        (nativeC60BVGeneratorCode (nativeK5AXKuuSignature W)
          (nativeK5BCFrame W) (nativeK5CZGenerator W R inner n)) := by
  rw [nativeK5CZCodeIndex_generator, nativeK5CZCodeIndex_generator]

/-- Shared original 15D Type-valued CZ conservative cores induce
the SAME NONCOMMUTATIVE two-letter partial group invariant for every
finite inner and outer AQ context. -/
def nativeK5DEOriginalTypedNatParity : FreeGroup Nat →* FreeGroup Bool :=
  FreeGroup.map (fun n : Nat => decide (n % 2 = 1))

theorem nativeK5DEOriginalTypedNatParity_sector
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer : List Bool) :
    (nativeK5DCParityQuotient W R inner outer).comp
        (nativeK5CZFreeNatEmbed W R inner outer) =
      nativeK5DEOriginalTypedNatParity := by
  apply FreeGroup.ext_hom
  intro n
  change nativeK5DCParityQuotient W R inner outer
    (nativeK5CZFreeNatEmbed W R inner outer (FreeGroup.of n)) =
      (FreeGroup.map (fun n : Nat => decide (n % 2 = 1))) (FreeGroup.of n)
  rw [nativeK5DCParityQuotient_CZ, FreeGroup.map.of]

/-- MAIN DE inner-context theorem. TWO INDEPENDENT inner and outer
finite AQ words have a canonically comparable, ORIGINAL Type-valued
conservative CZ sector. The entire signed free group on Nat is
faithfully embedded in each genuine strict group (CZ), and the
partial parity quotient agrees on all original words. This does NOT
claim a whole-isotropy map between unrelated inner proof boundaries. -/
theorem nativeK5DETwoInnerTypedCZ_parity
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer inner' outer' : List Bool) :
    (nativeK5DCParityQuotient W R inner outer).comp
        (nativeK5CZFreeNatEmbed W R inner outer) =
      (nativeK5DCParityQuotient W R inner' outer').comp
        (nativeK5CZFreeNatEmbed W R inner' outer') := by
  calc
    _ = nativeK5DEOriginalTypedNatParity :=
      nativeK5DEOriginalTypedNatParity_sector W R inner outer
    _ = _ := (nativeK5DEOriginalTypedNatParity_sector W R inner' outer').symm

/-- Full-word version includes arbitrary noncommutative signed
original CZ compositions, not only individual n-generators. -/
theorem nativeK5DETwoInnerTypedCZ_parity_word
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer inner' outer' : List Bool)
    (z : FreeGroup Nat) :
    nativeK5DCParityQuotient W R inner outer
        (nativeK5CZFreeNatEmbed W R inner outer z) =
      nativeK5DCParityQuotient W R inner' outer'
        (nativeK5CZFreeNatEmbed W R inner' outer' z) :=
  DFunLike.congr_fun
    (nativeK5DETwoInnerTypedCZ_parity W R inner outer inner' outer') z

/-- A proposed genuine strict transport between two different
inner contexts preserves the EXACT original CZ Type-valued sector
iff it matches each original n proof-bearing generator. -/
def NativeK5DEOriginalCZTransportCompatible
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer inner' outer' : List Bool)
    (transport : nativeK5DBIsotropy W R inner outer →*
        nativeK5DBIsotropy W R inner' outer') : Prop :=
  transport.comp (nativeK5CZFreeNatEmbed W R inner outer) =
    nativeK5CZFreeNatEmbed W R inner' outer'

theorem nativeK5DEOriginalCZTransport_iff_generators
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer inner' outer' : List Bool)
    (transport : nativeK5DBIsotropy W R inner outer →*
        nativeK5DBIsotropy W R inner' outer') :
    NativeK5DEOriginalCZTransportCompatible W R
        inner outer inner' outer' transport ↔
      ∀ n : Nat,
        transport (nativeK5CZFreeNatEmbed W R inner outer (FreeGroup.of n)) =
          nativeK5CZFreeNatEmbed W R inner' outer' (FreeGroup.of n) := by
  constructor
  · intro h n
    exact DFunLike.congr_fun h (FreeGroup.of n)
  · intro h
    apply FreeGroup.ext_hom
    intro n
    exact h n

/-- When independently supplied actual strict transport has kept
EVERY original proof-bearing CZ generator, the original partial gauge
quotient necessarily commutes on the entire native free subgroup.
No equality on the WHOLE strict isotropy group is silently inferred. -/
theorem nativeK5DEOriginalCZTransport_parity
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer inner' outer' : List Bool)
    (transport : nativeK5DBIsotropy W R inner outer →*
        nativeK5DBIsotropy W R inner' outer')
    (h : NativeK5DEOriginalCZTransportCompatible W R
        inner outer inner' outer' transport) :
    ((nativeK5DCParityQuotient W R inner' outer').comp transport).comp
        (nativeK5CZFreeNatEmbed W R inner outer) =
      (nativeK5DCParityQuotient W R inner outer).comp
        (nativeK5CZFreeNatEmbed W R inner outer) := by
  apply FreeGroup.ext_hom
  intro n
  change nativeK5DCParityQuotient W R inner' outer'
      (transport (nativeK5CZFreeNatEmbed W R inner outer (FreeGroup.of n))) =
    nativeK5DCParityQuotient W R inner outer
      (nativeK5CZFreeNatEmbed W R inner outer (FreeGroup.of n))
  rw [(nativeK5DEOriginalCZTransport_iff_generators W R
    inner outer inner' outer' transport).mp h n]
  exact (nativeK5DETwoInnerTypedCZ_parity_word
    W R inner outer inner' outer' (FreeGroup.of n)).symm

end PhysicalStrictOuterCoherence

#print axioms nativeC60DEFullStrictBF_BW
#print axioms nativeC60DEFullStrictBF_faithful
#print axioms nativeK5DEOuterStrictTransport_nil
#print axioms nativeK5DEOuterStrictTransport_comp
#print axioms nativeK5DEOuterStrictTransport_nil_hom
#print axioms nativeK5DEOuterStrictTransport_comp_hom
#print axioms nativeK5DEInnerSource_prefix
#print axioms nativeK5DEInnerTarget_prefix
#print axioms nativeK5DEOriginalPositiveCode_prefix
#print axioms nativeK5DEOriginalCZIndex_inner_prefix
#print axioms nativeK5DEOriginalTypedNatParity
#print axioms nativeK5DEOriginalTypedNatParity_sector
#print axioms nativeK5DETwoInnerTypedCZ_parity
#print axioms nativeK5DETwoInnerTypedCZ_parity_word
#print axioms NativeK5DEOriginalCZTransportCompatible
#print axioms nativeK5DEOriginalCZTransport_iff_generators
#print axioms nativeK5DEOriginalCZTransport_parity

end
end Kuu.F112.Physical
