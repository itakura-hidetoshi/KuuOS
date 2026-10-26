import Kuu.F112.PolygonNativeC60SharedContextProofEnvelope

/-!
# F112-P94D3BR — exact raw-pair descent and original 14D boundary obstruction

BQ stores a single finite AQ context word with TWO independently typed
raw 16D cells. BR identifies the precise descent that is already
constructible WITHOUT fabricating geometric horizontal composition.

POSITIVE: Quotient the shared-word PRESENTATIONS solely by equality
of BOTH WHOLE DECODED RAW 16D SIGMA BUNDLES, not by observer, Peiffer
charge, or strict categorical equality. The resulting quotient is
equivalent to the PRODUCT of the original raw dependent 16D proof
bundles. The equivalence intertwines every true/false finite context
word with exact Type-valued proof transport. Both original source/target
14D boundaries remain encoded and recoverable.

NEGATIVE: A SINGLE flat original physical C60 15D object cannot, for
ALL pairs, have its original 14D source boundary literally equal to
BOTH independent input source boundaries. The original forward and
backward non-loop exchanges give a concrete typed counterexample.
The necessary-and-sufficient lower-boundary matching condition is
separate from Peiffer, strict quotient, observer, or source-size issues.

QUANTITATIVE: Under either actual physical BG singleton gate the
signed original source-size deficit grows by EXACTLY n*k_side under
n simultaneous AQ frames, strengthening BQ's unbounded-budget result.

No global no-go for every conceivable nondegenerate horizontal
composition is claimed; a different typed output boundary law or
additional genuinely geometric data may evade this particular flat
matching demand. No new axioms, sorry, admit, Gray, or changes to the
107 public roots.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u uD vD uE vE

/-- Decoded pair of independent WHOLE original-dependent raw 16D proofs.
The context prefix is unfolded on both sources and targets, and the
raw comparison term itself; neither input is projected away. -/
def nativeC60BRRawPair {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (z : NativeC60BQSharedProof S F) :
    NativeC60BGRawArrowBundle S F × NativeC60BGRawArrowBundle S F :=
  (nativeC60BQDecodeFirst S F z, nativeC60BQDecodeSecond S F z)

/-- Empty shared frame gives a section from the complete original
raw-proof pair back into the shared-context presentation. -/
theorem nativeC60BRRawPair_pack {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (q r : NativeC60BGRawArrowBundle S F) :
    nativeC60BRRawPair S F (nativeC60BQPack S F q r) = (q, r) := by
  simp only [nativeC60BRRawPair, nativeC60BQDecodeFirst_pack,
    nativeC60BQDecodeSecond_pack]

/-- Original full raw context transport on BOTH proof coordinates. -/
def nativeC60BRRawPairContext {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (word : List Bool)
    (pair : NativeC60BGRawArrowBundle S F × NativeC60BGRawArrowBundle S F) :
    NativeC60BGRawArrowBundle S F × NativeC60BGRawArrowBundle S F :=
  (nativeC60BGRawContext S F word pair.1,
    nativeC60BGRawContext S F word pair.2)

/-- Exact naturality of BOTH entire raw dependent 16D proofs under
any shared finite AQ word. This does not identify raw 16D terms. -/
theorem nativeC60BRRawPair_frame {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (word : List Bool) (z : NativeC60BQSharedProof S F) :
    nativeC60BRRawPair S F (nativeC60BQFrame S F word z) =
      nativeC60BRRawPairContext S F word (nativeC60BRRawPair S F z) :=
  Prod.ext
    (nativeC60BQDecodeFirst_frame S F word z)
    (nativeC60BQDecodeSecond_frame S F word z)

/-- Equality of BOTH COMPLETE DECODED RAW sigma-bundles defines
the representation kernel. This is not observational equivalence. -/
def nativeC60BRRawKernelSetoid {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L) :
    Setoid (NativeC60BQSharedProof S F) where
  r z z' := nativeC60BRRawPair S F z = nativeC60BRRawPair S F z'
  iseqv := ⟨fun _ => rfl,
    fun _ _ h => h.symm, fun _ _ _ h k => h.trans k⟩

/-- Proof-relevant exact raw-pair DESCENT target.
No observational or Peiffer quotient has been inserted. -/
abbrev NativeC60BRRawQuotient {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L) :=
  Quotient (nativeC60BRRawKernelSetoid S F)

/-- The quotient maps to both full raw16D bundles. -/
def nativeC60BRDescend {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L) :
    NativeC60BRRawQuotient S F →
      NativeC60BGRawArrowBundle S F × NativeC60BGRawArrowBundle S F :=
  Quotient.lift (nativeC60BRRawPair S F) (by
    intro z z' h
    exact h)

/-- A product of raw 16D proofs embeds into the quotient as an
empty-prefix shared presentation. -/
def nativeC60BRRise {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (qr : NativeC60BGRawArrowBundle S F × NativeC60BGRawArrowBundle S F) :
    NativeC60BRRawQuotient S F :=
  Quotient.mk (nativeC60BRRawKernelSetoid S F)
    (nativeC60BQPack S F qr.1 qr.2)

theorem nativeC60BRDescend_rise {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (qr : NativeC60BGRawArrowBundle S F × NativeC60BGRawArrowBundle S F) :
    nativeC60BRDescend S F (nativeC60BRRise S F qr) = qr := by
  rcases qr with ⟨q, r⟩
  exact nativeC60BRRawPair_pack S F q r

theorem nativeC60BRRise_descend {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (z : NativeC60BRRawQuotient S F) :
    nativeC60BRRise S F (nativeC60BRDescend S F z) = z := by
  refine Quotient.inductionOn z ?_
  intro q
  apply Quotient.sound
  change nativeC60BRRawPair S F
      (nativeC60BQPack S F
        (nativeC60BRRawPair S F q).1
        (nativeC60BRRawPair S F q).2) =
    nativeC60BRRawPair S F q
  exact nativeC60BRRawPair_pack S F _ _

/-- Complete exact RAW descent: the shared-context presentation modulo
ONLY complete decoded raw equality is equivalent to a full PAIR of
original dependent 16D proofs. Neither higher proof is forgotten. -/
def nativeC60BRRawDescentEquiv {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L) :
    NativeC60BRRawQuotient S F ≃
      (NativeC60BGRawArrowBundle S F × NativeC60BGRawArrowBundle S F) where
  toFun := nativeC60BRDescend S F
  invFun := nativeC60BRRise S F
  left_inv := nativeC60BRRise_descend S F
  right_inv := nativeC60BRDescend_rise S F

/-- Shared AQ framing passes to the exact raw-pair presentation
quotient because the COMPLETE decoded pair is frame-natural. -/
def nativeC60BRQuotientFrame {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (word : List Bool) :
    NativeC60BRRawQuotient S F → NativeC60BRRawQuotient S F :=
  Quotient.lift
    (fun z => Quotient.mk (nativeC60BRRawKernelSetoid S F)
      (nativeC60BQFrame S F word z))
    (by
      intro z z' h
      apply Quotient.sound
      change nativeC60BRRawPair S F (nativeC60BQFrame S F word z) =
        nativeC60BRRawPair S F (nativeC60BQFrame S F word z')
      rw [nativeC60BRRawPair_frame, nativeC60BRRawPair_frame]
      exact congrArg (nativeC60BRRawPairContext S F word) h)

/-- The raw descent equivalence commutes with all finite physical
frame actions (in particular each independent true/false generator). -/
theorem nativeC60BRDescend_frame {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (word : List Bool) (z : NativeC60BRRawQuotient S F) :
    nativeC60BRDescend S F (nativeC60BRQuotientFrame S F word z) =
      nativeC60BRRawPairContext S F word (nativeC60BRDescend S F z) := by
  refine Quotient.inductionOn z ?_
  intro q
  exact nativeC60BRRawPair_frame S F word q

/-- Exact criterion for any SINGLE original lower source 14D boundary
to match BOTH sources of the independent decoded 16D proofs. -/
def NativeC60BRSourceBoundaryCompatible {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (z : NativeC60BQSharedProof S F) : Prop :=
  (nativeC60BQDecodeFirst S F z).1.1.1 =
    (nativeC60BQDecodeSecond S F z).1.1.1

/-- Necessary and sufficient: a single exact-boundary physical
15D witness with both source 14D boundaries exists precisely on the
matching-boundary locus. This is not a horizontal composition. -/
theorem nativeC60BRSourceBoundary_iff_exists {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (z : NativeC60BQSharedProof S F) :
    NativeC60BRSourceBoundaryCompatible S F z ↔
      ∃ out : L.Total,
        out.1 = (nativeC60BQDecodeFirst S F z).1.1.1 ∧
        out.1 = (nativeC60BQDecodeSecond S F z).1.1.1 := by
  constructor
  · intro h
    exact ⟨(nativeC60BQDecodeFirst S F z).1.1, rfl, h⟩
  · rintro ⟨out, hfirst, hsecond⟩
    exact hfirst.symm.trans hsecond

/-- Matching of the FULL original lower boundary pairs is preserved
by each genuine AQ frame, not merely by observed Peiffer charges. -/
theorem nativeC60BRSourceBoundaryCompatible_frame
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (word : List Bool) (z : NativeC60BQSharedProof S F)
    (h : NativeC60BRSourceBoundaryCompatible S F z) :
    NativeC60BRSourceBoundaryCompatible S F
      (nativeC60BQFrame S F word z) := by
  dsimp only [NativeC60BRSourceBoundaryCompatible] at h ⊢
  rw [nativeC60BQDecodeFirst_frame, nativeC60BQDecodeSecond_frame]
  rcases nativeC60BQDecodeFirst S F z with ⟨⟨a, b⟩, cell⟩
  rcases nativeC60BQDecodeSecond S F z with ⟨⟨c, d⟩, cell'⟩
  change a.1 = c.1 at h
  change (nativeC60BCContextTotal F word a).1 =
    (nativeC60BCContextTotal F word c).1
  exact nativeC60BCContextTotal_boundary F word h

section OriginalC60

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

/-- A concrete shared pair of the ACTUAL forward/backward physical
15D exchange, each with its own typed original raw 16D reflexivity. -/
def nativeK5BRIncompatiblePair
    (W : NativeK5StructuralThirteenCell p U V) :
    NativeC60BQSharedProof (nativeK5AXKuuSignature W) (nativeK5BCFrame W) :=
  nativeC60BQPack (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
    (nativeK5BQForwardReflexive W) (nativeK5BQBackwardReflexive W)

/-- Genuine original physical obstruction to literally identifying
both lower source 14D boundaries in ONE original 15D output. -/
theorem nativeK5BRIncompatiblePair_no_flat_source
    (W : NativeK5StructuralThirteenCell p U V) :
    ¬ NativeC60BRSourceBoundaryCompatible
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
      (nativeK5BRIncompatiblePair W) := by
  intro h
  have hraw :
      (nativeK5BQForwardReflexive W).1.1.1 =
        (nativeK5BQBackwardReflexive W).1.1.1 := by
    simpa only [nativeK5BRIncompatiblePair,
      NativeC60BRSourceBoundaryCompatible,
      nativeC60BQDecodeFirst_pack,
      nativeC60BQDecodeSecond_pack] using h
  change (nativeK5BKExchangeForward W []).1 =
    (nativeK5BKExchangeBackward W []).1 at hraw
  exact (nativeK5BKExchange_boundary_ne W []) hraw

/-- There is NO global, literally DOUBLE-source-boundary-preserving
flattening from the shared raw16D pair to a SINGLE original 15D
physical object. No BG assumptions or syntax-size metric are used. -/
theorem nativeK5BRNo_flat_double_source_descent
    (W : NativeK5StructuralThirteenCell p U V) :
    ¬ ∃ flatten :
        NativeC60BQSharedProof
          (nativeK5AXKuuSignature W) (nativeK5BCFrame W) →
            (nativeK5AXBaseLayer W).Total,
      ∀ z,
        (flatten z).1 =
            (nativeC60BQDecodeFirst (nativeK5AXKuuSignature W)
              (nativeK5BCFrame W) z).1.1.1 ∧
        (flatten z).1 =
            (nativeC60BQDecodeSecond (nativeK5AXKuuSignature W)
              (nativeK5BCFrame W) z).1.1.1 := by
  rintro ⟨flatten, hflat⟩
  apply nativeK5BRIncompatiblePair_no_flat_source W
  let z := nativeK5BRIncompatiblePair W
  exact (hflat z).1.symm.trans (hflat z).2

/-- Signed raw 14D source-compression DEFICIT of an arbitrary binary
whiskering candidate, without truncation to natural subtraction. -/
def nativeK5BRSourceDeficit
    (W : NativeK5StructuralThirteenCell p U V)
    (Hh : NativeC60BBWhiskering (nativeK5BCSignature W))
    (x y : (nativeK5AXBaseLayer W).Total) : ℤ :=
  (nativeK5BPSourceSize W x : ℤ) +
      (nativeK5BPSourceSize W y : ℤ) -
        (nativeK5BPSourceSize W (Hh.obj x y) : ℤ)

/-- SHARP SLOPE: if even ONE true physical BG singleton holds, the
signed source-information compression deficit on two parallel AQ
context iterates grows EXACTLY by n*k_side. This is an equality
about ORIGINAL raw14D constructor trees, not merely an asymptotic. -/
theorem nativeK5BRSourceDeficit_iter
    (W : NativeK5StructuralThirteenCell p U V)
    (Hh : NativeC60BBWhiskering (nativeK5BCSignature W))
    (side : Bool)
    (he : NativeC60BGWhiskeringEquivariant
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W) Hh [side])
    (n : Nat) (x y : (nativeK5AXBaseLayer W).Total) :
    nativeK5BRSourceDeficit W Hh
        (nativeK5BPIter W side n x) (nativeK5BPIter W side n y) =
      nativeK5BRSourceDeficit W Hh x y +
        (n * nativeK5BPFrameCost W side : Nat) := by
  have hdiag := nativeK5BPIter_diagonal W Hh side he n x y
  have hsize := congrArg (nativeK5BPSourceSize W) hdiag
  rw [nativeK5BPSourceSize_iter W side n (Hh.obj x y)] at hsize
  dsimp only [nativeK5BRSourceDeficit]
  rw [← hsize, nativeK5BPSourceSize_iter W side n x,
    nativeK5BPSourceSize_iter W side n y]
  omega

end OriginalC60

#print axioms nativeC60BRRawPair
#print axioms nativeC60BRRawPair_pack
#print axioms nativeC60BRRawPairContext
#print axioms nativeC60BRRawPair_frame
#print axioms nativeC60BRRawKernelSetoid
#print axioms NativeC60BRRawQuotient
#print axioms nativeC60BRDescend
#print axioms nativeC60BRRise
#print axioms nativeC60BRDescend_rise
#print axioms nativeC60BRRise_descend
#print axioms nativeC60BRRawDescentEquiv
#print axioms nativeC60BRQuotientFrame
#print axioms nativeC60BRDescend_frame
#print axioms NativeC60BRSourceBoundaryCompatible
#print axioms nativeC60BRSourceBoundary_iff_exists
#print axioms nativeC60BRSourceBoundaryCompatible_frame
#print axioms nativeK5BRIncompatiblePair
#print axioms nativeK5BRIncompatiblePair_no_flat_source
#print axioms nativeK5BRNo_flat_double_source_descent
#print axioms nativeK5BRSourceDeficit
#print axioms nativeK5BRSourceDeficit_iter

end
end Kuu.F112.Physical
