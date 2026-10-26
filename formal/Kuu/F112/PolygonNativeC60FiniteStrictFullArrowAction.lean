import Kuu.F112.PolygonNativeC60FiniteContextStrictFunctorDescent

/-!
# F112-P94D3BE — full strict-arrow transport under finite C60 contexts

BD built a strict endofunctor for each finite original 14D C60 context.
BE proves their successive action on the *full dependent arrow bundle*
(including exact source, exact target and the strict arrow) is coherent
with context concatenation. The hom-level proof reduces to honest raw
Type-valued AX terms, not merely equality of objects or scalar shadows.

This is unary context coherence. It neither manufactures a binary
horizontal whiskering nor fills the original geometric 16-cell.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u v uD vD uE vE

/-- The identity word does not relabel the ACTUAL source-indexed
16D generator, including its proof-carrying endpoint equations. -/
theorem nativeC60BEShiftGen_nil {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {x y : L.Total}
    (g : (nativeC60BCClosedSignature S F).Gen x y) :
    nativeC60BCShiftGen S F [] g = g := by
  rcases g with ⟨word, a, b, ⟨gen, hx, hy⟩⟩
  rfl

/-- One outer letter acts by exactly the same raw generator as
successive inner-word transport and one-letter transport. -/
theorem nativeC60BEShiftGen_cons {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (side : Bool) (rest : List Bool)
    {x y : L.Total}
    (g : (nativeC60BCClosedSignature S F).Gen x y) :
    nativeC60BCShiftGen S F (side :: rest) g =
      nativeC60BCShiftGen S F [side]
        (nativeC60BCShiftGen S F rest g) := by
  rcases g with ⟨inner, a, b, ⟨gen, hx, hy⟩⟩
  cases hx
  cases hy
  rfl

/-- Identity context acts as the ACTUAL identity on Type-valued
AX higher syntax; no quotient or proof-term collapse is needed. -/
theorem nativeC60BEMapClosedStep_nil {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {x y : L.Total}
    (c : NativeC60AXStep (nativeC60BCClosedSignature S F) x y) :
    nativeC60BCMapClosedStep S F [] c = c := by
  induction c with
  | atom g =>
      change NativeC60AXStep.atom (nativeC60BCShiftGen S F [] g) =
        NativeC60AXStep.atom g
      rw [nativeC60BEShiftGen_nil S F g]
      rfl
  | refl _ => rfl
  | symm c ih =>
      change NativeC60AXStep.symm (nativeC60BCMapClosedStep S F [] c) =
        NativeC60AXStep.symm c
      rw [ih]
      rfl
  | trans c d ih ik =>
      change NativeC60AXStep.trans (nativeC60BCMapClosedStep S F [] c)
          (nativeC60BCMapClosedStep S F [] d) = NativeC60AXStep.trans c d
      rw [ih, ik]
      rfl

/-- Arbitrary long contexts admit an exact raw one-letter recursion on
EVERY typed 16D comparison, including inverse and vertical composites. -/
theorem nativeC60BEMapClosedStep_cons {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (side : Bool) (rest : List Bool)
    {x y : L.Total}
    (c : NativeC60AXStep (nativeC60BCClosedSignature S F) x y) :
    nativeC60BCMapClosedStep S F (side :: rest) c =
      nativeC60BCMapClosedStep S F [side]
        (nativeC60BCMapClosedStep S F rest c) := by
  induction c with
  | atom g =>
      change NativeC60AXStep.atom (nativeC60BCShiftGen S F (side :: rest) g) =
        NativeC60AXStep.atom
          (nativeC60BCShiftGen S F [side] (nativeC60BCShiftGen S F rest g))
      rw [nativeC60BEShiftGen_cons S F side rest g]
      rfl
  | refl _ => rfl
  | symm c ih =>
      change NativeC60AXStep.symm (nativeC60BCMapClosedStep S F (side :: rest) c) =
        NativeC60AXStep.symm
          (nativeC60BCMapClosedStep S F [side]
            (nativeC60BCMapClosedStep S F rest c))
      rw [ih]
      rfl
  | trans c d ih ik =>
      change NativeC60AXStep.trans (nativeC60BCMapClosedStep S F (side :: rest) c)
          (nativeC60BCMapClosedStep S F (side :: rest) d) =
        NativeC60AXStep.trans
          (nativeC60BCMapClosedStep S F [side]
            (nativeC60BCMapClosedStep S F rest c))
          (nativeC60BCMapClosedStep S F [side]
            (nativeC60BCMapClosedStep S F rest d))
      rw [ih, ik]
      rfl

/-- The carrier keeps BOTH original 15D endpoints and the full
strict 16D arrow. It is the previously proved BA arrow bundle. -/
abbrev NativeC60BEStrictArrowBundle {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L) :=
  NativeC60BAStrictArrows (nativeC60BCClosedSignature S F)
    (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))

/-- An ACTUAL endomorphism of the exact-boundary strict-arrow bundle.
The arrow itself is transported by BD's genuine strict endofunctor. -/
def nativeC60BEArrowContext {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (steps : List Bool) :
    NativeC60BEStrictArrowBundle S F → NativeC60BEStrictArrowBundle S F :=
  fun q => ⟨(nativeC60BCContextTotal F steps q.1.1,
      nativeC60BCContextTotal F steps q.1.2),
    (nativeC60BDNoRelations_strictFunctor S F steps).map q.2⟩

/-- The full bundle action reads the strict realization of the actual
transported raw higher term, not a scalar evaluation. -/
theorem nativeC60BEArrowContext_realize {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (steps : List Bool)
    {x y : L.Total}
    (c : NativeC60AXStep (nativeC60BCClosedSignature S F) x y) :
    nativeC60BEArrowContext S F steps
        ⟨(x, y), nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
            (nativeC60AZNoRelations (nativeC60BCClosedSignature S F)) c⟩ =
      ⟨(nativeC60BCContextTotal F steps x,
          nativeC60BCContextTotal F steps y),
        nativeC60AZStrictStep (nativeC60BCClosedSignature S F)
          (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
          (nativeC60BCMapClosedStep S F steps c)⟩ := by
  exact congrArg (fun k =>
      (⟨(nativeC60BCContextTotal F steps x, nativeC60BCContextTotal F steps y), k⟩ :
        NativeC60BEStrictArrowBundle S F))
      (nativeC60BDStrictContext_step S F
        (nativeC60AZNoRelations (nativeC60BCClosedSignature S F))
        steps (nativeC60BDNoRelations_context S F steps) c)

/-- The empty context is the identity on ALL strict arrows, not just
on the earlier BD object assignments. -/
theorem nativeC60BEArrowContext_nil {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (q : NativeC60BEStrictArrowBundle S F) :
    nativeC60BEArrowContext S F [] q = q := by
  rcases q with ⟨⟨x, y⟩, f⟩
  obtain ⟨c, rfl⟩ := nativeC60BAStep_surjective
    (nativeC60BCClosedSignature S F)
    (nativeC60AZNoRelations (nativeC60BCClosedSignature S F)) x y f
  rw [nativeC60BEArrowContext_realize, nativeC60BEMapClosedStep_nil]
  rfl

/-- The crucial one-step full-arrow equation. The two context actions
have exactly the same dependent endpoints, and the hom equation uses
the honest free 16D comparison, never an implicit scalar quotient. -/
theorem nativeC60BEArrowContext_cons {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (side : Bool) (rest : List Bool)
    (q : NativeC60BEStrictArrowBundle S F) :
    nativeC60BEArrowContext S F (side :: rest) q =
      nativeC60BEArrowContext S F [side]
        (nativeC60BEArrowContext S F rest q) := by
  rcases q with ⟨⟨x, y⟩, f⟩
  obtain ⟨c, rfl⟩ := nativeC60BAStep_surjective
    (nativeC60BCClosedSignature S F)
    (nativeC60AZNoRelations (nativeC60BCClosedSignature S F)) x y f
  rw [nativeC60BEArrowContext_realize S F rest]
  rw [nativeC60BEArrowContext_realize S F [side]]
  rw [nativeC60BEArrowContext_realize S F (side :: rest)]
  rw [nativeC60BEMapClosedStep_cons S F side rest c]
  rfl

/-- ONE proof by finite-context induction: genuine full-arrow action
on the strict Kuu quotient obeys concatenation in the correct order. -/
theorem nativeC60BEArrowContext_append {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (outer inner : List Bool) (q : NativeC60BEStrictArrowBundle S F) :
    nativeC60BEArrowContext S F (outer ++ inner) q =
      nativeC60BEArrowContext S F outer
        (nativeC60BEArrowContext S F inner q) := by
  induction outer with
  | nil =>
      change nativeC60BEArrowContext S F inner q =
        nativeC60BEArrowContext S F []
          (nativeC60BEArrowContext S F inner q)
      exact (nativeC60BEArrowContext_nil S F _).symm
  | cons side rest ih =>
      calc
        nativeC60BEArrowContext S F ((side :: rest) ++ inner) q =
          nativeC60BEArrowContext S F [side]
            (nativeC60BEArrowContext S F (rest ++ inner) q) :=
              nativeC60BEArrowContext_cons S F side (rest ++ inner) q
        _ = nativeC60BEArrowContext S F [side]
              (nativeC60BEArrowContext S F rest
                (nativeC60BEArrowContext S F inner q)) :=
              congrArg (nativeC60BEArrowContext S F [side]) ih
        _ = nativeC60BEArrowContext S F (side :: rest)
              (nativeC60BEArrowContext S F inner q) :=
              (nativeC60BEArrowContext_cons S F side rest _).symm

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

/-- Real original C60 14D whiskering gives a strict full-arrow action
for arbitrary finite words, not merely objects of its strict category. -/
def nativeK5BEPhysicalArrowContext (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool) :
    NativeC60BEStrictArrowBundle
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W) →
    NativeC60BEStrictArrowBundle
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W) :=
  nativeC60BEArrowContext (nativeK5AXKuuSignature W) (nativeK5BCFrame W) word

theorem nativeK5BEPhysicalArrowContext_append
    (W : NativeK5StructuralThirteenCell p U V)
    (outer inner : List Bool)
    (q : NativeC60BEStrictArrowBundle
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)) :
    nativeK5BEPhysicalArrowContext W (outer ++ inner) q =
      nativeK5BEPhysicalArrowContext W outer
        (nativeK5BEPhysicalArrowContext W inner q) :=
  nativeC60BEArrowContext_append
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W) outer inner q

/-- Every finite context preserves actual noncommutative AS Peiffer
values of each of the *two* original endpoints of a strict arrow. -/
theorem nativeK5BEPhysicalArrowContext_source_peiffer
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool)
    (q : NativeC60BEStrictArrowBundle
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)) :
    nativeK5AXPeiffer W (nativeK5BEPhysicalArrowContext W word q).1.1 =
      nativeK5ASPeifferAct W (nativeK5ATGaugeWord W word)
        (nativeK5AXPeiffer W q.1.1) :=
  nativeK5BCContext_peiffer W word q.1.1

theorem nativeK5BEPhysicalArrowContext_target_peiffer
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool)
    (q : NativeC60BEStrictArrowBundle
      (nativeK5AXKuuSignature W) (nativeK5BCFrame W)) :
    nativeK5AXPeiffer W (nativeK5BEPhysicalArrowContext W word q).1.2 =
      nativeK5ASPeifferAct W (nativeK5ATGaugeWord W word)
        (nativeK5AXPeiffer W q.1.2) :=
  nativeK5BCContext_peiffer W word q.1.2

end PhysicalC60

#print axioms nativeC60BEShiftGen_nil
#print axioms nativeC60BEShiftGen_cons
#print axioms nativeC60BEMapClosedStep_nil
#print axioms nativeC60BEMapClosedStep_cons
#print axioms NativeC60BEStrictArrowBundle
#print axioms nativeC60BEArrowContext
#print axioms nativeC60BEArrowContext_realize
#print axioms nativeC60BEArrowContext_nil
#print axioms nativeC60BEArrowContext_cons
#print axioms nativeC60BEArrowContext_append
#print axioms nativeK5BEPhysicalArrowContext
#print axioms nativeK5BEPhysicalArrowContext_append
#print axioms nativeK5BEPhysicalArrowContext_source_peiffer
#print axioms nativeK5BEPhysicalArrowContext_target_peiffer

end
end Kuu.F112.Physical
