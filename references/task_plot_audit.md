# Task Plot Audit

- generated_at: 2026-03-10T00:17:32
- mode: existing
- task_path: E:\Taskbeacon\T000009-prl

## 1. Inputs and provenance

- E:\Taskbeacon\T000009-prl\README.md
- E:\Taskbeacon\T000009-prl\config\config.yaml
- E:\Taskbeacon\T000009-prl\src\run_trial.py

## 2. Evidence extracted from README

- Trial-Level Flow table not found; run_trial.py used as primary source.

## 3. Evidence extracted from config/source

- AB: phase=pre choice fixation, deadline_expr=settings.fixation_duration, response_expr=n/a, stim_expr='fixation'
- AB: phase=choice response window, deadline_expr=settings.choice_duration, response_expr=settings.choice_duration, stim_expr='choice_pair'
- BA: phase=pre choice fixation, deadline_expr=settings.fixation_duration, response_expr=n/a, stim_expr='fixation'
- BA: phase=choice response window, deadline_expr=settings.choice_duration, response_expr=settings.choice_duration, stim_expr='choice_pair'

## 4. Mapping to task_plot_spec

- timeline collection: one representative timeline per unique trial logic
- phase flow inferred from run_trial set_trial_context order and branch predicates
- participant-visible show() phases without set_trial_context are inferred where possible and warned
- duration/response inferred from deadline/capture expressions
- stimulus examples inferred from stim_id + config stimuli
- conditions with equivalent phase/timing logic collapsed and annotated as variants
- root_key: task_plot_spec
- spec_version: 0.2

## 5. Style decision and rationale

- Single timeline-collection view selected by policy: one representative condition per unique timeline logic.

## 6. Rendering parameters and constraints

- output_file: task_flow.png
- dpi: 300
- max_conditions: 4
- screens_per_timeline: 6
- screen_overlap_ratio: 0.1
- screen_slope: 0.08
- screen_slope_deg: 25.0
- screen_aspect_ratio: 1.4545454545454546
- qa_mode: local
- auto_layout_feedback:
  - layout pass 1: crop-only; left=0.031, right=0.031, blank=0.146
- auto_layout_feedback_records:
  - pass: 1
    metrics: {'left_ratio': 0.0308, 'right_ratio': 0.0308, 'blank_ratio': 0.1456}

## 7. Output files and checksums

- E:\Taskbeacon\T000009-prl\references\task_plot_spec.yaml: sha256=fbb1aa2e57b597537128b647a0d2bffb9845de024d923fd2e6cbf7e85a1e1dc9
- E:\Taskbeacon\T000009-prl\references\task_plot_spec.json: sha256=171af4c83bc3a704ce3d7733ad6caf7fb63800d1a2247bdea9e4b171d58bac17
- E:\Taskbeacon\T000009-prl\references\task_plot_source_excerpt.md: sha256=81a183817c015fad29663873cba536e7bfa03e05776af25cb2e08d8445c848dd
- E:\Taskbeacon\T000009-prl\task_flow.png: sha256=7216a9687f1fc4d15583ce49ef2732a4199a5f664ccfdb5c8a9c6df54b21edec

## 8. Inferred/uncertain items

- collapsed equivalent condition logic into representative timeline: AB, BA
- unparsed if-tests defaulted to condition-agnostic applicability: condition_id == 'AB'; controller.current_correct == 'stima'; hit; respond
