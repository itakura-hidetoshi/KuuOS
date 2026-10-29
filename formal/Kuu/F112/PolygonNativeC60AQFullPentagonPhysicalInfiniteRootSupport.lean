import Kuu.F112.PolygonNativeC60AQFullPentagonClosedBoundaryKeyExactReflection

/-!
# F112-P94D3FU — actual arbitrarily deep physical 18D collision tower

FR proved that the whole actual DV kernel is normally generated
by collisions internal to the EXACT recursive assoc/post/pre spine.
FT made the genuine receiving dependent 18D boundary key complete.

FU exhibits actual, explicit, ORIGINAL fully dependent 18D source
code collisions at EVERY post-whiskering recursion depth:
  * for EACH original 17D object a, build the original
    (.post)^n (.assoc refl refl refl) generator, whiskering with the
    genuine original 17D identity at each step;
  * prove its complete original source remains a, its complete
    constructor spine has length n+1, and its actual DV code
    transport is natural under ANY context-object collision a,b;
  * FJ's two actually distinct original 15D/17D proof histories
    hence yield distinct original 18D source letters with the
    SAME real context-closed target code for every n and every
    nonempty genuine finite physical C60 AQ word;
  * from each such collision select an actual non-root letter in
    the FQ/FS image fiber; chosen active letters at different
    depths are distinct, giving an injection Nat into the ACTUAL
    active-root-support subtype, hence that subtype is infinite.

This is a strict quantitative structural advance: nontrivial
root-fiber source LETTERS exist at every original recursion depth
without ANY finite-depth cutoff. It is NOT by itself a proof that
the whole normal kernel is not finitely normally generated: a
different finite family of group WORD relators might generate
all those two-letter relations via conjugation. Do not confuse
infinitely many relators with independent normal generators.
No FJ single-defect whole-kernel claim, no genuine geometric
19D filler, new Gray/strict n-category/hyperdescent. Retain
all old Type-valued 14D-18D proofs, DS/FJ/FN no-go, separate
FK/FL/FM presentation, 107 public roots, pinned Lean/mathlib
and strict Kuu primary / independent Kuu presentation.
Append-only, no new axioms/sorry/admit.
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

section GenuinePostTower

variable {L : NativeC60AXLayer.{u}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- The source raw17D bracketed path of n actual post-whiskerings,
with every original Type-valued endpoint still equal to a. -/
def nativeC60FUTowerLeft
    (a : (nativeC60DQSeventeenLayer S F).Total) :
    Nat → NativeC60FGOriginal17Step S F a a
  | 0 => .trans (.trans (.refl a) (.refl a)) (.refl a)
  | n + 1 => .trans (nativeC60FUTowerLeft a n) (.refl a)

/-- Distinct right-bracketed raw17D target at each recursive depth. -/
def nativeC60FUTowerRight
    (a : (nativeC60DQSeventeenLayer S F).Total) :
    Nat → NativeC60FGOriginal17Step S F a a
  | 0 => .trans (.refl a) (.trans (.refl a) (.refl a))
  | n + 1 => .trans (nativeC60FUTowerRight a n) (.refl a)

/-- Genuine typed original DR 18D generator with arbitrary n nested
post constructors; the inner dependent source and target remain
ACTUAL entire original raw17D proof objects. -/
def nativeC60FUTowerGen
    (a : (nativeC60DQSeventeenLayer S F).Total) :
    (n : Nat) →
      (nativeC60DREighteenAssocSignature S F).Gen
        (nativeC60DRPackSeventeen S F (nativeC60FUTowerLeft S F a n))
        (nativeC60DRPackSeventeen S F (nativeC60FUTowerRight S F a n))
  | 0 => .assoc (.refl a) (.refl a) (.refl a)
  | n + 1 => .post (nativeC60FUTowerGen a n) (.refl a)

/-- An ORIGINAL complete dependent 18D code, not a charge,
abelian quotient, lower graph generator, or a new filler. -/
def nativeC60FUTowerCode
    (a : (nativeC60DQSeventeenLayer S F).Total) (n : Nat) :
    NativeC60DSCompleteEighteenCode S F :=
  nativeC60DSCode S F (nativeC60FUTowerGen S F a n)

/-- A tower code remembers its original (and possibly nonfaithful)
lower 17D Type-valued object at EVERY depth. -/
theorem nativeC60FUTowerCode_source
    (a : (nativeC60DQSeventeenLayer S F).Total) (n : Nat) :
    (nativeC60FUTowerCode S F a n).1.1.1 = a := rfl

/-- In a fixed recursion depth, different 17D raw proof objects
are genuinely different ORIGINAL complete 18D source letters. -/
theorem nativeC60FUTowerCode_injective (n : Nat) :
    Function.Injective (fun a : (nativeC60DQSeventeenLayer S F).Total =>
      nativeC60FUTowerCode S F a n) := by
  intro a b h
  have ha := congrArg
    (fun z : NativeC60DSCompleteEighteenCode S F => z.1.1.1) h
  exact ha

/-- The full ORIGINAL assoc/post/... constructor depth is exactly
n+1, so no two tower codes of distinct recursion depths coincide. -/
theorem nativeC60FUTowerCode_depth
    (a : (nativeC60DQSeventeenLayer S F).Total) :
    ∀ n : Nat,
      nativeC60FIOriginalCodeDepth S F
        (nativeC60FUTowerCode S F a n) = n + 1
  | 0 => rfl
  | n + 1 => by
      change
        (nativeC60FIOriginalCodeSpine S F
          (nativeC60FUTowerCode S F a n)).length + 1 =
          (n + 1) + 1
      exact congrArg Nat.succ (nativeC60FUTowerCode_depth a n)

/-- Naturality of EACH full post-whiskered original 18D code
collision: if the ACTUAL true DR 17D context maps a,b to equal
source objects, every post-recursion depth gives equal receiving
18D complete codes, without assuming injectivity of the frame. -/
theorem nativeC60FUTowerCode_collision
    (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (hab : nativeC60BCContextTotal
        (nativeC60DRSeventeenFrame S F) word a =
      nativeC60BCContextTotal
        (nativeC60DRSeventeenFrame S F) word b) :
    ∀ n : Nat,
      nativeC60DVTransportCompleteCode S F word
          (nativeC60FUTowerCode S F a n) =
        nativeC60DVTransportCompleteCode S F word
          (nativeC60FUTowerCode S F b n)
  | 0 => nativeC60FDContextCollision_codes S F word hab
  | n + 1 => by
      have hinner := nativeC60FUTowerCode_collision word hab n
      have hsuf :
          nativeC60DVPackClosedSeventeen S F
              (NativeC60AXStep.refl
                (nativeC60BCContextTotal
                  (nativeC60DRSeventeenFrame S F) word a)) =
            nativeC60DVPackClosedSeventeen S F
              (NativeC60AXStep.refl
                (nativeC60BCContextTotal
                  (nativeC60DRSeventeenFrame S F) word b)) :=
        congrArg (fun x => nativeC60DVPackClosedSeventeen S F
          (NativeC60AXStep.refl x)) hab
      exact nativeC60FTClosedPostCode_congr S F hinner hsuf

/-- At every n a genuine lower 17D context collision produces
distinct ORIGINAL full dependent 18D letters with equal true
context-CLOSED 18D code images. -/
theorem nativeC60FUTowerCode_distinct_collision
    (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (hne : a ≠ b)
    (hab : nativeC60BCContextTotal
        (nativeC60DRSeventeenFrame S F) word a =
      nativeC60BCContextTotal
        (nativeC60DRSeventeenFrame S F) word b)
    (n : Nat) :
    nativeC60FUTowerCode S F a n ≠
        nativeC60FUTowerCode S F b n ∧
      nativeC60DVTransportCompleteCode S F word
          (nativeC60FUTowerCode S F a n) =
        nativeC60DVTransportCompleteCode S F word
          (nativeC60FUTowerCode S F b n) :=
  ⟨fun h => hne (nativeC60FUTowerCode_injective S F n h),
    nativeC60FUTowerCode_collision S F word hab n⟩

/-- Choose one truly non-root original 18D letter from each actual
colliding tower pair, without assuming decidable equality of the
entire dependent generator syntax. -/
noncomputable def nativeC60FUActiveTowerLetter
    (word : List Bool)
    (a b : (nativeC60DQSeventeenLayer S F).Total)
    (n : Nat) : NativeC60DSCompleteEighteenCode S F := by
  classical
  exact if nativeC60FUTowerCode S F a n =
      nativeC60FQLetterRoot
        (nativeC60DVTransportCompleteCode S F word)
        (nativeC60FUTowerCode S F a n)
    then nativeC60FUTowerCode S F b n
    else nativeC60FUTowerCode S F a n

/-- The chosen code is an ACTUAL nontrivial fiber-root letter in
the exact original 18D code alphabet at the specified finite word. -/
theorem nativeC60FUActiveTowerLetter_mem
    (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (hne : a ≠ b)
    (hab : nativeC60BCContextTotal
        (nativeC60DRSeventeenFrame S F) word a =
      nativeC60BCContextTotal
        (nativeC60DRSeventeenFrame S F) word b)
    (n : Nat) :
    nativeC60FUActiveTowerLetter S F word a b n ∈
      nativeC60FSActiveLetters
        (nativeC60DVTransportCompleteCode S F word) := by
  classical
  have hcodes := nativeC60FUTowerCode_distinct_collision S F word hne hab n
  have hroots :=
    nativeC60FQLetterRoot_eq_of_image_eq
      (nativeC60DVTransportCompleteCode S F word) hcodes.2
  by_cases hleft : nativeC60FUTowerCode S F a n =
      nativeC60FQLetterRoot
        (nativeC60DVTransportCompleteCode S F word)
        (nativeC60FUTowerCode S F a n)
  · have hright : nativeC60FUTowerCode S F b n ≠
        nativeC60FQLetterRoot
          (nativeC60DVTransportCompleteCode S F word)
          (nativeC60FUTowerCode S F b n) := by
      intro hr
      exact hcodes.1 (hleft.trans (hroots.trans hr.symm))
    simpa only [nativeC60FUActiveTowerLetter, if_pos hleft,
      nativeC60FSActiveLetters, Set.mem_setOf_eq] using hright
  · simpa only [nativeC60FUActiveTowerLetter, if_neg hleft,
      nativeC60FSActiveLetters, Set.mem_setOf_eq] using hleft

/-- The selected non-root code has the SAME exact original recursive
depth n+1 as both its witness letters; the selection never changes
a full assoc/post/pre recursion spine or invents a new code. -/
theorem nativeC60FUActiveTowerLetter_depth
    (word : List Bool)
    (a b : (nativeC60DQSeventeenLayer S F).Total)
    (n : Nat) :
    nativeC60FIOriginalCodeDepth S F
      (nativeC60FUActiveTowerLetter S F word a b n) = n + 1 := by
  classical
  by_cases hleft : nativeC60FUTowerCode S F a n =
      nativeC60FQLetterRoot
        (nativeC60DVTransportCompleteCode S F word)
        (nativeC60FUTowerCode S F a n)
  · simpa only [nativeC60FUActiveTowerLetter, if_pos hleft]
      using nativeC60FUTowerCode_depth S F b n
  · simpa only [nativeC60FUActiveTowerLetter, if_neg hleft]
      using nativeC60FUTowerCode_depth S F a n

/-- No nontrivial original lower 17D context collision can occur
at only FINITELY many active 18D post-whiskering depths.
We inject Nat into the ACTUAL dependent code-fiber active subtype,
using exact original source recursion depth as the separation
certificate. No non-finite normal rank is claimed here. -/
theorem nativeC60FUActiveSupport_infinite_of_context_collision
    (word : List Bool)
    {a b : (nativeC60DQSeventeenLayer S F).Total}
    (hne : a ≠ b)
    (hab : nativeC60BCContextTotal
        (nativeC60DRSeventeenFrame S F) word a =
      nativeC60BCContextTotal
        (nativeC60DRSeventeenFrame S F) word b) :
    Infinite (nativeC60FSActiveLetters
      (nativeC60DVTransportCompleteCode S F word)) := by
  let c : Nat → nativeC60FSActiveLetters
      (nativeC60DVTransportCompleteCode S F word) :=
    fun n => ⟨nativeC60FUActiveTowerLetter S F word a b n,
      nativeC60FUActiveTowerLetter_mem S F word hne hab n⟩
  have hc : Function.Injective c := by
    intro n m h
    have hdepth := congrArg
      (fun z : nativeC60FSActiveLetters
        (nativeC60DVTransportCompleteCode S F word) =>
          nativeC60FIOriginalCodeDepth S F z.1) h
    change nativeC60FIOriginalCodeDepth S F
        (nativeC60FUActiveTowerLetter S F word a b n) =
      nativeC60FIOriginalCodeDepth S F
        (nativeC60FUActiveTowerLetter S F word a b m) at hdepth
    rw [nativeC60FUActiveTowerLetter_depth S F word a b n,
      nativeC60FUActiveTowerLetter_depth S F word a b m] at hdepth
    omega
  exact Infinite.of_injective c hc

end GenuinePostTower

section ActualPhysicalInfiniteActiveSupport

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

/-- At EVERY original full 18D post recursion depth, the two
DISTINCT FJ physical source terms have the SAME full dependent
receiving code under EVERY nonempty genuine finite C60 AQ word. -/
theorem nativeK5FUTowerPhysical_distinct_collision
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (word : List Bool) (hne : word ≠ []) (depth : Nat) :
    nativeC60FUTowerCode (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W) (nativeK5FJSeventeenRefl W R) depth ≠
      nativeC60FUTowerCode (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W) (nativeK5FJSeventeenAtom W R) depth ∧
    nativeC60DVTransportCompleteCode (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W) word
        (nativeC60FUTowerCode (nativeK5AXKuuSignature W)
          (nativeK5BCFrame W) (nativeK5FJSeventeenRefl W R) depth) =
      nativeC60DVTransportCompleteCode (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W) word
        (nativeC60FUTowerCode (nativeK5AXKuuSignature W)
          (nativeK5BCFrame W) (nativeK5FJSeventeenAtom W R) depth) :=
  nativeC60FUTowerCode_distinct_collision
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
    word (nativeK5FJSeventeenRefl_ne_atom W R)
    (nativeK5FJPhysical_nonempty_context_collision W R word hne) depth

/-- PHYSICAL RESULT. Every genuine nonempty finite original C60
AQ context has an INFINITE subtype of source 18D complete code
letters different from their chosen actual-image fiber root.
A direct Nat injection is carried by the original nested post
constructor depth. No inference of infinite normal generating
rank is smuggled into this statement. -/
theorem nativeK5FUPhysical_activeSource_infinite
    (W : NativeK5StructuralThirteenCell p U V)
    (R : NativeK5FifteenFourteenFiber W)
    (word : List Bool) (hne : word ≠ []) :
    Infinite (nativeC60FSActiveLetters
      (nativeC60DVTransportCompleteCode (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W) word)) :=
  nativeC60FUActiveSupport_infinite_of_context_collision
    (nativeK5AXKuuSignature W) (nativeK5BCFrame W)
    word (nativeK5FJSeventeenRefl_ne_atom W R)
    (nativeK5FJPhysical_nonempty_context_collision W R word hne)

/-- No arbitrary new physical source fiber is needed: the
existing canonical inhabited original 14D critical left fiber
already yields infinitely many active root letters in EVERY
nonempty original C60 AQ physical word. -/
theorem nativeK5FUPhysical_canonicalActiveSource_infinite
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool) (hne : word ≠ []) :
    Infinite (nativeC60FSActiveLetters
      (nativeC60DVTransportCompleteCode (nativeK5AXKuuSignature W)
        (nativeK5BCFrame W) word)) :=
  nativeK5FUPhysical_activeSource_infinite W
    (nativeK5FifteenCriticalLeft W) word hne

end ActualPhysicalInfiniteActiveSupport

#print axioms nativeC60FUTowerCode_source
#print axioms nativeC60FUTowerCode_injective
#print axioms nativeC60FUTowerCode_depth
#print axioms nativeC60FUTowerCode_collision
#print axioms nativeC60FUTowerCode_distinct_collision
#print axioms nativeC60FUActiveTowerLetter_mem
#print axioms nativeC60FUActiveTowerLetter_depth
#print axioms nativeC60FUActiveSupport_infinite_of_context_collision
#print axioms nativeK5FUTowerPhysical_distinct_collision
#print axioms nativeK5FUPhysical_activeSource_infinite
#print axioms nativeK5FUPhysical_canonicalActiveSource_infinite

end
end Kuu.F112.Physical
