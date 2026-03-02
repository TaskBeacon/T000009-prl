from psychopy import logging


class Controller:
    """State controller for probabilistic reversal learning."""

    def __init__(
        self,
        win_prob: float,
        rev_win_prob: float,
        enable_logging: bool = True,
        sliding_window: int = 10,
        sliding_window_hits: int = 9,
    ):
        self.win_prob = float(win_prob)
        self.rev_win_prob = float(rev_win_prob)
        self.current_correct = "stima"
        self.reversal_count = 0
        self.phase_hits: list[bool] = []
        self.sliding_window = int(sliding_window)
        self.sliding_window_hits = int(sliding_window_hits)
        self.enable_logging = bool(enable_logging)

    @classmethod
    def from_dict(cls, config: dict) -> "Controller":
        """Create a controller from config values."""
        allowed = {
            "win_prob",
            "rev_win_prob",
            "enable_logging",
            "sliding_window",
            "sliding_window_hits",
        }
        extra = set(config) - allowed
        if extra:
            raise ValueError(f"[Controller.from_dict] Unknown config keys: {extra}")

        if "win_prob" not in config:
            raise ValueError("[Controller.from_dict] Missing required key: 'win_prob'")

        win_prob = config["win_prob"]
        rev_win_prob = config.get("rev_win_prob", win_prob)

        return cls(
            win_prob=win_prob,
            rev_win_prob=rev_win_prob,
            enable_logging=config.get("enable_logging", True),
            sliding_window=config.get("sliding_window", 10),
            sliding_window_hits=config.get("sliding_window_hits", 9),
        )

    def get_win_prob(self) -> float:
        """Return the active win probability for the current reversal phase."""
        return self.win_prob if self.reversal_count == 0 else self.rev_win_prob

    def update(self, hit: bool) -> None:
        """Update trial history and reverse mapping when threshold is met."""
        self.phase_hits.append(bool(hit))
        if len(self.phase_hits) > self.sliding_window:
            self.phase_hits.pop(0)

        if (
            len(self.phase_hits) == self.sliding_window
            and sum(self.phase_hits) >= self.sliding_window_hits
        ):
            old = self.current_correct
            self.current_correct = "stimb" if old == "stima" else "stima"
            self.reversal_count += 1
            self.phase_hits.clear()
            if self.enable_logging:
                logging.data(
                    f"[Controller] Reversal #{self.reversal_count}: {old} -> {self.current_correct}"
                )
