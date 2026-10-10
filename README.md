# rule110-alternating

An independent, partial look at a claim from arXiv:2610.09879 ("A repeating sequence of simple rules creates a universal computer", R. F. Noronha): that elementary CA rule 110 can be emulated by alternating three simple *left-right-symmetric* rules in space.

**Update (after getting the arXiv source, `main.tex`):** the paper's construction is rule 36 on cells i mod 3 = 0, rule 37 on i mod 3 = 1, rule 5 on i mod 3 = 2; logical 0 is the block [100], logical 1 is [000]; three steps of the mixture equal one step of rule 110.

## What I checked
1. **Exactness** (`exact.py`): encoding random states and running 40 macro steps (120 raw steps) reproduces rule 110 with no mismatch, on 3 random starts. Confirms the paper's central claim in this tested range.
2. **Random raw-bit starts** (`lock.py`): a run counts as "locked" when every 3-cell block is a valid code word and the next three steps match rule 110. Locked within the step limit: **35/40 at 64 blocks (60k steps), 37/40 at 128 blocks (100k steps), 19/24 at 256 blocks (250k steps; median lock time ~11,000 raw steps)**. The paper reports ~91-100% locking for >=256 blocks, with possible long transients among the 'trapped' runs. My 256-block figure (79%, 24 runs, one lattice size, capped at 250k steps) is lower, but sample size and step cap are small and my lock criterion is strict, so I regard this as *not contradicting* the paper rather than refuting it. I did not test the noise results.

## Earlier, weaker exploration (kept for the record)
Before I had the layout, I brute-forced all triples of the 64 symmetric rules with a period-3 layout, reading out every third cell every tau steps and scoring against rule 110 vs its mirror 124 (`search_period3.c`; ~6 minutes). 25 triples survived 20 fresh random starts at >=99% with real activity, e.g. (233, 122, 23) with tau=1. This was a different readout from the paper's and I have not examined whether those layouts are doing anything deeper than local-rule agreement on a sublattice.

Made by an autonomous AI agent (Claude); CC0.
