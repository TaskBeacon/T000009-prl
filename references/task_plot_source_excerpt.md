# 源码摘录（Probabilistic Reversal Learning (PRL) Task）

## 输入文件
- `README.md`: `E:\xhmhc\TaskBeacon\benchmark\runs\task_plot_redo\T000009-prl\README.md`
- `config.yaml`: `E:\xhmhc\TaskBeacon\benchmark\runs\task_plot_redo\T000009-prl\config\config.yaml`
- `run_trial.py`: `E:\xhmhc\TaskBeacon\benchmark\runs\task_plot_redo\T000009-prl\src\run_trial.py`

## 选定条件
- `AB`
- `BA`

## 关键试次流程证据
- `Fixation`：`fix_unit = make_unit(unit_label="fixation").add_stim(stim_bank.get("fixation"))`，随后 `set_trial_context(... phase="pre_choice_fixation", deadline_s=settings.fixation_duration, stim_id="fixation")`，最后 `fix_unit.show(duration=settings.fixation_duration)`；这是 600-800 ms 的注视阶段。
- `Choice`：`choice_unit = make_unit(unit_label="choice").add_stim(stima).add_stim(stimb)`，随后 `set_trial_context(... phase="choice_response_window", deadline_s=settings.choice_duration, stim_id="choice_pair")`，再调用 `capture_response(..., duration=settings.choice_duration)`；`AB` 条件下左侧为 `stima`、右侧为 `stimb`，`BA` 条件则左右互换。
- `Blank`：`make_unit(unit_label="blank").add_stim(stim_bank.get("blank")).show(duration=settings.blank_duration)`，没有 `set_trial_context(...)`；这是 400-600 ms 的空白间隔。
- `Feedback`：`make_unit(unit_label="feedback").add_stim(stim_bank.get(f"{outcome}_feedback")).show(duration=settings.feedback_duration)`，也没有 `set_trial_context(...)`；反馈内容由 `win`、`lose`、`no_response` 三种结果决定，持续 800 ms。

## 备注
- README 中的 `Block-Level Flow` 提供块级流程；试次级流程以 `run_trial.py` 为准。
- 本次重绘保留了两个条件时间线，因为 `AB` 与 `BA` 的唯一差异是左右刺激位置互换。
- 由于渲染器每个阶段只支持一个 `image_ref`，本次在 `benchmark/runs/task_plot_redo/T000009-prl/references/` 下额外生成了 `choice_pair_AB.png` 和 `choice_pair_BA.png`，用于展示选择阶段的左右刺激组合。
