import Kuu.F112.PolygonNativeC60AQFullPentagonFiniteRankQuotients
import Mathlib.Algebra.Group.TypeTags.Hom
import Mathlib.GroupTheory.Finiteness
import Mathlib.RingTheory.Finiteness.Defs
import Mathlib.LinearAlgebra.Dimension.StrongRankCondition
import Mathlib.LinearAlgebra.Dimension.Constructions

/-!
# F112-P94D3EC — non-finite generation of genuine C60 AQ obstruction kernels

EB established, without assuming any commutativity of the original
Type-valued pentagon obstruction kernel, surjective group homomorphisms
from its actual abelianization to Z^n for EVERY finite n.

EC derives the strict finite-generation obstruction from the pinned
mathlib rank theory over Z:
* The homomorphic image of a finitely generated group is finitely generated.
* The additive re-interpretation of a finitely generated commutative group
  is a finite module over Z.
* Surjective Z-linear maps do not increase finite rank.
* The free Z-module (Fin n -> Z) has exact rank n.
Choosing n = finrank(source) + 1 yields a contradiction.

A true C60 AU dependent 16D zigzag provides the 18D defect witnesses.
The proof retains the actual noncommutative kernel and separately
tests its actual abelianization. It does NOT assert the kernel is
abelian, free abelian, nor that a geometric 19D filler exists.
DS no-go, strict Kuu, independent Kuu as a presentation, original
14D--18D Type-valued proof history, the public 107 roots, no-Gray,
and append-only, fixed-toolchain conditions remain intact.
No sorry, admit, or new axioms.
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

section FiniteGenerationObstruction

/-- An abelian integer-vector group receiver becomes a genuine
additive homomorphism from the additive reinterpretation of the
source group. Its construction is not a claim about any earlier
noncommutative obstruction kernel. -/
private def nativeC60ECToIntAddHom
    {G : Type*} [CommGroup G] (n : ℕ)
    (f : G →* (Fin n → Multiplicative ℤ)) :
    Additive G →+ (Fin n → ℤ) where
  toFun x i := ((f x.toMul) i).toAdd
  map_zero' := by
    funext i
    change ((f (1 : G)) i).toAdd = 0
    rw [map_one]
    rfl
  map_add' x y := by
    funext i
    change ((f (x.toMul * y.toMul)) i).toAdd =
      ((f x.toMul) i).toAdd + ((f y.toMul) i).toAdd
    rw [map_mul]
    rfl

/-- Ordinary surjectivity survives genuine additive reinterpretation,
without introducing a choice of a generating set. -/
private theorem nativeC60ECToIntAddHom_surjective
    {G : Type*} [CommGroup G] (n : ℕ)
    (f : G →* (Fin n → Multiplicative ℤ))
    (hf : Function.Surjective f) :
    Function.Surjective (nativeC60ECToIntAddHom n f) := by
  intro v
  obtain ⟨x, hx⟩ := hf (fun i => Multiplicative.ofAdd (v i))
  refine ⟨Additive.ofMul x, ?_⟩
  funext i
  change ((f x) i).toAdd = v i
  rw [hx]
  rfl

/-- General rank obstruction: a COMMUTATIVE group that surjects onto
arbitrarily high finite-rank integer lattices cannot be generated
by a finite family. The only commutativity assumed is here, on the
abelian receiver; not on the original C60 kernel. -/
private theorem nativeC60ECUnboundedRank_not_fg
    {G : Type*} [CommGroup G]
    (h : ∀ n : ℕ, ∃ f : G →* (Fin n → Multiplicative ℤ),
      Function.Surjective f) : ¬ Group.FG G := by
  intro hfg
  letI : Group.FG G := hfg
  letI : Module.Finite ℤ (Additive G) :=
    Module.Finite.iff_addGroup_fg.mpr
      (inferInstance : AddGroup.FG (Additive G))
  let rank := Module.finrank ℤ (Additive G)
  obtain ⟨f, hf⟩ := h (rank + 1)
  let linear : Additive G →ₗ[ℤ] (Fin (rank + 1) → ℤ) :=
    (nativeC60ECToIntAddHom (rank + 1) f).toIntLinearMap
  have hlinear : Function.Surjective linear := by
    exact nativeC60ECToIntAddHom_surjective (rank + 1) f hf
  have hbound : Module.finrank ℤ (Fin (rank + 1) → ℤ) ≤
      Module.finrank ℤ (Additive G) :=
    LinearMap.finrank_le_finrank_of_surjective hlinear
  have hfalse : rank + 1 ≤ rank := by
    simpa [rank, Module.finrank_pi] using hbound
  omega

variable {L : NativeC60AXLayer.{u}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- Main EC theorem I: the TRUE abelianization of the original
(noncommutative) transported-vs-full quotient kernel is NOT
finitely generated. Every finite-rank integer quotient is supplied
by EB's actual dependent Type-valued pentagon witnesses. -/
theorem nativeC60ECAbelianKernel_not_fg (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b) :
    ¬ Group.FG
      (Abelianization ((nativeC60DZImageToFull S F word).ker)) := by
  apply nativeC60ECUnboundedRank_not_fg
  intro rank
  exact ⟨nativeC60EBAbelianReceiver S F word rank,
    nativeC60EBAbelianReceiver_surjective S F word r rank⟩

/-- Main EC theorem II: even the ACTUAL original noncommutative
quotient kernel is not finitely generated.
If it were, its surjective abelianization would be finitely
generated, contradicting the independent integer receivers. -/
theorem nativeC60ECOriginalKernel_not_fg (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b) :
    ¬ Group.FG ((nativeC60DZImageToFull S F word).ker) := by
  intro hfg
  letI : Group.FG ((nativeC60DZImageToFull S F word).ker) := hfg
  have hproj : Function.Surjective
      (Abelianization.of :
        (nativeC60DZImageToFull S F word).ker →*
          Abelianization ((nativeC60DZImageToFull S F word).ker)) := by
    change Function.Surjective
      (QuotientGroup.mk'
        (commutator ((nativeC60DZImageToFull S F word).ker)))
    exact QuotientGroup.mk'_surjective _
  have hfgAb : Group.FG
      (Abelianization ((nativeC60DZImageToFull S F word).ker)) :=
    Group.fg_of_surjective hproj
  exact (nativeC60ECAbelianKernel_not_fg S F word r) hfgAb

end FiniteGenerationObstruction

section PhysicalC60AU

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

/-- For EVERY physically chosen C60 AU zigzag W and finite AQ tree,
the actual abelian obstruction kernel is non-finitely generated. -/
theorem nativeK5ECPhysicalAQ_abelianKernel_not_fg
    (W : NativeK5StructuralThirteenCell p U V)
    (tree : NativeK5DOContextTree) :
    let S := nativeK5AXKuuSignature W
    let F := nativeK5BCFrame W
    ¬ Group.FG
      (Abelianization
        ((nativeC60DZImageToFull S F (nativeK5DOTreeWord tree)).ker)) := by
  dsimp only
  exact nativeC60ECAbelianKernel_not_fg
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
    (nativeK5DOTreeWord tree)
    (nativeC60DYOriginalZigzagGen
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
      (nativeK5CEPhysicalAUGenerator W))

/-- The physical original noncommutative kernel cannot be finitely
generated either; no abelianization of its underlying group is assumed. -/
theorem nativeK5ECPhysicalAQ_originalKernel_not_fg
    (W : NativeK5StructuralThirteenCell p U V)
    (tree : NativeK5DOContextTree) :
    let S := nativeK5AXKuuSignature W
    let F := nativeK5BCFrame W
    ¬ Group.FG
      ((nativeC60DZImageToFull S F (nativeK5DOTreeWord tree)).ker) := by
  dsimp only
  exact nativeC60ECOriginalKernel_not_fg
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
    (nativeK5DOTreeWord tree)
    (nativeC60DYOriginalZigzagGen
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
      (nativeK5CEPhysicalAUGenerator W))

end PhysicalC60AU

#print axioms nativeC60ECAbelianKernel_not_fg
#print axioms nativeC60ECOriginalKernel_not_fg
#print axioms nativeK5ECPhysicalAQ_abelianKernel_not_fg
#print axioms nativeK5ECPhysicalAQ_originalKernel_not_fg

end
end Kuu.F112.Physical
