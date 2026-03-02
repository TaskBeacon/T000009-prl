# Task Logic Audit

## 1. Paradigm Intent

- Task: Probabilistic reversal learning (PRL) task with two simultaneous options.
- Primary construct: Feedback-guided adaptation and cognitive flexibility under changing reward contingencies.
- Manipulated factors:
  - Option-side assignment (`AB` vs `BA`)
  - Reward contingency phase (before vs after reversal)
- Dependent measures:
  - Choice accuracy relative to latent correct option
  - Response time and omissions
  - Reward/loss trajectory and reversal count
  - Feedback-aligned EEG events
- Key citations:
  - W2159371292
  - W2108312837
  - W2025693086

## 2. Block/Trial Workflow

### Block Structure

- Total blocks: 6 in human mode; 1 in qa/sim profiles.
- Trials per block: 40 in human mode; 24 in qa/sim profiles.
- Randomization/counterbalancing:
  - `BlockUnit.generate_conditions()` alternates `AB` and `BA` assignment by config-driven condition generation.
- Condition weight policy:
  - `task.condition_weights` is not explicitly defined.
  - `TaskSettings.resolve_condition_weights()` is not used.
  - Default/even condition generation is used for `AB`/`BA`.
- Condition generation method:
  - Built-in `BlockUnit.generate_conditions()`.
  - No custom generator is required; trial semantics are representable by side-assignment condition tokens.
  - Generated condition data shape passed into `run_trial.py`: scalar token (`AB` or `BA`).
- Runtime-generated trial values (if any):
  - Reward outcome sampled each trial by `np.random.rand()` using controller-dependent win probability.
  - Trigger pad is derived from `controller.reversal_count` to mark reversal epochs.

### Trial State Machine

1. State name: `pre_choice_fixation`
   - Onset trigger: `fixation_onset` (+reversal pad)
   - Stimuli shown: fixation cross
   - Valid keys: `task.key_list` (not scored)
   - Timeout behavior: auto-advance after `timing.fixation_duration`
   - Next state: `choice_response_window`
2. State name: `choice_response_window`
   - Onset trigger: `choice_onset` (+reversal pad)
   - Stimuli shown: two symbols (`stima`, `stimb`) with side mapping from condition
   - Valid keys: `f`, `j`
   - Timeout behavior: if no key before deadline, emit `no_response` (+pad) and proceed as omission
   - Next state: `post_choice_blank`
3. State name: `post_choice_blank`
   - Onset trigger: none
   - Stimuli shown: blank
   - Valid keys: none (not scored)
   - Timeout behavior: auto-advance after `timing.blank_duration`
   - Next state: `feedback`
4. State name: `feedback`
   - Onset trigger: `win_feedback_onset` / `lose_feedback_onset` / `no_response_feedback_onset` (+pad)
   - Stimuli shown: outcome text based on sampled result
   - Valid keys: none
   - Timeout behavior: auto-close after `timing.feedback_duration`
   - Next state: trial end

## 3. Condition Semantics

- Condition ID: `AB`
- Participant-facing meaning: left option = `stima`, right option = `stimb`.
- Concrete stimulus realization: two image symbols with fixed left/right placement.
- Outcome rules: response correctness depends on controller `current_correct` and selected side.

- Condition ID: `BA`
- Participant-facing meaning: left option = `stimb`, right option = `stima`.
- Concrete stimulus realization: same two symbols with swapped positions.
- Outcome rules: response correctness depends on controller `current_correct` and selected side.

Participant-facing text/stimuli source:

- Participant-facing text source: `config/*.yaml` stimuli (`instruction_text`, feedback texts, break/goodbye text).
- Why this source is appropriate for auditability: language and symbol labels are centralized and modifiable without runtime code edits.
- Localization strategy: swap config text/font mappings while keeping trial logic unchanged.

## 4. Response and Scoring Rules

- Response mapping:
  - `f` = choose left symbol
  - `j` = choose right symbol
- Response key source: config (`task.left_key`, `task.right_key`, `task.key_list`).
- If code-defined, why config-driven mapping is not sufficient: not applicable.
- Missing-response policy: omission produces `no_response` outcome and negative score delta.
- Correctness logic:
  - Determine which side corresponds to `controller.current_correct`.
  - Compare participant key with expected side key.
- Reward/penalty updates:
  - If choice is correct: reward with probability `win_prob` (or `rev_win_prob` after first reversal), otherwise loss.
  - If choice is incorrect: inverse reward probability.
  - No response: fixed loss.
- Running metrics:
  - Per-trial `choice_delta` accumulated for block and total scores.
  - Controller updates hit history and reversal state.

## 5. Stimulus Layout Plan

- Screen name: `choice_response_window`
- Stimulus IDs shown together: `stima`, `stimb`, optional highlight rectangle
- Layout anchors (`pos`): left `(-4, 0)`, right `(4, 0)`
- Size/spacing (`height`, width, wrap): image size `[5, 5]` deg; highlight rect size `3x4`
- Readability/overlap checks: symmetric placement prevents overlap in 1920x1080 fullscreen
- Rationale: explicit left/right choice mapping with equal visual salience

- Screen name: `feedback`
- Stimulus IDs shown together: one of `win_feedback`, `lose_feedback`, `no_response_feedback`
- Layout anchors (`pos`): centered text
- Size/spacing (`height`, width, wrap): text-only single stimulus
- Readability/overlap checks: no concurrent text overlap
- Rationale: isolate outcome valence for feedback-related EEG effects

## 6. Trigger Plan

- `exp_onset` (`98`), `exp_end` (`99`): session boundaries.
- `block_onset` (`100`), `block_end` (`101`): block boundaries.
- `fixation_onset` (`1`) + reversal pad.
- `choice_onset` (`2`) + reversal pad.
- `key_press` (`3`) + reversal pad.
- `no_response` (`4`) + reversal pad.
- `win_feedback_onset` (`5`) + reversal pad.
- `lose_feedback_onset` (`6`) + reversal pad.
- `no_response_feedback_onset` (`7`) + reversal pad.

Reversal pad rule:
- pad = `controller.reversal_count * 10`.
- All trial-phase trigger codes are offset by pad to mark reversal epoch.

## 7. Architecture Decisions (Auditability)

- `main.py` runtime flow style: single mode-aware flow (`human|qa|sim`) with shared setup order.
- `utils.py` used?: yes.
- If yes, exact purpose: `Controller` encapsulates reversal-state updates and win-probability policy.
- Custom controller used?: yes.
- If yes, why PsyFlow-native path is insufficient: reversal criterion depends on rolling hit history and dynamic latent mapping.
- Legacy/backward-compatibility fallback logic required?: no.

## 8. Inference Log

- Decision: Use `sliding_window=10` and `sliding_window_hits=9` as reversal trigger.
- Why inference was required: references motivate performance-driven reversals but implementation threshold is profile-specific.
- Citation-supported rationale: W2108312837 and W2159371292 describe adaptive feedback-based learning phases requiring high-confidence criterion before policy shift.

- Decision: Add trigger marker pad by reversal count.
- Why inference was required: references support phase-sensitive EEG analysis but do not prescribe a fixed coding scheme.
- Citation-supported rationale: W2025693086 and W2159371292 emphasize outcome/event timing separation, motivating explicit epoch coding.
