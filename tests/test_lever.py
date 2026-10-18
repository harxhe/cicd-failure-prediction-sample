import os


def _mode():
    flag = os.path.join(os.path.dirname(os.path.dirname(__file__)), "fail_flag.txt")
    if os.path.exists(flag):
        with open(flag) as handle:
            return handle.read().strip()
    return "FLAKY"


def test_forced_outcome():
    """Demo lever: the build is forced to fail when fail_flag.txt says FAIL."""
    assert _mode() != "FAIL"
