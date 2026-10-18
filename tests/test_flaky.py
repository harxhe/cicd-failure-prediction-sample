import os
import random


def _mode():
    flag = os.path.join(os.path.dirname(os.path.dirname(__file__)), "fail_flag.txt")
    if os.path.exists(flag):
        with open(flag) as handle:
            return handle.read().strip()
    return "FLAKY"


def test_flaky_timing():
    # Only flaky when fail_flag.txt says FLAKY (or is absent); otherwise switched off.
    if _mode() != "FLAKY":
        return
    assert random.random() > 0.3
