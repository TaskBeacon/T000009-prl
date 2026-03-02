from contextlib import nullcontext
from functools import partial
from pathlib import Path

import glob
import pandas as pd
from psychopy import core

from psyflow import (
    BlockUnit,
    StimBank,
    StimUnit,
    SubInfo,
    TaskRunOptions,
    TaskSettings,
    context_from_config,
    count_down,
    initialize_exp,
    initialize_triggers,
    load_config,
    parse_task_run_options,
    runtime_context,
)

from src import Controller, run_trial


MODES = ("human", "qa", "sim")
DEFAULT_CONFIG_BY_MODE = {
    "human": "config/config.yaml",
    "qa": "config/config_qa.yaml",
    "sim": "config/config_scripted_sim.yaml",
}


def run(options: TaskRunOptions):
    """Run PRL in human/qa/sim mode with one auditable flow."""
    task_root = Path(__file__).resolve().parent
    cfg = load_config(str(options.config_path))
    print(f"[PRL] mode={options.mode} config={options.config_path}")

    output_dir: Path | None = None
    runtime_scope = nullcontext()
    runtime_ctx = None
    if options.mode in ("qa", "sim"):
        runtime_ctx = context_from_config(task_dir=task_root, config=cfg, mode=options.mode)
        output_dir = runtime_ctx.output_dir
        runtime_scope = runtime_context(runtime_ctx)

    with runtime_scope:
        if options.mode == "human":
            subform = SubInfo(cfg["subform_config"])
            subject_data = subform.collect()
        elif options.mode == "qa":
            subject_data = {"subject_id": "qa"}
        else:
            participant_id = "sim"
            if runtime_ctx is not None and runtime_ctx.session is not None:
                participant_id = str(runtime_ctx.session.participant_id or "sim")
            subject_data = {"subject_id": participant_id}

        settings = TaskSettings.from_dict(cfg["task_config"])
        if options.mode in ("qa", "sim") and output_dir is not None:
            settings.save_path = str(output_dir)
        settings.add_subinfo(subject_data)

        if options.mode == "qa" and output_dir is not None:
            output_dir.mkdir(parents=True, exist_ok=True)
            settings.res_file = str(output_dir / "qa_trace.csv")
            settings.log_file = str(output_dir / "qa_psychopy.log")
            settings.json_file = str(output_dir / "qa_settings.json")

        settings.triggers = cfg["trigger_config"]
        trigger_runtime = initialize_triggers(mock=True) if options.mode in ("qa", "sim") else initialize_triggers(cfg)

        win, kb = initialize_exp(settings)

        stim_bank_for_instruction = StimBank(win, cfg["stim_config"])
        if bool(getattr(settings, "voice_enabled", True)) and options.mode not in ("qa", "sim"):
            stim_bank_for_instruction = stim_bank_for_instruction.convert_to_voice("instruction_text", voice=settings.voice_name)
        stim_bank_for_instruction = stim_bank_for_instruction.preload_all()

        settings.controller = cfg["controller_config"]
        settings.save_to_json()

        files = sorted(glob.glob(str(task_root / "assets" / "*.png")))
        pairs = list(zip(files[::2], files[1::2]))

        trigger_runtime.send(settings.triggers.get("exp_onset"))

        instruction = StimUnit("instruction_text", win, kb, runtime=trigger_runtime).add_stim(
            stim_bank_for_instruction.get("instruction_text")
        )
        if bool(getattr(settings, "voice_enabled", True)) and options.mode not in ("qa", "sim"):
            instruction.add_stim(stim_bank_for_instruction.get("instruction_text_voice"))
        instruction.wait_and_continue()

        all_data = []
        for block_i in range(settings.total_blocks):
            if options.mode not in ("qa", "sim"):
                count_down(win, 3, color="white")

            stim_bank = StimBank(win)
            stima_img, stimb_img = pairs[block_i]
            block_stim = cfg["stim_config"].copy()
            block_stim["stima"] = dict(block_stim.get("stima", {}), image=stima_img)
            block_stim["stimb"] = dict(block_stim.get("stimb", {}), image=stimb_img)
            stim_bank.add_from_dict(block_stim)
            stim_bank.preload_all()

            controller = Controller.from_dict(settings.controller)
            block = (
                BlockUnit(
                    block_id=f"block_{block_i}",
                    block_idx=block_i,
                    settings=settings,
                    window=win,
                    keyboard=kb,
                )
                .generate_conditions()
                .on_start(lambda b: trigger_runtime.send(settings.triggers.get("block_onset")))
                .on_end(lambda b: trigger_runtime.send(settings.triggers.get("block_end")))
                .run_trial(
                    partial(run_trial, stim_bank=stim_bank, controller=controller, trigger_runtime=trigger_runtime),
                    block_id=f"block_{block_i}",
                    block_idx=block_i,
                )
                .to_dict(all_data)
            )

            block_trials = block.get_all_data()
            score = sum(trial.get("choice_delta", 0) for trial in block_trials)
            StimUnit("block", win, kb, runtime=trigger_runtime).add_stim(
                stim_bank.get_and_format(
                    "block_break",
                    block_num=block_i + 1,
                    total_blocks=settings.total_blocks,
                    score=score,
                )
            ).wait_and_continue()

        total_score = sum(trial.get("choice_delta", 0) for trial in all_data)
        StimUnit("block", win, kb, runtime=trigger_runtime).add_stim(
            stim_bank.get_and_format("good_bye", total_score=total_score)
        ).wait_and_continue(terminate=True)
        trigger_runtime.send(settings.triggers.get("exp_end"))

        df = pd.DataFrame(all_data)
        df.to_csv(settings.res_file, index=False)

        trigger_runtime.close()
        core.quit()


def main() -> None:
    task_root = Path(__file__).resolve().parent
    options = parse_task_run_options(
        task_root=task_root,
        description="Run PRL in human/qa/sim mode.",
        default_config_by_mode=DEFAULT_CONFIG_BY_MODE,
        modes=MODES,
    )
    run(options)


if __name__ == "__main__":
    main()
