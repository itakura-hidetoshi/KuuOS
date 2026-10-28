import Kuu.F112.PolygonNativeC60AQFullPentagonTailComplementEmbedding
import Mathlib.Algebra.Group.TypeTags.Hom
import Mathlib.GroupTheory.Finiteness
import Mathlib.RingTheory.Finiteness.Defs
import Mathlib.LinearAlgebra.Dimension.StrongRankCondition
import Mathlib.LinearAlgebra.Dimension.Constructions

/-!
# F112-P94D3EH — nonfinite generation of every genuine finite-rank AQ complement

EG embeds the countable direct sum of integer pentagon charges in the
actual kernel of EVERY finite-rank abelianized AQ receiver. EH proves
the stronger concrete fact that, for each deleted finite rank n, this
same complementary kernel surjects onto integer vectors of EVERY
finite rank m. The receiver tests the consecutive surviving AQ
coordinates n,...,n+m-1.

The explicit surjection is witnessed by shifting EE's finite integer
extension, inserting it via the EG *actual kernel embedding*, and
evaluating ED's genuine Kronecker charge recovery. Applying the same
pinned-mathlib finite-rank obstruction as EC proves that none of
these honest complementary subgroups is finitely generated.

The source Type-valued obstruction kernel is not declared abelian;
only its actual abelianization and its subgroup kernels have
commutative group structure. No claim is made about the total
abelianization being free, infinite-product surjectivity, infinite
splitting, a 19D geometric filler, or any Gray structure.
Preserve strict Kuu, independent Kuu as a presentation, DS no-go,
the 14D--18D Type-valued history, pinned toolchain, all 107 public
roots, and same-root/append-only requirements.
No new axiom, sorry, or admit.
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

section AbstractFiniteRankContradiction

/-- The integer-vector receiver, after converting a commutative
multiplicative source to its additive presentation. -/
private def nativeC60EHToIntAddHom
    {G : Type*} [CommGroup G] (rank : ℕ)
    (f : G →* (Fin rank → Multiplicative ℤ)) :
    Additive G →+ (Fin rank → ℤ) where
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

/-- A surjective multiplicative integer-vector receiver gives
a genuinely surjective additive receiver. -/
private theorem nativeC60EHToIntAddHom_surjective
    {G : Type*} [CommGroup G] (rank : ℕ)
    (f : G →* (Fin rank → Multiplicative ℤ))
    (hf : Function.Surjective f) :
    Function.Surjective (nativeC60EHToIntAddHom rank f) := by
  intro v
  obtain ⟨x, hx⟩ := hf (fun i => Multiplicative.ofAdd (v i))
  refine ⟨Additive.ofMul x, ?_⟩
  funext i
  change ((f x) i).toAdd = v i
  rw [hx]
  rfl

/-- The EC finite-rank contradiction, now independently available
for the TRUE commutative complementary kernels. The assumption is
surjectivity to all finite integer powers, not mere subgroup size. -/
private theorem nativeC60EHUnboundedRank_not_fg
    {G : Type*} [CommGroup G]
    (h : ∀ rank : ℕ, ∃ f : G →* (Fin rank → Multiplicative ℤ),
      Function.Surjective f) : ¬ Group.FG G := by
  intro hfg
  letI : Group.FG G := hfg
  letI : Module.Finite ℤ (Additive G) :=
    Module.Finite.iff_addGroup_fg.mpr
      (inferInstance : AddGroup.FG (Additive G))
  let rank := Module.finrank ℤ (Additive G)
  obtain ⟨f, hf⟩ := h (rank + 1)
  let linear : Additive G →ₗ[ℤ] (Fin (rank + 1) → ℤ) :=
    (nativeC60EHToIntAddHom (rank + 1) f).toIntLinearMap
  have hlinear : Function.Surjective linear := by
    exact nativeC60EHToIntAddHom_surjective (rank + 1) f hf
  have hbound : Module.finrank ℤ (Fin (rank + 1) → ℤ) ≤
      Module.finrank ℤ (Additive G) :=
    LinearMap.finrank_le_finrank_of_surjective hlinear
  have hfalse : rank + 1 ≤ rank := by
    simpa [rank, Module.finrank_pi] using hbound
  omega

end AbstractFiniteRankContradiction

section FiniteRankAQComplement

/-- The EG index shift preserves the exact integer coefficient
at every surviving coordinate n+j; its initial n coordinates vanish
by EG's separate theorem. -/
theorem nativeC60EHTailShift_apply
    (n : ℕ) (v : ℕ →₀ ℤ) (j : ℕ) :
    nativeC60EGTailShift n v (n + j) = v j := by
  change (Finsupp.mapDomain (fun k : ℕ => n + k) v) (n + j) = v j
  have hshift : Function.Injective (fun k : ℕ => n + k) := by
    intro a b hab
    change n + a = n + b at hab
    omega
  rw [Finsupp.mapDomain_apply hshift]

variable {L : NativeC60AXLayer.{u}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- The ACTUAL multiplicative group homomorphism on the honest
complementary kernel of the first n characters, evaluating the
next rank integer coordinates via the same EB abelian receiver. -/
def nativeC60EHTailReceiver (word : List Bool)
    (n rank : ℕ) :
    (nativeC60EBAbelianReceiver S F word n).ker →*
      (Fin rank → Multiplicative ℤ) where
  toFun x i :=
    (nativeC60EBAbelianReceiver S F word (n + rank))
      x.1 ⟨n + i.val, by omega⟩
  map_one' := by
    funext i
    change ((nativeC60EBAbelianReceiver S F word (n + rank))
      (1 : Abelianization ((nativeC60DZImageToFull S F word).ker)))
        ⟨n + i.val, by omega⟩ = 1
    rw [map_one]
    rfl
  map_mul' x y := by
    funext i
    change ((nativeC60EBAbelianReceiver S F word (n + rank))
      (x.1 * y.1)) ⟨n + i.val, by omega⟩ =
        ((nativeC60EBAbelianReceiver S F word (n + rank))
          x.1) ⟨n + i.val, by omega⟩ *
        ((nativeC60EBAbelianReceiver S F word (n + rank))
          y.1) ⟨n + i.val, by omega⟩
    rw [map_mul]
    rfl

/-- The explicit EG subgroup element obtained from a finite
integer vector has precisely that vector's surviving AQ coordinates.
This is an exact evaluation in the actual abelianization; none of the
original noncommutative defect generators is reordered. -/
theorem nativeC60EHTailReceiver_shiftedFiniteExtension
    (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n rank : ℕ) (v : Fin rank → Multiplicative ℤ) :
    (nativeC60EHTailReceiver S F word n rank)
      ((nativeC60EGTailComplementEmbedding S F word r n
        (nativeC60EEFiniteExtension rank
          (fun i => (v i).toAdd))).toMul) = v := by
  funext i
  change ((nativeC60EBAbelianReceiver S F word (n + rank))
      ((nativeC60EDFiniteSupportEmbedding S F word r
        (nativeC60EGTailShift n
          (nativeC60EEFiniteExtension rank (fun j => (v j).toAdd)))).toMul))
        ⟨n + i.val, by omega⟩ = v i
  rw [nativeC60EEReceiver_coordinate S F word (n + rank)
    (nativeC60EDFiniteSupportEmbedding S F word r
      (nativeC60EGTailShift n
        (nativeC60EEFiniteExtension rank (fun j => (v j).toAdd))))
      ⟨n + i.val, by omega⟩]
  rw [nativeC60EDCoordinate_finiteSupport S F word r
    (nativeC60EGTailShift n
      (nativeC60EEFiniteExtension rank (fun j => (v j).toAdd)))
    (n + i.val)]
  rw [nativeC60EHTailShift_apply n
    (nativeC60EEFiniteExtension rank (fun j => (v j).toAdd)) i.val]
  rw [nativeC60EEFiniteExtension_apply rank (fun j => (v j).toAdd) i]
  exact ofAdd_toAdd (v i)

/-- A surjection onto EVERY desired finite integer lattice is
supplied by the genuine surviving Type-valued AQ family in EG. -/
theorem nativeC60EHTailReceiver_surjective (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n rank : ℕ) :
    Function.Surjective (nativeC60EHTailReceiver S F word n rank) := by
  intro v
  exact ⟨(nativeC60EGTailComplementEmbedding S F word r n
    (nativeC60EEFiniteExtension rank
      (fun i => (v i).toAdd))).toMul,
    nativeC60EHTailReceiver_shiftedFiniteExtension
      S F word r n rank v⟩

/-- MAIN EH THEOREM: no finite deletion of independent AQ
coordinates can make the honest complementary kernel finitely
generated, with no new commutativity hypothesis on the source. -/
theorem nativeC60EHTailComplement_not_fg (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (r : (nativeC60DQTriangleSeventeenSignature S F).Gen a b)
    (n : ℕ) :
    ¬ Group.FG ((nativeC60EBAbelianReceiver S F word n).ker) := by
  apply nativeC60EHUnboundedRank_not_fg
  intro rank
  exact ⟨nativeC60EHTailReceiver S F word n rank,
    nativeC60EHTailReceiver_surjective S F word r n rank⟩

end FiniteRankAQComplement

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

/-- The physical C60 AU family and every honest finite AQ context tree
have non-finitely generated complementary abelianized obstruction
kernels after deleting ANY finite rank of integer coordinates. -/
theorem nativeK5EHPhysicalAQ_tailComplement_not_fg
    (W : NativeK5StructuralThirteenCell p U V)
    (tree : NativeK5DOContextTree) (rank : ℕ) :
    let S := nativeK5AXKuuSignature W
    let F := nativeK5BCFrame W
    ¬ Group.FG
      ((nativeC60EBAbelianReceiver S F
        (nativeK5DOTreeWord tree) rank).ker) := by
  dsimp only
  exact nativeC60EHTailComplement_not_fg
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
    (nativeK5DOTreeWord tree)
    (nativeC60DYOriginalZigzagGen
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
      (nativeK5CEPhysicalAUGenerator W)) rank

end PhysicalC60AU

#print axioms nativeC60EHTailShift_apply
#print axioms nativeC60EHTailReceiver
#print axioms nativeC60EHTailReceiver_shiftedFiniteExtension
#print axioms nativeC60EHTailReceiver_surjective
#print axioms nativeC60EHTailComplement_not_fg
#print axioms nativeK5EHPhysicalAQ_tailComplement_not_fg

end
end Kuu.F112.Physical
