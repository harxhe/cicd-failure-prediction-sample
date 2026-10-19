# CI/CD Failure Prediction: Sample App

This is the **application that gets monitored**. It is deliberately tiny. Its only job is to produce
realistic build results (passes, failures, flaky failures) for the
[CI/CD failure prediction framework](https://github.com/harxhe/cicd-failure-prediction-framework).

> **Every push to `main` starts a real AWS build and becomes a row of training data.** Don't push
> experiments or unrelated changes here.

## How it is wired

```
push to main -> CodePipeline (cicdfp-sample-app-pipeline) -> CodeBuild (cicdfp-sample-app-build)
                                                                  |
                                              build events feed the prediction framework
```

CodeBuild reads `buildspec.yml`: it installs `requirements.txt` and runs `pytest tests/ -v`. A failing
test fails the build.

## Layout

```
.
├── src/calculator.py        # small functions to test (add, divide, subtract, multiply, power)
├── tests/
│   ├── test_basic.py        # reliable tests
│   ├── test_edge_cases.py   # edge cases
│   ├── test_flaky.py        # intentionally flaky (about a 30% failure chance in FLAKY mode)
│   └── test_lever.py        # fails on purpose when fail_flag.txt says FAIL
├── fail_flag.txt            # controls the build outcome: STABLE, FAIL or FLAKY
├── gen/                     # generated modules, added by the build generator to vary commit size
├── buildspec.yml            # CodeBuild instructions
├── pytest.ini               # puts the repo root on the import path
└── requirements.txt         # pytest, pinned
```

## Controlling the build outcome

`fail_flag.txt` holds one word:

| Value | Result of the next build |
|---|---|
| `STABLE` | passes (the flaky test is switched off) |
| `FAIL` | fails on purpose |
| `FLAKY` | the flaky test is on, so roughly 30% of builds fail |

If the file is missing, the repo behaves as `FLAKY`.

You normally don't edit this by hand. The generator in the framework repo does it for you, and also
adds files under `gen/` so that each commit has a different size:

```
# run from inside THIS repo
python <path-to-framework>/tools/generate_builds.py history --dry-run   # preview a scripted series
python <path-to-framework>/tools/generate_builds.py one --mode FAIL --files 2 --lines 50
python <path-to-framework>/tools/generate_builds.py one --mode STABLE --files 2 --lines 40
```

The script checks the git remote and refuses to run in the wrong repository or with uncommitted
changes.

## Running the tests locally

```
pip install -r requirements.txt
pytest tests/ -v
```

## Why the demo needs a failure streak

The framework scores a build from the recent history of this repo. After five failed builds in a row,
the next build is predicted as high risk (score around 0.86) and an alert email is sent. A single
failure is not enough. Details are in the framework repo's `docs/specs.md`.
