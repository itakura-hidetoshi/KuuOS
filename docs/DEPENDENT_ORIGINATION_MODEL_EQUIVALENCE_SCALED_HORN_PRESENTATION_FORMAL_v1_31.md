# Dependent Origination model-equivalence scaled horn presentation — formal v1.31

Version 1.31 connects bicategorical model replacement to the presentation-independent scaled-fibrancy theorem of v1.30.

The new certificate is `BidirectionalScaledDuskinModelEquivalence HB HC`. It contains:

- a strictly-unitary bicategorical model equivalence `B -> C`;
- a strictly-unitary comparison `C -> B`;
- full scaled-map certificates for both normalized global Duskin maps;
- preservation of the chosen admissible horn families in both directions;
- equivalence of filler existence after each forward/backward round trip.

From this data KuuOS constructs, rather than assumes,

```text
ScaledHornPresentationEquivalence HB HC
```

and therefore proves

```text
HasScaledHornFillers (duskinNerve B) (duskinScaling B) HB
  <->
HasScaledHornFillers (duskinNerve C) (duskinScaling C) HC.
```

Thus global scaled fibrancy is invariant under every bicategorical model replacement carrying the explicit bidirectional scaled-Duskin equivalence structure.

The remaining boundary is existence. A general v1.26 `BicategoricalModelEquivalence` does not yet automatically produce this stronger package. The missing construction is the coherent combination of strictly-unitary normalization, a quasi-inverse, full scaling preservation, and the induced round-trip filler equivalences.
