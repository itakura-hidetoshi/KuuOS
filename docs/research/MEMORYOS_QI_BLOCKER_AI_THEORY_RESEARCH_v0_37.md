# MemoryOS、気のプロセステンソル、ブロッカー理論に関連するAI理論調査 v0.37

## 調査目的

本調査は、MemoryOS を単なる長期保存機構ではなく、時間相関を保持し、安全制約の下で予測候補を返す非マルコフ記憶系へ発展させるために行った。

論文の理論を空OSの既存概念と同一視せず、採用できる構造だけを限定して取り込む。

気のプロセステンソルは量子 process tensor の物理的主張そのものではない。

ブロッカー理論は safe reinforcement learning の shield や runtime assurance と同一ではない。

WORLD は reinforcement learning の world model と同一ではない。

以下の対応は、設計上の限定的な写像である。

## 非マルコフ過程

### Non-Markovian quantum processes: complete framework and efficient characterisation

- Authors: Felix A. Pollock et al.
- arXiv: `1512.00589`
- URL: `https://arxiv.org/abs/1512.00589`
- 採用点: 多時点過程を一時点の状態へ潰さず、操作可能な履歴相関として表現する。
- MemoryOSへの反映: `source_qi_process_tensor_trace_digest` を保存し、current snapshot が process history を置換しない。
- 非採用点: MemoryOS が量子過程であるという主張はしない。

### Learning Causal State Representations of Partially Observable Environments

- Authors: Amy Zhang et al.
- arXiv: `1906.10437`
- URL: `https://arxiv.org/abs/1906.10437`
- 採用点: 履歴全体を、将来観測予測に必要な候補状態へ圧縮する。
- MemoryOSへの反映: `OBSERVABLE_PREDICTIVE_STATE_CANDIDATE` を導入する。
- 非採用点: predictive state を潜在状態の真値へ昇格しない。

### PAC Reinforcement Learning for Predictive State Representations

- Authors: Wenhao Zhan et al.
- arXiv: `2207.05738`
- URL: `https://arxiv.org/abs/2207.05738`
- 採用点: 部分観測環境を、観測可能量に基づく予測状態として扱う。
- MemoryOSへの反映: predictive state に `observable_history_digest`、`prediction_target`、`uncertainty_milli` を要求する。
- 非採用点: MemoryOS runtime に PAC 最適性や sample complexity を主張しない。

## 認知アーキテクチャと階層記憶

### Cognitive Architectures for Language Agents

- Authors: Theodore R. Sumers et al.
- arXiv: `2309.02427`
- URL: `https://arxiv.org/abs/2309.02427`
- 採用点: working、episodic、semantic、procedural memory を分離する。
- MemoryOSへの反映: 四種類の memory record と retention route を型付きで区別する。
- 非採用点: semantic memory を事実、procedural memory を実行許可とはみなさない。

### MemGPT: Towards LLMs as Operating Systems

- Authors: Charles Packer et al.
- arXiv: `2310.08560`
- URL: `https://arxiv.org/abs/2310.08560`
- 採用点: context window と外部記憶を階層化し、制御フローを記憶管理から分離する。
- MemoryOSへの反映: retrieval は capsule から候補文脈だけを返し、実行や plan activation を行わない。
- 非採用点: 無制限文脈や無制限永続性を主張しない。

### MemOS: An Operating System for Memory-Augmented Generation in Large Language Models

- Authors: Zhiyu Li et al.
- arXiv: `2505.22101`
- URL: `https://arxiv.org/abs/2505.22101`
- 採用点: memory を first-class resource として表現、組織化、追跡、統治する。
- MemoryOSへの反映: record provenance、memory inventory、append-only capsule lineage、明示的 lifecycle status を導入する。
- 非採用点: parametric memory の書換えやモデル重み更新は実装しない。

### Generative Agents: Interactive Simulacra of Human Behavior

- Authors: Joon Sung Park et al.
- arXiv: `2304.03442`
- URL: `https://arxiv.org/abs/2304.03442`
- 採用点: observation、memory retrieval、reflection、planning を分離する。
- MemoryOSへの反映: semantic consolidation は proposal に限定し、automatic consolidation を禁止する。
- 非採用点: reflection の出力を真理や権威へ昇格しない。

### Reflexion: Language Agents with Verbal Reinforcement Learning

- Authors: Noah Shinn et al.
- arXiv: `2303.11366`
- URL: `https://arxiv.org/abs/2303.11366`
- 採用点: 失敗やフィードバックを episodic memory として次回判断へ渡す。
- MemoryOSへの反映: procedural reuse を candidate として保存する。
- 非採用点: 保存された反省文を自動実行規則にしない。

### LEGOMem: Modular Procedural Memory for Multi-agent LLM Systems for Workflow Automation

- Authors: Dongge Han et al.
- arXiv: `2510.04851`
- URL: `https://arxiv.org/abs/2510.04851`
- 採用点: procedural memory を再利用可能な単位へ分け、配置先と利用者を区別する。
- MemoryOSへの反映: procedural record に `PROCEDURAL_REUSE_CANDIDATE` を要求する。
- 非採用点: procedural memory 自体に delegation authority を与えない。

### Zep: A Temporal Knowledge Graph Architecture for Agent Memory

- Authors: Preston Rasmussen et al.
- arXiv: `2501.13956`
- URL: `https://arxiv.org/abs/2501.13956`
- 採用点: 時間変化と過去関係を消さずに保持する。
- MemoryOSへの反映: contradiction residue と append-only lineage を保存する。
- 非採用点: グラフ統合によって competing claims を一つの事実へ潰さない。

## ブロッカーと安全シールド

### Safe Reinforcement Learning via Shielding

- Authors: Mohammed Alshiekh et al.
- arXiv: `1708.08611`
- URL: `https://arxiv.org/abs/1708.08611`
- 採用点: agent の選択前または選択後に safety specification を強制する shield を置く。
- MemoryOSへの反映: capability return の前に blocker shield gate を必須化する。
- 非採用点: shield の存在を blocker discharge とみなさない。

### Safe Reinforcement Learning via Shielding under Partial Observability

- Authors: Steven Carr et al.
- arXiv: `2204.00755`
- URL: `https://arxiv.org/abs/2204.00755`
- 採用点: 部分観測下では安全判定と性能の双方に履歴状態が必要になる。
- MemoryOSへの反映: predictive history が不十分なら `REOBSERVE_PREDICTIVE_STATE` へ送る。
- 非採用点: shield を解除する学習機構は導入しない。

### The Black-Box Simplex Architecture for Runtime Assurance of Autonomous CPS

- Authors: Usama Mehmood et al.
- arXiv: `2102.12981`
- URL: `https://arxiv.org/abs/2102.12981`
- 採用点: advanced controller が危険な場合に安全な fallback へ切り替える。
- MemoryOSへの反映: `READ_ONLY_CONTEXT_OR_REOBSERVE` を safe fallback として固定する。
- 非採用点: MemoryOS を制御装置や実行 controller とみなさない。

## WORLDモデルと反事実候補

### Mastering Diverse Domains through World Models

- Authors: Danijar Hafner et al.
- arXiv: `2301.04104`
- URL: `https://arxiv.org/abs/2301.04104`
- 採用点: environment model 上で future scenario を想像し、候補を比較する。
- MemoryOSへの反映: sourced WORLD fragment から `world_imagination_candidates` を生成可能にする。
- 非採用点: imagination candidate を WORLD の真値、commit、execution authority にしない。

## 近年の補助的証拠

以下は新しい preprint であり、v0.37 の境界を決める補助資料としてのみ扱う。

### Episodic-Semantic Memory Architecture for Long-Horizon Scientific Agents

- arXiv: `2605.17625`
- URL: `https://arxiv.org/abs/2605.17625`
- 補助点: long-horizon workflow では episodic と semantic consolidation の分離が重要になる。

### Multi-Layered Memory Architectures for LLM Agents

- arXiv: `2603.29194`
- URL: `https://arxiv.org/abs/2603.29194`
- 補助点: working、episodic、semantic layer と adaptive retrieval gate の組合せを検討する。

これらの結果は再現、査読、一般化範囲を別途確認する必要がある。

## v0.37への統合原則

```text
raw history != current snapshot
predictive state candidate != hidden-state truth
semantic consolidation candidate != fact
procedural memory candidate != execution authority
reflection != verification
shield active != blocker discharged
safe fallback != task success
WORLD imagination != sourced WORLD
WORLD imagination != WORLD commit
contradiction residue != noise to erase
retrieval != plan activation
CI success != empirical truth
```

## 実装した進化

- working、episodic、semantic、procedural の四層 memory record
- source digest、confidence、uncertainty、lifecycle status の明示
- semantic と procedural の automatic promotion 禁止
- observable-history-bound predictive state candidate
- contradiction residue の append-only 保存
- blocker shield gate を通過する retrieval
- read-only context または reobserve への safe fallback
- sourced WORLD と分離した counterfactual imagination candidate
- capsule lineage の append-only 検査
- truth、execution、plan activation、ActOS、WORLD commit の非権限固定

## 証明状態

論文との対応は設計根拠であり、論文の定理がそのまま MemoryOS に移植されたことを意味しない。

Runtime test は宣言された入力クラスに対する回帰検査である。

Lean theorem は bool boundary の型付き整合性を証明する。

経験的性能、安全性、臨床的妥当性、物理的 WORLD の正しさは証明しない。
