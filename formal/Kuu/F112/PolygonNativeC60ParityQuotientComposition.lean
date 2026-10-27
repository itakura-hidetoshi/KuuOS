import Kuu.F112.PolygonNativeC60StrictParityQuotientTransport

/-!
# F112-P94D3DK — finite AQ strict-parity quotient composition

DJ constructs the genuine kernel quotient of original strict C60 isotropy,
and identifies it through the original surjective DC map with the
noncommutative two-generator free group. DK establishes canonical
identity and COMPOSITION on these actual strict kernel quotients,
including arbitrary noncommuting finite AQ inner context words.

For any three genuine strict groups and their original surjective
observables to the SAME FreeGroup Bool, the induced quotient
comparisons are canonical and compose strictly, whether or not the
corresponding full unquotiented group equivalences compose. We prove
that every DJ genuine strict transport induces this canonical map.
Thus the composite of two physical inner-prefix transports is the
canonical strict quotient transport to the exactly ordered final
context `more ++ (shift ++ inner)`.

A separate genuine whole-strict noncommutative parity theorem tracks
each of the original DF isomorphisms without claiming their composites
are equal as strict automorphisms. Difference between any three
independently supplied parity-natural strict transports is proved
to lie in the original target DC kernel; this is the precise
remaining obstruction to lifting quotient coherence to raw strict
coherence. No such kernel element is assumed to be the identity.

Associativity of list prefixes is used in the correct, ordered
direction. No commutativity of AQ prefixes, no geometric new 16-cell,
no Gray, no axioms, sorry or admit. Retain original Type-valued
14D/15D boundaries, 16D witnesses and finite C60 gauge contexts.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uDK vDK wDK zDK uD vD uE vE

section AbstractExactQuotientCoherence

variable {G : Type uDK} {H : Type vDK} {K : Type wDK} {Q : Type zDK}
variable [Group G] [Group H] [Group K] [Group Q]

/-- The canonical genuine strict-kernel quotient transport through
the common ORIGINAL surjective group-valued observable. The kernel
is taken in the actual G/H groups, not a newly asserted 16D relation. -/
def nativeC60DKCanonicalQuotientEquiv
    (q : G →* Q) (r : H →* Q)
    (hq : Function.Surjective q) (hr : Function.Surjective r) :
    (G ⧸ q.ker) ≃* (H ⧸ r.ker) :=
  (QuotientGroup.quotientKerEquivOfSurjective q hq).trans
    (QuotientGroup.quotientKerEquivOfSurjective r hr).symm

/-- The group identity survives in the canonical strict quotient:
no additional context-specific choice is required. -/
theorem nativeC60DKCanonical_refl
    (q : G →* Q) (hq : Function.Surjective q) :
    nativeC60DKCanonicalQuotientEquiv q q hq hq =
      MulEquiv.refl (G ⧸ q.ker) := by
  apply MulEquiv.ext
  intro x
  change (QuotientGroup.quotientKerEquivOfSurjective q hq).symm
      ((QuotientGroup.quotientKerEquivOfSurjective q hq) x) = x
  simp

/-- True group-valued composition of arbitrary original strict
kernel quotients, with no symmetry imposed on the context order. -/
theorem nativeC60DKCanonical_comp
    (q : G →* Q) (r : H →* Q) (t : K →* Q)
    (hq : Function.Surjective q)
    (hr : Function.Surjective r)
    (ht : Function.Surjective t) :
    (nativeC60DKCanonicalQuotientEquiv q r hq hr).trans
      (nativeC60DKCanonicalQuotientEquiv r t hr ht) =
        nativeC60DKCanonicalQuotientEquiv q t hq ht := by
  apply MulEquiv.ext
  intro x
  change (QuotientGroup.quotientKerEquivOfSurjective t ht).symm
      ((QuotientGroup.quotientKerEquivOfSurjective r hr)
        ((QuotientGroup.quotientKerEquivOfSurjective r hr).symm
          ((QuotientGroup.quotientKerEquivOfSurjective q hq) x))) =
    (QuotientGroup.quotientKerEquivOfSurjective t ht).symm
      ((QuotientGroup.quotientKerEquivOfSurjective q hq) x)
  simp

/-- DJ's quotient transport from an ACTUAL strict group equivalence
is exactly the canonical quotient map. This upgrades the first
isomorphism theorem's commuting square to an equality of MulEquivs. -/
theorem nativeC60DKDJTransport_eq_canonical
    (q : G →* Q) (r : H →* Q)
    (e : G ≃* H) (h : r.comp e.toMonoidHom = q)
    (hq : Function.Surjective q) (hr : Function.Surjective r) :
    nativeC60DJQuotientTransport q r e h =
      nativeC60DKCanonicalQuotientEquiv q r hq hr := by
  apply MulEquiv.ext
  intro x
  apply (QuotientGroup.quotientKerEquivOfSurjective r hr).injective
  have hn := DFunLike.congr_fun
    (nativeC60DJQuotientParity_equiv q r e h hq hr) x
  change (QuotientGroup.quotientKerEquivOfSurjective r hr)
      (nativeC60DJQuotientTransport q r e h x) =
    (QuotientGroup.quotientKerEquivOfSurjective q hq) x at hn
  calc
    (QuotientGroup.quotientKerEquivOfSurjective r hr)
        (nativeC60DJQuotientTransport q r e h x) =
      (QuotientGroup.quotientKerEquivOfSurjective q hq) x := hn
    _ = (QuotientGroup.quotientKerEquivOfSurjective r hr)
        (nativeC60DKCanonicalQuotientEquiv q r hq hr x) := by
      change _ = (QuotientGroup.quotientKerEquivOfSurjective r hr)
        ((QuotientGroup.quotientKerEquivOfSurjective r hr).symm
          ((QuotientGroup.quotientKerEquivOfSurjective q hq) x))
      simp

/-- Even if the three independent whole-strict equivalences have not
been identified, their ACTUAL induced strict kernel-quotient maps
compose without an obstruction. This uses no hypothesis e₂₀=e₂₁∘e₁₀. -/
theorem nativeC60DKDJTransport_comp
    (q : G →* Q) (r : H →* Q) (t : K →* Q)
    (hq : Function.Surjective q)
    (hr : Function.Surjective r)
    (ht : Function.Surjective t)
    (e : G ≃* H) (f : H ≃* K) (g : G ≃* K)
    (he : r.comp e.toMonoidHom = q)
    (hf : t.comp f.toMonoidHom = r)
    (hg : t.comp g.toMonoidHom = q) :
    (nativeC60DJQuotientTransport q r e he).trans
        (nativeC60DJQuotientTransport r t f hf) =
      nativeC60DJQuotientTransport q t g hg := by
  rw [nativeC60DKDJTransport_eq_canonical q r e he hq hr,
    nativeC60DKDJTransport_eq_canonical r t f hf hr ht,
    nativeC60DKDJTransport_eq_canonical q t g hg hq ht]
  exact nativeC60DKCanonical_comp q r t hq hr ht

/-- Precise remaining strict-lift obstruction: any failure to
identify two compatible routes of genuine strict isomorphisms
is necessarily contained in the ORIGINAL target DC kernel.
No assertion that this element equals the identity. -/
theorem nativeC60DKStrict_comp_defect_kernel
    (q : G →* Q) (r : H →* Q) (t : K →* Q)
    (e : G ≃* H) (f : H ≃* K) (g : G ≃* K)
    (he : r.comp e.toMonoidHom = q)
    (hf : t.comp f.toMonoidHom = r)
    (hg : t.comp g.toMonoidHom = q)
    (x : G) :
    f (e x) * (g x)⁻¹ ∈ t.ker := by
  apply (MonoidHom.mem_ker).mpr
  rw [map_mul, map_inv]
  have h1 := DFunLike.congr_fun he x
  have h2 := DFunLike.congr_fun hf (e x)
  have h3 := DFunLike.congr_fun hg x
  change r (e x) = q x at h1
  change t (f (e x)) = r (e x) at h2
  change t (g x) = q x at h3
  rw [h2, h1, h3]
  exact mul_inv_cancel _

end AbstractExactQuotientCoherence

section OriginalPhysicalC60

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

/-- Canonical quotient transport between any two physical ORIGINAL
finite AQ inner context histories, without claiming an actual strict
lift between independent arbitrary inner contexts. -/
def nativeK5DKCanonicalParityTransport
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer targetInner : List Bool) :
    (nativeK5DBIsotropy W R inner outer ⧸
      (nativeK5DCParityQuotient W R inner outer).ker) ≃*
    (nativeK5DBIsotropy W R targetInner outer ⧸
      (nativeK5DCParityQuotient W R targetInner outer).ker) :=
  nativeC60DKCanonicalQuotientEquiv
    (nativeK5DCParityQuotient W R inner outer)
    (nativeK5DCParityQuotient W R targetInner outer)
    (nativeK5DCParityQuotient_surjective W R inner outer)
    (nativeK5DCParityQuotient_surjective W R targetInner outer)

/-- Physical exact unit, at ALL genuine original finite C60 contexts. -/
theorem nativeK5DKCanonical_refl
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer : List Bool) :
    nativeK5DKCanonicalParityTransport W R inner outer inner =
      MulEquiv.refl _ :=
  nativeC60DKCanonical_refl
    (nativeK5DCParityQuotient W R inner outer)
    (nativeK5DCParityQuotient_surjective W R inner outer)

/-- Full strict-QUOTIENT composition on three arbitrary original
finite inner AQ histories; composition has precisely the given
order and does NOT commute the inner words. -/
theorem nativeK5DKCanonical_comp
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner middle target outer : List Bool) :
    (nativeK5DKCanonicalParityTransport W R inner outer middle).trans
        (nativeK5DKCanonicalParityTransport W R middle outer target) =
      nativeK5DKCanonicalParityTransport W R inner outer target :=
  nativeC60DKCanonical_comp
    (nativeK5DCParityQuotient W R inner outer)
    (nativeK5DCParityQuotient W R middle outer)
    (nativeK5DCParityQuotient W R target outer)
    (nativeK5DCParityQuotient_surjective W R inner outer)
    (nativeK5DCParityQuotient_surjective W R middle outer)
    (nativeK5DCParityQuotient_surjective W R target outer)

/-- The canonical map IS the true DJ quotient of the actual DF
whole-strict inner-prefix group equivalence, not an independent
substitute for the genuine Type-valued physical strict transport. -/
theorem nativeK5DKDJInnerPrefix_eq_canonical
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer shift : List Bool) :
    nativeK5DJInnerPrefix_quotientEquiv W R inner outer shift =
      nativeK5DKCanonicalParityTransport W R inner outer (shift ++ inner) :=
  nativeC60DKDJTransport_eq_canonical
    (nativeK5DCParityQuotient W R inner outer)
    (nativeK5DCParityQuotient W R (shift ++ inner) outer)
    (nativeK5DFInnerPrefixStrictEquiv W R inner outer shift)
    (nativeK5DIInnerPrefix_full_parity W R inner outer shift)
    (nativeK5DCParityQuotient_surjective W R inner outer)
    (nativeK5DCParityQuotient_surjective W R (shift ++ inner) outer)

/-- MAIN DK: apply shift first and more second, with NONCOMMUTATIVE
order more ++ shift and target bracketing more ++ (shift ++ inner).
The composite of two genuine DJ strict-quotient transports is the
canonical strict quotient transport to the final original context.
There is NO assumption that DF's whole raw strict maps compose. -/
theorem nativeK5DKInnerPrefix_quotient_comp
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer shift more : List Bool) :
    (nativeK5DJInnerPrefix_quotientEquiv W R inner outer shift).trans
        (nativeK5DJInnerPrefix_quotientEquiv W R
          (shift ++ inner) outer more) =
      nativeK5DKCanonicalParityTransport W R inner outer
        (more ++ (shift ++ inner)) := by
  rw [nativeK5DKDJInnerPrefix_eq_canonical W R inner outer shift,
    nativeK5DKDJInnerPrefix_eq_canonical W R (shift ++ inner) outer more]
  exact nativeK5DKCanonical_comp W R inner
    (shift ++ inner) (more ++ (shift ++ inner)) outer

/-- The actual whole-strict two-stage transfer retains the original
DC parity. We prove this DIRECTLY from the DI *genuine* strict
naturality theorems, preserving all 14D/15D and 16D source evidence. -/
theorem nativeK5DKInnerPrefix_strict_twostep_parity
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer shift more : List Bool)
    (z : nativeK5DBIsotropy W R inner outer) :
    nativeK5DCParityQuotient W R (more ++ (shift ++ inner)) outer
        (nativeK5DFInnerPrefixStrictEquiv W R (shift ++ inner) outer more
          (nativeK5DFInnerPrefixStrictEquiv W R inner outer shift z)) =
      nativeK5DCParityQuotient W R inner outer z := by
  have h1 := DFunLike.congr_fun
    (nativeK5DIInnerPrefix_full_parity W R inner outer shift) z
  have h2 := DFunLike.congr_fun
    (nativeK5DIInnerPrefix_full_parity W R (shift ++ inner) outer more)
      (nativeK5DFInnerPrefixStrictEquiv W R inner outer shift z)
  change nativeK5DCParityQuotient W R (shift ++ inner) outer
      (nativeK5DFInnerPrefixStrictEquiv W R inner outer shift z) =
        nativeK5DCParityQuotient W R inner outer z at h1
  change nativeK5DCParityQuotient W R (more ++ (shift ++ inner)) outer
      (nativeK5DFInnerPrefixStrictEquiv W R (shift ++ inner) outer more
        (nativeK5DFInnerPrefixStrictEquiv W R inner outer shift z)) =
    nativeK5DCParityQuotient W R (shift ++ inner) outer
      (nativeK5DFInnerPrefixStrictEquiv W R inner outer shift z) at h2
  exact h2.trans h1

/-- Two actual strict transfer routes have IDENTICAL original parity
after correctly ordered prefix reassociation. This does NOT assert
that their underlying strict Type-valued automorphisms are equal. -/
theorem nativeK5DKInnerPrefix_twostep_total_parity
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer shift more : List Bool)
    (z : nativeK5DBIsotropy W R inner outer) :
    nativeK5DCParityQuotient W R (more ++ (shift ++ inner)) outer
        (nativeK5DFInnerPrefixStrictEquiv W R (shift ++ inner) outer more
          (nativeK5DFInnerPrefixStrictEquiv W R inner outer shift z)) =
      nativeK5DCParityQuotient W R ((more ++ shift) ++ inner) outer
        (nativeK5DFInnerPrefixStrictEquiv W R inner outer (more ++ shift) z) := by
  calc
    _ = nativeK5DCParityQuotient W R inner outer z :=
      nativeK5DKInnerPrefix_strict_twostep_parity W R inner outer shift more z
    _ = _ := (DFunLike.congr_fun
      (nativeK5DIInnerPrefix_full_parity W R inner outer (more ++ shift)) z).symm

end OriginalPhysicalC60

#print axioms nativeC60DKCanonicalQuotientEquiv
#print axioms nativeC60DKCanonical_refl
#print axioms nativeC60DKCanonical_comp
#print axioms nativeC60DKDJTransport_eq_canonical
#print axioms nativeC60DKDJTransport_comp
#print axioms nativeC60DKStrict_comp_defect_kernel
#print axioms nativeK5DKCanonicalParityTransport
#print axioms nativeK5DKCanonical_refl
#print axioms nativeK5DKCanonical_comp
#print axioms nativeK5DKDJInnerPrefix_eq_canonical
#print axioms nativeK5DKInnerPrefix_quotient_comp
#print axioms nativeK5DKInnerPrefix_strict_twostep_parity
#print axioms nativeK5DKInnerPrefix_twostep_total_parity

end
end Kuu.F112.Physical
