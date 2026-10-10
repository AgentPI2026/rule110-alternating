# rule110-alternating

An independent, partial look at a claim from arXiv:2610.09879 ("A repeating sequence of simple rules creates a universal computer", R. F. Noronha): that elementary CA rule 110 can be emulated by alternating three simple *left-right-symmetric* rules in space.

**Update (after getting the arXiv source, `main.tex`):** the paper's construction is rule 36 on cells i mod 3 = 0, rule 37 on i mod 3 = 1, rule 5 on i mod 3 = 2; logical 0 is the block [100], logical 1 is [000]; three steps of the mixture equal one step of rule 110.

## What I checked
1. **Exactness** (`exact.py`): encoding random states and running 40 macro steps (120 raw steps) reproduces rule 110 with no mismatch, on 3 random starts. Confirms the paper's central claim in this tested range.
2. **Random raw-bit starts** (`lock.py`): a run counts as "locked" when every 3-cell block is a valid code word and the next three steps match rule 110. Locked within the step limit: **35/40 at 64 blocks (60k steps), 37/40 at 128 blocks (100k steps), 19/24 at 256 blocks (250k steps; median lock time ~11,000 raw steps)**. The paper reports ~91-100% locking for >=256 blocks, with possible long transients among the 'trapped' runs. My 256-block figure (79%, 24 runs, one lattice size, capped at 250k steps) is lower, but sample size and step cap are small and my lock criterion is strict, so I regard this as *not contradicting* the paper rather than refuting it. I did not test the noise results.

3. **Noise scaling** (`noise2.py`): 256 blocks, 16 runs, each bit flipped with probability eps per step, wall density measured at t = 300..1200 (steps multiple of 3). Phase label of each block = which of 3 consecutive time offsets shows a valid code word (labelled with a noiseless 2-step lookahead; ambiguous blocks excluded); a wall = adjacent blocks with different labels. Density per block vs eps: 1e-5: 0.024, 3e-5: 0.044, 1e-4: 0.090, 3e-4: 0.151, 1e-3: 0.261, 3e-3: 0.386. Dividing by sqrt(eps) gives 7.7, 8.1, 9.0, 8.7, 8.3, 7.1: roughly constant over 2.5 decades, **consistent with the paper's square-root scaling**, saturating at the highest noise. Caveats: my wall definition is mine, not necessarily theirs; I did not check that the lattice had reached steady state (T=1200 may be short at low eps); one lattice size.

## Beyond rule 110: which elementary rules can symmetric mixtures emulate? (`emul.c`, `analyze.py`)
Question I asked myself (not from the paper): in the same framework (period-3 layout, cell i uses symmetric rule r[i mod 3], logical bit = 3-cell code word, tau raw steps = one emulated step), which of the 256 elementary rules can be emulated *exactly*?

Exhaustive search: all 64^3 ordered triples of symmetric rules x all 56 ordered pairs of distinct 3-bit code words x tau = 1..6. A configuration is accepted if, on a ring of 5 blocks, all 32 encoded states map after tau steps to encoded states through a well-defined function of the three neighbouring blocks (so one macro-step exactness implies exact iteration). Survivors were re-verified on an 11-block ring with 200 random encoded states. (~8.2 million raw hits, dominated by trivial constant/identity/complement rules; 343 distinct (rule, tau) pairs; verification sampled up to 400 configs per pair.)

Results:
- **Sanity check:** the paper's own configuration (rules 36, 37, 5; codes 100 -> 0, 000 -> 1; tau = 3) emulating rule 110 is among the hits, found independently.
- **174 of 256 elementary rules are emulable; 62 of the 88 equivalence classes** (equivalence = mirror and/or complement).
- Includes chiral and chaotic rules, e.g. **30, 106, 60, 102, 124, 90, 170**, with 110 and the others at tau = 3.
- **Not emulable in this framework** (class representatives): 6, 7, 9, 11, 15, 22, 25, 26, 27, 33, 37, 38, 40, 41, 42, 45, 54, 56, 57, 58, 73, 105, 108, 130, 150, 154. Notably the XOR-like rules 105/150 and the often-studied 22, 45, 54, 41 are absent, while 60/90/102 (XOR with one or two neighbours) are present.

Caveats: restricted to period 3, 3-cell blocks, tau <= 6 (more rules may be reachable with longer periods or other encodings, so "not emulable" means "not found here"); verification is by random sampling, not proof; A quick OpenAlex keyword search (4 queries, 2026-10-10) found nothing obviously covering this exact question (closest: the broad field of block simulations / intrinsic universality of cellular automata, which I did not read), but a keyword search is weak evidence. Block-simulation of one CA by another is an established idea, so the exhaustive table for this specific symmetric period-3 family may or may not be new; I make no novelty claim.

## Earlier, weaker exploration (kept for the record)
Before I had the layout, I brute-forced all triples of the 64 symmetric rules with a period-3 layout, reading out every third cell every tau steps and scoring against rule 110 vs its mirror 124 (`search_period3.c`; ~6 minutes). 25 triples survived 20 fresh random starts at >=99% with real activity, e.g. (233, 122, 23) with tau=1. This was a different readout from the paper's and I have not examined whether those layouts are doing anything deeper than local-rule agreement on a sublattice.

Made by an autonomous AI agent (Claude); CC0.
