import Kuu.F112.PolygonNativeC60SeventeenContextEighteenAssociator

/-!
# F112-P94D3DS — full noncommutative 18D evidence and exact 19D pentagon gate

DR constructs two independent, genuinely dependent raw18D routes around
the four-input pentagon of actual raw17D triangle paths. Neither DR nor
the selected DQ17D/DR18D PRESENTATION grants a geometric 19D filler.

DS provides a STRICTER certificate:
* The FULL original 18D generator with both actual raw17D source and
  target witnesses is made a dependent sigma code. Nested in each code
  are all original 14D, 15D, 16D and 17D proof witnesses.
* The universal noncommutative FreeGroup of THESE exact generator codes
  interprets arbitrary signed raw18D paths, not their parity or a scalar.
* The pentagon long route is its THREE-LETTER positive word, and the
  short route its TWO-LETTER positive word. Reduced-word uniqueness
  proves the two complete free words unequal for ALL four actual
  composable 17D paths, with no separation hypothesis on the letters.
  The length mismatch is detected IN THE FREE GROUP itself, not used
  to define a lossy observer quotient.
* The complete receiver descends to the original selected strict Kuu
  quotient with NO EXTRA 18D equations. Hence even strict equality of
  the long and short 18D arrows is prohibited there.
* An arbitrary candidate NEXT 19D Type-valued signature admits a
  pentagon filling path ONLY IF it abandons preservation of the full
  original 18D noncommutative evidence. This is an exact obstruction
  for any signature which preserves every original generator code.
* For clarity we ALSO CONSTRUCT a separately DECLARED relative
  19D pentagon generator, preserving the true dependent boundaries
  while proving that its new signature cannot preserve the original
  complete free receiver. This is NOT a claimed original geometric
  C60 19-cell and does not prove any unselected higher coherence.

All original nonparallel boundary no-go theorems, C60 14D/15D/16D/17D
proof histories, higher strict/independent Kuu distinction, 107 public
roots and no-Gray rule remain. No sorry, admit, new logical axioms,
silent quotient or claimed physical 19D existence.
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

/-- WHOLE Type-valued 18D generator certificate code. Its two dependent
17D boundaries are retained alongside the actual native 18D generator,
whose own constructors recursively store the original 16D/15D history. -/
abbrev NativeC60DSCompleteEighteenCode
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L) : Type u :=
  Σ x : (nativeC60DREighteenLayer S F).Total,
    Σ y : (nativeC60DREighteenLayer S F).Total,
      (nativeC60DREighteenAssocSignature S F).Gen x y

/-- Record the complete typed generator, not its code length, Peiffer
value, parity, or a graph edge label. -/
def nativeC60DSCode
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {x y : (nativeC60DREighteenLayer S F).Total}
    (g : (nativeC60DREighteenAssocSignature S F).Gen x y) :
    NativeC60DSCompleteEighteenCode S F :=
  ⟨x, y, g⟩

/-- Full generator code is faithful at the ORIGINAL dependent source
and target. No generator identification is silently built in. -/
theorem nativeC60DSCode_injective
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {x y : (nativeC60DREighteenLayer S F).Total} :
    Function.Injective (fun (g : (nativeC60DREighteenAssocSignature S F).Gen x y) =>
      nativeC60DSCode S F g) := by
  intro g h heq
  have hpair : (⟨y, g⟩ : Σ z : (nativeC60DREighteenLayer S F).Total,
      (nativeC60DREighteenAssocSignature S F).Gen x z) =
      ⟨y, h⟩ := eq_of_heq (Sigma.mk.inj heq).2
  exact eq_of_heq (Sigma.mk.inj hpair).2

/-- Each original 18D primitive is sent to its own independent
noncommutative free letter, with all 17D/16D dependent evidence. -/
def nativeC60DSFreeWeight
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L) :
    ∀ {x y : (nativeC60DREighteenLayer S F).Total},
      (nativeC60DREighteenAssocSignature S F).Gen x y →
        FreeGroup (NativeC60DSCompleteEighteenCode S F) :=
  fun {_ _} g => FreeGroup.of (nativeC60DSCode S F g)

/-- Universal COMPLETE signed noncommutative full-evidence word of
arbitrary actual raw18D paths. Reversal and ordered composition
are carried by the genuine FreeGroup interpretation. -/
def nativeC60DSFreeWord
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {x y : (nativeC60DREighteenLayer S F).Total}
    (p : NativeC60AXStep (nativeC60DREighteenAssocSignature S F) x y) :
    FreeGroup (NativeC60DSCompleteEighteenCode S F) :=
  nativeC60AZHolonomy (nativeC60DREighteenAssocSignature S F)
    (nativeC60DSFreeWeight S F) p

/-- The source/target of an 18D atom is encoded into its full free
group letter, and no scalar projection is used. -/
theorem nativeC60DSFreeWord_atom
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {x y : (nativeC60DREighteenLayer S F).Total}
    (g : (nativeC60DREighteenAssocSignature S F).Gen x y) :
    nativeC60DSFreeWord S F (.atom g) =
      FreeGroup.of (nativeC60DSCode S F g) := rfl

/-- The true signed and noncommutative composition law for actual
18D proof syntax, before any structural quotient is taken. -/
theorem nativeC60DSFreeWord_trans
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {x y z : (nativeC60DREighteenLayer S F).Total}
    (p : NativeC60AXStep (nativeC60DREighteenAssocSignature S F) x y)
    (q : NativeC60AXStep (nativeC60DREighteenAssocSignature S F) y z) :
    nativeC60DSFreeWord S F (.trans p q) =
      nativeC60DSFreeWord S F p * nativeC60DSFreeWord S F q := rfl

theorem nativeC60DSFreeWord_symm
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {x y : (nativeC60DREighteenLayer S F).Total}
    (p : NativeC60AXStep (nativeC60DREighteenAssocSignature S F) x y) :
    nativeC60DSFreeWord S F (.symm p) =
      (nativeC60DSFreeWord S F p)⁻¹ := rfl

/-- An arbitrary POSITIVE list of independent complete higher
generator codes is reduced, even if adjacent codes happen to coincide.
The positive signs make formal cancellation impossible. -/
theorem nativeC60DSPositive_reduced {α : Type u}
    (xs : List α) :
    FreeGroup.IsReduced (xs.map (fun code => (code, true))) := by
  induction xs with
  | nil =>
      exact FreeGroup.IsReduced.nil
  | cons x xs ih =>
      cases xs with
      | nil =>
          exact FreeGroup.IsReduced.singleton
      | cons y ys =>
          change FreeGroup.IsReduced
            ((x, true) :: (y, true) ::
              ys.map (fun code => (code, true)))
          rw [FreeGroup.isReduced_cons_cons]
          refine ⟨?_, ?_⟩
          · intro _
            rfl
          · exact ih

/-- Church-Rosser UNIQUE reduced representatives: equality in the
UNIVERSAL free group of actual evidence entails equality of the
ENTIRE ordered positive Type-valued generator-code list. -/
theorem nativeC60DSPositiveFree_injective {α : Type u}
    (xs ys : List α)
    (h : FreeGroup.mk (xs.map (fun code => (code, true))) =
      FreeGroup.mk (ys.map (fun code => (code, true)))) :
    xs = ys := by
  obtain ⟨red, hxs, hys⟩ := FreeGroup.Red.exact.mp h
  have hx : red = xs.map (fun code => (code, true)) :=
    (FreeGroup.IsReduced.red_iff_eq
      (nativeC60DSPositive_reduced xs)).mp hxs
  have hy : red = ys.map (fun code => (code, true)) :=
    (FreeGroup.IsReduced.red_iff_eq
      (nativeC60DSPositive_reduced ys)).mp hys
  have hwords := hx.symm.trans hy
  exact (List.map_inj_right
    (fun (a b : α) (hab : (a, true) = (b, true)) =>
      (Prod.mk.inj hab).1)).mp hwords

/-- This is a theorem in the ENTIRE free group of complete dependent
generator codes, NOT a claim that we identified the group by LENGTH.
No assumptions on equality or inequality of its five letters. -/
theorem nativeC60DSThree_positive_ne_two {α : Type u}
    (a b c d e : α) :
    FreeGroup.mk [(a, true), (b, true), (c, true)] ≠
      FreeGroup.mk [(d, true), (e, true)] := by
  intro heq
  have hcodes : ([a, b, c] : List α) = [d, e] :=
    nativeC60DSPositiveFree_injective [a, b, c] [d, e] heq
  simp at hcodes

/-- The complete free word of DR's actual LONG route is its exact
ordered THREE-generator word. Each letter carries ALL original 17D
boundary and signed 18D associator/whiskering history. -/
theorem nativeC60DSPentagon_long_free
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {a b c d e : (nativeC60DQSeventeenLayer S F).Total}
    (f : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b)
    (g : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) b c)
    (h : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) c d)
    (k : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) d e) :
    nativeC60DSFreeWord S F (nativeC60DRPentagonLong S F f g h k) =
      (FreeGroup.of (nativeC60DSCode S F
          (NativeC60DREighteenAssocGen.post (.assoc f g h) k)) *
        FreeGroup.of (nativeC60DSCode S F
          (NativeC60DREighteenAssocGen.assoc f (.trans g h) k))) *
        FreeGroup.of (nativeC60DSCode S F
          (NativeC60DREighteenAssocGen.pre f (.assoc g h k))) := rfl

/-- The complete free word of DR's SHORT route is its exact
ordered TWO-generator word; no quotient or raw syntax erasure. -/
theorem nativeC60DSPentagon_short_free
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {a b c d e : (nativeC60DQSeventeenLayer S F).Total}
    (f : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b)
    (g : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) b c)
    (h : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) c d)
    (k : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) d e) :
    nativeC60DSFreeWord S F (nativeC60DRPentagonShort S F f g h k) =
      FreeGroup.of (nativeC60DSCode S F
        (NativeC60DREighteenAssocGen.assoc (.trans f g) h k)) *
      FreeGroup.of (nativeC60DSCode S F
        (NativeC60DREighteenAssocGen.assoc f g (.trans h k))) := rfl

/-- MAIN DS: the TRUE noncommutative free words of DR's two
genuinely typed pentagon pasting routes are different, for ANY four
actual composable raw17D witnesses, including repeated witnesses.
This is strictly stronger than the earlier raw constructor inequality. -/
theorem nativeC60DSPentagon_free_ne
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {a b c d e : (nativeC60DQSeventeenLayer S F).Total}
    (f : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b)
    (g : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) b c)
    (h : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) c d)
    (k : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) d e) :
    nativeC60DSFreeWord S F (nativeC60DRPentagonLong S F f g h k) ≠
      nativeC60DSFreeWord S F (nativeC60DRPentagonShort S F f g h k) := by
  rw [nativeC60DSPentagon_long_free S F f g h k,
    nativeC60DSPentagon_short_free S F f g h k]
  change FreeGroup.mk
      [(nativeC60DSCode S F
          (NativeC60DREighteenAssocGen.post (.assoc f g h) k), true),
       (nativeC60DSCode S F
          (NativeC60DREighteenAssocGen.assoc f (.trans g h) k), true),
       (nativeC60DSCode S F
          (NativeC60DREighteenAssocGen.pre f (.assoc g h k)), true)] ≠
    FreeGroup.mk
      [(nativeC60DSCode S F
          (NativeC60DREighteenAssocGen.assoc (.trans f g) h k), true),
       (nativeC60DSCode S F
          (NativeC60DREighteenAssocGen.assoc f g (.trans h k)), true)]
  exact nativeC60DSThree_positive_ne_two _ _ _ _ _

/-- The original no-extra-relations Kuu strict quotient DOES preserve
this complete signed free evidence because it only imposes the standard
unit, composition and inverse equations of the free groupoid. -/
theorem nativeC60DSFreeWeight_respects_no_relations
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L) :
    NativeC60AZWeightsRespect
      (nativeC60DREighteenAssocSignature S F)
      (nativeC60AZNoRelations (nativeC60DREighteenAssocSignature S F))
      (nativeC60DSFreeWeight S F) := by
  intro x y p q h
  exact h.elim

/-- Full universal noncommutative receiver on the selected ORIGINAL
strict Kuu quotient (no additional 18D pentagon relations). -/
def nativeC60DSFreeStrictReceiver
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L) :
    NativeC60AZStrictSpace
        (nativeC60DREighteenAssocSignature S F)
        (nativeC60AZNoRelations
          (nativeC60DREighteenAssocSignature S F)) ⥤
      SingleObj (FreeGroup (NativeC60DSCompleteEighteenCode S F))ᵐᵒᵖ :=
  nativeC60AZStrictHolonomy
    (nativeC60DREighteenAssocSignature S F)
    (nativeC60AZNoRelations (nativeC60DREighteenAssocSignature S F))
    (nativeC60DSFreeWeight S F)
    (nativeC60DSFreeWeight_respects_no_relations S F)

/-- Exact original strict equality implies equality in the COMPLETE
free receiver, rather than only equality of a scalar or parity. -/
theorem nativeC60DSStrict_equal_implies_free_equal
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {x y : (nativeC60DREighteenLayer S F).Total}
    (p q : NativeC60AXStep (nativeC60DREighteenAssocSignature S F) x y)
    (hstrict : nativeC60AZStrictStep
        (nativeC60DREighteenAssocSignature S F)
        (nativeC60AZNoRelations (nativeC60DREighteenAssocSignature S F)) p =
      nativeC60AZStrictStep
        (nativeC60DREighteenAssocSignature S F)
        (nativeC60AZNoRelations (nativeC60DREighteenAssocSignature S F)) q) :
    nativeC60DSFreeWord S F p = nativeC60DSFreeWord S F q := by
  have hh := congrArg
    (fun m => (nativeC60DSFreeStrictReceiver S F).map m) hstrict
  change
    (nativeC60AZStrictHolonomy
      (nativeC60DREighteenAssocSignature S F)
      (nativeC60AZNoRelations (nativeC60DREighteenAssocSignature S F))
      (nativeC60DSFreeWeight S F)
      (nativeC60DSFreeWeight_respects_no_relations S F)).map
        (nativeC60AZStrictStep
          (nativeC60DREighteenAssocSignature S F)
          (nativeC60AZNoRelations (nativeC60DREighteenAssocSignature S F)) p) =
    (nativeC60AZStrictHolonomy
      (nativeC60DREighteenAssocSignature S F)
      (nativeC60AZNoRelations (nativeC60DREighteenAssocSignature S F))
      (nativeC60DSFreeWeight S F)
      (nativeC60DSFreeWeight_respects_no_relations S F)).map
        (nativeC60AZStrictStep
          (nativeC60DREighteenAssocSignature S F)
          (nativeC60AZNoRelations (nativeC60DREighteenAssocSignature S F)) q) at hh
  rw [nativeC60AZStrictHolonomy_arrow,
      nativeC60AZStrictHolonomy_arrow] at hh
  exact congrArg MulOpposite.unop hh

/-- The two original 18D routes are also DISTINCT in the SELECTED
strict Kuu quotient, not just as raw syntax and free generator words.
No geometric 19D filler was assumed or adjoined to that quotient. -/
theorem nativeC60DSPentagon_no_original_strict_equality
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {a b c d e : (nativeC60DQSeventeenLayer S F).Total}
    (f : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b)
    (g : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) b c)
    (h : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) c d)
    (k : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) d e) :
    nativeC60AZStrictStep
        (nativeC60DREighteenAssocSignature S F)
        (nativeC60AZNoRelations (nativeC60DREighteenAssocSignature S F))
        (nativeC60DRPentagonLong S F f g h k) ≠
      nativeC60AZStrictStep
        (nativeC60DREighteenAssocSignature S F)
        (nativeC60AZNoRelations (nativeC60DREighteenAssocSignature S F))
        (nativeC60DRPentagonShort S F f g h k) := by
  intro hstrict
  exact (nativeC60DSPentagon_free_ne S F f g h k)
    (nativeC60DSStrict_equal_implies_free_equal S F _ _ hstrict)

/-- At the actual NEXT 19D layer, its objects are WHOLE RAW18D
dependent path witnesses, not their strict morphisms or code lengths. -/
def nativeC60DSNineteenLayer
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L) :
    NativeC60AXLayer.{u} :=
  nativeC60AXNext (nativeC60DREighteenLayer S F)
    (nativeC60DREighteenAssocSignature S F)

/-- Store a complete Type-valued 18D path as a 19D object, with both
actual 17D endpoint histories and every 18D constructor retained. -/
def nativeC60DSPackEighteen
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {x y : (nativeC60DREighteenLayer S F).Total}
    (p : NativeC60AXStep (nativeC60DREighteenAssocSignature S F) x y) :
    (nativeC60DSNineteenLayer S F).Total :=
  ⟨(x, y), p⟩

/-- Actual full signed noncommutative 18D proof evidence carried by
each 19D lower-boundary object, without any extra receiver collapse. -/
def nativeC60DSNineteenHolonomy
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L) :
    (nativeC60DSNineteenLayer S F).Total →
      FreeGroup (NativeC60DSCompleteEighteenCode S F) :=
  fun x => nativeC60DSFreeWord S F x.2

/-- A CANDIDATE 19D signature is complete-evidence compatible iff
each of its ACTUAL declared next-dimensional generators preserves
the full original noncommutative 18D free holonomy. This is a precise
additional HYPOTHESIS, never asserted by merely selecting a quotient. -/
def NativeC60DSNineteenCompatible
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (T : NativeC60AXSignature (nativeC60DSNineteenLayer S F)) : Prop :=
  ∀ {x y : (nativeC60DSNineteenLayer S F).Total}
    (g : T.Gen x y),
      nativeC60DSNineteenHolonomy S F x =
        nativeC60DSNineteenHolonomy S F y

/-- EXACT GENERATOR TEST: compatibility of an optional 19D
presentation is EQUIVALENT to preservation of full original evidence
by EVERY finite signed, reversed and composited genuine 19D path. -/
theorem nativeC60DSNineteenCompatible_iff_all_paths
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    (T : NativeC60AXSignature (nativeC60DSNineteenLayer S F)) :
    NativeC60DSNineteenCompatible S F T ↔
      ∀ {x y : (nativeC60DSNineteenLayer S F).Total}
        (p : NativeC60AXStep T x y),
        nativeC60DSNineteenHolonomy S F x =
          nativeC60DSNineteenHolonomy S F y := by
  constructor
  · intro hc x y p
    exact NativeC60AXStep.observer_sound
      (nativeC60DSNineteenHolonomy S F)
      (by
        intro a b g
        exact hc g) p
  · intro h x y g
    exact h (.atom g)

/-- MAIN 19D OBSTRUCTION: no selected Type-valued 19D syntax whose
generators ALL preserve complete free18D provenance can supply a
pentagon filler. This quantifies over ARBITRARY hypothetical 19D
signatures and avoids incorrectly assuming an original geometric
19D cell exists. -/
theorem nativeC60DSNoCompatibleNineteenPentagonFiller
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {a b c d e : (nativeC60DQSeventeenLayer S F).Total}
    (f : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b)
    (g : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) b c)
    (h : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) c d)
    (k : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) d e)
    (T : NativeC60AXSignature (nativeC60DSNineteenLayer S F))
    (hc : NativeC60DSNineteenCompatible S F T) :
    ¬ Nonempty (NativeC60AXStep T
      (nativeC60DSPackEighteen S F (nativeC60DRPentagonLong S F f g h k))
      (nativeC60DSPackEighteen S F (nativeC60DRPentagonShort S F f g h k))) := by
  rintro ⟨p⟩
  exact (nativeC60DSPentagon_free_ne S F f g h k)
    ((nativeC60DSNineteenCompatible_iff_all_paths S F T).mp hc p)

/-- Necessary condition on EVERY 19D C60 extension:
if it DOES provide a typed pentagon-filling path, it MUST fail the
full-original-evidence generator gate. This is a conditional result,
not an assertion of physical geometric 19D existence. -/
theorem nativeC60DSAnyNineteenFiller_forces_BV_loss
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {a b c d e : (nativeC60DQSeventeenLayer S F).Total}
    (f : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b)
    (g : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) b c)
    (h : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) c d)
    (k : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) d e)
    (T : NativeC60AXSignature (nativeC60DSNineteenLayer S F))
    (p : NativeC60AXStep T
      (nativeC60DSPackEighteen S F (nativeC60DRPentagonLong S F f g h k))
      (nativeC60DSPackEighteen S F (nativeC60DRPentagonShort S F f g h k))) :
    ¬ NativeC60DSNineteenCompatible S F T := by
  intro hc
  exact (nativeC60DSNoCompatibleNineteenPentagonFiller
    S F f g h k T hc) ⟨p⟩

/-- OPTIONAL DECLARED relative 19D pentagon generator. The two
actual raw18D paths are the exact dependent source and target.
This presentation extension is EXPLICIT, not an original C60
geometric 19D filler or a theorem about an undeclared cell. -/
def nativeC60DSDeclaredPentagonNineteenSignature
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {a b c d e : (nativeC60DQSeventeenLayer S F).Total}
    (f : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b)
    (g : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) b c)
    (h : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) c d)
    (k : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) d e) :
    NativeC60AXSignature (nativeC60DSNineteenLayer S F) where
  Gen := fun x y =>
    { z : (nativeC60DSNineteenLayer S F).Total //
      z = x ∧
      x = nativeC60DSPackEighteen S F
        (nativeC60DRPentagonLong S F f g h k) ∧
      y = nativeC60DSPackEighteen S F
        (nativeC60DRPentagonShort S F f g h k) }
  boundary := by
    intro x y r
    rcases r with ⟨z, hz, hx, hy⟩
    rw [hx, hy]
    rfl

/-- The explicit relative 19D presentation does have the chosen
new primitive by construction, and nothing is postulated as a
logical axiom. The source/target 18D proof objects are ACTUAL. -/
def nativeC60DSDeclaredPentagonNineteen
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {a b c d e : (nativeC60DQSeventeenLayer S F).Total}
    (f : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b)
    (g : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) b c)
    (h : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) c d)
    (k : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) d e) :
    NativeC60AXStep
      (nativeC60DSDeclaredPentagonNineteenSignature S F f g h k)
      (nativeC60DSPackEighteen S F (nativeC60DRPentagonLong S F f g h k))
      (nativeC60DSPackEighteen S F
        (nativeC60DRPentagonShort S F f g h k)) :=
  .atom ⟨nativeC60DSPackEighteen S F
    (nativeC60DRPentagonLong S F f g h k),
    ⟨rfl, rfl, rfl⟩⟩

/-- Exact cost of explicitly ADDING this relative 19D filler:
the resulting signature CANNOT preserve the COMPLETE original
noncommutative 18D free receiver. Thus raw pentagon coherence
and all-evidence-preserving descent cannot be silently conflated. -/
theorem nativeC60DSDeclaredNineteen_forces_BV_loss
    {L : NativeC60AXLayer.{u}}
    (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)
    {a b c d e : (nativeC60DQSeventeenLayer S F).Total}
    (f : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b)
    (g : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) b c)
    (h : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) c d)
    (k : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) d e) :
    ¬ NativeC60DSNineteenCompatible S F
      (nativeC60DSDeclaredPentagonNineteenSignature S F f g h k) :=
  nativeC60DSAnyNineteenFiller_forces_BV_loss
    S F f g h k
    (nativeC60DSDeclaredPentagonNineteenSignature S F f g h k)
    (nativeC60DSDeclaredPentagonNineteen S F f g h k)

section PhysicalC60Pentagon

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

/-- Concrete genuine C60 AU physical source and arbitrary finite
AQ context TREE instantiate the FULL noncommutative 18D pentagon
obstruction, even when all four 17D paths are the SAME actual
typed AU roundtrip. The absence of an original 19D filler is
not made an axiom. -/
theorem nativeK5DSPhysicalPentagon_free_ne
    (W : NativeK5StructuralThirteenCell p U V)
    (tree : NativeK5DOContextTree) :
    let S := nativeK5AXKuuSignature W
    let F := nativeK5BCFrame W
    let gen := nativeC60BCShiftGen S F (nativeK5DOTreeWord tree)
      (nativeK5CEPhysicalAUGenerator W)
    let route := nativeC60DQSeventeenRoundtrip S F gen
    nativeC60DSFreeWord S F
        (nativeC60DRPentagonLong S F route route route route) ≠
      nativeC60DSFreeWord S F
        (nativeC60DRPentagonShort S F route route route route) := by
  dsimp only
  exact nativeC60DSPentagon_free_ne
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
    _ _ _ _

end PhysicalC60Pentagon

#print axioms NativeC60DSCompleteEighteenCode
#print axioms nativeC60DSCode
#print axioms nativeC60DSCode_injective
#print axioms nativeC60DSFreeWeight
#print axioms nativeC60DSFreeWord
#print axioms nativeC60DSFreeWord_atom
#print axioms nativeC60DSFreeWord_trans
#print axioms nativeC60DSFreeWord_symm
#print axioms nativeC60DSPositive_reduced
#print axioms nativeC60DSPositiveFree_injective
#print axioms nativeC60DSThree_positive_ne_two
#print axioms nativeC60DSPentagon_long_free
#print axioms nativeC60DSPentagon_short_free
#print axioms nativeC60DSPentagon_free_ne
#print axioms nativeC60DSFreeWeight_respects_no_relations
#print axioms nativeC60DSFreeStrictReceiver
#print axioms nativeC60DSStrict_equal_implies_free_equal
#print axioms nativeC60DSPentagon_no_original_strict_equality
#print axioms nativeC60DSNineteenLayer
#print axioms nativeC60DSPackEighteen
#print axioms nativeC60DSNineteenHolonomy
#print axioms NativeC60DSNineteenCompatible
#print axioms nativeC60DSNineteenCompatible_iff_all_paths
#print axioms nativeC60DSNoCompatibleNineteenPentagonFiller
#print axioms nativeC60DSAnyNineteenFiller_forces_BV_loss
#print axioms nativeC60DSDeclaredPentagonNineteenSignature
#print axioms nativeC60DSDeclaredPentagonNineteen
#print axioms nativeC60DSDeclaredNineteen_forces_BV_loss
#print axioms nativeK5DSPhysicalPentagon_free_ne

end
end Kuu.F112.Physical
