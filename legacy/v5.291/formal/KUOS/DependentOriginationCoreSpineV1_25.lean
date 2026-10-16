import KUOS.DependentOriginationCoreSpineV1_24
import KUOS.DependentOriginationPresentationIndependentInvariantV1_25

namespace KUOS.DependentOriginationCoreSpineV1_25

/-!
# Dependent-origination core spine v1.25

The v1.25 spine advances the higher-categorical realization from a pairwise
local/global comparison to an explicit presentation-independent invariant
kernel.

The parent dependent-origination definition remains unchanged.  For a native
bicategorical specialization `B`, the new layer places the intrinsic
hom-category `B(X,Y)` between the two presentations:

```text
local mapping nerve N(B(X,Y))
          \
           \-> intrinsic B(X,Y) <-/
                                /
                    global scaled Duskin nerve
```

At degree zero, local vertices and fixed-endpoint global Duskin edges recover
the same intrinsic 1-morphism.  At degree one of the mapping nerve, local edges
and global Duskin comparison triangles recover the same intrinsic 2-morphism.
Thus every observable factoring through the intrinsic carrier is automatically
presentation independent.

For nondegenerate Duskin triangles, scaling is exactly intrinsic invertibility
of the comparison 2-cell.  Under object univalence plus all-pairs global edge
representability, equality paths, local equivalence vertices, and global Duskin
equivalence edges all classify the same intrinsic object-equivalence relation.

This is still a two-skeleton / object-completeness invariant kernel.  It does
not yet assert a full equivalence of local and global `(∞,2)` presentations in
all degrees, nor invariance under changing the underlying bicategory itself.
-/

end KUOS.DependentOriginationCoreSpineV1_25
