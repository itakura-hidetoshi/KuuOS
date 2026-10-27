import Kuu.F112.PolygonNativeC60DoubleSymmDescentObstruction

/-!
# F112-P94D3DB — exact full strict CN/BW descent iff injectivity

CY proves that, at every genuine conservative C60 fifteen-dimensional
base with independently chosen finite inner/outer AQ contexts, the
EXISTING actual strict CO/CN retraction is a group isomorphism.
DA proves that collapsing particular original double-symm witnesses
obstructs exact decoding.

DB gives the COMPLETE classification for every independently supplied
SURJECTIVE group homomorphism q from the actual strict isotropy:
the ORIGINAL CN retraction factors through q as a group homomorphism
if and only if q is injective. The same holds for complete BW strict
holonomy. Hence a surjective CN-preserving quotient is an isomorphism;
the factor decoder is unique.

Surjectivity is necessary for the stated sufficiency construction:
for an arbitrary non-surjective map, factorization still implies
injectivity but injectivity alone does NOT imply a decoder extension.
No quotient or geometric 16-cell is silently constructed or imposed.
The original 14D/15D Type-valued boundaries, BC provenance, finite
AQ histories, strict Kuu, independent Kuu presentations and existing
no-go results remain unchanged.

No Gray, no new geometric relation, new axiom, sorry or admit.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uDB vDB wDB uD vD uE vE

section AbstractSurjectiveDescent

variable {G : Type uDB} {H : Type vDB} {Q : Type wDB}
variable [Group G] [Group H] [Group Q]

/-- An exact factorization through an ARBITRARY group map forces
injectivity whenever its original readout is faithful.
Surjectivity is not needed in this necessary direction. -/
theorem nativeC60DBDescent_requires_injective
    (r : G →* H) (hr : Function.Injective r)
    (q : G →* Q)
    (hdesc : ∃ decoder : Q →* H, decoder.comp q = r) :
    Function.Injective q := by
  obtain ⟨decoder, hdecoder⟩ := hdesc
  intro x y hxy
  apply hr
  have hx := DFunLike.congr_fun hdecoder x
  have hy := DFunLike.congr_fun hdecoder y
  change decoder (q x) = r x at hx
  change decoder (q y) = r y at hy
  exact hx.symm.trans ((congrArg decoder hxy).trans hy)

/-- A SURJECTIVE and INJECTIVE proposed geometric group quotient is
an actual group equivalence. Its inverse is selected from the proved
fibers, never from an assumed inverse of the original C60 context. -/
def nativeC60DBBijectiveQuotientEquiv
    (q : G →* Q) (hsurj : Function.Surjective q)
    (hinj : Function.Injective q) : G ≃* Q where
  toFun := q
  invFun z := Classical.choose (hsurj z)
  left_inv := by
    intro g
    apply hinj
    exact Classical.choose_spec (hsurj (q g))
  right_inv := by
    intro z
    exact Classical.choose_spec (hsurj z)
  map_mul' := q.map_mul

/-- A typed, explicit group decoder from the proposed quotient back to
the true original CN or BW receiver, when that quotient is bijective. -/
def nativeC60DBExplicitDecoder
    (r : G →* H)
    (q : G →* Q) (hsurj : Function.Surjective q)
    (hinj : Function.Injective q) : Q →* H :=
  r.comp (nativeC60DBBijectiveQuotientEquiv q hsurj hinj).symm.toMonoidHom

/-- The constructed decoder recovers the EXACT original group map,
not merely its action on a chosen free-generator family. -/
theorem nativeC60DBExplicitDecoder_comp
    (r : G →* H)
    (q : G →* Q) (hsurj : Function.Surjective q)
    (hinj : Function.Injective q) :
    (nativeC60DBExplicitDecoder r q hsurj hinj).comp q = r := by
  apply MonoidHom.ext
  intro g
  change r ((nativeC60DBBijectiveQuotientEquiv q hsurj hinj).symm
    (q g)) = r g
  exact congrArg r
    ((nativeC60DBBijectiveQuotientEquiv q hsurj hinj).left_inv g)

/-- MAIN GENERAL DB THEOREM. For a surjective group map, preserving
an ORIGINAL faithful group-valued invariant is equivalent to the map
being injective. The source invariant is supplied, not manufactured
from a quotient observation. -/
theorem nativeC60DBSurjective_descent_iff_injective
    (r : G →* H) (hr : Function.Injective r)
    (q : G →* Q) (hsurj : Function.Surjective q) :
    (∃ decoder : Q →* H, decoder.comp q = r) ↔
      Function.Injective q := by
  constructor
  · intro hdesc
    exact nativeC60DBDescent_requires_injective r hr q hdesc
  · intro hinj
    exact ⟨nativeC60DBExplicitDecoder r q hsurj hinj,
      nativeC60DBExplicitDecoder_comp r q hsurj hinj⟩

/-- A surjective q determines at MOST one exact decoder, so the
proof is not dependent on an arbitrary selection of a new observable. -/
theorem nativeC60DBSurjective_decoder_unique
    (r : G →* H) (q : G →* Q)
    (hsurj : Function.Surjective q)
    (d e : Q →* H)
    (hd : d.comp q = r) (he : e.comp q = r) :
    d = e := by
  apply MonoidHom.ext
  intro z
  obtain ⟨x, rfl⟩ := hsurj z
  have hx := DFunLike.congr_fun hd x
  have hy := DFunLike.congr_fun he x
  change d (q x) = r x at hx
  change e (q x) = r x at hy
  exact hx.trans hy.symm

/-- In particular a surjective quotient admitting the entire original
faithful decoder cannot truly quotient anything: it is isomorphic
to the original strict group. -/
theorem nativeC60DBSurjective_descent_forces_equivalence
    (r : G →* H) (hr : Function.Injective r)
    (q : G →* Q) (hsurj : Function.Surjective q)
    (hdesc : ∃ decoder : Q →* H, decoder.comp q = r) :
    ∃ e : G ≃* Q, ∀ x : G, e x = q x := by
  have hinj : Function.Injective q :=
    nativeC60DBDescent_requires_injective r hr q hdesc
  exact ⟨nativeC60DBBijectiveQuotientEquiv q hsurj hinj, fun _ => rfl⟩

end AbstractSurjectiveDescent

section PhysicalConservativeC60

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

/-- The actual ORIGINAL strict C60 conservative isotropy at the precise
outer AQ framed dependent fifteen-dimensional boundary. -/
abbrev nativeK5DBIsotropy
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer : List Bool) :=
  NativeC60COIsotropy
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
    outer (nativeK5CHSource W inner (nativeK5CKConservativeRefl W R))

/-- The actual original proof-carrying CN fork alphabet after choosing
one conservative 16D atom generator. This is not the entire abstract
code set of a novel independently declared group. -/
abbrev nativeK5DBForkFree
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner : List Bool) :=
  FreeGroup (NativeC60CNForkAlphabet
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
    (nativeK5CKAtomGenerator W R inner))

/-- Exact physical theorem: among all surjective maps from the
genuine strict C60 isotropy, and with all finite original AQ contexts,
the WHOLE CN retraction descends iff the map is injective. -/
theorem nativeK5DBPhysical_CN_descent_iff_injective
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer : List Bool)
    {Q : Type wDB} [Group Q]
    (quotient : nativeK5DBIsotropy W R inner outer →* Q)
    (hsurj : Function.Surjective quotient) :
    (∃ decoder : Q →* nativeK5DBForkFree W R inner,
      decoder.comp quotient =
        nativeC60CORetraction (nativeK5AXKuuSignature W)
          (nativeK5BCFrame W) outer (nativeK5CKAtomGenerator W R inner)) ↔
      Function.Injective quotient := by
  exact nativeC60DBSurjective_descent_iff_injective
    (nativeC60CORetraction (nativeK5AXKuuSignature W)
      (nativeK5BCFrame W) outer (nativeK5CKAtomGenerator W R inner))
    (nativeC60CYGenericRetraction_injective
      (nativeC60CORetraction (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W) outer (nativeK5CKAtomGenerator W R inner))
      (nativeK5CYPhysicalKernel_eq_one W R inner outer))
    quotient hsurj

/-- Exact physical theorem for faithful FULL noncommutative BW strict
holonomy, not just an abelian charge or a partial signed-word code. -/
theorem nativeK5DBPhysical_BW_descent_iff_injective
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer : List Bool)
    {Q : Type wDB} [Group Q]
    (quotient : nativeK5DBIsotropy W R inner outer →* Q)
    (hsurj : Function.Surjective quotient) :
    (∃ descended : Q →*
        FreeGroup (NativeC60BVGeneratorCode (nativeK5AXKuuSignature W)),
      descended.comp quotient =
        nativeC60COHolonomy (nativeK5AXKuuSignature W)
          (nativeK5BCFrame W) outer
          (nativeK5CHSource W inner (nativeK5CKConservativeRefl W R))) ↔
      Function.Injective quotient := by
  exact nativeC60DBSurjective_descent_iff_injective
    (nativeC60COHolonomy (nativeK5AXKuuSignature W)
      (nativeK5BCFrame W) outer
      (nativeK5CHSource W inner (nativeK5CKConservativeRefl W R)))
    (nativeC60COHolonomy_injective (nativeK5AXKuuSignature W)
      (nativeK5BCFrame W) outer
      (nativeK5CHSource W inner (nativeK5CKConservativeRefl W R)))
    quotient hsurj

/-- At the actual full physical isotropy, complete CN descent and
complete BW descent are EQUIVALENT for every independently supplied
surjective group quotient. Their kernels are not equated in some
separately invented raw comparison presentation. -/
theorem nativeK5DBPhysical_CN_iff_BW_descent
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer : List Bool)
    {Q : Type wDB} [Group Q]
    (quotient : nativeK5DBIsotropy W R inner outer →* Q)
    (hsurj : Function.Surjective quotient) :
    (∃ decoder : Q →* nativeK5DBForkFree W R inner,
      decoder.comp quotient =
        nativeC60CORetraction (nativeK5AXKuuSignature W)
          (nativeK5BCFrame W) outer (nativeK5CKAtomGenerator W R inner)) ↔
    (∃ descended : Q →*
        FreeGroup (NativeC60BVGeneratorCode (nativeK5AXKuuSignature W)),
      descended.comp quotient =
        nativeC60COHolonomy (nativeK5AXKuuSignature W)
          (nativeK5BCFrame W) outer
          (nativeK5CHSource W inner (nativeK5CKConservativeRefl W R))) := by
  exact (nativeK5DBPhysical_CN_descent_iff_injective
    W R inner outer quotient hsurj).trans
    (nativeK5DBPhysical_BW_descent_iff_injective
      W R inner outer quotient hsurj).symm

/-- Exact CN-preserving surjective quotients are ONLY isomorphisms of
the original physical strict C60 isotropy. All lower Type-valued
proof witnesses are still accessed through the original group. -/
theorem nativeK5DBPhysical_CN_descent_forces_isomorphism
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer : List Bool)
    {Q : Type wDB} [Group Q]
    (quotient : nativeK5DBIsotropy W R inner outer →* Q)
    (hsurj : Function.Surjective quotient)
    (hdesc : ∃ decoder : Q →* nativeK5DBForkFree W R inner,
      decoder.comp quotient =
        nativeC60CORetraction (nativeK5AXKuuSignature W)
          (nativeK5BCFrame W) outer (nativeK5CKAtomGenerator W R inner)) :
    ∃ e : nativeK5DBIsotropy W R inner outer ≃* Q,
      ∀ z : nativeK5DBIsotropy W R inner outer, e z = quotient z := by
  exact nativeC60DBSurjective_descent_forces_equivalence
    (nativeC60CORetraction (nativeK5AXKuuSignature W)
      (nativeK5BCFrame W) outer (nativeK5CKAtomGenerator W R inner))
    (nativeC60CYGenericRetraction_injective
      (nativeC60CORetraction (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W) outer (nativeK5CKAtomGenerator W R inner))
      (nativeK5CYPhysicalKernel_eq_one W R inner outer))
    quotient hsurj hdesc

/-- Even without surjectivity, a proposed map that identifies TWO
different original strict loops can NEVER admit the full CN decoder.
DA is the concrete double-symm instance of this general obstruction. -/
theorem nativeK5DBPhysical_any_collapse_no_CN_descent
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (inner outer : List Bool)
    {Q : Type wDB} [Group Q]
    (quotient : nativeK5DBIsotropy W R inner outer →* Q)
    (x y : nativeK5DBIsotropy W R inner outer)
    (hne : x ≠ y) (hidentify : quotient x = quotient y) :
    ¬ ∃ decoder : Q →* nativeK5DBForkFree W R inner,
      decoder.comp quotient =
        nativeC60CORetraction (nativeK5AXKuuSignature W)
          (nativeK5BCFrame W) outer (nativeK5CKAtomGenerator W R inner) := by
  intro hdesc
  have hinj : Function.Injective quotient :=
    nativeC60DBDescent_requires_injective
      (nativeC60CORetraction (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W) outer (nativeK5CKAtomGenerator W R inner))
      (nativeC60CYGenericRetraction_injective
        (nativeC60CORetraction (nativeK5AXKuuSignature W)
          (nativeK5BCFrame W) outer (nativeK5CKAtomGenerator W R inner))
        (nativeK5CYPhysicalKernel_eq_one W R inner outer))
      quotient hdesc
  exact hne (hinj hidentify)

end PhysicalConservativeC60

#print axioms nativeC60DBDescent_requires_injective
#print axioms nativeC60DBBijectiveQuotientEquiv
#print axioms nativeC60DBExplicitDecoder
#print axioms nativeC60DBExplicitDecoder_comp
#print axioms nativeC60DBSurjective_descent_iff_injective
#print axioms nativeC60DBSurjective_decoder_unique
#print axioms nativeC60DBSurjective_descent_forces_equivalence
#print axioms nativeK5DBIsotropy
#print axioms nativeK5DBForkFree
#print axioms nativeK5DBPhysical_CN_descent_iff_injective
#print axioms nativeK5DBPhysical_BW_descent_iff_injective
#print axioms nativeK5DBPhysical_CN_iff_BW_descent
#print axioms nativeK5DBPhysical_CN_descent_forces_isomorphism
#print axioms nativeK5DBPhysical_any_collapse_no_CN_descent

end
end Kuu.F112.Physical
