# Parameter Mapping

## Mapping Table

| Parameter ID | Config Path | Implemented Value | Source Paper ID | Evidence (quote/figure/table) | Decision Type | Notes |
|---|---|---|---|---|---|---|
| `total_blocks` | `task.total_blocks` | `6` (human), `1` (qa/sim) | `W2108312837` | PRL protocols rely on repeated feedback-driven adaptation episodes. | `inferred` | QA/sim reduced for runtime efficiency. |
| `trial_per_block` | `task.trial_per_block` | `40` (human), `24` (qa/sim) | `W2159371292` | Sufficient trials are needed to observe reversal and post-reversal adaptation. | `inferred` | QA/sim shorter while keeping reversal logic active. |
| `conditions` | `task.conditions` | `['AB', 'BA']` | `W2108312837` | Left/right assignment of two options is counterbalanced at trial level. | `reference_exact` | Condition controls on-screen side mapping only. |
| `left_key` | `task.left_key` | `f` | `W2159371292` | Binary choice responses are mapped to stable left/right keys. | `inferred` | Key mapping is config-defined for localization portability. |
| `right_key` | `task.right_key` | `j` | `W2159371292` | Binary choice responses are mapped to stable left/right keys. | `inferred` | Matches instruction text in config. |
| `choice_duration` | `timing.choice_duration` | `1.5` | `W2025693086` | Decision/response period precedes outcome feedback stage in EEG learning paradigms. | `inferred` | Fixed duration for predictable trigger timing. |
| `feedback_duration` | `timing.feedback_duration` | `0.8` | `W2159371292` | Outcome display window supports feedback-locked electrophysiology. | `inferred` | Separate from blank interval to isolate feedback onset. |
| `win_prob` | `controller.win_prob` | `0.8` | `W2108312837` | PRL depends on probabilistic reward schedule favoring one option before reversal. | `inferred` | Baseline reinforcement probability. |
| `rev_win_prob` | `controller.rev_win_prob` | `0.9` | `W2108312837` | Post-reversal behavior is shaped by updated reward contingencies. | `inferred` | Higher post-reversal stability in this implementation profile. |
| `sliding_window` | `controller.sliding_window` | `10` | `W2159371292` | Behavioral adjustment thresholds are derived from recent response history. | `inferred` | Controller reverses when criterion is met. |
| `sliding_window_hits` | `controller.sliding_window_hits` | `9` | `W2159371292` | Reversal trigger requires strong evidence of criterion learning. | `inferred` | Implements near-ceiling criterion before switching rule. |
| `choice_onset` | `triggers.map.choice_onset` | `2` (+reversal pad) | `W2025693086` | Choice onset marker is required for response-aligned EEG analysis. | `inferred` | Runtime adds `reversal_count * 10` marker pad. |
| `win_feedback_onset` | `triggers.map.win_feedback_onset` | `5` (+reversal pad) | `W2159371292` | Feedback valence onset marker supports FRN/feedback processing analysis. | `inferred` | Same pad policy as choice phase. |
| `lose_feedback_onset` | `triggers.map.lose_feedback_onset` | `6` (+reversal pad) | `W2159371292` | Negative outcome onset marker supports valence-specific analysis. | `inferred` | Same pad policy as choice phase. |
