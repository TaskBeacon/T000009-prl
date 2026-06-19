# Task Plot Review

## Evidence Match

- Pass: task title and construct match the PRL README and task logic.
- Pass: AB and BA rows correctly show the left/right stimulus swap.
- Pass: phase order matches `src/run_trial.py` and README: Fixation -> Choice -> Blank -> Feedback.
- Pass: timing labels match config: 600-800 ms, 1500 ms, 400-600 ms, and 800 ms.
- Pass: choice response mapping is correct: F = left and J = right.
- Pass: feedback outcomes show +10, -10, and no response -10.
- Pass: reversal threshold note shows reverse after 9/10 correct.

## Visual Quality

- Pass: timeline text is readable at preview size.
- Pass: fixed title and Construct subtitle are centered.
- Pass: TaskBeacon logo lockup is borderless, top-right, and does not overlap content.
- Pass: no generated title, logo, watermark, people, devices, or decorative scene is present.
- Pass: raw timeline is preserved separately in `references/task_plot_timeline_raw.png`.

## README Embed

- Pass: `README.md` contains `## 2. Task Flow`.
- Pass: the section embeds `![Task Flow](task_flow.png)`.
- Pass: final image is saved as `task_flow.png`.
