# KuuOS Qi v3.3 — 到達可能な観測圏とKuu観測商の圏同値

## 数学的構成

v3.2ではpathShiftの一致を明示的な合同としてKuu商に与えた。
v3.3では、商を単に改名するのではなく、別の観測圏ObservedPhaseを構成する。

- 対象：ZMod 5の五相。
- pからqへの射：自然数nと、長さnの型付き自由経路p→qが存在するというPropの証明。
- 恒等射：イベント数0の空経路。
- 合成：イベント数の加算。型付き経路の合成によって到達可能性を証明。

観測値に元の経路の順序・履歴は含まれず、存在証明はPropに保たれる。
自由経路からのpathObservationFunctorはfullだがfaithfulではない。
その核がv3.2のshiftObservationRelationsと正確に一致する。

独立Kuuの普遍性からobservationDescentを構成し、homの単射性・全射性と
本質的全射性を証明して、mathlibのFunctor.asEquivalenceにより
Kuu.Space(shiftObservationRelations) ≌ ObservedPhase を実装する。
元の異なる型付き経路が等しいという主張ではない。

## 保全と検証

標準公開入口はKuuOSFormalのみ。107公開root、F112 PR #2339、
固定Lean/mathlib、Gray非依存、legacyの証明を変更しない。
v3.3の定理・圏同値は#print axiomsを監査し、sorryAxを許さない。
物理的ゲージ同一性、臨床的な因果、外部実行権限には適用しない。
