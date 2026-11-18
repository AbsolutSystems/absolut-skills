# Performance path

Used by [tech-lead](../SKILL.md#performance) for "X is slow", "make Y faster" or a measured regression, and by
[fix](../../fix/SKILL.md) for a `perf` issue. The result is a number a person can check: a verdict, the value with
its unit, the run count and range, and the limiter. Measurement scripts live in a temporary directory outside the
repository (`${TMPDIR:-/tmp}/as-perf/`) until the plan is approved; no production code before that.

## 1. Claim

Write three things before measuring anything:

- the sentence you expect to report — "export is 30% faster at p50 on the 60k-row data set";
- the decision it serves — ship the change, drop it, or buy hardware instead;
- how it is measured — an existing benchmark first; else a script or a timed request with realistic data (size and
  shape of production) and realistic concurrency. Name the command.

## 2. Baseline

Run the measurement at least 5 times on the current code. Record the median and the range (min–max). Count errors and
non-success responses, and confirm that the work actually ran inside the timed region (rows written, items returned,
a cache that was not answered from a stub). A run with errors or no work is not a data point.

## 3. Limiter

Name the resource or code path that bounds the result: CPU in a function, a query, lock waits, I/O, the network, the
allocator. Take it from a profile or counters (profiler, query plan and timing, database statistics, GC log) of a run
that is not one of the reported ones — profiling slows the code. A guess from reading the code is not a limiter.

## 4. Plan

The smallest change at the limiter, with the claim and the measurement command in the plan. The user approves the plan
before any code, as on the other paths.

## 5. After

The same measurement on the changed code. Both sides run the way production runs them (release build, same flags,
warmed up the same way, same data); alternate A and B where possible; at least 5 runs each. A difference within the
run-to-run range of either side is no measurable difference: revert the change. Slower beyond the range: revert it
too.

## 6. Report

Verdict first — **faster**, **slower**, **no measurable difference** or **inconclusive** — then:

- the number with its unit, for both sides: median, range, run count;
- the limiter, and whether the change moved it (a new limiter is named);
- the share of the end-to-end path a user waits on — "the export query went from 4.1 s to 2.6 s; the user waits 9 s
  in total, now 7.5 s".

**Inconclusive** when the limiter is not named, a side ran untuned (debug build, cold cache on one side only), or
errors and "did the work run" were not checked — say which.

## Deferred

When the user does not fix it now, offer to save it as an issue per
[../../issue/references/issue-format.md](../../issue/references/issue-format.md) with kind `perf`: the claim, the
measurement command, the baseline numbers and the limiter (or "limiter not named") as evidence; `**Source:**`
`as:tech-lead`.
