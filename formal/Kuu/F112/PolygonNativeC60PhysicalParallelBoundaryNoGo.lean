import Kuu.F112.PolygonNativeC60PhysicalGeneratorFrameObstruction

/-!
# F112-P94D3BK — original C60 parallel-boundary obstruction to naive binary gluing

BJ proves physical nonvanishing of the original Peiffer normal-kernel
element through all two-sided fourteen-dimensional contexts. BK locates a
separate and strictly stronger *typing* constraint at the actual fifteen-
to-sixteen-dimensional interface.

For every finite word of the TWO GENUINE AQ fourteen-cell whiskerings:
* the actual fifteen-cell exchange has unequal original fourteen-cell
  source and target history words;
* the exchange and its formal inverse have SWAPPED dependent boundaries;
* therefore NO typed sixteen-cell comparison between them can exist in
  ANY AX signature over the original source-dependent physical layer;
* the same pair has NO strict arrow or strict isomorphism in ANY Kuu
  category formed with independently chosen parallel replacement laws.

These assertions are about actual original 14D/15D boundaries; they
do NOT merely assert that two raw proof expressions are distinct.
The empty-word case also excludes treating original fifteen-cell
vertical composition as an everywhere-composable binary operation.

In contrast, AU's two 15D naturality routes have EXACTLY parallel
14D boundaries and an actually ADJOINED typed 16D comparison in the
BC context-closed presentation, despite remaining distinct raw terms.
Thus the negative result is a precise *nonparallel* no-go and is NOT
a prohibition on all horizontal whiskering or a global 16-cell no-go.

No Gray, fabricated geometry, observer-kernel quotient, new axiom,
sorry or admit.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u v uD vD uE vE

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

/-- The real 15D source-dependent exchange in a genuine finite 14D
physical context, keeping both different 14D endpoints in a sigma. -/
def nativeK5BKExchangeForward
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool) : (nativeK5AXBaseLayer W).Total :=
  nativeK5AXPack W (nativeK5AQExchange W word)

/-- The actual syntactic inverse 15D witness. Its exact original
fourteen-dimensional source and target are REVERSED, not forgotten. -/
def nativeK5BKExchangeBackward
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool) : (nativeK5AXBaseLayer W).Total :=
  nativeK5AXPack W (.symm (nativeK5AQExchange W word))

/-- Every true physical exchange at any finite original 14D context
is a NON-LOOP at the exact unquotiented source-dependent boundary. -/
theorem nativeK5BKExchange_not_loop
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool) :
    (nativeK5BKExchangeForward W word).1.1 ≠
      (nativeK5BKExchangeForward W word).1.2 := by
  intro h
  have heq :
      (nativeK5AQLeft W word).historyWord =
        (nativeK5AQRight W word).historyWord :=
    congrArg
      (fun c : (nativeK5AXBaseLayer W).Obj => c.down.historyWord) h
  exact (nativeK5AQBoundary_history_ne W word) heq

/-- The forward exchange and its reverse have DIFFERENT original
14D source-target PAIRS. The obstruction is physical free-history
separation, rather than distinctness of parenthesized proof syntax. -/
theorem nativeK5BKExchange_boundary_ne
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool) :
    (nativeK5BKExchangeForward W word).1 ≠
      (nativeK5BKExchangeBackward W word).1 := by
  intro h
  have heq :
      (nativeK5AQLeft W word).historyWord =
        (nativeK5AQRight W word).historyWord :=
    congrArg
      (fun z : (nativeK5AXBaseLayer W).Obj ×
          (nativeK5AXBaseLayer W).Obj => z.1.down.historyWord) h
  exact (nativeK5AQBoundary_history_ne W word) heq

/-- Genuine no-go: no typed 16D comparison of forward versus
reversed 15D exchange, for ANY original-physical AX signature
whatsoever. Every AX step preserves its EXACT 14D boundary. -/
theorem nativeK5BKExchange_no_sixteen_cell
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool)
    (T : NativeC60AXSignature (nativeK5AXBaseLayer W)) :
    ¬ Nonempty (NativeC60AXStep T
        (nativeK5BKExchangeForward W word)
        (nativeK5BKExchangeBackward W word)) := by
  rintro ⟨cell⟩
  exact (nativeK5BKExchange_boundary_ne W word) cell.boundary

/-- No strict quotient of an original physical AX signature can
identify these two distinct 15D objects: replacement acts on arrows,
not on the faithfully retained lower source/target objects. -/
theorem nativeK5BKExchange_strict_objects_ne
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool)
    (T : NativeC60AXSignature (nativeK5AXBaseLayer W))
    (R : NativeC60AZParallelRelation T) :
    (nativeC60AZStrictProject T R).obj
        ⟨nativeK5BKExchangeForward W word⟩ ≠
      (nativeC60AZStrictProject T R).obj
        ⟨nativeK5BKExchangeBackward W word⟩ := by
  intro heq
  have h := nativeC60AZStrictObj_injective T R heq
  exact (nativeK5BKExchange_boundary_ne W word)
    (congrArg (fun x : (nativeK5AXBaseLayer W).Total => x.1) h)

/-- In fact there is NO STRICT MORPHISM from the forward exchange
to its reverse in ANY selected Kuu presentation over the original
C60 physical layer, since BA's surjection realizes every strict
morphism from an actual boundary-typed raw comparison. -/
theorem nativeK5BKExchange_no_strict_morphism
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool)
    (T : NativeC60AXSignature (nativeK5AXBaseLayer W))
    (R : NativeC60AZParallelRelation T) :
    ¬ Nonempty
      ((nativeC60AZStrictProject T R).obj
          ⟨nativeK5BKExchangeForward W word⟩ ⟶
        (nativeC60AZStrictProject T R).obj
          ⟨nativeK5BKExchangeBackward W word⟩) := by
  rintro ⟨morphism⟩
  obtain ⟨cell, _⟩ := nativeC60BAStep_surjective T R
    (nativeK5BKExchangeForward W word)
    (nativeK5BKExchangeBackward W word) morphism
  exact (nativeK5BKExchange_no_sixteen_cell W word T) ⟨cell⟩

/-- Neither can there be an isomorphism; changing the selected
parallel Kuu replacement does NOT repair the incompatible boundary. -/
theorem nativeK5BKExchange_no_strict_iso
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool)
    (T : NativeC60AXSignature (nativeK5AXBaseLayer W))
    (R : NativeC60AZParallelRelation T) :
    ¬ Nonempty
      ((nativeC60AZStrictProject T R).obj
          ⟨nativeK5BKExchangeForward W word⟩ ≅
        (nativeC60AZStrictProject T R).obj
          ⟨nativeK5BKExchangeBackward W word⟩) := by
  rintro ⟨i⟩
  exact nativeK5BKExchange_no_strict_morphism W word T R ⟨i.hom⟩

/-- A *naive*, literally vertical composition of original 15D
proofs is necessarily PARTIAL: the actual exchange itself is not a
loop, so not all pairs of full physical proof-carrying arrows have
matching end/start 14D objects. This does not rule out some OTHER,
genuine binary horizontal operation. -/
theorem nativeK5BKNo_everywhere_vertical_composability
    (W : NativeK5StructuralThirteenCell p U V) :
    ¬ ∀ (x y : (nativeK5AXBaseLayer W).Total),
        x.1.2 = y.1.1 := by
  intro h
  exact (nativeK5BKExchange_not_loop W [])
    (h (nativeK5BKExchangeForward W [])
       (nativeK5BKExchangeForward W [])).symm

/-- POSITIVE contrast: the two genuine AU 15D naturality proofs
remain DIFFERENT original raw cells, but have a NAMED TYPE-VALUED
16D comparison in the explicitly context-closed BC presentation.
That existing comparison is only for PARALLEL 14D boundaries. -/
theorem nativeK5BKParallelNaturality_has_comparison
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool) :
    let a := nativeK5BCContext W word
      (nativeK5AXPack W
        (nativeK5AUNaturalityViaSource W (nativeK5AQExchange W [])))
    let b := nativeK5BCContext W word
      (nativeK5AXPack W
        (nativeK5AUNaturalityViaTarget W (nativeK5AQExchange W [])))
    a ≠ b ∧ Nonempty (NativeC60AXStep (nativeK5BCSignature W) a b) := by
  dsimp
  exact ⟨nativeK5BCContextualPacked_raw_ne W word,
    ⟨nativeK5BCContextualNaturality W word (nativeK5AQExchange W [])⟩⟩

/-- The ACTUAL AU comparison witnesses equality of the exact original
14D pair, while the raw 15D proof objects stay separate.
No nonparallel pseudo-filler is invented in either direction. -/
theorem nativeK5BKParallelNaturality_boundary
    (W : NativeK5StructuralThirteenCell p U V)
    (word : List Bool) :
    (nativeK5BCContext W word
      (nativeK5AXPack W
        (nativeK5AUNaturalityViaSource W (nativeK5AQExchange W [])))).1 =
    (nativeK5BCContext W word
      (nativeK5AXPack W
        (nativeK5AUNaturalityViaTarget W (nativeK5AQExchange W [])))).1 :=
  (nativeK5BCContextualNaturality W word
    (nativeK5AQExchange W [])).boundary

end OriginalC60

#print axioms nativeK5BKExchangeForward
#print axioms nativeK5BKExchangeBackward
#print axioms nativeK5BKExchange_not_loop
#print axioms nativeK5BKExchange_boundary_ne
#print axioms nativeK5BKExchange_no_sixteen_cell
#print axioms nativeK5BKExchange_strict_objects_ne
#print axioms nativeK5BKExchange_no_strict_morphism
#print axioms nativeK5BKExchange_no_strict_iso
#print axioms nativeK5BKNo_everywhere_vertical_composability
#print axioms nativeK5BKParallelNaturality_has_comparison
#print axioms nativeK5BKParallelNaturality_boundary

end
end Kuu.F112.Physical
