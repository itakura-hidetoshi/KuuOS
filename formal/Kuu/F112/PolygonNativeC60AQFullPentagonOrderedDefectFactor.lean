import Kuu.F112.PolygonNativeC60AQFullPentagonNineteenPathGate

/-!
# F112-P94D3EX — ordered noncommutative defect of a genuine typed higher path

EW locates a violating primitive ATOM inside the GIVEN hypothetical 19D
pentagon-filler path, retaining the original dependent 18D/17D boundaries.
EX upgrades the occurrence certificate to a noncommutative factorization.

For a group-valued observer H on the same Type-valued layer, every
original signed comparison path is evaluated IN ITS ACTUAL ORDER:
  atom(g) ↦ H(source(g))⁻¹ * H(target(g))
  refl ↦ 1, symm ↦ inverse, trans ↦ ordered group multiplication.
The resulting defect telescopes EXACTLY to H(source(p))⁻¹ * H(target(p)).
This uses the original typed signed syntax; no scalar receiver, graph,
commutativity assumption, or replacement proof grammar is introduced.

Any path-local violating atom provided by EW produces a certified
factorization D(p)=prefix * signed-atom-defect * suffix, with a
nonidentity middle factor. Prefix/suffix are genuinely ordered
noncommutative GROUP values. The sign inversion and position are
tracked by the original Type-valued occurrence witness. The middle
factor need not equal D(p), nor does any individual factor have to
survive cancellation in a quotient.

No 19D geometric filler is created. The original strict Kuu, distinct
independent Kuu presentation, DS complete-evidence no-go, 14D--18D
typed evidence, 107 public roots, fixed Lean/mathlib and no-Gray
policy remain. Append-only/same-root; no new axioms, sorry or admit.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u v

section GeneralNoncommutativePathDefect

variable {L : NativeC60AXLayer.{u}} (T : NativeC60AXSignature L)
variable {G : Type v} [Group G] (obs : L.Total → G)

/-- Actual ordered group evaluation of the signed, dependent
NativeC60AXStep grammar. It is NOT an abelianized statistic. -/
def nativeC60EXFoldDefect {x y : L.Total}
    (p : NativeC60AXStep T x y) : G :=
  p.fold
    (fun {a b} (_ : T.Gen a b) => (obs a)⁻¹ * obs b)
    (fun _ => 1)
    (fun d => d⁻¹)
    (fun d e => d * e)

theorem nativeC60EXFoldDefect_atom
    {x y : L.Total} (g : T.Gen x y) :
    nativeC60EXFoldDefect T obs (.atom g) = (obs x)⁻¹ * obs y := rfl

theorem nativeC60EXFoldDefect_refl (x : L.Total) :
    nativeC60EXFoldDefect T obs (.refl x) = 1 := rfl

theorem nativeC60EXFoldDefect_symm
    {x y : L.Total} (p : NativeC60AXStep T x y) :
    nativeC60EXFoldDefect T obs (.symm p) =
      (nativeC60EXFoldDefect T obs p)⁻¹ := rfl

theorem nativeC60EXFoldDefect_trans
    {x y z : L.Total} (p : NativeC60AXStep T x y)
    (q : NativeC60AXStep T y z) :
    nativeC60EXFoldDefect T obs (.trans p q) =
      nativeC60EXFoldDefect T obs p *
        nativeC60EXFoldDefect T obs q := rfl

/-- The full noncommutative signed path defect telescopes, with
NO commutativity assumption, to the exact endpoint difference. -/
theorem nativeC60EXFoldDefect_eq_endpoints :
    ∀ {x y : L.Total} (p : NativeC60AXStep T x y),
      nativeC60EXFoldDefect T obs p = (obs x)⁻¹ * obs y := by
  intro x y p
  induction p with
  | atom g => rfl
  | refl x =>
      calc
        nativeC60EXFoldDefect T obs (.refl x) = 1 :=
          nativeC60EXFoldDefect_refl T obs x
        _ = (obs x)⁻¹ * obs x := by simp
  | symm p ih =>
      rw [nativeC60EXFoldDefect_symm, ih]
      group
  | trans p q ihp ihq =>
      rw [nativeC60EXFoldDefect_trans, ihp, ihq]
      group

/-- A nontrivial change of group value at the endpoints makes the
original generator's ordered noncommutative ratio nonidentity. -/
theorem nativeC60EXAtomicDefect_ne_one
    {x y : L.Total} (h : obs x ≠ obs y) :
    (obs x)⁻¹ * obs y ≠ 1 := by
  intro heq
  have hh := congrArg (fun t : G => obs x * t) heq
  have hyx : obs y = obs x := by simpa using hh
  exact h hyx.symm

/-- A signed atom which occurs inside p, together with precise
prefix and suffix group factors. The signed factor is either the
atom's forward noncommutative defect or its genuine inverse.
In particular, this is NOT an equality of raw Type-valued histories. -/
def NativeC60EXNoncommutativeFactor
    {x y : L.Total} (p : NativeC60AXStep T x y) : Prop :=
  ∃ (a b : L.Total) (g : T.Gen a b)
    (before middle after : G),
      NativeC60EWAtomOccursOn T g p ∧
      (middle = (obs a)⁻¹ * obs b ∨
       middle = ((obs a)⁻¹ * obs b)⁻¹) ∧
      middle ≠ 1 ∧
      nativeC60EXFoldDefect T obs p = before * middle * after

/-- Strengthen EW's proof-relevant bad-atom certificate into an
ORDERED decomposition of the full noncommutative path defect.
For inverse steps, prefix/suffix are inverted and REVERSED. For
composite steps the untouched side is multiplied on the correct
left/right, with no spurious commutative exchange. -/
theorem nativeC60EXBadAtom_factor
    {x y : L.Total} {p : NativeC60AXStep T x y}
    (h : NativeC60EWBadAtomOn T obs p) :
    NativeC60EXNoncommutativeFactor T obs p := by
  induction h with
  | atom g hne =>
      refine ⟨_, _, g, 1, (obs _)⁻¹ * obs _, 1,
        .atom, Or.inl rfl, ?_, ?_⟩
      · exact nativeC60EXAtomicDefect_ne_one obs hne
      · simp [nativeC60EXFoldDefect_atom]
  | symm _ ih =>
      obtain ⟨a, b, g, front, mid, back, hocc, hsign, hnon, hfactor⟩ := ih
      refine ⟨a, b, g, back⁻¹, mid⁻¹, front⁻¹,
        .symm hocc, ?_, ?_, ?_⟩
      · rcases hsign with hforward | hbackward
        · exact Or.inr (by simp [hforward])
        · exact Or.inl (by simp [hbackward])
      · intro h
        apply hnon
        have h' := congrArg (fun t : G => t⁻¹) h
        simpa using h'
      · rw [nativeC60EXFoldDefect_symm, hfactor]
        group
  | @transLeft x₀ y₀ z₀ pLeft pRight h ih =>
      obtain ⟨a, b, g, front, mid, back, hocc, hsign, hnon, hfactor⟩ := ih
      refine ⟨a, b, g, front, mid,
        back * nativeC60EXFoldDefect T obs pRight, .transLeft hocc,
        hsign, hnon, ?_⟩
      rw [nativeC60EXFoldDefect_trans, hfactor]
      group
  | @transRight x₀ y₀ z₀ pLeft pRight h ih =>
      obtain ⟨a, b, g, front, mid, back, hocc, hsign, hnon, hfactor⟩ := ih
      refine ⟨a, b, g,
        nativeC60EXFoldDefect T obs pLeft * front,
        mid, back, .transRight hocc, hsign, hnon, ?_⟩
      rw [nativeC60EXFoldDefect_trans, hfactor]
      group

/-- If the endpoint observations differ, there is an original atom
INSIDE THE PATH with a nonidentity forward-or-reverse ratio, and
the entire ordered defect is precisely prefix * atom * suffix. -/
theorem nativeC60EXEndpoint_ne_factor
    {x y : L.Total} (p : NativeC60AXStep T x y)
    (hne : obs x ≠ obs y) :
    NativeC60EXNoncommutativeFactor T obs p :=
  nativeC60EXBadAtom_factor T obs
    (nativeC60EWBadOnPath_of_endpoint_ne T obs p hne)

end GeneralNoncommutativePathDefect

#print axioms nativeC60EXFoldDefect
#print axioms nativeC60EXFoldDefect_eq_endpoints
#print axioms nativeC60EXAtomicDefect_ne_one
#print axioms NativeC60EXNoncommutativeFactor
#print axioms nativeC60EXBadAtom_factor
#print axioms nativeC60EXEndpoint_ne_factor

end
end Kuu.F112.Physical
