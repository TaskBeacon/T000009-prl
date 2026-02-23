from functools import partial

import numpy as np

from psyflow import StimUnit, set_trial_context, next_trial_id
from .utils import Controller

# trial stages use task-specific phase labels via set_trial_context(...)


def run_trial(
    win,
    kb,
    settings,
    condition,
    stim_bank,
    controller,
    trigger_runtime=None,
    block_id=None,
    block_idx=None,
):
    """Run one PRL trial."""
    trial_id = next_trial_id()
    trial_data = {"condition": condition}
    make_unit = partial(StimUnit, win=win, kb=kb, runtime=trigger_runtime)
    marker_pad = controller.reversal_count * 10

    # phase: pre_choice_fixation
    # phase: pre_choice_fixation
    fix_unit = make_unit(unit_label="fixation").add_stim(stim_bank.get("fixation"))
    set_trial_context(
        fix_unit,
        trial_id=trial_id,
        phase="pre_choice_fixation",
        deadline_s=settings.fixation_duration,
        valid_keys=list(settings.key_list),
        block_id=block_id,
        condition_id=str(condition),
        task_factors={"condition": str(condition), "stage": "pre_choice_fixation", "block_idx": block_idx},
        stim_id="fixation",
    )
    fix_unit.show(
        duration=settings.fixation_duration,
        onset_trigger=settings.triggers.get("fixation_onset") + marker_pad,
    ).to_dict(trial_data)

    # phase: choice_response_window
    if condition == "AB":
        stima = stim_bank.rebuild("stima", pos=(-4, 0))
        stimb = stim_bank.rebuild("stimb", pos=(4, 0))
    else:
        stimb = stim_bank.rebuild("stimb", pos=(-4, 0))
        stima = stim_bank.rebuild("stima", pos=(4, 0))

    if controller.current_correct == "stima":
        correct_side = "left" if condition == "AB" else "right"
    else:
        correct_side = "left" if condition == "BA" else "right"
    correct_key = settings.left_key if correct_side == "left" else settings.right_key

    cue = make_unit(unit_label="cue").add_stim(stima).add_stim(stimb)
    set_trial_context(
        cue,
        trial_id=trial_id,
        phase="choice_response_window",
        deadline_s=settings.cue_duration,
        valid_keys=list(settings.key_list),
        block_id=block_id,
        condition_id=str(condition),
        task_factors={
            "condition": str(condition),
            "stage": "choice_response_window",
            "current_correct": str(controller.current_correct),
            "reversal_count": int(controller.reversal_count),
            "block_idx": block_idx,
        },
        stim_id="choice_pair",
    )
    cue.capture_response(
        keys=settings.key_list,
        correct_keys=correct_key,
        duration=settings.cue_duration,
        onset_trigger=settings.triggers.get("cue_onset") + marker_pad,
        response_trigger=settings.triggers.get("key_press") + marker_pad,
        timeout_trigger=settings.triggers.get("no_response") + marker_pad,
        terminate_on_response=False,
        highlight_stim={settings.left_key: stim_bank.get("highlight_left"), settings.right_key: stim_bank.get("highlight_right")},
        dynamic_highlight=False,
    )

    respond = cue.get_state("key_press", False)
    win_prob = controller.get_win_prob()
    if respond:
        rand_val = np.random.rand()
        hit = cue.get_state("hit", False)
        if hit:
            outcome = "win" if rand_val < win_prob else "lose"
            delta = settings.delta if rand_val < win_prob else settings.delta * -1
        else:
            outcome = "win" if rand_val < (1 - win_prob) else "lose"
            delta = settings.delta if rand_val < (1 - win_prob) else settings.delta * -1
    else:
        outcome = "no_response"
        delta = settings.delta * -1
        hit = False
        rand_val = np.nan

    cue.set_state(outcome=outcome, hit=hit, delta=delta, win_prob=win_prob, rand_val=rand_val)
    cue.to_dict(trial_data)

    controller.update(hit)

    make_unit(unit_label="blank").add_stim(stim_bank.get("blank")).show(duration=settings.blank_duration).to_dict(trial_data)

    # outcome display
    make_unit(unit_label="feedback").add_stim(stim_bank.get(f"{outcome}_feedback")).show(
        duration=settings.feedback_duration,
        onset_trigger=settings.triggers.get(f"{outcome}_feedback_onset") + marker_pad,
    ).to_dict(trial_data)

    return trial_data
