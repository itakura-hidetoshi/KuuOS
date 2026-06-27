# KuuOS Connection Candidate Review v0.63

## 目的

v0.63は、v0.62が生成した接続改善候補を、外部の人間または統治されたreviewerへ渡す境界です。

review結果はproduction適用権を与えません。

承認された場合でも、出力はstaging-ready receiptだけです。

## 完全束縛

review requestは次のdigestへ完全に束縛されます。

```text
source bundle
v0.62 proposal
selected candidate receipt
candidate connection
rollback target
```

review licenseはrequest digestと同じ五つのdigestへ再束縛されます。

どれか一つでも一致しない場合はblockedです。

## reviewer境界

reviewer classは`external_human_or_governed_supervisor`に限定します。

許可scopeは`stage_connection_candidate`だけです。

追加scopeを含むlicenseはauthority wideningとして拒否します。

有効epochの外にあるlicenseも拒否します。

## 決定

runtimeの決定は次の三つです。

```text
ADMIT
REJECT
DEFER
```

Leanでは`ADMIT`を`approve`として表現します。

`ADMIT`だけがstaging-readyになります。

`REJECT`と`DEFER`はstaging-readyになりません。

## 固定境界

```text
candidate only
production apply denied
state write denied
authority widening denied
rollback binding preserved
memory holonomy already protected by v0.62
```

## 検証

専用validatorはADMIT、REJECT、DEFERの三決定経路を検査します。

Lean coreは完全binding、candidate-only、production適用否定、state write否定、authority widening否定を形式化します。
