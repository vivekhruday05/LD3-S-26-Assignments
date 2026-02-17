# Assignment 2 — Dependency Parsing (Transition-Based)

This workspace contains the completed implementation for the assignment “Dependency Parsing”.

## What’s implemented

**Required (Arc-Eager)**
- Full arc-eager transition function: `SH`, `RE`, `RA(label)`, `LA(label)`
- Static oracle for arc-eager (Goldberg & Nivre 2012, Algorithm 1)
- Runs on the provided `.tab` format and can emit either tree view or tab view

**Extra credit (Arc-Standard)**
- A second transition system (arc-standard) + static oracle
- Can be selected via a CLI flag

## Setup

Uses only the Python standard library.

- Python: `python3` (tested with the environment’s Python 3.13)

## Data format

Input is a blank-line separated list of sentences, with one token per line:

```
WORD<TAB>POS<TAB>HEAD_INDEX<TAB>DEPREL
```

Indices are 1-based token positions; `0` is the special ROOT.

## How to run

All runnable scripts are in `dep_starter_code/`.

### 1) Sanity check: toy transition demo

Runs the hard-coded example from the assignment PDF:

```bash
cd dep_starter_code
python3 transition.py
```

### 2) Required: arc-eager oracle parsing

Tree (pretty) output:

```bash
cd dep_starter_code
python3 oracle.py < example.tab
```

Tab output (same format as input):

```bash
cd dep_starter_code
python3 oracle.py tab < example.tab
```

Run on the full dev set and write the derived trees:

```bash
cd dep_starter_code
python3 oracle.py tab < en-ud-dev.tab > en-ud-dev.out
```

Note: If the input contains non-projective structures, a projective transition system + static oracle may not reproduce the gold tree perfectly; unattached tokens are attached to ROOT at the end (as in the starter code).

### 3) Extra credit: arc-standard system

Same input/output interface, selected by an additional argument:

```bash
cd dep_starter_code
python3 oracle.py tab arc-standard < example.tab
```

### 4) Optional: evaluate UAS/LAS vs gold

This compares oracle-derived heads/labels to the gold heads/labels in a `.tab` file.

Arc-eager:

```bash
cd dep_starter_code
python3 evaluate.py en-ud-dev.tab --system arc-eager
```

Arc-standard:

```bash
cd dep_starter_code
python3 evaluate.py en-ud-dev.tab --system arc-standard
```

### 5) Run Section 5 (Hindi Treebank Evaluation)

The `run_section5.sh` script automates the conversion of Hindi Treebank data to `.tab` format and evaluates the Arc-Eager system on it.

```bash
cd dep_starter_code
chmod +x run_section5.sh
./run_section5.sh
```

## Code map

- `dep_starter_code/arc_eager.py`: arc-eager transitions + static oracle
- `dep_starter_code/oracle.py`: sentence reader + runner (required entrypoint)
- `dep_starter_code/transition.py`: toy demo wired to arc-eager transitions
- `dep_starter_code/arc_standard.py`: extra credit transition system + oracle
- `dep_starter_code/evaluate.py`: optional scorer against gold `.tab`
