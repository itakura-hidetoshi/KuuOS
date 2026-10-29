import Kuu.F112.PolygonNativeC60AQFullPentagonCompleteKernelNormalClosure

/-!
# F112-P94D3FP — complete 18D collision quotient = ACTUAL transport image

FO proved that the whole kernel of FreeGroup.map f is the normal closure
of ALL original source-code collision differences, including empty,
constant and non-surjective cases. Apply the pinned mathlib first
isomorphism theorem to this EXACT normal quotient, not to a scalar
shadow or a fabricated surjective target.

Any group-valued receiver that respects all original code collisions
has a UNIQUE group-homomorphism factor on the ACTUAL image of transport.
Its extension to the entire target free group is not generally unique:
unused target letters have unconstrained values. An explicit empty-source
regression gives two different target maps with identical source pullback.
Surjectivity restores whole-target uniqueness.

Specialize to the existing fully dependent Type-valued 18D DV transport,
with the distinct old FJ physical nonfaithful and FK/FL/FM faithful
presentations retained. No 19D filler, finite/minimal normal generators,
Gray, global strict n-category or hyperdescent. All prior root imports,
historical no-go and original evidence stay intact. Append-only.
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

/-- First isomorphism theorem for the EXACT FO collision normal closure,
not merely for an abstractly renamed kernel. The subgroup equality
makes the quotient types equivalent, then Noether I identifies the range. -/
noncomputable def nativeC60FPFreeMapFirstIso
    {A : Type u} {B : Type v} (f : A → B) :
    NativeC60FOFiberQuotient f ≃* (FreeGroup.map f).range :=
  (QuotientGroup.quotientMulEquivOfEq
    (nativeC60FOFreeMap_ker_eq_normalClosure f).symm).trans
      (QuotientGroup.quotientKerEquivRange (FreeGroup.map f))

/-- On every original signed free word the canonical quotient-range
isomorphism is precisely the original map restricted to its image. -/
@[simp] theorem nativeC60FPFreeMapFirstIso_mk
    {A : Type u} {B : Type v} (f : A → B) (z : FreeGroup A) :
    nativeC60FPFreeMapFirstIso f
        (QuotientGroup.mk' (nativeC60FOFiberNormalClosure f) z) =
      (FreeGroup.map f).rangeRestrict z := by
  apply Subtype.ext
  rfl

/-- A fiber-compatible receiver admits a UNIQUE factor on the actual
image subgroup. In particular this does not claim the entire free-group
target extension chosen in FO is unique on letters outside the image. -/
theorem nativeC60FPFreeMap_receiver_image_unique_iff
    {A : Type u} {B : Type v} {G : Type w} [Group G]
    (f : A → B) (receiver : FreeGroup A →* G) :
    (∃! induced : (FreeGroup.map f).range →* G,
      induced.comp (FreeGroup.map f).rangeRestrict = receiver) ↔
      ∀ a b : A, f a = f b →
        receiver (FreeGroup.of a) = receiver (FreeGroup.of b) := by
  classical
  constructor
  · rintro ⟨induced, hinduced, _⟩ a b hab
    have ha := DFunLike.congr_fun hinduced (FreeGroup.of a)
    have hb := DFunLike.congr_fun hinduced (FreeGroup.of b)
    change induced ((FreeGroup.map f).rangeRestrict (FreeGroup.of a)) =
      receiver (FreeGroup.of a) at ha
    change induced ((FreeGroup.map f).rangeRestrict (FreeGroup.of b)) =
      receiver (FreeGroup.of b) at hb
    have hsame :
        (FreeGroup.map f).rangeRestrict (FreeGroup.of a) =
          (FreeGroup.map f).rangeRestrict (FreeGroup.of b) := by
      apply Subtype.ext
      change FreeGroup.of (f a) = FreeGroup.of (f b)
      exact congrArg FreeGroup.of hab
    exact ha.symm.trans ((congrArg induced hsame).trans hb)
  · intro compatible
    obtain ⟨target, htarget⟩ :=
      (nativeC60FOFreeMap_factor_iff f receiver).mpr compatible
    let induced : (FreeGroup.map f).range →* G :=
      target.comp (Subgroup.subtype (FreeGroup.map f).range)
    have hdesc : induced.comp (FreeGroup.map f).rangeRestrict = receiver := by
      apply MonoidHom.ext
      intro z
      change target ((FreeGroup.map f) z) = receiver z
      exact DFunLike.congr_fun htarget z
    refine ⟨induced, hdesc, ?_⟩
    intro alternative halternative
    apply MonoidHom.ext
    rintro ⟨b, hb⟩
    obtain ⟨a, ha⟩ := hb
    have hx : (FreeGroup.map f).rangeRestrict a =
        (⟨b, ⟨a, ha⟩⟩ : (FreeGroup.map f).range) :=
      Subtype.ext ha
    calc
      alternative ⟨b, ⟨a, ha⟩⟩ =
          alternative ((FreeGroup.map f).rangeRestrict a) :=
        congrArg alternative hx.symm
      _ = receiver a := DFunLike.congr_fun halternative a
      _ = induced ((FreeGroup.map f).rangeRestrict a) :=
        (DFunLike.congr_fun hdesc a).symm
      _ = induced ⟨b, ⟨a, ha⟩⟩ := congrArg induced hx

/-- If the original letter map is surjective, the entire target is
the image; target extensions agreeing on source must then coincide. -/
theorem nativeC60FPWholeTarget_unique_of_surjective
    {A : Type u} {B : Type v} {G : Type w} [Group G]
    (f : A → B) (hf : Function.Surjective f)
    (t u : FreeGroup B →* G)
    (h : t.comp (FreeGroup.map f) = u.comp (FreeGroup.map f)) :
    t = u := by
  apply FreeGroup.ext_hom
  intro b
  obtain ⟨a, rfl⟩ := hf b
  have hh := DFunLike.congr_fun h (FreeGroup.of a)
  simpa only [MonoidHom.comp_apply, FreeGroup.map.of] using hh

/-- Regression: a non-surjective letter map can have distinct whole-target
extensions while their source restrictions are identical. This is WHY
FP's canonical receiver factor lives on the image, not all target letters. -/
theorem nativeC60FPWholeTarget_extension_not_unique_example :
    ∃ t u : FreeGroup Bool →* Multiplicative ℤ,
      t ≠ u ∧
        t.comp (FreeGroup.map (fun e : Empty => (Empty.elim e : Bool))) =
          u.comp (FreeGroup.map (fun e : Empty => (Empty.elim e : Bool))) := by
  let t : FreeGroup Bool →* Multiplicative ℤ :=
    FreeGroup.lift (fun _ : Bool => (1 : Multiplicative ℤ))
  let u : FreeGroup Bool →* Multiplicative ℤ :=
    FreeGroup.lift (fun _ : Bool => Multiplicative.ofAdd (1 : ℤ))
  refine ⟨t, u, ?_, ?_⟩
  · intro heq
    have hh := DFunLike.congr_fun heq (FreeGroup.of true)
    have hbad : (1 : Multiplicative ℤ) =
        Multiplicative.ofAdd (1 : ℤ) := by
      simpa only [t, u, FreeGroup.lift_apply_of] using hh
    have hzero : (0 : ℤ) = 1 := congrArg Multiplicative.toAdd hbad
    norm_num at hzero
  · apply FreeGroup.ext_hom
    intro e
    exact Empty.elim e

/-- Once a full-target extension exists for an arbitrary group homomorphism,
its restriction to the *actual image* is automatically the unique factor.
The definition never changes the image subtype along a hom equality. -/
theorem nativeC60FPHom_image_unique_of_extension
    {X : Type u} {Y : Type v} {G : Type w}
    [Group X] [Group Y] [Group G]
    (φ : X →* Y) (receiver : X →* G)
    (target : Y →* G) (htarget : target.comp φ = receiver) :
    ∃! induced : φ.range →* G,
      induced.comp φ.rangeRestrict = receiver := by
  let induced : φ.range →* G :=
    target.comp (Subgroup.subtype φ.range)
  have hdesc : induced.comp φ.rangeRestrict = receiver := by
    apply MonoidHom.ext
    intro z
    change target (φ z) = receiver z
    exact DFunLike.congr_fun htarget z
  refine ⟨induced, hdesc, ?_⟩
  intro alternative halternative
  apply MonoidHom.ext
  rintro ⟨b, hb⟩
  obtain ⟨a, ha⟩ := hb
  have hx : φ.rangeRestrict a = (⟨b, ⟨a, ha⟩⟩ : φ.range) :=
    Subtype.ext ha
  calc
    alternative ⟨b, ⟨a, ha⟩⟩ =
        alternative (φ.rangeRestrict a) := congrArg alternative hx.symm
    _ = receiver a := DFunLike.congr_fun halternative a
    _ = induced (φ.rangeRestrict a) :=
      (DFunLike.congr_fun hdesc a).symm
    _ = induced ⟨b, ⟨a, ha⟩⟩ := congrArg induced hx

section FullDependentEighteenCode

variable {L : NativeC60AXLayer.{u}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- The ACTUAL 18D fully dependent full signed-word transport image,
not a freely chosen copy of the whole context-closed target. -/
abbrev NativeC60FPFullImage (word : List Bool) :=
  (nativeC60DVFullWordTransport S F word).range

/-- Noether I for the genuine complete DV Type-valued 18D code:
the FO full collision normal quotient IS canonically the actual image. -/
noncomputable def nativeC60FPFullTransportFirstIso (word : List Bool) :
    (NativeC60DTFullFree S F ⧸
      nativeC60FOFullKernelNormalClosure S F word) ≃*
        NativeC60FPFullImage S F word :=
  (QuotientGroup.quotientMulEquivOfEq
    (nativeC60FOFullTransport_kernel_eq_normalClosure S F word).symm).trans
      (QuotientGroup.quotientKerEquivRange
        (nativeC60DVFullWordTransport S F word))

/-- Representative-level commuting diagram for the original 18D
dependent word, with no abelianization or erased Type-valued witness. -/
@[simp] theorem nativeC60FPFullTransportFirstIso_mk
    (word : List Bool) (z : NativeC60DTFullFree S F) :
    nativeC60FPFullTransportFirstIso S F word
      (QuotientGroup.mk' (nativeC60FOFullKernelNormalClosure S F word) z) =
        (nativeC60DVFullWordTransport S F word).rangeRestrict z := by
  apply Subtype.ext
  rfl

/-- Exact existence AND uniqueness of a group receiver on the genuine
18D transport image, iff it respects ALL original full-code collisions.
No equality of unused whole-target letters is inferred. -/
theorem nativeC60FPFullReceiver_image_unique_iff
    {G : Type v} [Group G]
    (word : List Bool) (receiver : NativeC60DTFullFree S F →* G) :
    (∃! induced : NativeC60FPFullImage S F word →* G,
      induced.comp (nativeC60DVFullWordTransport S F word).rangeRestrict =
        receiver) ↔
      ∀ a b : NativeC60DSCompleteEighteenCode S F,
        nativeC60DVTransportCompleteCode S F word a =
          nativeC60DVTransportCompleteCode S F word b →
        receiver (FreeGroup.of a) = receiver (FreeGroup.of b) := by
  constructor
  · rintro ⟨induced, hinduced, _⟩ a b hab
    have ha := DFunLike.congr_fun hinduced (FreeGroup.of a)
    have hb := DFunLike.congr_fun hinduced (FreeGroup.of b)
    change induced ((nativeC60DVFullWordTransport S F word).rangeRestrict
      (FreeGroup.of a)) = receiver (FreeGroup.of a) at ha
    change induced ((nativeC60DVFullWordTransport S F word).rangeRestrict
      (FreeGroup.of b)) = receiver (FreeGroup.of b) at hb
    have hsame :
        (nativeC60DVFullWordTransport S F word).rangeRestrict
            (FreeGroup.of a) =
          (nativeC60DVFullWordTransport S F word).rangeRestrict
            (FreeGroup.of b) := by
      apply Subtype.ext
      simpa only [nativeC60FCTransport_eq_freeMap S F word,
        FreeGroup.map.of] using congrArg FreeGroup.of hab
    exact ha.symm.trans ((congrArg induced hsame).trans hb)
  · intro compatible
    obtain ⟨target, htarget⟩ :=
      (nativeC60FOReceiver_descends_iff_code_fibers
        S F word receiver).mpr compatible
    exact nativeC60FPHom_image_unique_of_extension
      (nativeC60DVFullWordTransport S F word) receiver target htarget

end FullDependentEighteenCode

section OriginalAndAlternativePhysicalKernels

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

/-- The existing original FJ FULL kernel stays nontrivial in every
nonempty genuine context, including after construction of FP's quotient
image equivalence. Not replaced by the separate FK presentation. -/
theorem nativeK5FPOriginalFullTransport_kernel_ne_bot
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool) (hne : word ≠ []) :
    (nativeC60DVFullWordTransport
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W) word).ker ≠ ⊥ := by
  rw [nativeC60FOFullTransport_kernel_eq_normalClosure]
  exact nativeK5FOOldFullKernel_ne_bot W word hne

/-- The independently selected FK/FL/FM full alternative stays faithful
at every finite context; its first isomorphism has zero kernel, unlike FJ. -/
theorem nativeK5FPAlternativeFullTransport_kernel_eq_bot
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool) :
    (nativeC60DVFullWordTransport
      (nativeK5AXKuuSignature W) (nativeK5FKBCFrame W) word).ker = ⊥ := by
  rw [nativeC60FOFullTransport_kernel_eq_normalClosure]
  exact nativeK5FOAlternativeFullKernel_eq_bot W word

end OriginalAndAlternativePhysicalKernels

-- Generic regression: empty letters and nonsurjective successors retain
-- precisely the same first-isomorphism statement, without extra hypotheses.
example :
    NativeC60FOFiberQuotient
      (fun e : Empty => (Empty.elim e : Bool)) ≃*
        (FreeGroup.map (fun e : Empty => (Empty.elim e : Bool))).range :=
  nativeC60FPFreeMapFirstIso _

example :
    NativeC60FOFiberQuotient (fun n : Nat => n + 1) ≃*
      (FreeGroup.map (fun n : Nat => n + 1)).range :=
  nativeC60FPFreeMapFirstIso _

#print axioms nativeC60FPFreeMapFirstIso
#print axioms nativeC60FPFreeMapFirstIso_mk
#print axioms nativeC60FPFreeMap_receiver_image_unique_iff
#print axioms nativeC60FPWholeTarget_unique_of_surjective
#print axioms nativeC60FPWholeTarget_extension_not_unique_example
#print axioms nativeC60FPFullTransportFirstIso
#print axioms nativeC60FPFullTransportFirstIso_mk
#print axioms nativeC60FPHom_image_unique_of_extension
#print axioms nativeC60FPFullReceiver_image_unique_iff
#print axioms nativeK5FPOriginalFullTransport_kernel_ne_bot
#print axioms nativeK5FPAlternativeFullTransport_kernel_eq_bot

end
end Kuu.F112.Physical
