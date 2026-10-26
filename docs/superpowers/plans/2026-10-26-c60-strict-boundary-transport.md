# C60 strict boundary transport implementation plan

**Goal:** Connect AZ finite strict realizations across adjacent levels without claiming that a list of strict categories is already a strict n-category.

**Spec / authority:** Continue after the user's explicit merge-and-proceed instruction and earlier strict-Kuu correction. #2558 was squash merged at canonical main 98476eff64fc4d90e78b551899f3446d72cb6a5a. Keep the actual C60 14/15-cell base, all finite heights, selected rather than universal Kuu comparisons, both endpoints, raw history and noncommutative observations.

**Architecture:** Fold every free path back to an actual AX comparison. Prove the strict realization is surjective on each hom-set and on the sigma bundle of endpoints plus a strict arrow. Establish the exact unique-factorization criterion for an upper-level readout through this strict-arrow bundle. Show why the current faithful upper object embedding does not itself factor: refl and trans(refl,refl) have equal lower strict realizations but are distinct raw next objects. Construct a compatible cross-level observer and strict functor to the discrete bundle, and carry its descent through every finite continuation. The discrete codomain is an observer only, never a replacement for the proof-relevant higher category.

**Alternatives:** Repeating stagewise category laws does not solve the cross-level issue. Identifying all parallel objects destroys information and is rejected. Selected: exact quotient interface, concrete obstruction to naive lifting, and compatible boundary transport, as preparation for genuine higher horizontal composition.

**Tech stack:** Lean v4.30.0-rc2; mathlib 5450b53e5ddc75d46418fabb605edbf36bd0beb6; Kuu.Strict; AX/AY/AZ. No new logical axioms, sorry/admit, Gray, new public roots, or changes to old theorem statements.

## Tasks
1. Verify #2558 exact-head green and merge; verify main equals returned merge SHA.
2. Observe source-contract RED before implementation. Local Lean is absent and container DNS is unavailable, so source checks are not compiler verification.
3. Implement free-path folding, strict realization surjectivity, and unique-factorization criterion with explicit dependent endpoint types.
4. Implement the unit-composite counterexample and obstruction to descending the faithful next-object embedding. Do not describe this as a no-go for all possible strict n-presentations.
5. Construct the compatible full strict-arrow boundary observer, its strict quotient functor, and all-finite continuation descent. Specialize to original C60 data.
6. Add exactly one KuuOSFormal import, preserving every older import and all 107 public roots. Add #print axioms for every declaration.
7. Open a draft PR and inspect exact-head pinned Strict Lean plus governance evidence. No success or merge claim without evidence.

## Scope and review
The quotient relations remain AZ's independently declared structural/selected relations; no Peiffer/evaluator kernel replaces them. The factorization condition describes readouts of an already constructed quotient. Surjectivity is proved by path induction, not assumed. Source and target travel together in a sigma bundle. The obstruction is only to retaining the present injective raw-object embedding while demanding descent along the lower strict realization. Cross-dimensional strict horizontal composition/interchange, original geometric 16-cell coherence, full P92B descent and hyperdescent remain separate obligations.

Primary sources consulted: pinned mathlib PathCategory/Basic and Quotient implementations; official mathlib4 documentation for path categories and category notation. Preserve the learned distinction between Quiver.Path.comp/nil and overloaded categorical notation, and give dependent local lemmas full expected types.
