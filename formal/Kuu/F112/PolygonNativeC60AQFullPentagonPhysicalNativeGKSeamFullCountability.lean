import Kuu.F112.PolygonNativeC60AQFullPentagonPhysicalNativeGKSeamTypedDecoder

/-!
# F112-P94D3GK2 — exact original fourteen-constructor proof countability

The genuine original NativeF54StructuralSeam Type-valued proof remains
exactly its original 14-constructor indexed source. A separate finite
and Countable code carries every original F54 route, D/E categorical
Blocks boundary, both Nat-depth axes, full F45 tree and each recursive
structural seam proof.

A dependent partial decoder rejects incompatible full original F45
or F54 boundaries. The strict decode(encode w) = some(original full w)
left inverse is proved for ALL fourteen constructors, not just their
numerical rotation-count observers. Therefore the whole genuine
source Type total injects into the Countable range of a partial
decoder. Each indexed proof fiber inherits Countable, under explicit
Countable D/E objects and EACH Hom fiber. C60 Site×Site and all its
actual polygons discharge those assumptions via GE–GI.

No old P92B extension, F55 structural comparison, historical
presentation isomorphism, original 14D Countable or 19D filler is
smuggled in. Pinned Lean v4.30.0-rc2/mathlib
5450b53e5ddc75d46418fabb605edbf36bd0beb6.
Append-only, 107 public roots, no Gray. Copyright Hidetoshi
Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical
open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section
universe uD vD uE vE

/-! ### Exact original recursive gluing lemmas -/

theorem nativeGK2TransExact_eq
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
    (left : NativeF54StructuralSeam p r s)
    (right : NativeF54StructuralSeam p s t) :
    nativeGK2TransExact
      (nativeGK2PackSeam left : NativeGK2OriginalSeamTotal p D E)
      (nativeGK2PackSeam right : NativeGK2OriginalSeamTotal p D E) =
    some (nativeGK2PackSeam (.trans left right) :
      NativeGK2OriginalSeamTotal p D E) := by
  simp [nativeGK2TransExact, nativeGK2PackSeam]

theorem nativeGK2LeftExact_eq
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
    (cell : NativeF54StructuralSeam p r s)
    (later : KuuNativeF45Tree p k l mb pb mc pc) :
    nativeGK2LeftExact
      (nativeGK2PackSeam cell : NativeGK2OriginalSeamTotal p D E)
      (nativeGIPackTree later) =
    some (nativeGK2PackSeam (.leftContextCongruence cell later) :
      NativeGK2OriginalSeamTotal p D E) := by
  simp [nativeGK2LeftExact, nativeGK2PackSeam, nativeGIPackTree]

theorem nativeGK2RightExact_eq
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
    (cell : NativeF54StructuralSeam p r s) :
    nativeGK2RightExact
      (nativeGIPackTree earlier)
      (nativeGK2PackSeam cell : NativeGK2OriginalSeamTotal p D E) =
    some (nativeGK2PackSeam (.rightContextCongruence earlier cell) :
      NativeGK2OriginalSeamTotal p D E) := by
  simp [nativeGK2RightExact, nativeGK2PackSeam, nativeGIPackTree]

theorem nativeGK2PreExact_eq
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
    (cell : NativeF54StructuralSeam p r s) :
    nativeGK2PreExact
      (nativeGJ2PackRoute priorRoute)
      (nativeGK2PackSeam cell : NativeGK2OriginalSeamTotal p D E) =
    some (nativeGK2PackSeam (.precompose priorRoute cell) :
      NativeGK2OriginalSeamTotal p D E) := by
  simp [nativeGK2PreExact, nativeGJ2PackRoute, nativeGK2PackSeam]

theorem nativeGK2PostExact_eq
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
    (cell : NativeF54StructuralSeam p r s)
    (suffix : KuuNativeF45Tree.DepthRotationRoute p middle last) :
    nativeGK2PostExact
      (nativeGK2PackSeam cell : NativeGK2OriginalSeamTotal p D E)
      (nativeGJ2PackRoute suffix) =
    some (nativeGK2PackSeam (.postcompose cell suffix) :
      NativeGK2OriginalSeamTotal p D E) := by
  simp [nativeGK2PostExact, nativeGJ2PackRoute, nativeGK2PackSeam]


/-- Strict left inverse on EVERY genuine 14-constructor original
F54 structural Type-valued proof, including all nested raw evidence. -/
theorem nativeGK2Decode_encodeStructural
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    {a b : D} {x y : E}
    {n n' m m' : Nat}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    {r s : KuuNativeF45Tree.DepthRotationRoute p first last}
    (w : NativeF54StructuralSeam p r s) :
    nativeGK2DecodeStructural (nativeGK2EncodeStructural w) =
      some (nativeGK2PackSeam w :
        NativeGK2OriginalSeamTotal p D E) := by
  induction w with
  | refl route =>
      simp [nativeGK2EncodeStructural, nativeGK2DecodeStructural,
        nativeGJ2PackRoute, nativeGK2PackSeam]
  | symm w ih =>
      simp [nativeGK2EncodeStructural, nativeGK2DecodeStructural,
        ih, nativeGK2PackSeam]
  | trans w v ihw ihv =>
      simp [nativeGK2EncodeStructural, nativeGK2DecodeStructural,
        ihw, ihv]
      exact nativeGK2TransExact_eq w v
  | reassoc u v z =>
      rfl
  | leftUnit route =>
      simp [nativeGK2EncodeStructural, nativeGK2DecodeStructural,
        nativeGJ2PackRoute, nativeGK2PackSeam]
  | rightUnit route =>
      simp [nativeGK2EncodeStructural, nativeGK2DecodeStructural,
        nativeGJ2PackRoute, nativeGK2PackSeam]
  | precompose route inner ih =>
      simp [nativeGK2EncodeStructural, nativeGK2DecodeStructural, ih]
      exact nativeGK2PreExact_eq route inner
  | postcompose inner route ih =>
      simp [nativeGK2EncodeStructural, nativeGK2DecodeStructural, ih]
      exact nativeGK2PostExact_eq inner route
  | leftContextTrans u v later =>
      rfl
  | rightContextTrans earlier u v =>
      rfl
  | leftContextUnit earlier later =>
      rfl
  | rightContextUnit earlier later =>
      rfl
  | leftContextCongruence inner later ih =>
      simp [nativeGK2EncodeStructural, nativeGK2DecodeStructural, ih]
      exact nativeGK2LeftExact_eq inner later
  | rightContextCongruence earlier inner ih =>
      simp [nativeGK2EncodeStructural, nativeGK2DecodeStructural, ih]
      exact nativeGK2RightExact_eq earlier inner

/-- The ORIGINAL raw 14-constructor F54 structural seam source total
is Countable, not merely the countable finite grammar. -/
theorem nativeGK2OriginalStructuralTotal_countable
    {p : Polygon}
    {D : Type uD} [Category.{vD} D]
    {E : Type uE} [Category.{vE} E]
    (hobjD : Countable D)
    (hhomD : ∀ a b : D, Countable (a ⟶ b))
    (hobjE : Countable E)
    (hhomE : ∀ x y : E, Countable (x ⟶ y)) :
    Countable (NativeGK2OriginalSeamTotal p D E) := by
  letI : Countable (NativeGK2StructuralTypedCode p D E) :=
    nativeGK2StructuralTypedCode_countable hobjD hhomD hobjE hhomE
  have hrange :
      (Set.range (nativeGK2DecodeStructural (p := p) (D := D) (E := E))).Countable :=
    Set.countable_range _
  letI : Countable (Set.range
      (nativeGK2DecodeStructural (p := p) (D := D) (E := E))) :=
    hrange.to_subtype
  let embedding : NativeGK2OriginalSeamTotal p D E →
      Set.range (nativeGK2DecodeStructural (p := p) (D := D) (E := E)) :=
    fun raw => ⟨some raw, by
      rcases raw with ⟨⟨⟨boundary, r⟩, s⟩, w⟩
      rcases boundary with
        ⟨a, b, x, y, ma, pa, mb, pb, n, n', m, m', first, last⟩
      exact ⟨nativeGK2EncodeStructural w,
        nativeGK2Decode_encodeStructural w⟩⟩
  have hinj : Function.Injective embedding := by
    intro left right h
    have hs : (some left : Option (NativeGK2OriginalSeamTotal p D E)) =
        some right := congrArg
          (fun t : Set.range
            (nativeGK2DecodeStructural (p := p) (D := D) (E := E)) => t.1) h
    exact Option.some.inj hs
  exact hinj.countable

/-- Original 14-constructor structural seam Countable at EVERY
original fully indexed Type-valued F54 source/target proof pair. -/
theorem nativeGK2OriginalStructuralFiber_countable
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
    Countable (NativeF54StructuralSeam p r s) := by
  letI : Countable (NativeGK2OriginalSeamTotal p D E) :=
    nativeGK2OriginalStructuralTotal_countable hobjD hhomD hobjE hhomE
  have hinj : Function.Injective
      (fun w : NativeF54StructuralSeam p r s =>
        (nativeGK2PackSeam w : NativeGK2OriginalSeamTotal p D E)) := by
    intro left right h
    exact eq_of_heq (Sigma.mk.inj h).2
  exact hinj.countable

/-- Complete original F54 structural proof total over two genuine
C60 Site axes is unconditionally Countable. -/
theorem nativeGK2PhysicalStructuralTotal_countable (p : Polygon) :
    Countable (NativeGK2OriginalSeamTotal p Site Site) :=
  nativeGK2OriginalStructuralTotal_countable
    nativeC60GEPhysicalSite_countable
    nativeC60GEPhysicalIncidenceHom_countable
    nativeC60GEPhysicalSite_countable
    nativeC60GEPhysicalIncidenceHom_countable

/-- Every original F54 structural seam fiber at a truly physical
C60 pair of independent raw routes is unconditionally Countable. -/
theorem nativeGK2PhysicalStructuralFiber_countable
    (p : Polygon)
    {a b x y : Site}
    {ma mb : KuuNativeBlocks a b}
    {pa pb : KuuNativeBlocks x y}
    {n n' m m' : Nat}
    {first : KuuNativeF45Tree p n m ma pa mb pb}
    {last : KuuNativeF45Tree p n' m' ma pa mb pb}
    (r s : KuuNativeF45Tree.DepthRotationRoute p first last) :
    Countable (NativeF54StructuralSeam p r s) :=
  nativeGK2OriginalStructuralFiber_countable
    nativeC60GEPhysicalSite_countable
    nativeC60GEPhysicalIncidenceHom_countable
    nativeC60GEPhysicalSite_countable
    nativeC60GEPhysicalIncidenceHom_countable r s

theorem nativeGK2PhysicalAllPolygonStructuralTotal_countable :
    Countable (Σ p : Polygon, NativeGK2OriginalSeamTotal p Site Site) := by
  letI : Countable Polygon := nativeC60GEPhysicalPolygon_countable
  letI : ∀ p : Polygon, Countable (NativeGK2OriginalSeamTotal p Site Site) :=
    nativeGK2PhysicalStructuralTotal_countable
  infer_instance

#print axioms nativeGK2TransExact_eq
#print axioms nativeGK2LeftExact_eq
#print axioms nativeGK2RightExact_eq
#print axioms nativeGK2PreExact_eq
#print axioms nativeGK2PostExact_eq
#print axioms nativeGK2Decode_encodeStructural
#print axioms nativeGK2OriginalStructuralTotal_countable
#print axioms nativeGK2OriginalStructuralFiber_countable
#print axioms nativeGK2PhysicalStructuralTotal_countable
#print axioms nativeGK2PhysicalStructuralFiber_countable
#print axioms nativeGK2PhysicalAllPolygonStructuralTotal_countable

end
end Kuu.F112.Physical
