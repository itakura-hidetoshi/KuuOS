import Kuu.F112.PolygonNativeC60AQFullPentagonCodeFiberKernel

/-!
# F112-P94D3FC — C60 finite AQ context full-code kernel versus pentagon relation

FC's general kernel/faithfulness criterion specializes to the actual
physical C60 DV finite context trees. It does NOT presume that
arbitrary Bool-indexed frame actions are injective.

The PREVIOUS FB theorem proves that the ORIGINAL genuinely typed
three-versus-two 18D pentagon free difference never belongs to
the kernel of DV's real original-to-closed 18D full-word transport,
for ANY original finite chronological context. This fact DOES NOT
by itself show that the whole DV code map is injective; FC isolates
the precise code-fiber criterion that would be needed.

The selected DT all-pentagon normal subgroup is NEVER contained in
the kernel of the unquotiented DV group hom, even though its image is
contained in the independent DX full-closed-pentagon normal closure.
Thus descending the original all-pentagon quotient through DV
requires the explicit target relative quotient and cannot result in
a faithful full-target receiver.

Under genuine finite AQ tree reassociation with equal chronological
steps the entire code map, collision test, group kernel and pentagon
nontriviality are unchanged. This requires no new physical 19D
filler, Gray, abelianization, or comparison of distinct raw histories.
All original 14D--18D proof data, strict Kuu, independent Kuu one
presentation, DS no-go, 107 public roots, fixed Lean/mathlib remain.
Append-only, tighten-only, same-root. No new axioms, sorry or admit.
Copyright Hidetoshi Itakura / 板倉英俊. Apache-2.0.
-/

namespace Kuu.F112.Physical

open CategoryTheory
set_option autoImplicit false
set_option warningAsError true
set_option maxRecDepth 8192
set_option maxHeartbeats 4000000
noncomputable section

universe u

section PhysicalOriginalCompleteKernelGate

variable {L : NativeC60AXLayer.{u}}
variable (S : NativeC60AXSignature L) (F : Bool → NativeC60BCFrame L)

/-- The ORIGINAL fully typed 18D pentagon ratio is NOT in the
kernel of ACTUAL DV transport into the distinct, unquotiented,
full target FreeGroup for ANY finite C60 context word. -/
theorem nativeC60FCPentagon_not_mem_DVKernel
    (word : List Bool)
    {a b c d e : (nativeC60DQSeventeenLayer S F).Total}
    (f : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b)
    (g : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) b c)
    (h : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) c d)
    (k : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) d e) :
    (nativeC60DSFreeWord S F
        (nativeC60DRPentagonLong S F f g h k))⁻¹ *
      nativeC60DSFreeWord S F
        (nativeC60DRPentagonShort S F f g h k) ∉
      (nativeC60DVFullWordTransport S F word).ker := by
  intro hmem
  exact nativeC60FBActualTransportPentagon_ratio_ne_one
    S F word f g h k (MonoidHom.mem_ker.mp hmem)

/-- STRONGER NORMAL-KERNEL BOUNDARY:
the global original DT all-pentagon relation subgroup is NOT
contained in the actual unquotiented complete-code DV transport
kernel. We use an actual original dependent 17D four-path pentagon,
not a fictitious element nor an arbitrary scalar witness. -/
theorem nativeC60FCAllPentagonKernel_not_le_DVKernel
    (word : List Bool)
    {a b c d e : (nativeC60DQSeventeenLayer S F).Total}
    (f : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b)
    (g : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) b c)
    (h : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) c d)
    (k : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) d e) :
    ¬ nativeC60DTPentagonNormalClosure S F ≤
        (nativeC60DVFullWordTransport S F word).ker := by
  intro hle
  have hsource :
      (nativeC60DSFreeWord S F
          (nativeC60DRPentagonLong S F f g h k))⁻¹ *
        nativeC60DSFreeWord S F
          (nativeC60DRPentagonShort S F f g h k) ∈
        nativeC60DTPentagonNormalClosure S F :=
    nativeC60EYNineteen_ratio_mem_DT S F f g h k
  exact nativeC60FCPentagon_not_mem_DVKernel
    S F word f g h k (hle hsource)

/-- In contrast the SAME original full pentagon difference is in
DX's separately DECLARED closed target normal subgroup. The
noncontainment above is for the kernel of the UNQUOTIENTED map. -/
theorem nativeC60FCPentagon_DVKernel_vs_relative
    (word : List Bool)
    {a b c d e : (nativeC60DQSeventeenLayer S F).Total}
    (f : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b)
    (g : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) b c)
    (h : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) c d)
    (k : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) d e) :
    let defect :=
      (nativeC60DSFreeWord S F
          (nativeC60DRPentagonLong S F f g h k))⁻¹ *
        nativeC60DSFreeWord S F
          (nativeC60DRPentagonShort S F f g h k)
    defect ∉ (nativeC60DVFullWordTransport S F word).ker ∧
      (nativeC60DVFullWordTransport S F word) defect ∈
        nativeC60DXFullClosedPentagonNormalClosure S F := by
  dsimp only
  exact ⟨nativeC60FCPentagon_not_mem_DVKernel
    S F word f g h k,
    nativeC60FAActualContext_pentagon_ratio_mem_full
      S F word f g h k⟩

/-- If two genuine finite C60 AQ context trees retain the same
chronological steps, the ENTIRE original dependent complete 18D
code function agrees, not only a Peiffer charge or parity shadow. -/
theorem nativeC60FCActualTree_code_refinement
    {left right : NativeK5DOContextTree}
    (hsteps : nativeK5DOTreeSteps left = nativeK5DOTreeSteps right) :
    nativeC60DVTransportCompleteCode S F
      (nativeK5DOTreeWord left) =
      nativeC60DVTransportCompleteCode S F
        (nativeK5DOTreeWord right) := by
  rw [nativeK5DOTreeWord_eq_of_steps_eq hsteps]

/-- The exact FC injectivity criterion is unchanged by genuine
finite AQ tree reparenthesization with the same chronological
physical context steps. -/
theorem nativeC60FCActualTree_injective_criterion_refinement
    {left right : NativeK5DOContextTree}
    (hsteps : nativeK5DOTreeSteps left = nativeK5DOTreeSteps right) :
    Function.Injective (nativeC60DVFullWordTransport S F
        (nativeK5DOTreeWord left)) ↔
      Function.Injective (nativeC60DVFullWordTransport S F
        (nativeK5DOTreeWord right)) := by
  rw [nativeC60DVActualTree_word_refinement S F hsteps]

/-- Full unquotiented original-to-closed DV group hom KERNEL
is invariant under regroupings of the exact same chronological
finite C60 AQ context steps. -/
theorem nativeC60FCActualTree_kernel_refinement
    {left right : NativeK5DOContextTree}
    (hsteps : nativeK5DOTreeSteps left = nativeK5DOTreeSteps right) :
    (nativeC60DVFullWordTransport S F
        (nativeK5DOTreeWord left)).ker =
      (nativeC60DVFullWordTransport S F
        (nativeK5DOTreeWord right)).ker := by
  rw [nativeC60DVActualTree_word_refinement S F hsteps]

/-- The original source complete 18D pentagon normal subgroup
continues to fail containment in the ACTUAL unquotiented DV kernel
for every genuine finite AQ context tree, even though transport
to DX's selected relative target quotient exists. -/
theorem nativeC60FCActualTree_pentagon_not_le_kernel
    (tree : NativeK5DOContextTree)
    {a b c d e : (nativeC60DQSeventeenLayer S F).Total}
    (f : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) a b)
    (g : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) b c)
    (h : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) c d)
    (k : NativeC60AXStep (nativeC60DQTriangleSeventeenSignature S F) d e) :
    ¬ nativeC60DTPentagonNormalClosure S F ≤
      (nativeC60DVFullWordTransport S F
        (nativeK5DOTreeWord tree)).ker :=
  nativeC60FCAllPentagonKernel_not_le_DVKernel S F
    (nativeK5DOTreeWord tree) f g h k

end PhysicalOriginalCompleteKernelGate

#print axioms nativeC60FCPentagon_not_mem_DVKernel
#print axioms nativeC60FCAllPentagonKernel_not_le_DVKernel
#print axioms nativeC60FCPentagon_DVKernel_vs_relative
#print axioms nativeC60FCActualTree_code_refinement
#print axioms nativeC60FCActualTree_injective_criterion_refinement
#print axioms nativeC60FCActualTree_kernel_refinement
#print axioms nativeC60FCActualTree_pentagon_not_le_kernel

end
end Kuu.F112.Physical
