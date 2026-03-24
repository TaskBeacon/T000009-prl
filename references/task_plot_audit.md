# Task Plot 审计

- generated_at: 2026-03-23T23:24:44
- mode: existing
- task_path: E:\xhmhc\TaskBeacon\benchmark\runs\task_plot_redo\T000009-prl

## 1. 输入与来源

- `README.md`: `E:\xhmhc\TaskBeacon\benchmark\runs\task_plot_redo\T000009-prl\README.md`
- `config.yaml`: `E:\xhmhc\TaskBeacon\benchmark\runs\task_plot_redo\T000009-prl\config\config.yaml`
- `run_trial.py`: `E:\xhmhc\TaskBeacon\benchmark\runs\task_plot_redo\T000009-prl\src\run_trial.py`

## 2. 从 README 提取的证据

- README 同时给出了 `Block-Level Flow` 和 `Trial-Level Flow`。
- `Trial-Level Flow` 明确包含 `Fixation`、`Choice`、`Blank Screen`、`Feedback Display` 四个步骤。
- `AB` / `BA` 条件差异主要体现在左右刺激位置互换。

## 3. 从 config/source 提取的证据

- `AB`：`fix_unit = make_unit(unit_label="fixation").add_stim(stim_bank.get("fixation"))`，随后 `set_trial_context(... phase="pre_choice_fixation", deadline_s=settings.fixation_duration, stim_id="fixation")`，最后 `show(duration=settings.fixation_duration)`。
- `AB`：`choice_unit = make_unit(unit_label="choice").add_stim(stima).add_stim(stimb)`，随后 `set_trial_context(... phase="choice_response_window", deadline_s=settings.choice_duration, stim_id="choice_pair")`，再调用 `capture_response(..., duration=settings.choice_duration)`；此时左侧是 `stima`，右侧是 `stimb`。
- `AB`：`make_unit(unit_label="blank").add_stim(stim_bank.get("blank")).show(duration=settings.blank_duration)`，没有 `set_trial_context(...)`，对应反馈前空白间隔。
- `AB`：`make_unit(unit_label="feedback").add_stim(stim_bank.get(f"{outcome}_feedback")).show(duration=settings.feedback_duration)`，没有 `set_trial_context(...)`，对应结果反馈。
- `BA`：与 `AB` 的阶段顺序一致，但 `choice_unit` 内左右刺激顺序相反，左侧是 `stimb`，右侧是 `stima`。
- `BA`：`blank` 与 `feedback` 的时序、持续时间和来源与 `AB` 相同。

## 3b. 需要显式记录的警告

- `blank`：participant-visible phase inferred from `show()` because `set_trial_context(...)` is missing.
- `feedback`：participant-visible phase inferred from `show()` because `set_trial_context(...)` is missing.

## 4. 映射到 task_plot_spec

- `root_key`: `task_plot_spec`
- `spec_version`: `0.2`
- 采用“一条条件一条时间线”的集合式图形。
- 保留 `AB` 与 `BA` 两条时间线，因为它们在选择阶段的左右刺激位置不同。
- `Fixation`、`Blank` 和 `Feedback` 共享相同的时序逻辑，但选择阶段的组合图不同。
- 由于渲染器每个阶段只支持一个 `image_ref`，本次在 `references/` 下额外生成了组合图 `choice_pair_AB.png` 与 `choice_pair_BA.png`，用于呈现左右刺激顺序。

## 5. 样式决策与理由

- 继续使用 timeline collection，因为这是 task-plot 的固定图型。
- 这个任务的关键信息是试次级时序和左右刺激位置切换，因此需要分别保留 `AB` 和 `BA`。
- 组合图比抽象文本更接近参与者实际看到的选择界面。

## 6. 渲染参数与约束

- `output_file`: `task_flow.png`
- `dpi`: `300`
- `max_conditions`: `2`
- `screens_per_timeline`: `4`
- `screen_overlap_ratio`: `0.1`
- `screen_slope`: `0.08`
- `screen_slope_deg`: `25.0`
- `screen_aspect_ratio`: `1.4545454545454546`
- `left_margin`: `0.2`
- `right_margin`: `0.03`
- `top_margin`: `0.03`
- `bottom_margin`: `0.05`
- `auto_width`: `false`
- `width_in`: `16.0`
- `qa_mode`: `local`
- `auto_layout_feedback`:
  - `layout pass 1: crop-only; left=0.052, right=0.060, blank=0.164`
- `auto_layout_feedback_records`:
  - `pass: 1`
    `metrics`: `{'left_ratio': 0.0517, 'right_ratio': 0.0597, 'blank_ratio': 0.1636}`
- `validator_warnings`: 无

## 7. 输出文件与校验和

- `E:\xhmhc\TaskBeacon\benchmark\runs\task_plot_redo\T000009-prl\references\task_plot_spec.yaml`: `sha256=f2848f3cb6e62611f939ded209b498b8cb7a36287558837229f8ac943c5d2c18`
- `E:\xhmhc\TaskBeacon\benchmark\runs\task_plot_redo\T000009-prl\references\task_plot_spec.json`: `sha256=04d24db1ae08b688960a1d708f98b3a475df98154fa359d0967a74610d51713a`
- `E:\xhmhc\TaskBeacon\benchmark\runs\task_plot_redo\T000009-prl\references\task_plot_source_excerpt.md`: `sha256=9fa7819d22d17c02cf6040ed8571918c9356df7a861106a0bf7f9a33a46057e7`
- `E:\xhmhc\TaskBeacon\benchmark\runs\task_plot_redo\T000009-prl\references\choice_pair_AB.png`: `sha256=b1fa19f6c88f4fc9c10422ad1afb5821376173360cb1d1d06aa9afa80611cad9`
- `E:\xhmhc\TaskBeacon\benchmark\runs\task_plot_redo\T000009-prl\references\choice_pair_BA.png`: `sha256=805927db8898ef14d2445cbd283170e6c5ee1871f767eb2b17447e877f187644`
- `E:\xhmhc\TaskBeacon\benchmark\runs\task_plot_redo\T000009-prl\task_flow.png`: `sha256=0efb2f827f18d9f818a3d7c55316b4d105547d03085def4e04b93d1b4cd068c0`
- `E:\xhmhc\TaskBeacon\benchmark\reports\task_plot_redo_T000009_prl_summary.md`: `sha256=23bb09a3877c660894727954c53297344f2cc5fab8a18d721a99388cc82861d6`

## 8. 推断项与不确定项

- `blank` 和 `feedback` 是从 `show()` 调用中恢复出的 participant-visible phase，而不是 `set_trial_context(...)` 直接提供的上下文阶段。
- `choice_pair_AB.png` 与 `choice_pair_BA.png` 属于渲染辅助素材，用于把左右刺激位置明确画出来。
- `Feedback` 的实际文字会随 `outcome` 变化，但图中使用的是覆盖所有结果的通用示意文本。
