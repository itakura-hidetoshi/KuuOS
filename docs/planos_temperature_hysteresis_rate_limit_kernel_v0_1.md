# PlanOS Temperature Hysteresis and Rate-Limit Kernel v0.1

## 位置づけ

本層は、PlanOS v0.95 が校正した Qi temperature を、そのまま次周期へ適用せず、履歴振動と方向反転を考慮して有界に更新する。

## 更新則

目標温度と現在温度の差が有効 deadband 内なら温度を保持する。

差が deadband を超える場合は、上昇方向と下降方向に独立した一周期上限を適用する。

振動量と方向反転回数が増えるほど、deadband を広げ、許容 step を縮小する。

## 境界

更新後温度は、v0.95 の minimum temperature、maximum temperature、concentration-preserving ceiling の共通区間に射影する。

Qi temperature の変更は権限を増加させない。

履歴は read-only である。

更新は future-only であり、active-now または execution permission を生じない。

## Fail-closed

source calibration の欠落、非正温度、不正な境界、負の deadband、負の rate limit、負の振動量、負の方向反転回数、空の有効温度区間を遮断する。
