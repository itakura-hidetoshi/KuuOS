# KuuOS 五行経路の観測合同と商 — v3.2

## 出発点
v3.1 では五次巡回群の相生(+1)・相剋(+2)を型付き矢印として定義し、
位相変位とイベント数を観測する `pathShift` を構成した。
その観測が経路の合成と整合する一方、異なる順序の経路を区別できないことも
証明した。

## v3.2 の新しい数学的結果

**観測による同一視は「自然に真理となる経路の等式」ではない。**
`shiftObservationRelations` という明示的な関係を独立 Kuu の
`Kuu.Relations` に定義して初めて、同一視が許される。

1. **合同性**：関係は各平行射集合上の同値関係であり、
   前合成・後合成・両側合成を保持する
   (`shiftObservationRelations_congruence`)。
2. **商の正確性**：商への射影で２経路が等しくなる条件は、
   `pathShift` が等しいことと同値。
   平行経路では位相差は始点と終点で固定されるため、これは
   **イベント数が等しいことと同値**。
3. **非忠実性**：相生→相剋と相剋→相生は、同じ終点とイベント数２に
   到達するため、この観測商では同一視される。しかし元の自由経路では
   中間頂点が異なるので同一ではない。
4. **保護される区別**：一つの相剋矢印と二つの相生矢印は、位相の終点が
   同じでもイベント数がそれぞれ１・２なので観測商でも異なる。
5. **独立 Kuu との関係**：恒等関係によるKuu商では相生→相剋と
   相剋→相生の両者が区別される。観測商の同一視は追加の明示関係による。
6. **普遍性**：観測関係を保つカテゴリーファンクターはこの商を通して
   一意に因子化される（既存Kuuの普遍性を具体化）。

## 形式化
- `formal/KUOS/Architecture/QiWuxingPathObservationCongruenceV3_2.lean`
- `formal/KuuOSQiWuxingPathObservationCongruenceV3_2.lean`
- 入口は従来どおり `KuuOSFormal`。追加の公開Lean rootは作成しない。
- `#print axioms` で新規定理の依存公理を監査する。

```sh
lake exe cache get
lake build +KUOS.Architecture.QiWuxingPathObservationCongruenceV3_2:olean \
  +KuuOSQiWuxingPathObservationCongruenceV3_2:olean
lake build KuuOSFormal
```

## 権限と適用範囲
この結果は、有限巡回群・型付き自由経路・観測合同の形式数学に限定される。
Grayの再導入は行わず、従来の証明・仮定・固定バージョンは変更しない。
物理ゲージ系、病態遷移、臨床治療効果、外部実行権限については何も主張しない。
