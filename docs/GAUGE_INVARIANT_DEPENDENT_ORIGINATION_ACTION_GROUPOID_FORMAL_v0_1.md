# Gauge-Invariant Dependent Origination — Action Groupoid Formalization v0.1

Date: 2026-08-16

This package is append-only and tighten-only. It follows the integrated dense-descent theorem and coarse orbit-factorization theorem without overwriting either.

## Exact lineage

- predecessor main: `5364ee37ba0ec07f6fe6090cbebfb8ba44f6eed9`
- predecessor PR: #1388
- formal file: `formal/KUOS/GaugeInvariantDependentOriginationActionGroupoidV0_1.lean`
- overwrite: forbidden
- same-root: required

## Why the orbit quotient is not enough

PR #1388 proves that gauge-invariant semantics factor uniquely through the coarse orbit quotient.

That quotient records only whether two representatives lie in the same gauge orbit. It does not retain which gauge transformation relates them, and therefore it can forget stabilizer/isotropy information.

The present layer retains the actual arrows

\[
\mathrm{Hom}(x,y)=\{g\in G\mid g\cdot x=y\}.
\]

This is the elementary action-groupoid presentation of the same gauge relation.

## Formal content

The Lean file proves:

- `ActionArrow`: actual gauge arrows between representatives;
- identity, composition, inverses, and groupoid laws;
- `GaugeRelated x y ↔ Nonempty (ActionArrow x y)`;
- equality of coarse orbit projections iff an action-groupoid arrow exists;
- `ActionIsotropy x`: loops at one representative;
- `gaugeStabilizer x`: stabilizer subgroup;
- `isotropyEquivStabilizer`: isotropy and stabilizer carry the same gauge elements;
- `isotropyEquivAlongArrow`: gauge-related representatives have equivalent isotropy via conjugation;
- distinct stabilizer elements remain distinct arrows although the coarse orbit point is identical;
- semantic gauge invariance iff semantics are constant along every action-groupoid arrow;
- dense dependent-origination descent generates action-groupoid semantic constancy, unique coarse-orbit semantics, and cross-scale compatibility.

## KuuOS interpretation

The strengthened reading is:

```text
空 = no representative has independent semantic authority
縁起 = relational appearances retain their transformation arrows and isotropy
二諦 gap = neither the representative space nor its invariant quotient is ultimate substance
中道 = preserve relational structure without reifying coordinates or erasing morphisms
```

The semantic layer is still invariant, while presentation-level data remain equivariant.

## 0-truncation boundary

The coarse orbit quotient is the 0-truncated semantic shadow of the action groupoid:

\[
G\ltimes X \longrightarrow X/G.
\]

The groupoid retains multiplicity of arrows and isotropy. The quotient keeps only connected-component/orbit information.

This package therefore does **not** identify `X/G` with the full relational structure of dependent origination.

## What this still does not prove

This layer does not yet construct a quotient stack, sheaf-valued descent object, higher stack, or derived moduli object. It does not claim that ordinary groupoid data alone retain all holonomy, curvature, or local gluing data already represented elsewhere in KuuOS.

It also does not weaken the existing boundary that cross-scale compatibility plus density does not generate existence of a continuous global semantic extension.

## Next formal frontier

The natural next refinement is to combine this action-groupoid layer with existing KuuOS sheaf/gauge runtime structure:

\[
\text{local sections + transition arrows + cocycle + gluing}
\Longrightarrow
\text{groupoid-aware descent object}.
\]

Only after that should a quotient-stack interpretation be promoted beyond documentation-level semantics.
