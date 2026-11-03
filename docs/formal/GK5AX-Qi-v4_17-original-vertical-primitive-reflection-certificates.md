# F112-P94D3GK5AX / Qi v4.17 — 元F55垂直primitiveの反射証明書と真正北C60の条件付き降下

**正式証明記録：2026-11-03 JST。** Repository: `itakura-hidetoshi/KuuOS`、canonical theorem-bearing branch: `main`。厳密なauthority境界は **strict 空／独立Kuu → Qi**。元のF54双Nat・二カテゴリー・Blocks・F55 3-proof履歴、P89元4-proof、選択P92B/P93C/P94AのType値付き証拠、北C60の物理gauge frameとshadowを無条件に同一視しない。旧Lean構成子／公開定理を上書きしない。公開root **107**、保護PR **#1558 Draft／OPEN／未マージ**維持。Lean **v4.30.0-rc2**、mathlib **5450b53e5ddc75d46418fabb605edbf36bd0beb6**。

## 1. Exact-source CI／マージ正本

| 対象 | 確定結果 |
| --- | --- |
| 独立Kuu GK5AX定理 | [PR #3019](https://github.com/itakura-hidetoshi/KuuOS/pull/3019) **MERGED** |
| 独立GK5AX最終exact-source HEAD | `ee62d1f3f93f8cde8dae17c5e617bf450ee2e434` |
| 独立GK5AX squash/main SHA | `202f2039dfe432e179b3b36e449caaa97475a18b` |
| GK5AX exact-source Governance | [#41591523550](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41591523550) **30 / 30 SUCCESS** |
| GK5AX Strict Lean | **9,252 / 9,252 SUCCESS** |
| GK5AX `#print axioms` | **13宣言**、`sorryAx`なし。Lean/mathlib標準の許容公理範囲 |
| Qi v4.17定理 | [PR #3020](https://github.com/itakura-hidetoshi/KuuOS/pull/3020) **MERGED** |
| Qi v4.17最終exact-source HEAD | `16a1cecb884d85936fde33fdb47d04ef60621a39` |
| Qi v4.17 squash/main SHA | `a72d15cb74761ef0a6ca78ef30630e21d06929f4` |
| Qi v4.17 exact-source Governance | [#41592158198](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/41592158198) **30 / 30 SUCCESS** |
| Qi v4.17 Strict Lean | **10,179 / 10,179 SUCCESS** |
| Qi `#print axioms` | **5定理**、`sorryAx`なし |

最終exact-source CIで、新規Leanファイルにcompiler error/warningはない。新公理、`sorry`、`admit`、`native_decide`、Gray復元なし。検証対象ソースHEADとsquash/main SHAは別物として記録する。

## 2. 数学的焦点：選択P94A垂直3 primitiveと元P89の証拠境界

GK5AWは元P89に実在する8種類のcontext／whisker操作に沿ってBadPair障害を局所化した。一方で、選択P93C/P94Aには原始的に新しく付け加えた垂直単位・垂直結合律4-cellが存在する。元P89の13構成子には、その3 primitiveが同じ形で自動的に元証拠化されるという保証はない。

GK5AXは、**元F55からの真正3-cell履歴に添字付けした**選択4-cellを構成した：

- `nativeGK5AXSelectedLeftUnit f`：選択 `P94A(φ(trans(ident r,f)),φ(f))`
- `nativeGK5AXSelectedRightUnit f`：選択 `P94A(φ(trans(f,ident s)),φ(f))`
- `nativeGK5AXSelectedVerticalAssoc f g h`：選択 `P94A(φ(trans(trans(f,g),h)),φ(trans(f,trans(g,h))))`

これらは全て元F55の本当の証拠型・元F54の正確な端点を保持する。数値shadowの等式やP93C/P94A商等式から選択証明を捏造しない。構成される選択4-cellがあることは、元P89の4-cellが存在することと同値ではない。

## 3. 3 primitiveの厳密なGK5AQ BadPair iff 元P89反射不在

実在する元F55証拠`f`と、その真の元F54経路`r,s`を使う。元F55の恒等証拠は `ident r` と `ident s`。GK5AXは3 primitiveそれぞれについて、**選択P94A 4-cellが既に実在する**ことを踏まえ、次をLean4で証明した。

- `nativeGK5AXLeftUnit_bad_iff_noP89`
- `nativeGK5AXRightUnit_bad_iff_noP89`
- `nativeGK5AXAssoc_bad_iff_noP89`

例えば左垂直単位について：

    GK5AQBadPair(trans(ident r,f), f)
      ↔ ¬ Nonempty(P89(trans(ident r,f), f)).

右垂直単位および`f,g,h`の真の依存型結合律ペアも同様に成立する。**どのBadPairが実際に存在するとも、元P89でその原始証拠が実際に欠けているとも主張しない。** これは追加の元4-cell反射条件が本当に必要となる位置の正確な分類である。

## 4. 元P89原始反射証明書と有限型付き垂直語の条件付き降下

新しい依存型レコード`NativeGK5AXVerticalPrimitiveCertificates first last`は、元F55のあらゆる適切な経路添字について、**本当に元P89 Type値付き** leftUnit／rightUnit／assoc の3種類の4-cell証拠を持つ。そのインスタンスが実在するとは無条件に仮定・主張しない。

`nativeGK5AXVerticalCertificates_iff_noPrimitiveBad`では、**この真正元P89証明書レコードのNonempty ↔ 3 primitive familyすべてにGK5AQ BadPairが存在しない**ことを証明した。逆方向は古典的choiceで元4-cell存在証拠を選択する、存在レベルの定理であり、追加の構成算法を無条件に与えるものではない。

次に、元F55証拠で添字付けした真正有限垂直4-proof文法`NativeGK5AXSourceVerticalWord`を新しく定義：

    refl / symm / trans /
    leftUnit / rightUnit / assoc

この**限定した元証拠型付き文法**に対して、

- `NativeGK5AXSourceVerticalWord.toSelected`：各語の真正選択P94A 4-proofへの無条件解釈を再帰的に構成する。
- `NativeGK5AXSourceVerticalWord.toOriginal`：前述の**真の元P89原始証明書レコードが与えられた場合に限り**、各有限語を真正元P89 4-proofへ再帰的に解釈する。
- `NativeGK5AXSourceVerticalWord.both_witnesses`：同じ元F55端点について、条件付き元P89証拠と真正選択P94A証拠の両方が存在することを確定。
- `NativeGK5AXSourceVerticalWord.not_bad`：同条件下では、この有限垂直語の元証拠ペアはGK5AQ BadPairにならない。

これは`P94A`全19構成子の無条件正規化や、元P89→P94Aの無条件faithfulnessを証明したものではない。元P89 primitiveの証明書がないまま、選択P94Aの新規4-generatorを元sourceに帰属させることはできない。

## 5. 真正北C60／Qi v4.17

Qi側で5定理を追加し、元北四段pentagon long／shortのF54双Nat、二圏Blocks、元F55 Type証拠を保存した。

1. `fivefoldGK5AXNorthVerticalUnit_bad_iff_noP89`：北四段元F55証拠に対して左右2種類の原始垂直単位の反射不在iff BadPair。
2. `fivefoldGK5AXNorthVerticalAssoc_bad_iff_noP89`：任意の元北F54経路で型付き合成できる元F55三証拠のverticalAssoc反射不在iff BadPair。
3. `fivefoldGK5AXNorthVerticalWord_conditionalDescent`：**元P89 primitive証明書を明示的に与えた場合に限る**、任意の有限北元F55垂直語の真正元P89と選択P94Aの両証拠。
4. `fivefoldGK5AXNorthPhysicalVerticalUnitReflectionGate`：上の左右原始反射判定と真正北C60第五around Dart閉路・物理／圏論の04／43方向差・条件付き元P89→P94A非単射性iffを同時に保持。
5. `fivefoldGK5AXNorthPhysicalFiniteWordConditionalDescent`：条件付き有限語元P89降下と、同じ物理境界／条件付き非単射性iffの両立を証明。

五行物理gauge frameは欠けている元P89垂直primitive証明書を生成しない。元P89→P94A非単射性も実在すると断定しない。

## 6. 次の境界：GK5AY（仮称）

GK5AXによって、原始垂直生成元をsource-labeledにした場合の**exact BadPair／P89 lift**、3 familyの元反射証明書とその存在iff、限定有限垂直語の条件付きP89 descentが形式化された。

次は、元F55像所属が確認できる選択P93C`.old`境界と、primitive以外のwhisker・context・horizontal／interchangeの証明語合成を扱う**型付きgenerator-indexed reflection interface**を追加する。とくに`P92B.original f`と再帰的`φ(f)`の証拠型は同じ選択presentation内でも一般に定義的同一ではない。このseamを埋める真正4-cellが必要な場合にはそれを明示し、存在しない場合のobstructionを切り分ける。全面的P94A normal form、元P89→P94Aの無条件faithfulness/nonfaithfulness、Gray復元・無条件高次gluingは未証明のまま維持する。

**Lean sources:** [独立GK5AX](../../formal/Kuu/F112/PolygonNativeC60AQFullPentagonPhysicalNativeGK5AXVerticalPrimitiveReflectionCertificates.lean)、[Qi v4.17](../../formal/KUOS/Architecture/QiWuxingGK5AXNorthVerticalPrimitiveReflectionV4_17.lean)、[GK5AW／Qi v4.16正式記録](GK5AW-Qi-v4_16-generator-context-reflection-and-north-physical-fibers.md)。
