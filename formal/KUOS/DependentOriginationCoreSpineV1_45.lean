import KUOS.DependentOriginationScaledColimitsPresentabilityV1_45

namespace KUOS.DependentOriginationCoreSpineV1_45

open CategoryTheory
open KUOS.DependentOriginationScaledColimitsPresentabilityV1_45

/-!
# Dependent-origination core spine v1.45

The higher scaled-Duskin specialization now closes the internal canonical
small-object / weak-factorization frontier.

The parent dependent-origination structure remains context-dependent
establishment plus composable transport.  Scaled simplicial sets, Duskin
nerves, horn fillers, and weak factorization systems remain higher
specializations/completions rather than a redefinition of the parent.

The lifting-theoretic route is now theorem-level:

```text
canonical horn-cylinder attachment generators T
  -> explicit colimits in ScaledSSet
  -> forget : ScaledSSet -> SSet preserves colimits
  -> minimal-scaled finite sources are finitely presentable
  -> IsCardinalForSmallObjectArgument T aleph0
  -> HasSmallObjectArgument T
  -> HasFunctorialFactorization (T.rlp.llp) (T.rlp)
  -> native IsWeakFactorizationSystem (T.rlp.llp) (T.rlp)

and

T.rlp.llp
  = retracts
      (transfinite compositions
        (pushouts
          (coproducts T))).
```

The colimit scaling is the least scaling containing the degenerate
2-simplices and the images of all thin 2-simplices from the diagram objects.
The canonical generator sources carry minimal scaling, so maps out of them
identify naturally with underlying simplicial maps.  Their underlying
horn-cylinder attachments are finite subcomplexes of `Δ[n] × Δ[1]`; Mathlib's
finite-simplicial-set presentability theorem therefore supplies the required
filtered-colimit preservation.

No factorization, strictification, horn-family RLP, or presentability
certificate remains as an independent field in this internal canonical route.
The external comparison with any future standard/Lurie scaled-anodyne class
remains a separate morphism-property comparison theorem.
-/

end KUOS.DependentOriginationCoreSpineV1_45
