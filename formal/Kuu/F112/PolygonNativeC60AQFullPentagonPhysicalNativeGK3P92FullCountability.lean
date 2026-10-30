import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGK3P92Decoder

/-!
# F112-P94D3GK3 — strict original P92B source reconstruction

Countable original P92B nine-constructor Type-valued comparison, with
separate original PresentedCell and added naturality atom. Strict
decode(encode c) = some(original c) keeps all original typed evidence.
No quotient, scalar replacement, coercion to F54 StructuralSeam,
historical equivalence or unconditional original 14D inference.
Lean v4.30.0-rc2 and pinned mathlib; no Gray, no axioms, no sorry.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section
universe uD vD uE vE

/-! All recursive glue operations retain the exact original F54 boundary. -/

theorem nativeGK3P92TransExact_eq
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {n n' m m' : Nat}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s t : KuuNativeF45Tree.DepthRotationRoute p first last}
    (left : NativeF55P92AssocComparison p r s)
    (right : NativeF55P92AssocComparison p s t) :
    nativeGK3P92TransExact
      (nativeGK3PackP92 left : NativeGKOriginalP92Total p D E)
      (nativeGK3PackP92 right : NativeGKOriginalP92Total p D E) =
    some (nativeGK3PackP92 (.trans left right) :
      NativeGKOriginalP92Total p D E) := by
  simp [nativeGK3P92TransExact, nativeGK3PackP92]

theorem nativeGK3P92LeftExact_eq
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    {ma mb mc : KuuNativeBlocks a b}
    {pa pb pc : KuuNativeBlocks x y}
    {n n' m m' k l : Nat}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (cell : NativeF55P92AssocComparison p r s)
    (later : KuuNativeF45Tree p k l mb pb mc pc) :
    nativeGK3P92LeftExact
      (nativeGK3PackP92 cell : NativeGKOriginalP92Total p D E)
      (nativeGIPackTree later) =
    some (nativeGK3PackP92 (.leftContext cell later) :
      NativeGKOriginalP92Total p D E) := by
  simp [nativeGK3P92LeftExact, nativeGK3PackP92, nativeGIPackTree]

theorem nativeGK3P92RightExact_eq
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    {ma mb mc : KuuNativeBlocks a b}
    {pa pb pc : KuuNativeBlocks x y}
    {n n' m m' k l : Nat}
    (earlier : KuuNativeF45Tree p k l ma pa mb pb)
    {first : KuuNativeF45Tree p n m mb pb mc pc}
    {last : KuuNativeF45Tree p n' m' mb pb mc pc}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (cell : NativeF55P92AssocComparison p r s) :
    nativeGK3P92RightExact
      (nativeGIPackTree earlier)
      (nativeGK3PackP92 cell : NativeGKOriginalP92Total p D E) =
    some (nativeGK3PackP92 (.rightContext earlier cell) :
      NativeGKOriginalP92Total p D E) := by
  simp [nativeGK3P92RightExact, nativeGK3PackP92, nativeGIPackTree]

theorem nativeGK3P92PreExact_eq
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
    {first : KuuNativeF45Tree p n₁ m₁ ma pa mb pb}
    {middle : KuuNativeF45Tree p n₂ m₂ ma pa mb pb}
    {last : KuuNativeF45Tree p n₃ m₃ ma pa mb pb}
    (priorRoute : KuuNativeF45Tree.DepthRotationRoute p first middle)
    {r s : KuuNativeF45Tree.DepthRotationRoute p middle last}
    (cell : NativeF55P92AssocComparison p r s) :
    nativeGK3P92PreExact
      (nativeGJ2PackRoute priorRoute)
      (nativeGK3PackP92 cell : NativeGKOriginalP92Total p D E) =
    some (nativeGK3PackP92 (.precompose priorRoute cell) :
      NativeGKOriginalP92Total p D E) := by
  simp [nativeGK3P92PreExact, nativeGJ2PackRoute, nativeGK3PackP92]

theorem nativeGK3P92PostExact_eq
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {n₁ n₂ n₃ m₁ m₂ m₃ : Nat}
    {first : KuuNativeF45Tree p n₁ m₁ ma pa mb pb}
    {middle : KuuNativeF45Tree p n₂ m₂ ma pa mb pb}
    {last : KuuNativeF45Tree p n₃ m₃ ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first middle}
    (cell : NativeF55P92AssocComparison p r s)
    (suffix : KuuNativeF45Tree.DepthRotationRoute p middle last) :
    nativeGK3P92PostExact
      (nativeGK3PackP92 cell : NativeGKOriginalP92Total p D E)
      (nativeGJ2PackRoute suffix) =
    some (nativeGK3PackP92 (.postcompose cell suffix) :
      NativeGKOriginalP92Total p D E) := by
  simp [nativeGK3P92PostExact, nativeGJ2PackRoute, nativeGK3PackP92]

/-- Faithful primitive pentagon code evaluates to the ACTUAL
original four-F45-tree primitive 3-cell, including both F54 paths. -/

/-- Faithful inverse on ALL nine constructors of the distinct original
P92B Type-valued comparison proof, with no omitted witness. -/
theorem nativeGK3P92Decode_encode
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {n n' m m' : Nat}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (cell : NativeF55P92AssocComparison p r s) :
    nativeGK3P92Decode (nativeGK3P92Encode cell) =
      some (nativeGK3PackP92 cell :
        NativeGKOriginalP92Total p D E) := by
  induction cell with
  | original source =>
      simp [nativeGK3P92Encode, nativeGK3P92Decode,
        nativeGJPackPresented, nativeGK3PackP92, nativeGJ2PackRoute]
  | assocNaturality u v w =>
      rfl
  | refl route =>
      simp [nativeGK3P92Encode, nativeGK3P92Decode,
        nativeGJ2PackRoute, nativeGK3PackP92]
  | symm inner ih =>
      simp [nativeGK3P92Encode, nativeGK3P92Decode,
        ih, nativeGK3PackP92, nativeGJ2PackRoute]
  | trans left right ihLeft ihRight =>
      simp [nativeGK3P92Encode, nativeGK3P92Decode,
        ihLeft, ihRight]
      exact nativeGK3P92TransExact_eq left right
  | leftContext inner later ih =>
      simp [nativeGK3P92Encode, nativeGK3P92Decode, ih]
      exact nativeGK3P92LeftExact_eq inner later
  | rightContext earlier inner ih =>
      simp [nativeGK3P92Encode, nativeGK3P92Decode, ih]
      exact nativeGK3P92RightExact_eq earlier inner
  | precompose prior inner ih =>
      simp [nativeGK3P92Encode, nativeGK3P92Decode, ih]
      exact nativeGK3P92PreExact_eq prior inner
  | postcompose inner suffix ih =>
      simp [nativeGK3P92Encode, nativeGK3P92Decode, ih]
      exact nativeGK3P92PostExact_eq inner suffix

/-! Original full P92B Type-valued proof totals and fibers. -/

theorem nativeGK3P92OriginalTotal_countable
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    (hobjD : Countable D)
    (hhomD : ∀ a b : D, Countable (a ⟶ b))
    (hobjE : Countable E)
    (hhomE : ∀ x y : E, Countable (x ⟶ y)) :
    Countable (NativeGKOriginalP92Total p D E) := by
  letI : Countable (NativeGK3P92TypedCode p D E) :=
    nativeGK3P92TypedCode_countable hobjD hhomD hobjE hhomE
  have hrange :
      (Set.range (nativeGK3P92Decode (p := p) (D := D) (E := E))).Countable :=
    Set.countable_range _
  letI : Countable (Set.range
      (nativeGK3P92Decode (p := p) (D := D) (E := E))) :=
    hrange.to_subtype
  let embedding : NativeGKOriginalP92Total p D E →
      Set.range (nativeGK3P92Decode (p := p) (D := D) (E := E)) :=
    fun raw => ⟨some raw, by
      rcases raw with ⟨⟨⟨boundary, r⟩, s⟩, cell⟩
      rcases boundary with
        ⟨a, b, x, y, ma, pa, mb, pb,
          n, n', m, m', first, last⟩
      exact ⟨nativeGK3P92Encode cell,
        nativeGK3P92Decode_encode cell⟩⟩
  have hinj : Function.Injective embedding := by
    intro left right h
    have hs : (some left : Option (NativeGKOriginalP92Total p D E)) =
        some right := congrArg
          (fun t : Set.range
            (nativeGK3P92Decode (p := p) (D := D) (E := E)) => t.1) h
    exact Option.some.inj hs
  exact hinj.countable

/-- Every original F55 dependent proof fiber is Countable at its
actual fully parallel F54 Type-valued source and target. -/
theorem nativeGK3P92OriginalFiber_countable
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    (hobjD : Countable D)
    (hhomD : ∀ a b : D, Countable (a ⟶ b))
    (hobjE : Countable E)
    (hhomE : ∀ x y : E, Countable (x ⟶ y))
    {a b : D} {x y : E}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {n n' m m' : Nat}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (r s : KuuNativeF45Tree.DepthRotationRoute p first last) :
    Countable (NativeF55P92AssocComparison p r s) := by
  letI : Countable (NativeGKOriginalP92Total p D E) :=
    nativeGK3P92OriginalTotal_countable hobjD hhomD hobjE hhomE
  have hinj : Function.Injective
      (fun cell : NativeF55P92AssocComparison p r s =>
        (nativeGK3PackP92 cell : NativeGKOriginalP92Total p D E)) := by
    intro left right h
    exact eq_of_heq (Sigma.mk.inj h).2
  exact hinj.countable

/-- The ACTUAL original raw F55 total on true physical C60 Site
axes is unconditionally Countable, retaining the complete proof. -/
theorem nativeGK3PhysicalP92Total_countable (p : Polygon) :
    Countable (NativeGKOriginalP92Total p Site Site) :=
  nativeGK3P92OriginalTotal_countable
    nativeC60GEPhysicalSite_countable
    nativeC60GEPhysicalIncidenceHom_countable
    nativeC60GEPhysicalSite_countable
    nativeC60GEPhysicalIncidenceHom_countable

/-- Each actual parallel C60 F54 raw route pair has a Countable
original F55 nine-constructor proof fiber, without quotienting. -/
theorem nativeGK3PhysicalP92Fiber_countable
    (p : Polygon)
    {a b x y : Site}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {n n' m m' : Nat}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (r s : KuuNativeF45Tree.DepthRotationRoute p first last) :
    Countable (NativeF55P92AssocComparison p r s) :=
  nativeGK3P92OriginalFiber_countable
    nativeC60GEPhysicalSite_countable
    nativeC60GEPhysicalIncidenceHom_countable
    nativeC60GEPhysicalSite_countable
    nativeC60GEPhysicalIncidenceHom_countable r s

/-- All true physical C60 polygons carry Countable original F55
proof totals with full independent two-axis history. -/
theorem nativeGK3PhysicalAllPolygonP92_countable :
    Countable (Σ p : Polygon,
      NativeGKOriginalP92Total p Site Site) := by
  letI : Countable Polygon := nativeC60GEPhysicalPolygon_countable
  letI : ∀ p : Polygon,
      Countable (NativeGKOriginalP92Total p Site Site) :=
    nativeGK3PhysicalP92Total_countable
  infer_instance


#print axioms nativeGK3P92Decode_encode
#print axioms nativeGK3P92OriginalTotal_countable
#print axioms nativeGK3P92OriginalFiber_countable
#print axioms nativeGK3PhysicalP92Total_countable
#print axioms nativeGK3PhysicalP92Fiber_countable
#print axioms nativeGK3PhysicalAllPolygonP92_countable

end
end Kuu.F112.Physical
