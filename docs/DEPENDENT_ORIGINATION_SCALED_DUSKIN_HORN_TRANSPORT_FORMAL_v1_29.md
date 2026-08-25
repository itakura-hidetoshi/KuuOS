# Dependent Origination — Scaled Duskin Horn Transport v1.29

Version 1.29 advances the presentation-independent invariant from intrinsic
1/2-cell comparison to the scaled-horn interface.

For any scaled simplicial map `f : X ⟶ Y`, a scaled horn-extension problem in
`X` is pushed forward by postcomposing its horn map with `f`.  Any scaled filler
pushes forward in the same way.  If chosen horn families are compatible under
this transport, admissibility and filler existence are preserved for every
transported source horn.

For global Duskin nerves, v1.27 already constructs the normalized simplicial
map induced by a strictly-unitary bicategorical model equivalence and proves
preservation of nondegenerate thin triangles.  v1.29 isolates the remaining
full scaling statement, including degenerate triangles, as
`FullScaledDuskinMapCertificate`.  Once that certificate is supplied, global
scaled horn problems and fillers transport by the generic theorems.

The direction is deliberately one-way.  A filler theorem for source horns does
not imply arbitrary target fibrancy unless every relevant target horn is known
to be represented by a transported source horn.  Full presentation-independent
fibrancy therefore requires an inverse or essential-surjectivity theorem at the
scaled horn level.

The current chain is

```text
presentation-independent intrinsic invariant
  -> normalized global Duskin map
  -> scaled horn-problem transport
  -> scaled filler transport
  -> future scaled-horn presentation equivalence
  -> presentation-independent global (∞,2) fibrancy
```
