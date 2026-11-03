# F112-P94D3GK5AW / Qi v4.16 — 元P89の8種context生成元の反射障害局所化と北C60の真正φ-fiber

**正式証明記録／2026年11月3日 JST。** Repository: `itakura-hidetoshi/KuuOS`、唯一のcanonical定理正本: `main`。strict 空は証明権限の境界であり、元F55の真正Type値付き証拠、選択P92B/P93C/P94A、観測shadow、北C60物理gaugeを無条件に同一視しない。権限方向：**独立Kuu → Qi**。

GK5AUで全19 P94A構成子・内部16 P93C構成子のφ-source-holeを検査し、GK5AVで真正P93C-in-P94A二段合成の元F55 source-vertex鎖を構成した。GK5AWはその次の対象として、**元P89に実在する8種類の非垂直生成元操作**の反射障害の局所化を形式化した。新しい型付き定理モジュールの追加と`KuuOSFormal`への追加importのみを行い、元F54/F55/P89および選択P92B/P93C/P94Aの旧ソース・宣言は一切変更しない。公開root **107**、保護PR **#1558 Draft／OPEN／未マージ**を維持。Lean **v4.30.0-rc2**、mathlib **5450b53e5ddc75d46418fabb605edbf36bd0beb6** 固定。

## 1. Exact-source検証とマージ正本

| 対象 | 最終検証済み状態 |
| --- | --- |
| 独立Kuu GK5AW定理 | [PR #3016](https://github.com/itakura-hidetoshi/KuuOS/pull/3016) **MERGED** |
| GK5AW exact-source HEAD | `ce48e80dd878f7dc2a488bbd66b354bceca12d54` |
| GK5AW squash/main SHA | `db6261e0d7a2d4440584329c39b0fed85bfdd72f` |
| GK5AW Governance CI | [#41588370677](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41588370677) **30 / 30 SUCCESS** |
| GK5AW Strict Lean | **9,250 / 9,250 SUCCESS** |
| GK5AW公理監査 | **14件**の`#print axioms`、`sorryAx`なし |
| 北C60 Qi v4.16物理統合 | [PR #3017](https://github.com/itakura-hidetoshi/KuuOS/pull/3017) **MERGED** |
| Qi exact-source HEAD | `2c39368bcedb5bec0ec2a48eede81673642b50c9` |
| Qi squash/main SHA | `7d1a1aeb4f1f5397d4d8d7ab3e61390e13353084` |
| Qi Governance CI | [#41589106673](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41589106673) **30 / 30 SUCCESS** |
| Qi Strict Lean | **10,177 / 10,177 SUCCESS** |
| Qi公理監査 | **4件**の`#print axioms`、`sorryAx`なし |

両exact-source CIで新規Leanファイルのerror/warningは0、`sorryAx`・新規公理はない。公理依存はなし、あるいはLean/mathlib標準の`propext`・`Classical.choice`・`Quot.sound`の範囲内。CI検証コミットとsquash SHAを同一視しない。

## 2. 数学的中心：BadPairの「外から内への」必要障害の局所化

元F54の二Nat・二圏Blocks付き経路上で、元F55真正3-cell証拠`f,g`の選択φ像にP94A四セルが存在するが、元P89四セルがない条件をGK5AQの`BadPair(f,g)`とする。

GK5AWでは次の**8種類の元P89生成元操作が既存ソースに本当に存在すること**を使い、それぞれ外側のBadPairがあれば内側の選択四セル比較にも真正元P89の欠損があることを示した。

| 元P89操作 | GK5AWの新規形式化 |
| --- | --- |
| 左3-cell whisker | `nativeGK5AWLeftWhisker_bad_localizes` |
| 右3-cell whisker | `nativeGK5AWRightWhisker_bad_localizes` |
| 左F45 context | `nativeGK5AWLeftContext_bad_localizes` |
| 右F45 context | `nativeGK5AWRightContext_bad_localizes` |
| 元F54 precompose | `nativeGK5AWPrecompose_bad_localizes` |
| 元F54 postcompose | `nativeGK5AWPostcompose_bad_localizes` |
| 左horizontal whisker | `nativeGK5AWHorizontalLeft_bad_localizes` |
| 右horizontal whisker | `nativeGK5AWHorizontalRight_bad_localizes` |

これらはすべて**元F55証拠に由来する追加contextと、内側の真正P94A比較が与えられた場合**に適用する条件付き定理である。例えば、元P89に`leftWhisker(prior,w)`が実在するため、

~~~text
SelectedP94A(phi(f), phi(g))
AND BadPair(trans(prior,f), trans(prior,g))
  => BadPair(f,g).
~~~

なぜなら元P89(f,g)が実在すれば、元P89の真正構成子で外側も元P89に反射でき、仮定した外側のBadPairと矛盾するからである。逆方向「内側BadPairなら必ず外側BadPair」は**主張しない**。contextは元の反射欠損を潰す可能性があり、必要性と十分性を無条件に同一視してはならない。

これによりGK5AVの二段source-vertex鎖に加え、*source-compatibleな非垂直操作が非反射障害を新規に生む場合は内側ですでに障害が存在する*という厳密な局所必要条件が得られた。

## 3. 別条件：選択P92Bの追加引数の真正φ-fiber

選択P94A側のwhiskerやhorizontalは、元F55に由来するとは限らない任意のP92B 3-proofを追加引数として取れる。GK5AWはこれを元P89反射とは混同せず、GK5AUの全構成子source-saturationから個々の元証拠fiberを取り出す。

- `nativeGK5AWLeftWhisker_prior_fiber`：選択leftWhiskerの追加priorに真正元F55 fiberが存在。
- `nativeGK5AWRightWhisker_suffix_fiber`：選択rightWhiskerの追加suffixに真正元F55 fiberが存在。
- `nativeGK5AWHorizontalLeft_other_fiber` と `nativeGK5AWHorizontalRight_other_fiber`：左右horizontal側の他方P92B証拠に真正元F55 fiberが存在。
- `nativeGK5AWInterchange_four_internal_fibers`：source-saturatedな真正P94A水平interchange構成子の**4つすべて**のP92B証拠に元F55 φ-fiberが存在。

fiberとは選択証拠`q`に対する本当の依存型`{m : OriginalF55 // φ(m)=q}`である。左右文脈生成元の偶奇、同じC60 shadow、商等式をfiberの代用にはしない。さらにfiberが非空でも、**元P89の4-cell反射を独立に確認する必要がある**。

## 4. 元P89の真正horizontal interchangeは独立に反射済み

`nativeGK5AWOriginalInterchange_reflects_not_bad`は、4つの**真正元F55証拠**`f₁,f₂,g₁,g₂`から既存の`P89.interchange f₁ f₂ g₁ g₂`を直接構成する。よってこの元証拠に由来する正確なinterchange source pairには元P89四セルが存在し、GK5AQ BadPairにはなり得ない。

これは「すべての任意選択P94A interchangeが元P89に反射可能」という証明ではない。選択inputごとのφ-fiberを先に検査し、既存元P89構成子へ型付きで接続できる場合にのみ元証拠へ降下する。元P80水平／左右contextの3原始unitについても、GK5AQの既証明が元P89への正確な反射を保持している。未検証の新P93C生成元まで自動的に含めない。

## 5. Qi v4.16：北C60の物理と証拠反射を分離して接続

Qiの4定理は、真正北四段pentagon長短のF54/F55二Nat付き元証拠にGK5AWを特殊化する。

1. `fivefoldGK5AWNorthWhisker_sourceFibers`：選択P94Aの左右whiskerがそれぞれsource-saturatedなら、実際に指定されたP92Bのprior/suffixは元F55 φ-fiberを持つ。
2. `fivefoldGK5AWNorthOriginalLeftWhisker_bad_localizes`：元F55 priorで構成した北長短経路の左whiskerに**仮に**BadPairがあれば、内側の元北F55長短の同じ`f,g`にも本当のGK5AQ BadPairがある。
3. `fivefoldGK5AWNorthPhysicalLeftWhiskerReflectionGate`：上記反射障害局所化と、北C60の真正第五around Dart閉路、物理／圏論の04・43方向不一致、条件付き非単射性iffを同時保持。
4. `fivefoldGK5AWNorthPhysicalWhiskerSourceFiberGate`：左右選択whiskerの元F55 fiber条件と、同じ真正北物理境界・条件付き非単射性iffを同時保持。

物理gauge frameは欠損した元F55 Type証拠や元P89四セルを作成しない。全4定理の元P89→P94A非単射性は**真の元F55二証拠からなるBadPairが存在する場合の条件付き命題**であり、その存在は現段階では未証明。

## 6. 意義と次の定理境界：GK5AX（仮称）

- **内部証拠の復元条件**：選択P92Bの各局所inputが元F55 `φ`-fiberを持つか。
- **元4-cell反射条件**：本当の元P89四セルが存在し、選択P94A比較との間で局所BadPairがないか。
- **物理的compatibility**：真正C60第五Dart閉路・04/43物理方向・五行gaugeが保たれるか。

上記は独立条件であり、初めの1条件または物理compatibilityだけから残る2条件を無条件に導かない。GK5AWは元P89の8操作に対して「外側BadPairから内側BadPair」という局所必要条件を証明したが、選択P93Cの新規垂直単位・結合律などの高次反射をすべて完成したものではない。

次の**GK5AX**では、まだ原始source反射が不明なP93C/P94Aの追加vertical unit/assoc、P93Cの独立`old`境界、選択3証拠付きinterchangeに必要な真正元P89 4-cell反射データを、generator-indexedな証明書として設計する。そこから全構成子に対する条件付き帰納的反射・obstructionを検査する。Gray再構築、無条件source-saturation、無条件faithfulness/nonfaithfulnessは主張しない。

**Lean sources:** [GK5AW独立](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5AWContextGeneratorReflectionGate.lean)、[Qi v4.16](../../formal/KUOS/Architecture/QiWuxingGK5AWNorthContextReflectionV4_16.lean)、[GK5AV／Qi v4.15](GK5AV-Qi-v4_15-nested-P93C-vertical-source-vertex-chain.md)。
