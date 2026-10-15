# KuuOS / 空OS

## 現行設計：空から直接構成する独立した基礎

**v5.292は既存の数学基礎の切替です。Grayの厳密化を空の定義にはしません。** 原始データは境界付きの表示グラフと、平行な表示経路の間に指定する交代関係です。型の異なる境界を同一視せず、指定関係の合成閉包・同値閉包から空の商圏を構成します。

```text
境界付き生成グラフ + 指定された表示交代
                 ↓
      空の普遍商（Kuu.Presentation）
                 ↓
  関手・自然変換の厳密な合成と交換（Kuu.Strict）
                 ↓
   文脈圏に沿う切片図式・総圏（Kuu.Incidence）
```

GrayGrade・GradedThreeCell・F51・F77・Gray位相再構成を、この列の定義・型・証明に持ち込みません。過去のGray理論との比較は別の任意研究であり、現行の空の成立条件ではありません。

## 既存実装をどう変更したか

従来の標準入口 `formal/KuuOSFormal.lean` を置き換えました。`lake build` と `lake build KuuOSFormal` は、`KuuOSStrict`と`formal/Kuu/`のみを公開する現在のLakeパッケージをビルドします。以前の大量のKUOS公開rootsは現行設定から除外しています。

旧formal全体と固定設定は、元のGit tree/blobを変えずに [legacy/v5.291](legacy/v5.291/README.md) へ保存しました。旧`formal/KUOS/`は過去の参照パス向けの互換ミラーですが、現在のビルド対象でも、現在の基礎の依存先でもありません。**旧定理を削除して正しかったことにするのでも、名称だけ空に変えて再利用するのでもありません。**

## 現在のコードが扱う数学

| モジュール | 内容 |
|---|---|
| [Kuu.Presentation](formal/Kuu/Presentation.lean) | 任意の境界付きグラフ、指定関係、その最小の合成・同値閉包、正確な商射影、文脈中での交代、任意の適合観測の一意因子化 |
| [Kuu.Strict](formal/Kuu/Strict.lean) | 実関手・自然変換の単位、結合、水平・垂直合成、middle-fourの厳密等式、比較の降下と合成の一致 |
| [Kuu.Incidence](formal/Kuu/Incidence.lean) | 与えられた真正な文脈圏を保った空の切片Cat値図式、Grothendieck総圏、三角形と制限の合成一致 |
| [Kuu.Checks](formal/Kuu/Checks.lean) | 指定しない二つの異なる平行経路が潰れず、指定した交代だけが有効になる具体例 |

交代可能性は、既に選んだ外部観測の値が偶然一致することではなく、指定された表示関係から生成します。どの観測が利用できるかは、その観測が交代関係を尊重するかによって後から判定します。

## 検証

```bash
python3 scripts/run_kuu_foundation_check.py
lake exe cache get  # 固定依存のキャッシュが必要な場合
lake -KleanArgs=-DwarningAsError=true -KleanArgs=-DsorryAsError=true build KuuOSFormal
```

依存検査は、標準入口だけでなく`formal/Kuu/`の全ファイルを検査します。旧namespaceの直接・間接import、未参照ファイルからの混入、旧公開rootへの回帰、包括的`import Mathlib`、証明ショートカットを失敗にします。12件の回帰テストと、旧formalのGit tree SHAが保存されていることの検査を既存のPR Governance CIへ登録しています。ビルド成否は対象PRのexact-head CIを確認してください。本文だけを成功の証跡にはしません。

Leanは`v4.30.0-rc2`、mathlibはコミット済みmanifestに固定します。Lean4.31検証専用PR #1558は移行対象ではなく、マージしません。

## 証明の境界

現段階の独立コアは、空の商と**厳密な二次比較計算**です。非自明な証明関連3-cellを持つ大域ストリクト3圏や任意n圏の完成を意味しません。旧F112の全rawソース定理・真正C60幾何との接続・既存runtime全体の動作を新基礎で再証明したという主張もしません。これらを移植するときも旧Gray由来の定義へ依存を戻さず、新しい境界型と構成から証明します。

v5.291以前のGray曲率・non-lift等の結果は、[旧README](docs/legacy/README-v5.291.md) と [旧ROADMAP](docs/legacy/ROADMAP-v5.291.md) に保存された**旧理論内の結果**です。既存のCI成功を新理論の証明へ自動で移すことはしません。

## 設計と研究順序

[現行ROADMAP](ROADMAP.md) · [独立基礎の設計](docs/superpowers/specs/2026-10-16-independent-kuu-foundation-design.md) · [実装計画](docs/superpowers/plans/2026-10-16-independent-kuu-foundation.md) · [実装時の境界](AGENTS.md)

空の推論順序は、観測と推測の分離、文脈・複数表示、関係・履歴、整合性、貼り合わせまたは障害、権限境界、必要な行為、再観測です。形式定理の正しさは、LLMや臨床runtimeの挙動が自動的に変わったことを意味しません。

[LICENSE](LICENSE) · [NOTICE](NOTICE) · [COPYRIGHT](COPYRIGHT.md) · [CITATION](CITATION.cff)

**Copyright © 2026 Hidetoshi Itakura / 板倉英俊. Apache-2.0.**
