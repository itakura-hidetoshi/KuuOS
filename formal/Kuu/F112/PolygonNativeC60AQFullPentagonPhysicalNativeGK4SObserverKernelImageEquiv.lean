import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK4RObservedUnitsVsSourceNoGo
import Mathlib.Tactic

/-!
# F112-P94D3GK4S — genuine P92B observer-kernel quotient = actual observation image

The original typed P92B witness-existence quotient is NOT replaced or
identified with the separately extended F54 STRUCTURAL comparison quotient.
At EACH fully dependent genuine F45 source/target boundary, take the precise
kernel Setoid of an arbitrary GK4O original P92B observer family:
  q ∼ r ↔ observe first last q = observe first last r.
The corresponding second quotient admits a canonical map to GK4Q's ACTUAL
dependent observation image. Prove it is bijective and build the natural
set-level equivalence, without choosing synthetic F54 routes, weakening
typed boundaries or identifying distinct original Type-valued P92B cells.

A map from original P92B classes factors through the observer kernel iff
it is constant on every observational fiber; its lift is unique. Under
GK4P's actual F54 composition/context laws, transport GK4Q's real
dependent image composition to the kernel quotient, and show the original
P92B quotient's genuine composition is preserved by this projection.
The induced operation is associative only under the explicit original
value-operation associativity hypothesis; this does NOT establish the
missing original P92B associativity.

The Boolean observer's P92B->kernel projection is provably NOT injective
at EVERY inhabited original F45 stage: genuine zero-route left-unit
failure in ORIGINAL P92B classes is erased by the Boolean grade.
In the physical C60 north stage the obstruction is unconditional.
The Boolean observation image is unital (GK4R) while original P92B
is not; the Option Nat image remains nonunital and does not descend
through actual extended structural F54 unit seams.

No new axioms, sorry/admit, Gray or unverified quotient equivalence.
No historical complete P92B/F19/F28/F54/F55 typed equivalence,
original 14D unconditional Countable, original 19D filler, global
strict n or hyperdescent. Append-only same-root / 107 public roots.
Pinned Lean v4.30.0-rc2 and mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Protect validation-only PR #1558 Draft/open/unmerged.
Copyright 板倉英俊 / Hidetoshi Itakura. Apache-2.0.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe uD vD uE vE uB uC

section KernelQuotient

variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {B : Type uB}
variable (observe : NativeGK4OObserverFamily p D E B)
variable {a b : D} {x y : E} {n n' m m' : Nat}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}
variable (first : KuuNativeF45Tree p n m ma pa mb pb)
variable (last : KuuNativeF45Tree p n' m' ma pa mb pb)

/-- Exact equality kernel of a VALUE observer on the actual ORIGINAL
P92B existence quotient, at this unchanged typed F45 boundary. -/
def nativeGK4SKernelSetoid :
    Setoid (NativeF55P92AssocRouteClasses first last) where
  r := fun q r => observe first last q = observe first last r
  iseqv := ⟨
    (by intro q; rfl),
    (by intro q r h; exact h.symm),
    (by intro q r s hqr hrs; exact hqr.trans hrs)⟩

/-- SECOND quotient: ORIGINAL P92B classes modulo their precise
observational equality, NOT quotient of raw F54 routes and NOT GK4E. -/
abbrev NativeGK4SKernelClasses :=
  Quotient (nativeGK4SKernelSetoid observe first last)

/-- Canonical SECOND-quotient projection, from true original P92B
witness-existence classes. -/
def nativeGK4SKernelClass
    (q : NativeF55P92AssocRouteClasses first last) :
    NativeGK4SKernelClasses observe first last :=
  _root_.Quotient.mk (nativeGK4SKernelSetoid observe first last) q

/-- This second quotient identifies EXACTLY and ONLY equal
observer values; no new Type-valued original P92B comparison is deduced. -/
theorem nativeGK4SKernelClass_eq_iff
    (q r : NativeF55P92AssocRouteClasses first last) :
    nativeGK4SKernelClass observe first last q =
      nativeGK4SKernelClass observe first last r ↔
      observe first last q = observe first last r := by
  constructor
  · intro h
    exact _root_.Quotient.exact h
  · intro h
    exact _root_.Quotient.sound h

/-- The exact observer-kernel quotient maps to GK4Q's ACTUAL image
subtype, not to an assumed globally inhabited/full ambient codomain. -/
def nativeGK4SKernelToImage :
    NativeGK4SKernelClasses observe first last →
      NativeGK4QImage observe first last :=
  _root_.Quotient.lift
    (nativeGK4QOfClass observe first last)
    (by
      intro q r h
      exact Subtype.ext h)

@[simp] theorem nativeGK4SKernelToImage_class
    (q : NativeF55P92AssocRouteClasses first last) :
    nativeGK4SKernelToImage observe first last
      (nativeGK4SKernelClass observe first last q) =
      nativeGK4QOfClass observe first last q := by
  rfl

/-- Injectivity is not obtained by falsely assuming that the original
P92B observer is injective; only observationally indistinguishable
P92B classes have ALREADY been identified by the second quotient. -/
theorem nativeGK4SKernelToImage_injective :
    Function.Injective (nativeGK4SKernelToImage observe first last) := by
  intro x y
  refine _root_.Quotient.inductionOn₂ x y ?_
  intro q r h
  exact _root_.Quotient.sound (congrArg Subtype.val h)

/-- Surjectivity uses the TRUE original P92B witness carried by each
actual GK4Q image element; no arbitrary replacement of the image. -/
theorem nativeGK4SKernelToImage_surjective :
    Function.Surjective (nativeGK4SKernelToImage observe first last) := by
  intro z
  obtain ⟨q, hq⟩ := nativeGK4QOfClass_surjective observe first last z
  exact ⟨nativeGK4SKernelClass observe first last q, hq⟩

/-- Genuine (set-level) first-isomorphism theorem at EVERY original
dependent F45 source/target, preserving original P92B and GK4E borders. -/
def nativeGK4SKernelImageEquiv :
    NativeGK4SKernelClasses observe first last ≃
      NativeGK4QImage observe first last :=
  Equiv.ofBijective
    (nativeGK4SKernelToImage observe first last)
    ⟨nativeGK4SKernelToImage_injective observe first last,
      nativeGK4SKernelToImage_surjective observe first last⟩

@[simp] theorem nativeGK4SKernelImageEquiv_class
    (q : NativeF55P92AssocRouteClasses first last) :
    nativeGK4SKernelImageEquiv observe first last
      (nativeGK4SKernelClass observe first last q) =
        nativeGK4QOfClass observe first last q := by
  rfl

/-- Exact universal property of the SECOND quotient: an arbitrary
P92B class map factors iff observationally equal classes map equally.
No original 3-cell comparison between equal observed values is claimed. -/
theorem nativeGK4SKernelFactor_iff
    {C : Type uC}
    (f : NativeF55P92AssocRouteClasses first last → C) :
    (∃ lift : NativeGK4SKernelClasses observe first last → C,
      ∀ q : NativeF55P92AssocRouteClasses first last,
        lift (nativeGK4SKernelClass observe first last q) = f q) ↔
      (∀ q r : NativeF55P92AssocRouteClasses first last,
        observe first last q = observe first last r →
          f q = f r) := by
  constructor
  · rintro ⟨lift, hlift⟩ q r h
    calc
      f q = lift (nativeGK4SKernelClass observe first last q) :=
        (hlift q).symm
      _ = lift (nativeGK4SKernelClass observe first last r) :=
        congrArg lift ((nativeGK4SKernelClass_eq_iff observe first last q r).mpr h)
      _ = f r := hlift r
  · intro hfiber
    refine ⟨_root_.Quotient.lift f (fun q r h => hfiber q r h), ?_⟩
    intro q
    rfl

/-- Unique lift: no arbitrary choices of raw F54 or original P92B
representatives occur when the observer-kernel factor exists. -/
theorem nativeGK4SKernelFactor_unique
    {C : Type uC}
    (f : NativeF55P92AssocRouteClasses first last → C)
    (lift₁ lift₂ : NativeGK4SKernelClasses observe first last → C)
    (h₁ : ∀ q : NativeF55P92AssocRouteClasses first last,
      lift₁ (nativeGK4SKernelClass observe first last q) = f q)
    (h₂ : ∀ q : NativeF55P92AssocRouteClasses first last,
      lift₂ (nativeGK4SKernelClass observe first last q) = f q) :
    lift₁ = lift₂ := by
  funext z
  refine _root_.Quotient.inductionOn z ?_
  intro q
  exact (h₁ q).trans (h₂ q).symm

end KernelQuotient

section ObservableComposition
variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {B : Type uB}
variable (observe : NativeGK4OObserverFamily p D E B)
variable (combine : B → B → B)
variable (leftAction rightAction : NativeGK4PContextAction p D E B)
variable (laws : NativeGK4PObservationLaws observe combine leftAction rightAction)
variable {a b : D} {x y : E}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}
variable {n₁ n₂ n₃ n₄ m₁ m₂ m₃ m₄ : Nat}
variable (t₁ : KuuNativeF45Tree p n₁ m₁ ma pa mb pb)
variable (t₂ : KuuNativeF45Tree p n₂ m₂ ma pa mb pb)
variable (t₃ : KuuNativeF45Tree p n₃ m₃ ma pa mb pb)
variable (t₄ : KuuNativeF45Tree p n₄ m₄ ma pa mb pb)

/-- Transport ACTUAL GK4Q dependent image composition along the proven
kernel-image equivalence: does not alter source P92B multiplication. -/
def nativeGK4SKernelCompose
    (u : NativeGK4SKernelClasses observe t₁ t₂)
    (v : NativeGK4SKernelClasses observe t₂ t₃) :
    NativeGK4SKernelClasses observe t₁ t₃ :=
  (nativeGK4SKernelImageEquiv observe t₁ t₃).symm
    (nativeGK4QImageCompose observe combine leftAction rightAction laws t₁ t₂ t₃
      (nativeGK4SKernelImageEquiv observe t₁ t₂ u)
      (nativeGK4SKernelImageEquiv observe t₂ t₃ v))

/-- Original actual P92B quotient composition projects STRICTLY to
the observer-kernel quotient's transported product. -/
theorem nativeGK4SKernelCompose_class
    (u : NativeF55P92AssocRouteClasses t₁ t₂)
    (v : NativeF55P92AssocRouteClasses t₂ t₃) :
    nativeGK4SKernelCompose observe combine leftAction rightAction laws t₁ t₂ t₃
      (nativeGK4SKernelClass observe t₁ t₂ u)
      (nativeGK4SKernelClass observe t₂ t₃ v) =
    nativeGK4SKernelClass observe t₁ t₃
      (nativeGK4H_p92Compose t₁ t₂ t₃ u v) := by
  apply (nativeGK4SKernelImageEquiv observe t₁ t₃).injective
  simpa only [nativeGK4SKernelCompose, Equiv.apply_symm_apply,
    nativeGK4SKernelImageEquiv_class] using
    (nativeGK4QImageCompose_ofClass observe combine leftAction rightAction laws
      t₁ t₂ t₃ u v)

/-- The observer-kernel quotient is associative WHEN the observer VALUE
product is associative. This NEVER proves original P92B associativity. -/
theorem nativeGK4SKernelCompose_assoc
    (hassoc : ∀ x y z : B, combine (combine x y) z = combine x (combine y z))
    (u : NativeGK4SKernelClasses observe t₁ t₂)
    (v : NativeGK4SKernelClasses observe t₂ t₃)
    (w : NativeGK4SKernelClasses observe t₃ t₄) :
    nativeGK4SKernelCompose observe combine leftAction rightAction laws t₁ t₃ t₄
        (nativeGK4SKernelCompose observe combine leftAction rightAction laws
          t₁ t₂ t₃ u v) w =
    nativeGK4SKernelCompose observe combine leftAction rightAction laws t₁ t₂ t₄
        u (nativeGK4SKernelCompose observe combine leftAction rightAction laws
          t₂ t₃ t₄ v w) := by
  apply (nativeGK4SKernelImageEquiv observe t₁ t₄).injective
  simp only [nativeGK4SKernelCompose, Equiv.apply_symm_apply]
  exact nativeGK4QImageCompose_assoc observe combine leftAction rightAction laws
    hassoc t₁ t₂ t₃ t₄
    (nativeGK4SKernelImageEquiv observe t₁ t₂ u)
    (nativeGK4SKernelImageEquiv observe t₂ t₃ v)
    (nativeGK4SKernelImageEquiv observe t₃ t₄ w)

end ObservableComposition

section GenuineNonfaithfulness

variable {p : Polygon}
variable {D : Type uD} [Category.{vD} D]
variable {E : Type uE} [Category.{vE} E]
variable {a b : D} {x y : E} {n m : Nat}
variable {ma mb : KuuNativeBlocks a b}
variable {pa pb : KuuNativeBlocks x y}
variable (tree : KuuNativeF45Tree p n m ma pa mb pb)

/-- The real Boolean observer kernel loses information even on ONE
source P92B self-Hom: original left unit fails on an actual F54 route
but both P92B classes have identical zero/positive rotation grading. -/
theorem nativeGK4SBooleanKernelProjection_not_injective :
    ¬ Function.Injective
      (nativeGK4SKernelClass
        (nativeGK4OBooleanFamily p D E) tree tree) := by
  intro hinj
  let route : KuuNativeF45Tree.DepthRotationRoute p tree tree :=
    .chain (.refl tree)
  have hpair := nativeGK4H_p92Grade_cannot_reflect_unit tree tree route
  have hkernel :
      nativeGK4SKernelClass (nativeGK4OBooleanFamily p D E) tree tree
          (nativeGK4H_p92Compose tree tree tree (nativeGK4H_p92Unit tree)
            (nativeF55P92AssocRouteClass tree tree route)) =
        nativeGK4SKernelClass (nativeGK4OBooleanFamily p D E) tree tree
          (nativeF55P92AssocRouteClass tree tree route) :=
    (nativeGK4SKernelClass_eq_iff (nativeGK4OBooleanFamily p D E) tree tree _ _).mpr
      hpair.1
  exact hpair.2 (hinj hkernel)

/-- Concrete non-injectivity is unconditional in the TRUE physical
C60 north F45 triple (no external countability assumptions). -/
theorem nativeGK4SPhysicalNorthBooleanKernel_not_injective :
    ¬ Function.Injective
      (nativeGK4SKernelClass (nativeGK4OBooleanFamily _ _ _)
        nativeGK4FPhysicalNorthTriple nativeGK4FPhysicalNorthTriple) := by
  exact nativeGK4SBooleanKernelProjection_not_injective
    nativeGK4FPhysicalNorthTriple

end GenuineNonfaithfulness

#print axioms nativeGK4SKernelSetoid
#print axioms NativeGK4SKernelClasses
#print axioms nativeGK4SKernelClass
#print axioms nativeGK4SKernelClass_eq_iff
#print axioms nativeGK4SKernelToImage
#print axioms nativeGK4SKernelToImage_class
#print axioms nativeGK4SKernelToImage_injective
#print axioms nativeGK4SKernelToImage_surjective
#print axioms nativeGK4SKernelImageEquiv
#print axioms nativeGK4SKernelImageEquiv_class
#print axioms nativeGK4SKernelFactor_iff
#print axioms nativeGK4SKernelFactor_unique
#print axioms nativeGK4SKernelCompose
#print axioms nativeGK4SKernelCompose_class
#print axioms nativeGK4SKernelCompose_assoc
#print axioms nativeGK4SBooleanKernelProjection_not_injective
#print axioms nativeGK4SPhysicalNorthBooleanKernel_not_injective

end
end Kuu.F112.Physical
