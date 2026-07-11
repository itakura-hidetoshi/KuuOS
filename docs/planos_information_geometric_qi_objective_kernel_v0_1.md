# PlanOS Information-Geometric Qi Objective Kernel v0.1

## 定義

PlanOSの目標を、固定された到達点ではなく、許容される未来経路の確率分布を形成する目的構造として定義する。

PlanOSは未来を一点として選択しない。

現在状態、非マルコフ履歴、Qi process tensor、使命、資源、検証条件、関係構造、権限境界から、未来経路の幾何と確率分布を構成する。

DecisionOSは離散候補場から候補を選択する。

ActOSは選択結果を実行可能性境界へ接続する。

LearnOSは観測差分を次周期の計量、作用、事前分布へ返す。

## 拡張状態

```text
s_t = (x_t, theta_t, Q_t, H_t, C_t, A_t)
```

`theta_t` は目標構造、手順、観測点、検証条件、資源配分、停止条件、rollback条件、リスク、可逆性、関係構造を保持する。

`Q_t` と `H_t` は計画を直接選択せず、計画空間の計量と作用を条件づける。

`A_t` は最適化対象ではない。

## 情報幾何

未来経路分布を `p_theta(gamma | s_t)` とし、計画状態を統計多様体上の点として扱う。

Fisher情報計量に相当する離散計量は、候補間の文章差ではなく、未来可能性分布の変化量を表す。

Qiと履歴は基底計量を次のように変形する。

```text
switch metric += recovery + hysteresis + oscillation
reroute metric -= stagnation only when reroute evidence exists
```

すべての計量成分は非負に保たれる。

Qiだけでreroute抵抗を低下させることはできず、観測または履歴証拠を必要とする。

## Plan action

各有限経路に対して次の作用成分を保持する。

```text
transition action
mission potential
risk potential
resource potential
authority potential
verification potential
Wa relational potential
Qi potential
history potential
```

許容経路では総作用を各成分の和とする。

権限境界外の経路は不許容とし、総作用を無限大として確率質量をゼロにする。

Qi temperatureは探索幅だけを変え、権限境界を緩和しない。

## Euclidean経路重み

実装では有限経路集合上で次を用いる。

```text
weight(path) = exp(-total_action / qi_temperature)
```

不許容経路の重みはゼロである。

許容経路の重みを分配関数で正規化し、総質量を1とする。

候補質量は、同一候補型に属する経路質量の総和として定義する。

## 離散候補場

```text
continue
strengthen
repair
slow_down
reobserve
reroute
hold
terminate_candidate
```

候補選択後も候補場を消去しない。

選択されなかった候補IDは、retained candidateとして次周期記録に残す。

許容されるhold経路が存在する場合、hold質量を設定された下限以上に保つ。

## 更新境界

生成される `PlanObjectiveUpdate` は次を満たす。

```text
future_only = true
active_now = false
execution_permission = false
```

Plan commitは現在周期を変更しない。

Plan commitは実行権限を付与しない。

経路最適化による権限増加を禁止する。

## 処理相との対応

```text
BIND          current state and prior distribution
HISTORY       non-Markov history potential
QI_CONDITION  Qi and history conditioned metric
GENERATE      finite path field
CONSTRAIN     admissible path restriction
DELIBERATE    candidate mass and relational evidence
SYNTHESIZE    next plan basis
COMMIT_NEXT   future-only distribution update
```

## 実装スキーマ

### PlanObjectiveGeometry

計画多様体、パラメータスキーマ、基底計量、Qi条件付き計量、履歴条件付き計量、現在分布、目標領域、KL divergence、entropy weight、action weightを保持する。

### PlanPathAction

経路ID、候補ID、各作用成分、総作用、許容性、action digestを保持する。

### PlanPathDistribution

source state digest、path action digests、partition function、Qi temperature、正規化経路重み、候補質量、hold質量、distribution digestを保持する。

### PlanObjectiveUpdate

prior distribution digest、選択候補と質量、保持候補、異論証拠、次分布、次計画基底、future-only境界、非実行境界を保持する。

## 不変条件

```text
history source is read-only
Qi conditioning grants no authority
authority-forbidden paths have zero mass
normalized path mass sums to one
candidate mass is nonnegative
hold mass is preserved when admissible
selected candidate belongs to candidate field
retained candidates survive selection
future-only update preserves current cycle
plan commit is not execution
```

## 最終定義

PlanOSは未来を決定しない。

PlanOSは、現在、履歴、Qi、使命、関係性、資源、権限から、許容される未来経路の幾何と確率分布を形成する。

したがってPlanOSは、未来可能性の情報幾何を形成する非マルコフ計画場OSとして位置づけられる。
